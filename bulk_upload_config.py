#!/usr/bin/env python3
"""
JAEGIS Bulk Upload Configuration and Setup Script
Configuration management and setup utilities for bulk upload automation

This script provides:
- Environment configuration setup
- GitHub token validation
- Workspace analysis and validation
- Upload plan customization
- Performance optimization settings
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import requests
from dataclasses import dataclass, asdict


@dataclass
class WorkspaceAnalysis:
    """Workspace analysis results."""
    total_files: int
    total_directories: int
    total_size_mb: float
    file_types: Dict[str, int]
    large_files: List[str]
    directory_breakdown: Dict[str, Dict[str, Any]]


class BulkUploadConfigurator:
    """Configuration manager for bulk upload operations."""
    
    def __init__(self):
        self.config_file = "bulk_upload_config.json"
        self.env_file = ".env"
        
    def analyze_workspace(self, workspace_path: str = ".") -> WorkspaceAnalysis:
        """Analyze workspace structure and content."""
        print("🔍 Analyzing workspace structure...")
        
        workspace = Path(workspace_path)
        total_files = 0
        total_directories = 0
        total_size = 0
        file_types = {}
        large_files = []
        directory_breakdown = {}
        
        # Analyze each directory
        for item in workspace.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                dir_info = self._analyze_directory(item)
                directory_breakdown[item.name] = dir_info
                
                total_files += dir_info['file_count']
                total_directories += dir_info['dir_count']
                total_size += dir_info['size_mb']
                
                # Merge file types
                for ext, count in dir_info['file_types'].items():
                    file_types[ext] = file_types.get(ext, 0) + count
                
                # Add large files
                large_files.extend(dir_info['large_files'])
        
        return WorkspaceAnalysis(
            total_files=total_files,
            total_directories=total_directories,
            total_size_mb=total_size,
            file_types=file_types,
            large_files=large_files,
            directory_breakdown=directory_breakdown
        )
    
    def _analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Analyze a single directory."""
        file_count = 0
        dir_count = 0
        total_size = 0
        file_types = {}
        large_files = []
        
        try:
            for item in dir_path.rglob('*'):
                if item.is_file():
                    file_count += 1
                    size_mb = item.stat().st_size / (1024 * 1024)
                    total_size += size_mb
                    
                    # Track file types
                    ext = item.suffix.lower() or 'no_extension'
                    file_types[ext] = file_types.get(ext, 0) + 1
                    
                    # Track large files (>10MB)
                    if size_mb > 10:
                        large_files.append(str(item))
                
                elif item.is_dir():
                    dir_count += 1
        
        except PermissionError:
            pass  # Skip inaccessible directories
        
        return {
            'file_count': file_count,
            'dir_count': dir_count,
            'size_mb': total_size,
            'file_types': file_types,
            'large_files': large_files
        }
    
    def validate_github_token(self, token: str) -> Dict[str, Any]:
        """Validate GitHub token and check permissions."""
        print("🔐 Validating GitHub token...")
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            # Check token validity
            response = requests.get('https://api.github.com/user', headers=headers)
            
            if response.status_code != 200:
                return {
                    'valid': False,
                    'error': f'Invalid token: HTTP {response.status_code}'
                }
            
            user_data = response.json()
            
            # Check repository access
            repo_response = requests.get(
                'https://api.github.com/repos/usemanusai/JAEGIS',
                headers=headers
            )
            
            repo_access = repo_response.status_code == 200
            
            # Check rate limits
            rate_limit_response = requests.get(
                'https://api.github.com/rate_limit',
                headers=headers
            )
            
            rate_limit_data = rate_limit_response.json() if rate_limit_response.status_code == 200 else {}
            
            return {
                'valid': True,
                'user': user_data.get('login'),
                'user_id': user_data.get('id'),
                'repo_access': repo_access,
                'rate_limit': rate_limit_data.get('rate', {}),
                'scopes': response.headers.get('X-OAuth-Scopes', '').split(', ')
            }
        
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def generate_optimized_config(self, workspace_analysis: WorkspaceAnalysis) -> Dict[str, Any]:
        """Generate optimized configuration based on workspace analysis."""
        print("⚙️ Generating optimized configuration...")
        
        # Calculate optimal batch size based on file count and types
        if workspace_analysis.total_files > 50000:
            batch_size = 100  # Larger batches for massive workspaces
            max_concurrent = 3  # Lower concurrency to avoid rate limits
        elif workspace_analysis.total_files > 10000:
            batch_size = 75
            max_concurrent = 4
        else:
            batch_size = 50
            max_concurrent = 5
        
        # Adjust rate limiting based on file types
        has_many_docs = workspace_analysis.file_types.get('.md', 0) > 100
        rate_limit_delay = 0.5 if has_many_docs else 1.0
        
        # Enable DocQA for documentation-heavy workspaces
        enable_docqa = (
            workspace_analysis.file_types.get('.md', 0) > 50 or
            workspace_analysis.file_types.get('.txt', 0) > 100 or
            workspace_analysis.file_types.get('.rst', 0) > 10
        )
        
        config = {
            "github_settings": {
                "owner": "usemanusai",
                "repo": "JAEGIS",
                "branch": "main"
            },
            "upload_settings": {
                "batch_size": batch_size,
                "max_concurrent": max_concurrent,
                "rate_limit_delay": rate_limit_delay,
                "max_retries": 3,
                "max_file_size_mb": 100
            },
            "optimization": {
                "enable_docqa_agent": enable_docqa,
                "enable_compression": True,
                "enable_smart_batching": True,
                "skip_binary_files": True
            },
            "workspace_info": {
                "total_files": workspace_analysis.total_files,
                "total_size_mb": workspace_analysis.total_size_mb,
                "estimated_upload_time_hours": self._estimate_upload_time(workspace_analysis, batch_size, rate_limit_delay)
            },
            "phases": [
                {
                    "phase_id": "phase_4",
                    "name": "Core System Foundation",
                    "directories": ["core/brain_protocol", "core/garas", "core/iuas", "core/nlds", "core/protocols"],
                    "priority": "CRITICAL"
                },
                {
                    "phase_id": "phase_5",
                    "name": "N.L.D.S. Complete System", 
                    "directories": ["nlds"],
                    "priority": "CRITICAL"
                },
                {
                    "phase_id": "phase_6",
                    "name": "Enhanced JAEGIS Systems",
                    "directories": ["JAEGIS", "JAEGIS_Config_System", "JAEGIS_Enhanced_System", "eJAEGIS"],
                    "priority": "HIGH"
                },
                {
                    "phase_id": "phase_7", 
                    "name": "P.I.T.C.E.S. & Cognitive Pipeline",
                    "directories": ["pitces", "cognitive_pipeline"],
                    "priority": "HIGH"
                },
                {
                    "phase_id": "phase_8",
                    "name": "Deployment & Infrastructure",
                    "directories": ["deployment"],
                    "priority": "MEDIUM"
                },
                {
                    "phase_id": "phase_9",
                    "name": "Documentation & Testing",
                    "directories": ["docs", "tests"],
                    "priority": "MEDIUM"
                },
                {
                    "phase_id": "phase_10",
                    "name": "Examples & Demonstrations", 
                    "directories": ["examples"],
                    "priority": "LOW"
                }
            ]
        }
        
        return config
    
    def _estimate_upload_time(self, analysis: WorkspaceAnalysis, batch_size: int, rate_delay: float) -> float:
        """Estimate total upload time in hours."""
        # Base time per file (including API call overhead)
        base_time_per_file = 0.5  # seconds
        
        # Rate limiting delay
        total_delay_time = analysis.total_files * rate_delay
        
        # Batch processing efficiency
        batches = (analysis.total_files + batch_size - 1) // batch_size
        batch_overhead = batches * 2  # 2 seconds overhead per batch
        
        # Total time in seconds
        total_seconds = (analysis.total_files * base_time_per_file) + total_delay_time + batch_overhead
        
        # Convert to hours
        return total_seconds / 3600
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"💾 Configuration saved to {self.config_file}")
    
    def create_env_file(self, github_token: str):
        """Create environment file with settings."""
        env_content = f"""# JAEGIS Bulk Upload Environment Configuration
GITHUB_TOKEN={github_token}
WORKSPACE_PATH=.
BATCH_SIZE=50
MAX_CONCURRENT=5
RATE_LIMIT_DELAY=1.0
ENABLE_DOCQA=true
DRY_RUN=false
"""
        
        with open(self.env_file, 'w') as f:
            f.write(env_content)
        print(f"💾 Environment file created: {self.env_file}")
    
    def print_workspace_summary(self, analysis: WorkspaceAnalysis):
        """Print workspace analysis summary."""
        print("\n📊 WORKSPACE ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"Total Files: {analysis.total_files:,}")
        print(f"Total Directories: {analysis.total_directories:,}")
        print(f"Total Size: {analysis.total_size_mb:.1f} MB")
        print(f"Large Files (>10MB): {len(analysis.large_files)}")
        
        print("\n📁 Top File Types:")
        sorted_types = sorted(analysis.file_types.items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_types[:10]:
            print(f"  {ext}: {count:,} files")
        
        print("\n📂 Directory Breakdown:")
        sorted_dirs = sorted(analysis.directory_breakdown.items(), key=lambda x: x[1]['file_count'], reverse=True)
        for dir_name, info in sorted_dirs[:10]:
            print(f"  {dir_name}: {info['file_count']:,} files ({info['size_mb']:.1f} MB)")


def main():
    """Main configuration setup function."""
    print("🚀 JAEGIS BULK UPLOAD CONFIGURATOR")
    print("=" * 50)
    
    configurator = BulkUploadConfigurator()
    
    # Get GitHub token
    github_token = input("Enter GitHub token (or press Enter to use GITHUB_TOKEN env var): ").strip()
    if not github_token:
        github_token = os.getenv('GITHUB_TOKEN', '')
    
    if not github_token:
        print("❌ GitHub token required")
        sys.exit(1)
    
    # Validate token
    token_validation = configurator.validate_github_token(github_token)
    if not token_validation['valid']:
        print(f"❌ Token validation failed: {token_validation['error']}")
        sys.exit(1)
    
    print(f"✅ Token valid for user: {token_validation['user']}")
    print(f"   Repository access: {'Yes' if token_validation['repo_access'] else 'No'}")
    
    # Analyze workspace
    workspace_path = input("Enter workspace path (or press Enter for current directory): ").strip() or "."
    analysis = configurator.analyze_workspace(workspace_path)
    
    # Print summary
    configurator.print_workspace_summary(analysis)
    
    # Generate configuration
    config = configurator.generate_optimized_config(analysis)
    
    print(f"\n⚙️ OPTIMIZED CONFIGURATION")
    print(f"Batch Size: {config['upload_settings']['batch_size']}")
    print(f"Max Concurrent: {config['upload_settings']['max_concurrent']}")
    print(f"Rate Limit Delay: {config['upload_settings']['rate_limit_delay']}s")
    print(f"DocQA Agent: {'Enabled' if config['optimization']['enable_docqa_agent'] else 'Disabled'}")
    print(f"Estimated Upload Time: {config['workspace_info']['estimated_upload_time_hours']:.1f} hours")
    
    # Save configuration
    save_config = input("\nSave configuration? (y/n): ").strip().lower()
    if save_config == 'y':
        configurator.save_config(config)
        configurator.create_env_file(github_token)
        
        print("\n✅ Configuration setup complete!")
        print("Next steps:")
        print("1. Review the generated configuration file")
        print("2. Run: python bulk_upload_automation.py")
        print("3. Monitor progress in bulk_upload.log")


if __name__ == "__main__":
    main()
