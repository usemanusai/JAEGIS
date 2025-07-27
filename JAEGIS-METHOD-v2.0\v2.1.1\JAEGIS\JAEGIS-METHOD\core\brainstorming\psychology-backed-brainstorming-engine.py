"""
JAEGIS Psychology-Backed Brainstorming Engine
Implements science-based brainstorming methodologies for optimal human-AI collaboration
"""

import json
import uuid
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class BrainstormingPhase(Enum):
    PREPARATION = "preparation"
    DIVERGENT_GENERATION = "divergent_generation"
    INCUBATION = "incubation"
    CONVERGENT_REFINEMENT = "convergent_refinement"
    SYNTHESIS = "synthesis"

class CognitiveStyle(Enum):
    ANALYTICAL = "analytical"
    INTUITIVE = "intuitive"
    BALANCED = "balanced"

class ThinkingMode(Enum):
    SYSTEM_1 = "system_1"  # Fast, intuitive, associative
    SYSTEM_2 = "system_2"  # Slow, deliberate, analytical

@dataclass
class BrainstormingContext:
    """Context for brainstorming session"""
    session_id: str
    problem_statement: str
    user_cognitive_style: CognitiveStyle
    session_duration: int  # minutes
    complexity_level: str  # "simple", "moderate", "complex"
    domain: str
    constraints: List[str]
    stakeholders: List[str]
    success_criteria: List[str]

@dataclass
class Idea:
    """Individual idea representation"""
    id: str
    content: str
    category: str
    originality_score: float
    feasibility_score: float
    impact_score: float
    elaboration_level: int
    source: str  # "human", "ai", "collaborative"
    timestamp: datetime
    related_ideas: List[str] = None

@dataclass
class BrainstormingResult:
    """Complete brainstorming session result"""
    session_id: str
    total_ideas: int
    ideas_by_phase: Dict[str, List[Idea]]
    quality_metrics: Dict[str, float]
    collaboration_metrics: Dict[str, float]
    final_concepts: List[Idea]
    next_steps: List[str]

class PsychologyBackedBrainstormingEngine:
    """Main brainstorming engine implementing psychology-backed methodologies"""
    
    def __init__(self):
        self.technique_library = self._initialize_techniques()
        self.quality_assessor = IdeaQualityAssessor()
        self.collaboration_optimizer = HumanAICollaborationOptimizer()
        
    def conduct_brainstorming_session(self, context: BrainstormingContext) -> BrainstormingResult:
        """Conduct complete psychology-backed brainstorming session"""
        
        session_result = BrainstormingResult(
            session_id=context.session_id,
            total_ideas=0,
            ideas_by_phase={},
            quality_metrics={},
            collaboration_metrics={},
            final_concepts=[],
            next_steps=[]
        )
        
        # Phase 1: Preparation and Priming
        prep_result = self._execute_preparation_phase(context)
        session_result.ideas_by_phase[BrainstormingPhase.PREPARATION.value] = prep_result
        
        # Phase 2: Divergent Generation
        divergent_result = self._execute_divergent_phase(context, prep_result)
        session_result.ideas_by_phase[BrainstormingPhase.DIVERGENT_GENERATION.value] = divergent_result
        
        # Phase 3: Incubation and Reflection
        incubation_result = self._execute_incubation_phase(context, divergent_result)
        session_result.ideas_by_phase[BrainstormingPhase.INCUBATION.value] = incubation_result
        
        # Phase 4: Convergent Refinement
        convergent_result = self._execute_convergent_phase(context, divergent_result + incubation_result)
        session_result.ideas_by_phase[BrainstormingPhase.CONVERGENT_REFINEMENT.value] = convergent_result
        
        # Phase 5: Synthesis and Planning
        synthesis_result = self._execute_synthesis_phase(context, convergent_result)
        session_result.ideas_by_phase[BrainstormingPhase.SYNTHESIS.value] = synthesis_result
        
        # Calculate final metrics
        all_ideas = []
        for phase_ideas in session_result.ideas_by_phase.values():
            all_ideas.extend(phase_ideas)
        
        session_result.total_ideas = len(all_ideas)
        session_result.quality_metrics = self.quality_assessor.assess_session_quality(all_ideas)
        session_result.collaboration_metrics = self.collaboration_optimizer.assess_collaboration_quality(all_ideas)
        session_result.final_concepts = synthesis_result[:5]  # Top 5 concepts
        session_result.next_steps = self._generate_next_steps(context, session_result)
        
        return session_result
    
    def _execute_preparation_phase(self, context: BrainstormingContext) -> List[Idea]:
        """Phase 1: Preparation and cognitive priming"""
        
        preparation_ideas = []
        
        # Context setting and goal clarification
        context_idea = self._generate_context_setting_idea(context)
        preparation_ideas.append(context_idea)
        
        # Stakeholder perspective priming
        for stakeholder in context.stakeholders:
            stakeholder_idea = self._generate_stakeholder_perspective_idea(stakeholder, context)
            preparation_ideas.append(stakeholder_idea)
        
        # Constraint awareness and opportunity framing
        constraint_opportunities = self._identify_constraint_opportunities(context.constraints)
        preparation_ideas.extend(constraint_opportunities)
        
        # Creative mindset activation
        mindset_activation = self._activate_creative_mindset(context)
        preparation_ideas.extend(mindset_activation)
        
        return preparation_ideas
    
    def _execute_divergent_phase(self, context: BrainstormingContext, prep_ideas: List[Idea]) -> List[Idea]:
        """Phase 2: Divergent idea generation using multiple techniques"""
        
        divergent_ideas = []
        
        # Technique 1: Rapid Idea Generation (System 1 thinking)
        rapid_ideas = self._rapid_idea_generation(context, duration_minutes=5)
        divergent_ideas.extend(rapid_ideas)
        
        # Technique 2: Analogical Thinking
        analogical_ideas = self._analogical_thinking_generation(context)
        divergent_ideas.extend(analogical_ideas)
        
        # Technique 3: Perspective Shifting
        perspective_ideas = self._perspective_shifting_generation(context)
        divergent_ideas.extend(perspective_ideas)
        
        # Technique 4: Constraint Challenging
        constraint_challenge_ideas = self._constraint_challenging_generation(context)
        divergent_ideas.extend(constraint_challenge_ideas)
        
        # Technique 5: Random Stimulation
        random_stimulation_ideas = self._random_stimulation_generation(context)
        divergent_ideas.extend(random_stimulation_ideas)
        
        return divergent_ideas
    
    def _execute_incubation_phase(self, context: BrainstormingContext, divergent_ideas: List[Idea]) -> List[Idea]:
        """Phase 3: Incubation and default mode network activation"""
        
        incubation_ideas = []
        
        # Pattern recognition and theme identification
        patterns = self._identify_idea_patterns(divergent_ideas)
        for pattern in patterns:
            pattern_idea = self._generate_pattern_based_idea(pattern, context)
            incubation_ideas.append(pattern_idea)
        
        # Unconscious processing simulation
        unconscious_ideas = self._simulate_unconscious_processing(divergent_ideas, context)
        incubation_ideas.extend(unconscious_ideas)
        
        # Cross-pollination between ideas
        cross_pollination_ideas = self._generate_cross_pollination_ideas(divergent_ideas)
        incubation_ideas.extend(cross_pollination_ideas)
        
        return incubation_ideas
    
    def _execute_convergent_phase(self, context: BrainstormingContext, all_ideas: List[Idea]) -> List[Idea]:
        """Phase 4: Convergent refinement and development"""
        
        # Cluster similar ideas
        idea_clusters = self._cluster_ideas(all_ideas)
        
        # Evaluate and prioritize ideas
        prioritized_ideas = self._prioritize_ideas(all_ideas, context)
        
        # Develop top ideas further
        developed_ideas = []
        for idea in prioritized_ideas[:10]:  # Top 10 ideas
            developed_idea = self._develop_idea_further(idea, context)
            developed_ideas.append(developed_idea)
        
        # Combine complementary ideas
        combined_ideas = self._combine_complementary_ideas(developed_ideas)
        developed_ideas.extend(combined_ideas)
        
        return developed_ideas
    
    def _execute_synthesis_phase(self, context: BrainstormingContext, refined_ideas: List[Idea]) -> List[Idea]:
        """Phase 5: Final synthesis and concept selection"""
        
        # Final evaluation using multiple criteria
        final_scores = {}
        for idea in refined_ideas:
            score = self._calculate_final_idea_score(idea, context)
            final_scores[idea.id] = score
        
        # Sort by final score
        sorted_ideas = sorted(refined_ideas, key=lambda x: final_scores[x.id], reverse=True)
        
        # Select final concepts
        final_concepts = sorted_ideas[:5]
        
        # Enhance final concepts with implementation insights
        enhanced_concepts = []
        for concept in final_concepts:
            enhanced_concept = self._enhance_concept_with_implementation_insights(concept, context)
            enhanced_concepts.append(enhanced_concept)
        
        return enhanced_concepts
    
    def _rapid_idea_generation(self, context: BrainstormingContext, duration_minutes: int) -> List[Idea]:
        """Generate ideas rapidly using System 1 thinking"""
        
        ideas = []
        
        # Simulate rapid associative thinking
        seed_words = self._extract_seed_words(context.problem_statement)
        
        for seed_word in seed_words:
            # Generate associations
            associations = self._generate_word_associations(seed_word)
            
            for association in associations:
                idea_content = self._create_idea_from_association(association, context)
                idea = Idea(
                    id=str(uuid.uuid4()),
                    content=idea_content,
                    category="rapid_generation",
                    originality_score=random.uniform(0.3, 0.8),
                    feasibility_score=random.uniform(0.4, 0.9),
                    impact_score=random.uniform(0.3, 0.7),
                    elaboration_level=1,
                    source="ai",
                    timestamp=datetime.now()
                )
                ideas.append(idea)
        
        return ideas[:15]  # Limit to 15 rapid ideas
    
    def _analogical_thinking_generation(self, context: BrainstormingContext) -> List[Idea]:
        """Generate ideas using analogical thinking"""
        
        ideas = []
        
        # Define analogy domains
        analogy_domains = [
            "nature_and_biology",
            "other_industries",
            "historical_solutions",
            "everyday_objects",
            "games_and_sports"
        ]
        
        for domain in analogy_domains:
            analogy_examples = self._get_analogy_examples(domain)
            
            for example in analogy_examples:
                analogical_idea = self._create_analogical_idea(example, context)
                idea = Idea(
                    id=str(uuid.uuid4()),
                    content=analogical_idea,
                    category="analogical_thinking",
                    originality_score=random.uniform(0.6, 0.9),
                    feasibility_score=random.uniform(0.3, 0.8),
                    impact_score=random.uniform(0.4, 0.8),
                    elaboration_level=2,
                    source="ai",
                    timestamp=datetime.now()
                )
                ideas.append(idea)
        
        return ideas
    
    def _perspective_shifting_generation(self, context: BrainstormingContext) -> List[Idea]:
        """Generate ideas from different perspectives"""
        
        ideas = []
        
        # Define perspectives
        perspectives = [
            "end_user",
            "business_stakeholder",
            "technical_implementer",
            "competitor",
            "future_user",
            "cost_conscious_buyer",
            "innovation_seeker"
        ]
        
        for perspective in perspectives:
            perspective_idea = self._create_perspective_based_idea(perspective, context)
            idea = Idea(
                id=str(uuid.uuid4()),
                content=perspective_idea,
                category="perspective_shifting",
                originality_score=random.uniform(0.4, 0.7),
                feasibility_score=random.uniform(0.5, 0.9),
                impact_score=random.uniform(0.5, 0.8),
                elaboration_level=2,
                source="collaborative",
                timestamp=datetime.now()
            )
            ideas.append(idea)
        
        return ideas
    
    def _initialize_techniques(self) -> Dict[str, Any]:
        """Initialize brainstorming technique library""return_osborn_rules": {
                "defer_judgment": True,
                "strive_for_quantity": True,
                "welcome_wild_ideas": True,
                "build_on_ideasTrue_guilford_factors": {
                "fluency": "number_of_ideas",
                "flexibility": "variety_of_categories",
                "originality": "uniqueness_of_ideas",
                "elaboration": "detail_and_developmentdual_process": {
                "system_1": ["rapid_generation", "associative_thinking", "intuitive_leaps"],
                "system_2": ["analytical_evaluation", "systematic_development", "logical_refinementenvironmental_factors": {
                "suggest_movement": True,
                "encourage_breaks": True,
                "optimize_timing": True,
                "manage_cognitive_load": True
            }
        }
    
    # Helper methods (abbreviated for space)
    def _generate_context_setting_idea(self, context: BrainstormingContext) -> Idea:
        """Generate context-setting idea"""
        content = f"Context: {context.problem_statement} - Domain: {context.domain}"
        return Idea(
            id=str(uuid.uuid4()),
            content=content,
            category="context_setting",
            originality_score=0.5,
            feasibility_score=1.0,
            impact_score=0.7,
            elaboration_level=1,
            source="ai",
            timestamp=datetime.now()
        )
    
    def _extract_seed_words(self, problem_statement: str) -> List[str]:
        """Extract key words from problem statement"""
        # Simplified implementation
        words = problem_statement.lower().split()
        return [word for word in words if len(word) > 3][:5]
    
    def _generate_word_associations(self, seed_word: str) -> List[str]:
        """Generate word associations"""
        # Simplified implementation - in real system would use semantic networks
        associations = {
            "software": ["application", "system", "platform", "tool", "solution"],
            "user": ["customer", "person", "individual", "client", "stakeholder"],
            "problem": ["challenge", "issue", "opportunity", "need", "gap"],
            "solution": ["answer", "approach", "method", "strategy", "fix"]
        }
        return associations.get(seed_word, ["innovation", "improvement", "enhancement"])
    
    def _calculate_final_idea_score(self, idea: Idea, context: BrainstormingContext) -> float:
        """Calculate final weighted score for idea"""
        weights = {
            "originality": 0.3,
            "feasibility": 0.3,
            "impact": 0.4
        }
        
        score = (
            idea.originality_score * weights["originality"] +
            idea.feasibility_score * weights["feasibility"] +
            idea.impact_score * weights["impact"]
        )
        
        return score

class IdeaQualityAssessor:
    """Assesses quality of generated ideas"""
    
    def assess_session_quality(self, ideas: List[Idea]) -> Dict[str, float]:
        """Assess overall session quality"""
        
        if not ideas:
            return {"fluency": 0.0, "flexibility": 0.0, "originality": 0.0, "elaboration": 0.0}
        
        # Fluency: Number of ideas
        fluency = len(ideas) / 50.0  # Normalize to expected 50 ideas
        
        # Flexibility: Number of different categories
        categories = set(idea.category for idea in ideas)
        flexibility = len(categories) / 10.0  # Normalize to expected 10 categories
        
        # Originality: Average originality score
        originality = sum(idea.originality_score for idea in ideas) / len(ideas)
        
        # Elaboration: Average elaboration level
        elaboration = sum(idea.elaboration_level for idea in ideas) / len(ideas) / 3.0  # Normalize to max 3
        
        return {
            "fluency": min(fluency, 1.0),
            "flexibility": min(flexibility, 1.0),
            "originality": originality,
            "elaboration": min(elaboration, 1.0)
        }

class HumanAICollaborationOptimizer:
    """Optimizes human-AI collaboration in brainstorming"""
    
    def assess_collaboration_quality(self, ideas: List[Idea]) -> Dict[str, float]:
        """Assess quality of human-AI collaboration"""
        
        if not ideas:
            return {"balance": 0.0, "synergy": 0.0, "engagement": 0.0}
        
        # Balance: Distribution of human vs AI vs collaborative ideas
        sources = [idea.source for idea in ideas]
        human_count = sources.count("human")
        ai_count = sources.count("ai")
        collaborative_count = sources.count("collaborative")
        
        total = len(ideas)
        balance = 1.0 - abs(0.33 - collaborative_count/total)  # Optimal is 33% collaborative
        
        # Synergy: Ideas that build on each other
        synergy = collaborative_count / total if total > 0 else 0.0
        
        # Engagement: Variety in idea development
        elaboration_levels = [idea.elaboration_level for idea in ideas]
        engagement = len(set(elaboration_levels)) / 3.0  # Max 3 levels
        
        return {
            "balance": balance,
            "synergy": synergy,
            "engagement": min(engagement, 1.0)
        }

# Example usage and testing
if __name__ == "__main__":
    # Create brainstorming context
    context = BrainstormingContext(
        session_id=str(uuid.uuid4()),
        problem_statement="How can we improve user onboarding for our software platform?",
        user_cognitive_style=CognitiveStyle.BALANCED,
        session_duration=60,
        complexity_level="moderate",
        domain="software_development",
        constraints=["limited_budget", "existing_user_base", "technical_debt"],
        stakeholders=["end_users", "product_managers", "developers", "support_team"],
        success_criteria=["increased_user_retention", "reduced_support_tickets", "faster_time_to_value"]
    )
    
    # Run brainstorming session
    engine = PsychologyBackedBrainstormingEngine()
    result = engine.conduct_brainstorming_session(context)
    
    # Display results
    print(f"Session completed with {result.total_ideas} total ideas")
    print(f"Quality metrics: {result.quality_metrics}")
    print(f"Collaboration metrics: {result.collaboration_metrics}")
    print(f"Top concepts: {[idea.content for idea in result.final_concepts]}")
