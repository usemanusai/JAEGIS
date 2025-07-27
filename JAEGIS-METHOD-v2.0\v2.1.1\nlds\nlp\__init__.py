"""
N.L.D.S. NLP Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Complete NLP processing pipeline integrating all Phase 2 components:
- Advanced Tokenization
- Semantic Analysis
- Intent Recognition
- Context Extraction
- Named Entity Recognition
- Language Detection
"""

from .tokenizer import (
    AdvancedTokenizer,
    TokenizerFactory,
    Token,
    TokenType,
    TokenizationResult,
    quick_tokenize,
    extract_jaegis_entities
)

from .semantic_analyzer import (
    SemanticAnalysisEngine,
    SemanticVector,
    SemanticRelation,
    SemanticAnalysisResult,
    SemanticUtils
)

from .intent_recognizer import (
    IntentRecognitionEngine,
    IntentCategory,
    IntentConfidence,
    IntentPrediction,
    IntentRecognitionResult,
    IntentNeuralNetwork
)

from .context_extractor import (
    ContextExtractionEngine,
    ContextType,
    ContextScope,
    ContextItem,
    ConversationTurn,
    ContextExtractionResult,
    ContextUtils
)

from .ner_processor import (
    NERProcessor,
    EntityType,
    EntityMention,
    EntityRecognitionResult,
    NERUtils
)

from .language_detector import (
    LanguageDetector,
    MultiLanguageProcessor,
    SupportedLanguage,
    LanguageFamily,
    LanguageDetectionResult,
    MultiLanguageProcessingResult,
    LanguageUtils
)

# Version information
__version__ = "2.2.0"
__author__ = "JAEGIS Development Team"
__description__ = "N.L.D.S. Natural Language Processing Module"

# Export all components
__all__ = [
    # Tokenization
    "AdvancedTokenizer",
    "TokenizerFactory", 
    "Token",
    "TokenType",
    "TokenizationResult",
    "quick_tokenize",
    "extract_jaegis_entities",
    
    # Semantic Analysis
    "SemanticAnalysisEngine",
    "SemanticVector",
    "SemanticRelation", 
    "SemanticAnalysisResult",
    "SemanticUtils",
    
    # Intent Recognition
    "IntentRecognitionEngine",
    "IntentCategory",
    "IntentConfidence",
    "IntentPrediction",
    "IntentRecognitionResult",
    "IntentNeuralNetwork",
    
    # Context Extraction
    "ContextExtractionEngine",
    "ContextType",
    "ContextScope",
    "ContextItem",
    "ConversationTurn",
    "ContextExtractionResult",
    "ContextUtils",
    
    # Named Entity Recognition
    "NERProcessor",
    "EntityType",
    "EntityMention",
    "EntityRecognitionResult",
    "NERUtils",
    
    # Language Detection
    "LanguageDetector",
    "MultiLanguageProcessor",
    "SupportedLanguage",
    "LanguageFamily",
    "LanguageDetectionResult",
    "MultiLanguageProcessingResult",
    "LanguageUtils"
]
