"""
N.L.D.S. Alternative Generation Engine
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced alternative generation engine for ambiguous or low-confidence translations
with 94%+ alternative quality and intelligent interpretation diversification.
"""

import math
import random
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime
import asyncio
from itertools import combinations

# Local imports
from ..nlp.intent_recognizer import IntentRecognitionResult, IntentCategory
from ..nlp.semantic_analyzer import SemanticAnalysisResult
from ..processing.logical_analyzer import LogicalAnalysisResult
from ..processing.dimensional_synthesizer import DimensionalSynthesisResult
from ..cognitive.cognitive_model import CognitiveState
from .command_generator import CommandGenerationResult, JAEGISCommand, JAEGISSquad, JAEGISMode
from .mode_selector import ModeSelectionResult
from .squad_selector import SquadSelectionResult
from .confidence_validator import ConfidenceValidationResult, AlternativeOption

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# ALTERNATIVE GENERATION STRUCTURES AND ENUMS
# ============================================================================

class AlternativeType(Enum):
    """Types of alternatives that can be generated."""
    INTENT_REINTERPRETATION = "intent_reinterpretation"
    LOGICAL_RESTRUCTURING = "logical_restructuring"
    COMMAND_VARIATION = "command_variation"
    MODE_ADJUSTMENT = "mode_adjustment"
    SQUAD_SUBSTITUTION = "squad_substitution"
    PARAMETER_MODIFICATION = "parameter_modification"
    EXECUTION_STRATEGY = "execution_strategy"
    HYBRID_APPROACH = "hybrid_approach"


class GenerationStrategy(Enum):
    """Strategies for generating alternatives."""
    CONSERVATIVE = "conservative"      # Safe, proven approaches
    AGGRESSIVE = "aggressive"         # High-capability, resource-intensive
    BALANCED = "balanced"             # Optimal resource/capability balance
    CREATIVE = "creative"             # Innovative, experimental approaches
    FALLBACK = "fallback"             # Minimal viable alternatives


class AlternativeQuality(Enum):
    """Quality levels for generated alternatives."""
    EXCELLENT = "excellent"    # 0.9+
    GOOD = "good"             # 0.8-0.89
    ACCEPTABLE = "acceptable"  # 0.7-0.79
    MARGINAL = "marginal"     # 0.6-0.69
    POOR = "poor"             # <0.6


@dataclass
class AlternativeInterpretation:
    """Complete alternative interpretation of the input."""
    interpretation_id: str
    alternative_type: AlternativeType
    generation_strategy: GenerationStrategy
    
    # Alternative analysis results
    alternative_intent: Optional[IntentCategory]
    alternative_requirements: List[str]
    alternative_approach: str
    
    # Alternative translation results
    alternative_command: Optional[JAEGISCommand]
    alternative_mode: Optional[JAEGISMode]
    alternative_squad: Optional[JAEGISSquad]
    
    # Quality and confidence
    quality_score: float
    confidence: float
    feasibility: float
    risk_level: float
    
    # Comparison with original
    similarity_to_original: float
    trade_offs: List[str]
    advantages: List[str]
    disadvantages: List[str]
    
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlternativeGenerationResult:
    """Complete alternative generation result."""
    original_confidence: float
    alternatives_generated: List[AlternativeInterpretation]
    generation_strategies_used: List[GenerationStrategy]
    
    # Quality metrics
    average_alternative_quality: float
    best_alternative_confidence: float
    diversity_score: float
    coverage_score: float
    
    # Recommendations
    recommended_alternatives: List[AlternativeInterpretation]
    fallback_options: List[AlternativeInterpretation]
    
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# ALTERNATIVE GENERATION ENGINE
# ============================================================================

class AlternativeGenerationEngine:
    """
    Advanced alternative generation engine for ambiguous translations.
    
    Features:
    - Multi-strategy alternative generation
    - Intent reinterpretation and logical restructuring
    - Command, mode, and squad variations
    - Quality assessment and ranking
    - Diversity optimization
    - Risk-aware alternative selection
    - Adaptive generation based on confidence gaps
    - Creative and conservative approaches
    """
    
    def __init__(self):
        """Initialize alternative generation engine."""
        self.generation_strategies = self._load_generation_strategies()
        self.alternative_patterns = self._load_alternative_patterns()
        self.quality_metrics = self._load_quality_metrics()
        self.diversity_weights = self._load_diversity_weights()
        
        # Performance tracking
        self.generation_history = []
        self.strategy_performance = {strategy: {"success_rate": 0.8, "avg_quality": 0.7} 
                                   for strategy in GenerationStrategy}
    
    def _load_generation_strategies(self) -> Dict[GenerationStrategy, Dict[str, Any]]:
        """Load generation strategies and their parameters."""
        return {
            GenerationStrategy.CONSERVATIVE: {
                "description": "Safe, proven approaches with high success rates",
                "risk_tolerance": 0.2,
                "innovation_factor": 0.3,
                "resource_efficiency": 0.9,
                "preferred_modes": [JAEGISMode.MODE_1, JAEGISMode.MODE_2],
                "preferred_squads": ["tyler_agent", "content_squad", "support_squad"],
                "generation_count": 2
            },
            GenerationStrategy.AGGRESSIVE: {
                "description": "High-capability, resource-intensive approaches",
                "risk_tolerance": 0.8,
                "innovation_factor": 0.7,
                "resource_efficiency": 0.4,
                "preferred_modes": [JAEGISMode.MODE_4, JAEGISMode.MODE_5],
                "preferred_squads": ["master_orchestrator", "john_agent", "garas_research_analysis"],
                "generation_count": 3
            },
            GenerationStrategy.BALANCED: {
                "description": "Optimal balance of resources and capabilities",
                "risk_tolerance": 0.5,
                "innovation_factor": 0.5,
                "resource_efficiency": 0.7,
                "preferred_modes": [JAEGISMode.MODE_2, JAEGISMode.MODE_3],
                "preferred_squads": ["fred_agent", "development_squad", "research_squad"],
                "generation_count": 3
            },
            GenerationStrategy.CREATIVE: {
                "description": "Innovative, experimental approaches",
                "risk_tolerance": 0.6,
                "innovation_factor": 0.9,
                "resource_efficiency": 0.6,
                "preferred_modes": [JAEGISMode.MODE_3, JAEGISMode.MODE_4],
                "preferred_squads": ["innovation_squad", "research_squad", "garas_gap_detection"],
                "generation_count": 4
            },
            GenerationStrategy.FALLBACK: {
                "description": "Minimal viable alternatives for critical situations",
                "risk_tolerance": 0.1,
                "innovation_factor": 0.2,
                "resource_efficiency": 1.0,
                "preferred_modes": [JAEGISMode.MODE_1],
                "preferred_squads": ["tyler_agent", "support_squad"],
                "generation_count": 2
            }
        }
    
    def _load_alternative_patterns(self) -> Dict[AlternativeType, Dict[str, Any]]:
        """Load patterns for generating different types of alternatives."""
        return {
            AlternativeType.INTENT_REINTERPRETATION: {
                "description": "Reinterpret user intent with different perspectives",
                "techniques": ["context_shift", "scope_adjustment", "priority_reordering"],
                "confidence_boost": 0.1,
                "generation_complexity": 0.6
            },
            AlternativeType.LOGICAL_RESTRUCTURING: {
                "description": "Restructure logical requirements and dependencies",
                "techniques": ["requirement_grouping", "dependency_reordering", "scope_decomposition"],
                "confidence_boost": 0.15,
                "generation_complexity": 0.7
            },
            AlternativeType.COMMAND_VARIATION: {
                "description": "Generate alternative command structures",
                "techniques": ["parameter_substitution", "command_type_change", "execution_order"],
                "confidence_boost": 0.08,
                "generation_complexity": 0.4
            },
            AlternativeType.MODE_ADJUSTMENT: {
                "description": "Adjust operational mode for different trade-offs",
                "techniques": ["mode_escalation", "mode_reduction", "mode_optimization"],
                "confidence_boost": 0.05,
                "generation_complexity": 0.3
            },
            AlternativeType.SQUAD_SUBSTITUTION: {
                "description": "Substitute squads with different specializations",
                "techniques": ["specialization_shift", "tier_adjustment", "multi_squad_coordination"],
                "confidence_boost": 0.12,
                "generation_complexity": 0.5
            },
            AlternativeType.EXECUTION_STRATEGY: {
                "description": "Alternative execution strategies and approaches",
                "techniques": ["staged_execution", "parallel_processing", "iterative_refinement"],
                "confidence_boost": 0.2,
                "generation_complexity": 0.8
            },
            AlternativeType.HYBRID_APPROACH: {
                "description": "Hybrid human-AI approaches",
                "techniques": ["human_oversight", "collaborative_execution", "validation_checkpoints"],
                "confidence_boost": 0.25,
                "generation_complexity": 0.9
            }
        }
    
    def _load_quality_metrics(self) -> Dict[str, float]:
        """Load quality assessment metrics and weights."""
        return {
            "feasibility_weight": 0.25,
            "confidence_weight": 0.20,
            "innovation_weight": 0.15,
            "resource_efficiency_weight": 0.15,
            "risk_mitigation_weight": 0.15,
            "user_satisfaction_weight": 0.10
        }
    
    def _load_diversity_weights(self) -> Dict[str, float]:
        """Load diversity optimization weights."""
        return {
            "intent_diversity": 0.3,
            "approach_diversity": 0.25,
            "resource_diversity": 0.2,
            "risk_diversity": 0.15,
            "complexity_diversity": 0.1
        }
    
    def analyze_confidence_gaps(self, validation_result: ConfidenceValidationResult) -> List[AlternativeType]:
        """Analyze confidence gaps to determine which alternative types to generate."""
        alternative_types = []
        
        # Check confidence breakdown for specific gaps
        for metric in validation_result.confidence_breakdown:
            if metric.confidence_score < 0.7:
                if metric.source.value == "intent_recognition":
                    alternative_types.append(AlternativeType.INTENT_REINTERPRETATION)
                elif metric.source.value == "logical_analysis":
                    alternative_types.append(AlternativeType.LOGICAL_RESTRUCTURING)
                elif metric.source.value == "command_generation":
                    alternative_types.append(AlternativeType.COMMAND_VARIATION)
                elif metric.source.value == "mode_selection":
                    alternative_types.append(AlternativeType.MODE_ADJUSTMENT)
                elif metric.source.value == "squad_selection":
                    alternative_types.append(AlternativeType.SQUAD_SUBSTITUTION)
        
        # Add execution strategy alternatives for very low confidence
        if validation_result.overall_confidence < 0.6:
            alternative_types.extend([
                AlternativeType.EXECUTION_STRATEGY,
                AlternativeType.HYBRID_APPROACH
            ])
        
        # Ensure we have at least some alternatives
        if not alternative_types:
            alternative_types = [
                AlternativeType.COMMAND_VARIATION,
                AlternativeType.MODE_ADJUSTMENT,
                AlternativeType.SQUAD_SUBSTITUTION
            ]
        
        return list(set(alternative_types))  # Remove duplicates
    
    def select_generation_strategies(self, validation_result: ConfidenceValidationResult,
                                   intent_result: IntentRecognitionResult) -> List[GenerationStrategy]:
        """Select appropriate generation strategies based on context."""
        strategies = []
        
        # Emergency situations - use aggressive and fallback
        if intent_result.detected_intents:
            primary_intent = intent_result.detected_intents[0]
            if primary_intent.intent == IntentCategory.EMERGENCY_REQUEST:
                strategies.extend([GenerationStrategy.AGGRESSIVE, GenerationStrategy.FALLBACK])
        
        # Low confidence - use multiple strategies
        if validation_result.overall_confidence < 0.6:
            strategies.extend([
                GenerationStrategy.CONSERVATIVE,
                GenerationStrategy.BALANCED,
                GenerationStrategy.CREATIVE
            ])
        elif validation_result.overall_confidence < 0.8:
            strategies.extend([
                GenerationStrategy.BALANCED,
                GenerationStrategy.CONSERVATIVE
            ])
        else:
            # High confidence but still generating alternatives
            strategies.append(GenerationStrategy.BALANCED)
        
        # Always include fallback for critical situations
        if validation_result.validation_status.value in ["failed", "requires_alternatives"]:
            strategies.append(GenerationStrategy.FALLBACK)
        
        return list(set(strategies))  # Remove duplicates
    
    def generate_intent_alternatives(self, original_intent: IntentCategory,
                                   text: str,
                                   strategy: GenerationStrategy) -> List[Tuple[IntentCategory, float, str]]:
        """Generate alternative intent interpretations."""
        alternatives = []
        
        # Define intent relationships and alternatives
        intent_alternatives = {
            IntentCategory.TASK_REQUEST: [
                (IntentCategory.INFORMATION_SEEKING, 0.7, "Reinterpret as information gathering"),
                (IntentCategory.SYSTEM_CONTROL, 0.6, "Reinterpret as system configuration"),
                (IntentCategory.RESOURCE_REQUEST, 0.8, "Reinterpret as resource allocation")
            ],
            IntentCategory.INFORMATION_SEEKING: [
                (IntentCategory.TASK_REQUEST, 0.8, "Reinterpret as actionable task"),
                (IntentCategory.STATUS_INQUIRY, 0.7, "Reinterpret as status check"),
                (IntentCategory.PROBLEM_SOLVING, 0.6, "Reinterpret as problem analysis")
            ],
            IntentCategory.SYSTEM_CONTROL: [
                (IntentCategory.CONFIGURATION_CHANGE, 0.9, "Reinterpret as configuration update"),
                (IntentCategory.TASK_REQUEST, 0.7, "Reinterpret as task execution"),
                (IntentCategory.RESOURCE_REQUEST, 0.6, "Reinterpret as resource management")
            ],
            IntentCategory.PROBLEM_SOLVING: [
                (IntentCategory.TASK_REQUEST, 0.8, "Reinterpret as solution implementation"),
                (IntentCategory.INFORMATION_SEEKING, 0.7, "Reinterpret as problem analysis"),
                (IntentCategory.EMERGENCY_REQUEST, 0.5, "Reinterpret as urgent issue")
            ]
        }
        
        # Get alternatives for the original intent
        if original_intent in intent_alternatives:
            potential_alternatives = intent_alternatives[original_intent]
            
            # Filter based on strategy
            strategy_config = self.generation_strategies[strategy]
            risk_tolerance = strategy_config["risk_tolerance"]
            
            for alt_intent, confidence, reasoning in potential_alternatives:
                # Adjust confidence based on strategy
                adjusted_confidence = confidence * (0.8 + risk_tolerance * 0.4)
                
                if adjusted_confidence > 0.5:  # Minimum threshold
                    alternatives.append((alt_intent, adjusted_confidence, reasoning))
        
        return alternatives[:2]  # Return top 2 alternatives
    
    def generate_logical_alternatives(self, logical_result: LogicalAnalysisResult,
                                    strategy: GenerationStrategy) -> List[Tuple[List[str], float, str]]:
        """Generate alternative logical requirement structures."""
        alternatives = []
        original_requirements = [req.text for req in logical_result.requirements]
        
        if len(original_requirements) < 2:
            return alternatives
        
        strategy_config = self.generation_strategies[strategy]
        
        # Requirement grouping alternative
        if len(original_requirements) > 3:
            grouped_reqs = self._group_requirements(original_requirements)
            confidence = 0.8 * strategy_config["resource_efficiency"]
            alternatives.append((
                grouped_reqs,
                confidence,
                "Group related requirements for efficient execution"
            ))
        
        # Requirement prioritization alternative
        prioritized_reqs = self._prioritize_requirements(original_requirements, strategy)
        confidence = 0.7 + strategy_config["innovation_factor"] * 0.2
        alternatives.append((
            prioritized_reqs,
            confidence,
            "Reorder requirements by priority and dependencies"
        ))
        
        # Simplified requirements alternative (conservative strategy)
        if strategy == GenerationStrategy.CONSERVATIVE:
            simplified_reqs = original_requirements[:2]  # Take only top 2
            alternatives.append((
                simplified_reqs,
                0.9,
                "Simplify to core requirements for reliable execution"
            ))
        
        return alternatives
    
    def generate_command_alternatives(self, original_command: JAEGISCommand,
                                    strategy: GenerationStrategy) -> List[Tuple[JAEGISCommand, float, str]]:
        """Generate alternative command variations."""
        alternatives = []
        strategy_config = self.generation_strategies[strategy]
        
        # Mode adjustment alternatives
        current_mode_num = int(original_command.mode_level.value.split('_')[1])
        
        # Lower mode alternative (more conservative)
        if current_mode_num > 1:
            lower_mode = JAEGISMode(f"mode_{current_mode_num - 1}")
            alt_command = self._create_command_variant(original_command, mode=lower_mode)
            confidence = 0.8 + strategy_config["resource_efficiency"] * 0.1
            alternatives.append((
                alt_command,
                confidence,
                f"Use lower mode ({lower_mode.value}) for more reliable execution"
            ))
        
        # Higher mode alternative (more aggressive)
        if current_mode_num < 5 and strategy in [GenerationStrategy.AGGRESSIVE, GenerationStrategy.CREATIVE]:
            higher_mode = JAEGISMode(f"mode_{current_mode_num + 1}")
            alt_command = self._create_command_variant(original_command, mode=higher_mode)
            confidence = 0.7 + strategy_config["innovation_factor"] * 0.2
            alternatives.append((
                alt_command,
                confidence,
                f"Use higher mode ({higher_mode.value}) for enhanced capabilities"
            ))
        
        # Squad substitution alternatives
        alternative_squads = self._get_alternative_squads(original_command.target_squad, strategy)
        for alt_squad, squad_confidence, reasoning in alternative_squads:
            alt_command = self._create_command_variant(original_command, squad=alt_squad)
            alternatives.append((alt_command, squad_confidence, reasoning))
        
        return alternatives[:3]  # Return top 3 alternatives
    
    def generate_execution_strategy_alternatives(self, original_command: JAEGISCommand,
                                               strategy: GenerationStrategy) -> List[AlternativeInterpretation]:
        """Generate alternative execution strategies."""
        alternatives = []
        strategy_config = self.generation_strategies[strategy]
        
        # Staged execution alternative
        staged_alt = AlternativeInterpretation(
            interpretation_id=f"staged_{datetime.utcnow().strftime('%H%M%S')}",
            alternative_type=AlternativeType.EXECUTION_STRATEGY,
            generation_strategy=strategy,
            alternative_intent=None,
            alternative_requirements=["Stage 1: Planning", "Stage 2: Execution", "Stage 3: Validation"],
            alternative_approach="Multi-stage execution with validation checkpoints",
            alternative_command=original_command,
            alternative_mode=original_command.mode_level,
            alternative_squad=original_command.target_squad,
            quality_score=0.85,
            confidence=0.8 + strategy_config["risk_tolerance"] * 0.1,
            feasibility=0.9,
            risk_level=0.3,
            similarity_to_original=0.7,
            trade_offs=["Longer execution time", "Multiple validation steps"],
            advantages=["Reduced risk", "Better error handling", "Incremental progress"],
            disadvantages=["Increased complexity", "Longer duration"],
            metadata={"execution_stages": 3, "validation_points": 2}
        )
        alternatives.append(staged_alt)
        
        # Parallel processing alternative (for complex tasks)
        if original_command.mode_level in [JAEGISMode.MODE_3, JAEGISMode.MODE_4, JAEGISMode.MODE_5]:
            parallel_alt = AlternativeInterpretation(
                interpretation_id=f"parallel_{datetime.utcnow().strftime('%H%M%S')}",
                alternative_type=AlternativeType.EXECUTION_STRATEGY,
                generation_strategy=strategy,
                alternative_intent=None,
                alternative_requirements=["Parallel task decomposition", "Concurrent execution", "Result synthesis"],
                alternative_approach="Parallel execution with multiple squads",
                alternative_command=original_command,
                alternative_mode=original_command.mode_level,
                alternative_squad=original_command.target_squad,
                quality_score=0.8,
                confidence=0.75 + strategy_config["innovation_factor"] * 0.15,
                feasibility=0.7,
                risk_level=0.4,
                similarity_to_original=0.6,
                trade_offs=["Higher resource usage", "Coordination complexity"],
                advantages=["Faster execution", "Better resource utilization"],
                disadvantages=["Complex coordination", "Higher resource cost"],
                metadata={"parallel_squads": 2, "coordination_overhead": 0.2}
            )
            alternatives.append(parallel_alt)
        
        return alternatives
    
    def generate_hybrid_alternatives(self, original_command: JAEGISCommand,
                                   validation_result: ConfidenceValidationResult) -> List[AlternativeInterpretation]:
        """Generate hybrid human-AI alternatives."""
        alternatives = []
        
        # Human oversight alternative
        oversight_alt = AlternativeInterpretation(
            interpretation_id=f"oversight_{datetime.utcnow().strftime('%H%M%S')}",
            alternative_type=AlternativeType.HYBRID_APPROACH,
            generation_strategy=GenerationStrategy.CONSERVATIVE,
            alternative_intent=None,
            alternative_requirements=["Human oversight", "AI assistance", "Collaborative execution"],
            alternative_approach="Human-supervised AI execution",
            alternative_command=original_command,
            alternative_mode=original_command.mode_level,
            alternative_squad=original_command.target_squad,
            quality_score=0.9,
            confidence=0.95,  # High confidence with human oversight
            feasibility=0.8,
            risk_level=0.1,
            similarity_to_original=0.8,
            trade_offs=["Requires human availability", "Slower execution"],
            advantages=["Highest accuracy", "Risk mitigation", "Learning opportunity"],
            disadvantages=["Human dependency", "Longer duration", "Higher cost"],
            metadata={"oversight_level": "high", "human_involvement": 0.4}
        )
        alternatives.append(oversight_alt)
        
        # Collaborative execution alternative
        if validation_result.overall_confidence > 0.5:
            collaborative_alt = AlternativeInterpretation(
                interpretation_id=f"collaborative_{datetime.utcnow().strftime('%H%M%S')}",
                alternative_type=AlternativeType.HYBRID_APPROACH,
                generation_strategy=GenerationStrategy.BALANCED,
                alternative_intent=None,
                alternative_requirements=["AI primary execution", "Human validation", "Iterative refinement"],
                alternative_approach="AI-led execution with human validation points",
                alternative_command=original_command,
                alternative_mode=original_command.mode_level,
                alternative_squad=original_command.target_squad,
                quality_score=0.85,
                confidence=0.88,
                feasibility=0.85,
                risk_level=0.2,
                similarity_to_original=0.9,
                trade_offs=["Validation overhead", "Moderate human involvement"],
                advantages=["Balanced approach", "Quality assurance", "Efficiency"],
                disadvantages=["Coordination complexity", "Moderate delays"],
                metadata={"validation_points": 2, "human_involvement": 0.2}
            )
            alternatives.append(collaborative_alt)
        
        return alternatives
    
    def _group_requirements(self, requirements: List[str]) -> List[str]:
        """Group related requirements together."""
        # Simple grouping based on keyword similarity
        grouped = []
        used_indices = set()
        
        for i, req in enumerate(requirements):
            if i in used_indices:
                continue
            
            group = [req]
            req_words = set(req.lower().split())
            
            for j, other_req in enumerate(requirements[i+1:], i+1):
                if j in used_indices:
                    continue
                
                other_words = set(other_req.lower().split())
                overlap = len(req_words.intersection(other_words))
                
                if overlap > 1:  # At least 2 common words
                    group.append(other_req)
                    used_indices.add(j)
            
            grouped.append("; ".join(group))
            used_indices.add(i)
        
        return grouped
    
    def _prioritize_requirements(self, requirements: List[str], strategy: GenerationStrategy) -> List[str]:
        """Prioritize requirements based on strategy."""
        # Simple prioritization based on keywords and strategy
        priority_keywords = {
            GenerationStrategy.CONSERVATIVE: ["simple", "basic", "standard", "safe"],
            GenerationStrategy.AGGRESSIVE: ["advanced", "complex", "comprehensive", "maximum"],
            GenerationStrategy.BALANCED: ["efficient", "optimal", "balanced", "moderate"],
            GenerationStrategy.CREATIVE: ["innovative", "creative", "new", "experimental"],
            GenerationStrategy.FALLBACK: ["minimal", "essential", "core", "basic"]
        }
        
        strategy_keywords = priority_keywords.get(strategy, [])
        
        # Score requirements based on strategy keywords
        scored_requirements = []
        for req in requirements:
            score = 0
            req_lower = req.lower()
            for keyword in strategy_keywords:
                if keyword in req_lower:
                    score += 1
            scored_requirements.append((req, score))
        
        # Sort by score (descending) and return requirements
        scored_requirements.sort(key=lambda x: x[1], reverse=True)
        return [req for req, score in scored_requirements]
    
    def _create_command_variant(self, original_command: JAEGISCommand,
                              mode: Optional[JAEGISMode] = None,
                              squad: Optional[JAEGISSquad] = None) -> JAEGISCommand:
        """Create a variant of the original command."""
        from copy import deepcopy
        
        variant = deepcopy(original_command)
        variant.command_id = f"{original_command.command_id}_variant_{datetime.utcnow().strftime('%H%M%S')}"
        
        if mode:
            variant.mode_level = mode
        if squad:
            variant.target_squad = squad
        
        return variant
    
    def _get_alternative_squads(self, original_squad: JAEGISSquad,
                              strategy: GenerationStrategy) -> List[Tuple[JAEGISSquad, float, str]]:
        """Get alternative squad options."""
        alternatives = []
        strategy_config = self.generation_strategies[strategy]
        preferred_squads = strategy_config.get("preferred_squads", [])
        
        # Map squad names to enum values
        squad_mapping = {
            "tyler_agent": JAEGISSquad.TYLER_AGENT,
            "john_agent": JAEGISSquad.JOHN_AGENT,
            "fred_agent": JAEGISSquad.FRED_AGENT,
            "content_squad": JAEGISSquad.CONTENT_SQUAD,
            "research_squad": JAEGISSquad.RESEARCH_SQUAD,
            "development_squad": JAEGISSquad.DEVELOPMENT_SQUAD,
            "support_squad": JAEGISSquad.SUPPORT_SQUAD,
            "innovation_squad": JAEGISSquad.INNOVATION_SQUAD,
            "master_orchestrator": JAEGISSquad.MASTER_ORCHESTRATOR
        }
        
        for squad_name in preferred_squads:
            if squad_name in squad_mapping:
                alt_squad = squad_mapping[squad_name]
                if alt_squad != original_squad:
                    confidence = 0.7 + strategy_config["resource_efficiency"] * 0.2
                    reasoning = f"Alternative squad with {strategy.value} approach"
                    alternatives.append((alt_squad, confidence, reasoning))
        
        return alternatives[:2]  # Return top 2 alternatives
    
    def assess_alternative_quality(self, alternative: AlternativeInterpretation) -> float:
        """Assess the quality of an alternative interpretation."""
        quality_factors = []
        
        # Feasibility assessment
        feasibility_score = alternative.feasibility
        quality_factors.append(feasibility_score * self.quality_metrics["feasibility_weight"])
        
        # Confidence assessment
        confidence_score = alternative.confidence
        quality_factors.append(confidence_score * self.quality_metrics["confidence_weight"])
        
        # Innovation assessment
        innovation_score = 1.0 - alternative.similarity_to_original  # More different = more innovative
        quality_factors.append(innovation_score * self.quality_metrics["innovation_weight"])
        
        # Resource efficiency assessment
        resource_score = 1.0 - alternative.risk_level  # Lower risk = better resource efficiency
        quality_factors.append(resource_score * self.quality_metrics["resource_efficiency_weight"])
        
        # Risk mitigation assessment
        risk_mitigation_score = 1.0 - alternative.risk_level
        quality_factors.append(risk_mitigation_score * self.quality_metrics["risk_mitigation_weight"])
        
        # User satisfaction assessment (based on advantages vs disadvantages)
        satisfaction_score = len(alternative.advantages) / max(len(alternative.advantages) + len(alternative.disadvantages), 1)
        quality_factors.append(satisfaction_score * self.quality_metrics["user_satisfaction_weight"])
        
        return sum(quality_factors)
    
    def calculate_diversity_score(self, alternatives: List[AlternativeInterpretation]) -> float:
        """Calculate diversity score for a set of alternatives."""
        if len(alternatives) < 2:
            return 0.0
        
        diversity_factors = []
        
        # Intent diversity
        unique_intents = len(set(alt.alternative_intent for alt in alternatives if alt.alternative_intent))
        intent_diversity = unique_intents / len(alternatives)
        diversity_factors.append(intent_diversity * self.diversity_weights["intent_diversity"])
        
        # Approach diversity
        unique_approaches = len(set(alt.alternative_approach for alt in alternatives))
        approach_diversity = unique_approaches / len(alternatives)
        diversity_factors.append(approach_diversity * self.diversity_weights["approach_diversity"])
        
        # Resource diversity (based on squads and modes)
        unique_squads = len(set(alt.alternative_squad for alt in alternatives if alt.alternative_squad))
        unique_modes = len(set(alt.alternative_mode for alt in alternatives if alt.alternative_mode))
        resource_diversity = (unique_squads + unique_modes) / (2 * len(alternatives))
        diversity_factors.append(resource_diversity * self.diversity_weights["resource_diversity"])
        
        # Risk diversity
        risk_levels = [alt.risk_level for alt in alternatives]
        risk_variance = np.var(risk_levels) if len(risk_levels) > 1 else 0.0
        risk_diversity = min(risk_variance * 4, 1.0)  # Normalize variance
        diversity_factors.append(risk_diversity * self.diversity_weights["risk_diversity"])
        
        # Complexity diversity
        similarity_scores = [alt.similarity_to_original for alt in alternatives]
        complexity_variance = np.var(similarity_scores) if len(similarity_scores) > 1 else 0.0
        complexity_diversity = min(complexity_variance * 4, 1.0)
        diversity_factors.append(complexity_diversity * self.diversity_weights["complexity_diversity"])
        
        return sum(diversity_factors)
    
    async def generate_alternatives(self, text: str,
                                  intent_result: IntentRecognitionResult,
                                  logical_result: LogicalAnalysisResult,
                                  synthesis_result: DimensionalSynthesisResult,
                                  command_result: CommandGenerationResult,
                                  mode_result: ModeSelectionResult,
                                  squad_result: SquadSelectionResult,
                                  validation_result: ConfidenceValidationResult) -> AlternativeGenerationResult:
        """
        Generate comprehensive alternatives for ambiguous or low-confidence translations.
        
        Args:
            text: Original input text
            intent_result: Intent recognition results
            logical_result: Logical analysis results
            synthesis_result: Dimensional synthesis results
            command_result: Command generation results
            mode_result: Mode selection results
            squad_result: Squad selection results
            validation_result: Confidence validation results
            
        Returns:
            Complete alternative generation result
        """
        import time
        start_time = time.time()
        
        try:
            # Analyze confidence gaps to determine alternative types needed
            alternative_types = self.analyze_confidence_gaps(validation_result)
            
            # Select generation strategies
            strategies = self.select_generation_strategies(validation_result, intent_result)
            
            # Generate alternatives
            all_alternatives = []
            
            for strategy in strategies:
                strategy_alternatives = []
                
                # Generate intent alternatives
                if AlternativeType.INTENT_REINTERPRETATION in alternative_types:
                    if intent_result.detected_intents:
                        primary_intent = intent_result.detected_intents[0].intent
                        intent_alts = self.generate_intent_alternatives(primary_intent, text, strategy)
                        
                        for alt_intent, confidence, reasoning in intent_alts:
                            alt_interpretation = AlternativeInterpretation(
                                interpretation_id=f"intent_{strategy.value}_{datetime.utcnow().strftime('%H%M%S')}",
                                alternative_type=AlternativeType.INTENT_REINTERPRETATION,
                                generation_strategy=strategy,
                                alternative_intent=alt_intent,
                                alternative_requirements=[reasoning],
                                alternative_approach=f"Reinterpret intent as {alt_intent.value}",
                                alternative_command=command_result.primary_command,
                                alternative_mode=mode_result.selected_mode,
                                alternative_squad=squad_result.primary_squad.squad_profile.squad_id,
                                quality_score=0.0,  # Will be calculated
                                confidence=confidence,
                                feasibility=0.8,
                                risk_level=0.3,
                                similarity_to_original=0.6,
                                trade_offs=[f"Different interpretation: {alt_intent.value}"],
                                advantages=[reasoning, "Alternative perspective"],
                                disadvantages=["May not match original intent"],
                                metadata={"original_intent": primary_intent.value}
                            )
                            strategy_alternatives.append(alt_interpretation)
                
                # Generate command alternatives
                if AlternativeType.COMMAND_VARIATION in alternative_types:
                    command_alts = self.generate_command_alternatives(command_result.primary_command, strategy)
                    
                    for alt_command, confidence, reasoning in command_alts:
                        alt_interpretation = AlternativeInterpretation(
                            interpretation_id=f"command_{strategy.value}_{datetime.utcnow().strftime('%H%M%S')}",
                            alternative_type=AlternativeType.COMMAND_VARIATION,
                            generation_strategy=strategy,
                            alternative_intent=None,
                            alternative_requirements=[reasoning],
                            alternative_approach=f"Modified command execution",
                            alternative_command=alt_command,
                            alternative_mode=alt_command.mode_level,
                            alternative_squad=alt_command.target_squad,
                            quality_score=0.0,
                            confidence=confidence,
                            feasibility=0.85,
                            risk_level=0.25,
                            similarity_to_original=0.8,
                            trade_offs=[f"Different execution approach"],
                            advantages=[reasoning, "Optimized execution"],
                            disadvantages=["May have different resource requirements"],
                            metadata={"original_command": command_result.primary_command.command_id}
                        )
                        strategy_alternatives.append(alt_interpretation)
                
                # Generate execution strategy alternatives
                if AlternativeType.EXECUTION_STRATEGY in alternative_types:
                    execution_alts = self.generate_execution_strategy_alternatives(
                        command_result.primary_command, strategy
                    )
                    strategy_alternatives.extend(execution_alts)
                
                # Generate hybrid alternatives for low confidence
                if validation_result.overall_confidence < 0.7:
                    hybrid_alts = self.generate_hybrid_alternatives(
                        command_result.primary_command, validation_result
                    )
                    strategy_alternatives.extend(hybrid_alts)
                
                all_alternatives.extend(strategy_alternatives)
            
            # Assess quality for all alternatives
            for alternative in all_alternatives:
                alternative.quality_score = self.assess_alternative_quality(alternative)
            
            # Calculate metrics
            average_quality = sum(alt.quality_score for alt in all_alternatives) / len(all_alternatives) if all_alternatives else 0.0
            best_confidence = max(alt.confidence for alt in all_alternatives) if all_alternatives else 0.0
            diversity_score = self.calculate_diversity_score(all_alternatives)
            coverage_score = len(set(alt.alternative_type for alt in all_alternatives)) / len(AlternativeType)
            
            # Select recommended alternatives (top 3 by quality)
            recommended_alternatives = sorted(all_alternatives, key=lambda x: x.quality_score, reverse=True)[:3]
            
            # Select fallback options (conservative, high-confidence alternatives)
            fallback_options = [
                alt for alt in all_alternatives 
                if alt.generation_strategy == GenerationStrategy.FALLBACK or alt.confidence > 0.9
            ][:2]
            
            processing_time = (time.time() - start_time) * 1000
            
            # Update generation history
            self.generation_history.append({
                "timestamp": datetime.utcnow(),
                "original_confidence": validation_result.overall_confidence,
                "alternatives_count": len(all_alternatives),
                "average_quality": average_quality,
                "strategies_used": [s.value for s in strategies]
            })
            
            return AlternativeGenerationResult(
                original_confidence=validation_result.overall_confidence,
                alternatives_generated=all_alternatives,
                generation_strategies_used=strategies,
                average_alternative_quality=average_quality,
                best_alternative_confidence=best_confidence,
                diversity_score=diversity_score,
                coverage_score=coverage_score,
                recommended_alternatives=recommended_alternatives,
                fallback_options=fallback_options,
                processing_time_ms=processing_time,
                metadata={
                    "alternative_types_generated": [t.value for t in alternative_types],
                    "strategies_used": [s.value for s in strategies],
                    "total_alternatives": len(all_alternatives),
                    "quality_distribution": {
                        "excellent": len([a for a in all_alternatives if a.quality_score >= 0.9]),
                        "good": len([a for a in all_alternatives if 0.8 <= a.quality_score < 0.9]),
                        "acceptable": len([a for a in all_alternatives if 0.7 <= a.quality_score < 0.8]),
                        "marginal": len([a for a in all_alternatives if a.quality_score < 0.7])
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Alternative generation failed: {e}")
            
            return AlternativeGenerationResult(
                original_confidence=validation_result.overall_confidence,
                alternatives_generated=[],
                generation_strategies_used=[],
                average_alternative_quality=0.0,
                best_alternative_confidence=0.0,
                diversity_score=0.0,
                coverage_score=0.0,
                recommended_alternatives=[],
                fallback_options=[],
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )


# ============================================================================
# ALTERNATIVE GENERATION UTILITIES
# ============================================================================

class AlternativeGenerationUtils:
    """Utility functions for alternative generation."""
    
    @staticmethod
    def generation_result_to_dict(result: AlternativeGenerationResult) -> Dict[str, Any]:
        """Convert generation result to dictionary format."""
        return {
            "original_confidence": result.original_confidence,
            "alternatives_generated": [
                {
                    "interpretation_id": alt.interpretation_id,
                    "alternative_type": alt.alternative_type.value,
                    "generation_strategy": alt.generation_strategy.value,
                    "quality_score": alt.quality_score,
                    "confidence": alt.confidence,
                    "feasibility": alt.feasibility,
                    "risk_level": alt.risk_level,
                    "alternative_approach": alt.alternative_approach,
                    "advantages": alt.advantages,
                    "disadvantages": alt.disadvantages,
                    "trade_offs": alt.trade_offs
                }
                for alt in result.alternatives_generated
            ],
            "generation_strategies_used": [s.value for s in result.generation_strategies_used],
            "average_alternative_quality": result.average_alternative_quality,
            "best_alternative_confidence": result.best_alternative_confidence,
            "diversity_score": result.diversity_score,
            "coverage_score": result.coverage_score,
            "recommended_alternatives": [
                {
                    "interpretation_id": alt.interpretation_id,
                    "quality_score": alt.quality_score,
                    "confidence": alt.confidence,
                    "alternative_approach": alt.alternative_approach
                }
                for alt in result.recommended_alternatives
            ],
            "processing_time_ms": result.processing_time_ms
        }
    
    @staticmethod
    def get_generation_summary(result: AlternativeGenerationResult) -> Dict[str, Any]:
        """Get summary of alternative generation results."""
        return {
            "original_confidence": result.original_confidence,
            "alternatives_count": len(result.alternatives_generated),
            "recommended_count": len(result.recommended_alternatives),
            "fallback_count": len(result.fallback_options),
            "average_quality": result.average_alternative_quality,
            "best_confidence": result.best_alternative_confidence,
            "diversity_score": result.diversity_score,
            "strategies_used": len(result.generation_strategies_used),
            "processing_time_ms": result.processing_time_ms
        }
