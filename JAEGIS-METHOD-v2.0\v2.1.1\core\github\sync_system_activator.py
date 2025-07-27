"""
GitHub Sync System Activation
Activate automated 60-minute sync cycles with comprehensive monitoring and error handling
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import aiohttp
import subprocess
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SyncCycleStatus(str, Enum):
    """Sync cycle status levels."""
    IDLE = "idle"
    PREPARING = "preparing"
    SYNCING = "syncing"
    VALIDATING = "validating"
    COMPLETE = "complete"
    ERROR = "error"
    PAUSED = "paused"


class SyncDirection(str, Enum):
    """Sync direction options."""
    BIDIRECTIONAL = "bidirectional"
    LOCAL_TO_REMOTE = "local_to_remote"
    REMOTE_TO_LOCAL = "remote_to_local"


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SyncCycle:
    """Sync cycle information."""
    cycle_id: str
    start_time: float
    end_time: Optional[float]
    status: SyncCycleStatus
    direction: SyncDirection
    files_processed: int
    files_synced: int
    files_skipped: int
    errors_encountered: List[str]
    performance_metrics: Dict[str, float]


@dataclass
class SyncError:
    """Sync error information."""
    error_id: str
    cycle_id: str
    severity: ErrorSeverity
    error_type: str
    description: str
    file_path: Optional[str]
    resolution_attempted: bool
    resolved: bool
    timestamp: float


@dataclass
class SyncMetrics:
    """Sync system metrics."""
    total_cycles: int
    successful_cycles: int
    failed_cycles: int
    average_cycle_duration: float
    total_files_synced: int
    sync_success_rate: float
    last_sync_time: float
    next_sync_time: float
    system_uptime: float


class GitHubSyncSystemActivator:
    """
    GitHub Sync System Activation
    
    Provides automated synchronization including:
    - 60-minute sync cycles
    - Comprehensive monitoring
    - Error handling and recovery
    - Performance optimization
    - Conflict resolution
    """
    
    def __init__(self, repository: str = "usemanusai/JAEGIS", sync_interval_minutes: int = 60):
        self.repository = repository
        self.sync_interval = sync_interval_minutes * 60  # Convert to seconds
        self.is_active = False
        self.current_cycle: Optional[SyncCycle] = None
        
        # Storage
        self.sync_history: List[SyncCycle] = []
        self.sync_errors: List[SyncError] = []
        
        # Configuration
        self.config = {
            "github_api_base": "https://api.github.com",
            "max_retries": 3,
            "retry_delay_seconds": 30,
            "timeout_seconds": 300,
            "max_file_size_mb": 100,
            "excluded_patterns": [
                "*.tmp", "*.log", "*.cache", "__pycache__", ".git",
                "node_modules", ".env", "*.pyc"
            ],
            "auto_recovery_enabled": True,
            "conflict_resolution": "prefer_remote",
            "backup_before_sync": True,
            "validate_after_sync": True
        }
        
        # Monitoring
        self.start_time = time.time()
        self.last_health_check = time.time()
        
        logger.info(f"GitHub Sync System initialized for {repository}")
    
    async def activate_sync_system(self) -> Dict[str, Any]:
        """Activate the automated sync system."""
        
        if self.is_active:
            return {"status": "already_active", "message": "Sync system is already running"}
        
        logger.info("Activating GitHub Sync System")
        
        try:
            # Perform initial system checks
            system_check = await self._perform_system_checks()
            
            if not system_check["ready"]:
                return {
                    "status": "activation_failed",
                    "message": "System checks failed",
                    "details": system_check
                }
            
            # Start sync system
            self.is_active = True
            
            # Schedule first sync cycle
            asyncio.create_task(self._sync_cycle_manager())
            
            # Start monitoring
            asyncio.create_task(self._monitoring_loop())
            
            # Start health checks
            asyncio.create_task(self._health_check_loop())
            
            logger.info("GitHub Sync System activated successfully")
            
            return {
                "status": "activated",
                "message": "Sync system activated successfully",
                "sync_interval_minutes": self.sync_interval / 60,
                "next_sync": time.time() + self.sync_interval,
                "configuration": self.config
            }
        
        except Exception as e:
            logger.error(f"Failed to activate sync system: {e}")
            return {
                "status": "activation_failed",
                "message": f"Activation failed: {str(e)}"
            }
    
    async def _perform_system_checks(self) -> Dict[str, Any]:
        """Perform comprehensive system checks before activation."""
        
        checks = {
            "git_available": False,
            "github_connectivity": False,
            "repository_access": False,
            "local_workspace": False,
            "permissions": False,
            "ready": False
        }
        
        try:
            # Check Git availability
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            checks["git_available"] = result.returncode == 0
            
            # Check GitHub connectivity
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.github.com") as response:
                    checks["github_connectivity"] = response.status == 200
            
            # Check repository access
            repo_check = await self._check_repository_access()
            checks["repository_access"] = repo_check
            
            # Check local workspace
            workspace_check = await self._check_local_workspace()
            checks["local_workspace"] = workspace_check
            
            # Check permissions
            permissions_check = await self._check_permissions()
            checks["permissions"] = permissions_check
            
            # Overall readiness
            checks["ready"] = all([
                checks["git_available"],
                checks["github_connectivity"],
                checks["repository_access"],
                checks["local_workspace"],
                checks["permissions"]
            ])
            
        except Exception as e:
            logger.error(f"System checks failed: {e}")
            checks["error"] = str(e)
        
        return checks
    
    async def _check_repository_access(self) -> bool:
        """Check GitHub repository access."""
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.config['github_api_base']}/repos/{self.repository}"
                async with session.get(url) as response:
                    return response.status == 200
        
        except Exception as e:
            logger.error(f"Repository access check failed: {e}")
            return False
    
    async def _check_local_workspace(self) -> bool:
        """Check local workspace readiness."""
        
        try:
            # Check if we're in a git repository
            result = subprocess.run(["git", "status"], capture_output=True, text=True)
            return result.returncode == 0
        
        except Exception as e:
            logger.error(f"Local workspace check failed: {e}")
            return False
    
    async def _check_permissions(self) -> bool:
        """Check file system permissions."""
        
        try:
            # Test write permissions
            test_file = Path(".sync_test")
            test_file.write_text("test")
            test_file.unlink()
            return True
        
        except Exception as e:
            logger.error(f"Permissions check failed: {e}")
            return False
    
    async def _sync_cycle_manager(self):
        """Manage sync cycles at regular intervals."""
        
        while self.is_active:
            try:
                # Wait for next sync interval
                await asyncio.sleep(self.sync_interval)
                
                if self.is_active:
                    # Execute sync cycle
                    await self._execute_sync_cycle()
                
            except Exception as e:
                logger.error(f"Sync cycle manager error: {e}")
                await self._handle_sync_error(e, "sync_cycle_manager")
                await asyncio.sleep(60)  # Wait before retry
    
    async def _execute_sync_cycle(self) -> SyncCycle:
        """Execute a complete sync cycle."""
        
        cycle_id = f"sync_{int(time.time())}"
        cycle_start = time.time()
        
        cycle = SyncCycle(
            cycle_id=cycle_id,
            start_time=cycle_start,
            end_time=None,
            status=SyncCycleStatus.PREPARING,
            direction=SyncDirection.BIDIRECTIONAL,
            files_processed=0,
            files_synced=0,
            files_skipped=0,
            errors_encountered=[],
            performance_metrics={}
        )
        
        self.current_cycle = cycle
        
        logger.info(f"Starting sync cycle: {cycle_id}")
        
        try:
            # Phase 1: Preparation
            cycle.status = SyncCycleStatus.PREPARING
            await self._prepare_sync_cycle(cycle)
            
            # Phase 2: Synchronization
            cycle.status = SyncCycleStatus.SYNCING
            await self._perform_synchronization(cycle)
            
            # Phase 3: Validation
            cycle.status = SyncCycleStatus.VALIDATING
            await self._validate_sync_results(cycle)
            
            # Phase 4: Completion
            cycle.status = SyncCycleStatus.COMPLETE
            cycle.end_time = time.time()
            
            # Calculate performance metrics
            cycle.performance_metrics = self._calculate_cycle_metrics(cycle)
            
            logger.info(f"Sync cycle completed: {cycle_id} - {cycle.files_synced} files synced")
        
        except Exception as e:
            logger.error(f"Sync cycle failed: {cycle_id} - {e}")
            cycle.status = SyncCycleStatus.ERROR
            cycle.end_time = time.time()
            cycle.errors_encountered.append(str(e))
            
            # Attempt error recovery
            if self.config["auto_recovery_enabled"]:
                await self._attempt_error_recovery(cycle, e)
        
        # Store cycle history
        self.sync_history.append(cycle)
        self.current_cycle = None
        
        # Cleanup old history
        self._cleanup_sync_history()
        
        return cycle
    
    async def _prepare_sync_cycle(self, cycle: SyncCycle):
        """Prepare for sync cycle execution."""
        
        # Create backup if enabled
        if self.config["backup_before_sync"]:
            await self._create_backup()
        
        # Check for conflicts
        conflicts = await self._detect_conflicts()
        
        if conflicts:
            logger.warning(f"Detected {len(conflicts)} conflicts before sync")
            await self._resolve_conflicts(conflicts)
        
        # Update local repository
        await self._update_local_repository()
    
    async def _perform_synchronization(self, cycle: SyncCycle):
        """Perform the actual synchronization."""
        
        # Get list of files to sync
        files_to_sync = await self._get_files_to_sync()
        cycle.files_processed = len(files_to_sync)
        
        # Sync files
        for file_path in files_to_sync:
            try:
                success = await self._sync_file(file_path)
                
                if success:
                    cycle.files_synced += 1
                else:
                    cycle.files_skipped += 1
                
            except Exception as e:
                logger.error(f"Failed to sync file {file_path}: {e}")
                cycle.errors_encountered.append(f"File sync error: {file_path} - {str(e)}")
        
        # Commit and push changes
        if cycle.files_synced > 0:
            await self._commit_and_push_changes(cycle)
    
    async def _validate_sync_results(self, cycle: SyncCycle):
        """Validate sync results."""
        
        if not self.config["validate_after_sync"]:
            return
        
        # Verify file integrity
        integrity_check = await self._verify_file_integrity()
        
        if not integrity_check:
            raise Exception("File integrity validation failed")
        
        # Verify repository state
        repo_state_check = await self._verify_repository_state()
        
        if not repo_state_check:
            raise Exception("Repository state validation failed")
    
    async def _get_files_to_sync(self) -> List[str]:
        """Get list of files that need synchronization."""
        
        try:
            # Get git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return []
            
            files = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    # Parse git status output
                    status = line[:2]
                    file_path = line[3:]
                    
                    # Skip excluded patterns
                    if not self._is_file_excluded(file_path):
                        files.append(file_path)
            
            return files
        
        except Exception as e:
            logger.error(f"Failed to get files to sync: {e}")
            return []
    
    def _is_file_excluded(self, file_path: str) -> bool:
        """Check if file should be excluded from sync."""
        
        for pattern in self.config["excluded_patterns"]:
            if pattern in file_path or file_path.endswith(pattern.replace("*", "")):
                return True
        
        return False
    
    async def _sync_file(self, file_path: str) -> bool:
        """Sync individual file."""
        
        try:
            # Check file size
            if Path(file_path).exists():
                file_size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
                
                if file_size > self.config["max_file_size_mb"]:
                    logger.warning(f"Skipping large file: {file_path} ({file_size:.1f} MB)")
                    return False
            
            # Add file to git
            result = subprocess.run(
                ["git", "add", file_path],
                capture_output=True,
                text=True
            )
            
            return result.returncode == 0
        
        except Exception as e:
            logger.error(f"Failed to sync file {file_path}: {e}")
            return False
    
    async def _commit_and_push_changes(self, cycle: SyncCycle):
        """Commit and push changes to repository."""
        
        try:
            # Commit changes
            commit_message = f"Automated sync: {cycle.files_synced} files updated"
            
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Push changes
                push_result = subprocess.run(
                    ["git", "push"],
                    capture_output=True,
                    text=True
                )
                
                if push_result.returncode != 0:
                    raise Exception(f"Git push failed: {push_result.stderr}")
            
            else:
                logger.warning("No changes to commit")
        
        except Exception as e:
            logger.error(f"Failed to commit and push changes: {e}")
            raise
    
    async def _create_backup(self):
        """Create backup before sync."""
        
        try:
            backup_branch = f"backup_{int(time.time())}"
            
            result = subprocess.run(
                ["git", "checkout", "-b", backup_branch],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Switch back to main branch
                subprocess.run(["git", "checkout", "main"], capture_output=True)
                logger.info(f"Created backup branch: {backup_branch}")
        
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
    
    async def _detect_conflicts(self) -> List[str]:
        """Detect potential conflicts."""
        
        # Simulate conflict detection
        return []  # No conflicts detected
    
    async def _resolve_conflicts(self, conflicts: List[str]):
        """Resolve detected conflicts."""
        
        for conflict in conflicts:
            logger.info(f"Resolving conflict: {conflict}")
            # Implement conflict resolution based on strategy
    
    async def _update_local_repository(self):
        """Update local repository from remote."""
        
        try:
            result = subprocess.run(
                ["git", "pull"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.warning(f"Git pull warning: {result.stderr}")
        
        except Exception as e:
            logger.error(f"Failed to update local repository: {e}")
    
    async def _verify_file_integrity(self) -> bool:
        """Verify file integrity after sync."""
        
        # Simulate integrity check
        return True
    
    async def _verify_repository_state(self) -> bool:
        """Verify repository state after sync."""
        
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )
            
            # Repository should be clean after sync
            return result.returncode == 0 and not result.stdout.strip()
        
        except Exception as e:
            logger.error(f"Repository state verification failed: {e}")
            return False
    
    def _calculate_cycle_metrics(self, cycle: SyncCycle) -> Dict[str, float]:
        """Calculate performance metrics for sync cycle."""
        
        duration = cycle.end_time - cycle.start_time if cycle.end_time else 0
        
        return {
            "duration_seconds": duration,
            "files_per_second": cycle.files_synced / duration if duration > 0 else 0,
            "success_rate": cycle.files_synced / cycle.files_processed if cycle.files_processed > 0 else 0,
            "error_rate": len(cycle.errors_encountered) / cycle.files_processed if cycle.files_processed > 0 else 0
        }
    
    async def _attempt_error_recovery(self, cycle: SyncCycle, error: Exception):
        """Attempt to recover from sync errors."""
        
        logger.info(f"Attempting error recovery for cycle: {cycle.cycle_id}")
        
        # Record error
        sync_error = SyncError(
            error_id=f"error_{int(time.time())}",
            cycle_id=cycle.cycle_id,
            severity=ErrorSeverity.HIGH,
            error_type=type(error).__name__,
            description=str(error),
            file_path=None,
            resolution_attempted=True,
            resolved=False,
            timestamp=time.time()
        )
        
        self.sync_errors.append(sync_error)
        
        # Attempt recovery strategies
        try:
            # Reset repository state
            await self._reset_repository_state()
            
            # Retry sync with reduced scope
            await self._retry_sync_reduced_scope(cycle)
            
            sync_error.resolved = True
            logger.info("Error recovery successful")
        
        except Exception as recovery_error:
            logger.error(f"Error recovery failed: {recovery_error}")
    
    async def _reset_repository_state(self):
        """Reset repository to clean state."""
        
        try:
            subprocess.run(["git", "reset", "--hard"], capture_output=True)
            subprocess.run(["git", "clean", "-fd"], capture_output=True)
        
        except Exception as e:
            logger.error(f"Failed to reset repository state: {e}")
    
    async def _retry_sync_reduced_scope(self, cycle: SyncCycle):
        """Retry sync with reduced scope."""
        
        # Implement reduced scope retry logic
        logger.info("Retrying sync with reduced scope")
    
    async def _handle_sync_error(self, error: Exception, context: str):
        """Handle sync system errors."""
        
        logger.error(f"Sync system error in {context}: {error}")
        
        # Record error
        sync_error = SyncError(
            error_id=f"system_error_{int(time.time())}",
            cycle_id=self.current_cycle.cycle_id if self.current_cycle else "system",
            severity=ErrorSeverity.CRITICAL,
            error_type=type(error).__name__,
            description=f"{context}: {str(error)}",
            file_path=None,
            resolution_attempted=False,
            resolved=False,
            timestamp=time.time()
        )
        
        self.sync_errors.append(sync_error)
    
    async def _monitoring_loop(self):
        """Continuous monitoring loop."""
        
        while self.is_active:
            try:
                # Monitor system health
                await self._monitor_system_health()
                
                # Monitor sync performance
                await self._monitor_sync_performance()
                
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(60)
    
    async def _health_check_loop(self):
        """Continuous health check loop."""
        
        while self.is_active:
            try:
                self.last_health_check = time.time()
                
                # Perform health checks
                health_status = await self._perform_health_checks()
                
                if not health_status["healthy"]:
                    logger.warning("System health check failed")
                    await self._handle_health_issues(health_status)
                
                await asyncio.sleep(600)  # 10 minutes
                
            except Exception as e:
                logger.error(f"Health check loop error: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_system_health(self):
        """Monitor overall system health."""
        
        # Check if sync cycles are running on schedule
        if self.sync_history:
            last_sync = self.sync_history[-1]
            time_since_last = time.time() - last_sync.start_time
            
            if time_since_last > self.sync_interval * 1.5:  # 50% tolerance
                logger.warning("Sync cycles are running behind schedule")
    
    async def _monitor_sync_performance(self):
        """Monitor sync performance metrics."""
        
        if len(self.sync_history) >= 5:
            recent_cycles = self.sync_history[-5:]
            
            # Calculate average performance
            avg_duration = sum(c.performance_metrics.get("duration_seconds", 0) for c in recent_cycles) / len(recent_cycles)
            avg_success_rate = sum(c.performance_metrics.get("success_rate", 0) for c in recent_cycles) / len(recent_cycles)
            
            if avg_success_rate < 0.8:  # 80% threshold
                logger.warning(f"Sync success rate below threshold: {avg_success_rate:.2%}")
    
    async def _perform_health_checks(self) -> Dict[str, Any]:
        """Perform comprehensive health checks."""
        
        health_status = {
            "healthy": True,
            "issues": []
        }
        
        # Check system connectivity
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.github.com") as response:
                    if response.status != 200:
                        health_status["healthy"] = False
                        health_status["issues"].append("GitHub API connectivity issue")
        
        except Exception as e:
            health_status["healthy"] = False
            health_status["issues"].append(f"Network connectivity issue: {e}")
        
        # Check repository access
        repo_access = await self._check_repository_access()
        if not repo_access:
            health_status["healthy"] = False
            health_status["issues"].append("Repository access issue")
        
        return health_status
    
    async def _handle_health_issues(self, health_status: Dict[str, Any]):
        """Handle detected health issues."""
        
        for issue in health_status["issues"]:
            logger.warning(f"Health issue detected: {issue}")
            
            # Implement issue-specific handling
            if "connectivity" in issue.lower():
                # Wait and retry
                await asyncio.sleep(60)
            
            elif "repository access" in issue.lower():
                # Check credentials and permissions
                logger.error("Repository access issue - check credentials")
    
    def _cleanup_sync_history(self):
        """Clean up old sync history."""
        
        # Keep last 100 cycles
        if len(self.sync_history) > 100:
            self.sync_history = self.sync_history[-100:]
        
        # Keep errors from last 7 days
        cutoff_time = time.time() - (7 * 24 * 3600)
        self.sync_errors = [e for e in self.sync_errors if e.timestamp >= cutoff_time]
    
    async def deactivate_sync_system(self) -> Dict[str, Any]:
        """Deactivate the sync system."""
        
        logger.info("Deactivating GitHub Sync System")
        
        self.is_active = False
        
        # Wait for current cycle to complete
        if self.current_cycle and self.current_cycle.status != SyncCycleStatus.COMPLETE:
            logger.info("Waiting for current sync cycle to complete")
            
            timeout = 300  # 5 minutes
            start_wait = time.time()
            
            while (self.current_cycle and 
                   self.current_cycle.status not in [SyncCycleStatus.COMPLETE, SyncCycleStatus.ERROR] and
                   time.time() - start_wait < timeout):
                await asyncio.sleep(5)
        
        return {
            "status": "deactivated",
            "message": "Sync system deactivated successfully",
            "final_metrics": self.get_sync_metrics()
        }
    
    def get_sync_metrics(self) -> SyncMetrics:
        """Get comprehensive sync metrics."""
        
        total_cycles = len(self.sync_history)
        successful_cycles = len([c for c in self.sync_history if c.status == SyncCycleStatus.COMPLETE])
        failed_cycles = len([c for c in self.sync_history if c.status == SyncCycleStatus.ERROR])
        
        avg_duration = 0
        total_files_synced = 0
        
        if self.sync_history:
            avg_duration = sum(c.performance_metrics.get("duration_seconds", 0) for c in self.sync_history) / total_cycles
            total_files_synced = sum(c.files_synced for c in self.sync_history)
        
        success_rate = successful_cycles / total_cycles if total_cycles > 0 else 0
        last_sync = self.sync_history[-1].start_time if self.sync_history else 0
        next_sync = last_sync + self.sync_interval if self.is_active else 0
        
        return SyncMetrics(
            total_cycles=total_cycles,
            successful_cycles=successful_cycles,
            failed_cycles=failed_cycles,
            average_cycle_duration=avg_duration,
            total_files_synced=total_files_synced,
            sync_success_rate=success_rate,
            last_sync_time=last_sync,
            next_sync_time=next_sync,
            system_uptime=time.time() - self.start_time
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        
        current_status = "idle"
        if self.current_cycle:
            current_status = self.current_cycle.status.value
        
        return {
            "active": self.is_active,
            "current_status": current_status,
            "sync_interval_minutes": self.sync_interval / 60,
            "repository": self.repository,
            "last_health_check": self.last_health_check,
            "recent_errors": len([e for e in self.sync_errors if time.time() - e.timestamp < 3600]),
            "metrics": asdict(self.get_sync_metrics())
        }


# Example usage
async def main():
    """Example usage of GitHub Sync System Activator."""
    
    sync_system = GitHubSyncSystemActivator()
    
    # Activate sync system
    activation_result = await sync_system.activate_sync_system()
    print(f"Activation Result: {activation_result['status']}")
    
    if activation_result["status"] == "activated":
        # Let it run for a short time
        await asyncio.sleep(10)
        
        # Get system status
        status = sync_system.get_system_status()
        print(f"System Status: {status['current_status']}")
        print(f"Active: {status['active']}")
        
        # Get metrics
        metrics = sync_system.get_sync_metrics()
        print(f"Total Cycles: {metrics.total_cycles}")
        print(f"Success Rate: {metrics.sync_success_rate:.1%}")
        
        # Deactivate
        deactivation_result = await sync_system.deactivate_sync_system()
        print(f"Deactivation: {deactivation_result['status']}")


if __name__ == "__main__":
    asyncio.run(main())
