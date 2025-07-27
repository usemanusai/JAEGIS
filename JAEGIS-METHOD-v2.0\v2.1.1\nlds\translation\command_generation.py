"""
N.L.D.S. Command Generation Engine
Advanced command generation with standardized JAEGIS syntax and parameter mapping
"""

import re
import json
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from collections import defaultdict
import hashlib

logger = logging.getLogger(__name__)


class JAEGISMode(int, Enum):
    """JAEGIS operation modes."""
    BASIC = 1
    STANDARD = 2
    ADVANCED = 3
    EXPERT = 4
    SPECIALIZED = 5


class JAEGISSquad(str, Enum):
    """JAEGIS squad types."""
    DEVELOPMENT = "development"
    ANALYSIS = "analysis"
    SECURITY = "security"
    CONTENT = "content"
    INTEGRATION = "integration"
    ARCHITECTURE = "architecture"
    GARAS = "garas"
    IUAS = "iuas"
    CHIMERA = "chimera"


class CommandType(str, Enum):
    """Types of JAEGIS commands."""
    IMPLEMENT = "IMPLEMENT"
    BUILD = "BUILD"
    CREATE = "CREATE"
    ANALYZE = "ANALYZE"
    INVESTIGATE = "INVESTIGATE"
    RESEARCH = "RESEARCH"
    VALIDATE = "VALIDATE"
    DESIGN = "DESIGN"
    ARCHITECT = "ARCHITECT"
    PLAN = "PLAN"
    SECURE = "SECURE"
    PROTECT = "PROTECT"
    AUDIT = "AUDIT"
    DOCUMENT = "DOCUMENT"
    EXPLAIN = "EXPLAIN"
    WRITE = "WRITE"
    CONNECT = "CONNECT"
    INTEGRATE = "INTEGRATE"
    SYNC = "SYNC"
    DEPLOY = "DEPLOY"
    MONITOR = "MONITOR"
    MAINTAIN = "MAINTAIN"
    OPTIMIZE = "OPTIMIZE"


@dataclass
class CommandParameter:
    """JAEGIS command parameter."""
    name: str
    value: Any
    parameter_type: str
    required: bool
    description: str
    validation_pattern: Optional[str] = None


@dataclass
class JAEGISCommand:
    """Generated JAEGIS command."""
    agent: str
    command: CommandType
    parameters: List[CommandParameter]
    mode: JAEGISMode
    squad: JAEGISSquad
    priority: str
    estimated_duration: str
    dependencies: List[str]
    confidence: float
    reasoning: str
    raw_command: str


@dataclass
class CommandGenerationResult:
    """Command generation result."""
    primary_command: JAEGISCommand
    alternative_commands: List[JAEGISCommand]
    generation_confidence: float
    processing_time_ms: float
    intent_analysis: Dict[str, Any]
    parameter_extraction: Dict[str, Any]
    validation_results: Dict[str, Any]


class CommandGenerationEngine:
    """
    Advanced command generation engine for JAEGIS operations.
    
    Converts natural language input into standardized JAEGIS commands
    with proper syntax, parameter mapping, and validation.
    """
    
    def __init__(self):
        # Command templates and patterns
        self.command_templates = self._initialize_command_templates()
        
        # Agent-squad mappings
        self.agent_squad_mapping = self._initialize_agent_squad_mapping()
        
        # Parameter extraction patterns
        self.parameter_patterns = self._initialize_parameter_patterns()
        
        # Intent-command mappings
        self.intent_command_mapping = self._initialize_intent_command_mapping()
        
        # Complexity analysis patterns
        self.complexity_patterns = self._initialize_complexity_patterns()
        
        logger.info("Command Generation Engine initialized")
    
    def _initialize_command_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize command templates for different operations."""
        
        return {
            "IMPLEMENT": {
                "agents": ["FRED", "TECHNICAL"],
                "required_params": ["component"],
                "optional_params": ["technology", "framework", "security", "testing"],
                "syntax": "{agent}:IMPLEMENT --component={component} --technology={technology} --mode={mode}",
                "complexity_indicators": ["system", "architecture", "integration", "security"],
                "estimated_duration": {"basic": "2-4 hours", "standard": "4-8 hours", "advanced": "1-2 days", "expert": "2-5 days"}
            },
            
            "BUILD": {
                "agents": ["FRED", "ARCHITECT"],
                "required_params": ["target"],
                "optional_params": ["architecture", "technology", "deployment", "testing"],
                "syntax": "{agent}:BUILD --target={target} --architecture={architecture} --deployment={deployment}",
                "complexity_indicators": ["application", "system", "platform", "infrastructure"],
                "estimated_duration": {"basic": "4-8 hours", "standard": "1-2 days", "advanced": "3-7 days", "expert": "1-3 weeks"}
            },
            
            "CREATE": {
                "agents": ["FRED", "ARCHITECT", "DOCUMENT"],
                "required_params": ["item"],
                "optional_params": ["type", "format", "specifications", "requirements"],
                "syntax": "{agent}:CREATE --item={item} --type={type} --specifications={specifications}",
                "complexity_indicators": ["new", "custom", "innovative", "complex"],
                "estimated_duration": {"basic": "1-2 hours", "standard": "2-4 hours", "advanced": "4-8 hours", "expert": "1-2 days"}
            },
            
            "ANALYZE": {
                "agents": ["TYLER", "TECHNICAL"],
                "required_params": ["target"],
                "optional_params": ["metrics", "scope", "depth", "format"],
                "syntax": "{agent}:ANALYZE --target={target} --metrics={metrics} --scope={scope}",
                "complexity_indicators": ["performance", "security", "architecture", "data"],
                "estimated_duration": {"basic": "1-2 hours", "standard": "2-4 hours", "advanced": "4-8 hours", "expert": "1-2 days"}
            },
            
            "SECURE": {
                "agents": ["SECURE", "TECHNICAL"],
                "required_params": ["component"],
                "optional_params": ["method", "level", "compliance", "audit"],
                "syntax": "{agent}:SECURE --component={component} --method={method} --level={level}",
                "complexity_indicators": ["encryption", "authentication", "authorization", "compliance"],
                "estimated_duration": {"basic": "2-4 hours", "standard": "4-8 hours", "advanced": "1-2 days", "expert": "2-5 days"}
            },
            
            "DEPLOY": {
                "agents": ["INTEGRATE", "TECHNICAL"],
                "required_params": ["target"],
                "optional_params": ["environment", "strategy", "rollback", "monitoring"],
                "syntax": "{agent}:DEPLOY --target={target} --environment={environment} --strategy={strategy}",
                "complexity_indicators": ["production", "scaling", "monitoring", "automation"],
                "estimated_duration": {"basic": "2-4 hours", "standard": "4-8 hours", "advanced": "1-2 days", "expert": "2-3 days"}
            },
            
            "DOCUMENT": {
                "agents": ["DOCUMENT", "TECHNICAL"],
                "required_params": ["subject"],
                "optional_params": ["format", "audience", "detail", "examples"],
                "syntax": "{agent}:DOCUMENT --subject={subject} --format={format} --audience={audience}",
                "complexity_indicators": ["comprehensive", "technical", "api", "architecture"],
                "estimated_duration": {"basic": "1-2 hours", "standard": "2-4 hours", "advanced": "4-8 hours", "expert": "1-2 days"}
            }
        }
    
    def _initialize_agent_squad_mapping(self) -> Dict[str, JAEGISSquad]:
        """Initialize agent to squad mappings."""
        
        return {
            "JAEGIS": JAEGISSquad.ARCHITECTURE,  # Master Orchestrator
            "JOHN": JAEGISSquad.ARCHITECTURE,    # Planning Coordinator
            "FRED": JAEGISSquad.DEVELOPMENT,     # Implementation Coordinator
            "TYLER": JAEGISSquad.ANALYSIS,       # Validation Coordinator
            "ARCHITECT": JAEGISSquad.ARCHITECTURE,
            "TECHNICAL": JAEGISSquad.DEVELOPMENT,
            "INTEGRATE": JAEGISSquad.INTEGRATION,
            "QA": JAEGISSquad.ANALYSIS,
            "SECURE": JAEGISSquad.SECURITY,
            "DOCUMENT": JAEGISSquad.CONTENT,
            "GARAS_ALPHA": JAEGISSquad.GARAS,
            "GARAS_BETA": JAEGISSquad.GARAS,
            "GARAS_GAMMA": JAEGISSquad.GARAS,
            "GARAS_DELTA": JAEGISSquad.GARAS,
            "GARAS_EPSILON": JAEGISSquad.GARAS,
            "IUAS_PRIME": JAEGISSquad.IUAS,
            "CHIMERA": JAEGISSquad.CHIMERA
        }
    
    def _initialize_parameter_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize parameter extraction patterns."""
        
        return {
            "component": {
                "patterns": [
                    r"(?:create|build|implement|develop)\s+(?:a\s+)?(\w+(?:\s+\w+)*?)(?:\s+(?:system|service|api|application|module|component))",
                    r"(?:for|of)\s+(?:the\s+)?(\w+(?:\s+\w+)*?)(?:\s+(?:system|service|component))",
                    r"(\w+(?:\s+\w+)*?)\s+(?:authentication|authorization|management|processing)"
                ],
                "examples": ["user authentication", "payment processing", "data validation", "file upload"]
            },
            
            "technology": {
                "patterns": [
                    r"(?:using|with|in)\s+(python|javascript|java|go|rust|php|ruby|c\+\+|c#)",
                    r"(?:using|with)\s+(django|flask|react|vue|angular|express|spring|laravel)",
                    r"(?:using|with)\s+(postgresql|mysql|mongodb|redis|elasticsearch)"
                ],
                "examples": ["python", "javascript", "django", "postgresql", "docker"]
            },
            
            "security": {
                "patterns": [
                    r"(?:with|using)\s+(jwt|oauth|saml|ssl|tls|encryption)",
                    r"(?:secure|security|authentication|authorization)",
                    r"(?:with|using)\s+(?:secure|encrypted|protected)\s+(\w+)"
                ],
                "examples": ["jwt", "oauth", "ssl", "encryption", "secure"]
            },
            
            "environment": {
                "patterns": [
                    r"(?:to|in|on)\s+(production|staging|development|test|local)",
                    r"(?:to|in|on)\s+(aws|azure|gcp|docker|kubernetes|heroku)"
                ],
                "examples": ["production", "staging", "aws", "docker", "kubernetes"]
            },
            
            "priority": {
                "patterns": [
                    r"(urgent|critical|high|medium|low)\s+priority",
                    r"(asap|immediately|soon|later)",
                    r"(critical|urgent|important|normal|low)"
                ],
                "examples": ["high", "urgent", "critical", "normal", "low"]
            }
        }
    
    def _initialize_intent_command_mapping(self) -> Dict[str, List[CommandType]]:
        """Initialize intent to command mappings."""
        
        return {
            "create": [CommandType.CREATE, CommandType.BUILD, CommandType.IMPLEMENT],
            "build": [CommandType.BUILD, CommandType.IMPLEMENT, CommandType.CREATE],
            "implement": [CommandType.IMPLEMENT, CommandType.BUILD, CommandType.CREATE],
            "develop": [CommandType.IMPLEMENT, CommandType.BUILD, CommandType.CREATE],
            "make": [CommandType.CREATE, CommandType.BUILD, CommandType.IMPLEMENT],
            
            "analyze": [CommandType.ANALYZE, CommandType.INVESTIGATE, CommandType.RESEARCH],
            "investigate": [CommandType.INVESTIGATE, CommandType.ANALYZE, CommandType.RESEARCH],
            "research": [CommandType.RESEARCH, CommandType.INVESTIGATE, CommandType.ANALYZE],
            "examine": [CommandType.ANALYZE, CommandType.INVESTIGATE],
            "study": [CommandType.RESEARCH, CommandType.ANALYZE],
            
            "secure": [CommandType.SECURE, CommandType.PROTECT, CommandType.AUDIT],
            "protect": [CommandType.PROTECT, CommandType.SECURE, CommandType.AUDIT],
            "audit": [CommandType.AUDIT, CommandType.SECURE, CommandType.ANALYZE],
            
            "deploy": [CommandType.DEPLOY, CommandType.INTEGRATE, CommandType.CONNECT],
            "release": [CommandType.DEPLOY, CommandType.INTEGRATE],
            "launch": [CommandType.DEPLOY, CommandType.INTEGRATE],
            
            "document": [CommandType.DOCUMENT, CommandType.WRITE, CommandType.EXPLAIN],
            "write": [CommandType.WRITE, CommandType.DOCUMENT, CommandType.CREATE],
            "explain": [CommandType.EXPLAIN, CommandType.DOCUMENT, CommandType.WRITE],
            
            "design": [CommandType.DESIGN, CommandType.ARCHITECT, CommandType.PLAN],
            "architect": [CommandType.ARCHITECT, CommandType.DESIGN, CommandType.PLAN],
            "plan": [CommandType.PLAN, CommandType.DESIGN, CommandType.ARCHITECT],
            
            "connect": [CommandType.CONNECT, CommandType.INTEGRATE, CommandType.SYNC],
            "integrate": [CommandType.INTEGRATE, CommandType.CONNECT, CommandType.SYNC],
            "sync": [CommandType.SYNC, CommandType.INTEGRATE, CommandType.CONNECT],
            
            "monitor": [CommandType.MONITOR, CommandType.ANALYZE, CommandType.VALIDATE],
            "maintain": [CommandType.MAINTAIN, CommandType.MONITOR, CommandType.OPTIMIZE],
            "optimize": [CommandType.OPTIMIZE, CommandType.ANALYZE, CommandType.MAINTAIN]
        }
    
    def _initialize_complexity_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize complexity analysis patterns."""
        
        return {
            "simple": {
                "keywords": ["simple", "basic", "quick", "small", "minimal"],
                "indicators": ["single", "one", "basic", "simple"],
                "mode": JAEGISMode.BASIC,
                "score_range": (0.0, 0.3)
            },
            
            "moderate": {
                "keywords": ["standard", "normal", "typical", "regular"],
                "indicators": ["multiple", "several", "standard", "typical"],
                "mode": JAEGISMode.STANDARD,
                "score_range": (0.3, 0.6)
            },
            
            "complex": {
                "keywords": ["complex", "advanced", "sophisticated", "comprehensive"],
                "indicators": ["complex", "advanced", "multiple", "integration"],
                "mode": JAEGISMode.ADVANCED,
                "score_range": (0.6, 0.8)
            },
            
            "expert": {
                "keywords": ["expert", "enterprise", "production", "scalable"],
                "indicators": ["enterprise", "production", "scalable", "distributed"],
                "mode": JAEGISMode.EXPERT,
                "score_range": (0.8, 0.9)
            },
            
            "specialized": {
                "keywords": ["specialized", "custom", "unique", "innovative"],
                "indicators": ["specialized", "custom", "innovative", "cutting-edge"],
                "mode": JAEGISMode.SPECIALIZED,
                "score_range": (0.9, 1.0)
            }
        }
    
    def generate_command(self, text: str, intent: str, entities: List[Dict[str, Any]], 
                        context: Optional[Dict[str, Any]] = None) -> CommandGenerationResult:
        """Generate JAEGIS command from natural language input."""
        
        start_time = time.time()
        
        # Analyze intent and map to commands
        intent_analysis = self._analyze_intent(text, intent, entities)
        
        # Extract parameters from text and entities
        parameter_extraction = self._extract_parameters(text, entities, context)
        
        # Determine complexity and mode
        complexity_analysis = self._analyze_complexity(text, entities, parameter_extraction)
        
        # Generate primary command
        primary_command = self._generate_primary_command(
            intent_analysis, parameter_extraction, complexity_analysis
        )
        
        # Generate alternative commands
        alternative_commands = self._generate_alternative_commands(
            intent_analysis, parameter_extraction, complexity_analysis
        )
        
        # Validate commands
        validation_results = self._validate_commands([primary_command] + alternative_commands)
        
        # Calculate overall confidence
        generation_confidence = self._calculate_generation_confidence(
            intent_analysis, parameter_extraction, validation_results
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return CommandGenerationResult(
            primary_command=primary_command,
            alternative_commands=alternative_commands,
            generation_confidence=generation_confidence,
            processing_time_ms=processing_time,
            intent_analysis=intent_analysis,
            parameter_extraction=parameter_extraction,
            validation_results=validation_results
        )
    
    def _analyze_intent(self, text: str, intent: str, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze intent and map to JAEGIS commands."""
        
        # Get possible commands for the intent
        possible_commands = self.intent_command_mapping.get(intent.lower(), [])
        
        # Analyze text for command indicators
        text_lower = text.lower()
        command_scores = {}
        
        for command_type in CommandType:
            score = 0.0
            command_name = command_type.value.lower()
            
            # Direct mention
            if command_name in text_lower:
                score += 0.8
            
            # Template analysis
            if command_type.value in self.command_templates:
                template = self.command_templates[command_type.value]
                for indicator in template.get("complexity_indicators", []):
                    if indicator in text_lower:
                        score += 0.2
            
            # Intent mapping
            if command_type in possible_commands:
                score += 0.6
            
            command_scores[command_type] = score
        
        # Sort by score
        sorted_commands = sorted(command_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "primary_intent": intent,
            "command_scores": {cmd.value: score for cmd, score in sorted_commands},
            "top_commands": [cmd.value for cmd, score in sorted_commands[:3] if score > 0],
            "confidence": max(score for _, score in sorted_commands) if sorted_commands else 0.0
        }
    
    def _extract_parameters(self, text: str, entities: List[Dict[str, Any]], 
                          context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract command parameters from text and entities."""
        
        extracted_params = {}
        
        # Extract from entities
        for entity in entities:
            entity_type = entity.get("label", "").lower()
            entity_value = entity.get("text", "")
            
            if entity_type in ["jaegis_component", "component"]:
                extracted_params["component"] = entity_value
            elif entity_type in ["technology", "programming_language", "framework"]:
                extracted_params["technology"] = entity_value
            elif entity_type in ["security_concept", "security"]:
                extracted_params["security"] = entity_value
            elif entity_type in ["deployment_target", "cloud_platform"]:
                extracted_params["environment"] = entity_value
        
        # Extract using regex patterns
        for param_name, param_config in self.parameter_patterns.items():
            for pattern in param_config["patterns"]:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    extracted_params[param_name] = matches[0] if isinstance(matches[0], str) else matches[0][0]
                    break
        
        # Extract from context
        if context:
            for key, value in context.items():
                if key in ["technology", "framework", "environment", "priority"]:
                    if key not in extracted_params:
                        extracted_params[key] = value
        
        # Infer missing parameters
        inferred_params = self._infer_parameters(text, extracted_params)
        extracted_params.update(inferred_params)
        
        return {
            "extracted": extracted_params,
            "confidence": self._calculate_parameter_confidence(extracted_params),
            "completeness": len(extracted_params) / 6.0  # Assuming 6 common parameters
        }
    
    def _infer_parameters(self, text: str, extracted_params: Dict[str, Any]) -> Dict[str, Any]:
        """Infer missing parameters from context."""
        
        inferred = {}
        text_lower = text.lower()
        
        # Infer component if not extracted
        if "component" not in extracted_params:
            component_indicators = {
                "authentication": ["login", "auth", "user", "password", "token"],
                "api": ["endpoint", "rest", "graphql", "service"],
                "database": ["data", "storage", "persistence", "db"],
                "ui": ["interface", "frontend", "dashboard", "form"],
                "payment": ["payment", "billing", "transaction", "checkout"]
            }
            
            for component, indicators in component_indicators.items():
                if any(indicator in text_lower for indicator in indicators):
                    inferred["component"] = component
                    break
        
        # Infer priority
        if "priority" not in extracted_params:
            if any(word in text_lower for word in ["urgent", "asap", "critical", "immediately"]):
                inferred["priority"] = "high"
            elif any(word in text_lower for word in ["later", "eventually", "when possible"]):
                inferred["priority"] = "low"
            else:
                inferred["priority"] = "medium"
        
        # Infer testing requirements
        if any(word in text_lower for word in ["test", "testing", "validate", "verify"]):
            inferred["testing"] = "required"
        
        return inferred
    
    def _analyze_complexity(self, text: str, entities: List[Dict[str, Any]], 
                          parameter_extraction: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task complexity and determine appropriate mode."""
        
        complexity_score = 0.0
        complexity_factors = []
        
        text_lower = text.lower()
        
        # Analyze complexity indicators
        for complexity_level, config in self.complexity_patterns.items():
            level_score = 0.0
            
            # Check keywords
            for keyword in config["keywords"]:
                if keyword in text_lower:
                    level_score += 0.2
                    complexity_factors.append(f"keyword: {keyword}")
            
            # Check indicators
            for indicator in config["indicators"]:
                if indicator in text_lower:
                    level_score += 0.3
                    complexity_factors.append(f"indicator: {indicator}")
            
            if level_score > complexity_score:
                complexity_score = level_score
                recommended_mode = config["mode"]
        
        # Adjust based on parameters
        extracted_params = parameter_extraction.get("extracted", {})
        
        # Multiple technologies increase complexity
        tech_count = sum(1 for key in ["technology", "framework", "database"] if key in extracted_params)
        if tech_count > 1:
            complexity_score += 0.2
            complexity_factors.append(f"multiple technologies: {tech_count}")
        
        # Security requirements increase complexity
        if "security" in extracted_params:
            complexity_score += 0.3
            complexity_factors.append("security requirements")
        
        # Production deployment increases complexity
        if extracted_params.get("environment") in ["production", "prod"]:
            complexity_score += 0.2
            complexity_factors.append("production deployment")
        
        # Determine final mode
        if complexity_score >= 0.9:
            final_mode = JAEGISMode.SPECIALIZED
        elif complexity_score >= 0.8:
            final_mode = JAEGISMode.EXPERT
        elif complexity_score >= 0.6:
            final_mode = JAEGISMode.ADVANCED
        elif complexity_score >= 0.3:
            final_mode = JAEGISMode.STANDARD
        else:
            final_mode = JAEGISMode.BASIC
        
        return {
            "complexity_score": complexity_score,
            "complexity_factors": complexity_factors,
            "recommended_mode": final_mode,
            "confidence": min(1.0, complexity_score + 0.3)
        }
    
    def _generate_primary_command(self, intent_analysis: Dict[str, Any], 
                                parameter_extraction: Dict[str, Any],
                                complexity_analysis: Dict[str, Any]) -> JAEGISCommand:
        """Generate the primary JAEGIS command."""
        
        # Select command type
        top_commands = intent_analysis.get("top_commands", [])
        if not top_commands:
            command_type = CommandType.IMPLEMENT  # Default
        else:
            command_type = CommandType(top_commands[0])
        
        # Select agent
        template = self.command_templates.get(command_type.value, {})
        possible_agents = template.get("agents", ["FRED"])
        
        # Choose agent based on complexity and command type
        if complexity_analysis["recommended_mode"] >= JAEGISMode.EXPERT:
            agent = possible_agents[0] if "TECHNICAL" in possible_agents else possible_agents[0]
        else:
            agent = possible_agents[0]
        
        # Get squad
        squad = self.agent_squad_mapping.get(agent, JAEGISSquad.DEVELOPMENT)
        
        # Build parameters
        extracted_params = parameter_extraction.get("extracted", {})
        parameters = []
        
        for param_name, param_value in extracted_params.items():
            parameters.append(CommandParameter(
                name=param_name,
                value=param_value,
                parameter_type="string",
                required=param_name in template.get("required_params", []),
                description=f"Parameter for {param_name}",
                validation_pattern=None
            ))
        
        # Generate raw command
        raw_command = self._build_raw_command(agent, command_type, extracted_params, complexity_analysis["recommended_mode"])
        
        # Estimate duration
        mode_name = complexity_analysis["recommended_mode"].name.lower()
        estimated_duration = template.get("estimated_duration", {}).get(mode_name, "2-4 hours")
        
        # Calculate confidence
        confidence = (
            intent_analysis.get("confidence", 0.0) * 0.4 +
            parameter_extraction.get("confidence", 0.0) * 0.3 +
            complexity_analysis.get("confidence", 0.0) * 0.3
        )
        
        return JAEGISCommand(
            agent=agent,
            command=command_type,
            parameters=parameters,
            mode=complexity_analysis["recommended_mode"],
            squad=squad,
            priority=extracted_params.get("priority", "medium"),
            estimated_duration=estimated_duration,
            dependencies=[],
            confidence=confidence,
            reasoning=f"Selected {command_type.value} based on intent analysis with {len(parameters)} parameters",
            raw_command=raw_command
        )
    
    def _generate_alternative_commands(self, intent_analysis: Dict[str, Any],
                                     parameter_extraction: Dict[str, Any],
                                     complexity_analysis: Dict[str, Any]) -> List[JAEGISCommand]:
        """Generate alternative command interpretations."""
        
        alternatives = []
        top_commands = intent_analysis.get("top_commands", [])
        
        # Generate alternatives for top 2 other commands
        for command_name in top_commands[1:3]:
            try:
                command_type = CommandType(command_name)
                
                # Use different agent if available
                template = self.command_templates.get(command_type.value, {})
                possible_agents = template.get("agents", ["FRED"])
                
                # Choose different agent than primary
                agent = possible_agents[-1] if len(possible_agents) > 1 else possible_agents[0]
                squad = self.agent_squad_mapping.get(agent, JAEGISSquad.DEVELOPMENT)
                
                # Adjust mode slightly
                alt_mode = complexity_analysis["recommended_mode"]
                if alt_mode.value > 1:
                    alt_mode = JAEGISMode(alt_mode.value - 1)
                
                # Build parameters (same as primary)
                extracted_params = parameter_extraction.get("extracted", {})
                parameters = []
                
                for param_name, param_value in extracted_params.items():
                    parameters.append(CommandParameter(
                        name=param_name,
                        value=param_value,
                        parameter_type="string",
                        required=param_name in template.get("required_params", []),
                        description=f"Parameter for {param_name}"
                    ))
                
                # Generate raw command
                raw_command = self._build_raw_command(agent, command_type, extracted_params, alt_mode)
                
                # Lower confidence for alternatives
                confidence = intent_analysis.get("confidence", 0.0) * 0.7
                
                alternative = JAEGISCommand(
                    agent=agent,
                    command=command_type,
                    parameters=parameters,
                    mode=alt_mode,
                    squad=squad,
                    priority=extracted_params.get("priority", "medium"),
                    estimated_duration=template.get("estimated_duration", {}).get(alt_mode.name.lower(), "2-4 hours"),
                    dependencies=[],
                    confidence=confidence,
                    reasoning=f"Alternative {command_type.value} interpretation with {agent}",
                    raw_command=raw_command
                )
                
                alternatives.append(alternative)
                
            except ValueError:
                continue
        
        return alternatives
    
    def _build_raw_command(self, agent: str, command_type: CommandType, 
                          params: Dict[str, Any], mode: JAEGISMode) -> str:
        """Build raw command string."""
        
        command_parts = [f"{agent}:{command_type.value}"]
        
        # Add parameters
        for param_name, param_value in params.items():
            if param_value:
                command_parts.append(f"--{param_name}={param_value}")
        
        # Add mode
        command_parts.append(f"--mode={mode.value}")
        
        return " ".join(command_parts)
    
    def _validate_commands(self, commands: List[JAEGISCommand]) -> Dict[str, Any]:
        """Validate generated commands."""
        
        validation_results = {
            "valid_commands": 0,
            "invalid_commands": 0,
            "validation_errors": [],
            "warnings": []
        }
        
        for command in commands:
            is_valid = True
            
            # Check agent exists
            if command.agent not in self.agent_squad_mapping:
                validation_results["validation_errors"].append(f"Unknown agent: {command.agent}")
                is_valid = False
            
            # Check required parameters
            template = self.command_templates.get(command.command.value, {})
            required_params = template.get("required_params", [])
            
            command_param_names = [p.name for p in command.parameters]
            for required_param in required_params:
                if required_param not in command_param_names:
                    validation_results["warnings"].append(f"Missing required parameter: {required_param}")
            
            # Check mode validity
            if not isinstance(command.mode, JAEGISMode):
                validation_results["validation_errors"].append(f"Invalid mode: {command.mode}")
                is_valid = False
            
            if is_valid:
                validation_results["valid_commands"] += 1
            else:
                validation_results["invalid_commands"] += 1
        
        return validation_results
    
    def _calculate_parameter_confidence(self, params: Dict[str, Any]) -> float:
        """Calculate confidence in parameter extraction."""
        
        if not params:
            return 0.0
        
        # Base confidence on number and quality of parameters
        base_confidence = min(1.0, len(params) / 4.0)  # Assume 4 is good coverage
        
        # Boost for important parameters
        important_params = ["component", "technology", "security"]
        important_count = sum(1 for param in important_params if param in params)
        importance_boost = important_count * 0.1
        
        return min(1.0, base_confidence + importance_boost)
    
    def _calculate_generation_confidence(self, intent_analysis: Dict[str, Any],
                                       parameter_extraction: Dict[str, Any],
                                       validation_results: Dict[str, Any]) -> float:
        """Calculate overall generation confidence."""
        
        intent_confidence = intent_analysis.get("confidence", 0.0)
        param_confidence = parameter_extraction.get("confidence", 0.0)
        
        # Validation penalty
        total_commands = validation_results["valid_commands"] + validation_results["invalid_commands"]
        validation_score = validation_results["valid_commands"] / total_commands if total_commands > 0 else 0.0
        
        # Weighted average
        overall_confidence = (
            intent_confidence * 0.4 +
            param_confidence * 0.3 +
            validation_score * 0.3
        )
        
        return overall_confidence


# Example usage
if __name__ == "__main__":
    # Initialize command generation engine
    engine = CommandGenerationEngine()
    
    # Test command generation
    test_text = "Create a secure user authentication system using JWT tokens with Python Flask"
    test_intent = "create"
    test_entities = [
        {"label": "JAEGIS_COMPONENT", "text": "authentication system"},
        {"label": "TECHNOLOGY", "text": "Python Flask"},
        {"label": "SECURITY_CONCEPT", "text": "JWT tokens"}
    ]
    
    result = engine.generate_command(test_text, test_intent, test_entities)
    
    print(f"Primary Command: {result.primary_command.raw_command}")
    print(f"Agent: {result.primary_command.agent}")
    print(f"Squad: {result.primary_command.squad.value}")
    print(f"Mode: {result.primary_command.mode.value}")
    print(f"Confidence: {result.generation_confidence:.3f}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    
    print(f"\nAlternatives ({len(result.alternative_commands)}):")
    for alt in result.alternative_commands:
        print(f"  - {alt.raw_command} (confidence: {alt.confidence:.3f})")
