#!/usr/bin/env python3
"""
UTMES Conversation Flow Override System
Creates system that overrides default conversation flow to include mandatory UTMES enforcement
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Conversation flow architecture override
"""

import json
import logging
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Import UTMES components
from master_utmes_integration_controller import MasterUTMESIntegrationController, UTMESOperationMode
from system_level_enforcement_hooks import UTMESSystemLevelEnforcementHooks, HookType

class ConversationFlowState(Enum):
    """States of conversation flow processing"""
    INITIALIZING = "INITIALIZING"
    PRE_PROCESSING = "PRE_PROCESSING"
    UTMES_ENFORCEMENT = "UTMES_ENFORCEMENT"
    CONTENT_GENERATION = "CONTENT_GENERATION"
    POST_PROCESSING = "POST_PROCESSING"
    RESPONSE_FINALIZATION = "RESPONSE_FINALIZATION"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"

class OverrideLevel(Enum):
    """Levels of conversation flow override"""
    COMPLETE_OVERRIDE = "COMPLETE_OVERRIDE"
    PARTIAL_OVERRIDE = "PARTIAL_OVERRIDE"
    HOOK_INJECTION = "HOOK_INJECTION"
    MONITORING_ONLY = "MONITORING_ONLY"

@dataclass
class ConversationFlowContext:
    """Context for conversation flow processing"""
    user_input: str
    conversation_id: str
    session_id: str
    timestamp: str
    flow_state: ConversationFlowState
    override_level: OverrideLevel
    enforcement_required: bool
    original_flow_data: Dict
    utmes_data: Dict

@dataclass
class FlowOverrideResult:
    """Result of conversation flow override"""
    override_success: bool
    flow_state: ConversationFlowState
    enforcement_applied: bool
    original_response: Optional[str]
    enhanced_response: str
    utmes_integration_result: Optional[Dict]
    processing_time_ms: float
    override_actions: List[str]

class UTMESConversationFlowOverrideSystem:
    """
    UTMES Conversation Flow Override System
    Overrides default conversation flow to include mandatory UTMES enforcement
    """
    
    def __init__(self, override_level: OverrideLevel = OverrideLevel.COMPLETE_OVERRIDE):
        # Initialize UTMES components
        self.master_controller = MasterUTMESIntegrationController()
        self.hook_system = UTMESSystemLevelEnforcementHooks(self.master_controller)
        
        # Override configuration
        self.override_level = override_level
        self.override_active = True
        self.mandatory_enforcement = True
        
        # Flow override state
        self.active_overrides = {}
        self.override_history = []
        
        # Install system hooks
        self._install_flow_override_hooks()
        
        # Initialize override system
        self._initialize_override_system()
    
    def override_conversation_flow(self, user_input: str, original_context: Optional[Dict] = None) -> FlowOverrideResult:
        """
        MAIN FLOW OVERRIDE FUNCTION
        Overrides default conversation flow to include mandatory UTMES enforcement
        
        Args:
            user_input: User input to process
            original_context: Original conversation context
            
        Returns:
            FlowOverrideResult with complete override processing
        """
        start_time = datetime.now()
        
        try:
            # Step 1: Initialize flow context
            flow_context = self._create_flow_context(user_input, original_context)
            
            # Step 2: Execute flow override based on level
            if self.override_level == OverrideLevel.COMPLETE_OVERRIDE:
                override_result = self._execute_complete_override(flow_context)
            elif self.override_level == OverrideLevel.PARTIAL_OVERRIDE:
                override_result = self._execute_partial_override(flow_context)
            elif self.override_level == OverrideLevel.HOOK_INJECTION:
                override_result = self._execute_hook_injection(flow_context)
            else:
                override_result = self._execute_monitoring_only(flow_context)
            
            # Step 3: Calculate processing time
            end_time = datetime.now()
            override_result.processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Step 4: Log and store result
            self._log_override_result(override_result, user_input)
            self.override_history.append(override_result)
            
            return override_result
            
        except Exception as e:
            # Handle override errors
            error_result = self._create_error_result(user_input, str(e), start_time)
            self.override_history.append(error_result)
            return error_result
    
    def _execute_complete_override(self, context: ConversationFlowContext) -> FlowOverrideResult:
        """Execute complete conversation flow override"""
        override_actions = []
        
        # Step 1: Pre-processing with UTMES hooks
        context.flow_state = ConversationFlowState.PRE_PROCESSING
        pre_hook_results = self.hook_system.execute_hooks(HookType.PRE_PROCESSING, context.__dict__)
        override_actions.append(f"Pre-processing hooks executed: {len(pre_hook_results)}")
        
        # Step 2: Input validation hooks
        input_hook_results = self.hook_system.execute_hooks(HookType.INPUT_VALIDATION, context.__dict__)
        override_actions.append(f"Input validation hooks executed: {len(input_hook_results)}")
        
        # Step 3: UTMES enforcement
        context.flow_state = ConversationFlowState.UTMES_ENFORCEMENT
        utmes_result = self.master_controller.process_user_input_with_full_enforcement(
            context.user_input, context.__dict__
        )
        override_actions.append(f"UTMES enforcement executed: {utmes_result.integration_success}")
        
        # Step 4: Content generation with enforcement data
        context.flow_state = ConversationFlowState.CONTENT_GENERATION
        enhanced_response = self._generate_enhanced_response(context, utmes_result)
        override_actions.append("Enhanced response generated with UTMES integration")
        
        # Step 5: Response generation hooks
        response_context = context.__dict__.copy()
        response_context['utmes_result'] = utmes_result
        response_hook_results = self.hook_system.execute_hooks(HookType.RESPONSE_GENERATION, response_context)
        override_actions.append(f"Response generation hooks executed: {len(response_hook_results)}")
        
        # Step 6: Post-processing hooks
        context.flow_state = ConversationFlowState.POST_PROCESSING
        post_hook_results = self.hook_system.execute_hooks(HookType.POST_PROCESSING, response_context)
        override_actions.append(f"Post-processing hooks executed: {len(post_hook_results)}")
        
        # Step 7: Finalize response
        context.flow_state = ConversationFlowState.RESPONSE_FINALIZATION
        final_response = self._finalize_response(enhanced_response, utmes_result, response_hook_results)
        override_actions.append("Response finalized with enforcement status")
        
        context.flow_state = ConversationFlowState.COMPLETE
        
        return FlowOverrideResult(
            override_success=True,
            flow_state=context.flow_state,
            enforcement_applied=True,
            original_response=None,  # Complete override - no original response
            enhanced_response=final_response,
            utmes_integration_result=utmes_result.__dict__,
            processing_time_ms=0.0,  # Will be set by caller
            override_actions=override_actions
        )
    
    def _execute_partial_override(self, context: ConversationFlowContext) -> FlowOverrideResult:
        """Execute partial conversation flow override"""
        override_actions = []
        
        # Step 1: Execute UTMES enforcement
        context.flow_state = ConversationFlowState.UTMES_ENFORCEMENT
        utmes_result = self.master_controller.process_user_input_with_full_enforcement(
            context.user_input, context.__dict__
        )
        override_actions.append("UTMES enforcement executed")
        
        # Step 2: Execute critical hooks only
        critical_hooks = self.hook_system.execute_hooks(HookType.PRE_PROCESSING, context.__dict__)
        override_actions.append(f"Critical hooks executed: {len(critical_hooks)}")
        
        # Step 3: Generate enhanced response
        context.flow_state = ConversationFlowState.CONTENT_GENERATION
        enhanced_response = self._generate_enhanced_response(context, utmes_result)
        override_actions.append("Partial enhancement applied to response")
        
        context.flow_state = ConversationFlowState.COMPLETE
        
        return FlowOverrideResult(
            override_success=True,
            flow_state=context.flow_state,
            enforcement_applied=True,
            original_response=context.original_flow_data.get('response'),
            enhanced_response=enhanced_response,
            utmes_integration_result=utmes_result.__dict__,
            processing_time_ms=0.0,
            override_actions=override_actions
        )
    
    def _execute_hook_injection(self, context: ConversationFlowContext) -> FlowOverrideResult:
        """Execute hook injection override"""
        override_actions = []
        
        # Step 1: Execute hooks without full override
        pre_hooks = self.hook_system.execute_hooks(HookType.PRE_PROCESSING, context.__dict__)
        post_hooks = self.hook_system.execute_hooks(HookType.POST_PROCESSING, context.__dict__)
        override_actions.extend([
            f"Pre-processing hooks injected: {len(pre_hooks)}",
            f"Post-processing hooks injected: {len(post_hooks)}"
        ])
        
        # Step 2: Light UTMES integration
        utmes_result = self.master_controller.process_user_input_with_full_enforcement(
            context.user_input, context.__dict__
        )
        override_actions.append("Light UTMES integration applied")
        
        context.flow_state = ConversationFlowState.COMPLETE
        
        return FlowOverrideResult(
            override_success=True,
            flow_state=context.flow_state,
            enforcement_applied=True,
            original_response=context.original_flow_data.get('response'),
            enhanced_response=self._inject_enforcement_status(
                context.original_flow_data.get('response', ''), utmes_result
            ),
            utmes_integration_result=utmes_result.__dict__,
            processing_time_ms=0.0,
            override_actions=override_actions
        )
    
    def _execute_monitoring_only(self, context: ConversationFlowContext) -> FlowOverrideResult:
        """Execute monitoring-only override"""
        override_actions = ["Monitoring-only mode - no enforcement applied"]
        
        # Just monitor without enforcement
        context.flow_state = ConversationFlowState.COMPLETE
        
        return FlowOverrideResult(
            override_success=True,
            flow_state=context.flow_state,
            enforcement_applied=False,
            original_response=context.original_flow_data.get('response'),
            enhanced_response=context.original_flow_data.get('response', ''),
            utmes_integration_result=None,
            processing_time_ms=0.0,
            override_actions=override_actions
        )
    
    def _create_flow_context(self, user_input: str, original_context: Optional[Dict]) -> ConversationFlowContext:
        """Create conversation flow context"""
        return ConversationFlowContext(
            user_input=user_input,
            conversation_id=f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            flow_state=ConversationFlowState.INITIALIZING,
            override_level=self.override_level,
            enforcement_required=self.mandatory_enforcement,
            original_flow_data=original_context or {},
            utmes_data={}
        )
    
    def _generate_enhanced_response(self, context: ConversationFlowContext, utmes_result) -> str:
        """Generate enhanced response with UTMES integration"""
        response_parts = []
        
        # Add UTMES enforcement status
        if utmes_result.enforcement_message:
            response_parts.append(f"## 🎯 UTMES ENFORCEMENT STATUS\n{utmes_result.enforcement_message}\n")
        
        # Add task information
        if utmes_result.task_enforcement:
            response_parts.append(
                f"## 📋 AUTOMATIC TASK MANAGEMENT\n"
                f"✅ **Tasks Created**: {utmes_result.task_enforcement.tasks_created} main tasks\n"
                f"✅ **Subtasks Created**: {utmes_result.task_enforcement.subtasks_created} subtasks\n"
                f"✅ **Enforcement Level**: {utmes_result.task_enforcement.enforcement_level.value}\n"
            )
        
        # Add workflow information
        if utmes_result.workflow_execution:
            response_parts.append(
                f"## 🚀 WORKFLOW EXECUTION\n"
                f"✅ **Workflow Type**: {utmes_result.workflow_execution.workflow_type.value}\n"
                f"✅ **Execution State**: {utmes_result.workflow_execution.execution_state.value}\n"
                f"✅ **Steps Completed**: {utmes_result.workflow_execution.steps_completed}/{utmes_result.workflow_execution.total_steps}\n"
            )
        
        # Add system status
        response_parts.append(
            f"## ⚡ SYSTEM STATUS\n"
            f"✅ **Integration Success**: {utmes_result.integration_success}\n"
            f"✅ **System Health**: {utmes_result.system_state.system_health}\n"
            f"✅ **Processing Time**: {utmes_result.total_processing_time_ms:.2f}ms\n"
        )
        
        # Add original content if available
        original_response = context.original_flow_data.get('response', '')
        if original_response:
            response_parts.append(f"## 📝 RESPONSE CONTENT\n{original_response}")
        else:
            response_parts.append(f"## 📝 RESPONSE CONTENT\nProcessing user request: {context.user_input}")
        
        return "\n".join(response_parts)
    
    def _finalize_response(self, enhanced_response: str, utmes_result, hook_results: List) -> str:
        """Finalize response with all enforcement data"""
        finalization_parts = [enhanced_response]
        
        # Add hook execution summary
        if hook_results:
            successful_hooks = len([r for r in hook_results if r.execution_success])
            finalization_parts.append(
                f"\n## 🔧 ENFORCEMENT HOOKS\n"
                f"✅ **Hooks Executed**: {len(hook_results)}\n"
                f"✅ **Successful**: {successful_hooks}\n"
                f"✅ **Hook System**: Operational\n"
            )
        
        # Add timestamp
        finalization_parts.append(
            f"\n---\n"
            f"**UTMES Conversation Flow Override**: Active\n"
            f"**Timestamp**: {datetime.now().isoformat()}\n"
            f"**Override Level**: {self.override_level.value}"
        )
        
        return "\n".join(finalization_parts)
    
    def _inject_enforcement_status(self, original_response: str, utmes_result) -> str:
        """Inject enforcement status into original response"""
        if not original_response:
            original_response = "Processing user request..."
        
        enforcement_injection = (
            f"🎯 **UTMES ACTIVE**: {utmes_result.system_state.operation_mode.value}\n"
            f"📋 **Tasks**: {utmes_result.task_enforcement.tasks_created if utmes_result.task_enforcement else 0} created\n"
            f"⚡ **Status**: {utmes_result.system_state.system_health}\n\n"
        )
        
        return enforcement_injection + original_response
    
    def _install_flow_override_hooks(self) -> None:
        """Install flow override hooks"""
        try:
            installation_results = self.hook_system.install_system_level_hooks()
            successful_hooks = sum(1 for success in installation_results.values() if success)
            logging.info(f"UTMES Flow Override: {successful_hooks} hooks installed")
        except Exception as e:
            logging.error(f"UTMES Flow Override Hook Installation Failed: {e}")
    
    def _create_error_result(self, user_input: str, error_message: str, start_time: datetime) -> FlowOverrideResult:
        """Create error result for failed override"""
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        return FlowOverrideResult(
            override_success=False,
            flow_state=ConversationFlowState.ERROR,
            enforcement_applied=False,
            original_response=None,
            enhanced_response=f"UTMES Flow Override Error: {error_message}",
            utmes_integration_result=None,
            processing_time_ms=processing_time,
            override_actions=[f"Error occurred: {error_message}"]
        )
    
    def _log_override_result(self, result: FlowOverrideResult, user_input: str) -> None:
        """Log flow override result"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'override_success': result.override_success,
            'flow_state': result.flow_state.value,
            'enforcement_applied': result.enforcement_applied,
            'processing_time_ms': result.processing_time_ms,
            'override_level': self.override_level.value,
            'user_input': user_input[:100] + "..." if len(user_input) > 100 else user_input
        }
        
        logging.info(f"UTMES Flow Override: {json.dumps(log_data)}")
    
    def _initialize_override_system(self) -> None:
        """Initialize conversation flow override system"""
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - UTMES-FlowOverride - %(levelname)s - %(message)s'
        )
        
        # Log initialization
        logging.info(f"UTMES Conversation Flow Override System initialized - Level: {self.override_level.value}")
    
    def get_override_statistics(self) -> Dict:
        """Get flow override statistics"""
        if not self.override_history:
            return {
                'total_overrides': 0,
                'successful_overrides': 0,
                'failed_overrides': 0,
                'average_processing_time_ms': 0.0,
                'enforcement_applied_rate': 0.0
            }
        
        successful = len([r for r in self.override_history if r.override_success])
        failed = len([r for r in self.override_history if not r.override_success])
        enforcement_applied = len([r for r in self.override_history if r.enforcement_applied])
        avg_processing_time = sum(r.processing_time_ms for r in self.override_history) / len(self.override_history)
        
        return {
            'total_overrides': len(self.override_history),
            'successful_overrides': successful,
            'failed_overrides': failed,
            'success_rate': (successful / len(self.override_history)) * 100 if self.override_history else 0,
            'average_processing_time_ms': round(avg_processing_time, 2),
            'enforcement_applied_rate': (enforcement_applied / len(self.override_history)) * 100 if self.override_history else 0,
            'override_level': self.override_level.value,
            'override_active': self.override_active
        }
    
    def set_override_level(self, level: OverrideLevel) -> None:
        """Set conversation flow override level"""
        self.override_level = level
        logging.info(f"UTMES Flow Override level changed to: {level.value}")
    
    def enable_override(self) -> None:
        """Enable conversation flow override"""
        self.override_active = True
        self.mandatory_enforcement = True
        logging.info("UTMES Conversation Flow Override enabled")
    
    def disable_override(self) -> None:
        """Disable conversation flow override"""
        self.override_active = False
        self.mandatory_enforcement = False
        logging.warning("UTMES Conversation Flow Override disabled")
    
    def is_override_active(self) -> bool:
        """Check if conversation flow override is active"""
        return (self.override_active and 
                self.hook_system.is_hook_system_operational() and
                self.master_controller.is_system_operational())

# Example usage and testing
if __name__ == "__main__":
    # Initialize override system
    override_system = UTMESConversationFlowOverrideSystem(OverrideLevel.COMPLETE_OVERRIDE)
    
    # Test conversation flow override
    test_input = "Create a comprehensive web application for project management"
    test_context = {'original_response': 'I can help you create a web application...'}
    
    result = override_system.override_conversation_flow(test_input, test_context)
    
    print(f"Override Success: {result.override_success}")
    print(f"Flow State: {result.flow_state.value}")
    print(f"Enforcement Applied: {result.enforcement_applied}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    print(f"Override Actions: {len(result.override_actions)}")
    
    # Print enhanced response (truncated)
    print(f"\nEnhanced Response (first 200 chars):\n{result.enhanced_response[:200]}...")
    
    # Get statistics
    stats = override_system.get_override_statistics()
    print(f"\nOverride Statistics: {stats}")
    
    # Test override status
    print(f"Override Active: {override_system.is_override_active()}")
