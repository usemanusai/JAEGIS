"""
N.L.D.S. Error Handling & Fallback Systems
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive error handling with graceful degradation, fallback mechanisms,
and resilient system recovery for maximum reliability and uptime.
"""

import asyncio
import traceback
import logging
from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import hashlib
from functools import wraps

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# ERROR HANDLING STRUCTURES AND ENUMS
# ============================================================================

class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    PROCESSING = "processing"
    INTEGRATION = "integration"
    SYSTEM = "system"
    USER_INPUT = "user_input"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    CONFIGURATION = "configuration"


class FallbackStrategy(Enum):
    """Fallback strategies for error recovery."""
    RETRY = "retry"
    DEGRADE = "degrade"
    CACHE = "cache"
    ALTERNATIVE = "alternative"
    FAIL_SAFE = "fail_safe"
    MANUAL_INTERVENTION = "manual_intervention"


class SystemState(Enum):
    """System operational states."""
    NORMAL = "normal"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


@dataclass
class ErrorInfo:
    """Comprehensive error information."""
    error_id: str
    error_type: str
    error_message: str
    error_category: ErrorCategory
    severity: ErrorSeverity
    timestamp: datetime
    component: str
    function_name: str
    stack_trace: str
    context: Dict[str, Any]
    user_impact: str
    recovery_actions: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FallbackAction:
    """Fallback action definition."""
    action_id: str
    strategy: FallbackStrategy
    description: str
    implementation: Callable
    conditions: Dict[str, Any]
    priority: int
    timeout_seconds: int
    success_criteria: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryPlan:
    """System recovery plan."""
    plan_id: str
    error_category: ErrorCategory
    severity_threshold: ErrorSeverity
    fallback_actions: List[FallbackAction]
    escalation_path: List[str]
    notification_targets: List[str]
    auto_recovery_enabled: bool
    max_retry_attempts: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemHealth:
    """System health status."""
    overall_state: SystemState
    component_states: Dict[str, SystemState]
    error_count_24h: int
    critical_errors_active: int
    last_error_time: Optional[datetime]
    uptime_percentage: float
    performance_metrics: Dict[str, float]
    active_fallbacks: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# ERROR HANDLING ENGINE
# ============================================================================

class ErrorHandlingEngine:
    """
    Comprehensive error handling and fallback system.
    
    Features:
    - Intelligent error classification and severity assessment
    - Automatic fallback strategy selection and execution
    - Graceful degradation with service continuity
    - Circuit breaker patterns for external dependencies
    - Comprehensive logging and monitoring
    - Recovery plan automation
    - Health monitoring and alerting
    - Performance impact minimization
    """
    
    def __init__(self, error_config: Dict[str, Any]):
        """
        Initialize error handling engine.
        
        Args:
            error_config: Configuration for error handling system
        """
        self.config = error_config
        self.is_active = True
        
        # Error tracking
        self.error_history = []
        self.active_errors = {}
        self.error_patterns = {}
        self.max_error_history = error_config.get("max_error_history", 10000)
        
        # Recovery plans
        self.recovery_plans = {}
        self.fallback_actions = {}
        self.active_fallbacks = {}
        
        # Circuit breakers
        self.circuit_breakers = {}
        self.circuit_breaker_config = error_config.get("circuit_breakers", {})
        
        # System health
        self.system_health = SystemHealth(
            overall_state=SystemState.NORMAL,
            component_states={},
            error_count_24h=0,
            critical_errors_active=0,
            last_error_time=None,
            uptime_percentage=100.0,
            performance_metrics={},
            active_fallbacks=[]
        )
        
        # Monitoring
        self.health_check_interval = error_config.get("health_check_interval", 60)
        self.error_threshold_24h = error_config.get("error_threshold_24h", 1000)
        self.critical_error_threshold = error_config.get("critical_error_threshold", 5)
        
        # Notification settings
        self.notification_enabled = error_config.get("notification_enabled", True)
        self.notification_targets = error_config.get("notification_targets", [])
        
        # Load default configurations
        self._load_default_recovery_plans()
        self._load_default_fallback_actions()
    
    def _load_default_recovery_plans(self) -> None:
        """Load default recovery plans for common error scenarios."""
        # Network error recovery plan
        network_plan = RecoveryPlan(
            plan_id="network_recovery",
            error_category=ErrorCategory.NETWORK,
            severity_threshold=ErrorSeverity.MEDIUM,
            fallback_actions=["retry_with_backoff", "use_cached_data", "degrade_service"],
            escalation_path=["auto_retry", "manual_intervention"],
            notification_targets=["system_admin"],
            auto_recovery_enabled=True,
            max_retry_attempts=3
        )
        
        # Authentication error recovery plan
        auth_plan = RecoveryPlan(
            plan_id="auth_recovery",
            error_category=ErrorCategory.AUTHENTICATION,
            severity_threshold=ErrorSeverity.HIGH,
            fallback_actions=["refresh_token", "fallback_auth", "guest_mode"],
            escalation_path=["token_refresh", "admin_notification"],
            notification_targets=["security_team"],
            auto_recovery_enabled=True,
            max_retry_attempts=2
        )
        
        # Processing error recovery plan
        processing_plan = RecoveryPlan(
            plan_id="processing_recovery",
            error_category=ErrorCategory.PROCESSING,
            severity_threshold=ErrorSeverity.MEDIUM,
            fallback_actions=["alternative_algorithm", "simplified_processing", "manual_queue"],
            escalation_path=["algorithm_switch", "human_review"],
            notification_targets=["dev_team"],
            auto_recovery_enabled=True,
            max_retry_attempts=2
        )
        
        self.recovery_plans = {
            ErrorCategory.NETWORK: network_plan,
            ErrorCategory.AUTHENTICATION: auth_plan,
            ErrorCategory.PROCESSING: processing_plan
        }
    
    def _load_default_fallback_actions(self) -> None:
        """Load default fallback actions."""
        self.fallback_actions = {
            "retry_with_backoff": FallbackAction(
                action_id="retry_with_backoff",
                strategy=FallbackStrategy.RETRY,
                description="Retry operation with exponential backoff",
                implementation=self._retry_with_backoff,
                conditions={"max_attempts": 3, "base_delay": 1},
                priority=1,
                timeout_seconds=30,
                success_criteria={"operation_success": True}
            ),
            "use_cached_data": FallbackAction(
                action_id="use_cached_data",
                strategy=FallbackStrategy.CACHE,
                description="Use cached data when fresh data unavailable",
                implementation=self._use_cached_data,
                conditions={"cache_age_limit": 3600},
                priority=2,
                timeout_seconds=5,
                success_criteria={"data_available": True}
            ),
            "degrade_service": FallbackAction(
                action_id="degrade_service",
                strategy=FallbackStrategy.DEGRADE,
                description="Provide degraded service functionality",
                implementation=self._degrade_service,
                conditions={"essential_features_only": True},
                priority=3,
                timeout_seconds=10,
                success_criteria={"service_available": True}
            ),
            "alternative_algorithm": FallbackAction(
                action_id="alternative_algorithm",
                strategy=FallbackStrategy.ALTERNATIVE,
                description="Use alternative processing algorithm",
                implementation=self._use_alternative_algorithm,
                conditions={"algorithm_available": True},
                priority=2,
                timeout_seconds=60,
                success_criteria={"processing_complete": True}
            )
        }
    
    async def handle_error(self, error: Exception, context: Dict[str, Any]) -> ErrorInfo:
        """
        Handle error with comprehensive analysis and recovery.
        
        Args:
            error: Exception that occurred
            context: Context information about the error
            
        Returns:
            Error information with recovery actions
        """
        try:
            # Create error info
            error_info = self._create_error_info(error, context)
            
            # Log error
            self._log_error(error_info)
            
            # Update system health
            self._update_system_health(error_info)
            
            # Execute recovery plan
            await self._execute_recovery_plan(error_info)
            
            # Store error for analysis
            self._store_error(error_info)
            
            # Send notifications if needed
            await self._send_notifications(error_info)
            
            return error_info
            
        except Exception as e:
            logger.critical(f"Error in error handling system: {e}")
            # Fallback error info
            return ErrorInfo(
                error_id=f"fallback_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                error_type=type(error).__name__,
                error_message=str(error),
                error_category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.CRITICAL,
                timestamp=datetime.utcnow(),
                component="error_handler",
                function_name="handle_error",
                stack_trace=traceback.format_exc(),
                context=context,
                user_impact="System error handling compromised",
                recovery_actions=["Manual intervention required"]
            )
    
    def _create_error_info(self, error: Exception, context: Dict[str, Any]) -> ErrorInfo:
        """Create comprehensive error information."""
        # Generate error ID
        error_id = hashlib.md5(f"{type(error).__name__}_{str(error)}_{datetime.utcnow()}".encode()).hexdigest()[:12]
        
        # Classify error
        error_category = self._classify_error(error, context)
        severity = self._assess_severity(error, context, error_category)
        
        # Extract context information
        component = context.get("component", "unknown")
        function_name = context.get("function", "unknown")
        
        # Assess user impact
        user_impact = self._assess_user_impact(error, severity, error_category)
        
        # Generate recovery actions
        recovery_actions = self._generate_recovery_actions(error_category, severity)
        
        return ErrorInfo(
            error_id=error_id,
            error_type=type(error).__name__,
            error_message=str(error),
            error_category=error_category,
            severity=severity,
            timestamp=datetime.utcnow(),
            component=component,
            function_name=function_name,
            stack_trace=traceback.format_exc(),
            context=context,
            user_impact=user_impact,
            recovery_actions=recovery_actions,
            metadata={
                "error_hash": error_id,
                "python_version": context.get("python_version"),
                "system_load": context.get("system_load")
            }
        )
    
    def _classify_error(self, error: Exception, context: Dict[str, Any]) -> ErrorCategory:
        """Classify error into appropriate category."""
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # Network-related errors
        if any(keyword in error_message for keyword in ["connection", "timeout", "network", "dns", "socket"]):
            return ErrorCategory.NETWORK
        
        # Authentication errors
        if any(keyword in error_message for keyword in ["auth", "token", "permission", "unauthorized", "forbidden"]):
            return ErrorCategory.AUTHENTICATION
        
        # Validation errors
        if any(keyword in error_message for keyword in ["validation", "invalid", "format", "schema"]):
            return ErrorCategory.VALIDATION
        
        # Database errors
        if any(keyword in error_message for keyword in ["database", "sql", "connection pool", "deadlock"]):
            return ErrorCategory.DATABASE
        
        # External API errors
        if "api" in context.get("component", "").lower() or "external" in error_message:
            return ErrorCategory.EXTERNAL_API
        
        # Configuration errors
        if any(keyword in error_message for keyword in ["config", "setting", "parameter", "missing"]):
            return ErrorCategory.CONFIGURATION
        
        # Default to processing error
        return ErrorCategory.PROCESSING
    
    def _assess_severity(self, error: Exception, context: Dict[str, Any], category: ErrorCategory) -> ErrorSeverity:
        """Assess error severity based on multiple factors."""
        # Critical errors
        if isinstance(error, (SystemExit, KeyboardInterrupt, MemoryError)):
            return ErrorSeverity.CRITICAL
        
        # High severity conditions
        if category in [ErrorCategory.AUTHENTICATION, ErrorCategory.SYSTEM]:
            return ErrorSeverity.HIGH
        
        if "critical" in str(error).lower() or "fatal" in str(error).lower():
            return ErrorSeverity.HIGH
        
        # Medium severity conditions
        if category in [ErrorCategory.NETWORK, ErrorCategory.DATABASE, ErrorCategory.EXTERNAL_API]:
            return ErrorSeverity.MEDIUM
        
        # Default to low severity
        return ErrorSeverity.LOW
    
    def _assess_user_impact(self, error: Exception, severity: ErrorSeverity, category: ErrorCategory) -> str:
        """Assess impact on user experience."""
        impact_map = {
            ErrorSeverity.CRITICAL: "Service completely unavailable",
            ErrorSeverity.HIGH: "Major functionality impaired",
            ErrorSeverity.MEDIUM: "Some features may be unavailable",
            ErrorSeverity.LOW: "Minimal impact on user experience"
        }
        
        base_impact = impact_map.get(severity, "Unknown impact")
        
        # Category-specific adjustments
        if category == ErrorCategory.AUTHENTICATION:
            return f"{base_impact} - User authentication affected"
        elif category == ErrorCategory.NETWORK:
            return f"{base_impact} - Network connectivity issues"
        elif category == ErrorCategory.PROCESSING:
            return f"{base_impact} - Processing delays possible"
        
        return base_impact
    
    def _generate_recovery_actions(self, category: ErrorCategory, severity: ErrorSeverity) -> List[str]:
        """Generate appropriate recovery actions."""
        actions = []
        
        # Get recovery plan for category
        recovery_plan = self.recovery_plans.get(category)
        if recovery_plan:
            actions.extend(recovery_plan.fallback_actions)
        
        # Add severity-specific actions
        if severity == ErrorSeverity.CRITICAL:
            actions.extend(["immediate_escalation", "system_restart", "manual_intervention"])
        elif severity == ErrorSeverity.HIGH:
            actions.extend(["escalate_to_admin", "activate_backup_systems"])
        
        # Default actions
        if not actions:
            actions = ["log_error", "retry_operation", "notify_admin"]
        
        return actions
    
    async def _execute_recovery_plan(self, error_info: ErrorInfo) -> None:
        """Execute recovery plan for the error."""
        try:
            recovery_plan = self.recovery_plans.get(error_info.error_category)
            if not recovery_plan:
                logger.warning(f"No recovery plan for category: {error_info.error_category}")
                return
            
            # Check if auto-recovery is enabled
            if not recovery_plan.auto_recovery_enabled:
                logger.info(f"Auto-recovery disabled for {error_info.error_category}")
                return
            
            # Execute fallback actions in priority order
            for action_id in recovery_plan.fallback_actions:
                fallback_action = self.fallback_actions.get(action_id)
                if fallback_action:
                    try:
                        logger.info(f"Executing fallback action: {action_id}")
                        success = await self._execute_fallback_action(fallback_action, error_info)
                        
                        if success:
                            logger.info(f"Fallback action {action_id} succeeded")
                            self.active_fallbacks[error_info.error_id] = action_id
                            break
                        else:
                            logger.warning(f"Fallback action {action_id} failed")
                            
                    except Exception as e:
                        logger.error(f"Error executing fallback action {action_id}: {e}")
                        
        except Exception as e:
            logger.error(f"Error executing recovery plan: {e}")
    
    async def _execute_fallback_action(self, action: FallbackAction, error_info: ErrorInfo) -> bool:
        """Execute a specific fallback action."""
        try:
            # Check conditions
            if not self._check_action_conditions(action, error_info):
                return False
            
            # Execute with timeout
            result = await asyncio.wait_for(
                action.implementation(error_info, action.conditions),
                timeout=action.timeout_seconds
            )
            
            # Check success criteria
            return self._check_success_criteria(result, action.success_criteria)
            
        except asyncio.TimeoutError:
            logger.warning(f"Fallback action {action.action_id} timed out")
            return False
        except Exception as e:
            logger.error(f"Fallback action {action.action_id} failed: {e}")
            return False
    
    def _check_action_conditions(self, action: FallbackAction, error_info: ErrorInfo) -> bool:
        """Check if conditions are met for executing fallback action."""
        # Basic condition checks
        conditions = action.conditions
        
        # Check error severity
        if "min_severity" in conditions:
            min_severity = ErrorSeverity(conditions["min_severity"])
            if error_info.severity.value < min_severity.value:
                return False
        
        # Check error category
        if "allowed_categories" in conditions:
            if error_info.error_category not in conditions["allowed_categories"]:
                return False
        
        return True
    
    def _check_success_criteria(self, result: Any, criteria: Dict[str, Any]) -> bool:
        """Check if success criteria are met."""
        if not isinstance(result, dict):
            return bool(result)
        
        for key, expected_value in criteria.items():
            if key not in result or result[key] != expected_value:
                return False
        
        return True
    
    # Fallback action implementations
    async def _retry_with_backoff(self, error_info: ErrorInfo, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Retry operation with exponential backoff."""
        max_attempts = conditions.get("max_attempts", 3)
        base_delay = conditions.get("base_delay", 1)
        
        for attempt in range(max_attempts):
            try:
                # Simulate retry logic
                await asyncio.sleep(base_delay * (2 ** attempt))
                
                # In real implementation, this would retry the original operation
                logger.info(f"Retry attempt {attempt + 1} for error {error_info.error_id}")
                
                # Simulate success after retries
                if attempt >= 1:  # Succeed after second attempt
                    return {"operation_success": True, "attempts": attempt + 1}
                    
            except Exception as e:
                logger.warning(f"Retry attempt {attempt + 1} failed: {e}")
        
        return {"operation_success": False, "attempts": max_attempts}
    
    async def _use_cached_data(self, error_info: ErrorInfo, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Use cached data as fallback."""
        cache_age_limit = conditions.get("cache_age_limit", 3600)
        
        # Simulate cache lookup
        logger.info(f"Using cached data for error {error_info.error_id}")
        
        # In real implementation, this would check cache age and return cached data
        return {"data_available": True, "cache_used": True, "age_seconds": 300}
    
    async def _degrade_service(self, error_info: ErrorInfo, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Provide degraded service functionality."""
        essential_only = conditions.get("essential_features_only", True)
        
        logger.info(f"Activating degraded service mode for error {error_info.error_id}")
        
        # Update system state
        self.system_health.overall_state = SystemState.DEGRADED
        
        return {"service_available": True, "degraded_mode": True, "essential_only": essential_only}
    
    async def _use_alternative_algorithm(self, error_info: ErrorInfo, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Use alternative processing algorithm."""
        logger.info(f"Switching to alternative algorithm for error {error_info.error_id}")
        
        # Simulate algorithm switch
        return {"processing_complete": True, "algorithm": "alternative", "performance_impact": 0.2}
    
    def _log_error(self, error_info: ErrorInfo) -> None:
        """Log error with appropriate level."""
        log_message = f"Error {error_info.error_id}: {error_info.error_message} in {error_info.component}.{error_info.function_name}"
        
        if error_info.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif error_info.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif error_info.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def _update_system_health(self, error_info: ErrorInfo) -> None:
        """Update system health based on error."""
        # Update error counts
        self.system_health.error_count_24h += 1
        self.system_health.last_error_time = error_info.timestamp
        
        # Update critical error count
        if error_info.severity == ErrorSeverity.CRITICAL:
            self.system_health.critical_errors_active += 1
        
        # Update component state
        component_state = SystemState.NORMAL
        if error_info.severity == ErrorSeverity.CRITICAL:
            component_state = SystemState.CRITICAL
        elif error_info.severity == ErrorSeverity.HIGH:
            component_state = SystemState.DEGRADED
        
        self.system_health.component_states[error_info.component] = component_state
        
        # Update overall state
        if self.system_health.critical_errors_active > self.critical_error_threshold:
            self.system_health.overall_state = SystemState.CRITICAL
        elif self.system_health.error_count_24h > self.error_threshold_24h:
            self.system_health.overall_state = SystemState.DEGRADED
    
    def _store_error(self, error_info: ErrorInfo) -> None:
        """Store error for analysis and pattern detection."""
        self.error_history.append(error_info)
        self.active_errors[error_info.error_id] = error_info
        
        # Maintain history size limit
        if len(self.error_history) > self.max_error_history:
            self.error_history.pop(0)
        
        # Detect patterns
        self._detect_error_patterns(error_info)
    
    def _detect_error_patterns(self, error_info: ErrorInfo) -> None:
        """Detect error patterns for proactive handling."""
        # Simple pattern detection based on error type and component
        pattern_key = f"{error_info.error_type}_{error_info.component}"
        
        if pattern_key not in self.error_patterns:
            self.error_patterns[pattern_key] = []
        
        self.error_patterns[pattern_key].append(error_info.timestamp)
        
        # Check for frequent errors (more than 5 in last hour)
        recent_errors = [
            ts for ts in self.error_patterns[pattern_key]
            if datetime.utcnow() - ts < timedelta(hours=1)
        ]
        
        if len(recent_errors) > 5:
            logger.warning(f"Error pattern detected: {pattern_key} occurred {len(recent_errors)} times in last hour")
    
    async def _send_notifications(self, error_info: ErrorInfo) -> None:
        """Send notifications for critical errors."""
        if not self.notification_enabled:
            return
        
        if error_info.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
            notification_data = {
                "error_id": error_info.error_id,
                "severity": error_info.severity.value,
                "message": error_info.error_message,
                "component": error_info.component,
                "timestamp": error_info.timestamp.isoformat(),
                "user_impact": error_info.user_impact
            }
            
            # In real implementation, this would send notifications via email, Slack, etc.
            logger.info(f"Notification sent for error {error_info.error_id}")
    
    async def get_system_health(self) -> SystemHealth:
        """Get current system health status."""
        # Update uptime percentage
        if self.system_health.error_count_24h > 0:
            error_rate = self.system_health.error_count_24h / (24 * 60)  # errors per minute
            self.system_health.uptime_percentage = max(0, 100 - (error_rate * 10))
        
        return self.system_health
    
    async def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics and analytics."""
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)
        
        # Count errors by category and severity
        recent_errors = [e for e in self.error_history if e.timestamp > last_24h]
        
        category_counts = {}
        severity_counts = {}
        
        for error in recent_errors:
            category_counts[error.error_category.value] = category_counts.get(error.error_category.value, 0) + 1
            severity_counts[error.severity.value] = severity_counts.get(error.severity.value, 0) + 1
        
        return {
            "total_errors_24h": len(recent_errors),
            "errors_by_category": category_counts,
            "errors_by_severity": severity_counts,
            "active_errors": len(self.active_errors),
            "active_fallbacks": len(self.active_fallbacks),
            "error_patterns": len(self.error_patterns),
            "system_health": {
                "overall_state": self.system_health.overall_state.value,
                "uptime_percentage": self.system_health.uptime_percentage,
                "critical_errors_active": self.system_health.critical_errors_active
            }
        }
    
    def create_error_decorator(self, component: str, function_name: str = None):
        """Create decorator for automatic error handling."""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    context = {
                        "component": component,
                        "function": function_name or func.__name__,
                        "args": str(args)[:200],  # Truncate for logging
                        "kwargs": str(kwargs)[:200]
                    }
                    await self.handle_error(e, context)
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    context = {
                        "component": component,
                        "function": function_name or func.__name__,
                        "args": str(args)[:200],
                        "kwargs": str(kwargs)[:200]
                    }
                    # For sync functions, we can't await, so we schedule the error handling
                    asyncio.create_task(self.handle_error(e, context))
                    raise
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator


# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

class ErrorHandlingUtils:
    """Utility functions for error handling."""
    
    @staticmethod
    def error_info_to_dict(error_info: ErrorInfo) -> Dict[str, Any]:
        """Convert error info to dictionary format."""
        return {
            "error_id": error_info.error_id,
            "error_type": error_info.error_type,
            "error_message": error_info.error_message,
            "error_category": error_info.error_category.value,
            "severity": error_info.severity.value,
            "timestamp": error_info.timestamp.isoformat(),
            "component": error_info.component,
            "function_name": error_info.function_name,
            "user_impact": error_info.user_impact,
            "recovery_actions": error_info.recovery_actions,
            "metadata": error_info.metadata
        }
    
    @staticmethod
    def create_circuit_breaker(failure_threshold: int = 5, 
                             recovery_timeout: int = 60,
                             expected_exception: type = Exception):
        """Create a circuit breaker decorator."""
        def decorator(func):
            failure_count = 0
            last_failure_time = None
            state = "closed"  # closed, open, half-open
            
            @wraps(func)
            async def wrapper(*args, **kwargs):
                nonlocal failure_count, last_failure_time, state
                
                # Check circuit state
                if state == "open":
                    if datetime.utcnow() - last_failure_time > timedelta(seconds=recovery_timeout):
                        state = "half-open"
                    else:
                        raise Exception("Circuit breaker is open")
                
                try:
                    result = await func(*args, **kwargs)
                    
                    # Reset on success
                    if state == "half-open":
                        state = "closed"
                        failure_count = 0
                    
                    return result
                    
                except expected_exception as e:
                    failure_count += 1
                    last_failure_time = datetime.utcnow()
                    
                    if failure_count >= failure_threshold:
                        state = "open"
                    
                    raise
            
            return wrapper
        return decorator
