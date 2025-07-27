"""
Unit Tests for N.L.D.S. API Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive unit tests for the API endpoints, authentication, and related components.
"""

import pytest
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from nlds.api import create_nlds_api, create_test_client
from nlds.api.auth import AuthenticationService, User, UserRole, Permission
from nlds.api.rate_limiting import RateLimitingEngine, RateLimitRule, RateLimitScope
from nlds.api.models import ProcessingRequest, AnalysisRequest, TranslationRequest


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return create_test_client()
    
    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers."""
        return {"Authorization": "Bearer test_api_key_001"}
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "timestamp" in data
        assert "version" in data
    
    def test_status_endpoint(self, client, auth_headers):
        """Test system status endpoint."""
        response = client.get("/status", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "system_status" in data
        assert "component_status" in data
        assert "performance_metrics" in data
    
    def test_process_endpoint_valid_input(self, client, auth_headers):
        """Test process endpoint with valid input."""
        request_data = {
            "input_text": "Analyze market trends for renewable energy",
            "mode": "enhanced",
            "enable_amasiap": True
        }
        
        response = client.post("/process", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "enhanced_input" in data
        assert "confidence_score" in data
        assert data["confidence_score"] >= 0.0
    
    def test_process_endpoint_invalid_input(self, client, auth_headers):
        """Test process endpoint with invalid input."""
        invalid_requests = [
            {},  # Empty request
            {"input_text": ""},  # Empty text
            {"input_text": "A" * 10001},  # Too long
            {"input_text": "valid", "mode": "invalid_mode"},  # Invalid mode
        ]
        
        for request_data in invalid_requests:
            response = client.post("/process", json=request_data, headers=auth_headers)
            assert response.status_code == 400
    
    def test_analyze_endpoint_valid_input(self, client, auth_headers):
        """Test analyze endpoint with valid input."""
        request_data = {
            "input_text": "Create strategic business plan",
            "analysis_types": ["logical", "emotional", "creative"],
            "depth_level": 3
        }
        
        response = client.post("/analyze", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "logical_analysis" in data
        assert "emotional_analysis" in data
        assert "creative_analysis" in data
        assert "synthesis" in data
    
    def test_translate_endpoint_valid_input(self, client, auth_headers):
        """Test translate endpoint with valid input."""
        request_data = {
            "input_text": "Develop innovation strategy",
            "target_mode": 3,
            "preferred_squad": "content_squad",
            "priority": "normal"
        }
        
        response = client.post("/translate", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "jaegis_command" in data
        assert "confidence_score" in data
        assert "alternative_commands" in data
    
    def test_jaegis_submit_endpoint(self, client, auth_headers):
        """Test JAEGIS command submission endpoint."""
        command_data = {
            "command": {
                "command_type": "analysis",
                "target_squad": "content_squad",
                "mode_level": 3,
                "parameters": [{"type": "text", "value": "test"}]
            },
            "priority": "normal",
            "timeout_seconds": 300
        }
        
        response = client.post("/jaegis/submit", json=command_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "command_id" in data
        assert "status" in data
        assert "submission_time" in data
    
    def test_jaegis_status_endpoint(self, client, auth_headers):
        """Test JAEGIS command status endpoint."""
        command_id = "test_command_001"
        
        response = client.get(f"/jaegis/status/{command_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "command_id" in data
        assert "status" in data
        assert "progress_percentage" in data
    
    def test_metrics_endpoint_admin_only(self, client):
        """Test metrics endpoint requires admin access."""
        # Without auth
        response = client.get("/metrics")
        assert response.status_code == 401
        
        # With user auth (should be forbidden)
        user_headers = {"Authorization": "Bearer nlds_user_key_001"}
        response = client.get("/metrics", headers=user_headers)
        assert response.status_code == 403
        
        # With admin auth (should work)
        admin_headers = {"Authorization": "Bearer nlds_admin_key_001"}
        response = client.get("/metrics", headers=admin_headers)
        assert response.status_code == 200
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/health")
        
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers
    
    def test_security_headers(self, client):
        """Test security headers are present."""
        response = client.get("/health")
        
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection"
        ]
        
        for header in security_headers:
            assert header in response.headers
    
    def test_rate_limit_headers(self, client, auth_headers):
        """Test rate limit headers are included."""
        response = client.get("/status", headers=auth_headers)
        
        rate_limit_headers = [
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset"
        ]
        
        for header in rate_limit_headers:
            assert header in response.headers


class TestAuthentication:
    """Test cases for authentication system."""
    
    def test_authentication_service_initialization(self):
        """Test authentication service initialization."""
        auth_service = AuthenticationService()
        
        assert auth_service.secret_key is not None
        assert auth_service.algorithm == "HS256"
        assert auth_service.access_token_expire_minutes > 0
    
    def test_create_access_token(self, sample_user):
        """Test access token creation."""
        auth_service = AuthenticationService()
        
        token = auth_service.create_access_token(sample_user)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token can be decoded
        token_data = auth_service.verify_token(token)
        assert token_data.user_id == sample_user.user_id
        assert token_data.username == sample_user.username
    
    def test_create_refresh_token(self, sample_user):
        """Test refresh token creation."""
        auth_service = AuthenticationService()
        
        token = auth_service.create_refresh_token(sample_user)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token can be decoded
        token_data = auth_service.verify_token(token)
        assert token_data.user_id == sample_user.user_id
        assert token_data.token_type.value == "refresh"
    
    def test_authenticate_user_valid_credentials(self):
        """Test user authentication with valid credentials."""
        auth_service = AuthenticationService()
        
        result = auth_service.authenticate_user("admin", "password")
        
        assert result.success
        assert result.user is not None
        assert result.access_token is not None
        assert result.refresh_token is not None
    
    def test_authenticate_user_invalid_credentials(self):
        """Test user authentication with invalid credentials."""
        auth_service = AuthenticationService()
        
        result = auth_service.authenticate_user("nonexistent", "password")
        
        assert not result.success
        assert result.user is None
        assert result.access_token is None
        assert "Invalid credentials" in result.error_message
    
    def test_authenticate_api_key_valid(self):
        """Test API key authentication with valid key."""
        auth_service = AuthenticationService()
        
        result = auth_service.authenticate_api_key("nlds_admin_key_001")
        
        assert result.success
        assert result.user is not None
        assert result.user.role == UserRole.ADMIN
    
    def test_authenticate_api_key_invalid(self):
        """Test API key authentication with invalid key."""
        auth_service = AuthenticationService()
        
        result = auth_service.authenticate_api_key("invalid_key")
        
        assert not result.success
        assert result.user is None
        assert "Invalid API key" in result.error_message
    
    def test_refresh_access_token(self, sample_user):
        """Test access token refresh."""
        auth_service = AuthenticationService()
        
        refresh_token = auth_service.create_refresh_token(sample_user)
        result = auth_service.refresh_access_token(refresh_token)
        
        assert result.success
        assert result.access_token is not None
        assert result.user.user_id == sample_user.user_id
    
    def test_revoke_token(self, sample_user):
        """Test token revocation."""
        auth_service = AuthenticationService()
        
        token = auth_service.create_access_token(sample_user)
        
        # Token should be valid initially
        token_data = auth_service.verify_token(token)
        assert token_data.user_id == sample_user.user_id
        
        # Revoke token
        success = auth_service.revoke_token(token)
        assert success
        
        # Token should be invalid after revocation
        with pytest.raises(Exception):  # Should raise HTTPException
            auth_service.verify_token(token)
    
    def test_permission_checking(self, sample_user, sample_admin_user):
        """Test permission checking."""
        auth_service = AuthenticationService()
        
        # Regular user should have limited permissions
        assert auth_service.check_permission(sample_user, Permission.READ)
        assert auth_service.check_permission(sample_user, Permission.WRITE)
        assert not auth_service.check_permission(sample_user, Permission.ADMIN)
        
        # Admin user should have all permissions
        assert auth_service.check_permission(sample_admin_user, Permission.READ)
        assert auth_service.check_permission(sample_admin_user, Permission.WRITE)
        assert auth_service.check_permission(sample_admin_user, Permission.ADMIN)


class TestRateLimiting:
    """Test cases for rate limiting system."""
    
    def test_rate_limiting_engine_initialization(self):
        """Test rate limiting engine initialization."""
        engine = RateLimitingEngine()
        
        assert engine.limiters is not None
        assert engine.rules is not None
        assert len(engine.rules) > 0  # Should have default rules
    
    def test_add_rate_limit_rule(self):
        """Test adding custom rate limit rule."""
        engine = RateLimitingEngine()
        
        rule = RateLimitRule(
            rule_id="test_rule",
            scope=RateLimitScope.USER,
            algorithm="token_bucket",
            requests_per_window=100,
            window_size_seconds=60
        )
        
        engine.add_rule(rule)
        
        assert "test_rule" in engine.rules
        assert engine.rules["test_rule"] == rule
    
    def test_token_bucket_limiter(self):
        """Test token bucket rate limiting algorithm."""
        from nlds.api.rate_limiting import TokenBucketLimiter
        
        limiter = TokenBucketLimiter(capacity=10, refill_rate=1.0)
        
        # Should allow initial requests up to capacity
        for i in range(10):
            assert limiter.consume()
        
        # Should deny additional requests
        assert not limiter.consume()
        
        # Should allow requests after time passes (mocked)
        import time
        time.sleep(1.1)  # Allow refill
        assert limiter.consume()
    
    def test_sliding_window_limiter(self):
        """Test sliding window rate limiting algorithm."""
        from nlds.api.rate_limiting import SlidingWindowLimiter
        
        limiter = SlidingWindowLimiter(window_size=60, max_requests=5)
        
        # Should allow requests up to limit
        for i in range(5):
            assert limiter.is_allowed()
        
        # Should deny additional requests
        assert not limiter.is_allowed()
    
    def test_rate_limit_extraction(self):
        """Test extraction of rate limit identifiers."""
        engine = RateLimitingEngine()
        
        # Mock request
        mock_request = Mock()
        mock_request.client.host = "192.168.1.1"
        mock_request.method = "POST"
        mock_request.url.path = "/process"
        
        user_info = {
            "user_id": "test_user",
            "api_key": "test_key"
        }
        
        identifiers = engine.extract_identifiers(mock_request, user_info)
        
        assert RateLimitScope.GLOBAL in identifiers
        assert RateLimitScope.IP in identifiers
        assert RateLimitScope.USER in identifiers
        assert RateLimitScope.ENDPOINT in identifiers
        assert identifiers[RateLimitScope.IP] == "192.168.1.1"
        assert identifiers[RateLimitScope.USER] == "test_user"
    
    @pytest.mark.asyncio
    async def test_rate_limit_checking(self):
        """Test rate limit checking."""
        engine = RateLimitingEngine()
        
        # Mock request
        mock_request = Mock()
        mock_request.client.host = "192.168.1.1"
        mock_request.method = "GET"
        mock_request.url.path = "/status"
        
        user_info = {"user_id": "test_user"}
        
        # First request should be allowed
        result = await engine.check_rate_limits(mock_request, user_info)
        assert result.allowed
        
        # After many requests, should be rate limited
        for i in range(200):  # Exceed typical limits
            result = await engine.check_rate_limits(mock_request, user_info)
        
        # Should eventually be rate limited
        assert not result.allowed or result.delay_seconds > 0


class TestAPIModels:
    """Test cases for API models."""
    
    def test_processing_request_validation(self):
        """Test processing request model validation."""
        # Valid request
        valid_request = ProcessingRequest(
            input_text="Test input",
            mode="standard",
            enable_amasiap=True
        )
        
        assert valid_request.input_text == "Test input"
        assert valid_request.mode == "standard"
        assert valid_request.enable_amasiap is True
    
    def test_analysis_request_validation(self):
        """Test analysis request model validation."""
        # Valid request
        valid_request = AnalysisRequest(
            input_text="Test analysis",
            analysis_types=["logical", "emotional"],
            depth_level=3
        )
        
        assert valid_request.input_text == "Test analysis"
        assert len(valid_request.analysis_types) == 2
        assert valid_request.depth_level == 3
    
    def test_translation_request_validation(self):
        """Test translation request model validation."""
        # Valid request
        valid_request = TranslationRequest(
            input_text="Test translation",
            target_mode=3,
            preferred_squad="content_squad"
        )
        
        assert valid_request.input_text == "Test translation"
        assert valid_request.target_mode == 3
        assert valid_request.preferred_squad == "content_squad"
    
    def test_model_serialization(self):
        """Test model serialization to JSON."""
        request = ProcessingRequest(
            input_text="Test",
            mode="enhanced"
        )
        
        # Should be serializable
        json_data = request.dict()
        assert isinstance(json_data, dict)
        assert json_data["input_text"] == "Test"
        assert json_data["mode"] == "enhanced"


class TestAPIErrorHandling:
    """Test cases for API error handling."""
    
    def test_validation_error_handling(self, client, auth_headers):
        """Test validation error handling."""
        invalid_request = {
            "input_text": "",  # Invalid empty text
            "mode": "invalid_mode"  # Invalid mode
        }
        
        response = client.post("/process", json=invalid_request, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "validation" in data["error"]["message"].lower()
    
    def test_authentication_error_handling(self, client):
        """Test authentication error handling."""
        # No auth header
        response = client.get("/status")
        assert response.status_code == 401
        
        # Invalid auth header
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/status", headers=invalid_headers)
        assert response.status_code == 401
    
    def test_authorization_error_handling(self, client):
        """Test authorization error handling."""
        # User trying to access admin endpoint
        user_headers = {"Authorization": "Bearer nlds_user_key_001"}
        response = client.get("/metrics", headers=user_headers)
        assert response.status_code == 403
    
    def test_rate_limit_error_handling(self, client, auth_headers):
        """Test rate limit error handling."""
        # Make many requests to trigger rate limiting
        for i in range(150):  # Exceed typical rate limits
            response = client.get("/status", headers=auth_headers)
            if response.status_code == 429:
                # Rate limit triggered
                assert "Retry-After" in response.headers
                data = response.json()
                assert "rate limit" in data["error"]["message"].lower()
                break
    
    def test_internal_error_handling(self, client, auth_headers):
        """Test internal error handling."""
        # Mock an internal error
        with patch('nlds.api.main.processing_orchestrator') as mock_orchestrator:
            mock_orchestrator.process_input.side_effect = Exception("Internal error")
            
            response = client.post("/process", json={
                "input_text": "Test input"
            }, headers=auth_headers)
            
            assert response.status_code == 500
            data = response.json()
            assert "error" in data
    
    def test_timeout_error_handling(self, client, auth_headers):
        """Test timeout error handling."""
        # Mock a timeout
        with patch('nlds.api.main.processing_orchestrator') as mock_orchestrator:
            import asyncio
            mock_orchestrator.process_input.side_effect = asyncio.TimeoutError()
            
            response = client.post("/process", json={
                "input_text": "Test input"
            }, headers=auth_headers)
            
            assert response.status_code == 408
            data = response.json()
            assert "timeout" in data["error"]["message"].lower()
