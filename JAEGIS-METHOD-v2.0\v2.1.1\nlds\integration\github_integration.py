"""
N.L.D.S. GitHub Integration Interface
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Interface with GitHub integration system for dynamic resource fetching,
synchronization, and real-time access to JAEGIS repository resources.
"""

import asyncio
import aiohttp
import json
import base64
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import hashlib
from urllib.parse import urljoin

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# GITHUB INTEGRATION STRUCTURES AND ENUMS
# ============================================================================

class ResourceType(Enum):
    """Types of GitHub resources."""
    AGENT_CONFIG = "agent_config"
    COMMAND_TEMPLATE = "command_template"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    SCHEMA = "schema"
    WORKFLOW = "workflow"
    SCRIPT = "script"
    DATA = "data"


class SyncStatus(Enum):
    """Synchronization status."""
    SYNCED = "synced"
    OUT_OF_SYNC = "out_of_sync"
    SYNCING = "syncing"
    ERROR = "error"
    UNKNOWN = "unknown"


class CacheStrategy(Enum):
    """Caching strategies for GitHub resources."""
    ALWAYS_FRESH = "always_fresh"
    CACHE_FIRST = "cache_first"
    NETWORK_FIRST = "network_first"
    CACHE_ONLY = "cache_only"


@dataclass
class GitHubResource:
    """GitHub resource information."""
    resource_id: str
    resource_type: ResourceType
    file_path: str
    content: str
    content_hash: str
    last_modified: datetime
    size_bytes: int
    encoding: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceRequest:
    """Resource fetch request."""
    request_id: str
    resource_path: str
    resource_type: ResourceType
    cache_strategy: CacheStrategy
    timeout_seconds: int
    priority: str = "normal"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SyncOperation:
    """Synchronization operation."""
    operation_id: str
    operation_type: str  # fetch, push, sync, validate
    target_paths: List[str]
    started_at: datetime
    completed_at: Optional[datetime]
    status: SyncStatus
    files_processed: int
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GitHubIntegrationResult:
    """GitHub integration operation result."""
    success: bool
    operation_type: str
    resource: Optional[GitHubResource]
    sync_operation: Optional[SyncOperation]
    cache_hit: bool
    response_time_ms: float
    error_message: Optional[str]
    metadata: Dict[str, Any]


# ============================================================================
# GITHUB INTEGRATION ENGINE
# ============================================================================

class GitHubIntegrationEngine:
    """
    GitHub integration engine for dynamic resource fetching.
    
    Features:
    - Dynamic resource fetching from JAEGIS repository
    - Intelligent caching with multiple strategies
    - Real-time synchronization monitoring
    - Branch-aware resource access
    - Content validation and integrity checking
    - Rate limit management
    - Webhook integration for real-time updates
    - Batch operations and bulk synchronization
    """
    
    def __init__(self, github_config: Dict[str, Any]):
        """
        Initialize GitHub integration engine.
        
        Args:
            github_config: Configuration for GitHub integration
        """
        self.config = github_config
        self.repository_url = github_config.get("repository_url", "https://github.com/usemanusai/JAEGIS")
        self.api_base_url = "https://api.github.com"
        self.access_token = github_config.get("access_token")
        self.default_branch = github_config.get("default_branch", "main")
        
        # Repository information
        self.owner = "usemanusai"
        self.repo_name = "JAEGIS"
        
        # Caching
        self.resource_cache = {}
        self.cache_ttl_seconds = github_config.get("cache_ttl_seconds", 300)  # 5 minutes
        self.max_cache_size = github_config.get("max_cache_size", 1000)
        
        # Rate limiting
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = datetime.utcnow()
        self.request_queue = asyncio.Queue()
        
        # Synchronization tracking
        self.sync_operations = {}
        self.last_sync_time = None
        self.sync_interval_seconds = github_config.get("sync_interval_seconds", 3600)  # 1 hour
        
        # Performance tracking
        self.performance_stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "successful_fetches": 0,
            "failed_fetches": 0,
            "average_response_time_ms": 0.0,
            "total_bytes_fetched": 0
        }
        
        # HTTP session
        self.http_session = None
        
        # Resource mappings
        self.resource_mappings = self._load_resource_mappings()
    
    def _load_resource_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Load mappings for different resource types."""
        return {
            "agent_configs": {
                "base_path": "core/agents",
                "file_pattern": "*.txt",
                "resource_type": ResourceType.AGENT_CONFIG,
                "cache_strategy": CacheStrategy.CACHE_FIRST
            },
            "command_templates": {
                "base_path": "commands",
                "file_pattern": "*.json",
                "resource_type": ResourceType.COMMAND_TEMPLATE,
                "cache_strategy": CacheStrategy.NETWORK_FIRST
            },
            "documentation": {
                "base_path": "docs",
                "file_pattern": "*.md",
                "resource_type": ResourceType.DOCUMENTATION,
                "cache_strategy": CacheStrategy.CACHE_FIRST
            },
            "configurations": {
                "base_path": "config",
                "file_pattern": "*.yaml",
                "resource_type": ResourceType.CONFIGURATION,
                "cache_strategy": CacheStrategy.ALWAYS_FRESH
            },
            "schemas": {
                "base_path": "schemas",
                "file_pattern": "*.json",
                "resource_type": ResourceType.SCHEMA,
                "cache_strategy": CacheStrategy.CACHE_FIRST
            },
            "workflows": {
                "base_path": ".github/workflows",
                "file_pattern": "*.yml",
                "resource_type": ResourceType.WORKFLOW,
                "cache_strategy": CacheStrategy.NETWORK_FIRST
            }
        }
    
    async def initialize_integration(self) -> bool:
        """Initialize GitHub integration."""
        try:
            # Initialize HTTP session
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "NLDS-GitHub-Integration/2.2.0"
            }
            
            if self.access_token:
                headers["Authorization"] = f"token {self.access_token}"
            
            self.http_session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Validate repository access
            if await self._validate_repository_access():
                logger.info(f"GitHub integration initialized for {self.owner}/{self.repo_name}")
                
                # Start background tasks
                asyncio.create_task(self._rate_limit_monitor())
                asyncio.create_task(self._periodic_sync())
                
                return True
            else:
                logger.error("Failed to validate repository access")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize GitHub integration: {e}")
            return False
    
    async def _validate_repository_access(self) -> bool:
        """Validate access to GitHub repository."""
        try:
            url = f"{self.api_base_url}/repos/{self.owner}/{self.repo_name}"
            
            async with self.http_session.get(url) as response:
                if response.status == 200:
                    repo_data = await response.json()
                    logger.info(f"Repository access validated: {repo_data.get('full_name')}")
                    
                    # Update rate limit info
                    self.rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 5000))
                    reset_timestamp = int(response.headers.get("X-RateLimit-Reset", 0))
                    self.rate_limit_reset = datetime.fromtimestamp(reset_timestamp)
                    
                    return True
                else:
                    logger.error(f"Repository access validation failed: HTTP {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Repository validation error: {e}")
            return False
    
    def _generate_cache_key(self, file_path: str, branch: str = None) -> str:
        """Generate cache key for resource."""
        branch = branch or self.default_branch
        return hashlib.md5(f"{file_path}:{branch}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached resource is still valid."""
        if cache_key not in self.resource_cache:
            return False
        
        cached_resource = self.resource_cache[cache_key]
        cache_age = datetime.utcnow() - cached_resource["cached_at"]
        
        return cache_age.total_seconds() < self.cache_ttl_seconds
    
    def _store_in_cache(self, cache_key: str, resource: GitHubResource) -> None:
        """Store resource in cache."""
        # Implement LRU eviction if cache is full
        if len(self.resource_cache) >= self.max_cache_size:
            # Remove oldest entry
            oldest_key = min(self.resource_cache.keys(), 
                           key=lambda k: self.resource_cache[k]["cached_at"])
            del self.resource_cache[oldest_key]
        
        self.resource_cache[cache_key] = {
            "resource": resource,
            "cached_at": datetime.utcnow()
        }
    
    async def fetch_resource(self, resource_path: str, 
                           resource_type: ResourceType = ResourceType.CONFIGURATION,
                           cache_strategy: CacheStrategy = CacheStrategy.CACHE_FIRST,
                           branch: str = None) -> GitHubIntegrationResult:
        """
        Fetch resource from GitHub repository.
        
        Args:
            resource_path: Path to resource in repository
            resource_type: Type of resource being fetched
            cache_strategy: Caching strategy to use
            branch: Git branch to fetch from (defaults to main)
            
        Returns:
            GitHub integration result
        """
        import time
        start_time = time.time()
        
        try:
            branch = branch or self.default_branch
            cache_key = self._generate_cache_key(resource_path, branch)
            
            # Check cache based on strategy
            if cache_strategy in [CacheStrategy.CACHE_FIRST, CacheStrategy.CACHE_ONLY]:
                if self._is_cache_valid(cache_key):
                    cached_data = self.resource_cache[cache_key]
                    self.performance_stats["cache_hits"] += 1
                    
                    return GitHubIntegrationResult(
                        success=True,
                        operation_type="fetch_resource",
                        resource=cached_data["resource"],
                        sync_operation=None,
                        cache_hit=True,
                        response_time_ms=(time.time() - start_time) * 1000,
                        error_message=None,
                        metadata={"cache_strategy": cache_strategy.value, "branch": branch}
                    )
                elif cache_strategy == CacheStrategy.CACHE_ONLY:
                    return GitHubIntegrationResult(
                        success=False,
                        operation_type="fetch_resource",
                        resource=None,
                        sync_operation=None,
                        cache_hit=False,
                        response_time_ms=(time.time() - start_time) * 1000,
                        error_message="Resource not in cache and cache-only strategy specified",
                        metadata={"cache_strategy": cache_strategy.value}
                    )
            
            # Fetch from GitHub
            url = f"{self.api_base_url}/repos/{self.owner}/{self.repo_name}/contents/{resource_path}"
            params = {"ref": branch}
            
            async with self.http_session.get(url, params=params) as response:
                response_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    content_data = await response.json()
                    
                    # Decode content
                    if content_data.get("encoding") == "base64":
                        content = base64.b64decode(content_data["content"]).decode("utf-8")
                    else:
                        content = content_data["content"]
                    
                    # Create resource object
                    resource = GitHubResource(
                        resource_id=content_data["sha"],
                        resource_type=resource_type,
                        file_path=resource_path,
                        content=content,
                        content_hash=content_data["sha"],
                        last_modified=datetime.fromisoformat(content_data["download_url"].split("?")[0]),  # Simplified
                        size_bytes=content_data["size"],
                        encoding=content_data.get("encoding", "utf-8"),
                        metadata={
                            "download_url": content_data["download_url"],
                            "html_url": content_data["html_url"],
                            "git_url": content_data["git_url"],
                            "branch": branch
                        }
                    )
                    
                    # Store in cache
                    if cache_strategy != CacheStrategy.ALWAYS_FRESH:
                        self._store_in_cache(cache_key, resource)
                    
                    # Update statistics
                    self.performance_stats["total_requests"] += 1
                    self.performance_stats["successful_fetches"] += 1
                    self.performance_stats["cache_misses"] += 1
                    self.performance_stats["total_bytes_fetched"] += content_data["size"]
                    
                    # Update average response time
                    current_avg = self.performance_stats["average_response_time_ms"]
                    total_requests = self.performance_stats["total_requests"]
                    self.performance_stats["average_response_time_ms"] = (current_avg * (total_requests - 1) + response_time) / total_requests
                    
                    return GitHubIntegrationResult(
                        success=True,
                        operation_type="fetch_resource",
                        resource=resource,
                        sync_operation=None,
                        cache_hit=False,
                        response_time_ms=response_time,
                        error_message=None,
                        metadata={
                            "cache_strategy": cache_strategy.value,
                            "branch": branch,
                            "content_size": content_data["size"]
                        }
                    )
                else:
                    error_data = await response.json() if response.content_type == "application/json" else {}
                    error_message = error_data.get("message", f"HTTP {response.status}")
                    
                    self.performance_stats["total_requests"] += 1
                    self.performance_stats["failed_fetches"] += 1
                    
                    return GitHubIntegrationResult(
                        success=False,
                        operation_type="fetch_resource",
                        resource=None,
                        sync_operation=None,
                        cache_hit=False,
                        response_time_ms=response_time,
                        error_message=error_message,
                        metadata={"http_status": response.status, "branch": branch}
                    )
                    
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logger.error(f"Resource fetch failed: {e}")
            
            return GitHubIntegrationResult(
                success=False,
                operation_type="fetch_resource",
                resource=None,
                sync_operation=None,
                cache_hit=False,
                response_time_ms=response_time,
                error_message=str(e),
                metadata={}
            )
    
    async def fetch_directory_contents(self, directory_path: str, 
                                     resource_type: ResourceType = ResourceType.CONFIGURATION,
                                     branch: str = None) -> List[GitHubIntegrationResult]:
        """Fetch all files in a directory."""
        try:
            branch = branch or self.default_branch
            url = f"{self.api_base_url}/repos/{self.owner}/{self.repo_name}/contents/{directory_path}"
            params = {"ref": branch}
            
            async with self.http_session.get(url, params=params) as response:
                if response.status == 200:
                    contents = await response.json()
                    
                    # Filter for files only
                    files = [item for item in contents if item["type"] == "file"]
                    
                    # Fetch each file
                    results = []
                    for file_item in files:
                        result = await self.fetch_resource(
                            file_item["path"],
                            resource_type,
                            CacheStrategy.CACHE_FIRST,
                            branch
                        )
                        results.append(result)
                    
                    return results
                else:
                    logger.error(f"Failed to fetch directory contents: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Directory fetch failed: {e}")
            return []
    
    async def fetch_agent_config(self, agent_name: str) -> GitHubIntegrationResult:
        """Fetch specific agent configuration."""
        agent_config_path = f"core/agents/{agent_name}.txt"
        return await self.fetch_resource(
            agent_config_path,
            ResourceType.AGENT_CONFIG,
            CacheStrategy.CACHE_FIRST
        )
    
    async def fetch_command_template(self, command_name: str) -> GitHubIntegrationResult:
        """Fetch specific command template."""
        command_template_path = f"commands/{command_name}.json"
        return await self.fetch_resource(
            command_template_path,
            ResourceType.COMMAND_TEMPLATE,
            CacheStrategy.NETWORK_FIRST
        )
    
    async def fetch_documentation(self, doc_path: str) -> GitHubIntegrationResult:
        """Fetch documentation file."""
        return await self.fetch_resource(
            doc_path,
            ResourceType.DOCUMENTATION,
            CacheStrategy.CACHE_FIRST
        )
    
    async def sync_resources(self, resource_paths: List[str], 
                           force_refresh: bool = False) -> SyncOperation:
        """Synchronize multiple resources."""
        operation_id = f"sync_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        sync_op = SyncOperation(
            operation_id=operation_id,
            operation_type="sync",
            target_paths=resource_paths,
            started_at=datetime.utcnow(),
            completed_at=None,
            status=SyncStatus.SYNCING,
            files_processed=0,
            errors=[]
        )
        
        self.sync_operations[operation_id] = sync_op
        
        try:
            for resource_path in resource_paths:
                try:
                    cache_strategy = CacheStrategy.ALWAYS_FRESH if force_refresh else CacheStrategy.NETWORK_FIRST
                    result = await self.fetch_resource(resource_path, cache_strategy=cache_strategy)
                    
                    if result.success:
                        sync_op.files_processed += 1
                    else:
                        sync_op.errors.append(f"{resource_path}: {result.error_message}")
                        
                except Exception as e:
                    sync_op.errors.append(f"{resource_path}: {str(e)}")
            
            sync_op.completed_at = datetime.utcnow()
            sync_op.status = SyncStatus.SYNCED if not sync_op.errors else SyncStatus.ERROR
            
        except Exception as e:
            sync_op.completed_at = datetime.utcnow()
            sync_op.status = SyncStatus.ERROR
            sync_op.errors.append(f"Sync operation failed: {str(e)}")
        
        return sync_op
    
    async def _rate_limit_monitor(self) -> None:
        """Monitor GitHub API rate limits."""
        while True:
            try:
                # Check rate limit status
                if self.rate_limit_remaining < 100:
                    wait_time = (self.rate_limit_reset - datetime.utcnow()).total_seconds()
                    if wait_time > 0:
                        logger.warning(f"Rate limit low ({self.rate_limit_remaining}), waiting {wait_time:.0f}s")
                        await asyncio.sleep(min(wait_time, 300))  # Max 5 minutes
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Rate limit monitor error: {e}")
                await asyncio.sleep(60)
    
    async def _periodic_sync(self) -> None:
        """Perform periodic synchronization of critical resources."""
        while True:
            try:
                await asyncio.sleep(self.sync_interval_seconds)
                
                # Sync critical resources
                critical_paths = [
                    "core/agent-config.txt",
                    "config/system-config.yaml",
                    "commands/core-commands.json"
                ]
                
                logger.info("Starting periodic resource synchronization")
                sync_op = await self.sync_resources(critical_paths)
                
                if sync_op.status == SyncStatus.SYNCED:
                    logger.info(f"Periodic sync completed: {sync_op.files_processed} files")
                else:
                    logger.warning(f"Periodic sync had errors: {len(sync_op.errors)} errors")
                
                self.last_sync_time = datetime.utcnow()
                
            except Exception as e:
                logger.error(f"Periodic sync error: {e}")
    
    async def get_integration_status(self) -> Dict[str, Any]:
        """Get current GitHub integration status."""
        return {
            "repository": f"{self.owner}/{self.repo_name}",
            "default_branch": self.default_branch,
            "cache_size": len(self.resource_cache),
            "cache_hit_rate": self.performance_stats["cache_hits"] / max(self.performance_stats["total_requests"], 1),
            "rate_limit_remaining": self.rate_limit_remaining,
            "rate_limit_reset": self.rate_limit_reset.isoformat(),
            "last_sync_time": self.last_sync_time.isoformat() if self.last_sync_time else None,
            "performance_stats": self.performance_stats.copy(),
            "active_sync_operations": len([op for op in self.sync_operations.values() if op.status == SyncStatus.SYNCING])
        }
    
    async def clear_cache(self, resource_path: Optional[str] = None) -> int:
        """Clear cache entries."""
        if resource_path:
            # Clear specific resource
            cache_key = self._generate_cache_key(resource_path)
            if cache_key in self.resource_cache:
                del self.resource_cache[cache_key]
                return 1
            return 0
        else:
            # Clear all cache
            cache_size = len(self.resource_cache)
            self.resource_cache.clear()
            return cache_size
    
    async def cleanup(self) -> None:
        """Cleanup GitHub integration resources."""
        try:
            if self.http_session and not self.http_session.closed:
                await self.http_session.close()
            
            # Clear cache
            self.resource_cache.clear()
            
            logger.info("GitHub integration cleaned up")
            
        except Exception as e:
            logger.error(f"Error during GitHub integration cleanup: {e}")


# ============================================================================
# GITHUB INTEGRATION UTILITIES
# ============================================================================

class GitHubIntegrationUtils:
    """Utility functions for GitHub integration."""
    
    @staticmethod
    def integration_result_to_dict(result: GitHubIntegrationResult) -> Dict[str, Any]:
        """Convert integration result to dictionary format."""
        return {
            "success": result.success,
            "operation_type": result.operation_type,
            "resource": {
                "resource_id": result.resource.resource_id,
                "resource_type": result.resource.resource_type.value,
                "file_path": result.resource.file_path,
                "content_length": len(result.resource.content),
                "content_hash": result.resource.content_hash,
                "last_modified": result.resource.last_modified.isoformat(),
                "size_bytes": result.resource.size_bytes
            } if result.resource else None,
            "cache_hit": result.cache_hit,
            "response_time_ms": result.response_time_ms,
            "error_message": result.error_message,
            "metadata": result.metadata
        }
    
    @staticmethod
    def sync_operation_to_dict(sync_op: SyncOperation) -> Dict[str, Any]:
        """Convert sync operation to dictionary format."""
        return {
            "operation_id": sync_op.operation_id,
            "operation_type": sync_op.operation_type,
            "target_paths": sync_op.target_paths,
            "started_at": sync_op.started_at.isoformat(),
            "completed_at": sync_op.completed_at.isoformat() if sync_op.completed_at else None,
            "status": sync_op.status.value,
            "files_processed": sync_op.files_processed,
            "errors": sync_op.errors,
            "duration_seconds": (sync_op.completed_at - sync_op.started_at).total_seconds() if sync_op.completed_at else None,
            "metadata": sync_op.metadata
        }
    
    @staticmethod
    def validate_github_config(config: Dict[str, Any]) -> List[str]:
        """Validate GitHub configuration."""
        errors = []
        
        required_fields = ["repository_url"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        if "access_token" not in config:
            errors.append("Access token not provided - API rate limits will be restrictive")
        
        return errors
