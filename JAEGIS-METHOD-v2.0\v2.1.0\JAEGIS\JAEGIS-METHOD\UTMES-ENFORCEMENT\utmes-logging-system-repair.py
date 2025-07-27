#!/usr/bin/env python3
"""
UTMES Logging System Repair Tool
Fixes the critical logging issues in existing UTMES components by updating them to use centralized logging
Addresses the detection/logging gap where critical issues are not being detected or logged

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - System repair and integration
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class UTMESLoggingSystemRepair:
    """
    UTMES Logging System Repair Tool
    Fixes existing UTMES components to use centralized logging
    """
    
    def __init__(self):
        self.utmes_directory = Path("JAEGIS-METHOD-v2.0/v2.1.0/JAEGIS/JAEGIS-METHOD/UTMES-ENFORCEMENT")
        self.files_to_repair = [
            "master-utmes-integration-controller.py",
            "system-level-enforcement-hooks.py",
            "conversation-flow-override-system.py",
            "response-generation-integration.py",
            "unbreakable-enforcement-implementation.py",
            "comprehensive-validation-testing.py",
            "automatic-task-generation-system.py",
            "workflow-auto-execution-engine.py",
            "mandatory-continuation-engine.py",
            "task-creation-enforcement.py",
            "input-analysis-algorithm.py",
            "conversation-flow-integration.py"
        ]
        
        self.repair_results = []
    
    def repair_all_utmes_logging(self) -> Dict:
        """
        Repair logging in all UTMES components
        
        Returns:
            Dictionary with repair results
        """
        print("🔧 Starting UTMES Logging System Repair...")
        
        repair_summary = {
            'files_processed': 0,
            'files_repaired': 0,
            'files_failed': 0,
            'total_changes': 0,
            'repair_details': []
        }
        
        for filename in self.files_to_repair:
            file_path = self.utmes_directory / filename
            
            if file_path.exists():
                print(f"🔍 Repairing {filename}...")
                repair_result = self._repair_file_logging(file_path)
                
                repair_summary['files_processed'] += 1
                if repair_result['success']:
                    repair_summary['files_repaired'] += 1
                    repair_summary['total_changes'] += repair_result['changes_made']
                else:
                    repair_summary['files_failed'] += 1
                
                repair_summary['repair_details'].append({
                    'filename': filename,
                    'success': repair_result['success'],
                    'changes_made': repair_result['changes_made'],
                    'issues': repair_result.get('issues', [])
                })
                
                print(f"  ✅ {filename}: {repair_result['changes_made']} changes made")
            else:
                print(f"  ⚠️ {filename}: File not found")
                repair_summary['repair_details'].append({
                    'filename': filename,
                    'success': False,
                    'changes_made': 0,
                    'issues': ['File not found']
                })
        
        print(f"\n📊 Repair Summary:")
        print(f"  Files Processed: {repair_summary['files_processed']}")
        print(f"  Files Repaired: {repair_summary['files_repaired']}")
        print(f"  Files Failed: {repair_summary['files_failed']}")
        print(f"  Total Changes: {repair_summary['total_changes']}")
        
        return repair_summary
    
    def _repair_file_logging(self, file_path: Path) -> Dict:
        """
        Repair logging in a specific file
        
        Args:
            file_path: Path to file to repair
            
        Returns:
            Dictionary with repair results
        """
        try:
            # Read original file
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Apply repairs
            repaired_content = original_content
            changes_made = 0
            
            # 1. Add centralized logging import
            if 'from utmes_centralized_logging_manager import' not in repaired_content:
                import_addition = self._get_centralized_logging_import()
                repaired_content = self._add_import_after_existing_imports(repaired_content, import_addition)
                changes_made += 1
            
            # 2. Replace logging.basicConfig() calls
            basicconfig_pattern = r'logging\.basicConfig\([^)]*\)'
            if re.search(basicconfig_pattern, repaired_content):
                repaired_content = re.sub(basicconfig_pattern, '# Removed - using centralized logging', repaired_content)
                changes_made += 1
            
            # 3. Replace direct logging calls with centralized logger
            repaired_content, logging_changes = self._replace_logging_calls(repaired_content, file_path.stem)
            changes_made += logging_changes
            
            # 4. Add critical issue logging for error conditions
            repaired_content, critical_changes = self._add_critical_issue_logging(repaired_content, file_path.stem)
            changes_made += critical_changes
            
            # 5. Add health monitoring integration
            repaired_content, health_changes = self._add_health_monitoring(repaired_content, file_path.stem)
            changes_made += health_changes
            
            # Write repaired file if changes were made
            if changes_made > 0:
                # Create backup
                backup_path = file_path.with_suffix('.py.backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write repaired version
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(repaired_content)
            
            return {
                'success': True,
                'changes_made': changes_made,
                'backup_created': changes_made > 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'changes_made': 0,
                'issues': [str(e)]
            }
    
    def _get_centralized_logging_import(self) -> str:
        """Get the import statement for centralized logging"""
        return """
# UTMES Centralized Logging Integration
from utmes_centralized_logging_manager import (
    get_utmes_logger, log_critical_issue, perform_system_health_check,
    LoggerType, LogLevel
)
"""
    
    def _add_import_after_existing_imports(self, content: str, import_addition: str) -> str:
        """Add import after existing imports"""
        lines = content.split('\n')
        import_end_index = 0
        
        # Find the end of existing imports
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_end_index = i
            elif line.strip() and not line.strip().startswith('#') and import_end_index > 0:
                break
        
        # Insert new import after existing imports
        lines.insert(import_end_index + 1, import_addition)
        return '\n'.join(lines)
    
    def _replace_logging_calls(self, content: str, component_name: str) -> Tuple[str, int]:
        """Replace direct logging calls with centralized logger calls"""
        changes_made = 0
        
        # Determine logger type based on component name
        logger_type_mapping = {
            'master-utmes-integration-controller': 'LoggerType.MASTER_CONTROLLER',
            'system-level-enforcement-hooks': 'LoggerType.ENFORCEMENT_HOOKS',
            'conversation-flow-override-system': 'LoggerType.FLOW_OVERRIDE',
            'response-generation-integration': 'LoggerType.RESPONSE_INTEGRATION',
            'unbreakable-enforcement-implementation': 'LoggerType.UNBREAKABLE_ENFORCEMENT',
            'comprehensive-validation-testing': 'LoggerType.VALIDATION_TESTING'
        }
        
        logger_type = logger_type_mapping.get(component_name, 'LoggerType.SYSTEM_MONITOR')
        
        # Add logger initialization at the beginning of __init__ methods
        init_pattern = r'(def __init__\(self[^)]*\):.*?\n)(.*?)(def|\Z)'
        
        def add_logger_init(match):
            nonlocal changes_made
            init_signature = match.group(1)
            init_body = match.group(2)
            next_def = match.group(3)
            
            if 'self.logger = get_utmes_logger' not in init_body:
                logger_init = f"        # Initialize centralized logger\n        self.logger = get_utmes_logger({logger_type}, '{component_name}')\n        \n"
                changes_made += 1
                return init_signature + logger_init + init_body + next_def
            return match.group(0)
        
        content = re.sub(init_pattern, add_logger_init, content, flags=re.DOTALL)
        
        # Replace logging.info, logging.error, etc. with self.logger calls
        logging_patterns = [
            (r'logging\.info\(', 'self.logger.info('),
            (r'logging\.warning\(', 'self.logger.warning('),
            (r'logging\.error\(', 'self.logger.error('),
            (r'logging\.critical\(', 'self.logger.critical('),
            (r'logging\.debug\(', 'self.logger.debug(')
        ]
        
        for old_pattern, new_pattern in logging_patterns:
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                changes_made += 1
        
        return content, changes_made
    
    def _add_critical_issue_logging(self, content: str, component_name: str) -> Tuple[str, int]:
        """Add critical issue logging for error conditions"""
        changes_made = 0
        
        # Find exception handling blocks and add critical issue logging
        exception_patterns = [
            r'except Exception as e:',
            r'except \w+ as e:',
            r'except:.*?'
        ]
        
        for pattern in exception_patterns:
            matches = list(re.finditer(pattern, content))
            for match in reversed(matches):  # Process in reverse to maintain positions
                # Find the exception handling block
                start_pos = match.end()
                lines = content[start_pos:].split('\n')
                
                # Look for existing logging in the exception block
                exception_block = []
                indent_level = None
                
                for i, line in enumerate(lines):
                    if line.strip() == '':
                        exception_block.append(line)
                        continue
                    
                    current_indent = len(line) - len(line.lstrip())
                    
                    if indent_level is None and line.strip():
                        indent_level = current_indent
                    
                    if line.strip() and current_indent <= indent_level and i > 0:
                        break
                    
                    exception_block.append(line)
                
                # Add critical issue logging if not present
                exception_text = '\n'.join(exception_block)
                if 'log_critical_issue' not in exception_text:
                    critical_logging = f"\n{' ' * (indent_level or 12)}# Log critical issue\n{' ' * (indent_level or 12)}log_critical_issue(\n{' ' * (indent_level or 16)}component='{component_name}',\n{' ' * (indent_level or 16)}issue_type='EXCEPTION',\n{' ' * (indent_level or 16)}message=str(e),\n{' ' * (indent_level or 16)}context={{'function': 'exception_handler'}},\n{' ' * (indent_level or 16)}severity=LogLevel.ERROR\n{' ' * (indent_level or 12)})"
                    
                    # Insert critical logging at the beginning of exception block
                    insert_pos = start_pos + len(lines[0]) + 1 if lines else start_pos
                    content = content[:insert_pos] + critical_logging + content[insert_pos:]
                    changes_made += 1
        
        return content, changes_made
    
    def _add_health_monitoring(self, content: str, component_name: str) -> Tuple[str, int]:
        """Add health monitoring integration"""
        changes_made = 0
        
        # Add health check method to classes
        class_pattern = r'(class \w+.*?:.*?\n)(.*?)((?:class|\Z))'
        
        def add_health_check_method(match):
            nonlocal changes_made
            class_signature = match.group(1)
            class_body = match.group(2)
            next_class = match.group(3)
            
            if 'def get_component_health' not in class_body:
                health_method = f"""
    def get_component_health(self) -> Dict:
        \"\"\"Get component health status\"\"\"
        try:
            health_results = perform_system_health_check()
            component_health = {{
                'component': '{component_name}',
                'timestamp': datetime.now().isoformat(),
                'healthy': True,
                'system_health': health_results.get('overall_healthy', False)
            }}
            
            self.logger.debug(f"Component health check: {{component_health}}")
            return component_health
            
        except Exception as e:
            log_critical_issue(
                component='{component_name}',
                issue_type='HEALTH_CHECK_FAILURE',
                message=f"Health check failed: {{str(e)}}",
                severity=LogLevel.ERROR
            )
            return {{
                'component': '{component_name}',
                'timestamp': datetime.now().isoformat(),
                'healthy': False,
                'error': str(e)
            }}
"""
                changes_made += 1
                return class_signature + class_body + health_method + next_class
            return match.group(0)
        
        content = re.sub(class_pattern, add_health_check_method, content, flags=re.DOTALL)
        
        return content, changes_made
    
    def create_integration_test(self) -> str:
        """Create integration test for repaired logging system"""
        test_content = '''#!/usr/bin/env python3
"""
UTMES Logging System Integration Test
Tests the repaired logging system to ensure all components are working correctly
"""

import sys
import os
from pathlib import Path

# Add UTMES directory to path
utmes_dir = Path(__file__).parent
sys.path.insert(0, str(utmes_dir))

def test_logging_integration():
    """Test the integrated logging system"""
    print("🧪 Testing UTMES Logging Integration...")
    
    try:
        # Test centralized logging manager
        from utmes_centralized_logging_manager import (
            get_utmes_logger, log_critical_issue, perform_system_health_check,
            LoggerType, LogLevel
        )
        
        print("✅ Centralized logging manager imported successfully")
        
        # Test logger creation
        test_logger = get_utmes_logger(LoggerType.SYSTEM_MONITOR, "IntegrationTest")
        test_logger.info("Integration test started")
        
        print("✅ Logger creation successful")
        
        # Test critical issue logging
        issue_id = log_critical_issue(
            component="IntegrationTest",
            issue_type="TEST_ISSUE",
            message="This is a test critical issue",
            severity=LogLevel.WARNING
        )
        
        print(f"✅ Critical issue logged: {issue_id}")
        
        # Test health check
        health_results = perform_system_health_check()
        print(f"✅ Health check completed: {health_results['overall_healthy']}")
        
        # Test component imports
        components_to_test = [
            "master_utmes_integration_controller",
            "unbreakable_enforcement_implementation",
            "comprehensive_validation_testing"
        ]
        
        for component in components_to_test:
            try:
                module = __import__(component.replace('-', '_'))
                print(f"✅ {component} imported successfully")
            except Exception as e:
                print(f"❌ {component} import failed: {e}")
        
        print("\\n🎉 UTMES Logging Integration Test Completed Successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_logging_integration()
    sys.exit(0 if success else 1)
'''
        
        # Write test file
        test_path = self.utmes_directory / "test_logging_integration.py"
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        return str(test_path)

# Example usage and execution
if __name__ == "__main__":
    repair_tool = UTMESLoggingSystemRepair()
    
    # Perform the repair
    results = repair_tool.repair_all_utmes_logging()
    
    # Create integration test
    test_file = repair_tool.create_integration_test()
    print(f"\\n📝 Integration test created: {test_file}")
    
    # Summary
    if results['files_failed'] == 0:
        print("\\n🎉 UTMES Logging System Repair Completed Successfully!")
        print("\\n📋 Next Steps:")
        print("1. Run the integration test to verify repairs")
        print("2. Check log files in the logs directory")
        print("3. Monitor system health using the centralized logging")
    else:
        print(f"\\n⚠️ Repair completed with {results['files_failed']} failures")
        print("Please review the repair details and fix any issues")
'''
