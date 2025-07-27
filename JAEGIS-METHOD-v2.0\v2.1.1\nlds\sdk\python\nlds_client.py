"""
N.L.D.S. Python SDK
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Official Python client SDK for the N.L.D.S. API with comprehensive
features, error handling, and developer-friendly interface.
"""

import asyncio
import aiohttp
import requests
import json
import time
from typing import Dict, List, Optional, Any, Union, AsyncGenerator
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from datetime import datetime, timedelta
import websockets
import ssl
import certifi

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# SDK MODELS
# ============================================================================

class ProcessingMode(str, Enum):
    """Processing mode options."""
    STANDARD = "standard"
    ENHANCED = "enhanced"
    COMPREHENSIVE = "comprehensive"
    FAST = "fast"


class AnalysisType(str, Enum):
    """Analysis type options."""
    LOGICAL = "logical"
    EMOTIONAL = "emotional"
    CREATIVE = "creative"
    COMPREHENSIVE = "comprehensive"


@dataclass
class NLDSConfig:
    """N.L.D.S. client configuration."""
    api_key: str
    base_url: str = "https://api.nlds.jaegis.ai"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    verify_ssl: bool = True
    user_agent: str = "NLDS-Python-SDK/2.2.0"


@dataclass
class ProcessingRequest:
    """Processing request model."""
    input_text: str
    mode: ProcessingMode = ProcessingMode.STANDARD
    context: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    enable_amasiap: bool = True


@dataclass
class ProcessingResult:
    """Processing result model."""
    request_id: str
    success: bool
    original_input: str
    enhanced_input: str
    processing_time_ms: float
    confidence_score: float
    components_used: List[str]
    amasiap_result: Optional[Dict[str, Any]]
    jaegis_command: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]


@dataclass
class AnalysisRequest:
    """Analysis request model."""
    input_text: str
    analysis_types: List[AnalysisType] = field(default_factory=lambda: [AnalysisType.COMPREHENSIVE])
    depth_level: int = 3
    include_metadata: bool = True


@dataclass
class AnalysisResult:
    """Analysis result model."""
    request_id: str
    input_text: str
    logical_analysis: Dict[str, Any]
    emotional_analysis: Dict[str, Any]
    creative_analysis: Dict[str, Any]
    synthesis: Dict[str, Any]
    processing_time_ms: float
    timestamp: datetime


@dataclass
class APIError:
    """API error model."""
    code: int
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None
    request_id: Optional[str] = None


# ============================================================================
# EXCEPTIONS
# ============================================================================

class NLDSException(Exception):
    """Base exception for N.L.D.S. SDK."""
    
    def __init__(self, message: str, error_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class AuthenticationError(NLDSException):
    """Authentication failed."""
    pass


class RateLimitError(NLDSException):
    """Rate limit exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ValidationError(NLDSException):
    """Request validation failed."""
    pass


class ProcessingError(NLDSException):
    """Processing failed."""
    pass


class NetworkError(NLDSException):
    """Network error occurred."""
    pass


# ============================================================================
# SYNCHRONOUS CLIENT
# ============================================================================

class NLDSClient:
    """
    Synchronous N.L.D.S. API client.
    
    Features:
    - Complete API coverage
    - Automatic retries with exponential backoff
    - Rate limit handling
    - Comprehensive error handling
    - Request/response logging
    - Timeout management
    """
    
    def __init__(self, config: NLDSConfig):
        """
        Initialize N.L.D.S. client.
        
        Args:
            config: Client configuration
        """
        self.config = config
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": config.user_agent,
            "Accept": "application/json"
        })
        
        # Configure SSL verification
        if not config.verify_ssl:
            self.session.verify = False
        else:
            self.session.verify = certifi.where()
        
        # Set timeout
        self.session.timeout = config.timeout
    
    def process(self, request: ProcessingRequest) -> ProcessingResult:
        """
        Process natural language input.
        
        Args:
            request: Processing request
            
        Returns:
            Processing result
            
        Raises:
            NLDSException: If processing fails
        """
        try:
            response = self._make_request(
                "POST",
                "/process",
                data=asdict(request)
            )
            
            return ProcessingResult(**response)
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise ProcessingError(f"Processing failed: {str(e)}")
    
    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Perform detailed analysis.
        
        Args:
            request: Analysis request
            
        Returns:
            Analysis result
            
        Raises:
            NLDSException: If analysis fails
        """
        try:
            # Convert enum values to strings
            request_data = asdict(request)
            request_data["analysis_types"] = [t.value for t in request.analysis_types]
            
            response = self._make_request(
                "POST",
                "/analyze",
                data=request_data
            )
            
            # Parse timestamp
            response["timestamp"] = datetime.fromisoformat(response["timestamp"])
            
            return AnalysisResult(**response)
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise ProcessingError(f"Analysis failed: {str(e)}")
    
    def translate(self, input_text: str, target_mode: Optional[int] = None, 
                 preferred_squad: Optional[str] = None, priority: str = "normal") -> Dict[str, Any]:
        """
        Translate to JAEGIS commands.
        
        Args:
            input_text: Input text to translate
            target_mode: Preferred JAEGIS mode
            preferred_squad: Preferred squad
            priority: Command priority
            
        Returns:
            Translation result
            
        Raises:
            NLDSException: If translation fails
        """
        try:
            request_data = {
                "input_text": input_text,
                "target_mode": target_mode,
                "preferred_squad": preferred_squad,
                "priority": priority
            }
            
            return self._make_request(
                "POST",
                "/translate",
                data=request_data
            )
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise ProcessingError(f"Translation failed: {str(e)}")
    
    def submit_command(self, command: Dict[str, Any], priority: str = "normal", 
                      timeout_seconds: int = 300) -> Dict[str, Any]:
        """
        Submit command to JAEGIS.
        
        Args:
            command: JAEGIS command
            priority: Command priority
            timeout_seconds: Command timeout
            
        Returns:
            Submission result
            
        Raises:
            NLDSException: If submission fails
        """
        try:
            request_data = {
                "command": command,
                "priority": priority,
                "timeout_seconds": timeout_seconds
            }
            
            return self._make_request(
                "POST",
                "/jaegis/submit",
                data=request_data
            )
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise ProcessingError(f"Command submission failed: {str(e)}")
    
    def get_command_status(self, command_id: str) -> Dict[str, Any]:
        """
        Get command status.
        
        Args:
            command_id: Command ID
            
        Returns:
            Command status
            
        Raises:
            NLDSException: If status check fails
        """
        try:
            return self._make_request(
                "GET",
                f"/jaegis/status/{command_id}"
            )
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise ProcessingError(f"Status check failed: {str(e)}")
    
    def get_health(self) -> Dict[str, Any]:
        """
        Get system health.
        
        Returns:
            Health status
            
        Raises:
            NLDSException: If health check fails
        """
        try:
            return self._make_request("GET", "/health")
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise NetworkError(f"Health check failed: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get system status.
        
        Returns:
            System status
            
        Raises:
            NLDSException: If status check fails
        """
        try:
            return self._make_request("GET", "/status")
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise NetworkError(f"Status check failed: {str(e)}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get system metrics.
        
        Returns:
            System metrics
            
        Raises:
            NLDSException: If metrics retrieval fails
        """
        try:
            return self._make_request("GET", "/metrics")
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise NetworkError(f"Metrics retrieval failed: {str(e)}")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make HTTP request with retries and error handling.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            
        Returns:
            Response data
            
        Raises:
            NLDSException: If request fails
        """
        url = f"{self.config.base_url}{endpoint}"
        
        for attempt in range(self.config.max_retries + 1):
            try:
                # Make request
                if method.upper() == "GET":
                    response = self.session.get(url, params=params)
                elif method.upper() == "POST":
                    response = self.session.post(url, json=data, params=params)
                elif method.upper() == "PUT":
                    response = self.session.put(url, json=data, params=params)
                elif method.upper() == "DELETE":
                    response = self.session.delete(url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Handle response
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise AuthenticationError("Invalid API key or authentication failed")
                elif response.status_code == 403:
                    raise AuthenticationError("Insufficient permissions")
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
                elif response.status_code == 400:
                    error_data = response.json() if response.content else {}
                    raise ValidationError(
                        error_data.get("error", {}).get("message", "Validation failed"),
                        error_code=400,
                        details=error_data
                    )
                elif response.status_code >= 500:
                    if attempt < self.config.max_retries:
                        # Retry on server errors
                        time.sleep(self.config.retry_delay * (2 ** attempt))
                        continue
                    else:
                        error_data = response.json() if response.content else {}
                        raise NetworkError(
                            f"Server error: {response.status_code}",
                            error_code=response.status_code,
                            details=error_data
                        )
                else:
                    error_data = response.json() if response.content else {}
                    raise NLDSException(
                        f"Request failed: {response.status_code}",
                        error_code=response.status_code,
                        details=error_data
                    )
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.config.max_retries:
                    time.sleep(self.config.retry_delay * (2 ** attempt))
                    continue
                else:
                    raise NetworkError(f"Network error: {str(e)}")
        
        raise NetworkError("Max retries exceeded")
    
    def close(self):
        """Close the client session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# ============================================================================
# ASYNCHRONOUS CLIENT
# ============================================================================

class AsyncNLDSClient:
    """
    Asynchronous N.L.D.S. API client.
    
    Features:
    - Async/await support
    - WebSocket real-time communication
    - Streaming responses
    - Concurrent request handling
    - Connection pooling
    """
    
    def __init__(self, config: NLDSConfig):
        """
        Initialize async N.L.D.S. client.
        
        Args:
            config: Client configuration
        """
        self.config = config
        self.session = None
        self.websocket = None
        
        # SSL context
        self.ssl_context = ssl.create_default_context(cafile=certifi.where()) if config.verify_ssl else None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def connect(self):
        """Initialize async session."""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            headers = {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
                "User-Agent": self.config.user_agent,
                "Accept": "application/json"
            }
            
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers=headers,
                connector=connector
            )
    
    async def process(self, request: ProcessingRequest) -> ProcessingResult:
        """
        Process natural language input asynchronously.
        
        Args:
            request: Processing request
            
        Returns:
            Processing result
            
        Raises:
            NLDSException: If processing fails
        """
        try:
            response = await self._make_request(
                "POST",
                "/process",
                data=asdict(request)
            )
            
            return ProcessingResult(**response)
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise ProcessingError(f"Processing failed: {str(e)}")
    
    async def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Perform detailed analysis asynchronously.
        
        Args:
            request: Analysis request
            
        Returns:
            Analysis result
            
        Raises:
            NLDSException: If analysis fails
        """
        try:
            # Convert enum values to strings
            request_data = asdict(request)
            request_data["analysis_types"] = [t.value for t in request.analysis_types]
            
            response = await self._make_request(
                "POST",
                "/analyze",
                data=request_data
            )
            
            # Parse timestamp
            response["timestamp"] = datetime.fromisoformat(response["timestamp"])
            
            return AnalysisResult(**response)
            
        except Exception as e:
            if isinstance(e, NLDSException):
                raise
            raise ProcessingError(f"Analysis failed: {str(e)}")
    
    async def connect_websocket(self) -> None:
        """Connect to WebSocket for real-time communication."""
        try:
            ws_url = self.config.base_url.replace("http", "ws") + "/ws"
            headers = {"Authorization": f"Bearer {self.config.api_key}"}
            
            self.websocket = await websockets.connect(
                ws_url,
                ssl=self.ssl_context,
                extra_headers=headers
            )
            
        except Exception as e:
            raise NetworkError(f"WebSocket connection failed: {str(e)}")
    
    async def listen_for_updates(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Listen for real-time updates via WebSocket.
        
        Yields:
            Real-time messages
            
        Raises:
            NetworkError: If WebSocket connection fails
        """
        if not self.websocket:
            await self.connect_websocket()
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    yield data
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received: {message}")
                    
        except websockets.exceptions.ConnectionClosed:
            raise NetworkError("WebSocket connection closed")
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make async HTTP request with retries and error handling.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            
        Returns:
            Response data
            
        Raises:
            NLDSException: If request fails
        """
        if not self.session:
            await self.connect()
        
        url = f"{self.config.base_url}{endpoint}"
        
        for attempt in range(self.config.max_retries + 1):
            try:
                # Make request
                if method.upper() == "GET":
                    async with self.session.get(url, params=params) as response:
                        return await self._handle_response(response)
                elif method.upper() == "POST":
                    async with self.session.post(url, json=data, params=params) as response:
                        return await self._handle_response(response)
                elif method.upper() == "PUT":
                    async with self.session.put(url, json=data, params=params) as response:
                        return await self._handle_response(response)
                elif method.upper() == "DELETE":
                    async with self.session.delete(url, params=params) as response:
                        return await self._handle_response(response)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                    
            except aiohttp.ClientError as e:
                if attempt < self.config.max_retries:
                    await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
                    continue
                else:
                    raise NetworkError(f"Network error: {str(e)}")
        
        raise NetworkError("Max retries exceeded")
    
    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle HTTP response."""
        if response.status == 200:
            return await response.json()
        elif response.status == 401:
            raise AuthenticationError("Invalid API key or authentication failed")
        elif response.status == 403:
            raise AuthenticationError("Insufficient permissions")
        elif response.status == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        elif response.status == 400:
            error_data = await response.json() if response.content_length else {}
            raise ValidationError(
                error_data.get("error", {}).get("message", "Validation failed"),
                error_code=400,
                details=error_data
            )
        else:
            error_data = await response.json() if response.content_length else {}
            raise NLDSException(
                f"Request failed: {response.status}",
                error_code=response.status,
                details=error_data
            )
    
    async def close(self):
        """Close async client."""
        if self.websocket:
            await self.websocket.close()
        
        if self.session:
            await self.session.close()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_client(api_key: str, base_url: str = "https://api.nlds.jaegis.ai", **kwargs) -> NLDSClient:
    """
    Create N.L.D.S. client with default configuration.
    
    Args:
        api_key: API key
        base_url: Base URL
        **kwargs: Additional configuration options
        
    Returns:
        N.L.D.S. client
    """
    config = NLDSConfig(api_key=api_key, base_url=base_url, **kwargs)
    return NLDSClient(config)


def create_async_client(api_key: str, base_url: str = "https://api.nlds.jaegis.ai", **kwargs) -> AsyncNLDSClient:
    """
    Create async N.L.D.S. client with default configuration.
    
    Args:
        api_key: API key
        base_url: Base URL
        **kwargs: Additional configuration options
        
    Returns:
        Async N.L.D.S. client
    """
    config = NLDSConfig(api_key=api_key, base_url=base_url, **kwargs)
    return AsyncNLDSClient(config)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example usage
    import os
    
    # Get API key from environment
    api_key = os.getenv("NLDS_API_KEY", "your_api_key_here")
    
    # Synchronous example
    with create_client(api_key) as client:
        # Process input
        request = ProcessingRequest(
            input_text="Analyze the current market trends for renewable energy",
            mode=ProcessingMode.ENHANCED,
            enable_amasiap=True
        )
        
        result = client.process(request)
        print(f"Processing successful: {result.success}")
        print(f"Enhanced input: {result.enhanced_input}")
        print(f"Confidence: {result.confidence_score}")
    
    # Asynchronous example
    async def async_example():
        async with create_async_client(api_key) as client:
            # Process input
            request = ProcessingRequest(
                input_text="Create a strategic plan for digital transformation",
                mode=ProcessingMode.COMPREHENSIVE
            )
            
            result = await client.process(request)
            print(f"Async processing successful: {result.success}")
            
            # Listen for real-time updates
            try:
                async for update in client.listen_for_updates():
                    print(f"Real-time update: {update}")
                    break  # Just show one update
            except Exception as e:
                print(f"WebSocket error: {e}")
    
    # Run async example (uncomment to test)
    # asyncio.run(async_example())
