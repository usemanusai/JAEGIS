"""
JAEGIS GitHub Client
Advanced GitHub API integration for content fetching and processing

@version 2.0.0
@author JAEGIS Development Team
"""

import asyncio
import aiohttp
import base64
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlparse, parse_qs
import structlog

logger = structlog.get_logger(__name__)

class GitHubClient:
    """Advanced GitHub API client with caching and rate limiting."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = datetime.now()
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = config.get('cache_ttl', 3600)  # 1 hour default
        
        # GitHub API configuration
        self.api_base = config.get('api_base_url', 'https://api.github.com')
        self.raw_base = 'https://raw.githubusercontent.com'
        self.token = config.get('token')
        self.timeout = config.get('timeout', 30)
        self.max_retries = config.get('max_retries', 3)
        self.retry_delay = config.get('retry_delay', 1)
        
        # Headers
        self.headers = {
            'User-Agent': 'JAEGIS-Python-Client/2.0.0',
            'Accept': 'application/vnd.github.v3+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    async def initialize(self):
        """Initialize the GitHub client."""
        logger.info("🌐 Initializing GitHub client...")
        
        # Create aiohttp session
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.headers
        )
        
        # Test connection
        await self.test_connection()
        
        logger.info("✅ GitHub client initialized successfully")
    
    async def test_connection(self):
        """Test GitHub API connection."""
        try:
            async with self.session.get(f"{self.api_base}/rate_limit") as response:
                if response.status == 200:
                    data = await response.json()
                    self.rate_limit_remaining = data['rate']['remaining']
                    self.rate_limit_reset = datetime.fromtimestamp(data['rate']['reset'])
                    logger.info(f"GitHub API connection successful. Rate limit: {self.rate_limit_remaining}")
                else:
                    logger.warning(f"GitHub API test returned status {response.status}")
        except Exception as e:
            logger.error(f"GitHub API connection test failed: {e}")
            raise
    
    async def fetch_content(self, url: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Fetch content from GitHub URL.
        
        Args:
            url: GitHub URL (raw or API)
            use_cache: Whether to use cached content
            
        Returns:
            Dictionary containing content and metadata
        """
        logger.info(f"📥 Fetching content from: {url}")
        
        # Check cache first
        cache_key = self._get_cache_key(url)
        if use_cache and cache_key in self.cache:
            cached_item = self.cache[cache_key]
            if not self._is_cache_expired(cached_item):
                logger.info("📋 Using cached content")
                return cached_item['data']
        
        try:
            # Determine if this is a raw URL or API URL
            if 'raw.githubusercontent.com' in url:
                content = await self._fetch_raw_content(url)
            elif 'api.github.com' in url:
                content = await self._fetch_api_content(url)
            else:
                # Convert GitHub URL to raw URL
                raw_url = self._convert_to_raw_url(url)
                content = await self._fetch_raw_content(raw_url)
            
            # Cache the result
            if use_cache:
                self.cache[cache_key] = {
                    'data': content,
                    'timestamp': datetime.now(),
                    'ttl': self.cache_ttl
                }
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to fetch content from {url}: {e}")
            raise
    
    async def _fetch_raw_content(self, url: str) -> Dict[str, Any]:
        """Fetch content from raw GitHub URL."""
        for attempt in range(self.max_retries):
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        return {
                            'content': content,
                            'url': url,
                            'size': len(content.encode('utf-8')),
                            'type': 'raw',
                            'encoding': 'utf-8',
                            'fetched_at': datetime.now().isoformat(),
                            'status': response.status,
                            'headers': dict(response.headers)
                        }
                    elif response.status == 404:
                        raise FileNotFoundError(f"Content not found: {url}")
                    elif response.status == 403:
                        raise PermissionError(f"Access denied: {url}")
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")
                        
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                
                logger.warning(f"Attempt {attempt + 1} failed, retrying: {e}")
                await asyncio.sleep(self.retry_delay * (attempt + 1))
    
    async def _fetch_api_content(self, url: str) -> Dict[str, Any]:
        """Fetch content using GitHub API."""
        for attempt in range(self.max_retries):
            try:
                # Check rate limit
                await self._check_rate_limit()
                
                async with self.session.get(url) as response:
                    # Update rate limit info
                    self._update_rate_limit(response.headers)
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Decode content if base64 encoded
                        content = data.get('content', '')
                        if data.get('encoding') == 'base64':
                            content = base64.b64decode(content).decode('utf-8')
                        
                        return {
                            'content': content,
                            'url': url,
                            'size': data.get('size', len(content.encode('utf-8'))),
                            'type': 'api',
                            'encoding': data.get('encoding', 'utf-8'),
                            'sha': data.get('sha'),
                            'path': data.get('path'),
                            'name': data.get('name'),
                            'fetched_at': datetime.now().isoformat(),
                            'status': response.status,
                            'api_data': data
                        }
                    elif response.status == 404:
                        raise FileNotFoundError(f"Content not found: {url}")
                    elif response.status == 403:
                        error_data = await response.json()
                        if 'rate limit' in error_data.get('message', '').lower():
                            await self._handle_rate_limit()
                            continue
                        raise PermissionError(f"Access denied: {url}")
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")
                        
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                
                logger.warning(f"Attempt {attempt + 1} failed, retrying: {e}")
                await asyncio.sleep(self.retry_delay * (attempt + 1))
    
    async def fetch_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository information."""
        url = f"{self.api_base}/repos/{owner}/{repo}"
        
        try:
            await self._check_rate_limit()
            
            async with self.session.get(url) as response:
                self._update_rate_limit(response.headers)
                
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise FileNotFoundError(f"Repository not found: {owner}/{repo}")
                else:
                    raise Exception(f"HTTP {response.status}: {await response.text()}")
                    
        except Exception as e:
            logger.error(f"Failed to fetch repository info: {e}")
            raise
    
    async def list_repository_contents(self, owner: str, repo: str, path: str = "") -> List[Dict[str, Any]]:
        """List repository contents."""
        url = f"{self.api_base}/repos/{owner}/{repo}/contents/{path}"
        
        try:
            await self._check_rate_limit()
            
            async with self.session.get(url) as response:
                self._update_rate_limit(response.headers)
                
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise FileNotFoundError(f"Path not found: {owner}/{repo}/{path}")
                else:
                    raise Exception(f"HTTP {response.status}: {await response.text()}")
                    
        except Exception as e:
            logger.error(f"Failed to list repository contents: {e}")
            raise
    
    async def search_repositories(self, query: str, sort: str = "updated", order: str = "desc") -> Dict[str, Any]:
        """Search repositories."""
        url = f"{self.api_base}/search/repositories"
        params = {
            'q': query,
            'sort': sort,
            'order': order
        }
        
        try:
            await self._check_rate_limit()
            
            async with self.session.get(url, params=params) as response:
                self._update_rate_limit(response.headers)
                
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"HTTP {response.status}: {await response.text()}")
                    
        except Exception as e:
            logger.error(f"Failed to search repositories: {e}")
            raise
    
    def _convert_to_raw_url(self, github_url: str) -> str:
        """Convert GitHub URL to raw content URL."""
        # Handle different GitHub URL formats
        if 'github.com' in github_url and '/blob/' in github_url:
            # Convert blob URL to raw URL
            return github_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        elif 'github.com' in github_url and '/tree/' in github_url:
            # Tree URLs can't be converted to raw URLs
            raise ValueError("Cannot convert tree URL to raw URL")
        else:
            # Assume it's already a raw URL or API URL
            return github_url
    
    def _get_cache_key(self, url: str) -> str:
        """Generate cache key for URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_cache_expired(self, cache_item: Dict[str, Any]) -> bool:
        """Check if cache item is expired."""
        timestamp = cache_item['timestamp']
        ttl = cache_item['ttl']
        return (datetime.now() - timestamp).total_seconds() > ttl
    
    async def _check_rate_limit(self):
        """Check and handle rate limiting."""
        if self.rate_limit_remaining <= 10:
            if datetime.now() < self.rate_limit_reset:
                wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
                logger.warning(f"Rate limit low, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
    
    def _update_rate_limit(self, headers: Dict[str, str]):
        """Update rate limit information from response headers."""
        if 'X-RateLimit-Remaining' in headers:
            self.rate_limit_remaining = int(headers['X-RateLimit-Remaining'])
        
        if 'X-RateLimit-Reset' in headers:
            self.rate_limit_reset = datetime.fromtimestamp(int(headers['X-RateLimit-Reset']))
    
    async def _handle_rate_limit(self):
        """Handle rate limit exceeded."""
        wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
        if wait_time > 0:
            logger.warning(f"Rate limit exceeded, waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
    
    def clear_cache(self, pattern: Optional[str] = None):
        """Clear cache entries."""
        if pattern:
            # Clear entries matching pattern
            keys_to_remove = [key for key in self.cache.keys() if pattern in key]
            for key in keys_to_remove:
                del self.cache[key]
            return len(keys_to_remove)
        else:
            # Clear all cache
            count = len(self.cache)
            self.cache.clear()
            return count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self.cache)
        expired_entries = sum(1 for item in self.cache.values() if self._is_cache_expired(item))
        
        return {
            'total_entries': total_entries,
            'expired_entries': expired_entries,
            'active_entries': total_entries - expired_entries,
            'cache_ttl': self.cache_ttl,
            'memory_usage': sum(len(str(item)) for item in self.cache.values())
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        try:
            # Test API connection
            async with self.session.get(f"{self.api_base}/rate_limit") as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'status': 'healthy',
                        'rate_limit': {
                            'remaining': data['rate']['remaining'],
                            'limit': data['rate']['limit'],
                            'reset': datetime.fromtimestamp(data['rate']['reset']).isoformat()
                        },
                        'cache_stats': self.get_cache_stats()
                    }
                else:
                    return {
                        'status': 'unhealthy',
                        'error': f"API returned status {response.status}"
                    }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("🧹 Cleaning up GitHub client...")
        
        if self.session:
            await self.session.close()
            self.session = None
        
        self.cache.clear()
        
        logger.info("✅ GitHub client cleanup complete")

# Utility functions
def parse_github_url(url: str) -> Dict[str, str]:
    """Parse GitHub URL and extract components."""
    parsed = urlparse(url)
    
    if 'github.com' in parsed.netloc:
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return {
                'owner': path_parts[0],
                'repo': path_parts[1],
                'type': path_parts[2] if len(path_parts) > 2 else 'repo',
                'branch': path_parts[3] if len(path_parts) > 3 else 'main',
                'path': '/'.join(path_parts[4:]) if len(path_parts) > 4 else ''
            }
    elif 'raw.githubusercontent.com' in parsed.netloc:
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 3:
            return {
                'owner': path_parts[0],
                'repo': path_parts[1],
                'branch': path_parts[2],
                'path': '/'.join(path_parts[3:]) if len(path_parts) > 3 else ''
            }
    
    raise ValueError(f"Invalid GitHub URL: {url}")

def build_raw_url(owner: str, repo: str, path: str, branch: str = "main") -> str:
    """Build raw GitHub URL."""
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

def build_api_url(owner: str, repo: str, path: str) -> str:
    """Build GitHub API URL."""
    return f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"