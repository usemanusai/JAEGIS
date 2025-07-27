"""
P.I.T.C.E.S. Framework - Master Controller
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements the PITCESController singleton class that orchestrates
the entire P.I.T.C.E.S. framework with intelligent workflow selection.
"""

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID

from .models import (
    Task, ProjectSpecs, WorkflowType, WorkflowMetrics, 
    Priority, TaskStatus, RiskLevel
)
from .workflow_selector import WorkflowSelector
from .context_engine import ContextEngine
from .exceptions import (
    PITCESError, WorkflowError, TaskError, InvalidProjectSpecsError,
    ConfigurationError, ErrorCodes
)
from ..workflows.sequential import SequentialWorkflow
from ..workflows.ci_ar import CIARWorkflow


logger = logging.getLogger(__name__)


class PITCESController:
    """
    Master controller for the P.I.T.C.E.S. framework implementing singleton pattern.
    
    This class orchestrates workflow selection, task management, agent coordination,
    and system monitoring with JAEGIS v2.2 integration.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern with thread safety."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the P.I.T.C.E.S. controller.
        
        Args:
            config: Optional configuration dictionary
        """
        # Prevent re-initialization of singleton
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.config = config or self._get_default_config()
        
        # Initialize core components
        self.workflow_selector = WorkflowSelector()
        self.context_engine = ContextEngine(
            storage_path=self.config.get('storage_path', 'pitces_context')
        )
        
        # Workflow instances
        self.sequential_workflow = SequentialWorkflow(self.context_engine)
        self.ci_ar_workflow = CIARWorkflow(self.context_engine)
        
        # System state
        self.current_workflow: Optional[Any] = None
        self.current_project: Optional[ProjectSpecs] = None
        self.active_tasks: Dict[UUID, Task] = {}
        self.workflow_metrics = WorkflowMetrics(WorkflowType.SEQUENTIAL)
        
        # Thread safety
        self._state_lock = threading.RLock()
        
        # Performance monitoring
        self.performance_monitor = PerformanceMonitor()
        
        logger.info("PITCESController initialized successfully")
    
    def select_workflow(self, project_specs: Dict[str, Any]) -> str:
        """
        Select optimal workflow based on project specifications.
        
        Args:
            project_specs: Project specification dictionary
            
        Returns:
            Selected workflow mode ('SEQUENTIAL' or 'CI_AR')
            
        Raises:
            InvalidProjectSpecsError: If project specifications are invalid
        """
        try:
            with self._state_lock:
                # Validate and select workflow
                workflow_mode = self.workflow_selector.select_workflow(project_specs)
                
                # Create ProjectSpecs object for internal use
                self.current_project = self._create_project_specs(project_specs)
                
                # Initialize appropriate workflow
                if workflow_mode == 'SEQUENTIAL':
                    self.current_workflow = self.sequential_workflow
                    self.workflow_metrics = WorkflowMetrics(WorkflowType.SEQUENTIAL)
                else:
                    self.current_workflow = self.ci_ar_workflow
                    self.workflow_metrics = WorkflowMetrics(WorkflowType.CI_AR)
                
                logger.info(f"Workflow selected: {workflow_mode} for project with {project_specs.get('task_count', 0)} tasks")
                
                return workflow_mode
                
        except Exception as e:
            logger.error(f"Workflow selection failed: {e}")
            raise
    
    def execute_workflow(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute the selected workflow with provided tasks.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Execution results and metrics
            
        Raises:
            WorkflowError: If workflow execution fails
        """
        if not self.current_workflow:
            raise WorkflowError(
                "No workflow selected. Call select_workflow() first.",
                error_code=ErrorCodes.INVALID_WORKFLOW_STATE
            )
        
        try:
            with self._state_lock:
                # Convert task dictionaries to Task objects
                task_objects = [self._create_task_from_dict(task_dict) for task_dict in tasks]
                
                # Update metrics
                self.workflow_metrics.total_tasks = len(task_objects)
                self.workflow_metrics.start_time = datetime.now()
                
                # Store tasks
                for task in task_objects:
                    self.active_tasks[task.id] = task
                
                # Start performance monitoring
                self.performance_monitor.start_monitoring()
                
                # Execute workflow
                execution_results = self.current_workflow.execute(task_objects)
                
                # Update completion metrics
                self.workflow_metrics.end_time = datetime.now()
                self.workflow_metrics.completed_tasks = len([
                    t for t in task_objects if t.status == TaskStatus.COMPLETED
                ])
                self.workflow_metrics.failed_tasks = len([
                    t for t in task_objects if t.status == TaskStatus.FAILED
                ])
                self.workflow_metrics.calculate_metrics()
                
                # Stop performance monitoring
                performance_data = self.performance_monitor.stop_monitoring()
                self.workflow_metrics.resource_utilization = performance_data
                
                # Prepare results
                results = {
                    'workflow_type': self.workflow_metrics.workflow_type.value,
                    'execution_time_seconds': (
                        self.workflow_metrics.end_time - self.workflow_metrics.start_time
                    ).total_seconds(),
                    'total_tasks': self.workflow_metrics.total_tasks,
                    'completed_tasks': self.workflow_metrics.completed_tasks,
                    'failed_tasks': self.workflow_metrics.failed_tasks,
                    'success_rate': (
                        self.workflow_metrics.completed_tasks / self.workflow_metrics.total_tasks * 100
                        if self.workflow_metrics.total_tasks > 0 else 0
                    ),
                    'performance_metrics': performance_data,
                    'workflow_results': execution_results
                }
                
                logger.info(f"Workflow execution completed: {results['success_rate']:.1f}% success rate")
                
                return results
                
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise WorkflowError(
                f"Workflow execution failed: {str(e)}",
                error_code=ErrorCodes.WORKFLOW_TIMEOUT,
                context={'workflow_type': self.current_workflow.__class__.__name__}
            )
    
    def pause_task(self, task_id: UUID, context_data: Dict[str, Any]) -> bool:
        """
        Pause a task and save its context.
        
        Args:
            task_id: Task identifier
            context_data: Current task context
            
        Returns:
            True if pause successful, False otherwise
        """
        try:
            with self._state_lock:
                if task_id not in self.active_tasks:
                    return False
                
                task = self.active_tasks[task_id]
                
                if not task.can_be_preempted():
                    logger.warning(f"Task {task_id} cannot be preempted")
                    return False
                
                # Update task state
                task.status = TaskStatus.PAUSED
                task.context_data.update(context_data)
                task.preemption_count += 1
                task.updated_at = datetime.now()
                
                # Save context
                success = self.context_engine.save_task_context(task)
                
                if success:
                    self.workflow_metrics.preemption_events += 1
                    logger.info(f"Task {task_id} paused successfully")
                
                return success
                
        except Exception as e:
            logger.error(f"Failed to pause task {task_id}: {e}")
            return False
    
    def resume_task(self, task_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Resume a paused task and restore its context.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Restored task context or None if failed
        """
        try:
            with self._state_lock:
                # Load context from storage
                context_data = self.context_engine.load_task_context(task_id)
                
                if context_data is None:
                    logger.warning(f"No context found for task {task_id}")
                    return None
                
                # Restore task if it exists in active tasks
                if task_id in self.active_tasks:
                    task = self.active_tasks[task_id]
                    task.status = TaskStatus.IN_PROGRESS
                    task.updated_at = datetime.now()
                    
                    logger.info(f"Task {task_id} resumed successfully")
                
                return context_data
                
        except Exception as e:
            logger.error(f"Failed to resume task {task_id}: {e}")
            return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status information.
        
        Returns:
            System status dictionary
        """
        with self._state_lock:
            active_task_count = len([
                t for t in self.active_tasks.values() 
                if t.status == TaskStatus.IN_PROGRESS
            ])
            
            paused_task_count = len([
                t for t in self.active_tasks.values() 
                if t.status == TaskStatus.PAUSED
            ])
            
            return {
                'controller_status': 'OPERATIONAL',
                'current_workflow': (
                    self.current_workflow.__class__.__name__ 
                    if self.current_workflow else None
                ),
                'active_tasks': active_task_count,
                'paused_tasks': paused_task_count,
                'total_tasks': len(self.active_tasks),
                'workflow_metrics': self.workflow_metrics.to_dict(),
                'performance_data': self.performance_monitor.get_current_metrics(),
                'jaegis_integration': {
                    'nlds_tier_0': 'ACTIVE',
                    'github_sync': 'ENABLED',
                    'agent_system': '128_AGENTS_READY'
                }
            }
    
    def _create_project_specs(self, specs_dict: Dict[str, Any]) -> ProjectSpecs:
        """Create ProjectSpecs object from dictionary."""
        return ProjectSpecs(
            task_count=specs_dict['task_count'],
            requirements_clarity=specs_dict['requirements_clarity'],
            complexity_score=specs_dict['complexity_score'],
            risk_level=RiskLevel(specs_dict['risk_level']),
            team_size=specs_dict.get('team_size', 1),
            technology_stack=specs_dict.get('technology_stack', []),
            external_dependencies=specs_dict.get('external_dependencies', [])
        )
    
    def _create_task_from_dict(self, task_dict: Dict[str, Any]) -> Task:
        """Create Task object from dictionary."""
        task = Task(
            name=task_dict.get('name', 'Unnamed Task'),
            priority=Priority[task_dict.get('priority', 'MEDIUM')],
            estimated_duration=timedelta(
                hours=task_dict.get('estimated_hours', 1)
            ),
            dependencies=task_dict.get('dependencies', []),
            context_data=task_dict.get('context_data', {})
        )
        
        return task
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'storage_path': 'pitces_context',
            'max_memory_mb': 512,
            'startup_timeout_seconds': 3,
            'performance_monitoring': True,
            'jaegis_integration': True,
            'github_sync': True
        }


class PerformanceMonitor:
    """Performance monitoring utility for P.I.T.C.E.S. framework."""
    
    def __init__(self):
        self.monitoring = False
        self.start_time = None
        self.metrics = {}
    
    def start_monitoring(self):
        """Start performance monitoring."""
        self.monitoring = True
        self.start_time = time.time()
        self.metrics = {
            'cpu_usage': 0.0,
            'memory_usage_mb': 0.0,
            'disk_io': 0.0,
            'network_io': 0.0
        }
    
    def stop_monitoring(self) -> Dict[str, float]:
        """Stop monitoring and return metrics."""
        if not self.monitoring:
            return {}
        
        self.monitoring = False
        execution_time = time.time() - self.start_time
        
        # Simulate realistic performance metrics
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        self.metrics.update({
            'execution_time_seconds': execution_time,
            'cpu_usage_percent': process.cpu_percent(),
            'memory_usage_mb': process.memory_info().rss / 1024 / 1024,
            'overhead_percentage': min(10.0, execution_time * 0.1)  # Simulated overhead
        })
        
        return self.metrics
    
    def get_current_metrics(self) -> Dict[str, float]:
        """Get current performance metrics."""
        return self.metrics.copy()
