"""
JAEGIS Configuration Management System - Core Engine
Central engine for managing configuration parameters, validation, and change propagation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import threading
import logging
from dataclasses import asdict

from .config_schema import (
    JAEGISConfiguration, FrequencyParameters, WorkflowProtocol, AgentConfiguration,
    ConfigurationMode, ParameterType, FREQUENCY_PARAMETER_DEFINITIONS, PRESET_CONFIGURATIONS
)

logger = logging.getLogger(__name__)

class ConfigurationChangeEvent:
    """Event fired when configuration changes"""
    def __init__(self, parameter_name: str, old_value: Any, new_value: Any, timestamp: datetime = None):
        self.parameter_name = parameter_name
        self.old_value = old_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.now()

class ConfigurationEngine:
    """Central configuration management engine"""
    
    def __init__(self, config_dir: str = "JAEGIS_config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.current_config: JAEGISConfiguration = JAEGISConfiguration()
        self.config_history: List[JAEGISConfiguration] = []
        self.change_listeners: List[Callable[[ConfigurationChangeEvent], None]] = []
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Performance tracking
        self.performance_metrics: Dict[str, Any] = {}
        
        # Load existing configuration if available
        self._load_configuration()
        
        logger.info("Configuration engine initialized")
    
    def _load_configuration(self):
        """Load configuration from disk"""
        config_file = self.config_dir / "current_config.json"
        if config_file.exists():
            try:
                self.current_config = JAEGISConfiguration.load_from_file(str(config_file))
                logger.info(f"Loaded configuration: {self.current_config.name}")
            except Exception as e:
                logger.error(f"Failed to load configuration: {e}")
                self.current_config = JAEGISConfiguration()
        else:
            # Create default configuration
            self._create_default_configuration()
    
    def _create_default_configuration(self):
        """Create and save default configuration"""
        self.current_config = JAEGISConfiguration(
            name="Default JAEGIS Configuration",
            description="Default configuration with balanced settings"
        )
        self._save_configuration()
        logger.info("Created default configuration")
    
    def _save_configuration(self):
        """Save current configuration to disk"""
        config_file = self.config_dir / "current_config.json"
        try:
            self.current_config.save_to_file(str(config_file))
            
            # Save to history
            history_file = self.config_dir / f"config_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.current_config.save_to_file(str(history_file))
            
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def get_current_config(self) -> JAEGISConfiguration:
        """Get the current configuration"""
        with self._lock:
            return self.current_config
    
    def update_frequency_parameter(self, parameter_name: str, value: Any) -> bool:
        """Update a frequency parameter"""
        with self._lock:
            # Validate parameter
            if parameter_name not in FREQUENCY_PARAMETER_DEFINITIONS:
                logger.error(f"Unknown frequency parameter: {parameter_name}")
                return False
            
            param_def = FREQUENCY_PARAMETER_DEFINITIONS[parameter_name]
            if not param_def.validate_value(value):
                logger.error(f"Invalid value for {parameter_name}: {value}")
                return False
            
            # Get old value
            old_value = getattr(self.current_config.frequency_parameters, parameter_name)
            
            # Update value
            setattr(self.current_config.frequency_parameters, parameter_name, value)
            self.current_config.modified_at = datetime.now()
            
            # Fire change event
            event = ConfigurationChangeEvent(parameter_name, old_value, value)
            self._fire_change_event(event)
            
            # Save configuration
            self._save_configuration()
            
            logger.info(f"Updated {parameter_name}: {old_value} -> {value}")
            return True
    
    def update_agent_utilization(self, tier: str, value: int) -> bool:
        """Update agent utilization for a specific tier"""
        with self._lock:
            if not (0 <= value <= 100):
                logger.error(f"Invalid agent utilization value: {value}")
                return False
            
            from .config_schema import AgentTier
            try:
                agent_tier = AgentTier(tier)
            except ValueError:
                logger.error(f"Invalid agent tier: {tier}")
                return False
            
            old_value = self.current_config.frequency_parameters.agent_utilization.get(agent_tier, 0)
            self.current_config.frequency_parameters.agent_utilization[agent_tier] = value
            self.current_config.modified_at = datetime.now()
            
            # Fire change event
            event = ConfigurationChangeEvent(f"agent_utilization.{tier}", old_value, value)
            self._fire_change_event(event)
            
            self._save_configuration()
            
            logger.info(f"Updated agent utilization for {tier}: {old_value} -> {value}")
            return True
    
    def apply_preset_mode(self, mode: ConfigurationMode) -> bool:
        """Apply a preset configuration mode"""
        with self._lock:
            if mode not in PRESET_CONFIGURATIONS:
                logger.error(f"Unknown preset mode: {mode}")
                return False
            
            preset = PRESET_CONFIGURATIONS[mode]
            old_mode = self.current_config.mode
            
            # Update frequency parameters
            for param_name, value in preset.items():
                if param_name == "agent_utilization":
                    for tier, util_value in value.items():
                        self.current_config.frequency_parameters.agent_utilization[tier] = util_value
                else:
                    setattr(self.current_config.frequency_parameters, param_name, value)
            
            self.current_config.mode = mode
            self.current_config.modified_at = datetime.now()
            
            # Fire change event
            event = ConfigurationChangeEvent("configuration_mode", old_mode, mode)
            self._fire_change_event(event)
            
            self._save_configuration()
            
            logger.info(f"Applied preset mode: {mode.value}")
            return True
    
    def add_protocol(self, protocol: WorkflowProtocol) -> bool:
        """Add a new workflow protocol"""
        with self._lock:
            # Check if protocol already exists
            existing = next((p for p in self.current_config.protocols if p.protocol_id == protocol.protocol_id), None)
            if existing:
                logger.error(f"Protocol already exists: {protocol.protocol_id}")
                return False
            
            self.current_config.protocols.append(protocol)
            self.current_config.modified_at = datetime.now()
            
            # Fire change event
            event = ConfigurationChangeEvent("protocol_added", None, protocol.protocol_id)
            self._fire_change_event(event)
            
            self._save_configuration()
            
            logger.info(f"Added protocol: {protocol.name}")
            return True
    
    def update_protocol(self, protocol: WorkflowProtocol) -> bool:
        """Update an existing workflow protocol"""
        with self._lock:
            # Find existing protocol
            for i, existing in enumerate(self.current_config.protocols):
                if existing.protocol_id == protocol.protocol_id:
                    old_protocol = existing
                    self.current_config.protocols[i] = protocol
                    self.current_config.modified_at = datetime.now()
                    
                    # Fire change event
                    event = ConfigurationChangeEvent("protocol_updated", old_protocol.name, protocol.name)
                    self._fire_change_event(event)
                    
                    self._save_configuration()
                    
                    logger.info(f"Updated protocol: {protocol.name}")
                    return True
            
            logger.error(f"Protocol not found: {protocol.protocol_id}")
            return False
    
    def remove_protocol(self, protocol_id: str) -> bool:
        """Remove a workflow protocol"""
        with self._lock:
            # Find and remove protocol
            for i, protocol in enumerate(self.current_config.protocols):
                if protocol.protocol_id == protocol_id:
                    removed_protocol = self.current_config.protocols.pop(i)
                    self.current_config.modified_at = datetime.now()
                    
                    # Fire change event
                    event = ConfigurationChangeEvent("protocol_removed", removed_protocol.name, None)
                    self._fire_change_event(event)
                    
                    self._save_configuration()
                    
                    logger.info(f"Removed protocol: {removed_protocol.name}")
                    return True
            
            logger.error(f"Protocol not found: {protocol_id}")
            return False
    
    def update_agent_configuration(self, agent_config: AgentConfiguration) -> bool:
        """Update agent configuration"""
        with self._lock:
            # Find existing agent configuration
            for i, existing in enumerate(self.current_config.agent_configurations):
                if existing.agent_id == agent_config.agent_id:
                    old_config = existing
                    self.current_config.agent_configurations[i] = agent_config
                    self.current_config.modified_at = datetime.now()
                    
                    # Fire change event
                    event = ConfigurationChangeEvent(
                        f"agent_config.{agent_config.agent_id}", 
                        old_config.to_dict(), 
                        agent_config.to_dict()
                    )
                    self._fire_change_event(event)
                    
                    self._save_configuration()
                    
                    logger.info(f"Updated agent configuration: {agent_config.agent_name}")
                    return True
            
            # Add new agent configuration
            self.current_config.agent_configurations.append(agent_config)
            self.current_config.modified_at = datetime.now()
            
            # Fire change event
            event = ConfigurationChangeEvent(
                f"agent_config.{agent_config.agent_id}", 
                None, 
                agent_config.to_dict()
            )
            self._fire_change_event(event)
            
            self._save_configuration()
            
            logger.info(f"Added agent configuration: {agent_config.agent_name}")
            return True
    
    def get_agent_configuration(self, agent_id: str) -> Optional[AgentConfiguration]:
        """Get configuration for a specific agent"""
        with self._lock:
            for config in self.current_config.agent_configurations:
                if config.agent_id == agent_id:
                    return config
            return None
    
    def validate_configuration(self) -> List[str]:
        """Validate the current configuration and return any errors"""
        errors = []
        
        # Validate frequency parameters
        for param_name, param_def in FREQUENCY_PARAMETER_DEFINITIONS.items():
            value = getattr(self.current_config.frequency_parameters, param_name)
            if not param_def.validate_value(value):
                errors.append(f"Invalid value for {param_name}: {value}")
        
        # Validate agent utilization
        for tier, value in self.current_config.frequency_parameters.agent_utilization.items():
            if not (0 <= value <= 100):
                errors.append(f"Invalid agent utilization for {tier.value}: {value}")
        
        # Validate protocols
        protocol_ids = set()
        for protocol in self.current_config.protocols:
            if protocol.protocol_id in protocol_ids:
                errors.append(f"Duplicate protocol ID: {protocol.protocol_id}")
            protocol_ids.add(protocol.protocol_id)
        
        # Validate agent configurations
        agent_ids = set()
        for agent_config in self.current_config.agent_configurations:
            if agent_config.agent_id in agent_ids:
                errors.append(f"Duplicate agent ID: {agent_config.agent_id}")
            agent_ids.add(agent_config.agent_id)
            
            if not (0 <= agent_config.activation_frequency <= 100):
                errors.append(f"Invalid activation frequency for {agent_config.agent_name}: {agent_config.activation_frequency}")
        
        return errors
    
    def export_configuration(self, filepath: str) -> bool:
        """Export configuration to file"""
        try:
            with self._lock:
                self.current_config.save_to_file(filepath)
            logger.info(f"Configuration exported to: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export configuration: {e}")
            return False
    
    def import_configuration(self, filepath: str) -> bool:
        """Import configuration from file"""
        try:
            with self._lock:
                new_config = JAEGISConfiguration.load_from_file(filepath)
                
                # Validate imported configuration
                old_config = self.current_config
                self.current_config = new_config
                errors = self.validate_configuration()
                
                if errors:
                    # Restore old configuration if validation fails
                    self.current_config = old_config
                    logger.error(f"Configuration validation failed: {errors}")
                    return False
                
                # Save imported configuration
                self._save_configuration()
                
                # Fire change event
                event = ConfigurationChangeEvent("configuration_imported", old_config.name, new_config.name)
                self._fire_change_event(event)
                
                logger.info(f"Configuration imported from: {filepath}")
                return True
        except Exception as e:
            logger.error(f"Failed to import configuration: {e}")
            return False
    
    def rollback_configuration(self, steps: int = 1) -> bool:
        """Rollback configuration to a previous state"""
        with self._lock:
            history_files = sorted([
                f for f in self.config_dir.glob("config_history_*.json")
            ], reverse=True)
            
            if len(history_files) < steps:
                logger.error(f"Not enough history to rollback {steps} steps")
                return False
            
            try:
                rollback_file = history_files[steps - 1]
                old_config = self.current_config
                self.current_config = JAEGISConfiguration.load_from_file(str(rollback_file))
                
                # Save rolled back configuration as current
                self._save_configuration()
                
                # Fire change event
                event = ConfigurationChangeEvent("configuration_rollback", old_config.name, self.current_config.name)
                self._fire_change_event(event)
                
                logger.info(f"Configuration rolled back {steps} steps")
                return True
            except Exception as e:
                logger.error(f"Failed to rollback configuration: {e}")
                return False
    
    def add_change_listener(self, listener: Callable[[ConfigurationChangeEvent], None]):
        """Add a listener for configuration changes"""
        self.change_listeners.append(listener)
    
    def remove_change_listener(self, listener: Callable[[ConfigurationChangeEvent], None]):
        """Remove a configuration change listener"""
        if listener in self.change_listeners:
            self.change_listeners.remove(listener)
    
    def _fire_change_event(self, event: ConfigurationChangeEvent):
        """Fire a configuration change event to all listeners"""
        for listener in self.change_listeners:
            try:
                listener(event)
            except Exception as e:
                logger.error(f"Error in change listener: {e}")
    
    def get_performance_impact_prediction(self, parameter_name: str, new_value: Any) -> Dict[str, Any]:
        """Predict the performance impact of changing a parameter"""
        # This would use historical data and ML models in a real implementation
        # For now, provide basic predictions based on parameter definitions
        
        if parameter_name not in FREQUENCY_PARAMETER_DEFINITIONS:
            return {"error": "Unknown parameter"}
        
        param_def = FREQUENCY_PARAMETER_DEFINITIONS[parameter_name]
        current_value = getattr(self.current_config.frequency_parameters, parameter_name)
        
        change_magnitude = abs(new_value - current_value)
        
        prediction = {
            "parameter": parameter_name,
            "current_value": current_value,
            "new_value": new_value,
            "change_magnitude": change_magnitude,
            "impact_level": "low" if change_magnitude < 20 else "medium" if change_magnitude < 50 else "high",
            "estimated_effects": []
        }
        
        # Add parameter-specific predictions
        if parameter_name == "research_intensity":
            if new_value > current_value:
                prediction["estimated_effects"].append("Increased research thoroughness")
                prediction["estimated_effects"].append("Longer initial response times")
            else:
                prediction["estimated_effects"].append("Faster initial responses")
                prediction["estimated_effects"].append("Potentially less comprehensive research")
        
        elif parameter_name == "validation_thoroughness":
            if new_value > current_value:
                prediction["estimated_effects"].append("Higher quality outputs")
                prediction["estimated_effects"].append("Increased processing time")
            else:
                prediction["estimated_effects"].append("Faster processing")
                prediction["estimated_effects"].append("Potentially lower quality assurance")
        
        return prediction
    
    def get_configuration_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current configuration"""
        with self._lock:
            stats = {
                "configuration_name": self.current_config.name,
                "mode": self.current_config.mode.value,
                "created_at": self.current_config.created_at.isoformat(),
                "modified_at": self.current_config.modified_at.isoformat(),
                "frequency_parameters": self.current_config.frequency_parameters.to_dict(),
                "protocol_count": len(self.current_config.protocols),
                "agent_configuration_count": len(self.current_config.agent_configurations),
                "validation_errors": len(self.validate_configuration())
            }
            
            # Calculate average utilization
            agent_utils = list(self.current_config.frequency_parameters.agent_utilization.values())
            stats["average_agent_utilization"] = sum(agent_utils) / len(agent_utils) if agent_utils else 0
            
            return stats
