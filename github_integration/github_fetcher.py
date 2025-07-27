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
    - Single GitHub link fetching with fallback support
    - Automatic multi-fetch discovery from fetched content
    - Intelligent caching with TTL and performance optimization
    - Comprehensive error handling and retry mechanisms
    - Multiple GitHub URL formats and content types
    """
    
    def __init__(self, cache_duration: int = 3600, max_retries: int = 3):
        self.cache_duration = cache_duration
        self.max_retries = max_retries
        self.cache: Dict[str, GitHubResource] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
        # GitHub URL patterns for link discovery
        self.github_patterns = [
            r'https://github\.com/[^/]+/[^/]+/blob/[^/]+/[^\s\)]+',
            r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/[^\s\)]+',
            r'https://github\.com/[^/]+/[^/]+/tree/[^/]+/[^\s\)]+',
            r'https://api\.github\.com/repos/[^/]+/[^/]+/contents/[^\s\)]+',
        ]
        
        logger.info("GitHub Fetcher initialized")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'JAEGIS-GitHub-Integration/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def _generate_cache_key(self, url: str) -> str:
        """Generate cache key for URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_cache_valid(self, resource: GitHubResource) -> bool:
        """Check if cached resource is still valid."""
        return (time.time() - resource.fetched_at) < self.cache_duration
    
    def _normalize_github_url(self, url: str) -> str:
        """Normalize GitHub URL to raw content URL if needed."""
        # Convert GitHub blob URLs to raw URLs
        if 'github.com' in url and '/blob/' in url:
            url = url.replace('github.com', 'raw.githubusercontent.com')
            url = url.replace('/blob/', '/')
        
        return url
    
    def _extract_github_links(self, content: str) -> List[str]:
        """Extract GitHub links from content."""
        links = []
        
        for pattern in self.github_patterns:
            matches = re.findall(pattern, content)
            links.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    def _determine_resource_type(self, url: str, content: str) -> str:
        """Determine resource type based on URL and content."""
        url_lower = url.lower()
        
        if url_lower.endswith('.md'):
            return 'markdown'
        elif url_lower.endswith('.json'):
            return 'json'
        elif url_lower.endswith('.txt'):
            return 'text'
        elif url_lower.endswith('.py'):
            return 'python'
        elif url_lower.endswith('.js'):
            return 'javascript'
        elif url_lower.endswith('.yaml') or url_lower.endswith('.yml'):
            return 'yaml'
        elif 'GOLD.md' in url:
            return 'guidelines'
        elif 'README' in url.upper():
            return 'readme'
        elif 'config' in url_lower:
            return 'configuration'
        else:
            # Try to determine from content
            if content.strip().startswith('{') and content.strip().endswith('}'):
                return 'json'
            elif content.strip().startswith('#') or '##' in content:
                return 'markdown'
            else:
                return 'text'
    
    async def fetch_single_github_link(self, url: str, enable_cache: bool = True) -> FetchResult:
        """
        Fetch a single GitHub link with caching and error handling.
        
        Args:
            url: GitHub URL to fetch
            enable_cache: Whether to use caching
            
        Returns:
            FetchResult with success status and resource data
        """
        start_time = time.time()
        cache_key = self._generate_cache_key(url)
        
        # Check cache first
        if enable_cache and cache_key in self.cache:
            cached_resource = self.cache[cache_key]
            if self._is_cache_valid(cached_resource):
                logger.info(f"✅ Cache hit for {url}")
                return FetchResult(
                    success=True,
                    resource=cached_resource,
                    fetch_time=time.time() - start_time,
                    cache_hit=True
                )
        
        # Normalize URL
        normalized_url = self._normalize_github_url(url)
        
        # Attempt fetch with retries
        for attempt in range(self.max_retries):
            try:
                if not self.session:
                    raise RuntimeError("Session not initialized. Use async context manager.")
                
                logger.info(f"🔄 Fetching {normalized_url} (attempt {attempt + 1})")
                
                async with self.session.get(normalized_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Extract metadata
                        metadata = {
                            'status_code': response.status,
                            'content_length': len(content),
                            'content_type': response.headers.get('content-type', ''),
                            'last_modified': response.headers.get('last-modified', ''),
                            'etag': response.headers.get('etag', ''),
                            'original_url': url,
                            'normalized_url': normalized_url
                        }
                        
                        # Determine resource type
                        resource_type = self._determine_resource_type(normalized_url, content)
                        
                        # Extract GitHub links for multi-fetch
                        links_found = self._extract_github_links(content)
                        
                        # Create resource
                        resource = GitHubResource(
                            url=normalized_url,
                            content=content,
                            resource_type=resource_type,
                            metadata=metadata,
                            fetched_at=time.time(),
                            cache_key=cache_key,
                            links_found=links_found
                        )
                        
                        # Cache the resource
                        if enable_cache:
                            self.cache[cache_key] = resource
                        
                        logger.info(f"✅ Successfully fetched {normalized_url}")
                        logger.info(f"   Resource type: {resource_type}")
                        logger.info(f"   Content length: {len(content)} chars")
                        logger.info(f"   Links found: {len(links_found)}")
                        
                        return FetchResult(
                            success=True,
                            resource=resource,
                            fetch_time=time.time() - start_time,
                            cache_hit=False
                        )
                    
                    elif response.status == 404:
                        error_msg = f"Resource not found: {normalized_url}"
                        logger.warning(f"⚠️ {error_msg}")
                        return FetchResult(
                            success=False,
                            error=error_msg,
                            fetch_time=time.time() - start_time
                        )
                    
                    elif response.status == 403:
                        error_msg = f"Access forbidden (rate limited?): {normalized_url}"
                        logger.warning(f"⚠️ {error_msg}")
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        return FetchResult(
                            success=False,
                            error=error_msg,
                            fetch_time=time.time() - start_time
                        )
                    
                    else:
                        error_msg = f"HTTP {response.status}: {normalized_url}"
                        logger.warning(f"⚠️ {error_msg}")
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(1)
                            continue
                        return FetchResult(
                            success=False,
                            error=error_msg,
                            fetch_time=time.time() - start_time
                        )
            
            except asyncio.TimeoutError:
                error_msg = f"Timeout fetching {normalized_url}"
                logger.warning(f"⚠️ {error_msg}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                return FetchResult(
                    success=False,
                    error=error_msg,
                    fetch_time=time.time() - start_time
                )
            
            except Exception as e:
                error_msg = f"Error fetching {normalized_url}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                return FetchResult(
                    success=False,
                    error=error_msg,
                    fetch_time=time.time() - start_time
                )
        
        # All retries failed
        return FetchResult(
            success=False,
            error=f"Failed to fetch after {self.max_retries} attempts",
            fetch_time=time.time() - start_time
        )
    
    async def multi_fetch_github_resources(self, primary_url: str, 
                                         max_additional_fetches: int = 10) -> Dict[str, FetchResult]:
        """
        Fetch primary GitHub resource and automatically discover and fetch related resources.
        
        Args:
            primary_url: Primary GitHub URL to fetch
            max_additional_fetches: Maximum number of additional resources to fetch
            
        Returns:
            Dictionary mapping URLs to FetchResults
        """
        logger.info(f"🔄 Starting multi-fetch for {primary_url}")
        
        results = {}
        
        # Fetch primary resource
        primary_result = await self.fetch_single_github_link(primary_url)
        results[primary_url] = primary_result
        
        if not primary_result.success or not primary_result.resource:
            logger.warning(f"⚠️ Primary fetch failed for {primary_url}")
            return results
        
        # Extract links from primary resource
        links_found = primary_result.resource.links_found or []
        
        if not links_found:
            logger.info(f"ℹ️ No additional GitHub links found in {primary_url}")
            return results
        
        logger.info(f"🔍 Found {len(links_found)} GitHub links in primary resource")
        
        # Limit additional fetches
        additional_links = links_found[:max_additional_fetches]
        
        # Fetch additional resources concurrently
        if additional_links:
            logger.info(f"🔄 Fetching {len(additional_links)} additional resources...")
            
            # Create fetch tasks
            fetch_tasks = []
            for link in additional_links:
                if link != primary_url:  # Don't refetch primary
                    task = self.fetch_single_github_link(link)
                    fetch_tasks.append((link, task))
            
            # Execute fetches concurrently
            if fetch_tasks:
                fetch_results = await asyncio.gather(
                    *[task for _, task in fetch_tasks],
                    return_exceptions=True
                )
                
                # Process results
                for (link, _), result in zip(fetch_tasks, fetch_results):
                    if isinstance(result, Exception):
                        logger.error(f"❌ Exception fetching {link}: {result}")
                        results[link] = FetchResult(
                            success=False,
                            error=str(result),
                            fetch_time=0.0
                        )
                    else:
                        results[link] = result
        
        # Summary
        successful_fetches = sum(1 for r in results.values() if r.success)
        total_fetches = len(results)
        
        logger.info(f"✅ Multi-fetch complete: {successful_fetches}/{total_fetches} successful")
        
        return results
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_cached = len(self.cache)
        valid_cached = sum(1 for r in self.cache.values() if self._is_cache_valid(r))
        
        return {
            'total_cached_resources': total_cached,
            'valid_cached_resources': valid_cached,
            'cache_hit_rate': f"{(valid_cached / max(total_cached, 1)) * 100:.1f}%",
            'cache_duration': self.cache_duration,
            'oldest_cache_age': min(
                (time.time() - r.fetched_at for r in self.cache.values()),
                default=0
            ),
            'newest_cache_age': max(
                (time.time() - r.fetched_at for r in self.cache.values()),
                default=0
            )
        }
    
    def clear_cache(self):
        """Clear the resource cache."""
        self.cache.clear()
        logger.info("🗑️ Cache cleared")
    
    def clear_expired_cache(self):
        """Clear expired cache entries."""
        expired_keys = [
            key for key, resource in self.cache.items()
            if not self._is_cache_valid(resource)
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        logger.info(f"🗑️ Cleared {len(expired_keys)} expired cache entries")


# Convenience functions for easy usage
async def fetch_github_resource(url: str, enable_cache: bool = True) -> FetchResult:
    """Convenience function to fetch a single GitHub resource."""
    async with GitHubFetcher() as fetcher:
        return await fetcher.fetch_single_github_link(url, enable_cache)


async def multi_fetch_github_resources(primary_url: str, 
                                     max_additional: int = 10) -> Dict[str, FetchResult]:
    """Convenience function for multi-fetch GitHub resources."""
    async with GitHubFetcher() as fetcher:
        return await fetcher.multi_fetch_github_resources(primary_url, max_additional)


# Example usage
async def main():
    """Example usage of GitHub Fetcher."""
    
    print("🔄 JAEGIS GitHub Fetcher - Example Usage")
    
    # Example: Fetch JAEGIS GOLD.md guidelines
    primary_url = "https://github.com/usemanusai/JAEGIS/GOLD.md"
    
    print(f"\n📋 Fetching primary resource: {primary_url}")
    
    async with GitHubFetcher() as fetcher:
        # Single fetch
        result = await fetcher.fetch_single_github_link(primary_url)
        
        if result.success:
            print(f"✅ Successfully fetched {primary_url}")
            print(f"   Resource type: {result.resource.resource_type}")
            print(f"   Content length: {len(result.resource.content)} characters")
            print(f"   Links found: {len(result.resource.links_found or [])}")
            print(f"   Fetch time: {result.fetch_time:.2f}s")
        else:
            print(f"❌ Failed to fetch {primary_url}: {result.error}")
        
        # Multi-fetch
        print(f"\n🔍 Multi-fetch from primary resource...")
        multi_results = await fetcher.multi_fetch_github_resources(primary_url, max_additional_fetches=5)
        
        print(f"\n📊 Multi-fetch Results:")
        for url, fetch_result in multi_results.items():
            status = "✅" if fetch_result.success else "❌"
            print(f"   {status} {url}")
        
        # Cache stats
        cache_stats = fetcher.get_cache_stats()
        print(f"\n📈 Cache Statistics:")
        for key, value in cache_stats.items():
            print(f"   {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())