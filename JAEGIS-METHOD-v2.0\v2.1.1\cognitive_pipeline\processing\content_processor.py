"""
JAEGIS Cognitive Pipeline - Content Processor
Automated content structuring with chapters, titles, and timestamps

This module implements content structuring capabilities using the
deployed Tier 13 Semantic Analysis Squad for advanced text processing.
"""

import asyncio
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import uuid

from cognitive_pipeline.models.pipeline_models import (
    ContentStructure, ContentChapter, ContentMetadata,
    DifficultyLevel, SkillTag
)

logger = logging.getLogger(__name__)


class ContentStructuringError(Exception):
    """Custom exception for content structuring errors."""
    pass


class ContentProcessor:
    """
    Content processing system implementing JAEGIS Tier 13 capabilities.
    
    Provides:
    - Automated content segmentation
    - Chapter and section identification
    - Title and heading extraction
    - Timestamp alignment for multimedia content
    - Difficulty assessment
    - Key concept extraction
    - Skill-based tagging
    """
    
    def __init__(self):
        self.semantic_analyzer = None
        self.chapter_detector = None
        self.concept_extractor = None
        self.skill_tagger = None
        
        # Configuration
        self.min_chapter_length = 200  # characters
        self.max_chapter_length = 2000  # characters
        self.chapter_overlap = 50  # characters for context
        
        # Patterns for structure detection
        self.heading_patterns = [
            r'^#{1,6}\s+(.+)$',  # Markdown headers
            r'^([A-Z][^.!?]*):?\s*$',  # All caps titles
            r'^\d+\.\s+(.+)$',  # Numbered sections
            r'^Chapter\s+\d+:?\s*(.*)$',  # Chapter titles
            r'^Section\s+\d+:?\s*(.*)$',  # Section titles
        ]
        
        # Skill detection patterns
        self.skill_patterns = {
            SkillTag.STATISTICAL_ANALYSIS: [
                r'\b(statistics?|statistical|analysis|data analysis|regression|correlation|hypothesis|p-value|significance)\b',
                r'\b(mean|median|mode|standard deviation|variance|distribution|sample|population)\b'
            ],
            SkillTag.API_DESIGN: [
                r'\b(API|REST|GraphQL|endpoint|HTTP|JSON|XML|microservice|web service)\b',
                r'\b(GET|POST|PUT|DELETE|authentication|authorization|rate limiting)\b'
            ],
            SkillTag.MACHINE_LEARNING: [
                r'\b(machine learning|ML|neural network|deep learning|algorithm|model|training|prediction)\b',
                r'\b(supervised|unsupervised|reinforcement|classification|regression|clustering)\b'
            ],
            SkillTag.SYSTEM_ARCHITECTURE: [
                r'\b(architecture|system design|scalability|distributed|microservices|load balancing)\b',
                r'\b(database|caching|messaging|queue|infrastructure|deployment)\b'
            ]
        }
        
        logger.info("ContentProcessor initialized")
    
    async def initialize(self):
        """Initialize content processing components."""
        
        logger.info("🔄 Initializing Content Processor")
        
        # Initialize semantic analyzer
        self.semantic_analyzer = SemanticAnalyzer()
        await self.semantic_analyzer.initialize()
        
        # Initialize chapter detector
        self.chapter_detector = ChapterDetector()
        await self.chapter_detector.initialize()
        
        # Initialize concept extractor
        self.concept_extractor = ConceptExtractor()
        await self.concept_extractor.initialize()
        
        # Initialize skill tagger
        self.skill_tagger = SkillTagger()
        await self.skill_tagger.initialize()
        
        logger.info("✅ Content Processor ready")
    
    async def cleanup(self):
        """Clean up resources."""
        
        if self.semantic_analyzer:
            await self.semantic_analyzer.cleanup()
        if self.chapter_detector:
            await self.chapter_detector.cleanup()
        if self.concept_extractor:
            await self.concept_extractor.cleanup()
        if self.skill_tagger:
            await self.skill_tagger.cleanup()
    
    async def health_check(self) -> bool:
        """Check health of content processing components."""
        
        try:
            checks = [
                self.semantic_analyzer.health_check() if self.semantic_analyzer else True,
                self.chapter_detector.health_check() if self.chapter_detector else True,
                self.concept_extractor.health_check() if self.concept_extractor else True,
                self.skill_tagger.health_check() if self.skill_tagger else True
            ]
            
            results = await asyncio.gather(*checks, return_exceptions=True)
            return all(result is True for result in results)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def structure_content(
        self,
        raw_content: str,
        metadata: Dict[str, Any]
    ) -> ContentStructure:
        """
        Main content structuring method.
        
        Args:
            raw_content: Raw text content to structure
            metadata: Content metadata from ingestion
        
        Returns:
            ContentStructure with organized chapters and metadata
        """
        
        logger.info("🔄 Starting content structuring")
        
        try:
            # Clean and preprocess content
            cleaned_content = await self._preprocess_content(raw_content)
            
            # Detect and extract chapters
            chapters = await self._detect_chapters(cleaned_content, metadata)
            
            # Extract key concepts from entire content
            key_concepts = await self.concept_extractor.extract_concepts(cleaned_content)
            
            # Detect skill tags
            skill_tags = await self._detect_skill_tags(cleaned_content)
            
            # Generate content summary
            summary = await self._generate_summary(cleaned_content, chapters)
            
            # Calculate reading time
            reading_time = self._calculate_reading_time(cleaned_content)
            
            # Create content metadata
            content_metadata = ContentMetadata(
                source_type=metadata.get("source_type", "unknown"),
                title=metadata.get("title", "Untitled Content"),
                description=metadata.get("description", ""),
                author=metadata.get("author", ""),
                language=metadata.get("language", "en"),
                tags=metadata.get("tags", []),
                skill_tags=skill_tags
            )
            
            # Create structured content
            structured_content = ContentStructure(
                title=metadata.get("title", "Untitled Content"),
                summary=summary,
                chapters=chapters,
                metadata=content_metadata,
                total_word_count=len(cleaned_content.split()),
                estimated_reading_time=reading_time,
                key_concepts=key_concepts,
                skill_tags=skill_tags
            )
            
            logger.info(f"✅ Content structured: {len(chapters)} chapters, {len(key_concepts)} concepts")
            
            return structured_content
            
        except Exception as e:
            logger.error(f"❌ Content structuring failed: {e}")
            raise ContentStructuringError(f"Failed to structure content: {str(e)}")
    
    async def _preprocess_content(self, content: str) -> str:
        """Clean and preprocess raw content."""
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove special characters that might interfere with processing
        content = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\"\'\/\\]', '', content)
        
        # Normalize line breaks
        content = re.sub(r'\n+', '\n', content)
        
        # Remove empty lines
        content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())
        
        return content.strip()
    
    async def _detect_chapters(
        self,
        content: str,
        metadata: Dict[str, Any]
    ) -> List[ContentChapter]:
        """Detect and create content chapters."""
        
        # Try different chapter detection methods
        chapters = []
        
        # Method 1: Detect by headings
        heading_chapters = await self._detect_chapters_by_headings(content)
        if heading_chapters:
            chapters = heading_chapters
        
        # Method 2: Detect by semantic breaks (if no clear headings)
        if not chapters:
            semantic_chapters = await self._detect_chapters_by_semantics(content)
            chapters = semantic_chapters
        
        # Method 3: Split by length (fallback)
        if not chapters:
            length_chapters = await self._split_by_length(content)
            chapters = length_chapters
        
        # Enhance chapters with additional analysis
        enhanced_chapters = []
        for i, chapter in enumerate(chapters):
            enhanced_chapter = await self._enhance_chapter(chapter, i, metadata)
            enhanced_chapters.append(enhanced_chapter)
        
        return enhanced_chapters
    
    async def _detect_chapters_by_headings(self, content: str) -> List[ContentChapter]:
        """Detect chapters based on heading patterns."""
        
        chapters = []
        lines = content.split('\n')
        current_chapter_lines = []
        current_title = None
        
        for line in lines:
            # Check if line matches any heading pattern
            is_heading = False
            title = None
            
            for pattern in self.heading_patterns:
                match = re.match(pattern, line.strip(), re.IGNORECASE)
                if match:
                    is_heading = True
                    title = match.group(1) if match.groups() else line.strip()
                    break
            
            if is_heading and current_chapter_lines:
                # Create chapter from accumulated lines
                chapter_content = '\n'.join(current_chapter_lines).strip()
                if len(chapter_content) >= self.min_chapter_length:
                    chapter = ContentChapter(
                        title=current_title or f"Chapter {len(chapters) + 1}",
                        content=chapter_content,
                        word_count=len(chapter_content.split())
                    )
                    chapters.append(chapter)
                
                # Start new chapter
                current_chapter_lines = []
                current_title = title
            else:
                current_chapter_lines.append(line)
        
        # Add final chapter
        if current_chapter_lines:
            chapter_content = '\n'.join(current_chapter_lines).strip()
            if len(chapter_content) >= self.min_chapter_length:
                chapter = ContentChapter(
                    title=current_title or f"Chapter {len(chapters) + 1}",
                    content=chapter_content,
                    word_count=len(chapter_content.split())
                )
                chapters.append(chapter)
        
        return chapters
    
    async def _detect_chapters_by_semantics(self, content: str) -> List[ContentChapter]:
        """Detect chapters based on semantic breaks."""
        
        # Use semantic analyzer to find topic boundaries
        semantic_breaks = await self.semantic_analyzer.find_topic_boundaries(content)
        
        chapters = []
        sentences = re.split(r'[.!?]+', content)
        
        if not semantic_breaks:
            # Fallback to paragraph-based splitting
            paragraphs = content.split('\n\n')
            current_chapter = []
            current_length = 0
            
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                
                if current_length + len(paragraph) > self.max_chapter_length and current_chapter:
                    # Create chapter
                    chapter_content = '\n\n'.join(current_chapter)
                    chapter = ContentChapter(
                        title=f"Section {len(chapters) + 1}",
                        content=chapter_content,
                        word_count=len(chapter_content.split())
                    )
                    chapters.append(chapter)
                    
                    # Start new chapter
                    current_chapter = [paragraph]
                    current_length = len(paragraph)
                else:
                    current_chapter.append(paragraph)
                    current_length += len(paragraph)
            
            # Add final chapter
            if current_chapter:
                chapter_content = '\n\n'.join(current_chapter)
                chapter = ContentChapter(
                    title=f"Section {len(chapters) + 1}",
                    content=chapter_content,
                    word_count=len(chapter_content.split())
                )
                chapters.append(chapter)
        
        return chapters
    
    async def _split_by_length(self, content: str) -> List[ContentChapter]:
        """Split content by length as fallback method."""
        
        chapters = []
        words = content.split()
        
        # Target words per chapter
        target_words = 300
        current_words = []
        
        for word in words:
            current_words.append(word)
            
            if len(current_words) >= target_words:
                # Find a good break point (end of sentence)
                chapter_text = ' '.join(current_words)
                
                # Look for sentence ending
                last_sentence_end = max(
                    chapter_text.rfind('.'),
                    chapter_text.rfind('!'),
                    chapter_text.rfind('?')
                )
                
                if last_sentence_end > len(chapter_text) * 0.7:  # If sentence end is reasonably close
                    chapter_content = chapter_text[:last_sentence_end + 1]
                    remaining = chapter_text[last_sentence_end + 1:].strip()
                    
                    chapter = ContentChapter(
                        title=f"Section {len(chapters) + 1}",
                        content=chapter_content,
                        word_count=len(chapter_content.split())
                    )
                    chapters.append(chapter)
                    
                    # Start new chapter with remaining text
                    current_words = remaining.split() if remaining else []
                else:
                    # No good break point, continue accumulating
                    continue
        
        # Add final chapter
        if current_words:
            chapter_content = ' '.join(current_words)
            chapter = ContentChapter(
                title=f"Section {len(chapters) + 1}",
                content=chapter_content,
                word_count=len(chapter_content.split())
            )
            chapters.append(chapter)
        
        return chapters
    
    async def _enhance_chapter(
        self,
        chapter: ContentChapter,
        index: int,
        metadata: Dict[str, Any]
    ) -> ContentChapter:
        """Enhance chapter with additional analysis."""
        
        # Extract key concepts for this chapter
        key_concepts = await self.concept_extractor.extract_concepts(chapter.content)
        
        # Assess difficulty level
        difficulty = await self._assess_difficulty(chapter.content)
        
        # Add timestamps if available
        start_timestamp = None
        end_timestamp = None
        
        if metadata.get("source_type") in ["youtube", "audio_file", "video_file"]:
            duration = metadata.get("duration", 0)
            if duration > 0:
                # Estimate timestamps based on chapter position
                total_chapters = metadata.get("total_chapters", 1)
                chapter_duration = duration / total_chapters
                start_timestamp = index * chapter_duration
                end_timestamp = (index + 1) * chapter_duration
        
        # Update chapter with enhancements
        chapter.key_concepts = key_concepts[:10]  # Limit to top 10
        chapter.difficulty_level = difficulty
        chapter.start_timestamp = start_timestamp
        chapter.end_timestamp = end_timestamp
        
        return chapter
    
    async def _assess_difficulty(self, content: str) -> DifficultyLevel:
        """Assess the difficulty level of content."""
        
        # Simple heuristics for difficulty assessment
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        
        # Calculate metrics
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Count complex indicators
        complex_words = sum(1 for word in words if len(word) > 7)
        technical_terms = sum(1 for word in words if word.lower() in [
            'algorithm', 'implementation', 'architecture', 'optimization',
            'methodology', 'framework', 'infrastructure', 'paradigm'
        ])
        
        # Calculate difficulty score
        difficulty_score = 0
        
        if avg_word_length > 6:
            difficulty_score += 1
        if avg_sentence_length > 20:
            difficulty_score += 1
        if complex_words / len(words) > 0.2:
            difficulty_score += 1
        if technical_terms / len(words) > 0.1:
            difficulty_score += 1
        
        # Map score to difficulty level
        if difficulty_score >= 3:
            return DifficultyLevel.EXPERT
        elif difficulty_score >= 2:
            return DifficultyLevel.HARD
        elif difficulty_score >= 1:
            return DifficultyLevel.MEDIUM
        else:
            return DifficultyLevel.EASY
    
    async def _detect_skill_tags(self, content: str) -> List[SkillTag]:
        """Detect skill tags based on content analysis."""
        
        detected_skills = []
        content_lower = content.lower()
        
        for skill, patterns in self.skill_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    detected_skills.append(skill)
                    break  # Found this skill, move to next
        
        return detected_skills
    
    async def _generate_summary(self, content: str, chapters: List[ContentChapter]) -> str:
        """Generate a summary of the content."""
        
        # Simple extractive summary
        sentences = re.split(r'[.!?]+', content)
        
        # Score sentences based on position and key terms
        sentence_scores = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) < 20:
                continue
            
            score = 0
            
            # Position bonus (first and last sentences)
            if i < 3 or i >= len(sentences) - 3:
                score += 2
            
            # Length bonus (moderate length preferred)
            if 50 <= len(sentence) <= 200:
                score += 1
            
            # Key term bonus
            key_terms = ['important', 'key', 'main', 'primary', 'essential', 'critical']
            for term in key_terms:
                if term in sentence.lower():
                    score += 1
            
            sentence_scores.append((sentence.strip(), score))
        
        # Select top sentences for summary
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:3]]
        
        return '. '.join(top_sentences) + '.'
    
    def _calculate_reading_time(self, content: str) -> int:
        """Calculate estimated reading time in minutes."""
        
        words = len(content.split())
        # Average reading speed: 200-250 words per minute
        reading_speed = 225
        
        return max(1, round(words / reading_speed))


# Component classes (simplified implementations)
class SemanticAnalyzer:
    """Semantic analysis component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def find_topic_boundaries(self, content: str):
        return []  # Simplified implementation


class ChapterDetector:
    """Chapter detection component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True


class ConceptExtractor:
    """Key concept extraction component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def extract_concepts(self, content: str):
        # Simple keyword extraction
        words = content.lower().split()
        word_freq = {}
        
        for word in words:
            if len(word) > 4 and word.isalpha():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top concepts
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:10]]


class SkillTagger:
    """Skill-based tagging component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
