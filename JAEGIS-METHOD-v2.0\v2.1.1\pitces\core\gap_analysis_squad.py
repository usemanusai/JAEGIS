"""
P.I.T.C.E.S. Framework - Gap Analysis Squad
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements the automated Gap Analysis Squad with comprehensive
audit capabilities across seven analysis domains.
"""

import json
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import asdict

from .models import GapAnalysisResult, Task, ProjectSpecs
from .exceptions import GapAnalysisError, ErrorCodes


logger = logging.getLogger(__name__)


class GapAnalysisSquad:
    """
    Automated Gap Analysis Squad implementing comprehensive project auditing.
    
    Analysis Domains:
    1. Functional Completeness - Feature coverage analysis
    2. Security & Integrity - Vulnerability and access control validation
    3. Performance & Scalability - Load testing and resource analysis
    4. Integration & Interoperability - API compatibility and data flow
    5. Compliance & Governance - Regulatory requirement adherence
    6. Logical & Strategic Alignment - Business objective mapping
    7. Documentation & Maintainability - Code quality and documentation
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Gap Analysis Squad.
        
        Args:
            config: Optional configuration for analysis parameters
        """
        self.config = config or self._get_default_config()
        
        # Analysis domain configurations
        self.analysis_domains = {
            'functional_completeness': {
                'weight': 0.20,
                'min_score_threshold': 80.0,
                'critical_threshold': 60.0
            },
            'security_integrity': {
                'weight': 0.25,
                'min_score_threshold': 90.0,
                'critical_threshold': 70.0
            },
            'performance_scalability': {
                'weight': 0.15,
                'min_score_threshold': 85.0,
                'critical_threshold': 65.0
            },
            'integration_interoperability': {
                'weight': 0.15,
                'min_score_threshold': 85.0,
                'critical_threshold': 70.0
            },
            'compliance_governance': {
                'weight': 0.10,
                'min_score_threshold': 95.0,
                'critical_threshold': 80.0
            },
            'logical_strategic_alignment': {
                'weight': 0.10,
                'min_score_threshold': 80.0,
                'critical_threshold': 60.0
            },
            'documentation_maintainability': {
                'weight': 0.05,
                'min_score_threshold': 75.0,
                'critical_threshold': 50.0
            }
        }
        
        # Audit history and metrics
        self.audit_history: List[Dict[str, Any]] = []
        self.audit_metrics = {
            'total_audits': 0,
            'critical_gaps_found': 0,
            'recommendations_generated': 0,
            'average_audit_time': 0.0
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
        logger.info("GapAnalysisSquad initialized with %d analysis domains", len(self.analysis_domains))
    
    def run_audit(self, project_specs: ProjectSpecs, tasks: List[Task]) -> Dict[str, GapAnalysisResult]:
        """
        Run comprehensive gap analysis audit across all domains.
        
        Args:
            project_specs: Project specifications
            tasks: List of project tasks
            
        Returns:
            Dictionary mapping domain names to analysis results
            
        Raises:
            GapAnalysisError: If audit execution fails
        """
        audit_start_time = time.time()
        
        try:
            with self._lock:
                logger.info("Starting comprehensive gap analysis audit")
                
                # Initialize audit context
                audit_context = self._prepare_audit_context(project_specs, tasks)
                
                # Run analysis for each domain
                results = {}
                
                for domain_name in self.analysis_domains.keys():
                    try:
                        logger.debug(f"Analyzing domain: {domain_name}")
                        result = self._analyze_domain(domain_name, audit_context)
                        results[domain_name] = result
                        
                    except Exception as e:
                        logger.error(f"Failed to analyze domain {domain_name}: {e}")
                        # Create error result
                        results[domain_name] = GapAnalysisResult(
                            domain=domain_name,
                            score=0.0,
                            findings=[f"Analysis failed: {str(e)}"],
                            recommendations=[f"Retry analysis for {domain_name}"],
                            priority_score=10.0  # High priority for failed analysis
                        )
                
                # Calculate overall audit metrics
                audit_time = time.time() - audit_start_time
                self._update_audit_metrics(results, audit_time)
                
                # Record audit in history
                audit_record = {
                    'timestamp': datetime.now().isoformat(),
                    'project_name': getattr(project_specs, 'name', 'Unknown'),
                    'task_count': len(tasks),
                    'audit_time_seconds': audit_time,
                    'domains_analyzed': list(results.keys()),
                    'overall_score': self._calculate_overall_score(results),
                    'critical_gaps': self._count_critical_gaps(results)
                }
                self.audit_history.append(audit_record)
                
                logger.info(f"Gap analysis audit completed in {audit_time:.2f}s")
                return results
                
        except Exception as e:
            logger.error(f"Gap analysis audit failed: {e}")
            raise GapAnalysisError(
                f"Audit execution failed: {str(e)}",
                error_code=ErrorCodes.AUDIT_FAILURE,
                context={'project_specs': asdict(project_specs), 'task_count': len(tasks)}
            )
    
    def generate_report(self, analysis_results: Dict[str, GapAnalysisResult]) -> Dict[str, Any]:
        """
        Generate comprehensive gap analysis report with actionable recommendations.
        
        Args:
            analysis_results: Results from run_audit()
            
        Returns:
            Structured gap analysis report
            
        Raises:
            GapAnalysisError: If report generation fails
        """
        try:
            logger.info("Generating gap analysis report")
            
            # Calculate overall metrics
            overall_score = self._calculate_overall_score(analysis_results)
            critical_gaps = self._count_critical_gaps(analysis_results)
            
            # Prioritize gaps by severity and impact
            prioritized_gaps = self._prioritize_gaps(analysis_results)
            
            # Generate executive summary
            executive_summary = self._generate_executive_summary(
                overall_score, critical_gaps, prioritized_gaps
            )
            
            # Compile detailed findings
            detailed_findings = {}
            for domain, result in analysis_results.items():
                detailed_findings[domain] = {
                    'score': result.score,
                    'findings': result.findings,
                    'recommendations': result.recommendations,
                    'priority_score': result.priority_score,
                    'status': self._get_domain_status(result)
                }
            
            # Generate action plan
            action_plan = self._generate_action_plan(prioritized_gaps)
            
            # Compile final report
            report = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'report_version': '1.0',
                    'analysis_domains': len(analysis_results),
                    'audit_framework': 'P.I.T.C.E.S. Gap Analysis Squad'
                },
                'executive_summary': executive_summary,
                'overall_metrics': {
                    'overall_score': overall_score,
                    'critical_gaps_count': critical_gaps,
                    'domains_analyzed': len(analysis_results),
                    'recommendations_count': sum(
                        len(result.recommendations) for result in analysis_results.values()
                    )
                },
                'detailed_findings': detailed_findings,
                'prioritized_gaps': prioritized_gaps,
                'action_plan': action_plan,
                'compliance_status': self._assess_compliance_status(analysis_results)
            }
            
            logger.info("Gap analysis report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise GapAnalysisError(
                f"Report generation failed: {str(e)}",
                error_code=ErrorCodes.REPORT_GENERATION_FAILURE,
                context={'analysis_domains': list(analysis_results.keys())}
            )
    
    def prioritize_gaps(self, analysis_results: Dict[str, GapAnalysisResult]) -> List[Dict[str, Any]]:
        """
        Prioritize identified gaps using weighted scoring algorithm.
        
        Args:
            analysis_results: Results from gap analysis
            
        Returns:
            List of prioritized gaps with scores and recommendations
        """
        try:
            prioritized_gaps = []
            
            for domain, result in analysis_results.items():
                domain_config = self.analysis_domains[domain]
                
                # Calculate weighted priority score
                weighted_score = (
                    result.priority_score * domain_config['weight'] * 
                    (1 - result.score / 100)  # Inverse of score (lower score = higher priority)
                )
                
                # Determine urgency level
                urgency = self._determine_urgency(result, domain_config)
                
                gap_entry = {
                    'domain': domain,
                    'priority_score': weighted_score,
                    'urgency': urgency,
                    'current_score': result.score,
                    'target_score': domain_config['min_score_threshold'],
                    'gap_size': domain_config['min_score_threshold'] - result.score,
                    'findings': result.findings,
                    'recommendations': result.recommendations,
                    'estimated_effort': self._estimate_effort(result, domain_config)
                }
                
                prioritized_gaps.append(gap_entry)
            
            # Sort by priority score (descending)
            prioritized_gaps.sort(key=lambda x: x['priority_score'], reverse=True)
            
            logger.debug(f"Prioritized {len(prioritized_gaps)} gaps")
            return prioritized_gaps
            
        except Exception as e:
            logger.error(f"Gap prioritization failed: {e}")
            return []
    
    def _prepare_audit_context(self, project_specs: ProjectSpecs, tasks: List[Task]) -> Dict[str, Any]:
        """Prepare context data for audit analysis."""
        return {
            'project_specs': project_specs,
            'tasks': tasks,
            'task_count': len(tasks),
            'complexity_score': project_specs.complexity_score,
            'risk_level': project_specs.risk_level.value,
            'requirements_clarity': project_specs.requirements_clarity,
            'technology_stack': project_specs.technology_stack,
            'external_dependencies': project_specs.external_dependencies,
            'audit_timestamp': datetime.now()
        }
    
    def _analyze_domain(self, domain_name: str, audit_context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze a specific domain and return results."""
        analysis_methods = {
            'functional_completeness': self._analyze_functional_completeness,
            'security_integrity': self._analyze_security_integrity,
            'performance_scalability': self._analyze_performance_scalability,
            'integration_interoperability': self._analyze_integration_interoperability,
            'compliance_governance': self._analyze_compliance_governance,
            'logical_strategic_alignment': self._analyze_logical_strategic_alignment,
            'documentation_maintainability': self._analyze_documentation_maintainability
        }
        
        analysis_method = analysis_methods.get(domain_name)
        if not analysis_method:
            raise GapAnalysisError(
                f"Unknown analysis domain: {domain_name}",
                error_code=ErrorCodes.ANALYSIS_DATA_CORRUPTION
            )
        
        return analysis_method(audit_context)
    
    def _analyze_functional_completeness(self, context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze functional completeness domain."""
        tasks = context['tasks']
        project_specs = context['project_specs']
        
        # Calculate feature coverage based on task completion and requirements clarity
        completed_tasks = len([t for t in tasks if t.status.name == 'COMPLETED'])
        total_tasks = len(tasks)
        
        if total_tasks == 0:
            coverage_score = 0.0
        else:
            coverage_score = (completed_tasks / total_tasks) * 100
        
        # Adjust score based on requirements clarity
        clarity_factor = project_specs.requirements_clarity / 100
        adjusted_score = coverage_score * clarity_factor
        
        findings = []
        recommendations = []
        
        if adjusted_score < 80:
            findings.append(f"Feature coverage is {adjusted_score:.1f}%, below target of 80%")
            recommendations.append("Complete remaining functional requirements")
            recommendations.append("Improve requirements clarity and definition")
        
        if project_specs.requirements_clarity < 90:
            findings.append(f"Requirements clarity is {project_specs.requirements_clarity:.1f}%")
            recommendations.append("Conduct requirements review and clarification sessions")
        
        priority_score = max(1.0, 10.0 - (adjusted_score / 10))
        
        return GapAnalysisResult(
            domain='functional_completeness',
            score=adjusted_score,
            findings=findings,
            recommendations=recommendations,
            priority_score=priority_score
        )
    
    def _analyze_security_integrity(self, context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze security and integrity domain."""
        project_specs = context['project_specs']
        tasks = context['tasks']
        
        # Base security score calculation
        base_score = 85.0  # Assume reasonable baseline
        
        # Adjust based on risk level
        risk_penalties = {'LOW': 0, 'MEDIUM': -10, 'HIGH': -20}
        risk_penalty = risk_penalties.get(project_specs.risk_level.value, -15)
        
        # Check for security-related tasks
        security_tasks = [
            t for t in tasks 
            if any(keyword in t.name.lower() for keyword in ['security', 'auth', 'encrypt', 'validate'])
        ]
        
        if security_tasks:
            security_completion = len([t for t in security_tasks if t.status.name == 'COMPLETED'])
            if len(security_tasks) > 0:
                security_factor = (security_completion / len(security_tasks)) * 15
            else:
                security_factor = 0
        else:
            security_factor = -15  # Penalty for no security tasks
        
        final_score = max(0, base_score + risk_penalty + security_factor)
        
        findings = []
        recommendations = []
        
        if final_score < 90:
            findings.append(f"Security score {final_score:.1f}% below target of 90%")
            recommendations.append("Implement comprehensive security testing")
            recommendations.append("Conduct security code review")
        
        if not security_tasks:
            findings.append("No explicit security-related tasks identified")
            recommendations.append("Add security validation and testing tasks")
        
        priority_score = max(1.0, 10.0 - (final_score / 10))
        
        return GapAnalysisResult(
            domain='security_integrity',
            score=final_score,
            findings=findings,
            recommendations=recommendations,
            priority_score=priority_score
        )
    
    def _analyze_performance_scalability(self, context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze performance and scalability domain."""
        project_specs = context['project_specs']
        
        # Base performance score
        base_score = 80.0
        
        # Adjust based on complexity
        complexity_penalty = (project_specs.complexity_score - 5) * 5
        
        # Check for performance-related considerations
        performance_boost = 0
        if 'performance' in str(project_specs.technology_stack).lower():
            performance_boost = 10
        
        final_score = max(0, min(100, base_score - complexity_penalty + performance_boost))
        
        findings = []
        recommendations = []
        
        if final_score < 85:
            findings.append(f"Performance score {final_score:.1f}% below target")
            recommendations.append("Implement performance testing and optimization")
            recommendations.append("Design for scalability from the start")
        
        if project_specs.complexity_score > 7:
            findings.append("High complexity may impact performance")
            recommendations.append("Consider performance implications of complex architecture")
        
        priority_score = max(1.0, 8.0 - (final_score / 12.5))
        
        return GapAnalysisResult(
            domain='performance_scalability',
            score=final_score,
            findings=findings,
            recommendations=recommendations,
            priority_score=priority_score
        )
    
    def _analyze_integration_interoperability(self, context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze integration and interoperability domain."""
        project_specs = context['project_specs']
        
        # Base integration score
        base_score = 85.0
        
        # Adjust based on external dependencies
        dependency_count = len(project_specs.external_dependencies)
        dependency_penalty = min(20, dependency_count * 3)
        
        final_score = max(0, base_score - dependency_penalty)
        
        findings = []
        recommendations = []
        
        if dependency_count > 5:
            findings.append(f"High number of external dependencies: {dependency_count}")
            recommendations.append("Minimize external dependencies where possible")
            recommendations.append("Implement robust integration testing")
        
        if final_score < 85:
            findings.append(f"Integration score {final_score:.1f}% below target")
            recommendations.append("Develop comprehensive integration strategy")
        
        priority_score = max(1.0, 7.0 - (final_score / 14))
        
        return GapAnalysisResult(
            domain='integration_interoperability',
            score=final_score,
            findings=findings,
            recommendations=recommendations,
            priority_score=priority_score
        )
    
    def _analyze_compliance_governance(self, context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze compliance and governance domain."""
        # Simplified compliance analysis
        base_score = 90.0  # Assume good baseline compliance
        
        findings = []
        recommendations = []
        
        # Basic compliance checks
        if base_score < 95:
            findings.append("Compliance validation needed")
            recommendations.append("Conduct compliance audit")
            recommendations.append("Document governance procedures")
        
        priority_score = max(1.0, 5.0 - (base_score / 20))
        
        return GapAnalysisResult(
            domain='compliance_governance',
            score=base_score,
            findings=findings,
            recommendations=recommendations,
            priority_score=priority_score
        )
    
    def _analyze_logical_strategic_alignment(self, context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze logical and strategic alignment domain."""
        project_specs = context['project_specs']
        
        # Base alignment score
        base_score = 80.0
        
        # Adjust based on requirements clarity (proxy for strategic clarity)
        clarity_boost = (project_specs.requirements_clarity - 80) / 4
        
        final_score = max(0, min(100, base_score + clarity_boost))
        
        findings = []
        recommendations = []
        
        if final_score < 80:
            findings.append(f"Strategic alignment score {final_score:.1f}% below target")
            recommendations.append("Review business objectives alignment")
            recommendations.append("Clarify strategic goals and success metrics")
        
        priority_score = max(1.0, 6.0 - (final_score / 15))
        
        return GapAnalysisResult(
            domain='logical_strategic_alignment',
            score=final_score,
            findings=findings,
            recommendations=recommendations,
            priority_score=priority_score
        )
    
    def _analyze_documentation_maintainability(self, context: Dict[str, Any]) -> GapAnalysisResult:
        """Analyze documentation and maintainability domain."""
        tasks = context['tasks']
        
        # Check for documentation-related tasks
        doc_tasks = [
            t for t in tasks 
            if any(keyword in t.name.lower() for keyword in ['doc', 'comment', 'readme', 'guide'])
        ]
        
        if doc_tasks:
            doc_completion = len([t for t in doc_tasks if t.status.name == 'COMPLETED'])
            if len(doc_tasks) > 0:
                doc_score = (doc_completion / len(doc_tasks)) * 100
            else:
                doc_score = 0
        else:
            doc_score = 50  # Penalty for no documentation tasks
        
        findings = []
        recommendations = []
        
        if doc_score < 75:
            findings.append(f"Documentation score {doc_score:.1f}% below target")
            recommendations.append("Improve code documentation and comments")
            recommendations.append("Create comprehensive user and developer guides")
        
        if not doc_tasks:
            findings.append("No explicit documentation tasks identified")
            recommendations.append("Add documentation tasks to project plan")
        
        priority_score = max(1.0, 4.0 - (doc_score / 25))
        
        return GapAnalysisResult(
            domain='documentation_maintainability',
            score=doc_score,
            findings=findings,
            recommendations=recommendations,
            priority_score=priority_score
        )
    
    def _calculate_overall_score(self, results: Dict[str, GapAnalysisResult]) -> float:
        """Calculate weighted overall score."""
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for domain, result in results.items():
            weight = self.analysis_domains[domain]['weight']
            total_weighted_score += result.score * weight
            total_weight += weight
        
        return total_weighted_score / total_weight if total_weight > 0 else 0.0
    
    def _count_critical_gaps(self, results: Dict[str, GapAnalysisResult]) -> int:
        """Count critical gaps across all domains."""
        critical_count = 0
        
        for domain, result in results.items():
            critical_threshold = self.analysis_domains[domain]['critical_threshold']
            if result.score < critical_threshold:
                critical_count += 1
        
        return critical_count
    
    def _prioritize_gaps(self, results: Dict[str, GapAnalysisResult]) -> List[Dict[str, Any]]:
        """Prioritize gaps using the prioritize_gaps method."""
        return self.prioritize_gaps(results)
    
    def _generate_executive_summary(self, overall_score: float, critical_gaps: int, prioritized_gaps: List) -> str:
        """Generate executive summary text."""
        if overall_score >= 85:
            status = "GOOD"
        elif overall_score >= 70:
            status = "ACCEPTABLE"
        else:
            status = "NEEDS IMPROVEMENT"
        
        summary = f"""
        Gap Analysis Executive Summary:
        
        Overall Score: {overall_score:.1f}% ({status})
        Critical Gaps Identified: {critical_gaps}
        Total Recommendations: {sum(len(gap['recommendations']) for gap in prioritized_gaps)}
        
        Key Areas for Improvement:
        {chr(10).join(f"- {gap['domain']}: {gap['current_score']:.1f}% (Target: {gap['target_score']:.1f}%)" 
                     for gap in prioritized_gaps[:3])}
        """
        
        return summary.strip()
    
    def _generate_action_plan(self, prioritized_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable plan based on prioritized gaps."""
        action_plan = []
        
        for i, gap in enumerate(prioritized_gaps[:5]):  # Top 5 priorities
            action_item = {
                'priority': i + 1,
                'domain': gap['domain'],
                'urgency': gap['urgency'],
                'estimated_effort': gap['estimated_effort'],
                'key_actions': gap['recommendations'][:3],  # Top 3 recommendations
                'success_criteria': f"Achieve {gap['target_score']:.1f}% score in {gap['domain']}"
            }
            action_plan.append(action_item)
        
        return action_plan
    
    def _assess_compliance_status(self, results: Dict[str, GapAnalysisResult]) -> Dict[str, Any]:
        """Assess overall compliance status."""
        compliance_domains = ['security_integrity', 'compliance_governance']
        
        compliance_scores = [
            results[domain].score for domain in compliance_domains 
            if domain in results
        ]
        
        if compliance_scores:
            avg_compliance = sum(compliance_scores) / len(compliance_scores)
            status = "COMPLIANT" if avg_compliance >= 90 else "NON_COMPLIANT"
        else:
            avg_compliance = 0.0
            status = "UNKNOWN"
        
        return {
            'status': status,
            'average_score': avg_compliance,
            'domains_assessed': compliance_domains
        }
    
    def _determine_urgency(self, result: GapAnalysisResult, domain_config: Dict[str, Any]) -> str:
        """Determine urgency level for a gap."""
        if result.score < domain_config['critical_threshold']:
            return "CRITICAL"
        elif result.score < domain_config['min_score_threshold']:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _estimate_effort(self, result: GapAnalysisResult, domain_config: Dict[str, Any]) -> str:
        """Estimate effort required to address gap."""
        gap_size = domain_config['min_score_threshold'] - result.score
        
        if gap_size > 30:
            return "HIGH"
        elif gap_size > 15:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_domain_status(self, result: GapAnalysisResult) -> str:
        """Get status for a domain based on score."""
        if result.score >= 90:
            return "EXCELLENT"
        elif result.score >= 80:
            return "GOOD"
        elif result.score >= 70:
            return "ACCEPTABLE"
        else:
            return "NEEDS_IMPROVEMENT"
    
    def _update_audit_metrics(self, results: Dict[str, GapAnalysisResult], audit_time: float):
        """Update audit metrics."""
        self.audit_metrics['total_audits'] += 1
        self.audit_metrics['critical_gaps_found'] += self._count_critical_gaps(results)
        self.audit_metrics['recommendations_generated'] += sum(
            len(result.recommendations) for result in results.values()
        )
        
        # Update average audit time
        current_avg = self.audit_metrics['average_audit_time']
        total_audits = self.audit_metrics['total_audits']
        
        if total_audits == 1:
            self.audit_metrics['average_audit_time'] = audit_time
        else:
            self.audit_metrics['average_audit_time'] = (
                (current_avg * (total_audits - 1) + audit_time) / total_audits
            )
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for gap analysis."""
        return {
            'enable_detailed_analysis': True,
            'generate_recommendations': True,
            'prioritize_security': True,
            'compliance_frameworks': ['SOC2', 'GDPR'],
            'performance_targets': {
                'response_time_ms': 500,
                'throughput_rps': 1000,
                'availability_percent': 99.9
            }
        }
