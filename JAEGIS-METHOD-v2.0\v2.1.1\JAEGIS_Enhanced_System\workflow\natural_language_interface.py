"""
JAEGIS Enhanced System v2.0 - Natural Language Interface for Workflow Configuration
Implements natural language processing for workflow modifications with intelligent parsing and voice-to-text capability
Provides conversational interface for workflow adjustments during active sessions
"""

import asyncio
import logging
import re
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import uuid

from .workflow_sequence_engine import WorkflowSequenceEngine, WorkflowOperation, WorkflowTemplate
from .feature_toggle_system import FeatureToggleSystem, ToggleMode

logger = logging.getLogger(__name__)

class CommandType(Enum):
    """Types of natural language commands"""
    SEQUENCE_MODIFICATION = "sequence_modification"
    FEATURE_TOGGLE = "feature_toggle"
    TEMPLATE_APPLICATION = "template_application"
    MODE_CHANGE = "mode_change"
    QUERY_STATUS = "query_status"
    HELP_REQUEST = "help_request"
    CONFIRMATION = "confirmation"
    CANCELLATION = "cancellation"

class IntentConfidence(Enum):
    """Confidence levels for intent recognition"""
    HIGH = "high"        # 90%+ confidence
    MEDIUM = "medium"    # 70-89% confidence
    LOW = "low"         # 50-69% confidence
    UNCLEAR = "unclear"  # <50% confidence

@dataclass
class ParsedCommand:
    """Parsed natural language command"""
    command_id: str
    original_text: str
    command_type: CommandType
    intent: str
    confidence: IntentConfidence
    parameters: Dict[str, Any]
    entities: List[Dict[str, Any]]
    requires_confirmation: bool
    suggested_action: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_id": self.command_id,
            "original_text": self.original_text,
            "command_type": self.command_type.value,
            "intent": self.intent,
            "confidence": self.confidence.value,
            "parameters": self.parameters,
            "entities": self.entities,
            "requires_confirmation": self.requires_confirmation,
            "suggested_action": self.suggested_action
        }

@dataclass
class ConversationContext:
    """Context for ongoing conversation"""
    session_id: str
    conversation_history: List[Dict[str, Any]]
    pending_confirmations: List[ParsedCommand]
    user_preferences: Dict[str, Any]
    last_interaction: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "pending_confirmations": [cmd.to_dict() for cmd in self.pending_confirmations],
            "user_preferences": self.user_preferences,
            "last_interaction": self.last_interaction.isoformat()
        }

class NaturalLanguageInterface:
    """Natural language interface for workflow configuration"""
    
    def __init__(self, workflow_engine: WorkflowSequenceEngine, feature_toggle_system: FeatureToggleSystem):
        # Core components
        self.workflow_engine = workflow_engine
        self.feature_toggle_system = feature_toggle_system
        
        # NLP components
        self.intent_recognizer = IntentRecognizer()
        self.entity_extractor = EntityExtractor()
        self.command_parser = CommandParser()
        self.response_generator = ResponseGenerator()
        
        # Voice interface
        self.voice_interface = VoiceInterface()
        
        # Conversation management
        self.active_sessions: Dict[str, ConversationContext] = {}
        self.command_patterns = self._initialize_command_patterns()
        
        # Statistics
        self.interface_stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "voice_commands": 0,
            "text_commands": 0
        }
        
        logger.info("Natural Language Interface initialized")
    
    def _initialize_command_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize natural language command patterns"""
        
        return {
            "sequence_modification": [
                {
                    "pattern": r"move\s+(.+?)\s+(?:to\s+)?(?:happen\s+)?(?:before|after)\s+(.+)",
                    "intent": "reorder_operations",
                    "parameters": ["operation1", "operation2", "position"]
                },
                {
                    "pattern": r"set\s+(.+?)\s+(?:to\s+)?priority\s+(\d+)",
                    "intent": "set_priority",
                    "parameters": ["operation", "priority"]
                },
                {
                    "pattern": r"change\s+(.+?)\s+priority\s+to\s+(\d+)",
                    "intent": "set_priority",
                    "parameters": ["operation", "priority"]
                },
                {
                    "pattern": r"make\s+(.+?)\s+(?:run\s+)?(?:in\s+)?parallel\s+(?:with\s+)?(.+)",
                    "intent": "set_parallel",
                    "parameters": ["operation1", "operation2"]
                }
            ],
            "feature_toggle": [
                {
                    "pattern": r"(?:disable|turn\s+off|deactivate)\s+(.+)",
                    "intent": "disable_feature",
                    "parameters": ["feature"]
                },
                {
                    "pattern": r"(?:enable|turn\s+on|activate)\s+(.+)",
                    "intent": "enable_feature",
                    "parameters": ["feature"]
                },
                {
                    "pattern": r"toggle\s+(.+)",
                    "intent": "toggle_feature",
                    "parameters": ["feature"]
                },
                {
                    "pattern": r"(?:disable|turn\s+off)\s+(?:all\s+)?(.+?)\s+features",
                    "intent": "disable_category",
                    "parameters": ["category"]
                }
            ],
            "template_application": [
                {
                    "pattern": r"(?:use|apply|switch\s+to)\s+(.+?)\s+(?:template|mode|workflow)",
                    "intent": "apply_template",
                    "parameters": ["template"]
                },
                {
                    "pattern": r"(?:set|change)\s+(?:to\s+)?(.+?)\s+(?:template|mode)",
                    "intent": "apply_template",
                    "parameters": ["template"]
                }
            ],
            "mode_change": [
                {
                    "pattern": r"(?:enable|activate)\s+(.+?)\s+mode",
                    "intent": "enable_mode",
                    "parameters": ["mode"]
                },
                {
                    "pattern": r"(?:switch\s+to|use)\s+(.+?)\s+mode",
                    "intent": "enable_mode",
                    "parameters": ["mode"]
                }
            ],
            "query_status": [
                {
                    "pattern": r"(?:what|show|display)\s+(?:is\s+)?(?:the\s+)?(?:current\s+)?(?:workflow\s+)?(?:sequence|status|configuration)",
                    "intent": "show_current_sequence",
                    "parameters": []
                },
                {
                    "pattern": r"(?:list|show)\s+(?:all\s+)?(?:available\s+)?(?:features|templates|modes)",
                    "intent": "list_available",
                    "parameters": ["type"]
                },
                {
                    "pattern": r"(?:how\s+long|what\s+is\s+the\s+estimated\s+time)",
                    "intent": "show_time_estimate",
                    "parameters": []
                }
            ],
            "help_request": [
                {
                    "pattern": r"(?:help|what\s+can\s+i\s+do|commands|options)",
                    "intent": "show_help",
                    "parameters": []
                },
                {
                    "pattern": r"how\s+(?:do\s+i|to)\s+(.+)",
                    "intent": "show_specific_help",
                    "parameters": ["topic"]
                }
            ]
        }
    
    async def process_natural_language_command(self, text: str, session_id: str = None, 
                                             voice_input: bool = False) -> Dict[str, Any]:
        """Process natural language command"""
        
        # Create or get session
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = ConversationContext(
                session_id=session_id,
                conversation_history=[],
                pending_confirmations=[],
                user_preferences={},
                last_interaction=datetime.now()
            )
        
        session = self.active_sessions[session_id]
        
        # Parse command
        parsed_command = await self._parse_command(text, session)
        
        # Add to conversation history
        session.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": text,
            "parsed_command": parsed_command.to_dict(),
            "voice_input": voice_input
        })
        
        # Update statistics
        self.interface_stats["total_commands"] += 1
        if voice_input:
            self.interface_stats["voice_commands"] += 1
        else:
            self.interface_stats["text_commands"] += 1
        
        # Process command
        try:
            result = await self._execute_command(parsed_command, session)
            
            if result.get("success"):
                self.interface_stats["successful_commands"] += 1
            else:
                self.interface_stats["failed_commands"] += 1
            
            # Generate response
            response = await self.response_generator.generate_response(
                parsed_command, result, session
            )
            
            # Add response to history
            session.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "system_response": response,
                "execution_result": result
            })
            
            session.last_interaction = datetime.now()
            
            return {
                "success": True,
                "session_id": session_id,
                "parsed_command": parsed_command.to_dict(),
                "execution_result": result,
                "response": response,
                "requires_confirmation": parsed_command.requires_confirmation
            }
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.interface_stats["failed_commands"] += 1
            
            error_response = await self.response_generator.generate_error_response(
                parsed_command, str(e), session
            )
            
            return {
                "success": False,
                "session_id": session_id,
                "error": str(e),
                "response": error_response
            }
    
    async def _parse_command(self, text: str, session: ConversationContext) -> ParsedCommand:
        """Parse natural language command"""
        
        # Clean and normalize text
        normalized_text = self._normalize_text(text)
        
        # Recognize intent
        intent_result = await self.intent_recognizer.recognize_intent(
            normalized_text, self.command_patterns, session
        )
        
        # Extract entities
        entities = await self.entity_extractor.extract_entities(
            normalized_text, intent_result["command_type"]
        )
        
        # Parse parameters
        parameters = await self.command_parser.parse_parameters(
            normalized_text, intent_result, entities
        )
        
        # Determine if confirmation is required
        requires_confirmation = self._requires_confirmation(
            intent_result["command_type"], intent_result["intent"], parameters
        )
        
        # Generate suggested action
        suggested_action = await self._generate_suggested_action(
            intent_result, parameters, entities
        )
        
        return ParsedCommand(
            command_id=str(uuid.uuid4()),
            original_text=text,
            command_type=intent_result["command_type"],
            intent=intent_result["intent"],
            confidence=intent_result["confidence"],
            parameters=parameters,
            entities=entities,
            requires_confirmation=requires_confirmation,
            suggested_action=suggested_action
        )
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for processing"""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Handle common abbreviations and synonyms
        replacements = {
            "docs": "documentation",
            "qa": "quality assurance",
            "ai": "intelligence",
            "perf": "performance",
            "opt": "optimization",
            "config": "configuration",
            "sync": "synchronization"
        }
        
        for abbrev, full in replacements.items():
            text = re.sub(rf'\b{abbrev}\b', full, text)
        
        return text
    
    async def _execute_command(self, command: ParsedCommand, session: ConversationContext) -> Dict[str, Any]:
        """Execute parsed command"""
        
        if command.command_type == CommandType.SEQUENCE_MODIFICATION:
            return await self._execute_sequence_modification(command)
        
        elif command.command_type == CommandType.FEATURE_TOGGLE:
            return await self._execute_feature_toggle(command)
        
        elif command.command_type == CommandType.TEMPLATE_APPLICATION:
            return await self._execute_template_application(command)
        
        elif command.command_type == CommandType.MODE_CHANGE:
            return await self._execute_mode_change(command)
        
        elif command.command_type == CommandType.QUERY_STATUS:
            return await self._execute_query_status(command)
        
        elif command.command_type == CommandType.HELP_REQUEST:
            return await self._execute_help_request(command)
        
        elif command.command_type == CommandType.CONFIRMATION:
            return await self._execute_confirmation(command, session)
        
        elif command.command_type == CommandType.CANCELLATION:
            return await self._execute_cancellation(command, session)
        
        else:
            return {"error": f"Unknown command type: {command.command_type.value}"}
    
    async def _execute_sequence_modification(self, command: ParsedCommand) -> Dict[str, Any]:
        """Execute sequence modification command"""
        
        if command.intent == "set_priority":
            operation_name = command.parameters.get("operation")
            priority = command.parameters.get("priority")
            
            # Map operation name to WorkflowOperation
            operation = self._map_operation_name(operation_name)
            if not operation:
                return {"error": f"Unknown operation: {operation_name}"}
            
            return await self.workflow_engine.modify_sequence_priority(operation, int(priority))
        
        elif command.intent == "reorder_operations":
            # Implementation for reordering operations
            return {"success": True, "message": "Operation reordering not yet implemented"}
        
        elif command.intent == "set_parallel":
            # Implementation for setting parallel execution
            return {"success": True, "message": "Parallel execution setting not yet implemented"}
        
        else:
            return {"error": f"Unknown sequence modification intent: {command.intent}"}
    
    async def _execute_feature_toggle(self, command: ParsedCommand) -> Dict[str, Any]:
        """Execute feature toggle command"""
        
        if command.intent in ["enable_feature", "disable_feature", "toggle_feature"]:
            feature_name = command.parameters.get("feature")
            enabled = command.intent == "enable_feature"
            
            if command.intent == "toggle_feature":
                # Get current state and toggle
                current_states = self.feature_toggle_system.get_feature_states_display()
                # Find feature and toggle its state
                # Implementation would determine current state and toggle
                enabled = True  # Placeholder
            
            # Map feature name to feature ID
            feature_id = self._map_feature_name(feature_name)
            if not feature_id:
                return {"error": f"Unknown feature: {feature_name}"}
            
            return await self.feature_toggle_system.toggle_feature(feature_id, enabled)
        
        elif command.intent == "disable_category":
            category = command.parameters.get("category")
            # Implementation for disabling feature category
            return {"success": True, "message": f"Category {category} toggle not yet implemented"}
        
        else:
            return {"error": f"Unknown feature toggle intent: {command.intent}"}
    
    async def _execute_template_application(self, command: ParsedCommand) -> Dict[str, Any]:
        """Execute template application command"""
        
        template_name = command.parameters.get("template")
        
        # Map template name to WorkflowTemplate
        template = self._map_template_name(template_name)
        if not template:
            return {"error": f"Unknown template: {template_name}"}
        
        return await self.workflow_engine.apply_template(template)
    
    async def _execute_mode_change(self, command: ParsedCommand) -> Dict[str, Any]:
        """Execute mode change command"""
        
        mode_name = command.parameters.get("mode")
        
        # Map mode name to ToggleMode
        mode = self._map_mode_name(mode_name)
        if not mode:
            return {"error": f"Unknown mode: {mode_name}"}
        
        return await self.feature_toggle_system.apply_toggle_mode(mode)
    
    async def _execute_query_status(self, command: ParsedCommand) -> Dict[str, Any]:
        """Execute status query command"""
        
        if command.intent == "show_current_sequence":
            return self.workflow_engine.get_current_sequence_display()
        
        elif command.intent == "list_available":
            list_type = command.parameters.get("type", "all")
            
            result = {}
            if list_type in ["all", "templates"]:
                result["templates"] = self.workflow_engine.get_available_templates()
            
            if list_type in ["all", "features"]:
                result["features"] = self.feature_toggle_system.get_feature_states_display()
            
            if list_type in ["all", "modes"]:
                result["modes"] = [mode.value for mode in ToggleMode]
            
            return {"success": True, "data": result}
        
        elif command.intent == "show_time_estimate":
            sequence_display = self.workflow_engine.get_current_sequence_display()
            if "error" in sequence_display:
                return sequence_display
            
            return {
                "success": True,
                "estimated_duration": sequence_display["total_estimated_duration"],
                "unit": "minutes"
            }
        
        else:
            return {"error": f"Unknown query intent: {command.intent}"}
    
    async def _execute_help_request(self, command: ParsedCommand) -> Dict[str, Any]:
        """Execute help request command"""
        
        if command.intent == "show_help":
            return {
                "success": True,
                "help_content": self._generate_general_help()
            }
        
        elif command.intent == "show_specific_help":
            topic = command.parameters.get("topic")
            return {
                "success": True,
                "help_content": self._generate_specific_help(topic)
            }
        
        else:
            return {"error": f"Unknown help intent: {command.intent}"}
    
    async def _execute_confirmation(self, command: ParsedCommand, session: ConversationContext) -> Dict[str, Any]:
        """Execute confirmation command"""
        
        if session.pending_confirmations:
            pending_command = session.pending_confirmations.pop(0)
            # Execute the pending command
            return await self._execute_command(pending_command, session)
        else:
            return {"error": "No pending confirmations"}
    
    async def _execute_cancellation(self, command: ParsedCommand, session: ConversationContext) -> Dict[str, Any]:
        """Execute cancellation command"""
        
        if session.pending_confirmations:
            cancelled_command = session.pending_confirmations.pop(0)
            return {
                "success": True,
                "message": f"Cancelled: {cancelled_command.suggested_action}"
            }
        else:
            return {"error": "No pending operations to cancel"}
    
    def _map_operation_name(self, name: str) -> Optional[WorkflowOperation]:
        """Map operation name to WorkflowOperation enum"""
        
        name_mappings = {
            "web research": WorkflowOperation.DEEP_WEB_RESEARCH,
            "research": WorkflowOperation.DEEP_WEB_RESEARCH,
            "task generation": WorkflowOperation.TASK_HIERARCHY_GENERATION,
            "task hierarchy": WorkflowOperation.TASK_HIERARCHY_GENERATION,
            "tasks": WorkflowOperation.TASK_HIERARCHY_GENERATION,
            "agent coordination": WorkflowOperation.AGENT_COORDINATION,
            "coordination": WorkflowOperation.AGENT_COORDINATION,
            "agents": WorkflowOperation.AGENT_COORDINATION,
            "quality validation": WorkflowOperation.QUALITY_VALIDATION,
            "validation": WorkflowOperation.QUALITY_VALIDATION,
            "quality": WorkflowOperation.QUALITY_VALIDATION,
            "documentation": WorkflowOperation.DOCUMENTATION_CREATION,
            "docs": WorkflowOperation.DOCUMENTATION_CREATION,
            "project execution": WorkflowOperation.PROJECT_EXECUTION,
            "execution": WorkflowOperation.PROJECT_EXECUTION,
            "temporal coordination": WorkflowOperation.TEMPORAL_COORDINATION,
            "temporal": WorkflowOperation.TEMPORAL_COORDINATION,
            "performance": WorkflowOperation.PERFORMANCE_OPTIMIZATION,
            "optimization": WorkflowOperation.PERFORMANCE_OPTIMIZATION,
            "intelligence": WorkflowOperation.INTELLIGENCE_ENHANCEMENT,
            "ai": WorkflowOperation.INTELLIGENCE_ENHANCEMENT,
            "scalability": WorkflowOperation.SCALABILITY_MANAGEMENT,
            "scaling": WorkflowOperation.SCALABILITY_MANAGEMENT
        }
        
        return name_mappings.get(name.lower())
    
    def _map_feature_name(self, name: str) -> Optional[str]:
        """Map feature name to feature ID"""
        
        # Get all feature definitions
        feature_states = self.feature_toggle_system.get_feature_states_display()
        if "error" in feature_states:
            return None
        
        # Search through features by name
        for category_features in feature_states["features_by_category"].values():
            for feature in category_features:
                if name.lower() in feature["name"].lower() or name.lower() in feature["description"].lower():
                    return feature["feature_id"]
        
        return None
    
    def _map_template_name(self, name: str) -> Optional[WorkflowTemplate]:
        """Map template name to WorkflowTemplate enum"""
        
        name_mappings = {
            "research first": WorkflowTemplate.RESEARCH_FIRST,
            "research-first": WorkflowTemplate.RESEARCH_FIRST,
            "rapid execution": WorkflowTemplate.RAPID_EXECUTION,
            "rapid": WorkflowTemplate.RAPID_EXECUTION,
            "speed": WorkflowTemplate.RAPID_EXECUTION,
            "fast": WorkflowTemplate.RAPID_EXECUTION,
            "quality focused": WorkflowTemplate.QUALITY_FOCUSED,
            "quality-focused": WorkflowTemplate.QUALITY_FOCUSED,
            "quality": WorkflowTemplate.QUALITY_FOCUSED,
            "balanced": WorkflowTemplate.BALANCED_APPROACH,
            "balanced approach": WorkflowTemplate.BALANCED_APPROACH,
            "default": WorkflowTemplate.BALANCED_APPROACH
        }
        
        return name_mappings.get(name.lower())
    
    def _map_mode_name(self, name: str) -> Optional[ToggleMode]:
        """Map mode name to ToggleMode enum"""
        
        name_mappings = {
            "speed": ToggleMode.SPEED_MODE,
            "speed mode": ToggleMode.SPEED_MODE,
            "fast": ToggleMode.SPEED_MODE,
            "rapid": ToggleMode.SPEED_MODE,
            "quality": ToggleMode.QUALITY_MODE,
            "quality mode": ToggleMode.QUALITY_MODE,
            "minimal": ToggleMode.MINIMAL_MODE,
            "minimal mode": ToggleMode.MINIMAL_MODE,
            "basic": ToggleMode.MINIMAL_MODE,
            "research": ToggleMode.RESEARCH_MODE,
            "research mode": ToggleMode.RESEARCH_MODE,
            "custom": ToggleMode.CUSTOM_MODE,
            "custom mode": ToggleMode.CUSTOM_MODE
        }
        
        return name_mappings.get(name.lower())
    
    def _requires_confirmation(self, command_type: CommandType, intent: str, parameters: Dict[str, Any]) -> bool:
        """Determine if command requires confirmation"""
        
        # High-impact operations require confirmation
        high_impact_intents = [
            "disable_feature",
            "disable_category",
            "apply_template",
            "enable_mode"
        ]
        
        return intent in high_impact_intents
    
    async def _generate_suggested_action(self, intent_result: Dict[str, Any], 
                                       parameters: Dict[str, Any], entities: List[Dict[str, Any]]) -> str:
        """Generate suggested action description"""
        
        command_type = intent_result["command_type"]
        intent = intent_result["intent"]
        
        if command_type == CommandType.SEQUENCE_MODIFICATION:
            if intent == "set_priority":
                return f"Set {parameters.get('operation', 'operation')} priority to {parameters.get('priority', 'N/A')}"
        
        elif command_type == CommandType.FEATURE_TOGGLE:
            if intent == "enable_feature":
                return f"Enable {parameters.get('feature', 'feature')}"
            elif intent == "disable_feature":
                return f"Disable {parameters.get('feature', 'feature')}"
        
        elif command_type == CommandType.TEMPLATE_APPLICATION:
            return f"Apply {parameters.get('template', 'template')} workflow template"
        
        elif command_type == CommandType.MODE_CHANGE:
            return f"Switch to {parameters.get('mode', 'mode')} mode"
        
        return "Execute command"
    
    def _generate_general_help(self) -> str:
        """Generate general help content"""
        
        return """
**JAEGIS Workflow Configuration - Natural Language Commands**

**Sequence Modification:**
- "Move web research to priority 1"
- "Set task generation priority to 3"
- "Change documentation priority to 5"

**Feature Toggle:**
- "Disable comprehensive web research"
- "Enable quality validation"
- "Turn off documentation generation"

**Template Application:**
- "Use research-first template"
- "Apply rapid execution workflow"
- "Switch to quality-focused mode"

**Status Queries:**
- "Show current workflow sequence"
- "What is the estimated time?"
- "List available templates"

**Voice Commands:**
- All text commands work with voice input
- Say "help" for assistance
- Say "confirm" or "cancel" for pending actions

**Examples:**
- "Disable documentation and use speed mode"
- "Move quality validation before project execution"
- "Show me the current configuration"
"""
    
    def _generate_specific_help(self, topic: str) -> str:
        """Generate specific help content"""
        
        help_topics = {
            "sequence": "Use commands like 'move X to priority Y' or 'set X priority to Y'",
            "features": "Use 'enable/disable [feature name]' or 'turn on/off [feature]'",
            "templates": "Use 'apply [template name]' or 'use [template] template'",
            "modes": "Use 'enable [mode] mode' or 'switch to [mode] mode'",
            "voice": "Speak naturally - all text commands work with voice input"
        }
        
        return help_topics.get(topic.lower(), f"No specific help available for '{topic}'")
    
    async def process_voice_command(self, audio_data: bytes, session_id: str = None) -> Dict[str, Any]:
        """Process voice command using speech-to-text"""
        
        try:
            # Convert speech to text
            text = await self.voice_interface.speech_to_text(audio_data)
            
            if not text:
                return {
                    "success": False,
                    "error": "Could not understand voice command",
                    "response": "I couldn't understand what you said. Please try again."
                }
            
            # Process as natural language command
            return await self.process_natural_language_command(text, session_id, voice_input=True)
            
        except Exception as e:
            logger.error(f"Voice command processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "Sorry, I had trouble processing your voice command."
            }
    
    def get_conversation_history(self, session_id: str) -> Dict[str, Any]:
        """Get conversation history for a session"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        return {
            "session_id": session_id,
            "conversation_history": session.conversation_history,
            "pending_confirmations": [cmd.to_dict() for cmd in session.pending_confirmations],
            "last_interaction": session.last_interaction.isoformat()
        }
    
    def get_interface_statistics(self) -> Dict[str, Any]:
        """Get natural language interface statistics"""
        
        return {
            "interface_statistics": self.interface_stats.copy(),
            "active_sessions": len(self.active_sessions),
            "success_rate": (
                self.interface_stats["successful_commands"] / 
                max(self.interface_stats["total_commands"], 1)
            ),
            "voice_usage_rate": (
                self.interface_stats["voice_commands"] / 
                max(self.interface_stats["total_commands"], 1)
            )
        }

# Supporting classes (simplified implementations)
class IntentRecognizer:
    """Recognizes intent from natural language"""
    
    async def recognize_intent(self, text: str, patterns: Dict[str, List[Dict[str, Any]]], 
                             session: ConversationContext) -> Dict[str, Any]:
        """Recognize intent from text"""
        
        # Simple pattern matching implementation
        for command_type, pattern_list in patterns.items():
            for pattern_info in pattern_list:
                if re.search(pattern_info["pattern"], text):
                    return {
                        "command_type": CommandType(command_type),
                        "intent": pattern_info["intent"],
                        "confidence": IntentConfidence.HIGH,
                        "pattern_matched": pattern_info["pattern"]
                    }
        
        return {
            "command_type": CommandType.HELP_REQUEST,
            "intent": "unclear_command",
            "confidence": IntentConfidence.UNCLEAR,
            "pattern_matched": None
        }

class EntityExtractor:
    """Extracts entities from natural language"""
    
    async def extract_entities(self, text: str, command_type: CommandType) -> List[Dict[str, Any]]:
        """Extract entities from text"""
        
        entities = []
        
        # Extract numbers (priorities, durations, etc.)
        numbers = re.findall(r'\b\d+\b', text)
        for number in numbers:
            entities.append({
                "type": "number",
                "value": int(number),
                "text": number
            })
        
        # Extract operation names
        operation_keywords = ["research", "task", "agent", "quality", "documentation", "execution"]
        for keyword in operation_keywords:
            if keyword in text:
                entities.append({
                    "type": "operation",
                    "value": keyword,
                    "text": keyword
                })
        
        return entities

class CommandParser:
    """Parses command parameters"""
    
    async def parse_parameters(self, text: str, intent_result: Dict[str, Any], 
                             entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse parameters from text and entities"""
        
        parameters = {}
        
        # Extract parameters based on intent
        intent = intent_result["intent"]
        
        if intent == "set_priority":
            # Find operation and priority
            for entity in entities:
                if entity["type"] == "number":
                    parameters["priority"] = entity["value"]
                elif entity["type"] == "operation":
                    parameters["operation"] = entity["value"]
        
        elif intent in ["enable_feature", "disable_feature", "toggle_feature"]:
            # Extract feature name (everything after enable/disable/toggle)
            words = text.split()
            if len(words) > 1:
                parameters["feature"] = " ".join(words[1:])
        
        elif intent == "apply_template":
            # Extract template name
            template_keywords = ["research", "rapid", "quality", "balanced"]
            for keyword in template_keywords:
                if keyword in text:
                    parameters["template"] = keyword
        
        return parameters

class ResponseGenerator:
    """Generates natural language responses"""
    
    async def generate_response(self, command: ParsedCommand, result: Dict[str, Any], 
                              session: ConversationContext) -> str:
        """Generate response to command"""
        
        if result.get("success"):
            if command.command_type == CommandType.SEQUENCE_MODIFICATION:
                return f"✅ Successfully updated workflow sequence: {command.suggested_action}"
            elif command.command_type == CommandType.FEATURE_TOGGLE:
                return f"✅ Feature toggle applied: {command.suggested_action}"
            elif command.command_type == CommandType.TEMPLATE_APPLICATION:
                return f"✅ Template applied: {command.suggested_action}"
            else:
                return "✅ Command executed successfully"
        else:
            error = result.get("error", "Unknown error")
            return f"❌ Error: {error}"
    
    async def generate_error_response(self, command: ParsedCommand, error: str, 
                                    session: ConversationContext) -> str:
        """Generate error response"""
        
        return f"❌ Sorry, I couldn't process that command. Error: {error}\n\nTry saying 'help' for available commands."

class VoiceInterface:
    """Voice interface for speech-to-text"""
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text"""
        
        # Placeholder implementation
        # In a real implementation, this would use a speech-to-text service
        # like Google Speech-to-Text, Azure Speech, or OpenAI Whisper
        
        logger.info("Voice command received (speech-to-text not implemented)")
        return "show current workflow sequence"  # Placeholder response
