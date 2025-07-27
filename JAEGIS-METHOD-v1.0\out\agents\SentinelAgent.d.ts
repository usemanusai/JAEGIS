import { Context7ResearchResult } from '../integration/Context7Integration';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Sentinel - Task Completion & Quality Assurance Specialist Agent
 * Handles comprehensive task completion monitoring, quality validation, and stakeholder confirmation
 * with seamless Context7 integration for quality standards research and completion criteria validation
 */
export interface TaskInfo {
    taskId: string;
    taskName: string;
    status: 'not_started' | 'in_progress' | 'completed' | 'cancelled';
    assignedAgent: string;
    completionCriteria: string[];
    qualityRequirements: string[];
    stakeholders: string[];
    lastModified: Date;
}
export interface QualityAssessment {
    taskId: string;
    overallScore: number;
    functionalityScore: number;
    reliabilityScore: number;
    performanceScore: number;
    usabilityScore: number;
    securityScore: number;
    stakeholderSatisfaction: number;
    complianceLevel: number;
    improvementAreas: string[];
}
export interface CompletionValidation {
    taskId: string;
    validationResult: 'passed' | 'failed' | 'pending';
    completionPercentage: number;
    criteriaValidation: CriteriaValidation[];
    qualityGateResults: QualityGateResult[];
    stakeholderApprovals: StakeholderApproval[];
    validationTimestamp: Date;
}
export interface CriteriaValidation {
    criterion: string;
    status: 'met' | 'not_met' | 'partial';
    validationMethod: string;
    evidence: string;
    qualityScore: number;
}
export interface QualityGateResult {
    gateName: string;
    threshold: number;
    actualValue: number;
    status: 'passed' | 'failed';
    impact: 'critical' | 'high' | 'medium' | 'low';
}
export interface StakeholderApproval {
    stakeholderRole: string;
    stakeholderName: string;
    approvalStatus: 'approved' | 'rejected' | 'pending';
    approvalDate?: Date;
    comments: string;
}
export interface TaskCompletionResult {
    projectPath: string;
    timestamp: Date;
    totalTasksMonitored: number;
    tasksCompleted: number;
    qualityAssessments: QualityAssessment[];
    completionValidations: CompletionValidation[];
    context7Insights: Context7ResearchResult[];
    recommendations: CompletionRecommendation[];
}
export interface ChecklistValidationResult {
    projectPath: string;
    timestamp: Date;
    totalChecklists: number;
    checklistsValidated: number;
    completionPercentage: number;
    qualityScore: number;
    context7Research: Context7ResearchResult[];
    validationIssues: ValidationIssue[];
}
export interface QualityAssuranceResult {
    projectPath: string;
    timestamp: Date;
    overallQualityScore: number;
    qualityDimensions: QualityDimensionScore[];
    complianceResults: ComplianceResult[];
    stakeholderFeedback: StakeholderFeedback[];
    context7Research: Context7ResearchResult[];
    improvementPlan: ImprovementPlan;
}
export interface CompletionRecommendation {
    type: 'completion' | 'quality' | 'stakeholder' | 'process';
    priority: 'critical' | 'high' | 'medium' | 'low';
    title: string;
    description: string;
    actionRequired: boolean;
    context7Research?: Context7ResearchResult;
}
export interface ValidationIssue {
    checklistName: string;
    itemName: string;
    issueType: 'incomplete' | 'invalid' | 'missing_evidence';
    severity: 'critical' | 'high' | 'medium' | 'low';
    description: string;
    recommendedAction: string;
}
export interface QualityDimensionScore {
    dimension: string;
    score: number;
    benchmark: number;
    status: 'excellent' | 'good' | 'acceptable' | 'needs_improvement';
    details: string;
}
export interface ComplianceResult {
    standard: string;
    complianceLevel: number;
    status: 'compliant' | 'non_compliant' | 'partial';
    gaps: string[];
    recommendations: string[];
}
export interface StakeholderFeedback {
    stakeholderRole: string;
    satisfactionScore: number;
    feedback: string;
    improvementSuggestions: string[];
}
export interface ImprovementPlan {
    immediateActions: ImprovementAction[];
    shortTermActions: ImprovementAction[];
    longTermActions: ImprovementAction[];
    resourceRequirements: string[];
    timeline: string;
}
export interface ImprovementAction {
    action: string;
    priority: 'critical' | 'high' | 'medium' | 'low';
    effort: 'low' | 'medium' | 'high';
    impact: 'low' | 'medium' | 'high';
    owner: string;
    dueDate: string;
    expectedOutcome: string;
}
/**
 * Sentinel Agent - Task Completion & Quality Assurance Specialist
 */
export declare class SentinelAgent {
    private context7;
    private analyzer;
    private statusBar;
    private taskMonitoring;
    private fileWatcher;
    private taskCache;
    private qualityCache;
    constructor(analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager, context7Config?: any);
    /**
     * Perform comprehensive task completion monitoring
     */
    performTaskCompletionMonitoring(projectPath?: string): Promise<TaskCompletionResult>;
    /**
     * Perform intelligent checklist validation
     */
    performChecklistValidation(): Promise<ChecklistValidationResult>;
    /**
     * Perform comprehensive quality assurance review
     */
    performQualityAssuranceReview(): Promise<QualityAssuranceResult>;
    /**
     * Initialize task monitoring file watcher
     */
    private initializeTaskWatcher;
    /**
     * Handle task file changes for real-time monitoring
     */
    private handleTaskFileChange;
    /**
     * Handle task file creation
     */
    private handleTaskFileCreate;
    /**
     * Handle task file deletion
     */
    private handleTaskFileDelete;
    /**
     * Discover all BMAD tasks across the ecosystem
     */
    private discoverBMADTasks;
    /**
     * Extract tasks from a file
     */
    private extractTasksFromFile;
    /**
     * Helper methods for task analysis
     */
    private containsTaskMarkers;
    private determineAssignedAgent;
    private performQualityAssessment;
    private validateTaskCompletion;
    private generateCompletionRecommendations;
    private discoverBMADChecklists;
    private validateChecklist;
    private assessQualityDimensions;
    private assessCompliance;
    private collectStakeholderFeedback;
    private generateImprovementPlan;
    private notifyTaskCompletion;
    private notifyValidationFailure;
    private generateCompletionReport;
    private generateQualityAssessmentReport;
    /**
     * Get Sentinel agent status
     */
    getStatus(): {
        context7Available: boolean;
        taskMonitoringActive: boolean;
        fileWatcherActive: boolean;
        tasksCached: number;
        lastUpdate?: Date;
    };
    /**
     * Dispose of agent resources
     */
    dispose(): void;
}
//# sourceMappingURL=SentinelAgent.d.ts.map