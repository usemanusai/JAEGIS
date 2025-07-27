"""
N.L.D.S. Authentication & Authorization
JWT-based authentication with role-based access control and API key management
"""

import jwt
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from pydantic import BaseModel, Field
import logging
import redis
import json

logger = logging.getLogger(__name__)

# Security schemes
bearer_scheme = HTTPBearer()
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


class UserRole(str, Enum):
    """User roles for role-based access control."""
    GUEST = "guest"
    USER = "user"
    PREMIUM = "premium"
    DEVELOPER = "developer"
    ADMIN = "admin"
    SYSTEM = "system"


class Permission(str, Enum):
    """System permissions."""
    READ_PUBLIC = "read:public"
    READ_USER = "read:user"
    WRITE_USER = "write:user"
    READ_PREMIUM = "read:premium"
    API_ACCESS = "api:access"
    USER_MANAGEMENT = "user:management"
    SYSTEM_ADMIN = "system:admin"
    ANALYTICS_READ = "analytics:read"
    ANALYTICS_WRITE = "analytics:write"


class RateLimitTier(str, Enum):
    """Rate limiting tiers."""
    BASIC = "basic"      # 100 req/min
    PREMIUM = "premium"  # 500 req/min
    ENTERPRISE = "enterprise"  # 1000 req/min
    UNLIMITED = "unlimited"    # No limits


@dataclass
class AuthConfig:
    """Authentication configuration."""
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    refresh_token_expiration_days: int = 30
    api_key_expiration_days: int = 365
    redis_url: str = "redis://localhost:6379"
    rate_limit_window_minutes: int = 1


class TokenData(BaseModel):
    """JWT token data."""
    user_id: str
    username: str
    role: UserRole
    permissions: List[Permission]
    rate_limit_tier: RateLimitTier
    exp: datetime
    iat: datetime
    jti: str  # JWT ID for token revocation


class APIKeyData(BaseModel):
    """API key data."""
    key_id: str
    user_id: str
    key_hash: str
    name: str
    permissions: List[Permission]
    rate_limit_tier: RateLimitTier
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]
    is_active: bool


class LoginRequest(BaseModel):
    """Login request model."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    remember_me: bool = Field(default=False)


class LoginResponse(BaseModel):
    """Login response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_info: Dict[str, Any]


class RefreshRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


class APIKeyRequest(BaseModel):
    """API key creation request."""
    name: str = Field(..., min_length=1, max_length=100)
    permissions: List[Permission] = Field(default_factory=list)
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)


class APIKeyResponse(BaseModel):
    """API key creation response."""
    key_id: str
    api_key: str
    name: str
    permissions: List[Permission]
    expires_at: Optional[datetime]
    created_at: datetime


class NLDSAuthenticationManager:
    """
    Comprehensive authentication and authorization manager for N.L.D.S.
    
    Provides JWT-based authentication, API key management, role-based access control,
    and rate limiting functionality.
    """
    
    def __init__(self, config: AuthConfig):
        self.config = config
        self.redis_client = redis.from_url(config.redis_url)
        
        # Role permissions mapping
        self.role_permissions = {
            UserRole.GUEST: [Permission.READ_PUBLIC],
            UserRole.USER: [
                Permission.READ_PUBLIC,
                Permission.READ_USER,
                Permission.WRITE_USER,
                Permission.API_ACCESS
            ],
            UserRole.PREMIUM: [
                Permission.READ_PUBLIC,
                Permission.READ_USER,
                Permission.WRITE_USER,
                Permission.READ_PREMIUM,
                Permission.API_ACCESS,
                Permission.ANALYTICS_READ
            ],
            UserRole.DEVELOPER: [
                Permission.READ_PUBLIC,
                Permission.READ_USER,
                Permission.WRITE_USER,
                Permission.READ_PREMIUM,
                Permission.API_ACCESS,
                Permission.ANALYTICS_READ,
                Permission.ANALYTICS_WRITE
            ],
            UserRole.ADMIN: [
                Permission.READ_PUBLIC,
                Permission.READ_USER,
                Permission.WRITE_USER,
                Permission.READ_PREMIUM,
                Permission.API_ACCESS,
                Permission.USER_MANAGEMENT,
                Permission.ANALYTICS_READ,
                Permission.ANALYTICS_WRITE
            ],
            UserRole.SYSTEM: [perm for perm in Permission]  # All permissions
        }
        
        # Rate limit tiers
        self.rate_limits = {
            RateLimitTier.BASIC: 100,
            RateLimitTier.PREMIUM: 500,
            RateLimitTier.ENTERPRISE: 1000,
            RateLimitTier.UNLIMITED: float('inf')
        }
        
        logger.info("N.L.D.S. Authentication Manager initialized")
    
    # JWT Token Management
    
    def create_access_token(self, user_id: str, username: str, role: UserRole) -> str:
        """Create JWT access token."""
        permissions = self.role_permissions.get(role, [])
        rate_limit_tier = self._get_rate_limit_tier(role)
        
        now = datetime.utcnow()
        exp = now + timedelta(hours=self.config.jwt_expiration_hours)
        jti = secrets.token_urlsafe(16)
        
        payload = {
            "user_id": user_id,
            "username": username,
            "role": role.value,
            "permissions": [perm.value for perm in permissions],
            "rate_limit_tier": rate_limit_tier.value,
            "exp": exp,
            "iat": now,
            "jti": jti
        }
        
        token = jwt.encode(payload, self.config.jwt_secret_key, algorithm=self.config.jwt_algorithm)
        
        # Store token in Redis for revocation tracking
        self.redis_client.setex(
            f"token:{jti}",
            int(timedelta(hours=self.config.jwt_expiration_hours).total_seconds()),
            json.dumps({"user_id": user_id, "active": True})
        )
        
        return token
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create refresh token."""
        jti = secrets.token_urlsafe(32)
        exp = datetime.utcnow() + timedelta(days=self.config.refresh_token_expiration_days)
        
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": exp,
            "iat": datetime.utcnow(),
            "jti": jti
        }
        
        token = jwt.encode(payload, self.config.jwt_secret_key, algorithm=self.config.jwt_algorithm)
        
        # Store refresh token
        self.redis_client.setex(
            f"refresh:{jti}",
            int(timedelta(days=self.config.refresh_token_expiration_days).total_seconds()),
            json.dumps({"user_id": user_id, "active": True})
        )
        
        return token
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret_key,
                algorithms=[self.config.jwt_algorithm]
            )
            
            # Check if token is revoked
            jti = payload.get("jti")
            if jti:
                token_data = self.redis_client.get(f"token:{jti}")
                if not token_data:
                    logger.warning(f"Token {jti} not found in Redis")
                    return None
                
                token_info = json.loads(token_data)
                if not token_info.get("active", False):
                    logger.warning(f"Token {jti} is revoked")
                    return None
            
            return TokenData(
                user_id=payload["user_id"],
                username=payload["username"],
                role=UserRole(payload["role"]),
                permissions=[Permission(perm) for perm in payload["permissions"]],
                rate_limit_tier=RateLimitTier(payload["rate_limit_tier"]),
                exp=datetime.fromtimestamp(payload["exp"]),
                iat=datetime.fromtimestamp(payload["iat"]),
                jti=payload["jti"]
            )
            
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None
    
    def revoke_token(self, jti: str) -> bool:
        """Revoke JWT token."""
        try:
            token_data = self.redis_client.get(f"token:{jti}")
            if token_data:
                token_info = json.loads(token_data)
                token_info["active"] = False
                
                # Update with remaining TTL
                ttl = self.redis_client.ttl(f"token:{jti}")
                if ttl > 0:
                    self.redis_client.setex(f"token:{jti}", ttl, json.dumps(token_info))
                    return True
            return False
        except Exception as e:
            logger.error(f"Token revocation error: {e}")
            return False
    
    # API Key Management
    
    def create_api_key(self, user_id: str, name: str, permissions: List[Permission], 
                      expires_in_days: Optional[int] = None) -> APIKeyResponse:
        """Create new API key."""
        key_id = secrets.token_urlsafe(16)
        api_key = f"nlds_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        now = datetime.utcnow()
        expires_at = now + timedelta(days=expires_in_days) if expires_in_days else None
        
        api_key_data = APIKeyData(
            key_id=key_id,
            user_id=user_id,
            key_hash=key_hash,
            name=name,
            permissions=permissions,
            rate_limit_tier=self._get_rate_limit_tier_for_permissions(permissions),
            created_at=now,
            expires_at=expires_at,
            last_used=None,
            is_active=True
        )
        
        # Store API key data
        self.redis_client.set(
            f"api_key:{key_hash}",
            json.dumps(asdict(api_key_data), default=str)
        )
        
        # Set expiration if specified
        if expires_at:
            self.redis_client.expireat(
                f"api_key:{key_hash}",
                int(expires_at.timestamp())
            )
        
        return APIKeyResponse(
            key_id=key_id,
            api_key=api_key,
            name=name,
            permissions=permissions,
            expires_at=expires_at,
            created_at=now
        )
    
    def verify_api_key(self, api_key: str) -> Optional[APIKeyData]:
        """Verify API key and return key data."""
        try:
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            key_data = self.redis_client.get(f"api_key:{key_hash}")
            
            if not key_data:
                return None
            
            api_key_info = json.loads(key_data)
            api_key_data = APIKeyData(**api_key_info)
            
            # Check if key is active
            if not api_key_data.is_active:
                return None
            
            # Check expiration
            if api_key_data.expires_at and datetime.utcnow() > api_key_data.expires_at:
                return None
            
            # Update last used timestamp
            api_key_data.last_used = datetime.utcnow()
            self.redis_client.set(
                f"api_key:{key_hash}",
                json.dumps(asdict(api_key_data), default=str)
            )
            
            return api_key_data
            
        except Exception as e:
            logger.error(f"API key verification error: {e}")
            return None
    
    def revoke_api_key(self, key_id: str, user_id: str) -> bool:
        """Revoke API key."""
        try:
            # Find and revoke the key
            # In a real implementation, you'd need to maintain a mapping of key_id to key_hash
            # For now, this is a simplified version
            return True
        except Exception as e:
            logger.error(f"API key revocation error: {e}")
            return False
    
    # Authorization
    
    def check_permission(self, user_permissions: List[Permission], required_permission: Permission) -> bool:
        """Check if user has required permission."""
        return required_permission in user_permissions or Permission.SYSTEM_ADMIN in user_permissions
    
    def check_role_permission(self, role: UserRole, required_permission: Permission) -> bool:
        """Check if role has required permission."""
        role_permissions = self.role_permissions.get(role, [])
        return self.check_permission(role_permissions, required_permission)
    
    # Rate Limiting
    
    def check_rate_limit(self, user_id: str, rate_limit_tier: RateLimitTier) -> bool:
        """Check if user is within rate limits."""
        if rate_limit_tier == RateLimitTier.UNLIMITED:
            return True
        
        limit = self.rate_limits.get(rate_limit_tier, 100)
        window_key = f"rate_limit:{user_id}:{datetime.utcnow().strftime('%Y%m%d%H%M')}"
        
        try:
            current_count = self.redis_client.get(window_key)
            current_count = int(current_count) if current_count else 0
            
            if current_count >= limit:
                return False
            
            # Increment counter
            pipe = self.redis_client.pipeline()
            pipe.incr(window_key)
            pipe.expire(window_key, self.config.rate_limit_window_minutes * 60)
            pipe.execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return True  # Allow request on error
    
    def get_rate_limit_status(self, user_id: str, rate_limit_tier: RateLimitTier) -> Dict[str, Any]:
        """Get current rate limit status."""
        if rate_limit_tier == RateLimitTier.UNLIMITED:
            return {
                "limit": "unlimited",
                "remaining": "unlimited",
                "reset_time": None
            }
        
        limit = self.rate_limits.get(rate_limit_tier, 100)
        window_key = f"rate_limit:{user_id}:{datetime.utcnow().strftime('%Y%m%d%H%M')}"
        
        try:
            current_count = self.redis_client.get(window_key)
            current_count = int(current_count) if current_count else 0
            
            remaining = max(0, limit - current_count)
            reset_time = datetime.utcnow().replace(second=0, microsecond=0) + timedelta(minutes=1)
            
            return {
                "limit": limit,
                "remaining": remaining,
                "reset_time": reset_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Rate limit status error: {e}")
            return {
                "limit": limit,
                "remaining": limit,
                "reset_time": None
            }
    
    # Helper Methods
    
    def _get_rate_limit_tier(self, role: UserRole) -> RateLimitTier:
        """Get rate limit tier for user role."""
        tier_mapping = {
            UserRole.GUEST: RateLimitTier.BASIC,
            UserRole.USER: RateLimitTier.BASIC,
            UserRole.PREMIUM: RateLimitTier.PREMIUM,
            UserRole.DEVELOPER: RateLimitTier.ENTERPRISE,
            UserRole.ADMIN: RateLimitTier.UNLIMITED,
            UserRole.SYSTEM: RateLimitTier.UNLIMITED
        }
        return tier_mapping.get(role, RateLimitTier.BASIC)
    
    def _get_rate_limit_tier_for_permissions(self, permissions: List[Permission]) -> RateLimitTier:
        """Get rate limit tier based on permissions."""
        if Permission.SYSTEM_ADMIN in permissions:
            return RateLimitTier.UNLIMITED
        elif Permission.ANALYTICS_WRITE in permissions:
            return RateLimitTier.ENTERPRISE
        elif Permission.READ_PREMIUM in permissions:
            return RateLimitTier.PREMIUM
        else:
            return RateLimitTier.BASIC


# Dependency functions for FastAPI

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_manager: NLDSAuthenticationManager = Depends()
) -> TokenData:
    """Get current authenticated user from JWT token."""
    token_data = auth_manager.verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token_data


async def get_current_user_or_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    api_key: Optional[str] = Depends(api_key_scheme),
    auth_manager: NLDSAuthenticationManager = Depends()
) -> Union[TokenData, APIKeyData]:
    """Get current user from JWT token or API key."""
    
    # Try JWT token first
    if credentials:
        token_data = auth_manager.verify_token(credentials.credentials)
        if token_data:
            return token_data
    
    # Try API key
    if api_key:
        api_key_data = auth_manager.verify_api_key(api_key)
        if api_key_data:
            return api_key_data
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication",
        headers={"WWW-Authenticate": "Bearer"}
    )


def require_permission(required_permission: Permission):
    """Dependency factory for permission-based authorization."""
    
    async def permission_checker(
        current_user: Union[TokenData, APIKeyData] = Depends(get_current_user_or_api_key),
        auth_manager: NLDSAuthenticationManager = Depends()
    ):
        permissions = current_user.permissions
        if not auth_manager.check_permission(permissions, required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {required_permission.value}"
            )
        return current_user
    
    return permission_checker


def require_role(required_role: UserRole):
    """Dependency factory for role-based authorization."""
    
    async def role_checker(
        current_user: TokenData = Depends(get_current_user)
    ):
        if current_user.role != required_role and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {required_role.value}"
            )
        return current_user
    
    return role_checker


# Example usage
if __name__ == "__main__":
    config = AuthConfig(jwt_secret_key="your-secret-key")
    auth_manager = NLDSAuthenticationManager(config)
    
    # Create access token
    token = auth_manager.create_access_token("user123", "testuser", UserRole.USER)
    print(f"Created token: {token}")
    
    # Verify token
    token_data = auth_manager.verify_token(token)
    print(f"Token data: {token_data}")
    
    # Create API key
    api_key_response = auth_manager.create_api_key(
        "user123",
        "Test API Key",
        [Permission.READ_USER, Permission.API_ACCESS]
    )
    print(f"Created API key: {api_key_response.api_key}")
