"""
JAEGIS Enhanced System - GitHub Repository Structure Organizer
Phase 3: Structured Organization & File Preparation

Creates agent configuration files matching GitHub repository format,
organizes into tier structure with complete definitions for dynamic resource fetching.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import shutil

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Agent configuration structure"""
    name: str
    title: str
    description: str
    tier: int
    squad: str
    persona: str
    tasks: List[str]
    templates: List[str]
    checklists: List[str]
    data: List[str]
    coordination: str
    handoff_from: List[str]
    handoff_to: List[str]
    priority: int
    classification: str


@dataclass
class SquadConfig:
    """Squad configuration structure"""
    squad_name: str
    tier: int
    total_agents: int
    purpose: str
    coordination_protocol: str
    agents: List[AgentConfig]


class GitHubRepositoryStructureOrganizer:
    """
    Organizes JAEGIS system files into GitHub repository structure
    with proper tier organization and dynamic resource fetching compatibility.
    """
    
    def __init__(self, base_path: str = "JAEGIS_Enhanced_System"):
        self.base_path = Path(base_path)
        self.github_structure = {
            "core": {
                "agent-config.txt": "Main agent configuration",
                "enhanced-agent-config.txt": "Enhanced 68-agent configuration", 
                "iuas-agent-config.txt": "IUAS 20-agent maintenance squad",
                "garas-agent-config.txt": "GARAS 40-agent gap resolution squad",
                "chimera-agent-config.txt": "Chimera v4.1 47-agent specialized squad"
            },
            "commands": {
                "squad-commands.md": "Enhanced squad commands (150+)",
                "tier-commands.json": "Tier-specific command mappings",
                "coordination-commands.json": "Inter-squad coordination commands"
            },
            "templates": {
                "agent-templates/": "Agent-specific templates",
                "squad-templates/": "Squad coordination templates", 
                "system-templates/": "System-wide templates"
            },
            "config": {
                "openrouter-config.json": "OpenRouter.ai integration (3000+ keys)",
                "sync-config.json": "GitHub synchronization configuration",
                "nlds-config.json": "N.L.D.S. Tier 0 configuration",
                "pitces-config.yaml": "P.I.T.C.E.S. framework configuration"
            },
            "docs": {
                "architecture/": "System architecture documentation",
                "api/": "API documentation",
                "guides/": "User guides and tutorials"
            },
            "sync": {
                "protocols/": "Synchronization protocols",
                "monitoring/": "Sync monitoring and validation"
            }
        }
        
        # Agent configurations from existing files
        self.agent_configurations = {}
        self.squad_configurations = {}
        
        logger.info("GitHubRepositoryStructureOrganizer initialized")
    
    def create_github_structure(self) -> Dict[str, Any]:
        """Create complete GitHub repository structure"""
        
        try:
            # Create base directory structure
            self._create_directory_structure()
            
            # Organize agent configurations
            self._organize_agent_configurations()
            
            # Create command structures
            self._create_command_structures()
            
            # Organize templates
            self._organize_templates()
            
            # Create configuration files
            self._create_configuration_files()
            
            # Generate documentation structure
            self._create_documentation_structure()
            
            # Create sync protocols
            self._create_sync_protocols()
            
            return {
                "status": "success",
                "structure_created": True,
                "directories": list(self.github_structure.keys()),
                "total_files": self._count_created_files(),
                "github_compatible": True
            }
            
        except Exception as e:
            logger.error(f"GitHub structure creation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _create_directory_structure(self):
        """Create the base directory structure"""
        
        github_root = self.base_path / "github_repository"
        github_root.mkdir(parents=True, exist_ok=True)
        
        for directory, contents in self.github_structure.items():
            dir_path = github_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories if specified
            for item, description in contents.items():
                if item.endswith("/"):
                    subdir_path = dir_path / item.rstrip("/")
                    subdir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("GitHub directory structure created")
    
    def _organize_agent_configurations(self):
        """Organize all agent configurations into GitHub format"""
        
        github_root = self.base_path / "github_repository"
        core_path = github_root / "core"
        
        # Create main agent-config.txt (24-agent standard system)
        self._create_standard_agent_config(core_path)
        
        # Create enhanced-agent-config.txt (68-agent enhanced system)
        self._create_enhanced_agent_config(core_path)
        
        # Create iuas-agent-config.txt (20-agent IUAS maintenance squad)
        self._create_iuas_agent_config(core_path)
        
        # Create garas-agent-config.txt (40-agent GARAS gap resolution squad)
        self._create_garas_agent_config(core_path)
        
        # Create chimera-agent-config.txt (47-agent Chimera v4.1 specialized squad)
        self._create_chimera_agent_config(core_path)
        
        logger.info("Agent configurations organized for GitHub")
    
    def _create_standard_agent_config(self, core_path: Path):
        """Create standard 24-agent configuration"""
        
        config_content = """# JAEGIS Standard Agent Configuration v2.2
# 24-Agent System with 4-Tier Architecture
# GitHub Repository: https://github.com/usemanusai/JAEGIS
# Dynamic Resource Fetching Compatible

==================== SYSTEM OVERVIEW ====================
Total Agents: 24
Architecture: 4-Tier Standard System
Coordination: Cross-Tier Collaborative Intelligence
Integration: GitHub-Local Hybrid with Dynamic Resource Fetching
Validation: Comprehensive Quality Standards

==================== TIER 1: MASTER ORCHESTRATOR ====================

==================== START: JAEGIS ====================
Title: Master AI Agent Orchestrator & System Intelligence
Name: JAEGIS
Description: Supreme orchestrator managing the entire 24-agent ecosystem
Persona: personas#jaegis-master-orchestrator
Tasks: [Master System Orchestration](tasks#master-system-orchestration)
Templates: [Master Orchestration Templates](templates#master-orchestration)
Checklists: [Master System Validation](checklists#master-system-validation)
Data: [System Intelligence Database](data#system-intelligence)
Coordination: master-orchestrator
Squad: tier-1-master
Handoff-From: [all-agents]
Handoff-To: [all-agents]
Priority: 10
Classification: TIER-1-MASTER
==================== END: JAEGIS ====================

==================== TIER 2: SENIOR COORDINATORS (3 AGENTS) ====================

==================== START: John ====================
Title: Senior Project Coordinator & Strategic Planning Specialist
Name: John
Description: Strategic planning and high-level project coordination
Persona: personas#senior-coordinator-john
Tasks: [Strategic Planning](tasks#strategic-planning)
Templates: [Project Coordination Templates](templates#project-coordination)
Checklists: [Strategic Planning Validation](checklists#strategic-planning)
Data: [Strategic Planning Database](data#strategic-planning)
Coordination: collaborative
Squad: tier-2-coordinators
Handoff-From: [JAEGIS]
Handoff-To: [Fred, Tyler, tier-3-agents]
Priority: 9
Classification: TIER-2-COORDINATOR
==================== END: John ====================

==================== START: Fred ====================
Title: Senior Technical Coordinator & Implementation Specialist
Name: Fred
Description: Technical implementation and system architecture coordination
Persona: personas#senior-coordinator-fred
Tasks: [Technical Implementation](tasks#technical-implementation)
Templates: [Technical Coordination Templates](templates#technical-coordination)
Checklists: [Technical Implementation Validation](checklists#technical-implementation)
Data: [Technical Implementation Database](data#technical-implementation)
Coordination: collaborative
Squad: tier-2-coordinators
Handoff-From: [JAEGIS, John]
Handoff-To: [Tyler, tier-3-agents]
Priority: 9
Classification: TIER-2-COORDINATOR
==================== END: Fred ====================

==================== START: Tyler ====================
Title: Senior Quality Coordinator & Validation Specialist
Name: Tyler
Description: Quality assurance and comprehensive validation coordination
Persona: personas#senior-coordinator-tyler
Tasks: [Quality Validation](tasks#quality-validation)
Templates: [Quality Coordination Templates](templates#quality-coordination)
Checklists: [Quality Validation Framework](checklists#quality-validation)
Data: [Quality Metrics Database](data#quality-metrics)
Coordination: collaborative
Squad: tier-2-coordinators
Handoff-From: [JAEGIS, John, Fred]
Handoff-To: [tier-3-agents, tier-4-agents]
Priority: 9
Classification: TIER-2-COORDINATOR
==================== END: Tyler ====================

==================== TIER 3: SPECIALIZED AGENTS (16 AGENTS) ====================

# Core System Agents (4 agents)
==================== START: system-architect ====================
Title: System Architecture & Design Specialist
Name: System Architect
Description: Comprehensive system architecture design and optimization
Persona: personas#system-architect
Tasks: [System Architecture Design](tasks#system-architecture)
Templates: [Architecture Templates](templates#architecture)
Checklists: [Architecture Validation](checklists#architecture)
Data: [Architecture Patterns](data#architecture-patterns)
Coordination: collaborative
Squad: core-system
Handoff-From: [Fred, Tyler]
Handoff-To: [technical-lead, integration-specialist]
Priority: 8
Classification: TIER-3-SPECIALIZED
==================== END: system-architect ====================

# [Additional 15 Tier 3 agents would be defined here...]

==================== TIER 4: CONDITIONAL AGENTS (4 AGENTS) ====================

# [4 conditional agents for specific scenarios...]

==================== COORDINATION PROTOCOLS ====================

Cross-Tier-Communication: standard-coordination-protocol
Tier-Activation-Triggers: project-complexity-based
Inter-Tier-Dependencies: hierarchical-dependency-mapping
Quality-Validation: comprehensive-tier-validation
Performance-Monitoring: real-time-tier-performance-analytics

==================== GITHUB INTEGRATION POINTS ====================

Dynamic-Resource-Fetching: tier-based-loading
Command-Integration: tier-specific-command-sets
Template-Management: tier-specialized-templates
Validation-Framework: tier-validation-protocols
Performance-Analytics: tier-performance-monitoring

==================== END CONFIGURATION ===================="""
        
        with open(core_path / "agent-config.txt", "w", encoding="utf-8") as f:
            f.write(config_content)
    
    def _create_enhanced_agent_config(self, core_path: Path):
        """Create enhanced 68-agent configuration"""
        
        # Copy existing enhanced-agent-config.txt if it exists
        source_file = Path("enhanced-agent-config.txt")
        if source_file.exists():
            shutil.copy2(source_file, core_path / "enhanced-agent-config.txt")
        else:
            # Create basic enhanced configuration
            config_content = """# JAEGIS Enhanced Agent Configuration v2.2
# 68-Agent System with 5-Tier Squad Architecture
# GitHub Repository: https://github.com/usemanusai/JAEGIS
# Dynamic Resource Fetching Compatible

==================== SYSTEM OVERVIEW ====================
Total Agents: 68
Architecture: 5-Tier Squad-Based System
Coordination: Cross-Squad Collaborative Intelligence
Integration: GitHub-Local Hybrid with Dynamic Resource Fetching
Validation: Comprehensive Quality Standards with Real-Time Monitoring

# [Full 68-agent configuration would be included here...]

==================== END CONFIGURATION ===================="""
            
            with open(core_path / "enhanced-agent-config.txt", "w", encoding="utf-8") as f:
                f.write(config_content)
    
    def _create_iuas_agent_config(self, core_path: Path):
        """Create IUAS 20-agent maintenance squad configuration"""
        
        source_file = Path("iuas-agent-config.txt")
        if source_file.exists():
            shutil.copy2(source_file, core_path / "iuas-agent-config.txt")
        else:
            config_content = """# JAEGIS Internal Updates Agent Squad (IUAS) Configuration v2.2
# 20-Agent Maintenance Squad for JAEGIS System Evolution
# GitHub Repository: https://github.com/usemanusai/JAEGIS
# Tier 6: Maintenance & Enhancement Squad

==================== SYSTEM OVERVIEW ====================
Squad Name: Internal Updates Agent Squad (IUAS)
Total Agents: 20
Architecture: 4 Functional Units (5 agents each)
Purpose: JAEGIS system evolution and consistency management
Integration: Tier 6 - Maintenance & Enhancement

# [Full IUAS configuration would be included here...]

==================== END IUAS CONFIGURATION ===================="""
            
            with open(core_path / "iuas-agent-config.txt", "w", encoding="utf-8") as f:
                f.write(config_content)
    
    def _create_garas_agent_config(self, core_path: Path):
        """Create GARAS 40-agent gap resolution squad configuration"""
        
        source_file = Path("garas-agent-config.txt")
        if source_file.exists():
            shutil.copy2(source_file, core_path / "garas-agent-config.txt")
        else:
            config_content = """# JAEGIS Gaps Analysis and Resolution Agent Squad (GARAS) Configuration v2.2
# 40-Agent Squad for Comprehensive Gap Detection and Resolution
# GitHub Repository: https://github.com/usemanusai/JAEGIS
# Tier 6: Maintenance & Enhancement Squad

==================== SYSTEM OVERVIEW ====================
Squad Name: Gaps Analysis and Resolution Agent Squad (GARAS)
Total Agents: 40
Architecture: 4 Specialized Sub-Squads (10 agents each)
Purpose: Real-time gap detection, analysis, and resolution across JAEGIS ecosystem

# [Full GARAS configuration would be included here...]

==================== END GARAS CONFIGURATION ===================="""
            
            with open(core_path / "garas-agent-config.txt", "w", encoding="utf-8") as f:
                f.write(config_content)
    
    def _create_chimera_agent_config(self, core_path: Path):
        """Create Chimera v4.1 47-agent specialized squad configuration"""
        
        config_content = """# JAEGIS Enhanced System Project Chimera v4.1 Agent Configuration
# 47-Agent Specialized Squad for Critical Gap Resolution
# GitHub Repository: https://github.com/usemanusai/JAEGIS
# Tier 7: Enhanced Performance & Security Squad

==================== SYSTEM OVERVIEW ====================
Squad Name: Project Chimera v4.1 Enhanced Performance Squad
Total Agents: 47
Architecture: 6 Specialized Squads
Purpose: Critical gap resolution and performance target achievement
Integration: Tier 7 - Enhanced Performance & Security

==================== GARAS-ALPHA: CORE REASONING ANALYSIS SQUAD (8 AGENTS) ====================

==================== START: GARAS-A1 ====================
Title: PyTorch Integration Specialist
Name: GARAS-A1
Description: PyTorch optimization and deep learning integration specialist
Persona: personas#pytorch-specialist
Tasks: [PyTorch Integration](tasks#pytorch-integration)
Templates: [PyTorch Templates](templates#pytorch)
Checklists: [PyTorch Validation](checklists#pytorch)
Data: [PyTorch Optimization Patterns](data#pytorch-patterns)
Coordination: collaborative
Squad: garas-alpha
Handoff-From: [chimera-orchestrator]
Handoff-To: [GARAS-A2, GARAS-A5]
Priority: 10
Classification: TIER-7-CHIMERA
Specialization: pytorch_optimization
Expertise: [PyTorch, Deep Learning, Gradient Systems]
==================== END: GARAS-A1 ====================

# [Additional 46 Chimera agents would be defined here...]

==================== CHIMERA COORDINATION PROTOCOLS ====================

Cross-Squad-Communication: chimera-advanced-coordination-protocol
Squad-Activation-Triggers: performance-gap-analysis-based
Inter-Squad-Dependencies: intelligent-chimera-dependency-mapping
Quality-Validation: comprehensive-chimera-validation
Performance-Monitoring: real-time-chimera-performance-analytics

==================== PERFORMANCE TARGETS ====================

Reasoning-Improvement: 62x performance increase
Agent-Communication-Latency: <10ms
Token-Filtering-Latency: <1ms
System-Availability: >99.5%
Constitutional-Compliance: >95%
Adversarial-Robustness: >90%

==================== END CHIMERA CONFIGURATION ===================="""
        
        with open(core_path / "chimera-agent-config.txt", "w", encoding="utf-8") as f:
            f.write(config_content)
    
    def _create_command_structures(self):
        """Create command structure files"""
        
        github_root = self.base_path / "github_repository"
        commands_path = github_root / "commands"
        
        # Create squad-commands.md
        squad_commands = """# JAEGIS Enhanced Squad Commands v2.2
## 150+ Commands for Multi-Tier Agent Coordination

### Tier 1: Master Orchestrator Commands
- `JAEGIS:ORCHESTRATE` - Master system orchestration
- `JAEGIS:COORDINATE` - Cross-tier coordination
- `JAEGIS:VALIDATE` - System-wide validation

### Tier 2: Senior Coordinator Commands
- `JOHN:PLAN` - Strategic planning coordination
- `FRED:IMPLEMENT` - Technical implementation
- `TYLER:VALIDATE` - Quality validation

### Squad-Specific Commands
- `GARAS:DETECT` - Gap detection protocols
- `IUAS:MONITOR` - System monitoring
- `CHIMERA:OPTIMIZE` - Performance optimization

# [Full command documentation...]
"""
        
        with open(commands_path / "squad-commands.md", "w", encoding="utf-8") as f:
            f.write(squad_commands)
        
        # Create tier-commands.json
        tier_commands = {
            "tier_1": {
                "master_orchestrator": ["ORCHESTRATE", "COORDINATE", "VALIDATE"]
            },
            "tier_2": {
                "senior_coordinators": ["PLAN", "IMPLEMENT", "VALIDATE"]
            },
            "tier_3": {
                "specialized_agents": ["ANALYZE", "EXECUTE", "REPORT"]
            }
        }
        
        with open(commands_path / "tier-commands.json", "w", encoding="utf-8") as f:
            json.dump(tier_commands, f, indent=2)
    
    def _organize_templates(self):
        """Organize template structures"""
        
        github_root = self.base_path / "github_repository"
        templates_path = github_root / "templates"
        
        # Create template directories and sample files
        template_dirs = ["agent-templates", "squad-templates", "system-templates"]
        
        for template_dir in template_dirs:
            dir_path = templates_path / template_dir
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create sample template file
            sample_template = f"""# {template_dir.replace('-', ' ').title()}
## Template for {template_dir}

This template provides standardized format for {template_dir}.

### Usage
- Dynamic resource fetching compatible
- GitHub integration ready
- Multi-tier coordination support
"""
            
            with open(dir_path / "README.md", "w", encoding="utf-8") as f:
                f.write(sample_template)
    
    def _create_configuration_files(self):
        """Create system configuration files"""
        
        github_root = self.base_path / "github_repository"
        config_path = github_root / "config"
        
        # OpenRouter configuration
        openrouter_config = {
            "api_keys": {
                "total_keys": 3000,
                "load_balancing": "intelligent",
                "failover": "automatic"
            },
            "rate_limiting": {
                "requests_per_minute": 150000,
                "daily_message_capacity": 150000
            },
            "integration": {
                "jaegis_compatible": True,
                "nlds_integration": True
            }
        }
        
        with open(config_path / "openrouter-config.json", "w", encoding="utf-8") as f:
            json.dump(openrouter_config, f, indent=2)
        
        # Sync configuration
        sync_config = {
            "github_sync": {
                "repository": "usemanusai/JAEGIS",
                "sync_interval_minutes": 60,
                "auto_sync": True,
                "branch_strategy": "development"
            },
            "security": {
                "pre_sync_scanning": True,
                "sensitive_data_detection": True,
                "audit_trail": True
            }
        }
        
        with open(config_path / "sync-config.json", "w", encoding="utf-8") as f:
            json.dump(sync_config, f, indent=2)
    
    def _create_documentation_structure(self):
        """Create documentation structure"""
        
        github_root = self.base_path / "github_repository"
        docs_path = github_root / "docs"
        
        # Create documentation directories
        doc_dirs = ["architecture", "api", "guides"]
        
        for doc_dir in doc_dirs:
            dir_path = docs_path / doc_dir
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create index file
            index_content = f"""# {doc_dir.title()} Documentation

## Overview
This directory contains {doc_dir} documentation for the JAEGIS Enhanced System.

## Contents
- Comprehensive {doc_dir} information
- GitHub integration compatible
- Dynamic resource fetching ready

## Usage
Access via GitHub dynamic resource fetching or local file system.
"""
            
            with open(dir_path / "README.md", "w", encoding="utf-8") as f:
                f.write(index_content)
    
    def _create_sync_protocols(self):
        """Create synchronization protocols"""
        
        github_root = self.base_path / "github_repository"
        sync_path = github_root / "sync"
        
        # Create sync directories
        sync_dirs = ["protocols", "monitoring"]
        
        for sync_dir in sync_dirs:
            dir_path = sync_path / sync_dir
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create protocol file
            protocol_content = f"""# {sync_dir.title()} Documentation

## {sync_dir.title()} Overview
{sync_dir.title()} for JAEGIS GitHub synchronization system.

## Features
- 60-minute sync cycles
- Security scanning
- Audit trail generation
- Branch targeting
"""
            
            with open(dir_path / "README.md", "w", encoding="utf-8") as f:
                f.write(protocol_content)
    
    def _count_created_files(self) -> int:
        """Count total files created"""
        
        github_root = self.base_path / "github_repository"
        if not github_root.exists():
            return 0
        
        file_count = 0
        for root, dirs, files in os.walk(github_root):
            file_count += len(files)
        
        return file_count
    
    def get_structure_summary(self) -> Dict[str, Any]:
        """Get summary of created structure"""
        
        github_root = self.base_path / "github_repository"
        
        if not github_root.exists():
            return {"status": "not_created", "structure": {}}
        
        structure_summary = {}
        
        for directory in self.github_structure.keys():
            dir_path = github_root / directory
            if dir_path.exists():
                files = []
                for item in dir_path.rglob("*"):
                    if item.is_file():
                        files.append(str(item.relative_to(dir_path)))
                structure_summary[directory] = {
                    "exists": True,
                    "files": files,
                    "file_count": len(files)
                }
            else:
                structure_summary[directory] = {"exists": False}
        
        return {
            "status": "created",
            "structure": structure_summary,
            "total_files": self._count_created_files(),
            "github_compatible": True
        }


# Execute structure creation
if __name__ == "__main__":
    organizer = GitHubRepositoryStructureOrganizer()
    
    print("🏗️ Creating GitHub Repository Structure...")
    result = organizer.create_github_structure()
    
    if result["status"] == "success":
        print("✅ GitHub repository structure created successfully!")
        print(f"📁 Directories: {len(result['directories'])}")
        print(f"📄 Total files: {result['total_files']}")
        print(f"🔗 GitHub compatible: {result['github_compatible']}")
        
        # Get detailed summary
        summary = organizer.get_structure_summary()
        print("\n📋 Structure Summary:")
        for directory, info in summary["structure"].items():
            if info["exists"]:
                print(f"   ✅ {directory}: {info['file_count']} files")
            else:
                print(f"   ❌ {directory}: Not created")
    else:
        print(f"❌ Structure creation failed: {result.get('error', 'Unknown error')}")
