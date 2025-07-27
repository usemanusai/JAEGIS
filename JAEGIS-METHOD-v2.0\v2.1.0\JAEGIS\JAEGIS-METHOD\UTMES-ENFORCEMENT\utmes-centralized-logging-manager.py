#!/usr/bin/env python3
"""
UTMES Centralized Logging Manager
Fixes critical logging issues in UTMES system with centralized logging, persistent files, and enhanced detection
Addresses the detection/logging gap where critical issues are not being detected or logged

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - System logging and monitoring repair
"""

import os
import sys
import json
import logging
import logging.handlers
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

class LogLevel(Enum):
    """Enhanced log levels for UTMES"""
    CRITICAL_SYSTEM = 60  # Above CRITICAL for system-breaking issues
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10

class LoggerType(Enum):
    """Types of UTMES loggers"""
    MASTER_CONTROLLER = "MASTER_CONTROLLER"
    ENFORCEMENT_HOOKS = "ENFORCEMENT_HOOKS"
    FLOW_OVERRIDE = "FLOW_OVERRIDE"
    RESPONSE_INTEGRATION = "RESPONSE_INTEGRATION"
    UNBREAKABLE_ENFORCEMENT = "UNBREAKABLE_ENFORCEMENT"
    VALIDATION_TESTING = "VALIDATION_TESTING"
    SYSTEM_MONITOR = "SYSTEM_MONITOR"

@dataclass
class LoggingConfiguration:
    """Configuration for UTMES logging system"""
    log_directory: str
    max_file_size_mb: int
    backup_count: int
    console_logging: bool
    file_logging: bool
    log_level: LogLevel
    enable_critical_detection: bool
    enable_health_monitoring: bool

@dataclass
class CriticalIssue:
    """Represents a detected critical issue"""
    issue_id: str
    issue_type: str
    severity: LogLevel
    component: str
    message: str
    timestamp: str
    context: Dict
    resolved: bool

class UTMESCentralizedLoggingManager:
    """
    UTMES Centralized Logging Manager
    Fixes critical logging issues and provides comprehensive system monitoring
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure only one logging manager"""
        if cls._instance is None:
            cls._instance = super(UTMESCentralizedLoggingManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize centralized logging manager"""
        if not self._initialized:
            # Logging configuration
            self.config = LoggingConfiguration(
                log_directory="JAEGIS-METHOD-v2.0/v2.1.0/JAEGIS/JAEGIS-METHOD/UTMES-ENFORCEMENT/logs",
                max_file_size_mb=50,
                backup_count=10,
                console_logging=True,
                file_logging=True,
                log_level=LogLevel.INFO,
                enable_critical_detection=True,
                enable_health_monitoring=True
            )

            # System state
            self.loggers: Dict[str, logging.Logger] = {}
            self.critical_issues: List[CriticalIssue] = []
            self.logging_health_status = "UNKNOWN"
            self.last_health_check = None

            # Self-healing integration
            self.self_healing_enabled = True
            self.self_healing_system = None

            # Initialize logging system
            self._initialize_logging_system()

            # Initialize self-healing system (delayed to avoid circular imports)
            self._initialize_self_healing_integration()

            UTMESCentralizedLoggingManager._initialized = True
    
    def get_logger(self, logger_type: LoggerType, component_name: str = None) -> logging.Logger:
        """
        Get or create a logger for a specific UTMES component
        
        Args:
            logger_type: Type of logger needed
            component_name: Optional specific component name
            
        Returns:
            Configured logger instance
        """
        logger_name = f"UTMES.{logger_type.value}"
        if component_name:
            logger_name += f".{component_name}"
        
        if logger_name not in self.loggers:
            self.loggers[logger_name] = self._create_component_logger(logger_name, logger_type)
        
        return self.loggers[logger_name]
    
    def log_critical_issue(self, component: str, issue_type: str, message: str, 
                          context: Dict = None, severity: LogLevel = LogLevel.CRITICAL) -> str:
        """
        Log a critical issue with enhanced detection and tracking
        
        Args:
            component: Component where issue occurred
            issue_type: Type of critical issue
            message: Issue description
            context: Additional context data
            severity: Issue severity level
            
        Returns:
            Issue ID for tracking
        """
        issue_id = self._generate_issue_id()
        
        critical_issue = CriticalIssue(
            issue_id=issue_id,
            issue_type=issue_type,
            severity=severity,
            component=component,
            message=message,
            timestamp=datetime.now().isoformat(),
            context=context or {},
            resolved=False
        )
        
        # Store critical issue
        self.critical_issues.append(critical_issue)
        
        # Log to appropriate logger
        logger = self.get_logger(LoggerType.SYSTEM_MONITOR, component)
        
        # Enhanced logging with context
        log_data = {
            'issue_id': issue_id,
            'issue_type': issue_type,
            'component': component,
            'severity': severity.name,
            'message': message,
            'context': context or {},
            'timestamp': critical_issue.timestamp
        }
        
        if severity == LogLevel.CRITICAL_SYSTEM:
            logger.log(LogLevel.CRITICAL_SYSTEM.value, f"CRITICAL SYSTEM ISSUE: {json.dumps(log_data)}")
        elif severity == LogLevel.CRITICAL:
            logger.critical(f"CRITICAL ISSUE: {json.dumps(log_data)}")
        elif severity == LogLevel.ERROR:
            logger.error(f"ERROR ISSUE: {json.dumps(log_data)}")
        else:
            logger.warning(f"WARNING ISSUE: {json.dumps(log_data)}")
        
        # Trigger immediate health check
        self._perform_logging_health_check()
        
        return issue_id
    
    def resolve_critical_issue(self, issue_id: str, resolution_notes: str = "") -> bool:
        """
        Mark a critical issue as resolved
        
        Args:
            issue_id: ID of issue to resolve
            resolution_notes: Optional resolution notes
            
        Returns:
            True if issue was found and resolved
        """
        for issue in self.critical_issues:
            if issue.issue_id == issue_id:
                issue.resolved = True
                issue.context['resolution_notes'] = resolution_notes
                issue.context['resolved_timestamp'] = datetime.now().isoformat()
                
                logger = self.get_logger(LoggerType.SYSTEM_MONITOR)
                logger.info(f"ISSUE RESOLVED: {issue_id} - {resolution_notes}")
                return True
        
        return False
    
    def get_critical_issues(self, unresolved_only: bool = True) -> List[CriticalIssue]:
        """Get list of critical issues"""
        if unresolved_only:
            return [issue for issue in self.critical_issues if not issue.resolved]
        return self.critical_issues.copy()
    
    def perform_system_health_check(self) -> Dict:
        """
        Perform comprehensive system health check

        Returns:
            Health check results
        """
        health_results = {
            'timestamp': datetime.now().isoformat(),
            'logging_system_healthy': True,
            'issues_detected': [],
            'recommendations': []
        }

        try:
            # Check logging system health
            logging_health = self._perform_logging_health_check()
            health_results['logging_system_healthy'] = logging_health['healthy']

            if not logging_health['healthy']:
                health_results['issues_detected'].extend(logging_health['issues'])
                health_results['recommendations'].extend(logging_health['recommendations'])

            # Check for unresolved critical issues
            unresolved_issues = self.get_critical_issues(unresolved_only=True)
            if unresolved_issues:
                health_results['issues_detected'].append(f"{len(unresolved_issues)} unresolved critical issues")
                health_results['recommendations'].append("Review and resolve critical issues")

            # Check log file accessibility
            log_file_check = self._check_log_file_accessibility()
            if not log_file_check['accessible']:
                health_results['issues_detected'].append("Log files not accessible")
                health_results['recommendations'].append("Check log directory permissions")

            # Overall health determination
            health_results['overall_healthy'] = (
                health_results['logging_system_healthy'] and
                len(unresolved_issues) == 0 and
                log_file_check['accessible']
            )

            # Trigger self-healing if issues detected and self-healing is enabled
            if not health_results['overall_healthy'] and self.self_healing_enabled and self.self_healing_system:
                try:
                    self._trigger_self_healing("Health check detected issues", health_results)
                except Exception as healing_error:
                    health_results['issues_detected'].append(f"Self-healing trigger failed: {str(healing_error)}")

            # Log health check results
            logger = self.get_logger(LoggerType.SYSTEM_MONITOR)
            if health_results['overall_healthy']:
                logger.info(f"SYSTEM HEALTH CHECK: HEALTHY - {json.dumps(health_results)}")
            else:
                logger.warning(f"SYSTEM HEALTH CHECK: ISSUES DETECTED - {json.dumps(health_results)}")

            return health_results

        except Exception as e:
            error_result = {
                'timestamp': datetime.now().isoformat(),
                'logging_system_healthy': False,
                'overall_healthy': False,
                'issues_detected': [f"Health check failed: {str(e)}"],
                'recommendations': ["Investigate health check system failure"]
            }

            # Try to log error (may fail if logging is broken)
            try:
                logger = self.get_logger(LoggerType.SYSTEM_MONITOR)
                logger.critical(f"HEALTH CHECK FAILURE: {json.dumps(error_result)}")
            except:
                # Fallback to console if logging completely fails
                print(f"CRITICAL: Health check and logging both failed - {str(e)}")

            # Trigger emergency self-healing
            if self.self_healing_enabled and self.self_healing_system:
                try:
                    self._trigger_self_healing("Critical health check failure", error_result)
                except:
                    pass  # Self-healing also failed

            return error_result
    
    def _initialize_logging_system(self) -> None:
        """Initialize the centralized logging system"""
        try:
            # Create log directory
            log_dir = Path(self.config.log_directory)
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Clear any existing logging configuration
            logging.getLogger().handlers.clear()
            
            # Set up root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(self.config.log_level.value)
            
            # Create formatters
            detailed_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            
            # Set up file logging
            if self.config.file_logging:
                file_handler = logging.handlers.RotatingFileHandler(
                    filename=log_dir / "utmes_system.log",
                    maxBytes=self.config.max_file_size_mb * 1024 * 1024,
                    backupCount=self.config.backup_count
                )
                file_handler.setFormatter(detailed_formatter)
                file_handler.setLevel(self.config.log_level.value)
                root_logger.addHandler(file_handler)
                
                # Separate critical issues log
                critical_handler = logging.handlers.RotatingFileHandler(
                    filename=log_dir / "utmes_critical.log",
                    maxBytes=self.config.max_file_size_mb * 1024 * 1024,
                    backupCount=self.config.backup_count
                )
                critical_handler.setFormatter(detailed_formatter)
                critical_handler.setLevel(LogLevel.WARNING.value)
                root_logger.addHandler(critical_handler)
            
            # Set up console logging
            if self.config.console_logging:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(console_formatter)
                console_handler.setLevel(self.config.log_level.value)
                root_logger.addHandler(console_handler)
            
            # Add custom log level for critical system issues
            logging.addLevelName(LogLevel.CRITICAL_SYSTEM.value, "CRITICAL_SYSTEM")
            
            self.logging_health_status = "HEALTHY"
            
            # Log successful initialization
            init_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "LoggingManager")
            init_logger.info("UTMES Centralized Logging Manager initialized successfully")
            
        except Exception as e:
            self.logging_health_status = "FAILED"
            # Fallback to console logging
            print(f"CRITICAL: Failed to initialize UTMES logging system - {str(e)}")
            raise
    
    def _create_component_logger(self, logger_name: str, logger_type: LoggerType) -> logging.Logger:
        """Create a logger for a specific component"""
        logger = logging.getLogger(logger_name)
        
        # Don't add handlers to component loggers - they inherit from root
        # This prevents duplicate log messages
        logger.propagate = True
        
        return logger
    
    def _perform_logging_health_check(self) -> Dict:
        """Perform logging system health check"""
        health_check = {
            'healthy': True,
            'issues': [],
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Check if log directory exists and is writable
            log_dir = Path(self.config.log_directory)
            if not log_dir.exists():
                health_check['healthy'] = False
                health_check['issues'].append("Log directory does not exist")
                health_check['recommendations'].append("Create log directory")
            elif not os.access(log_dir, os.W_OK):
                health_check['healthy'] = False
                health_check['issues'].append("Log directory not writable")
                health_check['recommendations'].append("Fix log directory permissions")
            
            # Check if loggers are working
            test_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "HealthCheck")
            test_logger.debug("Logging health check test message")
            
            # Check for excessive critical issues
            unresolved_critical = len([i for i in self.critical_issues if not i.resolved and i.severity in [LogLevel.CRITICAL, LogLevel.CRITICAL_SYSTEM]])
            if unresolved_critical > 5:
                health_check['healthy'] = False
                health_check['issues'].append(f"Too many unresolved critical issues: {unresolved_critical}")
                health_check['recommendations'].append("Investigate and resolve critical issues")
            
            self.logging_health_status = "HEALTHY" if health_check['healthy'] else "DEGRADED"
            self.last_health_check = datetime.now().isoformat()
            
        except Exception as e:
            health_check['healthy'] = False
            health_check['issues'].append(f"Health check failed: {str(e)}")
            health_check['recommendations'].append("Investigate logging system failure")
            self.logging_health_status = "FAILED"
        
        return health_check
    
    def _check_log_file_accessibility(self) -> Dict:
        """Check if log files are accessible"""
        try:
            log_dir = Path(self.config.log_directory)
            main_log = log_dir / "utmes_system.log"
            critical_log = log_dir / "utmes_critical.log"
            
            accessible = True
            issues = []
            
            if main_log.exists() and not os.access(main_log, os.R_OK):
                accessible = False
                issues.append("Main log file not readable")
            
            if critical_log.exists() and not os.access(critical_log, os.R_OK):
                accessible = False
                issues.append("Critical log file not readable")
            
            return {
                'accessible': accessible,
                'issues': issues,
                'main_log_exists': main_log.exists(),
                'critical_log_exists': critical_log.exists()
            }
            
        except Exception as e:
            return {
                'accessible': False,
                'issues': [f"Log file check failed: {str(e)}"],
                'main_log_exists': False,
                'critical_log_exists': False
            }
    
    def _generate_issue_id(self) -> str:
        """Generate unique issue ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"UTMES_ISSUE_{timestamp}"
    
    def get_logging_statistics(self) -> Dict:
        """Get logging system statistics"""
        return {
            'logging_health_status': self.logging_health_status,
            'last_health_check': self.last_health_check,
            'total_loggers': len(self.loggers),
            'total_critical_issues': len(self.critical_issues),
            'unresolved_critical_issues': len([i for i in self.critical_issues if not i.resolved]),
            'log_directory': self.config.log_directory,
            'file_logging_enabled': self.config.file_logging,
            'console_logging_enabled': self.config.console_logging,
            'current_log_level': self.config.log_level.name
        }

    def _initialize_self_healing_integration(self) -> None:
        """Initialize self-healing system integration"""
        if not self.self_healing_enabled:
            return

        try:
            # Delayed import to avoid circular dependencies
            from utmes_automated_self_healing_logging import UTMESAutomatedSelfHealingLogging

            # Initialize self-healing system
            self.self_healing_system = UTMESAutomatedSelfHealingLogging(monitoring_interval_seconds=300)

            # Start automated monitoring
            if self.self_healing_system.start_automated_monitoring():
                init_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "SelfHealingIntegration")
                init_logger.info("Self-healing system integrated and monitoring started")
            else:
                init_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "SelfHealingIntegration")
                init_logger.warning("Self-healing system integration failed")

        except ImportError:
            # Self-healing system not available
            init_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "SelfHealingIntegration")
            init_logger.warning("Self-healing system not available - continuing without automated repair")
            self.self_healing_enabled = False
        except Exception as e:
            init_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "SelfHealingIntegration")
            init_logger.error(f"Self-healing system initialization failed: {e}")
            self.self_healing_enabled = False

    def _trigger_self_healing(self, reason: str, context: Dict) -> None:
        """Trigger self-healing system"""
        if not self.self_healing_enabled or not self.self_healing_system:
            return

        try:
            # Log the trigger
            trigger_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "SelfHealingTrigger")
            trigger_logger.warning(f"Triggering self-healing: {reason}")

            # Force system repair
            repair_result = self.self_healing_system.force_system_repair(reason)

            if repair_result.success:
                trigger_logger.info(f"Self-healing repair successful: {repair_result.repair_id}")
            else:
                trigger_logger.error(f"Self-healing repair failed: {repair_result.error_message}")

        except Exception as e:
            trigger_logger = self.get_logger(LoggerType.SYSTEM_MONITOR, "SelfHealingTrigger")
            trigger_logger.critical(f"Self-healing trigger failed: {e}")

    def get_self_healing_status(self) -> Dict:
        """Get self-healing system status"""
        if not self.self_healing_enabled or not self.self_healing_system:
            return {
                'self_healing_enabled': False,
                'monitoring_active': False,
                'status': 'DISABLED'
            }

        try:
            stats = self.self_healing_system.get_self_healing_statistics()
            stats['self_healing_enabled'] = self.self_healing_enabled
            stats['status'] = 'ACTIVE' if stats.get('monitoring_active', False) else 'INACTIVE'
            return stats
        except Exception as e:
            return {
                'self_healing_enabled': self.self_healing_enabled,
                'monitoring_active': False,
                'status': 'ERROR',
                'error': str(e)
            }

# Global instance for easy access
UTMES_LOGGING_MANAGER = UTMESCentralizedLoggingManager()

# Convenience functions for easy use
def get_utmes_logger(logger_type: LoggerType, component_name: str = None) -> logging.Logger:
    """Get UTMES logger - convenience function"""
    return UTMES_LOGGING_MANAGER.get_logger(logger_type, component_name)

def log_critical_issue(component: str, issue_type: str, message: str, 
                      context: Dict = None, severity: LogLevel = LogLevel.CRITICAL) -> str:
    """Log critical issue - convenience function"""
    return UTMES_LOGGING_MANAGER.log_critical_issue(component, issue_type, message, context, severity)

def perform_system_health_check() -> Dict:
    """Perform system health check - convenience function"""
    return UTMES_LOGGING_MANAGER.perform_system_health_check()

# Example usage and testing
if __name__ == "__main__":
    # Test the logging system
    print("🔍 Testing UTMES Centralized Logging Manager...")
    
    # Get different types of loggers
    master_logger = get_utmes_logger(LoggerType.MASTER_CONTROLLER)
    enforcement_logger = get_utmes_logger(LoggerType.UNBREAKABLE_ENFORCEMENT)
    
    # Test logging at different levels
    master_logger.info("Master controller test message")
    enforcement_logger.warning("Enforcement system test warning")
    
    # Test critical issue logging
    issue_id = log_critical_issue(
        component="TestComponent",
        issue_type="SYSTEM_TEST",
        message="This is a test critical issue",
        context={"test_data": "example"},
        severity=LogLevel.CRITICAL
    )
    
    print(f"Created test critical issue: {issue_id}")
    
    # Perform health check
    health_results = perform_system_health_check()
    print(f"Health check results: {health_results}")
    
    # Get statistics
    stats = UTMES_LOGGING_MANAGER.get_logging_statistics()
    print(f"Logging statistics: {stats}")
    
    # Resolve test issue
    UTMES_LOGGING_MANAGER.resolve_critical_issue(issue_id, "Test issue resolved")
    
    print("✅ UTMES Centralized Logging Manager test completed")
