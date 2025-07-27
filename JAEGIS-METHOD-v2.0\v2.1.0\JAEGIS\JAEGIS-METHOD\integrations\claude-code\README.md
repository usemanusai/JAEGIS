# JAEGIS Claude Code Integration

Native integration of the JAEGIS Method with Claude Code for seamless AI-assisted development workflows.

## Overview

This integration provides a Model Context Protocol (MCP) server that enables Claude Code to access the full JAEGIS methodology, including:

- **Interactive Brainstorming**: Psychology-backed ideation sessions
- **PRD Creation**: Collaborative product requirements development
- **Architecture Design**: Technical architecture with AI guidance
- **Development Support**: Code generation and development assistance

## Installation

### Prerequisites

- Python 3.8 or higher
- Claude Code installed and configured
- Terminal access (bash, zsh, PowerShell)

### Install JAEGIS MCP Server

```bash
# Clone the repository
git clone https://github.com/jaegis-method/claude-code-integration.git
cd claude-code-integration

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Configure Claude Code

1. **Start the MCP Server**:
   ```bash
   python jaegis-mcp-server.py server
   ```

2. **Configure Claude Code MCP**:
   Add the following to your Claude Code configuration:
   ```json
   {
     "mcp_servers": {
       "jaegis": {
         "url": "http://localhost:8000/mcp",
         "description": "JAEGIS Method integration"
       }
     }
   }
   ```

3. **Restart Claude Code** to load the new MCP server.

## Usage

### Basic Commands

#### Initialize a New JAEGIS Project
```bash
jaegis init [project-type]
```

**Example**:
```bash
jaegis init web-app
```

This creates a new project structure with:
- Project directories (`docs/`, `brainstorming/`, `architecture/`, `development/`)
- Initial README.md
- JAEGIS workflow configuration

#### Start Brainstorming Session
```bash
jaegis brainstorm [topic]
```

**Example**:
```bash
jaegis brainstorm "mobile app for task management"
```

Features:
- Psychology-backed brainstorming techniques
- Interactive idea development
- Automatic session documentation
- Idea categorization and prioritization

#### Create Product Requirements Document
```bash
jaegis prd [project-name]
```

**Example**:
```bash
jaegis prd task-manager-app
```

Interactive PRD creation with:
- Guided section completion
- Stakeholder analysis
- User story development
- Acceptance criteria definition

#### Design Technical Architecture
```bash
jaegis architecture [project-name]
```

**Example**:
```bash
jaegis architecture task-manager-app
```

Comprehensive architecture design:
- System component analysis
- Technology stack recommendations
- Architecture diagrams (Mermaid)
- Security and scalability considerations

#### Begin Development
```bash
jaegis develop [feature]
```

**Example**:
```bash
jaegis develop "user authentication system"
```

Development assistance:
- Code generation and scaffolding
- Best practices implementation
- Testing framework setup
- Documentation generation

### Advanced Usage

#### Check Project Status
```bash
jaegis status
```

Shows:
- Current project phase
- Completed milestones
- Next recommended actions
- Generated files and artifacts

#### List Available Templates
```bash
jaegis templates [type]
```

**Examples**:
```bash
jaegis templates prd
jaegis templates architecture
jaegis templates all
```

#### Interactive Mode

All commands support interactive mode for guided workflows:

```bash
# Start interactive brainstorming
jaegis brainstorm --interactive

# Create PRD with step-by-step guidance
jaegis prd --interactive --template=comprehensive

# Design architecture with AI assistance
jaegis architecture --interactive --type=microservices
```

## Integration with Claude Code

### Seamless Workflow

1. **Natural Language Commands**: Use natural language to describe what you want to accomplish
2. **File Integration**: Automatically creates and updates project files
3. **Context Awareness**: Maintains project context across sessions
4. **Code Generation**: Generates code based on architecture and requirements

### Example Workflow

```bash
# In Claude Code terminal
$ jaegis init web-app
✓ Project initialized: web-app
✓ Created project structure
✓ Generated README.md

$ jaegis brainstorm "e-commerce platform features"
🧠 Starting brainstorming session...
💡 Generated 15 initial ideas
📝 Created: brainstorming/session_abc123.md

# Claude Code automatically shows the brainstorming file
# Continue with natural language interaction...

$ jaegis prd e-commerce-platform
📋 Starting PRD creation...
❓ Let's define the executive summary. What problem does your e-commerce platform solve?

# Interactive PRD creation continues...
# Files are automatically created and updated
```

### File Management

The integration automatically manages project files:

```
project-name/
├── README.md
├── docs/
│   ├── prd.md
│   └── requirements.md
├── brainstorming/
│   ├── session_001.md
│   └── ideas_summary.md
├── architecture/
│   ├── system_architecture.md
│   ├── api_specification.md
│   └── diagrams/
│       ├── system_overview.mermaid
│       └── data_flow.mermaid
└── development/
    ├── development_plan.md
    ├── coding_standards.md
    └── testing_strategy.md
```

## Configuration

### MCP Server Configuration

Create `config/mcp_config.json`:

```json
{
  "server": {
    "host": "localhost",
    "port": 8000,
    "debug": false
  },
  "jaegis": {
    "default_project_type": "web-app",
    "brainstorming_duration": 30,
    "interactive_mode": true,
    "auto_save": true
  },
  "templates": {
    "prd_template": "comprehensive",
    "architecture_template": "modern_web",
    "development_template": "agile"
  }
}
```

### Claude Code Configuration

Add to your Claude Code settings:

```json
{
  "mcp_servers": {
    "jaegis": {
      "url": "http://localhost:8000/mcp",
      "timeout": 30000,
      "retry_attempts": 3,
      "features": [
        "project_initialization",
        "brainstorming",
        "prd_creation",
        "architecture_design",
        "development_support"
      ]
    }
  },
  "jaegis_preferences": {
    "auto_open_files": true,
    "show_progress": true,
    "enable_notifications": true
  }
}
```

## Troubleshooting

### Common Issues

1. **MCP Server Not Starting**:
   ```bash
   # Check if port is available
   netstat -an | grep 8000
   
   # Start with different port
   python jaegis-mcp-server.py server --port 8001
   ```

2. **Claude Code Not Connecting**:
   - Verify MCP server is running
   - Check Claude Code configuration
   - Restart Claude Code after configuration changes

3. **Permission Errors**:
   ```bash
   # Ensure proper file permissions
   chmod +x jaegis-mcp-server.py
   
   # Check directory permissions
   ls -la project-directory/
   ```

### Debug Mode

Enable debug logging:

```bash
# Start server with debug logging
python jaegis-mcp-server.py server --debug

# Check logs
tail -f logs/jaegis-mcp.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Setup

```bash
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

## License

MIT License - see LICENSE file for details.

## Support

- **Documentation**: https://jaegis-method.com/docs/claude-code
- **Issues**: https://github.com/jaegis-method/claude-code-integration/issues
- **Discord**: https://discord.gg/jaegis-method
- **Email**: support@jaegis-method.com
