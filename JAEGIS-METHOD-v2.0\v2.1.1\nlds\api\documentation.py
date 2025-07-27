"""
N.L.D.S. API Documentation
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive OpenAPI 3.0 documentation with interactive Swagger UI,
examples, and detailed API specifications.
"""

from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import FastAPI
from typing import Dict, Any, List
import json


# ============================================================================
# OPENAPI SCHEMA CUSTOMIZATION
# ============================================================================

def create_custom_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """
    Create comprehensive OpenAPI 3.0 schema with detailed documentation.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        Custom OpenAPI schema
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    # Generate base schema
    openapi_schema = get_openapi(
        title="N.L.D.S. API",
        version="2.2.0",
        description=get_api_description(),
        routes=app.routes,
        tags=get_api_tags()
    )
    
    # Add custom components
    openapi_schema["components"] = {
        **openapi_schema.get("components", {}),
        **get_custom_components()
    }
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = get_security_schemes()
    
    # Add servers
    openapi_schema["servers"] = get_api_servers()
    
    # Add examples to paths
    add_examples_to_paths(openapi_schema)
    
    # Add custom extensions
    add_custom_extensions(openapi_schema)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def get_api_description() -> str:
    """Get comprehensive API description."""
    return """
# Natural Language Detection System API

**JAEGIS Enhanced Agent System v2.2 - Tier 0 Component**

## 🚀 Overview

The N.L.D.S. API provides comprehensive natural language processing capabilities for the JAEGIS ecosystem. 
This API serves as the primary interface for converting natural language input into actionable JAEGIS commands 
through advanced multi-dimensional analysis and intelligent enhancement protocols.

## 🎯 Key Features

### 🔧 Core Processing
- **Input Enhancement**: Automatic enhancement via A.M.A.S.I.A.P. Protocol
- **Multi-dimensional Analysis**: Logical, emotional, and creative analysis
- **JAEGIS Translation**: Convert natural language to executable commands
- **Confidence Validation**: Ensure high-quality command generation

### 🌐 Integration Capabilities
- **Real-time Communication**: WebSocket-based messaging
- **OpenRouter.ai**: Access to 3000+ AI models
- **GitHub Integration**: Dynamic resource fetching
- **Error Handling**: Comprehensive fallback mechanisms

### 📊 System Management
- **Health Monitoring**: Real-time system health checks
- **Performance Metrics**: Detailed analytics and monitoring
- **Rate Limiting**: Fair usage enforcement
- **Security**: JWT authentication and authorization

## 🔐 Authentication

All API endpoints require authentication using Bearer tokens:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \\
     -H "Content-Type: application/json" \\
     https://api.nlds.jaegis.ai/process
```

### API Key Types
- **Development Keys**: For testing and development (rate limited)
- **Production Keys**: For production use (higher limits)
- **Admin Keys**: For system administration (unlimited)

## 📈 Rate Limiting

API requests are rate-limited based on your subscription:

| Tier | Requests/Minute | Burst Limit |
|------|----------------|-------------|
| Free | 100 | 200 |
| Pro | 1,000 | 2,000 |
| Enterprise | 10,000 | 20,000 |
| Admin | Unlimited | Unlimited |

Rate limit headers are included in all responses:
- `X-RateLimit-Limit`: Your rate limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset timestamp

## 🔄 Processing Pipeline

The N.L.D.S. processing pipeline consists of several stages:

1. **Input Validation**: Validate and sanitize input
2. **A.M.A.S.I.A.P. Enhancement**: Automatic input enhancement
3. **Multi-dimensional Analysis**: Logical, emotional, creative analysis
4. **JAEGIS Translation**: Generate executable commands
5. **Confidence Validation**: Ensure quality and reliability
6. **Command Submission**: Submit to JAEGIS Master Orchestrator

## 📝 Request/Response Format

All requests and responses use JSON format with UTF-8 encoding.

### Standard Response Structure
```json
{
  "success": true,
  "data": { ... },
  "metadata": {
    "request_id": "req_123456",
    "timestamp": "2025-07-26T12:00:00Z",
    "processing_time_ms": 150.5
  }
}
```

### Error Response Structure
```json
{
  "error": {
    "code": 400,
    "message": "Invalid input parameters",
    "details": { ... },
    "timestamp": "2025-07-26T12:00:00Z",
    "request_id": "req_123456"
  }
}
```

## 🚨 Error Handling

The API uses standard HTTP status codes:

- **200**: Success
- **400**: Bad Request - Invalid parameters
- **401**: Unauthorized - Invalid/missing authentication
- **403**: Forbidden - Insufficient permissions
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - System error
- **503**: Service Unavailable - System maintenance

## 📊 Monitoring & Analytics

### Health Checks
- `GET /health`: Basic health status
- `GET /status`: Comprehensive system status
- `GET /metrics`: Performance metrics

### Request Tracking
Every request includes:
- Unique request ID for tracking
- Processing time measurement
- Component usage tracking
- Error categorization

## 🔧 SDKs & Libraries

Official SDKs are available for:
- **Python**: `pip install nlds-python-sdk`
- **JavaScript/Node.js**: `npm install nlds-js-sdk`
- **Go**: `go get github.com/jaegis/nlds-go-sdk`
- **Java**: Maven/Gradle dependencies available

## 📞 Support

- **Documentation**: https://docs.nlds.jaegis.ai
- **GitHub**: https://github.com/usemanusai/JAEGIS
- **Support Email**: support@jaegis.ai
- **Status Page**: https://status.jaegis.ai

## 📄 License

This API is licensed under the MIT License. See the LICENSE file for details.

---

*Last updated: July 26, 2025*
"""


def get_api_tags() -> List[Dict[str, Any]]:
    """Get API endpoint tags with descriptions."""
    return [
        {
            "name": "Health",
            "description": "Health check and system status endpoints"
        },
        {
            "name": "Processing",
            "description": "Core N.L.D.S. processing endpoints for natural language input"
        },
        {
            "name": "Analysis",
            "description": "Multi-dimensional analysis endpoints (logical, emotional, creative)"
        },
        {
            "name": "Translation",
            "description": "JAEGIS command translation and generation endpoints"
        },
        {
            "name": "JAEGIS",
            "description": "Direct integration with JAEGIS Master Orchestrator"
        },
        {
            "name": "System",
            "description": "System management, metrics, and monitoring endpoints"
        },
        {
            "name": "Admin",
            "description": "Administrative endpoints (admin access required)"
        }
    ]


def get_custom_components() -> Dict[str, Any]:
    """Get custom OpenAPI components."""
    return {
        "examples": {
            "ProcessingRequestExample": {
                "summary": "Standard processing request",
                "description": "Example of a typical processing request",
                "value": {
                    "input_text": "Analyze the current market trends for AI technology and provide recommendations",
                    "mode": "enhanced",
                    "context": {
                        "domain": "technology",
                        "urgency": "medium",
                        "audience": "executives"
                    },
                    "enable_amasiap": True
                }
            },
            "ProcessingResponseExample": {
                "summary": "Successful processing response",
                "description": "Example of a successful processing response",
                "value": {
                    "request_id": "req_20250726_120000_abc123",
                    "success": True,
                    "original_input": "Analyze the current market trends for AI technology",
                    "enhanced_input": "Analyze the current market trends for AI technology [Context: 2025-07-26 12:00:00 UTC] [Domain Context: technology - Consider: frameworks, methodologies, tools] [System: JAEGIS v2.2 | N.L.D.S. Tier 0 | A.M.A.S.I.A.P. Active | Context: 0.8]",
                    "processing_time_ms": 245.7,
                    "confidence_score": 0.92,
                    "components_used": ["amasiap_protocol", "jaegis_interface"],
                    "amasiap_result": {
                        "enhancement_quality_score": 0.95,
                        "research_relevance_score": 0.88,
                        "overall_improvement_score": 0.91
                    },
                    "metadata": {
                        "user_id": "user_001",
                        "timestamp": "2025-07-26T12:00:00Z",
                        "api_version": "2.2.0"
                    }
                }
            },
            "ErrorResponseExample": {
                "summary": "Error response",
                "description": "Example of an error response",
                "value": {
                    "error": {
                        "code": 400,
                        "message": "Input text cannot be empty",
                        "timestamp": "2025-07-26T12:00:00Z",
                        "path": "/process",
                        "request_id": "req_20250726_120000_def456"
                    }
                }
            }
        },
        "headers": {
            "X-Request-ID": {
                "description": "Unique request identifier for tracking",
                "schema": {
                    "type": "string",
                    "example": "req_20250726_120000_abc123"
                }
            },
            "X-Response-Time": {
                "description": "Response time in milliseconds",
                "schema": {
                    "type": "string",
                    "example": "245.7ms"
                }
            },
            "X-RateLimit-Limit": {
                "description": "Rate limit for the user",
                "schema": {
                    "type": "string",
                    "example": "1000"
                }
            },
            "X-RateLimit-Remaining": {
                "description": "Remaining requests in current window",
                "schema": {
                    "type": "string",
                    "example": "999"
                }
            }
        }
    }


def get_security_schemes() -> Dict[str, Any]:
    """Get security schemes for OpenAPI."""
    return {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer token authentication. Include your API token in the Authorization header."
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API Key authentication. Include your API key in the X-API-Key header."
        }
    }


def get_api_servers() -> List[Dict[str, Any]]:
    """Get API server configurations."""
    return [
        {
            "url": "https://api.nlds.jaegis.ai",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.nlds.jaegis.ai",
            "description": "Staging server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        }
    ]


def add_examples_to_paths(openapi_schema: Dict[str, Any]) -> None:
    """Add examples to API paths."""
    paths = openapi_schema.get("paths", {})
    
    # Add examples to /process endpoint
    if "/process" in paths and "post" in paths["/process"]:
        process_post = paths["/process"]["post"]
        
        # Request body examples
        if "requestBody" in process_post:
            process_post["requestBody"]["content"]["application/json"]["examples"] = {
                "standard_request": {
                    "summary": "Standard processing request",
                    "value": {
                        "input_text": "Create a comprehensive analysis of renewable energy trends",
                        "mode": "standard",
                        "enable_amasiap": True
                    }
                },
                "enhanced_request": {
                    "summary": "Enhanced processing with context",
                    "value": {
                        "input_text": "Develop a strategic plan for digital transformation",
                        "mode": "enhanced",
                        "context": {
                            "industry": "healthcare",
                            "timeline": "6 months",
                            "budget": "high"
                        },
                        "user_preferences": {
                            "detail_level": "comprehensive",
                            "format": "executive_summary"
                        }
                    }
                }
            }
        
        # Response examples
        if "responses" in process_post and "200" in process_post["responses"]:
            response_200 = process_post["responses"]["200"]
            if "content" in response_200 and "application/json" in response_200["content"]:
                response_200["content"]["application/json"]["examples"] = {
                    "successful_processing": {
                        "summary": "Successful processing response",
                        "value": {
                            "request_id": "req_20250726_120000_abc123",
                            "success": True,
                            "original_input": "Create a comprehensive analysis of renewable energy trends",
                            "enhanced_input": "Create a comprehensive analysis of renewable energy trends [Context: 2025-07-26 12:00:00 UTC] [Domain Context: technology] [System: JAEGIS v2.2]",
                            "processing_time_ms": 189.3,
                            "confidence_score": 0.94,
                            "components_used": ["amasiap_protocol", "jaegis_interface"],
                            "metadata": {
                                "timestamp": "2025-07-26T12:00:00Z",
                                "api_version": "2.2.0"
                            }
                        }
                    }
                }


def add_custom_extensions(openapi_schema: Dict[str, Any]) -> None:
    """Add custom OpenAPI extensions."""
    # Add custom info extensions
    openapi_schema["info"]["x-logo"] = {
        "url": "https://jaegis.ai/logo.png",
        "altText": "JAEGIS Logo"
    }
    
    openapi_schema["info"]["x-api-id"] = "nlds-api"
    openapi_schema["info"]["x-audience"] = "developers"
    openapi_schema["info"]["x-category"] = "ai-nlp"
    
    # Add rate limiting extension
    openapi_schema["x-rate-limiting"] = {
        "default": {
            "requests": 100,
            "window": "1m"
        },
        "tiers": {
            "free": {"requests": 100, "window": "1m"},
            "pro": {"requests": 1000, "window": "1m"},
            "enterprise": {"requests": 10000, "window": "1m"}
        }
    }
    
    # Add SDK information
    openapi_schema["x-sdks"] = {
        "python": {
            "package": "nlds-python-sdk",
            "version": "2.2.0",
            "repository": "https://github.com/jaegis/nlds-python-sdk"
        },
        "javascript": {
            "package": "nlds-js-sdk",
            "version": "2.2.0",
            "repository": "https://github.com/jaegis/nlds-js-sdk"
        }
    }


# ============================================================================
# CUSTOM DOCUMENTATION PAGES
# ============================================================================

def get_custom_swagger_ui_html(
    openapi_url: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: str = "https://jaegis.ai/favicon.ico"
) -> str:
    """Get custom Swagger UI HTML with enhanced styling."""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <link rel="stylesheet" type="text/css" href="{swagger_css_url}" />
        <link rel="icon" type="image/png" href="{swagger_favicon_url}" sizes="32x32" />
        <style>
            .swagger-ui .topbar {{
                background-color: #1f2937;
                border-bottom: 3px solid #3b82f6;
            }}
            .swagger-ui .topbar .download-url-wrapper .download-url-button {{
                background-color: #3b82f6;
                border-color: #3b82f6;
            }}
            .swagger-ui .info .title {{
                color: #1f2937;
            }}
            .swagger-ui .scheme-container {{
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
            }}
            .swagger-ui .info .description {{
                font-size: 14px;
                line-height: 1.6;
            }}
            .swagger-ui .opblock.opblock-post {{
                border-color: #10b981;
                background: rgba(16, 185, 129, 0.1);
            }}
            .swagger-ui .opblock.opblock-get {{
                border-color: #3b82f6;
                background: rgba(59, 130, 246, 0.1);
            }}
            .swagger-ui .opblock.opblock-put {{
                border-color: #f59e0b;
                background: rgba(245, 158, 11, 0.1);
            }}
            .swagger-ui .opblock.opblock-delete {{
                border-color: #ef4444;
                background: rgba(239, 68, 68, 0.1);
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="{swagger_js_url}"></script>
        <script>
            const ui = SwaggerUIBundle({{
                url: '{openapi_url}',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.presets.standalone
                ],
                layout: "StandaloneLayout",
                deepLinking: true,
                showExtensions: true,
                showCommonExtensions: true,
                defaultModelsExpandDepth: 2,
                defaultModelExpandDepth: 2,
                displayRequestDuration: true,
                tryItOutEnabled: true,
                filter: true,
                supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                onComplete: function() {{
                    console.log("N.L.D.S. API Documentation loaded successfully");
                }},
                requestInterceptor: function(request) {{
                    // Add custom headers or modify requests
                    request.headers['X-API-Client'] = 'swagger-ui';
                    return request;
                }},
                responseInterceptor: function(response) {{
                    // Log response times
                    console.log('Response time:', response.headers['x-response-time']);
                    return response;
                }}
            }});
            
            // Add custom functionality
            window.ui = ui;
        </script>
    </body>
    </html>
    """
    
    return html


def get_custom_redoc_html(
    openapi_url: str,
    title: str,
    redoc_js_url: str = "https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
    redoc_favicon_url: str = "https://jaegis.ai/favicon.ico"
) -> str:
    """Get custom ReDoc HTML with enhanced styling."""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" type="image/png" href="{redoc_favicon_url}" sizes="32x32" />
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
        </style>
    </head>
    <body>
        <redoc spec-url='{openapi_url}' 
               theme='{{
                   "colors": {{
                       "primary": {{
                           "main": "#3b82f6"
                       }}
                   }},
                   "typography": {{
                       "fontSize": "14px",
                       "lineHeight": "1.6em",
                       "code": {{
                           "fontSize": "13px"
                       }},
                       "headings": {{
                           "fontFamily": "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
                           "fontWeight": "600"
                       }}
                   }},
                   "sidebar": {{
                       "backgroundColor": "#f8fafc",
                       "textColor": "#374151"
                   }},
                   "rightPanel": {{
                       "backgroundColor": "#1f2937",
                       "textColor": "#f9fafb"
                   }}
               }}'
               expand-responses="200,201"
               show-extensions="true"
               native-scrollbars="true"
               path-in-middle-panel="true"
               hide-download-button="false">
        </redoc>
        <script src="{redoc_js_url}"></script>
    </body>
    </html>
    """
    
    return html


# ============================================================================
# DOCUMENTATION UTILITIES
# ============================================================================

def generate_api_changelog() -> Dict[str, Any]:
    """Generate API changelog."""
    return {
        "2.2.0": {
            "date": "2025-07-26",
            "changes": [
                "Initial release of N.L.D.S. API",
                "Added comprehensive processing pipeline",
                "Implemented A.M.A.S.I.A.P. Protocol integration",
                "Added JAEGIS Master Orchestrator interface",
                "Implemented multi-dimensional analysis",
                "Added rate limiting and authentication",
                "Comprehensive error handling and fallbacks"
            ],
            "breaking_changes": [],
            "deprecations": []
        }
    }


def generate_api_examples() -> Dict[str, Any]:
    """Generate comprehensive API examples."""
    return {
        "curl_examples": {
            "process_input": """
curl -X POST "https://api.nlds.jaegis.ai/process" \\
     -H "Authorization: Bearer YOUR_API_TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{
       "input_text": "Analyze market trends for renewable energy",
       "mode": "enhanced",
       "enable_amasiap": true
     }'
            """,
            "get_status": """
curl -X GET "https://api.nlds.jaegis.ai/status" \\
     -H "Authorization: Bearer YOUR_API_TOKEN"
            """,
            "submit_command": """
curl -X POST "https://api.nlds.jaegis.ai/jaegis/submit" \\
     -H "Authorization: Bearer YOUR_API_TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{
       "command": {
         "command_type": "analysis",
         "target_squad": "content_squad",
         "parameters": [...]
       },
       "priority": "normal"
     }'
            """
        },
        "python_examples": {
            "basic_usage": """
import requests

# Initialize client
api_token = "YOUR_API_TOKEN"
base_url = "https://api.nlds.jaegis.ai"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Process input
response = requests.post(
    f"{base_url}/process",
    headers=headers,
    json={
        "input_text": "Create a strategic plan for digital transformation",
        "mode": "enhanced",
        "enable_amasiap": True
    }
)

result = response.json()
print(f"Processing successful: {result['success']}")
print(f"Enhanced input: {result['enhanced_input']}")
            """
        }
    }


def get_api_metrics_schema() -> Dict[str, Any]:
    """Get schema for API metrics."""
    return {
        "type": "object",
        "properties": {
            "api": {
                "type": "object",
                "properties": {
                    "total_requests": {"type": "integer"},
                    "successful_requests": {"type": "integer"},
                    "failed_requests": {"type": "integer"},
                    "average_response_time_ms": {"type": "number"},
                    "requests_per_minute": {"type": "number"}
                }
            },
            "processing": {
                "type": "object",
                "properties": {
                    "total_processed": {"type": "integer"},
                    "average_processing_time_ms": {"type": "number"},
                    "confidence_average": {"type": "number"},
                    "enhancement_rate": {"type": "number"}
                }
            },
            "integration": {
                "type": "object",
                "properties": {
                    "jaegis_commands_submitted": {"type": "integer"},
                    "amasiap_enhancements": {"type": "integer"},
                    "openrouter_requests": {"type": "integer"},
                    "github_fetches": {"type": "integer"}
                }
            }
        }
    }
