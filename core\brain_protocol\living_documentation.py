"""
JAEGIS Brain Protocol Suite v1.0 - Living Documentation Mandate
Mandate 2.3: Automatic documentation consistency detection and diff generation

This module implements the mandatory living documentation protocol that maintains
documentation consistency by automatically detecting inconsistencies and generating
specific diff changes to bring documents back into alignment.
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
import difflib
import re

logger = logging.getLogger(__name__)


class DocumentType(str, Enum):
    """Types of documents managed."""
    README = "readme"
    API_REFERENCE = "api_reference"
    ARCHITECTURE = "architecture"
    USER_GUIDE = "user_guide"
    CHANGELOG = "changelog"
    CONTRIBUTING = "contributing"
    SECURITY = "security"
    DEPLOYMENT = "deployment"


class InconsistencyType(str, Enum):
    """Types of documentation inconsistencies."""
    VERSION_MISMATCH = "version_mismatch"
    FEATURE_OUTDATED = "feature_outdated"
    API_CHANGE = "api_change"
    ARCHITECTURE_DRIFT = "architecture_drift"
    BROKEN_REFERENCE = "broken_reference"
    MISSING_SECTION = "missing_section"
    OUTDATED_EXAMPLE = "outdated_example"
    CONFIGURATION_CHANGE = "configuration_change"


class InconsistencySeverity(str, Enum):
    """Severity levels for inconsistencies."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


@dataclass
class DocumentInconsistency:
    """Documentation inconsistency detection."""
    inconsistency_id: str
    document_path: str
    document_type: DocumentType
    inconsistency_type: InconsistencyType
    severity: InconsistencySeverity
    description: str
    current_content: str
    expected_content: str
    line_number: Optional[int]
    section: str
    detected_at: float


@dataclass
class DocumentDiff:
    """Generated diff for document correction."""
    diff_id: str
    inconsistency_id: str
    document_path: str
    operation: str  # "replace", "insert", "delete"
    line_start: int
    line_end: int
    old_content: str
    new_content: str
    diff_text: str
    confidence_score: float
    generated_at: float


@dataclass
class DocumentScan:
    """Document consistency scan result."""
    scan_id: str
    scan_timestamp: float
    documents_scanned: List[str]
    inconsistencies_found: List[DocumentInconsistency]
    diffs_generated: List[DocumentDiff]
    scan_duration_ms: float
    total_issues: int
    critical_issues: int


class LivingDocumentationManager:
    """
    JAEGIS Brain Protocol Suite Living Documentation Manager
    
    Implements Mandate 2.3: Living Documentation Mandate
    
    Mandatory execution sequence:
    1. Assume Custodianship - Official custodian of core document suite
    2. Automatic Inconsistency Detection - Cross-reference changes against documents
    3. Propose Exact Changes - Generate specific diff or proposed text changes
    """
    
    def __init__(self):
        self.document_registry: Dict[str, DocumentType] = {}
        self.scan_history: List[DocumentScan] = []
        self.inconsistencies: List[DocumentInconsistency] = []
        self.pending_diffs: List[DocumentDiff] = []
        
        # Document patterns and rules
        self.consistency_rules = {
            "version_patterns": [
                r"version\s*[:\-=]\s*([0-9]+\.[0-9]+\.[0-9]+)",
                r"v([0-9]+\.[0-9]+\.[0-9]+)",
                r"JAEGIS\s+v?([0-9]+\.[0-9]+)"
            ],
            "api_patterns": [
                r"(GET|POST|PUT|DELETE)\s+(/[^\s]+)",
                r"endpoint[:\s]+([^\s]+)",
                r"api\.([a-zA-Z_]+)\("
            ],
            "feature_patterns": [
                r"feature[:\s]+([^\n]+)",
                r"supports?\s+([^\n]+)",
                r"includes?\s+([^\n]+)"
            ],
            "configuration_patterns": [
                r"config[:\s]+([^\n]+)",
                r"setting[:\s]+([^\n]+)",
                r"parameter[:\s]+([^\n]+)"
            ]
        }
        
        # Initialize document registry
        self._initialize_document_registry()
        
        logger.info("Living Documentation Manager initialized as custodian")
    
    def _initialize_document_registry(self):
        """Initialize registry of canonical documents."""
        
        canonical_documents = {
            "README.md": DocumentType.README,
            "docs/API.md": DocumentType.API_REFERENCE,
            "docs/ARCHITECTURE.md": DocumentType.ARCHITECTURE,
            "docs/USER_GUIDE.md": DocumentType.USER_GUIDE,
            "CHANGELOG.md": DocumentType.CHANGELOG,
            "CONTRIBUTING.md": DocumentType.CONTRIBUTING,
            "SECURITY.md": DocumentType.SECURITY,
            "docs/DEPLOYMENT.md": DocumentType.DEPLOYMENT,
            "core/brain_protocol/protocol_suite.json": DocumentType.API_REFERENCE
        }
        
        for doc_path, doc_type in canonical_documents.items():
            self.document_registry[doc_path] = doc_type
    
    async def mandatory_consistency_scan(self, recent_changes: List[str]) -> DocumentScan:
        """
        MANDATORY: Automatic inconsistency detection after changes
        
        This method MUST cross-reference recent changes against the content
        of all canonical project documents as part of the Strategic Horizon Scan.
        """
        
        scan_start = time.time()
        scan_id = f"doc_scan_{int(time.time())}"
        
        logger.info(f"📚 MANDATORY CONSISTENCY SCAN - Scan ID: {scan_id}")
        logger.info(f"🔍 Recent Changes: {len(recent_changes)}")
        
        # Step 1: Analyze recent changes for documentation impact
        change_analysis = await self._analyze_change_impact(recent_changes)
        
        # Step 2: Scan all canonical documents
        documents_scanned = []
        inconsistencies_found = []
        
        for doc_path, doc_type in self.document_registry.items():
            if Path(doc_path).exists():
                documents_scanned.append(doc_path)
                doc_inconsistencies = await self._scan_document_consistency(
                    doc_path, doc_type, change_analysis
                )
                inconsistencies_found.extend(doc_inconsistencies)
        
        # Step 3: Generate diffs for inconsistencies
        diffs_generated = []
        for inconsistency in inconsistencies_found:
            diff = await self._generate_correction_diff(inconsistency)
            if diff:
                diffs_generated.append(diff)
        
        scan_duration = (time.time() - scan_start) * 1000
        
        # Create scan result
        document_scan = DocumentScan(
            scan_id=scan_id,
            scan_timestamp=time.time(),
            documents_scanned=documents_scanned,
            inconsistencies_found=inconsistencies_found,
            diffs_generated=diffs_generated,
            scan_duration_ms=scan_duration,
            total_issues=len(inconsistencies_found),
            critical_issues=len([i for i in inconsistencies_found if i.severity == InconsistencySeverity.CRITICAL])
        )
        
        # Store results
        self.scan_history.append(document_scan)
        self.inconsistencies.extend(inconsistencies_found)
        self.pending_diffs.extend(diffs_generated)
        
        logger.info(f"📚 Consistency scan complete:")
        logger.info(f"  Documents scanned: {len(documents_scanned)}")
        logger.info(f"  Inconsistencies found: {len(inconsistencies_found)}")
        logger.info(f"  Diffs generated: {len(diffs_generated)}")
        logger.info(f"  Critical issues: {document_scan.critical_issues}")
        logger.info(f"  Scan duration: {scan_duration:.1f}ms")
        
        return document_scan
    
    async def _analyze_change_impact(self, recent_changes: List[str]) -> Dict[str, Any]:
        """Analyze recent changes for documentation impact."""
        
        impact_analysis = {
            "version_changes": [],
            "api_changes": [],
            "feature_changes": [],
            "configuration_changes": [],
            "architecture_changes": [],
            "security_changes": []
        }
        
        for change in recent_changes:
            change_lower = change.lower()
            
            # Version changes
            if any(word in change_lower for word in ["version", "release", "update"]):
                impact_analysis["version_changes"].append(change)
            
            # API changes
            if any(word in change_lower for word in ["api", "endpoint", "route", "interface"]):
                impact_analysis["api_changes"].append(change)
            
            # Feature changes
            if any(word in change_lower for word in ["feature", "functionality", "capability"]):
                impact_analysis["feature_changes"].append(change)
            
            # Configuration changes
            if any(word in change_lower for word in ["config", "setting", "parameter", "option"]):
                impact_analysis["configuration_changes"].append(change)
            
            # Architecture changes
            if any(word in change_lower for word in ["architecture", "structure", "design", "pattern"]):
                impact_analysis["architecture_changes"].append(change)
            
            # Security changes
            if any(word in change_lower for word in ["security", "auth", "permission", "access"]):
                impact_analysis["security_changes"].append(change)
        
        return impact_analysis
    
    async def _scan_document_consistency(self, doc_path: str, doc_type: DocumentType, 
                                       change_analysis: Dict[str, Any]) -> List[DocumentInconsistency]:
        """Scan individual document for consistency issues."""
        
        inconsistencies = []
        
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Check version consistency
            if change_analysis["version_changes"]:
                version_inconsistencies = await self._check_version_consistency(
                    doc_path, doc_type, content, lines
                )
                inconsistencies.extend(version_inconsistencies)
            
            # Check API consistency
            if change_analysis["api_changes"]:
                api_inconsistencies = await self._check_api_consistency(
                    doc_path, doc_type, content, lines
                )
                inconsistencies.extend(api_inconsistencies)
            
            # Check feature consistency
            if change_analysis["feature_changes"]:
                feature_inconsistencies = await self._check_feature_consistency(
                    doc_path, doc_type, content, lines
                )
                inconsistencies.extend(feature_inconsistencies)
            
            # Check configuration consistency
            if change_analysis["configuration_changes"]:
                config_inconsistencies = await self._check_configuration_consistency(
                    doc_path, doc_type, content, lines
                )
                inconsistencies.extend(config_inconsistencies)
            
            # Check for broken references
            reference_inconsistencies = await self._check_broken_references(
                doc_path, doc_type, content, lines
            )
            inconsistencies.extend(reference_inconsistencies)
            
        except Exception as e:
            logger.error(f"Error scanning document {doc_path}: {e}")
        
        return inconsistencies
    
    async def _check_version_consistency(self, doc_path: str, doc_type: DocumentType,
                                       content: str, lines: List[str]) -> List[DocumentInconsistency]:
        """Check for version inconsistencies."""
        
        inconsistencies = []
        
        # Get current system version
        current_version = await self._get_current_system_version()
        
        # Find version references in document
        for i, line in enumerate(lines):
            for pattern in self.consistency_rules["version_patterns"]:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    found_version = match.group(1)
                    
                    if found_version != current_version:
                        inconsistency_id = f"version_{int(time.time())}_{i}"
                        
                        inconsistency = DocumentInconsistency(
                            inconsistency_id=inconsistency_id,
                            document_path=doc_path,
                            document_type=doc_type,
                            inconsistency_type=InconsistencyType.VERSION_MISMATCH,
                            severity=InconsistencySeverity.HIGH,
                            description=f"Version mismatch: found {found_version}, expected {current_version}",
                            current_content=line,
                            expected_content=line.replace(found_version, current_version),
                            line_number=i + 1,
                            section=self._identify_section(lines, i),
                            detected_at=time.time()
                        )
                        
                        inconsistencies.append(inconsistency)
        
        return inconsistencies
    
    async def _check_api_consistency(self, doc_path: str, doc_type: DocumentType,
                                   content: str, lines: List[str]) -> List[DocumentInconsistency]:
        """Check for API documentation inconsistencies."""
        
        inconsistencies = []
        
        # Get current API endpoints
        current_apis = await self._get_current_api_endpoints()
        
        # Find API references in document
        for i, line in enumerate(lines):
            for pattern in self.consistency_rules["api_patterns"]:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    found_api = match.group(0)
                    
                    # Check if API still exists
                    if not self._api_exists(found_api, current_apis):
                        inconsistency_id = f"api_{int(time.time())}_{i}"
                        
                        inconsistency = DocumentInconsistency(
                            inconsistency_id=inconsistency_id,
                            document_path=doc_path,
                            document_type=doc_type,
                            inconsistency_type=InconsistencyType.API_CHANGE,
                            severity=InconsistencySeverity.MEDIUM,
                            description=f"API reference may be outdated: {found_api}",
                            current_content=line,
                            expected_content=f"# TODO: Update API reference - {found_api}",
                            line_number=i + 1,
                            section=self._identify_section(lines, i),
                            detected_at=time.time()
                        )
                        
                        inconsistencies.append(inconsistency)
        
        return inconsistencies
    
    async def _check_feature_consistency(self, doc_path: str, doc_type: DocumentType,
                                       content: str, lines: List[str]) -> List[DocumentInconsistency]:
        """Check for feature documentation inconsistencies."""
        
        inconsistencies = []
        
        # Simple feature consistency check
        outdated_features = ["old_feature", "deprecated_function", "legacy_mode"]
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for outdated_feature in outdated_features:
                if outdated_feature in line_lower:
                    inconsistency_id = f"feature_{int(time.time())}_{i}"
                    
                    inconsistency = DocumentInconsistency(
                        inconsistency_id=inconsistency_id,
                        document_path=doc_path,
                        document_type=doc_type,
                        inconsistency_type=InconsistencyType.FEATURE_OUTDATED,
                        severity=InconsistencySeverity.MEDIUM,
                        description=f"Outdated feature reference: {outdated_feature}",
                        current_content=line,
                        expected_content=f"# TODO: Update feature reference - {outdated_feature}",
                        line_number=i + 1,
                        section=self._identify_section(lines, i),
                        detected_at=time.time()
                    )
                    
                    inconsistencies.append(inconsistency)
        
        return inconsistencies
    
    async def _check_configuration_consistency(self, doc_path: str, doc_type: DocumentType,
                                             content: str, lines: List[str]) -> List[DocumentInconsistency]:
        """Check for configuration documentation inconsistencies."""
        
        inconsistencies = []
        
        # Get current configuration
        current_config = await self._get_current_configuration()
        
        # Check for outdated configuration examples
        for i, line in enumerate(lines):
            if "config" in line.lower() and "example" in line.lower():
                # Simplified check for configuration consistency
                if "old_setting" in line.lower():
                    inconsistency_id = f"config_{int(time.time())}_{i}"
                    
                    inconsistency = DocumentInconsistency(
                        inconsistency_id=inconsistency_id,
                        document_path=doc_path,
                        document_type=doc_type,
                        inconsistency_type=InconsistencyType.CONFIGURATION_CHANGE,
                        severity=InconsistencySeverity.LOW,
                        description="Configuration example may be outdated",
                        current_content=line,
                        expected_content="# TODO: Update configuration example",
                        line_number=i + 1,
                        section=self._identify_section(lines, i),
                        detected_at=time.time()
                    )
                    
                    inconsistencies.append(inconsistency)
        
        return inconsistencies
    
    async def _check_broken_references(self, doc_path: str, doc_type: DocumentType,
                                     content: str, lines: List[str]) -> List[DocumentInconsistency]:
        """Check for broken internal references."""
        
        inconsistencies = []
        
        # Find markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        for i, line in enumerate(lines):
            matches = re.finditer(link_pattern, line)
            for match in matches:
                link_text = match.group(1)
                link_url = match.group(2)
                
                # Check internal links
                if not link_url.startswith('http') and not link_url.startswith('#'):
                    # Check if file exists
                    link_path = Path(doc_path).parent / link_url
                    if not link_path.exists():
                        inconsistency_id = f"link_{int(time.time())}_{i}"
                        
                        inconsistency = DocumentInconsistency(
                            inconsistency_id=inconsistency_id,
                            document_path=doc_path,
                            document_type=doc_type,
                            inconsistency_type=InconsistencyType.BROKEN_REFERENCE,
                            severity=InconsistencySeverity.MEDIUM,
                            description=f"Broken internal link: {link_url}",
                            current_content=line,
                            expected_content=f"# TODO: Fix broken link - {link_url}",
                            line_number=i + 1,
                            section=self._identify_section(lines, i),
                            detected_at=time.time()
                        )
                        
                        inconsistencies.append(inconsistency)
        
        return inconsistencies
    
    async def _generate_correction_diff(self, inconsistency: DocumentInconsistency) -> Optional[DocumentDiff]:
        """Generate specific diff for correcting inconsistency."""
        
        diff_id = f"diff_{inconsistency.inconsistency_id}"
        
        # Generate unified diff
        old_lines = [inconsistency.current_content]
        new_lines = [inconsistency.expected_content]
        
        diff_text = '\n'.join(difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"{inconsistency.document_path}:old",
            tofile=f"{inconsistency.document_path}:new",
            lineterm=''
        ))
        
        # Calculate confidence score
        confidence_score = self._calculate_diff_confidence(inconsistency)
        
        diff = DocumentDiff(
            diff_id=diff_id,
            inconsistency_id=inconsistency.inconsistency_id,
            document_path=inconsistency.document_path,
            operation="replace",
            line_start=inconsistency.line_number or 1,
            line_end=inconsistency.line_number or 1,
            old_content=inconsistency.current_content,
            new_content=inconsistency.expected_content,
            diff_text=diff_text,
            confidence_score=confidence_score,
            generated_at=time.time()
        )
        
        return diff
    
    def _calculate_diff_confidence(self, inconsistency: DocumentInconsistency) -> float:
        """Calculate confidence score for the diff."""
        
        base_confidence = 0.8
        
        # Adjust based on inconsistency type
        type_adjustments = {
            InconsistencyType.VERSION_MISMATCH: 0.1,
            InconsistencyType.BROKEN_REFERENCE: 0.05,
            InconsistencyType.API_CHANGE: -0.1,
            InconsistencyType.FEATURE_OUTDATED: -0.05
        }
        
        adjustment = type_adjustments.get(inconsistency.inconsistency_type, 0.0)
        
        return min(1.0, max(0.0, base_confidence + adjustment))
    
    def _identify_section(self, lines: List[str], line_index: int) -> str:
        """Identify the section containing the line."""
        
        # Look backwards for the nearest heading
        for i in range(line_index, -1, -1):
            line = lines[i].strip()
            if line.startswith('#'):
                return line.lstrip('#').strip()
        
        return "Unknown Section"
    
    async def _get_current_system_version(self) -> str:
        """Get current system version."""
        
        try:
            # Try to read from protocol suite
            protocol_path = Path("core/brain_protocol/protocol_suite.json")
            if protocol_path.exists():
                with open(protocol_path, 'r') as f:
                    data = json.load(f)
                    return data.get("version", "1.0")
        except Exception:
            pass
        
        return "1.0"  # Default version
    
    async def _get_current_api_endpoints(self) -> List[str]:
        """Get current API endpoints."""
        
        # Simplified - would scan actual API definitions
        return [
            "GET /api/v1/status",
            "POST /api/v1/process",
            "GET /api/v1/agents"
        ]
    
    def _api_exists(self, api_reference: str, current_apis: List[str]) -> bool:
        """Check if API reference exists in current APIs."""
        
        # Simplified check
        return any(api_reference in api for api in current_apis)
    
    async def _get_current_configuration(self) -> Dict[str, Any]:
        """Get current system configuration."""
        
        # Simplified configuration
        return {
            "version": "1.0",
            "mode": "production",
            "features": ["brain_protocol", "agent_system"]
        }
    
    def get_pending_diffs(self, severity_filter: Optional[InconsistencySeverity] = None) -> List[DocumentDiff]:
        """Get pending diffs, optionally filtered by severity."""
        
        if not severity_filter:
            return self.pending_diffs.copy()
        
        filtered_diffs = []
        for diff in self.pending_diffs:
            # Find corresponding inconsistency
            inconsistency = next(
                (i for i in self.inconsistencies if i.inconsistency_id == diff.inconsistency_id),
                None
            )
            if inconsistency and inconsistency.severity == severity_filter:
                filtered_diffs.append(diff)
        
        return filtered_diffs
    
    def get_documentation_status(self) -> Dict[str, Any]:
        """Get comprehensive documentation status."""
        
        recent_scans = len([s for s in self.scan_history if time.time() - s.scan_timestamp < 3600])
        
        severity_counts = {}
        for inconsistency in self.inconsistencies:
            severity = inconsistency.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "total_documents": len(self.document_registry),
            "total_scans": len(self.scan_history),
            "recent_scans_1h": recent_scans,
            "total_inconsistencies": len(self.inconsistencies),
            "pending_diffs": len(self.pending_diffs),
            "inconsistencies_by_severity": severity_counts,
            "average_scan_duration_ms": sum(s.scan_duration_ms for s in self.scan_history) / len(self.scan_history) if self.scan_history else 0,
            "documents_managed": list(self.document_registry.keys())
        }


# Global living documentation manager
LIVING_DOCUMENTATION_MANAGER = LivingDocumentationManager()


async def mandatory_documentation_consistency_check(recent_changes: List[str]) -> DocumentScan:
    """
    MANDATORY: Check documentation consistency after changes
    
    This function MUST be called as part of the Strategic Horizon Scan
    according to JAEGIS Brain Protocol Suite Mandate 2.3.
    """
    
    return await LIVING_DOCUMENTATION_MANAGER.mandatory_consistency_scan(recent_changes)


def get_documentation_diffs(severity_filter: Optional[InconsistencySeverity] = None) -> List[DocumentDiff]:
    """
    Get proposed documentation diffs
    
    This provides the specific diff or proposed text changes required to
    bring documents back into alignment with recent changes.
    """
    
    return LIVING_DOCUMENTATION_MANAGER.get_pending_diffs(severity_filter)


# Example usage
async def main():
    """Example usage of Living Documentation Manager."""
    
    print("📚 JAEGIS BRAIN PROTOCOL SUITE - LIVING DOCUMENTATION TEST")
    
    # Test consistency scan
    recent_changes = [
        "Updated JAEGIS version to 2.2",
        "Added new API endpoint /api/v1/brain",
        "Deprecated old_feature functionality",
        "Changed configuration format"
    ]
    
    scan = await LIVING_DOCUMENTATION_MANAGER.mandatory_consistency_scan(recent_changes)
    
    print(f"\n📚 Documentation Scan Results:")
    print(f"  Scan ID: {scan.scan_id}")
    print(f"  Documents Scanned: {len(scan.documents_scanned)}")
    print(f"  Inconsistencies Found: {scan.total_issues}")
    print(f"  Critical Issues: {scan.critical_issues}")
    print(f"  Diffs Generated: {len(scan.diffs_generated)}")
    
    # Show pending diffs
    critical_diffs = LIVING_DOCUMENTATION_MANAGER.get_pending_diffs(InconsistencySeverity.CRITICAL)
    print(f"\n📝 Critical Diffs: {len(critical_diffs)}")
    
    for diff in critical_diffs[:3]:
        print(f"  - {diff.document_path}:{diff.line_start}")
        print(f"    Old: {diff.old_content[:50]}...")
        print(f"    New: {diff.new_content[:50]}...")
    
    # Get status
    status = LIVING_DOCUMENTATION_MANAGER.get_documentation_status()
    print(f"\n📊 Documentation Status:")
    print(f"  Total Documents: {status['total_documents']}")
    print(f"  Total Inconsistencies: {status['total_inconsistencies']}")
    print(f"  Pending Diffs: {status['pending_diffs']}")


if __name__ == "__main__":
    asyncio.run(main())
