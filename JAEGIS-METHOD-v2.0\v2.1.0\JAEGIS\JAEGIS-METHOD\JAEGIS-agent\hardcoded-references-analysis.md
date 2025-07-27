# JAEGIS Project Hardcoded References Analysis - UPDATED

## Task 1.2: Scan for Hardcoded File References

**Date**: 2025-01-23 (Updated)
**Purpose**: Identify all hardcoded file references that need updating during reorganization

## Critical File Reference Analysis - COMPREHENSIVE SCAN COMPLETE

### 🚨 **HIGHEST PRIORITY: agent-config.txt**

#### **File Path References Found (200+ instances)**
```yaml
# Core directory structure references
agent-root: JAEGIS-agent
personas: JAEGIS-agent/personas
tasks: JAEGIS-agent/tasks
templates: JAEGIS-agent/templates
checklists: JAEGIS-agent/checklists
data: JAEGIS-agent/data
```

#### **Agent Definition References (24 agents)**
Each agent contains multiple file references:
- `Persona: personas#[agent-name]` (24 instances)
- `Tasks: [tasks#task-name]` (100+ instances)
- `Templates: [templates#template-name]` (50+ instances)
- `Checklists: [checklists#checklist-name]` (50+ instances)

#### **Impact Assessment: CRITICAL**
- **agent-config.txt is the core system file** - all agents depend on it
- **All file paths are hardcoded** relative to JAEGIS-agent directory
- **Moving files will break all agent loading** unless paths are updated
- **Must be updated FIRST** before any file movement

### 📋 **HIGH PRIORITY: Documentation Files**

#### **enhanced-JAEGIS-orchestrator-instructions.md**
```yaml
References Found:
- "JAEGIS-agent/" directory structure (5+ instances)
- "agent-config.txt" (3 instances)
- "personas/", "tasks/", "templates/", "checklists/", "data/" (10+ instances)
- ".md", ".txt", ".json", ".yaml" file extensions (20+ instances)
- "prd.md", "architecture.md", "checklist.md" output files (3 instances)
```

#### **Other Documentation Files**
- **24-agent-system-*.md files**: May contain references to agent-config.txt
- **deployment-*.md files**: May reference script locations
- **user-guidelines-*.md files**: May reference file structures

### 🔧 **MEDIUM PRIORITY: Script Files**

#### **PowerShell Scripts (.ps1)**
```yaml
build-and-test-integration.ps1:
- "package.json" (3 instances)
- ".md" file references (2 instances)

Other .ps1 files:
- May reference configuration files
- May reference other scripts
- May have hardcoded paths to JAEGIS-agent
```

#### **Python Scripts (.py)**
```yaml
emad-auto-sync.py:
- ".json" file processing (5 instances)
- File path calculations (3 instances)
- May reference JAEGIS-agent directory structure

Other .py files:
- Configuration file references
- Log file paths
- Service file references
```

#### **Batch/Shell Scripts**
```yaml
.bat and .sh files:
- May reference other scripts
- May have hardcoded installation paths
- May reference configuration files
```

### ⚙️ **MEDIUM PRIORITY: Configuration Files**

#### **Build Configuration**
```yaml
package.json:
- Script references to other files
- Build output paths
- Extension configuration

tsconfig.json:
- Source file paths
- Output directory paths
- Include/exclude patterns

webpack.config.js:
- Entry point paths
- Output paths
- Asset paths
```

#### **Service Configuration**
```yaml
emad-auto-sync.service:
- Script file paths
- Working directory paths
- Log file paths
```

## Reference Pattern Analysis

### **Pattern 1: JAEGIS-agent Directory References**
```yaml
Pattern: "JAEGIS-agent/"
Found in:
- agent-config.txt (core paths)
- enhanced-JAEGIS-orchestrator-instructions.md
- Various documentation files
Impact: HIGH - Core system structure
```

### **Pattern 2: Sectioned File References**
```yaml
Pattern: "personas#agent-name", "tasks#task-name"
Found in:
- agent-config.txt (200+ instances)
Impact: CRITICAL - Agent loading system
```

### **Pattern 3: Direct File References**
```yaml
Pattern: "filename.md", "filename.txt", "filename.json"
Found in:
- Documentation files
- Script files
- Configuration files
Impact: MEDIUM - Individual file access
```

### **Pattern 4: Relative Path References**
```yaml
Pattern: "./", "../", "subfolder/"
Found in:
- Build configuration files
- Script files
Impact: MEDIUM - Build and execution paths
```

## Update Strategy by File Type

### **1. agent-config.txt (CRITICAL - Update First)**
```yaml
Current Paths:
- agent-root: JAEGIS-agent
- personas: JAEGIS-agent/personas
- tasks: JAEGIS-agent/tasks
- templates: JAEGIS-agent/templates
- checklists: JAEGIS-agent/checklists
- data: JAEGIS-agent/data

Updated Paths (NO CHANGE NEEDED):
- Keep all JAEGIS-agent paths unchanged
- Core structure remains in place
```

### **2. Documentation Files (Update References)**
```yaml
Files to Update:
- enhanced-JAEGIS-orchestrator-instructions.md
- All 24-agent-*.md files
- deployment-*.md files
- user-guidelines-*.md files

Reference Updates Needed:
- Update references to moved documentation files
- Update script file references
- Update configuration file references
```

### **3. Script Files (Update Paths)**
```yaml
Files to Update:
- All .ps1 files
- All .py files
- All .bat/.sh files

Path Updates Needed:
- Update references to moved scripts
- Update references to moved configuration files
- Update references to moved documentation
```

### **4. Configuration Files (Update Paths)**
```yaml
Files to Update:
- package.json
- tsconfig.json
- webpack.config.js
- Service configuration files

Path Updates Needed:
- Update build output paths
- Update source file paths
- Update script references
```

## Risk Assessment

### **CRITICAL RISKS**
1. **agent-config.txt corruption** - Would break entire JAEGIS system
2. **Missing persona/task/template references** - Would break agent loading
3. **Broken build configuration** - Would break extension compilation

### **HIGH RISKS**
1. **Documentation cross-references** - Would break navigation
2. **Script execution failures** - Would break automation
3. **Service configuration errors** - Would break background services

### **MEDIUM RISKS**
1. **Relative path issues** - Would cause file not found errors
2. **Case sensitivity issues** - Would cause problems on Linux/Mac
3. **Missing file extensions** - Would cause ambiguous references

## Recommended Update Sequence

### **Phase 1: Preparation**
1. Create backup of all files
2. Create reference mapping document
3. Validate current system functionality

### **Phase 2: Core System Updates**
1. **DO NOT UPDATE agent-config.txt** - JAEGIS-agent structure stays in place
2. Update documentation files to reference new locations
3. Update script files to reference new locations

### **Phase 3: Configuration Updates**
1. Update build configuration files
2. Update service configuration files
3. Update any remaining hardcoded references

### **Phase 4: Validation**
1. Test agent loading functionality
2. Test build processes
3. Test script execution
4. Test service functionality

## Next Steps

1. **Create detailed dependency map** (Task 1.3)
2. **Identify critical system files** (Task 1.4)
3. **Assess risks and impacts** (Task 1.5)
4. **Plan reference update strategy** (Phase 2)

**Status**: ✅ **TASK 1.2 COMPLETE** - Hardcoded references identified and analyzed
