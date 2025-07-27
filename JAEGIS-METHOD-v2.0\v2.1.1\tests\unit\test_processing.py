"""
Unit Tests for N.L.D.S. Processing Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive unit tests for the processing orchestrator and related components.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from typing import Dict, Any

from nlds.processing import (
    ProcessingOrchestrator,
    ProcessingResult,
    ProcessingError,
    InputValidator,
    ContextEnricher,
    QualityAssessor
)


class TestInputValidator:
    """Test cases for InputValidator."""
    
    def test_validate_valid_input(self):
        """Test validation of valid input."""
        validator = InputValidator()
        
        valid_inputs = [
            "Simple text input",
            "Multi-word input with punctuation!",
            "Input with numbers 123 and symbols @#$",
            "A" * 1000,  # Long but valid input
        ]
        
        for input_text in valid_inputs:
            result = validator.validate(input_text)
            assert result.is_valid
            assert result.error_message is None
            assert result.confidence_score > 0.8
    
    def test_validate_invalid_input(self):
        """Test validation of invalid input."""
        validator = InputValidator()
        
        invalid_inputs = [
            "",  # Empty string
            "   ",  # Only whitespace
            "A" * 10001,  # Too long
            None,  # None value
        ]
        
        for input_text in invalid_inputs:
            result = validator.validate(input_text)
            assert not result.is_valid
            assert result.error_message is not None
            assert result.confidence_score == 0.0
    
    def test_validate_edge_cases(self):
        """Test validation edge cases."""
        validator = InputValidator()
        
        # Exactly at length limit
        max_length_input = "A" * 10000
        result = validator.validate(max_length_input)
        assert result.is_valid
        
        # Special characters
        special_input = "Input with émojis 🚀 and ñoñó characters"
        result = validator.validate(special_input)
        assert result.is_valid
        
        # Mixed languages
        mixed_input = "English text with 中文 and العربية"
        result = validator.validate(mixed_input)
        assert result.is_valid
    
    def test_security_validation(self):
        """Test security-related validation."""
        validator = InputValidator()
        
        # Potentially malicious inputs should still be valid for processing
        # but flagged for security review
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
        ]
        
        for input_text in malicious_inputs:
            result = validator.validate(input_text)
            # Should be valid for processing but with security flags
            assert result.is_valid
            assert "security_flags" in result.metadata
            assert len(result.metadata["security_flags"]) > 0


class TestContextEnricher:
    """Test cases for ContextEnricher."""
    
    def test_enrich_basic_context(self):
        """Test basic context enrichment."""
        enricher = ContextEnricher()
        
        input_text = "Analyze market trends"
        context = {"domain": "finance"}
        
        result = enricher.enrich(input_text, context)
        
        assert result.enriched_context is not None
        assert "temporal_context" in result.enriched_context
        assert "domain_context" in result.enriched_context
        assert "system_context" in result.enriched_context
        assert result.enrichment_score > 0.0
    
    def test_enrich_empty_context(self):
        """Test enrichment with empty context."""
        enricher = ContextEnricher()
        
        input_text = "Simple input"
        context = {}
        
        result = enricher.enrich(input_text, context)
        
        # Should still provide basic enrichment
        assert result.enriched_context is not None
        assert "temporal_context" in result.enriched_context
        assert result.enrichment_score > 0.0
    
    def test_enrich_complex_context(self):
        """Test enrichment with complex context."""
        enricher = ContextEnricher()
        
        input_text = "Create strategic plan"
        context = {
            "domain": "business",
            "urgency": "high",
            "audience": "executives",
            "timeline": "Q4 2025",
            "budget": "unlimited"
        }
        
        result = enricher.enrich(input_text, context)
        
        assert result.enriched_context is not None
        assert result.enrichment_score > 0.7
        assert "domain_context" in result.enriched_context
        assert "urgency_context" in result.enriched_context
    
    def test_temporal_context_injection(self):
        """Test temporal context injection."""
        enricher = ContextEnricher()
        
        input_text = "What's happening now?"
        
        result = enricher.enrich(input_text, {})
        
        temporal_context = result.enriched_context["temporal_context"]
        assert "current_datetime" in temporal_context
        assert "timezone" in temporal_context
        assert "day_of_week" in temporal_context


class TestQualityAssessor:
    """Test cases for QualityAssessor."""
    
    def test_assess_high_quality_input(self):
        """Test assessment of high-quality input."""
        assessor = QualityAssessor()
        
        high_quality_inputs = [
            "Analyze the current market trends for renewable energy and provide strategic recommendations",
            "Create a comprehensive business plan for a sustainable technology startup",
            "Develop a detailed project timeline for implementing AI solutions in healthcare",
        ]
        
        for input_text in high_quality_inputs:
            result = assessor.assess(input_text)
            assert result.overall_score > 0.8
            assert result.clarity_score > 0.7
            assert result.completeness_score > 0.7
            assert result.specificity_score > 0.6
    
    def test_assess_low_quality_input(self):
        """Test assessment of low-quality input."""
        assessor = QualityAssessor()
        
        low_quality_inputs = [
            "do stuff",
            "help",
            "idk what to do",
            "asdfghjkl",
        ]
        
        for input_text in low_quality_inputs:
            result = assessor.assess(input_text)
            assert result.overall_score < 0.6
            assert len(result.improvement_suggestions) > 0
    
    def test_assess_medium_quality_input(self):
        """Test assessment of medium-quality input."""
        assessor = QualityAssessor()
        
        medium_quality_inputs = [
            "Analyze market trends",
            "Create a plan for the project",
            "Help me with business strategy",
        ]
        
        for input_text in medium_quality_inputs:
            result = assessor.assess(input_text)
            assert 0.5 <= result.overall_score <= 0.8
    
    def test_improvement_suggestions(self):
        """Test quality improvement suggestions."""
        assessor = QualityAssessor()
        
        vague_input = "do something"
        result = assessor.assess(vague_input)
        
        assert len(result.improvement_suggestions) > 0
        suggestions = [s.lower() for s in result.improvement_suggestions]
        
        # Should suggest being more specific
        assert any("specific" in s or "detail" in s for s in suggestions)


class TestProcessingOrchestrator:
    """Test cases for ProcessingOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self, sample_config):
        """Create processing orchestrator for testing."""
        return ProcessingOrchestrator(sample_config["processing"])
    
    @pytest.mark.asyncio
    async def test_process_valid_input(self, orchestrator, sample_input_text):
        """Test processing of valid input."""
        result = await orchestrator.process_input(sample_input_text)
        
        assert isinstance(result, ProcessingResult)
        assert result.success
        assert result.original_input == sample_input_text
        assert result.processed_input is not None
        assert result.confidence_score > 0.0
        assert result.processing_time_ms > 0
        assert result.metadata is not None
    
    @pytest.mark.asyncio
    async def test_process_with_context(self, orchestrator, sample_input_text):
        """Test processing with additional context."""
        context = {
            "domain": "technology",
            "urgency": "medium",
            "user_preferences": {"detail_level": "high"}
        }
        
        result = await orchestrator.process_input(sample_input_text, context)
        
        assert result.success
        assert "context_enrichment" in result.metadata
        assert result.confidence_score > 0.0
    
    @pytest.mark.asyncio
    async def test_process_invalid_input(self, orchestrator):
        """Test processing of invalid input."""
        invalid_inputs = ["", "   ", None, "A" * 10001]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ProcessingError):
                await orchestrator.process_input(invalid_input)
    
    @pytest.mark.asyncio
    async def test_process_timeout(self, orchestrator):
        """Test processing timeout handling."""
        # Mock a slow processing operation
        with patch.object(orchestrator, '_enhance_input', new_callable=AsyncMock) as mock_enhance:
            mock_enhance.side_effect = asyncio.TimeoutError()
            
            with pytest.raises(ProcessingError) as exc_info:
                await orchestrator.process_input("test input")
            
            assert "timeout" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_process_with_quality_threshold(self, orchestrator):
        """Test processing with quality threshold enforcement."""
        # Configure strict quality threshold
        orchestrator.config["quality_threshold"] = 0.9
        
        low_quality_input = "do stuff"
        
        result = await orchestrator.process_input(low_quality_input)
        
        # Should still process but with warnings
        assert result.success
        assert "quality_warnings" in result.metadata
    
    @pytest.mark.asyncio
    async def test_process_batch_inputs(self, orchestrator):
        """Test batch processing of multiple inputs."""
        inputs = [
            "Analyze market trends",
            "Create business plan",
            "Develop strategy"
        ]
        
        results = await orchestrator.process_batch(inputs)
        
        assert len(results) == len(inputs)
        for result in results:
            assert isinstance(result, ProcessingResult)
            assert result.success
    
    @pytest.mark.asyncio
    async def test_process_with_enhancement_disabled(self, orchestrator):
        """Test processing with enhancement disabled."""
        result = await orchestrator.process_input(
            "test input",
            options={"enable_enhancement": False}
        )
        
        assert result.success
        assert result.processed_input == result.original_input
    
    @pytest.mark.asyncio
    async def test_process_error_handling(self, orchestrator):
        """Test error handling during processing."""
        # Mock an internal error
        with patch.object(orchestrator, '_validate_input') as mock_validate:
            mock_validate.side_effect = Exception("Internal error")
            
            with pytest.raises(ProcessingError):
                await orchestrator.process_input("test input")
    
    @pytest.mark.asyncio
    async def test_process_metrics_collection(self, orchestrator):
        """Test metrics collection during processing."""
        result = await orchestrator.process_input("test input")
        
        assert "processing_metrics" in result.metadata
        metrics = result.metadata["processing_metrics"]
        assert "validation_time_ms" in metrics
        assert "enhancement_time_ms" in metrics
        assert "quality_assessment_time_ms" in metrics
    
    @pytest.mark.asyncio
    async def test_process_concurrent_requests(self, orchestrator):
        """Test concurrent processing requests."""
        inputs = ["input 1", "input 2", "input 3", "input 4", "input 5"]
        
        # Process all inputs concurrently
        tasks = [orchestrator.process_input(inp) for inp in inputs]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == len(inputs)
        for i, result in enumerate(results):
            assert result.success
            assert result.original_input == inputs[i]
    
    def test_orchestrator_configuration(self, sample_config):
        """Test orchestrator configuration."""
        orchestrator = ProcessingOrchestrator(sample_config["processing"])
        
        assert orchestrator.config["max_input_length"] == 10000
        assert orchestrator.config["timeout_seconds"] == 30
        assert orchestrator.config["confidence_threshold"] == 0.85
    
    def test_orchestrator_invalid_configuration(self):
        """Test orchestrator with invalid configuration."""
        invalid_configs = [
            {},  # Empty config
            {"max_input_length": -1},  # Invalid length
            {"timeout_seconds": 0},  # Invalid timeout
            {"confidence_threshold": 1.5},  # Invalid threshold
        ]
        
        for config in invalid_configs:
            with pytest.raises((ValueError, KeyError)):
                ProcessingOrchestrator(config)
    
    @pytest.mark.asyncio
    async def test_process_performance(self, orchestrator, sample_input_text, assert_async_timing):
        """Test processing performance requirements."""
        # Processing should complete within 1 second for normal input
        result = await assert_async_timing(
            orchestrator.process_input(sample_input_text),
            max_time_ms=1000
        )
        
        assert result.success
        assert result.processing_time_ms < 1000
    
    @pytest.mark.asyncio
    async def test_process_memory_usage(self, orchestrator):
        """Test memory usage during processing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Process multiple inputs
        for i in range(10):
            await orchestrator.process_input(f"Test input {i}")
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024
    
    @pytest.mark.asyncio
    async def test_process_state_isolation(self, orchestrator):
        """Test that processing requests don't interfere with each other."""
        # Process two different inputs concurrently
        task1 = orchestrator.process_input("First input")
        task2 = orchestrator.process_input("Second input")
        
        result1, result2 = await asyncio.gather(task1, task2)
        
        # Results should be independent
        assert result1.original_input == "First input"
        assert result2.original_input == "Second input"
        assert result1.processed_input != result2.processed_input
