"""
N.L.D.S. Semantic Analysis Engine
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced semantic analysis using transformer models, word embeddings,
and contextual understanding for JAEGIS-specific domain knowledge.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
import logging
from datetime import datetime
import asyncio

# ML and NLP imports
import torch
import torch.nn.functional as F
from transformers import (
    AutoTokenizer, AutoModel, AutoConfig,
    BertTokenizer, BertModel,
    RobertaTokenizer, RobertaModel
)
from sentence_transformers import SentenceTransformer
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import faiss

# Local imports
from .tokenizer import TokenizationResult, Token, TokenType

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class SemanticVector:
    """Semantic vector representation."""
    vector: np.ndarray
    dimension: int
    model_name: str
    confidence: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SemanticRelation:
    """Semantic relationship between concepts."""
    source: str
    target: str
    relation_type: str
    strength: float
    confidence: float
    metadata: Dict[str, Any] = None


@dataclass
class SemanticAnalysisResult:
    """Complete semantic analysis result."""
    text: str
    embeddings: SemanticVector
    concepts: List[Dict[str, Any]]
    relations: List[SemanticRelation]
    semantic_similarity: Dict[str, float]
    domain_relevance: Dict[str, float]
    processing_time_ms: float
    confidence_score: float
    metadata: Dict[str, Any]


# ============================================================================
# SEMANTIC ANALYSIS ENGINE
# ============================================================================

class SemanticAnalysisEngine:
    """
    Advanced semantic analysis engine with transformer models.
    
    Features:
    - Multiple transformer model support (BERT, RoBERTa, Sentence-BERT)
    - Contextual embeddings generation
    - Semantic similarity computation
    - Concept extraction and relationship mapping
    - JAEGIS domain-specific semantic understanding
    - Caching for performance optimization
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize semantic analysis engine.
        
        Args:
            model_name: Transformer model to use
        """
        self.model_name = model_name
        self.models = {}
        self.tokenizers = {}
        self.embeddings_cache = {}
        self.jaegis_concepts = self._load_jaegis_concepts()
        self.concept_embeddings = {}
        
        # Initialize models
        self._initialize_models()
        
        # Build concept embeddings
        self._build_concept_embeddings()
    
    def _initialize_models(self):
        """Initialize transformer models."""
        try:
            # Primary sentence transformer model
            self.sentence_model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded sentence transformer: {self.model_name}")
            
            # BERT model for detailed analysis
            self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.bert_model = BertModel.from_pretrained('bert-base-uncased')
            self.bert_model.eval()
            
            # RoBERTa model for robust analysis
            self.roberta_tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
            self.roberta_model = RobertaModel.from_pretrained('roberta-base')
            self.roberta_model.eval()
            
            logger.info("All transformer models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load transformer models: {e}")
            raise
    
    def _load_jaegis_concepts(self) -> Dict[str, List[str]]:
        """Load JAEGIS-specific concepts and terminology."""
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
                "agent-creator-mode", "basic-mode", "advanced-mode"
            ],
            "operations": [
                "create", "update", "delete", "analyze", "process",
                "generate", "optimize", "validate", "execute", "monitor"
            ],
            "entities": [
                "agent", "task", "project", "workflow", "pipeline",
                "configuration", "template", "resource", "data", "model"
            ],
            "qualities": [
                "efficient", "secure", "scalable", "reliable", "accurate",
                "fast", "comprehensive", "detailed", "automated", "intelligent"
            ],
            "domains": [
                "development", "testing", "deployment", "monitoring",
                "security", "compliance", "analytics", "reporting"
            ]
        }
    
    def _build_concept_embeddings(self):
        """Build embeddings for JAEGIS concepts."""
        logger.info("Building JAEGIS concept embeddings...")
        
        for category, concepts in self.jaegis_concepts.items():
            self.concept_embeddings[category] = {}
            
            for concept in concepts:
                try:
                    embedding = self.sentence_model.encode(concept)
                    self.concept_embeddings[category][concept] = embedding
                except Exception as e:
                    logger.warning(f"Failed to create embedding for {concept}: {e}")
        
        logger.info("JAEGIS concept embeddings built successfully")
    
    def get_sentence_embedding(self, text: str, model_type: str = "sentence_transformer") -> SemanticVector:
        """
        Generate sentence-level embeddings.
        
        Args:
            text: Input text
            model_type: Type of model to use
            
        Returns:
            SemanticVector with embeddings
        """
        # Check cache first
        cache_key = f"{model_type}:{hash(text)}"
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]
        
        try:
            if model_type == "sentence_transformer":
                embedding = self.sentence_model.encode(text)
                confidence = 0.95
                
            elif model_type == "bert":
                embedding = self._get_bert_embedding(text)
                confidence = 0.90
                
            elif model_type == "roberta":
                embedding = self._get_roberta_embedding(text)
                confidence = 0.92
                
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            semantic_vector = SemanticVector(
                vector=embedding,
                dimension=len(embedding),
                model_name=model_type,
                confidence=confidence,
                metadata={"text_length": len(text), "model": model_type}
            )
            
            # Cache result
            self.embeddings_cache[cache_key] = semantic_vector
            
            return semantic_vector
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            # Return zero vector as fallback
            return SemanticVector(
                vector=np.zeros(384),  # Default dimension
                dimension=384,
                model_name=model_type,
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    def _get_bert_embedding(self, text: str) -> np.ndarray:
        """Get BERT embeddings for text."""
        inputs = self.bert_tokenizer(text, return_tensors="pt", 
                                   truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
            # Use [CLS] token embedding
            embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
        
        return embedding
    
    def _get_roberta_embedding(self, text: str) -> np.ndarray:
        """Get RoBERTa embeddings for text."""
        inputs = self.roberta_tokenizer(text, return_tensors="pt",
                                      truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.roberta_model(**inputs)
            # Use <s> token embedding (equivalent to [CLS])
            embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
        
        return embedding
    
    def extract_concepts(self, text: str, tokenization_result: TokenizationResult) -> List[Dict[str, Any]]:
        """
        Extract semantic concepts from text.
        
        Args:
            text: Input text
            tokenization_result: Tokenization results
            
        Returns:
            List of extracted concepts
        """
        concepts = []
        
        # Extract concepts from tokens
        for token in tokenization_result.tokens:
            if token.token_type in [TokenType.WORD, TokenType.JAEGIS_ENTITY]:
                concept = {
                    "text": token.text,
                    "normalized": token.normalized,
                    "type": "token_concept",
                    "confidence": token.confidence,
                    "position": (token.start_pos, token.end_pos),
                    "metadata": token.metadata
                }
                concepts.append(concept)
        
        # Extract JAEGIS-specific concepts
        jaegis_concepts = self._extract_jaegis_concepts(text)
        concepts.extend(jaegis_concepts)
        
        # Extract noun phrases using spaCy
        noun_phrases = self._extract_noun_phrases(text)
        concepts.extend(noun_phrases)
        
        return concepts
    
    def _extract_jaegis_concepts(self, text: str) -> List[Dict[str, Any]]:
        """Extract JAEGIS-specific concepts."""
        concepts = []
        text_lower = text.lower()
        
        for category, concept_list in self.jaegis_concepts.items():
            for concept in concept_list:
                if concept.lower() in text_lower:
                    # Calculate semantic similarity
                    text_embedding = self.get_sentence_embedding(text)
                    concept_embedding = self.concept_embeddings[category][concept]
                    
                    similarity = cosine_similarity(
                        text_embedding.vector.reshape(1, -1),
                        concept_embedding.reshape(1, -1)
                    )[0][0]
                    
                    concepts.append({
                        "text": concept,
                        "category": category,
                        "type": "jaegis_concept",
                        "confidence": float(similarity),
                        "semantic_similarity": float(similarity),
                        "metadata": {"domain": "jaegis", "category": category}
                    })
        
        return concepts
    
    def _extract_noun_phrases(self, text: str) -> List[Dict[str, Any]]:
        """Extract noun phrases using spaCy."""
        try:
            import spacy
            nlp = spacy.load("en_core_web_lg")
            doc = nlp(text)
            
            concepts = []
            for chunk in doc.noun_chunks:
                if len(chunk.text.strip()) > 2:  # Filter short phrases
                    concepts.append({
                        "text": chunk.text,
                        "type": "noun_phrase",
                        "confidence": 0.8,
                        "position": (chunk.start_char, chunk.end_char),
                        "metadata": {
                            "root": chunk.root.text,
                            "pos": chunk.root.pos_
                        }
                    })
            
            return concepts
            
        except Exception as e:
            logger.warning(f"Failed to extract noun phrases: {e}")
            return []
    
    def compute_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        try:
            embedding1 = self.get_sentence_embedding(text1)
            embedding2 = self.get_sentence_embedding(text2)
            
            similarity = cosine_similarity(
                embedding1.vector.reshape(1, -1),
                embedding2.vector.reshape(1, -1)
            )[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to compute similarity: {e}")
            return 0.0
    
    def analyze_domain_relevance(self, text: str) -> Dict[str, float]:
        """
        Analyze relevance to different JAEGIS domains.
        
        Args:
            text: Input text
            
        Returns:
            Domain relevance scores
        """
        text_embedding = self.get_sentence_embedding(text)
        domain_scores = {}
        
        for domain in self.jaegis_concepts["domains"]:
            domain_embedding = self.concept_embeddings["domains"][domain]
            
            similarity = cosine_similarity(
                text_embedding.vector.reshape(1, -1),
                domain_embedding.reshape(1, -1)
            )[0][0]
            
            domain_scores[domain] = float(similarity)
        
        return domain_scores
    
    def find_semantic_relations(self, concepts: List[Dict[str, Any]]) -> List[SemanticRelation]:
        """
        Find semantic relationships between concepts.
        
        Args:
            concepts: List of extracted concepts
            
        Returns:
            List of semantic relations
        """
        relations = []
        
        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts[i+1:], i+1):
                try:
                    # Compute semantic similarity
                    similarity = self.compute_semantic_similarity(
                        concept1["text"], concept2["text"]
                    )
                    
                    if similarity > 0.7:  # High similarity threshold
                        relation_type = "similar"
                    elif similarity > 0.5:  # Medium similarity
                        relation_type = "related"
                    else:
                        continue  # Skip low similarity
                    
                    relation = SemanticRelation(
                        source=concept1["text"],
                        target=concept2["text"],
                        relation_type=relation_type,
                        strength=similarity,
                        confidence=min(concept1["confidence"], concept2["confidence"]),
                        metadata={
                            "source_type": concept1["type"],
                            "target_type": concept2["type"]
                        }
                    )
                    
                    relations.append(relation)
                    
                except Exception as e:
                    logger.warning(f"Failed to compute relation: {e}")
                    continue
        
        return relations
    
    async def analyze(self, text: str, tokenization_result: TokenizationResult) -> SemanticAnalysisResult:
        """
        Perform complete semantic analysis.
        
        Args:
            text: Input text
            tokenization_result: Tokenization results
            
        Returns:
            Complete semantic analysis result
        """
        import time
        start_time = time.time()
        
        try:
            # Generate embeddings
            embeddings = self.get_sentence_embedding(text)
            
            # Extract concepts
            concepts = self.extract_concepts(text, tokenization_result)
            
            # Find semantic relations
            relations = self.find_semantic_relations(concepts)
            
            # Compute domain relevance
            domain_relevance = self.analyze_domain_relevance(text)
            
            # Compute semantic similarity with JAEGIS concepts
            semantic_similarity = {}
            for category, concept_list in self.jaegis_concepts.items():
                category_scores = {}
                for concept in concept_list[:5]:  # Limit for performance
                    score = self.compute_semantic_similarity(text, concept)
                    category_scores[concept] = score
                semantic_similarity[category] = category_scores
            
            # Calculate overall confidence
            confidence_score = min(
                embeddings.confidence,
                np.mean([c["confidence"] for c in concepts]) if concepts else 0.5,
                0.95
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return SemanticAnalysisResult(
                text=text,
                embeddings=embeddings,
                concepts=concepts,
                relations=relations,
                semantic_similarity=semantic_similarity,
                domain_relevance=domain_relevance,
                processing_time_ms=processing_time,
                confidence_score=confidence_score,
                metadata={
                    "model_name": self.model_name,
                    "concepts_count": len(concepts),
                    "relations_count": len(relations),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Semantic analysis failed: {e}")
            
            # Return minimal result on error
            return SemanticAnalysisResult(
                text=text,
                embeddings=SemanticVector(
                    vector=np.zeros(384),
                    dimension=384,
                    model_name="error",
                    confidence=0.0
                ),
                concepts=[],
                relations=[],
                semantic_similarity={},
                domain_relevance={},
                processing_time_ms=(time.time() - start_time) * 1000,
                confidence_score=0.0,
                metadata={"error": str(e)}
            )


# ============================================================================
# SEMANTIC UTILITIES
# ============================================================================

class SemanticUtils:
    """Utility functions for semantic analysis."""
    
    @staticmethod
    def merge_similar_concepts(concepts: List[Dict[str, Any]], 
                             threshold: float = 0.8) -> List[Dict[str, Any]]:
        """Merge semantically similar concepts."""
        if not concepts:
            return concepts
        
        merged = []
        used_indices = set()
        
        for i, concept1 in enumerate(concepts):
            if i in used_indices:
                continue
            
            similar_concepts = [concept1]
            used_indices.add(i)
            
            for j, concept2 in enumerate(concepts[i+1:], i+1):
                if j in used_indices:
                    continue
                
                # Simple text similarity check
                if concept1["text"].lower() in concept2["text"].lower() or \
                   concept2["text"].lower() in concept1["text"].lower():
                    similar_concepts.append(concept2)
                    used_indices.add(j)
            
            # Create merged concept
            if len(similar_concepts) > 1:
                merged_concept = {
                    "text": max(similar_concepts, key=lambda x: len(x["text"]))["text"],
                    "type": "merged_concept",
                    "confidence": np.mean([c["confidence"] for c in similar_concepts]),
                    "variants": [c["text"] for c in similar_concepts],
                    "metadata": {"merged_count": len(similar_concepts)}
                }
                merged.append(merged_concept)
            else:
                merged.append(concept1)
        
        return merged
    
    @staticmethod
    def filter_concepts_by_confidence(concepts: List[Dict[str, Any]], 
                                    min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """Filter concepts by confidence threshold."""
        return [c for c in concepts if c.get("confidence", 0) >= min_confidence]
    
    @staticmethod
    def rank_concepts_by_relevance(concepts: List[Dict[str, Any]], 
                                 domain_weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """Rank concepts by relevance to JAEGIS domain."""
        if domain_weights is None:
            domain_weights = {"jaegis_concept": 1.0, "noun_phrase": 0.7, "token_concept": 0.5}
        
        for concept in concepts:
            concept_type = concept.get("type", "unknown")
            weight = domain_weights.get(concept_type, 0.3)
            concept["relevance_score"] = concept.get("confidence", 0) * weight
        
        return sorted(concepts, key=lambda x: x.get("relevance_score", 0), reverse=True)
