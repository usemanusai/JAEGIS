import { BMadMode, AgentId, WorkflowProgress, ProjectIssue, StatusBarInfo } from '../types/BMadTypes';
export declare class StatusBarManager {
    private statusBarItem;
    private progressItem;
    private issueItem;
    private currentInfo;
    constructor();
    /**
     * Initialize status bar with default state
     */
    initialize(): void;
    /**
     * Update status bar with current mode and agents
     */
    updateMode(mode: BMadMode, agents?: AgentId[]): void;
    /**
     * Update progress information
     */
    updateProgress(progress: WorkflowProgress): void;
    /**
     * Update issue information
     */
    updateIssues(issues: ProjectIssue[]): void;
    /**
     * Show error state
     */
    showError(message: string, command?: string): void;
    /**
     * Show loading state
     */
    showLoading(message: string): void;
    /**
     * Show success state
     */
    showSuccess(message: string, command?: string): void;
    /**
     * Show info state
     */
    showInfo(message: string, command?: string): void;
    /**
     * Clear all status items
     */
    clear(): void;
    /**
     * Get current status information
     */
    getCurrentInfo(): StatusBarInfo;
    /**
     * Dispose of status bar items
     */
    dispose(): void;
    private getModeDisplayName;
    private getAgentDisplayName;
    private buildModeTooltip;
    private buildProgressTooltip;
    private buildIssueTooltip;
    private getModeDescription;
}
//# sourceMappingURL=StatusBarManager.d.ts.map