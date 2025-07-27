"""
N.L.D.S. Component Interface Specifications
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

This module defines the core interfaces and contracts for all N.L.D.S. components,
ensuring consistent integration patterns and maintainable architecture.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime


# ============================================================================
# CORE DATA MODELS
# ============================================================================

class InputType(Enum):
    """Supported input types for N.L.D.S."""
    TEXT = "text"
    VOICE = "voice"
    COMMAND = "command"
    CONVERSATION = "conversation"


class ConfidenceLevel(Enum):
    """Confidence level classifications."""
    HIGH = "high"      # ≥85%
    MEDIUM = "medium"  # 70-84%
    LOW = "low"        # <70%


@dataclass
class AnalysisResult:
    """Core analysis result from NLP processing."""
    tokens: List[str]
    semantics: Dict[str, Any]
    intent: Dict[str, Any]
    context: Dict[str, Any]
    confidence: float
    processing_time_ms: int
    timestamp: datetime


@dataclass
class DimensionalResult:
    """Three-dimensional processing result."""
    logical: Dict[str, Any]
    emotional: Dict[str, Any]
    creative: Dict[str, Any]
    synthesis: Dict[str, Any]
    confidence_score: float


@dataclass
class HumanProcessingResult:
    """Human-centric processing result."""
    cognitive_model: Dict[str, Any]
    decision: Dict[str, Any]
    inferred_intent: Dict[str, Any]
    updated_profile: Dict[str, Any]
    confidence_score: float


@dataclass
class TranslationResult:
    """Final translation result with JAEGIS commands."""
    primary_commands: List[Dict[str, Any]]
    selected_mode: int
    selected_squads: List[str]
    confidence_score: float
    alternatives: List[Dict[str, Any]]
    intent_mapping: Dict[str, Any]
    context_preservation: Dict[str, Any]


# ============================================================================
# INPUT PROCESSING INTERFACES
# ============================================================================

class InputProcessorInterface(ABC):
    """Base interface for all input processors."""
    
    @abstractmethod
    async def process_input(self, raw_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process raw input and return normalized format."""
        pass
    
    @abstractmethod
    def validate_input(self, raw_input: str) -> bool:
        """Validate input format and content."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Return list of supported input formats."""
        pass


class TextInputProcessor(InputProcessorInterface):
    """Interface for text input processing."""
    
    @abstractmethod
    async def normalize_text(self, text: str) -> str:
        """Normalize text input for processing."""
        pass
    
    @abstractmethod
    async def detect_encoding(self, text: str) -> str:
        """Detect text encoding."""
        pass


class VoiceInputProcessor(InputProcessorInterface):
    """Interface for voice input processing."""
    
    @abstractmethod
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Transcribe audio to text."""
        pass
    
    @abstractmethod
    async def detect_language(self, audio_data: bytes) -> str:
        """Detect spoken language."""
        pass


# ============================================================================
# NLP ANALYSIS INTERFACES
# ============================================================================

class NLPAnalysisInterface(ABC):
    """Base interface for NLP analysis components."""
    
    @abstractmethod
    async def analyze(self, input_data: str, context: Optional[Dict] = None) -> AnalysisResult:
        """Perform NLP analysis on input data."""
        pass
    
    @abstractmethod
    def get_confidence_score(self, analysis_result: AnalysisResult) -> float:
        """Calculate confidence score for analysis."""
        pass


class TokenizerInterface(NLPAnalysisInterface):
    """Interface for tokenization components."""
    
    @abstractmethod
    async def tokenize(self, text: str) -> List[str]:
        """Tokenize input text."""
        pass
    
    @abstractmethod
    async def preprocess(self, text: str) -> str:
        """Preprocess text before tokenization."""
        pass


class SemanticAnalyzerInterface(NLPAnalysisInterface):
    """Interface for semantic analysis."""
    
    @abstractmethod
    async def extract_semantics(self, tokens: List[str]) -> Dict[str, Any]:
        """Extract semantic meaning from tokens."""
        pass
    
    @abstractmethod
    async def analyze_context(self, semantics: Dict, context: Dict) -> Dict[str, Any]:
        """Analyze semantic context."""
        pass


class IntentRecognizerInterface(NLPAnalysisInterface):
    """Interface for intent recognition."""
    
    @abstractmethod
    async def recognize_intent(self, semantics: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize user intent from semantic analysis."""
        pass
    
    @abstractmethod
    async def classify_intent_category(self, intent: Dict) -> str:
        """Classify intent into JAEGIS categories."""
        pass


# ============================================================================
# THREE-DIMENSIONAL PROCESSING INTERFACES
# ============================================================================

class DimensionalProcessorInterface(ABC):
    """Base interface for dimensional processing."""
    
    @abstractmethod
    async def process_dimension(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """Process specific dimension of analysis."""
        pass
    
    @abstractmethod
    def get_dimension_name(self) -> str:
        """Return dimension name."""
        pass


class LogicalAnalyzerInterface(DimensionalProcessorInterface):
    """Interface for logical analysis dimension."""
    
    @abstractmethod
    async def extract_requirements(self, semantics: Dict) -> List[str]:
        """Extract logical requirements from input."""
        pass
    
    @abstractmethod
    async def decompose_logic(self, intent: Dict) -> Dict[str, Any]:
        """Decompose logical structure of request."""
        pass


class EmotionalAnalyzerInterface(DimensionalProcessorInterface):
    """Interface for emotional context analysis."""
    
    @abstractmethod
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze emotional sentiment."""
        pass
    
    @abstractmethod
    async def detect_user_state(self, context: Dict) -> Dict[str, Any]:
        """Detect user emotional state."""
        pass


class CreativeInterpreterInterface(DimensionalProcessorInterface):
    """Interface for creative interpretation."""
    
    @abstractmethod
    async def identify_patterns(self, semantics: Dict) -> List[Dict]:
        """Identify creative patterns in input."""
        pass
    
    @abstractmethod
    async def generate_alternatives(self, intent: Dict) -> List[Dict]:
        """Generate creative alternative interpretations."""
        pass


# ============================================================================
# HUMAN-CENTRIC PROCESSING INTERFACES
# ============================================================================

class CognitiveModelInterface(ABC):
    """Interface for cognitive modeling."""
    
    @abstractmethod
    async def model_cognition(self, dimensional_result: DimensionalResult) -> Dict[str, Any]:
        """Model human cognitive patterns."""
        pass
    
    @abstractmethod
    async def simulate_multitasking(self, tasks: List[Dict]) -> Dict[str, Any]:
        """Simulate human multitasking patterns."""
        pass


class DecisionFrameworkInterface(ABC):
    """Interface for decision-making framework."""
    
    @abstractmethod
    async def make_decision(self, cognitive_model: Dict, options: List[Dict]) -> Dict[str, Any]:
        """Make decision using human-like framework."""
        pass
    
    @abstractmethod
    async def apply_bounded_rationality(self, decision_context: Dict) -> Dict[str, Any]:
        """Apply bounded rationality principles."""
        pass


class UserLearningInterface(ABC):
    """Interface for user learning and adaptation."""
    
    @abstractmethod
    async def update_user_profile(self, user_id: str, interaction_data: Dict) -> Dict[str, Any]:
        """Update user profile based on interaction."""
        pass
    
    @abstractmethod
    async def learn_preferences(self, user_id: str, feedback: Dict) -> None:
        """Learn user preferences from feedback."""
        pass


# ============================================================================
# TRANSLATION ENGINE INTERFACES
# ============================================================================

class TranslationEngineInterface(ABC):
    """Base interface for translation components."""
    
    @abstractmethod
    async def translate(self, human_result: HumanProcessingResult) -> TranslationResult:
        """Translate human processing result to JAEGIS commands."""
        pass
    
    @abstractmethod
    def validate_confidence(self, confidence_score: float) -> bool:
        """Validate confidence meets threshold."""
        pass


class CommandGeneratorInterface(TranslationEngineInterface):
    """Interface for command generation."""
    
    @abstractmethod
    async def generate_commands(self, intent: Dict, requirements: List[str]) -> List[Dict]:
        """Generate JAEGIS commands from intent and requirements."""
        pass
    
    @abstractmethod
    async def validate_command_syntax(self, commands: List[Dict]) -> bool:
        """Validate generated command syntax."""
        pass


class ModeSelectionInterface(ABC):
    """Interface for mode selection."""
    
    @abstractmethod
    async def select_mode(self, complexity: float, requirements: Dict) -> int:
        """Select appropriate JAEGIS operational mode."""
        pass
    
    @abstractmethod
    def get_mode_capabilities(self, mode: int) -> Dict[str, Any]:
        """Get capabilities for specific mode."""
        pass


class SquadSelectionInterface(ABC):
    """Interface for squad selection."""
    
    @abstractmethod
    async def select_squads(self, task_type: str, requirements: Dict) -> List[str]:
        """Select appropriate squads for task."""
        pass
    
    @abstractmethod
    def get_squad_capabilities(self, squad_name: str) -> Dict[str, Any]:
        """Get capabilities for specific squad."""
        pass


# ============================================================================
# INTEGRATION INTERFACES
# ============================================================================

class JAEGISIntegrationInterface(ABC):
    """Interface for JAEGIS system integration."""
    
    @abstractmethod
    async def execute_commands(self, translation_result: TranslationResult) -> Dict[str, Any]:
        """Execute commands through JAEGIS system."""
        pass
    
    @abstractmethod
    async def monitor_execution(self, execution_id: str) -> Dict[str, Any]:
        """Monitor command execution status."""
        pass


class AMASIAPIntegrationInterface(ABC):
    """Interface for A.M.A.S.I.A.P. Protocol integration."""
    
    @abstractmethod
    async def enhance_input(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """Enhance input using A.M.A.S.I.A.P. Protocol."""
        pass
    
    @abstractmethod
    async def trigger_research(self, research_query: str) -> Dict[str, Any]:
        """Trigger research framework."""
        pass


# ============================================================================
# STORAGE INTERFACES
# ============================================================================

class UserProfileStorageInterface(ABC):
    """Interface for user profile storage."""
    
    @abstractmethod
    async def save_profile(self, user_id: str, profile_data: Dict) -> bool:
        """Save user profile data."""
        pass
    
    @abstractmethod
    async def load_profile(self, user_id: str) -> Optional[Dict]:
        """Load user profile data."""
        pass
    
    @abstractmethod
    async def update_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences."""
        pass


class SessionStorageInterface(ABC):
    """Interface for session storage."""
    
    @abstractmethod
    async def create_session(self, user_id: str, session_data: Dict) -> str:
        """Create new session."""
        pass
    
    @abstractmethod
    async def update_session(self, session_id: str, session_data: Dict) -> bool:
        """Update session data."""
        pass
    
    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data."""
        pass


# ============================================================================
# MONITORING INTERFACES
# ============================================================================

class MonitoringInterface(ABC):
    """Interface for system monitoring."""
    
    @abstractmethod
    async def log_metrics(self, metrics: Dict[str, Any]) -> None:
        """Log system metrics."""
        pass
    
    @abstractmethod
    async def track_performance(self, operation: str, duration_ms: int) -> None:
        """Track performance metrics."""
        pass
    
    @abstractmethod
    async def alert_on_threshold(self, metric: str, value: float, threshold: float) -> None:
        """Alert when metric exceeds threshold."""
        pass


# ============================================================================
# FACTORY INTERFACES
# ============================================================================

class ComponentFactoryInterface(ABC):
    """Interface for component factories."""
    
    @abstractmethod
    def create_component(self, component_type: str, config: Dict) -> Any:
        """Create component instance."""
        pass
    
    @abstractmethod
    def get_available_components(self) -> List[str]:
        """Get list of available components."""
        pass


# ============================================================================
# CONFIGURATION INTERFACES
# ============================================================================

class ConfigurationInterface(ABC):
    """Interface for configuration management."""
    
    @abstractmethod
    async def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from path."""
        pass
    
    @abstractmethod
    async def validate_config(self, config: Dict) -> bool:
        """Validate configuration."""
        pass
    
    @abstractmethod
    async def update_config(self, key: str, value: Any) -> bool:
        """Update configuration value."""
        pass


# ============================================================================
# HEALTH CHECK INTERFACES
# ============================================================================

class HealthCheckInterface(ABC):
    """Interface for health checks."""
    
    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Perform health check."""
        pass
    
    @abstractmethod
    async def check_dependencies(self) -> Dict[str, bool]:
        """Check dependency health."""
        pass
    
    @abstractmethod
    def get_status(self) -> str:
        """Get current status."""
        pass
