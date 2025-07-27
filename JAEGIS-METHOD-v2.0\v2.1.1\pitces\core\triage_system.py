"""
P.I.T.C.E.S. Framework - Triage System
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements the task triage system with priority-based queuing,
SLA management, and automatic escalation protocols.
"""

import logging
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from uuid import UUID

from .models import Task, Priority, TaskStatus
from .exceptions import TriageError, ErrorCodes


logger = logging.getLogger(__name__)


class TriageSystem:
    """
    Task triage system implementing priority-based queuing with SLA management.
    
    Features:
    - Priority-based task classification
    - SLA deadline tracking and enforcement
    - Automatic escalation for overdue tasks
    - Queue management with overflow protection
    - Real-time monitoring and metrics
    """
    
    def __init__(self, max_queue_size: int = 1000):
        """
        Initialize the triage system.
        
        Args:
            max_queue_size: Maximum number of tasks per priority queue
        """
        self.max_queue_size = max_queue_size
        
        # Priority queues for each priority level
        self.queues: Dict[Priority, deque] = {
            Priority.CRITICAL: deque(maxlen=max_queue_size),
            Priority.HIGH: deque(maxlen=max_queue_size),
            Priority.MEDIUM: deque(maxlen=max_queue_size),
            Priority.LOW: deque(maxlen=max_queue_size)
        }
        
        # SLA targets for each priority level
        self.sla_targets = {
            Priority.CRITICAL: timedelta(minutes=5),
            Priority.HIGH: timedelta(hours=1),
            Priority.MEDIUM: timedelta(hours=24),
            Priority.LOW: timedelta(days=7)
        }
        
        # Tracking and metrics
        self.task_registry: Dict[UUID, Task] = {}
        self.escalation_history: List[Dict] = []
        self.queue_metrics = defaultdict(int)
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Background monitoring
        self._monitoring_active = False
        self._monitor_thread = None
        
        logger.info("TriageSystem initialized with max queue size: %d", max_queue_size)
    
    def classify_task(self, task: Task) -> Priority:
        """
        Classify task priority based on content analysis and metadata.
        
        Args:
            task: Task to classify
            
        Returns:
            Classified priority level
        """
        try:
            # Start with the task's declared priority
            classified_priority = task.priority
            
            # Apply classification rules
            classification_rules = [
                self._check_security_keywords,
                self._check_system_critical_keywords,
                self._check_deadline_urgency,
                self._check_dependency_impact,
                self._check_business_impact
            ]
            
            for rule in classification_rules:
                rule_priority = rule(task)
                if rule_priority and rule_priority.value < classified_priority.value:
                    classified_priority = rule_priority
                    logger.debug(f"Task {task.id} escalated to {classified_priority.name} by rule {rule.__name__}")
            
            # Update task priority if changed
            if classified_priority != task.priority:
                task.priority = classified_priority
                task.updated_at = datetime.now()
                logger.info(f"Task {task.id} priority updated to {classified_priority.name}")
            
            return classified_priority
            
        except Exception as e:
            logger.error(f"Task classification failed for {task.id}: {e}")
            return task.priority  # Return original priority on error
    
    def add_task(self, task: Task) -> bool:
        """
        Add task to appropriate priority queue.
        
        Args:
            task: Task to add to queue
            
        Returns:
            True if task added successfully, False otherwise
            
        Raises:
            TriageError: If queue operations fail
        """
        try:
            with self._lock:
                # Classify task priority
                priority = self.classify_task(task)
                
                # Check queue capacity
                if len(self.queues[priority]) >= self.max_queue_size:
                    logger.warning(f"Queue overflow for priority {priority.name}")
                    raise TriageError(
                        f"Queue overflow for priority {priority.name}",
                        error_code=ErrorCodes.QUEUE_OVERFLOW,
                        context={'priority': priority.name, 'queue_size': len(self.queues[priority])}
                    )
                
                # Add to queue
                self.queues[priority].append(task)
                self.task_registry[task.id] = task
                
                # Update metrics
                self.queue_metrics[f"{priority.name}_added"] += 1
                self.queue_metrics[f"{priority.name}_current"] = len(self.queues[priority])
                
                # Start monitoring if not already active
                if not self._monitoring_active:
                    self._start_monitoring()
                
                logger.info(f"Task {task.id} added to {priority.name} queue")
                return True
                
        except Exception as e:
            logger.error(f"Failed to add task {task.id} to queue: {e}")
            if isinstance(e, TriageError):
                raise
            
            raise TriageError(
                f"Failed to add task to queue: {str(e)}",
                error_code=ErrorCodes.TRIAGE_ERROR,
                context={'task_id': str(task.id)}
            )
    
    def get_next_task(self) -> Optional[Task]:
        """
        Get the next highest priority task from queues.
        
        Returns:
            Next task to execute or None if no tasks available
        """
        try:
            with self._lock:
                # Check queues in priority order
                for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
                    if self.queues[priority]:
                        task = self.queues[priority].popleft()
                        
                        # Update metrics
                        self.queue_metrics[f"{priority.name}_processed"] += 1
                        self.queue_metrics[f"{priority.name}_current"] = len(self.queues[priority])
                        
                        # Check for SLA violation
                        if task.is_sla_violated():
                            self._handle_sla_violation(task)
                        
                        logger.debug(f"Retrieved task {task.id} from {priority.name} queue")
                        return task
                
                return None
                
        except Exception as e:
            logger.error(f"Failed to get next task: {e}")
            return None
    
    def escalate_task(self, task_id: UUID, reason: str = "SLA violation") -> bool:
        """
        Escalate task to higher priority level.
        
        Args:
            task_id: Task identifier
            reason: Escalation reason
            
        Returns:
            True if escalation successful, False otherwise
        """
        try:
            with self._lock:
                if task_id not in self.task_registry:
                    logger.warning(f"Task {task_id} not found for escalation")
                    return False
                
                task = self.task_registry[task_id]
                original_priority = task.priority
                
                # Determine new priority
                if task.priority == Priority.LOW:
                    new_priority = Priority.MEDIUM
                elif task.priority == Priority.MEDIUM:
                    new_priority = Priority.HIGH
                elif task.priority == Priority.HIGH:
                    new_priority = Priority.CRITICAL
                else:
                    # Already at highest priority
                    logger.info(f"Task {task_id} already at CRITICAL priority")
                    return False
                
                # Remove from current queue
                try:
                    self.queues[original_priority].remove(task)
                    self.queue_metrics[f"{original_priority.name}_current"] = len(self.queues[original_priority])
                except ValueError:
                    # Task not in queue (might be in progress)
                    pass
                
                # Update task priority
                task.priority = new_priority
                task.updated_at = datetime.now()
                
                # Add to new priority queue
                self.queues[new_priority].appendleft(task)  # Add to front for immediate processing
                self.queue_metrics[f"{new_priority.name}_current"] = len(self.queues[new_priority])
                
                # Record escalation
                escalation_record = {
                    'task_id': str(task_id),
                    'original_priority': original_priority.name,
                    'new_priority': new_priority.name,
                    'reason': reason,
                    'timestamp': datetime.now().isoformat()
                }
                self.escalation_history.append(escalation_record)
                
                logger.warning(f"Task {task_id} escalated from {original_priority.name} to {new_priority.name}: {reason}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to escalate task {task_id}: {e}")
            return False
    
    def get_queue_status(self) -> Dict[str, any]:
        """
        Get comprehensive queue status and metrics.
        
        Returns:
            Queue status dictionary
        """
        with self._lock:
            status = {
                'queue_sizes': {
                    priority.name: len(self.queues[priority])
                    for priority in Priority
                },
                'total_tasks': sum(len(queue) for queue in self.queues.values()),
                'sla_violations': len([
                    task for task in self.task_registry.values()
                    if task.is_sla_violated()
                ]),
                'escalation_count': len(self.escalation_history),
                'metrics': dict(self.queue_metrics),
                'oldest_tasks': self._get_oldest_tasks(),
                'monitoring_active': self._monitoring_active
            }
            
            return status
    
    def _check_security_keywords(self, task: Task) -> Optional[Priority]:
        """Check for security-related keywords."""
        security_keywords = [
            'security', 'vulnerability', 'breach', 'exploit', 'malware',
            'unauthorized', 'attack', 'intrusion', 'compromise'
        ]
        
        text_to_check = f"{task.name} {task.context_data.get('description', '')}"
        
        if any(keyword in text_to_check.lower() for keyword in security_keywords):
            return Priority.CRITICAL
        
        return None
    
    def _check_system_critical_keywords(self, task: Task) -> Optional[Priority]:
        """Check for system-critical keywords."""
        critical_keywords = [
            'system down', 'outage', 'crash', 'failure', 'broken',
            'not working', 'emergency', 'urgent', 'critical'
        ]
        
        text_to_check = f"{task.name} {task.context_data.get('description', '')}"
        
        if any(keyword in text_to_check.lower() for keyword in critical_keywords):
            return Priority.HIGH
        
        return None
    
    def _check_deadline_urgency(self, task: Task) -> Optional[Priority]:
        """Check deadline urgency."""
        if task.sla_deadline:
            time_remaining = task.sla_deadline - datetime.now()
            
            if time_remaining <= timedelta(minutes=30):
                return Priority.CRITICAL
            elif time_remaining <= timedelta(hours=2):
                return Priority.HIGH
        
        return None
    
    def _check_dependency_impact(self, task: Task) -> Optional[Priority]:
        """Check impact on dependent tasks."""
        # If task has many dependencies, it might be critical
        if len(task.dependencies) > 5:
            return Priority.HIGH
        
        return None
    
    def _check_business_impact(self, task: Task) -> Optional[Priority]:
        """Check business impact indicators."""
        high_impact_keywords = [
            'revenue', 'customer', 'production', 'business critical',
            'client facing', 'public', 'compliance'
        ]
        
        text_to_check = f"{task.name} {task.context_data.get('description', '')}"
        
        if any(keyword in text_to_check.lower() for keyword in high_impact_keywords):
            return Priority.HIGH
        
        return None
    
    def _handle_sla_violation(self, task: Task):
        """Handle SLA violation for a task."""
        violation_record = {
            'task_id': str(task.id),
            'priority': task.priority.name,
            'sla_deadline': task.sla_deadline.isoformat(),
            'violation_time': datetime.now().isoformat(),
            'delay_minutes': (datetime.now() - task.sla_deadline).total_seconds() / 60
        }
        
        logger.warning(f"SLA violation detected for task {task.id}: {violation_record['delay_minutes']:.1f} minutes late")
        
        # Attempt automatic escalation
        self.escalate_task(task.id, "SLA violation")
    
    def _get_oldest_tasks(self) -> Dict[str, Optional[str]]:
        """Get oldest task in each priority queue."""
        oldest_tasks = {}
        
        for priority in Priority:
            if self.queues[priority]:
                oldest_task = min(self.queues[priority], key=lambda t: t.created_at)
                oldest_tasks[priority.name] = {
                    'task_id': str(oldest_task.id),
                    'age_minutes': (datetime.now() - oldest_task.created_at).total_seconds() / 60
                }
            else:
                oldest_tasks[priority.name] = None
        
        return oldest_tasks
    
    def _start_monitoring(self):
        """Start background monitoring thread."""
        if self._monitoring_active:
            return
        
        self._monitoring_active = True
        self._monitor_thread = threading.Thread(target=self._monitor_queues, daemon=True)
        self._monitor_thread.start()
        
        logger.info("Queue monitoring started")
    
    def _monitor_queues(self):
        """Background monitoring of queues for SLA violations."""
        while self._monitoring_active:
            try:
                with self._lock:
                    # Check for SLA violations
                    for task in self.task_registry.values():
                        if task.status == TaskStatus.PENDING and task.is_sla_violated():
                            self._handle_sla_violation(task)
                
                # Sleep for monitoring interval
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Queue monitoring error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def stop_monitoring(self):
        """Stop background monitoring."""
        self._monitoring_active = False
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)
        
        logger.info("Queue monitoring stopped")
