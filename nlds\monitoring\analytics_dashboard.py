"""
N.L.D.S. API Monitoring & Analytics Dashboard
Real-time monitoring, usage analytics, and performance tracking for N.L.D.S. API
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

logger = logging.getLogger(__name__)


@dataclass
class APIMetrics:
    """API performance metrics."""
    timestamp: datetime
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    user_id: Optional[str]
    rate_limit_tier: str
    confidence_score: Optional[float]
    processing_dimensions: List[str]
    squad_selected: Optional[str]
    mode_selected: Optional[int]


@dataclass
class UsageStatistics:
    """Usage statistics summary."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    requests_per_minute: float
    unique_users: int
    top_endpoints: List[Dict[str, Any]]
    error_rate: float


@dataclass
class PerformanceMetrics:
    """Performance metrics summary."""
    avg_confidence_score: float
    high_confidence_rate: float
    avg_processing_time: float
    squad_distribution: Dict[str, int]
    mode_distribution: Dict[str, int]
    dimension_usage: Dict[str, int]


class NLDSAnalyticsDashboard:
    """
    Comprehensive analytics dashboard for N.L.D.S. API monitoring.
    
    Provides real-time monitoring, usage analytics, performance tracking,
    and interactive dashboards for system observability.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379", 
                 postgres_url: str = "postgresql://localhost/nlds"):
        self.redis_client = redis.from_url(redis_url)
        self.postgres_url = postgres_url
        
        # In-memory metrics storage for real-time data
        self.recent_metrics: deque = deque(maxlen=10000)
        self.real_time_stats = {
            "requests_per_second": deque(maxlen=300),  # 5 minutes at 1-second intervals
            "response_times": deque(maxlen=1000),
            "error_rates": deque(maxlen=300),
            "confidence_scores": deque(maxlen=1000)
        }
        
        # Performance targets
        self.performance_targets = {
            "response_time_ms": 500,
            "confidence_threshold": 0.85,
            "error_rate_threshold": 0.05,
            "availability_target": 0.995
        }
        
        # Initialize database
        self._initialize_database()
        
        # Start background tasks
        asyncio.create_task(self._collect_real_time_metrics())
        asyncio.create_task(self._aggregate_metrics())
        
        logger.info("N.L.D.S. Analytics Dashboard initialized")
    
    def _initialize_database(self):
        """Initialize PostgreSQL database for metrics storage."""
        try:
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor() as cur:
                    # Create metrics table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS api_metrics (
                            id SERIAL PRIMARY KEY,
                            timestamp TIMESTAMP NOT NULL,
                            endpoint VARCHAR(255) NOT NULL,
                            method VARCHAR(10) NOT NULL,
                            status_code INTEGER NOT NULL,
                            response_time_ms FLOAT NOT NULL,
                            user_id VARCHAR(255),
                            rate_limit_tier VARCHAR(50),
                            confidence_score FLOAT,
                            processing_dimensions TEXT[],
                            squad_selected VARCHAR(100),
                            mode_selected INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    
                    # Create indexes
                    cur.execute("CREATE INDEX IF NOT EXISTS idx_api_metrics_timestamp ON api_metrics(timestamp)")
                    cur.execute("CREATE INDEX IF NOT EXISTS idx_api_metrics_endpoint ON api_metrics(endpoint)")
                    cur.execute("CREATE INDEX IF NOT EXISTS idx_api_metrics_user_id ON api_metrics(user_id)")
                    
                    # Create aggregated metrics table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS metrics_hourly (
                            id SERIAL PRIMARY KEY,
                            hour_timestamp TIMESTAMP NOT NULL,
                            endpoint VARCHAR(255) NOT NULL,
                            total_requests INTEGER NOT NULL,
                            successful_requests INTEGER NOT NULL,
                            failed_requests INTEGER NOT NULL,
                            avg_response_time FLOAT NOT NULL,
                            p95_response_time FLOAT NOT NULL,
                            p99_response_time FLOAT NOT NULL,
                            avg_confidence_score FLOAT,
                            unique_users INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(hour_timestamp, endpoint)
                        )
                    """)
                    
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    async def record_api_request(self, request: Request, response: Response, 
                                response_time_ms: float, **kwargs):
        """Record API request metrics."""
        
        metrics = APIMetrics(
            timestamp=datetime.utcnow(),
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            user_id=kwargs.get('user_id'),
            rate_limit_tier=kwargs.get('rate_limit_tier', 'basic'),
            confidence_score=kwargs.get('confidence_score'),
            processing_dimensions=kwargs.get('processing_dimensions', []),
            squad_selected=kwargs.get('squad_selected'),
            mode_selected=kwargs.get('mode_selected')
        )
        
        # Store in memory for real-time access
        self.recent_metrics.append(metrics)
        
        # Store in Redis for fast access
        await self._store_in_redis(metrics)
        
        # Store in PostgreSQL for long-term analysis
        await self._store_in_postgres(metrics)
        
        # Update real-time statistics
        self._update_real_time_stats(metrics)
    
    async def _store_in_redis(self, metrics: APIMetrics):
        """Store metrics in Redis for fast access."""
        try:
            # Store recent metrics
            key = f"metrics:recent:{int(time.time())}"
            self.redis_client.setex(key, 3600, json.dumps(asdict(metrics), default=str))
            
            # Update counters
            minute_key = f"metrics:minute:{datetime.utcnow().strftime('%Y%m%d%H%M')}"
            hour_key = f"metrics:hour:{datetime.utcnow().strftime('%Y%m%d%H')}"
            
            pipe = self.redis_client.pipeline()
            pipe.incr(minute_key)
            pipe.expire(minute_key, 3600)
            pipe.incr(hour_key)
            pipe.expire(hour_key, 86400)
            pipe.execute()
            
        except Exception as e:
            logger.error(f"Redis storage failed: {e}")
    
    async def _store_in_postgres(self, metrics: APIMetrics):
        """Store metrics in PostgreSQL for long-term analysis."""
        try:
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO api_metrics (
                            timestamp, endpoint, method, status_code, response_time_ms,
                            user_id, rate_limit_tier, confidence_score, processing_dimensions,
                            squad_selected, mode_selected
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        metrics.timestamp, metrics.endpoint, metrics.method,
                        metrics.status_code, metrics.response_time_ms, metrics.user_id,
                        metrics.rate_limit_tier, metrics.confidence_score,
                        metrics.processing_dimensions, metrics.squad_selected,
                        metrics.mode_selected
                    ))
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"PostgreSQL storage failed: {e}")
    
    def _update_real_time_stats(self, metrics: APIMetrics):
        """Update real-time statistics."""
        now = time.time()
        
        # Update requests per second
        self.real_time_stats["requests_per_second"].append((now, 1))
        
        # Update response times
        self.real_time_stats["response_times"].append((now, metrics.response_time_ms))
        
        # Update error rates
        is_error = 1 if metrics.status_code >= 400 else 0
        self.real_time_stats["error_rates"].append((now, is_error))
        
        # Update confidence scores
        if metrics.confidence_score is not None:
            self.real_time_stats["confidence_scores"].append((now, metrics.confidence_score))
    
    async def _collect_real_time_metrics(self):
        """Background task to collect real-time metrics."""
        while True:
            try:
                # Clean up old data
                cutoff_time = time.time() - 300  # 5 minutes
                
                for stat_name, stat_data in self.real_time_stats.items():
                    while stat_data and stat_data[0][0] < cutoff_time:
                        stat_data.popleft()
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Real-time metrics collection error: {e}")
                await asyncio.sleep(5)
    
    async def _aggregate_metrics(self):
        """Background task to aggregate metrics hourly."""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                await self._create_hourly_aggregates()
                
            except Exception as e:
                logger.error(f"Metrics aggregation error: {e}")
                await asyncio.sleep(300)
    
    async def _create_hourly_aggregates(self):
        """Create hourly aggregated metrics."""
        try:
            current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
            previous_hour = current_hour - timedelta(hours=1)
            
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Aggregate metrics for previous hour
                    cur.execute("""
                        SELECT 
                            endpoint,
                            COUNT(*) as total_requests,
                            COUNT(*) FILTER (WHERE status_code < 400) as successful_requests,
                            COUNT(*) FILTER (WHERE status_code >= 400) as failed_requests,
                            AVG(response_time_ms) as avg_response_time,
                            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms) as p95_response_time,
                            PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY response_time_ms) as p99_response_time,
                            AVG(confidence_score) as avg_confidence_score,
                            COUNT(DISTINCT user_id) as unique_users
                        FROM api_metrics 
                        WHERE timestamp >= %s AND timestamp < %s
                        GROUP BY endpoint
                    """, (previous_hour, current_hour))
                    
                    results = cur.fetchall()
                    
                    # Insert aggregated data
                    for row in results:
                        cur.execute("""
                            INSERT INTO metrics_hourly (
                                hour_timestamp, endpoint, total_requests, successful_requests,
                                failed_requests, avg_response_time, p95_response_time,
                                p99_response_time, avg_confidence_score, unique_users
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (hour_timestamp, endpoint) DO UPDATE SET
                                total_requests = EXCLUDED.total_requests,
                                successful_requests = EXCLUDED.successful_requests,
                                failed_requests = EXCLUDED.failed_requests,
                                avg_response_time = EXCLUDED.avg_response_time,
                                p95_response_time = EXCLUDED.p95_response_time,
                                p99_response_time = EXCLUDED.p99_response_time,
                                avg_confidence_score = EXCLUDED.avg_confidence_score,
                                unique_users = EXCLUDED.unique_users
                        """, (
                            previous_hour, row['endpoint'], row['total_requests'],
                            row['successful_requests'], row['failed_requests'],
                            row['avg_response_time'], row['p95_response_time'],
                            row['p99_response_time'], row['avg_confidence_score'],
                            row['unique_users']
                        ))
                    
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Hourly aggregation failed: {e}")
    
    async def get_usage_statistics(self, hours: int = 24) -> UsageStatistics:
        """Get usage statistics for specified time period."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Get basic statistics
                    cur.execute("""
                        SELECT 
                            COUNT(*) as total_requests,
                            COUNT(*) FILTER (WHERE status_code < 400) as successful_requests,
                            COUNT(*) FILTER (WHERE status_code >= 400) as failed_requests,
                            AVG(response_time_ms) as avg_response_time,
                            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms) as p95_response_time,
                            PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY response_time_ms) as p99_response_time,
                            COUNT(DISTINCT user_id) as unique_users
                        FROM api_metrics 
                        WHERE timestamp >= %s
                    """, (cutoff_time,))
                    
                    stats = cur.fetchone()
                    
                    # Get top endpoints
                    cur.execute("""
                        SELECT endpoint, COUNT(*) as requests
                        FROM api_metrics 
                        WHERE timestamp >= %s
                        GROUP BY endpoint
                        ORDER BY requests DESC
                        LIMIT 10
                    """, (cutoff_time,))
                    
                    top_endpoints = [dict(row) for row in cur.fetchall()]
                    
                    # Calculate requests per minute
                    requests_per_minute = stats['total_requests'] / (hours * 60) if hours > 0 else 0
                    
                    # Calculate error rate
                    error_rate = (stats['failed_requests'] / stats['total_requests']) if stats['total_requests'] > 0 else 0
                    
                    return UsageStatistics(
                        total_requests=stats['total_requests'],
                        successful_requests=stats['successful_requests'],
                        failed_requests=stats['failed_requests'],
                        avg_response_time=stats['avg_response_time'] or 0,
                        p95_response_time=stats['p95_response_time'] or 0,
                        p99_response_time=stats['p99_response_time'] or 0,
                        requests_per_minute=requests_per_minute,
                        unique_users=stats['unique_users'],
                        top_endpoints=top_endpoints,
                        error_rate=error_rate
                    )
                    
        except Exception as e:
            logger.error(f"Usage statistics query failed: {e}")
            return UsageStatistics(0, 0, 0, 0, 0, 0, 0, 0, [], 0)
    
    async def get_performance_metrics(self, hours: int = 24) -> PerformanceMetrics:
        """Get performance metrics for specified time period."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            with psycopg2.connect(self.postgres_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Get confidence metrics
                    cur.execute("""
                        SELECT 
                            AVG(confidence_score) as avg_confidence_score,
                            COUNT(*) FILTER (WHERE confidence_score >= 0.85) * 100.0 / COUNT(*) as high_confidence_rate,
                            AVG(response_time_ms) as avg_processing_time
                        FROM api_metrics 
                        WHERE timestamp >= %s AND confidence_score IS NOT NULL
                    """, (cutoff_time,))
                    
                    metrics = cur.fetchone()
                    
                    # Get squad distribution
                    cur.execute("""
                        SELECT squad_selected, COUNT(*) as count
                        FROM api_metrics 
                        WHERE timestamp >= %s AND squad_selected IS NOT NULL
                        GROUP BY squad_selected
                    """, (cutoff_time,))
                    
                    squad_distribution = {row['squad_selected']: row['count'] for row in cur.fetchall()}
                    
                    # Get mode distribution
                    cur.execute("""
                        SELECT mode_selected, COUNT(*) as count
                        FROM api_metrics 
                        WHERE timestamp >= %s AND mode_selected IS NOT NULL
                        GROUP BY mode_selected
                    """, (cutoff_time,))
                    
                    mode_distribution = {str(row['mode_selected']): row['count'] for row in cur.fetchall()}
                    
                    # Get dimension usage (simplified)
                    dimension_usage = {"logical": 0, "emotional": 0, "creative": 0, "all": 0}
                    
                    return PerformanceMetrics(
                        avg_confidence_score=metrics['avg_confidence_score'] or 0,
                        high_confidence_rate=metrics['high_confidence_rate'] or 0,
                        avg_processing_time=metrics['avg_processing_time'] or 0,
                        squad_distribution=squad_distribution,
                        mode_distribution=mode_distribution,
                        dimension_usage=dimension_usage
                    )
                    
        except Exception as e:
            logger.error(f"Performance metrics query failed: {e}")
            return PerformanceMetrics(0, 0, 0, {}, {}, {})
    
    def get_real_time_dashboard_data(self) -> Dict[str, Any]:
        """Get real-time dashboard data."""
        now = time.time()
        cutoff = now - 300  # Last 5 minutes
        
        # Calculate requests per second
        recent_requests = [req for req in self.real_time_stats["requests_per_second"] if req[0] > cutoff]
        rps = len(recent_requests) / 300 if recent_requests else 0
        
        # Calculate average response time
        recent_response_times = [rt[1] for rt in self.real_time_stats["response_times"] if rt[0] > cutoff]
        avg_response_time = sum(recent_response_times) / len(recent_response_times) if recent_response_times else 0
        
        # Calculate error rate
        recent_errors = [err for err in self.real_time_stats["error_rates"] if err[0] > cutoff]
        error_rate = sum(err[1] for err in recent_errors) / len(recent_errors) if recent_errors else 0
        
        # Calculate average confidence
        recent_confidence = [conf[1] for conf in self.real_time_stats["confidence_scores"] if conf[0] > cutoff]
        avg_confidence = sum(recent_confidence) / len(recent_confidence) if recent_confidence else 0
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "requests_per_second": rps,
            "avg_response_time_ms": avg_response_time,
            "error_rate": error_rate,
            "avg_confidence_score": avg_confidence,
            "performance_targets": self.performance_targets,
            "target_status": {
                "response_time": avg_response_time <= self.performance_targets["response_time_ms"],
                "confidence": avg_confidence >= self.performance_targets["confidence_threshold"],
                "error_rate": error_rate <= self.performance_targets["error_rate_threshold"]
            }
        }
    
    def generate_performance_charts(self, hours: int = 24) -> Dict[str, str]:
        """Generate performance charts as JSON for frontend."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            with psycopg2.connect(self.postgres_url) as conn:
                # Response time chart
                df_response = pd.read_sql("""
                    SELECT 
                        DATE_TRUNC('hour', timestamp) as hour,
                        AVG(response_time_ms) as avg_response_time
                    FROM api_metrics 
                    WHERE timestamp >= %s
                    GROUP BY hour
                    ORDER BY hour
                """, conn, params=(cutoff_time,))
                
                response_chart = px.line(
                    df_response, 
                    x='hour', 
                    y='avg_response_time',
                    title='Average Response Time Over Time'
                )
                
                # Confidence score chart
                df_confidence = pd.read_sql("""
                    SELECT 
                        DATE_TRUNC('hour', timestamp) as hour,
                        AVG(confidence_score) as avg_confidence
                    FROM api_metrics 
                    WHERE timestamp >= %s AND confidence_score IS NOT NULL
                    GROUP BY hour
                    ORDER BY hour
                """, conn, params=(cutoff_time,))
                
                confidence_chart = px.line(
                    df_confidence,
                    x='hour',
                    y='avg_confidence',
                    title='Average Confidence Score Over Time'
                )
                
                return {
                    "response_time_chart": json.dumps(response_chart, cls=PlotlyJSONEncoder),
                    "confidence_chart": json.dumps(confidence_chart, cls=PlotlyJSONEncoder)
                }
                
        except Exception as e:
            logger.error(f"Chart generation failed: {e}")
            return {}


# FastAPI integration for dashboard endpoints
def create_dashboard_app(analytics: NLDSAnalyticsDashboard) -> FastAPI:
    """Create FastAPI app for analytics dashboard."""
    
    app = FastAPI(title="N.L.D.S. Analytics Dashboard")
    templates = Jinja2Templates(directory="templates")
    
    @app.get("/", response_class=HTMLResponse)
    async def dashboard_home():
        """Main dashboard page."""
        return """
        <html>
        <head><title>N.L.D.S. Analytics Dashboard</title></head>
        <body>
        <h1>N.L.D.S. Analytics Dashboard</h1>
        <p>Real-time monitoring and analytics for N.L.D.S. API</p>
        <ul>
            <li><a href="/api/real-time">Real-time Metrics</a></li>
            <li><a href="/api/usage">Usage Statistics</a></li>
            <li><a href="/api/performance">Performance Metrics</a></li>
        </ul>
        </body>
        </html>
        """
    
    @app.get("/api/real-time")
    async def get_real_time_metrics():
        """Get real-time metrics."""
        return analytics.get_real_time_dashboard_data()
    
    @app.get("/api/usage")
    async def get_usage_stats(hours: int = 24):
        """Get usage statistics."""
        stats = await analytics.get_usage_statistics(hours)
        return asdict(stats)
    
    @app.get("/api/performance")
    async def get_performance_metrics(hours: int = 24):
        """Get performance metrics."""
        metrics = await analytics.get_performance_metrics(hours)
        return asdict(metrics)
    
    @app.get("/api/charts")
    async def get_charts(hours: int = 24):
        """Get performance charts."""
        return analytics.generate_performance_charts(hours)
    
    return app


# Example usage
if __name__ == "__main__":
    import uvicorn
    
    # Initialize analytics dashboard
    analytics = NLDSAnalyticsDashboard()
    
    # Create dashboard app
    dashboard_app = create_dashboard_app(analytics)
    
    # Run dashboard
    uvicorn.run(dashboard_app, host="0.0.0.0", port=8001)
