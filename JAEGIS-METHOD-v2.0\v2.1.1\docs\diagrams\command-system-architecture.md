# ⚡ **JAEGIS v2.2 Command System Architecture**

## **Overview**
This diagram illustrates the comprehensive command system with 150+ specialized commands, categorization structure, mode selection flow, infrastructure protection protocols, and authorization mechanisms.

## **Command System Architecture**

```mermaid
graph TB
    %% JAEGIS v2.2 Command System Architecture - 150+ Commands
    
    %% Command System Entry Point
    CommandSystem[🎯 JAEGIS Command System<br/>150+ Specialized Commands<br/>5 Operational Modes]
    
    %% Mode Selection Commands
    ModeCommands[🎮 Mode Selection Commands]
    ModeSelect[/mode-select<br/>Display enhanced mode menu]
    ModeDoc[/mode-doc<br/>Activate Documentation Mode]
    ModeStandard[/mode-standard<br/>Activate Standard Mode]
    ModeEnhanced[/mode-enhanced<br/>Activate Enhanced Mode]
    ModeAI[/mode-ai-system<br/>Activate AI System Mode]
    ModeCreator[/mode-agent-creator<br/>Activate Agent Creator Mode]
    
    %% Core System Commands
    CoreCommands[⚙️ Core System Commands]
    JAEGISStatus[/jaegis-status<br/>Display system status]
    JAEGISOptimize[/jaegis-optimize<br/>System-wide optimization]
    JAEGISReset[/jaegis-reset<br/>Reset orchestrator state]
    JAEGISAnalytics[/jaegis-analytics<br/>System analytics]
    
    %% Squad Management Commands
    SquadCommands[👥 Squad Management Commands]
    SquadList[/squad-list<br/>List all squads]
    SquadActivate[/squad-activate [name]<br/>Activate specific squad]
    SquadDeactivate[/squad-deactivate [name]<br/>Deactivate squad]
    SquadStatus[/squad-status [name]<br/>Squad status and health]
    SquadOptimize[/squad-optimize [name]<br/>Optimize squad performance]
    
    %% Infrastructure Protection Commands
    InfraCommands[🛡️ Infrastructure Protection Commands]
    InfraLock[/jaegis-lock-infrastructure<br/>Activate protection protocol]
    InfraUnlock[/jaegis-unlock-infrastructure<br/>Deactivate protection]
    InfraStatus[/jaegis-infrastructure-status<br/>Protection status & audit]
    InfraAudit[/jaegis-protection-audit<br/>Generate audit report]
    InfraScan[/jaegis-security-scan<br/>Security scan]
    
    %% Primary Leadership Commands
    LeadershipCommands[👔 Primary Leadership Commands]
    
    %% John Commands
    JohnCommands[👔 John (Product Manager)]
    JohnSwitch[/john<br/>Switch to John persona]
    ProductStrategy[/product-strategy<br/>Product strategy framework]
    StakeholderAnalysis[/stakeholder-analysis<br/>Stakeholder analysis]
    MarketIntel[/market-intelligence<br/>Market intelligence data]
    ProductRoadmap[/product-roadmap<br/>Generate roadmap]
    
    %% Fred Commands
    FredCommands[🏗️ Fred (Architect)]
    FredSwitch[/fred<br/>Switch to Fred persona]
    ArchDesign[/architecture-design<br/>Architecture framework]
    TechReview[/technical-review<br/>Technical review]
    SystemCoherence[/system-coherence<br/>Architectural coherence]
    TechStrategy[/tech-strategy<br/>Technical strategy]
    
    %% Tyler Commands
    TylerCommands[⚡ Tyler (Task Specialist)]
    TylerSwitch[/tyler<br/>Switch to Tyler persona]
    TaskCoordinate[/task-coordinate<br/>Task coordination]
    ExecutionOptimize[/execution-optimize<br/>Execution optimization]
    OperationalReview[/operational-review<br/>Operational review]
    TaskAnalytics[/task-analytics<br/>Task analytics]
    
    %% Phase 5 Enhanced Commands
    Phase5Commands[🚀 Phase 5 Enhanced Commands]
    
    %% IUAS Commands
    IUASCommands[🔧 IUAS Commands]
    IUASActivate[/iuas-activate<br/>Activate IUAS squad]
    IUASStatus[/iuas-status<br/>IUAS status & health]
    IUASMonitor[/iuas-monitor<br/>System monitoring]
    IUASUpdateCoord[/iuas-update-coordinate<br/>Update coordination]
    IUASChangeImpl[/iuas-change-implement<br/>Change implementation]
    IUASDocumentation[/iuas-documentation<br/>Maintenance docs]
    
    %% GARAS Commands
    GARASCommands[🎯 GARAS Commands]
    GARASActivate[/garas-activate<br/>Activate GARAS squad]
    GARASScan[/garas-scan<br/>Gap analysis]
    GARASResearch[/garas-research<br/>15-20 research queries]
    GARASSimulate[/garas-simulate<br/>High-speed simulation]
    GARASImplement[/garas-implement<br/>Gap resolution]
    GARASLearn[/garas-learn<br/>Meta-cognitive learning]
    
    %% A.M.A.S.I.A.P. Protocol Commands
    AMASIAPCommands[🔄 A.M.A.S.I.A.P. Protocol]
    AMASIAPActivate[/amasiap-activate<br/>Activate protocol]
    AMASIAPStatus[/amasiap-status<br/>Protocol status]
    AMASIAPConfigure[/amasiap-configure<br/>Configure parameters]
    AMASIAPAnalytics[/amasiap-analytics<br/>Enhancement analytics]
    
    %% Enhanced OpenRouter Commands
    OpenRouterCommands[🤖 Enhanced OpenRouter.ai]
    OpenRouterStatus[/openrouter-status<br/>API key pool status]
    OpenRouterBalance[/openrouter-balance<br/>Load balancing]
    OpenRouterOptimize[/openrouter-optimize<br/>Key optimization]
    OpenRouterFailover[/openrouter-failover<br/>Failover testing]
    OpenRouterAnalytics[/openrouter-analytics<br/>Usage analytics]
    
    %% GitHub Sync Commands
    GitHubSyncCommands[🔄 GitHub Sync Commands]
    GitHubSyncStart[/github-sync-start<br/>Start sync]
    GitHubSyncStop[/github-sync-stop<br/>Stop sync]
    GitHubSyncStatus[/github-sync-status<br/>Sync status]
    GitHubSecScan[/github-security-scan<br/>Security scan]
    GitHubDocsGen[/github-docs-generate<br/>Generate docs]
    
    %% Cross-Squad Coordination Commands
    CrossSquadCommands[🔗 Cross-Squad Coordination]
    CrossSquadSync[/cross-squad-sync<br/>Multi-squad sync]
    MultiSquadActivate[/multi-squad-activate<br/>Multiple activation]
    SquadHandoff[/squad-handoff<br/>Handoff management]
    CrossSquadValidate[/cross-squad-validate<br/>Cross-validation]
    SquadPerformance[/squad-performance<br/>Performance analysis]
    
    %% Emergency and Maintenance Commands
    EmergencyCommands[🚨 Emergency & Maintenance]
    EmergencyStop[/emergency-stop<br/>Emergency stop]
    SafeMode[/safe-mode<br/>Safe mode operation]
    DiagnosticFull[/diagnostic-full<br/>Full diagnostics]
    MaintenanceMode[/maintenance-mode<br/>Maintenance mode]
    RecoveryMode[/recovery-mode<br/>Recovery mode]
    SystemRestore[/system-restore<br/>System restore]
    
    %% Help and Documentation Commands
    HelpCommands[📚 Help & Documentation]
    Help[/help<br/>Basic help]
    HelpEnhanced[/help-enhanced<br/>Enhanced system help]
    HelpSquads[/help-squads<br/>Squad-specific help]
    HelpCommandsCmd[/help-commands<br/>All commands]
    Docs[/docs<br/>Access documentation]
    Examples[/examples<br/>Command examples]
    
    %% Command Authorization Flow
    AuthFlow[🔐 Command Authorization Flow]
    UserInput[👤 User Input]
    AuthCheck[🔍 Authorization Check]
    InfraProtCheck[🛡️ Infrastructure Protection Check]
    CommandExecution[⚡ Command Execution]
    AuditLog[📊 Audit Logging]
    
    %% Command Flow Connections
    CommandSystem --> ModeCommands
    CommandSystem --> CoreCommands
    CommandSystem --> SquadCommands
    CommandSystem --> InfraCommands
    CommandSystem --> LeadershipCommands
    CommandSystem --> Phase5Commands
    CommandSystem --> CrossSquadCommands
    CommandSystem --> EmergencyCommands
    CommandSystem --> HelpCommands
    
    %% Mode Commands
    ModeCommands --> ModeSelect
    ModeCommands --> ModeDoc
    ModeCommands --> ModeStandard
    ModeCommands --> ModeEnhanced
    ModeCommands --> ModeAI
    ModeCommands --> ModeCreator
    
    %% Core Commands
    CoreCommands --> JAEGISStatus
    CoreCommands --> JAEGISOptimize
    CoreCommands --> JAEGISReset
    CoreCommands --> JAEGISAnalytics
    
    %% Squad Management
    SquadCommands --> SquadList
    SquadCommands --> SquadActivate
    SquadCommands --> SquadDeactivate
    SquadCommands --> SquadStatus
    SquadCommands --> SquadOptimize
    
    %% Infrastructure Protection
    InfraCommands --> InfraLock
    InfraCommands --> InfraUnlock
    InfraCommands --> InfraStatus
    InfraCommands --> InfraAudit
    InfraCommands --> InfraScan
    
    %% Leadership Commands
    LeadershipCommands --> JohnCommands
    LeadershipCommands --> FredCommands
    LeadershipCommands --> TylerCommands
    
    %% John Commands
    JohnCommands --> JohnSwitch
    JohnCommands --> ProductStrategy
    JohnCommands --> StakeholderAnalysis
    JohnCommands --> MarketIntel
    JohnCommands --> ProductRoadmap
    
    %% Fred Commands
    FredCommands --> FredSwitch
    FredCommands --> ArchDesign
    FredCommands --> TechReview
    FredCommands --> SystemCoherence
    FredCommands --> TechStrategy
    
    %% Tyler Commands
    TylerCommands --> TylerSwitch
    TylerCommands --> TaskCoordinate
    TylerCommands --> ExecutionOptimize
    TylerCommands --> OperationalReview
    TylerCommands --> TaskAnalytics
    
    %% Phase 5 Commands
    Phase5Commands --> IUASCommands
    Phase5Commands --> GARASCommands
    Phase5Commands --> AMASIAPCommands
    Phase5Commands --> OpenRouterCommands
    Phase5Commands --> GitHubSyncCommands
    
    %% IUAS Commands
    IUASCommands --> IUASActivate
    IUASCommands --> IUASStatus
    IUASCommands --> IUASMonitor
    IUASCommands --> IUASUpdateCoord
    IUASCommands --> IUASChangeImpl
    IUASCommands --> IUASDocumentation
    
    %% GARAS Commands
    GARASCommands --> GARASActivate
    GARASCommands --> GARASScan
    GARASCommands --> GARASResearch
    GARASCommands --> GARASSimulate
    GARASCommands --> GARASImplement
    GARASCommands --> GARASLearn
    
    %% A.M.A.S.I.A.P. Commands
    AMASIAPCommands --> AMASIAPActivate
    AMASIAPCommands --> AMASIAPStatus
    AMASIAPCommands --> AMASIAPConfigure
    AMASIAPCommands --> AMASIAPAnalytics
    
    %% OpenRouter Commands
    OpenRouterCommands --> OpenRouterStatus
    OpenRouterCommands --> OpenRouterBalance
    OpenRouterCommands --> OpenRouterOptimize
    OpenRouterCommands --> OpenRouterFailover
    OpenRouterCommands --> OpenRouterAnalytics
    
    %% GitHub Sync Commands
    GitHubSyncCommands --> GitHubSyncStart
    GitHubSyncCommands --> GitHubSyncStop
    GitHubSyncCommands --> GitHubSyncStatus
    GitHubSyncCommands --> GitHubSecScan
    GitHubSyncCommands --> GitHubDocsGen
    
    %% Cross-Squad Commands
    CrossSquadCommands --> CrossSquadSync
    CrossSquadCommands --> MultiSquadActivate
    CrossSquadCommands --> SquadHandoff
    CrossSquadCommands --> CrossSquadValidate
    CrossSquadCommands --> SquadPerformance
    
    %% Emergency Commands
    EmergencyCommands --> EmergencyStop
    EmergencyCommands --> SafeMode
    EmergencyCommands --> DiagnosticFull
    EmergencyCommands --> MaintenanceMode
    EmergencyCommands --> RecoveryMode
    EmergencyCommands --> SystemRestore
    
    %% Help Commands
    HelpCommands --> Help
    HelpCommands --> HelpEnhanced
    HelpCommands --> HelpSquads
    HelpCommands --> HelpCommandsCmd
    HelpCommands --> Docs
    HelpCommands --> Examples
    
    %% Authorization Flow
    UserInput --> AuthCheck
    AuthCheck --> InfraProtCheck
    InfraProtCheck --> CommandExecution
    CommandExecution --> AuditLog
    
    %% Infrastructure Protection Integration
    InfraLock -.-> |Blocks| CommandExecution
    InfraUnlock -.-> |Enables| CommandExecution
    InfraStatus -.-> |Monitors| AuthCheck
    
    %% Styling
    classDef system fill:#ff6b6b,stroke:#333,stroke-width:3px,color:#fff
    classDef category fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff
    classDef command fill:#45b7d1,stroke:#333,stroke-width:1px,color:#fff
    classDef phase5 fill:#ff9ff3,stroke:#333,stroke-width:2px,color:#fff
    classDef security fill:#dc3545,stroke:#333,stroke-width:2px,color:#fff
    classDef auth fill:#28a745,stroke:#333,stroke-width:2px,color:#fff
    classDef emergency fill:#fd7e14,stroke:#333,stroke-width:2px,color:#fff
    
    class CommandSystem system
    class ModeCommands,CoreCommands,SquadCommands,LeadershipCommands,Phase5Commands,CrossSquadCommands,HelpCommands category
    class InfraCommands,InfraLock,InfraUnlock,InfraStatus,InfraAudit,InfraScan security
    class Phase5Commands,IUASCommands,GARASCommands,AMASIAPCommands,OpenRouterCommands,GitHubSyncCommands phase5
    class EmergencyCommands,EmergencyStop,SafeMode,DiagnosticFull,MaintenanceMode,RecoveryMode,SystemRestore emergency
    class AuthFlow,UserInput,AuthCheck,InfraProtCheck,CommandExecution,AuditLog auth
```

## **Command Categories**

### **🎮 Mode Selection Commands (6 Commands)**
- `/mode-select` - Display enhanced mode selection menu
- `/mode-doc` - Activate Documentation Mode (3 agents)
- `/mode-standard` - Activate Standard Development Mode (24 agents)
- `/mode-enhanced` - Activate Enhanced Development Mode (68 agents)
- `/mode-ai-system` - Activate AI System Mode (GitHub-hosted)
- `/mode-agent-creator` - Activate Agent Creator Mode (128 agents)

### **⚙️ Core System Commands (4 Commands)**
- `/jaegis-status` - Display comprehensive system status
- `/jaegis-optimize` - Execute system-wide optimization
- `/jaegis-reset` - Reset orchestrator to initial state
- `/jaegis-analytics` - Generate system analytics report

### **👥 Squad Management Commands (5 Commands)**
- `/squad-list` - List all available squads and status
- `/squad-activate [name]` - Activate specific squad by name
- `/squad-deactivate [name]` - Deactivate specific squad
- `/squad-status [name]` - Get detailed squad status and health
- `/squad-optimize [name]` - Optimize squad performance

### **🛡️ Infrastructure Protection Commands (5 Commands)**
- `/jaegis-lock-infrastructure` - Activate protection protocol
- `/jaegis-unlock-infrastructure` - Deactivate protection
- `/jaegis-infrastructure-status` - Protection status and audit
- `/jaegis-protection-audit` - Generate comprehensive audit report
- `/jaegis-security-scan` - Execute security vulnerability scan

### **👔 Primary Leadership Commands (15 Commands)**

#### **John (Product Manager) - 5 Commands**
- `/john` - Switch to John persona
- `/product-strategy` - Product strategy framework
- `/stakeholder-analysis` - Stakeholder analysis
- `/market-intelligence` - Market intelligence data
- `/product-roadmap` - Generate product roadmap

#### **Fred (System Architect) - 5 Commands**
- `/fred` - Switch to Fred persona
- `/architecture-design` - Architecture framework
- `/technical-review` - Technical review process
- `/system-coherence` - Architectural coherence check
- `/tech-strategy` - Technical strategy development

#### **Tyler (Task Specialist) - 5 Commands**
- `/tyler` - Switch to Tyler persona
- `/task-coordinate` - Task coordination protocols
- `/execution-optimize` - Execution optimization
- `/operational-review` - Operational review process
- `/task-analytics` - Task performance analytics

### **🚀 Phase 5 Enhanced Commands (30 Commands)**

#### **🔧 IUAS Commands (6 Commands)**
- `/iuas-activate` - Activate IUAS maintenance squad
- `/iuas-status` - IUAS squad status and health
- `/iuas-monitor` - System monitoring dashboard
- `/iuas-update-coordinate` - Update coordination protocols
- `/iuas-change-implement` - Change implementation process
- `/iuas-documentation` - Maintenance documentation

#### **🎯 GARAS Commands (6 Commands)**
- `/garas-activate` - Activate GARAS gap resolution squad
- `/garas-scan` - Execute comprehensive gap analysis
- `/garas-research` - Execute 15-20 research queries
- `/garas-simulate` - High-speed simulation testing
- `/garas-implement` - Gap resolution implementation
- `/garas-learn` - Meta-cognitive learning process

#### **🔄 A.M.A.S.I.A.P. Protocol Commands (4 Commands)**
- `/amasiap-activate` - Activate enhancement protocol
- `/amasiap-status` - Protocol status and metrics
- `/amasiap-configure` - Configure protocol parameters
- `/amasiap-analytics` - Enhancement analytics report

#### **🤖 Enhanced OpenRouter Commands (5 Commands)**
- `/openrouter-status` - API key pool status
- `/openrouter-balance` - Load balancing status
- `/openrouter-optimize` - Key optimization process
- `/openrouter-failover` - Failover testing
- `/openrouter-analytics` - Usage analytics report

#### **🔄 GitHub Sync Commands (5 Commands)**
- `/github-sync-start` - Start automated sync
- `/github-sync-stop` - Stop automated sync
- `/github-sync-status` - Sync status and metrics
- `/github-security-scan` - Pre-sync security scan
- `/github-docs-generate` - Generate documentation

#### **🔗 Cross-Squad Coordination Commands (5 Commands)**
- `/cross-squad-sync` - Multi-squad synchronization
- `/multi-squad-activate` - Multiple squad activation
- `/squad-handoff` - Intelligent handoff management
- `/cross-squad-validate` - Cross-squad validation
- `/squad-performance` - Performance analysis

### **🚨 Emergency & Maintenance Commands (6 Commands)**
- `/emergency-stop` - Emergency system stop
- `/safe-mode` - Activate safe mode operation
- `/diagnostic-full` - Full system diagnostics
- `/maintenance-mode` - Enter maintenance mode
- `/recovery-mode` - Activate recovery mode
- `/system-restore` - System restore from backup

### **📚 Help & Documentation Commands (6 Commands)**
- `/help` - Basic help and command overview
- `/help-enhanced` - Enhanced system help
- `/help-squads` - Squad-specific help
- `/help-commands` - Complete command reference
- `/docs` - Access documentation
- `/examples` - Command usage examples

## **Command Authorization Flow**

### **Security Pipeline**
1. **User Input**: Command entered by user
2. **Authorization Check**: Role-based permission validation
3. **Infrastructure Protection Check**: Lock/unlock status verification
4. **Command Execution**: Authorized command execution
5. **Audit Logging**: Comprehensive action logging

### **Infrastructure Protection Integration**
- **Lock State**: `/jaegis-lock-infrastructure` blocks architectural changes
- **Unlock State**: `/jaegis-unlock-infrastructure` enables modifications
- **Status Monitoring**: `/jaegis-infrastructure-status` provides real-time status
- **Audit Trail**: All commands logged with AES-256 encryption

## **Command Usage Examples**

### **Basic Operations**
```bash
# Check system status
/jaegis-status

# Activate Agent Creator Mode
/mode-agent-creator

# Activate development squad
/squad-activate development

# Check squad status
/squad-status development
```

### **Advanced Operations**
```bash
# Lock infrastructure for protection
/jaegis-lock-infrastructure

# Activate GARAS for gap analysis
/garas-activate
/garas-scan

# Start GitHub synchronization
/github-sync-start

# Generate comprehensive audit
/jaegis-protection-audit
```

### **Emergency Procedures**
```bash
# Emergency stop
/emergency-stop

# Enter safe mode
/safe-mode

# Full diagnostics
/diagnostic-full

# System recovery
/recovery-mode
```

## **Command Categories Summary**

| Category | Commands | Purpose |
|----------|----------|---------|
| Mode Selection | 6 | Operational mode management |
| Core System | 4 | Basic system operations |
| Squad Management | 5 | Squad coordination |
| Infrastructure Protection | 5 | Security and protection |
| Leadership | 15 | Persona-based operations |
| Phase 5 Enhanced | 30 | Advanced capabilities |
| Cross-Squad Coordination | 5 | Multi-squad operations |
| Emergency & Maintenance | 6 | Emergency procedures |
| Help & Documentation | 6 | User assistance |
| **Total** | **82+** | **Comprehensive control** |

*Note: Additional specialized commands available in squad-specific contexts*

## **Usage Context**

This command system provides:
- **Comprehensive Control**: 150+ commands for all system aspects
- **Security Integration**: Infrastructure protection and audit trails
- **Mode-Based Operation**: Commands adapt to current operational mode
- **Emergency Procedures**: Complete emergency response capabilities
- **User Assistance**: Comprehensive help and documentation system

---

*For security details, see [Security Framework](security-protection-framework.md)*  
*For GitHub integration, see [GitHub Integration Flow](github-integration-flow.md)*
