"""
JAEGIS Enhanced System v2.0 - Workflow Sequence Management Engine
Core engine for managing workflow sequences with numbered priority interface, dependency validation, and preset templates
Provides granular control over JAEGIS operation execution order and dependencies
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid

logger = logging.getLogger(__name__)

class WorkflowOperation(Enum):
    """Core JAEGIS workflow operations"""
    DEEP_WEB_RESEARCH = "deep_web_research"
    TASK_HIERARCHY_GENERATION = "task_hierarchy_generation"
    AGENT_COORDINATION = "agent_coordination"
    QUALITY_VALIDATION = "quality_validation"
    DOCUMENTATION_CREATION = "documentation_creation"
    PROJECT_EXECUTION = "project_execution"
    TEMPORAL_COORDINATION = "temporal_coordination"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    INTELLIGENCE_ENHANCEMENT = "intelligence_enhancement"
    SCALABILITY_MANAGEMENT = "scalability_management"

class DependencyType(Enum):
    """Types of dependencies between operations"""
    REQUIRED = "required"        # Must complete before dependent operation
    OPTIONAL = "optional"        # Recommended but not required
    PARALLEL = "parallel"        # Can run in parallel
    EXCLUSIVE = "exclusive"      # Cannot run simultaneously

class WorkflowTemplate(Enum):
    """Preset workflow templates"""
    RESEARCH_FIRST = "research_first"
    RAPID_EXECUTION = "rapid_execution"
    QUALITY_FOCUSED = "quality_focused"
    BALANCED_APPROACH = "balanced_approach"
    CUSTOM = "custom"

@dataclass
class WorkflowStep:
    """Individual workflow step configuration"""
    operation: WorkflowOperation
    priority: int
    enabled: bool
    estimated_duration: float  # minutes
    dependencies: List[str]
    dependency_type: DependencyType
    parallel_group: Optional[str] = None
    configuration: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation.value,
            "priority": self.priority,
            "enabled": self.enabled,
            "estimated_duration": self.estimated_duration,
            "dependencies": self.dependencies,
            "dependency_type": self.dependency_type.value,
            "parallel_group": self.parallel_group,
            "configuration": self.configuration
        }

@dataclass
class WorkflowSequence:
    """Complete workflow sequence configuration"""
    sequence_id: str
    name: str
    template: WorkflowTemplate
    steps: List[WorkflowStep]
    total_estimated_duration: float
    created_at: datetime
    last_modified: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence_id": self.sequence_id,
            "name": self.name,
            "template": self.template.value,
            "steps": [step.to_dict() for step in self.steps],
            "total_estimated_duration": self.total_estimated_duration,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat()
        }

class WorkflowSequenceEngine:
    """Core engine for managing JAEGIS workflow sequences"""
    
    def __init__(self):
        # Workflow management
        self.current_sequence: Optional[WorkflowSequence] = None
        self.saved_sequences: Dict[str, WorkflowSequence] = {}
        self.preset_templates: Dict[WorkflowTemplate, WorkflowSequence] = {}
        
        # Operation definitions
        self.operation_definitions = self._initialize_operation_definitions()
        self.dependency_rules = self._initialize_dependency_rules()
        
        # Validation engine
        self.dependency_validator = DependencyValidator()
        self.sequence_optimizer = SequenceOptimizer()
        
        # Statistics
        self.sequence_stats = {
            "sequences_created": 0,
            "sequences_executed": 0,
            "average_execution_time": 0.0,
            "most_used_template": None
        }
        
        logger.info("Workflow Sequence Engine initialized")
    
    def _initialize_operation_definitions(self) -> Dict[WorkflowOperation, Dict[str, Any]]:
        """Initialize operation definitions with metadata"""
        
        return {
            WorkflowOperation.DEEP_WEB_RESEARCH: {
                "name": "Deep_Web_Research",
                "description": "Comprehensive web research with 15+ sources per topic",
                "base_duration": 8.0,  # minutes
                "criticality": "high",
                "can_disable": False,
                "parallel_capable": True,
                "resource_intensive": True
            },
            WorkflowOperation.TASK_HIERARCHY_GENERATION: {
                "name": "Task_Hierarchy_Generation",
                "description": "AI-generated task structures with dependencies",
                "base_duration": 3.0,
                "criticality": "high",
                "can_disable": False,
                "parallel_capable": False,
                "resource_intensive": False
            },
            WorkflowOperation.AGENT_COORDINATION: {
                "name": "Agent_Coordination",
                "description": "Coordinate all 74 agents for optimal collaboration",
                "base_duration": 2.0,
                "criticality": "high",
                "can_disable": False,
                "parallel_capable": True,
                "resource_intensive": False
            },
            WorkflowOperation.QUALITY_VALIDATION: {
                "name": "Quality_Validation",
                "description": "Multi-layer validation with evidence-based verification",
                "base_duration": 5.0,
                "criticality": "medium",
                "can_disable": True,
                "parallel_capable": True,
                "resource_intensive": False
            },
            WorkflowOperation.DOCUMENTATION_CREATION: {
                "name": "Documentation_Creation",
                "description": "Generate comprehensive project documentation",
                "base_duration": 15.0,
                "criticality": "medium",
                "can_disable": True,
                "parallel_capable": False,
                "resource_intensive": False
            },
            WorkflowOperation.PROJECT_EXECUTION: {
                "name": "Project_Execution",
                "description": "Execute project tasks with continuous monitoring",
                "base_duration": 30.0,
                "criticality": "high",
                "can_disable": False,
                "parallel_capable": False,
                "resource_intensive": True
            },
            WorkflowOperation.TEMPORAL_COORDINATION: {
                "name": "Temporal_Coordination",
                "description": "Ensure temporal accuracy across all operations",
                "base_duration": 1.0,
                "criticality": "high",
                "can_disable": False,
                "parallel_capable": True,
                "resource_intensive": False
            },
            WorkflowOperation.PERFORMANCE_OPTIMIZATION: {
                "name": "Performance_Optimization",
                "description": "Optimize system performance and resource utilization",
                "base_duration": 2.0,
                "criticality": "medium",
                "can_disable": True,
                "parallel_capable": True,
                "resource_intensive": False
            },
            WorkflowOperation.INTELLIGENCE_ENHANCEMENT: {
                "name": "Intelligence_Enhancement",
                "description": "Enhance AI capabilities across agent ecosystem",
                "base_duration": 3.0,
                "criticality": "medium",
                "can_disable": True,
                "parallel_capable": True,
                "resource_intensive": False
            },
            WorkflowOperation.SCALABILITY_MANAGEMENT: {
                "name": "Scalability_Management",
                "description": "Configure auto-scaling and load balancing",
                "base_duration": 2.0,
                "criticality": "low",
                "can_disable": True,
                "parallel_capable": True,
                "resource_intensive": False
            }
        }
    
    def _initialize_dependency_rules(self) -> Dict[WorkflowOperation, List[Tuple[WorkflowOperation, DependencyType]]]:
        """Initialize dependency rules between operations"""
        
        return {
            WorkflowOperation.DEEP_WEB_RESEARCH: [
                (WorkflowOperation.TEMPORAL_COORDINATION, DependencyType.REQUIRED)
            ],
            WorkflowOperation.TASK_HIERARCHY_GENERATION: [
                (WorkflowOperation.DEEP_WEB_RESEARCH, DependencyType.REQUIRED),
                (WorkflowOperation.AGENT_COORDINATION, DependencyType.OPTIONAL)
            ],
            WorkflowOperation.AGENT_COORDINATION: [
                (WorkflowOperation.TEMPORAL_COORDINATION, DependencyType.REQUIRED),
                (WorkflowOperation.PERFORMANCE_OPTIMIZATION, DependencyType.OPTIONAL)
            ],
            WorkflowOperation.QUALITY_VALIDATION: [
                (WorkflowOperation.TASK_HIERARCHY_GENERATION, DependencyType.REQUIRED)
            ],
            WorkflowOperation.DOCUMENTATION_CREATION: [
                (WorkflowOperation.TASK_HIERARCHY_GENERATION, DependencyType.REQUIRED),
                (WorkflowOperation.QUALITY_VALIDATION, DependencyType.OPTIONAL)
            ],
            WorkflowOperation.PROJECT_EXECUTION: [
                (WorkflowOperation.TASK_HIERARCHY_GENERATION, DependencyType.REQUIRED),
                (WorkflowOperation.AGENT_COORDINATION, DependencyType.REQUIRED)
            ],
            WorkflowOperation.TEMPORAL_COORDINATION: [],  # No dependencies
            WorkflowOperation.PERFORMANCE_OPTIMIZATION: [
                (WorkflowOperation.TEMPORAL_COORDINATION, DependencyType.OPTIONAL)
            ],
            WorkflowOperation.INTELLIGENCE_ENHANCEMENT: [
                (WorkflowOperation.AGENT_COORDINATION, DependencyType.OPTIONAL)
            ],
            WorkflowOperation.SCALABILITY_MANAGEMENT: [
                (WorkflowOperation.PERFORMANCE_OPTIMIZATION, DependencyType.OPTIONAL)
            ]
        }
    
    async def initialize_preset_templates(self) -> Dict[str, Any]:
        """Initialize preset workflow templates"""
        
        # Research-First Template
        research_first = await self._create_research_first_template()
        self.preset_templates[WorkflowTemplate.RESEARCH_FIRST] = research_first
        
        # Rapid Execution Template
        rapid_execution = await self._create_rapid_execution_template()
        self.preset_templates[WorkflowTemplate.RAPID_EXECUTION] = rapid_execution
        
        # Quality-Focused Template
        quality_focused = await self._create_quality_focused_template()
        self.preset_templates[WorkflowTemplate.QUALITY_FOCUSED] = quality_focused
        
        # Balanced Approach Template
        balanced_approach = await self._create_balanced_approach_template()
        self.preset_templates[WorkflowTemplate.BALANCED_APPROACH] = balanced_approach
        
        # Set default sequence
        self.current_sequence = balanced_approach
        
        return {
            "preset_templates_initialized": True,
            "templates_available": len(self.preset_templates),
            "default_template": WorkflowTemplate.BALANCED_APPROACH.value
        }
    
    async def _create_research_first_template(self) -> WorkflowSequence:
        """Create Research-First workflow template"""
        
        steps = [
            WorkflowStep(
                operation=WorkflowOperation.TEMPORAL_COORDINATION,
                priority=1,
                enabled=True,
                estimated_duration=1.0,
                dependencies=[],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.DEEP_WEB_RESEARCH,
                priority=2,
                enabled=True,
                estimated_duration=12.0,  # Extended research
                dependencies=["temporal_coordination"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.INTELLIGENCE_ENHANCEMENT,
                priority=3,
                enabled=True,
                estimated_duration=3.0,
                dependencies=["deep_web_research"],
                dependency_type=DependencyType.OPTIONAL,
                parallel_group="enhancement"
            ),
            WorkflowStep(
                operation=WorkflowOperation.PERFORMANCE_OPTIMIZATION,
                priority=3,
                enabled=True,
                estimated_duration=2.0,
                dependencies=["deep_web_research"],
                dependency_type=DependencyType.OPTIONAL,
                parallel_group="enhancement"
            ),
            WorkflowStep(
                operation=WorkflowOperation.AGENT_COORDINATION,
                priority=4,
                enabled=True,
                estimated_duration=2.0,
                dependencies=["intelligence_enhancement"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.TASK_HIERARCHY_GENERATION,
                priority=5,
                enabled=True,
                estimated_duration=3.0,
                dependencies=["agent_coordination"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.QUALITY_VALIDATION,
                priority=6,
                enabled=True,
                estimated_duration=5.0,
                dependencies=["task_hierarchy_generation"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.DOCUMENTATION_CREATION,
                priority=7,
                enabled=True,
                estimated_duration=15.0,
                dependencies=["quality_validation"],
                dependency_type=DependencyType.OPTIONAL,
                parallel_group="output"
            ),
            WorkflowStep(
                operation=WorkflowOperation.PROJECT_EXECUTION,
                priority=7,
                enabled=True,
                estimated_duration=30.0,
                dependencies=["quality_validation"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="output"
            )
        ]
        
        total_duration = self._calculate_total_duration(steps)
        
        return WorkflowSequence(
            sequence_id=str(uuid.uuid4()),
            name="Research-First Workflow",
            template=WorkflowTemplate.RESEARCH_FIRST,
            steps=steps,
            total_estimated_duration=total_duration,
            created_at=datetime.now(),
            last_modified=datetime.now()
        )
    
    async def _create_rapid_execution_template(self) -> WorkflowSequence:
        """Create Rapid Execution workflow template"""
        
        steps = [
            WorkflowStep(
                operation=WorkflowOperation.TEMPORAL_COORDINATION,
                priority=1,
                enabled=True,
                estimated_duration=1.0,
                dependencies=[],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.AGENT_COORDINATION,
                priority=2,
                enabled=True,
                estimated_duration=2.0,
                dependencies=["temporal_coordination"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="setup"
            ),
            WorkflowStep(
                operation=WorkflowOperation.DEEP_WEB_RESEARCH,
                priority=2,
                enabled=True,
                estimated_duration=5.0,  # Reduced research time
                dependencies=["temporal_coordination"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="setup"
            ),
            WorkflowStep(
                operation=WorkflowOperation.TASK_HIERARCHY_GENERATION,
                priority=3,
                enabled=True,
                estimated_duration=3.0,
                dependencies=["agent_coordination", "deep_web_research"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.PROJECT_EXECUTION,
                priority=4,
                enabled=True,
                estimated_duration=25.0,  # Reduced execution time
                dependencies=["task_hierarchy_generation"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.QUALITY_VALIDATION,
                priority=5,
                enabled=False,  # Disabled for speed
                estimated_duration=3.0,
                dependencies=["project_execution"],
                dependency_type=DependencyType.OPTIONAL
            ),
            WorkflowStep(
                operation=WorkflowOperation.DOCUMENTATION_CREATION,
                priority=5,
                enabled=False,  # Disabled for speed
                estimated_duration=10.0,
                dependencies=["project_execution"],
                dependency_type=DependencyType.OPTIONAL
            )
        ]
        
        total_duration = self._calculate_total_duration(steps)
        
        return WorkflowSequence(
            sequence_id=str(uuid.uuid4()),
            name="Rapid Execution Workflow",
            template=WorkflowTemplate.RAPID_EXECUTION,
            steps=steps,
            total_estimated_duration=total_duration,
            created_at=datetime.now(),
            last_modified=datetime.now()
        )
    
    async def _create_quality_focused_template(self) -> WorkflowSequence:
        """Create Quality-Focused workflow template"""
        
        steps = [
            WorkflowStep(
                operation=WorkflowOperation.TEMPORAL_COORDINATION,
                priority=1,
                enabled=True,
                estimated_duration=1.0,
                dependencies=[],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.PERFORMANCE_OPTIMIZATION,
                priority=2,
                enabled=True,
                estimated_duration=3.0,  # Extended optimization
                dependencies=["temporal_coordination"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="preparation"
            ),
            WorkflowStep(
                operation=WorkflowOperation.INTELLIGENCE_ENHANCEMENT,
                priority=2,
                enabled=True,
                estimated_duration=4.0,  # Extended enhancement
                dependencies=["temporal_coordination"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="preparation"
            ),
            WorkflowStep(
                operation=WorkflowOperation.DEEP_WEB_RESEARCH,
                priority=3,
                enabled=True,
                estimated_duration=15.0,  # Maximum research time
                dependencies=["performance_optimization", "intelligence_enhancement"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.AGENT_COORDINATION,
                priority=4,
                enabled=True,
                estimated_duration=3.0,  # Extended coordination
                dependencies=["deep_web_research"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.TASK_HIERARCHY_GENERATION,
                priority=5,
                enabled=True,
                estimated_duration=4.0,  # Extended task generation
                dependencies=["agent_coordination"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.QUALITY_VALIDATION,
                priority=6,
                enabled=True,
                estimated_duration=8.0,  # Extended validation
                dependencies=["task_hierarchy_generation"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.DOCUMENTATION_CREATION,
                priority=7,
                enabled=True,
                estimated_duration=20.0,  # Extended documentation
                dependencies=["quality_validation"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.PROJECT_EXECUTION,
                priority=8,
                enabled=True,
                estimated_duration=35.0,  # Extended execution with quality focus
                dependencies=["documentation_creation"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.SCALABILITY_MANAGEMENT,
                priority=9,
                enabled=True,
                estimated_duration=3.0,
                dependencies=["project_execution"],
                dependency_type=DependencyType.OPTIONAL
            )
        ]
        
        total_duration = self._calculate_total_duration(steps)
        
        return WorkflowSequence(
            sequence_id=str(uuid.uuid4()),
            name="Quality-Focused Workflow",
            template=WorkflowTemplate.QUALITY_FOCUSED,
            steps=steps,
            total_estimated_duration=total_duration,
            created_at=datetime.now(),
            last_modified=datetime.now()
        )
    
    async def _create_balanced_approach_template(self) -> WorkflowSequence:
        """Create Balanced Approach workflow template (default)"""
        
        steps = [
            WorkflowStep(
                operation=WorkflowOperation.TEMPORAL_COORDINATION,
                priority=1,
                enabled=True,
                estimated_duration=1.0,
                dependencies=[],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.PERFORMANCE_OPTIMIZATION,
                priority=2,
                enabled=True,
                estimated_duration=2.0,
                dependencies=["temporal_coordination"],
                dependency_type=DependencyType.OPTIONAL,
                parallel_group="setup"
            ),
            WorkflowStep(
                operation=WorkflowOperation.AGENT_COORDINATION,
                priority=2,
                enabled=True,
                estimated_duration=2.0,
                dependencies=["temporal_coordination"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="setup"
            ),
            WorkflowStep(
                operation=WorkflowOperation.DEEP_WEB_RESEARCH,
                priority=3,
                enabled=True,
                estimated_duration=8.0,
                dependencies=["agent_coordination"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.INTELLIGENCE_ENHANCEMENT,
                priority=4,
                enabled=True,
                estimated_duration=3.0,
                dependencies=["deep_web_research"],
                dependency_type=DependencyType.OPTIONAL,
                parallel_group="enhancement"
            ),
            WorkflowStep(
                operation=WorkflowOperation.TASK_HIERARCHY_GENERATION,
                priority=4,
                enabled=True,
                estimated_duration=3.0,
                dependencies=["deep_web_research"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="enhancement"
            ),
            WorkflowStep(
                operation=WorkflowOperation.QUALITY_VALIDATION,
                priority=5,
                enabled=True,
                estimated_duration=5.0,
                dependencies=["task_hierarchy_generation"],
                dependency_type=DependencyType.REQUIRED
            ),
            WorkflowStep(
                operation=WorkflowOperation.DOCUMENTATION_CREATION,
                priority=6,
                enabled=True,
                estimated_duration=15.0,
                dependencies=["quality_validation"],
                dependency_type=DependencyType.OPTIONAL,
                parallel_group="output"
            ),
            WorkflowStep(
                operation=WorkflowOperation.PROJECT_EXECUTION,
                priority=6,
                enabled=True,
                estimated_duration=30.0,
                dependencies=["quality_validation"],
                dependency_type=DependencyType.REQUIRED,
                parallel_group="output"
            ),
            WorkflowStep(
                operation=WorkflowOperation.SCALABILITY_MANAGEMENT,
                priority=7,
                enabled=True,
                estimated_duration=2.0,
                dependencies=["project_execution"],
                dependency_type=DependencyType.OPTIONAL
            )
        ]
        
        total_duration = self._calculate_total_duration(steps)
        
        return WorkflowSequence(
            sequence_id=str(uuid.uuid4()),
            name="Balanced Approach Workflow",
            template=WorkflowTemplate.BALANCED_APPROACH,
            steps=steps,
            total_estimated_duration=total_duration,
            created_at=datetime.now(),
            last_modified=datetime.now()
        )
    
    def _calculate_total_duration(self, steps: List[WorkflowStep]) -> float:
        """Calculate total estimated duration considering parallel execution"""
        
        # Group steps by priority and parallel groups
        priority_groups = {}
        for step in steps:
            if not step.enabled:
                continue
                
            if step.priority not in priority_groups:
                priority_groups[step.priority] = {}
            
            group_key = step.parallel_group or "sequential"
            if group_key not in priority_groups[step.priority]:
                priority_groups[step.priority][group_key] = []
            
            priority_groups[step.priority][group_key].append(step)
        
        # Calculate duration for each priority level
        total_duration = 0.0
        
        for priority in sorted(priority_groups.keys()):
            priority_duration = 0.0
            
            for group_key, group_steps in priority_groups[priority].items():
                if group_key == "sequential":
                    # Sequential steps add up
                    group_duration = sum(step.estimated_duration for step in group_steps)
                else:
                    # Parallel steps take the maximum duration
                    group_duration = max(step.estimated_duration for step in group_steps)
                
                priority_duration = max(priority_duration, group_duration)
            
            total_duration += priority_duration
        
        return total_duration
    
    async def modify_sequence_priority(self, operation: WorkflowOperation, new_priority: int) -> Dict[str, Any]:
        """Modify the priority of a workflow operation"""
        
        if not self.current_sequence:
            return {"error": "No current sequence to modify"}
        
        # Find the step to modify
        step_to_modify = None
        for step in self.current_sequence.steps:
            if step.operation == operation:
                step_to_modify = step
                break
        
        if not step_to_modify:
            return {"error": f"Operation {operation.value} not found in current sequence"}
        
        # Validate new priority
        validation_result = await self.dependency_validator.validate_priority_change(
            self.current_sequence, operation, new_priority
        )
        
        if not validation_result["valid"]:
            return {
                "error": "Priority change violates dependencies",
                "violations": validation_result["violations"]
            }
        
        # Apply priority change
        old_priority = step_to_modify.priority
        step_to_modify.priority = new_priority
        
        # Recalculate total duration
        self.current_sequence.total_estimated_duration = self._calculate_total_duration(
            self.current_sequence.steps
        )
        self.current_sequence.last_modified = datetime.now()
        
        return {
            "success": True,
            "operation": operation.value,
            "old_priority": old_priority,
            "new_priority": new_priority,
            "new_total_duration": self.current_sequence.total_estimated_duration,
            "validation_passed": True
        }
    
    async def toggle_operation(self, operation: WorkflowOperation, enabled: bool) -> Dict[str, Any]:
        """Toggle an operation on/off"""
        
        if not self.current_sequence:
            return {"error": "No current sequence to modify"}
        
        # Find the step to toggle
        step_to_toggle = None
        for step in self.current_sequence.steps:
            if step.operation == operation:
                step_to_toggle = step
                break
        
        if not step_to_toggle:
            return {"error": f"Operation {operation.value} not found in current sequence"}
        
        # Check if operation can be disabled
        operation_def = self.operation_definitions[operation]
        if not enabled and not operation_def["can_disable"]:
            return {
                "error": f"Operation {operation.value} cannot be disabled",
                "reason": f"Critical operation with {operation_def['criticality']} criticality"
            }
        
        # Validate toggle
        validation_result = await self.dependency_validator.validate_operation_toggle(
            self.current_sequence, operation, enabled
        )
        
        if not validation_result["valid"]:
            return {
                "error": "Toggle violates dependencies",
                "violations": validation_result["violations"],
                "warnings": validation_result.get("warnings", [])
            }
        
        # Apply toggle
        old_enabled = step_to_toggle.enabled
        step_to_toggle.enabled = enabled
        
        # Recalculate total duration
        self.current_sequence.total_estimated_duration = self._calculate_total_duration(
            self.current_sequence.steps
        )
        self.current_sequence.last_modified = datetime.now()
        
        return {
            "success": True,
            "operation": operation.value,
            "old_enabled": old_enabled,
            "new_enabled": enabled,
            "new_total_duration": self.current_sequence.total_estimated_duration,
            "impact_warnings": validation_result.get("warnings", [])
        }
    
    async def apply_template(self, template: WorkflowTemplate) -> Dict[str, Any]:
        """Apply a preset workflow template"""
        
        if template not in self.preset_templates:
            return {"error": f"Template {template.value} not found"}
        
        # Apply template
        self.current_sequence = self.preset_templates[template]
        
        # Update statistics
        self.sequence_stats["sequences_created"] += 1
        
        return {
            "success": True,
            "template_applied": template.value,
            "sequence_name": self.current_sequence.name,
            "total_duration": self.current_sequence.total_estimated_duration,
            "enabled_operations": len([s for s in self.current_sequence.steps if s.enabled]),
            "total_operations": len(self.current_sequence.steps)
        }
    
    def get_current_sequence_display(self) -> Dict[str, Any]:
        """Get current sequence for display"""
        
        if not self.current_sequence:
            return {"error": "No current sequence"}
        
        # Sort steps by priority
        sorted_steps = sorted(self.current_sequence.steps, key=lambda x: x.priority)
        
        # Format for display
        display_steps = []
        for step in sorted_steps:
            operation_def = self.operation_definitions[step.operation]
            
            display_steps.append({
                "priority": step.priority,
                "operation": step.operation.value,
                "name": operation_def["name"],
                "description": operation_def["description"],
                "enabled": step.enabled,
                "estimated_duration": step.estimated_duration,
                "criticality": operation_def["criticality"],
                "can_disable": operation_def["can_disable"],
                "parallel_group": step.parallel_group,
                "dependencies": step.dependencies
            })
        
        return {
            "sequence_id": self.current_sequence.sequence_id,
            "name": self.current_sequence.name,
            "template": self.current_sequence.template.value,
            "total_estimated_duration": self.current_sequence.total_estimated_duration,
            "steps": display_steps,
            "last_modified": self.current_sequence.last_modified.isoformat()
        }
    
    def get_available_templates(self) -> Dict[str, Any]:
        """Get available workflow templates"""
        
        templates = {}
        for template, sequence in self.preset_templates.items():
            templates[template.value] = {
                "name": sequence.name,
                "total_duration": sequence.total_estimated_duration,
                "enabled_operations": len([s for s in sequence.steps if s.enabled]),
                "description": self._get_template_description(template)
            }
        
        return {
            "available_templates": templates,
            "current_template": self.current_sequence.template.value if self.current_sequence else None
        }
    
    def _get_template_description(self, template: WorkflowTemplate) -> str:
        """Get description for workflow template"""
        
        descriptions = {
            WorkflowTemplate.RESEARCH_FIRST: "Prioritizes comprehensive research before execution",
            WorkflowTemplate.RAPID_EXECUTION: "Optimized for speed with minimal overhead",
            WorkflowTemplate.QUALITY_FOCUSED: "Maximum quality with extensive validation",
            WorkflowTemplate.BALANCED_APPROACH: "Balanced approach between speed and quality"
        }
        
        return descriptions.get(template, "Custom workflow template")

# Supporting classes
class DependencyValidator:
    """Validates workflow dependencies"""
    
    async def validate_priority_change(self, sequence: WorkflowSequence, 
                                     operation: WorkflowOperation, new_priority: int) -> Dict[str, Any]:
        """Validate priority change against dependencies"""
        # Implementation would check dependency constraints
        return {"valid": True, "violations": []}
    
    async def validate_operation_toggle(self, sequence: WorkflowSequence,
                                      operation: WorkflowOperation, enabled: bool) -> Dict[str, Any]:
        """Validate operation toggle against dependencies"""
        # Implementation would check if disabling breaks dependencies
        return {"valid": True, "violations": [], "warnings": []}

class SequenceOptimizer:
    """Optimizes workflow sequences"""
    
    async def optimize_sequence(self, sequence: WorkflowSequence) -> WorkflowSequence:
        """Optimize workflow sequence for performance"""
        # Implementation would optimize parallel execution and dependencies
        return sequence
