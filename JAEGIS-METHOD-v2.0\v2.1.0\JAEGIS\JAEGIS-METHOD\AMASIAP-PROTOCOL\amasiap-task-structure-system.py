#!/usr/bin/env python3
"""
A.M.A.S.I.A.P. Task Structure Creation System
Implements hierarchical task structure creation with research, analysis, implementation, validation, and documentation categories
Part of the #1 System-Wide Protocol

Date: 24 July 2025 (Auto-updating daily)
Priority: #1 SYSTEM-WIDE PROTOCOL COMPONENT
Status: ACTIVE AND OPERATIONAL
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Import task management capabilities
from add_tasks import add_tasks
from update_tasks import update_tasks

class TaskComplexity(Enum):
    """Task complexity levels"""
    SIMPLE = "SIMPLE"
    MODERATE = "MODERATE"
    COMPLEX = "COMPLEX"
    ADVANCED = "ADVANCED"

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class TaskTemplate:
    """Template for creating structured tasks"""
    category: str
    name_pattern: str
    description_pattern: str
    min_tasks: int
    max_tasks: int
    complexity_factors: List[str]
    success_criteria_template: List[str]
    dependencies_template: List[str]

@dataclass
class TaskStructureAnalysis:
    """Analysis of user input for task structure creation"""
    input_complexity: TaskComplexity
    domain_keywords: List[str]
    action_keywords: List[str]
    scope_indicators: List[str]
    estimated_effort: str
    recommended_task_distribution: Dict[str, int]

@dataclass
class StructuredTask:
    """Represents a structured task in the A.M.A.S.I.A.P. system"""
    task_id: str
    name: str
    description: str
    category: str
    priority: TaskPriority
    complexity: TaskComplexity
    estimated_duration: str
    dependencies: List[str]
    success_criteria: List[str]
    deliverables: List[str]
    resources_required: List[str]
    validation_methods: List[str]

class AMASIAPTaskStructureSystem:
    """
    A.M.A.S.I.A.P. Task Structure Creation System
    Creates hierarchical task structures with comprehensive categorization
    """
    
    def __init__(self):
        # Task templates for each category
        self.task_templates = self._initialize_task_templates()
        
        # Analysis configuration
        self.complexity_keywords = {
            TaskComplexity.SIMPLE: ['basic', 'simple', 'quick', 'easy', 'straightforward'],
            TaskComplexity.MODERATE: ['moderate', 'standard', 'typical', 'regular'],
            TaskComplexity.COMPLEX: ['complex', 'advanced', 'comprehensive', 'detailed', 'thorough'],
            TaskComplexity.ADVANCED: ['enterprise', 'system-wide', 'complete', 'full-scale', 'entire']
        }
        
        # Domain-specific task adjustments
        self.domain_adjustments = {
            'system': {'implementation': +3, 'validation': +1},
            'protocol': {'research': +2, 'documentation': +1},
            'automation': {'implementation': +2, 'validation': +2},
            'integration': {'analysis': +1, 'implementation': +2},
            'enhancement': {'research': +1, 'implementation': +1}
        }
        
        # Initialize system
        self._initialize_system()
    
    def create_hierarchical_task_structure(self, user_input: str) -> Dict[str, Any]:
        """
        MAIN TASK STRUCTURE CREATION FUNCTION
        Creates comprehensive hierarchical task structure based on user input
        
        Args:
            user_input: Original user input to analyze and create tasks for
            
        Returns:
            Complete task structure with all categories and tasks
        """
        print(f"🏗️ Creating hierarchical task structure for: {user_input}")
        
        # Step 1: Analyze user input
        analysis = self._analyze_user_input(user_input)
        print(f"📊 Input Analysis: {analysis.input_complexity.value} complexity")
        
        # Step 2: Create task structure for each category
        task_structure = {}
        total_tasks_created = 0
        
        for category, template in self.task_templates.items():
            print(f"📋 Creating {category} tasks...")
            
            # Determine number of tasks for this category
            task_count = self._calculate_task_count(category, analysis)
            
            # Create tasks for this category
            category_tasks = self._create_category_tasks(
                category, template, task_count, user_input, analysis
            )
            
            task_structure[category] = {
                'tasks': category_tasks,
                'count': len(category_tasks),
                'estimated_duration': self._calculate_category_duration(category_tasks)
            }
            
            total_tasks_created += len(category_tasks)
            print(f"✅ Created {len(category_tasks)} {category} tasks")
        
        # Step 3: Establish task dependencies
        task_structure = self._establish_task_dependencies(task_structure)
        
        # Step 4: Create execution order
        execution_order = self._create_execution_order(task_structure)
        
        # Step 5: Generate comprehensive structure
        comprehensive_structure = {
            'user_input': user_input,
            'analysis': asdict(analysis),
            'task_structure': task_structure,
            'execution_order': execution_order,
            'total_tasks': total_tasks_created,
            'estimated_total_duration': self._calculate_total_duration(task_structure),
            'creation_timestamp': datetime.now().isoformat(),
            'structure_id': self._generate_structure_id()
        }
        
        print(f"🎯 Task Structure Created: {total_tasks_created} total tasks across {len(self.task_templates)} categories")
        
        return comprehensive_structure
    
    def _analyze_user_input(self, user_input: str) -> TaskStructureAnalysis:
        """Analyze user input to determine task structure requirements"""
        input_lower = user_input.lower()
        
        # Determine complexity
        complexity = self._determine_complexity(input_lower)
        
        # Extract domain keywords
        domain_keywords = self._extract_domain_keywords(input_lower)
        
        # Extract action keywords
        action_keywords = self._extract_action_keywords(input_lower)
        
        # Identify scope indicators
        scope_indicators = self._identify_scope_indicators(input_lower)
        
        # Estimate effort
        estimated_effort = self._estimate_effort(complexity, len(domain_keywords), len(action_keywords))
        
        # Calculate recommended task distribution
        task_distribution = self._calculate_task_distribution(
            complexity, domain_keywords, action_keywords, scope_indicators
        )
        
        return TaskStructureAnalysis(
            input_complexity=complexity,
            domain_keywords=domain_keywords,
            action_keywords=action_keywords,
            scope_indicators=scope_indicators,
            estimated_effort=estimated_effort,
            recommended_task_distribution=task_distribution
        )
    
    def _determine_complexity(self, input_lower: str) -> TaskComplexity:
        """Determine input complexity based on keywords"""
        complexity_scores = {complexity: 0 for complexity in TaskComplexity}
        
        for complexity, keywords in self.complexity_keywords.items():
            for keyword in keywords:
                if keyword in input_lower:
                    complexity_scores[complexity] += 1
        
        # Return highest scoring complexity, default to MODERATE
        max_complexity = max(complexity_scores.items(), key=lambda x: x[1])
        return max_complexity[0] if max_complexity[1] > 0 else TaskComplexity.MODERATE
    
    def _extract_domain_keywords(self, input_lower: str) -> List[str]:
        """Extract domain-specific keywords"""
        domain_keywords = [
            'system', 'protocol', 'automation', 'integration', 'enhancement',
            'framework', 'architecture', 'infrastructure', 'platform', 'service',
            'application', 'software', 'hardware', 'network', 'security',
            'database', 'api', 'interface', 'workflow', 'process'
        ]
        
        return [keyword for keyword in domain_keywords if keyword in input_lower]
    
    def _extract_action_keywords(self, input_lower: str) -> List[str]:
        """Extract action keywords"""
        action_keywords = [
            'create', 'build', 'develop', 'implement', 'design', 'enhance',
            'improve', 'optimize', 'integrate', 'automate', 'configure',
            'deploy', 'test', 'validate', 'monitor', 'maintain', 'update',
            'upgrade', 'migrate', 'analyze', 'research', 'document'
        ]
        
        return [keyword for keyword in action_keywords if keyword in input_lower]
    
    def _identify_scope_indicators(self, input_lower: str) -> List[str]:
        """Identify scope indicators"""
        scope_indicators = [
            'entire', 'complete', 'full', 'comprehensive', 'system-wide',
            'end-to-end', 'holistic', 'integrated', 'unified', 'centralized'
        ]
        
        return [indicator for indicator in scope_indicators if indicator in input_lower]
    
    def _estimate_effort(self, complexity: TaskComplexity, domain_count: int, action_count: int) -> str:
        """Estimate effort based on complexity and keyword counts"""
        base_effort = {
            TaskComplexity.SIMPLE: 1,
            TaskComplexity.MODERATE: 2,
            TaskComplexity.COMPLEX: 4,
            TaskComplexity.ADVANCED: 8
        }
        
        effort_score = base_effort[complexity] + (domain_count * 0.5) + (action_count * 0.3)
        
        if effort_score <= 2:
            return "LOW"
        elif effort_score <= 4:
            return "MEDIUM"
        elif effort_score <= 6:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    def _calculate_task_distribution(self, complexity: TaskComplexity, domain_keywords: List[str], 
                                   action_keywords: List[str], scope_indicators: List[str]) -> Dict[str, int]:
        """Calculate recommended task distribution across categories"""
        # Base distribution by complexity
        base_distribution = {
            TaskComplexity.SIMPLE: {
                'research': 3, 'analysis': 2, 'implementation': 5, 'validation': 2, 'documentation': 1
            },
            TaskComplexity.MODERATE: {
                'research': 4, 'analysis': 2, 'implementation': 6, 'validation': 2, 'documentation': 1
            },
            TaskComplexity.COMPLEX: {
                'research': 5, 'analysis': 3, 'implementation': 8, 'validation': 3, 'documentation': 2
            },
            TaskComplexity.ADVANCED: {
                'research': 5, 'analysis': 3, 'implementation': 10, 'validation': 3, 'documentation': 2
            }
        }
        
        distribution = base_distribution[complexity].copy()
        
        # Apply domain-specific adjustments
        for domain in domain_keywords:
            if domain in self.domain_adjustments:
                adjustments = self.domain_adjustments[domain]
                for category, adjustment in adjustments.items():
                    if category in distribution:
                        distribution[category] = max(1, distribution[category] + adjustment)
        
        # Apply scope adjustments
        if scope_indicators:
            scope_multiplier = min(2.0, 1.0 + (len(scope_indicators) * 0.2))
            for category in distribution:
                distribution[category] = int(distribution[category] * scope_multiplier)
        
        return distribution
    
    def _calculate_task_count(self, category: str, analysis: TaskStructureAnalysis) -> int:
        """Calculate number of tasks for a specific category"""
        recommended = analysis.recommended_task_distribution.get(category, 3)
        template = self.task_templates[category]
        
        # Ensure within template bounds
        return max(template.min_tasks, min(template.max_tasks, recommended))
    
    def _create_category_tasks(self, category: str, template: TaskTemplate, 
                             task_count: int, user_input: str, analysis: TaskStructureAnalysis) -> List[StructuredTask]:
        """Create tasks for a specific category"""
        tasks = []
        
        for i in range(task_count):
            task = self._create_single_task(category, template, i + 1, user_input, analysis)
            tasks.append(task)
        
        return tasks
    
    def _create_single_task(self, category: str, template: TaskTemplate, task_number: int, 
                          user_input: str, analysis: TaskStructureAnalysis) -> StructuredTask:
        """Create a single structured task"""
        task_id = f"{category.upper()}_{task_number:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate task name
        name = template.name_pattern.format(
            number=task_number,
            category=category.title(),
            input_summary=user_input[:50] + "..." if len(user_input) > 50 else user_input
        )
        
        # Generate task description
        description = template.description_pattern.format(
            number=task_number,
            category=category.lower(),
            user_input=user_input,
            complexity=analysis.input_complexity.value.lower(),
            domain_keywords=", ".join(analysis.domain_keywords[:3])
        )
        
        # Determine task priority
        priority = self._determine_task_priority(category, task_number, analysis)
        
        # Generate success criteria
        success_criteria = [
            criterion.format(category=category.lower(), user_input=user_input)
            for criterion in template.success_criteria_template
        ]
        
        # Generate deliverables
        deliverables = self._generate_deliverables(category, task_number, user_input)
        
        # Generate resources required
        resources_required = self._generate_resources_required(category, analysis)
        
        # Generate validation methods
        validation_methods = self._generate_validation_methods(category, task_number)
        
        return StructuredTask(
            task_id=task_id,
            name=name,
            description=description,
            category=category,
            priority=priority,
            complexity=analysis.input_complexity,
            estimated_duration=self._estimate_task_duration(category, analysis.input_complexity),
            dependencies=[],  # Will be set later
            success_criteria=success_criteria,
            deliverables=deliverables,
            resources_required=resources_required,
            validation_methods=validation_methods
        )
    
    def _determine_task_priority(self, category: str, task_number: int, analysis: TaskStructureAnalysis) -> TaskPriority:
        """Determine task priority based on category and analysis"""
        # Category-based priority
        category_priorities = {
            'research': TaskPriority.HIGH,
            'analysis': TaskPriority.HIGH,
            'implementation': TaskPriority.CRITICAL,
            'validation': TaskPriority.MEDIUM,
            'documentation': TaskPriority.LOW
        }
        
        base_priority = category_priorities.get(category, TaskPriority.MEDIUM)
        
        # Adjust for complexity
        if analysis.input_complexity == TaskComplexity.ADVANCED:
            if base_priority.value > 1:
                return TaskPriority(base_priority.value - 1)
        
        return base_priority
    
    def _estimate_task_duration(self, category: str, complexity: TaskComplexity) -> str:
        """Estimate task duration based on category and complexity"""
        base_durations = {
            'research': {'SIMPLE': '2h', 'MODERATE': '4h', 'COMPLEX': '6h', 'ADVANCED': '8h'},
            'analysis': {'SIMPLE': '1h', 'MODERATE': '2h', 'COMPLEX': '4h', 'ADVANCED': '6h'},
            'implementation': {'SIMPLE': '4h', 'MODERATE': '8h', 'COMPLEX': '16h', 'ADVANCED': '24h'},
            'validation': {'SIMPLE': '1h', 'MODERATE': '2h', 'COMPLEX': '4h', 'ADVANCED': '6h'},
            'documentation': {'SIMPLE': '1h', 'MODERATE': '2h', 'COMPLEX': '3h', 'ADVANCED': '4h'}
        }
        
        return base_durations.get(category, {}).get(complexity.value, '2h')
    
    def _generate_deliverables(self, category: str, task_number: int, user_input: str) -> List[str]:
        """Generate deliverables for a task"""
        deliverable_templates = {
            'research': [f"Research report {task_number}", f"Data analysis for {user_input[:30]}"],
            'analysis': [f"Analysis document {task_number}", f"Findings summary"],
            'implementation': [f"Implementation component {task_number}", f"Working solution"],
            'validation': [f"Validation report {task_number}", f"Test results"],
            'documentation': [f"Documentation update {task_number}", f"User guide section"]
        }
        
        return deliverable_templates.get(category, [f"{category.title()} deliverable {task_number}"])
    
    def _generate_resources_required(self, category: str, analysis: TaskStructureAnalysis) -> List[str]:
        """Generate resources required for a task"""
        base_resources = {
            'research': ['Web access', 'Research databases', 'Analysis tools'],
            'analysis': ['Data processing tools', 'Analysis frameworks', 'Visualization tools'],
            'implementation': ['Development environment', 'Programming tools', 'Testing frameworks'],
            'validation': ['Testing tools', 'Quality assurance frameworks', 'Validation criteria'],
            'documentation': ['Documentation tools', 'Writing guidelines', 'Review processes']
        }
        
        resources = base_resources.get(category, ['Standard tools'])
        
        # Add complexity-based resources
        if analysis.input_complexity in [TaskComplexity.COMPLEX, TaskComplexity.ADVANCED]:
            resources.extend(['Expert consultation', 'Advanced tools', 'Additional time'])
        
        return resources
    
    def _generate_validation_methods(self, category: str, task_number: int) -> List[str]:
        """Generate validation methods for a task"""
        validation_templates = {
            'research': ['Peer review', 'Source verification', 'Data quality check'],
            'analysis': ['Logic validation', 'Result verification', 'Cross-reference check'],
            'implementation': ['Unit testing', 'Integration testing', 'Performance testing'],
            'validation': ['Acceptance testing', 'User validation', 'Compliance check'],
            'documentation': ['Content review', 'Accuracy check', 'Completeness validation']
        }
        
        return validation_templates.get(category, ['Standard validation'])
    
    def _establish_task_dependencies(self, task_structure: Dict) -> Dict:
        """Establish dependencies between tasks"""
        # Define category dependencies
        category_dependencies = {
            'analysis': ['research'],
            'implementation': ['research', 'analysis'],
            'validation': ['implementation'],
            'documentation': ['implementation', 'validation']
        }
        
        # Apply dependencies
        for category, structure in task_structure.items():
            if category in category_dependencies:
                dependent_categories = category_dependencies[category]
                for task in structure['tasks']:
                    task.dependencies = dependent_categories
        
        return task_structure
    
    def _create_execution_order(self, task_structure: Dict) -> List[str]:
        """Create execution order for all tasks"""
        execution_order = []
        
        # Define category execution order
        category_order = ['research', 'analysis', 'implementation', 'validation', 'documentation']
        
        for category in category_order:
            if category in task_structure:
                category_tasks = task_structure[category]['tasks']
                # Sort tasks within category by priority
                sorted_tasks = sorted(category_tasks, key=lambda t: t.priority.value)
                execution_order.extend([task.task_id for task in sorted_tasks])
        
        return execution_order
    
    def _calculate_category_duration(self, tasks: List[StructuredTask]) -> str:
        """Calculate total duration for a category"""
        # Simplified duration calculation
        return f"{len(tasks) * 4}h"  # Assume 4h average per task
    
    def _calculate_total_duration(self, task_structure: Dict) -> str:
        """Calculate total duration for all tasks"""
        total_hours = 0
        
        for category, structure in task_structure.items():
            category_duration = structure['estimated_duration']
            hours = int(category_duration.replace('h', ''))
            total_hours += hours
        
        return f"{total_hours}h"
    
    def _generate_structure_id(self) -> str:
        """Generate unique structure ID"""
        return f"TASK_STRUCT_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _initialize_task_templates(self) -> Dict[str, TaskTemplate]:
        """Initialize task templates for each category"""
        return {
            'research': TaskTemplate(
                category='research',
                name_pattern="Research Task {number}: {category} Investigation",
                description_pattern="Conduct comprehensive {category} research for: {user_input}. Focus on {complexity} level analysis with emphasis on {domain_keywords}.",
                min_tasks=3,
                max_tasks=5,
                complexity_factors=['scope', 'depth', 'technical_level'],
                success_criteria_template=[
                    "Complete {category} investigation requirements",
                    "Gather comprehensive data for {user_input}",
                    "Validate research findings quality"
                ],
                dependencies_template=[]
            ),
            'analysis': TaskTemplate(
                category='analysis',
                name_pattern="Analysis Task {number}: Data Processing",
                description_pattern="Analyze research findings and process data for: {user_input}. Perform {complexity} level analysis focusing on {domain_keywords}.",
                min_tasks=2,
                max_tasks=3,
                complexity_factors=['data_volume', 'analysis_depth', 'complexity'],
                success_criteria_template=[
                    "Complete data analysis for {category}",
                    "Generate actionable insights for {user_input}",
                    "Validate analysis accuracy"
                ],
                dependencies_template=['research']
            ),
            'implementation': TaskTemplate(
                category='implementation',
                name_pattern="Implementation Task {number}: Solution Development",
                description_pattern="Implement solution components for: {user_input}. Develop {complexity} level implementation with focus on {domain_keywords}.",
                min_tasks=5,
                max_tasks=10,
                complexity_factors=['technical_complexity', 'integration_requirements', 'scalability'],
                success_criteria_template=[
                    "Complete {category} development requirements",
                    "Deliver working solution for {user_input}",
                    "Meet technical specifications"
                ],
                dependencies_template=['research', 'analysis']
            ),
            'validation': TaskTemplate(
                category='validation',
                name_pattern="Validation Task {number}: Quality Assurance",
                description_pattern="Validate implementation and ensure quality for: {user_input}. Perform {complexity} level validation with emphasis on {domain_keywords}.",
                min_tasks=2,
                max_tasks=3,
                complexity_factors=['validation_scope', 'quality_requirements', 'testing_depth'],
                success_criteria_template=[
                    "Complete {category} validation requirements",
                    "Ensure quality standards for {user_input}",
                    "Validate all success criteria"
                ],
                dependencies_template=['implementation']
            ),
            'documentation': TaskTemplate(
                category='documentation',
                name_pattern="Documentation Task {number}: Documentation Update",
                description_pattern="Create and update documentation for: {user_input}. Develop {complexity} level documentation covering {domain_keywords}.",
                min_tasks=1,
                max_tasks=2,
                complexity_factors=['documentation_scope', 'detail_level', 'audience'],
                success_criteria_template=[
                    "Complete {category} documentation requirements",
                    "Create comprehensive documentation for {user_input}",
                    "Ensure documentation accuracy and completeness"
                ],
                dependencies_template=['implementation', 'validation']
            )
        }
    
    def _initialize_system(self) -> None:
        """Initialize the task structure system"""
        print("🏗️ A.M.A.S.I.A.P. Task Structure System initialized")
        print("   Categories: Research, Analysis, Implementation, Validation, Documentation")
        print("   Hierarchical structure with dependencies and execution order")

# Global task structure system instance
AMASIAP_TASK_STRUCTURE = AMASIAPTaskStructureSystem()

# Convenience function for task structure creation
def create_amasiap_task_structure(user_input: str) -> Dict[str, Any]:
    """Create A.M.A.S.I.A.P. task structure for user input"""
    return AMASIAP_TASK_STRUCTURE.create_hierarchical_task_structure(user_input)

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing A.M.A.S.I.A.P. Task Structure System...")
    
    # Test task structure creation
    test_input = "Enhance the entire system with automated protocols"
    structure = create_amasiap_task_structure(test_input)
    
    print(f"\n📊 TASK STRUCTURE SUMMARY:")
    print(f"   Structure ID: {structure['structure_id']}")
    print(f"   Total Tasks: {structure['total_tasks']}")
    print(f"   Estimated Duration: {structure['estimated_total_duration']}")
    print(f"   Input Complexity: {structure['analysis']['input_complexity']}")
    
    # Show category breakdown
    for category, details in structure['task_structure'].items():
        print(f"   {category.title()}: {details['count']} tasks ({details['estimated_duration']})")
    
    print("\n✅ A.M.A.S.I.A.P. Task Structure System test completed")
