"""
N.L.D.S. Semantic Analysis Engine
Advanced semantic analysis using transformer models, word embeddings, and contextual understanding
"""

import numpy as np
import torch
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
from transformers import (
    AutoModel, AutoTokenizer, AutoConfig,
    BertModel, BertTokenizer,
    RobertaModel, RobertaTokenizer,
    pipeline
)
from sentence_transformers import SentenceTransformer
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import networkx as nx
from collections import defaultdict
import time

logger = logging.getLogger(__name__)


@dataclass
class SemanticVector:
    """Semantic vector representation."""
    vector: List[float]
    dimension: int
    model_name: str
    confidence: float
    processing_time_ms: float


@dataclass
class SemanticSimilarity:
    """Semantic similarity result."""
    similarity_score: float
    distance_metric: str
    comparison_type: str
    confidence: float


@dataclass
class ConceptExtraction:
    """Extracted concept information."""
    concept: str
    importance_score: float
    semantic_category: str
    related_concepts: List[str]
    context_window: str


@dataclass
class SemanticAnalysisResult:
    """Comprehensive semantic analysis result."""
    input_text: str
    semantic_vector: SemanticVector
    key_concepts: List[ConceptExtraction]
    semantic_clusters: List[Dict[str, Any]]
    contextual_embeddings: Dict[str, List[float]]
    semantic_graph: Dict[str, List[str]]
    complexity_score: float
    coherence_score: float
    processing_time_ms: float
    model_metadata: Dict[str, Any]


class SemanticAnalysisEngine:
    """
    Advanced semantic analysis engine using transformer models,
    word embeddings, and contextual understanding for N.L.D.S.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        
        # Initialize sentence transformer for semantic embeddings
        self.sentence_transformer = SentenceTransformer(model_name)
        
        # Initialize BERT for contextual analysis
        self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = BertModel.from_pretrained('bert-base-uncased')
        
        # Initialize RoBERTa for enhanced understanding
        self.roberta_tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        self.roberta_model = RobertaModel.from_pretrained('roberta-base')
        
        # Initialize spaCy for linguistic analysis
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            logger.warning("spaCy large model not found, using medium model")
            try:
                self.nlp = spacy.load("en_core_web_md")
            except OSError:
                logger.warning("spaCy medium model not found, using small model")
                self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize semantic analysis pipeline
        self.sentiment_pipeline = pipeline("sentiment-analysis", 
                                          model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        
        # Semantic categories for concept classification
        self.semantic_categories = {
            "action": ["do", "make", "create", "build", "implement", "execute", "run", "perform"],
            "object": ["system", "component", "module", "service", "application", "tool"],
            "quality": ["secure", "fast", "reliable", "efficient", "scalable", "robust"],
            "technology": ["api", "database", "server", "cloud", "ai", "ml", "algorithm"],
            "process": ["analyze", "process", "validate", "test", "deploy", "monitor"],
            "data": ["information", "data", "content", "message", "input", "output"]
        }
        
        logger.info(f"Semantic Analysis Engine initialized with model: {model_name}")
    
    def extract_semantic_vector(self, text: str, model_type: str = "sentence_transformer") -> SemanticVector:
        """Extract semantic vector representation of text."""
        start_time = time.time()
        
        try:
            if model_type == "sentence_transformer":
                # Use sentence transformer for high-quality embeddings
                embedding = self.sentence_transformer.encode(text, convert_to_tensor=False)
                vector = embedding.tolist()
                confidence = 0.95  # High confidence for sentence transformers
                
            elif model_type == "bert":
                # Use BERT for contextual embeddings
                inputs = self.bert_tokenizer(text, return_tensors="pt", 
                                           padding=True, truncation=True, max_length=512)
                
                with torch.no_grad():
                    outputs = self.bert_model(**inputs)
                    # Use [CLS] token embedding as sentence representation
                    vector = outputs.last_hidden_state[0][0].numpy().tolist()
                    confidence = 0.90
                    
            elif model_type == "roberta":
                # Use RoBERTa for enhanced understanding
                inputs = self.roberta_tokenizer(text, return_tensors="pt",
                                              padding=True, truncation=True, max_length=512)
                
                with torch.no_grad():
                    outputs = self.roberta_model(**inputs)
                    # Use first token embedding as sentence representation
                    vector = outputs.last_hidden_state[0][0].numpy().tolist()
                    confidence = 0.92
                    
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            processing_time = (time.time() - start_time) * 1000
            
            return SemanticVector(
                vector=vector,
                dimension=len(vector),
                model_name=f"{model_type}_{self.model_name}",
                confidence=confidence,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logger.error(f"Semantic vector extraction failed: {e}")
            # Return zero vector as fallback
            return SemanticVector(
                vector=[0.0] * 384,  # Default dimension
                dimension=384,
                model_name=f"fallback_{model_type}",
                confidence=0.0,
                processing_time_ms=(time.time() - start_time) * 1000
            )
    
    def calculate_semantic_similarity(self, text1: str, text2: str, 
                                    method: str = "cosine") -> SemanticSimilarity:
        """Calculate semantic similarity between two texts."""
        
        # Extract vectors for both texts
        vector1 = self.extract_semantic_vector(text1)
        vector2 = self.extract_semantic_vector(text2)
        
        # Calculate similarity based on method
        if method == "cosine":
            similarity = cosine_similarity(
                [vector1.vector], [vector2.vector]
            )[0][0]
        elif method == "euclidean":
            # Convert to numpy arrays
            v1 = np.array(vector1.vector)
            v2 = np.array(vector2.vector)
            # Calculate normalized euclidean distance (convert to similarity)
            distance = np.linalg.norm(v1 - v2)
            similarity = 1 / (1 + distance)  # Convert distance to similarity
        else:
            raise ValueError(f"Unsupported similarity method: {method}")
        
        # Calculate confidence based on vector confidences
        confidence = min(vector1.confidence, vector2.confidence)
        
        return SemanticSimilarity(
            similarity_score=float(similarity),
            distance_metric=method,
            comparison_type="text_to_text",
            confidence=confidence
        )
    
    def extract_key_concepts(self, text: str, max_concepts: int = 10) -> List[ConceptExtraction]:
        """Extract key concepts from text using multiple techniques."""
        
        # Process with spaCy
        doc = self.nlp(text)
        
        concepts = []
        
        # Extract named entities
        for ent in doc.ents:
            concept = ConceptExtraction(
                concept=ent.text,
                importance_score=0.8,  # High importance for named entities
                semantic_category=ent.label_,
                related_concepts=[],
                context_window=ent.sent.text if ent.sent else text[:100]
            )
            concepts.append(concept)
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:  # Multi-word phrases
                concept = ConceptExtraction(
                    concept=chunk.text,
                    importance_score=0.6,
                    semantic_category="noun_phrase",
                    related_concepts=[],
                    context_window=chunk.sent.text if chunk.sent else text[:100]
                )
                concepts.append(concept)
        
        # Extract important single words
        for token in doc:
            if (token.pos_ in ['NOUN', 'VERB', 'ADJ'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                
                # Classify semantic category
                semantic_category = self._classify_semantic_category(token.text.lower())
                
                concept = ConceptExtraction(
                    concept=token.text,
                    importance_score=0.4,
                    semantic_category=semantic_category,
                    related_concepts=[],
                    context_window=token.sent.text if token.sent else text[:100]
                )
                concepts.append(concept)
        
        # Remove duplicates and sort by importance
        unique_concepts = {}
        for concept in concepts:
            key = concept.concept.lower()
            if key not in unique_concepts or concept.importance_score > unique_concepts[key].importance_score:
                unique_concepts[key] = concept
        
        # Sort by importance and return top concepts
        sorted_concepts = sorted(unique_concepts.values(), 
                               key=lambda x: x.importance_score, reverse=True)
        
        return sorted_concepts[:max_concepts]
    
    def _classify_semantic_category(self, word: str) -> str:
        """Classify word into semantic category."""
        for category, keywords in self.semantic_categories.items():
            if word in keywords:
                return category
        return "general"
    
    def create_semantic_clusters(self, texts: List[str], n_clusters: int = 5) -> List[Dict[str, Any]]:
        """Create semantic clusters from multiple texts."""
        
        if len(texts) < n_clusters:
            n_clusters = len(texts)
        
        # Extract vectors for all texts
        vectors = []
        for text in texts:
            vector = self.extract_semantic_vector(text)
            vectors.append(vector.vector)
        
        # Perform clustering
        vectors_array = np.array(vectors)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(vectors_array)
        
        # Organize results by cluster
        clusters = []
        for i in range(n_clusters):
            cluster_texts = [texts[j] for j in range(len(texts)) if cluster_labels[j] == i]
            cluster_center = kmeans.cluster_centers_[i].tolist()
            
            # Calculate intra-cluster similarity
            if len(cluster_texts) > 1:
                cluster_vectors = [vectors[j] for j in range(len(texts)) if cluster_labels[j] == i]
                similarities = []
                for k in range(len(cluster_vectors)):
                    for l in range(k + 1, len(cluster_vectors)):
                        sim = cosine_similarity([cluster_vectors[k]], [cluster_vectors[l]])[0][0]
                        similarities.append(sim)
                avg_similarity = np.mean(similarities) if similarities else 1.0
            else:
                avg_similarity = 1.0
            
            cluster = {
                "cluster_id": i,
                "texts": cluster_texts,
                "center_vector": cluster_center,
                "size": len(cluster_texts),
                "avg_intra_similarity": float(avg_similarity),
                "representative_text": cluster_texts[0] if cluster_texts else ""
            }
            clusters.append(cluster)
        
        return clusters
    
    def build_semantic_graph(self, concepts: List[ConceptExtraction], 
                           similarity_threshold: float = 0.7) -> Dict[str, List[str]]:
        """Build semantic relationship graph between concepts."""
        
        graph = defaultdict(list)
        
        # Calculate similarities between all concept pairs
        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts[i + 1:], i + 1):
                similarity = self.calculate_semantic_similarity(
                    concept1.concept, concept2.concept
                )
                
                if similarity.similarity_score >= similarity_threshold:
                    graph[concept1.concept].append(concept2.concept)
                    graph[concept2.concept].append(concept1.concept)
        
        return dict(graph)
    
    def calculate_text_complexity(self, text: str) -> float:
        """Calculate semantic complexity score of text."""
        
        doc = self.nlp(text)
        
        # Factors contributing to complexity
        factors = {
            "sentence_length": len(text.split()) / len(list(doc.sents)) if list(doc.sents) else 0,
            "vocabulary_diversity": len(set(token.text.lower() for token in doc if token.is_alpha)) / len([token for token in doc if token.is_alpha]) if [token for token in doc if token.is_alpha] else 0,
            "syntactic_complexity": len([token for token in doc if token.dep_ in ['nsubj', 'dobj', 'prep']]) / len(doc) if len(doc) > 0 else 0,
            "entity_density": len(doc.ents) / len(doc) if len(doc) > 0 else 0,
            "semantic_depth": len([token for token in doc if token.pos_ in ['NOUN', 'VERB', 'ADJ']]) / len(doc) if len(doc) > 0 else 0
        }
        
        # Weighted combination of factors
        weights = {
            "sentence_length": 0.2,
            "vocabulary_diversity": 0.3,
            "syntactic_complexity": 0.2,
            "entity_density": 0.15,
            "semantic_depth": 0.15
        }
        
        complexity_score = sum(factors[factor] * weights[factor] for factor in factors)
        
        # Normalize to 0-1 range
        return min(1.0, complexity_score)
    
    def calculate_coherence_score(self, text: str) -> float:
        """Calculate semantic coherence score of text."""
        
        sentences = text.split('.')
        if len(sentences) < 2:
            return 1.0  # Single sentence is perfectly coherent
        
        # Calculate inter-sentence similarities
        similarities = []
        for i in range(len(sentences) - 1):
            if sentences[i].strip() and sentences[i + 1].strip():
                similarity = self.calculate_semantic_similarity(
                    sentences[i].strip(), sentences[i + 1].strip()
                )
                similarities.append(similarity.similarity_score)
        
        # Average similarity as coherence measure
        coherence_score = np.mean(similarities) if similarities else 0.0
        
        return float(coherence_score)
    
    def analyze(self, text: str) -> SemanticAnalysisResult:
        """Perform comprehensive semantic analysis."""
        start_time = time.time()
        
        # Extract semantic vector
        semantic_vector = self.extract_semantic_vector(text)
        
        # Extract key concepts
        key_concepts = self.extract_key_concepts(text)
        
        # Create semantic clusters (for single text, create concept clusters)
        concept_texts = [concept.concept for concept in key_concepts]
        if len(concept_texts) > 1:
            semantic_clusters = self.create_semantic_clusters(concept_texts, 
                                                            min(3, len(concept_texts)))
        else:
            semantic_clusters = []
        
        # Build semantic graph
        semantic_graph = self.build_semantic_graph(key_concepts)
        
        # Calculate complexity and coherence
        complexity_score = self.calculate_text_complexity(text)
        coherence_score = self.calculate_coherence_score(text)
        
        # Create contextual embeddings for key phrases
        contextual_embeddings = {}
        for concept in key_concepts[:5]:  # Top 5 concepts
            vector = self.extract_semantic_vector(concept.concept)
            contextual_embeddings[concept.concept] = vector.vector
        
        processing_time = (time.time() - start_time) * 1000
        
        return SemanticAnalysisResult(
            input_text=text,
            semantic_vector=semantic_vector,
            key_concepts=key_concepts,
            semantic_clusters=semantic_clusters,
            contextual_embeddings=contextual_embeddings,
            semantic_graph=semantic_graph,
            complexity_score=complexity_score,
            coherence_score=coherence_score,
            processing_time_ms=processing_time,
            model_metadata={
                "sentence_transformer_model": self.model_name,
                "bert_model": "bert-base-uncased",
                "roberta_model": "roberta-base",
                "spacy_model": self.nlp.meta["name"]
            }
        )


# Example usage
if __name__ == "__main__":
    # Initialize semantic analysis engine
    engine = SemanticAnalysisEngine()
    
    # Test text
    test_text = """
    Create a secure user authentication system with JWT tokens and role-based access control.
    The system should integrate with the existing database and provide real-time monitoring capabilities.
    Implement comprehensive logging and ensure high performance with response times under 500ms.
    """
    
    # Perform analysis
    result = engine.analyze(test_text)
    
    # Print results
    print(f"Semantic Analysis Results:")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    print(f"Complexity Score: {result.complexity_score:.3f}")
    print(f"Coherence Score: {result.coherence_score:.3f}")
    print(f"Vector Dimension: {result.semantic_vector.dimension}")
    
    print(f"\nKey Concepts ({len(result.key_concepts)}):")
    for concept in result.key_concepts[:5]:
        print(f"  - {concept.concept} ({concept.semantic_category}, {concept.importance_score:.2f})")
    
    print(f"\nSemantic Clusters: {len(result.semantic_clusters)}")
    print(f"Semantic Graph Connections: {len(result.semantic_graph)}")
