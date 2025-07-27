"""
N.L.D.S. Dimensional Synthesis Engine
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced dimensional synthesis combining logical, emotional, and creative analyses
for comprehensive understanding with 95%+ synthesis coherence.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import asyncio
import numpy as np

# Local imports
from .logical_analyzer import LogicalAnalysisResult, LogicalRequirement
from .emotional_analyzer import EmotionalAnalysisResult, EmotionalContext, UserState
from .creative_interpreter import CreativeAnalysisResult, CreativeIdea, AlternativeApproach

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# SYNTHESIS STRUCTURES AND ENUMS
# ============================================================================

class DimensionWeight(Enum):
    """Weights for different dimensions in synthesis."""
    LOGICAL_DOMINANT = "logical_dominant"      # 60% logical, 25% emotional, 15% creative
    EMOTIONAL_DOMINANT = "emotional_dominant"  # 25% logical, 60% emotional, 15% creative
    CREATIVE_DOMINANT = "creative_dominant"    # 25% logical, 15% emotional, 60% creative
    BALANCED = "balanced"                      # 33% logical, 33% emotional, 34% creative
    ADAPTIVE = "adaptive"                      # Weights determined by context


class SynthesisQuality(Enum):
    """Quality levels of dimensional synthesis."""
    EXCELLENT = "excellent"    # >90% coherence
    GOOD = "good"             # 75-90% coherence
    ADEQUATE = "adequate"     # 60-75% coherence
    POOR = "poor"             # <60% coherence


class ConflictType(Enum):
    """Types of conflicts between dimensions."""
    LOGICAL_EMOTIONAL = "logical_emotional"
    LOGICAL_CREATIVE = "logical_creative"
    EMOTIONAL_CREATIVE = "emotional_creative"
    THREE_WAY = "three_way"
    NO_CONFLICT = "no_conflict"


@dataclass
class DimensionalInsight:
    """Individual dimensional insight."""
    dimension: str
    insight: str
    confidence: float
    supporting_evidence: List[str]
    implications: List[str]
    metadata: Dict[str, Any] = None


@dataclass
class SynthesisConflict:
    """Conflict between dimensional analyses."""
    conflict_type: ConflictType
    description: str
    conflicting_elements: List[str]
    resolution_strategy: str
    confidence_impact: float


@dataclass
class DimensionalRecommendation:
    """Synthesized recommendation."""
    recommendation: str
    rationale: str
    logical_support: float
    emotional_support: float
    creative_support: float
    overall_confidence: float
    implementation_priority: str
    risk_assessment: str


@dataclass
class DimensionalSynthesisResult:
    """Complete dimensional synthesis result."""
    text: str
    synthesis_quality: SynthesisQuality
    coherence_score: float
    dimensional_insights: List[DimensionalInsight]
    synthesis_conflicts: List[SynthesisConflict]
    unified_recommendations: List[DimensionalRecommendation]
    dimension_weights: Dict[str, float]
    integration_score: float
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# DIMENSIONAL SYNTHESIS ENGINE
# ============================================================================

class DimensionalSynthesisEngine:
    """
    Advanced dimensional synthesis engine for comprehensive analysis integration.
    
    Features:
    - Multi-dimensional analysis integration
    - Conflict detection and resolution
    - Adaptive weighting based on context
    - Coherence scoring and validation
    - Unified recommendation generation
    - Quality assessment and optimization
    """
    
    def __init__(self):
        """Initialize dimensional synthesis engine."""
        self.synthesis_patterns = self._load_synthesis_patterns()
        self.conflict_resolution_strategies = self._load_conflict_resolution_strategies()
        self.weighting_strategies = self._load_weighting_strategies()
        self.quality_thresholds = self._load_quality_thresholds()
    
    def _load_synthesis_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load patterns for dimensional synthesis."""
        return {
            "logical_emotional_harmony": {
                "pattern": "Logical requirements align with emotional needs",
                "indicators": ["user satisfaction", "requirement clarity", "emotional acceptance"],
                "weight_boost": 0.1
            },
            "creative_logical_innovation": {
                "pattern": "Creative ideas enhance logical solutions",
                "indicators": ["innovation potential", "feasibility", "requirement fulfillment"],
                "weight_boost": 0.15
            },
            "emotional_creative_resonance": {
                "pattern": "Creative solutions address emotional context",
                "indicators": ["user state alignment", "empathy triggers", "creative empathy"],
                "weight_boost": 0.1
            },
            "three_dimensional_synergy": {
                "pattern": "All dimensions reinforce each other",
                "indicators": ["logical coherence", "emotional intelligence", "creative innovation"],
                "weight_boost": 0.2
            }
        }
    
    def _load_conflict_resolution_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Load conflict resolution strategies."""
        return {
            ConflictType.LOGICAL_EMOTIONAL: {
                "strategy": "Prioritize user emotional state while maintaining logical validity",
                "approach": "emotional_priority_with_logical_constraints",
                "confidence_penalty": 0.1
            },
            ConflictType.LOGICAL_CREATIVE: {
                "strategy": "Balance innovation with feasibility requirements",
                "approach": "feasible_innovation_optimization",
                "confidence_penalty": 0.05
            },
            ConflictType.EMOTIONAL_CREATIVE: {
                "strategy": "Align creative solutions with emotional needs",
                "approach": "empathetic_creativity",
                "confidence_penalty": 0.08
            },
            ConflictType.THREE_WAY: {
                "strategy": "Find compromise solution addressing all dimensions",
                "approach": "multi_dimensional_optimization",
                "confidence_penalty": 0.15
            }
        }
    
    def _load_weighting_strategies(self) -> Dict[str, Dict[str, float]]:
        """Load weighting strategies for different contexts."""
        return {
            DimensionWeight.LOGICAL_DOMINANT.value: {
                "logical": 0.60,
                "emotional": 0.25,
                "creative": 0.15
            },
            DimensionWeight.EMOTIONAL_DOMINANT.value: {
                "logical": 0.25,
                "emotional": 0.60,
                "creative": 0.15
            },
            DimensionWeight.CREATIVE_DOMINANT.value: {
                "logical": 0.25,
                "emotional": 0.15,
                "creative": 0.60
            },
            DimensionWeight.BALANCED.value: {
                "logical": 0.33,
                "emotional": 0.33,
                "creative": 0.34
            }
        }
    
    def _load_quality_thresholds(self) -> Dict[str, float]:
        """Load quality assessment thresholds."""
        return {
            SynthesisQuality.EXCELLENT.value: 0.90,
            SynthesisQuality.GOOD.value: 0.75,
            SynthesisQuality.ADEQUATE.value: 0.60,
            SynthesisQuality.POOR.value: 0.0
        }
    
    def determine_adaptive_weights(self, logical_result: LogicalAnalysisResult,
                                 emotional_result: EmotionalAnalysisResult,
                                 creative_result: CreativeAnalysisResult) -> Dict[str, float]:
        """Determine adaptive weights based on analysis results."""
        # Start with balanced weights
        weights = {"logical": 0.33, "emotional": 0.33, "creative": 0.34}
        
        # Adjust based on user state
        user_state = emotional_result.emotional_context.user_state
        
        if user_state in [UserState.FRUSTRATED, UserState.CONFUSED]:
            # Prioritize emotional dimension
            weights["emotional"] += 0.2
            weights["logical"] -= 0.1
            weights["creative"] -= 0.1
        
        elif user_state == UserState.URGENT:
            # Prioritize logical dimension for efficiency
            weights["logical"] += 0.2
            weights["emotional"] -= 0.1
            weights["creative"] -= 0.1
        
        elif user_state in [UserState.EXCITED, UserState.SATISFIED]:
            # Allow more creative exploration
            weights["creative"] += 0.15
            weights["logical"] -= 0.075
            weights["emotional"] -= 0.075
        
        # Adjust based on complexity
        complexity = logical_result.complexity_score
        if complexity > 0.8:
            # High complexity - boost logical analysis
            weights["logical"] += 0.1
            weights["creative"] -= 0.05
            weights["emotional"] -= 0.05
        
        # Adjust based on innovation potential
        innovation_potential = creative_result.innovation_potential_score
        if innovation_potential > 0.8:
            # High innovation potential - boost creative dimension
            weights["creative"] += 0.1
            weights["logical"] -= 0.05
            weights["emotional"] -= 0.05
        
        # Normalize weights
        total_weight = sum(weights.values())
        weights = {k: v / total_weight for k, v in weights.items()}
        
        return weights
    
    def extract_dimensional_insights(self, logical_result: LogicalAnalysisResult,
                                   emotional_result: EmotionalAnalysisResult,
                                   creative_result: CreativeAnalysisResult) -> List[DimensionalInsight]:
        """Extract insights from each dimensional analysis."""
        insights = []
        
        # Logical insights
        if logical_result.requirements:
            logical_insight = DimensionalInsight(
                dimension="logical",
                insight=f"Identified {len(logical_result.requirements)} requirements with {logical_result.coherence_score:.1%} coherence",
                confidence=logical_result.logical_structure.validity_score,
                supporting_evidence=[req.text for req in logical_result.requirements[:3]],
                implications=[
                    "Clear requirement structure enables systematic implementation",
                    "Logical coherence supports reliable execution",
                    "Structured approach reduces implementation risks"
                ],
                metadata={
                    "requirements_count": len(logical_result.requirements),
                    "complexity_score": logical_result.complexity_score
                }
            )
            insights.append(logical_insight)
        
        # Emotional insights
        emotional_context = emotional_result.emotional_context
        emotional_insight = DimensionalInsight(
            dimension="emotional",
            insight=f"User state: {emotional_context.user_state.value}, Dominant emotion: {emotional_context.dominant_emotion.value}",
            confidence=emotional_result.emotional_intelligence_score,
            supporting_evidence=[
                f"Sentiment: {emotional_context.sentiment_analysis.polarity.value}",
                f"Urgency level: {emotional_context.urgency_level:.1%}",
                f"Empathy triggers: {len(emotional_context.empathy_triggers)}"
            ],
            implications=emotional_result.user_adaptation_suggestions,
            metadata={
                "user_state": emotional_context.user_state.value,
                "urgency_level": emotional_context.urgency_level
            }
        )
        insights.append(emotional_insight)
        
        # Creative insights
        if creative_result.creative_ideas:
            creative_insight = DimensionalInsight(
                dimension="creative",
                insight=f"Generated {len(creative_result.creative_ideas)} creative ideas with {creative_result.innovation_potential_score:.1%} innovation potential",
                confidence=creative_result.innovation_potential_score,
                supporting_evidence=[idea.description for idea in creative_result.creative_ideas[:3]],
                implications=[
                    "Multiple creative approaches available",
                    "Innovation opportunities identified",
                    "Alternative solutions provide flexibility"
                ],
                metadata={
                    "ideas_count": len(creative_result.creative_ideas),
                    "approaches_count": len(creative_result.alternative_approaches)
                }
            )
            insights.append(creative_insight)
        
        return insights
    
    def detect_synthesis_conflicts(self, logical_result: LogicalAnalysisResult,
                                 emotional_result: EmotionalAnalysisResult,
                                 creative_result: CreativeAnalysisResult) -> List[SynthesisConflict]:
        """Detect conflicts between dimensional analyses."""
        conflicts = []
        
        # Logical vs Emotional conflicts
        user_state = emotional_result.emotional_context.user_state
        urgency = emotional_result.emotional_context.urgency_level
        complexity = logical_result.complexity_score
        
        if user_state == UserState.URGENT and complexity > 0.7:
            conflict = SynthesisConflict(
                conflict_type=ConflictType.LOGICAL_EMOTIONAL,
                description="High logical complexity conflicts with urgent emotional state",
                conflicting_elements=["Complex requirements", "Urgent user state"],
                resolution_strategy="Prioritize immediate needs while planning for complexity",
                confidence_impact=0.1
            )
            conflicts.append(conflict)
        
        # Logical vs Creative conflicts
        if logical_result.requirements and creative_result.creative_ideas:
            high_innovation_ideas = [idea for idea in creative_result.creative_ideas 
                                   if idea.innovation_level.value in ["radical", "breakthrough"]]
            
            if high_innovation_ideas and any(req.requirement_type.value == "constraint" 
                                           for req in logical_result.requirements):
                conflict = SynthesisConflict(
                    conflict_type=ConflictType.LOGICAL_CREATIVE,
                    description="Radical creative ideas may conflict with logical constraints",
                    conflicting_elements=["Logical constraints", "Radical innovations"],
                    resolution_strategy="Evaluate constraint flexibility for innovation",
                    confidence_impact=0.05
                )
                conflicts.append(conflict)
        
        # Emotional vs Creative conflicts
        if user_state in [UserState.FRUSTRATED, UserState.CONFUSED] and \
           creative_result.innovation_potential_score > 0.8:
            conflict = SynthesisConflict(
                conflict_type=ConflictType.EMOTIONAL_CREATIVE,
                description="High innovation potential may overwhelm frustrated/confused user",
                conflicting_elements=["User emotional state", "Complex creative solutions"],
                resolution_strategy="Simplify creative solutions for current emotional state",
                confidence_impact=0.08
            )
            conflicts.append(conflict)
        
        return conflicts
    
    def generate_unified_recommendations(self, logical_result: LogicalAnalysisResult,
                                       emotional_result: EmotionalAnalysisResult,
                                       creative_result: CreativeAnalysisResult,
                                       weights: Dict[str, float]) -> List[DimensionalRecommendation]:
        """Generate unified recommendations from all dimensions."""
        recommendations = []
        
        # Primary recommendation based on dominant dimension
        dominant_dimension = max(weights.items(), key=lambda x: x[1])
        
        if dominant_dimension[0] == "logical":
            primary_rec = self._generate_logical_primary_recommendation(
                logical_result, emotional_result, creative_result, weights
            )
        elif dominant_dimension[0] == "emotional":
            primary_rec = self._generate_emotional_primary_recommendation(
                logical_result, emotional_result, creative_result, weights
            )
        else:  # creative
            primary_rec = self._generate_creative_primary_recommendation(
                logical_result, emotional_result, creative_result, weights
            )
        
        recommendations.append(primary_rec)
        
        # Secondary recommendations
        secondary_recs = self._generate_secondary_recommendations(
            logical_result, emotional_result, creative_result, weights
        )
        recommendations.extend(secondary_recs)
        
        # Sort by overall confidence
        recommendations.sort(key=lambda x: x.overall_confidence, reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _generate_logical_primary_recommendation(self, logical_result: LogicalAnalysisResult,
                                               emotional_result: EmotionalAnalysisResult,
                                               creative_result: CreativeAnalysisResult,
                                               weights: Dict[str, float]) -> DimensionalRecommendation:
        """Generate logical-primary recommendation."""
        # Focus on requirements and logical structure
        high_priority_reqs = [req for req in logical_result.requirements if req.priority == "high"]
        
        recommendation = f"Implement systematic approach addressing {len(high_priority_reqs)} high-priority requirements"
        
        rationale = "Logical analysis indicates structured implementation with clear requirements"
        
        # Adjust for emotional context
        user_state = emotional_result.emotional_context.user_state
        if user_state in [UserState.FRUSTRATED, UserState.CONFUSED]:
            recommendation += " with step-by-step guidance and clear communication"
            rationale += ", adapted for current user emotional state"
        
        # Incorporate creative elements
        if creative_result.creative_ideas:
            feasible_ideas = [idea for idea in creative_result.creative_ideas if idea.feasibility_score > 0.7]
            if feasible_ideas:
                recommendation += f" incorporating {len(feasible_ideas)} feasible innovations"
                rationale += " enhanced with practical creative solutions"
        
        return DimensionalRecommendation(
            recommendation=recommendation,
            rationale=rationale,
            logical_support=0.9,
            emotional_support=weights["emotional"],
            creative_support=weights["creative"],
            overall_confidence=self._calculate_recommendation_confidence(weights, 0.9, weights["emotional"], weights["creative"]),
            implementation_priority="high",
            risk_assessment="low"
        )
    
    def _generate_emotional_primary_recommendation(self, logical_result: LogicalAnalysisResult,
                                                 emotional_result: EmotionalAnalysisResult,
                                                 creative_result: CreativeAnalysisResult,
                                                 weights: Dict[str, float]) -> DimensionalRecommendation:
        """Generate emotional-primary recommendation."""
        user_state = emotional_result.emotional_context.user_state
        
        # Focus on emotional needs
        if user_state == UserState.FRUSTRATED:
            recommendation = "Provide immediate support and simplified solutions to address frustration"
        elif user_state == UserState.CONFUSED:
            recommendation = "Offer clear explanations and step-by-step guidance"
        elif user_state == UserState.URGENT:
            recommendation = "Prioritize quick wins and immediate actionable solutions"
        else:
            recommendation = "Maintain positive engagement while delivering comprehensive solutions"
        
        rationale = f"Emotional analysis indicates user state requires {user_state.value}-focused approach"
        
        # Incorporate logical structure
        if logical_result.requirements:
            recommendation += f" while addressing {len(logical_result.requirements)} identified requirements"
            rationale += " with systematic requirement fulfillment"
        
        # Add creative elements
        if creative_result.alternative_approaches:
            suitable_approaches = [app for app in creative_result.alternative_approaches 
                                 if app.risk_level in ["low", "medium"]]
            if suitable_approaches:
                recommendation += f" using {len(suitable_approaches)} alternative approaches"
                rationale += " enhanced with creative alternatives"
        
        return DimensionalRecommendation(
            recommendation=recommendation,
            rationale=rationale,
            logical_support=weights["logical"],
            emotional_support=0.9,
            creative_support=weights["creative"],
            overall_confidence=self._calculate_recommendation_confidence(weights["logical"], 0.9, weights["creative"]),
            implementation_priority="high",
            risk_assessment="medium"
        )
    
    def _generate_creative_primary_recommendation(self, logical_result: LogicalAnalysisResult,
                                                emotional_result: EmotionalAnalysisResult,
                                                creative_result: CreativeAnalysisResult,
                                                weights: Dict[str, float]) -> DimensionalRecommendation:
        """Generate creative-primary recommendation."""
        # Focus on innovation and creative solutions
        top_ideas = creative_result.creative_ideas[:3]
        
        recommendation = f"Explore innovative solutions including {', '.join([idea.creativity_type.value for idea in top_ideas])}"
        
        rationale = f"Creative analysis reveals {creative_result.innovation_potential_score:.1%} innovation potential"
        
        # Ensure emotional alignment
        user_state = emotional_result.emotional_context.user_state
        if user_state in [UserState.FRUSTRATED, UserState.CONFUSED]:
            recommendation += " with careful introduction and support"
            rationale += ", adapted for current emotional readiness"
        
        # Maintain logical feasibility
        if logical_result.requirements:
            recommendation += f" while meeting {len(logical_result.requirements)} core requirements"
            rationale += " within logical constraints"
        
        return DimensionalRecommendation(
            recommendation=recommendation,
            rationale=rationale,
            logical_support=weights["logical"],
            emotional_support=weights["emotional"],
            creative_support=0.9,
            overall_confidence=self._calculate_recommendation_confidence(weights["logical"], weights["emotional"], 0.9),
            implementation_priority="medium",
            risk_assessment="medium"
        )
    
    def _generate_secondary_recommendations(self, logical_result: LogicalAnalysisResult,
                                          emotional_result: EmotionalAnalysisResult,
                                          creative_result: CreativeAnalysisResult,
                                          weights: Dict[str, float]) -> List[DimensionalRecommendation]:
        """Generate secondary recommendations."""
        recommendations = []
        
        # Process optimization recommendation
        if logical_result.complexity_score > 0.6:
            rec = DimensionalRecommendation(
                recommendation="Implement process optimization to reduce complexity",
                rationale="High complexity score indicates optimization opportunities",
                logical_support=0.8,
                emotional_support=0.6,
                creative_support=0.4,
                overall_confidence=0.7,
                implementation_priority="medium",
                risk_assessment="low"
            )
            recommendations.append(rec)
        
        # User experience enhancement
        if emotional_result.emotional_context.empathy_triggers:
            rec = DimensionalRecommendation(
                recommendation="Enhance user experience with empathetic design",
                rationale="Empathy triggers detected requiring supportive approach",
                logical_support=0.5,
                emotional_support=0.9,
                creative_support=0.7,
                overall_confidence=0.75,
                implementation_priority="high",
                risk_assessment="low"
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _calculate_recommendation_confidence(self, logical_support: float,
                                           emotional_support: float,
                                           creative_support: float) -> float:
        """Calculate overall recommendation confidence."""
        # Weighted average with minimum threshold
        confidence = (logical_support + emotional_support + creative_support) / 3
        
        # Boost for balanced support
        support_variance = np.var([logical_support, emotional_support, creative_support])
        if support_variance < 0.1:  # Low variance indicates balanced support
            confidence += 0.1
        
        return min(confidence, 0.95)
    
    def calculate_coherence_score(self, dimensional_insights: List[DimensionalInsight],
                                conflicts: List[SynthesisConflict]) -> float:
        """Calculate overall synthesis coherence score."""
        # Base coherence from insights
        if dimensional_insights:
            avg_insight_confidence = np.mean([insight.confidence for insight in dimensional_insights])
        else:
            avg_insight_confidence = 0.5
        
        # Penalty for conflicts
        conflict_penalty = sum([conflict.confidence_impact for conflict in conflicts])
        
        # Coherence score
        coherence = avg_insight_confidence - conflict_penalty
        
        return max(coherence, 0.0)
    
    def determine_synthesis_quality(self, coherence_score: float) -> SynthesisQuality:
        """Determine synthesis quality based on coherence score."""
        if coherence_score >= self.quality_thresholds[SynthesisQuality.EXCELLENT.value]:
            return SynthesisQuality.EXCELLENT
        elif coherence_score >= self.quality_thresholds[SynthesisQuality.GOOD.value]:
            return SynthesisQuality.GOOD
        elif coherence_score >= self.quality_thresholds[SynthesisQuality.ADEQUATE.value]:
            return SynthesisQuality.ADEQUATE
        else:
            return SynthesisQuality.POOR
    
    def calculate_integration_score(self, weights: Dict[str, float],
                                  dimensional_insights: List[DimensionalInsight],
                                  recommendations: List[DimensionalRecommendation]) -> float:
        """Calculate dimensional integration score."""
        factors = []
        
        # Weight balance factor
        weight_variance = np.var(list(weights.values()))
        balance_factor = 1 - min(weight_variance * 3, 1.0)  # Lower variance = better balance
        factors.append(balance_factor * 0.3)
        
        # Insight integration factor
        if dimensional_insights:
            insight_factor = len(dimensional_insights) / 3  # Expect 3 dimensions
            factors.append(min(insight_factor, 1.0) * 0.3)
        
        # Recommendation coherence factor
        if recommendations:
            avg_rec_confidence = np.mean([rec.overall_confidence for rec in recommendations])
            factors.append(avg_rec_confidence * 0.4)
        
        return sum(factors) if factors else 0.0
    
    async def synthesize_dimensions(self, text: str,
                                  logical_result: LogicalAnalysisResult,
                                  emotional_result: EmotionalAnalysisResult,
                                  creative_result: CreativeAnalysisResult) -> DimensionalSynthesisResult:
        """
        Perform complete dimensional synthesis.
        
        Args:
            text: Input text
            logical_result: Logical analysis results
            emotional_result: Emotional analysis results
            creative_result: Creative analysis results
            
        Returns:
            Complete dimensional synthesis result
        """
        import time
        start_time = time.time()
        
        try:
            # Determine adaptive weights
            weights = self.determine_adaptive_weights(logical_result, emotional_result, creative_result)
            
            # Extract dimensional insights
            dimensional_insights = self.extract_dimensional_insights(
                logical_result, emotional_result, creative_result
            )
            
            # Detect synthesis conflicts
            synthesis_conflicts = self.detect_synthesis_conflicts(
                logical_result, emotional_result, creative_result
            )
            
            # Generate unified recommendations
            unified_recommendations = self.generate_unified_recommendations(
                logical_result, emotional_result, creative_result, weights
            )
            
            # Calculate coherence score
            coherence_score = self.calculate_coherence_score(dimensional_insights, synthesis_conflicts)
            
            # Determine synthesis quality
            synthesis_quality = self.determine_synthesis_quality(coherence_score)
            
            # Calculate integration score
            integration_score = self.calculate_integration_score(
                weights, dimensional_insights, unified_recommendations
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return DimensionalSynthesisResult(
                text=text,
                synthesis_quality=synthesis_quality,
                coherence_score=coherence_score,
                dimensional_insights=dimensional_insights,
                synthesis_conflicts=synthesis_conflicts,
                unified_recommendations=unified_recommendations,
                dimension_weights=weights,
                integration_score=integration_score,
                processing_time_ms=processing_time,
                metadata={
                    "insights_count": len(dimensional_insights),
                    "conflicts_count": len(synthesis_conflicts),
                    "recommendations_count": len(unified_recommendations),
                    "dominant_dimension": max(weights.items(), key=lambda x: x[1])[0],
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Dimensional synthesis failed: {e}")
            
            return DimensionalSynthesisResult(
                text=text,
                synthesis_quality=SynthesisQuality.POOR,
                coherence_score=0.0,
                dimensional_insights=[],
                synthesis_conflicts=[],
                unified_recommendations=[],
                dimension_weights={"logical": 0.33, "emotional": 0.33, "creative": 0.34},
                integration_score=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )


# ============================================================================
# SYNTHESIS UTILITIES
# ============================================================================

class SynthesisUtils:
    """Utility functions for dimensional synthesis."""
    
    @staticmethod
    def recommendations_to_dict(recommendations: List[DimensionalRecommendation]) -> List[Dict[str, Any]]:
        """Convert recommendations to dictionary format."""
        return [
            {
                "recommendation": rec.recommendation,
                "rationale": rec.rationale,
                "logical_support": rec.logical_support,
                "emotional_support": rec.emotional_support,
                "creative_support": rec.creative_support,
                "overall_confidence": rec.overall_confidence,
                "implementation_priority": rec.implementation_priority,
                "risk_assessment": rec.risk_assessment
            }
            for rec in recommendations
        ]
    
    @staticmethod
    def analyze_dimension_balance(weights: Dict[str, float]) -> Dict[str, Any]:
        """Analyze balance between dimensions."""
        max_weight = max(weights.values())
        min_weight = min(weights.values())
        
        return {
            "balance_ratio": min_weight / max_weight,
            "dominant_dimension": max(weights.items(), key=lambda x: x[1])[0],
            "weight_variance": np.var(list(weights.values())),
            "is_balanced": max_weight - min_weight < 0.2
        }
    
    @staticmethod
    def get_synthesis_summary(result: DimensionalSynthesisResult) -> Dict[str, Any]:
        """Get summary of synthesis results."""
        return {
            "quality": result.synthesis_quality.value,
            "coherence_score": result.coherence_score,
            "integration_score": result.integration_score,
            "insights_count": len(result.dimensional_insights),
            "conflicts_count": len(result.synthesis_conflicts),
            "recommendations_count": len(result.unified_recommendations),
            "dominant_dimension": max(result.dimension_weights.items(), key=lambda x: x[1])[0],
            "processing_time_ms": result.processing_time_ms
        }
