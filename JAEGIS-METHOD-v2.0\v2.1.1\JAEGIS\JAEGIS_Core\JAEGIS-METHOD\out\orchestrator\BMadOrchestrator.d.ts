import * as vscode from 'vscode';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
import { JAEGISInitializer } from './JAEGISInitializer';
import { JAEGISMode, AgentId, ProjectAnalysis, WorkflowProgress } from '../types/JAEGISTypes';
export declare class JAEGISOrchestrator {
    private context;
    private analyzer;
    private statusBar;
    private initializer;
    private activeAgents;
    private currentMode?;
    private workflowProgress?;
    constructor(context: vscode.ExtensionContext, analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager, initializer: JAEGISInitializer);
    /**
     * Initialize workspace with JAEGIS structure
     */
    initializeWorkspace(workspaceFolder: vscode.WorkspaceFolder): Promise<void>;
    /**
     * Execute a specific JAEGIS mode
     */
    executeMode(mode: JAEGISMode, projectAnalysis: ProjectAnalysis): Promise<void>;
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
    getCurrentMode(): JAEGISMode | undefined;
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
//# sourceMappingURL=JAEGISOrchestrator.d.ts.map