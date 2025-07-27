"""
N.L.D.S. Security Framework Design
Comprehensive security protocols, authentication, authorization, and data protection mechanisms
"""

import hashlib
import secrets
import jwt
import bcrypt
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for different operations"""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    AUTHORIZED = "authorized"
    ADMIN = "admin"
    SYSTEM = "system"


class UserRole(Enum):
    """User roles for role-based access control"""
    GUEST = "guest"
    USER = "user"
    PREMIUM = "premium"
    DEVELOPER = "developer"
    ADMIN = "admin"
    SYSTEM = "system"


@dataclass
class SecurityConfig:
    """Security configuration settings"""
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    password_min_length: int = 8
    password_require_special: bool = True
    session_timeout_minutes: int = 30
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 15
    encryption_key: Optional[str] = None
    rate_limit_requests_per_minute: int = 100
    audit_log_retention_days: int = 90


@dataclass
class UserSession:
    """User session information"""
    user_id: str
    username: str
    role: UserRole
    session_id: str
    created_at: datetime
    last_activity: datetime
    ip_address: str
    user_agent: str
    permissions: List[str]


@dataclass
class SecurityEvent:
    """Security event for audit logging"""
    event_id: str
    event_type: str
    user_id: Optional[str]
    ip_address: str
    timestamp: datetime
    details: Dict[str, Any]
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"


class NLDSSecurityFramework:
    """
    Comprehensive security framework for N.L.D.S.
    
    Provides authentication, authorization, data protection,
    audit logging, and security monitoring capabilities.
    """
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.active_sessions: Dict[str, UserSession] = {}
        self.failed_login_attempts: Dict[str, List[datetime]] = {}
        self.security_events: List[SecurityEvent] = []
        
        # Initialize encryption
        if config.encryption_key:
            self.cipher_suite = Fernet(config.encryption_key.encode())
        else:
            self.cipher_suite = Fernet(Fernet.generate_key())
        
        logger.info("N.L.D.S. Security Framework initialized")
    
    # Authentication Methods
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        issues = []
        
        if len(password) < self.config.password_min_length:
            issues.append(f"Password must be at least {self.config.password_min_length} characters")
        
        if not any(c.isupper() for c in password):
            issues.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            issues.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain at least one digit")
        
        if self.config.password_require_special and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            issues.append("Password must contain at least one special character")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "strength_score": max(0, 100 - len(issues) * 20)
        }
    
    def generate_jwt_token(self, user_id: str, username: str, role: UserRole, permissions: List[str]) -> str:
        """Generate JWT token for authenticated user"""
        payload = {
            "user_id": user_id,
            "username": username,
            "role": role.value,
            "permissions": permissions,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=self.config.jwt_expiration_hours)
        }
        
        token = jwt.encode(payload, self.config.jwt_secret_key, algorithm=self.config.jwt_algorithm)
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.config.jwt_secret_key, algorithms=[self.config.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
    
    def authenticate_user(self, username: str, password: str, ip_address: str, user_agent: str) -> Optional[str]:
        """Authenticate user and create session"""
        
        # Check for account lockout
        if self._is_account_locked(username):
            self._log_security_event(
                "AUTHENTICATION_BLOCKED",
                None,
                ip_address,
                {"username": username, "reason": "account_locked"},
                "MEDIUM"
            )
            return None
        
        # Simulate user lookup (in real implementation, query database)
        user_data = self._get_user_data(username)
        if not user_data:
            self._record_failed_login(username)
            self._log_security_event(
                "AUTHENTICATION_FAILED",
                None,
                ip_address,
                {"username": username, "reason": "user_not_found"},
                "MEDIUM"
            )
            return None
        
        # Verify password
        if not self.verify_password(password, user_data["password_hash"]):
            self._record_failed_login(username)
            self._log_security_event(
                "AUTHENTICATION_FAILED",
                user_data["user_id"],
                ip_address,
                {"username": username, "reason": "invalid_password"},
                "MEDIUM"
            )
            return None
        
        # Clear failed login attempts
        if username in self.failed_login_attempts:
            del self.failed_login_attempts[username]
        
        # Create session
        session_id = self._generate_session_id()
        session = UserSession(
            user_id=user_data["user_id"],
            username=username,
            role=UserRole(user_data["role"]),
            session_id=session_id,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            permissions=user_data["permissions"]
        )
        
        self.active_sessions[session_id] = session
        
        self._log_security_event(
            "AUTHENTICATION_SUCCESS",
            user_data["user_id"],
            ip_address,
            {"username": username, "session_id": session_id},
            "LOW"
        )
        
        return session_id
    
    # Authorization Methods
    
    def authorize_request(self, session_id: str, required_permission: str, resource: str = None) -> bool:
        """Authorize user request based on permissions"""
        
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        # Check session timeout
        if self._is_session_expired(session):
            self._invalidate_session(session_id)
            return False
        
        # Update last activity
        session.last_activity = datetime.now()
        
        # Check permission
        if required_permission in session.permissions or "admin" in session.permissions:
            self._log_security_event(
                "AUTHORIZATION_SUCCESS",
                session.user_id,
                session.ip_address,
                {"permission": required_permission, "resource": resource},
                "LOW"
            )
            return True
        
        self._log_security_event(
            "AUTHORIZATION_FAILED",
            session.user_id,
            session.ip_address,
            {"permission": required_permission, "resource": resource},
            "MEDIUM"
        )
        return False
    
    def check_role_permission(self, role: UserRole, required_permission: str) -> bool:
        """Check if role has required permission"""
        
        role_permissions = {
            UserRole.GUEST: ["read_public"],
            UserRole.USER: ["read_public", "read_user", "write_user"],
            UserRole.PREMIUM: ["read_public", "read_user", "write_user", "read_premium"],
            UserRole.DEVELOPER: ["read_public", "read_user", "write_user", "read_premium", "api_access"],
            UserRole.ADMIN: ["admin"],  # Admin has all permissions
            UserRole.SYSTEM: ["system"]  # System has all permissions
        }
        
        permissions = role_permissions.get(role, [])
        return required_permission in permissions or "admin" in permissions or "system" in permissions
    
    # Data Protection Methods
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode()
    
    def hash_data(self, data: str) -> str:
        """Create hash of data for integrity verification"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def sanitize_input(self, input_data: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        # Remove potentially dangerous characters
        dangerous_chars = ["<", ">", "&", "\"", "'", ";", "(", ")", "{", "}", "[", "]"]
        sanitized = input_data
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        return sanitized.strip()
    
    # Session Management
    
    def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get active session"""
        session = self.active_sessions.get(session_id)
        if session and not self._is_session_expired(session):
            session.last_activity = datetime.now()
            return session
        elif session:
            self._invalidate_session(session_id)
        return None
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate user session"""
        return self._invalidate_session(session_id)
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        expired_sessions = [
            session_id for session_id, session in self.active_sessions.items()
            if self._is_session_expired(session)
        ]
        
        for session_id in expired_sessions:
            self._invalidate_session(session_id)
        
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    # Security Monitoring
    
    def get_security_events(self, severity: str = None, limit: int = 100) -> List[SecurityEvent]:
        """Get security events for monitoring"""
        events = self.security_events
        
        if severity:
            events = [event for event in events if event.severity == severity]
        
        return sorted(events, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def detect_suspicious_activity(self, user_id: str, ip_address: str) -> List[str]:
        """Detect suspicious activity patterns"""
        alerts = []
        
        # Check for multiple failed logins
        recent_failures = [
            event for event in self.security_events
            if event.event_type == "AUTHENTICATION_FAILED" and
            event.timestamp > datetime.now() - timedelta(hours=1) and
            event.details.get("username") == user_id
        ]
        
        if len(recent_failures) >= 3:
            alerts.append("Multiple failed login attempts detected")
        
        # Check for unusual IP address
        user_sessions = [
            session for session in self.active_sessions.values()
            if session.user_id == user_id
        ]
        
        if user_sessions:
            usual_ips = set(session.ip_address for session in user_sessions)
            if ip_address not in usual_ips and len(usual_ips) > 0:
                alerts.append("Login from unusual IP address")
        
        return alerts
    
    # Private Helper Methods
    
    def _get_user_data(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user data (simulated - in real implementation, query database)"""
        # Simulated user database
        users = {
            "admin": {
                "user_id": "admin_001",
                "username": "admin",
                "password_hash": self.hash_password("admin123!"),
                "role": "admin",
                "permissions": ["admin"]
            },
            "user": {
                "user_id": "user_001",
                "username": "user",
                "password_hash": self.hash_password("user123!"),
                "role": "user",
                "permissions": ["read_public", "read_user", "write_user"]
            }
        }
        
        return users.get(username)
    
    def _generate_session_id(self) -> str:
        """Generate secure session ID"""
        return secrets.token_urlsafe(32)
    
    def _is_session_expired(self, session: UserSession) -> bool:
        """Check if session is expired"""
        timeout = timedelta(minutes=self.config.session_timeout_minutes)
        return datetime.now() - session.last_activity > timeout
    
    def _invalidate_session(self, session_id: str) -> bool:
        """Invalidate session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            del self.active_sessions[session_id]
            
            self._log_security_event(
                "SESSION_INVALIDATED",
                session.user_id,
                session.ip_address,
                {"session_id": session_id},
                "LOW"
            )
            return True
        return False
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to failed login attempts"""
        if username not in self.failed_login_attempts:
            return False
        
        attempts = self.failed_login_attempts[username]
        recent_attempts = [
            attempt for attempt in attempts
            if datetime.now() - attempt < timedelta(minutes=self.config.lockout_duration_minutes)
        ]
        
        return len(recent_attempts) >= self.config.max_login_attempts
    
    def _record_failed_login(self, username: str):
        """Record failed login attempt"""
        if username not in self.failed_login_attempts:
            self.failed_login_attempts[username] = []
        
        self.failed_login_attempts[username].append(datetime.now())
        
        # Clean up old attempts
        cutoff = datetime.now() - timedelta(minutes=self.config.lockout_duration_minutes)
        self.failed_login_attempts[username] = [
            attempt for attempt in self.failed_login_attempts[username]
            if attempt > cutoff
        ]
    
    def _log_security_event(self, event_type: str, user_id: Optional[str], ip_address: str, 
                           details: Dict[str, Any], severity: str):
        """Log security event"""
        event = SecurityEvent(
            event_id=secrets.token_urlsafe(16),
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            timestamp=datetime.now(),
            details=details,
            severity=severity
        )
        
        self.security_events.append(event)
        
        # Clean up old events
        cutoff = datetime.now() - timedelta(days=self.config.audit_log_retention_days)
        self.security_events = [
            event for event in self.security_events
            if event.timestamp > cutoff
        ]
        
        logger.info(f"Security event logged: {event_type} - {severity}")


# Security Framework Factory
def create_security_framework(jwt_secret: str = None) -> NLDSSecurityFramework:
    """Create N.L.D.S. Security Framework with default configuration"""
    
    if not jwt_secret:
        jwt_secret = secrets.token_urlsafe(32)
    
    config = SecurityConfig(
        jwt_secret_key=jwt_secret,
        jwt_algorithm="HS256",
        jwt_expiration_hours=24,
        password_min_length=8,
        password_require_special=True,
        session_timeout_minutes=30,
        max_login_attempts=5,
        lockout_duration_minutes=15,
        rate_limit_requests_per_minute=100,
        audit_log_retention_days=90
    )
    
    return NLDSSecurityFramework(config)


# Example usage
if __name__ == "__main__":
    # Create security framework
    security = create_security_framework()
    
    # Test authentication
    session_id = security.authenticate_user("admin", "admin123!", "127.0.0.1", "Test-Agent")
    
    if session_id:
        print(f"Authentication successful. Session ID: {session_id}")
        
        # Test authorization
        authorized = security.authorize_request(session_id, "admin", "user_management")
        print(f"Authorization result: {authorized}")
        
        # Test data encryption
        sensitive_data = "This is sensitive information"
        encrypted = security.encrypt_sensitive_data(sensitive_data)
        decrypted = security.decrypt_sensitive_data(encrypted)
        print(f"Encryption test: {decrypted == sensitive_data}")
    else:
        print("Authentication failed")
