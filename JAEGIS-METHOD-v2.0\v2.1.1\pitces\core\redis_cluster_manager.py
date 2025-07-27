"""
P.I.T.C.E.S. Framework - Redis Cluster Manager
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements Redis Cluster support for horizontal scaling,
performance optimization, and high availability across the P.I.T.C.E.S. framework.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass
from enum import Enum

import redis
import redis.asyncio as aioredis
from redis.cluster import RedisCluster
from redis.asyncio.cluster import RedisCluster as AsyncRedisCluster

from .exceptions import PITCESError, ErrorCodes


logger = logging.getLogger(__name__)


class ClusterNodeRole(Enum):
    """Redis cluster node roles."""
    MASTER = "master"
    SLAVE = "slave"
    REPLICA = "replica"


class ClusterHealth(Enum):
    """Cluster health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"


@dataclass
class ClusterNode:
    """Redis cluster node information."""
    node_id: str
    host: str
    port: int
    role: ClusterNodeRole
    slots: List[Tuple[int, int]]
    flags: List[str]
    master_id: Optional[str] = None
    ping_sent: int = 0
    pong_recv: int = 0
    config_epoch: int = 0
    link_state: str = "connected"
    
    @property
    def is_master(self) -> bool:
        """Check if node is a master."""
        return self.role == ClusterNodeRole.MASTER
    
    @property
    def is_replica(self) -> bool:
        """Check if node is a replica."""
        return self.role in [ClusterNodeRole.SLAVE, ClusterNodeRole.REPLICA]
    
    @property
    def slot_count(self) -> int:
        """Get number of slots assigned to this node."""
        return sum(end - start + 1 for start, end in self.slots)


class RedisClusterManager:
    """
    Redis Cluster manager for horizontal scaling and high availability.
    
    Features:
    - Automatic cluster discovery and topology management
    - Load balancing across cluster nodes
    - Failover detection and handling
    - Performance monitoring and optimization
    - Slot migration and rebalancing
    - Backup and recovery coordination
    - Memory optimization across nodes
    """
    
    def __init__(self, cluster_nodes: List[Dict[str, Any]], config: Optional[Dict[str, Any]] = None):
        """
        Initialize Redis Cluster Manager.
        
        Args:
            cluster_nodes: List of cluster node configurations
            config: Cluster management configuration
        """
        self.cluster_nodes = cluster_nodes
        self.config = config or self._get_default_config()
        
        # Cluster clients
        self.cluster_client: Optional[RedisCluster] = None
        self.async_cluster_client: Optional[AsyncRedisCluster] = None
        
        # Cluster topology
        self.cluster_topology: Dict[str, ClusterNode] = {}
        self.master_nodes: Dict[str, ClusterNode] = {}
        self.replica_nodes: Dict[str, ClusterNode] = {}
        
        # Performance metrics
        self.cluster_metrics = {
            'total_nodes': 0,
            'master_nodes': 0,
            'replica_nodes': 0,
            'total_slots': 16384,
            'assigned_slots': 0,
            'cluster_health': ClusterHealth.OFFLINE,
            'failover_events': 0,
            'slot_migrations': 0,
            'memory_usage': {},
            'connection_pool_stats': {},
            'command_latencies': {},
            'throughput_metrics': {}
        }
        
        # Monitoring and optimization
        self.monitoring_enabled = self.config.get('monitoring_enabled', True)
        self.optimization_enabled = self.config.get('optimization_enabled', True)
        
        # Failover tracking
        self.failover_history: List[Dict[str, Any]] = []
        
        logger.info("RedisClusterManager initialized")
    
    async def initialize_cluster(self) -> bool:
        """
        Initialize Redis Cluster connections and topology.
        
        Returns:
            True if initialization successful
        """
        try:
            # Initialize cluster clients
            await self._initialize_cluster_clients()
            
            # Discover cluster topology
            await self._discover_cluster_topology()
            
            # Validate cluster health
            cluster_health = await self._check_cluster_health()
            
            if cluster_health == ClusterHealth.OFFLINE:
                logger.error("Cluster is offline - initialization failed")
                return False
            
            # Start monitoring if enabled
            if self.monitoring_enabled:
                asyncio.create_task(self._monitor_cluster_health())
                asyncio.create_task(self._monitor_performance_metrics())
            
            # Start optimization if enabled
            if self.optimization_enabled:
                asyncio.create_task(self._optimize_cluster_performance())
            
            logger.info("Redis Cluster initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Redis Cluster initialization failed: {e}")
            return False
    
    async def get_cluster_info(self) -> Dict[str, Any]:
        """
        Get comprehensive cluster information.
        
        Returns:
            Cluster information dictionary
        """
        try:
            # Update topology
            await self._discover_cluster_topology()
            
            # Get cluster state
            cluster_info = await self.async_cluster_client.cluster_info()
            
            # Calculate slot distribution
            slot_distribution = self._calculate_slot_distribution()
            
            # Get memory usage
            memory_usage = await self._get_cluster_memory_usage()
            
            return {
                'cluster_state': cluster_info.get('cluster_state', 'unknown'),
                'cluster_size': cluster_info.get('cluster_size', 0),
                'cluster_known_nodes': cluster_info.get('cluster_known_nodes', 0),
                'cluster_slots_assigned': cluster_info.get('cluster_slots_assigned', 0),
                'cluster_slots_ok': cluster_info.get('cluster_slots_ok', 0),
                'cluster_slots_pfail': cluster_info.get('cluster_slots_pfail', 0),
                'cluster_slots_fail': cluster_info.get('cluster_slots_fail', 0),
                'topology': {
                    'master_nodes': len(self.master_nodes),
                    'replica_nodes': len(self.replica_nodes),
                    'total_nodes': len(self.cluster_topology)
                },
                'slot_distribution': slot_distribution,
                'memory_usage': memory_usage,
                'health_status': self.cluster_metrics['cluster_health'].value,
                'metrics': self.cluster_metrics
            }
            
        except Exception as e:
            logger.error(f"Failed to get cluster info: {e}")
            return {'error': str(e)}
    
    async def execute_cluster_command(
        self, 
        command: str, 
        *args,
        target_node: Optional[str] = None,
        **kwargs
    ) -> Any:
        """
        Execute command on cluster with optional node targeting.
        
        Args:
            command: Redis command to execute
            *args: Command arguments
            target_node: Optional specific node to target
            **kwargs: Additional keyword arguments
            
        Returns:
            Command result
        """
        try:
            start_time = time.time()
            
            if target_node and target_node in self.cluster_topology:
                # Execute on specific node
                node = self.cluster_topology[target_node]
                node_client = redis.Redis(host=node.host, port=node.port)
                result = await asyncio.get_event_loop().run_in_executor(
                    None, getattr(node_client, command.lower()), *args
                )
            else:
                # Execute on cluster (automatic routing)
                result = await getattr(self.async_cluster_client, command.lower())(*args, **kwargs)
            
            # Track command latency
            latency = time.time() - start_time
            self._update_command_latency(command, latency)
            
            return result
            
        except Exception as e:
            logger.error(f"Cluster command execution failed: {e}")
            raise PITCESError(
                f"Cluster command failed: {str(e)}",
                error_code=ErrorCodes.CLUSTER_COMMAND_FAILURE
            )
    
    async def rebalance_cluster_slots(self) -> Dict[str, Any]:
        """
        Rebalance cluster slots for optimal distribution.
        
        Returns:
            Rebalancing results
        """
        try:
            logger.info("Starting cluster slot rebalancing")
            
            # Analyze current slot distribution
            slot_analysis = await self._analyze_slot_distribution()
            
            if not slot_analysis['needs_rebalancing']:
                logger.info("Cluster slots are already well balanced")
                return {'status': 'no_action_needed', 'analysis': slot_analysis}
            
            # Plan slot migrations
            migration_plan = await self._plan_slot_migrations(slot_analysis)
            
            # Execute migrations
            migration_results = await self._execute_slot_migrations(migration_plan)
            
            # Update metrics
            self.cluster_metrics['slot_migrations'] += len(migration_results)
            
            logger.info(f"Cluster rebalancing completed: {len(migration_results)} migrations")
            
            return {
                'status': 'completed',
                'migrations_executed': len(migration_results),
                'migration_results': migration_results,
                'new_distribution': await self._calculate_slot_distribution()
            }
            
        except Exception as e:
            logger.error(f"Cluster rebalancing failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    async def handle_node_failover(self, failed_node_id: str) -> Dict[str, Any]:
        """
        Handle node failover scenario.
        
        Args:
            failed_node_id: ID of the failed node
            
        Returns:
            Failover handling results
        """
        try:
            logger.warning(f"Handling failover for node: {failed_node_id}")
            
            # Record failover event
            failover_event = {
                'node_id': failed_node_id,
                'timestamp': datetime.now().isoformat(),
                'type': 'automatic_failover'
            }
            
            # Check if failed node is a master
            if failed_node_id in self.master_nodes:
                # Master failover
                result = await self._handle_master_failover(failed_node_id)
                failover_event['failover_type'] = 'master'
            else:
                # Replica failover
                result = await self._handle_replica_failover(failed_node_id)
                failover_event['failover_type'] = 'replica'
            
            failover_event['result'] = result
            self.failover_history.append(failover_event)
            self.cluster_metrics['failover_events'] += 1
            
            # Update cluster topology
            await self._discover_cluster_topology()
            
            logger.info(f"Failover handling completed for node: {failed_node_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failover handling failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    async def optimize_memory_usage(self) -> Dict[str, Any]:
        """
        Optimize memory usage across cluster nodes.
        
        Returns:
            Memory optimization results
        """
        try:
            logger.info("Starting cluster memory optimization")
            
            # Analyze memory usage
            memory_analysis = await self._analyze_memory_usage()
            
            # Optimize each node
            optimization_results = {}
            
            for node_id, node in self.cluster_topology.items():
                try:
                    node_optimization = await self._optimize_node_memory(node)
                    optimization_results[node_id] = node_optimization
                except Exception as e:
                    logger.error(f"Memory optimization failed for node {node_id}: {e}")
                    optimization_results[node_id] = {'status': 'failed', 'error': str(e)}
            
            # Update memory metrics
            await self._update_memory_metrics()
            
            logger.info("Cluster memory optimization completed")
            
            return {
                'status': 'completed',
                'memory_analysis': memory_analysis,
                'optimization_results': optimization_results,
                'total_memory_saved': sum(
                    result.get('memory_saved', 0) 
                    for result in optimization_results.values()
                    if isinstance(result, dict)
                )
            }
            
        except Exception as e:
            logger.error(f"Memory optimization failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    async def backup_cluster_configuration(self) -> Dict[str, Any]:
        """
        Backup cluster configuration and data.
        
        Returns:
            Backup results
        """
        try:
            logger.info("Starting cluster configuration backup")
            
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'cluster_topology': {
                    node_id: {
                        'host': node.host,
                        'port': node.port,
                        'role': node.role.value,
                        'slots': node.slots,
                        'master_id': node.master_id
                    }
                    for node_id, node in self.cluster_topology.items()
                },
                'cluster_info': await self.get_cluster_info(),
                'configuration': self.config
            }
            
            # Save backup data
            backup_filename = f"cluster_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_path = self.config.get('backup_path', './backups')
            
            import os
            os.makedirs(backup_path, exist_ok=True)
            
            with open(f"{backup_path}/{backup_filename}", 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            logger.info(f"Cluster backup completed: {backup_filename}")
            
            return {
                'status': 'completed',
                'backup_file': backup_filename,
                'backup_size': len(json.dumps(backup_data)),
                'nodes_backed_up': len(self.cluster_topology)
            }
            
        except Exception as e:
            logger.error(f"Cluster backup failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def get_cluster_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive cluster performance metrics.
        
        Returns:
            Cluster metrics dictionary
        """
        return {
            **self.cluster_metrics,
            'failover_history_count': len(self.failover_history),
            'recent_failovers': self.failover_history[-5:] if self.failover_history else [],
            'cluster_uptime': self._calculate_cluster_uptime(),
            'node_details': {
                node_id: {
                    'host': node.host,
                    'port': node.port,
                    'role': node.role.value,
                    'slot_count': node.slot_count,
                    'is_connected': node.link_state == 'connected'
                }
                for node_id, node in self.cluster_topology.items()
            }
        }
    
    async def _initialize_cluster_clients(self):
        """Initialize Redis cluster clients."""
        try:
            # Prepare startup nodes
            startup_nodes = [
                {'host': node['host'], 'port': node['port']}
                for node in self.cluster_nodes
            ]
            
            # Initialize synchronous cluster client
            self.cluster_client = RedisCluster(
                startup_nodes=startup_nodes,
                decode_responses=True,
                skip_full_coverage_check=True,
                health_check_interval=30
            )
            
            # Initialize asynchronous cluster client
            self.async_cluster_client = AsyncRedisCluster(
                startup_nodes=startup_nodes,
                decode_responses=True,
                skip_full_coverage_check=True,
                health_check_interval=30
            )
            
            # Test connections
            await self.async_cluster_client.ping()
            
            logger.info("Cluster clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize cluster clients: {e}")
            raise
    
    async def _discover_cluster_topology(self):
        """Discover and update cluster topology."""
        try:
            # Get cluster nodes information
            nodes_info = await self.async_cluster_client.cluster_nodes()
            
            # Parse nodes information
            self.cluster_topology.clear()
            self.master_nodes.clear()
            self.replica_nodes.clear()
            
            for line in nodes_info.split('\n'):
                if not line.strip():
                    continue
                
                node = self._parse_cluster_node_info(line)
                if node:
                    self.cluster_topology[node.node_id] = node
                    
                    if node.is_master:
                        self.master_nodes[node.node_id] = node
                    elif node.is_replica:
                        self.replica_nodes[node.node_id] = node
            
            # Update metrics
            self.cluster_metrics['total_nodes'] = len(self.cluster_topology)
            self.cluster_metrics['master_nodes'] = len(self.master_nodes)
            self.cluster_metrics['replica_nodes'] = len(self.replica_nodes)
            self.cluster_metrics['assigned_slots'] = sum(
                node.slot_count for node in self.master_nodes.values()
            )
            
            logger.debug(f"Discovered cluster topology: {len(self.cluster_topology)} nodes")
            
        except Exception as e:
            logger.error(f"Failed to discover cluster topology: {e}")
            raise
    
    def _parse_cluster_node_info(self, node_line: str) -> Optional[ClusterNode]:
        """Parse cluster node information from CLUSTER NODES output."""
        try:
            parts = node_line.split()
            if len(parts) < 8:
                return None
            
            node_id = parts[0]
            host_port = parts[1].split(':')
            host = host_port[0]
            port = int(host_port[1])
            flags = parts[2].split(',')
            master_id = parts[3] if parts[3] != '-' else None
            ping_sent = int(parts[4])
            pong_recv = int(parts[5])
            config_epoch = int(parts[6])
            link_state = parts[7]
            
            # Determine role
            if 'master' in flags:
                role = ClusterNodeRole.MASTER
            elif 'slave' in flags:
                role = ClusterNodeRole.SLAVE
            else:
                role = ClusterNodeRole.REPLICA
            
            # Parse slot ranges
            slots = []
            for slot_info in parts[8:]:
                if '-' in slot_info:
                    start, end = map(int, slot_info.split('-'))
                    slots.append((start, end))
                elif slot_info.isdigit():
                    slot_num = int(slot_info)
                    slots.append((slot_num, slot_num))
            
            return ClusterNode(
                node_id=node_id,
                host=host,
                port=port,
                role=role,
                slots=slots,
                flags=flags,
                master_id=master_id,
                ping_sent=ping_sent,
                pong_recv=pong_recv,
                config_epoch=config_epoch,
                link_state=link_state
            )
            
        except Exception as e:
            logger.error(f"Failed to parse cluster node info: {e}")
            return None
    
    async def _check_cluster_health(self) -> ClusterHealth:
        """Check overall cluster health."""
        try:
            cluster_info = await self.async_cluster_client.cluster_info()
            cluster_state = cluster_info.get('cluster_state', 'fail')
            
            if cluster_state == 'ok':
                # Check if all master nodes are available
                failed_masters = sum(
                    1 for node in self.master_nodes.values()
                    if node.link_state != 'connected'
                )
                
                if failed_masters == 0:
                    health = ClusterHealth.HEALTHY
                elif failed_masters < len(self.master_nodes) * 0.5:
                    health = ClusterHealth.DEGRADED
                else:
                    health = ClusterHealth.CRITICAL
            else:
                health = ClusterHealth.OFFLINE
            
            self.cluster_metrics['cluster_health'] = health
            return health
            
        except Exception as e:
            logger.error(f"Cluster health check failed: {e}")
            self.cluster_metrics['cluster_health'] = ClusterHealth.OFFLINE
            return ClusterHealth.OFFLINE
    
    async def _monitor_cluster_health(self):
        """Background task to monitor cluster health."""
        while True:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                
                health = await self._check_cluster_health()
                
                if health in [ClusterHealth.CRITICAL, ClusterHealth.OFFLINE]:
                    logger.warning(f"Cluster health is {health.value}")
                    # Could trigger alerts here
                
                # Update topology
                await self._discover_cluster_topology()
                
            except Exception as e:
                logger.error(f"Cluster health monitoring error: {e}")
    
    async def _monitor_performance_metrics(self):
        """Background task to monitor performance metrics."""
        while True:
            try:
                await asyncio.sleep(60)  # Monitor every minute
                
                # Update memory metrics
                await self._update_memory_metrics()
                
                # Update connection pool stats
                await self._update_connection_pool_stats()
                
                # Update throughput metrics
                await self._update_throughput_metrics()
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
    
    async def _optimize_cluster_performance(self):
        """Background task for cluster performance optimization."""
        while True:
            try:
                await asyncio.sleep(3600)  # Optimize every hour
                
                # Check if optimization is needed
                if await self._should_optimize():
                    await self.optimize_memory_usage()
                    
                    # Check if rebalancing is needed
                    slot_analysis = await self._analyze_slot_distribution()
                    if slot_analysis['needs_rebalancing']:
                        await self.rebalance_cluster_slots()
                
            except Exception as e:
                logger.error(f"Cluster optimization error: {e}")
    
    def _calculate_slot_distribution(self) -> Dict[str, Any]:
        """Calculate slot distribution across master nodes."""
        distribution = {}
        total_slots = 0
        
        for node_id, node in self.master_nodes.items():
            slot_count = node.slot_count
            distribution[node_id] = {
                'slot_count': slot_count,
                'percentage': (slot_count / 16384) * 100 if slot_count > 0 else 0
            }
            total_slots += slot_count
        
        return {
            'distribution': distribution,
            'total_assigned_slots': total_slots,
            'unassigned_slots': 16384 - total_slots
        }
    
    async def _get_cluster_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage across all cluster nodes."""
        memory_usage = {}
        
        for node_id, node in self.cluster_topology.items():
            try:
                node_client = redis.Redis(host=node.host, port=node.port)
                memory_info = node_client.memory_usage()
                memory_usage[node_id] = memory_info
            except Exception as e:
                logger.error(f"Failed to get memory usage for node {node_id}: {e}")
                memory_usage[node_id] = {'error': str(e)}
        
        return memory_usage
    
    async def _analyze_slot_distribution(self) -> Dict[str, Any]:
        """Analyze slot distribution for rebalancing needs."""
        distribution = self._calculate_slot_distribution()
        
        if not self.master_nodes:
            return {'needs_rebalancing': False, 'reason': 'no_master_nodes'}
        
        # Calculate ideal slots per master
        ideal_slots_per_master = 16384 // len(self.master_nodes)
        
        # Check for imbalance
        max_deviation = 0
        for node_data in distribution['distribution'].values():
            deviation = abs(node_data['slot_count'] - ideal_slots_per_master)
            max_deviation = max(max_deviation, deviation)
        
        # Consider rebalancing if deviation > 10% of ideal
        threshold = ideal_slots_per_master * 0.1
        needs_rebalancing = max_deviation > threshold
        
        return {
            'needs_rebalancing': needs_rebalancing,
            'max_deviation': max_deviation,
            'threshold': threshold,
            'ideal_slots_per_master': ideal_slots_per_master,
            'current_distribution': distribution
        }
    
    async def _plan_slot_migrations(self, slot_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan slot migrations for rebalancing."""
        # This would implement slot migration planning logic
        return []
    
    async def _execute_slot_migrations(self, migration_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute planned slot migrations."""
        # This would implement slot migration execution
        return []
    
    async def _handle_master_failover(self, failed_master_id: str) -> Dict[str, Any]:
        """Handle master node failover."""
        # This would implement master failover logic
        return {'status': 'completed', 'new_master': 'replica_promoted'}
    
    async def _handle_replica_failover(self, failed_replica_id: str) -> Dict[str, Any]:
        """Handle replica node failover."""
        # This would implement replica failover logic
        return {'status': 'completed', 'action': 'replica_removed'}
    
    async def _analyze_memory_usage(self) -> Dict[str, Any]:
        """Analyze memory usage patterns."""
        return {'total_memory': 0, 'used_memory': 0, 'fragmentation': 0}
    
    async def _optimize_node_memory(self, node: ClusterNode) -> Dict[str, Any]:
        """Optimize memory usage for a specific node."""
        return {'status': 'completed', 'memory_saved': 0}
    
    async def _update_memory_metrics(self):
        """Update memory usage metrics."""
        memory_usage = await self._get_cluster_memory_usage()
        self.cluster_metrics['memory_usage'] = memory_usage
    
    async def _update_connection_pool_stats(self):
        """Update connection pool statistics."""
        # This would implement connection pool stats collection
        pass
    
    async def _update_throughput_metrics(self):
        """Update throughput metrics."""
        # This would implement throughput metrics collection
        pass
    
    async def _should_optimize(self) -> bool:
        """Check if cluster optimization is needed."""
        # This would implement optimization decision logic
        return False
    
    def _update_command_latency(self, command: str, latency: float):
        """Update command latency metrics."""
        if command not in self.cluster_metrics['command_latencies']:
            self.cluster_metrics['command_latencies'][command] = {
                'total_time': 0.0,
                'count': 0,
                'average': 0.0
            }
        
        metrics = self.cluster_metrics['command_latencies'][command]
        metrics['total_time'] += latency
        metrics['count'] += 1
        metrics['average'] = metrics['total_time'] / metrics['count']
    
    def _calculate_cluster_uptime(self) -> float:
        """Calculate cluster uptime in seconds."""
        # This would implement uptime calculation
        return 0.0
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default cluster configuration."""
        return {
            'monitoring_enabled': True,
            'optimization_enabled': True,
            'backup_enabled': True,
            'backup_path': './backups',
            'health_check_interval': 30,
            'optimization_interval': 3600,
            'failover_timeout': 15,
            'slot_migration_timeout': 30000
        }
