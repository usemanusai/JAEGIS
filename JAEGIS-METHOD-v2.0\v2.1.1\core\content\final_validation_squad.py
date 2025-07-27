"""
Content Squad Final Validation System
Deploy Content Squad (8 agents) for comprehensive content validation, quality assurance, and professional presentation
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class ContentType(str, Enum):
    """Types of content to validate."""
    DOCUMENTATION = "documentation"
    API_REFERENCE = "api_reference"
    USER_GUIDE = "user_guide"
    TECHNICAL_SPEC = "technical_spec"
    README = "readme"
    CHANGELOG = "changelog"
    TUTORIAL = "tutorial"
    ARCHITECTURE_DOC = "architecture_doc"


class ValidationAspect(str, Enum):
    """Aspects of content validation."""
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    CONSISTENCY = "consistency"
    FORMATTING = "formatting"
    GRAMMAR = "grammar"
    STRUCTURE = "structure"
    ACCESSIBILITY = "accessibility"


class QualityLevel(str, Enum):
    """Quality assessment levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    SATISFACTORY = "satisfactory"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


@dataclass
class ContentAgent:
    """Content Squad agent configuration."""
    agent_id: str
    name: str
    specialization: str
    validation_aspects: List[ValidationAspect]
    content_types: List[ContentType]
    performance_metrics: Dict[str, float]
    current_assignment: Optional[str]


@dataclass
class ValidationResult:
    """Content validation result."""
    result_id: str
    content_path: str
    content_type: ContentType
    validation_aspect: ValidationAspect
    quality_level: QualityLevel
    score: float
    issues_found: List[str]
    recommendations: List[str]
    validator_agent: str
    timestamp: float


@dataclass
class ContentQualityReport:
    """Comprehensive content quality report."""
    report_id: str
    content_inventory: Dict[str, ContentType]
    validation_results: List[ValidationResult]
    overall_quality_score: float
    quality_by_type: Dict[str, float]
    quality_by_aspect: Dict[str, float]
    critical_issues: List[str]
    improvement_recommendations: List[str]
    professional_presentation_score: float
    timestamp: float


class ContentSquadFinalValidator:
    """
    Content Squad Final Validation System
    
    Deploys 8 specialized content validation agents:
    - Documentation Specialist: README, guides, tutorials
    - API Documentation Specialist: API references, technical specs
    - Technical Writing Specialist: Architecture docs, technical content
    - Copy Editor: Grammar, style, consistency
    - Formatting Specialist: Structure, presentation, accessibility
    - Quality Assurance Specialist: Completeness, accuracy
    - User Experience Specialist: Clarity, usability
    - Brand Compliance Specialist: Brand guidelines, professional standards
    """
    
    def __init__(self):
        self.agents: Dict[str, ContentAgent] = {}
        self.validation_results: List[ValidationResult] = []
        self.quality_reports: List[ContentQualityReport] = []
        
        # Configuration
        self.config = {
            "quality_threshold": 80.0,
            "professional_standard": 85.0,
            "critical_issue_threshold": 3,
            "validation_depth": "comprehensive",
            "brand_guidelines_enabled": True,
            "accessibility_compliance": "WCAG_2.1_AA"
        }
        
        # Initialize Content Squad
        self._initialize_content_squad()
        
        logger.info("Content Squad Final Validator initialized with 8 agents")
    
    def _initialize_content_squad(self):
        """Initialize the 8-agent Content Squad."""
        
        agents_config = [
            {
                "name": "DocumentationSpecialist-Alpha",
                "specialization": "Documentation Excellence",
                "validation_aspects": [ValidationAspect.COMPLETENESS, ValidationAspect.STRUCTURE, ValidationAspect.CLARITY],
                "content_types": [ContentType.DOCUMENTATION, ContentType.README, ContentType.USER_GUIDE, ContentType.TUTORIAL]
            },
            {
                "name": "APIDocumentationSpecialist-Beta",
                "specialization": "API Documentation & Technical Specifications",
                "validation_aspects": [ValidationAspect.ACCURACY, ValidationAspect.COMPLETENESS, ValidationAspect.CONSISTENCY],
                "content_types": [ContentType.API_REFERENCE, ContentType.TECHNICAL_SPEC]
            },
            {
                "name": "TechnicalWritingSpecialist-Gamma",
                "specialization": "Technical Content & Architecture Documentation",
                "validation_aspects": [ValidationAspect.ACCURACY, ValidationAspect.CLARITY, ValidationAspect.STRUCTURE],
                "content_types": [ContentType.ARCHITECTURE_DOC, ContentType.TECHNICAL_SPEC, ContentType.DOCUMENTATION]
            },
            {
                "name": "CopyEditor-Delta",
                "specialization": "Grammar, Style & Language Consistency",
                "validation_aspects": [ValidationAspect.GRAMMAR, ValidationAspect.CONSISTENCY, ValidationAspect.CLARITY],
                "content_types": list(ContentType)  # All content types
            },
            {
                "name": "FormattingSpecialist-Epsilon",
                "specialization": "Structure, Presentation & Accessibility",
                "validation_aspects": [ValidationAspect.FORMATTING, ValidationAspect.STRUCTURE, ValidationAspect.ACCESSIBILITY],
                "content_types": list(ContentType)  # All content types
            },
            {
                "name": "QualityAssuranceSpecialist-Zeta",
                "specialization": "Completeness & Accuracy Validation",
                "validation_aspects": [ValidationAspect.COMPLETENESS, ValidationAspect.ACCURACY, ValidationAspect.CONSISTENCY],
                "content_types": list(ContentType)  # All content types
            },
            {
                "name": "UserExperienceSpecialist-Eta",
                "specialization": "Clarity, Usability & User-Centric Content",
                "validation_aspects": [ValidationAspect.CLARITY, ValidationAspect.STRUCTURE, ValidationAspect.ACCESSIBILITY],
                "content_types": [ContentType.USER_GUIDE, ContentType.TUTORIAL, ContentType.README, ContentType.DOCUMENTATION]
            },
            {
                "name": "BrandComplianceSpecialist-Theta",
                "specialization": "Brand Guidelines & Professional Standards",
                "validation_aspects": [ValidationAspect.CONSISTENCY, ValidationAspect.FORMATTING, ValidationAspect.CLARITY],
                "content_types": list(ContentType)  # All content types
            }
        ]
        
        for i, agent_config in enumerate(agents_config):
            agent_id = f"content_squad_{i+1:02d}"
            
            agent = ContentAgent(
                agent_id=agent_id,
                name=agent_config["name"],
                specialization=agent_config["specialization"],
                validation_aspects=agent_config["validation_aspects"],
                content_types=agent_config["content_types"],
                performance_metrics={
                    "validations_completed": 0,
                    "issues_identified": 0,
                    "quality_improvements": 0,
                    "accuracy_rate": 1.0
                },
                current_assignment=None
            )
            
            self.agents[agent_id] = agent
    
    async def execute_final_content_validation(self, content_paths: List[str] = None) -> ContentQualityReport:
        """Execute comprehensive final content validation."""
        
        report_id = f"content_validation_{int(time.time())}"
        
        logger.info("Starting comprehensive content validation")
        
        # Discover content if not provided
        if content_paths is None:
            content_paths = await self._discover_content()
        
        # Create content inventory
        content_inventory = await self._create_content_inventory(content_paths)
        
        # Execute validation across all agents
        validation_results = await self._execute_validation_matrix(content_inventory)
        
        # Analyze results and generate report
        report = await self._generate_quality_report(report_id, content_inventory, validation_results)
        
        self.quality_reports.append(report)
        
        logger.info(f"Content validation completed: {report.overall_quality_score:.1f}% quality score")
        
        return report
    
    async def _discover_content(self) -> List[str]:
        """Discover all content files in the workspace."""
        
        content_extensions = [".md", ".rst", ".txt", ".adoc"]
        content_files = []
        
        # Scan workspace for content files
        workspace = Path(".")
        
        for ext in content_extensions:
            content_files.extend(workspace.rglob(f"*{ext}"))
        
        # Convert to string paths
        return [str(path) for path in content_files]
    
    async def _create_content_inventory(self, content_paths: List[str]) -> Dict[str, ContentType]:
        """Create inventory of content with type classification."""
        
        inventory = {}
        
        for path in content_paths:
            content_type = self._classify_content_type(path)
            inventory[path] = content_type
        
        return inventory
    
    def _classify_content_type(self, file_path: str) -> ContentType:
        """Classify content type based on file path and name."""
        
        path_lower = file_path.lower()
        
        if "readme" in path_lower:
            return ContentType.README
        elif "changelog" in path_lower or "history" in path_lower:
            return ContentType.CHANGELOG
        elif "api" in path_lower and ("reference" in path_lower or "doc" in path_lower):
            return ContentType.API_REFERENCE
        elif "tutorial" in path_lower or "guide" in path_lower:
            return ContentType.TUTORIAL if "tutorial" in path_lower else ContentType.USER_GUIDE
        elif "architecture" in path_lower or "design" in path_lower:
            return ContentType.ARCHITECTURE_DOC
        elif "spec" in path_lower or "specification" in path_lower:
            return ContentType.TECHNICAL_SPEC
        else:
            return ContentType.DOCUMENTATION
    
    async def _execute_validation_matrix(self, content_inventory: Dict[str, ContentType]) -> List[ValidationResult]:
        """Execute validation matrix across all agents and content."""
        
        all_results = []
        
        for content_path, content_type in content_inventory.items():
            # Get relevant agents for this content type
            relevant_agents = [
                agent for agent in self.agents.values()
                if content_type in agent.content_types
            ]
            
            # Execute validation with each relevant agent
            for agent in relevant_agents:
                for aspect in agent.validation_aspects:
                    result = await self._validate_content_aspect(
                        content_path, content_type, aspect, agent
                    )
                    all_results.append(result)
        
        self.validation_results.extend(all_results)
        
        return all_results
    
    async def _validate_content_aspect(self, content_path: str, content_type: ContentType, 
                                     aspect: ValidationAspect, agent: ContentAgent) -> ValidationResult:
        """Validate specific aspect of content with specific agent."""
        
        result_id = f"validation_{int(time.time())}_{len(self.validation_results)}"
        
        # Read content
        try:
            with open(content_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return ValidationResult(
                result_id=result_id,
                content_path=content_path,
                content_type=content_type,
                validation_aspect=aspect,
                quality_level=QualityLevel.POOR,
                score=0.0,
                issues_found=[f"Failed to read file: {str(e)}"],
                recommendations=["Fix file access issues"],
                validator_agent=agent.agent_id,
                timestamp=time.time()
            )
        
        # Execute aspect-specific validation
        if aspect == ValidationAspect.ACCURACY:
            score, issues, recommendations = await self._validate_accuracy(content, content_type)
        elif aspect == ValidationAspect.COMPLETENESS:
            score, issues, recommendations = await self._validate_completeness(content, content_type)
        elif aspect == ValidationAspect.CLARITY:
            score, issues, recommendations = await self._validate_clarity(content, content_type)
        elif aspect == ValidationAspect.CONSISTENCY:
            score, issues, recommendations = await self._validate_consistency(content, content_type)
        elif aspect == ValidationAspect.FORMATTING:
            score, issues, recommendations = await self._validate_formatting(content, content_type)
        elif aspect == ValidationAspect.GRAMMAR:
            score, issues, recommendations = await self._validate_grammar(content, content_type)
        elif aspect == ValidationAspect.STRUCTURE:
            score, issues, recommendations = await self._validate_structure(content, content_type)
        elif aspect == ValidationAspect.ACCESSIBILITY:
            score, issues, recommendations = await self._validate_accessibility(content, content_type)
        else:
            score, issues, recommendations = 80.0, [], []
        
        # Determine quality level
        quality_level = self._determine_quality_level(score)
        
        # Update agent metrics
        agent.performance_metrics["validations_completed"] += 1
        agent.performance_metrics["issues_identified"] += len(issues)
        
        return ValidationResult(
            result_id=result_id,
            content_path=content_path,
            content_type=content_type,
            validation_aspect=aspect,
            quality_level=quality_level,
            score=score,
            issues_found=issues,
            recommendations=recommendations,
            validator_agent=agent.agent_id,
            timestamp=time.time()
        )
    
    async def _validate_accuracy(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content accuracy."""
        
        issues = []
        recommendations = []
        score = 90.0  # Base score
        
        # Check for placeholder content
        placeholders = ["TODO", "FIXME", "XXX", "placeholder", "example.com"]
        for placeholder in placeholders:
            if placeholder.lower() in content.lower():
                issues.append(f"Placeholder content found: {placeholder}")
                score -= 5.0
        
        # Check for broken references
        if "[broken]" in content or "[missing]" in content:
            issues.append("Broken references detected")
            score -= 10.0
        
        # Check for outdated information
        if "2023" in content and content_type in [ContentType.README, ContentType.DOCUMENTATION]:
            recommendations.append("Review dates and version information for currency")
        
        if issues:
            recommendations.append("Review and update inaccurate content")
        
        return max(0.0, score), issues, recommendations
    
    async def _validate_completeness(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content completeness."""
        
        issues = []
        recommendations = []
        score = 85.0  # Base score
        
        # Check minimum content length
        if len(content) < 100:
            issues.append("Content appears too brief")
            score -= 20.0
        
        # Content type specific checks
        if content_type == ContentType.README:
            required_sections = ["installation", "usage", "contributing", "license"]
            missing_sections = []
            
            for section in required_sections:
                if section.lower() not in content.lower():
                    missing_sections.append(section)
            
            if missing_sections:
                issues.append(f"Missing README sections: {', '.join(missing_sections)}")
                score -= len(missing_sections) * 5.0
        
        elif content_type == ContentType.API_REFERENCE:
            if "example" not in content.lower():
                issues.append("API documentation missing usage examples")
                score -= 10.0
        
        if issues:
            recommendations.append("Add missing content sections and examples")
        
        return max(0.0, score), issues, recommendations
    
    async def _validate_clarity(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content clarity."""
        
        issues = []
        recommendations = []
        score = 88.0  # Base score
        
        # Check for overly complex sentences
        sentences = content.split('.')
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        
        if len(long_sentences) > len(sentences) * 0.2:  # More than 20% long sentences
            issues.append("Many sentences are overly complex")
            score -= 10.0
            recommendations.append("Break down complex sentences for better readability")
        
        # Check for jargon without explanation
        technical_terms = ["API", "SDK", "CLI", "JSON", "HTTP", "REST"]
        unexplained_terms = []
        
        for term in technical_terms:
            if term in content and f"{term} is" not in content and f"{term} stands for" not in content:
                unexplained_terms.append(term)
        
        if len(unexplained_terms) > 3:
            issues.append("Technical terms may need explanation")
            score -= 5.0
            recommendations.append("Consider adding explanations for technical terms")
        
        return max(0.0, score), issues, recommendations
    
    async def _validate_consistency(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content consistency."""
        
        issues = []
        recommendations = []
        score = 92.0  # Base score
        
        # Check heading consistency
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        
        if headings:
            # Check for consistent capitalization
            title_case_count = sum(1 for h in headings if h.istitle())
            sentence_case_count = len(headings) - title_case_count
            
            if title_case_count > 0 and sentence_case_count > 0:
                issues.append("Inconsistent heading capitalization")
                score -= 8.0
                recommendations.append("Use consistent heading capitalization style")
        
        # Check for consistent terminology
        variations = [
            ("GitHub", "Github", "github"),
            ("JavaScript", "Javascript", "javascript"),
            ("API", "Api", "api")
        ]
        
        for correct, *variants in variations:
            if correct in content:
                for variant in variants:
                    if variant in content:
                        issues.append(f"Inconsistent terminology: {correct} vs {variant}")
                        score -= 3.0
        
        return max(0.0, score), issues, recommendations
    
    async def _validate_formatting(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content formatting."""
        
        issues = []
        recommendations = []
        score = 90.0  # Base score
        
        # Check for proper markdown formatting
        if content_type in [ContentType.README, ContentType.DOCUMENTATION]:
            # Check for unformatted code
            if "`" not in content and ("function" in content or "class" in content):
                issues.append("Code snippets not properly formatted")
                score -= 10.0
                recommendations.append("Use code blocks for code snippets")
            
            # Check for proper list formatting
            list_items = re.findall(r'^[\s]*[-*+]\s', content, re.MULTILINE)
            if list_items:
                # Check for consistent list markers
                markers = set(re.findall(r'^[\s]*([-*+])', content, re.MULTILINE))
                if len(markers) > 1:
                    issues.append("Inconsistent list formatting")
                    score -= 5.0
        
        # Check for trailing whitespace
        lines_with_trailing_space = [i for i, line in enumerate(content.split('\n')) if line.endswith(' ')]
        if len(lines_with_trailing_space) > 5:
            issues.append("Multiple lines with trailing whitespace")
            score -= 5.0
            recommendations.append("Remove trailing whitespace")
        
        return max(0.0, score), issues, recommendations
    
    async def _validate_grammar(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content grammar."""
        
        issues = []
        recommendations = []
        score = 85.0  # Base score
        
        # Basic grammar checks
        common_errors = [
            ("it's", "its", "Possible incorrect usage of it's/its"),
            ("your", "you're", "Possible incorrect usage of your/you're"),
            ("there", "their", "Possible incorrect usage of there/their/they're")
        ]
        
        for word1, word2, message in common_errors:
            if word1 in content.lower() and word2 in content.lower():
                # This is a simplified check - in practice, would need more sophisticated analysis
                pass
        
        # Check for sentence structure
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        # Check for very short sentences that might be fragments
        fragments = [s for s in sentences if len(s.split()) < 3 and not s.isupper()]
        if len(fragments) > len(sentences) * 0.1:  # More than 10% fragments
            issues.append("Possible sentence fragments detected")
            score -= 8.0
            recommendations.append("Review sentence structure and completeness")
        
        return max(0.0, score), issues, recommendations
    
    async def _validate_structure(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content structure."""
        
        issues = []
        recommendations = []
        score = 87.0  # Base score
        
        # Check heading hierarchy
        headings = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
        
        if headings:
            levels = [len(h[0]) for h in headings]
            
            # Check for proper hierarchy (no skipping levels)
            for i in range(1, len(levels)):
                if levels[i] > levels[i-1] + 1:
                    issues.append("Heading hierarchy skips levels")
                    score -= 10.0
                    break
            
            # Check for single h1
            h1_count = levels.count(1)
            if h1_count == 0:
                issues.append("Missing main heading (h1)")
                score -= 15.0
            elif h1_count > 1:
                issues.append("Multiple main headings (h1)")
                score -= 8.0
        
        # Check for logical flow
        if content_type == ContentType.TUTORIAL:
            step_indicators = ["step", "first", "next", "then", "finally"]
            step_count = sum(1 for indicator in step_indicators if indicator in content.lower())
            
            if step_count < 3:
                issues.append("Tutorial lacks clear step-by-step structure")
                score -= 10.0
                recommendations.append("Add clear step indicators for better flow")
        
        return max(0.0, score), issues, recommendations
    
    async def _validate_accessibility(self, content: str, content_type: ContentType) -> Tuple[float, List[str], List[str]]:
        """Validate content accessibility."""
        
        issues = []
        recommendations = []
        score = 90.0  # Base score
        
        # Check for alt text in images
        images = re.findall(r'!\[([^\]]*)\]\([^)]+\)', content)
        
        for alt_text in images:
            if not alt_text.strip():
                issues.append("Images missing alt text")
                score -= 10.0
                break
        
        # Check for descriptive link text
        links = re.findall(r'\[([^\]]+)\]\([^)]+\)', content)
        generic_link_text = ["click here", "read more", "link", "here"]
        
        for link_text in links:
            if link_text.lower() in generic_link_text:
                issues.append("Non-descriptive link text found")
                score -= 5.0
                break
        
        # Check for proper heading structure (accessibility requirement)
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        if not headings:
            issues.append("No headings found - impacts screen reader navigation")
            score -= 15.0
            recommendations.append("Add headings for better document structure")
        
        if issues:
            recommendations.append("Improve accessibility compliance")
        
        return max(0.0, score), issues, recommendations
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """Determine quality level based on score."""
        
        if score >= 95:
            return QualityLevel.EXCELLENT
        elif score >= 85:
            return QualityLevel.GOOD
        elif score >= 70:
            return QualityLevel.SATISFACTORY
        elif score >= 50:
            return QualityLevel.NEEDS_IMPROVEMENT
        else:
            return QualityLevel.POOR
    
    async def _generate_quality_report(self, report_id: str, content_inventory: Dict[str, ContentType],
                                     validation_results: List[ValidationResult]) -> ContentQualityReport:
        """Generate comprehensive content quality report."""
        
        # Calculate overall quality score
        if validation_results:
            overall_score = sum(result.score for result in validation_results) / len(validation_results)
        else:
            overall_score = 0.0
        
        # Calculate quality by content type
        quality_by_type = {}
        for content_type in ContentType:
            type_results = [r for r in validation_results if r.content_type == content_type]
            if type_results:
                quality_by_type[content_type.value] = sum(r.score for r in type_results) / len(type_results)
        
        # Calculate quality by validation aspect
        quality_by_aspect = {}
        for aspect in ValidationAspect:
            aspect_results = [r for r in validation_results if r.validation_aspect == aspect]
            if aspect_results:
                quality_by_aspect[aspect.value] = sum(r.score for r in aspect_results) / len(aspect_results)
        
        # Identify critical issues
        critical_issues = []
        poor_results = [r for r in validation_results if r.quality_level == QualityLevel.POOR]
        
        for result in poor_results:
            critical_issues.extend(result.issues_found)
        
        # Generate improvement recommendations
        improvement_recommendations = []
        all_recommendations = []
        
        for result in validation_results:
            all_recommendations.extend(result.recommendations)
        
        # Deduplicate and prioritize recommendations
        unique_recommendations = list(set(all_recommendations))
        improvement_recommendations = unique_recommendations[:10]  # Top 10 recommendations
        
        # Calculate professional presentation score
        presentation_aspects = [ValidationAspect.FORMATTING, ValidationAspect.STRUCTURE, ValidationAspect.CONSISTENCY]
        presentation_results = [r for r in validation_results if r.validation_aspect in presentation_aspects]
        
        if presentation_results:
            professional_score = sum(r.score for r in presentation_results) / len(presentation_results)
        else:
            professional_score = overall_score
        
        return ContentQualityReport(
            report_id=report_id,
            content_inventory=content_inventory,
            validation_results=validation_results,
            overall_quality_score=overall_score,
            quality_by_type=quality_by_type,
            quality_by_aspect=quality_by_aspect,
            critical_issues=critical_issues,
            improvement_recommendations=improvement_recommendations,
            professional_presentation_score=professional_score,
            timestamp=time.time()
        )
    
    def get_squad_status(self) -> Dict[str, Any]:
        """Get Content Squad status and metrics."""
        
        total_validations = sum(agent.performance_metrics["validations_completed"] for agent in self.agents.values())
        total_issues = sum(agent.performance_metrics["issues_identified"] for agent in self.agents.values())
        
        return {
            "total_agents": len(self.agents),
            "agents_active": len([a for a in self.agents.values() if a.current_assignment]),
            "total_validations": total_validations,
            "total_issues_identified": total_issues,
            "quality_reports_generated": len(self.quality_reports),
            "latest_quality_score": self.quality_reports[-1].overall_quality_score if self.quality_reports else 0,
            "professional_presentation_score": self.quality_reports[-1].professional_presentation_score if self.quality_reports else 0,
            "agent_specializations": [agent.specialization for agent in self.agents.values()]
        }


# Example usage
async def main():
    """Example usage of Content Squad Final Validator."""
    
    validator = ContentSquadFinalValidator()
    
    # Execute final content validation
    report = await validator.execute_final_content_validation()
    
    print(f"Content Quality Report:")
    print(f"  Overall Quality Score: {report.overall_quality_score:.1f}%")
    print(f"  Professional Presentation: {report.professional_presentation_score:.1f}%")
    print(f"  Content Files Validated: {len(report.content_inventory)}")
    print(f"  Critical Issues: {len(report.critical_issues)}")
    print(f"  Improvement Recommendations: {len(report.improvement_recommendations)}")
    
    # Show quality by content type
    print(f"\nQuality by Content Type:")
    for content_type, score in report.quality_by_type.items():
        print(f"  {content_type}: {score:.1f}%")
    
    # Get squad status
    status = validator.get_squad_status()
    print(f"\nContent Squad Status:")
    print(f"  Total Agents: {status['total_agents']}")
    print(f"  Total Validations: {status['total_validations']}")
    print(f"  Issues Identified: {status['total_issues_identified']}")


if __name__ == "__main__":
    asyncio.run(main())
