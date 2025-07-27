# 🚀 JAEGIS Extension Setup & Configuration Guide

## 📋 **Quick Setup Checklist**

### ✅ **1. Icon Setup**
- [ ] Convert `images/jaegis-icon.svg` to PNG format (128x128px)
- [ ] Use any online SVG to PNG converter or image editor
- [ ] Save as `images/jaegis-icon.png`

### ✅ **2. Extension Testing**
Your extension is already compiled and ready! Here's how to test it:

#### **In VS Code Insiders (Extension Development Host):**
1. Press `Ctrl+Shift+P` to open Command Palette
2. Type "JAEGIS" to see all available commands:
   - `JAEGIS: Quick Mode Selection` (Ctrl+Shift+B)
   - `JAEGIS: Activate Documentation Mode`
   - `JAEGIS: Activate Full Development Mode`
   - `JAEGIS: Continue Existing Project`
   - `JAEGIS: Task List Overview`
   - `JAEGIS: Debug & Troubleshoot Mode`
   - `JAEGIS: Continuous Execution Mode`
   - `JAEGIS: Feature Gap Analysis Mode`
   - `JAEGIS: GitHub Integration & Documentation Mode`
   - `JAEGIS: Scan Workspace` (Ctrl+Shift+Alt+S)
   - `JAEGIS: Auto Setup Project` (Ctrl+Shift+Alt+I)

### ✅ **3. Augment Code Integration**

**YES! This extension will work perfectly with Augment Code!** Here's why:

#### **🤝 Compatibility Features:**
- **VS Code Extension**: Works in any VS Code environment including Augment Code
- **Command Palette Integration**: All JAEGIS commands accessible via `Ctrl+Shift+P`
- **Keyboard Shortcuts**: Quick access without interfering with Augment Code
- **Context Menu Integration**: Right-click folder → "Auto Setup Project"
- **Status Bar Integration**: Shows JAEGIS status alongside other extensions

#### **🔄 Workflow Integration:**
1. **Use Augment Code** for your regular AI coding assistance
2. **Use JAEGIS** for:
   - Project planning and documentation
   - AI agent orchestration
   - Architecture design
   - Task breakdown and management
   - Multi-agent collaboration workflows

#### **💡 Recommended Workflow:**
```
1. Open project in VS Code with Augment Code
2. Use JAEGIS: Quick Mode Selection (Ctrl+Shift+B)
3. Choose Documentation Mode for planning
4. Use Augment Code for actual coding
5. Use JAEGIS for project management and orchestration
```

### ✅ **4. Configuration Options**

Access via: `File > Preferences > Settings > Extensions > JAEGIS AI Agent Orchestrator`

**Key Settings:**
- `jaegis.autoInitialize`: Auto-setup JAEGIS in new workspaces (default: true)
- `jaegis.defaultMode`: Default mode for new projects (default: documentation)
- `jaegis.enableRealTimeMonitoring`: Real-time workspace monitoring (default: true)
- `jaegis.statusBarIntegration`: Show status in VS Code status bar (default: true)

### ✅ **5. Publishing Your Extension**

When ready to share:
```bash
# Install VSCE (VS Code Extension Manager)
npm install -g @vscode/vsce

# Package your extension
npm run vsce:package

# This creates: jaegis-vscode-extension-1.0.0.vsix
```

## 🎯 **Testing Commands**

### **Start Here:**
1. `JAEGIS: Quick Mode Selection` - Main entry point
2. `JAEGIS: Scan Workspace` - Analyze current project
3. `JAEGIS: Auto Setup Project` - Initialize JAEGIS structure

### **Documentation Workflow:**
1. `JAEGIS: Activate Documentation Mode`
2. Follow the AI agent prompts
3. Get professional handoff documents

### **Development Workflow:**
1. `JAEGIS: Activate Full Development Mode`
2. Select AI agents for your project
3. Collaborate with AI team

## 🔧 **Troubleshooting**

### **Extension Not Loading:**
- Check VS Code Insiders is running in Extension Development Host mode
- Look for "[Extension Development Host]" in window title
- Check terminal for compilation errors

### **Commands Not Appearing:**
- Press `Ctrl+Shift+P` and type "JAEGIS"
- Check if extension is activated (status bar should show JAEGIS status)
- Try reloading window: `Ctrl+Shift+P` → "Developer: Reload Window"

### **Icon Not Showing:**
- Convert SVG to PNG (128x128px)
- Save as `images/jaegis-icon.png`
- Recompile: `npm run compile`

## 🌟 **Next Steps**

1. **Test all commands** in Extension Development Host
2. **Create the PNG icon** from the provided SVG
3. **Configure settings** to your preferences
4. **Use alongside Augment Code** for enhanced AI development
5. **Package and share** when ready!

---

**🎉 Your JAEGIS extension is ready to revolutionize your AI-assisted development workflow!**
