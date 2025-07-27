# N.L.D.S. API Reference Documentation

## **Overview**

The Natural Language Detection System (N.L.D.S.) API provides a comprehensive RESTful interface for processing natural language input and generating optimized JAEGIS commands. As the Tier 0 component of JAEGIS v2.2, N.L.D.S. serves as the primary human-AI interface.

## **Base URL**

```
Production: https://api.jaegis.ai/v1
Development: http://localhost:8000
```

## **Authentication**

All API requests require authentication using JWT tokens or API keys.

### **JWT Authentication**
```http
Authorization: Bearer <jwt_token>
```

### **API Key Authentication**
```http
Authorization: Bearer <api_key>
```

### **Authentication Endpoints**

#### **POST /auth/login**
Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "user_id": "string",
    "username": "string",
    "role": "admin|developer|user|readonly",
    "permissions": ["read", "write", "admin", "process"]
  }
}
```

#### **POST /auth/refresh**
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## **Core Processing Endpoints**

### **POST /process**
Process natural language input through the N.L.D.S. pipeline.

**Request Body:**
```json
{
  "input_text": "string (required, max 10000 chars)",
  "mode": "standard|enhanced|comprehensive (optional, default: standard)",
  "enable_amasiap": "boolean (optional, default: true)",
  "context": {
    "domain": "string (optional)",
    "urgency": "low|medium|high (optional)",
    "audience": "string (optional)",
    "user_preferences": "object (optional)"
  },
  "options": {
    "enable_caching": "boolean (optional, default: true)",
    "timeout_seconds": "number (optional, default: 30)"
  }
}
```

**Response:**
```json
{
  "success": true,
  "request_id": "string",
  "original_input": "string",
  "enhanced_input": "string",
  "confidence_score": 0.92,
  "processing_time_ms": 450,
  "metadata": {
    "enhancement_applied": true,
    "quality_score": 0.88,
    "context_enrichment": {
      "temporal_context": "2025-07-26T12:00:00Z",
      "domain_context": "technology",
      "system_context": "JAEGIS v2.2"
    }
  }
}
```

### **POST /analyze**
Perform multi-dimensional analysis of processed input.

**Request Body:**
```json
{
  "input_text": "string (required)",
  "analysis_types": ["logical", "emotional", "creative", "comprehensive"],
  "depth_level": "number (1-5, optional, default: 3)",
  "context": "object (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "request_id": "string",
  "input_text": "string",
  "logical_analysis": {
    "confidence": 0.89,
    "requirements": ["analyze", "recommend", "implement"],
    "logical_structure": "sequential",
    "reasoning_type": "analytical",
    "complexity_score": 0.75
  },
  "emotional_analysis": {
    "confidence": 0.82,
    "sentiment": "positive",
    "emotional_intensity": 0.6,
    "detected_emotions": ["enthusiasm", "determination"],
    "emotional_context": "professional"
  },
  "creative_analysis": {
    "confidence": 0.85,
    "creativity_score": 0.7,
    "innovation_potential": "high",
    "creative_patterns": ["strategic_thinking", "problem_solving"],
    "originality_score": 0.8
  },
  "synthesis": {
    "overall_confidence": 0.85,
    "recommended_approach": "comprehensive",
    "key_insights": ["strategic_focus", "technical_implementation"],
    "confidence_distribution": {
      "logical": 0.4,
      "emotional": 0.3,
      "creative": 0.3
    }
  },
  "processing_time_ms": 1200,
  "depth_level": 3
}
```

### **POST /translate**
Translate analysis results into optimized JAEGIS commands.

**Request Body:**
```json
{
  "input_text": "string (required)",
  "analysis_result": "object (optional, if not provided, analysis will be performed)",
  "target_mode": "number (1-5, optional)",
  "preferred_squad": "string (optional)",
  "priority": "low|normal|high|urgent (optional, default: normal)",
  "constraints": {
    "budget_limit": "number (optional)",
    "time_limit": "number (optional)",
    "resource_constraints": "array (optional)"
  }
}
```

**Response:**
```json
{
  "success": true,
  "request_id": "string",
  "jaegis_command": {
    "command_id": "cmd_20250726_001",
    "command_type": "comprehensive_analysis",
    "target_squad": "content_squad",
    "mode_level": 3,
    "parameters": [
      {
        "type": "text_input",
        "value": "Enhanced input text",
        "confidence": 0.95
      },
      {
        "type": "context",
        "value": {
          "domain": "technology",
          "urgency": "medium"
        },
        "confidence": 0.88
      }
    ],
    "priority": "normal",
    "estimated_duration": 300,
    "resource_requirements": {
      "agents_required": 4,
      "estimated_cost": 0.05
    }
  },
  "confidence_score": 0.87,
  "alternative_commands": [
    {
      "command_id": "cmd_20250726_002",
      "command_type": "focused_analysis",
      "confidence": 0.82
    }
  ],
  "processing_time_ms": 180,
  "metadata": {
    "translation_strategy": "confidence_optimized",
    "fallback_options": 2
  }
}
```

## **JAEGIS Integration Endpoints**

### **POST /jaegis/submit**
Submit JAEGIS command for execution.

**Request Body:**
```json
{
  "command": {
    "command_id": "string",
    "command_type": "string",
    "target_squad": "string",
    "mode_level": "number",
    "parameters": "array"
  },
  "priority": "low|normal|high|urgent (optional, default: normal)",
  "timeout_seconds": "number (optional, default: 300)",
  "callback_url": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "command_id": "string",
  "status": "submitted|queued|processing|completed|failed",
  "submission_time": "2025-07-26T12:00:00Z",
  "estimated_completion": "2025-07-26T12:05:00Z",
  "queue_position": 3
}
```

### **GET /jaegis/status/{command_id}**
Get JAEGIS command execution status.

**Response:**
```json
{
  "command_id": "string",
  "status": "submitted|queued|processing|completed|failed",
  "progress_percentage": 75.0,
  "current_stage": "analysis_phase",
  "estimated_completion": "2025-07-26T12:05:00Z",
  "result_data": {
    "success": true,
    "output": "Analysis completed successfully",
    "artifacts": ["report.pdf", "data.json"],
    "metrics": {
      "processing_time": 240,
      "agents_used": 4,
      "confidence_score": 0.91
    }
  },
  "error_details": null
}
```

### **GET /jaegis/results/{command_id}**
Retrieve JAEGIS command execution results.

**Response:**
```json
{
  "command_id": "string",
  "status": "completed",
  "completion_time": "2025-07-26T12:05:00Z",
  "results": {
    "primary_output": "string",
    "artifacts": [
      {
        "type": "document",
        "name": "analysis_report.pdf",
        "url": "https://api.jaegis.ai/artifacts/...",
        "size": 1024000
      }
    ],
    "metrics": {
      "total_processing_time": 300,
      "agents_involved": ["john", "content_squad_1", "content_squad_2"],
      "confidence_score": 0.91,
      "quality_score": 0.88
    },
    "recommendations": [
      "Consider implementing automated testing",
      "Optimize database queries for better performance"
    ]
  }
}
```

## **System Status Endpoints**

### **GET /health**
System health check (no authentication required).

**Response:**
```json
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": "2025-07-26T12:00:00Z",
  "version": "2.2.0",
  "components": {
    "nlds_core": "healthy",
    "database": "healthy",
    "cache": "healthy",
    "jaegis_integration": "healthy",
    "external_apis": "degraded"
  },
  "uptime_seconds": 86400
}
```

### **GET /status**
Detailed system status (requires authentication).

**Response:**
```json
{
  "system_status": "operational",
  "timestamp": "2025-07-26T12:00:00Z",
  "component_status": {
    "processing_orchestrator": {
      "status": "healthy",
      "response_time_ms": 45,
      "throughput_rpm": 850,
      "error_rate": 0.02
    },
    "analysis_orchestrator": {
      "status": "healthy",
      "response_time_ms": 120,
      "confidence_accuracy": 0.89,
      "analysis_depth": 4.2
    },
    "translation_orchestrator": {
      "status": "healthy",
      "response_time_ms": 35,
      "command_success_rate": 0.94,
      "optimization_score": 0.87
    }
  },
  "performance_metrics": {
    "requests_per_minute": 850,
    "average_response_time_ms": 420,
    "p95_response_time_ms": 680,
    "error_rate": 0.015,
    "cache_hit_rate": 0.78
  },
  "resource_utilization": {
    "cpu_usage": 0.65,
    "memory_usage": 0.72,
    "disk_usage": 0.45,
    "network_io": 0.38
  }
}
```

### **GET /metrics**
Prometheus-compatible metrics (requires admin role).

**Response:**
```
# HELP nlds_requests_total Total number of requests processed
# TYPE nlds_requests_total counter
nlds_requests_total{endpoint="/process",status="success"} 15420
nlds_requests_total{endpoint="/process",status="error"} 234

# HELP nlds_response_time_seconds Response time in seconds
# TYPE nlds_response_time_seconds histogram
nlds_response_time_seconds_bucket{endpoint="/process",le="0.1"} 8950
nlds_response_time_seconds_bucket{endpoint="/process",le="0.5"} 14200
nlds_response_time_seconds_bucket{endpoint="/process",le="1.0"} 15420
```

## **Error Handling**

### **Error Response Format**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input text exceeds maximum length of 10000 characters",
    "details": {
      "field": "input_text",
      "provided_length": 12500,
      "max_length": 10000
    },
    "request_id": "req_20250726_001",
    "timestamp": "2025-07-26T12:00:00Z"
  }
}
```

### **Common Error Codes**

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `AUTHENTICATION_REQUIRED` | 401 | Authentication required |
| `INSUFFICIENT_PERMISSIONS` | 403 | Insufficient permissions |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded |
| `PROCESSING_ERROR` | 500 | Internal processing error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |
| `TIMEOUT_ERROR` | 504 | Request timeout |

## **Rate Limiting**

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1627846261
X-RateLimit-Scope: user
```

### **Rate Limit Tiers**

| User Role | Requests/Minute | Burst Limit |
|-----------|-----------------|-------------|
| **ReadOnly** | 100 | 150 |
| **User** | 500 | 750 |
| **Developer** | 1000 | 1500 |
| **Admin** | Unlimited | Unlimited |
| **Service** | 2000 | 3000 |

## **Webhooks**

### **Webhook Configuration**
```json
{
  "webhook_url": "https://your-app.com/webhooks/nlds",
  "events": ["command.completed", "command.failed", "system.alert"],
  "secret": "your-webhook-secret",
  "retry_policy": {
    "max_retries": 3,
    "retry_delay_seconds": 60
  }
}
```

### **Webhook Payload**
```json
{
  "event": "command.completed",
  "timestamp": "2025-07-26T12:05:00Z",
  "data": {
    "command_id": "cmd_20250726_001",
    "status": "completed",
    "results": {
      "success": true,
      "confidence_score": 0.91
    }
  },
  "signature": "sha256=..."
}
```

## **Advanced Features**

### **Batch Processing**

#### **POST /batch/process**
Process multiple inputs in a single request.

**Request Body:**
```json
{
  "inputs": [
    {
      "id": "batch_001",
      "input_text": "First input text",
      "context": {"domain": "technology"}
    },
    {
      "id": "batch_002",
      "input_text": "Second input text",
      "context": {"domain": "business"}
    }
  ],
  "options": {
    "parallel_processing": true,
    "max_concurrent": 5
  }
}
```

**Response:**
```json
{
  "success": true,
  "batch_id": "batch_20250726_001",
  "results": [
    {
      "id": "batch_001",
      "success": true,
      "enhanced_input": "Enhanced first input",
      "confidence_score": 0.89
    },
    {
      "id": "batch_002",
      "success": true,
      "enhanced_input": "Enhanced second input",
      "confidence_score": 0.92
    }
  ],
  "summary": {
    "total_inputs": 2,
    "successful": 2,
    "failed": 0,
    "average_confidence": 0.905,
    "total_processing_time_ms": 850
  }
}
```

### **Streaming API**

#### **POST /stream/process**
Process input with real-time streaming response.

**Request:**
```bash
curl -X POST http://localhost:8000/stream/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{"input_text": "Analyze market trends"}' \
  --no-buffer
```

**Response (Server-Sent Events):**
```
data: {"event": "processing_started", "timestamp": "2025-07-26T12:00:00Z"}

data: {"event": "enhancement_complete", "confidence": 0.85, "progress": 25}

data: {"event": "analysis_complete", "confidence": 0.89, "progress": 75}

data: {"event": "translation_complete", "jaegis_command": {...}, "progress": 100}

data: {"event": "processing_complete", "final_result": {...}}
```

### **WebSocket API**

#### **WS /ws/realtime**
Real-time bidirectional communication.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/realtime?token=your-jwt-token');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'process',
    data: {
      input_text: 'Create strategic plan',
      enable_realtime_updates: true
    }
  }));
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};
```

## **SDK Examples**

### **Python SDK**
```python
from nlds_sdk import NLDSClient

# Initialize client
client = NLDSClient(
    base_url="https://api.jaegis.ai/v1",
    api_key="your-api-key"
)

# Process input
result = await client.process(
    input_text="Analyze system performance",
    mode="enhanced",
    enable_amasiap=True
)

print(f"Confidence: {result.confidence_score}")
print(f"JAEGIS Command: {result.jaegis_command}")
```

### **JavaScript SDK**
```javascript
import { NLDSClient } from '@jaegis/nlds-sdk';

const client = new NLDSClient({
  baseURL: 'https://api.jaegis.ai/v1',
  apiKey: 'your-api-key'
});

const result = await client.process({
  inputText: 'Create project roadmap',
  mode: 'comprehensive',
  enableAmasiap: true
});

console.log('Confidence:', result.confidenceScore);
console.log('Command:', result.jaegisCommand);
```

### **cURL Examples**

#### **Basic Processing**
```bash
curl -X POST https://api.jaegis.ai/v1/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "input_text": "Optimize database performance",
    "mode": "enhanced",
    "context": {
      "domain": "technology",
      "urgency": "high"
    }
  }'
```

#### **Complete Pipeline**
```bash
# Step 1: Process input
PROCESS_RESULT=$(curl -s -X POST https://api.jaegis.ai/v1/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"input_text": "Create marketing strategy"}')

# Step 2: Analyze processed input
ENHANCED_INPUT=$(echo $PROCESS_RESULT | jq -r '.enhanced_input')
ANALYSIS_RESULT=$(curl -s -X POST https://api.jaegis.ai/v1/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d "{\"input_text\": \"$ENHANCED_INPUT\"}")

# Step 3: Translate to JAEGIS command
JAEGIS_COMMAND=$(curl -s -X POST https://api.jaegis.ai/v1/translate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d "{\"input_text\": \"$ENHANCED_INPUT\"}")

echo "Final JAEGIS Command: $JAEGIS_COMMAND"
```

---

**API Version**: 1.0
**Last Updated**: July 26, 2025
**Status**: Production Ready
**Support**: api-support@jaegis.ai
