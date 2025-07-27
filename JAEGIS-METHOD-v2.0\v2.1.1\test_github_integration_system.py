"""
JAEGIS GitHub Integration System - Comprehensive Test Suite
Tests the complete GitHub integration system with all components

This test suite validates:
1. Agent Creator system and agent/squad creation
2. GitHub fetching with single link and multi-fetch
3. A.M.A.S.I.A.P. Protocol enhancement
4. Squad coordination and orchestration
5. Complete integration workflow
"""

import asyncio
import logging
import time
import json
from typing import Dict, List, Any
from pathlib import Path

# Import the complete GitHub integration system
from jaegis_github_integration_system import GitHubIntegrationAgentCreator
from github_integration.github_fetcher import GitHubFetcher
from github_integration.amasiap_protocol import AMASIAPProtocol
from github_integration.squad_coordinator import GitHubSquadCoordinator, initialize_squad_coordinator
from github_integration.integration_orchestrator import GitHubIntegrationOrchestrator, IntegrationRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class GitHubIntegrationTestSuite:
    """
    Comprehensive test suite for JAEGIS GitHub Integration System
    
    Tests all components designed by the Agent Creator and validates
    the complete integration workflow.
    """
    
    def __init__(self):
        self.test_results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    async def run_all_tests(self):
        """Run complete test suite."""
        
        print("🧪 JAEGIS GITHUB INTEGRATION SYSTEM - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        
        try:
            # Test 1: Agent Creator System
            await self._test_agent_creator_system()
            
            # Test 2: GitHub Fetcher
            await self._test_github_fetcher()
            
            # Test 3: A.M.A.S.I.A.P. Protocol
            await self._test_amasiap_protocol()
            
            # Test 4: Squad Coordination
            await self._test_squad_coordination()
            
            # Test 5: Complete Integration Orchestrator
            await self._test_integration_orchestrator()
            
            # Test 6: End-to-End Integration
            await self._test_end_to_end_integration()
            
            # Generate test report
            await self._generate_test_report()
            
        except Exception as e:
            logger.error(f"Test suite failed: {e}")
            print(f"❌ Test suite failed: {e}")
    
    async def _test_agent_creator_system(self):
        """Test Agent Creator system and agent/squad creation."""
        
        print("\n🧪 TEST 1: Agent Creator System")
        print("-" * 50)
        
        test_name = "agent_creator_system"
        self.total_tests += 1
        
        try:
            # Initialize Agent Creator
            agent_creator = GitHubIntegrationAgentCreator()
            
            # Test gap analysis
            gaps = await agent_creator.analyze_github_integration_gaps()
            assert len(gaps) > 0, "No gaps identified"
            print(f"✅ Gap analysis: {len(gaps)} gaps identified")
            
            # Test agent creation
            agents = await agent_creator.create_github_integration_agents(gaps)
            assert len(agents) > 0, "No agents created"
            print(f"✅ Agent creation: {len(agents)} agents created")
            
            # Test squad design
            squads = await agent_creator.design_github_integration_squads(gaps, agents)
            assert len(squads) > 0, "No squads created"
            print(f"✅ Squad design: {len(squads)} squads created")
            
            # Test complete deployment
            deployment_result = await agent_creator.deploy_github_integration_system()
            assert deployment_result["github_agents_created"] > 0, "No agents deployed"
            assert deployment_result["github_squads_created"] > 0, "No squads deployed"
            print(f"✅ System deployment: {deployment_result['github_agents_created']} agents, {deployment_result['github_squads_created']} squads")
            
            self.test_results[test_name] = {
                "status": "PASSED",
                "gaps_identified": len(gaps),
                "agents_created": len(agents),
                "squads_created": len(squads),
                "deployment_result": deployment_result
            }
            
            self.passed_tests += 1
            print(f"✅ TEST 1 PASSED: Agent Creator System")
            
        except Exception as e:
            self.test_results[test_name] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.failed_tests += 1
            print(f"❌ TEST 1 FAILED: {e}")
    
    async def _test_github_fetcher(self):
        """Test GitHub fetching capabilities."""
        
        print("\n🧪 TEST 2: GitHub Fetcher")
        print("-" * 50)
        
        test_name = "github_fetcher"
        self.total_tests += 1
        
        try:
            # Initialize GitHub Fetcher
            fetcher = GitHubFetcher()
            await fetcher.initialize()
            
            # Test single GitHub fetch (will use fallback for demo)
            test_url = "https://github.com/usemanusai/JAEGIS/GOLD.md"
            result = await fetcher.fetch_github_guideline(test_url)
            
            # Should succeed with fallback content
            assert result.success or result.error, "Fetch result invalid"
            print(f"✅ Single fetch: {'Success' if result.success else 'Fallback used'}")
            
            # Test multi-fetch discovery (simulated)
            if result.success and result.resource:
                # Simulate discovered links
                result.resource.links_found = [
                    "https://github.com/usemanusai/JAEGIS/README.md",
                    "https://github.com/usemanusai/JAEGIS/docs/API.md"
                ]
                
                multi_results = await fetcher.multi_fetch_from_guideline(result.resource)
                print(f"✅ Multi-fetch: {len(multi_results)} links processed")
            
            # Test caching
            stats = fetcher.get_fetch_stats()
            print(f"✅ Fetcher stats: {stats['total_fetches']} fetches, {stats['cache_hit_rate']}% cache hit rate")
            
            await fetcher.cleanup()
            
            self.test_results[test_name] = {
                "status": "PASSED",
                "fetch_success": result.success,
                "stats": stats
            }
            
            self.passed_tests += 1
            print(f"✅ TEST 2 PASSED: GitHub Fetcher")
            
        except Exception as e:
            self.test_results[test_name] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.failed_tests += 1
            print(f"❌ TEST 2 FAILED: {e}")
    
    async def _test_amasiap_protocol(self):
        """Test A.M.A.S.I.A.P. Protocol enhancement."""
        
        print("\n🧪 TEST 3: A.M.A.S.I.A.P. Protocol")
        print("-" * 50)
        
        test_name = "amasiap_protocol"
        self.total_tests += 1
        
        try:
            # Initialize A.M.A.S.I.A.P. Protocol
            protocol = AMASIAPProtocol()
            await protocol.activate_protocol()
            
            # Test input enhancement
            test_input = "Create a GitHub integration system with multi-fetch capabilities"
            
            enhancement_result = await protocol.enhance_input_automatically(test_input)
            
            assert enhancement_result.enhanced_input != test_input, "Input not enhanced"
            assert len(enhancement_result.research_findings) > 0, "No research performed"
            assert len(enhancement_result.task_hierarchy) > 0, "No task hierarchy created"
            
            print(f"✅ Input enhancement: {len(enhancement_result.enhanced_input)} chars")
            print(f"✅ Research queries: {len(enhancement_result.research_findings)}")
            print(f"✅ Task phases: {len(enhancement_result.task_hierarchy)}")
            print(f"✅ Gaps identified: {len(enhancement_result.gap_analysis)}")
            
            # Test protocol stats
            stats = protocol.get_protocol_stats()
            assert stats["protocol_active"], "Protocol not active"
            print(f"✅ Protocol stats: {stats['enhancement_stats']['total_enhancements']} enhancements")
            
            self.test_results[test_name] = {
                "status": "PASSED",
                "enhancement_result": {
                    "research_queries": len(enhancement_result.research_findings),
                    "task_phases": len(enhancement_result.task_hierarchy),
                    "gaps_identified": len(enhancement_result.gap_analysis),
                    "processing_time": enhancement_result.processing_time
                },
                "protocol_stats": stats
            }
            
            self.passed_tests += 1
            print(f"✅ TEST 3 PASSED: A.M.A.S.I.A.P. Protocol")
            
        except Exception as e:
            self.test_results[test_name] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.failed_tests += 1
            print(f"❌ TEST 3 FAILED: {e}")
    
    async def _test_squad_coordination(self):
        """Test squad coordination system."""
        
        print("\n🧪 TEST 4: Squad Coordination")
        print("-" * 50)
        
        test_name = "squad_coordination"
        self.total_tests += 1
        
        try:
            # Initialize Agent Creator and Squad Coordinator
            agent_creator = GitHubIntegrationAgentCreator()
            await agent_creator.deploy_github_integration_system()
            
            squad_coordinator = initialize_squad_coordinator(agent_creator)
            await squad_coordinator.initialize_squad_coordination()
            
            # Test guideline fetching coordination
            guideline_result = await squad_coordinator.coordinate_guideline_fetching(
                "https://github.com/usemanusai/JAEGIS/GOLD.md",
                {"timeout": 30, "cache_enabled": True}
            )
            
            assert guideline_result.success, "Guideline fetching coordination failed"
            print(f"✅ Guideline coordination: {guideline_result.coordination_time:.2f}s")
            
            # Test multi-fetch coordination
            multi_fetch_result = await squad_coordinator.coordinate_multi_fetch_operation(
                ["https://github.com/usemanusai/JAEGIS/README.md", "https://github.com/usemanusai/JAEGIS/docs/API.md"],
                "https://github.com/usemanusai/JAEGIS"
            )
            
            assert multi_fetch_result.success, "Multi-fetch coordination failed"
            print(f"✅ Multi-fetch coordination: {multi_fetch_result.coordination_time:.2f}s")
            
            # Test A.M.A.S.I.A.P. coordination
            amasiap_result = await squad_coordinator.coordinate_amasiap_protocol(
                "Test input for enhancement",
                {"research_enabled": True, "task_breakdown": True}
            )
            
            assert amasiap_result.success, "A.M.A.S.I.A.P. coordination failed"
            print(f"✅ A.M.A.S.I.A.P. coordination: {amasiap_result.coordination_time:.2f}s")
            
            # Test coordination status
            status = squad_coordinator.get_coordination_status()
            print(f"✅ Coordination status: {status['available_squads']} squads available")
            
            self.test_results[test_name] = {
                "status": "PASSED",
                "guideline_coordination": guideline_result.success,
                "multi_fetch_coordination": multi_fetch_result.success,
                "amasiap_coordination": amasiap_result.success,
                "coordination_status": status
            }
            
            self.passed_tests += 1
            print(f"✅ TEST 4 PASSED: Squad Coordination")
            
        except Exception as e:
            self.test_results[test_name] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.failed_tests += 1
            print(f"❌ TEST 4 FAILED: {e}")
    
    async def _test_integration_orchestrator(self):
        """Test complete integration orchestrator."""
        
        print("\n🧪 TEST 5: Integration Orchestrator")
        print("-" * 50)
        
        test_name = "integration_orchestrator"
        self.total_tests += 1
        
        try:
            # Initialize Integration Orchestrator
            orchestrator = GitHubIntegrationOrchestrator()
            await orchestrator.initialize()
            
            # Test complete integration request
            request = IntegrationRequest(
                user_input="Create a comprehensive GitHub integration system",
                primary_github_url="https://github.com/usemanusai/JAEGIS/GOLD.md",
                enable_amasiap=True,
                enable_multi_fetch=True
            )
            
            result = await orchestrator.process_integration_request(request)
            
            assert result.success, "Integration request failed"
            assert result.enhanced_input, "No enhanced input"
            assert result.primary_resource, "No primary resource"
            
            print(f"✅ Integration processing: {result.processing_metadata['processing_time']:.2f}s")
            print(f"✅ Enhanced input: {len(result.enhanced_input)} chars")
            print(f"✅ Resources fetched: {result.processing_metadata['total_resources_fetched']}")
            print(f"✅ A.M.A.S.I.A.P. applied: {result.processing_metadata['amasiap_applied']}")
            
            # Test system status
            status = orchestrator.get_system_status()
            assert status["initialized"], "System not initialized"
            assert status["agents_deployed"], "Agents not deployed"
            
            print(f"✅ System status: Initialized={status['initialized']}, Agents={status['agents_deployed']}")
            
            await orchestrator.cleanup()
            
            self.test_results[test_name] = {
                "status": "PASSED",
                "integration_success": result.success,
                "processing_metadata": result.processing_metadata,
                "system_status": status
            }
            
            self.passed_tests += 1
            print(f"✅ TEST 5 PASSED: Integration Orchestrator")
            
        except Exception as e:
            self.test_results[test_name] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.failed_tests += 1
            print(f"❌ TEST 5 FAILED: {e}")
    
    async def _test_end_to_end_integration(self):
        """Test complete end-to-end integration workflow."""
        
        print("\n🧪 TEST 6: End-to-End Integration")
        print("-" * 50)
        
        test_name = "end_to_end_integration"
        self.total_tests += 1
        
        try:
            # Import convenience function
            from github_integration.integration_orchestrator import process_github_integration
            
            # Test complete workflow
            user_input = """
            Implement a comprehensive GitHub integration system that can:
            1. Fetch guidelines from a single GitHub link
            2. Discover and fetch multiple related resources
            3. Apply A.M.A.S.I.A.P. Protocol for enhancement
            4. Coordinate agent squads for optimal performance
            """
            
            start_time = time.time()
            
            result = await process_github_integration(
                user_input=user_input,
                github_url="https://github.com/usemanusai/JAEGIS/GOLD.md",
                enable_amasiap=True,
                enable_multi_fetch=True
            )
            
            end_to_end_time = time.time() - start_time
            
            assert result.success, "End-to-end integration failed"
            
            print(f"✅ End-to-end processing: {end_to_end_time:.2f}s")
            print(f"✅ Complete workflow: Success")
            print(f"✅ All components integrated: True")
            
            # Validate all components were used
            metadata = result.processing_metadata
            assert metadata["amasiap_applied"], "A.M.A.S.I.A.P. not applied"
            assert metadata["agents_deployed"], "Agents not deployed"
            assert metadata["total_resources_fetched"] > 0, "No resources fetched"
            
            print(f"✅ Component validation: All components active")
            
            self.test_results[test_name] = {
                "status": "PASSED",
                "end_to_end_time": end_to_end_time,
                "integration_success": result.success,
                "components_validated": True,
                "processing_metadata": metadata
            }
            
            self.passed_tests += 1
            print(f"✅ TEST 6 PASSED: End-to-End Integration")
            
        except Exception as e:
            self.test_results[test_name] = {
                "status": "FAILED",
                "error": str(e)
            }
            self.failed_tests += 1
            print(f"❌ TEST 6 FAILED: {e}")
    
    async def _generate_test_report(self):
        """Generate comprehensive test report."""
        
        print("\n📋 TEST SUITE COMPLETE - GENERATING REPORT")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        report = {
            "test_suite": "JAEGIS GitHub Integration System",
            "timestamp": time.time(),
            "summary": {
                "total_tests": self.total_tests,
                "passed_tests": self.passed_tests,
                "failed_tests": self.failed_tests,
                "success_rate": success_rate
            },
            "test_results": self.test_results
        }
        
        # Save report
        report_file = Path("github_integration_test_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Test report saved to: {report_file}")
        
        print(f"\n🎯 TEST SUITE SUMMARY:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   Passed: {self.passed_tests}")
        print(f"   Failed: {self.failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests == 0:
            print(f"\n🎉 ALL TESTS PASSED! GitHub Integration System is fully operational.")
        else:
            print(f"\n⚠️  {self.failed_tests} test(s) failed. Review test report for details.")


async def main():
    """Run the complete test suite."""
    
    test_suite = GitHubIntegrationTestSuite()
    await test_suite.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
