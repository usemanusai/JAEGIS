"""
Confidence Accuracy Validation Tests
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive validation tests to ensure the N.L.D.S. system maintains
≥85% confidence threshold accuracy across all components and scenarios.
"""

import pytest
import asyncio
import statistics
from typing import List, Dict, Any, Tuple
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
import json
import random

from nlds.processing import ProcessingOrchestrator
from nlds.analysis import AnalysisOrchestrator, AnalysisType
from nlds.translation import TranslationOrchestrator
from nlds.integration import NLDSIntegrationOrchestrator


class ConfidenceValidator:
    """Confidence validation utilities."""
    
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.validation_results = []
    
    def validate_confidence_score(self, confidence: float, context: str = "") -> Dict[str, Any]:
        """Validate a confidence score against threshold."""
        is_valid = confidence >= self.threshold
        
        result = {
            "confidence": confidence,
            "threshold": self.threshold,
            "is_valid": is_valid,
            "context": context,
            "timestamp": datetime.utcnow(),
            "deviation": confidence - self.threshold
        }
        
        self.validation_results.append(result)
        return result
    
    def validate_confidence_distribution(self, confidences: List[float]) -> Dict[str, Any]:
        """Validate confidence distribution."""
        if not confidences:
            return {"error": "No confidence scores provided"}
        
        valid_count = sum(1 for c in confidences if c >= self.threshold)
        total_count = len(confidences)
        accuracy_rate = valid_count / total_count
        
        return {
            "total_scores": total_count,
            "valid_scores": valid_count,
            "accuracy_rate": accuracy_rate,
            "meets_threshold": accuracy_rate >= 0.85,  # 85% of scores should meet threshold
            "mean_confidence": statistics.mean(confidences),
            "median_confidence": statistics.median(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences),
            "std_dev": statistics.stdev(confidences) if len(confidences) > 1 else 0
        }
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get overall validation summary."""
        if not self.validation_results:
            return {"error": "No validation results"}
        
        valid_results = [r for r in self.validation_results if r["is_valid"]]
        accuracy_rate = len(valid_results) / len(self.validation_results)
        
        return {
            "total_validations": len(self.validation_results),
            "valid_validations": len(valid_results),
            "accuracy_rate": accuracy_rate,
            "meets_requirement": accuracy_rate >= 0.85,
            "mean_confidence": statistics.mean(r["confidence"] for r in self.validation_results),
            "mean_deviation": statistics.mean(r["deviation"] for r in self.validation_results)
        }


class TestProcessingConfidenceAccuracy:
    """Test processing component confidence accuracy."""
    
    @pytest.fixture
    def confidence_validator(self):
        """Create confidence validator."""
        return ConfidenceValidator(threshold=0.85)
    
    @pytest.fixture
    def processing_orchestrator(self, sample_config):
        """Create processing orchestrator."""
        return ProcessingOrchestrator(sample_config["processing"])
    
    @pytest.mark.asyncio
    async def test_high_quality_input_confidence(self, processing_orchestrator, confidence_validator):
        """Test confidence accuracy for high-quality inputs."""
        high_quality_inputs = [
            "Analyze the current market trends for renewable energy sector and provide comprehensive strategic recommendations for investment opportunities in Q4 2025",
            "Create a detailed business plan for a sustainable technology startup focusing on AI-powered energy management solutions",
            "Develop a comprehensive risk assessment framework for digital transformation initiatives in healthcare organizations",
            "Design an innovative product roadmap for next-generation electric vehicle charging infrastructure",
            "Formulate a strategic partnership strategy for expanding into emerging markets in Southeast Asia"
        ]
        
        confidences = []
        for input_text in high_quality_inputs:
            result = await processing_orchestrator.process_input(input_text)
            
            assert result.success
            confidences.append(result.confidence_score)
            
            # Validate individual confidence
            validation = confidence_validator.validate_confidence_score(
                result.confidence_score,
                f"High-quality input: {input_text[:50]}..."
            )
            
            # High-quality inputs should consistently meet threshold
            assert validation["is_valid"], f"High-quality input confidence {result.confidence_score:.3f} below threshold"
        
        # Validate overall distribution
        distribution = confidence_validator.validate_confidence_distribution(confidences)
        assert distribution["accuracy_rate"] >= 0.90, f"High-quality input accuracy rate {distribution['accuracy_rate']:.2%} below 90%"
        assert distribution["mean_confidence"] >= 0.88, f"Mean confidence {distribution['mean_confidence']:.3f} below expected 0.88"
    
    @pytest.mark.asyncio
    async def test_medium_quality_input_confidence(self, processing_orchestrator, confidence_validator):
        """Test confidence accuracy for medium-quality inputs."""
        medium_quality_inputs = [
            "Analyze market trends for technology",
            "Create business plan for startup",
            "Develop risk assessment for project",
            "Design product roadmap",
            "Plan marketing strategy"
        ]
        
        confidences = []
        for input_text in medium_quality_inputs:
            result = await processing_orchestrator.process_input(input_text)
            
            assert result.success
            confidences.append(result.confidence_score)
            
            confidence_validator.validate_confidence_score(
                result.confidence_score,
                f"Medium-quality input: {input_text}"
            )
        
        # Medium-quality inputs should have lower but reasonable confidence
        distribution = confidence_validator.validate_confidence_distribution(confidences)
        assert distribution["mean_confidence"] >= 0.70, f"Medium-quality mean confidence {distribution['mean_confidence']:.3f} too low"
        assert distribution["mean_confidence"] <= 0.85, f"Medium-quality mean confidence {distribution['mean_confidence']:.3f} unexpectedly high"
    
    @pytest.mark.asyncio
    async def test_low_quality_input_confidence(self, processing_orchestrator, confidence_validator):
        """Test confidence accuracy for low-quality inputs."""
        low_quality_inputs = [
            "do stuff",
            "help me",
            "idk",
            "something",
            "fix it"
        ]
        
        confidences = []
        for input_text in low_quality_inputs:
            result = await processing_orchestrator.process_input(input_text)
            
            assert result.success
            confidences.append(result.confidence_score)
            
            confidence_validator.validate_confidence_score(
                result.confidence_score,
                f"Low-quality input: {input_text}"
            )
        
        # Low-quality inputs should have appropriately low confidence
        distribution = confidence_validator.validate_confidence_distribution(confidences)
        assert distribution["mean_confidence"] <= 0.70, f"Low-quality mean confidence {distribution['mean_confidence']:.3f} too high"
        assert distribution["max_confidence"] <= 0.80, f"Low-quality max confidence {distribution['max_confidence']:.3f} too high"
    
    @pytest.mark.asyncio
    async def test_confidence_calibration_accuracy(self, processing_orchestrator, confidence_validator):
        """Test confidence calibration accuracy."""
        # Test inputs with known expected confidence ranges
        calibration_tests = [
            ("Comprehensive strategic analysis of global renewable energy market trends with detailed investment recommendations", 0.85, 0.95),
            ("Analyze renewable energy market trends", 0.70, 0.85),
            ("Market analysis", 0.60, 0.80),
            ("help with analysis", 0.40, 0.70),
            ("help", 0.20, 0.60)
        ]
        
        calibration_accuracy = []
        
        for input_text, min_expected, max_expected in calibration_tests:
            result = await processing_orchestrator.process_input(input_text)
            
            assert result.success
            confidence = result.confidence_score
            
            # Check if confidence falls within expected range
            is_calibrated = min_expected <= confidence <= max_expected
            calibration_accuracy.append(is_calibrated)
            
            confidence_validator.validate_confidence_score(
                confidence,
                f"Calibration test: {input_text[:30]}... (expected: {min_expected:.2f}-{max_expected:.2f})"
            )
        
        # At least 80% of calibration tests should be accurate
        accuracy_rate = sum(calibration_accuracy) / len(calibration_accuracy)
        assert accuracy_rate >= 0.80, f"Confidence calibration accuracy {accuracy_rate:.2%} below 80%"


class TestAnalysisConfidenceAccuracy:
    """Test analysis component confidence accuracy."""
    
    @pytest.fixture
    def analysis_orchestrator(self, sample_config):
        """Create analysis orchestrator."""
        return AnalysisOrchestrator(sample_config["analysis"])
    
    @pytest.mark.asyncio
    async def test_comprehensive_analysis_confidence(self, analysis_orchestrator):
        """Test comprehensive analysis confidence accuracy."""
        validator = ConfidenceValidator()
        
        comprehensive_inputs = [
            "Develop a comprehensive digital transformation strategy for a Fortune 500 manufacturing company",
            "Create an innovative product development framework for sustainable consumer electronics",
            "Design a strategic market entry plan for emerging technologies in the healthcare sector",
            "Formulate a comprehensive risk management strategy for cryptocurrency investments",
            "Establish a global supply chain optimization framework for e-commerce operations"
        ]
        
        confidences = []
        for input_text in comprehensive_inputs:
            result = await analysis_orchestrator.analyze(
                input_text,
                analysis_types=[AnalysisType.COMPREHENSIVE],
                depth_level=4
            )
            
            assert result.overall_confidence > 0.0
            confidences.append(result.overall_confidence)
            
            # Validate individual analysis components
            validator.validate_confidence_score(
                result.logical_analysis.confidence,
                f"Logical analysis: {input_text[:30]}..."
            )
            validator.validate_confidence_score(
                result.emotional_analysis.confidence,
                f"Emotional analysis: {input_text[:30]}..."
            )
            validator.validate_confidence_score(
                result.creative_analysis.confidence,
                f"Creative analysis: {input_text[:30]}..."
            )
        
        # Comprehensive analysis should have high confidence
        distribution = validator.validate_confidence_distribution(confidences)
        assert distribution["accuracy_rate"] >= 0.80, f"Comprehensive analysis accuracy rate {distribution['accuracy_rate']:.2%} below 80%"
        assert distribution["mean_confidence"] >= 0.80, f"Mean comprehensive confidence {distribution['mean_confidence']:.3f} below 0.80"
    
    @pytest.mark.asyncio
    async def test_analysis_depth_confidence_correlation(self, analysis_orchestrator):
        """Test correlation between analysis depth and confidence."""
        validator = ConfidenceValidator()
        
        test_input = "Create strategic business plan for AI-powered healthcare solutions"
        depth_confidences = {}
        
        for depth in range(1, 6):
            result = await analysis_orchestrator.analyze(
                test_input,
                analysis_types=[AnalysisType.COMPREHENSIVE],
                depth_level=depth
            )
            
            depth_confidences[depth] = result.overall_confidence
            
            validator.validate_confidence_score(
                result.overall_confidence,
                f"Depth {depth} analysis"
            )
        
        # Higher depth should generally correlate with higher confidence
        # (though not strictly monotonic due to complexity)
        depth_3_confidence = depth_confidences[3]
        depth_5_confidence = depth_confidences[5]
        
        assert depth_5_confidence >= depth_3_confidence * 0.95, "Deeper analysis should maintain or improve confidence"
    
    @pytest.mark.asyncio
    async def test_multi_dimensional_confidence_consistency(self, analysis_orchestrator):
        """Test confidence consistency across analysis dimensions."""
        validator = ConfidenceValidator()
        
        test_inputs = [
            "Develop innovative marketing strategy for sustainable products",
            "Create technical architecture for distributed AI systems",
            "Design emotional intelligence training program for leadership",
            "Formulate creative problem-solving methodology for R&D teams"
        ]
        
        dimension_confidences = {
            "logical": [],
            "emotional": [],
            "creative": []
        }
        
        for input_text in test_inputs:
            result = await analysis_orchestrator.analyze(
                input_text,
                analysis_types=[AnalysisType.LOGICAL, AnalysisType.EMOTIONAL, AnalysisType.CREATIVE]
            )
            
            dimension_confidences["logical"].append(result.logical_analysis.confidence)
            dimension_confidences["emotional"].append(result.emotional_analysis.confidence)
            dimension_confidences["creative"].append(result.creative_analysis.confidence)
        
        # Validate each dimension
        for dimension, confidences in dimension_confidences.items():
            distribution = validator.validate_confidence_distribution(confidences)
            assert distribution["mean_confidence"] >= 0.70, f"{dimension} analysis mean confidence {distribution['mean_confidence']:.3f} too low"


class TestTranslationConfidenceAccuracy:
    """Test translation component confidence accuracy."""
    
    @pytest.fixture
    def translation_orchestrator(self, sample_config):
        """Create translation orchestrator."""
        return TranslationOrchestrator(sample_config["translation"])
    
    @pytest.mark.asyncio
    async def test_high_confidence_translation_accuracy(self, translation_orchestrator):
        """Test translation accuracy for high-confidence analysis results."""
        validator = ConfidenceValidator()
        
        # Create high-confidence analysis results
        high_confidence_analyses = []
        for i in range(10):
            analysis_result = Mock(
                logical_analysis=Mock(
                    confidence=0.90 + random.uniform(0, 0.08),
                    requirements=["analyze", "recommend", "strategize"],
                    logical_structure="sequential"
                ),
                emotional_analysis=Mock(
                    confidence=0.85 + random.uniform(0, 0.10),
                    sentiment="positive",
                    emotional_intensity=0.7
                ),
                creative_analysis=Mock(
                    confidence=0.88 + random.uniform(0, 0.10),
                    creativity_score=0.8,
                    innovation_potential="high"
                ),
                synthesis=Mock(
                    overall_confidence=0.88 + random.uniform(0, 0.10),
                    recommended_approach="comprehensive"
                )
            )
            high_confidence_analyses.append(analysis_result)
        
        translation_confidences = []
        for analysis_result in high_confidence_analyses:
            result = await translation_orchestrator.translate(analysis_result)
            
            assert result.success
            translation_confidences.append(result.confidence_score)
            
            validator.validate_confidence_score(
                result.confidence_score,
                f"High-confidence translation (input confidence: {analysis_result.synthesis.overall_confidence:.3f})"
            )
        
        # High-confidence inputs should produce high-confidence translations
        distribution = validator.validate_confidence_distribution(translation_confidences)
        assert distribution["accuracy_rate"] >= 0.90, f"High-confidence translation accuracy {distribution['accuracy_rate']:.2%} below 90%"
        assert distribution["mean_confidence"] >= 0.85, f"Mean translation confidence {distribution['mean_confidence']:.3f} below 0.85"
    
    @pytest.mark.asyncio
    async def test_confidence_propagation_accuracy(self, translation_orchestrator):
        """Test confidence propagation from analysis to translation."""
        validator = ConfidenceValidator()
        
        # Test confidence propagation with varying input confidences
        confidence_levels = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70]
        propagation_accuracy = []
        
        for input_confidence in confidence_levels:
            analysis_result = Mock(
                synthesis=Mock(
                    overall_confidence=input_confidence,
                    recommended_approach="analytical"
                ),
                logical_analysis=Mock(confidence=input_confidence),
                emotional_analysis=Mock(confidence=input_confidence),
                creative_analysis=Mock(confidence=input_confidence)
            )
            
            result = await translation_orchestrator.translate(analysis_result)
            
            assert result.success
            output_confidence = result.confidence_score
            
            # Translation confidence should be correlated with input confidence
            confidence_ratio = output_confidence / input_confidence
            is_reasonable_propagation = 0.8 <= confidence_ratio <= 1.1
            propagation_accuracy.append(is_reasonable_propagation)
            
            validator.validate_confidence_score(
                output_confidence,
                f"Confidence propagation: {input_confidence:.3f} -> {output_confidence:.3f}"
            )
        
        # At least 80% of propagations should be reasonable
        accuracy_rate = sum(propagation_accuracy) / len(propagation_accuracy)
        assert accuracy_rate >= 0.80, f"Confidence propagation accuracy {accuracy_rate:.2%} below 80%"


class TestEndToEndConfidenceAccuracy:
    """Test end-to-end confidence accuracy."""
    
    @pytest.mark.asyncio
    async def test_complete_pipeline_confidence_accuracy(self, integration_orchestrator):
        """Test confidence accuracy through complete pipeline."""
        validator = ConfidenceValidator()
        
        # Test scenarios with expected confidence ranges
        test_scenarios = [
            {
                "input": "Develop comprehensive strategic plan for digital transformation in healthcare with detailed implementation roadmap and risk assessment",
                "expected_min": 0.85,
                "category": "high_quality"
            },
            {
                "input": "Create business strategy for technology startup",
                "expected_min": 0.75,
                "category": "medium_quality"
            },
            {
                "input": "Analyze market trends",
                "expected_min": 0.65,
                "category": "basic_quality"
            },
            {
                "input": "Help with planning",
                "expected_min": 0.50,
                "category": "low_quality"
            }
        ]
        
        pipeline_confidences = []
        category_results = {}
        
        for scenario in test_scenarios:
            result = await integration_orchestrator.process_complete_pipeline(
                input_text=scenario["input"],
                user_context={"user_id": "confidence_test_user"}
            )
            
            assert result.success
            
            # Collect confidences from each stage
            processing_confidence = result.processing_result.confidence_score
            analysis_confidence = result.analysis_result.overall_confidence
            translation_confidence = result.translation_result.confidence_score
            overall_confidence = result.overall_confidence
            
            pipeline_confidences.append(overall_confidence)
            
            # Validate each stage
            validator.validate_confidence_score(processing_confidence, f"Processing: {scenario['category']}")
            validator.validate_confidence_score(analysis_confidence, f"Analysis: {scenario['category']}")
            validator.validate_confidence_score(translation_confidence, f"Translation: {scenario['category']}")
            validator.validate_confidence_score(overall_confidence, f"Overall: {scenario['category']}")
            
            # Track by category
            if scenario["category"] not in category_results:
                category_results[scenario["category"]] = []
            category_results[scenario["category"]].append({
                "input": scenario["input"],
                "expected_min": scenario["expected_min"],
                "actual": overall_confidence,
                "meets_expectation": overall_confidence >= scenario["expected_min"]
            })
        
        # Validate overall pipeline confidence
        distribution = validator.validate_confidence_distribution(pipeline_confidences)
        assert distribution["accuracy_rate"] >= 0.75, f"Pipeline confidence accuracy {distribution['accuracy_rate']:.2%} below 75%"
        
        # Validate category-specific results
        for category, results in category_results.items():
            category_accuracy = sum(r["meets_expectation"] for r in results) / len(results)
            assert category_accuracy >= 0.75, f"Category {category} accuracy {category_accuracy:.2%} below 75%"
    
    @pytest.mark.asyncio
    async def test_confidence_threshold_compliance(self, integration_orchestrator):
        """Test compliance with 85% confidence threshold requirement."""
        validator = ConfidenceValidator(threshold=0.85)
        
        # Test with inputs that should meet the 85% threshold
        high_quality_inputs = [
            "Conduct comprehensive market analysis for renewable energy sector including competitive landscape, regulatory environment, and investment opportunities with detailed financial projections",
            "Design innovative product development strategy for AI-powered healthcare solutions with focus on patient outcomes, regulatory compliance, and market penetration",
            "Create strategic digital transformation roadmap for manufacturing company including technology assessment, implementation phases, and ROI analysis",
            "Develop comprehensive risk management framework for financial services organization with focus on cybersecurity, regulatory compliance, and operational resilience",
            "Formulate global expansion strategy for e-commerce platform including market entry analysis, localization requirements, and partnership opportunities"
        ]
        
        threshold_compliance_results = []
        
        for input_text in high_quality_inputs:
            result = await integration_orchestrator.process_complete_pipeline(
                input_text=input_text,
                user_context={"user_id": "threshold_test_user"}
            )
            
            assert result.success
            
            # Check if overall confidence meets threshold
            meets_threshold = result.overall_confidence >= 0.85
            threshold_compliance_results.append(meets_threshold)
            
            validator.validate_confidence_score(
                result.overall_confidence,
                f"Threshold compliance test: {input_text[:50]}..."
            )
        
        # At least 80% of high-quality inputs should meet the 85% threshold
        compliance_rate = sum(threshold_compliance_results) / len(threshold_compliance_results)
        assert compliance_rate >= 0.80, f"Threshold compliance rate {compliance_rate:.2%} below 80%"
        
        # Get overall validation summary
        summary = validator.get_validation_summary()
        assert summary["meets_requirement"], f"Overall confidence accuracy requirement not met: {summary['accuracy_rate']:.2%}"


class TestConfidenceReliability:
    """Test confidence score reliability and consistency."""
    
    @pytest.mark.asyncio
    async def test_confidence_consistency_across_runs(self, integration_orchestrator):
        """Test confidence consistency across multiple runs."""
        test_input = "Create strategic business plan for sustainable technology startup"
        
        # Run the same input multiple times
        confidences = []
        for run in range(10):
            result = await integration_orchestrator.process_complete_pipeline(
                input_text=test_input,
                user_context={"user_id": f"consistency_test_{run}"}
            )
            
            assert result.success
            confidences.append(result.overall_confidence)
        
        # Confidence should be consistent (low variance)
        mean_confidence = statistics.mean(confidences)
        std_dev = statistics.stdev(confidences) if len(confidences) > 1 else 0
        coefficient_of_variation = std_dev / mean_confidence if mean_confidence > 0 else 0
        
        # Coefficient of variation should be low (< 10%)
        assert coefficient_of_variation < 0.10, f"Confidence inconsistency: CV {coefficient_of_variation:.3f} too high"
        assert std_dev < 0.05, f"Confidence standard deviation {std_dev:.3f} too high"
    
    @pytest.mark.asyncio
    async def test_confidence_monotonicity(self, processing_orchestrator):
        """Test confidence monotonicity with input quality."""
        # Inputs ordered from low to high quality
        quality_ordered_inputs = [
            "help",
            "help me",
            "help with analysis",
            "help with market analysis",
            "help with comprehensive market analysis",
            "conduct comprehensive market analysis for renewable energy",
            "conduct comprehensive market analysis for renewable energy sector with detailed recommendations"
        ]
        
        confidences = []
        for input_text in quality_ordered_inputs:
            result = await processing_orchestrator.process_input(input_text)
            assert result.success
            confidences.append(result.confidence_score)
        
        # Check for general upward trend (allowing some variation)
        # Use moving averages to smooth out noise
        window_size = 3
        moving_averages = []
        for i in range(len(confidences) - window_size + 1):
            avg = statistics.mean(confidences[i:i + window_size])
            moving_averages.append(avg)
        
        # Moving averages should show upward trend
        trend_violations = 0
        for i in range(1, len(moving_averages)):
            if moving_averages[i] < moving_averages[i-1] * 0.95:  # Allow 5% tolerance
                trend_violations += 1
        
        violation_rate = trend_violations / (len(moving_averages) - 1) if len(moving_averages) > 1 else 0
        assert violation_rate <= 0.3, f"Too many monotonicity violations: {violation_rate:.2%}"
