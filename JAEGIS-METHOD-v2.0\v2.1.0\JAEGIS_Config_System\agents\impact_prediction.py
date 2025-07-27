"""
JAEGIS Configuration Management System - Impact Prediction System
Advanced system to predict and display impact of parameter changes before applying them
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import statistics
import json

from ..core.config_schema import FrequencyParameters, AgentTier
from ..core.config_engine import ConfigurationEngine

logger = logging.getLogger(__name__)

@dataclass
class ImpactMetrics:
    """Metrics for measuring impact of parameter changes"""
    performance_delta: float  # Percentage change in performance
    quality_delta: float     # Percentage change in quality
    speed_delta: float       # Percentage change in speed
    resource_delta: float    # Percentage change in resource usage
    complexity_delta: float  # Percentage change in workflow complexity
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "performance_delta": self.performance_delta,
            "quality_delta": self.quality_delta,
            "speed_delta": self.speed_delta,
            "resource_delta": self.resource_delta,
            "complexity_delta": self.complexity_delta
        }

@dataclass
class ImpactPrediction:
    """Complete impact prediction for parameter changes"""
    parameter_name: str
    current_value: Any
    proposed_value: Any
    impact_level: str  # "minimal", "low", "medium", "high", "critical"
    confidence_score: float  # 0.0 to 1.0
    metrics: ImpactMetrics
    estimated_effects: List[str]
    potential_risks: List[str]
    mitigation_suggestions: List[str]
    time_to_effect: str  # "immediate", "short-term", "medium-term", "long-term"
    reversibility: str   # "easily_reversible", "reversible", "difficult_to_reverse"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "parameter_name": self.parameter_name,
            "current_value": self.current_value,
            "proposed_value": self.proposed_value,
            "impact_level": self.impact_level,
            "confidence_score": self.confidence_score,
            "metrics": self.metrics.to_dict(),
            "estimated_effects": self.estimated_effects,
            "potential_risks": self.potential_risks,
            "mitigation_suggestions": self.mitigation_suggestions,
            "time_to_effect": self.time_to_effect,
            "reversibility": self.reversibility
        }

@dataclass
class SystemImpactAnalysis:
    """Analysis of system-wide impact from multiple parameter changes"""
    total_parameters_changed: int
    overall_impact_level: str
    combined_confidence: float
    synergy_effects: List[str]  # Positive interactions between changes
    conflict_effects: List[str]  # Negative interactions between changes
    system_stability_risk: str  # "low", "medium", "high"
    recommended_rollout: str     # "immediate", "gradual", "staged"

class ImpactPredictionSystem:
    """Advanced system for predicting parameter change impacts"""
    
    def __init__(self, config_engine: ConfigurationEngine):
        self.config_engine = config_engine
        
        # Historical data for learning
        self.impact_history: List[Dict[str, Any]] = []
        self.accuracy_metrics: Dict[str, float] = {}
        
        # Parameter interaction models
        self.parameter_correlations = self._initialize_correlations()
        self.impact_models = self._initialize_impact_models()
        
        logger.info("Impact Prediction System initialized")
    
    def _initialize_correlations(self) -> Dict[str, Dict[str, float]]:
        """Initialize parameter correlation matrix""return_research_intensity": {
                "task_decomposition": 0.3,
                "validation_thoroughness": 0.6,
                "documentation_detail0_4_task_decomposition": {
                "research_intensity": 0.3,
                "validation_thoroughness": 0.4,
                "documentation_detail0_5_validation_thoroughness": {
                "research_intensity": 0.6,
                "task_decomposition": 0.4,
                "documentation_detail0_3_documentation_detail": {
                "research_intensity": 0.4,
                "task_decomposition": 0.5,
                "validation_thoroughness": 0.3
            }
        }
    
    def _initialize_impact_models(self) -> Dict[str, Dict[str, Any]]:
        """Initialize impact prediction models for each parameter""return_research_intensity": {
                "performance_weight": 0.7,
                "quality_weight": 0.9,
                "speed_weight": -0.5,
                "resource_weight": 0.6,
                "complexity_weight": 0.3,
                "baseline_impact": 0.5,
                "saturation_point": 85,
                "diminishing_returns0_8_task_decomposition": {
                "performance_weight": 0.5,
                "quality_weight": 0.6,
                "speed_weight": -0.3,
                "resource_weight": 0.4,
                "complexity_weight": 0.8,
                "baseline_impact": 0.4,
                "saturation_point": 80,
                "diminishing_returns0_7_validation_thoroughness": {
                "performance_weight": 0.8,
                "quality_weight": 1.0,
                "speed_weight": -0.7,
                "resource_weight": 0.8,
                "complexity_weight": 0.4,
                "baseline_impact": 0.6,
                "saturation_point": 90,
                "diminishing_returns0_9_documentation_detail": {
                "performance_weight": 0.4,
                "quality_weight": 0.5,
                "speed_weight": -0.2,
                "resource_weight": 0.3,
                "complexity_weight": 0.2,
                "baseline_impact": 0.3,
                "saturation_point": 85,
                "diminishing_returns": 0.6
            }
        }
    
    async def predict_single_parameter_impact(self, parameter_name: str, 
                                            current_value: Any, 
                                            proposed_value: Any) -> ImpactPrediction:
        """Predict impact of changing a single parameter"""
        
        # Calculate change magnitude
        change_magnitude = abs(proposed_value - current_value)
        change_direction = 1 if proposed_value > current_value else -1
        
        # Get impact model for parameter
        model = self.impact_models.get(parameter_name, {})
        if not model:
            # Default model for unknown parameters
            model = {
                "performance_weight": 0.5,
                "quality_weight": 0.5,
                "speed_weight": -0.3,
                "resource_weight": 0.4,
                "complexity_weight": 0.3,
                "baseline_impact": 0.4,
                "saturation_point": 80,
                "diminishing_returns": 0.7
            }
        
        # Calculate impact metrics
        metrics = self._calculate_impact_metrics(
            parameter_name, current_value, proposed_value, change_magnitude, change_direction, model
        )
        
        # Determine impact level
        impact_level = self._determine_impact_level(change_magnitude, metrics)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(parameter_name, change_magnitude)
        
        # Generate effects and risks
        estimated_effects = self._generate_estimated_effects(parameter_name, change_direction, change_magnitude)
        potential_risks = self._generate_potential_risks(parameter_name, change_direction, change_magnitude)
        mitigation_suggestions = self._generate_mitigation_suggestions(parameter_name, potential_risks)
        
        # Determine time to effect and reversibility
        time_to_effect = self._determine_time_to_effect(parameter_name, change_magnitude)
        reversibility = self._determine_reversibility(parameter_name, change_magnitude)
        
        return ImpactPrediction(
            parameter_name=parameter_name,
            current_value=current_value,
            proposed_value=proposed_value,
            impact_level=impact_level,
            confidence_score=confidence_score,
            metrics=metrics,
            estimated_effects=estimated_effects,
            potential_risks=potential_risks,
            mitigation_suggestions=mitigation_suggestions,
            time_to_effect=time_to_effect,
            reversibility=reversibility
        )
    
    def _calculate_impact_metrics(self, parameter_name: str, current_value: int, 
                                proposed_value: int, change_magnitude: int, 
                                change_direction: int, model: Dict[str, Any]) -> ImpactMetrics:
        """Calculate detailed impact metrics"""
        
        # Base impact calculation
        base_impact = (change_magnitude / 100.0) * model["baseline_impact"]
        
        # Apply diminishing returns for high values
        saturation_point = model["saturation_point"]
        if proposed_value > saturation_point:
            diminishing_factor = model["diminishing_returns"]
            excess = proposed_value - saturation_point
            base_impact *= (1.0 - (excess / 100.0) * (1.0 - diminishing_factor))
        
        # Calculate individual metrics
        performance_delta = base_impact * model["performance_weight"] * change_direction
        quality_delta = base_impact * model["quality_weight"] * change_direction
        speed_delta = base_impact * model["speed_weight"] * change_direction
        resource_delta = base_impact * model["resource_weight"] * change_direction
        complexity_delta = base_impact * model["complexity_weight"] * change_direction
        
        # Apply parameter-specific adjustments
        if parameter_name == "research_intensity":
            # Research intensity has non-linear quality benefits
            if change_direction > 0:
                quality_delta *= 1.2
                speed_delta *= 1.3  # More negative impact on speed
        
        elif parameter_name == "validation_thoroughness":
            # Validation has exponential quality benefits but speed costs
            if change_direction > 0:
                quality_delta *= 1.5
                speed_delta *= 1.4
        
        return ImpactMetrics(
            performance_delta=performance_delta * 100,  # Convert to percentage
            quality_delta=quality_delta * 100,
            speed_delta=speed_delta * 100,
            resource_delta=resource_delta * 100,
            complexity_delta=complexity_delta * 100
        )
    
    def _determine_impact_level(self, change_magnitude: int, metrics: ImpactMetrics) -> str:
        """Determine overall impact level"""
        # Calculate weighted impact score
        impact_score = (
            abs(metrics.performance_delta) * 0.3 +
            abs(metrics.quality_delta) * 0.25 +
            abs(metrics.speed_delta) * 0.2 +
            abs(metrics.resource_delta) * 0.15 +
            abs(metrics.complexity_delta) * 0.1
        )
        
        if impact_score < 5:
            return "minimal"
        elif impact_score < 15:
            return "low"
        elif impact_score < 30:
            return "medium"
        elif impact_score < 50:
            return "high"
        else:
            return "critical"
    
    def _calculate_confidence_score(self, parameter_name: str, change_magnitude: int) -> float:
        """Calculate confidence score for prediction"""
        base_confidence = 0.8
        
        # Reduce confidence for larger changes
        magnitude_penalty = min(0.3, change_magnitude / 100.0 * 0.5)
        
        # Adjust based on parameter knowledge
        if parameter_name in self.impact_models:
            knowledge_bonus = 0.1
        else:
            knowledge_bonus = -0.2
        
        # Historical accuracy adjustment
        if parameter_name in self.accuracy_metrics:
            accuracy_adjustment = (self.accuracy_metrics[parameter_name] - 0.5) * 0.2
        else:
            accuracy_adjustment = 0
        
        confidence = base_confidence - magnitude_penalty + knowledge_bonus + accuracy_adjustment
        return max(0.1, min(1.0, confidence))
    
    def _generate_estimated_effects(self, parameter_name: str, change_direction: int, 
                                  change_magnitude: int) -> List[str]:
        """Generate list of estimated effects""effects_eq_effect_templates_eq_research_intensity": {
                "increase": [
                    "More comprehensive information gathering",
                    "Deeper analysis of requirements and constraints",
                    "Better informed decision making",
                    "Increased initial response time",
                    "Higher quality research outputs"
                ],
                "decrease": [
                    "Faster initial responses",
                    "Reduced research overhead",
                    "More streamlined information gathering",
                    "Potentially less comprehensive analysis",
                    "Quicker_project_initiationvalidation_thoroughness": {
                "increase": [
                    "Enhanced quality assurance",
                    "Fewer errors in final outputs",
                    "More comprehensive testing",
                    "Increased processing time",
                    "Better reliability and robustness"
                ],
                "decrease": [
                    "Faster processing and delivery",
                    "Reduced validation overhead",
                    "Streamlined quality checks",
                    "Potential increase in error rates",
                    "Quicker iterations"
                ]
            }
        }
        
        direction_key = "increase" if change_direction > 0 else "decrease"
        templates = effect_templates.get(parameter_name, {}).get(direction_key, [])
        
        # Select effects based on change magnitude
        num_effects = min(len(templates), max(2, change_magnitude // 15))
        effects = templates[:num_effects]
        
        return effects
    
    def _generate_potential_risks(self, parameter_name: str, change_direction: int, 
                                change_magnitude: int) -> List[str]:
        """Generate list of potential risks"""
        risks = []
        
        if change_magnitude > 30:
            risks.append("Large parameter change may cause workflow disruption")
        
        if parameter_name == "research_intensity" and change_direction > 0 and change_magnitude > 20:
            risks.append("Significantly increased response times")
            risks.append("Potential analysis paralysis")
        
        if parameter_name == "validation_thoroughness" and change_direction < 0 and change_magnitude > 25:
            risks.append("Reduced quality assurance may lead to errors")
            risks.append("Potential decrease in output reliability")
        
        return risks
    
    def _generate_mitigation_suggestions(self, parameter_name: str, risks: List[str]) -> List[str]:
        """Generate mitigation suggestions for identified risks"""
        suggestions = []
        
        if "workflow disruption" in " ".join(risks).lower():
            suggestions.append("Consider implementing changes gradually")
            suggestions.append("Monitor system performance closely after changes")
        
        if "response times" in " ".join(risks).lower():
            suggestions.append("Adjust expectations for initial response delays")
            suggestions.append("Consider balancing with speed-optimized parameters")
        
        if "quality" in " ".join(risks).lower():
            suggestions.append("Implement additional manual quality checks")
            suggestions.append("Consider increasing validation in other areas")
        
        return suggestions
    
    def _determine_time_to_effect(self, parameter_name: str, change_magnitude: int) -> str:
        """Determine how quickly changes will take effect"""
        if change_magnitude < 10:
            return "immediate"
        elif change_magnitude < 25:
            return "short-term"
        elif change_magnitude < 40:
            return "medium-term"
        else:
            return "long-term"
    
    def _determine_reversibility(self, parameter_name: str, change_magnitude: int) -> str:
        """Determine how easily changes can be reversed"""
        if change_magnitude < 15:
            return "easily_reversible"
        elif change_magnitude < 35:
            return "reversible"
        else:
            return "difficult_to_reverse"
    
    async def predict_system_impact(self, parameter_changes: Dict[str, Tuple[Any, Any]]) -> SystemImpactAnalysis:
        """Predict system-wide impact of multiple parameter changes"""
        
        individual_predictions = []
        for param_name, (current_val, proposed_val) in parameter_changes.items():
            prediction = await self.predict_single_parameter_impact(param_name, current_val, proposed_val)
            individual_predictions.append(prediction)
        
        # Analyze interactions between parameters
        synergy_effects = self._analyze_synergies(individual_predictions)
        conflict_effects = self._analyze_conflicts(individual_predictions)
        
        # Calculate overall impact
        overall_impact_level = self._calculate_overall_impact(individual_predictions)
        combined_confidence = statistics.mean([p.confidence_score for p in individual_predictions])
        
        # Assess system stability risk
        stability_risk = self._assess_stability_risk(individual_predictions, conflict_effects)
        
        # Recommend rollout strategy
        recommended_rollout = self._recommend_rollout_strategy(overall_impact_level, stability_risk)
        
        return SystemImpactAnalysis(
            total_parameters_changed=len(parameter_changes),
            overall_impact_level=overall_impact_level,
            combined_confidence=combined_confidence,
            synergy_effects=synergy_effects,
            conflict_effects=conflict_effects,
            system_stability_risk=stability_risk,
            recommended_rollout=recommended_rollout
        )
    
    def _analyze_synergies(self, predictions: List[ImpactPrediction]) -> List[str]:
        """Analyze positive interactions between parameter changes"""
        synergies = []
        
        param_names = [p.parameter_name for p in predictions]
        
        # Check for known synergistic combinations
        if "research_intensity" in param_names and "validation_thoroughness" in param_names:
            synergies.append("Research and validation improvements work together for higher quality")
        
        if "task_decomposition" in param_names and "documentation_detail" in param_names:
            synergies.append("Better task breakdown enhances documentation effectiveness")
        
        return synergies
    
    def _analyze_conflicts(self, predictions: List[ImpactPrediction]) -> List[str]:
        """Analyze negative interactions between parameter changes"""
        conflicts = []
        
        # Check for conflicting directions
        speed_impacts = [p.metrics.speed_delta for p in predictions]
        if any(impact < -20 for impact in speed_impacts) and len(speed_impacts) > 2:
            conflicts.append("Multiple parameters negatively impact speed simultaneously")
        
        return conflicts
    
    def _calculate_overall_impact(self, predictions: List[ImpactPrediction]) -> str:
        """Calculate overall system impact level"""
        impact_scores = {
            "minimal": 1, "low": 2, "medium": 3, "high": 4, "critical": 5
        }
        
        scores = [impact_scores[p.impact_level] for p in predictions]
        avg_score = statistics.mean(scores)
        
        if avg_score < 1.5:
            return "minimal"
        elif avg_score < 2.5:
            return "low"
        elif avg_score < 3.5:
            return "medium"
        elif avg_score < 4.5:
            return "high"
        else:
            return "critical"
    
    def _assess_stability_risk(self, predictions: List[ImpactPrediction], conflicts: List[str]) -> str:
        """Assess system stability risk"""
        if len(conflicts) > 2:
            return "high"
        elif len(conflicts) > 0:
            return "medium"
        else:
            return "low"
    
    def _recommend_rollout_strategy(self, impact_level: str, stability_risk: str) -> str:
        """Recommend rollout strategy based on impact and risk"""
        if impact_level in ["critical", "high"] or stability_risk == "high":
            return "staged"
        elif impact_level == "medium" or stability_risk == "medium":
            return "gradual"
        else:
            return "immediate"
    
    def record_actual_impact(self, parameter_name: str, predicted_impact: ImpactPrediction, 
                           actual_metrics: Dict[str, float]):
        """Record actual impact to improve future predictions"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "parameter_name": parameter_name,
            "predicted": predicted_impact.to_dict(),
            "actual": actual_metrics
        }
        
        self.impact_history.append(record)
        
        # Update accuracy metrics
        self._update_accuracy_metrics(parameter_name, predicted_impact, actual_metrics)
    
    def _update_accuracy_metrics(self, parameter_name: str, predicted: ImpactPrediction, 
                               actual: Dict[str, float]):
        """Update accuracy metrics for future predictions"""
        # Calculate prediction accuracy
        predicted_metrics = predicted.metrics.to_dict()
        
        accuracy_scores = []
        for metric_name in ["performance_delta", "quality_delta", "speed_delta"]:
            if metric_name in actual and metric_name in predicted_metrics:
                predicted_val = predicted_metrics[metric_name]
                actual_val = actual[metric_name]
                
                if predicted_val != 0:
                    accuracy = 1.0 - abs(predicted_val - actual_val) / abs(predicted_val)
                    accuracy_scores.append(max(0.0, accuracy))
        
        if accuracy_scores:
            avg_accuracy = statistics.mean(accuracy_scores)
            
            if parameter_name not in self.accuracy_metrics:
                self.accuracy_metrics[parameter_name] = avg_accuracy
            else:
                # Exponential moving average
                self.accuracy_metrics[parameter_name] = (
                    0.7 * self.accuracy_metrics[parameter_name] + 0.3 * avg_accuracy
                )
    
    def get_prediction_statistics(self) -> Dict[str, Any]:
        """Get statistics about prediction accuracy and usage"""
        return {
            "total_predictions": len(self.impact_history),
            "accuracy_metrics": self.accuracy_metrics.copy(),
            "parameters_tracked": len(self.accuracy_metrics),
            "average_accuracy": statistics.mean(self.accuracy_metrics.values()) if self.accuracy_metrics else 0.0
        }
