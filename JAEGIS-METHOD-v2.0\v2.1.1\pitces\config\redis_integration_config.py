"""
P.I.T.C.E.S. Framework - Redis Integration Configuration
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module provides comprehensive configuration management for Redis vector integration,
caching strategies, and performance optimization across the P.I.T.C.E.S. framework.
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class RedisDeploymentMode(Enum):
    """Redis deployment modes."""
    STANDALONE = "standalone"
    CLUSTER = "cluster"
    SENTINEL = "sentinel"


class CacheStrategy(Enum):
    """Cache strategy types."""
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"
    WRITE_AROUND = "write_around"
    READ_THROUGH = "read_through"
    REFRESH_AHEAD = "refresh_ahead"


@dataclass
class RedisConnectionConfig:
    """Redis connection configuration."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ssl: bool = False
    ssl_cert_reqs: str = "required"
    ssl_ca_certs: Optional[str] = None
    ssl_certfile: Optional[str] = None
    ssl_keyfile: Optional[str] = None
    max_connections: int = 20
    retry_on_timeout: bool = True
    socket_timeout: float = 5.0
    socket_connect_timeout: float = 5.0
    socket_keepalive: bool = True
    socket_keepalive_options: Dict[str, int] = None
    
    def __post_init__(self):
        if self.socket_keepalive_options is None:
            self.socket_keepalive_options = {}


@dataclass
class VectorEngineConfig:
    """Vector engine configuration."""
    enabled: bool = True
    vector_dimensions: Dict[str, int] = None
    similarity_threshold: float = 0.8
    max_search_results: int = 10
    index_refresh_interval: int = 300  # seconds
    vector_compression: bool = True
    batch_size: int = 100
    
    def __post_init__(self):
        if self.vector_dimensions is None:
            self.vector_dimensions = {
                'workflow_decision': 128,
                'task_context': 256,
                'gap_analysis': 512,
                'agent_coordination': 64,
                'nlds_embedding': 1024
            }


@dataclass
class CachingConfig:
    """Enhanced caching configuration."""
    enabled: bool = True
    l1_cache_size_limit: int = 1000
    l2_cache_enabled: bool = True
    vector_cache_enabled: bool = True
    cache_warming_enabled: bool = True
    default_ttl_seconds: int = 3600
    priority_ttl_multipliers: Dict[str, float] = None
    cache_strategies: Dict[str, str] = None
    compression_enabled: bool = True
    eviction_policy: str = "lru"
    
    def __post_init__(self):
        if self.priority_ttl_multipliers is None:
            self.priority_ttl_multipliers = {
                'CRITICAL': 0.5,
                'HIGH': 0.75,
                'MEDIUM': 1.0,
                'LOW': 2.0
            }
        
        if self.cache_strategies is None:
            self.cache_strategies = {
                'workflow_decisions': 'write_through',
                'task_contexts': 'write_back',
                'gap_analyses': 'refresh_ahead',
                'agent_states': 'write_through',
                'nlds_embeddings': 'read_through'
            }


@dataclass
class StreamsConfig:
    """Redis Streams configuration."""
    enabled: bool = True
    max_stream_length: int = 10000
    consumer_group_prefix: str = "pitces"
    batch_size: int = 10
    block_timeout: int = 1000  # milliseconds
    max_retries: int = 3
    retry_delay: int = 5  # seconds
    dead_letter_queue_enabled: bool = True
    stream_retention_hours: int = 24
    consumer_timeout: int = 300  # seconds
    
    @property
    def stream_names(self) -> Dict[str, str]:
        """Get stream names configuration."""
        return {
            'task_priority': 'pitces:tasks:priority',
            'task_preemption': 'pitces:tasks:preemption',
            'workflow_decisions': 'pitces:workflow:decisions',
            'gap_analysis': 'pitces:gap:analysis',
            'agent_coordination': 'pitces:agent:coordination',
            'nlds_processing': 'pitces:nlds:processing',
            'system_events': 'pitces:system:events'
        }


@dataclass
class ClusterConfig:
    """Redis Cluster configuration."""
    enabled: bool = False
    startup_nodes: List[Dict[str, Any]] = None
    skip_full_coverage_check: bool = True
    health_check_interval: int = 30
    max_connections_per_node: int = 50
    readonly_mode: bool = False
    decode_responses: bool = True
    cluster_require_full_coverage: bool = False
    reinitialize_steps: int = 10
    
    def __post_init__(self):
        if self.startup_nodes is None:
            self.startup_nodes = [
                {'host': 'localhost', 'port': 7000},
                {'host': 'localhost', 'port': 7001},
                {'host': 'localhost', 'port': 7002}
            ]


@dataclass
class MonitoringConfig:
    """Monitoring and metrics configuration."""
    enabled: bool = True
    dashboard_enabled: bool = True
    metrics_retention_days: int = 7
    alert_retention_days: int = 30
    performance_monitoring_interval: int = 30  # seconds
    health_check_interval: int = 60  # seconds
    trend_analysis_interval: int = 300  # seconds
    optimization_check_interval: int = 900  # seconds
    
    # Performance thresholds
    vector_search_time_warning: float = 1.0
    vector_search_time_critical: float = 5.0
    cache_hit_ratio_warning: float = 70.0
    cache_hit_ratio_critical: float = 50.0
    stream_lag_warning: int = 100
    stream_lag_critical: int = 1000
    memory_usage_warning: float = 80.0
    memory_usage_critical: float = 95.0
    
    # Alert configuration
    email_alerts_enabled: bool = False
    webhook_alerts_enabled: bool = False
    alert_email_recipients: List[str] = None
    alert_webhook_url: Optional[str] = None
    
    def __post_init__(self):
        if self.alert_email_recipients is None:
            self.alert_email_recipients = []


@dataclass
class ContextEngineConfig:
    """Enhanced context engine configuration."""
    enabled: bool = True
    storage_path: str = "pitces_context"
    vector_storage_enabled: bool = True
    distributed_caching_enabled: bool = True
    background_tasks_enabled: bool = True
    cache_warming_enabled: bool = True
    compression_enabled: bool = True
    sync_interval_hours: int = 2
    cleanup_interval_hours: int = 24
    index_maintenance_interval_minutes: int = 30
    max_context_age_days: int = 30


class RedisIntegrationConfig:
    """
    Comprehensive Redis integration configuration for P.I.T.C.E.S. framework.
    
    This class manages all Redis-related configurations including vector engine,
    caching, streams, clustering, monitoring, and context management.
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize Redis integration configuration.
        
        Args:
            config_dict: Optional configuration dictionary
        """
        config = config_dict or {}
        
        # Core Redis configuration
        self.deployment_mode = RedisDeploymentMode(
            config.get('deployment_mode', 'standalone')
        )
        
        self.connection = RedisConnectionConfig(
            **config.get('connection', {})
        )
        
        # Component configurations
        self.vector_engine = VectorEngineConfig(
            **config.get('vector_engine', {})
        )
        
        self.caching = CachingConfig(
            **config.get('caching', {})
        )
        
        self.streams = StreamsConfig(
            **config.get('streams', {})
        )
        
        self.cluster = ClusterConfig(
            **config.get('cluster', {})
        )
        
        self.monitoring = MonitoringConfig(
            **config.get('monitoring', {})
        )
        
        self.context_engine = ContextEngineConfig(
            **config.get('context_engine', {})
        )
        
        # Integration settings
        self.nlds_integration_enabled = config.get('nlds_integration_enabled', True)
        self.jaegis_integration_enabled = config.get('jaegis_integration_enabled', True)
        self.gap_analysis_integration_enabled = config.get('gap_analysis_integration_enabled', True)
        self.triage_system_integration_enabled = config.get('triage_system_integration_enabled', True)
        
        # Performance optimization
        self.auto_optimization_enabled = config.get('auto_optimization_enabled', True)
        self.performance_baseline_enabled = config.get('performance_baseline_enabled', True)
        self.adaptive_caching_enabled = config.get('adaptive_caching_enabled', True)
        
        # Security settings
        self.encryption_enabled = config.get('encryption_enabled', False)
        self.access_control_enabled = config.get('access_control_enabled', True)
        self.audit_logging_enabled = config.get('audit_logging_enabled', True)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Configuration dictionary
        """
        return {
            'deployment_mode': self.deployment_mode.value,
            'connection': asdict(self.connection),
            'vector_engine': asdict(self.vector_engine),
            'caching': asdict(self.caching),
            'streams': asdict(self.streams),
            'cluster': asdict(self.cluster),
            'monitoring': asdict(self.monitoring),
            'context_engine': asdict(self.context_engine),
            'nlds_integration_enabled': self.nlds_integration_enabled,
            'jaegis_integration_enabled': self.jaegis_integration_enabled,
            'gap_analysis_integration_enabled': self.gap_analysis_integration_enabled,
            'triage_system_integration_enabled': self.triage_system_integration_enabled,
            'auto_optimization_enabled': self.auto_optimization_enabled,
            'performance_baseline_enabled': self.performance_baseline_enabled,
            'adaptive_caching_enabled': self.adaptive_caching_enabled,
            'encryption_enabled': self.encryption_enabled,
            'access_control_enabled': self.access_control_enabled,
            'audit_logging_enabled': self.audit_logging_enabled
        }
    
    @classmethod
    def from_environment(cls) -> 'RedisIntegrationConfig':
        """
        Create configuration from environment variables.
        
        Returns:
            Configuration instance
        """
        config = {
            'connection': {
                'host': os.getenv('REDIS_HOST', 'localhost'),
                'port': int(os.getenv('REDIS_PORT', '6379')),
                'db': int(os.getenv('REDIS_DB', '0')),
                'password': os.getenv('REDIS_PASSWORD'),
                'ssl': os.getenv('REDIS_SSL', 'false').lower() == 'true',
                'max_connections': int(os.getenv('REDIS_MAX_CONNECTIONS', '20'))
            },
            'vector_engine': {
                'enabled': os.getenv('VECTOR_ENGINE_ENABLED', 'true').lower() == 'true',
                'similarity_threshold': float(os.getenv('VECTOR_SIMILARITY_THRESHOLD', '0.8'))
            },
            'caching': {
                'enabled': os.getenv('CACHING_ENABLED', 'true').lower() == 'true',
                'l1_cache_size_limit': int(os.getenv('L1_CACHE_SIZE_LIMIT', '1000')),
                'cache_warming_enabled': os.getenv('CACHE_WARMING_ENABLED', 'true').lower() == 'true'
            },
            'streams': {
                'enabled': os.getenv('STREAMS_ENABLED', 'true').lower() == 'true',
                'batch_size': int(os.getenv('STREAMS_BATCH_SIZE', '10'))
            },
            'cluster': {
                'enabled': os.getenv('CLUSTER_ENABLED', 'false').lower() == 'true'
            },
            'monitoring': {
                'enabled': os.getenv('MONITORING_ENABLED', 'true').lower() == 'true',
                'dashboard_enabled': os.getenv('DASHBOARD_ENABLED', 'true').lower() == 'true'
            }
        }
        
        return cls(config)
    
    @classmethod
    def get_development_config(cls) -> 'RedisIntegrationConfig':
        """
        Get development environment configuration.
        
        Returns:
            Development configuration
        """
        config = {
            'deployment_mode': 'standalone',
            'connection': {
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'max_connections': 10
            },
            'vector_engine': {
                'enabled': True,
                'similarity_threshold': 0.8
            },
            'caching': {
                'enabled': True,
                'l1_cache_size_limit': 500,
                'cache_warming_enabled': True
            },
            'streams': {
                'enabled': True,
                'batch_size': 5
            },
            'cluster': {
                'enabled': False
            },
            'monitoring': {
                'enabled': True,
                'dashboard_enabled': True,
                'performance_monitoring_interval': 60
            }
        }
        
        return cls(config)
    
    @classmethod
    def get_production_config(cls) -> 'RedisIntegrationConfig':
        """
        Get production environment configuration.
        
        Returns:
            Production configuration
        """
        config = {
            'deployment_mode': 'cluster',
            'connection': {
                'host': 'redis-cluster.production.local',
                'port': 6379,
                'db': 0,
                'ssl': True,
                'max_connections': 50
            },
            'vector_engine': {
                'enabled': True,
                'similarity_threshold': 0.85,
                'vector_compression': True
            },
            'caching': {
                'enabled': True,
                'l1_cache_size_limit': 2000,
                'cache_warming_enabled': True,
                'compression_enabled': True
            },
            'streams': {
                'enabled': True,
                'batch_size': 20,
                'max_stream_length': 50000
            },
            'cluster': {
                'enabled': True,
                'health_check_interval': 15,
                'max_connections_per_node': 100
            },
            'monitoring': {
                'enabled': True,
                'dashboard_enabled': True,
                'performance_monitoring_interval': 15,
                'email_alerts_enabled': True,
                'webhook_alerts_enabled': True
            },
            'auto_optimization_enabled': True,
            'encryption_enabled': True,
            'access_control_enabled': True,
            'audit_logging_enabled': True
        }
        
        return cls(config)
    
    def validate(self) -> List[str]:
        """
        Validate configuration settings.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate connection settings
        if not self.connection.host:
            errors.append("Redis host is required")
        
        if self.connection.port <= 0 or self.connection.port > 65535:
            errors.append("Redis port must be between 1 and 65535")
        
        # Validate cluster settings
        if self.cluster.enabled and not self.cluster.startup_nodes:
            errors.append("Cluster startup nodes are required when cluster is enabled")
        
        # Validate vector engine settings
        if self.vector_engine.enabled:
            if self.vector_engine.similarity_threshold < 0 or self.vector_engine.similarity_threshold > 1:
                errors.append("Vector similarity threshold must be between 0 and 1")
        
        # Validate caching settings
        if self.caching.enabled:
            if self.caching.l1_cache_size_limit <= 0:
                errors.append("L1 cache size limit must be positive")
        
        # Validate monitoring settings
        if self.monitoring.enabled:
            if self.monitoring.performance_monitoring_interval <= 0:
                errors.append("Performance monitoring interval must be positive")
        
        return errors
    
    def get_redis_url(self) -> str:
        """
        Get Redis connection URL.
        
        Returns:
            Redis connection URL
        """
        scheme = "rediss" if self.connection.ssl else "redis"
        auth = f":{self.connection.password}@" if self.connection.password else ""
        
        return f"{scheme}://{auth}{self.connection.host}:{self.connection.port}/{self.connection.db}"
