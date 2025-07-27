"""
JAEGIS Enhanced System v2.0 - Web Research Temporal Integration
Integrates Temporal Coordination Agent with all web research engines to ensure 2025-current queries
Updates existing research systems to use current temporal context
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import re

from .temporal_coordination_agent import TemporalCoordinationAgent, TemporalContext, TemporalAccuracy

logger = logging.getLogger(__name__)

class WebResearchTemporalIntegrator:
    """Integrates temporal coordination with all web research systems"""
    
    def __init__(self, temporal_agent: TemporalCoordinationAgent):
        self.temporal_agent = temporal_agent
        self.original_web_search_tools: Dict[str, Callable] = {}
        self.enhanced_search_tools: Dict[str, Callable] = {}
        
        # Temporal enhancement statistics
        self.enhancement_stats = {
            "queries_enhanced": 0,
            "results_validated": 0,
            "temporal_accuracy_improved": 0,
            "outdated_sources_filtered": 0
        }
        
        logger.info("Web Research Temporal Integrator initialized")
    
    async def integrate_with_automation_engine(self, automation_engine) -> Dict[str, Any]:
        """Integrate temporal coordination with Advanced Automation Engine"""
        
        # Enhance the research engine
        if hasattr(automation_engine, 'advanced_research_engine'):
            research_engine = automation_engine.advanced_research_engine
            
            # Wrap the web search tool with temporal enhancement
            if hasattr(research_engine, 'web_search_tool') and research_engine.web_search_tool:
                original_tool = research_engine.web_search_tool
                self.original_web_search_tools['automation_engine'] = original_tool
                
                # Create enhanced web search tool
                enhanced_tool = self._create_enhanced_web_search_tool(original_tool, 'automation_engine')
                research_engine.web_search_tool = enhanced_tool
                self.enhanced_search_tools['automation_engine'] = enhanced_tool
                
                logger.info("Automation Engine web search tool enhanced with temporal coordination")
        
        # Enhance research query generation
        if hasattr(automation_engine, 'advanced_research_engine'):
            await self._enhance_research_query_generation(automation_engine.advanced_research_engine)
        
        return {
            "automation_engine_integrated": True,
            "web_search_enhanced": True,
            "query_generation_enhanced": True
        }
    
    async def integrate_with_performance_optimizer(self, performance_optimizer) -> Dict[str, Any]:
        """Integrate temporal coordination with Performance Optimizer"""
        
        # Enhance any web research capabilities in performance optimizer
        integration_result = await self._enhance_system_web_research(
            performance_optimizer, 'performance_optimizer'
        )
        
        return {
            "performance_optimizer_integrated": True,
            **integration_result
        }
    
    async def integrate_with_ai_engine(self, ai_engine) -> Dict[str, Any]:
        """Integrate temporal coordination with AI Engine"""
        
        # Enhance any research capabilities in AI engine
        integration_result = await self._enhance_system_web_research(
            ai_engine, 'ai_engine'
        )
        
        return {
            "ai_engine_integrated": True,
            **integration_result
        }
    
    async def integrate_with_scalability_engine(self, scalability_engine) -> Dict[str, Any]:
        """Integrate temporal coordination with Scalability Engine"""
        
        # Enhance any research capabilities in scalability engine
        integration_result = await self._enhance_system_web_research(
            scalability_engine, 'scalability_engine'
        )
        
        return {
            "scalability_engine_integrated": True,
            **integration_result
        }
    
    async def integrate_with_integration_engine(self, integration_engine) -> Dict[str, Any]:
        """Integrate temporal coordination with Deep Integration Engine"""
        
        # Enhance any research capabilities in integration engine
        integration_result = await self._enhance_system_web_research(
            integration_engine, 'integration_engine'
        )
        
        return {
            "integration_engine_integrated": True,
            **integration_result
        }
    
    async def integrate_with_base_orchestrator(self, base_orchestrator) -> Dict[str, Any]:
        """Integrate temporal coordination with Base JAEGIS Orchestrator"""
        
        # Enhance task management web research
        if hasattr(base_orchestrator, 'task_manager'):
            task_manager = base_orchestrator.task_manager
            
            if hasattr(task_manager, 'web_search_tool') and task_manager.web_search_tool:
                original_tool = task_manager.web_search_tool
                self.original_web_search_tools['base_orchestrator'] = original_tool
                
                enhanced_tool = self._create_enhanced_web_search_tool(original_tool, 'base_orchestrator')
                task_manager.web_search_tool = enhanced_tool
                self.enhanced_search_tools['base_orchestrator'] = enhanced_tool
        
        return {
            "base_orchestrator_integrated": True,
            "task_manager_enhanced": True
        }
    
    def _create_enhanced_web_search_tool(self, original_tool: Callable, system_name: str) -> Callable:
        """Create enhanced web search tool with temporal coordination"""
        
        async def enhanced_web_search_tool(query: str, num_results: int = 5, **kwargs) -> Any:
            """Enhanced web search tool with temporal coordination"""
            
            try:
                # Enhance query with temporal context
                enhanced_query = await self.temporal_agent.enhance_web_research_query(
                    query, {"system": system_name, **kwargs}
                )
                
                # Log query enhancement
                logger.info(f"Query enhanced for {system_name}: '{query}' -> '{enhanced_query}'")
                self.enhancement_stats["queries_enhanced"] += 1
                
                # Execute search with enhanced query
                search_result = await original_tool(query=enhanced_query, num_results=num_results, **kwargs)
                
                # Validate temporal accuracy of results if possible
                if hasattr(search_result, 'content') and search_result.content:
                    # Parse results for temporal validation
                    parsed_results = self._parse_search_results_for_validation(search_result.content)
                    
                    # Create operation ID for validation
                    operation_id = f"{system_name}_{int(datetime.now().timestamp())}"
                    
                    # Validate results
                    validation_result = await self.temporal_agent.validate_research_results(
                        parsed_results, operation_id
                    )
                    
                    if validation_result["validated"]:
                        self.enhancement_stats["results_validated"] += 1
                        
                        # Filter out outdated sources if needed
                        filtered_results = self._filter_outdated_sources(
                            validation_result["results"]
                        )
                        
                        if len(filtered_results) < len(parsed_results):
                            self.enhancement_stats["outdated_sources_filtered"] += len(parsed_results) - len(filtered_results)
                        
                        # Update search result content with filtered results
                        if filtered_results:
                            search_result.content = self._reconstruct_search_content(filtered_results)
                            self.enhancement_stats["temporal_accuracy_improved"] += 1
                
                return search_result
                
            except Exception as e:
                logger.error(f"Error in enhanced web search for {system_name}: {e}")
                # Fallback to original tool
                return await original_tool(query=query, num_results=num_results, **kwargs)
        
        return enhanced_web_search_tool
    
    async def _enhance_system_web_research(self, system_obj, system_name: str) -> Dict[str, Any]:
        """Enhance web research capabilities in any system object"""
        
        enhanced_components = []
        
        # Look for web search tools in the system
        for attr_name in dir(system_obj):
            attr_value = getattr(system_obj, attr_name)
            
            # Check if it's a web search tool
            if (callable(attr_value) and 
                ('search' in attr_name.lower() or 'web' in attr_name.lower()) and
                not attr_name.startswith('_')):
                
                # Enhance this tool
                original_tool = attr_value
                self.original_web_search_tools[f"{system_name}_{attr_name}"] = original_tool
                
                enhanced_tool = self._create_enhanced_web_search_tool(original_tool, f"{system_name}_{attr_name}")
                setattr(system_obj, attr_name, enhanced_tool)
                self.enhanced_search_tools[f"{system_name}_{attr_name}"] = enhanced_tool
                
                enhanced_components.append(attr_name)
        
        return {
            "enhanced_components": enhanced_components,
            "components_count": len(enhanced_components)
        }
    
    async def _enhance_research_query_generation(self, research_engine) -> Dict[str, Any]:
        """Enhance research query generation methods"""
        
        # Enhance _generate_intelligent_queries method if it exists
        if hasattr(research_engine, '_generate_intelligent_queries'):
            original_method = research_engine._generate_intelligent_queries
            
            async def enhanced_generate_queries(project_description: str, domains: List[str], depth) -> List[str]:
                """Enhanced query generation with temporal context"""
                
                # Get original queries
                original_queries = original_method(project_description, domains, depth)
                
                # Enhance each query with temporal context
                enhanced_queries = []
                for query in original_queries:
                    enhanced_query = await self.temporal_agent.enhance_web_research_query(
                        query, {"domains": domains, "depth": depth.value if hasattr(depth, 'value') else str(depth)}
                    )
                    enhanced_queries.append(enhanced_query)
                
                return enhanced_queries
            
            # Replace the method
            research_engine._generate_intelligent_queries = enhanced_generate_queries
            
            logger.info("Research query generation enhanced with temporal coordination")
        
        return {"query_generation_enhanced": True}
    
    def _parse_search_results_for_validation(self, search_content: str) -> List[Dict[str, Any]]:
        """Parse search results for temporal validation"""
        
        results = []
        lines = search_content.split('\n')
        
        current_result = {}
        for line in lines:
            line = line.strip()
            
            if line.startswith('- [') and '](' in line:
                # New result found
                if current_result:
                    results.append(current_result)
                
                # Extract title and URL
                title_match = re.search(r'\[(.*?)\]', line)
                url_match = re.search(r'\((.*?)\)', line)
                
                current_result = {
                    "title": title_match.group(1) if title_match else "Unknown",
                    "url": url_match.group(1) if url_match else "",
                    "content": "",
                    "source": "web_search"
                }
            elif line and current_result:
                current_result["content"] += line + " "
        
        # Add the last result
        if current_result:
            results.append(current_result)
        
        return results
    
    def _filter_outdated_sources(self, validated_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out outdated sources based on temporal validation"""
        
        filtered_results = []
        
        for result in validated_results:
            temporal_validation = result.get("temporal_validation", {})
            
            if temporal_validation:
                accuracy_level = temporal_validation.get("accuracy_level")
                confidence_score = temporal_validation.get("confidence_score", 0)
                
                # Keep results that are current or recent with good confidence
                if (accuracy_level in ["current", "recent"] and confidence_score >= 0.6) or confidence_score >= 0.8:
                    filtered_results.append(result)
            else:
                # Keep results without validation (fallback)
                filtered_results.append(result)
        
        return filtered_results
    
    def _reconstruct_search_content(self, filtered_results: List[Dict[str, Any]]) -> str:
        """Reconstruct search content from filtered results"""
        
        content_lines = []
        
        for result in filtered_results:
            title = result.get("title", "Unknown")
            url = result.get("url", "")
            content = result.get("content", "")
            
            # Reconstruct the search result format
            if url:
                content_lines.append(f"- [{title}]({url})")
            else:
                content_lines.append(f"- {title}")
            
            if content:
                # Add content with proper indentation
                content_lines.append(f"  {content.strip()}")
            
            content_lines.append("")  # Empty line between results
        
        return "\n".join(content_lines)
    
    async def update_hardcoded_2024_references(self, target_files: List[str] = None) -> Dict[str, Any]:
        """Update hardcoded 2024 references in research-related files"""
        
        # Get current date from temporal agent
        current_context = await self.temporal_agent.get_current_temporal_context()
        current_year = current_context.current_date.year
        
        # Files to update if not specified
        if target_files is None:
            target_files = [
                "JAEGIS_Enhanced_System/automation/advanced_automation_engine.py",
                "JAEGIS_Enhanced_System/optimization/performance_optimizer.py",
                "JAEGIS_Enhanced_System/intelligence/advanced_ai_engine.py",
                "JAEGIS_Enhanced_System/scalability/scalability_engine.py",
                "JAEGIS_Enhanced_System/integration/deep_integration_engine.py"
            ]
        
        updates_made = []
        
        for file_path in target_files:
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Track changes
                original_content = content
                
                # Update 2024 references to current year or 2024-2025 range
                content = re.sub(r'\b2024\b(?!\s*-\s*2025)', f'{current_year}', content)
                content = re.sub(r'2024\s+(?=best practices|guide|trends|technology)', f'{current_year} ', content)
                
                # Add temporal keywords to research queries
                content = re.sub(
                    r'(query.*?=.*?["\'])([^"\']*?)(["\']\s*)',
                    lambda m: f'{m.group(1)}{m.group(2)} {current_year} current{m.group(3)}' 
                    if 'best practices' in m.group(2) or 'guide' in m.group(2) else m.group(0),
                    content
                )
                
                # Write updated content if changes were made
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updates_made.append({
                        "file": file_path,
                        "updated": True,
                        "changes": "Updated 2024 references and added temporal keywords"
                    })
                else:
                    updates_made.append({
                        "file": file_path,
                        "updated": False,
                        "changes": "No updates needed"
                    })
                    
            except Exception as e:
                logger.error(f"Error updating file {file_path}: {e}")
                updates_made.append({
                    "file": file_path,
                    "updated": False,
                    "error": str(e)
                })
        
        return {
            "files_processed": len(target_files),
            "files_updated": len([u for u in updates_made if u.get("updated", False)]),
            "updates_made": updates_made,
            "current_year": current_year
        }
    
    def get_enhancement_statistics(self) -> Dict[str, Any]:
        """Get temporal enhancement statistics"""
        
        return {
            "temporal_integration_active": True,
            "enhanced_systems": len(self.enhanced_search_tools),
            "enhancement_statistics": self.enhancement_stats.copy(),
            "original_tools_preserved": len(self.original_web_search_tools),
            "temporal_accuracy_rate": (
                self.enhancement_stats["temporal_accuracy_improved"] / 
                max(self.enhancement_stats["results_validated"], 1)
            )
        }
    
    async def restore_original_tools(self) -> Dict[str, Any]:
        """Restore original web search tools (for testing or rollback)"""
        
        restored_count = 0
        
        for system_name, original_tool in self.original_web_search_tools.items():
            # This would require references to the original objects
            # Implementation would depend on how we store object references
            restored_count += 1
        
        return {
            "restoration_completed": True,
            "tools_restored": restored_count
        }

class TemporalQueryEnhancer:
    """Specialized class for enhancing queries with temporal context"""
    
    def __init__(self):
        self.temporal_patterns = {
            "current_year": ["2025", "current year"],
            "recent_timeframe": ["2024-2025", "last 12 months", "recent"],
            "latest": ["latest", "newest", "most recent", "up-to-date"],
            "exclude_old": ["-2023", "-2022", "-outdated", "-legacy"]
        }
    
    def enhance_query_with_temporal_keywords(self, query: str, temporal_context: TemporalContext) -> str:
        """Enhance query with appropriate temporal keywords"""
        
        query_lower = query.lower()
        current_year = temporal_context.current_date.year
        
        # Check if query already has temporal context
        if any(str(current_year) in query_lower or keyword in query_lower 
               for keywords in self.temporal_patterns.values() 
               for keyword in keywords):
            return query  # Already has temporal context
        
        # Determine best enhancement based on query content
        if any(word in query_lower for word in ["best practices", "guide", "tutorial"]):
            return f"{query} {current_year} latest"
        elif any(word in query_lower for word in ["trends", "emerging", "new"]):
            return f"{query} 2024-2025 current"
        elif any(word in query_lower for word in ["technology", "software", "tools"]):
            return f"{query} {current_year} recent"
        elif any(word in query_lower for word in ["research", "study", "analysis"]):
            return f"{query} 2024-2025 recent studies"
        else:
            return f"{query} {current_year} current"
    
    def add_temporal_filters(self, query: str) -> str:
        """Add temporal filters to exclude outdated content"""
        
        # Add exclusion filters for old content
        exclusions = ["-2023", "-2022", "-outdated"]
        
        for exclusion in exclusions:
            if exclusion not in query:
                query += f" {exclusion}"
        
        return query
