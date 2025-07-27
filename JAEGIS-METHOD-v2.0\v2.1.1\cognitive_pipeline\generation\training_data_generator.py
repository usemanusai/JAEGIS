"""
JAEGIS Cognitive Pipeline - Training Data Generator
Generate quizzes, flashcards, scenarios, and other training materials

This module implements the Tier 14 Training Data Generation Squad capabilities
for comprehensive educational content creation and optimization.
"""

import asyncio
import logging
import re
import json
import random
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import uuid

from cognitive_pipeline.models.pipeline_models import (
    ContentStructure, QuizData, QuizQuestion, QuizOption, FlashcardData,
    Flashcard, TrainingScenario, ScenarioRole, SummaryData,
    QuestionType, DifficultyLevel, SkillTag
)
from cognitive_pipeline.audio.tts_processor import TTSProcessor

logger = logging.getLogger(__name__)


class TrainingDataGenerationError(Exception):
    """Custom exception for training data generation errors."""
    pass


class TrainingDataGenerator:
    """
    Training data generation system implementing JAEGIS Tier 14 capabilities.
    
    Provides:
    - Quiz generation with multiple question types
    - Flashcard creation with spaced repetition optimization
    - Training scenario development for agent simulation
    - Behavioral benchmark generation
    - Skill-based tagging and categorization
    - Educational effectiveness optimization
    """
    
    def __init__(self):
        self.quiz_generator = None
        self.flashcard_generator = None
        self.scenario_generator = None
        self.summary_generator = None
        self.tts_processor = None
        
        # Configuration
        self.quiz_config = {
            "default_questions_per_chapter": 3,
            "max_questions_total": 50,
            "difficulty_distribution": {
                DifficultyLevel.EASY: 0.4,
                DifficultyLevel.MEDIUM: 0.4,
                DifficultyLevel.HARD: 0.2
            },
            "question_type_distribution": {
                QuestionType.MULTIPLE_CHOICE: 0.6,
                QuestionType.TRUE_FALSE: 0.2,
                QuestionType.FILL_IN_BLANK: 0.2
            }
        }
        
        self.flashcard_config = {
            "max_cards_per_chapter": 5,
            "max_cards_total": 100,
            "spaced_repetition_intervals": [1, 3, 7, 14, 30, 90],
            "difficulty_factors": {
                DifficultyLevel.EASY: 1.0,
                DifficultyLevel.MEDIUM: 1.5,
                DifficultyLevel.HARD: 2.0
            }
        }
        
        self.scenario_config = {
            "max_scenarios_per_content": 3,
            "min_roles_per_scenario": 2,
            "max_roles_per_scenario": 4,
            "duration_estimates": {
                DifficultyLevel.EASY: 15,  # minutes
                DifficultyLevel.MEDIUM: 30,
                DifficultyLevel.HARD: 60
            }
        }
        
        # Question templates
        self.question_templates = {
            QuestionType.MULTIPLE_CHOICE: [
                "What is the main purpose of {concept}?",
                "Which of the following best describes {concept}?",
                "According to the content, {concept} is primarily used for:",
                "What are the key characteristics of {concept}?"
            ],
            QuestionType.TRUE_FALSE: [
                "{statement} is always true.",
                "The content states that {statement}.",
                "{concept} is essential for {context}.",
                "According to the material, {statement}."
            ],
            QuestionType.FILL_IN_BLANK: [
                "The primary function of _____ is to {purpose}.",
                "_____ is a key component of {system}.",
                "To achieve {goal}, one must first _____.",
                "The relationship between {concept1} and _____ is crucial."
            ]
        }
        
        logger.info("TrainingDataGenerator initialized")
    
    async def initialize(self):
        """Initialize training data generation components."""
        
        logger.info("🔄 Initializing Training Data Generator")
        
        # Initialize quiz generator
        self.quiz_generator = QuizGenerator(self.quiz_config, self.question_templates)
        await self.quiz_generator.initialize()
        
        # Initialize flashcard generator
        self.flashcard_generator = FlashcardGenerator(self.flashcard_config)
        await self.flashcard_generator.initialize()
        
        # Initialize scenario generator
        self.scenario_generator = ScenarioGenerator(self.scenario_config)
        await self.scenario_generator.initialize()
        
        # Initialize summary generator
        self.summary_generator = SummaryGenerator()
        await self.summary_generator.initialize()

        # Initialize TTS processor
        self.tts_processor = TTSProcessor()
        await self.tts_processor.initialize()

        logger.info("✅ Training Data Generator ready")
    
    async def cleanup(self):
        """Clean up resources."""
        
        if self.quiz_generator:
            await self.quiz_generator.cleanup()
        if self.flashcard_generator:
            await self.flashcard_generator.cleanup()
        if self.scenario_generator:
            await self.scenario_generator.cleanup()
        if self.summary_generator:
            await self.summary_generator.cleanup()
        if self.tts_processor:
            await self.tts_processor.cleanup()
    
    async def health_check(self) -> bool:
        """Check health of training data generation components."""
        
        try:
            checks = [
                self.quiz_generator.health_check() if self.quiz_generator else True,
                self.flashcard_generator.health_check() if self.flashcard_generator else True,
                self.scenario_generator.health_check() if self.scenario_generator else True,
                self.summary_generator.health_check() if self.summary_generator else True
            ]
            
            results = await asyncio.gather(*checks, return_exceptions=True)
            return all(result is True for result in results)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def generate_training_data(
        self,
        content: ContentStructure,
        analysis: Dict[str, Any],
        generation_types: List[str]
    ) -> Dict[str, Any]:
        """
        Main training data generation method.
        
        Args:
            content: Structured content to generate training data from
            analysis: LLM analysis results
            generation_types: Types of training data to generate
        
        Returns:
            Dict containing generated training data
        """
        
        logger.info(f"🔄 Starting training data generation: {generation_types}")
        
        try:
            training_data = {}
            
            # Generate each requested type
            for generation_type in generation_types:
                if generation_type == "quiz":
                    quiz_data = await self.quiz_generator.generate_quiz(content, analysis)
                    training_data["quiz"] = quiz_data
                
                elif generation_type == "flashcards":
                    flashcard_data = await self.flashcard_generator.generate_flashcards(content, analysis)
                    training_data["flashcards"] = flashcard_data
                
                elif generation_type == "scenarios":
                    scenarios = await self.scenario_generator.generate_scenarios(content, analysis)
                    training_data["scenarios"] = scenarios
                
                elif generation_type == "summary":
                    summary_data = await self.summary_generator.generate_summary(content, analysis)
                    training_data["summary"] = summary_data
            
            # Calculate overall metrics
            generation_metrics = await self._calculate_generation_metrics(training_data)
            
            return {
                "training_data": training_data,
                "generation_metrics": generation_metrics,
                "content_coverage": await self._assess_content_coverage(content, training_data),
                "educational_effectiveness": await self._assess_educational_effectiveness(training_data),
                "generation_metadata": {
                    "total_types_generated": len(training_data),
                    "content_source_id": content.content_id,
                    "generation_timestamp": datetime.utcnow().isoformat(),
                    "skill_tags_covered": list(set(content.skill_tags))
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Training data generation failed: {e}")
            raise TrainingDataGenerationError(f"Failed to generate training data: {str(e)}")
    
    async def _calculate_generation_metrics(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metrics for generated training data."""
        
        metrics = {
            "total_items_generated": 0,
            "types_generated": list(training_data.keys()),
            "difficulty_distribution": {},
            "skill_coverage": set(),
            "estimated_completion_time": 0
        }
        
        # Count items and analyze distribution
        for data_type, data in training_data.items():
            if data_type == "quiz" and isinstance(data, QuizData):
                metrics["total_items_generated"] += len(data.questions)
                metrics["estimated_completion_time"] += data.estimated_time
                
                # Difficulty distribution
                for question in data.questions:
                    diff = question.difficulty
                    metrics["difficulty_distribution"][diff] = metrics["difficulty_distribution"].get(diff, 0) + 1
                    metrics["skill_coverage"].update(question.skill_tags)
            
            elif data_type == "flashcards" and isinstance(data, FlashcardData):
                metrics["total_items_generated"] += len(data.flashcards)
                metrics["estimated_completion_time"] += len(data.flashcards) * 2  # 2 min per card
                
                for card in data.flashcards:
                    diff = card.difficulty
                    metrics["difficulty_distribution"][diff] = metrics["difficulty_distribution"].get(diff, 0) + 1
                    metrics["skill_coverage"].update(card.skill_tags)
            
            elif data_type == "scenarios" and isinstance(data, list):
                metrics["total_items_generated"] += len(data)
                for scenario in data:
                    if isinstance(scenario, TrainingScenario):
                        metrics["estimated_completion_time"] += scenario.duration_estimate
                        metrics["skill_coverage"].update(scenario.skill_tags)
        
        # Convert skill coverage set to list
        metrics["skill_coverage"] = list(metrics["skill_coverage"])
        
        return metrics
    
    async def _assess_content_coverage(
        self,
        content: ContentStructure,
        training_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess how well training data covers the source content."""
        
        # Calculate chapter coverage
        total_chapters = len(content.chapters)
        covered_chapters = 0
        
        # Simple heuristic: if training data mentions chapter concepts, it's covered
        all_concepts = set()
        for chapter in content.chapters:
            all_concepts.update(chapter.key_concepts)
        
        training_concepts = set()
        for data_type, data in training_data.items():
            if data_type == "quiz" and isinstance(data, QuizData):
                for question in data.questions:
                    # Extract concepts from question text
                    question_words = set(question.text.lower().split())
                    training_concepts.update(question_words)
        
        # Calculate concept overlap
        concept_overlap = len(all_concepts & training_concepts) / len(all_concepts) if all_concepts else 0
        
        return {
            "chapter_coverage_percentage": (covered_chapters / total_chapters) * 100 if total_chapters > 0 else 0,
            "concept_coverage_percentage": concept_overlap * 100,
            "total_source_concepts": len(all_concepts),
            "covered_concepts": len(all_concepts & training_concepts),
            "coverage_quality": "high" if concept_overlap > 0.7 else "medium" if concept_overlap > 0.4 else "low"
        }
    
    async def _assess_educational_effectiveness(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the educational effectiveness of generated training data."""
        
        effectiveness_score = 0
        factors = []
        
        # Check for variety in question types
        if "quiz" in training_data:
            quiz = training_data["quiz"]
            if isinstance(quiz, QuizData):
                question_types = set(q.type for q in quiz.questions)
                if len(question_types) > 1:
                    effectiveness_score += 20
                    factors.append("variety_in_question_types")
        
        # Check for balanced difficulty
        difficulty_counts = {}
        total_items = 0
        
        for data_type, data in training_data.items():
            if data_type == "quiz" and isinstance(data, QuizData):
                for question in data.questions:
                    difficulty_counts[question.difficulty] = difficulty_counts.get(question.difficulty, 0) + 1
                    total_items += 1
            elif data_type == "flashcards" and isinstance(data, FlashcardData):
                for card in data.flashcards:
                    difficulty_counts[card.difficulty] = difficulty_counts.get(card.difficulty, 0) + 1
                    total_items += 1
        
        if total_items > 0:
            # Check for balanced difficulty distribution
            easy_ratio = difficulty_counts.get(DifficultyLevel.EASY, 0) / total_items
            medium_ratio = difficulty_counts.get(DifficultyLevel.MEDIUM, 0) / total_items
            hard_ratio = difficulty_counts.get(DifficultyLevel.HARD, 0) / total_items
            
            # Ideal distribution: 40% easy, 40% medium, 20% hard
            if 0.3 <= easy_ratio <= 0.5 and 0.3 <= medium_ratio <= 0.5:
                effectiveness_score += 25
                factors.append("balanced_difficulty_distribution")
        
        # Check for multiple training modalities
        modality_count = len(training_data)
        if modality_count >= 3:
            effectiveness_score += 30
            factors.append("multiple_training_modalities")
        elif modality_count >= 2:
            effectiveness_score += 15
            factors.append("dual_training_modalities")
        
        # Check for skill tag coverage
        all_skill_tags = set()
        for data_type, data in training_data.items():
            if data_type == "quiz" and isinstance(data, QuizData):
                all_skill_tags.update(data.skill_coverage)
            elif data_type == "flashcards" and isinstance(data, FlashcardData):
                all_skill_tags.update(data.skill_coverage)
        
        if len(all_skill_tags) >= 3:
            effectiveness_score += 25
            factors.append("comprehensive_skill_coverage")
        elif len(all_skill_tags) >= 2:
            effectiveness_score += 15
            factors.append("moderate_skill_coverage")
        
        return {
            "effectiveness_score": min(100, effectiveness_score),
            "effectiveness_factors": factors,
            "difficulty_distribution": difficulty_counts,
            "skill_tags_covered": list(all_skill_tags),
            "training_modalities": list(training_data.keys()),
            "recommendations": await self._generate_effectiveness_recommendations(effectiveness_score, factors)
        }
    
    async def _generate_effectiveness_recommendations(
        self,
        score: int,
        factors: List[str]
    ) -> List[str]:
        """Generate recommendations for improving educational effectiveness."""
        
        recommendations = []
        
        if score < 50:
            recommendations.append("Consider adding more variety in question types")
            recommendations.append("Ensure balanced difficulty distribution")
            recommendations.append("Add multiple training modalities (quiz + flashcards + scenarios)")
        
        if "variety_in_question_types" not in factors:
            recommendations.append("Add more question types (multiple choice, true/false, fill-in-blank)")
        
        if "balanced_difficulty_distribution" not in factors:
            recommendations.append("Adjust difficulty distribution to 40% easy, 40% medium, 20% hard")
        
        if "multiple_training_modalities" not in factors:
            recommendations.append("Include multiple training formats for better learning outcomes")
        
        if "comprehensive_skill_coverage" not in factors:
            recommendations.append("Ensure training data covers multiple skill areas")
        
        return recommendations


# Component classes (simplified implementations)
class QuizGenerator:
    """Quiz generation component."""
    
    def __init__(self, config: Dict[str, Any], templates: Dict[str, List[str]]):
        self.config = config
        self.templates = templates
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def generate_quiz(self, content: ContentStructure, analysis: Dict[str, Any]) -> QuizData:
        """Generate quiz from content."""
        
        questions = []
        
        # Generate questions for each chapter
        for i, chapter in enumerate(content.chapters[:10]):  # Limit to 10 chapters
            chapter_questions = await self._generate_chapter_questions(chapter, i)
            questions.extend(chapter_questions)
        
        # Limit total questions
        if len(questions) > self.config["max_questions_total"]:
            questions = questions[:self.config["max_questions_total"]]
        
        return QuizData(
            source_id=content.content_id,
            title=f"Quiz: {content.title}",
            description=f"Comprehensive quiz covering {content.title}",
            questions=questions,
            total_points=sum(q.points for q in questions),
            estimated_time=len(questions) * 2,  # 2 minutes per question
            difficulty_distribution={
                diff: len([q for q in questions if q.difficulty == diff])
                for diff in DifficultyLevel
            },
            skill_coverage=list(set(tag for q in questions for tag in q.skill_tags))
        )
    
    async def _generate_chapter_questions(self, chapter, chapter_index: int) -> List[QuizQuestion]:
        """Generate questions for a specific chapter."""
        
        questions = []
        num_questions = min(self.config["default_questions_per_chapter"], 
                          len(chapter.key_concepts))
        
        for i in range(num_questions):
            # Select question type based on distribution
            question_type = random.choices(
                list(self.config["question_type_distribution"].keys()),
                weights=list(self.config["question_type_distribution"].values())
            )[0]
            
            # Select difficulty based on distribution
            difficulty = random.choices(
                list(self.config["difficulty_distribution"].keys()),
                weights=list(self.config["difficulty_distribution"].values())
            )[0]
            
            # Generate question
            question = await self._create_question(
                chapter, question_type, difficulty, i
            )
            
            if question:
                questions.append(question)
        
        return questions
    
    async def _create_question(
        self,
        chapter,
        question_type: QuestionType,
        difficulty: DifficultyLevel,
        index: int
    ) -> Optional[QuizQuestion]:
        """Create a specific question."""
        
        if not chapter.key_concepts:
            return None
        
        concept = random.choice(chapter.key_concepts)
        
        if question_type == QuestionType.MULTIPLE_CHOICE:
            return QuizQuestion(
                type=question_type,
                text=f"What is the primary purpose of {concept}?",
                options=[
                    QuizOption(text="Option A", is_correct=True),
                    QuizOption(text="Option B", is_correct=False),
                    QuizOption(text="Option C", is_correct=False),
                    QuizOption(text="Option D", is_correct=False)
                ],
                correct_answer="Option A",
                difficulty=difficulty,
                source_reference=f"Chapter: {chapter.title}",
                skill_tags=[SkillTag.CRITICAL_THINKING],
                points=1 if difficulty == DifficultyLevel.EASY else 2 if difficulty == DifficultyLevel.MEDIUM else 3
            )
        
        elif question_type == QuestionType.TRUE_FALSE:
            return QuizQuestion(
                type=question_type,
                text=f"{concept} is a fundamental concept in this domain.",
                correct_answer="True",
                difficulty=difficulty,
                source_reference=f"Chapter: {chapter.title}",
                skill_tags=[SkillTag.CRITICAL_THINKING],
                points=1
            )
        
        elif question_type == QuestionType.FILL_IN_BLANK:
            return QuizQuestion(
                type=question_type,
                text=f"The primary function of _____ is essential for understanding this topic.",
                correct_answer=concept,
                difficulty=difficulty,
                source_reference=f"Chapter: {chapter.title}",
                skill_tags=[SkillTag.CRITICAL_THINKING],
                points=2
            )
        
        return None


class FlashcardGenerator:
    """Flashcard generation component."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def generate_flashcards(self, content: ContentStructure, analysis: Dict[str, Any]) -> FlashcardData:
        """Generate flashcards from content."""
        
        flashcards = []
        
        # Generate flashcards for key concepts
        for chapter in content.chapters:
            chapter_cards = await self._generate_chapter_flashcards(chapter)
            flashcards.extend(chapter_cards)
        
        # Limit total flashcards
        if len(flashcards) > self.config["max_cards_total"]:
            flashcards = flashcards[:self.config["max_cards_total"]]
        
        return FlashcardData(
            source_id=content.content_id,
            title=f"Flashcards: {content.title}",
            description=f"Key concepts from {content.title}",
            flashcards=flashcards,
            categories=list(set(card.category for card in flashcards if card.category)),
            total_cards=len(flashcards),
            skill_coverage=list(set(tag for card in flashcards for tag in card.skill_tags))
        )
    
    async def _generate_chapter_flashcards(self, chapter) -> List[Flashcard]:
        """Generate flashcards for a chapter."""
        
        flashcards = []
        
        for concept in chapter.key_concepts[:self.config["max_cards_per_chapter"]]:
            flashcard = Flashcard(
                front=f"What is {concept}?",
                back=f"{concept} is a key concept related to {chapter.title}",
                category=chapter.title,
                difficulty=chapter.difficulty_level,
                source_reference=f"Chapter: {chapter.title}",
                skill_tags=[SkillTag.CRITICAL_THINKING],
                spaced_repetition_interval=self.config["spaced_repetition_intervals"][0]
            )
            flashcards.append(flashcard)
        
        return flashcards


class ScenarioGenerator:
    """Training scenario generation component."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def generate_scenarios(self, content: ContentStructure, analysis: Dict[str, Any]) -> List[TrainingScenario]:
        """Generate training scenarios from content."""
        
        scenarios = []
        
        # Generate scenarios based on content themes
        for i in range(min(self.config["max_scenarios_per_content"], len(content.chapters))):
            scenario = await self._create_scenario(content, i)
            if scenario:
                scenarios.append(scenario)
        
        return scenarios
    
    async def _create_scenario(self, content: ContentStructure, index: int) -> Optional[TrainingScenario]:
        """Create a training scenario."""
        
        if index >= len(content.chapters):
            return None
        
        chapter = content.chapters[index]
        
        # Create roles
        roles = [
            ScenarioRole(
                role_name="Learner",
                objective="Understand and apply the concepts",
                constraints=["Must ask clarifying questions", "Cannot use external resources"],
                success_criteria=["Demonstrates understanding", "Applies concepts correctly"],
                skill_requirements=[SkillTag.CRITICAL_THINKING]
            ),
            ScenarioRole(
                role_name="Instructor",
                objective="Guide the learner effectively",
                constraints=["Cannot give direct answers", "Must use Socratic method"],
                success_criteria=["Learner achieves understanding", "Maintains engagement"],
                skill_requirements=[SkillTag.COMMUNICATION]
            )
        ]
        
        return TrainingScenario(
            source_id=content.content_id,
            title=f"Learning Scenario: {chapter.title}",
            description=f"Interactive learning scenario based on {chapter.title}",
            context=f"This scenario focuses on the key concepts from {chapter.title}",
            roles=roles,
            duration_estimate=self.config["duration_estimates"][chapter.difficulty_level],
            difficulty=chapter.difficulty_level,
            learning_objectives=[f"Understand {concept}" for concept in chapter.key_concepts[:3]],
            skill_tags=[SkillTag.CRITICAL_THINKING, SkillTag.COMMUNICATION],
            success_metrics=["Concept mastery", "Application ability", "Engagement level"]
        )


class SummaryGenerator:
    """Summary generation component."""

    def __init__(self):
        self.tts_processor = None

    async def initialize(self):
        # Initialize TTS processor for audio generation
        from cognitive_pipeline.audio.tts_processor import TTSProcessor
        self.tts_processor = TTSProcessor()
        await self.tts_processor.initialize()

    async def cleanup(self):
        if self.tts_processor:
            await self.tts_processor.cleanup()

    async def health_check(self):
        return True

    async def generate_summary(self, content: ContentStructure, analysis: Dict[str, Any]) -> SummaryData:
        """Generate summary with audio."""

        # Use existing summary or create new one
        text_summary = content.summary

        # Extract key points
        key_points = []
        for chapter in content.chapters[:5]:  # Top 5 chapters
            if chapter.key_concepts:
                key_points.append(f"{chapter.title}: {chapter.key_concepts[0]}")

        # Generate audio using TTS
        audio_result = None
        audio_url = None
        audio_duration = None
        listening_time = None

        try:
            if self.tts_processor:
                audio_result = await self.tts_processor.synthesize_summary_audio(
                    summary_text=text_summary,
                    key_points=key_points,
                    voice_style="podcast"
                )

                if audio_result:
                    audio_url = audio_result.get("audio_file_path")
                    audio_duration = audio_result.get("duration", 0)
                    listening_time = int(audio_duration / 60) if audio_duration else None

        except Exception as e:
            logger.warning(f"TTS generation failed: {e}")

        return SummaryData(
            source_id=content.content_id,
            title=f"Summary: {content.title}",
            text_summary=text_summary,
            key_points=key_points,
            audio_url=audio_url,
            audio_duration=audio_duration,
            reading_time=content.estimated_reading_time,
            listening_time=listening_time,
            voice_settings={
                "voice": "rachel",
                "style": "podcast",
                "speed": "normal",
                "emotion": "engaging"
            }
        )
