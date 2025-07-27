# Platform Detection Patterns

## Overview
This data file contains comprehensive patterns and heuristics for detecting technology stacks, frameworks, dependencies, and platform requirements from project files. These patterns are used by I.S.A.A.C. during the project scanning phase.

## Language Detection Patterns

### JavaScript/Node.js Detection
```json
{
  "language": "javascript",
  "confidence_base": 0.8,
  "file_patterns": [
    {
      "pattern": "package.json",
      "confidence_boost": 0.9,
      "required_fields": ["name", "version"],
      "framework_indicators": {
        "react": ["react", "react-dom", "react-scripts"],
        "vue": ["vue", "@vue/cli"],
        "angular": ["@angular/core", "@angular/cli"],
        "express": ["express"],
        "next": ["next", "react"]
      }
    },
    {
      "pattern": "package-lock.json",
      "confidence_boost": 0.7
    },
    {
      "pattern": "yarn.lock",
      "confidence_boost": 0.7
    },
    {
      "pattern": "*.js",
      "confidence_boost": 0.3,
      "content_patterns": [
        "require\\(",
        "module\\.exports",
        "import.*from",
        "export.*"
      ]
    },
    {
      "pattern": "*.ts",
      "confidence_boost": 0.4,
      "indicates_typescript": true
    }
  ],
  "version_detection": {
    "source": "package.json",
    "field": "engines.node",
    "fallback": ">=14.0.0"
  }
}
```

### Python Detection
```json
{
  "language": "python",
  "confidence_base": 0.8,
  "file_patterns": [
    {
      "pattern": "requirements.txt",
      "confidence_boost": 0.9,
      "framework_indicators": {
        "django": ["Django", "django"],
        "flask": ["Flask", "flask"],
        "fastapi": ["fastapi", "FastAPI"],
        "pyramid": ["pyramid"]
      }
    },
    {
      "pattern": "Pipfile",
      "confidence_boost": 0.8
    },
    {
      "pattern": "pyproject.toml",
      "confidence_boost": 0.8
    },
    {
      "pattern": "setup.py",
      "confidence_boost": 0.7
    },
    {
      "pattern": "*.py",
      "confidence_boost": 0.4,
      "content_patterns": [
        "import\\s+\\w+",
        "from\\s+\\w+\\s+import",
        "def\\s+\\w+\\(",
        "class\\s+\\w+:"
      ]
    }
  ],
  "version_detection": {
    "source": "runtime.txt",
    "pattern": "python-(\\d+\\.\\d+\\.\\d+)",
    "fallback": ">=3.8"
  }
}
```

### Java Detection
```json
{
  "language": "java",
  "confidence_base": 0.8,
  "file_patterns": [
    {
      "pattern": "pom.xml",
      "confidence_boost": 0.9,
      "framework_indicators": {
        "spring": ["spring-boot-starter", "spring-framework"],
        "spring-boot": ["spring-boot-starter"],
        "hibernate": ["hibernate-core"],
        "struts": ["struts2-core"]
      }
    },
    {
      "pattern": "build.gradle",
      "confidence_boost": 0.9,
      "framework_indicators": {
        "spring": ["org.springframework"],
        "android": ["com.android.application"]
      }
    },
    {
      "pattern": "*.java",
      "confidence_boost": 0.4,
      "content_patterns": [
        "public\\s+class\\s+\\w+",
        "import\\s+java\\.",
        "package\\s+\\w+"
      ]
    }
  ],
  "version_detection": {
    "source": "pom.xml",
    "xpath": "//maven.compiler.source",
    "fallback": "11"
  }
}
```

### .NET Detection
```json
{
  "language": "csharp",
  "confidence_base": 0.8,
  "file_patterns": [
    {
      "pattern": "*.csproj",
      "confidence_boost": 0.9,
      "framework_indicators": {
        "aspnet": ["Microsoft.AspNetCore"],
        "mvc": ["Microsoft.AspNetCore.Mvc"],
        "webapi": ["Microsoft.AspNetCore.WebApi"],
        "blazor": ["Microsoft.AspNetCore.Blazor"]
      }
    },
    {
      "pattern": "*.sln",
      "confidence_boost": 0.8
    },
    {
      "pattern": "packages.config",
      "confidence_boost": 0.7
    },
    {
      "pattern": "*.cs",
      "confidence_boost": 0.4,
      "content_patterns": [
        "using\\s+System",
        "namespace\\s+\\w+",
        "public\\s+class\\s+\\w+"
      ]
    }
  ],
  "version_detection": {
    "source": "*.csproj",
    "xpath": "//TargetFramework",
    "fallback": "net6.0"
  }
}
```

## Framework Detection Patterns

### Web Frameworks
```json
{
  "web_frameworks": {
    "react": {
      "detection_patterns": [
        {
          "file": "package.json",
          "dependencies": ["react", "react-dom"],
          "confidence": 0.9
        },
        {
          "file": "*.jsx",
          "content": "import.*React",
          "confidence": 0.8
        }
      ],
      "version_source": "package.json",
      "build_tools": ["webpack", "create-react-app", "vite"],
      "typical_structure": [
        "src/",
        "public/",
        "package.json"
      ]
    },
    "vue": {
      "detection_patterns": [
        {
          "file": "package.json",
          "dependencies": ["vue"],
          "confidence": 0.9
        },
        {
          "file": "*.vue",
          "content": "<template>",
          "confidence": 0.9
        }
      ],
      "version_source": "package.json",
      "build_tools": ["vue-cli", "vite", "webpack"],
      "typical_structure": [
        "src/",
        "public/",
        "vue.config.js"
      ]
    },
    "angular": {
      "detection_patterns": [
        {
          "file": "package.json",
          "dependencies": ["@angular/core"],
          "confidence": 0.9
        },
        {
          "file": "angular.json",
          "confidence": 0.95
        }
      ],
      "version_source": "package.json",
      "build_tools": ["@angular/cli", "webpack"],
      "typical_structure": [
        "src/app/",
        "angular.json",
        "tsconfig.json"
      ]
    }
  }
}
```

### Backend Frameworks
```json
{
  "backend_frameworks": {
    "express": {
      "detection_patterns": [
        {
          "file": "package.json",
          "dependencies": ["express"],
          "confidence": 0.9
        },
        {
          "file": "*.js",
          "content": "require\\(['\"]express['\"]\\)",
          "confidence": 0.8
        }
      ],
      "typical_dependencies": ["body-parser", "cors", "helmet"],
      "port_patterns": ["process.env.PORT", "3000", "8000"]
    },
    "django": {
      "detection_patterns": [
        {
          "file": "requirements.txt",
          "content": "Django",
          "confidence": 0.9
        },
        {
          "file": "manage.py",
          "confidence": 0.95
        },
        {
          "file": "settings.py",
          "content": "DJANGO_SETTINGS_MODULE",
          "confidence": 0.8
        }
      ],
      "typical_structure": [
        "manage.py",
        "*/settings.py",
        "*/urls.py"
      ]
    },
    "flask": {
      "detection_patterns": [
        {
          "file": "requirements.txt",
          "content": "Flask",
          "confidence": 0.9
        },
        {
          "file": "*.py",
          "content": "from flask import",
          "confidence": 0.8
        }
      ],
      "typical_dependencies": ["Jinja2", "Werkzeug", "click"]
    }
  }
}
```

## Database Detection Patterns

### Database Systems
```json
{
  "databases": {
    "postgresql": {
      "detection_patterns": [
        {
          "file": "requirements.txt",
          "content": "psycopg2|PostgreSQL",
          "confidence": 0.8
        },
        {
          "file": "package.json",
          "dependencies": ["pg", "postgres"],
          "confidence": 0.8
        },
        {
          "environment_variables": ["DATABASE_URL", "POSTGRES_URL"],
          "confidence": 0.7
        }
      ],
      "connection_patterns": [
        "postgresql://",
        "postgres://",
        "psql://"
      ],
      "default_port": 5432
    },
    "mysql": {
      "detection_patterns": [
        {
          "file": "requirements.txt",
          "content": "mysql|MySQL",
          "confidence": 0.8
        },
        {
          "file": "package.json",
          "dependencies": ["mysql", "mysql2"],
          "confidence": 0.8
        }
      ],
      "connection_patterns": [
        "mysql://",
        "mysql2://"
      ],
      "default_port": 3306
    },
    "mongodb": {
      "detection_patterns": [
        {
          "file": "requirements.txt",
          "content": "pymongo|mongoengine",
          "confidence": 0.8
        },
        {
          "file": "package.json",
          "dependencies": ["mongodb", "mongoose"],
          "confidence": 0.8
        }
      ],
      "connection_patterns": [
        "mongodb://",
        "mongodb+srv://"
      ],
      "default_port": 27017
    }
  }
}
```

## Build System Detection

### Build Tools
```json
{
  "build_systems": {
    "webpack": {
      "detection_patterns": [
        {
          "file": "webpack.config.js",
          "confidence": 0.95
        },
        {
          "file": "package.json",
          "dependencies": ["webpack"],
          "confidence": 0.8
        }
      ],
      "config_files": [
        "webpack.config.js",
        "webpack.dev.js",
        "webpack.prod.js"
      ]
    },
    "vite": {
      "detection_patterns": [
        {
          "file": "vite.config.js",
          "confidence": 0.95
        },
        {
          "file": "package.json",
          "dependencies": ["vite"],
          "confidence": 0.8
        }
      ]
    },
    "gradle": {
      "detection_patterns": [
        {
          "file": "build.gradle",
          "confidence": 0.95
        },
        {
          "file": "gradlew",
          "confidence": 0.9
        }
      ]
    },
    "maven": {
      "detection_patterns": [
        {
          "file": "pom.xml",
          "confidence": 0.95
        },
        {
          "file": "mvnw",
          "confidence": 0.9
        }
      ]
    }
  }
}
```

## Container Detection Patterns

### Containerization
```json
{
  "containerization": {
    "docker": {
      "detection_patterns": [
        {
          "file": "Dockerfile",
          "confidence": 0.95
        },
        {
          "file": "docker-compose.yml",
          "confidence": 0.9
        },
        {
          "file": ".dockerignore",
          "confidence": 0.7
        }
      ],
      "base_image_patterns": [
        "FROM node:",
        "FROM python:",
        "FROM openjdk:",
        "FROM nginx:",
        "FROM alpine:"
      ]
    },
    "kubernetes": {
      "detection_patterns": [
        {
          "file": "*.yaml",
          "content": "apiVersion.*apps/v1",
          "confidence": 0.8
        },
        {
          "file": "k8s/",
          "confidence": 0.7
        },
        {
          "file": "helm/",
          "confidence": 0.8
        }
      ]
    }
  }
}
```

## Environment Detection Patterns

### Development Environment
```json
{
  "development_environment": {
    "environment_files": [
      {
        "pattern": ".env",
        "confidence": 0.8,
        "variable_patterns": [
          "DATABASE_URL=",
          "API_KEY=",
          "SECRET_KEY=",
          "PORT="
        ]
      },
      {
        "pattern": ".env.example",
        "confidence": 0.6
      },
      {
        "pattern": "config.json",
        "confidence": 0.5
      }
    ],
    "configuration_patterns": {
      "database_config": [
        "DATABASE_URL",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
      ],
      "api_config": [
        "API_KEY",
        "API_SECRET",
        "API_URL",
        "API_VERSION"
      ],
      "server_config": [
        "PORT",
        "HOST",
        "SERVER_NAME",
        "BASE_URL"
      ]
    }
  }
}
```

## Testing Framework Detection

### Testing Tools
```json
{
  "testing_frameworks": {
    "jest": {
      "detection_patterns": [
        {
          "file": "package.json",
          "dependencies": ["jest"],
          "confidence": 0.9
        },
        {
          "file": "jest.config.js",
          "confidence": 0.95
        }
      ]
    },
    "pytest": {
      "detection_patterns": [
        {
          "file": "requirements.txt",
          "content": "pytest",
          "confidence": 0.9
        },
        {
          "file": "pytest.ini",
          "confidence": 0.95
        }
      ]
    },
    "junit": {
      "detection_patterns": [
        {
          "file": "pom.xml",
          "content": "junit",
          "confidence": 0.8
        },
        {
          "file": "build.gradle",
          "content": "junit",
          "confidence": 0.8
        }
      ]
    }
  }
}
```

## Platform-Specific Patterns

### Operating System Indicators
```json
{
  "platform_indicators": {
    "windows_specific": [
      {
        "pattern": "*.bat",
        "confidence": 0.6
      },
      {
        "pattern": "*.ps1",
        "confidence": 0.7
      },
      {
        "content": "CRLF line endings",
        "confidence": 0.3
      }
    ],
    "linux_specific": [
      {
        "pattern": "*.sh",
        "confidence": 0.6
      },
      {
        "pattern": "Makefile",
        "confidence": 0.5
      },
      {
        "content": "#!/bin/bash",
        "confidence": 0.7
      }
    ],
    "macos_specific": [
      {
        "pattern": "*.app/",
        "confidence": 0.8
      },
      {
        "pattern": "Brewfile",
        "confidence": 0.9
      }
    ]
  }
}
```

## Confidence Scoring Algorithm

### Scoring Rules
```json
{
  "confidence_calculation": {
    "base_confidence": 0.5,
    "file_existence_boost": 0.3,
    "content_match_boost": 0.2,
    "multiple_indicators_multiplier": 1.2,
    "conflicting_indicators_penalty": 0.8,
    "minimum_confidence_threshold": 0.6,
    "maximum_confidence_cap": 0.95,
    "scoring_weights": {
      "primary_indicators": 1.0,
      "secondary_indicators": 0.7,
      "tertiary_indicators": 0.4,
      "negative_indicators": -0.3
    }
  }
}
```

## Pattern Matching Configuration

### Matching Rules
```json
{
  "pattern_matching": {
    "case_sensitive": false,
    "regex_enabled": true,
    "glob_patterns": true,
    "content_sampling": {
      "max_file_size": "1MB",
      "sample_lines": 100,
      "encoding": "utf-8"
    },
    "exclusion_patterns": [
      "node_modules/",
      ".git/",
      "*.log",
      "*.tmp",
      "dist/",
      "build/"
    ]
  }
}
```
