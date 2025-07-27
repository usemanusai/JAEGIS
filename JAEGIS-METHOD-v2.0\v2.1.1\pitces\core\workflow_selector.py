"""
P.I.T.C.E.S. Workflow Selection Engine
Parallel Integrated Task Contexting Engine System

This module implements the intelligent workflow selection logic based on quantifiable project characteristics.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Tuple

from .models import ProjectSpecs, WorkflowMode, RiskLevel
from .exceptions import InvalidProjectSpecsError, ErrorCodes


logger = logging.getLogger(__name__)


class WorkflowSelector:
    """
    Intelligent workflow selection engine that analyzes project characteristics
    and determines the optimal execution mode.
    """
    
    def __init__(self):
        """Initialize the workflow selector with default thresholds."""
        self.task_count_threshold = 50
        self.clarity_threshold = 95.0
        self.complexity_threshold = 5
        self.sequential_risk_levels = {RiskLevel.LOW}
        
        # Decision weights for hybrid scoring (future enhancement)
        self.weights = {
            'task_count': 0.3,
            'requirements_clarity': 0.25,
            'architectural_complexity': 0.25,
            'risk_level': 0.2
        }
    
    def select_workflow(self, project_specs: Dict[str, Any]) -> str:
        """
        Analyze project specifications and select optimal workflow mode.
        
        Args:
            project_specs: Dictionary containing project characteristics:
                - task_count (int): Number of tasks in project
                - requirements_clarity (float): Clarity percentage (0-100)
                - architectural_complexity (int): Complexity score (1-10)
                - risk_level (str): Risk assessment ("LOW", "MEDIUM", "HIGH")
        
        Returns:
            str: Selected workflow mode ("SEQUENTIAL" or "CI_AR")
        
        Raises:
            InvalidProjectSpecsError: If project specifications are invalid
        """
        try:
            # Validate and parse project specifications
            specs = self._validate_and_parse_specs(project_specs)
            
            # Apply selection logic
            workflow_mode, decision_rationale = self._apply_selection_logic(specs)
            
            # Log decision with structured information
            self._log_decision(specs, workflow_mode, decision_rationale)
            
            return workflow_mode.value
            
        except Exception as e:
            if isinstance(e, InvalidProjectSpecsError):
                raise
            
            logger.error(f"Unexpected error in workflow selection: {e}")
            raise InvalidProjectSpecsError(
                message="Failed to select workflow due to unexpected error",
                error_code=ErrorCodes.INVALID_TASK_COUNT,
                context={'original_error': str(e)}
            )
    
    def _validate_and_parse_specs(self, project_specs: Dict[str, Any]) -> ProjectSpecs:
        """
        Validate and parse project specifications into ProjectSpecs object.
        
        Args:
            project_specs: Raw project specification dictionary
        
        Returns:
            ProjectSpecs: Validated project specifications
        
        Raises:
            InvalidProjectSpecsError: If specifications are invalid
        """
        required_fields = ['task_count', 'requirements_clarity', 'architectural_complexity', 'risk_level']
        
        # Check for required fields
        missing_fields = [field for field in required_fields if field not in project_specs]
        if missing_fields:
            raise InvalidProjectSpecsError(
                message=f"Missing required fields: {missing_fields}",
                error_code=ErrorCodes.INVALID_TASK_COUNT,
                context={'missing_fields': missing_fields}
            )
        
        try:
            # Parse and validate individual fields
            task_count = int(project_specs['task_count'])
            requirements_clarity = float(project_specs['requirements_clarity'])
            architectural_complexity = int(project_specs['architectural_complexity'])
            risk_level_str = str(project_specs['risk_level']).upper()
            
            # Validate risk level enum
            try:
                risk_level = RiskLevel(risk_level_str)
            except ValueError:
                raise InvalidProjectSpecsError(
                    message=f"Invalid risk level: {risk_level_str}. Must be LOW, MEDIUM, or HIGH",
                    error_code=ErrorCodes.INVALID_RISK_LEVEL,
                    context={'provided_risk_level': risk_level_str}
                )
            
            # Create ProjectSpecs object (this will validate ranges)
            return ProjectSpecs(
                task_count=task_count,
                requirements_clarity=requirements_clarity,
                architectural_complexity=architectural_complexity,
                risk_level=risk_level,
                name=project_specs.get('name', 'Unnamed Project'),
                description=project_specs.get('description', '')
            )
            
        except ValueError as e:
            raise InvalidProjectSpecsError(
                message=f"Invalid data types in project specifications: {e}",
                error_code=ErrorCodes.INVALID_TASK_COUNT,
                context={'validation_error': str(e)}
            )
        except Exception as e:
            # ProjectSpecs validation errors
            if "Task count must be at least 1" in str(e):
                error_code = ErrorCodes.INVALID_TASK_COUNT
            elif "Requirements clarity must be between 0 and 100" in str(e):
                error_code = ErrorCodes.INVALID_CLARITY_PERCENTAGE
            elif "Architectural complexity must be between 1 and 10" in str(e):
                error_code = ErrorCodes.INVALID_COMPLEXITY_SCORE
            else:
                error_code = ErrorCodes.INVALID_TASK_COUNT
            
            raise InvalidProjectSpecsError(
                message=f"Project specification validation failed: {e}",
                error_code=error_code,
                context={'validation_error': str(e)}
            )
    
    def _apply_selection_logic(self, specs: ProjectSpecs) -> Tuple[WorkflowMode, Dict[str, Any]]:
        """
        Apply workflow selection logic based on project specifications.
        
        Args:
            specs: Validated project specifications
        
        Returns:
            Tuple of (WorkflowMode, decision rationale dictionary)
        """
        decision_factors = {}
        sequential_votes = 0
        ci_ar_votes = 0
        
        # Factor 1: Task count threshold
        if specs.task_count < self.task_count_threshold:
            decision_factors['task_count'] = 'SEQUENTIAL'
            sequential_votes += 1
        else:
            decision_factors['task_count'] = 'CI_AR'
            ci_ar_votes += 1
        
        # Factor 2: Requirements clarity
        if specs.requirements_clarity > self.clarity_threshold:
            decision_factors['requirements_clarity'] = 'SEQUENTIAL'
            sequential_votes += 1
        else:
            decision_factors['requirements_clarity'] = 'CI_AR'
            ci_ar_votes += 1
        
        # Factor 3: Architectural complexity
        if specs.architectural_complexity <= self.complexity_threshold:
            decision_factors['architectural_complexity'] = 'SEQUENTIAL'
            sequential_votes += 1
        else:
            decision_factors['architectural_complexity'] = 'CI_AR'
            ci_ar_votes += 1
        
        # Factor 4: Risk level
        if specs.risk_level in self.sequential_risk_levels:
            decision_factors['risk_level'] = 'SEQUENTIAL'
            sequential_votes += 1
        else:
            decision_factors['risk_level'] = 'CI_AR'
            ci_ar_votes += 1
        
        # Determine workflow mode based on majority vote
        if sequential_votes > ci_ar_votes:
            selected_mode = WorkflowMode.SEQUENTIAL
        else:
            selected_mode = WorkflowMode.CI_AR
        
        # Build decision rationale
        decision_rationale = {
            'selected_mode': selected_mode.value,
            'sequential_votes': sequential_votes,
            'ci_ar_votes': ci_ar_votes,
            'decision_factors': decision_factors,
            'thresholds_used': {
                'task_count_threshold': self.task_count_threshold,
                'clarity_threshold': self.clarity_threshold,
                'complexity_threshold': self.complexity_threshold,
                'sequential_risk_levels': [level.value for level in self.sequential_risk_levels]
            },
            'project_values': {
                'task_count': specs.task_count,
                'requirements_clarity': specs.requirements_clarity,
                'architectural_complexity': specs.architectural_complexity,
                'risk_level': specs.risk_level.value
            }
        }
        
        return selected_mode, decision_rationale
    
    def _log_decision(
        self, 
        specs: ProjectSpecs, 
        workflow_mode: WorkflowMode, 
        decision_rationale: Dict[str, Any]
    ) -> None:
        """
        Log the workflow selection decision with structured information.
        
        Args:
            specs: Project specifications
            workflow_mode: Selected workflow mode
            decision_rationale: Decision rationale data
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'project_name': specs.name,
            'selected_workflow': workflow_mode.value,
            'decision_rationale': decision_rationale
        }
        
        logger.info(
            f"Workflow selection completed: {workflow_mode.value} selected for project '{specs.name}'",
            extra={'workflow_selection': log_data}
        )
        
        # Log detailed decision breakdown
        logger.debug(
            f"Decision breakdown - Sequential votes: {decision_rationale['sequential_votes']}, "
            f"CI/AR votes: {decision_rationale['ci_ar_votes']}, "
            f"Factors: {decision_rationale['decision_factors']}"
        )
    
    def update_thresholds(
        self,
        task_count_threshold: int = None,
        clarity_threshold: float = None,
        complexity_threshold: int = None,
        sequential_risk_levels: set = None
    ) -> None:
        """
        Update workflow selection thresholds for customization.
        
        Args:
            task_count_threshold: New task count threshold
            clarity_threshold: New requirements clarity threshold
            complexity_threshold: New architectural complexity threshold
            sequential_risk_levels: New set of risk levels for sequential mode
        """
        if task_count_threshold is not None:
            if task_count_threshold < 1:
                raise ValueError("Task count threshold must be at least 1")
            self.task_count_threshold = task_count_threshold
        
        if clarity_threshold is not None:
            if not 0 <= clarity_threshold <= 100:
                raise ValueError("Clarity threshold must be between 0 and 100")
            self.clarity_threshold = clarity_threshold
        
        if complexity_threshold is not None:
            if not 1 <= complexity_threshold <= 10:
                raise ValueError("Complexity threshold must be between 1 and 10")
            self.complexity_threshold = complexity_threshold
        
        if sequential_risk_levels is not None:
            if not all(isinstance(level, RiskLevel) for level in sequential_risk_levels):
                raise ValueError("Sequential risk levels must be RiskLevel enum values")
            self.sequential_risk_levels = sequential_risk_levels
        
        logger.info(f"Workflow selection thresholds updated: "
                   f"task_count={self.task_count_threshold}, "
                   f"clarity={self.clarity_threshold}, "
                   f"complexity={self.complexity_threshold}, "
                   f"risk_levels={[level.value for level in self.sequential_risk_levels]}")
    
    def get_current_thresholds(self) -> Dict[str, Any]:
        """
        Get current workflow selection thresholds.
        
        Returns:
            Dictionary containing current threshold values
        """
        return {
            'task_count_threshold': self.task_count_threshold,
            'clarity_threshold': self.clarity_threshold,
            'complexity_threshold': self.complexity_threshold,
            'sequential_risk_levels': [level.value for level in self.sequential_risk_levels]
        }
