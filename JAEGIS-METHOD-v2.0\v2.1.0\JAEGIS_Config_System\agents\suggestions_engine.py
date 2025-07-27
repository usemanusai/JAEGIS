"""
JAEGIS Configuration Management System - Intelligent Suggestions Engine
AI-powered system for recommending parameter adjustments based on project type and user expertise
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import statistics

from ..core.config_schema import FrequencyParameters, ConfigurationMode, AgentTier
from ..core.config_engine import ConfigurationEngine

logger = logging.getLogger(__name__)

class ProjectType(Enum):
    """Types of projects for optimization suggestions"""
    WEB_APPLICATION = "web_application"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    DATA_ANALYSIS = "data_analysis"
    MACHINE_LEARNING = "machine_learning"
    DOCUMENTATION = "documentation"
    PROTOTYPE = "prototype"
    ENTERPRISE_SYSTEM = "enterprise_system"
    RESEARCH_PROJECT = "research_project"
    MAINTENANCE = "maintenance"

class UserExpertiseLevel(Enum):
    """User expertise levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ProjectPhase(Enum):
    """Project development phases"""
    PLANNING = "planning"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"

@dataclass
class ProjectContext:
    """Context information about the current project"""
    project_type: ProjectType
    user_expertise: UserExpertiseLevel
    project_phase: ProjectPhase
    team_size: int = 1
    timeline_urgency: str = "normal"  # "low", "normal", "high", "critical"
    quality_requirements: str = "normal"  # "low", "normal", "high", "critical"
    complexity_level: str = "medium"  # "low", "medium", "high"
    budget_constraints: str = "normal"  # "tight", "normal", "flexible"

@dataclass
class Suggestion:
    """Configuration suggestion"""
    suggestion_id: str
    title: str
    description: str
    parameter_changes: Dict[str, int]
    confidence_score: float  # 0.0 to 1.0
    reasoning: List[str]
    expected_benefits: List[str]
    potential_drawbacks: List[str]
    priority: str = "medium"  # "low", "medium", "high"
    category: str = "optimization"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "suggestion_id": self.suggestion_id,
            "title": self.title,
            "description": self.description,
            "parameter_changes": self.parameter_changes,
            "confidence_score": self.confidence_score,
            "reasoning": self.reasoning,
            "expected_benefits": self.expected_benefits,
            "potential_drawbacks": self.potential_drawbacks,
            "priority": self.priority,
            "category": self.category
        }

class IntelligentSuggestionsEngine:
    """AI-powered suggestions engine for configuration optimization"""
    
    def __init__(self, config_engine: ConfigurationEngine):
        self.config_engine = config_engine
        
        # Performance tracking
        self.suggestion_history: List[Dict[str, Any]] = []
        self.user_feedback: Dict[str, List[Dict[str, Any]]] = {}
        self.performance_metrics: Dict[str, List[float]] = {}
        
        # Knowledge base for suggestions
        self.project_type_profiles = self._initialize_project_profiles()
        self.expertise_adjustments = self._initialize_expertise_adjustments()
        
        logger.info("Intelligent Suggestions Engine initialized")
    
    def _initialize_project_profiles(self) -> Dict[ProjectType, Dict[str, int]]:
        """Initialize optimal parameter profiles for different project types"""
        return {
            ProjectType.WEB_APPLICATION: {
                "research_intensity": 65,
                "task_decomposition": 70,
                "validation_thoroughness": 85,
                "documentation_detail": 75,
                "tier_1_utilization": 100,
                "tier_2_utilization": 90,
                "tier_3_utilization": 80,
                "tier_4_utilization": 60
            },
            ProjectType.MOBILE_APP: {
                "research_intensity": 70,
                "task_decomposition": 75,
                "validation_thoroughness": 90,
                "documentation_detail": 70,
                "tier_1_utilization": 100,
                "tier_2_utilization": 95,
                "tier_3_utilization": 85,
                "tier_4_utilization": 70
            },
            ProjectType.API_SERVICE: {
                "research_intensity": 60,
                "task_decomposition": 65,
                "validation_thoroughness": 95,
                "documentation_detail": 85,
                "tier_1_utilization": 100,
                "tier_2_utilization": 90,
                "tier_3_utilization": 75,
                "tier_4_utilization": 50
            },
            ProjectType.DATA_ANALYSIS: {
                "research_intensity": 85,
                "task_decomposition": 60,
                "validation_thoroughness": 80,
                "documentation_detail": 90,
                "tier_1_utilization": 100,
                "tier_2_utilization": 85,
                "tier_3_utilization": 90,
                "tier_4_utilization": 80
            },
            ProjectType.MACHINE_LEARNING: {
                "research_intensity": 90,
                "task_decomposition": 70,
                "validation_thoroughness": 85,
                "documentation_detail": 85,
                "tier_1_utilization": 100,
                "tier_2_utilization": 90,
                "tier_3_utilization": 95,
                "tier_4_utilization": 85
            },
            ProjectType.DOCUMENTATION: {
                "research_intensity": 80,
                "task_decomposition": 50,
                "validation_thoroughness": 70,
                "documentation_detail": 95,
                "tier_1_utilization": 100,
                "tier_2_utilization": 70,
                "tier_3_utilization": 60,
                "tier_4_utilization": 40
            },
            ProjectType.PROTOTYPE: {
                "research_intensity": 50,
                "task_decomposition": 40,
                "validation_thoroughness": 60,
                "documentation_detail": 50,
                "tier_1_utilization": 100,
                "tier_2_utilization": 80,
                "tier_3_utilization": 50,
                "tier_4_utilization": 30
            },
            ProjectType.ENTERPRISE_SYSTEM: {
                "research_intensity": 75,
                "task_decomposition": 85,
                "validation_thoroughness": 95,
                "documentation_detail": 90,
                "tier_1_utilization": 100,
                "tier_2_utilization": 95,
                "tier_3_utilization": 90,
                "tier_4_utilization": 80
            },
            ProjectType.RESEARCH_PROJECT: {
                "research_intensity": 95,
                "task_decomposition": 75,
                "validation_thoroughness": 85,
                "documentation_detail": 95,
                "tier_1_utilization": 100,
                "tier_2_utilization": 90,
                "tier_3_utilization": 95,
                "tier_4_utilization": 90
            },
            ProjectType.MAINTENANCE: {
                "research_intensity": 60,
                "task_decomposition": 55,
                "validation_thoroughness": 85,
                "documentation_detail": 70,
                "tier_1_utilization": 100,
                "tier_2_utilization": 80,
                "tier_3_utilization": 70,
                "tier_4_utilization": 40
            }
        }
    
    def _initialize_expertise_adjustments(self) -> Dict[UserExpertiseLevel, Dict[str, float]]:
        """Initialize adjustments based on user expertise level"""
        return {
            UserExpertiseLevel.BEGINNER: {
                "research_intensity": 1.2,  # More research for beginners
                "task_decomposition": 1.3,  # More detailed breakdowns
                "validation_thoroughness": 1.1,  # Extra validation
                "documentation_detail": 1.2,  # More documentation
                "agent_utilization": 1.1  # More agent assistance
            },
            UserExpertiseLevel.INTERMEDIATE: {
                "research_intensity": 1.0,
                "task_decomposition": 1.0,
                "validation_thoroughness": 1.0,
                "documentation_detail": 1.0,
                "agent_utilization": 1.0
            },
            UserExpertiseLevel.ADVANCED: {
                "research_intensity": 0.9,  # Less research needed
                "task_decomposition": 0.9,  # Can handle larger tasks
                "validation_thoroughness": 0.95,  # Still need validation
                "documentation_detail": 0.9,  # Less detailed docs
                "agent_utilization": 0.9  # Less agent assistance
            },
            UserExpertiseLevel.EXPERT: {
                "research_intensity": 0.8,
                "task_decomposition": 0.8,
                "validation_thoroughness": 0.9,
                "documentation_detail": 0.8,
                "agent_utilization": 0.8
            }
        }
    
    def generate_suggestions(self, project_context: ProjectContext) -> List[Suggestion]:
        """Generate configuration suggestions based on project context"""
        suggestions = []
        current_config = self.config_engine.get_current_config()
        current_params = current_config.frequency_parameters
        
        # Get optimal profile for project type
        optimal_profile = self.project_type_profiles.get(project_context.project_type, {})
        if not optimal_profile:
            return suggestions
        
        # Apply expertise adjustments
        expertise_adjustments = self.expertise_adjustments.get(project_context.user_expertise, {})
        
        # Calculate suggested parameters
        suggested_params = {}
        for param_name in ["research_intensity", "task_decomposition", "validation_thoroughness", "documentation_detail"]:
            base_value = optimal_profile.get(param_name, 70)
            adjustment = expertise_adjustments.get(param_name, 1.0)
            suggested_value = min(100, max(0, int(base_value * adjustment)))
            suggested_params[param_name] = suggested_value
        
        # Apply phase-specific adjustments
        suggested_params = self._apply_phase_adjustments(suggested_params, project_context.project_phase)
        
        # Apply urgency and quality adjustments
        suggested_params = self._apply_urgency_adjustments(suggested_params, project_context.timeline_urgency)
        suggested_params = self._apply_quality_adjustments(suggested_params, project_context.quality_requirements)
        
        # Generate suggestions for significant differences
        parameter_suggestions = self._generate_parameter_suggestions(current_params, suggested_params, project_context)
        suggestions.extend(parameter_suggestions)
        
        # Generate agent utilization suggestions
        agent_suggestions = self._generate_agent_utilization_suggestions(current_params, optimal_profile, project_context)
        suggestions.extend(agent_suggestions)
        
        # Generate preset mode suggestions
        preset_suggestions = self._generate_preset_suggestions(project_context)
        suggestions.extend(preset_suggestions)
        
        # Sort suggestions by confidence score
        suggestions.sort(key=lambda s: s.confidence_score, reverse=True)
        
        return suggestions[:10]  # Return top 10 suggestions
    
    def _apply_phase_adjustments(self, params: Dict[str, int], phase: ProjectPhase) -> Dict[str, int]:
        """Apply adjustments based on project phase"""
        adjustments = {
            ProjectPhase.PLANNING: {
                "research_intensity": 1.2,
                "task_decomposition": 1.3,
                "validation_thoroughness": 0.9,
                "documentation_detail": 1.1
            },
            ProjectPhase.DEVELOPMENT: {
                "research_intensity": 1.0,
                "task_decomposition": 1.0,
                "validation_thoroughness": 1.0,
                "documentation_detail": 0.9
            },
            ProjectPhase.TESTING: {
                "research_intensity": 0.8,
                "task_decomposition": 0.9,
                "validation_thoroughness": 1.3,
                "documentation_detail": 1.0
            },
            ProjectPhase.DEPLOYMENT: {
                "research_intensity": 0.7,
                "task_decomposition": 0.8,
                "validation_thoroughness": 1.2,
                "documentation_detail": 1.2
            },
            ProjectPhase.MAINTENANCE: {
                "research_intensity": 0.9,
                "task_decomposition": 0.8,
                "validation_thoroughness": 1.1,
                "documentation_detail": 1.0
            }
        }
        
        phase_adjustments = adjustments.get(phase, {})
        adjusted_params = {}
        
        for param_name, value in params.items():
            adjustment = phase_adjustments.get(param_name, 1.0)
            adjusted_params[param_name] = min(100, max(0, int(value * adjustment)))
        
        return adjusted_params
    
    def _apply_urgency_adjustments(self, params: Dict[str, int], urgency: str) -> Dict[str, int]:
        """Apply adjustments based on timeline urgency""urgency_multipliers_eq_low": {"research_intensity": 1.1, "task_decomposition": 1.1, "validation_thoroughness": 1.0, "documentation_detail1_1_normal": {"research_intensity": 1.0, "task_decomposition": 1.0, "validation_thoroughness": 1.0, "documentation_detail1_0_high": {"research_intensity": 0.8, "task_decomposition": 0.9, "validation_thoroughness": 0.9, "documentation_detail0_8_critical": {"research_intensity": 0.6, "task_decomposition": 0.7, "validation_thoroughness": 0.8, "documentation_detail": 0.6}
        }
        
        multipliers = urgency_multipliers.get(urgency, urgency_multipliers["normal"])
        adjusted_params = {}
        
        for param_name, value in params.items():
            multiplier = multipliers.get(param_name, 1.0)
            adjusted_params[param_name] = min(100, max(0, int(value * multiplier)))
        
        return adjusted_params
    
    def _apply_quality_adjustments(self, params: Dict[str, int], quality_req: str) -> Dict[str, int]:
        """Apply adjustments based on quality requirements""quality_multipliers_eq_low": {"research_intensity": 0.8, "task_decomposition": 0.8, "validation_thoroughness": 0.7, "documentation_detail0_7_normal": {"research_intensity": 1.0, "task_decomposition": 1.0, "validation_thoroughness": 1.0, "documentation_detail1_0_high": {"research_intensity": 1.1, "task_decomposition": 1.1, "validation_thoroughness": 1.2, "documentation_detail1_2_critical": {"research_intensity": 1.2, "task_decomposition": 1.2, "validation_thoroughness": 1.4, "documentation_detail": 1.3}
        }
        
        multipliers = quality_multipliers.get(quality_req, quality_multipliers["normal"])
        adjusted_params = {}
        
        for param_name, value in params.items():
            multiplier = multipliers.get(param_name, 1.0)
            adjusted_params[param_name] = min(100, max(0, int(value * multiplier)))
        
        return adjusted_params
    
    def _generate_parameter_suggestions(self, current_params: FrequencyParameters, 
                                      suggested_params: Dict[str, int], 
                                      context: ProjectContext) -> List[Suggestion]:
        """Generate suggestions for parameter adjustments"""
        suggestions = []
        
        for param_name, suggested_value in suggested_params.items():
            current_value = getattr(current_params, param_name)
            difference = abs(suggested_value - current_value)
            
            # Only suggest if difference is significant (>= 10%)
            if difference >= 10:
                confidence = min(1.0, difference / 50.0)  # Higher confidence for larger differences
                
                direction = "increase" if suggested_value > current_value else "decrease"
                
                suggestion = Suggestion(
                    suggestion_id=f"param_{param_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    title=f"{direction.title()} {param_name.replace('_', ' ').title()}",
                    description=f"Adjust {param_name.replace('_', ' ')} from {current_value}% to {suggested_value}% for {context.project_type.value} projects",
                    parameter_changes={param_name: suggested_value},
                    confidence_score=confidence,
                    reasoning=[
                        f"Optimal for {context.project_type.value} projects",
                        f"Adjusted for {context.user_expertise.value} expertise level",
                        f"Optimized for {context.project_phase.value} phase"
                    ],
                    expected_benefits=self._get_parameter_benefits(param_name, direction),
                    potential_drawbacks=self._get_parameter_drawbacks(param_name, direction),
                    priority="high" if difference >= 30 else "medium",
                    category="parameter_optimization"
                )
                
                suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_agent_utilization_suggestions(self, current_params: FrequencyParameters,
                                              optimal_profile: Dict[str, int],
                                              context: ProjectContext) -> List[Suggestion]:
        """Generate suggestions for agent utilization adjustments"""
        suggestions = []
        
        tier_mapping = {
            "tier_1_utilization": AgentTier.TIER_1_ORCHESTRATOR,
            "tier_2_utilization": AgentTier.TIER_2_PRIMARY,
            "tier_3_utilization": AgentTier.TIER_3_SECONDARY,
            "tier_4_utilization": AgentTier.TIER_4_SPECIALIZED
        }
        
        for tier_key, agent_tier in tier_mapping.items():
            if tier_key in optimal_profile:
                suggested_value = optimal_profile[tier_key]
                current_value = current_params.agent_utilization.get(agent_tier, 50)
                difference = abs(suggested_value - current_value)
                
                if difference >= 15:  # Suggest if difference >= 15%
                    confidence = min(1.0, difference / 40.0)
                    direction = "increase" if suggested_value > current_value else "decrease"
                    
                    suggestion = Suggestion(
                        suggestion_id=f"agent_{tier_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        title=f"{direction.title()} {agent_tier.value.replace('_', ' ').title()} Agent Utilization",
                        description=f"Adjust {agent_tier.value} utilization from {current_value}% to {suggested_value}%",
                        parameter_changes={f"agent_utilization.{agent_tier.value}": suggested_value},
                        confidence_score=confidence,
                        reasoning=[
                            f"Optimal agent mix for {context.project_type.value}",
                            f"Balanced resource allocation",
                            f"Improved efficiency for project type"
                        ],
                        expected_benefits=[
                            "Better resource utilization",
                            "Improved workflow efficiency",
                            "Optimized agent collaboration"
                        ],
                        potential_drawbacks=[
                            "May require adjustment period",
                            "Could affect familiar workflows"
                        ],
                        priority="medium",
                        category="agent_optimization"
                    )
                    
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_preset_suggestions(self, context: ProjectContext) -> List[Suggestion]:
        """Generate suggestions for preset configuration modes"""
        suggestions = []
        
        # Suggest preset based on project characteristics
        if context.timeline_urgency in ["high", "critical"]:
            suggestion = Suggestion(
                suggestion_id=f"preset_speed_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Apply Speed Mode Configuration",
                description="Switch to Speed Mode for faster turnaround times",
                parameter_changes={"preset_mode": "speed_mode"},
                confidence_score=0.8,
                reasoning=[
                    "High urgency timeline detected",
                    "Speed mode optimizes for fast delivery",
                    "Reduces processing overhead"
                ],
                expected_benefits=[
                    "Faster response times",
                    "Quicker project completion",
                    "Reduced processing delays"
                ],
                potential_drawbacks=[
                    "May reduce output quality",
                    "Less thorough validation",
                    "Simplified documentation"
                ],
                priority="high",
                category="preset_mode"
            )
            suggestions.append(suggestion)
        
        elif context.quality_requirements in ["high", "critical"]:
            suggestion = Suggestion(
                suggestion_id=f"preset_quality_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Apply Quality Mode Configuration",
                description="Switch to Quality Mode for highest output quality",
                parameter_changes={"preset_mode": "quality_mode"},
                confidence_score=0.9,
                reasoning=[
                    "High quality requirements detected",
                    "Quality mode maximizes output quality",
                    "Enhanced validation and documentation"
                ],
                expected_benefits=[
                    "Higher output quality",
                    "Comprehensive validation",
                    "Detailed documentation"
                ],
                potential_drawbacks=[
                    "Longer processing times",
                    "Increased resource usage",
                    "More complex workflows"
                ],
                priority="high",
                category="preset_mode"
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_parameter_benefits(self, parameter_name: str, direction: str) -> List[str]:
        """Get expected benefits for parameter changes""benefits_map_eq_research_intensity": {
                "increase": ["More thorough research", "Better informed decisions", "Higher quality insights"],
                "decrease": ["Faster initial responses", "Quicker project start", "Reduced_research_overheadtask_decomposition": {
                "increase": ["Better project organization", "Clearer task structure", "Improved tracking"],
                "decrease": ["Simpler workflows", "Faster task execution", "Less_planning_overheadvalidation_thoroughness": {
                "increase": ["Higher output quality", "Fewer errors", "Better reliability"],
                "decrease": ["Faster processing", "Quicker iterations", "Reduced_validation_timedocumentation_detail": {
                "increase": ["Better project handoff", "Comprehensive guides", "Improved maintainability"],
                "decrease": ["Faster documentation", "Concise outputs", "Reduced documentation time"]
            }
        }
        
        return benefits_map.get(parameter_name, {}).get(direction, ["Improved workflow efficiency"])
    
    def _get_parameter_drawbacks(self, parameter_name: str, direction: str) -> List[str]:
        """Get potential drawbacks for parameter changes""drawbacks_map_eq_research_intensity": {
                "increase": ["Longer initial response times", "Increased processing overhead"],
                "decrease": ["Potentially less comprehensive research", "May_miss_important_informationtask_decomposition": {
                "increase": ["More complex project structure", "Increased planning time"],
                "decrease": ["Less detailed task breakdown", "Potential_oversight_of_subtasksvalidation_thoroughness": {
                "increase": ["Longer processing times", "Increased resource usage"],
                "decrease": ["Potential quality issues", "Reduced_error_detectiondocumentation_detail": {
                "increase": ["Longer documentation time", "More complex outputs"],
                "decrease": ["Less comprehensive documentation", "Potential information gaps"]
            }
        }
        
        return drawbacks_map.get(parameter_name, {}).get(direction, ["May require adjustment period"])
    
    def record_suggestion_feedback(self, suggestion_id: str, feedback: Dict[str, Any]):
        """Record user feedback on suggestions"""
        if suggestion_id not in self.user_feedback:
            self.user_feedback[suggestion_id] = []
        
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback
        }
        
        self.user_feedback[suggestion_id].append(feedback_entry)
        
        # Update suggestion quality metrics
        self._update_suggestion_metrics(suggestion_id, feedback)
    
    def _update_suggestion_metrics(self, suggestion_id: str, feedback: Dict[str, Any]):
        """Update suggestion quality metrics based on feedback"""
        # This would implement machine learning to improve suggestions over time
        # For now, just log the feedback
        logger.info(f"Received feedback for suggestion {suggestion_id}: {feedback}")
    
    def get_suggestion_statistics(self) -> Dict[str, Any]:
        """Get statistics about suggestion performance"""
        total_suggestions = len(self.suggestion_history)
        total_feedback = sum(len(feedback_list) for feedback_list in self.user_feedback.values())
        
        return {
            "total_suggestions_generated": total_suggestions,
            "total_feedback_received": total_feedback,
            "feedback_rate": total_feedback / total_suggestions if total_suggestions > 0 else 0,
            "supported_project_types": len(self.project_type_profiles),
            "supported_expertise_levels": len(self.expertise_adjustments)
        }
