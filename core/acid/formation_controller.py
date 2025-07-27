#!/usr/bin/env python3
"""
A.C.I.D. Formation Controller
Autonomous Cognitive Intelligence Directorate - Formation Mode

This module implements the Formation Mode controller for A.C.I.D., providing
manual agent squad configuration with hierarchical coordination and precise
control mechanisms for the JAEGIS A.E.G.I.S. Protocol Suite.

Formation Mode Features:
- Manual agent squad configuration
- Hierarchical coordination protocols
- Precise control mechanisms
- Task delegation and monitoring
- Resource allocation and optimization
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FormationMode(Enum):
    """Formation operation modes"""
    MANUAL = "manual"
    GUIDED = "guided"
    TEMPLATE = "template"
    ADAPTIVE = "adaptive"

class AgentRole(Enum):
    """Agent roles in formation"""
    LEADER = "leader"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"
    EXECUTOR = "executor"
    MONITOR = "monitor"

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class Agent:
    """Agent configuration and state"""
    id: str
    name: str
    role: AgentRole
    capabilities: List[str]
    current_task: Optional[str] = None
    status: str = "available"
    performance_score: float = 1.0
    last_active: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Task:
    """Task definition and tracking"""
    id: str
    name: str
    description: str
    priority: TaskPriority
    required_capabilities: List[str]
    assigned_agents: List[str] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Formation:
    """Formation configuration and state"""
    id: str
    name: str
    mode: FormationMode
    agents: List[Agent]
    tasks: List[Task]
    hierarchy: Dict[str, List[str]]  # leader_id -> [subordinate_ids]
    coordination_protocol: str
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "active"
    metadata: Dict[str, Any] = field(default_factory=dict)

class FormationController:
    """
    A.C.I.D. Formation Controller
    
    Manages manual agent squad configuration with hierarchical coordination
    and precise control mechanisms for optimal task execution.
    """
    
    def __init__(self):
        self.formations: Dict[str, Formation] = {}
        self.agent_registry: Dict[str, Agent] = {}
        self.task_queue: List[Task] = []
        self.active_tasks: Dict[str, Task] = {}
        self.performance_metrics: Dict[str, Any] = {}
        self.coordination_protocols: Dict[str, Any] = {}
        
        # Initialize default coordination protocols
        self._initialize_coordination_protocols()
        
        logger.info("A.C.I.D. Formation Controller initialized")
    
    def _initialize_coordination_protocols(self):
        """Initialize default coordination protocols"""
        self.coordination_protocols = {
            "hierarchical": {
                "communication_flow": "top_down",
                "decision_authority": "leader",
                "reporting_frequency": "real_time",
                "escalation_rules": ["performance_threshold", "time_threshold"]
            },
            "collaborative": {
                "communication_flow": "peer_to_peer",
                "decision_authority": "consensus",
                "reporting_frequency": "milestone",
                "escalation_rules": ["deadlock", "resource_conflict"]
            },
            "specialized": {
                "communication_flow": "domain_based",
                "decision_authority": "specialist",
                "reporting_frequency": "on_demand",
                "escalation_rules": ["capability_gap", "quality_threshold"]
            }
        }
    
    async def create_formation(
        self,
        name: str,
        mode: FormationMode,
        agents: List[Dict[str, Any]],
        coordination_protocol: str = "hierarchical"
    ) -> str:
        """
        Create a new agent formation
        
        Args:
            name: Formation name
            mode: Formation operation mode
            agents: List of agent configurations
            coordination_protocol: Coordination protocol to use
            
        Returns:
            Formation ID
        """
        formation_id = str(uuid.uuid4())
        
        # Create agent objects
        formation_agents = []
        for agent_config in agents:
            agent = Agent(
                id=agent_config.get("id", str(uuid.uuid4())),
                name=agent_config["name"],
                role=AgentRole(agent_config.get("role", "executor")),
                capabilities=agent_config.get("capabilities", []),
                metadata=agent_config.get("metadata", {})
            )
            formation_agents.append(agent)
            self.agent_registry[agent.id] = agent
        
        # Create formation
        formation = Formation(
            id=formation_id,
            name=name,
            mode=mode,
            agents=formation_agents,
            tasks=[],
            hierarchy=self._build_hierarchy(formation_agents),
            coordination_protocol=coordination_protocol
        )
        
        self.formations[formation_id] = formation
        
        logger.info(f"Created formation '{name}' with {len(formation_agents)} agents")
        return formation_id
    
    def _build_hierarchy(self, agents: List[Agent]) -> Dict[str, List[str]]:
        """Build agent hierarchy based on roles"""
        hierarchy = {}
        
        # Find leaders
        leaders = [agent for agent in agents if agent.role == AgentRole.LEADER]
        coordinators = [agent for agent in agents if agent.role == AgentRole.COORDINATOR]
        specialists = [agent for agent in agents if agent.role == AgentRole.SPECIALIST]
        executors = [agent for agent in agents if agent.role == AgentRole.EXECUTOR]
        monitors = [agent for agent in agents if agent.role == AgentRole.MONITOR]
        
        # Build hierarchy
        for leader in leaders:
            subordinates = []
            
            # Assign coordinators to leaders
            if coordinators:
                subordinates.extend([coord.id for coord in coordinators])
                
                # Assign specialists and executors to coordinators
                for coordinator in coordinators:
                    coord_subordinates = []
                    if specialists:
                        coord_subordinates.extend([spec.id for spec in specialists[:2]])
                        specialists = specialists[2:]
                    if executors:
                        coord_subordinates.extend([exec.id for exec in executors[:3]])
                        executors = executors[3:]
                    hierarchy[coordinator.id] = coord_subordinates
            else:
                # Direct assignment to leader
                subordinates.extend([spec.id for spec in specialists])
                subordinates.extend([exec.id for exec in executors])
            
            # Monitors report to everyone
            subordinates.extend([mon.id for mon in monitors])
            hierarchy[leader.id] = subordinates
        
        return hierarchy
    
    async def assign_task(
        self,
        formation_id: str,
        task_name: str,
        task_description: str,
        priority: TaskPriority,
        required_capabilities: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Assign a task to a formation
        
        Args:
            formation_id: Target formation ID
            task_name: Task name
            task_description: Task description
            priority: Task priority level
            required_capabilities: Required agent capabilities
            metadata: Additional task metadata
            
        Returns:
            Task ID
        """
        if formation_id not in self.formations:
            raise ValueError(f"Formation {formation_id} not found")
        
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            name=task_name,
            description=task_description,
            priority=priority,
            required_capabilities=required_capabilities,
            metadata=metadata or {}
        )
        
        formation = self.formations[formation_id]
        formation.tasks.append(task)
        self.task_queue.append(task)
        
        # Auto-assign agents based on capabilities
        await self._auto_assign_agents(formation_id, task_id)
        
        logger.info(f"Assigned task '{task_name}' to formation '{formation.name}'")
        return task_id
    
    async def _auto_assign_agents(self, formation_id: str, task_id: str):
        """Automatically assign agents to a task based on capabilities"""
        formation = self.formations[formation_id]
        task = next((t for t in formation.tasks if t.id == task_id), None)
        
        if not task:
            return
        
        # Find suitable agents
        suitable_agents = []
        for agent in formation.agents:
            if agent.status == "available":
                # Check capability match
                capability_match = any(
                    cap in agent.capabilities 
                    for cap in task.required_capabilities
                )
                if capability_match:
                    suitable_agents.append((agent, self._calculate_agent_score(agent, task)))
        
        # Sort by score and assign best agents
        suitable_agents.sort(key=lambda x: x[1], reverse=True)
        
        # Assign agents based on task complexity
        num_agents_needed = min(len(suitable_agents), self._calculate_agents_needed(task))
        
        for i in range(num_agents_needed):
            agent = suitable_agents[i][0]
            task.assigned_agents.append(agent.id)
            agent.current_task = task_id
            agent.status = "assigned"
        
        logger.info(f"Assigned {len(task.assigned_agents)} agents to task '{task.name}'")
    
    def _calculate_agent_score(self, agent: Agent, task: Task) -> float:
        """Calculate agent suitability score for a task"""
        score = agent.performance_score
        
        # Capability match bonus
        capability_matches = sum(
            1 for cap in task.required_capabilities 
            if cap in agent.capabilities
        )
        score += capability_matches * 0.2
        
        # Role bonus
        if task.priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]:
            if agent.role in [AgentRole.LEADER, AgentRole.SPECIALIST]:
                score += 0.3
        
        # Availability bonus
        if agent.status == "available":
            score += 0.1
        
        return score
    
    def _calculate_agents_needed(self, task: Task) -> int:
        """Calculate number of agents needed for a task"""
        base_agents = 1
        
        # Priority-based scaling
        if task.priority == TaskPriority.CRITICAL:
            base_agents = 3
        elif task.priority == TaskPriority.HIGH:
            base_agents = 2
        
        # Capability complexity scaling
        if len(task.required_capabilities) > 3:
            base_agents += 1
        
        return min(base_agents, 5)  # Max 5 agents per task
    
    async def start_task_execution(self, formation_id: str, task_id: str) -> bool:
        """
        Start task execution in a formation
        
        Args:
            formation_id: Formation ID
            task_id: Task ID
            
        Returns:
            Success status
        """
        formation = self.formations.get(formation_id)
        if not formation:
            return False
        
        task = next((t for t in formation.tasks if t.id == task_id), None)
        if not task or not task.assigned_agents:
            return False
        
        # Update task status
        task.status = "in_progress"
        task.started_at = datetime.now()
        self.active_tasks[task_id] = task
        
        # Update agent statuses
        for agent_id in task.assigned_agents:
            if agent_id in self.agent_registry:
                self.agent_registry[agent_id].status = "active"
        
        # Start coordination protocol
        await self._initiate_coordination(formation_id, task_id)
        
        logger.info(f"Started execution of task '{task.name}' in formation '{formation.name}'")
        return True
    
    async def _initiate_coordination(self, formation_id: str, task_id: str):
        """Initiate coordination protocol for task execution"""
        formation = self.formations[formation_id]
        protocol = self.coordination_protocols.get(formation.coordination_protocol, {})
        
        # Implement coordination logic based on protocol
        if formation.coordination_protocol == "hierarchical":
            await self._hierarchical_coordination(formation_id, task_id)
        elif formation.coordination_protocol == "collaborative":
            await self._collaborative_coordination(formation_id, task_id)
        elif formation.coordination_protocol == "specialized":
            await self._specialized_coordination(formation_id, task_id)
    
    async def _hierarchical_coordination(self, formation_id: str, task_id: str):
        """Implement hierarchical coordination protocol"""
        formation = self.formations[formation_id]
        task = self.active_tasks[task_id]
        
        # Find task leader
        leaders = [
            agent for agent in formation.agents 
            if agent.role == AgentRole.LEADER and agent.id in task.assigned_agents
        ]
        
        if leaders:
            leader = leaders[0]
            logger.info(f"Hierarchical coordination initiated by {leader.name}")
            
            # Leader coordinates subordinates
            subordinates = formation.hierarchy.get(leader.id, [])
            assigned_subordinates = [
                agent_id for agent_id in subordinates 
                if agent_id in task.assigned_agents
            ]
            
            # Delegate subtasks to subordinates
            for subordinate_id in assigned_subordinates:
                await self._delegate_subtask(leader.id, subordinate_id, task_id)
    
    async def _collaborative_coordination(self, formation_id: str, task_id: str):
        """Implement collaborative coordination protocol"""
        formation = self.formations[formation_id]
        task = self.active_tasks[task_id]
        
        logger.info(f"Collaborative coordination initiated for task '{task.name}'")
        
        # All agents participate in planning
        assigned_agents = [
            self.agent_registry[agent_id] 
            for agent_id in task.assigned_agents
        ]
        
        # Simulate collaborative planning
        for agent in assigned_agents:
            await self._agent_contribute_to_plan(agent.id, task_id)
    
    async def _specialized_coordination(self, formation_id: str, task_id: str):
        """Implement specialized coordination protocol"""
        formation = self.formations[formation_id]
        task = self.active_tasks[task_id]
        
        logger.info(f"Specialized coordination initiated for task '{task.name}'")
        
        # Find specialists for each required capability
        for capability in task.required_capabilities:
            specialists = [
                agent for agent in formation.agents
                if capability in agent.capabilities and agent.id in task.assigned_agents
            ]
            
            if specialists:
                specialist = specialists[0]  # Use best specialist
                await self._assign_capability_leadership(specialist.id, capability, task_id)
    
    async def _delegate_subtask(self, leader_id: str, subordinate_id: str, task_id: str):
        """Delegate subtask from leader to subordinate"""
        logger.info(f"Delegating subtask from {leader_id} to {subordinate_id}")
        # Implementation would include actual task delegation logic
        pass
    
    async def _agent_contribute_to_plan(self, agent_id: str, task_id: str):
        """Agent contributes to collaborative planning"""
        logger.info(f"Agent {agent_id} contributing to plan for task {task_id}")
        # Implementation would include planning contribution logic
        pass
    
    async def _assign_capability_leadership(self, specialist_id: str, capability: str, task_id: str):
        """Assign capability leadership to specialist"""
        logger.info(f"Assigning {capability} leadership to specialist {specialist_id}")
        # Implementation would include capability leadership logic
        pass
    
    async def monitor_formation_performance(self, formation_id: str) -> Dict[str, Any]:
        """
        Monitor formation performance metrics
        
        Args:
            formation_id: Formation ID
            
        Returns:
            Performance metrics
        """
        formation = self.formations.get(formation_id)
        if not formation:
            return {}
        
        metrics = {
            "formation_id": formation_id,
            "formation_name": formation.name,
            "total_agents": len(formation.agents),
            "active_agents": len([a for a in formation.agents if a.status == "active"]),
            "total_tasks": len(formation.tasks),
            "active_tasks": len([t for t in formation.tasks if t.status == "in_progress"]),
            "completed_tasks": len([t for t in formation.tasks if t.status == "completed"]),
            "average_agent_performance": sum(a.performance_score for a in formation.agents) / len(formation.agents),
            "task_completion_rate": 0.0,
            "coordination_efficiency": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Calculate task completion rate
        if formation.tasks:
            completed_tasks = len([t for t in formation.tasks if t.status == "completed"])
            metrics["task_completion_rate"] = completed_tasks / len(formation.tasks)
        
        # Calculate coordination efficiency (simplified)
        active_tasks = [t for t in formation.tasks if t.status == "in_progress"]
        if active_tasks:
            avg_progress = sum(t.progress for t in active_tasks) / len(active_tasks)
            metrics["coordination_efficiency"] = avg_progress
        
        return metrics
    
    async def update_task_progress(self, task_id: str, progress: float, status: Optional[str] = None):
        """
        Update task progress
        
        Args:
            task_id: Task ID
            progress: Progress percentage (0.0 to 1.0)
            status: Optional status update
        """
        task = self.active_tasks.get(task_id)
        if not task:
            return
        
        task.progress = max(0.0, min(1.0, progress))
        
        if status:
            task.status = status
        
        # Auto-complete if progress reaches 100%
        if task.progress >= 1.0 and task.status != "completed":
            task.status = "completed"
            task.completed_at = datetime.now()
            
            # Free up assigned agents
            for agent_id in task.assigned_agents:
                if agent_id in self.agent_registry:
                    agent = self.agent_registry[agent_id]
                    agent.status = "available"
                    agent.current_task = None
            
            # Remove from active tasks
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            
            logger.info(f"Task '{task.name}' completed successfully")
    
    def get_formation_status(self, formation_id: str) -> Dict[str, Any]:
        """
        Get formation status
        
        Args:
            formation_id: Formation ID
            
        Returns:
            Formation status information
        """
        formation = self.formations.get(formation_id)
        if not formation:
            return {}
        
        return {
            "id": formation.id,
            "name": formation.name,
            "mode": formation.mode.value,
            "status": formation.status,
            "agent_count": len(formation.agents),
            "task_count": len(formation.tasks),
            "coordination_protocol": formation.coordination_protocol,
            "created_at": formation.created_at.isoformat(),
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "role": agent.role.value,
                    "status": agent.status,
                    "current_task": agent.current_task,
                    "performance_score": agent.performance_score
                }
                for agent in formation.agents
            ],
            "tasks": [
                {
                    "id": task.id,
                    "name": task.name,
                    "status": task.status,
                    "priority": task.priority.value,
                    "progress": task.progress,
                    "assigned_agents": len(task.assigned_agents)
                }
                for task in formation.tasks
            ]
        }
    
    async def shutdown_formation(self, formation_id: str) -> bool:
        """
        Shutdown a formation
        
        Args:
            formation_id: Formation ID
            
        Returns:
            Success status
        """
        formation = self.formations.get(formation_id)
        if not formation:
            return False
        
        # Complete or cancel active tasks
        active_formation_tasks = [
            task for task in self.active_tasks.values()
            if any(agent_id in [a.id for a in formation.agents] for agent_id in task.assigned_agents)
        ]
        
        for task in active_formation_tasks:
            task.status = "cancelled"
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
        
        # Free up agents
        for agent in formation.agents:
            agent.status = "available"
            agent.current_task = None
        
        # Mark formation as inactive
        formation.status = "inactive"
        
        logger.info(f"Formation '{formation.name}' shutdown successfully")
        return True

# Example usage and testing
async def main():
    """Example usage of the Formation Controller"""
    controller = FormationController()
    
    # Create a formation
    agents = [
        {
            "name": "Alpha Leader",
            "role": "leader",
            "capabilities": ["leadership", "coordination", "strategic_planning"]
        },
        {
            "name": "Beta Specialist",
            "role": "specialist",
            "capabilities": ["data_analysis", "machine_learning", "research"]
        },
        {
            "name": "Gamma Executor",
            "role": "executor",
            "capabilities": ["implementation", "testing", "deployment"]
        },
        {
            "name": "Delta Monitor",
            "role": "monitor",
            "capabilities": ["monitoring", "reporting", "quality_assurance"]
        }
    ]
    
    formation_id = await controller.create_formation(
        name="Alpha Squad",
        mode=FormationMode.MANUAL,
        agents=agents,
        coordination_protocol="hierarchical"
    )
    
    # Assign a task
    task_id = await controller.assign_task(
        formation_id=formation_id,
        task_name="Data Analysis Project",
        task_description="Analyze customer data and generate insights",
        priority=TaskPriority.HIGH,
        required_capabilities=["data_analysis", "research"]
    )
    
    # Start task execution
    await controller.start_task_execution(formation_id, task_id)
    
    # Monitor performance
    metrics = await controller.monitor_formation_performance(formation_id)
    print(f"Formation Metrics: {json.dumps(metrics, indent=2)}")
    
    # Update task progress
    await controller.update_task_progress(task_id, 0.5, "in_progress")
    await controller.update_task_progress(task_id, 1.0, "completed")
    
    # Get formation status
    status = controller.get_formation_status(formation_id)
    print(f"Formation Status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())