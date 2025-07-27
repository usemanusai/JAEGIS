# Directory Structure Template
## Standardized Project Organization Framework

### Template Overview
This template provides a comprehensive framework for creating consistent, scalable directory structures across different project types. It serves as the foundation for automated project scaffolding and ensures organizational consistency.

### Template Categories

#### 1. Python ML Project Template
```yaml
python_ml_project:
  metadata:
    name: "python-ml-project"
    version: "2.1.0"
    description: "Machine Learning project with modern Python tooling"
    last_updated: "2025-07-24"
    compatibility: ["Python 3.9+", "Poetry", "Docker", "Jupyter"]
    target_audience: "Data Scientists, ML Engineers, Research Teams"
  
  directory_structure:
    root: "/"
    core_directories:
      - path: ".github/workflows/"
        purpose: "CI/CD pipeline configurations"
        permissions: "644"
        auto_create: true
        
      - path: "src/"
        purpose: "Main source code directory"
        permissions: "755"
        subdirectories:
          - "data/"           # Raw and processed datasets
          - "models/"         # Trained models and artifacts
          - "notebooks/"      # Jupyter notebooks for exploration
          - "scripts/"        # Standalone processing scripts
          - "utils/"          # Helper functions and shared utilities
          - "tests/"          # Unit and integration tests
          
      - path: "docs/"
        purpose: "Project documentation"
        permissions: "755"
        subdirectories:
          - "api/"            # API documentation
          - "guides/"         # User guides and tutorials
          - "architecture/"   # System architecture docs
          
      - path: "config/"
        purpose: "Configuration files"
        permissions: "644"
        subdirectories:
          - "environments/"   # Environment-specific configs
          - "models/"         # Model configuration files
          
      - path: "staging/"
        purpose: "File classification inbox for Classifico agent"
        permissions: "777"
        monitoring: "real_time_file_events"
        
      - path: "logs/"
        purpose: "Application and system logs"
        permissions: "755"
        retention_policy: "30_days"
        
      - path: "results/"
        purpose: "Experiment outputs and analysis results"
        permissions: "755"
        subdirectories:
          - "experiments/"    # Experiment results
          - "reports/"        # Generated reports
          - "visualizations/" # Charts and graphs
  
  configuration_files:
    - name: ".gitignore"
      template: "python_ml_gitignore"
      purpose: "Version control exclusions"
      
    - name: "README.md"
      template: "python_ml_readme"
      purpose: "Project overview and setup instructions"
      
    - name: "pyproject.toml"
      template: "python_ml_pyproject"
      purpose: "Python project configuration and dependencies"
      
    - name: "environment.yml"
      template: "conda_environment"
      purpose: "Conda environment specification"
      
    - name: "Dockerfile"
      template: "python_ml_dockerfile"
      purpose: "Container configuration"
      
    - name: "docker-compose.yml"
      template: "ml_docker_compose"
      purpose: "Multi-container orchestration"
      
    - name: "Makefile"
      template: "python_ml_makefile"
      purpose: "Build and automation commands"
```

#### 2. Web Application Template
```yaml
web_application:
  metadata:
    name: "modern-web-app"
    version: "2.0.0"
    description: "Modern web application with TypeScript and React/Vue/Angular"
    compatibility: ["Node.js 18+", "TypeScript", "Modern Frameworks"]
    target_audience: "Frontend Developers, Full-Stack Teams"
  
  directory_structure:
    root: "/"
    core_directories:
      - path: "src/"
        purpose: "Source code directory"
        subdirectories:
          - "components/"     # Reusable UI components
          - "pages/"          # Page components
          - "hooks/"          # Custom React hooks
          - "utils/"          # Utility functions
          - "services/"       # API services and data layer
          - "types/"          # TypeScript type definitions
          - "assets/"         # Static assets (images, fonts)
          - "styles/"         # CSS/SCSS stylesheets
          - "tests/"          # Test files
          
      - path: "public/"
        purpose: "Public static assets"
        permissions: "644"
        
      - path: "docs/"
        purpose: "Documentation"
        subdirectories:
          - "components/"     # Component documentation
          - "api/"            # API documentation
          - "deployment/"     # Deployment guides
          
      - path: "scripts/"
        purpose: "Build and utility scripts"
        permissions: "755"
        
      - path: "staging/"
        purpose: "File classification inbox"
        permissions: "777"
        monitoring: "enabled"
  
  configuration_files:
    - name: "package.json"
      template: "web_app_package_json"
      purpose: "Node.js project configuration"
      
    - name: "tsconfig.json"
      template: "typescript_config"
      purpose: "TypeScript compiler configuration"
      
    - name: "vite.config.ts"
      template: "vite_configuration"
      purpose: "Build tool configuration"
      
    - name: ".eslintrc.js"
      template: "eslint_config"
      purpose: "Code linting rules"
      
    - name: ".prettierrc"
      template: "prettier_config"
      purpose: "Code formatting rules"
```

#### 3. Research Project Template
```yaml
research_project:
  metadata:
    name: "academic-research"
    version: "1.5.0"
    description: "Academic research project with LaTeX and data analysis"
    compatibility: ["LaTeX", "R/Python", "Reference Management"]
    target_audience: "Researchers, Academics, Graduate Students"
  
  directory_structure:
    root: "/"
    core_directories:
      - path: "manuscript/"
        purpose: "Main research manuscript"
        subdirectories:
          - "sections/"       # Individual manuscript sections
          - "figures/"        # Manuscript figures
          - "tables/"         # Data tables
          - "references/"     # Bibliography files
          
      - path: "data/"
        purpose: "Research data"
        subdirectories:
          - "raw/"            # Original, unprocessed data
          - "processed/"      # Cleaned and processed data
          - "external/"       # External datasets
          
      - path: "analysis/"
        purpose: "Data analysis scripts and notebooks"
        subdirectories:
          - "scripts/"        # Analysis scripts
          - "notebooks/"      # Jupyter/R notebooks
          - "results/"        # Analysis outputs
          
      - path: "literature/"
        purpose: "Literature review and references"
        subdirectories:
          - "papers/"         # Collected research papers
          - "notes/"          # Literature notes
          - "summaries/"      # Paper summaries
          
      - path: "staging/"
        purpose: "File classification inbox"
        permissions: "777"
        
      - path: "presentations/"
        purpose: "Conference presentations and talks"
        subdirectories:
          - "conferences/"    # Conference presentations
          - "seminars/"       # Seminar talks
          - "posters/"        # Research posters
  
  configuration_files:
    - name: "main.tex"
      template: "latex_main_document"
      purpose: "Main LaTeX document"
      
    - name: "bibliography.bib"
      template: "bibtex_bibliography"
      purpose: "Reference bibliography"
      
    - name: "requirements.txt"
      template: "research_python_requirements"
      purpose: "Python dependencies for analysis"
```

### Template Customization Framework

#### Dynamic Template Generation
```python
def customize_template(base_template, customization_parameters):
    """
    Dynamically customize templates based on project requirements
    """
    customization_options = {
        'project_scale': {
            'solo': 'simplified_structure_with_minimal_overhead',
            'small_team': 'collaborative_structure_with_shared_resources',
            'large_team': 'enterprise_structure_with_role_separation',
            'enterprise': 'full_governance_structure_with_compliance'
        },
        'technology_stack': {
            'python': 'python_specific_configurations_and_tools',
            'javascript': 'node_js_and_frontend_optimizations',
            'java': 'maven_gradle_enterprise_java_structure',
            'mixed': 'polyglot_project_structure_with_language_separation'
        },
        'deployment_target': {
            'local': 'development_focused_structure',
            'cloud': 'cloud_native_structure_with_containerization',
            'hybrid': 'flexible_structure_supporting_multiple_targets',
            'edge': 'lightweight_structure_for_edge_deployment'
        }
    }
    
    customized_template = apply_customizations(base_template, customization_options)
    return customized_template
```

#### Template Validation Rules
```yaml
validation_rules:
  required_directories:
    - "staging/"              # Required for file organization system
    - "docs/"                 # Documentation is mandatory
    - source_directory        # At least one source code directory
    
  naming_conventions:
    directory_names: "lowercase_with_underscores_or_hyphens"
    file_names: "descriptive_names_with_appropriate_extensions"
    configuration_files: "standard_names_for_tool_recognition"
    
  permission_requirements:
    staging_directory: "read_write_all_team_members"
    source_directories: "read_write_developers"
    configuration_files: "read_all_write_maintainers"
    
  structure_constraints:
    maximum_depth: 5          # Prevent overly nested structures
    minimum_directories: 3    # Ensure adequate organization
    staging_accessibility: true  # Staging must be accessible to all agents
```

### Template Integration Points

#### Classifico Integration
```yaml
classifico_integration:
  classification_rules:
    - template_type: "python_ml_project"
      rules:
        - "*.py with 'import pandas' -> src/data/"
        - "*.py with 'class.*Model' -> src/models/"
        - "*.ipynb -> src/notebooks/"
        - "*.csv -> src/data/raw/"
        - "*.pkl -> src/models/"
        
    - template_type: "web_application"
      rules:
        - "*.tsx with 'export default' -> src/components/"
        - "*.ts with 'service' in name -> src/services/"
        - "*.css -> src/styles/"
        - "*.test.* -> src/tests/"
        - "*.json with 'dependencies' -> root/"
```

#### Locomoto Integration
```yaml
locomoto_integration:
  directory_permissions:
    - path: "staging/"
      permissions: "777"
      purpose: "file_intake_and_processing"
      
    - path: "src/"
      permissions: "755"
      purpose: "source_code_management"
      
    - path: "docs/"
      permissions: "755"
      purpose: "documentation_collaboration"
  
  file_movement_rules:
    - source: "staging/"
      destinations: "all_project_directories"
      validation: "required_before_movement"
      
    - backup_locations:
      - "backups/daily/"
      - "backups/weekly/"
      - "backups/monthly/"
```

#### Purgo Integration
```yaml
purgo_integration:
  hygiene_monitoring:
    - directory: "staging/"
      max_age: "24_hours"
      action: "alert_if_files_remain_too_long"
      
    - directory: "logs/"
      retention: "30_days"
      action: "automatic_cleanup_of_old_logs"
      
    - directory: "temp/"
      max_age: "7_days"
      action: "automatic_removal_of_temporary_files"
  
  structure_validation:
    - check: "empty_directories"
      grace_period: "7_days"
      exceptions: ["staging/", "logs/", "temp/"]
      
    - check: "naming_conventions"
      enforcement: "flag_violations_for_review"
      
    - check: "permission_consistency"
      enforcement: "automatic_correction_where_safe"
```

### Success Metrics

#### Template Quality Standards
- ✅ **Completeness**: All necessary directories and files included
- ✅ **Scalability**: Structure supports project growth without reorganization
- ✅ **Consistency**: Standardized patterns across similar project types
- ✅ **Maintainability**: Clear organization facilitates long-term maintenance

#### Usage Metrics
- ✅ **Adoption Rate**: 90%+ of new projects use template-based initialization
- ✅ **Customization Success**: 95%+ of templates successfully customized for specific needs
- ✅ **Developer Satisfaction**: 85%+ approval rating for generated structures
- ✅ **Maintenance Efficiency**: 50%+ reduction in manual directory organization time

This template framework ensures consistent, well-organized project structures that support efficient development workflows and automated file organization processes.
