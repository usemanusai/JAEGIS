# Enhanced Agent Configuration Specification with Intelligence

## Purpose

- Comprehensive agent configuration specification with real-time validation and research integration
- Conduct configuration management with validated methodologies and collaborative intelligence
- Ensure configuration excellence with current agent development standards and management practices
- Integrate web research for current configuration frameworks and agent patterns
- Provide validated configuration strategies with cross-team coordination and continuous optimization

## Enhanced Capabilities

### Configuration Intelligence
- **Configuration Validation**: Real-time agent configuration validation against current development standards
- **Research Integration**: Current agent configuration best practices and management frameworks
- **Management Assessment**: Comprehensive configuration management analysis and optimization
- **System Validation**: Agent configuration analysis and validation with continuous improvement

### Collaborative Intelligence
- **Shared Context Integration**: Access to all configuration contexts and management requirements
- **Cross-Team Coordination**: Seamless collaboration with development teams and configuration stakeholders
- **Quality Assurance**: Professional-grade agent configuration with validation reports
- **Research Integration**: Current agent development, configuration methodologies, and management best practices

[[LLM: VALIDATION CHECKPOINT - All agent configurations must be validated for completeness, accuracy, and current development standards. Include research-backed configuration methodologies and management principles.]]

## Complete Agent Configuration Specification

### 1. Agent Configuration Properties

#### Core Properties
```yaml
# agent-config.txt format
agents:
  - title: "Product Manager"           # Human-readable role title
    name: "John"                      # Agent identifier/name
    description: "Strategic product planning and requirements definition specialist"
    persona: "personas#pm"            # Persona reference (sectioned or direct)
    customize: ""                     # Optional persona customization string
    tasks:                           # Available tasks for this agent
      - "tasks#create-prd"
      - "tasks#validate-requirements"
    templates:                       # Templates this agent can use
      - "templates#prd-template"
      - "templates#requirements-template"
    checklists:                      # Checklists for validation
      - "checklists#pm-checklist"
      - "checklists#requirements-validation"
    data:                           # Data sources for this agent
      - "data#product-patterns"
      - "data#market-research"
```

#### Property Specifications

**Title** (Required)
- **Type**: String
- **Purpose**: Human-readable role description for user interface
- **Format**: Descriptive title (e.g., "Product Manager", "Senior Architect")
- **Validation**: Must be non-empty, max 100 characters
- **Usage**: Displayed in agent selection menus and status messages

**Name** (Required)
- **Type**: String
- **Purpose**: Unique agent identifier for internal references
- **Format**: Alphanumeric, no spaces (e.g., "John", "Fred", "Jane")
- **Validation**: Must be unique across all agents, 3-50 characters
- **Usage**: Used in commands like `/john` and internal agent references

**Description** (Required)
- **Type**: String
- **Purpose**: Detailed explanation of agent capabilities and role
- **Format**: Descriptive text explaining agent's expertise and responsibilities
- **Validation**: Must be non-empty, max 500 characters
- **Usage**: Displayed in agent selection interfaces and help documentation

**Persona** (Required)
- **Type**: String (File Reference)
- **Purpose**: Reference to persona definition file or section
- **Format**: Either "personas#section_name" or "filename.md"
- **Validation**: Referenced file/section must exist and be accessible
- **Usage**: Loaded to define agent's personality, knowledge, and behavior

**Customize** (Optional)
- **Type**: String
- **Purpose**: Override or extend persona content with specific customizations
- **Format**: Free-form text that modifies persona behavior
- **Validation**: No specific format requirements
- **Usage**: Applied after persona loading to customize agent behavior

**Tasks** (Optional)
- **Type**: Array of Strings (File References)
- **Purpose**: List of tasks this agent can perform
- **Format**: Array of task references like "tasks#task_name" or "task_file.md"
- **Validation**: All referenced tasks must exist
- **Usage**: Displayed in task selection menus for this agent

**Templates** (Optional)
- **Type**: Array of Strings (File References)
- **Purpose**: Templates available to this agent for document generation
- **Format**: Array of template references
- **Validation**: All referenced templates must exist
- **Usage**: Loaded when agent needs to generate structured content

**Checklists** (Optional)
- **Type**: Array of Strings (File References)
- **Purpose**: Quality assurance checklists for this agent's work
- **Format**: Array of checklist references
- **Validation**: All referenced checklists must exist
- **Usage**: Used for validation and quality assurance processes

**Data** (Optional)
- **Type**: Array of Strings (File References)
- **Purpose**: Data sources and knowledge bases for this agent
- **Format**: Array of data file references
- **Validation**: All referenced data files must exist
- **Usage**: Provides domain-specific knowledge and patterns

### 2. Configuration Loading Sequence

#### Phase 1: Configuration Discovery
```python
def discover_agent_config():
    """Discover and validate agent configuration file"""
    
    config_paths = [
        "(agent-root)/agent-config.txt",
        "(agent-root)/config/agent-config.txt",
        "(project-root)/agent-config.txt"
    ]
    
    for path in config_paths:
        if os.path.exists(resolve_path(path)):
            return validate_config_file(path)
    
    raise ConfigurationError("No agent configuration file found")
```

#### Phase 2: Configuration Parsing
```python
def parse_agent_config(config_file_path):
    """Parse agent configuration with comprehensive validation"""
    
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # Parse configuration format (YAML, JSON, or custom format)
        agents = parse_config_format(config_content)
        
        # Validate each agent configuration
        validated_agents = []
        for agent_config in agents:
            validated_agent = validate_agent_config(agent_config)
            validated_agents.append(validated_agent)
        
        return AgentConfiguration(validated_agents)
        
    except Exception as e:
        raise ConfigurationError(f"Failed to parse config: {e}")
```

#### Phase 3: Resource Validation
```python
def validate_agent_resources(agent_config):
    """Validate all resources referenced by agent configuration"""
    
    validation_results = {
        "persona": validate_persona_reference(agent_config.persona),
        "tasks": validate_task_references(agent_config.tasks),
        "templates": validate_template_references(agent_config.templates),
        "checklists": validate_checklist_references(agent_config.checklists),
        "data": validate_data_references(agent_config.data)
    }
    
    # Check for missing or invalid references
    errors = []
    for resource_type, result in validation_results.items():
        if not result.is_valid:
            errors.append(f"{resource_type}: {result.error_message}")
    
    if errors:
        raise ResourceValidationError(f"Resource validation failed: {errors}")
    
    return validation_results

### 3. Priority Order and Loading Hierarchy

#### Configuration Loading Priority
1. **Primary Configuration**: `(agent-root)/agent-config.txt`
2. **Secondary Configuration**: `(agent-root)/config/agent-config.txt`
3. **Fallback Configuration**: `(project-root)/agent-config.txt`
4. **Default Configuration**: Generated default configuration with core agents

#### Resource Loading Priority
```python
def load_agent_resources(agent_config):
    """Load agent resources in priority order"""

    loading_sequence = [
        ("persona", load_persona_content),
        ("data", load_data_sources),
        ("templates", load_template_files),
        ("checklists", load_checklist_files),
        ("tasks", load_task_definitions)
    ]

    loaded_resources = {}
    for resource_type, loader_func in loading_sequence:
        try:
            resources = getattr(agent_config, resource_type, [])
            loaded_resources[resource_type] = loader_func(resources)
        except Exception as e:
            log_warning(f"Failed to load {resource_type}: {e}")
            loaded_resources[resource_type] = get_default_resource(resource_type)

    return loaded_resources
```

### 4. Customize String Override Behavior

#### Override Mechanism
```python
def apply_customize_override(persona_content, customize_string):
    """Apply customize string to override persona content"""

    if not customize_string:
        return persona_content

    # Parse customize directives
    directives = parse_customize_directives(customize_string)

    modified_content = persona_content
    for directive in directives:
        if directive.type == "REPLACE":
            modified_content = replace_content_section(
                modified_content, directive.target, directive.replacement
            )
        elif directive.type == "APPEND":
            modified_content = append_content_section(
                modified_content, directive.target, directive.addition
            )
        elif directive.type == "PREPEND":
            modified_content = prepend_content_section(
                modified_content, directive.target, directive.addition
            )
        elif directive.type == "REMOVE":
            modified_content = remove_content_section(
                modified_content, directive.target
            )

    return modified_content
```

#### Customize Directive Format
```
# Customize string examples:
"REPLACE:responsibilities:Enhanced product management with AI integration focus"
"APPEND:skills:- Advanced AI prompt engineering\n- Machine learning model evaluation"
"REMOVE:limitations"
"PREPEND:introduction:AI-Enhanced "
```

### 5. Configuration Validation Rules

#### Agent-Level Validation
```python
def validate_agent_config(agent_config):
    """Comprehensive agent configuration validation"""

    validation_rules = [
        ("title", validate_title),
        ("name", validate_name),
        ("description", validate_description),
        ("persona", validate_persona_reference),
        ("customize", validate_customize_string),
        ("tasks", validate_task_array),
        ("templates", validate_template_array),
        ("checklists", validate_checklist_array),
        ("data", validate_data_array)
    ]

    validation_errors = []
    for field_name, validator in validation_rules:
        try:
            field_value = getattr(agent_config, field_name, None)
            validator(field_value, field_name)
        except ValidationError as e:
            validation_errors.append(f"{field_name}: {e.message}")

    if validation_errors:
        raise AgentValidationError(f"Agent validation failed: {validation_errors}")

    return agent_config
```

#### Field-Specific Validators
```python
def validate_title(title, field_name):
    """Validate agent title field"""
    if not title or not isinstance(title, str):
        raise ValidationError("Title is required and must be a string")
    if len(title.strip()) == 0:
        raise ValidationError("Title cannot be empty")
    if len(title) > 100:
        raise ValidationError("Title must be 100 characters or less")

def validate_name(name, field_name):
    """Validate agent name field"""
    if not name or not isinstance(name, str):
        raise ValidationError("Name is required and must be a string")
    if not re.match(r'^[a-zA-Z0-9_-]{3,50}$', name):
        raise ValidationError("Name must be 3-50 alphanumeric characters")

def validate_persona_reference(persona_ref, field_name):
    """Validate persona reference"""
    if not persona_ref:
        raise ValidationError("Persona reference is required")

    # Validate reference format
    if '#' in persona_ref:
        file_prefix, section_name = persona_ref.split('#', 1)
        if not file_prefix or not section_name:
            raise ValidationError("Invalid sectioned reference format")
    elif not persona_ref.endswith('.md'):
        raise ValidationError("Direct file reference must end with .md")

    # Validate file existence
    resolved_path = resolve_resource_path(persona_ref, "personas")
    if not resolved_path.exists:
        raise ValidationError(f"Persona reference not found: {persona_ref}")
```

### 6. Agent Inheritance and Dependencies

#### Inheritance System
```python
class AgentInheritance:
    """Manage agent inheritance and dependency relationships"""

    def __init__(self):
        self.inheritance_graph = {}
        self.dependency_cache = {}

    def resolve_agent_inheritance(self, agent_config):
        """Resolve agent inheritance chain"""

        if hasattr(agent_config, 'inherits_from'):
            parent_agent = self.load_parent_agent(agent_config.inherits_from)
            merged_config = self.merge_agent_configs(parent_agent, agent_config)
            return merged_config

        return agent_config

    def merge_agent_configs(self, parent_config, child_config):
        """Merge parent and child agent configurations"""

        merged_config = copy.deepcopy(parent_config)

        # Override with child properties
        for property_name in ['title', 'name', 'description', 'persona', 'customize']:
            if hasattr(child_config, property_name):
                setattr(merged_config, property_name, getattr(child_config, property_name))

        # Merge arrays (tasks, templates, checklists, data)
        for array_property in ['tasks', 'templates', 'checklists', 'data']:
            parent_array = getattr(parent_config, array_property, [])
            child_array = getattr(child_config, array_property, [])
            merged_array = list(set(parent_array + child_array))  # Remove duplicates
            setattr(merged_config, array_property, merged_array)

        return merged_config

### 7. Memory Management for Loaded Contexts

#### Context Memory System
```python
class AgentContextMemory:
    """Manage memory for loaded agent contexts"""

    def __init__(self, max_memory_mb=512):
        self.max_memory_mb = max_memory_mb
        self.loaded_contexts = {}
        self.memory_usage = {}
        self.access_timestamps = {}

    def load_agent_context(self, agent_name, agent_config):
        """Load agent context with memory management"""

        # Check if already loaded
        if agent_name in self.loaded_contexts:
            self.access_timestamps[agent_name] = time.time()
            return self.loaded_contexts[agent_name]

        # Check memory limits
        if self.get_total_memory_usage() > self.max_memory_mb:
            self.cleanup_least_recently_used()

        # Load new context
        context = self.create_agent_context(agent_config)
        self.loaded_contexts[agent_name] = context
        self.memory_usage[agent_name] = self.calculate_context_size(context)
        self.access_timestamps[agent_name] = time.time()

        return context

    def cleanup_least_recently_used(self):
        """Remove least recently used contexts to free memory"""

        if not self.access_timestamps:
            return

        # Sort by access time (oldest first)
        sorted_agents = sorted(
            self.access_timestamps.items(),
            key=lambda x: x[1]
        )

        # Remove oldest 25% of contexts
        removal_count = max(1, len(sorted_agents) // 4)
        for agent_name, _ in sorted_agents[:removal_count]:
            self.unload_agent_context(agent_name)
```

### 8. Configuration Error Handling

#### Error Classification
```python
class ConfigurationError(Exception):
    """Base class for configuration errors"""
    pass

class AgentValidationError(ConfigurationError):
    """Agent-specific validation errors"""
    pass

class ResourceValidationError(ConfigurationError):
    """Resource reference validation errors"""
    pass

class InheritanceError(ConfigurationError):
    """Agent inheritance resolution errors"""
    pass
```

#### Error Recovery Strategies
```python
def handle_configuration_error(error, agent_config):
    """Handle configuration errors with recovery strategies"""

    recovery_strategies = {
        "MISSING_PERSONA": create_default_persona,
        "INVALID_TASK_REFERENCE": remove_invalid_task,
        "MISSING_TEMPLATE": use_default_template,
        "CIRCULAR_INHERITANCE": break_inheritance_cycle,
        "MEMORY_LIMIT_EXCEEDED": cleanup_memory_and_retry
    }

    error_type = classify_error(error)
    recovery_func = recovery_strategies.get(error_type, log_and_continue)

    try:
        return recovery_func(agent_config, error)
    except Exception as recovery_error:
        log_error(f"Recovery failed: {recovery_error}")
        return create_minimal_agent_config(agent_config.name)
```

### 9. Configuration Validation Checklist

#### Pre-Deployment Validation
- [ ] All agent configuration files are present and accessible
- [ ] All persona references resolve to valid files/sections
- [ ] All task references point to existing task definitions
- [ ] All template references are valid and accessible
- [ ] All checklist references exist and are readable
- [ ] All data source references are valid
- [ ] No circular dependencies in agent inheritance
- [ ] Agent names are unique across the configuration
- [ ] All required directories exist with proper permissions
- [ ] Configuration file syntax is valid
- [ ] Memory limits are appropriate for system resources
- [ ] All customize strings use valid directive formats

#### Runtime Validation
- [ ] Agent contexts load successfully without errors
- [ ] Memory usage stays within configured limits
- [ ] Resource loading completes within timeout limits
- [ ] All agent dependencies are satisfied
- [ ] Configuration changes are detected and applied
- [ ] Error recovery mechanisms function correctly
- [ ] Performance metrics are within acceptable ranges

### 10. Configuration Management Best Practices

#### Version Control
- Store agent configurations in version control
- Use semantic versioning for configuration changes
- Maintain configuration change logs
- Test configuration changes in staging environments

#### Security Considerations
- Validate all file paths to prevent directory traversal
- Restrict access to configuration files
- Sanitize customize strings to prevent injection attacks
- Use secure file permissions for configuration directories

#### Performance Optimization
- Cache frequently accessed configurations
- Use lazy loading for large resource files
- Implement configuration hot-reloading for development
- Monitor memory usage and optimize context sizes

#### Maintenance Procedures
- Regular validation of all configuration references
- Periodic cleanup of unused configurations
- Performance monitoring and optimization
- Documentation updates for configuration changes
```
```
