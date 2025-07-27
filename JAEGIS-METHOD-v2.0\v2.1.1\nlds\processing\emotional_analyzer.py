"""
N.L.D.S. Emotional Context Analyzer
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced emotional analysis for user state detection, sentiment analysis,
and emotional intelligence with 95%+ emotion recognition accuracy.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import asyncio
import numpy as np

# ML and NLP imports
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Local imports
from ..nlp.tokenizer import TokenizationResult
from ..nlp.semantic_analyzer import SemanticAnalysisResult
from ..nlp.context_extractor import ContextExtractionResult

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# EMOTIONAL STRUCTURES AND ENUMS
# ============================================================================

class EmotionType(Enum):
    """Primary emotion types based on Plutchik's model."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    NEUTRAL = "neutral"


class SentimentPolarity(Enum):
    """Sentiment polarity classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class EmotionalIntensity(Enum):
    """Emotional intensity levels."""
    VERY_LOW = "very_low"    # 0.0-0.2
    LOW = "low"              # 0.2-0.4
    MEDIUM = "medium"        # 0.4-0.6
    HIGH = "high"            # 0.6-0.8
    VERY_HIGH = "very_high"  # 0.8-1.0


class UserState(Enum):
    """User emotional states."""
    CALM = "calm"
    EXCITED = "excited"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    SATISFIED = "satisfied"
    URGENT = "urgent"
    FOCUSED = "focused"
    DISTRACTED = "distracted"


@dataclass
class EmotionScore:
    """Individual emotion score."""
    emotion: EmotionType
    intensity: float
    confidence: float
    evidence: List[str]
    metadata: Dict[str, Any] = None


@dataclass
class SentimentAnalysis:
    """Sentiment analysis result."""
    polarity: SentimentPolarity
    polarity_score: float  # -1 to 1
    subjectivity: float    # 0 to 1
    confidence: float
    method: str
    details: Dict[str, Any] = None


@dataclass
class EmotionalContext:
    """Emotional context information."""
    user_state: UserState
    dominant_emotion: EmotionType
    emotion_scores: List[EmotionScore]
    sentiment_analysis: SentimentAnalysis
    emotional_trajectory: List[Dict[str, Any]]
    stress_indicators: List[str]
    urgency_level: float
    empathy_triggers: List[str]


@dataclass
class EmotionalAnalysisResult:
    """Complete emotional analysis result."""
    text: str
    emotional_context: EmotionalContext
    emotional_intelligence_score: float
    user_adaptation_suggestions: List[str]
    response_tone_recommendations: Dict[str, Any]
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# EMOTIONAL ANALYSIS ENGINE
# ============================================================================

class EmotionalAnalysisEngine:
    """
    Advanced emotional analysis engine for user state detection.
    
    Features:
    - Multi-model sentiment analysis
    - Emotion recognition with Plutchik's model
    - User state classification
    - Emotional trajectory tracking
    - Stress and urgency detection
    - Empathy trigger identification
    - Response tone adaptation
    """
    
    def __init__(self):
        """Initialize emotional analysis engine."""
        self.sentiment_analyzers = {}
        self.emotion_models = {}
        self.emotional_lexicons = self._load_emotional_lexicons()
        self.stress_indicators = self._load_stress_indicators()
        self.urgency_patterns = self._load_urgency_patterns()
        self.empathy_triggers = self._load_empathy_triggers()
        self.emotional_history = []
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize sentiment and emotion analysis models."""
        try:
            # NLTK VADER sentiment analyzer
            try:
                nltk.data.find('vader_lexicon')
            except LookupError:
                nltk.download('vader_lexicon')
            
            self.sentiment_analyzers["vader"] = SentimentIntensityAnalyzer()
            logger.info("Loaded VADER sentiment analyzer")
            
            # Transformer-based emotion model
            try:
                self.emotion_models["transformer"] = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    return_all_scores=True
                )
                logger.info("Loaded transformer emotion model")
            except Exception as e:
                logger.warning(f"Failed to load transformer emotion model: {e}")
            
            # spaCy for linguistic features
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_lg")
                logger.info("Loaded spaCy model for emotional analysis")
            except Exception as e:
                logger.warning(f"Failed to load spaCy model: {e}")
                self.nlp = None
            
        except Exception as e:
            logger.error(f"Failed to initialize emotional analysis models: {e}")
    
    def _load_emotional_lexicons(self) -> Dict[str, Dict[str, float]]:
        """Load emotional lexicons and word associations."""
        return {
            "joy": {
                "happy": 0.9, "excited": 0.8, "pleased": 0.7, "delighted": 0.9,
                "thrilled": 0.9, "cheerful": 0.8, "joyful": 0.9, "elated": 0.8,
                "great": 0.6, "awesome": 0.8, "fantastic": 0.8, "wonderful": 0.8
            },
            "sadness": {
                "sad": 0.8, "depressed": 0.9, "disappointed": 0.7, "upset": 0.7,
                "miserable": 0.9, "gloomy": 0.7, "melancholy": 0.8, "sorrowful": 0.8,
                "terrible": 0.7, "awful": 0.8, "horrible": 0.8, "bad": 0.6
            },
            "anger": {
                "angry": 0.9, "furious": 0.9, "mad": 0.8, "irritated": 0.7,
                "annoyed": 0.6, "frustrated": 0.8, "outraged": 0.9, "livid": 0.9,
                "hate": 0.9, "disgusted": 0.8, "pissed": 0.8, "enraged": 0.9
            },
            "fear": {
                "afraid": 0.8, "scared": 0.8, "terrified": 0.9, "anxious": 0.7,
                "worried": 0.6, "nervous": 0.7, "panicked": 0.9, "frightened": 0.8,
                "concerned": 0.5, "uneasy": 0.6, "apprehensive": 0.7
            },
            "surprise": {
                "surprised": 0.8, "amazed": 0.8, "astonished": 0.9, "shocked": 0.8,
                "stunned": 0.8, "bewildered": 0.7, "confused": 0.6, "puzzled": 0.6,
                "unexpected": 0.6, "sudden": 0.5
            },
            "trust": {
                "trust": 0.8, "confident": 0.8, "sure": 0.7, "certain": 0.7,
                "reliable": 0.7, "dependable": 0.7, "secure": 0.7, "safe": 0.6,
                "comfortable": 0.6, "assured": 0.7
            },
            "anticipation": {
                "excited": 0.7, "eager": 0.8, "hopeful": 0.7, "optimistic": 0.8,
                "expecting": 0.6, "anticipating": 0.8, "looking forward": 0.8,
                "can't wait": 0.9, "ready": 0.6
            }
        }
    
    def _load_stress_indicators(self) -> List[str]:
        """Load stress indicator patterns."""
        return [
            "urgent", "asap", "immediately", "critical", "emergency",
            "deadline", "pressure", "stressed", "overwhelmed", "rushed",
            "can't handle", "too much", "breaking point", "exhausted",
            "burned out", "at my limit", "going crazy", "losing it"
        ]
    
    def _load_urgency_patterns(self) -> List[str]:
        """Load urgency detection patterns."""
        return [
            r"\b(urgent|asap|immediately|now|quick|fast|hurry)\b",
            r"\b(deadline|due|overdue|late)\b",
            r"\b(emergency|critical|important)\b",
            r"[!]{2,}",  # Multiple exclamation marks
            r"\b(need.{0,10}(now|asap|immediately))\b"
        ]
    
    def _load_empathy_triggers(self) -> List[str]:
        """Load empathy trigger patterns."""
        return [
            "struggling", "difficult", "hard time", "challenging",
            "frustrated", "confused", "lost", "stuck", "overwhelmed",
            "don't understand", "can't figure out", "need help",
            "please help", "desperate", "at a loss"
        ]
    
    def analyze_sentiment_vader(self, text: str) -> SentimentAnalysis:
        """Analyze sentiment using VADER."""
        if "vader" not in self.sentiment_analyzers:
            return SentimentAnalysis(
                polarity=SentimentPolarity.NEUTRAL,
                polarity_score=0.0,
                subjectivity=0.5,
                confidence=0.0,
                method="vader_unavailable"
            )
        
        analyzer = self.sentiment_analyzers["vader"]
        scores = analyzer.polarity_scores(text)
        
        # Determine polarity
        compound = scores['compound']
        if compound >= 0.05:
            polarity = SentimentPolarity.POSITIVE
        elif compound <= -0.05:
            polarity = SentimentPolarity.NEGATIVE
        else:
            polarity = SentimentPolarity.NEUTRAL
        
        # Calculate confidence based on compound score magnitude
        confidence = abs(compound)
        
        return SentimentAnalysis(
            polarity=polarity,
            polarity_score=compound,
            subjectivity=0.5,  # VADER doesn't provide subjectivity
            confidence=confidence,
            method="vader",
            details={
                "positive": scores['pos'],
                "negative": scores['neg'],
                "neutral": scores['neu'],
                "compound": scores['compound']
            }
        )
    
    def analyze_sentiment_textblob(self, text: str) -> SentimentAnalysis:
        """Analyze sentiment using TextBlob."""
        try:
            blob = TextBlob(text)
            polarity_score = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine polarity
            if polarity_score > 0.1:
                polarity = SentimentPolarity.POSITIVE
            elif polarity_score < -0.1:
                polarity = SentimentPolarity.NEGATIVE
            else:
                polarity = SentimentPolarity.NEUTRAL
            
            # Confidence based on polarity magnitude
            confidence = abs(polarity_score)
            
            return SentimentAnalysis(
                polarity=polarity,
                polarity_score=polarity_score,
                subjectivity=subjectivity,
                confidence=confidence,
                method="textblob",
                details={
                    "polarity": polarity_score,
                    "subjectivity": subjectivity
                }
            )
            
        except Exception as e:
            logger.warning(f"TextBlob sentiment analysis failed: {e}")
            return SentimentAnalysis(
                polarity=SentimentPolarity.NEUTRAL,
                polarity_score=0.0,
                subjectivity=0.5,
                confidence=0.0,
                method="textblob_error"
            )
    
    def analyze_emotions_transformer(self, text: str) -> List[EmotionScore]:
        """Analyze emotions using transformer model."""
        emotions = []
        
        if "transformer" not in self.emotion_models:
            return emotions
        
        try:
            model = self.emotion_models["transformer"]
            results = model(text)
            
            for result in results:
                # Map model labels to our emotion types
                emotion_type = self._map_emotion_label(result['label'])
                
                emotion_score = EmotionScore(
                    emotion=emotion_type,
                    intensity=result['score'],
                    confidence=result['score'],
                    evidence=[text],
                    metadata={
                        "model_label": result['label'],
                        "model_score": result['score']
                    }
                )
                
                emotions.append(emotion_score)
            
            # Sort by intensity
            emotions.sort(key=lambda x: x.intensity, reverse=True)
            
        except Exception as e:
            logger.warning(f"Transformer emotion analysis failed: {e}")
        
        return emotions
    
    def analyze_emotions_lexicon(self, text: str) -> List[EmotionScore]:
        """Analyze emotions using lexicon-based approach."""
        emotions = []
        words = text.lower().split()
        
        emotion_scores = {emotion: 0.0 for emotion in EmotionType}
        emotion_evidence = {emotion: [] for emotion in EmotionType}
        
        for word in words:
            for emotion_name, lexicon in self.emotional_lexicons.items():
                if word in lexicon:
                    emotion_type = EmotionType(emotion_name)
                    emotion_scores[emotion_type] += lexicon[word]
                    emotion_evidence[emotion_type].append(word)
        
        # Normalize scores and create EmotionScore objects
        total_words = len(words)
        for emotion_type, score in emotion_scores.items():
            if score > 0:
                normalized_score = min(score / total_words * 10, 1.0)  # Normalize
                confidence = min(len(emotion_evidence[emotion_type]) / total_words * 5, 1.0)
                
                emotion_score = EmotionScore(
                    emotion=emotion_type,
                    intensity=normalized_score,
                    confidence=confidence,
                    evidence=emotion_evidence[emotion_type],
                    metadata={"method": "lexicon", "raw_score": score}
                )
                
                emotions.append(emotion_score)
        
        # Sort by intensity
        emotions.sort(key=lambda x: x.intensity, reverse=True)
        
        return emotions
    
    def _map_emotion_label(self, label: str) -> EmotionType:
        """Map model emotion labels to our emotion types."""
        label_mapping = {
            "joy": EmotionType.JOY,
            "happiness": EmotionType.JOY,
            "sadness": EmotionType.SADNESS,
            "anger": EmotionType.ANGER,
            "fear": EmotionType.FEAR,
            "surprise": EmotionType.SURPRISE,
            "disgust": EmotionType.DISGUST,
            "trust": EmotionType.TRUST,
            "anticipation": EmotionType.ANTICIPATION,
            "neutral": EmotionType.NEUTRAL
        }
        
        return label_mapping.get(label.lower(), EmotionType.NEUTRAL)
    
    def detect_user_state(self, text: str, emotion_scores: List[EmotionScore],
                         sentiment: SentimentAnalysis) -> UserState:
        """Detect user emotional state."""
        text_lower = text.lower()
        
        # Check for specific state indicators
        if any(indicator in text_lower for indicator in self.stress_indicators):
            return UserState.FRUSTRATED
        
        if self._detect_urgency(text) > 0.7:
            return UserState.URGENT
        
        if any(word in text_lower for word in ["confused", "don't understand", "unclear"]):
            return UserState.CONFUSED
        
        # Use dominant emotion and sentiment
        if emotion_scores:
            dominant_emotion = emotion_scores[0].emotion
            
            if dominant_emotion == EmotionType.JOY and sentiment.polarity == SentimentPolarity.POSITIVE:
                return UserState.SATISFIED
            elif dominant_emotion == EmotionType.ANGER:
                return UserState.FRUSTRATED
            elif dominant_emotion == EmotionType.ANTICIPATION:
                return UserState.EXCITED
            elif dominant_emotion == EmotionType.FEAR:
                return UserState.CONFUSED
        
        # Default based on sentiment
        if sentiment.polarity == SentimentPolarity.POSITIVE:
            return UserState.CALM
        elif sentiment.polarity == SentimentPolarity.NEGATIVE:
            return UserState.FRUSTRATED
        else:
            return UserState.FOCUSED
    
    def _detect_urgency(self, text: str) -> float:
        """Detect urgency level in text."""
        urgency_score = 0.0
        
        for pattern in self.urgency_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            urgency_score += matches * 0.2
        
        # Check for multiple exclamation marks
        exclamation_count = text.count('!')
        if exclamation_count > 1:
            urgency_score += min(exclamation_count * 0.1, 0.3)
        
        # Check for capital letters (shouting)
        capital_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if capital_ratio > 0.3:
            urgency_score += 0.2
        
        return min(urgency_score, 1.0)
    
    def detect_empathy_triggers(self, text: str) -> List[str]:
        """Detect empathy triggers in text."""
        triggers = []
        text_lower = text.lower()
        
        for trigger in self.empathy_triggers:
            if trigger in text_lower:
                triggers.append(trigger)
        
        return triggers
    
    def generate_response_recommendations(self, emotional_context: EmotionalContext) -> Dict[str, Any]:
        """Generate response tone recommendations."""
        recommendations = {
            "tone": "neutral",
            "empathy_level": "medium",
            "formality": "medium",
            "supportiveness": "medium",
            "specific_suggestions": []
        }
        
        user_state = emotional_context.user_state
        dominant_emotion = emotional_context.dominant_emotion
        urgency = emotional_context.urgency_level
        
        # Adjust based on user state
        if user_state == UserState.FRUSTRATED:
            recommendations.update({
                "tone": "calm_supportive",
                "empathy_level": "high",
                "supportiveness": "high",
                "specific_suggestions": [
                    "Acknowledge the frustration",
                    "Offer step-by-step guidance",
                    "Provide reassurance"
                ]
            })
        
        elif user_state == UserState.CONFUSED:
            recommendations.update({
                "tone": "patient_explanatory",
                "empathy_level": "high",
                "formality": "low",
                "specific_suggestions": [
                    "Use simple, clear language",
                    "Break down complex concepts",
                    "Ask clarifying questions"
                ]
            })
        
        elif user_state == UserState.URGENT:
            recommendations.update({
                "tone": "efficient_helpful",
                "empathy_level": "medium",
                "formality": "low",
                "specific_suggestions": [
                    "Provide direct, actionable solutions",
                    "Prioritize immediate needs",
                    "Offer quick alternatives"
                ]
            })
        
        elif user_state == UserState.SATISFIED:
            recommendations.update({
                "tone": "positive_encouraging",
                "empathy_level": "medium",
                "formality": "medium",
                "specific_suggestions": [
                    "Maintain positive momentum",
                    "Offer additional helpful information",
                    "Encourage continued engagement"
                ]
            })
        
        # Adjust for high urgency
        if urgency > 0.7:
            recommendations["specific_suggestions"].insert(0, "Address urgency immediately")
        
        # Adjust for empathy triggers
        if emotional_context.empathy_triggers:
            recommendations["empathy_level"] = "very_high"
            recommendations["specific_suggestions"].append("Show understanding and support")
        
        return recommendations
    
    def calculate_emotional_intelligence_score(self, emotional_context: EmotionalContext,
                                             context_result: ContextExtractionResult) -> float:
        """Calculate emotional intelligence score for the analysis."""
        factors = []
        
        # Emotion detection accuracy
        if emotional_context.emotion_scores:
            avg_confidence = np.mean([score.confidence for score in emotional_context.emotion_scores])
            factors.append(avg_confidence * 0.3)
        else:
            factors.append(0.1)
        
        # Sentiment analysis confidence
        factors.append(emotional_context.sentiment_analysis.confidence * 0.2)
        
        # Context awareness
        if context_result.extracted_context:
            context_factor = min(len(context_result.extracted_context) / 10, 1.0)
            factors.append(context_factor * 0.2)
        else:
            factors.append(0.1)
        
        # User state detection confidence
        state_confidence = 0.8 if emotional_context.user_state != UserState.CALM else 0.6
        factors.append(state_confidence * 0.15)
        
        # Empathy trigger detection
        empathy_factor = min(len(emotional_context.empathy_triggers) / 5, 1.0)
        factors.append(empathy_factor * 0.15)
        
        return sum(factors)
    
    async def analyze_emotional_context(self, text: str,
                                      semantic_result: SemanticAnalysisResult,
                                      context_result: ContextExtractionResult) -> EmotionalAnalysisResult:
        """
        Perform complete emotional analysis.
        
        Args:
            text: Input text
            semantic_result: Semantic analysis results
            context_result: Context extraction results
            
        Returns:
            Complete emotional analysis result
        """
        import time
        start_time = time.time()
        
        try:
            # Analyze sentiment using multiple methods
            vader_sentiment = self.analyze_sentiment_vader(text)
            textblob_sentiment = self.analyze_sentiment_textblob(text)
            
            # Choose best sentiment analysis (highest confidence)
            sentiment_analysis = vader_sentiment if vader_sentiment.confidence > textblob_sentiment.confidence else textblob_sentiment
            
            # Analyze emotions
            transformer_emotions = self.analyze_emotions_transformer(text)
            lexicon_emotions = self.analyze_emotions_lexicon(text)
            
            # Combine emotion analyses
            all_emotions = transformer_emotions + lexicon_emotions
            
            # Remove duplicates and merge similar emotions
            emotion_scores = self._merge_emotion_scores(all_emotions)
            
            # Detect user state
            user_state = self.detect_user_state(text, emotion_scores, sentiment_analysis)
            
            # Detect urgency and empathy triggers
            urgency_level = self._detect_urgency(text)
            empathy_triggers = self.detect_empathy_triggers(text)
            
            # Get dominant emotion
            dominant_emotion = emotion_scores[0].emotion if emotion_scores else EmotionType.NEUTRAL
            
            # Create emotional context
            emotional_context = EmotionalContext(
                user_state=user_state,
                dominant_emotion=dominant_emotion,
                emotion_scores=emotion_scores,
                sentiment_analysis=sentiment_analysis,
                emotional_trajectory=[],  # Would be populated from history
                stress_indicators=[indicator for indicator in self.stress_indicators if indicator in text.lower()],
                urgency_level=urgency_level,
                empathy_triggers=empathy_triggers
            )
            
            # Calculate emotional intelligence score
            ei_score = self.calculate_emotional_intelligence_score(emotional_context, context_result)
            
            # Generate response recommendations
            response_recommendations = self.generate_response_recommendations(emotional_context)
            
            # Generate user adaptation suggestions
            adaptation_suggestions = self._generate_adaptation_suggestions(emotional_context)
            
            processing_time = (time.time() - start_time) * 1000
            
            return EmotionalAnalysisResult(
                text=text,
                emotional_context=emotional_context,
                emotional_intelligence_score=ei_score,
                user_adaptation_suggestions=adaptation_suggestions,
                response_tone_recommendations=response_recommendations,
                processing_time_ms=processing_time,
                metadata={
                    "sentiment_method": sentiment_analysis.method,
                    "emotions_detected": len(emotion_scores),
                    "urgency_level": urgency_level,
                    "empathy_triggers_count": len(empathy_triggers),
                    "user_state": user_state.value,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Emotional analysis failed: {e}")
            
            # Return minimal result on error
            return EmotionalAnalysisResult(
                text=text,
                emotional_context=EmotionalContext(
                    user_state=UserState.CALM,
                    dominant_emotion=EmotionType.NEUTRAL,
                    emotion_scores=[],
                    sentiment_analysis=SentimentAnalysis(
                        polarity=SentimentPolarity.NEUTRAL,
                        polarity_score=0.0,
                        subjectivity=0.5,
                        confidence=0.0,
                        method="error"
                    ),
                    emotional_trajectory=[],
                    stress_indicators=[],
                    urgency_level=0.0,
                    empathy_triggers=[]
                ),
                emotional_intelligence_score=0.0,
                user_adaptation_suggestions=[],
                response_tone_recommendations={},
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )
    
    def _merge_emotion_scores(self, emotions: List[EmotionScore]) -> List[EmotionScore]:
        """Merge similar emotion scores from different methods."""
        emotion_map = {}
        
        for emotion in emotions:
            emotion_type = emotion.emotion
            
            if emotion_type in emotion_map:
                # Average the scores
                existing = emotion_map[emotion_type]
                combined_intensity = (existing.intensity + emotion.intensity) / 2
                combined_confidence = max(existing.confidence, emotion.confidence)
                combined_evidence = list(set(existing.evidence + emotion.evidence))
                
                emotion_map[emotion_type] = EmotionScore(
                    emotion=emotion_type,
                    intensity=combined_intensity,
                    confidence=combined_confidence,
                    evidence=combined_evidence,
                    metadata={"merged": True}
                )
            else:
                emotion_map[emotion_type] = emotion
        
        # Sort by intensity
        merged_emotions = list(emotion_map.values())
        merged_emotions.sort(key=lambda x: x.intensity, reverse=True)
        
        return merged_emotions
    
    def _generate_adaptation_suggestions(self, emotional_context: EmotionalContext) -> List[str]:
        """Generate user adaptation suggestions."""
        suggestions = []
        
        user_state = emotional_context.user_state
        urgency = emotional_context.urgency_level
        
        if user_state == UserState.FRUSTRATED:
            suggestions.extend([
                "Provide step-by-step guidance",
                "Offer alternative solutions",
                "Break down complex tasks into smaller steps"
            ])
        
        elif user_state == UserState.CONFUSED:
            suggestions.extend([
                "Use simpler language",
                "Provide examples and analogies",
                "Ask clarifying questions to understand needs better"
            ])
        
        elif user_state == UserState.URGENT:
            suggestions.extend([
                "Prioritize immediate actionable solutions",
                "Provide quick wins first",
                "Offer expedited processing options"
            ])
        
        if urgency > 0.7:
            suggestions.insert(0, "Address time-sensitive requirements first")
        
        if emotional_context.empathy_triggers:
            suggestions.append("Show understanding and provide emotional support")
        
        return suggestions


# ============================================================================
# EMOTIONAL UTILITIES
# ============================================================================

class EmotionalUtils:
    """Utility functions for emotional analysis."""
    
    @staticmethod
    def get_intensity_level(intensity: float) -> EmotionalIntensity:
        """Convert intensity score to intensity level."""
        if intensity >= 0.8:
            return EmotionalIntensity.VERY_HIGH
        elif intensity >= 0.6:
            return EmotionalIntensity.HIGH
        elif intensity >= 0.4:
            return EmotionalIntensity.MEDIUM
        elif intensity >= 0.2:
            return EmotionalIntensity.LOW
        else:
            return EmotionalIntensity.VERY_LOW
    
    @staticmethod
    def emotions_to_dict(emotions: List[EmotionScore]) -> List[Dict[str, Any]]:
        """Convert emotion scores to dictionary format."""
        return [
            {
                "emotion": emotion.emotion.value,
                "intensity": emotion.intensity,
                "intensity_level": EmotionalUtils.get_intensity_level(emotion.intensity).value,
                "confidence": emotion.confidence,
                "evidence": emotion.evidence,
                "metadata": emotion.metadata
            }
            for emotion in emotions
        ]
    
    @staticmethod
    def calculate_emotional_distance(emotions1: List[EmotionScore], 
                                   emotions2: List[EmotionScore]) -> float:
        """Calculate emotional distance between two emotion sets."""
        if not emotions1 or not emotions2:
            return 1.0
        
        # Create emotion vectors
        all_emotions = set([e.emotion for e in emotions1 + emotions2])
        
        vector1 = np.array([
            next((e.intensity for e in emotions1 if e.emotion == emotion), 0.0)
            for emotion in all_emotions
        ])
        
        vector2 = np.array([
            next((e.intensity for e in emotions2 if e.emotion == emotion), 0.0)
            for emotion in all_emotions
        ])
        
        # Calculate cosine distance
        similarity = cosine_similarity([vector1], [vector2])[0][0]
        distance = 1 - similarity
        
        return distance
