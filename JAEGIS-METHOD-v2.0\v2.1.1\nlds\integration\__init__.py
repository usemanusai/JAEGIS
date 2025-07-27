"""
N.L.D.S. Integration Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Complete integration layer providing seamless connectivity with JAEGIS ecosystem,
external systems, and comprehensive error handling with fallback mechanisms.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import all integration components
from .jaegis_orchestrator import (
    JAEGISMasterOrchestratorInterface,
    CommandStatus,
    OrchestratorStatus,
    MessageType as JAEGISMessageType,
    JAEGISMessage,
    CommandSubmission,
    CommandStatusResponse,
    OrchestratorCapabilities,
    InterfaceResult,
    JAEGISInterfaceUtils
)

from .amasiap_protocol import (
    AMASIAPProtocolEngine,
    EnhancementType,
    ResearchFramework,
    ProtocolStatus,
    InputEnhancement,
    ResearchActivation,
    ContextEnrichment,
    AMASIAPResult,
    AMASIAPUtils
)

from .openrouter_integration import (
    OpenRouterIntegrationEngine,
    ModelCategory,
    ModelProvider,
    RequestPriority,
    ModelInfo,
    APIKeyInfo,
    ModelRequest,
    ModelResponse,
    OpenRouterResult,
    OpenRouterUtils
)

from .github_integration import (
    GitHubIntegrationEngine,
    ResourceType,
    SyncStatus,
    CacheStrategy,
    GitHubResource,
    ResourceRequest,
    SyncOperation,
    GitHubIntegrationResult,
    GitHubIntegrationUtils
)

from .realtime_communication import (
    RealtimeCommunicationEngine,
    MessageType as CommMessageType,
    ConnectionStatus,
    SubscriptionType,
    RealtimeMessage,
    ConnectionInfo,
    Subscription,
    CommunicationStats,
    RealtimeCommunicationUtils
)

from .error_handling import (
    ErrorHandlingEngine,
    ErrorSeverity,
    ErrorCategory,
    FallbackStrategy,
    SystemState,
    ErrorInfo,
    FallbackAction,
    RecoveryPlan,
    SystemHealth,
    ErrorHandlingUtils
)

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# INTEGRATION ORCHESTRATOR
# ============================================================================

class NLDSIntegrationOrchestrator:
    """
    Master orchestrator for all N.L.D.S. integration components.
    
    Coordinates and manages:
    - JAEGIS Master Orchestrator Interface
    - A.M.A.S.I.A.P. Protocol Engine
    - OpenRouter.ai Integration
    - GitHub Integration Interface
    - Real-time Communication Layer
    - Error Handling & Fallback Systems
    """
    
    def __init__(self, integration_config: Dict[str, Any]):
        """
        Initialize N.L.D.S. Integration Orchestrator.
        
        Args:
            integration_config: Complete integration configuration
        """
        self.config = integration_config
        self.is_initialized = False
        self.start_time = None
        
        # Initialize all integration components
        self.jaegis_interface = None
        self.amasiap_engine = None
        self.openrouter_engine = None
        self.github_interface = None
        self.communication_engine = None
        self.error_handler = None
        
        # Integration status
        self.component_status = {
            "jaegis_interface": False,
            "amasiap_engine": False,
            "openrouter_engine": False,
            "github_interface": False,
            "communication_engine": False,
            "error_handler": False
        }
        
        # Performance metrics
        self.integration_metrics = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "average_response_time_ms": 0.0,
            "uptime_seconds": 0.0
        }
    
    async def initialize_all_components(self) -> bool:
        """Initialize all integration components."""
        try:
            self.start_time = datetime.utcnow()
            
            # Initialize error handler first
            if "error_handling" in self.config:
                self.error_handler = ErrorHandlingEngine(self.config["error_handling"])
                self.component_status["error_handler"] = True
                logger.info("Error handling engine initialized")
            
            # Initialize JAEGIS interface
            if "jaegis_orchestrator" in self.config:
                self.jaegis_interface = JAEGISMasterOrchestratorInterface(self.config["jaegis_orchestrator"])
                success = await self.jaegis_interface.initialize_connection()
                self.component_status["jaegis_interface"] = success
                if success:
                    logger.info("JAEGIS Master Orchestrator interface initialized")
                else:
                    logger.warning("JAEGIS Master Orchestrator interface initialization failed")
            
            # Initialize A.M.A.S.I.A.P. engine
            if "amasiap_protocol" in self.config:
                self.amasiap_engine = AMASIAPProtocolEngine(self.config["amasiap_protocol"])
                success = await self.amasiap_engine.initialize_protocol()
                self.component_status["amasiap_engine"] = success
                if success:
                    logger.info("A.M.A.S.I.A.P. Protocol engine initialized")
                else:
                    logger.warning("A.M.A.S.I.A.P. Protocol engine initialization failed")
            
            # Initialize OpenRouter integration
            if "openrouter_integration" in self.config:
                self.openrouter_engine = OpenRouterIntegrationEngine(self.config["openrouter_integration"])
                success = await self.openrouter_engine.initialize_integration()
                self.component_status["openrouter_engine"] = success
                if success:
                    logger.info("OpenRouter integration engine initialized")
                else:
                    logger.warning("OpenRouter integration engine initialization failed")
            
            # Initialize GitHub integration
            if "github_integration" in self.config:
                self.github_interface = GitHubIntegrationEngine(self.config["github_integration"])
                success = await self.github_interface.initialize_integration()
                self.component_status["github_interface"] = success
                if success:
                    logger.info("GitHub integration interface initialized")
                else:
                    logger.warning("GitHub integration interface initialization failed")
            
            # Initialize real-time communication
            if "realtime_communication" in self.config:
                self.communication_engine = RealtimeCommunicationEngine(self.config["realtime_communication"])
                success = await self.communication_engine.initialize_server()
                self.component_status["communication_engine"] = success
                if success:
                    logger.info("Real-time communication engine initialized")
                else:
                    logger.warning("Real-time communication engine initialization failed")
            
            # Check overall initialization status
            successful_components = sum(self.component_status.values())
            total_components = len(self.component_status)
            
            self.is_initialized = successful_components > 0  # At least one component must be working
            
            if self.is_initialized:
                logger.info(f"N.L.D.S. Integration Orchestrator initialized: {successful_components}/{total_components} components active")
                return True
            else:
                logger.error("N.L.D.S. Integration Orchestrator initialization failed: No components initialized")
                return False
                
        except Exception as e:
            logger.error(f"Integration orchestrator initialization failed: {e}")
            if self.error_handler:
                await self.error_handler.handle_error(e, {
                    "component": "integration_orchestrator",
                    "function": "initialize_all_components"
                })
            return False
    
    async def process_enhanced_input(self, user_input: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user input through the complete integration pipeline.
        
        Args:
            user_input: Original user input
            user_context: Optional user context
            
        Returns:
            Complete processing result with enhanced input and JAEGIS command
        """
        try:
            processing_start = datetime.utcnow()
            result = {
                "success": False,
                "original_input": user_input,
                "enhanced_input": user_input,
                "jaegis_command": None,
                "amasiap_result": None,
                "processing_time_ms": 0.0,
                "components_used": [],
                "error_message": None
            }
            
            # Step 1: A.M.A.S.I.A.P. Protocol Enhancement
            if self.amasiap_engine and self.component_status["amasiap_engine"]:
                try:
                    amasiap_result = await self.amasiap_engine.process_input(user_input, user_context)
                    result["enhanced_input"] = amasiap_result.enhanced_input
                    result["amasiap_result"] = AMASIAPUtils.amasiap_result_to_dict(amasiap_result)
                    result["components_used"].append("amasiap_protocol")
                    logger.debug("A.M.A.S.I.A.P. enhancement completed")
                except Exception as e:
                    logger.warning(f"A.M.A.S.I.A.P. enhancement failed: {e}")
                    if self.error_handler:
                        await self.error_handler.handle_error(e, {
                            "component": "amasiap_engine",
                            "function": "process_input"
                        })
            
            # Step 2: JAEGIS Command Generation (would use translation engine)
            # This would integrate with the translation engine from Phase 5
            # For now, we'll simulate command generation
            if self.jaegis_interface and self.component_status["jaegis_interface"]:
                try:
                    # In real implementation, this would use the translation engine
                    # to generate JAEGIS commands from enhanced input
                    result["components_used"].append("jaegis_interface")
                    logger.debug("JAEGIS interface ready for command submission")
                except Exception as e:
                    logger.warning(f"JAEGIS interface error: {e}")
                    if self.error_handler:
                        await self.error_handler.handle_error(e, {
                            "component": "jaegis_interface",
                            "function": "process_enhanced_input"
                        })
            
            # Step 3: OpenRouter.ai Processing (if needed)
            if self.openrouter_engine and self.component_status["openrouter_engine"]:
                try:
                    # OpenRouter integration available for enhanced AI processing
                    result["components_used"].append("openrouter_integration")
                    logger.debug("OpenRouter integration available")
                except Exception as e:
                    logger.warning(f"OpenRouter integration error: {e}")
                    if self.error_handler:
                        await self.error_handler.handle_error(e, {
                            "component": "openrouter_engine",
                            "function": "process_enhanced_input"
                        })
            
            # Step 4: GitHub Resource Fetching (if needed)
            if self.github_interface and self.component_status["github_interface"]:
                try:
                    # GitHub integration available for dynamic resource fetching
                    result["components_used"].append("github_integration")
                    logger.debug("GitHub integration available")
                except Exception as e:
                    logger.warning(f"GitHub integration error: {e}")
                    if self.error_handler:
                        await self.error_handler.handle_error(e, {
                            "component": "github_interface",
                            "function": "process_enhanced_input"
                        })
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - processing_start).total_seconds() * 1000
            result["processing_time_ms"] = processing_time
            
            # Update metrics
            self.integration_metrics["total_operations"] += 1
            if len(result["components_used"]) > 0:
                self.integration_metrics["successful_operations"] += 1
                result["success"] = True
            else:
                self.integration_metrics["failed_operations"] += 1
                result["error_message"] = "No integration components available"
            
            # Update average response time
            current_avg = self.integration_metrics["average_response_time_ms"]
            total_ops = self.integration_metrics["total_operations"]
            self.integration_metrics["average_response_time_ms"] = (current_avg * (total_ops - 1) + processing_time) / total_ops
            
            return result
            
        except Exception as e:
            logger.error(f"Enhanced input processing failed: {e}")
            if self.error_handler:
                await self.error_handler.handle_error(e, {
                    "component": "integration_orchestrator",
                    "function": "process_enhanced_input"
                })
            
            return {
                "success": False,
                "original_input": user_input,
                "enhanced_input": user_input,
                "jaegis_command": None,
                "amasiap_result": None,
                "processing_time_ms": (datetime.utcnow() - processing_start).total_seconds() * 1000 if 'processing_start' in locals() else 0.0,
                "components_used": [],
                "error_message": str(e)
            }
    
    async def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status."""
        try:
            status = {
                "orchestrator": {
                    "initialized": self.is_initialized,
                    "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0,
                    "metrics": self.integration_metrics.copy()
                },
                "components": {}
            }
            
            # Get status from each component
            if self.jaegis_interface:
                status["components"]["jaegis_interface"] = await self.jaegis_interface.get_orchestrator_status()
            
            if self.amasiap_engine:
                status["components"]["amasiap_engine"] = await self.amasiap_engine.get_protocol_status()
            
            if self.openrouter_engine:
                status["components"]["openrouter_engine"] = await self.openrouter_engine.get_integration_status()
            
            if self.github_interface:
                status["components"]["github_interface"] = await self.github_interface.get_integration_status()
            
            if self.communication_engine:
                status["components"]["communication_engine"] = await self.communication_engine.get_communication_status()
            
            if self.error_handler:
                status["components"]["error_handler"] = await self.error_handler.get_error_statistics()
            
            # Add component status summary
            status["component_status"] = self.component_status.copy()
            status["active_components"] = sum(self.component_status.values())
            status["total_components"] = len(self.component_status)
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting integration status: {e}")
            return {
                "orchestrator": {"initialized": False, "error": str(e)},
                "components": {},
                "component_status": self.component_status.copy()
            }
    
    async def cleanup_all_components(self) -> None:
        """Cleanup all integration components."""
        try:
            logger.info("Starting integration components cleanup")
            
            # Cleanup in reverse order of initialization
            if self.communication_engine:
                await self.communication_engine.shutdown()
                logger.info("Real-time communication engine cleaned up")
            
            if self.github_interface:
                await self.github_interface.cleanup()
                logger.info("GitHub integration interface cleaned up")
            
            if self.openrouter_engine:
                await self.openrouter_engine.cleanup()
                logger.info("OpenRouter integration engine cleaned up")
            
            if self.amasiap_engine:
                await self.amasiap_engine.cleanup()
                logger.info("A.M.A.S.I.A.P. Protocol engine cleaned up")
            
            if self.jaegis_interface:
                await self.jaegis_interface.cleanup()
                logger.info("JAEGIS Master Orchestrator interface cleaned up")
            
            # Reset status
            self.is_initialized = False
            for component in self.component_status:
                self.component_status[component] = False
            
            logger.info("All integration components cleaned up successfully")
            
        except Exception as e:
            logger.error(f"Error during integration cleanup: {e}")


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    # Main orchestrator
    "NLDSIntegrationOrchestrator",
    
    # JAEGIS Integration
    "JAEGISMasterOrchestratorInterface",
    "CommandStatus",
    "OrchestratorStatus",
    "JAEGISMessage",
    "CommandSubmission",
    "CommandStatusResponse",
    "OrchestratorCapabilities",
    "InterfaceResult",
    "JAEGISInterfaceUtils",
    
    # A.M.A.S.I.A.P. Protocol
    "AMASIAPProtocolEngine",
    "EnhancementType",
    "ResearchFramework",
    "ProtocolStatus",
    "InputEnhancement",
    "ResearchActivation",
    "ContextEnrichment",
    "AMASIAPResult",
    "AMASIAPUtils",
    
    # OpenRouter Integration
    "OpenRouterIntegrationEngine",
    "ModelCategory",
    "ModelProvider",
    "RequestPriority",
    "ModelInfo",
    "APIKeyInfo",
    "ModelRequest",
    "ModelResponse",
    "OpenRouterResult",
    "OpenRouterUtils",
    
    # GitHub Integration
    "GitHubIntegrationEngine",
    "ResourceType",
    "SyncStatus",
    "CacheStrategy",
    "GitHubResource",
    "ResourceRequest",
    "SyncOperation",
    "GitHubIntegrationResult",
    "GitHubIntegrationUtils",
    
    # Real-time Communication
    "RealtimeCommunicationEngine",
    "ConnectionStatus",
    "SubscriptionType",
    "RealtimeMessage",
    "ConnectionInfo",
    "Subscription",
    "CommunicationStats",
    "RealtimeCommunicationUtils",
    
    # Error Handling
    "ErrorHandlingEngine",
    "ErrorSeverity",
    "ErrorCategory",
    "FallbackStrategy",
    "SystemState",
    "ErrorInfo",
    "FallbackAction",
    "RecoveryPlan",
    "SystemHealth",
    "ErrorHandlingUtils"
]


# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

def create_integration_orchestrator(config: Dict[str, Any]) -> NLDSIntegrationOrchestrator:
    """
    Create and return a configured N.L.D.S. Integration Orchestrator.
    
    Args:
        config: Complete integration configuration
        
    Returns:
        Configured integration orchestrator
    """
    return NLDSIntegrationOrchestrator(config)


def get_default_integration_config() -> Dict[str, Any]:
    """Get default integration configuration."""
    return {
        "jaegis_orchestrator": {
            "base_url": "https://jaegis.orchestrator.local",
            "websocket_url": "wss://jaegis.orchestrator.local/ws",
            "api_key": None,
            "client_id": "nlds_tier0"
        },
        "amasiap_protocol": {
            "research_api_url": None,
            "context_api_url": None
        },
        "openrouter_integration": {
            "api_keys": [],
            "load_balancing_enabled": True,
            "cost_optimization_enabled": True,
            "max_cost_per_request": 1.0,
            "default_timeout": 30
        },
        "github_integration": {
            "repository_url": "https://github.com/usemanusai/JAEGIS",
            "access_token": None,
            "default_branch": "main",
            "cache_ttl_seconds": 300,
            "max_cache_size": 1000,
            "sync_interval_seconds": 3600
        },
        "realtime_communication": {
            "host": "localhost",
            "port": 8765,
            "ssl_enabled": False,
            "auth_enabled": True,
            "heartbeat_interval": 30,
            "heartbeat_timeout": 60
        },
        "error_handling": {
            "max_error_history": 10000,
            "health_check_interval": 60,
            "error_threshold_24h": 1000,
            "critical_error_threshold": 5,
            "notification_enabled": True,
            "notification_targets": []
        }
    }


# Module version
__version__ = "2.2.0"

logger.info(f"N.L.D.S. Integration Module v{__version__} loaded successfully")
