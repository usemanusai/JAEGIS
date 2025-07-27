"""
P.I.T.C.E.S. Exception Hierarchy
Parallel Integrated Task Contexting Engine System

This module defines the custom exception hierarchy for comprehensive error handling.
"""

from typing import Optional, Dict, Any


class PITCESError(Exception):
    """
    Base exception class for all P.I.T.C.E.S. framework errors.
    
    Attributes:
        message: Error description
        error_code: Unique error identifier
        context: Additional error context data
    """
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None, 
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.context = context or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'context': self.context
        }


class WorkflowError(PITCESError):
    """
    Raised when workflow execution encounters an error.
    
    Examples:
        - Invalid workflow state transitions
        - Workflow configuration errors
        - Phase gate validation failures
    """
    pass


class TaskError(PITCESError):
    """
    Raised when task operations fail.
    
    Examples:
        - Task dependency cycles
        - Invalid task state transitions
        - Task execution failures
    """
    pass


class InvalidProjectSpecsError(PITCESError):
    """
    Raised when project specifications are invalid or malformed.
    
    Examples:
        - Missing required fields
        - Invalid value ranges
        - Inconsistent specifications
    """
    pass


class ContextEngineError(PITCESError):
    """
    Raised when context persistence operations fail.
    
    Examples:
        - File system access errors
        - Serialization/deserialization failures
        - Context data corruption
    """
    pass


class PreemptionError(PITCESError):
    """
    Raised when task preemption operations fail.
    
    Examples:
        - Unable to pause task
        - Context serialization failure
        - Resume operation failure
    """
    pass


class TriageError(PITCESError):
    """
    Raised when task triage operations fail.
    
    Examples:
        - Invalid priority classification
        - Queue management errors
        - Escalation failures
    """
    pass


class GapAnalysisError(PITCESError):
    """
    Raised when gap analysis operations fail.
    
    Examples:
        - Audit execution failures
        - Report generation errors
        - Analysis data corruption
    """
    pass


class AgentError(PITCESError):
    """
    Raised when agent operations fail.
    
    Examples:
        - Agent initialization failures
        - Communication errors
        - Resource allocation failures
    """
    pass


class SquadError(PITCESError):
    """
    Raised when squad operations fail.
    
    Examples:
        - Squad coordination failures
        - Resource conflicts
        - Squad communication errors
    """
    pass


class ConfigurationError(PITCESError):
    """
    Raised when configuration is invalid or missing.
    
    Examples:
        - Missing configuration files
        - Invalid configuration values
        - Configuration validation failures
    """
    pass


class ValidationError(PITCESError):
    """
    Raised when data validation fails.
    
    Examples:
        - Invalid input parameters
        - Data type mismatches
        - Constraint violations
    """
    pass


class ResourceError(PITCESError):
    """
    Raised when resource operations fail.
    
    Examples:
        - Insufficient memory
        - File system errors
        - Network connectivity issues
    """
    pass


class TimeoutError(PITCESError):
    """
    Raised when operations exceed time limits.
    
    Examples:
        - Task execution timeouts
        - Network request timeouts
        - Lock acquisition timeouts
    """
    pass


class DependencyError(PITCESError):
    """
    Raised when dependency resolution fails.
    
    Examples:
        - Circular dependencies
        - Missing dependencies
        - Dependency conflicts
    """
    pass


class StateError(PITCESError):
    """
    Raised when state management operations fail.
    
    Examples:
        - Invalid state transitions
        - State corruption
        - State synchronization failures
    """
    pass


class IntegrationError(PITCESError):
    """
    Raised when external system integration fails.
    
    Examples:
        - JAEGIS integration failures
        - GitHub synchronization errors
        - N.L.D.S. communication failures
    """
    pass


# Error code constants for common scenarios
class ErrorCodes:
    """Standard error codes for consistent error handling."""
    
    # Workflow errors
    INVALID_WORKFLOW_STATE = "WF001"
    PHASE_GATE_FAILURE = "WF002"
    WORKFLOW_TIMEOUT = "WF003"
    
    # Task errors
    TASK_DEPENDENCY_CYCLE = "TK001"
    TASK_EXECUTION_FAILURE = "TK002"
    INVALID_TASK_STATE = "TK003"
    
    # Project specification errors
    INVALID_TASK_COUNT = "PS001"
    INVALID_CLARITY_PERCENTAGE = "PS002"
    INVALID_COMPLEXITY_SCORE = "PS003"
    INVALID_RISK_LEVEL = "PS004"
    
    # Context engine errors
    CONTEXT_SAVE_FAILURE = "CE001"
    CONTEXT_LOAD_FAILURE = "CE002"
    CONTEXT_CORRUPTION = "CE003"
    
    # Preemption errors
    PAUSE_FAILURE = "PR001"
    RESUME_FAILURE = "PR002"
    CONTEXT_SWITCH_FAILURE = "PR003"
    
    # Triage errors
    INVALID_PRIORITY = "TR001"
    QUEUE_OVERFLOW = "TR002"
    ESCALATION_FAILURE = "TR003"
    
    # Gap analysis errors
    AUDIT_FAILURE = "GA001"
    REPORT_GENERATION_FAILURE = "GA002"
    ANALYSIS_DATA_CORRUPTION = "GA003"
    
    # Agent/Squad errors
    AGENT_INITIALIZATION_FAILURE = "AG001"
    SQUAD_COORDINATION_FAILURE = "SQ001"
    RESOURCE_ALLOCATION_FAILURE = "RS001"
    
    # Configuration errors
    MISSING_CONFIG = "CF001"
    INVALID_CONFIG_VALUE = "CF002"
    CONFIG_VALIDATION_FAILURE = "CF003"


def create_error_with_context(
    error_class: type,
    message: str,
    error_code: str,
    **context_kwargs
) -> PITCESError:
    """
    Factory function to create errors with standardized context.
    
    Args:
        error_class: Exception class to instantiate
        message: Error message
        error_code: Standard error code
        **context_kwargs: Additional context data
    
    Returns:
        Configured exception instance
    """
    return error_class(
        message=message,
        error_code=error_code,
        context=context_kwargs
    )


def handle_and_reraise(
    original_exception: Exception,
    error_class: type,
    message: str,
    error_code: str,
    **context_kwargs
) -> None:
    """
    Handle an exception and reraise as P.I.T.C.E.S. exception.
    
    Args:
        original_exception: The original exception that occurred
        error_class: P.I.T.C.E.S. exception class to raise
        message: New error message
        error_code: Standard error code
        **context_kwargs: Additional context data
    
    Raises:
        PITCESError: Wrapped exception with additional context
    """
    context = {
        'original_error': str(original_exception),
        'original_type': type(original_exception).__name__,
        **context_kwargs
    }
    
    raise error_class(
        message=f"{message}: {str(original_exception)}",
        error_code=error_code,
        context=context
    ) from original_exception
