"""
N.L.D.S. API Middleware
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Custom middleware for request logging, rate limiting, security, and monitoring.
"""

import time
import uuid
import json
import logging
from typing import Callable, Dict, Any
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from datetime import datetime
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

# Global middleware state
request_metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "average_response_time": 0.0,
    "requests_by_endpoint": {},
    "requests_by_status": {}
}


# ============================================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================================

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for comprehensive request logging and monitoring."""
    
    def __init__(self, app: ASGIApp, log_level: str = "INFO"):
        """
        Initialize request logging middleware.
        
        Args:
            app: ASGI application
            log_level: Logging level
        """
        super().__init__(app)
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger = logging.getLogger("nlds.api.requests")
        self.logger.setLevel(self.log_level)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.
        
        Args:
            request: FastAPI request
            call_next: Next middleware/endpoint
            
        Returns:
            Response from next middleware/endpoint
        """
        # Generate request ID if not present
        request_id = request.headers.get("x-request-id", str(uuid.uuid4())[:12])
        
        # Start timing
        start_time = time.time()
        
        # Extract request information
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        method = request.method
        url = str(request.url)
        path = request.url.path
        
        # Log request start
        self.logger.info(
            f"Request started - ID: {request_id}, Method: {method}, "
            f"Path: {path}, IP: {client_ip}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000
            
            # Update metrics
            await self._update_metrics(path, response.status_code, response_time)
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{response_time:.2f}ms"
            response.headers["X-API-Version"] = "2.2.0"
            
            # Log response
            self.logger.info(
                f"Request completed - ID: {request_id}, Status: {response.status_code}, "
                f"Time: {response_time:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            # Calculate response time for failed requests
            response_time = (time.time() - start_time) * 1000
            
            # Update metrics for errors
            await self._update_metrics(path, 500, response_time)
            
            # Log error
            self.logger.error(
                f"Request failed - ID: {request_id}, Error: {str(e)}, "
                f"Time: {response_time:.2f}ms"
            )
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": 500,
                        "message": "Internal server error",
                        "request_id": request_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                },
                headers={
                    "X-Request-ID": request_id,
                    "X-Response-Time": f"{response_time:.2f}ms"
                }
            )
    
    async def _update_metrics(self, path: str, status_code: int, response_time: float):
        """Update request metrics."""
        global request_metrics
        
        try:
            # Update total requests
            request_metrics["total_requests"] += 1
            
            # Update success/failure counts
            if 200 <= status_code < 400:
                request_metrics["successful_requests"] += 1
            else:
                request_metrics["failed_requests"] += 1
            
            # Update average response time
            total_requests = request_metrics["total_requests"]
            current_avg = request_metrics["average_response_time"]
            request_metrics["average_response_time"] = (
                (current_avg * (total_requests - 1) + response_time) / total_requests
            )
            
            # Update endpoint metrics
            if path not in request_metrics["requests_by_endpoint"]:
                request_metrics["requests_by_endpoint"][path] = {
                    "count": 0,
                    "average_time": 0.0,
                    "success_count": 0,
                    "error_count": 0
                }
            
            endpoint_metrics = request_metrics["requests_by_endpoint"][path]
            endpoint_metrics["count"] += 1
            
            # Update endpoint average time
            endpoint_avg = endpoint_metrics["average_time"]
            endpoint_count = endpoint_metrics["count"]
            endpoint_metrics["average_time"] = (
                (endpoint_avg * (endpoint_count - 1) + response_time) / endpoint_count
            )
            
            # Update endpoint success/error counts
            if 200 <= status_code < 400:
                endpoint_metrics["success_count"] += 1
            else:
                endpoint_metrics["error_count"] += 1
            
            # Update status code metrics
            status_key = f"{status_code // 100}xx"
            if status_key not in request_metrics["requests_by_status"]:
                request_metrics["requests_by_status"][status_key] = 0
            request_metrics["requests_by_status"][status_key] += 1
            
        except Exception as e:
            logger.error(f"Failed to update metrics: {e}")


# ============================================================================
# RATE LIMITING MIDDLEWARE
# ============================================================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for API rate limiting."""
    
    def __init__(self, app: ASGIApp, default_limit: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiting middleware.
        
        Args:
            app: ASGI application
            default_limit: Default requests per window
            window_seconds: Time window in seconds
        """
        super().__init__(app)
        self.default_limit = default_limit
        self.window_seconds = window_seconds
        self.rate_limit_store = {}
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_expired_entries())
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Check rate limits and process request.
        
        Args:
            request: FastAPI request
            call_next: Next middleware/endpoint
            
        Returns:
            Response or rate limit error
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limit
        is_allowed, rate_info = await self._check_rate_limit(client_id)
        
        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": 429,
                        "message": "Rate limit exceeded",
                        "rate_limit": rate_info["limit"],
                        "remaining": 0,
                        "reset_time": rate_info["reset_time"],
                        "timestamp": datetime.utcnow().isoformat()
                    }
                },
                headers={
                    "X-RateLimit-Limit": str(rate_info["limit"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(rate_info["reset_time"]),
                    "Retry-After": str(rate_info["retry_after"])
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset_time"])
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting."""
        # Try to get user ID from authorization header
        auth_header = request.headers.get("authorization")
        if auth_header:
            # In production, this would decode the token to get user ID
            return f"user:{auth_header[:20]}"  # Simplified
        
        # Fall back to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    async def _check_rate_limit(self, client_id: str) -> tuple[bool, Dict[str, Any]]:
        """
        Check if client is within rate limits.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Tuple of (is_allowed, rate_info)
        """
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_seconds)
        
        # Get or create rate limit entry
        if client_id not in self.rate_limit_store:
            self.rate_limit_store[client_id] = {
                "count": 0,
                "window_start": window_start,
                "limit": self.default_limit
            }
        
        rate_entry = self.rate_limit_store[client_id]
        
        # Reset count if new window
        if rate_entry["window_start"] < window_start:
            rate_entry["count"] = 0
            rate_entry["window_start"] = window_start
        
        # Check if limit exceeded
        if rate_entry["count"] >= rate_entry["limit"]:
            return False, {
                "limit": rate_entry["limit"],
                "remaining": 0,
                "reset_time": window_start + self.window_seconds,
                "retry_after": (window_start + self.window_seconds) - current_time
            }
        
        # Increment count
        rate_entry["count"] += 1
        
        return True, {
            "limit": rate_entry["limit"],
            "remaining": rate_entry["limit"] - rate_entry["count"],
            "reset_time": window_start + self.window_seconds,
            "retry_after": 0
        }
    
    async def _cleanup_expired_entries(self):
        """Clean up expired rate limit entries."""
        while True:
            try:
                current_time = int(time.time())
                expired_clients = []
                
                for client_id, rate_entry in self.rate_limit_store.items():
                    if rate_entry["window_start"] + self.window_seconds < current_time:
                        expired_clients.append(client_id)
                
                for client_id in expired_clients:
                    del self.rate_limit_store[client_id]
                
                # Clean up every minute
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Rate limit cleanup failed: {e}")
                await asyncio.sleep(60)


# ============================================================================
# SECURITY MIDDLEWARE
# ============================================================================

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for security headers and protection."""
    
    def __init__(self, app: ASGIApp):
        """
        Initialize security middleware.
        
        Args:
            app: ASGI application
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Add security headers to response.
        
        Args:
            request: FastAPI request
            call_next: Next middleware/endpoint
            
        Returns:
            Response with security headers
        """
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


# ============================================================================
# CORS MIDDLEWARE (Custom)
# ============================================================================

class CustomCORSMiddleware(BaseHTTPMiddleware):
    """Custom CORS middleware with enhanced logging."""
    
    def __init__(self, app: ASGIApp, allowed_origins: list = None):
        """
        Initialize CORS middleware.
        
        Args:
            app: ASGI application
            allowed_origins: List of allowed origins
        """
        super().__init__(app)
        self.allowed_origins = allowed_origins or ["*"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Handle CORS preflight and add CORS headers.
        
        Args:
            request: FastAPI request
            call_next: Next middleware/endpoint
            
        Returns:
            Response with CORS headers
        """
        origin = request.headers.get("origin")
        
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response()
            response.status_code = 200
        else:
            response = await call_next(request)
        
        # Add CORS headers
        if "*" in self.allowed_origins or (origin and origin in self.allowed_origins):
            response.headers["Access-Control-Allow-Origin"] = origin or "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-Request-ID"
            response.headers["Access-Control-Expose-Headers"] = "X-Request-ID, X-Response-Time, X-RateLimit-Remaining"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Max-Age"] = "86400"
        
        return response


# ============================================================================
# METRICS MIDDLEWARE
# ============================================================================

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting detailed metrics."""
    
    def __init__(self, app: ASGIApp):
        """
        Initialize metrics middleware.
        
        Args:
            app: ASGI application
        """
        super().__init__(app)
        self.metrics = {
            "requests_total": 0,
            "requests_duration_seconds": [],
            "requests_size_bytes": [],
            "response_size_bytes": [],
            "active_requests": 0
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Collect metrics for request/response.
        
        Args:
            request: FastAPI request
            call_next: Next middleware/endpoint
            
        Returns:
            Response with metrics collected
        """
        start_time = time.time()
        
        # Increment active requests
        self.metrics["active_requests"] += 1
        
        try:
            # Get request size
            request_size = int(request.headers.get("content-length", 0))
            
            # Process request
            response = await call_next(request)
            
            # Calculate metrics
            duration = time.time() - start_time
            response_size = len(response.body) if hasattr(response, 'body') else 0
            
            # Update metrics
            self.metrics["requests_total"] += 1
            self.metrics["requests_duration_seconds"].append(duration)
            self.metrics["requests_size_bytes"].append(request_size)
            self.metrics["response_size_bytes"].append(response_size)
            
            # Keep only last 1000 measurements
            for key in ["requests_duration_seconds", "requests_size_bytes", "response_size_bytes"]:
                if len(self.metrics[key]) > 1000:
                    self.metrics[key] = self.metrics[key][-1000:]
            
            return response
            
        finally:
            # Decrement active requests
            self.metrics["active_requests"] -= 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        durations = self.metrics["requests_duration_seconds"]
        request_sizes = self.metrics["requests_size_bytes"]
        response_sizes = self.metrics["response_size_bytes"]
        
        return {
            "requests_total": self.metrics["requests_total"],
            "active_requests": self.metrics["active_requests"],
            "average_duration_seconds": sum(durations) / len(durations) if durations else 0,
            "average_request_size_bytes": sum(request_sizes) / len(request_sizes) if request_sizes else 0,
            "average_response_size_bytes": sum(response_sizes) / len(response_sizes) if response_sizes else 0,
            "p95_duration_seconds": sorted(durations)[int(len(durations) * 0.95)] if durations else 0,
            "p99_duration_seconds": sorted(durations)[int(len(durations) * 0.99)] if durations else 0
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_request_metrics() -> Dict[str, Any]:
    """Get current request metrics."""
    return request_metrics.copy()


def reset_request_metrics():
    """Reset request metrics."""
    global request_metrics
    request_metrics = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "average_response_time": 0.0,
        "requests_by_endpoint": {},
        "requests_by_status": {}
    }
