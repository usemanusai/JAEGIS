# N.L.D.S. Performance Optimization Guide

## **Overview**

This document outlines comprehensive performance optimization strategies for the Natural Language Detection System (N.L.D.S.) in production environments, ensuring optimal resource utilization and meeting SLA requirements.

## **Performance Targets**

### **Service Level Agreements (SLAs)**
- **Response Time**: <500ms (95th percentile)
- **Throughput**: 1000 requests/minute sustained
- **Availability**: 99.9% uptime
- **Confidence Accuracy**: ≥85% threshold
- **Resource Utilization**: <80% CPU, <85% Memory

### **Performance Metrics**
- **P50 Response Time**: <200ms
- **P95 Response Time**: <500ms
- **P99 Response Time**: <1000ms
- **Error Rate**: <1%
- **Cache Hit Rate**: >80%

## **Application-Level Optimizations**

### **1. Processing Pipeline Optimization**

#### **Asynchronous Processing**
```python
# nlds/optimization/async_processing.py

import asyncio
import aioredis
import asyncpg
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

@dataclass
class ProcessingTask:
    task_id: str
    input_text: str
    priority: int
    user_context: Dict[str, Any]

class OptimizedProcessingOrchestrator:
    def __init__(self):
        self.redis_pool = None
        self.db_pool = None
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        self.processing_queue = asyncio.Queue(maxsize=1000)
        self.batch_size = 10
        self.batch_timeout = 0.1  # 100ms
        
    async def initialize(self):
        """Initialize connection pools"""
        self.redis_pool = aioredis.ConnectionPool.from_url(
            "redis://redis-service:6379",
            max_connections=20,
            retry_on_timeout=True
        )
        
        self.db_pool = await asyncpg.create_pool(
            "postgresql://nlds:password@postgres-service:5432/nlds",
            min_size=5,
            max_size=20,
            command_timeout=30
        )
    
    async def process_batch(self, tasks: List[ProcessingTask]) -> List[Dict[str, Any]]:
        """Process multiple tasks in parallel"""
        # Group tasks by similarity for batch processing
        grouped_tasks = self._group_similar_tasks(tasks)
        
        # Process groups concurrently
        results = []
        for group in grouped_tasks:
            group_results = await asyncio.gather(*[
                self._process_single_task(task) for task in group
            ])
            results.extend(group_results)
        
        return results
    
    def _group_similar_tasks(self, tasks: List[ProcessingTask]) -> List[List[ProcessingTask]]:
        """Group similar tasks for batch processing"""
        # Simple grouping by input length and domain
        groups = {}
        
        for task in tasks:
            key = (
                len(task.input_text) // 100,  # Group by text length
                task.user_context.get('domain', 'general')
            )
            
            if key not in groups:
                groups[key] = []
            groups[key].append(task)
        
        return list(groups.values())
    
    async def _process_single_task(self, task: ProcessingTask) -> Dict[str, Any]:
        """Process individual task with optimizations"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Check cache first
            cached_result = await self._check_cache(task)
            if cached_result:
                return cached_result
            
            # Process with timeout
            result = await asyncio.wait_for(
                self._execute_processing_pipeline(task),
                timeout=5.0  # 5 second timeout
            )
            
            # Cache result
            await self._cache_result(task, result)
            
            # Record metrics
            processing_time = asyncio.get_event_loop().time() - start_time
            await self._record_metrics(task, result, processing_time)
            
            return result
            
        except asyncio.TimeoutError:
            return {"error": "Processing timeout", "task_id": task.task_id}
        except Exception as e:
            return {"error": str(e), "task_id": task.task_id}
```

#### **Intelligent Caching Strategy**
```python
# nlds/optimization/caching.py

import hashlib
import json
import pickle
from typing import Any, Optional, Dict
from datetime import datetime, timedelta

class IntelligentCache:
    def __init__(self, redis_pool):
        self.redis = redis_pool
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
    
    async def get_cached_result(self, input_text: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached result with intelligent key generation"""
        cache_key = self._generate_cache_key(input_text, context)
        
        try:
            cached_data = await self.redis.get(cache_key)
            if cached_data:
                result = pickle.loads(cached_data)
                
                # Check if cache is still valid
                if self._is_cache_valid(result):
                    self.cache_stats['hits'] += 1
                    return result['data']
                else:
                    # Remove expired cache
                    await self.redis.delete(cache_key)
            
            self.cache_stats['misses'] += 1
            return None
            
        except Exception:
            self.cache_stats['misses'] += 1
            return None
    
    async def cache_result(self, input_text: str, context: Dict[str, Any], 
                          result: Dict[str, Any], ttl: int = 3600):
        """Cache result with intelligent TTL"""
        cache_key = self._generate_cache_key(input_text, context)
        
        # Determine TTL based on confidence score
        confidence = result.get('confidence_score', 0)
        if confidence >= 0.9:
            ttl = 7200  # 2 hours for high confidence
        elif confidence >= 0.8:
            ttl = 3600  # 1 hour for medium confidence
        else:
            ttl = 1800  # 30 minutes for low confidence
        
        cache_data = {
            'data': result,
            'cached_at': datetime.utcnow().isoformat(),
            'ttl': ttl,
            'confidence': confidence
        }
        
        try:
            await self.redis.setex(
                cache_key,
                ttl,
                pickle.dumps(cache_data)
            )
        except Exception:
            pass  # Cache failure shouldn't break the request
    
    def _generate_cache_key(self, input_text: str, context: Dict[str, Any]) -> str:
        """Generate intelligent cache key"""
        # Normalize input for better cache hits
        normalized_text = input_text.lower().strip()
        
        # Include relevant context in key
        relevant_context = {
            'domain': context.get('domain'),
            'urgency': context.get('urgency'),
            'mode': context.get('mode', 'standard')
        }
        
        # Create hash
        key_data = f"{normalized_text}:{json.dumps(relevant_context, sort_keys=True)}"
        cache_key = hashlib.sha256(key_data.encode()).hexdigest()[:16]
        
        return f"nlds:cache:{cache_key}"
    
    def _is_cache_valid(self, cached_result: Dict[str, Any]) -> bool:
        """Check if cached result is still valid"""
        cached_at = datetime.fromisoformat(cached_result['cached_at'])
        ttl = cached_result['ttl']
        
        return datetime.utcnow() < cached_at + timedelta(seconds=ttl)
```

### **2. Database Optimization**

#### **Connection Pool Optimization**
```python
# nlds/optimization/database.py

import asyncpg
from typing import List, Dict, Any
import logging

class OptimizedDatabaseManager:
    def __init__(self):
        self.pool = None
        self.prepared_statements = {}
        
    async def initialize_pool(self):
        """Initialize optimized connection pool"""
        self.pool = await asyncpg.create_pool(
            "postgresql://nlds:password@postgres-service:5432/nlds",
            min_size=10,
            max_size=50,
            max_queries=50000,
            max_inactive_connection_lifetime=300,
            command_timeout=30,
            server_settings={
                'application_name': 'nlds_api',
                'tcp_keepalives_idle': '600',
                'tcp_keepalives_interval': '30',
                'tcp_keepalives_count': '3',
            }
        )
        
        # Prepare frequently used statements
        await self._prepare_statements()
    
    async def _prepare_statements(self):
        """Prepare frequently used SQL statements"""
        async with self.pool.acquire() as conn:
            # User session queries
            self.prepared_statements['get_session'] = await conn.prepare("""
                SELECT session_data, expires_at 
                FROM user_sessions 
                WHERE session_id = $1 AND expires_at > NOW()
            """)
            
            self.prepared_statements['update_session'] = await conn.prepare("""
                UPDATE user_sessions 
                SET last_activity = NOW(), session_data = $2
                WHERE session_id = $1
            """)
            
            # Processing history queries
            self.prepared_statements['insert_processing_log'] = await conn.prepare("""
                INSERT INTO processing_logs 
                (request_id, input_text, confidence_score, processing_time_ms, created_at)
                VALUES ($1, $2, $3, $4, NOW())
            """)
            
            self.prepared_statements['get_recent_processing'] = await conn.prepare("""
                SELECT input_text, confidence_score, jaegis_command
                FROM processing_logs 
                WHERE user_id = $1 AND created_at > NOW() - INTERVAL '1 hour'
                ORDER BY created_at DESC LIMIT 10
            """)
    
    async def execute_batch_insert(self, table: str, records: List[Dict[str, Any]]):
        """Optimized batch insert"""
        if not records:
            return
        
        async with self.pool.acquire() as conn:
            # Use COPY for large batch inserts
            if len(records) > 100:
                await self._copy_insert(conn, table, records)
            else:
                await self._batch_insert(conn, table, records)
    
    async def _copy_insert(self, conn, table: str, records: List[Dict[str, Any]]):
        """Use COPY for high-performance bulk inserts"""
        columns = list(records[0].keys())
        
        async with conn.transaction():
            await conn.copy_records_to_table(
                table,
                records=[(tuple(record[col] for col in columns)) for record in records],
                columns=columns
            )
```

#### **Query Optimization**
```sql
-- Database optimization queries
-- nlds/optimization/database_optimizations.sql

-- Create indexes for better performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_sessions_expires_at 
ON user_sessions (expires_at) WHERE expires_at > NOW();

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_processing_logs_user_created 
ON processing_logs (user_id, created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_processing_logs_confidence 
ON processing_logs (confidence_score) WHERE confidence_score >= 0.85;

-- Partitioning for large tables
CREATE TABLE IF NOT EXISTS processing_logs_y2025m07 PARTITION OF processing_logs
FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');

-- Optimize PostgreSQL settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;

-- Reload configuration
SELECT pg_reload_conf();
```

### **3. Redis Optimization**

#### **Redis Configuration**
```conf
# redis.conf - Optimized Redis configuration

# Memory optimization
maxmemory 1gb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# Persistence optimization
save 900 1
save 300 10
save 60 10000

# Network optimization
tcp-keepalive 300
timeout 0

# Performance optimization
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64

# Disable slow operations in production
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
```

## **Infrastructure-Level Optimizations**

### **1. Kubernetes Resource Optimization**

#### **Optimized Deployment Configuration**
```yaml
# deployment/optimization/nlds-optimized-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nlds-api-optimized
  namespace: nlds
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  template:
    spec:
      containers:
      - name: nlds-api
        image: jaegis/nlds:2.2.0
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        env:
        - name: NLDS_WORKERS
          value: "4"
        - name: NLDS_WORKER_CONNECTIONS
          value: "1000"
        - name: NLDS_KEEPALIVE
          value: "2"
        - name: NLDS_MAX_REQUESTS
          value: "1000"
        - name: NLDS_MAX_REQUESTS_JITTER
          value: "100"
        - name: NLDS_PRELOAD_APP
          value: "true"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app.kubernetes.io/name
                  operator: In
                  values:
                  - nlds
              topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: nlds
```

#### **Horizontal Pod Autoscaler (HPA) Optimization**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nlds-api-hpa-optimized
  namespace: nlds
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nlds-api-optimized
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: nlds_requests_per_second
      target:
        type: AverageValue
        averageValue: "50"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      - type: Pods
        value: 1
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max
```

### **2. Load Balancing Optimization**

#### **NGINX Configuration**
```nginx
# nginx.conf - Optimized NGINX configuration

upstream nlds_backend {
    least_conn;
    keepalive 32;
    
    server nlds-api-service:80 max_fails=3 fail_timeout=30s;
    
    # Health check
    check interval=3000 rise=2 fall=3 timeout=1000 type=http;
    check_http_send "GET /health HTTP/1.0\r\n\r\n";
    check_http_expect_alive http_2xx http_3xx;
}

server {
    listen 80;
    server_name api.jaegis.ai;
    
    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 1000;
    
    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=burst:10m rate=1000r/m;
    
    location / {
        limit_req zone=api burst=20 nodelay;
        limit_req zone=burst burst=100 nodelay;
        
        proxy_pass http://nlds_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
        
        # Caching for static content
        location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## **Monitoring & Performance Tuning**

### **Performance Monitoring Dashboard**
```python
# nlds/optimization/performance_monitor.py

import time
import asyncio
from typing import Dict, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque

@dataclass
class PerformanceMetrics:
    request_count: int = 0
    total_response_time: float = 0.0
    error_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    confidence_scores: deque = field(default_factory=lambda: deque(maxlen=1000))
    response_times: deque = field(default_factory=lambda: deque(maxlen=1000))

class PerformanceMonitor:
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.start_time = time.time()
        
    def record_request(self, response_time: float, confidence_score: float, 
                      cache_hit: bool, error: bool = False):
        """Record request metrics"""
        self.metrics.request_count += 1
        self.metrics.total_response_time += response_time
        self.metrics.response_times.append(response_time)
        self.metrics.confidence_scores.append(confidence_score)
        
        if cache_hit:
            self.metrics.cache_hits += 1
        else:
            self.metrics.cache_misses += 1
            
        if error:
            self.metrics.error_count += 1
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get current performance summary"""
        uptime = time.time() - self.start_time
        
        # Calculate percentiles
        sorted_times = sorted(self.metrics.response_times)
        p50 = sorted_times[len(sorted_times)//2] if sorted_times else 0
        p95 = sorted_times[int(len(sorted_times)*0.95)] if sorted_times else 0
        p99 = sorted_times[int(len(sorted_times)*0.99)] if sorted_times else 0
        
        # Calculate rates
        requests_per_second = self.metrics.request_count / uptime if uptime > 0 else 0
        error_rate = (self.metrics.error_count / self.metrics.request_count * 100) if self.metrics.request_count > 0 else 0
        cache_hit_rate = (self.metrics.cache_hits / (self.metrics.cache_hits + self.metrics.cache_misses) * 100) if (self.metrics.cache_hits + self.metrics.cache_misses) > 0 else 0
        
        # Calculate average confidence
        avg_confidence = sum(self.metrics.confidence_scores) / len(self.metrics.confidence_scores) if self.metrics.confidence_scores else 0
        
        return {
            'uptime_seconds': uptime,
            'total_requests': self.metrics.request_count,
            'requests_per_second': requests_per_second,
            'error_rate_percent': error_rate,
            'cache_hit_rate_percent': cache_hit_rate,
            'average_confidence_score': avg_confidence,
            'response_times': {
                'p50_ms': p50 * 1000,
                'p95_ms': p95 * 1000,
                'p99_ms': p99 * 1000,
                'average_ms': (self.metrics.total_response_time / self.metrics.request_count * 1000) if self.metrics.request_count > 0 else 0
            },
            'sla_compliance': {
                'response_time_sla': p95 < 0.5,  # <500ms
                'error_rate_sla': error_rate < 1.0,  # <1%
                'confidence_sla': avg_confidence >= 0.85  # ≥85%
            }
        }
```

---

**Document Version**: 1.0  
**Last Updated**: July 26, 2025  
**Next Review**: August 26, 2025  
**Owner**: N.L.D.S. Performance Team
