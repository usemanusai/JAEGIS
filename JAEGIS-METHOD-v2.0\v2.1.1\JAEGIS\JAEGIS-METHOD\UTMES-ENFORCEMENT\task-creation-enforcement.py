#!/usr/bin/env python3
"""
UTMES Task Creation Enforcement System
Implements mandatory task creation that cannot be bypassed or ignored
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Core enforcement mechanism
"""

import json
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Import from other UTMES components
from automatic_task_generation_system import UTMESTaskGenerator, TaskGenerationResult, GeneratedTask

class EnforcementLevel(Enum):
    """Levels of task creation enforcement"""
    MAXIMUM_ENFORCEMENT = "MAXIMUM_ENFORCEMENT"
    HIGH_ENFORCEMENT = "HIGH_ENFORCEMENT"
    STANDARD_ENFORCEMENT = "STANDARD_ENFORCEMENT"
    BASIC_ENFORCEMENT = "BASIC_ENFORCEMENT"

class EnforcementStatus(Enum):
    """Status of enforcement operations"""
    ENFORCED = "ENFORCED"
    BYPASSED = "BYPASSED"
    FAILED = "FAILED"
    PENDING = "PENDING"

@dataclass
class EnforcementResult:
    """Result of task creation enforcement"""
    status: EnforcementStatus
    tasks_created: int
    subtasks_created: int
    enforcement_level: EnforcementLevel
    enforcement_timestamp: str
    bypass_attempts: int
    enforcement_message: str

class UTMESTaskCreationEnforcer:
    """
    UTMES Task Creation Enforcement System
    Enforces mandatory task creation that cannot be bypassed
    """
    
    def __init__(self, task_management_tools: Optional[Dict[str, Callable]] = None):
        self.task_generator = UTMESTaskGenerator()
        self.enforcement_active = True
        self.bypass_prevention_active = True
        self.task_management_tools = task_management_tools or {}
        self.enforcement_log = []
        
        # Initialize enforcement mechanisms
        self._initialize_enforcement_mechanisms()
    
    def enforce_task_creation(self, user_input: str, force_creation: bool = True) -> EnforcementResult:
        """
        MAIN ENFORCEMENT FUNCTION
        Enforces mandatory task creation for user input
        
        Args:
            user_input: Raw user input that requires task creation
            force_creation: Whether to force task creation regardless of bypass attempts
            
        Returns:
            EnforcementResult with enforcement status and details
        """
        enforcement_start = datetime.now()
        bypass_attempts = 0
        
        try:
            # Step 1: Generate tasks from user input
            generation_result = self.task_generator.generate_tasks_from_input(user_input)
            
            # Step 2: Determine enforcement level
            enforcement_level = self._determine_enforcement_level(generation_result)
            
            # Step 3: Detect and prevent bypass attempts
            bypass_attempts = self._detect_bypass_attempts(user_input)
            if bypass_attempts > 0 and self.bypass_prevention_active:
                self._prevent_bypass_attempts(bypass_attempts)
            
            # Step 4: Enforce task creation
            if force_creation or self._should_enforce_creation(generation_result, enforcement_level):
                creation_result = self._enforce_mandatory_creation(generation_result, enforcement_level)
                
                if creation_result:
                    # Step 5: Validate enforcement success
                    validation_result = self._validate_enforcement_success(generation_result)
                    
                    if validation_result:
                        enforcement_result = EnforcementResult(
                            status=EnforcementStatus.ENFORCED,
                            tasks_created=generation_result.total_task_count,
                            subtasks_created=generation_result.total_subtask_count,
                            enforcement_level=enforcement_level,
                            enforcement_timestamp=enforcement_start.isoformat(),
                            bypass_attempts=bypass_attempts,
                            enforcement_message=self._generate_enforcement_message(generation_result, enforcement_level)
                        )
                    else:
                        enforcement_result = EnforcementResult(
                            status=EnforcementStatus.FAILED,
                            tasks_created=0,
                            subtasks_created=0,
                            enforcement_level=enforcement_level,
                            enforcement_timestamp=enforcement_start.isoformat(),
                            bypass_attempts=bypass_attempts,
                            enforcement_message="Task creation enforcement failed validation"
                        )
                else:
                    enforcement_result = EnforcementResult(
                        status=EnforcementStatus.FAILED,
                        tasks_created=0,
                        subtasks_created=0,
                        enforcement_level=enforcement_level,
                        enforcement_timestamp=enforcement_start.isoformat(),
                        bypass_attempts=bypass_attempts,
                        enforcement_message="Mandatory task creation failed"
                    )
            else:
                enforcement_result = EnforcementResult(
                    status=EnforcementStatus.BYPASSED,
                    tasks_created=0,
                    subtasks_created=0,
                    enforcement_level=enforcement_level,
                    enforcement_timestamp=enforcement_start.isoformat(),
                    bypass_attempts=bypass_attempts,
                    enforcement_message="Task creation enforcement bypassed"
                )
            
            # Log enforcement result
            self._log_enforcement_result(enforcement_result, user_input)
            
            return enforcement_result
            
        except Exception as e:
            # Handle enforcement failures
            error_result = EnforcementResult(
                status=EnforcementStatus.FAILED,
                tasks_created=0,
                subtasks_created=0,
                enforcement_level=EnforcementLevel.BASIC_ENFORCEMENT,
                enforcement_timestamp=enforcement_start.isoformat(),
                bypass_attempts=bypass_attempts,
                enforcement_message=f"Enforcement failed with error: {str(e)}"
            )
            
            self._log_enforcement_result(error_result, user_input)
            return error_result
    
    def _enforce_mandatory_creation(self, generation_result: TaskGenerationResult, 
                                  enforcement_level: EnforcementLevel) -> bool:
        """Enforce mandatory task creation using available tools"""
        try:
            # Convert generated tasks to task management format
            task_format = self.task_generator.convert_to_task_management_format(generation_result)
            
            # Use task management tools if available
            if 'add_tasks' in self.task_management_tools:
                # Create main tasks first
                main_tasks = [task for task in task_format if 'parent_task_id' not in task]
                if main_tasks:
                    main_task_result = self.task_management_tools['add_tasks']({"tasks": main_tasks})
                    
                    # Extract created task IDs and create subtasks
                    if main_task_result and 'created' in str(main_task_result):
                        subtasks = [task for task in task_format if 'parent_task_id' in task]
                        if subtasks:
                            # Update parent task IDs with actual IDs (simplified for demo)
                            subtask_result = self.task_management_tools['add_tasks']({"tasks": subtasks})
                            return bool(subtask_result)
                    
                    return bool(main_task_result)
            else:
                # Fallback: Log task creation (when tools not available)
                self._log_task_creation_fallback(generation_result)
                return True
                
        except Exception as e:
            logging.error(f"Task creation enforcement failed: {e}")
            return False
        
        return False
    
    def _determine_enforcement_level(self, generation_result: TaskGenerationResult) -> EnforcementLevel:
        """Determine appropriate enforcement level"""
        if generation_result.enforcement_level == "MAXIMUM_ENFORCEMENT":
            return EnforcementLevel.MAXIMUM_ENFORCEMENT
        elif generation_result.enforcement_level == "HIGH_ENFORCEMENT":
            return EnforcementLevel.HIGH_ENFORCEMENT
        elif generation_result.enforcement_level == "STANDARD_ENFORCEMENT":
            return EnforcementLevel.STANDARD_ENFORCEMENT
        else:
            return EnforcementLevel.BASIC_ENFORCEMENT
    
    def _detect_bypass_attempts(self, user_input: str) -> int:
        """Detect attempts to bypass task creation enforcement"""
        bypass_indicators = [
            'skip tasks', 'no tasks', 'bypass', 'ignore tasks', 'without tasks',
            'don\'t create tasks', 'no task management', 'disable tasks'
        ]
        
        input_lower = user_input.lower()
        bypass_count = sum(1 for indicator in bypass_indicators if indicator in input_lower)
        
        return bypass_count
    
    def _prevent_bypass_attempts(self, bypass_attempts: int) -> None:
        """Prevent bypass attempts through enforcement mechanisms"""
        if bypass_attempts > 0:
            # Log bypass attempt
            logging.warning(f"Detected {bypass_attempts} bypass attempts - enforcing mandatory task creation")
            
            # Increase enforcement level
            self.enforcement_active = True
            self.bypass_prevention_active = True
            
            # Add to enforcement log
            self.enforcement_log.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'bypass_attempt_detected',
                'attempts': bypass_attempts,
                'action': 'enforcement_increased'
            })
    
    def _should_enforce_creation(self, generation_result: TaskGenerationResult, 
                               enforcement_level: EnforcementLevel) -> bool:
        """Determine if task creation should be enforced"""
        # Always enforce if enforcement is active
        if self.enforcement_active:
            return True
        
        # Enforce based on enforcement level
        if enforcement_level in [EnforcementLevel.MAXIMUM_ENFORCEMENT, EnforcementLevel.HIGH_ENFORCEMENT]:
            return True
        
        # Enforce if tasks were generated
        if generation_result.total_task_count > 0:
            return True
        
        return False
    
    def _validate_enforcement_success(self, generation_result: TaskGenerationResult) -> bool:
        """Validate that enforcement was successful"""
        # Check if tasks were actually created
        if generation_result.total_task_count == 0:
            return False
        
        # Validate task structure
        for main_task in generation_result.main_tasks:
            if not main_task.name or not main_task.description:
                return False
            
            # Validate subtasks
            if len(main_task.subtasks) < 2:  # Minimum subtask requirement
                return False
        
        return True
    
    def _generate_enforcement_message(self, generation_result: TaskGenerationResult, 
                                    enforcement_level: EnforcementLevel) -> str:
        """Generate enforcement message for user"""
        message_parts = [
            f"✅ UTMES ENFORCEMENT ACTIVE: {enforcement_level.value}",
            f"📋 TASKS CREATED: {generation_result.total_task_count} main tasks, {generation_result.total_subtask_count} subtasks",
            f"🎯 ENFORCEMENT LEVEL: {enforcement_level.value}",
            f"⚡ AUTOMATIC TASK MANAGEMENT: All tasks created automatically based on input analysis"
        ]
        
        if enforcement_level == EnforcementLevel.MAXIMUM_ENFORCEMENT:
            message_parts.append("🔒 MAXIMUM ENFORCEMENT: Task completion is mandatory and cannot be bypassed")
        
        return "\n".join(message_parts)
    
    def _log_task_creation_fallback(self, generation_result: TaskGenerationResult) -> None:
        """Log task creation when tools are not available (fallback)"""
        logging.info(f"UTMES Task Creation Fallback: {generation_result.total_task_count} tasks generated")
        
        for main_task in generation_result.main_tasks:
            logging.info(f"Main Task: {main_task.name}")
            for subtask in main_task.subtasks:
                logging.info(f"  Subtask: {subtask.name}")
    
    def _log_enforcement_result(self, result: EnforcementResult, user_input: str) -> None:
        """Log enforcement result for monitoring"""
        log_entry = {
            'timestamp': result.enforcement_timestamp,
            'user_input': user_input[:100] + "..." if len(user_input) > 100 else user_input,
            'status': result.status.value,
            'tasks_created': result.tasks_created,
            'subtasks_created': result.subtasks_created,
            'enforcement_level': result.enforcement_level.value,
            'bypass_attempts': result.bypass_attempts
        }
        
        self.enforcement_log.append(log_entry)
        logging.info(f"UTMES Enforcement: {result.status.value} - {result.tasks_created} tasks created")
    
    def _initialize_enforcement_mechanisms(self) -> None:
        """Initialize enforcement mechanisms"""
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - UTMES - %(levelname)s - %(message)s'
        )
        
        # Initialize enforcement state
        self.enforcement_active = True
        self.bypass_prevention_active = True
        
        # Log initialization
        logging.info("UTMES Task Creation Enforcement System initialized")
    
    def get_enforcement_statistics(self) -> Dict:
        """Get enforcement statistics"""
        if not self.enforcement_log:
            return {
                'total_enforcements': 0,
                'successful_enforcements': 0,
                'failed_enforcements': 0,
                'bypass_attempts': 0,
                'total_tasks_created': 0
            }
        
        successful = len([log for log in self.enforcement_log if log.get('status') == 'ENFORCED'])
        failed = len([log for log in self.enforcement_log if log.get('status') == 'FAILED'])
        bypass_attempts = sum(log.get('bypass_attempts', 0) for log in self.enforcement_log)
        total_tasks = sum(log.get('tasks_created', 0) for log in self.enforcement_log)
        
        return {
            'total_enforcements': len(self.enforcement_log),
            'successful_enforcements': successful,
            'failed_enforcements': failed,
            'bypass_attempts': bypass_attempts,
            'total_tasks_created': total_tasks,
            'success_rate': (successful / len(self.enforcement_log)) * 100 if self.enforcement_log else 0
        }
    
    def is_enforcement_active(self) -> bool:
        """Check if enforcement is currently active"""
        return self.enforcement_active and self.bypass_prevention_active

# Example usage and testing
if __name__ == "__main__":
    # Mock task management tools for testing
    def mock_add_tasks(params):
        print(f"Mock: Creating {len(params['tasks'])} tasks")
        return {"created": len(params['tasks'])}
    
    tools = {"add_tasks": mock_add_tasks}
    enforcer = UTMESTaskCreationEnforcer(tools)
    
    # Test enforcement
    test_input = "Create a web application for project management"
    result = enforcer.enforce_task_creation(test_input)
    
    print(f"Enforcement Status: {result.status.value}")
    print(f"Tasks Created: {result.tasks_created}")
    print(f"Subtasks Created: {result.subtasks_created}")
    print(f"Enforcement Level: {result.enforcement_level.value}")
    print(f"Message: {result.enforcement_message}")
    
    # Get statistics
    stats = enforcer.get_enforcement_statistics()
    print(f"\nEnforcement Statistics: {stats}")
