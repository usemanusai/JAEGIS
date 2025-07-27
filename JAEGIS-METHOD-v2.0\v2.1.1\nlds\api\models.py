"""
N.L.D.S. API Models
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Pydantic models for API request/response schemas, validation, and documentation.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class ProcessingMode(str, Enum):
    """Processing mode options."""
    STANDARD = "standard"
    ENHANCED = "enhanced"
    COMPREHENSIVE = "comprehensive"
    FAST = "fast"


class AnalysisType(str, Enum):
    """Analysis type options."""
    LOGICAL = "logical"
    EMOTIONAL = "emotional"
    CREATIVE = "creative"
    COMPREHENSIVE = "comprehensive"


class CommandStatus(str, Enum):
    """JAEGIS command status."""
    PENDING = "pending"
    QUEUED = "queued"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SystemStatus(str, Enum):
    """System status options."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"


# ============================================================================
# REQUEST MODELS
# ============================================================================

class ProcessingRequest(BaseModel):
    """Request model for input processing."""
    input_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Natural language input text to process",
        example="Analyze the current market trends for AI technology"
    )
    mode: ProcessingMode = Field(
        default=ProcessingMode.STANDARD,
        description="Processing mode to use"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context information"
    )
    user_preferences: Optional[Dict[str, Any]] = Field(
        default=None,
        description="User-specific preferences"
    )
    enable_amasiap: bool = Field(
        default=True,
        description="Enable A.M.A.S.I.A.P. Protocol enhancement"
    )
    
    @validator('input_text')
    def validate_input_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Input text cannot be empty')
        return v.strip()


class AnalysisRequest(BaseModel):
    """Request model for detailed analysis."""
    input_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Text to analyze"
    )
    analysis_types: List[AnalysisType] = Field(
        default=[AnalysisType.COMPREHENSIVE],
        description="Types of analysis to perform"
    )
    depth_level: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Analysis depth level (1-5)"
    )
    include_metadata: bool = Field(
        default=True,
        description="Include detailed metadata in response"
    )


class TranslationRequest(BaseModel):
    """Request model for JAEGIS translation."""
    input_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Enhanced input text to translate"
    )
    target_mode: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="Preferred JAEGIS mode (1-5)"
    )
    preferred_squad: Optional[str] = Field(
        default=None,
        description="Preferred squad for execution"
    )
    priority: str = Field(
        default="normal",
        regex="^(low|normal|high|critical)$",
        description="Command priority level"
    )


class CommandSubmissionRequest(BaseModel):
    """Request model for JAEGIS command submission."""
    command: Dict[str, Any] = Field(
        ...,
        description="JAEGIS command to submit"
    )
    priority: str = Field(
        default="normal",
        regex="^(low|normal|high|critical)$",
        description="Command priority"
    )
    timeout_seconds: int = Field(
        default=300,
        ge=10,
        le=3600,
        description="Command timeout in seconds"
    )


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(description="Overall health status")
    timestamp: datetime = Field(description="Health check timestamp")
    version: str = Field(description="API version")
    components: Dict[str, Any] = Field(description="Component health status")


class ProcessingResponse(BaseModel):
    """Response model for input processing."""
    request_id: str = Field(description="Unique request identifier")
    success: bool = Field(description="Processing success status")
    original_input: str = Field(description="Original input text")
    enhanced_input: str = Field(description="Enhanced input text")
    processing_time_ms: float = Field(description="Processing time in milliseconds")
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall confidence score"
    )
    components_used: List[str] = Field(description="Components used in processing")
    amasiap_result: Optional[Dict[str, Any]] = Field(
        default=None,
        description="A.M.A.S.I.A.P. Protocol results"
    )
    jaegis_command: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Generated JAEGIS command"
    )
    metadata: Dict[str, Any] = Field(description="Additional metadata")


class AnalysisResponse(BaseModel):
    """Response model for detailed analysis."""
    request_id: str = Field(description="Unique request identifier")
    input_text: str = Field(description="Analyzed input text")
    logical_analysis: Dict[str, Any] = Field(description="Logical analysis results")
    emotional_analysis: Dict[str, Any] = Field(description="Emotional analysis results")
    creative_analysis: Dict[str, Any] = Field(description="Creative analysis results")
    synthesis: Dict[str, Any] = Field(description="Synthesized analysis results")
    processing_time_ms: float = Field(description="Analysis time in milliseconds")
    timestamp: datetime = Field(description="Analysis timestamp")


class TranslationResponse(BaseModel):
    """Response model for JAEGIS translation."""
    request_id: str = Field(description="Unique request identifier")
    input_text: str = Field(description="Input text")
    jaegis_command: Dict[str, Any] = Field(description="Generated JAEGIS command")
    mode_selection: Dict[str, Any] = Field(description="Mode selection details")
    squad_selection: Dict[str, Any] = Field(description="Squad selection details")
    confidence_validation: Dict[str, Any] = Field(description="Confidence validation results")
    processing_time_ms: float = Field(description="Translation time in milliseconds")
    timestamp: datetime = Field(description="Translation timestamp")


class CommandSubmissionResponse(BaseModel):
    """Response model for command submission."""
    command_id: str = Field(description="Unique command identifier")
    status: CommandStatus = Field(description="Command status")
    submission_time: datetime = Field(description="Submission timestamp")
    estimated_completion: Optional[datetime] = Field(
        default=None,
        description="Estimated completion time"
    )
    tracking_url: str = Field(description="URL for status tracking")


class CommandStatusResponse(BaseModel):
    """Response model for command status."""
    command_id: str = Field(description="Command identifier")
    status: CommandStatus = Field(description="Current command status")
    progress_percentage: float = Field(
        ge=0.0,
        le=100.0,
        description="Completion percentage"
    )
    assigned_squad: Optional[str] = Field(
        default=None,
        description="Assigned squad"
    )
    assigned_agents: List[str] = Field(description="Assigned agents")
    execution_start: Optional[datetime] = Field(
        default=None,
        description="Execution start time"
    )
    estimated_completion: Optional[datetime] = Field(
        default=None,
        description="Estimated completion time"
    )
    result_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Command result data"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if failed"
    )
    last_update: datetime = Field(description="Last status update time")


class SystemStatusResponse(BaseModel):
    """Response model for system status."""
    system: Dict[str, Any] = Field(description="System information")
    components: Dict[str, Any] = Field(description="Component status")
    metrics: Dict[str, Any] = Field(description="System metrics")
    timestamp: datetime = Field(description="Status timestamp")


class MetricsResponse(BaseModel):
    """Response model for system metrics."""
    api: Dict[str, Any] = Field(description="API metrics")
    processing: Dict[str, Any] = Field(description="Processing metrics")
    integration: Dict[str, Any] = Field(description="Integration metrics")
    timestamp: datetime = Field(description="Metrics timestamp")


# ============================================================================
# ERROR MODELS
# ============================================================================

class ErrorResponse(BaseModel):
    """Error response model."""
    error: Dict[str, Any] = Field(description="Error details")
    
    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "code": 400,
                    "message": "Invalid input parameters",
                    "timestamp": "2025-07-26T12:00:00Z",
                    "path": "/process"
                }
            }
        }


class ValidationErrorResponse(BaseModel):
    """Validation error response model."""
    detail: List[Dict[str, Any]] = Field(description="Validation error details")
    
    class Config:
        schema_extra = {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "input_text"],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }


# ============================================================================
# UTILITY MODELS
# ============================================================================

class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(
        default=1,
        ge=1,
        description="Page number"
    )
    size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Page size"
    )


class SortParams(BaseModel):
    """Sorting parameters."""
    sort_by: str = Field(
        default="timestamp",
        description="Field to sort by"
    )
    sort_order: str = Field(
        default="desc",
        regex="^(asc|desc)$",
        description="Sort order"
    )


class FilterParams(BaseModel):
    """Filtering parameters."""
    start_date: Optional[datetime] = Field(
        default=None,
        description="Start date filter"
    )
    end_date: Optional[datetime] = Field(
        default=None,
        description="End date filter"
    )
    status: Optional[str] = Field(
        default=None,
        description="Status filter"
    )


# ============================================================================
# CONFIGURATION MODELS
# ============================================================================

class APIConfig(BaseModel):
    """API configuration model."""
    title: str = "N.L.D.S. API"
    version: str = "2.2.0"
    description: str = "Natural Language Detection System API"
    debug: bool = False
    cors_origins: List[str] = ["*"]
    rate_limit_per_minute: int = 100
    max_request_size: int = 10000
    
    class Config:
        env_prefix = "NLDS_API_"


class DatabaseConfig(BaseModel):
    """Database configuration model."""
    url: str = Field(description="Database connection URL")
    pool_size: int = Field(default=10, description="Connection pool size")
    max_overflow: int = Field(default=20, description="Max pool overflow")
    
    class Config:
        env_prefix = "NLDS_DB_"


class AuthConfig(BaseModel):
    """Authentication configuration model."""
    secret_key: str = Field(description="JWT secret key")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time"
    )
    
    class Config:
        env_prefix = "NLDS_AUTH_"
