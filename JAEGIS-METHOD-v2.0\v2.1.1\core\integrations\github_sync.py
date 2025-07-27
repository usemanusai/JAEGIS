"""
GitHub Sync System for JAEGIS Enhanced Agent System
Automated synchronization with usemanusai/JAEGIS repository for dynamic resource fetching
"""

import asyncio
import aiohttp
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import base64
import hashlib
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


class SyncStatus(str, Enum):
    """Synchronization status."""
    SYNCED = "synced"
    PENDING = "pending"
    SYNCING = "syncing"
    ERROR = "error"
    CONFLICT = "conflict"


class ResourceType(str, Enum):
    """Types of resources to sync."""
    COMMANDS = "commands"
    TEMPLATES = "templates"
    CONFIGS = "configs"
    DOCUMENTATION = "documentation"
    AGENT_CONFIGS = "agent_configs"
    SQUAD_DEFINITIONS = "squad_definitions"


class SyncMode(str, Enum):
    """Synchronization modes."""
    AUTOMATIC = "automatic"      # Auto-sync on changes
    SCHEDULED = "scheduled"      # Scheduled sync intervals
    MANUAL = "manual"           # Manual sync only
    REAL_TIME = "real_time"     # Real-time webhook sync


@dataclass
class GitHubResource:
    """GitHub resource representation."""
    resource_id: str
    resource_type: ResourceType
    file_path: str
    content: str
    sha: str
    last_modified: str
    size: int
    local_path: str
    sync_status: SyncStatus


@dataclass
class SyncOperation:
    """Synchronization operation."""
    operation_id: str
    operation_type: str  # fetch, update, create, delete
    resource_path: str
    status: SyncStatus
    started_at: float
    completed_at: Optional[float]
    error_message: Optional[str]
    changes_detected: List[str]


@dataclass
class SyncResult:
    """Synchronization result."""
    success: bool
    operations: List[SyncOperation]
    resources_synced: int
    resources_updated: int
    resources_created: int
    resources_deleted: int
    sync_duration_ms: float
    errors: List[str]
    warnings: List[str]


class GitHubSyncSystem:
    """
    GitHub Sync System for automated synchronization with usemanusai/JAEGIS repository.
    
    Features:
    - Dynamic resource fetching from GitHub
    - Automated sync with change detection
    - Real-time webhook integration
    - Conflict resolution
    - Local caching and optimization
    """
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.repository = "usemanusai/JAEGIS"
        self.base_url = "https://api.github.com"
        
        # Configuration
        self.config = {
            "sync_interval": 300,        # 5 minutes
            "max_file_size": 10485760,   # 10MB
            "cache_duration": 3600,      # 1 hour
            "retry_attempts": 3,
            "webhook_secret": None,
            "local_cache_dir": "cache/github",
            "sync_patterns": [
                "core/agent-config.txt",
                "commands/**/*.yaml",
                "templates/**/*.json",
                "config/**/*.yaml",
                "docs/**/*.md"
            ]
        }
        
        # State management
        self.resources: Dict[str, GitHubResource] = {}
        self.sync_operations: List[SyncOperation] = []
        self.last_sync_time = 0.0
        self.sync_mode = SyncMode.AUTOMATIC
        
        # Initialize local cache
        self._initialize_cache()
        
        # Start background sync if automatic mode
        if self.sync_mode == SyncMode.AUTOMATIC:
            asyncio.create_task(self._background_sync())
        
        logger.info(f"GitHub Sync System initialized for {self.repository}")
    
    def _initialize_cache(self):
        """Initialize local cache directory."""
        
        cache_dir = Path(self.config["local_cache_dir"])
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different resource types
        for resource_type in ResourceType:
            (cache_dir / resource_type.value).mkdir(exist_ok=True)
    
    async def sync_repository(self, 
                            force: bool = False,
                            specific_paths: Optional[List[str]] = None) -> SyncResult:
        """Synchronize with GitHub repository."""
        
        start_time = time.time()
        operations = []
        errors = []
        warnings = []
        
        try:
            # Check if sync is needed
            if not force and time.time() - self.last_sync_time < self.config["sync_interval"]:
                return SyncResult(
                    success=True,
                    operations=[],
                    resources_synced=0,
                    resources_updated=0,
                    resources_created=0,
                    resources_deleted=0,
                    sync_duration_ms=0.0,
                    errors=[],
                    warnings=["Sync skipped - too recent"]
                )
            
            # Get repository contents
            if specific_paths:
                contents = []
                for path in specific_paths:
                    try:
                        content = await self._fetch_file_content(path)
                        if content:
                            contents.append(content)
                    except Exception as e:
                        errors.append(f"Failed to fetch {path}: {str(e)}")
            else:
                contents = await self._fetch_repository_contents()
            
            # Process each resource
            for content_info in contents:
                try:
                    operation = await self._process_resource(content_info)
                    if operation:
                        operations.append(operation)
                except Exception as e:
                    errors.append(f"Failed to process {content_info.get('path', 'unknown')}: {str(e)}")
            
            # Update sync time
            self.last_sync_time = time.time()
            
            # Calculate statistics
            resources_synced = len([op for op in operations if op.status == SyncStatus.SYNCED])
            resources_updated = len([op for op in operations if op.operation_type == "update"])
            resources_created = len([op for op in operations if op.operation_type == "create"])
            resources_deleted = len([op for op in operations if op.operation_type == "delete"])
            
            sync_duration = (time.time() - start_time) * 1000
            
            logger.info(f"Sync completed: {resources_synced} resources synced in {sync_duration:.2f}ms")
            
            return SyncResult(
                success=len(errors) == 0,
                operations=operations,
                resources_synced=resources_synced,
                resources_updated=resources_updated,
                resources_created=resources_created,
                resources_deleted=resources_deleted,
                sync_duration_ms=sync_duration,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            error_message = f"Sync failed: {str(e)}"
            logger.error(error_message)
            
            return SyncResult(
                success=False,
                operations=operations,
                resources_synced=0,
                resources_updated=0,
                resources_created=0,
                resources_deleted=0,
                sync_duration_ms=(time.time() - start_time) * 1000,
                errors=[error_message],
                warnings=warnings
            )
    
    async def _fetch_repository_contents(self) -> List[Dict[str, Any]]:
        """Fetch repository contents from GitHub API."""
        
        contents = []
        
        # Fetch contents recursively
        for pattern in self.config["sync_patterns"]:
            try:
                if "**" in pattern:
                    # Handle recursive patterns
                    base_path = pattern.split("**")[0].rstrip("/")
                    recursive_contents = await self._fetch_recursive_contents(base_path)
                    contents.extend(recursive_contents)
                else:
                    # Handle specific files
                    file_content = await self._fetch_file_content(pattern)
                    if file_content:
                        contents.append(file_content)
            except Exception as e:
                logger.warning(f"Failed to fetch pattern {pattern}: {e}")
        
        return contents
    
    async def _fetch_recursive_contents(self, path: str) -> List[Dict[str, Any]]:
        """Fetch contents recursively from a directory."""
        
        contents = []
        
        try:
            url = f"{self.base_url}/repos/{self.repository}/contents/{path}"
            headers = {}
            
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        items = await response.json()
                        
                        for item in items:
                            if item["type"] == "file":
                                contents.append(item)
                            elif item["type"] == "dir":
                                # Recursively fetch subdirectory contents
                                sub_contents = await self._fetch_recursive_contents(item["path"])
                                contents.extend(sub_contents)
                    
                    elif response.status == 404:
                        logger.warning(f"Path not found: {path}")
                    else:
                        logger.error(f"Failed to fetch {path}: {response.status}")
        
        except Exception as e:
            logger.error(f"Error fetching recursive contents for {path}: {e}")
        
        return contents
    
    async def _fetch_file_content(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Fetch specific file content from GitHub."""
        
        try:
            url = f"{self.base_url}/repos/{self.repository}/contents/{file_path}"
            headers = {}
            
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        logger.warning(f"File not found: {file_path}")
                        return None
                    else:
                        logger.error(f"Failed to fetch {file_path}: {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"Error fetching file {file_path}: {e}")
            return None
    
    async def _process_resource(self, content_info: Dict[str, Any]) -> Optional[SyncOperation]:
        """Process a single resource for synchronization."""
        
        file_path = content_info["path"]
        sha = content_info["sha"]
        size = content_info["size"]
        
        # Skip large files
        if size > self.config["max_file_size"]:
            logger.warning(f"Skipping large file: {file_path} ({size} bytes)")
            return None
        
        # Determine resource type
        resource_type = self._determine_resource_type(file_path)
        
        # Generate resource ID
        resource_id = hashlib.md5(file_path.encode()).hexdigest()
        
        # Check if resource exists and needs update
        existing_resource = self.resources.get(resource_id)
        
        operation_type = "create"
        if existing_resource:
            if existing_resource.sha == sha:
                # No changes needed
                return None
            operation_type = "update"
        
        # Create sync operation
        operation = SyncOperation(
            operation_id=f"sync_{int(time.time())}_{resource_id[:8]}",
            operation_type=operation_type,
            resource_path=file_path,
            status=SyncStatus.SYNCING,
            started_at=time.time(),
            completed_at=None,
            error_message=None,
            changes_detected=[]
        )
        
        try:
            # Fetch file content
            if content_info.get("content"):
                # Content is already included (base64 encoded)
                content = base64.b64decode(content_info["content"]).decode("utf-8")
            else:
                # Need to fetch content separately
                file_data = await self._fetch_file_content(file_path)
                if not file_data or not file_data.get("content"):
                    raise Exception("Failed to fetch file content")
                content = base64.b64decode(file_data["content"]).decode("utf-8")
            
            # Create local path
            local_path = Path(self.config["local_cache_dir"]) / resource_type.value / Path(file_path).name
            
            # Save to local cache
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Create/update resource
            resource = GitHubResource(
                resource_id=resource_id,
                resource_type=resource_type,
                file_path=file_path,
                content=content,
                sha=sha,
                last_modified=content_info.get("last_modified", ""),
                size=size,
                local_path=str(local_path),
                sync_status=SyncStatus.SYNCED
            )
            
            # Detect changes if updating
            if existing_resource:
                changes = self._detect_changes(existing_resource, resource)
                operation.changes_detected = changes
            
            # Update resource registry
            self.resources[resource_id] = resource
            
            # Complete operation
            operation.status = SyncStatus.SYNCED
            operation.completed_at = time.time()
            
            logger.debug(f"Successfully synced: {file_path}")
            
        except Exception as e:
            operation.status = SyncStatus.ERROR
            operation.error_message = str(e)
            operation.completed_at = time.time()
            
            logger.error(f"Failed to sync {file_path}: {e}")
        
        return operation
    
    def _determine_resource_type(self, file_path: str) -> ResourceType:
        """Determine resource type based on file path."""
        
        path_lower = file_path.lower()
        
        if "commands" in path_lower:
            return ResourceType.COMMANDS
        elif "templates" in path_lower:
            return ResourceType.TEMPLATES
        elif "config" in path_lower:
            return ResourceType.CONFIGS
        elif "docs" in path_lower or "documentation" in path_lower:
            return ResourceType.DOCUMENTATION
        elif "agent-config" in path_lower:
            return ResourceType.AGENT_CONFIGS
        elif "squad" in path_lower:
            return ResourceType.SQUAD_DEFINITIONS
        else:
            return ResourceType.CONFIGS  # Default
    
    def _detect_changes(self, old_resource: GitHubResource, new_resource: GitHubResource) -> List[str]:
        """Detect changes between old and new resource versions."""
        
        changes = []
        
        if old_resource.content != new_resource.content:
            changes.append("content_modified")
        
        if old_resource.size != new_resource.size:
            changes.append(f"size_changed_{old_resource.size}_to_{new_resource.size}")
        
        if old_resource.last_modified != new_resource.last_modified:
            changes.append("timestamp_updated")
        
        return changes
    
    async def _background_sync(self):
        """Background synchronization task."""
        
        while True:
            try:
                if self.sync_mode == SyncMode.AUTOMATIC:
                    await self.sync_repository()
                
                await asyncio.sleep(self.config["sync_interval"])
                
            except Exception as e:
                logger.error(f"Background sync error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    async def get_resource(self, resource_path: str) -> Optional[GitHubResource]:
        """Get a specific resource by path."""
        
        # Try to find in local cache first
        for resource in self.resources.values():
            if resource.file_path == resource_path:
                return resource
        
        # If not found, try to fetch from GitHub
        try:
            content_info = await self._fetch_file_content(resource_path)
            if content_info:
                operation = await self._process_resource(content_info)
                if operation and operation.status == SyncStatus.SYNCED:
                    # Find the newly created resource
                    for resource in self.resources.values():
                        if resource.file_path == resource_path:
                            return resource
        except Exception as e:
            logger.error(f"Failed to fetch resource {resource_path}: {e}")
        
        return None
    
    async def get_resources_by_type(self, resource_type: ResourceType) -> List[GitHubResource]:
        """Get all resources of a specific type."""
        
        return [
            resource for resource in self.resources.values()
            if resource.resource_type == resource_type
        ]
    
    def set_sync_mode(self, mode: SyncMode):
        """Set synchronization mode."""
        
        self.sync_mode = mode
        logger.info(f"Sync mode set to: {mode.value}")
        
        if mode == SyncMode.AUTOMATIC:
            asyncio.create_task(self._background_sync())
    
    async def webhook_handler(self, payload: Dict[str, Any]) -> bool:
        """Handle GitHub webhook events."""
        
        try:
            # Verify webhook signature if secret is configured
            if self.config["webhook_secret"]:
                # TODO: Implement webhook signature verification
                pass
            
            # Process push events
            if payload.get("action") == "push":
                modified_files = []
                
                for commit in payload.get("commits", []):
                    modified_files.extend(commit.get("modified", []))
                    modified_files.extend(commit.get("added", []))
                
                # Filter files that match sync patterns
                relevant_files = []
                for file_path in modified_files:
                    for pattern in self.config["sync_patterns"]:
                        if self._matches_pattern(file_path, pattern):
                            relevant_files.append(file_path)
                            break
                
                # Sync relevant files
                if relevant_files:
                    await self.sync_repository(specific_paths=relevant_files)
                    return True
            
        except Exception as e:
            logger.error(f"Webhook handler error: {e}")
        
        return False
    
    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if file path matches sync pattern."""
        
        # Simple pattern matching (could be enhanced with fnmatch or regex)
        if "**" in pattern:
            base_path = pattern.split("**")[0].rstrip("/")
            return file_path.startswith(base_path)
        else:
            return file_path == pattern
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get synchronization statistics."""
        
        total_resources = len(self.resources)
        synced_resources = len([r for r in self.resources.values() if r.sync_status == SyncStatus.SYNCED])
        error_resources = len([r for r in self.resources.values() if r.sync_status == SyncStatus.ERROR])
        
        recent_operations = [op for op in self.sync_operations if time.time() - op.started_at < 3600]
        successful_operations = len([op for op in recent_operations if op.status == SyncStatus.SYNCED])
        
        return {
            "total_resources": total_resources,
            "synced_resources": synced_resources,
            "error_resources": error_resources,
            "sync_success_rate": synced_resources / total_resources if total_resources > 0 else 0,
            "last_sync_time": self.last_sync_time,
            "sync_mode": self.sync_mode.value,
            "recent_operations": len(recent_operations),
            "recent_success_rate": successful_operations / len(recent_operations) if recent_operations else 0,
            "repository": self.repository
        }


# Example usage
async def main():
    """Example usage of GitHub Sync System."""
    
    # Initialize sync system
    sync_system = GitHubSyncSystem()
    
    # Perform initial sync
    result = await sync_system.sync_repository()
    
    print(f"Sync completed: {result.success}")
    print(f"Resources synced: {result.resources_synced}")
    print(f"Duration: {result.sync_duration_ms:.2f}ms")
    
    if result.errors:
        print(f"Errors: {result.errors}")
    
    # Get specific resource
    agent_config = await sync_system.get_resource("core/agent-config.txt")
    if agent_config:
        print(f"Agent config found: {len(agent_config.content)} characters")
    
    # Get statistics
    stats = sync_system.get_sync_statistics()
    print(f"Total resources: {stats['total_resources']}")
    print(f"Success rate: {stats['sync_success_rate']:.2%}")


if __name__ == "__main__":
    asyncio.run(main())
