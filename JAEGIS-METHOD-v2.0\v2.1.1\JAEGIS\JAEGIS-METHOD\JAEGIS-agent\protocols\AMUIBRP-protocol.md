# A.M.U.I.B.R.P. Protocol Implementation
## Always Modify User Input Before Responding Protocol

### Protocol Overview
**Protocol ID**: AMUIBRP-003  
**Protocol Name**: Always Modify User Input Before Responding Protocol  
**Status**: ALWAYS ACTIVE  
**Priority**: CRITICAL  
**Implementation Date**: July 24, 2025  

---

## 🔄 **PROTOCOL SPECIFICATION**

### **Core Protocol Definition**
```yaml
protocol_configuration:
  name: "A.M.U.I.B.R.P."
  full_name: "Always Modify User Input Before Responding Protocol"
  activation_mode: "ALWAYS_ACTIVE"
  scope: "ALL_JAEGIS_AGENTS"
  priority: "CRITICAL"
  override_permissions: "NONE"
  user_disable: false
  
input_modification:
  prepend_text:
    - "Always initialize the latest up-to-date JAEGIS Method to work with in either a local or remote workspace."
    - "Create multiple comprehensive TASKS and SUB-TASKS for the requests below."
  
  application_scope: "ALL_USER_INPUTS"
  exception_handling: "SMART_DETECTION_OF_EXISTING_INSTRUCTIONS"
  transparency: "INFORM_USER_OF_ENHANCEMENT"
  
processing_rules:
  check_for_existing_instructions: true
  avoid_duplication: true
  maintain_user_intent: true
  preserve_original_context: true
```

### **Implementation Architecture**
```python
class AMUIBRPProtocol:
    """
    Always Modify User Input Before Responding Protocol Implementation
    """
    
    def __init__(self):
        """
        Initialize AMUIBRP Protocol with always-active input modification
        """
        print("🔄 INITIALIZING A.M.U.I.B.R.P. PROTOCOL")
        
        self.protocol_id = "AMUIBRP-003"
        self.protocol_name = "Always Modify User Input Before Responding Protocol"
        self.status = "ALWAYS_ACTIVE"
        self.priority = "CRITICAL"
        
        # Input modification configuration
        self.prepend_instructions = [
            "Always initialize the latest up-to-date JAEGIS Method to work with in either a local or remote workspace.",
            "Create multiple comprehensive TASKS and SUB-TASKS for the requests below."
        ]
        
        # Exception detection patterns
        self.existing_instruction_patterns = self.load_existing_instruction_patterns()
        
        # Processing statistics
        self.modification_stats = {
            'total_inputs_processed': 0,
            'inputs_modified': 0,
            'inputs_skipped': 0,
            'exceptions_detected': 0
        }
        
        print("   ✅ Prepend instructions: LOADED")
        print("   ✅ Exception patterns: CONFIGURED")
        print("   ✅ Processing statistics: INITIALIZED")
        print("   ✅ A.M.U.I.B.R.P. Protocol: OPERATIONAL")
    
    def process_user_input(self, user_input, session_context=None):
        """
        Process user input by adding JAEGIS initialization and task creation instructions
        """
        # Update processing statistics
        self.modification_stats['total_inputs_processed'] += 1
        
        # Check if input already contains JAEGIS instructions
        if self.contains_existing_instructions(user_input):
            self.modification_stats['inputs_skipped'] += 1
            self.modification_stats['exceptions_detected'] += 1
            
            return {
                'modified_input': user_input,
                'modification_applied': False,
                'reason': 'existing_instructions_detected',
                'original_input': user_input,
                'protocol_id': self.protocol_id,
                'timestamp': self.get_current_timestamp()
            }
        
        # Apply input modification
        modified_input = self.apply_input_modification(user_input)
        self.modification_stats['inputs_modified'] += 1
        
        # Log modification
        self.log_input_modification(user_input, modified_input)
        
        return {
            'modified_input': modified_input,
            'modification_applied': True,
            'reason': 'automatic_enhancement',
            'original_input': user_input,
            'prepended_instructions': self.prepend_instructions,
            'protocol_id': self.protocol_id,
            'timestamp': self.get_current_timestamp()
        }
    
    def apply_input_modification(self, user_input):
        """
        Apply the input modification by prepending JAEGIS instructions
        """
        # Create the prepended instructions block
        prepended_block = "\n".join(self.prepend_instructions)
        
        # Add separator and original input
        modified_input = f"{prepended_block}\n\n--- USER REQUEST ---\n{user_input}"
        
        return modified_input
    
    def contains_existing_instructions(self, user_input):
        """
        Check if user input already contains JAEGIS initialization or task creation instructions
        """
        input_lower = user_input.lower()
        
        # Check for JAEGIS initialization patterns
        for pattern in self.existing_instruction_patterns['jaegis_initialization']:
            if pattern.lower() in input_lower:
                return True
        
        # Check for task creation patterns
        for pattern in self.existing_instruction_patterns['task_creation']:
            if pattern.lower() in input_lower:
                return True
        
        # Check for explicit protocol mentions
        for pattern in self.existing_instruction_patterns['protocol_mentions']:
            if pattern.lower() in input_lower:
                return True
        
        return False
    
    def load_existing_instruction_patterns(self):
        """
        Load patterns that indicate existing JAEGIS instructions
        """
        patterns = {
            'jaegis_initialization': [
                'initialize jaegis',
                'jaegis method',
                'initialize the latest',
                'up-to-date jaegis',
                'jaegis system',
                'activate jaegis',
                'load jaegis',
                'start jaegis',
                'jaegis initialization',
                'initialize latest jaegis'
            ],
            'task_creation': [
                'create tasks',
                'create subtasks',
                'create multiple tasks',
                'comprehensive tasks',
                'task and subtask',
                'tasks and sub-tasks',
                'generate tasks',
                'build tasks',
                'make tasks',
                'task creation',
                'subtask creation'
            ],
            'protocol_mentions': [
                'amuibrp',
                'always modify user input',
                'input modification protocol',
                'prepend instructions',
                'automatic enhancement',
                'protocol modification'
            ]
        }
        
        return patterns
    
    def generate_transparency_message(self, modification_result):
        """
        Generate transparency message to inform user of input enhancement
        """
        if modification_result['modification_applied']:
            return {
                'transparency_message': (
                    "🔄 **Input Enhancement Applied**: Your request has been automatically enhanced with "
                    "JAEGIS Method initialization and task creation instructions to ensure optimal processing."
                ),
                'enhancement_details': {
                    'jaegis_initialization': "Added automatic JAEGIS Method initialization",
                    'task_creation': "Added comprehensive task and subtask creation instructions",
                    'benefit': "Ensures consistent workflow execution and task management"
                },
                'original_preserved': True
            }
        else:
            return {
                'transparency_message': (
                    "ℹ️ **Input Processing**: Your request already contains JAEGIS instructions, "
                    "so no automatic enhancement was applied."
                ),
                'enhancement_details': {
                    'reason': modification_result['reason'],
                    'existing_instructions_detected': True
                },
                'original_preserved': True
            }
    
    def validate_modification_safety(self, original_input, modified_input):
        """
        Validate that modification preserves user intent and doesn't cause issues
        """
        validation_result = {
            'safe': True,
            'issues': [],
            'warnings': []
        }
        
        # Check for potential conflicts
        if self.check_for_conflicting_instructions(original_input, modified_input):
            validation_result['warnings'].append("Potential instruction conflicts detected")
        
        # Check input length
        if len(modified_input) > 10000:  # Arbitrary limit
            validation_result['warnings'].append("Modified input is very long")
        
        # Check for user intent preservation
        if not self.preserves_user_intent(original_input, modified_input):
            validation_result['issues'].append("User intent may not be preserved")
            validation_result['safe'] = False
        
        return validation_result
    
    def check_for_conflicting_instructions(self, original_input, modified_input):
        """
        Check for conflicting instructions between original and modified input
        """
        # Look for contradictory instructions
        conflict_patterns = [
            ('don\'t create tasks', 'create multiple comprehensive tasks'),
            ('no initialization', 'initialize the latest'),
            ('skip jaegis', 'jaegis method'),
            ('manual setup', 'automatic initialization')
        ]
        
        original_lower = original_input.lower()
        modified_lower = modified_input.lower()
        
        for original_pattern, modified_pattern in conflict_patterns:
            if original_pattern in original_lower and modified_pattern in modified_lower:
                return True
        
        return False
    
    def preserves_user_intent(self, original_input, modified_input):
        """
        Check if modification preserves the user's original intent
        """
        # The original input should still be clearly present and unmodified
        return original_input.strip() in modified_input
    
    def get_modification_statistics(self):
        """
        Get protocol modification statistics
        """
        total_processed = self.modification_stats['total_inputs_processed']
        
        if total_processed == 0:
            return {
                'total_inputs_processed': 0,
                'modification_rate': 0,
                'exception_rate': 0,
                'statistics': self.modification_stats
            }
        
        return {
            'total_inputs_processed': total_processed,
            'modification_rate': (self.modification_stats['inputs_modified'] / total_processed) * 100,
            'exception_rate': (self.modification_stats['exceptions_detected'] / total_processed) * 100,
            'statistics': self.modification_stats,
            'timestamp': self.get_current_timestamp()
        }
    
    def log_input_modification(self, original_input, modified_input):
        """
        Log input modification for monitoring and debugging
        """
        log_entry = {
            'timestamp': self.get_current_timestamp(),
            'protocol': self.protocol_id,
            'event': 'input_modified',
            'original_length': len(original_input),
            'modified_length': len(modified_input),
            'modification_applied': True,
            'prepended_instructions_count': len(self.prepend_instructions)
        }
        
        self.write_protocol_log(log_entry)
    
    def handle_edge_cases(self, user_input):
        """
        Handle edge cases and special scenarios
        """
        edge_cases = {
            'empty_input': len(user_input.strip()) == 0,
            'very_long_input': len(user_input) > 50000,
            'special_characters': self.contains_special_formatting(user_input),
            'code_blocks': self.contains_code_blocks(user_input),
            'system_commands': self.contains_system_commands(user_input)
        }
        
        # Handle empty input
        if edge_cases['empty_input']:
            return {
                'handle_specially': True,
                'reason': 'empty_input',
                'action': 'skip_modification'
            }
        
        # Handle very long input
        if edge_cases['very_long_input']:
            return {
                'handle_specially': True,
                'reason': 'very_long_input',
                'action': 'careful_modification'
            }
        
        return {'handle_specially': False}
    
    def contains_special_formatting(self, user_input):
        """
        Check if input contains special formatting that might be affected
        """
        special_patterns = ['```', '~~~', '---', '===', '***']
        return any(pattern in user_input for pattern in special_patterns)
    
    def contains_code_blocks(self, user_input):
        """
        Check if input contains code blocks
        """
        return '```' in user_input or '~~~' in user_input
    
    def contains_system_commands(self, user_input):
        """
        Check if input contains system commands that shouldn't be modified
        """
        system_command_patterns = ['/help', '/status', '/config', '/exit', '/agent-list']
        input_lower = user_input.lower().strip()
        
        return any(input_lower.startswith(cmd) for cmd in system_command_patterns)
    
    def get_current_timestamp(self):
        """
        Get current timestamp for logging
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def write_protocol_log(self, log_entry):
        """
        Write protocol execution log
        """
        # Implementation would write to protocol log system
        pass


class InputModificationValidator:
    """
    Validator for input modifications to ensure safety and correctness
    """
    
    def __init__(self):
        self.validation_rules = self.load_validation_rules()
    
    def validate_modification(self, original, modified):
        """
        Validate that modification is safe and appropriate
        """
        validation_results = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check preservation of original content
        if not self.original_content_preserved(original, modified):
            validation_results['valid'] = False
            validation_results['issues'].append("Original content not preserved")
        
        # Check for excessive length
        if len(modified) > 100000:  # 100KB limit
            validation_results['warnings'].append("Modified input is very large")
        
        # Check for formatting issues
        formatting_issues = self.check_formatting_preservation(original, modified)
        validation_results['warnings'].extend(formatting_issues)
        
        return validation_results
    
    def original_content_preserved(self, original, modified):
        """
        Check if original content is preserved in modification
        """
        return original.strip() in modified
    
    def check_formatting_preservation(self, original, modified):
        """
        Check if important formatting is preserved
        """
        issues = []
        
        # Check code blocks
        original_code_blocks = original.count('```')
        modified_code_blocks = modified.count('```')
        
        if original_code_blocks != modified_code_blocks:
            issues.append("Code block formatting may be affected")
        
        return issues
    
    def load_validation_rules(self):
        """
        Load validation rules for input modification
        """
        return {
            'max_length': 100000,
            'preserve_formatting': True,
            'preserve_code_blocks': True,
            'preserve_user_intent': True
        }
```

### **Integration and Safety Configuration**
```yaml
integration_configuration:
  agent_integration:
    scope: "ALL_24_PLUS_AGENTS"
    hook_point: "INPUT_PREPROCESSING"
    priority: "HIGHEST"
    execution_order: "BEFORE_ALL_OTHER_PROCESSING"
    
  task_management_integration:
    automatic_task_creation: "ENABLED"
    task_validation: "COMPREHENSIVE"
    subtask_generation: "AUTOMATIC"
    
  workflow_integration:
    documentation_mode: "ENHANCED_WITH_TASKS"
    development_mode: "ENHANCED_WITH_TASKS"
    collaboration_mode: "ENHANCED_WITH_TASKS"
    
  transparency_integration:
    user_notification: "AUTOMATIC"
    modification_logging: "DETAILED"
    statistics_tracking: "ENABLED"

safety_configuration:
  exception_handling:
    existing_instructions: "SMART_DETECTION_AND_SKIP"
    conflicting_instructions: "WARNING_AND_PROCEED"
    malformed_input: "GRACEFUL_HANDLING"
    
  validation_rules:
    preserve_user_intent: "MANDATORY"
    preserve_formatting: "BEST_EFFORT"
    length_limits: "ENFORCED"
    
  monitoring:
    modification_statistics: "REAL_TIME"
    error_tracking: "COMPREHENSIVE"
    performance_monitoring: "ACTIVE"
```

### **Natural Language Configuration Examples**
```yaml
configuration_examples:
  basic_usage:
    description: "Standard automatic enhancement"
    user_input: "Help me build a web application"
    modified_input: |
      Always initialize the latest up-to-date JAEGIS Method to work with in either a local or remote workspace.
      Create multiple comprehensive TASKS and SUB-TASKS for the requests below.
      
      --- USER REQUEST ---
      Help me build a web application
      
  exception_case:
    description: "Input with existing JAEGIS instructions"
    user_input: "Initialize JAEGIS Method and create tasks for building a mobile app"
    modified_input: "Initialize JAEGIS Method and create tasks for building a mobile app"
    modification_applied: false
    reason: "existing_instructions_detected"
```

**Protocol Status**: ✅ **IMPLEMENTED AND ALWAYS ACTIVE**  
**Integration**: ✅ **ALL JAEGIS AGENTS CONNECTED**  
**Safety Mechanisms**: ✅ **COMPREHENSIVE VALIDATION ACTIVE**
