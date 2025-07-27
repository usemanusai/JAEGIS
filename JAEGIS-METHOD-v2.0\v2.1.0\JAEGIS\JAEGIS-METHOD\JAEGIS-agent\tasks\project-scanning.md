# Project Analysis & Scanning Task

## Objective
Automatically analyze a project's codebase to identify technology stack, dependencies, and deployment requirements for cross-platform installer generation.

## Task Overview
This task performs comprehensive project analysis to understand the complete technology ecosystem, dependencies, and configuration requirements needed for successful deployment across multiple platforms.

## Process Steps

### 1. File System Analysis
**Purpose**: Identify project structure and technology indicators

**Actions**:
- Scan root directory for package manager files (package.json, requirements.txt, pom.xml, Cargo.toml, etc.)
- Identify configuration files and their formats (.env, config.yaml, settings.json, etc.)
- Detect framework-specific patterns and directory structures
- Analyze build scripts and automation files (Makefile, build.gradle, webpack.config.js)
- Identify containerization files (Dockerfile, docker-compose.yml, .dockerignore)

**Output**: Technology stack identification with confidence scores

### 2. Dependency Mapping
**Purpose**: Extract and categorize all project dependencies

**Actions**:
- Parse package manager files to extract runtime dependencies
- Identify system-level requirements (Node.js, Python, Java runtime versions)
- Map platform-specific dependency variations (Windows vs Linux package names)
- Analyze transitive dependencies and potential conflicts
- Identify optional vs required dependencies
- Extract version constraints and compatibility requirements

**Output**: Comprehensive dependency tree with platform mappings

### 3. Configuration Discovery
**Purpose**: Identify all configurable parameters and environment requirements

**Actions**:
- Scan for environment variable usage in code and configuration files
- Identify database connections and external service dependencies
- Extract port numbers, file paths, and network configuration
- Discover API keys, credentials, and secret management requirements
- Identify feature flags and conditional configuration options
- Map configuration hierarchies and inheritance patterns

**Output**: Configuration parameter inventory with types and defaults

### 4. Platform Compatibility Assessment
**Purpose**: Evaluate cross-platform deployment feasibility

**Actions**:
- Identify platform-specific code or dependencies
- Assess compatibility with target operating systems
- Flag potential issues with file paths, permissions, or system calls
- Evaluate container vs native deployment options
- Identify architecture-specific requirements (x64, ARM, etc.)
- Assess network and firewall requirements

**Output**: Platform compatibility matrix with risk assessment

### 5. Service & Infrastructure Analysis
**Purpose**: Understand service dependencies and infrastructure requirements

**Actions**:
- Identify database requirements and connection patterns
- Discover external service dependencies (APIs, message queues, etc.)
- Analyze caching requirements (Redis, Memcached, etc.)
- Identify web server and reverse proxy needs
- Discover monitoring and logging requirements
- Assess scaling and load balancing considerations

**Output**: Infrastructure requirements specification

## Validation Criteria

### Completeness Checks
- [ ] All package manager files identified and parsed
- [ ] Technology stack detected with high confidence
- [ ] All dependencies mapped with version requirements
- [ ] Configuration parameters catalogued with types
- [ ] Platform compatibility assessed for all targets

### Accuracy Validation
- [ ] Dependency versions match actual requirements
- [ ] Configuration parameters include all environment variables
- [ ] Platform-specific variations correctly identified
- [ ] Service dependencies accurately mapped
- [ ] Risk assessment reflects actual deployment challenges

### Quality Standards
- [ ] Analysis results are comprehensive and actionable
- [ ] Risk factors are clearly identified and prioritized
- [ ] Platform-specific considerations are documented
- [ ] Configuration options are properly categorized
- [ ] Dependencies include both direct and transitive requirements

## Output Deliverables

### 1. Technology Stack Report
```json
{
  "language": "Node.js",
  "version": ">=18.0.0",
  "framework": "Express",
  "package_manager": "npm",
  "confidence": 0.95
}
```

### 2. Dependency Matrix
```json
{
  "runtime": [
    {
      "name": "express",
      "version": "^4.18.0",
      "platform_specific": {
        "windows": "npm install express",
        "linux": "npm install express",
        "macos": "npm install express"
      }
    }
  ],
  "system": [
    {
      "name": "Node.js",
      "minimum_version": "18.0.0",
      "installation_method": "package_manager"
    }
  ]
}
```

### 3. Configuration Inventory
```json
{
  "parameters": [
    {
      "name": "PORT",
      "type": "integer",
      "description": "Server listening port",
      "default": 3000,
      "required": false,
      "validation": "^[0-9]{1,5}$"
    }
  ]
}
```

### 4. Platform Compatibility Assessment
```json
{
  "platforms": {
    "windows": {
      "compatible": true,
      "issues": [],
      "requirements": ["Node.js 18+", "npm"]
    },
    "linux": {
      "compatible": true,
      "issues": [],
      "requirements": ["Node.js 18+", "npm"]
    },
    "macos": {
      "compatible": true,
      "issues": [],
      "requirements": ["Node.js 18+", "npm"]
    }
  }
}
```

## Integration Points

### Input Sources
- Project codebase and file system
- Package manager configuration files
- Environment and configuration files
- Documentation and README files
- Existing deployment scripts or containers

### Output Consumers
- Manifest Generation task (uses analysis results)
- Script Generation task (uses dependency and platform data)
- Template Management task (uses configuration parameters)
- Quality Validation processes (uses compatibility assessment)

## Error Handling

### Common Issues
- **Incomplete package files**: Handle missing or corrupted package manager files
- **Ambiguous technology stack**: Resolve conflicts when multiple frameworks detected
- **Missing dependencies**: Identify implicit or undeclared dependencies
- **Platform conflicts**: Handle platform-specific code or dependencies
- **Configuration complexity**: Manage complex configuration hierarchies

### Recovery Strategies
- **Fallback detection**: Use multiple detection methods for technology identification
- **User confirmation**: Prompt for clarification on ambiguous results
- **Incremental analysis**: Allow partial results when complete analysis fails
- **Manual override**: Provide mechanisms for user corrections
- **Validation loops**: Re-analyze after user modifications

## Performance Considerations

### Optimization Strategies
- **Parallel scanning**: Analyze multiple file types concurrently
- **Caching**: Cache analysis results for unchanged projects
- **Incremental updates**: Re-analyze only changed components
- **Selective depth**: Limit analysis depth based on project size
- **Pattern matching**: Use efficient regex patterns for file detection

### Resource Management
- **Memory usage**: Stream large files instead of loading entirely
- **File system**: Minimize directory traversal operations
- **Network**: Avoid external API calls during scanning
- **CPU**: Use efficient parsing algorithms
- **Time limits**: Implement timeouts for long-running analysis
