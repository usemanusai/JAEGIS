#!/usr/bin/env python3
"""
Master UTMES Integration Controller
Central controller that coordinates all UTMES enforcement engines and integrates them into system architecture
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - System architecture integration
"""

import json
import logging
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Import all UTMES enforcement engines
from input_analysis_algorithm import UTMESInputAnalyzer, InputAnalysisResult
from automatic_task_generation_system import UTMESTaskGenerator, TaskGenerationResult
from task_creation_enforcement import UTMESTaskCreationEnforcer, EnforcementResult
from conversation_flow_integration import UTMESConversationFlowIntegrator, IntegrationResult
from workflow_auto_execution_engine import UTMESWorkflowAutoExecutor, WorkflowExecutionResult
from mandatory_continuation_engine import UTMESMandatoryContinuationEngine, ContinuationEnforcementResult, TaskContinuationContext

# UTMES Centralized Logging Integration
from utmes_centralized_logging_manager import (
    get_utmes_logger, log_critical_issue, perform_system_health_check,
    LoggerType, LogLevel
)

class UTMESOperationMode(Enum):
    """UTMES operation modes"""
    FULL_ENFORCEMENT = "FULL_ENFORCEMENT"
    TASK_ONLY = "TASK_ONLY"
    WORKFLOW_ONLY = "WORKFLOW_ONLY"
    MONITORING_ONLY = "MONITORING_ONLY"
    DISABLED = "DISABLED"

class SystemIntegrationLevel(Enum):
    """Levels of system integration"""
    ARCHITECTURE_CORE = "ARCHITECTURE_CORE"
    CONVERSATION_FLOW = "CONVERSATION_FLOW"
    RESPONSE_GENERATION = "RESPONSE_GENERATION"
    USER_INTERACTION = "USER_INTERACTION"

@dataclass
class UTMESSystemState:
    """Current state of UTMES system"""
    operation_mode: UTMESOperationMode
    integration_level: SystemIntegrationLevel
    enforcement_active: bool
    automatic_execution: bool
    task_management_active: bool
    workflow_execution_active: bool
    continuation_enforcement_active: bool
    system_health: str
    last_activity_timestamp: str

@dataclass
class UTMESIntegrationResult:
    """Result of complete UTMES integration"""
    system_state: UTMESSystemState
    input_analysis: Optional[InputAnalysisResult]
    task_generation: Optional[TaskGenerationResult]
    task_enforcement: Optional[EnforcementResult]
    workflow_execution: Optional[WorkflowExecutionResult]
    continuation_enforcement: Optional[ContinuationEnforcementResult]
    integration_success: bool
    total_processing_time_ms: float
    enforcement_message: str
    system_response: Dict

class MasterUTMESIntegrationController:
    """
    Master UTMES Integration Controller
    Coordinates all UTMES enforcement engines and system integration
    """
    
    def __init__(self, task_management_tools: Optional[Dict[str, Callable]] = None,
                 operation_mode: UTMESOperationMode = UTMESOperationMode.FULL_ENFORCEMENT):

        # Initialize centralized logger
        self.logger = get_utmes_logger(LoggerType.MASTER_CONTROLLER, 'MasterController')

        # Initialize all UTMES enforcement engines
        self.input_analyzer = UTMESInputAnalyzer()
        self.task_generator = UTMESTaskGenerator()
        self.task_enforcer = UTMESTaskCreationEnforcer(task_management_tools)
        self.conversation_integrator = UTMESConversationFlowIntegrator(task_management_tools)
        self.workflow_executor = UTMESWorkflowAutoExecutor()
        self.continuation_engine = UTMESMandatoryContinuationEngine(task_management_tools)
        
        # System configuration
        self.operation_mode = operation_mode
        self.task_management_tools = task_management_tools or {}
        self.integration_level = SystemIntegrationLevel.ARCHITECTURE_CORE
        
        # System state
        self.system_state = UTMESSystemState(
            operation_mode=operation_mode,
            integration_level=self.integration_level,
            enforcement_active=True,
            automatic_execution=True,
            task_management_active=True,
            workflow_execution_active=True,
            continuation_enforcement_active=True,
            system_health="OPERATIONAL",
            last_activity_timestamp=datetime.now().isoformat()
        )
        
        # Integration history
        self.integration_history = []
        self.active_tasks = {}
        
        # Initialize controller
        self._initialize_controller()
    
    def process_user_input_with_full_enforcement(self, user_input: str, 
                                               conversation_context: Optional[Dict] = None) -> UTMESIntegrationResult:
        """
        MAIN INTEGRATION FUNCTION
        Processes user input with complete UTMES enforcement integration
        
        Args:
            user_input: Raw user input string
            conversation_context: Optional conversation context
            
        Returns:
            UTMESIntegrationResult with complete enforcement results
        """
        start_time = datetime.now()
        
        try:
            # Step 1: Initialize integration result
            integration_result = UTMESIntegrationResult(
                system_state=self.system_state,
                input_analysis=None,
                task_generation=None,
                task_enforcement=None,
                workflow_execution=None,
                continuation_enforcement=None,
                integration_success=False,
                total_processing_time_ms=0.0,
                enforcement_message="",
                system_response={}
            )
            
            # Step 2: Update system state
            self._update_system_state()
            
            # Step 3: Execute full UTMES enforcement pipeline
            if self.operation_mode != UTMESOperationMode.DISABLED:
                integration_result = self._execute_full_enforcement_pipeline(user_input, integration_result, conversation_context)
            else:
                integration_result = self._execute_disabled_mode(user_input, integration_result)
            
            # Step 4: Calculate processing time
            end_time = datetime.now()
            integration_result.total_processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Step 5: Generate system response
            integration_result.system_response = self._generate_system_response(integration_result, user_input)
            
            # Step 6: Log integration result
            self._log_integration_result(integration_result, user_input)
            
            # Step 7: Store in history
            self.integration_history.append(integration_result)
            
            return integration_result
            
        except Exception as e:
            # Handle integration errors
            error_result = self._create_error_result(user_input, str(e), start_time)
            self.integration_history.append(error_result)
            return error_result
    
    def _execute_full_enforcement_pipeline(self, user_input: str, result: UTMESIntegrationResult,
                                         context: Optional[Dict]) -> UTMESIntegrationResult:
        """Execute complete UTMES enforcement pipeline"""
        
        # Step 1: Input Analysis (Always executed)
        self.logger.info("UTMES: Executing input analysis")
        result.input_analysis = self.input_analyzer.analyze_user_input(user_input)
        
        # Step 2: Task Generation and Enforcement
        if self.operation_mode in [UTMESOperationMode.FULL_ENFORCEMENT, UTMESOperationMode.TASK_ONLY]:
            self.logger.info("UTMES: Executing task generation and enforcement")
            
            # Generate tasks
            result.task_generation = self.task_generator.generate_tasks_from_input(user_input)
            
            # Enforce task creation
            if result.task_generation and self.system_state.task_management_active:
                result.task_enforcement = self.task_enforcer.enforce_task_creation(user_input, force_creation=True)
                
                # Update active tasks registry
                if result.task_enforcement.status.value == "ENFORCED":
                    self._update_active_tasks(result.task_generation)
        
        # Step 3: Workflow Execution
        if self.operation_mode in [UTMESOperationMode.FULL_ENFORCEMENT, UTMESOperationMode.WORKFLOW_ONLY]:
            self.logger.info("UTMES: Executing workflow auto-execution")
            
            if self.system_state.workflow_execution_active:
                result.workflow_execution = self.workflow_executor.auto_execute_workflow(user_input, force_execution=True)
        
        # Step 4: Continuation Enforcement
        if self.operation_mode == UTMESOperationMode.FULL_ENFORCEMENT:
            self.logger.info("UTMES: Executing continuation enforcement")
            
            if self.system_state.continuation_enforcement_active and self.active_tasks:
                # Convert active tasks to continuation contexts
                continuation_contexts = self._convert_to_continuation_contexts()
                result.continuation_enforcement = self.continuation_engine.enforce_task_continuation(continuation_contexts)
        
        # Step 5: Determine integration success
        result.integration_success = self._determine_integration_success(result)
        
        # Step 6: Generate enforcement message
        result.enforcement_message = self._generate_enforcement_message(result)
        
        return result
    
    def _execute_disabled_mode(self, user_input: str, result: UTMESIntegrationResult) -> UTMESIntegrationResult:
        """Execute in disabled mode (minimal processing)"""
        result.integration_success = False
        result.enforcement_message = "UTMES enforcement is currently disabled"
        result.system_response = {
            'utmes_status': 'DISABLED',
            'message': 'UTMES enforcement is disabled - no automatic task management active',
            'user_input': user_input
        }
        return result
    
    def _update_system_state(self) -> None:
        """Update current system state"""
        self.system_state.last_activity_timestamp = datetime.now().isoformat()
        
        # Update component states
        self.system_state.enforcement_active = (
            self.task_enforcer.enforcement_active and
            self.workflow_executor.is_auto_execution_active() and
            self.continuation_engine.is_continuation_enforcement_active()
        )
        
        # Update system health
        if self.system_state.enforcement_active:
            self.system_state.system_health = "OPERATIONAL"
        else:
            self.system_state.system_health = "DEGRADED"
    
    def _update_active_tasks(self, task_generation: TaskGenerationResult) -> None:
        """Update active tasks registry"""
        for main_task in task_generation.main_tasks:
            self.active_tasks[main_task.task_id] = {
                'task_context': main_task,
                'created_timestamp': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'status': 'ACTIVE'
            }
    
    def _convert_to_continuation_contexts(self) -> List[TaskContinuationContext]:
        """Convert active tasks to continuation contexts"""
        continuation_contexts = []
        
        for task_id, task_data in self.active_tasks.items():
            task_context = task_data['task_context']
            
            # Create continuation context
            continuation_context = TaskContinuationContext(
                task_id=task_context.task_id,
                task_name=task_context.name,
                task_description=task_context.description,
                current_status=self._map_task_state_to_status(task_context.state),
                priority_level=task_context.priority.value,
                created_timestamp=task_context.created_timestamp,
                last_activity_timestamp=task_data['last_activity'],
                completion_percentage=self._estimate_completion_percentage(task_context),
                deliverables_completed=[],
                deliverables_remaining=task_context.deliverables,
                dependencies=task_context.dependencies,
                success_criteria=task_context.success_criteria
            )
            
            continuation_contexts.append(continuation_context)
        
        return continuation_contexts
    
    def _map_task_state_to_status(self, task_state) -> Any:
        """Map task state to continuation status"""
        # Import the TaskStatus enum from mandatory_continuation_engine
        from mandatory_continuation_engine import TaskStatus
        
        if task_state.value == "NOT_STARTED":
            return TaskStatus.NOT_STARTED
        elif task_state.value == "IN_PROGRESS":
            return TaskStatus.IN_PROGRESS
        elif task_state.value == "COMPLETE":
            return TaskStatus.COMPLETE
        else:
            return TaskStatus.NOT_STARTED
    
    def _estimate_completion_percentage(self, task_context) -> float:
        """Estimate task completion percentage"""
        # Simple estimation based on task state
        if task_context.state.value == "NOT_STARTED":
            return 0.0
        elif task_context.state.value == "IN_PROGRESS":
            return 25.0  # Assume 25% complete when in progress
        elif task_context.state.value == "COMPLETE":
            return 100.0
        else:
            return 0.0
    
    def _determine_integration_success(self, result: UTMESIntegrationResult) -> bool:
        """Determine if integration was successful"""
        success_criteria = []
        
        # Input analysis must succeed
        success_criteria.append(result.input_analysis is not None)
        
        # Task enforcement should succeed if tasks were generated
        if result.task_generation:
            success_criteria.append(
                result.task_enforcement is not None and 
                result.task_enforcement.status.value in ["ENFORCED", "BYPASSED"]
            )
        
        # Workflow execution should succeed if workflow was triggered
        if result.workflow_execution:
            success_criteria.append(
                result.workflow_execution.execution_state.value in ["COMPLETED", "EXECUTING"]
            )
        
        # At least 80% of criteria must be met
        success_rate = sum(success_criteria) / len(success_criteria) if success_criteria else 0
        return success_rate >= 0.8
    
    def _generate_enforcement_message(self, result: UTMESIntegrationResult) -> str:
        """Generate comprehensive enforcement message"""
        message_parts = [
            f"🎯 UTMES MASTER CONTROLLER: {self.operation_mode.value}",
            f"⚡ SYSTEM STATUS: {self.system_state.system_health}",
            f"🔧 INTEGRATION LEVEL: {self.integration_level.value}"
        ]
        
        # Add component status
        if result.input_analysis:
            message_parts.append(f"📊 INPUT ANALYSIS: {result.input_analysis.input_type.value} detected")
        
        if result.task_enforcement:
            message_parts.append(f"📋 TASK ENFORCEMENT: {result.task_enforcement.status.value} - {result.task_enforcement.tasks_created} tasks created")
        
        if result.workflow_execution:
            message_parts.append(f"🚀 WORKFLOW EXECUTION: {result.workflow_execution.execution_state.value}")
        
        if result.continuation_enforcement:
            message_parts.append(f"🔄 CONTINUATION: {result.continuation_enforcement.tasks_monitored} tasks monitored")
        
        # Add integration success status
        if result.integration_success:
            message_parts.append("✅ INTEGRATION: Successful enforcement across all components")
        else:
            message_parts.append("⚠️ INTEGRATION: Partial enforcement - some components may need attention")
        
        return "\n".join(message_parts)
    
    def _generate_system_response(self, result: UTMESIntegrationResult, user_input: str) -> Dict:
        """Generate comprehensive system response"""
        response = {
            'utmes_master_controller': {
                'status': 'ACTIVE',
                'operation_mode': self.operation_mode.value,
                'integration_level': self.integration_level.value,
                'system_health': self.system_state.system_health,
                'integration_success': result.integration_success,
                'processing_time_ms': result.total_processing_time_ms
            },
            'enforcement_components': {},
            'user_input_processed': user_input,
            'enforcement_message': result.enforcement_message,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add component results
        if result.input_analysis:
            response['enforcement_components']['input_analysis'] = {
                'input_type': result.input_analysis.input_type.value,
                'workflow_type': result.input_analysis.workflow_type.value if result.input_analysis.workflow_type else None,
                'complexity_score': result.input_analysis.complexity_score,
                'priority_level': result.input_analysis.priority_level.value
            }
        
        if result.task_enforcement:
            response['enforcement_components']['task_enforcement'] = {
                'status': result.task_enforcement.status.value,
                'tasks_created': result.task_enforcement.tasks_created,
                'subtasks_created': result.task_enforcement.subtasks_created,
                'enforcement_level': result.task_enforcement.enforcement_level.value
            }
        
        if result.workflow_execution:
            response['enforcement_components']['workflow_execution'] = {
                'workflow_type': result.workflow_execution.workflow_type.value,
                'execution_state': result.workflow_execution.execution_state.value,
                'steps_completed': result.workflow_execution.steps_completed,
                'success_rate': result.workflow_execution.success_rate
            }
        
        if result.continuation_enforcement:
            response['enforcement_components']['continuation_enforcement'] = {
                'continuation_state': result.continuation_enforcement.continuation_state.value,
                'tasks_monitored': result.continuation_enforcement.tasks_monitored,
                'tasks_enforced': result.continuation_enforcement.tasks_enforced,
                'abandonment_attempts_blocked': result.continuation_enforcement.abandonment_attempts_blocked
            }
        
        return response
    
    def _create_error_result(self, user_input: str, error_message: str, start_time: datetime) -> UTMESIntegrationResult:
        """Create error result for failed integration"""
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        return UTMESIntegrationResult(
            system_state=self.system_state,
            input_analysis=None,
            task_generation=None,
            task_enforcement=None,
            workflow_execution=None,
            continuation_enforcement=None,
            integration_success=False,
            total_processing_time_ms=processing_time,
            enforcement_message=f"UTMES integration failed: {error_message}",
            system_response={
                'error': True,
                'error_message': error_message,
                'user_input': user_input,
                'utmes_status': 'ERROR'
            }
        )
    
    def _log_integration_result(self, result: UTMESIntegrationResult, user_input: str) -> None:
        """Log integration result for monitoring"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'operation_mode': self.operation_mode.value,
            'integration_success': result.integration_success,
            'processing_time_ms': result.total_processing_time_ms,
            'system_health': self.system_state.system_health,
            'user_input': user_input[:100] + "..." if len(user_input) > 100 else user_input,
            'components_executed': {
                'input_analysis': result.input_analysis is not None,
                'task_enforcement': result.task_enforcement is not None,
                'workflow_execution': result.workflow_execution is not None,
                'continuation_enforcement': result.continuation_enforcement is not None
            }
        }
        
        self.logger.info(f"UTMES Master Controller: {json.dumps(log_data)}")
    
    def _initialize_controller(self) -> None:
        """Initialize master controller"""
        # Removed - using centralized logging

        # Log initialization
        self.logger.info(f"UTMES Master Integration Controller initialized - Mode: {self.operation_mode.value}")
    
    def get_system_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        if not self.integration_history:
            return {
                'total_integrations': 0,
                'successful_integrations': 0,
                'failed_integrations': 0,
                'average_processing_time_ms': 0.0,
                'system_health': self.system_state.system_health,
                'active_tasks_count': len(self.active_tasks)
            }
        
        successful = len([r for r in self.integration_history if r.integration_success])
        failed = len([r for r in self.integration_history if not r.integration_success])
        avg_processing_time = sum(r.total_processing_time_ms for r in self.integration_history) / len(self.integration_history)
        
        return {
            'total_integrations': len(self.integration_history),
            'successful_integrations': successful,
            'failed_integrations': failed,
            'success_rate': (successful / len(self.integration_history)) * 100 if self.integration_history else 0,
            'average_processing_time_ms': round(avg_processing_time, 2),
            'system_health': self.system_state.system_health,
            'operation_mode': self.operation_mode.value,
            'active_tasks_count': len(self.active_tasks),
            'enforcement_components_active': {
                'task_management': self.system_state.task_management_active,
                'workflow_execution': self.system_state.workflow_execution_active,
                'continuation_enforcement': self.system_state.continuation_enforcement_active
            }
        }
    
    def set_operation_mode(self, mode: UTMESOperationMode) -> None:
        """Set UTMES operation mode"""
        self.operation_mode = mode
        self.system_state.operation_mode = mode
        self.logger.info(f"UTMES operation mode changed to: {mode.value}")
    
    def is_system_operational(self) -> bool:
        """Check if UTMES system is fully operational"""
        return (self.system_state.system_health == "OPERATIONAL" and
                self.system_state.enforcement_active and
                self.operation_mode != UTMESOperationMode.DISABLED)

# Example usage and testing
if __name__ == "__main__":
    # Mock task management tools for testing
    def mock_add_tasks(params):
        print(f"Mock: Creating {len(params['tasks'])} tasks")
        return {"created": len(params['tasks'])}
    
    def mock_update_tasks(params):
        print(f"Mock: Updating {len(params['tasks'])} tasks")
        return {"updated": len(params['tasks'])}
    
    tools = {"add_tasks": mock_add_tasks, "update_tasks": mock_update_tasks}
    controller = MasterUTMESIntegrationController(tools, UTMESOperationMode.FULL_ENFORCEMENT)
    
    # Test full enforcement integration
    test_input = "Create a comprehensive web application for project management with user authentication, task tracking, and real-time collaboration features"
    result = controller.process_user_input_with_full_enforcement(test_input)
    
    print(f"Integration Success: {result.integration_success}")
    print(f"System Health: {result.system_state.system_health}")
    print(f"Processing Time: {result.total_processing_time_ms:.2f}ms")
    print(f"Operation Mode: {result.system_state.operation_mode.value}")
    
    # Print enforcement message
    print(f"\nEnforcement Message:\n{result.enforcement_message}")
    
    # Get system statistics
    stats = controller.get_system_statistics()
    print(f"\nSystem Statistics: {stats}")
    
    # Test system operational status
    print(f"System Operational: {controller.is_system_operational()}")
