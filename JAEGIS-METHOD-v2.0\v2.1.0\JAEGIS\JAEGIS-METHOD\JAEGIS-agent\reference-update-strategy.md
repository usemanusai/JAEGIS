# Reference Update Strategy - Task 2.3

## Task 2.3: Plan Reference Update Strategy

**Date**: 2025-01-23  
**Purpose**: Systematic approach for updating all file references to reflect new directory structure  

## Reference Update Overview

### 🎯 **Strategic Approach: Systematic Path Mapping**
1. **Map all current references** to their new locations
2. **Update references systematically** by file type and priority
3. **Validate reference updates** at each step
4. **Test functionality** after each update batch

## Reference Mapping Strategy

### 📋 **Reference Type 1: Documentation Cross-References**

#### **Current → New Path Mappings**
```yaml
# User Guidelines
JAEGIS-agent/enhanced-JAEGIS-orchestrator-instructions.md → docs/user-guides/enhanced-JAEGIS-orchestrator-instructions.md
JAEGIS-agent/JAEGIS-user-guidelines-condensed.md → docs/user-guides/JAEGIS-user-guidelines-condensed.md

# Agent System Documentation
JAEGIS-agent/24-agent-*.md → docs/agent-system/24-agent-*.md
JAEGIS-agent/expanded-agent-classification-system.md → docs/agent-system/expanded-agent-classification-system.md

# Workflow Documentation
JAEGIS-agent/documentation-mode-integration-enhancement.md → docs/workflows/documentation-mode-integration-enhancement.md
JAEGIS-agent/full-development-mode-integration-enhancement.md → docs/workflows/full-development-mode-integration-enhancement.md

# Command Documentation
JAEGIS-agent/enhanced-24-agent-command-system.md → docs/commands/enhanced-24-agent-command-system.md
JAEGIS-agent/full-team-commands-implementation.md → docs/commands/full-team-commands-implementation.md
```

#### **Files Requiring Documentation Reference Updates**
```yaml
Primary files to update:
  1. enhanced-JAEGIS-orchestrator-instructions.md
     - References to other documentation files
     - Internal cross-links
     - File structure references

  2. JAEGIS-user-guidelines-condensed.md
     - References to enhanced instructions
     - System documentation links

  3. 24-agent system documentation files
     - Cross-references between agent docs
     - Links to validation reports
     - References to implementation guides

Update method:
  - Search for relative path references
  - Update to new directory structure
  - Validate link functionality
```

### 🔧 **Reference Type 2: Script File References**

#### **Current → New Path Mappings**
```yaml
# Build Scripts
build-and-test-integration.ps1 → scripts/build/build-and-test-integration.ps1
build-integration.bat → scripts/build/build-integration.bat
build-integration.js → scripts/build/build-integration.js

# Installation Scripts
install-*.ps1/sh/bat → scripts/installation/install-*.ps1/sh/bat
setup-*.ps1/sh/bat → scripts/setup/setup-*.ps1/sh/bat

# Service Scripts
emad-auto-sync.py → scripts/services/emad-auto-sync.py
emad-service-manager.py → scripts/services/emad-service-manager.py
```

#### **Files Requiring Script Reference Updates**
```yaml
Primary files to update:
  1. package.json
     - Script execution paths
     - Build script references
     - Test script references

  2. Documentation files
     - Installation procedure references
     - Build process documentation
     - Service setup instructions

  3. Other scripts
     - Cross-script references
     - Service dependency references
     - Build process chains

Update method:
  - Scan for script path references
  - Update to new script locations
  - Test script execution
```

### ⚙️ **Reference Type 3: Configuration File References**

#### **Current → New Path Mappings**
```yaml
# Build Configuration
package.json → config/build/package.json
tsconfig.json → config/build/tsconfig.json
webpack.config.js → config/build/webpack.config.js

# Service Configuration
emad-auto-sync.service → config/services/emad-auto-sync.service
ide-JAEGIS-orchestrator.cfg.md → config/ide/ide-JAEGIS-orchestrator.cfg.md
```

#### **System-Wide Reference Updates Required**
```yaml
NPM/Node.js system references:
  - package.json location for npm commands
  - Node.js module resolution paths
  - Script execution paths

TypeScript compiler references:
  - tsconfig.json location for tsc commands
  - Source file path mappings
  - Output directory configurations

Webpack references:
  - webpack.config.js location
  - Entry point paths
  - Output directory paths
  - Asset path configurations

VS Code Extension references:
  - Extension configuration paths
  - Build output paths
  - Package.json extension metadata
```

## Systematic Update Process

### **Phase 1: Documentation Reference Updates**

#### **Step 1: Map Documentation Cross-References**
```yaml
Process:
  1. Scan all documentation files for internal links
  2. Identify relative path references
  3. Create reference mapping table
  4. Update paths systematically

Files to scan:
  - enhanced-JAEGIS-orchestrator-instructions.md
  - JAEGIS-user-guidelines-condensed.md
  - All 24-agent-*.md files
  - Workflow documentation files
  - Command documentation files

Reference patterns to find:
  - [text](./filename.md)
  - [text](../directory/filename.md)
  - [text](JAEGIS-agent/filename.md)
  - Direct file path references
```

#### **Step 2: Update Documentation References**
```yaml
Update process:
  1. Replace old paths with new paths
  2. Validate markdown link syntax
  3. Test link functionality
  4. Verify cross-reference integrity

Validation:
  - All internal links work
  - No broken references
  - Proper relative path structure
  - Consistent link formatting
```

### **Phase 2: Script Reference Updates**

#### **Step 1: Identify Script Dependencies**
```yaml
Script dependency analysis:
  1. Build scripts → Configuration files
  2. Installation scripts → Other scripts
  3. Service scripts → Configuration files
  4. Utility scripts → System paths

Reference patterns to find:
  - Hardcoded file paths
  - Relative path references
  - Configuration file imports
  - Script execution calls
```

#### **Step 2: Update Script References**
```yaml
Update process:
  1. Update configuration file paths
  2. Update script execution paths
  3. Update output directory paths
  4. Update dependency references

Validation:
  - Script execution successful
  - Configuration files accessible
  - Output paths functional
  - Dependencies resolved
```

### **Phase 3: Configuration Reference Updates (CRITICAL)**

#### **Step 1: Build System Path Updates**
```yaml
package.json updates:
  - Script paths: "build": "scripts/build/build-integration.js"
  - Output paths: Update any hardcoded output references
  - Extension paths: Update VS Code extension configuration

tsconfig.json updates:
  - Source paths: Update include/exclude patterns if needed
  - Output paths: Update outDir if hardcoded
  - Path mappings: Update any path mapping configurations

webpack.config.js updates:
  - Entry paths: Update entry point references
  - Output paths: Update output directory configuration
  - Asset paths: Update asset loading paths
```

#### **Step 2: System Integration Updates**
```yaml
NPM system updates:
  - Update npm commands to reference config/build/package.json
  - Update Node.js module resolution if needed
  - Update package manager configurations

TypeScript system updates:
  - Update tsc commands to reference config/build/tsconfig.json
  - Update IDE TypeScript configuration
  - Update build tool TypeScript references

VS Code Extension updates:
  - Update extension loading paths
  - Update package.json reference in extension system
  - Update build output paths for extension packaging
```

## Reference Update Validation

### **Validation Level 1: File Accessibility**
```yaml
Tests:
  - All referenced files exist at new locations
  - File permissions preserved
  - File content integrity maintained

Success criteria:
  - 100% file accessibility
  - No file not found errors
  - Proper file permissions
```

### **Validation Level 2: Reference Functionality**
```yaml
Tests:
  - Documentation links work correctly
  - Script references execute properly
  - Configuration files load successfully

Success criteria:
  - All links functional
  - All scripts executable
  - All configurations accessible
```

### **Validation Level 3: System Integration**
```yaml
Tests:
  - Build system functions correctly
  - Extension loads properly
  - User interface works
  - Documentation navigation functional

Success criteria:
  - Complete system functionality
  - No integration failures
  - User experience preserved
```

## Update Sequence and Timing

### **Sequence 1: Low-Risk Updates First**
```yaml
Order:
  1. Utility script references
  2. Service configuration references
  3. Low-impact documentation references

Risk: LOW
Time: 30-60 minutes
Validation: Basic functionality testing
```

### **Sequence 2: Medium-Risk Updates**
```yaml
Order:
  1. Agent system documentation references
  2. Workflow documentation references
  3. Service script references

Risk: MEDIUM
Time: 1-2 hours
Validation: Integration testing
```

### **Sequence 3: High-Risk Updates**
```yaml
Order:
  1. User guideline references
  2. Build script references
  3. Primary documentation references

Risk: HIGH
Time: 2-3 hours
Validation: User interface and build testing
```

### **Sequence 4: Critical Updates**
```yaml
Order:
  1. package.json path references
  2. tsconfig.json path references
  3. webpack.config.js path references
  4. System-wide path updates

Risk: CRITICAL
Time: 3-4 hours
Validation: Complete system testing
```

## Error Handling and Rollback

### **Error Detection**
```yaml
Monitoring for:
  - Broken links in documentation
  - Script execution failures
  - Configuration loading errors
  - Build system failures
  - Extension loading issues
```

### **Rollback Procedures**
```yaml
Level 1 Rollback (Reference-specific):
  - Revert specific reference changes
  - Test affected functionality
  - Continue with corrected references

Level 2 Rollback (File-specific):
  - Revert all references for specific file
  - Restore file to original location
  - Update references back to original paths

Level 3 Rollback (System-wide):
  - Revert all reference changes
  - Restore all files to original locations
  - Validate complete system functionality
```

## Success Metrics

### **Reference Update Success**
```yaml
- 100% of references updated correctly
- 0% broken links or references
- 100% functionality preserved
- 0% performance degradation
```

### **System Integration Success**
```yaml
- Build system fully functional
- Extension loads correctly
- Documentation navigation works
- User interface preserved
- All automation functional
```

## Next Steps

1. **Create backup strategy** (Task 2.4)
2. **Begin reference mapping** for low-risk files
3. **Start systematic updates** following sequence
4. **Validate at each step** before proceeding

**Status**: ✅ **TASK 2.3 COMPLETE** - Comprehensive reference update strategy planned with systematic validation approach
