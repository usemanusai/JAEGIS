"""
JAEGIS Enhanced System v2.0 - Agent Temporal Compliance System
Monitors and ensures all 74 agents in the JAEGIS ecosystem maintain temporal accuracy
Validates and updates agent protocols, rules, and references to use current dates
"""

import asyncio
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid

logger = logging.getLogger(__name__)

class ComplianceLevel(Enum):
    """Agent temporal compliance levels"""
    FULLY_COMPLIANT = "fully_compliant"
    MOSTLY_COMPLIANT = "mostly_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"

class AgentTier(Enum):
    """JAEGIS agent tier classification"""
    TIER_1_ORCHESTRATOR = "tier_1_orchestrator"
    TIER_2_PRIMARY = "tier_2_primary"
    TIER_3_SECONDARY = "tier_3_secondary"
    TIER_4_SPECIALIZED = "tier_4_specialized"

@dataclass
class TemporalComplianceReport:
    """Temporal compliance report for an agent"""
    agent_id: str
    agent_name: str
    agent_tier: AgentTier
    compliance_level: ComplianceLevel
    compliance_score: float
    issues_found: List[str]
    recommendations: List[str]
    last_updated: datetime
    temporal_references: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_tier": self.agent_tier.value,
            "compliance_level": self.compliance_level.value,
            "compliance_score": self.compliance_score,
            "issues_found": self.issues_found,
            "recommendations": self.recommendations,
            "last_updated": self.last_updated.isoformat(),
            "temporal_references": self.temporal_references
        }

class AgentTemporalComplianceSystem:
    """Comprehensive temporal compliance system for all JAEGIS agents"""
    
    def __init__(self):
        # Agent registry and compliance tracking
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.compliance_reports: Dict[str, TemporalComplianceReport] = {}
        
        # Temporal compliance rules
        self.compliance_rules = self._initialize_compliance_rules()
        
        # Agent tier definitions
        self.agent_tiers = self._initialize_agent_tiers()
        
        # Monitoring configuration
        self.monitoring_active = False
        self.monitoring_interval = 3600  # 1 hour
        self.compliance_threshold = 0.8  # 80% compliance required
        
        # Statistics
        self.compliance_stats = {
            "total_agents": 0,
            "compliant_agents": 0,
            "non_compliant_agents": 0,
            "last_full_scan": None,
            "issues_resolved": 0
        }
        
        logger.info("Agent Temporal Compliance System initialized")
    
    def _initialize_compliance_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize temporal compliance rules""return_date_references": {
                "description": "Check for hardcoded date references",
                "patterns": [
                    r'\b202[0-3]\b',  # Years 2020-2023
                    r'\b2024\b(?!\s*-\s*2025)',  # 2024 without range
                    r'(?i)last\s+year(?!\s+2024)',  # "last year" without context
                    r'(?i)this\s+year(?!\s+2025)',  # "this year" without context
                ],
                "severity": "high",
                "auto_fixTrue_temporal_keywords": {
                "description": "Check for outdated temporal keywords",
                "patterns": [
                    r'(?i)\bcurrent(?!\s+2025)',  # "current" without year
                    r'(?i)\blatest(?!\s+2025)',  # "latest" without year
                    r'(?i)\brecent(?!\s+2024-2025)',  # "recent" without timeframe
                    r'(?i)\bup-to-date(?!\s+2025)',  # "up-to-date" without year
                ],
                "severity": "medium",
                "auto_fixTrue_research_queries": {
                "description": "Check research queries for temporal context",
                "patterns": [
                    r'(?i)best\s+practices(?!\s+2025)',
                    r'(?i)guide(?!\s+2025)',
                    r'(?i)tutorial(?!\s+2025)',
                    r'(?i)trends(?!\s+2024-2025)',
                ],
                "severity": "high",
                "auto_fixTrue_protocol_rules": {
                "description": "Check protocol rules for temporal accuracy",
                "patterns": [
                    r'(?i)as\s+of\s+202[0-3]',  # "as of 2020-2023"
                    r'(?i)since\s+202[0-3]',  # "since 2020-2023"
                    r'(?i)until\s+202[0-3]',  # "until 2020-2023"
                ],
                "severity": "medium",
                "auto_fix": False
            }
        }
    
    def _initialize_agent_tiers(self) -> Dict[str, AgentTier]:
        """Initialize agent tier classifications"""
        
        return {
            # Tier 1: Orchestrator
            "JAEGIS_orchestrator": AgentTier.TIER_1_ORCHESTRATOR,
            
            # Tier 2: Primary Agents
            "product_manager": AgentTier.TIER_2_PRIMARY,
            "system_architect": AgentTier.TIER_2_PRIMARY,
            "task_breakdown_specialist": AgentTier.TIER_2_PRIMARY,
            
            # Tier 3: Secondary Agents (16 agents)
            "design_architect": AgentTier.TIER_3_SECONDARY,
            "platform_engineer": AgentTier.TIER_3_SECONDARY,
            "full_stack_developer": AgentTier.TIER_3_SECONDARY,
            "data_engineer": AgentTier.TIER_3_SECONDARY,
            "validation_engineer": AgentTier.TIER_3_SECONDARY,
            "qa_specialist": AgentTier.TIER_3_SECONDARY,
            "business_analyst": AgentTier.TIER_3_SECONDARY,
            "product_owner": AgentTier.TIER_3_SECONDARY,
            "meta_orchestrator": AgentTier.TIER_3_SECONDARY,
            "scrum_master": AgentTier.TIER_3_SECONDARY,
            "time_manager": AgentTier.TIER_3_SECONDARY,
            "technical_writer": AgentTier.TIER_3_SECONDARY,
            "content_optimizer": AgentTier.TIER_3_SECONDARY,
            "agent_creator": AgentTier.TIER_3_SECONDARY,
            "recovery_specialist": AgentTier.TIER_3_SECONDARY,
            "integration_specialist": AgentTier.TIER_3_SECONDARY,
            
            # Tier 4: Specialized Agents (4 agents)
            "web_agent_creator": AgentTier.TIER_4_SPECIALIZED,
            "ide_integration_specialist": AgentTier.TIER_4_SPECIALIZED,
            "devops_ide_specialist": AgentTier.TIER_4_SPECIALIZED,
            "advanced_ide_developer": AgentTier.TIER_4_SPECIALIZED
        }
    
    async def register_agent(self, agent_id: str, agent_data: Dict[str, Any]) -> str:
        """Register an agent for temporal compliance monitoring"""
        
        # Determine agent tier
        agent_tier = self.agent_tiers.get(agent_id, AgentTier.TIER_3_SECONDARY)
        
        # Store agent data
        self.agent_registry[agent_id] = {
            **agent_data,
            "agent_tier": agent_tier,
            "registered_at": datetime.now(),
            "last_compliance_check": None
        }
        
        # Perform initial compliance check
        compliance_report = await self.check_agent_compliance(agent_id)
        
        # Update statistics
        self.compliance_stats["total_agents"] = len(self.agent_registry)
        
        logger.info(f"Agent {agent_id} registered for temporal compliance monitoring")
        
        return compliance_report.compliance_level.value
    
    async def check_agent_compliance(self, agent_id: str) -> TemporalComplianceReport:
        """Check temporal compliance for a specific agent"""
        
        if agent_id not in self.agent_registry:
            raise ValueError(f"Agent {agent_id} not registered")
        
        agent_data = self.agent_registry[agent_id]
        agent_tier = agent_data["agent_tier"]
        
        # Analyze agent data for temporal compliance
        compliance_analysis = await self._analyze_agent_temporal_compliance(agent_data)
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(compliance_analysis)
        
        # Determine compliance level
        compliance_level = self._determine_compliance_level(compliance_score)
        
        # Generate recommendations
        recommendations = self._generate_compliance_recommendations(compliance_analysis, agent_tier)
        
        # Create compliance report
        compliance_report = TemporalComplianceReport(
            agent_id=agent_id,
            agent_name=agent_data.get("name", agent_id),
            agent_tier=agent_tier,
            compliance_level=compliance_level,
            compliance_score=compliance_score,
            issues_found=compliance_analysis["issues"],
            recommendations=recommendations,
            last_updated=datetime.now(),
            temporal_references=compliance_analysis["temporal_references"]
        )
        
        # Store compliance report
        self.compliance_reports[agent_id] = compliance_report
        
        # Update agent registry
        self.agent_registry[agent_id]["last_compliance_check"] = datetime.now()
        
        return compliance_report
    
    async def _analyze_agent_temporal_compliance(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze agent data for temporal compliance issues"""
        
        issues = []
        temporal_references = {}
        
        # Convert agent data to searchable text
        agent_text = json.dumps(agent_data, default=str)
        
        # Check each compliance rule
        for rule_name, rule_config in self.compliance_rules.items():
            rule_issues = []
            
            for pattern in rule_config["patterns"]:
                matches = re.findall(pattern, agent_text)
                
                if matches:
                    rule_issues.extend([
                        f"{rule_name}: Found '{match}' - {rule_config['description']}"
                        for match in matches
                    ])
            
            if rule_issues:
                issues.extend(rule_issues)
                temporal_references[rule_name] = {
                    "issues_count": len(rule_issues),
                    "severity": rule_config["severity"],
                    "auto_fixable": rule_config["auto_fix"]
                }
        
        # Check for missing temporal context
        missing_context_issues = self._check_missing_temporal_context(agent_data)
        issues.extend(missing_context_issues)
        
        return {
            "issues": issues,
            "temporal_references": temporal_references,
            "total_issues": len(issues)
        }
    
    def _check_missing_temporal_context(self, agent_data: Dict[str, Any]) -> List[str]:
        """Check for missing temporal context in agent data"""
        
        missing_context_issues = []
        
        # Check if agent has any temporal context
        agent_text = json.dumps(agent_data, default=str).lower()
        
        # Look for temporal indicators
        temporal_indicators = ["2025", "2024-2025", "current", "latest", "recent"]
        
        has_temporal_context = any(indicator in agent_text for indicator in temporal_indicators)
        
        if not has_temporal_context:
            missing_context_issues.append("Missing temporal context - no current date references found")
        
        # Check specific fields that should have temporal context
        temporal_fields = ["description", "protocols", "rules", "guidelines"]
        
        for field in temporal_fields:
            if field in agent_data and agent_data[field]:
                field_text = str(agent_data[field]).lower()
                
                if not any(indicator in field_text for indicator in temporal_indicators):
                    missing_context_issues.append(f"Field '{field}' lacks temporal context")
        
        return missing_context_issues
    
    def _calculate_compliance_score(self, compliance_analysis: Dict[str, Any]) -> float:
        """Calculate compliance score based on analysis"""
        
        total_issues = compliance_analysis["total_issues"]
        
        if total_issues == 0:
            return 1.0  # Perfect compliance
        
        # Weight issues by severity
        severity_weights = {"high": 0.3, "medium": 0.2, "low": 0.1}
        
        weighted_issues = 0
        for rule_name, rule_data in compliance_analysis["temporal_references"].items():
            severity = rule_data["severity"]
            issues_count = rule_data["issues_count"]
            weight = severity_weights.get(severity, 0.1)
            weighted_issues += issues_count * weight
        
        # Calculate score (1.0 - penalty)
        max_penalty = 1.0
        penalty = min(weighted_issues / 10.0, max_penalty)  # Normalize to 0-1
        
        return max(0.0, 1.0 - penalty)
    
    def _determine_compliance_level(self, compliance_score: float) -> ComplianceLevel:
        """Determine compliance level based on score"""
        
        if compliance_score >= 0.9:
            return ComplianceLevel.FULLY_COMPLIANT
        elif compliance_score >= 0.7:
            return ComplianceLevel.MOSTLY_COMPLIANT
        elif compliance_score >= 0.5:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _generate_compliance_recommendations(self, compliance_analysis: Dict[str, Any], 
                                           agent_tier: AgentTier) -> List[str]:
        """Generate compliance recommendations"""
        
        recommendations = []
        
        # General recommendations based on issues
        if compliance_analysis["total_issues"] > 0:
            recommendations.append("Update temporal references to use current dates (2025)")
            recommendations.append("Add temporal context to research queries and protocols")
        
        # Tier-specific recommendations
        if agent_tier == AgentTier.TIER_1_ORCHESTRATOR:
            recommendations.append("As orchestrator, ensure all coordinated agents maintain temporal accuracy")
            recommendations.append("Implement temporal validation in agent coordination workflows")
        
        elif agent_tier == AgentTier.TIER_2_PRIMARY:
            recommendations.append("As primary agent, set temporal compliance example for secondary agents")
            recommendations.append("Include current date validation in all major decision processes")
        
        elif agent_tier == AgentTier.TIER_3_SECONDARY:
            recommendations.append("Align temporal references with primary agents and orchestrator")
            recommendations.append("Update specialized protocols to reflect current timeframes")
        
        elif agent_tier == AgentTier.TIER_4_SPECIALIZED:
            recommendations.append("Ensure specialized capabilities use current technology standards")
            recommendations.append("Update domain-specific temporal references")
        
        # Auto-fix recommendations
        auto_fixable_issues = [
            rule_name for rule_name, rule_data in compliance_analysis["temporal_references"].items()
            if rule_data["auto_fixable"]
        ]
        
        if auto_fixable_issues:
            recommendations.append(f"Auto-fix available for: {', '.join(auto_fixable_issues)}")
        
        return recommendations
    
    async def update_agent_temporal_compliance(self, agent_id: str, auto_fix: bool = True) -> Dict[str, Any]:
        """Update agent to achieve temporal compliance"""
        
        if agent_id not in self.agent_registry:
            raise ValueError(f"Agent {agent_id} not registered")
        
        # Get current compliance report
        compliance_report = await self.check_agent_compliance(agent_id)
        
        if compliance_report.compliance_level == ComplianceLevel.FULLY_COMPLIANT:
            return {
                "agent_id": agent_id,
                "already_compliant": True,
                "compliance_score": compliance_report.compliance_score
            }
        
        # Apply fixes
        agent_data = self.agent_registry[agent_id].copy()
        fixes_applied = []
        
        if auto_fix:
            # Apply automatic fixes
            for rule_name, rule_config in self.compliance_rules.items():
                if rule_config["auto_fix"]:
                    fixes = await self._apply_auto_fixes(agent_data, rule_name, rule_config)
                    fixes_applied.extend(fixes)
        
        # Update agent data
        self.agent_registry[agent_id].update(agent_data)
        
        # Re-check compliance
        updated_compliance_report = await self.check_agent_compliance(agent_id)
        
        # Update statistics
        if updated_compliance_report.compliance_level in [ComplianceLevel.FULLY_COMPLIANT, ComplianceLevel.MOSTLY_COMPLIANT]:
            self.compliance_stats["issues_resolved"] += len(fixes_applied)
        
        return {
            "agent_id": agent_id,
            "compliance_updated": True,
            "fixes_applied": fixes_applied,
            "original_score": compliance_report.compliance_score,
            "updated_score": updated_compliance_report.compliance_score,
            "compliance_level": updated_compliance_report.compliance_level.value
        }
    
    async def _apply_auto_fixes(self, agent_data: Dict[str, Any], rule_name: str, 
                              rule_config: Dict[str, Any]) -> List[str]:
        """Apply automatic fixes for compliance issues"""
        
        fixes_applied = []
        current_year = datetime.now().year
        
        # Convert agent data to JSON string for processing
        agent_json = json.dumps(agent_data, default=str, indent=2)
        
        if rule_name == "date_references":
            # Fix hardcoded date references
            original_json = agent_json
            
            # Update years 2020-2023 to current year
            agent_json = re.sub(r'\b202[0-3]\b', str(current_year), agent_json)
            
            # Update standalone 2024 to 2024-2025 range
            agent_json = re.sub(r'\b2024\b(?!\s*-\s*2025)', '2024-2025', agent_json)
            
            if agent_json != original_json:
                fixes_applied.append("Updated hardcoded date references")
        
        elif rule_name == "temporal_keywords":
            # Fix temporal keywords
            original_json = agent_json
            
            # Add year context to temporal keywords
            agent_json = re.sub(r'\bcurrent\b(?!\s+2025)', f'current {current_year}', agent_json)
            agent_json = re.sub(r'\blatest\b(?!\s+2025)', f'latest {current_year}', agent_json)
            agent_json = re.sub(r'\brecent\b(?!\s+2024-2025)', 'recent 2024-2025', agent_json)
            
            if agent_json != original_json:
                fixes_applied.append("Added temporal context to keywords")
        
        elif rule_name == "research_queries":
            # Fix research queries
            original_json = agent_json
            
            # Add year context to research-related terms
            agent_json = re.sub(r'\bbest practices\b(?!\s+2025)', f'best practices {current_year}', agent_json)
            agent_json = re.sub(r'\bguide\b(?!\s+2025)', f'guide {current_year}', agent_json)
            agent_json = re.sub(r'\btrends\b(?!\s+2024-2025)', 'trends 2024-2025', agent_json)
            
            if agent_json != original_json:
                fixes_applied.append("Updated research queries with temporal context")
        
        # Convert back to dictionary
        try:
            updated_agent_data = json.loads(agent_json)
            agent_data.update(updated_agent_data)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse updated agent data for {rule_name}")
        
        return fixes_applied
    
    async def monitor_all_agents(self) -> Dict[str, Any]:
        """Monitor temporal compliance across all registered agents"""
        
        compliance_summary = {
            "total_agents": len(self.agent_registry),
            "fully_compliant": 0,
            "mostly_compliant": 0,
            "partially_compliant": 0,
            "non_compliant": 0,
            "compliance_rate0_0_issues_by_tier": {},
            "recommendations_summary": []
        }
        
        # Check compliance for all agents
        for agent_id in self.agent_registry.keys():
            try:
                compliance_report = await self.check_agent_compliance(agent_id)
                
                # Update summary counts
                if compliance_report.compliance_level == ComplianceLevel.FULLY_COMPLIANT:
                    compliance_summary["fully_compliant"] += 1
                elif compliance_report.compliance_level == ComplianceLevel.MOSTLY_COMPLIANT:
                    compliance_summary["mostly_compliant"] += 1
                elif compliance_report.compliance_level == ComplianceLevel.PARTIALLY_COMPLIANT:
                    compliance_summary["partially_compliant"] += 1
                else:
                    compliance_summary["non_compliant"] += 1
                
                # Track issues by tier
                tier = compliance_report.agent_tier.value
                if tier not in compliance_summary["issues_by_tier"]:
                    compliance_summary["issues_by_tier"][tier] = 0
                compliance_summary["issues_by_tier"][tier] += len(compliance_report.issues_found)
                
            except Exception as e:
                logger.error(f"Error checking compliance for agent {agent_id}: {e}")
        
        # Calculate overall compliance rate
        compliant_agents = compliance_summary["fully_compliant"] + compliance_summary["mostly_compliant"]
        compliance_summary["compliance_rate"] = compliant_agents / max(compliance_summary["total_agents"], 1)
        
        # Update statistics
        self.compliance_stats.update({
            "total_agents": compliance_summary["total_agents"],
            "compliant_agents": compliant_agents,
            "non_compliant_agents": compliance_summary["non_compliant"] + compliance_summary["partially_compliant"],
            "last_full_scan": datetime.now()
        })
        
        return compliance_summary
    
    async def start_compliance_monitoring(self, interval_hours: int = 1) -> Dict[str, Any]:
        """Start continuous compliance monitoring"""
        
        self.monitoring_active = True
        self.monitoring_interval = interval_hours * 3600  # Convert to seconds
        
        # Start monitoring task
        asyncio.create_task(self._compliance_monitoring_loop())
        
        logger.info(f"Agent temporal compliance monitoring started (interval: {interval_hours} hours)")
        
        return {
            "monitoring_started": True,
            "interval_hours": interval_hours,
            "registered_agents": len(self.agent_registry)
        }
    
    async def _compliance_monitoring_loop(self):
        """Continuous compliance monitoring loop"""
        
        while self.monitoring_active:
            try:
                # Monitor all agents
                monitoring_result = await self.monitor_all_agents()
                
                # Log compliance status
                compliance_rate = monitoring_result["compliance_rate"]
                logger.info(f"Agent compliance monitoring: {compliance_rate:.1%} compliant")
                
                # Auto-fix non-compliant agents if enabled
                if compliance_rate < self.compliance_threshold:
                    await self._auto_fix_non_compliant_agents()
                
                # Wait for next monitoring cycle
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Compliance monitoring error: {e}")
                await asyncio.sleep(1800)  # Wait 30 minutes on error
    
    async def _auto_fix_non_compliant_agents(self):
        """Automatically fix non-compliant agents"""
        
        non_compliant_agents = [
            agent_id for agent_id, report in self.compliance_reports.items()
            if report.compliance_level in [ComplianceLevel.NON_COMPLIANT, ComplianceLevel.PARTIALLY_COMPLIANT]
        ]
        
        for agent_id in non_compliant_agents:
            try:
                await self.update_agent_temporal_compliance(agent_id, auto_fix=True)
                logger.info(f"Auto-fixed temporal compliance for agent {agent_id}")
            except Exception as e:
                logger.error(f"Failed to auto-fix agent {agent_id}: {e}")
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """Get comprehensive compliance status"""
        
        return {
            "monitoring_active": self.monitoring_active,
            "monitoring_interval_hours": self.monitoring_interval / 3600,
            "compliance_threshold": self.compliance_threshold,
            "statistics": self.compliance_stats.copy(),
            "registered_agents": len(self.agent_registry),
            "compliance_reportslen_self_compliance_reports_agent_tiers": {tier.value: len([a for a in self.agent_registry.values() if a["agent_tier"] == tier]) 
                           for tier in AgentTier}
        }
    
    async def stop_compliance_monitoring(self):
        """Stop compliance monitoring"""
        
        self.monitoring_active = False
        logger.info("Agent temporal compliance monitoring stopped")
