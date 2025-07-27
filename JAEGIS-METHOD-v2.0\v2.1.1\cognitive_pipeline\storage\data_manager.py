"""
JAEGIS Cognitive Pipeline - Data Manager
Storage, indexing, and retrieval for all pipeline data

This module implements comprehensive data management capabilities
including vector storage, relational data, and file management.
"""

import asyncio
import aiofiles
import logging
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import tempfile
import uuid

from cognitive_pipeline.models.pipeline_models import (
    PipelineResult, IngestionResult, ContentStructure,
    QuizData, FlashcardData, TrainingScenario, SummaryData
)

logger = logging.getLogger(__name__)


class DataStorageError(Exception):
    """Custom exception for data storage errors."""
    pass


class DataManager:
    """
    Comprehensive data management system for the cognitive pipeline.
    
    Provides:
    - Vector database integration for embeddings
    - Relational database for metadata and relationships
    - File storage for media and documents
    - Search and retrieval capabilities
    - Data versioning and backup
    """
    
    def __init__(self):
        self.vector_db = None
        self.relational_db = None
        self.file_storage = None
        self.search_engine = None
        
        # Configuration
        self.storage_config = {
            "base_path": Path("./data"),
            "vector_db_path": Path("./data/vector_db"),
            "relational_db_path": Path("./data/relational.db"),
            "file_storage_path": Path("./data/files"),
            "temp_path": Path("./data/temp"),
            "backup_path": Path("./data/backups")
        }
        
        # Ensure directories exist
        for path in self.storage_config.values():
            if isinstance(path, Path):
                path.mkdir(parents=True, exist_ok=True)
        
        # Storage statistics
        self.storage_stats = {
            "total_documents": 0,
            "total_size_bytes": 0,
            "vector_embeddings": 0,
            "relational_records": 0,
            "file_objects": 0
        }
        
        logger.info("DataManager initialized")
    
    async def initialize(self):
        """Initialize data management components."""
        
        logger.info("🔄 Initializing Data Manager")
        
        # Initialize vector database
        self.vector_db = VectorDatabase(self.storage_config["vector_db_path"])
        await self.vector_db.initialize()
        
        # Initialize relational database
        self.relational_db = RelationalDatabase(self.storage_config["relational_db_path"])
        await self.relational_db.initialize()
        
        # Initialize file storage
        self.file_storage = FileStorage(self.storage_config["file_storage_path"])
        await self.file_storage.initialize()
        
        # Initialize search engine
        self.search_engine = SearchEngine(self.vector_db, self.relational_db)
        await self.search_engine.initialize()
        
        # Load storage statistics
        await self._load_storage_stats()
        
        logger.info("✅ Data Manager ready")
    
    async def cleanup(self):
        """Clean up resources."""
        
        if self.vector_db:
            await self.vector_db.cleanup()
        if self.relational_db:
            await self.relational_db.cleanup()
        if self.file_storage:
            await self.file_storage.cleanup()
        if self.search_engine:
            await self.search_engine.cleanup()
    
    async def health_check(self) -> bool:
        """Check health of data management components."""
        
        try:
            checks = [
                self.vector_db.health_check() if self.vector_db else True,
                self.relational_db.health_check() if self.relational_db else True,
                self.file_storage.health_check() if self.file_storage else True,
                self.search_engine.health_check() if self.search_engine else True
            ]
            
            results = await asyncio.gather(*checks, return_exceptions=True)
            return all(result is True for result in results)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def store_results(
        self,
        job_id: str,
        ingestion_result: IngestionResult,
        structure_result: ContentStructure,
        analysis_result: Dict[str, Any],
        training_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Store complete pipeline results.
        
        Args:
            job_id: Unique job identifier
            ingestion_result: Content ingestion results
            structure_result: Structured content
            analysis_result: LLM analysis results
            training_data: Generated training data
        
        Returns:
            Dict containing storage information and references
        """
        
        logger.info(f"🔄 Storing pipeline results for job: {job_id}")
        
        try:
            storage_info = {
                "job_id": job_id,
                "storage_timestamp": datetime.utcnow().isoformat(),
                "storage_references": {},
                "file_references": {},
                "vector_references": {},
                "search_indices": []
            }
            
            # Store content structure in relational database
            content_ref = await self.relational_db.store_content_structure(structure_result)
            storage_info["storage_references"]["content_structure"] = content_ref
            
            # Store analysis results
            analysis_ref = await self.relational_db.store_analysis_results(job_id, analysis_result)
            storage_info["storage_references"]["analysis_results"] = analysis_ref
            
            # Store training data
            training_refs = await self._store_training_data(job_id, training_data)
            storage_info["storage_references"]["training_data"] = training_refs
            
            # Generate and store vector embeddings
            vector_refs = await self._store_vector_embeddings(structure_result, analysis_result)
            storage_info["vector_references"] = vector_refs
            
            # Store any file attachments
            file_refs = await self._store_file_attachments(job_id, ingestion_result)
            storage_info["file_references"] = file_refs
            
            # Create search indices
            search_indices = await self.search_engine.create_indices(job_id, structure_result, training_data)
            storage_info["search_indices"] = search_indices
            
            # Update storage statistics
            await self._update_storage_stats(storage_info)
            
            # Create pipeline result record
            pipeline_result = PipelineResult(
                job_id=job_id,
                source_info=ingestion_result,
                content_structure=structure_result,
                quiz_data=training_data.get("quiz"),
                flashcard_data=training_data.get("flashcards"),
                scenarios=training_data.get("scenarios", []),
                summary_data=training_data.get("summary"),
                processing_metadata=analysis_result,
                completed_at=datetime.utcnow()
            )
            
            # Store complete pipeline result
            result_ref = await self.relational_db.store_pipeline_result(pipeline_result)
            storage_info["storage_references"]["pipeline_result"] = result_ref
            
            logger.info(f"✅ Pipeline results stored successfully for job: {job_id}")
            
            return storage_info
            
        except Exception as e:
            logger.error(f"❌ Failed to store pipeline results for job {job_id}: {e}")
            raise DataStorageError(f"Failed to store results: {str(e)}")
    
    async def retrieve_results(self, job_id: str) -> Optional[PipelineResult]:
        """Retrieve complete pipeline results by job ID."""
        
        try:
            return await self.relational_db.retrieve_pipeline_result(job_id)
        except Exception as e:
            logger.error(f"Failed to retrieve results for job {job_id}: {e}")
            return None
    
    async def search_content(
        self,
        query: str,
        content_types: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search stored content using vector similarity and text search."""
        
        try:
            return await self.search_engine.search(query, content_types, limit)
        except Exception as e:
            logger.error(f"Search failed for query '{query}': {e}")
            return []
    
    async def save_uploaded_file(self, file, job_id: str) -> str:
        """Save uploaded file and return file path."""
        
        try:
            # Generate unique filename
            file_extension = Path(file.filename).suffix if file.filename else ""
            unique_filename = f"{job_id}_{uuid.uuid4().hex}{file_extension}"
            file_path = self.storage_config["temp_path"] / unique_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            logger.info(f"File saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save uploaded file: {e}")
            raise DataStorageError(f"Failed to save file: {str(e)}")
    
    async def _store_training_data(self, job_id: str, training_data: Dict[str, Any]) -> Dict[str, str]:
        """Store training data components."""
        
        refs = {}
        
        for data_type, data in training_data.items():
            if data_type == "quiz" and data:
                ref = await self.relational_db.store_quiz_data(data)
                refs["quiz"] = ref
            
            elif data_type == "flashcards" and data:
                ref = await self.relational_db.store_flashcard_data(data)
                refs["flashcards"] = ref
            
            elif data_type == "scenarios" and data:
                ref = await self.relational_db.store_scenarios(data)
                refs["scenarios"] = ref
            
            elif data_type == "summary" and data:
                ref = await self.relational_db.store_summary_data(data)
                refs["summary"] = ref
        
        return refs
    
    async def _store_vector_embeddings(
        self,
        content: ContentStructure,
        analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate and store vector embeddings."""
        
        refs = {}
        
        # Store content embeddings
        content_embedding_ref = await self.vector_db.store_content_embedding(content)
        refs["content"] = content_embedding_ref
        
        # Store chapter embeddings
        chapter_refs = []
        for chapter in content.chapters:
            chapter_ref = await self.vector_db.store_chapter_embedding(chapter)
            chapter_refs.append(chapter_ref)
        refs["chapters"] = chapter_refs
        
        # Store analysis embeddings
        if "key_concepts" in analysis:
            concepts_ref = await self.vector_db.store_concepts_embedding(analysis["key_concepts"])
            refs["concepts"] = concepts_ref
        
        return refs
    
    async def _store_file_attachments(self, job_id: str, ingestion_result: IngestionResult) -> Dict[str, str]:
        """Store file attachments from ingestion."""
        
        refs = {}
        
        # Check for audio files
        metadata = ingestion_result.metadata
        if hasattr(metadata, 'audio_path') and metadata.audio_path:
            audio_ref = await self.file_storage.store_file(metadata.audio_path, f"{job_id}_audio")
            refs["audio"] = audio_ref
        
        # Check for other file references
        processing_info = ingestion_result.processing_info
        if "file_path" in processing_info:
            file_ref = await self.file_storage.store_file(processing_info["file_path"], f"{job_id}_source")
            refs["source_file"] = file_ref
        
        return refs
    
    async def _load_storage_stats(self):
        """Load storage statistics."""
        
        try:
            stats_file = self.storage_config["base_path"] / "storage_stats.json"
            if stats_file.exists():
                async with aiofiles.open(stats_file, 'r') as f:
                    content = await f.read()
                    self.storage_stats = json.loads(content)
        except Exception as e:
            logger.warning(f"Could not load storage stats: {e}")
    
    async def _update_storage_stats(self, storage_info: Dict[str, Any]):
        """Update storage statistics."""
        
        self.storage_stats["total_documents"] += 1
        self.storage_stats["relational_records"] += len(storage_info.get("storage_references", {}))
        self.storage_stats["vector_embeddings"] += len(storage_info.get("vector_references", {}))
        self.storage_stats["file_objects"] += len(storage_info.get("file_references", {}))
        
        # Save updated stats
        try:
            stats_file = self.storage_config["base_path"] / "storage_stats.json"
            async with aiofiles.open(stats_file, 'w') as f:
                await f.write(json.dumps(self.storage_stats, indent=2))
        except Exception as e:
            logger.warning(f"Could not save storage stats: {e}")
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get current storage statistics."""
        return self.storage_stats.copy()


# Component classes (simplified implementations)
class VectorDatabase:
    """Vector database for embeddings storage."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.embeddings = {}
    
    async def initialize(self):
        self.db_path.mkdir(parents=True, exist_ok=True)
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def store_content_embedding(self, content: ContentStructure) -> str:
        ref_id = f"content_{content.content_id}"
        # Simplified: would generate actual embeddings
        self.embeddings[ref_id] = {"type": "content", "id": content.content_id}
        return ref_id
    
    async def store_chapter_embedding(self, chapter) -> str:
        ref_id = f"chapter_{chapter.chapter_id}"
        self.embeddings[ref_id] = {"type": "chapter", "id": chapter.chapter_id}
        return ref_id
    
    async def store_concepts_embedding(self, concepts) -> str:
        ref_id = f"concepts_{uuid.uuid4().hex}"
        self.embeddings[ref_id] = {"type": "concepts", "data": concepts}
        return ref_id


class RelationalDatabase:
    """Relational database for metadata and relationships."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.records = {}
    
    async def initialize(self):
        # Would initialize actual database connection
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def store_content_structure(self, content: ContentStructure) -> str:
        ref_id = f"content_struct_{content.content_id}"
        self.records[ref_id] = content.dict()
        return ref_id
    
    async def store_analysis_results(self, job_id: str, analysis: Dict[str, Any]) -> str:
        ref_id = f"analysis_{job_id}"
        self.records[ref_id] = analysis
        return ref_id
    
    async def store_quiz_data(self, quiz_data) -> str:
        ref_id = f"quiz_{quiz_data.quiz_id}"
        self.records[ref_id] = quiz_data.dict()
        return ref_id
    
    async def store_flashcard_data(self, flashcard_data) -> str:
        ref_id = f"flashcards_{flashcard_data.flashcard_set_id}"
        self.records[ref_id] = flashcard_data.dict()
        return ref_id
    
    async def store_scenarios(self, scenarios) -> str:
        ref_id = f"scenarios_{uuid.uuid4().hex}"
        self.records[ref_id] = [s.dict() for s in scenarios]
        return ref_id
    
    async def store_summary_data(self, summary_data) -> str:
        ref_id = f"summary_{summary_data.summary_id}"
        self.records[ref_id] = summary_data.dict()
        return ref_id
    
    async def store_pipeline_result(self, result: PipelineResult) -> str:
        ref_id = f"pipeline_{result.job_id}"
        self.records[ref_id] = result.dict()
        return ref_id
    
    async def retrieve_pipeline_result(self, job_id: str) -> Optional[PipelineResult]:
        ref_id = f"pipeline_{job_id}"
        if ref_id in self.records:
            return PipelineResult(**self.records[ref_id])
        return None


class FileStorage:
    """File storage for media and documents."""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.file_registry = {}
    
    async def initialize(self):
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def store_file(self, source_path: str, ref_name: str) -> str:
        """Store file and return reference."""
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # Generate unique filename
        file_extension = source.suffix
        unique_filename = f"{ref_name}_{uuid.uuid4().hex}{file_extension}"
        dest_path = self.storage_path / unique_filename
        
        # Copy file (simplified)
        import shutil
        shutil.copy2(source, dest_path)
        
        ref_id = f"file_{ref_name}"
        self.file_registry[ref_id] = str(dest_path)
        
        return ref_id


class SearchEngine:
    """Search engine for content discovery."""
    
    def __init__(self, vector_db: VectorDatabase, relational_db: RelationalDatabase):
        self.vector_db = vector_db
        self.relational_db = relational_db
        self.search_indices = {}
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def create_indices(self, job_id: str, content: ContentStructure, training_data: Dict[str, Any]) -> List[str]:
        """Create search indices for content."""
        indices = []
        
        # Create content index
        content_index = f"content_index_{job_id}"
        self.search_indices[content_index] = {
            "type": "content",
            "title": content.title,
            "summary": content.summary,
            "key_concepts": content.key_concepts
        }
        indices.append(content_index)
        
        # Create training data indices
        if "quiz" in training_data:
            quiz_index = f"quiz_index_{job_id}"
            self.search_indices[quiz_index] = {
                "type": "quiz",
                "questions": len(training_data["quiz"].questions) if training_data["quiz"] else 0
            }
            indices.append(quiz_index)
        
        return indices
    
    async def search(self, query: str, content_types: Optional[List[str]], limit: int) -> List[Dict[str, Any]]:
        """Search content using query."""
        results = []
        
        # Simple text-based search (would use vector similarity in real implementation)
        query_lower = query.lower()
        
        for index_id, index_data in self.search_indices.items():
            if content_types and index_data["type"] not in content_types:
                continue
            
            # Check if query matches content
            if "title" in index_data and query_lower in index_data["title"].lower():
                results.append({
                    "index_id": index_id,
                    "type": index_data["type"],
                    "title": index_data.get("title", ""),
                    "relevance_score": 0.8
                })
            elif "summary" in index_data and query_lower in index_data["summary"].lower():
                results.append({
                    "index_id": index_id,
                    "type": index_data["type"],
                    "title": index_data.get("title", ""),
                    "relevance_score": 0.6
                })
        
        # Sort by relevance and limit results
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]
