#!/usr/bin/env python3
"""
JAEGIS Bulk Upload Execution Script
Simple execution wrapper for the bulk upload automation system

This script provides:
- One-command execution
- Pre-flight checks
- Configuration validation
- Progress monitoring
- Error handling
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Any


class BulkUploadExecutor:
    """Execution wrapper for bulk upload automation."""
    
    def __init__(self):
        self.config_file = "bulk_upload_config.json"
        self.env_file = ".env"
        self.log_file = "bulk_upload.log"
        
    def check_prerequisites(self) -> Dict[str, bool]:
        """Check all prerequisites for bulk upload."""
        print("🔍 Checking prerequisites...")
        
        checks = {
            "python_version": sys.version_info >= (3, 8),
            "config_exists": Path(self.config_file).exists(),
            "env_exists": Path(self.env_file).exists(),
            "github_token": bool(os.getenv('GITHUB_TOKEN')),
            "automation_script": Path("bulk_upload_automation.py").exists(),
            "workspace_valid": Path(".").exists()
        }
        
        # Check Python dependencies
        try:
            import aiohttp
            import aiofiles
            import requests
            checks["dependencies"] = True
        except ImportError:
            checks["dependencies"] = False
        
        return checks
    
    def print_prerequisite_status(self, checks: Dict[str, bool]):
        """Print prerequisite check results."""
        print("\n📋 PREREQUISITE CHECK RESULTS")
        print("=" * 40)
        
        status_map = {
            "python_version": "Python 3.8+",
            "dependencies": "Required Python packages",
            "config_exists": "Configuration file",
            "env_exists": "Environment file", 
            "github_token": "GitHub token",
            "automation_script": "Automation script",
            "workspace_valid": "Workspace directory"
        }
        
        all_passed = True
        for check, status in checks.items():
            icon = "✅" if status else "❌"
            name = status_map.get(check, check)
            print(f"{icon} {name}")
            if not status:
                all_passed = False
        
        return all_passed
    
    def setup_missing_prerequisites(self, checks: Dict[str, bool]):
        """Setup missing prerequisites."""
        print("\n🔧 Setting up missing prerequisites...")
        
        if not checks["dependencies"]:
            print("Installing Python dependencies...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", 
                    "aiohttp", "aiofiles", "requests"
                ], check=True)
                print("✅ Dependencies installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies")
                return False
        
        if not checks["config_exists"] or not checks["env_exists"]:
            print("Running configuration setup...")
            try:
                subprocess.run([sys.executable, "bulk_upload_config.py"], check=True)
                print("✅ Configuration setup complete")
            except subprocess.CalledProcessError:
                print("❌ Configuration setup failed")
                return False
        
        if not checks["github_token"]:
            token = input("Enter GitHub token: ").strip()
            if token:
                # Update .env file
                env_content = f"GITHUB_TOKEN={token}\n"
                if Path(self.env_file).exists():
                    with open(self.env_file, 'r') as f:
                        existing = f.read()
                    if 'GITHUB_TOKEN=' not in existing:
                        env_content = existing + env_content
                    else:
                        # Replace existing token
                        lines = existing.split('\n')
                        new_lines = []
                        for line in lines:
                            if line.startswith('GITHUB_TOKEN='):
                                new_lines.append(f"GITHUB_TOKEN={token}")
                            else:
                                new_lines.append(line)
                        env_content = '\n'.join(new_lines)
                
                with open(self.env_file, 'w') as f:
                    f.write(env_content)
                
                os.environ['GITHUB_TOKEN'] = token
                print("✅ GitHub token configured")
            else:
                print("❌ GitHub token required")
                return False
        
        return True
    
    def load_env_file(self):
        """Load environment variables from .env file."""
        if Path(self.env_file).exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
    
    def get_upload_summary(self) -> Dict[str, Any]:
        """Get upload summary from configuration."""
        if not Path(self.config_file).exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            workspace_info = config.get('workspace_info', {})
            return {
                "total_files": workspace_info.get('total_files', 0),
                "total_size_mb": workspace_info.get('total_size_mb', 0),
                "estimated_hours": workspace_info.get('estimated_upload_time_hours', 0),
                "phases": len(config.get('phases', [])),
                "docqa_enabled": config.get('optimization', {}).get('enable_docqa_agent', False)
            }
        except Exception:
            return {}
    
    def print_upload_summary(self, summary: Dict[str, Any]):
        """Print upload operation summary."""
        if not summary:
            return
        
        print("\n📊 UPLOAD OPERATION SUMMARY")
        print("=" * 40)
        print(f"Total Files: {summary['total_files']:,}")
        print(f"Total Size: {summary['total_size_mb']:.1f} MB")
        print(f"Upload Phases: {summary['phases']}")
        print(f"DocQA Agent: {'Enabled' if summary['docqa_enabled'] else 'Disabled'}")
        print(f"Estimated Time: {summary['estimated_hours']:.1f} hours")
        print(f"Target Repository: usemanusai/JAEGIS")
    
    def confirm_execution(self) -> bool:
        """Confirm execution with user."""
        print("\n⚠️  IMPORTANT NOTICE")
        print("This will upload 96,715+ files to GitHub.")
        print("The process will take 24-36 hours to complete.")
        print("Ensure you have a stable internet connection.")
        
        response = input("\nProceed with bulk upload? (yes/no): ").strip().lower()
        return response in ['yes', 'y']
    
    def execute_upload(self):
        """Execute the bulk upload process."""
        print("\n🚀 STARTING BULK UPLOAD AUTOMATION")
        print("=" * 50)
        print("Monitor progress: tail -f bulk_upload.log")
        print("Press Ctrl+C to stop (not recommended during upload)")
        print("=" * 50)
        
        try:
            # Execute the automation script
            process = subprocess.Popen(
                [sys.executable, "bulk_upload_automation.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Stream output
            for line in process.stdout:
                print(line.rstrip())
            
            # Wait for completion
            return_code = process.wait()
            
            if return_code == 0:
                print("\n✅ BULK UPLOAD COMPLETED SUCCESSFULLY")
                self.print_completion_summary()
            else:
                print(f"\n❌ BULK UPLOAD FAILED (exit code: {return_code})")
                print("Check bulk_upload.log for detailed error information")
            
            return return_code == 0
        
        except KeyboardInterrupt:
            print("\n⚠️ Upload interrupted by user")
            print("Progress has been saved. You can resume later.")
            return False
        except Exception as e:
            print(f"\n❌ Execution error: {e}")
            return False
    
    def print_completion_summary(self):
        """Print completion summary."""
        print("\n📊 UPLOAD COMPLETION SUMMARY")
        print("=" * 40)
        
        # Try to read final results
        results_files = list(Path(".").glob("bulk_upload_results_*.json"))
        if results_files:
            latest_results = max(results_files, key=lambda p: p.stat().st_mtime)
            try:
                with open(latest_results, 'r') as f:
                    results = json.load(f)
                
                stats = results.get('upload_statistics', {})
                print(f"Files Uploaded: {stats.get('uploaded_files', 0):,}")
                print(f"Files Failed: {stats.get('failed_files', 0):,}")
                print(f"Files Skipped: {stats.get('skipped_files', 0):,}")
                print(f"Success Rate: {results.get('success_rate', 0):.1f}%")
                print(f"Total Size: {stats.get('total_size_mb', 0):.1f} MB")
                print(f"Phases Completed: {stats.get('phases_completed', 0)}")
                
            except Exception:
                pass
        
        print(f"\nRepository: https://github.com/usemanusai/JAEGIS")
        print(f"Log File: {self.log_file}")
        print(f"Results: {latest_results.name if results_files else 'Not available'}")


def main():
    """Main execution function."""
    print("🚀 JAEGIS WORKSPACE BULK UPLOAD EXECUTOR")
    print("=" * 50)
    
    executor = BulkUploadExecutor()
    
    # Load environment
    executor.load_env_file()
    
    # Check prerequisites
    checks = executor.check_prerequisites()
    all_passed = executor.print_prerequisite_status(checks)
    
    if not all_passed:
        print("\n🔧 Some prerequisites are missing.")
        setup_response = input("Setup missing prerequisites? (y/n): ").strip().lower()
        
        if setup_response == 'y':
            if not executor.setup_missing_prerequisites(checks):
                print("❌ Failed to setup prerequisites")
                sys.exit(1)
        else:
            print("❌ Prerequisites required for execution")
            sys.exit(1)
    
    # Show upload summary
    summary = executor.get_upload_summary()
    executor.print_upload_summary(summary)
    
    # Confirm execution
    if not executor.confirm_execution():
        print("❌ Upload cancelled by user")
        sys.exit(0)
    
    # Execute upload
    success = executor.execute_upload()
    
    if success:
        print("\n🎉 Bulk upload completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Bulk upload failed or was interrupted")
        sys.exit(1)


if __name__ == "__main__":
    main()
