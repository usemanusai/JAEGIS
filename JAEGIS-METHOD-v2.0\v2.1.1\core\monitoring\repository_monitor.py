"""
Real-time Repository Monitoring System
Monitor GitHub repository state, detect changes, analyze current structure and content
"""

import asyncio
import aiohttp
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)


class ChangeType(str, Enum):
    """Types of repository changes."""
    FILE_ADDED = "file_added"
    FILE_MODIFIED = "file_modified"
    FILE_DELETED = "file_deleted"
    DIRECTORY_ADDED = "directory_added"
    DIRECTORY_DELETED = "directory_deleted"
    BRANCH_CREATED = "branch_created"
    BRANCH_DELETED = "branch_deleted"
    COMMIT_PUSHED = "commit_pushed"


class MonitoringStatus(str, Enum):
    """Repository monitoring status."""
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    INITIALIZING = "initializing"


@dataclass
class RepositoryChange:
    """Repository change detection."""
    change_id: str
    change_type: ChangeType
    file_path: str
    branch: str
    commit_sha: str
    author: str
    timestamp: float
    details: Dict[str, Any]


@dataclass
class RepositorySnapshot:
    """Repository state snapshot."""
    snapshot_id: str
    repository: str
    branch: str
    commit_sha: str
    file_count: int
    directory_count: int
    total_size_bytes: int
    file_structure: Dict[str, Any]
    timestamp: float


@dataclass
class MonitoringMetrics:
    """Repository monitoring metrics."""
    total_changes_detected: int
    changes_by_type: Dict[str, int]
    monitoring_uptime_hours: float
    last_check_timestamp: float
    average_check_duration_ms: float
    error_count: int


class RepositoryMonitor:
    """
    Real-time Repository Monitoring System
    
    Monitors GitHub repository for:
    - File and directory changes
    - Branch operations
    - Commit activity
    - Structure modifications
    - Content updates
    """
    
    def __init__(self, repository: str = "usemanusai/JAEGIS", github_token: Optional[str] = None):
        self.repository = repository
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        
        # Monitoring state
        self.status = MonitoringStatus.INITIALIZING
        self.current_snapshot: Optional[RepositorySnapshot] = None
        self.previous_snapshot: Optional[RepositorySnapshot] = None
        self.detected_changes: List[RepositoryChange] = []
        
        # Configuration
        self.config = {
            "monitoring_interval": 300,  # 5 minutes
            "max_changes_history": 1000,
            "snapshot_retention": 24,    # 24 snapshots
            "change_detection_enabled": True,
            "webhook_notifications": True,
            "detailed_file_analysis": True
        }
        
        # Metrics
        self.metrics = MonitoringMetrics(
            total_changes_detected=0,
            changes_by_type=defaultdict(int),
            monitoring_uptime_hours=0.0,
            last_check_timestamp=0.0,
            average_check_duration_ms=0.0,
            error_count=0
        )
        
        # Start monitoring
        self.start_time = time.time()
        asyncio.create_task(self._monitoring_loop())
        
        logger.info(f"Repository Monitor initialized for {repository}")
    
    async def _monitoring_loop(self):
        """Main monitoring loop."""
        
        self.status = MonitoringStatus.ACTIVE
        
        while self.status == MonitoringStatus.ACTIVE:
            try:
                check_start = time.time()
                
                # Create repository snapshot
                snapshot = await self._create_repository_snapshot()
                
                # Detect changes if we have a previous snapshot
                if self.previous_snapshot:
                    changes = await self._detect_changes(self.previous_snapshot, snapshot)
                    
                    if changes:
                        self.detected_changes.extend(changes)
                        self.metrics.total_changes_detected += len(changes)
                        
                        for change in changes:
                            self.metrics.changes_by_type[change.change_type.value] += 1
                        
                        logger.info(f"Detected {len(changes)} repository changes")
                        
                        # Process changes
                        await self._process_changes(changes)
                
                # Update snapshots
                self.previous_snapshot = self.current_snapshot
                self.current_snapshot = snapshot
                
                # Update metrics
                check_duration = (time.time() - check_start) * 1000
                self.metrics.last_check_timestamp = time.time()
                self.metrics.average_check_duration_ms = (
                    (self.metrics.average_check_duration_ms + check_duration) / 2
                    if self.metrics.average_check_duration_ms > 0 else check_duration
                )
                self.metrics.monitoring_uptime_hours = (time.time() - self.start_time) / 3600
                
                # Cleanup old changes
                self._cleanup_old_changes()
                
                await asyncio.sleep(self.config["monitoring_interval"])
                
            except Exception as e:
                logger.error(f"Repository monitoring error: {e}")
                self.metrics.error_count += 1
                self.status = MonitoringStatus.ERROR
                await asyncio.sleep(60)  # Wait before retry
                self.status = MonitoringStatus.ACTIVE
    
    async def _create_repository_snapshot(self) -> RepositorySnapshot:
        """Create a snapshot of current repository state."""
        
        snapshot_id = f"snapshot_{int(time.time())}"
        
        try:
            # Get repository information
            repo_info = await self._get_repository_info()
            
            # Get file structure
            file_structure = await self._get_file_structure()
            
            # Calculate metrics
            file_count = self._count_files(file_structure)
            directory_count = self._count_directories(file_structure)
            total_size = self._calculate_total_size(file_structure)
            
            snapshot = RepositorySnapshot(
                snapshot_id=snapshot_id,
                repository=self.repository,
                branch=repo_info.get("default_branch", "main"),
                commit_sha=repo_info.get("commit_sha", ""),
                file_count=file_count,
                directory_count=directory_count,
                total_size_bytes=total_size,
                file_structure=file_structure,
                timestamp=time.time()
            )
            
            logger.debug(f"Created repository snapshot: {file_count} files, {directory_count} directories")
            
            return snapshot
            
        except Exception as e:
            logger.error(f"Failed to create repository snapshot: {e}")
            raise
    
    async def _get_repository_info(self) -> Dict[str, Any]:
        """Get basic repository information."""
        
        url = f"{self.base_url}/repos/{self.repository}"
        headers = {}
        
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    repo_data = await response.json()
                    
                    # Get latest commit SHA
                    commits_url = f"{self.base_url}/repos/{self.repository}/commits"
                    async with session.get(commits_url, headers=headers) as commits_response:
                        if commits_response.status == 200:
                            commits_data = await commits_response.json()
                            latest_commit = commits_data[0] if commits_data else {}
                            repo_data["commit_sha"] = latest_commit.get("sha", "")
                    
                    return repo_data
                else:
                    raise Exception(f"Failed to get repository info: {response.status}")
    
    async def _get_file_structure(self, path: str = "") -> Dict[str, Any]:
        """Get repository file structure recursively."""
        
        url = f"{self.base_url}/repos/{self.repository}/contents/{path}"
        headers = {}
        
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        structure = {}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        contents = await response.json()
                        
                        for item in contents:
                            item_name = item["name"]
                            item_path = item["path"]
                            
                            if item["type"] == "file":
                                structure[item_name] = {
                                    "type": "file",
                                    "path": item_path,
                                    "size": item["size"],
                                    "sha": item["sha"],
                                    "download_url": item.get("download_url")
                                }
                            
                            elif item["type"] == "dir":
                                # Recursively get subdirectory contents
                                subdirectory = await self._get_file_structure(item_path)
                                structure[item_name] = {
                                    "type": "directory",
                                    "path": item_path,
                                    "contents": subdirectory
                                }
                    
                    elif response.status == 404:
                        logger.warning(f"Path not found: {path}")
                    
                    else:
                        logger.error(f"Failed to get contents for {path}: {response.status}")
        
        except Exception as e:
            logger.error(f"Error getting file structure for {path}: {e}")
        
        return structure
    
    def _count_files(self, structure: Dict[str, Any]) -> int:
        """Count total files in structure."""
        
        count = 0
        
        for item in structure.values():
            if item.get("type") == "file":
                count += 1
            elif item.get("type") == "directory":
                count += self._count_files(item.get("contents", {}))
        
        return count
    
    def _count_directories(self, structure: Dict[str, Any]) -> int:
        """Count total directories in structure."""
        
        count = 0
        
        for item in structure.values():
            if item.get("type") == "directory":
                count += 1
                count += self._count_directories(item.get("contents", {}))
        
        return count
    
    def _calculate_total_size(self, structure: Dict[str, Any]) -> int:
        """Calculate total size of all files."""
        
        total_size = 0
        
        for item in structure.values():
            if item.get("type") == "file":
                total_size += item.get("size", 0)
            elif item.get("type") == "directory":
                total_size += self._calculate_total_size(item.get("contents", {}))
        
        return total_size
    
    async def _detect_changes(self, previous: RepositorySnapshot, current: RepositorySnapshot) -> List[RepositoryChange]:
        """Detect changes between repository snapshots."""
        
        changes = []
        
        # Check for commit changes
        if previous.commit_sha != current.commit_sha:
            change = RepositoryChange(
                change_id=f"commit_{int(time.time())}",
                change_type=ChangeType.COMMIT_PUSHED,
                file_path="",
                branch=current.branch,
                commit_sha=current.commit_sha,
                author="unknown",  # Would need additional API call to get author
                timestamp=time.time(),
                details={
                    "previous_sha": previous.commit_sha,
                    "current_sha": current.commit_sha
                }
            )
            changes.append(change)
        
        # Detect file structure changes
        file_changes = self._detect_file_changes(
            previous.file_structure, 
            current.file_structure,
            current.branch,
            current.commit_sha
        )
        changes.extend(file_changes)
        
        return changes
    
    def _detect_file_changes(self, previous_structure: Dict[str, Any], 
                           current_structure: Dict[str, Any],
                           branch: str, commit_sha: str, 
                           base_path: str = "") -> List[RepositoryChange]:
        """Detect file and directory changes."""
        
        changes = []
        
        # Get all paths from both structures
        previous_items = set(previous_structure.keys())
        current_items = set(current_structure.keys())
        
        # Detect added items
        added_items = current_items - previous_items
        for item_name in added_items:
            item = current_structure[item_name]
            item_path = f"{base_path}/{item_name}".lstrip("/")
            
            change_type = ChangeType.FILE_ADDED if item["type"] == "file" else ChangeType.DIRECTORY_ADDED
            
            change = RepositoryChange(
                change_id=f"add_{hashlib.md5(item_path.encode()).hexdigest()[:8]}",
                change_type=change_type,
                file_path=item_path,
                branch=branch,
                commit_sha=commit_sha,
                author="unknown",
                timestamp=time.time(),
                details={
                    "item_type": item["type"],
                    "size": item.get("size", 0) if item["type"] == "file" else 0
                }
            )
            changes.append(change)
        
        # Detect deleted items
        deleted_items = previous_items - current_items
        for item_name in deleted_items:
            item = previous_structure[item_name]
            item_path = f"{base_path}/{item_name}".lstrip("/")
            
            change_type = ChangeType.FILE_DELETED if item["type"] == "file" else ChangeType.DIRECTORY_DELETED
            
            change = RepositoryChange(
                change_id=f"del_{hashlib.md5(item_path.encode()).hexdigest()[:8]}",
                change_type=change_type,
                file_path=item_path,
                branch=branch,
                commit_sha=commit_sha,
                author="unknown",
                timestamp=time.time(),
                details={
                    "item_type": item["type"],
                    "previous_size": item.get("size", 0) if item["type"] == "file" else 0
                }
            )
            changes.append(change)
        
        # Detect modified items
        common_items = previous_items & current_items
        for item_name in common_items:
            previous_item = previous_structure[item_name]
            current_item = current_structure[item_name]
            item_path = f"{base_path}/{item_name}".lstrip("/")
            
            if previous_item["type"] == "file" and current_item["type"] == "file":
                # Check if file was modified (SHA changed)
                if previous_item.get("sha") != current_item.get("sha"):
                    change = RepositoryChange(
                        change_id=f"mod_{hashlib.md5(item_path.encode()).hexdigest()[:8]}",
                        change_type=ChangeType.FILE_MODIFIED,
                        file_path=item_path,
                        branch=branch,
                        commit_sha=commit_sha,
                        author="unknown",
                        timestamp=time.time(),
                        details={
                            "previous_sha": previous_item.get("sha"),
                            "current_sha": current_item.get("sha"),
                            "previous_size": previous_item.get("size", 0),
                            "current_size": current_item.get("size", 0)
                        }
                    )
                    changes.append(change)
            
            elif previous_item["type"] == "directory" and current_item["type"] == "directory":
                # Recursively check subdirectory
                subdirectory_changes = self._detect_file_changes(
                    previous_item.get("contents", {}),
                    current_item.get("contents", {}),
                    branch,
                    commit_sha,
                    item_path
                )
                changes.extend(subdirectory_changes)
        
        return changes
    
    async def _process_changes(self, changes: List[RepositoryChange]):
        """Process detected repository changes."""
        
        for change in changes:
            logger.info(f"Processing change: {change.change_type.value} - {change.file_path}")
            
            # Trigger appropriate actions based on change type
            if change.change_type == ChangeType.FILE_ADDED:
                await self._handle_file_added(change)
            
            elif change.change_type == ChangeType.FILE_MODIFIED:
                await self._handle_file_modified(change)
            
            elif change.change_type == ChangeType.FILE_DELETED:
                await self._handle_file_deleted(change)
            
            elif change.change_type == ChangeType.COMMIT_PUSHED:
                await self._handle_commit_pushed(change)
            
            # Send notifications if enabled
            if self.config["webhook_notifications"]:
                await self._send_change_notification(change)
    
    async def _handle_file_added(self, change: RepositoryChange):
        """Handle file addition."""
        logger.debug(f"File added: {change.file_path}")
        # Implement specific handling for file additions
    
    async def _handle_file_modified(self, change: RepositoryChange):
        """Handle file modification."""
        logger.debug(f"File modified: {change.file_path}")
        # Implement specific handling for file modifications
    
    async def _handle_file_deleted(self, change: RepositoryChange):
        """Handle file deletion."""
        logger.debug(f"File deleted: {change.file_path}")
        # Implement specific handling for file deletions
    
    async def _handle_commit_pushed(self, change: RepositoryChange):
        """Handle new commit."""
        logger.debug(f"New commit: {change.commit_sha}")
        # Implement specific handling for new commits
    
    async def _send_change_notification(self, change: RepositoryChange):
        """Send notification about repository change."""
        # Implement webhook or notification system
        logger.debug(f"Notification sent for change: {change.change_id}")
    
    def _cleanup_old_changes(self):
        """Clean up old change records."""
        
        if len(self.detected_changes) > self.config["max_changes_history"]:
            # Keep only the most recent changes
            self.detected_changes = self.detected_changes[-self.config["max_changes_history"]:]
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status and metrics."""
        
        recent_changes = [
            change for change in self.detected_changes
            if time.time() - change.timestamp < 3600  # Last hour
        ]
        
        return {
            "status": self.status.value,
            "repository": self.repository,
            "monitoring_uptime_hours": self.metrics.monitoring_uptime_hours,
            "total_changes_detected": self.metrics.total_changes_detected,
            "recent_changes": len(recent_changes),
            "changes_by_type": dict(self.metrics.changes_by_type),
            "last_check": self.metrics.last_check_timestamp,
            "average_check_duration_ms": self.metrics.average_check_duration_ms,
            "error_count": self.metrics.error_count,
            "current_snapshot": {
                "file_count": self.current_snapshot.file_count if self.current_snapshot else 0,
                "directory_count": self.current_snapshot.directory_count if self.current_snapshot else 0,
                "total_size_mb": (self.current_snapshot.total_size_bytes / 1024 / 1024) if self.current_snapshot else 0
            }
        }
    
    def get_recent_changes(self, hours: int = 24) -> List[RepositoryChange]:
        """Get recent repository changes."""
        
        cutoff_time = time.time() - (hours * 3600)
        
        return [
            change for change in self.detected_changes
            if change.timestamp >= cutoff_time
        ]
    
    def pause_monitoring(self):
        """Pause repository monitoring."""
        self.status = MonitoringStatus.PAUSED
        logger.info("Repository monitoring paused")
    
    def resume_monitoring(self):
        """Resume repository monitoring."""
        if self.status == MonitoringStatus.PAUSED:
            self.status = MonitoringStatus.ACTIVE
            logger.info("Repository monitoring resumed")
    
    async def force_check(self) -> List[RepositoryChange]:
        """Force an immediate repository check."""
        
        logger.info("Forcing repository check")
        
        # Create new snapshot
        snapshot = await self._create_repository_snapshot()
        
        changes = []
        if self.current_snapshot:
            changes = await self._detect_changes(self.current_snapshot, snapshot)
            
            if changes:
                self.detected_changes.extend(changes)
                await self._process_changes(changes)
        
        # Update current snapshot
        self.previous_snapshot = self.current_snapshot
        self.current_snapshot = snapshot
        
        return changes


# Example usage
async def main():
    """Example usage of Repository Monitor."""
    
    monitor = RepositoryMonitor("usemanusai/JAEGIS")
    
    # Wait for initial monitoring
    await asyncio.sleep(10)
    
    # Get monitoring status
    status = monitor.get_monitoring_status()
    print(f"Monitoring Status:")
    print(f"  Repository: {status['repository']}")
    print(f"  Status: {status['status']}")
    print(f"  Uptime: {status['monitoring_uptime_hours']:.2f} hours")
    print(f"  Total changes: {status['total_changes_detected']}")
    print(f"  Files: {status['current_snapshot']['file_count']}")
    print(f"  Directories: {status['current_snapshot']['directory_count']}")
    print(f"  Size: {status['current_snapshot']['total_size_mb']:.2f} MB")
    
    # Force a check
    changes = await monitor.force_check()
    print(f"Force check detected {len(changes)} changes")
    
    # Get recent changes
    recent_changes = monitor.get_recent_changes(1)  # Last hour
    print(f"Recent changes: {len(recent_changes)}")
    
    for change in recent_changes[:5]:  # Show first 5
        print(f"  {change.change_type.value}: {change.file_path}")


if __name__ == "__main__":
    asyncio.run(main())
