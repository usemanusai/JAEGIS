"""
N.L.D.S. Intent Recognition System
Advanced intent classification using machine learning models with JAEGIS-specific intent categories
"""

import numpy as np
import torch
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import spacy
from collections import defaultdict, Counter
import re

logger = logging.getLogger(__name__)


class JAEGISIntentCategory(str, Enum):
    """JAEGIS-specific intent categories."""
    # Core System Operations
    CREATE = "create"
    IMPLEMENT = "implement"
    BUILD = "build"
    DEVELOP = "develop"
    DESIGN = "design"
    
    # Analysis and Investigation
    ANALYZE = "analyze"
    INVESTIGATE = "investigate"
    RESEARCH = "research"
    EVALUATE = "evaluate"
    ASSESS = "assess"
    
    # Modification and Updates
    UPDATE = "update"
    MODIFY = "modify"
    ENHANCE = "enhance"
    IMPROVE = "improve"
    OPTIMIZE = "optimize"
    
    # Testing and Validation
    TEST = "test"
    VALIDATE = "validate"
    VERIFY = "verify"
    DEBUG = "debug"
    TROUBLESHOOT = "troubleshoot"
    
    # Deployment and Operations
    DEPLOY = "deploy"
    CONFIGURE = "configure"
    SETUP = "setup"
    INSTALL = "install"
    EXECUTE = "execute"
    
    # Documentation and Communication
    DOCUMENT = "document"
    EXPLAIN = "explain"
    DESCRIBE = "describe"
    REPORT = "report"
    COMMUNICATE = "communicate"
    
    # Monitoring and Maintenance
    MONITOR = "monitor"
    MAINTAIN = "maintain"
    BACKUP = "backup"
    RESTORE = "restore"
    CLEAN = "clean"
    
    # Security and Compliance
    SECURE = "secure"
    PROTECT = "protect"
    AUDIT = "audit"
    COMPLY = "comply"
    ENCRYPT = "encrypt"
    
    # Integration and Coordination
    INTEGRATE = "integrate"
    CONNECT = "connect"
    COORDINATE = "coordinate"
    SYNCHRONIZE = "synchronize"
    ORCHESTRATE = "orchestrate"
    
    # Information Retrieval
    SEARCH = "search"
    FIND = "find"
    RETRIEVE = "retrieve"
    QUERY = "query"
    LOOKUP = "lookup"
    
    # General Actions
    HELP = "help"
    SUPPORT = "support"
    GUIDE = "guide"
    ASSIST = "assist"
    UNKNOWN = "unknown"


@dataclass
class IntentPrediction:
    """Intent prediction result."""
    intent: JAEGISIntentCategory
    confidence: float
    probability_distribution: Dict[str, float]
    reasoning: str
    alternative_intents: List[Tuple[JAEGISIntentCategory, float]]


@dataclass
class IntentFeatures:
    """Extracted features for intent classification."""
    action_verbs: List[str]
    object_nouns: List[str]
    technical_terms: List[str]
    sentiment_score: float
    urgency_indicators: List[str]
    complexity_score: float
    context_keywords: List[str]


@dataclass
class IntentRecognitionResult:
    """Comprehensive intent recognition result."""
    input_text: str
    predicted_intent: IntentPrediction
    extracted_features: IntentFeatures
    processing_time_ms: float
    model_metadata: Dict[str, Any]


class IntentRecognitionSystem:
    """
    Advanced intent recognition system for JAEGIS-specific intent categories
    using multiple machine learning models and feature extraction techniques.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        
        # Initialize NLP components
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.error("spaCy model not found. Please install: python -m spacy download en_core_web_sm")
            raise
        
        # Initialize transformer-based classifier
        self.transformer_classifier = pipeline(
            "text-classification",
            model="microsoft/DialoGPT-medium",
            return_all_scores=True
        )
        
        # Intent keyword mappings for rule-based classification
        self.intent_keywords = self._initialize_intent_keywords()
        
        # Feature extractors
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            stop_words='english'
        )
        
        # Machine learning models
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'svm': SVC(probability=True, random_state=42),
            'naive_bayes': MultinomialNB()
        }
        
        # Load pre-trained models if available
        if model_path:
            self._load_models(model_path)
        
        # Training data for JAEGIS intents
        self.training_data = self._generate_training_data()
        
        # Train models with synthetic data
        self._train_models()
        
        logger.info("Intent Recognition System initialized")
    
    def _initialize_intent_keywords(self) -> Dict[JAEGISIntentCategory, List[str]]:
        """Initialize keyword mappings for each intent category."""
        return {
            JAEGISIntentCategory.CREATE: [
                "create", "make", "build", "generate", "establish", "form", "construct",
                "new", "fresh", "initialize", "start", "begin"
            ],
            JAEGISIntentCategory.IMPLEMENT: [
                "implement", "execute", "realize", "carry out", "put into practice",
                "deploy", "apply", "enact", "fulfill"
            ],
            JAEGISIntentCategory.ANALYZE: [
                "analyze", "examine", "study", "investigate", "review", "assess",
                "evaluate", "inspect", "scrutinize", "research"
            ],
            JAEGISIntentCategory.UPDATE: [
                "update", "modify", "change", "alter", "revise", "edit", "adjust",
                "improve", "enhance", "upgrade", "refresh"
            ],
            JAEGISIntentCategory.TEST: [
                "test", "check", "verify", "validate", "confirm", "ensure",
                "trial", "experiment", "probe", "examine"
            ],
            JAEGISIntentCategory.DEPLOY: [
                "deploy", "release", "launch", "publish", "distribute", "install",
                "setup", "configure", "activate", "enable"
            ],
            JAEGISIntentCategory.DOCUMENT: [
                "document", "write", "record", "note", "log", "report",
                "explain", "describe", "detail", "outline"
            ],
            JAEGISIntentCategory.MONITOR: [
                "monitor", "watch", "observe", "track", "supervise", "oversee",
                "check", "survey", "guard", "patrol"
            ],
            JAEGISIntentCategory.SECURE: [
                "secure", "protect", "safeguard", "defend", "shield", "guard",
                "encrypt", "lock", "authenticate", "authorize"
            ],
            JAEGISIntentCategory.INTEGRATE: [
                "integrate", "connect", "link", "join", "merge", "combine",
                "unite", "coordinate", "synchronize", "orchestrate"
            ],
            JAEGISIntentCategory.SEARCH: [
                "search", "find", "look", "seek", "locate", "discover",
                "retrieve", "fetch", "query", "lookup"
            ],
            JAEGISIntentCategory.HELP: [
                "help", "assist", "support", "aid", "guide", "advise",
                "recommend", "suggest", "explain", "clarify"
            ]
        }
    
    def _generate_training_data(self) -> List[Tuple[str, JAEGISIntentCategory]]:
        """Generate synthetic training data for JAEGIS intents."""
        training_examples = [
            # CREATE examples
            ("Create a new user authentication system", JAEGISIntentCategory.CREATE),
            ("Build a secure API endpoint", JAEGISIntentCategory.CREATE),
            ("Generate documentation for the project", JAEGISIntentCategory.CREATE),
            ("Make a new database schema", JAEGISIntentCategory.CREATE),
            
            # IMPLEMENT examples
            ("Implement JWT token authentication", JAEGISIntentCategory.IMPLEMENT),
            ("Execute the deployment pipeline", JAEGISIntentCategory.IMPLEMENT),
            ("Apply security patches to the system", JAEGISIntentCategory.IMPLEMENT),
            ("Realize the proposed architecture", JAEGISIntentCategory.IMPLEMENT),
            
            # ANALYZE examples
            ("Analyze the system performance metrics", JAEGISIntentCategory.ANALYZE),
            ("Investigate the security vulnerabilities", JAEGISIntentCategory.ANALYZE),
            ("Examine the code quality issues", JAEGISIntentCategory.ANALYZE),
            ("Study the user behavior patterns", JAEGISIntentCategory.ANALYZE),
            
            # UPDATE examples
            ("Update the database schema", JAEGISIntentCategory.UPDATE),
            ("Modify the API response format", JAEGISIntentCategory.UPDATE),
            ("Enhance the user interface", JAEGISIntentCategory.UPDATE),
            ("Improve the system performance", JAEGISIntentCategory.UPDATE),
            
            # TEST examples
            ("Test the authentication flow", JAEGISIntentCategory.TEST),
            ("Validate the API endpoints", JAEGISIntentCategory.TEST),
            ("Verify the security measures", JAEGISIntentCategory.TEST),
            ("Check the system integration", JAEGISIntentCategory.TEST),
            
            # DEPLOY examples
            ("Deploy the application to production", JAEGISIntentCategory.DEPLOY),
            ("Release the new version", JAEGISIntentCategory.DEPLOY),
            ("Configure the server environment", JAEGISIntentCategory.DEPLOY),
            ("Setup the monitoring system", JAEGISIntentCategory.DEPLOY),
            
            # DOCUMENT examples
            ("Document the API specifications", JAEGISIntentCategory.DOCUMENT),
            ("Write user guide for the system", JAEGISIntentCategory.DOCUMENT),
            ("Explain the architecture design", JAEGISIntentCategory.DOCUMENT),
            ("Record the deployment process", JAEGISIntentCategory.DOCUMENT),
            
            # MONITOR examples
            ("Monitor system health metrics", JAEGISIntentCategory.MONITOR),
            ("Track user activity logs", JAEGISIntentCategory.MONITOR),
            ("Observe performance indicators", JAEGISIntentCategory.MONITOR),
            ("Watch for security threats", JAEGISIntentCategory.MONITOR),
            
            # SECURE examples
            ("Secure the database connections", JAEGISIntentCategory.SECURE),
            ("Protect user data privacy", JAEGISIntentCategory.SECURE),
            ("Encrypt sensitive information", JAEGISIntentCategory.SECURE),
            ("Authenticate user access", JAEGISIntentCategory.SECURE),
            
            # INTEGRATE examples
            ("Integrate with external APIs", JAEGISIntentCategory.INTEGRATE),
            ("Connect to the payment gateway", JAEGISIntentCategory.INTEGRATE),
            ("Synchronize data between systems", JAEGISIntentCategory.INTEGRATE),
            ("Coordinate multiple services", JAEGISIntentCategory.INTEGRATE),
            
            # SEARCH examples
            ("Search for user records", JAEGISIntentCategory.SEARCH),
            ("Find system configuration files", JAEGISIntentCategory.SEARCH),
            ("Lookup database entries", JAEGISIntentCategory.SEARCH),
            ("Retrieve log information", JAEGISIntentCategory.SEARCH),
            
            # HELP examples
            ("Help me understand the system", JAEGISIntentCategory.HELP),
            ("Assist with troubleshooting", JAEGISIntentCategory.HELP),
            ("Guide through the setup process", JAEGISIntentCategory.HELP),
            ("Support the development team", JAEGISIntentCategory.HELP)
        ]
        
        return training_examples
    
    def _train_models(self):
        """Train machine learning models with synthetic data."""
        if not self.training_data:
            logger.warning("No training data available")
            return
        
        # Prepare training data
        texts = [example[0] for example in self.training_data]
        labels = [example[1].value for example in self.training_data]
        
        # Vectorize texts
        X = self.tfidf_vectorizer.fit_transform(texts)
        y = labels
        
        # Train each model
        for model_name, model in self.models.items():
            try:
                model.fit(X, y)
                logger.info(f"Trained {model_name} model")
            except Exception as e:
                logger.error(f"Failed to train {model_name}: {e}")
    
    def extract_features(self, text: str) -> IntentFeatures:
        """Extract features for intent classification."""
        doc = self.nlp(text)
        
        # Extract action verbs
        action_verbs = [token.lemma_ for token in doc 
                       if token.pos_ == 'VERB' and not token.is_stop]
        
        # Extract object nouns
        object_nouns = [token.lemma_ for token in doc 
                       if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]
        
        # Extract technical terms (entities and compound nouns)
        technical_terms = []
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'TECH']:
                technical_terms.append(ent.text)
        
        # Add compound technical terms
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:
                technical_terms.append(chunk.text)
        
        # Calculate sentiment score (simplified)
        sentiment_score = 0.0
        positive_words = ['good', 'great', 'excellent', 'perfect', 'amazing']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'wrong']
        
        text_lower = text.lower()
        for word in positive_words:
            sentiment_score += text_lower.count(word) * 0.1
        for word in negative_words:
            sentiment_score -= text_lower.count(word) * 0.1
        
        # Detect urgency indicators
        urgency_indicators = []
        urgency_words = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'now']
        for word in urgency_words:
            if word in text_lower:
                urgency_indicators.append(word)
        
        # Calculate complexity score
        complexity_factors = {
            'sentence_length': len(text.split()) / 20.0,  # Normalize by 20 words
            'technical_terms': len(technical_terms) / 10.0,  # Normalize by 10 terms
            'verb_diversity': len(set(action_verbs)) / 5.0,  # Normalize by 5 unique verbs
        }
        complexity_score = min(1.0, sum(complexity_factors.values()) / len(complexity_factors))
        
        # Extract context keywords
        context_keywords = []
        for token in doc:
            if (token.pos_ in ['NOUN', 'VERB', 'ADJ'] and 
                not token.is_stop and 
                len(token.text) > 2):
                context_keywords.append(token.lemma_)
        
        return IntentFeatures(
            action_verbs=action_verbs,
            object_nouns=object_nouns,
            technical_terms=technical_terms,
            sentiment_score=sentiment_score,
            urgency_indicators=urgency_indicators,
            complexity_score=complexity_score,
            context_keywords=context_keywords[:10]  # Top 10 keywords
        )
    
    def _rule_based_classification(self, text: str, features: IntentFeatures) -> Dict[JAEGISIntentCategory, float]:
        """Perform rule-based intent classification."""
        scores = defaultdict(float)
        text_lower = text.lower()
        
        # Score based on keyword matching
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[intent] += 1.0
                # Partial matching for action verbs
                if keyword in features.action_verbs:
                    scores[intent] += 1.5
        
        # Boost scores based on features
        if features.urgency_indicators:
            scores[JAEGISIntentCategory.HELP] += 0.5
            scores[JAEGISIntentCategory.TROUBLESHOOT] += 0.5
        
        if features.complexity_score > 0.7:
            scores[JAEGISIntentCategory.ANALYZE] += 0.3
            scores[JAEGISIntentCategory.IMPLEMENT] += 0.3
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            for intent in scores:
                scores[intent] /= total_score
        
        return dict(scores)
    
    def _ml_classification(self, text: str) -> Dict[JAEGISIntentCategory, float]:
        """Perform machine learning-based classification."""
        try:
            # Vectorize input text
            X = self.tfidf_vectorizer.transform([text])
            
            # Get predictions from all models
            model_predictions = {}
            for model_name, model in self.models.items():
                if hasattr(model, 'predict_proba'):
                    probabilities = model.predict_proba(X)[0]
                    classes = model.classes_
                    model_predictions[model_name] = dict(zip(classes, probabilities))
            
            # Ensemble predictions (average)
            if model_predictions:
                all_intents = set()
                for pred in model_predictions.values():
                    all_intents.update(pred.keys())
                
                ensemble_scores = {}
                for intent in all_intents:
                    scores = [pred.get(intent, 0.0) for pred in model_predictions.values()]
                    ensemble_scores[intent] = np.mean(scores)
                
                # Convert string intents back to enum
                enum_scores = {}
                for intent_str, score in ensemble_scores.items():
                    try:
                        intent_enum = JAEGISIntentCategory(intent_str)
                        enum_scores[intent_enum] = score
                    except ValueError:
                        continue
                
                return enum_scores
            
        except Exception as e:
            logger.error(f"ML classification failed: {e}")
        
        return {}
    
    def predict_intent(self, text: str) -> IntentRecognitionResult:
        """Predict intent using ensemble of methods."""
        import time
        start_time = time.time()
        
        # Extract features
        features = self.extract_features(text)
        
        # Get predictions from different methods
        rule_scores = self._rule_based_classification(text, features)
        ml_scores = self._ml_classification(text)
        
        # Combine scores (weighted ensemble)
        combined_scores = defaultdict(float)
        
        # Weight rule-based predictions
        for intent, score in rule_scores.items():
            combined_scores[intent] += score * 0.6
        
        # Weight ML predictions
        for intent, score in ml_scores.items():
            combined_scores[intent] += score * 0.4
        
        # Handle case where no predictions are made
        if not combined_scores:
            combined_scores[JAEGISIntentCategory.UNKNOWN] = 1.0
        
        # Get top prediction
        top_intent = max(combined_scores, key=combined_scores.get)
        top_confidence = combined_scores[top_intent]
        
        # Get alternative intents
        sorted_intents = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        alternative_intents = [(intent, score) for intent, score in sorted_intents[1:4]]
        
        # Generate reasoning
        reasoning = self._generate_reasoning(text, features, top_intent, rule_scores, ml_scores)
        
        # Create prediction object
        prediction = IntentPrediction(
            intent=top_intent,
            confidence=top_confidence,
            probability_distribution={intent.value: score for intent, score in combined_scores.items()},
            reasoning=reasoning,
            alternative_intents=alternative_intents
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return IntentRecognitionResult(
            input_text=text,
            predicted_intent=prediction,
            extracted_features=features,
            processing_time_ms=processing_time,
            model_metadata={
                "models_used": list(self.models.keys()),
                "rule_based_weight": 0.6,
                "ml_weight": 0.4,
                "feature_count": len(features.context_keywords)
            }
        )
    
    def _generate_reasoning(self, text: str, features: IntentFeatures, 
                          predicted_intent: JAEGISIntentCategory,
                          rule_scores: Dict, ml_scores: Dict) -> str:
        """Generate human-readable reasoning for the prediction."""
        
        reasoning_parts = []
        
        # Action verb analysis
        if features.action_verbs:
            reasoning_parts.append(f"Detected action verbs: {', '.join(features.action_verbs[:3])}")
        
        # Technical terms
        if features.technical_terms:
            reasoning_parts.append(f"Technical terms found: {', '.join(features.technical_terms[:2])}")
        
        # Urgency indicators
        if features.urgency_indicators:
            reasoning_parts.append(f"Urgency indicators: {', '.join(features.urgency_indicators)}")
        
        # Complexity assessment
        if features.complexity_score > 0.7:
            reasoning_parts.append("High complexity detected")
        elif features.complexity_score < 0.3:
            reasoning_parts.append("Low complexity detected")
        
        # Top scoring method
        rule_top_score = max(rule_scores.values()) if rule_scores else 0
        ml_top_score = max(ml_scores.values()) if ml_scores else 0
        
        if rule_top_score > ml_top_score:
            reasoning_parts.append("Primarily based on keyword matching")
        else:
            reasoning_parts.append("Primarily based on machine learning models")
        
        return "; ".join(reasoning_parts) if reasoning_parts else "Based on general text analysis"
    
    def _save_models(self, path: str):
        """Save trained models to disk."""
        try:
            model_data = {
                'models': self.models,
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'intent_keywords': self.intent_keywords
            }
            with open(path, 'wb') as f:
                pickle.dump(model_data, f)
            logger.info(f"Models saved to {path}")
        except Exception as e:
            logger.error(f"Failed to save models: {e}")
    
    def _load_models(self, path: str):
        """Load pre-trained models from disk."""
        try:
            with open(path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.models = model_data['models']
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            self.intent_keywords = model_data['intent_keywords']
            
            logger.info(f"Models loaded from {path}")
        except Exception as e:
            logger.error(f"Failed to load models: {e}")


# Example usage
if __name__ == "__main__":
    # Initialize intent recognition system
    intent_system = IntentRecognitionSystem()
    
    # Test examples
    test_texts = [
        "Create a secure user authentication system with JWT tokens",
        "Analyze the performance metrics of the database",
        "Deploy the application to the production environment",
        "Help me troubleshoot the API connection issues",
        "Update the documentation for the new features"
    ]
    
    # Predict intents
    for text in test_texts:
        result = intent_system.predict_intent(text)
        print(f"\nText: {text}")
        print(f"Predicted Intent: {result.predicted_intent.intent.value}")
        print(f"Confidence: {result.predicted_intent.confidence:.3f}")
        print(f"Reasoning: {result.predicted_intent.reasoning}")
        print(f"Processing Time: {result.processing_time_ms:.2f}ms")
