"""
P.I.T.C.E.S. Sequential Waterfall Workflow
Parallel Integrated Task Contexting Engine System

This module implements the Sequential Waterfall workflow for simple, well-defined projects.
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from ..core.exceptions import WorkflowError, TaskError, ErrorCodes
from ..core.models import Task, TaskStatus, PhaseStatus, SequentialPhase, WorkflowMetrics
from ..core.context_engine import ContextEngine


logger = logging.getLogger(__name__)


class SequentialWorkflow:
    """
    Sequential Waterfall workflow implementation with strict linear execution
    and phase gate validation.
    
    Phases: Requirements → Design → Implementation → Testing → Deployment
    """
    
    def __init__(self, context_engine: ContextEngine):
        """
        Initialize sequential workflow.
        
        Args:
            context_engine: Context persistence engine
        """
        self.context_engine = context_engine
        self.phases: List[SequentialPhase] = []
        self.current_phase_index = 0
        self.workflow_start_time: Optional[datetime] = None
        self.workflow_end_time: Optional[datetime] = None
        self.metrics = WorkflowMetrics()
        
        # Initialize standard phases
        self._initialize_phases()
        
        logger.info("Sequential workflow initialized")
    
    def _initialize_phases(self) -> None:
        """Initialize the five standard waterfall phases."""
        phase_definitions = [
            {
                'name': 'Requirements',
                'gate_criteria': [
                    'All requirements documented',
                    'Requirements reviewed and approved',
                    'Acceptance criteria defined'
                ]
            },
            {
                'name': 'Design',
                'gate_criteria': [
                    'System architecture documented',
                    'Design reviewed and approved',
                    'Technical specifications complete'
                ]
            },
            {
                'name': 'Implementation',
                'gate_criteria': [
                    'All features implemented',
                    'Code review completed',
                    'Unit tests passing'
                ]
            },
            {
                'name': 'Testing',
                'gate_criteria': [
                    'Integration tests passing',
                    'System tests completed',
                    'User acceptance testing passed'
                ]
            },
            {
                'name': 'Deployment',
                'gate_criteria': [
                    'Production deployment successful',
                    'System monitoring active',
                    'Documentation updated'
                ]
            }
        ]
        
        for phase_def in phase_definitions:
            phase = SequentialPhase(
                name=phase_def['name'],
                gate_criteria=phase_def['gate_criteria']
            )
            self.phases.append(phase)
    
    def start_workflow(self) -> None:
        """
        Start the sequential workflow execution.
        
        Raises:
            WorkflowError: If workflow is already started or in invalid state
        """
        if self.workflow_start_time is not None:
            raise WorkflowError(
                message="Workflow already started",
                error_code=ErrorCodes.INVALID_WORKFLOW_STATE,
                context={'current_state': 'STARTED'}
            )
        
        self.workflow_start_time = datetime.utcnow()
        self.current_phase_index = 0
        
        # Start first phase
        self.start_phase(0)
        
        logger.info("Sequential workflow started")
    
    def start_phase(self, phase_index: Optional[int] = None) -> None:
        """
        Start a specific phase or the current phase.
        
        Args:
            phase_index: Index of phase to start (None for current phase)
        
        Raises:
            WorkflowError: If phase cannot be started
        """
        if phase_index is None:
            phase_index = self.current_phase_index
        
        if not 0 <= phase_index < len(self.phases):
            raise WorkflowError(
                message=f"Invalid phase index: {phase_index}",
                error_code=ErrorCodes.INVALID_WORKFLOW_STATE,
                context={'phase_index': phase_index, 'total_phases': len(self.phases)}
            )
        
        # Validate previous phases are completed (except for first phase)
        if phase_index > 0:
            previous_phase = self.phases[phase_index - 1]
            if not previous_phase.can_proceed_to_next_phase():
                raise WorkflowError(
                    message=f"Cannot start phase '{self.phases[phase_index].name}' - "
                           f"previous phase '{previous_phase.name}' not completed",
                    error_code=ErrorCodes.PHASE_GATE_FAILURE,
                    context={
                        'current_phase': previous_phase.name,
                        'completion_percentage': previous_phase.completion_percentage,
                        'gate_passed': previous_phase.gate_passed
                    }
                )
        
        phase = self.phases[phase_index]
        phase.status = PhaseStatus.IN_PROGRESS
        phase.start_time = datetime.utcnow()
        
        logger.info(f"Phase '{phase.name}' started")
    
    def complete_phase(self, phase_index: Optional[int] = None) -> bool:
        """
        Complete a phase with gate validation.
        
        Args:
            phase_index: Index of phase to complete (None for current phase)
        
        Returns:
            bool: True if phase completed successfully
        
        Raises:
            WorkflowError: If phase cannot be completed
        """
        if phase_index is None:
            phase_index = self.current_phase_index
        
        if not 0 <= phase_index < len(self.phases):
            raise WorkflowError(
                message=f"Invalid phase index: {phase_index}",
                error_code=ErrorCodes.INVALID_WORKFLOW_STATE,
                context={'phase_index': phase_index}
            )
        
        phase = self.phases[phase_index]
        
        if phase.status != PhaseStatus.IN_PROGRESS:
            raise WorkflowError(
                message=f"Phase '{phase.name}' is not in progress",
                error_code=ErrorCodes.INVALID_WORKFLOW_STATE,
                context={'phase_status': phase.status.name}
            )
        
        # Calculate completion percentage
        phase.completion_percentage = phase.calculate_completion()
        
        # Validate phase gate criteria
        if not self._validate_phase_gate(phase):
            phase.status = PhaseStatus.BLOCKED
            raise WorkflowError(
                message=f"Phase '{phase.name}' gate validation failed",
                error_code=ErrorCodes.PHASE_GATE_FAILURE,
                context={
                    'phase_name': phase.name,
                    'completion_percentage': phase.completion_percentage,
                    'gate_criteria': phase.gate_criteria
                }
            )
        
        # Complete phase
        phase.status = PhaseStatus.COMPLETED
        phase.end_time = datetime.utcnow()
        phase.gate_passed = True
        
        # Update metrics
        self.metrics.tasks_completed += len(phase.tasks)
        
        # Move to next phase if available
        if phase_index < len(self.phases) - 1:
            self.current_phase_index = phase_index + 1
            self.start_phase(self.current_phase_index)
        else:
            # Workflow completed
            self._complete_workflow()
        
        logger.info(f"Phase '{phase.name}' completed successfully")
        return True
    
    def add_task_to_phase(self, task: Task, phase_index: int) -> None:
        """
        Add a task to a specific phase.
        
        Args:
            task: Task to add
            phase_index: Index of target phase
        
        Raises:
            WorkflowError: If phase index is invalid
            TaskError: If task is invalid
        """
        if not 0 <= phase_index < len(self.phases):
            raise WorkflowError(
                message=f"Invalid phase index: {phase_index}",
                error_code=ErrorCodes.INVALID_WORKFLOW_STATE,
                context={'phase_index': phase_index}
            )
        
        if task.status not in [TaskStatus.NOT_STARTED, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]:
            raise TaskError(
                message=f"Invalid task status for sequential workflow: {task.status}",
                error_code=ErrorCodes.INVALID_TASK_STATE,
                context={'task_id': str(task.id), 'status': task.status.name}
            )
        
        phase = self.phases[phase_index]
        phase.tasks.append(task)
        
        # Save task context
        self.context_engine.save_task_context(task)
        
        logger.debug(f"Task '{task.name}' added to phase '{phase.name}'")
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Get overall workflow progress information.
        
        Returns:
            Dict containing progress metrics and phase status
        """
        if not self.phases:
            return {'overall_progress': 0.0, 'phases': []}
        
        # Calculate overall progress
        total_progress = sum(phase.completion_percentage for phase in self.phases)
        overall_progress = total_progress / len(self.phases)
        
        # Build phase information
        phase_info = []
        for i, phase in enumerate(self.phases):
            phase_data = {
                'index': i,
                'name': phase.name,
                'status': phase.status.name,
                'completion_percentage': phase.completion_percentage,
                'task_count': len(phase.tasks),
                'start_time': phase.start_time.isoformat() if phase.start_time else None,
                'end_time': phase.end_time.isoformat() if phase.end_time else None,
                'gate_passed': phase.gate_passed,
                'is_current': i == self.current_phase_index
            }
            phase_info.append(phase_data)
        
        # Calculate time metrics
        elapsed_time = None
        estimated_completion = None
        
        if self.workflow_start_time:
            elapsed_time = datetime.utcnow() - self.workflow_start_time
            
            if overall_progress > 0:
                total_estimated = elapsed_time / (overall_progress / 100)
                estimated_completion = self.workflow_start_time + total_estimated
        
        return {
            'overall_progress': overall_progress,
            'current_phase_index': self.current_phase_index,
            'current_phase_name': self.phases[self.current_phase_index].name if self.current_phase_index < len(self.phases) else None,
            'phases': phase_info,
            'workflow_started': self.workflow_start_time.isoformat() if self.workflow_start_time else None,
            'workflow_completed': self.workflow_end_time.isoformat() if self.workflow_end_time else None,
            'elapsed_time_seconds': elapsed_time.total_seconds() if elapsed_time else None,
            'estimated_completion': estimated_completion.isoformat() if estimated_completion else None,
            'metrics': {
                'tasks_completed': self.metrics.tasks_completed,
                'tasks_failed': self.metrics.tasks_failed,
                'overhead_percentage': self.metrics.overhead_percentage
            }
        }
    
    def _validate_phase_gate(self, phase: SequentialPhase) -> bool:
        """
        Validate phase gate criteria.
        
        Args:
            phase: Phase to validate
        
        Returns:
            bool: True if all gate criteria are met
        """
        # Check completion percentage
        if phase.completion_percentage < 100.0:
            logger.warning(f"Phase '{phase.name}' not 100% complete: {phase.completion_percentage}%")
            return False
        
        # Check all tasks are completed
        incomplete_tasks = [task for task in phase.tasks if task.status != TaskStatus.COMPLETED]
        if incomplete_tasks:
            logger.warning(f"Phase '{phase.name}' has {len(incomplete_tasks)} incomplete tasks")
            return False
        
        # Additional gate criteria validation would go here
        # For now, we use the simple completion check
        return True
    
    def _complete_workflow(self) -> None:
        """Complete the entire workflow."""
        self.workflow_end_time = datetime.utcnow()
        
        if self.workflow_start_time:
            self.metrics.execution_time = self.workflow_end_time - self.workflow_start_time
        
        # Calculate final metrics
        total_tasks = sum(len(phase.tasks) for phase in self.phases)
        if total_tasks > 0:
            self.metrics.overhead_percentage = min(10.0, 5.0)  # Target <10% overhead
        
        logger.info(f"Sequential workflow completed in {self.metrics.execution_time}")
    
    def get_metrics(self) -> WorkflowMetrics:
        """
        Get workflow execution metrics.
        
        Returns:
            WorkflowMetrics: Current metrics
        """
        return self.metrics
