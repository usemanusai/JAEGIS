"""
JAEGIS Cognitive Pipeline - Data Models
Pydantic models for the cognitive ingestion and synthesis pipeline

This module defines all data structures used throughout the pipeline,
ensuring type safety and data validation.
"""

from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid


class SourceType(str, Enum):
    """Supported content source types."""
    YOUTUBE = "youtube"
    PDF = "pdf"
    WEB_URL = "url"
    FILE = "file"
    TEXT = "text"


class ProcessingStatus(str, Enum):
    """Processing job status values."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class QuestionType(str, Enum):
    """Quiz question types."""
    MULTIPLE_CHOICE = "multiple-choice"
    TRUE_FALSE = "true-false"
    FILL_IN_BLANK = "fill-in-the-blank"
    SHORT_ANSWER = "short-answer"


class DifficultyLevel(str, Enum):
    """Content difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class SkillTag(str, Enum):
    """Skill-based tags for content categorization."""
    STATISTICAL_ANALYSIS = "skill:statistical_analysis"
    API_DESIGN = "skill:api_design"
    MACHINE_LEARNING = "skill:machine_learning"
    DATA_VISUALIZATION = "skill:data_visualization"
    SYSTEM_ARCHITECTURE = "skill:system_architecture"
    PROBLEM_SOLVING = "skill:problem_solving"
    COMMUNICATION = "skill:communication"
    CRITICAL_THINKING = "skill:critical_thinking"


# Base Models
class BaseTimestampedModel(BaseModel):
    """Base model with timestamp fields."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class QualityMetrics(BaseModel):
    """Content quality assessment metrics."""
    quality_score: float = Field(ge=0, le=100, description="Overall quality score (0-100)")
    issues: List[str] = Field(default_factory=list, description="List of quality issues")
    character_count: int = Field(ge=0, description="Total character count")
    word_count: int = Field(ge=0, description="Total word count")
    coherence_score: float = Field(ge=0, le=1, description="Content coherence score (0-1)")
    noise_ratio: float = Field(ge=0, le=1, description="Noise to signal ratio (0-1)")
    processing_time: float = Field(ge=0, description="Processing time in seconds")


class ContentMetadata(BaseModel):
    """Base content metadata."""
    source_type: SourceType
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    language: Optional[str] = "en"
    tags: List[str] = Field(default_factory=list)
    skill_tags: List[SkillTag] = Field(default_factory=list)


# Ingestion Models
class IngestionRequest(BaseModel):
    """Request model for content ingestion."""
    source_type: SourceType
    source_url: Optional[HttpUrl] = None
    content_text: Optional[str] = None
    processing_options: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[str] = None
    
    @validator('source_url')
    def validate_source_url(cls, v, values):
        source_type = values.get('source_type')
        if source_type in [SourceType.YOUTUBE, SourceType.WEB_URL] and not v:
            raise ValueError(f"source_url is required for {source_type}")
        return v
    
    @validator('content_text')
    def validate_content_text(cls, v, values):
        source_type = values.get('source_type')
        if source_type in [SourceType.TEXT, SourceType.FILE] and not v:
            raise ValueError(f"content_text is required for {source_type}")
        return v


class IngestionResponse(BaseModel):
    """Response model for content ingestion."""
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: ProcessingStatus
    message: str
    estimated_completion_time: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class IngestionResult(BaseModel):
    """Result of content ingestion process."""
    content: str
    metadata: ContentMetadata
    quality_metrics: QualityMetrics
    processing_info: Dict[str, Any]


# Content Structure Models
class ContentChapter(BaseModel):
    """Individual content chapter/section."""
    chapter_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    start_timestamp: Optional[float] = None
    end_timestamp: Optional[float] = None
    page_reference: Optional[str] = None
    word_count: int = Field(ge=0)
    key_concepts: List[str] = Field(default_factory=list)
    difficulty_level: DifficultyLevel = DifficultyLevel.MEDIUM


class ContentStructure(BaseModel):
    """Structured content with chapters and metadata."""
    content_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    summary: str
    chapters: List[ContentChapter]
    metadata: ContentMetadata
    total_word_count: int = Field(ge=0)
    estimated_reading_time: int = Field(ge=0, description="Estimated reading time in minutes")
    key_concepts: List[str] = Field(default_factory=list)
    skill_tags: List[SkillTag] = Field(default_factory=list)


# Quiz Models
class QuizOption(BaseModel):
    """Individual quiz option."""
    option_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    is_correct: bool = False


class QuizQuestion(BaseModel):
    """Individual quiz question."""
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: QuestionType
    text: str
    options: List[QuizOption] = Field(default_factory=list)
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    source_reference: Optional[str] = None
    skill_tags: List[SkillTag] = Field(default_factory=list)
    points: int = Field(default=1, ge=1)


class QuizData(BaseModel):
    """Complete quiz dataset."""
    quiz_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    title: str
    description: Optional[str] = None
    questions: List[QuizQuestion]
    total_points: int = Field(ge=0)
    estimated_time: int = Field(ge=0, description="Estimated completion time in minutes")
    difficulty_distribution: Dict[DifficultyLevel, int] = Field(default_factory=dict)
    skill_coverage: List[SkillTag] = Field(default_factory=list)


# Flashcard Models
class Flashcard(BaseModel):
    """Individual flashcard."""
    flashcard_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    front: str = Field(description="Question or term")
    back: str = Field(description="Answer or definition")
    category: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    source_reference: Optional[str] = None
    skill_tags: List[SkillTag] = Field(default_factory=list)
    spaced_repetition_interval: int = Field(default=1, description="Days until next review")


class FlashcardData(BaseModel):
    """Complete flashcard dataset."""
    flashcard_set_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    title: str
    description: Optional[str] = None
    flashcards: List[Flashcard]
    categories: List[str] = Field(default_factory=list)
    total_cards: int = Field(ge=0)
    skill_coverage: List[SkillTag] = Field(default_factory=list)


# Scenario Models
class ScenarioRole(BaseModel):
    """Role definition for training scenario."""
    role_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role_name: str
    objective: str
    private_information: Optional[str] = None
    constraints: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    skill_requirements: List[SkillTag] = Field(default_factory=list)


class TrainingScenario(BaseModel):
    """Training scenario for agent simulation."""
    scenario_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    title: str
    description: str
    context: str
    roles: List[ScenarioRole]
    duration_estimate: int = Field(ge=0, description="Estimated duration in minutes")
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    learning_objectives: List[str] = Field(default_factory=list)
    skill_tags: List[SkillTag] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)


# Summary Models
class SummaryData(BaseModel):
    """Content summary with audio."""
    summary_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    title: str
    text_summary: str
    key_points: List[str] = Field(default_factory=list)
    audio_url: Optional[str] = None
    audio_duration: Optional[int] = None
    reading_time: int = Field(ge=0, description="Estimated reading time in minutes")
    listening_time: Optional[int] = None
    voice_settings: Dict[str, Any] = Field(default_factory=dict)


# Analysis Models
class ThesisAnalysis(BaseModel):
    """Thesis deconstruction analysis."""
    thesis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    main_thesis: str
    supporting_arguments: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    counterarguments: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0, le=1)
    analysis_notes: Optional[str] = None


class ConceptTriangulation(BaseModel):
    """Conceptual triangulation across multiple sources."""
    triangulation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_ids: List[str]
    topic: str
    consensus_points: List[str] = Field(default_factory=list)
    disagreement_points: List[str] = Field(default_factory=list)
    unique_insights: Dict[str, List[str]] = Field(default_factory=dict)
    confidence_score: float = Field(ge=0, le=1)
    analysis_summary: str


class NoveltyDetection(BaseModel):
    """Novelty detection analysis."""
    novelty_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str
    novel_concepts: List[str] = Field(default_factory=list)
    novelty_scores: Dict[str, float] = Field(default_factory=dict)
    innovation_indicators: List[str] = Field(default_factory=list)
    comparison_sources: List[str] = Field(default_factory=list)
    overall_novelty_score: float = Field(ge=0, le=1)


# Confidence and Intelligence Models
class ConfidenceScore(BaseModel):
    """Confidence scoring for generated content."""
    confidence_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str
    content_type: str
    overall_confidence: float = Field(ge=0, le=1)
    component_scores: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    reliability_indicators: List[str] = Field(default_factory=list)
    calculation_method: str
    calculated_at: datetime = Field(default_factory=datetime.utcnow)


class FeedbackData(BaseModel):
    """User feedback for fine-tuning."""
    feedback_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str
    content_type: str
    user_id: Optional[str] = None
    rating: int = Field(ge=1, le=5)
    feedback_text: Optional[str] = None
    improvement_suggestions: List[str] = Field(default_factory=list)
    accuracy_rating: Optional[int] = Field(None, ge=1, le=5)
    usefulness_rating: Optional[int] = Field(None, ge=1, le=5)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


# Complete Pipeline Result
class PipelineResult(BaseModel):
    """Complete pipeline processing result."""
    job_id: str
    source_info: IngestionResult
    content_structure: ContentStructure
    quiz_data: Optional[QuizData] = None
    flashcard_data: Optional[FlashcardData] = None
    scenarios: List[TrainingScenario] = Field(default_factory=list)
    summary_data: Optional[SummaryData] = None
    thesis_analysis: Optional[ThesisAnalysis] = None
    novelty_detection: Optional[NoveltyDetection] = None
    confidence_scores: List[ConfidenceScore] = Field(default_factory=list)
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


# API Response Models
class JobStatusResponse(BaseModel):
    """Job status response model."""
    job_id: str
    status: ProcessingStatus
    progress: int = Field(ge=0, le=100)
    current_stage: str
    stages_completed: List[str] = Field(default_factory=list)
    created_at: datetime
    processing_time: Optional[float] = None
    results_available: bool = False
    error_message: Optional[str] = None


class JobResultsResponse(BaseModel):
    """Job results response model."""
    job_id: str
    status: ProcessingStatus
    results: PipelineResult
    processing_summary: Dict[str, Any] = Field(default_factory=dict)


class JobListResponse(BaseModel):
    """Job list response model."""
    total_jobs: int
    jobs: List[JobStatusResponse]
    filters_applied: Dict[str, Any] = Field(default_factory=dict)
