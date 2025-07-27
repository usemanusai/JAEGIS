"""
JAEGIS Brain Protocol Suite v1.0 - Persistent Project Memex Protocol
Mandate 2.1: Persistent knowledge base with decision rationale tracking

This module implements the mandatory project memex protocol that maintains
persistent, structured knowledge base logging all key decisions, alternatives
considered, and rationale for strategic continuity.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)


class DecisionType(str, Enum):
    """Types of decisions tracked in the memex."""
    ARCHITECTURAL = "architectural"
    TECHNICAL = "technical"
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    SECURITY = "security"
    PERFORMANCE = "performance"


class DecisionStatus(str, Enum):
    """Status of decisions in the memex."""
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class MemexEntryType(str, Enum):
    """Types of memex entries."""
    DECISION = "decision"
    PRECEDENT = "precedent"
    LESSON_LEARNED = "lesson_learned"
    CONTEXT = "context"
    RATIONALE = "rationale"
    ALTERNATIVE = "alternative"


@dataclass
class Alternative:
    """Alternative option considered for a decision."""
    alternative_id: str
    description: str
    pros: List[str]
    cons: List[str]
    estimated_effort: str
    risk_level: str
    rejection_reason: str


@dataclass
class DecisionRecord:
    """Complete decision record for the memex."""
    decision_id: str
    decision_type: DecisionType
    title: str
    description: str
    context: str
    problem_statement: str
    chosen_solution: str
    alternatives_considered: List[Alternative]
    rationale: str
    decision_maker: str
    stakeholders: List[str]
    impact_assessment: str
    implementation_notes: str
    status: DecisionStatus
    created_at: float
    updated_at: float
    tags: List[str]
    related_decisions: List[str]


@dataclass
class MemexQuery:
    """Query for searching the memex."""
    query_id: str
    query_text: str
    query_type: str
    filters: Dict[str, Any]
    timestamp: float


@dataclass
class MemexSearchResult:
    """Search result from memex query."""
    result_id: str
    query_id: str
    matching_entries: List[str]
    relevance_scores: Dict[str, float]
    total_matches: int
    search_duration_ms: float
    timestamp: float


@dataclass
class ProjectContext:
    """Current project context for decision making."""
    context_id: str
    project_phase: str
    current_objectives: List[str]
    active_constraints: List[str]
    key_stakeholders: List[str]
    recent_decisions: List[str]
    pending_decisions: List[str]
    last_updated: float


class PersistentProjectMemex:
    """
    JAEGIS Brain Protocol Suite Persistent Project Memex
    
    Implements Mandate 2.1: Persistent Project Memex Protocol
    
    Mandatory execution sequence:
    1. Establish Memex - Maintain persistent, structured knowledge base
    2. Log All Key Decisions - Record decisions, alternatives, and rationale
    3. Mandatory Consultation - Query memex for relevant precedents
    """
    
    def __init__(self):
        self.memex_path = Path("core/brain_protocol/project_memex.json")
        self.decisions: Dict[str, DecisionRecord] = {}
        self.project_context: Optional[ProjectContext] = None
        self.query_history: List[MemexQuery] = []
        self.search_results: List[MemexSearchResult] = []
        
        # Initialize memex
        self._initialize_memex()
        
        logger.info("Persistent Project Memex initialized")
    
    def _initialize_memex(self):
        """Initialize the persistent project memex."""
        
        # Create memex directory
        self.memex_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing memex or create new
        if self.memex_path.exists():
            self._load_memex()
        else:
            self._create_initial_memex()
        
        # Initialize project context
        self._initialize_project_context()
    
    def _create_initial_memex(self):
        """Create initial memex structure."""
        
        initial_memex = {
            "version": "1.0",
            "created": time.time(),
            "last_updated": time.time(),
            "decisions": {},
            "project_context": None,
            "metadata": {
                "total_decisions": 0,
                "decision_types": {},
                "last_consultation": 0.0
            }
        }
        
        with open(self.memex_path, 'w') as f:
            json.dump(initial_memex, f, indent=2)
        
        logger.info("Created initial project memex")
    
    def _load_memex(self):
        """Load existing memex from storage."""
        
        try:
            with open(self.memex_path, 'r') as f:
                memex_data = json.load(f)
            
            # Load decisions
            for decision_id, decision_data in memex_data.get("decisions", {}).items():
                # Convert alternatives
                alternatives = []
                for alt_data in decision_data.get("alternatives_considered", []):
                    alternatives.append(Alternative(**alt_data))
                
                # Create decision record
                decision_data["alternatives_considered"] = alternatives
                decision_data["decision_type"] = DecisionType(decision_data["decision_type"])
                decision_data["status"] = DecisionStatus(decision_data["status"])
                
                self.decisions[decision_id] = DecisionRecord(**decision_data)
            
            # Load project context
            context_data = memex_data.get("project_context")
            if context_data:
                self.project_context = ProjectContext(**context_data)
            
            logger.info(f"Loaded memex with {len(self.decisions)} decisions")
            
        except Exception as e:
            logger.error(f"Failed to load memex: {e}")
            self._create_initial_memex()
    
    def _initialize_project_context(self):
        """Initialize current project context."""
        
        if not self.project_context:
            self.project_context = ProjectContext(
                context_id=f"context_{int(time.time())}",
                project_phase="implementation",
                current_objectives=[
                    "Implement JAEGIS Brain Protocol Suite v1.0",
                    "Deploy 128-agent system architecture",
                    "Achieve production readiness"
                ],
                active_constraints=[
                    "Performance targets: <500ms response time",
                    "Confidence threshold: ≥85%",
                    "Security compliance requirements"
                ],
                key_stakeholders=["JAEGIS Orchestrator", "User", "Development Team"],
                recent_decisions=[],
                pending_decisions=[],
                last_updated=time.time()
            )
    
    async def mandatory_decision_logging(self, decision_title: str, chosen_solution: str,
                                       alternatives: List[Dict[str, Any]], rationale: str,
                                       decision_type: DecisionType = DecisionType.TECHNICAL) -> str:
        """
        MANDATORY: Log key decision with alternatives and rationale
        
        This method MUST be called at the conclusion of any significant task
        to record key decisions, alternatives considered, and rationale.
        """
        
        decision_id = f"decision_{int(time.time())}_{hash(decision_title) % 10000}"
        
        logger.info(f"📝 MANDATORY DECISION LOGGING - Decision ID: {decision_id}")
        logger.info(f"🎯 Decision: {decision_title}")
        
        # Convert alternatives to Alternative objects
        alternative_objects = []
        for i, alt in enumerate(alternatives):
            alt_id = f"{decision_id}_alt_{i+1}"
            alternative_objects.append(Alternative(
                alternative_id=alt_id,
                description=alt.get("description", ""),
                pros=alt.get("pros", []),
                cons=alt.get("cons", []),
                estimated_effort=alt.get("estimated_effort", "unknown"),
                risk_level=alt.get("risk_level", "medium"),
                rejection_reason=alt.get("rejection_reason", "")
            ))
        
        # Create decision record
        decision_record = DecisionRecord(
            decision_id=decision_id,
            decision_type=decision_type,
            title=decision_title,
            description=f"Decision regarding: {decision_title}",
            context=self._get_current_context_summary(),
            problem_statement=f"Need to decide on: {decision_title}",
            chosen_solution=chosen_solution,
            alternatives_considered=alternative_objects,
            rationale=rationale,
            decision_maker="JAEGIS Brain Protocol Suite",
            stakeholders=self.project_context.key_stakeholders if self.project_context else [],
            impact_assessment=await self._assess_decision_impact(chosen_solution, alternatives),
            implementation_notes="",
            status=DecisionStatus.APPROVED,
            created_at=time.time(),
            updated_at=time.time(),
            tags=await self._generate_decision_tags(decision_title, chosen_solution),
            related_decisions=await self._find_related_decisions(decision_title)
        )
        
        # Store decision
        self.decisions[decision_id] = decision_record
        
        # Update project context
        if self.project_context:
            self.project_context.recent_decisions.append(decision_id)
            # Keep only last 10 recent decisions
            if len(self.project_context.recent_decisions) > 10:
                self.project_context.recent_decisions = self.project_context.recent_decisions[-10:]
            self.project_context.last_updated = time.time()
        
        # Save memex
        await self._save_memex()
        
        logger.info(f"✅ Decision logged: {decision_title}")
        logger.info(f"📊 Alternatives considered: {len(alternative_objects)}")
        logger.info(f"🎯 Chosen solution: {chosen_solution[:100]}...")
        
        return decision_id
    
    async def mandatory_precedent_consultation(self, task_description: str) -> List[DecisionRecord]:
        """
        MANDATORY: Query memex for relevant precedents
        
        This method MUST be called before beginning any new task to ensure
        the proposed action is logically consistent with project history.
        """
        
        query_id = f"query_{int(time.time())}_{hash(task_description) % 10000}"
        
        logger.info(f"🔍 MANDATORY PRECEDENT CONSULTATION - Query ID: {query_id}")
        logger.info(f"📝 Task: {task_description[:100]}...")
        
        # Create query record
        query = MemexQuery(
            query_id=query_id,
            query_text=task_description,
            query_type="precedent_search",
            filters={},
            timestamp=time.time()
        )
        
        self.query_history.append(query)
        
        # Search for relevant precedents
        relevant_decisions = await self._search_relevant_decisions(task_description)
        
        # Create search result
        search_result = MemexSearchResult(
            result_id=f"result_{query_id}",
            query_id=query_id,
            matching_entries=[d.decision_id for d in relevant_decisions],
            relevance_scores={d.decision_id: 0.8 for d in relevant_decisions},  # Simplified scoring
            total_matches=len(relevant_decisions),
            search_duration_ms=50.0,  # Simulated
            timestamp=time.time()
        )
        
        self.search_results.append(search_result)
        
        logger.info(f"🔍 Precedent consultation complete:")
        logger.info(f"  Relevant precedents found: {len(relevant_decisions)}")
        
        if relevant_decisions:
            logger.info("📚 Relevant precedents:")
            for decision in relevant_decisions[:3]:  # Show top 3
                logger.info(f"  - {decision.title}: {decision.chosen_solution[:50]}...")
        
        return relevant_decisions
    
    async def _search_relevant_decisions(self, task_description: str) -> List[DecisionRecord]:
        """Search for decisions relevant to the task."""
        
        relevant_decisions = []
        task_lower = task_description.lower()
        
        # Simple keyword-based relevance (in production, would use semantic search)
        for decision in self.decisions.values():
            relevance_score = 0.0
            
            # Check title relevance
            if any(word in decision.title.lower() for word in task_lower.split()):
                relevance_score += 0.3
            
            # Check description relevance
            if any(word in decision.description.lower() for word in task_lower.split()):
                relevance_score += 0.2
            
            # Check solution relevance
            if any(word in decision.chosen_solution.lower() for word in task_lower.split()):
                relevance_score += 0.3
            
            # Check tags relevance
            for tag in decision.tags:
                if tag.lower() in task_lower:
                    relevance_score += 0.2
            
            # Include if relevance score is above threshold
            if relevance_score > 0.3:
                relevant_decisions.append(decision)
        
        # Sort by relevance (simplified - would use actual scores in production)
        return relevant_decisions[:5]  # Return top 5
    
    def _get_current_context_summary(self) -> str:
        """Get summary of current project context."""
        
        if not self.project_context:
            return "No project context available"
        
        return f"Phase: {self.project_context.project_phase}, " \
               f"Objectives: {len(self.project_context.current_objectives)}, " \
               f"Constraints: {len(self.project_context.active_constraints)}"
    
    async def _assess_decision_impact(self, chosen_solution: str, alternatives: List[Dict[str, Any]]) -> str:
        """Assess the impact of the chosen decision."""
        
        impact_factors = []
        
        # Assess based on solution content
        solution_lower = chosen_solution.lower()
        
        if any(word in solution_lower for word in ["architecture", "system", "framework"]):
            impact_factors.append("High architectural impact")
        
        if any(word in solution_lower for word in ["security", "authentication", "encryption"]):
            impact_factors.append("Security implications")
        
        if any(word in solution_lower for word in ["performance", "optimization", "speed"]):
            impact_factors.append("Performance impact")
        
        if any(word in solution_lower for word in ["api", "interface", "integration"]):
            impact_factors.append("Integration impact")
        
        # Assess based on number of alternatives
        if len(alternatives) > 3:
            impact_factors.append("Multiple alternatives considered - well-analyzed decision")
        elif len(alternatives) == 0:
            impact_factors.append("No alternatives documented - may need review")
        
        return "; ".join(impact_factors) if impact_factors else "Standard implementation impact"
    
    async def _generate_decision_tags(self, title: str, solution: str) -> List[str]:
        """Generate tags for the decision."""
        
        tags = []
        combined_text = f"{title} {solution}".lower()
        
        # Technology tags
        tech_keywords = {
            "python": "python",
            "api": "api",
            "database": "database",
            "security": "security",
            "performance": "performance",
            "architecture": "architecture",
            "integration": "integration",
            "testing": "testing",
            "documentation": "documentation",
            "deployment": "deployment"
        }
        
        for keyword, tag in tech_keywords.items():
            if keyword in combined_text:
                tags.append(tag)
        
        # Decision type tags
        if "implement" in combined_text:
            tags.append("implementation")
        if "design" in combined_text:
            tags.append("design")
        if "choose" in combined_text or "select" in combined_text:
            tags.append("selection")
        
        return tags
    
    async def _find_related_decisions(self, title: str) -> List[str]:
        """Find decisions related to the current one."""
        
        related = []
        title_words = set(title.lower().split())
        
        for decision_id, decision in self.decisions.items():
            decision_words = set(decision.title.lower().split())
            
            # Find decisions with overlapping keywords
            overlap = len(title_words.intersection(decision_words))
            if overlap >= 2:  # At least 2 words in common
                related.append(decision_id)
        
        return related[:3]  # Return top 3 related
    
    async def _save_memex(self):
        """Save current memex state to storage."""
        
        memex_data = {
            "version": "1.0",
            "created": time.time(),
            "last_updated": time.time(),
            "decisions": {},
            "project_context": asdict(self.project_context) if self.project_context else None,
            "metadata": {
                "total_decisions": len(self.decisions),
                "decision_types": self._count_decision_types(),
                "last_consultation": time.time()
            }
        }
        
        # Serialize decisions
        for decision_id, decision in self.decisions.items():
            decision_dict = asdict(decision)
            # Convert enums to strings
            decision_dict["decision_type"] = decision.decision_type.value
            decision_dict["status"] = decision.status.value
            memex_data["decisions"][decision_id] = decision_dict
        
        with open(self.memex_path, 'w') as f:
            json.dump(memex_data, f, indent=2)
    
    def _count_decision_types(self) -> Dict[str, int]:
        """Count decisions by type."""
        
        type_counts = {}
        for decision in self.decisions.values():
            decision_type = decision.decision_type.value
            type_counts[decision_type] = type_counts.get(decision_type, 0) + 1
        
        return type_counts
    
    async def get_decision_summary(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of a specific decision."""
        
        if decision_id not in self.decisions:
            return None
        
        decision = self.decisions[decision_id]
        
        return {
            "decision_id": decision.decision_id,
            "title": decision.title,
            "type": decision.decision_type.value,
            "chosen_solution": decision.chosen_solution,
            "alternatives_count": len(decision.alternatives_considered),
            "rationale": decision.rationale,
            "status": decision.status.value,
            "created_at": decision.created_at,
            "tags": decision.tags,
            "related_decisions": decision.related_decisions
        }
    
    async def get_recent_decisions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent decisions summary."""
        
        # Sort decisions by creation time
        sorted_decisions = sorted(
            self.decisions.values(),
            key=lambda d: d.created_at,
            reverse=True
        )
        
        recent_decisions = []
        for decision in sorted_decisions[:limit]:
            recent_decisions.append({
                "decision_id": decision.decision_id,
                "title": decision.title,
                "type": decision.decision_type.value,
                "status": decision.status.value,
                "created_at": decision.created_at
            })
        
        return recent_decisions
    
    def get_memex_status(self) -> Dict[str, Any]:
        """Get comprehensive memex status."""
        
        recent_queries = len([q for q in self.query_history if time.time() - q.timestamp < 3600])
        
        return {
            "memex_file": str(self.memex_path),
            "file_exists": self.memex_path.exists(),
            "total_decisions": len(self.decisions),
            "decision_types": self._count_decision_types(),
            "recent_queries_1h": recent_queries,
            "project_context": {
                "phase": self.project_context.project_phase if self.project_context else "unknown",
                "objectives": len(self.project_context.current_objectives) if self.project_context else 0,
                "constraints": len(self.project_context.active_constraints) if self.project_context else 0,
                "recent_decisions": len(self.project_context.recent_decisions) if self.project_context else 0
            },
            "last_updated": max([d.updated_at for d in self.decisions.values()]) if self.decisions else 0
        }


# Global project memex instance
PROJECT_MEMEX = PersistentProjectMemex()


async def mandatory_log_decision(decision_title: str, chosen_solution: str,
                                alternatives: List[Dict[str, Any]], rationale: str,
                                decision_type: DecisionType = DecisionType.TECHNICAL) -> str:
    """
    MANDATORY: Log key decision with alternatives and rationale
    
    This function MUST be called at the conclusion of any significant task
    according to JAEGIS Brain Protocol Suite Mandate 2.1.
    """
    
    return await PROJECT_MEMEX.mandatory_decision_logging(
        decision_title, chosen_solution, alternatives, rationale, decision_type
    )


async def mandatory_consult_precedents(task_description: str) -> List[DecisionRecord]:
    """
    MANDATORY: Consult memex for relevant precedents
    
    This function MUST be called before beginning any new task to ensure
    logical consistency with project history according to Mandate 2.1.
    """
    
    return await PROJECT_MEMEX.mandatory_precedent_consultation(task_description)


# Example usage
async def main():
    """Example usage of Persistent Project Memex."""
    
    print("📝 JAEGIS BRAIN PROTOCOL SUITE - PROJECT MEMEX TEST")
    
    # Test precedent consultation
    task = "Implement new authentication system"
    precedents = await PROJECT_MEMEX.mandatory_precedent_consultation(task)
    
    print(f"\n🔍 Precedent Consultation:")
    print(f"  Task: {task}")
    print(f"  Relevant precedents: {len(precedents)}")
    
    # Test decision logging
    alternatives = [
        {
            "description": "JWT-based authentication",
            "pros": ["Stateless", "Scalable", "Standard"],
            "cons": ["Token management complexity"],
            "estimated_effort": "2 weeks",
            "risk_level": "low",
            "rejection_reason": ""
        },
        {
            "description": "Session-based authentication",
            "pros": ["Simple", "Familiar"],
            "cons": ["Stateful", "Scaling issues"],
            "estimated_effort": "1 week",
            "risk_level": "medium",
            "rejection_reason": "Scaling concerns"
        }
    ]
    
    decision_id = await PROJECT_MEMEX.mandatory_decision_logging(
        "Authentication System Implementation",
        "Implement JWT-based authentication with refresh tokens",
        alternatives,
        "JWT provides better scalability and aligns with microservices architecture",
        DecisionType.SECURITY
    )
    
    print(f"\n📝 Decision Logged:")
    print(f"  Decision ID: {decision_id}")
    
    # Get recent decisions
    recent = await PROJECT_MEMEX.get_recent_decisions(5)
    print(f"\n📚 Recent Decisions: {len(recent)}")
    for decision in recent:
        print(f"  - {decision['title']} ({decision['type']})")
    
    # Get memex status
    status = PROJECT_MEMEX.get_memex_status()
    print(f"\n📊 Memex Status:")
    print(f"  Total Decisions: {status['total_decisions']}")
    print(f"  Decision Types: {status['decision_types']}")
    print(f"  Project Phase: {status['project_context']['phase']}")


if __name__ == "__main__":
    asyncio.run(main())
