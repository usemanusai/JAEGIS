#!/usr/bin/env python3
"""
JAEGIS Multi-Account GitHub Bulk Upload Script
Distributes uploads across multiple GitHub accounts to maximize throughput
"""

import os
import sys
import time
import json
import asyncio
import aiohttp
import base64
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)

@dataclass
class GitHubAccount:
    """GitHub account configuration."""
    account_id: int
    token: str
    username: str = ""
    rate_limit_remaining: int = 5000
    rate_limit_reset: int = 0
    files_uploaded: int = 0
    success_rate: float = 0.0
    avg_response_time: float = 0.0
    is_active: bool = True
    last_used: float = 0.0

@dataclass
class UploadStats:
    """Upload statistics tracking."""
    total_files: int = 0
    uploaded: int = 0
    failed: int = 0
    skipped: int = 0
    start_time: float = field(default_factory=time.time)
    elapsed_time: float = 0.0
    upload_rate: float = 0.0
    account_switches: int = 0
    rate_limit_events: int = 0

class MultiAccountUploader:
    """Multi-account GitHub bulk uploader."""
    
    def __init__(self, workspace_path: str = None):
        self.accounts: List[GitHubAccount] = []
        self.current_account_index = 0
        self.stats = UploadStats()
        
        # Set workspace path - default to JAEGIS directory
        if workspace_path:
            self.workspace_path = Path(workspace_path)
        else:
            # Default to the JAEGIS directory structure
            current_dir = Path.cwd()
            if "JAEGIS-METHOD-v2.0" in str(current_dir):
                # We're in a subdirectory, go up to JAEGIS
                self.workspace_path = current_dir.parent.parent
            else:
                # Assume we're already in JAEGIS directory
                self.workspace_path = current_dir
        
        print(f"{Fore.CYAN}📁 Workspace: {self.workspace_path}")
        
        self.github_owner = "usemanusai"
        self.github_repo = "JAEGIS"
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Load accounts from environment
        self._load_accounts()
        
        # File exclusion patterns
        self.exclude_patterns = [
            '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.git', '.vscode',
            '*.log', '*.tmp', '*.bak', '*.backup', 'node_modules',
            '.pytest_cache', 'dist', 'build', '*.egg-info', '.env'
        ]
    
    def _load_accounts(self):
        """Load GitHub accounts from environment variables."""
        account_count = 0
        for i in range(1, 11):  # Check for up to 10 accounts
            token = os.getenv(f'GITHUB_TOKEN_{i}')
            if token:
                account = GitHubAccount(
                    account_id=i,
                    token=token,
                    username=f"Account_{i}"
                )
                self.accounts.append(account)
                account_count += 1
        
        if not self.accounts:
            print(f"{Fore.RED}❌ ERROR - No GitHub tokens found!")
            print(f"{Fore.YELLOW}💡 Set environment variables: GITHUB_TOKEN_1, GITHUB_TOKEN_2, etc.")
            sys.exit(1)
        
        print(f"{Fore.GREEN}✅ Loaded {account_count} GitHub accounts")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def _should_exclude_file(self, file_path: str) -> bool:
        """Check if file should be excluded."""
        path_str = str(file_path).lower()
        
        for pattern in self.exclude_patterns:
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        
        return False
    
    def _get_files_to_upload(self) -> List[str]:
        """Get list of files to upload."""
        files = []
        
        print(f"{Fore.CYAN}🔍 Scanning workspace for files...")
        
        for file_path in self.workspace_path.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.workspace_path)
                if not self._should_exclude_file(str(rel_path)):
                    files.append(str(rel_path))
        
        print(f"{Fore.GREEN}✅ Found {len(files):,} files to upload")
        return files
    
    def _get_next_available_account(self) -> Optional[GitHubAccount]:
        """Get next available account for upload."""
        current_time = time.time()
        
        # Check all accounts for availability
        for i in range(len(self.accounts)):
            account_index = (self.current_account_index + i) % len(self.accounts)
            account = self.accounts[account_index]
            
            # Check if account is available (more lenient check)
            if (account.is_active and 
                account.rate_limit_remaining > 5):  # Lower threshold
                
                self.current_account_index = account_index
                return account
        
        return None
    
    async def _check_rate_limits(self):
        """Check and update rate limits for all accounts."""
        if not self.session:
            return
        
        print(f"{Fore.YELLOW}🔄 Checking rate limits...")
        
        for account in self.accounts:
            try:
                headers = {'Authorization': f'token {account.token}'}
                async with self.session.get(
                    'https://api.github.com/rate_limit',
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        core_limit = data['resources']['core']
                        account.rate_limit_remaining = core_limit['remaining']
                        account.rate_limit_reset = core_limit['reset']
                        account.is_active = account.rate_limit_remaining > 5
                        
                        print(f"{Fore.BLUE}  Account {account.account_id}: {account.rate_limit_remaining} remaining")
                    else:
                        print(f"{Fore.RED}  Account {account.account_id}: Rate limit check failed ({response.status})")
                        account.is_active = False
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Rate limit check failed for account {account.account_id}: {e}")
                account.is_active = False

    async def _get_file_sha(self, file_path: str, account: GitHubAccount, branch: str = 'main') -> Optional[str]:
        """Get existing file SHA from repository for updates."""
        try:
            api_url = f'https://api.github.com/repos/{self.github_owner}/{self.github_repo}/contents/{file_path}'
            headers = {'Authorization': f'token {account.token}'}
            params = {'ref': branch}

            async with self.session.get(api_url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('sha')
                else:
                    # File doesn't exist (404) or other error
                    return None
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Could not get SHA for {file_path}: {e}")
            return None

    async def _upload_file(self, file_path: str, account: GitHubAccount) -> bool:
        """Upload single file using specified account."""
        if not self.session:
            return False
        
        try:
            # Read file content
            full_path = self.workspace_path / file_path
            
            # Check file size (GitHub has 100MB limit)
            file_size = full_path.stat().st_size
            if file_size > 100 * 1024 * 1024:  # 100MB
                print(f"{Fore.YELLOW}⏭️ Skipping large file: {file_path} ({file_size/1024/1024:.1f}MB)")
                self.stats.skipped += 1
                return True
            
            with open(full_path, 'rb') as f:
                content = base64.b64encode(f.read()).decode('utf-8')

            # Check if file exists and get SHA for updates
            existing_sha = await self._get_file_sha(file_path, account, 'main')

            # Prepare upload data
            upload_data = {
                'message': f'feat: bulk upload - Add {file_path}',
                'content': content,
                'branch': 'main'
            }

            # Add SHA if file exists (for updates)
            if existing_sha:
                upload_data['sha'] = existing_sha
            
            # GitHub API URL
            api_url = f'https://api.github.com/repos/{self.github_owner}/{self.github_repo}/contents/{file_path}'
            headers = {'Authorization': f'token {account.token}'}
            
            # Upload file
            start_time = time.time()
            async with self.session.put(api_url, json=upload_data, headers=headers) as response:
                upload_time = time.time() - start_time
                
                # Update account metrics
                account.last_used = time.time()
                account.avg_response_time = (account.avg_response_time + upload_time) / 2
                
                if response.status in [200, 201]:
                    account.files_uploaded += 1
                    account.rate_limit_remaining = max(0, account.rate_limit_remaining - 1)
                    self.stats.uploaded += 1
                    print(f"{Fore.GREEN}✅ {file_path} (Account {account.account_id})")
                    return True
                elif response.status == 409:
                    # File already exists
                    self.stats.skipped += 1
                    print(f"{Fore.YELLOW}⏭️ {file_path} (already exists)")
                    return True
                elif response.status == 403:
                    # Rate limited
                    account.rate_limit_remaining = 0
                    account.is_active = False
                    self.stats.rate_limit_events += 1
                    print(f"{Fore.RED}🚫 Account {account.account_id} rate limited")
                    return False
                else:
                    # Other error
                    error_text = await response.text()
                    print(f"{Fore.RED}❌ {file_path}: HTTP {response.status} - {error_text[:100]}")
                    self.stats.failed += 1
                    return False
        
        except Exception as e:
            print(f"{Fore.RED}❌ Upload failed for {file_path}: {e}")
            self.stats.failed += 1
            return False
    
    def _display_dashboard(self):
        """Display real-time upload dashboard."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print(f"{Fore.CYAN}🚀 MULTI-ACCOUNT GITHUB UPLOAD DASHBOARD")
        print("=" * 80)
        
        # Overall progress
        total_processed = self.stats.uploaded + self.stats.failed + self.stats.skipped
        progress_pct = total_processed / max(self.stats.total_files, 1) * 100
        
        print(f"\n{Fore.GREEN}📊 OVERALL PROGRESS:")
        print(f"Progress: {progress_pct:.1f}% ({total_processed:,}/{self.stats.total_files:,})")
        print(f"{Fore.GREEN}✅ Uploaded: {self.stats.uploaded:,}")
        print(f"{Fore.RED}❌ Failed: {self.stats.failed:,}")
        print(f"{Fore.YELLOW}⏭️ Skipped: {self.stats.skipped:,}")
        
        # Account status
        print(f"\n{Fore.BLUE}🔧 ACCOUNT STATUS:")
        for account in self.accounts:
            status_color = Fore.GREEN if account.is_active else Fore.RED
            status_text = "ACTIVE" if account.is_active else "INACTIVE"
            
            print(f"{account.username}: {status_color}{status_text}")
            print(f"  Files: {account.files_uploaded} ({account.files_uploaded/max(self.stats.total_files, 1)*100:.1f}%)")
            print(f"  Rate Limit: {account.rate_limit_remaining:,}")
            print(f"  Success Rate: {account.success_rate:.1f}%")
            print(f"  Avg Response: {account.avg_response_time*1000:.0f}ms")
        
        # Performance
        self.stats.elapsed_time = time.time() - self.stats.start_time
        if self.stats.elapsed_time > 0:
            self.stats.upload_rate = self.stats.uploaded / self.stats.elapsed_time
        
        print(f"\n{Fore.MAGENTA}⚡ PERFORMANCE:")
        print(f"Elapsed Time: {self.stats.elapsed_time/3600:.1f} hours")
        print(f"Upload Rate: {self.stats.upload_rate:.1f} files/second")
        print(f"Account Switches: {self.stats.account_switches}")
        print(f"Rate Limit Events: {self.stats.rate_limit_events}")
        
        print(f"\nLast Updated: {datetime.now().strftime('%H:%M:%S')}")

async def main():
    """Main execution function."""
    print(f"{Fore.CYAN}🚀 JAEGIS Multi-Account GitHub Bulk Upload")
    print(f"{Fore.CYAN}=" * 50)
    
    # Set workspace to JAEGIS directory
    workspace = r"C:\Users\Lenovo ThinkPad T480\Desktop\JAEGIS"
    
    async with MultiAccountUploader(workspace) as uploader:
        # Get files to upload
        files = uploader._get_files_to_upload()
        uploader.stats.total_files = len(files)
        
        if not files:
            print(f"{Fore.RED}❌ No files found to upload!")
            return
        
        # Initial rate limit check
        await uploader._check_rate_limits()
        
        # Upload files
        for i, file_path in enumerate(files):
            # Display dashboard every 50 files
            if i % 50 == 0:
                uploader._display_dashboard()
            
            # Get available account
            account = uploader._get_next_available_account()
            
            if not account:
                # No accounts available, wait and check again
                print(f"{Fore.YELLOW}⏳ No accounts available, checking rate limits...")
                await uploader._check_rate_limits()
                account = uploader._get_next_available_account()
                
                if not account:
                    print(f"{Fore.YELLOW}⏳ Still no accounts available, waiting 60s...")
                    await asyncio.sleep(60)
                    continue
            
            # Upload file
            await uploader._upload_file(file_path, account)
            
            # Small delay between uploads
            await asyncio.sleep(0.2)
        
        # Final dashboard
        uploader._display_dashboard()
        print(f"\n{Fore.CYAN}🎉 Upload complete!")

if __name__ == "__main__":
    asyncio.run(main())
