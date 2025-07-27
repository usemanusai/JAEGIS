# N.L.D.S. API Documentation

## Overview

The Natural Language Detection System (N.L.D.S.) API provides advanced natural language processing capabilities as the Tier 0 component of the JAEGIS Enhanced Agent System. This RESTful API enables seamless integration of natural language understanding, intent recognition, and JAEGIS command generation.

## Base URL

```
Production: https://api.jaegis.ai/v2
Staging: https://staging-api.jaegis.ai/v2
Development: http://localhost:8000/v2
```

## Authentication

N.L.D.S. API supports multiple authentication methods:

### JWT Token Authentication (Recommended)

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     https://api.jaegis.ai/v2/process
```

### API Key Authentication

```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.jaegis.ai/v2/process
```

## Core Endpoints

### 1. Process Natural Language Input

**Endpoint:** `POST /process`

**Description:** Process natural language input and generate JAEGIS commands with confidence scoring.

**Request Body:**
```json
{
  "input_text": "Create a secure user authentication system with JWT tokens",
  "user_id": "user123",
  "session_id": "session456",
  "processing_dimensions": ["logical", "emotional", "creative"],
  "preferred_mode": 3,
  "preferred_squad": "development",
  "context": {
    "project_type": "web_application",
    "technology_stack": "python"
  },
  "require_high_confidence": true
}
```

**Response:**
```json
{
  "request_id": "req_abc123",
  "processing_timestamp": "2024-01-15T10:30:00Z",
  "total_processing_time_ms": 245.7,
  "dimensional_analysis": [
    {
      "dimension": "logical",
      "confidence": 0.92,
      "analysis_result": {
        "intent": "create_authentication_system",
        "complexity": "medium",
        "technical_requirements": ["jwt", "security", "authentication"]
      },
      "processing_time_ms": 89.3
    }
  ],
  "overall_confidence": 0.89,
  "confidence_level": "high",
  "primary_command": {
    "command": "FRED:IMPLEMENT --component=auth --security=jwt --mode=secure",
    "mode": 3,
    "squad": "development",
    "parameters": {
      "component": "authentication_system",
      "security_level": "high",
      "token_type": "jwt"
    },
    "confidence": 0.89
  },
  "alternative_interpretations": [
    {
      "command": "ARCHITECT:DESIGN --system=auth --pattern=jwt",
      "confidence": 0.76,
      "reasoning": "Alternative design-focused approach"
    }
  ],
  "context_updates": {
    "last_intent": "create_authentication_system",
    "session_complexity": "medium"
  },
  "warnings": []
}
```

### 2. Health Check

**Endpoint:** `GET /health`

**Description:** Check system health and status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.2.0",
  "components": {
    "nlp_engine": "operational",
    "intent_recognition": "operational",
    "translation_engine": "operational",
    "jaegis_integration": "operational"
  },
  "performance_metrics": {
    "avg_response_time_ms": 234.5,
    "requests_per_minute": 847,
    "confidence_accuracy": 0.91
  }
}
```

### 3. User Profile Management

**Endpoint:** `GET /user/{user_id}/profile`

**Description:** Retrieve user profile and preferences.

**Response:**
```json
{
  "user_id": "user123",
  "preferences": {
    "default_processing_dimensions": ["logical", "creative"],
    "preferred_squad": "development",
    "confidence_threshold": 0.85
  },
  "usage_statistics": {
    "total_requests": 1247,
    "avg_confidence": 0.87,
    "most_common_intents": ["create", "implement", "analyze"]
  },
  "session_context": {
    "active_sessions": 2,
    "last_activity": "2024-01-15T10:25:00Z"
  }
}
```

### 4. Batch Processing

**Endpoint:** `POST /batch`

**Description:** Process multiple natural language inputs in a single request.

**Request Body:**
```json
{
  "inputs": [
    {
      "id": "input_1",
      "text": "Create a user authentication system",
      "context": {"priority": "high"}
    },
    {
      "id": "input_2", 
      "text": "Analyze system performance metrics",
      "context": {"priority": "medium"}
    }
  ],
  "batch_options": {
    "parallel_processing": true,
    "return_partial_results": true
  }
}
```

**Response:**
```json
{
  "batch_id": "batch_xyz789",
  "total_inputs": 2,
  "processed_inputs": 2,
  "failed_inputs": 0,
  "total_processing_time_ms": 456.2,
  "results": [
    {
      "input_id": "input_1",
      "status": "success",
      "result": {
        "primary_command": "FRED:IMPLEMENT --component=auth",
        "confidence": 0.91
      }
    },
    {
      "input_id": "input_2",
      "status": "success", 
      "result": {
        "primary_command": "TYLER:ANALYZE --metrics=performance",
        "confidence": 0.88
      }
    }
  ]
}
```

## Processing Dimensions

N.L.D.S. supports multi-dimensional analysis:

| Dimension | Description | Use Cases |
|-----------|-------------|-----------|
| `logical` | Logical reasoning and technical analysis | System design, technical implementation |
| `emotional` | Emotional context and user experience | UX design, user feedback analysis |
| `creative` | Creative problem-solving and innovation | Brainstorming, alternative solutions |
| `all` | Combined analysis across all dimensions | Comprehensive understanding |

## JAEGIS Integration

### Squad Types

| Squad | Description | Typical Commands |
|-------|-------------|------------------|
| `development` | Software development tasks | FRED:IMPLEMENT, FRED:BUILD |
| `analysis` | Analysis and research tasks | TYLER:ANALYZE, TYLER:INVESTIGATE |
| `security` | Security-related tasks | SECURE:PROTECT, SECURE:AUDIT |
| `content` | Documentation and content | DOCUMENT:CREATE, DOCUMENT:UPDATE |
| `integration` | System integration tasks | INTEGRATE:CONNECT, INTEGRATE:SYNC |

### Operation Modes

| Mode | Description | Complexity Level |
|------|-------------|------------------|
| 1 | Basic operations | Simple tasks |
| 2 | Standard operations | Moderate complexity |
| 3 | Advanced operations | Complex tasks |
| 4 | Expert operations | Highly complex tasks |
| 5 | Specialized operations | Domain-specific expertise |

## Error Handling

### HTTP Status Codes

| Code | Description | Response |
|------|-------------|----------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Authentication required or invalid |
| 403 | Forbidden | Insufficient permissions |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side processing error |

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Input text is required and cannot be empty",
    "details": {
      "field": "input_text",
      "provided_value": "",
      "expected_format": "non-empty string"
    },
    "request_id": "req_error123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Rate Limiting

N.L.D.S. implements intelligent rate limiting based on user tiers:

| Tier | Requests/Minute | Requests/Hour | Requests/Day |
|------|-----------------|---------------|--------------|
| Basic | 100 | 1,000 | 10,000 |
| Premium | 500 | 5,000 | 50,000 |
| Enterprise | 1,000 | 10,000 | 100,000 |
| Unlimited | ∞ | ∞ | ∞ |

### Rate Limit Headers

```
X-RateLimit-Limit-Minute: 100
X-RateLimit-Remaining-Minute: 87
X-RateLimit-Reset-Minute: 2024-01-15T10:31:00Z
Retry-After: 60
```

## SDK Integration

### Python SDK

```python
from nlds import NLDSClient

async with NLDSClient(api_key="your-api-key") as client:
    client.set_user_session("user123", "session456")
    
    response = await client.process(
        "Create a secure user authentication system",
        preferred_mode=3,
        preferred_squad="development"
    )
    
    print(f"Command: {response.primary_command.command}")
    print(f"Confidence: {response.overall_confidence:.2%}")
```

### JavaScript SDK

```javascript
const { NLDSClient } = require('nlds-client');

const client = new NLDSClient({
    apiKey: 'your-api-key',
    baseUrl: 'https://api.jaegis.ai/v2'
});

const response = await client.process(
    'Create a secure user authentication system',
    {
        preferredMode: 3,
        preferredSquad: 'development'
    }
);

console.log('Command:', response.primaryCommand.command);
console.log('Confidence:', response.overallConfidence);
```

## Webhooks

N.L.D.S. supports webhooks for real-time notifications:

### Webhook Configuration

```json
{
  "webhook_url": "https://your-app.com/webhooks/nlds",
  "events": ["processing_complete", "high_confidence_result", "error"],
  "secret": "your_webhook_secret",
  "retry_policy": {
    "max_retries": 3,
    "retry_delay_seconds": 60
  }
}
```

### Webhook Payload

```json
{
  "event": "processing_complete",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "request_id": "req_abc123",
    "user_id": "user123",
    "confidence": 0.89,
    "primary_command": "FRED:IMPLEMENT --component=auth"
  },
  "signature": "sha256=abc123..."
}
```

## Performance Optimization

### Caching

N.L.D.S. implements intelligent caching:

- **Session Context**: Cached for 1 hour
- **User Preferences**: Cached for 24 hours  
- **Common Patterns**: Cached for 7 days

### Request Optimization

```json
{
  "input_text": "Create authentication system",
  "optimization_hints": {
    "cache_result": true,
    "priority": "normal",
    "timeout_ms": 5000
  }
}
```

## Monitoring and Analytics

### Real-time Metrics

Access real-time performance metrics:

**Endpoint:** `GET /metrics`

```json
{
  "current_load": {
    "requests_per_second": 23.4,
    "avg_response_time_ms": 234.5,
    "active_sessions": 156
  },
  "confidence_metrics": {
    "avg_confidence": 0.87,
    "high_confidence_rate": 0.73,
    "low_confidence_rate": 0.12
  },
  "system_health": {
    "cpu_usage": 0.45,
    "memory_usage": 0.62,
    "disk_usage": 0.23
  }
}
```

## Compliance and Security

### Data Protection

- All data encrypted in transit (TLS 1.3)
- Sensitive data encrypted at rest (AES-256)
- GDPR compliant data handling
- SOC 2 Type II certified

### Audit Logging

All API requests are logged with:
- Request/response details
- User identification
- Processing metrics
- Security events

## Support and Resources

### Documentation Links

- [Getting Started Guide](./getting-started.md)
- [SDK Documentation](./sdks/)
- [Integration Examples](./examples/)
- [Troubleshooting Guide](./troubleshooting.md)

### Support Channels

- **Technical Support**: support@jaegis.ai
- **API Issues**: api-support@jaegis.ai
- **Documentation**: docs@jaegis.ai
- **Emergency**: emergency@jaegis.ai

### Status Page

Monitor API status: https://status.jaegis.ai

---

**API Version:** 2.2.0  
**Last Updated:** January 15, 2024  
**Next Update:** February 1, 2024
