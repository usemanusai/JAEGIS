# N.L.D.S. Developer Quick Start

## **5-Minute Setup Guide**

Get up and running with N.L.D.S. in 5 minutes or less.

### **Step 1: Installation**

#### **Python**
```bash
pip install nlds-sdk
```

#### **Node.js**
```bash
npm install @jaegis/nlds-sdk
```

#### **Docker**
```bash
docker pull jaegis/nlds:latest
docker run -p 8000:8000 jaegis/nlds:latest
```

### **Step 2: Authentication**

Get your API key from the [JAEGIS Dashboard](https://dashboard.jaegis.ai):

```python
# Python
import os
os.environ['NLDS_API_KEY'] = 'your-api-key-here'
```

```javascript
// Node.js
process.env.NLDS_API_KEY = 'your-api-key-here';
```

### **Step 3: First Request**

#### **Python Example**
```python
from nlds_sdk import NLDSClient

# Initialize client
client = NLDSClient()

# Process natural language
result = await client.process(
    "Create a REST API for user management with authentication"
)

print(f"Confidence: {result.confidence_score:.2%}")
print(f"Enhanced Input: {result.enhanced_input}")
print(f"JAEGIS Command: {result.jaegis_command}")
```

#### **JavaScript Example**
```javascript
import { NLDSClient } from '@jaegis/nlds-sdk';

const client = new NLDSClient();

const result = await client.process(
  'Create a REST API for user management with authentication'
);

console.log(`Confidence: ${result.confidenceScore}%`);
console.log(`Enhanced Input: ${result.enhancedInput}`);
console.log(`JAEGIS Command:`, result.jaegisCommand);
```

#### **cURL Example**
```bash
curl -X POST https://api.jaegis.ai/v1/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "input_text": "Create a REST API for user management with authentication"
  }'
```

### **Step 4: Enhanced Processing**

```python
# Add context for better results
result = await client.process(
    input_text="Optimize database queries for better performance",
    mode="enhanced",
    enable_amasiap=True,
    context={
        "domain": "technology",
        "tech_stack": ["postgresql", "python"],
        "urgency": "high",
        "current_issues": ["slow_queries", "high_cpu_usage"]
    }
)
```

## **Common Use Cases**

### **1. Code Generation**
```python
result = await client.process(
    "Generate a Python function that validates email addresses using regex"
)
```

### **2. System Analysis**
```python
result = await client.process(
    "Analyze our microservices architecture and identify potential bottlenecks",
    context={"domain": "architecture", "scale": "enterprise"}
)
```

### **3. Documentation**
```python
result = await client.process(
    "Create API documentation for our user authentication endpoints",
    context={"format": "openapi", "audience": "developers"}
)
```

### **4. Testing Strategy**
```python
result = await client.process(
    "Design a comprehensive testing strategy for our e-commerce platform",
    context={"testing_types": ["unit", "integration", "e2e"]}
)
```

## **Advanced Features**

### **Streaming Responses**
```python
async for update in client.stream_process("Analyze large dataset"):
    print(f"Progress: {update.progress}%")
    if update.event == "complete":
        print(f"Final result: {update.result}")
```

### **Batch Processing**
```python
inputs = [
    {"id": "task1", "input_text": "Create user model"},
    {"id": "task2", "input_text": "Design authentication flow"},
    {"id": "task3", "input_text": "Implement rate limiting"}
]

results = await client.batch_process(inputs)
for result in results:
    print(f"{result.id}: {result.confidence_score:.2%}")
```

### **WebSocket Integration**
```python
import asyncio
import websockets

async def realtime_processing():
    uri = "ws://localhost:8000/ws/realtime"
    headers = {"Authorization": "Bearer your-api-key"}
    
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        # Send request
        await websocket.send(json.dumps({
            "type": "process",
            "data": {"input_text": "Create deployment pipeline"}
        }))
        
        # Receive updates
        async for message in websocket:
            data = json.loads(message)
            print(f"Update: {data}")
```

## **Error Handling**

```python
from nlds_sdk import NLDSError, ValidationError, RateLimitError

try:
    result = await client.process("Your input here")
except ValidationError as e:
    print(f"Input validation failed: {e.message}")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after: {e.retry_after}")
except NLDSError as e:
    print(f"NLDS error: {e.message}")
```

## **Configuration**

### **Environment Variables**
```bash
export NLDS_API_KEY="your-api-key"
export NLDS_BASE_URL="https://api.jaegis.ai/v1"
export NLDS_TIMEOUT=30
export NLDS_MAX_RETRIES=3
```

### **Client Configuration**
```python
client = NLDSClient(
    api_key="your-api-key",
    base_url="https://api.jaegis.ai/v1",
    timeout=30,
    max_retries=3,
    enable_caching=True,
    cache_ttl=300  # 5 minutes
)
```

## **Testing**

### **Unit Tests**
```python
import pytest
from unittest.mock import AsyncMock
from nlds_sdk import NLDSClient

@pytest.mark.asyncio
async def test_process_success():
    client = NLDSClient()
    client._make_request = AsyncMock(return_value={
        "success": True,
        "confidence_score": 0.92,
        "enhanced_input": "Enhanced input text"
    })
    
    result = await client.process("Test input")
    assert result.confidence_score == 0.92
    assert result.success is True
```

### **Integration Tests**
```python
@pytest.mark.integration
async def test_real_api():
    client = NLDSClient()
    result = await client.process(
        "Create a simple hello world function in Python"
    )
    assert result.confidence_score > 0.8
    assert "python" in result.enhanced_input.lower()
```

## **Performance Optimization**

### **Caching**
```python
# Enable client-side caching
client = NLDSClient(enable_caching=True, cache_ttl=300)

# Manual cache control
result = await client.process(
    "Your input",
    cache_key="custom-key",
    use_cache=True
)
```

### **Concurrent Processing**
```python
import asyncio

async def process_multiple():
    tasks = [
        client.process("Task 1"),
        client.process("Task 2"), 
        client.process("Task 3")
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### **Connection Pooling**
```python
# Configure connection pool
client = NLDSClient(
    pool_connections=10,
    pool_maxsize=20,
    pool_block=True
)
```

## **Monitoring & Debugging**

### **Logging**
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('nlds_sdk')

# Custom logging
client = NLDSClient(debug=True)
```

### **Metrics Collection**
```python
# Track performance metrics
result = await client.process("Your input")
print(f"Processing time: {result.processing_time_ms}ms")
print(f"Tokens used: {result.token_usage}")
print(f"Cache hit: {result.cache_hit}")
```

### **Health Checks**
```python
# Check system health
health = await client.health_check()
print(f"Status: {health.status}")
print(f"Response time: {health.response_time_ms}ms")
```

## **Production Deployment**

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

### **Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nlds-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nlds-app
  template:
    metadata:
      labels:
        app: nlds-app
    spec:
      containers:
      - name: app
        image: your-app:latest
        env:
        - name: NLDS_API_KEY
          valueFrom:
            secretKeyRef:
              name: nlds-secret
              key: api-key
```

### **Environment Configuration**
```python
# Production settings
client = NLDSClient(
    api_key=os.getenv('NLDS_API_KEY'),
    base_url=os.getenv('NLDS_BASE_URL', 'https://api.jaegis.ai/v1'),
    timeout=int(os.getenv('NLDS_TIMEOUT', '30')),
    max_retries=int(os.getenv('NLDS_MAX_RETRIES', '3')),
    enable_caching=os.getenv('NLDS_ENABLE_CACHE', 'true').lower() == 'true'
)
```

## **Next Steps**

1. **Explore Advanced Features**: Try batch processing, streaming, and WebSocket APIs
2. **Read the Full Documentation**: Visit [docs.jaegis.ai](https://docs.jaegis.ai)
3. **Join the Community**: Connect with other developers on [Discord](https://discord.gg/jaegis)
4. **Contribute**: Check out our [GitHub repository](https://github.com/usemanusai/JAEGIS)

## **Support**

- **Documentation**: https://docs.jaegis.ai
- **API Reference**: https://docs.jaegis.ai/api
- **GitHub Issues**: https://github.com/usemanusai/JAEGIS/issues
- **Discord Community**: https://discord.gg/jaegis
- **Email Support**: support@jaegis.ai

---

**Quick Start Version**: 1.0  
**Last Updated**: July 26, 2025  
**Estimated Setup Time**: 5 minutes
