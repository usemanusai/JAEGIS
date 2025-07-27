"""
N.L.D.S. Processing Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Complete three-dimensional processing pipeline integrating all Phase 3 components:
- Logical Analysis Engine
- Emotional Context Analyzer
- Creative Interpretation Module
- Dimensional Synthesis Engine
- Confidence Scoring Algorithms
- Dimensional Validation Framework
"""

from .logical_analyzer import (
    LogicalAnalysisEngine,
    LogicalRequirement,
    LogicalStatement,
    LogicalStructure,
    LogicalAnalysisResult,
    RequirementType,
    LogicalOperator,
    LogicalRelation,
    LogicalUtils
)

from .emotional_analyzer import (
    EmotionalAnalysisEngine,
    EmotionType,
    SentimentPolarity,
    EmotionalIntensity,
    UserState,
    EmotionScore,
    SentimentAnalysis,
    EmotionalContext,
    EmotionalAnalysisResult,
    EmotionalUtils
)

from .creative_interpreter import (
    CreativeInterpretationEngine,
    CreativityType,
    InnovationLevel,
    CreativePattern,
    CreativeIdea,
    AlternativeApproach,
    CreativeConnection,
    CreativeAnalysisResult,
    CreativeUtils
)

from .dimensional_synthesizer import (
    DimensionalSynthesisEngine,
    DimensionWeight,
    SynthesisQuality,
    ConflictType,
    DimensionalInsight,
    SynthesisConflict,
    DimensionalRecommendation,
    DimensionalSynthesisResult,
    SynthesisUtils
)

from .confidence_scorer import (
    ConfidenceScoringEngine,
    ConfidenceLevel,
    UncertaintyType,
    ConfidenceSource,
    ConfidenceMetric,
    UncertaintyQuantification,
    ConfidenceScoringResult,
    ConfidenceUtils
)

from .dimensional_validator import (
    DimensionalValidationEngine,
    ValidationStatus,
    ValidationCategory,
    ValidationSeverity,
    ValidationCheck,
    ValidationRule,
    DimensionalValidationResult,
    ValidationUtils
)

# Version information
__version__ = "2.2.0"
__author__ = "JAEGIS Development Team"
__description__ = "N.L.D.S. Three-Dimensional Processing Module"

# Export all components
__all__ = [
    # Logical Analysis
    "LogicalAnalysisEngine",
    "LogicalRequirement",
    "LogicalStatement",
    "LogicalStructure",
    "LogicalAnalysisResult",
    "RequirementType",
    "LogicalOperator",
    "LogicalRelation",
    "LogicalUtils",
    
    # Emotional Analysis
    "EmotionalAnalysisEngine",
    "EmotionType",
    "SentimentPolarity",
    "EmotionalIntensity",
    "UserState",
    "EmotionScore",
    "SentimentAnalysis",
    "EmotionalContext",
    "EmotionalAnalysisResult",
    "EmotionalUtils",
    
    # Creative Interpretation
    "CreativeInterpretationEngine",
    "CreativityType",
    "InnovationLevel",
    "CreativePattern",
    "CreativeIdea",
    "AlternativeApproach",
    "CreativeConnection",
    "CreativeAnalysisResult",
    "CreativeUtils",
    
    # Dimensional Synthesis
    "DimensionalSynthesisEngine",
    "DimensionWeight",
    "SynthesisQuality",
    "ConflictType",
    "DimensionalInsight",
    "SynthesisConflict",
    "DimensionalRecommendation",
    "DimensionalSynthesisResult",
    "SynthesisUtils",
    
    # Confidence Scoring
    "ConfidenceScoringEngine",
    "ConfidenceLevel",
    "UncertaintyType",
    "ConfidenceSource",
    "ConfidenceMetric",
    "UncertaintyQuantification",
    "ConfidenceScoringResult",
    "ConfidenceUtils",
    
    # Dimensional Validation
    "DimensionalValidationEngine",
    "ValidationStatus",
    "ValidationCategory",
    "ValidationSeverity",
    "ValidationCheck",
    "ValidationRule",
    "DimensionalValidationResult",
    "ValidationUtils"
]
