"""
P.I.T.C.E.S. Framework - Parallel Integrated Task Contexting Engine System
Hybrid workflow system with Sequential Waterfall and CI/AR modes for JAEGIS v2.2 integration
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import uuid
import time

logger = logging.getLogger(__name__)


class WorkflowMode(str, Enum):
    """P.I.T.C.E.S. workflow modes."""
    SEQUENTIAL_WATERFALL = "sequential_waterfall"
    CI_AR = "ci_ar"  # Continuous Integration / Adaptive Reasoning
    HYBRID = "hybrid"
    AUTO_SELECT = "auto_select"


class TaskComplexity(str, Enum):
    """Task complexity levels for intelligent mode selection."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


@dataclass
class PITCESTask:
    """P.I.T.C.E.S. task definition."""
    task_id: str
    name: str
    description: str
    complexity: TaskComplexity
    dependencies: List[str]
    estimated_duration: timedelta
    required_resources: List[str]
    jaegis_commands: List[str]
    validation_criteria: List[str]
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


@dataclass
class WorkflowContext:
    """Workflow execution context."""
    workflow_id: str
    project_name: str
    mode: WorkflowMode
    complexity_metrics: Dict[str, float]
    resource_availability: Dict[str, bool]
    performance_targets: Dict[str, float]
    jaegis_integration: Dict[str, Any]
    nlds_integration: Dict[str, Any]


@dataclass
class ExecutionMetrics:
    """Workflow execution metrics."""
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    blocked_tasks: int
    average_execution_time: float
    resource_utilization: Dict[str, float]
    performance_score: float
    jaegis_coordination_efficiency: float


class PITCESFramework:
    """
    P.I.T.C.E.S. Framework - Parallel Integrated Task Contexting Engine System
    
    Hybrid workflow system that intelligently selects between Sequential Waterfall
    and CI/AR modes based on project complexity metrics, integrating seamlessly
    with JAEGIS v2.2 and N.L.D.S. Tier 0 component.
    """
    
    def __init__(self, jaegis_interface=None, nlds_interface=None):
        self.jaegis_interface = jaegis_interface
        self.nlds_interface = nlds_interface
        
        # Active workflows
        self.active_workflows: Dict[str, WorkflowContext] = {}
        self.workflow_tasks: Dict[str, List[PITCESTask]] = {}
        self.execution_metrics: Dict[str, ExecutionMetrics] = {}
        
        # Complexity analysis thresholds
        self.complexity_thresholds = {
            "task_count": {"simple": 5, "moderate": 15, "complex": 50, "highly_complex": float('inf')},
            "dependency_ratio": {"simple": 0.2, "moderate": 0.4, "complex": 0.7, "highly_complex": float('inf')},
            "resource_diversity": {"simple": 3, "moderate": 6, "complex": 12, "highly_complex": float('inf')},
            "estimated_duration_hours": {"simple": 8, "moderate": 40, "complex": 200, "highly_complex": float('inf')}
        }
        
        # Mode selection criteria
        self.mode_selection_criteria = {
            WorkflowMode.SEQUENTIAL_WATERFALL: {
                "best_for": ["well_defined_requirements", "linear_dependencies", "stable_scope"],
                "complexity_preference": [TaskComplexity.SIMPLE, TaskComplexity.MODERATE],
                "resource_efficiency": 0.85,
                "predictability": 0.90
            },
            WorkflowMode.CI_AR: {
                "best_for": ["adaptive_requirements", "parallel_execution", "iterative_development"],
                "complexity_preference": [TaskComplexity.COMPLEX, TaskComplexity.HIGHLY_COMPLEX],
                "resource_efficiency": 0.75,
                "adaptability": 0.95
            }
        }
        
        logger.info("P.I.T.C.E.S. Framework initialized")
    
    async def create_workflow(self, project_name: str, tasks: List[Dict[str, Any]], 
                            mode: WorkflowMode = WorkflowMode.AUTO_SELECT) -> str:
        """Create new P.I.T.C.E.S. workflow."""
        
        workflow_id = str(uuid.uuid4())
        
        # Convert task definitions to PITCESTask objects
        pitces_tasks = []
        for task_data in tasks:
            task = PITCESTask(
                task_id=task_data.get('task_id', str(uuid.uuid4())),
                name=task_data['name'],
                description=task_data['description'],
                complexity=TaskComplexity(task_data.get('complexity', 'moderate')),
                dependencies=task_data.get('dependencies', []),
                estimated_duration=timedelta(hours=task_data.get('estimated_hours', 1)),
                required_resources=task_data.get('required_resources', []),
                jaegis_commands=task_data.get('jaegis_commands', []),
                validation_criteria=task_data.get('validation_criteria', [])
            )
            pitces_tasks.append(task)
        
        # Analyze project complexity
        complexity_metrics = self._analyze_project_complexity(pitces_tasks)
        
        # Select optimal workflow mode
        if mode == WorkflowMode.AUTO_SELECT:
            selected_mode = self._select_optimal_mode(complexity_metrics, pitces_tasks)
        else:
            selected_mode = mode
        
        # Create workflow context
        context = WorkflowContext(
            workflow_id=workflow_id,
            project_name=project_name,
            mode=selected_mode,
            complexity_metrics=complexity_metrics,
            resource_availability={},
            performance_targets={
                "completion_time_hours": sum(task.estimated_duration.total_seconds() / 3600 for task in pitces_tasks),
                "success_rate": 0.95,
                "resource_efficiency": 0.80
            },
            jaegis_integration={
                "enabled": self.jaegis_interface is not None,
                "coordination_mode": "enhanced" if selected_mode == WorkflowMode.CI_AR else "standard"
            },
            nlds_integration={
                "enabled": self.nlds_interface is not None,
                "natural_language_processing": True
            }
        )
        
        # Store workflow
        self.active_workflows[workflow_id] = context
        self.workflow_tasks[workflow_id] = pitces_tasks
        
        # Initialize metrics
        self.execution_metrics[workflow_id] = ExecutionMetrics(
            total_tasks=len(pitces_tasks),
            completed_tasks=0,
            failed_tasks=0,
            blocked_tasks=0,
            average_execution_time=0.0,
            resource_utilization={},
            performance_score=1.0,
            jaegis_coordination_efficiency=1.0
        )
        
        logger.info(f"Created P.I.T.C.E.S. workflow {workflow_id} with mode {selected_mode.value}")
        
        return workflow_id
    
    def _analyze_project_complexity(self, tasks: List[PITCESTask]) -> Dict[str, float]:
        """Analyze project complexity metrics."""
        
        total_tasks = len(tasks)
        total_dependencies = sum(len(task.dependencies) for task in tasks)
        dependency_ratio = total_dependencies / total_tasks if total_tasks > 0 else 0
        
        unique_resources = set()
        for task in tasks:
            unique_resources.update(task.required_resources)
        resource_diversity = len(unique_resources)
        
        total_duration = sum(task.estimated_duration.total_seconds() / 3600 for task in tasks)
        
        complexity_counts = {complexity: 0 for complexity in TaskComplexity}
        for task in tasks:
            complexity_counts[task.complexity] += 1
        
        # Calculate weighted complexity score
        complexity_weights = {
            TaskComplexity.SIMPLE: 1,
            TaskComplexity.MODERATE: 2,
            TaskComplexity.COMPLEX: 4,
            TaskComplexity.HIGHLY_COMPLEX: 8
        }
        
        weighted_complexity = sum(
            complexity_counts[complexity] * complexity_weights[complexity]
            for complexity in TaskComplexity
        ) / total_tasks if total_tasks > 0 else 0
        
        return {
            "task_count": total_tasks,
            "dependency_ratio": dependency_ratio,
            "resource_diversity": resource_diversity,
            "estimated_duration_hours": total_duration,
            "weighted_complexity": weighted_complexity,
            "parallel_potential": self._calculate_parallel_potential(tasks),
            "uncertainty_factor": self._calculate_uncertainty_factor(tasks)
        }
    
    def _calculate_parallel_potential(self, tasks: List[PITCESTask]) -> float:
        """Calculate potential for parallel execution."""
        
        if not tasks:
            return 0.0
        
        # Build dependency graph
        dependency_graph = {}
        for task in tasks:
            dependency_graph[task.task_id] = task.dependencies
        
        # Calculate maximum parallel paths
        independent_tasks = [task for task in tasks if not task.dependencies]
        parallel_potential = len(independent_tasks) / len(tasks)
        
        return min(1.0, parallel_potential)
    
    def _calculate_uncertainty_factor(self, tasks: List[PITCESTask]) -> float:
        """Calculate uncertainty factor based on task characteristics."""
        
        if not tasks:
            return 0.0
        
        # Factors that increase uncertainty
        complex_tasks = sum(1 for task in tasks if task.complexity in [TaskComplexity.COMPLEX, TaskComplexity.HIGHLY_COMPLEX])
        high_dependency_tasks = sum(1 for task in tasks if len(task.dependencies) > 3)
        
        uncertainty_score = (complex_tasks + high_dependency_tasks) / (len(tasks) * 2)
        
        return min(1.0, uncertainty_score)
    
    def _select_optimal_mode(self, complexity_metrics: Dict[str, float], tasks: List[PITCESTask]) -> WorkflowMode:
        """Select optimal workflow mode based on complexity analysis."""
        
        # Score each mode based on project characteristics
        mode_scores = {}
        
        for mode in [WorkflowMode.SEQUENTIAL_WATERFALL, WorkflowMode.CI_AR]:
            score = 0.0
            criteria = self.mode_selection_criteria[mode]
            
            # Complexity preference scoring
            avg_complexity = complexity_metrics["weighted_complexity"]
            if avg_complexity <= 2 and TaskComplexity.SIMPLE in criteria["complexity_preference"]:
                score += 0.3
            elif avg_complexity <= 4 and TaskComplexity.MODERATE in criteria["complexity_preference"]:
                score += 0.3
            elif avg_complexity <= 6 and TaskComplexity.COMPLEX in criteria["complexity_preference"]:
                score += 0.3
            elif avg_complexity > 6 and TaskComplexity.HIGHLY_COMPLEX in criteria["complexity_preference"]:
                score += 0.3
            
            # Parallel potential scoring
            parallel_potential = complexity_metrics["parallel_potential"]
            if mode == WorkflowMode.CI_AR and parallel_potential > 0.5:
                score += 0.2
            elif mode == WorkflowMode.SEQUENTIAL_WATERFALL and parallel_potential <= 0.3:
                score += 0.2
            
            # Uncertainty factor scoring
            uncertainty = complexity_metrics["uncertainty_factor"]
            if mode == WorkflowMode.CI_AR and uncertainty > 0.4:
                score += 0.2
            elif mode == WorkflowMode.SEQUENTIAL_WATERFALL and uncertainty <= 0.3:
                score += 0.2
            
            # Resource efficiency consideration
            if complexity_metrics["resource_diversity"] <= 5:
                score += criteria.get("resource_efficiency", 0) * 0.3
            
            mode_scores[mode] = score
        
        # Select mode with highest score
        optimal_mode = max(mode_scores, key=mode_scores.get)
        
        # Use hybrid mode if scores are close
        if abs(mode_scores[WorkflowMode.SEQUENTIAL_WATERFALL] - mode_scores[WorkflowMode.CI_AR]) < 0.1:
            optimal_mode = WorkflowMode.HYBRID
        
        logger.info(f"Mode selection scores: {mode_scores}, selected: {optimal_mode.value}")
        
        return optimal_mode
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute P.I.T.C.E.S. workflow."""
        
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        context = self.active_workflows[workflow_id]
        tasks = self.workflow_tasks[workflow_id]
        
        logger.info(f"Executing workflow {workflow_id} in {context.mode.value} mode")
        
        if context.mode == WorkflowMode.SEQUENTIAL_WATERFALL:
            return await self._execute_sequential_waterfall(workflow_id, tasks)
        elif context.mode == WorkflowMode.CI_AR:
            return await self._execute_ci_ar(workflow_id, tasks)
        elif context.mode == WorkflowMode.HYBRID:
            return await self._execute_hybrid(workflow_id, tasks)
        else:
            raise ValueError(f"Unsupported workflow mode: {context.mode}")
    
    async def _execute_sequential_waterfall(self, workflow_id: str, tasks: List[PITCESTask]) -> Dict[str, Any]:
        """Execute workflow in Sequential Waterfall mode."""
        
        # Sort tasks by dependencies (topological sort)
        sorted_tasks = self._topological_sort(tasks)
        
        execution_results = []
        
        for task in sorted_tasks:
            # Check dependencies
            if not await self._check_dependencies_completed(task, workflow_id):
                task.status = TaskStatus.BLOCKED
                continue
            
            # Execute task
            result = await self._execute_task(task, workflow_id)
            execution_results.append(result)
            
            # Update metrics
            await self._update_execution_metrics(workflow_id)
            
            # Stop on failure if in strict waterfall mode
            if task.status == TaskStatus.FAILED:
                logger.error(f"Task {task.task_id} failed, stopping waterfall execution")
                break
        
        return {
            "workflow_id": workflow_id,
            "mode": "sequential_waterfall",
            "execution_results": execution_results,
            "metrics": asdict(self.execution_metrics[workflow_id])
        }
    
    async def _execute_ci_ar(self, workflow_id: str, tasks: List[PITCESTask]) -> Dict[str, Any]:
        """Execute workflow in CI/AR (Continuous Integration / Adaptive Reasoning) mode."""
        
        # Group tasks by dependency levels for parallel execution
        execution_levels = self._group_tasks_by_dependency_level(tasks)
        
        execution_results = []
        
        for level, level_tasks in execution_levels.items():
            # Execute tasks in parallel within each level
            level_results = await asyncio.gather(
                *[self._execute_task(task, workflow_id) for task in level_tasks],
                return_exceptions=True
            )
            
            execution_results.extend(level_results)
            
            # Update metrics after each level
            await self._update_execution_metrics(workflow_id)
            
            # Adaptive reasoning: adjust strategy based on results
            await self._adaptive_reasoning_adjustment(workflow_id, level_results)
        
        return {
            "workflow_id": workflow_id,
            "mode": "ci_ar",
            "execution_results": execution_results,
            "metrics": asdict(self.execution_metrics[workflow_id])
        }
    
    async def _execute_hybrid(self, workflow_id: str, tasks: List[PITCESTask]) -> Dict[str, Any]:
        """Execute workflow in Hybrid mode."""
        
        # Analyze tasks and split between sequential and parallel execution
        sequential_tasks = [task for task in tasks if len(task.dependencies) > 2 or task.complexity == TaskComplexity.HIGHLY_COMPLEX]
        parallel_tasks = [task for task in tasks if task not in sequential_tasks]
        
        execution_results = []
        
        # Execute sequential tasks first
        if sequential_tasks:
            sequential_results = await self._execute_sequential_waterfall(workflow_id, sequential_tasks)
            execution_results.extend(sequential_results["execution_results"])
        
        # Execute parallel tasks
        if parallel_tasks:
            parallel_results = await self._execute_ci_ar(workflow_id, parallel_tasks)
            execution_results.extend(parallel_results["execution_results"])
        
        return {
            "workflow_id": workflow_id,
            "mode": "hybrid",
            "execution_results": execution_results,
            "metrics": asdict(self.execution_metrics[workflow_id])
        }
    
    def _topological_sort(self, tasks: List[PITCESTask]) -> List[PITCESTask]:
        """Perform topological sort on tasks based on dependencies."""
        
        # Build adjacency list and in-degree count
        task_map = {task.task_id: task for task in tasks}
        in_degree = {task.task_id: 0 for task in tasks}
        adj_list = {task.task_id: [] for task in tasks}
        
        for task in tasks:
            for dep in task.dependencies:
                if dep in task_map:
                    adj_list[dep].append(task.task_id)
                    in_degree[task.task_id] += 1
        
        # Kahn's algorithm
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        sorted_tasks = []
        
        while queue:
            current = queue.pop(0)
            sorted_tasks.append(task_map[current])
            
            for neighbor in adj_list[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return sorted_tasks
    
    def _group_tasks_by_dependency_level(self, tasks: List[PITCESTask]) -> Dict[int, List[PITCESTask]]:
        """Group tasks by dependency level for parallel execution."""
        
        task_map = {task.task_id: task for task in tasks}
        levels = {}
        
        def get_task_level(task_id: str, visited: set) -> int:
            if task_id in visited:
                return 0  # Circular dependency, assign to level 0
            
            visited.add(task_id)
            task = task_map.get(task_id)
            if not task or not task.dependencies:
                return 0
            
            max_dep_level = max(get_task_level(dep, visited.copy()) for dep in task.dependencies if dep in task_map)
            return max_dep_level + 1
        
        for task in tasks:
            level = get_task_level(task.task_id, set())
            if level not in levels:
                levels[level] = []
            levels[level].append(task)
        
        return levels
    
    async def _execute_task(self, task: PITCESTask, workflow_id: str) -> Dict[str, Any]:
        """Execute individual task."""
        
        task.status = TaskStatus.EXECUTING
        task.start_time = datetime.now()
        
        try:
            # Integrate with JAEGIS if available
            if self.jaegis_interface and task.jaegis_commands:
                jaegis_results = []
                for command in task.jaegis_commands:
                    result = await self.jaegis_interface.execute_command(command)
                    jaegis_results.append(result)
                task.result = {"jaegis_results": jaegis_results}
            else:
                # Simulate task execution
                await asyncio.sleep(0.1)  # Simulate work
                task.result = {"status": "completed", "output": f"Task {task.name} completed successfully"}
            
            task.status = TaskStatus.COMPLETED
            task.completion_time = datetime.now()
            
            logger.info(f"Task {task.task_id} completed successfully")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.completion_time = datetime.now()
            
            logger.error(f"Task {task.task_id} failed: {e}")
        
        return {
            "task_id": task.task_id,
            "status": task.status.value,
            "result": task.result,
            "error": task.error_message,
            "execution_time": (task.completion_time - task.start_time).total_seconds() if task.completion_time else None
        }
    
    async def _check_dependencies_completed(self, task: PITCESTask, workflow_id: str) -> bool:
        """Check if all task dependencies are completed."""
        
        workflow_tasks = self.workflow_tasks[workflow_id]
        task_map = {t.task_id: t for t in workflow_tasks}
        
        for dep_id in task.dependencies:
            if dep_id in task_map:
                dep_task = task_map[dep_id]
                if dep_task.status != TaskStatus.COMPLETED:
                    return False
        
        return True
    
    async def _adaptive_reasoning_adjustment(self, workflow_id: str, level_results: List[Any]):
        """Apply adaptive reasoning adjustments based on execution results."""
        
        # Analyze results and adjust strategy
        failed_tasks = [result for result in level_results if isinstance(result, dict) and result.get("status") == "failed"]
        
        if len(failed_tasks) > len(level_results) * 0.3:  # More than 30% failure rate
            logger.warning(f"High failure rate detected in workflow {workflow_id}, applying adaptive adjustments")
            
            # Implement adaptive strategies
            # 1. Increase resource allocation
            # 2. Add retry mechanisms
            # 3. Adjust task priorities
            # 4. Enable additional validation
        
        # Update workflow context with learned insights
        context = self.active_workflows[workflow_id]
        if "adaptive_adjustments" not in context.jaegis_integration:
            context.jaegis_integration["adaptive_adjustments"] = []
        
        context.jaegis_integration["adaptive_adjustments"].append({
            "timestamp": datetime.now().isoformat(),
            "adjustment_type": "failure_rate_response",
            "details": f"Applied adjustments due to {len(failed_tasks)} failures"
        })
    
    async def _update_execution_metrics(self, workflow_id: str):
        """Update execution metrics for workflow."""
        
        tasks = self.workflow_tasks[workflow_id]
        metrics = self.execution_metrics[workflow_id]
        
        metrics.completed_tasks = sum(1 for task in tasks if task.status == TaskStatus.COMPLETED)
        metrics.failed_tasks = sum(1 for task in tasks if task.status == TaskStatus.FAILED)
        metrics.blocked_tasks = sum(1 for task in tasks if task.status == TaskStatus.BLOCKED)
        
        # Calculate average execution time
        completed_tasks_with_time = [
            task for task in tasks 
            if task.status == TaskStatus.COMPLETED and task.start_time and task.completion_time
        ]
        
        if completed_tasks_with_time:
            total_time = sum(
                (task.completion_time - task.start_time).total_seconds()
                for task in completed_tasks_with_time
            )
            metrics.average_execution_time = total_time / len(completed_tasks_with_time)
        
        # Calculate performance score
        if metrics.total_tasks > 0:
            completion_rate = metrics.completed_tasks / metrics.total_tasks
            failure_penalty = metrics.failed_tasks / metrics.total_tasks * 0.5
            metrics.performance_score = max(0.0, completion_rate - failure_penalty)
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get current workflow status."""
        
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        context = self.active_workflows[workflow_id]
        tasks = self.workflow_tasks[workflow_id]
        metrics = self.execution_metrics[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "project_name": context.project_name,
            "mode": context.mode.value,
            "complexity_metrics": context.complexity_metrics,
            "execution_metrics": asdict(metrics),
            "task_summary": {
                "total": len(tasks),
                "pending": sum(1 for task in tasks if task.status == TaskStatus.PENDING),
                "executing": sum(1 for task in tasks if task.status == TaskStatus.EXECUTING),
                "completed": sum(1 for task in tasks if task.status == TaskStatus.COMPLETED),
                "failed": sum(1 for task in tasks if task.status == TaskStatus.FAILED),
                "blocked": sum(1 for task in tasks if task.status == TaskStatus.BLOCKED)
            },
            "jaegis_integration": context.jaegis_integration,
            "nlds_integration": context.nlds_integration
        }


# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize P.I.T.C.E.S. framework
        pitces = PITCESFramework()
        
        # Define sample tasks
        sample_tasks = [
            {
                "name": "Setup Development Environment",
                "description": "Configure development environment and dependencies",
                "complexity": "simple",
                "estimated_hours": 2,
                "jaegis_commands": ["FRED:SETUP --env=development"]
            },
            {
                "name": "Implement Core Features",
                "description": "Develop main application features",
                "complexity": "complex",
                "dependencies": ["task_1"],
                "estimated_hours": 16,
                "jaegis_commands": ["FRED:IMPLEMENT --component=core"]
            },
            {
                "name": "Testing and Validation",
                "description": "Comprehensive testing and quality assurance",
                "complexity": "moderate",
                "dependencies": ["task_2"],
                "estimated_hours": 8,
                "jaegis_commands": ["TYLER:VALIDATE --scope=comprehensive"]
            }
        ]
        
        # Create workflow
        workflow_id = await pitces.create_workflow("Sample Project", sample_tasks)
        
        # Execute workflow
        result = await pitces.execute_workflow(workflow_id)
        
        print("P.I.T.C.E.S. Workflow Execution Result:")
        print(json.dumps(result, indent=2, default=str))
    
    asyncio.run(main())
