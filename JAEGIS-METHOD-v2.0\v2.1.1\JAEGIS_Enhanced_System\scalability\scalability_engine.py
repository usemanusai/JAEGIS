"""
JAEGIS Enhanced System v2.0 - Advanced Scalability Engine
Comprehensive scalability optimization for larger workloads, concurrent users, and expanded agent interactions
Based on latest 2024 scalability patterns including horizontal scaling, load balancing, and distributed architecture
"""

import asyncio
import logging
import time
import psutil
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid
import threading
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import weakref
import json

logger = logging.getLogger(__name__)

class ScalingStrategy(Enum):
    """Scaling strategy types"""
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    ELASTIC = "elastic"
    PREDICTIVE = "predictive"

class LoadBalancingAlgorithm(Enum):
    """Load balancing algorithms"""
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    LEAST_RESPONSE_TIME = "least_response_time"
    CONSISTENT_HASHING = "consistent_hashing"
    ADAPTIVE = "adaptive"

class ResourceType(Enum):
    """Resource types for scaling"""
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK = "network"
    STORAGE = "storage"
    AGENT_INSTANCES = "agent_instances"

@dataclass
class ScalabilityMetrics:
    """Scalability performance metrics"""
    timestamp: datetime
    concurrent_users: int
    active_agents: int
    request_rate: float
    response_time_p95: float
    cpu_utilization: float
    memory_utilization: float
    network_throughput: float
    error_rate: float
    queue_depth: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "concurrent_users": self.concurrent_users,
            "active_agents": self.active_agents,
            "request_rate": self.request_rate,
            "response_time_p95": self.response_time_p95,
            "cpu_utilization": self.cpu_utilization,
            "memory_utilization": self.memory_utilization,
            "network_throughput": self.network_throughput,
            "error_rate": self.error_rate,
            "queue_depth": self.queue_depth
        }

@dataclass
class ScalingRule:
    """Scaling rule configuration"""
    rule_id: str
    name: str
    resource_type: ResourceType
    scaling_strategy: ScalingStrategy
    trigger_threshold: float
    scale_down_threshold: float
    cooldown_period: int  # seconds
    max_instances: int
    min_instances: int
    enabled: bool = True

class AdvancedScalabilityEngine:
    """Advanced scalability engine for JAEGIS Enhanced System"""
    
    def __init__(self):
        # Core scalability components
        self.load_balancer = IntelligentLoadBalancer()
        self.auto_scaler = AutoScalingManager()
        self.resource_manager = DistributedResourceManager()
        self.capacity_planner = CapacityPlanner()
        
        # Monitoring and metrics
        self.metrics_collector = ScalabilityMetricsCollector()
        self.performance_monitor = PerformanceMonitor()
        
        # Agent scaling
        self.agent_scaler = AgentScalingManager()
        self.agent_pool_manager = AgentPoolManager()
        
        # Distributed coordination
        self.cluster_coordinator = ClusterCoordinator()
        self.service_mesh = ServiceMeshManager()
        
        # Predictive scaling
        self.predictive_scaler = PredictiveScaler()
        
        # Configuration
        self.scaling_rules: Dict[str, ScalingRule] = {}
        self.scaling_active = False
        
        logger.info("Advanced Scalability Engine initialized")
    
    async def initialize_scalability_systems(self) -> Dict[str, Any]:
        """Initialize all scalability systems"""
        
        # Initialize load balancer
        lb_config = await self.load_balancer.initialize()
        
        # Initialize auto-scaling
        autoscale_config = await self.auto_scaler.initialize()
        
        # Initialize resource management
        resource_config = await self.resource_manager.initialize()
        
        # Initialize agent scaling
        agent_scaling_config = await self.agent_scaler.initialize()
        
        # Initialize cluster coordination
        cluster_config = await self.cluster_coordinator.initialize()
        
        # Initialize service mesh
        mesh_config = await self.service_mesh.initialize()
        
        # Initialize predictive scaling
        predictive_config = await self.predictive_scaler.initialize()
        
        # Set up default scaling rules
        await self._setup_default_scaling_rules()
        
        # Start monitoring
        await self._start_scalability_monitoring()
        
        return {
            "scalability_systems_initialized": True,
            "load_balancer": lb_config,
            "auto_scaler": autoscale_config,
            "resource_manager": resource_config,
            "agent_scaling": agent_scaling_config,
            "cluster_coordination": cluster_config,
            "service_mesh": mesh_config,
            "predictive_scaling": predictive_config,
            "scaling_rules": len(self.scaling_rules)
        }
    
    async def _setup_default_scaling_rules(self):
        """Set up default scaling rules"""
        
        # CPU-based scaling rule
        cpu_rule = ScalingRule(
            rule_id="cpu_scaling",
            name="CPU-based Auto Scaling",
            resource_type=ResourceType.CPU,
            scaling_strategy=ScalingStrategy.HORIZONTAL,
            trigger_threshold=75.0,  # Scale up at 75% CPU
            scale_down_threshold=30.0,  # Scale down at 30% CPU
            cooldown_period=300,  # 5 minutes
            max_instances=20,
            min_instances=2
        )
        
        # Memory-based scaling rule
        memory_rule = ScalingRule(
            rule_id="memory_scaling",
            name="Memory-based Auto Scaling",
            resource_type=ResourceType.MEMORY,
            scaling_strategy=ScalingStrategy.HORIZONTAL,
            trigger_threshold=80.0,  # Scale up at 80% memory
            scale_down_threshold=40.0,  # Scale down at 40% memory
            cooldown_period=300,
            max_instances=15,
            min_instances=2
        )
        
        # Agent-based scaling rule
        agent_rule = ScalingRule(
            rule_id="agent_scaling",
            name="Agent Instance Scaling",
            resource_type=ResourceType.AGENT_INSTANCES,
            scaling_strategy=ScalingStrategy.ELASTIC,
            trigger_threshold=90.0,  # Scale up at 90% agent utilization
            scale_down_threshold=50.0,  # Scale down at 50% utilization
            cooldown_period=180,  # 3 minutes
            max_instances=100,
            min_instances=10
        )
        
        self.scaling_rules = {
            "cpu_scaling": cpu_rule,
            "memory_scaling": memory_rule,
            "agent_scaling": agent_rule
        }
    
    async def _start_scalability_monitoring(self):
        """Start scalability monitoring"""
        self.scaling_active = True
        
        # Start metrics collection
        await self.metrics_collector.start_collection()
        
        # Start performance monitoring
        await self.performance_monitor.start_monitoring()
        
        # Start scaling decision loop
        asyncio.create_task(self._scaling_decision_loop())
        
        logger.info("Scalability monitoring started")
    
    async def _scaling_decision_loop(self):
        """Main scaling decision loop"""
        while self.scaling_active:
            try:
                # Collect current metrics
                current_metrics = await self.metrics_collector.get_current_metrics()
                
                # Evaluate scaling rules
                scaling_decisions = await self._evaluate_scaling_rules(current_metrics)
                
                # Execute scaling decisions
                for decision in scaling_decisions:
                    await self._execute_scaling_decision(decision)
                
                # Predictive scaling analysis
                await self.predictive_scaler.analyze_and_predict(current_metrics)
                
                # Wait for next evaluation cycle
                await asyncio.sleep(30)  # Evaluate every 30 seconds
                
            except Exception as e:
                logger.error(f"Scaling decision loop error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _evaluate_scaling_rules(self, metrics: ScalabilityMetrics) -> List[Dict[str, Any]]:
        """Evaluate scaling rules against current metrics"""
        scaling_decisions = []
        
        for rule in self.scaling_rules.values():
            if not rule.enabled:
                continue
            
            decision = await self._evaluate_single_rule(rule, metrics)
            if decision:
                scaling_decisions.append(decision)
        
        return scaling_decisions
    
    async def _evaluate_single_rule(self, rule: ScalingRule, metrics: ScalabilityMetrics) -> Optional[Dict[str, Any]]:
        """Evaluate single scaling rule"""
        
        # Get current resource utilization
        current_utilization = self._get_resource_utilization(rule.resource_type, metrics)
        
        # Check if scaling is needed
        if current_utilization > rule.trigger_threshold:
            # Scale up needed
            return {
                "rule_id": rule.rule_id,
                "action": "scale_up",
                "resource_type": rule.resource_type.value,
                "current_utilization": current_utilization,
                "threshold": rule.trigger_threshold,
                "strategy": rule.scaling_strategy.value
            }
        
        elif current_utilization < rule.scale_down_threshold:
            # Scale down possible
            return {
                "rule_id": rule.rule_id,
                "action": "scale_down",
                "resource_type": rule.resource_type.value,
                "current_utilization": current_utilization,
                "threshold": rule.scale_down_threshold,
                "strategy": rule.scaling_strategy.value
            }
        
        return None
    
    def _get_resource_utilization(self, resource_type: ResourceType, metrics: ScalabilityMetrics) -> float:
        """Get current utilization for specific resource type"""
        
        if resource_type == ResourceType.CPU:
            return metrics.cpu_utilization
        elif resource_type == ResourceType.MEMORY:
            return metrics.memory_utilization
        elif resource_type == ResourceType.AGENT_INSTANCES:
            # Calculate agent utilization based on active agents vs capacity
            return (metrics.active_agents / 100.0) * 100  # Assuming capacity of 100
        else:
            return 0.0
    
    async def _execute_scaling_decision(self, decision: Dict[str, Any]):
        """Execute scaling decision"""
        
        rule_id = decision["rule_id"]
        action = decision["action"]
        resource_type = decision["resource_type"]
        strategy = decision["strategy"]
        
        logger.info(f"Executing scaling decision: {action} for {resource_type} using {strategy}")
        
        if resource_type == "agent_instances":
            if action == "scale_up":
                await self.agent_scaler.scale_up_agents(strategy)
            else:
                await self.agent_scaler.scale_down_agents(strategy)
        
        elif resource_type in ["cpu", "memory"]:
            if action == "scale_up":
                await self.auto_scaler.scale_up_infrastructure(resource_type, strategy)
            else:
                await self.auto_scaler.scale_down_infrastructure(resource_type, strategy)
    
    async def handle_traffic_spike(self, spike_magnitude: float) -> Dict[str, Any]:
        """Handle sudden traffic spike"""
        
        # Immediate response actions
        immediate_actions = []
        
        # Scale up load balancer capacity
        lb_scaling = await self.load_balancer.handle_traffic_spike(spike_magnitude)
        immediate_actions.append(lb_scaling)
        
        # Emergency agent scaling
        agent_scaling = await self.agent_scaler.emergency_scale_up(spike_magnitude)
        immediate_actions.append(agent_scaling)
        
        # Activate circuit breakers if needed
        if spike_magnitude > 5.0:  # 5x normal traffic
            circuit_breaker = await self.service_mesh.activate_circuit_breakers()
            immediate_actions.append(circuit_breaker)
        
        # Predictive scaling for sustained load
        predictive_scaling = await self.predictive_scaler.handle_traffic_spike(spike_magnitude)
        immediate_actions.append(predictive_scaling)
        
        return {
            "traffic_spike_handled": True,
            "spike_magnitude": spike_magnitude,
            "immediate_actions": immediate_actions,
            "estimated_capacity_increase": spike_magnitude * 1.2,  # 20% buffer
            "response_time": "< 30 seconds"
        }
    
    async def optimize_for_concurrent_users(self, target_users: int) -> Dict[str, Any]:
        """Optimize system for specific number of concurrent users"""
        
        # Calculate required resources
        resource_requirements = await self.capacity_planner.calculate_requirements(target_users)
        
        # Optimize load balancing
        lb_optimization = await self.load_balancer.optimize_for_users(target_users)
        
        # Scale agent pool
        agent_optimization = await self.agent_pool_manager.optimize_for_users(target_users)
        
        # Optimize resource allocation
        resource_optimization = await self.resource_manager.optimize_allocation(resource_requirements)
        
        # Update scaling rules
        rule_updates = await self._update_scaling_rules_for_users(target_users)
        
        return {
            "optimization_complete": True,
            "target_concurrent_users": target_users,
            "resource_requirements": resource_requirements,
            "load_balancer_optimization": lb_optimization,
            "agent_optimization": agent_optimization,
            "resource_optimization": resource_optimization,
            "scaling_rule_updates": rule_updates
        }
    
    async def _update_scaling_rules_for_users(self, target_users: int) -> Dict[str, Any]:
        """Update scaling rules based on target user count"""
        
        # Calculate scaling factors
        base_users = 1000  # Base capacity
        scaling_factor = target_users / base_users
        
        updates = {}
        
        for rule_id, rule in self.scaling_rules.items():
            # Adjust thresholds based on expected load
            if scaling_factor > 1.0:
                # Lower thresholds for higher user counts
                rule.trigger_threshold *= 0.9
                rule.scale_down_threshold *= 0.8
            
            # Adjust instance limits
            rule.max_instances = int(rule.max_instances * scaling_factor)
            rule.min_instances = max(1, int(rule.min_instances * scaling_factor * 0.5))
            
            updates[rule_id] = {
                "trigger_threshold": rule.trigger_threshold,
                "scale_down_threshold": rule.scale_down_threshold,
                "max_instances": rule.max_instances,
                "min_instances": rule.min_instances
            }
        
        return updates
    
    def get_scalability_status(self) -> Dict[str, Any]:
        """Get comprehensive scalability status"""
        
        current_metrics = self.metrics_collector.get_latest_metrics()
        
        return {
            "scaling_active": self.scaling_active,
            "current_metrics": current_metrics.to_dict() if current_metrics else None,
            "active_scaling_rules": len([r for r in self.scaling_rules.values() if r.enabled]),
            "load_balancer_status": self.load_balancer.get_status(),
            "agent_pool_status": self.agent_pool_manager.get_status(),
            "cluster_status": self.cluster_coordinator.get_status(),
            "predictive_scaling_status": self.predictive_scaler.get_status()
        }

class IntelligentLoadBalancer:
    """Intelligent load balancer with adaptive algorithms"""
    
    def __init__(self):
        self.algorithm = LoadBalancingAlgorithm.ADAPTIVE
        self.backend_servers: List[Dict[str, Any]] = []
        self.health_checks_enabled = True
        self.sticky_sessions = False
        
    async def initialize(self) -> Dict[str, Any]:
        """Initialize load balancer"""
        
        # Set up backend servers
        self.backend_servers = [
            {"id": f"server_{i}", "weight": 1, "connections": 0, "response_time": 0.0, "healthy": True}
            for i in range(3)  # Start with 3 backend servers
        ]
        
        return {
            "load_balancer_initialized": True,
            "algorithm": self.algorithm.value,
            "backend_servers": len(self.backend_servers),
            "health_checks": self.health_checks_enabled
        }
    
    async def handle_traffic_spike(self, spike_magnitude: float) -> Dict[str, Any]:
        """Handle traffic spike by adjusting load balancing"""
        
        # Add more backend servers if needed
        additional_servers = int(spike_magnitude)
        
        for i in range(additional_servers):
            server_id = f"spike_server_{i}"
            self.backend_servers.append({
                "id": server_id,
                "weight": 2,  # Higher weight for spike servers
                "connections": 0,
                "response_time": 0.0,
                "healthy": True
            })
        
        # Switch to more aggressive algorithm during spike
        if spike_magnitude > 3.0:
            self.algorithm = LoadBalancingAlgorithm.LEAST_RESPONSE_TIME
        
        return {
            "traffic_spike_handled": True,
            "additional_servers": additional_servers,
            "algorithm_switched": self.algorithm.value,
            "total_servers": len(self.backend_servers)
        }
    
    async def optimize_for_users(self, target_users: int) -> Dict[str, Any]:
        """Optimize load balancer for target user count"""
        
        # Calculate optimal server count
        users_per_server = 500  # Assume 500 users per server
        optimal_servers = max(2, (target_users // users_per_server) + 1)
        
        # Adjust server pool
        current_servers = len(self.backend_servers)
        
        if optimal_servers > current_servers:
            # Add servers
            for i in range(optimal_servers - current_servers):
                server_id = f"optimized_server_{i}"
                self.backend_servers.append({
                    "id": server_id,
                    "weight": 1,
                    "connections": 0,
                    "response_time": 0.0,
                    "healthy": True
                })
        
        return {
            "optimization_complete": True,
            "target_users": target_users,
            "optimal_servers": optimal_servers,
            "servers_added": max(0, optimal_servers - current_servers)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get load balancer status"""
        return {
            "algorithm": self.algorithm.value,
            "backend_servers": len(self.backend_servers),
            "healthy_servers": len([s for s in self.backend_servers if s["healthy"]]),
            "total_connections": sum(s["connections"] for s in self.backend_servers),
            "average_response_time": sum(s["response_time"] for s in self.backend_servers) / len(self.backend_servers) if self.backend_servers else 0
        }

class AutoScalingManager:
    """Automatic scaling manager for infrastructure"""
    
    def __init__(self):
        self.scaling_policies: Dict[str, Dict[str, Any]] = {}
        self.scaling_history: List[Dict[str, Any]] = []
        
    async def initialize(self) -> Dict[str, Any]:
        """Initialize auto-scaling manager""tool_5477": {
                "metric": "cpu_utilization",
                "scale_up_threshold": 75.0,
                "scale_down_threshold": 30.0,
                "scaling_adjustment": 2,  # Add/remove 2 instances
                "cooldown300_memory_policy": {
                "metric": "memory_utilization",
                "scale_up_threshold": 80.0,
                "scale_down_threshold": 40.0,
                "scaling_adjustment": 1,
                "cooldown": 300
            }
        }
        
        return {
            "auto_scaling_initialized": True,
            "scaling_policies": len(self.scaling_policies),
            "scaling_enabled": True
        }
    
    async def scale_up_infrastructure(self, resource_type: str, strategy: str) -> Dict[str, Any]:
        """Scale up infrastructure resources"""
        
        policy = self.scaling_policies.get(f"{resource_type}_policy", {})
        adjustment = policy.get("scaling_adjustment", 1)
        
        # Record scaling action
        scaling_action = {
            "timestamp": datetime.now(),
            "action": "scale_up",
            "resource_type": resource_type,
            "strategy": strategy,
            "adjustment": adjustment
        }
        
        self.scaling_history.append(scaling_action)
        
        return {
            "scaling_action": "scale_up",
            "resource_type": resource_type,
            "instances_added": adjustment,
            "strategy": strategy
        }
    
    async def scale_down_infrastructure(self, resource_type: str, strategy: str) -> Dict[str, Any]:
        """Scale down infrastructure resources"""
        
        policy = self.scaling_policies.get(f"{resource_type}_policy", {})
        adjustment = policy.get("scaling_adjustment", 1)
        
        # Record scaling action
        scaling_action = {
            "timestamp": datetime.now(),
            "action": "scale_down",
            "resource_type": resource_type,
            "strategy": strategy,
            "adjustment": adjustment
        }
        
        self.scaling_history.append(scaling_action)
        
        return {
            "scaling_action": "scale_down",
            "resource_type": resource_type,
            "instances_removed": adjustment,
            "strategy": strategy
        }

class AgentScalingManager:
    """Manages scaling of JAEGIS agents"""
    
    def __init__(self):
        self.agent_pools: Dict[str, List[str]] = defaultdict(list)
        self.scaling_metrics: Dict[str, Any] = {}
        
    async def initialize(self) -> Dict[str, Any]:
        """Initialize agent scaling manager"""
        
        # Initialize agent pools for different agent types
        agent_types = ["orchestrator", "analyst", "creative", "implementer", "validator"]
        
        for agent_type in agent_types:
            # Start with minimum pool size
            for i in range(2):
                agent_id = f"{agent_type}_agent_{i}"
                self.agent_pools[agent_type].append(agent_id)
        
        return {
            "agent_scaling_initialized": True,
            "agent_types": len(agent_types),
            "tool_1797": {k: len(v) for k, v in self.agent_pools.items()}
        }
    
    async def scale_up_agents(self, strategy: str) -> Dict[str, Any]:
        """Scale up agent instances"""
        
        agents_added = 0
        
        # Determine which agent types need scaling
        for agent_type, pool in self.agent_pools.items():
            if len(pool) < 10:  # Max 10 agents per type
                new_agent_id = f"{agent_type}_agent_{len(pool)}"
                pool.append(new_agent_id)
                agents_added += 1
        
        return {
            "scaling_action": "scale_up",
            "agents_added": agents_added,
            "strategy": strategy,
            "total_agents": sum(len(pool) for pool in self.agent_pools.values())
        }
    
    async def scale_down_agents(self, strategy: str) -> Dict[str, Any]:
        """Scale down agent instances"""
        
        agents_removed = 0
        
        # Remove agents from pools (keep minimum of 1 per type)
        for agent_type, pool in self.agent_pools.items():
            if len(pool) > 1:
                pool.pop()
                agents_removed += 1
        
        return {
            "scaling_action": "scale_down",
            "agents_removed": agents_removed,
            "strategy": strategy,
            "total_agents": sum(len(pool) for pool in self.agent_pools.values())
        }
    
    async def emergency_scale_up(self, spike_magnitude: float) -> Dict[str, Any]:
        """Emergency scaling for traffic spikes"""
        
        # Calculate emergency scaling factor
        emergency_agents = int(spike_magnitude * 2)  # 2 agents per magnitude unit
        
        agents_added = 0
        
        # Add emergency agents to all pools
        for agent_type, pool in self.agent_pools.items():
            for i in range(min(emergency_agents, 5)):  # Max 5 emergency agents per type
                emergency_agent_id = f"{agent_type}_emergency_{i}"
                pool.append(emergency_agent_id)
                agents_added += 1
        
        return {
            "emergency_scaling": True,
            "spike_magnitude": spike_magnitude,
            "emergency_agents_added": agents_added,
            "total_agents": sum(len(pool) for pool in self.agent_pools.values())
        }

# Additional placeholder classes for scalability components
class DistributedResourceManager:
    async def initialize(self) -> Dict[str, Any]:
        return {"resource_manager_initialized": True}
    
    async def optimize_allocation(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        return {"resource_allocation_optimized": True}

class CapacityPlanner:
    async def calculate_requirements(self, target_users: int) -> Dict[str, Any]:
        return {
            "cpu_cores": target_users // 100,
            "memory_gb": target_users // 50,
            "storage_gb": target_users * 0.1,
            "network_mbps": target_users * 0.5
        }

class ScalabilityMetricsCollector:
    def __init__(self):
        self.latest_metrics: Optional[ScalabilityMetrics] = None
    
    async def start_collection(self):
        pass
    
    async def get_current_metrics(self) -> ScalabilityMetrics:
        # Mock metrics for demonstration
        return ScalabilityMetrics(
            timestamp=datetime.now(),
            concurrent_users=1000,
            active_agents=50,
            request_rate=100.0,
            response_time_p95=0.5,
            cpu_utilization=60.0,
            memory_utilization=70.0,
            network_throughput=50.0,
            error_rate=0.1,
            queue_depth=10
        )
    
    def get_latest_metrics(self) -> Optional[ScalabilityMetrics]:
        return self.latest_metrics

class PerformanceMonitor:
    async def start_monitoring(self):
        pass

class AgentPoolManager:
    async def optimize_for_users(self, target_users: int) -> Dict[str, Any]:
        return {"agent_pool_optimized": True}
    
    def get_status(self) -> Dict[str, Any]:
        return {"pool_status": "healthy"}

class ClusterCoordinator:
    async def initialize(self) -> Dict[str, Any]:
        return {"cluster_coordinator_initialized": True}
    
    def get_status(self) -> Dict[str, Any]:
        return {"cluster_status": "healthy"}

class ServiceMeshManager:
    async def initialize(self) -> Dict[str, Any]:
        return {"service_mesh_initialized": True}
    
    async def activate_circuit_breakers(self) -> Dict[str, Any]:
        return {"circuit_breakers_activated": True}

class PredictiveScaler:
    async def initialize(self) -> Dict[str, Any]:
        return {"predictive_scaler_initialized": True}
    
    async def analyze_and_predict(self, metrics: ScalabilityMetrics):
        pass
    
    async def handle_traffic_spike(self, spike_magnitude: float) -> Dict[str, Any]:
        return {"predictive_scaling_activated": True}
    
    def get_status(self) -> Dict[str, Any]:
        return {"predictive_scaling_status": "active"}
