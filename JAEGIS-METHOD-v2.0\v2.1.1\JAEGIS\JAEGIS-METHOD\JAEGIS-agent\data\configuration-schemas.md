# Configuration Schemas

## Overview
This data file contains comprehensive schemas and validation rules for configuration parameters that I.S.A.A.C. can detect and manage during installer generation. These schemas ensure proper validation and user guidance for configuration values.

## Parameter Type Schemas

### String Parameters
```json
{
  "string_parameter": {
    "type": "string",
    "validation": {
      "min_length": 1,
      "max_length": 255,
      "pattern": null,
      "allowed_characters": null,
      "forbidden_characters": null,
      "case_sensitive": true,
      "trim_whitespace": true
    },
    "display": {
      "input_type": "text",
      "placeholder": "",
      "help_text": "",
      "mask_input": false
    },
    "examples": [
      {
        "name": "APPLICATION_NAME",
        "description": "Name of the application",
        "default": "MyApp",
        "validation": {
          "min_length": 3,
          "max_length": 50,
          "pattern": "^[a-zA-Z][a-zA-Z0-9_-]*$"
        },
        "help_text": "Enter a name for your application (3-50 characters, alphanumeric, underscore, and dash allowed)"
      },
      {
        "name": "DATABASE_HOST",
        "description": "Database server hostname or IP address",
        "default": "localhost",
        "validation": {
          "pattern": "^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$"
        },
        "help_text": "Enter the hostname or IP address of your database server"
      }
    ]
  }
}
```

### Integer Parameters
```json
{
  "integer_parameter": {
    "type": "integer",
    "validation": {
      "minimum": null,
      "maximum": null,
      "multiple_of": null,
      "exclusive_minimum": false,
      "exclusive_maximum": false
    },
    "display": {
      "input_type": "number",
      "step": 1,
      "placeholder": "",
      "help_text": ""
    },
    "examples": [
      {
        "name": "SERVER_PORT",
        "description": "Port number for the web server",
        "default": 3000,
        "validation": {
          "minimum": 1024,
          "maximum": 65535
        },
        "help_text": "Enter a port number between 1024 and 65535"
      },
      {
        "name": "MAX_CONNECTIONS",
        "description": "Maximum number of concurrent connections",
        "default": 100,
        "validation": {
          "minimum": 1,
          "maximum": 10000,
          "multiple_of": 10
        },
        "help_text": "Maximum concurrent connections (must be a multiple of 10)"
      },
      {
        "name": "TIMEOUT_SECONDS",
        "description": "Request timeout in seconds",
        "default": 30,
        "validation": {
          "minimum": 5,
          "maximum": 300
        },
        "help_text": "Timeout value in seconds (5-300)"
      }
    ]
  }
}
```

### Boolean Parameters
```json
{
  "boolean_parameter": {
    "type": "boolean",
    "validation": {
      "true_values": ["true", "yes", "y", "1", "on", "enable", "enabled"],
      "false_values": ["false", "no", "n", "0", "off", "disable", "disabled"]
    },
    "display": {
      "input_type": "choice",
      "true_label": "Yes",
      "false_label": "No",
      "help_text": ""
    },
    "examples": [
      {
        "name": "ENABLE_SSL",
        "description": "Enable SSL/TLS encryption",
        "default": true,
        "display": {
          "true_label": "Enable SSL",
          "false_label": "Disable SSL"
        },
        "help_text": "Enable SSL/TLS encryption for secure connections"
      },
      {
        "name": "DEBUG_MODE",
        "description": "Enable debug logging",
        "default": false,
        "display": {
          "true_label": "Enable Debug",
          "false_label": "Disable Debug"
        },
        "help_text": "Enable detailed debug logging (not recommended for production)"
      }
    ]
  }
}
```

### Choice Parameters
```json
{
  "choice_parameter": {
    "type": "choice",
    "validation": {
      "choices": [],
      "allow_custom": false,
      "case_sensitive": true
    },
    "display": {
      "input_type": "select",
      "multiple": false,
      "help_text": ""
    },
    "examples": [
      {
        "name": "DATABASE_TYPE",
        "description": "Database system to use",
        "default": "postgresql",
        "validation": {
          "choices": [
            {
              "value": "postgresql",
              "label": "PostgreSQL",
              "description": "Robust relational database with advanced features"
            },
            {
              "value": "mysql",
              "label": "MySQL",
              "description": "Popular open-source relational database"
            },
            {
              "value": "sqlite",
              "label": "SQLite",
              "description": "Lightweight file-based database"
            },
            {
              "value": "mongodb",
              "label": "MongoDB",
              "description": "Document-oriented NoSQL database"
            }
          ]
        },
        "help_text": "Choose the database system for your application"
      },
      {
        "name": "LOG_LEVEL",
        "description": "Logging level",
        "default": "info",
        "validation": {
          "choices": [
            {
              "value": "debug",
              "label": "Debug",
              "description": "Detailed debugging information"
            },
            {
              "value": "info",
              "label": "Info",
              "description": "General information messages"
            },
            {
              "value": "warn",
              "label": "Warning",
              "description": "Warning messages only"
            },
            {
              "value": "error",
              "label": "Error",
              "description": "Error messages only"
            }
          ]
        },
        "help_text": "Set the minimum logging level"
      }
    ]
  }
}
```

### Path Parameters
```json
{
  "path_parameter": {
    "type": "path",
    "validation": {
      "must_exist": false,
      "must_be_directory": false,
      "must_be_file": false,
      "must_be_writable": false,
      "must_be_readable": false,
      "must_be_executable": false,
      "resolve_relative": true,
      "normalize_path": true
    },
    "display": {
      "input_type": "path",
      "browse_button": true,
      "help_text": ""
    },
    "examples": [
      {
        "name": "INSTALL_PATH",
        "description": "Installation directory path",
        "default": {
          "windows": "C:\\Program Files\\MyApp",
          "linux": "/opt/myapp",
          "macos": "/Applications/MyApp"
        },
        "validation": {
          "must_be_directory": true,
          "must_be_writable": true
        },
        "help_text": "Choose the directory where the application will be installed"
      },
      {
        "name": "CONFIG_FILE",
        "description": "Configuration file path",
        "default": {
          "windows": "%APPDATA%\\MyApp\\config.json",
          "linux": "/etc/myapp/config.json",
          "macos": "~/Library/Application Support/MyApp/config.json"
        },
        "validation": {
          "must_be_file": true,
          "must_be_readable": true
        },
        "help_text": "Path to the configuration file"
      }
    ]
  }
}
```

### URL Parameters
```json
{
  "url_parameter": {
    "type": "url",
    "validation": {
      "schemes": ["http", "https"],
      "require_scheme": true,
      "require_host": true,
      "allow_localhost": true,
      "allow_ip_address": true,
      "require_port": false,
      "require_path": false
    },
    "display": {
      "input_type": "url",
      "placeholder": "https://example.com",
      "help_text": ""
    },
    "examples": [
      {
        "name": "API_BASE_URL",
        "description": "Base URL for API endpoints",
        "default": "https://api.example.com",
        "validation": {
          "schemes": ["https"],
          "require_scheme": true,
          "require_host": true
        },
        "help_text": "Enter the base URL for your API (HTTPS required)"
      },
      {
        "name": "WEBHOOK_URL",
        "description": "Webhook callback URL",
        "default": "",
        "validation": {
          "schemes": ["http", "https"],
          "require_scheme": true,
          "allow_localhost": false
        },
        "help_text": "URL where webhook notifications will be sent"
      }
    ]
  }
}
```

### Email Parameters
```json
{
  "email_parameter": {
    "type": "email",
    "validation": {
      "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
      "allow_multiple": false,
      "separator": ",",
      "normalize": true
    },
    "display": {
      "input_type": "email",
      "placeholder": "user@example.com",
      "help_text": ""
    },
    "examples": [
      {
        "name": "ADMIN_EMAIL",
        "description": "Administrator email address",
        "default": "",
        "validation": {
          "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "help_text": "Email address for system administrator notifications"
      },
      {
        "name": "NOTIFICATION_EMAILS",
        "description": "Email addresses for notifications",
        "default": "",
        "validation": {
          "allow_multiple": true,
          "separator": ","
        },
        "help_text": "Comma-separated list of email addresses for notifications"
      }
    ]
  }
}
```

## Common Configuration Patterns

### Database Configuration
```json
{
  "database_configuration": {
    "category": "database",
    "parameters": [
      {
        "name": "DATABASE_TYPE",
        "type": "choice",
        "description": "Database system type",
        "default": "postgresql",
        "choices": ["postgresql", "mysql", "sqlite", "mongodb"],
        "affects": ["DATABASE_HOST", "DATABASE_PORT", "DATABASE_NAME"]
      },
      {
        "name": "DATABASE_HOST",
        "type": "string",
        "description": "Database server hostname",
        "default": "localhost",
        "depends_on": {
          "DATABASE_TYPE": ["postgresql", "mysql", "mongodb"]
        }
      },
      {
        "name": "DATABASE_PORT",
        "type": "integer",
        "description": "Database server port",
        "default": {
          "postgresql": 5432,
          "mysql": 3306,
          "mongodb": 27017
        },
        "validation": {
          "minimum": 1,
          "maximum": 65535
        },
        "depends_on": {
          "DATABASE_TYPE": ["postgresql", "mysql", "mongodb"]
        }
      },
      {
        "name": "DATABASE_NAME",
        "type": "string",
        "description": "Database name",
        "default": "myapp",
        "validation": {
          "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$",
          "min_length": 1,
          "max_length": 63
        }
      },
      {
        "name": "DATABASE_USERNAME",
        "type": "string",
        "description": "Database username",
        "default": "myapp_user",
        "depends_on": {
          "DATABASE_TYPE": ["postgresql", "mysql", "mongodb"]
        }
      },
      {
        "name": "DATABASE_PASSWORD",
        "type": "string",
        "description": "Database password",
        "default": "",
        "display": {
          "mask_input": true
        },
        "depends_on": {
          "DATABASE_TYPE": ["postgresql", "mysql", "mongodb"]
        }
      }
    ]
  }
}
```

### Web Server Configuration
```json
{
  "web_server_configuration": {
    "category": "web_server",
    "parameters": [
      {
        "name": "SERVER_HOST",
        "type": "string",
        "description": "Server bind address",
        "default": "0.0.0.0",
        "validation": {
          "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^localhost$|^0\\.0\\.0\\.0$"
        }
      },
      {
        "name": "SERVER_PORT",
        "type": "integer",
        "description": "Server port number",
        "default": 8080,
        "validation": {
          "minimum": 1024,
          "maximum": 65535
        }
      },
      {
        "name": "ENABLE_HTTPS",
        "type": "boolean",
        "description": "Enable HTTPS",
        "default": false,
        "affects": ["SSL_CERT_PATH", "SSL_KEY_PATH", "HTTPS_PORT"]
      },
      {
        "name": "HTTPS_PORT",
        "type": "integer",
        "description": "HTTPS port number",
        "default": 8443,
        "validation": {
          "minimum": 1024,
          "maximum": 65535
        },
        "depends_on": {
          "ENABLE_HTTPS": true
        }
      },
      {
        "name": "SSL_CERT_PATH",
        "type": "path",
        "description": "SSL certificate file path",
        "default": "",
        "validation": {
          "must_be_file": true,
          "must_be_readable": true
        },
        "depends_on": {
          "ENABLE_HTTPS": true
        }
      },
      {
        "name": "SSL_KEY_PATH",
        "type": "path",
        "description": "SSL private key file path",
        "default": "",
        "validation": {
          "must_be_file": true,
          "must_be_readable": true
        },
        "depends_on": {
          "ENABLE_HTTPS": true
        }
      }
    ]
  }
}
```

### Authentication Configuration
```json
{
  "authentication_configuration": {
    "category": "authentication",
    "parameters": [
      {
        "name": "AUTH_METHOD",
        "type": "choice",
        "description": "Authentication method",
        "default": "local",
        "choices": [
          {
            "value": "local",
            "label": "Local Authentication",
            "description": "Username/password stored locally"
          },
          {
            "value": "ldap",
            "label": "LDAP",
            "description": "Authenticate against LDAP server"
          },
          {
            "value": "oauth2",
            "label": "OAuth 2.0",
            "description": "OAuth 2.0 authentication"
          },
          {
            "value": "saml",
            "label": "SAML",
            "description": "SAML-based authentication"
          }
        ],
        "affects": ["LDAP_SERVER", "OAUTH2_CLIENT_ID", "SAML_IDP_URL"]
      },
      {
        "name": "SESSION_TIMEOUT",
        "type": "integer",
        "description": "Session timeout in minutes",
        "default": 60,
        "validation": {
          "minimum": 5,
          "maximum": 1440
        }
      },
      {
        "name": "LDAP_SERVER",
        "type": "string",
        "description": "LDAP server URL",
        "default": "ldap://localhost:389",
        "validation": {
          "pattern": "^ldaps?://[^\\s]+$"
        },
        "depends_on": {
          "AUTH_METHOD": "ldap"
        }
      },
      {
        "name": "OAUTH2_CLIENT_ID",
        "type": "string",
        "description": "OAuth 2.0 client ID",
        "default": "",
        "depends_on": {
          "AUTH_METHOD": "oauth2"
        }
      },
      {
        "name": "OAUTH2_CLIENT_SECRET",
        "type": "string",
        "description": "OAuth 2.0 client secret",
        "default": "",
        "display": {
          "mask_input": true
        },
        "depends_on": {
          "AUTH_METHOD": "oauth2"
        }
      }
    ]
  }
}
```

### Logging Configuration
```json
{
  "logging_configuration": {
    "category": "logging",
    "parameters": [
      {
        "name": "LOG_LEVEL",
        "type": "choice",
        "description": "Minimum logging level",
        "default": "info",
        "choices": [
          {"value": "debug", "label": "Debug"},
          {"value": "info", "label": "Info"},
          {"value": "warn", "label": "Warning"},
          {"value": "error", "label": "Error"}
        ]
      },
      {
        "name": "LOG_FORMAT",
        "type": "choice",
        "description": "Log output format",
        "default": "text",
        "choices": [
          {"value": "text", "label": "Plain Text"},
          {"value": "json", "label": "JSON"},
          {"value": "structured", "label": "Structured"}
        ]
      },
      {
        "name": "LOG_FILE_PATH",
        "type": "path",
        "description": "Log file path",
        "default": {
          "windows": "%PROGRAMDATA%\\MyApp\\logs\\app.log",
          "linux": "/var/log/myapp/app.log",
          "macos": "/usr/local/var/log/myapp/app.log"
        },
        "validation": {
          "must_be_writable": true
        }
      },
      {
        "name": "LOG_ROTATION",
        "type": "boolean",
        "description": "Enable log rotation",
        "default": true,
        "affects": ["LOG_MAX_SIZE", "LOG_MAX_FILES"]
      },
      {
        "name": "LOG_MAX_SIZE",
        "type": "string",
        "description": "Maximum log file size",
        "default": "100MB",
        "validation": {
          "pattern": "^\\d+[KMGT]?B$"
        },
        "depends_on": {
          "LOG_ROTATION": true
        }
      },
      {
        "name": "LOG_MAX_FILES",
        "type": "integer",
        "description": "Maximum number of log files to keep",
        "default": 10,
        "validation": {
          "minimum": 1,
          "maximum": 100
        },
        "depends_on": {
          "LOG_ROTATION": true
        }
      }
    ]
  }
}
```

## Validation Rules

### Cross-Parameter Validation
```json
{
  "cross_parameter_validation": {
    "rules": [
      {
        "name": "port_uniqueness",
        "description": "Ensure all port numbers are unique",
        "type": "uniqueness",
        "parameters": ["SERVER_PORT", "HTTPS_PORT", "ADMIN_PORT"],
        "error_message": "Port numbers must be unique"
      },
      {
        "name": "ssl_certificate_consistency",
        "description": "SSL certificate and key must both be provided",
        "type": "conditional_required",
        "condition": {
          "ENABLE_HTTPS": true
        },
        "required_parameters": ["SSL_CERT_PATH", "SSL_KEY_PATH"],
        "error_message": "Both SSL certificate and private key are required when HTTPS is enabled"
      },
      {
        "name": "database_connection_validation",
        "description": "Validate database connection parameters",
        "type": "conditional_validation",
        "condition": {
          "DATABASE_TYPE": ["postgresql", "mysql"]
        },
        "validation": {
          "required_parameters": ["DATABASE_HOST", "DATABASE_PORT", "DATABASE_NAME"],
          "test_connection": true
        },
        "error_message": "Database connection parameters are invalid"
      }
    ]
  }
}
```

### Environment-Specific Defaults
```json
{
  "environment_defaults": {
    "development": {
      "DEBUG_MODE": true,
      "LOG_LEVEL": "debug",
      "ENABLE_HTTPS": false,
      "SESSION_TIMEOUT": 1440
    },
    "staging": {
      "DEBUG_MODE": false,
      "LOG_LEVEL": "info",
      "ENABLE_HTTPS": true,
      "SESSION_TIMEOUT": 240
    },
    "production": {
      "DEBUG_MODE": false,
      "LOG_LEVEL": "warn",
      "ENABLE_HTTPS": true,
      "SESSION_TIMEOUT": 60
    }
  }
}
```
