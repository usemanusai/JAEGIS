"""
JAEGIS GitHub Integration - GitHub Fetcher Implementation
Single GitHub link fetching with multi-fetch capabilities

This module implements the core GitHub fetching functionality as designed
by the Agent Creator system for comprehensive GitHub integration.
"""

import asyncio
import aiohttp
import json
import logging
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import re
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)


@dataclass
class GitHubResource:
    """GitHub resource representation."""
    url: str
    content: str
    resource_type: str
    metadata: Dict[str, Any]
    fetched_at: float
    cache_key: str
    links_found: List[str] = None


@dataclass
class FetchResult:
    """Result of GitHub fetch operation."""
    success: bool
    resource: Optional[GitHubResource] = None
    error: Optional[str] = None
    fetch_time: float = 0.0
    cache_hit: bool = False


class GitHubFetcher:
    """
    Core GitHub fetching system implementing single link fetch with multi-fetch discovery.
    
    Designed by Agent Creator to handle:
    1. Single GitHub link fetching (e.g., GOLD.md guidelines)
    2. Multi-fetch link discovery and coordination
    3. Content processing and validation
    4. Intelligent caching and fallback handling
    """
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache: Dict[str, GitHubResource] = {}
        self.fetch_stats = {
            "total_fetches": 0,
            "cache_hits": 0,
            "fetch_errors": 0,
            "multi_fetch_discoveries": 0
        }
        
        # Configuration
        self.config = {
            "timeout": 10,
            "max_retries": 3,
            "cache_duration": 3600,  # 1 hour
            "user_agent": "JAEGIS-GitHub-Integration/1.0",
            "max_content_size": 10 * 1024 * 1024,  # 10MB
            "supported_extensions": [".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js"]
        }
        
        # GitHub URL patterns for link discovery
        self.github_patterns = {
            "raw_content": r"https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/(.+)",
            "blob_content": r"https://github\.com/[^/]+/[^/]+/blob/[^/]+/(.+)",
            "repo_reference": r"https://github\.com/([^/]+/[^/]+)",
            "relative_link": r"\[([^\]]+)\]\(([^)]+)\)",
            "absolute_github": r"https://github\.com/[^\s)]+",
            "raw_github": r"https://raw\.githubusercontent\.com/[^\s)]+"
        }
        
        logger.info("GitHub Fetcher initialized")
    
    async def initialize(self):
        """Initialize the GitHub fetcher."""
        
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        timeout = aiohttp.ClientTimeout(total=self.config["timeout"])
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": self.config["user_agent"]}
        )
        
        logger.info("✅ GitHub Fetcher session initialized")
    
    async def cleanup(self):
        """Clean up resources."""
        
        if self.session:
            await self.session.close()
        
        logger.info("GitHub Fetcher cleaned up")
    
    async def fetch_github_guideline(self, url: str) -> FetchResult:
        """
        Fetch a single GitHub guideline URL (e.g., GOLD.md).
        
        Args:
            url: GitHub URL to fetch (e.g., https://github.com/usemanusai/JAEGIS/GOLD.md)
        
        Returns:
            FetchResult with content and discovered links for multi-fetch
        """
        
        logger.info(f"📥 Fetching GitHub guideline: {url}")
        
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(url)
            cached_resource = self._get_cached_resource(cache_key)
            
            if cached_resource:
                logger.info(f"✅ Cache hit for: {url}")
                self.fetch_stats["cache_hits"] += 1
                return FetchResult(
                    success=True,
                    resource=cached_resource,
                    fetch_time=time.time() - start_time,
                    cache_hit=True
                )
            
            # Convert GitHub URL to raw content URL if needed
            raw_url = self._convert_to_raw_url(url)
            
            # Fetch content
            resource = await self._fetch_content(raw_url)
            
            if resource:
                # Discover multi-fetch links
                discovered_links = await self._discover_multi_fetch_links(resource.content, url)
                resource.links_found = discovered_links
                
                # Cache the resource
                self._cache_resource(cache_key, resource)
                
                # Update stats
                self.fetch_stats["total_fetches"] += 1
                if discovered_links:
                    self.fetch_stats["multi_fetch_discoveries"] += 1
                
                logger.info(f"✅ Successfully fetched: {url}")
                logger.info(f"  Content length: {len(resource.content)} chars")
                logger.info(f"  Links discovered: {len(discovered_links)}")
                
                return FetchResult(
                    success=True,
                    resource=resource,
                    fetch_time=time.time() - start_time,
                    cache_hit=False
                )
            else:
                self.fetch_stats["fetch_errors"] += 1
                return FetchResult(
                    success=False,
                    error="Failed to fetch content",
                    fetch_time=time.time() - start_time
                )
        
        except Exception as e:
            logger.error(f"❌ Error fetching {url}: {e}")
            self.fetch_stats["fetch_errors"] += 1
            return FetchResult(
                success=False,
                error=str(e),
                fetch_time=time.time() - start_time
            )
    
    async def multi_fetch_from_guideline(self, guideline_resource: GitHubResource) -> List[FetchResult]:
        """
        Perform multi-fetch based on links discovered in guideline.
        
        Args:
            guideline_resource: The fetched guideline resource containing discovered links
        
        Returns:
            List of FetchResult for each discovered link
        """
        
        if not guideline_resource.links_found:
            logger.info("No links found for multi-fetch")
            return []
        
        logger.info(f"🔄 Starting multi-fetch for {len(guideline_resource.links_found)} links")
        
        # Create fetch tasks for all discovered links
        fetch_tasks = []
        for link in guideline_resource.links_found:
            task = self._fetch_discovered_link(link, guideline_resource.url)
            fetch_tasks.append(task)
        
        # Execute all fetches concurrently
        results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
        
        # Process results
        fetch_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                fetch_results.append(FetchResult(
                    success=False,
                    error=str(result),
                    fetch_time=0.0
                ))
            else:
                fetch_results.append(result)
        
        successful_fetches = sum(1 for r in fetch_results if r.success)
        logger.info(f"✅ Multi-fetch complete: {successful_fetches}/{len(fetch_results)} successful")
        
        return fetch_results
    
    async def _fetch_content(self, url: str) -> Optional[GitHubResource]:
        """Fetch content from GitHub URL."""
        
        if not self.session:
            await self.initialize()
        
        for attempt in range(self.config["max_retries"]):
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Validate content size
                        if len(content) > self.config["max_content_size"]:
                            logger.warning(f"Content too large: {len(content)} bytes")
                            content = content[:self.config["max_content_size"]]
                        
                        # Determine resource type
                        resource_type = self._determine_resource_type(url, content)
                        
                        # Extract metadata
                        metadata = await self._extract_metadata(content, resource_type)
                        
                        return GitHubResource(
                            url=url,
                            content=content,
                            resource_type=resource_type,
                            metadata=metadata,
                            fetched_at=time.time(),
                            cache_key=self._generate_cache_key(url)
                        )
                    
                    elif response.status == 404:
                        logger.error(f"Resource not found: {url}")
                        return None
                    
                    else:
                        logger.warning(f"HTTP {response.status} for {url}, attempt {attempt + 1}")
                        if attempt == self.config["max_retries"] - 1:
                            return None
                        
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            except asyncio.TimeoutError:
                logger.warning(f"Timeout fetching {url}, attempt {attempt + 1}")
                if attempt == self.config["max_retries"] - 1:
                    return None
                await asyncio.sleep(2 ** attempt)
            
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
                return None
        
        return None
    
    async def _discover_multi_fetch_links(self, content: str, base_url: str) -> List[str]:
        """Discover GitHub links in content for multi-fetch."""
        
        discovered_links = set()
        
        # Extract base repository info
        base_repo = self._extract_repo_info(base_url)
        
        # Find all GitHub links in content
        for pattern_name, pattern in self.github_patterns.items():
            matches = re.findall(pattern, content)
            
            for match in matches:
                if pattern_name == "relative_link":
                    # Handle relative links [text](path)
                    link_text, link_path = match
                    if not link_path.startswith("http"):
                        # Convert relative to absolute
                        absolute_url = self._resolve_relative_link(link_path, base_repo)
                        if absolute_url:
                            discovered_links.add(absolute_url)
                    else:
                        discovered_links.add(link_path)
                
                elif pattern_name in ["absolute_github", "raw_github"]:
                    # Direct GitHub URLs
                    discovered_links.add(match)
                
                elif pattern_name == "repo_reference":
                    # Repository references
                    repo_path = match
                    repo_url = f"https://github.com/{repo_path}"
                    discovered_links.add(repo_url)
        
        # Filter and validate discovered links
        valid_links = []
        for link in discovered_links:
            if self._is_valid_github_link(link) and link != base_url:
                valid_links.append(link)
        
        return valid_links
    
    async def _fetch_discovered_link(self, url: str, base_url: str) -> FetchResult:
        """Fetch a discovered link."""
        
        try:
            # Convert to raw URL if needed
            raw_url = self._convert_to_raw_url(url)
            
            # Check cache
            cache_key = self._generate_cache_key(raw_url)
            cached_resource = self._get_cached_resource(cache_key)
            
            if cached_resource:
                return FetchResult(
                    success=True,
                    resource=cached_resource,
                    cache_hit=True
                )
            
            # Fetch content
            resource = await self._fetch_content(raw_url)
            
            if resource:
                self._cache_resource(cache_key, resource)
                return FetchResult(
                    success=True,
                    resource=resource,
                    cache_hit=False
                )
            else:
                return FetchResult(
                    success=False,
                    error="Failed to fetch content"
                )
        
        except Exception as e:
            return FetchResult(
                success=False,
                error=str(e)
            )
    
    def _convert_to_raw_url(self, url: str) -> str:
        """Convert GitHub URL to raw content URL."""
        
        # If already a raw URL, return as-is
        if "raw.githubusercontent.com" in url:
            return url
        
        # Convert blob URL to raw URL
        if "/blob/" in url:
            return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        
        # Handle direct file references
        if url.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js")):
            if "github.com" in url and "/blob/" not in url:
                # Add default branch and convert to raw
                parts = url.replace("https://github.com/", "").split("/")
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    file_path = "/".join(parts[2:]) if len(parts) > 2 else ""
                    return f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}"
        
        return url
    
    def _extract_repo_info(self, url: str) -> Optional[str]:
        """Extract repository information from GitHub URL."""
        
        match = re.search(r"github\.com/([^/]+/[^/]+)", url)
        return match.group(1) if match else None
    
    def _resolve_relative_link(self, relative_path: str, base_repo: str) -> Optional[str]:
        """Resolve relative link to absolute GitHub URL."""
        
        if not base_repo:
            return None
        
        # Clean relative path
        relative_path = relative_path.lstrip("./")
        
        # Create absolute URL
        return f"https://github.com/{base_repo}/blob/main/{relative_path}"
    
    def _is_valid_github_link(self, url: str) -> bool:
        """Check if URL is a valid GitHub link."""
        
        if not url.startswith("https://"):
            return False
        
        if "github.com" not in url and "raw.githubusercontent.com" not in url:
            return False
        
        # Check for supported file extensions
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        return any(path.endswith(ext) for ext in self.config["supported_extensions"]) or "/blob/" in url
    
    def _determine_resource_type(self, url: str, content: str) -> str:
        """Determine the type of resource based on URL and content."""
        
        if url.endswith(".md"):
            return "markdown"
        elif url.endswith(".json"):
            return "json"
        elif url.endswith((".yaml", ".yml")):
            return "yaml"
        elif url.endswith(".py"):
            return "python"
        elif url.endswith(".js"):
            return "javascript"
        elif url.endswith(".txt"):
            return "text"
        else:
            # Try to determine from content
            if content.strip().startswith("{"):
                return "json"
            elif content.strip().startswith("---"):
                return "yaml"
            else:
                return "text"
    
    async def _extract_metadata(self, content: str, resource_type: str) -> Dict[str, Any]:
        """Extract metadata from content."""
        
        metadata = {
            "content_length": len(content),
            "line_count": len(content.splitlines()),
            "resource_type": resource_type
        }
        
        if resource_type == "markdown":
            # Extract markdown metadata
            lines = content.splitlines()
            if lines and lines[0].startswith("#"):
                metadata["title"] = lines[0].lstrip("#").strip()
            
            # Count headers
            headers = [line for line in lines if line.startswith("#")]
            metadata["header_count"] = len(headers)
        
        elif resource_type == "json":
            try:
                data = json.loads(content)
                metadata["json_keys"] = list(data.keys()) if isinstance(data, dict) else []
            except:
                pass
        
        return metadata
    
    def _generate_cache_key(self, url: str) -> str:
        """Generate cache key for URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _get_cached_resource(self, cache_key: str) -> Optional[GitHubResource]:
        """Get resource from cache if valid."""
        
        if cache_key in self.cache:
            resource = self.cache[cache_key]
            if time.time() - resource.fetched_at < self.config["cache_duration"]:
                return resource
            else:
                # Remove expired cache entry
                del self.cache[cache_key]
        
        return None
    
    def _cache_resource(self, cache_key: str, resource: GitHubResource):
        """Cache resource."""
        self.cache[cache_key] = resource
    
    def get_fetch_stats(self) -> Dict[str, Any]:
        """Get fetching statistics."""
        
        total = self.fetch_stats["total_fetches"]
        cache_hit_rate = (self.fetch_stats["cache_hits"] / total * 100) if total > 0 else 0
        
        return {
            **self.fetch_stats,
            "cache_hit_rate": round(cache_hit_rate, 2),
            "cache_size": len(self.cache)
        }


# Global GitHub fetcher instance
GITHUB_FETCHER = GitHubFetcher()


async def fetch_github_guideline(url: str) -> FetchResult:
    """Convenience function to fetch GitHub guideline."""
    
    if not GITHUB_FETCHER.session:
        await GITHUB_FETCHER.initialize()
    
    return await GITHUB_FETCHER.fetch_github_guideline(url)


async def multi_fetch_from_guideline(guideline_resource: GitHubResource) -> List[FetchResult]:
    """Convenience function for multi-fetch."""
    
    return await GITHUB_FETCHER.multi_fetch_from_guideline(guideline_resource)
