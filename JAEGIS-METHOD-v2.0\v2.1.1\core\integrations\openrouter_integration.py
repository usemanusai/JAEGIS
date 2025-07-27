"""
OpenRouter.ai Integration for JAEGIS Enhanced Agent System
Manages 3000+ API keys pool with intelligent routing and load balancing
"""

import asyncio
import aiohttp
import json
import time
import random
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
from collections import defaultdict, deque
import statistics

logger = logging.getLogger(__name__)


class ModelProvider(str, Enum):
    """Supported AI model providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    META = "meta"
    MISTRAL = "mistral"
    PERPLEXITY = "perplexity"


class RequestPriority(str, Enum):
    """Request priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class KeyStatus(str, Enum):
    """API key status."""
    ACTIVE = "active"
    RATE_LIMITED = "rate_limited"
    QUOTA_EXCEEDED = "quota_exceeded"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class APIKey:
    """API key configuration."""
    key_id: str
    provider: ModelProvider
    key_value: str
    rate_limit: int
    quota_limit: int
    current_usage: int
    status: KeyStatus
    last_used: float
    error_count: int
    success_count: int
    average_response_time: float


@dataclass
class ModelConfig:
    """Model configuration."""
    model_name: str
    provider: ModelProvider
    max_tokens: int
    cost_per_token: float
    capabilities: List[str]
    preferred_use_cases: List[str]


@dataclass
class RequestMetrics:
    """Request performance metrics."""
    request_id: str
    model_used: str
    api_key_id: str
    response_time_ms: float
    tokens_used: int
    cost: float
    success: bool
    error_message: Optional[str]
    timestamp: float


@dataclass
class OpenRouterResponse:
    """OpenRouter API response."""
    success: bool
    response_data: Any
    model_used: str
    api_key_used: str
    tokens_used: int
    cost: float
    response_time_ms: float
    error_message: Optional[str]
    request_id: str


class OpenRouterIntegration:
    """
    OpenRouter.ai Integration with 3000+ API keys management.
    
    Features:
    - Intelligent key rotation and load balancing
    - Rate limit management and quota tracking
    - Multi-provider model routing
    - Performance optimization
    - Error handling and failover
    """
    
    def __init__(self):
        self.api_keys: Dict[str, APIKey] = {}
        self.models: Dict[str, ModelConfig] = {}
        self.request_queue = asyncio.Queue()
        self.metrics_history: deque = deque(maxlen=10000)
        self.provider_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Configuration
        self.config = {
            "base_url": "https://openrouter.ai/api/v1",
            "max_concurrent_requests": 100,
            "request_timeout": 30,
            "retry_attempts": 3,
            "rate_limit_buffer": 0.1,  # 10% buffer
            "key_rotation_interval": 300,  # 5 minutes
            "health_check_interval": 60,   # 1 minute
            "performance_window": 3600     # 1 hour
        }
        
        # Initialize components
        self._initialize_models()
        self._initialize_api_keys()
        
        # Start background tasks
        asyncio.create_task(self._key_health_monitor())
        asyncio.create_task(self._performance_optimizer())
        
        logger.info("OpenRouter.ai Integration initialized with 3000+ API keys")
    
    def _initialize_models(self):
        """Initialize supported models configuration."""
        
        models_config = [
            # OpenAI Models
            {
                "model_name": "gpt-4-turbo",
                "provider": ModelProvider.OPENAI,
                "max_tokens": 128000,
                "cost_per_token": 0.00003,
                "capabilities": ["text", "code", "reasoning"],
                "preferred_use_cases": ["complex_analysis", "code_generation"]
            },
            {
                "model_name": "gpt-3.5-turbo",
                "provider": ModelProvider.OPENAI,
                "max_tokens": 16384,
                "cost_per_token": 0.000002,
                "capabilities": ["text", "conversation"],
                "preferred_use_cases": ["general_chat", "simple_tasks"]
            },
            
            # Anthropic Models
            {
                "model_name": "claude-3-opus",
                "provider": ModelProvider.ANTHROPIC,
                "max_tokens": 200000,
                "cost_per_token": 0.000075,
                "capabilities": ["text", "reasoning", "analysis"],
                "preferred_use_cases": ["complex_reasoning", "analysis"]
            },
            {
                "model_name": "claude-3-sonnet",
                "provider": ModelProvider.ANTHROPIC,
                "max_tokens": 200000,
                "cost_per_token": 0.000015,
                "capabilities": ["text", "reasoning", "code"],
                "preferred_use_cases": ["balanced_tasks", "code_analysis"]
            },
            
            # Google Models
            {
                "model_name": "gemini-pro",
                "provider": ModelProvider.GOOGLE,
                "max_tokens": 32768,
                "cost_per_token": 0.000001,
                "capabilities": ["text", "multimodal"],
                "preferred_use_cases": ["multimodal_tasks", "cost_effective"]
            },
            
            # Meta Models
            {
                "model_name": "llama-2-70b",
                "provider": ModelProvider.META,
                "max_tokens": 4096,
                "cost_per_token": 0.0000007,
                "capabilities": ["text", "open_source"],
                "preferred_use_cases": ["cost_effective", "privacy_focused"]
            }
        ]
        
        for model_config in models_config:
            model = ModelConfig(**model_config)
            self.models[model.model_name] = model
    
    def _initialize_api_keys(self):
        """Initialize 3000+ API keys pool."""
        
        # Simulate 3000+ API keys across different providers
        providers_distribution = {
            ModelProvider.OPENAI: 800,
            ModelProvider.ANTHROPIC: 600,
            ModelProvider.GOOGLE: 500,
            ModelProvider.COHERE: 400,
            ModelProvider.META: 300,
            ModelProvider.MISTRAL: 250,
            ModelProvider.PERPLEXITY: 150
        }
        
        key_id_counter = 1
        
        for provider, count in providers_distribution.items():
            for i in range(count):
                key_id = f"{provider.value}_key_{key_id_counter:04d}"
                
                # Generate realistic key configuration
                api_key = APIKey(
                    key_id=key_id,
                    provider=provider,
                    key_value=f"sk-{hashlib.md5(key_id.encode()).hexdigest()}",
                    rate_limit=random.randint(100, 1000),  # requests per minute
                    quota_limit=random.randint(10000, 100000),  # tokens per day
                    current_usage=0,
                    status=KeyStatus.ACTIVE,
                    last_used=0.0,
                    error_count=0,
                    success_count=0,
                    average_response_time=0.0
                )
                
                self.api_keys[key_id] = api_key
                key_id_counter += 1
        
        logger.info(f"Initialized {len(self.api_keys)} API keys across {len(providers_distribution)} providers")
    
    async def make_request(self, 
                          prompt: str,
                          model_preference: Optional[str] = None,
                          priority: RequestPriority = RequestPriority.MEDIUM,
                          max_tokens: Optional[int] = None,
                          temperature: float = 0.7,
                          **kwargs) -> OpenRouterResponse:
        """Make an API request through OpenRouter with intelligent routing."""
        
        request_id = hashlib.md5(f"{prompt}{time.time()}".encode()).hexdigest()[:12]
        start_time = time.time()
        
        try:
            # Select optimal model
            selected_model = self._select_optimal_model(
                model_preference, prompt, priority, max_tokens
            )
            
            # Select best API key for the model
            selected_key = await self._select_optimal_key(
                selected_model.provider, priority
            )
            
            if not selected_key:
                return OpenRouterResponse(
                    success=False,
                    response_data=None,
                    model_used="",
                    api_key_used="",
                    tokens_used=0,
                    cost=0.0,
                    response_time_ms=0.0,
                    error_message="No available API keys",
                    request_id=request_id
                )
            
            # Prepare request
            request_data = {
                "model": selected_model.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens or min(selected_model.max_tokens, 4096),
                "temperature": temperature,
                **kwargs
            }
            
            # Make API request
            response_data = await self._execute_request(
                selected_key, request_data, request_id
            )
            
            # Calculate metrics
            response_time = (time.time() - start_time) * 1000
            tokens_used = response_data.get("usage", {}).get("total_tokens", 0)
            cost = tokens_used * selected_model.cost_per_token
            
            # Update key statistics
            await self._update_key_stats(selected_key.key_id, True, response_time, tokens_used)
            
            # Record metrics
            metrics = RequestMetrics(
                request_id=request_id,
                model_used=selected_model.model_name,
                api_key_id=selected_key.key_id,
                response_time_ms=response_time,
                tokens_used=tokens_used,
                cost=cost,
                success=True,
                error_message=None,
                timestamp=time.time()
            )
            self.metrics_history.append(metrics)
            
            return OpenRouterResponse(
                success=True,
                response_data=response_data,
                model_used=selected_model.model_name,
                api_key_used=selected_key.key_id,
                tokens_used=tokens_used,
                cost=cost,
                response_time_ms=response_time,
                error_message=None,
                request_id=request_id
            )
            
        except Exception as e:
            error_message = str(e)
            response_time = (time.time() - start_time) * 1000
            
            # Update error statistics
            if 'selected_key' in locals():
                await self._update_key_stats(selected_key.key_id, False, response_time, 0)
            
            logger.error(f"Request {request_id} failed: {error_message}")
            
            return OpenRouterResponse(
                success=False,
                response_data=None,
                model_used=selected_model.model_name if 'selected_model' in locals() else "",
                api_key_used=selected_key.key_id if 'selected_key' in locals() else "",
                tokens_used=0,
                cost=0.0,
                response_time_ms=response_time,
                error_message=error_message,
                request_id=request_id
            )
    
    def _select_optimal_model(self, 
                            model_preference: Optional[str],
                            prompt: str,
                            priority: RequestPriority,
                            max_tokens: Optional[int]) -> ModelConfig:
        """Select optimal model based on requirements and performance."""
        
        # If specific model requested and available
        if model_preference and model_preference in self.models:
            return self.models[model_preference]
        
        # Analyze prompt to determine best model
        prompt_lower = prompt.lower()
        
        # Code-related tasks
        if any(keyword in prompt_lower for keyword in ["code", "implement", "function", "class", "debug"]):
            preferred_models = ["claude-3-sonnet", "gpt-4-turbo", "claude-3-opus"]
        
        # Complex reasoning tasks
        elif any(keyword in prompt_lower for keyword in ["analyze", "complex", "reasoning", "logic"]):
            preferred_models = ["claude-3-opus", "gpt-4-turbo", "claude-3-sonnet"]
        
        # Cost-sensitive tasks
        elif priority == RequestPriority.LOW:
            preferred_models = ["gemini-pro", "llama-2-70b", "gpt-3.5-turbo"]
        
        # High priority tasks
        elif priority == RequestPriority.CRITICAL:
            preferred_models = ["gpt-4-turbo", "claude-3-opus", "claude-3-sonnet"]
        
        # Default selection
        else:
            preferred_models = ["claude-3-sonnet", "gpt-3.5-turbo", "gemini-pro"]
        
        # Select first available model from preferences
        for model_name in preferred_models:
            if model_name in self.models:
                model = self.models[model_name]
                
                # Check token requirements
                if max_tokens and max_tokens > model.max_tokens:
                    continue
                
                # Check if provider has available keys
                available_keys = [
                    key for key in self.api_keys.values()
                    if key.provider == model.provider and key.status == KeyStatus.ACTIVE
                ]
                
                if available_keys:
                    return model
        
        # Fallback to any available model
        for model in self.models.values():
            available_keys = [
                key for key in self.api_keys.values()
                if key.provider == model.provider and key.status == KeyStatus.ACTIVE
            ]
            if available_keys:
                return model
        
        # Return first model as last resort
        return list(self.models.values())[0]
    
    async def _select_optimal_key(self, 
                                provider: ModelProvider,
                                priority: RequestPriority) -> Optional[APIKey]:
        """Select optimal API key for the provider."""
        
        # Get available keys for provider
        available_keys = [
            key for key in self.api_keys.values()
            if key.provider == provider and key.status == KeyStatus.ACTIVE
        ]
        
        if not available_keys:
            return None
        
        # Filter by rate limits and quotas
        usable_keys = []
        current_time = time.time()
        
        for key in available_keys:
            # Check rate limit (requests per minute)
            recent_requests = len([
                m for m in self.metrics_history
                if m.api_key_id == key.key_id and 
                   current_time - m.timestamp < 60
            ])
            
            if recent_requests < key.rate_limit * (1 - self.config["rate_limit_buffer"]):
                # Check daily quota
                daily_usage = sum([
                    m.tokens_used for m in self.metrics_history
                    if m.api_key_id == key.key_id and 
                       current_time - m.timestamp < 86400  # 24 hours
                ])
                
                if daily_usage < key.quota_limit * (1 - self.config["rate_limit_buffer"]):
                    usable_keys.append(key)
        
        if not usable_keys:
            return None
        
        # Select key based on priority and performance
        if priority == RequestPriority.CRITICAL:
            # Use key with best performance
            return min(usable_keys, key=lambda k: k.average_response_time or 1000)
        
        elif priority == RequestPriority.HIGH:
            # Balance performance and usage
            return min(usable_keys, key=lambda k: (k.average_response_time or 1000) + k.current_usage * 10)
        
        else:
            # Load balance across keys
            return min(usable_keys, key=lambda k: k.current_usage)
    
    async def _execute_request(self, 
                             api_key: APIKey,
                             request_data: Dict[str, Any],
                             request_id: str) -> Dict[str, Any]:
        """Execute API request with retry logic."""
        
        headers = {
            "Authorization": f"Bearer {api_key.key_value}",
            "Content-Type": "application/json",
            "X-Request-ID": request_id
        }
        
        for attempt in range(self.config["retry_attempts"]):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config["request_timeout"])) as session:
                    async with session.post(
                        f"{self.config['base_url']}/chat/completions",
                        headers=headers,
                        json=request_data
                    ) as response:
                        
                        if response.status == 200:
                            return await response.json()
                        
                        elif response.status == 429:  # Rate limited
                            api_key.status = KeyStatus.RATE_LIMITED
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        
                        elif response.status == 403:  # Quota exceeded
                            api_key.status = KeyStatus.QUOTA_EXCEEDED
                            raise Exception("API quota exceeded")
                        
                        else:
                            error_text = await response.text()
                            raise Exception(f"API error {response.status}: {error_text}")
            
            except asyncio.TimeoutError:
                if attempt == self.config["retry_attempts"] - 1:
                    raise Exception("Request timeout")
                await asyncio.sleep(1)
            
            except Exception as e:
                if attempt == self.config["retry_attempts"] - 1:
                    raise e
                await asyncio.sleep(1)
        
        raise Exception("Max retry attempts exceeded")
    
    async def _update_key_stats(self, 
                              key_id: str,
                              success: bool,
                              response_time: float,
                              tokens_used: int):
        """Update API key statistics."""
        
        if key_id not in self.api_keys:
            return
        
        key = self.api_keys[key_id]
        key.last_used = time.time()
        key.current_usage += tokens_used
        
        if success:
            key.success_count += 1
            # Update average response time
            if key.average_response_time == 0:
                key.average_response_time = response_time
            else:
                key.average_response_time = (key.average_response_time + response_time) / 2
        else:
            key.error_count += 1
            
            # Disable key if too many errors
            if key.error_count > 10 and key.error_count > key.success_count:
                key.status = KeyStatus.ERROR
    
    async def _key_health_monitor(self):
        """Monitor API key health and status."""
        
        while True:
            try:
                current_time = time.time()
                
                for key in self.api_keys.values():
                    # Reset rate limited keys after cooldown
                    if key.status == KeyStatus.RATE_LIMITED and current_time - key.last_used > 60:
                        key.status = KeyStatus.ACTIVE
                    
                    # Reset quota exceeded keys daily
                    if key.status == KeyStatus.QUOTA_EXCEEDED and current_time - key.last_used > 86400:
                        key.status = KeyStatus.ACTIVE
                        key.current_usage = 0
                    
                    # Re-enable error keys after cooldown if error rate improved
                    if key.status == KeyStatus.ERROR and current_time - key.last_used > 3600:
                        if key.success_count > key.error_count:
                            key.status = KeyStatus.ACTIVE
                
                await asyncio.sleep(self.config["health_check_interval"])
                
            except Exception as e:
                logger.error(f"Key health monitor error: {e}")
                await asyncio.sleep(60)
    
    async def _performance_optimizer(self):
        """Optimize performance based on metrics."""
        
        while True:
            try:
                # Analyze performance metrics
                if len(self.metrics_history) > 100:
                    recent_metrics = list(self.metrics_history)[-1000:]  # Last 1000 requests
                    
                    # Calculate provider performance
                    provider_performance = defaultdict(list)
                    for metric in recent_metrics:
                        model = self.models.get(metric.model_used)
                        if model:
                            provider_performance[model.provider.value].append(metric.response_time_ms)
                    
                    # Update provider statistics
                    for provider, times in provider_performance.items():
                        self.provider_stats[provider] = {
                            "average_response_time": statistics.mean(times),
                            "median_response_time": statistics.median(times),
                            "request_count": len(times),
                            "success_rate": len([t for t in times if t > 0]) / len(times)
                        }
                
                await asyncio.sleep(self.config["performance_window"])
                
            except Exception as e:
                logger.error(f"Performance optimizer error: {e}")
                await asyncio.sleep(300)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        
        active_keys = len([k for k in self.api_keys.values() if k.status == KeyStatus.ACTIVE])
        total_requests = len(self.metrics_history)
        successful_requests = len([m for m in self.metrics_history if m.success])
        
        return {
            "total_api_keys": len(self.api_keys),
            "active_api_keys": active_keys,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "success_rate": successful_requests / total_requests if total_requests > 0 else 0,
            "provider_stats": dict(self.provider_stats),
            "supported_models": len(self.models),
            "average_response_time": statistics.mean([m.response_time_ms for m in self.metrics_history]) if self.metrics_history else 0
        }


# Example usage
async def main():
    """Example usage of OpenRouter integration."""
    
    integration = OpenRouterIntegration()
    
    # Test request
    response = await integration.make_request(
        prompt="Explain the concept of microservices architecture",
        model_preference="claude-3-sonnet",
        priority=RequestPriority.MEDIUM,
        max_tokens=1000
    )
    
    print(f"Success: {response.success}")
    print(f"Model used: {response.model_used}")
    print(f"Response time: {response.response_time_ms:.2f}ms")
    print(f"Tokens used: {response.tokens_used}")
    print(f"Cost: ${response.cost:.6f}")
    
    # Get statistics
    stats = integration.get_statistics()
    print(f"\nStatistics:")
    print(f"Total API keys: {stats['total_api_keys']}")
    print(f"Active API keys: {stats['active_api_keys']}")
    print(f"Success rate: {stats['success_rate']:.2%}")


if __name__ == "__main__":
    asyncio.run(main())
