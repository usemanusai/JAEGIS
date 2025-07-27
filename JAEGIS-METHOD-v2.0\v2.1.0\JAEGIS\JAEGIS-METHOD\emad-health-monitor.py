#!/usr/bin/env python3

"""
eJAEGIS Health Monitoring System

Comprehensive health monitoring and verification system for eJAEGIS installations.
Provides real-time status monitoring, automated troubleshooting, and system validation.
"""

import sys
import os
import json
import time
import psutil
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

class eJAEGISHealthCheck:
    """Individual health check implementation"""
    
    def __init__(self, name: str, description: str, critical: bool = False):
        self.name = name
        self.description = description
        self.critical = critical
        self.last_result = None
        self.last_run = None
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Run the health check. Returns (success, message, details)"""
        raise NotImplementedError
    
    def get_resolution_steps(self) -> List[str]:
        """Get resolution steps for when this check fails"""
        return ["Check the eJAEGIS documentation for troubleshooting steps"]

class PythonEnvironmentCheck(eJAEGISHealthCheck):
    """Check Python environment and dependencies"""
    
    def __init__(self):
        super().__init__(
            "Python Environment",
            "Verify Python version and required dependencies",
            critical=True
        )
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        # Check Python version
        python_version = sys.version_info
        details["python_version"] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
        
        if python_version < (3, 7):
            return False, f"Python 3.7+ required, found {details['python_version']}", details
        
        # Check required packages
        required_packages = ["requests", "psutil"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                details[f"{package}_available"] = True
            except ImportError:
                missing_packages.append(package)
                details[f"{package}_available"] = False
        
        if missing_packages:
            return False, f"Missing packages: {', '.join(missing_packages)}", details
        
        return True, f"Python {details['python_version']} with all dependencies", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Install Python 3.7 or higher from https://python.org",
            "Install missing packages: pip install requests psutil",
            "Verify installation: python -c 'import requests, psutil'"
        ]

class GitHubConnectivityCheck(eJAEGISHealthCheck):
    """Check GitHub API connectivity and authentication"""
    
    def __init__(self, github_token: str = None):
        super().__init__(
            "GitHub Connectivity",
            "Verify GitHub API access and authentication",
            critical=True
        )
        self.github_token = github_token
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        if not self.github_token:
            return False, "No GitHub token configured", details
        
        try:
            headers = {"Authorization": f"Bearer {self.github_token}"}
            response = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            
            details["status_code"] = response.status_code
            details["rate_limit_remaining"] = response.headers.get("X-RateLimit-Remaining")
            
            if response.status_code == 200:
                user_data = response.json()
                details["username"] = user_data.get("login")
                details["user_type"] = user_data.get("type")
                return True, f"Connected as {details['username']}", details
            elif response.status_code == 401:
                return False, "Invalid GitHub token", details
            else:
                return False, f"GitHub API error: {response.status_code}", details
                
        except requests.RequestException as e:
            details["error"] = str(e)
            return False, f"Network error: {e}", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Create a GitHub Personal Access Token at https://github.com/settings/tokens",
            "Ensure token has 'repo' and 'workflow' scopes",
            "Update eJAEGIS configuration with the new token",
            "Test connectivity: eJAEGIS test"
        ]

class eJAEGISProcessCheck(eJAEGISHealthCheck):
    """Check if eJAEGIS background processes are running"""
    
    def __init__(self):
        super().__init__(
            "eJAEGIS Processes",
            "Verify eJAEGIS background runner and failsafe processes",
            critical=False
        )
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        # Check for eJAEGIS background runner
        eJAEGIS_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any('eJAEGIS-background-runner.py' in arg for arg in cmdline):
                    eJAEGIS_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': ' '.join(cmdline)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        details["eJAEGIS_processes"] = eJAEGIS_processes
        details["process_count"] = len(eJAEGIS_processes)
        
        if eJAEGIS_processes:
            return True, f"Found {len(eJAEGIS_processes)} eJAEGIS process(es)", details
        else:
            return False, "No eJAEGIS processes running", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Start eJAEGIS background runner: eJAEGIS start",
            "Check for errors: eJAEGIS status",
            "Review logs in the logs/ directory",
            "Restart if needed: eJAEGIS restart"
        ]

class FileSystemCheck(eJAEGISHealthCheck):
    """Check file system permissions and directory structure"""
    
    def __init__(self, eJAEGIS_dir: Path):
        super().__init__(
            "File System",
            "Verify eJAEGIS directory structure and permissions",
            critical=True
        )
        self.eJAEGIS_dir = eJAEGIS_dir
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        # Check eJAEGIS directory exists
        details["eJAEGIS_dir_exists"] = self.eJAEGIS_dir.exists()
        if not details["eJAEGIS_dir_exists"]:
            return False, f"eJAEGIS directory not found: {self.eJAEGIS_dir}", details
        
        # Check permissions
        details["can_read"] = os.access(self.eJAEGIS_dir, os.R_OK)
        details["can_write"] = os.access(self.eJAEGIS_dir, os.W_OK)
        
        if not details["can_read"] or not details["can_write"]:
            return False, "Insufficient permissions on eJAEGIS directory", details
        
        # Check required files
        required_files = [
            "eJAEGIS-auto-sync.py",
            "eJAEGIS-background-runner.py",
            "eJAEGIS-failsafe-system.py",
            "eJAEGIS-cli.py"
        ]
        
        missing_files = []
        for file_name in required_files:
            file_path = self.eJAEGIS_dir / file_name
            if file_path.exists():
                details[f"{file_name}_exists"] = True
            else:
                missing_files.append(file_name)
                details[f"{file_name}_exists"] = False
        
        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}", details
        
        # Check logs directory
        logs_dir = self.eJAEGIS_dir / "logs"
        if not logs_dir.exists():
            try:
                logs_dir.mkdir(exist_ok=True)
                details["logs_dir_created"] = True
            except Exception as e:
                details["logs_dir_error"] = str(e)
                return False, f"Cannot create logs directory: {e}", details
        
        details["logs_dir_exists"] = True
        
        return True, "File system structure is valid", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Reinstall eJAEGIS using the universal installer",
            "Check file permissions: ls -la ~/.eJAEGIS",
            "Ensure you have write access to the eJAEGIS directory",
            "Run: eJAEGIS init to reinitialize if needed"
        ]

class ConfigurationCheck(eJAEGISHealthCheck):
    """Check eJAEGIS configuration files"""
    
    def __init__(self, eJAEGIS_dir: Path):
        super().__init__(
            "Configuration",
            "Verify eJAEGIS configuration files are valid",
            critical=False
        )
        self.eJAEGIS_dir = eJAEGIS_dir
    
    def run(self) -> Tuple[bool, str, Dict[str, Any]]:
        details = {}
        
        config_dir = self.eJAEGIS_dir / "config"
        details["config_dir_exists"] = config_dir.exists()
        
        if not details["config_dir_exists"]:
            return False, "Configuration directory not found", details
        
        # Check user configuration
        user_config_path = config_dir / "eJAEGIS-user-config.json"
        details["user_config_exists"] = user_config_path.exists()
        
        if details["user_config_exists"]:
            try:
                with open(user_config_path, 'r') as f:
                    user_config = json.load(f)
                details["user_config_valid"] = True
                details["github_token_configured"] = bool(user_config.get("github", {}).get("token"))
            except json.JSONDecodeError:
                details["user_config_valid"] = False
                return False, "Invalid user configuration JSON", details
        
        # Check project configuration
        project_config_path = config_dir / "eJAEGIS-project-config.json"
        details["project_config_exists"] = project_config_path.exists()
        
        if details["project_config_exists"]:
            try:
                with open(project_config_path, 'r') as f:
                    json.load(f)
                details["project_config_valid"] = True
            except json.JSONDecodeError:
                details["project_config_valid"] = False
                return False, "Invalid project configuration JSON", details
        
        config_score = sum([
            details.get("user_config_exists", False),
            details.get("user_config_valid", False),
            details.get("project_config_exists", False),
            details.get("project_config_valid", False),
            details.get("github_token_configured", False)
        ])
        
        if config_score >= 3:
            return True, f"Configuration is valid ({config_score}/5 checks passed)", details
        else:
            return False, f"Configuration issues ({config_score}/5 checks passed)", details
    
    def get_resolution_steps(self) -> List[str]:
        return [
            "Run: eJAEGIS config --edit to update configuration",
            "Ensure GitHub token is properly set",
            "Validate JSON syntax in configuration files",
            "Reinitialize if needed: eJAEGIS init"
        ]

class eJAEGISHealthMonitor:
    """Main health monitoring system"""
    
    def __init__(self, eJAEGIS_dir: Path):
        self.eJAEGIS_dir = eJAEGIS_dir
        self.checks = []
        self.last_run = None
        self.setup_checks()
    
    def setup_checks(self):
        """Initialize all health checks"""
        self.checks = [
            PythonEnvironmentCheck(),
            FileSystemCheck(self.eJAEGIS_dir),
            ConfigurationCheck(self.eJAEGIS_dir),
            eJAEGISProcessCheck()
        ]
        
        # Add GitHub check if token is available
        try:
            config_path = self.eJAEGIS_dir / "config" / "eJAEGIS-user-config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    github_token = config.get("github", {}).get("token")
                    if github_token:
                        self.checks.append(GitHubConnectivityCheck(github_token))
        except Exception:
            pass
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {
            "timestampdatetime_now_isoformat_checks": {},
            "summary": {
                "total": len(self.checks),
                "passed": 0,
                "failed": 0,
                "critical_failed": 0
            }
        }
        
        for check in self.checks:
            try:
                success, message, details = check.run()
                
                results["checks"][check.name] = {
                    "success": success,
                    "message": message,
                    "details": details,
                    "critical": check.critical,
                    "resolution_steps": check.get_resolution_steps() if not success else []
                }
                
                if success:
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1
                    if check.critical:
                        results["summary"]["critical_failed"] += 1
                
                check.last_result = success
                check.last_run = datetime.now()
                
            except Exception as e:
                results["checks"][check.name] = {
                    "success": False,
                    "message": f"Check_failed_with_error_e_details": {"error": str(e)},
                    "critical": check.critical,
                    "resolution_steps": ["Contact support with error details"]
                }
                results["summary"]["failed"] += 1
                if check.critical:
                    results["summary"]["critical_failed"] += 1
        
        self.last_run = datetime.now()
        return results
    
    def get_health_status(self) -> str:
        """Get overall health status"""
        if not self.last_run:
            return "unknown"
        
        critical_checks = [c for c in self.checks if c.critical]
        critical_failed = [c for c in critical_checks if c.last_result is False]
        
        if critical_failed:
            return "critical"
        
        failed_checks = [c for c in self.checks if c.last_result is False]
        if failed_checks:
            return "warning"
        
        return "healthy"
    
    def generate_report(self) -> str:
        """Generate human-readable health report"""
        results = self.run_all_checks()
        
        report = []
        report.append("🏥 eJAEGIS Health Monitor Report")
        report.append("=" * 50)
        report.append(f"Timestamp: {results['timestamp']}")
        report.append(f"Overall Status: {self.get_health_status().upper()}")
        report.append("")
        
        # Summary
        summary = results["summary"]
        report.append(f"📊 Summary: {summary['passed']}/{summary['total']} checks passed")
        if summary["critical_failed"] > 0:
            report.append(f"🚨 Critical Issues: {summary['critical_failed']}")
        report.append("")
        
        # Individual check results
        for check_name, result in results["checks"].items():
            status_icon = "✅" if result["success"] else "❌"
            critical_marker = " (CRITICAL)" if result["critical"] else ""
            
            report.append(f"{status_icon} {check_name}{critical_marker}")
            report.append(f"   {result['message']}")
            
            if not result["success"] and result["resolution_steps"]:
                report.append("   Resolution steps:")
                for step in result["resolution_steps"]:
                    report.append(f"   • {step}")
            report.append("")
        
        return "\n".join(report)
    
    def save_report(self, output_path: Path = None):
        """Save health report to file"""
        if not output_path:
            output_path = self.eJAEGIS_dir / "logs" / f"health-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(self.generate_report())
        
        return output_path

def main():
    """CLI for health monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description="eJAEGIS Health Monitor")
    parser.add_argument("--eJAEGIS-dir", default=".", help="eJAEGIS installation directory")
    parser.add_argument("--save-report", help="Save report to file")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--watch", type=int, help="Monitor continuously (interval in seconds)")
    
    args = parser.parse_args()
    
    eJAEGIS_dir = Path(args.eJAEGIS_dir).absolute()
    monitor = eJAEGISHealthMonitor(eJAEGIS_dir)
    
    if args.watch:
        print(f"🔄 Monitoring eJAEGIS health every {args.watch} seconds (Ctrl+C to stop)")
        try:
            while True:
                results = monitor.run_all_checks()
                
                if args.json:
                    print(json.dumps(results, indent=2))
                else:
                    print(monitor.generate_report())
                    print(f"\n⏰ Next check in {args.watch} seconds...")
                
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
    else:
        results = monitor.run_all_checks()
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(monitor.generate_report())
        
        if args.save_report:
            report_path = monitor.save_report(Path(args.save_report))
            print(f"\n📄 Report saved to: {report_path}")
        
        # Exit with error code if critical issues found
        if results["summary"]["critical_failed"] > 0:
            sys.exit(1)

if __name__ == "__main__":
    main()
