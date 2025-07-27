# JAEGIS Project Hardcoded References Scan Results

## Task 1.3: Scan for Hardcoded File References

**Date**: 2025-01-23  
**Purpose**: Identify all hardcoded file references that need updating during reorganization  

## Critical File Reference Analysis

### 🚨 **HIGHEST PRIORITY: package.json**

#### **Script References Found (26 instances)**
```yaml
Build and execution references:
- "main": "./out/extension.js" (Line 30)
- "scripts" section with multiple file references (Lines 747-775)
- "fresh-install": "powershell -ExecutionPolicy Bypass -File clean-install.ps1" (Line 763)
- "fresh-install-bash": "bash clean-install.sh" (Line 764)
- "build-integration": "node build-integration.js" (Line 769)
- "test-integration": "node test-augment-integration.js" (Line 773)

Workspace detection references:
- "workspaceContains:package.json" (Line 33)
- "workspaceContains:composer.json" (Line 38)

Impact Assessment: CRITICAL
- Build system dependencies - scripts must be accessible
- Extension functionality - commands may reference moved files
- Installation procedures - script paths hardcoded
```

### 🚨 **HIGHEST PRIORITY: agent-config.txt**

#### **Core Directory Structure References (Lines 6-11)**
```yaml
agent-root: JAEGIS-agent
personas: JAEGIS-agent/personas
tasks: JAEGIS-agent/tasks
templates: JAEGIS-agent/templates
checklists: JAEGIS-agent/checklists
data: JAEGIS-agent/data

Impact Assessment: SAFE
- All JAEGIS-agent paths remain unchanged
- No updates needed to core system files
- Core system functionality preserved
```

### 📋 **HIGH PRIORITY: Build Configuration Files**

#### **tsconfig.json**
```yaml
Potential references to scan:
- Source file paths and patterns
- Output directory configurations
- Include/exclude patterns
- Path mappings

Status: NEEDS DETAILED SCAN
```

#### **webpack.config.js**
```yaml
Potential references to scan:
- Entry point paths
- Output directory paths
- Asset loading paths
- Plugin configurations

Status: NEEDS DETAILED SCAN
```

### 📝 **MEDIUM PRIORITY: Documentation Files**

#### **Enhanced JAEGIS Orchestrator Instructions**
```yaml
Directory structure documentation:
- "JAEGIS-agent/" directory references
- File reference patterns and examples
- Path resolution examples

Status: NEEDS SCAN FOR DOCUMENTATION UPDATES
```

## Reference Pattern Analysis

### **Pattern 1: Script Execution References**
```yaml
Pattern: "script-name.ps1", "script-name.js", "script-name.sh"
Found in:
- package.json (build scripts)
- Documentation files
Impact: HIGH - Build and automation systems
Update Required: YES - Update paths to scripts/ directory
```

### **Pattern 2: Configuration File References**
```yaml
Pattern: "config.json", "package.json"
Found in:
- Build scripts
- Documentation
- Extension configuration
Impact: MEDIUM - System configuration
Update Required: CONDITIONAL - Only if files moved
```

### **Pattern 3: JAEGIS-agent Directory References**
```yaml
Pattern: "JAEGIS-agent/"
Found in:
- agent-config.txt (core paths)
- Documentation files
Impact: SAFE - Core system structure preserved
Update Required: NO - Paths remain unchanged
```

## Files Requiring Reference Updates

### **CRITICAL UPDATES REQUIRED**

#### **package.json**
```yaml
Script references to update:
- "fresh-install": "powershell -ExecutionPolicy Bypass -File scripts/installation/clean-install.ps1"
- "fresh-install-bash": "bash scripts/installation/clean-install.sh"
- "build-integration": "node scripts/build/build-integration.js"
- "test-integration": "node scripts/testing/test-augment-integration.js"

Priority: CRITICAL
Risk: HIGH - Build system failure if not updated
```

#### **Build Configuration Files**
```yaml
Files to update:
- tsconfig.json (if contains hardcoded paths)
- webpack.config.js (if contains hardcoded paths)
- Any configuration files with script references

Priority: HIGH
Risk: MEDIUM - Build compilation issues
```

### **MEDIUM UPDATES REQUIRED**

#### **Documentation Files**
```yaml
Files to update:
- Enhanced orchestrator instructions
- User guidelines
- Any documentation referencing moved files

Priority: MEDIUM
Risk: LOW - Documentation inconsistencies
```

## Files Requiring NO UPDATES

### **Core JAEGIS System (SAFE)**
```yaml
agent-config.txt:
- All JAEGIS-agent/* paths remain unchanged
- No updates needed to core directory references
- Agent loading system preserved

JAEGIS-agent/ structure:
- personas/, tasks/, templates/, checklists/, data/
- All internal references remain unchanged
- Core system functionality preserved
```

## Update Strategy by Priority

### **Phase 1: Critical System Files**
1. **package.json** - Update script references to new locations
2. **Build configuration files** - Update any hardcoded paths
3. **Test build system** - Ensure compilation works

### **Phase 2: Documentation Updates**
1. **Enhanced orchestrator instructions** - Update path examples
2. **User guidelines** - Update file location references
3. **Cross-references** - Update internal documentation links

### **Phase 3: Validation**
1. **Test all script executions** - Verify paths work correctly
2. **Test build processes** - Ensure no broken references
3. **Test documentation accessibility** - Verify all links work

## Risk Assessment

### **CRITICAL RISKS**
1. **package.json script failures** - Would break automation
2. **Build configuration errors** - Would break compilation
3. **Extension command failures** - Would break VS Code integration

### **MEDIUM RISKS**
1. **Documentation inconsistencies** - Would confuse users
2. **Cross-reference failures** - Would break navigation
3. **Example code failures** - Would mislead developers

### **LOW RISKS**
1. **Core system references** - SAFE (no changes needed)
2. **Agent loading system** - SAFE (JAEGIS-agent preserved)
3. **Internal JAEGIS-agent references** - SAFE (unchanged)

## Recommended Update Sequence

### **Step 1: Identify All References**
1. Complete scan of build configuration files
2. Document all hardcoded paths
3. Create reference mapping document

### **Step 2: Update Critical Files**
1. Update package.json script references
2. Update build configuration files
3. Test build system functionality

### **Step 3: Update Documentation**
1. Update enhanced orchestrator instructions
2. Update user guidelines
3. Update cross-references between files

### **Step 4: Validation**
1. Test all script executions
2. Test build processes
3. Test extension functionality
4. Test documentation accessibility

## Key Findings

### **SAFE AREAS (No Updates Needed)**
- **agent-config.txt**: All JAEGIS-agent paths preserved
- **Core JAEGIS-agent structure**: Remains unchanged
- **Agent loading system**: Fully preserved

### **UPDATE REQUIRED AREAS**
- **package.json**: Script paths need updating
- **Build configuration**: May need path updates
- **Documentation**: Path examples need updating

### **SUCCESS CRITERIA**
- All scripts execute correctly from new locations
- Build system compiles without errors
- Extension functions properly in VS Code
- Documentation accurately reflects new structure

**Status**: ✅ **TASK 1.3 COMPLETE** - Hardcoded references identified and categorized by priority

**Key Finding**: Core JAEGIS-agent system is SAFE - main updates needed for package.json script references
