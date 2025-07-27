"""
GARAS Gap Detection & Pattern Recognition System
Real-time monitoring and pattern recognition to identify documentation gaps,
missing content, and improvement opportunities
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import re
from pathlib import Path
import hashlib
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)


class GapType(str, Enum):
    """Types of gaps that can be detected."""
    MISSING_DOCUMENTATION = "missing_documentation"
    INCOMPLETE_CONTENT = "incomplete_content"
    OUTDATED_INFORMATION = "outdated_information"
    BROKEN_LINKS = "broken_links"
    INCONSISTENT_FORMAT = "inconsistent_format"
    MISSING_EXAMPLES = "missing_examples"
    UNCLEAR_INSTRUCTIONS = "unclear_instructions"
    MISSING_DEPENDENCIES = "missing_dependencies"


class GapSeverity(str, Enum):
    """Severity levels for detected gaps."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ContentType(str, Enum):
    """Types of content being analyzed."""
    DOCUMENTATION = "documentation"
    CODE = "code"
    CONFIGURATION = "configuration"
    API_REFERENCE = "api_reference"
    TUTORIAL = "tutorial"
    README = "readme"


@dataclass
class DetectedGap:
    """Detected gap in content or documentation."""
    gap_id: str
    gap_type: GapType
    severity: GapSeverity
    content_type: ContentType
    file_path: str
    line_number: Optional[int]
    description: str
    evidence: List[str]
    suggested_fixes: List[str]
    confidence: float
    detected_at: float
    pattern_matched: str


@dataclass
class Pattern:
    """Pattern for gap detection."""
    pattern_id: str
    name: str
    description: str
    regex_pattern: str
    gap_type: GapType
    severity: GapSeverity
    confidence_weight: float
    applicable_content_types: List[ContentType]


@dataclass
class GapAnalysisResult:
    """Result of gap analysis."""
    analysis_id: str
    file_path: str
    content_type: ContentType
    gaps_detected: List[DetectedGap]
    total_gaps: int
    critical_gaps: int
    high_priority_gaps: int
    analysis_duration_ms: float
    confidence_score: float


class GapDetectionSystem:
    """
    GARAS Gap Detection & Pattern Recognition System
    
    Provides real-time monitoring and pattern recognition to identify:
    - Documentation gaps and missing content
    - Inconsistencies and formatting issues
    - Broken links and outdated information
    - Missing examples and unclear instructions
    """
    
    def __init__(self):
        self.patterns: Dict[str, Pattern] = {}
        self.detected_gaps: List[DetectedGap] = []
        self.analysis_results: List[GapAnalysisResult] = []
        
        # Configuration
        self.config = {
            "min_confidence_threshold": 0.7,
            "max_file_size": 10485760,  # 10MB
            "analysis_timeout": 30,     # seconds
            "pattern_cache_duration": 3600,  # 1 hour
            "real_time_monitoring": True,
            "batch_analysis_size": 100
        }
        
        # Initialize detection patterns
        self._initialize_detection_patterns()
        
        # Start real-time monitoring if enabled
        if self.config["real_time_monitoring"]:
            asyncio.create_task(self._real_time_monitor())
        
        logger.info("Gap Detection System initialized")
    
    def _initialize_detection_patterns(self):
        """Initialize gap detection patterns."""
        
        patterns = [
            # Missing documentation patterns
            {
                "pattern_id": "missing_function_docs",
                "name": "Missing Function Documentation",
                "description": "Functions without docstrings or comments",
                "regex_pattern": r"def\s+\w+\([^)]*\):\s*\n(?!\s*\"\"\"|\s*#)",
                "gap_type": GapType.MISSING_DOCUMENTATION,
                "severity": GapSeverity.MEDIUM,
                "confidence_weight": 0.9,
                "applicable_content_types": [ContentType.CODE]
            },
            
            {
                "pattern_id": "missing_class_docs",
                "name": "Missing Class Documentation",
                "description": "Classes without docstrings",
                "regex_pattern": r"class\s+\w+[^:]*:\s*\n(?!\s*\"\"\"|\s*#)",
                "gap_type": GapType.MISSING_DOCUMENTATION,
                "severity": GapSeverity.HIGH,
                "confidence_weight": 0.95,
                "applicable_content_types": [ContentType.CODE]
            },
            
            # Incomplete content patterns
            {
                "pattern_id": "todo_comments",
                "name": "TODO Comments",
                "description": "TODO comments indicating incomplete work",
                "regex_pattern": r"#\s*TODO|//\s*TODO|<!--\s*TODO",
                "gap_type": GapType.INCOMPLETE_CONTENT,
                "severity": GapSeverity.MEDIUM,
                "confidence_weight": 0.8,
                "applicable_content_types": [ContentType.CODE, ContentType.DOCUMENTATION]
            },
            
            {
                "pattern_id": "placeholder_text",
                "name": "Placeholder Text",
                "description": "Placeholder text that needs to be replaced",
                "regex_pattern": r"\[PLACEHOLDER\]|\[TBD\]|\[TODO\]|FIXME|XXX",
                "gap_type": GapType.INCOMPLETE_CONTENT,
                "severity": GapSeverity.HIGH,
                "confidence_weight": 0.9,
                "applicable_content_types": [ContentType.DOCUMENTATION, ContentType.README]
            },
            
            # Broken links patterns
            {
                "pattern_id": "broken_markdown_links",
                "name": "Potentially Broken Markdown Links",
                "description": "Markdown links that may be broken",
                "regex_pattern": r"\[([^\]]+)\]\(([^)]+)\)",
                "gap_type": GapType.BROKEN_LINKS,
                "severity": GapSeverity.MEDIUM,
                "confidence_weight": 0.6,
                "applicable_content_types": [ContentType.DOCUMENTATION, ContentType.README]
            },
            
            # Missing examples patterns
            {
                "pattern_id": "missing_code_examples",
                "name": "Missing Code Examples",
                "description": "API documentation without code examples",
                "regex_pattern": r"(function|method|endpoint).*?(?!```|example|sample)",
                "gap_type": GapType.MISSING_EXAMPLES,
                "severity": GapSeverity.MEDIUM,
                "confidence_weight": 0.7,
                "applicable_content_types": [ContentType.API_REFERENCE, ContentType.DOCUMENTATION]
            },
            
            # Inconsistent format patterns
            {
                "pattern_id": "inconsistent_headers",
                "name": "Inconsistent Header Formatting",
                "description": "Inconsistent markdown header formatting",
                "regex_pattern": r"^#{1,6}\s*[^#\n]*[^#\s]\s*#{1,6}\s*$",
                "gap_type": GapType.INCONSISTENT_FORMAT,
                "severity": GapSeverity.LOW,
                "confidence_weight": 0.8,
                "applicable_content_types": [ContentType.DOCUMENTATION, ContentType.README]
            },
            
            # Unclear instructions patterns
            {
                "pattern_id": "vague_instructions",
                "name": "Vague Instructions",
                "description": "Instructions that are too vague or unclear",
                "regex_pattern": r"\b(somehow|maybe|probably|might|could|should work)\b",
                "gap_type": GapType.UNCLEAR_INSTRUCTIONS,
                "severity": GapSeverity.MEDIUM,
                "confidence_weight": 0.6,
                "applicable_content_types": [ContentType.DOCUMENTATION, ContentType.TUTORIAL]
            },
            
            # Missing dependencies patterns
            {
                "pattern_id": "missing_imports",
                "name": "Missing Import Statements",
                "description": "Code using undefined variables or functions",
                "regex_pattern": r"^(?!import|from).*\b([A-Z][a-zA-Z0-9_]*)\(",
                "gap_type": GapType.MISSING_DEPENDENCIES,
                "severity": GapSeverity.HIGH,
                "confidence_weight": 0.7,
                "applicable_content_types": [ContentType.CODE]
            }
        ]
        
        # Create Pattern objects
        for pattern_config in patterns:
            pattern = Pattern(**pattern_config)
            self.patterns[pattern.pattern_id] = pattern
        
        logger.info(f"Initialized {len(self.patterns)} detection patterns")
    
    async def analyze_content(self, 
                            content: str,
                            file_path: str,
                            content_type: ContentType) -> GapAnalysisResult:
        """Analyze content for gaps and issues."""
        
        analysis_id = hashlib.md5(f"{file_path}{time.time()}".encode()).hexdigest()[:12]
        start_time = time.time()
        
        detected_gaps = []
        
        try:
            # Apply relevant patterns
            for pattern in self.patterns.values():
                if content_type in pattern.applicable_content_types:
                    gaps = await self._apply_pattern(pattern, content, file_path)
                    detected_gaps.extend(gaps)
            
            # Additional content-specific analysis
            if content_type == ContentType.README:
                readme_gaps = await self._analyze_readme_specific(content, file_path)
                detected_gaps.extend(readme_gaps)
            
            elif content_type == ContentType.API_REFERENCE:
                api_gaps = await self._analyze_api_specific(content, file_path)
                detected_gaps.extend(api_gaps)
            
            # Calculate statistics
            total_gaps = len(detected_gaps)
            critical_gaps = len([g for g in detected_gaps if g.severity == GapSeverity.CRITICAL])
            high_priority_gaps = len([g for g in detected_gaps if g.severity == GapSeverity.HIGH])
            
            # Calculate confidence score
            if detected_gaps:
                confidence_score = sum(gap.confidence for gap in detected_gaps) / len(detected_gaps)
            else:
                confidence_score = 1.0  # No gaps = high confidence
            
            analysis_duration = (time.time() - start_time) * 1000
            
            result = GapAnalysisResult(
                analysis_id=analysis_id,
                file_path=file_path,
                content_type=content_type,
                gaps_detected=detected_gaps,
                total_gaps=total_gaps,
                critical_gaps=critical_gaps,
                high_priority_gaps=high_priority_gaps,
                analysis_duration_ms=analysis_duration,
                confidence_score=confidence_score
            )
            
            # Store results
            self.analysis_results.append(result)
            self.detected_gaps.extend(detected_gaps)
            
            logger.info(f"Analysis completed for {file_path}: {total_gaps} gaps detected")
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed for {file_path}: {e}")
            
            return GapAnalysisResult(
                analysis_id=analysis_id,
                file_path=file_path,
                content_type=content_type,
                gaps_detected=[],
                total_gaps=0,
                critical_gaps=0,
                high_priority_gaps=0,
                analysis_duration_ms=(time.time() - start_time) * 1000,
                confidence_score=0.0
            )
    
    async def _apply_pattern(self, 
                           pattern: Pattern,
                           content: str,
                           file_path: str) -> List[DetectedGap]:
        """Apply a detection pattern to content."""
        
        gaps = []
        
        try:
            matches = re.finditer(pattern.regex_pattern, content, re.MULTILINE | re.IGNORECASE)
            
            for match in matches:
                # Calculate line number
                line_number = content[:match.start()].count('\n') + 1
                
                # Generate gap ID
                gap_id = hashlib.md5(f"{pattern.pattern_id}{file_path}{line_number}".encode()).hexdigest()[:12]
                
                # Extract evidence
                evidence = [match.group(0)]
                if match.groups():
                    evidence.extend(match.groups())
                
                # Generate suggested fixes based on pattern type
                suggested_fixes = self._generate_suggested_fixes(pattern.gap_type, match.group(0))
                
                gap = DetectedGap(
                    gap_id=gap_id,
                    gap_type=pattern.gap_type,
                    severity=pattern.severity,
                    content_type=ContentType.CODE,  # Will be overridden by caller
                    file_path=file_path,
                    line_number=line_number,
                    description=pattern.description,
                    evidence=evidence,
                    suggested_fixes=suggested_fixes,
                    confidence=pattern.confidence_weight,
                    detected_at=time.time(),
                    pattern_matched=pattern.pattern_id
                )
                
                gaps.append(gap)
        
        except Exception as e:
            logger.error(f"Pattern application failed for {pattern.pattern_id}: {e}")
        
        return gaps
    
    def _generate_suggested_fixes(self, gap_type: GapType, evidence: str) -> List[str]:
        """Generate suggested fixes based on gap type."""
        
        fixes = []
        
        if gap_type == GapType.MISSING_DOCUMENTATION:
            fixes = [
                "Add comprehensive docstring with description, parameters, and return value",
                "Include usage examples in the documentation",
                "Document any exceptions that may be raised"
            ]
        
        elif gap_type == GapType.INCOMPLETE_CONTENT:
            fixes = [
                "Complete the TODO item or remove if no longer needed",
                "Replace placeholder text with actual content",
                "Add implementation details or mark as future enhancement"
            ]
        
        elif gap_type == GapType.BROKEN_LINKS:
            fixes = [
                "Verify link target exists and is accessible",
                "Update link URL if target has moved",
                "Add alternative link or remove if no longer relevant"
            ]
        
        elif gap_type == GapType.MISSING_EXAMPLES:
            fixes = [
                "Add practical code examples showing usage",
                "Include both basic and advanced usage scenarios",
                "Provide complete, runnable examples"
            ]
        
        elif gap_type == GapType.INCONSISTENT_FORMAT:
            fixes = [
                "Standardize formatting according to style guide",
                "Use consistent header levels and spacing",
                "Apply automated formatting tools"
            ]
        
        elif gap_type == GapType.UNCLEAR_INSTRUCTIONS:
            fixes = [
                "Provide specific, step-by-step instructions",
                "Replace vague language with precise terms",
                "Add clarifying examples or screenshots"
            ]
        
        elif gap_type == GapType.MISSING_DEPENDENCIES:
            fixes = [
                "Add missing import statements",
                "Document required dependencies",
                "Include installation instructions"
            ]
        
        return fixes
    
    async def _analyze_readme_specific(self, content: str, file_path: str) -> List[DetectedGap]:
        """Analyze README-specific gaps."""
        
        gaps = []
        
        # Check for essential README sections
        essential_sections = [
            "installation", "usage", "examples", "contributing", "license"
        ]
        
        content_lower = content.lower()
        
        for section in essential_sections:
            if section not in content_lower:
                gap_id = hashlib.md5(f"missing_{section}_{file_path}".encode()).hexdigest()[:12]
                
                gap = DetectedGap(
                    gap_id=gap_id,
                    gap_type=GapType.MISSING_DOCUMENTATION,
                    severity=GapSeverity.HIGH,
                    content_type=ContentType.README,
                    file_path=file_path,
                    line_number=None,
                    description=f"Missing {section.title()} section",
                    evidence=[f"No {section} section found"],
                    suggested_fixes=[f"Add {section.title()} section with relevant information"],
                    confidence=0.9,
                    detected_at=time.time(),
                    pattern_matched="readme_essential_sections"
                )
                
                gaps.append(gap)
        
        return gaps
    
    async def _analyze_api_specific(self, content: str, file_path: str) -> List[DetectedGap]:
        """Analyze API documentation specific gaps."""
        
        gaps = []
        
        # Check for API endpoints without examples
        endpoint_pattern = r"(GET|POST|PUT|DELETE|PATCH)\s+(/[^\s]*)"
        endpoints = re.findall(endpoint_pattern, content)
        
        for method, path in endpoints:
            # Check if endpoint has example
            endpoint_section = f"{method} {path}"
            
            # Look for example in the next 500 characters
            endpoint_pos = content.find(endpoint_section)
            if endpoint_pos != -1:
                next_section = content[endpoint_pos:endpoint_pos + 500]
                
                if "example" not in next_section.lower() and "```" not in next_section:
                    gap_id = hashlib.md5(f"missing_example_{method}_{path}".encode()).hexdigest()[:12]
                    
                    gap = DetectedGap(
                        gap_id=gap_id,
                        gap_type=GapType.MISSING_EXAMPLES,
                        severity=GapSeverity.MEDIUM,
                        content_type=ContentType.API_REFERENCE,
                        file_path=file_path,
                        line_number=content[:endpoint_pos].count('\n') + 1,
                        description=f"API endpoint {method} {path} missing example",
                        evidence=[endpoint_section],
                        suggested_fixes=[
                            "Add request/response examples",
                            "Include curl command examples",
                            "Show different response scenarios"
                        ],
                        confidence=0.8,
                        detected_at=time.time(),
                        pattern_matched="api_missing_examples"
                    )
                    
                    gaps.append(gap)
        
        return gaps
    
    async def analyze_directory(self, directory_path: str) -> Dict[str, Any]:
        """Analyze all files in a directory for gaps."""
        
        directory = Path(directory_path)
        if not directory.exists():
            return {"error": f"Directory {directory_path} not found"}
        
        results = []
        total_gaps = 0
        
        # Analyze all relevant files
        for file_path in directory.rglob("*"):
            if file_path.is_file() and self._should_analyze_file(file_path):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    content_type = self._determine_content_type(file_path)
                    
                    result = await self.analyze_content(content, str(file_path), content_type)
                    results.append(result)
                    total_gaps += result.total_gaps
                    
                except Exception as e:
                    logger.error(f"Failed to analyze {file_path}: {e}")
        
        return {
            "directory": directory_path,
            "files_analyzed": len(results),
            "total_gaps": total_gaps,
            "results": results
        }
    
    def _should_analyze_file(self, file_path: Path) -> bool:
        """Determine if file should be analyzed."""
        
        # Skip binary files and large files
        if file_path.stat().st_size > self.config["max_file_size"]:
            return False
        
        # Analyze text files
        text_extensions = {".py", ".md", ".txt", ".yaml", ".yml", ".json", ".js", ".ts", ".html", ".css"}
        return file_path.suffix.lower() in text_extensions
    
    def _determine_content_type(self, file_path: Path) -> ContentType:
        """Determine content type based on file path."""
        
        name_lower = file_path.name.lower()
        
        if name_lower == "readme.md" or name_lower.startswith("readme"):
            return ContentType.README
        elif "api" in name_lower or "reference" in name_lower:
            return ContentType.API_REFERENCE
        elif "tutorial" in name_lower or "guide" in name_lower:
            return ContentType.TUTORIAL
        elif file_path.suffix in [".py", ".js", ".ts"]:
            return ContentType.CODE
        elif file_path.suffix in [".yaml", ".yml", ".json"]:
            return ContentType.CONFIGURATION
        else:
            return ContentType.DOCUMENTATION
    
    async def _real_time_monitor(self):
        """Real-time monitoring for gap detection."""
        
        while True:
            try:
                # Monitor for file changes and analyze new/modified files
                # This would integrate with file system watchers in a real implementation
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Real-time monitor error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    def get_gap_statistics(self) -> Dict[str, Any]:
        """Get comprehensive gap statistics."""
        
        total_gaps = len(self.detected_gaps)
        
        # Count by severity
        severity_counts = Counter(gap.severity.value for gap in self.detected_gaps)
        
        # Count by type
        type_counts = Counter(gap.gap_type.value for gap in self.detected_gaps)
        
        # Count by content type
        content_type_counts = Counter(gap.content_type.value for gap in self.detected_gaps)
        
        # Calculate average confidence
        avg_confidence = sum(gap.confidence for gap in self.detected_gaps) / total_gaps if total_gaps > 0 else 0
        
        return {
            "total_gaps": total_gaps,
            "severity_distribution": dict(severity_counts),
            "type_distribution": dict(type_counts),
            "content_type_distribution": dict(content_type_counts),
            "average_confidence": avg_confidence,
            "patterns_active": len(self.patterns),
            "analyses_performed": len(self.analysis_results)
        }


# Example usage
async def main():
    """Example usage of Gap Detection System."""
    
    detector = GapDetectionSystem()
    
    # Analyze sample content
    sample_code = '''
def process_data(data):
    # TODO: Add validation
    result = data * 2
    return result

class DataProcessor:
    def __init__(self):
        pass
    '''
    
    result = await detector.analyze_content(
        content=sample_code,
        file_path="sample.py",
        content_type=ContentType.CODE
    )
    
    print(f"Analysis completed: {result.total_gaps} gaps detected")
    for gap in result.gaps_detected:
        print(f"- {gap.gap_type.value}: {gap.description} (Line {gap.line_number})")
    
    # Get statistics
    stats = detector.get_gap_statistics()
    print(f"Total gaps detected: {stats['total_gaps']}")
    print(f"Severity distribution: {stats['severity_distribution']}")


if __name__ == "__main__":
    asyncio.run(main())
