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
from github_integration.squad_coordinator import GitHubSquadCoordinator, initialize_squad_coordinator
from jaegis_github_integration_system import GitHubIntegrationAgentCreator

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
    Main orchestrator for JAEGIS GitHub Integration System
    
    Coordinates:
    1. GitHub guideline fetching (single link)
    2. Multi-fetch discovery and execution
    3. A.M.A.S.I.A.P. Protocol enhancement
    4. Agent squad deployment and coordination
    5. Comprehensive result integration
    """
    
    def __init__(self):
        # Initialize core components
        self.github_fetcher = GitHubFetcher()
        self.amasiap_protocol = AMASIAPProtocol()
        self.agent_creator = GitHubIntegrationAgentCreator()
        self.squad_coordinator: Optional[GitHubSquadCoordinator] = None

        # System state
        self.initialized = False
        self.agents_deployed = False
        
        # Configuration
        self.config = {
            "default_github_url": "https://github.com/usemanusai/JAEGIS/GOLD.md",
            "enable_agent_deployment": True,
            "enable_comprehensive_logging": True,
            "max_processing_time": 120,  # 2 minutes
            "fallback_guidelines": """
# JAEGIS Method Guidelines (Fallback)

## Your Role
You are JAEGIS, Master of the JAEGIS Method - AI Agent Orchestrator with GitHub integration.

## Primary Functions
1. GitHub-Local Integration - Coordinate local agents with GitHub resources
2. Dynamic Resource Fetching - Load GitHub content on-demand
3. A.M.A.S.I.A.P. Protocol - Always Modify And Send Input Automatically
4. Multi-Agent Orchestration - Manage specialized agent system

## Core Capabilities
- Single GitHub link fetching with multi-fetch discovery
- Automatic input enhancement with comprehensive research
- Systematic task breakdown and implementation planning
- Agent-based system coordination and management
            """
        }
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_integrations": 0,
            "github_fetches": 0,
            "amasiap_enhancements": 0,
            "agent_deployments": 0
        }
        
        logger.info("GitHub Integration Orchestrator initialized")
    
    async def initialize(self):
        """Initialize the complete integration system."""
        
        if self.initialized:
            return
        
        logger.info("🚀 Initializing GitHub Integration System...")
        
        try:
            # Initialize GitHub fetcher
            await self.github_fetcher.initialize()
            
            # Activate A.M.A.S.I.A.P. Protocol
            await self.amasiap_protocol.activate_protocol()
            
            # Deploy GitHub integration agents if enabled
            if self.config["enable_agent_deployment"]:
                deployment_result = await self.agent_creator.deploy_github_integration_system()
                self.agents_deployed = True
                self.stats["agent_deployments"] += 1

                # Initialize squad coordinator
                self.squad_coordinator = initialize_squad_coordinator(self.agent_creator)
                await self.squad_coordinator.initialize_squad_coordination()

                logger.info(f"✅ Agents deployed: {deployment_result['github_agents_created']} agents, {deployment_result['github_squads_created']} squads")
            
            self.initialized = True
            logger.info("✅ GitHub Integration System initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize GitHub Integration System: {e}")
            raise
    
    async def process_integration_request(self, request: IntegrationRequest) -> IntegrationResult:
        """
        Process complete GitHub integration request.
        
        Args:
            request: IntegrationRequest with user input and configuration
        
        Returns:
            IntegrationResult with comprehensive processing results
        """
        
        if not self.initialized:
            await self.initialize()
        
        logger.info("🔄 Processing GitHub integration request...")
        
        start_time = time.time()
        self.stats["total_requests"] += 1
        
        try:
            # Step 1: Apply A.M.A.S.I.A.P. Protocol if enabled
            amasiap_result = None
            enhanced_input = request.user_input
            
            if request.enable_amasiap:
                logger.info("🧠 Applying A.M.A.S.I.A.P. Protocol...")
                amasiap_result = await self.amasiap_protocol.enhance_input_automatically(request.user_input)
                enhanced_input = amasiap_result.enhanced_input
                self.stats["amasiap_enhancements"] += 1
                logger.info(f"✅ A.M.A.S.I.A.P. enhancement complete")
            
            # Step 2: Fetch primary GitHub resource
            primary_resource = None
            github_url = request.primary_github_url or self.config["default_github_url"]
            
            logger.info(f"📥 Fetching primary GitHub resource: {github_url}")
            fetch_result = await self.github_fetcher.fetch_github_guideline(github_url)
            
            if fetch_result.success:
                primary_resource = fetch_result.resource
                self.stats["github_fetches"] += 1
                logger.info(f"✅ Primary resource fetched successfully")
            else:
                logger.warning(f"⚠️ Primary fetch failed: {fetch_result.error}")
                # Use fallback content
                primary_resource = self._create_fallback_resource(github_url)
            
            # Step 3: Perform multi-fetch if enabled and links discovered
            multi_fetch_resources = []
            
            if request.enable_multi_fetch and primary_resource and primary_resource.links_found:
                logger.info(f"🔄 Starting multi-fetch for {len(primary_resource.links_found)} discovered links")
                multi_fetch_results = await self.github_fetcher.multi_fetch_from_guideline(primary_resource)
                
                multi_fetch_resources = [
                    result.resource for result in multi_fetch_results 
                    if result.success and result.resource
                ]
                
                logger.info(f"✅ Multi-fetch complete: {len(multi_fetch_resources)} resources fetched")
            
            # Step 4: Create comprehensive result
            processing_time = time.time() - start_time
            
            result = IntegrationResult(
                success=True,
                enhanced_input=enhanced_input,
                primary_resource=primary_resource,
                multi_fetch_resources=multi_fetch_resources,
                amasiap_result=amasiap_result,
                agent_deployment_result=self._get_agent_deployment_status(),
                processing_metadata={
                    "processing_time": processing_time,
                    "github_fetches_performed": 1 + len(multi_fetch_resources),
                    "amasiap_applied": request.enable_amasiap,
                    "multi_fetch_enabled": request.enable_multi_fetch,
                    "agents_deployed": self.agents_deployed,
                    "primary_url": github_url,
                    "links_discovered": len(primary_resource.links_found) if primary_resource and primary_resource.links_found else 0,
                    "total_resources_fetched": 1 + len(multi_fetch_resources)
                }
            )
            
            self.stats["successful_integrations"] += 1
            
            logger.info(f"✅ GitHub integration complete in {processing_time:.2f}s")
            logger.info(f"  Enhanced input: {len(enhanced_input)} characters")
            logger.info(f"  Resources fetched: {1 + len(multi_fetch_resources)}")
            logger.info(f"  A.M.A.S.I.A.P. applied: {request.enable_amasiap}")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ GitHub integration failed: {e}")
            
            return IntegrationResult(
                success=False,
                enhanced_input=request.user_input,
                error=str(e),
                processing_metadata={
                    "processing_time": processing_time,
                    "error_occurred": True
                }
            )
    
    async def fetch_github_guideline_only(self, url: str) -> FetchResult:
        """
        Convenience method to fetch only a GitHub guideline without full integration.
        
        Args:
            url: GitHub URL to fetch
        
        Returns:
            FetchResult with the fetched resource
        """
        
        if not self.initialized:
            await self.initialize()
        
        return await self.github_fetcher.fetch_github_guideline(url)
    
    async def enhance_input_only(self, user_input: str) -> EnhancementResult:
        """
        Convenience method to apply only A.M.A.S.I.A.P. Protocol enhancement.
        
        Args:
            user_input: User input to enhance
        
        Returns:
            EnhancementResult with enhanced input and research
        """
        
        if not self.initialized:
            await self.initialize()
        
        return await self.amasiap_protocol.enhance_input_automatically(user_input)
    
    def _create_fallback_resource(self, url: str) -> GitHubResource:
        """Create fallback resource when GitHub fetch fails."""
        
        return GitHubResource(
            url=url,
            content=self.config["fallback_guidelines"],
            resource_type="markdown",
            metadata={
                "fallback": True,
                "content_length": len(self.config["fallback_guidelines"]),
                "resource_type": "markdown"
            },
            fetched_at=time.time(),
            cache_key=f"fallback_{hash(url)}",
            links_found=[]
        )
    
    def _get_agent_deployment_status(self) -> Dict[str, Any]:
        """Get current agent deployment status."""
        
        if not self.agents_deployed:
            return {"deployed": False}
        
        return {
            "deployed": True,
            "github_agents": len(self.agent_creator.github_agents),
            "github_squads": len(self.agent_creator.github_squads),
            "total_system_agents": len(self.agent_creator.base_agent_creator.agent_registry),
            "total_system_squads": len(self.agent_creator.base_agent_creator.squad_registry)
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        
        return {
            "initialized": self.initialized,
            "agents_deployed": self.agents_deployed,
            "statistics": self.stats,
            "github_fetcher_stats": self.github_fetcher.get_fetch_stats(),
            "amasiap_stats": self.amasiap_protocol.get_protocol_stats(),
            "agent_deployment_status": self._get_agent_deployment_status()
        }
    
    async def cleanup(self):
        """Clean up system resources."""
        
        await self.github_fetcher.cleanup()
        logger.info("GitHub Integration Orchestrator cleaned up")


# Global orchestrator instance
GITHUB_INTEGRATION_ORCHESTRATOR = GitHubIntegrationOrchestrator()


async def process_github_integration(user_input: str, 
                                   github_url: Optional[str] = None,
                                   enable_amasiap: bool = True,
                                   enable_multi_fetch: bool = True) -> IntegrationResult:
    """
    Convenience function for complete GitHub integration processing.
    
    Args:
        user_input: User input to process
        github_url: Optional GitHub URL to fetch (uses default if not provided)
        enable_amasiap: Whether to apply A.M.A.S.I.A.P. Protocol
        enable_multi_fetch: Whether to enable multi-fetch discovery
    
    Returns:
        IntegrationResult with complete processing results
    """
    
    request = IntegrationRequest(
        user_input=user_input,
        primary_github_url=github_url,
        enable_amasiap=enable_amasiap,
        enable_multi_fetch=enable_multi_fetch
    )
    
    return await GITHUB_INTEGRATION_ORCHESTRATOR.process_integration_request(request)


async def fetch_github_guideline(url: str) -> FetchResult:
    """Convenience function to fetch GitHub guideline."""
    
    return await GITHUB_INTEGRATION_ORCHESTRATOR.fetch_github_guideline_only(url)


async def enhance_input_with_amasiap(user_input: str) -> EnhancementResult:
    """Convenience function to enhance input with A.M.A.S.I.A.P. Protocol."""
    
    return await GITHUB_INTEGRATION_ORCHESTRATOR.enhance_input_only(user_input)
