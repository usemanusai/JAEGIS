"""
JAEGIS Configuration Management System - Core Schema
Defines the data structures and validation for configuration parameters
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any
from enum import Enum
import json
from datetime import datetime
import uuid

class ParameterType(Enum):
    """Types of configuration parameters"""
    PERCENTAGE = "percentage"
    BOOLEAN = "boolean"
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    LIST = "list"
    DICT = "dict"

class AgentTier(Enum):
    """Agent classification tiers"""
    TIER_1_ORCHESTRATOR = "tier_1_orchestrator"
    TIER_2_PRIMARY = "tier_2_primary"
    TIER_3_SECONDARY = "tier_3_secondary"
    TIER_4_SPECIALIZED = "tier_4_specialized"

class ConfigurationMode(Enum):
    """Preset configuration modes"""
    SPEED_MODE = "speed_mode"
    QUALITY_MODE = "quality_mode"
    BALANCED_MODE = "balanced_mode"
    CUSTOM = "custom"

@dataclass
class ParameterDefinition:
    """Definition of a configuration parameter"""
    name: str
    display_name: str
    description: str
    parameter_type: ParameterType
    default_value: Any
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    allowed_values: Optional[List[Any]] = None
    validation_rules: List[str] = field(default_factory=list)
    impact_description: str = ""
    category: str = "general"
    requires_restart: bool = False
    
    def validate_value(self, value: Any) -> bool:
        """Validate a value against this parameter definition"""
        if self.parameter_type == ParameterType.PERCENTAGE:
            return isinstance(value, (int, float)) and 0 <= value <= 100
        elif self.parameter_type == ParameterType.BOOLEAN:
            return isinstance(value, bool)
        elif self.parameter_type == ParameterType.STRING:
            return isinstance(value, str)
        elif self.parameter_type == ParameterType.INTEGER:
            if not isinstance(value, int):
                return False
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False
            return True
        elif self.parameter_type == ParameterType.FLOAT:
            if not isinstance(value, (int, float)):
                return False
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False
            return True
        elif self.parameter_type == ParameterType.LIST:
            return isinstance(value, list)
        elif self.parameter_type == ParameterType.DICT:
            return isinstance(value, dict)
        
        if self.allowed_values:
            return value in self.allowed_values
        
        return True

@dataclass
class FrequencyParameters:
    """Core frequency control parameters"""
    research_intensity: int = 70  # 0-100%
    task_decomposition: int = 60  # 0-100%
    agent_utilization: Dict[AgentTier, int] = field(default_factory=lambda: {
        AgentTier.TIER_1_ORCHESTRATOR: 100,
        AgentTier.TIER_2_PRIMARY: 90,
        AgentTier.TIER_3_SECONDARY: 70,
        AgentTier.TIER_4_SPECIALIZED: 50
    })
    validation_thoroughness: int = 80  # 0-100%
    documentation_detail: int = 75  # 0-100%
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "research_intensity": self.research_intensity,
            "task_decompositionself_task_decomposition_agent_utilization": {tier.value: value for tier, value in self.agent_utilization.items()},
            "validation_thoroughness": self.validation_thoroughness,
            "documentation_detail": self.documentation_detail
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FrequencyParameters':
        """Create from dictionary"""
        agent_util = {}
        if "agent_utilization" in data:
            for tier_str, value in data["agent_utilization"].items():
                tier = AgentTier(tier_str)
                agent_util[tier] = value
        
        return cls(
            research_intensity=data.get("research_intensity", 70),
            task_decomposition=data.get("task_decomposition", 60),
            agent_utilization=agent_util or cls().agent_utilization,
            validation_thoroughness=data.get("validation_thoroughness", 80),
            documentation_detail=data.get("documentation_detail", 75)
        )

@dataclass
class ProtocolRule:
    """Individual protocol rule definition"""
    rule_id: str
    name: str
    description: str
    condition: str  # Condition when rule applies
    action: str  # Action to take when rule triggers
    priority: int = 1  # Higher number = higher priority
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "condition": self.condition,
            "action": self.action,
            "priority": self.priority,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProtocolRule':
        """Create from dictionary"""
        return cls(
            rule_id=data["rule_id"],
            name=data["name"],
            description=data["description"],
            condition=data["condition"],
            action=data["action"],
            priority=data.get("priority", 1),
            enabled=data.get("enabled", True),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            modified_at=datetime.fromisoformat(data.get("modified_at", datetime.now().isoformat()))
        )

@dataclass
class WorkflowProtocol:
    """Complete workflow protocol definition"""
    protocol_id: str
    name: str
    description: str
    rules: List[ProtocolRule] = field(default_factory=list)
    project_types: List[str] = field(default_factory=list)  # Which project types this applies to
    agent_constraints: Dict[str, Any] = field(default_factory=dict)
    approval_required: bool = False
    escalation_rules: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    def add_rule(self, rule: ProtocolRule):
        """Add a rule to this protocol"""
        self.rules.append(rule)
        self.modified_at = datetime.now()
    
    def remove_rule(self, rule_id: str):
        """Remove a rule from this protocol"""
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        self.modified_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "protocol_id": self.protocol_id,
            "name": self.name,
            "description": self.description,
            "rules": [rule.to_dict() for rule in self.rules],
            "project_types": self.project_types,
            "agent_constraints": self.agent_constraints,
            "approval_required": self.approval_required,
            "escalation_rules": self.escalation_rules,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowProtocol':
        """Create from dictionary"""
        rules = [ProtocolRule.from_dict(rule_data) for rule_data in data.get("rules", [])]
        
        return cls(
            protocol_id=data["protocol_id"],
            name=data["name"],
            description=data["description"],
            rules=rules,
            project_types=data.get("project_types", []),
            agent_constraints=data.get("agent_constraints", {}),
            approval_required=data.get("approval_required", False),
            escalation_rules=data.get("escalation_rules", []),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            modified_at=datetime.fromisoformat(data.get("modified_at", datetime.now().isoformat())),
            version=data.get("version", "1.0.0")
        )

@dataclass
class AgentConfiguration:
    """Configuration for individual agents"""
    agent_id: str
    agent_name: str
    tier: AgentTier
    enabled: bool = True
    activation_frequency: int = 100  # 0-100%
    behavior_parameters: Dict[str, Any] = field(default_factory=dict)
    interaction_rules: List[str] = field(default_factory=list)
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "tier": self.tier.value,
            "enabled": self.enabled,
            "activation_frequency": self.activation_frequency,
            "behavior_parameters": self.behavior_parameters,
            "interaction_rules": self.interaction_rules,
            "resource_limits": self.resource_limits
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfiguration':
        """Create from dictionary"""
        return cls(
            agent_id=data["agent_id"],
            agent_name=data["agent_name"],
            tier=AgentTier(data["tier"]),
            enabled=data.get("enabled", True),
            activation_frequency=data.get("activation_frequency", 100),
            behavior_parameters=data.get("behavior_parameters", {}),
            interaction_rules=data.get("interaction_rules", []),
            resource_limits=data.get("resource_limits", {})
        )

@dataclass
class JAEGISConfiguration:
    """Complete JAEGIS system configuration"""
    config_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Default Configuration"
    description: str = "Default JAEGIS configuration"
    mode: ConfigurationMode = ConfigurationMode.BALANCED_MODE
    frequency_parameters: FrequencyParameters = field(default_factory=FrequencyParameters)
    protocols: List[WorkflowProtocol] = field(default_factory=list)
    agent_configurations: List[AgentConfiguration] = field(default_factory=list)
    global_settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "config_id": self.config_id,
            "name": self.name,
            "description": self.description,
            "mode": self.mode.value,
            "frequency_parameters": self.frequency_parameters.to_dict(),
            "protocols": [protocol.to_dict() for protocol in self.protocols],
            "agent_configurations": [agent.to_dict() for agent in self.agent_configurations],
            "global_settings": self.global_settings,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JAEGISConfiguration':
        """Create from dictionary"""
        frequency_params = FrequencyParameters.from_dict(data.get("frequency_parameters", {}))
        protocols = [WorkflowProtocol.from_dict(p) for p in data.get("protocols", [])]
        agent_configs = [AgentConfiguration.from_dict(a) for a in data.get("agent_configurations", [])]
        
        return cls(
            config_id=data.get("config_id", str(uuid.uuid4())),
            name=data.get("name", "Default Configuration"),
            description=data.get("description", "Default JAEGIS configuration"),
            mode=ConfigurationMode(data.get("mode", ConfigurationMode.BALANCED_MODE.value)),
            frequency_parameters=frequency_params,
            protocols=protocols,
            agent_configurations=agent_configs,
            global_settings=data.get("global_settings", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            modified_at=datetime.fromisoformat(data.get("modified_at", datetime.now().isoformat())),
            version=data.get("version", "1.0.0")
        )
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'JAEGISConfiguration':
        """Load configuration from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

# Predefined parameter definitions for the system
FREQUENCY_PARAMETER_DEFINITIONS = {
    "research_intensity": ParameterDefinition(
        name="research_intensity",
        display_name="Research Intensity",
        description="Controls the depth of web research and information gathering",
        parameter_type=ParameterType.PERCENTAGE,
        default_value=70,
        min_value=0,
        max_value=100,
        impact_description="Higher values increase research thoroughness but may slow down initial responses",
        category="research"
    ),
    "task_decomposition": ParameterDefinition(
        name="task_decomposition",
        display_name="Task Decomposition",
        description="Controls how often tasks are broken into subtasks",
        parameter_type=ParameterType.PERCENTAGE,
        default_value=60,
        min_value=0,
        max_value=100,
        impact_description="Higher values create more detailed task breakdowns but may increase complexity",
        category="workflow"
    ),
    "validation_thoroughness": ParameterDefinition(
        name="validation_thoroughness",
        display_name="Validation Thoroughness",
        description="Controls the depth of quality assurance checks",
        parameter_type=ParameterType.PERCENTAGE,
        default_value=80,
        min_value=0,
        max_value=100,
        impact_description="Higher values improve quality but may increase processing time",
        category="quality"
    ),
    "documentation_detail": ParameterDefinition(
        name="documentation_detail",
        display_name="Documentation Detail",
        description="Controls the comprehensiveness of generated documentation",
        parameter_type=ParameterType.PERCENTAGE,
        default_value=75,
        min_value=0,
        max_value=100,
        impact_description="Higher values create more detailed documentation but may increase generation time",
        category="documentation"
    )
}

# Preset configuration modes
PRESET_CONFIGURATIONS = {
    ConfigurationMode.SPEED_MODE: {
        "research_intensity": 40,
        "task_decomposition": 30,
        "validation_thoroughness": 50,
        "documentation_detail40_agent_utilization": {
            AgentTier.TIER_1_ORCHESTRATOR: 100,
            AgentTier.TIER_2_PRIMARY: 80,
            AgentTier.TIER_3_SECONDARY: 40,
            AgentTier.TIER_4_SPECIALIZED: 20
        }
    },
    ConfigurationMode.QUALITY_MODE: {
        "research_intensity": 90,
        "task_decomposition": 80,
        "validation_thoroughness": 95,
        "documentation_detail90_agent_utilization": {
            AgentTier.TIER_1_ORCHESTRATOR: 100,
            AgentTier.TIER_2_PRIMARY: 100,
            AgentTier.TIER_3_SECONDARY: 90,
            AgentTier.TIER_4_SPECIALIZED: 80
        }
    },
    ConfigurationMode.BALANCED_MODE: {
        "research_intensity": 70,
        "task_decomposition": 60,
        "validation_thoroughness": 80,
        "documentation_detail75_agent_utilization": {
            AgentTier.TIER_1_ORCHESTRATOR: 100,
            AgentTier.TIER_2_PRIMARY: 90,
            AgentTier.TIER_3_SECONDARY: 70,
            AgentTier.TIER_4_SPECIALIZED: 50
        }
    }
}
