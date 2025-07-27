# Automated Agent Generation Template

## Overview
This template provides the standardized structure and automation framework for generating new AI agents within the JAEGIS Method system. It ensures consistency, quality, and seamless integration while incorporating real-time market research and intelligence.

## Agent Generation Configuration Template

### User Configuration Interface
```yaml
agent_generation_config:
  session_id: "{{session_timestamp}}"
  user_preferences:
    quantity: "{{agent_quantity}}"  # number, "optimal", or "custom"
    organization: "{{organization_strategy}}"  # "squads", "individual", "hybrid"
    focus_areas: [{{focus_area_list}}]  # Array of focus areas
    research_depth: "{{research_depth}}"  # "surface", "comprehensive", "exhaustive"
    target_market: "{{target_market}}"  # "enterprise", "startup", "general", "niche"
  
  research_parameters:
    max_queries: {{max_research_queries}}
    source_priority: {{research_source_priority}}
    date_context: "{{current_date_context}}"
    trend_analysis_depth: {{trend_analysis_depth}}
    competitive_intelligence: {{competitive_intelligence_enabled}}
  
  quality_standards:
    minimum_content_words: 1500
    market_relevance_threshold: 0.8
    technical_feasibility_threshold: 0.9
    integration_compatibility_threshold: 0.9
    documentation_quality_threshold: 0.85
```

### Research Query Templates

#### Trend Analysis Queries
```yaml
trend_analysis_queries:
  emerging_technology:
    - "{{current_year}} emerging AI automation trends"
    - "latest {{current_year}} machine learning applications"
    - "{{current_year}} breakthrough automation technologies"
    - "emerging {{current_year}} business process automation"
    - "{{current_year}} AI/ML industry disruptions"
  
  business_automation:
    - "{{current_year}} business process automation opportunities"
    - "enterprise automation trends {{current_year}}"
    - "workflow optimization solutions {{current_year}}"
    - "business intelligence automation {{current_year}}"
    - "operational efficiency AI tools {{current_year}}"
  
  industry_specific:
    - "{{industry}} automation challenges {{current_year}}"
    - "{{industry}} AI implementation trends {{current_year}}"
    - "{{industry}} digital transformation {{current_year}}"
    - "{{industry}} process optimization needs {{current_year}}"
    - "{{industry}} technology adoption patterns {{current_year}}"
```

#### Gap Analysis Queries
```yaml
gap_analysis_queries:
  capability_gaps:
    - "unmet automation needs {{current_year}}"
    - "AI capability gaps in enterprise {{current_year}}"
    - "missing automation tools {{current_year}}"
    - "underserved automation markets {{current_year}}"
    - "automation pain points {{current_year}}"
  
  technology_gaps:
    - "missing AI/ML tools {{current_year}}"
    - "automation technology limitations {{current_year}}"
    - "unaddressed technical challenges {{current_year}}"
    - "integration gaps in automation {{current_year}}"
    - "scalability issues automation {{current_year}}"
```

## Agent Specification Template

### Core Agent Structure
```yaml
agent_specification:
  metadata:
    name: "{{agent_name}}"  # lowercase-with-hyphens
    title: "{{agent_title}}"  # Human-readable title
    description: "{{agent_description}}"  # Comprehensive description
    tier: {{agent_tier}}  # 1-4 based on classification
    priority: {{agent_priority}}  # Numeric priority
    classification: "{{tier_classification}}"  # PRIMARY, SECONDARY, SPECIALIZED
    
  research_basis:
    market_need: "{{identified_market_need}}"
    research_sources: [{{research_source_list}}]
    competitive_analysis: "{{competitive_positioning}}"
    technology_assessment: "{{technology_feasibility}}"
    trend_alignment: "{{trend_alignment_score}}"
    
  capabilities:
    core_functions: [{{core_function_list}}]
    specialized_skills: [{{specialized_skill_list}}]
    integration_points: [{{integration_point_list}}]
    technology_stack: [{{technology_stack_list}}]
    
  coordination:
    type: "{{coordination_type}}"  # collaborative, specialized, service, master
    handoff_from: [{{handoff_from_agents}}]
    handoff_to: [{{handoff_to_agents}}]
    validation_requirements: [{{validation_requirement_list}}]
    
  full_team_participation:
    contribution_types: [{{contribution_type_list}}]
    integration_points: [{{integration_point_list}}]
    meaningful_contribution_criteria: "{{contribution_criteria}}"
    quality_standards: "{{quality_standards}}"
```

### Task Definition Template
```yaml
task_definition:
  name: "{{task_name}}"
  display_name: "{{task_display_name}}"
  description: "{{task_description}}"
  
  objective: "{{task_objective}}"
  
  process_steps:
    - step_number: 1
      name: "{{step_1_name}}"
      purpose: "{{step_1_purpose}}"
      actions: [{{step_1_actions}}]
      output: "{{step_1_output}}"
    
    - step_number: 2
      name: "{{step_2_name}}"
      purpose: "{{step_2_purpose}}"
      actions: [{{step_2_actions}}]
      output: "{{step_2_output}}"
  
  quality_assurance:
    validation_criteria: [{{validation_criteria_list}}]
    success_metrics: [{{success_metrics_list}}]
    error_handling: "{{error_handling_approach}}"
  
  integration_points:
    input_sources: [{{input_source_list}}]
    output_consumers: [{{output_consumer_list}}]
    dependencies: [{{dependency_list}}]
```

### Template File Structure
```yaml
template_file:
  name: "{{template_name}}"
  display_name: "{{template_display_name}}"
  description: "{{template_description}}"
  
  template_type: "{{template_type}}"  # specification, framework, configuration, etc.
  
  template_content:
    overview: "{{template_overview}}"
    structure: "{{template_structure}}"
    usage_examples: [{{usage_example_list}}]
    customization_points: [{{customization_point_list}}]
    
  variables:
    - name: "{{variable_name}}"
      type: "{{variable_type}}"
      description: "{{variable_description}}"
      default_value: "{{variable_default}}"
      required: {{variable_required}}
  
  validation_rules:
    syntax_validation: "{{syntax_validation_rules}}"
    content_validation: "{{content_validation_rules}}"
    integration_validation: "{{integration_validation_rules}}"
```

### Checklist Template Structure
```yaml
checklist_template:
  name: "{{checklist_name}}"
  display_name: "{{checklist_display_name}}"
  description: "{{checklist_description}}"
  
  checklist_type: "{{checklist_type}}"  # quality_assurance, validation, integration, etc.
  
  sections:
    - section_name: "{{section_1_name}}"
      description: "{{section_1_description}}"
      items:
        - item: "{{checklist_item_1}}"
          required: {{item_required}}
          validation_method: "{{validation_method}}"
        - item: "{{checklist_item_2}}"
          required: {{item_required}}
          validation_method: "{{validation_method}}"
  
  success_criteria:
    minimum_completion_rate: {{minimum_completion_rate}}
    critical_items: [{{critical_item_list}}]
    quality_threshold: {{quality_threshold}}
```

### Data File Template Structure
```yaml
data_file_template:
  name: "{{data_file_name}}"
  display_name: "{{data_file_display_name}}"
  description: "{{data_file_description}}"
  
  data_type: "{{data_type}}"  # reference, configuration, mapping, schema, etc.
  
  data_structure:
    format: "{{data_format}}"  # json, yaml, markdown, etc.
    schema_version: "{{schema_version}}"
    last_updated: "{{last_updated_timestamp}}"
    
  content_sections:
    - section_name: "{{section_1_name}}"
      description: "{{section_1_description}}"
      data_schema: "{{section_1_schema}}"
      
  validation_rules:
    data_integrity: "{{data_integrity_rules}}"
    format_validation: "{{format_validation_rules}}"
    content_validation: "{{content_validation_rules}}"
```

## Agent Configuration Entry Template

### JAEGIS Agent Config Format
```
==================== START: {{agent_name}} ====================
Title: {{agent_title}}
Name: {{agent_display_name}}
Description: {{agent_description}}
Persona: personas#{{agent_name}}
Tasks:
{{#each tasks}}
  - [{{display_name}}](tasks#{{file_name}})
{{/each}}
{{#if templates}}
Templates:
{{#each templates}}
  - [{{display_name}}](templates#{{file_name}})
{{/each}}
{{/if}}
{{#if checklists}}
Checklists:
{{#each checklists}}
  - [{{display_name}}](checklists#{{file_name}})
{{/each}}
{{/if}}
{{#if data_files}}
Data:
{{#each data_files}}
  - [{{display_name}}](data#{{file_name}})
{{/each}}
{{/if}}
Coordination: {{coordination_type}}
{{#if handoff_from}}
Handoff-From: [{{handoff_from}}]
{{/if}}
{{#if handoff_to}}
Handoff-To: [{{handoff_to}}]
{{/if}}
{{#if validation_requirements}}
Validation: {{validation_requirements}}
{{/if}}
Priority: {{priority}}
Classification: {{classification}}
{{#if activation_criteria}}
Activation-Criteria: [{{activation_criteria}}]
{{/if}}
Full-Team-Participation:
  contribution-types: [{{contribution_types}}]
  integration-points: [{{integration_points}}]
  meaningful-contribution-criteria: "{{contribution_criteria}}"
  quality-standards: "{{quality_standards}}"
==================== END: {{agent_name}} ====================
```

## Automation Script Templates

### Integration Automation Script
```bash
#!/bin/bash
# Automated JAEGIS Integration Script Template

set -euo pipefail

# Configuration
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly JAEGIS_ROOT="{{jaegis_root_path}}"
readonly BACKUP_DIR="{{backup_directory}}"
readonly LOG_FILE="{{log_file_path}}"

# Agent configuration
readonly AGENT_NAME="{{agent_name}}"
readonly AGENT_TIER={{agent_tier}}
readonly AGENT_FILES=({{agent_file_list}})

# Logging functions
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE" >&2
}

# Pre-integration validation
validate_system_readiness() {
    log_info "Validating system readiness for agent integration"
    
    # Check JAEGIS directory structure
    if [[ ! -d "$JAEGIS_ROOT" ]]; then
        log_error "JAEGIS root directory not found: $JAEGIS_ROOT"
        return 1
    fi
    
    # Check required directories
    local required_dirs=("personas" "tasks" "templates" "checklists" "data")
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$JAEGIS_ROOT/$dir" ]]; then
            log_error "Required directory not found: $JAEGIS_ROOT/$dir"
            return 1
        fi
        
        if [[ ! -w "$JAEGIS_ROOT/$dir" ]]; then
            log_error "Directory not writable: $JAEGIS_ROOT/$dir"
            return 1
        fi
    done
    
    log_info "System readiness validation completed successfully"
    return 0
}

# Agent name uniqueness validation
validate_agent_uniqueness() {
    log_info "Validating agent name uniqueness: $AGENT_NAME"
    
    if grep -q "START: $AGENT_NAME" "$JAEGIS_ROOT/agent-config.txt"; then
        log_error "Agent name already exists: $AGENT_NAME"
        return 1
    fi
    
    log_info "Agent name uniqueness validated: $AGENT_NAME"
    return 0
}

# Create system backup
create_system_backup() {
    local backup_timestamp=$(date '+%Y-%m-%d-%H%M%S')
    local backup_path="$BACKUP_DIR/$backup_timestamp"
    
    log_info "Creating system backup: $backup_path"
    
    mkdir -p "$backup_path"
    cp -r "$JAEGIS_ROOT" "$backup_path/"
    
    # Create backup manifest
    cat > "$backup_path/backup-manifest.json" << EOF
{
  "backup_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "backup_id": "$backup_timestamp",
  "agent_name": "$AGENT_NAME",
  "backup_path": "$backup_path",
  "integrity_verified": true
}
EOF
    
    log_info "System backup created successfully: $backup_path"
    echo "$backup_timestamp"
}

# Deploy agent files
deploy_agent_files() {
    log_info "Deploying agent files for: $AGENT_NAME"
    
    for file_spec in "${AGENT_FILES[@]}"; do
        local file_type=$(echo "$file_spec" | cut -d':' -f1)
        local file_name=$(echo "$file_spec" | cut -d':' -f2)
        local source_path="{{generated_files_path}}/$file_name"
        local target_path="$JAEGIS_ROOT/$file_type/$file_name"
        
        if [[ ! -f "$source_path" ]]; then
            log_error "Source file not found: $source_path"
            return 1
        fi
        
        cp "$source_path" "$target_path"
        log_info "Deployed: $target_path"
    done
    
    log_info "Agent file deployment completed successfully"
    return 0
}

# Update agent configuration
update_agent_config() {
    log_info "Updating agent configuration file"
    
    local config_file="$JAEGIS_ROOT/agent-config.txt"
    local temp_file=$(mktemp)
    local agent_entry="{{generated_agent_config_entry}}"
    
    # Find insertion point based on tier and alphabetical order
    local insertion_line=$(find_insertion_point "$config_file" "$AGENT_TIER" "$AGENT_NAME")
    
    # Insert agent configuration
    head -n "$insertion_line" "$config_file" > "$temp_file"
    echo "$agent_entry" >> "$temp_file"
    tail -n +"$((insertion_line + 1))" "$config_file" >> "$temp_file"
    
    # Replace original file
    mv "$temp_file" "$config_file"
    
    log_info "Agent configuration updated successfully"
    return 0
}

# Integration verification
verify_integration() {
    log_info "Verifying integration for agent: $AGENT_NAME"
    
    # Test configuration file parsing
    if ! validate_config_syntax "$JAEGIS_ROOT/agent-config.txt"; then
        log_error "Configuration file syntax validation failed"
        return 1
    fi
    
    # Verify all files exist and are readable
    for file_spec in "${AGENT_FILES[@]}"; do
        local file_type=$(echo "$file_spec" | cut -d':' -f1)
        local file_name=$(echo "$file_spec" | cut -d':' -f2)
        local file_path="$JAEGIS_ROOT/$file_type/$file_name"
        
        if [[ ! -r "$file_path" ]]; then
            log_error "File not readable: $file_path"
            return 1
        fi
    done
    
    log_info "Integration verification completed successfully"
    return 0
}

# Main integration workflow
main() {
    log_info "Starting automated JAEGIS integration for agent: $AGENT_NAME"
    
    # Pre-integration validation
    validate_system_readiness || exit 1
    validate_agent_uniqueness || exit 1
    
    # Create backup
    local backup_id=$(create_system_backup)
    
    # Deploy agent
    deploy_agent_files || {
        log_error "Agent deployment failed - initiating rollback"
        rollback_integration "$backup_id"
        exit 1
    }
    
    # Update configuration
    update_agent_config || {
        log_error "Configuration update failed - initiating rollback"
        rollback_integration "$backup_id"
        exit 1
    }
    
    # Verify integration
    verify_integration || {
        log_error "Integration verification failed - initiating rollback"
        rollback_integration "$backup_id"
        exit 1
    }
    
    log_info "Automated JAEGIS integration completed successfully for agent: $AGENT_NAME"
    log_info "Backup available at: $BACKUP_DIR/$backup_id"
}

# Execute main function
main "$@"
```

## Quality Validation Templates

### Agent Quality Validation Script
```python
#!/usr/bin/env python3
"""
Agent Quality Validation Template
Validates generated agents against JAEGIS quality standards
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

class AgentQualityValidator:
    def __init__(self, quality_standards: Dict[str, float]):
        self.quality_standards = quality_standards
        self.validation_results = {}
    
    def validate_agent(self, agent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive agent quality validation
        """
        results = {
            'agent_name': agent_spec.get('name', 'unknown'),
            'validation_timestamp': '{{validation_timestamp}}',
            'validations': {}
        }
        
        # Market relevance validation
        results['validations']['market_relevance'] = self.validate_market_relevance(agent_spec)
        
        # Technical feasibility validation
        results['validations']['technical_feasibility'] = self.validate_technical_feasibility(agent_spec)
        
        # Content completeness validation
        results['validations']['content_completeness'] = self.validate_content_completeness(agent_spec)
        
        # Integration compatibility validation
        results['validations']['integration_compatibility'] = self.validate_integration_compatibility(agent_spec)
        
        # Documentation quality validation
        results['validations']['documentation_quality'] = self.validate_documentation_quality(agent_spec)
        
        # Calculate overall score
        results['overall_score'] = self.calculate_overall_score(results['validations'])
        results['meets_standards'] = results['overall_score'] >= 0.85
        
        return results
    
    def validate_market_relevance(self, agent_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate market relevance based on research findings
        """
        validation = {
            'score': 0.0,
            'checks': {},
            'recommendations': []
        }
        
        # Check for research basis
        if 'research_basis' in agent_spec:
            validation['checks']['has_research_basis'] = True
            validation['score'] += 0.2
        else:
            validation['checks']['has_research_basis'] = False
            validation['recommendations'].append('Add research basis documentation')
        
        # Check for market need identification
        if agent_spec.get('research_basis', {}).get('market_need'):
            validation['checks']['addresses_market_need'] = True
            validation['score'] += 0.2
        else:
            validation['checks']['addresses_market_need'] = False
            validation['recommendations'].append('Clearly identify market need')
        
        # Additional market relevance checks...
        
        return validation
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """
        Generate comprehensive validation report
        """
        report = f"""
# Agent Quality Validation Report

**Agent Name**: {validation_results['agent_name']}
**Validation Date**: {validation_results['validation_timestamp']}
**Overall Score**: {validation_results['overall_score']:.2f}
**Meets Standards**: {'✅ Yes' if validation_results['meets_standards'] else '❌ No'}

## Validation Results

{{#each validation_results.validations}}
### {{@key}}
- **Score**: {{score}}
- **Status**: {{#if (gte score ../quality_standards.@key)}}✅ Pass{{else}}❌ Fail{{/if}}

{{#if recommendations}}
**Recommendations**:
{{#each recommendations}}
- {{this}}
{{/each}}
{{/if}}

{{/each}}

## Summary

{{#if validation_results.meets_standards}}
✅ This agent meets all quality standards and is ready for integration.
{{else}}
❌ This agent requires improvements before integration. Please address the recommendations above.
{{/if}}
        """
        
        return report

# Usage example
if __name__ == "__main__":
    quality_standards = {
        'market_relevance': 0.8,
        'technical_feasibility': 0.9,
        'content_completeness': 0.95,
        'integration_compatibility': 0.9,
        'documentation_quality': 0.85
    }
    
    validator = AgentQualityValidator(quality_standards)
    
    # Load agent specification
    agent_spec = {{agent_specification_json}}
    
    # Validate agent
    results = validator.validate_agent(agent_spec)
    
    # Generate report
    report = validator.generate_validation_report(results)
    
    print(report)
```

This comprehensive template system ensures consistent, high-quality agent generation with full automation and validation capabilities, maintaining the JAEGIS Method's standards while incorporating real-time market intelligence.
