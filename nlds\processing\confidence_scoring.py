"""
N.L.D.S. Confidence Scoring Algorithm
Advanced confidence scoring across all three dimensions with weighted aggregation
"""

import numpy as np
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import time
from collections import defaultdict

logger = logging.getLogger(__name__)


class ConfidenceLevel(str, Enum):
    """Confidence level classifications."""
    VERY_HIGH = "very_high"    # 90-100%
    HIGH = "high"              # 80-89%
    MEDIUM = "medium"          # 70-79%
    LOW = "low"                # 60-69%
    VERY_LOW = "very_low"      # <60%


class ConfidenceSource(str, Enum):
    """Sources of confidence information."""
    LOGICAL_ANALYSIS = "logical_analysis"
    EMOTIONAL_ANALYSIS = "emotional_analysis"
    CREATIVE_ANALYSIS = "creative_analysis"
    DIMENSIONAL_SYNTHESIS = "dimensional_synthesis"
    EXTERNAL_VALIDATION = "external_validation"
    HISTORICAL_PERFORMANCE = "historical_performance"


class UncertaintyType(str, Enum):
    """Types of uncertainty in analysis."""
    ALEATORY = "aleatory"          # Inherent randomness
    EPISTEMIC = "epistemic"        # Knowledge uncertainty
    LINGUISTIC = "linguistic"      # Language ambiguity
    CONTEXTUAL = "contextual"      # Context dependency
    TEMPORAL = "temporal"          # Time-dependent uncertainty


@dataclass
class ConfidenceComponent:
    """Individual confidence component."""
    component_id: str
    source: ConfidenceSource
    base_confidence: float
    uncertainty_factors: List[str]
    evidence_strength: float
    reliability_score: float
    temporal_decay: float
    weight: float


@dataclass
class UncertaintyFactor:
    """Uncertainty factor affecting confidence."""
    factor_type: UncertaintyType
    description: str
    impact_magnitude: float
    mitigation_strategies: List[str]
    confidence_reduction: float


@dataclass
class ConfidenceCalibration:
    """Confidence calibration parameters."""
    calibration_curve: List[Tuple[float, float]]
    overconfidence_bias: float
    underconfidence_bias: float
    domain_expertise_factor: float
    historical_accuracy: float


@dataclass
class ConfidenceBreakdown:
    """Detailed confidence breakdown."""
    overall_confidence: float
    confidence_level: ConfidenceLevel
    component_confidences: List[ConfidenceComponent]
    uncertainty_factors: List[UncertaintyFactor]
    confidence_intervals: Dict[str, Tuple[float, float]]
    reliability_assessment: Dict[str, float]
    calibration_metrics: ConfidenceCalibration


@dataclass
class ConfidenceScoringResult:
    """Complete confidence scoring result."""
    confidence_breakdown: ConfidenceBreakdown
    dimensional_confidences: Dict[str, float]
    aggregated_confidence: float
    confidence_trajectory: List[float]
    uncertainty_analysis: Dict[str, Any]
    recommendations: List[str]
    processing_time_ms: float
    metadata: Dict[str, Any]


class ConfidenceScoringAlgorithm:
    """
    Advanced confidence scoring algorithm for N.L.D.S.
    
    Provides comprehensive confidence assessment across logical, emotional,
    and creative dimensions with uncertainty quantification and calibration.
    """
    
    def __init__(self):
        # Confidence scoring configuration
        self.scoring_config = self._initialize_scoring_config()
        
        # Uncertainty models
        self.uncertainty_models = self._initialize_uncertainty_models()
        
        # Calibration parameters
        self.calibration_params = self._initialize_calibration_params()
        
        # Confidence aggregation weights
        self.aggregation_weights = self._initialize_aggregation_weights()
        
        # Historical performance data
        self.performance_history = self._initialize_performance_history()
        
        logger.info("Confidence Scoring Algorithm initialized")
    
    def _initialize_scoring_config(self) -> Dict[str, Any]:
        """Initialize confidence scoring configuration."""
        
        return {
            "confidence_threshold": 0.85,  # N.L.D.S. requirement
            "uncertainty_penalty_factor": 0.1,
            "evidence_weight_factor": 0.2,
            "temporal_decay_rate": 0.05,
            "calibration_enabled": True,
            "confidence_intervals": {
                "alpha": 0.05,  # 95% confidence intervals
                "bootstrap_samples": 1000
            },
            "aggregation_method": "weighted_geometric_mean",
            "bias_correction": {
                "overconfidence_correction": 0.05,
                "underconfidence_correction": 0.03
            }
        }
    
    def _initialize_uncertainty_models(self) -> Dict[UncertaintyType, Dict[str, Any]]:
        """Initialize uncertainty quantification models."""
        
        return {
            UncertaintyType.ALEATORY: {
                "description": "Inherent randomness in data and processes",
                "base_uncertainty": 0.05,
                "factors": ["data_noise", "measurement_error", "natural_variation"],
                "mitigation": ["larger_samples", "better_instruments", "statistical_methods"]
            },
            
            UncertaintyType.EPISTEMIC: {
                "description": "Uncertainty due to lack of knowledge",
                "base_uncertainty": 0.10,
                "factors": ["incomplete_data", "model_limitations", "unknown_unknowns"],
                "mitigation": ["more_data", "better_models", "expert_knowledge"]
            },
            
            UncertaintyType.LINGUISTIC: {
                "description": "Ambiguity in natural language",
                "base_uncertainty": 0.08,
                "factors": ["word_ambiguity", "context_dependency", "cultural_differences"],
                "mitigation": ["clarification", "context_analysis", "multiple_interpretations"]
            },
            
            UncertaintyType.CONTEXTUAL: {
                "description": "Context-dependent interpretation",
                "base_uncertainty": 0.12,
                "factors": ["missing_context", "implicit_assumptions", "domain_specificity"],
                "mitigation": ["context_gathering", "assumption_validation", "domain_expertise"]
            },
            
            UncertaintyType.TEMPORAL: {
                "description": "Time-dependent changes",
                "base_uncertainty": 0.06,
                "factors": ["information_decay", "changing_requirements", "evolving_context"],
                "mitigation": ["regular_updates", "change_monitoring", "adaptive_systems"]
            }
        }
    
    def _initialize_calibration_params(self) -> ConfidenceCalibration:
        """Initialize confidence calibration parameters."""
        
        # Calibration curve: (predicted_confidence, actual_accuracy)
        calibration_curve = [
            (0.5, 0.45), (0.6, 0.55), (0.7, 0.65), (0.8, 0.75),
            (0.85, 0.82), (0.9, 0.88), (0.95, 0.92), (1.0, 0.95)
        ]
        
        return ConfidenceCalibration(
            calibration_curve=calibration_curve,
            overconfidence_bias=0.05,
            underconfidence_bias=0.03,
            domain_expertise_factor=1.1,
            historical_accuracy=0.82
        )
    
    def _initialize_aggregation_weights(self) -> Dict[str, Dict[str, float]]:
        """Initialize confidence aggregation weights."""
        
        return {
            "balanced": {
                "logical": 0.35,
                "emotional": 0.30,
                "creative": 0.25,
                "synthesis": 0.10
            },
            
            "logic_heavy": {
                "logical": 0.50,
                "emotional": 0.25,
                "creative": 0.15,
                "synthesis": 0.10
            },
            
            "emotion_aware": {
                "logical": 0.25,
                "emotional": 0.45,
                "creative": 0.20,
                "synthesis": 0.10
            },
            
            "creative_focus": {
                "logical": 0.20,
                "emotional": 0.25,
                "creative": 0.45,
                "synthesis": 0.10
            }
        }
    
    def _initialize_performance_history(self) -> Dict[str, List[float]]:
        """Initialize historical performance data."""
        
        return {
            "logical_accuracy": [0.85, 0.87, 0.84, 0.86, 0.88],
            "emotional_accuracy": [0.78, 0.80, 0.79, 0.82, 0.81],
            "creative_accuracy": [0.72, 0.75, 0.73, 0.76, 0.74],
            "overall_accuracy": [0.82, 0.84, 0.81, 0.83, 0.85]
        }
    
    def calculate_confidence(self, 
                           logical_confidence: float,
                           emotional_confidence: float,
                           creative_confidence: float,
                           synthesis_confidence: Optional[float] = None,
                           context: Optional[Dict[str, Any]] = None) -> ConfidenceScoringResult:
        """Calculate comprehensive confidence score across all dimensions."""
        
        start_time = time.time()
        
        # Create confidence components
        components = self._create_confidence_components(
            logical_confidence, emotional_confidence, creative_confidence, synthesis_confidence
        )
        
        # Identify uncertainty factors
        uncertainty_factors = self._identify_uncertainty_factors(context)
        
        # Calculate component-level confidences with uncertainty
        adjusted_components = self._adjust_for_uncertainty(components, uncertainty_factors)
        
        # Determine aggregation weights based on context
        weights = self._determine_aggregation_weights(context)
        
        # Aggregate dimensional confidences
        aggregated_confidence = self._aggregate_confidences(adjusted_components, weights)
        
        # Apply calibration
        calibrated_confidence = self._apply_calibration(aggregated_confidence, context)
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(adjusted_components)
        
        # Assess reliability
        reliability_assessment = self._assess_reliability(adjusted_components, uncertainty_factors)
        
        # Generate confidence trajectory
        confidence_trajectory = self._generate_confidence_trajectory(adjusted_components)
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(calibrated_confidence)
        
        # Create confidence breakdown
        confidence_breakdown = ConfidenceBreakdown(
            overall_confidence=calibrated_confidence,
            confidence_level=confidence_level,
            component_confidences=adjusted_components,
            uncertainty_factors=uncertainty_factors,
            confidence_intervals=confidence_intervals,
            reliability_assessment=reliability_assessment,
            calibration_metrics=self.calibration_params
        )
        
        # Generate recommendations
        recommendations = self._generate_confidence_recommendations(
            confidence_breakdown, uncertainty_factors
        )
        
        # Perform uncertainty analysis
        uncertainty_analysis = self._perform_uncertainty_analysis(uncertainty_factors)
        
        processing_time = (time.time() - start_time) * 1000
        
        return ConfidenceScoringResult(
            confidence_breakdown=confidence_breakdown,
            dimensional_confidences={
                "logical": logical_confidence,
                "emotional": emotional_confidence,
                "creative": creative_confidence,
                "synthesis": synthesis_confidence or 0.0
            },
            aggregated_confidence=calibrated_confidence,
            confidence_trajectory=confidence_trajectory,
            uncertainty_analysis=uncertainty_analysis,
            recommendations=recommendations,
            processing_time_ms=processing_time,
            metadata={
                "aggregation_method": self.scoring_config["aggregation_method"],
                "calibration_applied": self.scoring_config["calibration_enabled"],
                "uncertainty_factors_count": len(uncertainty_factors),
                "confidence_threshold": self.scoring_config["confidence_threshold"]
            }
        )
    
    def _create_confidence_components(self, logical_conf: float, emotional_conf: float,
                                    creative_conf: float, synthesis_conf: Optional[float]) -> List[ConfidenceComponent]:
        """Create confidence components for each dimension."""
        
        components = []
        
        # Logical component
        logical_component = ConfidenceComponent(
            component_id="logical_analysis",
            source=ConfidenceSource.LOGICAL_ANALYSIS,
            base_confidence=logical_conf,
            uncertainty_factors=["epistemic", "contextual"],
            evidence_strength=self._calculate_evidence_strength(logical_conf),
            reliability_score=np.mean(self.performance_history["logical_accuracy"]),
            temporal_decay=0.0,  # Fresh analysis
            weight=0.35
        )
        components.append(logical_component)
        
        # Emotional component
        emotional_component = ConfidenceComponent(
            component_id="emotional_analysis",
            source=ConfidenceSource.EMOTIONAL_ANALYSIS,
            base_confidence=emotional_conf,
            uncertainty_factors=["linguistic", "contextual"],
            evidence_strength=self._calculate_evidence_strength(emotional_conf),
            reliability_score=np.mean(self.performance_history["emotional_accuracy"]),
            temporal_decay=0.0,
            weight=0.30
        )
        components.append(emotional_component)
        
        # Creative component
        creative_component = ConfidenceComponent(
            component_id="creative_analysis",
            source=ConfidenceSource.CREATIVE_ANALYSIS,
            base_confidence=creative_conf,
            uncertainty_factors=["aleatory", "epistemic"],
            evidence_strength=self._calculate_evidence_strength(creative_conf),
            reliability_score=np.mean(self.performance_history["creative_accuracy"]),
            temporal_decay=0.0,
            weight=0.25
        )
        components.append(creative_component)
        
        # Synthesis component (if available)
        if synthesis_conf is not None:
            synthesis_component = ConfidenceComponent(
                component_id="dimensional_synthesis",
                source=ConfidenceSource.DIMENSIONAL_SYNTHESIS,
                base_confidence=synthesis_conf,
                uncertainty_factors=["epistemic", "contextual"],
                evidence_strength=self._calculate_evidence_strength(synthesis_conf),
                reliability_score=0.80,  # Estimated reliability
                temporal_decay=0.0,
                weight=0.10
            )
            components.append(synthesis_component)
        
        return components
    
    def _calculate_evidence_strength(self, confidence: float) -> float:
        """Calculate evidence strength based on confidence."""
        
        # Evidence strength increases non-linearly with confidence
        return min(1.0, confidence ** 1.5)
    
    def _identify_uncertainty_factors(self, context: Optional[Dict[str, Any]]) -> List[UncertaintyFactor]:
        """Identify uncertainty factors affecting confidence."""
        
        factors = []
        
        # Always present base uncertainties
        for uncertainty_type, model in self.uncertainty_models.items():
            base_impact = model["base_uncertainty"]
            
            # Adjust impact based on context
            if context:
                if uncertainty_type == UncertaintyType.LINGUISTIC and context.get("language") != "en":
                    base_impact *= 1.5
                elif uncertainty_type == UncertaintyType.CONTEXTUAL and not context.get("context_complete", True):
                    base_impact *= 1.3
                elif uncertainty_type == UncertaintyType.TEMPORAL and context.get("time_sensitive", False):
                    base_impact *= 1.2
            
            factor = UncertaintyFactor(
                factor_type=uncertainty_type,
                description=model["description"],
                impact_magnitude=base_impact,
                mitigation_strategies=model["mitigation"],
                confidence_reduction=base_impact * self.scoring_config["uncertainty_penalty_factor"]
            )
            
            factors.append(factor)
        
        # Context-specific uncertainties
        if context:
            if context.get("ambiguous_input", False):
                factors.append(UncertaintyFactor(
                    factor_type=UncertaintyType.LINGUISTIC,
                    description="Input contains ambiguous language",
                    impact_magnitude=0.15,
                    mitigation_strategies=["request_clarification", "provide_alternatives"],
                    confidence_reduction=0.15
                ))
            
            if context.get("incomplete_information", False):
                factors.append(UncertaintyFactor(
                    factor_type=UncertaintyType.EPISTEMIC,
                    description="Incomplete information provided",
                    impact_magnitude=0.20,
                    mitigation_strategies=["gather_more_information", "make_assumptions_explicit"],
                    confidence_reduction=0.20
                ))
        
        return factors
    
    def _adjust_for_uncertainty(self, components: List[ConfidenceComponent],
                              uncertainty_factors: List[UncertaintyFactor]) -> List[ConfidenceComponent]:
        """Adjust confidence components for uncertainty factors."""
        
        adjusted_components = []
        
        for component in components:
            adjusted_confidence = component.base_confidence
            
            # Apply uncertainty reductions
            for factor in uncertainty_factors:
                if factor.factor_type.value in component.uncertainty_factors:
                    adjusted_confidence -= factor.confidence_reduction
            
            # Apply evidence strength weighting
            evidence_weight = self.scoring_config["evidence_weight_factor"]
            adjusted_confidence = (
                adjusted_confidence * (1 - evidence_weight) +
                component.evidence_strength * adjusted_confidence * evidence_weight
            )
            
            # Apply reliability adjustment
            reliability_adjustment = (component.reliability_score - 0.5) * 0.1
            adjusted_confidence += reliability_adjustment
            
            # Apply temporal decay (if any)
            adjusted_confidence *= (1 - component.temporal_decay)
            
            # Clamp to valid range
            adjusted_confidence = max(0.0, min(1.0, adjusted_confidence))
            
            # Create adjusted component
            adjusted_component = ConfidenceComponent(
                component_id=component.component_id,
                source=component.source,
                base_confidence=adjusted_confidence,
                uncertainty_factors=component.uncertainty_factors,
                evidence_strength=component.evidence_strength,
                reliability_score=component.reliability_score,
                temporal_decay=component.temporal_decay,
                weight=component.weight
            )
            
            adjusted_components.append(adjusted_component)
        
        return adjusted_components
    
    def _determine_aggregation_weights(self, context: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """Determine aggregation weights based on context."""
        
        if not context:
            return self.aggregation_weights["balanced"]
        
        # Context-based weight selection
        task_type = context.get("task_type", "general")
        urgency = context.get("urgency_level", "medium")
        user_preference = context.get("analysis_preference", "balanced")
        
        if task_type == "technical" or urgency in ["high", "critical"]:
            return self.aggregation_weights["logic_heavy"]
        elif task_type == "emotional" or context.get("emotional_context", False):
            return self.aggregation_weights["emotion_aware"]
        elif task_type == "creative" or context.get("innovation_focus", False):
            return self.aggregation_weights["creative_focus"]
        else:
            return self.aggregation_weights["balanced"]
    
    def _aggregate_confidences(self, components: List[ConfidenceComponent],
                             weights: Dict[str, float]) -> float:
        """Aggregate dimensional confidences using specified method."""
        
        method = self.scoring_config["aggregation_method"]
        
        if method == "weighted_arithmetic_mean":
            return self._weighted_arithmetic_mean(components, weights)
        elif method == "weighted_geometric_mean":
            return self._weighted_geometric_mean(components, weights)
        elif method == "weighted_harmonic_mean":
            return self._weighted_harmonic_mean(components, weights)
        else:
            return self._weighted_arithmetic_mean(components, weights)  # Default
    
    def _weighted_arithmetic_mean(self, components: List[ConfidenceComponent],
                                weights: Dict[str, float]) -> float:
        """Calculate weighted arithmetic mean of confidences."""
        
        total_weighted_confidence = 0.0
        total_weight = 0.0
        
        for component in components:
            weight_key = component.component_id.split("_")[0]  # Extract dimension
            weight = weights.get(weight_key, component.weight)
            
            total_weighted_confidence += component.base_confidence * weight
            total_weight += weight
        
        return total_weighted_confidence / total_weight if total_weight > 0 else 0.0
    
    def _weighted_geometric_mean(self, components: List[ConfidenceComponent],
                               weights: Dict[str, float]) -> float:
        """Calculate weighted geometric mean of confidences."""
        
        product = 1.0
        total_weight = 0.0
        
        for component in components:
            weight_key = component.component_id.split("_")[0]
            weight = weights.get(weight_key, component.weight)
            
            # Avoid log(0) by ensuring minimum confidence
            confidence = max(0.01, component.base_confidence)
            product *= confidence ** weight
            total_weight += weight
        
        return product ** (1.0 / total_weight) if total_weight > 0 else 0.0
    
    def _weighted_harmonic_mean(self, components: List[ConfidenceComponent],
                              weights: Dict[str, float]) -> float:
        """Calculate weighted harmonic mean of confidences."""
        
        weighted_reciprocal_sum = 0.0
        total_weight = 0.0
        
        for component in components:
            weight_key = component.component_id.split("_")[0]
            weight = weights.get(weight_key, component.weight)
            
            # Avoid division by zero
            confidence = max(0.01, component.base_confidence)
            weighted_reciprocal_sum += weight / confidence
            total_weight += weight
        
        return total_weight / weighted_reciprocal_sum if weighted_reciprocal_sum > 0 else 0.0
    
    def _apply_calibration(self, confidence: float, context: Optional[Dict[str, Any]]) -> float:
        """Apply confidence calibration to reduce bias."""
        
        if not self.scoring_config["calibration_enabled"]:
            return confidence
        
        # Interpolate calibration curve
        calibrated_confidence = self._interpolate_calibration_curve(confidence)
        
        # Apply bias corrections
        bias_config = self.scoring_config["bias_correction"]
        
        # Overconfidence correction (reduce high confidences slightly)
        if confidence > 0.8:
            calibrated_confidence -= bias_config["overconfidence_correction"]
        
        # Underconfidence correction (boost low confidences slightly)
        if confidence < 0.6:
            calibrated_confidence += bias_config["underconfidence_correction"]
        
        return max(0.0, min(1.0, calibrated_confidence))
    
    def _interpolate_calibration_curve(self, confidence: float) -> float:
        """Interpolate calibration curve to get calibrated confidence."""
        
        curve = self.calibration_params.calibration_curve
        
        # Find surrounding points
        for i in range(len(curve) - 1):
            x1, y1 = curve[i]
            x2, y2 = curve[i + 1]
            
            if x1 <= confidence <= x2:
                # Linear interpolation
                if x2 - x1 == 0:
                    return y1
                
                alpha = (confidence - x1) / (x2 - x1)
                return y1 + alpha * (y2 - y1)
        
        # Extrapolation for edge cases
        if confidence <= curve[0][0]:
            return curve[0][1]
        else:
            return curve[-1][1]
    
    def _calculate_confidence_intervals(self, components: List[ConfidenceComponent]) -> Dict[str, Tuple[float, float]]:
        """Calculate confidence intervals for each component."""
        
        intervals = {}
        alpha = self.scoring_config["confidence_intervals"]["alpha"]
        
        for component in components:
            # Estimate standard error based on confidence and evidence strength
            std_error = (1 - component.evidence_strength) * 0.1
            
            # Calculate margin of error for 95% CI
            margin_of_error = 1.96 * std_error
            
            lower_bound = max(0.0, component.base_confidence - margin_of_error)
            upper_bound = min(1.0, component.base_confidence + margin_of_error)
            
            intervals[component.component_id] = (lower_bound, upper_bound)
        
        return intervals
    
    def _assess_reliability(self, components: List[ConfidenceComponent],
                          uncertainty_factors: List[UncertaintyFactor]) -> Dict[str, float]:
        """Assess reliability of confidence estimates."""
        
        reliability = {}
        
        # Component-level reliability
        for component in components:
            base_reliability = component.reliability_score
            
            # Adjust for uncertainty factors
            uncertainty_penalty = sum(
                factor.impact_magnitude for factor in uncertainty_factors
                if factor.factor_type.value in component.uncertainty_factors
            )
            
            adjusted_reliability = base_reliability - uncertainty_penalty
            reliability[component.component_id] = max(0.0, min(1.0, adjusted_reliability))
        
        # Overall reliability
        reliability["overall"] = np.mean(list(reliability.values()))
        
        return reliability
    
    def _generate_confidence_trajectory(self, components: List[ConfidenceComponent]) -> List[float]:
        """Generate confidence trajectory over processing steps."""
        
        trajectory = []
        
        # Simulate confidence evolution during processing
        for i, component in enumerate(components):
            # Initial confidence (lower due to uncertainty)
            initial_conf = component.base_confidence * 0.7
            
            # Progressive confidence building
            final_conf = component.base_confidence
            
            # Add intermediate points
            steps = 5
            for step in range(steps + 1):
                alpha = step / steps
                conf = initial_conf + alpha * (final_conf - initial_conf)
                trajectory.append(conf)
        
        return trajectory
    
    def _determine_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Determine confidence level classification."""
        
        if confidence >= 0.90:
            return ConfidenceLevel.VERY_HIGH
        elif confidence >= 0.80:
            return ConfidenceLevel.HIGH
        elif confidence >= 0.70:
            return ConfidenceLevel.MEDIUM
        elif confidence >= 0.60:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def _generate_confidence_recommendations(self, breakdown: ConfidenceBreakdown,
                                           uncertainty_factors: List[UncertaintyFactor]) -> List[str]:
        """Generate recommendations based on confidence analysis."""
        
        recommendations = []
        
        # Overall confidence recommendations
        if breakdown.overall_confidence < self.scoring_config["confidence_threshold"]:
            recommendations.append("confidence_below_threshold")
            recommendations.append("provide_alternative_interpretations")
        
        # Component-specific recommendations
        for component in breakdown.component_confidences:
            if component.base_confidence < 0.7:
                recommendations.append(f"improve_{component.component_id}_confidence")
        
        # Uncertainty-based recommendations
        high_impact_uncertainties = [f for f in uncertainty_factors if f.impact_magnitude > 0.1]
        
        for uncertainty in high_impact_uncertainties:
            recommendations.extend(uncertainty.mitigation_strategies)
        
        # Reliability-based recommendations
        if breakdown.reliability_assessment.get("overall", 1.0) < 0.8:
            recommendations.append("enhance_reliability_through_validation")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _perform_uncertainty_analysis(self, uncertainty_factors: List[UncertaintyFactor]) -> Dict[str, Any]:
        """Perform comprehensive uncertainty analysis."""
        
        analysis = {
            "total_uncertainty": sum(f.impact_magnitude for f in uncertainty_factors),
            "dominant_uncertainty": max(uncertainty_factors, key=lambda f: f.impact_magnitude).factor_type.value if uncertainty_factors else None,
            "uncertainty_distribution": {f.factor_type.value: f.impact_magnitude for f in uncertainty_factors},
            "mitigation_priority": sorted(uncertainty_factors, key=lambda f: f.impact_magnitude, reverse=True)[:3],
            "reducible_uncertainty": sum(f.impact_magnitude for f in uncertainty_factors if f.factor_type in [UncertaintyType.EPISTEMIC, UncertaintyType.CONTEXTUAL]),
            "irreducible_uncertainty": sum(f.impact_magnitude for f in uncertainty_factors if f.factor_type == UncertaintyType.ALEATORY)
        }
        
        return analysis


# Example usage
if __name__ == "__main__":
    # Initialize confidence scoring algorithm
    scorer = ConfidenceScoringAlgorithm()
    
    # Test confidence calculation
    result = scorer.calculate_confidence(
        logical_confidence=0.85,
        emotional_confidence=0.78,
        creative_confidence=0.72,
        synthesis_confidence=0.80,
        context={
            "task_type": "technical",
            "urgency_level": "medium",
            "ambiguous_input": False,
            "incomplete_information": False
        }
    )
    
    print(f"Confidence Scoring Results:")
    print(f"Overall confidence: {result.aggregated_confidence:.3f}")
    print(f"Confidence level: {result.confidence_breakdown.confidence_level.value}")
    print(f"Uncertainty factors: {len(result.confidence_breakdown.uncertainty_factors)}")
    print(f"Reliability assessment: {result.confidence_breakdown.reliability_assessment.get('overall', 0):.3f}")
    print(f"Processing time: {result.processing_time_ms:.2f}ms")
    
    print(f"\nDimensional confidences:")
    for dim, conf in result.dimensional_confidences.items():
        print(f"  {dim}: {conf:.3f}")
    
    print(f"\nRecommendations:")
    for rec in result.recommendations[:5]:  # Show top 5
        print(f"  - {rec}")
    
    print(f"\nMeets N.L.D.S. threshold (≥85%): {'Yes' if result.aggregated_confidence >= 0.85 else 'No'}")
