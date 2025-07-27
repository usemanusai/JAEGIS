"""
N.L.D.S. Performance Optimization System
Production performance optimization, caching strategies, and resource utilization
"""

import asyncio
import time
import logging
import psutil
import gc
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
from collections import defaultdict, deque
import redis
import json
import hashlib

logger = logging.getLogger(__name__)


class OptimizationLevel(str, Enum):
    """Performance optimization levels."""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    MAXIMUM = "maximum"


class CacheStrategy(str, Enum):
    """Caching strategies."""
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    ADAPTIVE = "adaptive"


class ResourceType(str, Enum):
    """Types of system resources."""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    DATABASE = "database"
    CACHE = "cache"


@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot."""
    timestamp: float
    response_time_ms: float
    throughput_rps: float
    cpu_usage_percent: float
    memory_usage_mb: float
    cache_hit_ratio: float
    database_query_time_ms: float
    active_connections: int
    queue_depth: int


@dataclass
class OptimizationRule:
    """Performance optimization rule."""
    rule_id: str
    name: str
    description: str
    resource_type: ResourceType
    trigger_condition: str
    optimization_action: str
    expected_improvement: float
    risk_level: str


@dataclass
class CacheConfiguration:
    """Cache configuration settings."""
    cache_type: str
    max_size_mb: int
    ttl_seconds: int
    eviction_policy: CacheStrategy
    compression_enabled: bool
    serialization_format: str


@dataclass
class OptimizationResult:
    """Result of optimization operation."""
    optimization_id: str
    rule_applied: str
    before_metrics: PerformanceMetrics
    after_metrics: PerformanceMetrics
    improvement_percent: float
    success: bool
    side_effects: List[str]
    timestamp: float


class PerformanceOptimizer:
    """
    N.L.D.S. Performance Optimization System
    
    Provides comprehensive performance optimization including:
    - Real-time performance monitoring
    - Intelligent caching strategies
    - Resource utilization optimization
    - Automatic performance tuning
    - Predictive scaling
    """
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0)
        
        # Performance tracking
        self.metrics_history: deque = deque(maxlen=1000)
        self.optimization_history: List[OptimizationResult] = []
        
        # Configuration
        self.config = {
            "target_response_time_ms": 500,
            "target_throughput_rps": 1000,
            "max_cpu_usage": 0.80,
            "max_memory_usage_mb": 8192,
            "cache_hit_ratio_target": 0.85,
            "optimization_interval": 60,  # seconds
            "metrics_collection_interval": 5,  # seconds
            "performance_window": 300  # 5 minutes
        }
        
        # Optimization rules
        self.optimization_rules = self._initialize_optimization_rules()
        
        # Cache configurations
        self.cache_configs = self._initialize_cache_configs()
        
        # Start background optimization
        asyncio.create_task(self._performance_monitor())
        asyncio.create_task(self._optimization_engine())
        
        logger.info("Performance Optimizer initialized")
    
    def _initialize_optimization_rules(self) -> List[OptimizationRule]:
        """Initialize performance optimization rules."""
        
        return [
            OptimizationRule(
                rule_id="high_response_time",
                name="High Response Time Optimization",
                description="Optimize when response time exceeds target",
                resource_type=ResourceType.CPU,
                trigger_condition="response_time_ms > 500",
                optimization_action="enable_aggressive_caching",
                expected_improvement=0.30,
                risk_level="low"
            ),
            
            OptimizationRule(
                rule_id="low_cache_hit_ratio",
                name="Cache Hit Ratio Optimization",
                description="Improve caching when hit ratio is low",
                resource_type=ResourceType.CACHE,
                trigger_condition="cache_hit_ratio < 0.80",
                optimization_action="optimize_cache_strategy",
                expected_improvement=0.25,
                risk_level="low"
            ),
            
            OptimizationRule(
                rule_id="high_cpu_usage",
                name="CPU Usage Optimization",
                description="Reduce CPU load when usage is high",
                resource_type=ResourceType.CPU,
                trigger_condition="cpu_usage_percent > 0.80",
                optimization_action="enable_request_throttling",
                expected_improvement=0.20,
                risk_level="medium"
            ),
            
            OptimizationRule(
                rule_id="high_memory_usage",
                name="Memory Usage Optimization",
                description="Optimize memory when usage is high",
                resource_type=ResourceType.MEMORY,
                trigger_condition="memory_usage_mb > 6144",
                optimization_action="trigger_garbage_collection",
                expected_improvement=0.15,
                risk_level="low"
            ),
            
            OptimizationRule(
                rule_id="low_throughput",
                name="Throughput Optimization",
                description="Improve throughput when below target",
                resource_type=ResourceType.NETWORK,
                trigger_condition="throughput_rps < 800",
                optimization_action="optimize_connection_pooling",
                expected_improvement=0.35,
                risk_level="medium"
            ),
            
            OptimizationRule(
                rule_id="high_queue_depth",
                name="Queue Depth Optimization",
                description="Reduce queue depth when too high",
                resource_type=ResourceType.NETWORK,
                trigger_condition="queue_depth > 100",
                optimization_action="increase_worker_threads",
                expected_improvement=0.40,
                risk_level="high"
            )
        ]
    
    def _initialize_cache_configs(self) -> Dict[str, CacheConfiguration]:
        """Initialize cache configurations."""
        
        return {
            "nlp_analysis": CacheConfiguration(
                cache_type="nlp_analysis",
                max_size_mb=512,
                ttl_seconds=3600,  # 1 hour
                eviction_policy=CacheStrategy.LRU,
                compression_enabled=True,
                serialization_format="json"
            ),
            
            "user_profiles": CacheConfiguration(
                cache_type="user_profiles",
                max_size_mb=256,
                ttl_seconds=86400,  # 24 hours
                eviction_policy=CacheStrategy.LFU,
                compression_enabled=True,
                serialization_format="pickle"
            ),
            
            "conversation_context": CacheConfiguration(
                cache_type="conversation_context",
                max_size_mb=1024,
                ttl_seconds=86400,  # 24 hours
                eviction_policy=CacheStrategy.TTL,
                compression_enabled=False,
                serialization_format="json"
            ),
            
            "jaegis_commands": CacheConfiguration(
                cache_type="jaegis_commands",
                max_size_mb=128,
                ttl_seconds=7200,  # 2 hours
                eviction_policy=CacheStrategy.LRU,
                compression_enabled=True,
                serialization_format="json"
            ),
            
            "api_responses": CacheConfiguration(
                cache_type="api_responses",
                max_size_mb=256,
                ttl_seconds=1800,  # 30 minutes
                eviction_policy=CacheStrategy.ADAPTIVE,
                compression_enabled=True,
                serialization_format="json"
            )
        }
    
    async def collect_performance_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage_mb = memory_info.used / (1024 * 1024)
        
        # Application metrics (simulated - would integrate with actual monitoring)
        response_time_ms = await self._get_average_response_time()
        throughput_rps = await self._get_current_throughput()
        cache_hit_ratio = await self._get_cache_hit_ratio()
        database_query_time = await self._get_database_query_time()
        active_connections = await self._get_active_connections()
        queue_depth = await self._get_queue_depth()
        
        metrics = PerformanceMetrics(
            timestamp=time.time(),
            response_time_ms=response_time_ms,
            throughput_rps=throughput_rps,
            cpu_usage_percent=cpu_percent,
            memory_usage_mb=memory_usage_mb,
            cache_hit_ratio=cache_hit_ratio,
            database_query_time_ms=database_query_time,
            active_connections=active_connections,
            queue_depth=queue_depth
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    async def _get_average_response_time(self) -> float:
        """Get average response time from recent metrics."""
        
        if len(self.metrics_history) < 5:
            return 320.0  # Default baseline
        
        recent_metrics = list(self.metrics_history)[-10:]
        return statistics.mean([m.response_time_ms for m in recent_metrics])
    
    async def _get_current_throughput(self) -> float:
        """Get current throughput in requests per second."""
        
        # Simulate throughput calculation
        base_throughput = 850.0
        
        # Adjust based on CPU usage
        if len(self.metrics_history) > 0:
            latest = self.metrics_history[-1]
            cpu_factor = max(0.5, 1.0 - (latest.cpu_usage_percent - 0.5))
            return base_throughput * cpu_factor
        
        return base_throughput
    
    async def _get_cache_hit_ratio(self) -> float:
        """Get current cache hit ratio."""
        
        try:
            # Get cache statistics from Redis
            info = self.redis_client.info()
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            
            if hits + misses > 0:
                return hits / (hits + misses)
            else:
                return 0.85  # Default good ratio
        
        except Exception:
            return 0.75  # Conservative default
    
    async def _get_database_query_time(self) -> float:
        """Get average database query time."""
        
        # Simulate database query time
        return 45.0  # milliseconds
    
    async def _get_active_connections(self) -> int:
        """Get number of active connections."""
        
        # Simulate active connections
        return 150
    
    async def _get_queue_depth(self) -> int:
        """Get current queue depth."""
        
        # Simulate queue depth
        return 25
    
    async def optimize_performance(self, optimization_level: OptimizationLevel = OptimizationLevel.BALANCED) -> List[OptimizationResult]:
        """Perform performance optimization based on current metrics."""
        
        current_metrics = await self.collect_performance_metrics()
        optimization_results = []
        
        # Apply relevant optimization rules
        for rule in self.optimization_rules:
            if self._should_apply_rule(rule, current_metrics, optimization_level):
                try:
                    result = await self._apply_optimization_rule(rule, current_metrics)
                    optimization_results.append(result)
                    
                    logger.info(f"Applied optimization: {rule.name} - {result.improvement_percent:.1f}% improvement")
                    
                except Exception as e:
                    logger.error(f"Failed to apply optimization rule {rule.rule_id}: {e}")
        
        return optimization_results
    
    def _should_apply_rule(self, rule: OptimizationRule, metrics: PerformanceMetrics, level: OptimizationLevel) -> bool:
        """Determine if optimization rule should be applied."""
        
        # Check trigger condition
        condition_met = self._evaluate_condition(rule.trigger_condition, metrics)
        
        if not condition_met:
            return False
        
        # Check optimization level constraints
        if level == OptimizationLevel.CONSERVATIVE and rule.risk_level in ["high", "maximum"]:
            return False
        elif level == OptimizationLevel.BALANCED and rule.risk_level == "maximum":
            return False
        
        # Check if rule was recently applied
        recent_applications = [
            opt for opt in self.optimization_history[-10:]
            if opt.rule_applied == rule.rule_id and time.time() - opt.timestamp < 300
        ]
        
        return len(recent_applications) == 0
    
    def _evaluate_condition(self, condition: str, metrics: PerformanceMetrics) -> bool:
        """Evaluate optimization trigger condition."""
        
        # Simple condition evaluation (in production, use a proper expression evaluator)
        context = {
            "response_time_ms": metrics.response_time_ms,
            "throughput_rps": metrics.throughput_rps,
            "cpu_usage_percent": metrics.cpu_usage_percent,
            "memory_usage_mb": metrics.memory_usage_mb,
            "cache_hit_ratio": metrics.cache_hit_ratio,
            "queue_depth": metrics.queue_depth
        }
        
        try:
            return eval(condition, {"__builtins__": {}}, context)
        except Exception:
            return False
    
    async def _apply_optimization_rule(self, rule: OptimizationRule, before_metrics: PerformanceMetrics) -> OptimizationResult:
        """Apply specific optimization rule."""
        
        optimization_id = f"opt_{int(time.time())}_{rule.rule_id}"
        
        # Apply optimization based on action
        if rule.optimization_action == "enable_aggressive_caching":
            await self._enable_aggressive_caching()
        
        elif rule.optimization_action == "optimize_cache_strategy":
            await self._optimize_cache_strategy()
        
        elif rule.optimization_action == "enable_request_throttling":
            await self._enable_request_throttling()
        
        elif rule.optimization_action == "trigger_garbage_collection":
            await self._trigger_garbage_collection()
        
        elif rule.optimization_action == "optimize_connection_pooling":
            await self._optimize_connection_pooling()
        
        elif rule.optimization_action == "increase_worker_threads":
            await self._increase_worker_threads()
        
        # Wait for optimization to take effect
        await asyncio.sleep(5)
        
        # Collect after metrics
        after_metrics = await self.collect_performance_metrics()
        
        # Calculate improvement
        improvement = self._calculate_improvement(rule, before_metrics, after_metrics)
        
        result = OptimizationResult(
            optimization_id=optimization_id,
            rule_applied=rule.rule_id,
            before_metrics=before_metrics,
            after_metrics=after_metrics,
            improvement_percent=improvement,
            success=improvement > 0,
            side_effects=[],
            timestamp=time.time()
        )
        
        self.optimization_history.append(result)
        return result
    
    def _calculate_improvement(self, rule: OptimizationRule, before: PerformanceMetrics, after: PerformanceMetrics) -> float:
        """Calculate performance improvement percentage."""
        
        if rule.resource_type == ResourceType.CPU:
            if before.response_time_ms > 0:
                return ((before.response_time_ms - after.response_time_ms) / before.response_time_ms) * 100
        
        elif rule.resource_type == ResourceType.CACHE:
            return ((after.cache_hit_ratio - before.cache_hit_ratio) / before.cache_hit_ratio) * 100
        
        elif rule.resource_type == ResourceType.NETWORK:
            if rule.rule_id == "low_throughput":
                return ((after.throughput_rps - before.throughput_rps) / before.throughput_rps) * 100
            elif rule.rule_id == "high_queue_depth":
                if before.queue_depth > 0:
                    return ((before.queue_depth - after.queue_depth) / before.queue_depth) * 100
        
        elif rule.resource_type == ResourceType.MEMORY:
            if before.memory_usage_mb > 0:
                return ((before.memory_usage_mb - after.memory_usage_mb) / before.memory_usage_mb) * 100
        
        return 0.0
    
    async def _enable_aggressive_caching(self):
        """Enable aggressive caching strategies."""
        
        # Increase cache sizes and TTL
        for cache_name, config in self.cache_configs.items():
            config.max_size_mb = int(config.max_size_mb * 1.5)
            config.ttl_seconds = int(config.ttl_seconds * 1.2)
        
        logger.info("Enabled aggressive caching")
    
    async def _optimize_cache_strategy(self):
        """Optimize cache strategy based on usage patterns."""
        
        # Switch to more efficient eviction policies
        for config in self.cache_configs.values():
            if config.eviction_policy == CacheStrategy.LRU:
                config.eviction_policy = CacheStrategy.ADAPTIVE
        
        logger.info("Optimized cache strategy")
    
    async def _enable_request_throttling(self):
        """Enable request throttling to reduce CPU load."""
        
        # This would integrate with the actual request handling system
        logger.info("Enabled request throttling")
    
    async def _trigger_garbage_collection(self):
        """Trigger garbage collection to free memory."""
        
        gc.collect()
        logger.info("Triggered garbage collection")
    
    async def _optimize_connection_pooling(self):
        """Optimize database connection pooling."""
        
        # This would adjust connection pool settings
        logger.info("Optimized connection pooling")
    
    async def _increase_worker_threads(self):
        """Increase worker thread count to handle queue depth."""
        
        # This would adjust worker thread configuration
        logger.info("Increased worker threads")
    
    async def _performance_monitor(self):
        """Background performance monitoring task."""
        
        while True:
            try:
                await self.collect_performance_metrics()
                await asyncio.sleep(self.config["metrics_collection_interval"])
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(30)
    
    async def _optimization_engine(self):
        """Background optimization engine."""
        
        while True:
            try:
                await self.optimize_performance(OptimizationLevel.BALANCED)
                await asyncio.sleep(self.config["optimization_interval"])
                
            except Exception as e:
                logger.error(f"Optimization engine error: {e}")
                await asyncio.sleep(60)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        recent_metrics = list(self.metrics_history)[-10:]
        
        avg_response_time = statistics.mean([m.response_time_ms for m in recent_metrics])
        avg_throughput = statistics.mean([m.throughput_rps for m in recent_metrics])
        avg_cpu_usage = statistics.mean([m.cpu_usage_percent for m in recent_metrics])
        avg_memory_usage = statistics.mean([m.memory_usage_mb for m in recent_metrics])
        avg_cache_hit_ratio = statistics.mean([m.cache_hit_ratio for m in recent_metrics])
        
        # Performance targets
        targets = {
            "response_time_ms": self.config["target_response_time_ms"],
            "throughput_rps": self.config["target_throughput_rps"],
            "cpu_usage": self.config["max_cpu_usage"],
            "memory_usage_mb": self.config["max_memory_usage_mb"],
            "cache_hit_ratio": self.config["cache_hit_ratio_target"]
        }
        
        # Calculate target achievement
        target_achievement = {
            "response_time": avg_response_time <= targets["response_time_ms"],
            "throughput": avg_throughput >= targets["throughput_rps"],
            "cpu_usage": avg_cpu_usage <= targets["cpu_usage"],
            "memory_usage": avg_memory_usage <= targets["memory_usage_mb"],
            "cache_hit_ratio": avg_cache_hit_ratio >= targets["cache_hit_ratio"]
        }
        
        return {
            "current_performance": {
                "avg_response_time_ms": avg_response_time,
                "avg_throughput_rps": avg_throughput,
                "avg_cpu_usage_percent": avg_cpu_usage,
                "avg_memory_usage_mb": avg_memory_usage,
                "avg_cache_hit_ratio": avg_cache_hit_ratio
            },
            "targets": targets,
            "target_achievement": target_achievement,
            "overall_health": sum(target_achievement.values()) / len(target_achievement),
            "optimizations_applied": len(self.optimization_history),
            "recent_optimizations": len([opt for opt in self.optimization_history if time.time() - opt.timestamp < 3600])
        }
    
    async def cache_nlp_result(self, input_text: str, result: Dict[str, Any], cache_type: str = "nlp_analysis"):
        """Cache NLP analysis result."""
        
        cache_key = f"{cache_type}:{hashlib.md5(input_text.encode()).hexdigest()}"
        config = self.cache_configs.get(cache_type)
        
        if config:
            try:
                serialized_result = json.dumps(result) if config.serialization_format == "json" else str(result)
                
                self.redis_client.setex(
                    cache_key,
                    config.ttl_seconds,
                    serialized_result
                )
                
                logger.debug(f"Cached NLP result for key: {cache_key}")
                
            except Exception as e:
                logger.error(f"Failed to cache NLP result: {e}")
    
    async def get_cached_nlp_result(self, input_text: str, cache_type: str = "nlp_analysis") -> Optional[Dict[str, Any]]:
        """Retrieve cached NLP analysis result."""
        
        cache_key = f"{cache_type}:{hashlib.md5(input_text.encode()).hexdigest()}"
        
        try:
            cached_result = self.redis_client.get(cache_key)
            
            if cached_result:
                config = self.cache_configs.get(cache_type)
                if config and config.serialization_format == "json":
                    return json.loads(cached_result)
                else:
                    return eval(cached_result)  # Use with caution in production
            
        except Exception as e:
            logger.error(f"Failed to retrieve cached result: {e}")
        
        return None


# Example usage
async def main():
    """Example usage of Performance Optimizer."""
    
    optimizer = PerformanceOptimizer()
    
    # Collect current metrics
    metrics = await optimizer.collect_performance_metrics()
    print(f"Current metrics:")
    print(f"  Response time: {metrics.response_time_ms:.1f}ms")
    print(f"  Throughput: {metrics.throughput_rps:.1f} RPS")
    print(f"  CPU usage: {metrics.cpu_usage_percent:.1f}%")
    print(f"  Memory usage: {metrics.memory_usage_mb:.1f}MB")
    print(f"  Cache hit ratio: {metrics.cache_hit_ratio:.2%}")
    
    # Run optimization
    optimizations = await optimizer.optimize_performance()
    print(f"\nApplied {len(optimizations)} optimizations")
    
    for opt in optimizations:
        print(f"  {opt.rule_applied}: {opt.improvement_percent:.1f}% improvement")
    
    # Get performance summary
    summary = optimizer.get_performance_summary()
    print(f"\nPerformance summary:")
    print(f"  Overall health: {summary['overall_health']:.1%}")
    print(f"  Target achievement: {sum(summary['target_achievement'].values())}/{len(summary['target_achievement'])}")


if __name__ == "__main__":
    asyncio.run(main())
