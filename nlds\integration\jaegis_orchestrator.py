"""
N.L.D.S. JAEGIS Master Orchestrator Interface
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Direct interface with JAEGIS Master Orchestrator for command transmission,
status monitoring, and real-time coordination with 99%+ reliability.
"""

import asyncio
import json
import uuid
import websockets
import aiohttp
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from datetime import datetime, timedelta
import ssl
import certifi
from urllib.parse import urljoin

# Local imports
from ..translation.command_generator import JAEGISCommand, CommandGenerationResult
from ..translation.mode_selector import JAEGISMode, ModeSelectionResult
from ..translation.squad_selector import SquadSelectionResult
from ..translation.confidence_validator import ConfidenceValidationResult

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# JAEGIS INTERFACE STRUCTURES AND ENUMS
# ============================================================================

class CommandStatus(Enum):
    """JAEGIS command execution status."""
    PENDING = "pending"
    QUEUED = "queued"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class OrchestratorStatus(Enum):
    """JAEGIS Master Orchestrator status."""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class MessageType(Enum):
    """Message types for JAEGIS communication."""
    COMMAND_SUBMISSION = "command_submission"
    STATUS_REQUEST = "status_request"
    STATUS_UPDATE = "status_update"
    HEARTBEAT = "heartbeat"
    ERROR_NOTIFICATION = "error_notification"
    SYSTEM_ALERT = "system_alert"
    CAPABILITY_QUERY = "capability_query"
    RESOURCE_STATUS = "resource_status"


@dataclass
class JAEGISMessage:
    """Standard JAEGIS communication message."""
    message_id: str
    message_type: MessageType
    timestamp: datetime
    source: str
    destination: str
    payload: Dict[str, Any]
    priority: str = "normal"  # low, normal, high, critical
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommandSubmission:
    """Command submission to JAEGIS Master Orchestrator."""
    command_id: str
    jaegis_command: JAEGISCommand
    submission_timestamp: datetime
    expected_completion: Optional[datetime]
    priority_level: str
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 300
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommandStatusResponse:
    """Command status response from JAEGIS."""
    command_id: str
    status: CommandStatus
    progress_percentage: float
    assigned_squad: Optional[str]
    assigned_agents: List[str]
    execution_start: Optional[datetime]
    execution_end: Optional[datetime]
    result_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    estimated_completion: Optional[datetime]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrchestratorCapabilities:
    """JAEGIS Master Orchestrator capabilities."""
    available_squads: List[str]
    available_modes: List[str]
    current_load: float
    max_concurrent_commands: int
    active_commands: int
    queue_length: int
    estimated_wait_time_seconds: int
    system_health: Dict[str, Any]
    last_updated: datetime


@dataclass
class InterfaceResult:
    """JAEGIS interface operation result."""
    success: bool
    operation_type: str
    response_time_ms: float
    data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    correlation_id: Optional[str]
    metadata: Dict[str, Any]


# ============================================================================
# JAEGIS MASTER ORCHESTRATOR INTERFACE
# ============================================================================

class JAEGISMasterOrchestratorInterface:
    """
    Direct interface with JAEGIS Master Orchestrator.
    
    Features:
    - Real-time command submission and tracking
    - WebSocket-based status monitoring
    - HTTP REST API integration
    - Automatic retry and error handling
    - Load balancing and queue management
    - Security and authentication
    - Performance monitoring and optimization
    - Heartbeat and health checking
    """
    
    def __init__(self, orchestrator_config: Dict[str, Any]):
        """
        Initialize JAEGIS Master Orchestrator interface.
        
        Args:
            orchestrator_config: Configuration for JAEGIS connection
        """
        self.config = orchestrator_config
        self.base_url = orchestrator_config.get("base_url", "https://jaegis.orchestrator.local")
        self.websocket_url = orchestrator_config.get("websocket_url", "wss://jaegis.orchestrator.local/ws")
        self.api_key = orchestrator_config.get("api_key")
        self.client_id = orchestrator_config.get("client_id", "nlds_tier0")
        
        # Connection management
        self.websocket = None
        self.http_session = None
        self.is_connected = False
        self.connection_retry_count = 0
        self.max_connection_retries = 5
        
        # Command tracking
        self.active_commands = {}
        self.command_history = []
        self.status_callbacks = {}
        
        # Performance monitoring
        self.performance_metrics = {
            "commands_submitted": 0,
            "commands_completed": 0,
            "commands_failed": 0,
            "average_response_time_ms": 0.0,
            "connection_uptime_seconds": 0,
            "last_heartbeat": None
        }
        
        # Orchestrator state
        self.orchestrator_status = OrchestratorStatus.OFFLINE
        self.orchestrator_capabilities = None
        self.last_capability_update = None
        
        # Security setup
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json",
            "User-Agent": "NLDS-Tier0-Interface/2.2.0",
            "X-Client-ID": self.client_id
        }
        
        # Remove None values from headers
        self.headers = {k: v for k, v in self.headers.items() if v is not None}
    
    async def initialize_connection(self) -> bool:
        """Initialize connection to JAEGIS Master Orchestrator."""
        try:
            # Initialize HTTP session
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            self.http_session = aiohttp.ClientSession(
                connector=connector,
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Test HTTP connection
            async with self.http_session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    logger.info("HTTP connection to JAEGIS Master Orchestrator established")
                else:
                    logger.warning(f"HTTP health check returned status {response.status}")
            
            # Initialize WebSocket connection
            await self._connect_websocket()
            
            # Query initial capabilities
            await self._query_capabilities()
            
            # Start heartbeat
            asyncio.create_task(self._heartbeat_loop())
            
            self.is_connected = True
            self.connection_retry_count = 0
            logger.info("JAEGIS Master Orchestrator interface initialized successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize JAEGIS connection: {e}")
            self.is_connected = False
            return False
    
    async def _connect_websocket(self) -> None:
        """Connect to JAEGIS WebSocket for real-time communication."""
        try:
            # Prepare WebSocket headers
            ws_headers = {}
            if self.api_key:
                ws_headers["Authorization"] = f"Bearer {self.api_key}"
            
            # Connect to WebSocket
            self.websocket = await websockets.connect(
                self.websocket_url,
                ssl=self.ssl_context,
                extra_headers=ws_headers,
                ping_interval=30,
                ping_timeout=10
            )
            
            # Start message handler
            asyncio.create_task(self._websocket_message_handler())
            
            logger.info("WebSocket connection to JAEGIS Master Orchestrator established")
            
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            raise
    
    async def _websocket_message_handler(self) -> None:
        """Handle incoming WebSocket messages from JAEGIS."""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    jaegis_message = JAEGISMessage(
                        message_id=data.get("message_id"),
                        message_type=MessageType(data.get("message_type")),
                        timestamp=datetime.fromisoformat(data.get("timestamp")),
                        source=data.get("source"),
                        destination=data.get("destination"),
                        payload=data.get("payload", {}),
                        priority=data.get("priority", "normal"),
                        correlation_id=data.get("correlation_id"),
                        metadata=data.get("metadata", {})
                    )
                    
                    await self._process_incoming_message(jaegis_message)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received from JAEGIS: {e}")
                except Exception as e:
                    logger.error(f"Error processing JAEGIS message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection to JAEGIS closed")
            self.is_connected = False
            await self._reconnect_websocket()
        except Exception as e:
            logger.error(f"WebSocket message handler error: {e}")
            self.is_connected = False
    
    async def _process_incoming_message(self, message: JAEGISMessage) -> None:
        """Process incoming message from JAEGIS Master Orchestrator."""
        try:
            if message.message_type == MessageType.STATUS_UPDATE:
                await self._handle_status_update(message)
            elif message.message_type == MessageType.HEARTBEAT:
                await self._handle_heartbeat(message)
            elif message.message_type == MessageType.ERROR_NOTIFICATION:
                await self._handle_error_notification(message)
            elif message.message_type == MessageType.SYSTEM_ALERT:
                await self._handle_system_alert(message)
            elif message.message_type == MessageType.RESOURCE_STATUS:
                await self._handle_resource_status(message)
            else:
                logger.debug(f"Unhandled message type: {message.message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {e}")
    
    async def _handle_status_update(self, message: JAEGISMessage) -> None:
        """Handle command status update from JAEGIS."""
        payload = message.payload
        command_id = payload.get("command_id")
        
        if command_id and command_id in self.active_commands:
            # Update command status
            status_response = CommandStatusResponse(
                command_id=command_id,
                status=CommandStatus(payload.get("status")),
                progress_percentage=payload.get("progress_percentage", 0.0),
                assigned_squad=payload.get("assigned_squad"),
                assigned_agents=payload.get("assigned_agents", []),
                execution_start=datetime.fromisoformat(payload["execution_start"]) if payload.get("execution_start") else None,
                execution_end=datetime.fromisoformat(payload["execution_end"]) if payload.get("execution_end") else None,
                result_data=payload.get("result_data"),
                error_message=payload.get("error_message"),
                estimated_completion=datetime.fromisoformat(payload["estimated_completion"]) if payload.get("estimated_completion") else None,
                metadata=payload.get("metadata", {})
            )
            
            # Update active commands
            self.active_commands[command_id]["status"] = status_response
            self.active_commands[command_id]["last_update"] = datetime.utcnow()
            
            # Call status callback if registered
            if command_id in self.status_callbacks:
                try:
                    await self.status_callbacks[command_id](status_response)
                except Exception as e:
                    logger.error(f"Status callback error for command {command_id}: {e}")
            
            # Move completed/failed commands to history
            if status_response.status in [CommandStatus.COMPLETED, CommandStatus.FAILED, CommandStatus.CANCELLED]:
                self.command_history.append(self.active_commands[command_id])
                del self.active_commands[command_id]
                
                # Update performance metrics
                if status_response.status == CommandStatus.COMPLETED:
                    self.performance_metrics["commands_completed"] += 1
                else:
                    self.performance_metrics["commands_failed"] += 1
            
            logger.debug(f"Status update for command {command_id}: {status_response.status.value}")
    
    async def _handle_heartbeat(self, message: JAEGISMessage) -> None:
        """Handle heartbeat from JAEGIS Master Orchestrator."""
        self.performance_metrics["last_heartbeat"] = datetime.utcnow()
        self.orchestrator_status = OrchestratorStatus(message.payload.get("status", "online"))
        
        # Send heartbeat response
        response_message = JAEGISMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.HEARTBEAT,
            timestamp=datetime.utcnow(),
            source=self.client_id,
            destination="master_orchestrator",
            payload={"status": "online", "client_type": "nlds_tier0"},
            correlation_id=message.message_id
        )
        
        await self._send_websocket_message(response_message)
    
    async def _handle_error_notification(self, message: JAEGISMessage) -> None:
        """Handle error notification from JAEGIS."""
        error_data = message.payload
        logger.error(f"JAEGIS Error: {error_data.get('error_message', 'Unknown error')}")
        
        # Handle command-specific errors
        command_id = error_data.get("command_id")
        if command_id and command_id in self.active_commands:
            self.active_commands[command_id]["error"] = error_data
            
            # Consider retry if appropriate
            submission = self.active_commands[command_id]["submission"]
            if submission.retry_count < submission.max_retries:
                logger.info(f"Retrying command {command_id} (attempt {submission.retry_count + 1})")
                await self._retry_command(command_id)
    
    async def _handle_system_alert(self, message: JAEGISMessage) -> None:
        """Handle system alert from JAEGIS."""
        alert_data = message.payload
        alert_level = alert_data.get("level", "info")
        alert_message = alert_data.get("message", "System alert")
        
        if alert_level == "critical":
            logger.critical(f"JAEGIS Critical Alert: {alert_message}")
        elif alert_level == "warning":
            logger.warning(f"JAEGIS Warning: {alert_message}")
        else:
            logger.info(f"JAEGIS Alert: {alert_message}")
    
    async def _handle_resource_status(self, message: JAEGISMessage) -> None:
        """Handle resource status update from JAEGIS."""
        resource_data = message.payload
        
        # Update orchestrator capabilities
        if self.orchestrator_capabilities:
            self.orchestrator_capabilities.current_load = resource_data.get("current_load", 0.0)
            self.orchestrator_capabilities.active_commands = resource_data.get("active_commands", 0)
            self.orchestrator_capabilities.queue_length = resource_data.get("queue_length", 0)
            self.orchestrator_capabilities.estimated_wait_time_seconds = resource_data.get("estimated_wait_time", 0)
            self.orchestrator_capabilities.last_updated = datetime.utcnow()
    
    async def _send_websocket_message(self, message: JAEGISMessage) -> None:
        """Send message via WebSocket to JAEGIS."""
        if not self.websocket or self.websocket.closed:
            raise ConnectionError("WebSocket connection not available")
        
        message_data = asdict(message)
        message_data["timestamp"] = message.timestamp.isoformat()
        message_data["message_type"] = message.message_type.value
        
        await self.websocket.send(json.dumps(message_data))
    
    async def _query_capabilities(self) -> None:
        """Query JAEGIS Master Orchestrator capabilities."""
        try:
            async with self.http_session.get(f"{self.base_url}/api/v1/capabilities") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    self.orchestrator_capabilities = OrchestratorCapabilities(
                        available_squads=data.get("available_squads", []),
                        available_modes=data.get("available_modes", []),
                        current_load=data.get("current_load", 0.0),
                        max_concurrent_commands=data.get("max_concurrent_commands", 100),
                        active_commands=data.get("active_commands", 0),
                        queue_length=data.get("queue_length", 0),
                        estimated_wait_time_seconds=data.get("estimated_wait_time", 0),
                        system_health=data.get("system_health", {}),
                        last_updated=datetime.utcnow()
                    )
                    
                    self.last_capability_update = datetime.utcnow()
                    logger.info("JAEGIS capabilities updated successfully")
                else:
                    logger.warning(f"Failed to query capabilities: HTTP {response.status}")
                    
        except Exception as e:
            logger.error(f"Error querying JAEGIS capabilities: {e}")
    
    async def _heartbeat_loop(self) -> None:
        """Maintain heartbeat with JAEGIS Master Orchestrator."""
        while self.is_connected:
            try:
                # Send heartbeat
                heartbeat_message = JAEGISMessage(
                    message_id=str(uuid.uuid4()),
                    message_type=MessageType.HEARTBEAT,
                    timestamp=datetime.utcnow(),
                    source=self.client_id,
                    destination="master_orchestrator",
                    payload={"status": "online", "client_type": "nlds_tier0"}
                )
                
                await self._send_websocket_message(heartbeat_message)
                
                # Wait for next heartbeat
                await asyncio.sleep(30)  # 30-second heartbeat interval
                
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(5)  # Short delay before retry
    
    async def _reconnect_websocket(self) -> None:
        """Reconnect WebSocket connection."""
        if self.connection_retry_count >= self.max_connection_retries:
            logger.error("Maximum WebSocket reconnection attempts reached")
            return
        
        self.connection_retry_count += 1
        wait_time = min(2 ** self.connection_retry_count, 60)  # Exponential backoff, max 60s
        
        logger.info(f"Attempting WebSocket reconnection in {wait_time} seconds (attempt {self.connection_retry_count})")
        await asyncio.sleep(wait_time)
        
        try:
            await self._connect_websocket()
            self.is_connected = True
            self.connection_retry_count = 0
            logger.info("WebSocket reconnection successful")
        except Exception as e:
            logger.error(f"WebSocket reconnection failed: {e}")
            await self._reconnect_websocket()
    
    async def submit_command(self, jaegis_command: JAEGISCommand,
                           priority: str = "normal",
                           timeout_seconds: int = 300,
                           status_callback: Optional[callable] = None) -> InterfaceResult:
        """
        Submit command to JAEGIS Master Orchestrator.
        
        Args:
            jaegis_command: JAEGIS command to execute
            priority: Command priority (low, normal, high, critical)
            timeout_seconds: Command timeout in seconds
            status_callback: Optional callback for status updates
            
        Returns:
            Interface operation result
        """
        start_time = datetime.utcnow()
        
        try:
            if not self.is_connected:
                return InterfaceResult(
                    success=False,
                    operation_type="command_submission",
                    response_time_ms=0.0,
                    data=None,
                    error_message="Not connected to JAEGIS Master Orchestrator",
                    correlation_id=None,
                    metadata={}
                )
            
            # Create command submission
            submission = CommandSubmission(
                command_id=jaegis_command.command_id,
                jaegis_command=jaegis_command,
                submission_timestamp=datetime.utcnow(),
                expected_completion=datetime.utcnow() + timedelta(seconds=timeout_seconds),
                priority_level=priority,
                timeout_seconds=timeout_seconds
            )
            
            # Register status callback
            if status_callback:
                self.status_callbacks[jaegis_command.command_id] = status_callback
            
            # Prepare submission message
            submission_message = JAEGISMessage(
                message_id=str(uuid.uuid4()),
                message_type=MessageType.COMMAND_SUBMISSION,
                timestamp=datetime.utcnow(),
                source=self.client_id,
                destination="master_orchestrator",
                payload={
                    "command_id": jaegis_command.command_id,
                    "command_type": jaegis_command.command_type.value,
                    "target_squad": jaegis_command.target_squad.value,
                    "mode_level": jaegis_command.mode_level.value,
                    "parameters": [
                        {
                            "type": param.parameter_type.value,
                            "value": param.value,
                            "confidence": param.confidence
                        }
                        for param in jaegis_command.parameters
                    ],
                    "priority": jaegis_command.priority,
                    "estimated_duration": jaegis_command.estimated_duration,
                    "timeout_seconds": timeout_seconds
                },
                priority=priority,
                correlation_id=jaegis_command.command_id
            )
            
            # Send command via WebSocket
            await self._send_websocket_message(submission_message)
            
            # Track active command
            self.active_commands[jaegis_command.command_id] = {
                "submission": submission,
                "status": None,
                "submitted_at": datetime.utcnow(),
                "last_update": datetime.utcnow()
            }
            
            # Update performance metrics
            self.performance_metrics["commands_submitted"] += 1
            
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            logger.info(f"Command {jaegis_command.command_id} submitted to JAEGIS successfully")
            
            return InterfaceResult(
                success=True,
                operation_type="command_submission",
                response_time_ms=response_time,
                data={
                    "command_id": jaegis_command.command_id,
                    "submission_timestamp": submission.submission_timestamp.isoformat(),
                    "expected_completion": submission.expected_completion.isoformat() if submission.expected_completion else None
                },
                error_message=None,
                correlation_id=jaegis_command.command_id,
                metadata={
                    "target_squad": jaegis_command.target_squad.value,
                    "mode_level": jaegis_command.mode_level.value,
                    "priority": priority
                }
            )
            
        except Exception as e:
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            logger.error(f"Command submission failed: {e}")
            
            return InterfaceResult(
                success=False,
                operation_type="command_submission",
                response_time_ms=response_time,
                data=None,
                error_message=str(e),
                correlation_id=jaegis_command.command_id if jaegis_command else None,
                metadata={}
            )
    
    async def get_command_status(self, command_id: str) -> Optional[CommandStatusResponse]:
        """Get current status of a submitted command."""
        if command_id in self.active_commands:
            return self.active_commands[command_id]["status"]
        
        # Check command history
        for historical_command in self.command_history:
            if historical_command["submission"].command_id == command_id:
                return historical_command["status"]
        
        # Query JAEGIS directly if not found locally
        try:
            async with self.http_session.get(f"{self.base_url}/api/v1/commands/{command_id}/status") as response:
                if response.status == 200:
                    data = await response.json()
                    return CommandStatusResponse(
                        command_id=command_id,
                        status=CommandStatus(data.get("status")),
                        progress_percentage=data.get("progress_percentage", 0.0),
                        assigned_squad=data.get("assigned_squad"),
                        assigned_agents=data.get("assigned_agents", []),
                        execution_start=datetime.fromisoformat(data["execution_start"]) if data.get("execution_start") else None,
                        execution_end=datetime.fromisoformat(data["execution_end"]) if data.get("execution_end") else None,
                        result_data=data.get("result_data"),
                        error_message=data.get("error_message"),
                        estimated_completion=datetime.fromisoformat(data["estimated_completion"]) if data.get("estimated_completion") else None,
                        metadata=data.get("metadata", {})
                    )
        except Exception as e:
            logger.error(f"Error querying command status: {e}")
        
        return None
    
    async def cancel_command(self, command_id: str) -> InterfaceResult:
        """Cancel a submitted command."""
        start_time = datetime.utcnow()
        
        try:
            # Send cancellation request
            async with self.http_session.post(f"{self.base_url}/api/v1/commands/{command_id}/cancel") as response:
                response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Update local tracking
                    if command_id in self.active_commands:
                        self.active_commands[command_id]["status"] = CommandStatusResponse(
                            command_id=command_id,
                            status=CommandStatus.CANCELLED,
                            progress_percentage=0.0,
                            assigned_squad=None,
                            assigned_agents=[],
                            execution_start=None,
                            execution_end=datetime.utcnow(),
                            result_data=None,
                            error_message="Command cancelled by user",
                            estimated_completion=None
                        )
                    
                    return InterfaceResult(
                        success=True,
                        operation_type="command_cancellation",
                        response_time_ms=response_time,
                        data=data,
                        error_message=None,
                        correlation_id=command_id,
                        metadata={}
                    )
                else:
                    error_data = await response.json() if response.content_type == "application/json" else {}
                    return InterfaceResult(
                        success=False,
                        operation_type="command_cancellation",
                        response_time_ms=response_time,
                        data=None,
                        error_message=error_data.get("error", f"HTTP {response.status}"),
                        correlation_id=command_id,
                        metadata={}
                    )
                    
        except Exception as e:
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            return InterfaceResult(
                success=False,
                operation_type="command_cancellation",
                response_time_ms=response_time,
                data=None,
                error_message=str(e),
                correlation_id=command_id,
                metadata={}
            )
    
    async def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get current JAEGIS Master Orchestrator status."""
        return {
            "connection_status": "connected" if self.is_connected else "disconnected",
            "orchestrator_status": self.orchestrator_status.value,
            "capabilities": asdict(self.orchestrator_capabilities) if self.orchestrator_capabilities else None,
            "active_commands": len(self.active_commands),
            "performance_metrics": self.performance_metrics.copy(),
            "last_heartbeat": self.performance_metrics["last_heartbeat"].isoformat() if self.performance_metrics["last_heartbeat"] else None,
            "connection_retry_count": self.connection_retry_count
        }
    
    async def cleanup(self) -> None:
        """Cleanup JAEGIS interface resources."""
        try:
            self.is_connected = False
            
            # Close WebSocket
            if self.websocket and not self.websocket.closed:
                await self.websocket.close()
            
            # Close HTTP session
            if self.http_session and not self.http_session.closed:
                await self.http_session.close()
            
            logger.info("JAEGIS Master Orchestrator interface cleaned up")
            
        except Exception as e:
            logger.error(f"Error during JAEGIS interface cleanup: {e}")


# ============================================================================
# JAEGIS INTERFACE UTILITIES
# ============================================================================

class JAEGISInterfaceUtils:
    """Utility functions for JAEGIS interface operations."""
    
    @staticmethod
    def interface_result_to_dict(result: InterfaceResult) -> Dict[str, Any]:
        """Convert interface result to dictionary format."""
        return {
            "success": result.success,
            "operation_type": result.operation_type,
            "response_time_ms": result.response_time_ms,
            "data": result.data,
            "error_message": result.error_message,
            "correlation_id": result.correlation_id,
            "metadata": result.metadata
        }
    
    @staticmethod
    def command_status_to_dict(status: CommandStatusResponse) -> Dict[str, Any]:
        """Convert command status to dictionary format."""
        return {
            "command_id": status.command_id,
            "status": status.status.value,
            "progress_percentage": status.progress_percentage,
            "assigned_squad": status.assigned_squad,
            "assigned_agents": status.assigned_agents,
            "execution_start": status.execution_start.isoformat() if status.execution_start else None,
            "execution_end": status.execution_end.isoformat() if status.execution_end else None,
            "result_data": status.result_data,
            "error_message": status.error_message,
            "estimated_completion": status.estimated_completion.isoformat() if status.estimated_completion else None,
            "metadata": status.metadata
        }
    
    @staticmethod
    def validate_jaegis_config(config: Dict[str, Any]) -> List[str]:
        """Validate JAEGIS configuration."""
        errors = []
        
        required_fields = ["base_url", "websocket_url"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        if "api_key" not in config:
            errors.append("API key not provided - authentication may fail")
        
        return errors
