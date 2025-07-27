# Template Management Task

## Objective
Maintain, organize, and optimize a comprehensive library of cross-platform installer templates that can be dynamically customized and rendered for different target platforms, architectures, and deployment scenarios.

## Task Overview
This task manages the complete lifecycle of installer templates, from creation and customization to versioning and optimization, ensuring that all generated installers maintain consistency, quality, and platform-specific best practices.

## Process Steps

### 1. Template Library Organization
**Purpose**: Maintain a structured, searchable library of installer templates

**Actions**:
- Organize templates by platform, architecture, and use case
- Implement template versioning and change tracking
- Create template metadata and documentation systems
- Establish template inheritance and composition patterns
- Implement template validation and quality assurance
- Create template discovery and selection mechanisms

**Output**: Well-organized, documented template library

### 2. Template Development & Customization
**Purpose**: Create and maintain high-quality, flexible installer templates

**Actions**:
- Develop platform-specific template foundations
- Implement template variable systems and substitution mechanisms
- Create modular template components for reusability
- Design template inheritance hierarchies for code reuse
- Implement conditional logic and dynamic content generation
- Create template testing and validation frameworks

**Output**: Comprehensive set of customizable installer templates

### 3. Template Rendering Engine
**Purpose**: Transform templates into executable installer scripts

**Actions**:
- Implement template parsing and variable substitution
- Create conditional rendering based on configuration parameters
- Handle template inheritance and composition during rendering
- Implement error handling and validation during rendering
- Create template debugging and troubleshooting tools
- Optimize rendering performance for large templates

**Output**: Robust template rendering system

### 4. Template Validation & Quality Assurance
**Purpose**: Ensure all templates meet quality and functionality standards

**Actions**:
- Implement syntax validation for each template type
- Create functional testing frameworks for generated scripts
- Validate template compliance with platform best practices
- Test template rendering with various configuration scenarios
- Implement automated quality checks and linting
- Create template performance benchmarking

**Output**: Comprehensive template quality assurance system

### 5. Template Lifecycle Management
**Purpose**: Manage template evolution, updates, and deprecation

**Actions**:
- Implement template versioning and migration strategies
- Create template update and patch management systems
- Handle template deprecation and replacement workflows
- Implement template backup and recovery procedures
- Create template usage analytics and optimization insights
- Manage template dependencies and compatibility matrices

**Output**: Complete template lifecycle management system

## Template Architecture Framework

### 1. Template Structure Definition
```yaml
template_metadata:
  name: "bash_installer"
  version: "2.1.0"
  platform: "linux"
  architecture: ["x86_64", "arm64"]
  shell: "bash"
  description: "Comprehensive Linux installer template with systemd integration"
  author: "I.S.A.A.C. Template Team"
  created: "2025-01-23"
  updated: "2025-01-23"
  
template_variables:
  required:
    - app_name
    - app_version
    - install_path
    - service_user
  optional:
    - custom_port
    - database_type
    - enable_ssl
    
template_dependencies:
  - base_installer.sh.tpl
  - systemd_service.tpl
  - validation_functions.tpl
  
template_features:
  - interactive_configuration
  - progress_tracking
  - rollback_capability
  - service_management
  - validation_checks
```

### 2. Template Inheritance System
```bash
# Base template: base_installer.sh.tpl
#!/bin/bash
set -euo pipefail

# Template: Base Installer Framework
# Version: 1.0.0
# Description: Foundation template for all Linux installers

# Import common functions
{{> common_functions.tpl}}

# Configuration variables
{{#each config_variables}}
{{name}}="{{default_value}}"
{{/each}}

# Main installation function
main() {
    show_welcome
    {{> pre_flight_checks.tpl}}
    {{> collect_configuration.tpl}}
    {{> install_dependencies.tpl}}
    {{> configure_application.tpl}}
    {{> setup_service.tpl}}
    {{> validate_installation.tpl}}
    show_completion
}

# Child templates inherit and extend this structure
{{> platform_specific_extensions.tpl}}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### 3. Variable Substitution System
```python
class TemplateRenderer:
    def __init__(self, template_library):
        self.template_library = template_library
        self.variable_processors = {
            'string': self.process_string_variable,
            'integer': self.process_integer_variable,
            'boolean': self.process_boolean_variable,
            'array': self.process_array_variable,
            'object': self.process_object_variable
        }
    
    def render_template(self, template_name, variables):
        """
        Render a template with provided variables
        """
        template = self.template_library.get_template(template_name)
        
        # Validate required variables
        self.validate_required_variables(template, variables)
        
        # Process variables by type
        processed_vars = self.process_variables(template, variables)
        
        # Render template with processed variables
        rendered_content = self.substitute_variables(template.content, processed_vars)
        
        # Apply post-processing
        final_content = self.post_process_template(rendered_content, template)
        
        return final_content
    
    def substitute_variables(self, content, variables):
        """
        Substitute template variables with actual values
        """
        import re
        
        # Handle simple variable substitution {{variable_name}}
        def simple_substitution(match):
            var_name = match.group(1).strip()
            return str(variables.get(var_name, f"{{{{MISSING: {var_name}}}}}"))
        
        content = re.sub(r'\{\{([^}]+)\}\}', simple_substitution, content)
        
        # Handle conditional blocks {{#if condition}}...{{/if}}
        content = self.process_conditional_blocks(content, variables)
        
        # Handle loops {{#each array}}...{{/each}}
        content = self.process_loop_blocks(content, variables)
        
        return content
```

### 4. Modular Template Components
```bash
# Component: common_functions.tpl
# Reusable functions for all installer templates

log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE" >&2
}

check_root_privileges() {
    if [[ $EUID -eq 0 ]]; then
        log_error "This installer should not be run as root"
        exit 1
    fi
}

create_user() {
    local username="$1"
    local home_dir="$2"
    
    if ! id "$username" &>/dev/null; then
        log_info "Creating user: $username"
        sudo useradd -r -m -d "$home_dir" -s /bin/bash "$username"
    else
        log_info "User $username already exists"
    fi
}

# Component: systemd_service.tpl
# Systemd service configuration template

create_systemd_service() {
    local service_name="{{app_name}}"
    local service_file="/etc/systemd/system/${service_name}.service"
    
    log_info "Creating systemd service: $service_name"
    
    sudo tee "$service_file" > /dev/null << EOF
[Unit]
Description={{app_description}}
After=network.target
{{#if database_required}}
After=postgresql.service mysql.service
{{/if}}

[Service]
Type={{service_type}}
User={{service_user}}
Group={{service_group}}
WorkingDirectory={{install_path}}
ExecStart={{install_path}}/bin/{{app_name}}
{{#if custom_port}}
Environment=PORT={{custom_port}}
{{/if}}
{{#each environment_variables}}
Environment={{name}}={{value}}
{{/each}}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable "$service_name"
}
```

### 5. Template Validation Framework
```python
class TemplateValidator:
    def __init__(self):
        self.validation_rules = {
            'bash': self.validate_bash_template,
            'powershell': self.validate_powershell_template,
            'batch': self.validate_batch_template
        }
    
    def validate_template(self, template):
        """
        Validate a template for syntax and best practices
        """
        validation_results = []
        
        # Syntax validation
        syntax_result = self.validate_syntax(template)
        validation_results.append(syntax_result)
        
        # Variable validation
        variable_result = self.validate_variables(template)
        validation_results.append(variable_result)
        
        # Security validation
        security_result = self.validate_security(template)
        validation_results.append(security_result)
        
        # Best practices validation
        practices_result = self.validate_best_practices(template)
        validation_results.append(practices_result)
        
        return self.aggregate_results(validation_results)
    
    def validate_bash_template(self, template):
        """
        Validate bash-specific template requirements
        """
        issues = []
        
        # Check for proper shebang
        if not template.content.startswith('#!/bin/bash'):
            issues.append("Missing or incorrect shebang")
        
        # Check for set -euo pipefail
        if 'set -euo pipefail' not in template.content:
            issues.append("Missing error handling: set -euo pipefail")
        
        # Check for proper variable quoting
        unquoted_vars = self.find_unquoted_variables(template.content)
        if unquoted_vars:
            issues.extend([f"Unquoted variable: {var}" for var in unquoted_vars])
        
        return ValidationResult(
            template_name=template.name,
            issues=issues,
            severity="high" if issues else "none"
        )
```

## Platform-Specific Template Implementations

### 1. Windows PowerShell Template
```powershell
# Template: powershell_installer.ps1.tpl
# Windows PowerShell installer template

#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$ConfigFile = "installer_config.json"
)

# Set error handling
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Import configuration
{{> load_configuration.ps1.tpl}}

# Main installation function
function Install-Application {
    [CmdletBinding()]
    param()
    
    try {
        Write-Host "Starting {{app_name}} installation..." -ForegroundColor Green
        
        # Pre-flight checks
        {{> windows_preflight_checks.ps1.tpl}}
        
        # Collect configuration
        {{> windows_configuration.ps1.tpl}}
        
        # Install dependencies
        {{> windows_dependencies.ps1.tpl}}
        
        # Configure application
        {{> windows_application_setup.ps1.tpl}}
        
        # Setup Windows service
        {{> windows_service_setup.ps1.tpl}}
        
        # Validate installation
        {{> windows_validation.ps1.tpl}}
        
        Write-Host "Installation completed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Error "Installation failed: $($_.Exception.Message)"
        {{> windows_rollback.ps1.tpl}}
        exit 1
    }
}

# Execute installation
Install-Application
```

### 2. macOS Bash Template
```bash
#!/bin/bash
# Template: macos_installer.sh.tpl
# macOS-specific installer template

set -euo pipefail

# macOS-specific configurations
readonly MACOS_VERSION=$(sw_vers -productVersion)
readonly HOMEBREW_PREFIX=$(brew --prefix 2>/dev/null || echo "/opt/homebrew")

# Import common functions
{{> common_functions.tpl}}
{{> macos_functions.tpl}}

# macOS-specific functions
setup_macos_environment() {
    log_info "Setting up macOS environment"
    
    # Check macOS version compatibility
    if ! version_compare "$MACOS_VERSION" ">=10.15"; then
        log_error "macOS 10.15 or later is required"
        exit 1
    fi
    
    # Ensure Homebrew is available
    if ! command -v brew >/dev/null 2>&1; then
        log_info "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Update Homebrew
    log_info "Updating Homebrew..."
    brew update
}

# macOS service management
setup_launchd_service() {
    local service_name="{{app_name}}"
    local plist_file="$HOME/Library/LaunchAgents/com.{{company}}.${service_name}.plist"
    
    log_info "Creating launchd service: $service_name"
    
    cat > "$plist_file" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{{company}}.{{app_name}}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{{install_path}}/bin/{{app_name}}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{{install_path}}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF
    
    # Load the service
    launchctl load "$plist_file"
    launchctl start "com.{{company}}.{{app_name}}"
}
```

## Quality Assurance & Testing

### Template Testing Framework
```python
class TemplateTestSuite:
    def __init__(self, template_library):
        self.template_library = template_library
        self.test_scenarios = self.load_test_scenarios()
    
    def run_template_tests(self, template_name):
        """
        Run comprehensive tests for a template
        """
        template = self.template_library.get_template(template_name)
        test_results = []
        
        # Syntax tests
        syntax_result = self.test_template_syntax(template)
        test_results.append(syntax_result)
        
        # Rendering tests
        for scenario in self.test_scenarios:
            render_result = self.test_template_rendering(template, scenario)
            test_results.append(render_result)
        
        # Integration tests
        integration_result = self.test_template_integration(template)
        test_results.append(integration_result)
        
        return self.aggregate_test_results(test_results)
    
    def test_template_rendering(self, template, scenario):
        """
        Test template rendering with specific scenario
        """
        try:
            rendered = self.template_library.render_template(
                template.name, 
                scenario.variables
            )
            
            # Validate rendered output
            validation_result = self.validate_rendered_output(rendered, scenario)
            
            return TestResult(
                test_name=f"render_{scenario.name}",
                passed=validation_result.is_valid,
                details=validation_result.details
            )
        except Exception as e:
            return TestResult(
                test_name=f"render_{scenario.name}",
                passed=False,
                details=f"Rendering failed: {str(e)}"
            )
```

## Integration Points

### Input Sources
- Template source files and components
- Platform-specific requirements and best practices
- User configuration and customization requests
- Template usage analytics and feedback

### Output Consumers
- Script generation system (primary consumer)
- Template validation and testing frameworks
- Documentation generation systems
- Template distribution and packaging systems

## Performance Optimization

### Template Rendering Performance
- **Caching**: Cache compiled templates and partial renders
- **Lazy loading**: Load template components only when needed
- **Parallel processing**: Render independent templates concurrently
- **Template compilation**: Pre-compile templates for faster rendering
- **Memory optimization**: Efficient memory usage during rendering

### Template Management Efficiency
- **Indexing**: Create searchable indexes for template discovery
- **Compression**: Compress template storage for space efficiency
- **Version control**: Efficient storage of template versions
- **Dependency tracking**: Optimize template dependency resolution
- **Update propagation**: Efficient template update distribution

## Error Handling & Recovery

### Template Error Management
- **Syntax errors**: Clear error messages with line numbers
- **Variable errors**: Detailed missing variable reports
- **Rendering failures**: Graceful degradation and fallback options
- **Template conflicts**: Resolution strategies for conflicting templates
- **Version incompatibilities**: Migration and compatibility guidance

### Recovery Mechanisms
- **Template rollback**: Revert to previous working versions
- **Partial rendering**: Continue with available components
- **Error isolation**: Prevent template errors from affecting others
- **Automatic repair**: Fix common template issues automatically
- **Manual intervention**: Clear guidance for manual template fixes
