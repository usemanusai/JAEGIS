"""
JAEGIS Configuration Management System - Security & Access Control
Implements security measures and access control for configuration management
"""

import hashlib
import secrets
import jwt
import logging
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import os

logger = logging.getLogger(__name__)

class Permission(Enum):
    """Configuration management permissions"""
    READ_CONFIG = "read_config"
    WRITE_CONFIG = "write_config"
    MANAGE_PROTOCOLS = "manage_protocols"
    MANAGE_AGENTS = "manage_agents"
    EXPORT_CONFIG = "export_config"
    IMPORT_CONFIG = "import_config"
    ROLLBACK_CONFIG = "rollback_config"
    VIEW_METRICS = "view_metrics"
    ADMIN_ACCESS = "admin_access"

class Role(Enum):
    """User roles with different permission levels"""
    VIEWER = "viewer"
    OPERATOR = "operator"
    ADMINISTRATOR = "administrator"
    SUPER_ADMIN = "super_admin"

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    Role.VIEWER: {
        Permission.READ_CONFIG,
        Permission.VIEW_METRICS
    },
    Role.OPERATOR: {
        Permission.READ_CONFIG,
        Permission.WRITE_CONFIG,
        Permission.VIEW_METRICS,
        Permission.EXPORT_CONFIG
    },
    Role.ADMINISTRATOR: {
        Permission.READ_CONFIG,
        Permission.WRITE_CONFIG,
        Permission.MANAGE_PROTOCOLS,
        Permission.MANAGE_AGENTS,
        Permission.EXPORT_CONFIG,
        Permission.IMPORT_CONFIG,
        Permission.ROLLBACK_CONFIG,
        Permission.VIEW_METRICS
    },
    Role.SUPER_ADMIN: set(Permission)  # All permissions
}

@dataclass
class User:
    """User account information"""
    user_id: str
    username: str
    email: str
    role: Role
    password_hash: str
    salt: str
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches"""
        return self._hash_password(password, self.salt) == self.password_hash
    
    def set_password(self, password: str):
        """Set a new password"""
        self.salt = secrets.token_hex(32)
        self.password_hash = self._hash_password(password, self.salt)
    
    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Hash password with salt"""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        if not self.is_active:
            return False
        
        if self.locked_until and datetime.now() < self.locked_until:
            return False
        
        return permission in ROLE_PERMISSIONS.get(self.role, set())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding sensitive data)"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active
        }

@dataclass
class Session:
    """User session information"""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.now() > self.expires_at
    
    def extend_session(self, hours: int = 24):
        """Extend session expiration"""
        self.expires_at = datetime.now() + timedelta(hours=hours)

@dataclass
class AuditLog:
    """Audit log entry"""
    log_id: str
    user_id: str
    action: str
    resource: str
    details: Dict[str, Any]
    timestamp: datetime
    ip_address: str
    success: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "action": self.action,
            "resource": self.resource,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "ip_address": self.ip_address,
            "success": self.success
        }

class SecurityManager:
    """Central security management system"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or os.environ.get('JAEGIS_SECRET_KEY', secrets.token_hex(32))
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.audit_logs: List[AuditLog] = []
        
        # Security settings
        self.max_failed_attempts = 5
        self.lockout_duration_minutes = 30
        self.session_duration_hours = 24
        self.password_min_length = 8
        
        # Create default admin user if none exists
        self._create_default_admin()
        
        logger.info("Security manager initialized")
    
    def _create_default_admin(self):
        """Create default admin user if no users exist"""
        if not self.users:
            admin_user = User(
                user_id="admin",
                username="admin",
                email="admin@JAEGIS.local",
                role=Role.SUPER_ADMIN,
                password_hash="",
                salt=""
            )
            admin_user.set_password("admin123")  # Default password - should be changed
            self.users[admin_user.user_id] = admin_user
            
            logger.warning("Created default admin user - please change password immediately")
    
    def create_user(self, username: str, email: str, password: str, role: Role, creator_user_id: str) -> Optional[User]:
        """Create a new user"""
        # Check if creator has permission
        creator = self.get_user(creator_user_id)
        if not creator or not creator.has_permission(Permission.ADMIN_ACCESS):
            logger.error(f"User {creator_user_id} does not have permission to create users")
            return None
        
        # Validate password
        if not self._validate_password(password):
            logger.error("Password does not meet requirements")
            return None
        
        # Check if username already exists
        if any(user.username == username for user in self.users.values()):
            logger.error(f"Username {username} already exists")
            return None
        
        # Create user
        user_id = secrets.token_hex(16)
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            password_hash="",
            salt=""
        )
        user.set_password(password)
        
        self.users[user_id] = user
        
        # Log the action
        self._log_action(
            user_id=creator_user_id,
            action="create_user",
            resource=f"user:{user_id}",
            details={"username": username, "role": role.value},
            success=True
        )
        
        logger.info(f"Created user: {username}")
        return user
    
    def authenticate_user(self, username: str, password: str, ip_address: str = "", user_agent: str = "") -> Optional[str]:
        """Authenticate user and create session"""
        # Find user by username
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            self._log_action(
                user_id="unknown",
                action="login_attempt",
                resource="authentication",
                details={"username": username, "reason": "user_not_found"},
                success=False,
                ip_address=ip_address
            )
            return None
        
        # Check if account is locked
        if user.locked_until and datetime.now() < user.locked_until:
            self._log_action(
                user_id=user.user_id,
                action="login_attempt",
                resource="authentication",
                details={"username": username, "reason": "account_locked"},
                success=False,
                ip_address=ip_address
            )
            return None
        
        # Check password
        if not user.check_password(password):
            user.failed_login_attempts += 1
            
            # Lock account if too many failed attempts
            if user.failed_login_attempts >= self.max_failed_attempts:
                user.locked_until = datetime.now() + timedelta(minutes=self.lockout_duration_minutes)
                logger.warning(f"Account locked for user {username}")
            
            self._log_action(
                user_id=user.user_id,
                action="login_attempt",
                resource="authentication",
                details={"username": username, "reason": "invalid_password"},
                success=False,
                ip_address=ip_address
            )
            return None
        
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.now()
        
        # Create session
        session_id = secrets.token_hex(32)
        session = Session(
            session_id=session_id,
            user_id=user.user_id,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=self.session_duration_hours),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.sessions[session_id] = session
        
        self._log_action(
            user_id=user.user_id,
            action="login",
            resource="authentication",
            details={"username": username},
            success=True,
            ip_address=ip_address
        )
        
        logger.info(f"User {username} authenticated successfully")
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[User]:
        """Validate session and return user"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        if not session.is_active or session.is_expired():
            # Clean up expired session
            if session_id in self.sessions:
                del self.sessions[session_id]
            return None
        
        user = self.get_user(session.user_id)
        if not user or not user.is_active:
            return None
        
        # Extend session
        session.extend_session(self.session_duration_hours)
        
        return user
    
    def logout_user(self, session_id: str) -> bool:
        """Logout user and invalidate session"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.is_active = False
        user = self.get_user(session.user_id)
        
        self._log_action(
            user_id=session.user_id,
            action="logout",
            resource="authentication",
            details={"session_id": session_id},
            success=True,
            ip_address=session.ip_address
        )
        
        # Remove session
        del self.sessions[session_id]
        
        logger.info(f"User {user.username if user else 'unknown'} logged out")
        return True
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def update_user_role(self, user_id: str, new_role: Role, updater_user_id: str) -> bool:
        """Update user role"""
        updater = self.get_user(updater_user_id)
        if not updater or not updater.has_permission(Permission.ADMIN_ACCESS):
            return False
        
        user = self.get_user(user_id)
        if not user:
            return False
        
        old_role = user.role
        user.role = new_role
        
        self._log_action(
            user_id=updater_user_id,
            action="update_user_role",
            resource=f"user:{user_id}",
            details={"old_role": old_role.value, "new_role": new_role.value},
            success=True
        )
        
        logger.info(f"Updated role for user {user.username}: {old_role.value} -> {new_role.value}")
        return True
    
    def deactivate_user(self, user_id: str, deactivator_user_id: str) -> bool:
        """Deactivate user account"""
        deactivator = self.get_user(deactivator_user_id)
        if not deactivator or not deactivator.has_permission(Permission.ADMIN_ACCESS):
            return False
        
        user = self.get_user(user_id)
        if not user:
            return False
        
        user.is_active = False
        
        # Invalidate all sessions for this user
        sessions_to_remove = [sid for sid, session in self.sessions.items() if session.user_id == user_id]
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
        
        self._log_action(
            user_id=deactivator_user_id,
            action="deactivate_user",
            resource=f"user:{user_id}",
            details={"username": user.username},
            success=True
        )
        
        logger.info(f"Deactivated user: {user.username}")
        return True
    
    def check_permission(self, session_id: str, permission: Permission) -> bool:
        """Check if session has specific permission"""
        user = self.validate_session(session_id)
        if not user:
            return False
        
        return user.has_permission(permission)
    
    def require_permission(self, session_id: str, permission: Permission) -> bool:
        """Require specific permission (logs unauthorized access)"""
        user = self.validate_session(session_id)
        if not user:
            self._log_action(
                user_id="unknown",
                action="unauthorized_access",
                resource=permission.value,
                details={"session_id": session_id},
                success=False
            )
            return False
        
        if not user.has_permission(permission):
            self._log_action(
                user_id=user.user_id,
                action="unauthorized_access",
                resource=permission.value,
                details={"username": user.username},
                success=False
            )
            return False
        
        return True
    
    def generate_api_token(self, user_id: str, expires_hours: int = 24) -> Optional[str]:
        """Generate JWT API token for user"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        payload = {
            "user_id": user_id,
            "username": user.username,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(hours=expires_hours),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        self._log_action(
            user_id=user_id,
            action="generate_api_token",
            resource="api_token",
            details={"expires_hours": expires_hours},
            success=True
        )
        
        return token
    
    def validate_api_token(self, token: str) -> Optional[User]:
        """Validate JWT API token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            
            user = self.get_user(user_id)
            if not user or not user.is_active:
                return None
            
            return user
            
        except jwt.ExpiredSignatureError:
            logger.warning("API token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid API token")
            return None
    
    def _validate_password(self, password: str) -> bool:
        """Validate password meets requirements"""
        if len(password) < self.password_min_length:
            return False
        
        # Add more password requirements as needed
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        return has_upper and has_lower and has_digit
    
    def _log_action(self, user_id: str, action: str, resource: str, details: Dict[str, Any], 
                   success: bool, ip_address: str = ""):
        """Log security action"""
        log_entry = AuditLog(
            log_id=secrets.token_hex(16),
            user_id=user_id,
            action=action,
            resource=resource,
            details=details,
            timestamp=datetime.now(),
            ip_address=ip_address,
            success=success
        )
        
        self.audit_logs.append(log_entry)
        
        # Keep only last 10000 log entries
        if len(self.audit_logs) > 10000:
            self.audit_logs = self.audit_logs[-10000:]
    
    def get_audit_logs(self, user_id: Optional[str] = None, action: Optional[str] = None, 
                      limit: int = 100) -> List[AuditLog]:
        """Get audit logs with optional filtering"""
        logs = self.audit_logs
        
        if user_id:
            logs = [log for log in logs if log.user_id == user_id]
        
        if action:
            logs = [log for log in logs if log.action == action]
        
        # Return most recent logs first
        return sorted(logs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_security_statistics(self) -> Dict[str, Any]:
        """Get security statistics"""
        total_users = len(self.users)
        active_users = len([u for u in self.users.values() if u.is_active])
        active_sessions = len([s for s in self.sessions.values() if s.is_active and not s.is_expired()])
        
        recent_logs = self.get_audit_logs(limit=1000)
        failed_logins = len([log for log in recent_logs if log.action == "login_attempt" and not log.success])
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "active_sessions": active_sessions,
            "total_audit_logs": len(self.audit_logs),
            "recent_failed_logins": failed_logins,
            "lockout_duration_minutes": self.lockout_duration_minutes,
            "max_failed_attempts": self.max_failed_attempts
        }

# Global security manager instance
_security_manager: Optional[SecurityManager] = None

def get_security_manager() -> SecurityManager:
    """Get the global security manager instance"""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager
