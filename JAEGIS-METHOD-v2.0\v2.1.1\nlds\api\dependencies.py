"""
N.L.D.S. API Dependencies
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

FastAPI dependencies for authentication, rate limiting, and request validation.
"""

import jwt
import redis
import time
from fastapi import HTTPException, Security, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional, Any
import logging
from datetime import datetime, timedelta
import hashlib
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Redis client for rate limiting (would be configured in production)
redis_client = None

# In-memory stores for development (replace with proper storage in production)
API_KEYS = {
    "nlds_dev_key_001": {
        "user_id": "dev_user_001",
        "username": "developer",
        "is_admin": True,
        "rate_limit": 1000,
        "permissions": ["read", "write", "admin"]
    },
    "nlds_user_key_001": {
        "user_id": "user_001",
        "username": "standard_user",
        "is_admin": False,
        "rate_limit": 100,
        "permissions": ["read", "write"]
    }
}

RATE_LIMIT_STORE = {}


# ============================================================================
# AUTHENTICATION DEPENDENCIES
# ============================================================================

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Verify API key from Authorization header.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        User information dictionary
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        token = credentials.credentials
        
        # Check if token exists in API keys
        if token not in API_KEYS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_info = API_KEYS[token].copy()
        user_info["api_key"] = token
        user_info["authenticated_at"] = datetime.utcnow()
        
        return user_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API key verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Verify JWT token from Authorization header.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        User information from JWT payload
        
    Raises:
        HTTPException: If token verification fails
    """
    try:
        token = credentials.credentials
        
        # JWT secret key (should be from environment in production)
        SECRET_KEY = "nlds_jwt_secret_key_2025"
        ALGORITHM = "HS256"
        
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user information
        user_id = payload.get("sub")
        username = payload.get("username")
        permissions = payload.get("permissions", [])
        is_admin = payload.get("is_admin", False)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Check token expiration
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        
        return {
            "user_id": user_id,
            "username": username,
            "permissions": permissions,
            "is_admin": is_admin,
            "token_payload": payload,
            "authenticated_at": datetime.utcnow()
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(user_info: Dict[str, Any] = Depends(verify_api_key)) -> Dict[str, Any]:
    """
    Get current authenticated user information.
    
    Args:
        user_info: User information from authentication
        
    Returns:
        Current user information
    """
    return user_info


async def get_admin_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Verify user has admin permissions.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Admin user information
        
    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


# ============================================================================
# RATE LIMITING DEPENDENCIES
# ============================================================================

class RateLimiter:
    """Rate limiter for API endpoints."""
    
    def __init__(self, requests_per_minute: int = 100, window_size: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute
            window_size: Time window in seconds
        """
        self.requests_per_minute = requests_per_minute
        self.window_size = window_size
    
    async def __call__(self, request: Request, current_user: Dict[str, Any] = Depends(get_current_user)):
        """
        Check rate limit for current user.
        
        Args:
            request: FastAPI request object
            current_user: Current authenticated user
            
        Raises:
            HTTPException: If rate limit exceeded
        """
        try:
            user_id = current_user.get("user_id")
            user_rate_limit = current_user.get("rate_limit", self.requests_per_minute)
            
            # Create rate limit key
            current_time = int(time.time())
            window_start = current_time - (current_time % self.window_size)
            rate_limit_key = f"rate_limit:{user_id}:{window_start}"
            
            # Check current request count
            if rate_limit_key not in RATE_LIMIT_STORE:
                RATE_LIMIT_STORE[rate_limit_key] = {
                    "count": 0,
                    "window_start": window_start,
                    "expires_at": window_start + self.window_size
                }
            
            # Clean up expired entries
            current_time = int(time.time())
            expired_keys = [
                key for key, data in RATE_LIMIT_STORE.items()
                if data["expires_at"] < current_time
            ]
            for key in expired_keys:
                del RATE_LIMIT_STORE[key]
            
            # Check rate limit
            rate_data = RATE_LIMIT_STORE[rate_limit_key]
            if rate_data["count"] >= user_rate_limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {user_rate_limit} requests per minute",
                    headers={
                        "X-RateLimit-Limit": str(user_rate_limit),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(rate_data["expires_at"])
                    }
                )
            
            # Increment request count
            rate_data["count"] += 1
            
            # Add rate limit headers to response (would be done in middleware)
            remaining = user_rate_limit - rate_data["count"]
            
            return {
                "rate_limit": user_rate_limit,
                "remaining": remaining,
                "reset_time": rate_data["expires_at"]
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Rate limiting failed: {e}")
            # Allow request to proceed if rate limiting fails
            return {"rate_limit": "unknown", "remaining": "unknown"}


async def get_rate_limiter(requests_per_minute: int = 100) -> RateLimiter:
    """
    Get rate limiter dependency.
    
    Args:
        requests_per_minute: Requests per minute limit
        
    Returns:
        Rate limiter instance
    """
    return RateLimiter(requests_per_minute)


# ============================================================================
# PERMISSION DEPENDENCIES
# ============================================================================

def require_permission(permission: str):
    """
    Create dependency that requires specific permission.
    
    Args:
        permission: Required permission
        
    Returns:
        Dependency function
    """
    async def permission_dependency(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_permissions = current_user.get("permissions", [])
        
        if permission not in user_permissions and not current_user.get("is_admin", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        
        return current_user
    
    return permission_dependency


def require_any_permission(permissions: list):
    """
    Create dependency that requires any of the specified permissions.
    
    Args:
        permissions: List of acceptable permissions
        
    Returns:
        Dependency function
    """
    async def permission_dependency(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_permissions = current_user.get("permissions", [])
        
        has_permission = any(perm in user_permissions for perm in permissions)
        
        if not has_permission and not current_user.get("is_admin", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of these permissions required: {', '.join(permissions)}"
            )
        
        return current_user
    
    return permission_dependency


# ============================================================================
# REQUEST VALIDATION DEPENDENCIES
# ============================================================================

async def validate_request_size(request: Request):
    """
    Validate request size.
    
    Args:
        request: FastAPI request object
        
    Raises:
        HTTPException: If request too large
    """
    try:
        content_length = request.headers.get("content-length")
        
        if content_length:
            content_length = int(content_length)
            max_size = 1024 * 1024  # 1MB limit
            
            if content_length > max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Request too large: {content_length} bytes (max: {max_size} bytes)"
                )
    
    except ValueError:
        # Invalid content-length header
        pass
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Request size validation failed: {e}")


async def validate_content_type(request: Request):
    """
    Validate request content type.
    
    Args:
        request: FastAPI request object
        
    Raises:
        HTTPException: If invalid content type
    """
    try:
        content_type = request.headers.get("content-type", "")
        
        # Allow JSON and form data
        allowed_types = [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ]
        
        if request.method in ["POST", "PUT", "PATCH"]:
            if not any(allowed_type in content_type for allowed_type in allowed_types):
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=f"Unsupported content type: {content_type}"
                )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content type validation failed: {e}")


# ============================================================================
# UTILITY DEPENDENCIES
# ============================================================================

async def get_request_id(request: Request) -> str:
    """
    Get or generate request ID.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Request ID
    """
    # Check for existing request ID in headers
    request_id = request.headers.get("x-request-id")
    
    if not request_id:
        # Generate new request ID
        timestamp = str(int(time.time() * 1000))
        client_ip = request.client.host if request.client else "unknown"
        request_id = hashlib.md5(f"{timestamp}:{client_ip}".encode()).hexdigest()[:12]
    
    return request_id


async def get_client_info(request: Request) -> Dict[str, Any]:
    """
    Get client information from request.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Client information dictionary
    """
    return {
        "ip_address": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "referer": request.headers.get("referer"),
        "request_id": await get_request_id(request),
        "timestamp": datetime.utcnow()
    }


# ============================================================================
# JWT UTILITIES
# ============================================================================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Token payload data
        expires_delta: Token expiration time
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    
    SECRET_KEY = "nlds_jwt_secret_key_2025"
    ALGORITHM = "HS256"
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token_signature(token: str) -> bool:
    """
    Verify JWT token signature without decoding.
    
    Args:
        token: JWT token
        
    Returns:
        True if signature is valid
    """
    try:
        SECRET_KEY = "nlds_jwt_secret_key_2025"
        ALGORITHM = "HS256"
        
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.JWTError:
        return False


# ============================================================================
# DEPENDENCY COMBINATIONS
# ============================================================================

# Common dependency combinations
authenticated_user = Depends(get_current_user)
admin_user = Depends(get_admin_user)
rate_limited = Depends(get_rate_limiter())
read_permission = Depends(require_permission("read"))
write_permission = Depends(require_permission("write"))
admin_permission = Depends(require_permission("admin"))

# Combined dependencies
authenticated_and_rate_limited = [authenticated_user, rate_limited]
admin_and_rate_limited = [admin_user, rate_limited]
