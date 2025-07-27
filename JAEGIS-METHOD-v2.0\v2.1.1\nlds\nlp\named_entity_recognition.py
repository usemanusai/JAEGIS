"""
N.L.D.S. Named Entity Recognition (NER)
Specialized NER for extracting entities relevant to JAEGIS operations (squads, modes, commands)
"""

import spacy
import re
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span
import numpy as np

logger = logging.getLogger(__name__)


class JAEGISEntityType(str, Enum):
    """JAEGIS-specific entity types."""
    SQUAD = "JAEGIS_SQUAD"
    AGENT = "JAEGIS_AGENT"
    COMMAND = "JAEGIS_COMMAND"
    MODE = "JAEGIS_MODE"
    COMPONENT = "JAEGIS_COMPONENT"
    TECHNOLOGY = "TECHNOLOGY"
    FRAMEWORK = "FRAMEWORK"
    DATABASE = "DATABASE"
    CLOUD_PLATFORM = "CLOUD_PLATFORM"
    PROGRAMMING_LANGUAGE = "PROGRAMMING_LANGUAGE"
    SECURITY_CONCEPT = "SECURITY_CONCEPT"
    DEPLOYMENT_TARGET = "DEPLOYMENT_TARGET"
    ARCHITECTURE_PATTERN = "ARCHITECTURE_PATTERN"


@dataclass
class JAEGISEntity:
    """JAEGIS-specific named entity."""
    text: str
    label: JAEGISEntityType
    start: int
    end: int
    confidence: float
    context: str
    attributes: Dict[str, Any]
    canonical_form: Optional[str] = None


@dataclass
class NERResult:
    """Named Entity Recognition result."""
    entities: List[JAEGISEntity]
    processing_time_ms: float
    confidence_score: float
    entity_count_by_type: Dict[str, int]
    relationships: List[Dict[str, Any]]


class JAEGISNamedEntityRecognizer:
    """
    Specialized Named Entity Recognizer for JAEGIS operations.
    
    Extracts entities relevant to JAEGIS squads, modes, commands,
    and technical components for enhanced command generation.
    """
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            logger.warning("Large spaCy model not found, using medium model")
            try:
                self.nlp = spacy.load("en_core_web_md")
            except OSError:
                self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize matchers
        self.matcher = Matcher(self.nlp.vocab)
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        
        # JAEGIS-specific entity definitions
        self.jaegis_entities = self._initialize_jaegis_entities()
        
        # Technology and framework entities
        self.tech_entities = self._initialize_tech_entities()
        
        # Initialize patterns and matchers
        self._setup_patterns()
        
        # Add custom entity labels to spaCy
        for entity_type in JAEGISEntityType:
            if entity_type.value not in self.nlp.pipe_labels['ner']:
                self.nlp.get_pipe('ner').add_label(entity_type.value)
        
        logger.info("JAEGIS Named Entity Recognizer initialized")
    
    def _initialize_jaegis_entities(self) -> Dict[str, Dict[str, Any]]:
        """Initialize JAEGIS-specific entity definitions."""
        
        return {
            # JAEGIS Squads
            "squads": {
                "development": {
                    "canonical": "development",
                    "aliases": ["dev", "development", "coding", "programming"],
                    "agents": ["FRED"],
                    "specialties": ["implementation", "coding", "building"]
                },
                "analysis": {
                    "canonical": "analysis",
                    "aliases": ["analysis", "research", "investigation", "analytics"],
                    "agents": ["TYLER"],
                    "specialties": ["analyzing", "investigating", "researching"]
                },
                "security": {
                    "canonical": "security",
                    "aliases": ["security", "sec", "cybersecurity", "infosec"],
                    "agents": ["SECURE"],
                    "specialties": ["protecting", "auditing", "securing"]
                },
                "content": {
                    "canonical": "content",
                    "aliases": ["content", "documentation", "docs", "writing"],
                    "agents": ["DOCUMENT"],
                    "specialties": ["documenting", "writing", "explaining"]
                },
                "integration": {
                    "canonical": "integration",
                    "aliases": ["integration", "connect", "sync", "orchestration"],
                    "agents": ["INTEGRATE"],
                    "specialties": ["connecting", "integrating", "synchronizing"]
                },
                "architecture": {
                    "canonical": "architecture",
                    "aliases": ["architecture", "design", "arch", "system design"],
                    "agents": ["ARCHITECT"],
                    "specialties": ["designing", "architecting", "planning"]
                },
                "garas": {
                    "canonical": "garas",
                    "aliases": ["garas", "gap analysis", "resolution"],
                    "agents": ["GARAS_ALPHA", "GARAS_BETA", "GARAS_GAMMA", "GARAS_DELTA", "GARAS_EPSILON"],
                    "specialties": ["gap analysis", "resolution", "optimization"]
                },
                "iuas": {
                    "canonical": "iuas",
                    "aliases": ["iuas", "infrastructure", "monitoring"],
                    "agents": ["IUAS_PRIME"],
                    "specialties": ["infrastructure", "monitoring", "maintenance"]
                }
            },
            
            # JAEGIS Agents
            "agents": {
                "JAEGIS": {"type": "orchestrator", "tier": 1},
                "JOHN": {"type": "coordinator", "tier": 2, "specialty": "planning"},
                "FRED": {"type": "coordinator", "tier": 2, "specialty": "implementation"},
                "TYLER": {"type": "coordinator", "tier": 2, "specialty": "validation"},
                "ARCHITECT": {"type": "specialized", "tier": 3, "specialty": "design"},
                "TECHNICAL": {"type": "specialized", "tier": 3, "specialty": "technical_lead"},
                "INTEGRATE": {"type": "specialized", "tier": 3, "specialty": "integration"},
                "QA": {"type": "specialized", "tier": 3, "specialty": "quality_assurance"},
                "SECURE": {"type": "specialized", "tier": 3, "specialty": "security"},
                "DOCUMENT": {"type": "specialized", "tier": 3, "specialty": "documentation"}
            },
            
            # JAEGIS Commands
            "commands": {
                "IMPLEMENT": {"squad": "development", "complexity": "medium"},
                "BUILD": {"squad": "development", "complexity": "high"},
                "CREATE": {"squad": "development", "complexity": "medium"},
                "ANALYZE": {"squad": "analysis", "complexity": "medium"},
                "INVESTIGATE": {"squad": "analysis", "complexity": "high"},
                "RESEARCH": {"squad": "analysis", "complexity": "medium"},
                "VALIDATE": {"squad": "analysis", "complexity": "low"},
                "DESIGN": {"squad": "architecture", "complexity": "high"},
                "ARCHITECT": {"squad": "architecture", "complexity": "high"},
                "PLAN": {"squad": "architecture", "complexity": "medium"},
                "SECURE": {"squad": "security", "complexity": "high"},
                "PROTECT": {"squad": "security", "complexity": "medium"},
                "AUDIT": {"squad": "security", "complexity": "high"},
                "DOCUMENT": {"squad": "content", "complexity": "low"},
                "EXPLAIN": {"squad": "content", "complexity": "low"},
                "WRITE": {"squad": "content", "complexity": "low"},
                "CONNECT": {"squad": "integration", "complexity": "medium"},
                "INTEGRATE": {"squad": "integration", "complexity": "high"},
                "SYNC": {"squad": "integration", "complexity": "medium"},
                "DEPLOY": {"squad": "integration", "complexity": "high"},
                "MONITOR": {"squad": "iuas", "complexity": "medium"},
                "MAINTAIN": {"squad": "iuas", "complexity": "medium"},
                "OPTIMIZE": {"squad": "garas", "complexity": "high"}
            },
            
            # JAEGIS Modes
            "modes": {
                "1": {"name": "basic", "complexity": "simple"},
                "2": {"name": "standard", "complexity": "moderate"},
                "3": {"name": "advanced", "complexity": "complex"},
                "4": {"name": "expert", "complexity": "highly_complex"},
                "5": {"name": "specialized", "complexity": "domain_specific"}
            }
        }
    
    def _initialize_tech_entities(self) -> Dict[str, List[str]]:
        """Initialize technology and framework entities."""
        
        return {
            "programming_languages": [
                "python", "javascript", "java", "c++", "c#", "go", "rust", "php",
                "ruby", "swift", "kotlin", "typescript", "scala", "r", "matlab"
            ],
            "frameworks": [
                "django", "flask", "fastapi", "react", "vue", "angular", "express",
                "spring", "laravel", "rails", "asp.net", "gin", "fiber", "echo"
            ],
            "databases": [
                "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
                "cassandra", "dynamodb", "sqlite", "oracle", "sql server"
            ],
            "cloud_platforms": [
                "aws", "azure", "gcp", "google cloud", "digital ocean",
                "heroku", "vercel", "netlify", "cloudflare"
            ],
            "technologies": [
                "docker", "kubernetes", "terraform", "ansible", "jenkins",
                "git", "nginx", "apache", "rabbitmq", "kafka", "graphql", "rest"
            ],
            "security_concepts": [
                "jwt", "oauth", "saml", "ssl", "tls", "encryption", "authentication",
                "authorization", "firewall", "vpn", "mfa", "2fa"
            ],
            "architecture_patterns": [
                "microservices", "monolith", "serverless", "event-driven",
                "mvc", "mvp", "mvvm", "clean architecture", "hexagonal"
            ]
        }
    
    def _setup_patterns(self):
        """Setup pattern matching for entity recognition."""
        
        # JAEGIS Squad patterns
        squad_patterns = []
        for squad, info in self.jaegis_entities["squads"].items():
            for alias in info["aliases"]:
                squad_patterns.append(self.nlp(alias))
        
        self.phrase_matcher.add("JAEGIS_SQUAD", squad_patterns)
        
        # JAEGIS Agent patterns
        agent_patterns = []
        for agent in self.jaegis_entities["agents"].keys():
            agent_patterns.append(self.nlp(agent))
        
        self.phrase_matcher.add("JAEGIS_AGENT", agent_patterns)
        
        # JAEGIS Command patterns
        command_patterns = []
        for command in self.jaegis_entities["commands"].keys():
            command_patterns.append(self.nlp(command))
        
        self.phrase_matcher.add("JAEGIS_COMMAND", command_patterns)
        
        # Technology patterns
        for tech_type, tech_list in self.tech_entities.items():
            patterns = [self.nlp(tech) for tech in tech_list]
            label = tech_type.upper()
            self.phrase_matcher.add(label, patterns)
        
        # Mode patterns (regex-based)
        mode_pattern = [{"TEXT": {"REGEX": r"mode\s*[1-5]"}}]
        self.matcher.add("JAEGIS_MODE", [mode_pattern])
        
        # Component patterns
        component_patterns = [
            [{"LOWER": {"IN": ["api", "service", "module", "component", "system"]}},
             {"LOWER": {"IN": ["authentication", "authorization", "user", "payment", "notification"]}, "OP": "?"}],
            [{"LOWER": {"IN": ["database", "db", "cache", "queue", "storage"]}},
             {"LOWER": {"IN": ["connection", "pool", "cluster", "instance"]}, "OP": "?"}]
        ]
        
        for pattern in component_patterns:
            self.matcher.add("JAEGIS_COMPONENT", [pattern])
    
    def recognize_entities(self, text: str) -> NERResult:
        """Recognize JAEGIS-specific named entities in text."""
        
        import time
        start_time = time.time()
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        entities = []
        
        # Extract standard spaCy entities
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "TECH", "PERSON"]:
                # Check if it's a JAEGIS-related entity
                jaegis_entity = self._classify_jaegis_entity(ent.text, ent.label_)
                if jaegis_entity:
                    entities.append(jaegis_entity)
        
        # Extract JAEGIS-specific entities using phrase matcher
        matches = self.phrase_matcher(doc)
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            
            jaegis_entity = self._create_jaegis_entity(
                text=span.text,
                label=label,
                start=span.start_char,
                end=span.end_char,
                context=self._extract_context(doc, start, end)
            )
            
            if jaegis_entity:
                entities.append(jaegis_entity)
        
        # Extract entities using pattern matcher
        pattern_matches = self.matcher(doc)
        for match_id, start, end in pattern_matches:
            label = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            
            jaegis_entity = self._create_jaegis_entity(
                text=span.text,
                label=label,
                start=span.start_char,
                end=span.end_char,
                context=self._extract_context(doc, start, end)
            )
            
            if jaegis_entity:
                entities.append(jaegis_entity)
        
        # Remove duplicates and overlapping entities
        entities = self._remove_overlapping_entities(entities)
        
        # Extract relationships between entities
        relationships = self._extract_entity_relationships(entities, doc)
        
        # Calculate metrics
        processing_time = (time.time() - start_time) * 1000
        confidence_score = self._calculate_overall_confidence(entities)
        entity_count_by_type = self._count_entities_by_type(entities)
        
        return NERResult(
            entities=entities,
            processing_time_ms=processing_time,
            confidence_score=confidence_score,
            entity_count_by_type=entity_count_by_type,
            relationships=relationships
        )
    
    def _classify_jaegis_entity(self, text: str, spacy_label: str) -> Optional[JAEGISEntity]:
        """Classify if a spaCy entity is JAEGIS-related."""
        
        text_lower = text.lower()
        
        # Check against JAEGIS entities
        for category, entities in self.jaegis_entities.items():
            if category == "squads":
                for squad, info in entities.items():
                    if text_lower in info["aliases"]:
                        return JAEGISEntity(
                            text=text,
                            label=JAEGISEntityType.SQUAD,
                            start=0, end=len(text),
                            confidence=0.9,
                            context="",
                            attributes={"canonical": info["canonical"], "agents": info["agents"]},
                            canonical_form=info["canonical"]
                        )
            
            elif category == "agents":
                if text.upper() in entities:
                    agent_info = entities[text.upper()]
                    return JAEGISEntity(
                        text=text,
                        label=JAEGISEntityType.AGENT,
                        start=0, end=len(text),
                        confidence=0.95,
                        context="",
                        attributes=agent_info,
                        canonical_form=text.upper()
                    )
        
        # Check against technology entities
        for tech_type, tech_list in self.tech_entities.items():
            if text_lower in tech_list:
                entity_type = getattr(JAEGISEntityType, tech_type.upper(), JAEGISEntityType.TECHNOLOGY)
                return JAEGISEntity(
                    text=text,
                    label=entity_type,
                    start=0, end=len(text),
                    confidence=0.8,
                    context="",
                    attributes={"category": tech_type},
                    canonical_form=text_lower
                )
        
        return None
    
    def _create_jaegis_entity(self, text: str, label: str, start: int, end: int, context: str) -> Optional[JAEGISEntity]:
        """Create a JAEGIS entity from matched text."""
        
        try:
            entity_type = JAEGISEntityType(label)
        except ValueError:
            # Map non-JAEGIS labels to JAEGIS types
            label_mapping = {
                "PROGRAMMING_LANGUAGES": JAEGISEntityType.PROGRAMMING_LANGUAGE,
                "FRAMEWORKS": JAEGISEntityType.FRAMEWORK,
                "DATABASES": JAEGISEntityType.DATABASE,
                "CLOUD_PLATFORMS": JAEGISEntityType.CLOUD_PLATFORM,
                "TECHNOLOGIES": JAEGISEntityType.TECHNOLOGY,
                "SECURITY_CONCEPTS": JAEGISEntityType.SECURITY_CONCEPT,
                "ARCHITECTURE_PATTERNS": JAEGISEntityType.ARCHITECTURE_PATTERN
            }
            entity_type = label_mapping.get(label, JAEGISEntityType.TECHNOLOGY)
        
        # Determine confidence based on entity type and context
        confidence = self._calculate_entity_confidence(text, entity_type, context)
        
        # Extract attributes
        attributes = self._extract_entity_attributes(text, entity_type)
        
        # Determine canonical form
        canonical_form = self._get_canonical_form(text, entity_type)
        
        return JAEGISEntity(
            text=text,
            label=entity_type,
            start=start,
            end=end,
            confidence=confidence,
            context=context,
            attributes=attributes,
            canonical_form=canonical_form
        )
    
    def _extract_context(self, doc, start: int, end: int, window: int = 3) -> str:
        """Extract context around an entity."""
        
        context_start = max(0, start - window)
        context_end = min(len(doc), end + window)
        
        context_tokens = []
        for i in range(context_start, context_end):
            if i < start or i >= end:
                context_tokens.append(doc[i].text)
            else:
                context_tokens.append(f"[{doc[i].text}]")
        
        return " ".join(context_tokens)
    
    def _calculate_entity_confidence(self, text: str, entity_type: JAEGISEntityType, context: str) -> float:
        """Calculate confidence score for an entity."""
        
        base_confidence = 0.7
        
        # Boost confidence for exact matches
        if entity_type == JAEGISEntityType.AGENT:
            if text.upper() in self.jaegis_entities["agents"]:
                base_confidence = 0.95
        
        elif entity_type == JAEGISEntityType.COMMAND:
            if text.upper() in self.jaegis_entities["commands"]:
                base_confidence = 0.9
        
        elif entity_type == JAEGISEntityType.SQUAD:
            for squad, info in self.jaegis_entities["squads"].items():
                if text.lower() in info["aliases"]:
                    base_confidence = 0.85
                    break
        
        # Adjust based on context
        context_lower = context.lower()
        
        # Boost if in technical context
        technical_indicators = ["system", "application", "service", "api", "database"]
        if any(indicator in context_lower for indicator in technical_indicators):
            base_confidence += 0.1
        
        # Boost if in command context
        command_indicators = ["create", "build", "implement", "deploy", "analyze"]
        if any(indicator in context_lower for indicator in command_indicators):
            base_confidence += 0.05
        
        return min(1.0, base_confidence)
    
    def _extract_entity_attributes(self, text: str, entity_type: JAEGISEntityType) -> Dict[str, Any]:
        """Extract attributes for an entity."""
        
        attributes = {}
        
        if entity_type == JAEGISEntityType.SQUAD:
            for squad, info in self.jaegis_entities["squads"].items():
                if text.lower() in info["aliases"]:
                    attributes.update(info)
                    break
        
        elif entity_type == JAEGISEntityType.AGENT:
            agent_info = self.jaegis_entities["agents"].get(text.upper(), {})
            attributes.update(agent_info)
        
        elif entity_type == JAEGISEntityType.COMMAND:
            command_info = self.jaegis_entities["commands"].get(text.upper(), {})
            attributes.update(command_info)
        
        elif entity_type == JAEGISEntityType.MODE:
            # Extract mode number
            mode_match = re.search(r'(\d+)', text)
            if mode_match:
                mode_num = mode_match.group(1)
                mode_info = self.jaegis_entities["modes"].get(mode_num, {})
                attributes.update(mode_info)
                attributes["mode_number"] = int(mode_num)
        
        return attributes
    
    def _get_canonical_form(self, text: str, entity_type: JAEGISEntityType) -> Optional[str]:
        """Get canonical form of an entity."""
        
        if entity_type == JAEGISEntityType.SQUAD:
            for squad, info in self.jaegis_entities["squads"].items():
                if text.lower() in info["aliases"]:
                    return info["canonical"]
        
        elif entity_type == JAEGISEntityType.AGENT:
            return text.upper()
        
        elif entity_type == JAEGISEntityType.COMMAND:
            return text.upper()
        
        elif entity_type in [JAEGISEntityType.PROGRAMMING_LANGUAGE, JAEGISEntityType.FRAMEWORK,
                           JAEGISEntityType.DATABASE, JAEGISEntityType.TECHNOLOGY]:
            return text.lower()
        
        return text
    
    def _remove_overlapping_entities(self, entities: List[JAEGISEntity]) -> List[JAEGISEntity]:
        """Remove overlapping entities, keeping the highest confidence ones."""
        
        # Sort by start position
        entities.sort(key=lambda e: e.start)
        
        filtered_entities = []
        
        for entity in entities:
            # Check for overlap with existing entities
            overlaps = False
            for existing in filtered_entities:
                if (entity.start < existing.end and entity.end > existing.start):
                    # Overlapping entities - keep the one with higher confidence
                    if entity.confidence > existing.confidence:
                        filtered_entities.remove(existing)
                    else:
                        overlaps = True
                        break
            
            if not overlaps:
                filtered_entities.append(entity)
        
        return filtered_entities
    
    def _extract_entity_relationships(self, entities: List[JAEGISEntity], doc) -> List[Dict[str, Any]]:
        """Extract relationships between entities."""
        
        relationships = []
        
        # Find command-squad relationships
        commands = [e for e in entities if e.label == JAEGISEntityType.COMMAND]
        squads = [e for e in entities if e.label == JAEGISEntityType.SQUAD]
        
        for command in commands:
            command_info = self.jaegis_entities["commands"].get(command.canonical_form, {})
            expected_squad = command_info.get("squad")
            
            if expected_squad:
                for squad in squads:
                    if squad.canonical_form == expected_squad:
                        relationships.append({
                            "type": "command_squad_match",
                            "source": command.text,
                            "target": squad.text,
                            "confidence": 0.9
                        })
        
        # Find agent-squad relationships
        agents = [e for e in entities if e.label == JAEGISEntityType.AGENT]
        
        for agent in agents:
            agent_info = self.jaegis_entities["agents"].get(agent.canonical_form, {})
            for squad in squads:
                squad_info = self.jaegis_entities["squads"].get(squad.canonical_form, {})
                if agent.canonical_form in squad_info.get("agents", []):
                    relationships.append({
                        "type": "agent_squad_membership",
                        "source": agent.text,
                        "target": squad.text,
                        "confidence": 0.95
                    })
        
        return relationships
    
    def _calculate_overall_confidence(self, entities: List[JAEGISEntity]) -> float:
        """Calculate overall confidence score."""
        
        if not entities:
            return 0.0
        
        return sum(e.confidence for e in entities) / len(entities)
    
    def _count_entities_by_type(self, entities: List[JAEGISEntity]) -> Dict[str, int]:
        """Count entities by type."""
        
        counts = {}
        for entity in entities:
            label = entity.label.value
            counts[label] = counts.get(label, 0) + 1
        
        return counts


# Example usage
if __name__ == "__main__":
    # Initialize NER
    ner = JAEGISNamedEntityRecognizer()
    
    # Test text
    test_text = """
    I need FRED to implement a Python Flask API with PostgreSQL database.
    The security squad should audit the authentication system using JWT tokens.
    Deploy this to AWS using Docker containers in mode 3.
    """
    
    # Recognize entities
    result = ner.recognize_entities(test_text)
    
    print(f"Found {len(result.entities)} entities:")
    print(f"Overall confidence: {result.confidence_score:.3f}")
    print(f"Processing time: {result.processing_time_ms:.2f}ms")
    
    for entity in result.entities:
        print(f"  - {entity.text} ({entity.label.value}) - confidence: {entity.confidence:.2f}")
        if entity.canonical_form:
            print(f"    Canonical: {entity.canonical_form}")
        if entity.attributes:
            print(f"    Attributes: {entity.attributes}")
    
    print(f"\nRelationships: {len(result.relationships)}")
    for rel in result.relationships:
        print(f"  - {rel['source']} -> {rel['target']} ({rel['type']})")
