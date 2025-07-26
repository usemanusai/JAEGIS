# Contributing to JAEGIS

Thank you for your interest in contributing to JAEGIS! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Node.js version, Python version)
   - Error messages and logs

### Submitting Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow the coding standards** outlined below
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

## 🏗️ Development Setup

### Prerequisites

- **Node.js** 18+ 
- **Python** 3.8+
- **Git**

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/JAEGIS.git
cd JAEGIS

# Install dependencies
npm install
pip install -r requirements.txt

# Copy configuration
cp config/config.example.json config/config.json

# Run tests
npm test
python -m pytest

# Start development server
npm run dev
```

## 📋 Coding Standards

### JavaScript/Node.js

- Use **ES6+** features
- Follow **Standard JS** style guide
- Use **meaningful variable names**
- Add **JSDoc comments** for functions
- Maximum line length: **100 characters**

```javascript
/**
 * Process a command and return the result
 * @param {string} command - The command to process
 * @param {Object} options - Processing options
 * @returns {Promise<Object>} Processing result
 */
async function processCommand(command, options = {}) {
  // Implementation
}
```

### Python

- Follow **PEP 8** style guide
- Use **type hints** for function signatures
- Add **docstrings** for classes and functions
- Maximum line length: **88 characters** (Black formatter)

```python
def process_github_content(url: str, cache_duration: int = 3600) -> dict:
    """
    Process GitHub content and return parsed data.
    
    Args:
        url: GitHub raw content URL
        cache_duration: Cache duration in seconds
        
    Returns:
        Parsed content dictionary
    """
    # Implementation
```

### Git Commit Messages

Use **conventional commits** format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Examples:**
```
feat(commands): add new /analytics command
fix(cache): resolve memory leak in cache cleanup
docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Node.js tests
npm test
npm run test:coverage

# Python tests
python -m pytest
python -m pytest --cov=src/python

# Integration tests
npm run test:integration
```

### Writing Tests

- **Unit tests** for individual functions
- **Integration tests** for component interactions
- **End-to-end tests** for complete workflows
- **Minimum 80% code coverage**

### Test Structure

```javascript
// Node.js test example
describe('CommandProcessor', () => {
  describe('processCommand', () => {
    it('should process help command correctly', async () => {
      const result = await processor.processCommand('/help')
      expect(result.success).toBe(true)
      expect(result.data).toContain('Available commands')
    })
  })
})
```

```python
# Python test example
class TestGitHubIntegration:
    def test_fetch_commands_success(self):
        """Test successful command fetching from GitHub."""
        integration = GitHubIntegration()
        result = integration.fetch_commands()
        assert result['success'] is True
        assert 'commands' in result['data']
```

## 📁 Project Structure

```
JAEGIS/
├── src/
│   ├── nodejs/           # Node.js components
│   │   ├── core/         # Core processing logic
│   │   ├── commands/     # Command handlers
│   │   ├── utils/        # Utility functions
│   │   └── tests/        # Node.js tests
│   ├── python/           # Python components
│   │   ├── github/       # GitHub integration
│   │   ├── processing/   # Content processing
│   │   ├── utils/        # Python utilities
│   │   └── tests/        # Python tests
│   └── shared/           # Shared utilities
├── config/               # Configuration files
├── commands/             # Command definitions
├── docs/                 # Documentation
├── examples/             # Usage examples
├── scripts/              # Build/deployment scripts
└── tests/                # Integration tests
```

## 🎯 Areas for Contribution

### High Priority

- **Command processing optimization**
- **GitHub integration improvements**
- **Error handling enhancements**
- **Performance optimizations**
- **Documentation improvements**

### Medium Priority

- **New command implementations**
- **UI/UX improvements**
- **Additional integrations**
- **Monitoring and analytics**
- **Security enhancements**

### Low Priority

- **Code refactoring**
- **Test coverage improvements**
- **Build process optimization**
- **Developer tooling**

## 🐛 Bug Reports

When reporting bugs, include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs **actual behavior**
4. **Environment information**:
   - Operating system
   - Node.js version
   - Python version
   - JAEGIS version
5. **Error messages** and **stack traces**
6. **Screenshots** if applicable

## 💡 Feature Requests

When requesting features:

1. **Describe the use case** and **problem** it solves
2. **Provide examples** of how it would work
3. **Consider implementation complexity**
4. **Check existing issues** for similar requests

## 📖 Documentation

### Types of Documentation

- **API documentation** - JSDoc/Sphinx generated
- **User guides** - Markdown in `/docs`
- **Code comments** - Inline documentation
- **README files** - Component overviews

### Documentation Standards

- Use **clear, concise language**
- Include **code examples**
- Provide **step-by-step instructions**
- Keep documentation **up-to-date**

## 🔄 Release Process

### Version Numbering

We use **Semantic Versioning** (SemVer):
- **MAJOR.MINOR.PATCH**
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Update documentation
5. Create release notes
6. Tag release in Git
7. Publish to npm/PyPI

## 🏆 Recognition

Contributors will be:
- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Credited in documentation**

## 📞 Getting Help

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Discord** - Real-time chat and support
- **Email** - use.manus.ai@gmail.com

## 📄 License

By contributing to JAEGIS, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to JAEGIS! 🚀**