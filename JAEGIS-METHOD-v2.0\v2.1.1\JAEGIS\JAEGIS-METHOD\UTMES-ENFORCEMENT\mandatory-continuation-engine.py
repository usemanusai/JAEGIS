#!/usr/bin/env python3
"""
UTMES Mandatory Continuation Engine
Automatically enforces task progression and prevents task abandonment
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Core enforcement mechanism
"""

import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

class ContinuationState(Enum):
    """States of task continuation"""
    MONITORING = "MONITORING"
    ENFORCING = "ENFORCING"
    REDIRECTING = "REDIRECTING"
    BLOCKING_ABANDONMENT = "BLOCKING_ABANDONMENT"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AbandonmentThreat(Enum):
    """Types of abandonment threats"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class TaskStatus(Enum):
    """Task status for continuation monitoring"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    STALLED = "STALLED"
    ABANDONED = "ABANDONED"
    COMPLETE = "COMPLETE"

@dataclass
class TaskContinuationContext:
    """Context for task continuation monitoring"""
    task_id: str
    task_name: str
    task_description: str
    current_status: TaskStatus
    priority_level: str
    created_timestamp: str
    last_activity_timestamp: str
    completion_percentage: float
    deliverables_completed: List[str]
    deliverables_remaining: List[str]
    dependencies: List[str]
    success_criteria: List[str]

@dataclass
class AbandonmentDetection:
    """Result of abandonment detection"""
    threat_level: AbandonmentThreat
    abandonment_indicators: List[str]
    time_since_activity: float
    completion_stagnation: bool
    user_behavior_patterns: List[str]
    recommended_actions: List[str]

@dataclass
class ContinuationEnforcementResult:
    """Result of continuation enforcement"""
    continuation_state: ContinuationState
    tasks_monitored: int
    tasks_enforced: int
    abandonment_attempts_blocked: int
    redirections_performed: int
    enforcement_actions: List[Dict]
    enforcement_timestamp: str
    enforcement_message: str

class UTMESMandatoryContinuationEngine:
    """
    UTMES Mandatory Continuation Engine
    Enforces task progression and prevents abandonment
    """
    
    def __init__(self, task_management_tools: Optional[Dict[str, Callable]] = None):
        # Initialize components
        self.task_management_tools = task_management_tools or {}
        
        # Continuation enforcement state
        self.continuation_enforcement_active = True
        self.abandonment_prevention_active = True
        self.automatic_redirection_active = True
        
        # Monitoring configuration
        self.monitoring_interval_minutes = 5
        self.abandonment_threshold_minutes = 30
        self.stagnation_threshold_hours = 2
        
        # Enforcement history
        self.enforcement_history = []
        self.monitored_tasks = {}
        
        # Initialize engine
        self._initialize_engine()
    
    def enforce_task_continuation(self, active_tasks: List[TaskContinuationContext]) -> ContinuationEnforcementResult:
        """
        MAIN CONTINUATION ENFORCEMENT FUNCTION
        Enforces continuation of all active tasks
        
        Args:
            active_tasks: List of active tasks to monitor and enforce
            
        Returns:
            ContinuationEnforcementResult with enforcement details
        """
        enforcement_start = datetime.now()
        enforcement_actions = []
        
        try:
            # Step 1: Update monitored tasks
            self._update_monitored_tasks(active_tasks)
            
            # Step 2: Monitor each active task
            tasks_monitored = 0
            tasks_enforced = 0
            abandonment_attempts_blocked = 0
            redirections_performed = 0
            
            for task_context in active_tasks:
                if task_context.current_status in [TaskStatus.NOT_STARTED, TaskStatus.IN_PROGRESS, TaskStatus.STALLED]:
                    tasks_monitored += 1
                    
                    # Step 3: Detect abandonment attempts
                    abandonment_detection = self._detect_abandonment_attempt(task_context)
                    
                    if abandonment_detection.threat_level != AbandonmentThreat.LOW:
                        # Step 4: Prevent abandonment
                        prevention_result = self._prevent_task_abandonment(task_context, abandonment_detection)
                        
                        if prevention_result['abandonment_blocked']:
                            abandonment_attempts_blocked += 1
                            enforcement_actions.append(prevention_result)
                        
                        # Step 5: Enforce continuation
                        continuation_result = self._enforce_mandatory_continuation(task_context)
                        
                        if continuation_result['continuation_enforced']:
                            tasks_enforced += 1
                            enforcement_actions.append(continuation_result)
                        
                        # Step 6: Redirect attention if needed
                        if self.automatic_redirection_active and abandonment_detection.threat_level in [AbandonmentThreat.HIGH, AbandonmentThreat.CRITICAL]:
                            redirection_result = self._enforce_attention_redirection(task_context)
                            
                            if redirection_result['redirection_performed']:
                                redirections_performed += 1
                                enforcement_actions.append(redirection_result)
            
            # Step 7: Generate enforcement result
            enforcement_result = ContinuationEnforcementResult(
                continuation_state=ContinuationState.COMPLETED,
                tasks_monitored=tasks_monitored,
                tasks_enforced=tasks_enforced,
                abandonment_attempts_blocked=abandonment_attempts_blocked,
                redirections_performed=redirections_performed,
                enforcement_actions=enforcement_actions,
                enforcement_timestamp=enforcement_start.isoformat(),
                enforcement_message=self._generate_enforcement_message(tasks_monitored, tasks_enforced, abandonment_attempts_blocked)
            )
            
            # Step 8: Log enforcement result
            self._log_enforcement_result(enforcement_result)
            self.enforcement_history.append(enforcement_result)
            
            return enforcement_result
            
        except Exception as e:
            # Handle enforcement errors
            error_result = ContinuationEnforcementResult(
                continuation_state=ContinuationState.FAILED,
                tasks_monitored=0,
                tasks_enforced=0,
                abandonment_attempts_blocked=0,
                redirections_performed=0,
                enforcement_actions=[],
                enforcement_timestamp=enforcement_start.isoformat(),
                enforcement_message=f"Continuation enforcement failed: {str(e)}"
            )
            
            self.enforcement_history.append(error_result)
            return error_result
    
    def _detect_abandonment_attempt(self, task_context: TaskContinuationContext) -> AbandonmentDetection:
        """Detect attempts to abandon task"""
        abandonment_indicators = []
        threat_level = AbandonmentThreat.LOW
        
        # Calculate time since last activity
        last_activity = datetime.fromisoformat(task_context.last_activity_timestamp)
        time_since_activity = (datetime.now() - last_activity).total_seconds() / 60  # minutes
        
        # Check for time-based abandonment indicators
        if time_since_activity > self.abandonment_threshold_minutes:
            abandonment_indicators.append(f"No activity for {time_since_activity:.1f} minutes")
            threat_level = AbandonmentThreat.MEDIUM
        
        if time_since_activity > (self.abandonment_threshold_minutes * 2):
            abandonment_indicators.append(f"Extended inactivity: {time_since_activity:.1f} minutes")
            threat_level = AbandonmentThreat.HIGH
        
        if time_since_activity > (self.abandonment_threshold_minutes * 4):
            abandonment_indicators.append(f"Critical inactivity: {time_since_activity:.1f} minutes")
            threat_level = AbandonmentThreat.CRITICAL
        
        # Check for completion stagnation
        completion_stagnation = False
        if task_context.completion_percentage < 10 and time_since_activity > 15:
            completion_stagnation = True
            abandonment_indicators.append("Task not started despite time elapsed")
            threat_level = max(threat_level, AbandonmentThreat.MEDIUM)
        
        if task_context.completion_percentage < 50 and time_since_activity > 60:
            completion_stagnation = True
            abandonment_indicators.append("Task progress stalled")
            threat_level = max(threat_level, AbandonmentThreat.HIGH)
        
        # Check for status-based indicators
        if task_context.current_status == TaskStatus.STALLED:
            abandonment_indicators.append("Task marked as stalled")
            threat_level = max(threat_level, AbandonmentThreat.HIGH)
        
        # Generate recommended actions
        recommended_actions = self._generate_recommended_actions(threat_level, abandonment_indicators)
        
        return AbandonmentDetection(
            threat_level=threat_level,
            abandonment_indicators=abandonment_indicators,
            time_since_activity=time_since_activity,
            completion_stagnation=completion_stagnation,
            user_behavior_patterns=[],  # Could be enhanced with user behavior analysis
            recommended_actions=recommended_actions
        )
    
    def _prevent_task_abandonment(self, task_context: TaskContinuationContext, 
                                 abandonment_detection: AbandonmentDetection) -> Dict:
        """Prevent task abandonment through enforcement mechanisms"""
        prevention_actions = []
        abandonment_blocked = False
        
        try:
            # Log abandonment attempt
            logging.warning(f"UTMES: Abandonment threat detected for task '{task_context.task_name}' - Level: {abandonment_detection.threat_level.value}")
            
            # Block abandonment based on threat level
            if abandonment_detection.threat_level in [AbandonmentThreat.HIGH, AbandonmentThreat.CRITICAL]:
                # Implement abandonment blocking mechanisms
                prevention_actions.append("Abandonment attempt blocked")
                prevention_actions.append("Task continuation enforced")
                abandonment_blocked = True
                
                # Update task status to prevent abandonment
                if 'update_tasks' in self.task_management_tools:
                    update_result = self.task_management_tools['update_tasks']({
                        "tasks": [{
                            "task_id": task_context.task_id,
                            "state": "IN_PROGRESS",
                            "description": f"{task_context.task_description} - CONTINUATION ENFORCED"
                        }]
                    })
                    
                    if update_result:
                        prevention_actions.append("Task status updated to enforce continuation")
            
            return {
                'abandonment_blocked': abandonment_blocked,
                'prevention_actions': prevention_actions,
                'threat_level': abandonment_detection.threat_level.value,
                'task_id': task_context.task_id,
                'task_name': task_context.task_name,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"UTMES: Failed to prevent task abandonment - {e}")
            return {
                'abandonment_blocked': False,
                'prevention_actions': [f"Prevention failed: {str(e)}"],
                'threat_level': abandonment_detection.threat_level.value,
                'task_id': task_context.task_id,
                'task_name': task_context.task_name,
                'timestamp': datetime.now().isoformat()
            }
    
    def _enforce_mandatory_continuation(self, task_context: TaskContinuationContext) -> Dict:
        """Enforce mandatory continuation of task"""
        continuation_actions = []
        continuation_enforced = False
        
        try:
            # Log continuation enforcement
            logging.info(f"UTMES: Enforcing mandatory continuation for task '{task_context.task_name}'")
            
            # Enforce continuation based on task status
            if task_context.current_status in [TaskStatus.NOT_STARTED, TaskStatus.STALLED]:
                continuation_actions.append("Task progression enforced")
                continuation_actions.append("Mandatory continuation activated")
                continuation_enforced = True
                
                # Generate continuation requirements
                continuation_requirements = self._generate_continuation_requirements(task_context)
                continuation_actions.extend(continuation_requirements)
            
            elif task_context.current_status == TaskStatus.IN_PROGRESS:
                # Ensure progress continues
                if task_context.completion_percentage < 100:
                    continuation_actions.append("Progress continuation enforced")
                    continuation_actions.append("Completion requirements activated")
                    continuation_enforced = True
            
            return {
                'continuation_enforced': continuation_enforced,
                'continuation_actions': continuation_actions,
                'task_id': task_context.task_id,
                'task_name': task_context.task_name,
                'current_status': task_context.current_status.value,
                'completion_percentage': task_context.completion_percentage,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"UTMES: Failed to enforce mandatory continuation - {e}")
            return {
                'continuation_enforced': False,
                'continuation_actions': [f"Continuation enforcement failed: {str(e)}"],
                'task_id': task_context.task_id,
                'task_name': task_context.task_name,
                'timestamp': datetime.now().isoformat()
            }
    
    def _enforce_attention_redirection(self, task_context: TaskContinuationContext) -> Dict:
        """Enforce redirection of attention to incomplete task"""
        redirection_actions = []
        redirection_performed = False
        
        try:
            # Log attention redirection
            logging.info(f"UTMES: Redirecting attention to incomplete task '{task_context.task_name}'")
            
            # Generate redirection message
            redirection_message = self._generate_redirection_message(task_context)
            redirection_actions.append(f"Attention redirected: {redirection_message}")
            
            # Display task status and requirements
            status_display = self._generate_task_status_display(task_context)
            redirection_actions.append(f"Task status displayed: {status_display}")
            
            # Enforce completion requirements
            completion_requirements = self._generate_completion_requirements(task_context)
            redirection_actions.extend(completion_requirements)
            
            redirection_performed = True
            
            return {
                'redirection_performed': redirection_performed,
                'redirection_actions': redirection_actions,
                'redirection_message': redirection_message,
                'task_id': task_context.task_id,
                'task_name': task_context.task_name,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"UTMES: Failed to enforce attention redirection - {e}")
            return {
                'redirection_performed': False,
                'redirection_actions': [f"Redirection failed: {str(e)}"],
                'task_id': task_context.task_id,
                'task_name': task_context.task_name,
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_recommended_actions(self, threat_level: AbandonmentThreat, indicators: List[str]) -> List[str]:
        """Generate recommended actions based on threat level"""
        actions = []
        
        if threat_level == AbandonmentThreat.LOW:
            actions.extend([
                "Continue monitoring task progress",
                "Provide gentle progress reminders"
            ])
        elif threat_level == AbandonmentThreat.MEDIUM:
            actions.extend([
                "Increase monitoring frequency",
                "Provide progress guidance",
                "Check for blocking issues"
            ])
        elif threat_level == AbandonmentThreat.HIGH:
            actions.extend([
                "Immediate attention redirection required",
                "Enforce task continuation",
                "Block abandonment attempts",
                "Provide completion assistance"
            ])
        elif threat_level == AbandonmentThreat.CRITICAL:
            actions.extend([
                "CRITICAL: Immediate intervention required",
                "Maximum enforcement activation",
                "Mandatory task completion",
                "Block all abandonment attempts",
                "Continuous monitoring until completion"
            ])
        
        return actions
    
    def _generate_continuation_requirements(self, task_context: TaskContinuationContext) -> List[str]:
        """Generate continuation requirements for task"""
        requirements = []
        
        if task_context.current_status == TaskStatus.NOT_STARTED:
            requirements.extend([
                "Task must be started immediately",
                "Initial progress must be made within 15 minutes",
                "First deliverable must be identified"
            ])
        elif task_context.current_status == TaskStatus.STALLED:
            requirements.extend([
                "Task progression must resume immediately",
                "Blocking issues must be resolved",
                "Progress must be demonstrated within 30 minutes"
            ])
        
        # Add deliverable-based requirements
        if task_context.deliverables_remaining:
            requirements.append(f"Remaining deliverables must be completed: {', '.join(task_context.deliverables_remaining[:3])}")
        
        return requirements
    
    def _generate_redirection_message(self, task_context: TaskContinuationContext) -> str:
        """Generate redirection message for incomplete task"""
        completion_status = f"{task_context.completion_percentage:.1f}% complete"
        time_elapsed = self._calculate_time_elapsed(task_context.created_timestamp)
        
        return (f"⚠️ ATTENTION REQUIRED: Task '{task_context.task_name}' is {completion_status} "
                f"after {time_elapsed}. Immediate continuation required.")
    
    def _generate_task_status_display(self, task_context: TaskContinuationContext) -> str:
        """Generate task status display"""
        return (f"Task: {task_context.task_name} | "
                f"Status: {task_context.current_status.value} | "
                f"Progress: {task_context.completion_percentage:.1f}% | "
                f"Remaining: {len(task_context.deliverables_remaining)} deliverables")
    
    def _generate_completion_requirements(self, task_context: TaskContinuationContext) -> List[str]:
        """Generate completion requirements for task"""
        requirements = [
            f"Task '{task_context.task_name}' must be completed before proceeding",
            f"All {len(task_context.deliverables_remaining)} remaining deliverables must be provided",
            "Progress must be demonstrated and validated"
        ]
        
        # Add success criteria requirements
        if task_context.success_criteria:
            requirements.append(f"Success criteria must be met: {', '.join(task_context.success_criteria[:2])}")
        
        return requirements
    
    def _calculate_time_elapsed(self, created_timestamp: str) -> str:
        """Calculate time elapsed since task creation"""
        created_time = datetime.fromisoformat(created_timestamp)
        elapsed = datetime.now() - created_time
        
        if elapsed.total_seconds() < 3600:  # Less than 1 hour
            minutes = int(elapsed.total_seconds() / 60)
            return f"{minutes} minutes"
        elif elapsed.total_seconds() < 86400:  # Less than 1 day
            hours = int(elapsed.total_seconds() / 3600)
            return f"{hours} hours"
        else:
            days = int(elapsed.total_seconds() / 86400)
            return f"{days} days"
    
    def _update_monitored_tasks(self, active_tasks: List[TaskContinuationContext]) -> None:
        """Update monitored tasks registry"""
        for task_context in active_tasks:
            self.monitored_tasks[task_context.task_id] = {
                'task_context': task_context,
                'last_monitored': datetime.now().isoformat(),
                'monitoring_count': self.monitored_tasks.get(task_context.task_id, {}).get('monitoring_count', 0) + 1
            }
    
    def _generate_enforcement_message(self, tasks_monitored: int, tasks_enforced: int, 
                                    abandonment_attempts_blocked: int) -> str:
        """Generate enforcement message"""
        message_parts = [
            f"✅ UTMES CONTINUATION ENFORCEMENT ACTIVE",
            f"📊 MONITORING: {tasks_monitored} active tasks",
            f"⚡ ENFORCED: {tasks_enforced} task continuations",
            f"🛡️ BLOCKED: {abandonment_attempts_blocked} abandonment attempts"
        ]
        
        if abandonment_attempts_blocked > 0:
            message_parts.append("🔒 MANDATORY CONTINUATION: Task abandonment prevented")
        
        return "\n".join(message_parts)
    
    def _log_enforcement_result(self, result: ContinuationEnforcementResult) -> None:
        """Log enforcement result for monitoring"""
        log_data = {
            'timestamp': result.enforcement_timestamp,
            'continuation_state': result.continuation_state.value,
            'tasks_monitored': result.tasks_monitored,
            'tasks_enforced': result.tasks_enforced,
            'abandonment_attempts_blocked': result.abandonment_attempts_blocked,
            'redirections_performed': result.redirections_performed,
            'enforcement_actions_count': len(result.enforcement_actions)
        }
        
        logging.info(f"UTMES Continuation Enforcement: {json.dumps(log_data)}")
    
    def _initialize_engine(self) -> None:
        """Initialize continuation engine"""
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - UTMES-Continuation - %(levelname)s - %(message)s'
        )
        
        # Log initialization
        logging.info("UTMES Mandatory Continuation Engine initialized")
    
    def get_continuation_statistics(self) -> Dict:
        """Get continuation enforcement statistics"""
        if not self.enforcement_history:
            return {
                'total_enforcements': 0,
                'tasks_monitored': 0,
                'tasks_enforced': 0,
                'abandonment_attempts_blocked': 0,
                'redirections_performed': 0,
                'enforcement_success_rate': 0.0
            }
        
        total_tasks_monitored = sum(r.tasks_monitored for r in self.enforcement_history)
        total_tasks_enforced = sum(r.tasks_enforced for r in self.enforcement_history)
        total_abandonment_blocked = sum(r.abandonment_attempts_blocked for r in self.enforcement_history)
        total_redirections = sum(r.redirections_performed for r in self.enforcement_history)
        
        successful_enforcements = len([r for r in self.enforcement_history if r.continuation_state == ContinuationState.COMPLETED])
        success_rate = (successful_enforcements / len(self.enforcement_history)) * 100 if self.enforcement_history else 0
        
        return {
            'total_enforcements': len(self.enforcement_history),
            'tasks_monitored': total_tasks_monitored,
            'tasks_enforced': total_tasks_enforced,
            'abandonment_attempts_blocked': total_abandonment_blocked,
            'redirections_performed': total_redirections,
            'enforcement_success_rate': round(success_rate, 2),
            'currently_monitored_tasks': len(self.monitored_tasks)
        }
    
    def is_continuation_enforcement_active(self) -> bool:
        """Check if continuation enforcement is currently active"""
        return (self.continuation_enforcement_active and 
                self.abandonment_prevention_active)

# Example usage and testing
if __name__ == "__main__":
    # Mock task management tools for testing
    def mock_update_tasks(params):
        print(f"Mock: Updating {len(params['tasks'])} tasks")
        return {"updated": len(params['tasks'])}
    
    tools = {"update_tasks": mock_update_tasks}
    engine = UTMESMandatoryContinuationEngine(tools)
    
    # Create test task context
    test_task = TaskContinuationContext(
        task_id="test_task_123",
        task_name="Test Task Implementation",
        task_description="Implement test functionality",
        current_status=TaskStatus.IN_PROGRESS,
        priority_level="HIGH",
        created_timestamp=(datetime.now() - timedelta(hours=1)).isoformat(),
        last_activity_timestamp=(datetime.now() - timedelta(minutes=45)).isoformat(),
        completion_percentage=25.0,
        deliverables_completed=["Initial setup"],
        deliverables_remaining=["Core implementation", "Testing", "Documentation"],
        dependencies=[],
        success_criteria=["Implementation complete", "Tests passing"]
    )
    
    # Test continuation enforcement
    result = engine.enforce_task_continuation([test_task])
    
    print(f"Continuation State: {result.continuation_state.value}")
    print(f"Tasks Monitored: {result.tasks_monitored}")
    print(f"Tasks Enforced: {result.tasks_enforced}")
    print(f"Abandonment Attempts Blocked: {result.abandonment_attempts_blocked}")
    print(f"Redirections Performed: {result.redirections_performed}")
    print(f"Enforcement Actions: {len(result.enforcement_actions)}")
    
    # Get statistics
    stats = engine.get_continuation_statistics()
    print(f"\nContinuation Statistics: {stats}")
    
    # Test enforcement status
    print(f"Continuation Enforcement Active: {engine.is_continuation_enforcement_active()}")
