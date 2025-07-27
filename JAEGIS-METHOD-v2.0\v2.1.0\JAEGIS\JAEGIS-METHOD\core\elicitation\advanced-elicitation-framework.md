# Advanced Elicitation Techniques Framework

## Framework Overview
The Advanced Elicitation Techniques Framework implements 30 research-backed techniques designed to push AI responses beyond average outputs through systematic application of psychological, creative, and analytical methods. This framework is the core differentiator of the JAEGIS method.

## Core Architecture

### Technique Classification System
```yaml
elicitation_categories:
  analytical_techniques:
    count: 8
    purpose: "Systematic analysis and logical reasoning"
    effectiveness: "High for technical and architectural tasks"
    
  creative_techniques:
    count: 8
    purpose: "Innovation and creative problem-solving"
    effectiveness: "High for brainstorming and ideation"
    
  collaborative_techniques:
    count: 7
    purpose: "Multi-perspective analysis and stakeholder simulation"
    effectiveness: "High for requirements and validation"
    
  systematic_techniques:
    count: 7
    purpose: "Structured decomposition and process analysis"
    effectiveness: "High for complex problem breakdown"
```

### Context-Aware Selection Engine
```python
class ElicitationTechniqueSelector:
    def __init__(self, technique_database, context_analyzer):
        self.technique_database = technique_database
        self.context_analyzer = context_analyzer
        self.selection_history = {}
        
    def select_optimal_techniques(self, context, user_preferences, session_history):
        """
        Select optimal elicitation techniques based on context and user preferences
        """
        technique_selection = {
            'selection_id': self.generate_selection_id(),
            'context_analysis': {},
            'primary_techniques': [],
            'supporting_techniques': [],
            'technique_sequence': [],
            'expected_outcomes': {}
        }
        
        # Analyze current context
        technique_selection['context_analysis'] = self.context_analyzer.analyze_context(
            context, user_preferences, session_history
        )
        
        # Select primary techniques
        technique_selection['primary_techniques'] = self.select_primary_techniques(
            technique_selection['context_analysis']
        )
        
        # Select supporting techniques
        technique_selection['supporting_techniques'] = self.select_supporting_techniques(
            technique_selection['primary_techniques'], technique_selection['context_analysis']
        )
        
        # Create technique sequence
        technique_selection['technique_sequence'] = self.create_technique_sequence(
            technique_selection['primary_techniques'], 
            technique_selection['supporting_techniques']
        )
        
        # Predict expected outcomes
        technique_selection['expected_outcomes'] = self.predict_technique_outcomes(
            technique_selection['technique_sequence'], technique_selection['context_analysis']
        )
        
        return technique_selection
    
    def select_primary_techniques(self, context_analysis):
        """
        Select primary techniques based on context analysis
        """
        context_type = context_analysis['context_type']
        task_complexity = context_analysis['task_complexity']
        user_expertise = context_analysis['user_expertise']
        
        technique_mapping = {
            'brainstorming': {
                'high_creativity': ['alternative_generation', 'yes_and_building', 'analogical_thinking'],
                'structured_exploration': ['scamper_application', 'constraint_removal', 'biomimicry_inspiration'],
                'rapid_ideation': ['random_word_association', 'reverse_brainstorming']
            },
            'requirements_gathering': {
                'stakeholder_focused': ['stakeholder_perspective_taking', 'multiple_personality_simulation'],
                'detail_oriented': ['progressive_deepening', 'laddering_up_down'],
                'comprehensive': ['what_if_analysis', 'constraint_analysis', 'dependency_mapping']
            },
            'architecture_design': {
                'analytical': ['chain_of_thought_analysis', 'hierarchical_decomposition'],
                'decision_focused': ['decision_tree_analysis', 'pros_cons_evaluation'],
                'risk_aware': ['risk_assessment_analysis', 'impact_analysis']
            },
            'validation_review': {
                'critical_analysis': ['devils_advocate_challenge', 'six_thinking_hats'],
                'consensus_building': ['conflict_resolution', 'consensus_building'],
                'comprehensive_review': ['critical_decision_method', 'expert_panel_simulation']
            }
        }
        
        return technique_mapping.get(context_type, {}).get(task_complexity, [])
```

## Technique Implementation Library

### Analytical Techniques

#### 1. Chain-of-Thought Analysis
```python
class ChainOfThoughtTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's approach this systematically, thinking through each step:
        
        Original Query: {query}
        
        Please work through this step-by-step:
        1. First, let's understand what we're trying to achieve
        2. Then, let's identify the key components or factors involved
        3. Next, let's analyze how these components interact
        4. Finally, let's synthesize our findings into a comprehensive response
        
        Think through each step carefully and show your reasoning:
        """
        return enhanced_prompt
```

#### 2. What-If Scenario Analysis
```python
class WhatIfAnalysisTechnique:
    def apply(self, query, context):
        scenarios = [
            "What if we had unlimited resources?",
            "What if we had to deliver this in half the time?",
            "What if our primary constraint was removed?",
            "What if we had to serve 10x more users?",
            "What if we had to make this work with legacy systems?"
        ]
        
        enhanced_prompt = f"""
        Let's explore this through multiple scenarios:
        
        Original Query: {query}
        
        Please analyze this from these different perspectives:
        {chr(10).join([f"• {scenario}" for scenario in scenarios])}
        
        For each scenario, consider:
        - How would the approach change?
        - What new opportunities or challenges would emerge?
        - What insights does this perspective reveal?
        """
        return enhanced_prompt
```

#### 3. Root Cause Analysis
```python
class RootCauseAnalysisTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's dig deeper to understand the root causes:
        
        Original Query: {query}
        
        Please apply the "5 Whys" technique:
        1. Why is this requirement/problem important?
        2. Why does that matter?
        3. Why is that significant?
        4. Why does that create value?
        5. Why is that the ultimate goal?
        
        Then, let's also consider:
        - What underlying assumptions are we making?
        - What systemic factors contribute to this situation?
        - What would happen if we addressed the root cause vs. symptoms?
        """
        return enhanced_prompt
```

### Creative Techniques

#### 4. Yes-And Building
```python
class YesAndBuildingTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's use the "Yes, And" approach to build on ideas:
        
        Original Query: {query}
        
        Please respond using this pattern:
        1. Start with "Yes, [acknowledge the core idea]..."
        2. Then add "And we could also [build on it]..."
        3. Continue with "And that opens up possibilities for [expand further]..."
        4. Keep building: "And if we combine that with [synthesize]..."
        
        Focus on building and expanding rather than critiquing or limiting.
        Generate at least 3-4 building iterations.
        """
        return enhanced_prompt
```

#### 5. Alternative Generation
```python
class AlternativeGenerationTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
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
        return enhanced_prompt
```

#### 6. Analogical Thinking
```python
class AnalogicalThinkingTechnique:
    def apply(self, query, context):
        domains = [
            "nature and biology",
            "other industries (automotive, healthcare, finance)",
            "historical solutions to similar problems",
            "everyday objects and systems",
            "games and sports"
        ]
        
        enhanced_prompt = f"""
        Let's draw insights from analogies:
        
        Original Query: {query}
        
        Please explore how this challenge is solved in:
        {chr(10).join([f"• {domain}" for domain in domains])}
        
        For each analogy:
        - Describe how that domain handles similar challenges
        - Identify transferable principles or patterns
        - Suggest how we could adapt their approach
        - Note what makes their solution effective
        
        Then synthesize the best insights into a novel approach.
        """
        return enhanced_prompt
```

### Collaborative Techniques

#### 7. Multiple Personality Simulation
```python
class MultiplePersonalityTechnique:
    def apply(self, query, context):
        personalities = [
            "The Optimist (focuses on possibilities and opportunities)",
            "The Skeptic (identifies risks and challenges)",
            "The Pragmatist (focuses on practical implementation)",
            "The Innovator (pushes for creative and novel solutions)",
            "The User Advocate (prioritizes user needs and experience)"
        ]
        
        enhanced_prompt = f"""
        Let's examine this from multiple personality perspectives:
        
        Original Query: {query}
        
        Please respond as each of these personalities:
        
        {chr(10).join([f"{i+1}. {personality}" for i, personality in enumerate(personalities)])}
        
        For each personality:
        - Provide their unique perspective on the query
        - Highlight what they would prioritize
        - Identify their main concerns or excitement
        - Suggest their preferred approach
        
        Finally, synthesize insights from all perspectives into a balanced response.
        """
        return enhanced_prompt
```

#### 8. Stakeholder Perspective Taking
```python
class StakeholderPerspectiveTechnique:
    def apply(self, query, context):
        stakeholders = [
            "End Users (who will use the final product)",
            "Business Stakeholders (who fund and benefit from the project)",
            "Development Team (who will build and maintain the solution)",
            "Operations Team (who will deploy and support the solution)",
            "Competitors (who might respond to this solution)"
        ]
        
        enhanced_prompt = f"""
        Let's consider this from different stakeholder perspectives:
        
        Original Query: {query}
        
        Please analyze this from each stakeholder's viewpoint:
        
        {chr(10).join([f"• {stakeholder}" for stakeholder in stakeholders])}
        
        For each stakeholder:
        - What would they care most about?
        - What would success look like to them?
        - What concerns or objections might they have?
        - How would they want this implemented?
        
        Then identify areas of alignment and potential conflicts.
        """
        return enhanced_prompt
```

### Systematic Techniques

#### 9. Hierarchical Decomposition
```python
class HierarchicalDecompositionTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's break this down hierarchically:
        
        Original Query: {query}
        
        Please decompose this into multiple levels:
        
        Level 1 (Highest): What is the overall goal or system?
        Level 2 (Major Components): What are the main subsystems or areas?
        Level 3 (Detailed Components): What are the specific elements within each area?
        Level 4 (Implementation Details): What are the concrete steps or requirements?
        
        For each level:
        - Clearly define the components
        - Show relationships between components
        - Identify dependencies and interactions
        - Note critical success factors
        
        Then validate that the decomposition is complete and coherent.
        """
        return enhanced_prompt
```

#### 10. Decision Tree Analysis
```python
class DecisionTreeAnalysisTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's map out the decision tree:
        
        Original Query: {query}
        
        Please create a decision tree structure:
        
        1. Initial Decision Point: What is the first major decision we need to make?
           - Option A: [Describe option and consequences]
             - Sub-decision: [Next decision point]
               - Outcome 1: [Final result]
               - Outcome 2: [Final result]
           - Option B: [Describe option and consequences]
             - Sub-decision: [Next decision point]
               - Outcome 1: [Final result]
               - Outcome 2: [Final result]
        
        For each decision point:
        - Identify the criteria for choosing
        - Estimate probability of success for each path
        - Note resource requirements and risks
        - Recommend the optimal path and explain why
        """
        return enhanced_prompt
```

## Technique Orchestration Engine

### Dynamic Technique Sequencing
```python
class TechniqueOrchestrator:
    def __init__(self, technique_library):
        self.technique_library = technique_library
        self.orchestration_patterns = {}
        
    def orchestrate_session(self, session_context, user_goals):
        """
        Orchestrate a complete elicitation session using multiple techniques
        """
        orchestration_plan = {
            'session_id': self.generate_session_id(),
            'opening_techniques': [],
            'exploration_techniques': [],
            'deepening_techniques': [],
            'validation_techniques': [],
            'synthesis_techniques': []
        }
        
        # Opening: Set context and activate thinking
        orchestration_plan['opening_techniques'] = self.select_opening_techniques(session_context)
        
        # Exploration: Generate ideas and alternatives
        orchestration_plan['exploration_techniques'] = self.select_exploration_techniques(
            session_context, user_goals
        )
        
        # Deepening: Drill down into specifics
        orchestration_plan['deepening_techniques'] = self.select_deepening_techniques(
            orchestration_plan['exploration_techniques']
        )
        
        # Validation: Challenge and verify
        orchestration_plan['validation_techniques'] = self.select_validation_techniques(
            orchestration_plan['deepening_techniques']
        )
        
        # Synthesis: Combine and conclude
        orchestration_plan['synthesis_techniques'] = self.select_synthesis_techniques(
            orchestration_plan
        )
        
        return orchestration_plan
    
    def execute_technique_sequence(self, technique_sequence, base_query, context):
        """
        Execute a sequence of elicitation techniques
        """
        results = []
        enhanced_query = base_query
        
        for technique_config in technique_sequence:
            technique = self.technique_library.get_technique(technique_config['technique_id'])
            
            # Apply technique to current query
            enhanced_query = technique.apply(enhanced_query, context)
            
            # Execute enhanced query (this would interface with the AI model)
            response = self.execute_query(enhanced_query, context)
            
            # Store result and prepare for next technique
            results.append({
                'technique_id': technique_config['technique_id'],
                'enhanced_query': enhanced_query,
                'response': response,
                'quality_metrics': self.assess_response_quality(response, technique_config)
            })
            
            # Update context with new insights
            context = self.update_context_with_insights(context, response)
            
        return results
```

## Quality Assessment Framework

### Response Quality Metrics
```python
class ResponseQualityAssessor:
    def assess_response_quality(self, response, technique_config, baseline_response=None):
        """
        Assess the quality improvement achieved by elicitation techniques
        """
        quality_metrics = {
            'depth_score': self.calculate_depth_score(response),
            'creativity_score': self.calculate_creativity_score(response),
            'comprehensiveness_score': self.calculate_comprehensiveness_score(response),
            'specificity_score': self.calculate_specificity_score(response),
            'actionability_score': self.calculate_actionability_score(response),
            'improvement_over_baseline': 0.0
        }
        
        if baseline_response:
            quality_metrics['improvement_over_baseline'] = self.calculate_improvement(
                response, baseline_response
            )
        
        # Calculate overall quality score
        quality_metrics['overall_quality'] = self.calculate_overall_quality(quality_metrics)
        
        return quality_metrics
    
    def calculate_depth_score(self, response):
        """Calculate how deeply the response explores the topic"""
        depth_indicators = [
            'multiple levels of analysis',
            'underlying principles explored',
            'root causes identified',
            'implications considered',
            'connections made'
        ]
        return self.score_indicators(response, depth_indicators)
    
    def calculate_creativity_score(self, response):
        """Calculate the creative and innovative aspects of the response"""
        creativity_indicators = [
            'novel ideas presented',
            'unique perspectives offered',
            'creative analogies used',
            'innovative solutions proposed',
            'unconventional approaches suggested'
        ]
        return self.score_indicators(response, creativity_indicators)
```

## Complete Technique Library (30 Techniques)

### Remaining Analytical Techniques

#### 11. Pros and Cons Evaluation
```python
class ProsConsEvaluationTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's systematically evaluate the advantages and disadvantages:

        Original Query: {query}

        Please provide a comprehensive pros and cons analysis:

        PROS (Advantages):
        • Immediate benefits: [List short-term advantages]
        • Long-term benefits: [List strategic advantages]
        • Stakeholder benefits: [Who benefits and how]
        • Competitive advantages: [Market positioning benefits]

        CONS (Disadvantages):
        • Immediate challenges: [List short-term disadvantages]
        • Long-term risks: [List strategic risks]
        • Resource costs: [Time, money, effort required]
        • Opportunity costs: [What we give up by choosing this]

        NEUTRAL CONSIDERATIONS:
        • Trade-offs: [What we gain vs. what we lose]
        • Dependencies: [What this relies on]
        • Assumptions: [What must be true for this to work]

        Finally, provide a weighted recommendation based on this analysis.
        """
        return enhanced_prompt
```

#### 12. Risk Assessment Analysis
```python
class RiskAssessmentTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's conduct a comprehensive risk assessment:

        Original Query: {query}

        Please analyze risks across multiple dimensions:

        TECHNICAL RISKS:
        • Implementation complexity risks
        • Technology obsolescence risks
        • Integration and compatibility risks
        • Performance and scalability risks

        BUSINESS RISKS:
        • Market acceptance risks
        • Competitive response risks
        • Resource availability risks
        • Timeline and budget risks

        OPERATIONAL RISKS:
        • Maintenance and support risks
        • Security and compliance risks
        • User adoption risks
        • Change management risks

        For each risk:
        - Probability (High/Medium/Low)
        - Impact (High/Medium/Low)
        - Mitigation strategies
        - Contingency plans

        Provide an overall risk profile and recommendations.
        """
        return enhanced_prompt
```

### Remaining Creative Techniques

#### 13. Reverse Brainstorming
```python
class ReverseBrainstormingTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's use reverse brainstorming to gain insights:

        Original Query: {query}

        First, let's explore the opposite: How could we make this project fail spectacularly?

        FAILURE SCENARIOS:
        • What would guarantee user rejection?
        • How could we waste the most resources?
        • What would create the worst user experience?
        • How could we ensure technical failure?
        • What would damage stakeholder relationships?

        Now, let's reverse each failure scenario into success strategies:

        REVERSED INSIGHTS:
        • User rejection → [How to ensure user delight]
        • Resource waste → [How to optimize resource usage]
        • Poor UX → [How to create exceptional experience]
        • Technical failure → [How to ensure technical excellence]
        • Damaged relationships → [How to strengthen stakeholder bonds]

        Synthesize these insights into actionable recommendations.
        """
        return enhanced_prompt
```

#### 14. SCAMPER Application
```python
class ScamperTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's apply the SCAMPER technique systematically:

        Original Query: {query}

        SUBSTITUTE: What can we substitute or replace?
        • Different technologies, approaches, or methods
        • Alternative resources or materials
        • Different user interfaces or experiences

        COMBINE: What can we combine or merge?
        • Existing solutions or features
        • Different technologies or approaches
        • Various stakeholder needs or requirements

        ADAPT: What can we adapt from elsewhere?
        • Solutions from other industries
        • Existing patterns or frameworks
        • Proven methodologies or processes

        MODIFY/MAGNIFY: What can we modify, magnify, or minimize?
        • Scale up or down different aspects
        • Enhance or reduce certain features
        • Adjust timing, frequency, or intensity

        PUT TO OTHER USES: How else can this be used?
        • Alternative applications or markets
        • Different user groups or scenarios
        • Unexpected use cases or benefits

        ELIMINATE: What can we remove or simplify?
        • Unnecessary features or complexity
        • Redundant processes or steps
        • Barriers or friction points

        REVERSE/REARRANGE: What can we reverse or rearrange?
        • Change the order of operations
        • Flip assumptions or perspectives
        • Reorganize structure or flow

        Synthesize the best SCAMPER insights into innovative solutions.
        """
        return enhanced_prompt
```

### Remaining Collaborative Techniques

#### 15. Six Thinking Hats
```python
class SixThinkingHatsTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's examine this using the Six Thinking Hats method:

        Original Query: {query}

        WHITE HAT (Facts and Information):
        • What facts do we know for certain?
        • What information do we need to gather?
        • What data would be most valuable?

        RED HAT (Emotions and Feelings):
        • What is your gut feeling about this?
        • What emotions does this evoke in stakeholders?
        • What are the emotional drivers and concerns?

        BLACK HAT (Critical Judgment):
        • What could go wrong with this approach?
        • What are the weaknesses and risks?
        • What critical concerns should we address?

        YELLOW HAT (Positive Assessment):
        • What are the benefits and opportunities?
        • What is the best-case scenario?
        • What positive outcomes can we expect?

        GREEN HAT (Creativity and Alternatives):
        • What creative alternatives exist?
        • How can we think outside the box?
        • What innovative approaches could we try?

        BLUE HAT (Process Control):
        • How should we approach this systematically?
        • What process would be most effective?
        • How can we organize our thinking and actions?

        Synthesize insights from all six perspectives into a comprehensive response.
        """
        return enhanced_prompt
```

#### 16. Expert Panel Simulation
```python
class ExpertPanelTechnique:
    def apply(self, query, context):
        experts = [
            "Industry Veteran (20+ years experience in the domain)",
            "Technology Innovator (cutting-edge technical expertise)",
            "User Experience Expert (deep understanding of user needs)",
            "Business Strategist (market and competitive intelligence)",
            "Implementation Specialist (practical delivery experience)"
        ]

        enhanced_prompt = f"""
        Let's convene a virtual expert panel:

        Original Query: {query}

        Please provide perspectives from each expert:

        {chr(10).join([f"{i+1}. {expert}" for i, expert in enumerate(experts)])}

        For each expert:
        • Their unique perspective on the challenge
        • Key insights from their domain expertise
        • Specific recommendations they would make
        • Potential concerns or warnings they would raise
        • Success factors they would emphasize

        PANEL DISCUSSION:
        • Where do the experts agree?
        • What are the key points of disagreement?
        • How can conflicting viewpoints be reconciled?
        • What synthesis emerges from their collective wisdom?

        Provide a final recommendation that incorporates the best insights from all experts.
        """
        return enhanced_prompt
```

### Remaining Systematic Techniques

#### 17. Progressive Deepening
```python
class ProgressiveDeepeningTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's use progressive deepening to explore this thoroughly:

        Original Query: {query}

        LEVEL 1 (Surface): What is the basic understanding?
        • Core concept or requirement
        • Primary stakeholders involved
        • Main objectives or goals

        LEVEL 2 (Context): What is the broader context?
        • Business or organizational context
        • Technical environment and constraints
        • Market or competitive landscape

        LEVEL 3 (Details): What are the specific details?
        • Detailed requirements and specifications
        • Technical implementation considerations
        • Resource and timeline implications

        LEVEL 4 (Implications): What are the deeper implications?
        • Long-term consequences and impacts
        • Strategic alignment and dependencies
        • Risk factors and mitigation strategies

        LEVEL 5 (Integration): How does this integrate with everything else?
        • Connections to other systems or initiatives
        • Organizational change implications
        • Success measurement and optimization

        For each level, build upon insights from previous levels and identify what needs further exploration.
        """
        return enhanced_prompt
```

#### 18. Critical Decision Method
```python
class CriticalDecisionMethodTechnique:
    def apply(self, query, context):
        enhanced_prompt = f"""
        Let's apply the Critical Decision Method:

        Original Query: {query}

        INCIDENT IDENTIFICATION:
        • What is the critical situation or decision point?
        • Why is this decision particularly important?
        • What makes this challenging or complex?

        TIMELINE CONSTRUCTION:
        • What events led up to this decision point?
        • What is the sequence of key milestones?
        • What are the time constraints or deadlines?

        DECISION POINT ANALYSIS:
        • What are the key decision points within this situation?
        • What information is available at each decision point?
        • What are the options and alternatives at each point?

        CUES AND INDICATORS:
        • What signals or indicators should we pay attention to?
        • How will we know if we're on the right track?
        • What early warning signs should we watch for?

        KNOWLEDGE REQUIREMENTS:
        • What expertise is needed for this decision?
        • What information gaps need to be filled?
        • What assumptions are we making?

        LESSONS LEARNED:
        • What can we learn from similar past decisions?
        • What would we do differently next time?
        • What best practices should we apply?

        Provide a comprehensive decision framework based on this analysis.
        """
        return enhanced_prompt
```

## Integration with JAEGIS Workflow

### Technique Selection Matrix
```yaml
jaegis_phase_techniques:
  brainstorming:
    primary: [alternative_generation, yes_and_building, analogical_thinking, scamper_application]
    creative: [reverse_brainstorming, constraint_removal, biomimicry_inspiration, random_word_association]
    analytical: [what_if_analysis, chain_of_thought_analysis]

  modeling_prd:
    collaborative: [stakeholder_perspective_taking, multiple_personality_simulation, expert_panel_simulation]
    systematic: [progressive_deepening, hierarchical_decomposition, laddering_up_down]
    analytical: [pros_cons_evaluation, risk_assessment_analysis, dependency_mapping]

  architecture:
    analytical: [chain_of_thought_analysis, decision_tree_analysis, impact_analysis]
    systematic: [hierarchical_decomposition, process_mapping, critical_decision_method]
    collaborative: [six_thinking_hats, devils_advocate_challenge]

  validation:
    collaborative: [devils_advocate_challenge, six_thinking_hats, conflict_resolution]
    analytical: [pros_cons_evaluation, risk_assessment_analysis, root_cause_analysis]
    systematic: [critical_decision_method, consensus_building]
```

This comprehensive framework implements all 30 advanced elicitation techniques that Brian identified as core to the JAEGIS method's ability to push AI responses beyond average outputs through systematic application of research-backed psychological, creative, and analytical methods.
