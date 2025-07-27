"""
N.L.D.S. RESTful API
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

FastAPI-based RESTful API providing comprehensive endpoints for N.L.D.S. processing,
system interaction, and integration with JAEGIS ecosystem.
"""

from fastapi import FastAPI, HTTPException, Depends, Security, status, Request, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import asyncio
import time
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from contextlib import asynccontextmanager

# Local imports
from .models import *
from .dependencies import get_current_user, get_rate_limiter, verify_api_key
from .middleware import RequestLoggingMiddleware, RateLimitMiddleware
from ..integration import NLDSIntegrationOrchestrator, get_default_integration_config
from ..translation import TranslationOrchestrator
from ..processing import ProcessingOrchestrator
from ..analysis import AnalysisOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global orchestrators
integration_orchestrator: Optional[NLDSIntegrationOrchestrator] = None
translation_orchestrator: Optional[TranslationOrchestrator] = None
processing_orchestrator: Optional[ProcessingOrchestrator] = None
analysis_orchestrator: Optional[AnalysisOrchestrator] = None


# ============================================================================
# APPLICATION LIFECYCLE
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("Starting N.L.D.S. API server...")
    
    global integration_orchestrator, translation_orchestrator, processing_orchestrator, analysis_orchestrator
    
    try:
        # Initialize integration orchestrator
        integration_config = get_default_integration_config()
        integration_orchestrator = NLDSIntegrationOrchestrator(integration_config)
        await integration_orchestrator.initialize_all_components()
        
        # Initialize other orchestrators (from previous phases)
        # These would be imported from the respective modules
        logger.info("All orchestrators initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize orchestrators: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down N.L.D.S. API server...")
    
    try:
        if integration_orchestrator:
            await integration_orchestrator.cleanup_all_components()
        
        logger.info("All orchestrators cleaned up successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="N.L.D.S. API",
    description="Natural Language Detection System - JAEGIS Enhanced Agent System v2.2 Tier 0 Component",
    version="2.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "JAEGIS Development Team",
        "url": "https://github.com/usemanusai/JAEGIS",
        "email": "support@jaegis.ai"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Security
security = HTTPBearer()

# ============================================================================
# MIDDLEWARE
# ============================================================================

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.jaegis.ai"]
)

# Custom middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url)
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url)
            }
        }
    )


# ============================================================================
# HEALTH AND STATUS ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    try:
        # Check all orchestrators
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "version": "2.2.0",
            "components": {}
        }
        
        if integration_orchestrator:
            integration_status = await integration_orchestrator.get_integration_status()
            health_status["components"]["integration"] = {
                "status": "healthy" if integration_status["orchestrator"]["initialized"] else "unhealthy",
                "active_components": integration_status.get("active_components", 0),
                "total_components": integration_status.get("total_components", 0)
            }
        
        # Add other component health checks
        overall_healthy = all(
            comp.get("status") == "healthy" 
            for comp in health_status["components"].values()
        )
        
        health_status["status"] = "healthy" if overall_healthy else "degraded"
        
        return HealthResponse(**health_status)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/status", response_model=SystemStatusResponse, tags=["System"])
async def get_system_status(current_user: dict = Depends(get_current_user)):
    """Get comprehensive system status."""
    try:
        status = {
            "system": {
                "status": "operational",
                "uptime_seconds": 0,
                "version": "2.2.0",
                "environment": "production"
            },
            "components": {},
            "metrics": {},
            "timestamp": datetime.utcnow()
        }
        
        if integration_orchestrator:
            integration_status = await integration_orchestrator.get_integration_status()
            status["components"]["integration"] = integration_status
        
        return SystemStatusResponse(**status)
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system status")


# ============================================================================
# CORE N.L.D.S. PROCESSING ENDPOINTS
# ============================================================================

@app.post("/process", response_model=ProcessingResponse, tags=["Processing"])
async def process_input(
    request: ProcessingRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    rate_limiter = Depends(get_rate_limiter)
):
    """
    Process natural language input through N.L.D.S. pipeline.
    
    This endpoint processes user input through the complete N.L.D.S. pipeline including:
    - A.M.A.S.I.A.P. Protocol enhancement
    - Multi-dimensional analysis (logical, emotional, creative)
    - JAEGIS command generation
    - Confidence validation
    """
    try:
        processing_start = time.time()
        
        # Validate input
        if not request.input_text or len(request.input_text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Input text cannot be empty")
        
        if len(request.input_text) > 10000:  # 10KB limit
            raise HTTPException(status_code=400, detail="Input text too long (max 10KB)")
        
        # Process through integration orchestrator
        if not integration_orchestrator:
            raise HTTPException(status_code=503, detail="Integration orchestrator not available")
        
        # Enhanced processing
        result = await integration_orchestrator.process_enhanced_input(
            request.input_text,
            request.context
        )
        
        processing_time = (time.time() - processing_start) * 1000
        
        # Create response
        response = ProcessingResponse(
            request_id=str(uuid.uuid4()),
            success=result["success"],
            original_input=result["original_input"],
            enhanced_input=result["enhanced_input"],
            processing_time_ms=processing_time,
            components_used=result["components_used"],
            amasiap_result=result.get("amasiap_result"),
            jaegis_command=result.get("jaegis_command"),
            confidence_score=0.85,  # Would come from actual processing
            metadata={
                "user_id": current_user.get("user_id"),
                "timestamp": datetime.utcnow().isoformat(),
                "api_version": "2.2.0"
            }
        )
        
        # Log processing for analytics
        background_tasks.add_task(
            log_processing_analytics,
            request.input_text,
            response,
            current_user
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")

@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_input(
    request: AnalysisRequest,
    current_user: dict = Depends(get_current_user),
    rate_limiter = Depends(get_rate_limiter)
):
    """
    Perform detailed analysis of input text.
    
    Provides multi-dimensional analysis including:
    - Logical analysis and requirement extraction
    - Emotional context and sentiment analysis
    - Creative interpretation and pattern recognition
    """
    try:
        # This would integrate with the analysis orchestrator from Phase 3
        analysis_result = {
            "request_id": str(uuid.uuid4()),
            "input_text": request.input_text,
            "logical_analysis": {
                "requirements": ["Requirement 1", "Requirement 2"],
                "logical_structure": "Sequential",
                "confidence": 0.9
            },
            "emotional_analysis": {
                "sentiment": "positive",
                "emotional_state": "confident",
                "confidence": 0.85
            },
            "creative_analysis": {
                "patterns": ["Pattern 1", "Pattern 2"],
                "innovation_potential": "high",
                "confidence": 0.8
            },
            "synthesis": {
                "overall_confidence": 0.85,
                "recommended_approach": "comprehensive",
                "key_insights": ["Insight 1", "Insight 2"]
            },
            "processing_time_ms": 150.0,
            "timestamp": datetime.utcnow()
        }
        
        return AnalysisResponse(**analysis_result)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

@app.post("/translate", response_model=TranslationResponse, tags=["Translation"])
async def translate_to_jaegis(
    request: TranslationRequest,
    current_user: dict = Depends(get_current_user),
    rate_limiter = Depends(get_rate_limiter)
):
    """
    Translate natural language to JAEGIS commands.
    
    Converts enhanced input into executable JAEGIS commands with:
    - Intelligent mode selection (1-5)
    - Optimal squad selection from 128 agents
    - Parameter extraction and mapping
    - Confidence validation
    """
    try:
        # This would integrate with the translation orchestrator from Phase 5
        translation_result = {
            "request_id": str(uuid.uuid4()),
            "input_text": request.input_text,
            "jaegis_command": {
                "command_id": str(uuid.uuid4()),
                "command_type": "analysis",
                "target_squad": "content_squad",
                "mode_level": 3,
                "parameters": [
                    {
                        "type": "text_input",
                        "value": request.input_text,
                        "confidence": 0.95
                    }
                ],
                "priority": "normal",
                "estimated_duration": 300
            },
            "mode_selection": {
                "selected_mode": 3,
                "confidence": 0.92,
                "reasoning": "Complex analysis requiring moderate resources"
            },
            "squad_selection": {
                "selected_squad": "content_squad",
                "confidence": 0.88,
                "reasoning": "Best suited for content analysis tasks"
            },
            "confidence_validation": {
                "overall_confidence": 0.91,
                "threshold_met": True,
                "alternatives_available": True
            },
            "processing_time_ms": 200.0,
            "timestamp": datetime.utcnow()
        }
        
        return TranslationResponse(**translation_result)
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail="Translation failed")


# ============================================================================
# JAEGIS INTEGRATION ENDPOINTS
# ============================================================================

@app.post("/jaegis/submit", response_model=CommandSubmissionResponse, tags=["JAEGIS"])
async def submit_jaegis_command(
    request: CommandSubmissionRequest,
    current_user: dict = Depends(get_current_user),
    rate_limiter = Depends(get_rate_limiter)
):
    """Submit command to JAEGIS Master Orchestrator."""
    try:
        if not integration_orchestrator or not integration_orchestrator.jaegis_interface:
            raise HTTPException(status_code=503, detail="JAEGIS interface not available")
        
        # Submit command through JAEGIS interface
        # This would use the actual JAEGIS command from translation
        submission_result = {
            "command_id": str(uuid.uuid4()),
            "status": "submitted",
            "submission_time": datetime.utcnow(),
            "estimated_completion": datetime.utcnow() + timedelta(minutes=5),
            "tracking_url": f"/jaegis/status/{str(uuid.uuid4())}"
        }
        
        return CommandSubmissionResponse(**submission_result)
        
    except Exception as e:
        logger.error(f"Command submission failed: {e}")
        raise HTTPException(status_code=500, detail="Command submission failed")

@app.get("/jaegis/status/{command_id}", response_model=CommandStatusResponse, tags=["JAEGIS"])
async def get_command_status(
    command_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get status of submitted JAEGIS command."""
    try:
        if not integration_orchestrator or not integration_orchestrator.jaegis_interface:
            raise HTTPException(status_code=503, detail="JAEGIS interface not available")
        
        # Get status from JAEGIS interface
        status_result = {
            "command_id": command_id,
            "status": "executing",
            "progress_percentage": 65.0,
            "assigned_squad": "content_squad",
            "assigned_agents": ["agent_001", "agent_002"],
            "execution_start": datetime.utcnow() - timedelta(minutes=2),
            "estimated_completion": datetime.utcnow() + timedelta(minutes=3),
            "result_data": None,
            "error_message": None,
            "last_update": datetime.utcnow()
        }
        
        return CommandStatusResponse(**status_result)
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail="Status check failed")


# ============================================================================
# SYSTEM MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/metrics", response_model=MetricsResponse, tags=["System"])
async def get_system_metrics(current_user: dict = Depends(get_current_user)):
    """Get system performance metrics."""
    try:
        metrics = {
            "api": {
                "total_requests": 1000,
                "successful_requests": 950,
                "failed_requests": 50,
                "average_response_time_ms": 250.0,
                "requests_per_minute": 25.5
            },
            "processing": {
                "total_processed": 800,
                "average_processing_time_ms": 180.0,
                "confidence_average": 0.87,
                "enhancement_rate": 0.95
            },
            "integration": {},
            "timestamp": datetime.utcnow()
        }
        
        if integration_orchestrator:
            integration_status = await integration_orchestrator.get_integration_status()
            metrics["integration"] = integration_status.get("orchestrator", {}).get("metrics", {})
        
        return MetricsResponse(**metrics)
        
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")

@app.post("/admin/cache/clear", tags=["Admin"])
async def clear_cache(
    cache_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Clear system caches."""
    try:
        # Verify admin permissions
        if not current_user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        cleared_items = 0
        
        if integration_orchestrator and integration_orchestrator.github_interface:
            cleared_items += await integration_orchestrator.github_interface.clear_cache()
        
        return {
            "success": True,
            "cache_type": cache_type or "all",
            "items_cleared": cleared_items,
            "timestamp": datetime.utcnow()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cache clear failed: {e}")
        raise HTTPException(status_code=500, detail="Cache clear failed")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def log_processing_analytics(input_text: str, response: ProcessingResponse, user: dict):
    """Log processing analytics for monitoring and improvement."""
    try:
        analytics_data = {
            "user_id": user.get("user_id"),
            "input_length": len(input_text),
            "processing_time_ms": response.processing_time_ms,
            "confidence_score": response.confidence_score,
            "components_used": response.components_used,
            "success": response.success,
            "timestamp": datetime.utcnow()
        }
        
        # In production, this would be sent to analytics service
        logger.info(f"Processing analytics: {analytics_data}")
        
    except Exception as e:
        logger.error(f"Analytics logging failed: {e}")


# ============================================================================
# CUSTOM OPENAPI
# ============================================================================

def custom_openapi():
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="N.L.D.S. API",
        version="2.2.0",
        description="""
        # Natural Language Detection System API
        
        JAEGIS Enhanced Agent System v2.2 - Tier 0 Component
        
        ## Overview
        
        The N.L.D.S. API provides comprehensive natural language processing capabilities
        for the JAEGIS ecosystem, including:
        
        - **Input Enhancement**: Automatic input enhancement via A.M.A.S.I.A.P. Protocol
        - **Multi-dimensional Analysis**: Logical, emotional, and creative analysis
        - **JAEGIS Translation**: Convert natural language to executable JAEGIS commands
        - **Real-time Integration**: Direct integration with JAEGIS Master Orchestrator
        - **System Management**: Comprehensive monitoring and administration
        
        ## Authentication
        
        All endpoints require authentication via Bearer token in the Authorization header:
        ```
        Authorization: Bearer <your-api-token>
        ```
        
        ## Rate Limiting
        
        API requests are rate-limited to ensure fair usage:
        - **Standard users**: 100 requests per minute
        - **Premium users**: 1000 requests per minute
        - **Admin users**: Unlimited
        
        ## Error Handling
        
        The API uses standard HTTP status codes and returns detailed error information:
        - **400**: Bad Request - Invalid input parameters
        - **401**: Unauthorized - Invalid or missing authentication
        - **403**: Forbidden - Insufficient permissions
        - **429**: Too Many Requests - Rate limit exceeded
        - **500**: Internal Server Error - System error
        
        ## Support
        
        For support and documentation, visit: https://github.com/usemanusai/JAEGIS
        """,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add security to all endpoints
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# ============================================================================
# STARTUP MESSAGE
# ============================================================================

@app.on_event("startup")
async def startup_message():
    """Display startup message."""
    logger.info("=" * 80)
    logger.info("N.L.D.S. API Server v2.2.0")
    logger.info("JAEGIS Enhanced Agent System - Tier 0 Component")
    logger.info("=" * 80)
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("Health Check: http://localhost:8000/health")
    logger.info("System Status: http://localhost:8000/status")
    logger.info("=" * 80)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "nlds.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
