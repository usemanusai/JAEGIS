"""
JAEGIS Cognitive Pipeline - Multi-Source Content Ingester
Handles ingestion from YouTube, PDFs, web URLs, and file uploads

This module implements the Tier 11 Content Ingestion Squad capabilities
for comprehensive multi-source content ingestion and validation.
"""

import asyncio
import aiohttp
import aiofiles
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import tempfile
import mimetypes
from urllib.parse import urlparse, parse_qs
import re

# Third-party imports for content processing
try:
    import yt_dlp
    import PyPDF2
    import fitz  # PyMuPDF
    from bs4 import BeautifulSoup
    import requests
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import whisper
except ImportError as e:
    logging.warning(f"Optional dependency not available: {e}")

logger = logging.getLogger(__name__)


class ContentIngestionError(Exception):
    """Custom exception for content ingestion errors."""
    pass


class MultiSourceIngester:
    """
    Multi-source content ingestion system implementing JAEGIS Tier 11 capabilities.
    
    Supports:
    - YouTube video/audio extraction
    - PDF document parsing
    - Web page scraping
    - File upload processing
    - Content validation and quality assessment
    """
    
    def __init__(self):
        self.youtube_extractor = None
        self.web_scraper = None
        self.pdf_processor = None
        self.audio_processor = None
        
        # Configuration
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.supported_formats = {
            "video": [".mp4", ".avi", ".mov", ".mkv", ".webm"],
            "audio": [".mp3", ".wav", ".m4a", ".flac", ".ogg"],
            "document": [".pdf", ".txt", ".docx", ".md"],
            "web": ["http", "https"]
        }
        
        # Quality thresholds
        self.quality_thresholds = {
            "min_content_length": 100,  # characters
            "min_word_count": 20,
            "max_noise_ratio": 0.3,
            "min_coherence_score": 0.6
        }
        
        logger.info("MultiSourceIngester initialized")
    
    async def initialize(self):
        """Initialize all ingestion components."""
        
        logger.info("🔄 Initializing Multi-Source Ingester")
        
        # Initialize YouTube extractor
        self.youtube_extractor = YouTubeExtractor()
        await self.youtube_extractor.initialize()
        
        # Initialize web scraper
        self.web_scraper = WebScraper()
        await self.web_scraper.initialize()
        
        # Initialize PDF processor
        self.pdf_processor = PDFProcessor()
        await self.pdf_processor.initialize()
        
        # Initialize audio processor
        self.audio_processor = AudioProcessor()
        await self.audio_processor.initialize()
        
        logger.info("✅ Multi-Source Ingester ready")
    
    async def cleanup(self):
        """Clean up resources."""
        
        if self.youtube_extractor:
            await self.youtube_extractor.cleanup()
        if self.web_scraper:
            await self.web_scraper.cleanup()
        if self.pdf_processor:
            await self.pdf_processor.cleanup()
        if self.audio_processor:
            await self.audio_processor.cleanup()
    
    async def health_check(self) -> bool:
        """Check health of all ingestion components."""
        
        try:
            checks = [
                self.youtube_extractor.health_check() if self.youtube_extractor else True,
                self.web_scraper.health_check() if self.web_scraper else True,
                self.pdf_processor.health_check() if self.pdf_processor else True,
                self.audio_processor.health_check() if self.audio_processor else True
            ]
            
            results = await asyncio.gather(*checks, return_exceptions=True)
            return all(result is True for result in results)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def ingest_content(
        self,
        source_type: str,
        source_url: Optional[str] = None,
        content_text: Optional[str] = None,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Main content ingestion method.
        
        Args:
            source_type: Type of source ("youtube", "pdf", "url", "file", "text")
            source_url: URL for web-based sources
            content_text: Direct text content or file path
            options: Additional processing options
        
        Returns:
            Dict containing extracted content, metadata, and quality metrics
        """
        
        if options is None:
            options = {}
        
        logger.info(f"📥 Starting ingestion - Type: {source_type}")
        
        try:
            if source_type == "youtube":
                return await self._ingest_youtube(source_url, options)
            elif source_type == "pdf":
                return await self._ingest_pdf(source_url or content_text, options)
            elif source_type == "url":
                return await self._ingest_web_url(source_url, options)
            elif source_type == "file":
                return await self._ingest_file(content_text, options)
            elif source_type == "text":
                return await self._ingest_text(content_text, options)
            else:
                raise ContentIngestionError(f"Unsupported source type: {source_type}")
                
        except Exception as e:
            logger.error(f"❌ Ingestion failed for {source_type}: {e}")
            raise ContentIngestionError(f"Failed to ingest {source_type}: {str(e)}")
    
    async def _ingest_youtube(self, url: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest content from YouTube URL."""
        
        logger.info(f"📺 Ingesting YouTube content: {url}")
        
        # Extract video information and content
        video_info = await self.youtube_extractor.extract_info(url)
        
        # Download audio for transcription if needed
        audio_path = None
        transcript = None
        
        if options.get("extract_audio", True):
            audio_path = await self.youtube_extractor.download_audio(url)
            transcript = await self.audio_processor.transcribe_audio(audio_path)
        
        # Get existing captions if available
        captions = await self.youtube_extractor.extract_captions(url)
        
        # Combine transcript sources
        content_text = self._combine_transcripts(transcript, captions)
        
        # Validate content quality
        quality_metrics = await self._assess_content_quality(content_text)
        
        return {
            "content": content_text,
            "metadata": {
                "source_type": "youtube",
                "source_url": url,
                "title": video_info.get("title", ""),
                "description": video_info.get("description", ""),
                "duration": video_info.get("duration", 0),
                "upload_date": video_info.get("upload_date", ""),
                "uploader": video_info.get("uploader", ""),
                "view_count": video_info.get("view_count", 0),
                "like_count": video_info.get("like_count", 0),
                "has_captions": bool(captions),
                "has_transcript": bool(transcript),
                "audio_path": audio_path
            },
            "quality_metrics": quality_metrics,
            "processing_info": {
                "ingestion_method": "youtube_api",
                "transcript_source": "audio" if transcript else "captions" if captions else "none",
                "processing_time": quality_metrics.get("processing_time", 0)
            }
        }
    
    async def _ingest_pdf(self, source: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest content from PDF document."""
        
        logger.info(f"📄 Ingesting PDF content: {source}")
        
        # Extract text and metadata from PDF
        pdf_data = await self.pdf_processor.extract_content(source)
        
        # Validate content quality
        quality_metrics = await self._assess_content_quality(pdf_data["text"])
        
        return {
            "content": pdf_data["text"],
            "metadata": {
                "source_type": "pdf",
                "source_path": source,
                "title": pdf_data["metadata"].get("title", ""),
                "author": pdf_data["metadata"].get("author", ""),
                "subject": pdf_data["metadata"].get("subject", ""),
                "creator": pdf_data["metadata"].get("creator", ""),
                "creation_date": pdf_data["metadata"].get("creation_date", ""),
                "modification_date": pdf_data["metadata"].get("modification_date", ""),
                "page_count": pdf_data["metadata"].get("page_count", 0),
                "has_images": pdf_data["metadata"].get("has_images", False),
                "has_tables": pdf_data["metadata"].get("has_tables", False)
            },
            "quality_metrics": quality_metrics,
            "processing_info": {
                "ingestion_method": "pdf_extraction",
                "extraction_method": pdf_data["extraction_method"],
                "processing_time": quality_metrics.get("processing_time", 0)
            }
        }
    
    async def _ingest_web_url(self, url: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest content from web URL."""
        
        logger.info(f"🌐 Ingesting web content: {url}")
        
        # Scrape web content
        web_data = await self.web_scraper.scrape_content(url, options)
        
        # Validate content quality
        quality_metrics = await self._assess_content_quality(web_data["text"])
        
        return {
            "content": web_data["text"],
            "metadata": {
                "source_type": "web_url",
                "source_url": url,
                "title": web_data["metadata"].get("title", ""),
                "description": web_data["metadata"].get("description", ""),
                "author": web_data["metadata"].get("author", ""),
                "publish_date": web_data["metadata"].get("publish_date", ""),
                "site_name": web_data["metadata"].get("site_name", ""),
                "language": web_data["metadata"].get("language", ""),
                "word_count": web_data["metadata"].get("word_count", 0),
                "has_images": web_data["metadata"].get("has_images", False),
                "has_videos": web_data["metadata"].get("has_videos", False)
            },
            "quality_metrics": quality_metrics,
            "processing_info": {
                "ingestion_method": "web_scraping",
                "scraping_method": web_data["scraping_method"],
                "processing_time": quality_metrics.get("processing_time", 0)
            }
        }
    
    async def _ingest_file(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest content from uploaded file."""
        
        logger.info(f"📁 Ingesting file content: {file_path}")
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ContentIngestionError(f"File not found: {file_path}")
        
        # Determine file type and process accordingly
        mime_type, _ = mimetypes.guess_type(str(file_path))
        file_extension = file_path.suffix.lower()
        
        if file_extension == ".pdf":
            return await self._ingest_pdf(str(file_path), options)
        elif file_extension in self.supported_formats["audio"]:
            return await self._ingest_audio_file(str(file_path), options)
        elif file_extension in self.supported_formats["video"]:
            return await self._ingest_video_file(str(file_path), options)
        elif file_extension in [".txt", ".md"]:
            return await self._ingest_text_file(str(file_path), options)
        else:
            raise ContentIngestionError(f"Unsupported file type: {file_extension}")
    
    async def _ingest_text(self, text: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest direct text content."""
        
        logger.info("📝 Ingesting direct text content")
        
        # Validate content quality
        quality_metrics = await self._assess_content_quality(text)
        
        return {
            "content": text,
            "metadata": {
                "source_type": "text",
                "character_count": len(text),
                "word_count": len(text.split()),
                "line_count": len(text.splitlines())
            },
            "quality_metrics": quality_metrics,
            "processing_info": {
                "ingestion_method": "direct_text",
                "processing_time": quality_metrics.get("processing_time", 0)
            }
        }
    
    async def _ingest_audio_file(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest content from audio file."""
        
        logger.info(f"🎵 Ingesting audio file: {file_path}")
        
        # Transcribe audio content
        transcript = await self.audio_processor.transcribe_audio(file_path)
        
        # Get audio metadata
        audio_metadata = await self.audio_processor.get_audio_metadata(file_path)
        
        # Validate content quality
        quality_metrics = await self._assess_content_quality(transcript)
        
        return {
            "content": transcript,
            "metadata": {
                "source_type": "audio_file",
                "source_path": file_path,
                "duration": audio_metadata.get("duration", 0),
                "format": audio_metadata.get("format", ""),
                "sample_rate": audio_metadata.get("sample_rate", 0),
                "channels": audio_metadata.get("channels", 0),
                "bitrate": audio_metadata.get("bitrate", 0)
            },
            "quality_metrics": quality_metrics,
            "processing_info": {
                "ingestion_method": "audio_transcription",
                "transcription_model": "whisper",
                "processing_time": quality_metrics.get("processing_time", 0)
            }
        }
    
    async def _ingest_video_file(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest content from video file."""
        
        logger.info(f"🎬 Ingesting video file: {file_path}")
        
        # Extract audio from video and transcribe
        audio_path = await self.audio_processor.extract_audio_from_video(file_path)
        transcript = await self.audio_processor.transcribe_audio(audio_path)
        
        # Get video metadata
        video_metadata = await self.audio_processor.get_video_metadata(file_path)
        
        # Validate content quality
        quality_metrics = await self._assess_content_quality(transcript)
        
        return {
            "content": transcript,
            "metadata": {
                "source_type": "video_file",
                "source_path": file_path,
                "duration": video_metadata.get("duration", 0),
                "format": video_metadata.get("format", ""),
                "resolution": video_metadata.get("resolution", ""),
                "fps": video_metadata.get("fps", 0),
                "video_codec": video_metadata.get("video_codec", ""),
                "audio_codec": video_metadata.get("audio_codec", ""),
                "extracted_audio_path": audio_path
            },
            "quality_metrics": quality_metrics,
            "processing_info": {
                "ingestion_method": "video_transcription",
                "transcription_model": "whisper",
                "processing_time": quality_metrics.get("processing_time", 0)
            }
        }
    
    async def _ingest_text_file(self, file_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest content from text file."""
        
        logger.info(f"📄 Ingesting text file: {file_path}")
        
        # Read text file content
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        # Validate content quality
        quality_metrics = await self._assess_content_quality(content)
        
        return {
            "content": content,
            "metadata": {
                "source_type": "text_file",
                "source_path": file_path,
                "file_size": Path(file_path).stat().st_size,
                "character_count": len(content),
                "word_count": len(content.split()),
                "line_count": len(content.splitlines())
            },
            "quality_metrics": quality_metrics,
            "processing_info": {
                "ingestion_method": "text_file_read",
                "encoding": "utf-8",
                "processing_time": quality_metrics.get("processing_time", 0)
            }
        }
    
    def _combine_transcripts(self, transcript: Optional[str], captions: Optional[str]) -> str:
        """Combine multiple transcript sources."""
        
        if transcript and captions:
            # Prefer transcript over captions, but use captions as fallback
            return transcript if len(transcript) > len(captions) else captions
        elif transcript:
            return transcript
        elif captions:
            return captions
        else:
            return ""
    
    async def _assess_content_quality(self, content: str) -> Dict[str, Any]:
        """Assess the quality of extracted content."""
        
        if not content:
            return {
                "quality_score": 0,
                "issues": ["empty_content"],
                "character_count": 0,
                "word_count": 0,
                "coherence_score": 0,
                "noise_ratio": 1.0
            }
        
        # Basic metrics
        char_count = len(content)
        word_count = len(content.split())
        line_count = len(content.splitlines())
        
        # Quality assessment
        issues = []
        quality_score = 100
        
        # Check minimum length
        if char_count < self.quality_thresholds["min_content_length"]:
            issues.append("content_too_short")
            quality_score -= 30
        
        if word_count < self.quality_thresholds["min_word_count"]:
            issues.append("insufficient_words")
            quality_score -= 20
        
        # Estimate noise ratio (repeated characters, special characters, etc.)
        noise_ratio = self._calculate_noise_ratio(content)
        if noise_ratio > self.quality_thresholds["max_noise_ratio"]:
            issues.append("high_noise_ratio")
            quality_score -= 25
        
        # Estimate coherence (basic heuristics)
        coherence_score = self._estimate_coherence(content)
        if coherence_score < self.quality_thresholds["min_coherence_score"]:
            issues.append("low_coherence")
            quality_score -= 15
        
        return {
            "quality_score": max(0, quality_score),
            "issues": issues,
            "character_count": char_count,
            "word_count": word_count,
            "line_count": line_count,
            "coherence_score": coherence_score,
            "noise_ratio": noise_ratio,
            "processing_time": 0.1  # Placeholder
        }
    
    def _calculate_noise_ratio(self, content: str) -> float:
        """Calculate the ratio of noise to signal in content."""
        
        if not content:
            return 1.0
        
        # Count various noise indicators
        special_chars = len(re.findall(r'[^\w\s]', content))
        repeated_chars = len(re.findall(r'(.)\1{3,}', content))
        total_chars = len(content)
        
        noise_score = (special_chars * 0.1 + repeated_chars * 0.5) / total_chars
        return min(1.0, noise_score)
    
    def _estimate_coherence(self, content: str) -> float:
        """Estimate content coherence using basic heuristics."""
        
        if not content:
            return 0.0
        
        words = content.split()
        if len(words) < 10:
            return 0.5
        
        # Basic coherence indicators
        sentences = re.split(r'[.!?]+', content)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        # Reasonable sentence length indicates coherence
        if 5 <= avg_sentence_length <= 25:
            coherence = 0.8
        else:
            coherence = 0.5
        
        # Check for common English words (basic indicator)
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        word_set = set(word.lower() for word in words)
        common_word_ratio = len(word_set & common_words) / len(common_words)
        
        coherence += common_word_ratio * 0.2
        
        return min(1.0, coherence)


# Component classes (simplified implementations)
class YouTubeExtractor:
    """YouTube content extraction component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def extract_info(self, url: str):
        return {"title": "Sample Video", "duration": 300}
    
    async def download_audio(self, url: str):
        return "/tmp/audio.mp3"
    
    async def extract_captions(self, url: str):
        return "Sample captions"


class WebScraper:
    """Web content scraping component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def scrape_content(self, url: str, options: Dict[str, Any]):
        return {
            "text": "Sample web content",
            "metadata": {"title": "Sample Page"},
            "scraping_method": "requests"
        }


class PDFProcessor:
    """PDF document processing component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def extract_content(self, source: str):
        return {
            "text": "Sample PDF content",
            "metadata": {"title": "Sample PDF", "page_count": 10},
            "extraction_method": "pypdf2"
        }


class AudioProcessor:
    """Audio processing and transcription component."""
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def health_check(self):
        return True
    
    async def transcribe_audio(self, file_path: str):
        return "Sample audio transcript"
    
    async def get_audio_metadata(self, file_path: str):
        return {"duration": 300, "format": "mp3"}
    
    async def extract_audio_from_video(self, file_path: str):
        return "/tmp/extracted_audio.mp3"
    
    async def get_video_metadata(self, file_path: str):
        return {"duration": 300, "format": "mp4"}
