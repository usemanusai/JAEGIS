"""
N.L.D.S. Authentication & Authorization Implementation
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive security implementation with JWT, OAuth 2.0, MFA, and RBAC.
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import jwt
from passlib.context import CryptContext
from passlib.hash import argon2
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pyotp
import qrcode
from io import BytesIO
import base64


# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

class SecurityConfig:
    """Security configuration constants."""
    
    # JWT Configuration
    JWT_SECRET_KEY = secrets.token_urlsafe(32)
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    # Password Configuration
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_MAX_AGE_DAYS = 90
    PASSWORD_HISTORY_COUNT = 12
    
    # Account Lockout Configuration
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES = 30
    MAX_CONCURRENT_SESSIONS = 5
    
    # MFA Configuration
    MFA_ISSUER_NAME = "JAEGIS N.L.D.S."
    MFA_TOKEN_VALIDITY_WINDOW = 1


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"


class Permission(Enum):
    """Permission enumeration."""
    READ_OWN_DATA = "read_own_data"
    READ_ALL_DATA = "read_all_data"
    WRITE_OWN_DATA = "write_own_data"
    WRITE_ALL_DATA = "write_all_data"
    CREATE_REQUESTS = "create_requests"
    MANAGE_USERS = "manage_users"
    DEBUG_ACCESS = "debug_access"
    API_ACCESS = "api_access"
    EXPORT_DATA = "export_data"
    GENERATE_REPORTS = "generate_reports"


class AuthenticationMethod(Enum):
    """Authentication method enumeration."""
    PASSWORD = "password"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    MFA = "mfa"


# ============================================================================
# PASSWORD SECURITY
# ============================================================================

class PasswordSecurity:
    """Password security implementation with Argon2id."""
    
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
            argon2__memory_cost=65536,  # 64 MB
            argon2__time_cost=3,        # 3 iterations
            argon2__parallelism=1,      # 1 thread
        )
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """
        Hash password with Argon2id.
        
        Args:
            password: Plain text password
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        salted_password = f"{password}{salt}"
        hashed_password = self.pwd_context.hash(salted_password)
        
        return hashed_password, salt
    
    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Plain text password
            hashed_password: Stored password hash
            salt: Password salt
            
        Returns:
            True if password is valid
        """
        salted_password = f"{password}{salt}"
        return self.pwd_context.verify(salted_password, hashed_password)
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength against policy.
        
        Args:
            password: Password to validate
            
        Returns:
            Validation result with details
        """
        issues = []
        
        if len(password) < SecurityConfig.PASSWORD_MIN_LENGTH:
            issues.append(f"Password must be at least {SecurityConfig.PASSWORD_MIN_LENGTH} characters")
        
        if not any(c.isupper() for c in password):
            issues.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            issues.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain at least one number")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            issues.append("Password must contain at least one special character")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "strength_score": max(0, 100 - len(issues) * 20)
        }


# ============================================================================
# JWT AUTHENTICATION
# ============================================================================

class JWTAuthentication:
    """JWT-based authentication implementation."""
    
    def __init__(self):
        self.security = HTTPBearer()
        self.password_security = PasswordSecurity()
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """
        Create JWT access token.
        
        Args:
            data: Token payload data
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=SecurityConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        
        return jwt.encode(to_encode, SecurityConfig.JWT_SECRET_KEY, algorithm=SecurityConfig.JWT_ALGORITHM)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create JWT refresh token.
        
        Args:
            data: Token payload data
            
        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=SecurityConfig.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        return jwt.encode(to_encode, SecurityConfig.JWT_SECRET_KEY, algorithm=SecurityConfig.JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token payload
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            payload = jwt.decode(token, SecurityConfig.JWT_SECRET_KEY, algorithms=[SecurityConfig.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> Dict[str, Any]:
        """
        Get current authenticated user from JWT token.
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            User information from token
        """
        token = credentials.credentials
        payload = self.verify_token(token)
        
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload


# ============================================================================
# MULTI-FACTOR AUTHENTICATION
# ============================================================================

class MFAAuthentication:
    """Multi-Factor Authentication implementation."""
    
    def __init__(self):
        self.issuer_name = SecurityConfig.MFA_ISSUER_NAME
    
    def generate_secret(self) -> str:
        """
        Generate MFA secret key.
        
        Returns:
            Base32 encoded secret key
        """
        return pyotp.random_base32()
    
    def generate_qr_code(self, user_email: str, secret: str) -> str:
        """
        Generate QR code for MFA setup.
        
        Args:
            user_email: User's email address
            secret: MFA secret key
            
        Returns:
            Base64 encoded QR code image
        """
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=self.issuer_name
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    def verify_totp(self, secret: str, token: str) -> bool:
        """
        Verify TOTP token.
        
        Args:
            secret: MFA secret key
            token: TOTP token to verify
            
        Returns:
            True if token is valid
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=SecurityConfig.MFA_TOKEN_VALIDITY_WINDOW)


# ============================================================================
# ROLE-BASED ACCESS CONTROL
# ============================================================================

class RBACManager:
    """Role-Based Access Control manager."""
    
    def __init__(self):
        self.role_permissions = {
            UserRole.USER: [
                Permission.READ_OWN_DATA,
                Permission.WRITE_OWN_DATA,
                Permission.CREATE_REQUESTS
            ],
            UserRole.ADMIN: [
                Permission.READ_ALL_DATA,
                Permission.WRITE_ALL_DATA,
                Permission.MANAGE_USERS,
                Permission.CREATE_REQUESTS
            ],
            UserRole.DEVELOPER: [
                Permission.READ_OWN_DATA,
                Permission.DEBUG_ACCESS,
                Permission.API_ACCESS,
                Permission.CREATE_REQUESTS
            ],
            UserRole.ANALYST: [
                Permission.READ_ALL_DATA,
                Permission.EXPORT_DATA,
                Permission.GENERATE_REPORTS,
                Permission.CREATE_REQUESTS
            ]
        }
    
    def has_permission(self, user_role: UserRole, permission: Permission) -> bool:
        """
        Check if user role has specific permission.
        
        Args:
            user_role: User's role
            permission: Permission to check
            
        Returns:
            True if user has permission
        """
        return permission in self.role_permissions.get(user_role, [])
    
    def get_user_permissions(self, user_role: UserRole) -> List[Permission]:
        """
        Get all permissions for user role.
        
        Args:
            user_role: User's role
            
        Returns:
            List of permissions
        """
        return self.role_permissions.get(user_role, [])
    
    def require_permission(self, permission: Permission):
        """
        Decorator to require specific permission.
        
        Args:
            permission: Required permission
            
        Returns:
            Decorator function
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Get current user from JWT token
                current_user = kwargs.get('current_user')
                if not current_user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )
                
                user_role = UserRole(current_user.get('role', 'user'))
                if not self.has_permission(user_role, permission):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient permissions"
                    )
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator


# ============================================================================
# API KEY AUTHENTICATION
# ============================================================================

class APIKeyAuthentication:
    """API Key authentication implementation."""
    
    def __init__(self):
        self.password_security = PasswordSecurity()
    
    def generate_api_key(self) -> str:
        """
        Generate secure API key.
        
        Returns:
            Generated API key
        """
        return f"nlds_{secrets.token_urlsafe(32)}"
    
    def hash_api_key(self, api_key: str) -> str:
        """
        Hash API key for storage.
        
        Args:
            api_key: API key to hash
            
        Returns:
            Hashed API key
        """
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def verify_api_key(self, api_key: str, hashed_key: str) -> bool:
        """
        Verify API key against hash.
        
        Args:
            api_key: API key to verify
            hashed_key: Stored API key hash
            
        Returns:
            True if API key is valid
        """
        return hashlib.sha256(api_key.encode()).hexdigest() == hashed_key


# ============================================================================
# SECURITY UTILITIES
# ============================================================================

class SecurityUtils:
    """Security utility functions."""
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate cryptographically secure token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def constant_time_compare(a: str, b: str) -> bool:
        """Constant time string comparison to prevent timing attacks."""
        return secrets.compare_digest(a.encode(), b.encode())
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        sanitized = input_string
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
