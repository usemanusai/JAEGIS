import { Context7Integration, Context7ResearchResult } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Task Monitoring Integration for Sentinel Agent
 * Provides real-time task tracking, completion detection, and quality validation
 * with intelligent Context7 research integration for task management best practices
 */
export interface TaskMonitoringConfig {
    enableRealTimeMonitoring: boolean;
    monitoringInterval: number;
    qualityThresholds: QualityThresholds;
    notificationSettings: NotificationSettings;
    validationRules: ValidationRules;
}
export interface QualityThresholds {
    minimumQualityScore: number;
    criticalDefectThreshold: number;
    stakeholderSatisfactionThreshold: number;
    completionPercentageThreshold: number;
}
export interface NotificationSettings {
    enableCompletionNotifications: boolean;
    enableQualityAlerts: boolean;
    enableStakeholderNotifications: boolean;
    notificationChannels: ('vscode' | 'email' | 'slack')[];
}
export interface ValidationRules {
    requireStakeholderApproval: boolean;
    requireQualityGateValidation: boolean;
    requireDocumentationUpdate: boolean;
    requireTestingCompletion: boolean;
}
export interface TaskMonitoringMetrics {
    totalTasksMonitored: number;
    tasksCompleted: number;
    tasksInProgress: number;
    tasksBlocked: number;
    averageQualityScore: number;
    averageCompletionTime: number;
    stakeholderSatisfactionAverage: number;
    qualityTrend: 'improving' | 'stable' | 'declining';
}
export interface TaskCompletionEvent {
    taskId: string;
    taskName: string;
    completionTimestamp: Date;
    qualityScore: number;
    validationResult: 'passed' | 'failed' | 'pending';
    stakeholderApprovals: StakeholderApproval[];
    context7Insights?: Context7ResearchResult;
}
export interface StakeholderApproval {
    stakeholderRole: string;
    approvalStatus: 'approved' | 'rejected' | 'pending';
    approvalTimestamp?: Date;
    comments: string;
}
export interface QualityValidationResult {
    taskId: string;
    overallQualityScore: number;
    qualityDimensions: QualityDimensionResult[];
    complianceChecks: ComplianceCheck[];
    improvementRecommendations: string[];
    validationTimestamp: Date;
}
export interface QualityDimensionResult {
    dimension: string;
    score: number;
    threshold: number;
    status: 'passed' | 'failed' | 'warning';
    details: string;
}
export interface ComplianceCheck {
    checkName: string;
    status: 'compliant' | 'non_compliant' | 'partial';
    details: string;
    remediation?: string;
}
export interface TaskAlert {
    alertId: string;
    taskId: string;
    alertType: 'quality_issue' | 'completion_delay' | 'stakeholder_approval_pending' | 'validation_failure';
    severity: 'critical' | 'high' | 'medium' | 'low';
    message: string;
    timestamp: Date;
    actionRequired: boolean;
    recommendedActions: string[];
}
/**
 * Task Monitoring Integration for real-time task tracking and quality validation
 */
export declare class TaskMonitoringIntegration {
    private context7;
    private statusBar;
    private config;
    private monitoringTimer;
    private taskEventListeners;
    private qualityValidationListeners;
    private alertListeners;
    private metrics;
    private isActive;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, config?: Partial<TaskMonitoringConfig>);
    /**
     * Start real-time task monitoring
     */
    startMonitoring(): Promise<void>;
    /**
     * Stop task monitoring
     */
    stopMonitoring(): void;
    /**
     * Monitor task completion for a specific task
     */
    monitorTaskCompletion(taskId: string): Promise<TaskCompletionEvent | null>;
    /**
     * Perform comprehensive quality validation for a task
     */
    performQualityValidation(taskId: string): Promise<QualityValidationResult>;
    /**
     * Generate task completion and quality alerts
     */
    generateTaskAlerts(completionEvent: TaskCompletionEvent, qualityResult: QualityValidationResult): Promise<TaskAlert[]>;
    /**
     * Get current task monitoring metrics
     */
    getMetrics(): TaskMonitoringMetrics;
    /**
     * Update task monitoring configuration
     */
    updateConfig(newConfig: Partial<TaskMonitoringConfig>): void;
    /**
     * Add event listeners
     */
    onTaskCompletion(listener: (event: TaskCompletionEvent) => void): void;
    onQualityValidation(listener: (result: QualityValidationResult) => void): void;
    onAlert(listener: (alert: TaskAlert) => void): void;
    /**
     * Check if monitoring is active
     */
    isActive(): boolean;
    /**
     * Private helper methods
     */
    private startPeriodicMonitoring;
    private performPeriodicCheck;
    private initializeTaskFileWatchers;
    private handleTaskFileChange;
    private getTaskInformation;
    private checkStakeholderApprovals;
    private determineValidationResult;
    private assessQualityDimensions;
    private performComplianceChecks;
    private calculateOverallQualityScore;
    private generateImprovementRecommendations;
    private updateMetrics;
    private checkTaskStatusChanges;
    private validateOngoingTasks;
    private containsTaskMarkers;
    private extractTasksFromFile;
    private notifyTaskCompletionListeners;
    private notifyQualityValidationListeners;
    private notifyAlertListeners;
    /**
     * Dispose of monitoring resources
     */
    dispose(): void;
}
//# sourceMappingURL=TaskMonitoringIntegration.d.ts.map