"""
N.L.D.S. Intent Recognition System
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced intent recognition with machine learning classification,
JAEGIS-specific intent categories, and contextual understanding.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging
import json
import pickle
from datetime import datetime
import asyncio

# ML imports
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
import joblib

# Local imports
from .tokenizer import TokenizationResult
from .semantic_analyzer import SemanticAnalysisResult

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# INTENT CATEGORIES AND ENUMS
# ============================================================================

class IntentCategory(Enum):
    """JAEGIS-specific intent categories."""
    
    # Core Operations
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    EXECUTE = "execute"
    
    # JAEGIS Specific
    SQUAD_ACTIVATION = "squad_activation"
    MODE_SELECTION = "mode_selection"
    AGENT_CREATION = "agent_creation"
    TASK_MANAGEMENT = "task_management"
    WORKFLOW_CONTROL = "workflow_control"
    
    # Analysis and Processing
    ANALYZE = "analyze"
    PROCESS = "process"
    GENERATE = "generate"
    OPTIMIZE = "optimize"
    VALIDATE = "validate"
    
    # Information Requests
    QUESTION = "question"
    HELP = "help"
    STATUS = "status"
    REPORT = "report"
    SEARCH = "search"
    
    # System Control
    CONFIGURE = "configure"
    MONITOR = "monitor"
    DEBUG = "debug"
    BACKUP = "backup"
    DEPLOY = "deploy"
    
    # Communication
    NOTIFICATION = "notification"
    ALERT = "alert"
    FEEDBACK = "feedback"
    COLLABORATION = "collaboration"
    
    # Unknown/Ambiguous
    UNKNOWN = "unknown"
    AMBIGUOUS = "ambiguous"


class IntentConfidence(Enum):
    """Intent confidence levels."""
    HIGH = "high"      # >0.8
    MEDIUM = "medium"  # 0.5-0.8
    LOW = "low"        # 0.2-0.5
    VERY_LOW = "very_low"  # <0.2


@dataclass
class IntentPrediction:
    """Intent prediction result."""
    intent: IntentCategory
    confidence: float
    confidence_level: IntentConfidence
    probability_distribution: Dict[str, float]
    features: Dict[str, Any]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class IntentRecognitionResult:
    """Complete intent recognition result."""
    text: str
    primary_intent: IntentPrediction
    alternative_intents: List[IntentPrediction]
    context_factors: Dict[str, Any]
    jaegis_mapping: Dict[str, Any]
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# INTENT RECOGNITION ENGINE
# ============================================================================

class IntentRecognitionEngine:
    """
    Advanced intent recognition system with ML classification.
    
    Features:
    - Multiple ML models (Neural Network, Random Forest, Logistic Regression)
    - JAEGIS-specific intent categories
    - Contextual understanding
    - Confidence scoring
    - Intent hierarchy and relationships
    - Real-time learning and adaptation
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize intent recognition engine.
        
        Args:
            model_path: Path to pre-trained model
        """
        self.models = {}
        self.feature_extractors = {}
        self.intent_patterns = self._load_intent_patterns()
        self.jaegis_mappings = self._load_jaegis_mappings()
        self.context_weights = self._load_context_weights()
        
        # Initialize models
        self._initialize_models()
        
        # Load pre-trained model if available
        if model_path:
            self.load_model(model_path)
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent patterns and keywords."""
        return {
            IntentCategory.CREATE.value: [
                "create", "make", "build", "generate", "new", "add",
                "establish", "set up", "initialize", "start"
            ],
            IntentCategory.UPDATE.value: [
                "update", "modify", "change", "edit", "alter", "revise",
                "improve", "enhance", "adjust", "refine"
            ],
            IntentCategory.DELETE.value: [
                "delete", "remove", "destroy", "eliminate", "clear",
                "erase", "drop", "purge", "clean", "terminate"
            ],
            IntentCategory.READ.value: [
                "read", "view", "show", "display", "get", "fetch",
                "retrieve", "list", "see", "check"
            ],
            IntentCategory.EXECUTE.value: [
                "execute", "run", "perform", "do", "carry out",
                "implement", "launch", "trigger", "activate", "start"
            ],
            IntentCategory.SQUAD_ACTIVATION.value: [
                "activate squad", "call squad", "use squad", "deploy squad",
                "development-squad", "quality-squad", "business-squad",
                "process-squad", "content-squad", "system-squad"
            ],
            IntentCategory.MODE_SELECTION.value: [
                "mode", "switch mode", "change mode", "use mode",
                "mode-1", "mode-2", "mode-3", "mode-4", "mode-5"
            ],
            IntentCategory.AGENT_CREATION.value: [
                "create agent", "new agent", "build agent", "agent creator",
                "make agent", "design agent", "develop agent"
            ],
            IntentCategory.TASK_MANAGEMENT.value: [
                "task", "manage task", "create task", "assign task",
                "complete task", "track task", "schedule", "organize"
            ],
            IntentCategory.ANALYZE.value: [
                "analyze", "examine", "study", "investigate", "review",
                "assess", "evaluate", "inspect", "research"
            ],
            IntentCategory.QUESTION.value: [
                "what", "how", "why", "when", "where", "who", "which",
                "can you", "could you", "would you", "is it", "are there"
            ],
            IntentCategory.HELP.value: [
                "help", "assist", "support", "guide", "explain",
                "tutorial", "documentation", "how to", "instructions"
            ],
            IntentCategory.STATUS.value: [
                "status", "state", "condition", "progress", "health",
                "check status", "current state", "how is"
            ],
            IntentCategory.CONFIGURE.value: [
                "configure", "setup", "settings", "preferences", "options",
                "customize", "adjust settings", "parameters"
            ],
            IntentCategory.MONITOR.value: [
                "monitor", "watch", "observe", "track", "supervise",
                "keep an eye", "surveillance", "oversight"
            ]
        }
    
    def _load_jaegis_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Load JAEGIS-specific intent mappings."""
        return {
            IntentCategory.SQUAD_ACTIVATION.value: {
                "target_modes": [1, 2, 3, 4, 5],
                "required_parameters": ["squad_name"],
                "optional_parameters": ["priority", "context"],
                "execution_type": "squad_deployment"
            },
            IntentCategory.MODE_SELECTION.value: {
                "target_modes": [1, 2, 3, 4, 5],
                "required_parameters": ["mode_number"],
                "optional_parameters": ["configuration", "timeout"],
                "execution_type": "mode_switch"
            },
            IntentCategory.AGENT_CREATION.value: {
                "target_modes": [4, 5],  # Advanced modes for agent creation
                "required_parameters": ["agent_type", "capabilities"],
                "optional_parameters": ["template", "configuration"],
                "execution_type": "agent_instantiation"
            },
            IntentCategory.TASK_MANAGEMENT.value: {
                "target_modes": [1, 2, 3],
                "required_parameters": ["task_action"],
                "optional_parameters": ["task_id", "assignee", "deadline"],
                "execution_type": "task_operation"
            },
            IntentCategory.ANALYZE.value: {
                "target_modes": [2, 3, 4],
                "required_parameters": ["analysis_target"],
                "optional_parameters": ["analysis_type", "depth"],
                "execution_type": "analysis_request"
            }
        }
    
    def _load_context_weights(self) -> Dict[str, float]:
        """Load context weighting factors."""
        return {
            "jaegis_entities": 1.5,
            "technical_terms": 1.2,
            "action_verbs": 1.3,
            "question_words": 1.4,
            "urgency_indicators": 1.6,
            "temporal_indicators": 1.1,
            "conditional_phrases": 1.2
        }
    
    def _initialize_models(self):
        """Initialize ML models for intent classification."""
        # Neural Network Model
        self.models["neural_net"] = IntentNeuralNetwork(
            input_size=100,  # Feature vector size
            hidden_size=64,
            num_classes=len(IntentCategory)
        )
        
        # Random Forest Model
        self.models["random_forest"] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        # Logistic Regression Model
        self.models["logistic_regression"] = LogisticRegression(
            max_iter=1000,
            random_state=42
        )
        
        logger.info("Intent recognition models initialized")
    
    def extract_features(self, text: str, 
                        tokenization_result: TokenizationResult,
                        semantic_result: SemanticAnalysisResult) -> np.ndarray:
        """
        Extract features for intent classification.
        
        Args:
            text: Input text
            tokenization_result: Tokenization results
            semantic_result: Semantic analysis results
            
        Returns:
            Feature vector
        """
        features = []
        
        # Text-based features
        features.extend(self._extract_text_features(text))
        
        # Token-based features
        features.extend(self._extract_token_features(tokenization_result))
        
        # Semantic features
        features.extend(self._extract_semantic_features(semantic_result))
        
        # Pattern-based features
        features.extend(self._extract_pattern_features(text))
        
        # JAEGIS-specific features
        features.extend(self._extract_jaegis_features(text, tokenization_result))
        
        # Pad or truncate to fixed size
        target_size = 100
        if len(features) < target_size:
            features.extend([0.0] * (target_size - len(features)))
        else:
            features = features[:target_size]
        
        return np.array(features, dtype=np.float32)
    
    def _extract_text_features(self, text: str) -> List[float]:
        """Extract basic text features."""
        features = []
        
        # Length features
        features.append(len(text))
        features.append(len(text.split()))
        features.append(len([c for c in text if c.isupper()]))
        features.append(len([c for c in text if c in '!?']))
        
        # Question indicators
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
        features.append(sum(1 for word in question_words if word in text.lower()))
        
        # Action indicators
        action_verbs = ['create', 'make', 'do', 'run', 'execute', 'build']
        features.append(sum(1 for verb in action_verbs if verb in text.lower()))
        
        # Urgency indicators
        urgency_words = ['urgent', 'asap', 'immediately', 'quickly', 'now']
        features.append(sum(1 for word in urgency_words if word in text.lower()))
        
        return features
    
    def _extract_token_features(self, tokenization_result: TokenizationResult) -> List[float]:
        """Extract token-based features."""
        features = []
        
        if not tokenization_result.tokens:
            return [0.0] * 10
        
        # Token type distribution
        token_types = {}
        for token in tokenization_result.tokens:
            token_types[token.token_type.value] = token_types.get(token.token_type.value, 0) + 1
        
        total_tokens = len(tokenization_result.tokens)
        features.append(token_types.get('word', 0) / total_tokens)
        features.append(token_types.get('jaegis_entity', 0) / total_tokens)
        features.append(token_types.get('jaegis_command', 0) / total_tokens)
        features.append(token_types.get('number', 0) / total_tokens)
        features.append(token_types.get('punctuation', 0) / total_tokens)
        
        # Average token length
        avg_length = np.mean([len(token.text) for token in tokenization_result.tokens])
        features.append(avg_length)
        
        # Language confidence
        features.append(tokenization_result.metadata.get('language_confidence', 0.5))
        
        # Special tokens count
        features.append(tokenization_result.metadata.get('special_tokens_count', 0))
        
        # Processing time (normalized)
        features.append(min(tokenization_result.processing_time_ms / 1000, 1.0))
        
        # Token count
        features.append(min(tokenization_result.token_count / 100, 1.0))
        
        return features
    
    def _extract_semantic_features(self, semantic_result: SemanticAnalysisResult) -> List[float]:
        """Extract semantic-based features."""
        features = []
        
        # Confidence score
        features.append(semantic_result.confidence_score)
        
        # Concept count
        features.append(min(len(semantic_result.concepts) / 20, 1.0))
        
        # Relations count
        features.append(min(len(semantic_result.relations) / 10, 1.0))
        
        # Domain relevance scores
        for domain in ['development', 'testing', 'deployment', 'monitoring']:
            score = semantic_result.domain_relevance.get(domain, 0.0)
            features.append(score)
        
        # Semantic similarity with key concepts
        for category in ['squads', 'modes', 'operations']:
            if category in semantic_result.semantic_similarity:
                avg_similarity = np.mean(list(semantic_result.semantic_similarity[category].values()))
                features.append(avg_similarity)
            else:
                features.append(0.0)
        
        # Processing time (normalized)
        features.append(min(semantic_result.processing_time_ms / 1000, 1.0))
        
        return features
    
    def _extract_pattern_features(self, text: str) -> List[float]:
        """Extract pattern-based features."""
        features = []
        text_lower = text.lower()
        
        # Intent pattern matching
        for intent, patterns in self.intent_patterns.items():
            pattern_score = sum(1 for pattern in patterns if pattern in text_lower)
            features.append(min(pattern_score / len(patterns), 1.0))
        
        return features[:15]  # Limit to prevent feature explosion
    
    def _extract_jaegis_features(self, text: str, 
                                tokenization_result: TokenizationResult) -> List[float]:
        """Extract JAEGIS-specific features."""
        features = []
        text_lower = text.lower()
        
        # Squad mentions
        squad_count = sum(1 for token in tokenization_result.tokens 
                         if 'squad' in token.text.lower())
        features.append(min(squad_count / 5, 1.0))
        
        # Mode mentions
        mode_count = sum(1 for token in tokenization_result.tokens 
                        if 'mode' in token.text.lower())
        features.append(min(mode_count / 3, 1.0))
        
        # Agent mentions
        agent_count = text_lower.count('agent')
        features.append(min(agent_count / 3, 1.0))
        
        # Task mentions
        task_count = text_lower.count('task')
        features.append(min(task_count / 3, 1.0))
        
        # Command indicators
        command_indicators = ['/jaegis', '/mode', '/squad', '/nlds']
        command_score = sum(1 for indicator in command_indicators if indicator in text_lower)
        features.append(min(command_score / len(command_indicators), 1.0))
        
        return features
    
    def predict_intent(self, features: np.ndarray, 
                      use_ensemble: bool = True) -> IntentPrediction:
        """
        Predict intent from features.
        
        Args:
            features: Feature vector
            use_ensemble: Whether to use ensemble prediction
            
        Returns:
            Intent prediction
        """
        if use_ensemble:
            return self._ensemble_predict(features)
        else:
            return self._single_model_predict(features, "neural_net")
    
    def _ensemble_predict(self, features: np.ndarray) -> IntentPrediction:
        """Ensemble prediction using multiple models."""
        predictions = {}
        confidences = {}
        
        # Neural network prediction
        if "neural_net" in self.models:
            nn_pred = self._neural_net_predict(features)
            predictions["neural_net"] = nn_pred
            confidences["neural_net"] = 0.4  # Weight
        
        # Random forest prediction
        if "random_forest" in self.models and hasattr(self.models["random_forest"], 'predict_proba'):
            rf_pred = self._sklearn_predict(features, "random_forest")
            predictions["random_forest"] = rf_pred
            confidences["random_forest"] = 0.3  # Weight
        
        # Logistic regression prediction
        if "logistic_regression" in self.models and hasattr(self.models["logistic_regression"], 'predict_proba'):
            lr_pred = self._sklearn_predict(features, "logistic_regression")
            predictions["logistic_regression"] = lr_pred
            confidences["logistic_regression"] = 0.3  # Weight
        
        # Combine predictions
        if not predictions:
            # Fallback to pattern-based prediction
            return self._pattern_based_predict(features)
        
        # Weighted average of probabilities
        combined_probs = {}
        total_weight = sum(confidences.values())
        
        for model_name, pred in predictions.items():
            weight = confidences[model_name] / total_weight
            for intent, prob in pred.probability_distribution.items():
                combined_probs[intent] = combined_probs.get(intent, 0) + prob * weight
        
        # Find best intent
        best_intent = max(combined_probs.items(), key=lambda x: x[1])
        intent_category = IntentCategory(best_intent[0])
        confidence = best_intent[1]
        
        # Determine confidence level
        if confidence > 0.8:
            confidence_level = IntentConfidence.HIGH
        elif confidence > 0.5:
            confidence_level = IntentConfidence.MEDIUM
        elif confidence > 0.2:
            confidence_level = IntentConfidence.LOW
        else:
            confidence_level = IntentConfidence.VERY_LOW
        
        return IntentPrediction(
            intent=intent_category,
            confidence=confidence,
            confidence_level=confidence_level,
            probability_distribution=combined_probs,
            features={"ensemble": True, "models_used": list(predictions.keys())},
            metadata={"prediction_method": "ensemble"}
        )
    
    def _neural_net_predict(self, features: np.ndarray) -> IntentPrediction:
        """Neural network prediction."""
        model = self.models["neural_net"]
        
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            outputs = model(features_tensor)
            probabilities = F.softmax(outputs, dim=1).squeeze().numpy()
        
        # Map to intent categories
        intent_list = list(IntentCategory)
        prob_dict = {intent.value: float(probabilities[i]) 
                    for i, intent in enumerate(intent_list)}
        
        best_intent_idx = np.argmax(probabilities)
        best_intent = intent_list[best_intent_idx]
        confidence = float(probabilities[best_intent_idx])
        
        return IntentPrediction(
            intent=best_intent,
            confidence=confidence,
            confidence_level=self._get_confidence_level(confidence),
            probability_distribution=prob_dict,
            features={"model": "neural_net"},
            metadata={"prediction_method": "neural_network"}
        )
    
    def _sklearn_predict(self, features: np.ndarray, model_name: str) -> IntentPrediction:
        """Scikit-learn model prediction."""
        model = self.models[model_name]
        
        try:
            probabilities = model.predict_proba(features.reshape(1, -1))[0]
            predicted_class = model.predict(features.reshape(1, -1))[0]
            
            # Map to intent categories
            intent_list = list(IntentCategory)
            prob_dict = {intent.value: float(probabilities[i]) 
                        for i, intent in enumerate(intent_list)}
            
            best_intent = IntentCategory(predicted_class)
            confidence = float(max(probabilities))
            
            return IntentPrediction(
                intent=best_intent,
                confidence=confidence,
                confidence_level=self._get_confidence_level(confidence),
                probability_distribution=prob_dict,
                features={"model": model_name},
                metadata={"prediction_method": model_name}
            )
            
        except Exception as e:
            logger.warning(f"Sklearn prediction failed: {e}")
            return self._pattern_based_predict(features)
    
    def _pattern_based_predict(self, features: np.ndarray) -> IntentPrediction:
        """Fallback pattern-based prediction."""
        # Simple pattern matching based on feature analysis
        # This is a simplified fallback method
        
        # Analyze feature patterns
        if features[4] > 0.5:  # Question words feature
            intent = IntentCategory.QUESTION
            confidence = 0.7
        elif features[5] > 0.5:  # Action verbs feature
            intent = IntentCategory.EXECUTE
            confidence = 0.6
        elif features[6] > 0.5:  # Urgency indicators
            intent = IntentCategory.HELP
            confidence = 0.6
        else:
            intent = IntentCategory.UNKNOWN
            confidence = 0.3
        
        prob_dict = {i.value: 0.1 for i in IntentCategory}
        prob_dict[intent.value] = confidence
        
        return IntentPrediction(
            intent=intent,
            confidence=confidence,
            confidence_level=self._get_confidence_level(confidence),
            probability_distribution=prob_dict,
            features={"model": "pattern_based"},
            metadata={"prediction_method": "pattern_fallback"}
        )
    
    def _get_confidence_level(self, confidence: float) -> IntentConfidence:
        """Convert confidence score to confidence level."""
        if confidence > 0.8:
            return IntentConfidence.HIGH
        elif confidence > 0.5:
            return IntentConfidence.MEDIUM
        elif confidence > 0.2:
            return IntentConfidence.LOW
        else:
            return IntentConfidence.VERY_LOW
    
    async def recognize_intent(self, text: str,
                             tokenization_result: TokenizationResult,
                             semantic_result: SemanticAnalysisResult,
                             context: Optional[Dict[str, Any]] = None) -> IntentRecognitionResult:
        """
        Perform complete intent recognition.
        
        Args:
            text: Input text
            tokenization_result: Tokenization results
            semantic_result: Semantic analysis results
            context: Optional context information
            
        Returns:
            Complete intent recognition result
        """
        import time
        start_time = time.time()
        
        try:
            # Extract features
            features = self.extract_features(text, tokenization_result, semantic_result)
            
            # Predict primary intent
            primary_intent = self.predict_intent(features)
            
            # Generate alternative intents
            alternative_intents = self._generate_alternatives(features, primary_intent)
            
            # Analyze context factors
            context_factors = self._analyze_context_factors(text, context)
            
            # Generate JAEGIS mapping
            jaegis_mapping = self._generate_jaegis_mapping(primary_intent, context_factors)
            
            processing_time = (time.time() - start_time) * 1000
            
            return IntentRecognitionResult(
                text=text,
                primary_intent=primary_intent,
                alternative_intents=alternative_intents,
                context_factors=context_factors,
                jaegis_mapping=jaegis_mapping,
                processing_time_ms=processing_time,
                metadata={
                    "feature_vector_size": len(features),
                    "timestamp": datetime.utcnow().isoformat(),
                    "context_provided": context is not None
                }
            )
            
        except Exception as e:
            logger.error(f"Intent recognition failed: {e}")
            
            # Return fallback result
            fallback_intent = IntentPrediction(
                intent=IntentCategory.UNKNOWN,
                confidence=0.0,
                confidence_level=IntentConfidence.VERY_LOW,
                probability_distribution={i.value: 0.0 for i in IntentCategory},
                features={},
                metadata={"error": str(e)}
            )
            
            return IntentRecognitionResult(
                text=text,
                primary_intent=fallback_intent,
                alternative_intents=[],
                context_factors={},
                jaegis_mapping={},
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )
    
    def _generate_alternatives(self, features: np.ndarray, 
                             primary_intent: IntentPrediction) -> List[IntentPrediction]:
        """Generate alternative intent predictions."""
        alternatives = []
        
        # Get top 3 alternatives from probability distribution
        sorted_probs = sorted(primary_intent.probability_distribution.items(), 
                            key=lambda x: x[1], reverse=True)
        
        for intent_name, prob in sorted_probs[1:4]:  # Skip primary (first)
            if prob > 0.1:  # Minimum threshold
                intent = IntentCategory(intent_name)
                alternatives.append(IntentPrediction(
                    intent=intent,
                    confidence=prob,
                    confidence_level=self._get_confidence_level(prob),
                    probability_distribution=primary_intent.probability_distribution,
                    features={"alternative": True},
                    metadata={"rank": len(alternatives) + 2}
                ))
        
        return alternatives
    
    def _analyze_context_factors(self, text: str, 
                                context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze contextual factors affecting intent."""
        factors = {}
        
        # Text-based context
        factors["text_length"] = len(text)
        factors["has_questions"] = "?" in text
        factors["has_commands"] = text.startswith("/")
        factors["urgency_level"] = self._assess_urgency(text)
        
        # External context
        if context:
            factors["user_context"] = context.get("user_context", {})
            factors["session_context"] = context.get("session_context", {})
            factors["conversation_history"] = context.get("conversation_history", [])
        
        return factors
    
    def _assess_urgency(self, text: str) -> str:
        """Assess urgency level from text."""
        urgent_words = ["urgent", "asap", "immediately", "critical", "emergency"]
        text_lower = text.lower()
        
        urgency_score = sum(1 for word in urgent_words if word in text_lower)
        
        if urgency_score >= 2:
            return "high"
        elif urgency_score == 1:
            return "medium"
        else:
            return "low"
    
    def _generate_jaegis_mapping(self, intent: IntentPrediction, 
                               context_factors: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JAEGIS-specific mapping for intent."""
        mapping = {}
        
        intent_value = intent.intent.value
        if intent_value in self.jaegis_mappings:
            base_mapping = self.jaegis_mappings[intent_value].copy()
            
            # Adjust based on context
            if context_factors.get("urgency_level") == "high":
                base_mapping["priority"] = "high"
                base_mapping["timeout"] = "short"
            
            mapping = base_mapping
        else:
            # Default mapping
            mapping = {
                "target_modes": [1],
                "required_parameters": [],
                "optional_parameters": [],
                "execution_type": "general"
            }
        
        mapping["confidence"] = intent.confidence
        mapping["intent_category"] = intent_value
        
        return mapping
    
    def save_model(self, path: str):
        """Save trained models to disk."""
        model_data = {
            "models": {},
            "intent_patterns": self.intent_patterns,
            "jaegis_mappings": self.jaegis_mappings,
            "context_weights": self.context_weights
        }
        
        # Save sklearn models
        for name, model in self.models.items():
            if name in ["random_forest", "logistic_regression"]:
                model_data["models"][name] = model
        
        # Save neural network separately
        if "neural_net" in self.models:
            torch.save(self.models["neural_net"].state_dict(), f"{path}_neural_net.pth")
        
        # Save other data
        with open(f"{path}_intent_data.pkl", "wb") as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Intent recognition models saved to {path}")
    
    def load_model(self, path: str):
        """Load trained models from disk."""
        try:
            # Load model data
            with open(f"{path}_intent_data.pkl", "rb") as f:
                model_data = pickle.load(f)
            
            # Load sklearn models
            for name, model in model_data["models"].items():
                self.models[name] = model
            
            # Load neural network
            if "neural_net" in self.models:
                self.models["neural_net"].load_state_dict(
                    torch.load(f"{path}_neural_net.pth")
                )
            
            # Load other data
            self.intent_patterns = model_data["intent_patterns"]
            self.jaegis_mappings = model_data["jaegis_mappings"]
            self.context_weights = model_data["context_weights"]
            
            logger.info(f"Intent recognition models loaded from {path}")
            
        except Exception as e:
            logger.error(f"Failed to load models: {e}")


# ============================================================================
# NEURAL NETWORK MODEL
# ============================================================================

class IntentNeuralNetwork(nn.Module):
    """Neural network for intent classification."""
    
    def __init__(self, input_size: int, hidden_size: int, num_classes: int):
        super(IntentNeuralNetwork, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, num_classes)
        self.dropout = nn.Dropout(0.3)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x
