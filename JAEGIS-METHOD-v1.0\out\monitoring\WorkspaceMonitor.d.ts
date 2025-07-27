import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { BMadOrchestrator } from '../orchestrator/BMadOrchestrator';
import { StatusBarManager } from '../ui/StatusBarManager';
export declare class WorkspaceMonitor {
    private analyzer;
    private orchestrator;
    private statusBar;
    private fileWatcher?;
    private diagnosticWatcher?;
    private configWatcher?;
    private changeTimeout?;
    private isMonitoring;
    private lastAnalysis?;
    constructor(analyzer: WorkspaceAnalyzer, orchestrator: BMadOrchestrator, statusBar: StatusBarManager);
    /**
     * Start monitoring workspace for changes
     */
    startMonitoring(): Promise<void>;
    /**
     * Stop monitoring workspace
     */
    stopMonitoring(): void;
    /**
     * Check if monitoring is active
     */
    isActive(): boolean;
    /**
     * Setup file system watcher for project files
     */
    private setupFileWatcher;
    /**
     * Setup diagnostic watcher for issue detection
     */
    private setupDiagnosticWatcher;
    /**
     * Setup configuration watcher
     */
    private setupConfigurationWatcher;
    /**
     * Handle configuration file changes
     */
    private onConfigFileChange;
    /**
     * Handle configuration file creation
     */
    private onConfigFileCreate;
    /**
     * Handle configuration file deletion
     */
    private onConfigFileDelete;
    /**
     * Handle VS Code diagnostics changes
     */
    private onDiagnosticsChange;
    /**
     * Handle BMAD configuration changes
     */
    private onBmadConfigurationChange;
    /**
     * Analyze project changes and suggest actions
     */
    private analyzeProjectChanges;
    /**
     * Suggest debug mode activation
     */
    private suggestDebugMode;
    /**
     * Suggest mode change
     */
    private suggestModeChange;
    /**
     * Suggest new agents
     */
    private suggestNewAgents;
    /**
     * Process VS Code diagnostics into project issues
     */
    private processDiagnostics;
    /**
     * Categorize diagnostic issue
     */
    private categorizeIssue;
    /**
     * Emit workspace event
     */
    private emitWorkspaceEvent;
    /**
     * Get agent display name
     */
    private getAgentDisplayName;
    /**
     * Dispose of all watchers and resources
     */
    dispose(): void;
}
//# sourceMappingURL=WorkspaceMonitor.d.ts.map