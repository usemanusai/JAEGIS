# 🤝 **Contributing to JAEGIS**

Thank you for your interest in contributing to JAEGIS (Just Another Enhanced General Intelligence System)! We welcome contributions from developers, researchers, and AI enthusiasts worldwide.

## 📋 **Table of Contents**

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Types](#contribution-types)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## 📜 **Code of Conduct**

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@jaegis.ai](mailto:conduct@jaegis.ai).

## 🚀 **Getting Started**

### **Prerequisites**
- **Git**: Version control system
- **Python 3.8+** or **Node.js 16+**: Runtime environment
- **GitHub Account**: For submitting contributions
- **Basic Understanding**: AI agents, multi-agent systems, or software architecture

### **First Steps**
1. **Fork the Repository**: Click the "Fork" button on GitHub
2. **Clone Your Fork**: `git clone https://github.com/yourusername/JAEGIS.git`
3. **Read Documentation**: Familiarize yourself with the [Architecture Guide](docs/architecture.md)
4. **Join Discussions**: Participate in [GitHub Discussions](https://github.com/usemanusai/JAEGIS/discussions)

## 🛠️ **Development Setup**

### **Local Environment Setup**

```bash
# Clone your fork
git clone https://github.com/yourusername/JAEGIS.git
cd JAEGIS

# Create virtual environment (Python)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# OR for Node.js
npm install
npm install --save-dev

# Initialize development environment
python scripts/setup-dev.py
# OR
npm run setup:dev
```

### **Configuration**

```bash
# Copy example configuration
cp config/example.json config/local.json

# Set up environment variables
cp .env.example .env
# Edit .env with your settings
```

### **Verify Setup**

```bash
# Run tests
pytest tests/
# OR
npm test

# Run linting
flake8 src/
black src/
# OR
npm run lint

# Start development server
python jaegis.py --dev
# OR
npm run dev
```

## 🎯 **Contribution Types**

### **🐛 Bug Reports**
Help us improve by reporting bugs:
- Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include system information and reproduction steps
- Provide logs and error messages
- Test with the latest version

### **✨ Feature Requests**
Suggest new capabilities:
- Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case and benefits
- Consider implementation complexity
- Discuss in [GitHub Discussions](https://github.com/usemanusai/JAEGIS/discussions) first

### **🔧 Code Contributions**
Submit code improvements:
- **Bug Fixes**: Address reported issues
- **New Features**: Implement approved feature requests
- **Performance**: Optimize existing functionality
- **Refactoring**: Improve code quality and structure

### **📚 Documentation**
Improve our documentation:
- **API Documentation**: Update method descriptions
- **User Guides**: Enhance usage instructions
- **Architecture Docs**: Clarify system design
- **Examples**: Add code examples and tutorials

### **🧪 Testing**
Enhance our test coverage:
- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **Performance Tests**: Benchmark system performance
- **End-to-End Tests**: Test complete workflows

## 🔄 **Development Workflow**

### **Branch Strategy**
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Create bugfix branch
git checkout -b bugfix/issue-number-description

# Create documentation branch
git checkout -b docs/documentation-improvement
```

### **Commit Guidelines**
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Feature
git commit -m "feat: add GARAS squad gap detection capability"

# Bug fix
git commit -m "fix: resolve agent coordination timeout issue"

# Documentation
git commit -m "docs: update API reference for squad management"

# Performance
git commit -m "perf: optimize agent communication protocols"

# Refactor
git commit -m "refactor: restructure squad activation logic"
```

### **Development Process**
1. **Create Issue**: Discuss changes before implementation
2. **Create Branch**: Use descriptive branch names
3. **Implement Changes**: Follow code standards
4. **Write Tests**: Ensure adequate test coverage
5. **Update Documentation**: Keep docs current
6. **Submit PR**: Use the pull request template

## 📏 **Code Standards**

### **Python Standards**
```python
# Use type hints
def activate_squad(squad_name: str) -> bool:
    """Activate a specific squad by name."""
    pass

# Follow PEP 8
class JAEGISOrchestrator:
    """Main orchestrator for JAEGIS agent system."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._agents = {}

# Use docstrings
def coordinate_agents(self, agents: List[Agent]) -> CoordinationResult:
    """
    Coordinate multiple agents for task execution.
    
    Args:
        agents: List of agents to coordinate
        
    Returns:
        CoordinationResult with execution status and metrics
        
    Raises:
        CoordinationError: If agent coordination fails
    """
    pass
```

### **JavaScript/TypeScript Standards**
```typescript
// Use TypeScript for type safety
interface SquadConfig {
  name: string;
  agents: Agent[];
  priority: number;
}

// Use async/await
async function activateSquad(config: SquadConfig): Promise<boolean> {
  try {
    const result = await squadManager.activate(config);
    return result.success;
  } catch (error) {
    logger.error('Squad activation failed', error);
    throw error;
  }
}

// Use JSDoc for documentation
/**
 * Coordinates multiple agents for task execution
 * @param agents - Array of agents to coordinate
 * @returns Promise resolving to coordination result
 */
async function coordinateAgents(agents: Agent[]): Promise<CoordinationResult> {
  // Implementation
}
```

### **General Standards**
- **Naming**: Use descriptive, meaningful names
- **Comments**: Explain complex logic and business rules
- **Error Handling**: Implement comprehensive error handling
- **Logging**: Use structured logging with appropriate levels
- **Security**: Follow security best practices

## 🧪 **Testing Guidelines**

### **Test Structure**
```python
# Unit test example
class TestSquadActivation:
    def test_activate_valid_squad(self):
        """Test successful squad activation."""
        orchestrator = JAEGISOrchestrator()
        result = orchestrator.activate_squad("development")
        assert result is True
        
    def test_activate_invalid_squad(self):
        """Test squad activation with invalid name."""
        orchestrator = JAEGISOrchestrator()
        with pytest.raises(SquadNotFoundError):
            orchestrator.activate_squad("nonexistent")
```

### **Test Coverage**
- **Minimum Coverage**: 80% for new code
- **Critical Paths**: 100% coverage for core functionality
- **Edge Cases**: Test error conditions and edge cases
- **Integration**: Test component interactions

### **Running Tests**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_squad_management.py

# Run with coverage
pytest --cov=src tests/

# Run integration tests
pytest tests/integration/

# Run performance tests
pytest tests/performance/ --benchmark-only
```

## 📚 **Documentation**

### **Documentation Types**
- **API Documentation**: Auto-generated from code comments
- **User Guides**: Step-by-step instructions
- **Architecture Docs**: System design and patterns
- **Examples**: Code examples and tutorials

### **Documentation Standards**
- **Clear Language**: Use simple, clear language
- **Code Examples**: Include working code examples
- **Screenshots**: Add visual aids where helpful
- **Links**: Cross-reference related documentation

### **Building Documentation**
```bash
# Build API documentation
sphinx-build -b html docs/ docs/_build/

# Serve documentation locally
mkdocs serve

# Check documentation links
linkchecker docs/
```

## 🔄 **Pull Request Process**

### **Before Submitting**
- [ ] **Tests Pass**: All tests pass locally
- [ ] **Linting**: Code passes linting checks
- [ ] **Documentation**: Documentation is updated
- [ ] **Changelog**: Update CHANGELOG.md if applicable
- [ ] **Rebase**: Rebase on latest main branch

### **PR Template**
Use the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md):

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### **Review Process**
1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers review code and provide feedback
3. **Discussion**: Address feedback and make necessary changes
4. **Approval**: Maintainer approves the PR
5. **Merge**: PR is merged into main branch

## 👥 **Community**

### **Communication Channels**
- **GitHub Discussions**: [General discussions](https://github.com/usemanusai/JAEGIS/discussions)
- **Issues**: [Bug reports and feature requests](https://github.com/usemanusai/JAEGIS/issues)
- **Email**: [development@jaegis.ai](mailto:development@jaegis.ai)

### **Getting Help**
- **Documentation**: Check [docs.jaegis.ai](https://docs.jaegis.ai)
- **FAQ**: See [Frequently Asked Questions](docs/faq.md)
- **Examples**: Browse [examples directory](examples/)
- **Discussions**: Ask in GitHub Discussions

### **Recognition**
Contributors are recognized in:
- **Contributors List**: Listed in README.md
- **Release Notes**: Mentioned in release announcements
- **Hall of Fame**: Featured on project website

## 📄 **License**

By contributing to JAEGIS, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

## 🙏 **Thank You**

Thank you for contributing to JAEGIS! Your contributions help make AI agent orchestration more accessible and powerful for everyone.

**Questions?** Feel free to reach out in [GitHub Discussions](https://github.com/usemanusai/JAEGIS/discussions) or email [development@jaegis.ai](mailto:development@jaegis.ai).

---

*Last Updated: July 26, 2025*  
*JAEGIS Enhanced Agent System v2.2*
