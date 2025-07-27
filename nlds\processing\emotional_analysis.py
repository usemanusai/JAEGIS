"""
N.L.D.S. Emotional Context Analyzer
Advanced sentiment analysis and emotional state detection using deep learning models
"""

import numpy as np
import spacy
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import re
import time
from collections import defaultdict
import json

logger = logging.getLogger(__name__)


class EmotionType(str, Enum):
    """Primary emotion types based on Plutchik's wheel."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"


class SentimentPolarity(str, Enum):
    """Sentiment polarity classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class EmotionalIntensity(str, Enum):
    """Emotional intensity levels."""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class UrgencyLevel(str, Enum):
    """Urgency level indicators."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


@dataclass
class EmotionScore:
    """Individual emotion score."""
    emotion: EmotionType
    intensity: float
    confidence: float
    evidence: List[str]


@dataclass
class SentimentAnalysis:
    """Sentiment analysis result."""
    polarity: SentimentPolarity
    score: float
    confidence: float
    subjectivity: float


@dataclass
class EmotionalState:
    """Complete emotional state representation."""
    primary_emotion: EmotionType
    emotion_scores: List[EmotionScore]
    sentiment: SentimentAnalysis
    emotional_intensity: EmotionalIntensity
    urgency_level: UrgencyLevel
    stress_indicators: List[str]
    satisfaction_indicators: List[str]
    frustration_indicators: List[str]


@dataclass
class EmotionalContext:
    """Emotional context information."""
    user_mood: str
    communication_style: str
    emotional_triggers: List[str]
    preferred_response_tone: str
    emotional_history: List[Dict[str, Any]]


@dataclass
class EmotionalAnalysisResult:
    """Complete emotional analysis result."""
    emotional_state: EmotionalState
    emotional_context: EmotionalContext
    processing_recommendations: List[str]
    response_adaptations: List[str]
    confidence_score: float
    processing_time_ms: float


class EmotionalContextAnalyzer:
    """
    Advanced emotional context analyzer for sentiment analysis and emotional state detection.
    
    Uses multiple approaches including lexicon-based analysis, pattern recognition,
    and contextual understanding to provide comprehensive emotional intelligence.
    """
    
    def __init__(self):
        # Initialize spaCy for linguistic analysis
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            try:
                self.nlp = spacy.load("en_core_web_md")
            except OSError:
                self.nlp = spacy.load("en_core_web_sm")
        
        # Emotion lexicons and patterns
        self.emotion_lexicons = self._initialize_emotion_lexicons()
        
        # Sentiment patterns
        self.sentiment_patterns = self._initialize_sentiment_patterns()
        
        # Urgency indicators
        self.urgency_indicators = self._initialize_urgency_indicators()
        
        # Stress and satisfaction patterns
        self.stress_patterns = self._initialize_stress_patterns()
        self.satisfaction_patterns = self._initialize_satisfaction_patterns()
        
        # Communication style indicators
        self.communication_styles = self._initialize_communication_styles()
        
        # Emotional intensifiers and diminishers
        self.intensifiers = self._initialize_intensifiers()
        
        logger.info("Emotional Context Analyzer initialized")
    
    def _initialize_emotion_lexicons(self) -> Dict[EmotionType, Dict[str, float]]:
        """Initialize emotion lexicons with word-emotion mappings."""
        
        return {
            EmotionType.JOY: {
                "happy": 0.8, "excited": 0.9, "pleased": 0.7, "delighted": 0.8,
                "thrilled": 0.9, "cheerful": 0.7, "elated": 0.8, "joyful": 0.9,
                "glad": 0.6, "satisfied": 0.7, "content": 0.6, "euphoric": 1.0,
                "ecstatic": 0.9, "blissful": 0.8, "overjoyed": 0.9, "wonderful": 0.7,
                "fantastic": 0.8, "amazing": 0.8, "excellent": 0.7, "great": 0.6
            },
            
            EmotionType.SADNESS: {
                "sad": 0.8, "depressed": 0.9, "disappointed": 0.7, "unhappy": 0.7,
                "miserable": 0.9, "gloomy": 0.6, "melancholy": 0.7, "sorrowful": 0.8,
                "dejected": 0.7, "downhearted": 0.7, "disheartened": 0.8, "blue": 0.6,
                "upset": 0.6, "hurt": 0.7, "heartbroken": 0.9, "devastated": 0.9,
                "crushed": 0.8, "terrible": 0.7, "awful": 0.8, "horrible": 0.8
            },
            
            EmotionType.ANGER: {
                "angry": 0.8, "furious": 0.9, "mad": 0.7, "irritated": 0.6,
                "annoyed": 0.5, "frustrated": 0.7, "outraged": 0.9, "livid": 0.9,
                "enraged": 1.0, "irate": 0.8, "incensed": 0.8, "infuriated": 0.9,
                "aggravated": 0.6, "exasperated": 0.7, "indignant": 0.7, "resentful": 0.6,
                "hostile": 0.8, "bitter": 0.7, "disgusted": 0.7, "hate": 0.9
            },
            
            EmotionType.FEAR: {
                "afraid": 0.8, "scared": 0.7, "terrified": 0.9, "frightened": 0.8,
                "anxious": 0.7, "worried": 0.6, "nervous": 0.6, "panicked": 0.9,
                "alarmed": 0.7, "concerned": 0.5, "apprehensive": 0.6, "uneasy": 0.5,
                "distressed": 0.7, "troubled": 0.6, "fearful": 0.8, "intimidated": 0.7,
                "overwhelmed": 0.7, "stressed": 0.6, "tense": 0.5, "uncertain": 0.4
            },
            
            EmotionType.SURPRISE: {
                "surprised": 0.7, "amazed": 0.8, "astonished": 0.8, "shocked": 0.8,
                "stunned": 0.8, "bewildered": 0.6, "confused": 0.5, "perplexed": 0.5,
                "puzzled": 0.4, "baffled": 0.6, "startled": 0.7, "unexpected": 0.6,
                "sudden": 0.5, "incredible": 0.7, "unbelievable": 0.7, "remarkable": 0.6
            },
            
            EmotionType.TRUST: {
                "trust": 0.8, "confident": 0.7, "secure": 0.6, "comfortable": 0.6,
                "reliable": 0.7, "dependable": 0.7, "faithful": 0.8, "loyal": 0.7,
                "honest": 0.6, "genuine": 0.6, "authentic": 0.6, "credible": 0.6,
                "trustworthy": 0.8, "assured": 0.6, "certain": 0.6, "convinced": 0.7
            },
            
            EmotionType.ANTICIPATION: {
                "excited": 0.8, "eager": 0.7, "hopeful": 0.7, "optimistic": 0.7,
                "enthusiastic": 0.8, "keen": 0.6, "anticipating": 0.8, "expecting": 0.6,
                "looking forward": 0.7, "can't wait": 0.8, "impatient": 0.6, "ready": 0.5,
                "prepared": 0.5, "motivated": 0.6, "determined": 0.7, "ambitious": 0.6
            }
        }
    
    def _initialize_sentiment_patterns(self) -> Dict[str, List[str]]:
        """Initialize sentiment analysis patterns."""
        
        return {
            "positive_patterns": [
                r"\b(?:love|like|enjoy|appreciate|adore)\b",
                r"\b(?:excellent|amazing|fantastic|wonderful|great)\b",
                r"\b(?:perfect|brilliant|outstanding|superb)\b",
                r"\b(?:thank you|thanks|grateful|pleased)\b",
                r"\b(?:successful|achievement|accomplish|succeed)\b"
            ],
            
            "negative_patterns": [
                r"\b(?:hate|dislike|despise|detest|loathe)\b",
                r"\b(?:terrible|awful|horrible|disgusting|appalling)\b",
                r"\b(?:failed|failure|disaster|catastrophe|nightmare)\b",
                r"\b(?:problem|issue|trouble|difficulty|challenge)\b",
                r"\b(?:broken|damaged|corrupted|error|bug)\b"
            ],
            
            "neutral_patterns": [
                r"\b(?:okay|fine|alright|acceptable|adequate)\b",
                r"\b(?:normal|standard|typical|regular|usual)\b",
                r"\b(?:information|data|details|facts|report)\b"
            ]
        }
    
    def _initialize_urgency_indicators(self) -> Dict[UrgencyLevel, List[str]]:
        """Initialize urgency level indicators."""
        
        return {
            UrgencyLevel.CRITICAL: [
                "emergency", "urgent", "critical", "asap", "immediately", "now",
                "crisis", "disaster", "catastrophe", "breaking", "severe"
            ],
            
            UrgencyLevel.HIGH: [
                "important", "priority", "soon", "quickly", "fast", "rapid",
                "pressing", "time-sensitive", "deadline", "rush"
            ],
            
            UrgencyLevel.MEDIUM: [
                "when possible", "convenient", "reasonable time", "moderate",
                "standard", "normal priority", "regular"
            ],
            
            UrgencyLevel.LOW: [
                "eventually", "sometime", "when you can", "no rush", "low priority",
                "later", "future", "optional"
            ]
        }
    
    def _initialize_stress_patterns(self) -> List[str]:
        """Initialize stress indicator patterns."""
        
        return [
            r"\b(?:stressed|overwhelmed|exhausted|burned out)\b",
            r"\b(?:can't handle|too much|breaking point)\b",
            r"\b(?:pressure|deadline|crunch time)\b",
            r"\b(?:frustrated|fed up|had enough)\b",
            r"\b(?:difficult|challenging|struggling)\b",
            r"(?:!!!|multiple exclamation)",
            r"(?:CAPS LOCK|ALL CAPS)",
            r"\b(?:help|stuck|lost|confused)\b"
        ]
    
    def _initialize_satisfaction_patterns(self) -> List[str]:
        """Initialize satisfaction indicator patterns."""
        
        return [
            r"\b(?:satisfied|pleased|happy|content)\b",
            r"\b(?:working well|smooth|seamless)\b",
            r"\b(?:exactly what|perfect|ideal)\b",
            r"\b(?:thank you|appreciate|grateful)\b",
            r"\b(?:exceeded expectations|beyond expectations)\b",
            r"\b(?:impressed|amazed|surprised)\b",
            r"\b(?:recommend|endorse|approve)\b"
        ]
    
    def _initialize_communication_styles(self) -> Dict[str, List[str]]:
        """Initialize communication style indicators."""
        
        return {
            "formal": [
                "please", "kindly", "would you", "could you", "may I",
                "thank you", "sincerely", "respectfully", "professional"
            ],
            
            "casual": [
                "hey", "hi", "thanks", "cool", "awesome", "yeah", "ok",
                "sure", "no problem", "sounds good"
            ],
            
            "technical": [
                "implement", "configure", "optimize", "debug", "deploy",
                "architecture", "framework", "algorithm", "protocol"
            ],
            
            "urgent": [
                "asap", "urgent", "immediately", "now", "critical", "emergency",
                "rush", "deadline", "time-sensitive"
            ],
            
            "collaborative": [
                "we", "us", "our", "together", "team", "collaborate",
                "work with", "partner", "joint", "shared"
            ]
        }
    
    def _initialize_intensifiers(self) -> Dict[str, float]:
        """Initialize emotional intensifiers and diminishers."""
        
        return {
            # Intensifiers (multiply emotion score)
            "very": 1.3,
            "extremely": 1.5,
            "incredibly": 1.4,
            "absolutely": 1.4,
            "completely": 1.3,
            "totally": 1.3,
            "really": 1.2,
            "quite": 1.1,
            "pretty": 1.1,
            "so": 1.2,
            "super": 1.3,
            "ultra": 1.4,
            
            # Diminishers (reduce emotion score)
            "slightly": 0.7,
            "somewhat": 0.8,
            "a bit": 0.8,
            "a little": 0.8,
            "kind of": 0.7,
            "sort of": 0.7,
            "rather": 0.9,
            "fairly": 0.9,
            "moderately": 0.8,
            "mildly": 0.6
        }
    
    def analyze_emotional_context(self, text: str, 
                                user_history: Optional[List[Dict[str, Any]]] = None) -> EmotionalAnalysisResult:
        """Analyze emotional context of input text."""
        
        start_time = time.time()
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Analyze emotions
        emotion_scores = self._analyze_emotions(doc, text)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(doc, text)
        
        # Determine emotional intensity
        emotional_intensity = self._determine_emotional_intensity(emotion_scores)
        
        # Assess urgency level
        urgency_level = self._assess_urgency_level(text)
        
        # Identify stress indicators
        stress_indicators = self._identify_stress_indicators(text)
        
        # Identify satisfaction indicators
        satisfaction_indicators = self._identify_satisfaction_indicators(text)
        
        # Identify frustration indicators
        frustration_indicators = self._identify_frustration_indicators(text)
        
        # Determine primary emotion
        primary_emotion = self._determine_primary_emotion(emotion_scores)
        
        # Build emotional state
        emotional_state = EmotionalState(
            primary_emotion=primary_emotion,
            emotion_scores=emotion_scores,
            sentiment=sentiment,
            emotional_intensity=emotional_intensity,
            urgency_level=urgency_level,
            stress_indicators=stress_indicators,
            satisfaction_indicators=satisfaction_indicators,
            frustration_indicators=frustration_indicators
        )
        
        # Analyze emotional context
        emotional_context = self._analyze_emotional_context(text, user_history)
        
        # Generate processing recommendations
        processing_recommendations = self._generate_processing_recommendations(emotional_state)
        
        # Generate response adaptations
        response_adaptations = self._generate_response_adaptations(emotional_state, emotional_context)
        
        # Calculate overall confidence
        confidence_score = self._calculate_emotional_confidence(emotional_state, sentiment)
        
        processing_time = (time.time() - start_time) * 1000
        
        return EmotionalAnalysisResult(
            emotional_state=emotional_state,
            emotional_context=emotional_context,
            processing_recommendations=processing_recommendations,
            response_adaptations=response_adaptations,
            confidence_score=confidence_score,
            processing_time_ms=processing_time
        )
    
    def _analyze_emotions(self, doc, text: str) -> List[EmotionScore]:
        """Analyze emotions in the text."""
        
        emotion_scores = []
        text_lower = text.lower()
        
        for emotion_type, word_scores in self.emotion_lexicons.items():
            total_score = 0.0
            evidence = []
            word_count = 0
            
            for word, base_score in word_scores.items():
                if word in text_lower:
                    # Apply intensifiers/diminishers
                    adjusted_score = self._apply_intensifiers(word, text_lower, base_score)
                    total_score += adjusted_score
                    evidence.append(word)
                    word_count += 1
            
            if word_count > 0:
                # Normalize by word count and text length
                intensity = min(1.0, total_score / word_count)
                confidence = min(1.0, word_count / 10.0)  # More words = higher confidence
                
                emotion_score = EmotionScore(
                    emotion=emotion_type,
                    intensity=intensity,
                    confidence=confidence,
                    evidence=evidence
                )
                
                emotion_scores.append(emotion_score)
        
        return sorted(emotion_scores, key=lambda x: x.intensity, reverse=True)
    
    def _apply_intensifiers(self, word: str, text: str, base_score: float) -> float:
        """Apply intensifiers and diminishers to emotion scores."""
        
        # Find the word in context
        word_index = text.find(word)
        if word_index == -1:
            return base_score
        
        # Look for intensifiers/diminishers in nearby words
        context_start = max(0, word_index - 50)
        context_end = min(len(text), word_index + len(word) + 50)
        context = text[context_start:context_end]
        
        multiplier = 1.0
        
        for intensifier, factor in self.intensifiers.items():
            if intensifier in context:
                multiplier *= factor
                break  # Apply only the first found intensifier
        
        return base_score * multiplier
    
    def _analyze_sentiment(self, doc, text: str) -> SentimentAnalysis:
        """Analyze sentiment polarity and subjectivity."""
        
        positive_score = 0.0
        negative_score = 0.0
        neutral_score = 0.0
        
        # Pattern-based sentiment analysis
        for pattern in self.sentiment_patterns["positive_patterns"]:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            positive_score += matches * 0.3
        
        for pattern in self.sentiment_patterns["negative_patterns"]:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            negative_score += matches * 0.3
        
        for pattern in self.sentiment_patterns["neutral_patterns"]:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            neutral_score += matches * 0.2
        
        # Normalize scores
        total_score = positive_score + negative_score + neutral_score
        
        if total_score > 0:
            positive_score /= total_score
            negative_score /= total_score
            neutral_score /= total_score
        
        # Determine polarity
        if positive_score > negative_score and positive_score > neutral_score:
            polarity = SentimentPolarity.POSITIVE
            score = positive_score
        elif negative_score > positive_score and negative_score > neutral_score:
            polarity = SentimentPolarity.NEGATIVE
            score = negative_score
        elif abs(positive_score - negative_score) < 0.1:
            polarity = SentimentPolarity.MIXED
            score = 0.5
        else:
            polarity = SentimentPolarity.NEUTRAL
            score = neutral_score
        
        # Calculate confidence and subjectivity
        confidence = max(positive_score, negative_score, neutral_score)
        subjectivity = 1.0 - neutral_score  # Higher subjectivity = less neutral
        
        return SentimentAnalysis(
            polarity=polarity,
            score=score,
            confidence=confidence,
            subjectivity=subjectivity
        )
    
    def _determine_emotional_intensity(self, emotion_scores: List[EmotionScore]) -> EmotionalIntensity:
        """Determine overall emotional intensity."""
        
        if not emotion_scores:
            return EmotionalIntensity.VERY_LOW
        
        # Get the highest emotion intensity
        max_intensity = max(score.intensity for score in emotion_scores)
        
        if max_intensity >= 0.8:
            return EmotionalIntensity.VERY_HIGH
        elif max_intensity >= 0.6:
            return EmotionalIntensity.HIGH
        elif max_intensity >= 0.4:
            return EmotionalIntensity.MODERATE
        elif max_intensity >= 0.2:
            return EmotionalIntensity.LOW
        else:
            return EmotionalIntensity.VERY_LOW
    
    def _assess_urgency_level(self, text: str) -> UrgencyLevel:
        """Assess urgency level from text."""
        
        text_lower = text.lower()
        
        for urgency_level, indicators in self.urgency_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return urgency_level
        
        return UrgencyLevel.NONE
    
    def _identify_stress_indicators(self, text: str) -> List[str]:
        """Identify stress indicators in text."""
        
        indicators = []
        
        for pattern in self.stress_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            indicators.extend(matches)
        
        # Check for excessive punctuation
        if "!!!" in text or "???" in text:
            indicators.append("excessive_punctuation")
        
        # Check for all caps
        if re.search(r'\b[A-Z]{3,}\b', text):
            indicators.append("all_caps")
        
        return list(set(indicators))  # Remove duplicates
    
    def _identify_satisfaction_indicators(self, text: str) -> List[str]:
        """Identify satisfaction indicators in text."""
        
        indicators = []
        
        for pattern in self.satisfaction_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            indicators.extend(matches)
        
        return list(set(indicators))  # Remove duplicates
    
    def _identify_frustration_indicators(self, text: str) -> List[str]:
        """Identify frustration indicators in text."""
        
        frustration_patterns = [
            r"\b(?:frustrated|annoyed|irritated|fed up)\b",
            r"\b(?:why|how come|what's wrong)\b",
            r"\b(?:again|still|keep|repeatedly)\b",
            r"\b(?:doesn't work|not working|broken)\b",
            r"\b(?:tried everything|nothing works)\b"
        ]
        
        indicators = []
        
        for pattern in frustration_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            indicators.extend(matches)
        
        return list(set(indicators))  # Remove duplicates
    
    def _determine_primary_emotion(self, emotion_scores: List[EmotionScore]) -> EmotionType:
        """Determine the primary emotion."""
        
        if not emotion_scores:
            return EmotionType.TRUST  # Default neutral emotion
        
        # Return the emotion with highest intensity
        return emotion_scores[0].emotion
    
    def _analyze_emotional_context(self, text: str, 
                                 user_history: Optional[List[Dict[str, Any]]]) -> EmotionalContext:
        """Analyze broader emotional context."""
        
        # Determine communication style
        communication_style = self._determine_communication_style(text)
        
        # Identify emotional triggers
        emotional_triggers = self._identify_emotional_triggers(text)
        
        # Determine preferred response tone
        preferred_tone = self._determine_preferred_response_tone(text, communication_style)
        
        # Analyze user mood from history
        user_mood = self._analyze_user_mood(user_history) if user_history else "neutral"
        
        return EmotionalContext(
            user_mood=user_mood,
            communication_style=communication_style,
            emotional_triggers=emotional_triggers,
            preferred_response_tone=preferred_tone,
            emotional_history=user_history or []
        )
    
    def _determine_communication_style(self, text: str) -> str:
        """Determine communication style from text."""
        
        text_lower = text.lower()
        style_scores = {}
        
        for style, indicators in self.communication_styles.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            style_scores[style] = score
        
        # Return style with highest score
        if style_scores:
            return max(style_scores, key=style_scores.get)
        
        return "neutral"
    
    def _identify_emotional_triggers(self, text: str) -> List[str]:
        """Identify potential emotional triggers."""
        
        triggers = []
        text_lower = text.lower()
        
        # Common emotional triggers
        trigger_patterns = [
            "deadline", "pressure", "stress", "problem", "issue", "error",
            "failure", "broken", "urgent", "critical", "emergency"
        ]
        
        for trigger in trigger_patterns:
            if trigger in text_lower:
                triggers.append(trigger)
        
        return triggers
    
    def _determine_preferred_response_tone(self, text: str, communication_style: str) -> str:
        """Determine preferred response tone."""
        
        if communication_style == "formal":
            return "professional"
        elif communication_style == "casual":
            return "friendly"
        elif communication_style == "technical":
            return "precise"
        elif communication_style == "urgent":
            return "direct"
        elif communication_style == "collaborative":
            return "supportive"
        else:
            return "balanced"
    
    def _analyze_user_mood(self, user_history: List[Dict[str, Any]]) -> str:
        """Analyze user mood from historical interactions."""
        
        if not user_history:
            return "neutral"
        
        # Analyze recent emotional patterns
        recent_emotions = []
        for interaction in user_history[-5:]:  # Last 5 interactions
            if "emotional_state" in interaction:
                recent_emotions.append(interaction["emotional_state"])
        
        if not recent_emotions:
            return "neutral"
        
        # Determine overall mood trend
        positive_count = sum(1 for emotion in recent_emotions if emotion in ["joy", "trust", "anticipation"])
        negative_count = sum(1 for emotion in recent_emotions if emotion in ["sadness", "anger", "fear"])
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _generate_processing_recommendations(self, emotional_state: EmotionalState) -> List[str]:
        """Generate processing recommendations based on emotional state."""
        
        recommendations = []
        
        # Urgency-based recommendations
        if emotional_state.urgency_level == UrgencyLevel.CRITICAL:
            recommendations.append("prioritize_immediate_response")
            recommendations.append("escalate_to_human_if_needed")
        elif emotional_state.urgency_level == UrgencyLevel.HIGH:
            recommendations.append("fast_track_processing")
        
        # Emotion-based recommendations
        if emotional_state.primary_emotion == EmotionType.ANGER:
            recommendations.append("use_calming_language")
            recommendations.append("acknowledge_frustration")
        elif emotional_state.primary_emotion == EmotionType.FEAR:
            recommendations.append("provide_reassurance")
            recommendations.append("explain_safety_measures")
        elif emotional_state.primary_emotion == EmotionType.SADNESS:
            recommendations.append("use_empathetic_tone")
            recommendations.append("offer_additional_support")
        
        # Stress-based recommendations
        if emotional_state.stress_indicators:
            recommendations.append("simplify_response")
            recommendations.append("break_down_complex_tasks")
        
        # Satisfaction-based recommendations
        if emotional_state.satisfaction_indicators:
            recommendations.append("maintain_current_approach")
            recommendations.append("build_on_positive_experience")
        
        return recommendations
    
    def _generate_response_adaptations(self, emotional_state: EmotionalState, 
                                     emotional_context: EmotionalContext) -> List[str]:
        """Generate response adaptations based on emotional analysis."""
        
        adaptations = []
        
        # Tone adaptations
        if emotional_context.preferred_response_tone == "professional":
            adaptations.append("use_formal_language")
        elif emotional_context.preferred_response_tone == "friendly":
            adaptations.append("use_casual_friendly_tone")
        elif emotional_context.preferred_response_tone == "direct":
            adaptations.append("be_concise_and_direct")
        
        # Emotional adaptations
        if emotional_state.emotional_intensity == EmotionalIntensity.VERY_HIGH:
            adaptations.append("acknowledge_strong_emotions")
            adaptations.append("provide_emotional_validation")
        
        # Communication style adaptations
        if emotional_context.communication_style == "technical":
            adaptations.append("use_technical_precision")
            adaptations.append("include_detailed_explanations")
        elif emotional_context.communication_style == "collaborative":
            adaptations.append("emphasize_partnership")
            adaptations.append("use_inclusive_language")
        
        return adaptations
    
    def _calculate_emotional_confidence(self, emotional_state: EmotionalState, 
                                      sentiment: SentimentAnalysis) -> float:
        """Calculate overall confidence in emotional analysis."""
        
        # Average emotion confidence
        if emotional_state.emotion_scores:
            avg_emotion_confidence = sum(score.confidence for score in emotional_state.emotion_scores) / len(emotional_state.emotion_scores)
        else:
            avg_emotion_confidence = 0.0
        
        # Sentiment confidence
        sentiment_confidence = sentiment.confidence
        
        # Intensity confidence (higher intensity = higher confidence)
        intensity_confidence = {
            EmotionalIntensity.VERY_HIGH: 0.9,
            EmotionalIntensity.HIGH: 0.8,
            EmotionalIntensity.MODERATE: 0.7,
            EmotionalIntensity.LOW: 0.6,
            EmotionalIntensity.VERY_LOW: 0.5
        }.get(emotional_state.emotional_intensity, 0.5)
        
        # Weighted combination
        overall_confidence = (
            avg_emotion_confidence * 0.4 +
            sentiment_confidence * 0.4 +
            intensity_confidence * 0.2
        )
        
        return overall_confidence


# Example usage
if __name__ == "__main__":
    # Initialize emotional analyzer
    analyzer = EmotionalContextAnalyzer()
    
    # Test texts with different emotional contexts
    test_texts = [
        "I'm really frustrated with this system! It keeps breaking and I need it fixed ASAP!",
        "Thank you so much for your help. The solution worked perfectly and I'm very satisfied.",
        "I'm a bit worried about the security implications. Could you please explain the safety measures?",
        "This is absolutely amazing! I'm so excited to implement this new feature.",
        "I'm not sure if this is the right approach. Could we explore some alternatives?"
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        
        # Analyze emotional context
        result = analyzer.analyze_emotional_context(text)
        
        print(f"Primary emotion: {result.emotional_state.primary_emotion.value}")
        print(f"Sentiment: {result.emotional_state.sentiment.polarity.value} ({result.emotional_state.sentiment.score:.2f})")
        print(f"Emotional intensity: {result.emotional_state.emotional_intensity.value}")
        print(f"Urgency level: {result.emotional_state.urgency_level.value}")
        print(f"Communication style: {result.emotional_context.communication_style}")
        print(f"Preferred tone: {result.emotional_context.preferred_response_tone}")
        print(f"Confidence: {result.confidence_score:.3f}")
        print(f"Processing time: {result.processing_time_ms:.2f}ms")
        
        if result.processing_recommendations:
            print(f"Recommendations: {', '.join(result.processing_recommendations)}")
        
        if result.response_adaptations:
            print(f"Adaptations: {', '.join(result.response_adaptations)}")
