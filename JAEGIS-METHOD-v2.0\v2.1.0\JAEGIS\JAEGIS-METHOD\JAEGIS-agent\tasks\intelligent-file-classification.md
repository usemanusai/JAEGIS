# Intelligent File Classification
## Advanced Content Analysis & Automated File Categorization

### Task Overview
Perform comprehensive analysis of files to determine their optimal placement within project directory structures using advanced NLP, code parsing, and metadata extraction techniques. This task transforms manual file organization into an intelligent, automated classification system.

### Core Objectives
1. **Analyze file content** using multi-modal understanding techniques
2. **Extract meaningful metadata** from various file types and formats
3. **Determine optimal placement** based on content, context, and project structure
4. **Maintain high accuracy** through continuous learning and feedback integration
5. **Provide transparent reasoning** for all classification decisions

### Input Requirements

#### File Analysis Context
```yaml
classification_input:
  file_information:
    - file_path: "absolute_path_to_file"
    - file_size: "size_in_bytes"
    - file_extension: "file_extension"
    - mime_type: "detected_mime_type"
    - creation_date: "iso_8601_timestamp"
    - modification_date: "iso_8601_timestamp"
  
  project_context:
    - project_type: "web_app | ml_project | research | documentation"
    - directory_structure: "current_project_structure_mapping"
    - naming_conventions: "established_naming_patterns"
    - classification_rules: "project_specific_placement_rules"
  
  content_analysis:
    - raw_content: "file_content_as_string"
    - extracted_text: "text_extracted_from_binary_files"
    - metadata: "embedded_file_metadata"
    - relationships: "connections_to_other_files"
```

### Execution Workflow

#### Phase 1: Content Extraction & Preprocessing (30-60 seconds)
```python
def extract_and_preprocess_content(file_path):
    """
    Extract content from various file types and prepare for analysis
    """
    file_info = get_file_metadata(file_path)
    
    content_extraction = {
        'text_files': extract_text_content(file_path),
        'code_files': parse_code_with_tree_sitter(file_path),
        'document_files': extract_document_content(file_path),
        'binary_files': extract_metadata_only(file_path),
        'media_files': extract_media_metadata(file_path)
    }
    
    preprocessing_results = {
        'cleaned_content': clean_and_normalize_text(content_extraction),
        'structural_elements': identify_structural_elements(content_extraction),
        'key_indicators': extract_classification_indicators(content_extraction),
        'relationships': find_related_files(file_path, content_extraction)
    }
    
    return preprocessing_results
```

#### Phase 2: Multi-Modal Analysis (1-2 minutes)
```python
def perform_multimodal_analysis(preprocessing_results, project_context):
    """
    Comprehensive analysis using multiple AI techniques
    """
    analysis_results = {}
    
    # Natural Language Processing Analysis
    if preprocessing_results['cleaned_content']:
        analysis_results['nlp_analysis'] = {
            'topic_classification': classify_document_topics(preprocessing_results['cleaned_content']),
            'intent_detection': detect_document_intent(preprocessing_results['cleaned_content']),
            'keyword_extraction': extract_key_terms(preprocessing_results['cleaned_content']),
            'semantic_similarity': compare_with_existing_files(preprocessing_results['cleaned_content'])
        }
    
    # Code Analysis (if applicable)
    if preprocessing_results['structural_elements'].get('code_elements'):
        analysis_results['code_analysis'] = {
            'language_detection': identify_programming_language(preprocessing_results),
            'framework_identification': detect_frameworks_and_libraries(preprocessing_results),
            'code_type_classification': classify_code_purpose(preprocessing_results),
            'complexity_metrics': calculate_code_complexity(preprocessing_results),
            'dependency_analysis': analyze_imports_and_dependencies(preprocessing_results)
        }
    
    # Contextual Analysis
    analysis_results['contextual_analysis'] = {
        'project_relevance': assess_project_relevance(preprocessing_results, project_context),
        'directory_fit': evaluate_directory_compatibility(preprocessing_results, project_context),
        'naming_pattern_match': check_naming_convention_compliance(preprocessing_results, project_context),
        'usage_prediction': predict_file_usage_patterns(preprocessing_results, project_context)
    }
    
    return analysis_results
```

#### Phase 3: Classification Decision Making (30-60 seconds)
```python
def make_classification_decision(analysis_results, project_context):
    """
    Intelligent decision making for optimal file placement
    """
    # Calculate destination scores for each possible directory
    destination_scores = {}
    
    for directory in project_context['directory_structure']:
        score = calculate_directory_compatibility_score(
            directory, analysis_results, project_context
        )
        destination_scores[directory] = score
    
    # Select optimal destination
    optimal_destination = select_highest_scoring_destination(destination_scores)
    
    # Generate confidence score and reasoning
    classification_result = {
        'destination_path': optimal_destination,
        'confidence_score': calculate_confidence_score(destination_scores),
        'reasoning': generate_classification_reasoning(analysis_results, optimal_destination),
        'alternative_options': get_alternative_destinations(destination_scores),
        'metadata': {
            'analysis_timestamp': get_current_timestamp(),
            'classification_version': get_classifier_version(),
            'project_context_hash': hash_project_context(project_context)
        }
    }
    
    return classification_result
```

### Classification Rules Engine

#### Content-Based Classification Rules
```yaml
classification_rules:
  python_ml_project:
    data_files:
      file_patterns: ["*.csv", "*.json", "*.parquet", "*.h5", "*.pkl"]
      content_indicators:
        - "dataset"
        - "training_data"
        - "features"
        - "labels"
        - "samples"
      size_thresholds:
        small: "< 10MB -> src/data/raw/"
        large: "> 100MB -> src/data/processed/"
      destination: "src/data/"
    
    model_files:
      file_patterns: ["*.pkl", "*.joblib", "*.h5", "*.onnx", "*.pt"]
      content_indicators:
        - "model"
        - "classifier"
        - "regressor"
        - "neural_network"
      metadata_checks:
        - "model_architecture"
        - "training_parameters"
      destination: "src/models/"
    
    notebook_files:
      file_patterns: ["*.ipynb"]
      content_analysis:
        - "exploration" -> "src/notebooks/exploratory/"
        - "analysis" -> "src/notebooks/analysis/"
        - "visualization" -> "src/notebooks/visualization/"
        - "modeling" -> "src/notebooks/modeling/"
      cell_count_threshold: "> 10 cells"
      destination: "src/notebooks/"
    
    script_files:
      file_patterns: ["*.py"]
      ast_analysis:
        - "if __name__ == '__main__'" -> "src/scripts/"
        - "class.*Model" -> "src/models/"
        - "def test_" -> "src/tests/"
        - "import unittest" -> "src/tests/"
      function_analysis:
        - "main()" -> "src/scripts/"
        - "train_model()" -> "src/scripts/"
        - "preprocess_data()" -> "src/utils/"
      destination: "determined_by_analysis"
```

#### Advanced Pattern Recognition
```python
def advanced_pattern_recognition(file_content, file_path):
    """
    Sophisticated pattern recognition for complex classification scenarios
    """
    patterns = {
        'configuration_files': {
            'indicators': ['config', 'settings', 'environment', 'env'],
            'formats': ['.json', '.yaml', '.yml', '.toml', '.ini'],
            'content_patterns': ['database_url', 'api_key', 'secret', 'port']
        },
        'documentation_files': {
            'indicators': ['readme', 'doc', 'guide', 'manual', 'help'],
            'formats': ['.md', '.rst', '.txt', '.pdf'],
            'content_patterns': ['# ', '## ', 'installation', 'usage', 'example']
        },
        'test_files': {
            'indicators': ['test', 'spec', 'mock'],
            'formats': ['.py', '.js', '.ts', '.java'],
            'content_patterns': ['assert', 'expect', 'should', 'describe', 'it(']
        },
        'utility_files': {
            'indicators': ['util', 'helper', 'common', 'shared'],
            'content_patterns': ['def ', 'function ', 'class ', 'export']
        }
    }
    
    recognition_results = {}
    for pattern_type, pattern_config in patterns.items():
        score = calculate_pattern_match_score(file_content, file_path, pattern_config)
        recognition_results[pattern_type] = score
    
    return recognition_results
```

### Machine Learning Integration

#### Continuous Learning System
```python
def update_classification_model(feedback_data):
    """
    Continuous improvement through user feedback and correction data
    """
    learning_pipeline = {
        'feedback_processing': {
            'user_corrections': process_manual_file_moves(feedback_data),
            'success_metrics': analyze_file_access_patterns(feedback_data),
            'error_analysis': identify_misclassification_patterns(feedback_data)
        },
        'model_training': {
            'feature_extraction': extract_features_from_feedback(feedback_data),
            'model_update': retrain_classification_models(feedback_data),
            'validation': cross_validate_updated_models(feedback_data)
        },
        'deployment': {
            'model_versioning': create_new_model_version(),
            'a_b_testing': deploy_with_gradual_rollout(),
            'performance_monitoring': track_classification_accuracy()
        }
    }
    
    execute_learning_pipeline(learning_pipeline)
    return learning_pipeline
```

### Quality Assurance

#### Classification Validation
```yaml
validation_framework:
  confidence_thresholds:
    high_confidence: "> 0.9"
    medium_confidence: "0.7 - 0.9"
    low_confidence: "< 0.7"
  
  validation_actions:
    high_confidence:
      action: "automatic_classification"
      review: "post_classification_audit"
    medium_confidence:
      action: "automatic_with_notification"
      review: "periodic_review"
    low_confidence:
      action: "flag_for_human_review"
      review: "mandatory_human_approval"
  
  accuracy_monitoring:
    metrics:
      - "classification_accuracy_rate"
      - "user_correction_frequency"
      - "processing_time_per_file"
      - "confidence_score_distribution"
    reporting_frequency: "weekly"
    improvement_targets: "monthly_accuracy_increase"
```

### Success Metrics

#### Performance Indicators
- ✅ **Classification Accuracy**: 95%+ correct placement for standard file types
- ✅ **Processing Speed**: Average 30 seconds per file for complete analysis
- ✅ **Confidence Reliability**: 90%+ accuracy for high-confidence classifications
- ✅ **User Satisfaction**: Less than 5% manual corrections required

#### Quality Standards
- ✅ **Consistency**: Same file types consistently classified to same locations
- ✅ **Transparency**: Clear reasoning provided for all classification decisions
- ✅ **Adaptability**: Continuous improvement through feedback integration
- ✅ **Scalability**: Handle increasing file volumes without performance degradation

### Integration Points

#### Handoff to Locomoto
```yaml
move_order_generation:
  required_fields:
    - source_path: "current_file_location"
    - destination_path: "classified_optimal_location"
    - classification_confidence: "confidence_score_0_to_1"
    - reasoning: "human_readable_classification_explanation"
  
  optional_fields:
    - backup_required: "boolean_flag_for_important_files"
    - conflict_resolution: "strategy_for_naming_conflicts"
    - priority_level: "urgency_of_file_movement"
    - batch_operation_id: "identifier_for_batch_processing"
```

This task ensures intelligent, accurate file classification that forms the core of the automated file organization system, providing the intelligence needed to maintain organized, logical project structures.
