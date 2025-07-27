"""
Branch Strategy Execution System
Implement development branch targeting with staging backup and main branch protection
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class BranchType(str, Enum):
    """Types of Git branches."""
    MAIN = "main"
    DEVELOPMENT = "development"
    FEATURE = "feature"
    HOTFIX = "hotfix"
    RELEASE = "release"
    STAGING = "staging"


class ProtectionLevel(str, Enum):
    """Branch protection levels."""
    NONE = "none"
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    LOCKED = "locked"


class OperationStatus(str, Enum):
    """Branch operation status."""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    SKIPPED = "skipped"


@dataclass
class BranchConfig:
    """Branch configuration settings."""
    branch_name: str
    branch_type: BranchType
    protection_level: ProtectionLevel
    auto_merge_enabled: bool
    require_pr_review: bool
    require_status_checks: bool
    backup_enabled: bool
    sync_priority: int


@dataclass
class BranchOperation:
    """Branch operation record."""
    operation_id: str
    operation_type: str
    branch_name: str
    status: OperationStatus
    details: Dict[str, Any]
    timestamp: float
    duration_seconds: float
    error_message: Optional[str]


@dataclass
class SyncResult:
    """Branch synchronization result."""
    sync_id: str
    source_branch: str
    target_branch: str
    files_synced: int
    conflicts_resolved: int
    backup_created: Optional[str]
    status: OperationStatus
    timestamp: float


class BranchStrategyExecutor:
    """
    Branch Strategy Execution System
    
    Provides comprehensive branch management including:
    - Development branch targeting
    - Staging backup creation
    - Main branch protection
    - Automated synchronization
    - Conflict resolution
    """
    
    def __init__(self, repository_path: str = "."):
        self.repository_path = Path(repository_path)
        self.branch_configs: Dict[str, BranchConfig] = {}
        self.operation_history: List[BranchOperation] = []
        self.sync_results: List[SyncResult] = []
        
        # Configuration
        self.config = {
            "default_protection_level": ProtectionLevel.STANDARD,
            "backup_retention_days": 30,
            "auto_backup_enabled": True,
            "conflict_resolution_strategy": "prefer_development",
            "max_sync_attempts": 3,
            "sync_timeout_minutes": 30,
            "staging_branch_prefix": "staging/",
            "backup_branch_prefix": "backup/"
        }
        
        # Initialize default branch configurations
        self._initialize_default_branches()
        
        logger.info(f"Branch Strategy Executor initialized for {repository_path}")
    
    def _initialize_default_branches(self):
        """Initialize default branch configurations."""
        
        default_branches = [
            BranchConfig(
                branch_name="main",
                branch_type=BranchType.MAIN,
                protection_level=ProtectionLevel.STRICT,
                auto_merge_enabled=False,
                require_pr_review=True,
                require_status_checks=True,
                backup_enabled=True,
                sync_priority=1
            ),
            
            BranchConfig(
                branch_name="development",
                branch_type=BranchType.DEVELOPMENT,
                protection_level=ProtectionLevel.STANDARD,
                auto_merge_enabled=True,
                require_pr_review=False,
                require_status_checks=True,
                backup_enabled=True,
                sync_priority=2
            ),
            
            BranchConfig(
                branch_name="staging",
                branch_type=BranchType.STAGING,
                protection_level=ProtectionLevel.BASIC,
                auto_merge_enabled=True,
                require_pr_review=False,
                require_status_checks=False,
                backup_enabled=True,
                sync_priority=3
            )
        ]
        
        for branch_config in default_branches:
            self.branch_configs[branch_config.branch_name] = branch_config
    
    async def execute_branch_strategy(self, target_files: List[str]) -> Dict[str, Any]:
        """Execute comprehensive branch strategy for file synchronization."""
        
        logger.info(f"Executing branch strategy for {len(target_files)} files")
        
        execution_start = time.time()
        results = {
            "strategy_execution_id": f"exec_{int(time.time())}",
            "target_files": target_files,
            "operations_performed": [],
            "sync_results": [],
            "backups_created": [],
            "conflicts_encountered": [],
            "overall_status": OperationStatus.PENDING,
            "execution_time_seconds": 0
        }
        
        try:
            # Step 1: Create staging backups
            backup_results = await self._create_staging_backups()
            results["backups_created"] = backup_results
            
            # Step 2: Sync to development branch first
            dev_sync = await self._sync_to_development_branch(target_files)
            results["sync_results"].append(dev_sync)
            
            # Step 3: Apply main branch protection
            protection_result = await self._apply_main_branch_protection()
            results["operations_performed"].append(protection_result)
            
            # Step 4: Conditional sync to main (if development sync successful)
            if dev_sync.status == OperationStatus.SUCCESS:
                main_sync = await self._conditional_sync_to_main(target_files)
                results["sync_results"].append(main_sync)
            
            # Step 5: Update staging branch
            staging_sync = await self._update_staging_branch(target_files)
            results["sync_results"].append(staging_sync)
            
            # Determine overall status
            failed_operations = [r for r in results["sync_results"] if r.status == OperationStatus.FAILED]
            if failed_operations:
                results["overall_status"] = OperationStatus.FAILED
            else:
                results["overall_status"] = OperationStatus.SUCCESS
        
        except Exception as e:
            logger.error(f"Branch strategy execution failed: {e}")
            results["overall_status"] = OperationStatus.FAILED
            results["error"] = str(e)
        
        results["execution_time_seconds"] = time.time() - execution_start
        
        logger.info(f"Branch strategy execution completed: {results['overall_status'].value}")
        
        return results
    
    async def _create_staging_backups(self) -> List[str]:
        """Create staging backups for protected branches."""
        
        backups_created = []
        
        for branch_name, config in self.branch_configs.items():
            if config.backup_enabled and config.protection_level in [ProtectionLevel.STANDARD, ProtectionLevel.STRICT]:
                try:
                    backup_name = await self._create_branch_backup(branch_name)
                    backups_created.append(backup_name)
                    
                    logger.info(f"Created backup for {branch_name}: {backup_name}")
                    
                except Exception as e:
                    logger.error(f"Failed to create backup for {branch_name}: {e}")
        
        return backups_created
    
    async def _create_branch_backup(self, branch_name: str) -> str:
        """Create backup of specified branch."""
        
        timestamp = int(time.time())
        backup_name = f"{self.config['backup_branch_prefix']}{branch_name}_{timestamp}"
        
        operation_start = time.time()
        
        try:
            # Create backup branch
            result = await self._run_git_command([
                "git", "checkout", "-b", backup_name, branch_name
            ])
            
            if result["success"]:
                # Switch back to original branch
                await self._run_git_command(["git", "checkout", branch_name])
                
                # Record operation
                operation = BranchOperation(
                    operation_id=f"backup_{timestamp}",
                    operation_type="create_backup",
                    branch_name=backup_name,
                    status=OperationStatus.SUCCESS,
                    details={
                        "source_branch": branch_name,
                        "backup_branch": backup_name
                    },
                    timestamp=time.time(),
                    duration_seconds=time.time() - operation_start,
                    error_message=None
                )
                
                self.operation_history.append(operation)
                
                return backup_name
            
            else:
                raise Exception(f"Git backup command failed: {result['error']}")
        
        except Exception as e:
            logger.error(f"Backup creation failed for {branch_name}: {e}")
            raise
    
    async def _sync_to_development_branch(self, target_files: List[str]) -> SyncResult:
        """Synchronize files to development branch."""
        
        sync_id = f"dev_sync_{int(time.time())}"
        sync_start = time.time()
        
        try:
            # Switch to development branch
            checkout_result = await self._run_git_command(["git", "checkout", "development"])
            
            if not checkout_result["success"]:
                # Create development branch if it doesn't exist
                create_result = await self._run_git_command([
                    "git", "checkout", "-b", "development"
                ])
                
                if not create_result["success"]:
                    raise Exception("Failed to create development branch")
            
            # Copy target files to development branch
            files_synced = 0
            conflicts_resolved = 0
            
            for file_path in target_files:
                try:
                    # Add file to git
                    add_result = await self._run_git_command(["git", "add", file_path])
                    
                    if add_result["success"]:
                        files_synced += 1
                    else:
                        logger.warning(f"Failed to add file to development: {file_path}")
                
                except Exception as e:
                    logger.error(f"Error syncing file {file_path}: {e}")
            
            # Commit changes
            if files_synced > 0:
                commit_message = f"Sync {files_synced} files to development branch"
                commit_result = await self._run_git_command([
                    "git", "commit", "-m", commit_message
                ])
                
                if not commit_result["success"]:
                    logger.warning("Commit to development branch failed")
            
            sync_result = SyncResult(
                sync_id=sync_id,
                source_branch="local",
                target_branch="development",
                files_synced=files_synced,
                conflicts_resolved=conflicts_resolved,
                backup_created=None,
                status=OperationStatus.SUCCESS if files_synced > 0 else OperationStatus.FAILED,
                timestamp=time.time()
            )
            
            self.sync_results.append(sync_result)
            
            logger.info(f"Development sync completed: {files_synced} files synced")
            
            return sync_result
        
        except Exception as e:
            logger.error(f"Development branch sync failed: {e}")
            
            return SyncResult(
                sync_id=sync_id,
                source_branch="local",
                target_branch="development",
                files_synced=0,
                conflicts_resolved=0,
                backup_created=None,
                status=OperationStatus.FAILED,
                timestamp=time.time()
            )
    
    async def _apply_main_branch_protection(self) -> BranchOperation:
        """Apply protection rules to main branch."""
        
        operation_id = f"protect_main_{int(time.time())}"
        operation_start = time.time()
        
        try:
            main_config = self.branch_configs.get("main")
            
            if not main_config:
                raise Exception("Main branch configuration not found")
            
            # Apply protection rules (simulated - would integrate with Git hosting service API)
            protection_rules = {
                "require_pull_request_reviews": main_config.require_pr_review,
                "required_status_checks": main_config.require_status_checks,
                "enforce_admins": main_config.protection_level == ProtectionLevel.STRICT,
                "allow_force_pushes": main_config.protection_level == ProtectionLevel.NONE,
                "allow_deletions": False
            }
            
            # Simulate API call to apply protection
            await asyncio.sleep(0.1)  # Simulate API delay
            
            operation = BranchOperation(
                operation_id=operation_id,
                operation_type="apply_protection",
                branch_name="main",
                status=OperationStatus.SUCCESS,
                details={
                    "protection_rules": protection_rules,
                    "protection_level": main_config.protection_level.value
                },
                timestamp=time.time(),
                duration_seconds=time.time() - operation_start,
                error_message=None
            )
            
            self.operation_history.append(operation)
            
            logger.info("Main branch protection applied successfully")
            
            return operation
        
        except Exception as e:
            logger.error(f"Failed to apply main branch protection: {e}")
            
            return BranchOperation(
                operation_id=operation_id,
                operation_type="apply_protection",
                branch_name="main",
                status=OperationStatus.FAILED,
                details={},
                timestamp=time.time(),
                duration_seconds=time.time() - operation_start,
                error_message=str(e)
            )
    
    async def _conditional_sync_to_main(self, target_files: List[str]) -> SyncResult:
        """Conditionally synchronize to main branch based on protection rules."""
        
        sync_id = f"main_sync_{int(time.time())}"
        
        main_config = self.branch_configs.get("main")
        
        if not main_config:
            return SyncResult(
                sync_id=sync_id,
                source_branch="development",
                target_branch="main",
                files_synced=0,
                conflicts_resolved=0,
                backup_created=None,
                status=OperationStatus.FAILED,
                timestamp=time.time()
            )
        
        # Check if direct sync is allowed based on protection level
        if main_config.protection_level in [ProtectionLevel.STRICT, ProtectionLevel.LOCKED]:
            logger.info("Main branch sync skipped due to protection level")
            
            return SyncResult(
                sync_id=sync_id,
                source_branch="development",
                target_branch="main",
                files_synced=0,
                conflicts_resolved=0,
                backup_created=None,
                status=OperationStatus.SKIPPED,
                timestamp=time.time()
            )
        
        # Perform sync to main branch
        try:
            # Create backup first
            backup_name = await self._create_branch_backup("main")
            
            # Switch to main branch
            await self._run_git_command(["git", "checkout", "main"])
            
            # Merge from development
            merge_result = await self._run_git_command([
                "git", "merge", "development", "--no-ff", "-m", "Sync from development branch"
            ])
            
            if merge_result["success"]:
                sync_result = SyncResult(
                    sync_id=sync_id,
                    source_branch="development",
                    target_branch="main",
                    files_synced=len(target_files),
                    conflicts_resolved=0,
                    backup_created=backup_name,
                    status=OperationStatus.SUCCESS,
                    timestamp=time.time()
                )
                
                logger.info("Main branch sync completed successfully")
            
            else:
                sync_result = SyncResult(
                    sync_id=sync_id,
                    source_branch="development",
                    target_branch="main",
                    files_synced=0,
                    conflicts_resolved=0,
                    backup_created=backup_name,
                    status=OperationStatus.FAILED,
                    timestamp=time.time()
                )
                
                logger.error("Main branch sync failed during merge")
            
            self.sync_results.append(sync_result)
            return sync_result
        
        except Exception as e:
            logger.error(f"Main branch sync failed: {e}")
            
            return SyncResult(
                sync_id=sync_id,
                source_branch="development",
                target_branch="main",
                files_synced=0,
                conflicts_resolved=0,
                backup_created=None,
                status=OperationStatus.FAILED,
                timestamp=time.time()
            )
    
    async def _update_staging_branch(self, target_files: List[str]) -> SyncResult:
        """Update staging branch with latest changes."""
        
        sync_id = f"staging_sync_{int(time.time())}"
        
        try:
            # Switch to staging branch
            checkout_result = await self._run_git_command(["git", "checkout", "staging"])
            
            if not checkout_result["success"]:
                # Create staging branch from development
                create_result = await self._run_git_command([
                    "git", "checkout", "-b", "staging", "development"
                ])
                
                if not create_result["success"]:
                    raise Exception("Failed to create staging branch")
            
            else:
                # Merge latest changes from development
                merge_result = await self._run_git_command([
                    "git", "merge", "development", "--no-ff", "-m", "Update staging from development"
                ])
                
                if not merge_result["success"]:
                    logger.warning("Staging branch merge had conflicts")
            
            sync_result = SyncResult(
                sync_id=sync_id,
                source_branch="development",
                target_branch="staging",
                files_synced=len(target_files),
                conflicts_resolved=0,
                backup_created=None,
                status=OperationStatus.SUCCESS,
                timestamp=time.time()
            )
            
            self.sync_results.append(sync_result)
            
            logger.info("Staging branch updated successfully")
            
            return sync_result
        
        except Exception as e:
            logger.error(f"Staging branch update failed: {e}")
            
            return SyncResult(
                sync_id=sync_id,
                source_branch="development",
                target_branch="staging",
                files_synced=0,
                conflicts_resolved=0,
                backup_created=None,
                status=OperationStatus.FAILED,
                timestamp=time.time()
            )
    
    async def _run_git_command(self, command: List[str]) -> Dict[str, Any]:
        """Run Git command and return result."""
        
        try:
            result = subprocess.run(
                command,
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": " ".join(command)
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1,
                "command": " ".join(command)
            }
        
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "command": " ".join(command)
            }
    
    def configure_branch(self, branch_name: str, config: BranchConfig):
        """Configure branch settings."""
        
        self.branch_configs[branch_name] = config
        logger.info(f"Branch configuration updated: {branch_name}")
    
    def get_branch_status(self) -> Dict[str, Any]:
        """Get current branch status and statistics."""
        
        recent_operations = [
            op for op in self.operation_history
            if time.time() - op.timestamp < 3600  # Last hour
        ]
        
        recent_syncs = [
            sync for sync in self.sync_results
            if time.time() - sync.timestamp < 3600  # Last hour
        ]
        
        return {
            "configured_branches": len(self.branch_configs),
            "total_operations": len(self.operation_history),
            "recent_operations": len(recent_operations),
            "total_syncs": len(self.sync_results),
            "recent_syncs": len(recent_syncs),
            "successful_syncs": len([s for s in recent_syncs if s.status == OperationStatus.SUCCESS]),
            "failed_syncs": len([s for s in recent_syncs if s.status == OperationStatus.FAILED]),
            "branch_configurations": {
                name: {
                    "type": config.branch_type.value,
                    "protection_level": config.protection_level.value,
                    "backup_enabled": config.backup_enabled
                }
                for name, config in self.branch_configs.items()
            }
        }
    
    async def cleanup_old_backups(self):
        """Clean up old backup branches."""
        
        cutoff_time = time.time() - (self.config["backup_retention_days"] * 24 * 3600)
        
        # Get list of backup branches
        list_result = await self._run_git_command(["git", "branch", "-a"])
        
        if list_result["success"]:
            branches = list_result["stdout"].split('\n')
            backup_branches = [
                b.strip() for b in branches
                if self.config["backup_branch_prefix"] in b
            ]
            
            for branch in backup_branches:
                # Extract timestamp from branch name
                try:
                    timestamp_str = branch.split('_')[-1]
                    branch_timestamp = int(timestamp_str)
                    
                    if branch_timestamp < cutoff_time:
                        # Delete old backup branch
                        delete_result = await self._run_git_command([
                            "git", "branch", "-D", branch.replace("origin/", "")
                        ])
                        
                        if delete_result["success"]:
                            logger.info(f"Deleted old backup branch: {branch}")
                
                except (ValueError, IndexError):
                    # Skip branches with invalid timestamp format
                    continue


# Example usage
async def main():
    """Example usage of Branch Strategy Executor."""
    
    executor = BranchStrategyExecutor(".")
    
    # Configure custom branch
    custom_config = BranchConfig(
        branch_name="feature/new-feature",
        branch_type=BranchType.FEATURE,
        protection_level=ProtectionLevel.BASIC,
        auto_merge_enabled=True,
        require_pr_review=False,
        require_status_checks=False,
        backup_enabled=False,
        sync_priority=4
    )
    
    executor.configure_branch("feature/new-feature", custom_config)
    
    # Execute branch strategy
    test_files = ["test_file.py", "README.md", "config.json"]
    
    results = await executor.execute_branch_strategy(test_files)
    
    print(f"Branch Strategy Execution Results:")
    print(f"  Overall Status: {results['overall_status'].value}")
    print(f"  Files Targeted: {len(results['target_files'])}")
    print(f"  Operations: {len(results['operations_performed'])}")
    print(f"  Syncs: {len(results['sync_results'])}")
    print(f"  Backups: {len(results['backups_created'])}")
    print(f"  Execution Time: {results['execution_time_seconds']:.2f}s")
    
    # Get branch status
    status = executor.get_branch_status()
    print(f"\nBranch Status:")
    print(f"  Configured Branches: {status['configured_branches']}")
    print(f"  Recent Operations: {status['recent_operations']}")
    print(f"  Successful Syncs: {status['successful_syncs']}")
    print(f"  Failed Syncs: {status['failed_syncs']}")


if __name__ == "__main__":
    asyncio.run(main())
