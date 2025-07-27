#!/usr/bin/env python3
"""
UTMES Input Analysis Algorithm
Automatically analyzes ALL user input to identify task requirements and deliverables
Part of the Unbreakable Task Management Enforcement System (UTMES)

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Core enforcement mechanism
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class InputType(Enum):
    """Classification of user input types"""
    PROJECT_REQUEST = "project_request"
    FEATURE_REQUEST = "feature_request"
    PROBLEM_SOLVING = "problem_solving"
    ANALYSIS_REQUEST = "analysis_request"
    IMPLEMENTATION_REQUEST = "implementation_request"
    DOCUMENTATION_REQUEST = "documentation_request"
    SYSTEM_MODIFICATION = "system_modification"
    QUESTION_INQUIRY = "question_inquiry"
    WORKFLOW_REQUEST = "workflow_request"
    MAINTENANCE_REQUEST = "maintenance_request"

class WorkflowType(Enum):
    """Types of workflows that can be triggered"""
    DOCUMENTATION_MODE = "documentation_mode"
    FULL_DEVELOPMENT_MODE = "full_development_mode"
    ANALYSIS_WORKFLOW = "analysis_workflow"
    IMPLEMENTATION_WORKFLOW = "implementation_workflow"
    MAINTENANCE_WORKFLOW = "maintenance_workflow"
    RESEARCH_WORKFLOW = "research_workflow"

class PriorityLevel(Enum):
    """Priority levels for task generation"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class TaskRequirement:
    """Represents a required task identified from user input"""
    name: str
    description: str
    deliverables: List[str]
    priority: PriorityLevel
    estimated_subtasks: int
    dependencies: List[str]
    success_criteria: List[str]

@dataclass
class InputAnalysisResult:
    """Result of analyzing user input"""
    input_type: InputType
    workflow_type: Optional[WorkflowType]
    priority_level: PriorityLevel
    required_tasks: List[TaskRequirement]
    key_concepts: List[str]
    deliverable_requirements: List[str]
    complexity_score: float
    automation_level: str

class UTMESInputAnalyzer:
    """
    UTMES Input Analysis Algorithm
    Automatically analyzes ALL user input to identify task requirements
    """
    
    def __init__(self):
        self.analysis_patterns = self._initialize_analysis_patterns()
        self.task_templates = self._initialize_task_templates()
        self.workflow_triggers = self._initialize_workflow_triggers()
        
    def analyze_user_input(self, user_input: str) -> InputAnalysisResult:
        """
        MAIN ANALYSIS FUNCTION
        Analyzes user input and returns comprehensive task requirements
        
        Args:
            user_input: Raw user input string
            
        Returns:
            InputAnalysisResult with complete analysis and task requirements
        """
        # Step 1: Classify input type
        input_type = self._classify_input_type(user_input)
        
        # Step 2: Determine workflow type
        workflow_type = self._determine_workflow_type(user_input, input_type)
        
        # Step 3: Assess priority level
        priority_level = self._assess_priority_level(user_input, input_type)
        
        # Step 4: Extract key concepts
        key_concepts = self._extract_key_concepts(user_input)
        
        # Step 5: Identify deliverable requirements
        deliverable_requirements = self._identify_deliverable_requirements(user_input, input_type)
        
        # Step 6: Calculate complexity score
        complexity_score = self._calculate_complexity_score(user_input, key_concepts)
        
        # Step 7: Generate required tasks
        required_tasks = self._generate_required_tasks(
            user_input, input_type, workflow_type, priority_level, 
            key_concepts, deliverable_requirements, complexity_score
        )
        
        # Step 8: Determine automation level
        automation_level = self._determine_automation_level(input_type, complexity_score)
        
        return InputAnalysisResult(
            input_type=input_type,
            workflow_type=workflow_type,
            priority_level=priority_level,
            required_tasks=required_tasks,
            key_concepts=key_concepts,
            deliverable_requirements=deliverable_requirements,
            complexity_score=complexity_score,
            automation_level=automation_level
        )
    
    def _classify_input_type(self, user_input: str) -> InputType:
        """Classify the type of user input"""
        input_lower = user_input.lower()
        
        # Project request patterns
        if any(pattern in input_lower for pattern in [
            'create', 'build', 'develop', 'make', 'design', 'implement'
        ]):
            if any(pattern in input_lower for pattern in [
                'project', 'application', 'system', 'platform', 'solution'
            ]):
                return InputType.PROJECT_REQUEST
            else:
                return InputType.IMPLEMENTATION_REQUEST
        
        # Analysis request patterns
        if any(pattern in input_lower for pattern in [
            'analyze', 'review', 'assess', 'evaluate', 'examine', 'investigate'
        ]):
            return InputType.ANALYSIS_REQUEST
        
        # Problem solving patterns
        if any(pattern in input_lower for pattern in [
            'fix', 'solve', 'resolve', 'debug', 'troubleshoot', 'repair'
        ]):
            return InputType.PROBLEM_SOLVING
        
        # Documentation patterns
        if any(pattern in input_lower for pattern in [
            'document', 'write', 'explain', 'describe', 'guide', 'manual'
        ]):
            return InputType.DOCUMENTATION_REQUEST
        
        # System modification patterns
        if any(pattern in input_lower for pattern in [
            'modify', 'update', 'enhance', 'improve', 'optimize', 'upgrade'
        ]):
            return InputType.SYSTEM_MODIFICATION
        
        # Maintenance patterns
        if any(pattern in input_lower for pattern in [
            'maintain', 'monitor', 'validate', 'test', 'verify'
        ]):
            return InputType.MAINTENANCE_REQUEST
        
        # Default to question inquiry
        return InputType.QUESTION_INQUIRY
    
    def _determine_workflow_type(self, user_input: str, input_type: InputType) -> Optional[WorkflowType]:
        """Determine the appropriate workflow type"""
        input_lower = user_input.lower()
        
        # Documentation mode triggers
        if any(pattern in input_lower for pattern in [
            'prd', 'requirements', 'specification', 'architecture', 'checklist'
        ]) or input_type == InputType.DOCUMENTATION_REQUEST:
            return WorkflowType.DOCUMENTATION_MODE
        
        # Full development mode triggers
        if any(pattern in input_lower for pattern in [
            'build', 'implement', 'develop', 'create application', 'full project'
        ]) and input_type == InputType.PROJECT_REQUEST:
            return WorkflowType.FULL_DEVELOPMENT_MODE
        
        # Analysis workflow triggers
        if input_type == InputType.ANALYSIS_REQUEST:
            return WorkflowType.ANALYSIS_WORKFLOW
        
        # Implementation workflow triggers
        if input_type == InputType.IMPLEMENTATION_REQUEST:
            return WorkflowType.IMPLEMENTATION_WORKFLOW
        
        # Maintenance workflow triggers
        if input_type == InputType.MAINTENANCE_REQUEST:
            return WorkflowType.MAINTENANCE_WORKFLOW
        
        # Research workflow triggers
        if any(pattern in input_lower for pattern in [
            'research', 'investigate', 'study', 'explore'
        ]):
            return WorkflowType.RESEARCH_WORKFLOW
        
        return None
    
    def _assess_priority_level(self, user_input: str, input_type: InputType) -> PriorityLevel:
        """Assess the priority level of the request"""
        input_lower = user_input.lower()
        
        # Critical priority indicators
        if any(pattern in input_lower for pattern in [
            'critical', 'urgent', 'emergency', 'immediate', 'asap', 'broken', 'failing'
        ]):
            return PriorityLevel.CRITICAL
        
        # High priority indicators
        if any(pattern in input_lower for pattern in [
            'important', 'high priority', 'soon', 'quickly', 'fast'
        ]) or input_type in [InputType.PROBLEM_SOLVING, InputType.SYSTEM_MODIFICATION]:
            return PriorityLevel.HIGH
        
        # Medium priority for most requests
        if input_type in [
            InputType.PROJECT_REQUEST, InputType.IMPLEMENTATION_REQUEST, 
            InputType.ANALYSIS_REQUEST, InputType.FEATURE_REQUEST
        ]:
            return PriorityLevel.MEDIUM
        
        # Low priority for documentation and questions
        return PriorityLevel.LOW
    
    def _extract_key_concepts(self, user_input: str) -> List[str]:
        """Extract key concepts and technologies from user input"""
        # Technology patterns
        tech_patterns = [
            r'\b(python|javascript|typescript|react|node|django|flask)\b',
            r'\b(database|sql|mongodb|postgresql|mysql)\b',
            r'\b(api|rest|graphql|microservices)\b',
            r'\b(docker|kubernetes|aws|azure|gcp)\b',
            r'\b(ai|machine learning|ml|neural network)\b',
            r'\b(frontend|backend|fullstack|web)\b'
        ]
        
        concepts = []
        input_lower = user_input.lower()
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, input_lower)
            concepts.extend(matches)
        
        # Extract capitalized words (likely proper nouns/technologies)
        capitalized_words = re.findall(r'\b[A-Z][a-zA-Z]+\b', user_input)
        concepts.extend([word.lower() for word in capitalized_words])
        
        return list(set(concepts))  # Remove duplicates
    
    def _identify_deliverable_requirements(self, user_input: str, input_type: InputType) -> List[str]:
        """Identify specific deliverable requirements"""
        deliverables = []
        input_lower = user_input.lower()
        
        # Common deliverable patterns
        if 'document' in input_lower or input_type == InputType.DOCUMENTATION_REQUEST:
            deliverables.extend(['documentation', 'user guide', 'technical specifications'])
        
        if 'code' in input_lower or input_type == InputType.IMPLEMENTATION_REQUEST:
            deliverables.extend(['source code', 'implementation', 'working application'])
        
        if 'test' in input_lower:
            deliverables.extend(['test suite', 'test cases', 'validation procedures'])
        
        if 'deploy' in input_lower:
            deliverables.extend(['deployment scripts', 'deployment guide'])
        
        if input_type == InputType.PROJECT_REQUEST:
            deliverables.extend(['project plan', 'architecture design', 'implementation'])
        
        if input_type == InputType.ANALYSIS_REQUEST:
            deliverables.extend(['analysis report', 'findings summary', 'recommendations'])
        
        return list(set(deliverables))  # Remove duplicates
    
    def _calculate_complexity_score(self, user_input: str, key_concepts: List[str]) -> float:
        """Calculate complexity score (0.0 to 1.0)"""
        complexity_factors = {
            'length': min(len(user_input) / 1000, 0.3),  # Max 0.3 for length
            'concepts': min(len(key_concepts) / 10, 0.3),  # Max 0.3 for concepts
            'technical_terms': 0.0,
            'complexity_indicators': 0.0
        }
        
        # Technical complexity indicators
        technical_terms = ['integration', 'architecture', 'scalability', 'performance', 'security']
        complexity_factors['technical_terms'] = min(
            sum(1 for term in technical_terms if term in user_input.lower()) / len(technical_terms),
            0.2
        )
        
        # Complexity indicators
        complexity_indicators = ['complex', 'advanced', 'sophisticated', 'enterprise', 'distributed']
        complexity_factors['complexity_indicators'] = min(
            sum(1 for indicator in complexity_indicators if indicator in user_input.lower()) / len(complexity_indicators),
            0.2
        )
        
        return sum(complexity_factors.values())
    
    def _generate_required_tasks(self, user_input: str, input_type: InputType, 
                               workflow_type: Optional[WorkflowType], priority_level: PriorityLevel,
                               key_concepts: List[str], deliverable_requirements: List[str],
                               complexity_score: float) -> List[TaskRequirement]:
        """Generate required tasks based on analysis"""
        tasks = []
        
        # Base task generation based on input type
        if input_type == InputType.PROJECT_REQUEST:
            tasks.extend(self._generate_project_tasks(user_input, complexity_score, deliverable_requirements))
        elif input_type == InputType.IMPLEMENTATION_REQUEST:
            tasks.extend(self._generate_implementation_tasks(user_input, key_concepts, deliverable_requirements))
        elif input_type == InputType.ANALYSIS_REQUEST:
            tasks.extend(self._generate_analysis_tasks(user_input, complexity_score))
        elif input_type == InputType.PROBLEM_SOLVING:
            tasks.extend(self._generate_problem_solving_tasks(user_input, priority_level))
        elif input_type == InputType.DOCUMENTATION_REQUEST:
            tasks.extend(self._generate_documentation_tasks(user_input, deliverable_requirements))
        elif input_type == InputType.SYSTEM_MODIFICATION:
            tasks.extend(self._generate_modification_tasks(user_input, complexity_score))
        else:
            # Default task for any input
            tasks.append(TaskRequirement(
                name=f"Address User Request: {input_type.value.replace('_', ' ').title()}",
                description=f"Process and respond to user request: {user_input[:100]}...",
                deliverables=deliverable_requirements or ["Response", "Solution"],
                priority=priority_level,
                estimated_subtasks=max(2, int(complexity_score * 5)),
                dependencies=[],
                success_criteria=["User request fully addressed", "All deliverables provided"]
            ))
        
        return tasks
    
    def _generate_project_tasks(self, user_input: str, complexity_score: float, 
                              deliverable_requirements: List[str]) -> List[TaskRequirement]:
        """Generate tasks for project requests"""
        return [
            TaskRequirement(
                name="Project Planning and Requirements Analysis",
                description=f"Analyze project requirements and create comprehensive plan for: {user_input[:100]}...",
                deliverables=["Project Requirements Document", "Technical Specifications", "Implementation Plan"],
                priority=PriorityLevel.HIGH,
                estimated_subtasks=max(3, int(complexity_score * 6)),
                dependencies=[],
                success_criteria=["Complete requirements analysis", "Clear project scope defined", "Implementation plan created"]
            ),
            TaskRequirement(
                name="System Architecture and Design",
                description="Design system architecture and technical implementation approach",
                deliverables=["Architecture Diagram", "Technical Design Document", "Component Specifications"],
                priority=PriorityLevel.HIGH,
                estimated_subtasks=max(4, int(complexity_score * 7)),
                dependencies=["Project Planning and Requirements Analysis"],
                success_criteria=["Architecture design complete", "Technical approach validated", "Component design finalized"]
            ),
            TaskRequirement(
                name="Implementation and Development",
                description="Implement the designed system according to specifications",
                deliverables=deliverable_requirements or ["Working Implementation", "Source Code", "Documentation"],
                priority=PriorityLevel.MEDIUM,
                estimated_subtasks=max(5, int(complexity_score * 10)),
                dependencies=["System Architecture and Design"],
                success_criteria=["Implementation complete", "All features functional", "Quality standards met"]
            )
        ]
    
    def _generate_implementation_tasks(self, user_input: str, key_concepts: List[str],
                                     deliverable_requirements: List[str]) -> List[TaskRequirement]:
        """Generate tasks for implementation requests"""
        return [
            TaskRequirement(
                name="Implementation Planning and Setup",
                description=f"Plan implementation approach for: {user_input[:100]}...",
                deliverables=["Implementation Plan", "Development Environment Setup", "Technical Approach"],
                priority=PriorityLevel.HIGH,
                estimated_subtasks=3,
                dependencies=[],
                success_criteria=["Implementation plan complete", "Environment ready", "Approach validated"]
            ),
            TaskRequirement(
                name="Core Implementation",
                description="Implement core functionality according to requirements",
                deliverables=deliverable_requirements or ["Working Implementation", "Source Code"],
                priority=PriorityLevel.HIGH,
                estimated_subtasks=max(4, len(key_concepts) + 2),
                dependencies=["Implementation Planning and Setup"],
                success_criteria=["Core functionality implemented", "Requirements met", "Code quality validated"]
            )
        ]
    
    def _generate_analysis_tasks(self, user_input: str, complexity_score: float) -> List[TaskRequirement]:
        """Generate tasks for analysis requests"""
        return [
            TaskRequirement(
                name="Comprehensive Analysis",
                description=f"Conduct comprehensive analysis of: {user_input[:100]}...",
                deliverables=["Analysis Report", "Findings Summary", "Recommendations"],
                priority=PriorityLevel.MEDIUM,
                estimated_subtasks=max(3, int(complexity_score * 5)),
                dependencies=[],
                success_criteria=["Analysis complete", "Findings documented", "Recommendations provided"]
            )
        ]
    
    def _generate_problem_solving_tasks(self, user_input: str, priority_level: PriorityLevel) -> List[TaskRequirement]:
        """Generate tasks for problem solving requests"""
        return [
            TaskRequirement(
                name="Problem Diagnosis and Resolution",
                description=f"Diagnose and resolve problem: {user_input[:100]}...",
                deliverables=["Problem Analysis", "Solution Implementation", "Validation Results"],
                priority=priority_level,
                estimated_subtasks=4,
                dependencies=[],
                success_criteria=["Problem identified", "Solution implemented", "Resolution validated"]
            )
        ]
    
    def _generate_documentation_tasks(self, user_input: str, deliverable_requirements: List[str]) -> List[TaskRequirement]:
        """Generate tasks for documentation requests"""
        return [
            TaskRequirement(
                name="Documentation Creation",
                description=f"Create comprehensive documentation for: {user_input[:100]}...",
                deliverables=deliverable_requirements or ["Documentation", "User Guide", "Technical Reference"],
                priority=PriorityLevel.MEDIUM,
                estimated_subtasks=3,
                dependencies=[],
                success_criteria=["Documentation complete", "Content accurate", "User-friendly format"]
            )
        ]
    
    def _generate_modification_tasks(self, user_input: str, complexity_score: float) -> List[TaskRequirement]:
        """Generate tasks for system modification requests"""
        return [
            TaskRequirement(
                name="System Modification and Enhancement",
                description=f"Modify and enhance system: {user_input[:100]}...",
                deliverables=["Modified System", "Enhancement Documentation", "Validation Results"],
                priority=PriorityLevel.HIGH,
                estimated_subtasks=max(3, int(complexity_score * 6)),
                dependencies=[],
                success_criteria=["Modifications implemented", "Enhancements validated", "System functional"]
            )
        ]
    
    def _determine_automation_level(self, input_type: InputType, complexity_score: float) -> str:
        """Determine the level of automation for task execution"""
        if complexity_score > 0.7:
            return "MANUAL_OVERSIGHT_REQUIRED"
        elif complexity_score > 0.4:
            return "SEMI_AUTOMATED"
        else:
            return "FULLY_AUTOMATED"
    
    def _initialize_analysis_patterns(self) -> Dict:
        """Initialize analysis patterns for input classification"""
        return {
            'project_indicators': ['create', 'build', 'develop', 'make', 'design'],
            'analysis_indicators': ['analyze', 'review', 'assess', 'evaluate'],
            'problem_indicators': ['fix', 'solve', 'resolve', 'debug', 'troubleshoot'],
            'documentation_indicators': ['document', 'write', 'explain', 'describe']
        }
    
    def _initialize_task_templates(self) -> Dict:
        """Initialize task templates for different input types"""
        return {
            'default_subtask_count': 3,
            'complex_subtask_multiplier': 2,
            'minimum_subtasks': 2,
            'maximum_subtasks': 10
        }
    
    def _initialize_workflow_triggers(self) -> Dict:
        """Initialize workflow trigger patterns"""
        return {
            'documentation_triggers': ['prd', 'requirements', 'specification'],
            'development_triggers': ['build', 'implement', 'develop'],
            'analysis_triggers': ['analyze', 'review', 'assess']
        }

# Example usage and testing
if __name__ == "__main__":
    analyzer = UTMESInputAnalyzer()
    
    # Test with sample input
    test_input = "Create a web application for task management with user authentication and real-time updates"
    result = analyzer.analyze_user_input(test_input)
    
    print(f"Input Type: {result.input_type}")
    print(f"Workflow Type: {result.workflow_type}")
    print(f"Priority: {result.priority_level}")
    print(f"Complexity Score: {result.complexity_score}")
    print(f"Required Tasks: {len(result.required_tasks)}")
    for task in result.required_tasks:
        print(f"  - {task.name} ({task.estimated_subtasks} subtasks)")
