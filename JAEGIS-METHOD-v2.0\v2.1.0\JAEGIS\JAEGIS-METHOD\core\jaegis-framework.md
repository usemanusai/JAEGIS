# JAEGIS Method Framework - Core Implementation

## Framework Overview
The JAEGIS (Brainstorming, Modeling, Architecture, Development) Method is a comprehensive framework for human-AI collaborative software development that emphasizes structured processes, advanced elicitation techniques, and multi-agent coordination.

## Core Principles

### 1. Human-AI Collaboration
- **Not "Vibe Coding"**: Structured approach requiring active human participation
- **Collaborative Intelligence**: Humans and AI working together to produce better outcomes than either could achieve alone
- **Active Engagement**: Users don't "check their brain at the door" - continuous collaboration required

### 2. Multi-Agent Team Approach
- **Agile Team of Agents**: Multiple specialized agents working together
- **Coordinated Workflow**: Seamless handoffs between agents and phases
- **Holistic Development**: End-to-end support from ideation to delivery

### 3. Advanced Elicitation Techniques
- **Beyond Average Responses**: 20-30 specialized techniques to push AI beyond generic outputs
- **Context-Aware Prompting**: Techniques selected based on document section and context
- **Psychological-Backed Methods**: Science-based approaches to enhance AI reasoning

## Core Agents

### Primary JAEGIS Agents
```yaml
brainstorming_agent:
  name: "Brainstorming Specialist"
  role: "Facilitates ideation using psychology-backed techniques"
  capabilities:
    - Science-backed brainstorming methodologies
    - Interactive idea generation
    - Creative problem-solving facilitation
    - Collaborative ideation sessions

product_manager_agent:
  name: "Product Manager (PM)"
  role: "Creates comprehensive Product Requirements Documents"
  capabilities:
    - PRD creation and refinement
    - Stakeholder requirement gathering
    - Feature prioritization
    - User story development

architect_agent:
  name: "System Architect"
  role: "Designs technical architecture and system specifications"
  capabilities:
    - Architecture document creation
    - Technical specification development
    - System design patterns
    - Technology stack recommendations

development_agent:
  name: "Development Coordinator"
  role: "Manages development process and code generation"
  capabilities:
    - Development planning
    - Code generation coordination
    - Quality assurance oversight
    - Deployment preparation
```

### Supporting Agents
```yaml
elicitation_agent:
  name: "Advanced Elicitation Specialist"
  role: "Applies advanced prompting techniques to enhance AI responses"
  capabilities:
    - 20-30 specialized elicitation techniques
    - Context-aware technique selection
    - Response quality enhancement
    - Multi-perspective analysis

template_agent:
  name: "Agentic Template Manager"
  role: "Manages interactive templates with embedded instructions"
  capabilities:
    - Dynamic template generation
    - Interactive user engagement
    - Context-sensitive questioning
    - Collaborative document creation

expansion_agent:
  name: "Expansion Pack Manager"
  role: "Manages domain-specific expansion packs"
  capabilities:
    - Expansion pack loading and management
    - Domain-specific agent coordination
    - Specialized workflow execution
    - Custom template integration
```

## Workflow Phases

### Phase 1: Brainstorming
```yaml
brainstorming_phase:
  description: "Interactive ideation using psychology-backed techniques"
  agents: [brainstorming_agent, elicitation_agent]
  techniques:
    - Divergent thinking exercises
    - Convergent analysis
    - Multi-perspective simulation
    - "What if" analysis
    - "Yes and" methodology
  outputs:
    - Refined project concept
    - Feature ideas and alternatives
    - Problem-solution mapping
    - Innovation opportunities
```

### Phase 2: Modeling (PRD Creation)
```yaml
modeling_phase:
  description: "Comprehensive Product Requirements Document creation"
  agents: [product_manager_agent, template_agent, elicitation_agent]
  techniques:
    - Advanced elicitation for requirements gathering
    - Stakeholder simulation
    - Use case development
    - Priority matrix analysis
  outputs:
    - Complete PRD document
    - User stories and acceptance criteria
    - Feature specifications
    - Success metrics definition
```

### Phase 3: Architecture
```yaml
architecture_phase:
  description: "Technical architecture and system design"
  agents: [architect_agent, template_agent, elicitation_agent]
  techniques:
    - System design elicitation
    - Technology stack analysis
    - Scalability planning
    - Security consideration analysis
  outputs:
    - Architecture document
    - Technical specifications
    - System diagrams
    - Implementation roadmap
```

### Phase 4: Development
```yaml
development_phase:
  description: "Coordinated development and implementation"
  agents: [development_agent, template_agent]
  techniques:
    - Iterative development planning
    - Code generation coordination
    - Quality assurance integration
    - Deployment preparation
  outputs:
    - Implementation plan
    - Code structure and components
    - Testing strategy
    - Deployment configuration
```

## Advanced Elicitation Techniques Framework

### Core Technique Categories
```yaml
analytical_techniques:
  - "What if analysis"
  - "Root cause analysis"
  - "Pros and cons evaluation"
  - "Risk assessment analysis"
  - "Impact analysis"

creative_techniques:
  - "Yes and methodology"
  - "Alternative generation"
  - "Reverse brainstorming"
  - "Analogical thinking"
  - "Random word association"

collaborative_techniques:
  - "Multiple personality simulation"
  - "Stakeholder perspective taking"
  - "Devil's advocate approach"
  - "Consensus building"
  - "Conflict resolution"

systematic_techniques:
  - "Structured decomposition"
  - "Hierarchical analysis"
  - "Process mapping"
  - "Decision tree analysis"
  - "Priority matrix evaluation"
```

### Technique Selection Logic
```yaml
technique_selection:
  context_based:
    requirements_gathering: ["stakeholder_simulation", "use_case_analysis", "priority_matrix"]
    architecture_design: ["what_if_analysis", "risk_assessment", "scalability_analysis"]
    problem_solving: ["root_cause_analysis", "alternative_generation", "reverse_brainstorming"]
    creative_ideation: ["yes_and_methodology", "analogical_thinking", "random_association"]
  
  document_section_based:
    introduction: ["context_setting", "stakeholder_identification"]
    requirements: ["elicitation_techniques", "validation_methods"]
    design: ["systematic_analysis", "alternative_evaluation"]
    implementation: ["structured_decomposition", "process_mapping"]
```

## Template System Architecture

### Agentic Template Structure
```yaml
agentic_template:
  metadata:
    template_id: "unique_identifier"
    template_name: "descriptive_name"
    template_type: "prd|architecture|brainstorming|custom"
    version: "semantic_version"
    
  sections:
    - section_id: "unique_section_id"
      section_name: "descriptive_section_name"
      agentic_instructions:
        - instruction_type: "question|brainstorm|analyze|validate"
          instruction_text: "specific_instruction"
          elicitation_techniques: ["technique1", "technique2"]
          expected_interaction: "description_of_expected_user_interaction"
      
  interaction_flow:
    - step: 1
      action: "present_section"
      agent_behavior: "introduce_section_and_ask_initial_questions"
    - step: 2
      action: "elicit_information"
      agent_behavior: "apply_selected_elicitation_techniques"
    - step: 3
      action: "validate_and_refine"
      agent_behavior: "confirm_understanding_and_suggest_improvements"
```

### Template Enhancement Features
```yaml
template_enhancements:
  dynamic_questioning:
    - Context-aware question generation
    - Follow-up question chains
    - Clarification requests
    - Validation questions
    
  interactive_brainstorming:
    - Real-time idea building
    - Alternative suggestion generation
    - Collaborative refinement
    - Consensus building
    
  adaptive_flow:
    - User response-based navigation
    - Skip logic for completed sections
    - Conditional section activation
    - Progress tracking and resumption
```

## Expansion Pack System

### Expansion Pack Architecture
```yaml
expansion_pack:
  metadata:
    pack_id: "unique_pack_identifier"
    pack_name: "descriptive_pack_name"
    domain: "target_domain" # e.g., "unity_2d_games", "web_development"
    version: "semantic_version"
    author: "pack_creator"
    
  specialized_agents:
    - agent_id: "domain_specific_agent_id"
      agent_name: "descriptive_agent_name"
      specialization: "specific_domain_expertise"
      capabilities: ["capability1", "capability2"]
      
  custom_templates:
    - template_id: "domain_specific_template_id"
      template_name: "descriptive_template_name"
      template_type: "domain_specific_type"
      
  workflow_modifications:
    - phase: "brainstorming|modeling|architecture|development"
      modifications: ["modification_description"]
      additional_steps: ["step_description"]
```

### Example Expansion Packs
```yaml
unity_2d_game_pack:
  domain: "Unity 2D Game Development"
  specialized_agents:
    - "Unity Game Designer"
    - "2D Asset Coordinator"
    - "Game Mechanics Specialist"
  custom_templates:
    - "Game Design Document Template"
    - "Unity Project Architecture Template"
    - "2D Asset Pipeline Template"

web_development_pack:
  domain: "Modern Web Development"
  specialized_agents:
    - "Frontend Architecture Specialist"
    - "Backend API Designer"
    - "Full-Stack Integration Coordinator"
  custom_templates:
    - "Web Application PRD Template"
    - "Modern Web Architecture Template"
    - "API Specification Template"
```

## Integration Points

### Platform Integration Framework
```yaml
platform_integrations:
  claude_code:
    integration_type: "native"
    features: ["full_workflow", "template_support", "agent_coordination"]
    setup_requirements: ["claude_code_access", "jaegis_configuration"]
    
  gemini_gems:
    integration_type: "gems_based"
    features: ["agent_gems", "workflow_gems", "template_gems"]
    setup_requirements: ["gemini_access", "gems_development_kit"]
    
  chatgpt_custom_gpts:
    integration_type: "custom_gpt"
    features: ["agent_gpts", "workflow_coordination", "cross_gpt_communication"]
    setup_requirements: ["chatgpt_plus", "custom_gpt_creation_access"]
```

### Cross-Platform Synchronization
```yaml
synchronization:
  project_data:
    - Project metadata and configuration
    - Document versions and history
    - Agent interaction logs
    - Template customizations
    
  user_preferences:
    - Preferred elicitation techniques
    - Template customizations
    - Workflow preferences
    - Agent interaction styles
```

This foundational framework provides the structure for implementing all the advanced JAEGIS method features identified from Brian's presentation, with clear separation of concerns and extensibility for future enhancements.
