#!/usr/bin/env python3
"""
A.C.I.D. Swarm Orchestrator
Autonomous Cognitive Intelligence Directorate - Swarm Mode

This module implements the Swarm Mode orchestrator for A.C.I.D., providing
autonomous task execution with emergent coordination and dynamic optimization
for the JAEGIS A.E.G.I.S. Protocol Suite.

Swarm Mode Features:
- Autonomous agent squad assembly
- Emergent coordination patterns
- Dynamic optimization algorithms
- Self-organizing task distribution
- Adaptive resource allocation
"""

import asyncio
import json
import logging
import time
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import uuid
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SwarmBehavior(Enum):
    """Swarm behavior patterns"""
    EXPLORATION = "exploration"
    EXPLOITATION = "exploitation"
    COORDINATION = "coordination"
    OPTIMIZATION = "optimization"
    ADAPTATION = "adaptation"

class AgentState(Enum):
    """Agent states in swarm"""
    IDLE = "idle"
    EXPLORING = "exploring"
    WORKING = "working"
    COORDINATING = "coordinating"
    OPTIMIZING = "optimizing"

class TaskComplexity(Enum):
    """Task complexity levels"""
    SIMPLE = 1
    MODERATE = 2
    COMPLEX = 3
    HIGHLY_COMPLEX = 4
    EXTREME = 5

@dataclass
class SwarmAgent:
    """Swarm agent with autonomous capabilities"""
    id: str
    name: str
    capabilities: List[str]
    state: AgentState = AgentState.IDLE
    position: Tuple[float, float] = (0.0, 0.0)  # Virtual position in task space
    velocity: Tuple[float, float] = (0.0, 0.0)  # Movement vector
    energy: float = 1.0  # Agent energy level
    experience: Dict[str, float] = field(default_factory=dict)  # Task experience
    connections: Set[str] = field(default_factory=set)  # Connected agents
    current_task: Optional[str] = None
    performance_history: List[float] = field(default_factory=list)
    last_active: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SwarmTask:
    """Task in swarm environment"""
    id: str
    name: str
    description: str
    complexity: TaskComplexity
    required_capabilities: List[str]
    position: Tuple[float, float] = (0.0, 0.0)  # Position in task space
    attractiveness: float = 1.0  # Task attractiveness to agents
    urgency: float = 0.5  # Task urgency (0.0 to 1.0)
    assigned_agents: Set[str] = field(default_factory=set)
    progress: float = 0.0
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SwarmMetrics:
    """Swarm performance metrics"""
    total_agents: int
    active_agents: int
    total_tasks: int
    completed_tasks: int
    average_efficiency: float
    coordination_index: float
    adaptation_rate: float
    energy_distribution: List[float]
    task_completion_rate: float
    timestamp: datetime = field(default_factory=datetime.now)

class SwarmOrchestrator:
    """
    A.C.I.D. Swarm Orchestrator
    
    Manages autonomous agent swarms with emergent coordination,
    self-organization, and dynamic optimization capabilities.
    """
    
    def __init__(self, task_space_size: Tuple[float, float] = (100.0, 100.0)):
        self.agents: Dict[str, SwarmAgent] = {}
        self.tasks: Dict[str, SwarmTask] = {}
        self.task_space_size = task_space_size
        self.swarm_behavior = SwarmBehavior.EXPLORATION
        self.coordination_radius = 10.0
        self.optimization_cycles = 0
        self.performance_history: List[float] = []
        self.adaptation_parameters = {
            "learning_rate": 0.1,
            "exploration_factor": 0.3,
            "coordination_strength": 0.5,
            "energy_decay_rate": 0.01,
            "task_attraction_factor": 2.0
        }
        
        # Swarm intelligence parameters
        self.pheromone_trails: Dict[str, float] = {}
        self.global_best_solution: Optional[Dict[str, Any]] = None
        self.local_best_solutions: Dict[str, Dict[str, Any]] = {}
        
        logger.info("A.C.I.D. Swarm Orchestrator initialized")
    
    async def add_agent(
        self,
        name: str,
        capabilities: List[str],
        position: Optional[Tuple[float, float]] = None
    ) -> str:
        """
        Add an agent to the swarm
        
        Args:
            name: Agent name
            capabilities: Agent capabilities
            position: Initial position in task space
            
        Returns:
            Agent ID
        """
        agent_id = str(uuid.uuid4())
        
        # Random position if not specified
        if position is None:
            position = (
                random.uniform(0, self.task_space_size[0]),
                random.uniform(0, self.task_space_size[1])
            )
        
        agent = SwarmAgent(
            id=agent_id,
            name=name,
            capabilities=capabilities,
            position=position
        )
        
        self.agents[agent_id] = agent
        
        logger.info(f"Added agent '{name}' to swarm at position {position}")
        return agent_id
    
    async def add_task(
        self,
        name: str,
        description: str,
        complexity: TaskComplexity,
        required_capabilities: List[str],
        urgency: float = 0.5,
        deadline: Optional[datetime] = None,
        position: Optional[Tuple[float, float]] = None
    ) -> str:
        """
        Add a task to the swarm environment
        
        Args:
            name: Task name
            description: Task description
            complexity: Task complexity level
            required_capabilities: Required capabilities
            urgency: Task urgency (0.0 to 1.0)
            deadline: Task deadline
            position: Position in task space
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        # Random position if not specified
        if position is None:
            position = (
                random.uniform(0, self.task_space_size[0]),
                random.uniform(0, self.task_space_size[1])
            )
        
        # Calculate attractiveness based on urgency and complexity
        attractiveness = urgency * (1.0 + complexity.value * 0.2)
        
        task = SwarmTask(
            id=task_id,
            name=name,
            description=description,
            complexity=complexity,
            required_capabilities=required_capabilities,
            position=position,
            attractiveness=attractiveness,
            urgency=urgency,
            deadline=deadline
        )
        
        self.tasks[task_id] = task
        
        logger.info(f"Added task '{name}' to swarm at position {position}")
        return task_id
    
    async def start_swarm_execution(self):
        """Start autonomous swarm execution"""
        logger.info("Starting autonomous swarm execution")
        
        # Main swarm execution loop
        while True:
            try:
                # Update swarm behavior
                await self._update_swarm_behavior()
                
                # Execute swarm cycle
                await self._execute_swarm_cycle()
                
                # Update metrics
                await self._update_metrics()
                
                # Adaptation and learning
                await self._adapt_parameters()
                
                # Sleep for next cycle
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logger.error(f"Error in swarm execution: {e}")
                await asyncio.sleep(5.0)
    
    async def _update_swarm_behavior(self):
        """Update overall swarm behavior based on current state"""
        active_agents = len([a for a in self.agents.values() if a.state != AgentState.IDLE])
        pending_tasks = len([t for t in self.tasks.values() if t.status == "pending"])
        
        # Determine behavior based on swarm state
        if pending_tasks > active_agents * 2:
            self.swarm_behavior = SwarmBehavior.EXPLORATION
        elif pending_tasks < active_agents * 0.5:
            self.swarm_behavior = SwarmBehavior.OPTIMIZATION
        else:
            self.swarm_behavior = SwarmBehavior.COORDINATION
    
    async def _execute_swarm_cycle(self):
        """Execute one cycle of swarm behavior"""
        # Update all agents
        for agent in self.agents.values():
            await self._update_agent(agent)
        
        # Update all tasks
        for task in self.tasks.values():
            await self._update_task(task)
        
        # Emergent coordination
        await self._emergent_coordination()
        
        # Dynamic optimization
        await self._dynamic_optimization()
    
    async def _update_agent(self, agent: SwarmAgent):
        """Update individual agent state and behavior"""
        # Decay energy
        agent.energy = max(0.0, agent.energy - self.adaptation_parameters["energy_decay_rate"])
        
        # Update agent based on current state
        if agent.state == AgentState.IDLE:
            await self._agent_explore(agent)
        elif agent.state == AgentState.EXPLORING:
            await self._agent_search_tasks(agent)
        elif agent.state == AgentState.WORKING:
            await self._agent_work_on_task(agent)
        elif agent.state == AgentState.COORDINATING:
            await self._agent_coordinate(agent)
        elif agent.state == AgentState.OPTIMIZING:
            await self._agent_optimize(agent)
        
        # Update position based on velocity
        new_x = agent.position[0] + agent.velocity[0]
        new_y = agent.position[1] + agent.velocity[1]
        
        # Boundary conditions
        new_x = max(0, min(self.task_space_size[0], new_x))
        new_y = max(0, min(self.task_space_size[1], new_y))
        
        agent.position = (new_x, new_y)
        
        # Damping
        agent.velocity = (agent.velocity[0] * 0.9, agent.velocity[1] * 0.9)
    
    async def _agent_explore(self, agent: SwarmAgent):
        """Agent explores the task space"""
        # Random movement for exploration
        if random.random() < self.adaptation_parameters["exploration_factor"]:
            direction = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2.0)
            
            agent.velocity = (
                speed * math.cos(direction),
                speed * math.sin(direction)
            )
            
            agent.state = AgentState.EXPLORING
    
    async def _agent_search_tasks(self, agent: SwarmAgent):
        """Agent searches for suitable tasks"""
        suitable_tasks = []
        
        for task in self.tasks.values():
            if task.status == "pending":
                # Check capability match
                capability_match = any(
                    cap in agent.capabilities 
                    for cap in task.required_capabilities
                )
                
                if capability_match:
                    # Calculate distance to task
                    distance = self._calculate_distance(agent.position, task.position)
                    
                    # Calculate task attractiveness
                    attractiveness = task.attractiveness / (1.0 + distance * 0.1)
                    
                    suitable_tasks.append((task, attractiveness, distance))
        
        if suitable_tasks:
            # Sort by attractiveness
            suitable_tasks.sort(key=lambda x: x[1], reverse=True)
            
            # Move towards most attractive task
            best_task = suitable_tasks[0][0]
            await self._move_towards_task(agent, best_task)
            
            # Check if close enough to start working
            distance = self._calculate_distance(agent.position, best_task.position)
            if distance < 2.0:  # Close enough to start working
                await self._assign_agent_to_task(agent, best_task)
        else:
            # No suitable tasks, continue exploring
            agent.state = AgentState.IDLE
    
    async def _agent_work_on_task(self, agent: SwarmAgent):
        """Agent works on assigned task"""
        if not agent.current_task:
            agent.state = AgentState.IDLE
            return
        
        task = self.tasks.get(agent.current_task)
        if not task or task.status == "completed":
            agent.current_task = None
            agent.state = AgentState.IDLE
            return
        
        # Work on task (simulate progress)
        progress_increment = self._calculate_work_progress(agent, task)
        task.progress = min(1.0, task.progress + progress_increment)
        
        # Update agent experience
        for capability in task.required_capabilities:
            if capability in agent.capabilities:
                current_exp = agent.experience.get(capability, 0.0)
                agent.experience[capability] = current_exp + 0.01
        
        # Check if task is completed
        if task.progress >= 1.0:
            await self._complete_task(task, agent)
    
    async def _agent_coordinate(self, agent: SwarmAgent):
        """Agent coordinates with nearby agents"""
        nearby_agents = self._find_nearby_agents(agent, self.coordination_radius)
        
        for nearby_agent in nearby_agents:
            # Share information
            await self._share_information(agent, nearby_agent)
            
            # Coordinate task assignments
            await self._coordinate_task_assignment(agent, nearby_agent)
        
        # Return to previous state after coordination
        agent.state = AgentState.WORKING if agent.current_task else AgentState.EXPLORING
    
    async def _agent_optimize(self, agent: SwarmAgent):
        """Agent performs optimization behaviors"""
        # Optimize current task assignment
        if agent.current_task:
            task = self.tasks.get(agent.current_task)
            if task:
                # Check if there's a better agent for this task
                better_agent = await self._find_better_agent_for_task(task, agent)
                if better_agent:
                    await self._reassign_task(task, agent, better_agent)
        
        # Look for optimization opportunities
        await self._optimize_local_area(agent)
        
        agent.state = AgentState.WORKING if agent.current_task else AgentState.EXPLORING
    
    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two positions"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    async def _move_towards_task(self, agent: SwarmAgent, task: SwarmTask):
        """Move agent towards a task"""
        direction_x = task.position[0] - agent.position[0]
        direction_y = task.position[1] - agent.position[1]
        
        distance = math.sqrt(direction_x**2 + direction_y**2)
        
        if distance > 0:
            # Normalize direction and apply speed
            speed = min(2.0, distance * 0.1)
            agent.velocity = (
                (direction_x / distance) * speed,
                (direction_y / distance) * speed
            )
    
    async def _assign_agent_to_task(self, agent: SwarmAgent, task: SwarmTask):
        """Assign agent to a task"""
        agent.current_task = task.id
        agent.state = AgentState.WORKING
        task.assigned_agents.add(agent.id)
        task.status = "in_progress"
        
        logger.info(f"Assigned agent '{agent.name}' to task '{task.name}'")
    
    def _calculate_work_progress(self, agent: SwarmAgent, task: SwarmTask) -> float:
        """Calculate work progress based on agent capabilities and task complexity"""
        base_progress = 0.01  # Base progress per cycle
        
        # Capability bonus
        capability_matches = sum(
            1 for cap in task.required_capabilities 
            if cap in agent.capabilities
        )
        capability_bonus = capability_matches * 0.005
        
        # Experience bonus
        experience_bonus = 0.0
        for capability in task.required_capabilities:
            if capability in agent.experience:
                experience_bonus += agent.experience[capability] * 0.001
        
        # Energy factor
        energy_factor = agent.energy
        
        # Complexity penalty
        complexity_penalty = task.complexity.value * 0.002
        
        total_progress = (base_progress + capability_bonus + experience_bonus) * energy_factor - complexity_penalty
        
        return max(0.001, total_progress)  # Minimum progress
    
    async def _complete_task(self, task: SwarmTask, agent: SwarmAgent):
        """Complete a task"""
        task.status = "completed"
        
        # Update agent performance
        performance_score = 1.0 + (1.0 - task.urgency) * 0.2  # Bonus for completing urgent tasks
        agent.performance_history.append(performance_score)
        
        # Keep only recent performance history
        if len(agent.performance_history) > 10:
            agent.performance_history = agent.performance_history[-10:]
        
        # Free up agent
        agent.current_task = None
        agent.state = AgentState.IDLE
        agent.energy = min(1.0, agent.energy + 0.1)  # Restore some energy
        
        logger.info(f"Task '{task.name}' completed by agent '{agent.name}'")
    
    def _find_nearby_agents(self, agent: SwarmAgent, radius: float) -> List[SwarmAgent]:
        """Find agents within coordination radius"""
        nearby_agents = []
        
        for other_agent in self.agents.values():
            if other_agent.id != agent.id:
                distance = self._calculate_distance(agent.position, other_agent.position)
                if distance <= radius:
                    nearby_agents.append(other_agent)
        
        return nearby_agents
    
    async def _share_information(self, agent1: SwarmAgent, agent2: SwarmAgent):
        """Share information between agents"""
        # Add connection
        agent1.connections.add(agent2.id)
        agent2.connections.add(agent1.id)
        
        # Share experience (simplified)
        for capability in agent1.experience:
            if capability in agent2.experience:
                avg_exp = (agent1.experience[capability] + agent2.experience[capability]) / 2
                agent1.experience[capability] = avg_exp * 1.01  # Slight learning bonus
                agent2.experience[capability] = avg_exp * 1.01
    
    async def _coordinate_task_assignment(self, agent1: SwarmAgent, agent2: SwarmAgent):
        """Coordinate task assignments between agents"""
        # Check if agents can collaborate on tasks
        if agent1.current_task and not agent2.current_task:
            task = self.tasks.get(agent1.current_task)
            if task and task.complexity.value >= 3:  # Complex tasks benefit from collaboration
                # Check if agent2 can help
                can_help = any(cap in agent2.capabilities for cap in task.required_capabilities)
                if can_help:
                    await self._assign_agent_to_task(agent2, task)
    
    async def _find_better_agent_for_task(self, task: SwarmTask, current_agent: SwarmAgent) -> Optional[SwarmAgent]:
        """Find a better agent for a task"""
        best_agent = None
        best_score = self._calculate_agent_task_score(current_agent, task)
        
        for agent in self.agents.values():
            if agent.id != current_agent.id and not agent.current_task:
                score = self._calculate_agent_task_score(agent, task)
                if score > best_score * 1.2:  # Significant improvement required
                    best_score = score
                    best_agent = agent
        
        return best_agent
    
    def _calculate_agent_task_score(self, agent: SwarmAgent, task: SwarmTask) -> float:
        """Calculate agent suitability score for a task"""
        score = 0.0
        
        # Capability match
        capability_matches = sum(
            1 for cap in task.required_capabilities 
            if cap in agent.capabilities
        )
        score += capability_matches * 2.0
        
        # Experience bonus
        for capability in task.required_capabilities:
            if capability in agent.experience:
                score += agent.experience[capability]
        
        # Energy factor
        score *= agent.energy
        
        # Distance penalty
        distance = self._calculate_distance(agent.position, task.position)
        score -= distance * 0.01
        
        return score
    
    async def _reassign_task(self, task: SwarmTask, old_agent: SwarmAgent, new_agent: SwarmAgent):
        """Reassign task from one agent to another"""
        # Remove from old agent
        old_agent.current_task = None
        old_agent.state = AgentState.IDLE
        task.assigned_agents.discard(old_agent.id)
        
        # Assign to new agent
        await self._assign_agent_to_task(new_agent, task)
        
        logger.info(f"Reassigned task '{task.name}' from '{old_agent.name}' to '{new_agent.name}'")
    
    async def _optimize_local_area(self, agent: SwarmAgent):
        """Optimize task assignments in local area"""
        nearby_tasks = []
        
        for task in self.tasks.values():
            if task.status in ["pending", "in_progress"]:
                distance = self._calculate_distance(agent.position, task.position)
                if distance <= self.coordination_radius:
                    nearby_tasks.append(task)
        
        # Look for optimization opportunities
        for task in nearby_tasks:
            if len(task.assigned_agents) > 1:
                # Check if task can be completed with fewer agents
                await self._optimize_task_assignment(task)
    
    async def _optimize_task_assignment(self, task: SwarmTask):
        """Optimize agent assignment for a specific task"""
        if len(task.assigned_agents) <= 1:
            return
        
        # Calculate if task can be completed with fewer agents
        assigned_agents = [self.agents[agent_id] for agent_id in task.assigned_agents]
        
        # Sort agents by suitability
        agent_scores = [
            (agent, self._calculate_agent_task_score(agent, task))
            for agent in assigned_agents
        ]
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Keep only the best agents needed
        optimal_agent_count = min(len(agent_scores), task.complexity.value)
        
        # Remove excess agents
        for i in range(optimal_agent_count, len(agent_scores)):
            agent = agent_scores[i][0]
            agent.current_task = None
            agent.state = AgentState.IDLE
            task.assigned_agents.discard(agent.id)
    
    async def _emergent_coordination(self):
        """Implement emergent coordination patterns"""
        # Update pheromone trails
        await self._update_pheromone_trails()
        
        # Detect coordination patterns
        await self._detect_coordination_patterns()
        
        # Facilitate emergent behaviors
        await self._facilitate_emergent_behaviors()
    
    async def _update_pheromone_trails(self):
        """Update pheromone trails for task coordination"""
        # Decay existing pheromones
        for key in list(self.pheromone_trails.keys()):
            self.pheromone_trails[key] *= 0.95
            if self.pheromone_trails[key] < 0.01:
                del self.pheromone_trails[key]
        
        # Add new pheromones based on successful task completions
        for task in self.tasks.values():
            if task.status == "completed":
                for agent_id in task.assigned_agents:
                    trail_key = f"{agent_id}_{task.id}"
                    self.pheromone_trails[trail_key] = 1.0
    
    async def _detect_coordination_patterns(self):
        """Detect emerging coordination patterns"""
        # Analyze agent connections
        connection_patterns = {}
        for agent in self.agents.values():
            pattern_key = tuple(sorted(agent.connections))
            if pattern_key in connection_patterns:
                connection_patterns[pattern_key] += 1
            else:
                connection_patterns[pattern_key] = 1
        
        # Identify dominant patterns
        if connection_patterns:
            dominant_pattern = max(connection_patterns.items(), key=lambda x: x[1])
            logger.debug(f"Dominant coordination pattern: {dominant_pattern}")
    
    async def _facilitate_emergent_behaviors(self):
        """Facilitate emergent swarm behaviors"""
        # Encourage coordination for complex tasks
        complex_tasks = [
            task for task in self.tasks.values()
            if task.complexity.value >= 3 and task.status == "pending"
        ]
        
        for task in complex_tasks:
            nearby_agents = []
            for agent in self.agents.values():
                if agent.state in [AgentState.IDLE, AgentState.EXPLORING]:
                    distance = self._calculate_distance(agent.position, task.position)
                    if distance <= self.coordination_radius * 2:
                        nearby_agents.append(agent)
            
            # Encourage coordination
            if len(nearby_agents) >= 2:
                for agent in nearby_agents[:task.complexity.value]:
                    agent.state = AgentState.COORDINATING
    
    async def _dynamic_optimization(self):
        """Perform dynamic optimization of swarm parameters"""
        self.optimization_cycles += 1
        
        # Calculate current performance
        current_performance = await self._calculate_swarm_performance()
        self.performance_history.append(current_performance)
        
        # Keep only recent history
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-50:]
        
        # Optimize parameters every 10 cycles
        if self.optimization_cycles % 10 == 0:
            await self._optimize_swarm_parameters()
    
    async def _calculate_swarm_performance(self) -> float:
        """Calculate overall swarm performance"""
        if not self.agents:
            return 0.0
        
        # Task completion rate
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == "completed"])
        completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
        
        # Agent efficiency
        active_agents = len([a for a in self.agents.values() if a.state != AgentState.IDLE])
        efficiency = active_agents / len(self.agents) if self.agents else 0.0
        
        # Coordination index
        total_connections = sum(len(a.connections) for a in self.agents.values())
        max_connections = len(self.agents) * (len(self.agents) - 1)
        coordination_index = total_connections / max_connections if max_connections > 0 else 0.0
        
        # Combined performance
        performance = (completion_rate * 0.5 + efficiency * 0.3 + coordination_index * 0.2)
        
        return performance
    
    async def _optimize_swarm_parameters(self):
        """Optimize swarm parameters based on performance"""
        if len(self.performance_history) < 10:
            return
        
        recent_performance = sum(self.performance_history[-10:]) / 10
        
        # Adjust parameters based on performance
        if recent_performance < 0.5:
            # Poor performance - increase exploration
            self.adaptation_parameters["exploration_factor"] = min(0.5, 
                self.adaptation_parameters["exploration_factor"] * 1.1)
            self.coordination_radius = min(20.0, self.coordination_radius * 1.1)
        elif recent_performance > 0.8:
            # Good performance - increase exploitation
            self.adaptation_parameters["exploration_factor"] = max(0.1, 
                self.adaptation_parameters["exploration_factor"] * 0.9)
            self.coordination_radius = max(5.0, self.coordination_radius * 0.9)
    
    async def _adapt_parameters(self):
        """Adapt swarm parameters based on current state"""
        # Adaptive learning rate
        if len(self.performance_history) >= 2:
            performance_trend = self.performance_history[-1] - self.performance_history[-2]
            if performance_trend > 0:
                # Performance improving - maintain current parameters
                pass
            else:
                # Performance declining - adjust parameters
                self.adaptation_parameters["learning_rate"] *= 1.05
                self.adaptation_parameters["coordination_strength"] *= 1.02
    
    async def _update_task(self, task: SwarmTask):
        """Update task state"""
        if task.status == "in_progress":
            # Check if task has assigned agents
            if not task.assigned_agents:
                task.status = "pending"
            
            # Check deadline
            if task.deadline and datetime.now() > task.deadline:
                task.urgency = min(1.0, task.urgency * 1.5)  # Increase urgency
    
    async def _update_metrics(self):
        """Update swarm metrics"""
        # This would update comprehensive metrics
        # Implementation depends on specific monitoring requirements
        pass
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get current swarm status"""
        active_agents = len([a for a in self.agents.values() if a.state != AgentState.IDLE])
        pending_tasks = len([t for t in self.tasks.values() if t.status == "pending"])
        in_progress_tasks = len([t for t in self.tasks.values() if t.status == "in_progress"])
        completed_tasks = len([t for t in self.tasks.values() if t.status == "completed"])
        
        return {
            "total_agents": len(self.agents),
            "active_agents": active_agents,
            "idle_agents": len(self.agents) - active_agents,
            "total_tasks": len(self.tasks),
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "swarm_behavior": self.swarm_behavior.value,
            "coordination_radius": self.coordination_radius,
            "optimization_cycles": self.optimization_cycles,
            "performance_history": self.performance_history[-10:],  # Recent performance
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_swarm_metrics(self) -> SwarmMetrics:
        """Get detailed swarm metrics"""
        total_agents = len(self.agents)
        active_agents = len([a for a in self.agents.values() if a.state != AgentState.IDLE])
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == "completed"])
        
        # Calculate metrics
        task_completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
        average_efficiency = active_agents / total_agents if total_agents > 0 else 0.0
        
        # Coordination index
        total_connections = sum(len(a.connections) for a in self.agents.values())
        max_connections = total_agents * (total_agents - 1)
        coordination_index = total_connections / max_connections if max_connections > 0 else 0.0
        
        # Adaptation rate (based on parameter changes)
        adaptation_rate = self.adaptation_parameters["learning_rate"]
        
        # Energy distribution
        energy_distribution = [agent.energy for agent in self.agents.values()]
        
        return SwarmMetrics(
            total_agents=total_agents,
            active_agents=active_agents,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            average_efficiency=average_efficiency,
            coordination_index=coordination_index,
            adaptation_rate=adaptation_rate,
            energy_distribution=energy_distribution,
            task_completion_rate=task_completion_rate
        )

# Example usage and testing
async def main():
    """Example usage of the Swarm Orchestrator"""
    orchestrator = SwarmOrchestrator()
    
    # Add agents to swarm
    agent_configs = [
        ("Alpha", ["data_analysis", "research"]),
        ("Beta", ["implementation", "testing"]),
        ("Gamma", ["coordination", "monitoring"]),
        ("Delta", ["optimization", "analysis"]),
        ("Epsilon", ["research", "implementation"])
    ]
    
    for name, capabilities in agent_configs:
        await orchestrator.add_agent(name, capabilities)
    
    # Add tasks
    task_configs = [
        ("Data Analysis", "Analyze customer data", TaskComplexity.MODERATE, ["data_analysis"], 0.8),
        ("System Implementation", "Implement new features", TaskComplexity.COMPLEX, ["implementation"], 0.6),
        ("Performance Optimization", "Optimize system performance", TaskComplexity.HIGHLY_COMPLEX, ["optimization"], 0.9),
        ("Research Project", "Conduct market research", TaskComplexity.SIMPLE, ["research"], 0.4)
    ]
    
    for name, description, complexity, capabilities, urgency in task_configs:
        await orchestrator.add_task(name, description, complexity, capabilities, urgency)
    
    # Start swarm execution (would run continuously in practice)
    print("Starting swarm execution...")
    
    # Run for a few cycles for demonstration
    for i in range(10):
        await orchestrator._execute_swarm_cycle()
        status = orchestrator.get_swarm_status()
        print(f"Cycle {i+1}: {status['active_agents']} active agents, "
              f"{status['in_progress_tasks']} tasks in progress")
        await asyncio.sleep(0.1)
    
    # Get final metrics
    metrics = await orchestrator.get_swarm_metrics()
    print(f"Final metrics: {metrics.task_completion_rate:.2f} completion rate, "
          f"{metrics.coordination_index:.2f} coordination index")

if __name__ == "__main__":
    asyncio.run(main())