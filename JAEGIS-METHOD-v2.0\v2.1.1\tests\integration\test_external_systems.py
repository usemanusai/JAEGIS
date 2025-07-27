"""
External Systems Integration Tests
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Integration tests for N.L.D.S. with external systems including databases,
message queues, caching systems, and third-party APIs.
"""

import pytest
import asyncio
import redis
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from typing import Dict, Any, List

import aiohttp
import asyncpg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDatabaseIntegration:
    """Test database integration."""
    
    @pytest.fixture
    async def mock_database_connection(self):
        """Mock database connection for testing."""
        mock_conn = AsyncMock()
        mock_conn.execute.return_value = Mock(rowcount=1)
        mock_conn.fetch.return_value = [
            {"id": 1, "user_id": "test_user", "input_text": "test", "created_at": datetime.utcnow()}
        ]
        mock_conn.fetchrow.return_value = {
            "id": 1, "user_id": "test_user", "input_text": "test", "created_at": datetime.utcnow()
        }
        return mock_conn
    
    @pytest.mark.asyncio
    async def test_user_session_persistence(self, mock_database_connection):
        """Test user session persistence in database."""
        from nlds.integration.database import DatabaseManager
        
        db_manager = DatabaseManager("postgresql://test:test@localhost/test")
        db_manager.connection = mock_database_connection
        
        # Store user session
        session_data = {
            "user_id": "test_user_001",
            "session_id": "session_001",
            "context": {"domain": "technology", "preferences": {"detail_level": "high"}},
            "conversation_history": [
                {"input": "test input", "timestamp": datetime.utcnow()}
            ]
        }
        
        result = await db_manager.store_user_session(session_data)
        
        assert result.success
        mock_database_connection.execute.assert_called()
    
    @pytest.mark.asyncio
    async def test_conversation_history_retrieval(self, mock_database_connection):
        """Test conversation history retrieval."""
        from nlds.integration.database import DatabaseManager
        
        db_manager = DatabaseManager("postgresql://test:test@localhost/test")
        db_manager.connection = mock_database_connection
        
        # Mock conversation history
        mock_database_connection.fetch.return_value = [
            {
                "id": 1,
                "user_id": "test_user_001",
                "input_text": "Previous input 1",
                "enhanced_input": "Enhanced previous input 1",
                "confidence_score": 0.85,
                "created_at": datetime.utcnow() - timedelta(hours=1)
            },
            {
                "id": 2,
                "user_id": "test_user_001",
                "input_text": "Previous input 2",
                "enhanced_input": "Enhanced previous input 2",
                "confidence_score": 0.90,
                "created_at": datetime.utcnow() - timedelta(minutes=30)
            }
        ]
        
        # Retrieve conversation history
        history = await db_manager.get_conversation_history("test_user_001", limit=10)
        
        assert len(history) == 2
        assert history[0]["input_text"] == "Previous input 1"
        assert history[1]["confidence_score"] == 0.90
    
    @pytest.mark.asyncio
    async def test_analytics_data_storage(self, mock_database_connection):
        """Test analytics data storage."""
        from nlds.integration.database import DatabaseManager
        
        db_manager = DatabaseManager("postgresql://test:test@localhost/test")
        db_manager.connection = mock_database_connection
        
        # Store analytics data
        analytics_data = {
            "request_id": "req_001",
            "user_id": "test_user_001",
            "processing_time_ms": 1250,
            "confidence_score": 0.88,
            "components_used": ["processing", "analysis", "translation"],
            "jaegis_command_generated": True,
            "timestamp": datetime.utcnow()
        }
        
        result = await db_manager.store_analytics_data(analytics_data)
        
        assert result.success
        mock_database_connection.execute.assert_called()
    
    @pytest.mark.asyncio
    async def test_database_connection_pooling(self):
        """Test database connection pooling."""
        from nlds.integration.database import DatabaseManager
        
        db_manager = DatabaseManager(
            "postgresql://test:test@localhost/test",
            pool_size=10,
            max_overflow=20
        )
        
        # Mock connection pool
        with patch('asyncpg.create_pool') as mock_create_pool:
            mock_pool = AsyncMock()
            mock_create_pool.return_value = mock_pool
            
            await db_manager.initialize_connection_pool()
            
            assert db_manager.pool is not None
            mock_create_pool.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_database_transaction_handling(self, mock_database_connection):
        """Test database transaction handling."""
        from nlds.integration.database import DatabaseManager
        
        db_manager = DatabaseManager("postgresql://test:test@localhost/test")
        db_manager.connection = mock_database_connection
        
        # Mock transaction
        mock_transaction = AsyncMock()
        mock_database_connection.transaction.return_value = mock_transaction
        
        # Execute transaction
        async with db_manager.transaction() as tx:
            await db_manager.store_user_session({"user_id": "test"})
            await db_manager.store_analytics_data({"request_id": "test"})
        
        # Verify transaction was used
        mock_database_connection.transaction.assert_called()


class TestRedisIntegration:
    """Test Redis caching integration."""
    
    @pytest.fixture
    def mock_redis_client(self):
        """Mock Redis client for testing."""
        mock_redis = AsyncMock()
        mock_redis.get.return_value = json.dumps({
            "cached_result": "test_data",
            "timestamp": datetime.utcnow().isoformat()
        })
        mock_redis.set.return_value = True
        mock_redis.exists.return_value = True
        mock_redis.delete.return_value = 1
        return mock_redis
    
    @pytest.mark.asyncio
    async def test_processing_result_caching(self, mock_redis_client):
        """Test caching of processing results."""
        from nlds.integration.cache import CacheManager
        
        cache_manager = CacheManager(redis_client=mock_redis_client)
        
        # Cache processing result
        cache_key = "processing:hash_12345"
        result_data = {
            "enhanced_input": "Enhanced test input",
            "confidence_score": 0.88,
            "processing_time_ms": 1200
        }
        
        success = await cache_manager.cache_processing_result(cache_key, result_data, ttl=3600)
        
        assert success
        mock_redis_client.set.assert_called()
    
    @pytest.mark.asyncio
    async def test_analysis_result_caching(self, mock_redis_client):
        """Test caching of analysis results."""
        from nlds.integration.cache import CacheManager
        
        cache_manager = CacheManager(redis_client=mock_redis_client)
        
        # Cache analysis result
        cache_key = "analysis:hash_67890"
        analysis_data = {
            "logical_analysis": {"confidence": 0.85},
            "emotional_analysis": {"confidence": 0.80},
            "creative_analysis": {"confidence": 0.75},
            "synthesis": {"overall_confidence": 0.80}
        }
        
        success = await cache_manager.cache_analysis_result(cache_key, analysis_data, ttl=1800)
        
        assert success
        mock_redis_client.set.assert_called()
    
    @pytest.mark.asyncio
    async def test_cache_hit_retrieval(self, mock_redis_client):
        """Test cache hit retrieval."""
        from nlds.integration.cache import CacheManager
        
        cache_manager = CacheManager(redis_client=mock_redis_client)
        
        # Retrieve cached data
        cache_key = "processing:hash_12345"
        cached_data = await cache_manager.get_cached_result(cache_key)
        
        assert cached_data is not None
        assert "cached_result" in cached_data
        mock_redis_client.get.assert_called_with(cache_key)
    
    @pytest.mark.asyncio
    async def test_cache_invalidation(self, mock_redis_client):
        """Test cache invalidation."""
        from nlds.integration.cache import CacheManager
        
        cache_manager = CacheManager(redis_client=mock_redis_client)
        
        # Invalidate cache pattern
        pattern = "processing:user_123:*"
        result = await cache_manager.invalidate_cache_pattern(pattern)
        
        assert result.success
        assert result.invalidated_count > 0
    
    @pytest.mark.asyncio
    async def test_distributed_locking(self, mock_redis_client):
        """Test distributed locking with Redis."""
        from nlds.integration.cache import CacheManager
        
        cache_manager = CacheManager(redis_client=mock_redis_client)
        
        # Mock lock acquisition
        mock_redis_client.set.return_value = True  # Lock acquired
        
        # Acquire distributed lock
        lock_key = "lock:processing:user_123"
        async with cache_manager.distributed_lock(lock_key, timeout=30):
            # Simulate work under lock
            await asyncio.sleep(0.1)
        
        # Verify lock was acquired and released
        assert mock_redis_client.set.call_count >= 1
        assert mock_redis_client.delete.call_count >= 1


class TestMessageQueueIntegration:
    """Test message queue integration."""
    
    @pytest.fixture
    def mock_message_queue(self):
        """Mock message queue for testing."""
        mock_queue = AsyncMock()
        mock_queue.publish.return_value = True
        mock_queue.subscribe.return_value = AsyncMock()
        mock_queue.acknowledge.return_value = True
        return mock_queue
    
    @pytest.mark.asyncio
    async def test_command_queue_publishing(self, mock_message_queue):
        """Test publishing commands to message queue."""
        from nlds.integration.messaging import MessageQueueManager
        
        queue_manager = MessageQueueManager(mock_message_queue)
        
        # Publish JAEGIS command
        command_message = {
            "command_id": "cmd_001",
            "command_type": "analysis",
            "target_squad": "content_squad",
            "priority": "normal",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = await queue_manager.publish_jaegis_command(command_message)
        
        assert result.success
        mock_message_queue.publish.assert_called()
    
    @pytest.mark.asyncio
    async def test_status_update_subscription(self, mock_message_queue):
        """Test subscribing to status updates."""
        from nlds.integration.messaging import MessageQueueManager
        
        queue_manager = MessageQueueManager(mock_message_queue)
        
        # Mock status update message
        status_message = {
            "command_id": "cmd_001",
            "status": "completed",
            "progress_percentage": 100.0,
            "result_data": {"success": True}
        }
        
        # Mock message reception
        mock_message_queue.subscribe.return_value.__aiter__.return_value = [
            Mock(body=json.dumps(status_message))
        ]
        
        # Subscribe to status updates
        async for message in queue_manager.subscribe_to_status_updates():
            assert message.command_id == "cmd_001"
            assert message.status == "completed"
            break  # Only test one message
    
    @pytest.mark.asyncio
    async def test_message_queue_error_handling(self, mock_message_queue):
        """Test message queue error handling."""
        from nlds.integration.messaging import MessageQueueManager
        
        queue_manager = MessageQueueManager(mock_message_queue)
        
        # Mock connection error
        mock_message_queue.publish.side_effect = Exception("Connection lost")
        
        # Should handle error gracefully
        result = await queue_manager.publish_jaegis_command({"test": "message"})
        
        assert not result.success
        assert "connection lost" in result.error_message.lower()
    
    @pytest.mark.asyncio
    async def test_message_queue_retry_logic(self, mock_message_queue):
        """Test message queue retry logic."""
        from nlds.integration.messaging import MessageQueueManager
        
        queue_manager = MessageQueueManager(mock_message_queue, max_retries=3)
        
        # Mock intermittent failures
        mock_message_queue.publish.side_effect = [
            Exception("Temporary failure"),
            Exception("Temporary failure"),
            True  # Success on third try
        ]
        
        # Should succeed after retries
        result = await queue_manager.publish_jaegis_command({"test": "message"})
        
        assert result.success
        assert mock_message_queue.publish.call_count == 3


class TestHTTPClientIntegration:
    """Test HTTP client integration for external APIs."""
    
    @pytest.fixture
    def mock_http_session(self):
        """Mock HTTP session for testing."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json.return_value = {"success": True, "data": "test_response"}
        mock_response.headers = {"content-type": "application/json"}
        mock_session.get.return_value.__aenter__.return_value = mock_response
        mock_session.post.return_value.__aenter__.return_value = mock_response
        return mock_session
    
    @pytest.mark.asyncio
    async def test_openrouter_api_integration(self, mock_http_session):
        """Test OpenRouter API integration."""
        from nlds.integration.external_apis import OpenRouterClient
        
        client = OpenRouterClient(
            api_keys=["key1", "key2", "key3"],
            http_session=mock_http_session
        )
        
        # Make API request
        request_data = {
            "model": "gpt-4-turbo",
            "messages": [{"role": "user", "content": "Test prompt"}],
            "max_tokens": 150
        }
        
        response = await client.make_request(request_data)
        
        assert response.success
        assert response.data is not None
        mock_http_session.post.assert_called()
    
    @pytest.mark.asyncio
    async def test_github_api_integration(self, mock_http_session):
        """Test GitHub API integration."""
        from nlds.integration.external_apis import GitHubClient
        
        client = GitHubClient(
            access_token="github_token",
            repository="usemanusai/JAEGIS",
            http_session=mock_http_session
        )
        
        # Fetch file content
        file_path = "commands/analysis_template.md"
        response = await client.get_file_content(file_path)
        
        assert response.success
        assert response.content is not None
        mock_http_session.get.assert_called()
    
    @pytest.mark.asyncio
    async def test_http_client_retry_logic(self, mock_http_session):
        """Test HTTP client retry logic."""
        from nlds.integration.external_apis import HTTPClient
        
        client = HTTPClient(max_retries=3, retry_delay=0.1)
        client.session = mock_http_session
        
        # Mock intermittent failures
        mock_responses = [
            Mock(status=500),  # Server error
            Mock(status=429),  # Rate limit
            Mock(status=200, json=lambda: {"success": True})  # Success
        ]
        
        mock_http_session.get.return_value.__aenter__.side_effect = mock_responses
        
        # Should succeed after retries
        response = await client.get("https://api.example.com/test")
        
        assert response.status == 200
        assert mock_http_session.get.call_count == 3
    
    @pytest.mark.asyncio
    async def test_http_client_timeout_handling(self, mock_http_session):
        """Test HTTP client timeout handling."""
        from nlds.integration.external_apis import HTTPClient
        
        client = HTTPClient(timeout=1.0)
        client.session = mock_http_session
        
        # Mock timeout
        mock_http_session.get.side_effect = asyncio.TimeoutError()
        
        # Should handle timeout gracefully
        with pytest.raises(asyncio.TimeoutError):
            await client.get("https://api.example.com/slow")


class TestWebSocketIntegration:
    """Test WebSocket integration for real-time communication."""
    
    @pytest.fixture
    def mock_websocket(self):
        """Mock WebSocket for testing."""
        mock_ws = AsyncMock()
        mock_ws.send.return_value = None
        mock_ws.recv.return_value = json.dumps({
            "message_type": "status_update",
            "command_id": "cmd_001",
            "status": "in_progress",
            "progress": 50.0
        })
        mock_ws.close.return_value = None
        return mock_ws
    
    @pytest.mark.asyncio
    async def test_websocket_connection_establishment(self, mock_websocket):
        """Test WebSocket connection establishment."""
        from nlds.integration.websocket import WebSocketManager
        
        ws_manager = WebSocketManager("ws://localhost:8080/ws")
        ws_manager.websocket = mock_websocket
        
        # Establish connection
        result = await ws_manager.connect()
        
        assert result.success
        assert ws_manager.is_connected
    
    @pytest.mark.asyncio
    async def test_websocket_message_sending(self, mock_websocket):
        """Test WebSocket message sending."""
        from nlds.integration.websocket import WebSocketManager
        
        ws_manager = WebSocketManager("ws://localhost:8080/ws")
        ws_manager.websocket = mock_websocket
        ws_manager.is_connected = True
        
        # Send message
        message = {
            "message_type": "command_submission",
            "command_id": "cmd_001",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = await ws_manager.send_message(message)
        
        assert result.success
        mock_websocket.send.assert_called_with(json.dumps(message))
    
    @pytest.mark.asyncio
    async def test_websocket_message_receiving(self, mock_websocket):
        """Test WebSocket message receiving."""
        from nlds.integration.websocket import WebSocketManager
        
        ws_manager = WebSocketManager("ws://localhost:8080/ws")
        ws_manager.websocket = mock_websocket
        ws_manager.is_connected = True
        
        # Receive message
        message = await ws_manager.receive_message()
        
        assert message is not None
        assert message.message_type == "status_update"
        assert message.command_id == "cmd_001"
        mock_websocket.recv.assert_called()
    
    @pytest.mark.asyncio
    async def test_websocket_connection_recovery(self, mock_websocket):
        """Test WebSocket connection recovery."""
        from nlds.integration.websocket import WebSocketManager
        
        ws_manager = WebSocketManager("ws://localhost:8080/ws", auto_reconnect=True)
        ws_manager.websocket = mock_websocket
        
        # Mock connection loss
        mock_websocket.recv.side_effect = [
            json.dumps({"test": "message"}),
            Exception("Connection lost"),
            json.dumps({"test": "reconnected"})
        ]
        
        # Should automatically reconnect
        messages = []
        async for message in ws_manager.listen_for_messages():
            messages.append(message)
            if len(messages) >= 2:
                break
        
        assert len(messages) == 2
        assert messages[1]["test"] == "reconnected"


class TestExternalSystemsOrchestration:
    """Test orchestration of multiple external systems."""
    
    @pytest.mark.asyncio
    async def test_multi_system_coordination(self):
        """Test coordination across multiple external systems."""
        from nlds.integration import ExternalSystemsOrchestrator
        
        # Mock all external systems
        mock_database = AsyncMock()
        mock_cache = AsyncMock()
        mock_queue = AsyncMock()
        mock_http = AsyncMock()
        
        orchestrator = ExternalSystemsOrchestrator(
            database=mock_database,
            cache=mock_cache,
            message_queue=mock_queue,
            http_client=mock_http
        )
        
        # Execute coordinated operation
        operation_data = {
            "user_id": "test_user",
            "request_id": "req_001",
            "input_text": "Test coordination",
            "processing_result": {"confidence": 0.88}
        }
        
        result = await orchestrator.execute_coordinated_operation(operation_data)
        
        # Should coordinate across all systems
        assert result.success
        assert result.database_stored
        assert result.cache_updated
        assert result.message_published
        assert result.external_api_called
    
    @pytest.mark.asyncio
    async def test_system_health_monitoring(self):
        """Test health monitoring of external systems."""
        from nlds.integration import ExternalSystemsOrchestrator
        
        orchestrator = ExternalSystemsOrchestrator()
        
        # Mock health checks
        with patch.object(orchestrator, 'check_database_health', return_value=True), \
             patch.object(orchestrator, 'check_cache_health', return_value=True), \
             patch.object(orchestrator, 'check_queue_health', return_value=False), \
             patch.object(orchestrator, 'check_api_health', return_value=True):
            
            health_status = await orchestrator.check_all_systems_health()
            
            assert health_status.overall_status == "degraded"  # One system down
            assert health_status.database_healthy
            assert health_status.cache_healthy
            assert not health_status.queue_healthy
            assert health_status.api_healthy
    
    @pytest.mark.asyncio
    async def test_graceful_degradation(self):
        """Test graceful degradation when external systems fail."""
        from nlds.integration import ExternalSystemsOrchestrator
        
        orchestrator = ExternalSystemsOrchestrator()
        
        # Mock cache failure
        with patch.object(orchestrator.cache, 'get', side_effect=Exception("Cache unavailable")):
            
            # Should continue operation without cache
            result = await orchestrator.process_with_fallback("test_input")
            
            assert result.success
            assert result.cache_used is False
            assert result.fallback_mode is True
