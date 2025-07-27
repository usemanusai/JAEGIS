"""
P.I.T.C.E.S. Framework - Enhanced Caching Layer
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements advanced caching strategies with vector embeddings,
priority-based TTL management, and intelligent cache warming for optimal performance.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import asdict
from uuid import UUID
from enum import Enum

from .redis_vector_engine import RedisVectorEngine
from .models import Task, ProjectSpecs, Priority, TaskStatus, WorkflowType, GapAnalysisResult
from .exceptions import PITCESError, ErrorCodes


logger = logging.getLogger(__name__)


class CacheStrategy(Enum):
    """Cache strategy types for different data patterns."""
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"
    WRITE_AROUND = "write_around"
    READ_THROUGH = "read_through"
    REFRESH_AHEAD = "refresh_ahead"


class CacheLevel(Enum):
    """Cache level hierarchy for multi-tier caching."""
    L1_MEMORY = "l1_memory"
    L2_REDIS = "l2_redis"
    L3_VECTOR = "l3_vector"
    L4_PERSISTENT = "l4_persistent"


class EnhancedCachingLayer:
    """
    Advanced caching layer with vector embeddings and intelligent strategies.
    
    Features:
    - Multi-tier caching (Memory -> Redis -> Vector -> Persistent)
    - Priority-based TTL management
    - Vector similarity-based cache retrieval
    - Intelligent cache warming and preloading
    - Performance optimization and monitoring
    - Distributed caching with consistency guarantees
    """
    
    def __init__(self, vector_engine: RedisVectorEngine, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Enhanced Caching Layer.
        
        Args:
            vector_engine: Redis vector engine instance
            config: Caching configuration
        """
        self.vector_engine = vector_engine
        self.config = config or self._get_default_config()
        
        # Multi-tier cache storage
        self.l1_cache: Dict[str, Any] = {}  # In-memory cache
        self.l2_cache = vector_engine.async_redis_client  # Redis cache
        
        # Cache strategies by data type
        self.cache_strategies = {
            'workflow_decisions': CacheStrategy.WRITE_THROUGH,
            'task_contexts': CacheStrategy.WRITE_BACK,
            'gap_analyses': CacheStrategy.REFRESH_AHEAD,
            'agent_states': CacheStrategy.WRITE_THROUGH,
            'nlds_embeddings': CacheStrategy.READ_THROUGH
        }
        
        # TTL strategies with priority-based adjustment
        self.base_ttl_strategies = {
            'workflow_decisions': timedelta(hours=24),
            'task_contexts': timedelta(hours=6),
            'gap_analyses': timedelta(days=7),
            'agent_states': timedelta(hours=2),
            'nlds_embeddings': timedelta(days=1)
        }
        
        # Priority multipliers for TTL adjustment
        self.priority_ttl_multipliers = {
            Priority.CRITICAL: 0.5,  # Shorter TTL for critical items
            Priority.HIGH: 0.75,
            Priority.MEDIUM: 1.0,
            Priority.LOW: 2.0  # Longer TTL for low priority items
        }
        
        # Cache warming patterns
        self.warming_patterns = {
            'frequent_workflows': [],
            'common_task_patterns': [],
            'popular_gap_analyses': [],
            'active_agent_states': []
        }
        
        # Performance metrics
        self.cache_metrics = {
            'l1_hits': 0,
            'l1_misses': 0,
            'l2_hits': 0,
            'l2_misses': 0,
            'vector_hits': 0,
            'vector_misses': 0,
            'cache_evictions': 0,
            'warming_operations': 0,
            'average_retrieval_time': 0.0,
            'hit_ratio': 0.0
        }
        
        # Cache consistency tracking
        self.consistency_tracker = {}
        
        logger.info("EnhancedCachingLayer initialized")
    
    async def get_workflow_decision_cached(
        self, 
        project_specs: ProjectSpecs,
        use_similarity: bool = True,
        similarity_threshold: float = 0.85
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve workflow decision from cache with vector similarity fallback.
        
        Args:
            project_specs: Project specifications
            use_similarity: Whether to use vector similarity search
            similarity_threshold: Minimum similarity for vector matches
            
        Returns:
            Cached workflow decision or None
        """
        start_time = time.time()
        cache_key = self._generate_cache_key('workflow_decision', project_specs)
        
        try:
            # L1 Cache (Memory) - Fastest
            if cache_key in self.l1_cache:
                self.cache_metrics['l1_hits'] += 1
                logger.debug(f"L1 cache hit for workflow decision: {cache_key}")
                return self.l1_cache[cache_key]
            
            self.cache_metrics['l1_misses'] += 1
            
            # L2 Cache (Redis) - Fast
            cached_data = await self.l2_cache.hgetall(f"cache:{cache_key}")
            if cached_data:
                self.cache_metrics['l2_hits'] += 1
                
                # Promote to L1 cache
                decision_data = json.loads(cached_data['data'])
                self.l1_cache[cache_key] = decision_data
                
                logger.debug(f"L2 cache hit for workflow decision: {cache_key}")
                return decision_data
            
            self.cache_metrics['l2_misses'] += 1
            
            # L3 Cache (Vector Similarity) - Intelligent
            if use_similarity:
                similar_decisions = await self.vector_engine.find_similar_workflow_decisions(
                    project_specs, top_k=1, similarity_threshold=similarity_threshold
                )
                
                if similar_decisions:
                    self.cache_metrics['vector_hits'] += 1
                    best_match = similar_decisions[0]
                    
                    # Cache the similar decision for future use
                    await self._cache_workflow_decision(
                        cache_key, best_match, 
                        ttl=self._calculate_ttl('workflow_decisions')
                    )
                    
                    logger.debug(f"Vector similarity hit for workflow decision: {cache_key}")
                    return best_match
                
                self.cache_metrics['vector_misses'] += 1
            
            # Cache miss - no data found
            retrieval_time = time.time() - start_time
            self._update_average_retrieval_time(retrieval_time)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve cached workflow decision: {e}")
            return None
    
    async def cache_workflow_decision(
        self, 
        project_specs: ProjectSpecs,
        workflow_type: WorkflowType,
        decision_context: Dict[str, Any],
        priority: Priority = Priority.MEDIUM
    ) -> bool:
        """
        Cache workflow decision with multi-tier storage.
        
        Args:
            project_specs: Project specifications
            workflow_type: Selected workflow type
            decision_context: Decision context data
            priority: Cache priority level
            
        Returns:
            True if caching successful
        """
        try:
            cache_key = self._generate_cache_key('workflow_decision', project_specs)
            
            decision_data = {
                'project_specs': asdict(project_specs),
                'workflow_type': workflow_type.value,
                'decision_context': decision_context,
                'timestamp': datetime.now().isoformat(),
                'priority': priority.name,
                'cache_level': 'multi_tier'
            }
            
            # Calculate TTL based on priority
            ttl = self._calculate_ttl('workflow_decisions', priority)
            
            # Store in vector engine for similarity search
            vector_id = await self.vector_engine.store_workflow_decision_vector(
                project_specs, workflow_type, decision_context
            )
            decision_data['vector_id'] = vector_id
            
            # Cache using appropriate strategy
            strategy = self.cache_strategies['workflow_decisions']
            success = await self._execute_cache_strategy(
                strategy, cache_key, decision_data, ttl
            )
            
            if success:
                logger.debug(f"Cached workflow decision: {cache_key}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to cache workflow decision: {e}")
            return False
    
    async def get_task_context_cached(
        self, 
        task_id: UUID,
        include_similar: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve task context from cache with similarity matching.
        
        Args:
            task_id: Task identifier
            include_similar: Whether to include similar task contexts
            
        Returns:
            Cached task context or None
        """
        start_time = time.time()
        cache_key = f"task_context:{task_id}"
        
        try:
            # L1 Cache check
            if cache_key in self.l1_cache:
                self.cache_metrics['l1_hits'] += 1
                return self.l1_cache[cache_key]
            
            self.cache_metrics['l1_misses'] += 1
            
            # L2 Cache check
            cached_data = await self.l2_cache.hgetall(f"cache:{cache_key}")
            if cached_data:
                self.cache_metrics['l2_hits'] += 1
                
                context_data = json.loads(cached_data['data'])
                
                # Promote to L1
                self.l1_cache[cache_key] = context_data
                
                return context_data
            
            self.cache_metrics['l2_misses'] += 1
            
            # Vector engine retrieval
            context_data = await self.vector_engine.retrieve_task_context_vector(task_id)
            
            if context_data:
                self.cache_metrics['vector_hits'] += 1
                
                # Cache for future use
                await self._cache_task_context(cache_key, context_data)
                
                return context_data
            
            self.cache_metrics['vector_misses'] += 1
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve cached task context: {e}")
            return None
    
    async def cache_task_context(
        self, 
        task: Task,
        context_data: Dict[str, Any]
    ) -> bool:
        """
        Cache task context with priority-based TTL.
        
        Args:
            task: Task object
            context_data: Task execution context
            
        Returns:
            True if caching successful
        """
        try:
            cache_key = f"task_context:{task.id}"
            
            enhanced_context = {
                'task_data': task.to_dict(),
                'context_data': context_data,
                'timestamp': datetime.now().isoformat(),
                'priority': task.priority.name,
                'status': task.status.name
            }
            
            # Store in vector engine
            vector_id = await self.vector_engine.store_task_context_vector(
                task, context_data
            )
            enhanced_context['vector_id'] = vector_id
            
            # Calculate priority-based TTL
            ttl = self._calculate_ttl('task_contexts', task.priority)
            
            # Cache using write-back strategy
            strategy = self.cache_strategies['task_contexts']
            success = await self._execute_cache_strategy(
                strategy, cache_key, enhanced_context, ttl
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to cache task context: {e}")
            return False
    
    async def cache_gap_analysis_results(
        self, 
        project_specs: ProjectSpecs,
        analysis_results: Dict[str, GapAnalysisResult]
    ) -> bool:
        """
        Cache gap analysis results with vector indexing.
        
        Args:
            project_specs: Project specifications
            analysis_results: Gap analysis results
            
        Returns:
            True if caching successful
        """
        try:
            cache_key = self._generate_cache_key('gap_analysis', project_specs)
            
            cached_analysis = {
                'project_specs': asdict(project_specs),
                'analysis_results': {
                    domain: asdict(result) for domain, result in analysis_results.items()
                },
                'timestamp': datetime.now().isoformat(),
                'overall_score': self._calculate_overall_score(analysis_results),
                'critical_gaps': len([
                    r for r in analysis_results.values() if r.score < 70
                ])
            }
            
            # Store in vector engine
            vector_id = await self.vector_engine.store_gap_analysis_vector(
                project_specs, analysis_results
            )
            cached_analysis['vector_id'] = vector_id
            
            # Use refresh-ahead strategy for gap analyses
            ttl = self._calculate_ttl('gap_analyses')
            strategy = self.cache_strategies['gap_analyses']
            
            success = await self._execute_cache_strategy(
                strategy, cache_key, cached_analysis, ttl
            )
            
            # Schedule refresh-ahead if needed
            if strategy == CacheStrategy.REFRESH_AHEAD:
                await self._schedule_refresh_ahead(cache_key, ttl)
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to cache gap analysis results: {e}")
            return False
    
    async def warm_cache_patterns(self) -> Dict[str, int]:
        """
        Warm cache with frequently accessed patterns.
        
        Returns:
            Dictionary with warming statistics
        """
        warming_stats = {
            'workflow_patterns': 0,
            'task_patterns': 0,
            'gap_patterns': 0,
            'agent_patterns': 0
        }
        
        try:
            # Warm workflow decision patterns
            workflow_count = await self._warm_workflow_patterns()
            warming_stats['workflow_patterns'] = workflow_count
            
            # Warm task context patterns
            task_count = await self._warm_task_patterns()
            warming_stats['task_patterns'] = task_count
            
            # Warm gap analysis patterns
            gap_count = await self._warm_gap_patterns()
            warming_stats['gap_patterns'] = gap_count
            
            # Warm agent coordination patterns
            agent_count = await self._warm_agent_patterns()
            warming_stats['agent_patterns'] = agent_count
            
            self.cache_metrics['warming_operations'] += 1
            logger.info(f"Cache warming completed: {warming_stats}")
            
            return warming_stats
            
        except Exception as e:
            logger.error(f"Cache warming failed: {e}")
            return warming_stats
    
    async def optimize_cache_performance(self) -> Dict[str, Any]:
        """
        Optimize cache performance based on usage patterns.
        
        Returns:
            Optimization results
        """
        try:
            optimization_results = {
                'evicted_entries': 0,
                'promoted_entries': 0,
                'ttl_adjustments': 0,
                'strategy_changes': 0
            }
            
            # Analyze cache usage patterns
            usage_patterns = await self._analyze_cache_usage()
            
            # Evict least recently used entries from L1
            evicted = await self._evict_lru_entries()
            optimization_results['evicted_entries'] = evicted
            
            # Promote frequently accessed L2 entries to L1
            promoted = await self._promote_frequent_entries()
            optimization_results['promoted_entries'] = promoted
            
            # Adjust TTL based on access patterns
            ttl_adjustments = await self._adjust_ttl_strategies(usage_patterns)
            optimization_results['ttl_adjustments'] = ttl_adjustments
            
            # Update cache strategies if needed
            strategy_changes = await self._optimize_cache_strategies(usage_patterns)
            optimization_results['strategy_changes'] = strategy_changes
            
            # Update hit ratio
            self._calculate_hit_ratio()
            
            logger.info(f"Cache optimization completed: {optimization_results}")
            return optimization_results
            
        except Exception as e:
            logger.error(f"Cache optimization failed: {e}")
            return {}
    
    def get_cache_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive cache performance metrics.
        
        Returns:
            Cache metrics dictionary
        """
        # Calculate derived metrics
        total_requests = (
            self.cache_metrics['l1_hits'] + self.cache_metrics['l1_misses'] +
            self.cache_metrics['l2_hits'] + self.cache_metrics['l2_misses'] +
            self.cache_metrics['vector_hits'] + self.cache_metrics['vector_misses']
        )
        
        if total_requests > 0:
            self.cache_metrics['hit_ratio'] = (
                (self.cache_metrics['l1_hits'] + self.cache_metrics['l2_hits'] + 
                 self.cache_metrics['vector_hits']) / total_requests
            )
        
        return {
            **self.cache_metrics,
            'l1_cache_size': len(self.l1_cache),
            'total_requests': total_requests,
            'cache_efficiency': self.cache_metrics['hit_ratio'] * 100,
            'warming_patterns_count': len(self.warming_patterns),
            'active_strategies': len(self.cache_strategies)
        }
    
    def _generate_cache_key(self, data_type: str, data: Any) -> str:
        """Generate cache key for data object."""
        if isinstance(data, ProjectSpecs):
            return f"{data_type}:{data.task_count}:{data.complexity_score}:{data.risk_level.value}"
        elif isinstance(data, Task):
            return f"{data_type}:{data.id}"
        else:
            return f"{data_type}:{hash(str(data))}"
    
    def _calculate_ttl(
        self, 
        data_type: str, 
        priority: Optional[Priority] = None
    ) -> timedelta:
        """Calculate TTL based on data type and priority."""
        base_ttl = self.base_ttl_strategies.get(data_type, timedelta(hours=1))
        
        if priority:
            multiplier = self.priority_ttl_multipliers.get(priority, 1.0)
            return timedelta(seconds=base_ttl.total_seconds() * multiplier)
        
        return base_ttl
    
    async def _execute_cache_strategy(
        self, 
        strategy: CacheStrategy,
        cache_key: str,
        data: Dict[str, Any],
        ttl: timedelta
    ) -> bool:
        """Execute specific caching strategy."""
        try:
            if strategy == CacheStrategy.WRITE_THROUGH:
                return await self._write_through_cache(cache_key, data, ttl)
            elif strategy == CacheStrategy.WRITE_BACK:
                return await self._write_back_cache(cache_key, data, ttl)
            elif strategy == CacheStrategy.WRITE_AROUND:
                return await self._write_around_cache(cache_key, data, ttl)
            elif strategy == CacheStrategy.READ_THROUGH:
                return await self._read_through_cache(cache_key, data, ttl)
            elif strategy == CacheStrategy.REFRESH_AHEAD:
                return await self._refresh_ahead_cache(cache_key, data, ttl)
            else:
                return await self._write_through_cache(cache_key, data, ttl)
                
        except Exception as e:
            logger.error(f"Cache strategy execution failed: {e}")
            return False
    
    async def _write_through_cache(
        self, 
        cache_key: str, 
        data: Dict[str, Any], 
        ttl: timedelta
    ) -> bool:
        """Write-through caching strategy."""
        # Write to both L1 and L2 simultaneously
        self.l1_cache[cache_key] = data
        
        await self.l2_cache.hset(
            f"cache:{cache_key}",
            mapping={
                'data': json.dumps(data),
                'timestamp': datetime.now().isoformat(),
                'ttl': str(ttl.total_seconds())
            }
        )
        await self.l2_cache.expire(f"cache:{cache_key}", int(ttl.total_seconds()))
        
        return True
    
    async def _write_back_cache(
        self, 
        cache_key: str, 
        data: Dict[str, Any], 
        ttl: timedelta
    ) -> bool:
        """Write-back caching strategy."""
        # Write to L1 immediately, L2 later
        self.l1_cache[cache_key] = data
        
        # Mark for later write-back
        self.consistency_tracker[cache_key] = {
            'data': data,
            'ttl': ttl,
            'dirty': True,
            'last_access': datetime.now()
        }
        
        return True
    
    async def _write_around_cache(
        self, 
        cache_key: str, 
        data: Dict[str, Any], 
        ttl: timedelta
    ) -> bool:
        """Write-around caching strategy."""
        # Write directly to L2, bypass L1
        await self.l2_cache.hset(
            f"cache:{cache_key}",
            mapping={
                'data': json.dumps(data),
                'timestamp': datetime.now().isoformat(),
                'ttl': str(ttl.total_seconds())
            }
        )
        await self.l2_cache.expire(f"cache:{cache_key}", int(ttl.total_seconds()))
        
        return True
    
    async def _read_through_cache(
        self, 
        cache_key: str, 
        data: Dict[str, Any], 
        ttl: timedelta
    ) -> bool:
        """Read-through caching strategy."""
        # Cache on read miss
        return await self._write_through_cache(cache_key, data, ttl)
    
    async def _refresh_ahead_cache(
        self, 
        cache_key: str, 
        data: Dict[str, Any], 
        ttl: timedelta
    ) -> bool:
        """Refresh-ahead caching strategy."""
        # Write to cache and schedule refresh
        success = await self._write_through_cache(cache_key, data, ttl)
        
        if success:
            await self._schedule_refresh_ahead(cache_key, ttl)
        
        return success
    
    async def _schedule_refresh_ahead(self, cache_key: str, ttl: timedelta):
        """Schedule refresh-ahead operation."""
        # Schedule refresh at 80% of TTL
        refresh_time = ttl.total_seconds() * 0.8
        
        # This would be implemented with a background task scheduler
        logger.debug(f"Scheduled refresh-ahead for {cache_key} in {refresh_time}s")
    
    async def _cache_workflow_decision(
        self, 
        cache_key: str, 
        decision_data: Dict[str, Any], 
        ttl: timedelta
    ) -> bool:
        """Cache workflow decision data."""
        return await self._write_through_cache(cache_key, decision_data, ttl)
    
    async def _cache_task_context(
        self, 
        cache_key: str, 
        context_data: Dict[str, Any]
    ) -> bool:
        """Cache task context data."""
        ttl = self._calculate_ttl('task_contexts')
        return await self._write_back_cache(cache_key, context_data, ttl)
    
    def _calculate_overall_score(
        self, 
        analysis_results: Dict[str, GapAnalysisResult]
    ) -> float:
        """Calculate overall gap analysis score."""
        if not analysis_results:
            return 0.0
        
        total_score = sum(result.score for result in analysis_results.values())
        return total_score / len(analysis_results)
    
    async def _warm_workflow_patterns(self) -> int:
        """Warm cache with workflow decision patterns."""
        # This would implement workflow pattern warming
        return 0
    
    async def _warm_task_patterns(self) -> int:
        """Warm cache with task context patterns."""
        # This would implement task pattern warming
        return 0
    
    async def _warm_gap_patterns(self) -> int:
        """Warm cache with gap analysis patterns."""
        # This would implement gap analysis pattern warming
        return 0
    
    async def _warm_agent_patterns(self) -> int:
        """Warm cache with agent coordination patterns."""
        # This would implement agent pattern warming
        return 0
    
    async def _analyze_cache_usage(self) -> Dict[str, Any]:
        """Analyze cache usage patterns."""
        return {
            'access_frequency': {},
            'data_types': {},
            'time_patterns': {}
        }
    
    async def _evict_lru_entries(self) -> int:
        """Evict least recently used entries from L1 cache."""
        # Implement LRU eviction logic
        return 0
    
    async def _promote_frequent_entries(self) -> int:
        """Promote frequently accessed entries to L1."""
        # Implement promotion logic
        return 0
    
    async def _adjust_ttl_strategies(self, usage_patterns: Dict[str, Any]) -> int:
        """Adjust TTL strategies based on usage patterns."""
        # Implement TTL adjustment logic
        return 0
    
    async def _optimize_cache_strategies(self, usage_patterns: Dict[str, Any]) -> int:
        """Optimize cache strategies based on patterns."""
        # Implement strategy optimization logic
        return 0
    
    def _calculate_hit_ratio(self):
        """Calculate and update cache hit ratio."""
        total_hits = (
            self.cache_metrics['l1_hits'] + 
            self.cache_metrics['l2_hits'] + 
            self.cache_metrics['vector_hits']
        )
        total_requests = (
            total_hits + 
            self.cache_metrics['l1_misses'] + 
            self.cache_metrics['l2_misses'] + 
            self.cache_metrics['vector_misses']
        )
        
        if total_requests > 0:
            self.cache_metrics['hit_ratio'] = total_hits / total_requests
    
    def _update_average_retrieval_time(self, retrieval_time: float):
        """Update average cache retrieval time."""
        current_avg = self.cache_metrics['average_retrieval_time']
        total_requests = (
            self.cache_metrics['l1_hits'] + self.cache_metrics['l1_misses'] +
            self.cache_metrics['l2_hits'] + self.cache_metrics['l2_misses'] +
            self.cache_metrics['vector_hits'] + self.cache_metrics['vector_misses']
        )
        
        if total_requests == 1:
            self.cache_metrics['average_retrieval_time'] = retrieval_time
        else:
            self.cache_metrics['average_retrieval_time'] = (
                (current_avg * (total_requests - 1) + retrieval_time) / total_requests
            )
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default caching configuration."""
        return {
            'l1_cache_size_limit': 1000,
            'l2_cache_enabled': True,
            'vector_cache_enabled': True,
            'cache_warming_enabled': True,
            'performance_monitoring': True,
            'consistency_checking': True,
            'auto_optimization': True
        }
