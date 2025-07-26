# JAEGIS API Documentation

## Overview

JAEGIS provides multiple interfaces for interacting with the AI Agent Intelligence System:

- **HTTP REST API** - Standard web API for integration
- **WebSocket API** - Real-time bidirectional communication
- **CLI Interface** - Command-line tool for direct interaction
- **Node.js SDK** - Programmatic access for Node.js applications

## HTTP REST API

### Base URL
```
http://localhost:3000/api
```

### Authentication
Currently, JAEGIS operates without authentication for development. In production, implement proper authentication mechanisms.

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1640995200000,
  "version": "2.0.0",
  "uptime": 3600
}
```

#### Execute Command
```http
POST /command
```

**Request Body:**
```json
{
  "command": "/help",
  "parameters": {
    "command": "status"
  },
  "context": {
    "user": "user123",
    "format": "json"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "title": "JAEGIS Help System",
    "command": "status",
    "description": "Show system status and health information",
    "usage": "/status",
    "examples": [
      {
        "command": "/status",
        "description": "Show current system status"
      }
    ]
  },
  "requestId": "req_1640995200000_abc123",
  "executionTime": 45,
  "timestamp": 1640995200000
}
```

#### System Status
```http
GET /status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "system": {
      "status": "healthy",
      "uptime": 3600,
      "version": "2.0.0",
      "environment": "production"
    },
    "executor": {
      "plugins_loaded": 12,
      "commands_processed": 1547,
      "active_executions": 3
    },
    "services": {
      "cache": {
        "status": "healthy",
        "hit_rate": "87.3%",
        "keys": 234
      },
      "python_bridge": {
        "status": "healthy",
        "requests": 892
      }
    }
  }
}
```

#### Performance Metrics
```http
GET /metrics
```

**Response:**
```json
{
  "timestamp": 1640995200000,
  "system": {
    "current": {
      "cpu": 23.5,
      "memory": 67.2,
      "load": 0.8,
      "activeRequests": 5
    },
    "totals": {
      "requests": 15847,
      "errors": 23,
      "commands": 12456
    },
    "rates": {
      "requestsPerSecond": 12.3,
      "errorRate": 0.15,
      "successRate": 99.85
    }
  },
  "commands": {
    "help": {
      "totalExecutions": 3421,
      "successRate": "99.9%",
      "averageDuration": 42
    },
    "status": {
      "totalExecutions": 1876,
      "successRate": "100%",
      "averageDuration": 28
    }
  }
}
```

#### Plugin Information
```http
GET /plugins
```

**Response:**
```json
{
  "success": true,
  "data": {
    "loaded": 12,
    "available": [
      {
        "name": "help",
        "description": "Comprehensive help system",
        "version": "2.0.0",
        "status": "active"
      },
      {
        "name": "status",
        "description": "System status monitoring",
        "version": "2.0.0",
        "status": "active"
      }
    ]
  }
}
```

### Error Responses

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "message": "Command not found",
    "type": "NOT_FOUND_ERROR",
    "code": "CMD_404",
    "timestamp": 1640995200000
  },
  "suggestions": [
    "Check command spelling",
    "Use /help to see available commands"
  ],
  "support": {
    "errorId": "err_1640995200000_xyz789",
    "contactInfo": "For support, please provide the error ID"
  }
}
```

## WebSocket API

### Connection
```javascript
const ws = new WebSocket('ws://localhost:3000/ws')
```

### Message Format

**Command Execution:**
```json
{
  "type": "command",
  "id": "unique-request-id",
  "command": "/help",
  "parameters": {
    "command": "status"
  },
  "context": {
    "user": "user123"
  }
}
```

**Response:**
```json
{
  "type": "response",
  "id": "unique-request-id",
  "payload": {
    "success": true,
    "data": { ... },
    "executionTime": 45
  }
}
```

**Real-time Updates:**
```json
{
  "type": "update",
  "category": "system",
  "data": {
    "metric": "cpu",
    "value": 25.3,
    "timestamp": 1640995200000
  }
}
```

## CLI Interface

### Installation
```bash
npm install -g jaegis
```

### Usage

**Interactive Mode:**
```bash
jaegis interactive
```

**Direct Command Execution:**
```bash
jaegis exec "/help"
jaegis exec "/status"
```

**Batch Mode:**
```bash
jaegis batch commands.txt
```

**Configuration:**
```bash
jaegis config show
jaegis config set cache.enabled true
```

## Node.js SDK

### Installation
```bash
npm install jaegis-sdk
```

### Usage

```javascript
const { JAEGISClient } = require('jaegis-sdk')

const client = new JAEGISClient({
  baseURL: 'http://localhost:3000',
  timeout: 30000
})

// Execute command
const result = await client.executeCommand('/help', {
  command: 'status'
})

// Get system status
const status = await client.getStatus()

// Subscribe to real-time updates
client.subscribe('system', (update) => {
  console.log('System update:', update)
})
```

## Response Formats

JAEGIS supports multiple response formats:

### JSON (Default)
```json
{
  "success": true,
  "data": { ... }
}
```

### Text
```
✅ Command executed successfully
Result: System is healthy
```

### Markdown
```markdown
## ✅ Success

**Result:** System is healthy

### Details
- Uptime: 1 hour
- Status: Healthy
```

### HTML
```html
<div class="jaegis-response jaegis-success">
  <div class="success-message">✅ Command executed successfully</div>
  <div class="success-data">...</div>
</div>
```

## Rate Limiting

JAEGIS implements rate limiting to ensure system stability:

- **Default Limit:** 100 requests per minute per IP
- **Burst Limit:** 20 requests per 10 seconds
- **WebSocket:** 50 messages per minute per connection

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995260
```

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `CMD_404` | Command not found | 404 |
| `PARAM_INVALID` | Invalid parameters | 400 |
| `AUTH_REQUIRED` | Authentication required | 401 |
| `RATE_LIMITED` | Rate limit exceeded | 429 |
| `SERVER_ERROR` | Internal server error | 500 |
| `SERVICE_UNAVAILABLE` | Service temporarily unavailable | 503 |

## Performance Considerations

### Caching
- Commands are cached for 5 minutes by default
- Cache hit rate typically >85%
- Use `cache-control: no-cache` header to bypass cache

### Timeouts
- Default command timeout: 30 seconds
- WebSocket ping interval: 30 seconds
- Connection timeout: 60 seconds

### Concurrency
- Maximum concurrent requests: 100
- Maximum WebSocket connections: 1000
- Request queuing when limits exceeded

## Examples

### Basic Command Execution
```bash
curl -X POST http://localhost:3000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "command": "/help",
    "parameters": {
      "command": "status"
    }
  }'
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:3000/ws')

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'command',
    id: 'test-1',
    command: '/status'
  }))
}

ws.onmessage = (event) => {
  const response = JSON.parse(event.data)
  console.log('Response:', response)
}
```

### Node.js Integration
```javascript
const express = require('express')
const { JAEGISClient } = require('jaegis-sdk')

const app = express()
const jaegis = new JAEGISClient()

app.get('/system-status', async (req, res) => {
  try {
    const status = await jaegis.executeCommand('/status')
    res.json(status)
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})
```

## Security

### Input Validation
- All inputs are validated and sanitized
- Command injection protection
- XSS prevention in responses

### CORS
```javascript
// Allowed origins
const allowedOrigins = [
  'http://localhost:3000',
  'https://your-domain.com'
]
```

### Headers
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

## Monitoring

### Health Checks
```bash
# Basic health check
curl http://localhost:3000/health

# Detailed status
curl http://localhost:3000/api/status

# Performance metrics
curl http://localhost:3000/api/metrics
```

### Logging
- All requests are logged with unique IDs
- Error tracking with stack traces
- Performance metrics collection

### Alerts
- CPU usage > 80%
- Memory usage > 80%
- Error rate > 5%
- Response time > 5 seconds

## Troubleshooting

### Common Issues

**Connection Refused:**
```bash
# Check if service is running
curl http://localhost:3000/health
```

**Slow Responses:**
```bash
# Check system metrics
curl http://localhost:3000/api/metrics
```

**Command Not Found:**
```bash
# List available commands
curl -X POST http://localhost:3000/api/command \
  -d '{"command": "/help"}'
```

### Debug Mode
```bash
# Start with debug logging
DEBUG=jaegis:* npm start

# Enable verbose CLI output
jaegis --verbose exec "/status"
```

## Support

For additional support:
- GitHub Issues: https://github.com/usemanusai/JAEGIS/issues
- Documentation: https://github.com/usemanusai/JAEGIS/docs
- Email: use.manus.ai@gmail.com