"""
N.L.D.S. Authentication & Authorization
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

JWT-based authentication and role-based authorization system with
comprehensive security features and user management.
"""

import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib
import time

# Configure logging
logger = logging.getLogger(__name__)

# Security configuration
JWT_SECRET_KEY = "nlds_jwt_secret_key_2025_secure"  # Should be from environment
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Security
security = HTTPBearer()


# ============================================================================
# AUTHENTICATION MODELS
# ============================================================================

class UserRole(str, Enum):
    """User roles for authorization."""
    ADMIN = "admin"
    DEVELOPER = "developer"
    USER = "user"
    READONLY = "readonly"
    SERVICE = "service"


class Permission(str, Enum):
    """System permissions."""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    PROCESS = "process"
    ANALYZE = "analyze"
    TRANSLATE = "translate"
    JAEGIS_SUBMIT = "jaegis_submit"
    JAEGIS_STATUS = "jaegis_status"
    SYSTEM_METRICS = "system_metrics"
    CACHE_MANAGE = "cache_manage"
    USER_MANAGE = "user_manage"


class TokenType(str, Enum):
    """Token types."""
    ACCESS = "access"
    REFRESH = "refresh"
    API_KEY = "api_key"


@dataclass
class User:
    """User model."""
    user_id: str
    username: str
    email: str
    role: UserRole
    permissions: Set[Permission]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    rate_limit: int
    api_keys: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TokenData:
    """Token payload data."""
    user_id: str
    username: str
    role: UserRole
    permissions: List[str]
    token_type: TokenType
    issued_at: datetime
    expires_at: datetime
    jti: str  # JWT ID
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthResult:
    """Authentication result."""
    success: bool
    user: Optional[User]
    access_token: Optional[str]
    refresh_token: Optional[str]
    expires_in: Optional[int]
    error_message: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# ROLE-BASED PERMISSIONS
# ============================================================================

ROLE_PERMISSIONS = {
    UserRole.ADMIN: {
        Permission.READ, Permission.WRITE, Permission.ADMIN,
        Permission.PROCESS, Permission.ANALYZE, Permission.TRANSLATE,
        Permission.JAEGIS_SUBMIT, Permission.JAEGIS_STATUS,
        Permission.SYSTEM_METRICS, Permission.CACHE_MANAGE,
        Permission.USER_MANAGE
    },
    UserRole.DEVELOPER: {
        Permission.READ, Permission.WRITE, Permission.PROCESS,
        Permission.ANALYZE, Permission.TRANSLATE, Permission.JAEGIS_SUBMIT,
        Permission.JAEGIS_STATUS, Permission.SYSTEM_METRICS
    },
    UserRole.USER: {
        Permission.READ, Permission.PROCESS, Permission.ANALYZE,
        Permission.TRANSLATE, Permission.JAEGIS_STATUS
    },
    UserRole.READONLY: {
        Permission.READ, Permission.JAEGIS_STATUS
    },
    UserRole.SERVICE: {
        Permission.READ, Permission.WRITE, Permission.PROCESS,
        Permission.ANALYZE, Permission.TRANSLATE, Permission.JAEGIS_SUBMIT,
        Permission.JAEGIS_STATUS
    }
}

# Rate limits by role
ROLE_RATE_LIMITS = {
    UserRole.ADMIN: 0,  # Unlimited
    UserRole.DEVELOPER: 1000,
    UserRole.USER: 100,
    UserRole.READONLY: 50,
    UserRole.SERVICE: 5000
}


# ============================================================================
# USER DATABASE (In-memory for demo - use proper DB in production)
# ============================================================================

USERS_DB = {
    "admin_001": User(
        user_id="admin_001",
        username="admin",
        email="admin@jaegis.ai",
        role=UserRole.ADMIN,
        permissions=ROLE_PERMISSIONS[UserRole.ADMIN],
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow(),
        last_login=None,
        rate_limit=0,
        api_keys=["nlds_admin_key_001"]
    ),
    "dev_001": User(
        user_id="dev_001",
        username="developer",
        email="dev@jaegis.ai",
        role=UserRole.DEVELOPER,
        permissions=ROLE_PERMISSIONS[UserRole.DEVELOPER],
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow(),
        last_login=None,
        rate_limit=1000,
        api_keys=["nlds_dev_key_001"]
    ),
    "user_001": User(
        user_id="user_001",
        username="standard_user",
        email="user@example.com",
        role=UserRole.USER,
        permissions=ROLE_PERMISSIONS[UserRole.USER],
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow(),
        last_login=None,
        rate_limit=100,
        api_keys=["nlds_user_key_001"]
    )
}

# API Key to User mapping
API_KEY_TO_USER = {
    "nlds_admin_key_001": "admin_001",
    "nlds_dev_key_001": "dev_001",
    "nlds_user_key_001": "user_001"
}

# Active tokens (for revocation)
ACTIVE_TOKENS = set()

# Blacklisted tokens
BLACKLISTED_TOKENS = set()


# ============================================================================
# AUTHENTICATION SERVICE
# ============================================================================

class AuthenticationService:
    """Authentication and authorization service."""
    
    def __init__(self):
        """Initialize authentication service."""
        self.secret_key = JWT_SECRET_KEY
        self.algorithm = JWT_ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(self, user: User, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.
        
        Args:
            user: User object
            expires_delta: Token expiration time
            
        Returns:
            JWT access token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        jti = secrets.token_urlsafe(32)
        
        token_data = {
            "sub": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "permissions": [perm.value for perm in user.permissions],
            "token_type": TokenType.ACCESS.value,
            "iat": datetime.utcnow(),
            "exp": expire,
            "jti": jti,
            "is_admin": user.role == UserRole.ADMIN,
            "rate_limit": user.rate_limit
        }
        
        encoded_jwt = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
        
        # Track active token
        ACTIVE_TOKENS.add(jti)
        
        return encoded_jwt
    
    def create_refresh_token(self, user: User) -> str:
        """
        Create JWT refresh token.
        
        Args:
            user: User object
            
        Returns:
            JWT refresh token
        """
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        jti = secrets.token_urlsafe(32)
        
        token_data = {
            "sub": user.user_id,
            "username": user.username,
            "token_type": TokenType.REFRESH.value,
            "iat": datetime.utcnow(),
            "exp": expire,
            "jti": jti
        }
        
        encoded_jwt = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)
        
        # Track active token
        ACTIVE_TOKENS.add(jti)
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> TokenData:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Token data
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if token is blacklisted
            jti = payload.get("jti")
            if jti in BLACKLISTED_TOKENS:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked"
                )
            
            # Check if token is active
            if jti not in ACTIVE_TOKENS:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is not active"
                )
            
            # Extract token data
            user_id = payload.get("sub")
            username = payload.get("username")
            role = UserRole(payload.get("role"))
            permissions = [Permission(perm) for perm in payload.get("permissions", [])]
            token_type = TokenType(payload.get("token_type"))
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
            return TokenData(
                user_id=user_id,
                username=username,
                role=role,
                permissions=[perm.value for perm in permissions],
                token_type=token_type,
                issued_at=datetime.fromtimestamp(payload.get("iat")),
                expires_at=datetime.fromtimestamp(payload.get("exp")),
                jti=jti,
                metadata=payload
            )
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
    
    def authenticate_user(self, username: str, password: str) -> AuthResult:
        """
        Authenticate user with username and password.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Authentication result
        """
        # Find user (simplified - in production, use proper password hashing)
        user = None
        for u in USERS_DB.values():
            if u.username == username:
                user = u
                break
        
        if not user or not user.is_active:
            return AuthResult(
                success=False,
                user=None,
                access_token=None,
                refresh_token=None,
                expires_in=None,
                error_message="Invalid credentials or inactive user"
            )
        
        # In production, verify password hash
        # For demo, accept any password for existing users
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        # Create tokens
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)
        
        return AuthResult(
            success=True,
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.access_token_expire_minutes * 60,
            error_message=None,
            metadata={
                "login_time": datetime.utcnow().isoformat(),
                "user_agent": "api_client"
            }
        )
    
    def authenticate_api_key(self, api_key: str) -> AuthResult:
        """
        Authenticate user with API key.
        
        Args:
            api_key: API key
            
        Returns:
            Authentication result
        """
        if api_key not in API_KEY_TO_USER:
            return AuthResult(
                success=False,
                user=None,
                access_token=None,
                refresh_token=None,
                expires_in=None,
                error_message="Invalid API key"
            )
        
        user_id = API_KEY_TO_USER[api_key]
        user = USERS_DB.get(user_id)
        
        if not user or not user.is_active:
            return AuthResult(
                success=False,
                user=None,
                access_token=None,
                refresh_token=None,
                expires_in=None,
                error_message="User not found or inactive"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        return AuthResult(
            success=True,
            user=user,
            access_token=None,  # API key auth doesn't need JWT
            refresh_token=None,
            expires_in=None,
            error_message=None,
            metadata={
                "auth_method": "api_key",
                "api_key_hash": hashlib.sha256(api_key.encode()).hexdigest()[:16]
            }
        )
    
    def refresh_access_token(self, refresh_token: str) -> AuthResult:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Authentication result with new access token
        """
        try:
            token_data = self.verify_token(refresh_token)
            
            if token_data.token_type != TokenType.REFRESH:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type for refresh"
                )
            
            user = USERS_DB.get(token_data.user_id)
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive"
                )
            
            # Create new access token
            new_access_token = self.create_access_token(user)
            
            return AuthResult(
                success=True,
                user=user,
                access_token=new_access_token,
                refresh_token=refresh_token,  # Keep same refresh token
                expires_in=self.access_token_expire_minutes * 60,
                error_message=None,
                metadata={
                    "refresh_time": datetime.utcnow().isoformat()
                }
            )
            
        except HTTPException as e:
            return AuthResult(
                success=False,
                user=None,
                access_token=None,
                refresh_token=None,
                expires_in=None,
                error_message=e.detail
            )
    
    def revoke_token(self, token: str) -> bool:
        """
        Revoke a token.
        
        Args:
            token: Token to revoke
            
        Returns:
            True if successful
        """
        try:
            token_data = self.verify_token(token)
            
            # Add to blacklist
            BLACKLISTED_TOKENS.add(token_data.jti)
            
            # Remove from active tokens
            ACTIVE_TOKENS.discard(token_data.jti)
            
            return True
            
        except HTTPException:
            return False
    
    def check_permission(self, user: User, required_permission: Permission) -> bool:
        """
        Check if user has required permission.
        
        Args:
            user: User object
            required_permission: Required permission
            
        Returns:
            True if user has permission
        """
        return required_permission in user.permissions or user.role == UserRole.ADMIN


# ============================================================================
# AUTHENTICATION DEPENDENCIES
# ============================================================================

# Global auth service
auth_service = AuthenticationService()


async def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Get current user from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    token_data = auth_service.verify_token(token)
    
    user = USERS_DB.get(token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    
    return user


async def get_current_user_from_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Get current user from API key.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If authentication fails
    """
    api_key = credentials.credentials
    auth_result = auth_service.authenticate_api_key(api_key)
    
    if not auth_result.success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=auth_result.error_message or "Authentication failed"
        )
    
    return auth_result.user


def require_permission(permission: Permission):
    """
    Create dependency that requires specific permission.
    
    Args:
        permission: Required permission
        
    Returns:
        Dependency function
    """
    async def permission_dependency(current_user: User = Depends(get_current_user_from_api_key)):
        if not auth_service.check_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission.value}' required"
            )
        return current_user
    
    return permission_dependency


def require_role(role: UserRole):
    """
    Create dependency that requires specific role.
    
    Args:
        role: Required role
        
    Returns:
        Dependency function
    """
    async def role_dependency(current_user: User = Depends(get_current_user_from_api_key)):
        if current_user.role != role and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role.value}' required"
            )
        return current_user
    
    return role_dependency


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def generate_api_key() -> str:
    """Generate secure API key."""
    return f"nlds_{secrets.token_urlsafe(32)}"


def create_user(username: str, email: str, password: str, role: UserRole) -> User:
    """
    Create new user.
    
    Args:
        username: Username
        email: Email address
        password: Password
        role: User role
        
    Returns:
        Created user
    """
    user_id = f"user_{secrets.token_urlsafe(8)}"
    api_key = generate_api_key()
    
    user = User(
        user_id=user_id,
        username=username,
        email=email,
        role=role,
        permissions=ROLE_PERMISSIONS[role],
        is_active=True,
        is_verified=False,
        created_at=datetime.utcnow(),
        last_login=None,
        rate_limit=ROLE_RATE_LIMITS[role],
        api_keys=[api_key]
    )
    
    # Store user
    USERS_DB[user_id] = user
    API_KEY_TO_USER[api_key] = user_id
    
    return user


def get_user_by_username(username: str) -> Optional[User]:
    """Get user by username."""
    for user in USERS_DB.values():
        if user.username == username:
            return user
    return None


def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    for user in USERS_DB.values():
        if user.email == email:
            return user
    return None


# ============================================================================
# COMMON DEPENDENCIES
# ============================================================================

# Authentication dependencies
current_user = Depends(get_current_user_from_api_key)
admin_user = Depends(require_role(UserRole.ADMIN))
developer_user = Depends(require_role(UserRole.DEVELOPER))

# Permission dependencies
read_permission = Depends(require_permission(Permission.READ))
write_permission = Depends(require_permission(Permission.WRITE))
admin_permission = Depends(require_permission(Permission.ADMIN))
process_permission = Depends(require_permission(Permission.PROCESS))
analyze_permission = Depends(require_permission(Permission.ANALYZE))
translate_permission = Depends(require_permission(Permission.TRANSLATE))
jaegis_submit_permission = Depends(require_permission(Permission.JAEGIS_SUBMIT))
system_metrics_permission = Depends(require_permission(Permission.SYSTEM_METRICS))
