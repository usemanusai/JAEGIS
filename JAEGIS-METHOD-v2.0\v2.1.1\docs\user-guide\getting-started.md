# N.L.D.S. User Guide - Getting Started

## Welcome to N.L.D.S.

The Natural Language Detection System (N.L.D.S.) is your gateway to the JAEGIS Enhanced Agent System. This guide will help you get started with natural language processing, command generation, and intelligent task automation.

## What is N.L.D.S.?

N.L.D.S. is the Tier 0 component of JAEGIS that transforms natural language input into precise, executable commands. It understands your intent across multiple dimensions and generates optimized instructions for the JAEGIS agent system.

### Key Capabilities

- **Multi-dimensional Analysis**: Logical, emotional, and creative understanding
- **High Confidence Processing**: ≥85% accuracy with alternative interpretations
- **Real-time Processing**: <500ms response time for most requests
- **Intelligent Command Generation**: Automatic JAEGIS command optimization
- **Context Awareness**: Session-based learning and adaptation

## Quick Start

### 1. Authentication Setup

First, obtain your API credentials:

```bash
# Using API Key (Simple)
export NLDS_API_KEY="your-api-key-here"

# Using JWT Token (Recommended)
export NLDS_JWT_TOKEN="your-jwt-token-here"
```

### 2. Your First Request

Try your first N.L.D.S. request:

```bash
curl -X POST "https://api.jaegis.ai/v2/process" \
  -H "Authorization: Bearer $NLDS_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Create a secure user authentication system",
    "user_id": "getting-started-user"
  }'
```

**Response:**
```json
{
  "request_id": "req_abc123",
  "overall_confidence": 0.91,
  "primary_command": {
    "command": "FRED:IMPLEMENT --component=auth --security=high",
    "confidence": 0.91,
    "squad": "development"
  }
}
```

### 3. Understanding the Response

- **`overall_confidence`**: How confident N.L.D.S. is in its understanding (0-1)
- **`primary_command`**: The main JAEGIS command generated
- **`squad`**: Which JAEGIS squad should handle the task
- **`alternative_interpretations`**: Other possible interpretations

## Core Concepts

### Processing Dimensions

N.L.D.S. analyzes your input across three dimensions:

#### Logical Dimension
- Technical requirements and constraints
- System architecture considerations
- Implementation complexity assessment

```json
{
  "processing_dimensions": ["logical"],
  "input_text": "Build a REST API with authentication"
}
```

#### Emotional Dimension
- User sentiment and urgency
- Satisfaction factors and concerns
- Communication tone and style

```json
{
  "processing_dimensions": ["emotional"],
  "input_text": "I urgently need help fixing this critical bug!"
}
```

#### Creative Dimension
- Alternative approaches and solutions
- Innovation opportunities
- Design patterns and best practices

```json
{
  "processing_dimensions": ["creative"],
  "input_text": "Design an innovative user onboarding experience"
}
```

#### All Dimensions (Default)
```json
{
  "processing_dimensions": ["all"],
  "input_text": "Create a user-friendly dashboard"
}
```

### Confidence Levels

N.L.D.S. provides confidence scoring for all interpretations:

| Confidence Range | Level | Action |
|------------------|-------|---------|
| 85-100% | High | Direct execution recommended |
| 70-84% | Medium | Review recommended |
| 50-69% | Low | Clarification needed |
| 0-49% | Very Low | Rephrase required |

### JAEGIS Integration

N.L.D.S. generates commands for different JAEGIS squads:

| Squad | Purpose | Example Commands |
|-------|---------|------------------|
| `development` | Software development | `FRED:IMPLEMENT`, `FRED:BUILD` |
| `analysis` | Research and analysis | `TYLER:ANALYZE`, `TYLER:INVESTIGATE` |
| `security` | Security tasks | `SECURE:PROTECT`, `SECURE:AUDIT` |
| `content` | Documentation | `DOCUMENT:CREATE`, `DOCUMENT:UPDATE` |
| `integration` | System integration | `INTEGRATE:CONNECT`, `INTEGRATE:SYNC` |

## Common Use Cases

### 1. Software Development

**Input:** "Create a microservice for user management with Docker deployment"

**N.L.D.S. Processing:**
```json
{
  "input_text": "Create a microservice for user management with Docker deployment",
  "processing_dimensions": ["logical", "creative"],
  "preferred_squad": "development"
}
```

**Expected Output:**
```json
{
  "primary_command": {
    "command": "FRED:IMPLEMENT --service=user_management --architecture=microservice --deployment=docker",
    "mode": 3,
    "squad": "development"
  },
  "alternative_interpretations": [
    {
      "command": "ARCHITECT:DESIGN --service=user_management --pattern=microservice",
      "reasoning": "Design-first approach for complex microservice"
    }
  ]
}
```

### 2. System Analysis

**Input:** "Analyze database performance and identify slow queries"

**N.L.D.S. Processing:**
```json
{
  "input_text": "Analyze database performance and identify slow queries",
  "processing_dimensions": ["logical"],
  "preferred_squad": "analysis"
}
```

**Expected Output:**
```json
{
  "primary_command": {
    "command": "TYLER:ANALYZE --target=database --metrics=performance --focus=slow_queries",
    "mode": 2,
    "squad": "analysis"
  }
}
```

### 3. Security Assessment

**Input:** "Perform security audit on the authentication system"

**N.L.D.S. Processing:**
```json
{
  "input_text": "Perform security audit on the authentication system",
  "processing_dimensions": ["logical"],
  "preferred_squad": "security"
}
```

**Expected Output:**
```json
{
  "primary_command": {
    "command": "SECURE:AUDIT --component=authentication --scope=comprehensive",
    "mode": 4,
    "squad": "security"
  }
}
```

## Best Practices

### 1. Writing Effective Prompts

**Good Examples:**
- ✅ "Create a REST API for user authentication with JWT tokens"
- ✅ "Analyze system performance metrics and identify bottlenecks"
- ✅ "Deploy the application to production with zero downtime"

**Avoid:**
- ❌ "Do something"
- ❌ "Fix it"
- ❌ "Make it better"

### 2. Providing Context

Include relevant context for better results:

```json
{
  "input_text": "Optimize database queries",
  "context": {
    "database_type": "postgresql",
    "current_performance": "slow",
    "priority": "high",
    "environment": "production"
  }
}
```

### 3. Using Sessions

Maintain context across requests:

```json
{
  "input_text": "Now add rate limiting to the API",
  "session_id": "session_123",
  "user_id": "user_456"
}
```

### 4. Handling Low Confidence

When confidence is low, try:

1. **Add more details**: "Create a secure user authentication system with JWT tokens and role-based access control"
2. **Specify technology**: "Build a Python Flask API with PostgreSQL database"
3. **Include context**: "For a web application with 1000+ users"

## Advanced Features

### Batch Processing

Process multiple requests efficiently:

```json
{
  "inputs": [
    {
      "id": "task_1",
      "text": "Create user authentication system"
    },
    {
      "id": "task_2", 
      "text": "Set up monitoring and logging"
    },
    {
      "id": "task_3",
      "text": "Deploy to production environment"
    }
  ],
  "batch_options": {
    "parallel_processing": true
  }
}
```

### Custom Preferences

Set user preferences for consistent results:

```json
{
  "input_text": "Create a web application",
  "user_preferences": {
    "default_technology": "python",
    "architecture_preference": "microservices",
    "security_level": "high",
    "deployment_target": "cloud"
  }
}
```

### Streaming Responses

For real-time processing updates:

```javascript
const eventSource = new EventSource('/api/v2/stream/process');
eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Processing update:', data);
};
```

## Troubleshooting

### Common Issues

#### Low Confidence Results
**Problem:** Confidence < 70%
**Solution:** 
- Add more specific details
- Include technical requirements
- Provide context information

#### Rate Limiting
**Problem:** 429 Too Many Requests
**Solution:**
- Check your tier limits
- Implement exponential backoff
- Consider upgrading your plan

#### Timeout Errors
**Problem:** Request timeout
**Solution:**
- Simplify complex requests
- Use batch processing for multiple tasks
- Increase timeout settings

### Getting Help

1. **Check Status**: https://status.jaegis.ai
2. **Documentation**: https://docs.jaegis.ai
3. **Support**: support@jaegis.ai
4. **Community**: GitHub Discussions

## Next Steps

1. **Explore SDKs**: Try the [Python SDK](../sdks/python.md) or [JavaScript SDK](../sdks/javascript.md)
2. **Advanced Tutorials**: Learn about [complex workflows](./advanced-workflows.md)
3. **Integration Patterns**: Discover [integration best practices](./integration-patterns.md)
4. **API Reference**: Review the complete [API documentation](../api/api-reference.md)

## Examples Repository

Find more examples in our GitHub repository:
- [Basic Examples](https://github.com/usemanusai/JAEGIS/tree/main/examples/basic)
- [Advanced Use Cases](https://github.com/usemanusai/JAEGIS/tree/main/examples/advanced)
- [Integration Samples](https://github.com/usemanusai/JAEGIS/tree/main/examples/integrations)

---

**Need Help?** Contact our support team at support@jaegis.ai or visit our [community forum](https://github.com/usemanusai/JAEGIS/discussions).
