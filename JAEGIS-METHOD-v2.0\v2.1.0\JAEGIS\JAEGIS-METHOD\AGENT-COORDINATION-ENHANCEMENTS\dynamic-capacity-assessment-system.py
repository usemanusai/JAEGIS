#!/usr/bin/env python3
"""
JAEGIS Agent System - Dynamic Capacity Assessment System
MEDIUM PRIORITY GAP RESOLUTION: Enables real-time agent capacity monitoring and optimal task assignment

Date: 24 July 2025
Priority: MEDIUM - Phase 2 Implementation
Gap ID: 4.1 - Dynamic Agent Capacity and Performance Assessment
Impact: HIGH - Optimizes task assignment and prevents agent bottlenecks
"""

import asyncio
import json
import time
import uuid
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics

class CapacityStatus(Enum):
    """Agent capacity status levels"""
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OVERLOADED = "OVERLOADED"
    UNAVAILABLE = "UNAVAILABLE"
    MAINTENANCE = "MAINTENANCE"

class PerformanceMetric(Enum):
    """Performance metrics for agents"""
    TASK_COMPLETION_RATE = "TASK_COMPLETION_RATE"
    AVERAGE_RESPONSE_TIME = "AVERAGE_RESPONSE_TIME"
    QUALITY_SCORE = "QUALITY_SCORE"
    COLLABORATION_EFFECTIVENESS = "COLLABORATION_EFFECTIVENESS"
    RESOURCE_UTILIZATION = "RESOURCE_UTILIZATION"

@dataclass
class AgentCapacityProfile:
    """Agent capacity and performance profile"""
    agent_id: str
    current_capacity: float  # 0.0 to 1.0
    max_concurrent_tasks: int
    current_tasks: int
    capacity_status: CapacityStatus
    performance_metrics: Dict[str, float]
    availability_schedule: Dict[str, Any]
    last_updated: str
    capacity_trend: List[float] = field(default_factory=list)
    performance_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class TaskAssignmentRecommendation:
    """Task assignment recommendation based on capacity analysis"""
    task_id: str
    recommended_agent: str
    confidence_score: float
    capacity_utilization: float
    expected_completion_time: int
    alternative_agents: List[Tuple[str, float]]
    assignment_rationale: str

class JAEGISDynamicCapacityAssessor:
    """
    JAEGIS Dynamic Capacity Assessment System
    Real-time monitoring and optimization of agent capacity and performance
    """
    
    def __init__(self):
        # Agent capacity tracking
        self.agent_profiles: Dict[str, AgentCapacityProfile] = {}
        self.capacity_history: Dict[str, List[Tuple[str, float]]] = {}
        self.performance_baselines: Dict[str, Dict[str, float]] = {}
        
        # Task assignment optimization
        self.assignment_recommendations: Dict[str, TaskAssignmentRecommendation] = {}
        self.assignment_history: List[Dict[str, Any]] = []
        self.optimization_rules: Dict[str, Any] = {}
        
        # Monitoring and alerting
        self.capacity_alerts: List[Dict[str, Any]] = []
        self.performance_alerts: List[Dict[str, Any]] = []
        self.monitoring_active: bool = True
        
        # System metrics
        self.assessment_metrics = {
            'total_assessments': 0,
            'optimal_assignments': 0,
            'capacity_predictions_accurate': 0,
            'average_utilization': 0.0,
            'bottleneck_prevention_count': 0
        }
        
        # Initialize system
        self._initialize_capacity_assessment()
    
    async def assess_agent_capacity(self, agent_id: str) -> AgentCapacityProfile:
        """
        Assess current capacity and performance of a specific agent
        Real-time capacity monitoring capability
        """
        print(f"📊 ASSESSING AGENT CAPACITY: {agent_id}")
        
        # Get or create agent profile
        if agent_id not in self.agent_profiles:
            self.agent_profiles[agent_id] = self._create_initial_agent_profile(agent_id)
        
        profile = self.agent_profiles[agent_id]
        
        # Update current capacity metrics
        current_metrics = await self._collect_current_metrics(agent_id)
        
        # Calculate current capacity utilization
        capacity_utilization = self._calculate_capacity_utilization(agent_id, current_metrics)
        
        # Determine capacity status
        capacity_status = self._determine_capacity_status(capacity_utilization, current_metrics)
        
        # Update performance metrics
        performance_metrics = await self._update_performance_metrics(agent_id, current_metrics)
        
        # Update profile
        profile.current_capacity = capacity_utilization
        profile.current_tasks = current_metrics.get('active_tasks', 0)
        profile.capacity_status = capacity_status
        profile.performance_metrics = performance_metrics
        profile.last_updated = datetime.now().isoformat()
        
        # Update capacity trend
        profile.capacity_trend.append(capacity_utilization)
        if len(profile.capacity_trend) > 50:  # Keep last 50 measurements
            profile.capacity_trend = profile.capacity_trend[-50:]
        
        # Store in history
        if agent_id not in self.capacity_history:
            self.capacity_history[agent_id] = []
        
        self.capacity_history[agent_id].append((datetime.now().isoformat(), capacity_utilization))
        if len(self.capacity_history[agent_id]) > 1000:  # Keep last 1000 measurements
            self.capacity_history[agent_id] = self.capacity_history[agent_id][-1000:]
        
        # Check for capacity alerts
        await self._check_capacity_alerts(agent_id, profile)
        
        # Update system metrics
        self.assessment_metrics['total_assessments'] += 1
        
        print(f"✅ CAPACITY ASSESSMENT COMPLETE: {agent_id} | Status: {capacity_status.value} | Utilization: {capacity_utilization:.1%}")
        
        return profile
    
    async def recommend_optimal_assignment(self, task_requirements: Dict[str, Any]) -> TaskAssignmentRecommendation:
        """
        Recommend optimal agent assignment based on capacity and performance analysis
        Capacity-aware task assignment capability
        """
        task_id = task_requirements.get('task_id', str(uuid.uuid4()))
        
        print(f"🎯 RECOMMENDING OPTIMAL ASSIGNMENT: {task_id}")
        
        # Assess all relevant agents
        relevant_agents = self._identify_relevant_agents(task_requirements)
        agent_assessments = {}
        
        for agent_id in relevant_agents:
            assessment = await self.assess_agent_capacity(agent_id)
            agent_assessments[agent_id] = assessment
        
        # Calculate assignment scores
        assignment_scores = {}
        for agent_id, assessment in agent_assessments.items():
            score = self._calculate_assignment_score(agent_id, assessment, task_requirements)
            assignment_scores[agent_id] = score
        
        # Find optimal assignment
        if assignment_scores:
            recommended_agent = max(assignment_scores.keys(), key=lambda x: assignment_scores[x]['total_score'])
            best_score = assignment_scores[recommended_agent]
            
            # Create alternative recommendations
            alternatives = []
            for agent_id, score_data in assignment_scores.items():
                if agent_id != recommended_agent:
                    alternatives.append((agent_id, score_data['total_score']))
            
            alternatives.sort(key=lambda x: x[1], reverse=True)
            alternatives = alternatives[:3]  # Top 3 alternatives
            
            # Calculate expected completion time
            agent_profile = agent_assessments[recommended_agent]
            expected_completion = self._estimate_completion_time(
                recommended_agent, agent_profile, task_requirements
            )
            
            # Create recommendation
            recommendation = TaskAssignmentRecommendation(
                task_id=task_id,
                recommended_agent=recommended_agent,
                confidence_score=best_score['confidence'],
                capacity_utilization=agent_profile.current_capacity,
                expected_completion_time=expected_completion,
                alternative_agents=alternatives,
                assignment_rationale=best_score['rationale']
            )
            
            # Store recommendation
            self.assignment_recommendations[task_id] = recommendation
            
            # Update metrics
            if best_score['total_score'] > 0.8:  # High confidence threshold
                self.assessment_metrics['optimal_assignments'] += 1
            
            print(f"✅ OPTIMAL ASSIGNMENT RECOMMENDED: {recommended_agent} | Confidence: {best_score['confidence']:.1%}")
            
            return recommendation
        
        else:
            # No suitable agents found
            print(f"⚠️ NO SUITABLE AGENTS FOUND for task {task_id}")
            return TaskAssignmentRecommendation(
                task_id=task_id,
                recommended_agent="NONE",
                confidence_score=0.0,
                capacity_utilization=0.0,
                expected_completion_time=0,
                alternative_agents=[],
                assignment_rationale="No agents with sufficient capacity or capability"
            )
    
    async def predict_capacity_bottlenecks(self, time_horizon_hours: int = 24) -> List[Dict[str, Any]]:
        """
        Predict potential capacity bottlenecks based on trends and scheduled work
        Predictive capacity planning capability
        """
        print(f"🔮 PREDICTING CAPACITY BOTTLENECKS: {time_horizon_hours}h horizon")
        
        bottleneck_predictions = []
        
        for agent_id, profile in self.agent_profiles.items():
            # Analyze capacity trend
            if len(profile.capacity_trend) >= 5:  # Need minimum data points
                trend_analysis = self._analyze_capacity_trend(profile.capacity_trend)
                
                # Predict future capacity
                predicted_capacity = self._predict_future_capacity(
                    profile, trend_analysis, time_horizon_hours
                )
                
                # Check for potential bottlenecks
                if predicted_capacity > 0.9:  # 90% capacity threshold
                    bottleneck_risk = self._calculate_bottleneck_risk(
                        agent_id, profile, predicted_capacity
                    )
                    
                    bottleneck_prediction = {
                        'agent_id': agent_id,
                        'predicted_capacity': predicted_capacity,
                        'bottleneck_risk': bottleneck_risk,
                        'time_to_bottleneck': self._estimate_time_to_bottleneck(profile, trend_analysis),
                        'mitigation_strategies': self._suggest_mitigation_strategies(agent_id, bottleneck_risk),
                        'prediction_confidence': trend_analysis['confidence']
                    }
                    
                    bottleneck_predictions.append(bottleneck_prediction)
        
        # Sort by risk level
        bottleneck_predictions.sort(key=lambda x: x['bottleneck_risk'], reverse=True)
        
        print(f"✅ BOTTLENECK PREDICTION COMPLETE: {len(bottleneck_predictions)} potential bottlenecks identified")
        
        return bottleneck_predictions
    
    async def optimize_workload_distribution(self) -> Dict[str, Any]:
        """
        Optimize workload distribution across all agents
        Load balancing optimization capability
        """
        print(f"⚖️ OPTIMIZING WORKLOAD DISTRIBUTION")
        
        # Assess all agents
        all_assessments = {}
        for agent_id in self.agent_profiles.keys():
            assessment = await self.assess_agent_capacity(agent_id)
            all_assessments[agent_id] = assessment
        
        # Calculate current distribution metrics
        current_distribution = self._calculate_distribution_metrics(all_assessments)
        
        # Identify optimization opportunities
        optimization_opportunities = self._identify_optimization_opportunities(all_assessments)
        
        # Generate redistribution recommendations
        redistribution_plan = self._create_redistribution_plan(
            all_assessments, optimization_opportunities
        )
        
        # Calculate expected improvements
        expected_improvements = self._calculate_expected_improvements(
            current_distribution, redistribution_plan
        )
        
        optimization_result = {
            'current_distribution': current_distribution,
            'optimization_opportunities': optimization_opportunities,
            'redistribution_plan': redistribution_plan,
            'expected_improvements': expected_improvements,
            'optimization_confidence': self._calculate_optimization_confidence(redistribution_plan)
        }
        
        print(f"✅ WORKLOAD OPTIMIZATION COMPLETE: {len(optimization_opportunities)} opportunities identified")
        
        return optimization_result
    
    def _create_initial_agent_profile(self, agent_id: str) -> AgentCapacityProfile:
        """Create initial capacity profile for an agent"""
        
        # Agent-specific capacity configurations
        agent_configs = {
            'JAEGIS': {'max_tasks': 10, 'base_capacity': 0.3},
            'John': {'max_tasks': 5, 'base_capacity': 0.4},
            'Fred': {'max_tasks': 6, 'base_capacity': 0.4},
            'Tyler': {'max_tasks': 8, 'base_capacity': 0.3},
            'Jane': {'max_tasks': 4, 'base_capacity': 0.5},
            'Alex': {'max_tasks': 6, 'base_capacity': 0.4},
            'James': {'max_tasks': 7, 'base_capacity': 0.4},
            'Dakota': {'max_tasks': 5, 'base_capacity': 0.5},
            'Sage': {'max_tasks': 4, 'base_capacity': 0.6},
            'Sentinel': {'max_tasks': 6, 'base_capacity': 0.4},
            'DocQA': {'max_tasks': 5, 'base_capacity': 0.5}
        }
        
        config = agent_configs.get(agent_id, {'max_tasks': 5, 'base_capacity': 0.4})
        
        return AgentCapacityProfile(
            agent_id=agent_id,
            current_capacity=config['base_capacity'],
            max_concurrent_tasks=config['max_tasks'],
            current_tasks=0,
            capacity_status=CapacityStatus.AVAILABLE,
            performance_metrics={
                'task_completion_rate': 0.85,
                'average_response_time': 300,  # seconds
                'quality_score': 0.9,
                'collaboration_effectiveness': 0.8,
                'resource_utilization': config['base_capacity']
            },
            availability_schedule={
                'timezone': 'UTC',
                'working_hours': {'start': '09:00', 'end': '17:00'},
                'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
            },
            last_updated=datetime.now().isoformat()
        )
    
    async def _collect_current_metrics(self, agent_id: str) -> Dict[str, Any]:
        """Collect current performance metrics for an agent"""
        
        # Simulate metric collection (in real implementation, would integrate with monitoring systems)
        import random
        
        base_metrics = {
            'active_tasks': random.randint(0, 5),
            'response_time': random.uniform(100, 500),
            'recent_completions': random.randint(0, 3),
            'error_rate': random.uniform(0.0, 0.1),
            'collaboration_requests': random.randint(0, 2),
            'resource_usage': random.uniform(0.2, 0.8)
        }
        
        return base_metrics
    
    def _calculate_capacity_utilization(self, agent_id: str, metrics: Dict[str, Any]) -> float:
        """Calculate current capacity utilization"""
        
        profile = self.agent_profiles.get(agent_id)
        if not profile:
            return 0.0
        
        # Calculate utilization based on multiple factors
        task_utilization = metrics['active_tasks'] / profile.max_concurrent_tasks
        resource_utilization = metrics['resource_usage']
        response_time_factor = min(metrics['response_time'] / 300, 1.0)  # Normalize to 300s baseline
        
        # Weighted average
        utilization = (
            task_utilization * 0.4 +
            resource_utilization * 0.4 +
            response_time_factor * 0.2
        )
        
        return min(utilization, 1.0)
    
    def _determine_capacity_status(self, utilization: float, metrics: Dict[str, Any]) -> CapacityStatus:
        """Determine capacity status based on utilization and metrics"""
        
        if utilization >= 0.9:
            return CapacityStatus.OVERLOADED
        elif utilization >= 0.7:
            return CapacityStatus.BUSY
        elif utilization >= 0.1:
            return CapacityStatus.AVAILABLE
        else:
            return CapacityStatus.AVAILABLE
    
    async def _update_performance_metrics(self, agent_id: str, current_metrics: Dict[str, Any]) -> Dict[str, float]:
        """Update performance metrics for an agent"""
        
        profile = self.agent_profiles.get(agent_id)
        if not profile:
            return {}
        
        # Calculate updated metrics
        updated_metrics = {}
        
        # Task completion rate
        if current_metrics['recent_completions'] > 0:
            completion_rate = max(0.0, 1.0 - current_metrics['error_rate'])
            updated_metrics['task_completion_rate'] = (
                profile.performance_metrics.get('task_completion_rate', 0.8) * 0.8 +
                completion_rate * 0.2
            )
        else:
            updated_metrics['task_completion_rate'] = profile.performance_metrics.get('task_completion_rate', 0.8)
        
        # Average response time
        updated_metrics['average_response_time'] = (
            profile.performance_metrics.get('average_response_time', 300) * 0.8 +
            current_metrics['response_time'] * 0.2
        )
        
        # Quality score (inverse of error rate)
        quality_score = max(0.0, 1.0 - current_metrics['error_rate'])
        updated_metrics['quality_score'] = (
            profile.performance_metrics.get('quality_score', 0.9) * 0.8 +
            quality_score * 0.2
        )
        
        # Collaboration effectiveness
        collab_factor = min(current_metrics['collaboration_requests'] / 5.0, 1.0)
        updated_metrics['collaboration_effectiveness'] = (
            profile.performance_metrics.get('collaboration_effectiveness', 0.8) * 0.8 +
            collab_factor * 0.2
        )
        
        # Resource utilization
        updated_metrics['resource_utilization'] = current_metrics['resource_usage']
        
        return updated_metrics
    
    async def _check_capacity_alerts(self, agent_id: str, profile: AgentCapacityProfile) -> None:
        """Check for capacity-related alerts"""
        
        # Overload alert
        if profile.capacity_status == CapacityStatus.OVERLOADED:
            alert = {
                'alert_id': str(uuid.uuid4()),
                'agent_id': agent_id,
                'alert_type': 'CAPACITY_OVERLOAD',
                'severity': 'HIGH',
                'message': f'Agent {agent_id} is overloaded (utilization: {profile.current_capacity:.1%})',
                'timestamp': datetime.now().isoformat(),
                'recommendations': [
                    'Redistribute tasks to other agents',
                    'Defer non-critical tasks',
                    'Increase agent capacity if possible'
                ]
            }
            self.capacity_alerts.append(alert)
        
        # Performance degradation alert
        if profile.performance_metrics.get('quality_score', 1.0) < 0.7:
            alert = {
                'alert_id': str(uuid.uuid4()),
                'agent_id': agent_id,
                'alert_type': 'PERFORMANCE_DEGRADATION',
                'severity': 'MEDIUM',
                'message': f'Agent {agent_id} performance below threshold (quality: {profile.performance_metrics["quality_score"]:.1%})',
                'timestamp': datetime.now().isoformat(),
                'recommendations': [
                    'Review recent task assignments',
                    'Check for resource constraints',
                    'Consider agent maintenance'
                ]
            }
            self.performance_alerts.append(alert)
    
    def _identify_relevant_agents(self, task_requirements: Dict[str, Any]) -> List[str]:
        """Identify agents relevant for a specific task"""
        
        task_type = task_requirements.get('type', 'general')
        required_skills = task_requirements.get('skills', [])
        
        # Agent skill mappings
        agent_skills = {
            'John': ['requirements', 'business_analysis', 'stakeholder_management'],
            'Fred': ['architecture', 'system_design', 'integration'],
            'Tyler': ['planning', 'task_breakdown', 'project_management'],
            'Jane': ['design', 'ui_ux', 'frontend'],
            'Alex': ['infrastructure', 'devops', 'security'],
            'James': ['development', 'backend', 'frontend', 'api'],
            'Dakota': ['data', 'database', 'analytics'],
            'Sage': ['validation', 'compliance', 'security'],
            'Sentinel': ['testing', 'quality_assurance', 'performance'],
            'DocQA': ['documentation', 'technical_writing', 'knowledge_management']
        }
        
        relevant_agents = []
        
        # Find agents with matching skills
        for agent_id, skills in agent_skills.items():
            if any(skill in skills for skill in required_skills) or not required_skills:
                relevant_agents.append(agent_id)
        
        # If no specific skills required, include all agents
        if not relevant_agents:
            relevant_agents = list(agent_skills.keys())
        
        return relevant_agents
    
    def _calculate_assignment_score(self, agent_id: str, assessment: AgentCapacityProfile, 
                                  task_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate assignment score for an agent"""
        
        # Capacity score (inverse of utilization)
        capacity_score = max(0.0, 1.0 - assessment.current_capacity)
        
        # Performance score
        performance_score = (
            assessment.performance_metrics.get('task_completion_rate', 0.8) * 0.3 +
            assessment.performance_metrics.get('quality_score', 0.9) * 0.4 +
            assessment.performance_metrics.get('collaboration_effectiveness', 0.8) * 0.3
        )
        
        # Availability score
        availability_score = 1.0 if assessment.capacity_status == CapacityStatus.AVAILABLE else 0.5
        if assessment.capacity_status == CapacityStatus.OVERLOADED:
            availability_score = 0.1
        
        # Skill match score (simplified)
        skill_score = 0.8  # Default skill match
        
        # Calculate total score
        total_score = (
            capacity_score * 0.3 +
            performance_score * 0.3 +
            availability_score * 0.3 +
            skill_score * 0.1
        )
        
        # Calculate confidence
        confidence = min(total_score * 1.2, 1.0)
        
        return {
            'total_score': total_score,
            'confidence': confidence,
            'capacity_score': capacity_score,
            'performance_score': performance_score,
            'availability_score': availability_score,
            'skill_score': skill_score,
            'rationale': f"Agent {agent_id} selected based on capacity ({capacity_score:.1%}), "
                        f"performance ({performance_score:.1%}), and availability ({availability_score:.1%})"
        }
    
    def _estimate_completion_time(self, agent_id: str, profile: AgentCapacityProfile, 
                                task_requirements: Dict[str, Any]) -> int:
        """Estimate task completion time for an agent"""
        
        base_time = task_requirements.get('estimated_duration', 3600)  # 1 hour default
        
        # Adjust based on current capacity
        capacity_factor = 1.0 + profile.current_capacity  # Higher capacity = longer time
        
        # Adjust based on performance
        performance_factor = 2.0 - profile.performance_metrics.get('task_completion_rate', 0.8)
        
        estimated_time = int(base_time * capacity_factor * performance_factor)
        
        return estimated_time
    
    def _analyze_capacity_trend(self, capacity_trend: List[float]) -> Dict[str, Any]:
        """Analyze capacity trend for predictions"""
        
        if len(capacity_trend) < 3:
            return {'trend': 'INSUFFICIENT_DATA', 'confidence': 0.0}
        
        # Calculate trend direction
        recent_trend = capacity_trend[-5:]  # Last 5 measurements
        if len(recent_trend) >= 3:
            slope = (recent_trend[-1] - recent_trend[0]) / len(recent_trend)
            
            if slope > 0.05:
                trend = 'INCREASING'
            elif slope < -0.05:
                trend = 'DECREASING'
            else:
                trend = 'STABLE'
        else:
            trend = 'STABLE'
        
        # Calculate confidence based on trend consistency
        variance = statistics.variance(capacity_trend) if len(capacity_trend) > 1 else 0.0
        confidence = max(0.0, 1.0 - variance * 2)  # Lower variance = higher confidence
        
        return {
            'trend': trend,
            'slope': slope if 'slope' in locals() else 0.0,
            'variance': variance,
            'confidence': confidence,
            'recent_average': statistics.mean(recent_trend) if recent_trend else 0.0
        }
    
    def _predict_future_capacity(self, profile: AgentCapacityProfile, 
                               trend_analysis: Dict[str, Any], hours: int) -> float:
        """Predict future capacity based on trend analysis"""
        
        current_capacity = profile.current_capacity
        
        if trend_analysis['trend'] == 'INCREASING':
            # Predict increase based on slope
            predicted_increase = trend_analysis['slope'] * hours * 0.1  # Scale factor
            predicted_capacity = current_capacity + predicted_increase
        elif trend_analysis['trend'] == 'DECREASING':
            # Predict decrease based on slope
            predicted_decrease = abs(trend_analysis['slope']) * hours * 0.1
            predicted_capacity = current_capacity - predicted_decrease
        else:
            # Stable trend
            predicted_capacity = current_capacity
        
        return max(0.0, min(predicted_capacity, 1.0))
    
    def _calculate_bottleneck_risk(self, agent_id: str, profile: AgentCapacityProfile, 
                                 predicted_capacity: float) -> float:
        """Calculate bottleneck risk score"""
        
        # Risk factors
        capacity_risk = predicted_capacity  # Higher predicted capacity = higher risk
        current_load_risk = profile.current_capacity
        performance_risk = 1.0 - profile.performance_metrics.get('quality_score', 0.9)
        
        # Calculate overall risk
        risk_score = (
            capacity_risk * 0.5 +
            current_load_risk * 0.3 +
            performance_risk * 0.2
        )
        
        return min(risk_score, 1.0)
    
    def _estimate_time_to_bottleneck(self, profile: AgentCapacityProfile, 
                                   trend_analysis: Dict[str, Any]) -> int:
        """Estimate time until bottleneck occurs"""
        
        if trend_analysis['trend'] != 'INCREASING':
            return -1  # No bottleneck expected
        
        current_capacity = profile.current_capacity
        bottleneck_threshold = 0.9
        
        if current_capacity >= bottleneck_threshold:
            return 0  # Already at bottleneck
        
        capacity_gap = bottleneck_threshold - current_capacity
        slope = trend_analysis.get('slope', 0.0)
        
        if slope <= 0:
            return -1  # No increase trend
        
        # Estimate hours to reach bottleneck
        hours_to_bottleneck = int(capacity_gap / (slope * 0.1))  # Scale factor
        
        return max(1, hours_to_bottleneck)
    
    def _suggest_mitigation_strategies(self, agent_id: str, risk_score: float) -> List[str]:
        """Suggest mitigation strategies for bottleneck risk"""
        
        strategies = []
        
        if risk_score > 0.8:
            strategies.extend([
                'Immediately redistribute high-priority tasks to other agents',
                'Defer non-critical tasks until capacity improves',
                'Consider temporary capacity increase or additional resources'
            ])
        elif risk_score > 0.6:
            strategies.extend([
                'Monitor capacity closely and prepare for task redistribution',
                'Identify tasks that can be delegated or postponed',
                'Review current task priorities and deadlines'
            ])
        else:
            strategies.extend([
                'Continue monitoring capacity trends',
                'Optimize current task assignments for efficiency'
            ])
        
        return strategies
    
    def _calculate_distribution_metrics(self, assessments: Dict[str, AgentCapacityProfile]) -> Dict[str, Any]:
        """Calculate current workload distribution metrics"""
        
        capacities = [profile.current_capacity for profile in assessments.values()]
        
        return {
            'average_utilization': statistics.mean(capacities),
            'utilization_variance': statistics.variance(capacities) if len(capacities) > 1 else 0.0,
            'max_utilization': max(capacities),
            'min_utilization': min(capacities),
            'overloaded_agents': len([c for c in capacities if c > 0.9]),
            'underutilized_agents': len([c for c in capacities if c < 0.3])
        }
    
    def _identify_optimization_opportunities(self, assessments: Dict[str, AgentCapacityProfile]) -> List[Dict[str, Any]]:
        """Identify workload optimization opportunities"""
        
        opportunities = []
        
        # Find overloaded and underutilized agents
        overloaded = [(aid, profile) for aid, profile in assessments.items() if profile.current_capacity > 0.8]
        underutilized = [(aid, profile) for aid, profile in assessments.items() if profile.current_capacity < 0.4]
        
        # Create redistribution opportunities
        for overloaded_agent, overloaded_profile in overloaded:
            for underutilized_agent, underutilized_profile in underutilized:
                opportunity = {
                    'type': 'TASK_REDISTRIBUTION',
                    'from_agent': overloaded_agent,
                    'to_agent': underutilized_agent,
                    'potential_improvement': overloaded_profile.current_capacity - underutilized_profile.current_capacity,
                    'feasibility': self._assess_redistribution_feasibility(overloaded_agent, underutilized_agent)
                }
                opportunities.append(opportunity)
        
        return opportunities
    
    def _assess_redistribution_feasibility(self, from_agent: str, to_agent: str) -> float:
        """Assess feasibility of task redistribution between agents"""
        
        # Simplified feasibility assessment
        # In real implementation, would consider skill compatibility, task types, etc.
        return 0.7  # Default feasibility score
    
    def _create_redistribution_plan(self, assessments: Dict[str, AgentCapacityProfile], 
                                  opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create redistribution plan based on opportunities"""
        
        plan = []
        
        # Sort opportunities by potential improvement
        sorted_opportunities = sorted(opportunities, key=lambda x: x['potential_improvement'], reverse=True)
        
        for opportunity in sorted_opportunities[:5]:  # Top 5 opportunities
            if opportunity['feasibility'] > 0.5:
                plan.append({
                    'action': 'REDISTRIBUTE_TASKS',
                    'from_agent': opportunity['from_agent'],
                    'to_agent': opportunity['to_agent'],
                    'expected_improvement': opportunity['potential_improvement'],
                    'priority': 'HIGH' if opportunity['potential_improvement'] > 0.4 else 'MEDIUM'
                })
        
        return plan
    
    def _calculate_expected_improvements(self, current_distribution: Dict[str, Any], 
                                       redistribution_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate expected improvements from redistribution plan"""
        
        if not redistribution_plan:
            return {'improvement_score': 0.0, 'variance_reduction': 0.0}
        
        # Estimate improvements
        total_improvement = sum(action['expected_improvement'] for action in redistribution_plan)
        variance_reduction = min(total_improvement * 0.5, current_distribution['utilization_variance'])
        
        return {
            'improvement_score': min(total_improvement, 1.0),
            'variance_reduction': variance_reduction,
            'expected_average_utilization': current_distribution['average_utilization'] + total_improvement * 0.1
        }
    
    def _calculate_optimization_confidence(self, redistribution_plan: List[Dict[str, Any]]) -> float:
        """Calculate confidence in optimization plan"""
        
        if not redistribution_plan:
            return 0.0
        
        # Base confidence on number and quality of actions
        base_confidence = min(len(redistribution_plan) * 0.2, 0.8)
        
        # Adjust based on expected improvements
        avg_improvement = statistics.mean([action['expected_improvement'] for action in redistribution_plan])
        improvement_factor = min(avg_improvement * 2, 1.0)
        
        return min(base_confidence * improvement_factor, 1.0)
    
    def get_capacity_assessment_status(self) -> Dict[str, Any]:
        """Get current capacity assessment system status"""
        
        return {
            'monitored_agents': len(self.agent_profiles),
            'active_alerts': len(self.capacity_alerts) + len(self.performance_alerts),
            'recent_assessments': self.assessment_metrics['total_assessments'],
            'optimal_assignments': self.assessment_metrics['optimal_assignments'],
            'average_system_utilization': self.assessment_metrics['average_utilization'],
            'monitoring_active': self.monitoring_active,
            'system_status': 'OPERATIONAL'
        }
    
    def _initialize_capacity_assessment(self) -> None:
        """Initialize the capacity assessment system"""
        
        # Create initial profiles for core agents
        core_agents = ['JAEGIS', 'John', 'Fred', 'Tyler', 'Jane', 'Alex', 'James', 'Dakota', 'Sage', 'Sentinel', 'DocQA']
        
        for agent_id in core_agents:
            self.agent_profiles[agent_id] = self._create_initial_agent_profile(agent_id)
        
        print("📊 JAEGIS Dynamic Capacity Assessment System initialized")
        print(f"   Monitoring: {len(self.agent_profiles)} agents")
        print("   Real-time Capacity Assessment: ACTIVE")
        print("   Predictive Analytics: ENABLED")
        print("   Optimization Recommendations: READY")

# Global capacity assessment system instance
JAEGIS_CAPACITY_ASSESSOR = JAEGISDynamicCapacityAssessor()

# Enhanced capacity assessment functions
async def assess_agent_capacity_real_time(agent_id: str) -> AgentCapacityProfile:
    """Real-time agent capacity assessment"""
    return await JAEGIS_CAPACITY_ASSESSOR.assess_agent_capacity(agent_id)

async def get_optimal_task_assignment(task_requirements: Dict[str, Any]) -> TaskAssignmentRecommendation:
    """Get optimal task assignment recommendation"""
    return await JAEGIS_CAPACITY_ASSESSOR.recommend_optimal_assignment(task_requirements)

async def predict_system_bottlenecks(hours: int = 24) -> List[Dict[str, Any]]:
    """Predict system capacity bottlenecks"""
    return await JAEGIS_CAPACITY_ASSESSOR.predict_capacity_bottlenecks(hours)

async def optimize_agent_workloads() -> Dict[str, Any]:
    """Optimize workload distribution across agents"""
    return await JAEGIS_CAPACITY_ASSESSOR.optimize_workload_distribution()

def get_capacity_system_status() -> Dict[str, Any]:
    """Get capacity assessment system status"""
    return JAEGIS_CAPACITY_ASSESSOR.get_capacity_assessment_status()

# Example usage and testing
if __name__ == "__main__":
    async def test_capacity_assessment():
        print("🧪 Testing JAEGIS Dynamic Capacity Assessment...")
        
        # Test agent capacity assessment
        agents_to_test = ['John', 'Fred', 'James', 'Jane']
        
        for agent_id in agents_to_test:
            profile = await assess_agent_capacity_real_time(agent_id)
            print(f"   {agent_id}: {profile.capacity_status.value} | Utilization: {profile.current_capacity:.1%}")
        
        # Test task assignment recommendation
        test_task = {
            'task_id': 'TEST_TASK_001',
            'type': 'development',
            'skills': ['backend', 'api'],
            'estimated_duration': 7200  # 2 hours
        }
        
        recommendation = await get_optimal_task_assignment(test_task)
        print(f"\n📋 TASK ASSIGNMENT RECOMMENDATION:")
        print(f"   Recommended Agent: {recommendation.recommended_agent}")
        print(f"   Confidence: {recommendation.confidence_score:.1%}")
        print(f"   Expected Completion: {recommendation.expected_completion_time}s")
        
        # Test bottleneck prediction
        bottlenecks = await predict_system_bottlenecks(24)
        print(f"\n🔮 BOTTLENECK PREDICTIONS:")
        print(f"   Potential Bottlenecks: {len(bottlenecks)}")
        
        for bottleneck in bottlenecks[:3]:  # Show top 3
            print(f"   {bottleneck['agent_id']}: Risk {bottleneck['bottleneck_risk']:.1%}")
        
        # Test workload optimization
        optimization = await optimize_agent_workloads()
        print(f"\n⚖️ WORKLOAD OPTIMIZATION:")
        print(f"   Opportunities: {len(optimization['optimization_opportunities'])}")
        print(f"   Redistribution Actions: {len(optimization['redistribution_plan'])}")
        
        # Get system status
        status = get_capacity_system_status()
        print(f"\n🎯 CAPACITY SYSTEM STATUS:")
        print(f"   Monitored Agents: {status['monitored_agents']}")
        print(f"   Active Alerts: {status['active_alerts']}")
        print(f"   Recent Assessments: {status['recent_assessments']}")
        
        print("\n✅ JAEGIS Dynamic Capacity Assessment test completed")

    # Run test
    asyncio.run(test_capacity_assessment())
