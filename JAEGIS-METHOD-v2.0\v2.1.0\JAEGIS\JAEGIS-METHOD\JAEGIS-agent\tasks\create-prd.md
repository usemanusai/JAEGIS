# Enhanced PRD Creation with Validation & Research

## Purpose

- Transform inputs into comprehensive PRD with validation, research, and collaborative intelligence
- Define clear MVP scope with validated technical feasibility
- Create research-backed requirements with current market and technology validation
- Provide validated foundation for technical teams with handoff protocols
- Integrate web research and dependency validation throughout the process

## Enhanced Capabilities

### Validation Integration
- **Requirement Validation**: All requirements validated for technical feasibility
- **Technology Research**: Current framework and platform validation
- **Market Research**: Evidence-based user need validation
- **Dependency Checking**: Real-time validation of technical dependencies

### Collaborative Intelligence
- **Shared Context**: Access to project state and previous agent insights
- **Cross-Agent Coordination**: Seamless handoffs with context preservation
- **Quality Assurance**: Professional-grade outputs with validation reports
- **Research Integration**: Current best practices and standards

## Enhanced Workflow

### 1. Context Integration & Validation
- **Review Shared Context**: Access project state from previous agents and collaborative intelligence
- **Validate Inputs**: Ensure all provided inputs are current and validated
- **Research Integration**: Incorporate web research findings and current best practices
- **Dependency Check**: Validate any mentioned technologies for current versions and security

### 2. Enhanced Interaction Mode Selection
Confirm with the user their preferred interaction style with validation:

- **Incremental with Validation**: Work through sections with real-time validation checkpoints
- **YOLO Mode with Research**: Draft complete PRD with integrated research and validation
- **Collaborative Mode**: Interactive development with cross-agent coordination

### 3. Pre-Generation Research & Validation
- **Market Research**: Current trends and competitive landscape analysis
- **Technology Validation**: Verify all proposed technologies are current and secure
- **User Research**: Validate user needs against current market data
- **Feasibility Assessment**: Technical feasibility validation with current standards

### 3. Execute Template

- Use the `prd-tmpl` template (or user-specified alternative template)
- Follow all embedded LLM instructions within the template
- Template contains section-specific guidance and examples

### 4. Template Processing Notes

- **Incremental Mode**: Present each section for review before proceeding
- **YOLO Mode**: Generate all sections, then review with user

Process all template elements according to `templates#template-format` conventions.

**CRITICAL: Never display or output template markup formatting, LLM instructions or examples - they MUST be used by you the agent only, AND NEVER shown to users in chat or document output**

**Content Presentation Guidelines:**

- Present only the final, clean content to users
- Replace template variables with actual project-specific content
- Process all conditional logic internally - show only relevant sections
- For Canvas mode: Update the document with clean, formatted content only

### 7. Prepare Handoffs

Based on PRD content, prepare appropriate next-step prompts:

**If UI Component Exists:**

1. Add Design Architect prompt in designated template section
2. Recommend: User engages Design Architect first for UI/UX Specification
3. Then proceed to Architect with enriched PRD

**If No UI Component:**

- Add Architect prompt in designated template section
- Recommend proceeding directly to Architect

### 8. Validate with Checklist

- Run the `pm-checklist` against completed PRD
- Document completion status for each checklist item
- Present summary by section, address any deficiencies
- Generate final checklist report with findings and resolutions

### 9. Final Presentation

**General Guidelines:**

- Present complete documents in clean, full format
- DO NOT truncate unchanged information
- Begin directly with content (no introductory text needed)
- Ensure all template sections are properly filled
- **NEVER show template markup, instructions, or processing directives to users**

## Key Resources

- **Default Template:** `templates#prd-tmpl`
- **Validation:** `checklists#pm-checklist`
- **User Preferences:** `data#technical-preferences`
- **Elicitation Protocol:** `tasks#advanced-elicitation`

## Important Notes

- This task is template-agnostic - users may specify custom templates
- All detailed instructions are embedded in templates, not this task file
- Focus on orchestration and workflow
- **Template markup is for AI processing only - users should never see output indicators from templates#template-format**
