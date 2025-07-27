# Manifest Generation Task

## Objective
Create and maintain the isaac_manifest.json configuration file that serves as the central definition for cross-platform installer generation, incorporating project analysis results and user customizations.

## Task Overview
This task transforms project analysis results into a structured, comprehensive manifest file that defines all aspects of the installation process, including dependencies, configuration parameters, target platforms, and installation steps.

## Process Steps

### 1. Manifest Structure Creation
**Purpose**: Establish the foundational structure of the isaac_manifest.json file

**Actions**:
- Initialize manifest with project metadata (name, version, description)
- Create technology stack section from project analysis results
- Establish dependency categories (runtime, system, development)
- Define configurable parameters structure with validation rules
- Set up target platform specifications
- Create installation steps framework

**Output**: Basic manifest structure with all required sections

### 2. Project Analysis Integration
**Purpose**: Populate manifest with data from project scanning results

**Actions**:
- Import detected technology stack information
- Map identified dependencies to manifest dependency structure
- Convert discovered configuration parameters to manifest format
- Integrate platform compatibility assessment results
- Import service and infrastructure requirements
- Validate imported data for completeness and accuracy

**Output**: Manifest populated with project-specific data

### 3. Platform-Specific Configuration
**Purpose**: Define platform-specific variations and requirements

**Actions**:
- Configure platform-specific dependency installation commands
- Define architecture-specific requirements (x64, ARM64, etc.)
- Set up platform-specific file paths and directory structures
- Configure service management approaches per platform
- Define platform-specific validation and testing procedures
- Establish platform-specific error handling strategies

**Output**: Complete platform configuration matrix

### 4. Interactive Parameter Definition
**Purpose**: Define user-configurable parameters with validation and defaults

**Actions**:
- Categorize configuration parameters by type and importance
- Define validation rules and input constraints
- Set appropriate default values based on common usage patterns
- Create parameter dependencies and conditional logic
- Define parameter grouping for organized user interaction
- Establish parameter documentation and help text

**Output**: Comprehensive parameter configuration system

### 5. Installation Step Orchestration
**Purpose**: Define the complete installation workflow with platform variations

**Actions**:
- Break down installation into logical, atomic steps
- Define step dependencies and execution order
- Create platform-specific command variations for each step
- Establish validation criteria for each installation step
- Define rollback procedures for failed steps
- Create progress tracking and user feedback mechanisms

**Output**: Complete installation workflow definition

## Manifest Schema Structure

### 1. Project Metadata
```json
{
  "project": {
    "name": "my-application",
    "version": "1.0.0",
    "description": "A sample web application",
    "author": "Development Team",
    "license": "MIT",
    "homepage": "https://github.com/org/my-app",
    "repository": {
      "type": "git",
      "url": "https://github.com/org/my-app.git"
    }
  }
}
```

### 2. Technology Stack Definition
```json
{
  "technology_stack": {
    "language": "Node.js",
    "version": ">=18.0.0",
    "framework": "Express",
    "framework_version": "^4.18.0",
    "package_manager": "npm",
    "build_system": "webpack",
    "runtime_environment": "node"
  }
}
```

### 3. Dependency Specification
```json
{
  "dependencies": {
    "runtime": [
      {
        "name": "nodejs",
        "version": ">=18.0.0",
        "required": true,
        "platform_specific": {
          "windows": {
            "install_command": "choco install nodejs",
            "verify_command": "node --version",
            "package_name": "nodejs"
          },
          "linux": {
            "install_command": "apt-get install -y nodejs npm",
            "verify_command": "node --version",
            "package_name": "nodejs"
          },
          "macos": {
            "install_command": "brew install node",
            "verify_command": "node --version",
            "package_name": "node"
          }
        }
      }
    ],
    "system": [
      {
        "name": "curl",
        "description": "HTTP client for downloads",
        "required": true,
        "platform_specific": {
          "windows": "Available by default in Windows 10+",
          "linux": "curl",
          "macos": "Available by default"
        }
      }
    ]
  }
}
```

### 4. Configuration Parameters
```json
{
  "configurable_parameters": [
    {
      "name": "SERVER_PORT",
      "type": "integer",
      "description": "Port number for the web server",
      "default": 3000,
      "required": false,
      "validation": {
        "min": 1024,
        "max": 65535,
        "pattern": "^[0-9]+$"
      },
      "prompt": "Enter server port",
      "help": "Choose a port between 1024-65535. Default is 3000."
    },
    {
      "name": "DATABASE_TYPE",
      "type": "choice",
      "description": "Database system to use",
      "default": "postgresql",
      "required": true,
      "choices": [
        {
          "value": "postgresql",
          "label": "PostgreSQL",
          "description": "Robust relational database"
        },
        {
          "value": "mysql",
          "label": "MySQL",
          "description": "Popular relational database"
        },
        {
          "value": "sqlite",
          "label": "SQLite",
          "description": "Lightweight file-based database"
        }
      ],
      "prompt": "Select database type",
      "help": "Choose the database system for your application."
    }
  ]
}
```

### 5. Target Platform Configuration
```json
{
  "target_platforms": [
    {
      "name": "linux_x64",
      "display_name": "Linux (64-bit)",
      "architecture": "x86_64",
      "os_family": "linux",
      "shell": "bash",
      "template": "bash_installer.sh.tpl",
      "package_managers": ["apt", "yum", "pacman"],
      "service_manager": "systemd"
    },
    {
      "name": "windows_amd64",
      "display_name": "Windows (64-bit)",
      "architecture": "amd64",
      "os_family": "windows",
      "shell": "powershell",
      "template": "powershell_installer.ps1.tpl",
      "package_managers": ["chocolatey", "winget"],
      "service_manager": "windows_service"
    }
  ]
}
```

### 6. Installation Steps
```json
{
  "installation_steps": [
    {
      "name": "system_check",
      "description": "Verify system requirements",
      "order": 1,
      "required": true,
      "commands": {
        "windows": "Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion",
        "linux": "uname -a && lsb_release -a",
        "macos": "sw_vers"
      },
      "validation": {
        "windows": "if ($LASTEXITCODE -eq 0) { Write-Host 'System check passed' }",
        "linux": "echo 'System check completed'",
        "macos": "echo 'System check completed'"
      }
    },
    {
      "name": "install_dependencies",
      "description": "Install required dependencies",
      "order": 2,
      "required": true,
      "depends_on": ["system_check"],
      "commands": {
        "windows": "choco install nodejs -y",
        "linux": "sudo apt-get update && sudo apt-get install -y nodejs npm",
        "macos": "brew install node"
      },
      "validation": {
        "windows": "node --version",
        "linux": "node --version && npm --version",
        "macos": "node --version && npm --version"
      },
      "rollback": {
        "windows": "choco uninstall nodejs -y",
        "linux": "sudo apt-get remove -y nodejs npm",
        "macos": "brew uninstall node"
      }
    }
  ]
}
```

## Validation & Quality Assurance

### Manifest Validation Rules
- [ ] All required sections are present and properly structured
- [ ] Project metadata is complete and accurate
- [ ] Technology stack information matches project analysis
- [ ] All dependencies have platform-specific installation commands
- [ ] Configuration parameters have proper validation rules
- [ ] Target platforms are supported and properly configured
- [ ] Installation steps are ordered and have proper dependencies

### Data Integrity Checks
- [ ] Version numbers follow semantic versioning
- [ ] Platform-specific commands are syntactically correct
- [ ] Parameter validation rules are logically consistent
- [ ] Installation step dependencies form a valid DAG
- [ ] Rollback procedures are defined for critical steps
- [ ] All referenced templates and resources exist

### User Experience Validation
- [ ] Parameter prompts are clear and helpful
- [ ] Default values are sensible for typical use cases
- [ ] Help text provides adequate guidance
- [ ] Error messages are actionable and specific
- [ ] Installation progress is clearly communicated

## Output Deliverables

### 1. Isaac Manifest File
- `isaac_manifest.json` - Complete configuration manifest
- `isaac_manifest.schema.json` - JSON schema for validation
- `isaac_manifest.example.json` - Example manifest with comments

### 2. Documentation
- `MANIFEST_GUIDE.md` - Comprehensive manifest documentation
- `PARAMETER_REFERENCE.md` - Configuration parameter reference
- `PLATFORM_GUIDE.md` - Platform-specific configuration guide

### 3. Validation Tools
- Manifest validation scripts
- Schema validation utilities
- Configuration testing tools

## Integration Points

### Input Sources
- Project analysis results from scanning task
- User customizations and preferences
- Template library and platform definitions
- Existing configuration files and documentation

### Output Consumers
- Script generation task (primary consumer)
- Template management system
- Validation and testing frameworks
- Documentation generation systems

## Maintenance & Updates

### Manifest Evolution
- **Version tracking**: Maintain manifest version history
- **Schema updates**: Handle manifest schema evolution
- **Migration tools**: Provide upgrade paths for manifest changes
- **Backward compatibility**: Ensure compatibility with older manifests

### Continuous Improvement
- **Usage analytics**: Track common configuration patterns
- **Error analysis**: Identify and resolve common manifest issues
- **Template updates**: Keep platform templates current
- **Best practices**: Evolve manifest patterns based on experience

## Error Handling

### Common Issues
- **Invalid JSON syntax**: Provide clear syntax error messages
- **Missing required fields**: Guide users to complete missing information
- **Invalid parameter values**: Validate against defined constraints
- **Platform incompatibilities**: Warn about unsupported combinations
- **Circular dependencies**: Detect and resolve step dependency cycles

### Recovery Strategies
- **Auto-correction**: Fix common formatting and syntax issues
- **Interactive repair**: Guide users through manifest corrections
- **Backup and restore**: Maintain manifest version history
- **Validation feedback**: Provide detailed validation reports
- **Template regeneration**: Recreate manifest from project analysis
