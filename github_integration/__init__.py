"""
JAEGIS GitHub Integration Package
Complete GitHub integration system with N.L.D.S. and A.M.A.S.I.A.P. Protocol

This package provides comprehensive GitHub integration capabilities including:
- Single GitHub link fetching with multi-fetch discovery
- A.M.A.S.I.A.P. Protocol for automatic input enhancement
- Agent squad coordination for specialized operations
- Comprehensive fallback mechanisms and error handling
"""

from github_integration.github_fetcher import (
    GitHubFetcher,
    GitHubResource,
    FetchResult,
    fetch_github_resource,
    multi_fetch_github_resources
)

from github_integration.amasiap_protocol import (
    AMASIAPProtocol,
    EnhancementResult,
    ResearchQuery,
    TaskPhase,
    enhance_input_with_amasiap
)

from github_integration.squad_coordinator import (
    GitHubIntegrationSquadCoordinator,
    SquadOperation,
    coordinate_github_guideline_fetching,
    coordinate_multi_fetch_operation,
    coordinate_amasiap_enhancement
)

from github_integration.integration_orchestrator import (
    GitHubIntegrationOrchestrator,
    IntegrationRequest,
    IntegrationResult,
    process_github_integration
)

# Package metadata
__version__ = "1.0.0"
__author__ = "JAEGIS Development Team"
__email__ = "use.manus.ai@gmail.com"
__description__ = "Complete GitHub integration system with N.L.D.S. and A.M.A.S.I.A.P. Protocol"

# Main exports for easy usage
__all__ = [
    # Core classes
    "GitHubFetcher",
    "AMASIAPProtocol", 
    "GitHubIntegrationSquadCoordinator",
    "GitHubIntegrationOrchestrator",
    
    # Data classes
    "GitHubResource",
    "FetchResult",
    "EnhancementResult",
    "ResearchQuery",
    "TaskPhase",
    "SquadOperation",
    "IntegrationRequest",
    "IntegrationResult",
    
    # Convenience functions
    "fetch_github_resource",
    "multi_fetch_github_resources",
    "enhance_input_with_amasiap",
    "coordinate_github_guideline_fetching",
    "coordinate_multi_fetch_operation", 
    "coordinate_amasiap_enhancement",
    "process_github_integration"
]

# Package-level convenience functions
async def quick_fetch_jaegis_guidelines():
    """Quick function to fetch JAEGIS guidelines."""
    return await process_github_integration(
        "Fetch JAEGIS guidelines",
        github_url="https://github.com/usemanusai/JAEGIS/GOLD.md",
        enable_amasiap=False,
        enable_multi_fetch=True
    )

async def quick_enhance_input(user_input: str):
    """Quick function to enhance input with A.M.A.S.I.A.P. Protocol."""
    return await process_github_integration(
        user_input,
        enable_amasiap=True,
        enable_multi_fetch=False
    )

async def quick_complete_integration(user_input: str, github_url: str = None):
    """Quick function for complete GitHub integration."""
    return await process_github_integration(
        user_input,
        github_url=github_url,
        enable_amasiap=True,
        enable_multi_fetch=True
    )

# Add quick functions to exports
__all__.extend([
    "quick_fetch_jaegis_guidelines",
    "quick_enhance_input", 
    "quick_complete_integration"
])

# Package information
def get_package_info():
    """Get package information."""
    return {
        "name": "github_integration",
        "version": __version__,
        "description": __description__,
        "author": __author__,
        "email": __email__,
        "components": [
            "GitHub Fetcher - Single link + multi-fetch system",
            "A.M.A.S.I.A.P. Protocol - Automatic input enhancement",
            "Squad Coordinator - Agent squad coordination",
            "Integration Orchestrator - Main coordination system"
        ],
        "capabilities": [
            "Single GitHub link fetching with fallback support",
            "Multi-fetch discovery and parallel processing",
            "A.M.A.S.I.A.P. Protocol with 15-20 research queries",
            "Agent squad coordination for specialized operations",
            "Comprehensive error handling and fallback mechanisms",
            "Intelligent caching and performance optimization"
        ],
        "performance_targets": {
            "github_fetch_time": "<5s",
            "amasiap_processing_time": "<2s", 
            "squad_coordination_time": "<3s",
            "cache_hit_rate": ">90%",
            "success_rate": ">95%"
        }
    }

# Module-level documentation
def print_usage_examples():
    """Print usage examples for the package."""
    examples = """
# JAEGIS GitHub Integration Package - Usage Examples

## 1. Simple GitHub Resource Fetching
```python
from github_integration import fetch_github_resource

result = await fetch_github_resource("https://github.com/usemanusai/JAEGIS/GOLD.md")
if result.success:
    print(f"Content: {result.resource.content[:100]}...")
```

## 2. Multi-Fetch with Discovery
```python
from github_integration import multi_fetch_github_resources

results = await multi_fetch_github_resources(
    "https://github.com/usemanusai/JAEGIS/GOLD.md",
    max_additional=10
)
print(f"Fetched {len(results)} resources")
```

## 3. A.M.A.S.I.A.P. Protocol Enhancement
```python
from github_integration import enhance_input_with_amasiap

result = await enhance_input_with_amasiap("Create a web application")
print(f"Research queries: {len(result.research_queries)}")
print(f"Task phases: {len(result.task_phases)}")
```

## 4. Complete Integration (Single Line)
```python
from github_integration import process_github_integration

result = await process_github_integration(
    "I need to create a web application",
    github_url="https://github.com/usemanusai/JAEGIS/GOLD.md",
    enable_amasiap=True,
    enable_multi_fetch=True
)
print(f"Success: {result.success}")
print(f"Enhanced input: {result.enhanced_input[:100]}...")
```

## 5. Quick Functions
```python
from github_integration import (
    quick_fetch_jaegis_guidelines,
    quick_enhance_input,
    quick_complete_integration
)

# Quick guideline fetch
guidelines = await quick_fetch_jaegis_guidelines()

# Quick input enhancement
enhanced = await quick_enhance_input("Build a mobile app")

# Quick complete integration
complete = await quick_complete_integration("Create documentation")
```

## 6. Squad Coordination
```python
from github_integration import coordinate_github_guideline_fetching

operation = await coordinate_github_guideline_fetching(
    "https://github.com/usemanusai/JAEGIS/GOLD.md"
)
print(f"Operation status: {operation.status}")
```
"""
    print(examples)

# Package initialization message
import logging
logger = logging.getLogger(__name__)
logger.info(f"JAEGIS GitHub Integration Package v{__version__} initialized")
logger.info("Components: GitHub Fetcher, A.M.A.S.I.A.P. Protocol, Squad Coordinator, Integration Orchestrator")
logger.info("Ready for single-line GitHub integration with automatic enhancement")