"""
P.I.T.C.E.S. Framework - Redis Streams Manager
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements Redis Streams for real-time task queue management,
distributed processing, and event-driven coordination across the P.I.T.C.E.S. framework.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import asdict
from uuid import UUID, uuid4
from enum import Enum

import redis.asyncio as aioredis

from .models import Task, Priority, TaskStatus, WorkflowType
from .exceptions import PITCESError, ErrorCodes


logger = logging.getLogger(__name__)


class StreamType(Enum):
    """Types of Redis Streams for different purposes."""
    TASK_PRIORITY = "pitces:tasks:priority"
    TASK_PREEMPTION = "pitces:tasks:preemption"
    WORKFLOW_DECISIONS = "pitces:workflow:decisions"
    GAP_ANALYSIS = "pitces:gap:analysis"
    AGENT_COORDINATION = "pitces:agent:coordination"
    NLDS_PROCESSING = "pitces:nlds:processing"
    SYSTEM_EVENTS = "pitces:system:events"


class ConsumerGroup(Enum):
    """Consumer groups for distributed processing."""
    TASK_PROCESSORS = "task_processors"
    WORKFLOW_MANAGERS = "workflow_managers"
    ANALYSIS_ENGINES = "analysis_engines"
    AGENT_COORDINATORS = "agent_coordinators"
    NLDS_PROCESSORS = "nlds_processors"
    SYSTEM_MONITORS = "system_monitors"


class MessagePriority(Enum):
    """Message priority levels for stream processing."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class RedisStreamsManager:
    """
    Redis Streams manager for real-time task queue management and event processing.
    
    Features:
    - Real-time task queue management with priority handling
    - Distributed consumer groups for scalable processing
    - Event-driven coordination between P.I.T.C.E.S. components
    - Stream monitoring and performance optimization
    - Automatic failover and message acknowledgment
    - Dead letter queue handling for failed messages
    """
    
    def __init__(self, redis_client: aioredis.Redis, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Redis Streams Manager.
        
        Args:
            redis_client: Async Redis client instance
            config: Streams configuration
        """
        self.redis_client = redis_client
        self.config = config or self._get_default_config()
        
        # Stream configurations
        self.stream_configs = {
            StreamType.TASK_PRIORITY: {
                'max_length': 10000,
                'consumer_groups': [ConsumerGroup.TASK_PROCESSORS],
                'retention_hours': 24
            },
            StreamType.TASK_PREEMPTION: {
                'max_length': 5000,
                'consumer_groups': [ConsumerGroup.TASK_PROCESSORS],
                'retention_hours': 12
            },
            StreamType.WORKFLOW_DECISIONS: {
                'max_length': 1000,
                'consumer_groups': [ConsumerGroup.WORKFLOW_MANAGERS],
                'retention_hours': 168  # 1 week
            },
            StreamType.GAP_ANALYSIS: {
                'max_length': 500,
                'consumer_groups': [ConsumerGroup.ANALYSIS_ENGINES],
                'retention_hours': 720  # 30 days
            },
            StreamType.AGENT_COORDINATION: {
                'max_length': 20000,
                'consumer_groups': [ConsumerGroup.AGENT_COORDINATORS],
                'retention_hours': 6
            },
            StreamType.NLDS_PROCESSING: {
                'max_length': 15000,
                'consumer_groups': [ConsumerGroup.NLDS_PROCESSORS],
                'retention_hours': 48
            },
            StreamType.SYSTEM_EVENTS: {
                'max_length': 50000,
                'consumer_groups': [ConsumerGroup.SYSTEM_MONITORS],
                'retention_hours': 168  # 1 week
            }
        }
        
        # Active consumers tracking
        self.active_consumers = {}
        
        # Message handlers
        self.message_handlers: Dict[StreamType, List[Callable]] = {
            stream_type: [] for stream_type in StreamType
        }
        
        # Performance metrics
        self.stream_metrics = {
            'messages_published': 0,
            'messages_consumed': 0,
            'messages_acknowledged': 0,
            'messages_failed': 0,
            'consumer_lag': {},
            'processing_times': {},
            'stream_lengths': {},
            'dead_letter_count': 0
        }
        
        # Dead letter queue
        self.dead_letter_stream = "pitces:dead_letter_queue"
        
        logger.info("RedisStreamsManager initialized")
    
    async def initialize_streams(self) -> bool:
        """
        Initialize all Redis Streams and consumer groups.
        
        Returns:
            True if initialization successful
        """
        try:
            # Create streams and consumer groups
            for stream_type, config in self.stream_configs.items():
                await self._create_stream_and_groups(stream_type, config)
            
            # Create dead letter queue
            await self._create_dead_letter_queue()
            
            # Start background monitoring
            asyncio.create_task(self._monitor_streams())
            
            logger.info("Redis Streams initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"Redis Streams initialization failed: {e}")
            return False
    
    async def publish_task_priority_message(
        self, 
        task: Task,
        priority_change: Optional[Priority] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Publish task priority message to stream.
        
        Args:
            task: Task object
            priority_change: New priority if changed
            context: Additional context data
            
        Returns:
            Message ID
        """
        try:
            message_data = {
                'message_type': 'task_priority',
                'task_id': str(task.id),
                'task_data': json.dumps(task.to_dict()),
                'current_priority': task.priority.name,
                'new_priority': priority_change.name if priority_change else task.priority.name,
                'context': json.dumps(context or {}),
                'timestamp': datetime.now().isoformat(),
                'source': 'triage_system'
            }
            
            message_id = await self._publish_message(
                StreamType.TASK_PRIORITY, 
                message_data,
                MessagePriority.HIGH if priority_change else MessagePriority.MEDIUM
            )
            
            logger.debug(f"Published task priority message: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish task priority message: {e}")
            raise PITCESError(
                f"Task priority message publish failed: {str(e)}",
                error_code=ErrorCodes.STREAM_PUBLISH_FAILURE
            )
    
    async def publish_task_preemption_message(
        self, 
        task_id: UUID,
        preemption_type: str,
        context_data: Dict[str, Any]
    ) -> str:
        """
        Publish task preemption message to stream.
        
        Args:
            task_id: Task identifier
            preemption_type: Type of preemption (pause, resume, cancel)
            context_data: Preemption context
            
        Returns:
            Message ID
        """
        try:
            message_data = {
                'message_type': 'task_preemption',
                'task_id': str(task_id),
                'preemption_type': preemption_type,
                'context_data': json.dumps(context_data),
                'timestamp': datetime.now().isoformat(),
                'source': 'preemption_manager'
            }
            
            # Preemption messages are always high priority
            message_id = await self._publish_message(
                StreamType.TASK_PREEMPTION, 
                message_data,
                MessagePriority.HIGH
            )
            
            logger.debug(f"Published task preemption message: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish task preemption message: {e}")
            raise PITCESError(
                f"Task preemption message publish failed: {str(e)}",
                error_code=ErrorCodes.STREAM_PUBLISH_FAILURE
            )
    
    async def publish_workflow_decision_message(
        self, 
        project_specs: Dict[str, Any],
        workflow_type: WorkflowType,
        decision_context: Dict[str, Any]
    ) -> str:
        """
        Publish workflow decision message to stream.
        
        Args:
            project_specs: Project specifications
            workflow_type: Selected workflow type
            decision_context: Decision context data
            
        Returns:
            Message ID
        """
        try:
            message_data = {
                'message_type': 'workflow_decision',
                'project_specs': json.dumps(project_specs),
                'workflow_type': workflow_type.value,
                'decision_context': json.dumps(decision_context),
                'timestamp': datetime.now().isoformat(),
                'source': 'workflow_selector'
            }
            
            message_id = await self._publish_message(
                StreamType.WORKFLOW_DECISIONS, 
                message_data,
                MessagePriority.MEDIUM
            )
            
            logger.debug(f"Published workflow decision message: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish workflow decision message: {e}")
            raise PITCESError(
                f"Workflow decision message publish failed: {str(e)}",
                error_code=ErrorCodes.STREAM_PUBLISH_FAILURE
            )
    
    async def publish_gap_analysis_message(
        self, 
        project_specs: Dict[str, Any],
        analysis_results: Dict[str, Any],
        recommendations: List[str]
    ) -> str:
        """
        Publish gap analysis message to stream.
        
        Args:
            project_specs: Project specifications
            analysis_results: Gap analysis results
            recommendations: Generated recommendations
            
        Returns:
            Message ID
        """
        try:
            message_data = {
                'message_type': 'gap_analysis',
                'project_specs': json.dumps(project_specs),
                'analysis_results': json.dumps(analysis_results),
                'recommendations': json.dumps(recommendations),
                'timestamp': datetime.now().isoformat(),
                'source': 'gap_analysis_squad'
            }
            
            message_id = await self._publish_message(
                StreamType.GAP_ANALYSIS, 
                message_data,
                MessagePriority.LOW
            )
            
            logger.debug(f"Published gap analysis message: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish gap analysis message: {e}")
            raise PITCESError(
                f"Gap analysis message publish failed: {str(e)}",
                error_code=ErrorCodes.STREAM_PUBLISH_FAILURE
            )
    
    async def publish_agent_coordination_message(
        self, 
        agent_tier: int,
        coordination_type: str,
        coordination_data: Dict[str, Any]
    ) -> str:
        """
        Publish agent coordination message to stream.
        
        Args:
            agent_tier: Agent tier (1-6)
            coordination_type: Type of coordination
            coordination_data: Coordination data
            
        Returns:
            Message ID
        """
        try:
            message_data = {
                'message_type': 'agent_coordination',
                'agent_tier': agent_tier,
                'coordination_type': coordination_type,
                'coordination_data': json.dumps(coordination_data),
                'timestamp': datetime.now().isoformat(),
                'source': 'agent_system'
            }
            
            # Agent coordination priority based on tier
            priority = MessagePriority.HIGH if agent_tier <= 2 else MessagePriority.MEDIUM
            
            message_id = await self._publish_message(
                StreamType.AGENT_COORDINATION, 
                message_data,
                priority
            )
            
            logger.debug(f"Published agent coordination message: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish agent coordination message: {e}")
            raise PITCESError(
                f"Agent coordination message publish failed: {str(e)}",
                error_code=ErrorCodes.STREAM_PUBLISH_FAILURE
            )
    
    async def publish_nlds_processing_message(
        self, 
        text_input: str,
        processing_type: str,
        confidence_threshold: float = 0.85
    ) -> str:
        """
        Publish N.L.D.S. processing message to stream.
        
        Args:
            text_input: Natural language input
            processing_type: Type of processing required
            confidence_threshold: Minimum confidence threshold
            
        Returns:
            Message ID
        """
        try:
            message_data = {
                'message_type': 'nlds_processing',
                'text_input': text_input,
                'processing_type': processing_type,
                'confidence_threshold': confidence_threshold,
                'timestamp': datetime.now().isoformat(),
                'source': 'nlds_tier_0'
            }
            
            message_id = await self._publish_message(
                StreamType.NLDS_PROCESSING, 
                message_data,
                MessagePriority.HIGH
            )
            
            logger.debug(f"Published N.L.D.S. processing message: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish N.L.D.S. processing message: {e}")
            raise PITCESError(
                f"N.L.D.S. processing message publish failed: {str(e)}",
                error_code=ErrorCodes.STREAM_PUBLISH_FAILURE
            )
    
    async def publish_system_event_message(
        self, 
        event_type: str,
        event_data: Dict[str, Any],
        severity: str = "INFO"
    ) -> str:
        """
        Publish system event message to stream.
        
        Args:
            event_type: Type of system event
            event_data: Event data
            severity: Event severity (INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Message ID
        """
        try:
            message_data = {
                'message_type': 'system_event',
                'event_type': event_type,
                'event_data': json.dumps(event_data),
                'severity': severity,
                'timestamp': datetime.now().isoformat(),
                'source': 'pitces_framework'
            }
            
            # Priority based on severity
            priority_map = {
                'CRITICAL': MessagePriority.CRITICAL,
                'ERROR': MessagePriority.HIGH,
                'WARNING': MessagePriority.MEDIUM,
                'INFO': MessagePriority.LOW
            }
            priority = priority_map.get(severity, MessagePriority.LOW)
            
            message_id = await self._publish_message(
                StreamType.SYSTEM_EVENTS, 
                message_data,
                priority
            )
            
            logger.debug(f"Published system event message: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish system event message: {e}")
            raise PITCESError(
                f"System event message publish failed: {str(e)}",
                error_code=ErrorCodes.STREAM_PUBLISH_FAILURE
            )
    
    async def start_consumer(
        self, 
        stream_type: StreamType,
        consumer_group: ConsumerGroup,
        consumer_name: str,
        message_handler: Callable[[Dict[str, Any]], bool]
    ) -> bool:
        """
        Start a consumer for a specific stream.
        
        Args:
            stream_type: Type of stream to consume
            consumer_group: Consumer group name
            consumer_name: Unique consumer identifier
            message_handler: Function to handle messages
            
        Returns:
            True if consumer started successfully
        """
        try:
            consumer_key = f"{stream_type.value}:{consumer_group.value}:{consumer_name}"
            
            if consumer_key in self.active_consumers:
                logger.warning(f"Consumer already active: {consumer_key}")
                return False
            
            # Register message handler
            self.message_handlers[stream_type].append(message_handler)
            
            # Start consumer task
            consumer_task = asyncio.create_task(
                self._consume_messages(stream_type, consumer_group, consumer_name, message_handler)
            )
            
            self.active_consumers[consumer_key] = {
                'task': consumer_task,
                'stream_type': stream_type,
                'consumer_group': consumer_group,
                'consumer_name': consumer_name,
                'start_time': datetime.now(),
                'messages_processed': 0,
                'last_activity': datetime.now()
            }
            
            logger.info(f"Started consumer: {consumer_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start consumer: {e}")
            return False
    
    async def stop_consumer(
        self, 
        stream_type: StreamType,
        consumer_group: ConsumerGroup,
        consumer_name: str
    ) -> bool:
        """
        Stop a specific consumer.
        
        Args:
            stream_type: Type of stream
            consumer_group: Consumer group name
            consumer_name: Consumer identifier
            
        Returns:
            True if consumer stopped successfully
        """
        try:
            consumer_key = f"{stream_type.value}:{consumer_group.value}:{consumer_name}"
            
            if consumer_key not in self.active_consumers:
                logger.warning(f"Consumer not found: {consumer_key}")
                return False
            
            # Cancel consumer task
            consumer_info = self.active_consumers[consumer_key]
            consumer_info['task'].cancel()
            
            try:
                await consumer_info['task']
            except asyncio.CancelledError:
                pass
            
            # Remove from active consumers
            del self.active_consumers[consumer_key]
            
            logger.info(f"Stopped consumer: {consumer_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop consumer: {e}")
            return False
    
    async def get_stream_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive stream metrics.
        
        Returns:
            Stream metrics dictionary
        """
        try:
            # Update stream lengths
            for stream_type in StreamType:
                try:
                    length = await self.redis_client.xlen(stream_type.value)
                    self.stream_metrics['stream_lengths'][stream_type.value] = length
                except Exception:
                    self.stream_metrics['stream_lengths'][stream_type.value] = 0
            
            # Update consumer lag
            await self._update_consumer_lag()
            
            # Calculate processing rates
            processing_rates = self._calculate_processing_rates()
            
            return {
                **self.stream_metrics,
                'active_consumers': len(self.active_consumers),
                'processing_rates': processing_rates,
                'consumer_details': {
                    key: {
                        'stream_type': info['stream_type'].value,
                        'consumer_group': info['consumer_group'].value,
                        'consumer_name': info['consumer_name'],
                        'messages_processed': info['messages_processed'],
                        'uptime_seconds': (datetime.now() - info['start_time']).total_seconds(),
                        'last_activity': info['last_activity'].isoformat()
                    }
                    for key, info in self.active_consumers.items()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get stream metrics: {e}")
            return self.stream_metrics
    
    async def _publish_message(
        self, 
        stream_type: StreamType,
        message_data: Dict[str, Any],
        priority: MessagePriority
    ) -> str:
        """Publish message to Redis Stream with priority handling."""
        try:
            # Add priority and metadata
            enhanced_message = {
                **message_data,
                'priority': priority.value,
                'message_id': str(uuid4()),
                'published_at': datetime.now().isoformat()
            }
            
            # Get stream configuration
            stream_config = self.stream_configs[stream_type]
            
            # Publish to stream with max length limit
            message_id = await self.redis_client.xadd(
                stream_type.value,
                enhanced_message,
                maxlen=stream_config['max_length'],
                approximate=True
            )
            
            self.stream_metrics['messages_published'] += 1
            
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to publish message to {stream_type.value}: {e}")
            raise
    
    async def _consume_messages(
        self, 
        stream_type: StreamType,
        consumer_group: ConsumerGroup,
        consumer_name: str,
        message_handler: Callable[[Dict[str, Any]], bool]
    ):
        """Consume messages from Redis Stream."""
        try:
            while True:
                try:
                    # Read messages from stream
                    messages = await self.redis_client.xreadgroup(
                        consumer_group.value,
                        consumer_name,
                        {stream_type.value: '>'},
                        count=self.config['batch_size'],
                        block=self.config['block_timeout']
                    )
                    
                    for stream, msgs in messages:
                        for msg_id, fields in msgs:
                            start_time = time.time()
                            
                            try:
                                # Process message
                                success = await self._process_message(
                                    stream_type, msg_id, fields, message_handler
                                )
                                
                                if success:
                                    # Acknowledge message
                                    await self.redis_client.xack(
                                        stream_type.value,
                                        consumer_group.value,
                                        msg_id
                                    )
                                    self.stream_metrics['messages_acknowledged'] += 1
                                else:
                                    # Move to dead letter queue
                                    await self._move_to_dead_letter_queue(
                                        stream_type, msg_id, fields, "Processing failed"
                                    )
                                    self.stream_metrics['messages_failed'] += 1
                                
                                # Update metrics
                                processing_time = time.time() - start_time
                                self._update_processing_time(stream_type, processing_time)
                                
                                # Update consumer activity
                                consumer_key = f"{stream_type.value}:{consumer_group.value}:{consumer_name}"
                                if consumer_key in self.active_consumers:
                                    self.active_consumers[consumer_key]['messages_processed'] += 1
                                    self.active_consumers[consumer_key]['last_activity'] = datetime.now()
                                
                            except Exception as e:
                                logger.error(f"Message processing error: {e}")
                                await self._move_to_dead_letter_queue(
                                    stream_type, msg_id, fields, str(e)
                                )
                                self.stream_metrics['messages_failed'] += 1
                    
                    self.stream_metrics['messages_consumed'] += len(msgs) if messages else 0
                    
                except asyncio.CancelledError:
                    logger.info(f"Consumer cancelled: {consumer_name}")
                    break
                except Exception as e:
                    logger.error(f"Consumer error: {e}")
                    await asyncio.sleep(5)  # Wait before retrying
                    
        except Exception as e:
            logger.error(f"Consumer {consumer_name} failed: {e}")
    
    async def _process_message(
        self, 
        stream_type: StreamType,
        msg_id: str,
        fields: Dict[str, Any],
        message_handler: Callable[[Dict[str, Any]], bool]
    ) -> bool:
        """Process individual message."""
        try:
            # Parse message data
            message_data = {
                'stream_type': stream_type.value,
                'message_id': msg_id,
                'fields': fields,
                'timestamp': fields.get('timestamp'),
                'priority': int(fields.get('priority', MessagePriority.MEDIUM.value))
            }
            
            # Call message handler
            success = await asyncio.get_event_loop().run_in_executor(
                None, message_handler, message_data
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Message processing failed: {e}")
            return False
    
    async def _create_stream_and_groups(
        self, 
        stream_type: StreamType, 
        config: Dict[str, Any]
    ):
        """Create stream and consumer groups."""
        try:
            # Create consumer groups
            for consumer_group in config['consumer_groups']:
                try:
                    await self.redis_client.xgroup_create(
                        stream_type.value,
                        consumer_group.value,
                        id='0',
                        mkstream=True
                    )
                    logger.debug(f"Created consumer group: {consumer_group.value} for {stream_type.value}")
                except Exception as e:
                    if "BUSYGROUP" not in str(e):
                        logger.warning(f"Failed to create consumer group {consumer_group.value}: {e}")
            
        except Exception as e:
            logger.error(f"Failed to create stream and groups for {stream_type.value}: {e}")
            raise
    
    async def _create_dead_letter_queue(self):
        """Create dead letter queue stream."""
        try:
            await self.redis_client.xgroup_create(
                self.dead_letter_stream,
                'dead_letter_processors',
                id='0',
                mkstream=True
            )
        except Exception as e:
            if "BUSYGROUP" not in str(e):
                logger.warning(f"Failed to create dead letter queue: {e}")
    
    async def _move_to_dead_letter_queue(
        self, 
        stream_type: StreamType,
        msg_id: str,
        fields: Dict[str, Any],
        error_reason: str
    ):
        """Move failed message to dead letter queue."""
        try:
            dead_letter_data = {
                'original_stream': stream_type.value,
                'original_message_id': msg_id,
                'original_fields': json.dumps(fields),
                'error_reason': error_reason,
                'failed_at': datetime.now().isoformat()
            }
            
            await self.redis_client.xadd(
                self.dead_letter_stream,
                dead_letter_data,
                maxlen=1000,
                approximate=True
            )
            
            self.stream_metrics['dead_letter_count'] += 1
            
        except Exception as e:
            logger.error(f"Failed to move message to dead letter queue: {e}")
    
    async def _monitor_streams(self):
        """Background task to monitor stream health."""
        while True:
            try:
                await asyncio.sleep(60)  # Monitor every minute
                
                # Check stream lengths and consumer lag
                await self._update_consumer_lag()
                
                # Clean up old messages based on retention policy
                await self._cleanup_old_messages()
                
                # Monitor consumer health
                await self._monitor_consumer_health()
                
            except Exception as e:
                logger.error(f"Stream monitoring error: {e}")
    
    async def _update_consumer_lag(self):
        """Update consumer lag metrics."""
        for stream_type in StreamType:
            try:
                # Get consumer group info
                groups = await self.redis_client.xinfo_groups(stream_type.value)
                
                for group in groups:
                    group_name = group['name']
                    lag = group.get('lag', 0)
                    
                    self.stream_metrics['consumer_lag'][f"{stream_type.value}:{group_name}"] = lag
                    
            except Exception as e:
                logger.debug(f"Failed to get consumer lag for {stream_type.value}: {e}")
    
    async def _cleanup_old_messages(self):
        """Clean up old messages based on retention policy."""
        for stream_type, config in self.stream_configs.items():
            try:
                retention_hours = config['retention_hours']
                cutoff_time = datetime.now() - timedelta(hours=retention_hours)
                cutoff_timestamp = int(cutoff_time.timestamp() * 1000)
                
                # Trim stream by timestamp
                await self.redis_client.xtrim(
                    stream_type.value,
                    minid=f"{cutoff_timestamp}-0",
                    approximate=True
                )
                
            except Exception as e:
                logger.debug(f"Failed to cleanup old messages for {stream_type.value}: {e}")
    
    async def _monitor_consumer_health(self):
        """Monitor consumer health and restart if needed."""
        current_time = datetime.now()
        
        for consumer_key, consumer_info in list(self.active_consumers.items()):
            try:
                # Check if consumer is still active
                if consumer_info['task'].done():
                    logger.warning(f"Consumer task completed unexpectedly: {consumer_key}")
                    del self.active_consumers[consumer_key]
                    continue
                
                # Check for stale consumers (no activity for 10 minutes)
                time_since_activity = current_time - consumer_info['last_activity']
                if time_since_activity > timedelta(minutes=10):
                    logger.warning(f"Consumer appears stale: {consumer_key}")
                    # Could implement automatic restart here
                
            except Exception as e:
                logger.error(f"Consumer health check failed for {consumer_key}: {e}")
    
    def _update_processing_time(self, stream_type: StreamType, processing_time: float):
        """Update processing time metrics."""
        stream_name = stream_type.value
        
        if stream_name not in self.stream_metrics['processing_times']:
            self.stream_metrics['processing_times'][stream_name] = {
                'total_time': 0.0,
                'message_count': 0,
                'average_time': 0.0
            }
        
        metrics = self.stream_metrics['processing_times'][stream_name]
        metrics['total_time'] += processing_time
        metrics['message_count'] += 1
        metrics['average_time'] = metrics['total_time'] / metrics['message_count']
    
    def _calculate_processing_rates(self) -> Dict[str, float]:
        """Calculate message processing rates."""
        rates = {}
        
        for consumer_key, consumer_info in self.active_consumers.items():
            uptime = (datetime.now() - consumer_info['start_time']).total_seconds()
            if uptime > 0:
                rate = consumer_info['messages_processed'] / uptime
                rates[consumer_key] = rate
        
        return rates
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default streams configuration."""
        return {
            'batch_size': 10,
            'block_timeout': 1000,  # 1 second
            'max_retries': 3,
            'retry_delay': 5,
            'enable_monitoring': True,
            'cleanup_interval': 3600  # 1 hour
        }
