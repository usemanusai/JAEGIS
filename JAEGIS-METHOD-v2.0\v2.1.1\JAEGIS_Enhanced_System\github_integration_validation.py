"""
JAEGIS Enhanced System - GitHub Integration Validation
Phase 4: GitHub Repository Integration Validation

Comprehensive validation of GitHub repository integration and dynamic resource fetching compatibility.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Validation result structure"""
    test_name: str
    status: str  # "PASS", "FAIL", "WARNING"
    message: str
    details: Dict[str, Any]
    timestamp: datetime


class GitHubIntegrationValidator:
    """
    Comprehensive GitHub integration validation for JAEGIS Enhanced System
    
    Validates dynamic resource fetching, configuration accessibility,
    and integration compatibility across all system components.
    """
    
    def __init__(self, repository: str = "usemanusai/JAEGIS"):
        self.repository = repository
        self.base_url = f"https://api.github.com/repos/{repository}"
        self.raw_url = f"https://raw.githubusercontent.com/{repository}/main"
        
        # Test configurations
        self.test_configurations = {
            "core_configs": [
                "core/agent-config.txt",
                "core/enhanced-agent-config.txt", 
                "core/iuas-agent-config.txt",
                "core/garas-agent-config.txt",
                "core/chimera-agent-config.txt"
            ],
            "command_configs": [
                "commands/squad-commands.md",
                "commands/enhanced-squad-commands.md"
            ],
            "system_configs": [
                "config/openrouter-config.json",
                "config/agent-config.json",
                "config/ai-config.json"
            ]
        }
        
        # Validation results
        self.validation_results: List[ValidationResult] = []
        
        logger.info("GitHubIntegrationValidator initialized")
    
    async def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive GitHub integration validation"""
        
        print("🔍 Starting GitHub Integration Validation...")
        print("=" * 60)
        
        # Test 1: Repository accessibility
        await self._test_repository_accessibility()
        
        # Test 2: Core configuration accessibility
        await self._test_core_configurations()
        
        # Test 3: Command configuration accessibility
        await self._test_command_configurations()
        
        # Test 4: System configuration accessibility
        await self._test_system_configurations()
        
        # Test 5: Dynamic resource fetching
        await self._test_dynamic_resource_fetching()
        
        # Test 6: Configuration parsing validation
        await self._test_configuration_parsing()
        
        # Test 7: Integration compatibility
        await self._test_integration_compatibility()
        
        # Generate validation report
        return await self._generate_validation_report()
    
    async def _test_repository_accessibility(self):
        """Test basic repository accessibility"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url) as response:
                    if response.status == 200:
                        repo_data = await response.json()
                        self._add_result(
                            "Repository Accessibility",
                            "PASS",
                            f"Repository {self.repository} is accessible",
                            {
                                "status_code": response.status,
                                "repository_name": repo_data.get("name"),
                                "default_branch": repo_data.get("default_branch"),
                                "visibility": "public" if not repo_data.get("private") else "private"
                            }
                        )
                    else:
                        self._add_result(
                            "Repository Accessibility",
                            "FAIL",
                            f"Repository not accessible: HTTP {response.status}",
                            {"status_code": response.status}
                        )
        except Exception as e:
            self._add_result(
                "Repository Accessibility",
                "FAIL",
                f"Repository accessibility test failed: {e}",
                {"error": str(e)}
            )
    
    async def _test_core_configurations(self):
        """Test core agent configuration accessibility"""
        
        for config_path in self.test_configurations["core_configs"]:
            await self._test_file_accessibility(config_path, "Core Configuration")
    
    async def _test_command_configurations(self):
        """Test command configuration accessibility"""
        
        for config_path in self.test_configurations["command_configs"]:
            await self._test_file_accessibility(config_path, "Command Configuration")
    
    async def _test_system_configurations(self):
        """Test system configuration accessibility"""
        
        for config_path in self.test_configurations["system_configs"]:
            await self._test_file_accessibility(config_path, "System Configuration")
    
    async def _test_file_accessibility(self, file_path: str, category: str):
        """Test individual file accessibility"""
        
        try:
            url = f"{self.raw_url}/{file_path}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        self._add_result(
                            f"{category}: {file_path}",
                            "PASS",
                            f"File accessible and readable",
                            {
                                "status_code": response.status,
                                "content_length": len(content),
                                "url": url
                            }
                        )
                    else:
                        self._add_result(
                            f"{category}: {file_path}",
                            "FAIL",
                            f"File not accessible: HTTP {response.status}",
                            {"status_code": response.status, "url": url}
                        )
        except Exception as e:
            self._add_result(
                f"{category}: {file_path}",
                "FAIL",
                f"File accessibility test failed: {e}",
                {"error": str(e), "file_path": file_path}
            )
    
    async def _test_dynamic_resource_fetching(self):
        """Test dynamic resource fetching capabilities"""
        
        # Test fetching Chimera configuration (newly added)
        chimera_config_url = f"{self.raw_url}/core/chimera-agent-config.txt"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(chimera_config_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Validate Chimera-specific content
                        chimera_indicators = [
                            "Project Chimera v4.1",
                            "47-Agent Specialized Squad",
                            "GARAS-ALPHA",
                            "GARAS-BETA",
                            "GARAS-GAMMA",
                            "GARAS-DELTA",
                            "GARAS-EPSILON",
                            "IUAS-PRIME"
                        ]
                        
                        found_indicators = [indicator for indicator in chimera_indicators if indicator in content]
                        
                        if len(found_indicators) >= 6:
                            self._add_result(
                                "Dynamic Resource Fetching - Chimera Config",
                                "PASS",
                                "Chimera configuration successfully fetched and validated",
                                {
                                    "content_length": len(content),
                                    "indicators_found": len(found_indicators),
                                    "indicators": found_indicators
                                }
                            )
                        else:
                            self._add_result(
                                "Dynamic Resource Fetching - Chimera Config",
                                "WARNING",
                                "Chimera configuration fetched but content validation incomplete",
                                {
                                    "content_length": len(content),
                                    "indicators_found": len(found_indicators),
                                    "expected_indicators": len(chimera_indicators)
                                }
                            )
                    else:
                        self._add_result(
                            "Dynamic Resource Fetching - Chimera Config",
                            "FAIL",
                            f"Failed to fetch Chimera configuration: HTTP {response.status}",
                            {"status_code": response.status}
                        )
        except Exception as e:
            self._add_result(
                "Dynamic Resource Fetching - Chimera Config",
                "FAIL",
                f"Dynamic resource fetching test failed: {e}",
                {"error": str(e)}
            )
    
    async def _test_configuration_parsing(self):
        """Test configuration parsing and validation"""
        
        # Test JSON configuration parsing
        openrouter_config_url = f"{self.raw_url}/config/openrouter-config.json"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(openrouter_config_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Parse JSON
                        config_data = json.loads(content)
                        
                        # Validate OpenRouter configuration structure
                        required_keys = [
                            "openrouter_config",
                            "api_management",
                            "key_pools",
                            "model_selection",
                            "integration_points"
                        ]
                        
                        missing_keys = [key for key in required_keys if key not in config_data.get("openrouter_config", {})]
                        
                        if not missing_keys:
                            self._add_result(
                                "Configuration Parsing - OpenRouter JSON",
                                "PASS",
                                "OpenRouter configuration parsed and validated successfully",
                                {
                                    "config_keys": list(config_data.get("openrouter_config", {}).keys()),
                                    "total_keys": config_data.get("openrouter_config", {}).get("api_management", {}).get("total_keys", 0)
                                }
                            )
                        else:
                            self._add_result(
                                "Configuration Parsing - OpenRouter JSON",
                                "WARNING",
                                f"OpenRouter configuration missing keys: {missing_keys}",
                                {"missing_keys": missing_keys}
                            )
                    else:
                        self._add_result(
                            "Configuration Parsing - OpenRouter JSON",
                            "FAIL",
                            f"Failed to fetch OpenRouter configuration: HTTP {response.status}",
                            {"status_code": response.status}
                        )
        except json.JSONDecodeError as e:
            self._add_result(
                "Configuration Parsing - OpenRouter JSON",
                "FAIL",
                f"JSON parsing failed: {e}",
                {"error": str(e)}
            )
        except Exception as e:
            self._add_result(
                "Configuration Parsing - OpenRouter JSON",
                "FAIL",
                f"Configuration parsing test failed: {e}",
                {"error": str(e)}
            )
    
    async def _test_integration_compatibility(self):
        """Test integration compatibility with JAEGIS system"""
        
        # Test agent configuration format compatibility
        agent_config_url = f"{self.raw_url}/core/agent-config.txt"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(agent_config_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Validate JAEGIS agent configuration format
                        format_indicators = [
                            "==================== START:",
                            "==================== END:",
                            "Title:",
                            "Name:",
                            "Description:",
                            "Persona:",
                            "Tasks:",
                            "Templates:",
                            "Coordination:",
                            "Priority:"
                        ]
                        
                        found_indicators = [indicator for indicator in format_indicators if indicator in content]
                        
                        if len(found_indicators) >= 8:
                            self._add_result(
                                "Integration Compatibility - Agent Format",
                                "PASS",
                                "Agent configuration format is JAEGIS-compatible",
                                {
                                    "format_indicators_found": len(found_indicators),
                                    "total_indicators": len(format_indicators),
                                    "compatibility_score": len(found_indicators) / len(format_indicators)
                                }
                            )
                        else:
                            self._add_result(
                                "Integration Compatibility - Agent Format",
                                "WARNING",
                                "Agent configuration format may have compatibility issues",
                                {
                                    "format_indicators_found": len(found_indicators),
                                    "total_indicators": len(format_indicators)
                                }
                            )
                    else:
                        self._add_result(
                            "Integration Compatibility - Agent Format",
                            "FAIL",
                            f"Failed to fetch agent configuration: HTTP {response.status}",
                            {"status_code": response.status}
                        )
        except Exception as e:
            self._add_result(
                "Integration Compatibility - Agent Format",
                "FAIL",
                f"Integration compatibility test failed: {e}",
                {"error": str(e)}
            )
    
    def _add_result(self, test_name: str, status: str, message: str, details: Dict[str, Any]):
        """Add validation result"""
        
        result = ValidationResult(
            test_name=test_name,
            status=status,
            message=message,
            details=details,
            timestamp=datetime.now()
        )
        
        self.validation_results.append(result)
        
        # Print result
        status_icon = "✅" if status == "PASS" else "⚠️" if status == "WARNING" else "❌"
        print(f"{status_icon} {test_name}: {message}")
    
    async def _generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        
        total_tests = len(self.validation_results)
        passed_tests = len([r for r in self.validation_results if r.status == "PASS"])
        warning_tests = len([r for r in self.validation_results if r.status == "WARNING"])
        failed_tests = len([r for r in self.validation_results if r.status == "FAIL"])
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        report = {
            "validation_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "warning_tests": warning_tests,
                "failed_tests": failed_tests,
                "success_rate": round(success_rate, 2),
                "overall_status": "PASS" if failed_tests == 0 else "WARNING" if warning_tests > 0 else "FAIL"
            },
            "test_results": [asdict(result) for result in self.validation_results],
            "integration_status": {
                "github_repository_accessible": passed_tests > 0,
                "dynamic_resource_fetching_operational": any(
                    "Dynamic Resource Fetching" in r.test_name and r.status == "PASS" 
                    for r in self.validation_results
                ),
                "configuration_parsing_functional": any(
                    "Configuration Parsing" in r.test_name and r.status == "PASS"
                    for r in self.validation_results
                ),
                "jaegis_compatibility_verified": any(
                    "Integration Compatibility" in r.test_name and r.status == "PASS"
                    for r in self.validation_results
                )
            },
            "recommendations": self._generate_recommendations()
        }
        
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"⚠️ Warnings: {warning_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Overall Status: {report['validation_summary']['overall_status']}")
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on validation results"""
        
        recommendations = []
        
        failed_results = [r for r in self.validation_results if r.status == "FAIL"]
        warning_results = [r for r in self.validation_results if r.status == "WARNING"]
        
        if failed_results:
            recommendations.append("Address failed tests before proceeding with production deployment")
            
        if warning_results:
            recommendations.append("Review warning tests and consider improvements")
            
        if not failed_results and not warning_results:
            recommendations.append("All tests passed - GitHub integration is ready for production")
            
        return recommendations


# Execute validation
async def run_validation():
    """Run GitHub integration validation"""
    
    validator = GitHubIntegrationValidator()
    report = await validator.run_comprehensive_validation()
    
    return report


if __name__ == "__main__":
    asyncio.run(run_validation())
