#!/usr/bin/env python3
"""
UTMES Integrated Self-Healing System
Complete integration of automated self-healing logging with UTMES system
Provides unified interface for all UTMES components to use automated logging repair

Date: 24 July 2025 (Auto-updating daily)
Priority: CRITICAL - Complete system integration
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Import all UTMES logging components
from utmes_centralized_logging_manager import (
    UTMESCentralizedLoggingManager, get_utmes_logger, log_critical_issue,
    perform_system_health_check, LoggerType, LogLevel
)
from utmes_automated_self_healing_logging import (
    UTMESAutomatedSelfHealingLogging, start_automated_self_healing,
    stop_automated_self_healing, force_logging_system_repair,
    get_self_healing_status
)

class IntegrationStatus(Enum):
    """Status of UTMES integration"""
    INITIALIZING = "INITIALIZING"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    EMERGENCY = "EMERGENCY"

@dataclass
class UTMESSystemStatus:
    """Complete UTMES system status"""
    integration_status: IntegrationStatus
    logging_system_healthy: bool
    self_healing_active: bool
    critical_issues_count: int
    last_health_check: str
    system_uptime: str
    components_operational: Dict[str, bool]

class UTMESIntegratedSelfHealingSystem:
    """
    UTMES Integrated Self-Healing System
    Complete integration of all UTMES logging and self-healing components
    """
    
    def __init__(self):
        # Initialize core components
        self.logging_manager = UTMESCentralizedLoggingManager()
        self.self_healing_system = None
        self.logger = get_utmes_logger(LoggerType.SYSTEM_MONITOR, "IntegratedSelfHealing")
        
        # Integration state
        self.integration_status = IntegrationStatus.INITIALIZING
        self.system_start_time = datetime.now()
        self.components_status = {}
        
        # Initialize integrated system
        self._initialize_integrated_system()
    
    def initialize_complete_system(self) -> bool:
        """
        Initialize complete UTMES self-healing system
        
        Returns:
            True if initialization successful
        """
        try:
            self.logger.info("Initializing UTMES Integrated Self-Healing System...")
            
            # Step 1: Verify centralized logging is operational
            if not self._verify_centralized_logging():
                self.integration_status = IntegrationStatus.FAILED
                return False
            
            # Step 2: Initialize self-healing system
            if not self._initialize_self_healing():
                self.integration_status = IntegrationStatus.DEGRADED
                self.logger.warning("Self-healing initialization failed - continuing with degraded functionality")
            
            # Step 3: Start automated monitoring
            if not self._start_integrated_monitoring():
                self.integration_status = IntegrationStatus.DEGRADED
                self.logger.warning("Integrated monitoring failed to start")
            
            # Step 4: Perform initial system health check
            initial_health = self.perform_comprehensive_health_check()
            if not initial_health['overall_healthy']:
                self.logger.warning("Initial health check detected issues - triggering repair")
                self.trigger_immediate_repair("Initial health check issues")
            
            # Step 5: Set integration status
            if self.integration_status == IntegrationStatus.INITIALIZING:
                self.integration_status = IntegrationStatus.ACTIVE
            
            self.logger.info(f"UTMES Integrated Self-Healing System initialized - Status: {self.integration_status.value}")
            
            # Log successful initialization
            log_critical_issue(
                component="IntegratedSelfHealing",
                issue_type="SYSTEM_INITIALIZED",
                message="UTMES Integrated Self-Healing System successfully initialized",
                context={
                    'integration_status': self.integration_status.value,
                    'self_healing_active': self.self_healing_system is not None,
                    'initialization_time': datetime.now().isoformat()
                },
                severity=LogLevel.INFO
            )
            
            return True
            
        except Exception as e:
            self.integration_status = IntegrationStatus.FAILED
            self.logger.critical(f"Failed to initialize integrated system: {e}")
            
            log_critical_issue(
                component="IntegratedSelfHealing",
                issue_type="INITIALIZATION_FAILURE",
                message=f"System initialization failed: {str(e)}",
                severity=LogLevel.CRITICAL
            )
            
            return False
    
    def perform_comprehensive_health_check(self) -> Dict:
        """
        Perform comprehensive health check of entire UTMES system
        
        Returns:
            Complete health check results
        """
        health_results = {
            'timestamp': datetime.now().isoformat(),
            'overall_healthy': True,
            'integration_status': self.integration_status.value,
            'components': {},
            'issues_detected': [],
            'recommendations': [],
            'self_healing_triggered': False
        }
        
        try:
            # 1. Check centralized logging health
            logging_health = perform_system_health_check()
            health_results['components']['centralized_logging'] = logging_health
            
            if not logging_health.get('overall_healthy', True):
                health_results['overall_healthy'] = False
                health_results['issues_detected'].extend(logging_health.get('issues_detected', []))
                health_results['recommendations'].extend(logging_health.get('recommendations', []))
            
            # 2. Check self-healing system health
            if self.self_healing_system:
                self_healing_health = get_self_healing_status()
                health_results['components']['self_healing'] = self_healing_health
                
                if not self_healing_health.get('monitoring_active', False):
                    health_results['overall_healthy'] = False
                    health_results['issues_detected'].append("Self-healing monitoring not active")
                    health_results['recommendations'].append("Restart self-healing monitoring")
            else:
                health_results['components']['self_healing'] = {'status': 'NOT_AVAILABLE'}
                health_results['issues_detected'].append("Self-healing system not available")
            
            # 3. Check integration status
            if self.integration_status in [IntegrationStatus.FAILED, IntegrationStatus.EMERGENCY]:
                health_results['overall_healthy'] = False
                health_results['issues_detected'].append(f"Integration status: {self.integration_status.value}")
                health_results['recommendations'].append("Investigate integration failures")
            
            # 4. Trigger self-healing if issues detected
            if not health_results['overall_healthy'] and self.self_healing_system:
                try:
                    repair_result = self.trigger_immediate_repair("Comprehensive health check detected issues")
                    health_results['self_healing_triggered'] = repair_result.success
                    health_results['repair_id'] = repair_result.repair_id
                except Exception as e:
                    health_results['issues_detected'].append(f"Self-healing trigger failed: {str(e)}")
            
            # Log health check results
            if health_results['overall_healthy']:
                self.logger.info(f"Comprehensive health check: HEALTHY")
            else:
                self.logger.warning(f"Comprehensive health check: ISSUES DETECTED - {len(health_results['issues_detected'])} issues")
            
            return health_results
            
        except Exception as e:
            error_health = {
                'timestamp': datetime.now().isoformat(),
                'overall_healthy': False,
                'integration_status': IntegrationStatus.FAILED.value,
                'components': {},
                'issues_detected': [f"Health check failed: {str(e)}"],
                'recommendations': ["Investigate health check system failure"],
                'self_healing_triggered': False
            }
            
            self.logger.critical(f"Comprehensive health check failed: {e}")
            return error_health
    
    def trigger_immediate_repair(self, reason: str) -> Any:
        """
        Trigger immediate system repair
        
        Args:
            reason: Reason for triggering repair
            
        Returns:
            Repair result
        """
        try:
            self.logger.info(f"Triggering immediate repair: {reason}")
            
            if self.self_healing_system:
                repair_result = force_logging_system_repair(reason)
                
                if repair_result.success:
                    self.logger.info(f"Immediate repair successful: {repair_result.repair_id}")
                else:
                    self.logger.error(f"Immediate repair failed: {repair_result.error_message}")
                
                return repair_result
            else:
                self.logger.warning("Self-healing system not available - cannot perform repair")
                return None
                
        except Exception as e:
            self.logger.critical(f"Failed to trigger immediate repair: {e}")
            
            log_critical_issue(
                component="IntegratedSelfHealing",
                issue_type="REPAIR_TRIGGER_FAILURE",
                message=f"Failed to trigger repair: {str(e)}",
                context={'reason': reason},
                severity=LogLevel.CRITICAL
            )
            
            return None
    
    def get_complete_system_status(self) -> UTMESSystemStatus:
        """Get complete UTMES system status"""
        try:
            # Get health check results
            health_results = self.perform_comprehensive_health_check()
            
            # Get critical issues count
            critical_issues = self.logging_manager.get_critical_issues(unresolved_only=True)
            
            # Calculate uptime
            uptime = datetime.now() - self.system_start_time
            uptime_str = f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
            
            # Determine component operational status
            components_operational = {
                'centralized_logging': health_results['components'].get('centralized_logging', {}).get('overall_healthy', False),
                'self_healing': health_results['components'].get('self_healing', {}).get('monitoring_active', False),
                'integration': self.integration_status == IntegrationStatus.ACTIVE
            }
            
            return UTMESSystemStatus(
                integration_status=self.integration_status,
                logging_system_healthy=health_results['overall_healthy'],
                self_healing_active=self.self_healing_system is not None,
                critical_issues_count=len(critical_issues),
                last_health_check=health_results['timestamp'],
                system_uptime=uptime_str,
                components_operational=components_operational
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            
            return UTMESSystemStatus(
                integration_status=IntegrationStatus.FAILED,
                logging_system_healthy=False,
                self_healing_active=False,
                critical_issues_count=0,
                last_health_check=datetime.now().isoformat(),
                system_uptime="UNKNOWN",
                components_operational={'error': str(e)}
            )
    
    def _verify_centralized_logging(self) -> bool:
        """Verify centralized logging is operational"""
        try:
            # Test logger creation
            test_logger = get_utmes_logger(LoggerType.SYSTEM_MONITOR, "VerificationTest")
            test_logger.info("Centralized logging verification test")
            
            # Test critical issue logging
            issue_id = log_critical_issue(
                component="VerificationTest",
                issue_type="VERIFICATION_TEST",
                message="Testing centralized logging functionality",
                severity=LogLevel.INFO
            )
            
            # Test health check
            health_results = perform_system_health_check()
            
            # Resolve test issue
            self.logging_manager.resolve_critical_issue(issue_id, "Verification test completed")
            
            return health_results.get('overall_healthy', False)
            
        except Exception as e:
            self.logger.error(f"Centralized logging verification failed: {e}")
            return False
    
    def _initialize_self_healing(self) -> bool:
        """Initialize self-healing system"""
        try:
            # Start automated self-healing
            success = start_automated_self_healing()
            
            if success:
                # Get reference to self-healing system
                from utmes_automated_self_healing_logging import UTMES_SELF_HEALING_LOGGING
                self.self_healing_system = UTMES_SELF_HEALING_LOGGING
                
                self.logger.info("Self-healing system initialized successfully")
                return True
            else:
                self.logger.warning("Self-healing system initialization failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Self-healing initialization error: {e}")
            return False
    
    def _start_integrated_monitoring(self) -> bool:
        """Start integrated monitoring"""
        try:
            # Monitoring is handled by the self-healing system
            if self.self_healing_system:
                status = get_self_healing_status()
                return status.get('monitoring_active', False)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Integrated monitoring start failed: {e}")
            return False
    
    def _initialize_integrated_system(self) -> None:
        """Initialize integrated system"""
        self.logger.info("UTMES Integrated Self-Healing System starting initialization...")
        
        # Set initial component status
        self.components_status = {
            'centralized_logging': 'INITIALIZING',
            'self_healing': 'INITIALIZING',
            'integration': 'INITIALIZING'
        }
    
    def shutdown_system(self) -> bool:
        """Shutdown integrated system gracefully"""
        try:
            self.logger.info("Shutting down UTMES Integrated Self-Healing System...")
            
            # Stop self-healing monitoring
            if self.self_healing_system:
                stop_success = stop_automated_self_healing()
                if stop_success:
                    self.logger.info("Self-healing monitoring stopped")
                else:
                    self.logger.warning("Failed to stop self-healing monitoring")
            
            # Update integration status
            self.integration_status = IntegrationStatus.FAILED
            
            self.logger.info("UTMES Integrated Self-Healing System shutdown completed")
            return True
            
        except Exception as e:
            self.logger.critical(f"System shutdown failed: {e}")
            return False

# Global integrated system instance
UTMES_INTEGRATED_SYSTEM = UTMESIntegratedSelfHealingSystem()

# Convenience functions for UTMES components
def initialize_utmes_logging_system() -> bool:
    """Initialize complete UTMES logging system"""
    return UTMES_INTEGRATED_SYSTEM.initialize_complete_system()

def get_utmes_system_status() -> UTMESSystemStatus:
    """Get complete UTMES system status"""
    return UTMES_INTEGRATED_SYSTEM.get_complete_system_status()

def perform_utmes_health_check() -> Dict:
    """Perform comprehensive UTMES health check"""
    return UTMES_INTEGRATED_SYSTEM.perform_comprehensive_health_check()

def trigger_utmes_repair(reason: str = "Manual trigger") -> Any:
    """Trigger UTMES system repair"""
    return UTMES_INTEGRATED_SYSTEM.trigger_immediate_repair(reason)

def shutdown_utmes_logging() -> bool:
    """Shutdown UTMES logging system"""
    return UTMES_INTEGRATED_SYSTEM.shutdown_system()

# Example usage and testing
if __name__ == "__main__":
    print("🔧 Testing UTMES Integrated Self-Healing System...")
    
    # Initialize complete system
    print("🚀 Initializing complete UTMES system...")
    if initialize_utmes_logging_system():
        print("✅ UTMES system initialized successfully")
        
        # Get system status
        status = get_utmes_system_status()
        print(f"📊 System Status: {status.integration_status.value}")
        print(f"   Logging Healthy: {status.logging_system_healthy}")
        print(f"   Self-Healing Active: {status.self_healing_active}")
        print(f"   Critical Issues: {status.critical_issues_count}")
        print(f"   System Uptime: {status.system_uptime}")
        
        # Perform health check
        print("🏥 Performing comprehensive health check...")
        health_results = perform_utmes_health_check()
        print(f"   Overall Healthy: {health_results['overall_healthy']}")
        print(f"   Issues Detected: {len(health_results['issues_detected'])}")
        
        # Test repair trigger
        print("🔧 Testing repair trigger...")
        repair_result = trigger_utmes_repair("Integration test")
        if repair_result:
            print(f"   Repair Success: {repair_result.success}")
        
        print("✅ UTMES Integrated Self-Healing System test completed")
        
    else:
        print("❌ UTMES system initialization failed")
    
    print("🎉 Testing completed")
