"""
P.I.T.C.E.S. Context Engine
Parallel Integrated Task Contexting Engine System

This module implements persistent state management with JSON serialization and file locking.
"""

import json
import logging
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import UUID

from .exceptions import ContextEngineError, ErrorCodes
from .models import Task, TaskStatus


logger = logging.getLogger(__name__)


class ContextEngine:
    """
    Persistent state management system with thread-safe operations and file locking.
    
    Handles serialization and deserialization of task contexts, workflow states,
    and system metadata with atomic operations and corruption protection.
    """
    
    def __init__(self, storage_path: str = "pitces_context", lock_timeout: float = 30.0):
        """
        Initialize the context engine.
        
        Args:
            storage_path: Directory path for context storage
            lock_timeout: Maximum time to wait for file locks (seconds)
        """
        self.storage_path = Path(storage_path)
        self.lock_timeout = lock_timeout
        self._locks: Dict[str, threading.Lock] = {}
        self._lock_registry_lock = threading.Lock()
        
        # Ensure storage directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize metadata
        self._metadata_file = self.storage_path / "metadata.json"
        self._initialize_metadata()
        
        logger.info(f"ContextEngine initialized with storage path: {self.storage_path}")
    
    def save_task_context(self, task: Task) -> bool:
        """
        Save task context to persistent storage with atomic operations.
        
        Args:
            task: Task object to serialize and save
        
        Returns:
            bool: True if save successful, False otherwise
        
        Raises:
            ContextEngineError: If save operation fails
        """
        try:
            task_file = self.storage_path / f"task_{task.id}.json"
            
            # Serialize task data
            task_data = self._serialize_task(task)
            
            # Add metadata
            context_data = {
                'task_data': task_data,
                'saved_at': datetime.utcnow().isoformat(),
                'version': '1.0',
                'checksum': self._calculate_checksum(task_data)
            }
            
            # Atomic write with file locking
            with self._get_file_lock(str(task_file)):
                self._atomic_write(task_file, context_data)
            
            # Update metadata
            self._update_task_metadata(task.id, task.status, task.name)
            
            logger.debug(f"Task context saved: {task.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save task context for {task.id}: {e}")
            raise ContextEngineError(
                message=f"Failed to save task context",
                error_code=ErrorCodes.CONTEXT_SAVE_FAILURE,
                context={'task_id': str(task.id), 'error': str(e)}
            )
    
    def load_task_context(self, task_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Load task context from persistent storage with validation.
        
        Args:
            task_id: UUID of task to load
        
        Returns:
            Optional[Dict]: Task context data or None if not found
        
        Raises:
            ContextEngineError: If load operation fails or data is corrupted
        """
        try:
            task_file = self.storage_path / f"task_{task_id}.json"
            
            if not task_file.exists():
                logger.debug(f"Task context not found: {task_id}")
                return None
            
            # Load with file locking
            with self._get_file_lock(str(task_file)):
                with open(task_file, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
            
            # Validate data integrity
            if not self._validate_context_data(context_data):
                raise ContextEngineError(
                    message="Context data validation failed",
                    error_code=ErrorCodes.CONTEXT_CORRUPTION,
                    context={'task_id': str(task_id)}
                )
            
            logger.debug(f"Task context loaded: {task_id}")
            return context_data['task_data']
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error loading task {task_id}: {e}")
            raise ContextEngineError(
                message="Context data is corrupted (invalid JSON)",
                error_code=ErrorCodes.CONTEXT_CORRUPTION,
                context={'task_id': str(task_id), 'json_error': str(e)}
            )
        except Exception as e:
            logger.error(f"Failed to load task context for {task_id}: {e}")
            raise ContextEngineError(
                message="Failed to load task context",
                error_code=ErrorCodes.CONTEXT_LOAD_FAILURE,
                context={'task_id': str(task_id), 'error': str(e)}
            )
    
    def delete_task_context(self, task_id: UUID) -> bool:
        """
        Delete task context from persistent storage.
        
        Args:
            task_id: UUID of task to delete
        
        Returns:
            bool: True if deletion successful, False if not found
        """
        try:
            task_file = self.storage_path / f"task_{task_id}.json"
            
            if not task_file.exists():
                return False
            
            # Delete with file locking
            with self._get_file_lock(str(task_file)):
                task_file.unlink()
            
            # Update metadata
            self._remove_task_metadata(task_id)
            
            logger.debug(f"Task context deleted: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete task context for {task_id}: {e}")
            return False
    
    def list_saved_tasks(self) -> Dict[str, Dict[str, Any]]:
        """
        List all saved task contexts with metadata.
        
        Returns:
            Dict: Mapping of task_id to metadata
        """
        try:
            with self._get_file_lock(str(self._metadata_file)):
                with open(self._metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            
            return metadata.get('tasks', {})
            
        except Exception as e:
            logger.error(f"Failed to list saved tasks: {e}")
            return {}
    
    def cleanup_old_contexts(self, max_age_days: int = 30) -> int:
        """
        Clean up old context files to prevent storage bloat.
        
        Args:
            max_age_days: Maximum age of context files to keep
        
        Returns:
            int: Number of files cleaned up
        """
        try:
            cleanup_count = 0
            cutoff_time = time.time() - (max_age_days * 24 * 3600)
            
            for task_file in self.storage_path.glob("task_*.json"):
                if task_file.stat().st_mtime < cutoff_time:
                    try:
                        task_id = UUID(task_file.stem.replace("task_", ""))
                        if self.delete_task_context(task_id):
                            cleanup_count += 1
                    except ValueError:
                        # Invalid UUID in filename, skip
                        continue
            
            logger.info(f"Cleaned up {cleanup_count} old context files")
            return cleanup_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup old contexts: {e}")
            return 0
    
    def _serialize_task(self, task: Task) -> Dict[str, Any]:
        """Serialize task object to JSON-compatible dictionary."""
        return {
            'id': str(task.id),
            'name': task.name,
            'priority': task.priority.value,
            'status': task.status.value,
            'dependencies': task.dependencies,
            'estimated_duration': task.estimated_duration.total_seconds(),
            'context_data': task.context_data,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'assigned_agent': task.assigned_agent,
            'completion_percentage': task.completion_percentage,
            'error_message': task.error_message
        }
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate simple checksum for data integrity validation."""
        import hashlib
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _validate_context_data(self, context_data: Dict[str, Any]) -> bool:
        """Validate context data integrity."""
        required_fields = ['task_data', 'saved_at', 'version', 'checksum']
        
        if not all(field in context_data for field in required_fields):
            return False
        
        # Validate checksum
        expected_checksum = self._calculate_checksum(context_data['task_data'])
        return context_data['checksum'] == expected_checksum
    
    def _atomic_write(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Perform atomic write operation to prevent corruption."""
        temp_file = file_path.with_suffix('.tmp')
        
        try:
            # Write to temporary file first
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Atomic move to final location
            temp_file.replace(file_path)
            
        except Exception:
            # Clean up temporary file on error
            if temp_file.exists():
                temp_file.unlink()
            raise
    
    def _get_file_lock(self, file_path: str) -> threading.Lock:
        """Get or create a file-specific lock."""
        with self._lock_registry_lock:
            if file_path not in self._locks:
                self._locks[file_path] = threading.Lock()
            return self._locks[file_path]
    
    def _initialize_metadata(self) -> None:
        """Initialize metadata file if it doesn't exist."""
        if not self._metadata_file.exists():
            metadata = {
                'created_at': datetime.utcnow().isoformat(),
                'version': '1.0',
                'tasks': {}
            }
            self._atomic_write(self._metadata_file, metadata)
    
    def _update_task_metadata(self, task_id: UUID, status: TaskStatus, name: str) -> None:
        """Update task metadata in the metadata file."""
        try:
            with self._get_file_lock(str(self._metadata_file)):
                with open(self._metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                metadata['tasks'][str(task_id)] = {
                    'name': name,
                    'status': status.name,
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                self._atomic_write(self._metadata_file, metadata)
                
        except Exception as e:
            logger.warning(f"Failed to update task metadata: {e}")
    
    def _remove_task_metadata(self, task_id: UUID) -> None:
        """Remove task metadata from the metadata file."""
        try:
            with self._get_file_lock(str(self._metadata_file)):
                with open(self._metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                metadata['tasks'].pop(str(task_id), None)
                
                self._atomic_write(self._metadata_file, metadata)
                
        except Exception as e:
            logger.warning(f"Failed to remove task metadata: {e}")
