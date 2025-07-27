"""
P.I.T.C.E.S. Core Data Models
Parallel Integrated Task Contexting Engine System

This module defines the core data structures and enums used throughout the P.I.T.C.E.S. framework.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4


class Priority(Enum):
    """Task priority levels for triage protocol."""
    CRITICAL = 1  # System-breaking bugs, security vulnerabilities
    HIGH = 2      # Core functional failures
    MEDIUM = 3    # Minor functional errors
    LOW = 4       # Cosmetic issues, documentation updates


class TaskStatus(Enum):
    """Task execution status."""
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class RiskLevel(Enum):
    """Project risk assessment levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WorkflowMode(Enum):
    """Available workflow execution modes."""
    SEQUENTIAL = "SEQUENTIAL"
    CI_AR = "CI_AR"


class PhaseStatus(Enum):
    """Sequential workflow phase status."""
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    BLOCKED = auto()


@dataclass
class Task:
    """
    Core task representation with comprehensive metadata.
    
    Attributes:
        id: Unique task identifier
        name: Human-readable task name
        priority: Task priority level for triage
        status: Current execution status
        dependencies: List of task IDs this task depends on
        estimated_duration: Expected execution time
        context_data: Serializable task state and metadata
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
        assigned_agent: Agent responsible for execution
        completion_percentage: Progress indicator (0-100)
        error_message: Error details if task failed
    """
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.NOT_STARTED
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: timedelta = field(default_factory=lambda: timedelta(hours=1))
    context_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    assigned_agent: Optional[str] = None
    completion_percentage: float = 0.0
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.name:
            raise ValueError("Task name cannot be empty")
        if not 0 <= self.completion_percentage <= 100:
            raise ValueError("Completion percentage must be between 0 and 100")


@dataclass
class ProjectSpecs:
    """
    Project specification for workflow selection.
    
    Attributes:
        task_count: Total number of tasks in project
        requirements_clarity: Percentage of clear requirements (0-100)
        architectural_complexity: Complexity score (1-10)
        risk_level: Overall project risk assessment
        name: Project identifier
        description: Project description
        estimated_duration: Total project duration estimate
        team_size: Number of team members
        budget: Project budget (optional)
    """
    task_count: int
    requirements_clarity: float
    architectural_complexity: int
    risk_level: RiskLevel
    name: str = "Unnamed Project"
    description: str = ""
    estimated_duration: timedelta = field(default_factory=lambda: timedelta(weeks=12))
    team_size: int = 5
    budget: Optional[float] = None
    
    def __post_init__(self):
        """Validate project specifications."""
        if self.task_count < 1:
            raise ValueError("Task count must be at least 1")
        if not 0 <= self.requirements_clarity <= 100:
            raise ValueError("Requirements clarity must be between 0 and 100")
        if not 1 <= self.architectural_complexity <= 10:
            raise ValueError("Architectural complexity must be between 1 and 10")
        if self.team_size < 1:
            raise ValueError("Team size must be at least 1")


@dataclass
class GapAnalysisResult:
    """
    Results from Gap Analysis Squad audit.
    
    Attributes:
        functional_completeness: Feature coverage percentage (0-100)
        security_integrity: Security risk score (1-10, lower is better)
        performance_scalability: Performance metrics dict
        integration_interoperability: Compatibility score (0-100)
        compliance_governance: Compliance percentage (0-100)
        logical_strategic_alignment: Alignment score (0-100)
        documentation_maintainability: Quality score (0-100)
        recommendations: List of actionable recommendations
        priority_score: Overall priority for addressing gaps (1-10)
        audit_timestamp: When audit was performed
    """
    functional_completeness: float
    security_integrity: float
    performance_scalability: Dict[str, float]
    integration_interoperability: float
    compliance_governance: float
    logical_strategic_alignment: float
    documentation_maintainability: float
    recommendations: List[str]
    priority_score: float
    audit_timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate gap analysis results."""
        scores = [
            self.functional_completeness,
            self.integration_interoperability,
            self.compliance_governance,
            self.logical_strategic_alignment,
            self.documentation_maintainability
        ]
        
        for score in scores:
            if not 0 <= score <= 100:
                raise ValueError("Percentage scores must be between 0 and 100")
        
        if not 1 <= self.security_integrity <= 10:
            raise ValueError("Security integrity score must be between 1 and 10")
        
        if not 1 <= self.priority_score <= 10:
            raise ValueError("Priority score must be between 1 and 10")


@dataclass
class WorkflowMetrics:
    """
    Performance and execution metrics for workflow analysis.
    
    Attributes:
        execution_time: Total workflow execution time
        memory_usage_mb: Peak memory usage in megabytes
        overhead_percentage: Computational overhead percentage
        tasks_completed: Number of successfully completed tasks
        tasks_failed: Number of failed tasks
        preemption_count: Number of task preemptions (CI/AR mode)
        context_switches: Number of context switches
        average_response_time: Average response time for task operations
        throughput_tasks_per_hour: Task completion rate
        error_rate: Percentage of failed operations
    """
    execution_time: timedelta = field(default_factory=lambda: timedelta(0))
    memory_usage_mb: float = 0.0
    overhead_percentage: float = 0.0
    tasks_completed: int = 0
    tasks_failed: int = 0
    preemption_count: int = 0
    context_switches: int = 0
    average_response_time: timedelta = field(default_factory=lambda: timedelta(0))
    throughput_tasks_per_hour: float = 0.0
    error_rate: float = 0.0
    
    def calculate_success_rate(self) -> float:
        """Calculate task success rate percentage."""
        total_tasks = self.tasks_completed + self.tasks_failed
        if total_tasks == 0:
            return 0.0
        return (self.tasks_completed / total_tasks) * 100
    
    def calculate_efficiency_score(self) -> float:
        """Calculate overall efficiency score (0-100)."""
        success_rate = self.calculate_success_rate()
        overhead_penalty = max(0, self.overhead_percentage - 10) * 2  # Penalty for >10% overhead
        efficiency = success_rate - overhead_penalty - (self.error_rate * 10)
        return max(0, min(100, efficiency))


@dataclass
class SequentialPhase:
    """
    Sequential workflow phase representation.
    
    Attributes:
        name: Phase name
        status: Current phase status
        tasks: List of tasks in this phase
        start_time: Phase start timestamp
        end_time: Phase completion timestamp
        completion_percentage: Phase progress (0-100)
        gate_criteria: Criteria that must be met to proceed
        gate_passed: Whether phase gate validation passed
    """
    name: str
    status: PhaseStatus = PhaseStatus.NOT_STARTED
    tasks: List[Task] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    completion_percentage: float = 0.0
    gate_criteria: List[str] = field(default_factory=list)
    gate_passed: bool = False
    
    def calculate_completion(self) -> float:
        """Calculate phase completion percentage based on tasks."""
        if not self.tasks:
            return 0.0
        
        total_progress = sum(task.completion_percentage for task in self.tasks)
        return total_progress / len(self.tasks)
    
    def can_proceed_to_next_phase(self) -> bool:
        """Check if phase gate criteria are met."""
        return self.completion_percentage >= 100.0 and self.gate_passed
    
    def validate_gate_criteria(self) -> bool:
        """Validate phase gate criteria and update gate_passed status."""
        # Implementation would check specific criteria
        # For now, simple completion check
        self.gate_passed = self.completion_percentage >= 100.0
        return self.gate_passed
