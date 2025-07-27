"""
N.L.D.S. OpenAPI 3.0 Documentation
Comprehensive API documentation with interactive Swagger UI and examples
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Pydantic models for API documentation

class ProcessingDimension(str, Enum):
    """Processing dimensions for N.L.D.S."""
    LOGICAL = "logical"
    EMOTIONAL = "emotional"
    CREATIVE = "creative"
    ALL = "all"


class JAEGISMode(int, Enum):
    """JAEGIS operation modes."""
    MODE_1 = 1  # Basic operation
    MODE_2 = 2  # Enhanced operation
    MODE_3 = 3  # Advanced operation
    MODE_4 = 4  # Expert operation
    MODE_5 = 5  # Master operation


class SquadType(str, Enum):
    """JAEGIS squad types."""
    CORE_SYSTEM = "core_system"
    DEVELOPMENT = "development"
    ANALYSIS = "analysis"
    SECURITY = "security"
    CONTENT = "content"
    INTEGRATION = "integration"
    GARAS_ALPHA = "garas_alpha"
    GARAS_BETA = "garas_beta"
    GARAS_GAMMA = "garas_gamma"
    GARAS_DELTA = "garas_delta"
    GARAS_EPSILON = "garas_epsilon"
    IUAS_PRIME = "iuas_prime"


class ConfidenceLevel(str, Enum):
    """Confidence levels for processing results."""
    LOW = "low"      # < 70%
    MEDIUM = "medium"  # 70-84%
    HIGH = "high"    # 85-94%
    VERY_HIGH = "very_high"  # >= 95%


class NLDSRequest(BaseModel):
    """Request model for N.L.D.S. processing."""
    
    input_text: str = Field(
        ...,
        description="Natural language input to be processed",
        example="Create a secure user authentication system with JWT tokens",
        min_length=1,
        max_length=10000
    )
    
    user_id: Optional[str] = Field(
        None,
        description="User identifier for personalized processing",
        example="user_12345"
    )
    
    session_id: Optional[str] = Field(
        None,
        description="Session identifier for context continuity",
        example="session_abc123"
    )
    
    processing_dimensions: List[ProcessingDimension] = Field(
        default=[ProcessingDimension.ALL],
        description="Dimensions to process (logical, emotional, creative, or all)",
        example=["logical", "emotional"]
    )
    
    preferred_mode: Optional[JAEGISMode] = Field(
        None,
        description="Preferred JAEGIS operation mode (1-5)",
        example=3
    )
    
    preferred_squad: Optional[SquadType] = Field(
        None,
        description="Preferred squad for task execution",
        example="development"
    )
    
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context information",
        example={"project": "web_app", "priority": "high"}
    )
    
    require_high_confidence: bool = Field(
        default=True,
        description="Require high confidence (≥85%) for processing",
        example=True
    )


class DimensionalAnalysis(BaseModel):
    """Analysis result for a specific dimension."""
    
    dimension: ProcessingDimension = Field(
        ...,
        description="Processing dimension",
        example="logical"
    )
    
    confidence: float = Field(
        ...,
        description="Confidence score (0.0-1.0)",
        example=0.92,
        ge=0.0,
        le=1.0
    )
    
    analysis_result: Dict[str, Any] = Field(
        ...,
        description="Detailed analysis results",
        example={
            "intent": "create_authentication_system",
            "requirements": ["security", "JWT", "user_management"],
            "complexity": "medium"
        }
    )
    
    processing_time_ms: float = Field(
        ...,
        description="Processing time in milliseconds",
        example=125.5
    )


class JAEGISCommand(BaseModel):
    """Generated JAEGIS command."""
    
    command: str = Field(
        ...,
        description="Generated JAEGIS command",
        example="FRED:IMPLEMENT --component=auth-system --security=jwt --priority=high"
    )
    
    mode: JAEGISMode = Field(
        ...,
        description="Recommended JAEGIS mode",
        example=3
    )
    
    squad: SquadType = Field(
        ...,
        description="Recommended squad for execution",
        example="development"
    )
    
    parameters: Dict[str, Any] = Field(
        ...,
        description="Command parameters",
        example={
            "component": "auth-system",
            "security": "jwt",
            "priority": "high"
        }
    )
    
    confidence: float = Field(
        ...,
        description="Command generation confidence",
        example=0.89,
        ge=0.0,
        le=1.0
    )


class AlternativeInterpretation(BaseModel):
    """Alternative interpretation for ambiguous input."""
    
    interpretation: str = Field(
        ...,
        description="Alternative interpretation of the input",
        example="Create user registration and login forms"
    )
    
    confidence: float = Field(
        ...,
        description="Confidence in this interpretation",
        example=0.76,
        ge=0.0,
        le=1.0
    )
    
    suggested_command: JAEGISCommand = Field(
        ...,
        description="Suggested JAEGIS command for this interpretation"
    )


class NLDSResponse(BaseModel):
    """Response model for N.L.D.S. processing."""
    
    request_id: str = Field(
        ...,
        description="Unique request identifier",
        example="req_abc123def456"
    )
    
    processing_timestamp: datetime = Field(
        ...,
        description="Processing timestamp",
        example="2024-01-15T10:30:00Z"
    )
    
    total_processing_time_ms: float = Field(
        ...,
        description="Total processing time in milliseconds",
        example=387.2
    )
    
    dimensional_analysis: List[DimensionalAnalysis] = Field(
        ...,
        description="Analysis results for each dimension"
    )
    
    overall_confidence: float = Field(
        ...,
        description="Overall confidence score",
        example=0.91,
        ge=0.0,
        le=1.0
    )
    
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Confidence level category",
        example="high"
    )
    
    primary_command: JAEGISCommand = Field(
        ...,
        description="Primary recommended JAEGIS command"
    )
    
    alternative_interpretations: List[AlternativeInterpretation] = Field(
        default_factory=list,
        description="Alternative interpretations (if confidence < 85%)"
    )
    
    context_updates: Dict[str, Any] = Field(
        default_factory=dict,
        description="Updates to user/session context",
        example={"last_intent": "authentication", "complexity_preference": "medium"}
    )
    
    warnings: List[str] = Field(
        default_factory=list,
        description="Processing warnings or notices",
        example=["Input contains ambiguous terms"]
    )


class HealthStatus(BaseModel):
    """System health status."""
    
    status: str = Field(
        ...,
        description="Overall system status",
        example="healthy"
    )
    
    timestamp: datetime = Field(
        ...,
        description="Health check timestamp",
        example="2024-01-15T10:30:00Z"
    )
    
    components: Dict[str, str] = Field(
        ...,
        description="Component health status",
        example={
            "nlp_engine": "healthy",
            "database": "healthy",
            "cache": "healthy",
            "jaegis_interface": "healthy"
        }
    )
    
    performance_metrics: Dict[str, float] = Field(
        ...,
        description="Performance metrics",
        example={
            "avg_response_time_ms": 245.7,
            "requests_per_minute": 87.3,
            "error_rate": 0.02
        }
    )


class UserProfile(BaseModel):
    """User profile information."""
    
    user_id: str = Field(
        ...,
        description="User identifier",
        example="user_12345"
    )
    
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="User preferences",
        example={
            "preferred_mode": 3,
            "preferred_squad": "development",
            "complexity_level": "medium"
        }
    )
    
    learning_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="User learning and adaptation data",
        example={
            "common_intents": ["development", "analysis"],
            "success_patterns": ["detailed_requirements", "step_by_step"]
        }
    )
    
    created_at: datetime = Field(
        ...,
        description="Profile creation timestamp",
        example="2024-01-01T00:00:00Z"
    )
    
    last_updated: datetime = Field(
        ...,
        description="Last update timestamp",
        example="2024-01-15T10:30:00Z"
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error_code: str = Field(
        ...,
        description="Error code",
        example="INVALID_INPUT"
    )
    
    error_message: str = Field(
        ...,
        description="Human-readable error message",
        example="Input text is too short or empty"
    )
    
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details",
        example={"min_length": 1, "provided_length": 0}
    )
    
    timestamp: datetime = Field(
        ...,
        description="Error timestamp",
        example="2024-01-15T10:30:00Z"
    )
    
    request_id: Optional[str] = Field(
        None,
        description="Request identifier",
        example="req_abc123def456"
    )


# FastAPI app with OpenAPI configuration
def create_nlds_api() -> FastAPI:
    """Create N.L.D.S. FastAPI application with comprehensive OpenAPI documentation."""
    
    app = FastAPI(
        title="N.L.D.S. - Natural Language Detection System",
        description="""
        ## Natural Language Detection System (N.L.D.S.)
        
        The N.L.D.S. is a Tier 0 component of the JAEGIS Enhanced Agent System v2.2 that provides 
        intelligent natural language processing and translation to JAEGIS commands.
        
        ### Key Features
        
        - **Three-Dimensional Processing**: Logical, emotional, and creative analysis
        - **Human-Centric Design**: Cognitive modeling and user adaptation
        - **High Confidence Translation**: ≥85% confidence threshold with alternatives
        - **Real-time Processing**: <500ms response time
        - **JAEGIS Integration**: Direct command generation and squad selection
        
        ### Processing Flow
        
        1. **Input Analysis**: Multi-dimensional natural language processing
        2. **Intent Recognition**: Identify user intent and requirements
        3. **Context Integration**: Apply user profile and session context
        4. **Command Generation**: Generate optimized JAEGIS commands
        5. **Confidence Validation**: Ensure ≥85% confidence or provide alternatives
        
        ### Authentication
        
        All endpoints require JWT authentication. Include the token in the Authorization header:
        ```
        Authorization: Bearer <your-jwt-token>
        ```
        
        ### Rate Limiting
        
        - **Standard Users**: 100 requests per minute
        - **Premium Users**: 500 requests per minute
        - **Enterprise**: 1000 requests per minute
        
        ### Support
        
        For support and documentation, visit: https://github.com/usemanusai/JAEGIS
        """,
        version="2.2.0",
        contact={
            "name": "JAEGIS Support",
            "url": "https://github.com/usemanusai/JAEGIS",
            "email": "support@jaegis.ai"
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        },
        servers=[
            {
                "url": "https://api.jaegis.ai/v2",
                "description": "Production server"
            },
            {
                "url": "https://staging-api.jaegis.ai/v2",
                "description": "Staging server"
            },
            {
                "url": "http://localhost:8000/v2",
                "description": "Development server"
            }
        ],
        openapi_tags=[
            {
                "name": "Processing",
                "description": "Natural language processing and command generation"
            },
            {
                "name": "User Management",
                "description": "User profile and preference management"
            },
            {
                "name": "System",
                "description": "System health and monitoring"
            },
            {
                "name": "Authentication",
                "description": "Authentication and authorization"
            }
        ]
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


# Create the FastAPI app
app = create_nlds_api()


# API endpoint definitions with comprehensive documentation
@app.post(
    "/process",
    response_model=NLDSResponse,
    responses={
        200: {
            "description": "Successful processing",
            "content": {
                "application/json": {
                    "example": {
                        "request_id": "req_abc123def456",
                        "processing_timestamp": "2024-01-15T10:30:00Z",
                        "total_processing_time_ms": 387.2,
                        "dimensional_analysis": [
                            {
                                "dimension": "logical",
                                "confidence": 0.92,
                                "analysis_result": {
                                    "intent": "create_authentication_system",
                                    "requirements": ["security", "JWT", "user_management"],
                                    "complexity": "medium"
                                },
                                "processing_time_ms": 125.5
                            }
                        ],
                        "overall_confidence": 0.91,
                        "confidence_level": "high",
                        "primary_command": {
                            "command": "FRED:IMPLEMENT --component=auth-system --security=jwt --priority=high",
                            "mode": 3,
                            "squad": "development",
                            "parameters": {
                                "component": "auth-system",
                                "security": "jwt",
                                "priority": "high"
                            },
                            "confidence": 0.89
                        },
                        "alternative_interpretations": [],
                        "context_updates": {
                            "last_intent": "authentication",
                            "complexity_preference": "medium"
                        },
                        "warnings": []
                    }
                }
            }
        },
        400: {"description": "Invalid input", "model": ErrorResponse},
        401: {"description": "Authentication required", "model": ErrorResponse},
        429: {"description": "Rate limit exceeded", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    },
    tags=["Processing"],
    summary="Process natural language input",
    description="""
    Process natural language input through the N.L.D.S. three-dimensional analysis engine.
    
    This endpoint performs comprehensive analysis including:
    - Logical analysis for requirement extraction
    - Emotional context analysis for user state
    - Creative interpretation for innovative solutions
    
    Returns optimized JAEGIS commands with confidence validation.
    """
)
async def process_natural_language(
    request: NLDSRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Process natural language input and generate JAEGIS commands."""
    # Implementation would go here
    pass


@app.get(
    "/health",
    response_model=HealthStatus,
    tags=["System"],
    summary="System health check",
    description="Get comprehensive system health status and performance metrics."
)
async def health_check():
    """Get system health status."""
    # Implementation would go here
    pass


@app.get(
    "/user/{user_id}/profile",
    response_model=UserProfile,
    tags=["User Management"],
    summary="Get user profile",
    description="Retrieve user profile including preferences and learning data."
)
async def get_user_profile(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get user profile."""
    # Implementation would go here
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
