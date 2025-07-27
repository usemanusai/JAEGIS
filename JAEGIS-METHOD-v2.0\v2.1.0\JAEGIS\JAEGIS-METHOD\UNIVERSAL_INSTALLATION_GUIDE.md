# eJAEGIS Universal Installation Guide

## 🚀 One-Command Installation

eJAEGIS (Ecosystem for JAEGIS Method AI Development) can be installed with a single command on any platform:

### **Unix/Linux/macOS**
```bash
curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.sh | bash
```

### **Windows PowerShell**
```powershell
powershell -ExecutionPolicy Bypass -c "iwr https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.ps1 | iex"
```

### **Windows Command Prompt**
```cmd
curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.bat -o install-eJAEGIS.bat && install-eJAEGIS.bat
```

## 📋 Prerequisites

### **System Requirements**
- **Python 3.7+** (automatically checked and guided installation)
- **Git** (for repository management)
- **Internet connection** (for GitHub integration)
- **10MB disk space** (for eJAEGIS system files)

### **Supported Platforms**
- ✅ **Windows 10/11** (PowerShell 5.1+, Command Prompt)
- ✅ **macOS 10.15+** (bash, zsh)
- ✅ **Ubuntu 20.04+** (bash)
- ✅ **CentOS/RHEL 8+** (bash)
- ✅ **Debian 10+** (bash)
- ✅ **Arch Linux** (bash)

## 🎯 Installation Process

### **What Happens During Installation**

1. **System Detection**: Automatically detects OS, package manager, and Python installation
2. **Dependency Check**: Verifies and installs required Python packages (`requests`, `psutil`)
3. **eJAEGIS Download**: Clones the complete eJAEGIS system from GitHub
4. **Interactive Setup**: Guides you through configuration with smart defaults
5. **Project Detection**: Automatically detects your project type and optimizes settings
6. **Configuration Generation**: Creates personalized configuration files
7. **Command Setup**: Installs `eJAEGIS` command for easy system management
8. **System Start**: Launches eJAEGIS background monitoring
9. **Verification**: Runs comprehensive tests to ensure everything works

### **Interactive Configuration**

During installation, you'll be prompted for:

- **GitHub Personal Access Token** (with scope validation)
- **Target Repository Name** (with auto-creation option)
- **Sync Frequency** (hourly, 30min, 15min, on-change)
- **Failsafe Sensitivity** (strict, balanced, permissive)

### **Project Type Detection**

eJAEGIS automatically detects and optimizes for:

- **Node.js/JavaScript** (`package.json` detected)
- **Python** (`requirements.txt`, `setup.py`, `pyproject.toml`)
- **Rust** (`Cargo.toml`)
- **Java** (`pom.xml`, `build.gradle`)
- **Go** (`go.mod`)
- **Generic** (fallback for other project types)

## 🔧 Post-Installation

### **Verification**

After installation, verify everything is working:

```bash
# Check system status
eJAEGIS status

# Run comprehensive tests
eJAEGIS test

# View health report
python ~/.eJAEGIS/eJAEGIS-health-monitor.py
```

### **Project Initialization**

Navigate to your project directory and initialize eJAEGIS:

```bash
cd /path/to/your/project
eJAEGIS init
eJAEGIS start
```

### **Essential Commands**

```bash
# System management
eJAEGIS start          # Start background monitoring
eJAEGIS stop           # Stop background monitoring
eJAEGIS restart        # Restart monitoring
eJAEGIS status         # Show system status

# Configuration
eJAEGIS config         # Show current configuration
eJAEGIS config --edit  # Edit configuration interactively

# Troubleshooting
eJAEGIS test           # Run system tests
eJAEGIS help           # Show help information
```

## 🛠️ Advanced Installation Options

### **Custom Installation Directory**

```bash
# Unix/Linux/macOS
export eJAEGIS_INSTALL_DIR="/custom/path"
curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.sh | bash

# Windows PowerShell
$env:eJAEGIS_INSTALL_DIR = "C:\custom\path"
iwr https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.ps1 | iex
```

### **Offline Installation**

1. Download the installer and eJAEGIS repository:
```bash
# Download installer
curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.sh -o install-eJAEGIS.sh

# Download eJAEGIS repository
git clone https://github.com/huggingfacer04/eJAEGIS.git
```

2. Run offline installation:
```bash
chmod +x install-eJAEGIS.sh
eJAEGIS_OFFLINE=true eJAEGIS_REPO_PATH="./eJAEGIS" ./install-eJAEGIS.sh
```

### **Silent Installation**

For automated deployments:

```bash
# Unix/Linux/macOS
export eJAEGIS_GITHUB_TOKEN="your_token_here"
export eJAEGIS_REPO_NAME="your-repo-name"
export eJAEGIS_SYNC_INTERVAL="3600"
export eJAEGIS_FAILSAFE_SENSITIVITY="balanced"
curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.sh | bash -s -- --silent
```

## 🔍 Troubleshooting

### **Common Installation Issues**

**Issue**: Python version too old
```bash
# Solution: Install Python 3.7+
# Ubuntu/Debian: sudo apt-get install python3.8
# CentOS/RHEL: sudo yum install python38
# macOS: brew install python@3.8
# Windows: Download from python.org
```

**Issue**: Permission denied
```bash
# Solution: Check permissions and run as appropriate user
# Don't run as root unless necessary
# Ensure user has write access to installation directory
```

**Issue**: Network connectivity problems
```bash
# Solution: Check firewall and proxy settings
# For corporate networks, configure proxy:
export https_proxy=http://proxy:port
export http_proxy=http://proxy:port
```

**Issue**: Git not found
```bash
# Solution: Install Git
# Ubuntu/Debian: sudo apt-get install git
# CentOS/RHEL: sudo yum install git
# macOS: xcode-select --install
# Windows: Download from git-scm.com
```

### **Verification and Diagnostics**

```bash
# Run comprehensive health check
python ~/.eJAEGIS/eJAEGIS-health-monitor.py

# Run installation verification
python ~/.eJAEGIS/eJAEGIS-installation-verifier.py

# Check system logs
cat ~/.eJAEGIS/logs/eJAEGIS-*.log

# Test GitHub connectivity
python -c "
import requests
token = 'your_token'
r = requests.get('https://api.github.com/user', 
                headers={'Authorization': f'Bearer {token}'})
print(f'Status: {r.status_code}, User: {r.json().get(\"login\", \"Unknown\")}')
"
```

### **Manual Recovery**

If installation fails, you can manually recover:

```bash
# 1. Clean up partial installation
rm -rf ~/.eJAEGIS
rm -f ~/.local/bin/eJAEGIS

# 2. Clear Python cache
python -c "import sys; print(sys.path)" # Check paths
find ~/.local/lib/python*/site-packages -name "*eJAEGIS*" -delete

# 3. Reinstall
curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.sh | bash
```

## 🔄 Updates and Maintenance

### **Updating eJAEGIS**

```bash
# Update to latest version
cd ~/.eJAEGIS
git pull origin main

# Restart services
eJAEGIS restart

# Verify update
eJAEGIS status
```

### **Backup Configuration**

```bash
# Backup configuration
cp -r ~/.eJAEGIS/config ~/.eJAEGIS/config.backup.$(date +%Y%m%d)

# Restore configuration
cp -r ~/.eJAEGIS/config.backup.YYYYMMDD ~/.eJAEGIS/config
```

## 🌐 Integration Examples

### **CI/CD Integration**

**GitHub Actions**:
```yaml
name: eJAEGIS Integration
on: [push, pull_request]
jobs:
  eJAEGIS-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install eJAEGIS
        run: curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.sh | bash
        env:
          eJAEGIS_GITHUB_TOKEN: ${{ secrets.eJAEGIS_TOKEN }}
      - name: Run eJAEGIS Tests
        run: eJAEGIS test
```

### **Docker Integration**

```dockerfile
FROM python:3.9-slim

# Install eJAEGIS
RUN curl -sSL https://raw.githubusercontent.com/huggingfacer04/eJAEGIS/main/install.sh | bash

# Configure eJAEGIS
ENV eJAEGIS_GITHUB_TOKEN=${GITHUB_TOKEN}
ENV eJAEGIS_REPO_NAME=${REPO_NAME}

# Start eJAEGIS
CMD ["eJAEGIS", "start"]
```

## 📞 Support and Resources

### **Getting Help**

- **Documentation**: https://github.com/huggingfacer04/eJAEGIS/wiki
- **Issues**: https://github.com/huggingfacer04/eJAEGIS/issues
- **Discussions**: https://github.com/huggingfacer04/eJAEGIS/discussions

### **Community**

- **Discord**: [eJAEGIS Community Server](https://discord.gg/eJAEGIS)
- **Reddit**: r/eJAEGISDevelopment
- **Stack Overflow**: Tag questions with `eJAEGIS-system`

### **Contributing**

- **Bug Reports**: Use GitHub Issues with detailed reproduction steps
- **Feature Requests**: Use GitHub Discussions for new feature ideas
- **Pull Requests**: Follow the contribution guidelines in CONTRIBUTING.md

## 🎉 Success Indicators

After successful installation, you should see:

- ✅ `eJAEGIS status` shows all systems operational
- ✅ Background runner process active
- ✅ Failsafe systems enabled and monitoring
- ✅ GitHub connectivity verified
- ✅ Project files being monitored
- ✅ Automatic sync to GitHub repository

**Welcome to the eJAEGIS ecosystem! Your development workflow is now protected and automated.** 🚀✨

---

*For the complete eJAEGIS documentation, visit: https://github.com/huggingfacer04/eJAEGIS*
