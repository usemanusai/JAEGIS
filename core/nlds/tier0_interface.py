#!/usr/bin/env python3
"""
N.L.D.S. Tier 0 Interface
Natural Language Detection System - Tier 0 Component

This module implements the Tier 0 Natural Language Detection System for JAEGIS,
providing automatic mode selection through 3-dimensional analysis (logical, emotional, creative)
with 85% confidence threshold, eliminating manual mode selection in most cases.

N.L.D.S. Tier 0 Features:
- Natural language processing and intent recognition
- 3-dimensional analysis: logical, emotional, creative
- Automatic mode selection with 85% confidence threshold
- Context-aware processing and decision making
- Integration with JAEGIS agent ecosystem
- Real-time language understanding and response
"""

import asyncio
import json
import logging
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisDimension(Enum):
    """3-dimensional analysis dimensions"""
    LOGICAL = "logical"
    EMOTIONAL = "emotional"
    CREATIVE = "creative"

class ProcessingMode(Enum):
    """JAEGIS processing modes"""
    FORMATION = "formation"  # A.C.I.D. Formation mode
    SWARM = "swarm"  # A.C.I.D. Swarm mode
    SEQUENTIAL = "sequential"  # P.I.T.C.E.S. Sequential Waterfall
    CIAR = "ciar"  # P.I.T.C.E.S. CI/AR mode
    DESIGN = "design"  # A.U.R.A. design mode
    APPLICATION = "application"  # P.H.A.L.A.N.X. app generation
    DEVELOPMENT = "development"  # O.D.I.N. development assistance
    HYBRID = "hybrid"  # Hybrid approach

class ConfidenceLevel(Enum):
    """Confidence levels for mode selection"""
    LOW = "low"  # < 60%
    MODERATE = "moderate"  # 60-75%
    HIGH = "high"  # 75-85%
    VERY_HIGH = "very_high"  # 85-95%
    CERTAIN = "certain"  # > 95%

@dataclass
class LanguageAnalysis:
    """Natural language analysis result"""
    text: str
    logical_score: float  # 0.0 to 1.0
    emotional_score: float  # 0.0 to 1.0
    creative_score: float  # 0.0 to 1.0
    intent: str
    entities: List[Dict[str, Any]] = field(default_factory=list)
    sentiment: str = "neutral"
    complexity: float = 0.5  # 0.0 to 1.0
    urgency: float = 0.5  # 0.0 to 1.0
    context_indicators: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ModeRecommendation:
    """Mode selection recommendation"""
    recommended_mode: ProcessingMode
    confidence: float  # 0.0 to 1.0
    confidence_level: ConfidenceLevel
    reasoning: str
    alternative_modes: List[Tuple[ProcessingMode, float]] = field(default_factory=list)
    analysis_breakdown: Dict[str, float] = field(default_factory=dict)
    context_factors: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ProcessingContext:
    """Processing context for mode selection"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    previous_interactions: List[str] = field(default_factory=list)
    current_project: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    system_state: Dict[str, Any] = field(default_factory=dict)
    time_constraints: Optional[Dict[str, Any]] = None
    resource_availability: Dict[str, Any] = field(default_factory=dict)

class NaturalLanguageProcessor:
    """Core natural language processing engine"""
    
    def __init__(self):
        self.intent_patterns = self._initialize_intent_patterns()
        self.entity_patterns = self._initialize_entity_patterns()
        self.sentiment_indicators = self._initialize_sentiment_indicators()
        self.complexity_indicators = self._initialize_complexity_indicators()
        
    def _initialize_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize intent recognition patterns"""
        return {
            "create": [
                r"create|build|make|generate|develop|design|implement",
                r"new\s+\w+|fresh\s+\w+|from\s+scratch",
                r"start\s+\w+|begin\s+\w+|initiate"
            ],
            "analyze": [
                r"analyze|examine|investigate|study|review|assess",
                r"what\s+is|how\s+does|why\s+is|explain",
                r"understand|comprehend|figure\s+out"
            ],
            "optimize": [
                r"optimize|improve|enhance|better|faster|efficient",
                r"performance|speed|quality|reduce|minimize",
                r"fix|repair|solve|resolve|debug"
            ],
            "integrate": [
                r"integrate|connect|combine|merge|link|join",
                r"api|service|system|database|external",
                r"workflow|process|automation"
            ],
            "deploy": [
                r"deploy|launch|release|publish|go\s+live",
                r"production|staging|environment|server",
                r"install|setup|configure"
            ],
            "test": [
                r"test|validate|verify|check|ensure|confirm",
                r"quality|bug|error|issue|problem",
                r"unit\s+test|integration\s+test|e2e"
            ],
            "document": [
                r"document|write|explain|describe|guide",
                r"readme|documentation|manual|tutorial",
                r"help|instruction|specification"
            ],
            "plan": [
                r"plan|strategy|roadmap|timeline|schedule",
                r"project|task|milestone|goal|objective",
                r"organize|structure|framework"
            ]
        }
    
    def _initialize_entity_patterns(self) -> Dict[str, List[str]]:
        """Initialize entity recognition patterns"""
        return {
            "technology": [
                r"react|vue|angular|svelte|javascript|typescript",
                r"python|java|c\+\+|rust|go|php|ruby",
                r"docker|kubernetes|aws|azure|gcp",
                r"database|sql|mongodb|redis|postgresql"
            ],
            "project_type": [
                r"web\s+app|mobile\s+app|desktop\s+app",
                r"api|microservice|backend|frontend",
                r"website|platform|system|tool|library"
            ],
            "complexity": [
                r"simple|basic|easy|straightforward",
                r"complex|advanced|sophisticated|enterprise",
                r"medium|moderate|standard|typical"
            ],
            "urgency": [
                r"urgent|asap|immediately|quickly|fast",
                r"deadline|due|timeline|schedule",
                r"slow|careful|thorough|detailed"
            ],
            "scope": [
                r"small|large|huge|massive|tiny",
                r"prototype|mvp|full\s+scale|enterprise",
                r"single|multiple|many|few"
            ]
        }
    
    def _initialize_sentiment_indicators(self) -> Dict[str, List[str]]:
        """Initialize sentiment analysis indicators"""
        return {
            "positive": [
                r"love|like|enjoy|excited|amazing|awesome",
                r"great|excellent|fantastic|wonderful|perfect",
                r"happy|pleased|satisfied|delighted"
            ],
            "negative": [
                r"hate|dislike|frustrated|annoyed|terrible",
                r"bad|awful|horrible|disappointing|broken",
                r"angry|upset|concerned|worried"
            ],
            "neutral": [
                r"need|want|require|looking\s+for|help",
                r"can\s+you|would\s+you|please|thanks",
                r"how\s+to|what\s+is|where\s+can"
            ]
        }
    
    def _initialize_complexity_indicators(self) -> Dict[str, float]:
        """Initialize complexity scoring indicators"""
        return {
            "simple_keywords": 0.2,  # simple, basic, easy
            "moderate_keywords": 0.5,  # standard, typical, normal
            "complex_keywords": 0.8,  # complex, advanced, enterprise
            "technical_terms": 0.1,  # per technical term
            "integration_mentions": 0.3,  # per integration requirement
            "multiple_technologies": 0.2,  # per additional technology
            "performance_requirements": 0.3,  # performance, scalability mentions
            "security_requirements": 0.4,  # security, compliance mentions
        }
    
    async def analyze_text(self, text: str, context: Optional[ProcessingContext] = None) -> LanguageAnalysis:
        """
        Analyze natural language text for intent, entities, and dimensions
        
        Args:
            text: Input text to analyze
            context: Optional processing context
            
        Returns:
            LanguageAnalysis with comprehensive analysis results
        """
        text_lower = text.lower()
        
        # Intent recognition
        intent = self._recognize_intent(text_lower)
        
        # Entity extraction
        entities = self._extract_entities(text_lower)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(text_lower)
        
        # Complexity assessment
        complexity = self._assess_complexity(text_lower, entities)
        
        # Urgency detection
        urgency = self._detect_urgency(text_lower)
        
        # 3-dimensional analysis
        logical_score = self._calculate_logical_dimension(text_lower, intent, entities)
        emotional_score = self._calculate_emotional_dimension(text_lower, sentiment)
        creative_score = self._calculate_creative_dimension(text_lower, intent, entities)
        
        # Context indicators
        context_indicators = self._identify_context_indicators(text_lower, entities)
        
        analysis = LanguageAnalysis(
            text=text,
            logical_score=logical_score,
            emotional_score=emotional_score,
            creative_score=creative_score,
            intent=intent,
            entities=entities,
            sentiment=sentiment,
            complexity=complexity,
            urgency=urgency,
            context_indicators=context_indicators,
            metadata={
                "word_count": len(text.split()),
                "sentence_count": len(re.split(r'[.!?]+', text)),
                "technical_density": self._calculate_technical_density(text_lower),
                "processed_at": datetime.now().isoformat()
            }
        )
        
        logger.info(f"Analyzed text: intent={intent}, logical={logical_score:.2f}, emotional={emotional_score:.2f}, creative={creative_score:.2f}")
        return analysis
    
    def _recognize_intent(self, text: str) -> str:
        """Recognize primary intent from text"""
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text))
                score += matches
            intent_scores[intent] = score
        
        if not intent_scores or max(intent_scores.values()) == 0:
            return "general"
        
        return max(intent_scores, key=intent_scores.get)
    
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text"""
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    entities.append({
                        "type": entity_type,
                        "value": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                        "confidence": 0.8  # Simple confidence score
                    })
        
        return entities
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
        
        for sentiment, patterns in self.sentiment_indicators.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, text))
                sentiment_scores[sentiment] += matches
        
        if max(sentiment_scores.values()) == 0:
            return "neutral"
        
        return max(sentiment_scores, key=sentiment_scores.get)
    
    def _assess_complexity(self, text: str, entities: List[Dict[str, Any]]) -> float:
        """Assess complexity of the request"""
        complexity_score = 0.0
        
        # Check for complexity keywords
        if re.search(r"simple|basic|easy|straightforward", text):
            complexity_score += self.complexity_indicators["simple_keywords"]
        elif re.search(r"complex|advanced|sophisticated|enterprise", text):
            complexity_score += self.complexity_indicators["complex_keywords"]
        else:
            complexity_score += self.complexity_indicators["moderate_keywords"]
        
        # Technical terms
        tech_entities = [e for e in entities if e["type"] == "technology"]
        complexity_score += len(tech_entities) * self.complexity_indicators["technical_terms"]
        
        # Integration requirements
        if re.search(r"integrate|api|service|external|third.party", text):
            complexity_score += self.complexity_indicators["integration_mentions"]
        
        # Performance requirements
        if re.search(r"performance|scalability|optimization|speed|efficient", text):
            complexity_score += self.complexity_indicators["performance_requirements"]
        
        # Security requirements
        if re.search(r"security|authentication|authorization|compliance|encryption", text):
            complexity_score += self.complexity_indicators["security_requirements"]
        
        return min(1.0, complexity_score)
    
    def _detect_urgency(self, text: str) -> float:
        """Detect urgency level"""
        urgency_score = 0.5  # Default moderate urgency
        
        if re.search(r"urgent|asap|immediately|quickly|fast|rush", text):
            urgency_score = 0.9
        elif re.search(r"deadline|due|timeline|schedule", text):
            urgency_score = 0.7
        elif re.search(r"slow|careful|thorough|detailed|when\s+possible", text):
            urgency_score = 0.3
        
        return urgency_score
    
    def _calculate_logical_dimension(self, text: str, intent: str, entities: List[Dict[str, Any]]) -> float:
        """Calculate logical dimension score"""
        logical_score = 0.0
        
        # Intent-based scoring
        logical_intents = ["analyze", "optimize", "test", "plan", "integrate"]
        if intent in logical_intents:
            logical_score += 0.4
        
        # Technical entities boost logical score
        tech_entities = [e for e in entities if e["type"] == "technology"]
        logical_score += min(0.3, len(tech_entities) * 0.1)
        
        # Logical keywords
        logical_keywords = r"algorithm|logic|system|architecture|performance|efficiency|optimization|analysis"
        matches = len(re.findall(logical_keywords, text))
        logical_score += min(0.3, matches * 0.1)
        
        return min(1.0, logical_score)
    
    def _calculate_emotional_dimension(self, text: str, sentiment: str) -> float:
        """Calculate emotional dimension score"""
        emotional_score = 0.0
        
        # Sentiment-based scoring
        if sentiment == "positive":
            emotional_score += 0.3
        elif sentiment == "negative":
            emotional_score += 0.4
        else:
            emotional_score += 0.1
        
        # Emotional keywords
        emotional_keywords = r"feel|love|hate|excited|frustrated|happy|sad|worried|concerned|passionate"
        matches = len(re.findall(emotional_keywords, text))
        emotional_score += min(0.4, matches * 0.2)
        
        # User experience focus
        ux_keywords = r"user\s+experience|usability|interface|design|beautiful|elegant|intuitive"
        matches = len(re.findall(ux_keywords, text))
        emotional_score += min(0.3, matches * 0.15)
        
        return min(1.0, emotional_score)
    
    def _calculate_creative_dimension(self, text: str, intent: str, entities: List[Dict[str, Any]]) -> float:
        """Calculate creative dimension score"""
        creative_score = 0.0
        
        # Intent-based scoring
        creative_intents = ["create", "design", "document"]
        if intent in creative_intents:
            creative_score += 0.4
        
        # Creative keywords
        creative_keywords = r"creative|innovative|unique|original|artistic|design|visual|beautiful|elegant"
        matches = len(re.findall(creative_keywords, text))
        creative_score += min(0.3, matches * 0.15)
        
        # Design and UI entities
        design_entities = [e for e in entities if "design" in e["value"] or "ui" in e["value"] or "interface" in e["value"]]
        creative_score += min(0.3, len(design_entities) * 0.15)
        
        return min(1.0, creative_score)
    
    def _identify_context_indicators(self, text: str, entities: List[Dict[str, Any]]) -> List[str]:
        """Identify context indicators from text"""
        indicators = []
        
        # Project type indicators
        if re.search(r"web\s+app|website|web\s+application", text):
            indicators.append("web_application")
        if re.search(r"mobile\s+app|ios|android", text):
            indicators.append("mobile_application")
        if re.search(r"api|backend|server", text):
            indicators.append("backend_service")
        if re.search(r"frontend|ui|interface", text):
            indicators.append("frontend_interface")
        
        # Technology indicators
        tech_entities = [e for e in entities if e["type"] == "technology"]
        for entity in tech_entities:
            indicators.append(f"technology_{entity['value']}")
        
        # Complexity indicators
        if re.search(r"simple|basic|easy", text):
            indicators.append("low_complexity")
        elif re.search(r"complex|advanced|enterprise", text):
            indicators.append("high_complexity")
        
        return indicators
    
    def _calculate_technical_density(self, text: str) -> float:
        """Calculate technical density of text"""
        words = text.split()
        if not words:
            return 0.0
        
        technical_terms = 0
        technical_patterns = [
            r"api|sdk|framework|library|database|server|client",
            r"javascript|python|java|react|vue|angular|node",
            r"docker|kubernetes|aws|azure|cloud|microservice",
            r"authentication|authorization|encryption|security",
            r"algorithm|optimization|performance|scalability"
        ]
        
        for pattern in technical_patterns:
            technical_terms += len(re.findall(pattern, text))
        
        return min(1.0, technical_terms / len(words))

class ModeSelector:
    """Intelligent mode selection engine"""
    
    def __init__(self):
        self.mode_criteria = self._initialize_mode_criteria()
        self.confidence_threshold = 0.85  # 85% confidence threshold
        
    def _initialize_mode_criteria(self) -> Dict[ProcessingMode, Dict[str, Any]]:
        """Initialize mode selection criteria"""
        return {
            ProcessingMode.FORMATION: {
                "logical_weight": 0.4,
                "emotional_weight": 0.2,
                "creative_weight": 0.4,
                "preferred_intents": ["plan", "analyze", "create"],
                "complexity_range": (0.3, 0.8),
                "context_indicators": ["high_complexity", "multiple_agents", "coordination"]
            },
            ProcessingMode.SWARM: {
                "logical_weight": 0.5,
                "emotional_weight": 0.1,
                "creative_weight": 0.4,
                "preferred_intents": ["optimize", "analyze", "integrate"],
                "complexity_range": (0.5, 1.0),
                "context_indicators": ["high_complexity", "autonomous", "emergent"]
            },
            ProcessingMode.SEQUENTIAL: {
                "logical_weight": 0.6,
                "emotional_weight": 0.1,
                "creative_weight": 0.3,
                "preferred_intents": ["plan", "create", "deploy"],
                "complexity_range": (0.0, 0.5),
                "context_indicators": ["low_complexity", "structured", "waterfall"]
            },
            ProcessingMode.CIAR: {
                "logical_weight": 0.5,
                "emotional_weight": 0.2,
                "creative_weight": 0.3,
                "preferred_intents": ["optimize", "integrate", "test"],
                "complexity_range": (0.4, 1.0),
                "context_indicators": ["high_complexity", "iterative", "continuous"]
            },
            ProcessingMode.DESIGN: {
                "logical_weight": 0.2,
                "emotional_weight": 0.4,
                "creative_weight": 0.4,
                "preferred_intents": ["create", "design", "document"],
                "complexity_range": (0.0, 0.8),
                "context_indicators": ["frontend_interface", "ui", "design", "visual"]
            },
            ProcessingMode.APPLICATION: {
                "logical_weight": 0.4,
                "emotional_weight": 0.2,
                "creative_weight": 0.4,
                "preferred_intents": ["create", "deploy", "integrate"],
                "complexity_range": (0.3, 1.0),
                "context_indicators": ["web_application", "mobile_application", "full_stack"]
            },
            ProcessingMode.DEVELOPMENT: {
                "logical_weight": 0.5,
                "emotional_weight": 0.1,
                "creative_weight": 0.4,
                "preferred_intents": ["optimize", "test", "document"],
                "complexity_range": (0.0, 1.0),
                "context_indicators": ["backend_service", "api", "development"]
            }
        }
    
    async def select_mode(
        self,
        analysis: LanguageAnalysis,
        context: Optional[ProcessingContext] = None
    ) -> ModeRecommendation:
        """
        Select optimal processing mode based on analysis
        
        Args:
            analysis: Language analysis results
            context: Optional processing context
            
        Returns:
            ModeRecommendation with selected mode and confidence
        """
        mode_scores = {}
        
        for mode, criteria in self.mode_criteria.items():
            score = self._calculate_mode_score(analysis, criteria, context)
            mode_scores[mode] = score
        
        # Sort modes by score
        sorted_modes = sorted(mode_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top recommendation
        recommended_mode, confidence = sorted_modes[0]
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(confidence)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(analysis, recommended_mode, confidence)
        
        # Get alternative modes
        alternative_modes = [(mode, score) for mode, score in sorted_modes[1:4]]
        
        # Analysis breakdown
        analysis_breakdown = {
            "logical_contribution": analysis.logical_score * 0.4,
            "emotional_contribution": analysis.emotional_score * 0.3,
            "creative_contribution": analysis.creative_score * 0.3,
            "intent_match": self._calculate_intent_match(analysis.intent, recommended_mode),
            "complexity_match": self._calculate_complexity_match(analysis.complexity, recommended_mode),
            "context_match": self._calculate_context_match(analysis.context_indicators, recommended_mode)
        }
        
        recommendation = ModeRecommendation(
            recommended_mode=recommended_mode,
            confidence=confidence,
            confidence_level=confidence_level,
            reasoning=reasoning,
            alternative_modes=alternative_modes,
            analysis_breakdown=analysis_breakdown,
            context_factors=analysis.context_indicators
        )
        
        logger.info(f"Mode selected: {recommended_mode.value} with {confidence:.1%} confidence")
        return recommendation
    
    def _calculate_mode_score(
        self,
        analysis: LanguageAnalysis,
        criteria: Dict[str, Any],
        context: Optional[ProcessingContext]
    ) -> float:
        """Calculate score for a specific mode"""
        score = 0.0
        
        # Dimensional scoring
        dimensional_score = (
            analysis.logical_score * criteria["logical_weight"] +
            analysis.emotional_score * criteria["emotional_weight"] +
            analysis.creative_score * criteria["creative_weight"]
        )
        score += dimensional_score * 0.4
        
        # Intent matching
        intent_score = 1.0 if analysis.intent in criteria["preferred_intents"] else 0.5
        score += intent_score * 0.2
        
        # Complexity matching
        complexity_min, complexity_max = criteria["complexity_range"]
        if complexity_min <= analysis.complexity <= complexity_max:
            complexity_score = 1.0
        else:
            # Penalty for being outside range
            if analysis.complexity < complexity_min:
                complexity_score = analysis.complexity / complexity_min
            else:
                complexity_score = complexity_max / analysis.complexity
        score += complexity_score * 0.2
        
        # Context indicator matching
        context_score = 0.0
        for indicator in criteria["context_indicators"]:
            if indicator in analysis.context_indicators:
                context_score += 0.2
        score += min(1.0, context_score) * 0.2
        
        return min(1.0, score)
    
    def _determine_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Determine confidence level from score"""
        if confidence >= 0.95:
            return ConfidenceLevel.CERTAIN
        elif confidence >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        elif confidence >= 0.75:
            return ConfidenceLevel.HIGH
        elif confidence >= 0.60:
            return ConfidenceLevel.MODERATE
        else:
            return ConfidenceLevel.LOW
    
    def _generate_reasoning(
        self,
        analysis: LanguageAnalysis,
        mode: ProcessingMode,
        confidence: float
    ) -> str:
        """Generate human-readable reasoning for mode selection"""
        reasons = []
        
        # Dimensional analysis
        if analysis.logical_score > 0.7:
            reasons.append("high logical content suggests structured approach")
        if analysis.emotional_score > 0.6:
            reasons.append("emotional elements indicate user-focused requirements")
        if analysis.creative_score > 0.6:
            reasons.append("creative aspects suggest design-oriented solution")
        
        # Intent-based reasoning
        intent_reasoning = {
            "create": "creation intent aligns with generative capabilities",
            "analyze": "analytical intent requires systematic processing",
            "optimize": "optimization focus benefits from intelligent coordination",
            "integrate": "integration requirements need careful orchestration",
            "deploy": "deployment needs structured workflow management",
            "test": "testing requirements benefit from systematic validation",
            "document": "documentation needs creative and structured approach",
            "plan": "planning requires strategic coordination"
        }
        
        if analysis.intent in intent_reasoning:
            reasons.append(intent_reasoning[analysis.intent])
        
        # Complexity-based reasoning
        if analysis.complexity > 0.7:
            reasons.append("high complexity requires advanced coordination")
        elif analysis.complexity < 0.3:
            reasons.append("low complexity suits streamlined approach")
        
        # Confidence-based reasoning
        if confidence >= 0.85:
            reasons.append("strong alignment with mode capabilities")
        elif confidence < 0.75:
            reasons.append("moderate alignment suggests careful consideration")
        
        return f"Selected {mode.value} mode because: " + "; ".join(reasons)
    
    def _calculate_intent_match(self, intent: str, mode: ProcessingMode) -> float:
        """Calculate intent match score for mode"""
        criteria = self.mode_criteria[mode]
        return 1.0 if intent in criteria["preferred_intents"] else 0.5
    
    def _calculate_complexity_match(self, complexity: float, mode: ProcessingMode) -> float:
        """Calculate complexity match score for mode"""
        criteria = self.mode_criteria[mode]
        complexity_min, complexity_max = criteria["complexity_range"]
        
        if complexity_min <= complexity <= complexity_max:
            return 1.0
        else:
            # Calculate distance from range
            if complexity < complexity_min:
                return complexity / complexity_min
            else:
                return complexity_max / complexity
    
    def _calculate_context_match(self, indicators: List[str], mode: ProcessingMode) -> float:
        """Calculate context match score for mode"""
        criteria = self.mode_criteria[mode]
        matches = sum(1 for indicator in criteria["context_indicators"] if indicator in indicators)
        return matches / len(criteria["context_indicators"]) if criteria["context_indicators"] else 0.5

class NLDSTier0Interface:
    """
    N.L.D.S. Tier 0 Interface
    
    Main interface for Natural Language Detection System providing automatic
    mode selection through 3-dimensional analysis with 85% confidence threshold.
    """
    
    def __init__(self):
        self.nlp_processor = NaturalLanguageProcessor()
        self.mode_selector = ModeSelector()
        self.processing_history: List[Dict[str, Any]] = []
        self.user_sessions: Dict[str, ProcessingContext] = {}
        self.system_metrics = {
            "total_requests": 0,
            "successful_selections": 0,
            "high_confidence_selections": 0,
            "average_confidence": 0.0,
            "mode_distribution": {},
            "system_uptime": datetime.now()
        }
        
        logger.info("N.L.D.S. Tier 0 Interface initialized")
    
    async def process_natural_language(
        self,
        text: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> ModeRecommendation:
        """
        Process natural language input and recommend processing mode
        
        Args:
            text: Natural language input
            user_id: Optional user identifier
            session_id: Optional session identifier
            additional_context: Optional additional context
            
        Returns:
            ModeRecommendation with selected mode and confidence
        """
        start_time = time.time()
        
        try:
            # Get or create processing context
            context = self._get_processing_context(user_id, session_id, additional_context)
            
            # Analyze natural language
            analysis = await self.nlp_processor.analyze_text(text, context)
            
            # Select processing mode
            recommendation = await self.mode_selector.select_mode(analysis, context)
            
            # Update metrics
            self._update_metrics(recommendation)
            
            # Store in history
            self._store_processing_history(text, analysis, recommendation, context)
            
            # Update user context
            if session_id:
                self._update_user_context(session_id, text, recommendation)
            
            processing_time = time.time() - start_time
            
            logger.info(
                f"Processed request in {processing_time:.3f}s: "
                f"mode={recommendation.recommended_mode.value}, "
                f"confidence={recommendation.confidence:.1%}"
            )
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error processing natural language: {e}")
            # Return fallback recommendation
            return ModeRecommendation(
                recommended_mode=ProcessingMode.DEVELOPMENT,
                confidence=0.5,
                confidence_level=ConfidenceLevel.MODERATE,
                reasoning=f"Fallback mode due to processing error: {e}",
                analysis_breakdown={"error": str(e)}
            )
    
    def _get_processing_context(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        additional_context: Optional[Dict[str, Any]]
    ) -> ProcessingContext:
        """Get or create processing context"""
        if session_id and session_id in self.user_sessions:
            context = self.user_sessions[session_id]
        else:
            context = ProcessingContext(
                user_id=user_id,
                session_id=session_id
            )
            if session_id:
                self.user_sessions[session_id] = context
        
        # Update with additional context
        if additional_context:
            context.system_state.update(additional_context)
        
        return context
    
    def _update_metrics(self, recommendation: ModeRecommendation):
        """Update system metrics"""
        self.system_metrics["total_requests"] += 1
        
        if recommendation.confidence >= 0.75:
            self.system_metrics["successful_selections"] += 1
        
        if recommendation.confidence >= 0.85:
            self.system_metrics["high_confidence_selections"] += 1
        
        # Update average confidence
        total = self.system_metrics["total_requests"]
        current_avg = self.system_metrics["average_confidence"]
        self.system_metrics["average_confidence"] = (
            (current_avg * (total - 1) + recommendation.confidence) / total
        )
        
        # Update mode distribution
        mode = recommendation.recommended_mode.value
        self.system_metrics["mode_distribution"][mode] = (
            self.system_metrics["mode_distribution"].get(mode, 0) + 1
        )
    
    def _store_processing_history(
        self,
        text: str,
        analysis: LanguageAnalysis,
        recommendation: ModeRecommendation,
        context: ProcessingContext
    ):
        """Store processing history"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "analysis": asdict(analysis),
            "recommendation": asdict(recommendation),
            "context": asdict(context)
        }
        
        self.processing_history.append(history_entry)
        
        # Keep only last 1000 entries
        if len(self.processing_history) > 1000:
            self.processing_history = self.processing_history[-1000:]
    
    def _update_user_context(
        self,
        session_id: str,
        text: str,
        recommendation: ModeRecommendation
    ):
        """Update user context with interaction"""
        if session_id in self.user_sessions:
            context = self.user_sessions[session_id]
            context.previous_interactions.append(text)
            
            # Keep only last 10 interactions
            if len(context.previous_interactions) > 10:
                context.previous_interactions = context.previous_interactions[-10:]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get N.L.D.S. system status"""
        uptime = datetime.now() - self.system_metrics["system_uptime"]
        
        return {
            "system_name": "N.L.D.S. Tier 0 Interface",
            "version": "1.0.0",
            "uptime_seconds": uptime.total_seconds(),
            "total_requests": self.system_metrics["total_requests"],
            "success_rate": (
                self.system_metrics["successful_selections"] / 
                max(1, self.system_metrics["total_requests"])
            ),
            "high_confidence_rate": (
                self.system_metrics["high_confidence_selections"] / 
                max(1, self.system_metrics["total_requests"])
            ),
            "average_confidence": self.system_metrics["average_confidence"],
            "mode_distribution": self.system_metrics["mode_distribution"],
            "active_sessions": len(self.user_sessions),
            "history_size": len(self.processing_history),
            "confidence_threshold": self.mode_selector.confidence_threshold,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_processing_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent processing history"""
        return self.processing_history[-limit:]

# Example usage and testing
async def main():
    """Example usage of N.L.D.S. Tier 0 Interface"""
    nlds = NLDSTier0Interface()
    
    print("🧠 N.L.D.S. Tier 0 Interface Demo")
    print("=" * 50)
    
    # Test cases with different types of requests
    test_cases = [
        "I need to create a modern React web application with user authentication",
        "Can you help me optimize the performance of my existing API?",
        "I want to design a beautiful and intuitive user interface for mobile",
        "Please analyze the security vulnerabilities in our system",
        "We need to plan a complex enterprise integration project",
        "Help me debug this Python code that's not working properly",
        "I'm looking for a simple solution to deploy my website",
        "Can you create comprehensive documentation for our API?"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{test_text}'")
        
        recommendation = await nlds.process_natural_language(
            text=test_text,
            session_id=f"demo_session_{i}"
        )
        
        print(f"   Mode: {recommendation.recommended_mode.value}")
        print(f"   Confidence: {recommendation.confidence:.1%} ({recommendation.confidence_level.value})")
        print(f"   Reasoning: {recommendation.reasoning}")
        
        if recommendation.alternative_modes:
            alt_mode, alt_conf = recommendation.alternative_modes[0]
            print(f"   Alternative: {alt_mode.value} ({alt_conf:.1%})")
    
    # Display system status
    print(f"\n📊 N.L.D.S. System Status:")
    status = nlds.get_system_status()
    print(f"   Total Requests: {status['total_requests']}")
    print(f"   Success Rate: {status['success_rate']:.1%}")
    print(f"   High Confidence Rate: {status['high_confidence_rate']:.1%}")
    print(f"   Average Confidence: {status['average_confidence']:.1%}")
    print(f"   Mode Distribution: {status['mode_distribution']}")
    
    print("\n✅ N.L.D.S. Tier 0 Interface demo completed!")

if __name__ == "__main__":
    asyncio.run(main())