"""
N.L.D.S. Security Testing & Penetration Testing Framework
Comprehensive security testing, vulnerability assessment, and penetration testing for N.L.D.S.
"""

import asyncio
import aiohttp
import json
import time
import hashlib
import secrets
import jwt
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import re
import base64
from urllib.parse import urljoin, urlparse
import ssl
import socket
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class VulnerabilityType(str, Enum):
    """Types of security vulnerabilities."""
    SQL_INJECTION = "sql_injection"
    XSS = "cross_site_scripting"
    CSRF = "cross_site_request_forgery"
    AUTHENTICATION_BYPASS = "authentication_bypass"
    AUTHORIZATION_FLAW = "authorization_flaw"
    INJECTION = "injection"
    BROKEN_ACCESS_CONTROL = "broken_access_control"
    SECURITY_MISCONFIGURATION = "security_misconfiguration"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    USING_COMPONENTS_WITH_VULNERABILITIES = "vulnerable_components"
    INSUFFICIENT_LOGGING = "insufficient_logging"
    RATE_LIMITING_BYPASS = "rate_limiting_bypass"
    JWT_VULNERABILITIES = "jwt_vulnerabilities"
    API_SECURITY_ISSUES = "api_security_issues"


class SeverityLevel(str, Enum):
    """Vulnerability severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SecurityTestResult:
    """Security test result."""
    test_name: str
    vulnerability_type: VulnerabilityType
    severity: SeverityLevel
    status: str  # PASS, FAIL, WARNING
    description: str
    evidence: Dict[str, Any]
    remediation: str
    cvss_score: Optional[float] = None


@dataclass
class PenetrationTestReport:
    """Comprehensive penetration test report."""
    target_system: str
    test_timestamp: datetime
    test_duration_minutes: float
    total_tests: int
    vulnerabilities_found: List[SecurityTestResult]
    security_score: float
    risk_assessment: str
    recommendations: List[str]
    compliance_status: Dict[str, bool]


class SecurityTestingFramework:
    """
    Comprehensive security testing and penetration testing framework
    for N.L.D.S. system security validation.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None
        
        # Test payloads for various vulnerability types
        self.sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "' OR 1=1#"
        ]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>"
        ]
        
        self.injection_payloads = [
            "; ls -la",
            "| whoami",
            "&& cat /etc/passwd",
            "`id`",
            "$(whoami)"
        ]
        
        # Common weak passwords for testing
        self.weak_passwords = [
            "password", "123456", "admin", "test", "guest",
            "password123", "admin123", "qwerty", "letmein"
        ]
        
        logger.info(f"Security Testing Framework initialized for {base_url}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(ssl=False)  # Allow testing with self-signed certs
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def test_sql_injection(self, endpoint: str, parameters: Dict[str, str]) -> List[SecurityTestResult]:
        """Test for SQL injection vulnerabilities."""
        results = []
        
        for payload in self.sql_injection_payloads:
            for param_name in parameters:
                test_params = parameters.copy()
                test_params[param_name] = payload
                
                try:
                    async with self.session.post(
                        urljoin(self.base_url, endpoint),
                        json=test_params,
                        headers=self._get_headers()
                    ) as response:
                        response_text = await response.text()
                        
                        # Check for SQL error indicators
                        sql_errors = [
                            "sql syntax", "mysql_fetch", "ora-", "postgresql",
                            "sqlite_", "sqlstate", "syntax error", "database error"
                        ]
                        
                        if any(error in response_text.lower() for error in sql_errors):
                            results.append(SecurityTestResult(
                                test_name=f"SQL Injection - {param_name}",
                                vulnerability_type=VulnerabilityType.SQL_INJECTION,
                                severity=SeverityLevel.HIGH,
                                status="FAIL",
                                description=f"SQL injection vulnerability detected in parameter '{param_name}'",
                                evidence={
                                    "payload": payload,
                                    "parameter": param_name,
                                    "response_snippet": response_text[:200],
                                    "status_code": response.status
                                },
                                remediation="Use parameterized queries and input validation",
                                cvss_score=8.1
                            ))
                        
                except Exception as e:
                    logger.debug(f"SQL injection test error: {e}")
        
        if not results:
            results.append(SecurityTestResult(
                test_name="SQL Injection Tests",
                vulnerability_type=VulnerabilityType.SQL_INJECTION,
                severity=SeverityLevel.INFO,
                status="PASS",
                description="No SQL injection vulnerabilities detected",
                evidence={},
                remediation="Continue using secure coding practices"
            ))
        
        return results
    
    async def test_xss_vulnerabilities(self, endpoint: str, parameters: Dict[str, str]) -> List[SecurityTestResult]:
        """Test for Cross-Site Scripting (XSS) vulnerabilities."""
        results = []
        
        for payload in self.xss_payloads:
            for param_name in parameters:
                test_params = parameters.copy()
                test_params[param_name] = payload
                
                try:
                    async with self.session.post(
                        urljoin(self.base_url, endpoint),
                        json=test_params,
                        headers=self._get_headers()
                    ) as response:
                        response_text = await response.text()
                        
                        # Check if payload is reflected in response
                        if payload in response_text:
                            results.append(SecurityTestResult(
                                test_name=f"XSS - {param_name}",
                                vulnerability_type=VulnerabilityType.XSS,
                                severity=SeverityLevel.MEDIUM,
                                status="FAIL",
                                description=f"XSS vulnerability detected in parameter '{param_name}'",
                                evidence={
                                    "payload": payload,
                                    "parameter": param_name,
                                    "reflected": True,
                                    "status_code": response.status
                                },
                                remediation="Implement proper input validation and output encoding",
                                cvss_score=6.1
                            ))
                        
                except Exception as e:
                    logger.debug(f"XSS test error: {e}")
        
        if not results:
            results.append(SecurityTestResult(
                test_name="XSS Tests",
                vulnerability_type=VulnerabilityType.XSS,
                severity=SeverityLevel.INFO,
                status="PASS",
                description="No XSS vulnerabilities detected",
                evidence={},
                remediation="Continue using proper input validation"
            ))
        
        return results
    
    async def test_authentication_bypass(self) -> List[SecurityTestResult]:
        """Test for authentication bypass vulnerabilities."""
        results = []
        
        # Test endpoints without authentication
        protected_endpoints = ["/admin", "/api/users", "/api/system", "/dashboard"]
        
        for endpoint in protected_endpoints:
            try:
                async with self.session.get(
                    urljoin(self.base_url, endpoint)
                ) as response:
                    if response.status == 200:
                        results.append(SecurityTestResult(
                            test_name=f"Authentication Bypass - {endpoint}",
                            vulnerability_type=VulnerabilityType.AUTHENTICATION_BYPASS,
                            severity=SeverityLevel.HIGH,
                            status="FAIL",
                            description=f"Protected endpoint '{endpoint}' accessible without authentication",
                            evidence={
                                "endpoint": endpoint,
                                "status_code": response.status,
                                "accessible": True
                            },
                            remediation="Implement proper authentication checks",
                            cvss_score=7.5
                        ))
                    
            except Exception as e:
                logger.debug(f"Authentication test error: {e}")
        
        # Test weak password authentication
        login_endpoint = "/api/auth/login"
        for password in self.weak_passwords:
            try:
                async with self.session.post(
                    urljoin(self.base_url, login_endpoint),
                    json={"username": "admin", "password": password},
                    headers=self._get_headers()
                ) as response:
                    if response.status == 200:
                        results.append(SecurityTestResult(
                            test_name="Weak Password Authentication",
                            vulnerability_type=VulnerabilityType.AUTHENTICATION_BYPASS,
                            severity=SeverityLevel.HIGH,
                            status="FAIL",
                            description=f"Weak password '{password}' accepted for admin user",
                            evidence={
                                "username": "admin",
                                "password": password,
                                "status_code": response.status
                            },
                            remediation="Enforce strong password policies",
                            cvss_score=8.0
                        ))
                        break
                        
            except Exception as e:
                logger.debug(f"Weak password test error: {e}")
        
        return results
    
    async def test_jwt_vulnerabilities(self) -> List[SecurityTestResult]:
        """Test for JWT-related vulnerabilities."""
        results = []
        
        # Test JWT with no signature
        try:
            # Create unsigned JWT
            header = {"alg": "none", "typ": "JWT"}
            payload = {"user": "admin", "role": "administrator", "exp": int(time.time()) + 3600}
            
            unsigned_jwt = (
                base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=') + '.' +
                base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=') + '.'
            )
            
            async with self.session.get(
                urljoin(self.base_url, "/api/protected"),
                headers={"Authorization": f"Bearer {unsigned_jwt}"}
            ) as response:
                if response.status == 200:
                    results.append(SecurityTestResult(
                        test_name="JWT None Algorithm",
                        vulnerability_type=VulnerabilityType.JWT_VULNERABILITIES,
                        severity=SeverityLevel.CRITICAL,
                        status="FAIL",
                        description="JWT with 'none' algorithm accepted",
                        evidence={
                            "jwt_token": unsigned_jwt,
                            "algorithm": "none",
                            "status_code": response.status
                        },
                        remediation="Reject JWTs with 'none' algorithm",
                        cvss_score=9.0
                    ))
                    
        except Exception as e:
            logger.debug(f"JWT none algorithm test error: {e}")
        
        # Test JWT with weak secret
        weak_secrets = ["secret", "key", "password", "123456"]
        for secret in weak_secrets:
            try:
                token = jwt.encode(
                    {"user": "admin", "role": "administrator", "exp": int(time.time()) + 3600},
                    secret,
                    algorithm="HS256"
                )
                
                async with self.session.get(
                    urljoin(self.base_url, "/api/protected"),
                    headers={"Authorization": f"Bearer {token}"}
                ) as response:
                    if response.status == 200:
                        results.append(SecurityTestResult(
                            test_name="JWT Weak Secret",
                            vulnerability_type=VulnerabilityType.JWT_VULNERABILITIES,
                            severity=SeverityLevel.HIGH,
                            status="FAIL",
                            description=f"JWT with weak secret '{secret}' accepted",
                            evidence={
                                "weak_secret": secret,
                                "status_code": response.status
                            },
                            remediation="Use strong, randomly generated JWT secrets",
                            cvss_score=7.8
                        ))
                        break
                        
            except Exception as e:
                logger.debug(f"JWT weak secret test error: {e}")
        
        return results
    
    async def test_rate_limiting(self, endpoint: str = "/api/process") -> List[SecurityTestResult]:
        """Test rate limiting implementation."""
        results = []
        
        # Send rapid requests to test rate limiting
        request_count = 50
        start_time = time.time()
        
        tasks = []
        for i in range(request_count):
            task = self._make_test_request(endpoint)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        # Analyze responses
        status_codes = []
        for response in responses:
            if isinstance(response, Exception):
                continue
            status_codes.append(response.get('status_code', 0))
        
        rate_limited_count = sum(1 for code in status_codes if code == 429)
        success_count = sum(1 for code in status_codes if code == 200)
        
        if rate_limited_count == 0:
            results.append(SecurityTestResult(
                test_name="Rate Limiting Test",
                vulnerability_type=VulnerabilityType.RATE_LIMITING_BYPASS,
                severity=SeverityLevel.MEDIUM,
                status="FAIL",
                description="No rate limiting detected",
                evidence={
                    "requests_sent": request_count,
                    "successful_requests": success_count,
                    "rate_limited_requests": rate_limited_count,
                    "duration_seconds": end_time - start_time
                },
                remediation="Implement proper rate limiting",
                cvss_score=5.3
            ))
        else:
            results.append(SecurityTestResult(
                test_name="Rate Limiting Test",
                vulnerability_type=VulnerabilityType.RATE_LIMITING_BYPASS,
                severity=SeverityLevel.INFO,
                status="PASS",
                description="Rate limiting is working properly",
                evidence={
                    "requests_sent": request_count,
                    "rate_limited_requests": rate_limited_count
                },
                remediation="Continue monitoring rate limiting effectiveness"
            ))
        
        return results
    
    async def _make_test_request(self, endpoint: str) -> Dict[str, Any]:
        """Make a test request and return response info."""
        try:
            async with self.session.post(
                urljoin(self.base_url, endpoint),
                json={"input_text": "test"},
                headers=self._get_headers()
            ) as response:
                return {
                    "status_code": response.status,
                    "headers": dict(response.headers)
                }
        except Exception as e:
            return {"error": str(e)}
    
    async def test_ssl_configuration(self) -> List[SecurityTestResult]:
        """Test SSL/TLS configuration."""
        results = []
        
        try:
            parsed_url = urlparse(self.base_url)
            hostname = parsed_url.hostname
            port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
            
            if parsed_url.scheme == 'https':
                # Test SSL certificate
                context = ssl.create_default_context()
                
                with socket.create_connection((hostname, port), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        
                        # Check certificate expiration
                        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        days_until_expiry = (not_after - datetime.now()).days
                        
                        if days_until_expiry < 30:
                            results.append(SecurityTestResult(
                                test_name="SSL Certificate Expiry",
                                vulnerability_type=VulnerabilityType.SECURITY_MISCONFIGURATION,
                                severity=SeverityLevel.MEDIUM,
                                status="WARNING",
                                description=f"SSL certificate expires in {days_until_expiry} days",
                                evidence={
                                    "expiry_date": cert['notAfter'],
                                    "days_remaining": days_until_expiry
                                },
                                remediation="Renew SSL certificate before expiration"
                            ))
                        
                        # Check for weak cipher suites (simplified check)
                        cipher = ssock.cipher()
                        if cipher and 'RC4' in cipher[0] or 'DES' in cipher[0]:
                            results.append(SecurityTestResult(
                                test_name="Weak SSL Cipher",
                                vulnerability_type=VulnerabilityType.SECURITY_MISCONFIGURATION,
                                severity=SeverityLevel.MEDIUM,
                                status="FAIL",
                                description="Weak SSL cipher suite detected",
                                evidence={"cipher": cipher[0]},
                                remediation="Configure strong cipher suites only"
                            ))
            else:
                results.append(SecurityTestResult(
                    test_name="HTTPS Usage",
                    vulnerability_type=VulnerabilityType.SECURITY_MISCONFIGURATION,
                    severity=SeverityLevel.HIGH,
                    status="FAIL",
                    description="Service not using HTTPS",
                    evidence={"scheme": parsed_url.scheme},
                    remediation="Enable HTTPS for all communications",
                    cvss_score=7.4
                ))
                
        except Exception as e:
            logger.error(f"SSL configuration test error: {e}")
        
        return results
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for requests."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "NLDS-Security-Scanner/1.0"
        }
        
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        return headers
    
    async def run_comprehensive_test(self) -> PenetrationTestReport:
        """Run comprehensive penetration testing."""
        start_time = datetime.now()
        all_results = []
        
        logger.info("Starting comprehensive security testing...")
        
        # Test SQL injection
        sql_results = await self.test_sql_injection("/api/process", {"input_text": "test"})
        all_results.extend(sql_results)
        
        # Test XSS
        xss_results = await self.test_xss_vulnerabilities("/api/process", {"input_text": "test"})
        all_results.extend(xss_results)
        
        # Test authentication bypass
        auth_results = await self.test_authentication_bypass()
        all_results.extend(auth_results)
        
        # Test JWT vulnerabilities
        jwt_results = await self.test_jwt_vulnerabilities()
        all_results.extend(jwt_results)
        
        # Test rate limiting
        rate_results = await self.test_rate_limiting()
        all_results.extend(rate_results)
        
        # Test SSL configuration
        ssl_results = await self.test_ssl_configuration()
        all_results.extend(ssl_results)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        
        # Calculate security score
        security_score = self._calculate_security_score(all_results)
        
        # Generate risk assessment
        risk_assessment = self._generate_risk_assessment(all_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_results)
        
        # Check compliance
        compliance_status = self._check_compliance(all_results)
        
        return PenetrationTestReport(
            target_system=self.base_url,
            test_timestamp=start_time,
            test_duration_minutes=duration,
            total_tests=len(all_results),
            vulnerabilities_found=[r for r in all_results if r.status == "FAIL"],
            security_score=security_score,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            compliance_status=compliance_status
        )
    
    def _calculate_security_score(self, results: List[SecurityTestResult]) -> float:
        """Calculate overall security score (0-100)."""
        if not results:
            return 0.0
        
        total_score = 0
        max_possible_score = 0
        
        for result in results:
            max_possible_score += 10  # Each test worth 10 points
            
            if result.status == "PASS":
                total_score += 10
            elif result.status == "WARNING":
                total_score += 5
            elif result.status == "FAIL":
                if result.severity == SeverityLevel.CRITICAL:
                    total_score += 0
                elif result.severity == SeverityLevel.HIGH:
                    total_score += 2
                elif result.severity == SeverityLevel.MEDIUM:
                    total_score += 4
                else:
                    total_score += 6
        
        return (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
    
    def _generate_risk_assessment(self, results: List[SecurityTestResult]) -> str:
        """Generate risk assessment based on findings."""
        critical_count = sum(1 for r in results if r.severity == SeverityLevel.CRITICAL and r.status == "FAIL")
        high_count = sum(1 for r in results if r.severity == SeverityLevel.HIGH and r.status == "FAIL")
        
        if critical_count > 0:
            return "CRITICAL - Immediate action required"
        elif high_count > 2:
            return "HIGH - Address vulnerabilities promptly"
        elif high_count > 0:
            return "MEDIUM - Plan remediation activities"
        else:
            return "LOW - Continue monitoring and maintenance"
    
    def _generate_recommendations(self, results: List[SecurityTestResult]) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        failed_results = [r for r in results if r.status == "FAIL"]
        
        if failed_results:
            recommendations.append("Address all identified vulnerabilities according to severity")
            recommendations.append("Implement regular security testing in CI/CD pipeline")
            recommendations.append("Conduct security code reviews for all changes")
            recommendations.append("Provide security training for development team")
        
        recommendations.append("Implement Web Application Firewall (WAF)")
        recommendations.append("Enable comprehensive security logging and monitoring")
        recommendations.append("Conduct regular penetration testing")
        
        return recommendations
    
    def _check_compliance(self, results: List[SecurityTestResult]) -> Dict[str, bool]:
        """Check compliance with security standards."""
        failed_critical = any(r.severity == SeverityLevel.CRITICAL and r.status == "FAIL" for r in results)
        failed_high = sum(1 for r in results if r.severity == SeverityLevel.HIGH and r.status == "FAIL")
        
        return {
            "OWASP_Top_10": not failed_critical and failed_high < 3,
            "PCI_DSS": not failed_critical and failed_high == 0,
            "SOC_2": not failed_critical and failed_high < 2,
            "ISO_27001": not failed_critical and failed_high < 3
        }


# Example usage
if __name__ == "__main__":
    async def main():
        async with SecurityTestingFramework("https://api.jaegis.ai") as security_tester:
            report = await security_tester.run_comprehensive_test()
            
            print("Security Testing Report")
            print("=" * 50)
            print(f"Target: {report.target_system}")
            print(f"Security Score: {report.security_score:.1f}/100")
            print(f"Risk Assessment: {report.risk_assessment}")
            print(f"Vulnerabilities Found: {len(report.vulnerabilities_found)}")
            
            if report.vulnerabilities_found:
                print("\nVulnerabilities:")
                for vuln in report.vulnerabilities_found:
                    print(f"  - {vuln.test_name} ({vuln.severity.value})")
    
    asyncio.run(main())
