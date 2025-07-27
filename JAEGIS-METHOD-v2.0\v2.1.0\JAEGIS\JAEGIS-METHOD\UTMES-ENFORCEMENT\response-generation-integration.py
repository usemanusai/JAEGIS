#!/usr/bin/env python3
"""
UTMES Response Generation Integration
Integrates UTMES enforcement into response generation so every response includes enforcement status
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Response generation integration
"""

import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Import UTMES components
from master_utmes_integration_controller import MasterUTMESIntegrationController, UTMESIntegrationResult
from conversation_flow_override_system import UTMESConversationFlowOverrideSystem, FlowOverrideResult

class ResponseIntegrationType(Enum):
    """Types of response integration"""
    FULL_INTEGRATION = "FULL_INTEGRATION"
    STATUS_INJECTION = "STATUS_INJECTION"
    HEADER_FOOTER = "HEADER_FOOTER"
    INLINE_INTEGRATION = "INLINE_INTEGRATION"

class ResponseFormat(Enum):
    """Response format types"""
    MARKDOWN = "MARKDOWN"
    PLAIN_TEXT = "PLAIN_TEXT"
    JSON = "JSON"
    HTML = "HTML"

@dataclass
class ResponseIntegrationConfig:
    """Configuration for response integration"""
    integration_type: ResponseIntegrationType
    response_format: ResponseFormat
    include_task_status: bool
    include_workflow_status: bool
    include_system_health: bool
    include_enforcement_message: bool
    include_statistics: bool
    compact_mode: bool

@dataclass
class IntegratedResponse:
    """Integrated response with UTMES enforcement data"""
    original_response: str
    integrated_response: str
    utmes_data: Dict
    integration_success: bool
    integration_timestamp: str
    response_length_increase: int
    integration_actions: List[str]

class UTMESResponseGenerationIntegrator:
    """
    UTMES Response Generation Integration
    Integrates UTMES enforcement into every response generation
    """
    
    def __init__(self, integration_config: Optional[ResponseIntegrationConfig] = None):
        # Initialize UTMES components
        self.master_controller = MasterUTMESIntegrationController()
        self.flow_override_system = UTMESConversationFlowOverrideSystem()
        
        # Integration configuration
        self.integration_config = integration_config or ResponseIntegrationConfig(
            integration_type=ResponseIntegrationType.FULL_INTEGRATION,
            response_format=ResponseFormat.MARKDOWN,
            include_task_status=True,
            include_workflow_status=True,
            include_system_health=True,
            include_enforcement_message=True,
            include_statistics=False,
            compact_mode=False
        )
        
        # Integration state
        self.integration_active = True
        self.response_history = []
        
        # Initialize integrator
        self._initialize_integrator()
    
    def integrate_utmes_into_response(self, user_input: str, original_response: str = "") -> IntegratedResponse:
        """
        MAIN INTEGRATION FUNCTION
        Integrates UTMES enforcement data into response generation
        
        Args:
            user_input: Original user input
            original_response: Original response content
            
        Returns:
            IntegratedResponse with UTMES enforcement integration
        """
        integration_start = datetime.now()
        integration_actions = []
        
        try:
            # Step 1: Execute UTMES enforcement
            utmes_result = self.master_controller.process_user_input_with_full_enforcement(user_input)
            integration_actions.append("UTMES enforcement executed")
            
            # Step 2: Generate integrated response based on configuration
            if self.integration_config.integration_type == ResponseIntegrationType.FULL_INTEGRATION:
                integrated_response = self._generate_full_integration_response(
                    user_input, original_response, utmes_result
                )
                integration_actions.append("Full integration response generated")
                
            elif self.integration_config.integration_type == ResponseIntegrationType.STATUS_INJECTION:
                integrated_response = self._generate_status_injection_response(
                    original_response, utmes_result
                )
                integration_actions.append("Status injection response generated")
                
            elif self.integration_config.integration_type == ResponseIntegrationType.HEADER_FOOTER:
                integrated_response = self._generate_header_footer_response(
                    original_response, utmes_result
                )
                integration_actions.append("Header/footer response generated")
                
            else:  # INLINE_INTEGRATION
                integrated_response = self._generate_inline_integration_response(
                    original_response, utmes_result
                )
                integration_actions.append("Inline integration response generated")
            
            # Step 3: Calculate response metrics
            response_length_increase = len(integrated_response) - len(original_response)
            
            # Step 4: Create integrated response result
            result = IntegratedResponse(
                original_response=original_response,
                integrated_response=integrated_response,
                utmes_data=utmes_result.__dict__,
                integration_success=True,
                integration_timestamp=integration_start.isoformat(),
                response_length_increase=response_length_increase,
                integration_actions=integration_actions
            )
            
            # Step 5: Log and store result
            self._log_integration_result(result, user_input)
            self.response_history.append(result)
            
            return result
            
        except Exception as e:
            # Handle integration errors
            error_result = IntegratedResponse(
                original_response=original_response,
                integrated_response=f"UTMES Integration Error: {str(e)}\n\n{original_response}",
                utmes_data={},
                integration_success=False,
                integration_timestamp=integration_start.isoformat(),
                response_length_increase=0,
                integration_actions=[f"Integration failed: {str(e)}"]
            )
            
            self.response_history.append(error_result)
            return error_result
    
    def _generate_full_integration_response(self, user_input: str, original_response: str, 
                                          utmes_result: UTMESIntegrationResult) -> str:
        """Generate fully integrated response with complete UTMES data"""
        response_parts = []
        
        # Add UTMES header
        response_parts.append(self._generate_utmes_header(utmes_result))
        
        # Add enforcement status
        if self.integration_config.include_enforcement_message and utmes_result.enforcement_message:
            response_parts.append(f"## 🎯 UTMES ENFORCEMENT STATUS\n{utmes_result.enforcement_message}\n")
        
        # Add task management status
        if self.integration_config.include_task_status and utmes_result.task_enforcement:
            response_parts.append(self._generate_task_status_section(utmes_result.task_enforcement))
        
        # Add workflow status
        if self.integration_config.include_workflow_status and utmes_result.workflow_execution:
            response_parts.append(self._generate_workflow_status_section(utmes_result.workflow_execution))
        
        # Add system health status
        if self.integration_config.include_system_health:
            response_parts.append(self._generate_system_health_section(utmes_result.system_state))
        
        # Add original response content
        if original_response:
            response_parts.append(f"## 📝 RESPONSE CONTENT\n{original_response}\n")
        else:
            response_parts.append(f"## 📝 RESPONSE CONTENT\nProcessing user request: {user_input}\n")
        
        # Add statistics if enabled
        if self.integration_config.include_statistics:
            response_parts.append(self._generate_statistics_section(utmes_result))
        
        # Add UTMES footer
        response_parts.append(self._generate_utmes_footer(utmes_result))
        
        return "\n".join(response_parts)
    
    def _generate_status_injection_response(self, original_response: str, 
                                          utmes_result: UTMESIntegrationResult) -> str:
        """Generate response with status injection"""
        status_injection = self._generate_compact_status(utmes_result)
        
        if original_response:
            return f"{status_injection}\n\n{original_response}"
        else:
            return f"{status_injection}\n\nProcessing your request with UTMES enforcement active."
    
    def _generate_header_footer_response(self, original_response: str, 
                                       utmes_result: UTMESIntegrationResult) -> str:
        """Generate response with header and footer"""
        header = self._generate_utmes_header(utmes_result)
        footer = self._generate_utmes_footer(utmes_result)
        
        content = original_response if original_response else "Processing your request with UTMES enforcement."
        
        return f"{header}\n\n{content}\n\n{footer}"
    
    def _generate_inline_integration_response(self, original_response: str, 
                                            utmes_result: UTMESIntegrationResult) -> str:
        """Generate response with inline integration"""
        if not original_response:
            return self._generate_status_injection_response(original_response, utmes_result)
        
        # Insert UTMES status at strategic points in the response
        lines = original_response.split('\n')
        integrated_lines = []
        
        # Add status after first paragraph
        for i, line in enumerate(lines):
            integrated_lines.append(line)
            if i == 0 and line.strip():  # After first non-empty line
                integrated_lines.append(f"\n🎯 **UTMES**: {self._generate_inline_status(utmes_result)}\n")
        
        return '\n'.join(integrated_lines)
    
    def _generate_utmes_header(self, utmes_result: UTMESIntegrationResult) -> str:
        """Generate UTMES header section"""
        if self.integration_config.compact_mode:
            return (f"🎯 **UTMES ACTIVE** | "
                   f"Mode: {utmes_result.system_state.operation_mode.value} | "
                   f"Health: {utmes_result.system_state.system_health} | "
                   f"Integration: {'✅' if utmes_result.integration_success else '⚠️'}")
        else:
            return (f"# 🎯 UTMES ENFORCEMENT SYSTEM\n"
                   f"**Operation Mode**: {utmes_result.system_state.operation_mode.value}\n"
                   f"**System Health**: {utmes_result.system_state.system_health}\n"
                   f"**Integration Status**: {'✅ Successful' if utmes_result.integration_success else '⚠️ Partial'}\n"
                   f"**Processing Time**: {utmes_result.total_processing_time_ms:.2f}ms")
    
    def _generate_task_status_section(self, task_enforcement) -> str:
        """Generate task status section"""
        return (f"## 📋 AUTOMATIC TASK MANAGEMENT\n"
               f"✅ **Status**: {task_enforcement.status.value}\n"
               f"✅ **Tasks Created**: {task_enforcement.tasks_created} main tasks\n"
               f"✅ **Subtasks Created**: {task_enforcement.subtasks_created} subtasks\n"
               f"✅ **Enforcement Level**: {task_enforcement.enforcement_level.value}\n")
    
    def _generate_workflow_status_section(self, workflow_execution) -> str:
        """Generate workflow status section"""
        return (f"## 🚀 WORKFLOW EXECUTION\n"
               f"✅ **Workflow Type**: {workflow_execution.workflow_type.value}\n"
               f"✅ **Execution State**: {workflow_execution.execution_state.value}\n"
               f"✅ **Progress**: {workflow_execution.steps_completed}/{workflow_execution.total_steps} steps\n"
               f"✅ **Success Rate**: {workflow_execution.success_rate:.1f}%\n")
    
    def _generate_system_health_section(self, system_state) -> str:
        """Generate system health section"""
        return (f"## ⚡ SYSTEM STATUS\n"
               f"✅ **System Health**: {system_state.system_health}\n"
               f"✅ **Enforcement Active**: {'Yes' if system_state.enforcement_active else 'No'}\n"
               f"✅ **Task Management**: {'Active' if system_state.task_management_active else 'Inactive'}\n"
               f"✅ **Workflow Execution**: {'Active' if system_state.workflow_execution_active else 'Inactive'}\n")
    
    def _generate_statistics_section(self, utmes_result: UTMESIntegrationResult) -> str:
        """Generate statistics section"""
        stats = self.master_controller.get_system_statistics()
        return (f"## 📊 SYSTEM STATISTICS\n"
               f"✅ **Total Integrations**: {stats.get('total_integrations', 0)}\n"
               f"✅ **Success Rate**: {stats.get('success_rate', 0):.1f}%\n"
               f"✅ **Average Processing Time**: {stats.get('average_processing_time_ms', 0):.2f}ms\n"
               f"✅ **Active Tasks**: {stats.get('active_tasks_count', 0)}\n")
    
    def _generate_utmes_footer(self, utmes_result: UTMESIntegrationResult) -> str:
        """Generate UTMES footer section"""
        return (f"---\n"
               f"**UTMES Response Integration**: Active | "
               f"**Timestamp**: {datetime.now().isoformat()} | "
               f"**Integration Type**: {self.integration_config.integration_type.value}")
    
    def _generate_compact_status(self, utmes_result: UTMESIntegrationResult) -> str:
        """Generate compact status for injection"""
        task_count = utmes_result.task_enforcement.tasks_created if utmes_result.task_enforcement else 0
        workflow_status = utmes_result.workflow_execution.execution_state.value if utmes_result.workflow_execution else "None"
        
        return (f"🎯 **UTMES**: {utmes_result.system_state.operation_mode.value} | "
               f"📋 **Tasks**: {task_count} created | "
               f"🚀 **Workflow**: {workflow_status} | "
               f"⚡ **Health**: {utmes_result.system_state.system_health}")
    
    def _generate_inline_status(self, utmes_result: UTMESIntegrationResult) -> str:
        """Generate inline status for integration"""
        return (f"Enforcement Active - "
               f"{utmes_result.task_enforcement.tasks_created if utmes_result.task_enforcement else 0} tasks created, "
               f"System {utmes_result.system_state.system_health}")
    
    def _log_integration_result(self, result: IntegratedResponse, user_input: str) -> None:
        """Log integration result for monitoring"""
        log_data = {
            'timestamp': result.integration_timestamp,
            'integration_success': result.integration_success,
            'response_length_increase': result.response_length_increase,
            'integration_type': self.integration_config.integration_type.value,
            'user_input': user_input[:100] + "..." if len(user_input) > 100 else user_input
        }
        
        logging.info(f"UTMES Response Integration: {json.dumps(log_data)}")
    
    def _initialize_integrator(self) -> None:
        """Initialize response generation integrator"""
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - UTMES-ResponseIntegration - %(levelname)s - %(message)s'
        )
        
        # Log initialization
        logging.info(f"UTMES Response Generation Integrator initialized - Type: {self.integration_config.integration_type.value}")
    
    def get_integration_statistics(self) -> Dict:
        """Get response integration statistics"""
        if not self.response_history:
            return {
                'total_integrations': 0,
                'successful_integrations': 0,
                'failed_integrations': 0,
                'average_response_increase': 0,
                'integration_type': self.integration_config.integration_type.value
            }
        
        successful = len([r for r in self.response_history if r.integration_success])
        failed = len([r for r in self.response_history if not r.integration_success])
        avg_increase = sum(r.response_length_increase for r in self.response_history) / len(self.response_history)
        
        return {
            'total_integrations': len(self.response_history),
            'successful_integrations': successful,
            'failed_integrations': failed,
            'success_rate': (successful / len(self.response_history)) * 100 if self.response_history else 0,
            'average_response_increase': round(avg_increase, 2),
            'integration_type': self.integration_config.integration_type.value,
            'integration_active': self.integration_active
        }
    
    def set_integration_config(self, config: ResponseIntegrationConfig) -> None:
        """Set response integration configuration"""
        self.integration_config = config
        logging.info(f"UTMES Response Integration config updated: {config.integration_type.value}")
    
    def enable_integration(self) -> None:
        """Enable response integration"""
        self.integration_active = True
        logging.info("UTMES Response Integration enabled")
    
    def disable_integration(self) -> None:
        """Disable response integration"""
        self.integration_active = False
        logging.warning("UTMES Response Integration disabled")
    
    def is_integration_active(self) -> bool:
        """Check if response integration is active"""
        return (self.integration_active and 
                self.master_controller.is_system_operational())

# Convenience functions for different integration types
def create_full_integration_config() -> ResponseIntegrationConfig:
    """Create configuration for full integration"""
    return ResponseIntegrationConfig(
        integration_type=ResponseIntegrationType.FULL_INTEGRATION,
        response_format=ResponseFormat.MARKDOWN,
        include_task_status=True,
        include_workflow_status=True,
        include_system_health=True,
        include_enforcement_message=True,
        include_statistics=True,
        compact_mode=False
    )

def create_compact_integration_config() -> ResponseIntegrationConfig:
    """Create configuration for compact integration"""
    return ResponseIntegrationConfig(
        integration_type=ResponseIntegrationType.STATUS_INJECTION,
        response_format=ResponseFormat.MARKDOWN,
        include_task_status=True,
        include_workflow_status=True,
        include_system_health=True,
        include_enforcement_message=False,
        include_statistics=False,
        compact_mode=True
    )

def create_minimal_integration_config() -> ResponseIntegrationConfig:
    """Create configuration for minimal integration"""
    return ResponseIntegrationConfig(
        integration_type=ResponseIntegrationType.INLINE_INTEGRATION,
        response_format=ResponseFormat.MARKDOWN,
        include_task_status=True,
        include_workflow_status=False,
        include_system_health=True,
        include_enforcement_message=False,
        include_statistics=False,
        compact_mode=True
    )

# Example usage and testing
if __name__ == "__main__":
    # Initialize response integrator with full integration
    integrator = UTMESResponseGenerationIntegrator(create_full_integration_config())
    
    # Test response integration
    test_input = "Create a comprehensive web application for project management"
    test_original_response = "I can help you create a web application for project management. Let me break this down into key components..."
    
    result = integrator.integrate_utmes_into_response(test_input, test_original_response)
    
    print(f"Integration Success: {result.integration_success}")
    print(f"Response Length Increase: {result.response_length_increase} characters")
    print(f"Integration Actions: {len(result.integration_actions)}")
    
    # Print integrated response (truncated)
    print(f"\nIntegrated Response (first 300 chars):\n{result.integrated_response[:300]}...")
    
    # Get statistics
    stats = integrator.get_integration_statistics()
    print(f"\nIntegration Statistics: {stats}")
    
    # Test integration status
    print(f"Integration Active: {integrator.is_integration_active()}")
    
    # Test different integration types
    print("\n--- Testing Compact Integration ---")
    compact_integrator = UTMESResponseGenerationIntegrator(create_compact_integration_config())
    compact_result = compact_integrator.integrate_utmes_into_response(test_input, test_original_response)
    print(f"Compact Integration (first 200 chars):\n{compact_result.integrated_response[:200]}...")
    
    print("\n--- Testing Minimal Integration ---")
    minimal_integrator = UTMESResponseGenerationIntegrator(create_minimal_integration_config())
    minimal_result = minimal_integrator.integrate_utmes_into_response(test_input, test_original_response)
    print(f"Minimal Integration (first 200 chars):\n{minimal_result.integrated_response[:200]}...")
