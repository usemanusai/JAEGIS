# JAEGIS Agent File Organization System
## Automated File Placement and Directory Structure Management

### System Overview
This system provides automated file organization and deployment functionality for the JAEGIS Agent Builder Enhancement Squad, ensuring all generated agent files are automatically placed in the correct directory structure without manual intervention.

---

## 🗂️ **AUTOMATED FILE ORGANIZATION ARCHITECTURE**

### **File Organization Manager**
```python
class JAEGISFileOrganizationManager:
    def __init__(self):
        """
        Automated file organization and deployment system for JAEGIS agents
        """
        print("🗂️ JAEGIS File Organization System: INITIALIZING")
        
        # Define JAEGIS directory structure
        self.jaegis_structure = {
            'base_path': 'JAEGIS-METHOD-v2.0/v2.1.0/JAEGIS/JAEGIS-METHOD/JAEGIS-agent',
            'directories': {
                'personas': {
                    'path': 'personas/',
                    'file_types': ['.md'],
                    'naming_convention': '{agent-name}.md',
                    'description': 'Agent personality and behavior definitions'
                },
                'tasks': {
                    'path': 'tasks/',
                    'file_types': ['.md'],
                    'naming_convention': '{task-name}.md',
                    'description': 'Task workflow and capability definitions'
                },
                'templates': {
                    'path': 'templates/',
                    'file_types': ['.md'],
                    'naming_convention': '{template-name}.md',
                    'description': 'Reusable template frameworks'
                },
                'checklists': {
                    'path': 'checklists/',
                    'file_types': ['.md'],
                    'naming_convention': '{checklist-name}.md',
                    'description': 'Quality assurance and validation checklists'
                },
                'data': {
                    'path': 'data/',
                    'file_types': ['.md', '.json', '.yaml'],
                    'naming_convention': '{data-name}.{extension}',
                    'description': 'Reference data and configuration files'
                }
            }
        }
        
        # Initialize file deployment system
        self.deployment_system = FileDeploymentSystem(self.jaegis_structure)
        
        print("   ✅ Directory structure mapping: LOADED")
        print("   ✅ File deployment system: READY")
        print("   ✅ Path resolution engine: ACTIVE")
    
    def organize_agent_files(self, agent_generation_result):
        """
        Organize and deploy all files for a generated agent
        """
        print(f"🚀 Organizing files for agent: {agent_generation_result['agent_name']}")
        
        organization_plan = self.create_organization_plan(agent_generation_result)
        deployment_result = self.execute_file_deployment(organization_plan)
        validation_result = self.validate_file_placement(deployment_result)
        
        return {
            'organization_successful': validation_result['all_files_placed'],
            'files_deployed': deployment_result['deployed_files'],
            'deployment_summary': deployment_result['summary'],
            'validation_report': validation_result
        }
    
    def create_organization_plan(self, agent_generation_result):
        """
        Create comprehensive file organization plan
        """
        organization_plan = {
            'agent_name': agent_generation_result['agent_name'],
            'file_mappings': [],
            'directory_operations': [],
            'validation_requirements': []
        }
        
        # Map persona files
        if 'persona_files' in agent_generation_result:
            for persona_file in agent_generation_result['persona_files']:
                file_mapping = self.create_file_mapping(
                    persona_file, 'personas', agent_generation_result['agent_name']
                )
                organization_plan['file_mappings'].append(file_mapping)
        
        # Map task files
        if 'task_files' in agent_generation_result:
            for task_file in agent_generation_result['task_files']:
                file_mapping = self.create_file_mapping(
                    task_file, 'tasks', task_file['task_name']
                )
                organization_plan['file_mappings'].append(file_mapping)
        
        # Map template files
        if 'template_files' in agent_generation_result:
            for template_file in agent_generation_result['template_files']:
                file_mapping = self.create_file_mapping(
                    template_file, 'templates', template_file['template_name']
                )
                organization_plan['file_mappings'].append(file_mapping)
        
        # Map checklist files
        if 'checklist_files' in agent_generation_result:
            for checklist_file in agent_generation_result['checklist_files']:
                file_mapping = self.create_file_mapping(
                    checklist_file, 'checklists', checklist_file['checklist_name']
                )
                organization_plan['file_mappings'].append(file_mapping)
        
        # Map data files
        if 'data_files' in agent_generation_result:
            for data_file in agent_generation_result['data_files']:
                file_mapping = self.create_file_mapping(
                    data_file, 'data', data_file['data_name']
                )
                organization_plan['file_mappings'].append(file_mapping)
        
        return organization_plan
    
    def create_file_mapping(self, file_data, directory_type, file_identifier):
        """
        Create individual file mapping with path resolution
        """
        directory_config = self.jaegis_structure['directories'][directory_type]
        
        # Generate target filename
        if directory_type == 'personas':
            target_filename = f"{file_identifier.lower().replace(' ', '-')}.md"
        elif directory_type == 'tasks':
            target_filename = f"{file_identifier.lower().replace(' ', '-')}.md"
        elif directory_type == 'templates':
            target_filename = f"{file_identifier.lower().replace(' ', '-')}-template.md"
        elif directory_type == 'checklists':
            target_filename = f"{file_identifier.lower().replace(' ', '-')}-checklist.md"
        elif directory_type == 'data':
            extension = file_data.get('file_extension', 'md')
            target_filename = f"{file_identifier.lower().replace(' ', '-')}.{extension}"
        
        # Create full target path
        target_path = os.path.join(
            self.jaegis_structure['base_path'],
            directory_config['path'],
            target_filename
        )
        
        return {
            'source_content': file_data['content'],
            'target_path': target_path,
            'target_filename': target_filename,
            'directory_type': directory_type,
            'file_identifier': file_identifier,
            'content_length': len(file_data['content']),
            'deployment_priority': self.get_deployment_priority(directory_type)
        }
    
    def get_deployment_priority(self, directory_type):
        """
        Get deployment priority for different file types
        """
        priority_map = {
            'personas': 1,  # Deploy personas first
            'tasks': 2,     # Then tasks
            'templates': 3, # Then templates
            'checklists': 4, # Then checklists
            'data': 5       # Finally data files
        }
        return priority_map.get(directory_type, 10)
```

### **File Deployment System**
```python
class FileDeploymentSystem:
    def __init__(self, jaegis_structure):
        """
        System for deploying files to correct JAEGIS directory structure
        """
        self.jaegis_structure = jaegis_structure
        self.deployment_log = []
        
    def execute_file_deployment(self, organization_plan):
        """
        Execute complete file deployment based on organization plan
        """
        print("📁 Executing File Deployment...")
        
        deployment_result = {
            'deployed_files': [],
            'failed_deployments': [],
            'created_directories': [],
            'summary': {}
        }
        
        # Sort file mappings by deployment priority
        sorted_mappings = sorted(
            organization_plan['file_mappings'],
            key=lambda x: x['deployment_priority']
        )
        
        # Deploy files in priority order
        for file_mapping in sorted_mappings:
            try:
                deployment_success = self.deploy_individual_file(file_mapping)
                
                if deployment_success:
                    deployment_result['deployed_files'].append(file_mapping)
                    print(f"   ✅ Deployed: {file_mapping['target_filename']}")
                else:
                    deployment_result['failed_deployments'].append(file_mapping)
                    print(f"   ❌ Failed: {file_mapping['target_filename']}")
                    
            except Exception as e:
                deployment_result['failed_deployments'].append({
                    **file_mapping,
                    'error': str(e)
                })
                print(f"   ❌ Error deploying {file_mapping['target_filename']}: {str(e)}")
        
        # Generate deployment summary
        deployment_result['summary'] = self.generate_deployment_summary(deployment_result)
        
        return deployment_result
    
    def deploy_individual_file(self, file_mapping):
        """
        Deploy individual file to target location
        """
        target_path = file_mapping['target_path']
        target_directory = os.path.dirname(target_path)
        
        # Ensure target directory exists
        if not os.path.exists(target_directory):
            os.makedirs(target_directory, exist_ok=True)
            print(f"   📁 Created directory: {target_directory}")
        
        # Write file content to target location
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(file_mapping['source_content'])
            
            # Verify file was created successfully
            if os.path.exists(target_path):
                file_size = os.path.getsize(target_path)
                self.deployment_log.append({
                    'timestamp': self.get_current_timestamp(),
                    'action': 'FILE_DEPLOYED',
                    'target_path': target_path,
                    'file_size': file_size,
                    'success': True
                })
                return True
            else:
                return False
                
        except Exception as e:
            self.deployment_log.append({
                'timestamp': self.get_current_timestamp(),
                'action': 'FILE_DEPLOYMENT_FAILED',
                'target_path': target_path,
                'error': str(e),
                'success': False
            })
            return False
    
    def generate_deployment_summary(self, deployment_result):
        """
        Generate comprehensive deployment summary
        """
        total_files = len(deployment_result['deployed_files']) + len(deployment_result['failed_deployments'])
        success_rate = (len(deployment_result['deployed_files']) / total_files * 100) if total_files > 0 else 0
        
        summary = {
            'total_files_processed': total_files,
            'successful_deployments': len(deployment_result['deployed_files']),
            'failed_deployments': len(deployment_result['failed_deployments']),
            'success_rate': f"{success_rate:.1f}%",
            'deployment_complete': len(deployment_result['failed_deployments']) == 0
        }
        
        # Categorize deployments by directory type
        deployment_by_type = {}
        for file_mapping in deployment_result['deployed_files']:
            directory_type = file_mapping['directory_type']
            if directory_type not in deployment_by_type:
                deployment_by_type[directory_type] = 0
            deployment_by_type[directory_type] += 1
        
        summary['deployments_by_type'] = deployment_by_type
        
        return summary
    
    def get_current_timestamp(self):
        """
        Get current timestamp for logging
        """
        from datetime import datetime
        return datetime.now().isoformat()
```

### **Path Resolution Engine**
```python
class PathResolutionEngine:
    def __init__(self, jaegis_structure):
        """
        Engine for resolving and validating JAEGIS file paths
        """
        self.jaegis_structure = jaegis_structure
        self.path_cache = {}
    
    def resolve_agent_file_paths(self, agent_name, file_types):
        """
        Resolve all file paths for a specific agent
        """
        resolved_paths = {}
        
        for file_type in file_types:
            if file_type in self.jaegis_structure['directories']:
                directory_config = self.jaegis_structure['directories'][file_type]
                
                # Generate filename based on agent name and file type
                filename = self.generate_filename(agent_name, file_type)
                
                # Create full path
                full_path = os.path.join(
                    self.jaegis_structure['base_path'],
                    directory_config['path'],
                    filename
                )
                
                resolved_paths[file_type] = {
                    'full_path': full_path,
                    'filename': filename,
                    'directory': directory_config['path'],
                    'exists': os.path.exists(full_path)
                }
        
        return resolved_paths
    
    def generate_filename(self, agent_name, file_type):
        """
        Generate appropriate filename based on agent name and file type
        """
        base_name = agent_name.lower().replace(' ', '-').replace('_', '-')
        
        filename_patterns = {
            'personas': f"{base_name}.md",
            'tasks': f"{base_name}-tasks.md",
            'templates': f"{base_name}-template.md",
            'checklists': f"{base_name}-checklist.md",
            'data': f"{base_name}-data.md"
        }
        
        return filename_patterns.get(file_type, f"{base_name}.md")
    
    def validate_path_structure(self):
        """
        Validate that all required JAEGIS directories exist
        """
        validation_result = {
            'structure_valid': True,
            'missing_directories': [],
            'directory_status': {}
        }
        
        base_path = self.jaegis_structure['base_path']
        
        # Check base path exists
        if not os.path.exists(base_path):
            validation_result['structure_valid'] = False
            validation_result['missing_directories'].append(base_path)
        
        # Check each required directory
        for dir_name, dir_config in self.jaegis_structure['directories'].items():
            dir_path = os.path.join(base_path, dir_config['path'])
            
            if os.path.exists(dir_path):
                validation_result['directory_status'][dir_name] = 'EXISTS'
            else:
                validation_result['structure_valid'] = False
                validation_result['missing_directories'].append(dir_path)
                validation_result['directory_status'][dir_name] = 'MISSING'
        
        return validation_result
```

This file organization system provides the missing automated file placement functionality that the Agent Builder Enhancement Squad needs to properly deploy generated agent files to the correct JAEGIS directory structure.

---

## 🔧 **INTEGRATION WITH AGENT BUILDER ENHANCEMENT SQUAD**

### **Enhanced Workflow Orchestrator Agent Integration**
```python
class EnhancedWorkflowOrchestratorAgent:
    def __init__(self):
        """
        Enhanced Workflow Orchestrator with integrated file organization
        """
        self.file_organization_manager = JAEGISFileOrganizationManager()
        self.deployment_system = self.file_organization_manager.deployment_system
        self.path_resolver = PathResolutionEngine(self.file_organization_manager.jaegis_structure)

        print("🔧 Enhanced Workflow Orchestrator: INITIALIZED")
        print("   ✅ File organization integration: ACTIVE")
        print("   ✅ Automated deployment: READY")

    def orchestrate_agent_creation_workflow(self, agent_requirements):
        """
        Complete agent creation workflow with automated file organization
        """
        print(f"🚀 Orchestrating agent creation: {agent_requirements['agent_name']}")

        # Phase 1: Agent Generation
        generation_result = self.generate_agent_components(agent_requirements)

        # Phase 2: File Organization and Deployment
        organization_result = self.file_organization_manager.organize_agent_files(generation_result)

        # Phase 3: System Integration
        integration_result = self.integrate_agent_with_jaegis_system(generation_result, organization_result)

        # Phase 4: Validation and Testing
        validation_result = self.validate_complete_agent_deployment(integration_result)

        return {
            'workflow_successful': validation_result['deployment_valid'],
            'agent_name': agent_requirements['agent_name'],
            'generation_result': generation_result,
            'organization_result': organization_result,
            'integration_result': integration_result,
            'validation_result': validation_result
        }

    def generate_agent_components(self, agent_requirements):
        """
        Generate all required agent components
        """
        print("   📝 Generating agent components...")

        # Generate persona file
        persona_content = self.generate_agent_persona(agent_requirements)

        # Generate task files (minimum 4-6 tasks per agent)
        task_files = self.generate_agent_tasks(agent_requirements)

        # Generate template files (minimum 2-4 templates)
        template_files = self.generate_agent_templates(agent_requirements)

        # Generate checklist files (minimum 2-3 checklists)
        checklist_files = self.generate_agent_checklists(agent_requirements)

        # Generate data files (minimum 1-3 data files)
        data_files = self.generate_agent_data_files(agent_requirements)

        return {
            'agent_name': agent_requirements['agent_name'],
            'persona_files': [{'content': persona_content, 'filename': f"{agent_requirements['agent_name'].lower().replace(' ', '-')}.md"}],
            'task_files': task_files,
            'template_files': template_files,
            'checklist_files': checklist_files,
            'data_files': data_files,
            'generation_timestamp': self.get_current_timestamp(),
            'generation_successful': True
        }

    def integrate_agent_with_jaegis_system(self, generation_result, organization_result):
        """
        Integrate newly created agent with JAEGIS system configuration
        """
        print("   🔗 Integrating with JAEGIS system...")

        if not organization_result['organization_successful']:
            return {
                'integration_successful': False,
                'error': 'File organization failed - cannot proceed with system integration'
            }

        # Update agent-config.txt
        config_update_result = self.update_agent_configuration(generation_result)

        # Validate system coherence
        coherence_validation = self.validate_system_coherence(generation_result)

        # Update system documentation
        documentation_update = self.update_system_documentation(generation_result)

        return {
            'integration_successful': all([
                config_update_result['success'],
                coherence_validation['valid'],
                documentation_update['success']
            ]),
            'config_update': config_update_result,
            'coherence_validation': coherence_validation,
            'documentation_update': documentation_update
        }

    def validate_complete_agent_deployment(self, integration_result):
        """
        Comprehensive validation of complete agent deployment
        """
        print("   ✅ Validating complete deployment...")

        validation_checks = {
            'file_deployment_valid': self.validate_file_deployment(),
            'system_integration_valid': integration_result['integration_successful'],
            'configuration_valid': self.validate_agent_configuration(),
            'directory_structure_valid': self.path_resolver.validate_path_structure()['structure_valid'],
            'agent_accessibility_valid': self.validate_agent_accessibility()
        }

        deployment_valid = all(validation_checks.values())

        return {
            'deployment_valid': deployment_valid,
            'validation_checks': validation_checks,
            'validation_timestamp': self.get_current_timestamp(),
            'next_steps': self.generate_next_steps(deployment_valid, validation_checks)
        }
```

### **Automated Directory Structure Creation**
```python
class AutomatedDirectoryManager:
    def __init__(self, jaegis_structure):
        """
        Manager for automated JAEGIS directory structure creation and maintenance
        """
        self.jaegis_structure = jaegis_structure

    def ensure_directory_structure_exists(self):
        """
        Ensure complete JAEGIS directory structure exists
        """
        print("📁 Ensuring JAEGIS directory structure...")

        base_path = self.jaegis_structure['base_path']

        # Create base directory if it doesn't exist
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)
            print(f"   📁 Created base directory: {base_path}")

        # Create all required subdirectories
        created_directories = []
        for dir_name, dir_config in self.jaegis_structure['directories'].items():
            dir_path = os.path.join(base_path, dir_config['path'])

            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                created_directories.append(dir_path)
                print(f"   📁 Created directory: {dir_path}")

        return {
            'structure_created': True,
            'created_directories': created_directories,
            'base_path': base_path
        }

    def create_directory_readme_files(self):
        """
        Create README files for each directory explaining its purpose
        """
        print("📄 Creating directory documentation...")

        for dir_name, dir_config in self.jaegis_structure['directories'].items():
            dir_path = os.path.join(self.jaegis_structure['base_path'], dir_config['path'])
            readme_path = os.path.join(dir_path, 'README.md')

            if not os.path.exists(readme_path):
                readme_content = self.generate_directory_readme(dir_name, dir_config)

                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)

                print(f"   📄 Created README: {readme_path}")

    def generate_directory_readme(self, dir_name, dir_config):
        """
        Generate README content for directory
        """
        return f"""# {dir_name.title()} Directory

## Purpose
{dir_config['description']}

## File Types
Supported file types: {', '.join(dir_config['file_types'])}

## Naming Convention
Files should follow the pattern: `{dir_config['naming_convention']}`

## Directory Structure
This directory is part of the JAEGIS Method v2.0 agent system and contains files that define agent {dir_name}.

## Automated Management
This directory is automatically managed by the JAEGIS Agent Builder Enhancement Squad. Files are automatically organized and deployed here during agent creation workflows.

---
*Generated by JAEGIS Agent File Organization System*
*Last updated: {self.get_current_timestamp()}*
"""
```

### **File Validation and Quality Assurance**
```python
class FileValidationSystem:
    def __init__(self):
        """
        System for validating deployed agent files
        """
        self.validation_rules = {
            'personas': {
                'min_lines': 300,
                'required_sections': ['Core Identity', 'Primary Mission', 'Enhanced Capabilities'],
                'file_extension': '.md'
            },
            'tasks': {
                'min_lines': 400,
                'required_sections': ['Purpose', 'Enhanced Capabilities', 'Implementation'],
                'file_extension': '.md'
            },
            'templates': {
                'min_lines': 300,
                'required_sections': ['Overview', 'Framework', 'Usage'],
                'file_extension': '.md'
            },
            'checklists': {
                'min_lines': 200,
                'required_sections': ['Checklist Overview', 'Validation Steps'],
                'file_extension': '.md'
            },
            'data': {
                'min_lines': 100,
                'file_extension': ['.md', '.json', '.yaml']
            }
        }

    def validate_deployed_files(self, deployment_result):
        """
        Validate all deployed files against quality standards
        """
        print("🔍 Validating deployed files...")

        validation_results = []

        for file_mapping in deployment_result['deployed_files']:
            file_validation = self.validate_individual_file(file_mapping)
            validation_results.append(file_validation)

            if file_validation['valid']:
                print(f"   ✅ Valid: {file_mapping['target_filename']}")
            else:
                print(f"   ❌ Invalid: {file_mapping['target_filename']} - {file_validation['issues']}")

        overall_valid = all(result['valid'] for result in validation_results)

        return {
            'all_files_valid': overall_valid,
            'individual_validations': validation_results,
            'validation_summary': self.generate_validation_summary(validation_results)
        }

    def validate_individual_file(self, file_mapping):
        """
        Validate individual file against quality standards
        """
        directory_type = file_mapping['directory_type']
        target_path = file_mapping['target_path']

        validation_result = {
            'file_path': target_path,
            'directory_type': directory_type,
            'valid': True,
            'issues': []
        }

        # Check if file exists
        if not os.path.exists(target_path):
            validation_result['valid'] = False
            validation_result['issues'].append('File does not exist')
            return validation_result

        # Get validation rules for this directory type
        rules = self.validation_rules.get(directory_type, {})

        # Read file content
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            validation_result['valid'] = False
            validation_result['issues'].append(f'Cannot read file: {str(e)}')
            return validation_result

        # Validate minimum line count
        if 'min_lines' in rules:
            line_count = len(content.split('\n'))
            if line_count < rules['min_lines']:
                validation_result['valid'] = False
                validation_result['issues'].append(f'File has {line_count} lines, minimum required: {rules["min_lines"]}')

        # Validate required sections
        if 'required_sections' in rules:
            for section in rules['required_sections']:
                if section not in content:
                    validation_result['valid'] = False
                    validation_result['issues'].append(f'Missing required section: {section}')

        return validation_result
```

This enhanced integration system provides complete automated file organization, deployment, and validation functionality for the JAEGIS Agent Builder Enhancement Squad, ensuring all generated agent files are properly placed in the correct directory structure with comprehensive quality assurance.
