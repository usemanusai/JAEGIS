"""
JAEGIS Advanced Elicitation Techniques - Execution Engine
Implements the 30 research-backed elicitation techniques for enhanced AI responses
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TechniqueCategory(Enum):
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    COLLABORATIVE = "collaborative"
    SYSTEMATIC = "systematic"

class JAEGISPhase(Enum):
    BRAINSTORMING = "brainstorming"
    MODELING = "modeling"
    ARCHITECTURE = "architecture"
    DEVELOPMENT = "development"
    VALIDATION = "validation"

@dataclass
class ElicitationContext:
    """Context information for technique selection and application"""
    phase: JAEGISPhase
    task_complexity: str  # "simple", "moderate", "complex"
    user_expertise: str   # "novice", "intermediate", "expert"
    session_history: List[Dict]
    user_preferences: Dict[str, Any]
    project_domain: str
    time_constraints: Optional[str] = None

@dataclass
class TechniqueResult:
    """Result of applying an elicitation technique"""
    technique_id: str
    technique_name: str
    enhanced_prompt: str
    execution_time: float
    quality_metrics: Dict[str, float]
    user_satisfaction: Optional[float] = None

class AdvancedElicitationEngine:
    """Main engine for selecting and applying elicitation techniques"""
    
    def __init__(self):
        self.technique_library = self._initialize_technique_library()
        self.selection_rules = self._initialize_selection_rules()
        self.quality_assessor = ResponseQualityAssessor()
        
    def select_techniques(self, context: ElicitationContext, max_techniques: int = 3) -> List[str]:
        """Select optimal techniques based on context"""
        
        # Get candidate techniques for the current phase
        phase_techniques = self.selection_rules.get(context.phase, {})
        
        # Score techniques based on context
        technique_scores = {}
        for category, techniques in phase_techniques.items():
            for technique_id in techniques:
                score = self._calculate_technique_score(technique_id, context)
                technique_scores[technique_id] = score
        
        # Select top techniques
        sorted_techniques = sorted(technique_scores.items(), key=lambda x: x[1], reverse=True)
        selected = [technique_id for technique_id, score in sorted_techniques[:max_techniques]]
        
        return selected
    
    def apply_technique(self, technique_id: str, query: str, context: ElicitationContext) -> TechniqueResult:
        """Apply a specific elicitation technique to enhance a query"""
        
        start_time = datetime.now()
        
        # Get technique implementation
        technique = self.technique_library.get(technique_id)
        if not technique:
            raise ValueError(f"Unknown technique: {technique_id}")
        
        # Apply technique to enhance the query
        enhanced_prompt = technique.apply(query, context)
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Assess quality (would integrate with actual AI response in real implementation)
        quality_metrics = self.quality_assessor.assess_enhancement_quality(
            original_query=query,
            enhanced_prompt=enhanced_prompt,
            technique_id=technique_id
        )
        
        return TechniqueResult(
            technique_id=technique_id,
            technique_name=technique.name,
            enhanced_prompt=enhanced_prompt,
            execution_time=execution_time,
            quality_metrics=quality_metrics
        )
    
    def orchestrate_session(self, base_query: str, context: ElicitationContext) -> List[TechniqueResult]:
        """Orchestrate a complete elicitation session with multiple techniques"""
        
        session_results = []
        
        # Select techniques for this session
        selected_techniques = self.select_techniques(context)
        
        # Apply techniques in sequence
        current_query = base_query
        for technique_id in selected_techniques:
            
            # Apply technique
            result = self.apply_technique(technique_id, current_query, context)
            session_results.append(result)
            
            # Update query for next technique (could use AI response here)
            current_query = self._update_query_with_insights(current_query, result)
            
            # Update context with new insights
            context = self._update_context_with_result(context, result)
        
        return session_results
    
    def _calculate_technique_score(self, technique_id: str, context: ElicitationContext) -> float:
        """Calculate relevance score for a technique given the context""tool_9311": {"systematic": 1.2, "analytical": 1.1, "creative": 0.9, "collaborative1_0_intermediate": {"systematic": 1.0, "analytical": 1.1, "creative": 1.1, "collaborative1_0_expert": {"systematic": 0.9, "analytical": 1.2, "creative": 1.2, "collaborativetool_2648": {"systematic": 0.8, "analytical": 0.9, "creative": 1.1, "collaborative0_9_moderate": {"systematic": 1.0, "analytical": 1.0, "creative": 1.0, "collaborative1_0_complex": {"systematic": 1.2, "analytical": 1.2, "creative": 0.9, "collaborative": 1.1}
        }
        
        # Get technique category
        technique = self.technique_library.get(technique_id)
        if technique:
            category = technique.category.value
            
            # Apply multipliers
            expertise_mult = expertise_multipliers.get(context.user_expertise, {}).get(category, 1.0)
            complexity_mult = complexity_multipliers.get(context.task_complexity, {}).get(category, 1.0)
            
            base_score = base_score * expertise_mult * complexity_mult
        
        # Adjust based on user preferences
        if context.user_preferences.get('preferred_techniques'):
            if technique_id in context.user_preferences['preferred_techniques']:
                base_score *= 1.3
        
        # Adjust based on recent usage (avoid overuse)
        recent_usage = self._get_recent_technique_usage(technique_id, context.session_history)
        if recent_usage > 2:
            base_score *= 0.7
        
        return min(base_score, 1.0)  # Cap at 1.0
    
    def _initialize_technique_library(self) -> Dict[str, 'ElicitationTechnique']:
        """Initialize the library of all 30 elicitation techniques"""
        
        techniques = {}
        
        # Analytical Techniques
        techniques.update({
            'chain_of_thought': ChainOfThoughtTechnique(),
            'what_if_analysis': WhatIfAnalysisTechnique(),
            'root_cause_analysis': RootCauseAnalysisTechnique(),
            'pros_cons_evaluation': ProsConsEvaluationTechnique(),
            'risk_assessment': RiskAssessmentTechnique(),
            'impact_analysis': ImpactAnalysisTechnique(),
            'constraint_analysis': ConstraintAnalysisTechnique(),
            'dependency_mapping': DependencyMappingTechnique()
        })
        
        # Creative Techniques
        techniques.update({
            'yes_and_building': YesAndBuildingTechnique(),
            'alternative_generation': AlternativeGenerationTechnique(),
            'analogical_thinking': AnalogicalThinkingTechnique(),
            'reverse_brainstorming': ReverseBrainstormingTechnique(),
            'scamper_application': ScamperTechnique(),
            'constraint_removal': ConstraintRemovalTechnique(),
            'biomimicry_inspiration': BiomimicryTechnique(),
            'random_word_association': RandomWordTechnique()
        })
        
        # Collaborative Techniques
        techniques.update({
            'multiple_personality': MultiplePersonalityTechnique(),
            'stakeholder_perspective': StakeholderPerspectiveTechnique(),
            'devils_advocate': DevilsAdvocateTechnique(),
            'six_thinking_hats': SixThinkingHatsTechnique(),
            'expert_panel_simulation': ExpertPanelTechnique(),
            'consensus_building': ConsensusBuildingTechnique(),
            'conflict_resolution': ConflictResolutionTechnique()
        })
        
        # Systematic Techniques
        techniques.update({
            'hierarchical_decomposition': HierarchicalDecompositionTechnique(),
            'process_mapping': ProcessMappingTechnique(),
            'decision_tree_analysis': DecisionTreeAnalysisTechnique(),
            'priority_matrix': PriorityMatrixTechnique(),
            'progressive_deepening': ProgressiveDeepeningTechnique(),
            'laddering_up_down': LadderingTechnique(),
            'critical_decision_method': CriticalDecisionMethodTechnique()
        })
        
        return techniques
    
    def _initialize_selection_rules(self) -> Dict[JAEGISPhase, Dict[str, List[str]]]:
        """Initialize rules for technique selection by phase"""
        
        return {
            JAEGISPhase.BRAINSTORMING: {
                "primary": ["alternative_generation", "yes_and_building", "analogical_thinking", "scamper_application"],
                "creative": ["reverse_brainstorming", "constraint_removal", "biomimicry_inspiration", "random_word_association"],
                "analytical": ["what_if_analysis", "chain_of_thought"]
            },
            JAEGISPhase.MODELING: {
                "collaborative": ["stakeholder_perspective", "multiple_personality", "expert_panel_simulation"],
                "systematic": ["progressive_deepening", "hierarchical_decomposition", "laddering_up_down"],
                "analytical": ["pros_cons_evaluation", "risk_assessment", "dependency_mapping"]
            },
            JAEGISPhase.ARCHITECTURE: {
                "analytical": ["chain_of_thought", "decision_tree_analysis", "impact_analysis"],
                "systematic": ["hierarchical_decomposition", "process_mapping", "critical_decision_method"],
                "collaborative": ["six_thinking_hats", "devils_advocate"]
            },
            JAEGISPhase.VALIDATION: {
                "collaborative": ["devils_advocate", "six_thinking_hats", "conflict_resolution"],
                "analytical": ["pros_cons_evaluation", "risk_assessment", "root_cause_analysis"],
                "systematic": ["critical_decision_method", "consensus_building"]
            }
        }
    
    def _update_query_with_insights(self, original_query: str, result: TechniqueResult) -> str:
        """Update query based on technique application results"""
        # In a real implementation, this would analyze the AI response and extract insights
        # For now, return the enhanced prompt as the new query base
        return result.enhanced_prompt
    
    def _update_context_with_result(self, context: ElicitationContext, result: TechniqueResult) -> ElicitationContext:
        """Update context with insights from technique application"""
        # Add result to session history
        context.session_history.append({
            'technique_id': result.technique_id,
            'timestamp': datetime.now().isoformat(),
            'quality_metrics': result.quality_metrics
        })
        return context
    
    def _get_recent_technique_usage(self, technique_id: str, session_history: List[Dict]) -> int:
        """Count recent usage of a technique"""
        return sum(1 for entry in session_history[-10:] if entry.get('technique_id') == technique_id)

class ResponseQualityAssessor:
    """Assesses the quality of elicitation technique applications"""
    
    def assess_enhancement_quality(self, original_query: str, enhanced_prompt: str, technique_id: str) -> Dict[str, float]:
        """Assess how much the technique enhanced the original query"""
        
        # In a real implementation, this would use NLP analysis
        # For now, provide estimated metrics based on technique characteristics
        
        base_metrics = {
            'depth_improvement': 0.0,
            'creativity_enhancement': 0.0,
            'specificity_increase': 0.0,
            'perspective_diversity': 0.0,
            'actionability_boost': 0.0
        }
        
        # Technique-specific quality profiles
        technique_profiles = {
            'chain_of_thought': {'depth_improvement': 0.8, 'specificity_increase': 0.7},
            'alternative_generation': {'creativity_enhancement': 0.9, 'perspective_diversity': 0.8},
            'stakeholder_perspective': {'perspective_diversity': 0.9, 'actionability_boost': 0.7},
            'hierarchical_decomposition': {'depth_improvement': 0.8, 'specificity_increase': 0.9}
        }
        
        # Apply technique-specific enhancements
        profile = technique_profiles.get(technique_id, {})
        for metric, value in profile.items():
            base_metrics[metric] = value
        
        # Calculate overall quality score
        base_metrics['overall_quality'] = sum(base_metrics.values()) / len(base_metrics)
        
        return base_metrics

# Base class for all elicitation techniques
class ElicitationTechnique:
    """Base class for all elicitation techniques"""
    
    def __init__(self, name: str, category: TechniqueCategory, description: str):
        self.name = name
        self.category = category
        self.description = description
        self.usage_count = 0
    
    def apply(self, query: str, context: ElicitationContext) -> str:
        """Apply the technique to enhance the query"""
        self.usage_count += 1
        return self._apply_technique(query, context)
    
    def _apply_technique(self, query: str, context: ElicitationContext) -> str:
        """Override this method in subclasses"""
        raise NotImplementedError("Subclasses must implement _apply_technique")

# Example technique implementations (abbreviated for space)
class ChainOfThoughtTechnique(ElicitationTechnique):
    def __init__(self):
        super().__init__(
            name="Chain of Thought Analysis",
            category=TechniqueCategory.ANALYTICAL,
            description="Elicits step-by-step reasoning and analysis"
        )
    
    def _apply_technique(self, query: str, context: ElicitationContext) -> str:
        return f"""
        Let's approach this systematically, thinking through each step:
        
        Original Query: {query}
        
        Please work through this step-by-step:
        1. First, let's understand what we're trying to achieve
        2. Then, let's identify the key components or factors involved
        3. Next, let's analyze how these components interact
        4. Finally, let's synthesize our findings into a comprehensive response
        
        Think through each step carefully and show your reasoning:
        """

class AlternativeGenerationTechnique(ElicitationTechnique):
    def __init__(self):
        super().__init__(
            name="Alternative Generation",
            category=TechniqueCategory.CREATIVE,
            description="Generates multiple alternative approaches"
        )
    
    def _apply_technique(self, query: str, context: ElicitationContext) -> str:
        return f"""
        Let's generate multiple alternative approaches:
        
        Original Query: {query}
        
        Please provide 5 completely different ways to approach this:
        
        Alternative 1: [Traditional/Conservative approach]
        Alternative 2: [Innovative/Disruptive approach]  
        Alternative 3: [Resource-constrained approach]
        Alternative 4: [Technology-first approach]
        Alternative 5: [User-centric approach]
        
        For each alternative:
        - Describe the core concept
        - Identify unique advantages
        - Note potential challenges
        - Suggest when this approach would be optimal
        """

# Additional technique implementations would follow the same pattern...
