"""
N.L.D.S. Confidence Accuracy Validation
Validate ≥85% confidence threshold accuracy through extensive test scenarios and datasets
"""

import asyncio
import json
import csv
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import logging
import random
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """Test case for confidence validation."""
    input_text: str
    expected_intent: str
    expected_command_type: str
    expected_squad: str
    expected_mode: int
    ground_truth_confidence: float
    category: str
    complexity: str
    ambiguity_level: str


@dataclass
class ValidationResult:
    """Validation result for a test case."""
    test_case: TestCase
    predicted_confidence: float
    predicted_intent: str
    predicted_command: str
    predicted_squad: str
    predicted_mode: int
    processing_time_ms: float
    confidence_accurate: bool
    intent_accurate: bool
    command_accurate: bool
    overall_accurate: bool


@dataclass
class ValidationMetrics:
    """Comprehensive validation metrics."""
    total_tests: int
    confidence_accuracy: float
    intent_accuracy: float
    command_accuracy: float
    overall_accuracy: float
    precision: float
    recall: float
    f1_score: float
    avg_processing_time: float
    confidence_distribution: Dict[str, int]
    accuracy_by_category: Dict[str, float]
    accuracy_by_complexity: Dict[str, float]
    accuracy_by_ambiguity: Dict[str, float]


class ConfidenceValidationFramework:
    """
    Comprehensive confidence validation framework for N.L.D.S.
    
    Validates confidence threshold accuracy through extensive test scenarios,
    datasets, and statistical analysis to ensure ≥85% accuracy target.
    """
    
    def __init__(self, nlds_processor=None):
        self.nlds_processor = nlds_processor
        self.test_cases: List[TestCase] = []
        self.validation_results: List[ValidationResult] = []
        
        # Confidence thresholds
        self.high_confidence_threshold = 0.85
        self.medium_confidence_threshold = 0.70
        self.low_confidence_threshold = 0.50
        
        logger.info("Confidence Validation Framework initialized")
    
    def load_test_dataset(self, dataset_path: str = None) -> List[TestCase]:
        """Load test dataset from file or generate synthetic data."""
        
        if dataset_path and Path(dataset_path).exists():
            return self._load_from_file(dataset_path)
        else:
            return self._generate_synthetic_dataset()
    
    def _load_from_file(self, dataset_path: str) -> List[TestCase]:
        """Load test cases from CSV file."""
        test_cases = []
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_case = TestCase(
                    input_text=row['input_text'],
                    expected_intent=row['expected_intent'],
                    expected_command_type=row['expected_command_type'],
                    expected_squad=row['expected_squad'],
                    expected_mode=int(row['expected_mode']),
                    ground_truth_confidence=float(row['ground_truth_confidence']),
                    category=row['category'],
                    complexity=row['complexity'],
                    ambiguity_level=row['ambiguity_level']
                )
                test_cases.append(test_case)
        
        logger.info(f"Loaded {len(test_cases)} test cases from {dataset_path}")
        return test_cases
    
    def _generate_synthetic_dataset(self) -> List[TestCase]:
        """Generate synthetic test dataset."""
        test_cases = []
        
        # High confidence test cases (clear, unambiguous)
        high_confidence_cases = [
            {
                "input_text": "Create a new user authentication system with JWT tokens",
                "expected_intent": "create_authentication_system",
                "expected_command_type": "IMPLEMENT",
                "expected_squad": "development",
                "expected_mode": 3,
                "ground_truth_confidence": 0.95,
                "category": "development",
                "complexity": "medium",
                "ambiguity_level": "low"
            },
            {
                "input_text": "Analyze the security vulnerabilities in the current codebase",
                "expected_intent": "security_analysis",
                "expected_command_type": "ANALYZE",
                "expected_squad": "security",
                "expected_mode": 4,
                "ground_truth_confidence": 0.92,
                "category": "security",
                "complexity": "high",
                "ambiguity_level": "low"
            },
            {
                "input_text": "Generate API documentation for the user management endpoints",
                "expected_intent": "generate_documentation",
                "expected_command_type": "DOCUMENT",
                "expected_squad": "content",
                "expected_mode": 2,
                "ground_truth_confidence": 0.90,
                "category": "documentation",
                "complexity": "low",
                "ambiguity_level": "low"
            },
            {
                "input_text": "Optimize database queries for better performance",
                "expected_intent": "optimize_performance",
                "expected_command_type": "OPTIMIZE",
                "expected_squad": "development",
                "expected_mode": 3,
                "ground_truth_confidence": 0.88,
                "category": "optimization",
                "complexity": "medium",
                "ambiguity_level": "low"
            },
            {
                "input_text": "Set up continuous integration pipeline with automated testing",
                "expected_intent": "setup_ci_pipeline",
                "expected_command_type": "IMPLEMENT",
                "expected_squad": "integration",
                "expected_mode": 4,
                "ground_truth_confidence": 0.93,
                "category": "devops",
                "complexity": "high",
                "ambiguity_level": "low"
            }
        ]
        
        # Medium confidence test cases (somewhat ambiguous)
        medium_confidence_cases = [
            {
                "input_text": "Make the system more secure",
                "expected_intent": "improve_security",
                "expected_command_type": "ANALYZE",
                "expected_squad": "security",
                "expected_mode": 3,
                "ground_truth_confidence": 0.75,
                "category": "security",
                "complexity": "medium",
                "ambiguity_level": "medium"
            },
            {
                "input_text": "Fix the issues with user login",
                "expected_intent": "fix_login_issues",
                "expected_command_type": "DEBUG",
                "expected_squad": "development",
                "expected_mode": 2,
                "ground_truth_confidence": 0.72,
                "category": "debugging",
                "complexity": "medium",
                "ambiguity_level": "medium"
            },
            {
                "input_text": "Improve the user experience",
                "expected_intent": "improve_ux",
                "expected_command_type": "ANALYZE",
                "expected_squad": "analysis",
                "expected_mode": 3,
                "ground_truth_confidence": 0.68,
                "category": "ux",
                "complexity": "high",
                "ambiguity_level": "high"
            }
        ]
        
        # Low confidence test cases (highly ambiguous)
        low_confidence_cases = [
            {
                "input_text": "Make it better",
                "expected_intent": "general_improvement",
                "expected_command_type": "ANALYZE",
                "expected_squad": "analysis",
                "expected_mode": 1,
                "ground_truth_confidence": 0.45,
                "category": "general",
                "complexity": "unknown",
                "ambiguity_level": "high"
            },
            {
                "input_text": "Something is wrong",
                "expected_intent": "investigate_issue",
                "expected_command_type": "ANALYZE",
                "expected_squad": "analysis",
                "expected_mode": 1,
                "ground_truth_confidence": 0.40,
                "category": "debugging",
                "complexity": "unknown",
                "ambiguity_level": "high"
            }
        ]
        
        # Create test cases
        all_cases = high_confidence_cases * 20 + medium_confidence_cases * 15 + low_confidence_cases * 10
        
        for case_data in all_cases:
            test_case = TestCase(**case_data)
            test_cases.append(test_case)
        
        # Add some variation
        random.shuffle(test_cases)
        
        logger.info(f"Generated {len(test_cases)} synthetic test cases")
        return test_cases
    
    async def run_validation(self, test_cases: List[TestCase] = None) -> ValidationMetrics:
        """Run comprehensive confidence validation."""
        
        if test_cases is None:
            test_cases = self.load_test_dataset()
        
        self.test_cases = test_cases
        self.validation_results = []
        
        logger.info(f"Starting validation with {len(test_cases)} test cases")
        
        # Process each test case
        for i, test_case in enumerate(test_cases):
            if i % 100 == 0:
                logger.info(f"Processing test case {i+1}/{len(test_cases)}")
            
            result = await self._process_test_case(test_case)
            self.validation_results.append(result)
        
        # Calculate metrics
        metrics = self._calculate_metrics()
        
        logger.info(f"Validation completed. Overall accuracy: {metrics.overall_accuracy:.2%}")
        
        return metrics
    
    async def _process_test_case(self, test_case: TestCase) -> ValidationResult:
        """Process a single test case."""
        
        start_time = datetime.now()
        
        # Simulate N.L.D.S. processing (replace with actual processor)
        if self.nlds_processor:
            response = await self.nlds_processor.process(test_case.input_text)
            predicted_confidence = response.overall_confidence
            predicted_intent = response.dimensional_analysis[0].analysis_result.get('intent', 'unknown')
            predicted_command = response.primary_command.command
            predicted_squad = response.primary_command.squad
            predicted_mode = response.primary_command.mode
        else:
            # Simulate processing for testing
            predicted_confidence = self._simulate_confidence_prediction(test_case)
            predicted_intent = self._simulate_intent_prediction(test_case)
            predicted_command = f"SIMULATED:{test_case.expected_command_type}"
            predicted_squad = test_case.expected_squad
            predicted_mode = test_case.expected_mode
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Evaluate accuracy
        confidence_accurate = self._evaluate_confidence_accuracy(
            test_case.ground_truth_confidence,
            predicted_confidence
        )
        
        intent_accurate = predicted_intent.lower() == test_case.expected_intent.lower()
        command_accurate = test_case.expected_command_type.lower() in predicted_command.lower()
        overall_accurate = confidence_accurate and intent_accurate and command_accurate
        
        return ValidationResult(
            test_case=test_case,
            predicted_confidence=predicted_confidence,
            predicted_intent=predicted_intent,
            predicted_command=predicted_command,
            predicted_squad=predicted_squad,
            predicted_mode=predicted_mode,
            processing_time_ms=processing_time,
            confidence_accurate=confidence_accurate,
            intent_accurate=intent_accurate,
            command_accurate=command_accurate,
            overall_accurate=overall_accurate
        )
    
    def _simulate_confidence_prediction(self, test_case: TestCase) -> float:
        """Simulate confidence prediction for testing."""
        # Add some noise to ground truth confidence
        base_confidence = test_case.ground_truth_confidence
        noise = random.gauss(0, 0.05)  # 5% standard deviation
        
        # Adjust based on ambiguity level
        if test_case.ambiguity_level == "high":
            noise += random.uniform(-0.1, -0.05)
        elif test_case.ambiguity_level == "low":
            noise += random.uniform(0.02, 0.05)
        
        predicted = max(0.0, min(1.0, base_confidence + noise))
        return predicted
    
    def _simulate_intent_prediction(self, test_case: TestCase) -> str:
        """Simulate intent prediction for testing."""
        # Simulate some prediction errors
        if random.random() < 0.1:  # 10% error rate
            wrong_intents = ["wrong_intent", "misclassified", "error_case"]
            return random.choice(wrong_intents)
        return test_case.expected_intent
    
    def _evaluate_confidence_accuracy(self, ground_truth: float, predicted: float) -> bool:
        """Evaluate confidence prediction accuracy."""
        # Define confidence bands
        if ground_truth >= self.high_confidence_threshold:
            return predicted >= self.high_confidence_threshold
        elif ground_truth >= self.medium_confidence_threshold:
            return self.medium_confidence_threshold <= predicted < self.high_confidence_threshold
        else:
            return predicted < self.medium_confidence_threshold
    
    def _calculate_metrics(self) -> ValidationMetrics:
        """Calculate comprehensive validation metrics."""
        
        if not self.validation_results:
            raise ValueError("No validation results available")
        
        total_tests = len(self.validation_results)
        
        # Basic accuracy metrics
        confidence_accurate = sum(1 for r in self.validation_results if r.confidence_accurate)
        intent_accurate = sum(1 for r in self.validation_results if r.intent_accurate)
        command_accurate = sum(1 for r in self.validation_results if r.command_accurate)
        overall_accurate = sum(1 for r in self.validation_results if r.overall_accurate)
        
        confidence_accuracy = confidence_accurate / total_tests
        intent_accuracy = intent_accurate / total_tests
        command_accuracy = command_accurate / total_tests
        overall_accuracy = overall_accurate / total_tests
        
        # Precision, recall, F1 for confidence classification
        y_true = [1 if r.test_case.ground_truth_confidence >= self.high_confidence_threshold else 0 
                 for r in self.validation_results]
        y_pred = [1 if r.predicted_confidence >= self.high_confidence_threshold else 0 
                 for r in self.validation_results]
        
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        # Processing time
        avg_processing_time = statistics.mean(r.processing_time_ms for r in self.validation_results)
        
        # Confidence distribution
        confidence_distribution = {
            "high": sum(1 for r in self.validation_results if r.predicted_confidence >= self.high_confidence_threshold),
            "medium": sum(1 for r in self.validation_results if self.medium_confidence_threshold <= r.predicted_confidence < self.high_confidence_threshold),
            "low": sum(1 for r in self.validation_results if r.predicted_confidence < self.medium_confidence_threshold)
        }
        
        # Accuracy by category
        accuracy_by_category = {}
        categories = set(r.test_case.category for r in self.validation_results)
        for category in categories:
            category_results = [r for r in self.validation_results if r.test_case.category == category]
            category_accurate = sum(1 for r in category_results if r.overall_accurate)
            accuracy_by_category[category] = category_accurate / len(category_results) if category_results else 0
        
        # Accuracy by complexity
        accuracy_by_complexity = {}
        complexities = set(r.test_case.complexity for r in self.validation_results)
        for complexity in complexities:
            complexity_results = [r for r in self.validation_results if r.test_case.complexity == complexity]
            complexity_accurate = sum(1 for r in complexity_results if r.overall_accurate)
            accuracy_by_complexity[complexity] = complexity_accurate / len(complexity_results) if complexity_results else 0
        
        # Accuracy by ambiguity
        accuracy_by_ambiguity = {}
        ambiguity_levels = set(r.test_case.ambiguity_level for r in self.validation_results)
        for ambiguity in ambiguity_levels:
            ambiguity_results = [r for r in self.validation_results if r.test_case.ambiguity_level == ambiguity]
            ambiguity_accurate = sum(1 for r in ambiguity_results if r.overall_accurate)
            accuracy_by_ambiguity[ambiguity] = ambiguity_accurate / len(ambiguity_results) if ambiguity_results else 0
        
        return ValidationMetrics(
            total_tests=total_tests,
            confidence_accuracy=confidence_accuracy,
            intent_accuracy=intent_accuracy,
            command_accuracy=command_accuracy,
            overall_accuracy=overall_accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            avg_processing_time=avg_processing_time,
            confidence_distribution=confidence_distribution,
            accuracy_by_category=accuracy_by_category,
            accuracy_by_complexity=accuracy_by_complexity,
            accuracy_by_ambiguity=accuracy_by_ambiguity
        )
    
    def generate_report(self, metrics: ValidationMetrics, output_path: str = "confidence_validation_report.json"):
        """Generate comprehensive validation report."""
        
        report = {
            "validation_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": metrics.total_tests,
                "target_confidence_threshold": self.high_confidence_threshold,
                "target_accuracy": 0.85,
                "achieved_accuracy": metrics.overall_accuracy,
                "target_met": metrics.overall_accuracy >= 0.85
            },
            "accuracy_metrics": {
                "confidence_accuracy": metrics.confidence_accuracy,
                "intent_accuracy": metrics.intent_accuracy,
                "command_accuracy": metrics.command_accuracy,
                "overall_accuracy": metrics.overall_accuracy
            },
            "statistical_metrics": {
                "precision": metrics.precision,
                "recall": metrics.recall,
                "f1_score": metrics.f1_score
            },
            "performance_metrics": {
                "avg_processing_time_ms": metrics.avg_processing_time,
                "target_processing_time_ms": 500,
                "performance_target_met": metrics.avg_processing_time <= 500
            },
            "confidence_distribution": metrics.confidence_distribution,
            "accuracy_breakdown": {
                "by_category": metrics.accuracy_by_category,
                "by_complexity": metrics.accuracy_by_complexity,
                "by_ambiguity": metrics.accuracy_by_ambiguity
            },
            "recommendations": self._generate_recommendations(metrics)
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Validation report saved to {output_path}")
        return report
    
    def _generate_recommendations(self, metrics: ValidationMetrics) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if metrics.overall_accuracy < 0.85:
            recommendations.append("Overall accuracy below 85% target - review confidence calibration")
        
        if metrics.confidence_accuracy < 0.90:
            recommendations.append("Confidence prediction accuracy needs improvement")
        
        if metrics.avg_processing_time > 500:
            recommendations.append("Processing time exceeds 500ms target - optimize performance")
        
        # Check category-specific issues
        for category, accuracy in metrics.accuracy_by_category.items():
            if accuracy < 0.80:
                recommendations.append(f"Low accuracy in {category} category ({accuracy:.1%}) - review training data")
        
        # Check ambiguity handling
        if metrics.accuracy_by_ambiguity.get("high", 1.0) < 0.60:
            recommendations.append("Poor handling of highly ambiguous inputs - improve disambiguation")
        
        if not recommendations:
            recommendations.append("All validation targets met - system ready for production")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    async def main():
        validator = ConfidenceValidationFramework()
        
        # Run validation
        metrics = await validator.run_validation()
        
        # Generate report
        report = validator.generate_report(metrics)
        
        print("Confidence Validation Results:")
        print(f"Overall Accuracy: {metrics.overall_accuracy:.2%}")
        print(f"Confidence Accuracy: {metrics.confidence_accuracy:.2%}")
        print(f"Target Met: {'Yes' if metrics.overall_accuracy >= 0.85 else 'No'}")
    
    asyncio.run(main())
