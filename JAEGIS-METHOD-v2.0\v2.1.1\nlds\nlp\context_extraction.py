"""
N.L.D.S. Context Extraction Module
Advanced context extraction for conversation continuity and session management
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import spacy
import redis
from collections import defaultdict, deque
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class ContextType(str, Enum):
    """Types of context information."""
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    TEMPORAL = "temporal"
    EMOTIONAL = "emotional"
    TASK_ORIENTED = "task_oriented"
    USER_PREFERENCE = "user_preference"
    SYSTEM_STATE = "system_state"


class ContextScope(str, Enum):
    """Scope of context information."""
    IMMEDIATE = "immediate"  # Current message
    SESSION = "session"      # Current session
    USER = "user"           # User-specific across sessions
    GLOBAL = "global"       # System-wide patterns


@dataclass
class ContextEntity:
    """Extracted context entity."""
    entity_id: str
    entity_type: str
    value: Any
    confidence: float
    source: str
    timestamp: datetime
    scope: ContextScope
    relevance_score: float
    dependencies: List[str]


@dataclass
class ConversationContext:
    """Conversation context information."""
    session_id: str
    user_id: str
    conversation_history: List[Dict[str, Any]]
    active_topics: List[str]
    intent_sequence: List[str]
    emotional_state: Dict[str, float]
    technical_context: Dict[str, Any]
    user_preferences: Dict[str, Any]
    last_updated: datetime


@dataclass
class ContextExtractionResult:
    """Context extraction result."""
    extracted_entities: List[ContextEntity]
    conversation_context: ConversationContext
    context_summary: Dict[str, Any]
    confidence_score: float
    processing_time_ms: float
    context_changes: List[str]


class ContextExtractionModule:
    """
    Advanced context extraction module for conversation continuity
    and session management in N.L.D.S.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Initialize NLP components
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            logger.warning("Large spaCy model not found, using medium model")
            try:
                self.nlp = spacy.load("en_core_web_md")
            except OSError:
                self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize Redis for session storage
        self.redis_client = redis.from_url(redis_url)
        
        # Context extraction patterns
        self.technical_patterns = {
            'programming_languages': ['python', 'javascript', 'java', 'c++', 'go', 'rust'],
            'frameworks': ['django', 'flask', 'react', 'vue', 'angular', 'express'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud_platforms': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'tools': ['git', 'jenkins', 'terraform', 'ansible', 'nginx']
        }
        
        self.intent_patterns = {
            'create': ['create', 'build', 'make', 'generate', 'develop'],
            'analyze': ['analyze', 'examine', 'investigate', 'study', 'review'],
            'fix': ['fix', 'repair', 'debug', 'troubleshoot', 'resolve'],
            'optimize': ['optimize', 'improve', 'enhance', 'speed up', 'performance'],
            'deploy': ['deploy', 'release', 'publish', 'launch', 'go live']
        }
        
        self.emotional_indicators = {
            'urgency': ['urgent', 'asap', 'immediately', 'critical', 'emergency'],
            'frustration': ['frustrated', 'annoying', 'stuck', 'confused', 'difficult'],
            'satisfaction': ['great', 'excellent', 'perfect', 'amazing', 'wonderful'],
            'uncertainty': ['maybe', 'perhaps', 'not sure', 'think', 'might']
        }
        
        # TF-IDF vectorizer for topic modeling
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Session configuration
        self.session_config = {
            'max_history_length': 50,
            'context_retention_hours': 24,
            'relevance_threshold': 0.3,
            'similarity_threshold': 0.7
        }
        
        logger.info("Context Extraction Module initialized")
    
    def extract_context(self, text: str, user_id: str, session_id: str,
                       previous_context: Optional[ConversationContext] = None) -> ContextExtractionResult:
        """Extract comprehensive context from input text."""
        
        start_time = time.time()
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Extract various types of context
        entities = []
        
        # Extract conversational context
        conversational_entities = self._extract_conversational_context(doc, text)
        entities.extend(conversational_entities)
        
        # Extract technical context
        technical_entities = self._extract_technical_context(doc, text)
        entities.extend(technical_entities)
        
        # Extract temporal context
        temporal_entities = self._extract_temporal_context(doc, text)
        entities.extend(temporal_entities)
        
        # Extract emotional context
        emotional_entities = self._extract_emotional_context(doc, text)
        entities.extend(emotional_entities)
        
        # Extract task-oriented context
        task_entities = self._extract_task_context(doc, text)
        entities.extend(task_entities)
        
        # Load or create conversation context
        if previous_context:
            conversation_context = previous_context
        else:
            conversation_context = self._load_conversation_context(user_id, session_id)
        
        # Update conversation context
        conversation_context = self._update_conversation_context(
            conversation_context, text, entities, user_id, session_id
        )
        
        # Generate context summary
        context_summary = self._generate_context_summary(entities, conversation_context)
        
        # Calculate overall confidence
        confidence_score = self._calculate_context_confidence(entities)
        
        # Identify context changes
        context_changes = self._identify_context_changes(entities, conversation_context)
        
        # Store updated context
        self._store_conversation_context(conversation_context)
        
        processing_time = (time.time() - start_time) * 1000
        
        return ContextExtractionResult(
            extracted_entities=entities,
            conversation_context=conversation_context,
            context_summary=context_summary,
            confidence_score=confidence_score,
            processing_time_ms=processing_time,
            context_changes=context_changes
        )
    
    def _extract_conversational_context(self, doc, text: str) -> List[ContextEntity]:
        """Extract conversational context entities."""
        
        entities = []
        
        # Extract references to previous conversations
        reference_patterns = ['as we discussed', 'like before', 'previously', 'earlier', 'last time']
        for pattern in reference_patterns:
            if pattern in text.lower():
                entities.append(ContextEntity(
                    entity_id=f"ref_{hashlib.md5(pattern.encode()).hexdigest()[:8]}",
                    entity_type="conversation_reference",
                    value=pattern,
                    confidence=0.8,
                    source="pattern_matching",
                    timestamp=datetime.utcnow(),
                    scope=ContextScope.SESSION,
                    relevance_score=0.7,
                    dependencies=[]
                ))
        
        # Extract pronouns and their potential referents
        pronouns = ['it', 'this', 'that', 'they', 'them']
        for token in doc:
            if token.text.lower() in pronouns:
                entities.append(ContextEntity(
                    entity_id=f"pronoun_{token.i}",
                    entity_type="pronoun_reference",
                    value=token.text,
                    confidence=0.6,
                    source="spacy_analysis",
                    timestamp=datetime.utcnow(),
                    scope=ContextScope.IMMEDIATE,
                    relevance_score=0.5,
                    dependencies=[]
                ))
        
        # Extract question patterns
        if text.strip().endswith('?'):
            entities.append(ContextEntity(
                entity_id=f"question_{int(time.time())}",
                entity_type="question",
                value=text.strip(),
                confidence=0.9,
                source="punctuation_analysis",
                timestamp=datetime.utcnow(),
                scope=ContextScope.IMMEDIATE,
                relevance_score=0.8,
                dependencies=[]
            ))
        
        return entities
    
    def _extract_technical_context(self, doc, text: str) -> List[ContextEntity]:
        """Extract technical context entities."""
        
        entities = []
        text_lower = text.lower()
        
        # Extract technical terms
        for category, terms in self.technical_patterns.items():
            for term in terms:
                if term in text_lower:
                    entities.append(ContextEntity(
                        entity_id=f"tech_{category}_{term}",
                        entity_type=f"technical_{category}",
                        value=term,
                        confidence=0.9,
                        source="technical_patterns",
                        timestamp=datetime.utcnow(),
                        scope=ContextScope.SESSION,
                        relevance_score=0.8,
                        dependencies=[]
                    ))
        
        # Extract version numbers
        import re
        version_pattern = r'\b\d+\.\d+(?:\.\d+)?\b'
        versions = re.findall(version_pattern, text)
        for version in versions:
            entities.append(ContextEntity(
                entity_id=f"version_{version}",
                entity_type="version_number",
                value=version,
                confidence=0.8,
                source="regex_pattern",
                timestamp=datetime.utcnow(),
                scope=ContextScope.IMMEDIATE,
                relevance_score=0.6,
                dependencies=[]
            ))
        
        # Extract file paths and URLs
        path_pattern = r'[/\\][\w/\\.-]+'
        paths = re.findall(path_pattern, text)
        for path in paths:
            entities.append(ContextEntity(
                entity_id=f"path_{hashlib.md5(path.encode()).hexdigest()[:8]}",
                entity_type="file_path",
                value=path,
                confidence=0.7,
                source="regex_pattern",
                timestamp=datetime.utcnow(),
                scope=ContextScope.IMMEDIATE,
                relevance_score=0.5,
                dependencies=[]
            ))
        
        return entities
    
    def _extract_temporal_context(self, doc, text: str) -> List[ContextEntity]:
        """Extract temporal context entities."""
        
        entities = []
        
        # Extract time expressions using spaCy
        for ent in doc.ents:
            if ent.label_ in ['DATE', 'TIME', 'EVENT']:
                entities.append(ContextEntity(
                    entity_id=f"temporal_{ent.start}_{ent.end}",
                    entity_type=f"temporal_{ent.label_.lower()}",
                    value=ent.text,
                    confidence=0.8,
                    source="spacy_ner",
                    timestamp=datetime.utcnow(),
                    scope=ContextScope.IMMEDIATE,
                    relevance_score=0.7,
                    dependencies=[]
                ))
        
        # Extract relative time expressions
        relative_time_patterns = [
            'today', 'tomorrow', 'yesterday', 'next week', 'last month',
            'soon', 'later', 'now', 'currently', 'recently'
        ]
        
        text_lower = text.lower()
        for pattern in relative_time_patterns:
            if pattern in text_lower:
                entities.append(ContextEntity(
                    entity_id=f"relative_time_{pattern}",
                    entity_type="relative_time",
                    value=pattern,
                    confidence=0.7,
                    source="pattern_matching",
                    timestamp=datetime.utcnow(),
                    scope=ContextScope.IMMEDIATE,
                    relevance_score=0.6,
                    dependencies=[]
                ))
        
        return entities
    
    def _extract_emotional_context(self, doc, text: str) -> List[ContextEntity]:
        """Extract emotional context entities."""
        
        entities = []
        text_lower = text.lower()
        
        # Extract emotional indicators
        for emotion, indicators in self.emotional_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    entities.append(ContextEntity(
                        entity_id=f"emotion_{emotion}_{indicator}",
                        entity_type=f"emotional_{emotion}",
                        value=indicator,
                        confidence=0.8,
                        source="emotional_patterns",
                        timestamp=datetime.utcnow(),
                        scope=ContextScope.IMMEDIATE,
                        relevance_score=0.7,
                        dependencies=[]
                    ))
        
        # Analyze sentiment using spaCy
        sentiment_score = self._calculate_sentiment(doc)
        if abs(sentiment_score) > 0.3:  # Significant sentiment
            sentiment_label = "positive" if sentiment_score > 0 else "negative"
            entities.append(ContextEntity(
                entity_id=f"sentiment_{int(time.time())}",
                entity_type="sentiment",
                value={"label": sentiment_label, "score": sentiment_score},
                confidence=0.7,
                source="sentiment_analysis",
                timestamp=datetime.utcnow(),
                scope=ContextScope.IMMEDIATE,
                relevance_score=0.6,
                dependencies=[]
            ))
        
        return entities
    
    def _extract_task_context(self, doc, text: str) -> List[ContextEntity]:
        """Extract task-oriented context entities."""
        
        entities = []
        text_lower = text.lower()
        
        # Extract intent patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    entities.append(ContextEntity(
                        entity_id=f"intent_{intent}_{pattern}",
                        entity_type="task_intent",
                        value=intent,
                        confidence=0.8,
                        source="intent_patterns",
                        timestamp=datetime.utcnow(),
                        scope=ContextScope.IMMEDIATE,
                        relevance_score=0.9,
                        dependencies=[]
                    ))
        
        # Extract action verbs
        action_verbs = []
        for token in doc:
            if token.pos_ == 'VERB' and not token.is_stop:
                action_verbs.append(token.lemma_)
        
        if action_verbs:
            entities.append(ContextEntity(
                entity_id=f"actions_{int(time.time())}",
                entity_type="action_verbs",
                value=action_verbs,
                confidence=0.7,
                source="pos_tagging",
                timestamp=datetime.utcnow(),
                scope=ContextScope.IMMEDIATE,
                relevance_score=0.8,
                dependencies=[]
            ))
        
        # Extract objects/targets
        objects = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Avoid very long phrases
                objects.append(chunk.text)
        
        if objects:
            entities.append(ContextEntity(
                entity_id=f"objects_{int(time.time())}",
                entity_type="task_objects",
                value=objects,
                confidence=0.6,
                source="noun_chunks",
                timestamp=datetime.utcnow(),
                scope=ContextScope.IMMEDIATE,
                relevance_score=0.7,
                dependencies=[]
            ))
        
        return entities
    
    def _calculate_sentiment(self, doc) -> float:
        """Calculate sentiment score using simple lexicon approach."""
        
        positive_words = ['good', 'great', 'excellent', 'amazing', 'perfect', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'wrong', 'error']
        
        positive_count = sum(1 for token in doc if token.text.lower() in positive_words)
        negative_count = sum(1 for token in doc if token.text.lower() in negative_words)
        
        total_words = len([token for token in doc if token.is_alpha])
        
        if total_words == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / total_words
        return max(-1.0, min(1.0, sentiment * 5))  # Scale and clamp
    
    def _load_conversation_context(self, user_id: str, session_id: str) -> ConversationContext:
        """Load conversation context from storage."""
        
        try:
            context_key = f"context:{user_id}:{session_id}"
            context_data = self.redis_client.get(context_key)
            
            if context_data:
                data = json.loads(context_data)
                return ConversationContext(
                    session_id=session_id,
                    user_id=user_id,
                    conversation_history=data.get('conversation_history', []),
                    active_topics=data.get('active_topics', []),
                    intent_sequence=data.get('intent_sequence', []),
                    emotional_state=data.get('emotional_state', {}),
                    technical_context=data.get('technical_context', {}),
                    user_preferences=data.get('user_preferences', {}),
                    last_updated=datetime.fromisoformat(data.get('last_updated', datetime.utcnow().isoformat()))
                )
            
        except Exception as e:
            logger.error(f"Failed to load conversation context: {e}")
        
        # Return new context if loading failed
        return ConversationContext(
            session_id=session_id,
            user_id=user_id,
            conversation_history=[],
            active_topics=[],
            intent_sequence=[],
            emotional_state={},
            technical_context={},
            user_preferences={},
            last_updated=datetime.utcnow()
        )
    
    def _update_conversation_context(self, context: ConversationContext, text: str,
                                   entities: List[ContextEntity], user_id: str, session_id: str) -> ConversationContext:
        """Update conversation context with new information."""
        
        # Add to conversation history
        context.conversation_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'text': text,
            'entities': [asdict(entity) for entity in entities]
        })
        
        # Limit history length
        max_length = self.session_config['max_history_length']
        if len(context.conversation_history) > max_length:
            context.conversation_history = context.conversation_history[-max_length:]
        
        # Update active topics
        technical_entities = [e for e in entities if e.entity_type.startswith('technical_')]
        for entity in technical_entities:
            if entity.value not in context.active_topics:
                context.active_topics.append(entity.value)
        
        # Update intent sequence
        intent_entities = [e for e in entities if e.entity_type == 'task_intent']
        for entity in intent_entities:
            context.intent_sequence.append(entity.value)
        
        # Limit intent sequence
        if len(context.intent_sequence) > 10:
            context.intent_sequence = context.intent_sequence[-10:]
        
        # Update emotional state
        emotional_entities = [e for e in entities if e.entity_type.startswith('emotional_')]
        for entity in emotional_entities:
            if isinstance(entity.value, dict) and 'label' in entity.value:
                context.emotional_state[entity.value['label']] = entity.value['score']
            else:
                context.emotional_state[entity.entity_type] = entity.confidence
        
        # Update technical context
        for entity in technical_entities:
            category = entity.entity_type.replace('technical_', '')
            if category not in context.technical_context:
                context.technical_context[category] = []
            if entity.value not in context.technical_context[category]:
                context.technical_context[category].append(entity.value)
        
        context.last_updated = datetime.utcnow()
        
        return context
    
    def _store_conversation_context(self, context: ConversationContext):
        """Store conversation context to Redis."""
        
        try:
            context_key = f"context:{context.user_id}:{context.session_id}"
            context_data = {
                'conversation_history': context.conversation_history,
                'active_topics': context.active_topics,
                'intent_sequence': context.intent_sequence,
                'emotional_state': context.emotional_state,
                'technical_context': context.technical_context,
                'user_preferences': context.user_preferences,
                'last_updated': context.last_updated.isoformat()
            }
            
            # Store with expiration
            expiration_hours = self.session_config['context_retention_hours']
            self.redis_client.setex(
                context_key,
                expiration_hours * 3600,
                json.dumps(context_data, default=str)
            )
            
        except Exception as e:
            logger.error(f"Failed to store conversation context: {e}")
    
    def _generate_context_summary(self, entities: List[ContextEntity], 
                                 context: ConversationContext) -> Dict[str, Any]:
        """Generate context summary."""
        
        summary = {
            'entity_count': len(entities),
            'entity_types': list(set(e.entity_type for e in entities)),
            'high_confidence_entities': len([e for e in entities if e.confidence > 0.8]),
            'conversation_length': len(context.conversation_history),
            'active_topics_count': len(context.active_topics),
            'recent_intents': context.intent_sequence[-3:] if context.intent_sequence else [],
            'dominant_emotion': max(context.emotional_state.items(), key=lambda x: x[1])[0] if context.emotional_state else None,
            'technical_domains': list(context.technical_context.keys()),
            'context_richness': self._calculate_context_richness(entities, context)
        }
        
        return summary
    
    def _calculate_context_confidence(self, entities: List[ContextEntity]) -> float:
        """Calculate overall context confidence."""
        
        if not entities:
            return 0.0
        
        # Weight by relevance and confidence
        weighted_confidence = sum(e.confidence * e.relevance_score for e in entities)
        total_weight = sum(e.relevance_score for e in entities)
        
        return weighted_confidence / total_weight if total_weight > 0 else 0.0
    
    def _calculate_context_richness(self, entities: List[ContextEntity], 
                                   context: ConversationContext) -> float:
        """Calculate context richness score."""
        
        richness_factors = {
            'entity_diversity': len(set(e.entity_type for e in entities)) / 10.0,
            'conversation_depth': min(len(context.conversation_history) / 10.0, 1.0),
            'technical_breadth': len(context.technical_context) / 5.0,
            'emotional_awareness': len(context.emotional_state) / 4.0,
            'intent_consistency': len(set(context.intent_sequence)) / max(len(context.intent_sequence), 1)
        }
        
        return min(1.0, sum(richness_factors.values()) / len(richness_factors))
    
    def _identify_context_changes(self, entities: List[ContextEntity], 
                                 context: ConversationContext) -> List[str]:
        """Identify significant context changes."""
        
        changes = []
        
        # Check for topic shifts
        current_topics = [e.value for e in entities if e.entity_type.startswith('technical_')]
        if current_topics and context.active_topics:
            new_topics = set(current_topics) - set(context.active_topics)
            if new_topics:
                changes.append(f"New topics introduced: {', '.join(new_topics)}")
        
        # Check for intent changes
        current_intents = [e.value for e in entities if e.entity_type == 'task_intent']
        if current_intents and context.intent_sequence:
            if current_intents[-1] != context.intent_sequence[-1]:
                changes.append(f"Intent changed from {context.intent_sequence[-1]} to {current_intents[-1]}")
        
        # Check for emotional state changes
        emotional_entities = [e for e in entities if e.entity_type.startswith('emotional_')]
        if emotional_entities and context.emotional_state:
            current_emotions = {e.entity_type: e.confidence for e in emotional_entities}
            for emotion, confidence in current_emotions.items():
                if emotion in context.emotional_state:
                    if abs(confidence - context.emotional_state[emotion]) > 0.3:
                        changes.append(f"Emotional state change: {emotion}")
        
        return changes


# Example usage
if __name__ == "__main__":
    # Initialize context extraction module
    context_extractor = ContextExtractionModule()
    
    # Test context extraction
    test_text = "I'm working on a Python Flask application with PostgreSQL. Can you help me optimize the database queries we discussed yesterday?"
    
    result = context_extractor.extract_context(
        text=test_text,
        user_id="test_user",
        session_id="test_session"
    )
    
    print(f"Extracted {len(result.extracted_entities)} entities")
    print(f"Context confidence: {result.confidence_score:.3f}")
    print(f"Processing time: {result.processing_time_ms:.2f}ms")
    print(f"Context changes: {result.context_changes}")
    
    for entity in result.extracted_entities[:5]:
        print(f"  - {entity.entity_type}: {entity.value} (confidence: {entity.confidence:.2f})")
