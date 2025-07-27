"""
P.I.T.C.E.S. Framework - Preemption Manager
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements task preemption protocols with state persistence,
context switching, and dependency management for CI/AR workflow mode.
"""

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set, Tuple
from uuid import UUID
import networkx as nx

from .models import Task, Priority, TaskStatus
from .context_engine import ContextEngine
from .exceptions import PreemptionError, DependencyError, ErrorCodes


logger = logging.getLogger(__name__)


class PreemptionManager:
    """
    Task preemption manager with state persistence and dependency management.
    
    Features:
    - Safe task preemption with context preservation
    - Dependency graph management (DAG validation)
    - State serialization and recovery
    - Preemption history and analytics
    - Deadlock detection and prevention
    """
    
    def __init__(self, context_engine: ContextEngine):
        """
        Initialize the preemption manager.
        
        Args:
            context_engine: Context engine for state persistence
        """
        self.context_engine = context_engine
        
        # Dependency graph (Directed Acyclic Graph)
        self.dependency_graph = nx.DiGraph()
        
        # Task state tracking
        self.active_tasks: Dict[UUID, Task] = {}
        self.paused_tasks: Dict[UUID, Task] = {}
        self.preemption_history: List[Dict[str, Any]] = []
        
        # Preemption policies
        self.max_preemption_depth = 3  # Maximum nested preemptions
        self.preemption_cooldown = timedelta(minutes=5)  # Minimum time between preemptions
        self.last_preemption_time: Dict[UUID, datetime] = {}
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Performance metrics
        self.metrics = {
            'total_preemptions': 0,
            'successful_preemptions': 0,
            'failed_preemptions': 0,
            'context_switches': 0,
            'average_preemption_time': 0.0,
            'deadlock_detections': 0
        }
        
        logger.info("PreemptionManager initialized")
    
    def pause_task(self, task_id: UUID, context_data: Dict[str, Any]) -> bool:
        """
        Pause a task and serialize its current state.
        
        Args:
            task_id: Task identifier to pause
            context_data: Current task execution context
            
        Returns:
            True if pause successful, False otherwise
            
        Raises:
            PreemptionError: If preemption fails
        """
        start_time = time.time()
        
        try:
            with self._lock:
                # Validate task exists and can be preempted
                if task_id not in self.active_tasks:
                    logger.warning(f"Task {task_id} not found in active tasks")
                    return False
                
                task = self.active_tasks[task_id]
                
                # Check preemption eligibility
                if not self._can_preempt_task(task):
                    logger.warning(f"Task {task_id} cannot be preempted")
                    return False
                
                # Check for circular dependencies
                if self._would_create_cycle(task_id):
                    logger.error(f"Preempting task {task_id} would create dependency cycle")
                    raise PreemptionError(
                        "Preemption would create circular dependency",
                        error_code=ErrorCodes.PAUSE_FAILURE,
                        context={'task_id': str(task_id)}
                    )
                
                # Update task state
                original_status = task.status
                task.status = TaskStatus.PAUSED
                task.context_data.update(context_data)
                task.context_data['preemption_timestamp'] = datetime.now().isoformat()
                task.context_data['original_status'] = original_status.name
                task.preemption_count += 1
                task.updated_at = datetime.now()
                
                # Serialize context to persistent storage
                success = self.context_engine.save_task_context(task)
                
                if not success:
                    # Rollback on failure
                    task.status = original_status
                    task.preemption_count -= 1
                    raise PreemptionError(
                        "Failed to save task context",
                        error_code=ErrorCodes.CONTEXT_SWITCH_FAILURE,
                        context={'task_id': str(task_id)}
                    )
                
                # Move task to paused collection
                self.paused_tasks[task_id] = task
                del self.active_tasks[task_id]
                
                # Update preemption tracking
                self.last_preemption_time[task_id] = datetime.now()
                
                # Record preemption event
                preemption_time = time.time() - start_time
                preemption_record = {
                    'task_id': str(task_id),
                    'timestamp': datetime.now().isoformat(),
                    'preemption_time_seconds': preemption_time,
                    'preemption_count': task.preemption_count,
                    'context_size_bytes': len(str(context_data)),
                    'reason': context_data.get('preemption_reason', 'Unknown')
                }
                self.preemption_history.append(preemption_record)
                
                # Update metrics
                self.metrics['total_preemptions'] += 1
                self.metrics['successful_preemptions'] += 1
                self.metrics['context_switches'] += 1
                self._update_average_preemption_time(preemption_time)
                
                logger.info(f"Task {task_id} paused successfully in {preemption_time:.3f}s")
                return True
                
        except Exception as e:
            self.metrics['failed_preemptions'] += 1
            logger.error(f"Failed to pause task {task_id}: {e}")
            
            if isinstance(e, PreemptionError):
                raise
            
            raise PreemptionError(
                f"Task preemption failed: {str(e)}",
                error_code=ErrorCodes.PAUSE_FAILURE,
                context={'task_id': str(task_id), 'error': str(e)}
            )
    
    def resume_task(self, task_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Resume a paused task and deserialize its state.
        
        Args:
            task_id: Task identifier to resume
            
        Returns:
            Restored task context or None if failed
            
        Raises:
            PreemptionError: If resume operation fails
        """
        try:
            with self._lock:
                # Check if task is in paused collection
                if task_id not in self.paused_tasks:
                    logger.warning(f"Task {task_id} not found in paused tasks")
                    return None
                
                # Load context from persistent storage
                context_data = self.context_engine.load_task_context(task_id)
                
                if context_data is None:
                    logger.error(f"Failed to load context for task {task_id}")
                    raise PreemptionError(
                        "Failed to load task context",
                        error_code=ErrorCodes.RESUME_FAILURE,
                        context={'task_id': str(task_id)}
                    )
                
                # Restore task state
                task = self.paused_tasks[task_id]
                
                # Restore original status if available
                original_status_name = task.context_data.get('original_status', 'IN_PROGRESS')
                try:
                    task.status = TaskStatus[original_status_name]
                except KeyError:
                    task.status = TaskStatus.IN_PROGRESS
                
                task.updated_at = datetime.now()
                
                # Move task back to active collection
                self.active_tasks[task_id] = task
                del self.paused_tasks[task_id]
                
                # Update metrics
                self.metrics['context_switches'] += 1
                
                logger.info(f"Task {task_id} resumed successfully")
                return context_data
                
        except Exception as e:
            logger.error(f"Failed to resume task {task_id}: {e}")
            
            if isinstance(e, PreemptionError):
                raise
            
            raise PreemptionError(
                f"Task resume failed: {str(e)}",
                error_code=ErrorCodes.RESUME_FAILURE,
                context={'task_id': str(task_id), 'error': str(e)}
            )
    
    def add_task_dependency(self, task_id: UUID, dependency_id: UUID) -> bool:
        """
        Add a dependency relationship between tasks.
        
        Args:
            task_id: Task that depends on dependency_id
            dependency_id: Task that task_id depends on
            
        Returns:
            True if dependency added successfully, False otherwise
            
        Raises:
            DependencyError: If adding dependency would create a cycle
        """
        try:
            with self._lock:
                # Add nodes if they don't exist
                if not self.dependency_graph.has_node(task_id):
                    self.dependency_graph.add_node(task_id)
                
                if not self.dependency_graph.has_node(dependency_id):
                    self.dependency_graph.add_node(dependency_id)
                
                # Check if adding edge would create a cycle
                if self.dependency_graph.has_edge(dependency_id, task_id):
                    # Direct reverse dependency exists
                    raise DependencyError(
                        f"Adding dependency would create direct cycle: {task_id} -> {dependency_id}",
                        context={'task_id': str(task_id), 'dependency_id': str(dependency_id)}
                    )
                
                # Temporarily add edge and check for cycles
                self.dependency_graph.add_edge(task_id, dependency_id)
                
                if not nx.is_directed_acyclic_graph(self.dependency_graph):
                    # Remove the edge that created the cycle
                    self.dependency_graph.remove_edge(task_id, dependency_id)
                    
                    raise DependencyError(
                        f"Adding dependency would create cycle in dependency graph",
                        context={'task_id': str(task_id), 'dependency_id': str(dependency_id)}
                    )
                
                logger.debug(f"Added dependency: {task_id} depends on {dependency_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to add dependency {task_id} -> {dependency_id}: {e}")
            
            if isinstance(e, DependencyError):
                raise
            
            return False
    
    def get_task_dependencies(self, task_id: UUID) -> List[UUID]:
        """
        Get all dependencies for a task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            List of task IDs that this task depends on
        """
        with self._lock:
            if self.dependency_graph.has_node(task_id):
                return list(self.dependency_graph.successors(task_id))
            return []
    
    def get_dependent_tasks(self, task_id: UUID) -> List[UUID]:
        """
        Get all tasks that depend on this task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            List of task IDs that depend on this task
        """
        with self._lock:
            if self.dependency_graph.has_node(task_id):
                return list(self.dependency_graph.predecessors(task_id))
            return []
    
    def detect_deadlocks(self) -> List[List[UUID]]:
        """
        Detect potential deadlocks in the dependency graph.
        
        Returns:
            List of strongly connected components (potential deadlocks)
        """
        with self._lock:
            try:
                # Find strongly connected components
                sccs = list(nx.strongly_connected_components(self.dependency_graph))
                
                # Filter out single-node components (not deadlocks)
                deadlocks = [list(scc) for scc in sccs if len(scc) > 1]
                
                if deadlocks:
                    self.metrics['deadlock_detections'] += len(deadlocks)
                    logger.warning(f"Detected {len(deadlocks)} potential deadlocks")
                
                return deadlocks
                
            except Exception as e:
                logger.error(f"Deadlock detection failed: {e}")
                return []
    
    def get_preemption_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive preemption metrics and statistics.
        
        Returns:
            Preemption metrics dictionary
        """
        with self._lock:
            return {
                'metrics': self.metrics.copy(),
                'active_tasks_count': len(self.active_tasks),
                'paused_tasks_count': len(self.paused_tasks),
                'dependency_graph_nodes': self.dependency_graph.number_of_nodes(),
                'dependency_graph_edges': self.dependency_graph.number_of_edges(),
                'preemption_history_size': len(self.preemption_history),
                'recent_preemptions': self.preemption_history[-10:],  # Last 10 preemptions
                'deadlock_status': {
                    'detected_deadlocks': len(self.detect_deadlocks()),
                    'is_dag': nx.is_directed_acyclic_graph(self.dependency_graph)
                }
            }
    
    def _can_preempt_task(self, task: Task) -> bool:
        """Check if a task can be safely preempted."""
        # Critical tasks cannot be preempted
        if task.priority == Priority.CRITICAL:
            return False
        
        # Check preemption count limit
        if task.preemption_count >= self.max_preemption_depth:
            logger.warning(f"Task {task.id} has reached maximum preemption depth")
            return False
        
        # Check cooldown period
        if task.id in self.last_preemption_time:
            time_since_last = datetime.now() - self.last_preemption_time[task.id]
            if time_since_last < self.preemption_cooldown:
                logger.warning(f"Task {task.id} is in preemption cooldown")
                return False
        
        # Task must be in progress to be preempted
        if task.status != TaskStatus.IN_PROGRESS:
            return False
        
        return True
    
    def _would_create_cycle(self, task_id: UUID) -> bool:
        """Check if preempting a task would create a dependency cycle."""
        # This is a simplified check - in practice, you'd need more sophisticated analysis
        # based on the specific preemption scenario and dependency relationships
        return False
    
    def _update_average_preemption_time(self, preemption_time: float):
        """Update the rolling average preemption time."""
        current_avg = self.metrics['average_preemption_time']
        total_preemptions = self.metrics['total_preemptions']
        
        if total_preemptions == 1:
            self.metrics['average_preemption_time'] = preemption_time
        else:
            # Rolling average calculation
            self.metrics['average_preemption_time'] = (
                (current_avg * (total_preemptions - 1) + preemption_time) / total_preemptions
            )
    
    def cleanup_old_preemption_history(self, max_age_days: int = 7):
        """
        Clean up old preemption history entries.
        
        Args:
            max_age_days: Maximum age of history entries to keep
        """
        cutoff_time = datetime.now() - timedelta(days=max_age_days)
        
        with self._lock:
            original_count = len(self.preemption_history)
            
            self.preemption_history = [
                record for record in self.preemption_history
                if datetime.fromisoformat(record['timestamp']) > cutoff_time
            ]
            
            cleaned_count = original_count - len(self.preemption_history)
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old preemption history entries")
