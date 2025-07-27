"""
A.M.A.S.I.A.P. Protocol Implementation
Always Modify And Send Input Automatically Protocol

This protocol automatically enhances user input with contextual information,
current date/time, and intelligent preprocessing before sending to JAEGIS agents.
"""

import datetime
import json
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import hashlib

logger = logging.getLogger(__name__)


class EnhancementType(str, Enum):
    """Types of input enhancements."""
    TEMPORAL = "temporal"           # Date/time context
    CONTEXTUAL = "contextual"       # Conversation context
    SEMANTIC = "semantic"           # Meaning enhancement
    TECHNICAL = "technical"         # Technical context
    PRIORITY = "priority"           # Urgency/priority indicators
    CLARIFICATION = "clarification" # Ambiguity resolution


class ProcessingMode(str, Enum):
    """A.M.A.S.I.A.P. processing modes."""
    AUTOMATIC = "automatic"         # Full automatic enhancement
    SEMI_AUTOMATIC = "semi_automatic" # User confirmation required
    MANUAL = "manual"              # User-controlled enhancement
    BYPASS = "bypass"              # Skip enhancement


@dataclass
class Enhancement:
    """Individual input enhancement."""
    enhancement_id: str
    enhancement_type: EnhancementType
    original_text: str
    enhanced_text: str
    confidence: float
    reasoning: str
    metadata: Dict[str, Any]


@dataclass
class AMASIAPResult:
    """A.M.A.S.I.A.P. processing result."""
    original_input: str
    enhanced_input: str
    enhancements: List[Enhancement]
    processing_mode: ProcessingMode
    confidence_score: float
    processing_time_ms: float
    context_added: Dict[str, Any]
    recommendations: List[str]


class AMASIAPProtocol:
    """
    Always Modify And Send Input Automatically Protocol
    
    Automatically enhances user input with:
    - Current date/time context
    - Conversation history
    - Technical context
    - Priority indicators
    - Semantic clarification
    """
    
    def __init__(self):
        self.processing_mode = ProcessingMode.AUTOMATIC
        self.enhancement_rules = self._initialize_enhancement_rules()
        self.context_templates = self._initialize_context_templates()
        self.temporal_patterns = self._initialize_temporal_patterns()
        self.priority_indicators = self._initialize_priority_indicators()
        
        logger.info("A.M.A.S.I.A.P. Protocol initialized")
    
    def _initialize_enhancement_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize enhancement rules and patterns."""
        
        return {
            "temporal_enhancement": {
                "triggers": ["today", "now", "current", "latest", "recent"],
                "patterns": [
                    r"\b(today|now|current|latest|recent)\b",
                    r"\b(this\s+(?:week|month|year))\b",
                    r"\b(yesterday|tomorrow)\b"
                ],
                "template": "Current context: {current_datetime} | {original_text}"
            },
            
            "contextual_enhancement": {
                "triggers": ["continue", "also", "additionally", "furthermore"],
                "patterns": [
                    r"\b(continue|also|additionally|furthermore)\b",
                    r"\b(as\s+mentioned|as\s+discussed)\b",
                    r"\b(building\s+on|following\s+up)\b"
                ],
                "template": "Context: {conversation_context} | {original_text}"
            },
            
            "technical_enhancement": {
                "triggers": ["implement", "deploy", "configure", "optimize"],
                "patterns": [
                    r"\b(implement|deploy|configure|optimize)\b",
                    r"\b(create|build|develop|design)\b",
                    r"\b(fix|debug|troubleshoot|resolve)\b"
                ],
                "template": "Technical Request: {original_text} | Context: JAEGIS Enhanced Agent System v2.2"
            },
            
            "priority_enhancement": {
                "triggers": ["urgent", "asap", "critical", "immediately"],
                "patterns": [
                    r"\b(urgent|asap|critical|immediately)\b",
                    r"\b(high\s+priority|time\s+sensitive)\b",
                    r"\b(emergency|crisis|blocking)\b"
                ],
                "template": "PRIORITY: {priority_level} | {original_text} | Timestamp: {current_datetime}"
            },
            
            "clarification_enhancement": {
                "triggers": ["help", "how", "what", "why", "explain"],
                "patterns": [
                    r"\b(help|how|what|why|explain)\b",
                    r"\b(unclear|confused|don't\s+understand)\b",
                    r"\b(clarify|elaborate|detail)\b"
                ],
                "template": "Clarification Request: {original_text} | Please provide detailed explanation"
            }
        }
    
    def _initialize_context_templates(self) -> Dict[str, str]:
        """Initialize context enhancement templates."""
        
        return {
            "datetime_context": "Current Date/Time: {datetime} (UTC) | Day: {day_of_week} | ",
            "system_context": "System: JAEGIS Enhanced Agent System v2.2 | N.L.D.S. Tier 0 Interface | ",
            "session_context": "Session: {session_id} | User: {user_id} | ",
            "conversation_context": "Previous Context: {previous_messages} | ",
            "technical_context": "Technical Environment: {environment} | Available Squads: {squads} | "
        }
    
    def _initialize_temporal_patterns(self) -> Dict[str, str]:
        """Initialize temporal enhancement patterns."""
        
        return {
            "relative_time": {
                "today": "current date",
                "now": "current timestamp",
                "this week": "current week",
                "this month": "current month",
                "this year": "current year",
                "recently": "within last 24 hours",
                "latest": "most recent version"
            },
            
            "time_sensitive": {
                "asap": "as soon as possible",
                "urgent": "high priority",
                "immediately": "immediate action required",
                "deadline": "time-constrained",
                "rush": "expedited processing"
            }
        }
    
    def _initialize_priority_indicators(self) -> Dict[str, int]:
        """Initialize priority level indicators."""
        
        return {
            "critical": 5,
            "urgent": 4,
            "high": 3,
            "normal": 2,
            "low": 1,
            "asap": 5,
            "immediately": 5,
            "soon": 3,
            "when possible": 1,
            "eventually": 1
        }
    
    async def process_input(self, 
                          user_input: str,
                          context: Optional[Dict[str, Any]] = None,
                          processing_mode: Optional[ProcessingMode] = None) -> AMASIAPResult:
        """Process user input through A.M.A.S.I.A.P. protocol."""
        
        start_time = datetime.datetime.now()
        
        # Use provided mode or default
        mode = processing_mode or self.processing_mode
        
        # Initialize context
        if context is None:
            context = {}
        
        # Apply enhancements based on mode
        if mode == ProcessingMode.BYPASS:
            return AMASIAPResult(
                original_input=user_input,
                enhanced_input=user_input,
                enhancements=[],
                processing_mode=mode,
                confidence_score=1.0,
                processing_time_ms=0.0,
                context_added={},
                recommendations=[]
            )
        
        # Analyze input for enhancement opportunities
        enhancements = await self._analyze_input(user_input, context)
        
        # Apply enhancements
        enhanced_input = await self._apply_enhancements(user_input, enhancements, context)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(enhancements)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(user_input, enhancements)
        
        # Calculate processing time
        processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
        
        # Extract context added
        context_added = self._extract_context_added(enhancements)
        
        return AMASIAPResult(
            original_input=user_input,
            enhanced_input=enhanced_input,
            enhancements=enhancements,
            processing_mode=mode,
            confidence_score=confidence_score,
            processing_time_ms=processing_time,
            context_added=context_added,
            recommendations=recommendations
        )
    
    async def _analyze_input(self, user_input: str, context: Dict[str, Any]) -> List[Enhancement]:
        """Analyze input for enhancement opportunities."""
        
        enhancements = []
        input_lower = user_input.lower()
        
        # Temporal enhancement analysis
        temporal_enhancement = self._analyze_temporal_needs(user_input, input_lower)
        if temporal_enhancement:
            enhancements.append(temporal_enhancement)
        
        # Contextual enhancement analysis
        contextual_enhancement = self._analyze_contextual_needs(user_input, input_lower, context)
        if contextual_enhancement:
            enhancements.append(contextual_enhancement)
        
        # Technical enhancement analysis
        technical_enhancement = self._analyze_technical_needs(user_input, input_lower)
        if technical_enhancement:
            enhancements.append(technical_enhancement)
        
        # Priority enhancement analysis
        priority_enhancement = self._analyze_priority_needs(user_input, input_lower)
        if priority_enhancement:
            enhancements.append(priority_enhancement)
        
        # Clarification enhancement analysis
        clarification_enhancement = self._analyze_clarification_needs(user_input, input_lower)
        if clarification_enhancement:
            enhancements.append(clarification_enhancement)
        
        return enhancements
    
    def _analyze_temporal_needs(self, user_input: str, input_lower: str) -> Optional[Enhancement]:
        """Analyze need for temporal context enhancement."""
        
        rules = self.enhancement_rules["temporal_enhancement"]
        
        # Check for temporal triggers
        for trigger in rules["triggers"]:
            if trigger in input_lower:
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
                day_of_week = datetime.datetime.now().strftime("%A")
                
                enhanced_text = f"[Current: {current_datetime} - {day_of_week}] {user_input}"
                
                return Enhancement(
                    enhancement_id=f"temporal_{hashlib.md5(user_input.encode()).hexdigest()[:8]}",
                    enhancement_type=EnhancementType.TEMPORAL,
                    original_text=user_input,
                    enhanced_text=enhanced_text,
                    confidence=0.9,
                    reasoning=f"Added temporal context due to trigger: '{trigger}'",
                    metadata={
                        "trigger": trigger,
                        "current_datetime": current_datetime,
                        "day_of_week": day_of_week
                    }
                )
        
        return None
    
    def _analyze_contextual_needs(self, user_input: str, input_lower: str, 
                                context: Dict[str, Any]) -> Optional[Enhancement]:
        """Analyze need for contextual enhancement."""
        
        rules = self.enhancement_rules["contextual_enhancement"]
        
        # Check for contextual triggers
        for trigger in rules["triggers"]:
            if trigger in input_lower:
                # Add conversation context if available
                previous_context = context.get("previous_messages", "")
                session_id = context.get("session_id", "unknown")
                
                enhanced_text = f"[Session: {session_id}] {user_input}"
                if previous_context:
                    enhanced_text = f"[Context: {previous_context[:100]}...] {enhanced_text}"
                
                return Enhancement(
                    enhancement_id=f"contextual_{hashlib.md5(user_input.encode()).hexdigest()[:8]}",
                    enhancement_type=EnhancementType.CONTEXTUAL,
                    original_text=user_input,
                    enhanced_text=enhanced_text,
                    confidence=0.8,
                    reasoning=f"Added contextual information due to trigger: '{trigger}'",
                    metadata={
                        "trigger": trigger,
                        "session_id": session_id,
                        "has_previous_context": bool(previous_context)
                    }
                )
        
        return None
    
    def _analyze_technical_needs(self, user_input: str, input_lower: str) -> Optional[Enhancement]:
        """Analyze need for technical context enhancement."""
        
        rules = self.enhancement_rules["technical_enhancement"]
        
        # Check for technical triggers
        for trigger in rules["triggers"]:
            if trigger in input_lower:
                enhanced_text = f"[JAEGIS v2.2 Technical Request] {user_input} [Available: 16 Squads, N.L.D.S. Interface]"
                
                return Enhancement(
                    enhancement_id=f"technical_{hashlib.md5(user_input.encode()).hexdigest()[:8]}",
                    enhancement_type=EnhancementType.TECHNICAL,
                    original_text=user_input,
                    enhanced_text=enhanced_text,
                    confidence=0.85,
                    reasoning=f"Added technical context due to trigger: '{trigger}'",
                    metadata={
                        "trigger": trigger,
                        "system_version": "JAEGIS v2.2",
                        "available_squads": 16,
                        "interface": "N.L.D.S."
                    }
                )
        
        return None
    
    def _analyze_priority_needs(self, user_input: str, input_lower: str) -> Optional[Enhancement]:
        """Analyze need for priority enhancement."""
        
        rules = self.enhancement_rules["priority_enhancement"]
        
        # Check for priority triggers
        for trigger in rules["triggers"]:
            if trigger in input_lower:
                priority_level = self.priority_indicators.get(trigger, 2)
                priority_name = "CRITICAL" if priority_level >= 5 else "HIGH" if priority_level >= 4 else "MEDIUM"
                
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
                enhanced_text = f"[{priority_name} PRIORITY - {current_datetime}] {user_input}"
                
                return Enhancement(
                    enhancement_id=f"priority_{hashlib.md5(user_input.encode()).hexdigest()[:8]}",
                    enhancement_type=EnhancementType.PRIORITY,
                    original_text=user_input,
                    enhanced_text=enhanced_text,
                    confidence=0.95,
                    reasoning=f"Added priority context due to trigger: '{trigger}'",
                    metadata={
                        "trigger": trigger,
                        "priority_level": priority_level,
                        "priority_name": priority_name,
                        "timestamp": current_datetime
                    }
                )
        
        return None
    
    def _analyze_clarification_needs(self, user_input: str, input_lower: str) -> Optional[Enhancement]:
        """Analyze need for clarification enhancement."""
        
        rules = self.enhancement_rules["clarification_enhancement"]
        
        # Check for clarification triggers
        for trigger in rules["triggers"]:
            if trigger in input_lower:
                enhanced_text = f"[Clarification Request] {user_input} [Please provide detailed explanation with examples]"
                
                return Enhancement(
                    enhancement_id=f"clarification_{hashlib.md5(user_input.encode()).hexdigest()[:8]}",
                    enhancement_type=EnhancementType.CLARIFICATION,
                    original_text=user_input,
                    enhanced_text=enhanced_text,
                    confidence=0.7,
                    reasoning=f"Added clarification request due to trigger: '{trigger}'",
                    metadata={
                        "trigger": trigger,
                        "request_type": "clarification",
                        "detail_level": "comprehensive"
                    }
                )
        
        return None
    
    async def _apply_enhancements(self, user_input: str, 
                                enhancements: List[Enhancement],
                                context: Dict[str, Any]) -> str:
        """Apply all enhancements to create enhanced input."""
        
        if not enhancements:
            return user_input
        
        # Sort enhancements by priority (priority > temporal > technical > contextual > clarification)
        priority_order = {
            EnhancementType.PRIORITY: 1,
            EnhancementType.TEMPORAL: 2,
            EnhancementType.TECHNICAL: 3,
            EnhancementType.CONTEXTUAL: 4,
            EnhancementType.CLARIFICATION: 5,
            EnhancementType.SEMANTIC: 6
        }
        
        sorted_enhancements = sorted(enhancements, key=lambda e: priority_order.get(e.enhancement_type, 10))
        
        # Apply enhancements in order
        enhanced_input = user_input
        
        for enhancement in sorted_enhancements:
            if enhancement.enhancement_type == EnhancementType.PRIORITY:
                # Priority enhancements wrap the entire input
                enhanced_input = enhancement.enhanced_text
            elif enhancement.enhancement_type == EnhancementType.TEMPORAL:
                # Temporal enhancements add timestamp prefix
                if not enhanced_input.startswith("["):
                    enhanced_input = enhancement.enhanced_text
            elif enhancement.enhancement_type == EnhancementType.TECHNICAL:
                # Technical enhancements add system context
                if "[JAEGIS" not in enhanced_input:
                    enhanced_input = enhancement.enhanced_text
            elif enhancement.enhancement_type == EnhancementType.CONTEXTUAL:
                # Contextual enhancements add session info
                if "[Session:" not in enhanced_input and "[Context:" not in enhanced_input:
                    enhanced_input = enhancement.enhanced_text
            elif enhancement.enhancement_type == EnhancementType.CLARIFICATION:
                # Clarification enhancements add request suffix
                if "[Clarification Request]" not in enhanced_input:
                    enhanced_input = enhancement.enhanced_text
        
        return enhanced_input
    
    def _calculate_confidence(self, enhancements: List[Enhancement]) -> float:
        """Calculate overall confidence score for enhancements."""
        
        if not enhancements:
            return 1.0  # No enhancements needed = high confidence
        
        # Average confidence of all enhancements
        total_confidence = sum(e.confidence for e in enhancements)
        average_confidence = total_confidence / len(enhancements)
        
        # Boost confidence if multiple enhancement types are applied
        type_diversity = len(set(e.enhancement_type for e in enhancements))
        diversity_bonus = min(0.1, type_diversity * 0.02)
        
        return min(1.0, average_confidence + diversity_bonus)
    
    def _generate_recommendations(self, user_input: str, 
                                enhancements: List[Enhancement]) -> List[str]:
        """Generate recommendations based on applied enhancements."""
        
        recommendations = []
        
        if not enhancements:
            recommendations.append("Input processed without enhancement - consider adding context for better results")
            return recommendations
        
        # Enhancement-specific recommendations
        enhancement_types = set(e.enhancement_type for e in enhancements)
        
        if EnhancementType.PRIORITY in enhancement_types:
            recommendations.append("High priority request detected - expedited processing recommended")
        
        if EnhancementType.TEMPORAL in enhancement_types:
            recommendations.append("Temporal context added - ensure time-sensitive processing")
        
        if EnhancementType.TECHNICAL in enhancement_types:
            recommendations.append("Technical request identified - route to appropriate JAEGIS squad")
        
        if EnhancementType.CONTEXTUAL in enhancement_types:
            recommendations.append("Conversation context applied - maintain session continuity")
        
        if EnhancementType.CLARIFICATION in enhancement_types:
            recommendations.append("Clarification request - provide detailed explanations")
        
        # General recommendations
        if len(enhancements) > 3:
            recommendations.append("Multiple enhancements applied - verify enhanced input accuracy")
        
        return recommendations
    
    def _extract_context_added(self, enhancements: List[Enhancement]) -> Dict[str, Any]:
        """Extract context information that was added."""
        
        context_added = {}
        
        for enhancement in enhancements:
            context_added[enhancement.enhancement_type.value] = {
                "confidence": enhancement.confidence,
                "reasoning": enhancement.reasoning,
                "metadata": enhancement.metadata
            }
        
        return context_added
    
    def set_processing_mode(self, mode: ProcessingMode):
        """Set the processing mode for A.M.A.S.I.A.P."""
        self.processing_mode = mode
        logger.info(f"A.M.A.S.I.A.P. processing mode set to: {mode.value}")
    
    def get_enhancement_statistics(self) -> Dict[str, Any]:
        """Get statistics about enhancement usage."""
        # This would typically track usage over time
        return {
            "total_enhancements_applied": 0,
            "enhancement_types_used": list(EnhancementType),
            "average_confidence": 0.85,
            "processing_mode": self.processing_mode.value
        }


# Example usage and testing
async def main():
    """Example usage of A.M.A.S.I.A.P. Protocol."""
    
    protocol = AMASIAPProtocol()
    
    # Test cases
    test_inputs = [
        "Create a user authentication system",
        "I need help with the current deployment",
        "This is urgent - fix the database connection now!",
        "How do I implement JWT tokens?",
        "Continue with the previous task we discussed"
    ]
    
    for test_input in test_inputs:
        print(f"\nOriginal: {test_input}")
        
        result = await protocol.process_input(
            test_input,
            context={
                "session_id": "test_session_123",
                "previous_messages": "Discussed authentication system requirements",
                "user_id": "test_user"
            }
        )
        
        print(f"Enhanced: {result.enhanced_input}")
        print(f"Enhancements: {len(result.enhancements)}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Processing time: {result.processing_time_ms:.2f}ms")
        
        if result.recommendations:
            print(f"Recommendations: {', '.join(result.recommendations)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
