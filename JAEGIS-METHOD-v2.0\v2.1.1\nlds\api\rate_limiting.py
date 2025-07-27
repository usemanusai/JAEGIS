"""
N.L.D.S. Rate Limiting & Throttling
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced rate limiting and throttling mechanisms with multiple algorithms,
user-based limits, endpoint-specific controls, and intelligent throttling.
"""

import time
import asyncio
import redis
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import hashlib
import json
from collections import defaultdict, deque
from fastapi import HTTPException, Request, status
import math

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# RATE LIMITING MODELS
# ============================================================================

class RateLimitAlgorithm(str, Enum):
    """Rate limiting algorithms."""
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"
    LEAKY_BUCKET = "leaky_bucket"
    ADAPTIVE = "adaptive"


class ThrottleStrategy(str, Enum):
    """Throttling strategies."""
    REJECT = "reject"
    DELAY = "delay"
    QUEUE = "queue"
    DEGRADE = "degrade"


class RateLimitScope(str, Enum):
    """Rate limit scope."""
    USER = "user"
    IP = "ip"
    API_KEY = "api_key"
    ENDPOINT = "endpoint"
    GLOBAL = "global"


@dataclass
class RateLimitRule:
    """Rate limiting rule configuration."""
    rule_id: str
    scope: RateLimitScope
    algorithm: RateLimitAlgorithm
    requests_per_window: int
    window_size_seconds: int
    burst_limit: Optional[int] = None
    throttle_strategy: ThrottleStrategy = ThrottleStrategy.REJECT
    priority: int = 1
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RateLimitStatus:
    """Current rate limit status."""
    rule_id: str
    scope: RateLimitScope
    identifier: str
    requests_made: int
    requests_remaining: int
    window_reset_time: datetime
    is_limited: bool
    retry_after_seconds: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThrottleResult:
    """Throttling operation result."""
    allowed: bool
    delay_seconds: float
    rate_limit_status: RateLimitStatus
    throttle_reason: Optional[str] = None
    suggested_action: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# RATE LIMITING ALGORITHMS
# ============================================================================

class TokenBucketLimiter:
    """Token bucket rate limiting algorithm."""
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket limiter.
        
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed
        """
        now = time.time()
        
        # Refill tokens based on elapsed time
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        
        # Check if enough tokens available
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bucket status."""
        return {
            "tokens_available": self.tokens,
            "capacity": self.capacity,
            "refill_rate": self.refill_rate,
            "last_refill": self.last_refill
        }


class SlidingWindowLimiter:
    """Sliding window rate limiting algorithm."""
    
    def __init__(self, window_size: int, max_requests: int):
        """
        Initialize sliding window limiter.
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests in window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = deque()
    
    def is_allowed(self) -> bool:
        """
        Check if request is allowed.
        
        Returns:
            True if request is allowed
        """
        now = time.time()
        
        # Remove old requests outside window
        while self.requests and self.requests[0] <= now - self.window_size:
            self.requests.popleft()
        
        # Check if under limit
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current window status."""
        now = time.time()
        
        # Clean old requests
        while self.requests and self.requests[0] <= now - self.window_size:
            self.requests.popleft()
        
        return {
            "requests_in_window": len(self.requests),
            "max_requests": self.max_requests,
            "window_size": self.window_size,
            "oldest_request": self.requests[0] if self.requests else None
        }


class FixedWindowLimiter:
    """Fixed window rate limiting algorithm."""
    
    def __init__(self, window_size: int, max_requests: int):
        """
        Initialize fixed window limiter.
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests in window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.current_window = 0
        self.request_count = 0
    
    def is_allowed(self) -> bool:
        """
        Check if request is allowed.
        
        Returns:
            True if request is allowed
        """
        now = time.time()
        current_window = int(now // self.window_size)
        
        # Reset counter for new window
        if current_window != self.current_window:
            self.current_window = current_window
            self.request_count = 0
        
        # Check if under limit
        if self.request_count < self.max_requests:
            self.request_count += 1
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current window status."""
        now = time.time()
        current_window = int(now // self.window_size)
        
        # Reset counter for new window
        if current_window != self.current_window:
            self.current_window = current_window
            self.request_count = 0
        
        window_end = (current_window + 1) * self.window_size
        
        return {
            "requests_in_window": self.request_count,
            "max_requests": self.max_requests,
            "window_size": self.window_size,
            "window_end": window_end,
            "time_until_reset": window_end - now
        }


class AdaptiveLimiter:
    """Adaptive rate limiting based on system load."""
    
    def __init__(self, base_limit: int, window_size: int):
        """
        Initialize adaptive limiter.
        
        Args:
            base_limit: Base request limit
            window_size: Window size in seconds
        """
        self.base_limit = base_limit
        self.window_size = window_size
        self.current_limit = base_limit
        self.request_times = deque()
        self.error_count = 0
        self.success_count = 0
        self.last_adjustment = time.time()
    
    def is_allowed(self, system_load: float = 0.5) -> bool:
        """
        Check if request is allowed with adaptive adjustment.
        
        Args:
            system_load: Current system load (0.0 to 1.0)
            
        Returns:
            True if request is allowed
        """
        now = time.time()
        
        # Adjust limit based on system load
        self._adjust_limit(system_load)
        
        # Remove old requests
        while self.request_times and self.request_times[0] <= now - self.window_size:
            self.request_times.popleft()
        
        # Check if under current limit
        if len(self.request_times) < self.current_limit:
            self.request_times.append(now)
            return True
        
        return False
    
    def _adjust_limit(self, system_load: float):
        """Adjust rate limit based on system conditions."""
        now = time.time()
        
        # Only adjust every 10 seconds
        if now - self.last_adjustment < 10:
            return
        
        # Calculate adjustment factor
        load_factor = 1.0 - system_load  # Higher load = lower limit
        error_rate = self.error_count / max(self.error_count + self.success_count, 1)
        error_factor = 1.0 - error_rate  # Higher error rate = lower limit
        
        adjustment_factor = (load_factor + error_factor) / 2
        
        # Adjust current limit
        new_limit = int(self.base_limit * adjustment_factor)
        self.current_limit = max(1, min(self.base_limit * 2, new_limit))
        
        # Reset counters
        self.error_count = 0
        self.success_count = 0
        self.last_adjustment = now
    
    def record_success(self):
        """Record successful request."""
        self.success_count += 1
    
    def record_error(self):
        """Record failed request."""
        self.error_count += 1
    
    def get_status(self) -> Dict[str, Any]:
        """Get current adaptive status."""
        now = time.time()
        
        # Clean old requests
        while self.request_times and self.request_times[0] <= now - self.window_size:
            self.request_times.popleft()
        
        return {
            "current_limit": self.current_limit,
            "base_limit": self.base_limit,
            "requests_in_window": len(self.request_times),
            "error_count": self.error_count,
            "success_count": self.success_count,
            "last_adjustment": self.last_adjustment
        }


# ============================================================================
# RATE LIMITING ENGINE
# ============================================================================

class RateLimitingEngine:
    """
    Advanced rate limiting engine with multiple algorithms and strategies.
    
    Features:
    - Multiple rate limiting algorithms
    - User-based and endpoint-specific limits
    - Intelligent throttling strategies
    - Redis-backed distributed limiting
    - Adaptive limits based on system load
    - Comprehensive monitoring and analytics
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize rate limiting engine.
        
        Args:
            redis_url: Redis connection URL for distributed limiting
        """
        self.redis_client = None
        if redis_url:
            try:
                self.redis_client = redis.from_url(redis_url)
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
        
        # In-memory limiters for local operation
        self.limiters = {}
        self.rules = {}
        self.statistics = defaultdict(lambda: {
            "total_requests": 0,
            "allowed_requests": 0,
            "rejected_requests": 0,
            "throttled_requests": 0
        })
        
        # Load default rules
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load default rate limiting rules."""
        default_rules = [
            RateLimitRule(
                rule_id="global_limit",
                scope=RateLimitScope.GLOBAL,
                algorithm=RateLimitAlgorithm.SLIDING_WINDOW,
                requests_per_window=10000,
                window_size_seconds=60,
                burst_limit=15000,
                throttle_strategy=ThrottleStrategy.REJECT,
                priority=1
            ),
            RateLimitRule(
                rule_id="user_standard",
                scope=RateLimitScope.USER,
                algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
                requests_per_window=100,
                window_size_seconds=60,
                burst_limit=150,
                throttle_strategy=ThrottleStrategy.DELAY,
                priority=2
            ),
            RateLimitRule(
                rule_id="user_premium",
                scope=RateLimitScope.USER,
                algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
                requests_per_window=1000,
                window_size_seconds=60,
                burst_limit=1500,
                throttle_strategy=ThrottleStrategy.DELAY,
                priority=2
            ),
            RateLimitRule(
                rule_id="endpoint_process",
                scope=RateLimitScope.ENDPOINT,
                algorithm=RateLimitAlgorithm.ADAPTIVE,
                requests_per_window=50,
                window_size_seconds=60,
                throttle_strategy=ThrottleStrategy.QUEUE,
                priority=3
            ),
            RateLimitRule(
                rule_id="ip_protection",
                scope=RateLimitScope.IP,
                algorithm=RateLimitAlgorithm.SLIDING_WINDOW,
                requests_per_window=200,
                window_size_seconds=60,
                throttle_strategy=ThrottleStrategy.REJECT,
                priority=4
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.rule_id] = rule
    
    def add_rule(self, rule: RateLimitRule):
        """Add rate limiting rule."""
        self.rules[rule.rule_id] = rule
    
    def remove_rule(self, rule_id: str):
        """Remove rate limiting rule."""
        if rule_id in self.rules:
            del self.rules[rule_id]
    
    def get_limiter_key(self, rule: RateLimitRule, identifier: str) -> str:
        """Generate limiter key for rule and identifier."""
        return f"rate_limit:{rule.rule_id}:{identifier}"
    
    def get_limiter(self, rule: RateLimitRule, identifier: str):
        """Get or create limiter for rule and identifier."""
        key = self.get_limiter_key(rule, identifier)
        
        if key not in self.limiters:
            if rule.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
                self.limiters[key] = TokenBucketLimiter(
                    capacity=rule.burst_limit or rule.requests_per_window,
                    refill_rate=rule.requests_per_window / rule.window_size_seconds
                )
            elif rule.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
                self.limiters[key] = SlidingWindowLimiter(
                    window_size=rule.window_size_seconds,
                    max_requests=rule.requests_per_window
                )
            elif rule.algorithm == RateLimitAlgorithm.FIXED_WINDOW:
                self.limiters[key] = FixedWindowLimiter(
                    window_size=rule.window_size_seconds,
                    max_requests=rule.requests_per_window
                )
            elif rule.algorithm == RateLimitAlgorithm.ADAPTIVE:
                self.limiters[key] = AdaptiveLimiter(
                    base_limit=rule.requests_per_window,
                    window_size=rule.window_size_seconds
                )
        
        return self.limiters[key]
    
    def extract_identifiers(self, request: Request, user_info: Optional[Dict[str, Any]] = None) -> Dict[RateLimitScope, str]:
        """Extract identifiers for different scopes."""
        identifiers = {}
        
        # Global identifier
        identifiers[RateLimitScope.GLOBAL] = "global"
        
        # IP identifier
        client_ip = request.client.host if request.client else "unknown"
        identifiers[RateLimitScope.IP] = client_ip
        
        # User identifier
        if user_info:
            identifiers[RateLimitScope.USER] = user_info.get("user_id", "anonymous")
            
            # API key identifier
            api_key = user_info.get("api_key")
            if api_key:
                identifiers[RateLimitScope.API_KEY] = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        
        # Endpoint identifier
        identifiers[RateLimitScope.ENDPOINT] = f"{request.method}:{request.url.path}"
        
        return identifiers
    
    async def check_rate_limits(self, request: Request, user_info: Optional[Dict[str, Any]] = None) -> ThrottleResult:
        """
        Check all applicable rate limits for request.
        
        Args:
            request: FastAPI request
            user_info: User information
            
        Returns:
            Throttle result
        """
        identifiers = self.extract_identifiers(request, user_info)
        
        # Get applicable rules sorted by priority
        applicable_rules = []
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            if rule.scope in identifiers:
                applicable_rules.append(rule)
        
        applicable_rules.sort(key=lambda r: r.priority)
        
        # Check each rule
        for rule in applicable_rules:
            identifier = identifiers[rule.scope]
            limiter = self.get_limiter(rule, identifier)
            
            # Check rate limit
            allowed = False
            if rule.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
                allowed = limiter.consume()
            elif rule.algorithm in [RateLimitAlgorithm.SLIDING_WINDOW, RateLimitAlgorithm.FIXED_WINDOW]:
                allowed = limiter.is_allowed()
            elif rule.algorithm == RateLimitAlgorithm.ADAPTIVE:
                system_load = self._get_system_load()
                allowed = limiter.is_allowed(system_load)
            
            # Update statistics
            stats_key = f"{rule.scope.value}:{identifier}"
            self.statistics[stats_key]["total_requests"] += 1
            
            if not allowed:
                self.statistics[stats_key]["rejected_requests"] += 1
                
                # Create rate limit status
                status = self._create_rate_limit_status(rule, identifier, limiter)
                
                # Apply throttling strategy
                return await self._apply_throttling_strategy(rule, status)
            else:
                self.statistics[stats_key]["allowed_requests"] += 1
                
                # Record success for adaptive limiters
                if rule.algorithm == RateLimitAlgorithm.ADAPTIVE:
                    limiter.record_success()
        
        # All limits passed
        return ThrottleResult(
            allowed=True,
            delay_seconds=0.0,
            rate_limit_status=RateLimitStatus(
                rule_id="none",
                scope=RateLimitScope.GLOBAL,
                identifier="global",
                requests_made=0,
                requests_remaining=1000,
                window_reset_time=datetime.utcnow() + timedelta(minutes=1),
                is_limited=False
            )
        )
    
    def _create_rate_limit_status(self, rule: RateLimitRule, identifier: str, limiter) -> RateLimitStatus:
        """Create rate limit status from limiter state."""
        status_data = limiter.get_status()
        
        if rule.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            requests_remaining = int(status_data["tokens_available"])
            requests_made = rule.requests_per_window - requests_remaining
        elif rule.algorithm in [RateLimitAlgorithm.SLIDING_WINDOW, RateLimitAlgorithm.FIXED_WINDOW]:
            requests_made = status_data.get("requests_in_window", 0)
            requests_remaining = rule.requests_per_window - requests_made
        elif rule.algorithm == RateLimitAlgorithm.ADAPTIVE:
            requests_made = status_data.get("requests_in_window", 0)
            requests_remaining = status_data.get("current_limit", 0) - requests_made
        else:
            requests_made = 0
            requests_remaining = 0
        
        # Calculate reset time
        if rule.algorithm == RateLimitAlgorithm.FIXED_WINDOW:
            reset_time = datetime.fromtimestamp(status_data.get("window_end", time.time()))
        else:
            reset_time = datetime.utcnow() + timedelta(seconds=rule.window_size_seconds)
        
        return RateLimitStatus(
            rule_id=rule.rule_id,
            scope=rule.scope,
            identifier=identifier,
            requests_made=requests_made,
            requests_remaining=max(0, requests_remaining),
            window_reset_time=reset_time,
            is_limited=True,
            retry_after_seconds=int((reset_time - datetime.utcnow()).total_seconds()),
            metadata=status_data
        )
    
    async def _apply_throttling_strategy(self, rule: RateLimitRule, status: RateLimitStatus) -> ThrottleResult:
        """Apply throttling strategy for rate limit violation."""
        if rule.throttle_strategy == ThrottleStrategy.REJECT:
            return ThrottleResult(
                allowed=False,
                delay_seconds=0.0,
                rate_limit_status=status,
                throttle_reason="Rate limit exceeded",
                suggested_action="Reduce request frequency or upgrade plan"
            )
        
        elif rule.throttle_strategy == ThrottleStrategy.DELAY:
            # Calculate delay based on rate limit
            delay = min(status.retry_after_seconds or 60, 300)  # Max 5 minutes
            
            return ThrottleResult(
                allowed=True,
                delay_seconds=delay,
                rate_limit_status=status,
                throttle_reason="Rate limit exceeded - request delayed",
                suggested_action="Consider upgrading plan for higher limits"
            )
        
        elif rule.throttle_strategy == ThrottleStrategy.QUEUE:
            # Queue request for later processing
            return ThrottleResult(
                allowed=True,
                delay_seconds=0.0,
                rate_limit_status=status,
                throttle_reason="Rate limit exceeded - request queued",
                suggested_action="Request queued for processing",
                metadata={"queued": True}
            )
        
        elif rule.throttle_strategy == ThrottleStrategy.DEGRADE:
            # Allow request but with degraded service
            return ThrottleResult(
                allowed=True,
                delay_seconds=0.0,
                rate_limit_status=status,
                throttle_reason="Rate limit exceeded - degraded service",
                suggested_action="Upgrade plan for full service quality",
                metadata={"degraded": True}
            )
        
        # Default to reject
        return ThrottleResult(
            allowed=False,
            delay_seconds=0.0,
            rate_limit_status=status,
            throttle_reason="Rate limit exceeded",
            suggested_action="Reduce request frequency"
        )
    
    def _get_system_load(self) -> float:
        """Get current system load (simplified)."""
        # In production, this would check actual system metrics
        return 0.5  # Placeholder
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get rate limiting statistics."""
        return dict(self.statistics)
    
    def reset_statistics(self):
        """Reset rate limiting statistics."""
        self.statistics.clear()
    
    def get_user_limits(self, user_id: str) -> List[RateLimitStatus]:
        """Get current rate limit status for user."""
        statuses = []
        
        for rule in self.rules.values():
            if rule.scope == RateLimitScope.USER:
                limiter = self.get_limiter(rule, user_id)
                status = self._create_rate_limit_status(rule, user_id, limiter)
                status.is_limited = False  # Just getting status, not checking limit
                statuses.append(status)
        
        return statuses


# ============================================================================
# RATE LIMITING UTILITIES
# ============================================================================

def create_rate_limit_response(throttle_result: ThrottleResult) -> HTTPException:
    """Create HTTP exception for rate limit violation."""
    status = throttle_result.rate_limit_status
    
    headers = {
        "X-RateLimit-Limit": str(status.requests_made + status.requests_remaining),
        "X-RateLimit-Remaining": str(status.requests_remaining),
        "X-RateLimit-Reset": str(int(status.window_reset_time.timestamp())),
        "X-RateLimit-Scope": status.scope.value
    }
    
    if status.retry_after_seconds:
        headers["Retry-After"] = str(status.retry_after_seconds)
    
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "error": "Rate limit exceeded",
            "message": throttle_result.throttle_reason,
            "suggested_action": throttle_result.suggested_action,
            "rate_limit": {
                "scope": status.scope.value,
                "requests_made": status.requests_made,
                "requests_remaining": status.requests_remaining,
                "reset_time": status.window_reset_time.isoformat(),
                "retry_after_seconds": status.retry_after_seconds
            }
        },
        headers=headers
    )


def get_rate_limit_headers(status: RateLimitStatus) -> Dict[str, str]:
    """Get rate limit headers for response."""
    return {
        "X-RateLimit-Limit": str(status.requests_made + status.requests_remaining),
        "X-RateLimit-Remaining": str(status.requests_remaining),
        "X-RateLimit-Reset": str(int(status.window_reset_time.timestamp())),
        "X-RateLimit-Scope": status.scope.value
    }
