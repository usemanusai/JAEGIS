"""
JAEGIS Brain Protocol Suite v1.0 - Proactive Next-Step & Dependency Analysis Protocol
Mandate 2.2: Strategic horizon scanning and automatic next action proposals

This module implements the mandatory proactive analysis protocol that automatically
performs strategic horizon scanning after task completion and proposes logical
next steps based on dependency analysis.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class DependencyType(str, Enum):
    """Types of dependencies detected."""
    TECHNICAL = "technical"
    FUNCTIONAL = "functional"
    SEQUENTIAL = "sequential"
    RESOURCE = "resource"
    INTEGRATION = "integration"
    VALIDATION = "validation"


class ActionPriority(str, Enum):
    """Priority levels for next actions."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    OPTIONAL = "optional"


class ImpactLevel(str, Enum):
    """Impact levels for changes."""
    SYSTEM_WIDE = "system_wide"
    MODULE_LEVEL = "module_level"
    COMPONENT_LEVEL = "component_level"
    LOCAL = "local"


@dataclass
class Dependency:
    """Dependency relationship."""
    dependency_id: str
    dependency_type: DependencyType
    source_component: str
    target_component: str
    description: str
    criticality: str
    resolution_required: bool
    estimated_effort: str


@dataclass
class NextAction:
    """Proposed next action."""
    action_id: str
    title: str
    description: str
    priority: ActionPriority
    estimated_duration: str
    dependencies: List[str]
    rationale: str
    impact_assessment: str
    suggested_assignee: str
    deadline_suggestion: Optional[str]


@dataclass
class HorizonScan:
    """Strategic horizon scan result."""
    scan_id: str
    trigger_task: str
    scan_timestamp: float
    changes_analyzed: List[str]
    dependencies_identified: List[Dependency]
    impacts_detected: List[str]
    next_actions_proposed: List[NextAction]
    scan_duration_ms: float
    confidence_score: float


class ProactiveAnalysisEngine:
    """
    JAEGIS Brain Protocol Suite Proactive Analysis Engine
    
    Implements Mandate 2.2: Proactive Next-Step & Dependency Analysis Protocol
    
    Mandatory execution sequence:
    1. Force Horizon Scan - Automatically perform after task completion
    2. Dependency Analysis - Analyze changes and identify downstream impacts
    3. Propose Next Actions - Generate logical next steps based on analysis
    """
    
    def __init__(self):
        self.scan_history: List[HorizonScan] = []
        self.dependency_graph: Dict[str, List[Dependency]] = {}
        self.action_queue: List[NextAction] = []
        
        # Analysis patterns for different types of changes
        self.analysis_patterns = {
            "code_changes": {
                "file_extensions": [".py", ".js", ".ts", ".java", ".cpp"],
                "impact_areas": ["testing", "documentation", "integration", "deployment"],
                "dependency_types": [DependencyType.TECHNICAL, DependencyType.FUNCTIONAL]
            },
            "documentation_changes": {
                "file_extensions": [".md", ".rst", ".txt"],
                "impact_areas": ["review", "validation", "publication"],
                "dependency_types": [DependencyType.VALIDATION, DependencyType.SEQUENTIAL]
            },
            "configuration_changes": {
                "file_extensions": [".json", ".yaml", ".yml", ".toml", ".ini"],
                "impact_areas": ["testing", "deployment", "validation", "backup"],
                "dependency_types": [DependencyType.INTEGRATION, DependencyType.RESOURCE]
            },
            "architecture_changes": {
                "keywords": ["architecture", "design", "structure", "framework"],
                "impact_areas": ["documentation", "implementation", "testing", "migration"],
                "dependency_types": [DependencyType.SYSTEM_WIDE, DependencyType.INTEGRATION]
            }
        }
        
        logger.info("Proactive Analysis Engine initialized")
    
    async def force_horizon_scan(self, completed_task: str, changes_made: List[str]) -> HorizonScan:
        """
        MANDATORY: Perform strategic horizon scan after task completion
        
        This method MUST automatically perform a "Strategic Horizon Scan"
        after successfully completing any task that modifies code or documentation.
        """
        
        scan_start = time.time()
        scan_id = f"scan_{int(time.time())}_{hash(completed_task) % 10000}"
        
        logger.info(f"🔭 FORCE HORIZON SCAN - Scan ID: {scan_id}")
        logger.info(f"📝 Completed Task: {completed_task[:100]}...")
        logger.info(f"📊 Changes Made: {len(changes_made)}")
        
        # Step 1: Analyze changes made
        change_analysis = await self._analyze_changes(changes_made)
        
        # Step 2: Identify new dependencies
        dependencies = await self._identify_dependencies(changes_made, change_analysis)
        
        # Step 3: Detect downstream impacts
        impacts = await self._detect_downstream_impacts(changes_made, dependencies)
        
        # Step 4: Propose next actions
        next_actions = await self._propose_next_actions(completed_task, changes_made, dependencies, impacts)
        
        # Step 5: Calculate confidence score
        confidence_score = await self._calculate_scan_confidence(dependencies, impacts, next_actions)
        
        scan_duration = (time.time() - scan_start) * 1000
        
        # Create horizon scan result
        horizon_scan = HorizonScan(
            scan_id=scan_id,
            trigger_task=completed_task,
            scan_timestamp=time.time(),
            changes_analyzed=changes_made,
            dependencies_identified=dependencies,
            impacts_detected=impacts,
            next_actions_proposed=next_actions,
            scan_duration_ms=scan_duration,
            confidence_score=confidence_score
        )
        
        # Store scan result
        self.scan_history.append(horizon_scan)
        
        # Update dependency graph
        await self._update_dependency_graph(dependencies)
        
        # Add actions to queue
        self.action_queue.extend(next_actions)
        
        logger.info(f"🔭 Horizon scan complete:")
        logger.info(f"  Dependencies identified: {len(dependencies)}")
        logger.info(f"  Impacts detected: {len(impacts)}")
        logger.info(f"  Next actions proposed: {len(next_actions)}")
        logger.info(f"  Confidence score: {confidence_score:.1%}")
        logger.info(f"  Scan duration: {scan_duration:.1f}ms")
        
        return horizon_scan
    
    async def _analyze_changes(self, changes_made: List[str]) -> Dict[str, Any]:
        """Analyze the types and scope of changes made."""
        
        analysis = {
            "change_types": [],
            "affected_areas": [],
            "complexity_score": 0.0,
            "risk_level": "low"
        }
        
        for change in changes_made:
            change_lower = change.lower()
            
            # Identify change types
            if any(ext in change for ext in self.analysis_patterns["code_changes"]["file_extensions"]):
                analysis["change_types"].append("code")
                analysis["complexity_score"] += 2.0
            
            if any(ext in change for ext in self.analysis_patterns["documentation_changes"]["file_extensions"]):
                analysis["change_types"].append("documentation")
                analysis["complexity_score"] += 1.0
            
            if any(ext in change for ext in self.analysis_patterns["configuration_changes"]["file_extensions"]):
                analysis["change_types"].append("configuration")
                analysis["complexity_score"] += 1.5
            
            # Check for architecture changes
            if any(keyword in change_lower for keyword in self.analysis_patterns["architecture_changes"]["keywords"]):
                analysis["change_types"].append("architecture")
                analysis["complexity_score"] += 3.0
        
        # Determine risk level
        if analysis["complexity_score"] > 5.0:
            analysis["risk_level"] = "high"
        elif analysis["complexity_score"] > 3.0:
            analysis["risk_level"] = "medium"
        
        # Remove duplicates
        analysis["change_types"] = list(set(analysis["change_types"]))
        
        return analysis
    
    async def _identify_dependencies(self, changes_made: List[str], change_analysis: Dict[str, Any]) -> List[Dependency]:
        """Identify new dependencies created by the changes."""
        
        dependencies = []
        
        for change_type in change_analysis["change_types"]:
            if change_type in self.analysis_patterns:
                pattern = self.analysis_patterns[change_type]
                
                for impact_area in pattern["impact_areas"]:
                    dependency_id = f"dep_{int(time.time())}_{len(dependencies)}"
                    
                    dependency = Dependency(
                        dependency_id=dependency_id,
                        dependency_type=pattern["dependency_types"][0],  # Use first type
                        source_component=f"changes_in_{change_type}",
                        target_component=impact_area,
                        description=f"{change_type.title()} changes require {impact_area}",
                        criticality="medium" if change_analysis["risk_level"] == "high" else "low",
                        resolution_required=True,
                        estimated_effort=self._estimate_dependency_effort(impact_area, change_analysis["complexity_score"])
                    )
                    
                    dependencies.append(dependency)
        
        return dependencies
    
    def _estimate_dependency_effort(self, impact_area: str, complexity_score: float) -> str:
        """Estimate effort required to resolve dependency."""
        
        base_efforts = {
            "testing": 2.0,
            "documentation": 1.5,
            "integration": 3.0,
            "deployment": 2.5,
            "validation": 1.0,
            "review": 0.5,
            "backup": 0.5,
            "migration": 4.0
        }
        
        base_effort = base_efforts.get(impact_area, 2.0)
        adjusted_effort = base_effort * (1 + complexity_score / 10.0)
        
        if adjusted_effort < 1.0:
            return "< 1 hour"
        elif adjusted_effort < 4.0:
            return f"{adjusted_effort:.1f} hours"
        elif adjusted_effort < 8.0:
            return f"{adjusted_effort / 8:.1f} days"
        else:
            return f"{adjusted_effort / 40:.1f} weeks"
    
    async def _detect_downstream_impacts(self, changes_made: List[str], dependencies: List[Dependency]) -> List[str]:
        """Detect downstream impacts of the changes."""
        
        impacts = []
        
        # Direct impacts from dependencies
        for dependency in dependencies:
            impacts.append(f"Impact on {dependency.target_component} due to {dependency.source_component}")
        
        # System-wide impacts
        if len(changes_made) > 5:
            impacts.append("Multiple file changes may require comprehensive testing")
        
        # Integration impacts
        if any("api" in change.lower() for change in changes_made):
            impacts.append("API changes may affect client integrations")
        
        # Security impacts
        if any("security" in change.lower() or "auth" in change.lower() for change in changes_made):
            impacts.append("Security changes require security review and testing")
        
        # Performance impacts
        if any("performance" in change.lower() or "optimization" in change.lower() for change in changes_made):
            impacts.append("Performance changes require benchmarking and validation")
        
        return impacts
    
    async def _propose_next_actions(self, completed_task: str, changes_made: List[str], 
                                  dependencies: List[Dependency], impacts: List[str]) -> List[NextAction]:
        """Propose logical next actions based on analysis."""
        
        next_actions = []
        
        # Actions based on dependencies
        for dependency in dependencies:
            action_id = f"action_{int(time.time())}_{len(next_actions)}"
            
            priority = ActionPriority.HIGH if dependency.criticality == "high" else ActionPriority.MEDIUM
            
            action = NextAction(
                action_id=action_id,
                title=f"Address {dependency.target_component} dependency",
                description=f"Resolve dependency: {dependency.description}",
                priority=priority,
                estimated_duration=dependency.estimated_effort,
                dependencies=[dependency.dependency_id],
                rationale=f"Required due to changes in {dependency.source_component}",
                impact_assessment=f"Addresses {dependency.target_component} requirements",
                suggested_assignee="JAEGIS Agent",
                deadline_suggestion=self._suggest_deadline(dependency.estimated_effort, priority)
            )
            
            next_actions.append(action)
        
        # Standard follow-up actions
        standard_actions = [
            {
                "title": "Update documentation",
                "description": "Update relevant documentation to reflect changes",
                "priority": ActionPriority.MEDIUM,
                "duration": "1-2 hours"
            },
            {
                "title": "Run comprehensive tests",
                "description": "Execute test suite to validate changes",
                "priority": ActionPriority.HIGH,
                "duration": "30 minutes"
            },
            {
                "title": "Review security implications",
                "description": "Assess security impact of changes",
                "priority": ActionPriority.MEDIUM,
                "duration": "1 hour"
            }
        ]
        
        for std_action in standard_actions:
            if len(next_actions) < 10:  # Limit total actions
                action_id = f"action_{int(time.time())}_{len(next_actions)}"
                
                action = NextAction(
                    action_id=action_id,
                    title=std_action["title"],
                    description=std_action["description"],
                    priority=ActionPriority(std_action["priority"]),
                    estimated_duration=std_action["duration"],
                    dependencies=[],
                    rationale="Standard follow-up action",
                    impact_assessment="Maintains system quality and reliability",
                    suggested_assignee="JAEGIS Agent",
                    deadline_suggestion=self._suggest_deadline(std_action["duration"], ActionPriority(std_action["priority"]))
                )
                
                next_actions.append(action)
        
        return next_actions
    
    def _suggest_deadline(self, estimated_duration: str, priority: ActionPriority) -> str:
        """Suggest deadline based on duration and priority."""
        
        priority_multipliers = {
            ActionPriority.CRITICAL: 0.5,
            ActionPriority.HIGH: 1.0,
            ActionPriority.MEDIUM: 2.0,
            ActionPriority.LOW: 5.0,
            ActionPriority.OPTIONAL: 10.0
        }
        
        # Parse duration (simplified)
        if "hour" in estimated_duration:
            base_hours = 2.0
        elif "day" in estimated_duration:
            base_hours = 16.0
        elif "week" in estimated_duration:
            base_hours = 80.0
        else:
            base_hours = 4.0
        
        deadline_hours = base_hours * priority_multipliers[priority]
        
        if deadline_hours < 24:
            return f"Within {deadline_hours:.0f} hours"
        elif deadline_hours < 168:  # 1 week
            return f"Within {deadline_hours / 24:.0f} days"
        else:
            return f"Within {deadline_hours / 168:.0f} weeks"
    
    async def _calculate_scan_confidence(self, dependencies: List[Dependency], 
                                       impacts: List[str], next_actions: List[NextAction]) -> float:
        """Calculate confidence score for the scan."""
        
        confidence = 0.7  # Base confidence
        
        # Increase confidence based on analysis depth
        if len(dependencies) > 0:
            confidence += 0.1
        
        if len(impacts) > 0:
            confidence += 0.1
        
        if len(next_actions) > 0:
            confidence += 0.1
        
        # Decrease confidence for high complexity
        if len(dependencies) > 10:
            confidence -= 0.1
        
        return min(1.0, max(0.0, confidence))
    
    async def _update_dependency_graph(self, dependencies: List[Dependency]):
        """Update the global dependency graph."""
        
        for dependency in dependencies:
            source = dependency.source_component
            if source not in self.dependency_graph:
                self.dependency_graph[source] = []
            
            self.dependency_graph[source].append(dependency)
    
    def get_proposed_actions(self, priority_filter: Optional[ActionPriority] = None) -> List[NextAction]:
        """Get proposed next actions, optionally filtered by priority."""
        
        if priority_filter:
            return [action for action in self.action_queue if action.priority == priority_filter]
        
        return self.action_queue.copy()
    
    def get_analysis_status(self) -> Dict[str, Any]:
        """Get comprehensive analysis engine status."""
        
        recent_scans = len([s for s in self.scan_history if time.time() - s.scan_timestamp < 3600])
        
        priority_counts = {}
        for action in self.action_queue:
            priority = action.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        return {
            "total_scans": len(self.scan_history),
            "recent_scans_1h": recent_scans,
            "dependency_graph_size": len(self.dependency_graph),
            "pending_actions": len(self.action_queue),
            "actions_by_priority": priority_counts,
            "average_scan_duration_ms": sum(s.scan_duration_ms for s in self.scan_history) / len(self.scan_history) if self.scan_history else 0,
            "average_confidence": sum(s.confidence_score for s in self.scan_history) / len(self.scan_history) if self.scan_history else 0
        }


# Global proactive analysis engine
PROACTIVE_ANALYSIS_ENGINE = ProactiveAnalysisEngine()


async def mandatory_horizon_scan(completed_task: str, changes_made: List[str]) -> HorizonScan:
    """
    MANDATORY: Perform strategic horizon scan after task completion
    
    This function MUST be called after successfully completing any task that
    modifies code or documentation according to JAEGIS Brain Protocol Suite Mandate 2.2.
    """
    
    return await PROACTIVE_ANALYSIS_ENGINE.force_horizon_scan(completed_task, changes_made)


def get_next_action_proposals(priority_filter: Optional[ActionPriority] = None) -> List[NextAction]:
    """
    Get proposed next actions from the analysis engine
    
    This provides the logical next steps identified by the proactive analysis
    system for continued project progress.
    """
    
    return PROACTIVE_ANALYSIS_ENGINE.get_proposed_actions(priority_filter)


# Example usage
async def main():
    """Example usage of Proactive Analysis Engine."""
    
    print("🔭 JAEGIS BRAIN PROTOCOL SUITE - PROACTIVE ANALYSIS TEST")
    
    # Test horizon scan
    completed_task = "Implement JAEGIS Brain Protocol Suite authentication system"
    changes_made = [
        "core/brain_protocol/authentication.py",
        "core/brain_protocol/security.py",
        "docs/security.md",
        "tests/test_authentication.py"
    ]
    
    scan = await PROACTIVE_ANALYSIS_ENGINE.force_horizon_scan(completed_task, changes_made)
    
    print(f"\n🔭 Horizon Scan Results:")
    print(f"  Scan ID: {scan.scan_id}")
    print(f"  Dependencies: {len(scan.dependencies_identified)}")
    print(f"  Impacts: {len(scan.impacts_detected)}")
    print(f"  Next Actions: {len(scan.next_actions_proposed)}")
    print(f"  Confidence: {scan.confidence_score:.1%}")
    
    # Show proposed actions
    actions = PROACTIVE_ANALYSIS_ENGINE.get_proposed_actions(ActionPriority.HIGH)
    print(f"\n📋 High Priority Actions: {len(actions)}")
    for action in actions[:3]:
        print(f"  - {action.title}: {action.estimated_duration}")
    
    # Get status
    status = PROACTIVE_ANALYSIS_ENGINE.get_analysis_status()
    print(f"\n📊 Analysis Engine Status:")
    print(f"  Total Scans: {status['total_scans']}")
    print(f"  Pending Actions: {status['pending_actions']}")
    print(f"  Average Confidence: {status['average_confidence']:.1%}")


if __name__ == "__main__":
    asyncio.run(main())
