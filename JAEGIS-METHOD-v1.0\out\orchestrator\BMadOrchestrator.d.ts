import * as vscode from 'vscode';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadInitializer } from './BMadInitializer';
import { BMadMode, AgentId, ProjectAnalysis, WorkflowProgress } from '../types/BMadTypes';
export declare class BMadOrchestrator {
    private context;
    private analyzer;
    private statusBar;
    private initializer;
    private activeAgents;
    private currentMode?;
    private workflowProgress?;
    constructor(context: vscode.ExtensionContext, analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager, initializer: BMadInitializer);
    /**
     * Initialize workspace with BMAD structure
     */
    initializeWorkspace(workspaceFolder: vscode.WorkspaceFolder): Promise<void>;
    /**
     * Execute a specific BMAD mode
     */
    executeMode(mode: BMadMode, projectAnalysis: ProjectAnalysis): Promise<void>;
    /**
     * Activate specific AI agents
     */
    activateAgents(agentIds: AgentId[]): Promise<void>;
    /**
     * Get currently active agents
     */
    getActiveAgents(): AgentId[];
    /**
     * Get current mode
     */
    getCurrentMode(): BMadMode | undefined;
    /**
     * Update workflow progress
     */
    updateProgress(progress: Partial<WorkflowProgress>): void;
    /**
     * Create execution context for mode
     */
    private createExecutionContext;
    /**
     * Initialize workflow progress tracking
     */
    private initializeWorkflowProgress;
    /**
     * Execute workflow based on mode
     */
    private executeWorkflow;
    /**
     * Execute Documentation Mode workflow
     */
    private executeDocumentationMode;
    /**
     * Execute Full Development Mode workflow
     */
    private executeFullDevelopmentMode;
    /**
     * Execute Continue Project Mode workflow
     */
    private executeContinueProjectMode;
    /**
     * Execute Task Overview Mode workflow
     */
    private executeTaskOverviewMode;
    /**
     * Execute Debug Mode workflow
     */
    private executeDebugMode;
    /**
     * Execute Continuous Execution Mode workflow
     */
    private executeContinuousExecutionMode;
    /**
     * Execute Feature Gap Analysis Mode workflow
     */
    private executeFeatureGapAnalysisMode;
    /**
     * Execute GitHub Integration Mode workflow
     */
    private executeGithubIntegrationMode;
    private getExistingArtifacts;
    private getModeTaskList;
    private delay;
    private openGeneratedDocuments;
    private analyzeExistingProjectState;
    private showContinuationOptions;
    private generateTaskDashboard;
    private processDiagnostics;
}
//# sourceMappingURL=BMadOrchestrator.d.ts.map