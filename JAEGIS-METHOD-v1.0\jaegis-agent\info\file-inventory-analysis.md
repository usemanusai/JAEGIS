# JAEGIS Project File Inventory and Classification Analysis

## Task 1.1: Complete File Inventory and Classification

**Date**: 2025-01-23  
**Purpose**: Comprehensive inventory of all files in JAEGIS project for reorganization planning  

## File Classification Categories

### 📋 **DOCUMENTATION FILES (.md) - TO MOVE TO /docs/**

#### Root Level Documentation
- `CONTRIBUTING.md` → `/docs/CONTRIBUTING.md`
- `README.md` → `/docs/README.md`
- `LICENSE` → `/docs/LICENSE`

#### JAEGIS-agent Documentation (24 files)
- `24-agent-configuration-update-summary.md` → `/docs/agent-system/`
- `24-agent-participation-tracking-validation.md` → `/docs/agent-system/`
- `24-agent-performance-optimization.md` → `/docs/agent-system/`
- `24-agent-system-summary.md` → `/docs/agent-system/`
- `24-agent-system-validation-report.md` → `/docs/agent-system/`
- `24-agent-workflow-integration-enhancement.md` → `/docs/agent-system/`
- `additional-agents-integration-points.md` → `/docs/agent-system/`
- `agent-activation-logic-system.md` → `/docs/agent-system/`
- `agent-update-summary.md` → `/docs/agent-system/`
- `JAEGIS-user-guidelines-condensed.md` → `/docs/user-guides/`
- `complete-20-agent-inventory-audit.md` → `/docs/agent-system/`
- `complete-24-agent-system-documentation.md` → `/docs/agent-system/`
- `deployment-readiness-checklist.md` → `/docs/deployment/`
- `documentation-mode-integration-enhancement.md` → `/docs/workflows/`
- `enhanced-24-agent-command-system.md` → `/docs/commands/`
- `enhanced-JAEGIS-orchestrator-instructions.md` → `/docs/user-guides/`
- `expanded-agent-classification-system.md` → `/docs/agent-system/`
- `full-development-mode-integration-enhancement.md` → `/docs/workflows/`
- `full-team-commands-implementation.md` → `/docs/commands/`
- `full-team-participation-validation-summary.md` → `/docs/agent-system/`
- `ide-JAEGIS-orchestrator.md` → `/docs/ide-integration/`
- `participation-manager-system.md` → `/docs/agent-system/`
- `participation-tracking-system-implementation.md` → `/docs/agent-system/`
- `production-deployment-guide.md` → `/docs/deployment/`
- `quality-assurance-standards-implementation.md` → `/docs/quality/`
- `system-validation-report.md` → `/docs/validation/`
- `updated-user-guidelines.md` → `/docs/user-guides/`
- `web-JAEGIS-orchestrator-agent.md` → `/docs/web-integration/`

#### Existing /docs Directory (50+ files)
- All existing documentation in `/docs/` stays in place
- May need reorganization within `/docs/` for better structure

### 🔧 **SCRIPT FILES - TO MOVE TO /scripts/**

#### PowerShell Scripts (.ps1)
- `build-and-test-integration.ps1` → `/scripts/build/`
- `clean-install.ps1` → `/scripts/installation/`
- `find-vscode-fixed.ps1` → `/scripts/utilities/`
- `find-vscode.ps1` → `/scripts/utilities/`
- `fix-build-errors.ps1` → `/scripts/build/`
- `install-emad-service.ps1` → `/scripts/installation/`
- `install-emad-universal.ps1` → `/scripts/installation/`
- `install-extension.ps1` → `/scripts/installation/`
- `install.ps1` → `/scripts/installation/`
- `launch-extension.ps1` → `/scripts/utilities/`
- `setup-emad-repository.ps1` → `/scripts/setup/`
- `verify-dependencies.ps1` → `/scripts/validation/`

#### Batch Scripts (.bat)
- `build-integration.bat` → `/scripts/build/`
- `create-emad-repository.bat` → `/scripts/setup/`
- `emad-launcher.bat` → `/scripts/utilities/`
- `emad-startup.bat` → `/scripts/utilities/`
- `fix-service-issue.bat` → `/scripts/troubleshooting/`
- `install-emad-service.bat` → `/scripts/installation/`
- `install.bat` → `/scripts/installation/`
- `setup-emad-simple.bat` → `/scripts/setup/`
- `setup-emad-with-failsafe.bat` → `/scripts/setup/`

#### Shell Scripts (.sh)
- `clean-install.sh` → `/scripts/installation/`
- `install-emad-universal.sh` → `/scripts/installation/`
- `install-extension.sh` → `/scripts/installation/`
- `install.sh` → `/scripts/installation/`
- `setup-emad-repository.sh` → `/scripts/setup/`

#### Python Scripts (.py)
- `emad-auto-sync-service.py` → `/scripts/services/`
- `emad-auto-sync.py` → `/scripts/services/`
- `emad-background-runner.py` → `/scripts/services/`
- `emad-cli.py` → `/scripts/cli/`
- `emad-failsafe-cli.py` → `/scripts/cli/`
- `emad-failsafe-system.py` → `/scripts/services/`
- `emad-health-monitor.py` → `/scripts/monitoring/`
- `emad-installation-verifier.py` → `/scripts/validation/`
- `emad-intelligent-config.py` → `/scripts/configuration/`
- `emad-launcher.ps1` → `/scripts/utilities/`
- `emad-project-templates.py` → `/scripts/templates/`
- `emad-service-manager.py` → `/scripts/services/`
- `emad-universal-verifier.py` → `/scripts/validation/`
- `emad_auto_sync.py` → `/scripts/services/`
- `test-augment-integration.js` → `/scripts/testing/`
- `test-emad-failsafe-integration.py` → `/scripts/testing/`
- `test-extension.js` → `/scripts/testing/`
- `test-universal-installation.py` → `/scripts/testing/`
- `troubleshoot-augment-integration.js` → `/scripts/troubleshooting/`
- `troubleshoot-emad.py` → `/scripts/troubleshooting/`

#### JavaScript Build Scripts (.js)
- `build-integration.js` → `/scripts/build/`
- `build-web-agent.cfg.js` → `/scripts/build/`
- `build-web-agent.js` → `/scripts/build/`

### ⚙️ **CONFIGURATION FILES - TO MOVE TO /config/**

#### Configuration Files
- `ide-JAEGIS-orchestrator.cfg.md` → `/config/ide/`
- `web-JAEGIS-orchestrator-agent.cfg.md` → `/config/web/`
- `emad-auto-sync.service` → `/config/services/`
- `tsconfig.json` → `/config/build/`
- `tsconfig.webpack.json` → `/config/build/`
- `webpack.config.js` → `/config/build/`
- `package.json` → `/config/build/`
- `package-lock.json` → `/config/build/`

#### JSON Configuration Files
- `JAEGIS-diagnostic-report.json` → `/config/diagnostics/`

### 🏗️ **CORE JAEGIS-AGENT STRUCTURE - KEEP IN PLACE**

#### Core Directories (DO NOT MOVE)
- `JAEGIS-agent/personas/` - Agent persona definitions
- `JAEGIS-agent/tasks/` - Task definitions
- `JAEGIS-agent/templates/` - Document templates
- `JAEGIS-agent/checklists/` - Quality checklists
- `JAEGIS-agent/data/` - Knowledge bases and data

#### Core Configuration Files (DO NOT MOVE)
- `JAEGIS-agent/agent-config.txt` - Main agent configuration
- `JAEGIS-agent/personas.txt` - Persona index
- `JAEGIS-agent/tasks.txt` - Task index
- `JAEGIS-agent/templates.txt` - Template index
- `JAEGIS-agent/checklists.txt` - Checklist index

### 🚫 **FILES TO EXCLUDE FROM REORGANIZATION**

#### Build Artifacts and Dependencies
- `node_modules/` - NPM dependencies (exclude)
- `dist/` - Build output (exclude)
- `out/` - Compiled output (exclude)
- `__pycache__/` - Python cache (exclude)
- `logs/` - Log files (exclude)

#### Development Directories
- `src/` - Source code (keep in place)
- `images/` - Image assets (keep in place)
- `new-agent-design/` - Development work (keep in place)
- `web-build-sample/` - Sample files (keep in place)

#### Special Files
- `Future.txt` - Planning document (keep in place)
- `EMAD_GITIGNORE` - Git ignore template (keep in place)

## Summary Statistics

### Files to Reorganize
- **Documentation Files**: ~75 files → `/docs/`
- **Script Files**: ~35 files → `/scripts/`
- **Configuration Files**: ~8 files → `/config/`
- **Total Files to Move**: ~118 files

### Files to Keep in Place
- **Core JAEGIS-agent structure**: All subdirectories and core files
- **Source code**: `src/` directory
- **Build artifacts**: `node_modules/`, `dist/`, `out/`
- **Development assets**: `images/`, `new-agent-design/`

### Critical Files Requiring Special Attention
1. **agent-config.txt** - Likely contains many file path references
2. **Enhanced orchestrator instructions** - May reference other files
3. **Build configuration files** - May have hardcoded paths
4. **Service configuration files** - May reference script locations

## Next Steps
1. Scan all files for hardcoded references (Task 1.2)
2. Create dependency map (Task 1.3)
3. Identify critical system files (Task 1.4)
4. Assess risks and impacts (Task 1.5)

**Status**: ✅ **TASK 1.1 COMPLETE** - File inventory and classification ready for dependency analysis
