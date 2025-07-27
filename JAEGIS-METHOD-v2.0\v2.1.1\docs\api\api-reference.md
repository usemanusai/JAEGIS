# N.L.D.S. API Reference

## Overview

The N.L.D.S. (Natural Language Detection System) API provides comprehensive natural language processing capabilities as the Tier 0 component of the JAEGIS Enhanced Agent System. This reference documentation covers all available endpoints, request/response formats, and integration patterns.

## Base Information

- **Base URL**: `https://api.jaegis.ai/v2`
- **Protocol**: HTTPS only
- **Content-Type**: `application/json`
- **API Version**: 2.2.0
- **Rate Limiting**: Tier-based (see [Rate Limiting](#rate-limiting))

## Authentication

### JWT Token (Recommended)

```http
Authorization: Bearer <jwt_token>
```

### API Key

```http
X-API-Key: <api_key>
```

## Core Endpoints

### POST /process

Process natural language input and generate JAEGIS commands.

#### Request

```http
POST /process
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

**Request Body Schema:**

```json
{
  "input_text": "string (required)",
  "user_id": "string (optional)",
  "session_id": "string (optional)",
  "processing_dimensions": ["logical", "emotional", "creative"] (optional),
  "preferred_mode": 1-5 (optional),
  "preferred_squad": "string (optional)",
  "context": {} (optional),
  "require_high_confidence": true (optional),
  "timeout_ms": 5000 (optional)
}
```

**Field Descriptions:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input_text` | string | Yes | Natural language input to process (1-10000 chars) |
| `user_id` | string | No | User identifier for personalization |
| `session_id` | string | No | Session identifier for context continuity |
| `processing_dimensions` | array | No | Dimensions to analyze: logical, emotional, creative, all |
| `preferred_mode` | integer | No | JAEGIS operation mode (1-5) |
| `preferred_squad` | string | No | Preferred squad for execution |
| `context` | object | No | Additional context information |
| `require_high_confidence` | boolean | No | Require ≥85% confidence (default: true) |
| `timeout_ms` | integer | No | Processing timeout in milliseconds |

#### Response

**Success Response (200):**

```json
{
  "request_id": "req_abc123def456",
  "processing_timestamp": "2024-01-15T10:30:00.123Z",
  "total_processing_time_ms": 245.7,
  "dimensional_analysis": [
    {
      "dimension": "logical",
      "confidence": 0.92,
      "analysis_result": {
        "intent": "create_authentication_system",
        "complexity": "medium",
        "technical_requirements": ["jwt", "security", "authentication"],
        "estimated_effort": "4-6 hours",
        "risk_factors": ["security_implementation", "integration_complexity"]
      },
      "processing_time_ms": 89.3
    },
    {
      "dimension": "emotional",
      "confidence": 0.78,
      "analysis_result": {
        "user_sentiment": "determined",
        "urgency_level": "medium",
        "satisfaction_factors": ["security", "reliability", "ease_of_use"]
      },
      "processing_time_ms": 67.2
    },
    {
      "dimension": "creative",
      "confidence": 0.85,
      "analysis_result": {
        "alternative_approaches": ["oauth2", "saml", "biometric"],
        "innovation_opportunities": ["passwordless_auth", "ai_behavior_analysis"],
        "design_patterns": ["decorator", "strategy", "factory"]
      },
      "processing_time_ms": 89.2
    }
  ],
  "overall_confidence": 0.89,
  "confidence_level": "high",
  "primary_command": {
    "command": "FRED:IMPLEMENT --component=auth --security=jwt --mode=secure --priority=high",
    "mode": 3,
    "squad": "development",
    "parameters": {
      "component": "authentication_system",
      "security_level": "high",
      "token_type": "jwt",
      "implementation_pattern": "secure_by_default",
      "testing_required": true
    },
    "confidence": 0.89,
    "estimated_duration": "4-6 hours",
    "dependencies": ["security_framework", "database_schema"]
  },
  "alternative_interpretations": [
    {
      "command": "ARCHITECT:DESIGN --system=auth --pattern=jwt --security=high",
      "confidence": 0.76,
      "reasoning": "Design-first approach for complex authentication system",
      "mode": 4,
      "squad": "architecture"
    },
    {
      "command": "SECURITY:AUDIT --component=auth --framework=jwt",
      "confidence": 0.71,
      "reasoning": "Security-focused analysis of authentication requirements",
      "mode": 3,
      "squad": "security"
    }
  ],
  "context_updates": {
    "last_intent": "create_authentication_system",
    "session_complexity": "medium",
    "user_preferences": {
      "security_focus": true,
      "implementation_speed": "balanced"
    },
    "project_context": {
      "technology_stack": "inferred_python",
      "architecture_pattern": "microservices"
    }
  },
  "warnings": [],
  "metadata": {
    "model_versions": {
      "nlp_engine": "2.2.0",
      "intent_classifier": "1.5.2",
      "confidence_scorer": "1.3.1"
    },
    "processing_pipeline": ["tokenization", "semantic_analysis", "intent_recognition", "command_generation"],
    "quality_metrics": {
      "input_clarity": 0.91,
      "context_richness": 0.67,
      "output_specificity": 0.88
    }
  }
}
```

**Error Responses:**

```json
// 400 Bad Request
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Input text is required and cannot be empty",
    "details": {
      "field": "input_text",
      "provided_value": "",
      "expected_format": "non-empty string (1-10000 characters)"
    },
    "request_id": "req_error123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// 401 Unauthorized
{
  "error": {
    "code": "AUTHENTICATION_REQUIRED",
    "message": "Valid authentication token required",
    "details": {
      "auth_methods": ["jwt_token", "api_key"],
      "token_format": "Bearer <token> or X-API-Key: <key>"
    },
    "request_id": "req_auth_error",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// 429 Too Many Requests
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Request rate limit exceeded for your tier",
    "details": {
      "current_tier": "basic",
      "limit_per_minute": 100,
      "requests_made": 101,
      "reset_time": "2024-01-15T10:31:00Z"
    },
    "request_id": "req_rate_limit",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### POST /batch

Process multiple natural language inputs in a single request.

#### Request

```json
{
  "inputs": [
    {
      "id": "input_1",
      "text": "Create a user authentication system with JWT tokens",
      "context": {
        "priority": "high",
        "project": "web_app"
      }
    },
    {
      "id": "input_2",
      "text": "Analyze system performance metrics and identify bottlenecks",
      "context": {
        "priority": "medium",
        "system": "production"
      }
    }
  ],
  "batch_options": {
    "parallel_processing": true,
    "return_partial_results": true,
    "max_processing_time_ms": 10000,
    "fail_fast": false
  },
  "default_options": {
    "processing_dimensions": ["logical", "creative"],
    "require_high_confidence": true
  }
}
```

#### Response

```json
{
  "batch_id": "batch_xyz789abc123",
  "total_inputs": 2,
  "processed_inputs": 2,
  "failed_inputs": 0,
  "total_processing_time_ms": 456.2,
  "parallel_processing_used": true,
  "results": [
    {
      "input_id": "input_1",
      "status": "success",
      "processing_time_ms": 234.5,
      "result": {
        "primary_command": {
          "command": "FRED:IMPLEMENT --component=auth --security=jwt",
          "confidence": 0.91
        },
        "overall_confidence": 0.91
      }
    },
    {
      "input_id": "input_2",
      "status": "success",
      "processing_time_ms": 221.7,
      "result": {
        "primary_command": {
          "command": "TYLER:ANALYZE --metrics=performance --scope=bottlenecks",
          "confidence": 0.88
        },
        "overall_confidence": 0.88
      }
    }
  ],
  "batch_metadata": {
    "processing_efficiency": 0.94,
    "average_confidence": 0.895,
    "resource_utilization": {
      "cpu_usage": 0.67,
      "memory_usage": 0.45
    }
  }
}
```

### GET /health

Check system health and operational status.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.2.0",
  "uptime_seconds": 86400,
  "components": {
    "nlp_engine": {
      "status": "operational",
      "response_time_ms": 12.3,
      "last_check": "2024-01-15T10:29:55Z"
    },
    "intent_recognition": {
      "status": "operational",
      "accuracy": 0.91,
      "last_check": "2024-01-15T10:29:55Z"
    },
    "translation_engine": {
      "status": "operational",
      "success_rate": 0.97,
      "last_check": "2024-01-15T10:29:55Z"
    },
    "jaegis_integration": {
      "status": "operational",
      "coordination_efficiency": 0.94,
      "last_check": "2024-01-15T10:29:55Z"
    },
    "database": {
      "status": "operational",
      "connection_pool": "85% utilized",
      "last_check": "2024-01-15T10:29:55Z"
    },
    "cache": {
      "status": "operational",
      "hit_ratio": 0.89,
      "last_check": "2024-01-15T10:29:55Z"
    }
  },
  "performance_metrics": {
    "avg_response_time_ms": 234.5,
    "requests_per_minute": 847,
    "confidence_accuracy": 0.91,
    "error_rate": 0.012,
    "uptime_percentage": 99.97
  },
  "resource_usage": {
    "cpu_usage": 0.45,
    "memory_usage": 0.62,
    "disk_usage": 0.23,
    "network_io": "moderate"
  }
}
```

### GET /user/{user_id}/profile

Retrieve user profile and processing preferences.

#### Response

```json
{
  "user_id": "user123",
  "profile": {
    "created_at": "2024-01-01T00:00:00Z",
    "last_active": "2024-01-15T10:25:00Z",
    "tier": "premium",
    "status": "active"
  },
  "preferences": {
    "default_processing_dimensions": ["logical", "creative"],
    "preferred_squad": "development",
    "confidence_threshold": 0.85,
    "timeout_preference": 5000,
    "language": "en",
    "notification_settings": {
      "low_confidence_alerts": true,
      "processing_complete": false
    }
  },
  "usage_statistics": {
    "total_requests": 1247,
    "requests_this_month": 89,
    "avg_confidence": 0.87,
    "most_common_intents": [
      {"intent": "create", "count": 234, "percentage": 18.8},
      {"intent": "implement", "count": 187, "percentage": 15.0},
      {"intent": "analyze", "count": 156, "percentage": 12.5}
    ],
    "preferred_squads": [
      {"squad": "development", "count": 567, "percentage": 45.5},
      {"squad": "analysis", "count": 234, "percentage": 18.8},
      {"squad": "security", "count": 123, "percentage": 9.9}
    ]
  },
  "session_context": {
    "active_sessions": 2,
    "current_session_id": "session456",
    "session_start": "2024-01-15T09:30:00Z",
    "context_data": {
      "recent_intents": ["create", "implement"],
      "project_context": "web_application",
      "complexity_trend": "increasing"
    }
  },
  "rate_limiting": {
    "current_tier": "premium",
    "requests_remaining_minute": 456,
    "requests_remaining_hour": 4567,
    "requests_remaining_day": 45678,
    "reset_times": {
      "minute": "2024-01-15T10:31:00Z",
      "hour": "2024-01-15T11:00:00Z",
      "day": "2024-01-16T00:00:00Z"
    }
  }
}
```

### GET /metrics

Retrieve real-time system metrics and analytics.

#### Response

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "current_load": {
    "requests_per_second": 23.4,
    "avg_response_time_ms": 234.5,
    "active_sessions": 156,
    "queue_depth": 12
  },
  "confidence_metrics": {
    "avg_confidence": 0.87,
    "high_confidence_rate": 0.73,
    "medium_confidence_rate": 0.15,
    "low_confidence_rate": 0.12,
    "confidence_distribution": {
      "0.9-1.0": 0.45,
      "0.8-0.9": 0.28,
      "0.7-0.8": 0.15,
      "0.6-0.7": 0.08,
      "0.0-0.6": 0.04
    }
  },
  "processing_metrics": {
    "avg_processing_time_ms": 234.5,
    "p95_processing_time_ms": 456.7,
    "p99_processing_time_ms": 789.1,
    "timeout_rate": 0.002,
    "retry_rate": 0.015
  },
  "system_health": {
    "cpu_usage": 0.45,
    "memory_usage": 0.62,
    "disk_usage": 0.23,
    "network_latency_ms": 12.3,
    "database_connections": 85,
    "cache_hit_ratio": 0.89
  },
  "error_metrics": {
    "total_error_rate": 0.012,
    "4xx_error_rate": 0.008,
    "5xx_error_rate": 0.004,
    "timeout_error_rate": 0.002,
    "common_errors": [
      {"code": "INVALID_INPUT", "count": 23, "percentage": 45.1},
      {"code": "RATE_LIMIT_EXCEEDED", "count": 12, "percentage": 23.5},
      {"code": "TIMEOUT", "count": 8, "percentage": 15.7}
    ]
  }
}
```

## Rate Limiting

N.L.D.S. implements intelligent rate limiting based on user tiers:

| Tier | Requests/Minute | Requests/Hour | Requests/Day | Burst Capacity |
|------|-----------------|---------------|--------------|----------------|
| Basic | 100 | 1,000 | 10,000 | 20 |
| Premium | 500 | 5,000 | 50,000 | 100 |
| Enterprise | 1,000 | 10,000 | 100,000 | 200 |
| Unlimited | ∞ | ∞ | ∞ | ∞ |

### Rate Limit Headers

All responses include rate limiting information:

```http
X-RateLimit-Limit-Minute: 100
X-RateLimit-Remaining-Minute: 87
X-RateLimit-Reset-Minute: 2024-01-15T10:31:00Z
X-RateLimit-Limit-Hour: 1000
X-RateLimit-Remaining-Hour: 923
X-RateLimit-Reset-Hour: 2024-01-15T11:00:00Z
```

## Error Handling

### Standard Error Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "problematic_field",
      "provided_value": "invalid_value",
      "expected_format": "expected_format_description"
    },
    "request_id": "req_error_123",
    "timestamp": "2024-01-15T10:30:00Z",
    "documentation_url": "https://docs.jaegis.ai/errors/ERROR_CODE"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_INPUT` | 400 | Request validation failed |
| `AUTHENTICATION_REQUIRED` | 401 | Authentication token missing or invalid |
| `INSUFFICIENT_PERMISSIONS` | 403 | User lacks required permissions |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource does not exist |
| `RATE_LIMIT_EXCEEDED` | 429 | Request rate limit exceeded |
| `PROCESSING_TIMEOUT` | 408 | Request processing timed out |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## Webhooks

Configure webhooks to receive real-time notifications:

### Webhook Events

- `processing_complete`: Processing finished successfully
- `high_confidence_result`: Result with confidence ≥95%
- `low_confidence_result`: Result with confidence <70%
- `processing_error`: Processing failed
- `rate_limit_warning`: Approaching rate limit

### Webhook Payload

```json
{
  "event": "processing_complete",
  "timestamp": "2024-01-15T10:30:00Z",
  "webhook_id": "webhook_abc123",
  "data": {
    "request_id": "req_abc123",
    "user_id": "user123",
    "confidence": 0.89,
    "primary_command": "FRED:IMPLEMENT --component=auth",
    "processing_time_ms": 234.5
  },
  "signature": "sha256=abc123def456..."
}
```

---

**API Version**: 2.2.0  
**Last Updated**: January 15, 2024  
**Support**: api-support@jaegis.ai
