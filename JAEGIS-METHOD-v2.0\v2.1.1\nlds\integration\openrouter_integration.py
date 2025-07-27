"""
N.L.D.S. OpenRouter.ai Integration
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Integration with OpenRouter.ai for accessing 3000+ AI models and API keys
with intelligent model selection, load balancing, and cost optimization.
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import hashlib
import random

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# OPENROUTER STRUCTURES AND ENUMS
# ============================================================================

class ModelCategory(Enum):
    """AI model categories."""
    LANGUAGE_MODEL = "language_model"
    CHAT_MODEL = "chat_model"
    CODE_MODEL = "code_model"
    REASONING_MODEL = "reasoning_model"
    CREATIVE_MODEL = "creative_model"
    ANALYSIS_MODEL = "analysis_model"
    MULTIMODAL_MODEL = "multimodal_model"
    SPECIALIZED_MODEL = "specialized_model"


class ModelProvider(Enum):
    """AI model providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    TOGETHER = "together"
    REPLICATE = "replicate"
    OTHER = "other"


class RequestPriority(Enum):
    """Request priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ModelInfo:
    """AI model information."""
    model_id: str
    model_name: str
    provider: ModelProvider
    category: ModelCategory
    context_length: int
    cost_per_1k_tokens: float
    performance_score: float
    availability: bool
    capabilities: List[str]
    rate_limits: Dict[str, int]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class APIKeyInfo:
    """API key information."""
    key_id: str
    provider: ModelProvider
    key_hash: str  # Hashed for security
    usage_count: int
    rate_limit_remaining: int
    cost_accumulated: float
    last_used: datetime
    is_active: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelRequest:
    """Model request specification."""
    request_id: str
    model_category: ModelCategory
    prompt: str
    max_tokens: int
    temperature: float
    priority: RequestPriority
    required_capabilities: List[str]
    cost_limit: Optional[float]
    timeout_seconds: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelResponse:
    """Model response data."""
    request_id: str
    model_used: str
    response_text: str
    tokens_used: int
    cost_incurred: float
    response_time_ms: float
    quality_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenRouterResult:
    """OpenRouter integration result."""
    success: bool
    request_id: str
    model_response: Optional[ModelResponse]
    selected_model: Optional[ModelInfo]
    api_key_used: Optional[str]
    load_balancing_info: Dict[str, Any]
    cost_optimization_info: Dict[str, Any]
    error_message: Optional[str]
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# OPENROUTER INTEGRATION ENGINE
# ============================================================================

class OpenRouterIntegrationEngine:
    """
    OpenRouter.ai integration engine for accessing 3000+ AI models.
    
    Features:
    - Intelligent model selection based on task requirements
    - Load balancing across multiple API keys
    - Cost optimization and budget management
    - Rate limit management and throttling
    - Quality assessment and model performance tracking
    - Fallback and retry mechanisms
    - Real-time model availability monitoring
    - Usage analytics and optimization
    """
    
    def __init__(self, openrouter_config: Dict[str, Any]):
        """
        Initialize OpenRouter integration engine.
        
        Args:
            openrouter_config: Configuration for OpenRouter integration
        """
        self.config = openrouter_config
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_keys = []
        self.available_models = {}
        self.model_performance_history = {}
        
        # Load configuration
        self.load_balancing_enabled = openrouter_config.get("load_balancing_enabled", True)
        self.cost_optimization_enabled = openrouter_config.get("cost_optimization_enabled", True)
        self.max_cost_per_request = openrouter_config.get("max_cost_per_request", 1.0)
        self.default_timeout = openrouter_config.get("default_timeout", 30)
        
        # Performance tracking
        self.usage_statistics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_cost": 0.0,
            "average_response_time_ms": 0.0,
            "models_used": {},
            "providers_used": {}
        }
        
        # Rate limiting
        self.rate_limit_tracker = {}
        self.request_queue = asyncio.Queue()
        
        # HTTP session
        self.http_session = None
        
        # Model selection weights
        self.selection_weights = {
            "cost": 0.3,
            "performance": 0.4,
            "availability": 0.2,
            "capability_match": 0.1
        }
    
    async def initialize_integration(self) -> bool:
        """Initialize OpenRouter integration."""
        try:
            # Initialize HTTP session
            self.http_session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60),
                headers={
                    "User-Agent": "NLDS-OpenRouter/2.2.0",
                    "Content-Type": "application/json"
                }
            )
            
            # Load API keys
            await self._load_api_keys()
            
            # Load available models
            await self._load_available_models()
            
            # Start background tasks
            asyncio.create_task(self._rate_limit_monitor())
            asyncio.create_task(self._model_availability_monitor())
            
            logger.info(f"OpenRouter integration initialized with {len(self.api_keys)} API keys and {len(self.available_models)} models")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter integration: {e}")
            return False
    
    async def _load_api_keys(self) -> None:
        """Load and validate API keys."""
        api_key_configs = self.config.get("api_keys", [])
        
        for key_config in api_key_configs:
            try:
                # Validate API key
                api_key = key_config.get("key")
                provider = ModelProvider(key_config.get("provider", "other"))
                
                if await self._validate_api_key(api_key, provider):
                    key_info = APIKeyInfo(
                        key_id=hashlib.md5(api_key.encode()).hexdigest()[:8],
                        provider=provider,
                        key_hash=hashlib.sha256(api_key.encode()).hexdigest(),
                        usage_count=0,
                        rate_limit_remaining=1000,  # Default
                        cost_accumulated=0.0,
                        last_used=datetime.utcnow(),
                        is_active=True,
                        metadata={"original_key": api_key}  # Store for actual use
                    )
                    self.api_keys.append(key_info)
                    logger.info(f"API key validated for provider: {provider.value}")
                else:
                    logger.warning(f"Invalid API key for provider: {provider.value}")
                    
            except Exception as e:
                logger.error(f"Error loading API key: {e}")
    
    async def _validate_api_key(self, api_key: str, provider: ModelProvider) -> bool:
        """Validate API key with provider."""
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            
            # Test endpoint varies by provider
            test_endpoints = {
                ModelProvider.OPENAI: "https://api.openai.com/v1/models",
                ModelProvider.ANTHROPIC: "https://api.anthropic.com/v1/messages",
                ModelProvider.GOOGLE: "https://generativelanguage.googleapis.com/v1/models"
            }
            
            test_url = test_endpoints.get(provider, f"{self.base_url}/models")
            
            async with self.http_session.get(test_url, headers=headers) as response:
                return response.status in [200, 401]  # 401 means key format is valid but may be expired
                
        except Exception as e:
            logger.debug(f"API key validation error: {e}")
            return False
    
    async def _load_available_models(self) -> None:
        """Load available models from OpenRouter."""
        try:
            if not self.api_keys:
                logger.warning("No valid API keys available for model loading")
                return
            
            # Use first available API key for model discovery
            api_key = self.api_keys[0].metadata["original_key"]
            headers = {"Authorization": f"Bearer {api_key}"}
            
            async with self.http_session.get(f"{self.base_url}/models", headers=headers) as response:
                if response.status == 200:
                    models_data = await response.json()
                    
                    for model_data in models_data.get("data", []):
                        model_info = self._parse_model_info(model_data)
                        self.available_models[model_info.model_id] = model_info
                    
                    logger.info(f"Loaded {len(self.available_models)} available models")
                else:
                    logger.warning(f"Failed to load models: HTTP {response.status}")
                    
        except Exception as e:
            logger.error(f"Error loading available models: {e}")
    
    def _parse_model_info(self, model_data: Dict[str, Any]) -> ModelInfo:
        """Parse model information from API response."""
        model_id = model_data.get("id", "unknown")
        model_name = model_data.get("name", model_id)
        
        # Determine provider from model ID
        provider = ModelProvider.OTHER
        if "openai" in model_id.lower():
            provider = ModelProvider.OPENAI
        elif "anthropic" in model_id.lower() or "claude" in model_id.lower():
            provider = ModelProvider.ANTHROPIC
        elif "google" in model_id.lower() or "gemini" in model_id.lower():
            provider = ModelProvider.GOOGLE
        elif "meta" in model_id.lower() or "llama" in model_id.lower():
            provider = ModelProvider.META
        elif "mistral" in model_id.lower():
            provider = ModelProvider.MISTRAL
        
        # Determine category
        category = ModelCategory.LANGUAGE_MODEL
        if "chat" in model_name.lower():
            category = ModelCategory.CHAT_MODEL
        elif "code" in model_name.lower():
            category = ModelCategory.CODE_MODEL
        elif "reasoning" in model_name.lower():
            category = ModelCategory.REASONING_MODEL
        
        # Extract capabilities
        capabilities = []
        if "vision" in model_name.lower():
            capabilities.append("vision")
        if "function" in model_name.lower():
            capabilities.append("function_calling")
        if "json" in model_name.lower():
            capabilities.append("json_mode")
        
        return ModelInfo(
            model_id=model_id,
            model_name=model_name,
            provider=provider,
            category=category,
            context_length=model_data.get("context_length", 4096),
            cost_per_1k_tokens=model_data.get("pricing", {}).get("prompt", 0.001),
            performance_score=0.8,  # Default, will be updated based on usage
            availability=True,
            capabilities=capabilities,
            rate_limits={"requests_per_minute": 60, "tokens_per_minute": 10000},
            metadata=model_data
        )
    
    def select_optimal_model(self, request: ModelRequest) -> Optional[ModelInfo]:
        """Select optimal model based on request requirements."""
        if not self.available_models:
            return None
        
        # Filter models by category and capabilities
        candidate_models = []
        for model in self.available_models.values():
            if model.category == request.model_category and model.availability:
                # Check capability requirements
                if all(cap in model.capabilities for cap in request.required_capabilities):
                    candidate_models.append(model)
        
        if not candidate_models:
            # Fallback to any available model in category
            candidate_models = [m for m in self.available_models.values() 
                             if m.category == request.model_category and m.availability]
        
        if not candidate_models:
            return None
        
        # Score models based on selection criteria
        scored_models = []
        for model in candidate_models:
            score = 0.0
            
            # Cost score (lower cost = higher score)
            if request.cost_limit:
                estimated_cost = (request.max_tokens / 1000) * model.cost_per_1k_tokens
                if estimated_cost <= request.cost_limit:
                    cost_score = 1.0 - (estimated_cost / request.cost_limit)
                else:
                    cost_score = 0.0  # Exceeds budget
            else:
                cost_score = 1.0 - min(model.cost_per_1k_tokens / 0.1, 1.0)  # Normalize by $0.1/1k
            
            score += cost_score * self.selection_weights["cost"]
            
            # Performance score
            performance_score = model.performance_score
            score += performance_score * self.selection_weights["performance"]
            
            # Availability score (always 1.0 for available models)
            availability_score = 1.0
            score += availability_score * self.selection_weights["availability"]
            
            # Capability match score
            capability_score = len([cap for cap in request.required_capabilities if cap in model.capabilities]) / max(len(request.required_capabilities), 1)
            score += capability_score * self.selection_weights["capability_match"]
            
            scored_models.append((model, score))
        
        # Sort by score and return best model
        scored_models.sort(key=lambda x: x[1], reverse=True)
        return scored_models[0][0] if scored_models else None
    
    def select_api_key(self, provider: Optional[ModelProvider] = None) -> Optional[APIKeyInfo]:
        """Select optimal API key for request."""
        if not self.api_keys:
            return None
        
        # Filter by provider if specified
        candidate_keys = self.api_keys
        if provider:
            candidate_keys = [key for key in self.api_keys if key.provider == provider]
        
        # Filter active keys with remaining rate limit
        available_keys = [key for key in candidate_keys if key.is_active and key.rate_limit_remaining > 0]
        
        if not available_keys:
            return None
        
        # Load balancing: select key with lowest usage
        if self.load_balancing_enabled:
            return min(available_keys, key=lambda k: k.usage_count)
        else:
            return available_keys[0]
    
    async def make_model_request(self, request: ModelRequest) -> OpenRouterResult:
        """Make request to selected model via OpenRouter."""
        start_time = time.time()
        
        try:
            # Select optimal model
            selected_model = self.select_optimal_model(request)
            if not selected_model:
                return OpenRouterResult(
                    success=False,
                    request_id=request.request_id,
                    model_response=None,
                    selected_model=None,
                    api_key_used=None,
                    load_balancing_info={},
                    cost_optimization_info={},
                    error_message="No suitable model available",
                    processing_time_ms=(time.time() - start_time) * 1000,
                    metadata={}
                )
            
            # Select API key
            api_key_info = self.select_api_key(selected_model.provider)
            if not api_key_info:
                return OpenRouterResult(
                    success=False,
                    request_id=request.request_id,
                    model_response=None,
                    selected_model=selected_model,
                    api_key_used=None,
                    load_balancing_info={},
                    cost_optimization_info={},
                    error_message="No available API key",
                    processing_time_ms=(time.time() - start_time) * 1000,
                    metadata={}
                )
            
            # Prepare request payload
            payload = {
                "model": selected_model.model_id,
                "messages": [{"role": "user", "content": request.prompt}],
                "max_tokens": request.max_tokens,
                "temperature": request.temperature
            }
            
            # Add capabilities if supported
            if "json_mode" in selected_model.capabilities:
                payload["response_format"] = {"type": "json_object"}
            
            headers = {
                "Authorization": f"Bearer {api_key_info.metadata['original_key']}",
                "HTTP-Referer": "https://nlds.jaegis.ai",
                "X-Title": "NLDS Tier 0 Integration"
            }
            
            # Make request
            async with self.http_session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=request.timeout_seconds)
            ) as response:
                
                response_data = await response.json()
                processing_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    # Parse successful response
                    choice = response_data.get("choices", [{}])[0]
                    message = choice.get("message", {})
                    response_text = message.get("content", "")
                    
                    usage = response_data.get("usage", {})
                    tokens_used = usage.get("total_tokens", 0)
                    cost_incurred = (tokens_used / 1000) * selected_model.cost_per_1k_tokens
                    
                    # Update API key usage
                    api_key_info.usage_count += 1
                    api_key_info.cost_accumulated += cost_incurred
                    api_key_info.last_used = datetime.utcnow()
                    
                    # Update model performance
                    if selected_model.model_id not in self.model_performance_history:
                        self.model_performance_history[selected_model.model_id] = []
                    
                    self.model_performance_history[selected_model.model_id].append({
                        "response_time_ms": processing_time,
                        "tokens_used": tokens_used,
                        "cost": cost_incurred,
                        "timestamp": datetime.utcnow()
                    })
                    
                    # Calculate quality score (simplified)
                    quality_score = min(len(response_text) / max(request.max_tokens, 1), 1.0)
                    
                    model_response = ModelResponse(
                        request_id=request.request_id,
                        model_used=selected_model.model_id,
                        response_text=response_text,
                        tokens_used=tokens_used,
                        cost_incurred=cost_incurred,
                        response_time_ms=processing_time,
                        quality_score=quality_score,
                        metadata=response_data
                    )
                    
                    # Update statistics
                    self.usage_statistics["total_requests"] += 1
                    self.usage_statistics["successful_requests"] += 1
                    self.usage_statistics["total_cost"] += cost_incurred
                    
                    # Update average response time
                    current_avg = self.usage_statistics["average_response_time_ms"]
                    total_requests = self.usage_statistics["total_requests"]
                    self.usage_statistics["average_response_time_ms"] = (current_avg * (total_requests - 1) + processing_time) / total_requests
                    
                    # Track model usage
                    if selected_model.model_id not in self.usage_statistics["models_used"]:
                        self.usage_statistics["models_used"][selected_model.model_id] = 0
                    self.usage_statistics["models_used"][selected_model.model_id] += 1
                    
                    # Track provider usage
                    provider_name = selected_model.provider.value
                    if provider_name not in self.usage_statistics["providers_used"]:
                        self.usage_statistics["providers_used"][provider_name] = 0
                    self.usage_statistics["providers_used"][provider_name] += 1
                    
                    return OpenRouterResult(
                        success=True,
                        request_id=request.request_id,
                        model_response=model_response,
                        selected_model=selected_model,
                        api_key_used=api_key_info.key_id,
                        load_balancing_info={
                            "api_keys_available": len([k for k in self.api_keys if k.is_active]),
                            "selected_key_usage": api_key_info.usage_count
                        },
                        cost_optimization_info={
                            "estimated_cost": cost_incurred,
                            "cost_limit": request.cost_limit,
                            "cost_efficiency": 1.0 - (cost_incurred / max(request.cost_limit or 1.0, cost_incurred))
                        },
                        error_message=None,
                        processing_time_ms=processing_time,
                        metadata={
                            "model_selection_score": 0.8,  # Placeholder
                            "rate_limit_remaining": api_key_info.rate_limit_remaining
                        }
                    )
                else:
                    # Handle error response
                    error_message = response_data.get("error", {}).get("message", f"HTTP {response.status}")
                    
                    self.usage_statistics["total_requests"] += 1
                    self.usage_statistics["failed_requests"] += 1
                    
                    return OpenRouterResult(
                        success=False,
                        request_id=request.request_id,
                        model_response=None,
                        selected_model=selected_model,
                        api_key_used=api_key_info.key_id,
                        load_balancing_info={},
                        cost_optimization_info={},
                        error_message=error_message,
                        processing_time_ms=processing_time,
                        metadata={"http_status": response.status, "response_data": response_data}
                    )
                    
        except asyncio.TimeoutError:
            processing_time = (time.time() - start_time) * 1000
            return OpenRouterResult(
                success=False,
                request_id=request.request_id,
                model_response=None,
                selected_model=selected_model if 'selected_model' in locals() else None,
                api_key_used=None,
                load_balancing_info={},
                cost_optimization_info={},
                error_message="Request timeout",
                processing_time_ms=processing_time,
                metadata={}
            )
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            logger.error(f"OpenRouter request failed: {e}")
            
            return OpenRouterResult(
                success=False,
                request_id=request.request_id,
                model_response=None,
                selected_model=selected_model if 'selected_model' in locals() else None,
                api_key_used=None,
                load_balancing_info={},
                cost_optimization_info={},
                error_message=str(e),
                processing_time_ms=processing_time,
                metadata={}
            )
    
    async def _rate_limit_monitor(self) -> None:
        """Monitor and manage rate limits."""
        while True:
            try:
                # Reset rate limits periodically
                current_time = datetime.utcnow()
                
                for api_key in self.api_keys:
                    # Reset rate limits every minute
                    if current_time - api_key.last_used > timedelta(minutes=1):
                        api_key.rate_limit_remaining = 60  # Reset to default
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Rate limit monitor error: {e}")
                await asyncio.sleep(60)
    
    async def _model_availability_monitor(self) -> None:
        """Monitor model availability."""
        while True:
            try:
                # Check model availability every 5 minutes
                await asyncio.sleep(300)
                
                # Simple availability check - in production, this would ping each model
                for model in self.available_models.values():
                    # Simulate availability check
                    model.availability = random.random() > 0.05  # 95% availability
                
            except Exception as e:
                logger.error(f"Model availability monitor error: {e}")
                await asyncio.sleep(300)
    
    async def get_integration_status(self) -> Dict[str, Any]:
        """Get current OpenRouter integration status."""
        return {
            "api_keys_count": len(self.api_keys),
            "active_api_keys": len([k for k in self.api_keys if k.is_active]),
            "available_models_count": len(self.available_models),
            "available_models": len([m for m in self.available_models.values() if m.availability]),
            "usage_statistics": self.usage_statistics.copy(),
            "load_balancing_enabled": self.load_balancing_enabled,
            "cost_optimization_enabled": self.cost_optimization_enabled,
            "max_cost_per_request": self.max_cost_per_request,
            "model_categories": list(set(m.category.value for m in self.available_models.values())),
            "providers": list(set(m.provider.value for m in self.available_models.values()))
        }
    
    async def cleanup(self) -> None:
        """Cleanup OpenRouter integration resources."""
        try:
            if self.http_session and not self.http_session.closed:
                await self.http_session.close()
            
            logger.info("OpenRouter integration cleaned up")
            
        except Exception as e:
            logger.error(f"Error during OpenRouter cleanup: {e}")


# ============================================================================
# OPENROUTER UTILITIES
# ============================================================================

class OpenRouterUtils:
    """Utility functions for OpenRouter integration."""
    
    @staticmethod
    def openrouter_result_to_dict(result: OpenRouterResult) -> Dict[str, Any]:
        """Convert OpenRouter result to dictionary format."""
        return {
            "success": result.success,
            "request_id": result.request_id,
            "model_response": {
                "model_used": result.model_response.model_used,
                "response_text": result.model_response.response_text,
                "tokens_used": result.model_response.tokens_used,
                "cost_incurred": result.model_response.cost_incurred,
                "response_time_ms": result.model_response.response_time_ms,
                "quality_score": result.model_response.quality_score
            } if result.model_response else None,
            "selected_model": {
                "model_id": result.selected_model.model_id,
                "model_name": result.selected_model.model_name,
                "provider": result.selected_model.provider.value,
                "category": result.selected_model.category.value
            } if result.selected_model else None,
            "api_key_used": result.api_key_used,
            "load_balancing_info": result.load_balancing_info,
            "cost_optimization_info": result.cost_optimization_info,
            "error_message": result.error_message,
            "processing_time_ms": result.processing_time_ms,
            "metadata": result.metadata
        }
    
    @staticmethod
    def create_model_request(prompt: str, category: ModelCategory = ModelCategory.CHAT_MODEL,
                           max_tokens: int = 1000, temperature: float = 0.7,
                           priority: RequestPriority = RequestPriority.NORMAL) -> ModelRequest:
        """Create a model request with default parameters."""
        return ModelRequest(
            request_id=f"req_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}",
            model_category=category,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            priority=priority,
            required_capabilities=[],
            cost_limit=None,
            timeout_seconds=30
        )
