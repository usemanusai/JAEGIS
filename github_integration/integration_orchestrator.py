"""
JAEGIS GitHub Integration - Main Integration Orchestrator
Coordinates GitHub fetching, A.M.A.S.I.A.P. Protocol, and agent squad operations

This module serves as the main orchestrator for the complete GitHub integration system,
coordinating all components designed by the Agent Creator.
"""

import asyncio
import logging
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# Import GitHub integration components
from github_integration.github_fetcher import GitHubFetcher, FetchResult, GitHubResource
from github_integration.amasiap_protocol import AMASIAPProtocol, EnhancementResult
from github_integration.squad_coordinator import GitHubIntegrationSquadCoordinator

logger = logging.getLogger(__name__)


@dataclass
class IntegrationRequest:
    """Request for GitHub integration processing."""
    user_input: str
    primary_github_url: Optional[str] = None
    enable_amasiap: bool = True
    enable_multi_fetch: bool = True
    fallback_content: Optional[str] = None


@dataclass
class IntegrationResult:
    """Result of complete GitHub integration processing."""
    success: bool
    enhanced_input: str
    primary_resource: Optional[GitHubResource] = None
    multi_fetch_resources: List[GitHubResource] = None
    amasiap_result: Optional[EnhancementResult] = None
    agent_deployment_result: Optional[Dict[str, Any]] = None
    processing_metadata: Dict[str, Any] = None
    error: Optional[str] = None


class GitHubIntegrationOrchestrator:
    """
    Main GitHub Integration Orchestrator
    
    Coordinates the complete GitHub integration system:
    - Single GitHub link fetching with fallback support
    - Multi-fetch discovery and coordination
    - A.M.A.S.I.A.P. Protocol automatic input enhancement
    - Agent squad coordination and deployment
    - Comprehensive error handling and fallback mechanisms
    """
    
    def __init__(self):
        self.github_fetcher: Optional[GitHubFetcher] = None
        self.amasiap_protocol = AMASIAPProtocol()
        self.squad_coordinator = GitHubIntegrationSquadCoordinator()
        
        # Default GitHub URLs for JAEGIS system
        self.default_github_urls = {
            "guidelines": "https://github.com/usemanusai/JAEGIS/GOLD.md",
            "commands": "https://raw.githubusercontent.com/usemanusai/JAEGIS/main/commands/commands.md",
            "agent_config": "https://raw.githubusercontent.com/usemanusai/JAEGIS/main/core/agent-config.txt",
            "enhanced_config": "https://raw.githubusercontent.com/usemanusai/JAEGIS/main/core/enhanced-agent-config.txt",
            "ai_config": "https://raw.githubusercontent.com/usemanusai/JAEGIS/main/config/ai-config.json"
        }
        
        # Fallback content for when GitHub is unavailable
        self.fallback_content = {
            "guidelines": """
# JAEGIS Method - Fallback Guidelines

## Core Principles
1. Natural Language Interface - Primary interaction method
2. Automatic Mode Selection - N.L.D.S. with 85%+ confidence
3. Agent Squad Coordination - Specialized teams for complex tasks
4. GitHub Integration - Dynamic resource fetching
5. A.M.A.S.I.A.P. Protocol - Automatic input enhancement

## Available Modes
1. Documentation Mode - 3-agent team for documentation
2. Standard Development - 24-agent system for development
3. Enhanced Development - 68-agent system for complex projects
4. AI System Mode - Enhanced OpenRouter integration
5. Agent Creator Mode - 128+ agent system expansion

## Quick Start
Simply describe your request in natural language. The system will automatically:
- Analyze your input through N.L.D.S.
- Select the optimal mode
- Activate appropriate agents
- Fetch relevant GitHub resources
- Apply A.M.A.S.I.A.P. Protocol enhancement
""",
            "commands": """
# JAEGIS Commands - Fallback

## Natural Language Commands (Primary)
- "Fetch JAEGIS guidelines"
- "Create documentation for my project"
- "Help me build a web application"
- "Expand the agent system"

## Traditional Commands (Fallback)
- /help - Display help
- /status - System status
- /github-sync - Refresh GitHub resources
- /create-agent - Create new agent
""",
            "basic_config": """
{
    "system": "JAEGIS v2.2 Phase 5",
    "architecture": "7-tier",
    "agents": "128+",
    "primary_interface": "N.L.D.S.",
    "github_integration": true,
    "amasiap_protocol": true
}
"""
        }
        
        logger.info("GitHub Integration Orchestrator initialized")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.github_fetcher = GitHubFetcher()
        await self.github_fetcher.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.github_fetcher:
            await self.github_fetcher.__aexit__(exc_type, exc_val, exc_tb)
    
    async def process_github_integration(self, request: IntegrationRequest) -> IntegrationResult:
        """
        Process complete GitHub integration request.
        
        Args:
            request: Integration request with user input and parameters
            
        Returns:
            IntegrationResult with comprehensive processing results
        """
        start_time = time.time()
        
        logger.info(f"🚀 Processing GitHub integration request: {request.user_input[:100]}...")
        
        try:
            # Step 1: Apply A.M.A.S.I.A.P. Protocol if enabled
            amasiap_result = None
            enhanced_input = request.user_input
            
            if request.enable_amasiap:
                logger.info("⚡ Applying A.M.A.S.I.A.P. Protocol...")
                amasiap_operation = await self.squad_coordinator.coordinate_amasiap_protocol(request.user_input)
                
                if amasiap_operation.status.value == "idle":  # Success
                    # Simulate A.M.A.S.I.A.P. result (in production, use actual protocol)
                    amasiap_result = await self.amasiap_protocol.enhance_user_input(request.user_input)
                    enhanced_input = amasiap_result.enhanced_input
                    logger.info(f"✅ A.M.A.S.I.A.P. Protocol applied: {len(amasiap_result.research_queries)} research queries generated")
                else:
                    logger.warning("⚠️ A.M.A.S.I.A.P. Protocol coordination failed, continuing without enhancement")
            
            # Step 2: Determine GitHub URL
            github_url = request.primary_github_url or self._determine_github_url(request.user_input)
            
            # Step 3: Fetch primary GitHub resource
            primary_resource = None
            if github_url:
                logger.info(f"📋 Fetching primary GitHub resource: {github_url}")
                guideline_operation = await self.squad_coordinator.coordinate_guideline_fetching(github_url)
                
                if guideline_operation.status.value == "idle":  # Success
                    # Fetch actual resource
                    if self.github_fetcher:
                        fetch_result = await self.github_fetcher.fetch_single_github_link(github_url)
                        if fetch_result.success:
                            primary_resource = fetch_result.resource
                            logger.info(f"✅ Primary resource fetched: {len(primary_resource.content)} characters")
                        else:
                            logger.warning(f"⚠️ Primary fetch failed: {fetch_result.error}")
                else:
                    logger.warning("⚠️ Guideline fetching coordination failed")
            
            # Step 4: Multi-fetch if enabled and primary resource available
            multi_fetch_resources = []
            if request.enable_multi_fetch and primary_resource and primary_resource.links_found:
                logger.info(f"🔍 Performing multi-fetch: {len(primary_resource.links_found)} links found")
                multi_fetch_operation = await self.squad_coordinator.coordinate_multi_fetch(github_url, max_additional=10)
                
                if multi_fetch_operation.status.value == "idle":  # Success
                    # Perform actual multi-fetch
                    if self.github_fetcher:
                        multi_results = await self.github_fetcher.multi_fetch_github_resources(github_url, max_additional_fetches=10)
                        multi_fetch_resources = [
                            result.resource for result in multi_results.values() 
                            if result.success and result.resource
                        ]
                        logger.info(f"✅ Multi-fetch complete: {len(multi_fetch_resources)} additional resources")
                else:
                    logger.warning("⚠️ Multi-fetch coordination failed")
            
            # Step 5: Apply fallback if no resources fetched
            if not primary_resource:
                logger.info("🛡️ Applying fallback content...")
                fallback_content = request.fallback_content or self._get_fallback_content(request.user_input)
                primary_resource = GitHubResource(
                    url="fallback://local",
                    content=fallback_content,
                    resource_type="fallback",
                    metadata={"source": "local_fallback"},
                    fetched_at=time.time(),
                    cache_key="fallback",
                    links_found=[]
                )
            
            # Step 6: Create processing metadata
            processing_metadata = {
                "processing_time": time.time() - start_time,
                "amasiap_applied": request.enable_amasiap and amasiap_result is not None,
                "multi_fetch_applied": request.enable_multi_fetch,
                "primary_resource_source": "github" if github_url else "fallback",
                "additional_resources_count": len(multi_fetch_resources),
                "total_content_length": (
                    len(primary_resource.content) + 
                    sum(len(r.content) for r in multi_fetch_resources)
                ),
                "github_url_used": github_url,
                "fallback_used": not github_url or primary_resource.url == "fallback://local",
                "squad_coordination_used": True,
                "processing_timestamp": time.time()
            }
            
            # Create successful result
            result = IntegrationResult(
                success=True,
                enhanced_input=enhanced_input,
                primary_resource=primary_resource,
                multi_fetch_resources=multi_fetch_resources,
                amasiap_result=amasiap_result,
                processing_metadata=processing_metadata
            )
            
            logger.info(f"✅ GitHub integration processing complete in {processing_metadata['processing_time']:.2f}s")
            
            return result
        
        except Exception as e:
            logger.error(f"❌ Error in GitHub integration processing: {e}")
            
            # Create error result with fallback
            fallback_content = request.fallback_content or self._get_fallback_content(request.user_input)
            
            return IntegrationResult(
                success=False,
                enhanced_input=request.user_input,
                primary_resource=GitHubResource(
                    url="fallback://error",
                    content=fallback_content,
                    resource_type="error_fallback",
                    metadata={"error": str(e)},
                    fetched_at=time.time(),
                    cache_key="error_fallback",
                    links_found=[]
                ),
                processing_metadata={
                    "processing_time": time.time() - start_time,
                    "error_occurred": True,
                    "fallback_used": True
                },
                error=str(e)
            )
    
    def _determine_github_url(self, user_input: str) -> Optional[str]:
        """Determine appropriate GitHub URL based on user input."""
        input_lower = user_input.lower()
        
        # Check for specific requests
        if any(keyword in input_lower for keyword in ['guideline', 'gold', 'method', 'jaegis']):
            return self.default_github_urls["guidelines"]
        elif any(keyword in input_lower for keyword in ['command', 'help', 'usage']):
            return self.default_github_urls["commands"]
        elif any(keyword in input_lower for keyword in ['config', 'configuration', 'agent']):
            return self.default_github_urls["agent_config"]
        elif any(keyword in input_lower for keyword in ['ai', 'openrouter', 'model']):
            return self.default_github_urls["ai_config"]
        else:
            # Default to guidelines for general requests
            return self.default_github_urls["guidelines"]
    
    def _get_fallback_content(self, user_input: str) -> str:
        """Get appropriate fallback content based on user input."""
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ['command', 'help', 'usage']):
            return self.fallback_content["commands"]
        elif any(keyword in input_lower for keyword in ['config', 'configuration']):
            return self.fallback_content["basic_config"]
        else:
            return self.fallback_content["guidelines"]
    
    async def fetch_jaegis_guidelines(self, enable_multi_fetch: bool = True) -> IntegrationResult:
        """Convenience method to fetch JAEGIS guidelines."""
        request = IntegrationRequest(
            user_input="Fetch JAEGIS guidelines",
            primary_github_url=self.default_github_urls["guidelines"],
            enable_amasiap=False,  # Skip A.M.A.S.I.A.P. for simple fetch
            enable_multi_fetch=enable_multi_fetch
        )
        return await self.process_github_integration(request)
    
    async def enhance_with_amasiap(self, user_input: str) -> IntegrationResult:
        """Convenience method to enhance input with A.M.A.S.I.A.P. Protocol."""
        request = IntegrationRequest(
            user_input=user_input,
            enable_amasiap=True,
            enable_multi_fetch=False  # Focus on enhancement
        )
        return await self.process_github_integration(request)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        squad_status = self.squad_coordinator.get_squad_status()
        coordination_stats = self.squad_coordinator.get_coordination_stats()
        amasiap_stats = self.amasiap_protocol.get_protocol_stats()
        
        cache_stats = {}
        if self.github_fetcher:
            cache_stats = self.github_fetcher.get_cache_stats()
        
        return {
            "orchestrator_status": "operational",
            "github_fetcher_available": self.github_fetcher is not None,
            "amasiap_protocol_available": True,
            "squad_coordinator_available": True,
            "default_github_urls": self.default_github_urls,
            "fallback_content_available": True,
            "squad_status": squad_status,
            "coordination_stats": coordination_stats,
            "amasiap_stats": amasiap_stats,
            "cache_stats": cache_stats,
            "system_capabilities": [
                "Single GitHub link fetching",
                "Multi-fetch discovery and coordination",
                "A.M.A.S.I.A.P. Protocol enhancement",
                "Agent squad coordination",
                "Comprehensive fallback mechanisms",
                "Intelligent caching and optimization"
            ]
        }


# Global orchestrator instance
GITHUB_INTEGRATION_ORCHESTRATOR = GitHubIntegrationOrchestrator()


# Main convenience function for single-line usage
async def process_github_integration(user_input: str, 
                                   github_url: Optional[str] = None,
                                   enable_amasiap: bool = True,
                                   enable_multi_fetch: bool = True,
                                   fallback_content: Optional[str] = None) -> IntegrationResult:
    """
    Single-line function for complete GitHub integration processing.
    
    Args:
        user_input: User input to process
        github_url: Optional specific GitHub URL
        enable_amasiap: Whether to apply A.M.A.S.I.A.P. Protocol
        enable_multi_fetch: Whether to enable multi-fetch
        fallback_content: Optional fallback content
        
    Returns:
        IntegrationResult with comprehensive processing results
    """
    async with GitHubIntegrationOrchestrator() as orchestrator:
        request = IntegrationRequest(
            user_input=user_input,
            primary_github_url=github_url,
            enable_amasiap=enable_amasiap,
            enable_multi_fetch=enable_multi_fetch,
            fallback_content=fallback_content
        )
        return await orchestrator.process_github_integration(request)


# Example usage
async def main():
    """Example usage of GitHub Integration Orchestrator."""
    
    print("🚀 GITHUB INTEGRATION ORCHESTRATOR - Example Usage")
    
    # Example 1: Complete integration with A.M.A.S.I.A.P. Protocol
    print(f"\n⚡ Complete integration with A.M.A.S.I.A.P. Protocol...")
    result1 = await process_github_integration(
        "I need to create a web application for project management",
        enable_amasiap=True,
        enable_multi_fetch=True
    )
    
    print(f"   Success: {result1.success}")
    print(f"   Processing time: {result1.processing_metadata['processing_time']:.2f}s")
    print(f"   A.M.A.S.I.A.P. applied: {result1.processing_metadata['amasiap_applied']}")
    print(f"   Additional resources: {result1.processing_metadata['additional_resources_count']}")
    
    # Example 2: Simple guideline fetching
    print(f"\n📋 Simple guideline fetching...")
    result2 = await process_github_integration(
        "Fetch JAEGIS guidelines",
        github_url="https://github.com/usemanusai/JAEGIS/GOLD.md",
        enable_amasiap=False,
        enable_multi_fetch=True
    )
    
    print(f"   Success: {result2.success}")
    print(f"   Resource type: {result2.primary_resource.resource_type}")
    print(f"   Content length: {len(result2.primary_resource.content)} characters")
    
    # Example 3: System status
    async with GitHubIntegrationOrchestrator() as orchestrator:
        status = orchestrator.get_system_status()
        print(f"\n📊 System Status:")
        print(f"   Orchestrator: {status['orchestrator_status']}")
        print(f"   GitHub Fetcher: {'Available' if status['github_fetcher_available'] else 'Unavailable'}")
        print(f"   Squad Coordinator: {'Available' if status['squad_coordinator_available'] else 'Unavailable'}")
        print(f"   Capabilities: {len(status['system_capabilities'])} features")


if __name__ == "__main__":
    asyncio.run(main())