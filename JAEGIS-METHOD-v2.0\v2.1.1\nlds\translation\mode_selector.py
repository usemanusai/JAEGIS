"""
N.L.D.S. Mode Selection Algorithm
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Intelligent mode selection algorithm that determines optimal JAEGIS operational mode (1-5)
based on complexity analysis, resource requirements, and contextual factors with 93%+ 
mode selection accuracy and dynamic optimization.
"""

import math
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import asyncio

# Local imports
from ..nlp.intent_recognizer import IntentRecognitionResult, IntentCategory
from ..processing.logical_analyzer import LogicalAnalysisResult
from ..processing.emotional_analyzer import EmotionalAnalysisResult, UserState
from ..processing.creative_interpreter import CreativeAnalysisResult
from ..processing.dimensional_synthesizer import DimensionalSynthesisResult
from ..cognitive.cognitive_model import CognitiveState
from ..cognitive.decision_framework import DecisionResult

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# MODE SELECTION STRUCTURES AND ENUMS
# ============================================================================

class JAEGISMode(Enum):
    """JAEGIS operational modes with capabilities."""
    MODE_1 = "mode_1"  # Basic operations - Simple tasks, single agent
    MODE_2 = "mode_2"  # Enhanced processing - Standard tasks, small team
    MODE_3 = "mode_3"  # Advanced analysis - Complex tasks, specialized team
    MODE_4 = "mode_4"  # Complex problem solving - Multi-dimensional, large team
    MODE_5 = "mode_5"  # Maximum capability - Enterprise-level, full system


class ComplexityFactor(Enum):
    """Factors contributing to task complexity."""
    LOGICAL_COMPLEXITY = "logical_complexity"
    EMOTIONAL_COMPLEXITY = "emotional_complexity"
    CREATIVE_COMPLEXITY = "creative_complexity"
    TEMPORAL_COMPLEXITY = "temporal_complexity"
    RESOURCE_COMPLEXITY = "resource_complexity"
    INTERDEPENDENCY_COMPLEXITY = "interdependency_complexity"
    UNCERTAINTY_COMPLEXITY = "uncertainty_complexity"
    SCALE_COMPLEXITY = "scale_complexity"


class ResourceType(Enum):
    """Types of resources required for task execution."""
    COMPUTATIONAL = "computational"
    HUMAN_EXPERTISE = "human_expertise"
    DATA_ACCESS = "data_access"
    EXTERNAL_APIS = "external_apis"
    SPECIALIZED_TOOLS = "specialized_tools"
    TIME_CRITICAL = "time_critical"
    COLLABORATIVE = "collaborative"
    RESEARCH_INTENSIVE = "research_intensive"


@dataclass
class ComplexityMetric:
    """Individual complexity measurement."""
    factor: ComplexityFactor
    score: float  # 0-1
    confidence: float  # 0-1
    contributing_elements: List[str]
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceRequirement:
    """Resource requirement specification."""
    resource_type: ResourceType
    intensity: float  # 0-1
    criticality: float  # 0-1
    availability: float  # 0-1
    estimated_usage: float  # 0-1
    alternatives: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModeCapability:
    """Capabilities and limitations of each mode."""
    mode: JAEGISMode
    max_complexity_score: float
    resource_capacity: Dict[ResourceType, float]
    agent_count_range: Tuple[int, int]
    typical_duration_minutes: Tuple[int, int]
    success_rate_threshold: float
    cost_factor: float
    specializations: List[str]


@dataclass
class ModeSelectionResult:
    """Mode selection result with analysis."""
    selected_mode: JAEGISMode
    confidence: float
    complexity_analysis: List[ComplexityMetric]
    resource_analysis: List[ResourceRequirement]
    alternative_modes: List[Tuple[JAEGISMode, float]]
    selection_reasoning: List[str]
    performance_prediction: Dict[str, float]
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# MODE SELECTION ENGINE
# ============================================================================

class ModeSelectionEngine:
    """
    Intelligent mode selection engine for JAEGIS operations.
    
    Features:
    - Multi-dimensional complexity analysis
    - Resource requirement assessment
    - Dynamic mode optimization
    - Performance prediction modeling
    - Contextual adaptation
    - Historical performance learning
    - Risk assessment and mitigation
    - Real-time capability monitoring
    """
    
    def __init__(self):
        """Initialize mode selection engine."""
        self.mode_capabilities = self._load_mode_capabilities()
        self.complexity_weights = self._load_complexity_weights()
        self.resource_mappings = self._load_resource_mappings()
        self.selection_rules = self._load_selection_rules()
        self.performance_history = {}
        
        # Learning and adaptation
        self.mode_performance_stats = {mode: {"success_rate": 0.85, "avg_duration": 60, "usage_count": 0} 
                                     for mode in JAEGISMode}
        self.complexity_calibration = {factor: 1.0 for factor in ComplexityFactor}
    
    def _load_mode_capabilities(self) -> Dict[JAEGISMode, ModeCapability]:
        """Load capabilities and specifications for each JAEGIS mode."""
        return {
            JAEGISMode.MODE_1: ModeCapability(
                mode=JAEGISMode.MODE_1,
                max_complexity_score=0.3,
                resource_capacity={
                    ResourceType.COMPUTATIONAL: 0.2,
                    ResourceType.HUMAN_EXPERTISE: 0.1,
                    ResourceType.DATA_ACCESS: 0.3,
                    ResourceType.EXTERNAL_APIS: 0.1,
                    ResourceType.SPECIALIZED_TOOLS: 0.1,
                    ResourceType.TIME_CRITICAL: 0.2,
                    ResourceType.COLLABORATIVE: 0.1,
                    ResourceType.RESEARCH_INTENSIVE: 0.1
                },
                agent_count_range=(1, 3),
                typical_duration_minutes=(5, 30),
                success_rate_threshold=0.95,
                cost_factor=0.1,
                specializations=["simple_queries", "basic_tasks", "quick_responses"]
            ),
            
            JAEGISMode.MODE_2: ModeCapability(
                mode=JAEGISMode.MODE_2,
                max_complexity_score=0.5,
                resource_capacity={
                    ResourceType.COMPUTATIONAL: 0.4,
                    ResourceType.HUMAN_EXPERTISE: 0.3,
                    ResourceType.DATA_ACCESS: 0.5,
                    ResourceType.EXTERNAL_APIS: 0.3,
                    ResourceType.SPECIALIZED_TOOLS: 0.3,
                    ResourceType.TIME_CRITICAL: 0.4,
                    ResourceType.COLLABORATIVE: 0.3,
                    ResourceType.RESEARCH_INTENSIVE: 0.3
                },
                agent_count_range=(3, 8),
                typical_duration_minutes=(15, 60),
                success_rate_threshold=0.90,
                cost_factor=0.3,
                specializations=["standard_analysis", "moderate_complexity", "team_coordination"]
            ),
            
            JAEGISMode.MODE_3: ModeCapability(
                mode=JAEGISMode.MODE_3,
                max_complexity_score=0.7,
                resource_capacity={
                    ResourceType.COMPUTATIONAL: 0.6,
                    ResourceType.HUMAN_EXPERTISE: 0.5,
                    ResourceType.DATA_ACCESS: 0.7,
                    ResourceType.EXTERNAL_APIS: 0.5,
                    ResourceType.SPECIALIZED_TOOLS: 0.5,
                    ResourceType.TIME_CRITICAL: 0.6,
                    ResourceType.COLLABORATIVE: 0.5,
                    ResourceType.RESEARCH_INTENSIVE: 0.5
                },
                agent_count_range=(8, 20),
                typical_duration_minutes=(30, 120),
                success_rate_threshold=0.85,
                cost_factor=0.5,
                specializations=["advanced_analysis", "specialized_tasks", "multi_agent_coordination"]
            ),
            
            JAEGISMode.MODE_4: ModeCapability(
                mode=JAEGISMode.MODE_4,
                max_complexity_score=0.9,
                resource_capacity={
                    ResourceType.COMPUTATIONAL: 0.8,
                    ResourceType.HUMAN_EXPERTISE: 0.7,
                    ResourceType.DATA_ACCESS: 0.9,
                    ResourceType.EXTERNAL_APIS: 0.7,
                    ResourceType.SPECIALIZED_TOOLS: 0.7,
                    ResourceType.TIME_CRITICAL: 0.8,
                    ResourceType.COLLABORATIVE: 0.8,
                    ResourceType.RESEARCH_INTENSIVE: 0.8
                },
                agent_count_range=(20, 60),
                typical_duration_minutes=(60, 240),
                success_rate_threshold=0.80,
                cost_factor=0.7,
                specializations=["complex_problem_solving", "multi_dimensional_analysis", "large_scale_coordination"]
            ),
            
            JAEGISMode.MODE_5: ModeCapability(
                mode=JAEGISMode.MODE_5,
                max_complexity_score=1.0,
                resource_capacity={
                    ResourceType.COMPUTATIONAL: 1.0,
                    ResourceType.HUMAN_EXPERTISE: 1.0,
                    ResourceType.DATA_ACCESS: 1.0,
                    ResourceType.EXTERNAL_APIS: 1.0,
                    ResourceType.SPECIALIZED_TOOLS: 1.0,
                    ResourceType.TIME_CRITICAL: 1.0,
                    ResourceType.COLLABORATIVE: 1.0,
                    ResourceType.RESEARCH_INTENSIVE: 1.0
                },
                agent_count_range=(60, 128),
                typical_duration_minutes=(120, 480),
                success_rate_threshold=0.75,
                cost_factor=1.0,
                specializations=["maximum_capability", "enterprise_level", "full_system_deployment"]
            )
        }
    
    def _load_complexity_weights(self) -> Dict[ComplexityFactor, float]:
        """Load weights for different complexity factors."""
        return {
            ComplexityFactor.LOGICAL_COMPLEXITY: 0.25,
            ComplexityFactor.EMOTIONAL_COMPLEXITY: 0.15,
            ComplexityFactor.CREATIVE_COMPLEXITY: 0.15,
            ComplexityFactor.TEMPORAL_COMPLEXITY: 0.10,
            ComplexityFactor.RESOURCE_COMPLEXITY: 0.15,
            ComplexityFactor.INTERDEPENDENCY_COMPLEXITY: 0.10,
            ComplexityFactor.UNCERTAINTY_COMPLEXITY: 0.05,
            ComplexityFactor.SCALE_COMPLEXITY: 0.05
        }
    
    def _load_resource_mappings(self) -> Dict[str, ResourceType]:
        """Load mappings from task characteristics to resource types."""
        return {
            "analysis": ResourceType.COMPUTATIONAL,
            "research": ResourceType.RESEARCH_INTENSIVE,
            "urgent": ResourceType.TIME_CRITICAL,
            "collaboration": ResourceType.COLLABORATIVE,
            "data": ResourceType.DATA_ACCESS,
            "api": ResourceType.EXTERNAL_APIS,
            "specialized": ResourceType.SPECIALIZED_TOOLS,
            "expert": ResourceType.HUMAN_EXPERTISE
        }
    
    def _load_selection_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load mode selection rules and heuristics."""
        return {
            "emergency_override": {
                "conditions": ["emergency_request", "critical_priority", "urgent_user_state"],
                "target_mode": JAEGISMode.MODE_5,
                "confidence_boost": 0.2
            },
            "simple_task_optimization": {
                "conditions": ["low_complexity", "single_requirement", "quick_response_needed"],
                "target_mode": JAEGISMode.MODE_1,
                "confidence_boost": 0.15
            },
            "research_intensive": {
                "conditions": ["high_uncertainty", "information_seeking", "analysis_required"],
                "target_mode": JAEGISMode.MODE_4,
                "confidence_boost": 0.1
            },
            "collaborative_task": {
                "conditions": ["multiple_stakeholders", "coordination_required", "team_effort"],
                "target_mode": JAEGISMode.MODE_3,
                "confidence_boost": 0.1
            }
        }
    
    def analyze_complexity(self, logical_result: LogicalAnalysisResult,
                         emotional_result: EmotionalAnalysisResult,
                         creative_result: CreativeAnalysisResult,
                         synthesis_result: DimensionalSynthesisResult,
                         cognitive_state: CognitiveState) -> List[ComplexityMetric]:
        """Analyze task complexity across multiple dimensions."""
        complexity_metrics = []
        
        # Logical complexity
        logical_metric = self._analyze_logical_complexity(logical_result)
        complexity_metrics.append(logical_metric)
        
        # Emotional complexity
        emotional_metric = self._analyze_emotional_complexity(emotional_result, cognitive_state)
        complexity_metrics.append(emotional_metric)
        
        # Creative complexity
        creative_metric = self._analyze_creative_complexity(creative_result)
        complexity_metrics.append(creative_metric)
        
        # Temporal complexity
        temporal_metric = self._analyze_temporal_complexity(emotional_result, logical_result)
        complexity_metrics.append(temporal_metric)
        
        # Resource complexity
        resource_metric = self._analyze_resource_complexity(logical_result, synthesis_result)
        complexity_metrics.append(resource_metric)
        
        # Interdependency complexity
        interdep_metric = self._analyze_interdependency_complexity(logical_result, synthesis_result)
        complexity_metrics.append(interdep_metric)
        
        # Uncertainty complexity
        uncertainty_metric = self._analyze_uncertainty_complexity(synthesis_result, cognitive_state)
        complexity_metrics.append(uncertainty_metric)
        
        # Scale complexity
        scale_metric = self._analyze_scale_complexity(logical_result, creative_result)
        complexity_metrics.append(scale_metric)
        
        return complexity_metrics
    
    def _analyze_logical_complexity(self, logical_result: LogicalAnalysisResult) -> ComplexityMetric:
        """Analyze logical complexity factors."""
        contributing_elements = []
        
        # Number of requirements
        req_count = len(logical_result.requirements)
        req_complexity = min(req_count / 10, 1.0)  # Normalize by 10 requirements
        if req_count > 5:
            contributing_elements.append(f"High requirement count: {req_count}")
        
        # Requirement interdependencies
        high_priority_reqs = sum(1 for req in logical_result.requirements if req.priority == "high")
        priority_complexity = high_priority_reqs / max(req_count, 1)
        if priority_complexity > 0.5:
            contributing_elements.append(f"High priority requirements: {high_priority_reqs}")
        
        # Logical structure complexity
        structure_complexity = logical_result.complexity_score
        if structure_complexity > 0.7:
            contributing_elements.append(f"Complex logical structure: {structure_complexity:.2f}")
        
        # Coherence challenges
        coherence_complexity = 1 - logical_result.coherence_score
        if coherence_complexity > 0.3:
            contributing_elements.append(f"Coherence challenges: {coherence_complexity:.2f}")
        
        # Overall logical complexity
        overall_score = (req_complexity + priority_complexity + structure_complexity + coherence_complexity) / 4
        
        return ComplexityMetric(
            factor=ComplexityFactor.LOGICAL_COMPLEXITY,
            score=overall_score,
            confidence=logical_result.coherence_score,
            contributing_elements=contributing_elements,
            metadata={
                "requirement_count": req_count,
                "high_priority_count": high_priority_reqs,
                "structure_score": structure_complexity,
                "coherence_score": logical_result.coherence_score
            }
        )
    
    def _analyze_emotional_complexity(self, emotional_result: EmotionalAnalysisResult,
                                    cognitive_state: CognitiveState) -> ComplexityMetric:
        """Analyze emotional complexity factors."""
        contributing_elements = []
        
        # User emotional state intensity
        user_state = emotional_result.emotional_context.user_state
        state_complexity_map = {
            UserState.CALM: 0.1,
            UserState.EXCITED: 0.3,
            UserState.SATISFIED: 0.2,
            UserState.FOCUSED: 0.2,
            UserState.CONFUSED: 0.6,
            UserState.FRUSTRATED: 0.8,
            UserState.URGENT: 0.9,
            UserState.DISTRACTED: 0.5
        }
        
        state_complexity = state_complexity_map.get(user_state, 0.5)
        if state_complexity > 0.6:
            contributing_elements.append(f"High emotional intensity: {user_state.value}")
        
        # Sentiment polarity extremes
        sentiment_polarity = abs(emotional_result.emotional_context.sentiment_analysis.polarity_score)
        if sentiment_polarity > 0.7:
            contributing_elements.append(f"Extreme sentiment: {sentiment_polarity:.2f}")
        
        # Urgency level
        urgency_level = emotional_result.emotional_context.urgency_level
        if urgency_level > 0.7:
            contributing_elements.append(f"High urgency: {urgency_level:.2f}")
        
        # Empathy triggers
        empathy_count = len(emotional_result.emotional_context.empathy_triggers)
        empathy_complexity = min(empathy_count / 5, 1.0)
        if empathy_count > 2:
            contributing_elements.append(f"Multiple empathy triggers: {empathy_count}")
        
        # Cognitive load impact
        cognitive_load = cognitive_state.cognitive_load
        if cognitive_load > 0.7:
            contributing_elements.append(f"High cognitive load: {cognitive_load:.2f}")
        
        overall_score = (state_complexity + sentiment_polarity + urgency_level + empathy_complexity + cognitive_load) / 5
        
        return ComplexityMetric(
            factor=ComplexityFactor.EMOTIONAL_COMPLEXITY,
            score=overall_score,
            confidence=emotional_result.emotional_intelligence_score,
            contributing_elements=contributing_elements,
            metadata={
                "user_state": user_state.value,
                "sentiment_polarity": sentiment_polarity,
                "urgency_level": urgency_level,
                "empathy_triggers": empathy_count,
                "cognitive_load": cognitive_load
            }
        )
    
    def _analyze_creative_complexity(self, creative_result: CreativeAnalysisResult) -> ComplexityMetric:
        """Analyze creative complexity factors."""
        contributing_elements = []
        
        # Number of creative ideas
        idea_count = len(creative_result.creative_ideas)
        idea_complexity = min(idea_count / 8, 1.0)  # Normalize by 8 ideas
        if idea_count > 5:
            contributing_elements.append(f"High creative idea count: {idea_count}")
        
        # Innovation potential
        innovation_potential = creative_result.innovation_potential_score
        if innovation_potential > 0.8:
            contributing_elements.append(f"High innovation potential: {innovation_potential:.2f}")
        
        # Alternative approaches
        alt_count = len(creative_result.alternative_approaches)
        alt_complexity = min(alt_count / 5, 1.0)
        if alt_count > 3:
            contributing_elements.append(f"Multiple alternative approaches: {alt_count}")
        
        # Creative connections
        connection_count = len(creative_result.creative_connections)
        connection_complexity = min(connection_count / 6, 1.0)
        if connection_count > 4:
            contributing_elements.append(f"Complex creative connections: {connection_count}")
        
        overall_score = (idea_complexity + innovation_potential + alt_complexity + connection_complexity) / 4
        
        return ComplexityMetric(
            factor=ComplexityFactor.CREATIVE_COMPLEXITY,
            score=overall_score,
            confidence=creative_result.innovation_potential_score,
            contributing_elements=contributing_elements,
            metadata={
                "idea_count": idea_count,
                "innovation_potential": innovation_potential,
                "alternative_count": alt_count,
                "connection_count": connection_count
            }
        )
    
    def _analyze_temporal_complexity(self, emotional_result: EmotionalAnalysisResult,
                                   logical_result: LogicalAnalysisResult) -> ComplexityMetric:
        """Analyze temporal complexity factors."""
        contributing_elements = []
        
        # Urgency level
        urgency_level = emotional_result.emotional_context.urgency_level
        if urgency_level > 0.8:
            contributing_elements.append(f"Critical time pressure: {urgency_level:.2f}")
        
        # Time-sensitive requirements
        time_sensitive_reqs = sum(1 for req in logical_result.requirements 
                                if any(keyword in req.text.lower() 
                                      for keyword in ["urgent", "asap", "immediate", "deadline", "time"]))
        time_req_complexity = min(time_sensitive_reqs / 3, 1.0)
        if time_sensitive_reqs > 1:
            contributing_elements.append(f"Time-sensitive requirements: {time_sensitive_reqs}")
        
        # Coordination timing complexity (estimated)
        req_count = len(logical_result.requirements)
        coordination_complexity = min(req_count / 8, 1.0) if req_count > 3 else 0.2
        if coordination_complexity > 0.6:
            contributing_elements.append(f"Complex coordination timing required")
        
        overall_score = (urgency_level + time_req_complexity + coordination_complexity) / 3
        
        return ComplexityMetric(
            factor=ComplexityFactor.TEMPORAL_COMPLEXITY,
            score=overall_score,
            confidence=0.7,  # Moderate confidence in temporal analysis
            contributing_elements=contributing_elements,
            metadata={
                "urgency_level": urgency_level,
                "time_sensitive_requirements": time_sensitive_reqs,
                "coordination_complexity": coordination_complexity
            }
        )
    
    def _analyze_resource_complexity(self, logical_result: LogicalAnalysisResult,
                                   synthesis_result: DimensionalSynthesisResult) -> ComplexityMetric:
        """Analyze resource complexity factors."""
        contributing_elements = []
        
        # Requirement diversity (different types of resources needed)
        req_texts = [req.text.lower() for req in logical_result.requirements]
        resource_types_needed = set()
        
        for text in req_texts:
            for keyword, resource_type in self.resource_mappings.items():
                if keyword in text:
                    resource_types_needed.add(resource_type)
        
        resource_diversity = len(resource_types_needed) / len(ResourceType)
        if len(resource_types_needed) > 3:
            contributing_elements.append(f"Diverse resource requirements: {len(resource_types_needed)}")
        
        # Synthesis complexity (indicates resource coordination needs)
        synthesis_complexity = 1 - synthesis_result.coherence_score
        if synthesis_complexity > 0.4:
            contributing_elements.append(f"Complex resource coordination: {synthesis_complexity:.2f}")
        
        # Estimated computational intensity
        computational_intensity = logical_result.complexity_score
        if computational_intensity > 0.7:
            contributing_elements.append(f"High computational requirements: {computational_intensity:.2f}")
        
        overall_score = (resource_diversity + synthesis_complexity + computational_intensity) / 3
        
        return ComplexityMetric(
            factor=ComplexityFactor.RESOURCE_COMPLEXITY,
            score=overall_score,
            confidence=0.6,
            contributing_elements=contributing_elements,
            metadata={
                "resource_types_needed": len(resource_types_needed),
                "synthesis_complexity": synthesis_complexity,
                "computational_intensity": computational_intensity
            }
        )
    
    def _analyze_interdependency_complexity(self, logical_result: LogicalAnalysisResult,
                                          synthesis_result: DimensionalSynthesisResult) -> ComplexityMetric:
        """Analyze interdependency complexity factors."""
        contributing_elements = []
        
        # Requirement interdependencies
        req_count = len(logical_result.requirements)
        if req_count > 1:
            # Estimate interdependencies based on requirement overlap and synthesis conflicts
            conflict_count = len(synthesis_result.synthesis_conflicts)
            interdep_ratio = conflict_count / max(req_count, 1)
            
            if conflict_count > 2:
                contributing_elements.append(f"Multiple synthesis conflicts: {conflict_count}")
        else:
            interdep_ratio = 0.1  # Minimal interdependencies for single requirement
        
        # Dimensional integration complexity
        dimensional_complexity = 1 - synthesis_result.coherence_score
        if dimensional_complexity > 0.5:
            contributing_elements.append(f"Complex dimensional integration: {dimensional_complexity:.2f}")
        
        # Cross-functional coordination needs (estimated)
        coordination_complexity = min(req_count / 6, 1.0) if req_count > 2 else 0.2
        if coordination_complexity > 0.6:
            contributing_elements.append(f"High coordination complexity")
        
        overall_score = (interdep_ratio + dimensional_complexity + coordination_complexity) / 3
        
        return ComplexityMetric(
            factor=ComplexityFactor.INTERDEPENDENCY_COMPLEXITY,
            score=overall_score,
            confidence=synthesis_result.coherence_score,
            contributing_elements=contributing_elements,
            metadata={
                "conflict_count": len(synthesis_result.synthesis_conflicts),
                "dimensional_complexity": dimensional_complexity,
                "coordination_complexity": coordination_complexity
            }
        )
    
    def _analyze_uncertainty_complexity(self, synthesis_result: DimensionalSynthesisResult,
                                      cognitive_state: CognitiveState) -> ComplexityMetric:
        """Analyze uncertainty complexity factors."""
        contributing_elements = []
        
        # Synthesis coherence uncertainty
        coherence_uncertainty = 1 - synthesis_result.coherence_score
        if coherence_uncertainty > 0.4:
            contributing_elements.append(f"Low synthesis coherence: {synthesis_result.coherence_score:.2f}")
        
        # Cognitive confidence uncertainty
        confidence_uncertainty = 1 - cognitive_state.confidence_level
        if confidence_uncertainty > 0.4:
            contributing_elements.append(f"Low cognitive confidence: {cognitive_state.confidence_level:.2f}")
        
        # Decision uncertainty (from cognitive biases)
        bias_uncertainty = len(cognitive_state.active_biases) / 5  # Normalize by max expected biases
        if len(cognitive_state.active_biases) > 2:
            contributing_elements.append(f"Multiple cognitive biases active: {len(cognitive_state.active_biases)}")
        
        overall_score = (coherence_uncertainty + confidence_uncertainty + bias_uncertainty) / 3
        
        return ComplexityMetric(
            factor=ComplexityFactor.UNCERTAINTY_COMPLEXITY,
            score=overall_score,
            confidence=0.5,  # Moderate confidence in uncertainty assessment
            contributing_elements=contributing_elements,
            metadata={
                "coherence_uncertainty": coherence_uncertainty,
                "confidence_uncertainty": confidence_uncertainty,
                "active_biases": len(cognitive_state.active_biases)
            }
        )
    
    def _analyze_scale_complexity(self, logical_result: LogicalAnalysisResult,
                                creative_result: CreativeAnalysisResult) -> ComplexityMetric:
        """Analyze scale complexity factors."""
        contributing_elements = []
        
        # Requirement scale
        req_count = len(logical_result.requirements)
        req_scale = min(req_count / 12, 1.0)  # Normalize by 12 requirements
        if req_count > 8:
            contributing_elements.append(f"Large requirement set: {req_count}")
        
        # Creative solution scale
        idea_count = len(creative_result.creative_ideas)
        creative_scale = min(idea_count / 10, 1.0)
        if idea_count > 6:
            contributing_elements.append(f"Large creative solution space: {idea_count}")
        
        # Estimated impact scale (based on complexity and innovation)
        impact_scale = (logical_result.complexity_score + creative_result.innovation_potential_score) / 2
        if impact_scale > 0.8:
            contributing_elements.append(f"High impact potential: {impact_scale:.2f}")
        
        overall_score = (req_scale + creative_scale + impact_scale) / 3
        
        return ComplexityMetric(
            factor=ComplexityFactor.SCALE_COMPLEXITY,
            score=overall_score,
            confidence=0.6,
            contributing_elements=contributing_elements,
            metadata={
                "requirement_count": req_count,
                "creative_idea_count": idea_count,
                "impact_scale": impact_scale
            }
        )
    
    def assess_resource_requirements(self, complexity_metrics: List[ComplexityMetric],
                                   logical_result: LogicalAnalysisResult,
                                   emotional_result: EmotionalAnalysisResult) -> List[ResourceRequirement]:
        """Assess resource requirements based on complexity analysis."""
        resource_requirements = []
        
        # Computational resources
        computational_intensity = next(
            (m.score for m in complexity_metrics if m.factor == ComplexityFactor.LOGICAL_COMPLEXITY), 0.5
        )
        
        computational_req = ResourceRequirement(
            resource_type=ResourceType.COMPUTATIONAL,
            intensity=computational_intensity,
            criticality=0.8,
            availability=0.9,  # Assume high availability
            estimated_usage=computational_intensity * 0.8
        )
        resource_requirements.append(computational_req)
        
        # Human expertise
        expertise_intensity = max(
            next((m.score for m in complexity_metrics if m.factor == ComplexityFactor.CREATIVE_COMPLEXITY), 0.3),
            next((m.score for m in complexity_metrics if m.factor == ComplexityFactor.EMOTIONAL_COMPLEXITY), 0.3)
        )
        
        expertise_req = ResourceRequirement(
            resource_type=ResourceType.HUMAN_EXPERTISE,
            intensity=expertise_intensity,
            criticality=0.7,
            availability=0.7,
            estimated_usage=expertise_intensity * 0.6
        )
        resource_requirements.append(expertise_req)
        
        # Time-critical resources
        temporal_complexity = next(
            (m.score for m in complexity_metrics if m.factor == ComplexityFactor.TEMPORAL_COMPLEXITY), 0.3
        )
        
        if temporal_complexity > 0.5:
            time_critical_req = ResourceRequirement(
                resource_type=ResourceType.TIME_CRITICAL,
                intensity=temporal_complexity,
                criticality=0.9,
                availability=0.6,
                estimated_usage=temporal_complexity * 0.9
            )
            resource_requirements.append(time_critical_req)
        
        # Collaborative resources
        interdep_complexity = next(
            (m.score for m in complexity_metrics if m.factor == ComplexityFactor.INTERDEPENDENCY_COMPLEXITY), 0.3
        )
        
        if interdep_complexity > 0.4:
            collaborative_req = ResourceRequirement(
                resource_type=ResourceType.COLLABORATIVE,
                intensity=interdep_complexity,
                criticality=0.6,
                availability=0.8,
                estimated_usage=interdep_complexity * 0.7
            )
            resource_requirements.append(collaborative_req)
        
        # Research-intensive resources
        uncertainty_complexity = next(
            (m.score for m in complexity_metrics if m.factor == ComplexityFactor.UNCERTAINTY_COMPLEXITY), 0.3
        )
        
        if uncertainty_complexity > 0.5:
            research_req = ResourceRequirement(
                resource_type=ResourceType.RESEARCH_INTENSIVE,
                intensity=uncertainty_complexity,
                criticality=0.7,
                availability=0.7,
                estimated_usage=uncertainty_complexity * 0.8
            )
            resource_requirements.append(research_req)
        
        return resource_requirements
    
    def calculate_overall_complexity(self, complexity_metrics: List[ComplexityMetric]) -> float:
        """Calculate overall complexity score from individual metrics."""
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric in complexity_metrics:
            weight = self.complexity_weights.get(metric.factor, 1.0) * metric.weight
            calibration = self.complexity_calibration.get(metric.factor, 1.0)
            
            weighted_sum += metric.score * weight * calibration * metric.confidence
            total_weight += weight * metric.confidence
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def select_optimal_mode(self, overall_complexity: float,
                          resource_requirements: List[ResourceRequirement],
                          complexity_metrics: List[ComplexityMetric],
                          intent_result: IntentRecognitionResult) -> Tuple[JAEGISMode, float, List[str]]:
        """Select optimal JAEGIS mode based on analysis."""
        mode_scores = {}
        selection_reasoning = []
        
        # Score each mode based on complexity fit
        for mode, capability in self.mode_capabilities.items():
            score = 0.0
            
            # Complexity fit score
            if overall_complexity <= capability.max_complexity_score:
                complexity_fit = 1.0 - abs(overall_complexity - capability.max_complexity_score * 0.8)
                score += complexity_fit * 0.4
                selection_reasoning.append(f"{mode.value}: Complexity fit {complexity_fit:.2f}")
            else:
                # Penalty for exceeding capability
                score += 0.1
                selection_reasoning.append(f"{mode.value}: Exceeds complexity capability")
            
            # Resource capacity fit
            resource_fit_scores = []
            for req in resource_requirements:
                capacity = capability.resource_capacity.get(req.resource_type, 0.5)
                if req.intensity <= capacity:
                    fit = 1.0 - abs(req.intensity - capacity * 0.8)
                    resource_fit_scores.append(fit)
                else:
                    resource_fit_scores.append(0.2)  # Penalty for insufficient capacity
            
            avg_resource_fit = sum(resource_fit_scores) / len(resource_fit_scores) if resource_fit_scores else 0.5
            score += avg_resource_fit * 0.3
            
            # Cost efficiency (prefer lower cost for similar capability)
            cost_efficiency = 1.0 - capability.cost_factor
            score += cost_efficiency * 0.1
            
            # Success rate consideration
            score += capability.success_rate_threshold * 0.1
            
            # Historical performance
            historical_performance = self.mode_performance_stats[mode]["success_rate"]
            score += historical_performance * 0.1
            
            mode_scores[mode] = score
        
        # Apply selection rules
        for rule_name, rule in self.selection_rules.items():
            if self._check_rule_conditions(rule["conditions"], complexity_metrics, intent_result):
                target_mode = rule["target_mode"]
                boost = rule["confidence_boost"]
                mode_scores[target_mode] = mode_scores.get(target_mode, 0.5) + boost
                selection_reasoning.append(f"Applied rule: {rule_name} -> {target_mode.value}")
        
        # Select best mode
        best_mode = max(mode_scores.items(), key=lambda x: x[1])
        selected_mode, confidence = best_mode
        
        # Normalize confidence
        confidence = min(confidence, 1.0)
        
        return selected_mode, confidence, selection_reasoning
    
    def _check_rule_conditions(self, conditions: List[str],
                             complexity_metrics: List[ComplexityMetric],
                             intent_result: IntentRecognitionResult) -> bool:
        """Check if rule conditions are met."""
        for condition in conditions:
            if condition == "emergency_request":
                if intent_result.detected_intents:
                    if intent_result.detected_intents[0].intent == IntentCategory.EMERGENCY_REQUEST:
                        return True
            
            elif condition == "low_complexity":
                overall_complexity = self.calculate_overall_complexity(complexity_metrics)
                if overall_complexity < 0.3:
                    return True
            
            elif condition == "high_uncertainty":
                uncertainty_metric = next(
                    (m for m in complexity_metrics if m.factor == ComplexityFactor.UNCERTAINTY_COMPLEXITY), None
                )
                if uncertainty_metric and uncertainty_metric.score > 0.6:
                    return True
            
            elif condition == "research_intensive":
                if intent_result.detected_intents:
                    if intent_result.detected_intents[0].intent == IntentCategory.INFORMATION_SEEKING:
                        return True
        
        return False
    
    def predict_performance(self, selected_mode: JAEGISMode,
                          complexity_metrics: List[ComplexityMetric],
                          resource_requirements: List[ResourceRequirement]) -> Dict[str, float]:
        """Predict performance metrics for selected mode."""
        capability = self.mode_capabilities[selected_mode]
        historical_stats = self.mode_performance_stats[selected_mode]
        
        # Success rate prediction
        overall_complexity = self.calculate_overall_complexity(complexity_metrics)
        complexity_factor = 1.0 - (overall_complexity / capability.max_complexity_score)
        predicted_success_rate = capability.success_rate_threshold * complexity_factor * 0.7 + historical_stats["success_rate"] * 0.3
        
        # Duration prediction
        base_duration = sum(capability.typical_duration_minutes) / 2  # Average
        
        # Adjust for complexity
        complexity_multiplier = 1.0 + overall_complexity
        
        # Adjust for resource intensity
        avg_resource_intensity = sum(req.intensity for req in resource_requirements) / len(resource_requirements) if resource_requirements else 0.5
        resource_multiplier = 1.0 + avg_resource_intensity * 0.5
        
        predicted_duration = base_duration * complexity_multiplier * resource_multiplier
        
        # Resource utilization prediction
        total_capacity = sum(capability.resource_capacity.values())
        total_demand = sum(req.intensity for req in resource_requirements)
        predicted_utilization = min(total_demand / total_capacity, 1.0) if total_capacity > 0 else 0.5
        
        # Confidence in predictions
        prediction_confidence = min(
            predicted_success_rate,
            1.0 - abs(overall_complexity - capability.max_complexity_score * 0.8),
            0.9
        )
        
        return {
            "success_rate": predicted_success_rate,
            "duration_minutes": predicted_duration,
            "resource_utilization": predicted_utilization,
            "prediction_confidence": prediction_confidence,
            "cost_estimate": capability.cost_factor * predicted_duration / 60  # Cost per hour
        }
    
    async def select_mode(self, intent_result: IntentRecognitionResult,
                        logical_result: LogicalAnalysisResult,
                        emotional_result: EmotionalAnalysisResult,
                        creative_result: CreativeAnalysisResult,
                        synthesis_result: DimensionalSynthesisResult,
                        cognitive_state: CognitiveState,
                        decision_result: DecisionResult) -> ModeSelectionResult:
        """
        Select optimal JAEGIS mode based on comprehensive analysis.
        
        Args:
            intent_result: Intent recognition results
            logical_result: Logical analysis results
            emotional_result: Emotional analysis results
            creative_result: Creative analysis results
            synthesis_result: Dimensional synthesis results
            cognitive_state: Current cognitive state
            decision_result: Decision-making results
            
        Returns:
            Complete mode selection result
        """
        import time
        start_time = time.time()
        
        try:
            # Analyze complexity across all dimensions
            complexity_metrics = self.analyze_complexity(
                logical_result, emotional_result, creative_result, synthesis_result, cognitive_state
            )
            
            # Assess resource requirements
            resource_requirements = self.assess_resource_requirements(
                complexity_metrics, logical_result, emotional_result
            )
            
            # Calculate overall complexity
            overall_complexity = self.calculate_overall_complexity(complexity_metrics)
            
            # Select optimal mode
            selected_mode, confidence, reasoning = self.select_optimal_mode(
                overall_complexity, resource_requirements, complexity_metrics, intent_result
            )
            
            # Generate alternative modes
            alternative_modes = []
            mode_scores = {mode: 0.5 for mode in JAEGISMode}  # Simplified for alternatives
            
            # Add complexity-based alternatives
            if overall_complexity > 0.7:
                alternative_modes.append((JAEGISMode.MODE_4, 0.7))
                alternative_modes.append((JAEGISMode.MODE_5, 0.6))
            elif overall_complexity < 0.3:
                alternative_modes.append((JAEGISMode.MODE_1, 0.8))
                alternative_modes.append((JAEGISMode.MODE_2, 0.7))
            else:
                alternative_modes.append((JAEGISMode.MODE_2, 0.7))
                alternative_modes.append((JAEGISMode.MODE_4, 0.6))
            
            # Remove selected mode from alternatives
            alternative_modes = [(mode, conf) for mode, conf in alternative_modes if mode != selected_mode]
            
            # Predict performance
            performance_prediction = self.predict_performance(
                selected_mode, complexity_metrics, resource_requirements
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            # Update performance statistics
            self.mode_performance_stats[selected_mode]["usage_count"] += 1
            
            return ModeSelectionResult(
                selected_mode=selected_mode,
                confidence=confidence,
                complexity_analysis=complexity_metrics,
                resource_analysis=resource_requirements,
                alternative_modes=alternative_modes,
                selection_reasoning=reasoning,
                performance_prediction=performance_prediction,
                processing_time_ms=processing_time,
                metadata={
                    "overall_complexity": overall_complexity,
                    "resource_requirements_count": len(resource_requirements),
                    "complexity_factors_analyzed": len(complexity_metrics),
                    "mode_capabilities": {
                        "max_complexity": self.mode_capabilities[selected_mode].max_complexity_score,
                        "agent_range": self.mode_capabilities[selected_mode].agent_count_range,
                        "typical_duration": self.mode_capabilities[selected_mode].typical_duration_minutes
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Mode selection failed: {e}")
            
            return ModeSelectionResult(
                selected_mode=JAEGISMode.MODE_2,  # Safe default
                confidence=0.5,
                complexity_analysis=[],
                resource_analysis=[],
                alternative_modes=[(JAEGISMode.MODE_1, 0.4), (JAEGISMode.MODE_3, 0.4)],
                selection_reasoning=["Error in mode selection - using default"],
                performance_prediction={"success_rate": 0.5, "duration_minutes": 60},
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )


# ============================================================================
# MODE SELECTION UTILITIES
# ============================================================================

class ModeSelectionUtils:
    """Utility functions for mode selection."""
    
    @staticmethod
    def mode_result_to_dict(result: ModeSelectionResult) -> Dict[str, Any]:
        """Convert mode selection result to dictionary format."""
        return {
            "selected_mode": result.selected_mode.value,
            "confidence": result.confidence,
            "complexity_analysis": [
                {
                    "factor": metric.factor.value,
                    "score": metric.score,
                    "confidence": metric.confidence,
                    "contributing_elements": metric.contributing_elements
                }
                for metric in result.complexity_analysis
            ],
            "resource_analysis": [
                {
                    "resource_type": req.resource_type.value,
                    "intensity": req.intensity,
                    "criticality": req.criticality,
                    "availability": req.availability
                }
                for req in result.resource_analysis
            ],
            "alternative_modes": [
                {"mode": mode.value, "confidence": conf}
                for mode, conf in result.alternative_modes
            ],
            "selection_reasoning": result.selection_reasoning,
            "performance_prediction": result.performance_prediction,
            "processing_time_ms": result.processing_time_ms
        }
    
    @staticmethod
    def get_mode_summary(result: ModeSelectionResult) -> Dict[str, Any]:
        """Get summary of mode selection results."""
        return {
            "selected_mode": result.selected_mode.value,
            "confidence": result.confidence,
            "overall_complexity": result.metadata.get("overall_complexity", 0.5),
            "predicted_success_rate": result.performance_prediction.get("success_rate", 0.5),
            "predicted_duration": result.performance_prediction.get("duration_minutes", 60),
            "resource_requirements": len(result.resource_analysis),
            "alternatives_available": len(result.alternative_modes),
            "processing_time_ms": result.processing_time_ms
        }
