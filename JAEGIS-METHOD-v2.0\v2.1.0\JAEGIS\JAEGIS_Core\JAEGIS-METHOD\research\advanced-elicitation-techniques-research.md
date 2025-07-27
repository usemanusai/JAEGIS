# Advanced Elicitation Techniques Research

## Research Overview
This document compiles comprehensive research on advanced prompting techniques, psychological elicitation methods, and best practices for enhancing AI response quality, based on current academic literature and industry practices.

## Core Research Findings

### 1. Advanced Prompting Techniques

#### Chain-of-Thought (CoT) Prompting
**Source**: Large Language Models are Zero-Shot Reasoners (Kojima et al., 2022)
- **Description**: Elicits complex multi-step reasoning by encouraging the model to show its work
- **Implementation**: Add "Let's think step by step" or provide reasoning examples
- **Effectiveness**: Significantly improves performance on reasoning tasks
- **JAEGIS Application**: Ideal for architecture design, problem decomposition, and technical analysis

#### Few-Shot Prompting with Examples
**Source**: Multiple academic sources on prompt engineering
- **Description**: Provides 2-5 examples of desired input-output patterns
- **Implementation**: Include relevant examples before the actual query
- **Effectiveness**: Improves task understanding and output consistency
- **JAEGIS Application**: Template completion, document formatting, specific deliverable creation

#### Role-Based Prompting (Persona Simulation)
**Source**: Role Prompting: Guide LLMs with Persona-Based Tasks (LearnPrompting.org)
- **Description**: Assigns specific roles or personas to guide AI behavior
- **Implementation**: "You are a [specific role] with [specific expertise]..."
- **Effectiveness**: Enhances domain-specific knowledge application
- **JAEGIS Application**: Stakeholder perspective simulation, expert consultation simulation

#### Zero-Shot Prompting Enhancements
**Source**: Introduction to Advanced Zero-Shot Prompting Techniques (LearnPrompting.org)
- **Emotion Prompting**: Adding emotional context to improve engagement
- **Re-reading Prompting**: Asking the model to re-read and reconsider
- **Self-Consistency**: Generating multiple responses and selecting the best
- **JAEGIS Application**: Initial brainstorming, creative ideation, quality validation

### 2. Psychological Elicitation Methods

#### Divergent-Convergent Thinking Cycles
**Source**: Convergent thinking? Divergent thinking? Creativity calls for both (InStoryMode, 2021)
- **Divergent Phase**: Generate multiple ideas without judgment
- **Convergent Phase**: Evaluate, refine, and select best options
- **Psychological Basis**: Guilford's Structure of Intellect model (1956)
- **JAEGIS Application**: Brainstorming sessions, feature ideation, solution exploration

#### SCAMPER Technique
**Source**: A Guide to the SCAMPER Technique for Design Thinking (Designorate)
- **S**ubstitute: What can be substituted?
- **C**ombine: What can be combined?
- **A**dapt: What can be adapted?
- **M**odify: What can be modified or magnified?
- **P**ut to other uses: How else can this be used?
- **E**liminate: What can be removed?
- **R**everse: What can be reversed or rearranged?
- **JAEGIS Application**: Feature enhancement, problem-solving, innovation generation

#### Six Thinking Hats Method
**Source**: Six Thinking Hats - Problem Solving & Brainstorming Techniques (GroupMap)
- **White Hat**: Facts and information
- **Red Hat**: Emotions and feelings
- **Black Hat**: Critical judgment and caution
- **Yellow Hat**: Positive assessment and optimism
- **Green Hat**: Creativity and alternatives
- **Blue Hat**: Process control and thinking about thinking
- **JAEGIS Application**: Comprehensive analysis, stakeholder perspective simulation, decision-making

#### Critical Decision Method (CDM)
**Source**: Use of the Critical Decision Method to Elicit Expert Knowledge (Hoffman et al., 1998)
- **Description**: Structured interview technique for extracting expert knowledge
- **Process**: Incident selection → Timeline construction → Decision point identification → Progressive deepening
- **JAEGIS Application**: Requirements gathering, architecture decision documentation, lessons learned capture

### 3. Creative Problem-Solving Techniques

#### "What If" Analysis
**Research Basis**: Scenario planning and futures thinking methodologies
- **Implementation**: Systematic exploration of alternative scenarios
- **Variations**: "What if we removed this constraint?", "What if we had unlimited resources?"
- **JAEGIS Application**: Risk assessment, opportunity identification, innovation exploration

#### "Yes, And" Methodology
**Source**: Improvisational theater and creative collaboration techniques
- **Principle**: Build on ideas rather than rejecting them
- **Implementation**: Always acknowledge the previous idea before adding to it
- **JAEGIS Application**: Collaborative ideation, feature building, solution enhancement

#### Analogical Reasoning
**Source**: Cognitive psychology research on problem-solving
- **Description**: Drawing insights from parallel domains or situations
- **Implementation**: "How do other industries solve similar problems?"
- **JAEGIS Application**: Innovation inspiration, solution adaptation, best practice identification

#### Reverse Brainstorming
**Source**: Creative thinking methodologies
- **Description**: Focus on how to cause the problem rather than solve it
- **Implementation**: "How could we make this project fail?" then reverse the insights
- **JAEGIS Application**: Risk identification, failure prevention, quality assurance

### 4. Multi-Perspective Simulation Techniques

#### Stakeholder Perspective Taking
**Source**: Design thinking and user-centered design methodologies
- **Implementation**: Systematically adopt different stakeholder viewpoints
- **Perspectives**: End users, business stakeholders, technical teams, competitors
- **JAEGIS Application**: Requirements validation, feature prioritization, user story development

#### Devil's Advocate Approach
**Source**: Critical thinking and decision-making research
- **Implementation**: Systematically challenge assumptions and proposals
- **Benefits**: Identifies weaknesses, improves robustness, prevents groupthink
- **JAEGIS Application**: Architecture review, risk assessment, quality validation

#### Multiple Personality Simulation
**Source**: Role-playing and perspective-taking research
- **Implementation**: AI adopts different personality types or thinking styles
- **Variations**: Optimist/pessimist, creative/analytical, user/developer perspectives
- **JAEGIS Application**: Comprehensive analysis, balanced decision-making, stakeholder simulation

### 5. Knowledge Elicitation from Expert Systems Research

#### Structured Interview Techniques
**Source**: Knowledge elicitation techniques for expert systems (Gammack & Young, 1985)
- **Laddering**: Moving up and down levels of abstraction
- **Repertory Grid**: Systematic comparison of concepts
- **Protocol Analysis**: Think-aloud during problem-solving
- **JAEGIS Application**: Requirements gathering, expertise capture, knowledge transfer

#### Cognitive Task Analysis
**Source**: Human factors contributions to knowledge elicitation (Seamster et al., 2008)
- **Description**: Understanding how experts perform complex cognitive tasks
- **Methods**: Critical incident technique, cognitive walkthroughs, concept mapping
- **JAEGIS Application**: Workflow analysis, process optimization, skill transfer

#### Progressive Deepening
**Source**: Methods for eliciting expert knowledge (Hart, 1986)
- **Description**: Iteratively drilling down into increasing levels of detail
- **Implementation**: Start broad, then progressively focus on specific aspects
- **JAEGIS Application**: Requirements refinement, architecture detailing, implementation planning

## Synthesis: 30 Advanced Elicitation Techniques for JAEGIS

### Analytical Techniques (8 techniques)
1. **Chain-of-Thought Analysis**: "Let's think through this step by step"
2. **Root Cause Analysis**: "What are the underlying causes of this requirement?"
3. **What-If Scenario Analysis**: "What if we changed this fundamental assumption?"
4. **Pros and Cons Evaluation**: "Let's systematically evaluate the advantages and disadvantages"
5. **Risk Assessment Analysis**: "What could go wrong and how likely is it?"
6. **Impact Analysis**: "What would be the ripple effects of this decision?"
7. **Constraint Analysis**: "What limitations do we need to work within?"
8. **Dependency Mapping**: "What does this depend on and what depends on this?"

### Creative Techniques (8 techniques)
9. **Yes-And Building**: "Yes, and we could also..."
10. **Alternative Generation**: "What are 5 completely different ways to approach this?"
11. **Reverse Brainstorming**: "How could we make this project fail?"
12. **Analogical Thinking**: "How do other industries solve similar problems?"
13. **Random Word Association**: "How does [random concept] relate to our challenge?"
14. **SCAMPER Application**: Systematic application of substitute, combine, adapt, modify, etc.
15. **Biomimicry Inspiration**: "How does nature solve similar problems?"
16. **Constraint Removal**: "What if we had no limitations?"

### Collaborative Techniques (7 techniques)
17. **Multiple Personality Simulation**: "Let's consider this from an optimist's vs. pessimist's perspective"
18. **Stakeholder Perspective Taking**: "How would the end user view this requirement?"
19. **Devil's Advocate Challenge**: "Let me challenge this assumption..."
20. **Six Thinking Hats**: Systematic exploration using different thinking modes
21. **Expert Panel Simulation**: "Let's convene a virtual panel of experts"
22. **Consensus Building**: "How can we find common ground between these viewpoints?"
23. **Conflict Resolution**: "How do we resolve the tension between these requirements?"

### Systematic Techniques (7 techniques)
24. **Hierarchical Decomposition**: "Let's break this down into smaller components"
25. **Process Mapping**: "What's the step-by-step flow of this process?"
26. **Decision Tree Analysis**: "What are all the decision points and their outcomes?"
27. **Priority Matrix Evaluation**: "Let's rank these by importance and urgency"
28. **Progressive Deepening**: "Let's start broad and drill down into specifics"
29. **Laddering Up/Down**: "Let's explore this at higher and lower levels of abstraction"
30. **Critical Decision Method**: "Let's identify the key decision points and explore them deeply"

## Implementation Guidelines for JAEGIS

### Context-Based Technique Selection
```yaml
technique_mapping:
  brainstorming_phase:
    primary: [alternative_generation, yes_and_building, analogical_thinking, constraint_removal]
    supporting: [random_word_association, biomimicry_inspiration, reverse_brainstorming]
    
  requirements_gathering:
    primary: [stakeholder_perspective_taking, progressive_deepening, laddering_up_down]
    supporting: [what_if_analysis, constraint_analysis, dependency_mapping]
    
  architecture_design:
    primary: [chain_of_thought_analysis, hierarchical_decomposition, decision_tree_analysis]
    supporting: [risk_assessment, impact_analysis, expert_panel_simulation]
    
  validation_review:
    primary: [devils_advocate_challenge, six_thinking_hats, pros_cons_evaluation]
    supporting: [critical_decision_method, conflict_resolution, consensus_building]
```

### Quality Enhancement Metrics
- **Response Depth**: Measure of detail and thoroughness in AI responses
- **Perspective Diversity**: Number of different viewpoints considered
- **Creative Novelty**: Degree of innovative thinking demonstrated
- **Analytical Rigor**: Depth of logical analysis and reasoning
- **Collaborative Engagement**: Level of human-AI interaction and co-creation

## Next Steps for Implementation
1. **Technique Categorization**: Organize techniques by use case and effectiveness
2. **Context-Aware Selection**: Develop algorithms for automatic technique selection
3. **User Training**: Create guides for humans to effectively use these techniques
4. **Performance Measurement**: Establish metrics for technique effectiveness
5. **Continuous Improvement**: Iteratively refine techniques based on usage data

This research provides the foundation for implementing the advanced elicitation techniques that Brian identified as core to the JAEGIS method's effectiveness in pushing AI beyond average responses.
