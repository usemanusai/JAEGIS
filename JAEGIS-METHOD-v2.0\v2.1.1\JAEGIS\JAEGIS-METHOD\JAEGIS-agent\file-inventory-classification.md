# JAEGIS Project File Inventory and Classification

## Task 1.1: Complete File Inventory and Classification

**Date**: 2025-01-23  
**Purpose**: Create comprehensive inventory of all files in JAEGIS project, classifying them by type and identifying which files need to be moved  

## File Classification Overview

### 📋 **DOCUMENTATION FILES (.md) - TO MOVE TO /docs/**

#### **Root Level Documentation (3 files)**
```yaml
Files to move:
- CONTRIBUTING.md → docs/CONTRIBUTING.md
- README.md → docs/README.md
- LICENSE → docs/LICENSE

Current location: Root directory
Target location: docs/
Priority: HIGH - Core project documentation
```

#### **JAEGIS-agent Documentation (47 files)**
```yaml
Files to move to docs/agent-system/:
- 24-agent-configuration-update-summary.md
- 24-agent-participation-tracking-validation.md
- 24-agent-performance-optimization.md
- 24-agent-system-summary.md
- 24-agent-system-validation-report.md
- 24-agent-workflow-integration-enhancement.md
- additional-agents-integration-points.md
- agent-activation-logic-system.md
- agent-update-summary.md
- complete-20-agent-inventory-audit.md
- complete-24-agent-system-documentation.md
- expanded-agent-classification-system.md
- participation-manager-system.md
- participation-tracking-system-implementation.md
- full-team-participation-validation-summary.md

Files to move to docs/user-guides/:
- JAEGIS-user-guidelines-condensed.md
- enhanced-JAEGIS-orchestrator-instructions.md
- updated-user-guidelines.md

Files to move to docs/workflows/:
- documentation-mode-integration-enhancement.md
- full-development-mode-integration-enhancement.md
- full-development-mode-integration.md

Files to move to docs/commands/:
- enhanced-24-agent-command-system.md
- full-team-commands-implementation.md

Files to move to docs/quality/:
- quality-assurance-standards-implementation.md
- quality-assurance-standards.md

Files to move to docs/validation/:
- system-validation-report.md
- full-implementation-validation.md

Files to move to docs/deployment/:
- deployment-readiness-checklist.md
- production-deployment-guide.md

Files to move to docs/ide-integration/:
- ide-JAEGIS-orchestrator.md

Files to move to docs/web-integration/:
- web-JAEGIS-orchestrator-agent.md

Files to move to docs/diagnostics/:
- backup-strategy.md
- critical-system-files-analysis.md
- dependency-map-analysis.md
- directory-structure-creation.md
- directory-structure-validation.md
- file-copying-progress.md
- file-inventory-analysis.md
- file-movement-strategy.md
- hardcoded-references-analysis.md
- reference-update-strategy.md
- reorganization-completion-summary.md
- risk-assessment-impact-analysis.md

Current location: JAEGIS-agent/
Target locations: Various docs/ subdirectories
Priority: MEDIUM - System documentation
```

#### **Existing docs/ Directory (50+ files)**
```yaml
Status: KEEP IN PLACE
Action: Organize existing documentation within docs/
Note: Already in correct location, may need reorganization
```

### 🔧 **SCRIPT FILES - TO MOVE TO /scripts/**

#### **PowerShell Scripts (.ps1) - 8 files**
```yaml
Files to move to scripts/build/:
- build-and-test-integration.ps1
- fix-build-errors.ps1

Files to move to scripts/installation/:
- clean-install.ps1
- install-emad-service.ps1
- install-emad-universal.ps1
- install-extension.ps1
- install.ps1

Files to move to scripts/utilities/:
- find-vscode-fixed.ps1
- find-vscode.ps1
- launch-extension.ps1
- emad-launcher.ps1

Files to move to scripts/setup/:
- setup-emad-repository.ps1
- verify-dependencies.ps1

Current location: Root directory
Target location: scripts/ subdirectories
Priority: MEDIUM - Build and setup automation
```

#### **Batch Scripts (.bat) - 7 files**
```yaml
Files to move to scripts/build/:
- build-integration.bat

Files to move to scripts/installation/:
- install-emad-service.bat
- install.bat

Files to move to scripts/setup/:
- create-emad-repository.bat
- setup-emad-simple.bat
- setup-emad-with-failsafe.bat

Files to move to scripts/utilities/:
- emad-launcher.bat
- emad-startup.bat

Files to move to scripts/troubleshooting/:
- fix-service-issue.bat

Current location: Root directory
Target location: scripts/ subdirectories
Priority: MEDIUM - Windows automation
```

#### **Shell Scripts (.sh) - 4 files**
```yaml
Files to move to scripts/installation/:
- clean-install.sh
- install-emad-universal.sh
- install-extension.sh
- install.sh

Files to move to scripts/setup/:
- setup-emad-repository.sh

Current location: Root directory
Target location: scripts/ subdirectories
Priority: MEDIUM - Unix/Linux automation
```

#### **Python Scripts (.py) - 12 files**
```yaml
Files to move to scripts/services/:
- emad-auto-sync-service.py
- emad-auto-sync.py
- emad-background-runner.py
- emad-service-manager.py
- emad-failsafe-system.py
- emad_auto_sync.py

Files to move to scripts/cli/:
- emad-cli.py
- emad-failsafe-cli.py

Files to move to scripts/monitoring/:
- emad-health-monitor.py

Files to move to scripts/validation/:
- emad-installation-verifier.py
- emad-universal-verifier.py

Files to move to scripts/configuration/:
- emad-intelligent-config.py

Files to move to scripts/templates/:
- emad-project-templates.py

Files to move to scripts/testing/:
- test-emad-failsafe-integration.py
- test-universal-installation.py

Files to move to scripts/troubleshooting/:
- troubleshoot-emad.py

Current location: Root directory
Target location: scripts/ subdirectories
Priority: MEDIUM - Service and automation scripts
```

#### **JavaScript Scripts (.js) - 5 files**
```yaml
Files to move to scripts/build/:
- build-integration.js
- build-web-agent.js
- build-web-agent.cfg.js

Files to move to scripts/testing/:
- test-augment-integration.js
- test-extension.js

Files to move to scripts/troubleshooting/:
- troubleshoot-augment-integration.js

Current location: Root directory
Target location: scripts/ subdirectories
Priority: MEDIUM - Build and test automation
```

### ⚙️ **CONFIGURATION FILES - TO MOVE TO /config/**

#### **Build Configuration Files (5 files)**
```yaml
Files to move to config/build/:
- package.json
- package-lock.json
- tsconfig.json
- tsconfig.webpack.json
- webpack.config.js

Current location: Root directory
Target location: config/build/
Priority: CRITICAL - Build system configuration
Special handling: These files may have hardcoded paths
```

#### **Service Configuration Files (1 file)**
```yaml
Files to move to config/services/:
- emad-auto-sync.service

Current location: Root directory
Target location: config/services/
Priority: MEDIUM - Service configuration
```

#### **IDE Configuration Files (1 file)**
```yaml
Files to move to config/ide/:
- ide-JAEGIS-orchestrator.cfg.md

Current location: JAEGIS-agent/
Target location: config/ide/
Priority: LOW - IDE-specific configuration
```

#### **Web Configuration Files (1 file)**
```yaml
Files to move to config/web/:
- web-JAEGIS-orchestrator-agent.cfg.md

Current location: JAEGIS-agent/
Target location: config/web/
Priority: LOW - Web-specific configuration
```

#### **Diagnostic Configuration Files (1 file)**
```yaml
Files to move to config/diagnostics/:
- JAEGIS-diagnostic-report.json

Current location: Root directory
Target location: config/diagnostics/
Priority: LOW - Diagnostic configuration
```

### 🏗️ **CORE JAEGIS-AGENT STRUCTURE - KEEP IN PLACE**

#### **Core Directories (DO NOT MOVE)**
```yaml
JAEGIS-agent/personas/ - Agent persona definitions
JAEGIS-agent/tasks/ - Task definitions
JAEGIS-agent/templates/ - Document templates
JAEGIS-agent/checklists/ - Quality checklists
JAEGIS-agent/data/ - Knowledge bases and data

Status: PRESERVE COMPLETELY
Reason: Core system architecture
Action: NO CHANGES
```

#### **Core Configuration Files (DO NOT MOVE)**
```yaml
JAEGIS-agent/agent-config.txt - Main agent configuration
JAEGIS-agent/personas.txt - Persona index
JAEGIS-agent/tasks.txt - Task index
JAEGIS-agent/templates.txt - Template index
JAEGIS-agent/checklists.txt - Checklist index

Status: PRESERVE COMPLETELY
Reason: Critical system files
Action: NO CHANGES
```

### 🚫 **FILES TO EXCLUDE FROM REORGANIZATION**

#### **Build Artifacts and Dependencies**
```yaml
node_modules/ - NPM dependencies (exclude)
dist/ - Build output (exclude)
out/ - Compiled output (exclude)
__pycache__/ - Python cache (exclude)
logs/ - Log files (exclude)

Status: EXCLUDE
Reason: Generated files, not source
Action: NO CHANGES
```

#### **Development Directories**
```yaml
src/ - Source code (keep in place)
images/ - Image assets (keep in place)
new-agent-design/ - Development work (keep in place)
web-build-sample/ - Sample files (keep in place)

Status: KEEP IN PLACE
Reason: Active development directories
Action: NO CHANGES
```

#### **Special Files**
```yaml
Future.txt - Planning document (keep in place)
EMAD_GITIGNORE - Git ignore template (keep in place)

Status: KEEP IN PLACE
Reason: Special purpose files
Action: NO CHANGES
```

## Summary Statistics

### Files to Reorganize
- **Documentation Files**: ~100 files → /docs/
- **Script Files**: ~36 files → /scripts/
- **Configuration Files**: ~9 files → /config/
- **Total Files to Move**: ~145 files

### Files to Keep in Place
- **Core JAEGIS-agent structure**: All subdirectories and core files
- **Source code**: src/ directory
- **Build artifacts**: node_modules/, dist/, out/
- **Development assets**: images/, new-agent-design/

### Critical Files Requiring Special Attention
1. **agent-config.txt** - Likely contains many file path references
2. **package.json** - Build system configuration with potential paths
3. **tsconfig.json** - TypeScript configuration with potential paths
4. **webpack.config.js** - Build configuration with potential paths
5. **Enhanced orchestrator instructions** - May reference other files

## Next Steps
1. Scan all files for hardcoded references (Task 1.2)
2. Create dependency map (Task 1.3)
3. Identify critical system files (Task 1.4)
4. Assess risks and impacts (Task 1.5)

**Status**: ✅ **TASK 1.1 COMPLETE** - Comprehensive file inventory and classification ready for dependency analysis
