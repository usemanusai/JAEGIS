"""
JAEGIS Agentic Template Instructions System
Implements interactive templates with embedded AI instructions for dynamic user engagement
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import yaml

class InteractionType(Enum):
    QUESTION = "question"
    BRAINSTORM = "brainstorm"
    ANALYZE = "analyze"
    VALIDATE = "validate"
    SUGGEST = "suggest"
    CLARIFY = "clarify"

class UserExpertiseLevel(Enum):
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

class TemplateState(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VALIDATED = "validated"

@dataclass
class AgenticInstruction:
    """Individual agentic instruction within a template section"""
    instruction_id: str
    instruction_type: InteractionType
    instruction_text: str
    elicitation_techniques: List[str]
    expected_interaction: str
    context_conditions: Dict[str, Any] = field(default_factory=dict)
    personalization_rules: Dict[str, Any] = field(default_factory=dict)
    validation_criteria: List[str] = field(default_factory=list)

@dataclass
class TemplateSection:
    """Individual section of an agentic template"""
    section_id: str
    section_name: str
    section_description: str
    agentic_instructions: List[AgenticInstruction]
    prerequisites: List[str] = field(default_factory=list)
    completion_criteria: List[str] = field(default_factory=list)
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    state: TemplateState = TemplateState.NOT_STARTED

@dataclass
class AgenticTemplate:
    """Complete agentic template with embedded AI instructions"""
    template_id: str
    template_name: str
    template_type: str
    template_description: str
    version: str
    sections: List[TemplateSection]
    global_context: Dict[str, Any] = field(default_factory=dict)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    interaction_history: List[Dict] = field(default_factory=list)

@dataclass
class UserInteractionContext:
    """Context for user interaction with template"""
    user_id: str
    session_id: str
    expertise_level: UserExpertiseLevel
    domain_knowledge: List[str]
    interaction_preferences: Dict[str, Any]
    current_section: str
    progress_metrics: Dict[str, float] = field(default_factory=dict)

class AgenticTemplateEngine:
    """Main engine for managing agentic template interactions"""
    
    def __init__(self):
        self.template_library = {}
        self.elicitation_engine = None  # Would integrate with advanced elicitation framework
        self.personalization_engine = PersonalizationEngine()
        self.quality_assessor = TemplateQualityAssessor()
        
    def load_template(self, template_config: Dict[str, Any]) -> AgenticTemplate:
        """Load template from configuration"""
        
        # Parse sections
        sections = []
        for section_config in template_config.get('sections', []):
            instructions = []
            
            for instruction_config in section_config.get('agentic_instructions', []):
                instruction = AgenticInstruction(
                    instruction_id=instruction_config['instruction_id'],
                    instruction_type=InteractionType(instruction_config['instruction_type']),
                    instruction_text=instruction_config['instruction_text'],
                    elicitation_techniques=instruction_config.get('elicitation_techniques', []),
                    expected_interaction=instruction_config['expected_interaction'],
                    context_conditions=instruction_config.get('context_conditions', {}),
                    personalization_rules=instruction_config.get('personalization_rules', {}),
                    validation_criteria=instruction_config.get('validation_criteria', [])
                )
                instructions.append(instruction)
            
            section = TemplateSection(
                section_id=section_config['section_id'],
                section_name=section_config['section_name'],
                section_description=section_config['section_description'],
                agentic_instructions=instructions,
                prerequisites=section_config.get('prerequisites', []),
                completion_criteria=section_config.get('completion_criteria', [])
            )
            sections.append(section)
        
        template = AgenticTemplate(
            template_id=template_config['template_id'],
            template_name=template_config['template_name'],
            template_type=template_config['template_type'],
            template_description=template_config['template_description'],
            version=template_config['version'],
            sections=sections,
            global_context=template_config.get('global_context', {})
        )
        
        self.template_library[template.template_id] = template
        return template
    
    def start_template_session(self, template_id: str, user_context: UserInteractionContext) -> Dict[str, Any]:
        """Start interactive template session"""
        
        template = self.template_library.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Initialize session
        session_data = {
            'session_id': user_context.session_id,
            'template_id': template_id,
            'user_context': user_context,
            'current_section_index': 0,
            'section_responses': {},
            'interaction_log': [],
            'quality_metrics': {},
            'personalization_applied': {}
        }
        
        # Personalize template for user
        personalized_template = self.personalization_engine.personalize_template(template, user_context)
        session_data['personalized_template'] = personalized_template
        
        # Start with first section
        first_section_interaction = self._initiate_section_interaction(
            personalized_template.sections[0], user_context, session_data
        )
        
        return {
            'session_data': session_data,
            'current_interaction': first_section_interaction,
            'progress': self._calculate_progress(session_data),
            'next_steps': self._generate_next_steps(session_data)
        }
    
    def process_user_response(self, session_data: Dict[str, Any], user_response: str) -> Dict[str, Any]:
        """Process user response and generate next interaction"""
        
        template = session_data['personalized_template']
        current_section_index = session_data['current_section_index']
        current_section = template.sections[current_section_index]
        
        # Log interaction
        interaction_log_entry = {
            'timestamp': datetime.now().isoformat(),
            'section_id': current_section.section_id,
            'user_response': user_response,
            'interaction_type': 'user_response'
        }
        session_data['interaction_log'].append(interaction_log_entry)
        
        # Process response with current section
        processing_result = self._process_section_response(
            current_section, user_response, session_data
        )
        
        # Update session data
        session_data['section_responses'][current_section.section_id] = processing_result['section_data']
        
        # Determine next interaction
        if processing_result['section_complete']:
            # Move to next section or complete template
            if current_section_index + 1 < len(template.sections):
                session_data['current_section_index'] += 1
                next_section = template.sections[session_data['current_section_index']]
                next_interaction = self._initiate_section_interaction(
                    next_section, session_data['user_context'], session_data
                )
            else:
                # Template complete
                next_interaction = self._generate_completion_interaction(session_data)
        else:
            # Continue with current section
            next_interaction = self._continue_section_interaction(
                current_section, processing_result, session_data
            )
        
        return {
            'session_data': session_data,
            'current_interaction': next_interaction,
            'progress': self._calculate_progress(session_data),
            'quality_feedback': processing_result.get('quality_feedback', {}),
            'suggestions': processing_result.get('suggestions', [])
        }
    
    def _initiate_section_interaction(self, section: TemplateSection, user_context: UserInteractionContext, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate interaction with a template section"""
        
        # Select first instruction for section
        first_instruction = section.agentic_instructions[0] if section.agentic_instructions else None
        
        if not first_instruction:
            return {
                'interaction_type': 'section_complete',
                'message': f"Section '{section.section_name}' has no instructions.",
                'section_id': section.section_id
            }
        
        # Personalize instruction
        personalized_instruction = self.personalization_engine.personalize_instruction(
            first_instruction, user_context
        )
        
        # Generate interaction
        interaction = {
            'interaction_type': first_instruction.instruction_type.value,
            'section_id': section.section_id,
            'section_name': section.section_name,
            'instruction_id': first_instruction.instruction_id,
            'message': personalized_instruction['instruction_text'],
            'expected_interaction': personalized_instruction['expected_interaction'],
            'context': {
                'section_description': section.section_description,
                'elicitation_techniques': first_instruction.elicitation_techniques,
                'validation_criteria': first_instruction.validation_criteria
            },
            'suggestions': personalized_instruction.get('suggestions', []),
            'examples': personalized_instruction.get('examples', [])
        }
        
        return interaction
    
    def _process_section_response(self, section: TemplateSection, user_response: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user response within a section"""
        
        # Analyze response quality
        quality_analysis = self.quality_assessor.analyze_response_quality(
            user_response, section, session_data
        )
        
        # Determine if section is complete
        section_complete = self._check_section_completion(section, session_data)
        
        # Generate suggestions for improvement
        suggestions = self._generate_improvement_suggestions(
            user_response, section, quality_analysis
        )
        
        # Update section data
        section_data = session_data['section_responses'].get(section.section_id, {})
        section_data['responses'] = section_data.get('responses', [])
        section_data['responses'].append({
            'response': user_response,
            'timestamp': datetime.now().isoformat(),
            'quality_metrics': quality_analysis
        })
        
        return {
            'section_complete': section_complete,
            'section_data': section_data,
            'quality_feedback': quality_analysis,
            'suggestions': suggestions
        }
    
    def _continue_section_interaction(self, section: TemplateSection, processing_result: Dict[str, Any], session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Continue interaction within current section"""
        
        # Determine next instruction or follow-up
        current_responses = len(processing_result['section_data'].get('responses', []))
        
        if current_responses < len(section.agentic_instructions):
            # Move to next instruction
            next_instruction = section.agentic_instructions[current_responses]
            
            personalized_instruction = self.personalization_engine.personalize_instruction(
                next_instruction, session_data['user_context']
            )
            
            return {
                'interaction_type': next_instruction.instruction_type.value,
                'section_id': section.section_id,
                'instruction_id': next_instruction.instruction_id,
                'message': personalized_instruction['instruction_text'],
                'expected_interaction': personalized_instruction['expected_interaction'],
                'context': {
                    'elicitation_techniques': next_instruction.elicitation_techniques,
                    'validation_criteria': next_instruction.validation_criteria
                },
                'quality_feedback': processing_result.get('quality_feedback', {}),
                'suggestions': processing_result.get('suggestions', [])
            }
        else:
            # Generate follow-up or refinement interaction
            return self._generate_refinement_interaction(section, processing_result, session_data)
    
    def _generate_refinement_interaction(self, section: TemplateSection, processing_result: Dict[str, Any], session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate refinement interaction for section improvement"""
        
        quality_feedback = processing_result.get('quality_feedback', {})
        suggestions = processing_result.get('suggestions', [])
        
        refinement_message = f"Great work on the '{section.section_name}' section! "
        
        if suggestions:
            refinement_message += "I have some suggestions to make it even better:\n\n"
            for i, suggestion in enumerate(suggestions, 1):
                refinement_message += f"{i}. {suggestion}\n"
            refinement_message += "\nWould you like to refine any of these aspects, or shall we move on?"
        else:
            refinement_message += "Your responses look comprehensive. Ready to move to the next section?"
        
        return {
            'interaction_type': 'validate',
            'section_id': section.section_id,
            'message': refinement_message,
            'expected_interaction': 'User can choose to refine responses or proceed',
            'context': {
                'quality_feedback': quality_feedback,
                'suggestions': suggestions,
                'refinement_options': ['refine', 'proceed']
            }
        }
    
    def _check_section_completion(self, section: TemplateSection, session_data: Dict[str, Any]) -> bool:
        """Check if section completion criteria are met"""
        
        section_data = session_data['section_responses'].get(section.section_id, {})
        responses = section_data.get('responses', [])
        
        # Basic completion: all instructions have responses
        if len(responses) < len(section.agentic_instructions):
            return False
        
        # Quality-based completion
        if section.completion_criteria:
            for criterion in section.completion_criteria:
                if not self._evaluate_completion_criterion(criterion, section_data):
                    return False
        
        return True
    
    def _calculate_progress(self, session_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate template completion progress"""
        
        template = session_data['personalized_template']
        total_sections = len(template.sections)
        completed_sections = len([s for s in session_data['section_responses'].keys()])
        current_section_index = session_data['current_section_index']
        
        return {
            'overall_progress': completed_sections / total_sections if total_sections > 0 else 0.0,
            'current_section_progress': (current_section_index + 1) / total_sections if total_sections > 0 else 0.0,
            'sections_completed': completed_sections,
            'total_sections': total_sections
        }

class PersonalizationEngine:
    """Handles personalization of templates and instructions"""
    
    def personalize_template(self, template: AgenticTemplate, user_context: UserInteractionContext) -> AgenticTemplate:
        """Personalize entire template for user"""
        
        personalized_sections = []
        for section in template.sections:
            personalized_instructions = []
            
            for instruction in section.agentic_instructions:
                personalized_instruction = self.personalize_instruction(instruction, user_context)
                personalized_instructions.append(personalized_instruction)
            
            personalized_section = TemplateSection(
                section_id=section.section_id,
                section_name=section.section_name,
                section_description=section.section_description,
                agentic_instructions=personalized_instructions,
                prerequisites=section.prerequisites,
                completion_criteria=section.completion_criteria
            )
            personalized_sections.append(personalized_section)
        
        personalized_template = AgenticTemplate(
            template_id=template.template_id,
            template_name=template.template_name,
            template_type=template.template_type,
            template_description=template.template_description,
            version=template.version,
            sections=personalized_sections,
            global_context=template.global_context,
            user_preferences=user_context.interaction_preferences
        )
        
        return personalized_template
    
    def personalize_instruction(self, instruction: AgenticInstruction, user_context: UserInteractionContext) -> Dict[str, Any]:
        """Personalize individual instruction for user"""
        
        personalized = {
            'instruction_text': instruction.instruction_text,
            'expected_interaction': instruction.expected_interaction,
            'suggestions': [],
            'examples': []
        }
        
        # Adjust based on expertise level
        if user_context.expertise_level == UserExpertiseLevel.NOVICE:
            personalized['instruction_text'] = self._add_beginner_guidance(instruction.instruction_text)
            personalized['examples'] = self._generate_beginner_examples(instruction)
        elif user_context.expertise_level == UserExpertiseLevel.EXPERT:
            personalized['instruction_text'] = self._make_concise_for_expert(instruction.instruction_text)
            personalized['suggestions'] = self._generate_expert_suggestions(instruction)
        
        # Apply personalization rules
        for rule_type, rule_config in instruction.personalization_rules.items():
            if rule_type == 'domain_specific' and user_context.domain_knowledge:
                personalized = self._apply_domain_personalization(personalized, rule_config, user_context.domain_knowledge)
        
        return personalized
    
    def _add_beginner_guidance(self, instruction_text: str) -> str:
        """Add guidance for novice users"""
        return f"{instruction_text}\n\n💡 Tip: Take your time and don't worry about getting it perfect on the first try. I'm here to help you refine your thoughts."
    
    def _make_concise_for_expert(self, instruction_text: str) -> str:
        """Make instruction more concise for expert users"""
        # Simplified implementation - would use NLP to identify and remove verbose explanations
        return instruction_text.replace("Please take your time to", "").replace("Don't worry if you're not sure,", "")

class TemplateQualityAssessor:
    """Assesses quality of template responses and interactions"""
    
    def analyze_response_quality(self, response: str, section: TemplateSection, session_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze quality of user response"""
        
        # Simplified quality metrics - would use NLP analysis in real implementation
        quality_metrics = {
            'completeness': self._assess_completeness(response, section),
            'clarity': self._assess_clarity(response),
            'specificity': self._assess_specificity(response),
            'relevance': self._assess_relevance(response, section),
            'actionability': self._assess_actionability(response)
        }
        
        quality_metrics['overall_quality'] = sum(quality_metrics.values()) / len(quality_metrics)
        
        return quality_metrics
    
    def _assess_completeness(self, response: str, section: TemplateSection) -> float:
        """Assess completeness of response"""
        # Simplified implementation
        word_count = len(response.split())
        if word_count < 10:
            return 0.3
        elif word_count < 50:
            return 0.6
        else:
            return 0.9
    
    def _assess_clarity(self, response: str) -> float:
        """Assess clarity of response"""
        # Simplified implementation
        sentence_count = response.count('.') + response.count('!') + response.count('?')
        word_count = len(response.split())
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        if avg_sentence_length > 30:
            return 0.4  # Too long sentences
        elif avg_sentence_length < 5:
            return 0.6  # Too short sentences
        else:
            return 0.9  # Good sentence length

# Example template configuration
EXAMPLE_PRD_TEMPLATE = {
    "template_id": "prd_template_v1",
    "template_name": "Product Requirements Document",
    "template_type": "prd",
    "template_description": "Interactive template for creating comprehensive Product Requirements Documents",
    "version": "1_0_0global_context": {
        "document_type": "PRD",
        "collaboration_mode": "human_ai_partnership"
    },
    "sections": [
        {
            "section_id": "executive_summary",
            "section_name": "Executive Summary",
            "section_description": "High-level overview of the product and its value proposition",
            "agentic_instructions": [
                {
                    "instruction_id": "exec_summary_intro",
                    "instruction_type": "question",
                    "instruction_text": "Let's start with the big picture. What problem does your product solve, and who experiences this problem?",
                    "elicitation_techniques": ["stakeholder_perspective_taking", "problem_exploration"],
                    "expected_interaction": "User describes the core problem and target audience",
                    "validation_criteria": ["clear_problem_statement", "identified_target_audience"]
                },
                {
                    "instruction_id": "exec_summary_solution",
                    "instruction_type": "brainstorm",
                    "instruction_text": "Now let's explore your solution. What makes your approach unique? Let's brainstorm the key differentiators.",
                    "elicitation_techniques": ["alternative_generation", "competitive_analysis"],
                    "expected_interaction": "Collaborative exploration of solution uniqueness and competitive advantages",
                    "validation_criteria": ["unique_value_proposition", "competitive_differentiation"]
                }
            ],
            "completion_criteria": ["problem_clearly_defined", "solution_articulated", "value_proposition_clear"]
        }
    ]
}
