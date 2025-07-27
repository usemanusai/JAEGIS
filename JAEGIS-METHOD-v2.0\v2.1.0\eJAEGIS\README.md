# Jaegis Agent

**Enhanced Multi-agent Architecture & Dependency Specialist**

A perpetual, active background monitor for project codebases that identifies, analyzes, and reports on dependencies affected by code modifications. e.J.A.E.G.I.S. ensures architectural integrity by autonomously creating and assigning tasks to the appropriate agents or human team members responsible for affected code segments.

## 🎯 **Key Features**

✅ **Environment Agnostic**: Operates identically on local machines and remote CI/CD infrastructure  
✅ **Proactive Prevention**: Identifies potential integration conflicts before they become bugs  
✅ **Seamless Integration**: Functions as background process with minimal developer overhead  
✅ **Single Source of Truth**: Version-controlled ownership ledger ensures clear accountability  
✅ **Real-time Monitoring**: Instant detection and analysis of code changes  
✅ **Intelligent Impact Analysis**: LLM-powered semantic analysis of code dependencies  

## 🏗️ **System Architecture**

e.J.A.E.G.I.S. consists of five core, interconnected components:

| Component | Capability | Implementation |
|-----------|------------|----------------|
| **Codebase Knowledge Graph** | Real-time model of project architecture and dependencies | Neo4j graph database or in-memory representation |
| **Ownership Ledger** | Definitive registry mapping code components to owners | Version-controlled `OWNERSHIP_LEDGER.json` file |
| **Active Monitoring Service** | Dual-mode change detection service | File system watcher (local) + webhook service (remote) |
| **Impact Analysis Engine** | Core logic for tracing "ripple effects" of changes | Graph traversal + LLM-powered semantic analysis |
| **Task Dispatch Router** | Central hub for notifications and task routing | Multi-channel notification system (IDE, Slack, email) |

## 🚀 **Quick Start**

### Installation

```bash
# Install e.J.A.E.G.I.S.
pip install eJaegis-agent

# Or install from source
git clone https://github.com/JAEGIS-method/eJaegis-agent.git
cd eJaegis-agent
pip install -e .
```

### Initialize Your Project

```bash
# Navigate to your project root
cd /path/to/your/project

# Initialize e.J.A.E.G.I.S.
eJaegis init

# This will:
# 1. Create .eJaegis/ directory for local storage
# 2. Build initial codebase knowledge graph
# 3. Create template OWNERSHIP_LEDGER.json
# 4. Start file system monitoring
```

### Basic Usage

```bash
# Check e.J.A.E.G.I.S. status
eJaegis status

# Start monitoring (if not already running)
eJaegis monitor

# Analyze dependencies for specific file
eJaegis analyze --file-path src/core/schemas.py

# Configure ownership and notifications
eJaegis configure
```

## 📋 **Configuration**

### Ownership Ledger

e.J.A.E.G.I.S. uses a version-controlled `OWNERSHIP_LEDGER.json` file to map code components to their owners:

```json
{
  "version": "1.0",
  "ownership_entries": [
    {
      "pattern": "src/api/**",
      "owner_type": "agent",
      "owner_id": "API-Agent",
      "contact_method": "ide_notification",
      "priority": 1
    },
    {
      "pattern": "src/core/**",
      "owner_type": "agent",
      "owner_id": "Core-Architecture-Agent", 
      "contact_method": "ide_notification",
      "priority": 1
    },
    {
      "pattern": "tests/**",
      "owner_type": "agent",
      "owner_id": "QA-Agent",
      "contact_method": "ide_notification",
      "priority": 2
    },
    {
      "pattern": "**",
      "owner_type": "human",
      "owner_id": "dev_team_lead",
      "contact_method": "slack",
      "priority": 3
    }
  ]
}
```

### Contact Methods

- **`ide_notification`**: Popup notifications in your IDE
- **`slack`**: Slack channel or DM notifications
- **`email`**: Email notifications
- **`webhook`**: Custom webhook integration

## 🔄 **How It Works**

### 1. **Continuous Monitoring**
e.J.A.E.G.I.S. watches your codebase for changes using efficient file system monitoring.

### 2. **Instant Analysis**
When a file changes, e.J.A.E.G.I.S.:
- Updates the knowledge graph
- Identifies all dependent components
- Analyzes the impact level (low/medium/high/critical)

### 3. **Smart Notifications**
For each affected component, e.J.A.E.G.I.S.:
- Finds the responsible owner from the ledger
- Generates specific, actionable tasks
- Sends notifications via the owner's preferred method

### 4. **Example Workflow**

```
Developer saves src/core/schemas.py
           ↓
e.J.A.E.G.I.S. detects change instantly
           ↓
Analyzes: "User schema modified"
           ↓
Finds dependents: src/api/v1/user_routes.py, src/utils/exporters.py
           ↓
Checks ownership: API-Agent owns user_routes.py
           ↓
Sends notification: "Schema change affects user creation endpoint"
```

## 🛠️ **Advanced Features**

### Neo4j Integration

For large projects, e.J.A.E.G.I.S. can use Neo4j for advanced graph operations:

```bash
# Start Neo4j (Docker)
docker run -p 7474:7474 -p 7687:7687 neo4j:latest

# Initialize with Neo4j
eJaegis init --neo4j-uri bolt://localhost:7687
```

### LLM-Powered Analysis

e.J.A.E.G.I.S. can integrate with LLMs for semantic code analysis:

```bash
# Set up OpenAI API key
export OPENAI_API_KEY="your-api-key"

# Enable LLM analysis
eJaegis configure --enable-llm-analysis
```

### CI/CD Integration

e.J.A.E.G.I.S. works in CI/CD environments via webhooks:

```yaml
# GitHub Actions example
name: e.J.A.E.G.I.S. Analysis
on: [push, pull_request]

jobs:
  eJaegis-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup e.J.A.E.G.I.S.
        run: |
          pip install eJaegis-agent
          eJaegis init
      - name: Analyze Changes
        run: eJaegis analyze
```

## 📊 **Supported Languages**

e.J.A.E.G.I.S. provides intelligent analysis for:

- **Python** (Full AST analysis)
- **JavaScript/TypeScript** (Import/export analysis)
- **Java** (Package and class analysis)
- **C/C++** (Header and include analysis)
- **Go** (Module and package analysis)
- **Rust** (Crate and module analysis)
- **Ruby** (Gem and module analysis)
- **Generic** (Basic file-level tracking)

## 🔧 **IDE Integration**

e.J.A.E.G.I.S. integrates with popular IDEs through Language Server Protocol:

### VS Code
```json
// settings.json
{
  "eJaegis.enableNotifications": true,
  "eJaegis.notificationLevel": "medium"
}
```

### JetBrains IDEs
Install the e.J.A.E.G.I.S. plugin from the marketplace.

### Vim/Neovim
Use the e.J.A.E.G.I.S. LSP client configuration.

## 🚨 **Troubleshooting**

### Common Issues

**e.J.A.E.G.I.S. not detecting changes:**
```bash
# Check if monitoring is running
eJaegis status

# Restart monitoring
eJaegis monitor
```

**Neo4j connection issues:**
```bash
# Check Neo4j status
docker ps | grep neo4j

# Use in-memory mode
eJaegis init --no-neo4j
```

**Permission errors:**
```bash
# Ensure proper file permissions
chmod +x $(which eJaegis)
```

### Debug Mode

```bash
# Enable debug logging
export E-JAEGIS_LOG_LEVEL=DEBUG
eJaegis monitor
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md).

### Development Setup

```bash
# Clone repository
git clone https://github.com/JAEGIS-method/eJaegis-agent.git
cd eJaegis-agent

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy .
```

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 **Links**

- **Documentation**: [JAEGIS-method.com/docs/eJaegis](https://JAEGIS-method.com/docs/eJaegis)
- **JAEGIS Method**: [JAEGIS-method.com](https://JAEGIS-method.com)
- **Issues**: [GitHub Issues](https://github.com/JAEGIS-method/eJaegis-agent/issues)
- **Discord**: [JAEGIS Community](https://discord.gg/JAEGIS-method)

---

**e.J.A.E.G.I.S. - Ensuring your codebase architecture stays intact, one dependency at a time.** 🛡️
