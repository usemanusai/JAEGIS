#!/usr/bin/env python3
"""
Run GitHub Repository Structure Creation
"""

import sys
import os
sys.path.append('JAEGIS_Enhanced_System')

from github_repository_structure import GitHubRepositoryStructureOrganizer

def main():
    print("🏗️ Creating GitHub Repository Structure...")
    organizer = GitHubRepositoryStructureOrganizer()
    result = organizer.create_github_structure()

    if result['status'] == 'success':
        print("✅ GitHub repository structure created successfully!")
        print(f"📁 Directories: {len(result['directories'])}")
        print(f"📄 Total files: {result['total_files']}")
        print(f"🔗 GitHub compatible: {result['github_compatible']}")
        
        summary = organizer.get_structure_summary()
        print("\n📋 Structure Summary:")
        for directory, info in summary['structure'].items():
            if info['exists']:
                print(f"   ✅ {directory}: {info['file_count']} files")
            else:
                print(f"   ❌ {directory}: Not created")
    else:
        print(f"❌ Structure creation failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
