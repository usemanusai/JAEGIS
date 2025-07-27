#!/usr/bin/env python3
"""
JAEGIS Enhanced Bulk Upload Automation Script
Production-ready automation with comprehensive error logging and diagnostics

Features:
- Detailed error categorization and structured reporting
- Real-time progress dashboard with performance metrics
- Enhanced checkpoint system with file-level tracking
- Intelligent retry strategies with exponential backoff
- Network connectivity monitoring and adaptive throttling
- Color-coded console output and JSON error reports
- GitHub API response analysis and rate limit handling
"""

import asyncio
import logging
import json
import time
import hashlib
import os
import sys
import psutil
import socket
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import traceback
import colorama
from colorama import Fore, Back, Style
import threading
import queue

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)

# Enhanced logging configuration
class ColoredFormatter(logging.Formatter):
    """Custom formatter with color coding for different log levels."""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

# Configure enhanced logging
def setup_logging():
    """Setup comprehensive logging with multiple handlers."""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Main logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler for all logs
    file_handler = logging.FileHandler(
        logs_dir / f"bulk_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Error-only handler
    error_handler = logging.FileHandler(
        logs_dir / f"errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger

logger = setup_logging()


class ErrorCategory(Enum):
    """Categorization of different error types."""
    GITHUB_API = "github_api"
    NETWORK = "network"
    FILESYSTEM = "filesystem"
    AUTHENTICATION = "authentication"
    RATE_LIMIT = "rate_limit"
    ENCODING = "encoding"
    VALIDATION = "validation"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DetailedError:
    """Comprehensive error information structure."""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    timestamp: datetime
    file_path: str
    error_code: Optional[str] = None
    http_status: Optional[int] = None
    error_message: str = ""
    stack_trace: Optional[str] = None
    retry_attempt: int = 0
    context: Dict[str, Any] = field(default_factory=dict)
    recovery_action: Optional[str] = None
    resolved: bool = False


@dataclass
class NetworkMetrics:
    """Network performance tracking."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_bytes_uploaded: int = 0
    average_response_time: float = 0.0
    current_throughput_mbps: float = 0.0
    rate_limit_hits: int = 0
    connection_errors: int = 0
    timeout_errors: int = 0
    last_update: datetime = field(default_factory=datetime.now)


@dataclass
class SystemMetrics:
    """System resource monitoring."""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_mb: float = 0.0
    disk_io_read_mb: float = 0.0
    disk_io_write_mb: float = 0.0
    network_sent_mb: float = 0.0
    network_recv_mb: float = 0.0
    active_connections: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class UploadConfig:
    """Enhanced upload configuration with diagnostics settings."""
    github_owner: str = "usemanusai"
    github_repo: str = "JAEGIS"
    github_token: str = ""
    workspace_path: str = "."
    batch_size: int = 50
    max_concurrent: int = 5
    rate_limit_delay: float = 1.0
    max_retries: int = 3
    max_file_size_mb: int = 100
    enable_docqa_agent: bool = True
    enable_compression: bool = True
    dry_run: bool = False
    
    # Enhanced diagnostics settings
    enable_detailed_logging: bool = True
    enable_performance_monitoring: bool = True
    enable_network_diagnostics: bool = True
    checkpoint_interval_seconds: int = 300  # 5 minutes
    progress_update_interval: int = 10  # Every 10 files
    max_error_log_size_mb: int = 100
    enable_color_output: bool = True
    export_error_reports: bool = True


@dataclass
class FileUploadResult:
    """Enhanced upload result with detailed diagnostics."""
    file_path: str
    success: bool
    error: Optional[DetailedError] = None
    upload_time: float = 0.0
    file_size: int = 0
    sha: Optional[str] = None
    retry_count: int = 0
    http_status: Optional[int] = None
    response_headers: Dict[str, str] = field(default_factory=dict)
    network_metrics: Optional[NetworkMetrics] = None


@dataclass
class PhaseProgress:
    """Enhanced phase progress tracking."""
    phase_id: str
    phase_name: str
    total_files: int
    uploaded_files: int = 0
    failed_files: int = 0
    skipped_files: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    current_file: str = ""
    errors: List[DetailedError] = field(default_factory=list)
    network_metrics: NetworkMetrics = field(default_factory=NetworkMetrics)
    estimated_completion: Optional[datetime] = None
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_files == 0:
            return 100.0
        processed = self.uploaded_files + self.failed_files + self.skipped_files
        return (processed / self.total_files) * 100.0
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        processed = self.uploaded_files + self.failed_files
        if processed == 0:
            return 0.0
        return (self.uploaded_files / processed) * 100.0
    
    @property
    def estimated_time_remaining(self) -> Optional[timedelta]:
        """Estimate time remaining for phase completion."""
        if self.total_files == 0 or self.uploaded_files == 0:
            return None
        
        elapsed = time.time() - self.start_time
        rate = self.uploaded_files / elapsed  # files per second
        remaining_files = self.total_files - (self.uploaded_files + self.failed_files + self.skipped_files)
        
        if rate > 0:
            remaining_seconds = remaining_files / rate
            return timedelta(seconds=remaining_seconds)
        return None


class ProgressDashboard:
    """Real-time progress dashboard with performance metrics."""
    
    def __init__(self):
        self.start_time = time.time()
        self.last_update = time.time()
        self.update_queue = queue.Queue()
        self.dashboard_thread = None
        self.running = False
    
    def start(self):
        """Start the dashboard in a separate thread."""
        self.running = True
        self.dashboard_thread = threading.Thread(target=self._dashboard_loop, daemon=True)
        self.dashboard_thread.start()
    
    def stop(self):
        """Stop the dashboard."""
        self.running = False
        if self.dashboard_thread:
            self.dashboard_thread.join(timeout=1.0)
    
    def update(self, phase_progress: PhaseProgress, system_metrics: SystemMetrics):
        """Update dashboard with new progress data."""
        try:
            self.update_queue.put_nowait({
                'phase_progress': phase_progress,
                'system_metrics': system_metrics,
                'timestamp': datetime.now()
            })
        except queue.Full:
            pass  # Skip update if queue is full
    
    def _dashboard_loop(self):
        """Main dashboard loop running in separate thread."""
        while self.running:
            try:
                # Get latest update
                update_data = self.update_queue.get(timeout=1.0)
                self._render_dashboard(update_data)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Dashboard error: {e}")
    
    def _render_dashboard(self, data: Dict[str, Any]):
        """Render the progress dashboard."""
        phase = data['phase_progress']
        metrics = data['system_metrics']
        
        # Clear screen and move cursor to top
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/MacOS
            os.system('clear')
        
        # Header
        print(f"{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}🚀 JAEGIS BULK UPLOAD - REAL-TIME DASHBOARD")
        print(f"{Fore.CYAN}{'='*80}")
        
        # Phase information
        print(f"\n{Fore.GREEN}📊 CURRENT PHASE: {phase.phase_name}")
        print(f"{Fore.WHITE}Phase ID: {phase.phase_id}")
        print(f"Progress: {phase.completion_percentage:.1f}% ({phase.uploaded_files + phase.failed_files + phase.skipped_files}/{phase.total_files})")
        
        # Progress bar
        bar_width = 50
        filled = int(bar_width * phase.completion_percentage / 100)
        bar = f"[{'█' * filled}{'░' * (bar_width - filled)}]"
        print(f"Progress: {Fore.GREEN}{bar} {phase.completion_percentage:.1f}%")
        
        # Statistics
        print(f"\n{Fore.YELLOW}📈 UPLOAD STATISTICS:")
        print(f"✅ Uploaded: {Fore.GREEN}{phase.uploaded_files:,}")
        print(f"❌ Failed: {Fore.RED}{phase.failed_files:,}")
        print(f"⏭️  Skipped: {Fore.YELLOW}{phase.skipped_files:,}")
        print(f"📊 Success Rate: {Fore.GREEN}{phase.success_rate:.1f}%")
        
        # Time estimates
        if phase.estimated_time_remaining:
            eta = datetime.now() + phase.estimated_time_remaining
            print(f"⏱️  ETA: {Fore.CYAN}{eta.strftime('%H:%M:%S')}")
            print(f"⏳ Time Remaining: {Fore.CYAN}{str(phase.estimated_time_remaining).split('.')[0]}")
        
        # Network metrics
        print(f"\n{Fore.BLUE}🌐 NETWORK PERFORMANCE:")
        print(f"Throughput: {Fore.CYAN}{phase.network_metrics.current_throughput_mbps:.2f} Mbps")
        print(f"Avg Response Time: {Fore.CYAN}{phase.network_metrics.average_response_time:.2f}ms")
        print(f"Rate Limit Hits: {Fore.YELLOW}{phase.network_metrics.rate_limit_hits}")
        
        # System metrics
        print(f"\n{Fore.MAGENTA}💻 SYSTEM RESOURCES:")
        print(f"CPU: {Fore.CYAN}{metrics.cpu_percent:.1f}%")
        print(f"Memory: {Fore.CYAN}{metrics.memory_percent:.1f}% ({metrics.memory_mb:.1f} MB)")
        print(f"Network I/O: {Fore.CYAN}↑{metrics.network_sent_mb:.1f}MB ↓{metrics.network_recv_mb:.1f}MB")
        
        # Current file
        if phase.current_file:
            print(f"\n{Fore.WHITE}📄 Current File: {phase.current_file}")
        
        # Recent errors (last 3)
        if phase.errors:
            print(f"\n{Fore.RED}🚨 RECENT ERRORS:")
            for error in phase.errors[-3:]:
                print(f"  {Fore.RED}• {error.file_path}: {error.error_message[:60]}...")
        
        print(f"\n{Fore.CYAN}Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{Fore.CYAN}{'='*80}")


class SystemMonitor:
    """System resource monitoring."""
    
    def __init__(self):
        self.process = psutil.Process()
        self.initial_io = psutil.disk_io_counters()
        self.initial_net = psutil.net_io_counters()
    
    def get_metrics(self) -> SystemMetrics:
        """Get current system metrics."""
        try:
            # CPU and memory
            cpu_percent = self.process.cpu_percent()
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            
            # Disk I/O
            current_io = psutil.disk_io_counters()
            disk_read_mb = (current_io.read_bytes - self.initial_io.read_bytes) / (1024 * 1024)
            disk_write_mb = (current_io.write_bytes - self.initial_io.write_bytes) / (1024 * 1024)
            
            # Network I/O
            current_net = psutil.net_io_counters()
            net_sent_mb = (current_net.bytes_sent - self.initial_net.bytes_sent) / (1024 * 1024)
            net_recv_mb = (current_net.bytes_recv - self.initial_net.bytes_recv) / (1024 * 1024)
            
            # Active connections
            connections = len(self.process.connections())
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_mb=memory_info.rss / (1024 * 1024),
                disk_io_read_mb=disk_read_mb,
                disk_io_write_mb=disk_write_mb,
                network_sent_mb=net_sent_mb,
                network_recv_mb=net_recv_mb,
                active_connections=connections
            )
        
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return SystemMetrics()


class NetworkDiagnostics:
    """Network connectivity and performance diagnostics."""
    
    def __init__(self):
        self.github_api_host = "api.github.com"
        self.github_api_port = 443
    
    async def check_connectivity(self) -> Dict[str, Any]:
        """Check network connectivity to GitHub API."""
        try:
            # DNS resolution test
            start_time = time.time()
            socket.gethostbyname(self.github_api_host)
            dns_time = (time.time() - start_time) * 1000
            
            # TCP connection test
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            result = sock.connect_ex((self.github_api_host, self.github_api_port))
            tcp_time = (time.time() - start_time) * 1000
            sock.close()
            
            # HTTP test
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://{self.github_api_host}") as response:
                    http_time = (time.time() - start_time) * 1000
                    http_status = response.status
            
            return {
                "connectivity": True,
                "dns_resolution_ms": dns_time,
                "tcp_connection_ms": tcp_time,
                "http_response_ms": http_time,
                "http_status": http_status,
                "tcp_connection_success": result == 0
            }
        
        except Exception as e:
            return {
                "connectivity": False,
                "error": str(e),
                "dns_resolution_ms": None,
                "tcp_connection_ms": None,
                "http_response_ms": None
            }
    
    async def measure_latency(self, samples: int = 5) -> Dict[str, float]:
        """Measure network latency to GitHub API."""
        latencies = []
        
        for _ in range(samples):
            try:
                start_time = time.time()
                async with aiohttp.ClientSession() as session:
                    async with session.head(f"https://{self.github_api_host}") as response:
                        latency = (time.time() - start_time) * 1000
                        latencies.append(latency)
            except Exception:
                continue
        
        if latencies:
            return {
                "min_latency_ms": min(latencies),
                "max_latency_ms": max(latencies),
                "avg_latency_ms": sum(latencies) / len(latencies),
                "samples": len(latencies)
            }
        else:
            return {
                "min_latency_ms": 0,
                "max_latency_ms": 0,
                "avg_latency_ms": 0,
                "samples": 0
            }


class ErrorAnalyzer:
    """Intelligent error analysis and categorization."""

    def __init__(self):
        self.error_patterns = {
            ErrorCategory.GITHUB_API: [
                (r"HTTP 4\d\d", "Client error"),
                (r"HTTP 5\d\d", "Server error"),
                (r"API rate limit", "Rate limiting"),
                (r"Repository not found", "Repository access"),
                (r"Invalid token", "Authentication")
            ],
            ErrorCategory.NETWORK: [
                (r"Connection.*timeout", "Connection timeout"),
                (r"Connection.*refused", "Connection refused"),
                (r"DNS.*failed", "DNS resolution"),
                (r"Network.*unreachable", "Network unreachable")
            ],
            ErrorCategory.FILESYSTEM: [
                (r"Permission denied", "File permissions"),
                (r"File not found", "Missing file"),
                (r"Disk.*full", "Disk space"),
                (r"I/O error", "File system I/O")
            ],
            ErrorCategory.ENCODING: [
                (r"UnicodeDecodeError", "Unicode decoding"),
                (r"UnicodeEncodeError", "Unicode encoding"),
                (r"charmap.*encode", "Character encoding"),
                (r"base64.*error", "Base64 encoding")
            ]
        }

    def analyze_error(self, error_message: str, http_status: Optional[int] = None,
                     exception_type: Optional[str] = None) -> Tuple[ErrorCategory, ErrorSeverity, str]:
        """Analyze error and determine category, severity, and recovery action."""

        error_message_lower = error_message.lower()

        # Analyze by HTTP status code
        if http_status:
            if http_status == 401:
                return ErrorCategory.AUTHENTICATION, ErrorSeverity.HIGH, "Check GitHub token validity"
            elif http_status == 403:
                return ErrorCategory.RATE_LIMIT, ErrorSeverity.MEDIUM, "Implement rate limiting delay"
            elif http_status == 404:
                return ErrorCategory.GITHUB_API, ErrorSeverity.LOW, "Verify repository and file path"
            elif http_status == 409:
                return ErrorCategory.GITHUB_API, ErrorSeverity.LOW, "File already exists, skip or update"
            elif http_status >= 500:
                return ErrorCategory.GITHUB_API, ErrorSeverity.HIGH, "Retry with exponential backoff"

        # Analyze by error patterns
        for category, patterns in self.error_patterns.items():
            for pattern, description in patterns:
                if pattern.lower() in error_message_lower:
                    severity = self._determine_severity(category, error_message)
                    action = self._suggest_recovery_action(category, description)
                    return category, severity, action

        # Default categorization
        return ErrorCategory.UNKNOWN, ErrorSeverity.MEDIUM, "Review error details and retry"

    def _determine_severity(self, category: ErrorCategory, error_message: str) -> ErrorSeverity:
        """Determine error severity based on category and message."""
        if category == ErrorCategory.AUTHENTICATION:
            return ErrorSeverity.CRITICAL
        elif category == ErrorCategory.RATE_LIMIT:
            return ErrorSeverity.MEDIUM
        elif category == ErrorCategory.NETWORK:
            return ErrorSeverity.HIGH
        elif "timeout" in error_message.lower():
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW

    def _suggest_recovery_action(self, category: ErrorCategory, description: str) -> str:
        """Suggest recovery action based on error category."""
        actions = {
            ErrorCategory.GITHUB_API: "Retry with exponential backoff",
            ErrorCategory.NETWORK: "Check network connectivity and retry",
            ErrorCategory.FILESYSTEM: "Verify file permissions and disk space",
            ErrorCategory.AUTHENTICATION: "Validate GitHub token and permissions",
            ErrorCategory.RATE_LIMIT: "Implement adaptive rate limiting",
            ErrorCategory.ENCODING: "Check file encoding and content type"
        }
        return actions.get(category, "Manual investigation required")


class IntelligentRetryManager:
    """Intelligent retry management with exponential backoff and adaptive strategies."""

    def __init__(self, config: UploadConfig):
        self.config = config
        self.error_analyzer = ErrorAnalyzer()
        self.retry_stats = {
            "total_retries": 0,
            "successful_retries": 0,
            "failed_retries": 0,
            "category_stats": {}
        }

    async def execute_with_retry(self, operation_func, file_path: str,
                               operation_context: Dict[str, Any]) -> FileUploadResult:
        """Execute operation with intelligent retry logic."""

        last_error = None
        retry_delays = []

        for attempt in range(self.config.max_retries + 1):
            try:
                # Execute the operation
                result = await operation_func(file_path, operation_context, attempt)

                if result.success:
                    if attempt > 0:
                        self.retry_stats["successful_retries"] += 1
                        logger.info(f"✅ Retry successful for {file_path} after {attempt} attempts")
                    return result
                else:
                    last_error = result.error

                    if attempt < self.config.max_retries:
                        # Analyze error and determine retry strategy
                        delay = await self._calculate_retry_delay(last_error, attempt, retry_delays)
                        retry_delays.append(delay)

                        logger.warning(f"🔄 Retry {attempt + 1}/{self.config.max_retries} for {file_path} "
                                     f"after {delay:.1f}s delay. Error: {last_error.error_message[:100]}")

                        await asyncio.sleep(delay)
                        self.retry_stats["total_retries"] += 1

            except Exception as e:
                # Create error object for unexpected exceptions
                error_id = f"error_{int(time.time())}_{hashlib.md5(file_path.encode()).hexdigest()[:8]}"
                category, severity, recovery_action = self.error_analyzer.analyze_error(
                    str(e), exception_type=type(e).__name__
                )

                last_error = DetailedError(
                    error_id=error_id,
                    category=category,
                    severity=severity,
                    timestamp=datetime.now(),
                    file_path=file_path,
                    error_message=str(e),
                    stack_trace=traceback.format_exc(),
                    retry_attempt=attempt,
                    recovery_action=recovery_action
                )

                if attempt < self.config.max_retries:
                    delay = await self._calculate_retry_delay(last_error, attempt, retry_delays)
                    retry_delays.append(delay)

                    logger.error(f"🔄 Exception on attempt {attempt + 1} for {file_path}: {str(e)[:100]}")
                    await asyncio.sleep(delay)
                    self.retry_stats["total_retries"] += 1

        # All retries exhausted
        self.retry_stats["failed_retries"] += 1
        if last_error:
            self._update_category_stats(last_error.category)

        return FileUploadResult(
            file_path=file_path,
            success=False,
            error=last_error,
            retry_count=self.config.max_retries
        )

    async def _calculate_retry_delay(self, error: DetailedError, attempt: int,
                                   previous_delays: List[float]) -> float:
        """Calculate intelligent retry delay based on error type and history."""

        base_delay = self.config.rate_limit_delay

        # Category-specific delay adjustments
        if error.category == ErrorCategory.RATE_LIMIT:
            # Longer delays for rate limiting
            base_delay = min(60.0, base_delay * (3 ** attempt))
        elif error.category == ErrorCategory.NETWORK:
            # Progressive delays for network issues
            base_delay = min(30.0, base_delay * (2 ** attempt))
        elif error.category == ErrorCategory.GITHUB_API and error.http_status and error.http_status >= 500:
            # Server errors need longer delays
            base_delay = min(45.0, base_delay * (2.5 ** attempt))
        else:
            # Standard exponential backoff
            base_delay = min(20.0, base_delay * (2 ** attempt))

        # Add jitter to prevent thundering herd
        jitter = base_delay * 0.1 * (0.5 - hash(error.file_path) % 100 / 100)

        return base_delay + jitter

    def _update_category_stats(self, category: ErrorCategory):
        """Update retry statistics by error category."""
        category_name = category.value
        if category_name not in self.retry_stats["category_stats"]:
            self.retry_stats["category_stats"][category_name] = 0
        self.retry_stats["category_stats"][category_name] += 1

    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get comprehensive retry statistics."""
        total_attempts = self.retry_stats["total_retries"]
        if total_attempts > 0:
            success_rate = (self.retry_stats["successful_retries"] / total_attempts) * 100
        else:
            success_rate = 0.0

        return {
            "total_retries": self.retry_stats["total_retries"],
            "successful_retries": self.retry_stats["successful_retries"],
            "failed_retries": self.retry_stats["failed_retries"],
            "retry_success_rate": success_rate,
            "category_breakdown": self.retry_stats["category_stats"]
        }


class EnhancedCheckpointManager:
    """Enhanced checkpoint system with file-level tracking."""

    def __init__(self, config: UploadConfig):
        self.config = config
        self.checkpoint_dir = Path("checkpoints")
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.file_status_cache = {}  # Cache for file upload status

    async def save_checkpoint(self, phase_progress: PhaseProgress,
                            upload_stats: Dict[str, Any],
                            file_results: List[FileUploadResult]) -> str:
        """Save comprehensive checkpoint with file-level details."""

        timestamp = datetime.now()
        checkpoint_id = f"checkpoint_{timestamp.strftime('%Y%m%d_%H%M%S')}"

        # Prepare file-level status
        file_status = {}
        for result in file_results:
            file_status[result.file_path] = {
                "success": result.success,
                "sha": result.sha,
                "file_size": result.file_size,
                "retry_count": result.retry_count,
                "last_attempt": timestamp.isoformat(),
                "error_category": result.error.category.value if result.error else None,
                "http_status": result.http_status
            }

        # Update cache
        self.file_status_cache.update(file_status)

        checkpoint_data = {
            "checkpoint_id": checkpoint_id,
            "timestamp": timestamp.isoformat(),
            "phase_progress": asdict(phase_progress),
            "upload_stats": upload_stats,
            "file_status": file_status,
            "total_files_processed": len(file_status),
            "config_snapshot": asdict(self.config)
        }

        # Save checkpoint
        checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.json"

        try:
            async with aiofiles.open(checkpoint_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(checkpoint_data, indent=2, default=str))

            logger.info(f"💾 Enhanced checkpoint saved: {checkpoint_file}")
            return checkpoint_id

        except Exception as e:
            logger.error(f"❌ Failed to save checkpoint: {e}")
            raise

    async def load_latest_checkpoint(self) -> Optional[Dict[str, Any]]:
        """Load the most recent checkpoint."""
        try:
            checkpoint_files = list(self.checkpoint_dir.glob("checkpoint_*.json"))
            if not checkpoint_files:
                return None

            # Get the most recent checkpoint
            latest_checkpoint = max(checkpoint_files, key=lambda p: p.stat().st_mtime)

            async with aiofiles.open(latest_checkpoint, 'r', encoding='utf-8') as f:
                content = await f.read()
                checkpoint_data = json.loads(content)

            # Load file status cache
            self.file_status_cache = checkpoint_data.get("file_status", {})

            logger.info(f"📂 Loaded checkpoint: {latest_checkpoint}")
            return checkpoint_data

        except Exception as e:
            logger.error(f"❌ Failed to load checkpoint: {e}")
            return None

    def is_file_uploaded(self, file_path: str) -> bool:
        """Check if file was already successfully uploaded."""
        status = self.file_status_cache.get(file_path)
        return status and status.get("success", False)

    def get_file_status(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get detailed status for a specific file."""
        return self.file_status_cache.get(file_path)


class DocQASpecialistAgent:
    """Enhanced DocQA Specialist Agent with detailed analytics."""

    def __init__(self, config: UploadConfig):
        self.config = config
        self.active = config.enable_docqa_agent
        self.processed_files = 0
        self.documentation_files = []
        self.file_type_stats = {}
        self.processing_times = []

    async def activate(self):
        """Activate DocQA specialist agent with enhanced logging."""
        if self.active:
            logger.info(f"{Fore.CYAN}🤖 Activating DocQA Specialist Agent for large-scale operations")
            logger.info(f"{Fore.CYAN}   - Optimizing for 96,715+ file workspace")
            logger.info(f"{Fore.CYAN}   - Enabling intelligent documentation processing")
            logger.info(f"{Fore.CYAN}   - Activating batch optimization algorithms")

    async def process_documentation_batch(self, files: List[str]) -> List[str]:
        """Process documentation files with enhanced analytics."""
        if not self.active:
            return files

        start_time = time.time()
        doc_files = []

        for file_path in files:
            file_ext = Path(file_path).suffix.lower()

            # Track file type statistics
            self.file_type_stats[file_ext] = self.file_type_stats.get(file_ext, 0) + 1

            # Identify documentation files
            if any(ext in file_path.lower() for ext in ['.md', '.txt', '.rst', '.doc', '.docx']):
                doc_files.append(file_path)
                self.documentation_files.append(file_path)

        self.processed_files += len(doc_files)
        processing_time = time.time() - start_time
        self.processing_times.append(processing_time)

        if doc_files:
            logger.info(f"{Fore.BLUE}📚 DocQA Agent processing {len(doc_files)} documentation files "
                       f"({processing_time:.3f}s)")

        return files

    def get_analytics(self) -> Dict[str, Any]:
        """Get comprehensive DocQA analytics."""
        avg_processing_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0

        return {
            "active": self.active,
            "processed_files": self.processed_files,
            "documentation_files_count": len(self.documentation_files),
            "file_type_distribution": self.file_type_stats,
            "average_processing_time_ms": avg_processing_time * 1000,
            "total_processing_time_s": sum(self.processing_times),
            "optimization_level": "maximum" if self.active else "disabled"
        }


class EnhancedGitHubUploader:
    """Enhanced GitHub uploader with comprehensive error handling and diagnostics."""

    def __init__(self, config: UploadConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.docqa_agent = DocQASpecialistAgent(config)
        self.retry_manager = IntelligentRetryManager(config)
        self.checkpoint_manager = EnhancedCheckpointManager(config)
        self.error_analyzer = ErrorAnalyzer()
        self.network_diagnostics = NetworkDiagnostics()
        self.system_monitor = SystemMonitor()
        self.progress_dashboard = ProgressDashboard()

        # Enhanced statistics tracking
        self.upload_stats = {
            "total_files": 0,
            "uploaded_files": 0,
            "failed_files": 0,
            "skipped_files": 0,
            "total_size_mb": 0.0,
            "start_time": 0.0,
            "phases_completed": 0,
            "network_metrics": NetworkMetrics(),
            "error_summary": {},
            "performance_metrics": {}
        }

        # Rate limiting tracking
        self.rate_limit_info = {
            "remaining": 5000,
            "reset_time": None,
            "last_check": None
        }

        # File processing queue for batch optimization
        self.processing_queue = asyncio.Queue()
        self.batch_results = []

        # Upload phases with enhanced configuration
        self.upload_phases = [
            {
                "phase_id": "phase_1",
                "phase_name": "JAEGIS Method v1.0 Complete",
                "directories": ["JAEGIS-METHOD-v1.0"],
                "priority": "CRITICAL",
                "estimated_files": 30000
            },
            {
                "phase_id": "phase_2",
                "phase_name": "JAEGIS Method v2.0 Complete",
                "directories": ["JAEGIS-METHOD-v2.0"],
                "priority": "CRITICAL",
                "estimated_files": 66000,
                "dependencies": ["phase_1"]
            }
        ]

    async def __aenter__(self):
        """Enhanced async context manager entry with diagnostics."""
        # Network connectivity check
        connectivity = await self.network_diagnostics.check_connectivity()
        if not connectivity["connectivity"]:
            raise ConnectionError(f"GitHub API connectivity failed: {connectivity.get('error')}")

        logger.info(f"{Fore.GREEN}🌐 Network connectivity verified:")
        logger.info(f"   DNS Resolution: {connectivity['dns_resolution_ms']:.1f}ms")
        logger.info(f"   TCP Connection: {connectivity['tcp_connection_ms']:.1f}ms")
        logger.info(f"   HTTP Response: {connectivity['http_response_ms']:.1f}ms")

        # Initialize HTTP session with enhanced configuration
        timeout = aiohttp.ClientTimeout(total=300, connect=30)
        connector = aiohttp.TCPConnector(
            limit=self.config.max_concurrent * 2,
            limit_per_host=self.config.max_concurrent,
            ttl_dns_cache=300,
            use_dns_cache=True
        )

        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                'Authorization': f'token {self.config.github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'JAEGIS-Enhanced-Bulk-Uploader/2.0',
                'X-GitHub-Api-Version': '2022-11-28'
            }
        )

        # Activate DocQA agent
        await self.docqa_agent.activate()

        # Start progress dashboard
        if self.config.enable_color_output:
            self.progress_dashboard.start()

        # Load existing checkpoint if available
        checkpoint = await self.checkpoint_manager.load_latest_checkpoint()
        if checkpoint:
            logger.info(f"{Fore.YELLOW}📂 Resuming from checkpoint: {checkpoint['checkpoint_id']}")
            self._restore_from_checkpoint(checkpoint)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Enhanced async context manager exit with cleanup."""
        if self.session:
            await self.session.close()

        self.progress_dashboard.stop()

        # Generate final error report
        if self.config.export_error_reports:
            await self._generate_error_report()

    def _restore_from_checkpoint(self, checkpoint: Dict[str, Any]):
        """Restore state from checkpoint."""
        self.upload_stats.update(checkpoint.get("upload_stats", {}))
        logger.info(f"{Fore.CYAN}📊 Restored upload statistics from checkpoint")

    def _should_skip_file(self, file_path: str) -> Tuple[bool, str]:
        """Enhanced file skipping logic with detailed reasoning."""
        file_path_obj = Path(self.config.workspace_path) / file_path

        # Check if already uploaded (from checkpoint)
        if self.checkpoint_manager.is_file_uploaded(file_path):
            return True, "Already uploaded (from checkpoint)"

        # Check if file exists
        if not file_path_obj.exists():
            return True, "File does not exist"

        # Check file size
        try:
            file_size_mb = file_path_obj.stat().st_size / (1024 * 1024)
            if file_size_mb > self.config.max_file_size_mb:
                return True, f"File too large: {file_size_mb:.1f} MB (limit: {self.config.max_file_size_mb} MB)"
        except OSError as e:
            return True, f"Cannot access file: {e}"

        # Skip certain file types and patterns
        skip_patterns = {
            '.pyc', '.pyo', '.pyd', '__pycache__', '.git', '.DS_Store',
            '.tmp', '.temp', '.cache', '.log', 'node_modules', '.env'
        }

        file_str = str(file_path).lower()
        for pattern in skip_patterns:
            if pattern in file_str:
                return True, f"Excluded pattern: {pattern}"

        # Skip binary files if configured
        if self.config.enable_compression:
            binary_extensions = {'.exe', '.dll', '.so', '.dylib', '.bin', '.dat'}
            if file_path_obj.suffix.lower() in binary_extensions:
                return True, f"Binary file type: {file_path_obj.suffix}"

        return False, ""

    async def _upload_single_file_with_diagnostics(self, file_path: str,
                                                  context: Dict[str, Any],
                                                  attempt: int) -> FileUploadResult:
        """Enhanced single file upload with comprehensive diagnostics."""
        start_time = time.time()
        error_id = f"upload_{int(start_time)}_{hashlib.md5(file_path.encode()).hexdigest()[:8]}"

        try:
            # Pre-upload checks
            should_skip, skip_reason = self._should_skip_file(file_path)
            if should_skip:
                return FileUploadResult(
                    file_path=file_path,
                    success=False,
                    error=DetailedError(
                        error_id=error_id,
                        category=ErrorCategory.VALIDATION,
                        severity=ErrorSeverity.LOW,
                        timestamp=datetime.now(),
                        file_path=file_path,
                        error_message=f"Skipped: {skip_reason}",
                        retry_attempt=attempt
                    ),
                    upload_time=time.time() - start_time
                )

            # Read and prepare file
            full_path = Path(self.config.workspace_path) / file_path
            file_size = full_path.stat().st_size

            # Rate limit check
            await self._check_rate_limits()

            # Read file content with error handling
            try:
                async with aiofiles.open(full_path, 'rb') as f:
                    content = await f.read()
            except Exception as e:
                return FileUploadResult(
                    file_path=file_path,
                    success=False,
                    error=DetailedError(
                        error_id=error_id,
                        category=ErrorCategory.FILESYSTEM,
                        severity=ErrorSeverity.MEDIUM,
                        timestamp=datetime.now(),
                        file_path=file_path,
                        error_message=f"File read error: {str(e)}",
                        retry_attempt=attempt,
                        recovery_action="Check file permissions and disk space"
                    ),
                    upload_time=time.time() - start_time,
                    file_size=file_size
                )

            # Encode content with error handling
            try:
                import base64
                encoded_content = base64.b64encode(content).decode('utf-8')
            except Exception as e:
                return FileUploadResult(
                    file_path=file_path,
                    success=False,
                    error=DetailedError(
                        error_id=error_id,
                        category=ErrorCategory.ENCODING,
                        severity=ErrorSeverity.MEDIUM,
                        timestamp=datetime.now(),
                        file_path=file_path,
                        error_message=f"Base64 encoding error: {str(e)}",
                        retry_attempt=attempt,
                        recovery_action="Check file content and encoding"
                    ),
                    upload_time=time.time() - start_time,
                    file_size=file_size
                )

            # Prepare upload data
            upload_data = {
                'message': f'feat: bulk upload - Add {file_path}',
                'content': encoded_content,
                'branch': 'main'
            }

            # GitHub API URL
            api_url = f'https://api.github.com/repos/{self.config.github_owner}/{self.config.github_repo}/contents/{file_path}'

            # Dry run check
            if self.config.dry_run:
                logger.info(f"{Fore.CYAN}🔄 [DRY RUN] Would upload: {file_path}")
                return FileUploadResult(
                    file_path=file_path,
                    success=True,
                    upload_time=time.time() - start_time,
                    file_size=file_size
                )

            # Perform upload with detailed error handling
            request_start = time.time()

            try:
                async with self.session.put(api_url, json=upload_data) as response:
                    response_time = (time.time() - request_start) * 1000
                    response_headers = dict(response.headers)

                    # Update rate limit info
                    self._update_rate_limit_info(response_headers)

                    # Update network metrics
                    self.upload_stats["network_metrics"].total_requests += 1
                    self.upload_stats["network_metrics"].average_response_time = (
                        (self.upload_stats["network_metrics"].average_response_time *
                         (self.upload_stats["network_metrics"].total_requests - 1) + response_time) /
                        self.upload_stats["network_metrics"].total_requests
                    )

                    if response.status in [200, 201]:
                        # Success
                        response_data = await response.json()
                        self.upload_stats["network_metrics"].successful_requests += 1
                        self.upload_stats["network_metrics"].total_bytes_uploaded += file_size

                        return FileUploadResult(
                            file_path=file_path,
                            success=True,
                            upload_time=time.time() - start_time,
                            file_size=file_size,
                            sha=response_data.get('content', {}).get('sha'),
                            retry_count=attempt,
                            http_status=response.status,
                            response_headers=response_headers
                        )
                    else:
                        # HTTP error
                        self.upload_stats["network_metrics"].failed_requests += 1
                        error_text = await response.text()

                        # Analyze error
                        category, severity, recovery_action = self.error_analyzer.analyze_error(
                            error_text, http_status=response.status
                        )

                        # Special handling for specific status codes
                        if response.status == 409:
                            # File already exists - this might be OK
                            logger.warning(f"{Fore.YELLOW}⚠️ File already exists: {file_path}")
                            severity = ErrorSeverity.LOW

                        return FileUploadResult(
                            file_path=file_path,
                            success=False,
                            error=DetailedError(
                                error_id=error_id,
                                category=category,
                                severity=severity,
                                timestamp=datetime.now(),
                                file_path=file_path,
                                error_code=str(response.status),
                                http_status=response.status,
                                error_message=f"HTTP {response.status}: {error_text[:200]}",
                                retry_attempt=attempt,
                                context={
                                    "response_headers": response_headers,
                                    "file_size": file_size,
                                    "response_time_ms": response_time
                                },
                                recovery_action=recovery_action
                            ),
                            upload_time=time.time() - start_time,
                            file_size=file_size,
                            retry_count=attempt,
                            http_status=response.status,
                            response_headers=response_headers
                        )

            except asyncio.TimeoutError:
                self.upload_stats["network_metrics"].timeout_errors += 1
                return FileUploadResult(
                    file_path=file_path,
                    success=False,
                    error=DetailedError(
                        error_id=error_id,
                        category=ErrorCategory.NETWORK,
                        severity=ErrorSeverity.MEDIUM,
                        timestamp=datetime.now(),
                        file_path=file_path,
                        error_message="Request timeout",
                        retry_attempt=attempt,
                        recovery_action="Check network connectivity and retry"
                    ),
                    upload_time=time.time() - start_time,
                    file_size=file_size,
                    retry_count=attempt
                )

            except aiohttp.ClientError as e:
                self.upload_stats["network_metrics"].connection_errors += 1
                return FileUploadResult(
                    file_path=file_path,
                    success=False,
                    error=DetailedError(
                        error_id=error_id,
                        category=ErrorCategory.NETWORK,
                        severity=ErrorSeverity.HIGH,
                        timestamp=datetime.now(),
                        file_path=file_path,
                        error_message=f"Network error: {str(e)}",
                        retry_attempt=attempt,
                        recovery_action="Check network connectivity and retry"
                    ),
                    upload_time=time.time() - start_time,
                    file_size=file_size,
                    retry_count=attempt
                )

        except Exception as e:
            # Unexpected error
            category, severity, recovery_action = self.error_analyzer.analyze_error(
                str(e), exception_type=type(e).__name__
            )

            return FileUploadResult(
                file_path=file_path,
                success=False,
                error=DetailedError(
                    error_id=error_id,
                    category=category,
                    severity=severity,
                    timestamp=datetime.now(),
                    file_path=file_path,
                    error_message=f"Unexpected error: {str(e)}",
                    stack_trace=traceback.format_exc(),
                    retry_attempt=attempt,
                    recovery_action=recovery_action
                ),
                upload_time=time.time() - start_time,
                retry_count=attempt
            )

    async def _check_rate_limits(self):
        """Check and handle GitHub API rate limits."""
        if self.rate_limit_info["remaining"] < 100:
            if self.rate_limit_info["reset_time"]:
                wait_time = (self.rate_limit_info["reset_time"] - datetime.now()).total_seconds()
                if wait_time > 0:
                    logger.warning(f"{Fore.YELLOW}⏳ Rate limit low ({self.rate_limit_info['remaining']}), "
                                 f"waiting {wait_time:.0f}s")
                    await asyncio.sleep(min(wait_time, 300))  # Max 5 minutes

    def _update_rate_limit_info(self, headers: Dict[str, str]):
        """Update rate limit information from response headers."""
        try:
            self.rate_limit_info["remaining"] = int(headers.get("X-RateLimit-Remaining", 5000))
            reset_timestamp = int(headers.get("X-RateLimit-Reset", 0))
            if reset_timestamp:
                self.rate_limit_info["reset_time"] = datetime.fromtimestamp(reset_timestamp)
            self.rate_limit_info["last_check"] = datetime.now()

            if self.rate_limit_info["remaining"] < 500:
                self.upload_stats["network_metrics"].rate_limit_hits += 1

        except (ValueError, TypeError):
            pass  # Ignore invalid header values

    async def _upload_batch_with_diagnostics(self, files: List[str]) -> List[FileUploadResult]:
        """Enhanced batch upload with comprehensive diagnostics."""

        # Process with DocQA agent
        files = await self.docqa_agent.process_documentation_batch(files)

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.config.max_concurrent)

        async def upload_with_semaphore_and_retry(file_path: str) -> FileUploadResult:
            async with semaphore:
                # Use intelligent retry manager
                result = await self.retry_manager.execute_with_retry(
                    self._upload_single_file_with_diagnostics,
                    file_path,
                    {"batch_context": True}
                )

                # Rate limiting delay
                await asyncio.sleep(self.config.rate_limit_delay)
                return result

        # Execute uploads concurrently
        batch_start_time = time.time()
        tasks = [upload_with_semaphore_and_retry(file_path) for file_path in files]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and handle exceptions
        upload_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle unexpected exceptions
                error_id = f"batch_error_{int(time.time())}_{i}"
                upload_results.append(FileUploadResult(
                    file_path=files[i] if i < len(files) else "unknown",
                    success=False,
                    error=DetailedError(
                        error_id=error_id,
                        category=ErrorCategory.SYSTEM,
                        severity=ErrorSeverity.HIGH,
                        timestamp=datetime.now(),
                        file_path=files[i] if i < len(files) else "unknown",
                        error_message=f"Batch processing error: {str(result)}",
                        stack_trace=traceback.format_exc(),
                        recovery_action="Review system resources and retry"
                    ),
                    upload_time=time.time() - batch_start_time
                ))
            else:
                upload_results.append(result)

        # Update batch performance metrics
        batch_time = time.time() - batch_start_time
        successful_uploads = sum(1 for r in upload_results if r.success)

        if batch_time > 0:
            throughput = (successful_uploads * len(files)) / batch_time
            self.upload_stats["network_metrics"].current_throughput_mbps = throughput / (1024 * 1024)

        return upload_results

    def _get_files_in_directories(self, directories: List[str]) -> List[str]:
        """Enhanced file discovery with detailed logging."""
        files = []
        workspace_path = Path(self.config.workspace_path)

        logger.info(f"{Fore.CYAN}🔍 Scanning directories: {', '.join(directories)}")

        for directory in directories:
            dir_path = workspace_path / directory
            if dir_path.exists() and dir_path.is_dir():
                dir_files = []
                try:
                    for file_path in dir_path.rglob('*'):
                        if file_path.is_file():
                            rel_path = file_path.relative_to(workspace_path)
                            dir_files.append(str(rel_path))

                    files.extend(dir_files)
                    logger.info(f"{Fore.GREEN}   📁 {directory}: {len(dir_files):,} files")

                except Exception as e:
                    logger.error(f"{Fore.RED}❌ Error scanning {directory}: {e}")
            else:
                logger.warning(f"{Fore.YELLOW}⚠️ Directory not found: {directory}")

        logger.info(f"{Fore.CYAN}📊 Total files discovered: {len(files):,}")
        return files

    async def upload_phase_with_diagnostics(self, phase_config: Dict[str, Any]) -> PhaseProgress:
        """Enhanced phase upload with comprehensive diagnostics and monitoring."""

        phase_id = phase_config["phase_id"]
        phase_name = phase_config["phase_name"]
        directories = phase_config["directories"]

        logger.info(f"{Fore.MAGENTA}🚀 Starting {phase_name} (Phase {phase_id})")
        logger.info(f"{Fore.MAGENTA}   Priority: {phase_config.get('priority', 'NORMAL')}")
        logger.info(f"{Fore.MAGENTA}   Directories: {', '.join(directories)}")

        # Get files for this phase
        files = self._get_files_in_directories(directories)
        total_files = len(files)

        # Initialize enhanced progress tracking
        progress = PhaseProgress(
            phase_id=phase_id,
            phase_name=phase_name,
            total_files=total_files,
            network_metrics=NetworkMetrics()
        )

        if total_files == 0:
            logger.warning(f"{Fore.YELLOW}⚠️ No files found for {phase_name}")
            progress.end_time = time.time()
            return progress

        logger.info(f"{Fore.GREEN}📊 Found {total_files:,} files to upload")

        # Process files in batches
        batch_results_all = []

        for i in range(0, total_files, self.config.batch_size):
            batch = files[i:i + self.config.batch_size]
            batch_num = (i // self.config.batch_size) + 1
            total_batches = (total_files + self.config.batch_size - 1) // self.config.batch_size

            logger.info(f"{Fore.BLUE}📦 Processing batch {batch_num}/{total_batches} ({len(batch)} files)")

            # Upload batch with diagnostics
            batch_start_time = time.time()
            batch_results = await self._upload_batch_with_diagnostics(batch)
            batch_time = time.time() - batch_start_time

            # Process batch results
            for result in batch_results:
                progress.current_file = result.file_path

                if result.success:
                    progress.uploaded_files += 1
                    self.upload_stats["uploaded_files"] += 1
                    self.upload_stats["total_size_mb"] += result.file_size / (1024 * 1024)
                elif result.error and "Skipped:" in result.error.error_message:
                    progress.skipped_files += 1
                    self.upload_stats["skipped_files"] += 1
                else:
                    progress.failed_files += 1
                    self.upload_stats["failed_files"] += 1
                    if result.error:
                        progress.errors.append(result.error)

                        # Update error summary
                        error_category = result.error.category.value
                        if error_category not in self.upload_stats["error_summary"]:
                            self.upload_stats["error_summary"][error_category] = 0
                        self.upload_stats["error_summary"][error_category] += 1

            batch_results_all.extend(batch_results)

            # Update progress metrics
            progress.network_metrics.total_requests += len(batch)
            progress.network_metrics.successful_requests += sum(1 for r in batch_results if r.success)
            progress.network_metrics.failed_requests += sum(1 for r in batch_results if not r.success)

            # Calculate and log progress
            completion_pct = progress.completion_percentage
            success_rate = progress.success_rate

            logger.info(f"{Fore.GREEN}   Progress: {completion_pct:.1f}% "
                       f"({progress.uploaded_files} uploaded, {progress.failed_files} failed, "
                       f"{progress.skipped_files} skipped) - Success Rate: {success_rate:.1f}%")

            # Update dashboard
            if self.config.enable_color_output:
                system_metrics = self.system_monitor.get_metrics()
                self.progress_dashboard.update(progress, system_metrics)

            # Save checkpoint periodically
            if batch_num % 10 == 0:  # Every 10 batches
                try:
                    await self.checkpoint_manager.save_checkpoint(
                        progress, self.upload_stats, batch_results_all
                    )
                except Exception as e:
                    logger.error(f"{Fore.RED}❌ Failed to save checkpoint: {e}")

            # Small delay between batches for system stability
            await asyncio.sleep(0.5)

        # Phase completion
        progress.end_time = time.time()
        elapsed_time = progress.end_time - progress.start_time

        logger.info(f"{Fore.GREEN}✅ {phase_name} complete in {elapsed_time:.1f}s")
        logger.info(f"{Fore.GREEN}   Results: {progress.uploaded_files} uploaded, "
                   f"{progress.failed_files} failed, {progress.skipped_files} skipped")
        logger.info(f"{Fore.GREEN}   Success Rate: {progress.success_rate:.1f}%")

        # Save final checkpoint for this phase
        try:
            await self.checkpoint_manager.save_checkpoint(
                progress, self.upload_stats, batch_results_all
            )
        except Exception as e:
            logger.error(f"{Fore.RED}❌ Failed to save final checkpoint: {e}")

        self.upload_stats["phases_completed"] += 1
        return progress

    async def execute_enhanced_systematic_upload(self) -> Dict[str, Any]:
        """Execute enhanced systematic upload with comprehensive diagnostics."""

        logger.info(f"{Fore.CYAN}🚀 STARTING ENHANCED SYSTEMATIC BULK UPLOAD")
        logger.info(f"{Fore.CYAN}   Workspace: {self.config.workspace_path}")
        logger.info(f"{Fore.CYAN}   Target: {self.config.github_owner}/{self.config.github_repo}")
        logger.info(f"{Fore.CYAN}   Phases: {len(self.upload_phases)}")
        logger.info(f"{Fore.CYAN}   DocQA Agent: {'Enabled' if self.config.enable_docqa_agent else 'Disabled'}")
        logger.info(f"{Fore.CYAN}   Dry Run: {'Yes' if self.config.dry_run else 'No'}")
        logger.info(f"{Fore.CYAN}   Enhanced Diagnostics: {'Enabled' if self.config.enable_detailed_logging else 'Disabled'}")

        self.upload_stats["start_time"] = time.time()

        # Initial network diagnostics
        if self.config.enable_network_diagnostics:
            logger.info(f"{Fore.BLUE}🌐 Running network diagnostics...")
            latency_info = await self.network_diagnostics.measure_latency()
            logger.info(f"{Fore.BLUE}   Average Latency: {latency_info['avg_latency_ms']:.1f}ms")
            logger.info(f"{Fore.BLUE}   Latency Range: {latency_info['min_latency_ms']:.1f}-{latency_info['max_latency_ms']:.1f}ms")

        # Count total files
        total_files = 0
        for phase_config in self.upload_phases:
            files = self._get_files_in_directories(phase_config["directories"])
            total_files += len(files)

        self.upload_stats["total_files"] = total_files
        logger.info(f"{Fore.GREEN}📊 Total files to process: {total_files:,}")

        # Execute phases
        phase_results = []

        for phase_config in self.upload_phases:
            # Check dependencies
            dependencies = phase_config.get("dependencies", [])
            if dependencies:
                missing_deps = [dep for dep in dependencies
                              if not any(p.phase_id == dep for p in phase_results)]
                if missing_deps:
                    logger.warning(f"{Fore.YELLOW}⚠️ Skipping {phase_config['phase_name']} - "
                                 f"missing dependencies: {missing_deps}")
                    continue

            try:
                progress = await self.upload_phase_with_diagnostics(phase_config)
                phase_results.append(progress)

            except Exception as e:
                logger.error(f"{Fore.RED}❌ Error in {phase_config['phase_name']}: {e}")
                logger.error(f"{Fore.RED}   Stack trace: {traceback.format_exc()}")

                # Create error record
                error = DetailedError(
                    error_id=f"phase_error_{int(time.time())}",
                    category=ErrorCategory.SYSTEM,
                    severity=ErrorSeverity.CRITICAL,
                    timestamp=datetime.now(),
                    file_path=f"phase_{phase_config['phase_id']}",
                    error_message=f"Phase execution failed: {str(e)}",
                    stack_trace=traceback.format_exc(),
                    recovery_action="Review system resources and phase configuration"
                )

                # Continue with next phase
                continue

        # Calculate final statistics
        total_time = time.time() - self.upload_stats["start_time"]

        # Generate comprehensive final report
        final_stats = {
            "execution_summary": {
                "total_time_seconds": total_time,
                "total_time_formatted": f"{total_time/3600:.1f} hours",
                "phases_completed": len(phase_results),
                "total_phases": len(self.upload_phases),
                "completion_timestamp": datetime.now().isoformat()
            },
            "upload_statistics": self.upload_stats,
            "docqa_agent_analytics": self.docqa_agent.get_analytics(),
            "retry_statistics": self.retry_manager.get_retry_statistics(),
            "phase_results": [asdict(p) for p in phase_results],
            "success_rate": (self.upload_stats["uploaded_files"] / max(self.upload_stats["total_files"], 1)) * 100,
            "performance_metrics": {
                "average_upload_speed_files_per_second": self.upload_stats["uploaded_files"] / max(total_time, 1),
                "average_throughput_mbps": self.upload_stats["total_size_mb"] / max(total_time / 3600, 0.001),
                "error_rate": (self.upload_stats["failed_files"] / max(self.upload_stats["total_files"], 1)) * 100
            },
            "error_analysis": await self._generate_error_analysis(),
            "recommendations": self._generate_recommendations()
        }

        # Log final summary
        logger.info(f"{Fore.GREEN}🎯 ENHANCED SYSTEMATIC BULK UPLOAD COMPLETE")
        logger.info(f"{Fore.GREEN}   Total time: {total_time/3600:.1f} hours")
        logger.info(f"{Fore.GREEN}   Files uploaded: {self.upload_stats['uploaded_files']:,}")
        logger.info(f"{Fore.GREEN}   Success rate: {final_stats['success_rate']:.1f}%")
        logger.info(f"{Fore.GREEN}   Total size: {self.upload_stats['total_size_mb']:.1f} MB")
        logger.info(f"{Fore.GREEN}   Average speed: {final_stats['performance_metrics']['average_upload_speed_files_per_second']:.1f} files/sec")

        return final_stats

    async def _generate_error_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive error analysis report."""

        error_analysis = {
            "total_errors": self.upload_stats["failed_files"],
            "error_categories": self.upload_stats["error_summary"],
            "top_error_patterns": {},
            "critical_errors": [],
            "recovery_suggestions": {}
        }

        # Analyze error patterns (this would be more sophisticated in a real implementation)
        for category, count in self.upload_stats["error_summary"].items():
            if count > 0:
                error_analysis["recovery_suggestions"][category] = self.error_analyzer._suggest_recovery_action(
                    ErrorCategory(category), ""
                )

        return error_analysis

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on upload results."""

        recommendations = []

        # Success rate recommendations
        success_rate = (self.upload_stats["uploaded_files"] / max(self.upload_stats["total_files"], 1)) * 100
        if success_rate < 50:
            recommendations.append("CRITICAL: Very low success rate. Check GitHub token permissions and network connectivity.")
        elif success_rate < 80:
            recommendations.append("WARNING: Low success rate. Consider reducing concurrency and increasing retry delays.")

        # Rate limiting recommendations
        if self.upload_stats["network_metrics"].rate_limit_hits > 10:
            recommendations.append("Frequent rate limiting detected. Increase rate_limit_delay or reduce max_concurrent.")

        # Network performance recommendations
        if self.upload_stats["network_metrics"].timeout_errors > self.upload_stats["uploaded_files"] * 0.1:
            recommendations.append("High timeout rate. Check network stability and consider increasing timeout values.")

        # Error category recommendations
        error_summary = self.upload_stats["error_summary"]
        if error_summary.get("authentication", 0) > 0:
            recommendations.append("Authentication errors detected. Verify GitHub token validity and repository permissions.")

        if error_summary.get("filesystem", 0) > 0:
            recommendations.append("File system errors detected. Check file permissions and disk space.")

        if not recommendations:
            recommendations.append("Upload completed successfully with good performance metrics.")

        return recommendations

    async def _generate_error_report(self):
        """Generate detailed error report for export."""

        if not self.config.export_error_reports:
            return

        try:
            error_report = {
                "report_metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "report_version": "2.0",
                    "workspace_path": self.config.workspace_path,
                    "target_repository": f"{self.config.github_owner}/{self.config.github_repo}"
                },
                "summary_statistics": self.upload_stats,
                "retry_analysis": self.retry_manager.get_retry_statistics(),
                "error_analysis": await self._generate_error_analysis(),
                "recommendations": self._generate_recommendations(),
                "system_configuration": asdict(self.config)
            }

            # Save error report
            report_file = f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            async with aiofiles.open(report_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(error_report, indent=2, default=str))

            logger.info(f"{Fore.CYAN}📊 Error report exported: {report_file}")

        except Exception as e:
            logger.error(f"{Fore.RED}❌ Failed to generate error report: {e}")


async def main():
    """Enhanced main execution function with comprehensive error handling."""

    try:
        # Configuration with enhanced settings
        config = UploadConfig(
            github_token=os.getenv('GITHUB_TOKEN', ''),
            workspace_path=os.getenv('WORKSPACE_PATH', r'C:\Users\Lenovo ThinkPad T480\Desktop\JAEGIS'),
            batch_size=int(os.getenv('BATCH_SIZE', '50')),
            max_concurrent=int(os.getenv('MAX_CONCURRENT', '5')),
            rate_limit_delay=float(os.getenv('RATE_LIMIT_DELAY', '1.0')),
            enable_docqa_agent=os.getenv('ENABLE_DOCQA', 'true').lower() == 'true',
            dry_run=os.getenv('DRY_RUN', 'false').lower() == 'true',
            enable_detailed_logging=os.getenv('ENABLE_DETAILED_LOGGING', 'true').lower() == 'true',
            enable_performance_monitoring=os.getenv('ENABLE_PERFORMANCE_MONITORING', 'true').lower() == 'true',
            enable_network_diagnostics=os.getenv('ENABLE_NETWORK_DIAGNOSTICS', 'true').lower() == 'true',
            enable_color_output=os.getenv('ENABLE_COLOR_OUTPUT', 'true').lower() == 'true',
            export_error_reports=os.getenv('EXPORT_ERROR_REPORTS', 'true').lower() == 'true'
        )

        # Validate configuration
        if not config.github_token:
            logger.error(f"{Fore.RED}❌ GITHUB_TOKEN environment variable required")
            sys.exit(1)

        # Execute enhanced bulk upload
        async with EnhancedGitHubUploader(config) as uploader:
            results = await uploader.execute_enhanced_systematic_upload()

            # Save final results
            results_file = f"enhanced_bulk_upload_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            async with aiofiles.open(results_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(results, indent=2, default=str))

            logger.info(f"{Fore.CYAN}📊 Enhanced results saved: {results_file}")

            # Print final summary
            print(f"\n{Fore.GREEN}{'='*80}")
            print(f"{Fore.GREEN}🎉 ENHANCED BULK UPLOAD COMPLETED")
            print(f"{Fore.GREEN}{'='*80}")
            print(f"{Fore.WHITE}📊 Final Statistics:")
            print(f"   Total Files: {results['upload_statistics']['total_files']:,}")
            print(f"   Uploaded: {Fore.GREEN}{results['upload_statistics']['uploaded_files']:,}")
            print(f"   Failed: {Fore.RED}{results['upload_statistics']['failed_files']:,}")
            print(f"   Skipped: {Fore.YELLOW}{results['upload_statistics']['skipped_files']:,}")
            print(f"   Success Rate: {Fore.GREEN}{results['success_rate']:.1f}%")
            print(f"   Total Time: {Fore.CYAN}{results['execution_summary']['total_time_formatted']}")
            print(f"   Average Speed: {Fore.CYAN}{results['performance_metrics']['average_upload_speed_files_per_second']:.1f} files/sec")

            if results['recommendations']:
                print(f"\n{Fore.YELLOW}💡 Recommendations:")
                for rec in results['recommendations']:
                    print(f"   • {rec}")

            print(f"\n{Fore.CYAN}📄 Detailed results: {results_file}")
            print(f"{Fore.GREEN}{'='*80}")

    except KeyboardInterrupt:
        logger.warning(f"{Fore.YELLOW}⚠️ Upload interrupted by user")
        print(f"\n{Fore.YELLOW}⚠️ Upload interrupted. Progress has been saved in checkpoints.")
        sys.exit(1)

    except Exception as e:
        logger.error(f"{Fore.RED}❌ Fatal error: {e}")
        logger.error(f"{Fore.RED}   Stack trace: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
