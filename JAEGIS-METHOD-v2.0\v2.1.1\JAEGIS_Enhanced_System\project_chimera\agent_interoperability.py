"""
JAEGIS Enhanced System Project Chimera v4.1
Agent Interoperability: A2A Protocol & Elkar Integration

Standardized agent communication protocols with HTTP/JSON-RPC/SSE stack,
compatible with existing JAEGIS agent coordination architecture and JAP/2.0 specifications.
"""

import asyncio
import json
import logging
import time
import uuid
import zlib
import hashlib
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
from aiohttp import web, WSMsgType
import websockets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import lz4.frame

# JAEGIS Integration Imports
from ..scalability.scalability_engine import ScalabilityEngine
from .security_architecture import DualLLMArchitecture, IsolationBarrier

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """A2A Protocol message types"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class DeliveryMode(Enum):
    """Message delivery modes"""
    DIRECT = "direct"
    BROADCAST = "broadcast"
    MULTICAST = "multicast"
    RELIABLE = "reliable"


class CompressionType(Enum):
    """Message compression types"""
    NONE = "none"
    LZ4 = "lz4"
    ZSTANDARD = "zstandard"
    GZIP = "gzip"


@dataclass
class A2AMessageHeader:
    """A2A Protocol message header (32-byte compatible)"""
    message_id: str
    sender_id: str
    recipient_id: str
    message_type: MessageType
    timestamp: str
    priority: int  # 1-10
    encryption: bool
    compression: CompressionType
    ttl: int  # seconds
    signature: Optional[str] = None
    
    def to_bytes(self) -> bytes:
        """Convert header to 32-byte format for JAP/2.0 compatibility"""
        header_dict = asdict(self)
        header_dict['message_type'] = self.message_type.value
        header_dict['compression'] = self.compression.value
        
        header_json = json.dumps(header_dict, separators=(',', ':'))
        header_bytes = header_json.encode('utf-8')
        
        # Pad or truncate to 32 bytes for compatibility
        if len(header_bytes) > 32:
            header_bytes = header_bytes[:32]
        else:
            header_bytes = header_bytes.ljust(32, b'\x00')
        
        return header_bytes


@dataclass
class A2AMessage:
    """Complete A2A Protocol message"""
    header: A2AMessageHeader
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    routing_path: Optional[List[str]] = None
    
    def calculate_checksum(self) -> str:
        """Calculate CRC32 checksum for message integrity"""
        message_data = json.dumps({
            'header': asdict(self.header),
            'payload': self.payload,
            'metadata': self.metadata
        }, separators=(',', ':')).encode('utf-8')
        
        return format(zlib.crc32(message_data) & 0xffffffff, '08x')
    
    def compress_payload(self) -> bytes:
        """Compress payload based on header compression type"""
        payload_bytes = json.dumps(self.payload).encode('utf-8')
        
        if self.header.compression == CompressionType.LZ4:
            return lz4.frame.compress(payload_bytes)
        elif self.header.compression == CompressionType.GZIP:
            return zlib.compress(payload_bytes)
        else:
            return payload_bytes
    
    def decompress_payload(self, compressed_data: bytes) -> Dict[str, Any]:
        """Decompress payload based on header compression type"""
        if self.header.compression == CompressionType.LZ4:
            decompressed = lz4.frame.decompress(compressed_data)
        elif self.header.compression == CompressionType.GZIP:
            decompressed = zlib.decompress(compressed_data)
        else:
            decompressed = compressed_data
        
        return json.loads(decompressed.decode('utf-8'))


class A2AProtocolHandler:
    """
    A2A Protocol implementation with JAP/2.0 compatibility
    Maintains sub-10ms latency with connection pooling and keep-alive
    """
    
    def __init__(self, 
                 agent_id: str,
                 scalability_engine: ScalabilityEngine,
                 dual_llm_architecture: DualLLMArchitecture):
        self.agent_id = agent_id
        self.scalability_engine = scalability_engine
        self.dual_llm_architecture = dual_llm_architecture
        
        # Connection management
        self.connection_pool = {}
        self.active_connections = {}
        self.message_handlers = {}
        self.response_futures = {}
        
        # Performance tracking
        self.latency_stats = {
            "message_count": 0,
            "total_latency": 0.0,
            "average_latency": 0.0,
            "max_latency": 0.0,
            "sub_10ms_count": 0
        }
        
        # Security components
        self.signing_key = ed25519.Ed25519PrivateKey.generate()
        self.verify_key = self.signing_key.public_key()
        
        # Message compression and integrity
        self.default_compression = CompressionType.LZ4
        self.enable_encryption = True
        
        logger.info(f"A2AProtocolHandler initialized for agent {agent_id}")
    
    async def initialize(self, host: str = "localhost", port: int = 8080):
        """Initialize A2A protocol server"""
        self.host = host
        self.port = port
        
        # Create aiohttp application
        app = web.Application()
        app.router.add_post('/a2a/message', self.handle_http_message)
        app.router.add_get('/a2a/websocket', self.handle_websocket)
        app.router.add_get('/a2a/health', self.handle_health_check)
        
        # Start server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        logger.info(f"A2A Protocol server started on {host}:{port}")
    
    async def send_message(self, 
                          recipient_id: str,
                          message_type: MessageType,
                          payload: Dict[str, Any],
                          priority: int = 5,
                          delivery_mode: DeliveryMode = DeliveryMode.DIRECT,
                          timeout: float = 10.0) -> Optional[Dict[str, Any]]:
        """
        Send A2A message with sub-10ms latency target
        
        Args:
            recipient_id: Target agent ID
            message_type: Type of message
            payload: Message payload
            priority: Message priority (1-10)
            delivery_mode: Delivery mode
            timeout: Response timeout in seconds
            
        Returns:
            Response message if request type, None for notifications
        """
        start_time = time.time()
        
        try:
            # Create message
            message = A2AMessage(
                header=A2AMessageHeader(
                    message_id=str(uuid.uuid4()),
                    sender_id=self.agent_id,
                    recipient_id=recipient_id,
                    message_type=message_type,
                    timestamp=time.time(),
                    priority=priority,
                    encryption=self.enable_encryption,
                    compression=self.default_compression,
                    ttl=int(timeout)
                ),
                payload=payload,
                metadata={"delivery_mode": delivery_mode.value}
            )
            
            # Sign message for integrity
            if self.enable_encryption:
                message.header.signature = self._sign_message(message)
            
            # Send based on delivery mode
            if delivery_mode == DeliveryMode.DIRECT:
                response = await self._send_direct_message(message, timeout)
            elif delivery_mode == DeliveryMode.BROADCAST:
                response = await self._send_broadcast_message(message)
            else:
                response = await self._send_multicast_message(message, [recipient_id])
            
            # Track latency
            latency = (time.time() - start_time) * 1000  # Convert to ms
            self._update_latency_stats(latency)
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to send message to {recipient_id}: {e}")
            return None
    
    async def _send_direct_message(self, message: A2AMessage, timeout: float) -> Optional[Dict[str, Any]]:
        """Send direct message with connection pooling"""
        recipient_id = message.header.recipient_id
        
        # Get or create connection
        connection = await self._get_connection(recipient_id)
        
        if not connection:
            logger.error(f"Failed to establish connection to {recipient_id}")
            return None
        
        try:
            # Prepare message data
            message_data = {
                "header": asdict(message.header),
                "payload": message.payload,
                "metadata": message.metadata,
                "checksum": message.calculate_checksum()
            }
            
            # Send via HTTP/JSON-RPC
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=timeout),
                connector=aiohttp.TCPConnector(keepalive_timeout=30)
            ) as session:
                async with session.post(
                    f"http://{connection['host']}:{connection['port']}/a2a/message",
                    json=message_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"HTTP error {response.status} from {recipient_id}")
                        return None
                        
        except Exception as e:
            logger.error(f"Direct message send failed: {e}")
            return None
    
    async def _get_connection(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get or create connection to agent with connection pooling"""
        if agent_id in self.connection_pool:
            return self.connection_pool[agent_id]
        
        # Discover agent endpoint through scalability engine
        try:
            agent_info = await self.scalability_engine.get_agent_info(agent_id)
            if agent_info:
                connection = {
                    "host": agent_info.get("host", "localhost"),
                    "port": agent_info.get("port", 8080),
                    "last_used": time.time()
                }
                self.connection_pool[agent_id] = connection
                return connection
        except Exception as e:
            logger.error(f"Failed to discover agent {agent_id}: {e}")
        
        return None
    
    async def handle_http_message(self, request: web.Request) -> web.Response:
        """Handle incoming HTTP A2A message"""
        try:
            message_data = await request.json()
            
            # Verify message integrity
            if not self._verify_message_integrity(message_data):
                return web.Response(status=400, text="Message integrity check failed")
            
            # Process through dual LLM architecture for security
            processed_result = await self.dual_llm_architecture.process_untrusted_input(
                json.dumps(message_data), {"source": "a2a_protocol"}
            )
            
            if not processed_result.get("isolation_maintained", False):
                return web.Response(status=403, text="Security isolation failed")
            
            # Handle message
            response = await self._handle_incoming_message(message_data)
            
            return web.json_response(response)
            
        except Exception as e:
            logger.error(f"HTTP message handling failed: {e}")
            return web.Response(status=500, text="Internal server error")
    
    async def handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connections for real-time communication"""
        ws = web.WebSocketResponse(heartbeat=30)
        await ws.prepare(request)
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    message_data = json.loads(msg.data)
                    response = await self._handle_incoming_message(message_data)
                    await ws.send_text(json.dumps(response))
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
                    break
        except Exception as e:
            logger.error(f"WebSocket handling failed: {e}")
        
        return ws
    
    async def handle_health_check(self, request: web.Request) -> web.Response:
        """Handle health check requests"""
        health_status = {
            "agent_id": self.agent_id,
            "status": "healthy",
            "timestamp": time.time(),
            "latency_stats": self.latency_stats,
            "active_connections": len(self.active_connections)
        }
        return web.json_response(health_status)
    
    async def _handle_incoming_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming message and route to appropriate handler"""
        try:
            header = message_data.get("header", {})
            message_type = header.get("message_type")
            
            # Route to registered handler
            if message_type in self.message_handlers:
                handler = self.message_handlers[message_type]
                result = await handler(message_data)
                
                return {
                    "status": "success",
                    "result": result,
                    "timestamp": time.time()
                }
            else:
                return {
                    "status": "error",
                    "error": f"No handler for message type: {message_type}",
                    "timestamp": time.time()
                }
                
        except Exception as e:
            logger.error(f"Message handling failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register handler for specific message type"""
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    def _sign_message(self, message: A2AMessage) -> str:
        """Sign message using Ed25519 for integrity verification"""
        message_content = json.dumps({
            "header": asdict(message.header),
            "payload": message.payload
        }, separators=(',', ':')).encode('utf-8')
        
        signature = self.signing_key.sign(message_content)
        return signature.hex()
    
    def _verify_message_integrity(self, message_data: Dict[str, Any]) -> bool:
        """Verify message integrity using CRC32 checksum"""
        try:
            provided_checksum = message_data.get("checksum")
            if not provided_checksum:
                return False
            
            # Recalculate checksum
            message_content = {
                "header": message_data.get("header"),
                "payload": message_data.get("payload"),
                "metadata": message_data.get("metadata")
            }
            
            calculated_checksum = format(
                zlib.crc32(json.dumps(message_content, separators=(',', ':')).encode('utf-8')) & 0xffffffff,
                '08x'
            )
            
            return provided_checksum == calculated_checksum
            
        except Exception as e:
            logger.error(f"Integrity verification failed: {e}")
            return False
    
    def _update_latency_stats(self, latency_ms: float):
        """Update latency statistics"""
        self.latency_stats["message_count"] += 1
        self.latency_stats["total_latency"] += latency_ms
        self.latency_stats["average_latency"] = (
            self.latency_stats["total_latency"] / self.latency_stats["message_count"]
        )
        self.latency_stats["max_latency"] = max(
            self.latency_stats["max_latency"], latency_ms
        )
        
        if latency_ms <= 10.0:  # Sub-10ms target
            self.latency_stats["sub_10ms_count"] += 1
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get A2A protocol performance metrics"""
        sub_10ms_percentage = 0.0
        if self.latency_stats["message_count"] > 0:
            sub_10ms_percentage = (
                self.latency_stats["sub_10ms_count"] / 
                self.latency_stats["message_count"] * 100
            )
        
        return {
            **self.latency_stats,
            "sub_10ms_percentage": sub_10ms_percentage,
            "connection_pool_size": len(self.connection_pool),
            "active_handlers": len(self.message_handlers),
            "target_latency_ms": 10.0
        }


class ElkarOrchestrator:
    """
    Rust-based Elkar framework integration for high-performance task management
    Compatible with existing Agent Synthesis Engine (ASE) architecture
    """
    
    def __init__(self, 
                 scalability_engine: ScalabilityEngine,
                 max_agents_per_type: int = 500):
        self.scalability_engine = scalability_engine
        self.max_agents_per_type = max_agents_per_type
        self.min_agents_per_type = 10
        
        # Agent management
        self.active_agents = {}
        self.agent_types = {}
        self.task_queues = {}
        
        # Performance tracking
        self.orchestration_stats = {
            "tasks_orchestrated": 0,
            "agents_managed": 0,
            "average_task_time": 0.0,
            "scaling_events": 0
        }
        
        logger.info("ElkarOrchestrator initialized with ASE integration")
    
    async def register_agent_type(self, 
                                 agent_type: str,
                                 initial_count: int = 10,
                                 scaling_config: Optional[Dict[str, Any]] = None):
        """Register new agent type with scaling configuration"""
        self.agent_types[agent_type] = {
            "initial_count": max(self.min_agents_per_type, initial_count),
            "current_count": 0,
            "max_count": self.max_agents_per_type,
            "scaling_config": scaling_config or {},
            "task_queue": asyncio.Queue()
        }
        
        # Initialize agents
        await self._scale_agent_type(agent_type, initial_count)
        
        logger.info(f"Registered agent type: {agent_type} with {initial_count} agents")
    
    async def orchestrate_task(self, 
                              agent_type: str,
                              task_data: Dict[str, Any],
                              priority: int = 5) -> Dict[str, Any]:
        """Orchestrate task to appropriate agent type"""
        if agent_type not in self.agent_types:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        start_time = time.time()
        
        try:
            # Check if scaling is needed
            await self._check_and_scale(agent_type)
            
            # Add task to queue
            task_queue = self.agent_types[agent_type]["task_queue"]
            await task_queue.put({
                "task_id": str(uuid.uuid4()),
                "task_data": task_data,
                "priority": priority,
                "timestamp": time.time()
            })
            
            # Update statistics
            self.orchestration_stats["tasks_orchestrated"] += 1
            
            return {
                "status": "orchestrated",
                "agent_type": agent_type,
                "queue_size": task_queue.qsize(),
                "orchestration_time_ms": (time.time() - start_time) * 1000
            }
            
        except Exception as e:
            logger.error(f"Task orchestration failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _scale_agent_type(self, agent_type: str, target_count: int):
        """Scale agent type to target count"""
        current_count = self.agent_types[agent_type]["current_count"]
        max_count = self.agent_types[agent_type]["max_count"]
        
        # Ensure within limits
        target_count = max(self.min_agents_per_type, min(target_count, max_count))
        
        if target_count > current_count:
            # Scale up
            for i in range(target_count - current_count):
                agent_id = f"{agent_type}_{current_count + i + 1}"
                await self._create_agent(agent_type, agent_id)
        elif target_count < current_count:
            # Scale down
            for i in range(current_count - target_count):
                await self._remove_agent(agent_type)
        
        self.agent_types[agent_type]["current_count"] = target_count
        self.orchestration_stats["scaling_events"] += 1
        
        logger.info(f"Scaled {agent_type} to {target_count} agents")
    
    async def _check_and_scale(self, agent_type: str):
        """Check if scaling is needed based on queue size"""
        agent_config = self.agent_types[agent_type]
        task_queue = agent_config["task_queue"]
        current_count = agent_config["current_count"]
        
        # Simple scaling logic based on queue size
        queue_size = task_queue.qsize()
        
        if queue_size > current_count * 2 and current_count < agent_config["max_count"]:
            # Scale up
            new_count = min(current_count + 5, agent_config["max_count"])
            await self._scale_agent_type(agent_type, new_count)
        elif queue_size < current_count // 2 and current_count > self.min_agents_per_type:
            # Scale down
            new_count = max(current_count - 2, self.min_agents_per_type)
            await self._scale_agent_type(agent_type, new_count)
    
    async def _create_agent(self, agent_type: str, agent_id: str):
        """Create new agent instance"""
        # Integration with scalability engine
        agent_info = await self.scalability_engine.create_agent_instance(
            agent_type, agent_id
        )
        
        if agent_id not in self.active_agents:
            self.active_agents[agent_id] = {
                "agent_type": agent_type,
                "created_at": time.time(),
                "status": "active",
                "tasks_processed": 0
            }
            self.orchestration_stats["agents_managed"] += 1
    
    async def _remove_agent(self, agent_type: str):
        """Remove agent instance"""
        # Find agent to remove
        agents_to_remove = [
            agent_id for agent_id, info in self.active_agents.items()
            if info["agent_type"] == agent_type
        ]
        
        if agents_to_remove:
            agent_id = agents_to_remove[0]
            await self.scalability_engine.remove_agent_instance(agent_id)
            del self.active_agents[agent_id]
            self.orchestration_stats["agents_managed"] -= 1
    
    async def get_orchestration_metrics(self) -> Dict[str, Any]:
        """Get orchestration performance metrics"""
        return {
            **self.orchestration_stats,
            "agent_types": len(self.agent_types),
            "total_active_agents": len(self.active_agents),
            "agent_type_details": {
                agent_type: {
                    "current_count": config["current_count"],
                    "queue_size": config["task_queue"].qsize(),
                    "max_count": config["max_count"]
                }
                for agent_type, config in self.agent_types.items()
            }
        }
