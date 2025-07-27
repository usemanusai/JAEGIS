# Isaac Manifest Template

## Overview
The Isaac Manifest Template provides the foundational structure for the `isaac_manifest.json` file that serves as the central configuration for cross-platform installer generation. This template ensures consistency and completeness across all project configurations.

## Template Structure

### Complete Isaac Manifest Template
```json
{
  "manifest_version": "1.0.0",
  "generated_at": "{{current_timestamp}}",
  "generated_by": "I.S.A.A.C. v{{isaac_version}}",
  
  "project": {
    "name": "{{project_name}}",
    "version": "{{project_version}}",
    "description": "{{project_description}}",
    "author": "{{project_author}}",
    "license": "{{project_license}}",
    "homepage": "{{project_homepage}}",
    "repository": {
      "type": "{{repository_type}}",
      "url": "{{repository_url}}"
    },
    "keywords": [{{#each project_keywords}}"{{this}}"{{#unless @last}},{{/unless}}{{/each}}]
  },
  
  "technology_stack": {
    "language": "{{detected_language}}",
    "version": "{{language_version}}",
    "framework": "{{detected_framework}}",
    "framework_version": "{{framework_version}}",
    "package_manager": "{{detected_package_manager}}",
    "build_system": "{{build_system}}",
    "runtime_environment": "{{runtime_environment}}",
    "additional_tools": [
      {{#each additional_tools}}
      {
        "name": "{{name}}",
        "version": "{{version}}",
        "required": {{required}}
      }{{#unless @last}},{{/unless}}
      {{/each}}
    ]
  },
  
  "dependencies": {
    "runtime": [
      {{#each runtime_dependencies}}
      {
        "name": "{{name}}",
        "version": "{{version}}",
        "required": {{required}},
        "description": "{{description}}",
        "platform_specific": {
          "windows": {
            "package_name": "{{windows.package_name}}",
            "package_manager": "{{windows.package_manager}}",
            "install_command": "{{windows.install_command}}",
            "verify_command": "{{windows.verify_command}}",
            "uninstall_command": "{{windows.uninstall_command}}"
          },
          "linux": {
            "package_name": "{{linux.package_name}}",
            "package_manager": "{{linux.package_manager}}",
            "install_command": "{{linux.install_command}}",
            "verify_command": "{{linux.verify_command}}",
            "uninstall_command": "{{linux.uninstall_command}}",
            "distributions": {
              "ubuntu": {
                "package_name": "{{linux.ubuntu.package_name}}",
                "install_command": "{{linux.ubuntu.install_command}}"
              },
              "centos": {
                "package_name": "{{linux.centos.package_name}}",
                "install_command": "{{linux.centos.install_command}}"
              }
            }
          },
          "macos": {
            "package_name": "{{macos.package_name}}",
            "package_manager": "{{macos.package_manager}}",
            "install_command": "{{macos.install_command}}",
            "verify_command": "{{macos.verify_command}}",
            "uninstall_command": "{{macos.uninstall_command}}"
          }
        }
      }{{#unless @last}},{{/unless}}
      {{/each}}
    ],
    "system": [
      {{#each system_dependencies}}
      {
        "name": "{{name}}",
        "description": "{{description}}",
        "required": {{required}},
        "minimum_version": "{{minimum_version}}",
        "platform_availability": {
          "windows": "{{windows_availability}}",
          "linux": "{{linux_availability}}",
          "macos": "{{macos_availability}}"
        }
      }{{#unless @last}},{{/unless}}
      {{/each}}
    ],
    "development": [
      {{#each development_dependencies}}
      {
        "name": "{{name}}",
        "version": "{{version}}",
        "description": "{{description}}",
        "optional": {{optional}}
      }{{#unless @last}},{{/unless}}
      {{/each}}
    ]
  },
  
  "configurable_parameters": [
    {{#each configurable_parameters}}
    {
      "name": "{{name}}",
      "type": "{{type}}",
      "description": "{{description}}",
      "default": {{#if (eq type "string")}}"{{default}}"{{else}}{{default}}{{/if}},
      "required": {{required}},
      "validation": {
        {{#if validation.pattern}}"pattern": "{{validation.pattern}}",{{/if}}
        {{#if validation.min}}"min": {{validation.min}},{{/if}}
        {{#if validation.max}}"max": {{validation.max}},{{/if}}
        {{#if validation.choices}}"choices": [{{#each validation.choices}}"{{this}}"{{#unless @last}},{{/unless}}{{/each}}]{{/if}}
      },
      "prompt": "{{prompt}}",
      "help": "{{help}}",
      {{#if depends_on}}"depends_on": "{{depends_on}}",{{/if}}
      "category": "{{category}}"
    }{{#unless @last}},{{/unless}}
    {{/each}}
  ],
  
  "target_platforms": [
    {{#each target_platforms}}
    {
      "name": "{{name}}",
      "display_name": "{{display_name}}",
      "architecture": "{{architecture}}",
      "os_family": "{{os_family}}",
      "shell": "{{shell}}",
      "template": "{{template}}",
      "package_managers": [{{#each package_managers}}"{{this}}"{{#unless @last}},{{/unless}}{{/each}}],
      "service_manager": "{{service_manager}}",
      "supported": {{supported}},
      "requirements": [{{#each requirements}}"{{this}}"{{#unless @last}},{{/unless}}{{/each}}]
    }{{#unless @last}},{{/unless}}
    {{/each}}
  ],
  
  "installation_steps": [
    {{#each installation_steps}}
    {
      "name": "{{name}}",
      "description": "{{description}}",
      "order": {{order}},
      "required": {{required}},
      "category": "{{category}}",
      {{#if depends_on}}"depends_on": [{{#each depends_on}}"{{this}}"{{#unless @last}},{{/unless}}{{/each}}],{{/if}}
      "commands": {
        "windows": "{{commands.windows}}",
        "linux": "{{commands.linux}}",
        "macos": "{{commands.macos}}"
      },
      "validation": {
        "windows": "{{validation.windows}}",
        "linux": "{{validation.linux}}",
        "macos": "{{validation.macos}}"
      },
      {{#if rollback}}"rollback": {
        "windows": "{{rollback.windows}}",
        "linux": "{{rollback.linux}}",
        "macos": "{{rollback.macos}}"
      },{{/if}}
      "timeout": {{timeout}},
      "retry_count": {{retry_count}},
      "critical": {{critical}}
    }{{#unless @last}},{{/unless}}
    {{/each}}
  ],
  
  "configuration": {
    "installer_settings": {
      "interactive_mode": {{interactive_mode}},
      "progress_reporting": {{progress_reporting}},
      "log_level": "{{log_level}}",
      "backup_existing": {{backup_existing}},
      "rollback_on_failure": {{rollback_on_failure}},
      "validate_after_install": {{validate_after_install}}
    },
    "security": {
      "require_admin": {{require_admin}},
      "verify_signatures": {{verify_signatures}},
      "secure_temp_files": {{secure_temp_files}},
      "credential_handling": "{{credential_handling}}"
    },
    "performance": {
      "parallel_operations": {{parallel_operations}},
      "download_timeout": {{download_timeout}},
      "max_retries": {{max_retries}},
      "cache_downloads": {{cache_downloads}}
    }
  },
  
  "metadata": {
    "created_at": "{{created_at}}",
    "updated_at": "{{updated_at}}",
    "isaac_version": "{{isaac_version}}",
    "template_version": "{{template_version}}",
    "checksum": "{{manifest_checksum}}",
    "validation_status": "{{validation_status}}"
  }
}
```

## Template Variables Reference

### Project Information Variables
- `{{project_name}}` - Name of the project/application
- `{{project_version}}` - Current version of the project
- `{{project_description}}` - Brief description of the project
- `{{project_author}}` - Author or organization name
- `{{project_license}}` - License type (MIT, Apache, etc.)
- `{{project_homepage}}` - Project homepage URL
- `{{repository_type}}` - Version control system (git, svn, etc.)
- `{{repository_url}}` - Repository URL
- `{{project_keywords}}` - Array of project keywords/tags

### Technology Stack Variables
- `{{detected_language}}` - Primary programming language
- `{{language_version}}` - Required language version
- `{{detected_framework}}` - Main framework used
- `{{framework_version}}` - Framework version requirement
- `{{detected_package_manager}}` - Package manager (npm, pip, etc.)
- `{{build_system}}` - Build system (webpack, gradle, etc.)
- `{{runtime_environment}}` - Runtime environment (node, jvm, etc.)

### Dependency Variables
- `{{runtime_dependencies}}` - Array of runtime dependencies
- `{{system_dependencies}}` - Array of system-level dependencies
- `{{development_dependencies}}` - Array of development dependencies

### Configuration Variables
- `{{configurable_parameters}}` - Array of user-configurable parameters
- `{{target_platforms}}` - Array of supported target platforms
- `{{installation_steps}}` - Array of installation step definitions

### Metadata Variables
- `{{current_timestamp}}` - Current timestamp in ISO format
- `{{isaac_version}}` - Version of I.S.A.A.C. generating the manifest
- `{{created_at}}` - Manifest creation timestamp
- `{{updated_at}}` - Last modification timestamp
- `{{manifest_checksum}}` - SHA-256 checksum of manifest content

## Usage Examples

### Basic Node.js Application Manifest
```json
{
  "project": {
    "name": "my-web-app",
    "version": "1.0.0",
    "description": "A modern web application",
    "author": "Development Team"
  },
  "technology_stack": {
    "language": "Node.js",
    "version": ">=18.0.0",
    "framework": "Express",
    "package_manager": "npm"
  },
  "configurable_parameters": [
    {
      "name": "SERVER_PORT",
      "type": "integer",
      "description": "Port for the web server",
      "default": 3000,
      "required": false,
      "validation": {
        "min": 1024,
        "max": 65535
      },
      "prompt": "Enter server port"
    }
  ]
}
```

### Python Django Application Manifest
```json
{
  "project": {
    "name": "django-blog",
    "version": "2.1.0",
    "description": "Django-based blog application"
  },
  "technology_stack": {
    "language": "Python",
    "version": ">=3.9",
    "framework": "Django",
    "package_manager": "pip"
  },
  "configurable_parameters": [
    {
      "name": "DATABASE_TYPE",
      "type": "choice",
      "description": "Database system to use",
      "default": "postgresql",
      "required": true,
      "validation": {
        "choices": ["postgresql", "mysql", "sqlite"]
      },
      "prompt": "Select database type"
    }
  ]
}
```

## Template Customization

### Adding Custom Parameters
```json
{
  "name": "CUSTOM_SETTING",
  "type": "string",
  "description": "Custom application setting",
  "default": "default_value",
  "required": false,
  "validation": {
    "pattern": "^[a-zA-Z0-9_]+$"
  },
  "prompt": "Enter custom setting value",
  "help": "This setting controls custom application behavior",
  "category": "advanced"
}
```

### Platform-Specific Dependencies
```json
{
  "name": "database_client",
  "version": ">=1.0.0",
  "required": true,
  "platform_specific": {
    "windows": {
      "package_name": "postgresql-client",
      "install_command": "choco install postgresql-client"
    },
    "linux": {
      "package_name": "postgresql-client",
      "install_command": "sudo apt-get install postgresql-client"
    },
    "macos": {
      "package_name": "postgresql",
      "install_command": "brew install postgresql"
    }
  }
}
```

## Validation Rules

### Required Fields
- `project.name` - Must be a valid identifier
- `project.version` - Must follow semantic versioning
- `technology_stack.language` - Must be a supported language
- `target_platforms` - Must include at least one platform

### Validation Constraints
- Parameter names must be valid environment variable names
- Version specifications must follow semantic versioning
- Platform-specific commands must be valid for their respective shells
- Installation step dependencies must form a valid directed acyclic graph

## Best Practices

### Manifest Organization
1. **Logical Grouping**: Group related parameters by category
2. **Clear Descriptions**: Provide helpful descriptions for all parameters
3. **Sensible Defaults**: Set appropriate default values for optional parameters
4. **Validation Rules**: Include proper validation for all user inputs
5. **Platform Coverage**: Ensure all target platforms are properly configured

### Parameter Design
1. **User-Friendly Names**: Use clear, descriptive parameter names
2. **Type Safety**: Specify correct parameter types with validation
3. **Help Text**: Provide helpful guidance for complex parameters
4. **Dependencies**: Clearly define parameter dependencies
5. **Categories**: Organize parameters into logical categories

### Maintenance
1. **Version Control**: Track manifest changes with version numbers
2. **Documentation**: Keep parameter documentation up to date
3. **Testing**: Validate manifest with different parameter combinations
4. **Migration**: Provide migration paths for manifest updates
5. **Backup**: Maintain backups of working manifest configurations
