"""
N.L.D.S. Advanced Tokenizer Implementation
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced tokenization with Unicode support, multi-language handling,
and JAEGIS-specific preprocessing pipeline.
"""

import re
import unicodedata
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import spacy
from spacy.lang.en import English
from spacy.lang.xx import MultiLanguage
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import logging

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION AND ENUMS
# ============================================================================

class TokenType(Enum):
    """Token type enumeration."""
    WORD = "word"
    PUNCTUATION = "punctuation"
    NUMBER = "number"
    EMAIL = "email"
    URL = "url"
    JAEGIS_COMMAND = "jaegis_command"
    JAEGIS_ENTITY = "jaegis_entity"
    SPECIAL = "special"
    WHITESPACE = "whitespace"


class LanguageCode(Enum):
    """Supported language codes."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    MULTILINGUAL = "xx"


@dataclass
class Token:
    """Token data structure."""
    text: str
    token_type: TokenType
    start_pos: int
    end_pos: int
    normalized: str
    language: Optional[str] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TokenizationResult:
    """Tokenization result container."""
    tokens: List[Token]
    original_text: str
    language: str
    processing_time_ms: float
    token_count: int
    character_count: int
    metadata: Dict[str, Any]


# ============================================================================
# ADVANCED TOKENIZER CLASS
# ============================================================================

class AdvancedTokenizer:
    """
    Advanced tokenizer with Unicode support and multi-language handling.
    
    Features:
    - Unicode normalization and support
    - Multi-language tokenization
    - JAEGIS-specific entity recognition
    - Command pattern detection
    - Preprocessing pipeline
    - Performance optimization
    """
    
    def __init__(self, language: str = "en", load_models: bool = True):
        """
        Initialize the advanced tokenizer.
        
        Args:
            language: Primary language code
            load_models: Whether to load spaCy models immediately
        """
        self.language = language
        self.models = {}
        self.patterns = self._compile_patterns()
        
        if load_models:
            self._load_models()
    
    def _load_models(self):
        """Load spaCy language models."""
        try:
            # Load English model
            self.models["en"] = spacy.load("en_core_web_lg")
            logger.info("Loaded English spaCy model")
            
            # Load multilingual model
            self.models["xx"] = spacy.load("xx_ent_wiki_sm")
            logger.info("Loaded multilingual spaCy model")
            
        except OSError as e:
            logger.warning(f"Could not load spaCy models: {e}")
            # Fallback to basic models
            self.models["en"] = English()
            self.models["xx"] = MultiLanguage()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for token recognition."""
        return {
            # JAEGIS command patterns
            "jaegis_command": re.compile(
                r'/(?:jaegis|mode|squad|nlds)-[\w-]+(?:\s+[\w-]+)*',
                re.IGNORECASE
            ),
            
            # JAEGIS entity patterns
            "jaegis_entity": re.compile(
                r'\b(?:development-squad|quality-squad|business-squad|'
                r'process-squad|content-squad|system-squad|'
                r'task-management-squad|agent-builder-squad|'
                r'system-coherence-squad|temporal-intelligence-squad|'
                r'iuas-squad|garas-squad|security-squad|compliance-squad|'
                r'audit-squad|backup-squad|mode-[1-5]|agent-creator-mode)\b',
                re.IGNORECASE
            ),
            
            # Email pattern
            "email": re.compile(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ),
            
            # URL pattern
            "url": re.compile(
                r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
            ),
            
            # Number patterns
            "number": re.compile(r'\b\d+(?:\.\d+)?\b'),
            
            # Punctuation
            "punctuation": re.compile(r'[^\w\s]'),
            
            # Whitespace
            "whitespace": re.compile(r'\s+')
        }
    
    def preprocess(self, text: str) -> str:
        """
        Preprocess text before tokenization.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Unicode normalization
        text = unicodedata.normalize('NFKC', text)
        
        # Remove control characters except newlines and tabs
        text = ''.join(char for char in text 
                      if unicodedata.category(char)[0] != 'C' 
                      or char in '\n\t')
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of the input text.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            # Use spaCy's language detection if available
            if "xx" in self.models:
                doc = self.models["xx"](text[:1000])  # Limit for performance
                if hasattr(doc, 'lang_'):
                    return doc.lang_, 0.9
            
            # Fallback to simple heuristics
            # Check for common English words
            english_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            words = set(text.lower().split())
            english_score = len(words.intersection(english_words)) / max(len(words), 1)
            
            if english_score > 0.1:
                return "en", min(english_score * 2, 0.9)
            else:
                return "xx", 0.5  # Unknown/multilingual
                
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return "en", 0.5  # Default to English
    
    def _create_token(self, text: str, token_type: TokenType, start: int, end: int, 
                     language: str = None, confidence: float = 1.0, 
                     metadata: Dict[str, Any] = None) -> Token:
        """Create a token with normalized text."""
        normalized = self._normalize_token(text, token_type)
        return Token(
            text=text,
            token_type=token_type,
            start_pos=start,
            end_pos=end,
            normalized=normalized,
            language=language,
            confidence=confidence,
            metadata=metadata or {}
        )
    
    def _normalize_token(self, text: str, token_type: TokenType) -> str:
        """Normalize token text based on type."""
        if token_type == TokenType.WORD:
            return text.lower()
        elif token_type == TokenType.JAEGIS_COMMAND:
            return text.lower().replace(' ', '-')
        elif token_type == TokenType.JAEGIS_ENTITY:
            return text.lower()
        elif token_type == TokenType.EMAIL:
            return text.lower()
        elif token_type == TokenType.URL:
            return text.lower()
        else:
            return text
    
    def _extract_special_tokens(self, text: str) -> List[Tuple[int, int, TokenType, Dict]]:
        """Extract special tokens (commands, entities, emails, URLs)."""
        special_tokens = []
        
        # Extract JAEGIS commands
        for match in self.patterns["jaegis_command"].finditer(text):
            special_tokens.append((
                match.start(), match.end(), TokenType.JAEGIS_COMMAND,
                {"command": match.group().strip()}
            ))
        
        # Extract JAEGIS entities
        for match in self.patterns["jaegis_entity"].finditer(text):
            special_tokens.append((
                match.start(), match.end(), TokenType.JAEGIS_ENTITY,
                {"entity": match.group().strip()}
            ))
        
        # Extract emails
        for match in self.patterns["email"].finditer(text):
            special_tokens.append((
                match.start(), match.end(), TokenType.EMAIL,
                {"email": match.group()}
            ))
        
        # Extract URLs
        for match in self.patterns["url"].finditer(text):
            special_tokens.append((
                match.start(), match.end(), TokenType.URL,
                {"url": match.group()}
            ))
        
        # Sort by start position
        special_tokens.sort(key=lambda x: x[0])
        return special_tokens
    
    def _spacy_tokenize(self, text: str, language: str) -> List[Token]:
        """Tokenize using spaCy."""
        model_key = language if language in self.models else "en"
        nlp = self.models.get(model_key)
        
        if not nlp:
            return self._fallback_tokenize(text, language)
        
        doc = nlp(text)
        tokens = []
        
        for token in doc:
            # Determine token type
            if token.is_punct:
                token_type = TokenType.PUNCTUATION
            elif token.like_num:
                token_type = TokenType.NUMBER
            elif token.like_email:
                token_type = TokenType.EMAIL
            elif token.like_url:
                token_type = TokenType.URL
            elif token.is_space:
                token_type = TokenType.WHITESPACE
            else:
                token_type = TokenType.WORD
            
            tokens.append(self._create_token(
                text=token.text,
                token_type=token_type,
                start=token.idx,
                end=token.idx + len(token.text),
                language=language,
                metadata={
                    "pos": token.pos_,
                    "lemma": token.lemma_,
                    "is_alpha": token.is_alpha,
                    "is_stop": token.is_stop
                }
            ))
        
        return tokens
    
    def _fallback_tokenize(self, text: str, language: str) -> List[Token]:
        """Fallback tokenization using NLTK."""
        try:
            words = word_tokenize(text)
            tokens = []
            current_pos = 0
            
            for word in words:
                # Find word position in text
                start_pos = text.find(word, current_pos)
                if start_pos == -1:
                    continue
                
                end_pos = start_pos + len(word)
                
                # Determine token type
                if re.match(r'^\W+$', word):
                    token_type = TokenType.PUNCTUATION
                elif re.match(r'^\d+(\.\d+)?$', word):
                    token_type = TokenType.NUMBER
                elif re.match(r'\s+', word):
                    token_type = TokenType.WHITESPACE
                else:
                    token_type = TokenType.WORD
                
                tokens.append(self._create_token(
                    text=word,
                    token_type=token_type,
                    start=start_pos,
                    end=end_pos,
                    language=language
                ))
                
                current_pos = end_pos
            
            return tokens
            
        except Exception as e:
            logger.error(f"Fallback tokenization failed: {e}")
            return []
    
    def tokenize(self, text: str, language: Optional[str] = None) -> TokenizationResult:
        """
        Tokenize input text with advanced processing.
        
        Args:
            text: Input text to tokenize
            language: Optional language override
            
        Returns:
            TokenizationResult with tokens and metadata
        """
        import time
        start_time = time.time()
        
        # Preprocess text
        original_text = text
        text = self.preprocess(text)
        
        if not text:
            return TokenizationResult(
                tokens=[],
                original_text=original_text,
                language="unknown",
                processing_time_ms=0,
                token_count=0,
                character_count=len(original_text),
                metadata={"empty_input": True}
            )
        
        # Detect language if not provided
        if language is None:
            language, lang_confidence = self.detect_language(text)
        else:
            lang_confidence = 1.0
        
        # Extract special tokens first
        special_tokens = self._extract_special_tokens(text)
        
        # Create mask for special token positions
        special_ranges = [(start, end) for start, end, _, _ in special_tokens]
        
        # Tokenize using spaCy
        base_tokens = self._spacy_tokenize(text, language)
        
        # Merge special tokens with base tokens
        final_tokens = []
        special_idx = 0
        
        for token in base_tokens:
            # Check if this token overlaps with a special token
            overlaps = False
            for start, end in special_ranges:
                if (token.start_pos < end and token.end_pos > start):
                    overlaps = True
                    break
            
            if not overlaps:
                final_tokens.append(token)
        
        # Add special tokens
        for start, end, token_type, metadata in special_tokens:
            special_token = self._create_token(
                text=text[start:end],
                token_type=token_type,
                start=start,
                end=end,
                language=language,
                metadata=metadata
            )
            final_tokens.append(special_token)
        
        # Sort tokens by position
        final_tokens.sort(key=lambda t: t.start_pos)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        return TokenizationResult(
            tokens=final_tokens,
            original_text=original_text,
            language=language,
            processing_time_ms=processing_time,
            token_count=len(final_tokens),
            character_count=len(original_text),
            metadata={
                "language_confidence": lang_confidence,
                "special_tokens_count": len(special_tokens),
                "preprocessing_applied": True
            }
        )
    
    def get_token_statistics(self, tokens: List[Token]) -> Dict[str, Any]:
        """Get statistics about tokenization results."""
        if not tokens:
            return {"empty": True}
        
        type_counts = {}
        for token in tokens:
            type_counts[token.token_type.value] = type_counts.get(token.token_type.value, 0) + 1
        
        return {
            "total_tokens": len(tokens),
            "type_distribution": type_counts,
            "average_token_length": sum(len(t.text) for t in tokens) / len(tokens),
            "jaegis_entities_found": type_counts.get("jaegis_entity", 0),
            "jaegis_commands_found": type_counts.get("jaegis_command", 0)
        }


# ============================================================================
# TOKENIZER FACTORY
# ============================================================================

class TokenizerFactory:
    """Factory for creating tokenizer instances."""
    
    _instances = {}
    
    @classmethod
    def get_tokenizer(cls, language: str = "en", force_reload: bool = False) -> AdvancedTokenizer:
        """
        Get or create tokenizer instance.
        
        Args:
            language: Language code
            force_reload: Force reload of models
            
        Returns:
            AdvancedTokenizer instance
        """
        if force_reload or language not in cls._instances:
            cls._instances[language] = AdvancedTokenizer(language=language)
        
        return cls._instances[language]
    
    @classmethod
    def clear_cache(cls):
        """Clear tokenizer cache."""
        cls._instances.clear()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def quick_tokenize(text: str, language: str = "en") -> List[str]:
    """
    Quick tokenization for simple use cases.
    
    Args:
        text: Input text
        language: Language code
        
    Returns:
        List of token strings
    """
    tokenizer = TokenizerFactory.get_tokenizer(language)
    result = tokenizer.tokenize(text)
    return [token.text for token in result.tokens if token.token_type != TokenType.WHITESPACE]


def extract_jaegis_entities(text: str) -> List[str]:
    """
    Extract JAEGIS entities from text.
    
    Args:
        text: Input text
        
    Returns:
        List of JAEGIS entities
    """
    tokenizer = TokenizerFactory.get_tokenizer()
    result = tokenizer.tokenize(text)
    return [token.text for token in result.tokens 
            if token.token_type in [TokenType.JAEGIS_ENTITY, TokenType.JAEGIS_COMMAND]]
