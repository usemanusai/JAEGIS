"""
N.L.D.S. Language Detection & Multi-Language Support
Advanced language detection and processing with primary English focus
"""

import langdetect
import spacy
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import re
from collections import defaultdict
import time

logger = logging.getLogger(__name__)


class SupportedLanguage(str, Enum):
    """Supported languages in N.L.D.S."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    PORTUGUESE = "pt"
    ITALIAN = "it"
    RUSSIAN = "ru"
    ARABIC = "ar"


class LanguageConfidence(str, Enum):
    """Language detection confidence levels."""
    HIGH = "high"      # >90%
    MEDIUM = "medium"  # 70-90%
    LOW = "low"        # 50-70%
    VERY_LOW = "very_low"  # <50%


@dataclass
class LanguageDetectionResult:
    """Language detection result."""
    detected_language: SupportedLanguage
    confidence: float
    confidence_level: LanguageConfidence
    alternative_languages: List[Tuple[SupportedLanguage, float]]
    processing_time_ms: float
    text_length: int
    detection_method: str
    language_features: Dict[str, Any]


@dataclass
class MultiLanguageProcessingResult:
    """Multi-language processing result."""
    original_text: str
    detected_language: SupportedLanguage
    translated_text: Optional[str]
    processing_language: SupportedLanguage
    language_detection: LanguageDetectionResult
    translation_confidence: Optional[float]
    processing_notes: List[str]


class LanguageDetectionEngine:
    """
    Advanced language detection and multi-language support engine.
    
    Provides robust language detection with fallback mechanisms,
    translation capabilities, and optimized processing for English.
    """
    
    def __init__(self):
        # Initialize spaCy models for supported languages
        self.spacy_models = {}
        self._load_spacy_models()
        
        # Language detection patterns and features
        self.language_patterns = self._initialize_language_patterns()
        
        # Character frequency analysis for language detection
        self.char_frequencies = self._initialize_char_frequencies()
        
        # Common words for language identification
        self.common_words = self._initialize_common_words()
        
        # Language-specific processing configurations
        self.processing_configs = self._initialize_processing_configs()
        
        logger.info("Language Detection Engine initialized")
    
    def _load_spacy_models(self):
        """Load spaCy models for supported languages."""
        
        model_mapping = {
            SupportedLanguage.ENGLISH: ["en_core_web_lg", "en_core_web_md", "en_core_web_sm"],
            SupportedLanguage.SPANISH: ["es_core_news_lg", "es_core_news_md", "es_core_news_sm"],
            SupportedLanguage.FRENCH: ["fr_core_news_lg", "fr_core_news_md", "fr_core_news_sm"],
            SupportedLanguage.GERMAN: ["de_core_news_lg", "de_core_news_md", "de_core_news_sm"],
            SupportedLanguage.CHINESE: ["zh_core_web_lg", "zh_core_web_md", "zh_core_web_sm"]
        }
        
        for language, models in model_mapping.items():
            for model_name in models:
                try:
                    self.spacy_models[language] = spacy.load(model_name)
                    logger.info(f"Loaded spaCy model {model_name} for {language.value}")
                    break
                except OSError:
                    continue
            
            # Fallback to basic language class if no model found
            if language not in self.spacy_models:
                try:
                    if language == SupportedLanguage.ENGLISH:
                        from spacy.lang.en import English
                        self.spacy_models[language] = English()
                    elif language == SupportedLanguage.SPANISH:
                        from spacy.lang.es import Spanish
                        self.spacy_models[language] = Spanish()
                    elif language == SupportedLanguage.FRENCH:
                        from spacy.lang.fr import French
                        self.spacy_models[language] = French()
                    elif language == SupportedLanguage.GERMAN:
                        from spacy.lang.de import German
                        self.spacy_models[language] = German()
                    elif language == SupportedLanguage.CHINESE:
                        from spacy.lang.zh import Chinese
                        self.spacy_models[language] = Chinese()
                    
                    logger.warning(f"Using basic language class for {language.value}")
                except ImportError:
                    logger.warning(f"No spaCy support available for {language.value}")
    
    def _initialize_language_patterns(self) -> Dict[SupportedLanguage, Dict[str, Any]]:
        """Initialize language-specific patterns and features."""
        
        return {
            SupportedLanguage.ENGLISH: {
                "articles": ["the", "a", "an"],
                "common_endings": ["ing", "ed", "ly", "tion", "ness"],
                "pronouns": ["i", "you", "he", "she", "it", "we", "they"],
                "prepositions": ["in", "on", "at", "by", "for", "with", "to"],
                "char_patterns": [r"[a-zA-Z]", r"\bth[aeiou]", r"\b[aeiou]nd\b"]
            },
            
            SupportedLanguage.SPANISH: {
                "articles": ["el", "la", "los", "las", "un", "una"],
                "common_endings": ["ción", "dad", "mente", "ado", "ido"],
                "pronouns": ["yo", "tú", "él", "ella", "nosotros", "ellos"],
                "prepositions": ["en", "de", "a", "por", "para", "con"],
                "char_patterns": [r"ñ", r"[áéíóú]", r"\b[aeiou]r\b"]
            },
            
            SupportedLanguage.FRENCH: {
                "articles": ["le", "la", "les", "un", "une", "des"],
                "common_endings": ["tion", "ment", "eur", "euse", "ique"],
                "pronouns": ["je", "tu", "il", "elle", "nous", "vous", "ils"],
                "prepositions": ["de", "à", "dans", "pour", "avec", "sur"],
                "char_patterns": [r"[àâäéèêëïîôöùûüÿç]", r"\bqu[aeiou]", r"\b[aeiou]nt\b"]
            },
            
            SupportedLanguage.GERMAN: {
                "articles": ["der", "die", "das", "ein", "eine"],
                "common_endings": ["ung", "keit", "heit", "lich", "isch"],
                "pronouns": ["ich", "du", "er", "sie", "es", "wir", "ihr"],
                "prepositions": ["in", "an", "auf", "für", "mit", "zu"],
                "char_patterns": [r"[äöüß]", r"\bsch", r"\b[aeiou]en\b"]
            },
            
            SupportedLanguage.CHINESE: {
                "char_patterns": [r"[\u4e00-\u9fff]"],  # Chinese characters
                "common_chars": ["的", "是", "在", "有", "和", "了"],
                "punctuation": ["。", "，", "？", "！", "；", "："]
            }
        }
    
    def _initialize_char_frequencies(self) -> Dict[SupportedLanguage, Dict[str, float]]:
        """Initialize character frequency patterns for languages."""
        
        return {
            SupportedLanguage.ENGLISH: {
                'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
                's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8
            },
            SupportedLanguage.SPANISH: {
                'e': 13.7, 'a': 12.5, 'o': 8.7, 's': 8.0, 'n': 6.8, 'r': 6.9,
                'i': 6.2, 't': 4.6, 'l': 5.0, 'd': 5.9, 'u': 3.9, 'c': 4.7
            },
            SupportedLanguage.FRENCH: {
                'e': 17.3, 's': 7.9, 'a': 7.6, 'i': 7.5, 't': 7.2, 'n': 7.1,
                'r': 6.6, 'u': 6.3, 'l': 5.5, 'o': 5.4, 'd': 3.7, 'c': 3.2
            },
            SupportedLanguage.GERMAN: {
                'e': 17.4, 'n': 9.8, 'i': 7.5, 's': 7.3, 'r': 7.0, 'a': 6.5,
                't': 6.2, 'd': 5.1, 'h': 4.8, 'u': 4.4, 'l': 3.4, 'c': 3.1
            }
        }
    
    def _initialize_common_words(self) -> Dict[SupportedLanguage, List[str]]:
        """Initialize common words for each language."""
        
        return {
            SupportedLanguage.ENGLISH: [
                "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
                "it", "for", "not", "on", "with", "he", "as", "you", "do", "at"
            ],
            SupportedLanguage.SPANISH: [
                "de", "la", "que", "el", "en", "y", "a", "es", "se", "no",
                "te", "lo", "le", "da", "su", "por", "son", "con", "para", "al"
            ],
            SupportedLanguage.FRENCH: [
                "de", "le", "et", "à", "un", "il", "être", "et", "en", "avoir",
                "que", "pour", "dans", "ce", "son", "une", "sur", "avec", "ne", "se"
            ],
            SupportedLanguage.GERMAN: [
                "der", "die", "und", "in", "den", "von", "zu", "das", "mit", "sich",
                "des", "auf", "für", "ist", "im", "dem", "nicht", "ein", "eine", "als"
            ],
            SupportedLanguage.CHINESE: [
                "的", "是", "在", "了", "不", "与", "也", "上", "个", "人",
                "这", "中", "大", "为", "来", "我", "到", "出", "要", "以"
            ]
        }
    
    def _initialize_processing_configs(self) -> Dict[SupportedLanguage, Dict[str, Any]]:
        """Initialize language-specific processing configurations."""
        
        return {
            SupportedLanguage.ENGLISH: {
                "primary_language": True,
                "translation_required": False,
                "confidence_boost": 0.1,
                "processing_priority": 1,
                "special_handling": []
            },
            SupportedLanguage.SPANISH: {
                "primary_language": False,
                "translation_required": True,
                "confidence_boost": 0.0,
                "processing_priority": 2,
                "special_handling": ["accent_normalization"]
            },
            SupportedLanguage.FRENCH: {
                "primary_language": False,
                "translation_required": True,
                "confidence_boost": 0.0,
                "processing_priority": 3,
                "special_handling": ["accent_normalization"]
            },
            SupportedLanguage.GERMAN: {
                "primary_language": False,
                "translation_required": True,
                "confidence_boost": 0.0,
                "processing_priority": 4,
                "special_handling": ["compound_word_handling"]
            },
            SupportedLanguage.CHINESE: {
                "primary_language": False,
                "translation_required": True,
                "confidence_boost": 0.0,
                "processing_priority": 5,
                "special_handling": ["character_segmentation"]
            }
        }
    
    def detect_language(self, text: str) -> LanguageDetectionResult:
        """Detect language of input text using multiple methods."""
        
        start_time = time.time()
        
        # Method 1: langdetect library
        langdetect_result = self._detect_with_langdetect(text)
        
        # Method 2: Character frequency analysis
        char_freq_result = self._detect_with_char_frequency(text)
        
        # Method 3: Common words analysis
        common_words_result = self._detect_with_common_words(text)
        
        # Method 4: Pattern matching
        pattern_result = self._detect_with_patterns(text)
        
        # Combine results using weighted voting
        combined_result = self._combine_detection_results([
            ("langdetect", langdetect_result, 0.4),
            ("char_frequency", char_freq_result, 0.2),
            ("common_words", common_words_result, 0.3),
            ("patterns", pattern_result, 0.1)
        ])
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(combined_result["confidence"])
        
        # Extract language features
        language_features = self._extract_language_features(text, combined_result["language"])
        
        processing_time = (time.time() - start_time) * 1000
        
        return LanguageDetectionResult(
            detected_language=combined_result["language"],
            confidence=combined_result["confidence"],
            confidence_level=confidence_level,
            alternative_languages=combined_result["alternatives"],
            processing_time_ms=processing_time,
            text_length=len(text),
            detection_method="ensemble",
            language_features=language_features
        )
    
    def _detect_with_langdetect(self, text: str) -> Dict[str, Any]:
        """Detect language using langdetect library."""
        
        try:
            # Get language probabilities
            lang_probs = langdetect.detect_langs(text)
            
            # Convert to our supported languages
            results = []
            for lang_prob in lang_probs:
                try:
                    supported_lang = SupportedLanguage(lang_prob.lang)
                    results.append((supported_lang, lang_prob.prob))
                except ValueError:
                    # Language not supported
                    continue
            
            if results:
                # Sort by probability
                results.sort(key=lambda x: x[1], reverse=True)
                
                return {
                    "language": results[0][0],
                    "confidence": results[0][1],
                    "alternatives": results[1:3]  # Top 2 alternatives
                }
            
        except Exception as e:
            logger.warning(f"langdetect failed: {e}")
        
        # Fallback to English
        return {
            "language": SupportedLanguage.ENGLISH,
            "confidence": 0.5,
            "alternatives": []
        }
    
    def _detect_with_char_frequency(self, text: str) -> Dict[str, Any]:
        """Detect language using character frequency analysis."""
        
        # Calculate character frequencies in text
        text_lower = text.lower()
        char_counts = defaultdict(int)
        total_chars = 0
        
        for char in text_lower:
            if char.isalpha():
                char_counts[char] += 1
                total_chars += 1
        
        if total_chars == 0:
            return {
                "language": SupportedLanguage.ENGLISH,
                "confidence": 0.3,
                "alternatives": []
            }
        
        # Calculate frequencies
        text_frequencies = {char: count / total_chars * 100 
                          for char, count in char_counts.items()}
        
        # Compare with language frequency patterns
        language_scores = {}
        
        for language, lang_frequencies in self.char_frequencies.items():
            score = 0.0
            common_chars = set(text_frequencies.keys()) & set(lang_frequencies.keys())
            
            for char in common_chars:
                # Calculate similarity (inverse of absolute difference)
                diff = abs(text_frequencies[char] - lang_frequencies[char])
                similarity = max(0, 1 - diff / 10)  # Normalize difference
                score += similarity
            
            # Normalize by number of common characters
            if common_chars:
                language_scores[language] = score / len(common_chars)
            else:
                language_scores[language] = 0.0
        
        # Sort by score
        sorted_scores = sorted(language_scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_scores:
            best_lang, best_score = sorted_scores[0]
            alternatives = [(lang, score) for lang, score in sorted_scores[1:3]]
            
            return {
                "language": best_lang,
                "confidence": min(1.0, best_score),
                "alternatives": alternatives
            }
        
        return {
            "language": SupportedLanguage.ENGLISH,
            "confidence": 0.3,
            "alternatives": []
        }
    
    def _detect_with_common_words(self, text: str) -> Dict[str, Any]:
        """Detect language using common words analysis."""
        
        words = re.findall(r'\b\w+\b', text.lower())
        
        if not words:
            return {
                "language": SupportedLanguage.ENGLISH,
                "confidence": 0.3,
                "alternatives": []
            }
        
        language_scores = {}
        
        for language, common_words in self.common_words.items():
            matches = sum(1 for word in words if word in common_words)
            score = matches / len(words) if words else 0
            language_scores[language] = score
        
        # Sort by score
        sorted_scores = sorted(language_scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_scores:
            best_lang, best_score = sorted_scores[0]
            alternatives = [(lang, score) for lang, score in sorted_scores[1:3]]
            
            return {
                "language": best_lang,
                "confidence": best_score,
                "alternatives": alternatives
            }
        
        return {
            "language": SupportedLanguage.ENGLISH,
            "confidence": 0.3,
            "alternatives": []
        }
    
    def _detect_with_patterns(self, text: str) -> Dict[str, Any]:
        """Detect language using pattern matching."""
        
        language_scores = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0.0
            
            # Check character patterns
            for pattern in patterns.get("char_patterns", []):
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches / len(text) if text else 0
            
            # Check for specific language features
            if "articles" in patterns:
                words = re.findall(r'\b\w+\b', text.lower())
                article_matches = sum(1 for word in words if word in patterns["articles"])
                score += article_matches / len(words) if words else 0
            
            language_scores[language] = min(1.0, score)
        
        # Sort by score
        sorted_scores = sorted(language_scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_scores:
            best_lang, best_score = sorted_scores[0]
            alternatives = [(lang, score) for lang, score in sorted_scores[1:3]]
            
            return {
                "language": best_lang,
                "confidence": best_score,
                "alternatives": alternatives
            }
        
        return {
            "language": SupportedLanguage.ENGLISH,
            "confidence": 0.3,
            "alternatives": []
        }
    
    def _combine_detection_results(self, results: List[Tuple[str, Dict[str, Any], float]]) -> Dict[str, Any]:
        """Combine multiple detection results using weighted voting."""
        
        language_scores = defaultdict(float)
        total_weight = 0.0
        
        for method_name, result, weight in results:
            language = result["language"]
            confidence = result["confidence"]
            
            language_scores[language] += confidence * weight
            total_weight += weight
        
        # Normalize scores
        if total_weight > 0:
            for language in language_scores:
                language_scores[language] /= total_weight
        
        # Sort by score
        sorted_scores = sorted(language_scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_scores:
            best_lang, best_score = sorted_scores[0]
            alternatives = [(lang, score) for lang, score in sorted_scores[1:3]]
            
            # Apply English boost if configured
            if best_lang == SupportedLanguage.ENGLISH:
                config = self.processing_configs[SupportedLanguage.ENGLISH]
                best_score += config.get("confidence_boost", 0.0)
                best_score = min(1.0, best_score)
            
            return {
                "language": best_lang,
                "confidence": best_score,
                "alternatives": alternatives
            }
        
        return {
            "language": SupportedLanguage.ENGLISH,
            "confidence": 0.5,
            "alternatives": []
        }
    
    def _determine_confidence_level(self, confidence: float) -> LanguageConfidence:
        """Determine confidence level based on confidence score."""
        
        if confidence >= 0.9:
            return LanguageConfidence.HIGH
        elif confidence >= 0.7:
            return LanguageConfidence.MEDIUM
        elif confidence >= 0.5:
            return LanguageConfidence.LOW
        else:
            return LanguageConfidence.VERY_LOW
    
    def _extract_language_features(self, text: str, language: SupportedLanguage) -> Dict[str, Any]:
        """Extract language-specific features from text."""
        
        features = {
            "text_length": len(text),
            "word_count": len(re.findall(r'\b\w+\b', text)),
            "sentence_count": len(re.findall(r'[.!?]+', text)),
            "avg_word_length": 0.0,
            "special_chars": []
        }
        
        words = re.findall(r'\b\w+\b', text)
        if words:
            features["avg_word_length"] = sum(len(word) for word in words) / len(words)
        
        # Language-specific features
        if language in self.language_patterns:
            patterns = self.language_patterns[language]
            
            # Check for special characters
            for pattern in patterns.get("char_patterns", []):
                matches = re.findall(pattern, text)
                if matches:
                    features["special_chars"].extend(matches)
        
        return features
    
    def process_multilingual_input(self, text: str, 
                                 target_language: SupportedLanguage = SupportedLanguage.ENGLISH) -> MultiLanguageProcessingResult:
        """Process multilingual input with optional translation."""
        
        # Detect language
        detection_result = self.detect_language(text)
        
        processing_notes = []
        translated_text = None
        translation_confidence = None
        
        # Determine if translation is needed
        if detection_result.detected_language != target_language:
            if detection_result.confidence_level in [LanguageConfidence.HIGH, LanguageConfidence.MEDIUM]:
                # Attempt translation (placeholder - would integrate with translation service)
                translated_text = self._translate_text(text, detection_result.detected_language, target_language)
                translation_confidence = 0.8  # Placeholder confidence
                processing_notes.append(f"Translated from {detection_result.detected_language.value} to {target_language.value}")
            else:
                processing_notes.append(f"Low confidence language detection ({detection_result.confidence:.2f}), processing as {target_language.value}")
        
        # Determine final processing language
        if translated_text:
            processing_language = target_language
            final_text = translated_text
        else:
            processing_language = detection_result.detected_language
            final_text = text
        
        return MultiLanguageProcessingResult(
            original_text=text,
            detected_language=detection_result.detected_language,
            translated_text=translated_text,
            processing_language=processing_language,
            language_detection=detection_result,
            translation_confidence=translation_confidence,
            processing_notes=processing_notes
        )
    
    def _translate_text(self, text: str, source_lang: SupportedLanguage, 
                       target_lang: SupportedLanguage) -> str:
        """Translate text between languages (placeholder implementation)."""
        
        # This is a placeholder - in production, this would integrate with
        # translation services like Google Translate, Azure Translator, etc.
        
        logger.info(f"Translation requested: {source_lang.value} -> {target_lang.value}")
        
        # For now, return original text with a note
        return f"[TRANSLATED FROM {source_lang.value.upper()}] {text}"
    
    def get_supported_languages(self) -> List[Dict[str, Any]]:
        """Get list of supported languages with their configurations."""
        
        languages = []
        
        for language in SupportedLanguage:
            config = self.processing_configs.get(language, {})
            has_spacy_model = language in self.spacy_models
            
            languages.append({
                "code": language.value,
                "name": language.name.title(),
                "primary_language": config.get("primary_language", False),
                "translation_required": config.get("translation_required", True),
                "processing_priority": config.get("processing_priority", 5),
                "spacy_model_available": has_spacy_model,
                "special_handling": config.get("special_handling", [])
            })
        
        return sorted(languages, key=lambda x: x["processing_priority"])


# Example usage
if __name__ == "__main__":
    # Initialize language detection engine
    engine = LanguageDetectionEngine()
    
    # Test texts in different languages
    test_texts = [
        "Create a secure user authentication system with JWT tokens",  # English
        "Crear un sistema de autenticación de usuarios seguro con tokens JWT",  # Spanish
        "Créer un système d'authentification utilisateur sécurisé avec des tokens JWT",  # French
        "Erstellen Sie ein sicheres Benutzerauthentifizierungssystem mit JWT-Token",  # German
        "创建一个使用JWT令牌的安全用户身份验证系统"  # Chinese
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        
        # Detect language
        detection = engine.detect_language(text)
        print(f"Detected: {detection.detected_language.value} (confidence: {detection.confidence:.3f})")
        print(f"Confidence level: {detection.confidence_level.value}")
        
        # Process multilingual input
        processing = engine.process_multilingual_input(text)
        print(f"Processing language: {processing.processing_language.value}")
        if processing.translated_text:
            print(f"Translated: {processing.translated_text}")
        
        print(f"Processing time: {detection.processing_time_ms:.2f}ms")
    
    # Show supported languages
    print(f"\nSupported languages: {len(engine.get_supported_languages())}")
    for lang_info in engine.get_supported_languages():
        print(f"  - {lang_info['name']} ({lang_info['code']}) - Priority: {lang_info['processing_priority']}")
