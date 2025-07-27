import * as vscode from 'vscode';
import { JAEGISOrchestrator } from '../orchestrator/JAEGISOrchestrator';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
export declare class CommandManager {
    private orchestrator;
    private analyzer;
    private statusBar;
    private dakotaAgent;
    private phoenixAgent;
    private chronosAgent;
    constructor(orchestrator: JAEGISOrchestrator, analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager);
    /**
     * Register all JAEGIS commands with VS Code
     */
    registerCommands(context: vscode.ExtensionContext): Promise<void>;
    /**
     * Activate a specific JAEGIS mode
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
     * Auto-setup JAEGIS for current workspace
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
     * Open JAEGIS settings
     */
    private openSettings;
    /**
     * Show JAEGIS help information
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
}
//# sourceMappingURL=CommandManager.d.ts.map