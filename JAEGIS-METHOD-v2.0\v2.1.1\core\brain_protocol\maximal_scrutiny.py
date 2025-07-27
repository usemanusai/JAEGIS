"""
JAEGIS Brain Protocol Suite v1.0 - Path of Maximal Scrutiny Protocol
Mandate 2.5: Anti-shiny object syndrome with comprehensive impact analysis

This module implements the mandatory maximal scrutiny protocol that provides
anti-shiny object syndrome protection by requiring comprehensive impact analysis
for any proposed deviation from the current strategic path.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class DeviationType(str, Enum):
    """Types of strategic deviations."""
    SCOPE_EXPANSION = "scope_expansion"
    TECHNOLOGY_CHANGE = "technology_change"
    PRIORITY_SHIFT = "priority_shift"
    RESOURCE_REALLOCATION = "resource_reallocation"
    TIMELINE_EXTENSION = "timeline_extension"
    FEATURE_ADDITION = "feature_addition"
    ARCHITECTURE_CHANGE = "architecture_change"
    PROCESS_MODIFICATION = "process_modification"


class ImpactSeverity(str, Enum):
    """Severity levels for impact analysis."""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"


class ScrutinyLevel(str, Enum):
    """Levels of scrutiny required."""
    STANDARD = "standard"
    ELEVATED = "elevated"
    HIGH = "high"
    MAXIMUM = "maximum"
    ABSOLUTE = "absolute"


@dataclass
class ImpactDimension:
    """Impact analysis dimension."""
    dimension_id: str
    dimension_name: str
    current_state: str
    proposed_state: str
    impact_description: str
    severity: ImpactSeverity
    mitigation_strategies: List[str]
    risk_factors: List[str]


@dataclass
class ScrutinyAnalysis:
    """Comprehensive scrutiny analysis result."""
    analysis_id: str
    proposed_deviation: str
    deviation_type: DeviationType
    scrutiny_level: ScrutinyLevel
    impact_dimensions: List[ImpactDimension]
    overall_impact_score: float
    strategic_cost: float
    opportunity_cost: float
    risk_assessment: str
    recommendation: str
    approval_required: bool
    stakeholder_review_needed: bool
    analyzed_at: float


@dataclass
class ShinyObjectDetection:
    """Shiny object syndrome detection result."""
    detection_id: str
    trigger_description: str
    shiny_object_indicators: List[str]
    distraction_risk: float
    strategic_misalignment: float
    novelty_bias_score: float
    complexity_inflation: float
    detection_confidence: float
    detected_at: float


class MaximalScrutinyEngine:
    """
    JAEGIS Brain Protocol Suite Maximal Scrutiny Engine
    
    Implements Mandate 2.5: Path of Maximal Scrutiny Protocol
    
    Mandatory execution sequence:
    1. Detect Shiny Objects - Identify potential distractions and scope creep
    2. Force Impact Analysis - Comprehensive analysis of proposed deviations
    3. Apply Maximal Scrutiny - Require explicit justification for deviations
    """
    
    def __init__(self):
        self.scrutiny_history: List[ScrutinyAnalysis] = []
        self.shiny_object_detections: List[ShinyObjectDetection] = []
        
        # Scrutiny thresholds
        self.scrutiny_thresholds = {
            "minimal_impact": 0.2,
            "low_impact": 0.4,
            "moderate_impact": 0.6,
            "high_impact": 0.8,
            "critical_impact": 0.9
        }
        
        # Shiny object indicators
        self.shiny_object_patterns = {
            "novelty_keywords": [
                "new", "latest", "cutting-edge", "revolutionary", "breakthrough",
                "innovative", "next-generation", "state-of-the-art", "advanced"
            ],
            "scope_expansion_keywords": [
                "also", "additionally", "while we're at it", "might as well",
                "quick addition", "small enhancement", "easy win"
            ],
            "complexity_keywords": [
                "comprehensive", "complete", "full-featured", "enterprise-grade",
                "scalable", "robust", "sophisticated", "advanced"
            ],
            "urgency_keywords": [
                "urgent", "critical", "must-have", "essential", "vital",
                "crucial", "immediate", "priority"
            ]
        }
        
        # Impact analysis dimensions
        self.impact_dimensions = [
            "timeline_impact",
            "resource_impact",
            "complexity_impact",
            "risk_impact",
            "strategic_impact",
            "technical_debt_impact",
            "maintenance_impact",
            "integration_impact"
        ]
        
        logger.info("Maximal Scrutiny Engine initialized")
    
    async def mandatory_deviation_scrutiny(self, proposed_deviation: str, 
                                         current_context: str) -> ScrutinyAnalysis:
        """
        MANDATORY: Apply maximal scrutiny to proposed deviations
        
        This method MUST be called whenever a proposed action represents a
        deviation from the current strategic path to prevent shiny object syndrome.
        """
        
        analysis_id = f"scrutiny_{int(time.time())}"
        
        logger.info(f"🔍 MANDATORY DEVIATION SCRUTINY - Analysis ID: {analysis_id}")
        logger.info(f"📝 Proposed Deviation: {proposed_deviation[:100]}...")
        
        # Step 1: Detect shiny object syndrome
        shiny_detection = await self._detect_shiny_object_syndrome(
            proposed_deviation, current_context
        )
        
        # Step 2: Classify deviation type
        deviation_type = await self._classify_deviation_type(proposed_deviation)
        
        # Step 3: Determine required scrutiny level
        scrutiny_level = await self._determine_scrutiny_level(
            proposed_deviation, shiny_detection, deviation_type
        )
        
        # Step 4: Perform comprehensive impact analysis
        impact_dimensions = await self._perform_impact_analysis(
            proposed_deviation, current_context, deviation_type
        )
        
        # Step 5: Calculate impact scores
        overall_impact_score = await self._calculate_overall_impact(impact_dimensions)
        strategic_cost = await self._calculate_strategic_cost(proposed_deviation, impact_dimensions)
        opportunity_cost = await self._calculate_opportunity_cost(proposed_deviation)
        
        # Step 6: Generate risk assessment
        risk_assessment = await self._generate_risk_assessment(
            impact_dimensions, overall_impact_score, shiny_detection
        )
        
        # Step 7: Generate recommendation
        recommendation = await self._generate_scrutiny_recommendation(
            proposed_deviation, overall_impact_score, strategic_cost, 
            opportunity_cost, shiny_detection
        )
        
        # Step 8: Determine approval requirements
        approval_required, stakeholder_review = await self._determine_approval_requirements(
            scrutiny_level, overall_impact_score, strategic_cost
        )
        
        # Create scrutiny analysis
        analysis = ScrutinyAnalysis(
            analysis_id=analysis_id,
            proposed_deviation=proposed_deviation,
            deviation_type=deviation_type,
            scrutiny_level=scrutiny_level,
            impact_dimensions=impact_dimensions,
            overall_impact_score=overall_impact_score,
            strategic_cost=strategic_cost,
            opportunity_cost=opportunity_cost,
            risk_assessment=risk_assessment,
            recommendation=recommendation,
            approval_required=approval_required,
            stakeholder_review_needed=stakeholder_review,
            analyzed_at=time.time()
        )
        
        # Store analysis
        self.scrutiny_history.append(analysis)
        if shiny_detection:
            self.shiny_object_detections.append(shiny_detection)
        
        logger.info(f"🔍 Deviation scrutiny complete:")
        logger.info(f"  Scrutiny Level: {scrutiny_level.value}")
        logger.info(f"  Overall Impact: {overall_impact_score:.1%}")
        logger.info(f"  Strategic Cost: {strategic_cost:.1%}")
        logger.info(f"  Approval Required: {'✅ YES' if approval_required else '❌ NO'}")
        logger.info(f"  Recommendation: {recommendation[:100]}...")
        
        return analysis
    
    async def _detect_shiny_object_syndrome(self, proposed_deviation: str, 
                                          current_context: str) -> Optional[ShinyObjectDetection]:
        """Detect potential shiny object syndrome."""
        
        detection_id = f"shiny_{int(time.time())}"
        indicators = []
        
        deviation_lower = proposed_deviation.lower()
        
        # Check for novelty bias
        novelty_score = 0.0
        for keyword in self.shiny_object_patterns["novelty_keywords"]:
            if keyword in deviation_lower:
                indicators.append(f"Novelty keyword: {keyword}")
                novelty_score += 0.2
        
        # Check for scope expansion
        scope_score = 0.0
        for keyword in self.shiny_object_patterns["scope_expansion_keywords"]:
            if keyword in deviation_lower:
                indicators.append(f"Scope expansion: {keyword}")
                scope_score += 0.3
        
        # Check for complexity inflation
        complexity_score = 0.0
        for keyword in self.shiny_object_patterns["complexity_keywords"]:
            if keyword in deviation_lower:
                indicators.append(f"Complexity inflation: {keyword}")
                complexity_score += 0.25
        
        # Check for artificial urgency
        urgency_score = 0.0
        for keyword in self.shiny_object_patterns["urgency_keywords"]:
            if keyword in deviation_lower:
                indicators.append(f"Artificial urgency: {keyword}")
                urgency_score += 0.15
        
        # Calculate distraction risk
        distraction_risk = min(1.0, (novelty_score + scope_score + complexity_score + urgency_score) / 4)
        
        # Calculate strategic misalignment (simplified)
        strategic_misalignment = 0.5 if scope_score > 0.3 else 0.2
        
        # Calculate detection confidence
        detection_confidence = min(1.0, len(indicators) * 0.2)
        
        # Only create detection if significant risk
        if distraction_risk > 0.3 or len(indicators) > 2:
            return ShinyObjectDetection(
                detection_id=detection_id,
                trigger_description=proposed_deviation,
                shiny_object_indicators=indicators,
                distraction_risk=distraction_risk,
                strategic_misalignment=strategic_misalignment,
                novelty_bias_score=novelty_score,
                complexity_inflation=complexity_score,
                detection_confidence=detection_confidence,
                detected_at=time.time()
            )
        
        return None
    
    async def _classify_deviation_type(self, proposed_deviation: str) -> DeviationType:
        """Classify the type of deviation."""
        
        deviation_lower = proposed_deviation.lower()
        
        # Classification keywords
        type_keywords = {
            DeviationType.SCOPE_EXPANSION: ["add", "include", "expand", "extend", "enhance"],
            DeviationType.TECHNOLOGY_CHANGE: ["technology", "framework", "library", "tool", "platform"],
            DeviationType.PRIORITY_SHIFT: ["priority", "urgent", "critical", "important", "first"],
            DeviationType.RESOURCE_REALLOCATION: ["resource", "team", "budget", "time", "allocation"],
            DeviationType.TIMELINE_EXTENSION: ["timeline", "deadline", "schedule", "delay", "extend"],
            DeviationType.FEATURE_ADDITION: ["feature", "functionality", "capability", "option"],
            DeviationType.ARCHITECTURE_CHANGE: ["architecture", "design", "structure", "pattern"],
            DeviationType.PROCESS_MODIFICATION: ["process", "workflow", "procedure", "method"]
        }
        
        # Score each type
        type_scores = {}
        for dev_type, keywords in type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in deviation_lower)
            if score > 0:
                type_scores[dev_type] = score
        
        # Return highest scoring type or default
        if type_scores:
            return max(type_scores.items(), key=lambda x: x[1])[0]
        else:
            return DeviationType.SCOPE_EXPANSION  # Default
    
    async def _determine_scrutiny_level(self, proposed_deviation: str,
                                      shiny_detection: Optional[ShinyObjectDetection],
                                      deviation_type: DeviationType) -> ScrutinyLevel:
        """Determine required level of scrutiny."""
        
        base_scrutiny = ScrutinyLevel.STANDARD
        
        # Escalate based on shiny object detection
        if shiny_detection:
            if shiny_detection.distraction_risk > 0.7:
                base_scrutiny = ScrutinyLevel.ABSOLUTE
            elif shiny_detection.distraction_risk > 0.5:
                base_scrutiny = ScrutinyLevel.MAXIMUM
            elif shiny_detection.distraction_risk > 0.3:
                base_scrutiny = ScrutinyLevel.HIGH
        
        # Escalate based on deviation type
        high_risk_types = [
            DeviationType.ARCHITECTURE_CHANGE,
            DeviationType.TECHNOLOGY_CHANGE,
            DeviationType.SCOPE_EXPANSION
        ]
        
        if deviation_type in high_risk_types:
            if base_scrutiny == ScrutinyLevel.STANDARD:
                base_scrutiny = ScrutinyLevel.ELEVATED
        
        return base_scrutiny
    
    async def _perform_impact_analysis(self, proposed_deviation: str, current_context: str,
                                     deviation_type: DeviationType) -> List[ImpactDimension]:
        """Perform comprehensive impact analysis."""
        
        impact_dimensions = []
        
        for dimension_name in self.impact_dimensions:
            dimension = await self._analyze_impact_dimension(
                proposed_deviation, current_context, deviation_type, dimension_name
            )
            impact_dimensions.append(dimension)
        
        return impact_dimensions
    
    async def _analyze_impact_dimension(self, proposed_deviation: str, current_context: str,
                                      deviation_type: DeviationType, dimension_name: str) -> ImpactDimension:
        """Analyze a specific impact dimension."""
        
        dimension_id = f"{dimension_name}_{int(time.time())}"
        
        # Simplified impact analysis based on dimension
        impact_assessments = {
            "timeline_impact": {
                "current_state": "On track for Q1 2024 completion",
                "proposed_state": "May require timeline extension",
                "severity": ImpactSeverity.MODERATE,
                "description": "Proposed deviation may impact delivery timeline"
            },
            "resource_impact": {
                "current_state": "Resources allocated to core objectives",
                "proposed_state": "Resources diverted to new initiative",
                "severity": ImpactSeverity.HIGH,
                "description": "Resource reallocation required for deviation"
            },
            "complexity_impact": {
                "current_state": "Manageable system complexity",
                "proposed_state": "Increased system complexity",
                "severity": ImpactSeverity.MODERATE,
                "description": "Additional complexity introduced"
            },
            "risk_impact": {
                "current_state": "Controlled risk profile",
                "proposed_state": "Elevated risk profile",
                "severity": ImpactSeverity.HIGH,
                "description": "New risks introduced by deviation"
            },
            "strategic_impact": {
                "current_state": "Aligned with strategic roadmap",
                "proposed_state": "Potential strategic misalignment",
                "severity": ImpactSeverity.HIGH,
                "description": "May deviate from strategic objectives"
            },
            "technical_debt_impact": {
                "current_state": "Manageable technical debt",
                "proposed_state": "Increased technical debt",
                "severity": ImpactSeverity.MODERATE,
                "description": "Additional technical debt accumulation"
            },
            "maintenance_impact": {
                "current_state": "Current maintenance overhead",
                "proposed_state": "Increased maintenance requirements",
                "severity": ImpactSeverity.LOW,
                "description": "Additional maintenance burden"
            },
            "integration_impact": {
                "current_state": "Stable integration points",
                "proposed_state": "New integration complexity",
                "severity": ImpactSeverity.MODERATE,
                "description": "Integration challenges introduced"
            }
        }
        
        assessment = impact_assessments.get(dimension_name, {
            "current_state": "Unknown",
            "proposed_state": "Unknown",
            "severity": ImpactSeverity.MODERATE,
            "description": "Impact assessment needed"
        })
        
        # Generate mitigation strategies
        mitigation_strategies = await self._generate_mitigation_strategies(dimension_name, assessment["severity"])
        
        # Identify risk factors
        risk_factors = await self._identify_dimension_risks(dimension_name, deviation_type)
        
        return ImpactDimension(
            dimension_id=dimension_id,
            dimension_name=dimension_name,
            current_state=assessment["current_state"],
            proposed_state=assessment["proposed_state"],
            impact_description=assessment["description"],
            severity=assessment["severity"],
            mitigation_strategies=mitigation_strategies,
            risk_factors=risk_factors
        )
    
    async def _generate_mitigation_strategies(self, dimension_name: str, severity: ImpactSeverity) -> List[str]:
        """Generate mitigation strategies for impact dimension."""
        
        strategies = {
            "timeline_impact": [
                "Implement phased delivery approach",
                "Identify critical path dependencies",
                "Allocate buffer time for integration"
            ],
            "resource_impact": [
                "Assess resource availability",
                "Consider external resources",
                "Prioritize critical components"
            ],
            "complexity_impact": [
                "Implement modular design",
                "Maintain clear interfaces",
                "Document architectural decisions"
            ],
            "risk_impact": [
                "Conduct risk assessment",
                "Implement risk monitoring",
                "Develop contingency plans"
            ]
        }
        
        return strategies.get(dimension_name, ["Develop specific mitigation plan"])
    
    async def _identify_dimension_risks(self, dimension_name: str, deviation_type: DeviationType) -> List[str]:
        """Identify risks for specific dimension."""
        
        risks = {
            "timeline_impact": ["Schedule slippage", "Dependency delays", "Resource conflicts"],
            "resource_impact": ["Resource shortage", "Skill gaps", "Budget overrun"],
            "complexity_impact": ["Integration failures", "Maintenance burden", "Performance degradation"],
            "strategic_impact": ["Scope creep", "Objective misalignment", "Stakeholder confusion"]
        }
        
        return risks.get(dimension_name, ["Unidentified risks"])
    
    async def _calculate_overall_impact(self, impact_dimensions: List[ImpactDimension]) -> float:
        """Calculate overall impact score."""
        
        severity_scores = {
            ImpactSeverity.MINIMAL: 0.1,
            ImpactSeverity.LOW: 0.3,
            ImpactSeverity.MODERATE: 0.5,
            ImpactSeverity.HIGH: 0.8,
            ImpactSeverity.CRITICAL: 0.9,
            ImpactSeverity.CATASTROPHIC: 1.0
        }
        
        total_score = sum(severity_scores[dim.severity] for dim in impact_dimensions)
        return total_score / len(impact_dimensions) if impact_dimensions else 0.0
    
    async def _calculate_strategic_cost(self, proposed_deviation: str, 
                                      impact_dimensions: List[ImpactDimension]) -> float:
        """Calculate strategic cost of deviation."""
        
        # Find strategic impact dimension
        strategic_dims = [dim for dim in impact_dimensions if "strategic" in dim.dimension_name]
        
        if strategic_dims:
            strategic_dim = strategic_dims[0]
            severity_scores = {
                ImpactSeverity.MINIMAL: 0.1,
                ImpactSeverity.LOW: 0.2,
                ImpactSeverity.MODERATE: 0.4,
                ImpactSeverity.HIGH: 0.7,
                ImpactSeverity.CRITICAL: 0.9,
                ImpactSeverity.CATASTROPHIC: 1.0
            }
            return severity_scores[strategic_dim.severity]
        
        return 0.5  # Default moderate cost
    
    async def _calculate_opportunity_cost(self, proposed_deviation: str) -> float:
        """Calculate opportunity cost of pursuing deviation."""
        
        # Simplified opportunity cost calculation
        # In practice, this would analyze what strategic objectives are delayed
        
        deviation_lower = proposed_deviation.lower()
        
        # High opportunity cost indicators
        if any(word in deviation_lower for word in ["new", "additional", "extra", "bonus"]):
            return 0.7
        
        # Medium opportunity cost
        if any(word in deviation_lower for word in ["enhance", "improve", "optimize"]):
            return 0.4
        
        # Low opportunity cost
        return 0.2
    
    async def _generate_risk_assessment(self, impact_dimensions: List[ImpactDimension],
                                      overall_impact: float, 
                                      shiny_detection: Optional[ShinyObjectDetection]) -> str:
        """Generate comprehensive risk assessment."""
        
        risk_level = "LOW"
        
        if overall_impact > 0.8:
            risk_level = "CRITICAL"
        elif overall_impact > 0.6:
            risk_level = "HIGH"
        elif overall_impact > 0.4:
            risk_level = "MODERATE"
        
        risk_factors = []
        for dim in impact_dimensions:
            if dim.severity in [ImpactSeverity.HIGH, ImpactSeverity.CRITICAL]:
                risk_factors.extend(dim.risk_factors)
        
        assessment = f"Risk Level: {risk_level}. "
        
        if shiny_detection and shiny_detection.distraction_risk > 0.5:
            assessment += "High distraction risk detected. "
        
        if risk_factors:
            assessment += f"Key risks: {', '.join(risk_factors[:3])}."
        
        return assessment
    
    async def _generate_scrutiny_recommendation(self, proposed_deviation: str,
                                              overall_impact: float, strategic_cost: float,
                                              opportunity_cost: float,
                                              shiny_detection: Optional[ShinyObjectDetection]) -> str:
        """Generate scrutiny recommendation."""
        
        if overall_impact > 0.8 or strategic_cost > 0.7:
            return "REJECT: High impact and strategic cost. Recommend focusing on core objectives."
        
        if shiny_detection and shiny_detection.distraction_risk > 0.6:
            return "DEFER: Potential shiny object syndrome detected. Recommend completing current priorities first."
        
        if overall_impact > 0.6:
            return "CONDITIONAL APPROVAL: Moderate impact. Require detailed implementation plan and risk mitigation."
        
        if overall_impact > 0.4:
            return "REVIEW REQUIRED: Some impact detected. Recommend stakeholder review before proceeding."
        
        return "APPROVE: Low impact. Proceed with caution and monitoring."
    
    async def _determine_approval_requirements(self, scrutiny_level: ScrutinyLevel,
                                             overall_impact: float, strategic_cost: float) -> Tuple[bool, bool]:
        """Determine approval and review requirements."""
        
        approval_required = False
        stakeholder_review = False
        
        # Require approval for high scrutiny levels
        if scrutiny_level in [ScrutinyLevel.MAXIMUM, ScrutinyLevel.ABSOLUTE]:
            approval_required = True
            stakeholder_review = True
        
        # Require approval for high impact
        if overall_impact > 0.7 or strategic_cost > 0.6:
            approval_required = True
        
        # Require stakeholder review for moderate impact
        if overall_impact > 0.5 or strategic_cost > 0.4:
            stakeholder_review = True
        
        return approval_required, stakeholder_review
    
    def get_scrutiny_status(self) -> Dict[str, Any]:
        """Get comprehensive scrutiny engine status."""
        
        recent_analyses = len([a for a in self.scrutiny_history if time.time() - a.analyzed_at < 3600])
        recent_detections = len([d for d in self.shiny_object_detections if time.time() - d.detected_at < 3600])
        
        approval_rate = len([a for a in self.scrutiny_history if not a.approval_required]) / len(self.scrutiny_history) if self.scrutiny_history else 0
        
        return {
            "total_scrutiny_analyses": len(self.scrutiny_history),
            "recent_analyses_1h": recent_analyses,
            "shiny_object_detections": len(self.shiny_object_detections),
            "recent_detections_1h": recent_detections,
            "approval_not_required_rate": approval_rate,
            "average_impact_score": sum(a.overall_impact_score for a in self.scrutiny_history) / len(self.scrutiny_history) if self.scrutiny_history else 0,
            "average_strategic_cost": sum(a.strategic_cost for a in self.scrutiny_history) / len(self.scrutiny_history) if self.scrutiny_history else 0
        }


# Global maximal scrutiny engine
MAXIMAL_SCRUTINY_ENGINE = MaximalScrutinyEngine()


async def mandatory_scrutiny_analysis(proposed_deviation: str, current_context: str) -> ScrutinyAnalysis:
    """
    MANDATORY: Apply maximal scrutiny to proposed deviations
    
    This function MUST be called whenever a proposed action represents a
    deviation from the current strategic path according to JAEGIS Brain Protocol Suite Mandate 2.5.
    """
    
    return await MAXIMAL_SCRUTINY_ENGINE.mandatory_deviation_scrutiny(proposed_deviation, current_context)


# Example usage
async def main():
    """Example usage of Maximal Scrutiny Engine."""
    
    print("🔍 JAEGIS BRAIN PROTOCOL SUITE - MAXIMAL SCRUTINY TEST")
    
    # Test scrutiny analysis
    deviation = "Add comprehensive machine learning capabilities to enhance the system with cutting-edge AI features"
    context = "Currently implementing JAEGIS Brain Protocol Suite v1.0 with focus on core operational directives"
    
    analysis = await MAXIMAL_SCRUTINY_ENGINE.mandatory_deviation_scrutiny(deviation, context)
    
    print(f"\n🔍 Scrutiny Analysis Results:")
    print(f"  Analysis ID: {analysis.analysis_id}")
    print(f"  Deviation Type: {analysis.deviation_type.value}")
    print(f"  Scrutiny Level: {analysis.scrutiny_level.value}")
    print(f"  Overall Impact: {analysis.overall_impact_score:.1%}")
    print(f"  Strategic Cost: {analysis.strategic_cost:.1%}")
    print(f"  Approval Required: {'✅ YES' if analysis.approval_required else '❌ NO'}")
    print(f"  Recommendation: {analysis.recommendation}")
    
    # Show impact dimensions
    print(f"\n📊 Impact Analysis:")
    for dim in analysis.impact_dimensions[:3]:
        print(f"  {dim.dimension_name}: {dim.severity.value}")
        print(f"    {dim.impact_description}")
    
    # Get status
    status = MAXIMAL_SCRUTINY_ENGINE.get_scrutiny_status()
    print(f"\n📊 Scrutiny Engine Status:")
    print(f"  Total Analyses: {status['total_scrutiny_analyses']}")
    print(f"  Shiny Object Detections: {status['shiny_object_detections']}")
    print(f"  Average Impact: {status['average_impact_score']:.1%}")


if __name__ == "__main__":
    asyncio.run(main())
