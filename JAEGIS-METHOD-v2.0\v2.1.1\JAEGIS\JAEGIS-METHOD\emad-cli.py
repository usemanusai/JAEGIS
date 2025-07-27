#!/usr/bin/env python3

"""
eJAEGIS Command Line Interface

Universal CLI for managing the eJAEGIS (Ecosystem for JAEGIS Method AI Development) system.
Provides unified access to all eJAEGIS functionality across platforms.
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from eJAEGIS_auto_sync import eJAEGISAutoSync
    from eJAEGIS_failsafe_system import eJAEGISFailsafeSystem
    eJAEGIS_MODULES_AVAILABLE = True
except ImportError as e:
    eJAEGIS_MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)

class eJAEGISConfig:
    """eJAEGIS configuration management"""
    
    def __init__(self, eJAEGIS_dir: Path):
        self.eJAEGIS_dir = eJAEGIS_dir
        self.config_dir = eJAEGIS_dir / "config"
        self.user_config_path = self.config_dir / "eJAEGIS-user-config.json"
        self.project_config_path = self.config_dir / "eJAEGIS-project-config.json"
        
        self.config_dir.mkdir(exist_ok=True)
        
    def load_user_config(self):
        """Load user configuration"""
        try:
            if self.user_config_path.exists():
                with open(self.user_config_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading user config: {e}")
            return {}
    
    def load_project_config(self):
        """Load project configuration"""
        try:
            if self.project_config_path.exists():
                with open(self.project_config_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading project config: {e}")
            return {}
    
    def save_user_config(self, config):
        """Save user configuration"""
        try:
            with open(self.user_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving user config: {e}")
            return False

class eJAEGISCLI:
    """Main eJAEGIS CLI class"""
    
    def __init__(self):
        self.eJAEGIS_dir = Path(__file__).parent.absolute()
        self.config = eJAEGISConfig(self.eJAEGIS_dir)
        self.user_config = self.config.load_user_config()
        self.project_config = self.config.load_project_config()
    
    def print_header(self, title):
        """Print formatted header"""
        print(f"\n🚀 {title}")
        print("=" * 60)
    
    def print_status(self, message, status):
        """Print status message"""
        if status:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    def cmd_version(self, args):
        """Show eJAEGIS version information"""
        print("eJAEGIS (Ecosystem for JAEGIS Method AI Development)")
        print("Version: 1.0.0")
        print(f"Installation: {self.eJAEGIS_dir}")
        print(f"Python: {sys.version}")
        print(f"Modules Available: {'Yes' if eJAEGIS_MODULES_AVAILABLE else 'No'}")
        if not eJAEGIS_MODULES_AVAILABLE:
            print(f"Import Error: {IMPORT_ERROR}")
    
    def cmd_status(self, args):
        """Show eJAEGIS system status"""
        self.print_header("eJAEGIS System Status")
        
        # Configuration status
        has_user_config = self.user_config_path.exists()
        has_project_config = self.project_config_path.exists()
        self.print_status("User configuration", has_user_config)
        self.print_status("Project configuration", has_project_config)
        
        # Module availability
        self.print_status("eJAEGIS modules", eJAEGIS_MODULES_AVAILABLE)
        
        if eJAEGIS_MODULES_AVAILABLE:
            # Background runner status
            try:
                result = subprocess.run([
                    sys.executable, str(self.eJAEGIS_dir / "eJAEGIS-background-runner.py"), "status"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print("✅ Background runner status:")
                    print("   " + result.stdout.replace('\n', '\n   '))
                else:
                    print("❌ Background runner not running")
            except Exception as e:
                print(f"⚠️  Could not check background runner: {e}")
            
            # Failsafe system status
            try:
                result = subprocess.run([
                    sys.executable, str(self.eJAEGIS_dir / "eJAEGIS-failsafe-cli.py"), "status"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print("✅ Failsafe system status:")
                    print("   " + result.stdout.replace('\n', '\n   '))
                else:
                    print("❌ Failsafe system not available")
            except Exception as e:
                print(f"⚠️  Could not check failsafe system: {e}")
        
        # Configuration details
        if has_user_config:
            print("\n📋 User Configuration:")
            github_config = self.user_config.get('github', {})
            print(f"   GitHub User: {github_config.get('username', 'Not set')}")
            print(f"   Repository: {github_config.get('repository', 'Not set')}")
            print(f"   Token: {'Set' if github_config.get('token') else 'Not set'}")
            
            sync_config = self.user_config.get('sync', {})
            interval = sync_config.get('interval_seconds', 3600)
            print(f"   Sync Interval: {interval} seconds ({interval//3600}h {(interval%3600)//60}m)")
        
        if has_project_config:
            print("\n📋 Project Configuration:")
            print(f"   Project Type: {self.project_config.get('project_type', 'Unknown')}")
            failsafe_config = self.project_config.get('failsafe', {})
            print(f"   Failsafe Sensitivity: {failsafe_config.get('sensitivity', 'balanced')}")
    
    def cmd_init(self, args):
        """Initialize eJAEGIS in current directory"""
        self.print_header("eJAEGIS Project Initialization")
        
        current_dir = Path.cwd()
        print(f"Initializing eJAEGIS in: {current_dir}")
        
        # Check if already initialized
        if (current_dir / ".eJAEGIS").exists():
            print("⚠️  eJAEGIS already initialized in this directory")
            response = input("Reinitialize? (y/N): ").lower().strip()
            if response != 'y':
                return
        
        # Create .eJAEGIS directory
        eJAEGIS_project_dir = current_dir / ".eJAEGIS"
        eJAEGIS_project_dir.mkdir(exist_ok=True)
        
        # Create project-specific configuration
        project_config = {
            "eJAEGIS_installation": str(self.eJAEGIS_dir),
            "project_root": str(current_dir),
            "initialized_at": datetime.now().isoformat(),
            "project_type": self.detect_project_type(current_dir)
        }
        
        with open(eJAEGIS_project_dir / "project.json", 'w') as f:
            json.dump(project_config, f, indent=2)
        
        # Create .gitignore entry
        gitignore_path = current_dir / ".gitignore"
        gitignore_entries = [
            "# eJAEGIS system files",
            ".eJAEGIS/",
            "eJAEGIS-*.log",
            "eJAEGIS-runner.pid"
        ]
        
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                existing_content = f.read()
            
            if ".eJAEGIS/" not in existing_content:
                with open(gitignore_path, 'a') as f:
                    f.write("\n" + "\n".join(gitignore_entries) + "\n")
                print("✅ Updated .gitignore with eJAEGIS entries")
        else:
            with open(gitignore_path, 'w') as f:
                f.write("\n".join(gitignore_entries) + "\n")
            print("✅ Created .gitignore with eJAEGIS entries")
        
        print("✅ eJAEGIS initialized successfully")
        print(f"   Project type: {project_config['project_type']}")
        print(f"   Configuration: {eJAEGIS_project_dir / 'project.json'}")
        
        # Suggest next steps
        print("\nNext steps:")
        print("1. Run: eJAEGIS start")
        print("2. Check status: eJAEGIS status")
    
    def cmd_start(self, args):
        """Start eJAEGIS background monitoring"""
        self.print_header("Starting eJAEGIS System")
        
        if not eJAEGIS_MODULES_AVAILABLE:
            print("❌ eJAEGIS modules not available")
            print(f"Error: {IMPORT_ERROR}")
            return
        
        try:
            # Start background runner
            result = subprocess.run([
                sys.executable, str(self.eJAEGIS_dir / "eJAEGIS-background-runner.py"), "start"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ eJAEGIS background runner started")
                print(result.stdout)
            else:
                print("❌ Failed to start background runner")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Error starting eJAEGIS: {e}")
    
    def cmd_stop(self, args):
        """Stop eJAEGIS background monitoring"""
        self.print_header("Stopping eJAEGIS System")
        
        try:
            # Stop background runner
            result = subprocess.run([
                sys.executable, str(self.eJAEGIS_dir / "eJAEGIS-background-runner.py"), "stop"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ eJAEGIS background runner stopped")
                print(result.stdout)
            else:
                print("❌ Failed to stop background runner")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Error stopping eJAEGIS: {e}")
    
    def cmd_restart(self, args):
        """Restart eJAEGIS background monitoring"""
        self.print_header("Restarting eJAEGIS System")
        
        # Stop first
        self.cmd_stop(args)
        
        # Wait a moment
        import time
        time.sleep(2)
        
        # Start again
        self.cmd_start(args)
    
    def cmd_test(self, args):
        """Run eJAEGIS system tests"""
        self.print_header("eJAEGIS System Tests")
        
        if not eJAEGIS_MODULES_AVAILABLE:
            print("❌ eJAEGIS modules not available")
            return
        
        try:
            # Run auto-sync test
            result = subprocess.run([
                sys.executable, str(self.eJAEGIS_dir / "eJAEGIS-auto-sync.py"), "--test"
            ], capture_output=True, text=True)
            
            print("📊 Auto-sync test results:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            
            # Run failsafe tests
            result = subprocess.run([
                sys.executable, str(self.eJAEGIS_dir / "eJAEGIS-failsafe-cli.py"), "test"
            ], capture_output=True, text=True)
            
            print("\n📊 Failsafe test results:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error running tests: {e}")
    
    def cmd_config(self, args):
        """Show or edit eJAEGIS configuration"""
        if args.edit:
            self.edit_config()
        else:
            self.show_config()
    
    def show_config(self):
        """Show current configuration"""
        self.print_header("eJAEGIS Configuration")
        
        print("📋 User Configuration:")
        if self.user_config:
            print(json.dumps(self.user_config, indent=2))
        else:
            print("   No user configuration found")
        
        print("\n📋 Project Configuration:")
        if self.project_config:
            print(json.dumps(self.project_config, indent=2))
        else:
            print("   No project configuration found")
    
    def edit_config(self):
        """Interactive configuration editor"""
        self.print_header("eJAEGIS Configuration Editor")
        
        # Edit GitHub settings
        print("GitHub Settings:")
        current_token = self.user_config.get('github', {}).get('token', '')
        if current_token:
            print(f"Current token: {current_token[:10]}...")
            change_token = input("Change GitHub token? (y/N): ").lower().strip()
            if change_token == 'y':
                new_token = input("New GitHub token: ").strip()
                if new_token:
                    if 'github' not in self.user_config:
                        self.user_config['github'] = {}
                    self.user_config['github']['token'] = new_token
        else:
            new_token = input("GitHub token: ").strip()
            if new_token:
                if 'github' not in self.user_config:
                    self.user_config['github'] = {}
                self.user_config['github']['token'] = new_token
        
        # Save configuration
        if self.config.save_user_config(self.user_config):
            print("✅ Configuration saved")
        else:
            print("❌ Failed to save configuration")
    
    def detect_project_type(self, project_dir):
        """Detect project type from files"""
        if (project_dir / "package.json").exists():
            return "nodejs"
        elif (project_dir / "requirements.txt").exists():
            return "python"
        elif (project_dir / "Cargo.toml").exists():
            return "rust"
        elif (project_dir / "pom.xml").exists():
            return "java"
        elif (project_dir / "go.mod").exists():
            return "go"
        else:
            return "generic"
    
    def cmd_help(self, args):
        """Show help information"""
        print("eJAEGIS - Ecosystem for JAEGIS Method AI Development")
        print("\nAvailable commands:")
        print("  init      - Initialize eJAEGIS in current directory")
        print("  start     - Start eJAEGIS background monitoring")
        print("  stop      - Stop eJAEGIS background monitoring")
        print("  restart   - Restart eJAEGIS background monitoring")
        print("  status    - Show eJAEGIS system status")
        print("  test      - Run eJAEGIS system tests")
        print("  config    - Show configuration")
        print("  version   - Show version information")
        print("  help      - Show this help")
        print("\nFor more information: https://github.com/huggingfacer04/eJAEGIS")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="eJAEGIS - Ecosystem for JAEGIS Method AI Development",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Commands
    subparsers.add_parser('init', help='Initialize eJAEGIS in current directory')
    subparsers.add_parser('start', help='Start eJAEGIS background monitoring')
    subparsers.add_parser('stop', help='Stop eJAEGIS background monitoring')
    subparsers.add_parser('restart', help='Restart eJAEGIS background monitoring')
    subparsers.add_parser('status', help='Show eJAEGIS system status')
    subparsers.add_parser('test', help='Run eJAEGIS system tests')
    subparsers.add_parser('version', help='Show version information')
    subparsers.add_parser('help', help='Show help information')
    
    config_parser = subparsers.add_parser('config', help='Show or edit configuration')
    config_parser.add_argument('--edit', action='store_true', help='Edit configuration interactively')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    cli = eJAEGISCLI()
    
    # Route to appropriate command
    command_map = {
        'init': cli.cmd_init,
        'start': cli.cmd_start,
        'stop': cli.cmd_stop,
        'restart': cli.cmd_restart,
        'status': cli.cmd_status,
        'test': cli.cmd_test,
        'config': cli.cmd_config,
        'version': cli.cmd_version,
        'help': cli.cmd_help
    }
    
    if args.command in command_map:
        try:
            command_map[args.command](args)
            return 0
        except KeyboardInterrupt:
            print("\n⚠️  Command interrupted by user")
            return 1
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            return 1
    else:
        print(f"Unknown command: {args.command}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
