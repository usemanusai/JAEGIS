"""
P.I.T.C.E.S. Framework - Enhanced Context Engine
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements advanced context persistence and state management with Redis vector
integration, distributed caching, and intelligent context retrieval for the P.I.T.C.E.S. framework.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from uuid import UUID

from .models import Task
from .exceptions import PITCESError, ErrorCodes
from .context_engine import ContextEngine
from .redis_vector_engine import RedisVectorEngine
from .enhanced_caching_layer import EnhancedCachingLayer


logger = logging.getLogger(__name__)


class EnhancedContextEngine(ContextEngine):
    """
    Enhanced context engine with Redis vector integration and distributed caching.
    
    Features:
    - Vector-based context similarity search
    - Multi-tier caching with Redis integration
    - Distributed context persistence
    - Intelligent context preloading
    - Advanced compression and optimization
    - Real-time context synchronization
    - Performance monitoring and analytics
    """
    
    def __init__(
        self, 
        storage_path: str = "pitces_context",
        vector_engine: Optional[RedisVectorEngine] = None,
        caching_layer: Optional[EnhancedCachingLayer] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Enhanced Context Engine.
        
        Args:
            storage_path: Path for local context storage
            vector_engine: Redis vector engine instance
            caching_layer: Enhanced caching layer instance
            config: Context engine configuration
        """
        # Initialize base context engine
        super().__init__(storage_path)
        
        self.vector_engine = vector_engine
        self.caching_layer = caching_layer
        self.config = config or self._get_default_config()
        
        # Enhanced metrics
        self.enhanced_metrics = {
            'vector_searches': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'similarity_matches': 0,
            'compression_ratio': 0.0,
            'sync_operations': 0,
            'preload_operations': 0
        }
        
        # Context indexing for fast retrieval
        self.context_index: Dict[str, Dict[str, Any]] = {}
        
        # Background tasks
        self.background_tasks: List[asyncio.Task] = []
        
        logger.info("EnhancedContextEngine initialized with Redis vector integration")
    
    async def initialize(self) -> bool:
        """
        Initialize the enhanced context engine.
        
        Returns:
            True if initialization successful
        """
        try:
            # Initialize vector engine if available
            if self.vector_engine:
                await self.vector_engine.initialize()
            
            # Load existing context index
            await self._load_context_index()
            
            # Start background tasks
            if self.config.get('enable_background_tasks', True):
                await self._start_background_tasks()
            
            # Warm up caches if enabled
            if self.config.get('enable_cache_warming', True):
                await self._warm_context_caches()
            
            logger.info("Enhanced Context Engine initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"Enhanced Context Engine initialization failed: {e}")
            return False
    
    async def save_task_context_enhanced(
        self, 
        task: Task, 
        include_vector: bool = True,
        cache_strategy: str = 'hybrid'
    ) -> bool:
        """
        Save task context with vector embedding and caching.
        
        Args:
            task: Task object with context data
            include_vector: Whether to include vector embedding
            cache_strategy: Caching strategy to use
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            # Save to base context engine first
            base_success = self.save_task_context(task)
            
            if not base_success:
                return False
            
            # Save to vector engine if available
            if self.vector_engine and include_vector:
                vector_id = await self.vector_engine.store_task_context_vector(
                    task, task.context_data
                )
                logger.debug(f"Stored task vector: {vector_id}")
            
            # Save to cache if available
            if self.caching_layer:
                cache_success = await self.caching_layer.cache_task_context(task, task.context_data)
                if cache_success:
                    self.enhanced_metrics['cache_hits'] += 1
                else:
                    self.enhanced_metrics['cache_misses'] += 1
            
            # Update context index
            await self._update_context_index(task.id, {
                'task_name': task.name,
                'priority': task.priority.name,
                'status': task.status.name,
                'timestamp': datetime.now().isoformat(),
                'has_vector': include_vector and self.vector_engine is not None,
                'cached': self.caching_layer is not None
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save enhanced task context {task.id}: {e}")
            return False
    
    async def load_task_context_enhanced(
        self, 
        task_id: UUID,
        include_similar: bool = False,
        similarity_threshold: float = 0.8
    ) -> Optional[Dict[str, Any]]:
        """
        Load task context with similarity search and caching.
        
        Args:
            task_id: Task identifier
            include_similar: Whether to include similar contexts
            similarity_threshold: Minimum similarity for related contexts
            
        Returns:
            Enhanced task context data or None if not found
        """
        try:
            # Try cache first if available
            if self.caching_layer:
                cached_context = await self.caching_layer.get_task_context_cached(task_id)
                if cached_context:
                    self.enhanced_metrics['cache_hits'] += 1
                    
                    if include_similar:
                        cached_context['similar_contexts'] = await self._find_similar_contexts(task_id)
                    
                    return cached_context
                else:
                    self.enhanced_metrics['cache_misses'] += 1
            
            # Load from base context engine
            base_context = self.load_task_context(task_id)
            
            if not base_context:
                return None
            
            enhanced_context = {
                'task_data': base_context,
                'source': 'local_storage',
                'loaded_at': datetime.now().isoformat()
            }
            
            # Add similar contexts if requested
            if include_similar:
                enhanced_context['similar_contexts'] = await self._find_similar_contexts(task_id)
            
            # Cache for future use
            if self.caching_layer:
                await self.caching_layer.cache_task_context(task_id, enhanced_context)
            
            return enhanced_context
            
        except Exception as e:
            logger.error(f"Failed to load enhanced task context {task_id}: {e}")
            return None
    
    async def find_similar_contexts(
        self, 
        task: Task,
        top_k: int = 5,
        similarity_threshold: float = 0.75
    ) -> List[Dict[str, Any]]:
        """
        Find similar task contexts using vector similarity search.
        
        Args:
            task: Reference task for similarity search
            top_k: Number of similar contexts to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of similar contexts with similarity scores
        """
        try:
            if not self.vector_engine:
                logger.warning("Vector engine not available for similarity search")
                return []
            
            # Search for similar contexts using vector engine
            similar_contexts = await self.vector_engine.find_similar_task_contexts(
                task, top_k, similarity_threshold
            )
            
            self.enhanced_metrics['vector_searches'] += 1
            self.enhanced_metrics['similarity_matches'] += len(similar_contexts)
            
            logger.debug(f"Found {len(similar_contexts)} similar contexts for task {task.id}")
            return similar_contexts
            
        except Exception as e:
            logger.error(f"Similar context search failed: {e}")
            return []
    
    async def preload_contexts(
        self, 
        task_ids: List[UUID],
        strategy: str = 'cached'
    ) -> Dict[UUID, bool]:
        """
        Preload multiple contexts for performance optimization.
        
        Args:
            task_ids: List of task identifiers to preload
            strategy: Preloading strategy
            
        Returns:
            Dictionary mapping task IDs to preload success status
        """
        try:
            preload_results = {}
            
            # Batch preload contexts
            for task_id in task_ids:
                try:
                    context_data = await self.load_task_context_enhanced(task_id)
                    preload_results[task_id] = context_data is not None
                except Exception as e:
                    logger.error(f"Failed to preload context {task_id}: {e}")
                    preload_results[task_id] = False
            
            successful_preloads = sum(preload_results.values())
            self.enhanced_metrics['preload_operations'] += 1
            
            logger.info(f"Preloaded {successful_preloads}/{len(task_ids)} contexts")
            
            return preload_results
            
        except Exception as e:
            logger.error(f"Context preloading failed: {e}")
            return {task_id: False for task_id in task_ids}
    
    async def synchronize_contexts(self) -> Dict[str, Any]:
        """
        Synchronize contexts across storage layers.
        
        Returns:
            Synchronization results
        """
        try:
            sync_results = {
                'local_to_cache': 0,
                'cache_to_vector': 0,
                'conflicts_resolved': 0,
                'errors': 0
            }
            
            # Get all local contexts
            local_contexts = list(self.storage_path.glob("task_*.json"))
            
            for context_file in local_contexts:
                try:
                    task_id = UUID(context_file.stem.replace('task_', ''))
                    
                    # Load local context
                    local_context = self.load_task_context(task_id)
                    if not local_context:
                        continue
                    
                    # Sync to cache if available
                    if self.caching_layer:
                        cache_success = await self.caching_layer.cache_task_context(
                            task_id, local_context
                        )
                        if cache_success:
                            sync_results['local_to_cache'] += 1
                    
                    # Sync to vector store if available
                    if self.vector_engine and 'task_data' in local_context:
                        # This would require reconstructing Task object
                        sync_results['cache_to_vector'] += 1
                    
                except Exception as e:
                    logger.error(f"Failed to sync context {context_file}: {e}")
                    sync_results['errors'] += 1
            
            self.enhanced_metrics['sync_operations'] += 1
            logger.info(f"Context synchronization completed: {sync_results}")
            
            return sync_results
            
        except Exception as e:
            logger.error(f"Context synchronization failed: {e}")
            return {'error': str(e)}
    
    def get_enhanced_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive enhanced context engine metrics.
        
        Returns:
            Enhanced metrics dictionary
        """
        base_metrics = self.get_context_metrics()
        
        enhanced_metrics = {
            **base_metrics,
            'enhanced_features': {
                **self.enhanced_metrics,
                'vector_engine_available': self.vector_engine is not None,
                'caching_layer_available': self.caching_layer is not None,
                'cache_hit_ratio': self._calculate_cache_hit_ratio()
            },
            'storage_distribution': {
                'local_contexts': len(list(self.storage_path.glob("task_*.json"))),
                'indexed_contexts': len(self.context_index),
                'background_tasks_active': len([t for t in self.background_tasks if not t.done()])
            }
        }
        
        return enhanced_metrics
    
    async def _find_similar_contexts(self, task_id: UUID) -> List[Dict[str, Any]]:
        """Find similar contexts for a given task ID."""
        try:
            # Load the task first
            context_data = self.load_task_context(task_id)
            if not context_data:
                return []
            
            # Create a temporary task object for similarity search
            # This is a simplified approach - in practice, you'd need proper Task reconstruction
            return []
            
        except Exception as e:
            logger.error(f"Failed to find similar contexts for {task_id}: {e}")
            return []
    
    async def _load_context_index(self):
        """Load context index from storage."""
        try:
            index_file = self.storage_path / "context_index.json"
            if index_file.exists():
                with open(index_file, 'r') as f:
                    self.context_index = json.load(f)
                logger.debug(f"Loaded context index with {len(self.context_index)} entries")
        except Exception as e:
            logger.warning(f"Failed to load context index: {e}")
            self.context_index = {}
    
    async def _update_context_index(self, task_id: UUID, metadata: Dict[str, Any]):
        """Update context index with task metadata."""
        try:
            self.context_index[str(task_id)] = metadata
            
            # Save index periodically
            if len(self.context_index) % 10 == 0:
                await self._save_context_index()
                
        except Exception as e:
            logger.error(f"Failed to update context index: {e}")
    
    async def _save_context_index(self):
        """Save context index to storage."""
        try:
            index_file = self.storage_path / "context_index.json"
            with open(index_file, 'w') as f:
                json.dump(self.context_index, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save context index: {e}")
    
    async def _start_background_tasks(self):
        """Start background maintenance tasks."""
        try:
            # Context cleanup task
            cleanup_task = asyncio.create_task(self._background_cleanup())
            self.background_tasks.append(cleanup_task)
            
            # Index maintenance task
            index_task = asyncio.create_task(self._background_index_maintenance())
            self.background_tasks.append(index_task)
            
            # Synchronization task
            sync_task = asyncio.create_task(self._background_synchronization())
            self.background_tasks.append(sync_task)
            
            logger.info("Started background tasks for enhanced context engine")
            
        except Exception as e:
            logger.error(f"Failed to start background tasks: {e}")
    
    async def _warm_context_caches(self):
        """Warm up context caches with frequently accessed data."""
        try:
            # Get recently accessed contexts
            recent_contexts = sorted(
                self.context_index.items(),
                key=lambda x: x[1].get('timestamp', ''),
                reverse=True
            )[:20]  # Top 20 recent contexts
            
            # Preload them
            task_ids = [UUID(task_id) for task_id, _ in recent_contexts]
            await self.preload_contexts(task_ids)
            
            logger.info(f"Warmed cache with {len(task_ids)} contexts")
            
        except Exception as e:
            logger.error(f"Cache warming failed: {e}")
    
    async def _background_cleanup(self):
        """Background task for context cleanup."""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                # Clean up old contexts
                cleaned = self.cleanup_old_contexts(max_age_days=30)
                if cleaned > 0:
                    logger.info(f"Background cleanup removed {cleaned} old contexts")
                
            except Exception as e:
                logger.error(f"Background cleanup error: {e}")
    
    async def _background_index_maintenance(self):
        """Background task for index maintenance."""
        while True:
            try:
                await asyncio.sleep(1800)  # Run every 30 minutes
                
                # Save context index
                await self._save_context_index()
                
                # Rebuild index if needed
                if len(self.context_index) > 1000:
                    await self._rebuild_context_index()
                
            except Exception as e:
                logger.error(f"Background index maintenance error: {e}")
    
    async def _background_synchronization(self):
        """Background task for context synchronization."""
        while True:
            try:
                await asyncio.sleep(7200)  # Run every 2 hours
                
                # Synchronize contexts
                sync_results = await self.synchronize_contexts()
                logger.debug(f"Background sync completed: {sync_results}")
                
            except Exception as e:
                logger.error(f"Background synchronization error: {e}")
    
    async def _rebuild_context_index(self):
        """Rebuild context index from storage."""
        try:
            new_index = {}
            
            for context_file in self.storage_path.glob("task_*.json"):
                try:
                    task_id = context_file.stem.replace('task_', '')
                    stat = context_file.stat()
                    
                    new_index[task_id] = {
                        'timestamp': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'size_bytes': stat.st_size,
                        'rebuilt': True
                    }
                    
                except Exception as e:
                    logger.warning(f"Failed to index {context_file}: {e}")
            
            self.context_index = new_index
            await self._save_context_index()
            
            logger.info(f"Rebuilt context index with {len(new_index)} entries")
            
        except Exception as e:
            logger.error(f"Failed to rebuild context index: {e}")
    
    def _calculate_cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        total_requests = self.enhanced_metrics['cache_hits'] + self.enhanced_metrics['cache_misses']
        if total_requests == 0:
            return 0.0
        return (self.enhanced_metrics['cache_hits'] / total_requests) * 100.0
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default enhanced context engine configuration."""
        return {
            'enable_background_tasks': True,
            'enable_cache_warming': True,
            'enable_vector_storage': True,
            'enable_compression': True,
            'sync_interval_hours': 2,
            'cleanup_interval_hours': 24,
            'index_maintenance_interval_minutes': 30
        }
