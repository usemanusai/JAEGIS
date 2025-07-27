"""
Unit Tests for N.L.D.S. Analysis Module
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive unit tests for the analysis orchestrator and multi-dimensional analysis components.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from typing import Dict, Any

from nlds.analysis import (
    AnalysisOrchestrator,
    LogicalAnalyzer,
    EmotionalAnalyzer,
    CreativeAnalyzer,
    AnalysisSynthesizer,
    AnalysisResult,
    AnalysisError,
    AnalysisType
)


class TestLogicalAnalyzer:
    """Test cases for LogicalAnalyzer."""
    
    def test_analyze_structured_input(self):
        """Test logical analysis of structured input."""
        analyzer = LogicalAnalyzer()
        
        structured_inputs = [
            "First, analyze the market. Then, identify opportunities. Finally, create recommendations.",
            "If sales increase by 20%, then we should expand operations.",
            "Given the current trends, we can conclude that investment is necessary.",
        ]
        
        for input_text in structured_inputs:
            result = analyzer.analyze(input_text)
            
            assert result.logical_structure is not None
            assert result.confidence > 0.7
            assert len(result.requirements) > 0
            assert result.reasoning_type in ["sequential", "conditional", "causal"]
    
    def test_analyze_unstructured_input(self):
        """Test logical analysis of unstructured input."""
        analyzer = LogicalAnalyzer()
        
        unstructured_inputs = [
            "I need help with stuff",
            "Random thoughts about things",
            "Maybe we should do something",
        ]
        
        for input_text in unstructured_inputs:
            result = analyzer.analyze(input_text)
            
            assert result.confidence < 0.6
            assert len(result.improvement_suggestions) > 0
    
    def test_requirement_extraction(self):
        """Test extraction of logical requirements."""
        analyzer = LogicalAnalyzer()
        
        input_text = "Create a business plan that includes market analysis, financial projections, and risk assessment."
        result = analyzer.analyze(input_text)
        
        requirements = [req.lower() for req in result.requirements]
        assert any("market analysis" in req for req in requirements)
        assert any("financial" in req for req in requirements)
        assert any("risk" in req for req in requirements)
    
    def test_logical_flow_detection(self):
        """Test detection of logical flow patterns."""
        analyzer = LogicalAnalyzer()
        
        sequential_input = "First step is research. Second step is analysis. Third step is implementation."
        result = analyzer.analyze(sequential_input)
        
        assert result.logical_structure == "sequential"
        assert result.flow_indicators is not None
        assert len(result.flow_indicators) >= 3
    
    def test_conditional_logic_detection(self):
        """Test detection of conditional logic."""
        analyzer = LogicalAnalyzer()
        
        conditional_input = "If the market conditions improve, then we should invest. Otherwise, we should wait."
        result = analyzer.analyze(conditional_input)
        
        assert result.reasoning_type == "conditional"
        assert "conditions" in result.metadata
        assert "outcomes" in result.metadata


class TestEmotionalAnalyzer:
    """Test cases for EmotionalAnalyzer."""
    
    def test_analyze_positive_sentiment(self):
        """Test analysis of positive emotional content."""
        analyzer = EmotionalAnalyzer()
        
        positive_inputs = [
            "I'm excited about this amazing opportunity!",
            "This is a fantastic project with great potential.",
            "We're thrilled to move forward with this initiative.",
        ]
        
        for input_text in positive_inputs:
            result = analyzer.analyze(input_text)
            
            assert result.sentiment in ["positive", "very_positive"]
            assert result.confidence > 0.6
            assert result.emotional_intensity > 0.5
    
    def test_analyze_negative_sentiment(self):
        """Test analysis of negative emotional content."""
        analyzer = EmotionalAnalyzer()
        
        negative_inputs = [
            "I'm frustrated with the current situation.",
            "This is a terrible idea that won't work.",
            "I'm worried about the potential risks.",
        ]
        
        for input_text in negative_inputs:
            result = analyzer.analyze(input_text)
            
            assert result.sentiment in ["negative", "very_negative"]
            assert result.confidence > 0.6
    
    def test_analyze_neutral_sentiment(self):
        """Test analysis of neutral emotional content."""
        analyzer = EmotionalAnalyzer()
        
        neutral_inputs = [
            "Please analyze the quarterly reports.",
            "The meeting is scheduled for 3 PM.",
            "Here are the technical specifications.",
        ]
        
        for input_text in neutral_inputs:
            result = analyzer.analyze(input_text)
            
            assert result.sentiment == "neutral"
            assert result.emotional_intensity < 0.3
    
    def test_emotion_detection(self):
        """Test detection of specific emotions."""
        analyzer = EmotionalAnalyzer()
        
        emotion_inputs = {
            "joy": "I'm so happy about this success!",
            "fear": "I'm afraid this might not work out.",
            "anger": "This is completely unacceptable!",
            "surprise": "I can't believe this happened!",
            "sadness": "I'm disappointed with the results.",
        }
        
        for expected_emotion, input_text in emotion_inputs.items():
            result = analyzer.analyze(input_text)
            
            assert expected_emotion in result.detected_emotions
            assert result.confidence > 0.5
    
    def test_emotional_context_analysis(self):
        """Test analysis of emotional context."""
        analyzer = EmotionalAnalyzer()
        
        input_text = "I'm cautiously optimistic about the project, but concerned about the timeline."
        result = analyzer.analyze(input_text)
        
        # Should detect mixed emotions
        assert len(result.detected_emotions) > 1
        assert "optimism" in result.detected_emotions or "hope" in result.detected_emotions
        assert "concern" in result.detected_emotions or "worry" in result.detected_emotions


class TestCreativeAnalyzer:
    """Test cases for CreativeAnalyzer."""
    
    def test_analyze_creative_input(self):
        """Test analysis of creative content."""
        analyzer = CreativeAnalyzer()
        
        creative_inputs = [
            "Let's think outside the box and revolutionize the industry with innovative solutions.",
            "Imagine a world where AI and humans collaborate seamlessly to solve complex problems.",
            "What if we could transform this challenge into an opportunity for breakthrough innovation?",
        ]
        
        for input_text in creative_inputs:
            result = analyzer.analyze(input_text)
            
            assert result.creativity_score > 0.6
            assert result.innovation_potential in ["medium", "high", "very_high"]
            assert len(result.creative_patterns) > 0
    
    def test_analyze_conventional_input(self):
        """Test analysis of conventional content."""
        analyzer = CreativeAnalyzer()
        
        conventional_inputs = [
            "Please prepare the standard quarterly report.",
            "Follow the established procedures for this task.",
            "Use the existing template for the documentation.",
        ]
        
        for input_text in conventional_inputs:
            result = analyzer.analyze(input_text)
            
            assert result.creativity_score < 0.4
            assert result.innovation_potential in ["low", "very_low"]
    
    def test_pattern_recognition(self):
        """Test recognition of creative patterns."""
        analyzer = CreativeAnalyzer()
        
        pattern_inputs = {
            "metaphor": "The market is a battlefield where only the strongest survive.",
            "analogy": "Like a symphony, our team needs to work in harmony.",
            "brainstorming": "What if we tried approach A, or maybe B, or even C?",
            "visionary": "Envision a future where technology enhances human potential.",
        }
        
        for pattern_type, input_text in pattern_inputs.items():
            result = analyzer.analyze(input_text)
            
            pattern_names = [p.lower() for p in result.creative_patterns]
            assert any(pattern_type in name for name in pattern_names)
    
    def test_innovation_assessment(self):
        """Test assessment of innovation potential."""
        analyzer = CreativeAnalyzer()
        
        high_innovation_input = "Let's disrupt the traditional model with a completely new paradigm."
        result = analyzer.analyze(high_innovation_input)
        
        assert result.innovation_potential in ["high", "very_high"]
        assert result.disruptive_potential > 0.7
        assert "innovation_indicators" in result.metadata
    
    def test_creative_suggestions(self):
        """Test generation of creative suggestions."""
        analyzer = CreativeAnalyzer()
        
        basic_input = "Improve the current process."
        result = analyzer.analyze(basic_input)
        
        if result.creativity_score < 0.5:
            assert len(result.enhancement_suggestions) > 0
            suggestions = [s.lower() for s in result.enhancement_suggestions]
            assert any("creative" in s or "innovative" in s for s in suggestions)


class TestAnalysisSynthesizer:
    """Test cases for AnalysisSynthesizer."""
    
    def test_synthesize_balanced_analysis(self):
        """Test synthesis of balanced multi-dimensional analysis."""
        synthesizer = AnalysisSynthesizer()
        
        # Mock analysis results
        logical_result = Mock(
            confidence=0.85,
            requirements=["req1", "req2"],
            logical_structure="sequential"
        )
        
        emotional_result = Mock(
            confidence=0.75,
            sentiment="positive",
            emotional_intensity=0.6
        )
        
        creative_result = Mock(
            confidence=0.80,
            creativity_score=0.7,
            innovation_potential="high"
        )
        
        synthesis = synthesizer.synthesize(logical_result, emotional_result, creative_result)
        
        assert synthesis.overall_confidence > 0.7
        assert synthesis.recommended_approach is not None
        assert len(synthesis.key_insights) > 0
        assert synthesis.confidence_distribution is not None
    
    def test_synthesize_conflicting_analysis(self):
        """Test synthesis when analyses conflict."""
        synthesizer = AnalysisSynthesizer()
        
        # High logical confidence, low emotional/creative
        logical_result = Mock(confidence=0.9, requirements=["clear_req"])
        emotional_result = Mock(confidence=0.3, sentiment="neutral")
        creative_result = Mock(confidence=0.2, creativity_score=0.1)
        
        synthesis = synthesizer.synthesize(logical_result, emotional_result, creative_result)
        
        assert synthesis.dominant_dimension == "logical"
        assert "confidence_variance" in synthesis.metadata
        assert synthesis.recommended_approach == "logical_focused"
    
    def test_synthesize_low_confidence(self):
        """Test synthesis with low confidence across all dimensions."""
        synthesizer = AnalysisSynthesizer()
        
        low_confidence_results = [
            Mock(confidence=0.3),
            Mock(confidence=0.2),
            Mock(confidence=0.4)
        ]
        
        synthesis = synthesizer.synthesize(*low_confidence_results)
        
        assert synthesis.overall_confidence < 0.5
        assert len(synthesis.improvement_recommendations) > 0
        assert "low_confidence_warning" in synthesis.metadata


class TestAnalysisOrchestrator:
    """Test cases for AnalysisOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self, sample_config):
        """Create analysis orchestrator for testing."""
        return AnalysisOrchestrator(sample_config["analysis"])
    
    @pytest.mark.asyncio
    async def test_analyze_comprehensive(self, orchestrator, sample_input_text):
        """Test comprehensive analysis."""
        result = await orchestrator.analyze(
            sample_input_text,
            analysis_types=[AnalysisType.COMPREHENSIVE]
        )
        
        assert isinstance(result, AnalysisResult)
        assert result.logical_analysis is not None
        assert result.emotional_analysis is not None
        assert result.creative_analysis is not None
        assert result.synthesis is not None
        assert result.overall_confidence > 0.0
    
    @pytest.mark.asyncio
    async def test_analyze_specific_types(self, orchestrator, sample_input_text):
        """Test analysis with specific types."""
        result = await orchestrator.analyze(
            sample_input_text,
            analysis_types=[AnalysisType.LOGICAL, AnalysisType.EMOTIONAL]
        )
        
        assert result.logical_analysis is not None
        assert result.emotional_analysis is not None
        assert result.creative_analysis is None  # Not requested
    
    @pytest.mark.asyncio
    async def test_analyze_with_depth_levels(self, orchestrator, sample_input_text):
        """Test analysis with different depth levels."""
        for depth in range(1, 6):
            result = await orchestrator.analyze(
                sample_input_text,
                depth_level=depth
            )
            
            assert result.depth_level == depth
            # Higher depth should generally mean more detailed analysis
            if depth > 3:
                assert len(result.metadata) > 5
    
    @pytest.mark.asyncio
    async def test_analyze_invalid_input(self, orchestrator):
        """Test analysis with invalid input."""
        invalid_inputs = ["", "   ", None]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(AnalysisError):
                await orchestrator.analyze(invalid_input)
    
    @pytest.mark.asyncio
    async def test_analyze_performance(self, orchestrator, sample_input_text, assert_async_timing):
        """Test analysis performance requirements."""
        # Analysis should complete within 2 seconds
        result = await assert_async_timing(
            orchestrator.analyze(sample_input_text),
            max_time_ms=2000
        )
        
        assert result.processing_time_ms < 2000
    
    @pytest.mark.asyncio
    async def test_analyze_concurrent_requests(self, orchestrator):
        """Test concurrent analysis requests."""
        inputs = [
            "Analyze market trends",
            "Create business strategy",
            "Develop innovation plan",
            "Assess risk factors",
            "Optimize operations"
        ]
        
        tasks = [orchestrator.analyze(inp) for inp in inputs]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == len(inputs)
        for result in results:
            assert isinstance(result, AnalysisResult)
            assert result.overall_confidence > 0.0
    
    @pytest.mark.asyncio
    async def test_analyze_with_context(self, orchestrator, sample_input_text):
        """Test analysis with additional context."""
        context = {
            "domain": "technology",
            "audience": "executives",
            "purpose": "strategic_planning"
        }
        
        result = await orchestrator.analyze(sample_input_text, context=context)
        
        assert "context_influence" in result.metadata
        assert result.overall_confidence > 0.0
    
    @pytest.mark.asyncio
    async def test_analyze_error_handling(self, orchestrator):
        """Test error handling during analysis."""
        # Mock an internal error
        with patch.object(orchestrator.logical_analyzer, 'analyze') as mock_analyze:
            mock_analyze.side_effect = Exception("Internal error")
            
            with pytest.raises(AnalysisError):
                await orchestrator.analyze("test input")
    
    @pytest.mark.asyncio
    async def test_analyze_timeout_handling(self, orchestrator):
        """Test timeout handling during analysis."""
        # Mock a slow analysis operation
        with patch.object(orchestrator.logical_analyzer, 'analyze', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.side_effect = asyncio.TimeoutError()
            
            with pytest.raises(AnalysisError) as exc_info:
                await orchestrator.analyze("test input")
            
            assert "timeout" in str(exc_info.value).lower()
    
    def test_orchestrator_configuration(self, sample_config):
        """Test orchestrator configuration."""
        orchestrator = AnalysisOrchestrator(sample_config["analysis"])
        
        assert orchestrator.config["logical_weight"] == 0.4
        assert orchestrator.config["emotional_weight"] == 0.3
        assert orchestrator.config["creative_weight"] == 0.3
        assert orchestrator.config["depth_levels"] == 5
    
    def test_orchestrator_weight_validation(self):
        """Test validation of analysis weights."""
        # Weights should sum to 1.0
        valid_config = {
            "logical_weight": 0.5,
            "emotional_weight": 0.3,
            "creative_weight": 0.2,
            "depth_levels": 5
        }
        
        orchestrator = AnalysisOrchestrator(valid_config)
        assert abs(sum([
            orchestrator.config["logical_weight"],
            orchestrator.config["emotional_weight"],
            orchestrator.config["creative_weight"]
        ]) - 1.0) < 0.001
    
    @pytest.mark.asyncio
    async def test_analyze_batch_processing(self, orchestrator):
        """Test batch analysis processing."""
        inputs = [
            "First analysis input",
            "Second analysis input",
            "Third analysis input"
        ]
        
        results = await orchestrator.analyze_batch(inputs)
        
        assert len(results) == len(inputs)
        for i, result in enumerate(results):
            assert isinstance(result, AnalysisResult)
            assert result.input_text == inputs[i]
