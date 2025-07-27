"""
Unit Tests for N.L.D.S. Translation Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive unit tests for the translation orchestrator and JAEGIS command generation.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from typing import Dict, Any, List

from nlds.translation import (
    TranslationOrchestrator,
    CommandGenerator,
    ModeSelector,
    SquadSelector,
    ConfidenceValidator,
    AlternativeGenerator,
    TranslationResult,
    TranslationError,
    JAEGISCommand,
    JAEGISMode,
    JAEGISSquad
)


class TestCommandGenerator:
    """Test cases for CommandGenerator."""
    
    def test_generate_basic_command(self):
        """Test generation of basic JAEGIS command."""
        generator = CommandGenerator()
        
        analysis_result = Mock(
            logical_analysis=Mock(
                requirements=["analyze", "recommend"],
                confidence=0.85
            ),
            emotional_analysis=Mock(
                sentiment="positive",
                confidence=0.80
            ),
            creative_analysis=Mock(
                innovation_potential="medium",
                confidence=0.75
            ),
            synthesis=Mock(
                overall_confidence=0.80,
                recommended_approach="comprehensive"
            )
        )
        
        command = generator.generate(analysis_result)
        
        assert isinstance(command, JAEGISCommand)
        assert command.command_id is not None
        assert command.command_type is not None
        assert len(command.parameters) > 0
        assert command.confidence_score >= 0.75
    
    def test_generate_command_with_context(self):
        """Test command generation with additional context."""
        generator = CommandGenerator()
        
        analysis_result = Mock(
            synthesis=Mock(
                overall_confidence=0.85,
                recommended_approach="logical_focused"
            )
        )
        
        context = {
            "urgency": "high",
            "domain": "technology",
            "user_preferences": {"detail_level": "comprehensive"}
        }
        
        command = generator.generate(analysis_result, context)
        
        assert command.priority == "high"  # Should reflect urgency
        assert "domain_context" in command.metadata
        assert command.estimated_duration > 0
    
    def test_generate_command_types(self):
        """Test generation of different command types."""
        generator = CommandGenerator()
        
        command_scenarios = {
            "analysis": Mock(
                synthesis=Mock(
                    recommended_approach="analytical",
                    key_insights=["data_analysis", "trend_identification"]
                )
            ),
            "creative": Mock(
                synthesis=Mock(
                    recommended_approach="creative_focused",
                    key_insights=["innovation", "brainstorming"]
                )
            ),
            "strategic": Mock(
                synthesis=Mock(
                    recommended_approach="strategic",
                    key_insights=["planning", "decision_making"]
                )
            )
        }
        
        for expected_type, analysis_result in command_scenarios.items():
            command = generator.generate(analysis_result)
            assert expected_type in command.command_type.lower()
    
    def test_parameter_extraction(self):
        """Test extraction of command parameters."""
        generator = CommandGenerator()
        
        analysis_result = Mock(
            logical_analysis=Mock(
                requirements=["market_analysis", "financial_projections"],
                entities=["Q4 2025", "renewable energy", "investment"]
            ),
            synthesis=Mock(
                overall_confidence=0.88,
                recommended_approach="comprehensive"
            )
        )
        
        command = generator.generate(analysis_result)
        
        # Should extract relevant parameters
        param_values = [p.value for p in command.parameters]
        assert any("market" in str(val).lower() for val in param_values)
        assert any("financial" in str(val).lower() for val in param_values)


class TestModeSelector:
    """Test cases for ModeSelector."""
    
    def test_select_mode_by_complexity(self):
        """Test mode selection based on complexity."""
        selector = ModeSelector()
        
        complexity_scenarios = [
            (["simple task"], 1),  # Simple -> Mode 1
            (["analyze", "compare"], 2),  # Medium -> Mode 2
            (["analyze", "synthesize", "recommend"], 3),  # Complex -> Mode 3
            (["comprehensive analysis", "strategic planning", "implementation"], 4),  # Very complex -> Mode 4
            (["enterprise transformation", "multi-stakeholder coordination"], 5)  # Extreme -> Mode 5
        ]
        
        for requirements, expected_mode in complexity_scenarios:
            analysis_result = Mock(
                logical_analysis=Mock(requirements=requirements),
                synthesis=Mock(overall_confidence=0.85)
            )
            
            mode = selector.select_mode(analysis_result)
            assert mode.level == expected_mode
    
    def test_select_mode_by_confidence(self):
        """Test mode selection influenced by confidence."""
        selector = ModeSelector()
        
        # High confidence should allow higher modes
        high_confidence_analysis = Mock(
            logical_analysis=Mock(requirements=["complex task"]),
            synthesis=Mock(overall_confidence=0.95)
        )
        
        # Low confidence should prefer lower modes
        low_confidence_analysis = Mock(
            logical_analysis=Mock(requirements=["complex task"]),
            synthesis=Mock(overall_confidence=0.60)
        )
        
        high_mode = selector.select_mode(high_confidence_analysis)
        low_mode = selector.select_mode(low_confidence_analysis)
        
        assert high_mode.level >= low_mode.level
    
    def test_mode_characteristics(self):
        """Test mode characteristics and capabilities."""
        selector = ModeSelector()
        
        for level in range(1, 6):
            mode = JAEGISMode(level)
            
            assert mode.level == level
            assert mode.name is not None
            assert mode.description is not None
            assert len(mode.capabilities) > 0
            assert mode.resource_requirements > 0
            
            # Higher modes should have more capabilities and resources
            if level > 1:
                prev_mode = JAEGISMode(level - 1)
                assert len(mode.capabilities) >= len(prev_mode.capabilities)
                assert mode.resource_requirements >= prev_mode.resource_requirements


class TestSquadSelector:
    """Test cases for SquadSelector."""
    
    def test_select_squad_by_domain(self):
        """Test squad selection based on domain analysis."""
        selector = SquadSelector()
        
        domain_scenarios = {
            "content": ["writing", "documentation", "content creation"],
            "research": ["analysis", "investigation", "data gathering"],
            "creative": ["innovation", "brainstorming", "design"],
            "technical": ["development", "implementation", "coding"],
            "strategic": ["planning", "strategy", "decision making"]
        }
        
        for expected_squad, keywords in domain_scenarios.items():
            analysis_result = Mock(
                logical_analysis=Mock(
                    requirements=keywords,
                    entities=keywords
                ),
                creative_analysis=Mock(
                    creative_patterns=keywords if expected_squad == "creative" else []
                ),
                synthesis=Mock(overall_confidence=0.85)
            )
            
            squad = selector.select_squad(analysis_result)
            assert expected_squad in squad.name.lower()
    
    def test_select_squad_by_complexity(self):
        """Test squad selection based on task complexity."""
        selector = SquadSelector()
        
        # Simple task should select basic squad
        simple_analysis = Mock(
            logical_analysis=Mock(requirements=["simple task"]),
            synthesis=Mock(overall_confidence=0.85)
        )
        
        # Complex task should select specialized squad
        complex_analysis = Mock(
            logical_analysis=Mock(
                requirements=["multi-phase analysis", "cross-functional coordination"]
            ),
            synthesis=Mock(overall_confidence=0.85)
        )
        
        simple_squad = selector.select_squad(simple_analysis)
        complex_squad = selector.select_squad(complex_analysis)
        
        # Complex tasks should get more capable squads
        assert complex_squad.capability_level >= simple_squad.capability_level
    
    def test_squad_capabilities(self):
        """Test squad capabilities and specializations."""
        selector = SquadSelector()
        
        # Test all available squads
        for squad_name in selector.available_squads:
            squad = JAEGISSquad(squad_name)
            
            assert squad.name == squad_name
            assert squad.description is not None
            assert len(squad.specializations) > 0
            assert len(squad.capabilities) > 0
            assert squad.capability_level > 0
    
    def test_fallback_squad_selection(self):
        """Test fallback squad selection for unclear requirements."""
        selector = SquadSelector()
        
        unclear_analysis = Mock(
            logical_analysis=Mock(requirements=["unclear", "vague"]),
            synthesis=Mock(overall_confidence=0.40)
        )
        
        squad = selector.select_squad(unclear_analysis)
        
        # Should select a general-purpose squad
        assert "general" in squad.name.lower() or "content" in squad.name.lower()


class TestConfidenceValidator:
    """Test cases for ConfidenceValidator."""
    
    def test_validate_high_confidence(self):
        """Test validation of high confidence translations."""
        validator = ConfidenceValidator(threshold=0.85)
        
        high_confidence_command = Mock(
            confidence_score=0.92,
            command_type="analysis",
            parameters=[Mock(confidence=0.90), Mock(confidence=0.88)]
        )
        
        result = validator.validate(high_confidence_command)
        
        assert result.is_valid
        assert result.confidence_score >= 0.85
        assert result.validation_details is not None
    
    def test_validate_low_confidence(self):
        """Test validation of low confidence translations."""
        validator = ConfidenceValidator(threshold=0.85)
        
        low_confidence_command = Mock(
            confidence_score=0.70,
            command_type="analysis",
            parameters=[Mock(confidence=0.65), Mock(confidence=0.75)]
        )
        
        result = validator.validate(low_confidence_command)
        
        assert not result.is_valid
        assert len(result.improvement_suggestions) > 0
        assert "confidence" in result.failure_reason.lower()
    
    def test_validate_parameter_confidence(self):
        """Test validation of individual parameter confidence."""
        validator = ConfidenceValidator(threshold=0.85)
        
        mixed_confidence_command = Mock(
            confidence_score=0.88,
            command_type="analysis",
            parameters=[
                Mock(confidence=0.95),  # High confidence
                Mock(confidence=0.60),  # Low confidence
                Mock(confidence=0.90)   # High confidence
            ]
        )
        
        result = validator.validate(mixed_confidence_command)
        
        # Overall might be valid, but should flag low-confidence parameters
        assert "parameter_warnings" in result.validation_details
    
    def test_confidence_threshold_adjustment(self):
        """Test dynamic confidence threshold adjustment."""
        validator = ConfidenceValidator(threshold=0.85)
        
        # Threshold should adjust based on command complexity
        simple_command = Mock(
            confidence_score=0.80,
            command_type="simple",
            complexity_score=0.3
        )
        
        complex_command = Mock(
            confidence_score=0.80,
            command_type="complex",
            complexity_score=0.9
        )
        
        simple_result = validator.validate(simple_command)
        complex_result = validator.validate(complex_command)
        
        # Simple commands might pass with lower confidence
        # Complex commands should require higher confidence
        assert simple_result.effective_threshold <= complex_result.effective_threshold


class TestAlternativeGenerator:
    """Test cases for AlternativeGenerator."""
    
    def test_generate_alternatives_for_low_confidence(self):
        """Test generation of alternatives for low confidence commands."""
        generator = AlternativeGenerator()
        
        low_confidence_command = Mock(
            confidence_score=0.60,
            command_type="analysis",
            parameters=[Mock(value="vague requirement")]
        )
        
        analysis_result = Mock(
            logical_analysis=Mock(requirements=["unclear task"]),
            synthesis=Mock(overall_confidence=0.60)
        )
        
        alternatives = generator.generate_alternatives(low_confidence_command, analysis_result)
        
        assert len(alternatives) > 0
        for alt in alternatives:
            assert isinstance(alt, JAEGISCommand)
            assert alt.command_id != low_confidence_command.command_id
    
    def test_generate_alternatives_with_different_approaches(self):
        """Test generation of alternatives with different approaches."""
        generator = AlternativeGenerator()
        
        original_command = Mock(
            confidence_score=0.70,
            command_type="analysis",
            approach="comprehensive"
        )
        
        analysis_result = Mock(
            synthesis=Mock(
                overall_confidence=0.70,
                alternative_approaches=["focused", "iterative", "collaborative"]
            )
        )
        
        alternatives = generator.generate_alternatives(original_command, analysis_result)
        
        # Should generate alternatives with different approaches
        approaches = [alt.approach for alt in alternatives if hasattr(alt, 'approach')]
        assert len(set(approaches)) > 1  # Multiple different approaches
    
    def test_alternative_ranking(self):
        """Test ranking of generated alternatives."""
        generator = AlternativeGenerator()
        
        command = Mock(confidence_score=0.65)
        analysis_result = Mock(synthesis=Mock(overall_confidence=0.65))
        
        alternatives = generator.generate_alternatives(command, analysis_result)
        
        # Alternatives should be ranked by confidence
        confidences = [alt.confidence_score for alt in alternatives]
        assert confidences == sorted(confidences, reverse=True)


class TestTranslationOrchestrator:
    """Test cases for TranslationOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self, sample_config):
        """Create translation orchestrator for testing."""
        return TranslationOrchestrator(sample_config["translation"])
    
    @pytest.mark.asyncio
    async def test_translate_high_confidence(self, orchestrator, sample_analysis_result):
        """Test translation of high confidence analysis."""
        result = await orchestrator.translate(sample_analysis_result)
        
        assert isinstance(result, TranslationResult)
        assert result.success
        assert result.primary_command is not None
        assert result.confidence_score >= 0.85
        assert len(result.alternative_commands) >= 0
    
    @pytest.mark.asyncio
    async def test_translate_low_confidence(self, orchestrator):
        """Test translation of low confidence analysis."""
        low_confidence_analysis = Mock(
            logical_analysis=Mock(confidence=0.50),
            emotional_analysis=Mock(confidence=0.45),
            creative_analysis=Mock(confidence=0.40),
            synthesis=Mock(overall_confidence=0.45)
        )
        
        result = await orchestrator.translate(low_confidence_analysis)
        
        # Should still succeed but with alternatives
        assert result.success
        assert result.confidence_score < 0.85
        assert len(result.alternative_commands) > 0
        assert len(result.improvement_suggestions) > 0
    
    @pytest.mark.asyncio
    async def test_translate_with_context(self, orchestrator, sample_analysis_result):
        """Test translation with additional context."""
        context = {
            "preferred_mode": 3,
            "preferred_squad": "content_squad",
            "urgency": "high",
            "constraints": ["budget_limited", "time_sensitive"]
        }
        
        result = await orchestrator.translate(sample_analysis_result, context)
        
        assert result.success
        assert result.primary_command.mode_level == 3
        assert "content" in result.primary_command.target_squad.lower()
        assert result.primary_command.priority == "high"
    
    @pytest.mark.asyncio
    async def test_translate_performance(self, orchestrator, sample_analysis_result, assert_async_timing):
        """Test translation performance requirements."""
        # Translation should complete within 500ms
        result = await assert_async_timing(
            orchestrator.translate(sample_analysis_result),
            max_time_ms=500
        )
        
        assert result.success
        assert result.processing_time_ms < 500
    
    @pytest.mark.asyncio
    async def test_translate_concurrent_requests(self, orchestrator):
        """Test concurrent translation requests."""
        analysis_results = [
            Mock(synthesis=Mock(overall_confidence=0.85 + i*0.01))
            for i in range(5)
        ]
        
        tasks = [orchestrator.translate(analysis) for analysis in analysis_results]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == len(analysis_results)
        for result in results:
            assert isinstance(result, TranslationResult)
            assert result.success
    
    @pytest.mark.asyncio
    async def test_translate_error_handling(self, orchestrator):
        """Test error handling during translation."""
        # Mock an internal error
        with patch.object(orchestrator.command_generator, 'generate') as mock_generate:
            mock_generate.side_effect = Exception("Internal error")
            
            with pytest.raises(TranslationError):
                await orchestrator.translate(Mock())
    
    @pytest.mark.asyncio
    async def test_translate_batch_processing(self, orchestrator):
        """Test batch translation processing."""
        analysis_results = [
            Mock(synthesis=Mock(overall_confidence=0.85)),
            Mock(synthesis=Mock(overall_confidence=0.90)),
            Mock(synthesis=Mock(overall_confidence=0.75))
        ]
        
        results = await orchestrator.translate_batch(analysis_results)
        
        assert len(results) == len(analysis_results)
        for result in results:
            assert isinstance(result, TranslationResult)
    
    def test_orchestrator_configuration(self, sample_config):
        """Test orchestrator configuration."""
        orchestrator = TranslationOrchestrator(sample_config["translation"])
        
        assert orchestrator.config["mode_selection_threshold"] == 0.8
        assert orchestrator.config["squad_selection_threshold"] == 0.75
        assert orchestrator.config["confidence_validation_threshold"] == 0.85
    
    @pytest.mark.asyncio
    async def test_translate_optimization(self, orchestrator, sample_analysis_result):
        """Test translation optimization features."""
        # Enable optimization
        result = await orchestrator.translate(
            sample_analysis_result,
            options={"enable_optimization": True, "cache_results": True}
        )
        
        assert result.success
        assert "optimization_applied" in result.metadata
        
        # Second call should be faster (cached)
        import time
        start_time = time.time()
        result2 = await orchestrator.translate(sample_analysis_result)
        elapsed = (time.time() - start_time) * 1000
        
        # Should be significantly faster due to caching
        assert elapsed < result.processing_time_ms
