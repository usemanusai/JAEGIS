#!/usr/bin/env python3
"""
JAEGIS Bulk Upload Runner
Simple script to run bulk upload with correct environment and paths
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 JAEGIS BULK UPLOAD RUNNER")
    print("=" * 50)
    
    # Set correct workspace path
    workspace_path = r"C:\Users\Lenovo ThinkPad T480\Desktop\JAEGIS"
    
    # Verify workspace exists
    if not Path(workspace_path).exists():
        print(f"❌ Workspace not found: {workspace_path}")
        sys.exit(1)
    
    # Check for JAEGIS directories
    jaegis_v1 = Path(workspace_path) / "JAEGIS-METHOD-v1.0"
    jaegis_v2 = Path(workspace_path) / "JAEGIS-METHOD-v2.0"
    
    if not jaegis_v1.exists():
        print(f"❌ JAEGIS-METHOD-v1.0 not found in {workspace_path}")
        sys.exit(1)
    
    if not jaegis_v2.exists():
        print(f"❌ JAEGIS-METHOD-v2.0 not found in {workspace_path}")
        sys.exit(1)
    
    print(f"✅ Workspace found: {workspace_path}")
    print(f"✅ JAEGIS-METHOD-v1.0 found")
    print(f"✅ JAEGIS-METHOD-v2.0 found")
    
    # Get GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        github_token = input("Enter GitHub token: ").strip()
        if not github_token:
            print("❌ GitHub token required")
            sys.exit(1)
    
    print(f"✅ GitHub token configured")
    
    # Set environment variables
    env = os.environ.copy()
    env.update({
        'GITHUB_TOKEN': github_token,
        'WORKSPACE_PATH': workspace_path,
        'BATCH_SIZE': '50',
        'MAX_CONCURRENT': '5',
        'RATE_LIMIT_DELAY': '1.0',
        'ENABLE_DOCQA': 'true',
        'DRY_RUN': 'false',
        'PYTHONIOENCODING': 'utf-8'
    })
    
    print("\n📊 UPLOAD CONFIGURATION")
    print(f"   Workspace: {workspace_path}")
    print(f"   Target: usemanusai/JAEGIS")
    print(f"   Batch Size: 50")
    print(f"   Max Concurrent: 5")
    print(f"   DocQA Agent: Enabled")
    
    # Confirm execution
    print("\n⚠️  IMPORTANT NOTICE")
    print("This will upload 96,715+ files to GitHub.")
    print("The process will take 24-36 hours to complete.")
    print("Ensure you have a stable internet connection.")
    
    response = input("\nProceed with bulk upload? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Upload cancelled")
        sys.exit(0)
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("\n🚀 STARTING BULK UPLOAD")
    print("=" * 50)
    print("Monitor progress: tail -f bulk_upload.log")
    print("Press Ctrl+C to stop (not recommended during upload)")
    print("=" * 50)
    
    try:
        # Run the bulk upload automation
        result = subprocess.run(
            [sys.executable, "bulk_upload_automation.py"],
            env=env,
            cwd=script_dir
        )
        
        if result.returncode == 0:
            print("\n✅ BULK UPLOAD COMPLETED SUCCESSFULLY")
        else:
            print(f"\n❌ BULK UPLOAD FAILED (exit code: {result.returncode})")
        
        return result.returncode
    
    except KeyboardInterrupt:
        print("\n⚠️ Upload interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Execution error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
