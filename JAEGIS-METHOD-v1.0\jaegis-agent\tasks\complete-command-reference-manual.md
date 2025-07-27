# Enhanced Complete Command Reference Manual with Intelligence

## Purpose

- Comprehensive command reference manual with real-time validation and research integration
- Conduct command documentation with validated methodologies and collaborative intelligence
- Ensure command excellence with current command interface standards and usability practices
- Integrate web research for current command frameworks and interface patterns
- Provide validated command strategies with cross-team coordination and continuous optimization

## Enhanced Capabilities

### Command Intelligence
- **Command Validation**: Real-time command interface validation against current usability standards
- **Research Integration**: Current command interface best practices and usability frameworks
- **Interface Assessment**: Comprehensive command interface analysis and optimization
- **Usability Validation**: Command usability analysis and interface validation with continuous improvement

### Collaborative Intelligence
- **Shared Context Integration**: Access to all command contexts and interface requirements
- **Cross-Team Coordination**: Seamless collaboration with interface teams and command stakeholders
- **Quality Assurance**: Professional-grade command interface with validation reports
- **Research Integration**: Current command design, interface methodologies, and usability best practices

[[LLM: VALIDATION CHECKPOINT - All command documentation must be validated for completeness, accuracy, and current interface standards. Include research-backed command design methodologies and usability principles.]]

## Complete Command Reference Manual

### 1. Core System Commands

#### `/help` Command
**Syntax**: `/help [topic]`

**Purpose**: Provides comprehensive help information about available commands, workflows, or specific topics.

**Parameters**:
- `topic` (optional): Specific topic for detailed help
  - Valid values: `commands`, `workflows`, `agents`, `modes`

**Behavioral Specifications**:
```python
def execute_help_command(topic=None):
    """Execute help command with comprehensive assistance"""
    
    if topic is None:
        # Display main help menu
        return display_main_help_menu()
    
    elif topic == "commands":
        # List all available commands with brief descriptions
        return display_command_list()
    
    elif topic == "workflows":
        # Explain available workflows and their purposes
        return display_workflow_help()
    
    elif topic == "agents":
        # Show available agents and their capabilities
        return display_agent_help()
    
    elif topic == "modes":
        # Explain different operational modes
        return display_mode_help()
    
    else:
        # Search for topic-specific help
        return search_help_content(topic)

def display_main_help_menu():
    """Display comprehensive main help menu"""
    
    help_content = {
        "title": "JAEGIS AI Agent Orchestrator - Help System",
        "sections": [
            {
                "name": "Quick Start",
                "content": "Type '1' for Documentation Mode or '2' for Full Development Mode"
            },
            {
                "name": "Available Commands",
                "content": "Type '/help commands' for complete command list"
            },
            {
                "name": "Available Agents",
                "content": "Type '/agent-list' to see all available AI agents"
            },
            {
                "name": "Workflows",
                "content": "Type '/help workflows' for workflow information"
            }
        ],
        "quick_commands": [
            "/help commands - List all commands",
            "/agent-list - Show available agents",
            "/exit - Return to orchestrator mode",
            "/yolo - Toggle YOLO mode"
        ]
    }
    
    return format_help_display(help_content)
```

**Examples**:
```bash
# Basic help
/help

# Command-specific help
/help commands

# Workflow help
/help workflows

# Agent help
/help agents
```

**State Management**: 
- Does not change system state
- Maintains current agent context
- Preserves workflow progress

**Troubleshooting**:
- **Issue**: Help command not responding
  - **Solution**: Check system initialization status
- **Issue**: Topic not found
  - **Solution**: Use `/help commands` to see available topics

#### `/yolo` Command
**Syntax**: `/yolo`

**Purpose**: Toggles YOLO (You Only Live Once) mode for rapid execution without confirmation prompts.

**Parameters**: None

**Behavioral Specifications**:
```python
def execute_yolo_command():
    """Toggle YOLO mode with state management"""
    
    current_mode = get_current_yolo_mode()
    
    if current_mode:
        # Disable YOLO mode
        set_yolo_mode(False)
        return YoloModeResult(
            mode="INTERACTIVE",
            message="Entering Interactive mode - confirmations enabled",
            previous_mode="YOLO"
        )
    else:
        # Enable YOLO mode
        set_yolo_mode(True)
        return YoloModeResult(
            mode="YOLO",
            message="Entering YOLO mode - rapid execution enabled",
            previous_mode="INTERACTIVE",
            warning="Confirmations disabled - proceed with caution"
        )

def set_yolo_mode(enabled):
    """Set YOLO mode with proper state management"""
    
    global_state.yolo_mode = enabled
    
    # Update all active agents
    for agent in get_active_agents():
        agent.set_yolo_mode(enabled)
    
    # Update workflow settings
    workflow_manager.set_confirmation_mode(not enabled)
    
    # Log mode change
    log_info(f"YOLO mode {'enabled' if enabled else 'disabled'}")
```

**Examples**:
```bash
# Toggle YOLO mode
/yolo
# Output: "Entering YOLO mode - rapid execution enabled"

# Toggle back to interactive
/yolo
# Output: "Entering Interactive mode - confirmations enabled"
```

**State Management**:
- Changes global execution mode
- Affects all subsequent operations
- Persists until toggled again

#### `/full_yolo` Command
**Syntax**: `/full_yolo`

**Purpose**: Enhanced YOLO mode that activates rapid execution AND configures all agents to assume complete user agreement.

**Parameters**: None

**Behavioral Specifications**:
```python
def execute_full_yolo_command():
    """Activate enhanced YOLO mode with auto-approval"""
    
    # Enable standard YOLO functionality
    set_yolo_mode(True)
    
    # Configure auto-approval for all agents
    configure_auto_approval_mode(True)
    
    # Set workflow expectations
    set_workflow_expectations("AUTO_APPROVE")
    
    # Configure agent behavior
    for agent in get_all_agents():
        agent.set_auto_approval_mode(True)
        agent.set_confirmation_expectations("AUTOMATIC")
    
    return FullYoloModeResult(
        mode="FULL_YOLO",
        message="Full YOLO mode activated - automatic approvals enabled",
        features=[
            "Rapid execution enabled",
            "Automatic approval of recommendations",
            "Elimination of confirmation prompts",
            "Full agent orchestration maintained",
            "Workflow progression without user input"
        ],
        warning="All confirmations disabled - system will proceed automatically"
    )

def configure_auto_approval_mode(enabled):
    """Configure automatic approval for all system components"""
    
    # Set global auto-approval state
    global_state.auto_approval_mode = enabled
    
    # Configure workflow manager
    workflow_manager.set_auto_approval(enabled)
    
    # Configure decision systems
    decision_manager.set_auto_approval(enabled)
    
    # Update agent coordination
    agent_coordinator.set_auto_approval_mode(enabled)
```

**Examples**:
```bash
# Activate full YOLO mode
/full_yolo
# Output: "Full YOLO mode activated - automatic approvals enabled"
```

**State Management**:
- Enables both YOLO and auto-approval modes
- Affects all agents and workflows
- Maintains full collaborative intelligence

### 2. Agent Management Commands

#### `/agent-list` Command
**Syntax**: `/agent-list`

**Purpose**: Displays a comprehensive table of all available AI agents with their capabilities and tasks.

**Parameters**: None

**Behavioral Specifications**:
```python
def execute_agent_list_command():
    """Display comprehensive agent list with capabilities"""
    
    # Load agent configuration
    agent_config = load_agent_configuration()
    
    # Build agent table
    agent_table = []
    
    for index, agent in enumerate(agent_config.agents, 1):
        # Get agent tasks (including checklist runner expansions)
        agent_tasks = expand_agent_tasks(agent.tasks)
        
        agent_entry = {
            "number": index,
            "name": agent.name,
            "title": agent.title,
            "tasks": format_agent_tasks(agent_tasks)
        }
        
        agent_table.append(agent_entry)
    
    return AgentListResult(
        agents=agent_table,
        total_agents=len(agent_table),
        display_format="table",
        headers=["#", "Agent Name", "Agent Title", "Available Tasks"]
    )

def expand_agent_tasks(tasks):
    """Expand tasks including checklist runner tasks"""
    
    expanded_tasks = []
    
    for task in tasks:
        if task == "checklist_runner":
            # Expand to individual checklist tasks
            checklists = get_agent_checklists()
            for checklist in checklists:
                expanded_tasks.append(f"[Run {checklist.name} Checklist]")
        else:
            expanded_tasks.append(f"[{task.display_name}]")
    
    return expanded_tasks

def format_agent_tasks(tasks):
    """Format tasks for display in agent list"""
    
    if len(tasks) <= 3:
        return ", ".join(tasks)
    else:
        # Show first 3 tasks and count
        displayed_tasks = ", ".join(tasks[:3])
        remaining_count = len(tasks) - 3
        return f"{displayed_tasks} (+{remaining_count} more)"
```

**Examples**:
```bash
/agent-list
```

**Output Format**:
```
| # | Agent Name | Agent Title           | Available Tasks                    |
|---|------------|-----------------------|------------------------------------|
| 1 | John       | Product Manager       | [Create PRD], [Validate Req] (+2) |
| 2 | Fred       | Senior Architect      | [Design Architecture], [Review]    |
| 3 | Tyler      | Task Breakdown Spec   | [Break Down Tasks], [Create DoD]   |
| 4 | Jane       | Design Architect      | [UI Design], [UX Review]           |
| 5 | Sage       | Security Engineer     | [Security Review], [Threat Model]  |
```

#### `/{agent}` Command
**Syntax**: `/{agent_name}`

**Purpose**: Immediately switch to the specified agent or confirm switch if already in another agent persona.

**Parameters**:
- `agent_name`: Name of the agent to activate (e.g., `john`, `fred`, `jane`)

**Behavioral Specifications**:
```python
def execute_agent_switch_command(agent_name):
    """Switch to specified agent with proper state management"""
    
    # Normalize agent name
    normalized_name = normalize_agent_name(agent_name)
    
    # Validate agent exists
    if not agent_exists(normalized_name):
        return AgentSwitchResult(
            success=False,
            error=f"Agent '{agent_name}' not found",
            available_agents=get_available_agent_names(),
            suggestion=find_similar_agent_name(agent_name)
        )
    
    # Check current state
    current_agent = get_current_agent()
    
    if current_agent and current_agent.name == normalized_name:
        return AgentSwitchResult(
            success=True,
            message=f"Already in {normalized_name} agent mode",
            current_agent=normalized_name,
            no_change=True
        )
    
    # Handle agent switch confirmation if needed
    if current_agent and not is_yolo_mode():
        confirmation = request_agent_switch_confirmation(current_agent, normalized_name)
        if not confirmation:
            return AgentSwitchResult(
                success=False,
                message="Agent switch cancelled by user",
                current_agent=current_agent.name
            )
    
    # Execute agent switch
    try:
        new_agent = activate_agent(normalized_name)
        
        # Deactivate previous agent if exists
        if current_agent:
            deactivate_agent(current_agent)
        
        # Set new agent as current
        set_current_agent(new_agent)
        
        # Initialize agent greeting
        greeting = new_agent.generate_initial_greeting()
        
        return AgentSwitchResult(
            success=True,
            message=f"Switched to {new_agent.title} ({new_agent.name})",
            current_agent=new_agent.name,
            agent_greeting=greeting,
            available_tasks=new_agent.get_available_tasks()
        )
        
    except AgentActivationError as e:
        return AgentSwitchResult(
            success=False,
            error=f"Failed to activate agent {normalized_name}: {e}",
            current_agent=current_agent.name if current_agent else None
        )
```

**Examples**:
```bash
# Switch to Product Manager
/john

# Switch to Architect
/fred

# Switch to Design Architect
/jane
```

**State Management**:
- Deactivates current agent
- Activates new agent persona
- Preserves workflow context where possible
- Updates command context

### 3. Workflow Control Commands

#### `/pre_select_agents` Command
**Syntax**: `/pre_select_agents`

**Purpose**: Present agent selection interface allowing users to select multiple agents and specific tasks before starting workflow.

**Parameters**: None

**Behavioral Specifications**:
```python
def execute_pre_select_agents_command():
    """Present comprehensive agent selection interface"""
    
    # Load all available agents
    all_agents = load_all_agents()
    
    # Organize agents by category
    categorized_agents = categorize_agents(all_agents)
    
    # Present selection interface
    selection_interface = AgentSelectionInterface(
        categorized_agents=categorized_agents,
        selection_mode="MULTI_SELECT",
        task_selection_enabled=True
    )
    
    # Display selection interface
    display_agent_selection_interface(selection_interface)
    
    # Wait for user selections
    user_selections = await_user_agent_selections()
    
    # Validate selections
    validation_result = validate_agent_selections(user_selections)
    if not validation_result.is_valid:
        return AgentSelectionResult(
            success=False,
            errors=validation_result.errors,
            recommendations=validation_result.recommendations
        )
    
    # Store selections for workflow execution
    store_agent_selections(user_selections)
    
    # Generate selection summary
    selection_summary = generate_selection_summary(user_selections)
    
    # Request user confirmation
    confirmation = request_selection_confirmation(selection_summary)
    
    if confirmation:
        return AgentSelectionResult(
            success=True,
            selected_agents=user_selections.agents,
            selected_tasks=user_selections.tasks,
            selection_summary=selection_summary,
            ready_for_workflow=True
        )
    else:
        return AgentSelectionResult(
            success=False,
            message="Agent selection cancelled by user"
        )

def categorize_agents(agents):
    """Organize agents into logical categories"""
    
    categories = {
        "Core Agents": [],
        "Specialist Agents": [],
        "Quality Assurance": [],
        "Technical Specialists": []
    }
    
    for agent in agents:
        if agent.name in ["John", "Fred", "Tyler"]:
            categories["Core Agents"].append(agent)
        elif agent.name in ["Jane", "Sage", "Dakota", "Alex"]:
            categories["Specialist Agents"].append(agent)
        elif agent.name in ["Sentinel", "DocQA"]:
            categories["Quality Assurance"].append(agent)
        else:
            categories["Technical Specialists"].append(agent)
    
    return categories
```

**Examples**:
```bash
/pre_select_agents
```

**Output Format**:
```
🎯 **Agent Selection Interface**

**Core Agents (Always Recommended)**
[ ] 1. John (Product Manager) - [Create PRD], [Validate Requirements]
[ ] 2. Fred (Senior Architect) - [Design Architecture], [Technical Review]
[ ] 3. Tyler (Task Breakdown Specialist) - [Break Down Tasks], [Create Checklist]

**Specialist Agents**
[ ] 4. Jane (Design Architect) - [UI Design], [UX Review], [Frontend Architecture]
[ ] 5. Sage (Security Engineer) - [Security Review], [Threat Modeling]
[ ] 6. Dakota (Data Engineer) - [Data Architecture], [Database Design]
[ ] 7. Alex (DevOps Engineer) - [Infrastructure], [Deployment Strategy]

Select agents by number (e.g., 1,2,4,5): 
```

#### `/party-mode` Command
**Syntax**: `/party-mode`

**Purpose**: Enters group chat simulation with all available AI agents for collaborative ideation and interaction.

**Parameters**: None

**Behavioral Specifications**:
```python
def execute_party_mode_command():
    """Enter multi-agent party mode for group collaboration"""
    
    # Load all available agents
    all_agents = load_all_agents()
    
    # Activate all agents in party mode
    party_participants = []
    for agent in all_agents:
        try:
            party_agent = activate_agent_for_party(agent.name)
            party_participants.append(party_agent)
        except Exception as e:
            log_warning(f"Failed to activate {agent.name} for party mode: {e}")
    
    # Initialize party mode session
    party_session = PartyModeSession(
        participants=party_participants,
        session_id=generate_party_session_id(),
        mode="GROUP_IDEATION",
        workflow_disabled=True
    )
    
    # Set up group communication
    group_communication = setup_group_communication(party_participants)
    
    # Initialize party mode interface
    party_interface = PartyModeInterface(
        session=party_session,
        communication=group_communication,
        display_mode="MULTI_AGENT_CHAT"
    )
    
    # Start party mode
    party_interface.start()
    
    # Generate welcome message
    welcome_message = generate_party_welcome_message(party_participants)
    
    return PartyModeResult(
        success=True,
        session=party_session,
        participants=[agent.name for agent in party_participants],
        welcome_message=welcome_message,
        instructions=[
            "All agents are now active in group chat mode",
            "No specific workflows will be followed",
            "Perfect for group ideation and brainstorming",
            "Type '/exit' to leave party mode"
        ]
    )

def generate_party_welcome_message(participants):
    """Generate welcome message for party mode"""
    
    participant_names = [agent.name for agent in participants]
    
    return f"""
🎉 **Welcome to JAEGIS Party Mode!** 🎉

Active Participants: {', '.join(participant_names)}

In party mode, all agents are active simultaneously for:
- Group brainstorming and ideation
- Multi-perspective problem solving
- Creative collaboration
- Fun interactions with your AI agent team

No formal workflows are active - just enjoy the collaborative intelligence!
    """
```

**Examples**:
```bash
/party-mode
```

**State Management**:
- Activates all available agents
- Disables formal workflows
- Enables group communication mode
- Maintains until `/exit` is called

### 4. Context and Communication Commands

#### `/JAEGIS {query}` Command
**Syntax**: `/JAEGIS {query}`

**Purpose**: Communicate directly with the base JAEGIS orchestrator even while in another agent persona.

**Parameters**:
- `query`: Message or question for the JAEGIS orchestrator

**Behavioral Specifications**:
```python
def execute_JAEGIS_query_command(query):
    """Send query to JAEGIS orchestrator while preserving current context"""

    # Preserve current agent context
    current_context = preserve_current_context()

    # Temporarily switch to JAEGIS orchestrator
    JAEGIS_orchestrator = get_JAEGIS_orchestrator()

    # Process query with JAEGIS
    try:
        JAEGIS_response = JAEGIS_orchestrator.process_query(
            query=query,
            context=current_context,
            source_agent=current_context.active_agent if current_context.active_agent else None
        )

        # Restore previous context
        restore_context(current_context)

        return JAEGISQueryResult(
            success=True,
            query=query,
            response=JAEGIS_response,
            context_preserved=True,
            current_agent=current_context.active_agent.name if current_context.active_agent else "JAEGIS"
        )

    except Exception as e:
        # Restore context even on error
        restore_context(current_context)

        return JAEGISQueryResult(
            success=False,
            query=query,
            error=str(e),
            context_preserved=True
        )

def preserve_current_context():
    """Preserve current system context for restoration"""

    return SystemContext(
        active_agent=get_current_agent(),
        workflow_state=get_current_workflow_state(),
        conversation_history=get_conversation_history(),
        shared_context=get_shared_context(),
        timestamp=time.time()
    )
```

**Examples**:
```bash
# While in John (PM) agent mode
/JAEGIS What other agents would be good for this project?

# While in Fred (Architect) agent mode
/JAEGIS Can you explain the JAEGIS method principles?

# While in any agent mode
/JAEGIS How do I switch back to documentation mode?
```

**State Management**:
- Preserves current agent context
- Temporarily activates JAEGIS orchestrator
- Restores previous context after response
- Maintains conversation continuity

#### `/{agent} {query}` Command
**Syntax**: `/{agent_name} {query}`

**Purpose**: Send a query to a specific agent without switching to that agent permanently.

**Parameters**:
- `agent_name`: Name of the target agent
- `query`: Message or question for the specified agent

**Behavioral Specifications**:
```python
def execute_agent_query_command(agent_name, query):
    """Send query to specific agent without permanent switch"""

    # Validate target agent
    target_agent = find_agent_by_name(agent_name)
    if not target_agent:
        return AgentQueryResult(
            success=False,
            error=f"Agent '{agent_name}' not found",
            available_agents=get_available_agent_names()
        )

    # Preserve current context
    current_context = preserve_current_context()

    # Temporarily activate target agent if not already active
    agent_was_active = target_agent.is_active()
    if not agent_was_active:
        target_agent.activate_temporarily()

    try:
        # Process query with target agent
        agent_response = target_agent.process_query(
            query=query,
            context=current_context,
            temporary_activation=True
        )

        # Deactivate agent if it wasn't previously active
        if not agent_was_active:
            target_agent.deactivate_temporary()

        # Restore original context
        restore_context(current_context)

        return AgentQueryResult(
            success=True,
            target_agent=agent_name,
            query=query,
            response=agent_response,
            context_preserved=True,
            temporary_activation=not agent_was_active
        )

    except Exception as e:
        # Cleanup on error
        if not agent_was_active:
            target_agent.deactivate_temporary()
        restore_context(current_context)

        return AgentQueryResult(
            success=False,
            target_agent=agent_name,
            query=query,
            error=str(e)
        )
```

**Examples**:
```bash
# Ask architect about technical feasibility while in PM mode
/fred Is this architecture scalable for 1M users?

# Ask security engineer about vulnerabilities while in architect mode
/sage What are the main security risks with this approach?

# Ask design architect about UI considerations
/jane How should we handle mobile responsiveness?
```

#### `/doc-out` Command
**Syntax**: `/doc-out`

**Purpose**: Output the full document being discussed or refined without truncation.

**Parameters**: None

**Behavioral Specifications**:
```python
def execute_doc_out_command():
    """Output complete document without truncation"""

    # Identify current document context
    current_document = identify_current_document()

    if not current_document:
        return DocOutResult(
            success=False,
            error="No document currently in context",
            suggestion="Generate or load a document first"
        )

    # Get complete document content
    try:
        full_content = current_document.get_full_content()

        # Format for output
        formatted_content = format_document_for_output(
            content=full_content,
            document_type=current_document.type,
            include_metadata=True
        )

        return DocOutResult(
            success=True,
            document_name=current_document.name,
            document_type=current_document.type,
            full_content=formatted_content,
            content_length=len(full_content),
            last_modified=current_document.last_modified
        )

    except Exception as e:
        return DocOutResult(
            success=False,
            error=f"Failed to output document: {e}",
            document_name=current_document.name if current_document else None
        )

def identify_current_document():
    """Identify the document currently being discussed"""

    # Check conversation context for document references
    conversation_context = get_conversation_context()

    # Look for recent document mentions
    recent_documents = find_recent_document_references(conversation_context)

    if recent_documents:
        return recent_documents[0]  # Most recent

    # Check active workflow for generated documents
    active_workflow = get_active_workflow()
    if active_workflow and hasattr(active_workflow, 'current_document'):
        return active_workflow.current_document

    return None
```

**Examples**:
```bash
# Output current PRD being discussed
/doc-out

# Output architecture document being refined
/doc-out
```

### 5. System Control Commands

#### `/exit` Command
**Syntax**: `/exit`

**Purpose**: Immediately abandon current agent or party-mode and return to base JAEGIS orchestrator.

**Parameters**: None

**Behavioral Specifications**:
```python
def execute_exit_command():
    """Exit current mode and return to JAEGIS orchestrator"""

    # Determine current mode
    current_mode = get_current_system_mode()

    # Handle different exit scenarios
    if current_mode == "PARTY_MODE":
        return exit_party_mode()
    elif current_mode == "AGENT_MODE":
        return exit_agent_mode()
    elif current_mode == "WORKFLOW_MODE":
        return exit_workflow_mode()
    else:
        return exit_to_orchestrator()

def exit_agent_mode():
    """Exit current agent mode"""

    current_agent = get_current_agent()

    if not current_agent:
        return ExitResult(
            success=True,
            message="Already in JAEGIS orchestrator mode",
            previous_mode="ORCHESTRATOR",
            current_mode="ORCHESTRATOR"
        )

    # Deactivate current agent
    try:
        current_agent.deactivate()

        # Clear agent context
        clear_agent_context()

        # Return to orchestrator
        activate_JAEGIS_orchestrator()

        return ExitResult(
            success=True,
            message=f"Exited {current_agent.title} mode, returned to JAEGIS orchestrator",
            previous_mode=f"AGENT_{current_agent.name.upper()}",
            current_mode="ORCHESTRATOR",
            previous_agent=current_agent.name
        )

    except Exception as e:
        return ExitResult(
            success=False,
            error=f"Failed to exit agent mode: {e}",
            current_mode=f"AGENT_{current_agent.name.upper()}"
        )

def exit_party_mode():
    """Exit party mode and return to orchestrator"""

    party_session = get_current_party_session()

    if not party_session:
        return ExitResult(
            success=True,
            message="Not currently in party mode",
            current_mode="ORCHESTRATOR"
        )

    try:
        # Deactivate all party participants
        for participant in party_session.participants:
            participant.deactivate()

        # Close party session
        party_session.close()

        # Clear party context
        clear_party_context()

        # Return to orchestrator
        activate_JAEGIS_orchestrator()

        return ExitResult(
            success=True,
            message="Exited party mode, returned to JAEGIS orchestrator",
            previous_mode="PARTY_MODE",
            current_mode="ORCHESTRATOR",
            deactivated_agents=[p.name for p in party_session.participants]
        )

    except Exception as e:
        return ExitResult(
            success=False,
            error=f"Failed to exit party mode: {e}",
            current_mode="PARTY_MODE"
        )
```

**Examples**:
```bash
# Exit from any agent mode
/exit

# Exit from party mode
/exit

# Exit from workflow mode
/exit
```

**State Management**:
- Deactivates current agent(s)
- Clears agent-specific context
- Returns to JAEGIS orchestrator
- Preserves workflow progress where appropriate

### 6. Command Precedence and Interaction Rules

#### Command Priority Hierarchy
1. **System Commands** (highest priority)
   - `/exit` - Always processed immediately
   - `/help` - Always available

2. **Mode Control Commands**
   - `/yolo`, `/full_yolo` - Mode toggles
   - `/party-mode` - Mode activation

3. **Agent Commands**
   - `/{agent}` - Agent switching
   - `/agent-list` - Agent information

4. **Context Commands**
   - `/JAEGIS {query}` - Orchestrator queries
   - `/{agent} {query}` - Agent queries
   - `/doc-out` - Document output

5. **Workflow Commands**
   - `/pre_select_agents` - Workflow preparation
   - Mode selection (1, 2) - Workflow activation

#### Command State Management
```python
class CommandStateManager:
    """Manage command state and interactions"""

    def __init__(self):
        self.command_history = []
        self.active_commands = {}
        self.command_context = {}
        self.state_stack = []

    def process_command(self, command_input):
        """Process command with proper state management"""

        # Parse command
        parsed_command = parse_command_input(command_input)

        # Check command precedence
        if self.has_higher_priority_command_active(parsed_command):
            return self.queue_command(parsed_command)

        # Validate command in current context
        validation_result = self.validate_command_context(parsed_command)
        if not validation_result.is_valid:
            return CommandResult(
                success=False,
                error=validation_result.error_message,
                suggestions=validation_result.suggestions
            )

        # Execute command
        try:
            # Save current state
            self.save_state_snapshot()

            # Execute command
            result = self.execute_command(parsed_command)

            # Update command history
            self.add_to_command_history(parsed_command, result)

            return result

        except Exception as e:
            # Restore previous state on error
            self.restore_state_snapshot()

            return CommandResult(
                success=False,
                error=f"Command execution failed: {e}",
                command=parsed_command.command_name
            )
```

### 7. Troubleshooting Guide

#### Common Command Issues

**Issue**: Command not recognized
- **Symptoms**: "Command not found" or "Unknown command" error
- **Solutions**:
  1. Check command spelling: `/help` not `/halp`
  2. Verify command exists: Use `/help commands` to see all available commands
  3. Check current mode: Some commands only work in specific modes

**Issue**: Agent switch fails
- **Symptoms**: "Agent not found" or "Failed to activate agent" error
- **Solutions**:
  1. Verify agent name: Use `/agent-list` to see correct names
  2. Check agent availability: Some agents may be temporarily unavailable
  3. Try alternative agent: Use similar agent if primary is unavailable

**Issue**: Commands not responding
- **Symptoms**: No response after entering command
- **Solutions**:
  1. Check system status: Ensure JAEGIS system is properly initialized
  2. Restart session: Use `/exit` and restart if needed
  3. Check for system errors: Look for error messages in logs

**Issue**: YOLO mode not working as expected
- **Symptoms**: Still getting confirmation prompts in YOLO mode
- **Solutions**:
  1. Verify mode activation: Check that YOLO mode confirmation was received
  2. Use `/full_yolo` for complete automation
  3. Check agent-specific settings: Some agents may have override settings
