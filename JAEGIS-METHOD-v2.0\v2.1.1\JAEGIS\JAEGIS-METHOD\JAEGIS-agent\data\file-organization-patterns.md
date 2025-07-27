# File Organization Patterns Database
## Comprehensive Reference for Automated Directory Management

### Pattern Overview
This database contains proven file organization patterns, classification rules, and best practices for automated directory management across different project types and organizational contexts.

### Project Type Classification Patterns

#### 1. Python Machine Learning Projects
```yaml
python_ml_patterns:
  identification_indicators:
    file_extensions: [".py", ".ipynb", ".pkl", ".h5", ".csv", ".json"]
    import_patterns:
      - "import pandas"
      - "import numpy"
      - "import sklearn"
      - "import tensorflow"
      - "import torch"
      - "import matplotlib"
    directory_hints: ["data", "models", "notebooks", "experiments"]
    
  classification_rules:
    data_files:
      patterns: ["*.csv", "*.json", "*.parquet", "*.h5", "*.pkl", "*.npy"]
      content_indicators: ["dataset", "training", "test", "validation", "features", "labels"]
      size_thresholds:
        raw_data: "> 1MB -> src/data/raw/"
        processed_data: "> 10MB -> src/data/processed/"
        model_artifacts: "> 50MB -> src/models/"
      destination_logic: "size_and_content_based"
      
    notebook_files:
      patterns: ["*.ipynb"]
      content_analysis:
        exploratory: "contains 'explore', 'EDA', 'analysis' -> src/notebooks/exploratory/"
        modeling: "contains 'model', 'train', 'fit' -> src/notebooks/modeling/"
        visualization: "contains 'plot', 'chart', 'graph' -> src/notebooks/visualization/"
        preprocessing: "contains 'clean', 'preprocess', 'transform' -> src/notebooks/preprocessing/"
      cell_count_threshold: "> 5 cells indicates active notebook"
      
    script_files:
      patterns: ["*.py"]
      ast_analysis:
        main_scripts: "contains 'if __name__ == \"__main__\"' -> src/scripts/"
        utility_functions: "only function definitions -> src/utils/"
        model_classes: "contains 'class.*Model' -> src/models/"
        test_files: "contains 'def test_' or 'import unittest' -> src/tests/"
        configuration: "contains config/settings variables -> config/"
      import_analysis:
        data_processing: "imports pandas/numpy heavily -> src/data/"
        model_training: "imports sklearn/tensorflow -> src/models/"
        visualization: "imports matplotlib/seaborn -> src/visualization/"
```

#### 2. Web Application Projects
```yaml
web_app_patterns:
  identification_indicators:
    file_extensions: [".js", ".ts", ".jsx", ".tsx", ".css", ".scss", ".html", ".json"]
    framework_indicators:
      react: ["import React", "useState", "useEffect", "jsx", "tsx"]
      vue: ["<template>", "<script>", "<style>", "vue"]
      angular: ["@Component", "@Injectable", "@NgModule", "angular"]
      node: ["express", "require(", "module.exports", "package.json"]
    
  classification_rules:
    component_files:
      patterns: ["*.jsx", "*.tsx", "*.vue"]
      content_analysis:
        ui_components: "export default.*Component -> src/components/"
        page_components: "contains routing/navigation -> src/pages/"
        layout_components: "contains header/footer/sidebar -> src/layouts/"
        utility_components: "reusable utilities -> src/components/common/"
      naming_conventions:
        pascal_case: "ComponentName.tsx -> src/components/"
        kebab_case: "component-name.tsx -> src/components/"
        
    style_files:
      patterns: ["*.css", "*.scss", "*.less", "*.styled.js"]
      organization:
        global_styles: "global/reset/normalize -> src/styles/global/"
        component_styles: "component-specific -> src/styles/components/"
        utility_styles: "utilities/mixins -> src/styles/utils/"
        theme_styles: "colors/typography/spacing -> src/styles/theme/"
        
    service_files:
      patterns: ["*.service.js", "*.api.js", "*Service.ts"]
      content_indicators:
        api_services: "fetch/axios/http -> src/services/api/"
        data_services: "data manipulation -> src/services/data/"
        utility_services: "helper functions -> src/services/utils/"
        auth_services: "authentication/authorization -> src/services/auth/"
```

#### 3. Research and Documentation Projects
```yaml
research_patterns:
  identification_indicators:
    file_extensions: [".tex", ".bib", ".md", ".rst", ".pdf", ".docx"]
    content_indicators: ["\\documentclass", "\\begin{document}", "bibliography", "references"]
    directory_hints: ["manuscript", "literature", "data", "analysis", "figures"]
    
  classification_rules:
    manuscript_files:
      patterns: ["*.tex", "*.md", "*.docx"]
      content_analysis:
        main_document: "\\documentclass or # Title -> manuscript/"
        sections: "\\section or ## -> manuscript/sections/"
        appendices: "\\appendix or # Appendix -> manuscript/appendices/"
        supplementary: "supplement/additional -> manuscript/supplementary/"
        
    reference_files:
      patterns: ["*.bib", "*.ris", "*.endnote"]
      organization: "all references -> literature/references/"
      
    data_files:
      patterns: ["*.csv", "*.xlsx", "*.json", "*.xml", "*.sql"]
      content_analysis:
        raw_data: "original/unprocessed -> data/raw/"
        processed_data: "cleaned/analyzed -> data/processed/"
        external_data: "third-party sources -> data/external/"
        
    analysis_files:
      patterns: ["*.R", "*.py", "*.ipynb", "*.sas", "*.spss"]
      content_analysis:
        exploratory: "exploration/EDA -> analysis/exploratory/"
        statistical: "statistical tests -> analysis/statistical/"
        visualization: "plots/charts -> analysis/visualization/"
        modeling: "models/predictions -> analysis/modeling/"
```

### Content-Based Classification Patterns

#### Natural Language Processing Indicators
```yaml
nlp_classification:
  document_types:
    requirements:
      keywords: ["requirement", "specification", "must", "shall", "should", "user story"]
      patterns: ["As a", "Given", "When", "Then", "Acceptance criteria"]
      destination: "docs/requirements/"
      
    technical_documentation:
      keywords: ["API", "documentation", "guide", "manual", "tutorial", "how-to"]
      patterns: ["## Installation", "## Usage", "## Examples", "### Parameters"]
      destination: "docs/technical/"
      
    meeting_notes:
      keywords: ["meeting", "notes", "agenda", "action items", "decisions"]
      patterns: ["Date:", "Attendees:", "Action items:", "Next steps:"]
      destination: "docs/meetings/"
      
    reports:
      keywords: ["report", "analysis", "findings", "conclusion", "summary"]
      patterns: ["Executive Summary", "Introduction", "Methodology", "Results"]
      destination: "docs/reports/"
```

#### Code Analysis Patterns
```yaml
code_classification:
  programming_languages:
    python:
      file_extensions: [".py"]
      ast_patterns:
        models: "class.*Model|class.*Classifier|class.*Regressor"
        utilities: "def.*util|def.*helper|def.*common"
        tests: "def test_|import unittest|import pytest"
        scripts: "if __name__ == '__main__'"
        configs: "CONFIG|SETTINGS|.*_config"
        
    javascript:
      file_extensions: [".js", ".ts", ".jsx", ".tsx"]
      patterns:
        components: "export default.*|React.Component|function.*Component"
        services: "service|api|fetch|axios"
        utilities: "util|helper|common"
        tests: "test|spec|describe|it("
        configs: "config|settings|environment"
        
    java:
      file_extensions: [".java"]
      patterns:
        models: "class.*Model|@Entity|@Table"
        controllers: "@Controller|@RestController|@RequestMapping"
        services: "@Service|@Component"
        tests: "@Test|extends TestCase"
        configs: "@Configuration|@Bean"
```

### File Naming Convention Patterns

#### Standard Naming Patterns
```yaml
naming_conventions:
  file_naming:
    camelCase:
      pattern: "fileName.extension"
      usage: "JavaScript, Java, C#"
      examples: ["userService.js", "dataModel.ts", "testHelper.java"]
      
    snake_case:
      pattern: "file_name.extension"
      usage: "Python, Ruby, C"
      examples: ["user_service.py", "data_model.rb", "test_helper.c"]
      
    kebab-case:
      pattern: "file-name.extension"
      usage: "CSS, HTML, Vue components"
      examples: ["user-service.css", "data-model.vue", "test-helper.html"]
      
    PascalCase:
      pattern: "FileName.extension"
      usage: "React components, C# classes"
      examples: ["UserService.tsx", "DataModel.cs", "TestHelper.jsx"]
      
  directory_naming:
    lowercase_with_underscores:
      pattern: "directory_name"
      usage: "Python projects, Unix systems"
      examples: ["user_management", "data_processing", "test_utilities"]
      
    lowercase_with_hyphens:
      pattern: "directory-name"
      usage: "Web projects, npm packages"
      examples: ["user-management", "data-processing", "test-utilities"]
      
    camelCase_directories:
      pattern: "directoryName"
      usage: "Java projects, some JavaScript projects"
      examples: ["userManagement", "dataProcessing", "testUtilities"]
```

### Size-Based Classification Patterns

#### File Size Thresholds
```yaml
size_based_classification:
  small_files:
    threshold: "< 1MB"
    typical_types: ["configuration", "documentation", "scripts", "source_code"]
    storage_strategy: "standard_storage"
    backup_frequency: "daily"
    
  medium_files:
    threshold: "1MB - 100MB"
    typical_types: ["datasets", "images", "compiled_binaries", "documentation_with_media"]
    storage_strategy: "standard_storage_with_compression"
    backup_frequency: "daily"
    
  large_files:
    threshold: "100MB - 1GB"
    typical_types: ["large_datasets", "video_files", "database_dumps", "model_files"]
    storage_strategy: "compressed_storage_or_external"
    backup_frequency: "weekly"
    special_handling: "consider_git_lfs_or_external_storage"
    
  very_large_files:
    threshold: "> 1GB"
    typical_types: ["massive_datasets", "video_content", "virtual_machine_images"]
    storage_strategy: "external_storage_mandatory"
    backup_frequency: "monthly"
    special_handling: "external_storage_with_reference_links"
```

### Temporal Classification Patterns

#### Time-Based Organization
```yaml
temporal_patterns:
  daily_organization:
    log_files:
      pattern: "YYYY-MM-DD format"
      retention: "30 days"
      archival: "compress after 7 days"
      destination: "logs/daily/"
      
    backup_files:
      pattern: "backup_YYYY-MM-DD_HHMMSS"
      retention: "90 days"
      archival: "compress after 30 days"
      destination: "backups/daily/"
      
  version_based:
    release_files:
      pattern: "v1.0.0, v1.0.1, etc."
      retention: "keep all major versions"
      archival: "compress old minor versions"
      destination: "releases/vX.Y.Z/"
      
    document_versions:
      pattern: "document_v1, document_v2"
      retention: "keep last 5 versions"
      archival: "archive older versions"
      destination: "docs/versions/"
```

### Integration Patterns

#### Squad Coordination Patterns
```yaml
squad_integration:
  structuro_patterns:
    template_selection:
      indicators: ["project_type", "technology_stack", "team_size", "complexity"]
      decision_matrix: "weighted_scoring_based_on_indicators"
      customization: "dynamic_template_modification"
      
  classifico_patterns:
    content_analysis:
      text_files: "NLP_based_topic_classification"
      code_files: "AST_parsing_and_pattern_matching"
      binary_files: "metadata_extraction_and_type_detection"
      
  locomoto_patterns:
    operation_safety:
      pre_checks: "existence_permissions_space_conflicts"
      execution: "atomic_operations_with_rollback"
      post_validation: "integrity_verification_and_logging"
      
  purgo_patterns:
    hygiene_monitoring:
      continuous: "real_time_anomaly_detection"
      scheduled: "periodic_comprehensive_analysis"
      reporting: "actionable_insights_and_recommendations"
```

### Success Metrics and Validation

#### Pattern Effectiveness Metrics
```yaml
pattern_validation:
  accuracy_metrics:
    classification_accuracy: "> 95% for standard file types"
    false_positive_rate: "< 2% for automated operations"
    user_correction_rate: "< 5% of all classifications"
    
  efficiency_metrics:
    processing_speed: "< 30 seconds average per file"
    resource_utilization: "< 15% CPU during normal operations"
    storage_optimization: "> 20% space savings through organization"
    
  user_satisfaction:
    adoption_rate: "> 85% of eligible projects"
    satisfaction_score: "> 4.0/5.0 user rating"
    training_time: "< 2 hours for new users"
```

This comprehensive pattern database serves as the knowledge foundation for intelligent file organization, enabling the squad to make informed decisions about file placement, structure optimization, and maintenance strategies.
