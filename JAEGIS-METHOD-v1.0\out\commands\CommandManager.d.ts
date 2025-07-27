import * as vscode from 'vscode';
import { BMadOrchestrator } from '../orchestrator/BMadOrchestrator';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
export declare class CommandManager {
    private orchestrator;
    private analyzer;
    private statusBar;
    private dakotaAgent;
    private phoenixAgent;
    private chronosAgent;
    private sentinelAgent;
    private metaOrchestratorAgent;
    private agentCreatorAgent;
    private webAgentCreatorAgent;
    private docQAAgent;
    private chunkyAgent;
    private synergyAgent;
    private context7;
    private logger;
    constructor(orchestrator: BMadOrchestrator, analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager);
    /**
     * Register all BMAD commands with VS Code
     */
    registerCommands(context: vscode.ExtensionContext): Promise<void>;
    /**
     * Activate a specific BMAD mode
     */
    private activateMode;
    /**
     * Show quick mode selection picker
     */
    private showQuickModeSelector;
    /**
     * Scan workspace and show analysis results
     */
    private scanWorkspace;
    /**
     * Auto-setup BMAD for current workspace
     */
    private autoSetup;
    /**
     * Detect and display technology stack
     */
    private detectTechStack;
    /**
     * Show agent selection interface
     */
    private showAgentSelector;
    /**
     * Perform agent handoff
     */
    private performAgentHandoff;
    /**
     * Perform project health check
     */
    private performHealthCheck;
    /**
     * Show detailed progress information
     */
    private showProgressDetails;
    /**
     * Show mode details
     */
    private showModeDetails;
    /**
     * Show error details
     */
    private showErrorDetails;
    /**
     * Handle configuration changes
     */
    private onConfigurationChanged;
    private getModeDisplayName;
    private getModeDescription;
    private getAgentDisplayName;
    private getAvailableAgents;
    private buildAnalysisMessage;
    private showAnalysisDetails;
    /**
     * Debug the currently active file
     */
    private debugCurrentFile;
    /**
     * Generate documentation for the currently active file
     */
    private documentCurrentFile;
    /**
     * Debug the currently selected code
     */
    private debugSelection;
    /**
     * Explain the current code context
     */
    private explainCode;
    /**
     * Generate tests for the current file
     */
    private generateTests;
    /**
     * Analyze a specific folder
     */
    private analyzeFolder;
    /**
     * Generate documentation for a specific folder
     */
    private generateDocsForFolder;
    /**
     * Refresh workspace analysis
     */
    private refreshAnalysis;
    /**
     * Open BMAD settings
     */
    private openSettings;
    /**
     * Show BMAD help information
     */
    private showHelp;
    private processDiagnostics;
    /**
     * Perform comprehensive dependency audit
     */
    private performDependencyAudit;
    /**
     * Perform dependency modernization
     */
    private performDependencyModernization;
    /**
     * Start background dependency monitoring
     */
    private startDependencyMonitoring;
    /**
     * Stop background dependency monitoring
     */
    private stopDependencyMonitoring;
    /**
     * Check for security vulnerabilities
     */
    private checkSecurityVulnerabilities;
    /**
     * Update outdated dependencies
     */
    private updateOutdatedDependencies;
    /**
     * Generate comprehensive dependency report
     */
    private generateDependencyReport;
    /**
     * Analyze dependency licenses
     */
    private analyzeDependencyLicenses;
    /**
     * Perform comprehensive deployment preparation
     */
    private performDeploymentPreparation;
    /**
     * Containerize the project
     */
    private containerizeProject;
    /**
     * Perform cross-platform setup
     */
    private performCrossPlatformSetup;
    /**
     * Generate deployment scripts
     */
    private generateDeploymentScripts;
    /**
     * Validate deployment configuration
     */
    private validateDeploymentConfig;
    /**
     * Perform deployment health check
     */
    private performDeploymentHealthCheck;
    /**
     * Perform deployment rollback
     */
    private performRollbackDeployment;
    /**
     * Generate deployment documentation
     */
    private generateDeploymentDocumentation;
    /**
     * Perform comprehensive version tracking
     */
    private performVersionTracking;
    /**
     * Perform real-time token monitoring
     */
    private performTokenMonitoring;
    /**
     * Perform model updates research
     */
    private performModelUpdatesResearch;
    /**
     * Generate version changelog
     */
    private generateVersionChangelog;
    /**
     * Optimize token usage
     */
    private optimizeTokenUsage;
    /**
     * Check current token limits
     */
    private checkTokenLimits;
    /**
     * Update model specifications
     */
    private updateModelSpecifications;
    /**
     * Generate token usage report
     */
    private generateTokenUsageReport;
    /**
     * Perform comprehensive task completion monitoring
     */
    private performTaskCompletionMonitoring;
    /**
     * Perform intelligent checklist validation
     */
    private performChecklistValidation;
    /**
     * Perform comprehensive quality assurance review
     */
    private performQualityAssuranceReview;
    /**
     * Generate comprehensive completion report
     */
    private generateCompletionReport;
    /**
     * Validate task completion criteria
     */
    private validateTaskCriteria;
    /**
     * Update task completion status
     */
    private updateCompletionStatus;
    /**
     * Monitor quality standards compliance
     */
    private monitorQualityStandards;
    /**
     * Generate quality assessment report
     */
    private generateQualityAssessment;
    /**
     * Perform comprehensive squad architecture monitoring
     */
    private performSquadArchitectureMonitoring;
    /**
     * Perform automated agent research and intelligence gathering
     */
    private performAgentResearchIntelligence;
    /**
     * Perform intelligent squad generation and design
     */
    private performSquadGenerationDesign;
    /**
     * Generate comprehensive squad specification document
     */
    private generateSquadSpecification;
    /**
     * Validate squad proposal against quality and safety standards
     */
    private validateSquadProposal;
    /**
     * Analyze squad evolution patterns and trends
     */
    private analyzeSquadEvolution;
    /**
     * Monitor agent performance across the BMAD ecosystem
     */
    private monitorAgentPerformance;
    /**
     * Generate comprehensive evolution report
     */
    private generateEvolutionReport;
    /**
     * Conceptualize new AI agent
     */
    private conceptualizeAgent;
    /**
     * Generate new AI agent implementation
     */
    private generateAgent;
    /**
     * Deploy generated agent
     */
    private deployAgent;
    /**
     * Generate agent brief
     */
    private generateAgentBrief;
    /**
     * Validate agent concept
     */
    private validateAgentConcept;
    /**
     * Analyze agent performance
     */
    private analyzeAgentPerformance;
    /**
     * Research agent models
     */
    private researchAgentModels;
    /**
     * Generate deployment plan
     */
    private generateDeploymentPlan;
    /**
     * Design web agent UI/UX
     */
    private designWebAgentUI;
    /**
     * Generate web agent implementation
     */
    private generateWebAgent;
    /**
     * Deploy generated web agent
     */
    private deployWebAgent;
    /**
     * Generate web agent specification
     */
    private generateWebAgentSpec;
    /**
     * Validate web agent design
     */
    private validateWebAgentDesign;
    /**
     * Analyze web agent performance
     */
    private analyzeWebAgentPerformance;
    /**
     * Research web technologies
     */
    private researchWebTechnologies;
    /**
     * Generate style guide
     */
    private generateStyleGuide;
    /**
     * Analyze documentation quality and structure
     */
    private analyzeDocumentation;
    /**
     * Validate documentation standards and compliance
     */
    private validateDocumentationStandards;
    /**
     * Generate comprehensive documentation quality report
     */
    private generateDocumentationReport;
    /**
     * Improve documentation based on analysis results
     */
    private improveDocumentation;
    /**
     * Audit content quality and accuracy
     */
    private auditContentQuality;
    /**
     * Generate documentation specification
     */
    private generateDocumentationSpec;
    /**
     * Create documentation style guide
     */
    private createStyleGuide;
    /**
     * Research documentation best practices
     */
    private researchDocumentationBestPractices;
    /**
     * Format documentation report for display
     */
    private formatDocumentationReport;
    /**
     * Decompose complex tasks into manageable chunks
     */
    private decomposeTask;
    /**
     * Orchestrate multi-agent execution
     */
    private orchestrateExecution;
    /**
     * Perform background optimization
     */
    private performBackgroundOptimization;
    /**
     * Generate task decomposition plan
     */
    private generateDecompositionPlan;
    /**
     * Create execution orchestration framework
     */
    private createOrchestrationFramework;
    /**
     * Research task management best practices
     */
    private researchTaskManagementBestPractices;
    /**
     * Monitor task execution
     */
    private monitorTaskExecution;
    /**
     * Optimize resource allocation
     */
    private optimizeResourceAllocation;
    /**
     * Validate dependencies and perform future-proofing
     */
    private validateDependenciesFutureProofing;
    /**
     * Perform code polish and refinement
     */
    private performCodePolishRefinement;
    /**
     * Perform AI integration and enhancement
     */
    private performAIIntegrationEnhancement;
    /**
     * Generate integrated enhancement plan
     */
    private generateIntegratedEnhancementPlan;
    /**
     * Create AI integration framework
     */
    private createAIIntegrationFramework;
    /**
     * Research integrated development best practices
     */
    private researchIntegratedDevelopmentBestPractices;
    /**
     * Monitor enhancement progress
     */
    private monitorEnhancementProgress;
    /**
     * Optimize project synergy
     */
    private optimizeProjectSynergy;
}
//# sourceMappingURL=CommandManager.d.ts.map