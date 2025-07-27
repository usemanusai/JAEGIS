"""
JAEGIS Configuration Management System - Real-time Statistics Dashboard
Dashboard for displaying workflow efficiency statistics and parameter impact analysis
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import statistics
from collections import defaultdict, deque

from ..core.config_engine import ConfigurationEngine
from ..agents.frequency_controller import FrequencyControllerAgent
from ..agents.suggestions_engine import IntelligentSuggestionsEngine
from ..core.agent_communication import AgentCommunicationHub

logger = logging.getLogger(__name__)

@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    value: float
    metadata: Dict[str, Any] = None

@dataclass
class DashboardWidget:
    """Dashboard widget configuration"""
    widget_id: str
    title: str
    widget_type: str  # "chart", "gauge", "table", "text"
    data_source: str
    refresh_interval: int = 30  # seconds
    config: Dict[str, Any] = None

class RealTimeStatisticsDashboard:
    """Real-time dashboard for configuration statistics and metrics"""
    
    def __init__(self, config_engine: ConfigurationEngine,
                 frequency_controller: FrequencyControllerAgent,
                 suggestions_engine: IntelligentSuggestionsEngine,
                 communication_hub: AgentCommunicationHub):
        self.config_engine = config_engine
        self.frequency_controller = frequency_controller
        self.suggestions_engine = suggestions_engine
        self.communication_hub = communication_hub
        
        # Metrics storage (in-memory for demo, would use time-series DB in production)
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.current_metrics: Dict[str, float] = {}
        
        # Dashboard configuration
        self.widgets: Dict[str, DashboardWidget] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.workflow_metrics: Dict[str, List[float]] = defaultdict(list)
        self.agent_performance: Dict[str, Dict[str, float]] = defaultdict(dict)
        
        # Initialize default widgets
        self._initialize_default_widgets()
        
        # Start metrics collection
        asyncio.create_task(self._collect_metrics_loop())
        
        logger.info("Real-time Statistics Dashboard initialized")
    
    def _initialize_default_widgets(self):
        """Initialize default dashboard widgets"""
        self.widgets = {
            "frequency_parameters": DashboardWidget(
                widget_id="frequency_parameters",
                title="Frequency Parameters",
                widget_type="gauge",
                data_source="frequency_controller",
                refresh_interval=10,
                config={
                    "parameters": ["research_intensity", "task_decomposition", "validation_thoroughness", "documentation_detail"],
                    "display_mode": "radial_gauge"
                }
            ),
            "agent_utilization": DashboardWidget(
                widget_id="agent_utilization",
                title="Agent Utilization",
                widget_type="chart",
                data_source="frequency_controller",
                refresh_interval=15,
                config={
                    "chart_type": "bar",
                    "tiers": ["tier_1_orchestrator", "tier_2_primary", "tier_3_secondary", "tier_4_specialized"]
                }
            ),
            "workflow_efficiency": DashboardWidget(
                widget_id="workflow_efficiency",
                title="Workflow Efficiency Trends",
                widget_type="chart",
                data_source="performance_metrics",
                refresh_interval=30,
                config={
                    "chart_type": "line",
                    "time_range": "24h",
                    "metrics": ["response_time", "quality_score", "completion_rate"]
                }
            ),
            "parameter_impact": DashboardWidget(
                widget_id="parameter_impact",
                title="Parameter Impact Analysis",
                widget_type="table",
                data_source="impact_analysis",
                refresh_interval=60,
                config={
                    "columns": ["parameter", "change", "impact_level", "performance_delta"],
                    "sort_by": "impact_level"
                }
            ),
            "system_health": DashboardWidget(
                widget_id="system_health",
                title="System Health",
                widget_type="text",
                data_source="system_status",
                refresh_interval=20,
                config={
                    "metrics": ["active_agents", "message_queue_size", "error_rate", "uptime"]
                }
            ),
            "suggestions_summary": DashboardWidget(
                widget_id="suggestions_summary",
                title="AI Suggestions Summary",
                widget_type="table",
                data_source="suggestions_engine",
                refresh_interval=45,
                config={
                    "show_recent": 5,
                    "columns": ["title", "confidence", "priority", "category"]
                }
            )
        }
    
    async def _collect_metrics_loop(self):
        """Continuously collect metrics from various sources"""
        while True:
            try:
                await self._collect_frequency_metrics()
                await self._collect_agent_metrics()
                await self._collect_performance_metrics()
                await self._collect_system_metrics()
                
                # Update current metrics summary
                self._update_current_metrics()
                
                await asyncio.sleep(10)  # Collect every 10 seconds
                
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                await asyncio.sleep(30)  # Wait longer on error
    
    async def _collect_frequency_metrics(self):
        """Collect frequency parameter metrics"""
        current_config = self.config_engine.get_current_config()
        freq_params = current_config.frequency_parameters
        
        timestamp = datetime.now()
        
        # Record frequency parameters
        for param_name in ["research_intensity", "task_decomposition", "validation_thoroughness", "documentation_detail"]:
            value = getattr(freq_params, param_name)
            metric_point = MetricPoint(timestamp=timestamp, value=value)
            self.metrics_history[f"frequency.{param_name}"].append(metric_point)
        
        # Record agent utilization
        for tier, utilization in freq_params.agent_utilization.items():
            metric_point = MetricPoint(timestamp=timestamp, value=utilization)
            self.metrics_history[f"agent_utilization.{tier.value}"].append(metric_point)
    
    async def _collect_agent_metrics(self):
        """Collect agent performance metrics"""
        comm_stats = self.communication_hub.get_communication_statistics()
        timestamp = datetime.now()
        
        # Record communication metrics
        for metric_name, value in comm_stats.items():
            if isinstance(value, (int, float)):
                metric_point = MetricPoint(timestamp=timestamp, value=value)
                self.metrics_history[f"communication.{metric_name}"].append(metric_point)
        
        # Record agent-specific metrics
        for agent_info in self.communication_hub.get_all_agents():
            if agent_info.last_heartbeat:
                # Calculate response time (time since last heartbeat)
                response_time = (timestamp - agent_info.last_heartbeat).total_seconds()
                metric_point = MetricPoint(
                    timestamp=timestamp, 
                    value=response_time,
                    metadata={"agent_id": agent_info.agent_id, "agent_name": agent_info.agent_name}
                )
                self.metrics_history[f"agent.{agent_info.agent_id}.response_time"].append(metric_point)
    
    async def _collect_performance_metrics(self):
        """Collect workflow performance metrics"""
        timestamp = datetime.now()
        
        # Simulate performance metrics (in real implementation, these would come from actual workflow data)
        current_config = self.config_engine.get_current_config()
        freq_params = current_config.frequency_parameters
        
        # Calculate efficiency score based on current parameters
        efficiency_score = self._calculate_efficiency_score(freq_params)
        quality_score = self._calculate_quality_score(freq_params)
        speed_score = self._calculate_speed_score(freq_params)
        
        # Record performance metrics
        metrics = {
            "efficiency_score": efficiency_score,
            "quality_score": quality_score,
            "speed_score": speed_score,
            "overall_performance": (efficiency_score + quality_score + speed_score) / 3
        }
        
        for metric_name, value in metrics.items():
            metric_point = MetricPoint(timestamp=timestamp, value=value)
            self.metrics_history[f"performance.{metric_name}"].append(metric_point)
    
    async def _collect_system_metrics(self):
        """Collect system health metrics"""
        timestamp = datetime.now()
        
        # System health indicators
        active_agents = len([a for a in self.communication_hub.get_all_agents() if a.status == "active"])
        total_agents = len(self.communication_hub.get_all_agents())
        queue_size = self.communication_hub.message_queue.qsize()
        
        # Calculate error rate (simplified)
        comm_stats = self.communication_hub.get_communication_statistics()
        total_messages = comm_stats.get("sent", 0) + comm_stats.get("received", 0)
        failed_messages = comm_stats.get("failed", 0)
        error_rate = (failed_messages / total_messages * 100) if total_messages > 0 else 0
        
        # Record system metrics
        system_metrics = {
            "active_agents": active_agents,
            "total_agents": total_agents,
            "agent_availability": (active_agents / total_agents * 100) if total_agents > 0 else 0,
            "message_queue_size": queue_size,
            "error_rate": error_rate
        }
        
        for metric_name, value in system_metrics.items():
            metric_point = MetricPoint(timestamp=timestamp, value=value)
            self.metrics_history[f"system.{metric_name}"].append(metric_point)
    
    def _calculate_efficiency_score(self, freq_params) -> float:
        """Calculate workflow efficiency score based on parameters"""
        # Weighted efficiency calculation
        weights = {
            "research_intensity": 0.2,
            "task_decomposition": 0.3,
            "validation_thoroughness": 0.3,
            "documentation_detail": 0.2
        }
        
        # Optimal values for efficiency (balanced approach)
        optimal_values = {
            "research_intensity": 70,
            "task_decomposition": 65,
            "validation_thoroughness": 80,
            "documentation_detail": 75
        }
        
        efficiency_score = 0
        for param_name, weight in weights.items():
            current_value = getattr(freq_params, param_name)
            optimal_value = optimal_values[param_name]
            
            # Calculate deviation from optimal
            deviation = abs(current_value - optimal_value) / optimal_value
            param_efficiency = max(0, 100 - (deviation * 100))
            
            efficiency_score += param_efficiency * weight
        
        return efficiency_score
    
    def _calculate_quality_score(self, freq_params) -> float:
        """Calculate quality score based on parameters"""
        # Quality is primarily driven by validation thoroughness and research intensity
        validation_weight = 0.6
        research_weight = 0.4
        
        validation_score = freq_params.validation_thoroughness
        research_score = freq_params.research_intensity
        
        return (validation_score * validation_weight) + (research_score * research_weight)
    
    def _calculate_speed_score(self, freq_params) -> float:
        """Calculate speed score based on parameters"""
        # Speed is inversely related to thoroughness parameters
        base_speed = 100
        
        # Penalties for high thoroughness (which slows things down)
        research_penalty = (freq_params.research_intensity - 50) * 0.3 if freq_params.research_intensity > 50 else 0
        validation_penalty = (freq_params.validation_thoroughness - 50) * 0.4 if freq_params.validation_thoroughness > 50 else 0
        decomposition_penalty = (freq_params.task_decomposition - 50) * 0.2 if freq_params.task_decomposition > 50 else 0
        
        speed_score = base_speed - research_penalty - validation_penalty - decomposition_penalty
        return max(0, min(100, speed_score))
    
    def _update_current_metrics(self):
        """Update current metrics summary"""
        self.current_metrics = {}
        
        # Get latest values for key metrics
        for metric_category in ["frequency", "performance", "system", "agent_utilization"]:
            for metric_name, history in self.metrics_history.items():
                if metric_name.startswith(metric_category) and history:
                    latest_point = history[-1]
                    self.current_metrics[metric_name] = latest_point.value
    
    def get_widget_data(self, widget_id: str) -> Dict[str, Any]:
        """Get data for a specific dashboard widget"""
        widget = self.widgets.get(widget_id)
        if not widget:
            return {"error": "Widget not found"}
        
        try:
            if widget.data_source == "frequency_controller":
                return self._get_frequency_widget_data(widget)
            elif widget.data_source == "performance_metrics":
                return self._get_performance_widget_data(widget)
            elif widget.data_source == "impact_analysis":
                return self._get_impact_widget_data(widget)
            elif widget.data_source == "system_status":
                return self._get_system_widget_data(widget)
            elif widget.data_source == "suggestions_engine":
                return self._get_suggestions_widget_data(widget)
            else:
                return {"error": "Unknown data source"}
                
        except Exception as e:
            logger.error(f"Error getting widget data for {widget_id}: {e}")
            return {"error": str(e)}
    
    def _get_frequency_widget_data(self, widget: DashboardWidget) -> Dict[str, Any]:
        """Get frequency parameter widget data"""
        if widget.widget_type == "gauge":
            # Return current frequency parameters for gauge display
            current_config = self.config_engine.get_current_config()
            freq_params = current_config.frequency_parameters
            
            data = {}
            for param_name in widget.config.get("parameters", []):
                value = getattr(freq_params, param_name, 0)
                data[param_name] = {
                    "value": value,
                    "max": 100,
                    "unit": "%",
                    "color": self._get_gauge_color(value)
                }
            
            return {"type": "gauge", "data": data}
        
        elif widget.widget_type == "chart":
            # Return agent utilization chart data
            current_config = self.config_engine.get_current_config()
            freq_params = current_config.frequency_parameters
            
            chart_data = {
                "labels": [],
                "values": [],
                "colors": []
            }
            
            for tier in widget.config.get("tiers", []):
                from ..core.config_schema import AgentTier
                agent_tier = AgentTier(tier)
                utilization = freq_params.agent_utilization.get(agent_tier, 0)
                
                chart_data["labels"].append(tier.replace("_", " ").title())
                chart_data["values"].append(utilization)
                chart_data["colors"].append(self._get_utilization_color(utilization))
            
            return {"type": "bar_chart", "data": chart_data}
    
    def _get_performance_widget_data(self, widget: DashboardWidget) -> Dict[str, Any]:
        """Get performance metrics widget data"""
        time_range = widget.config.get("time_range", "24h")
        metrics = widget.config.get("metrics", [])
        
        # Calculate time range
        if time_range == "24h":
            start_time = datetime.now() - timedelta(hours=24)
        elif time_range == "1h":
            start_time = datetime.now() - timedelta(hours=1)
        else:
            start_time = datetime.now() - timedelta(hours=24)
        
        chart_data = {
            "timestampsseries": {}
        }
        
        # Initialize series
        for metric in metrics:
            chart_data["series"][metric] = []
        
        # Get data points for each metric
        for metric in metrics:
            metric_key = f"performance.{metric}"
            if metric_key in self.metrics_history:
                # Filter by time range and extract data
                filtered_points = [
                    point for point in self.metrics_history[metric_key]
                    if point.timestamp >= start_time
                ]
                
                if filtered_points:
                    # Sample data points (max 100 points for chart)
                    step = max(1, len(filtered_points) // 100)
                    sampled_points = filtered_points[::step]
                    
                    for point in sampled_points:
                        if not chart_data["timestamps"] or point.timestamp not in chart_data["timestamps"]:
                            chart_data["timestamps"].append(point.timestamp.isoformat())
                        chart_data["series"][metric].append(point.value)
        
        return {"type": "line_chart", "data": chart_data}
    
    def _get_impact_widget_data(self, widget: DashboardWidget) -> Dict[str, Any]:
        """Get parameter impact analysis widget data"""
        # Get recent parameter changes from frequency controller
        recent_changes = self.frequency_controller.get_parameter_history(limit=10)
        
        table_data = {
            "headers": ["Parameter", "Change", "Impact Level", "Performance Delta"],
            "rows": []
        }
        
        for change in recent_changes:
            parameter = change.get("parameter", "")
            old_value = change.get("old_value", 0)
            new_value = change.get("new_value", 0)
            
            # Calculate change and impact
            change_amount = new_value - old_value
            change_str = f"{old_value}% → {new_value}% ({change_amount:+d}%)"
            
            # Determine impact level
            if abs(change_amount) >= 30:
                impact_level = "High"
            elif abs(change_amount) >= 15:
                impact_level = "Medium"
            else:
                impact_level = "Low"
            
            # Estimate performance delta (simplified)
            performance_delta = f"{change_amount * 0.5:+.1f}%"
            
            table_data["rows"].append([
                parameter.replace("_", " ").title(),
                change_str,
                impact_level,
                performance_delta
            ])
        
        return {"type": "table", "data": table_data}
    
    def _get_system_widget_data(self, widget: DashboardWidget) -> Dict[str, Any]:
        """Get system health widget data"""
        metrics = widget.config.get("metrics", [])
        
        status_data = {}
        for metric in metrics:
            metric_key = f"system.{metric}"
            if metric_key in self.current_metrics:
                value = self.current_metrics[metric_key]
                
                if metric == "active_agents":
                    status_data[metric] = f"{int(value)} agents"
                elif metric == "message_queue_size":
                    status_data[metric] = f"{int(value)} messages"
                elif metric == "error_rate":
                    status_data[metric] = f"{value:.1f}%"
                elif metric == "uptime":
                    # Calculate uptime (simplified)
                    status_data[metric] = "99.9%"
                else:
                    status_data[metric] = str(value)
        
        return {"type": "status", "data": status_data}
    
    def _get_suggestions_widget_data(self, widget: DashboardWidget) -> Dict[str, Any]:
        """Get AI suggestions widget data"""
        # This would integrate with the suggestions engine
        # For now, return sample data
        
        table_data = {
            "headers": ["Title", "Confidence", "Priority", "Category"],
            "rows": [
                ["Increase Research Intensity", "85%", "Medium", "Parameter"],
                ["Apply Quality Mode", "92%", "High", "Preset"],
                ["Optimize Agent Utilization", "78%", "Low", "Agent"]
            ]
        }
        
        return {"type": "table", "data": table_data}
    
    def _get_gauge_color(self, value: float) -> str:
        """Get color for gauge based on value"""
        if value >= 80:
            return "#28a745"  # Green
        elif value >= 60:
            return "#ffc107"  # Yellow
        elif value >= 40:
            return "#fd7e14"  # Orange
        else:
            return "#dc3545"  # Red
    
    def _get_utilization_color(self, utilization: float) -> str:
        """Get color for utilization based on value"""
        if utilization >= 90:
            return "#007bff"  # Blue
        elif utilization >= 70:
            return "#28a745"  # Green
        elif utilization >= 50:
            return "#ffc107"  # Yellow
        else:
            return "#6c757d"  # Gray
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get overall dashboard summary"""
        current_config = self.config_engine.get_current_config()
        
        # Calculate summary metrics
        freq_params = current_config.frequency_parameters
        avg_frequency = statistics.mean([
            freq_params.research_intensity,
            freq_params.task_decomposition,
            freq_params.validation_thoroughness,
            freq_params.documentation_detail
        ])
        
        avg_utilization = statistics.mean(list(freq_params.agent_utilization.values()))
        
        return {
            "configuration_mode": current_config.mode.value,
            "average_frequency": round(avg_frequency, 1),
            "average_utilization": round(avg_utilization, 1),
            "total_widgets": len(self.widgets),
            "active_metrics": len(self.current_metrics),
            "last_updated": datetime.now().isoformat()
        }
    
    def export_metrics(self, time_range: str = "24h") -> Dict[str, Any]:
        """Export metrics data for analysis"""
        # Calculate time range
        if time_range == "24h":
            start_time = datetime.now() - timedelta(hours=24)
        elif time_range == "1h":
            start_time = datetime.now() - timedelta(hours=1)
        elif time_range == "7d":
            start_time = datetime.now() - timedelta(days=7)
        else:
            start_time = datetime.now() - timedelta(hours=24)
        
        exported_data = {
            "export_timestamp": datetime.now().isoformat(),
            "time_rangetime_range_metrics": {}
        }
        
        # Export all metrics within time range
        for metric_name, history in self.metrics_history.items():
            filtered_points = [
                {
                    "timestamp": point.timestamp.isoformat(),
                    "value": point.value,
                    "metadata": point.metadata
                }
                for point in history
                if point.timestamp >= start_time
            ]
            
            if filtered_points:
                exported_data["metrics"][metric_name] = filtered_points
        
        return exported_data
