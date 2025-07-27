"""
Link Testing & Cross-Reference Validation System
Test all internal and external links, validate cross-references and navigation structure
"""

import asyncio
import aiohttp
import re
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse, urljoin, unquote
import ssl

logger = logging.getLogger(__name__)


class LinkType(str, Enum):
    """Types of links."""
    INTERNAL_FILE = "internal_file"
    INTERNAL_ANCHOR = "internal_anchor"
    EXTERNAL_HTTP = "external_http"
    EXTERNAL_HTTPS = "external_https"
    EMAIL = "email"
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


class LinkStatus(str, Enum):
    """Link validation status."""
    VALID = "valid"
    BROKEN = "broken"
    REDIRECT = "redirect"
    TIMEOUT = "timeout"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


@dataclass
class LinkInfo:
    """Link information and metadata."""
    link_id: str
    link_type: LinkType
    url: str
    text: str
    source_file: str
    line_number: int
    status: LinkStatus
    status_code: Optional[int]
    redirect_url: Optional[str]
    response_time_ms: float
    error_message: Optional[str]


@dataclass
class CrossReference:
    """Cross-reference between documents."""
    ref_id: str
    source_file: str
    target_file: str
    anchor: Optional[str]
    link_text: str
    valid: bool
    bidirectional: bool


@dataclass
class NavigationStructure:
    """Navigation structure analysis."""
    structure_id: str
    root_documents: List[str]
    document_hierarchy: Dict[str, List[str]]
    orphaned_documents: List[str]
    circular_references: List[List[str]]
    max_depth: int
    total_documents: int


@dataclass
class ValidationReport:
    """Link validation report."""
    report_id: str
    total_links: int
    valid_links: int
    broken_links: int
    external_links: int
    internal_links: int
    links_by_status: Dict[str, int]
    cross_references: List[CrossReference]
    navigation_structure: NavigationStructure
    validation_duration_seconds: float
    timestamp: float


class LinkValidator:
    """
    Link Testing & Cross-Reference Validation System
    
    Provides comprehensive link validation including:
    - Internal and external link testing
    - Cross-reference validation
    - Navigation structure analysis
    - Broken link detection
    - Performance monitoring
    """
    
    def __init__(self, base_path: str = ".", timeout_seconds: int = 10):
        self.base_path = Path(base_path)
        self.timeout_seconds = timeout_seconds
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Validation results
        self.link_results: List[LinkInfo] = []
        self.cross_references: List[CrossReference] = []
        self.validation_reports: List[ValidationReport] = []
        
        # Configuration
        self.config = {
            "max_concurrent_requests": 10,
            "retry_attempts": 3,
            "retry_delay_seconds": 1,
            "user_agent": "JAEGIS-LinkValidator/1.0",
            "follow_redirects": True,
            "validate_anchors": True,
            "check_external_links": True,
            "ignore_patterns": [
                r"^mailto:",
                r"^tel:",
                r"^javascript:",
                r"^#$"  # Empty anchors
            ]
        }
        
        logger.info(f"Link Validator initialized for {base_path}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        connector = aiohttp.TCPConnector(
            limit=self.config["max_concurrent_requests"],
            ssl=ssl.create_default_context()
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": self.config["user_agent"]}
        )
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def validate_all_links(self, file_paths: List[str]) -> ValidationReport:
        """Validate all links in specified files."""
        
        validation_start = time.time()
        report_id = f"validation_{int(time.time())}"
        
        logger.info(f"Starting link validation for {len(file_paths)} files")
        
        # Extract all links from files
        all_links = await self._extract_all_links(file_paths)
        
        # Validate links
        validated_links = await self._validate_links(all_links)
        
        # Analyze cross-references
        cross_refs = await self._analyze_cross_references(file_paths, validated_links)
        
        # Analyze navigation structure
        nav_structure = await self._analyze_navigation_structure(file_paths, validated_links)
        
        # Generate statistics
        total_links = len(validated_links)
        valid_links = len([l for l in validated_links if l.status == LinkStatus.VALID])
        broken_links = len([l for l in validated_links if l.status in [LinkStatus.BROKEN, LinkStatus.NOT_FOUND]])
        external_links = len([l for l in validated_links if l.link_type in [LinkType.EXTERNAL_HTTP, LinkType.EXTERNAL_HTTPS]])
        internal_links = total_links - external_links
        
        # Count by status
        links_by_status = {}
        for status in LinkStatus:
            links_by_status[status.value] = len([l for l in validated_links if l.status == status])
        
        # Create validation report
        report = ValidationReport(
            report_id=report_id,
            total_links=total_links,
            valid_links=valid_links,
            broken_links=broken_links,
            external_links=external_links,
            internal_links=internal_links,
            links_by_status=links_by_status,
            cross_references=cross_refs,
            navigation_structure=nav_structure,
            validation_duration_seconds=time.time() - validation_start,
            timestamp=time.time()
        )
        
        # Store results
        self.link_results.extend(validated_links)
        self.cross_references.extend(cross_refs)
        self.validation_reports.append(report)
        
        logger.info(f"Link validation completed: {valid_links}/{total_links} valid links")
        
        return report
    
    async def _extract_all_links(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Extract all links from specified files."""
        
        all_links = []
        
        for file_path in file_paths:
            try:
                links = await self._extract_links_from_file(file_path)
                all_links.extend(links)
                
            except Exception as e:
                logger.error(f"Failed to extract links from {file_path}: {e}")
        
        logger.info(f"Extracted {len(all_links)} links from {len(file_paths)} files")
        
        return all_links
    
    async def _extract_links_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract links from a single file."""
        
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Markdown link pattern: [text](url)
            markdown_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
            
            # HTML link pattern: <a href="url">text</a>
            html_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'
            
            # Reference link pattern: [text][ref] and [ref]: url
            ref_pattern = r'\[([^\]]+)\]\[([^\]]+)\]'
            ref_def_pattern = r'^\[([^\]]+)\]:\s*(.+)$'
            
            # Extract reference definitions first
            ref_definitions = {}
            for line_num, line in enumerate(lines, 1):
                ref_match = re.search(ref_def_pattern, line.strip())
                if ref_match:
                    ref_id = ref_match.group(1)
                    ref_url = ref_match.group(2).strip()
                    ref_definitions[ref_id] = ref_url
            
            # Extract links
            for line_num, line in enumerate(lines, 1):
                # Markdown links
                for match in re.finditer(markdown_pattern, line):
                    link_text = match.group(1)
                    link_url = match.group(2)
                    
                    if not self._should_ignore_link(link_url):
                        links.append({
                            "text": link_text,
                            "url": link_url,
                            "source_file": file_path,
                            "line_number": line_num,
                            "type": "markdown"
                        })
                
                # HTML links
                for match in re.finditer(html_pattern, line):
                    link_url = match.group(1)
                    link_text = match.group(2)
                    
                    if not self._should_ignore_link(link_url):
                        links.append({
                            "text": link_text,
                            "url": link_url,
                            "source_file": file_path,
                            "line_number": line_num,
                            "type": "html"
                        })
                
                # Reference links
                for match in re.finditer(ref_pattern, line):
                    link_text = match.group(1)
                    ref_id = match.group(2)
                    
                    if ref_id in ref_definitions:
                        link_url = ref_definitions[ref_id]
                        
                        if not self._should_ignore_link(link_url):
                            links.append({
                                "text": link_text,
                                "url": link_url,
                                "source_file": file_path,
                                "line_number": line_num,
                                "type": "reference"
                            })
        
        except Exception as e:
            logger.error(f"Error extracting links from {file_path}: {e}")
        
        return links
    
    def _should_ignore_link(self, url: str) -> bool:
        """Check if link should be ignored based on patterns."""
        
        for pattern in self.config["ignore_patterns"]:
            if re.match(pattern, url):
                return True
        
        return False
    
    async def _validate_links(self, links: List[Dict[str, Any]]) -> List[LinkInfo]:
        """Validate all extracted links."""
        
        validated_links = []
        
        # Create semaphore for concurrent requests
        semaphore = asyncio.Semaphore(self.config["max_concurrent_requests"])
        
        # Validate links concurrently
        tasks = []
        for i, link_data in enumerate(links):
            task = self._validate_single_link(semaphore, i, link_data)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, LinkInfo):
                validated_links.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Link validation error: {result}")
        
        return validated_links
    
    async def _validate_single_link(self, semaphore: asyncio.Semaphore, 
                                  link_index: int, link_data: Dict[str, Any]) -> LinkInfo:
        """Validate a single link."""
        
        async with semaphore:
            link_id = f"link_{link_index}_{int(time.time())}"
            url = link_data["url"]
            
            # Determine link type
            link_type = self._determine_link_type(url)
            
            validation_start = time.time()
            status = LinkStatus.UNKNOWN
            status_code = None
            redirect_url = None
            error_message = None
            
            try:
                if link_type in [LinkType.EXTERNAL_HTTP, LinkType.EXTERNAL_HTTPS]:
                    # Validate external link
                    status, status_code, redirect_url, error_message = await self._validate_external_link(url)
                
                elif link_type in [LinkType.INTERNAL_FILE, LinkType.RELATIVE]:
                    # Validate internal link
                    status, error_message = await self._validate_internal_link(url, link_data["source_file"])
                
                elif link_type == LinkType.INTERNAL_ANCHOR:
                    # Validate anchor link
                    status, error_message = await self._validate_anchor_link(url, link_data["source_file"])
                
                elif link_type == LinkType.EMAIL:
                    # Email links are considered valid if properly formatted
                    status = LinkStatus.VALID if "@" in url else LinkStatus.BROKEN
                
                else:
                    status = LinkStatus.UNKNOWN
                    error_message = f"Unsupported link type: {link_type}"
            
            except Exception as e:
                status = LinkStatus.BROKEN
                error_message = str(e)
            
            response_time = (time.time() - validation_start) * 1000  # milliseconds
            
            return LinkInfo(
                link_id=link_id,
                link_type=link_type,
                url=url,
                text=link_data["text"],
                source_file=link_data["source_file"],
                line_number=link_data["line_number"],
                status=status,
                status_code=status_code,
                redirect_url=redirect_url,
                response_time_ms=response_time,
                error_message=error_message
            )
    
    def _determine_link_type(self, url: str) -> LinkType:
        """Determine the type of link."""
        
        if url.startswith("mailto:"):
            return LinkType.EMAIL
        elif url.startswith("https://"):
            return LinkType.EXTERNAL_HTTPS
        elif url.startswith("http://"):
            return LinkType.EXTERNAL_HTTP
        elif url.startswith("#"):
            return LinkType.INTERNAL_ANCHOR
        elif url.startswith("/"):
            return LinkType.ABSOLUTE
        elif "://" in url:
            return LinkType.EXTERNAL_HTTPS  # Assume HTTPS for other protocols
        else:
            return LinkType.RELATIVE
    
    async def _validate_external_link(self, url: str) -> Tuple[LinkStatus, Optional[int], Optional[str], Optional[str]]:
        """Validate external HTTP/HTTPS link."""
        
        if not self.session:
            return LinkStatus.BROKEN, None, None, "No HTTP session available"
        
        for attempt in range(self.config["retry_attempts"]):
            try:
                async with self.session.head(url, allow_redirects=self.config["follow_redirects"]) as response:
                    if response.status == 200:
                        redirect_url = str(response.url) if str(response.url) != url else None
                        return LinkStatus.VALID, response.status, redirect_url, None
                    
                    elif response.status in [301, 302, 303, 307, 308]:
                        return LinkStatus.REDIRECT, response.status, str(response.url), None
                    
                    elif response.status == 404:
                        return LinkStatus.NOT_FOUND, response.status, None, "Page not found"
                    
                    elif response.status == 403:
                        return LinkStatus.FORBIDDEN, response.status, None, "Access forbidden"
                    
                    else:
                        return LinkStatus.BROKEN, response.status, None, f"HTTP {response.status}"
            
            except asyncio.TimeoutError:
                if attempt == self.config["retry_attempts"] - 1:
                    return LinkStatus.TIMEOUT, None, None, "Request timeout"
                await asyncio.sleep(self.config["retry_delay_seconds"])
            
            except Exception as e:
                if attempt == self.config["retry_attempts"] - 1:
                    return LinkStatus.BROKEN, None, None, str(e)
                await asyncio.sleep(self.config["retry_delay_seconds"])
        
        return LinkStatus.BROKEN, None, None, "Max retries exceeded"
    
    async def _validate_internal_link(self, url: str, source_file: str) -> Tuple[LinkStatus, Optional[str]]:
        """Validate internal file link."""
        
        try:
            # Resolve relative path
            source_dir = Path(source_file).parent
            
            if url.startswith("/"):
                # Absolute path from repository root
                target_path = self.base_path / url.lstrip("/")
            else:
                # Relative path from source file
                target_path = source_dir / url
            
            # Remove URL fragments and query parameters
            clean_url = url.split("#")[0].split("?")[0]
            target_path = source_dir / clean_url if not url.startswith("/") else self.base_path / clean_url.lstrip("/")
            
            # Resolve path
            target_path = target_path.resolve()
            
            if target_path.exists():
                return LinkStatus.VALID, None
            else:
                return LinkStatus.NOT_FOUND, f"File not found: {target_path}"
        
        except Exception as e:
            return LinkStatus.BROKEN, str(e)
    
    async def _validate_anchor_link(self, url: str, source_file: str) -> Tuple[LinkStatus, Optional[str]]:
        """Validate anchor link within document."""
        
        if not self.config["validate_anchors"]:
            return LinkStatus.VALID, None
        
        try:
            anchor = url.lstrip("#")
            
            if not anchor:
                return LinkStatus.VALID, None  # Empty anchor is valid
            
            # Read source file to check for anchor
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for heading that matches anchor
            heading_pattern = rf"^#+\s+.*{re.escape(anchor)}.*$"
            
            if re.search(heading_pattern, content, re.MULTILINE | re.IGNORECASE):
                return LinkStatus.VALID, None
            
            # Check for HTML anchor
            html_anchor_pattern = rf'<[^>]+id=["\']?{re.escape(anchor)}["\']?[^>]*>'
            
            if re.search(html_anchor_pattern, content, re.IGNORECASE):
                return LinkStatus.VALID, None
            
            return LinkStatus.NOT_FOUND, f"Anchor not found: #{anchor}"
        
        except Exception as e:
            return LinkStatus.BROKEN, str(e)
    
    async def _analyze_cross_references(self, file_paths: List[str], 
                                      validated_links: List[LinkInfo]) -> List[CrossReference]:
        """Analyze cross-references between documents."""
        
        cross_refs = []
        
        # Group links by source and target files
        file_links = {}
        for link in validated_links:
            if link.link_type in [LinkType.INTERNAL_FILE, LinkType.RELATIVE]:
                source = link.source_file
                
                # Determine target file
                if link.url.startswith("/"):
                    target = str(self.base_path / link.url.lstrip("/"))
                else:
                    source_dir = Path(link.source_file).parent
                    target = str(source_dir / link.url.split("#")[0])
                
                if source not in file_links:
                    file_links[source] = []
                
                file_links[source].append((target, link))
        
        # Create cross-reference objects
        ref_id = 0
        for source_file, targets in file_links.items():
            for target_file, link in targets:
                ref_id += 1
                
                # Check if reference is bidirectional
                bidirectional = False
                if target_file in file_links:
                    target_links = [t[0] for t in file_links[target_file]]
                    bidirectional = source_file in target_links
                
                cross_ref = CrossReference(
                    ref_id=f"ref_{ref_id}",
                    source_file=source_file,
                    target_file=target_file,
                    anchor=link.url.split("#")[1] if "#" in link.url else None,
                    link_text=link.text,
                    valid=link.status == LinkStatus.VALID,
                    bidirectional=bidirectional
                )
                
                cross_refs.append(cross_ref)
        
        return cross_refs
    
    async def _analyze_navigation_structure(self, file_paths: List[str], 
                                          validated_links: List[LinkInfo]) -> NavigationStructure:
        """Analyze navigation structure of documentation."""
        
        structure_id = f"nav_{int(time.time())}"
        
        # Build document graph
        document_graph = {}
        all_documents = set(file_paths)
        
        for link in validated_links:
            if link.link_type in [LinkType.INTERNAL_FILE, LinkType.RELATIVE] and link.status == LinkStatus.VALID:
                source = link.source_file
                
                # Determine target
                if link.url.startswith("/"):
                    target = str(self.base_path / link.url.lstrip("/"))
                else:
                    source_dir = Path(link.source_file).parent
                    target = str(source_dir / link.url.split("#")[0])
                
                if source not in document_graph:
                    document_graph[source] = []
                
                if target in all_documents:
                    document_graph[source].append(target)
        
        # Find root documents (documents with no incoming links)
        all_targets = set()
        for targets in document_graph.values():
            all_targets.update(targets)
        
        root_documents = [doc for doc in all_documents if doc not in all_targets]
        
        # Find orphaned documents (documents with no links in or out)
        linked_documents = set(document_graph.keys()) | all_targets
        orphaned_documents = [doc for doc in all_documents if doc not in linked_documents]
        
        # Calculate maximum depth
        max_depth = self._calculate_max_depth(document_graph, root_documents)
        
        # Detect circular references
        circular_refs = self._detect_circular_references(document_graph)
        
        return NavigationStructure(
            structure_id=structure_id,
            root_documents=root_documents,
            document_hierarchy=document_graph,
            orphaned_documents=orphaned_documents,
            circular_references=circular_refs,
            max_depth=max_depth,
            total_documents=len(all_documents)
        )
    
    def _calculate_max_depth(self, graph: Dict[str, List[str]], roots: List[str]) -> int:
        """Calculate maximum depth of document hierarchy."""
        
        max_depth = 0
        
        def dfs(node: str, depth: int, visited: Set[str]) -> int:
            if node in visited:
                return depth
            
            visited.add(node)
            current_max = depth
            
            for child in graph.get(node, []):
                child_depth = dfs(child, depth + 1, visited.copy())
                current_max = max(current_max, child_depth)
            
            return current_max
        
        for root in roots:
            depth = dfs(root, 0, set())
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _detect_circular_references(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """Detect circular references in document graph."""
        
        circular_refs = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> bool:
            if node in rec_stack:
                # Found cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                circular_refs.append(cycle)
                return True
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if dfs(neighbor, path + [neighbor]):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                dfs(node, [node])
        
        return circular_refs
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get comprehensive validation summary."""
        
        if not self.validation_reports:
            return {"error": "No validation reports available"}
        
        latest_report = self.validation_reports[-1]
        
        return {
            "total_links_validated": latest_report.total_links,
            "valid_links": latest_report.valid_links,
            "broken_links": latest_report.broken_links,
            "external_links": latest_report.external_links,
            "internal_links": latest_report.internal_links,
            "validation_success_rate": (latest_report.valid_links / latest_report.total_links * 100) if latest_report.total_links > 0 else 0,
            "cross_references": len(latest_report.cross_references),
            "bidirectional_references": len([cr for cr in latest_report.cross_references if cr.bidirectional]),
            "navigation_structure": {
                "root_documents": len(latest_report.navigation_structure.root_documents),
                "orphaned_documents": len(latest_report.navigation_structure.orphaned_documents),
                "max_depth": latest_report.navigation_structure.max_depth,
                "circular_references": len(latest_report.navigation_structure.circular_references)
            },
            "validation_duration": latest_report.validation_duration_seconds
        }


# Example usage
async def main():
    """Example usage of Link Validator."""
    
    async with LinkValidator(".") as validator:
        # Test files
        test_files = [
            "README.md",
            "docs/api.md",
            "CONTRIBUTING.md"
        ]
        
        # Validate all links
        report = await validator.validate_all_links(test_files)
        
        print(f"Link Validation Report:")
        print(f"  Total Links: {report.total_links}")
        print(f"  Valid Links: {report.valid_links}")
        print(f"  Broken Links: {report.broken_links}")
        print(f"  External Links: {report.external_links}")
        print(f"  Internal Links: {report.internal_links}")
        print(f"  Cross References: {len(report.cross_references)}")
        print(f"  Validation Duration: {report.validation_duration_seconds:.2f}s")
        
        # Navigation structure
        nav = report.navigation_structure
        print(f"\nNavigation Structure:")
        print(f"  Root Documents: {len(nav.root_documents)}")
        print(f"  Orphaned Documents: {len(nav.orphaned_documents)}")
        print(f"  Max Depth: {nav.max_depth}")
        print(f"  Circular References: {len(nav.circular_references)}")
        
        # Get summary
        summary = validator.get_validation_summary()
        print(f"\nValidation Summary:")
        print(f"  Success Rate: {summary['validation_success_rate']:.1f}%")
        print(f"  Bidirectional References: {summary['bidirectional_references']}")


if __name__ == "__main__":
    asyncio.run(main())
