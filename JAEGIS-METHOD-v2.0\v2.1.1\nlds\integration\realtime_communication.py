"""
N.L.D.S. Real-time Communication Layer
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

WebSocket-based real-time communication layer for seamless integration
with JAEGIS components, agents, and external systems.
"""

import asyncio
import websockets
import json
import uuid
from typing import Dict, List, Optional, Tuple, Any, Set, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from datetime import datetime, timedelta
import ssl
import certifi
from urllib.parse import urlparse

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# REAL-TIME COMMUNICATION STRUCTURES AND ENUMS
# ============================================================================

class MessageType(Enum):
    """Real-time message types."""
    COMMAND = "command"
    STATUS_UPDATE = "status_update"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    SUBSCRIPTION = "subscription"
    UNSUBSCRIPTION = "unsubscription"
    BROADCAST = "broadcast"
    DIRECT_MESSAGE = "direct_message"
    SYSTEM_ALERT = "system_alert"
    ERROR = "error"


class ConnectionStatus(Enum):
    """WebSocket connection status."""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


class SubscriptionType(Enum):
    """Subscription types for real-time updates."""
    COMMAND_STATUS = "command_status"
    AGENT_STATUS = "agent_status"
    SYSTEM_METRICS = "system_metrics"
    USER_NOTIFICATIONS = "user_notifications"
    ERROR_ALERTS = "error_alerts"
    PERFORMANCE_UPDATES = "performance_updates"
    ALL = "all"


@dataclass
class RealtimeMessage:
    """Real-time communication message."""
    message_id: str
    message_type: MessageType
    timestamp: datetime
    source: str
    destination: Optional[str]
    payload: Dict[str, Any]
    priority: str = "normal"  # low, normal, high, critical
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectionInfo:
    """WebSocket connection information."""
    connection_id: str
    websocket: websockets.WebSocketServerProtocol
    client_type: str
    client_id: str
    connected_at: datetime
    last_heartbeat: datetime
    subscriptions: Set[SubscriptionType]
    is_authenticated: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Subscription:
    """Subscription to real-time updates."""
    subscription_id: str
    connection_id: str
    subscription_type: SubscriptionType
    filters: Dict[str, Any]
    created_at: datetime
    last_update: datetime
    message_count: int = 0


@dataclass
class CommunicationStats:
    """Real-time communication statistics."""
    total_connections: int
    active_connections: int
    total_messages_sent: int
    total_messages_received: int
    average_latency_ms: float
    subscription_count: int
    error_count: int
    uptime_seconds: float


# ============================================================================
# REAL-TIME COMMUNICATION ENGINE
# ============================================================================

class RealtimeCommunicationEngine:
    """
    Real-time communication engine for JAEGIS integration.
    
    Features:
    - WebSocket server for real-time connections
    - Message routing and broadcasting
    - Subscription management
    - Connection pooling and management
    - Heartbeat monitoring
    - Authentication and authorization
    - Message queuing and delivery guarantees
    - Performance monitoring and analytics
    """
    
    def __init__(self, communication_config: Dict[str, Any]):
        """
        Initialize real-time communication engine.
        
        Args:
            communication_config: Configuration for real-time communication
        """
        self.config = communication_config
        self.host = communication_config.get("host", "localhost")
        self.port = communication_config.get("port", 8765)
        self.ssl_enabled = communication_config.get("ssl_enabled", False)
        self.ssl_cert_path = communication_config.get("ssl_cert_path")
        self.ssl_key_path = communication_config.get("ssl_key_path")
        
        # Connection management
        self.connections = {}  # connection_id -> ConnectionInfo
        self.subscriptions = {}  # subscription_id -> Subscription
        self.message_handlers = {}  # message_type -> handler_function
        self.message_queue = asyncio.Queue()
        
        # Authentication
        self.auth_enabled = communication_config.get("auth_enabled", True)
        self.auth_tokens = communication_config.get("auth_tokens", {})
        
        # Performance tracking
        self.stats = CommunicationStats(
            total_connections=0,
            active_connections=0,
            total_messages_sent=0,
            total_messages_received=0,
            average_latency_ms=0.0,
            subscription_count=0,
            error_count=0,
            uptime_seconds=0.0
        )
        
        # Server state
        self.server = None
        self.is_running = False
        self.start_time = None
        
        # Message routing
        self.broadcast_channels = {}  # channel -> set of connection_ids
        self.direct_routes = {}  # client_id -> connection_id
        
        # Heartbeat settings
        self.heartbeat_interval = communication_config.get("heartbeat_interval", 30)
        self.heartbeat_timeout = communication_config.get("heartbeat_timeout", 60)
    
    async def initialize_server(self) -> bool:
        """Initialize WebSocket server."""
        try:
            # Setup SSL context if enabled
            ssl_context = None
            if self.ssl_enabled and self.ssl_cert_path and self.ssl_key_path:
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                ssl_context.load_cert_chain(self.ssl_cert_path, self.ssl_key_path)
            
            # Register message handlers
            self._register_default_handlers()
            
            # Start WebSocket server
            self.server = await websockets.serve(
                self._handle_connection,
                self.host,
                self.port,
                ssl=ssl_context,
                ping_interval=self.heartbeat_interval,
                ping_timeout=self.heartbeat_timeout
            )
            
            self.is_running = True
            self.start_time = datetime.utcnow()
            
            # Start background tasks
            asyncio.create_task(self._message_processor())
            asyncio.create_task(self._heartbeat_monitor())
            asyncio.create_task(self._stats_updater())
            
            protocol = "wss" if self.ssl_enabled else "ws"
            logger.info(f"Real-time communication server started on {protocol}://{self.host}:{self.port}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize WebSocket server: {e}")
            return False
    
    def _register_default_handlers(self) -> None:
        """Register default message handlers."""
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat
        self.message_handlers[MessageType.SUBSCRIPTION] = self._handle_subscription
        self.message_handlers[MessageType.UNSUBSCRIPTION] = self._handle_unsubscription
        self.message_handlers[MessageType.COMMAND] = self._handle_command
        self.message_handlers[MessageType.STATUS_UPDATE] = self._handle_status_update
    
    async def _handle_connection(self, websocket, path):
        """Handle new WebSocket connection."""
        connection_id = str(uuid.uuid4())
        
        try:
            # Create connection info
            connection_info = ConnectionInfo(
                connection_id=connection_id,
                websocket=websocket,
                client_type="unknown",
                client_id="unknown",
                connected_at=datetime.utcnow(),
                last_heartbeat=datetime.utcnow(),
                subscriptions=set(),
                is_authenticated=not self.auth_enabled  # Auto-auth if disabled
            )
            
            self.connections[connection_id] = connection_info
            self.stats.total_connections += 1
            self.stats.active_connections += 1
            
            logger.info(f"New WebSocket connection: {connection_id}")
            
            # Send welcome message
            welcome_message = RealtimeMessage(
                message_id=str(uuid.uuid4()),
                message_type=MessageType.NOTIFICATION,
                timestamp=datetime.utcnow(),
                source="nlds_server",
                destination=connection_id,
                payload={
                    "type": "welcome",
                    "connection_id": connection_id,
                    "server_time": datetime.utcnow().isoformat(),
                    "auth_required": self.auth_enabled
                }
            )
            
            await self._send_message_to_connection(connection_id, welcome_message)
            
            # Handle incoming messages
            async for message in websocket:
                try:
                    await self._process_incoming_message(connection_id, message)
                except Exception as e:
                    logger.error(f"Error processing message from {connection_id}: {e}")
                    await self._send_error_message(connection_id, str(e))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed: {connection_id}")
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
        finally:
            # Cleanup connection
            await self._cleanup_connection(connection_id)
    
    async def _process_incoming_message(self, connection_id: str, raw_message: str) -> None:
        """Process incoming message from WebSocket."""
        try:
            message_data = json.loads(raw_message)
            
            # Create message object
            message = RealtimeMessage(
                message_id=message_data.get("message_id", str(uuid.uuid4())),
                message_type=MessageType(message_data.get("message_type")),
                timestamp=datetime.fromisoformat(message_data.get("timestamp", datetime.utcnow().isoformat())),
                source=connection_id,
                destination=message_data.get("destination"),
                payload=message_data.get("payload", {}),
                priority=message_data.get("priority", "normal"),
                correlation_id=message_data.get("correlation_id"),
                metadata=message_data.get("metadata", {})
            )
            
            # Update connection heartbeat
            if connection_id in self.connections:
                self.connections[connection_id].last_heartbeat = datetime.utcnow()
            
            # Check authentication
            if self.auth_enabled and not self.connections[connection_id].is_authenticated:
                if message.message_type != MessageType.COMMAND or message.payload.get("command") != "authenticate":
                    await self._send_error_message(connection_id, "Authentication required")
                    return
            
            # Route message to handler
            handler = self.message_handlers.get(message.message_type)
            if handler:
                await handler(connection_id, message)
            else:
                # Queue message for processing
                await self.message_queue.put((connection_id, message))
            
            self.stats.total_messages_received += 1
            
        except json.JSONDecodeError:
            await self._send_error_message(connection_id, "Invalid JSON message")
        except ValueError as e:
            await self._send_error_message(connection_id, f"Invalid message format: {e}")
        except Exception as e:
            logger.error(f"Message processing error: {e}")
            await self._send_error_message(connection_id, "Internal server error")
    
    async def _handle_heartbeat(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle heartbeat message."""
        # Send heartbeat response
        response = RealtimeMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.HEARTBEAT,
            timestamp=datetime.utcnow(),
            source="nlds_server",
            destination=connection_id,
            payload={"status": "alive", "server_time": datetime.utcnow().isoformat()},
            correlation_id=message.message_id
        )
        
        await self._send_message_to_connection(connection_id, response)
    
    async def _handle_subscription(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle subscription request."""
        try:
            subscription_type = SubscriptionType(message.payload.get("subscription_type"))
            filters = message.payload.get("filters", {})
            
            # Create subscription
            subscription_id = str(uuid.uuid4())
            subscription = Subscription(
                subscription_id=subscription_id,
                connection_id=connection_id,
                subscription_type=subscription_type,
                filters=filters,
                created_at=datetime.utcnow(),
                last_update=datetime.utcnow()
            )
            
            self.subscriptions[subscription_id] = subscription
            self.connections[connection_id].subscriptions.add(subscription_type)
            self.stats.subscription_count += 1
            
            # Send confirmation
            response = RealtimeMessage(
                message_id=str(uuid.uuid4()),
                message_type=MessageType.NOTIFICATION,
                timestamp=datetime.utcnow(),
                source="nlds_server",
                destination=connection_id,
                payload={
                    "type": "subscription_confirmed",
                    "subscription_id": subscription_id,
                    "subscription_type": subscription_type.value
                },
                correlation_id=message.message_id
            )
            
            await self._send_message_to_connection(connection_id, response)
            
        except ValueError:
            await self._send_error_message(connection_id, "Invalid subscription type")
    
    async def _handle_unsubscription(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle unsubscription request."""
        subscription_id = message.payload.get("subscription_id")
        
        if subscription_id in self.subscriptions:
            subscription = self.subscriptions[subscription_id]
            
            # Remove subscription
            del self.subscriptions[subscription_id]
            self.connections[connection_id].subscriptions.discard(subscription.subscription_type)
            self.stats.subscription_count -= 1
            
            # Send confirmation
            response = RealtimeMessage(
                message_id=str(uuid.uuid4()),
                message_type=MessageType.NOTIFICATION,
                timestamp=datetime.utcnow(),
                source="nlds_server",
                destination=connection_id,
                payload={
                    "type": "unsubscription_confirmed",
                    "subscription_id": subscription_id
                },
                correlation_id=message.message_id
            )
            
            await self._send_message_to_connection(connection_id, response)
        else:
            await self._send_error_message(connection_id, "Subscription not found")
    
    async def _handle_command(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle command message."""
        command = message.payload.get("command")
        
        if command == "authenticate":
            await self._handle_authentication(connection_id, message)
        elif command == "get_status":
            await self._handle_status_request(connection_id, message)
        elif command == "register_client":
            await self._handle_client_registration(connection_id, message)
        else:
            # Forward to external command handler
            await self.message_queue.put((connection_id, message))
    
    async def _handle_authentication(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle authentication request."""
        token = message.payload.get("token")
        client_id = message.payload.get("client_id")
        
        if token in self.auth_tokens:
            self.connections[connection_id].is_authenticated = True
            self.connections[connection_id].client_id = client_id or "authenticated_client"
            
            response = RealtimeMessage(
                message_id=str(uuid.uuid4()),
                message_type=MessageType.NOTIFICATION,
                timestamp=datetime.utcnow(),
                source="nlds_server",
                destination=connection_id,
                payload={"type": "authentication_success"},
                correlation_id=message.message_id
            )
        else:
            response = RealtimeMessage(
                message_id=str(uuid.uuid4()),
                message_type=MessageType.ERROR,
                timestamp=datetime.utcnow(),
                source="nlds_server",
                destination=connection_id,
                payload={"type": "authentication_failed", "message": "Invalid token"},
                correlation_id=message.message_id
            )
        
        await self._send_message_to_connection(connection_id, response)
    
    async def _handle_status_request(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle status request."""
        status_data = {
            "server_status": "running",
            "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "active_connections": self.stats.active_connections,
            "total_subscriptions": self.stats.subscription_count,
            "server_time": datetime.utcnow().isoformat()
        }
        
        response = RealtimeMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.STATUS_UPDATE,
            timestamp=datetime.utcnow(),
            source="nlds_server",
            destination=connection_id,
            payload=status_data,
            correlation_id=message.message_id
        )
        
        await self._send_message_to_connection(connection_id, response)
    
    async def _handle_client_registration(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle client registration."""
        client_type = message.payload.get("client_type", "unknown")
        client_id = message.payload.get("client_id", f"client_{connection_id[:8]}")
        
        self.connections[connection_id].client_type = client_type
        self.connections[connection_id].client_id = client_id
        
        # Register direct route
        self.direct_routes[client_id] = connection_id
        
        response = RealtimeMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.NOTIFICATION,
            timestamp=datetime.utcnow(),
            source="nlds_server",
            destination=connection_id,
            payload={
                "type": "registration_success",
                "client_id": client_id,
                "client_type": client_type
            },
            correlation_id=message.message_id
        )
        
        await self._send_message_to_connection(connection_id, response)
    
    async def _handle_status_update(self, connection_id: str, message: RealtimeMessage) -> None:
        """Handle status update message."""
        # Broadcast to subscribers
        await self._broadcast_to_subscribers(SubscriptionType.AGENT_STATUS, message)
    
    async def _send_message_to_connection(self, connection_id: str, message: RealtimeMessage) -> bool:
        """Send message to specific connection."""
        if connection_id not in self.connections:
            return False
        
        try:
            connection = self.connections[connection_id]
            message_data = asdict(message)
            message_data["timestamp"] = message.timestamp.isoformat()
            message_data["message_type"] = message.message_type.value
            
            await connection.websocket.send(json.dumps(message_data))
            self.stats.total_messages_sent += 1
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message to {connection_id}: {e}")
            return False
    
    async def _send_error_message(self, connection_id: str, error_message: str) -> None:
        """Send error message to connection."""
        error_msg = RealtimeMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.ERROR,
            timestamp=datetime.utcnow(),
            source="nlds_server",
            destination=connection_id,
            payload={"error": error_message}
        )
        
        await self._send_message_to_connection(connection_id, error_msg)
        self.stats.error_count += 1
    
    async def _broadcast_to_subscribers(self, subscription_type: SubscriptionType, message: RealtimeMessage) -> int:
        """Broadcast message to all subscribers of a type."""
        sent_count = 0
        
        for subscription in self.subscriptions.values():
            if subscription.subscription_type == subscription_type or subscription.subscription_type == SubscriptionType.ALL:
                if await self._send_message_to_connection(subscription.connection_id, message):
                    sent_count += 1
                    subscription.message_count += 1
                    subscription.last_update = datetime.utcnow()
        
        return sent_count
    
    async def _message_processor(self) -> None:
        """Process queued messages."""
        while self.is_running:
            try:
                connection_id, message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                
                # Process message based on type
                if message.message_type == MessageType.BROADCAST:
                    await self._handle_broadcast(message)
                elif message.message_type == MessageType.DIRECT_MESSAGE:
                    await self._handle_direct_message(message)
                else:
                    # Default: broadcast to relevant subscribers
                    subscription_map = {
                        MessageType.COMMAND: SubscriptionType.COMMAND_STATUS,
                        MessageType.STATUS_UPDATE: SubscriptionType.AGENT_STATUS,
                        MessageType.SYSTEM_ALERT: SubscriptionType.ERROR_ALERTS
                    }
                    
                    sub_type = subscription_map.get(message.message_type, SubscriptionType.ALL)
                    await self._broadcast_to_subscribers(sub_type, message)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Message processor error: {e}")
    
    async def _handle_broadcast(self, message: RealtimeMessage) -> None:
        """Handle broadcast message."""
        for connection_id in self.connections.keys():
            await self._send_message_to_connection(connection_id, message)
    
    async def _handle_direct_message(self, message: RealtimeMessage) -> None:
        """Handle direct message."""
        if message.destination:
            # Try direct connection ID first
            if message.destination in self.connections:
                await self._send_message_to_connection(message.destination, message)
            # Try client ID route
            elif message.destination in self.direct_routes:
                connection_id = self.direct_routes[message.destination]
                await self._send_message_to_connection(connection_id, message)
    
    async def _heartbeat_monitor(self) -> None:
        """Monitor connection heartbeats."""
        while self.is_running:
            try:
                current_time = datetime.utcnow()
                timeout_threshold = current_time - timedelta(seconds=self.heartbeat_timeout)
                
                # Check for timed out connections
                timed_out_connections = []
                for connection_id, connection in self.connections.items():
                    if connection.last_heartbeat < timeout_threshold:
                        timed_out_connections.append(connection_id)
                
                # Cleanup timed out connections
                for connection_id in timed_out_connections:
                    logger.warning(f"Connection {connection_id} timed out")
                    await self._cleanup_connection(connection_id)
                
                await asyncio.sleep(self.heartbeat_interval)
                
            except Exception as e:
                logger.error(f"Heartbeat monitor error: {e}")
                await asyncio.sleep(self.heartbeat_interval)
    
    async def _stats_updater(self) -> None:
        """Update statistics periodically."""
        while self.is_running:
            try:
                if self.start_time:
                    self.stats.uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()
                
                self.stats.active_connections = len(self.connections)
                
                await asyncio.sleep(60)  # Update every minute
                
            except Exception as e:
                logger.error(f"Stats updater error: {e}")
                await asyncio.sleep(60)
    
    async def _cleanup_connection(self, connection_id: str) -> None:
        """Cleanup connection and associated resources."""
        if connection_id in self.connections:
            connection = self.connections[connection_id]
            
            # Remove subscriptions
            subscriptions_to_remove = [
                sub_id for sub_id, sub in self.subscriptions.items()
                if sub.connection_id == connection_id
            ]
            
            for sub_id in subscriptions_to_remove:
                del self.subscriptions[sub_id]
                self.stats.subscription_count -= 1
            
            # Remove direct routes
            client_id = connection.client_id
            if client_id in self.direct_routes:
                del self.direct_routes[client_id]
            
            # Close WebSocket
            try:
                await connection.websocket.close()
            except:
                pass
            
            # Remove connection
            del self.connections[connection_id]
            self.stats.active_connections -= 1
            
            logger.info(f"Connection {connection_id} cleaned up")
    
    async def send_message(self, message: RealtimeMessage) -> bool:
        """Send message through the communication layer."""
        await self.message_queue.put((None, message))
        return True
    
    async def broadcast_message(self, payload: Dict[str, Any], 
                              message_type: MessageType = MessageType.BROADCAST,
                              priority: str = "normal") -> int:
        """Broadcast message to all connections."""
        message = RealtimeMessage(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            timestamp=datetime.utcnow(),
            source="nlds_server",
            destination=None,
            payload=payload,
            priority=priority
        )
        
        await self.send_message(message)
        return len(self.connections)
    
    async def get_communication_status(self) -> Dict[str, Any]:
        """Get current communication layer status."""
        return {
            "server_running": self.is_running,
            "host": self.host,
            "port": self.port,
            "ssl_enabled": self.ssl_enabled,
            "auth_enabled": self.auth_enabled,
            "statistics": asdict(self.stats),
            "connections": {
                "total": len(self.connections),
                "by_type": {},
                "authenticated": len([c for c in self.connections.values() if c.is_authenticated])
            },
            "subscriptions": {
                "total": len(self.subscriptions),
                "by_type": {}
            },
            "uptime_seconds": self.stats.uptime_seconds
        }
    
    async def shutdown(self) -> None:
        """Shutdown communication server."""
        try:
            self.is_running = False
            
            # Close all connections
            for connection_id in list(self.connections.keys()):
                await self._cleanup_connection(connection_id)
            
            # Close server
            if self.server:
                self.server.close()
                await self.server.wait_closed()
            
            logger.info("Real-time communication server shut down")
            
        except Exception as e:
            logger.error(f"Error during communication server shutdown: {e}")


# ============================================================================
# COMMUNICATION UTILITIES
# ============================================================================

class RealtimeCommunicationUtils:
    """Utility functions for real-time communication."""
    
    @staticmethod
    def create_message(message_type: MessageType, payload: Dict[str, Any],
                      destination: Optional[str] = None, priority: str = "normal") -> RealtimeMessage:
        """Create a real-time message."""
        return RealtimeMessage(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            timestamp=datetime.utcnow(),
            source="nlds_client",
            destination=destination,
            payload=payload,
            priority=priority
        )
    
    @staticmethod
    def message_to_dict(message: RealtimeMessage) -> Dict[str, Any]:
        """Convert message to dictionary format."""
        data = asdict(message)
        data["timestamp"] = message.timestamp.isoformat()
        data["message_type"] = message.message_type.value
        return data
    
    @staticmethod
    def validate_communication_config(config: Dict[str, Any]) -> List[str]:
        """Validate communication configuration."""
        errors = []
        
        if config.get("ssl_enabled", False):
            if not config.get("ssl_cert_path"):
                errors.append("SSL enabled but no certificate path provided")
            if not config.get("ssl_key_path"):
                errors.append("SSL enabled but no key path provided")
        
        port = config.get("port", 8765)
        if not isinstance(port, int) or port < 1 or port > 65535:
            errors.append("Invalid port number")
        
        return errors
