#!/usr/bin/env python3
"""
UTMES Automatic Task Generation System
Automatically generates main tasks and subtasks based on input analysis
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Core enforcement mechanism
"""

import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Import from input analysis algorithm
from input_analysis_algorithm import (
    UTMESInputAnalyzer, InputAnalysisResult, TaskRequirement, 
    InputType, WorkflowType, PriorityLevel
)

class TaskState(Enum):
    """Task states for UTMES task management"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    CANCELLED = "CANCELLED"

@dataclass
class GeneratedTask:
    """Represents a generated task with all required metadata"""
    task_id: str
    name: str
    description: str
    state: TaskState
    priority: PriorityLevel
    parent_task_id: Optional[str]
    subtasks: List['GeneratedTask']
    deliverables: List[str]
    success_criteria: List[str]
    dependencies: List[str]
    estimated_duration: str
    created_timestamp: str
    automation_level: str

@dataclass
class TaskGenerationResult:
    """Result of automatic task generation"""
    main_tasks: List[GeneratedTask]
    total_task_count: int
    total_subtask_count: int
    generation_timestamp: str
    input_analysis: InputAnalysisResult
    enforcement_level: str

class UTMESTaskGenerator:
    """
    UTMES Automatic Task Generation System
    Generates comprehensive task structures automatically
    """
    
    def __init__(self):
        self.input_analyzer = UTMESInputAnalyzer()
        self.task_templates = self._initialize_task_templates()
        self.subtask_generators = self._initialize_subtask_generators()
        
    def generate_tasks_from_input(self, user_input: str) -> TaskGenerationResult:
        """
        MAIN GENERATION FUNCTION
        Automatically generates complete task structure from user input
        
        Args:
            user_input: Raw user input string
            
        Returns:
            TaskGenerationResult with complete task hierarchy
        """
        # Step 1: Analyze user input
        input_analysis = self.input_analyzer.analyze_user_input(user_input)
        
        # Step 2: Generate main tasks
        main_tasks = self._generate_main_tasks(input_analysis, user_input)
        
        # Step 3: Generate subtasks for each main task
        for main_task in main_tasks:
            main_task.subtasks = self._generate_subtasks(main_task, input_analysis)
        
        # Step 4: Calculate totals
        total_task_count = len(main_tasks)
        total_subtask_count = sum(len(task.subtasks) for task in main_tasks)
        
        # Step 5: Determine enforcement level
        enforcement_level = self._determine_enforcement_level(input_analysis)
        
        return TaskGenerationResult(
            main_tasks=main_tasks,
            total_task_count=total_task_count,
            total_subtask_count=total_subtask_count,
            generation_timestamp=datetime.now().isoformat(),
            input_analysis=input_analysis,
            enforcement_level=enforcement_level
        )
    
    def _generate_main_tasks(self, input_analysis: InputAnalysisResult, user_input: str) -> List[GeneratedTask]:
        """Generate main tasks based on input analysis"""
        main_tasks = []
        
        for task_req in input_analysis.required_tasks:
            main_task = GeneratedTask(
                task_id=self._generate_task_id(),
                name=task_req.name,
                description=task_req.description,
                state=TaskState.NOT_STARTED,
                priority=task_req.priority,
                parent_task_id=None,
                subtasks=[],  # Will be populated later
                deliverables=task_req.deliverables,
                success_criteria=task_req.success_criteria,
                dependencies=task_req.dependencies,
                estimated_duration=self._estimate_duration(task_req, input_analysis.complexity_score),
                created_timestamp=datetime.now().isoformat(),
                automation_level=input_analysis.automation_level
            )
            main_tasks.append(main_task)
        
        # If no tasks were generated from requirements, create default task
        if not main_tasks:
            main_tasks.append(self._create_default_task(user_input, input_analysis))
        
        return main_tasks
    
    def _generate_subtasks(self, main_task: GeneratedTask, input_analysis: InputAnalysisResult) -> List[GeneratedTask]:
        """Generate subtasks for a main task"""
        subtasks = []
        
        # Determine subtask generation strategy based on main task type
        if "Planning" in main_task.name:
            subtasks = self._generate_planning_subtasks(main_task, input_analysis)
        elif "Implementation" in main_task.name or "Development" in main_task.name:
            subtasks = self._generate_implementation_subtasks(main_task, input_analysis)
        elif "Analysis" in main_task.name:
            subtasks = self._generate_analysis_subtasks(main_task, input_analysis)
        elif "Documentation" in main_task.name:
            subtasks = self._generate_documentation_subtasks(main_task, input_analysis)
        elif "Architecture" in main_task.name or "Design" in main_task.name:
            subtasks = self._generate_architecture_subtasks(main_task, input_analysis)
        else:
            subtasks = self._generate_generic_subtasks(main_task, input_analysis)
        
        # Ensure minimum subtask count
        if len(subtasks) < 2:
            subtasks.extend(self._generate_additional_subtasks(main_task, 2 - len(subtasks)))
        
        return subtasks
    
    def _generate_planning_subtasks(self, main_task: GeneratedTask, input_analysis: InputAnalysisResult) -> List[GeneratedTask]:
        """Generate subtasks for planning tasks"""
        subtasks = [
            self._create_subtask(
                main_task.task_id,
                "Requirements Gathering and Analysis",
                "Gather comprehensive requirements and analyze project scope",
                ["Requirements Document", "Scope Analysis", "Stakeholder Input"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Technical Feasibility Assessment",
                "Assess technical feasibility and identify potential challenges",
                ["Feasibility Report", "Risk Assessment", "Technical Constraints"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Resource Planning and Timeline Creation",
                "Plan required resources and create detailed project timeline",
                ["Resource Plan", "Project Timeline", "Milestone Definition"],
                main_task.priority
            )
        ]
        
        # Add complexity-based subtasks
        if input_analysis.complexity_score > 0.5:
            subtasks.append(self._create_subtask(
                main_task.task_id,
                "Risk Analysis and Mitigation Planning",
                "Identify potential risks and create mitigation strategies",
                ["Risk Register", "Mitigation Strategies", "Contingency Plans"],
                main_task.priority
            ))
        
        return subtasks
    
    def _generate_implementation_subtasks(self, main_task: GeneratedTask, input_analysis: InputAnalysisResult) -> List[GeneratedTask]:
        """Generate subtasks for implementation tasks"""
        subtasks = [
            self._create_subtask(
                main_task.task_id,
                "Development Environment Setup",
                "Set up development environment and initialize project structure",
                ["Development Environment", "Project Structure", "Configuration Files"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Core Functionality Implementation",
                "Implement core functionality according to specifications",
                ["Core Implementation", "Functional Code", "Basic Features"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Testing and Quality Assurance",
                "Implement comprehensive testing and quality assurance procedures",
                ["Test Suite", "Quality Validation", "Bug Fixes"],
                main_task.priority
            )
        ]
        
        # Add technology-specific subtasks
        if any(tech in input_analysis.key_concepts for tech in ['api', 'database', 'frontend']):
            if 'api' in input_analysis.key_concepts:
                subtasks.append(self._create_subtask(
                    main_task.task_id,
                    "API Development and Integration",
                    "Develop and integrate API endpoints and services",
                    ["API Implementation", "Endpoint Documentation", "Integration Tests"],
                    main_task.priority
                ))
            
            if 'database' in input_analysis.key_concepts:
                subtasks.append(self._create_subtask(
                    main_task.task_id,
                    "Database Design and Implementation",
                    "Design and implement database schema and data access layer",
                    ["Database Schema", "Data Access Layer", "Database Tests"],
                    main_task.priority
                ))
        
        return subtasks
    
    def _generate_analysis_subtasks(self, main_task: GeneratedTask, input_analysis: InputAnalysisResult) -> List[GeneratedTask]:
        """Generate subtasks for analysis tasks"""
        return [
            self._create_subtask(
                main_task.task_id,
                "Data Collection and Preparation",
                "Collect and prepare data for comprehensive analysis",
                ["Data Collection", "Data Cleaning", "Data Validation"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Analysis Execution and Processing",
                "Execute analysis procedures and process results",
                ["Analysis Results", "Data Processing", "Statistical Analysis"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Findings Documentation and Recommendations",
                "Document findings and provide actionable recommendations",
                ["Analysis Report", "Key Findings", "Recommendations"],
                main_task.priority
            )
        ]
    
    def _generate_documentation_subtasks(self, main_task: GeneratedTask, input_analysis: InputAnalysisResult) -> List[GeneratedTask]:
        """Generate subtasks for documentation tasks"""
        return [
            self._create_subtask(
                main_task.task_id,
                "Content Planning and Structure Design",
                "Plan documentation content and design information structure",
                ["Content Plan", "Documentation Structure", "Information Architecture"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Content Creation and Writing",
                "Create comprehensive documentation content",
                ["Written Content", "Technical Documentation", "User Guides"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Review, Editing, and Finalization",
                "Review, edit, and finalize all documentation",
                ["Final Documentation", "Quality Review", "Publication Ready Content"],
                main_task.priority
            )
        ]
    
    def _generate_architecture_subtasks(self, main_task: GeneratedTask, input_analysis: InputAnalysisResult) -> List[GeneratedTask]:
        """Generate subtasks for architecture and design tasks"""
        return [
            self._create_subtask(
                main_task.task_id,
                "System Architecture Design",
                "Design overall system architecture and component relationships",
                ["Architecture Diagram", "System Design", "Component Specifications"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Technical Specification Creation",
                "Create detailed technical specifications for implementation",
                ["Technical Specifications", "API Design", "Data Models"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Architecture Validation and Review",
                "Validate architecture design and conduct technical review",
                ["Architecture Validation", "Technical Review", "Design Approval"],
                main_task.priority
            )
        ]
    
    def _generate_generic_subtasks(self, main_task: GeneratedTask, input_analysis: InputAnalysisResult) -> List[GeneratedTask]:
        """Generate generic subtasks for any task type"""
        subtask_count = max(3, min(7, int(input_analysis.complexity_score * 6) + 2))
        
        subtasks = [
            self._create_subtask(
                main_task.task_id,
                "Task Planning and Preparation",
                f"Plan and prepare for execution of: {main_task.name}",
                ["Task Plan", "Resource Preparation", "Execution Strategy"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Core Task Execution",
                f"Execute core activities for: {main_task.name}",
                ["Core Deliverables", "Primary Outputs", "Task Results"],
                main_task.priority
            ),
            self._create_subtask(
                main_task.task_id,
                "Quality Validation and Completion",
                f"Validate quality and complete: {main_task.name}",
                ["Quality Validation", "Completion Verification", "Final Deliverables"],
                main_task.priority
            )
        ]
        
        # Add additional subtasks based on complexity
        for i in range(len(subtasks), subtask_count):
            subtasks.append(self._create_subtask(
                main_task.task_id,
                f"Additional Task Component {i-2}",
                f"Additional component for comprehensive completion of: {main_task.name}",
                [f"Component {i-2} Deliverables", f"Additional Outputs {i-2}"],
                main_task.priority
            ))
        
        return subtasks
    
    def _generate_additional_subtasks(self, main_task: GeneratedTask, count: int) -> List[GeneratedTask]:
        """Generate additional subtasks to meet minimum requirements"""
        additional_subtasks = []
        
        for i in range(count):
            additional_subtasks.append(self._create_subtask(
                main_task.task_id,
                f"Additional Task Requirement {i+1}",
                f"Additional requirement for comprehensive completion of: {main_task.name}",
                [f"Additional Deliverable {i+1}", f"Supplementary Output {i+1}"],
                main_task.priority
            ))
        
        return additional_subtasks
    
    def _create_subtask(self, parent_task_id: str, name: str, description: str, 
                       deliverables: List[str], priority: PriorityLevel) -> GeneratedTask:
        """Create a subtask with standard structure"""
        return GeneratedTask(
            task_id=self._generate_task_id(),
            name=name,
            description=description,
            state=TaskState.NOT_STARTED,
            priority=priority,
            parent_task_id=parent_task_id,
            subtasks=[],  # Subtasks don't have sub-subtasks in this implementation
            deliverables=deliverables,
            success_criteria=[f"{name} completed successfully", "All deliverables provided", "Quality standards met"],
            dependencies=[],
            estimated_duration=self._estimate_subtask_duration(name),
            created_timestamp=datetime.now().isoformat(),
            automation_level="SEMI_AUTOMATED"
        )
    
    def _create_default_task(self, user_input: str, input_analysis: InputAnalysisResult) -> GeneratedTask:
        """Create a default task when no specific tasks are identified"""
        return GeneratedTask(
            task_id=self._generate_task_id(),
            name=f"Process User Request: {input_analysis.input_type.value.replace('_', ' ').title()}",
            description=f"Process and respond to user request: {user_input[:100]}...",
            state=TaskState.NOT_STARTED,
            priority=input_analysis.priority_level,
            parent_task_id=None,
            subtasks=[],
            deliverables=input_analysis.deliverable_requirements or ["Response", "Solution"],
            success_criteria=["User request fully addressed", "All deliverables provided", "User satisfaction achieved"],
            dependencies=[],
            estimated_duration=self._estimate_duration_from_complexity(input_analysis.complexity_score),
            created_timestamp=datetime.now().isoformat(),
            automation_level=input_analysis.automation_level
        )
    
    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        return str(uuid.uuid4())[:22]  # Shortened UUID for readability
    
    def _estimate_duration(self, task_req: TaskRequirement, complexity_score: float) -> str:
        """Estimate task duration based on requirements and complexity"""
        base_hours = task_req.estimated_subtasks * 2  # 2 hours per subtask
        complexity_multiplier = 1 + complexity_score
        total_hours = int(base_hours * complexity_multiplier)
        
        if total_hours <= 4:
            return "2-4 hours"
        elif total_hours <= 8:
            return "4-8 hours"
        elif total_hours <= 16:
            return "1-2 days"
        elif total_hours <= 40:
            return "3-5 days"
        else:
            return "1-2 weeks"
    
    def _estimate_subtask_duration(self, subtask_name: str) -> str:
        """Estimate subtask duration based on name and type"""
        if any(keyword in subtask_name.lower() for keyword in ['planning', 'analysis', 'design']):
            return "2-4 hours"
        elif any(keyword in subtask_name.lower() for keyword in ['implementation', 'development', 'creation']):
            return "4-8 hours"
        elif any(keyword in subtask_name.lower() for keyword in ['testing', 'validation', 'review']):
            return "1-3 hours"
        else:
            return "2-4 hours"
    
    def _estimate_duration_from_complexity(self, complexity_score: float) -> str:
        """Estimate duration based on complexity score"""
        if complexity_score <= 0.3:
            return "1-2 hours"
        elif complexity_score <= 0.5:
            return "2-4 hours"
        elif complexity_score <= 0.7:
            return "4-8 hours"
        else:
            return "1-2 days"
    
    def _determine_enforcement_level(self, input_analysis: InputAnalysisResult) -> str:
        """Determine enforcement level for generated tasks"""
        if input_analysis.priority_level == PriorityLevel.CRITICAL:
            return "MAXIMUM_ENFORCEMENT"
        elif input_analysis.complexity_score > 0.6:
            return "HIGH_ENFORCEMENT"
        elif input_analysis.input_type in [InputType.PROJECT_REQUEST, InputType.IMPLEMENTATION_REQUEST]:
            return "STANDARD_ENFORCEMENT"
        else:
            return "BASIC_ENFORCEMENT"
    
    def _initialize_task_templates(self) -> Dict:
        """Initialize task generation templates"""
        return {
            'minimum_subtasks': 2,
            'maximum_subtasks': 7,
            'default_subtasks': 3,
            'complexity_multiplier': 2
        }
    
    def _initialize_subtask_generators(self) -> Dict:
        """Initialize subtask generation strategies"""
        return {
            'planning': self._generate_planning_subtasks,
            'implementation': self._generate_implementation_subtasks,
            'analysis': self._generate_analysis_subtasks,
            'documentation': self._generate_documentation_subtasks,
            'architecture': self._generate_architecture_subtasks
        }

    def convert_to_task_management_format(self, generation_result: TaskGenerationResult) -> List[Dict]:
        """Convert generated tasks to task management tool format"""
        task_management_format = []

        for main_task in generation_result.main_tasks:
            # Add main task
            main_task_dict = {
                "name": main_task.name,
                "description": main_task.description,
                "state": main_task.state.value
            }
            task_management_format.append(main_task_dict)

            # Add subtasks
            for subtask in main_task.subtasks:
                subtask_dict = {
                    "name": subtask.name,
                    "description": subtask.description,
                    "parent_task_id": "PLACEHOLDER_FOR_MAIN_TASK_ID",  # Will be replaced with actual ID
                    "state": subtask.state.value
                }
                task_management_format.append(subtask_dict)

        return task_management_format

# Example usage and testing
if __name__ == "__main__":
    generator = UTMESTaskGenerator()

    # Test with sample input
    test_input = "Create a comprehensive project management system with user authentication, task tracking, and real-time collaboration features"
    result = generator.generate_tasks_from_input(test_input)

    print(f"Generated {result.total_task_count} main tasks with {result.total_subtask_count} subtasks")
    print(f"Enforcement Level: {result.enforcement_level}")

    for main_task in result.main_tasks:
        print(f"\nMain Task: {main_task.name}")
        print(f"  Priority: {main_task.priority.value}")
        print(f"  Subtasks ({len(main_task.subtasks)}):")
        for subtask in main_task.subtasks:
            print(f"    - {subtask.name}")
            print(f"      Deliverables: {', '.join(subtask.deliverables)}")
