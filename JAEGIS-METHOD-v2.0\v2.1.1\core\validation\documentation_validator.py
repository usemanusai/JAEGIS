"""
Documentation Format Validation System
Verify all documentation files meet GitHub standards and maintain professional presentation
"""

import asyncio
import re
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import markdown
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ValidationLevel(str, Enum):
    """Documentation validation levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    GITHUB_COMPLIANT = "github_compliant"


class IssueType(str, Enum):
    """Types of documentation issues."""
    FORMAT_ERROR = "format_error"
    STYLE_VIOLATION = "style_violation"
    BROKEN_LINK = "broken_link"
    MISSING_CONTENT = "missing_content"
    ACCESSIBILITY_ISSUE = "accessibility_issue"
    SEO_ISSUE = "seo_issue"


class Severity(str, Enum):
    """Issue severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Documentation validation issue."""
    issue_id: str
    issue_type: IssueType
    severity: Severity
    file_path: str
    line_number: Optional[int]
    description: str
    suggestion: str
    auto_fixable: bool


@dataclass
class ValidationReport:
    """Documentation validation report."""
    report_id: str
    file_path: str
    validation_level: ValidationLevel
    total_issues: int
    issues_by_severity: Dict[str, int]
    issues_found: List[ValidationIssue]
    validation_score: float
    github_compliant: bool
    timestamp: float


class DocumentationValidator:
    """
    Documentation Format Validation System
    
    Provides comprehensive documentation validation including:
    - GitHub Markdown standards compliance
    - Professional formatting verification
    - Link validation and accessibility
    - SEO optimization checks
    - Style consistency validation
    """
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.GITHUB_COMPLIANT):
        self.validation_level = validation_level
        self.validation_reports: List[ValidationReport] = []
        
        # Validation rules
        self.validation_rules = self._initialize_validation_rules()
        
        # GitHub standards
        self.github_standards = self._initialize_github_standards()
        
        logger.info(f"Documentation Validator initialized with {validation_level.value} level")
    
    def _initialize_validation_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize documentation validation rules."""
        
        return {
            "markdown_format": [
                {
                    "name": "Header Hierarchy",
                    "pattern": r"^#{7,}",
                    "severity": Severity.ERROR,
                    "description": "Headers should not exceed 6 levels (######)",
                    "suggestion": "Use maximum 6 header levels"
                },
                {
                    "name": "Missing Space After Hash",
                    "pattern": r"^#+[^#\s]",
                    "severity": Severity.WARNING,
                    "description": "Headers should have space after hash symbols",
                    "suggestion": "Add space after # symbols"
                },
                {
                    "name": "Trailing Whitespace",
                    "pattern": r"\s+$",
                    "severity": Severity.WARNING,
                    "description": "Lines should not have trailing whitespace",
                    "suggestion": "Remove trailing whitespace"
                },
                {
                    "name": "Multiple Blank Lines",
                    "pattern": r"\n\n\n+",
                    "severity": Severity.INFO,
                    "description": "Avoid multiple consecutive blank lines",
                    "suggestion": "Use single blank line for separation"
                }
            ],
            
            "link_validation": [
                {
                    "name": "Broken Internal Link",
                    "pattern": r"\[([^\]]+)\]\(([^)]+)\)",
                    "severity": Severity.ERROR,
                    "description": "Internal link may be broken",
                    "suggestion": "Verify link target exists"
                },
                {
                    "name": "Missing Alt Text",
                    "pattern": r"!\[\]\([^)]+\)",
                    "severity": Severity.WARNING,
                    "description": "Images should have alt text for accessibility",
                    "suggestion": "Add descriptive alt text"
                }
            ],
            
            "content_structure": [
                {
                    "name": "Missing Main Header",
                    "pattern": r"^(?!#\s)",
                    "severity": Severity.ERROR,
                    "description": "Document should start with main header (# Title)",
                    "suggestion": "Add main header at document start"
                },
                {
                    "name": "Empty Code Block",
                    "pattern": r"```\s*\n\s*```",
                    "severity": Severity.WARNING,
                    "description": "Code blocks should not be empty",
                    "suggestion": "Add code content or remove block"
                }
            ],
            
            "github_specific": [
                {
                    "name": "Table of Contents",
                    "pattern": r"(?i)table\s+of\s+contents|toc",
                    "severity": Severity.INFO,
                    "description": "Consider adding table of contents for long documents",
                    "suggestion": "Add TOC for documents > 500 lines"
                },
                {
                    "name": "Badge Format",
                    "pattern": r"!\[([^\]]*)\]\(https://img\.shields\.io/[^)]+\)",
                    "severity": Severity.INFO,
                    "description": "Shields.io badges detected",
                    "suggestion": "Ensure badges are relevant and up-to-date"
                }
            ]
        }
    
    def _initialize_github_standards(self) -> Dict[str, Any]:
        """Initialize GitHub documentation standards."""
        
        return {
            "required_files": [
                "README.md",
                "LICENSE",
                "CONTRIBUTING.md",
                "CHANGELOG.md"
            ],
            
            "readme_sections": [
                "title",
                "description",
                "installation",
                "usage",
                "contributing",
                "license"
            ],
            
            "markdown_extensions": [
                ".md",
                ".markdown",
                ".mdown",
                ".mkdn"
            ],
            
            "max_line_length": 120,
            "max_file_size_kb": 1024,
            
            "accessibility_requirements": {
                "alt_text_required": True,
                "heading_structure": True,
                "link_descriptions": True
            },
            
            "seo_requirements": {
                "meta_description": True,
                "keywords": True,
                "structured_headings": True
            }
        }
    
    async def validate_documentation(self, file_paths: List[str]) -> Dict[str, ValidationReport]:
        """Validate multiple documentation files."""
        
        logger.info(f"Validating {len(file_paths)} documentation files")
        
        validation_results = {}
        
        for file_path in file_paths:
            try:
                report = await self._validate_single_file(file_path)
                validation_results[file_path] = report
                
                logger.info(f"Validated {file_path}: {report.total_issues} issues, score {report.validation_score:.1f}")
                
            except Exception as e:
                logger.error(f"Validation failed for {file_path}: {e}")
                
                # Create error report
                validation_results[file_path] = ValidationReport(
                    report_id=f"report_{int(time.time())}",
                    file_path=file_path,
                    validation_level=self.validation_level,
                    total_issues=1,
                    issues_by_severity={"critical": 1},
                    issues_found=[ValidationIssue(
                        issue_id=f"issue_{int(time.time())}",
                        issue_type=IssueType.FORMAT_ERROR,
                        severity=Severity.CRITICAL,
                        file_path=file_path,
                        line_number=None,
                        description=f"Validation error: {str(e)}",
                        suggestion="Fix file format or encoding issues",
                        auto_fixable=False
                    )],
                    validation_score=0.0,
                    github_compliant=False,
                    timestamp=time.time()
                )
        
        # Store validation reports
        self.validation_reports.extend(validation_results.values())
        
        logger.info(f"Documentation validation completed: {len(validation_results)} files processed")
        
        return validation_results
    
    async def _validate_single_file(self, file_path: str) -> ValidationReport:
        """Validate single documentation file."""
        
        report_id = f"report_{int(time.time())}"
        issues_found = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Basic file checks
            issues_found.extend(await self._validate_file_basics(file_path, content))
            
            # Markdown format validation
            if Path(file_path).suffix.lower() in self.github_standards["markdown_extensions"]:
                issues_found.extend(await self._validate_markdown_format(file_path, lines))
                issues_found.extend(await self._validate_content_structure(file_path, content))
                issues_found.extend(await self._validate_links(file_path, content))
                issues_found.extend(await self._validate_accessibility(file_path, content))
                
                # GitHub-specific validation
                if self.validation_level == ValidationLevel.GITHUB_COMPLIANT:
                    issues_found.extend(await self._validate_github_standards(file_path, content))
            
            # Calculate validation score
            validation_score = self._calculate_validation_score(issues_found, len(lines))
            
            # Count issues by severity
            issues_by_severity = {}
            for severity in Severity:
                issues_by_severity[severity.value] = len([i for i in issues_found if i.severity == severity])
            
            # Determine GitHub compliance
            github_compliant = (
                validation_score >= 80.0 and
                issues_by_severity.get("critical", 0) == 0 and
                issues_by_severity.get("error", 0) <= 2
            )
            
            return ValidationReport(
                report_id=report_id,
                file_path=file_path,
                validation_level=self.validation_level,
                total_issues=len(issues_found),
                issues_by_severity=issues_by_severity,
                issues_found=issues_found,
                validation_score=validation_score,
                github_compliant=github_compliant,
                timestamp=time.time()
            )
        
        except Exception as e:
            logger.error(f"File validation error for {file_path}: {e}")
            raise
    
    async def _validate_file_basics(self, file_path: str, content: str) -> List[ValidationIssue]:
        """Validate basic file properties."""
        
        issues = []
        
        # Check file size
        file_size_kb = len(content.encode('utf-8')) / 1024
        
        if file_size_kb > self.github_standards["max_file_size_kb"]:
            issues.append(ValidationIssue(
                issue_id=f"issue_{int(time.time())}",
                issue_type=IssueType.FORMAT_ERROR,
                severity=Severity.WARNING,
                file_path=file_path,
                line_number=None,
                description=f"File size ({file_size_kb:.1f} KB) exceeds recommended limit",
                suggestion=f"Consider splitting file or reducing content",
                auto_fixable=False
            ))
        
        # Check encoding
        try:
            content.encode('utf-8')
        except UnicodeEncodeError:
            issues.append(ValidationIssue(
                issue_id=f"issue_{int(time.time())}",
                issue_type=IssueType.FORMAT_ERROR,
                severity=Severity.ERROR,
                file_path=file_path,
                line_number=None,
                description="File contains non-UTF-8 characters",
                suggestion="Convert file to UTF-8 encoding",
                auto_fixable=True
            ))
        
        return issues
    
    async def _validate_markdown_format(self, file_path: str, lines: List[str]) -> List[ValidationIssue]:
        """Validate Markdown formatting."""
        
        issues = []
        
        for category, rules in self.validation_rules.items():
            if category == "markdown_format":
                for rule in rules:
                    pattern = rule["pattern"]
                    
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            issues.append(ValidationIssue(
                                issue_id=f"issue_{int(time.time())}_{line_num}",
                                issue_type=IssueType.FORMAT_ERROR,
                                severity=rule["severity"],
                                file_path=file_path,
                                line_number=line_num,
                                description=rule["description"],
                                suggestion=rule["suggestion"],
                                auto_fixable=rule["severity"] in [Severity.INFO, Severity.WARNING]
                            ))
        
        return issues
    
    async def _validate_content_structure(self, file_path: str, content: str) -> List[ValidationIssue]:
        """Validate content structure and organization."""
        
        issues = []
        lines = content.split('\n')
        
        # Check for main header
        if lines and not lines[0].startswith('# '):
            issues.append(ValidationIssue(
                issue_id=f"issue_{int(time.time())}",
                issue_type=IssueType.MISSING_CONTENT,
                severity=Severity.ERROR,
                file_path=file_path,
                line_number=1,
                description="Document should start with main header (# Title)",
                suggestion="Add main header at document start",
                auto_fixable=False
            ))
        
        # Check header hierarchy
        header_levels = []
        for line_num, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                header_levels.append((line_num, level))
        
        # Validate header progression
        for i in range(1, len(header_levels)):
            prev_level = header_levels[i-1][1]
            curr_level = header_levels[i][1]
            curr_line = header_levels[i][0]
            
            if curr_level > prev_level + 1:
                issues.append(ValidationIssue(
                    issue_id=f"issue_{int(time.time())}_{curr_line}",
                    issue_type=IssueType.STYLE_VIOLATION,
                    severity=Severity.WARNING,
                    file_path=file_path,
                    line_number=curr_line,
                    description="Header level skips intermediate levels",
                    suggestion="Use sequential header levels (h1 -> h2 -> h3)",
                    auto_fixable=True
                ))
        
        return issues
    
    async def _validate_links(self, file_path: str, content: str) -> List[ValidationIssue]:
        """Validate links and references."""
        
        issues = []
        
        # Find all markdown links
        link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        links = re.finditer(link_pattern, content)
        
        for match in links:
            link_text = match.group(1)
            link_url = match.group(2)
            
            # Check for empty link text
            if not link_text.strip():
                issues.append(ValidationIssue(
                    issue_id=f"issue_{int(time.time())}",
                    issue_type=IssueType.ACCESSIBILITY_ISSUE,
                    severity=Severity.WARNING,
                    file_path=file_path,
                    line_number=None,
                    description="Link has empty or missing text",
                    suggestion="Add descriptive link text",
                    auto_fixable=False
                ))
            
            # Check internal links
            if not link_url.startswith(('http://', 'https://', 'mailto:')):
                # Internal link - check if file exists
                link_path = Path(file_path).parent / link_url
                if not link_path.exists():
                    issues.append(ValidationIssue(
                        issue_id=f"issue_{int(time.time())}",
                        issue_type=IssueType.BROKEN_LINK,
                        severity=Severity.ERROR,
                        file_path=file_path,
                        line_number=None,
                        description=f"Internal link target not found: {link_url}",
                        suggestion="Verify link target exists or update path",
                        auto_fixable=False
                    ))
        
        # Find all image references
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.finditer(image_pattern, content)
        
        for match in images:
            alt_text = match.group(1)
            image_url = match.group(2)
            
            # Check for missing alt text
            if not alt_text.strip():
                issues.append(ValidationIssue(
                    issue_id=f"issue_{int(time.time())}",
                    issue_type=IssueType.ACCESSIBILITY_ISSUE,
                    severity=Severity.WARNING,
                    file_path=file_path,
                    line_number=None,
                    description="Image missing alt text for accessibility",
                    suggestion="Add descriptive alt text",
                    auto_fixable=False
                ))
        
        return issues
    
    async def _validate_accessibility(self, file_path: str, content: str) -> List[ValidationIssue]:
        """Validate accessibility compliance."""
        
        issues = []
        
        # Check for proper heading structure
        lines = content.split('\n')
        headings = []
        
        for line_num, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                headings.append((line_num, level, line.strip()))
        
        # Ensure h1 exists
        h1_count = len([h for h in headings if h[1] == 1])
        if h1_count == 0:
            issues.append(ValidationIssue(
                issue_id=f"issue_{int(time.time())}",
                issue_type=IssueType.ACCESSIBILITY_ISSUE,
                severity=Severity.ERROR,
                file_path=file_path,
                line_number=None,
                description="Document missing main heading (h1)",
                suggestion="Add main heading for document structure",
                auto_fixable=False
            ))
        elif h1_count > 1:
            issues.append(ValidationIssue(
                issue_id=f"issue_{int(time.time())}",
                issue_type=IssueType.ACCESSIBILITY_ISSUE,
                severity=Severity.WARNING,
                file_path=file_path,
                line_number=None,
                description="Multiple h1 headings found",
                suggestion="Use only one h1 heading per document",
                auto_fixable=True
            ))
        
        return issues
    
    async def _validate_github_standards(self, file_path: str, content: str) -> List[ValidationIssue]:
        """Validate GitHub-specific standards."""
        
        issues = []
        
        # Check README.md specific requirements
        if Path(file_path).name.lower() == 'readme.md':
            issues.extend(await self._validate_readme_structure(file_path, content))
        
        # Check for GitHub-flavored markdown features
        if '```' in content:
            # Check code block language specification
            code_blocks = re.finditer(r'```(\w*)\n', content)
            for match in code_blocks:
                language = match.group(1)
                if not language:
                    issues.append(ValidationIssue(
                        issue_id=f"issue_{int(time.time())}",
                        issue_type=IssueType.STYLE_VIOLATION,
                        severity=Severity.INFO,
                        file_path=file_path,
                        line_number=None,
                        description="Code block missing language specification",
                        suggestion="Specify language for syntax highlighting",
                        auto_fixable=True
                    ))
        
        return issues
    
    async def _validate_readme_structure(self, file_path: str, content: str) -> List[ValidationIssue]:
        """Validate README.md structure."""
        
        issues = []
        content_lower = content.lower()
        
        required_sections = self.github_standards["readme_sections"]
        
        for section in required_sections:
            if section not in content_lower:
                issues.append(ValidationIssue(
                    issue_id=f"issue_{int(time.time())}",
                    issue_type=IssueType.MISSING_CONTENT,
                    severity=Severity.WARNING,
                    file_path=file_path,
                    line_number=None,
                    description=f"README missing recommended section: {section}",
                    suggestion=f"Add {section} section to README",
                    auto_fixable=False
                ))
        
        return issues
    
    def _calculate_validation_score(self, issues: List[ValidationIssue], line_count: int) -> float:
        """Calculate validation score based on issues found."""
        
        if not issues:
            return 100.0
        
        # Weight issues by severity
        severity_weights = {
            Severity.CRITICAL: 20,
            Severity.ERROR: 10,
            Severity.WARNING: 5,
            Severity.INFO: 1
        }
        
        total_penalty = sum(severity_weights.get(issue.severity, 1) for issue in issues)
        
        # Base score calculation
        base_score = max(0, 100 - (total_penalty / max(1, line_count / 10)))
        
        return min(100.0, base_score)
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get comprehensive validation summary."""
        
        if not self.validation_reports:
            return {"error": "No validation reports available"}
        
        total_files = len(self.validation_reports)
        total_issues = sum(report.total_issues for report in self.validation_reports)
        
        # Average score
        avg_score = sum(report.validation_score for report in self.validation_reports) / total_files
        
        # GitHub compliance rate
        compliant_files = len([r for r in self.validation_reports if r.github_compliant])
        compliance_rate = (compliant_files / total_files) * 100
        
        # Issues by type
        issues_by_type = {}
        for report in self.validation_reports:
            for issue in report.issues_found:
                issue_type = issue.issue_type.value
                issues_by_type[issue_type] = issues_by_type.get(issue_type, 0) + 1
        
        # Issues by severity
        issues_by_severity = {}
        for report in self.validation_reports:
            for severity, count in report.issues_by_severity.items():
                issues_by_severity[severity] = issues_by_severity.get(severity, 0) + count
        
        return {
            "total_files_validated": total_files,
            "total_issues_found": total_issues,
            "average_validation_score": avg_score,
            "github_compliance_rate": compliance_rate,
            "compliant_files": compliant_files,
            "issues_by_type": issues_by_type,
            "issues_by_severity": issues_by_severity,
            "validation_level": self.validation_level.value
        }


# Example usage
async def main():
    """Example usage of Documentation Validator."""
    
    validator = DocumentationValidator(ValidationLevel.GITHUB_COMPLIANT)
    
    # Simulate documentation files
    test_files = [
        "README.md",
        "CONTRIBUTING.md",
        "docs/api.md"
    ]
    
    # Validate documentation
    results = await validator.validate_documentation(test_files)
    
    print(f"Documentation Validation Results:")
    for file_path, report in results.items():
        print(f"  {file_path}:")
        print(f"    Score: {report.validation_score:.1f}/100")
        print(f"    Issues: {report.total_issues}")
        print(f"    GitHub Compliant: {report.github_compliant}")
        
        if report.issues_found:
            print(f"    Top Issues:")
            for issue in report.issues_found[:3]:  # Show first 3
                print(f"      - {issue.severity.value}: {issue.description}")
    
    # Get validation summary
    summary = validator.get_validation_summary()
    print(f"\nValidation Summary:")
    print(f"  Files Validated: {summary['total_files_validated']}")
    print(f"  Average Score: {summary['average_validation_score']:.1f}")
    print(f"  GitHub Compliance: {summary['github_compliance_rate']:.1f}%")
    print(f"  Total Issues: {summary['total_issues_found']}")


if __name__ == "__main__":
    asyncio.run(main())
