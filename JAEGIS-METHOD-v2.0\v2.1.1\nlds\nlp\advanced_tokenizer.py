"""
N.L.D.S. Advanced Tokenizer Implementation
Advanced tokenization with Unicode support, multi-language handling, and preprocessing pipeline
"""

import re
import unicodedata
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import logging
import spacy
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.de import German
from spacy.lang.zh import Chinese
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import AutoTokenizer
import langdetect
import emoji

logger = logging.getLogger(__name__)


class TokenType(str, Enum):
    """Token type classification."""
    WORD = "word"
    NUMBER = "number"
    PUNCTUATION = "punctuation"
    SYMBOL = "symbol"
    EMOJI = "emoji"
    URL = "url"
    EMAIL = "email"
    HASHTAG = "hashtag"
    MENTION = "mention"
    SPECIAL = "special"
    UNKNOWN = "unknown"


class LanguageCode(str, Enum):
    """Supported language codes."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    AUTO_DETECT = "auto"


@dataclass
class Token:
    """Advanced token representation."""
    text: str
    normalized_text: str
    token_type: TokenType
    start_pos: int
    end_pos: int
    language: str
    confidence: float
    lemma: Optional[str] = None
    pos_tag: Optional[str] = None
    dependency: Optional[str] = None
    entity_type: Optional[str] = None
    is_stop_word: bool = False
    is_alpha: bool = False
    is_digit: bool = False
    is_punct: bool = False
    is_space: bool = False
    is_oov: bool = False  # Out of vocabulary
    vector: Optional[List[float]] = None


@dataclass
class TokenizationResult:
    """Tokenization result with metadata."""
    tokens: List[Token]
    sentences: List[str]
    detected_language: str
    language_confidence: float
    processing_time_ms: float
    token_count: int
    character_count: int
    preprocessing_applied: List[str]


class AdvancedTokenizer:
    """
    Advanced tokenizer with Unicode support, multi-language handling,
    and comprehensive preprocessing pipeline for N.L.D.S.
    """
    
    def __init__(self, default_language: LanguageCode = LanguageCode.ENGLISH):
        self.default_language = default_language
        
        # Initialize spaCy models
        self.spacy_models = {}
        self._load_spacy_models()
        
        # Initialize transformer tokenizer for advanced features
        self.transformer_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        
        # Preprocessing patterns
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.hashtag_pattern = re.compile(r'#\w+')
        self.mention_pattern = re.compile(r'@\w+')
        self.number_pattern = re.compile(r'\b\d+(?:\.\d+)?\b')
        
        # Unicode categories for classification
        self.punctuation_categories = {'Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps'}
        self.symbol_categories = {'Sc', 'Sk', 'Sm', 'So'}
        
        # Stop words for multiple languages
        self.stop_words = self._load_stop_words()
        
        logger.info("Advanced Tokenizer initialized")
    
    def _load_spacy_models(self):
        """Load spaCy models for supported languages."""
        model_mapping = {
            LanguageCode.ENGLISH: "en_core_web_sm",
            LanguageCode.SPANISH: "es_core_news_sm",
            LanguageCode.FRENCH: "fr_core_news_sm",
            LanguageCode.GERMAN: "de_core_news_sm",
            LanguageCode.CHINESE: "zh_core_web_sm"
        }
        
        for lang, model_name in model_mapping.items():
            try:
                self.spacy_models[lang] = spacy.load(model_name)
                logger.info(f"Loaded spaCy model for {lang.value}")
            except OSError:
                logger.warning(f"spaCy model {model_name} not found, using basic tokenizer for {lang.value}")
                # Fallback to basic language class
                if lang == LanguageCode.ENGLISH:
                    self.spacy_models[lang] = English()
                elif lang == LanguageCode.SPANISH:
                    self.spacy_models[lang] = Spanish()
                elif lang == LanguageCode.FRENCH:
                    self.spacy_models[lang] = French()
                elif lang == LanguageCode.GERMAN:
                    self.spacy_models[lang] = German()
                elif lang == LanguageCode.CHINESE:
                    self.spacy_models[lang] = Chinese()
    
    def _load_stop_words(self) -> Dict[str, Set[str]]:
        """Load stop words for supported languages."""
        stop_words = {}
        
        try:
            # Download NLTK stop words if not already present
            nltk.download('stopwords', quiet=True)
            from nltk.corpus import stopwords
            
            stop_words[LanguageCode.ENGLISH] = set(stopwords.words('english'))
            stop_words[LanguageCode.SPANISH] = set(stopwords.words('spanish'))
            stop_words[LanguageCode.FRENCH] = set(stopwords.words('french'))
            stop_words[LanguageCode.GERMAN] = set(stopwords.words('german'))
            
        except Exception as e:
            logger.warning(f"Could not load NLTK stop words: {e}")
            # Fallback to basic stop words
            stop_words[LanguageCode.ENGLISH] = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'
            }
        
        return stop_words
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """Detect language of input text."""
        try:
            detected_lang = langdetect.detect(text)
            # Get confidence (langdetect doesn't provide confidence directly)
            confidence = 0.9  # Default high confidence
            
            # Map to supported languages
            lang_mapping = {
                'en': LanguageCode.ENGLISH,
                'es': LanguageCode.SPANISH,
                'fr': LanguageCode.FRENCH,
                'de': LanguageCode.GERMAN,
                'zh': LanguageCode.CHINESE,
                'zh-cn': LanguageCode.CHINESE,
                'zh-tw': LanguageCode.CHINESE
            }
            
            mapped_lang = lang_mapping.get(detected_lang, LanguageCode.ENGLISH)
            return mapped_lang.value, confidence
            
        except Exception as e:
            logger.warning(f"Language detection failed: {e}, defaulting to English")
            return LanguageCode.ENGLISH.value, 0.5
    
    def preprocess_text(self, text: str) -> Tuple[str, List[str]]:
        """Apply preprocessing pipeline to input text."""
        applied_steps = []
        processed_text = text
        
        # 1. Unicode normalization
        processed_text = unicodedata.normalize('NFKC', processed_text)
        applied_steps.append("unicode_normalization")
        
        # 2. Remove or replace control characters
        processed_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', processed_text)
        applied_steps.append("control_character_removal")
        
        # 3. Normalize whitespace
        processed_text = re.sub(r'\s+', ' ', processed_text).strip()
        applied_steps.append("whitespace_normalization")
        
        # 4. Handle special characters and emojis (preserve them)
        # Convert emojis to text representation for better processing
        emoji_text = emoji.demojize(processed_text)
        if emoji_text != processed_text:
            processed_text = emoji_text
            applied_steps.append("emoji_conversion")
        
        return processed_text, applied_steps
    
    def classify_token_type(self, token_text: str) -> TokenType:
        """Classify token type based on content."""
        
        # Check for URLs
        if self.url_pattern.match(token_text):
            return TokenType.URL
        
        # Check for emails
        if self.email_pattern.match(token_text):
            return TokenType.EMAIL
        
        # Check for hashtags
        if self.hashtag_pattern.match(token_text):
            return TokenType.HASHTAG
        
        # Check for mentions
        if self.mention_pattern.match(token_text):
            return TokenType.MENTION
        
        # Check for numbers
        if self.number_pattern.match(token_text):
            return TokenType.NUMBER
        
        # Check for emojis
        if any(char in emoji.EMOJI_DATA for char in token_text):
            return TokenType.EMOJI
        
        # Check Unicode categories
        if len(token_text) == 1:
            category = unicodedata.category(token_text)
            if category in self.punctuation_categories:
                return TokenType.PUNCTUATION
            elif category in self.symbol_categories:
                return TokenType.SYMBOL
        
        # Check if it's a word (contains alphabetic characters)
        if any(char.isalpha() for char in token_text):
            return TokenType.WORD
        
        # Check if it's purely punctuation
        if all(char in '.,;:!?()[]{}"\'-' for char in token_text):
            return TokenType.PUNCTUATION
        
        return TokenType.UNKNOWN
    
    def tokenize(self, text: str, language: LanguageCode = LanguageCode.AUTO_DETECT) -> TokenizationResult:
        """
        Perform advanced tokenization with full preprocessing pipeline.
        
        Args:
            text: Input text to tokenize
            language: Target language (auto-detect if not specified)
            
        Returns:
            TokenizationResult with comprehensive token information
        """
        import time
        start_time = time.time()
        
        # Detect language if auto-detect is specified
        if language == LanguageCode.AUTO_DETECT:
            detected_lang, lang_confidence = self.detect_language(text)
        else:
            detected_lang = language.value
            lang_confidence = 1.0
        
        # Preprocess text
        preprocessed_text, preprocessing_steps = self.preprocess_text(text)
        
        # Get appropriate spaCy model
        lang_enum = LanguageCode(detected_lang)
        nlp = self.spacy_models.get(lang_enum, self.spacy_models[LanguageCode.ENGLISH])
        
        # Process with spaCy
        doc = nlp(preprocessed_text)
        
        # Extract sentences
        sentences = [sent.text for sent in doc.sents]
        
        # Create tokens
        tokens = []
        for spacy_token in doc:
            # Classify token type
            token_type = self.classify_token_type(spacy_token.text)
            
            # Normalize token text
            normalized_text = spacy_token.text.lower().strip()
            
            # Check if it's a stop word
            stop_words_set = self.stop_words.get(lang_enum, set())
            is_stop_word = normalized_text in stop_words_set
            
            # Create token object
            token = Token(
                text=spacy_token.text,
                normalized_text=normalized_text,
                token_type=token_type,
                start_pos=spacy_token.idx,
                end_pos=spacy_token.idx + len(spacy_token.text),
                language=detected_lang,
                confidence=lang_confidence,
                lemma=spacy_token.lemma_,
                pos_tag=spacy_token.pos_,
                dependency=spacy_token.dep_,
                entity_type=spacy_token.ent_type_ if spacy_token.ent_type_ else None,
                is_stop_word=is_stop_word,
                is_alpha=spacy_token.is_alpha,
                is_digit=spacy_token.is_digit,
                is_punct=spacy_token.is_punct,
                is_space=spacy_token.is_space,
                is_oov=spacy_token.is_oov,
                vector=spacy_token.vector.tolist() if spacy_token.has_vector else None
            )
            
            tokens.append(token)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Create result
        result = TokenizationResult(
            tokens=tokens,
            sentences=sentences,
            detected_language=detected_lang,
            language_confidence=lang_confidence,
            processing_time_ms=processing_time,
            token_count=len(tokens),
            character_count=len(text),
            preprocessing_applied=preprocessing_steps
        )
        
        logger.debug(f"Tokenized {len(tokens)} tokens in {processing_time:.2f}ms")
        
        return result
    
    def tokenize_for_transformer(self, text: str) -> Dict[str, Any]:
        """Tokenize text for transformer model compatibility."""
        
        # Use transformer tokenizer
        encoded = self.transformer_tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
            return_attention_mask=True,
            return_token_type_ids=True
        )
        
        # Decode tokens for inspection
        tokens = self.transformer_tokenizer.convert_ids_to_tokens(encoded['input_ids'][0])
        
        return {
            "input_ids": encoded['input_ids'],
            "attention_mask": encoded['attention_mask'],
            "token_type_ids": encoded.get('token_type_ids'),
            "tokens": tokens,
            "token_count": len(tokens)
        }
    
    def batch_tokenize(self, texts: List[str], language: LanguageCode = LanguageCode.AUTO_DETECT) -> List[TokenizationResult]:
        """Tokenize multiple texts in batch for efficiency."""
        
        results = []
        for text in texts:
            result = self.tokenize(text, language)
            results.append(result)
        
        return results
    
    def get_token_statistics(self, result: TokenizationResult) -> Dict[str, Any]:
        """Generate comprehensive token statistics."""
        
        token_types = {}
        pos_tags = {}
        languages = {}
        
        for token in result.tokens:
            # Count token types
            token_types[token.token_type.value] = token_types.get(token.token_type.value, 0) + 1
            
            # Count POS tags
            if token.pos_tag:
                pos_tags[token.pos_tag] = pos_tags.get(token.pos_tag, 0) + 1
            
            # Count languages
            languages[token.language] = languages.get(token.language, 0) + 1
        
        # Calculate ratios
        total_tokens = len(result.tokens)
        stop_word_ratio = sum(1 for token in result.tokens if token.is_stop_word) / total_tokens if total_tokens > 0 else 0
        oov_ratio = sum(1 for token in result.tokens if token.is_oov) / total_tokens if total_tokens > 0 else 0
        
        return {
            "total_tokens": total_tokens,
            "total_sentences": len(result.sentences),
            "total_characters": result.character_count,
            "average_tokens_per_sentence": total_tokens / len(result.sentences) if result.sentences else 0,
            "token_types": token_types,
            "pos_tags": pos_tags,
            "languages": languages,
            "stop_word_ratio": stop_word_ratio,
            "oov_ratio": oov_ratio,
            "processing_time_ms": result.processing_time_ms,
            "detected_language": result.detected_language,
            "language_confidence": result.language_confidence
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize tokenizer
    tokenizer = AdvancedTokenizer()
    
    # Test text with multiple languages and special content
    test_text = """
    Hello! This is a test 🚀 with emojis and URLs like https://example.com.
    Contact us at test@example.com or follow @username #hashtag.
    The price is $29.99 and the date is 2024-01-15.
    """
    
    # Tokenize
    result = tokenizer.tokenize(test_text)
    
    # Print results
    print(f"Detected Language: {result.detected_language}")
    print(f"Token Count: {result.token_count}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    
    print("\nTokens:")
    for token in result.tokens[:10]:  # Show first 10 tokens
        print(f"  {token.text} -> {token.token_type.value} ({token.pos_tag})")
    
    # Get statistics
    stats = tokenizer.get_token_statistics(result)
    print(f"\nStatistics: {stats}")
