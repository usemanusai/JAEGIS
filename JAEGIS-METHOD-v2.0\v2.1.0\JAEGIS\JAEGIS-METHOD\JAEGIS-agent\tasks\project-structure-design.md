# Project Structure Design
## Intelligent Directory Architecture & Template Selection

### Task Overview
Design and create optimal directory structures for new projects based on comprehensive analysis of project requirements, technology stack, team size, and organizational standards. This task transforms project initialization from ad-hoc directory creation to systematic, template-driven architecture design.

### Core Objectives
1. **Analyze project requirements** to determine optimal directory structure
2. **Select appropriate golden templates** from comprehensive template library
3. **Customize directory architecture** based on specific project needs
4. **Generate complete project foundation** with all necessary directories and files
5. **Ensure scalability and maintainability** of the created structure

### Input Requirements

#### Project Analysis Parameters
```yaml
project_context:
  basic_information:
    - project_name: "string"
    - project_type: "web_app | ml_project | research | documentation | infrastructure"
    - primary_language: "python | javascript | java | c++ | rust | go | other"
    - framework_stack: ["react", "django", "tensorflow", "docker"]
  
  team_context:
    - team_size: "solo | small_team | large_team | enterprise"
    - collaboration_model: "centralized | distributed | hybrid"
    - experience_level: "beginner | intermediate | expert | mixed"
  
  technical_requirements:
    - deployment_target: "local | cloud | hybrid | edge"
    - ci_cd_requirements: "basic | advanced | enterprise"
    - testing_framework: "unit | integration | e2e | all"
    - documentation_needs: "minimal | standard | comprehensive"
  
  organizational_constraints:
    - naming_conventions: "camelCase | snake_case | kebab-case | custom"
    - compliance_requirements: ["GDPR", "HIPAA", "SOX", "ISO27001"]
    - security_standards: "basic | enhanced | enterprise"
```

### Execution Workflow

#### Phase 1: Project Analysis (2-3 minutes)
```python
def analyze_project_requirements(project_context):
    """
    Comprehensive analysis of project requirements for optimal structure design
    """
    analysis_results = {
        'technology_profile': {
            'primary_stack': identify_primary_technology_stack(project_context),
            'framework_dependencies': extract_framework_requirements(project_context),
            'build_system_needs': determine_build_system_requirements(project_context),
            'testing_requirements': analyze_testing_framework_needs(project_context)
        },
        'scale_assessment': {
            'project_complexity': assess_project_complexity(project_context),
            'team_collaboration_needs': evaluate_team_requirements(project_context),
            'growth_projection': predict_project_growth_patterns(project_context),
            'maintenance_requirements': estimate_maintenance_needs(project_context)
        },
        'compliance_analysis': {
            'regulatory_requirements': identify_compliance_needs(project_context),
            'security_standards': determine_security_requirements(project_context),
            'audit_trail_needs': assess_audit_requirements(project_context),
            'documentation_standards': evaluate_documentation_needs(project_context)
        }
    }
    return analysis_results
```

#### Phase 2: Template Selection & Customization (3-5 minutes)
```python
def select_and_customize_template(analysis_results, available_templates):
    """
    Intelligent template selection and customization based on project analysis
    """
    # Template matching algorithm
    template_scores = {}
    for template in available_templates:
        compatibility_score = calculate_template_compatibility(
            template, analysis_results
        )
        template_scores[template.name] = compatibility_score
    
    # Select best matching template
    optimal_template = select_highest_scoring_template(template_scores)
    
    # Customize template based on specific requirements
    customized_structure = customize_template_structure(
        optimal_template, analysis_results
    )
    
    return customized_structure
```

#### Phase 3: Structure Generation (2-4 minutes)
```python
def generate_project_structure(customized_structure, project_context):
    """
    Create complete directory structure with all necessary files
    """
    generation_plan = {
        'directory_creation': create_directory_hierarchy(customized_structure),
        'configuration_files': generate_config_files(customized_structure, project_context),
        'documentation_setup': create_documentation_structure(customized_structure),
        'development_environment': setup_dev_environment(customized_structure),
        'staging_area': create_staging_directory_for_classifico()
    }
    
    execute_generation_plan(generation_plan)
    validate_structure_integrity(generation_plan)
    
    return generation_plan
```

### Template Library Categories

#### 1. Python ML Project Template
```yaml
python_ml_template:
  name: "python-ml-project"
  version: "2.1.0"
  compatibility: ["Python 3.9+", "Poetry", "Docker", "Jupyter"]
  structure:
    root: "/"
    directories:
      - ".github/workflows/"     # CI/CD pipelines
      - "src/data/"             # Raw and processed datasets
      - "src/models/"           # Trained models and artifacts
      - "src/notebooks/"        # Jupyter notebooks
      - "src/scripts/"          # Processing scripts
      - "src/utils/"            # Helper functions
      - "src/tests/"            # Unit and integration tests
      - "docs/"                 # Project documentation
      - "config/"               # Configuration files
      - "logs/"                 # Application logs
      - "results/"              # Experiment outputs
      - "staging/"              # File classification inbox
    files:
      - ".gitignore"
      - "LICENSE"
      - "README.md"
      - "pyproject.toml"
      - "environment.yml"
      - "Dockerfile"
      - "docker-compose.yml"
      - "Makefile"
```

#### 2. Web Application Template
```yaml
web_app_template:
  name: "modern-web-app"
  version: "2.0.0"
  compatibility: ["Node.js 18+", "React/Vue/Angular", "TypeScript"]
  structure:
    root: "/"
    directories:
      - "src/components/"       # UI components
      - "src/pages/"            # Page components
      - "src/hooks/"            # Custom hooks
      - "src/utils/"            # Utility functions
      - "src/services/"         # API services
      - "src/types/"            # TypeScript definitions
      - "src/assets/"           # Static assets
      - "src/styles/"           # CSS/SCSS files
      - "src/tests/"            # Test files
      - "public/"               # Public assets
      - "docs/"                 # Documentation
      - "scripts/"              # Build scripts
      - "staging/"              # File classification inbox
    files:
      - "package.json"
      - "tsconfig.json"
      - "vite.config.ts"
      - ".eslintrc.js"
      - ".prettierrc"
      - "README.md"
      - "Dockerfile"
```

### Quality Validation

#### Structure Validation Checklist
```yaml
validation_criteria:
  completeness:
    - all_required_directories_created: true
    - configuration_files_generated: true
    - documentation_structure_initialized: true
    - staging_area_configured: true
  
  compliance:
    - naming_conventions_followed: true
    - organizational_standards_met: true
    - security_requirements_addressed: true
    - accessibility_permissions_set: true
  
  functionality:
    - build_system_configured: true
    - development_environment_ready: true
    - ci_cd_pipeline_initialized: true
    - testing_framework_setup: true
  
  scalability:
    - structure_supports_growth: true
    - modular_organization_implemented: true
    - clear_separation_of_concerns: true
    - maintainability_optimized: true
```

### Success Metrics

#### Performance Indicators
- ✅ **Template Accuracy**: 95%+ match between project needs and selected template
- ✅ **Generation Speed**: Complete structure creation in under 10 minutes
- ✅ **Validation Success**: 100% of generated structures pass validation checks
- ✅ **User Satisfaction**: 90%+ developer approval of generated structures

#### Quality Standards
- ✅ **Best Practice Compliance**: Adherence to industry standards and conventions
- ✅ **Scalability**: Structure supports project growth without reorganization
- ✅ **Maintainability**: Clear organization facilitates long-term maintenance
- ✅ **Team Adoption**: Easy onboarding for new team members

### Integration Points

#### Handoff to Classifico
```yaml
classifico_integration:
  staging_directory:
    location: "/staging"
    purpose: "File classification inbox"
    permissions: "read_write_all_team_members"
    monitoring: "real_time_file_system_events"
  
  project_context:
    structure_type: "template_name_and_version"
    directory_purposes: "mapping_of_directory_functions"
    classification_rules: "project_specific_file_placement_rules"
    naming_conventions: "established_naming_patterns"
```

#### Support for Other Agents
- **Locomoto Integration**: Ensure proper permissions for file movement operations
- **Purgo Coordination**: Create structure that supports automated hygiene monitoring
- **Documentation**: Provide comprehensive structure documentation for team reference

### Error Handling

#### Common Issues & Resolutions
```yaml
error_scenarios:
  insufficient_permissions:
    detection: "permission_denied_during_directory_creation"
    resolution: "request_elevated_privileges_or_alternative_location"
    fallback: "create_structure_in_user_accessible_directory"
  
  naming_conflicts:
    detection: "directory_or_file_already_exists"
    resolution: "append_timestamp_or_version_number"
    user_prompt: "request_alternative_name_or_merge_strategy"
  
  template_incompatibility:
    detection: "selected_template_missing_required_features"
    resolution: "hybrid_template_creation_or_custom_modification"
    escalation: "human_review_for_complex_requirements"
```

This task establishes the foundation for all subsequent file organization activities by creating well-designed, scalable directory structures that support efficient project development and maintenance.
