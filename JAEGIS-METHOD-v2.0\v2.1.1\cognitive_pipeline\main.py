"""
JAEGIS Cognitive Ingestion & Synthesis Pipeline - Main Application
FastAPI-based service for converting unstructured information into structured training data

This is the main entry point for the cognitive pipeline system, implementing
the foundational tier with multi-source ingestion capabilities.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
import asyncio
import logging
import time
from datetime import datetime
import uuid

# Import cognitive pipeline modules
from cognitive_pipeline.ingestion.multi_source_ingester import MultiSourceIngester
from cognitive_pipeline.processing.content_processor import ContentProcessor
from cognitive_pipeline.orchestration.llm_orchestrator import LLMOrchestrator
from cognitive_pipeline.generation.training_data_generator import TrainingDataGenerator
from cognitive_pipeline.storage.data_manager import DataManager
from cognitive_pipeline.models.pipeline_models import (
    IngestionRequest, IngestionResponse, ProcessingStatus,
    ContentStructure, QuizData, FlashcardData, SummaryData
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="JAEGIS Cognitive Ingestion & Synthesis Pipeline",
    description="Convert unstructured information into structured, interactive training data for AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
multi_source_ingester = MultiSourceIngester()
content_processor = ContentProcessor()
llm_orchestrator = LLMOrchestrator()
training_data_generator = TrainingDataGenerator()
data_manager = DataManager()

# Global processing status tracking
processing_jobs: Dict[str, Dict[str, Any]] = {}


class IngestionRequest(BaseModel):
    """Request model for content ingestion."""
    source_type: str  # "youtube", "pdf", "url", "file"
    source_url: Optional[HttpUrl] = None
    content_text: Optional[str] = None
    processing_options: Dict[str, Any] = {}
    user_id: Optional[str] = None


class IngestionResponse(BaseModel):
    """Response model for content ingestion."""
    job_id: str
    status: str
    message: str
    estimated_completion_time: Optional[int] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the cognitive pipeline system on startup."""
    
    logger.info("🧠 JAEGIS Cognitive Pipeline - Starting Up")
    
    # Initialize all components
    await multi_source_ingester.initialize()
    await content_processor.initialize()
    await llm_orchestrator.initialize()
    await training_data_generator.initialize()
    await data_manager.initialize()
    
    logger.info("✅ Cognitive Pipeline - Ready for Operations")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    
    logger.info("🔄 Cognitive Pipeline - Shutting Down")
    
    # Clean up all components
    await multi_source_ingester.cleanup()
    await content_processor.cleanup()
    await llm_orchestrator.cleanup()
    await training_data_generator.cleanup()
    await data_manager.cleanup()
    
    logger.info("✅ Cognitive Pipeline - Shutdown Complete")


@app.get("/")
async def root():
    """Root endpoint with system status."""
    
    return {
        "service": "JAEGIS Cognitive Ingestion & Synthesis Pipeline",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "capabilities": [
            "multi_source_ingestion",
            "content_structuring",
            "quiz_generation",
            "flashcard_generation",
            "summarization_with_tts",
            "smart_llm_selection"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    
    # Check component health
    component_health = {
        "multi_source_ingester": await multi_source_ingester.health_check(),
        "content_processor": await content_processor.health_check(),
        "llm_orchestrator": await llm_orchestrator.health_check(),
        "training_data_generator": await training_data_generator.health_check(),
        "data_manager": await data_manager.health_check()
    }
    
    overall_health = all(component_health.values())
    
    return {
        "status": "healthy" if overall_health else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": component_health
    }


@app.post("/ingest", response_model=IngestionResponse)
async def ingest_content(
    request: IngestionRequest,
    background_tasks: BackgroundTasks
):
    """
    Main ingestion endpoint for all content types.
    
    Supports:
    - YouTube URLs
    - PDF documents
    - Web page URLs
    - Direct text content
    """
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job tracking
    processing_jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "source_type": request.source_type,
        "source_url": str(request.source_url) if request.source_url else None,
        "created_at": time.time(),
        "progress": 0,
        "stages_completed": [],
        "current_stage": "queued",
        "results": {}
    }
    
    # Add background processing task
    background_tasks.add_task(
        process_content_pipeline,
        job_id,
        request
    )
    
    logger.info(f"📥 Content ingestion started - Job ID: {job_id}")
    
    return IngestionResponse(
        job_id=job_id,
        status="queued",
        message="Content ingestion job queued for processing",
        estimated_completion_time=300  # 5 minutes estimate
    )


@app.post("/ingest/file")
async def ingest_file(
    file: UploadFile = File(...),
    processing_options: str = "{}",
    background_tasks: BackgroundTasks = None
):
    """
    File upload ingestion endpoint.
    
    Supports:
    - PDF documents
    - Audio/video files
    - Text files
    """
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = await data_manager.save_uploaded_file(file, job_id)
    
    # Create ingestion request
    request = IngestionRequest(
        source_type="file",
        content_text=file_path,
        processing_options=eval(processing_options) if processing_options else {}
    )
    
    # Initialize job tracking
    processing_jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "source_type": "file",
        "file_name": file.filename,
        "file_path": file_path,
        "created_at": time.time(),
        "progress": 0,
        "stages_completed": [],
        "current_stage": "queued",
        "results": {}
    }
    
    # Add background processing task
    background_tasks.add_task(
        process_content_pipeline,
        job_id,
        request
    )
    
    logger.info(f"📁 File ingestion started - Job ID: {job_id}, File: {file.filename}")
    
    return IngestionResponse(
        job_id=job_id,
        status="queued",
        message=f"File '{file.filename}' queued for processing",
        estimated_completion_time=300
    )


@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Get processing status for a specific job."""
    
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = processing_jobs[job_id]
    
    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job["progress"],
        "current_stage": job["current_stage"],
        "stages_completed": job["stages_completed"],
        "created_at": job["created_at"],
        "processing_time": time.time() - job["created_at"] if job["status"] != "completed" else None,
        "results_available": len(job["results"]) > 0
    }


@app.get("/results/{job_id}")
async def get_job_results(job_id: str):
    """Get processing results for a completed job."""
    
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = processing_jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not yet completed")
    
    return {
        "job_id": job_id,
        "status": job["status"],
        "results": job["results"],
        "processing_summary": {
            "total_processing_time": job.get("total_processing_time", 0),
            "stages_completed": job["stages_completed"],
            "content_quality_score": job["results"].get("quality_score", 0)
        }
    }


@app.get("/jobs")
async def list_jobs(status: Optional[str] = None, limit: int = 50):
    """List processing jobs with optional status filter."""
    
    jobs = list(processing_jobs.values())
    
    if status:
        jobs = [job for job in jobs if job["status"] == status]
    
    # Sort by creation time (newest first)
    jobs.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "total_jobs": len(jobs),
        "jobs": jobs[:limit]
    }


async def process_content_pipeline(job_id: str, request: IngestionRequest):
    """
    Main content processing pipeline.
    
    Stages:
    1. Content Ingestion
    2. Content Structuring
    3. LLM Analysis
    4. Training Data Generation
    5. Audio Processing (if applicable)
    6. Storage & Indexing
    """
    
    job = processing_jobs[job_id]
    
    try:
        # Stage 1: Content Ingestion
        job["current_stage"] = "ingestion"
        job["status"] = "processing"
        job["progress"] = 10
        
        logger.info(f"🔄 Job {job_id}: Starting content ingestion")
        
        ingestion_result = await multi_source_ingester.ingest_content(
            source_type=request.source_type,
            source_url=str(request.source_url) if request.source_url else None,
            content_text=request.content_text,
            options=request.processing_options
        )
        
        job["stages_completed"].append("ingestion")
        job["progress"] = 25
        
        # Stage 2: Content Structuring
        job["current_stage"] = "structuring"
        job["progress"] = 30
        
        logger.info(f"🔄 Job {job_id}: Starting content structuring")
        
        structure_result = await content_processor.structure_content(
            raw_content=ingestion_result["content"],
            metadata=ingestion_result["metadata"]
        )
        
        job["stages_completed"].append("structuring")
        job["progress"] = 50
        
        # Stage 3: LLM Analysis
        job["current_stage"] = "llm_analysis"
        job["progress"] = 55
        
        logger.info(f"🔄 Job {job_id}: Starting LLM analysis")
        
        analysis_result = await llm_orchestrator.analyze_content(
            structured_content=structure_result,
            analysis_types=["summarization", "key_concepts", "thesis_analysis"]
        )
        
        job["stages_completed"].append("llm_analysis")
        job["progress"] = 75
        
        # Stage 4: Training Data Generation
        job["current_stage"] = "training_data_generation"
        job["progress"] = 80
        
        logger.info(f"🔄 Job {job_id}: Starting training data generation")
        
        training_data = await training_data_generator.generate_training_data(
            content=structure_result,
            analysis=analysis_result,
            generation_types=["quiz", "flashcards", "scenarios"]
        )
        
        job["stages_completed"].append("training_data_generation")
        job["progress"] = 90
        
        # Stage 5: Storage & Indexing
        job["current_stage"] = "storage"
        job["progress"] = 95
        
        logger.info(f"🔄 Job {job_id}: Starting storage and indexing")
        
        storage_result = await data_manager.store_results(
            job_id=job_id,
            ingestion_result=ingestion_result,
            structure_result=structure_result,
            analysis_result=analysis_result,
            training_data=training_data
        )
        
        job["stages_completed"].append("storage")
        job["progress"] = 100
        
        # Complete job
        job["status"] = "completed"
        job["current_stage"] = "completed"
        job["total_processing_time"] = time.time() - job["created_at"]
        
        # Store results
        job["results"] = {
            "content_structure": structure_result,
            "analysis": analysis_result,
            "training_data": training_data,
            "storage_info": storage_result,
            "quality_score": analysis_result.get("quality_score", 85)
        }
        
        logger.info(f"✅ Job {job_id}: Processing completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Job {job_id}: Processing failed - {str(e)}")
        
        job["status"] = "failed"
        job["current_stage"] = "error"
        job["error_message"] = str(e)
        job["total_processing_time"] = time.time() - job["created_at"]


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
