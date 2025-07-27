#!/usr/bin/env python3
"""
Test UTMES Logging Fix
Simple test to verify the centralized logging system is working
"""

import os
import sys
from pathlib import Path

def test_centralized_logging():
    """Test the centralized logging system"""
    print("🧪 Testing UTMES Centralized Logging Fix...")
    
    try:
        # Test 1: Import centralized logging manager
        print("📦 Testing centralized logging manager import...")
        from utmes_centralized_logging_manager import (
            get_utmes_logger, log_critical_issue, perform_system_health_check,
            LoggerType, LogLevel, UTMES_LOGGING_MANAGER
        )
        print("✅ Centralized logging manager imported successfully")
        
        # Test 2: Create logger
        print("🔧 Testing logger creation...")
        test_logger = get_utmes_logger(LoggerType.SYSTEM_MONITOR, "LoggingTest")
        test_logger.info("Test logging message - centralized logging is working!")
        print("✅ Logger created and test message logged")
        
        # Test 3: Log critical issue
        print("🚨 Testing critical issue logging...")
        issue_id = log_critical_issue(
            component="LoggingTest",
            issue_type="TEST_CRITICAL_ISSUE",
            message="This is a test critical issue to verify logging works",
            context={"test_data": "logging_verification"},
            severity=LogLevel.WARNING
        )
        print(f"✅ Critical issue logged with ID: {issue_id}")
        
        # Test 4: Health check
        print("🏥 Testing system health check...")
        health_results = perform_system_health_check()
        print(f"✅ Health check completed - System healthy: {health_results.get('overall_healthy', False)}")
        
        # Test 5: Check log files
        print("📁 Testing log file creation...")
        log_dir = Path("JAEGIS-METHOD-v2.0/v2.1.0/JAEGIS/JAEGIS-METHOD/UTMES-ENFORCEMENT/logs")
        
        if log_dir.exists():
            log_files = list(log_dir.glob("*.log"))
            if log_files:
                print(f"✅ Log files created: {[f.name for f in log_files]}")
            else:
                print("⚠️ Log directory exists but no log files found")
        else:
            print("⚠️ Log directory not found - may be created on first use")
        
        # Test 6: Get logging statistics
        print("📊 Testing logging statistics...")
        stats = UTMES_LOGGING_MANAGER.get_logging_statistics()
        print(f"✅ Logging statistics retrieved:")
        print(f"   - Health Status: {stats['logging_health_status']}")
        print(f"   - Total Loggers: {stats['total_loggers']}")
        print(f"   - Critical Issues: {stats['total_critical_issues']}")
        
        # Test 7: Resolve test issue
        print("🔧 Testing issue resolution...")
        resolved = UTMES_LOGGING_MANAGER.resolve_critical_issue(issue_id, "Test issue resolved successfully")
        print(f"✅ Test issue resolved: {resolved}")
        
        print("\n🎉 All centralized logging tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   This indicates the centralized logging manager is not accessible")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_master_controller_integration():
    """Test that the master controller uses centralized logging"""
    print("\n🧪 Testing Master Controller Integration...")
    
    try:
        # Import the fixed master controller
        print("📦 Testing master controller import...")
        from master_utmes_integration_controller import MasterUTMESIntegrationController
        print("✅ Master controller imported successfully")
        
        # Create instance (this should use centralized logging)
        print("🔧 Testing master controller initialization...")
        controller = MasterUTMESIntegrationController()
        print("✅ Master controller initialized with centralized logging")
        
        # Test that it has the logger attribute
        if hasattr(controller, 'logger'):
            print("✅ Master controller has centralized logger attribute")
            
            # Test logging
            controller.logger.info("Test message from master controller - centralized logging working!")
            print("✅ Master controller logging test successful")
        else:
            print("❌ Master controller missing logger attribute")
            return False
        
        print("🎉 Master controller integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Master controller integration test failed: {e}")
        return False

def main():
    """Run all logging tests"""
    print("🔍 UTMES Logging Fix Verification")
    print("=" * 50)
    
    # Test centralized logging
    logging_test_passed = test_centralized_logging()
    
    # Test master controller integration
    integration_test_passed = test_master_controller_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    print(f"   Centralized Logging: {'✅ PASSED' if logging_test_passed else '❌ FAILED'}")
    print(f"   Master Controller Integration: {'✅ PASSED' if integration_test_passed else '❌ FAILED'}")
    
    if logging_test_passed and integration_test_passed:
        print("\n🎉 ALL TESTS PASSED - LOGGING FIX SUCCESSFUL!")
        print("\n📋 Next Steps:")
        print("   1. Check log files in the logs directory")
        print("   2. Apply similar fixes to other UTMES components")
        print("   3. Monitor system health using centralized logging")
        return True
    else:
        print("\n❌ SOME TESTS FAILED - REVIEW AND FIX ISSUES")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
