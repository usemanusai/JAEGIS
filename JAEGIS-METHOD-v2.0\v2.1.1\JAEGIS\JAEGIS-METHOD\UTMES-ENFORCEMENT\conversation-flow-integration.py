#!/usr/bin/env python3
"""
UTMES Conversation Flow Integration System
Integrates automatic task injection into core conversation processing
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Core system integration
"""

import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Import from other UTMES components
from input_analysis_algorithm import UTMESInputAnalyzer, InputAnalysisResult
from automatic_task_generation_system import UTMESTaskGenerator, TaskGenerationResult
from task_creation_enforcement import UTMESTaskCreationEnforcer, EnforcementResult

class ConversationState(Enum):
    """States of conversation processing"""
    INITIALIZING = "INITIALIZING"
    PROCESSING_INPUT = "PROCESSING_INPUT"
    ANALYZING_REQUIREMENTS = "ANALYZING_REQUIREMENTS"
    GENERATING_TASKS = "GENERATING_TASKS"
    ENFORCING_CREATION = "ENFORCING_CREATION"
    EXECUTING_WORKFLOW = "EXECUTING_WORKFLOW"
    GENERATING_RESPONSE = "GENERATING_RESPONSE"
    COMPLETE = "COMPLETE"

class IntegrationMode(Enum):
    """Modes of conversation flow integration"""
    FULL_INTEGRATION = "FULL_INTEGRATION"
    TASK_ONLY_INTEGRATION = "TASK_ONLY_INTEGRATION"
    MONITORING_ONLY = "MONITORING_ONLY"
    DISABLED = "DISABLED"

@dataclass
class ConversationContext:
    """Context for conversation processing"""
    user_input: str
    conversation_id: str
    session_id: str
    timestamp: str
    previous_tasks: List[Dict]
    conversation_history: List[Dict]
    user_preferences: Dict
    system_state: Dict

@dataclass
class IntegrationResult:
    """Result of conversation flow integration"""
    conversation_state: ConversationState
    input_analysis: Optional[InputAnalysisResult]
    task_generation: Optional[TaskGenerationResult]
    enforcement_result: Optional[EnforcementResult]
    workflow_triggered: bool
    response_data: Dict
    integration_timestamp: str
    processing_time_ms: float

class UTMESConversationFlowIntegrator:
    """
    UTMES Conversation Flow Integration System
    Integrates automatic task management into core conversation processing
    """
    
    def __init__(self, task_management_tools: Optional[Dict[str, Callable]] = None,
                 integration_mode: IntegrationMode = IntegrationMode.FULL_INTEGRATION):
        
        # Initialize UTMES components
        self.input_analyzer = UTMESInputAnalyzer()
        self.task_generator = UTMESTaskGenerator()
        self.task_enforcer = UTMESTaskCreationEnforcer(task_management_tools)
        
        # Integration configuration
        self.integration_mode = integration_mode
        self.task_management_tools = task_management_tools or {}
        
        # Integration state
        self.integration_active = True
        self.automatic_enforcement = True
        self.workflow_triggering_enabled = True
        
        # Processing history
        self.processing_history = []
        
        # Initialize integration
        self._initialize_integration()
    
    def process_user_input(self, user_input: str, context: Optional[ConversationContext] = None) -> IntegrationResult:
        """
        MAIN INTEGRATION FUNCTION
        Processes user input with full UTMES integration
        
        Args:
            user_input: Raw user input string
            context: Optional conversation context
            
        Returns:
            IntegrationResult with complete processing results
        """
        start_time = datetime.now()
        
        # Create default context if not provided
        if context is None:
            context = self._create_default_context(user_input)
        
        try:
            # Step 1: Initialize processing
            integration_result = IntegrationResult(
                conversation_state=ConversationState.INITIALIZING,
                input_analysis=None,
                task_generation=None,
                enforcement_result=None,
                workflow_triggered=False,
                response_data={},
                integration_timestamp=start_time.isoformat(),
                processing_time_ms=0.0
            )
            
            # Step 2: Process input if integration is active
            if self.integration_active and self.integration_mode != IntegrationMode.DISABLED:
                integration_result = self._process_with_integration(user_input, context, integration_result)
            else:
                integration_result = self._process_without_integration(user_input, context, integration_result)
            
            # Step 3: Calculate processing time
            end_time = datetime.now()
            integration_result.processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Step 4: Log processing result
            self._log_processing_result(integration_result, context)
            
            # Step 5: Update processing history
            self.processing_history.append(integration_result)
            
            return integration_result
            
        except Exception as e:
            # Handle processing errors
            error_result = self._create_error_result(user_input, context, str(e), start_time)
            self.processing_history.append(error_result)
            return error_result
    
    def _process_with_integration(self, user_input: str, context: ConversationContext, 
                                result: IntegrationResult) -> IntegrationResult:
        """Process user input with full UTMES integration"""
        
        # Step 1: Analyze user input
        result.conversation_state = ConversationState.ANALYZING_REQUIREMENTS
        result.input_analysis = self.input_analyzer.analyze_user_input(user_input)
        
        # Step 2: Generate tasks if required
        if self._should_generate_tasks(result.input_analysis, context):
            result.conversation_state = ConversationState.GENERATING_TASKS
            result.task_generation = self.task_generator.generate_tasks_from_input(user_input)
            
            # Step 3: Enforce task creation
            if self.automatic_enforcement and result.task_generation:
                result.conversation_state = ConversationState.ENFORCING_CREATION
                result.enforcement_result = self.task_enforcer.enforce_task_creation(user_input, force_creation=True)
        
        # Step 4: Trigger workflow if applicable
        if self.workflow_triggering_enabled and result.input_analysis and result.input_analysis.workflow_type:
            result.conversation_state = ConversationState.EXECUTING_WORKFLOW
            result.workflow_triggered = self._trigger_workflow(result.input_analysis.workflow_type, context)
        
        # Step 5: Generate response data
        result.conversation_state = ConversationState.GENERATING_RESPONSE
        result.response_data = self._generate_response_data(result, context)
        
        # Step 6: Mark as complete
        result.conversation_state = ConversationState.COMPLETE
        
        return result
    
    def _process_without_integration(self, user_input: str, context: ConversationContext,
                                   result: IntegrationResult) -> IntegrationResult:
        """Process user input without UTMES integration (fallback)"""
        result.conversation_state = ConversationState.PROCESSING_INPUT
        result.response_data = {
            'message': 'UTMES integration disabled - processing without automatic task management',
            'user_input': user_input,
            'integration_mode': self.integration_mode.value
        }
        result.conversation_state = ConversationState.COMPLETE
        return result
    
    def _should_generate_tasks(self, input_analysis: InputAnalysisResult, context: ConversationContext) -> bool:
        """Determine if tasks should be generated"""
        if self.integration_mode == IntegrationMode.MONITORING_ONLY:
            return False
        
        # Always generate tasks for project and implementation requests
        if input_analysis.input_type.value in ['project_request', 'implementation_request', 'problem_solving']:
            return True
        
        # Generate tasks for complex requests
        if input_analysis.complexity_score > 0.3:
            return True
        
        # Generate tasks if workflow is triggered
        if input_analysis.workflow_type:
            return True
        
        return False
    
    def _trigger_workflow(self, workflow_type, context: ConversationContext) -> bool:
        """Trigger appropriate workflow based on type"""
        try:
            workflow_config = {
                'workflow_type': workflow_type.value,
                'context': asdict(context),
                'timestamp': datetime.now().isoformat()
            }
            
            # Log workflow triggering
            logging.info(f"UTMES: Triggering workflow - {workflow_type.value}")
            
            # In a real implementation, this would trigger actual workflow execution
            # For now, we simulate successful workflow triggering
            return True
            
        except Exception as e:
            logging.error(f"UTMES: Workflow triggering failed - {e}")
            return False
    
    def _generate_response_data(self, result: IntegrationResult, context: ConversationContext) -> Dict:
        """Generate comprehensive response data"""
        response_data = {
            'utmes_status': 'ACTIVE_AND_INTEGRATED',
            'integration_mode': self.integration_mode.value,
            'conversation_state': result.conversation_state.value,
            'timestamp': result.integration_timestamp
        }
        
        # Add input analysis data
        if result.input_analysis:
            response_data['input_analysis'] = {
                'input_type': result.input_analysis.input_type.value,
                'workflow_type': result.input_analysis.workflow_type.value if result.input_analysis.workflow_type else None,
                'priority_level': result.input_analysis.priority_level.value,
                'complexity_score': result.input_analysis.complexity_score,
                'key_concepts': result.input_analysis.key_concepts,
                'deliverable_requirements': result.input_analysis.deliverable_requirements
            }
        
        # Add task generation data
        if result.task_generation:
            response_data['task_generation'] = {
                'total_tasks': result.task_generation.total_task_count,
                'total_subtasks': result.task_generation.total_subtask_count,
                'enforcement_level': result.task_generation.enforcement_level,
                'tasks_summary': [
                    {
                        'name': task.name,
                        'priority': task.priority.value,
                        'subtask_count': len(task.subtasks),
                        'deliverables': task.deliverables
                    }
                    for task in result.task_generation.main_tasks
                ]
            }
        
        # Add enforcement data
        if result.enforcement_result:
            response_data['enforcement'] = {
                'status': result.enforcement_result.status.value,
                'tasks_created': result.enforcement_result.tasks_created,
                'subtasks_created': result.enforcement_result.subtasks_created,
                'enforcement_level': result.enforcement_result.enforcement_level.value,
                'bypass_attempts': result.enforcement_result.bypass_attempts,
                'message': result.enforcement_result.enforcement_message
            }
        
        # Add workflow data
        if result.workflow_triggered:
            response_data['workflow'] = {
                'triggered': True,
                'workflow_type': result.input_analysis.workflow_type.value if result.input_analysis and result.input_analysis.workflow_type else 'unknown'
            }
        
        return response_data
    
    def _create_default_context(self, user_input: str) -> ConversationContext:
        """Create default conversation context"""
        return ConversationContext(
            user_input=user_input,
            conversation_id=f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            previous_tasks=[],
            conversation_history=[],
            user_preferences={},
            system_state={}
        )
    
    def _create_error_result(self, user_input: str, context: ConversationContext, 
                           error_message: str, start_time: datetime) -> IntegrationResult:
        """Create error result for failed processing"""
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        return IntegrationResult(
            conversation_state=ConversationState.COMPLETE,
            input_analysis=None,
            task_generation=None,
            enforcement_result=None,
            workflow_triggered=False,
            response_data={
                'error': True,
                'error_message': error_message,
                'user_input': user_input,
                'utmes_status': 'ERROR'
            },
            integration_timestamp=start_time.isoformat(),
            processing_time_ms=processing_time
        )
    
    def _log_processing_result(self, result: IntegrationResult, context: ConversationContext) -> None:
        """Log processing result for monitoring"""
        log_data = {
            'timestamp': result.integration_timestamp,
            'conversation_id': context.conversation_id,
            'session_id': context.session_id,
            'conversation_state': result.conversation_state.value,
            'processing_time_ms': result.processing_time_ms,
            'tasks_generated': result.task_generation.total_task_count if result.task_generation else 0,
            'workflow_triggered': result.workflow_triggered,
            'enforcement_status': result.enforcement_result.status.value if result.enforcement_result else 'none'
        }
        
        logging.info(f"UTMES Integration: {json.dumps(log_data)}")
    
    def _initialize_integration(self) -> None:
        """Initialize conversation flow integration"""
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - UTMES-Integration - %(levelname)s - %(message)s'
        )
        
        # Log initialization
        logging.info(f"UTMES Conversation Flow Integration initialized - Mode: {self.integration_mode.value}")
    
    def get_integration_statistics(self) -> Dict:
        """Get integration processing statistics"""
        if not self.processing_history:
            return {
                'total_processed': 0,
                'successful_integrations': 0,
                'failed_integrations': 0,
                'tasks_generated': 0,
                'workflows_triggered': 0,
                'average_processing_time_ms': 0.0
            }
        
        successful = len([r for r in self.processing_history if r.conversation_state == ConversationState.COMPLETE and not r.response_data.get('error')])
        failed = len([r for r in self.processing_history if r.response_data.get('error')])
        tasks_generated = sum(r.task_generation.total_task_count if r.task_generation else 0 for r in self.processing_history)
        workflows_triggered = len([r for r in self.processing_history if r.workflow_triggered])
        avg_processing_time = sum(r.processing_time_ms for r in self.processing_history) / len(self.processing_history)
        
        return {
            'total_processed': len(self.processing_history),
            'successful_integrations': successful,
            'failed_integrations': failed,
            'tasks_generated': tasks_generated,
            'workflows_triggered': workflows_triggered,
            'average_processing_time_ms': round(avg_processing_time, 2),
            'success_rate': (successful / len(self.processing_history)) * 100 if self.processing_history else 0
        }
    
    def set_integration_mode(self, mode: IntegrationMode) -> None:
        """Set integration mode"""
        self.integration_mode = mode
        logging.info(f"UTMES Integration mode changed to: {mode.value}")
    
    def is_integration_active(self) -> bool:
        """Check if integration is currently active"""
        return (self.integration_active and 
                self.integration_mode != IntegrationMode.DISABLED and
                self.task_enforcer.is_enforcement_active())

# Example usage and testing
if __name__ == "__main__":
    # Mock task management tools for testing
    def mock_add_tasks(params):
        print(f"Mock: Creating {len(params['tasks'])} tasks")
        return {"created": len(params['tasks'])}
    
    tools = {"add_tasks": mock_add_tasks}
    integrator = UTMESConversationFlowIntegrator(tools, IntegrationMode.FULL_INTEGRATION)
    
    # Test integration
    test_input = "Create a comprehensive web application for project management with user authentication and real-time collaboration"
    result = integrator.process_user_input(test_input)
    
    print(f"Conversation State: {result.conversation_state.value}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    print(f"Tasks Generated: {result.task_generation.total_task_count if result.task_generation else 0}")
    print(f"Workflow Triggered: {result.workflow_triggered}")
    print(f"Enforcement Status: {result.enforcement_result.status.value if result.enforcement_result else 'none'}")
    
    # Get statistics
    stats = integrator.get_integration_statistics()
    print(f"\nIntegration Statistics: {stats}")
    
    # Test integration status
    print(f"Integration Active: {integrator.is_integration_active()}")
