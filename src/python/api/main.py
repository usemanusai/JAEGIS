#!/usr/bin/env python3
"""
JAEGIS Python API Service
GitHub Integration and Markdown Processing Service

@version 2.0.0
@author JAEGIS Development Team
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
import structlog

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from python.github.client import GitHubClient
from python.processing.markdown import MarkdownProcessor
from python.processing.commands import CommandExtractor
from python.utils.logger import setup_logger
from python.utils.config import load_config
from python.utils.cache import CacheManager
from python.utils.metrics import MetricsCollector

# Setup structured logging
setup_logger()
logger = structlog.get_logger(__name__)

# Pydantic models for API requests/responses
class GitHubFetchRequest(BaseModel):
    url: str = Field(..., description="GitHub raw content URL")
    cache: bool = Field(True, description="Whether to cache the result")
    parse: bool = Field(False, description="Whether to parse the content")

class ParseCommandsRequest(BaseModel):
    content: str = Field(..., description="Markdown content to parse")
    format: str = Field("markdown", description="Content format")
    extract_metadata: bool = Field(True, description="Extract metadata")

class AnalyzeContentRequest(BaseModel):
    content: str = Field(..., description="Content to analyze")
    options: Dict[str, Any] = Field(default_factory=dict, description="Analysis options")

class ValidateCommandRequest(BaseModel):
    command: str = Field(..., description="Command to validate")
    commands_data: Optional[Dict] = Field(None, description="Commands data for validation")
    strict: bool = Field(True, description="Strict validation mode")

class SuggestionsRequest(BaseModel):
    query: str = Field(..., description="Query for suggestions")
    context: Dict[str, Any] = Field(default_factory=dict, description="Context data")
    max_suggestions: int = Field(10, description="Maximum number of suggestions")

class CacheClearRequest(BaseModel):
    pattern: Optional[str] = Field(None, description="Cache key pattern to clear")

class ScriptExecuteRequest(BaseModel):
    script: str = Field(..., description="Python script to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Script parameters")
    timeout: int = Field(60000, description="Execution timeout in milliseconds")

# Global services
github_client: Optional[GitHubClient] = None
markdown_processor: Optional[MarkdownProcessor] = None
command_extractor: Optional[CommandExtractor] = None
cache_manager: Optional[CacheManager] = None
metrics_collector: Optional[MetricsCollector] = None
config: Dict = {}

# FastAPI app
app = FastAPI(
    title="JAEGIS Python Intelligence API",
    description="GitHub Integration and Markdown Processing Service",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses."""
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Response-Time"] = f"{process_time:.3f}s"
    
    # Record metrics
    if metrics_collector:
        await metrics_collector.record_request(
            method=request.method,
            endpoint=str(request.url.path),
            status_code=response.status_code,
            duration=process_time
        )
    
    return response

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global github_client, markdown_processor, command_extractor, cache_manager, metrics_collector, config
    
    logger.info("🚀 Starting JAEGIS Python API Service...")
    
    try:
        # Load configuration
        config = load_config()
        logger.info("⚙️ Configuration loaded")
        
        # Initialize cache manager
        cache_manager = CacheManager(config.get('cache', {}))
        await cache_manager.initialize()
        logger.info("💾 Cache manager initialized")
        
        # Initialize GitHub client
        github_client = GitHubClient(config.get('github', {}))
        await github_client.initialize()
        logger.info("🌐 GitHub client initialized")
        
        # Initialize markdown processor
        markdown_processor = MarkdownProcessor(config.get('processing', {}))
        await markdown_processor.initialize()
        logger.info("📝 Markdown processor initialized")
        
        # Initialize command extractor
        command_extractor = CommandExtractor(config.get('commands', {}))
        await command_extractor.initialize()
        logger.info("🎯 Command extractor initialized")
        
        # Initialize metrics collector
        metrics_collector = MetricsCollector(config.get('metrics', {}))
        await metrics_collector.initialize()
        logger.info("📊 Metrics collector initialized")
        
        logger.info("✅ JAEGIS Python API Service started successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to start service: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 Shutting down JAEGIS Python API Service...")
    
    if github_client:
        await github_client.cleanup()
    if markdown_processor:
        await markdown_processor.cleanup()
    if command_extractor:
        await command_extractor.cleanup()
    if cache_manager:
        await cache_manager.cleanup()
    if metrics_collector:
        await metrics_collector.cleanup()
    
    logger.info("✅ Shutdown complete")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "services": {
                "github_client": await github_client.health_check() if github_client else {"status": "not_initialized"},
                "cache_manager": await cache_manager.health_check() if cache_manager else {"status": "not_initialized"},
                "markdown_processor": {"status": "healthy"} if markdown_processor else {"status": "not_initialized"},
                "command_extractor": {"status": "healthy"} if command_extractor else {"status": "not_initialized"},
                "metrics_collector": {"status": "healthy"} if metrics_collector else {"status": "not_initialized"}
            }
        }
        
        # Check if all services are healthy
        all_healthy = all(
            service.get("status") == "healthy" 
            for service in health_status["services"].values()
        )
        
        if not all_healthy:
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Test endpoint
@app.get("/test")
async def test_connection():
    """Test connection endpoint."""
    return {
        "success": True,
        "message": "JAEGIS Python API is running",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# GitHub endpoints
@app.post("/github/fetch")
async def fetch_github_content(request: GitHubFetchRequest):
    """Fetch content from GitHub."""
    try:
        logger.info(f"📥 Fetching GitHub content: {request.url}")
        
        if not github_client:
            raise HTTPException(status_code=503, detail="GitHub client not initialized")
        
        # Check cache first if enabled
        cache_key = f"github_content:{request.url}"
        if request.cache and cache_manager:
            cached_content = await cache_manager.get(cache_key)
            if cached_content:
                logger.info("📋 Using cached GitHub content")
                return {
                    "success": True,
                    "data": cached_content,
                    "cached": True,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Fetch from GitHub
        content = await github_client.fetch_content(request.url)
        
        # Cache the result if enabled
        if request.cache and cache_manager:
            await cache_manager.set(cache_key, content, ttl=3600)  # Cache for 1 hour
        
        # Parse if requested
        if request.parse and markdown_processor:
            parsed_content = await markdown_processor.parse(content["content"])
            content["parsed"] = parsed_content
        
        return {
            "success": True,
            "data": content,
            "cached": False,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"GitHub fetch error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub content: {str(e)}")

# Processing endpoints
@app.post("/processing/parse-commands")
async def parse_commands(request: ParseCommandsRequest):
    """Parse commands from markdown content."""
    try:
        logger.info("📝 Parsing commands from content")
        
        if not command_extractor:
            raise HTTPException(status_code=503, detail="Command extractor not initialized")
        
        # Extract commands
        commands = await command_extractor.extract_commands(
            content=request.content,
            format=request.format,
            extract_metadata=request.extract_metadata
        )
        
        return {
            "success": True,
            "data": commands,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Command parsing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse commands: {str(e)}")

@app.post("/processing/analyze")
async def analyze_content(request: AnalyzeContentRequest):
    """Analyze content structure and extract information."""
    try:
        logger.info("🔍 Analyzing content")
        
        if not markdown_processor:
            raise HTTPException(status_code=503, detail="Markdown processor not initialized")
        
        # Analyze content
        analysis = await markdown_processor.analyze(
            content=request.content,
            options=request.options
        )
        
        return {
            "success": True,
            "data": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Content analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze content: {str(e)}")

@app.post("/processing/validate")
async def validate_command(request: ValidateCommandRequest):
    """Validate a command against available commands."""
    try:
        logger.info(f"✅ Validating command: {request.command}")
        
        if not command_extractor:
            raise HTTPException(status_code=503, detail="Command extractor not initialized")
        
        # Validate command
        validation = await command_extractor.validate_command(
            command=request.command,
            commands_data=request.commands_data,
            strict=request.strict
        )
        
        return {
            "success": True,
            "data": validation,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Command validation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to validate command: {str(e)}")

# AI endpoints
@app.post("/ai/suggestions")
async def generate_suggestions(request: SuggestionsRequest):
    """Generate command suggestions based on query."""
    try:
        logger.info(f"💡 Generating suggestions for: {request.query}")
        
        if not command_extractor:
            raise HTTPException(status_code=503, detail="Command extractor not initialized")
        
        # Generate suggestions
        suggestions = await command_extractor.generate_suggestions(
            query=request.query,
            context=request.context,
            max_suggestions=request.max_suggestions
        )
        
        return {
            "success": True,
            "data": suggestions,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Suggestion generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate suggestions: {str(e)}")

@app.post("/ai/process")
async def process_ai_request(request: Dict[str, Any]):
    """Process AI request."""
    try:
        logger.info("🤖 Processing AI request")
        
        # Placeholder for AI processing
        # This can be extended with actual AI/ML models
        
        return {
            "success": True,
            "data": {
                "message": "AI processing not yet implemented",
                "request": request
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"AI processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process AI request: {str(e)}")

# Cache endpoints
@app.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics."""
    try:
        if not cache_manager:
            raise HTTPException(status_code=503, detail="Cache manager not initialized")
        
        stats = await cache_manager.get_stats()
        
        return {
            "success": True,
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cache stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache stats: {str(e)}")

@app.post("/cache/clear")
async def clear_cache(request: CacheClearRequest):
    """Clear cache entries."""
    try:
        if not cache_manager:
            raise HTTPException(status_code=503, detail="Cache manager not initialized")
        
        cleared = await cache_manager.clear(pattern=request.pattern)
        
        return {
            "success": True,
            "data": {
                "cleared_entries": cleared,
                "pattern": request.pattern
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

# Metrics endpoint
@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics():
    """Get Prometheus-style metrics."""
    try:
        if not metrics_collector:
            return "# Metrics collector not initialized\n"
        
        metrics = await metrics_collector.get_prometheus_metrics()
        return metrics
        
    except Exception as e:
        logger.error(f"Metrics error: {e}")
        return f"# Error getting metrics: {str(e)}\n"

# Script execution endpoint
@app.post("/execute/script")
async def execute_script(request: ScriptExecuteRequest):
    """Execute Python script safely."""
    try:
        logger.info("📜 Executing Python script")
        
        # This is a placeholder for safe script execution
        # In production, this should use a sandboxed environment
        
        return {
            "success": True,
            "data": {
                "message": "Script execution not yet implemented for security reasons",
                "script_length": len(request.script),
                "parameters": request.parameters
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Script execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to execute script: {str(e)}")

# Shutdown endpoint
@app.post("/shutdown")
async def shutdown_service(background_tasks: BackgroundTasks):
    """Graceful shutdown endpoint."""
    logger.info("🛑 Shutdown requested")
    
    def shutdown():
        import signal
        import os
        os.kill(os.getpid(), signal.SIGTERM)
    
    background_tasks.add_task(shutdown)
    
    return {
        "success": True,
        "message": "Shutdown initiated",
        "timestamp": datetime.now().isoformat()
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("JAEGIS_HOST", "localhost")
    port = int(os.getenv("JAEGIS_PORT", "5000"))
    log_level = os.getenv("JAEGIS_LOG_LEVEL", "info")
    
    logger.info(f"🚀 Starting JAEGIS Python API on {host}:{port}")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=False,
        access_log=True
    )