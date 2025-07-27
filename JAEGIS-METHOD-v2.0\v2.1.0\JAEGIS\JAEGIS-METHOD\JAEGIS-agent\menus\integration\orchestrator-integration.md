# JAEGIS Orchestrator Integration
## Help System Integration with Main JAEGIS Orchestrator

### Integration Overview
This document defines how the help system integrates with the main JAEGIS orchestrator to ensure seamless operation and consistent command availability across all interactions.

---

## 🔗 **ORCHESTRATOR INTEGRATION SYSTEM**

### **Integration Architecture**
```python
class JAEGISOrchestratorIntegration:
    """
    Integration system connecting help system with main JAEGIS orchestrator
    """
    
    def __init__(self):
        """
        Initialize orchestrator integration with help system
        """
        print("🔗 JAEGIS ORCHESTRATOR INTEGRATION: INITIALIZING")
        
        # Load integration components
        self.help_system = self.load_help_system()
        self.orchestrator_hooks = self.establish_orchestrator_hooks()
        self.input_interceptor = self.initialize_input_interceptor()
        self.command_router = self.initialize_command_router()
        
        print("   ✅ Help system: LOADED")
        print("   ✅ Orchestrator hooks: ESTABLISHED")
        print("   ✅ Input interceptor: ACTIVE")
        print("   ✅ Command router: OPERATIONAL")
        print("   ✅ Integration: COMPLETE")
    
    def establish_orchestrator_hooks(self):
        """
        Establish hooks with main JAEGIS orchestrator system
        """
        orchestrator_hooks = {
            'initialization_hook': {
                'trigger': 'orchestrator_startup',
                'priority': 'CRITICAL',
                'action': 'load_help_system_immediately',
                'validation': 'verify_help_system_operational'
            },
            'input_processing_hook': {
                'trigger': 'before_user_input_processing',
                'priority': 'HIGHEST',
                'action': 'intercept_help_requests',
                'method': 'check_for_help_patterns_first'
            },
            'mode_selection_hook': {
                'trigger': 'mode_selection_display',
                'priority': 'HIGH',
                'action': 'include_help_information',
                'method': 'add_help_context_to_mode_menu'
            },
            'agent_activation_hook': {
                'trigger': 'agent_activation_sequence',
                'priority': 'MEDIUM',
                'action': 'preserve_help_availability',
                'method': 'maintain_help_during_agent_switch'
            }
        }
        
        return orchestrator_hooks
    
    def initialize_input_interceptor(self):
        """
        Initialize input interceptor for help request detection
        """
        interceptor_config = {
            'interception_patterns': [
                # Exact command patterns
                r'^/help$', r'^/HELP$', r'^help$', r'^HELP$',
                
                # Natural language patterns
                r'.*what commands.*available.*',
                r'.*show.*all commands.*',
                r'.*how.*commands work.*',
                r'.*list.*commands.*',
                r'.*help.*commands.*',
                r'.*what can.*do.*',
                r'.*available commands.*',
                r'.*command list.*',
                r'.*show commands.*',
                r'.*help menu.*'
            ],
            'interception_priority': 'HIGHEST',
            'processing_method': 'immediate_help_response',
            'fallback_behavior': 'pass_to_normal_processing'
        }
        
        return interceptor_config
    
    def initialize_command_router(self):
        """
        Initialize command router for help system integration
        """
        router_config = {
            'routing_logic': {
                'help_requests': 'route_to_help_system',
                'agent_commands': 'route_to_agent_activation',
                'workflow_commands': 'route_to_workflow_system',
                'unknown_commands': 'route_to_help_suggestion'
            },
            'integration_points': {
                'help_system': 'direct_integration',
                'agent_system': 'coordinated_integration',
                'workflow_system': 'collaborative_integration'
            },
            'error_handling': {
                'help_system_failure': 'fallback_to_basic_help',
                'routing_failure': 'display_available_commands',
                'integration_failure': 'emergency_help_mode'
            }
        }
        
        return router_config
    
    def process_user_input(self, user_input):
        """
        Process user input with help system integration
        """
        # Step 1: Check for help requests first (highest priority)
        if self.is_help_request(user_input):
            return self.handle_help_request(user_input)
        
        # Step 2: Check for agent commands
        if self.is_agent_command(user_input):
            return self.handle_agent_command(user_input)
        
        # Step 3: Check for workflow commands
        if self.is_workflow_command(user_input):
            return self.handle_workflow_command(user_input)
        
        # Step 4: Pass to normal orchestrator processing
        return self.pass_to_orchestrator(user_input)
    
    def is_help_request(self, user_input):
        """
        Check if user input is a help request
        """
        import re
        
        normalized_input = user_input.strip().lower()
        
        # Check exact patterns
        exact_patterns = ['/help', '/HELP', 'help', 'HELP']
        if normalized_input in [p.lower() for p in exact_patterns]:
            return True
        
        # Check natural language patterns
        natural_patterns = [
            'what commands are available',
            'show me all commands',
            'how do the commands work',
            'list all commands',
            'help me with commands',
            'what can i do',
            'available commands',
            'command list',
            'show commands',
            'help menu'
        ]
        
        for pattern in natural_patterns:
            if pattern in normalized_input:
                return True
        
        # Check partial patterns
        help_keywords = ['command', 'commands', 'help', 'menu', 'available', 'list', 'show']
        question_words = ['what', 'how', 'where', 'which']
        
        words = normalized_input.split()
        has_help_keyword = any(word in help_keywords for word in words)
        has_question_word = any(word in question_words for word in words)
        
        if has_help_keyword and has_question_word:
            return True
        
        return False
    
    def handle_help_request(self, user_input):
        """
        Handle help request by routing to help system
        """
        help_response = self.help_system.generate_complete_help_menu()
        return {
            'response_type': 'help_menu',
            'content': help_response,
            'source': 'integrated_help_system',
            'processed_by': 'orchestrator_integration'
        }
    
    def integrate_with_mode_selection(self):
        """
        Integrate help information with mode selection menu
        """
        mode_selection_integration = {
            'help_context_addition': {
                'location': 'after_mode_options',
                'content': '💡 **Need Help?** Type `/help` or "what commands are available?" at any time for complete command list.',
                'formatting': 'highlighted_tip'
            },
            'command_preview': {
                'location': 'before_mode_selection',
                'content': '📋 **Quick Commands**: `/help` (full help), `/agent-list` (see agents), `/{agent}` (activate agent)',
                'formatting': 'quick_reference'
            }
        }
        
        return mode_selection_integration
    
    def maintain_help_during_agent_switch(self):
        """
        Maintain help system availability during agent switching
        """
        agent_switch_maintenance = {
            'pre_switch_actions': [
                'preserve_help_system_state',
                'maintain_help_command_registration',
                'ensure_help_router_availability'
            ],
            'during_switch_actions': [
                'keep_help_system_active',
                'update_agent_specific_commands',
                'maintain_universal_help_recognition'
            ],
            'post_switch_actions': [
                'verify_help_system_functionality',
                'test_help_command_response',
                'confirm_agent_command_integration'
            ]
        }
        
        return agent_switch_maintenance
```

### **Integration Testing Framework**
```yaml
integration_testing:
  orchestrator_startup_test:
    description: "Verify help system loads with orchestrator"
    test_cases:
      - "Help system initializes within 2 seconds of orchestrator startup"
      - "Help command responds immediately after initialization"
      - "All help patterns recognized from startup"
    
  input_interception_test:
    description: "Verify help requests are intercepted correctly"
    test_cases:
      - "Exact help commands intercepted before normal processing"
      - "Natural language help requests recognized and routed"
      - "Non-help inputs passed to normal processing"
    
  agent_integration_test:
    description: "Verify help system works during agent operations"
    test_cases:
      - "Help available during agent activation"
      - "Help works within agent contexts"
      - "Agent-specific commands appear in help"
    
  mode_selection_test:
    description: "Verify help integration with mode selection"
    test_cases:
      - "Help context appears in mode selection menu"
      - "Help commands work during mode selection"
      - "Mode selection doesn't interfere with help system"
```

### **Error Handling and Fallbacks**
```python
class IntegrationErrorHandling:
    """
    Error handling and fallback mechanisms for orchestrator integration
    """
    
    def handle_integration_failures(self):
        """
        Handle various integration failure scenarios
        """
        failure_handlers = {
            'help_system_load_failure': {
                'action': 'load_basic_help_fallback',
                'message': 'Help system loading with basic functionality',
                'recovery': 'attempt_full_reload_in_background'
            },
            'input_interception_failure': {
                'action': 'disable_interception_use_polling',
                'message': 'Help available via direct /help command',
                'recovery': 'restore_interception_when_possible'
            },
            'orchestrator_hook_failure': {
                'action': 'run_help_system_independently',
                'message': 'Help system running in standalone mode',
                'recovery': 'attempt_hook_reestablishment'
            }
        }
        
        return failure_handlers
```

This integration ensures the help system works seamlessly with the main JAEGIS orchestrator, providing consistent and reliable access to help functionality across all interactions.
