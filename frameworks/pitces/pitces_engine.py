#!/usr/bin/env python3
"""
P.I.T.C.E.S. Framework Engine
Parallel Integrated Task Contexting Engine System

This module implements the P.I.T.C.E.S. framework, a hybrid workflow system
that intelligently selects between Sequential Waterfall and CI/AR modes based
on project complexity metrics. Integrates with JAEGIS v2.2 and N.L.D.S. Tier 0
for enhanced AI-driven project management.

P.I.T.C.E.S. Features:
- Intelligent workflow selection based on complexity analysis
- Sequential Waterfall mode for well-defined projects
- CI/AR (Continuous Integration/Adaptive Response) mode for complex projects
- Real-time progress monitoring and adaptive workflow management
- Integration with JAEGIS A.C.I.D. and N.L.D.S. systems
- Comprehensive error handling and recovery mechanisms
"""

import asyncio
import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid
from pathlib import Path
import concurrent.futures
from threading import Lock

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowMode(Enum):
    """P.I.T.C.E.S. workflow modes"""
    SEQUENTIAL_WATERFALL = "sequential_waterfall"
    CIAR = "continuous_integration_adaptive_response"
    HYBRID = "hybrid"
    AUTO_SELECT = "auto_select"

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class ProjectComplexity(Enum):
    """Project complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"

class WorkflowStage(Enum):
    """Workflow execution stages"""
    ANALYSIS = "analysis"
    PLANNING = "planning"
    EXECUTION = "execution"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"

@dataclass
class PITCESTask:
    """P.I.T.C.E.S. task definition"""
    id: str
    name: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: int = 60  # minutes
    priority: int = 5  # 1-10, 10 being highest
    required_resources: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    progress: float = 0.0  # 0.0 to 1.0
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProjectMetrics:
    """Project complexity and performance metrics"""
    total_tasks: int = 0
    dependency_complexity: float = 0.0  # 0.0 to 1.0
    resource_requirements: int = 0
    estimated_duration: int = 0  # minutes
    risk_factors: List[str] = field(default_factory=list)
    team_size: int = 1
    complexity_score: float = 0.0  # 0.0 to 1.0
    recommended_mode: WorkflowMode = WorkflowMode.AUTO_SELECT

@dataclass
class WorkflowExecution:
    """Workflow execution tracking"""
    id: str
    project_name: str
    mode: WorkflowMode
    stage: WorkflowStage
    tasks: List[PITCESTask] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    progress: float = 0.0
    metrics: ProjectMetrics = field(default_factory=ProjectMetrics)
    status: str = "active"
    error_log: List[str] = field(default_factory=list)
    performance_data: Dict[str, Any] = field(default_factory=dict)

class PITCESException(Exception):
    """Base exception for P.I.T.C.E.S. framework"""
    pass

class WorkflowExecutionError(PITCESException):
    """Workflow execution error"""
    pass

class ComplexityAnalysisError(PITCESException):
    """Complexity analysis error"""
    pass

class TaskExecutionError(PITCESException):
    """Task execution error"""
    pass

class ComplexityAnalyzer:
    """Analyzes project complexity to determine optimal workflow mode"""
    
    def __init__(self):
        self.complexity_weights = {
            "task_count": 0.2,
            "dependency_complexity": 0.3,
            "resource_requirements": 0.15,
            "time_constraints": 0.15,
            "risk_factors": 0.1,
            "team_distribution": 0.1
        }
    
    def analyze_project_complexity(
        self,
        tasks: List[PITCESTask],
        constraints: Optional[Dict[str, Any]] = None
    ) -> ProjectMetrics:
        """
        Analyze project complexity and recommend workflow mode
        
        Args:
            tasks: List of project tasks
            constraints: Additional project constraints
            
        Returns:
            ProjectMetrics with complexity analysis
        """
        try:
            constraints = constraints or {}
            
            # Calculate individual complexity factors
            task_complexity = self._calculate_task_complexity(tasks)
            dependency_complexity = self._calculate_dependency_complexity(tasks)
            resource_complexity = self._calculate_resource_complexity(tasks)
            time_complexity = self._calculate_time_complexity(tasks, constraints)
            risk_complexity = self._calculate_risk_complexity(tasks, constraints)
            team_complexity = self._calculate_team_complexity(constraints)
            
            # Calculate weighted complexity score
            complexity_score = (
                task_complexity * self.complexity_weights["task_count"] +
                dependency_complexity * self.complexity_weights["dependency_complexity"] +
                resource_complexity * self.complexity_weights["resource_requirements"] +
                time_complexity * self.complexity_weights["time_constraints"] +
                risk_complexity * self.complexity_weights["risk_factors"] +
                team_complexity * self.complexity_weights["team_distribution"]
            )
            
            # Determine recommended workflow mode
            recommended_mode = self._recommend_workflow_mode(complexity_score)
            
            metrics = ProjectMetrics(
                total_tasks=len(tasks),
                dependency_complexity=dependency_complexity,
                resource_requirements=len(set(
                    resource for task in tasks for resource in task.required_resources
                )),
                estimated_duration=sum(task.estimated_duration for task in tasks),
                risk_factors=self._identify_risk_factors(tasks, constraints),
                team_size=constraints.get("team_size", 1),
                complexity_score=complexity_score,
                recommended_mode=recommended_mode
            )
            
            logger.info(f"Project complexity analysis completed: {complexity_score:.2f} -> {recommended_mode.value}")
            return metrics
            
        except Exception as e:
            logger.error(f"Complexity analysis failed: {e}")
            raise ComplexityAnalysisError(f"Failed to analyze project complexity: {e}")
    
    def _calculate_task_complexity(self, tasks: List[PITCESTask]) -> float:
        """Calculate complexity based on number of tasks"""
        task_count = len(tasks)
        if task_count <= 5:
            return 0.2
        elif task_count <= 15:
            return 0.5
        elif task_count <= 30:
            return 0.8
        else:
            return 1.0
    
    def _calculate_dependency_complexity(self, tasks: List[PITCESTask]) -> float:
        """Calculate complexity based on task dependencies"""
        total_dependencies = sum(len(task.dependencies) for task in tasks)
        if not tasks:
            return 0.0
        
        avg_dependencies = total_dependencies / len(tasks)
        
        # Normalize to 0-1 scale
        if avg_dependencies <= 1:
            return 0.2
        elif avg_dependencies <= 3:
            return 0.5
        elif avg_dependencies <= 5:
            return 0.8
        else:
            return 1.0
    
    def _calculate_resource_complexity(self, tasks: List[PITCESTask]) -> float:
        """Calculate complexity based on resource requirements"""
        unique_resources = set()
        for task in tasks:
            unique_resources.update(task.required_resources)
        
        resource_count = len(unique_resources)
        
        if resource_count <= 3:
            return 0.2
        elif resource_count <= 8:
            return 0.5
        elif resource_count <= 15:
            return 0.8
        else:
            return 1.0
    
    def _calculate_time_complexity(
        self,
        tasks: List[PITCESTask],
        constraints: Dict[str, Any]
    ) -> float:
        """Calculate complexity based on time constraints"""
        total_estimated = sum(task.estimated_duration for task in tasks)
        deadline = constraints.get("deadline_hours", total_estimated / 60 * 2)  # Default: 2x estimated
        
        time_pressure = (total_estimated / 60) / deadline
        
        return min(1.0, time_pressure)
    
    def _calculate_risk_complexity(
        self,
        tasks: List[PITCESTask],
        constraints: Dict[str, Any]
    ) -> float:
        """Calculate complexity based on risk factors"""
        risk_factors = constraints.get("risk_factors", [])
        high_risk_tasks = sum(1 for task in tasks if task.priority >= 8)
        
        risk_score = (len(risk_factors) * 0.1) + (high_risk_tasks / len(tasks) if tasks else 0)
        
        return min(1.0, risk_score)
    
    def _calculate_team_complexity(self, constraints: Dict[str, Any]) -> float:
        """Calculate complexity based on team distribution"""
        team_size = constraints.get("team_size", 1)
        distributed_team = constraints.get("distributed_team", False)
        
        if team_size == 1:
            return 0.1
        elif team_size <= 5:
            return 0.3 if not distributed_team else 0.5
        elif team_size <= 10:
            return 0.6 if not distributed_team else 0.8
        else:
            return 0.8 if not distributed_team else 1.0
    
    def _recommend_workflow_mode(self, complexity_score: float) -> WorkflowMode:
        """Recommend workflow mode based on complexity score"""
        if complexity_score <= 0.3:
            return WorkflowMode.SEQUENTIAL_WATERFALL
        elif complexity_score <= 0.7:
            return WorkflowMode.HYBRID
        else:
            return WorkflowMode.CIAR
    
    def _identify_risk_factors(
        self,
        tasks: List[PITCESTask],
        constraints: Dict[str, Any]
    ) -> List[str]:
        """Identify project risk factors"""
        risks = []
        
        # High dependency tasks
        high_dep_tasks = [t for t in tasks if len(t.dependencies) > 3]
        if high_dep_tasks:
            risks.append("high_dependency_complexity")
        
        # Critical path risks
        critical_tasks = [t for t in tasks if t.priority >= 9]
        if len(critical_tasks) > len(tasks) * 0.3:
            risks.append("high_critical_task_ratio")
        
        # Resource contention
        resource_usage = {}
        for task in tasks:
            for resource in task.required_resources:
                resource_usage[resource] = resource_usage.get(resource, 0) + 1
        
        if any(count > 3 for count in resource_usage.values()):
            risks.append("resource_contention")
        
        # Time pressure
        if constraints.get("tight_deadline", False):
            risks.append("time_pressure")
        
        return risks

class BaseWorkflowMode(ABC):
    """Abstract base class for workflow modes"""
    
    def __init__(self, execution: WorkflowExecution):
        self.execution = execution
        self.is_running = False
        self.performance_metrics = {}
    
    @abstractmethod
    async def execute(self) -> bool:
        """Execute the workflow mode"""
        pass
    
    @abstractmethod
    async def validate_stage(self, stage: WorkflowStage) -> bool:
        """Validate completion of workflow stage"""
        pass
    
    @abstractmethod
    async def handle_failure(self, task: PITCESTask, error: Exception) -> bool:
        """Handle task failure and determine recovery strategy"""
        pass
    
    def update_progress(self):
        """Update overall workflow progress"""
        if not self.execution.tasks:
            self.execution.progress = 0.0
            return
        
        completed_tasks = sum(1 for task in self.execution.tasks if task.status == TaskStatus.COMPLETED)
        self.execution.progress = completed_tasks / len(self.execution.tasks)

class SequentialWaterfallMode(BaseWorkflowMode):
    """Sequential Waterfall workflow mode for well-defined projects"""
    
    async def execute(self) -> bool:
        """Execute sequential waterfall workflow"""
        logger.info("Starting Sequential Waterfall execution")
        self.is_running = True
        
        try:
            # Execute stages sequentially
            stages = [
                WorkflowStage.ANALYSIS,
                WorkflowStage.PLANNING,
                WorkflowStage.EXECUTION,
                WorkflowStage.VALIDATION,
                WorkflowStage.DEPLOYMENT
            ]
            
            for stage in stages:
                self.execution.stage = stage
                logger.info(f"Executing stage: {stage.value}")
                
                # Execute tasks for this stage
                stage_tasks = self._get_stage_tasks(stage)
                for task in stage_tasks:
                    success = await self._execute_task(task)
                    if not success:
                        logger.error(f"Task {task.name} failed in stage {stage.value}")
                        return False
                
                # Validate stage completion
                if not await self.validate_stage(stage):
                    logger.error(f"Stage {stage.value} validation failed")
                    return False
                
                self.update_progress()
            
            self.execution.status = "completed"
            self.execution.end_time = datetime.now()
            logger.info("Sequential Waterfall execution completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Sequential Waterfall execution failed: {e}")
            self.execution.status = "failed"
            self.execution.error_log.append(str(e))
            return False
        finally:
            self.is_running = False
    
    async def validate_stage(self, stage: WorkflowStage) -> bool:
        """Validate stage completion with comprehensive checks"""
        stage_tasks = self._get_stage_tasks(stage)
        
        # Check all tasks completed
        incomplete_tasks = [t for t in stage_tasks if t.status != TaskStatus.COMPLETED]
        if incomplete_tasks:
            logger.warning(f"Stage {stage.value} has incomplete tasks: {[t.name for t in incomplete_tasks]}")
            return False
        
        # Stage-specific validation
        if stage == WorkflowStage.ANALYSIS:
            return self._validate_analysis_stage()
        elif stage == WorkflowStage.PLANNING:
            return self._validate_planning_stage()
        elif stage == WorkflowStage.EXECUTION:
            return self._validate_execution_stage()
        elif stage == WorkflowStage.VALIDATION:
            return self._validate_validation_stage()
        elif stage == WorkflowStage.DEPLOYMENT:
            return self._validate_deployment_stage()
        
        return True
    
    async def handle_failure(self, task: PITCESTask, error: Exception) -> bool:
        """Handle task failure with rollback and retry logic"""
        logger.error(f"Task {task.name} failed: {error}")
        
        # Attempt retry
        if task.metadata.get("retry_count", 0) < 3:
            task.metadata["retry_count"] = task.metadata.get("retry_count", 0) + 1
            task.status = TaskStatus.PENDING
            logger.info(f"Retrying task {task.name} (attempt {task.metadata['retry_count']})")
            return await self._execute_task(task)
        
        # Mark as failed and determine impact
        task.status = TaskStatus.FAILED
        
        # Check if failure is critical
        if task.priority >= 8:
            logger.error(f"Critical task {task.name} failed - stopping workflow")
            return False
        
        # Continue with non-critical failures
        logger.warning(f"Non-critical task {task.name} failed - continuing workflow")
        return True
    
    def _get_stage_tasks(self, stage: WorkflowStage) -> List[PITCESTask]:
        """Get tasks for a specific stage"""
        # Simple stage mapping - in real implementation, this would be more sophisticated
        stage_mapping = {
            WorkflowStage.ANALYSIS: [t for t in self.execution.tasks if "analysis" in t.name.lower()],
            WorkflowStage.PLANNING: [t for t in self.execution.tasks if "plan" in t.name.lower()],
            WorkflowStage.EXECUTION: [t for t in self.execution.tasks if "implement" in t.name.lower() or "develop" in t.name.lower()],
            WorkflowStage.VALIDATION: [t for t in self.execution.tasks if "test" in t.name.lower() or "validate" in t.name.lower()],
            WorkflowStage.DEPLOYMENT: [t for t in self.execution.tasks if "deploy" in t.name.lower()]
        }
        
        return stage_mapping.get(stage, [])
    
    async def _execute_task(self, task: PITCESTask) -> bool:
        """Execute a single task"""
        try:
            task.status = TaskStatus.IN_PROGRESS
            task.start_time = datetime.now()
            
            # Simulate task execution
            await asyncio.sleep(0.1)  # Simulate work
            
            task.status = TaskStatus.COMPLETED
            task.end_time = datetime.now()
            task.progress = 1.0
            
            logger.info(f"Task {task.name} completed successfully")
            return True
            
        except Exception as e:
            return await self.handle_failure(task, e)
    
    def _validate_analysis_stage(self) -> bool:
        """Validate analysis stage completion"""
        # Check if requirements are documented
        return True  # Simplified validation
    
    def _validate_planning_stage(self) -> bool:
        """Validate planning stage completion"""
        # Check if design documents exist
        return True  # Simplified validation
    
    def _validate_execution_stage(self) -> bool:
        """Validate execution stage completion"""
        # Check if implementation is complete
        return True  # Simplified validation
    
    def _validate_validation_stage(self) -> bool:
        """Validate validation stage completion"""
        # Check if tests pass
        return True  # Simplified validation
    
    def _validate_deployment_stage(self) -> bool:
        """Validate deployment stage completion"""
        # Check if deployment is successful
        return True  # Simplified validation

class CIARMode(BaseWorkflowMode):
    """Continuous Integration/Adaptive Response mode for complex projects"""
    
    def __init__(self, execution: WorkflowExecution):
        super().__init__(execution)
        self.parallel_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.feedback_loop_active = True
    
    async def execute(self) -> bool:
        """Execute CI/AR workflow with parallel processing and adaptive response"""
        logger.info("Starting CI/AR execution")
        self.is_running = True
        
        try:
            # Start continuous integration loop
            ci_task = asyncio.create_task(self._continuous_integration_loop())
            
            # Start adaptive response monitoring
            ar_task = asyncio.create_task(self._adaptive_response_loop())
            
            # Execute tasks in parallel where possible
            execution_task = asyncio.create_task(self._parallel_task_execution())
            
            # Wait for completion
            await asyncio.gather(ci_task, ar_task, execution_task)
            
            self.execution.status = "completed"
            self.execution.end_time = datetime.now()
            logger.info("CI/AR execution completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"CI/AR execution failed: {e}")
            self.execution.status = "failed"
            self.execution.error_log.append(str(e))
            return False
        finally:
            self.is_running = False
            self.feedback_loop_active = False
            self.parallel_executor.shutdown(wait=True)
    
    async def _continuous_integration_loop(self):
        """Continuous integration monitoring and validation"""
        while self.is_running:
            try:
                # Validate current state
                await self._validate_current_state()
                
                # Check for integration issues
                await self._check_integration_health()
                
                # Update progress
                self.update_progress()
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"CI loop error: {e}")
                await asyncio.sleep(10)
    
    async def _adaptive_response_loop(self):
        """Adaptive response to changing conditions"""
        while self.feedback_loop_active:
            try:
                # Monitor performance metrics
                await self._monitor_performance()
                
                # Adapt workflow based on feedback
                await self._adapt_workflow()
                
                # Optimize resource allocation
                await self._optimize_resources()
                
                await asyncio.sleep(10)  # Adapt every 10 seconds
                
            except Exception as e:
                logger.error(f"AR loop error: {e}")
                await asyncio.sleep(15)
    
    async def _parallel_task_execution(self):
        """Execute tasks in parallel where dependencies allow"""
        while self.is_running:
            # Find ready tasks (no pending dependencies)
            ready_tasks = self._get_ready_tasks()
            
            if ready_tasks:
                # Execute tasks in parallel
                futures = []
                for task in ready_tasks[:4]:  # Limit concurrent tasks
                    future = self.parallel_executor.submit(self._execute_task_sync, task)
                    futures.append(future)
                
                # Wait for completion
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        if not result:
                            logger.warning("Task execution failed in parallel mode")
                    except Exception as e:
                        logger.error(f"Parallel task execution error: {e}")
            
            # Check if all tasks completed
            if all(task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED] for task in self.execution.tasks):
                break
            
            await asyncio.sleep(1)
    
    def _get_ready_tasks(self) -> List[PITCESTask]:
        """Get tasks that are ready for execution (dependencies satisfied)"""
        ready_tasks = []
        
        for task in self.execution.tasks:
            if task.status == TaskStatus.PENDING:
                # Check if all dependencies are completed
                dependencies_met = all(
                    any(t.id == dep_id and t.status == TaskStatus.COMPLETED 
                        for t in self.execution.tasks)
                    for dep_id in task.dependencies
                ) if task.dependencies else True
                
                if dependencies_met:
                    ready_tasks.append(task)
        
        return ready_tasks
    
    def _execute_task_sync(self, task: PITCESTask) -> bool:
        """Synchronous task execution for thread pool"""
        try:
            task.status = TaskStatus.IN_PROGRESS
            task.start_time = datetime.now()
            
            # Simulate task execution
            time.sleep(0.1)
            
            task.status = TaskStatus.COMPLETED
            task.end_time = datetime.now()
            task.progress = 1.0
            
            logger.info(f"Task {task.name} completed in parallel mode")
            return True
            
        except Exception as e:
            logger.error(f"Task {task.name} failed: {e}")
            task.status = TaskStatus.FAILED
            return False
    
    async def validate_stage(self, stage: WorkflowStage) -> bool:
        """Continuous validation instead of stage-based"""
        return True  # CI/AR mode uses continuous validation
    
    async def handle_failure(self, task: PITCESTask, error: Exception) -> bool:
        """Adaptive failure handling"""
        logger.error(f"Task {task.name} failed: {error}")
        
        # Immediate retry for transient failures
        if "timeout" in str(error).lower() or "network" in str(error).lower():
            task.status = TaskStatus.PENDING
            return True
        
        # Adaptive response - reassign or modify task
        if task.priority >= 7:
            # Try alternative approach
            await self._adapt_task_approach(task)
            return True
        
        # Mark as failed but continue
        task.status = TaskStatus.FAILED
        return True
    
    async def _validate_current_state(self):
        """Validate current workflow state"""
        # Check for deadlocks
        blocked_tasks = [t for t in self.execution.tasks if t.status == TaskStatus.BLOCKED]
        if blocked_tasks:
            logger.warning(f"Detected blocked tasks: {[t.name for t in blocked_tasks]}")
    
    async def _check_integration_health(self):
        """Check integration health"""
        # Simulate integration checks
        pass
    
    async def _monitor_performance(self):
        """Monitor performance metrics"""
        # Calculate throughput
        completed_tasks = [t for t in self.execution.tasks if t.status == TaskStatus.COMPLETED]
        if completed_tasks:
            avg_duration = sum(
                (t.end_time - t.start_time).total_seconds() 
                for t in completed_tasks if t.start_time and t.end_time
            ) / len(completed_tasks)
            
            self.performance_metrics["avg_task_duration"] = avg_duration
    
    async def _adapt_workflow(self):
        """Adapt workflow based on performance"""
        # Adjust parallelism based on performance
        if self.performance_metrics.get("avg_task_duration", 0) > 300:  # 5 minutes
            logger.info("Increasing parallelism due to slow task execution")
    
    async def _optimize_resources(self):
        """Optimize resource allocation"""
        # Resource optimization logic
        pass
    
    async def _adapt_task_approach(self, task: PITCESTask):
        """Adapt task approach for failed tasks"""
        # Modify task parameters or approach
        task.metadata["adapted"] = True
        task.status = TaskStatus.PENDING

class PITCESEngine:
    """
    P.I.T.C.E.S. Engine - Singleton
    
    Main orchestration engine for the Parallel Integrated Task Contexting Engine System.
    Provides intelligent workflow selection and execution management.
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(PITCESEngine, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.complexity_analyzer = ComplexityAnalyzer()
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.execution_history: List[WorkflowExecution] = []
        self.system_metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "average_execution_time": 0.0,
            "system_uptime": datetime.now()
        }
        
        # Integration components (will be initialized when available)
        self.acid_integration = None
        self.nlds_integration = None
        
        self._initialized = True
        logger.info("P.I.T.C.E.S. Engine initialized (Singleton)")
    
    async def execute_project(
        self,
        project_name: str,
        tasks: List[PITCESTask],
        constraints: Optional[Dict[str, Any]] = None,
        force_mode: Optional[WorkflowMode] = None
    ) -> str:
        """
        Execute a project using P.I.T.C.E.S. framework
        
        Args:
            project_name: Name of the project
            tasks: List of project tasks
            constraints: Project constraints and requirements
            force_mode: Force specific workflow mode (overrides analysis)
            
        Returns:
            Execution ID for tracking
        """
        execution_id = str(uuid.uuid4())
        
        try:
            # Analyze project complexity
            if force_mode:
                metrics = ProjectMetrics(recommended_mode=force_mode)
                logger.info(f"Using forced workflow mode: {force_mode.value}")
            else:
                metrics = self.complexity_analyzer.analyze_project_complexity(tasks, constraints)
                logger.info(f"Recommended workflow mode: {metrics.recommended_mode.value}")
            
            # Create workflow execution
            execution = WorkflowExecution(
                id=execution_id,
                project_name=project_name,
                mode=metrics.recommended_mode,
                stage=WorkflowStage.ANALYSIS,
                tasks=tasks,
                metrics=metrics
            )
            
            self.active_executions[execution_id] = execution
            self.system_metrics["total_executions"] += 1
            
            # Execute workflow
            success = await self._execute_workflow(execution)
            
            if success:
                self.system_metrics["successful_executions"] += 1
                logger.info(f"Project {project_name} executed successfully")
            else:
                self.system_metrics["failed_executions"] += 1
                logger.error(f"Project {project_name} execution failed")
            
            # Move to history
            self.execution_history.append(execution)
            del self.active_executions[execution_id]
            
            return execution_id
            
        except Exception as e:
            logger.error(f"Project execution failed: {e}")
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]
            raise WorkflowExecutionError(f"Failed to execute project {project_name}: {e}")
    
    async def _execute_workflow(self, execution: WorkflowExecution) -> bool:
        """Execute workflow using appropriate mode"""
        if execution.mode == WorkflowMode.SEQUENTIAL_WATERFALL:
            workflow = SequentialWaterfallMode(execution)
        elif execution.mode in [WorkflowMode.CIAR, WorkflowMode.HYBRID]:
            workflow = CIARMode(execution)
        else:
            raise WorkflowExecutionError(f"Unsupported workflow mode: {execution.mode}")
        
        return await workflow.execute()
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow execution"""
        execution = self.active_executions.get(execution_id)
        if not execution:
            # Check history
            execution = next(
                (e for e in self.execution_history if e.id == execution_id),
                None
            )
        
        if not execution:
            return None
        
        return {
            "id": execution.id,
            "project_name": execution.project_name,
            "mode": execution.mode.value,
            "stage": execution.stage.value,
            "progress": execution.progress,
            "status": execution.status,
            "start_time": execution.start_time.isoformat(),
            "end_time": execution.end_time.isoformat() if execution.end_time else None,
            "task_count": len(execution.tasks),
            "completed_tasks": len([t for t in execution.tasks if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in execution.tasks if t.status == TaskStatus.FAILED]),
            "error_count": len(execution.error_log)
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get P.I.T.C.E.S. system metrics"""
        uptime = datetime.now() - self.system_metrics["system_uptime"]
        
        return {
            "system_name": "P.I.T.C.E.S. Engine",
            "version": "1.0.0",
            "uptime_seconds": uptime.total_seconds(),
            "active_executions": len(self.active_executions),
            "total_executions": self.system_metrics["total_executions"],
            "successful_executions": self.system_metrics["successful_executions"],
            "failed_executions": self.system_metrics["failed_executions"],
            "success_rate": (
                self.system_metrics["successful_executions"] / 
                max(1, self.system_metrics["total_executions"])
            ),
            "execution_history_size": len(self.execution_history),
            "timestamp": datetime.now().isoformat()
        }
    
    async def integrate_with_acid(self, acid_components: Dict[str, Any]):
        """Integrate with A.C.I.D. components"""
        self.acid_integration = acid_components
        logger.info("P.I.T.C.E.S. integrated with A.C.I.D.")
    
    async def integrate_with_nlds(self, nlds_component: Any):
        """Integrate with N.L.D.S. Tier 0"""
        self.nlds_integration = nlds_component
        logger.info("P.I.T.C.E.S. integrated with N.L.D.S.")

# Example usage and testing
async def main():
    """Example usage of P.I.T.C.E.S. framework"""
    # Initialize P.I.T.C.E.S. engine (singleton)
    pitces = PITCESEngine()
    
    print("🔧 P.I.T.C.E.S. Framework Demo")
    print("=" * 50)
    
    # Create sample tasks
    tasks = [
        PITCESTask(
            id="task_1",
            name="Requirements Analysis",
            description="Analyze project requirements",
            estimated_duration=120,
            priority=8
        ),
        PITCESTask(
            id="task_2",
            name="System Design",
            description="Design system architecture",
            dependencies=["task_1"],
            estimated_duration=180,
            priority=7
        ),
        PITCESTask(
            id="task_3",
            name="Implementation Phase 1",
            description="Implement core functionality",
            dependencies=["task_2"],
            estimated_duration=300,
            priority=6
        ),
        PITCESTask(
            id="task_4",
            name="Testing",
            description="Test implemented features",
            dependencies=["task_3"],
            estimated_duration=120,
            priority=8
        ),
        PITCESTask(
            id="task_5",
            name="Deployment",
            description="Deploy to production",
            dependencies=["task_4"],
            estimated_duration=60,
            priority=9
        )
    ]
    
    # Test simple project (should use Sequential Waterfall)
    print("\n1. Testing Simple Project (Sequential Waterfall)...")
    simple_execution_id = await pitces.execute_project(
        project_name="Simple Web App",
        tasks=tasks[:3],  # Fewer tasks
        constraints={"team_size": 2, "deadline_hours": 24}
    )
    
    status = pitces.get_execution_status(simple_execution_id)
    print(f"   Execution ID: {simple_execution_id}")
    print(f"   Mode: {status['mode']}")
    print(f"   Status: {status['status']}")
    print(f"   Progress: {status['progress']:.1%}")
    
    # Test complex project (should use CI/AR)
    print("\n2. Testing Complex Project (CI/AR Mode)...")
    complex_tasks = tasks + [
        PITCESTask(
            id="task_6",
            name="Performance Optimization",
            description="Optimize system performance",
            dependencies=["task_3"],
            estimated_duration=240,
            priority=7
        ),
        PITCESTask(
            id="task_7",
            name="Security Audit",
            description="Conduct security audit",
            dependencies=["task_4"],
            estimated_duration=180,
            priority=9
        )
    ]
    
    complex_execution_id = await pitces.execute_project(
        project_name="Enterprise Platform",
        tasks=complex_tasks,
        constraints={
            "team_size": 8,
            "distributed_team": True,
            "tight_deadline": True,
            "risk_factors": ["integration_complexity", "performance_requirements"]
        }
    )
    
    status = pitces.get_execution_status(complex_execution_id)
    print(f"   Execution ID: {complex_execution_id}")
    print(f"   Mode: {status['mode']}")
    print(f"   Status: {status['status']}")
    print(f"   Progress: {status['progress']:.1%}")
    
    # Display system metrics
    print("\n📊 P.I.T.C.E.S. System Metrics:")
    metrics = pitces.get_system_metrics()
    print(f"   Total Executions: {metrics['total_executions']}")
    print(f"   Success Rate: {metrics['success_rate']:.1%}")
    print(f"   Active Executions: {metrics['active_executions']}")
    
    print("\n✅ P.I.T.C.E.S. Framework demo completed!")

if __name__ == "__main__":
    asyncio.run(main())