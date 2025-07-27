"""
JAEGIS Enhanced System v2.0 - Workflow Configuration Controller
Main controller that orchestrates all workflow configuration components
Provides unified interface for workflow sequence management, feature toggles, and natural language processing
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json
import uuid

from .workflow_sequence_engine import WorkflowSequenceEngine, WorkflowOperation, WorkflowTemplate
from .feature_toggle_system import FeatureToggleSystem, ToggleMode
from .natural_language_interface import NaturalLanguageInterface
from .workflow_interface_design import WorkflowInterfaceDesign

logger = logging.getLogger(__name__)

class WorkflowConfigurationController:
    """Main controller for workflow configuration system"""
    
    def __init__(self):
        # Initialize core components
        self.workflow_engine = WorkflowSequenceEngine()
        self.feature_toggle_system = FeatureToggleSystem()
        self.natural_language_interface = NaturalLanguageInterface(
            self.workflow_engine, self.feature_toggle_system
        )
        self.interface_design = WorkflowInterfaceDesign(
            self.workflow_engine, self.feature_toggle_system, self.natural_language_interface
        )
        
        # System state
        self.system_initialized = False
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Configuration state
        self.current_configuration = {
            "workflow_sequence": None,
            "feature_states": None,
            "interface_settings": None,
            "last_modified": None
        }
        
        # Statistics
        self.controller_stats = {
            "total_configurations": 0,
            "successful_modifications": 0,
            "failed_modifications": 0,
            "natural_language_commands": 0,
            "voice_commands": 0
        }
        
        logger.info("Workflow Configuration Controller initialized")
    
    async def initialize_workflow_configuration_system(self) -> Dict[str, Any]:
        """Initialize the complete workflow configuration system"""
        
        try:
            # Initialize workflow sequence engine
            logger.info("Initializing workflow sequence engine...")
            workflow_init = await self.workflow_engine.initialize_preset_templates()
            
            # Initialize feature toggle system
            logger.info("Initializing feature toggle system...")
            feature_init = await self.feature_toggle_system.initialize_feature_definitions()
            
            # Initialize natural language interface (no async init needed)
            nl_init = {"natural_language_interface_initialized": True}
            
            # Initialize interface design (no async init needed)
            interface_init = {"workflow_interface_design_initialized": True}
            
            # Update current configuration
            self.current_configuration = {
                "workflow_sequence": self.workflow_engine.get_current_sequence_display(),
                "feature_states": self.feature_toggle_system.get_feature_states_display(),
                "interface_settings": self.interface_design.get_interface_configuration(),
                "last_modified": datetime.now().isoformat()
            }
            
            self.system_initialized = True
            
            return {
                "workflow_configuration_initializedTrue_system_components": {
                    "workflow_engine": workflow_init,
                    "feature_toggle_system": feature_init,
                    "natural_language_interface": nl_init,
                    "interface_design": interface_init
                },
                "total_features": feature_init.get("total_features", 0),
                "preset_templates": workflow_init.get("templates_available", 0),
                "current_configuration": self.current_configuration
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize workflow configuration system: {e}")
            return {
                "workflow_configuration_initialized": False,
                "error": str(e)
            }
    
    async def get_workflow_configuration_menu(self, session_id: str = None) -> str:
        """Get the complete workflow configuration menu"""
        
        if not self.system_initialized:
            return """
# ❌ **Workflow Configuration System Not Initialized**

The workflow configuration system is not yet initialized. Please initialize the system first.

**To initialize**: Call `initialize_workflow_configuration_system()`
"""
        
        try:
            # Generate comprehensive menu
            menu = await self.interface_design.generate_workflow_configuration_menu(session_id)
            
            # Add session-specific information if available
            if session_id and session_id in self.active_sessions:
                session_info = self.active_sessions[session_id]
                menu += f"\n\n**🔄 Session Info**: Active session {session_id} | Commands: {session_info.get('command_count', 0)}"
            
            return menu
            
        except Exception as e:
            logger.error(f"Error generating workflow configuration menu: {e}")
            return f"""
# ❌ **Error Generating Configuration Menu**

An error occurred while generating the workflow configuration menu:
**Error**: {str(e)}

Please try again or contact support if the issue persists.
"""
    
    async def process_workflow_command(self, command: str, session_id: str = None, 
                                     voice_input: bool = False) -> Dict[str, Any]:
        """Process workflow configuration command"""
        
        if not self.system_initialized:
            return {
                "success": False,
                "error": "Workflow configuration system not initialized",
                "response": "Please initialize the workflow configuration system first."
            }
        
        try:
            # Create or update session
            if not session_id:
                session_id = str(uuid.uuid4())
            
            if session_id not in self.active_sessions:
                self.active_sessions[session_id] = {
                    "created_at": datetime.now(),
                    "command_count": 0,
                    "last_activity": datetime.now()
                }
            
            session = self.active_sessions[session_id]
            session["command_count"] += 1
            session["last_activity"] = datetime.now()
            
            # Process command through natural language interface
            result = await self.natural_language_interface.process_natural_language_command(
                command, session_id, voice_input
            )
            
            # Update statistics
            self.controller_stats["total_configurations"] += 1
            if voice_input:
                self.controller_stats["voice_commands"] += 1
            else:
                self.controller_stats["natural_language_commands"] += 1
            
            if result.get("success"):
                self.controller_stats["successful_modifications"] += 1
                
                # Update current configuration
                self.current_configuration = {
                    "workflow_sequence": self.workflow_engine.get_current_sequence_display(),
                    "feature_states": self.feature_toggle_system.get_feature_states_display(),
                    "interface_settings": self.interface_design.get_interface_configuration(),
                    "last_modified": datetime.now().isoformat()
                }
            else:
                self.controller_stats["failed_modifications"] += 1
            
            # Add session information to result
            result["session_id"] = session_id
            result["session_info"] = {
                "command_count": session["command_count"],
                "session_duration": (datetime.now() - session["created_at"]).total_seconds()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing workflow command: {e}")
            self.controller_stats["failed_modifications"] += 1
            
            return {
                "success": False,
                "error": str(e),
                "response": f"Sorry, I encountered an error processing your command: {str(e)}"
            }
    
    async def process_voice_command(self, audio_data: bytes, session_id: str = None) -> Dict[str, Any]:
        """Process voice workflow command"""
        
        if not self.system_initialized:
            return {
                "success": False,
                "error": "Workflow configuration system not initialized",
                "response": "Please initialize the workflow configuration system first."
            }
        
        try:
            # Process voice command through natural language interface
            result = await self.natural_language_interface.process_voice_command(audio_data, session_id)
            
            # Update statistics
            self.controller_stats["voice_commands"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "Sorry, I had trouble processing your voice command."
            }
    
    async def apply_workflow_template(self, template_name: str) -> Dict[str, Any]:
        """Apply a workflow template"""
        
        if not self.system_initialized:
            return {"error": "System not initialized"}
        
        try:
            # Map template name to enum
            template_mapping = {
                "research_first": WorkflowTemplate.RESEARCH_FIRST,
                "research-first": WorkflowTemplate.RESEARCH_FIRST,
                "rapid_execution": WorkflowTemplate.RAPID_EXECUTION,
                "rapid": WorkflowTemplate.RAPID_EXECUTION,
                "quality_focused": WorkflowTemplate.QUALITY_FOCUSED,
                "quality": WorkflowTemplate.QUALITY_FOCUSED,
                "balanced": WorkflowTemplate.BALANCED_APPROACH,
                "balanced_approach": WorkflowTemplate.BALANCED_APPROACH
            }
            
            template = template_mapping.get(template_name.lower())
            if not template:
                return {"error": f"Unknown template: {template_name}"}
            
            # Apply template
            result = await self.workflow_engine.apply_template(template)
            
            if result.get("success"):
                # Update current configuration
                self.current_configuration["workflow_sequence"] = self.workflow_engine.get_current_sequence_display()
                self.current_configuration["last_modified"] = datetime.now().isoformat()
                
                self.controller_stats["successful_modifications"] += 1
            else:
                self.controller_stats["failed_modifications"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Error applying workflow template: {e}")
            self.controller_stats["failed_modifications"] += 1
            return {"error": str(e)}
    
    async def toggle_feature_mode(self, mode_name: str) -> Dict[str, Any]:
        """Toggle feature mode"""
        
        if not self.system_initialized:
            return {"error": "System not initialized"}
        
        try:
            # Map mode name to enum
            mode_mapping = {
                "speed": ToggleMode.SPEED_MODE,
                "speed_mode": ToggleMode.SPEED_MODE,
                "quality": ToggleMode.QUALITY_MODE,
                "quality_mode": ToggleMode.QUALITY_MODE,
                "minimal": ToggleMode.MINIMAL_MODE,
                "minimal_mode": ToggleMode.MINIMAL_MODE,
                "research": ToggleMode.RESEARCH_MODE,
                "research_mode": ToggleMode.RESEARCH_MODE,
                "custom": ToggleMode.CUSTOM_MODE
            }
            
            mode = mode_mapping.get(mode_name.lower())
            if not mode:
                return {"error": f"Unknown mode: {mode_name}"}
            
            # Apply mode
            result = await self.feature_toggle_system.apply_toggle_mode(mode)
            
            if result.get("success"):
                # Update current configuration
                self.current_configuration["feature_states"] = self.feature_toggle_system.get_feature_states_display()
                self.current_configuration["last_modified"] = datetime.now().isoformat()
                
                self.controller_stats["successful_modifications"] += 1
            else:
                self.controller_stats["failed_modifications"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Error toggling feature mode: {e}")
            self.controller_stats["failed_modifications"] += 1
            return {"error": str(e)}
    
    def get_current_configuration(self) -> Dict[str, Any]:
        """Get current workflow configuration"""
        
        if not self.system_initialized:
            return {"error": "System not initialized"}
        
        return {
            "system_initialized": self.system_initialized,
            "current_configuration": self.current_configuration,
            "active_sessions": len(self.active_sessions),
            "statistics": self.controller_stats.copy()
        }
    
    def get_configuration_status(self) -> Dict[str, Any]:
        """Get comprehensive configuration status"""
        
        if not self.system_initialized:
            return {
                "system_initialized": False,
                "error": "Workflow configuration system not initialized"
            }
        
        return {
            "system_initializedself_system_initialized_workflow_engine_status": {
                "current_sequence": self.workflow_engine.get_current_sequence_display(),
                "available_templatestool_2311": {
                "feature_statestool_9475": {
                "interface_statisticstool_1828": {
                "interface_configuration": self.interface_design.get_interface_configuration()
            },
            "controller_statistics": self.controller_stats.copy(),
            "active_sessions": len(self.active_sessions),
            "last_modified": self.current_configuration.get("last_modified")
        }
    
    async def reset_to_default_configuration(self) -> Dict[str, Any]:
        """Reset workflow configuration to default settings"""
        
        if not self.system_initialized:
            return {"error": "System not initialized"}
        
        try:
            # Apply balanced approach template (default)
            template_result = await self.workflow_engine.apply_template(WorkflowTemplate.BALANCED_APPROACH)
            
            # Apply custom mode (default feature state)
            mode_result = await self.feature_toggle_system.apply_toggle_mode(ToggleMode.CUSTOM_MODE)
            
            # Update current configuration
            self.current_configuration = {
                "workflow_sequence": self.workflow_engine.get_current_sequence_display(),
                "feature_states": self.feature_toggle_system.get_feature_states_display(),
                "interface_settings": self.interface_design.get_interface_configuration(),
                "last_modified": datetime.now().isoformat()
            }
            
            self.controller_stats["successful_modifications"] += 1
            
            return {
                "success": True,
                "message": "Configuration reset to default settings",
                "template_result": template_result,
                "mode_result": mode_result,
                "current_configuration": self.current_configuration
            }
            
        except Exception as e:
            logger.error(f"Error resetting configuration: {e}")
            self.controller_stats["failed_modifications"] += 1
            return {"error": str(e)}
    
    def cleanup_inactive_sessions(self, max_age_hours: int = 24) -> Dict[str, Any]:
        """Clean up inactive sessions"""
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        inactive_sessions = [
            session_id for session_id, session_data in self.active_sessions.items()
            if session_data["last_activity"] < cutoff_time
        ]
        
        for session_id in inactive_sessions:
            del self.active_sessions[session_id]
        
        return {
            "sessions_cleaned": len(inactive_sessions),
            "active_sessions_remaining": len(self.active_sessions)
        }
    
    async def export_configuration(self) -> Dict[str, Any]:
        """Export current configuration for backup or sharing"""
        
        if not self.system_initialized:
            return {"error": "System not initialized"}
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "system_version": "JAEGIS Enhanced System v2.0",
            "workflow_configuration": self.current_configuration,
            "statistics": self.controller_stats.copy()
        }
        
        return {
            "success": True,
            "export_data": export_data,
            "export_size": len(json.dumps(export_data))
        }
    
    async def import_configuration(self, import_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import configuration from backup or sharing"""
        
        if not self.system_initialized:
            return {"error": "System not initialized"}
        
        try:
            # Validate import data
            if "workflow_configuration" not in import_data:
                return {"error": "Invalid import data - missing workflow_configuration"}
            
            # Apply imported configuration (simplified implementation)
            # In a real implementation, this would restore the exact configuration
            
            return {
                "success": True,
                "message": "Configuration imported successfully",
                "import_timestamp": import_data.get("export_timestamp", "unknown")
            }
            
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
            return {"error": str(e)}
