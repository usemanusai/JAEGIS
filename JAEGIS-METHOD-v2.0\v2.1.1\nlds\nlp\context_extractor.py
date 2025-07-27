"""
N.L.D.S. Context Extraction Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced context extraction for conversation continuity, session management,
and contextual understanding with 24-hour retention capability.
"""

import json
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import asyncio
from collections import deque, defaultdict

# Local imports
from .tokenizer import TokenizationResult, Token
from .semantic_analyzer import SemanticAnalysisResult
from .intent_recognizer import IntentRecognitionResult, IntentCategory

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# CONTEXT DATA STRUCTURES
# ============================================================================

class ContextType(Enum):
    """Types of context information."""
    USER_PROFILE = "user_profile"
    SESSION_STATE = "session_state"
    CONVERSATION_HISTORY = "conversation_history"
    TASK_CONTEXT = "task_context"
    JAEGIS_STATE = "jaegis_state"
    TEMPORAL_CONTEXT = "temporal_context"
    ENTITY_CONTEXT = "entity_context"
    INTENT_CONTEXT = "intent_context"


class ContextScope(Enum):
    """Scope of context information."""
    IMMEDIATE = "immediate"      # Current turn
    SHORT_TERM = "short_term"    # Last 5 turns
    MEDIUM_TERM = "medium_term"  # Last hour
    LONG_TERM = "long_term"      # Session duration
    PERSISTENT = "persistent"    # Cross-session


@dataclass
class ContextItem:
    """Individual context item."""
    key: str
    value: Any
    context_type: ContextType
    scope: ContextScope
    confidence: float
    timestamp: datetime
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.expires_at is None:
            # Default expiration based on scope
            if self.scope == ContextScope.IMMEDIATE:
                self.expires_at = self.timestamp + timedelta(minutes=5)
            elif self.scope == ContextScope.SHORT_TERM:
                self.expires_at = self.timestamp + timedelta(minutes=30)
            elif self.scope == ContextScope.MEDIUM_TERM:
                self.expires_at = self.timestamp + timedelta(hours=1)
            elif self.scope == ContextScope.LONG_TERM:
                self.expires_at = self.timestamp + timedelta(hours=24)
            # PERSISTENT items don't expire


@dataclass
class ConversationTurn:
    """Single conversation turn."""
    turn_id: str
    user_input: str
    system_response: Optional[str]
    intent: Optional[IntentCategory]
    entities: List[Dict[str, Any]]
    context_updates: List[ContextItem]
    timestamp: datetime
    processing_time_ms: float
    metadata: Dict[str, Any] = None


@dataclass
class ContextExtractionResult:
    """Result of context extraction."""
    extracted_context: Dict[str, ContextItem]
    updated_context: Dict[str, ContextItem]
    conversation_state: Dict[str, Any]
    entity_references: Dict[str, Any]
    temporal_markers: List[Dict[str, Any]]
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# CONTEXT EXTRACTION ENGINE
# ============================================================================

class ContextExtractionEngine:
    """
    Advanced context extraction engine for conversation continuity.
    
    Features:
    - Multi-scope context management (immediate to persistent)
    - Entity tracking and reference resolution
    - Temporal context understanding
    - JAEGIS-specific state management
    - Conversation flow analysis
    - Context decay and cleanup
    - Cross-session context persistence
    """
    
    def __init__(self, session_id: str, user_id: str):
        """
        Initialize context extraction engine.
        
        Args:
            session_id: Current session identifier
            user_id: User identifier
        """
        self.session_id = session_id
        self.user_id = user_id
        
        # Context storage
        self.context_store: Dict[str, ContextItem] = {}
        self.conversation_history: deque = deque(maxlen=100)  # Last 100 turns
        self.entity_tracker: Dict[str, Any] = {}
        self.jaegis_state: Dict[str, Any] = {}
        
        # Context patterns and rules
        self.context_patterns = self._load_context_patterns()
        self.entity_patterns = self._load_entity_patterns()
        self.temporal_patterns = self._load_temporal_patterns()
        
        # Initialize with default context
        self._initialize_default_context()
    
    def _load_context_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for context extraction."""
        return {
            "reference_pronouns": [
                "it", "this", "that", "these", "those", "they", "them",
                "he", "she", "his", "her", "its", "their"
            ],
            "temporal_references": [
                "now", "today", "yesterday", "tomorrow", "later", "earlier",
                "before", "after", "then", "next", "previous", "last"
            ],
            "continuation_markers": [
                "also", "additionally", "furthermore", "moreover", "besides",
                "and", "plus", "as well", "too", "again"
            ],
            "task_references": [
                "task", "project", "work", "job", "assignment", "activity",
                "process", "workflow", "pipeline", "operation"
            ],
            "jaegis_references": [
                "squad", "mode", "agent", "system", "configuration",
                "deployment", "analysis", "report", "status"
            ]
        }
    
    def _load_entity_patterns(self) -> Dict[str, str]:
        """Load entity recognition patterns."""
        return {
            "squad_names": r"\b(?:development|quality|business|process|content|system|task-management|agent-builder|system-coherence|temporal-intelligence|iuas|garas|security|compliance|audit|backup)-squad\b",
            "mode_numbers": r"\bmode-[1-5]\b",
            "agent_types": r"\b(?:agent|bot|assistant|helper|processor)\b",
            "file_paths": r"[/\\][\w/\\.-]+",
            "urls": r"https?://[\w.-]+(?:/[\w.-]*)*",
            "emails": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "dates": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            "times": r"\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\b"
        }
    
    def _load_temporal_patterns(self) -> Dict[str, str]:
        """Load temporal pattern recognition."""
        return {
            "relative_time": r"\b(?:in|after|before|within)\s+\d+\s+(?:minutes?|hours?|days?|weeks?|months?)\b",
            "absolute_time": r"\b(?:at|on|by)\s+\d{1,2}:\d{2}\b",
            "time_periods": r"\b(?:morning|afternoon|evening|night|today|tomorrow|yesterday)\b",
            "duration": r"\b\d+\s+(?:minutes?|hours?|days?|weeks?|months?)\b"
        }
    
    def _initialize_default_context(self):
        """Initialize default context items."""
        now = datetime.utcnow()
        
        # Session context
        self.add_context_item(
            "session_id", self.session_id,
            ContextType.SESSION_STATE, ContextScope.LONG_TERM,
            confidence=1.0, timestamp=now
        )
        
        self.add_context_item(
            "user_id", self.user_id,
            ContextType.USER_PROFILE, ContextScope.PERSISTENT,
            confidence=1.0, timestamp=now
        )
        
        # JAEGIS default state
        self.add_context_item(
            "current_mode", 1,
            ContextType.JAEGIS_STATE, ContextScope.LONG_TERM,
            confidence=0.8, timestamp=now
        )
        
        self.add_context_item(
            "active_squads", [],
            ContextType.JAEGIS_STATE, ContextScope.MEDIUM_TERM,
            confidence=1.0, timestamp=now
        )
    
    def add_context_item(self, key: str, value: Any, context_type: ContextType,
                        scope: ContextScope, confidence: float,
                        timestamp: Optional[datetime] = None,
                        metadata: Optional[Dict[str, Any]] = None):
        """Add or update context item."""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        context_item = ContextItem(
            key=key,
            value=value,
            context_type=context_type,
            scope=scope,
            confidence=confidence,
            timestamp=timestamp,
            metadata=metadata or {}
        )
        
        self.context_store[key] = context_item
        logger.debug(f"Added context item: {key} = {value}")
    
    def get_context_item(self, key: str) -> Optional[ContextItem]:
        """Get context item by key."""
        item = self.context_store.get(key)
        if item and self._is_context_valid(item):
            return item
        elif item:
            # Remove expired item
            del self.context_store[key]
        return None
    
    def _is_context_valid(self, item: ContextItem) -> bool:
        """Check if context item is still valid."""
        if item.expires_at is None:
            return True  # Persistent items
        return datetime.utcnow() < item.expires_at
    
    def extract_entities(self, text: str, tokenization_result: TokenizationResult) -> Dict[str, Any]:
        """Extract entities from text and tokens."""
        entities = {}
        
        # Extract from tokens
        for token in tokenization_result.tokens:
            if token.token_type.value in ["jaegis_entity", "jaegis_command"]:
                entity_type = "jaegis_entity" if token.token_type.value == "jaegis_entity" else "jaegis_command"
                if entity_type not in entities:
                    entities[entity_type] = []
                entities[entity_type].append({
                    "text": token.text,
                    "normalized": token.normalized,
                    "position": (token.start_pos, token.end_pos),
                    "confidence": token.confidence
                })
        
        # Extract using patterns
        import re
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if entity_type not in entities:
                    entities[entity_type] = []
                entities[entity_type].append({
                    "text": match.group(),
                    "position": (match.start(), match.end()),
                    "confidence": 0.9
                })
        
        return entities
    
    def extract_temporal_markers(self, text: str) -> List[Dict[str, Any]]:
        """Extract temporal markers and references."""
        temporal_markers = []
        
        import re
        for marker_type, pattern in self.temporal_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                temporal_markers.append({
                    "type": marker_type,
                    "text": match.group(),
                    "position": (match.start(), match.end()),
                    "confidence": 0.8
                })
        
        return temporal_markers
    
    def resolve_references(self, text: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve pronoun and entity references."""
        references = {}
        text_lower = text.lower()
        
        # Check for reference pronouns
        for pronoun in self.context_patterns["reference_pronouns"]:
            if pronoun in text_lower:
                # Find most recent relevant entity
                recent_entity = self._find_recent_entity(pronoun)
                if recent_entity:
                    references[pronoun] = recent_entity
        
        # Check for continuation markers
        has_continuation = any(marker in text_lower 
                             for marker in self.context_patterns["continuation_markers"])
        
        if has_continuation:
            references["continuation_context"] = self._get_recent_context()
        
        return references
    
    def _find_recent_entity(self, pronoun: str) -> Optional[Dict[str, Any]]:
        """Find most recent entity that could be referenced by pronoun."""
        # Look through recent conversation history
        for turn in reversed(list(self.conversation_history)[-5:]):  # Last 5 turns
            for entity_list in turn.entities:
                if entity_list:  # If entities exist in this turn
                    return {
                        "entity": entity_list[0],  # Most prominent entity
                        "turn_id": turn.turn_id,
                        "confidence": 0.7
                    }
        return None
    
    def _get_recent_context(self) -> Dict[str, Any]:
        """Get recent conversation context."""
        if not self.conversation_history:
            return {}
        
        recent_turn = self.conversation_history[-1]
        return {
            "last_intent": recent_turn.intent.value if recent_turn.intent else None,
            "last_entities": recent_turn.entities,
            "turn_id": recent_turn.turn_id,
            "timestamp": recent_turn.timestamp.isoformat()
        }
    
    def update_jaegis_state(self, intent_result: IntentRecognitionResult):
        """Update JAEGIS-specific state based on intent."""
        now = datetime.utcnow()
        
        # Update based on intent
        if intent_result.primary_intent.intent == IntentCategory.MODE_SELECTION:
            # Extract mode number from JAEGIS mapping
            mode = intent_result.jaegis_mapping.get("target_modes", [1])[0]
            self.add_context_item(
                "current_mode", mode,
                ContextType.JAEGIS_STATE, ContextScope.LONG_TERM,
                confidence=intent_result.primary_intent.confidence,
                timestamp=now
            )
        
        elif intent_result.primary_intent.intent == IntentCategory.SQUAD_ACTIVATION:
            # Update active squads
            current_squads = self.get_context_item("active_squads")
            squad_list = current_squads.value if current_squads else []
            
            # Add new squad (extract from text or mapping)
            if "squad_name" in intent_result.jaegis_mapping.get("required_parameters", []):
                # This would be extracted from the actual text in a real implementation
                squad_list.append("extracted_squad_name")
            
            self.add_context_item(
                "active_squads", squad_list,
                ContextType.JAEGIS_STATE, ContextScope.MEDIUM_TERM,
                confidence=intent_result.primary_intent.confidence,
                timestamp=now
            )
        
        # Update last intent
        self.add_context_item(
            "last_intent", intent_result.primary_intent.intent.value,
            ContextType.INTENT_CONTEXT, ContextScope.SHORT_TERM,
            confidence=intent_result.primary_intent.confidence,
            timestamp=now
        )
    
    def add_conversation_turn(self, turn: ConversationTurn):
        """Add conversation turn to history."""
        self.conversation_history.append(turn)
        
        # Update context based on turn
        for context_update in turn.context_updates:
            self.context_store[context_update.key] = context_update
    
    def get_conversation_context(self, scope: ContextScope = ContextScope.SHORT_TERM) -> Dict[str, Any]:
        """Get conversation context for specified scope."""
        context = {}
        
        if scope == ContextScope.IMMEDIATE and self.conversation_history:
            # Last turn only
            last_turn = self.conversation_history[-1]
            context = {
                "last_input": last_turn.user_input,
                "last_intent": last_turn.intent.value if last_turn.intent else None,
                "last_entities": last_turn.entities
            }
        
        elif scope == ContextScope.SHORT_TERM:
            # Last 5 turns
            recent_turns = list(self.conversation_history)[-5:]
            context = {
                "recent_intents": [turn.intent.value for turn in recent_turns if turn.intent],
                "recent_entities": [entity for turn in recent_turns for entity in turn.entities],
                "turn_count": len(recent_turns)
            }
        
        elif scope == ContextScope.MEDIUM_TERM:
            # Last hour of conversation
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            recent_turns = [turn for turn in self.conversation_history 
                          if turn.timestamp > one_hour_ago]
            context = {
                "session_intents": [turn.intent.value for turn in recent_turns if turn.intent],
                "session_entities": [entity for turn in recent_turns for entity in turn.entities],
                "session_duration": len(recent_turns)
            }
        
        return context
    
    def cleanup_expired_context(self):
        """Remove expired context items."""
        now = datetime.utcnow()
        expired_keys = []
        
        for key, item in self.context_store.items():
            if not self._is_context_valid(item):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.context_store[key]
            logger.debug(f"Removed expired context item: {key}")
    
    async def extract_context(self, text: str,
                            tokenization_result: TokenizationResult,
                            semantic_result: SemanticAnalysisResult,
                            intent_result: IntentRecognitionResult) -> ContextExtractionResult:
        """
        Perform complete context extraction.
        
        Args:
            text: Input text
            tokenization_result: Tokenization results
            semantic_result: Semantic analysis results
            intent_result: Intent recognition results
            
        Returns:
            Complete context extraction result
        """
        import time
        start_time = time.time()
        
        try:
            # Clean up expired context first
            self.cleanup_expired_context()
            
            # Extract entities
            entities = self.extract_entities(text, tokenization_result)
            
            # Extract temporal markers
            temporal_markers = self.extract_temporal_markers(text)
            
            # Resolve references
            entity_references = self.resolve_references(text, entities)
            
            # Update JAEGIS state
            self.update_jaegis_state(intent_result)
            
            # Extract new context items
            extracted_context = {}
            now = datetime.utcnow()
            
            # Add entities as context
            for entity_type, entity_list in entities.items():
                if entity_list:
                    extracted_context[f"current_{entity_type}"] = ContextItem(
                        key=f"current_{entity_type}",
                        value=entity_list,
                        context_type=ContextType.ENTITY_CONTEXT,
                        scope=ContextScope.SHORT_TERM,
                        confidence=0.8,
                        timestamp=now
                    )
            
            # Add temporal context
            if temporal_markers:
                extracted_context["temporal_markers"] = ContextItem(
                    key="temporal_markers",
                    value=temporal_markers,
                    context_type=ContextType.TEMPORAL_CONTEXT,
                    scope=ContextScope.IMMEDIATE,
                    confidence=0.7,
                    timestamp=now
                )
            
            # Get current conversation state
            conversation_state = {
                "session_id": self.session_id,
                "user_id": self.user_id,
                "turn_count": len(self.conversation_history),
                "context_items": len(self.context_store),
                "jaegis_state": {
                    "current_mode": self.get_context_item("current_mode").value if self.get_context_item("current_mode") else 1,
                    "active_squads": self.get_context_item("active_squads").value if self.get_context_item("active_squads") else []
                }
            }
            
            # Update context store with extracted items
            updated_context = {}
            for key, item in extracted_context.items():
                self.context_store[key] = item
                updated_context[key] = item
            
            processing_time = (time.time() - start_time) * 1000
            
            return ContextExtractionResult(
                extracted_context=extracted_context,
                updated_context=updated_context,
                conversation_state=conversation_state,
                entity_references=entity_references,
                temporal_markers=temporal_markers,
                processing_time_ms=processing_time,
                metadata={
                    "entities_found": len(entities),
                    "temporal_markers_found": len(temporal_markers),
                    "references_resolved": len(entity_references),
                    "context_items_total": len(self.context_store),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Context extraction failed: {e}")
            
            return ContextExtractionResult(
                extracted_context={},
                updated_context={},
                conversation_state={"error": str(e)},
                entity_references={},
                temporal_markers=[],
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )
    
    def export_context(self) -> Dict[str, Any]:
        """Export context for persistence."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "context_store": {
                key: asdict(item) for key, item in self.context_store.items()
                if item.scope == ContextScope.PERSISTENT
            },
            "conversation_history": [
                asdict(turn) for turn in list(self.conversation_history)[-10:]  # Last 10 turns
            ],
            "jaegis_state": self.jaegis_state,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def import_context(self, context_data: Dict[str, Any]):
        """Import context from persistence."""
        try:
            # Restore persistent context items
            if "context_store" in context_data:
                for key, item_data in context_data["context_store"].items():
                    # Convert back to ContextItem
                    item_data["timestamp"] = datetime.fromisoformat(item_data["timestamp"])
                    if item_data["expires_at"]:
                        item_data["expires_at"] = datetime.fromisoformat(item_data["expires_at"])
                    item_data["context_type"] = ContextType(item_data["context_type"])
                    item_data["scope"] = ContextScope(item_data["scope"])
                    
                    context_item = ContextItem(**item_data)
                    if self._is_context_valid(context_item):
                        self.context_store[key] = context_item
            
            # Restore JAEGIS state
            if "jaegis_state" in context_data:
                self.jaegis_state = context_data["jaegis_state"]
            
            logger.info(f"Imported context for session {self.session_id}")
            
        except Exception as e:
            logger.error(f"Failed to import context: {e}")


# ============================================================================
# CONTEXT UTILITIES
# ============================================================================

class ContextUtils:
    """Utility functions for context management."""
    
    @staticmethod
    def merge_contexts(context1: Dict[str, ContextItem], 
                      context2: Dict[str, ContextItem]) -> Dict[str, ContextItem]:
        """Merge two context dictionaries."""
        merged = context1.copy()
        
        for key, item in context2.items():
            if key in merged:
                # Keep the more recent or higher confidence item
                existing = merged[key]
                if (item.timestamp > existing.timestamp or 
                    item.confidence > existing.confidence):
                    merged[key] = item
            else:
                merged[key] = item
        
        return merged
    
    @staticmethod
    def filter_context_by_type(context: Dict[str, ContextItem], 
                              context_type: ContextType) -> Dict[str, ContextItem]:
        """Filter context items by type."""
        return {key: item for key, item in context.items() 
                if item.context_type == context_type}
    
    @staticmethod
    def get_context_summary(context: Dict[str, ContextItem]) -> Dict[str, Any]:
        """Get summary statistics of context."""
        if not context:
            return {"empty": True}
        
        type_counts = defaultdict(int)
        scope_counts = defaultdict(int)
        total_confidence = 0
        
        for item in context.values():
            type_counts[item.context_type.value] += 1
            scope_counts[item.scope.value] += 1
            total_confidence += item.confidence
        
        return {
            "total_items": len(context),
            "type_distribution": dict(type_counts),
            "scope_distribution": dict(scope_counts),
            "average_confidence": total_confidence / len(context),
            "oldest_item": min(item.timestamp for item in context.values()).isoformat(),
            "newest_item": max(item.timestamp for item in context.values()).isoformat()
        }
