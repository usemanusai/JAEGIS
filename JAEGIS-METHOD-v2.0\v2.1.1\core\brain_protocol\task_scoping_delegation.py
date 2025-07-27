"""
JAEGIS Brain Protocol Suite v1.0 - Task Scoping & Agent Delegation Protocol
Directive 1.2: Automatic agent selection and squad formation for task delegation

This module implements the mandatory task analysis and agent delegation protocol
that ensures logical delegation of tasks to specialized JAEGIS components.
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class TaskComplexity(str, Enum):
    """Task complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"


class TaskCategory(str, Enum):
    """Primary task categories."""
    DEVELOPMENT = "development"
    DOCUMENTATION = "documentation"
    ANALYSIS = "analysis"
    ARCHITECTURE = "architecture"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    RESEARCH = "research"
    INTEGRATION = "integration"
    OPTIMIZATION = "optimization"
    SECURITY = "security"


class AgentTier(str, Enum):
    """JAEGIS agent tier levels."""
    TIER_0 = "tier_0"  # N.L.D.S.
    TIER_1 = "tier_1"  # JAEGIS Orchestrator
    TIER_2 = "tier_2"  # John, Fred, Tyler
    TIER_3 = "tier_3"  # 16 specialized agents
    TIER_4 = "tier_4"  # 4 conditional agents
    TIER_5 = "tier_5"  # IUAS Squad (20 agents)
    TIER_6 = "tier_6"  # GARAS Squad (40 agents)


@dataclass
class JAEGISAgent:
    """JAEGIS agent definition."""
    agent_id: str
    name: str
    tier: AgentTier
    specializations: List[str]
    capabilities: List[str]
    task_categories: List[TaskCategory]
    complexity_range: List[TaskComplexity]
    collaboration_agents: List[str]
    load_capacity: int
    current_load: int = 0


@dataclass
class JAEGISSquad:
    """JAEGIS squad definition."""
    squad_id: str
    name: str
    description: str
    lead_agent: str
    member_agents: List[str]
    specialization: str
    task_categories: List[TaskCategory]
    coordination_protocol: str


@dataclass
class TaskAnalysis:
    """Comprehensive task analysis result."""
    task_id: str
    original_request: str
    task_category: TaskCategory
    task_complexity: TaskComplexity
    required_capabilities: List[str]
    estimated_duration_hours: float
    dependencies: List[str]
    deliverables: List[str]
    success_criteria: List[str]


@dataclass
class DelegationDecision:
    """Agent delegation decision."""
    task_id: str
    delegation_type: str  # "single_agent" or "squad"
    selected_agent: Optional[str]
    selected_squad: Optional[str]
    squad_members: List[str]
    delegation_rationale: str
    confidence_score: float
    alternative_options: List[str]
    timestamp: float


class TaskScopingDelegationEngine:
    """
    JAEGIS Brain Protocol Suite Task Scoping & Delegation Engine
    
    Implements Directive 1.2: Task Scoping & Agent Delegation Protocol
    
    Mandatory execution sequence:
    1. Force Agent Selection - Analyze request and select best agent
    2. Force Squad Selection - Define squad for multi-capability tasks
    3. Logical Delegation - Ensure optimal resource allocation
    """
    
    def __init__(self):
        self.agents: Dict[str, JAEGISAgent] = {}
        self.squads: Dict[str, JAEGISSquad] = {}
        self.delegation_history: List[DelegationDecision] = []
        
        # Initialize JAEGIS agent registry
        self._initialize_agent_registry()
        self._initialize_squad_registry()
        
        logger.info("Task Scoping & Delegation Engine initialized")
    
    def _initialize_agent_registry(self):
        """Initialize the complete JAEGIS agent registry."""
        
        # Tier 0: N.L.D.S.
        self.agents["nlds"] = JAEGISAgent(
            agent_id="nlds",
            name="Natural Language Detection System",
            tier=AgentTier.TIER_0,
            specializations=["natural_language_processing", "intent_analysis", "command_optimization"],
            capabilities=["multi_dimensional_analysis", "confidence_validation", "real_time_processing"],
            task_categories=[TaskCategory.ANALYSIS, TaskCategory.RESEARCH],
            complexity_range=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE, TaskComplexity.COMPLEX],
            collaboration_agents=["jaegis_orchestrator"],
            load_capacity=1000
        )
        
        # Tier 1: JAEGIS Orchestrator
        self.agents["jaegis_orchestrator"] = JAEGISAgent(
            agent_id="jaegis_orchestrator",
            name="JAEGIS Master Orchestrator",
            tier=AgentTier.TIER_1,
            specializations=["system_orchestration", "agent_coordination", "workflow_management"],
            capabilities=["master_coordination", "resource_allocation", "priority_management"],
            task_categories=list(TaskCategory),  # All categories
            complexity_range=list(TaskComplexity),  # All complexity levels
            collaboration_agents=["john", "fred", "tyler"],
            load_capacity=100
        )
        
        # Tier 2: Core Agents
        tier_2_agents = [
            {
                "agent_id": "john",
                "name": "John - Research & Analysis Specialist",
                "specializations": ["research", "data_analysis", "market_intelligence"],
                "capabilities": ["comprehensive_research", "data_synthesis", "trend_analysis"],
                "task_categories": [TaskCategory.RESEARCH, TaskCategory.ANALYSIS]
            },
            {
                "agent_id": "fred",
                "name": "Fred - Architecture & Design Specialist", 
                "specializations": ["system_architecture", "design_patterns", "technical_leadership"],
                "capabilities": ["architectural_design", "system_planning", "technical_guidance"],
                "task_categories": [TaskCategory.ARCHITECTURE, TaskCategory.DEVELOPMENT]
            },
            {
                "agent_id": "tyler",
                "name": "Tyler - Implementation & Task Specialist",
                "specializations": ["task_execution", "implementation", "project_management"],
                "capabilities": ["rapid_implementation", "task_coordination", "delivery_management"],
                "task_categories": [TaskCategory.DEVELOPMENT, TaskCategory.TESTING, TaskCategory.DEPLOYMENT]
            }
        ]
        
        for agent_data in tier_2_agents:
            self.agents[agent_data["agent_id"]] = JAEGISAgent(
                agent_id=agent_data["agent_id"],
                name=agent_data["name"],
                tier=AgentTier.TIER_2,
                specializations=agent_data["specializations"],
                capabilities=agent_data["capabilities"],
                task_categories=agent_data["task_categories"],
                complexity_range=[TaskComplexity.MODERATE, TaskComplexity.COMPLEX, TaskComplexity.ENTERPRISE],
                collaboration_agents=["jaegis_orchestrator"],
                load_capacity=50
            )
        
        # Add placeholder entries for other tiers
        self._add_tier_3_agents()
        self._add_tier_4_agents()
        self._add_tier_5_agents()  # IUAS Squad
        self._add_tier_6_agents()  # GARAS Squad
    
    def _add_tier_3_agents(self):
        """Add Tier 3 specialized agents (16 agents)."""
        
        tier_3_specializations = [
            "api_development", "database_design", "frontend_development", "backend_development",
            "devops_automation", "security_implementation", "testing_automation", "documentation_generation",
            "performance_optimization", "integration_management", "monitoring_setup", "deployment_automation",
            "code_review", "quality_assurance", "user_experience", "data_processing"
        ]
        
        for i, specialization in enumerate(tier_3_specializations):
            agent_id = f"tier3_agent_{i+1:02d}"
            self.agents[agent_id] = JAEGISAgent(
                agent_id=agent_id,
                name=f"Tier 3 {specialization.replace('_', ' ').title()} Specialist",
                tier=AgentTier.TIER_3,
                specializations=[specialization],
                capabilities=[f"{specialization}_expertise"],
                task_categories=[TaskCategory.DEVELOPMENT, TaskCategory.TESTING],
                complexity_range=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE],
                collaboration_agents=["fred", "tyler"],
                load_capacity=20
            )
    
    def _add_tier_4_agents(self):
        """Add Tier 4 conditional agents (4 agents)."""
        
        tier_4_agents = [
            "emergency_response", "crisis_management", "escalation_handling", "recovery_operations"
        ]
        
        for i, specialization in enumerate(tier_4_agents):
            agent_id = f"tier4_agent_{i+1:02d}"
            self.agents[agent_id] = JAEGISAgent(
                agent_id=agent_id,
                name=f"Tier 4 {specialization.replace('_', ' ').title()} Agent",
                tier=AgentTier.TIER_4,
                specializations=[specialization],
                capabilities=[f"{specialization}_capability"],
                task_categories=[TaskCategory.SECURITY, TaskCategory.OPTIMIZATION],
                complexity_range=[TaskComplexity.COMPLEX, TaskComplexity.ENTERPRISE],
                collaboration_agents=["jaegis_orchestrator"],
                load_capacity=10
            )
    
    def _add_tier_5_agents(self):
        """Add Tier 5 IUAS Squad agents (20 agents)."""
        
        for i in range(20):
            agent_id = f"iuas_agent_{i+1:02d}"
            self.agents[agent_id] = JAEGISAgent(
                agent_id=agent_id,
                name=f"IUAS Agent {i+1:02d}",
                tier=AgentTier.TIER_5,
                specializations=["system_maintenance", "updates", "synchronization"],
                capabilities=["maintenance_operations", "update_coordination", "sync_management"],
                task_categories=[TaskCategory.INTEGRATION, TaskCategory.OPTIMIZATION],
                complexity_range=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE],
                collaboration_agents=["iuas_squad"],
                load_capacity=15
            )
    
    def _add_tier_6_agents(self):
        """Add Tier 6 GARAS Squad agents (40 agents)."""
        
        for i in range(40):
            agent_id = f"garas_agent_{i+1:02d}"
            self.agents[agent_id] = JAEGISAgent(
                agent_id=agent_id,
                name=f"GARAS Agent {i+1:02d}",
                tier=AgentTier.TIER_6,
                specializations=["gap_analysis", "resolution", "pattern_recognition"],
                capabilities=["gap_detection", "analysis_resolution", "pattern_analysis"],
                task_categories=[TaskCategory.ANALYSIS, TaskCategory.RESEARCH],
                complexity_range=[TaskComplexity.MODERATE, TaskComplexity.COMPLEX],
                collaboration_agents=["garas_squad"],
                load_capacity=10
            )
    
    def _initialize_squad_registry(self):
        """Initialize the JAEGIS squad registry."""
        
        # IUAS Squad
        self.squads["iuas_squad"] = JAEGISSquad(
            squad_id="iuas_squad",
            name="Internal Updates Agent Squad",
            description="20-agent squad for system maintenance and synchronization",
            lead_agent="iuas_agent_01",
            member_agents=[f"iuas_agent_{i+1:02d}" for i in range(20)],
            specialization="system_maintenance_and_updates",
            task_categories=[TaskCategory.INTEGRATION, TaskCategory.OPTIMIZATION],
            coordination_protocol="maintenance_coordination"
        )
        
        # GARAS Squad
        self.squads["garas_squad"] = JAEGISSquad(
            squad_id="garas_squad",
            name="Gaps Analysis and Resolution Agent Squad",
            description="40-agent squad for comprehensive gap analysis and resolution",
            lead_agent="garas_agent_01",
            member_agents=[f"garas_agent_{i+1:02d}" for i in range(40)],
            specialization="gap_analysis_and_resolution",
            task_categories=[TaskCategory.ANALYSIS, TaskCategory.RESEARCH],
            coordination_protocol="gap_analysis_coordination"
        )
        
        # Content Squad
        self.squads["content_squad"] = JAEGISSquad(
            squad_id="content_squad",
            name="Content Validation Squad",
            description="8-agent squad for content validation and quality assurance",
            lead_agent="tier3_agent_08",  # Documentation specialist
            member_agents=[f"tier3_agent_{i+8:02d}" for i in range(8)],
            specialization="content_validation_and_quality",
            task_categories=[TaskCategory.DOCUMENTATION, TaskCategory.TESTING],
            coordination_protocol="content_validation_coordination"
        )
    
    async def force_agent_selection(self, user_request: str) -> DelegationDecision:
        """
        MANDATORY: Analyze request and explicitly select best suited agent
        
        This method MUST analyze the user's primary objective and explicitly
        state which JAEGIS agent is best suited for the task.
        """
        
        task_id = f"task_{int(time.time())}_{hash(user_request) % 10000}"
        
        logger.info(f"🎯 FORCE AGENT SELECTION - Task ID: {task_id}")
        logger.info(f"📝 User Request: {user_request[:100]}...")
        
        # Step 1: Analyze the task
        task_analysis = await self._analyze_task(task_id, user_request)
        
        # Step 2: Find best matching agent
        best_agent = await self._find_best_agent(task_analysis)
        
        # Step 3: Create delegation decision
        delegation_decision = DelegationDecision(
            task_id=task_id,
            delegation_type="single_agent",
            selected_agent=best_agent.agent_id,
            selected_squad=None,
            squad_members=[],
            delegation_rationale=f"Selected {best_agent.name} based on specializations: {', '.join(best_agent.specializations)}",
            confidence_score=0.85,  # Simplified confidence calculation
            alternative_options=await self._get_alternative_agents(task_analysis),
            timestamp=time.time()
        )
        
        # Update agent load
        best_agent.current_load += 1
        
        # Store delegation history
        self.delegation_history.append(delegation_decision)
        
        logger.info(f"✅ Agent Selected: {best_agent.name}")
        logger.info(f"🎯 Delegation Rationale: {delegation_decision.delegation_rationale}")
        
        return delegation_decision
    
    async def force_squad_selection(self, user_request: str) -> DelegationDecision:
        """
        MANDATORY: Define squad for multi-capability tasks
        
        This method MUST define a JAEGIS Squad by selecting necessary agents
        and defining their roles and collaboration workflow.
        """
        
        task_id = f"squad_task_{int(time.time())}_{hash(user_request) % 10000}"
        
        logger.info(f"👥 FORCE SQUAD SELECTION - Task ID: {task_id}")
        logger.info(f"📝 User Request: {user_request[:100]}...")
        
        # Step 1: Analyze the task
        task_analysis = await self._analyze_task(task_id, user_request)
        
        # Step 2: Determine if squad is needed
        requires_squad = await self._requires_squad_coordination(task_analysis)
        
        if not requires_squad:
            # Fallback to single agent
            return await self.force_agent_selection(user_request)
        
        # Step 3: Select best squad
        best_squad = await self._find_best_squad(task_analysis)
        
        # Step 4: Create squad delegation decision
        delegation_decision = DelegationDecision(
            task_id=task_id,
            delegation_type="squad",
            selected_agent=None,
            selected_squad=best_squad.squad_id,
            squad_members=best_squad.member_agents,
            delegation_rationale=f"Selected {best_squad.name} for multi-capability task requiring: {best_squad.specialization}",
            confidence_score=0.90,  # Higher confidence for squad tasks
            alternative_options=await self._get_alternative_squads(task_analysis),
            timestamp=time.time()
        )
        
        # Store delegation history
        self.delegation_history.append(delegation_decision)
        
        logger.info(f"✅ Squad Selected: {best_squad.name}")
        logger.info(f"👥 Squad Members: {len(best_squad.member_agents)} agents")
        logger.info(f"🎯 Delegation Rationale: {delegation_decision.delegation_rationale}")
        
        return delegation_decision
    
    async def _analyze_task(self, task_id: str, user_request: str) -> TaskAnalysis:
        """Analyze the user request to determine task characteristics."""
        
        # Simple keyword-based analysis (in production, would use N.L.D.S.)
        request_lower = user_request.lower()
        
        # Determine task category
        task_category = TaskCategory.DEVELOPMENT  # Default
        
        if any(word in request_lower for word in ["document", "write", "readme", "guide"]):
            task_category = TaskCategory.DOCUMENTATION
        elif any(word in request_lower for word in ["analyze", "research", "investigate"]):
            task_category = TaskCategory.ANALYSIS
        elif any(word in request_lower for word in ["architecture", "design", "structure"]):
            task_category = TaskCategory.ARCHITECTURE
        elif any(word in request_lower for word in ["test", "validate", "verify"]):
            task_category = TaskCategory.TESTING
        elif any(word in request_lower for word in ["deploy", "release", "publish"]):
            task_category = TaskCategory.DEPLOYMENT
        elif any(word in request_lower for word in ["integrate", "connect", "sync"]):
            task_category = TaskCategory.INTEGRATION
        elif any(word in request_lower for word in ["optimize", "improve", "enhance"]):
            task_category = TaskCategory.OPTIMIZATION
        elif any(word in request_lower for word in ["security", "secure", "protect"]):
            task_category = TaskCategory.SECURITY
        
        # Determine complexity
        complexity = TaskComplexity.MODERATE  # Default
        
        if any(word in request_lower for word in ["simple", "basic", "quick"]):
            complexity = TaskComplexity.SIMPLE
        elif any(word in request_lower for word in ["complex", "comprehensive", "advanced"]):
            complexity = TaskComplexity.COMPLEX
        elif any(word in request_lower for word in ["enterprise", "production", "scale"]):
            complexity = TaskComplexity.ENTERPRISE
        
        # Extract capabilities (simplified)
        required_capabilities = []
        if "api" in request_lower:
            required_capabilities.append("api_development")
        if "database" in request_lower:
            required_capabilities.append("database_design")
        if "frontend" in request_lower:
            required_capabilities.append("frontend_development")
        if "backend" in request_lower:
            required_capabilities.append("backend_development")
        
        return TaskAnalysis(
            task_id=task_id,
            original_request=user_request,
            task_category=task_category,
            task_complexity=complexity,
            required_capabilities=required_capabilities,
            estimated_duration_hours=2.0,  # Simplified estimation
            dependencies=[],
            deliverables=["task_completion"],
            success_criteria=["requirements_met", "quality_validated"]
        )
    
    async def _find_best_agent(self, task_analysis: TaskAnalysis) -> JAEGISAgent:
        """Find the best agent for the analyzed task."""
        
        # Score agents based on task fit
        agent_scores = {}
        
        for agent_id, agent in self.agents.items():
            score = 0.0
            
            # Category match
            if task_analysis.task_category in agent.task_categories:
                score += 40.0
            
            # Complexity match
            if task_analysis.task_complexity in agent.complexity_range:
                score += 30.0
            
            # Capability match
            for capability in task_analysis.required_capabilities:
                if capability in agent.specializations:
                    score += 20.0
            
            # Load factor (prefer less loaded agents)
            load_factor = 1.0 - (agent.current_load / agent.load_capacity)
            score += load_factor * 10.0
            
            agent_scores[agent_id] = score
        
        # Select highest scoring agent
        best_agent_id = max(agent_scores.items(), key=lambda x: x[1])[0]
        return self.agents[best_agent_id]
    
    async def _requires_squad_coordination(self, task_analysis: TaskAnalysis) -> bool:
        """Determine if the task requires squad coordination."""
        
        # Squad required for complex tasks with multiple capabilities
        if task_analysis.task_complexity in [TaskComplexity.COMPLEX, TaskComplexity.ENTERPRISE]:
            return True
        
        # Squad required for multiple capability requirements
        if len(task_analysis.required_capabilities) > 2:
            return True
        
        # Squad required for specific keywords
        squad_keywords = ["comprehensive", "complete", "full", "entire", "system"]
        if any(keyword in task_analysis.original_request.lower() for keyword in squad_keywords):
            return True
        
        return False
    
    async def _find_best_squad(self, task_analysis: TaskAnalysis) -> JAEGISSquad:
        """Find the best squad for the analyzed task."""
        
        # Simple squad selection based on task category
        if task_analysis.task_category in [TaskCategory.ANALYSIS, TaskCategory.RESEARCH]:
            return self.squads["garas_squad"]
        elif task_analysis.task_category in [TaskCategory.INTEGRATION, TaskCategory.OPTIMIZATION]:
            return self.squads["iuas_squad"]
        elif task_analysis.task_category == TaskCategory.DOCUMENTATION:
            return self.squads["content_squad"]
        else:
            # Default to GARAS for comprehensive analysis
            return self.squads["garas_squad"]
    
    async def _get_alternative_agents(self, task_analysis: TaskAnalysis) -> List[str]:
        """Get alternative agent options."""
        
        alternatives = []
        for agent_id, agent in self.agents.items():
            if (task_analysis.task_category in agent.task_categories and
                task_analysis.task_complexity in agent.complexity_range):
                alternatives.append(agent_id)
        
        return alternatives[:3]  # Top 3 alternatives
    
    async def _get_alternative_squads(self, task_analysis: TaskAnalysis) -> List[str]:
        """Get alternative squad options."""
        
        return list(self.squads.keys())
    
    def get_delegation_status(self) -> Dict[str, Any]:
        """Get current delegation system status."""
        
        total_agents = len(self.agents)
        active_agents = len([a for a in self.agents.values() if a.current_load > 0])
        total_squads = len(self.squads)
        
        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "total_squads": total_squads,
            "delegation_history": len(self.delegation_history),
            "agent_utilization": active_agents / total_agents if total_agents > 0 else 0,
            "recent_delegations": len([d for d in self.delegation_history if time.time() - d.timestamp < 3600])
        }
    
    def get_agent_registry(self) -> Dict[str, Dict[str, Any]]:
        """Get complete agent registry."""
        
        return {
            agent_id: {
                "name": agent.name,
                "tier": agent.tier.value,
                "specializations": agent.specializations,
                "task_categories": [cat.value for cat in agent.task_categories],
                "current_load": agent.current_load,
                "load_capacity": agent.load_capacity,
                "utilization": agent.current_load / agent.load_capacity
            }
            for agent_id, agent in self.agents.items()
        }


# Global delegation engine instance
TASK_DELEGATION_ENGINE = TaskScopingDelegationEngine()


async def mandatory_agent_delegation(user_request: str) -> DelegationDecision:
    """
    MANDATORY: Delegate user request to appropriate JAEGIS agent or squad
    
    This function MUST be called for every user request to ensure proper
    task delegation according to JAEGIS Brain Protocol Suite Directive 1.2.
    """
    
    # Determine if squad coordination is needed
    task_analysis = await TASK_DELEGATION_ENGINE._analyze_task("temp", user_request)
    requires_squad = await TASK_DELEGATION_ENGINE._requires_squad_coordination(task_analysis)
    
    if requires_squad:
        return await TASK_DELEGATION_ENGINE.force_squad_selection(user_request)
    else:
        return await TASK_DELEGATION_ENGINE.force_agent_selection(user_request)


# Example usage
async def main():
    """Example usage of Task Scoping & Delegation Engine."""
    
    print("🎯 JAEGIS BRAIN PROTOCOL SUITE - TASK DELEGATION TEST")
    
    # Test single agent delegation
    single_task = "Create a comprehensive API documentation system"
    delegation = await TASK_DELEGATION_ENGINE.force_agent_selection(single_task)
    
    print(f"\n✅ Single Agent Delegation:")
    print(f"  Task: {single_task}")
    print(f"  Selected Agent: {delegation.selected_agent}")
    print(f"  Rationale: {delegation.delegation_rationale}")
    
    # Test squad delegation
    squad_task = "Implement a complete enterprise security system with monitoring"
    squad_delegation = await TASK_DELEGATION_ENGINE.force_squad_selection(squad_task)
    
    print(f"\n👥 Squad Delegation:")
    print(f"  Task: {squad_task}")
    print(f"  Selected Squad: {squad_delegation.selected_squad}")
    print(f"  Squad Members: {len(squad_delegation.squad_members)}")
    print(f"  Rationale: {squad_delegation.delegation_rationale}")
    
    # Get system status
    status = TASK_DELEGATION_ENGINE.get_delegation_status()
    print(f"\n📊 Delegation System Status:")
    print(f"  Total Agents: {status['total_agents']}")
    print(f"  Active Agents: {status['active_agents']}")
    print(f"  Total Squads: {status['total_squads']}")
    print(f"  Agent Utilization: {status['agent_utilization']:.1%}")


if __name__ == "__main__":
    asyncio.run(main())
