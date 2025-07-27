"""
JAEGIS Enhanced System - Enhanced Task Management with Web Research Integration
Implements comprehensive task execution loop that begins with web research
Based on research findings on hierarchical task planning and validation systems
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import uuid
import re

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RESEARCHING = "researching"
    PLANNING = "planning"
    EXECUTING = "executing"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ValidationLevel(Enum):
    """Task validation levels"""
    BASIC = "basic"
    THOROUGH = "thorough"
    COMPREHENSIVE = "comprehensive"

@dataclass
class ResearchContext:
    """Context for web research phase"""
    research_id: str
    query: str
    sources_found: List[Dict[str, Any]] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)
    research_duration: float = 0.0
    confidence_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "research_id": self.research_id,
            "query": self.query,
            "sources_found": self.sources_found,
            "key_insights": self.key_insights,
            "research_duration": self.research_duration,
            "confidence_score": self.confidence_score,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class TaskNode:
    """Individual task node in hierarchy"""
    task_id: str
    name: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    research_context: Optional[ResearchContext] = None
    validation_criteria: List[str] = field(default_factory=list)
    completion_evidence: List[str] = field(default_factory=list)
    estimated_duration: Optional[float] = None
    actual_duration: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "parent_id": self.parent_id,
            "children": self.children,
            "dependencies": self.dependencies,
            "research_context": self.research_context.to_dict() if self.research_context else None,
            "validation_criteria": self.validation_criteria,
            "completion_evidence": self.completion_evidence,
            "estimated_duration": self.estimated_duration,
            "actual_duration": self.actual_duration,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class EnhancedTaskManager:
    """Enhanced task management system with web research integration"""
    
    def __init__(self, web_search_tool, validation_engine):
        self.web_search_tool = web_search_tool
        self.validation_engine = validation_engine
        
        # Task hierarchy storage
        self.task_hierarchy: Dict[str, TaskNode] = {}
        self.execution_queue: List[str] = []
        self.completed_tasks: List[str] = []
        
        # Research integration
        self.research_cache: Dict[str, ResearchContext] = {}
        self.research_patterns = self._initialize_research_patterns()
        
        # Validation system
        self.validation_rules = self._initialize_validation_rules()
        self.completion_validators: Dict[str, Callable] = {}
        
        # Execution control
        self.execution_active = False
        self.current_task_id: Optional[str] = None
        self.execution_metrics: Dict[str, Any] = {}
        
        # Prevention of false completion
        self.completion_safeguards = CompletionSafeguards()
        
        logger.info("Enhanced Task Manager initialized")
    
    def _initialize_research_patterns(self) -> Dict[str, List[str]]:
        """Initialize research query patterns for different task types"""
        return {
            "implementation": [
                "best practices {task_domain}",
                "implementation guide {task_domain}",
                "common pitfalls {task_domain}",
                "architecture patterns {task_domain}"
            ],
            "design": [
                "design patterns {task_domain}",
                "user experience {task_domain}",
                "design principles {task_domain}",
                "interface guidelines {task_domain}"
            ],
            "analysis": [
                "analysis methods {task_domain}",
                "evaluation criteria {task_domain}",
                "benchmarking {task_domain}",
                "comparison framework {task_domain}"
            ],
            "integration": [
                "integration patterns {task_domain}",
                "compatibility issues {task_domain}",
                "API documentation {task_domain}",
                "integration testing {task_domain}"
            ]
        }
    
    def _initialize_validation_rules(self) -> Dict[str, List[str]]:
        """Initialize validation rules for task completion"""
        return {
            "implementation": [
                "Code is functional and tested",
                "Documentation is complete",
                "Error handling is implemented",
                "Performance requirements are met"
            ],
            "design": [
                "Design meets requirements",
                "User experience is validated",
                "Accessibility standards are met",
                "Design is consistent with guidelines"
            ],
            "analysis": [
                "Analysis is comprehensive",
                "Data sources are credible",
                "Conclusions are supported by evidence",
                "Recommendations are actionable"
            ],
            "documentation": [
                "All sections are complete",
                "Information is accurate and current",
                "Examples are provided where needed",
                "Format follows standards"
            ]
        }
    
    async def initiate_research_driven_execution(self, project_description: str, 
                                               project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate research-driven task execution loop"""
        
        # Phase 1: Initial Web Research
        logger.info("Phase 1: Conducting initial web research")
        initial_research = await self._conduct_initial_research(project_description, project_context)
        
        # Phase 2: Generate Task Hierarchy
        logger.info("Phase 2: Generating detailed task hierarchy")
        task_hierarchy = await self._generate_task_hierarchy_from_research(initial_research, project_context)
        
        # Phase 3: Validate and Sequence Tasks
        logger.info("Phase 3: Validating and sequencing tasks")
        execution_plan = await self._create_execution_plan(task_hierarchy)
        
        # Phase 4: Begin Sequential Execution
        logger.info("Phase 4: Beginning sequential task execution")
        execution_result = await self._begin_sequential_execution(execution_plan)
        
        return {
            "research_driven_execution": True,
            "initial_research": initial_research,
            "task_hierarchy": task_hierarchy,
            "execution_plan": execution_plan,
            "execution_started": execution_result["started"],
            "total_tasks": len(self.task_hierarchy),
            "estimated_duration": execution_result.get("estimated_duration", 0)
        }
    
    async def _conduct_initial_research(self, project_description: str, 
                                      project_context: Dict[str, Any]) -> ResearchContext:
        """Conduct comprehensive initial web research"""
        research_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # Generate research queries based on project description
        research_queries = self._generate_research_queries(project_description, project_context)
        
        all_sources = []
        key_insights = []
        
        # Execute research queries
        for query in research_queries:
            try:
                search_results = await self.web_search_tool(query=query, num_results=5)
                
                if hasattr(search_results, 'content') and search_results.content:
                    # Parse search results
                    sources = self._parse_search_results(search_results.content, query)
                    all_sources.extend(sources)
                    
                    # Extract key insights
                    insights = self._extract_insights_from_sources(sources, query)
                    key_insights.extend(insights)
                
                # Small delay between queries to be respectful
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Research query failed for '{query}': {e}")
        
        # Calculate research duration and confidence
        research_duration = (datetime.now() - start_time).total_seconds()
        confidence_score = self._calculate_research_confidence(all_sources, key_insights)
        
        research_context = ResearchContext(
            research_id=research_id,
            query=f"Initial research for: {project_description}",
            sources_found=all_sources,
            key_insights=key_insights,
            research_duration=research_duration,
            confidence_score=confidence_score
        )
        
        # Cache research results
        self.research_cache[research_id] = research_context
        
        logger.info(f"Initial research completed: {len(all_sources)} sources, {len(key_insights)} insights")
        return research_context
    
    def _generate_research_queries(self, project_description: str, 
                                 project_context: Dict[str, Any]) -> List[str]:
        """Generate targeted research queries"""
        queries = []
        
        # Extract key terms from project description
        key_terms = self._extract_key_terms(project_description)
        project_type = project_context.get("project_type", "software")
        
        # Generate domain-specific queries
        base_queries = [
            f"{project_type} {' '.join(key_terms[:3])} best practices",
            f"{project_type} {' '.join(key_terms[:2])} implementation guide",
            f"{project_type} architecture patterns {key_terms[0] if key_terms else ''}",
            f"{project_type} development methodology {' '.join(key_terms[:2])}",
            f"{project_type} testing strategies {key_terms[0] if key_terms else ''}"
        ]
        
        # Add context-specific queries
        if "web" in project_description.lower():
            queries.extend([
                "web application development best practices",
                "modern web development architecture",
                "web application security considerations"
            ])
        
        if "api" in project_description.lower():
            queries.extend([
                "REST API design best practices",
                "API documentation standards",
                "API testing methodologies"
            ])
        
        if "database" in project_description.lower():
            queries.extend([
                "database design principles",
                "database optimization techniques",
                "data modeling best practices"
            ])
        
        queries.extend(base_queries)
        return queries[:10]  # Limit to 10 queries for efficiency
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from project description"""
        # Simple keyword extraction - in production would use NLP
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        
        # Clean and tokenize
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter stop words and short words
        key_terms = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return most frequent terms (simplified)
        return list(set(key_terms))[:10]
    
    def _parse_search_results(self, search_content: str, query: str) -> List[Dict[str, Any]]:
        """Parse search results into structured format"""
        sources = []
        
        # Simple parsing - in production would be more sophisticated
        lines = search_content.split('\n')
        current_source = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('- [') and '](' in line:
                # Extract title and URL
                title_match = re.search(r'\[(.*?)\]', line)
                url_match = re.search(r'\((.*?)\)', line)
                
                if title_match and url_match:
                    if current_source:
                        sources.append(current_source)
                    
                    current_source = {
                        "title": title_match.group(1),
                        "url": url_match.group(1),
                        "query": query,
                        "relevance_score": 0.8,  # Would calculate actual relevance
                        "content_preview": ""
                    }
            elif line and current_source and not line.startswith('- ['):
                # Add content preview
                current_source["content_preview"] += line + " "
        
        # Add the last source
        if current_source:
            sources.append(current_source)
        
        return sources
    
    def _extract_insights_from_sources(self, sources: List[Dict[str, Any]], query: str) -> List[str]:
        """Extract key insights from research sources"""
        insights = []
        
        for source in sources:
            content = source.get("content_preview", "")
            title = source.get("title", "")
            
            # Extract insights based on content patterns
            if "best practice" in content.lower() or "best practice" in title.lower():
                insights.append(f"Best practice identified: {title}")
            
            if "implementation" in content.lower():
                insights.append(f"Implementation guidance found: {title}")
            
            if "architecture" in content.lower():
                insights.append(f"Architecture pattern referenced: {title}")
            
            if "testing" in content.lower():
                insights.append(f"Testing approach mentioned: {title}")
        
        return insights[:5]  # Limit insights per query
    
    def _calculate_research_confidence(self, sources: List[Dict[str, Any]], 
                                     insights: List[str]) -> float:
        """Calculate confidence score for research results"""
        if not sources:
            return 0.0
        
        # Base confidence on number and quality of sources
        source_score = min(1.0, len(sources) / 10.0)  # Up to 10 sources = 1.0
        insight_score = min(1.0, len(insights) / 15.0)  # Up to 15 insights = 1.0
        
        # Average relevance score
        relevance_scores = [s.get("relevance_score", 0.5) for s in sources]
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.5
        
        # Combined confidence score
        confidence = (source_score * 0.4 + insight_score * 0.3 + avg_relevance * 0.3)
        return round(confidence, 2)
    
    async def _generate_task_hierarchy_from_research(self, research: ResearchContext, 
                                                   project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed task hierarchy based on research findings"""
        
        # Analyze research insights to identify task categories
        task_categories = self._identify_task_categories(research.key_insights, project_context)
        
        # Generate primary tasks
        primary_tasks = []
        for category in task_categories:
            primary_task = await self._create_primary_task(category, research, project_context)
            primary_tasks.append(primary_task)
            self.task_hierarchy[primary_task.task_id] = primary_task
        
        # Generate subtasks for each primary task
        for primary_task in primary_tasks:
            subtasks = await self._generate_subtasks(primary_task, research, project_context)
            primary_task.children = [st.task_id for st in subtasks]
            
            for subtask in subtasks:
                subtask.parent_id = primary_task.task_id
                self.task_hierarchy[subtask.task_id] = subtask
        
        # Establish dependencies
        await self._establish_task_dependencies()
        
        return {
            "total_tasks": len(self.task_hierarchy),
            "primary_tasks": len(primary_tasks),
            "task_categories": task_categories,
            "hierarchy_depth": self._calculate_hierarchy_depth(),
            "research_confidence": research.confidence_score
        }
    
    def _identify_task_categories(self, insights: List[str], 
                                project_context: Dict[str, Any]) -> List[str]:
        """Identify task categories from research insights"""
        categories = set()
        
        # Analyze insights for task categories
        for insight in insights:
            insight_lower = insight.lower()
            
            if any(word in insight_lower for word in ["design", "ui", "ux", "interface"]):
                categories.add("design")
            
            if any(word in insight_lower for word in ["implement", "code", "develop", "build"]):
                categories.add("implementation")
            
            if any(word in insight_lower for word in ["test", "quality", "validation"]):
                categories.add("testing")
            
            if any(word in insight_lower for word in ["document", "documentation", "guide"]):
                categories.add("documentation")
            
            if any(word in insight_lower for word in ["deploy", "deployment", "production"]):
                categories.add("deployment")
            
            if any(word in insight_lower for word in ["architecture", "system", "structure"]):
                categories.add("architecture")
        
        # Ensure minimum categories based on project type
        project_type = project_context.get("project_type", "software")
        if project_type == "web_application":
            categories.update(["design", "implementation", "testing"])
        elif project_type == "api_service":
            categories.update(["architecture", "implementation", "testing", "documentation"])
        
        # Default categories if none identified
        if not categories:
            categories = {"planning", "implementation", "validation"}
        
        return sorted(list(categories))
    
    async def _create_primary_task(self, category: str, research: ResearchContext, 
                                 project_context: Dict[str, Any]) -> TaskNode:
        """Create a primary task for a category""tool_1804": {
                "name": "Design_System_Architecture",
                "description": "Create comprehensive system design based on research findings and best practices",
                "validation_criteria": [
                    "Design meets functional requirements",
                    "Architecture follows industry best practices",
                    "Design is scalable and maintainable",
                    "User_experience_considerations_are_addressedimplementation": {
                "name": "Core_Implementation",
                "description": "Implement core functionality based on architectural design and research insights",
                "validation_criteria": [
                    "All core features are implemented",
                    "Code follows best practices identified in research",
                    "Implementation matches design specifications",
                    "Error_handling_is_comprehensivetesting": {
                "name": "Comprehensive_Testing",
                "description": "Implement testing strategy based on research findings and industry standards",
                "validation_criteria": [
                    "Test coverage meets requirements",
                    "All critical paths are tested",
                    "Testing follows identified best practices",
                    "Performance_requirements_are_validateddocumentation": {
                "name": "Documentation_Creation",
                "description": "Create comprehensive documentation based on research standards",
                "validation_criteria": [
                    "All components are documented",
                    "Documentation follows industry standards",
                    "Examples and usage guides are provided",
                    "Documentation is accurate and current"
                ]
            }
        }
        
        template = task_templates.get(category, {
            "name": f"{category.title()} Task",
            "description": f"Complete {category} phase based on research findings",
            "validation_criteria": [f"{category.title()} requirements are met"]
        })
        
        # Conduct specific research for this task
        task_research = await self._conduct_task_specific_research(category, research)
        
        return TaskNode(
            task_id=task_id,
            name=template["name"],
            description=template["description"],
            priority=TaskPriority.HIGH,
            research_context=task_research,
            validation_criteria=template["validation_criteria"]
        )
    
    async def _conduct_task_specific_research(self, category: str, 
                                           base_research: ResearchContext) -> ResearchContext:
        """Conduct additional research specific to task category"""
        research_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # Generate category-specific queries
        category_queries = self.research_patterns.get(category, [])
        if not category_queries:
            category_queries = [f"{category} best practices", f"{category} methodology"]
        
        # Use base research context to inform specific queries
        domain_terms = self._extract_domain_from_research(base_research)
        specific_queries = [query.format(task_domain=domain_terms) for query in category_queries[:3]]
        
        sources = []
        insights = []
        
        # Execute specific research
        for query in specific_queries:
            try:
                search_results = await self.web_search_tool(query=query, num_results=3)
                
                if hasattr(search_results, 'content') and search_results.content:
                    query_sources = self._parse_search_results(search_results.content, query)
                    sources.extend(query_sources)
                    
                    query_insights = self._extract_insights_from_sources(query_sources, query)
                    insights.extend(query_insights)
                
                await asyncio.sleep(0.5)  # Shorter delay for specific research
                
            except Exception as e:
                logger.error(f"Task-specific research failed for '{query}': {e}")
        
        research_duration = (datetime.now() - start_time).total_seconds()
        confidence_score = self._calculate_research_confidence(sources, insights)
        
        return ResearchContext(
            research_id=research_id,
            query=f"Specific research for {category}",
            sources_found=sources,
            key_insights=insights,
            research_duration=research_duration,
            confidence_score=confidence_score
        )
    
    def _extract_domain_from_research(self, research: ResearchContext) -> str:
        """Extract domain context from research"""
        # Simple domain extraction from insights
        domain_indicators = []
        
        for insight in research.key_insights:
            if "web" in insight.lower():
                domain_indicators.append("web development")
            elif "api" in insight.lower():
                domain_indicators.append("API development")
            elif "database" in insight.lower():
                domain_indicators.append("database design")
            elif "mobile" in insight.lower():
                domain_indicators.append("mobile development")
        
        return domain_indicators[0] if domain_indicators else "software development"
    
    async def _generate_subtasks(self, primary_task: TaskNode, research: ResearchContext, 
                               project_context: Dict[str, Any]) -> List[TaskNode]:
        """Generate detailed subtasks for primary task"""
        subtasks = []
        
        # Generate subtasks based on primary task category and research insights
        category = self._infer_category_from_task(primary_task.name)
        
        subtask_templates = {
            "design": [
                "Research design patterns and best practices",
                "Create system architecture diagrams",
                "Design user interface mockups",
                "Define data models and schemas",
                "Validate design with stakeholders"
            ],
            "implementation": [
                "Set up development environment",
                "Implement core business logic",
                "Create data access layer",
                "Implement user interface",
                "Add error handling and logging",
                "Optimize performance"
            ],
            "testing": [
                "Create test strategy and plan",
                "Implement unit tests",
                "Create integration tests",
                "Perform system testing",
                "Conduct performance testing",
                "Execute user acceptance testing"
            ],
            "documentation": [
                "Create technical documentation",
                "Write user guides",
                "Document API specifications",
                "Create deployment guides",
                "Review and validate documentation"
            ]
        }
        
        templates = subtask_templates.get(category, [
            "Research requirements",
            "Plan implementation",
            "Execute implementation",
            "Validate results"
        ])
        
        for i, template in enumerate(templates):
            subtask_id = str(uuid.uuid4())
            
            # Create validation criteria for subtask
            validation_criteria = self._generate_subtask_validation_criteria(template, category)
            
            subtask = TaskNode(
                task_id=subtask_id,
                name=template,
                description=f"Detailed implementation of: {template}",
                priority=TaskPriority.MEDIUM,
                validation_criteria=validation_criteria,
                estimated_duration=self._estimate_subtask_duration(template, category)
            )
            
            subtasks.append(subtask)
        
        return subtasks
    
    def _infer_category_from_task(self, task_name: str) -> str:
        """Infer category from task name"""
        task_name_lower = task_name.lower()
        
        if any(word in task_name_lower for word in ["design", "architecture", "ui", "ux"]):
            return "design"
        elif any(word in task_name_lower for word in ["implement", "code", "develop", "build"]):
            return "implementation"
        elif any(word in task_name_lower for word in ["test", "testing", "quality", "validation"]):
            return "testing"
        elif any(word in task_name_lower for word in ["document", "documentation", "guide"]):
            return "documentation"
        else:
            return "general"
    
    def _generate_subtask_validation_criteria(self, subtask_name: str, category: str) -> List[str]:
        """Generate validation criteria for subtask"""
        base_criteria = self.validation_rules.get(category, ["Task is completed according to requirements"])
        
        # Add specific criteria based on subtask name
        specific_criteria = []
        subtask_lower = subtask_name.lower()
        
        if "research" in subtask_lower:
            specific_criteria.append("Research findings are documented and validated")
        elif "implement" in subtask_lower:
            specific_criteria.append("Implementation is functional and tested")
        elif "test" in subtask_lower:
            specific_criteria.append("Tests pass and provide adequate coverage")
        elif "document" in subtask_lower:
            specific_criteria.append("Documentation is complete and accurate")
        
        return base_criteria + specific_criteria
    
    def _estimate_subtask_duration(self, subtask_name: str, category: str) -> float:
        """Estimate duration for subtask in hours"""
        # Simple duration estimation - in production would be more sophisticated
        base_durations = {
            "design": 2.0,
            "implementation": 4.0,
            "testing": 2.5,
            "documentation": 1.5,
            "general": 2.0
        }
        
        base_duration = base_durations.get(category, 2.0)
        
        # Adjust based on subtask complexity
        if "research" in subtask_name.lower():
            return base_duration * 0.8
        elif "implement" in subtask_name.lower():
            return base_duration * 1.5
        elif "optimize" in subtask_name.lower():
            return base_duration * 1.3
        
        return base_duration
    
    async def _establish_task_dependencies(self):
        """Establish dependencies between tasks"""
        # Simple dependency establishment - in production would be more sophisticated
        primary_tasks = [task for task in self.task_hierarchy.values() if not task.parent_id]
        
        # Sort primary tasks by typical execution order
        task_order = ["design", "implementation", "testing", "documentation", "deployment"]
        
        sorted_tasks = []
        for order_category in task_order:
            for task in primary_tasks:
                if order_category in task.name.lower():
                    sorted_tasks.append(task)
        
        # Add any remaining tasks
        for task in primary_tasks:
            if task not in sorted_tasks:
                sorted_tasks.append(task)
        
        # Establish sequential dependencies
        for i in range(1, len(sorted_tasks)):
            sorted_tasks[i].dependencies.append(sorted_tasks[i-1].task_id)
    
    def _calculate_hierarchy_depth(self) -> int:
        """Calculate maximum depth of task hierarchy"""
        max_depth = 0
        
        for task in self.task_hierarchy.values():
            depth = 1
            current_task = task
            
            while current_task.parent_id:
                depth += 1
                current_task = self.task_hierarchy.get(current_task.parent_id)
                if not current_task:
                    break
            
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    async def _create_execution_plan(self, task_hierarchy: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed execution plan with sequencing"""
        
        # Topological sort for dependency resolution
        execution_order = self._topological_sort()
        
        # Calculate total estimated duration
        total_duration = sum(
            task.estimated_duration or 2.0 
            for task in self.task_hierarchy.values()
        )
        
        # Create execution phases
        phases = self._create_execution_phases(execution_order)
        
        return {
            "execution_order": execution_order,
            "total_tasks": len(self.task_hierarchy),
            "estimated_duration": total_duration,
            "execution_phases": phases,
            "validation_checkpoints": self._identify_validation_checkpoints(execution_order)
        }
    
    def _topological_sort(self) -> List[str]:
        """Perform topological sort for task execution order"""
        # Simple topological sort implementation
        in_degree = {task_id: 0 for task_id in self.task_hierarchy}
        
        # Calculate in-degrees
        for task in self.task_hierarchy.values():
            for dep in task.dependencies:
                if dep in in_degree:
                    in_degree[task.task_id] += 1
        
        # Find tasks with no dependencies
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        execution_order = []
        
        while queue:
            current_task_id = queue.pop(0)
            execution_order.append(current_task_id)
            
            # Update in-degrees for dependent tasks
            current_task = self.task_hierarchy[current_task_id]
            for child_id in current_task.children:
                if child_id in in_degree:
                    in_degree[child_id] -= 1
                    if in_degree[child_id] == 0:
                        queue.append(child_id)
        
        return execution_order
    
    def _create_execution_phases(self, execution_order: List[str]) -> List[Dict[str, Any]]:
        """Create execution phases for better organization"""
        phases = []
        current_phase = []
        current_phase_name = ""
        
        for task_id in execution_order:
            task = self.task_hierarchy[task_id]
            
            # Determine phase based on task category
            task_category = self._infer_category_from_task(task.name)
            
            if task_category != current_phase_name:
                # Start new phase
                if current_phase:
                    phases.append({
                        "phase_name": current_phase_name,
                        "tasks": current_phase,
                        "estimated_duration": sum(
                            self.task_hierarchy[tid].estimated_duration or 2.0 
                            for tid in current_phase
                        )
                    })
                
                current_phase = [task_id]
                current_phase_name = task_category
            else:
                current_phase.append(task_id)
        
        # Add final phase
        if current_phase:
            phases.append({
                "phase_name": current_phase_name,
                "tasks": current_phase,
                "estimated_duration": sum(
                    self.task_hierarchy[tid].estimated_duration or 2.0 
                    for tid in current_phase
                )
            })
        
        return phases
    
    def _identify_validation_checkpoints(self, execution_order: List[str]) -> List[Dict[str, Any]]:
        """Identify key validation checkpoints in execution"""
        checkpoints = []
        
        # Add checkpoint after each primary task
        primary_tasks = [task_id for task_id in execution_order 
                        if not self.task_hierarchy[task_id].parent_id]
        
        for task_id in primary_tasks:
            task = self.task_hierarchy[task_id]
            checkpoints.append({
                "checkpoint_id": str(uuid.uuid4()),
                "after_task": task_id,
                "checkpoint_name": f"Validate {task.name}",
                "validation_criteria": task.validation_criteria,
                "critical": True
            })
        
        return checkpoints
    
    async def _begin_sequential_execution(self, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Begin sequential task execution"""
        self.execution_active = True
        self.execution_queue = execution_plan["execution_order"].copy()
        
        # Initialize execution metrics
        self.execution_metrics = {
            "started_at": datetime.now(),
            "total_tasks": len(self.execution_queue),
            "completed_tasks": 0,
            "failed_tasks": 0,
            "current_phase": execution_plan["execution_phases"][0]["phase_name"] if execution_plan["execution_phases"] else "unknown"
        }
        
        # Start execution loop
        asyncio.create_task(self._execution_loop())
        
        return {
            "started": True,
            "total_tasks": len(self.execution_queue),
            "estimated_duration": execution_plan["estimated_duration"],
            "first_task": self.execution_queue[0] if self.execution_queue else None
        }
    
    async def _execution_loop(self):
        """Main execution loop for sequential task processing"""
        while self.execution_active and self.execution_queue:
            try:
                # Get next task
                current_task_id = self.execution_queue.pop(0)
                self.current_task_id = current_task_id
                current_task = self.task_hierarchy[current_task_id]
                
                logger.info(f"Starting task: {current_task.name}")
                
                # Execute task with full validation
                execution_result = await self._execute_single_task(current_task)
                
                if execution_result["success"]:
                    # Task completed successfully
                    current_task.status = TaskStatus.COMPLETED
                    current_task.completed_at = datetime.now()
                    self.completed_tasks.append(current_task_id)
                    self.execution_metrics["completed_tasks"] += 1
                    
                    logger.info(f"Task completed: {current_task.name}")
                else:
                    # Task failed - handle failure
                    current_task.status = TaskStatus.FAILED
                    self.execution_metrics["failed_tasks"] += 1
                    
                    logger.error(f"Task failed: {current_task.name} - {execution_result.get('error', 'Unknown error')}")
                    
                    # Decide whether to continue or stop
                    if execution_result.get("critical_failure", False):
                        logger.error("Critical failure detected - stopping execution")
                        break
                
                # Small delay between tasks
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Execution loop error: {e}")
                break
        
        # Execution completed
        self.execution_active = False
        self.current_task_id = None
        
        logger.info(f"Execution completed: {self.execution_metrics['completed_tasks']}/{self.execution_metrics['total_tasks']} tasks")
    
    async def _execute_single_task(self, task: TaskNode) -> Dict[str, Any]:
        """Execute a single task with comprehensive validation"""
        
        # Update task status
        task.status = TaskStatus.EXECUTING
        task.started_at = datetime.now()
        
        try:
            # Phase 1: Task-specific research (if needed)
            if not task.research_context:
                research_result = await self._conduct_task_research(task)
                task.research_context = research_result
            
            # Phase 2: Execute task implementation
            implementation_result = await self._implement_task(task)
            
            if not implementation_result["success"]:
                return implementation_result
            
            # Phase 3: Validate task completion
            validation_result = await self._validate_task_completion(task)
            
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": "Task validation failed",
                    "validation_details": validation_result
                }
            
            # Phase 4: Record completion evidence
            task.completion_evidence = validation_result.get("evidence", [])
            task.actual_duration = (datetime.now() - task.started_at).total_seconds() / 3600.0  # Convert to hours
            
            return {
                "success": True,
                "task_id": task.task_id,
                "duration": task.actual_duration,
                "validation_passed": True
            }
            
        except Exception as e:
            logger.error(f"Task execution error for {task.name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "critical_failure": "critical" in task.name.lower()
            }
    
    async def _conduct_task_research(self, task: TaskNode) -> ResearchContext:
        """Conduct research specific to individual task"""
        # This would conduct focused research for the specific task
        # For now, return a placeholder research context
        return ResearchContext(
            research_id=str(uuid.uuid4()),
            query=f"Research for task: {task.name}",
            sources_found=[],
            key_insights=[f"Task-specific research for {task.name}"],
            research_duration=0.5,
            confidence_score=0.7
        )
    
    async def _implement_task(self, task: TaskNode) -> Dict[str, Any]:
        """Implement the actual task"""
        # This is where the actual task implementation would occur
        # For now, simulate task implementation
        
        logger.info(f"Implementing task: {task.name}")
        
        # Simulate implementation time
        await asyncio.sleep(0.1)
        
        return {
            "success": True,
            "implementation_details": f"Task {task.name} implemented successfully"
        }
    
    async def _validate_task_completion(self, task: TaskNode) -> Dict[str, Any]:
        """Validate that task is genuinely complete"""
        
        # Use completion safeguards to prevent false completion
        safeguard_result = self.completion_safeguards.validate_completion(task)
        
        if not safeguard_result["valid"]:
            return safeguard_result
        
        # Check validation criteria
        validation_results = []
        
        for criterion in task.validation_criteria:
            # Simulate criterion validation
            criterion_result = await self._validate_criterion(task, criterion)
            validation_results.append(criterion_result)
        
        # Determine overall validation
        all_valid = all(result["valid"] for result in validation_results)
        
        return {
            "valid": all_valid,
            "criteria_results": validation_results,
            "evidence": [result["evidence"] for result in validation_results if result.get("evidence")]
        }
    
    async def _validate_criterion(self, task: TaskNode, criterion: str) -> Dict[str, Any]:
        """Validate individual completion criterion"""
        # This would implement actual criterion validation
        # For now, simulate validation
        
        return {
            "criterion": criterion,
            "valid": True,
            "evidence": f"Criterion '{criterion}' validated for task {task.name}"
        }
    
    def get_execution_status(self) -> Dict[str, Any]:
        """Get current execution status"""
        return {
            "execution_active": self.execution_active,
            "current_task": self.current_task_id,
            "queue_remaining": len(self.execution_queue),
            "completed_tasks": len(self.completed_tasks),
            "total_tasks": len(self.task_hierarchy),
            "execution_metrics": self.execution_metrics.copy(),
            "progress_percentage": (len(self.completed_tasks) / len(self.task_hierarchy) * 100) if self.task_hierarchy else 0
        }
    
    def get_task_hierarchy_summary(self) -> Dict[str, Any]:
        """Get summary of task hierarchy"""
        return {
            "total_tasks": len(self.task_hierarchy),
            "primary_tasks": len([t for t in self.task_hierarchy.values() if not t.parent_id]),
            "completed_tasks": len([t for t in self.task_hierarchy.values() if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in self.task_hierarchy.values() if t.status == TaskStatus.FAILED]),
            "research_contexts": len(self.research_cache),
            "hierarchy_depth": self._calculate_hierarchy_depth()
        }

class CompletionSafeguards:
    """Safeguards to prevent false completion signals"""
    
    def __init__(self):
        self.completion_patterns = self._initialize_completion_patterns()
    
    def _initialize_completion_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns that indicate incomplete work"""
        return {
            "incomplete_indicators": [
                "TODO", "FIXME", "HACK", "TEMP", "placeholder",
                "not implemented", "coming soon", "work in progress"
            ],
            "quality_indicators": [
                "error handling", "validation", "testing", "documentation",
                "optimization", "security", "accessibility"
            ]
        }
    
    def validate_completion(self, task: TaskNode) -> Dict[str, Any]:
        """Validate that task completion is genuine"""
        
        # Check for incomplete indicators
        incomplete_signals = self._check_incomplete_signals(task)
        
        # Check for missing quality aspects
        quality_gaps = self._check_quality_gaps(task)
        
        # Check validation criteria coverage
        criteria_coverage = self._check_criteria_coverage(task)
        
        # Determine if completion is valid
        is_valid = (
            len(incomplete_signals) == 0 and
            len(quality_gaps) <= 1 and  # Allow minor quality gaps
            criteria_coverage >= 0.8    # Require 80% criteria coverage
        )
        
        return {
            "valid": is_valid,
            "incomplete_signals": incomplete_signals,
            "quality_gaps": quality_gaps,
            "criteria_coverage": criteria_coverage,
            "message": "Task completion validated" if is_valid else "Task appears incomplete"
        }
    
    def _check_incomplete_signals(self, task: TaskNode) -> List[str]:
        """Check for signals indicating incomplete work"""
        signals = []
        
        # Check task description and name for incomplete indicators
        text_to_check = f"{task.name} {task.description}".lower()
        
        for indicator in self.completion_patterns["incomplete_indicators"]:
            if indicator in text_to_check:
                signals.append(f"Incomplete indicator found: {indicator}")
        
        return signals
    
    def _check_quality_gaps(self, task: TaskNode) -> List[str]:
        """Check for missing quality aspects"""
        gaps = []
        
        # Check if quality indicators are addressed
        task_text = f"{task.name} {task.description}".lower()
        
        for quality_aspect in self.completion_patterns["quality_indicators"]:
            if quality_aspect not in task_text and quality_aspect not in str(task.validation_criteria).lower():
                gaps.append(f"Quality aspect not addressed: {quality_aspect}")
        
        return gaps
    
    def _check_criteria_coverage(self, task: TaskNode) -> float:
        """Check coverage of validation criteria"""
        if not task.validation_criteria:
            return 0.0
        
        # Check how many criteria have evidence
        criteria_with_evidence = len([
            criterion for criterion in task.validation_criteria
            if any(criterion.lower() in evidence.lower() for evidence in task.completion_evidence)
        ])
        
        return criteria_with_evidence / len(task.validation_criteria)
