"""
Security Protocol Implementation for Synchronization
Apply pre-sync scanning, data sanitization, audit trail generation, and protection mechanisms
"""

import asyncio
import hashlib
import json
import time
import logging
import re
import os
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import secrets

logger = logging.getLogger(__name__)


class SecurityLevel(str, Enum):
    """Security scanning levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    PARANOID = "paranoid"


class ThreatLevel(str, Enum):
    """Threat severity levels."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ScanResult(str, Enum):
    """Security scan results."""
    CLEAN = "clean"
    SANITIZED = "sanitized"
    BLOCKED = "blocked"
    QUARANTINED = "quarantined"


@dataclass
class SecurityThreat:
    """Security threat detection."""
    threat_id: str
    threat_type: str
    severity: ThreatLevel
    file_path: str
    line_number: Optional[int]
    description: str
    evidence: str
    recommendation: str
    auto_fixable: bool


@dataclass
class ScanReport:
    """Security scan report."""
    scan_id: str
    file_path: str
    scan_level: SecurityLevel
    result: ScanResult
    threats_found: List[SecurityThreat]
    sanitization_applied: List[str]
    scan_duration_ms: float
    timestamp: float


@dataclass
class AuditEntry:
    """Security audit trail entry."""
    entry_id: str
    action: str
    user: str
    file_path: str
    details: Dict[str, Any]
    security_context: Dict[str, Any]
    timestamp: float
    ip_address: str


class SyncSecurityProtocols:
    """
    Security Protocol Implementation for Synchronization
    
    Provides comprehensive security protocols including:
    - Pre-sync security scanning
    - Data sanitization and cleaning
    - Audit trail generation
    - Protection mechanisms
    - Threat detection and response
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        self.security_level = security_level
        self.scan_reports: List[ScanReport] = []
        self.audit_trail: List[AuditEntry] = []
        self.quarantine_files: Set[str] = set()
        
        # Security patterns
        self.security_patterns = self._initialize_security_patterns()
        
        # Configuration
        self.config = {
            "max_file_size_mb": 100,
            "scan_timeout_seconds": 30,
            "quarantine_enabled": True,
            "auto_sanitization": True,
            "audit_retention_days": 90,
            "threat_notification_threshold": ThreatLevel.HIGH,
            "allowed_file_extensions": {
                ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".md", ".txt", ".rst",
                ".toml", ".cfg", ".ini", ".conf", ".dockerfile", ".gitignore"
            },
            "blocked_file_extensions": {
                ".exe", ".bat", ".cmd", ".ps1", ".sh", ".scr", ".com", ".pif"
            }
        }
        
        logger.info(f"Security Protocols initialized with {security_level.value} level")
    
    def _initialize_security_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize security threat detection patterns."""
        
        return {
            "secrets": [
                {
                    "name": "API Key",
                    "pattern": r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
                    "severity": ThreatLevel.HIGH,
                    "description": "Potential API key exposure"
                },
                {
                    "name": "Password",
                    "pattern": r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?([^'\"\s]{8,})['\"]?",
                    "severity": ThreatLevel.HIGH,
                    "description": "Potential password exposure"
                },
                {
                    "name": "Private Key",
                    "pattern": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
                    "severity": ThreatLevel.CRITICAL,
                    "description": "Private key detected"
                },
                {
                    "name": "JWT Token",
                    "pattern": r"eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*",
                    "severity": ThreatLevel.HIGH,
                    "description": "JWT token detected"
                },
                {
                    "name": "Database URL",
                    "pattern": r"(?i)(mongodb|mysql|postgresql|redis)://[^\s]+",
                    "severity": ThreatLevel.MEDIUM,
                    "description": "Database connection string detected"
                }
            ],
            
            "malicious_code": [
                {
                    "name": "SQL Injection",
                    "pattern": r"(?i)(union\s+select|drop\s+table|delete\s+from|insert\s+into).*['\"]",
                    "severity": ThreatLevel.HIGH,
                    "description": "Potential SQL injection pattern"
                },
                {
                    "name": "Command Injection",
                    "pattern": r"(?i)(exec|eval|system|shell_exec|passthru)\s*\(",
                    "severity": ThreatLevel.HIGH,
                    "description": "Potential command injection"
                },
                {
                    "name": "XSS Pattern",
                    "pattern": r"<script[^>]*>.*?</script>",
                    "severity": ThreatLevel.MEDIUM,
                    "description": "Potential XSS script tag"
                }
            ],
            
            "sensitive_data": [
                {
                    "name": "Credit Card",
                    "pattern": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
                    "severity": ThreatLevel.HIGH,
                    "description": "Potential credit card number"
                },
                {
                    "name": "SSN",
                    "pattern": r"\b\d{3}-\d{2}-\d{4}\b",
                    "severity": ThreatLevel.HIGH,
                    "description": "Potential Social Security Number"
                },
                {
                    "name": "Email Address",
                    "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                    "severity": ThreatLevel.LOW,
                    "description": "Email address detected"
                }
            ],
            
            "configuration_issues": [
                {
                    "name": "Debug Mode",
                    "pattern": r"(?i)(debug\s*[:=]\s*true|debug_mode\s*[:=]\s*true)",
                    "severity": ThreatLevel.MEDIUM,
                    "description": "Debug mode enabled"
                },
                {
                    "name": "Insecure Protocol",
                    "pattern": r"(?i)http://[^\s]+",
                    "severity": ThreatLevel.LOW,
                    "description": "Insecure HTTP protocol usage"
                }
            ]
        }
    
    async def pre_sync_security_scan(self, file_paths: List[str]) -> Dict[str, ScanReport]:
        """Perform comprehensive pre-sync security scanning."""
        
        logger.info(f"Starting pre-sync security scan for {len(file_paths)} files")
        
        scan_results = {}
        
        for file_path in file_paths:
            try:
                scan_report = await self._scan_file(file_path)
                scan_results[file_path] = scan_report
                
                # Handle threats based on severity
                await self._handle_scan_results(scan_report)
                
            except Exception as e:
                logger.error(f"Security scan failed for {file_path}: {e}")
                
                # Create error report
                scan_results[file_path] = ScanReport(
                    scan_id=f"scan_{int(time.time())}_{secrets.token_hex(4)}",
                    file_path=file_path,
                    scan_level=self.security_level,
                    result=ScanResult.BLOCKED,
                    threats_found=[],
                    sanitization_applied=[],
                    scan_duration_ms=0,
                    timestamp=time.time()
                )
        
        # Store scan reports
        self.scan_reports.extend(scan_results.values())
        
        # Generate audit entry
        await self._create_audit_entry(
            action="pre_sync_scan",
            details={
                "files_scanned": len(file_paths),
                "threats_found": sum(len(report.threats_found) for report in scan_results.values()),
                "files_blocked": len([r for r in scan_results.values() if r.result == ScanResult.BLOCKED])
            }
        )
        
        logger.info(f"Pre-sync security scan completed: {len(scan_results)} files processed")
        
        return scan_results
    
    async def _scan_file(self, file_path: str) -> ScanReport:
        """Scan individual file for security threats."""
        
        scan_start = time.time()
        scan_id = f"scan_{int(time.time())}_{secrets.token_hex(4)}"
        
        threats_found = []
        sanitization_applied = []
        result = ScanResult.CLEAN
        
        try:
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext in self.config["blocked_file_extensions"]:
                threats_found.append(SecurityThreat(
                    threat_id=f"threat_{secrets.token_hex(4)}",
                    threat_type="blocked_extension",
                    severity=ThreatLevel.HIGH,
                    file_path=file_path,
                    line_number=None,
                    description=f"Blocked file extension: {file_ext}",
                    evidence=f"File extension {file_ext} is not allowed",
                    recommendation="Remove file or change extension",
                    auto_fixable=False
                ))
                result = ScanResult.BLOCKED
            
            # Check file size
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                
                if file_size > self.config["max_file_size_mb"]:
                    threats_found.append(SecurityThreat(
                        threat_id=f"threat_{secrets.token_hex(4)}",
                        threat_type="oversized_file",
                        severity=ThreatLevel.MEDIUM,
                        file_path=file_path,
                        line_number=None,
                        description=f"File size exceeds limit: {file_size:.1f} MB",
                        evidence=f"File size: {file_size:.1f} MB, limit: {self.config['max_file_size_mb']} MB",
                        recommendation="Reduce file size or split into smaller files",
                        auto_fixable=False
                    ))
                
                # Scan file content
                content_threats, content_sanitization = await self._scan_file_content(file_path)
                threats_found.extend(content_threats)
                sanitization_applied.extend(content_sanitization)
            
            # Determine final result
            if result != ScanResult.BLOCKED:
                if threats_found:
                    critical_threats = [t for t in threats_found if t.severity == ThreatLevel.CRITICAL]
                    high_threats = [t for t in threats_found if t.severity == ThreatLevel.HIGH]
                    
                    if critical_threats:
                        result = ScanResult.BLOCKED
                    elif high_threats and self.security_level in [SecurityLevel.STRICT, SecurityLevel.PARANOID]:
                        result = ScanResult.QUARANTINED
                    elif sanitization_applied:
                        result = ScanResult.SANITIZED
                    else:
                        result = ScanResult.CLEAN
                else:
                    result = ScanResult.CLEAN
        
        except Exception as e:
            logger.error(f"File scan error for {file_path}: {e}")
            result = ScanResult.BLOCKED
        
        scan_duration = (time.time() - scan_start) * 1000  # milliseconds
        
        return ScanReport(
            scan_id=scan_id,
            file_path=file_path,
            scan_level=self.security_level,
            result=result,
            threats_found=threats_found,
            sanitization_applied=sanitization_applied,
            scan_duration_ms=scan_duration,
            timestamp=time.time()
        )
    
    async def _scan_file_content(self, file_path: str) -> Tuple[List[SecurityThreat], List[str]]:
        """Scan file content for security threats."""
        
        threats = []
        sanitization = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Scan for each pattern category
            for category, patterns in self.security_patterns.items():
                for pattern_info in patterns:
                    pattern = pattern_info["pattern"]
                    
                    for line_num, line in enumerate(lines, 1):
                        matches = re.finditer(pattern, line)
                        
                        for match in matches:
                            threat = SecurityThreat(
                                threat_id=f"threat_{secrets.token_hex(4)}",
                                threat_type=pattern_info["name"],
                                severity=pattern_info["severity"],
                                file_path=file_path,
                                line_number=line_num,
                                description=pattern_info["description"],
                                evidence=match.group(0)[:100],  # Limit evidence length
                                recommendation=self._get_threat_recommendation(pattern_info["name"]),
                                auto_fixable=self._is_auto_fixable(pattern_info["name"])
                            )
                            
                            threats.append(threat)
                            
                            # Apply auto-sanitization if enabled
                            if (self.config["auto_sanitization"] and 
                                threat.auto_fixable and 
                                threat.severity not in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]):
                                
                                sanitized_line = self._sanitize_line(line, pattern, pattern_info["name"])
                                if sanitized_line != line:
                                    lines[line_num - 1] = sanitized_line
                                    sanitization.append(f"Line {line_num}: {pattern_info['name']}")
            
            # Write sanitized content back if changes were made
            if sanitization and self.config["auto_sanitization"]:
                sanitized_content = '\n'.join(lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(sanitized_content)
        
        except Exception as e:
            logger.error(f"Content scan error for {file_path}: {e}")
        
        return threats, sanitization
    
    def _get_threat_recommendation(self, threat_type: str) -> str:
        """Get recommendation for specific threat type."""
        
        recommendations = {
            "API Key": "Remove API key and use environment variables",
            "Password": "Remove password and use secure configuration",
            "Private Key": "Remove private key and use secure key management",
            "JWT Token": "Remove JWT token and use secure token storage",
            "Database URL": "Use environment variables for database configuration",
            "SQL Injection": "Use parameterized queries",
            "Command Injection": "Validate and sanitize input",
            "XSS Pattern": "Escape HTML content properly",
            "Credit Card": "Remove or mask credit card numbers",
            "SSN": "Remove or mask Social Security Numbers",
            "Email Address": "Consider if email exposure is necessary",
            "Debug Mode": "Disable debug mode in production",
            "Insecure Protocol": "Use HTTPS instead of HTTP"
        }
        
        return recommendations.get(threat_type, "Review and address security concern")
    
    def _is_auto_fixable(self, threat_type: str) -> bool:
        """Determine if threat can be automatically fixed."""
        
        auto_fixable = {
            "Email Address", "Debug Mode", "Insecure Protocol"
        }
        
        return threat_type in auto_fixable
    
    def _sanitize_line(self, line: str, pattern: str, threat_type: str) -> str:
        """Sanitize line content based on threat type."""
        
        if threat_type == "Email Address":
            # Mask email addresses
            return re.sub(pattern, "[EMAIL_REDACTED]", line)
        
        elif threat_type == "Debug Mode":
            # Disable debug mode
            return re.sub(r"(?i)(debug\s*[:=]\s*)true", r"\1false", line)
        
        elif threat_type == "Insecure Protocol":
            # Convert HTTP to HTTPS
            return re.sub(r"(?i)http://", "https://", line)
        
        return line
    
    async def _handle_scan_results(self, scan_report: ScanReport):
        """Handle scan results based on severity and configuration."""
        
        if scan_report.result == ScanResult.BLOCKED:
            logger.warning(f"File blocked: {scan_report.file_path}")
            
        elif scan_report.result == ScanResult.QUARANTINED:
            self.quarantine_files.add(scan_report.file_path)
            logger.warning(f"File quarantined: {scan_report.file_path}")
        
        # Check for notification threshold
        critical_threats = [t for t in scan_report.threats_found 
                          if t.severity in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]]
        
        if critical_threats:
            await self._send_security_notification(scan_report, critical_threats)
    
    async def _send_security_notification(self, scan_report: ScanReport, threats: List[SecurityThreat]):
        """Send security notification for high-severity threats."""
        
        logger.critical(f"Security threats detected in {scan_report.file_path}: {len(threats)} threats")
        
        # In a real implementation, this would send notifications via email, Slack, etc.
        for threat in threats:
            logger.critical(f"  {threat.threat_type}: {threat.description}")
    
    async def _create_audit_entry(self, action: str, details: Dict[str, Any], 
                                file_path: str = "", user: str = "system"):
        """Create audit trail entry."""
        
        entry = AuditEntry(
            entry_id=f"audit_{int(time.time())}_{secrets.token_hex(4)}",
            action=action,
            user=user,
            file_path=file_path,
            details=details,
            security_context={
                "security_level": self.security_level.value,
                "scan_patterns": len(sum(self.security_patterns.values(), [])),
                "quarantine_enabled": self.config["quarantine_enabled"]
            },
            timestamp=time.time(),
            ip_address="127.0.0.1"  # Would be actual IP in real implementation
        )
        
        self.audit_trail.append(entry)
        
        # Cleanup old audit entries
        cutoff_time = time.time() - (self.config["audit_retention_days"] * 24 * 3600)
        self.audit_trail = [e for e in self.audit_trail if e.timestamp >= cutoff_time]
    
    async def sanitize_data(self, data: str, sanitization_rules: Optional[List[str]] = None) -> Tuple[str, List[str]]:
        """Sanitize data using specified or default rules."""
        
        if sanitization_rules is None:
            sanitization_rules = ["secrets", "sensitive_data"]
        
        sanitized_data = data
        applied_sanitizations = []
        
        for rule_category in sanitization_rules:
            if rule_category in self.security_patterns:
                for pattern_info in self.security_patterns[rule_category]:
                    pattern = pattern_info["pattern"]
                    
                    if re.search(pattern, sanitized_data):
                        if pattern_info["name"] in ["API Key", "Password", "Private Key", "JWT Token"]:
                            sanitized_data = re.sub(pattern, "[REDACTED]", sanitized_data)
                            applied_sanitizations.append(pattern_info["name"])
                        
                        elif pattern_info["name"] == "Credit Card":
                            sanitized_data = re.sub(pattern, "****-****-****-****", sanitized_data)
                            applied_sanitizations.append(pattern_info["name"])
                        
                        elif pattern_info["name"] == "SSN":
                            sanitized_data = re.sub(pattern, "***-**-****", sanitized_data)
                            applied_sanitizations.append(pattern_info["name"])
        
        return sanitized_data, applied_sanitizations
    
    def generate_audit_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive audit report."""
        
        cutoff_time = time.time() - (hours * 3600)
        recent_entries = [e for e in self.audit_trail if e.timestamp >= cutoff_time]
        recent_scans = [s for s in self.scan_reports if s.timestamp >= cutoff_time]
        
        # Count actions
        action_counts = {}
        for entry in recent_entries:
            action_counts[entry.action] = action_counts.get(entry.action, 0) + 1
        
        # Count threats by type
        threat_counts = {}
        for scan in recent_scans:
            for threat in scan.threats_found:
                threat_counts[threat.threat_type] = threat_counts.get(threat.threat_type, 0) + 1
        
        # Count scan results
        result_counts = {}
        for scan in recent_scans:
            result_counts[scan.result.value] = result_counts.get(scan.result.value, 0) + 1
        
        return {
            "report_period_hours": hours,
            "audit_entries": len(recent_entries),
            "security_scans": len(recent_scans),
            "action_distribution": action_counts,
            "threat_distribution": threat_counts,
            "scan_result_distribution": result_counts,
            "quarantined_files": len(self.quarantine_files),
            "total_threats_found": sum(len(s.threats_found) for s in recent_scans),
            "average_scan_duration_ms": sum(s.scan_duration_ms for s in recent_scans) / len(recent_scans) if recent_scans else 0
        }
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status and metrics."""
        
        recent_scans = [s for s in self.scan_reports if time.time() - s.timestamp < 3600]  # Last hour
        
        return {
            "security_level": self.security_level.value,
            "total_scans": len(self.scan_reports),
            "recent_scans": len(recent_scans),
            "quarantined_files": len(self.quarantine_files),
            "audit_entries": len(self.audit_trail),
            "threat_patterns": len(sum(self.security_patterns.values(), [])),
            "auto_sanitization_enabled": self.config["auto_sanitization"],
            "quarantine_enabled": self.config["quarantine_enabled"]
        }
    
    async def release_quarantine(self, file_path: str, justification: str) -> bool:
        """Release file from quarantine with justification."""
        
        if file_path in self.quarantine_files:
            self.quarantine_files.remove(file_path)
            
            await self._create_audit_entry(
                action="quarantine_release",
                file_path=file_path,
                details={
                    "justification": justification,
                    "released_by": "admin"  # Would be actual user in real implementation
                }
            )
            
            logger.info(f"File released from quarantine: {file_path}")
            return True
        
        return False


# Example usage
async def main():
    """Example usage of Sync Security Protocols."""
    
    security = SyncSecurityProtocols(SecurityLevel.STANDARD)
    
    # Simulate file paths
    test_files = [
        "test_file.py",
        "config.json",
        "README.md"
    ]
    
    # Perform pre-sync security scan
    scan_results = await security.pre_sync_security_scan(test_files)
    
    print(f"Security Scan Results:")
    for file_path, report in scan_results.items():
        print(f"  {file_path}: {report.result.value}")
        if report.threats_found:
            print(f"    Threats: {len(report.threats_found)}")
            for threat in report.threats_found[:3]:  # Show first 3
                print(f"      - {threat.threat_type}: {threat.severity.value}")
    
    # Generate audit report
    audit_report = security.generate_audit_report(24)
    print(f"\nAudit Report (24h):")
    print(f"  Security scans: {audit_report['security_scans']}")
    print(f"  Threats found: {audit_report['total_threats_found']}")
    print(f"  Quarantined files: {audit_report['quarantined_files']}")
    
    # Get security status
    status = security.get_security_status()
    print(f"\nSecurity Status:")
    print(f"  Level: {status['security_level']}")
    print(f"  Total scans: {status['total_scans']}")
    print(f"  Threat patterns: {status['threat_patterns']}")


if __name__ == "__main__":
    asyncio.run(main())
