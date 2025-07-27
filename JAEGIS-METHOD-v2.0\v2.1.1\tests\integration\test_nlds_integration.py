"""
Integration Tests for N.L.D.S. System
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive integration tests for the complete N.L.D.S. system including
all components working together and external system integrations.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from typing import Dict, Any, List

from nlds.integration import NLDSIntegrationOrchestrator
from nlds.processing import ProcessingOrchestrator
from nlds.analysis import AnalysisOrchestrator
from nlds.translation import TranslationOrchestrator
from nlds.api import create_test_client


class TestNLDSEndToEndIntegration:
    """Test complete end-to-end N.L.D.S. integration."""
    
    @pytest.fixture
    async def integration_orchestrator(self, sample_config):
        """Create integration orchestrator for testing."""
        orchestrator = NLDSIntegrationOrchestrator(sample_config["integration"])
        
        # Mock external dependencies
        with patch.object(orchestrator, 'initialize_all_components', new_callable=AsyncMock) as mock_init:
            mock_init.return_value = True
            await orchestrator.initialize_all_components()
        
        yield orchestrator
        
        # Cleanup
        with patch.object(orchestrator, 'cleanup_all_components', new_callable=AsyncMock):
            await orchestrator.cleanup_all_components()
    
    @pytest.mark.asyncio
    async def test_complete_processing_pipeline(self, integration_orchestrator):
        """Test complete processing pipeline from input to JAEGIS command."""
        input_text = "Analyze the current market trends for renewable energy and provide strategic recommendations for investment opportunities in Q4 2025."
        
        # Process through complete pipeline
        result = await integration_orchestrator.process_complete_pipeline(
            input_text=input_text,
            user_context={
                "user_id": "test_user_001",
                "domain_expertise": "finance",
                "urgency": "medium"
            }
        )
        
        # Verify complete pipeline execution
        assert result.success
        assert result.processing_result is not None
        assert result.analysis_result is not None
        assert result.translation_result is not None
        assert result.jaegis_command is not None
        
        # Verify processing quality
        assert result.processing_result.confidence_score >= 0.7
        assert result.analysis_result.overall_confidence >= 0.7
        assert result.translation_result.confidence_score >= 0.7
        
        # Verify JAEGIS command structure
        command = result.jaegis_command
        assert command.command_id is not None
        assert command.command_type is not None
        assert command.target_squad is not None
        assert command.mode_level in range(1, 6)
        assert len(command.parameters) > 0
    
    @pytest.mark.asyncio
    async def test_pipeline_with_low_confidence_handling(self, integration_orchestrator):
        """Test pipeline handling of low confidence scenarios."""
        # Intentionally vague input to trigger low confidence
        vague_input = "do something"
        
        result = await integration_orchestrator.process_complete_pipeline(
            input_text=vague_input,
            user_context={"user_id": "test_user_001"}
        )
        
        # Should still succeed but with alternatives and suggestions
        assert result.success
        assert result.overall_confidence < 0.8
        assert len(result.improvement_suggestions) > 0
        assert len(result.alternative_commands) > 0
    
    @pytest.mark.asyncio
    async def test_pipeline_error_recovery(self, integration_orchestrator):
        """Test pipeline error recovery mechanisms."""
        # Mock a failure in one component
        with patch.object(integration_orchestrator.analysis_orchestrator, 'analyze', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.side_effect = Exception("Analysis component failure")
            
            # Should gracefully handle the error
            result = await integration_orchestrator.process_complete_pipeline(
                input_text="test input",
                user_context={"user_id": "test_user_001"}
            )
            
            # Should indicate partial failure but still provide useful output
            assert not result.success
            assert "analysis_error" in result.error_details
            assert result.processing_result is not None  # Should have partial results
    
    @pytest.mark.asyncio
    async def test_pipeline_performance_requirements(self, integration_orchestrator, assert_async_timing):
        """Test pipeline performance meets requirements."""
        input_text = "Create a comprehensive business strategy for digital transformation"
        
        # Complete pipeline should execute within 3 seconds
        result = await assert_async_timing(
            integration_orchestrator.process_complete_pipeline(
                input_text=input_text,
                user_context={"user_id": "test_user_001"}
            ),
            max_time_ms=3000
        )
        
        assert result.success
        assert result.total_processing_time_ms < 3000
    
    @pytest.mark.asyncio
    async def test_pipeline_concurrent_processing(self, integration_orchestrator):
        """Test concurrent pipeline processing."""
        inputs = [
            "Analyze market trends for technology sector",
            "Create strategic plan for product launch",
            "Develop risk assessment framework",
            "Optimize operational efficiency",
            "Design innovation roadmap"
        ]
        
        # Process all inputs concurrently
        tasks = [
            integration_orchestrator.process_complete_pipeline(
                input_text=inp,
                user_context={"user_id": f"user_{i}"}
            )
            for i, inp in enumerate(inputs)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # All should succeed
        assert len(results) == len(inputs)
        for result in results:
            assert result.success
            assert result.jaegis_command is not None
    
    @pytest.mark.asyncio
    async def test_pipeline_context_preservation(self, integration_orchestrator):
        """Test context preservation throughout pipeline."""
        input_text = "Analyze quarterly performance"
        context = {
            "user_id": "test_user_001",
            "domain": "finance",
            "company": "TechCorp",
            "quarter": "Q3 2025",
            "urgency": "high"
        }
        
        result = await integration_orchestrator.process_complete_pipeline(
            input_text=input_text,
            user_context=context
        )
        
        # Context should be preserved and enriched throughout pipeline
        assert result.success
        assert "context_enrichment" in result.metadata
        
        # JAEGIS command should reflect context
        command = result.jaegis_command
        assert command.priority == "high"  # Should reflect urgency
        assert "finance" in str(command.metadata).lower()  # Should include domain


class TestJAEGISIntegration:
    """Test integration with JAEGIS components."""
    
    @pytest.fixture
    def mock_jaegis_interface(self):
        """Mock JAEGIS interface for testing."""
        mock = AsyncMock()
        mock.initialize_connection.return_value = True
        mock.submit_command.return_value = {
            "command_id": "jaegis_cmd_001",
            "status": "submitted",
            "submission_time": datetime.utcnow(),
            "estimated_completion": datetime.utcnow() + timedelta(minutes=5)
        }
        mock.get_command_status.return_value = {
            "command_id": "jaegis_cmd_001",
            "status": "completed",
            "progress_percentage": 100.0,
            "result_data": {
                "success": True,
                "output": "Analysis completed successfully",
                "artifacts": ["report.pdf", "data.json"]
            },
            "completion_time": datetime.utcnow()
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_jaegis_command_submission(self, integration_orchestrator, mock_jaegis_interface):
        """Test JAEGIS command submission integration."""
        # Mock the JAEGIS interface
        integration_orchestrator.jaegis_interface = mock_jaegis_interface
        
        # Create a test command
        from nlds.translation import JAEGISCommand
        command = JAEGISCommand(
            command_id="test_cmd_001",
            command_type="analysis",
            target_squad="content_squad",
            mode_level=3,
            parameters=[{"type": "text", "value": "test input"}],
            priority="normal"
        )
        
        # Submit command
        result = await integration_orchestrator.submit_jaegis_command(command)
        
        assert result.success
        assert result.command_id == "jaegis_cmd_001"
        assert result.status == "submitted"
        
        # Verify interface was called correctly
        mock_jaegis_interface.submit_command.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_jaegis_status_monitoring(self, integration_orchestrator, mock_jaegis_interface):
        """Test JAEGIS command status monitoring."""
        integration_orchestrator.jaegis_interface = mock_jaegis_interface
        
        command_id = "jaegis_cmd_001"
        
        # Monitor command status
        status = await integration_orchestrator.get_jaegis_command_status(command_id)
        
        assert status.command_id == command_id
        assert status.status == "completed"
        assert status.progress_percentage == 100.0
        assert status.result_data is not None
        
        # Verify interface was called correctly
        mock_jaegis_interface.get_command_status.assert_called_once_with(command_id)
    
    @pytest.mark.asyncio
    async def test_jaegis_real_time_communication(self, integration_orchestrator, mock_jaegis_interface):
        """Test real-time communication with JAEGIS."""
        integration_orchestrator.jaegis_interface = mock_jaegis_interface
        
        # Mock WebSocket connection
        mock_websocket = AsyncMock()
        mock_websocket.receive.return_value = json.dumps({
            "message_type": "command_update",
            "command_id": "jaegis_cmd_001",
            "status": "in_progress",
            "progress_percentage": 50.0
        })
        
        integration_orchestrator.jaegis_interface.websocket = mock_websocket
        
        # Listen for updates
        update = await integration_orchestrator.listen_for_jaegis_updates()
        
        assert update.message_type == "command_update"
        assert update.command_id == "jaegis_cmd_001"
        assert update.progress_percentage == 50.0
    
    @pytest.mark.asyncio
    async def test_jaegis_error_handling(self, integration_orchestrator, mock_jaegis_interface):
        """Test JAEGIS integration error handling."""
        # Mock a JAEGIS error
        mock_jaegis_interface.submit_command.side_effect = Exception("JAEGIS connection failed")
        integration_orchestrator.jaegis_interface = mock_jaegis_interface
        
        from nlds.translation import JAEGISCommand
        command = JAEGISCommand(
            command_id="test_cmd_001",
            command_type="analysis",
            target_squad="content_squad",
            mode_level=3,
            parameters=[],
            priority="normal"
        )
        
        # Should handle error gracefully
        result = await integration_orchestrator.submit_jaegis_command(command)
        
        assert not result.success
        assert "connection failed" in result.error_message.lower()


class TestAMASIAPIntegration:
    """Test integration with A.M.A.S.I.A.P. Protocol."""
    
    @pytest.fixture
    def mock_amasiap_engine(self):
        """Mock A.M.A.S.I.A.P. engine for testing."""
        mock = AsyncMock()
        mock.initialize_protocol.return_value = True
        mock.process_input.return_value = Mock(
            enhanced_input="Enhanced input with context [Context: 2025-07-26 12:00:00 UTC] [Domain Context: technology]",
            enhancement_quality_score=0.95,
            research_relevance_score=0.88,
            overall_improvement_score=0.91,
            enhancement_metadata={
                "temporal_context_added": True,
                "domain_context_added": True,
                "research_context_added": True
            }
        )
        return mock
    
    @pytest.mark.asyncio
    async def test_amasiap_input_enhancement(self, integration_orchestrator, mock_amasiap_engine):
        """Test A.M.A.S.I.A.P. input enhancement integration."""
        integration_orchestrator.amasiap_engine = mock_amasiap_engine
        
        original_input = "Analyze market trends"
        
        # Process input through A.M.A.S.I.A.P.
        result = await integration_orchestrator.enhance_input_with_amasiap(original_input)
        
        assert result.success
        assert result.enhanced_input != original_input
        assert result.enhancement_quality_score >= 0.9
        assert "Context:" in result.enhanced_input
        
        # Verify engine was called correctly
        mock_amasiap_engine.process_input.assert_called_once_with(original_input)
    
    @pytest.mark.asyncio
    async def test_amasiap_research_framework_activation(self, integration_orchestrator, mock_amasiap_engine):
        """Test A.M.A.S.I.A.P. research framework activation."""
        integration_orchestrator.amasiap_engine = mock_amasiap_engine
        
        # Mock research framework activation
        mock_amasiap_engine.activate_research_framework.return_value = {
            "research_queries": [
                "Current renewable energy market trends 2025",
                "Investment opportunities renewable energy Q4 2025",
                "Strategic recommendations energy sector"
            ],
            "research_results": [
                {"query": "trends", "relevance": 0.95, "data": "Market data..."},
                {"query": "opportunities", "relevance": 0.88, "data": "Investment data..."}
            ],
            "synthesis": "Comprehensive market analysis with investment recommendations"
        }
        
        input_text = "Analyze renewable energy investment opportunities"
        
        # Activate research framework
        result = await integration_orchestrator.activate_amasiap_research(input_text)
        
        assert result.success
        assert len(result.research_queries) > 0
        assert len(result.research_results) > 0
        assert result.synthesis is not None
    
    @pytest.mark.asyncio
    async def test_amasiap_context_injection(self, integration_orchestrator, mock_amasiap_engine):
        """Test A.M.A.S.I.A.P. context injection."""
        integration_orchestrator.amasiap_engine = mock_amasiap_engine
        
        # Test with different context types
        context_scenarios = [
            {"domain": "technology", "urgency": "high"},
            {"domain": "finance", "audience": "executives"},
            {"domain": "healthcare", "compliance": "HIPAA"}
        ]
        
        for context in context_scenarios:
            result = await integration_orchestrator.enhance_input_with_amasiap(
                "Test input",
                additional_context=context
            )
            
            assert result.success
            assert any(key in result.enhanced_input.lower() for key in context.keys())


class TestOpenRouterIntegration:
    """Test integration with OpenRouter.ai system."""
    
    @pytest.fixture
    def mock_openrouter_engine(self):
        """Mock OpenRouter engine for testing."""
        mock = AsyncMock()
        mock.initialize_integration.return_value = True
        mock.select_optimal_model.return_value = {
            "model_id": "gpt-4-turbo",
            "provider": "openai",
            "confidence": 0.95,
            "cost_per_token": 0.00001,
            "estimated_cost": 0.05
        }
        mock.process_request.return_value = {
            "response": "Detailed analysis response from AI model",
            "usage": {
                "prompt_tokens": 150,
                "completion_tokens": 300,
                "total_tokens": 450
            },
            "cost": 0.045,
            "model_used": "gpt-4-turbo",
            "processing_time_ms": 1200
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_openrouter_model_selection(self, integration_orchestrator, mock_openrouter_engine):
        """Test OpenRouter optimal model selection."""
        integration_orchestrator.openrouter_engine = mock_openrouter_engine
        
        request_context = {
            "task_type": "analysis",
            "complexity": "high",
            "budget_limit": 0.10,
            "quality_requirement": "premium"
        }
        
        # Select optimal model
        model_info = await integration_orchestrator.select_openrouter_model(request_context)
        
        assert model_info.model_id is not None
        assert model_info.provider is not None
        assert model_info.confidence >= 0.9
        assert model_info.estimated_cost <= request_context["budget_limit"]
        
        # Verify engine was called correctly
        mock_openrouter_engine.select_optimal_model.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_openrouter_load_balancing(self, integration_orchestrator, mock_openrouter_engine):
        """Test OpenRouter load balancing across API keys."""
        integration_orchestrator.openrouter_engine = mock_openrouter_engine
        
        # Mock load balancing
        mock_openrouter_engine.get_available_keys.return_value = [
            {"key_id": "key_001", "usage": 0.2, "rate_limit_remaining": 1000},
            {"key_id": "key_002", "usage": 0.8, "rate_limit_remaining": 200},
            {"key_id": "key_003", "usage": 0.1, "rate_limit_remaining": 1500}
        ]
        
        # Should select key with lowest usage and highest remaining limit
        selected_key = await integration_orchestrator.select_openrouter_key()
        
        assert selected_key.key_id == "key_003"  # Lowest usage, highest remaining
    
    @pytest.mark.asyncio
    async def test_openrouter_concurrent_requests(self, integration_orchestrator, mock_openrouter_engine):
        """Test OpenRouter concurrent request handling."""
        integration_orchestrator.openrouter_engine = mock_openrouter_engine
        
        # Process multiple requests concurrently
        requests = [
            {"prompt": f"Analyze topic {i}", "max_tokens": 100}
            for i in range(10)
        ]
        
        tasks = [
            integration_orchestrator.process_openrouter_request(req)
            for req in requests
        ]
        
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert len(results) == len(requests)
        for result in results:
            assert result.success
            assert result.response is not None
            assert result.usage is not None


class TestGitHubIntegration:
    """Test integration with GitHub system."""
    
    @pytest.fixture
    def mock_github_interface(self):
        """Mock GitHub interface for testing."""
        mock = AsyncMock()
        mock.initialize_integration.return_value = True
        mock.fetch_resource.return_value = {
            "content": "# JAEGIS Command Template\n\nCommand structure...",
            "last_modified": datetime.utcnow(),
            "cache_hit": False,
            "file_path": "commands/analysis_template.md"
        }
        mock.sync_resources.return_value = {
            "synced_count": 15,
            "updated_count": 3,
            "errors": [],
            "sync_duration_ms": 2500
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_github_resource_fetching(self, integration_orchestrator, mock_github_interface):
        """Test GitHub resource fetching integration."""
        integration_orchestrator.github_interface = mock_github_interface
        
        resource_path = "commands/analysis_template.md"
        
        # Fetch resource
        result = await integration_orchestrator.fetch_github_resource(resource_path)
        
        assert result.success
        assert result.content is not None
        assert "JAEGIS" in result.content
        assert result.last_modified is not None
        
        # Verify interface was called correctly
        mock_github_interface.fetch_resource.assert_called_once_with(resource_path)
    
    @pytest.mark.asyncio
    async def test_github_dynamic_resource_loading(self, integration_orchestrator, mock_github_interface):
        """Test dynamic resource loading from GitHub."""
        integration_orchestrator.github_interface = mock_github_interface
        
        # Mock dynamic resource discovery
        mock_github_interface.discover_resources.return_value = [
            {"path": "commands/analysis.md", "type": "command_template"},
            {"path": "squads/content_squad.md", "type": "squad_definition"},
            {"path": "modes/mode_3.md", "type": "mode_specification"}
        ]
        
        # Load resources dynamically
        resources = await integration_orchestrator.load_dynamic_resources("commands")
        
        assert len(resources) > 0
        for resource in resources:
            assert resource.path is not None
            assert resource.type is not None
            assert resource.content is not None
    
    @pytest.mark.asyncio
    async def test_github_sync_system(self, integration_orchestrator, mock_github_interface):
        """Test GitHub synchronization system."""
        integration_orchestrator.github_interface = mock_github_interface
        
        # Trigger sync
        result = await integration_orchestrator.sync_github_resources()
        
        assert result.success
        assert result.synced_count > 0
        assert len(result.errors) == 0
        assert result.sync_duration_ms > 0
        
        # Verify interface was called correctly
        mock_github_interface.sync_resources.assert_called_once()


class TestAPIIntegration:
    """Test API integration with all components."""
    
    @pytest.fixture
    def api_client(self):
        """Create API test client."""
        return create_test_client()
    
    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers."""
        return {"Authorization": "Bearer nlds_admin_key_001"}
    
    @pytest.mark.asyncio
    async def test_api_complete_workflow(self, api_client, auth_headers):
        """Test complete API workflow integration."""
        # Step 1: Process input
        process_response = api_client.post("/process", json={
            "input_text": "Analyze market trends for renewable energy sector",
            "mode": "enhanced",
            "enable_amasiap": True
        }, headers=auth_headers)
        
        assert process_response.status_code == 200
        process_data = process_response.json()
        assert process_data["success"]
        
        # Step 2: Analyze processed input
        analyze_response = api_client.post("/analyze", json={
            "input_text": process_data["enhanced_input"],
            "analysis_types": ["comprehensive"],
            "depth_level": 3
        }, headers=auth_headers)
        
        assert analyze_response.status_code == 200
        analyze_data = analyze_response.json()
        assert "synthesis" in analyze_data
        
        # Step 3: Translate to JAEGIS command
        translate_response = api_client.post("/translate", json={
            "input_text": process_data["enhanced_input"],
            "target_mode": 3,
            "priority": "normal"
        }, headers=auth_headers)
        
        assert translate_response.status_code == 200
        translate_data = translate_response.json()
        assert "jaegis_command" in translate_data
        
        # Step 4: Submit JAEGIS command
        submit_response = api_client.post("/jaegis/submit", json={
            "command": translate_data["jaegis_command"],
            "priority": "normal",
            "timeout_seconds": 300
        }, headers=auth_headers)
        
        assert submit_response.status_code == 200
        submit_data = submit_response.json()
        assert "command_id" in submit_data
        
        # Step 5: Check command status
        command_id = submit_data["command_id"]
        status_response = api_client.get(f"/jaegis/status/{command_id}", headers=auth_headers)
        
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert "status" in status_data
    
    def test_api_error_propagation(self, api_client, auth_headers):
        """Test error propagation through API layers."""
        # Test with invalid input that should trigger errors
        invalid_response = api_client.post("/process", json={
            "input_text": "",  # Invalid empty input
            "mode": "enhanced"
        }, headers=auth_headers)
        
        assert invalid_response.status_code == 400
        error_data = invalid_response.json()
        assert "error" in error_data
        assert "validation" in error_data["error"]["message"].lower()
    
    def test_api_performance_monitoring(self, api_client, auth_headers):
        """Test API performance monitoring integration."""
        # Make request and check performance headers
        response = api_client.post("/process", json={
            "input_text": "Test performance monitoring",
            "mode": "standard"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        
        # Check performance headers
        assert "X-Response-Time" in response.headers
        assert "X-Request-ID" in response.headers
        
        # Response time should be reasonable
        response_time = float(response.headers["X-Response-Time"].replace("ms", ""))
        assert response_time < 2000  # Less than 2 seconds
