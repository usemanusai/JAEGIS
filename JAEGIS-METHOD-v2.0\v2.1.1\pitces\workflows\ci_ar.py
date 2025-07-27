"""
P.I.T.C.E.S. Continuous Integration & Adaptive Refinement (CI/AR) Workflow
Parallel Integrated Task Contexting Engine System

This module implements the CI/AR workflow for complex, dynamic projects with task preemption
and adaptive refinement capabilities.
"""

import logging
import time
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from uuid import UUID

from ..core.exceptions import WorkflowError, TaskError, PreemptionError, TriageError, ErrorCodes
from ..core.models import Task, TaskStatus, Priority, WorkflowMetrics
from ..core.context_engine import ContextEngine


logger = logging.getLogger(__name__)


class TriageSystem:
    """
    Task triage system with priority-based queuing and automatic escalation.
    
    Priority levels:
    - CRITICAL: <5 minute response SLA
    - HIGH: <1 hour response SLA  
    - MEDIUM: <24 hours response SLA
    - LOW: <1 week response SLA
    """
    
    def __init__(self):
        """Initialize triage system with priority queues."""
        self.queues: Dict[Priority, deque] = {
            Priority.CRITICAL: deque(),
            Priority.HIGH: deque(),
            Priority.MEDIUM: deque(),
            Priority.LOW: deque()
        }
        
        self.sla_timeouts = {
            Priority.CRITICAL: timedelta(minutes=5),
            Priority.HIGH: timedelta(hours=1),
            Priority.MEDIUM: timedelta(hours=24),
            Priority.LOW: timedelta(weeks=1)
        }
        
        self.task_timestamps: Dict[UUID, datetime] = {}
        
        logger.info("Triage system initialized")
    
    def classify_task(self, task: Task) -> Priority:
        """
        Classify task priority based on content and context.
        
        Args:
            task: Task to classify
        
        Returns:
            Priority: Classified priority level
        """
        # Priority classification logic
        task_name_lower = task.name.lower()
        context_data = task.context_data or {}
        
        # Critical indicators
        critical_keywords = ['security', 'vulnerability', 'system-breaking', 'critical', 'emergency']
        if any(keyword in task_name_lower for keyword in critical_keywords):
            return Priority.CRITICAL
        
        # High priority indicators
        high_keywords = ['core', 'functional', 'failure', 'urgent', 'blocking']
        if any(keyword in task_name_lower for keyword in high_keywords):
            return Priority.HIGH
        
        # Check context for priority hints
        if context_data.get('severity') == 'critical':
            return Priority.CRITICAL
        elif context_data.get('severity') == 'high':
            return Priority.HIGH
        elif context_data.get('severity') == 'low':
            return Priority.LOW
        
        # Default to medium priority
        return Priority.MEDIUM
    
    def add_task(self, task: Task) -> None:
        """
        Add task to appropriate priority queue.
        
        Args:
            task: Task to add to queue
        """
        # Classify if not already set
        if task.priority == Priority.MEDIUM and task.name:
            task.priority = self.classify_task(task)
        
        # Add to appropriate queue
        self.queues[task.priority].append(task)
        self.task_timestamps[task.id] = datetime.utcnow()
        
        logger.debug(f"Task '{task.name}' added to {task.priority.name} queue")
    
    def get_next_task(self) -> Optional[Task]:
        """
        Get next highest priority task from queues.
        
        Returns:
            Optional[Task]: Next task to process or None if queues empty
        """
        # Check queues in priority order
        for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            if self.queues[priority]:
                task = self.queues[priority].popleft()
                self.task_timestamps.pop(task.id, None)
                return task
        
        return None
    
    def escalate_task(self, task: Task) -> bool:
        """
        Escalate task to higher priority level.
        
        Args:
            task: Task to escalate
        
        Returns:
            bool: True if escalation successful
        """
        if task.priority == Priority.CRITICAL:
            logger.warning(f"Cannot escalate CRITICAL task '{task.name}' further")
            return False
        
        # Remove from current queue
        try:
            self.queues[task.priority].remove(task)
        except ValueError:
            logger.warning(f"Task '{task.name}' not found in {task.priority.name} queue")
            return False
        
        # Escalate priority
        priority_order = [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL]
        current_index = priority_order.index(task.priority)
        new_priority = priority_order[current_index + 1]
        
        task.priority = new_priority
        self.queues[new_priority].appendleft(task)  # Add to front of higher priority queue
        
        logger.info(f"Task '{task.name}' escalated from {priority_order[current_index].name} to {new_priority.name}")
        return True
    
    def check_sla_violations(self) -> List[Task]:
        """
        Check for SLA violations and return tasks that need escalation.
        
        Returns:
            List[Task]: Tasks that have exceeded their SLA
        """
        violations = []
        current_time = datetime.utcnow()
        
        for priority, queue in self.queues.items():
            sla_timeout = self.sla_timeouts[priority]
            
            for task in queue:
                task_time = self.task_timestamps.get(task.id)
                if task_time and (current_time - task_time) > sla_timeout:
                    violations.append(task)
        
        return violations
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get current queue status and metrics.
        
        Returns:
            Dict: Queue status information
        """
        status = {
            'queue_lengths': {priority.name: len(queue) for priority, queue in self.queues.items()},
            'total_tasks': sum(len(queue) for queue in self.queues.values()),
            'oldest_task_age': None,
            'sla_violations': len(self.check_sla_violations())
        }
        
        # Find oldest task
        if self.task_timestamps:
            oldest_time = min(self.task_timestamps.values())
            status['oldest_task_age'] = (datetime.utcnow() - oldest_time).total_seconds()
        
        return status


class PreemptionManager:
    """
    Task preemption manager with state persistence and recovery.
    """
    
    def __init__(self, context_engine: ContextEngine):
        """
        Initialize preemption manager.
        
        Args:
            context_engine: Context persistence engine
        """
        self.context_engine = context_engine
        self.paused_tasks: Dict[UUID, Dict[str, Any]] = {}
        self.dependency_graph: Dict[UUID, Set[UUID]] = {}
        
        logger.info("Preemption manager initialized")
    
    def pause_task(self, task_id: UUID, context_data: Dict[str, Any]) -> bool:
        """
        Pause task and serialize current state.
        
        Args:
            task_id: ID of task to pause
            context_data: Current task context and state
        
        Returns:
            bool: True if pause successful
        
        Raises:
            PreemptionError: If pause operation fails
        """
        try:
            # Create pause context
            pause_context = {
                'task_id': str(task_id),
                'paused_at': datetime.utcnow().isoformat(),
                'context_data': context_data,
                'state': 'PAUSED'
            }
            
            # Store in memory for quick access
            self.paused_tasks[task_id] = pause_context
            
            # Persist to storage
            # Note: In a real implementation, this would create a special pause context file
            logger.info(f"Task {task_id} paused successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to pause task {task_id}: {e}")
            raise PreemptionError(
                message=f"Failed to pause task",
                error_code=ErrorCodes.PAUSE_FAILURE,
                context={'task_id': str(task_id), 'error': str(e)}
            )
    
    def resume_task(self, task_id: UUID) -> Dict[str, Any]:
        """
        Resume paused task and deserialize state.
        
        Args:
            task_id: ID of task to resume
        
        Returns:
            Dict: Restored task context
        
        Raises:
            PreemptionError: If resume operation fails
        """
        try:
            if task_id not in self.paused_tasks:
                raise PreemptionError(
                    message=f"No paused task found with ID {task_id}",
                    error_code=ErrorCodes.RESUME_FAILURE,
                    context={'task_id': str(task_id)}
                )
            
            # Retrieve pause context
            pause_context = self.paused_tasks.pop(task_id)
            
            # Validate context
            if pause_context.get('state') != 'PAUSED':
                raise PreemptionError(
                    message=f"Task {task_id} is not in paused state",
                    error_code=ErrorCodes.RESUME_FAILURE,
                    context={'task_id': str(task_id), 'state': pause_context.get('state')}
                )
            
            # Return restored context
            restored_context = pause_context['context_data']
            restored_context['resumed_at'] = datetime.utcnow().isoformat()
            
            logger.info(f"Task {task_id} resumed successfully")
            return restored_context
            
        except Exception as e:
            if isinstance(e, PreemptionError):
                raise
            
            logger.error(f"Failed to resume task {task_id}: {e}")
            raise PreemptionError(
                message=f"Failed to resume task",
                error_code=ErrorCodes.RESUME_FAILURE,
                context={'task_id': str(task_id), 'error': str(e)}
            )
    
    def add_dependency(self, task_id: UUID, depends_on: UUID) -> None:
        """
        Add task dependency to the dependency graph.
        
        Args:
            task_id: Task that has the dependency
            depends_on: Task that must complete first
        
        Raises:
            PreemptionError: If adding dependency would create a cycle
        """
        # Check for circular dependencies
        if self._would_create_cycle(task_id, depends_on):
            raise PreemptionError(
                message=f"Adding dependency would create circular dependency",
                error_code=ErrorCodes.CONTEXT_SWITCH_FAILURE,
                context={'task_id': str(task_id), 'depends_on': str(depends_on)}
            )
        
        if task_id not in self.dependency_graph:
            self.dependency_graph[task_id] = set()
        
        self.dependency_graph[task_id].add(depends_on)
        logger.debug(f"Added dependency: {task_id} depends on {depends_on}")
    
    def _would_create_cycle(self, task_id: UUID, depends_on: UUID) -> bool:
        """Check if adding dependency would create a circular dependency."""
        visited = set()
        
        def has_path(start: UUID, target: UUID) -> bool:
            if start == target:
                return True
            if start in visited:
                return False
            
            visited.add(start)
            dependencies = self.dependency_graph.get(start, set())
            
            return any(has_path(dep, target) for dep in dependencies)
        
        return has_path(depends_on, task_id)


class CIARWorkflow:
    """
    Continuous Integration & Adaptive Refinement workflow implementation.
    
    Features:
    - Task preemption and context switching
    - Priority-based triage system
    - Adaptive task scheduling
    - Real-time remedial task handling
    """
    
    def __init__(self, context_engine: ContextEngine):
        """
        Initialize CI/AR workflow.
        
        Args:
            context_engine: Context persistence engine
        """
        self.context_engine = context_engine
        self.triage_system = TriageSystem()
        self.preemption_manager = PreemptionManager(context_engine)
        self.active_tasks: Dict[UUID, Task] = {}
        self.completed_tasks: List[Task] = []
        self.metrics = WorkflowMetrics()
        self.workflow_start_time: Optional[datetime] = None
        self.is_running = False
        
        logger.info("CI/AR workflow initialized")
    
    def start_workflow(self) -> None:
        """Start the CI/AR workflow execution."""
        if self.is_running:
            raise WorkflowError(
                message="Workflow already running",
                error_code=ErrorCodes.INVALID_WORKFLOW_STATE,
                context={'current_state': 'RUNNING'}
            )
        
        self.workflow_start_time = datetime.utcnow()
        self.is_running = True
        
        logger.info("CI/AR workflow started")
    
    def add_task(self, task: Task) -> None:
        """
        Add task to the workflow with automatic triage.
        
        Args:
            task: Task to add
        """
        # Add to triage system
        self.triage_system.add_task(task)
        
        # Save context
        self.context_engine.save_task_context(task)
        
        logger.debug(f"Task '{task.name}' added to CI/AR workflow")
    
    def process_next_task(self) -> Optional[Task]:
        """
        Process the next highest priority task.
        
        Returns:
            Optional[Task]: Processed task or None if no tasks available
        """
        # Check for SLA violations and escalate
        violations = self.triage_system.check_sla_violations()
        for task in violations:
            self.triage_system.escalate_task(task)
            self.metrics.context_switches += 1
        
        # Get next task
        task = self.triage_system.get_next_task()
        if not task:
            return None
        
        # Check if we need to preempt current task
        if self.active_tasks and task.priority == Priority.CRITICAL:
            self._handle_preemption(task)
        
        # Execute task
        self._execute_task(task)
        
        return task
    
    def _handle_preemption(self, urgent_task: Task) -> None:
        """
        Handle task preemption for urgent tasks.
        
        Args:
            urgent_task: Urgent task that requires immediate attention
        """
        # Pause all active tasks
        for task_id, active_task in list(self.active_tasks.items()):
            try:
                context_data = {
                    'status': active_task.status.name,
                    'completion_percentage': active_task.completion_percentage,
                    'context_data': active_task.context_data,
                    'preempted_by': str(urgent_task.id)
                }
                
                if self.preemption_manager.pause_task(task_id, context_data):
                    active_task.status = TaskStatus.PAUSED
                    self.active_tasks.pop(task_id)
                    self.metrics.preemption_count += 1
                    
                    logger.info(f"Task '{active_task.name}' preempted by urgent task '{urgent_task.name}'")
                
            except PreemptionError as e:
                logger.error(f"Failed to preempt task {task_id}: {e}")
    
    def _execute_task(self, task: Task) -> None:
        """
        Execute a task with context management.
        
        Args:
            task: Task to execute
        """
        start_time = time.time()
        
        try:
            # Mark as active
            task.status = TaskStatus.IN_PROGRESS
            self.active_tasks[task.id] = task
            
            # Simulate task execution (in real implementation, this would delegate to agents)
            execution_time = self._simulate_task_execution(task)
            
            # Complete task
            task.status = TaskStatus.COMPLETED
            task.completion_percentage = 100.0
            task.updated_at = datetime.utcnow()
            
            # Move to completed
            self.active_tasks.pop(task.id, None)
            self.completed_tasks.append(task)
            self.metrics.tasks_completed += 1
            
            # Update context
            self.context_engine.save_task_context(task)
            
            logger.info(f"Task '{task.name}' completed in {execution_time:.2f}s")
            
        except Exception as e:
            # Handle task failure
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.utcnow()
            
            self.active_tasks.pop(task.id, None)
            self.metrics.tasks_failed += 1
            
            logger.error(f"Task '{task.name}' failed: {e}")
        
        finally:
            # Update metrics
            execution_time = time.time() - start_time
            self.metrics.average_response_time = timedelta(seconds=execution_time)
    
    def _simulate_task_execution(self, task: Task) -> float:
        """
        Simulate task execution time based on task characteristics.
        
        Args:
            task: Task to simulate
        
        Returns:
            float: Simulated execution time in seconds
        """
        # Base execution time
        base_time = 1.0
        
        # Adjust based on priority (higher priority = faster execution)
        priority_multiplier = {
            Priority.CRITICAL: 0.5,
            Priority.HIGH: 0.7,
            Priority.MEDIUM: 1.0,
            Priority.LOW: 1.5
        }
        
        execution_time = base_time * priority_multiplier.get(task.priority, 1.0)
        
        # Simulate work
        time.sleep(min(execution_time, 0.1))  # Cap at 100ms for demo
        
        return execution_time
    
    def resume_paused_tasks(self) -> int:
        """
        Resume all paused tasks.
        
        Returns:
            int: Number of tasks resumed
        """
        resumed_count = 0
        
        # Get all paused task IDs
        paused_task_ids = list(self.preemption_manager.paused_tasks.keys())
        
        for task_id in paused_task_ids:
            try:
                context_data = self.preemption_manager.resume_task(task_id)
                
                # Recreate task from context (simplified)
                # In real implementation, this would fully restore task state
                logger.info(f"Task {task_id} resumed from pause")
                resumed_count += 1
                
            except PreemptionError as e:
                logger.error(f"Failed to resume task {task_id}: {e}")
        
        return resumed_count
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """
        Get current workflow status and metrics.
        
        Returns:
            Dict: Workflow status information
        """
        queue_status = self.triage_system.get_queue_status()
        
        return {
            'is_running': self.is_running,
            'workflow_start_time': self.workflow_start_time.isoformat() if self.workflow_start_time else None,
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'paused_tasks': len(self.preemption_manager.paused_tasks),
            'queue_status': queue_status,
            'metrics': {
                'tasks_completed': self.metrics.tasks_completed,
                'tasks_failed': self.metrics.tasks_failed,
                'preemption_count': self.metrics.preemption_count,
                'context_switches': self.metrics.context_switches,
                'success_rate': self.metrics.calculate_success_rate(),
                'efficiency_score': self.metrics.calculate_efficiency_score()
            }
        }
    
    def get_metrics(self) -> WorkflowMetrics:
        """
        Get workflow execution metrics.
        
        Returns:
            WorkflowMetrics: Current metrics
        """
        return self.metrics
