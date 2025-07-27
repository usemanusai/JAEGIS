"""
N.L.D.S. Named Entity Recognition Processor
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced Named Entity Recognition with custom JAEGIS entity models,
squad names, mode numbers, command parameters, and domain-specific entities.
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import asyncio

# NLP imports
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Local imports
from .tokenizer import TokenizationResult, Token

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# ENTITY TYPES AND STRUCTURES
# ============================================================================

class EntityType(Enum):
    """JAEGIS-specific entity types."""
    
    # JAEGIS Core Entities
    SQUAD_NAME = "SQUAD_NAME"
    MODE_NUMBER = "MODE_NUMBER"
    AGENT_TYPE = "AGENT_TYPE"
    COMMAND_NAME = "COMMAND_NAME"
    PARAMETER_NAME = "PARAMETER_NAME"
    
    # System Entities
    FILE_PATH = "FILE_PATH"
    URL = "URL"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    DATE = "DATE"
    TIME = "TIME"
    
    # Technical Entities
    API_ENDPOINT = "API_ENDPOINT"
    DATABASE_NAME = "DATABASE_NAME"
    SERVICE_NAME = "SERVICE_NAME"
    CONFIGURATION_KEY = "CONFIGURATION_KEY"
    
    # Business Entities
    PROJECT_NAME = "PROJECT_NAME"
    TASK_ID = "TASK_ID"
    USER_ROLE = "USER_ROLE"
    DEPARTMENT = "DEPARTMENT"
    
    # Generic Entities
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    PRODUCT = "PRODUCT"
    
    # Unknown
    UNKNOWN = "UNKNOWN"


@dataclass
class EntityMention:
    """Individual entity mention."""
    text: str
    entity_type: EntityType
    start_pos: int
    end_pos: int
    confidence: float
    normalized_value: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.normalized_value is None:
            self.normalized_value = self.text.lower().strip()


@dataclass
class EntityRecognitionResult:
    """Complete NER result."""
    text: str
    entities: List[EntityMention]
    entity_counts: Dict[str, int]
    jaegis_entities: List[EntityMention]
    confidence_scores: Dict[str, float]
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# NER PROCESSOR ENGINE
# ============================================================================

class NERProcessor:
    """
    Advanced Named Entity Recognition processor.
    
    Features:
    - Custom JAEGIS entity recognition
    - Pre-trained transformer models
    - Rule-based pattern matching
    - Entity linking and normalization
    - Confidence scoring
    - Multi-model ensemble
    """
    
    def __init__(self, model_name: str = "dbmdz/bert-large-cased-finetuned-conll03-english"):
        """
        Initialize NER processor.
        
        Args:
            model_name: Pre-trained NER model name
        """
        self.model_name = model_name
        self.models = {}
        self.entity_patterns = self._load_entity_patterns()
        self.jaegis_entities = self._load_jaegis_entities()
        self.normalization_rules = self._load_normalization_rules()
        
        # Initialize models
        self._initialize_models()
    
    def _load_entity_patterns(self) -> Dict[str, str]:
        """Load regex patterns for entity recognition."""
        return {
            # JAEGIS Specific Patterns
            EntityType.SQUAD_NAME.value: r'\b(?:development|quality|business|process|content|system|task-management|agent-builder|system-coherence|temporal-intelligence|iuas|garas|security|compliance|audit|backup)-squad\b',
            EntityType.MODE_NUMBER.value: r'\bmode-[1-5]\b',
            EntityType.AGENT_TYPE.value: r'\b(?:agent|bot|assistant|helper|processor|analyzer|generator|optimizer|validator|monitor)\b',
            EntityType.COMMAND_NAME.value: r'/(?:jaegis|nlds|mode|squad|create|update|delete|analyze|process|generate|optimize|validate|execute|monitor|configure|deploy|backup)-[\w-]*',
            
            # System Patterns
            EntityType.FILE_PATH.value: r'(?:[a-zA-Z]:\\|/)[^\s<>:"|?*]+',
            EntityType.URL.value: r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
            EntityType.EMAIL.value: r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            EntityType.PHONE.value: r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            EntityType.DATE.value: r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b',
            EntityType.TIME.value: r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\b',
            
            # Technical Patterns
            EntityType.API_ENDPOINT.value: r'/api/v?\d*/[\w/-]+',
            EntityType.DATABASE_NAME.value: r'\b(?:postgres|mysql|mongodb|redis|elasticsearch)_[\w_]+\b',
            EntityType.SERVICE_NAME.value: r'\b[\w-]+-service\b',
            EntityType.CONFIGURATION_KEY.value: r'\b[A-Z_][A-Z0-9_]*\b',
            
            # Business Patterns
            EntityType.PROJECT_NAME.value: r'\b(?:project|proj)-[\w-]+\b',
            EntityType.TASK_ID.value: r'\b(?:task|ticket|issue)-\d+\b',
            EntityType.USER_ROLE.value: r'\b(?:admin|user|developer|analyst|manager|lead|senior|junior)\b',
            EntityType.DEPARTMENT.value: r'\b(?:engineering|development|qa|testing|devops|security|compliance|business|marketing|sales|support)\b'
        }
    
    def _load_jaegis_entities(self) -> Dict[str, List[str]]:
        """Load JAEGIS-specific entity vocabularies."""
        return {
            "squads": [
                "development-squad", "quality-squad", "business-squad",
                "process-squad", "content-squad", "system-squad",
                "task-management-squad", "agent-builder-squad",
                "system-coherence-squad", "temporal-intelligence-squad",
                "iuas-squad", "garas-squad", "security-squad",
                "compliance-squad", "audit-squad", "backup-squad"
            ],
            "modes": [
                "mode-1", "mode-2", "mode-3", "mode-4", "mode-5",
                "basic-mode", "advanced-mode", "expert-mode",
                "agent-creator-mode", "system-mode"
            ],
            "agents": [
                "agent", "bot", "assistant", "helper", "processor",
                "analyzer", "generator", "optimizer", "validator",
                "monitor", "coordinator", "orchestrator"
            ],
            "commands": [
                "create", "update", "delete", "read", "execute",
                "analyze", "process", "generate", "optimize",
                "validate", "monitor", "configure", "deploy",
                "backup", "restore", "migrate", "scale"
            ],
            "parameters": [
                "name", "type", "value", "config", "settings",
                "options", "properties", "attributes", "metadata",
                "context", "scope", "priority", "timeout"
            ]
        }
    
    def _load_normalization_rules(self) -> Dict[str, Dict[str, str]]:
        """Load entity normalization rules."""
        return {
            EntityType.SQUAD_NAME.value: {
                "dev-squad": "development-squad",
                "qa-squad": "quality-squad",
                "biz-squad": "business-squad",
                "sys-squad": "system-squad"
            },
            EntityType.MODE_NUMBER.value: {
                "mode1": "mode-1",
                "mode2": "mode-2",
                "mode3": "mode-3",
                "mode4": "mode-4",
                "mode5": "mode-5"
            },
            EntityType.USER_ROLE.value: {
                "dev": "developer",
                "qa": "analyst",
                "admin": "administrator",
                "mgr": "manager"
            }
        }
    
    def _initialize_models(self):
        """Initialize NER models."""
        try:
            # Load spaCy model
            self.models["spacy"] = spacy.load("en_core_web_lg")
            logger.info("Loaded spaCy NER model")
            
            # Load transformer model
            self.models["transformer"] = pipeline(
                "ner",
                model=self.model_name,
                tokenizer=self.model_name,
                aggregation_strategy="simple"
            )
            logger.info(f"Loaded transformer NER model: {self.model_name}")
            
        except Exception as e:
            logger.warning(f"Failed to load some NER models: {e}")
            # Fallback to basic spaCy
            try:
                import spacy.cli
                spacy.cli.download("en_core_web_sm")
                self.models["spacy"] = spacy.load("en_core_web_sm")
            except:
                logger.error("Failed to load any NER models")
    
    def extract_pattern_entities(self, text: str) -> List[EntityMention]:
        """Extract entities using regex patterns."""
        entities = []
        
        for entity_type_str, pattern in self.entity_patterns.items():
            entity_type = EntityType(entity_type_str)
            
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity_text = match.group().strip()
                
                # Normalize entity
                normalized = self._normalize_entity(entity_text, entity_type)
                
                # Calculate confidence based on pattern specificity
                confidence = self._calculate_pattern_confidence(entity_text, entity_type)
                
                entity = EntityMention(
                    text=entity_text,
                    entity_type=entity_type,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=confidence,
                    normalized_value=normalized,
                    metadata={
                        "extraction_method": "pattern",
                        "pattern": pattern[:50] + "..." if len(pattern) > 50 else pattern
                    }
                )
                
                entities.append(entity)
        
        return entities
    
    def extract_spacy_entities(self, text: str) -> List[EntityMention]:
        """Extract entities using spaCy NER."""
        entities = []
        
        if "spacy" not in self.models:
            return entities
        
        try:
            nlp = self.models["spacy"]
            doc = nlp(text)
            
            for ent in doc.ents:
                # Map spaCy labels to our entity types
                entity_type = self._map_spacy_label(ent.label_)
                
                entity = EntityMention(
                    text=ent.text,
                    entity_type=entity_type,
                    start_pos=ent.start_char,
                    end_pos=ent.end_char,
                    confidence=0.8,  # Default spaCy confidence
                    normalized_value=ent.text.lower().strip(),
                    metadata={
                        "extraction_method": "spacy",
                        "spacy_label": ent.label_,
                        "spacy_confidence": getattr(ent, 'confidence', 0.8)
                    }
                )
                
                entities.append(entity)
                
        except Exception as e:
            logger.warning(f"spaCy NER extraction failed: {e}")
        
        return entities
    
    def extract_transformer_entities(self, text: str) -> List[EntityMention]:
        """Extract entities using transformer model."""
        entities = []
        
        if "transformer" not in self.models:
            return entities
        
        try:
            ner_pipeline = self.models["transformer"]
            results = ner_pipeline(text)
            
            for result in results:
                # Map transformer labels to our entity types
                entity_type = self._map_transformer_label(result['entity_group'])
                
                entity = EntityMention(
                    text=result['word'],
                    entity_type=entity_type,
                    start_pos=result['start'],
                    end_pos=result['end'],
                    confidence=result['score'],
                    normalized_value=result['word'].lower().strip(),
                    metadata={
                        "extraction_method": "transformer",
                        "transformer_label": result['entity_group'],
                        "transformer_score": result['score']
                    }
                )
                
                entities.append(entity)
                
        except Exception as e:
            logger.warning(f"Transformer NER extraction failed: {e}")
        
        return entities
    
    def extract_jaegis_entities(self, text: str, tokenization_result: TokenizationResult) -> List[EntityMention]:
        """Extract JAEGIS-specific entities."""
        entities = []
        text_lower = text.lower()
        
        # Extract from tokenization results first
        for token in tokenization_result.tokens:
            if token.token_type.value in ["jaegis_entity", "jaegis_command"]:
                entity_type = self._classify_jaegis_entity(token.text)
                
                entity = EntityMention(
                    text=token.text,
                    entity_type=entity_type,
                    start_pos=token.start_pos,
                    end_pos=token.end_pos,
                    confidence=token.confidence,
                    normalized_value=token.normalized,
                    metadata={
                        "extraction_method": "tokenizer",
                        "token_type": token.token_type.value,
                        "token_metadata": token.metadata
                    }
                )
                
                entities.append(entity)
        
        # Extract using JAEGIS vocabularies
        for category, entity_list in self.jaegis_entities.items():
            for entity_text in entity_list:
                if entity_text.lower() in text_lower:
                    # Find position in text
                    start_pos = text_lower.find(entity_text.lower())
                    if start_pos != -1:
                        end_pos = start_pos + len(entity_text)
                        
                        # Determine entity type based on category
                        entity_type = self._get_entity_type_from_category(category)
                        
                        # Calculate confidence based on exact match
                        confidence = 0.95 if entity_text.lower() == text_lower[start_pos:end_pos] else 0.8
                        
                        entity = EntityMention(
                            text=text[start_pos:end_pos],
                            entity_type=entity_type,
                            start_pos=start_pos,
                            end_pos=end_pos,
                            confidence=confidence,
                            normalized_value=entity_text.lower(),
                            metadata={
                                "extraction_method": "jaegis_vocabulary",
                                "category": category,
                                "exact_match": entity_text.lower() == text_lower[start_pos:end_pos]
                            }
                        )
                        
                        entities.append(entity)
        
        return entities
    
    def _normalize_entity(self, text: str, entity_type: EntityType) -> str:
        """Normalize entity text."""
        normalized = text.lower().strip()
        
        # Apply normalization rules
        if entity_type.value in self.normalization_rules:
            rules = self.normalization_rules[entity_type.value]
            normalized = rules.get(normalized, normalized)
        
        return normalized
    
    def _calculate_pattern_confidence(self, text: str, entity_type: EntityType) -> float:
        """Calculate confidence for pattern-based extraction."""
        base_confidence = 0.7
        
        # Boost confidence for JAEGIS-specific entities
        if entity_type in [EntityType.SQUAD_NAME, EntityType.MODE_NUMBER, EntityType.COMMAND_NAME]:
            base_confidence = 0.9
        
        # Boost for exact vocabulary matches
        if entity_type == EntityType.SQUAD_NAME and text.lower() in self.jaegis_entities["squads"]:
            base_confidence = 0.95
        
        return base_confidence
    
    def _map_spacy_label(self, spacy_label: str) -> EntityType:
        """Map spaCy entity labels to our entity types."""
        mapping = {
            "PERSON": EntityType.PERSON,
            "ORG": EntityType.ORGANIZATION,
            "GPE": EntityType.LOCATION,
            "DATE": EntityType.DATE,
            "TIME": EntityType.TIME,
            "PRODUCT": EntityType.PRODUCT,
            "EMAIL": EntityType.EMAIL
        }
        
        return mapping.get(spacy_label, EntityType.UNKNOWN)
    
    def _map_transformer_label(self, transformer_label: str) -> EntityType:
        """Map transformer entity labels to our entity types."""
        mapping = {
            "PER": EntityType.PERSON,
            "ORG": EntityType.ORGANIZATION,
            "LOC": EntityType.LOCATION,
            "MISC": EntityType.UNKNOWN
        }
        
        return mapping.get(transformer_label, EntityType.UNKNOWN)
    
    def _classify_jaegis_entity(self, text: str) -> EntityType:
        """Classify JAEGIS entity type."""
        text_lower = text.lower()
        
        if "squad" in text_lower:
            return EntityType.SQUAD_NAME
        elif "mode" in text_lower:
            return EntityType.MODE_NUMBER
        elif "agent" in text_lower:
            return EntityType.AGENT_TYPE
        elif text_lower.startswith("/"):
            return EntityType.COMMAND_NAME
        else:
            return EntityType.UNKNOWN
    
    def _get_entity_type_from_category(self, category: str) -> EntityType:
        """Get entity type from JAEGIS category."""
        mapping = {
            "squads": EntityType.SQUAD_NAME,
            "modes": EntityType.MODE_NUMBER,
            "agents": EntityType.AGENT_TYPE,
            "commands": EntityType.COMMAND_NAME,
            "parameters": EntityType.PARAMETER_NAME
        }
        
        return mapping.get(category, EntityType.UNKNOWN)
    
    def merge_entities(self, entity_lists: List[List[EntityMention]]) -> List[EntityMention]:
        """Merge entities from multiple extraction methods."""
        all_entities = []
        for entity_list in entity_lists:
            all_entities.extend(entity_list)
        
        # Remove duplicates and overlaps
        merged_entities = []
        all_entities.sort(key=lambda e: e.start_pos)
        
        for entity in all_entities:
            # Check for overlaps with existing entities
            overlaps = False
            for existing in merged_entities:
                if (entity.start_pos < existing.end_pos and 
                    entity.end_pos > existing.start_pos):
                    # Overlap detected - keep the one with higher confidence
                    if entity.confidence > existing.confidence:
                        merged_entities.remove(existing)
                        merged_entities.append(entity)
                    overlaps = True
                    break
            
            if not overlaps:
                merged_entities.append(entity)
        
        # Sort by position
        merged_entities.sort(key=lambda e: e.start_pos)
        
        return merged_entities
    
    def filter_entities_by_confidence(self, entities: List[EntityMention], 
                                    min_confidence: float = 0.5) -> List[EntityMention]:
        """Filter entities by minimum confidence threshold."""
        return [entity for entity in entities if entity.confidence >= min_confidence]
    
    async def recognize_entities(self, text: str, 
                               tokenization_result: TokenizationResult) -> EntityRecognitionResult:
        """
        Perform complete named entity recognition.
        
        Args:
            text: Input text
            tokenization_result: Tokenization results
            
        Returns:
            Complete NER result
        """
        import time
        start_time = time.time()
        
        try:
            # Extract entities using different methods
            pattern_entities = self.extract_pattern_entities(text)
            spacy_entities = self.extract_spacy_entities(text)
            transformer_entities = self.extract_transformer_entities(text)
            jaegis_entities = self.extract_jaegis_entities(text, tokenization_result)
            
            # Merge all entities
            all_entities = self.merge_entities([
                pattern_entities,
                spacy_entities,
                transformer_entities,
                jaegis_entities
            ])
            
            # Filter by confidence
            filtered_entities = self.filter_entities_by_confidence(all_entities)
            
            # Calculate statistics
            entity_counts = {}
            confidence_scores = {}
            jaegis_only = []
            
            for entity in filtered_entities:
                entity_type = entity.entity_type.value
                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
                
                if entity_type not in confidence_scores:
                    confidence_scores[entity_type] = []
                confidence_scores[entity_type].append(entity.confidence)
                
                # Collect JAEGIS-specific entities
                if entity.entity_type in [EntityType.SQUAD_NAME, EntityType.MODE_NUMBER, 
                                        EntityType.AGENT_TYPE, EntityType.COMMAND_NAME]:
                    jaegis_only.append(entity)
            
            # Average confidence scores
            for entity_type in confidence_scores:
                confidence_scores[entity_type] = sum(confidence_scores[entity_type]) / len(confidence_scores[entity_type])
            
            processing_time = (time.time() - start_time) * 1000
            
            return EntityRecognitionResult(
                text=text,
                entities=filtered_entities,
                entity_counts=entity_counts,
                jaegis_entities=jaegis_only,
                confidence_scores=confidence_scores,
                processing_time_ms=processing_time,
                metadata={
                    "extraction_methods": ["pattern", "spacy", "transformer", "jaegis"],
                    "total_entities_found": len(all_entities),
                    "entities_after_filtering": len(filtered_entities),
                    "jaegis_entities_count": len(jaegis_only),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"NER processing failed: {e}")
            
            return EntityRecognitionResult(
                text=text,
                entities=[],
                entity_counts={},
                jaegis_entities=[],
                confidence_scores={},
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )


# ============================================================================
# NER UTILITIES
# ============================================================================

class NERUtils:
    """Utility functions for NER processing."""
    
    @staticmethod
    def entities_to_dict(entities: List[EntityMention]) -> List[Dict[str, Any]]:
        """Convert entities to dictionary format."""
        return [
            {
                "text": entity.text,
                "type": entity.entity_type.value,
                "start": entity.start_pos,
                "end": entity.end_pos,
                "confidence": entity.confidence,
                "normalized": entity.normalized_value,
                "metadata": entity.metadata
            }
            for entity in entities
        ]
    
    @staticmethod
    def group_entities_by_type(entities: List[EntityMention]) -> Dict[str, List[EntityMention]]:
        """Group entities by type."""
        grouped = {}
        for entity in entities:
            entity_type = entity.entity_type.value
            if entity_type not in grouped:
                grouped[entity_type] = []
            grouped[entity_type].append(entity)
        
        return grouped
    
    @staticmethod
    def get_entity_statistics(entities: List[EntityMention]) -> Dict[str, Any]:
        """Get statistics about extracted entities."""
        if not entities:
            return {"empty": True}
        
        type_counts = {}
        confidence_sum = 0
        
        for entity in entities:
            entity_type = entity.entity_type.value
            type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
            confidence_sum += entity.confidence
        
        return {
            "total_entities": len(entities),
            "unique_types": len(type_counts),
            "type_distribution": type_counts,
            "average_confidence": confidence_sum / len(entities),
            "highest_confidence": max(entity.confidence for entity in entities),
            "lowest_confidence": min(entity.confidence for entity in entities)
        }
