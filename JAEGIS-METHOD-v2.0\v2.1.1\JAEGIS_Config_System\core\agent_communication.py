"""
JAEGIS Configuration Management System - Agent Communication Framework
Handles communication between configuration agents and existing JAEGIS agents
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Types of messages in the agent communication system"""
    CONFIG_UPDATE = "config_update"
    CONFIG_REQUEST = "config_request"
    AGENT_STATUS = "agent_status"
    PARAMETER_CHANGE = "parameter_change"
    PROTOCOL_UPDATE = "protocol_update"
    PERFORMANCE_METRIC = "performance_metric"
    HEARTBEAT = "heartbeat"
    ERROR = "error"

class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class AgentMessage:
    """Message structure for agent communication"""
    message_id: str
    sender_id: str
    recipient_id: str
    message_type: MessageType
    priority: MessagePriority
    payload: Dict[str, Any]
    timestamp: datetime
    expires_at: Optional[datetime] = None
    requires_response: bool = False
    correlation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "requires_response": self.requires_response,
            "correlation_id": self.correlation_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        """Create message from dictionary"""
        return cls(
            message_id=data["message_id"],
            sender_id=data["sender_id"],
            recipient_id=data["recipient_id"],
            message_type=MessageType(data["message_type"]),
            priority=MessagePriority(data["priority"]),
            payload=data["payload"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            requires_response=data.get("requires_response", False),
            correlation_id=data.get("correlation_id")
        )

@dataclass
class AgentInfo:
    """Information about a registered agent"""
    agent_id: str
    agent_name: str
    agent_type: str
    tier: str
    capabilities: List[str]
    status: str = "active"
    last_heartbeat: Optional[datetime] = None
    configuration: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "tier": self.tier,
            "capabilities": self.capabilities,
            "status": self.status,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "configuration": self.configuration or {}
        }

class AgentCommunicationHub:
    """Central hub for agent communication"""
    
    def __init__(self):
        self.registered_agents: Dict[str, AgentInfo] = {}
        self.message_handlers: Dict[MessageType, List[Callable]] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.response_handlers: Dict[str, Callable] = {}
        
        # Performance tracking
        self.message_stats: Dict[str, int] = {
            "sent": 0,
            "received": 0,
            "failed": 0,
            "expired": 0
        }
        
        # Initialize default handlers
        self._setup_default_handlers()
        
        logger.info("Agent communication hub initialized")
    
    def _setup_default_handlers(self):
        """Setup default message handlers"""
        self.register_handler(MessageType.HEARTBEAT, self._handle_heartbeat)
        self.register_handler(MessageType.AGENT_STATUS, self._handle_agent_status)
        self.register_handler(MessageType.ERROR, self._handle_error)
    
    def register_agent(self, agent_info: AgentInfo) -> bool:
        """Register an agent with the communication hub"""
        try:
            self.registered_agents[agent_info.agent_id] = agent_info
            logger.info(f"Registered agent: {agent_info.agent_name} ({agent_info.agent_id})")
            
            # Send welcome message
            welcome_message = AgentMessage(
                message_id=str(uuid.uuid4()),
                sender_id="communication_hub",
                recipient_id=agent_info.agent_id,
                message_type=MessageType.CONFIG_REQUEST,
                priority=MessagePriority.NORMAL,
                payload={"action": "welcome", "hub_status": "active"},
                timestamp=datetime.now()
            )
            
            asyncio.create_task(self.send_message(welcome_message))
            return True
            
        except Exception as e:
            logger.error(f"Failed to register agent {agent_info.agent_id}: {e}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent"""
        if agent_id in self.registered_agents:
            agent_info = self.registered_agents.pop(agent_id)
            logger.info(f"Unregistered agent: {agent_info.agent_name}")
            return True
        return False
    
    def get_agent_info(self, agent_id: str) -> Optional[AgentInfo]:
        """Get information about a registered agent"""
        return self.registered_agents.get(agent_id)
    
    def get_all_agents(self) -> List[AgentInfo]:
        """Get information about all registered agents"""
        return list(self.registered_agents.values())
    
    def get_agents_by_tier(self, tier: str) -> List[AgentInfo]:
        """Get agents by tier"""
        return [agent for agent in self.registered_agents.values() if agent.tier == tier]
    
    def register_handler(self, message_type: MessageType, handler: Callable[[AgentMessage], None]):
        """Register a message handler"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
        logger.debug(f"Registered handler for {message_type.value}")
    
    def unregister_handler(self, message_type: MessageType, handler: Callable):
        """Unregister a message handler"""
        if message_type in self.message_handlers:
            if handler in self.message_handlers[message_type]:
                self.message_handlers[message_type].remove(handler)
    
    async def send_message(self, message: AgentMessage) -> bool:
        """Send a message to an agent"""
        try:
            # Validate recipient
            if message.recipient_id not in self.registered_agents and message.recipient_id != "broadcast":
                logger.error(f"Unknown recipient: {message.recipient_id}")
                self.message_stats["failed"] += 1
                return False
            
            # Check if message has expired
            if message.expires_at and datetime.now() > message.expires_at:
                logger.warning(f"Message expired: {message.message_id}")
                self.message_stats["expired"] += 1
                return False
            
            # Add to queue for processing
            await self.message_queue.put(message)
            self.message_stats["sent"] += 1
            
            logger.debug(f"Queued message {message.message_id} for {message.recipient_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self.message_stats["failed"] += 1
            return False
    
    async def broadcast_message(self, message: AgentMessage) -> int:
        """Broadcast a message to all registered agents"""
        sent_count = 0
        
        for agent_id in self.registered_agents.keys():
            # Create a copy of the message for each recipient
            broadcast_message = AgentMessage(
                message_id=str(uuid.uuid4()),
                sender_id=message.sender_id,
                recipient_id=agent_id,
                message_type=message.message_type,
                priority=message.priority,
                payload=message.payload.copy(),
                timestamp=message.timestamp,
                expires_at=message.expires_at,
                requires_response=message.requires_response,
                correlation_id=message.correlation_id
            )
            
            if await self.send_message(broadcast_message):
                sent_count += 1
        
        logger.info(f"Broadcast message to {sent_count} agents")
        return sent_count
    
    async def send_configuration_update(self, config_data: Dict[str, Any], target_agents: Optional[List[str]] = None) -> bool:
        """Send configuration update to agents"""
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id="configuration_engine",
            recipient_id="broadcast" if not target_agents else "",
            message_type=MessageType.CONFIG_UPDATE,
            priority=MessagePriority.HIGH,
            payload={
                "action": "config_update",
                "configuration": config_data,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now(),
            requires_response=True
        )
        
        if target_agents:
            # Send to specific agents
            success_count = 0
            for agent_id in target_agents:
                message.recipient_id = agent_id
                message.message_id = str(uuid.uuid4())  # New ID for each message
                if await self.send_message(message):
                    success_count += 1
            
            logger.info(f"Sent configuration update to {success_count}/{len(target_agents)} agents")
            return success_count == len(target_agents)
        else:
            # Broadcast to all agents
            sent_count = await self.broadcast_message(message)
            logger.info(f"Broadcast configuration update to {sent_count} agents")
            return sent_count > 0
    
    async def request_agent_status(self, agent_id: str) -> bool:
        """Request status from a specific agent"""
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id="communication_hub",
            recipient_id=agent_id,
            message_type=MessageType.AGENT_STATUS,
            priority=MessagePriority.NORMAL,
            payload={"action": "status_request"},
            timestamp=datetime.now(),
            requires_response=True
        )
        
        return await self.send_message(message)
    
    async def process_messages(self):
        """Process messages from the queue"""
        while True:
            try:
                # Get message from queue
                message = await self.message_queue.get()
                
                # Handle the message
                await self._handle_message(message)
                
                # Mark task as done
                self.message_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    async def _handle_message(self, message: AgentMessage):
        """Handle a received message"""
        try:
            self.message_stats["received"] += 1
            
            # Call registered handlers
            if message.message_type in self.message_handlers:
                for handler in self.message_handlers[message.message_type]:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(message)
                        else:
                            handler(message)
                    except Exception as e:
                        logger.error(f"Error in message handler: {e}")
            
            # Handle response requirements
            if message.requires_response and message.correlation_id:
                if message.correlation_id in self.response_handlers:
                    handler = self.response_handlers[message.correlation_id]
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(message)
                        else:
                            handler(message)
                    except Exception as e:
                        logger.error(f"Error in response handler: {e}")
                    finally:
                        # Remove the response handler
                        del self.response_handlers[message.correlation_id]
            
            logger.debug(f"Processed message {message.message_id}")
            
        except Exception as e:
            logger.error(f"Failed to handle message {message.message_id}: {e}")
    
    async def _handle_heartbeat(self, message: AgentMessage):
        """Handle heartbeat messages"""
        agent_id = message.sender_id
        if agent_id in self.registered_agents:
            self.registered_agents[agent_id].last_heartbeat = datetime.now()
            self.registered_agents[agent_id].status = "active"
            logger.debug(f"Received heartbeat from {agent_id}")
    
    async def _handle_agent_status(self, message: AgentMessage):
        """Handle agent status messages"""
        agent_id = message.sender_id
        if agent_id in self.registered_agents:
            status_data = message.payload.get("status", {})
            
            # Update agent status
            if "status" in status_data:
                self.registered_agents[agent_id].status = status_data["status"]
            
            # Update configuration if provided
            if "configuration" in status_data:
                self.registered_agents[agent_id].configuration = status_data["configuration"]
            
            logger.info(f"Updated status for agent {agent_id}")
    
    async def _handle_error(self, message: AgentMessage):
        """Handle error messages"""
        error_data = message.payload
        logger.error(f"Agent error from {message.sender_id}: {error_data}")
    
    def get_communication_statistics(self) -> Dict[str, Any]:
        """Get communication statistics"""
        active_agents = len([a for a in self.registered_agents.values() if a.status == "active"])
        
        return {
            "total_agents": len(self.registered_agents),
            "active_agents": active_agents,
            "message_stats": self.message_stats.copy(),
            "queue_size": self.message_queue.qsize(),
            "handler_count": sum(len(handlers) for handlers in self.message_handlers.values())
        }
    
    async def cleanup_expired_messages(self):
        """Clean up expired messages and inactive agents"""
        current_time = datetime.now()
        
        # Mark agents as inactive if no heartbeat for 5 minutes
        for agent in self.registered_agents.values():
            if (agent.last_heartbeat and 
                (current_time - agent.last_heartbeat).total_seconds() > 300):
                agent.status = "inactive"
        
        logger.debug("Cleaned up expired messages and inactive agents")

class ConfigurationBroadcaster:
    """Specialized class for broadcasting configuration changes"""
    
    def __init__(self, communication_hub: AgentCommunicationHub):
        self.hub = communication_hub
        self.pending_updates: Dict[str, Dict[str, Any]] = {}
        
    async def broadcast_frequency_change(self, parameter_name: str, new_value: Any, old_value: Any):
        """Broadcast frequency parameter changes"""
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id="frequency_controller",
            recipient_id="broadcast",
            message_type=MessageType.PARAMETER_CHANGE,
            priority=MessagePriority.HIGH,
            payload={
                "parameter_type": "frequency",
                "parameter_name": parameter_name,
                "new_value": new_value,
                "old_value": old_value,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
        
        await self.hub.broadcast_message(message)
        logger.info(f"Broadcast frequency change: {parameter_name} = {new_value}")
    
    async def broadcast_protocol_change(self, protocol_id: str, action: str, protocol_data: Dict[str, Any]):
        """Broadcast protocol changes"""
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id="protocol_manager",
            recipient_id="broadcast",
            message_type=MessageType.PROTOCOL_UPDATE,
            priority=MessagePriority.HIGH,
            payload={
                "protocol_id": protocol_id,
                "action": action,  # "added", "updated", "removed"
                "protocol_data": protocol_data,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
        
        await self.hub.broadcast_message(message)
        logger.info(f"Broadcast protocol change: {action} {protocol_id}")
    
    async def broadcast_agent_config_change(self, agent_id: str, config_data: Dict[str, Any]):
        """Broadcast agent configuration changes"""
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id="configuration_engine",
            recipient_id=agent_id,
            message_type=MessageType.CONFIG_UPDATE,
            priority=MessagePriority.HIGH,
            payload={
                "action": "agent_config_update",
                "agent_id": agent_id,
                "configuration": config_data,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now(),
            requires_response=True
        )
        
        await self.hub.send_message(message)
        logger.info(f"Sent configuration update to agent {agent_id}")

# Global communication hub instance
_communication_hub: Optional[AgentCommunicationHub] = None

def get_communication_hub() -> AgentCommunicationHub:
    """Get the global communication hub instance"""
    global _communication_hub
    if _communication_hub is None:
        _communication_hub = AgentCommunicationHub()
    return _communication_hub

def initialize_communication_system():
    """Initialize the communication system"""
    hub = get_communication_hub()
    
    # Start message processing
    asyncio.create_task(hub.process_messages())
    
    # Start cleanup task
    async def cleanup_task():
        while True:
            await asyncio.sleep(300)  # Clean up every 5 minutes
            await hub.cleanup_expired_messages()
    
    asyncio.create_task(cleanup_task())
    
    logger.info("Communication system initialized")
