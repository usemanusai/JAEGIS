#!/usr/bin/env python3
"""
UTMES System-Level Enforcement Hooks
Implements system-level hooks that automatically trigger UTMES enforcement for every user interaction
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - System architecture level integration
"""

import json
import logging
import functools
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Import Master UTMES Integration Controller
from master_utmes_integration_controller import MasterUTMESIntegrationController, UTMESOperationMode, UTMESIntegrationResult

class HookType(Enum):
    """Types of system-level hooks"""
    PRE_PROCESSING = "PRE_PROCESSING"
    POST_PROCESSING = "POST_PROCESSING"
    INPUT_VALIDATION = "INPUT_VALIDATION"
    RESPONSE_GENERATION = "RESPONSE_GENERATION"
    ERROR_HANDLING = "ERROR_HANDLING"

class HookPriority(Enum):
    """Priority levels for hook execution"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class SystemHook:
    """Represents a system-level enforcement hook"""
    hook_id: str
    hook_type: HookType
    priority: HookPriority
    hook_function: Callable
    description: str
    enabled: bool
    execution_count: int
    last_execution: Optional[str]

@dataclass
class HookExecutionResult:
    """Result of hook execution"""
    hook_id: str
    execution_success: bool
    execution_time_ms: float
    result_data: Dict
    error_message: Optional[str]
    timestamp: str

class UTMESSystemLevelEnforcementHooks:
    """
    UTMES System-Level Enforcement Hooks
    Implements hooks that automatically trigger UTMES enforcement for every user interaction
    """
    
    def __init__(self, master_controller: Optional[MasterUTMESIntegrationController] = None):
        # Initialize master controller
        self.master_controller = master_controller or MasterUTMESIntegrationController()
        
        # Hook registry
        self.registered_hooks: Dict[str, SystemHook] = {}
        self.hook_execution_history: List[HookExecutionResult] = []
        
        # Hook system state
        self.hooks_enabled = True
        self.automatic_enforcement = True
        self.bypass_prevention_active = True
        
        # Initialize system hooks
        self._initialize_system_hooks()
        
        # Hook system statistics
        self.total_hook_executions = 0
        self.successful_executions = 0
        self.failed_executions = 0
        
        # Initialize hook system
        self._initialize_hook_system()
    
    def install_system_level_hooks(self) -> Dict[str, bool]:
        """
        MAIN HOOK INSTALLATION FUNCTION
        Installs all system-level hooks for automatic UTMES enforcement
        
        Returns:
            Dict mapping hook IDs to installation success status
        """
        installation_results = {}
        
        try:
            # Install pre-processing hooks
            installation_results.update(self._install_pre_processing_hooks())
            
            # Install post-processing hooks
            installation_results.update(self._install_post_processing_hooks())
            
            # Install input validation hooks
            installation_results.update(self._install_input_validation_hooks())
            
            # Install response generation hooks
            installation_results.update(self._install_response_generation_hooks())
            
            # Install error handling hooks
            installation_results.update(self._install_error_handling_hooks())
            
            # Log installation results
            self._log_hook_installation(installation_results)
            
            return installation_results
            
        except Exception as e:
            logging.error(f"UTMES Hook Installation Failed: {e}")
            return {"error": False, "message": str(e)}
    
    def execute_hooks(self, hook_type: HookType, context: Dict) -> List[HookExecutionResult]:
        """
        Execute all hooks of specified type
        
        Args:
            hook_type: Type of hooks to execute
            context: Execution context data
            
        Returns:
            List of hook execution results
        """
        if not self.hooks_enabled:
            return []
        
        # Get hooks of specified type
        type_hooks = [hook for hook in self.registered_hooks.values() 
                     if hook.hook_type == hook_type and hook.enabled]
        
        # Sort by priority
        type_hooks.sort(key=lambda h: h.priority.value)
        
        execution_results = []
        
        for hook in type_hooks:
            try:
                result = self._execute_single_hook(hook, context)
                execution_results.append(result)
                
                # Update hook statistics
                hook.execution_count += 1
                hook.last_execution = datetime.now().isoformat()
                
                if result.execution_success:
                    self.successful_executions += 1
                else:
                    self.failed_executions += 1
                    
            except Exception as e:
                error_result = HookExecutionResult(
                    hook_id=hook.hook_id,
                    execution_success=False,
                    execution_time_ms=0.0,
                    result_data={},
                    error_message=str(e),
                    timestamp=datetime.now().isoformat()
                )
                execution_results.append(error_result)
                self.failed_executions += 1
        
        self.total_hook_executions += len(execution_results)
        self.hook_execution_history.extend(execution_results)
        
        return execution_results
    
    def _execute_single_hook(self, hook: SystemHook, context: Dict) -> HookExecutionResult:
        """Execute a single hook with timing and error handling"""
        start_time = datetime.now()
        
        try:
            # Execute hook function
            result_data = hook.hook_function(context)
            
            # Calculate execution time
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds() * 1000
            
            return HookExecutionResult(
                hook_id=hook.hook_id,
                execution_success=True,
                execution_time_ms=execution_time,
                result_data=result_data or {},
                error_message=None,
                timestamp=start_time.isoformat()
            )
            
        except Exception as e:
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds() * 1000
            
            return HookExecutionResult(
                hook_id=hook.hook_id,
                execution_success=False,
                execution_time_ms=execution_time,
                result_data={},
                error_message=str(e),
                timestamp=start_time.isoformat()
            )
    
    def _install_pre_processing_hooks(self) -> Dict[str, bool]:
        """Install pre-processing hooks"""
        hooks = {
            "utmes_input_analyzer": SystemHook(
                hook_id="utmes_input_analyzer",
                hook_type=HookType.PRE_PROCESSING,
                priority=HookPriority.CRITICAL,
                hook_function=self._hook_input_analysis,
                description="Automatically analyze user input for UTMES enforcement",
                enabled=True,
                execution_count=0,
                last_execution=None
            ),
            "automatic_task_injector": SystemHook(
                hook_id="automatic_task_injector",
                hook_type=HookType.PRE_PROCESSING,
                priority=HookPriority.CRITICAL,
                hook_function=self._hook_automatic_task_injection,
                description="Automatically inject tasks based on user input",
                enabled=True,
                execution_count=0,
                last_execution=None
            ),
            "workflow_auto_trigger": SystemHook(
                hook_id="workflow_auto_trigger",
                hook_type=HookType.PRE_PROCESSING,
                priority=HookPriority.HIGH,
                hook_function=self._hook_workflow_auto_trigger,
                description="Automatically trigger appropriate workflows",
                enabled=True,
                execution_count=0,
                last_execution=None
            )
        }
        
        installation_results = {}
        for hook_id, hook in hooks.items():
            try:
                self.registered_hooks[hook_id] = hook
                installation_results[hook_id] = True
                logging.info(f"UTMES Hook Installed: {hook_id}")
            except Exception as e:
                installation_results[hook_id] = False
                logging.error(f"UTMES Hook Installation Failed: {hook_id} - {e}")
        
        return installation_results
    
    def _install_post_processing_hooks(self) -> Dict[str, bool]:
        """Install post-processing hooks"""
        hooks = {
            "continuation_enforcer": SystemHook(
                hook_id="continuation_enforcer",
                hook_type=HookType.POST_PROCESSING,
                priority=HookPriority.CRITICAL,
                hook_function=self._hook_continuation_enforcement,
                description="Enforce task continuation and prevent abandonment",
                enabled=True,
                execution_count=0,
                last_execution=None
            ),
            "enforcement_validator": SystemHook(
                hook_id="enforcement_validator",
                hook_type=HookType.POST_PROCESSING,
                priority=HookPriority.HIGH,
                hook_function=self._hook_enforcement_validation,
                description="Validate that enforcement was successful",
                enabled=True,
                execution_count=0,
                last_execution=None
            )
        }
        
        installation_results = {}
        for hook_id, hook in hooks.items():
            try:
                self.registered_hooks[hook_id] = hook
                installation_results[hook_id] = True
                logging.info(f"UTMES Hook Installed: {hook_id}")
            except Exception as e:
                installation_results[hook_id] = False
                logging.error(f"UTMES Hook Installation Failed: {hook_id} - {e}")
        
        return installation_results
    
    def _install_input_validation_hooks(self) -> Dict[str, bool]:
        """Install input validation hooks"""
        hooks = {
            "bypass_detector": SystemHook(
                hook_id="bypass_detector",
                hook_type=HookType.INPUT_VALIDATION,
                priority=HookPriority.CRITICAL,
                hook_function=self._hook_bypass_detection,
                description="Detect and prevent bypass attempts",
                enabled=True,
                execution_count=0,
                last_execution=None
            ),
            "input_sanitizer": SystemHook(
                hook_id="input_sanitizer",
                hook_type=HookType.INPUT_VALIDATION,
                priority=HookPriority.HIGH,
                hook_function=self._hook_input_sanitization,
                description="Sanitize input for security and enforcement",
                enabled=True,
                execution_count=0,
                last_execution=None
            )
        }
        
        installation_results = {}
        for hook_id, hook in hooks.items():
            try:
                self.registered_hooks[hook_id] = hook
                installation_results[hook_id] = True
                logging.info(f"UTMES Hook Installed: {hook_id}")
            except Exception as e:
                installation_results[hook_id] = False
                logging.error(f"UTMES Hook Installation Failed: {hook_id} - {e}")
        
        return installation_results
    
    def _install_response_generation_hooks(self) -> Dict[str, bool]:
        """Install response generation hooks"""
        hooks = {
            "enforcement_status_injector": SystemHook(
                hook_id="enforcement_status_injector",
                hook_type=HookType.RESPONSE_GENERATION,
                priority=HookPriority.CRITICAL,
                hook_function=self._hook_enforcement_status_injection,
                description="Inject enforcement status into all responses",
                enabled=True,
                execution_count=0,
                last_execution=None
            ),
            "task_status_reporter": SystemHook(
                hook_id="task_status_reporter",
                hook_type=HookType.RESPONSE_GENERATION,
                priority=HookPriority.HIGH,
                hook_function=self._hook_task_status_reporting,
                description="Report current task status in responses",
                enabled=True,
                execution_count=0,
                last_execution=None
            )
        }
        
        installation_results = {}
        for hook_id, hook in hooks.items():
            try:
                self.registered_hooks[hook_id] = hook
                installation_results[hook_id] = True
                logging.info(f"UTMES Hook Installed: {hook_id}")
            except Exception as e:
                installation_results[hook_id] = False
                logging.error(f"UTMES Hook Installation Failed: {hook_id} - {e}")
        
        return installation_results
    
    def _install_error_handling_hooks(self) -> Dict[str, bool]:
        """Install error handling hooks"""
        hooks = {
            "enforcement_recovery": SystemHook(
                hook_id="enforcement_recovery",
                hook_type=HookType.ERROR_HANDLING,
                priority=HookPriority.CRITICAL,
                hook_function=self._hook_enforcement_recovery,
                description="Recover from enforcement failures",
                enabled=True,
                execution_count=0,
                last_execution=None
            )
        }
        
        installation_results = {}
        for hook_id, hook in hooks.items():
            try:
                self.registered_hooks[hook_id] = hook
                installation_results[hook_id] = True
                logging.info(f"UTMES Hook Installed: {hook_id}")
            except Exception as e:
                installation_results[hook_id] = False
                logging.error(f"UTMES Hook Installation Failed: {hook_id} - {e}")
        
        return installation_results
    
    # Hook Implementation Functions
    def _hook_input_analysis(self, context: Dict) -> Dict:
        """Hook function for automatic input analysis"""
        user_input = context.get('user_input', '')
        if not user_input:
            return {'status': 'no_input', 'analysis': None}
        
        try:
            # Use master controller for input analysis
            result = self.master_controller.process_user_input_with_full_enforcement(user_input, context)
            return {
                'status': 'success',
                'analysis': result.input_analysis.__dict__ if result.input_analysis else None,
                'integration_success': result.integration_success
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _hook_automatic_task_injection(self, context: Dict) -> Dict:
        """Hook function for automatic task injection"""
        user_input = context.get('user_input', '')
        if not user_input:
            return {'status': 'no_input', 'tasks_created': 0}
        
        try:
            # Task injection is handled by master controller
            result = self.master_controller.process_user_input_with_full_enforcement(user_input, context)
            tasks_created = result.task_enforcement.tasks_created if result.task_enforcement else 0
            return {
                'status': 'success',
                'tasks_created': tasks_created,
                'enforcement_status': result.task_enforcement.status.value if result.task_enforcement else 'none'
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e), 'tasks_created': 0}
    
    def _hook_workflow_auto_trigger(self, context: Dict) -> Dict:
        """Hook function for automatic workflow triggering"""
        user_input = context.get('user_input', '')
        if not user_input:
            return {'status': 'no_input', 'workflow_triggered': False}
        
        try:
            result = self.master_controller.process_user_input_with_full_enforcement(user_input, context)
            workflow_triggered = result.workflow_execution is not None
            return {
                'status': 'success',
                'workflow_triggered': workflow_triggered,
                'workflow_type': result.workflow_execution.workflow_type.value if result.workflow_execution else None
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e), 'workflow_triggered': False}
    
    def _hook_continuation_enforcement(self, context: Dict) -> Dict:
        """Hook function for continuation enforcement"""
        try:
            # Continuation enforcement is handled by master controller
            result = context.get('utmes_result')
            if result and result.continuation_enforcement:
                return {
                    'status': 'success',
                    'tasks_monitored': result.continuation_enforcement.tasks_monitored,
                    'tasks_enforced': result.continuation_enforcement.tasks_enforced,
                    'abandonment_blocked': result.continuation_enforcement.abandonment_attempts_blocked
                }
            return {'status': 'no_continuation_needed'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _hook_enforcement_validation(self, context: Dict) -> Dict:
        """Hook function for enforcement validation"""
        try:
            result = context.get('utmes_result')
            if result:
                return {
                    'status': 'success',
                    'integration_success': result.integration_success,
                    'system_health': result.system_state.system_health,
                    'enforcement_active': result.system_state.enforcement_active
                }
            return {'status': 'no_result_to_validate'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _hook_bypass_detection(self, context: Dict) -> Dict:
        """Hook function for bypass detection"""
        user_input = context.get('user_input', '').lower()
        
        bypass_indicators = [
            'skip tasks', 'no tasks', 'bypass', 'ignore tasks', 'without tasks',
            'don\'t create tasks', 'no task management', 'disable tasks', 'turn off utmes'
        ]
        
        detected_bypasses = [indicator for indicator in bypass_indicators if indicator in user_input]
        
        if detected_bypasses and self.bypass_prevention_active:
            return {
                'status': 'bypass_detected',
                'bypass_attempts': len(detected_bypasses),
                'indicators': detected_bypasses,
                'action': 'enforcement_increased'
            }
        
        return {'status': 'no_bypass_detected'}
    
    def _hook_input_sanitization(self, context: Dict) -> Dict:
        """Hook function for input sanitization"""
        user_input = context.get('user_input', '')
        
        # Basic sanitization (can be enhanced)
        sanitized_input = user_input.strip()
        
        return {
            'status': 'success',
            'original_length': len(user_input),
            'sanitized_length': len(sanitized_input),
            'sanitized_input': sanitized_input
        }
    
    def _hook_enforcement_status_injection(self, context: Dict) -> Dict:
        """Hook function for enforcement status injection"""
        try:
            result = context.get('utmes_result')
            if result:
                enforcement_status = {
                    'utmes_active': True,
                    'operation_mode': result.system_state.operation_mode.value,
                    'system_health': result.system_state.system_health,
                    'integration_success': result.integration_success,
                    'enforcement_message': result.enforcement_message
                }
                return {'status': 'success', 'enforcement_status': enforcement_status}
            return {'status': 'no_enforcement_data'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _hook_task_status_reporting(self, context: Dict) -> Dict:
        """Hook function for task status reporting"""
        try:
            result = context.get('utmes_result')
            if result and result.task_enforcement:
                task_status = {
                    'tasks_created': result.task_enforcement.tasks_created,
                    'subtasks_created': result.task_enforcement.subtasks_created,
                    'enforcement_level': result.task_enforcement.enforcement_level.value,
                    'enforcement_status': result.task_enforcement.status.value
                }
                return {'status': 'success', 'task_status': task_status}
            return {'status': 'no_task_data'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _hook_enforcement_recovery(self, context: Dict) -> Dict:
        """Hook function for enforcement recovery"""
        error = context.get('error')
        if error:
            try:
                # Attempt to recover enforcement
                logging.warning(f"UTMES Enforcement Recovery: {error}")
                
                # Re-enable enforcement if disabled
                self.hooks_enabled = True
                self.automatic_enforcement = True
                
                return {
                    'status': 'recovery_attempted',
                    'error': str(error),
                    'recovery_actions': ['hooks_re_enabled', 'enforcement_reactivated']
                }
            except Exception as e:
                return {'status': 'recovery_failed', 'error': str(e)}
        
        return {'status': 'no_recovery_needed'}
    
    def _initialize_system_hooks(self) -> None:
        """Initialize system hook registry"""
        self.registered_hooks = {}
        self.hook_execution_history = []
        logging.info("UTMES System Hooks initialized")
    
    def _log_hook_installation(self, results: Dict[str, bool]) -> None:
        """Log hook installation results"""
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        logging.info(f"UTMES Hook Installation: {successful}/{total} hooks installed successfully")
        
        for hook_id, success in results.items():
            if not success:
                logging.error(f"UTMES Hook Installation Failed: {hook_id}")
    
    def _initialize_hook_system(self) -> None:
        """Initialize hook system"""
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - UTMES-Hooks - %(levelname)s - %(message)s'
        )
        
        # Log initialization
        logging.info("UTMES System-Level Enforcement Hooks initialized")
    
    def get_hook_statistics(self) -> Dict:
        """Get hook system statistics"""
        return {
            'total_hooks_registered': len(self.registered_hooks),
            'enabled_hooks': len([h for h in self.registered_hooks.values() if h.enabled]),
            'total_executions': self.total_hook_executions,
            'successful_executions': self.successful_executions,
            'failed_executions': self.failed_executions,
            'success_rate': (self.successful_executions / self.total_hook_executions * 100) if self.total_hook_executions > 0 else 0,
            'hooks_enabled': self.hooks_enabled,
            'automatic_enforcement': self.automatic_enforcement,
            'bypass_prevention_active': self.bypass_prevention_active
        }
    
    def enable_all_hooks(self) -> None:
        """Enable all registered hooks"""
        for hook in self.registered_hooks.values():
            hook.enabled = True
        self.hooks_enabled = True
        logging.info("UTMES: All hooks enabled")
    
    def disable_all_hooks(self) -> None:
        """Disable all registered hooks"""
        for hook in self.registered_hooks.values():
            hook.enabled = False
        self.hooks_enabled = False
        logging.warning("UTMES: All hooks disabled")
    
    def is_hook_system_operational(self) -> bool:
        """Check if hook system is operational"""
        return (self.hooks_enabled and 
                len(self.registered_hooks) > 0 and
                any(hook.enabled for hook in self.registered_hooks.values()))

# Example usage and testing
if __name__ == "__main__":
    # Initialize hook system
    hook_system = UTMESSystemLevelEnforcementHooks()
    
    # Install all hooks
    installation_results = hook_system.install_system_level_hooks()
    print(f"Hook Installation Results: {installation_results}")
    
    # Test hook execution
    test_context = {
        'user_input': 'Create a web application for project management',
        'timestamp': datetime.now().isoformat()
    }
    
    # Execute pre-processing hooks
    pre_results = hook_system.execute_hooks(HookType.PRE_PROCESSING, test_context)
    print(f"Pre-processing hooks executed: {len(pre_results)}")
    
    # Get statistics
    stats = hook_system.get_hook_statistics()
    print(f"Hook System Statistics: {stats}")
    
    # Check operational status
    print(f"Hook System Operational: {hook_system.is_hook_system_operational()}")
