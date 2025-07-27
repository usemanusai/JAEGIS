"""
N.L.D.S. API Monitoring & Analytics
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive API monitoring, analytics, and dashboard system with
real-time metrics, performance tracking, and intelligent alerting.
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging
import statistics
import psutil
import threading
from fastapi import Request, Response
import hashlib

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# MONITORING MODELS
# ============================================================================

class MetricType(str, Enum):
    """Types of metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Alert status."""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ACKNOWLEDGED = "acknowledged"


@dataclass
class Metric:
    """Metric data point."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """System alert."""
    alert_id: str
    name: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    triggered_at: datetime
    resolved_at: Optional[datetime]
    metric_name: str
    threshold_value: float
    current_value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceSnapshot:
    """Performance snapshot."""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    active_connections: int
    request_rate: float
    error_rate: float
    average_response_time: float
    p95_response_time: float
    p99_response_time: float


@dataclass
class APIMetrics:
    """API-specific metrics."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    requests_per_minute: float
    average_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    error_rate: float
    unique_users: int
    top_endpoints: List[Dict[str, Any]]
    top_errors: List[Dict[str, Any]]
    rate_limit_violations: int


# ============================================================================
# METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """
    Comprehensive metrics collection system.
    
    Features:
    - Real-time metric collection
    - Multiple metric types (counter, gauge, histogram, timer)
    - Automatic aggregation and rollup
    - Memory-efficient storage with TTL
    - Label-based filtering and grouping
    """
    
    def __init__(self, retention_hours: int = 24, max_metrics: int = 100000):
        """
        Initialize metrics collector.
        
        Args:
            retention_hours: How long to retain metrics
            max_metrics: Maximum number of metrics to store
        """
        self.retention_hours = retention_hours
        self.max_metrics = max_metrics
        
        # Metric storage
        self.metrics = defaultdict(deque)
        self.counters = defaultdict(float)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.timers = defaultdict(list)
        
        # Aggregated metrics
        self.aggregated_metrics = {}
        
        # Cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
    
    def record_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Record counter metric."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.COUNTER,
            timestamp=datetime.utcnow(),
            labels=labels or {}
        )
        
        self._store_metric(metric)
        self.counters[name] += value
    
    def record_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record gauge metric."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.GAUGE,
            timestamp=datetime.utcnow(),
            labels=labels or {}
        )
        
        self._store_metric(metric)
        self.gauges[name] = value
    
    def record_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record histogram metric."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.HISTOGRAM,
            timestamp=datetime.utcnow(),
            labels=labels or {}
        )
        
        self._store_metric(metric)
        self.histograms[name].append(value)
        
        # Keep only recent values
        if len(self.histograms[name]) > 1000:
            self.histograms[name] = self.histograms[name][-1000:]
    
    def record_timer(self, name: str, duration_ms: float, labels: Optional[Dict[str, str]] = None):
        """Record timer metric."""
        metric = Metric(
            name=name,
            value=duration_ms,
            metric_type=MetricType.TIMER,
            timestamp=datetime.utcnow(),
            labels=labels or {}
        )
        
        self._store_metric(metric)
        self.timers[name].append(duration_ms)
        
        # Keep only recent values
        if len(self.timers[name]) > 1000:
            self.timers[name] = self.timers[name][-1000:]
    
    def _store_metric(self, metric: Metric):
        """Store metric in time series."""
        self.metrics[metric.name].append(metric)
        
        # Limit storage
        if len(self.metrics[metric.name]) > 10000:
            self.metrics[metric.name].popleft()
    
    def get_counter(self, name: str) -> float:
        """Get counter value."""
        return self.counters.get(name, 0.0)
    
    def get_gauge(self, name: str) -> float:
        """Get gauge value."""
        return self.gauges.get(name, 0.0)
    
    def get_histogram_stats(self, name: str) -> Dict[str, float]:
        """Get histogram statistics."""
        values = self.histograms.get(name, [])
        if not values:
            return {}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99)
        }
    
    def get_timer_stats(self, name: str) -> Dict[str, float]:
        """Get timer statistics."""
        values = self.timers.get(name, [])
        if not values:
            return {}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99)
        }
    
    def _percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile."""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int((percentile / 100) * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        return {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {name: self.get_histogram_stats(name) for name in self.histograms},
            "timers": {name: self.get_timer_stats(name) for name in self.timers},
            "total_metrics": sum(len(deque_) for deque_ in self.metrics.values()),
            "metric_names": list(self.metrics.keys())
        }
    
    def _cleanup_loop(self):
        """Background cleanup of old metrics."""
        while True:
            try:
                cutoff_time = datetime.utcnow() - timedelta(hours=self.retention_hours)
                
                for name, metric_deque in self.metrics.items():
                    # Remove old metrics
                    while metric_deque and metric_deque[0].timestamp < cutoff_time:
                        metric_deque.popleft()
                
                time.sleep(300)  # Cleanup every 5 minutes
                
            except Exception as e:
                logger.error(f"Metrics cleanup error: {e}")
                time.sleep(60)


# ============================================================================
# PERFORMANCE MONITOR
# ============================================================================

class PerformanceMonitor:
    """
    System performance monitoring.
    
    Features:
    - CPU, memory, disk, network monitoring
    - Application-specific metrics
    - Performance trend analysis
    - Automatic alerting on thresholds
    """
    
    def __init__(self, metrics_collector: MetricsCollector):
        """
        Initialize performance monitor.
        
        Args:
            metrics_collector: Metrics collector instance
        """
        self.metrics = metrics_collector
        self.snapshots = deque(maxlen=1440)  # 24 hours of minute snapshots
        
        # Performance tracking
        self.request_times = deque(maxlen=10000)
        self.active_requests = 0
        self.total_requests = 0
        self.failed_requests = 0
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def record_request_start(self):
        """Record request start."""
        self.active_requests += 1
        self.total_requests += 1
        self.metrics.record_gauge("active_requests", self.active_requests)
        self.metrics.record_counter("total_requests")
    
    def record_request_end(self, duration_ms: float, success: bool = True):
        """Record request completion."""
        self.active_requests = max(0, self.active_requests - 1)
        self.request_times.append(duration_ms)
        
        if not success:
            self.failed_requests += 1
            self.metrics.record_counter("failed_requests")
        
        self.metrics.record_gauge("active_requests", self.active_requests)
        self.metrics.record_timer("request_duration", duration_ms)
    
    def get_current_snapshot(self) -> PerformanceSnapshot:
        """Get current performance snapshot."""
        # System metrics
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # Request metrics
        request_rate = len([t for t in self.request_times if time.time() - t < 60]) / 60.0
        error_rate = self.failed_requests / max(self.total_requests, 1)
        
        # Response time metrics
        recent_times = list(self.request_times)
        avg_response_time = statistics.mean(recent_times) if recent_times else 0.0
        p95_response_time = self.metrics._percentile(recent_times, 95) if recent_times else 0.0
        p99_response_time = self.metrics._percentile(recent_times, 99) if recent_times else 0.0
        
        return PerformanceSnapshot(
            timestamp=datetime.utcnow(),
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=disk.percent,
            network_io={
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            },
            active_connections=self.active_requests,
            request_rate=request_rate,
            error_rate=error_rate,
            average_response_time=avg_response_time,
            p95_response_time=p95_response_time,
            p99_response_time=p99_response_time
        )
    
    def _monitor_loop(self):
        """Background monitoring loop."""
        while True:
            try:
                snapshot = self.get_current_snapshot()
                self.snapshots.append(snapshot)
                
                # Record system metrics
                self.metrics.record_gauge("cpu_usage", snapshot.cpu_usage)
                self.metrics.record_gauge("memory_usage", snapshot.memory_usage)
                self.metrics.record_gauge("disk_usage", snapshot.disk_usage)
                self.metrics.record_gauge("request_rate", snapshot.request_rate)
                self.metrics.record_gauge("error_rate", snapshot.error_rate)
                
                time.sleep(60)  # Snapshot every minute
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                time.sleep(60)
    
    def get_performance_trends(self, hours: int = 1) -> Dict[str, Any]:
        """Get performance trends over specified hours."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_snapshots = [s for s in self.snapshots if s.timestamp > cutoff_time]
        
        if not recent_snapshots:
            return {}
        
        return {
            "cpu_usage": {
                "min": min(s.cpu_usage for s in recent_snapshots),
                "max": max(s.cpu_usage for s in recent_snapshots),
                "avg": statistics.mean(s.cpu_usage for s in recent_snapshots)
            },
            "memory_usage": {
                "min": min(s.memory_usage for s in recent_snapshots),
                "max": max(s.memory_usage for s in recent_snapshots),
                "avg": statistics.mean(s.memory_usage for s in recent_snapshots)
            },
            "request_rate": {
                "min": min(s.request_rate for s in recent_snapshots),
                "max": max(s.request_rate for s in recent_snapshots),
                "avg": statistics.mean(s.request_rate for s in recent_snapshots)
            },
            "error_rate": {
                "min": min(s.error_rate for s in recent_snapshots),
                "max": max(s.error_rate for s in recent_snapshots),
                "avg": statistics.mean(s.error_rate for s in recent_snapshots)
            },
            "response_time": {
                "min": min(s.average_response_time for s in recent_snapshots),
                "max": max(s.average_response_time for s in recent_snapshots),
                "avg": statistics.mean(s.average_response_time for s in recent_snapshots)
            }
        }


# ============================================================================
# ALERT MANAGER
# ============================================================================

class AlertManager:
    """
    Intelligent alerting system.
    
    Features:
    - Threshold-based alerting
    - Alert aggregation and deduplication
    - Multiple notification channels
    - Alert escalation and acknowledgment
    """
    
    def __init__(self, metrics_collector: MetricsCollector):
        """
        Initialize alert manager.
        
        Args:
            metrics_collector: Metrics collector instance
        """
        self.metrics = metrics_collector
        self.alerts = {}
        self.alert_rules = {}
        self.notification_channels = []
        
        # Load default alert rules
        self._load_default_rules()
        
        # Start alert checking thread
        self.alert_thread = threading.Thread(target=self._alert_loop, daemon=True)
        self.alert_thread.start()
    
    def _load_default_rules(self):
        """Load default alert rules."""
        self.alert_rules = {
            "high_cpu_usage": {
                "metric": "cpu_usage",
                "threshold": 80.0,
                "operator": ">",
                "severity": AlertSeverity.WARNING,
                "description": "High CPU usage detected"
            },
            "high_memory_usage": {
                "metric": "memory_usage",
                "threshold": 85.0,
                "operator": ">",
                "severity": AlertSeverity.WARNING,
                "description": "High memory usage detected"
            },
            "high_error_rate": {
                "metric": "error_rate",
                "threshold": 0.05,  # 5%
                "operator": ">",
                "severity": AlertSeverity.ERROR,
                "description": "High error rate detected"
            },
            "slow_response_time": {
                "metric": "request_duration",
                "threshold": 5000.0,  # 5 seconds
                "operator": ">",
                "severity": AlertSeverity.WARNING,
                "description": "Slow response times detected"
            }
        }
    
    def add_alert_rule(self, name: str, metric: str, threshold: float, operator: str, 
                      severity: AlertSeverity, description: str):
        """Add custom alert rule."""
        self.alert_rules[name] = {
            "metric": metric,
            "threshold": threshold,
            "operator": operator,
            "severity": severity,
            "description": description
        }
    
    def check_alerts(self):
        """Check all alert rules."""
        for rule_name, rule in self.alert_rules.items():
            try:
                current_value = self._get_metric_value(rule["metric"])
                threshold = rule["threshold"]
                operator = rule["operator"]
                
                # Check threshold
                triggered = False
                if operator == ">" and current_value > threshold:
                    triggered = True
                elif operator == "<" and current_value < threshold:
                    triggered = True
                elif operator == "==" and current_value == threshold:
                    triggered = True
                elif operator == ">=" and current_value >= threshold:
                    triggered = True
                elif operator == "<=" and current_value <= threshold:
                    triggered = True
                
                if triggered:
                    self._trigger_alert(rule_name, rule, current_value)
                else:
                    self._resolve_alert(rule_name)
                    
            except Exception as e:
                logger.error(f"Alert check error for {rule_name}: {e}")
    
    def _get_metric_value(self, metric_name: str) -> float:
        """Get current metric value."""
        # Try gauge first
        if metric_name in self.metrics.gauges:
            return self.metrics.gauges[metric_name]
        
        # Try timer stats
        timer_stats = self.metrics.get_timer_stats(metric_name)
        if timer_stats:
            return timer_stats.get("p95", 0.0)
        
        # Try histogram stats
        histogram_stats = self.metrics.get_histogram_stats(metric_name)
        if histogram_stats:
            return histogram_stats.get("p95", 0.0)
        
        return 0.0
    
    def _trigger_alert(self, rule_name: str, rule: Dict[str, Any], current_value: float):
        """Trigger alert."""
        alert_id = f"{rule_name}_{int(time.time())}"
        
        # Check if alert already exists
        existing_alert = None
        for alert in self.alerts.values():
            if alert.name == rule_name and alert.status == AlertStatus.ACTIVE:
                existing_alert = alert
                break
        
        if not existing_alert:
            alert = Alert(
                alert_id=alert_id,
                name=rule_name,
                description=rule["description"],
                severity=rule["severity"],
                status=AlertStatus.ACTIVE,
                triggered_at=datetime.utcnow(),
                resolved_at=None,
                metric_name=rule["metric"],
                threshold_value=rule["threshold"],
                current_value=current_value
            )
            
            self.alerts[alert_id] = alert
            self._send_alert_notification(alert)
            
            logger.warning(f"Alert triggered: {rule_name} - {rule['description']}")
    
    def _resolve_alert(self, rule_name: str):
        """Resolve alert."""
        for alert in self.alerts.values():
            if alert.name == rule_name and alert.status == AlertStatus.ACTIVE:
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = datetime.utcnow()
                
                logger.info(f"Alert resolved: {rule_name}")
                break
    
    def _send_alert_notification(self, alert: Alert):
        """Send alert notification."""
        # In production, this would send notifications via email, Slack, etc.
        logger.warning(f"ALERT: {alert.name} - {alert.description} (Value: {alert.current_value}, Threshold: {alert.threshold_value})")
    
    def _alert_loop(self):
        """Background alert checking loop."""
        while True:
            try:
                self.check_alerts()
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Alert loop error: {e}")
                time.sleep(30)
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts."""
        return [alert for alert in self.alerts.values() if alert.status == AlertStatus.ACTIVE]
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge alert."""
        if alert_id in self.alerts:
            self.alerts[alert_id].status = AlertStatus.ACKNOWLEDGED
            return True
        return False


# ============================================================================
# ANALYTICS DASHBOARD
# ============================================================================

class AnalyticsDashboard:
    """
    Comprehensive analytics dashboard.
    
    Features:
    - Real-time metrics visualization
    - Historical trend analysis
    - User behavior analytics
    - Performance insights
    - Custom dashboards
    """
    
    def __init__(self, metrics_collector: MetricsCollector, performance_monitor: PerformanceMonitor, 
                 alert_manager: AlertManager):
        """
        Initialize analytics dashboard.
        
        Args:
            metrics_collector: Metrics collector instance
            performance_monitor: Performance monitor instance
            alert_manager: Alert manager instance
        """
        self.metrics = metrics_collector
        self.performance = performance_monitor
        self.alerts = alert_manager
        
        # User analytics
        self.user_sessions = defaultdict(dict)
        self.endpoint_usage = defaultdict(int)
        self.error_tracking = defaultdict(int)
    
    def record_user_activity(self, user_id: str, endpoint: str, success: bool, response_time: float):
        """Record user activity."""
        self.endpoint_usage[endpoint] += 1
        
        if not success:
            self.error_tracking[endpoint] += 1
        
        # Update user session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "first_seen": datetime.utcnow(),
                "last_seen": datetime.utcnow(),
                "request_count": 0,
                "total_response_time": 0.0,
                "endpoints_used": set()
            }
        
        session = self.user_sessions[user_id]
        session["last_seen"] = datetime.utcnow()
        session["request_count"] += 1
        session["total_response_time"] += response_time
        session["endpoints_used"].add(endpoint)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        # Current metrics
        current_snapshot = self.performance.get_current_snapshot()
        metrics_summary = self.metrics.get_metrics_summary()
        active_alerts = self.alerts.get_active_alerts()
        
        # API metrics
        api_metrics = self._calculate_api_metrics()
        
        # User analytics
        user_analytics = self._calculate_user_analytics()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system_health": {
                "status": "healthy" if len(active_alerts) == 0 else "degraded",
                "cpu_usage": current_snapshot.cpu_usage,
                "memory_usage": current_snapshot.memory_usage,
                "disk_usage": current_snapshot.disk_usage,
                "active_connections": current_snapshot.active_connections,
                "request_rate": current_snapshot.request_rate,
                "error_rate": current_snapshot.error_rate
            },
            "api_metrics": api_metrics,
            "user_analytics": user_analytics,
            "alerts": {
                "active_count": len(active_alerts),
                "alerts": [asdict(alert) for alert in active_alerts[:10]]  # Top 10
            },
            "performance_trends": self.performance.get_performance_trends(1),
            "metrics_summary": metrics_summary
        }
    
    def _calculate_api_metrics(self) -> APIMetrics:
        """Calculate API-specific metrics."""
        total_requests = self.metrics.get_counter("total_requests")
        failed_requests = self.metrics.get_counter("failed_requests")
        successful_requests = total_requests - failed_requests
        
        # Response time stats
        timer_stats = self.metrics.get_timer_stats("request_duration")
        
        # Top endpoints
        top_endpoints = sorted(
            [{"endpoint": k, "count": v} for k, v in self.endpoint_usage.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]
        
        # Top errors
        top_errors = sorted(
            [{"endpoint": k, "errors": v} for k, v in self.error_tracking.items()],
            key=lambda x: x["errors"],
            reverse=True
        )[:10]
        
        return APIMetrics(
            total_requests=int(total_requests),
            successful_requests=int(successful_requests),
            failed_requests=int(failed_requests),
            requests_per_minute=self.performance.get_current_snapshot().request_rate,
            average_response_time_ms=timer_stats.get("mean", 0.0),
            p95_response_time_ms=timer_stats.get("p95", 0.0),
            p99_response_time_ms=timer_stats.get("p99", 0.0),
            error_rate=failed_requests / max(total_requests, 1),
            unique_users=len(self.user_sessions),
            top_endpoints=top_endpoints,
            top_errors=top_errors,
            rate_limit_violations=int(self.metrics.get_counter("rate_limit_violations"))
        )
    
    def _calculate_user_analytics(self) -> Dict[str, Any]:
        """Calculate user analytics."""
        if not self.user_sessions:
            return {}
        
        # Active users (last hour)
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        active_users = len([
            s for s in self.user_sessions.values()
            if s["last_seen"] > one_hour_ago
        ])
        
        # Average session duration
        session_durations = [
            (s["last_seen"] - s["first_seen"]).total_seconds()
            for s in self.user_sessions.values()
        ]
        avg_session_duration = statistics.mean(session_durations) if session_durations else 0.0
        
        # Average requests per user
        avg_requests_per_user = statistics.mean([
            s["request_count"] for s in self.user_sessions.values()
        ]) if self.user_sessions else 0.0
        
        return {
            "total_users": len(self.user_sessions),
            "active_users_1h": active_users,
            "average_session_duration_seconds": avg_session_duration,
            "average_requests_per_user": avg_requests_per_user,
            "most_popular_endpoints": sorted(
                self.endpoint_usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }


# ============================================================================
# MONITORING UTILITIES
# ============================================================================

def create_monitoring_system() -> Tuple[MetricsCollector, PerformanceMonitor, AlertManager, AnalyticsDashboard]:
    """Create complete monitoring system."""
    metrics_collector = MetricsCollector()
    performance_monitor = PerformanceMonitor(metrics_collector)
    alert_manager = AlertManager(metrics_collector)
    analytics_dashboard = AnalyticsDashboard(metrics_collector, performance_monitor, alert_manager)
    
    return metrics_collector, performance_monitor, alert_manager, analytics_dashboard


def monitoring_middleware(metrics_collector: MetricsCollector, performance_monitor: PerformanceMonitor,
                         analytics_dashboard: AnalyticsDashboard):
    """Create monitoring middleware for FastAPI."""
    
    async def middleware(request: Request, call_next):
        start_time = time.time()
        
        # Record request start
        performance_monitor.record_request_start()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Record metrics
            success = 200 <= response.status_code < 400
            performance_monitor.record_request_end(duration_ms, success)
            
            # Record user activity
            user_id = getattr(request.state, 'user_id', 'anonymous')
            analytics_dashboard.record_user_activity(
                user_id=user_id,
                endpoint=request.url.path,
                success=success,
                response_time=duration_ms
            )
            
            # Add monitoring headers
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
            response.headers["X-Request-ID"] = getattr(request.state, 'request_id', 'unknown')
            
            return response
            
        except Exception as e:
            # Record error
            duration_ms = (time.time() - start_time) * 1000
            performance_monitor.record_request_end(duration_ms, False)
            
            # Record error metrics
            metrics_collector.record_counter("request_errors")
            
            raise
    
    return middleware
