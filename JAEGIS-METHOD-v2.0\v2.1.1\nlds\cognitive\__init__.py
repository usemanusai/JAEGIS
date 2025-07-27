"""
N.L.D.S. Cognitive Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Complete human-centric cognitive modeling and processing framework with
cognitive modeling, decision-making, intent inference, user learning,
context retention, and user profile management.
"""

from .cognitive_model import (
    CognitiveModelingEngine,
    CognitiveProcess,
    CognitiveBias,
    MemoryType,
    AttentionType,
    CognitiveState,
    MemoryItem,
    CognitiveDecision,
    CognitiveModelingResult,
    CognitiveUtils
)

from .decision_framework import (
    DecisionFrameworkEngine,
    DecisionSystem,
    DecisionStrategy,
    Heuristic,
    DecisionCriterion,
    DecisionOption,
    DecisionContext,
    DecisionProcess,
    DecisionResult,
    DecisionUtils
)

from .intent_inference import (
    IntentInferenceEngine,
    ImplicitIntentType,
    SemanticGapType,
    InferenceConfidence,
    ImplicitIntent,
    SemanticGap,
    ContextualClue,
    IntentInferenceResult,
    IntentInferenceUtils
)

from .user_learning import (
    UserLearningEngine,
    LearningType,
    AdaptationType,
    BehaviorPattern,
    UserPreference,
    BehaviorObservation,
    AdaptationStrategy,
    LearningSession,
    UserLearningResult,
    UserLearningUtils
)

from .context_retention import (
    ContextRetentionEngine,
    ContextType,
    RetentionPriority,
    CompressionLevel,
    ContextItem,
    ConversationTurn,
    SessionContext,
    ContextRetentionResult,
    ContextRetentionUtils
)

from .user_profile import (
    UserProfileManager,
    PrivacyLevel,
    DataCategory,
    ConsentType,
    UserConsent,
    DataRetentionPolicy,
    UserProfile,
    ProfileUpdateResult,
    UserProfileUtils
)

# Version information
__version__ = "2.2.0"
__author__ = "JAEGIS Development Team"
__description__ = "N.L.D.S. Human-Centric Cognitive Framework"

# Export all components
__all__ = [
    # Cognitive Modeling
    "CognitiveModelingEngine",
    "CognitiveProcess",
    "CognitiveBias",
    "MemoryType",
    "AttentionType",
    "CognitiveState",
    "MemoryItem",
    "CognitiveDecision",
    "CognitiveModelingResult",
    "CognitiveUtils",

    # Decision Framework
    "DecisionFrameworkEngine",
    "DecisionSystem",
    "DecisionStrategy",
    "Heuristic",
    "DecisionCriterion",
    "DecisionOption",
    "DecisionContext",
    "DecisionProcess",
    "DecisionResult",
    "DecisionUtils",

    # Intent Inference
    "IntentInferenceEngine",
    "ImplicitIntentType",
    "SemanticGapType",
    "InferenceConfidence",
    "ImplicitIntent",
    "SemanticGap",
    "ContextualClue",
    "IntentInferenceResult",
    "IntentInferenceUtils",

    # User Learning
    "UserLearningEngine",
    "LearningType",
    "AdaptationType",
    "BehaviorPattern",
    "UserPreference",
    "BehaviorObservation",
    "AdaptationStrategy",
    "LearningSession",
    "UserLearningResult",
    "UserLearningUtils",

    # Context Retention
    "ContextRetentionEngine",
    "ContextType",
    "RetentionPriority",
    "CompressionLevel",
    "ContextItem",
    "ConversationTurn",
    "SessionContext",
    "ContextRetentionResult",
    "ContextRetentionUtils",

    # User Profile Management
    "UserProfileManager",
    "PrivacyLevel",
    "DataCategory",
    "ConsentType",
    "UserConsent",
    "DataRetentionPolicy",
    "UserProfile",
    "ProfileUpdateResult",
    "UserProfileUtils"
]
