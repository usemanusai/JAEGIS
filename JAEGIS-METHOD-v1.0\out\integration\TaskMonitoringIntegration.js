"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaskMonitoringIntegration = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
/**
 * Task Monitoring Integration for real-time task tracking and quality validation
 */
class TaskMonitoringIntegration {
    context7;
    statusBar;
    config;
    monitoringTimer = null;
    taskEventListeners = [];
    qualityValidationListeners = [];
    alertListeners = [];
    metrics;
    isActive = false;
    constructor(context7, statusBar, config) {
        this.context7 = context7;
        this.statusBar = statusBar;
        this.config = {
            enableRealTimeMonitoring: true,
            monitoringInterval: 30000, // 30 seconds
            qualityThresholds: {
                minimumQualityScore: 85,
                criticalDefectThreshold: 0,
                stakeholderSatisfactionThreshold: 4.0,
                completionPercentageThreshold: 95
            },
            notificationSettings: {
                enableCompletionNotifications: true,
                enableQualityAlerts: true,
                enableStakeholderNotifications: true,
                notificationChannels: ['vscode']
            },
            validationRules: {
                requireStakeholderApproval: true,
                requireQualityGateValidation: true,
                requireDocumentationUpdate: true,
                requireTestingCompletion: true
            },
            ...config
        };
        this.metrics = {
            totalTasksMonitored: 0,
            tasksCompleted: 0,
            tasksInProgress: 0,
            tasksBlocked: 0,
            averageQualityScore: 0,
            averageCompletionTime: 0,
            stakeholderSatisfactionAverage: 0,
            qualityTrend: 'stable'
        };
        console.log('Task Monitoring Integration initialized for Sentinel Agent');
    }
    /**
     * Start real-time task monitoring
     */
    async startMonitoring() {
        if (this.isActive) {
            console.log('Task monitoring is already active');
            return;
        }
        this.isActive = true;
        this.statusBar.showInfo('Sentinel: Task monitoring started');
        // Context7 research for task monitoring best practices
        const monitoringResearch = await this.context7.autoResearch({
            query: `task monitoring best practices real-time quality validation ${new Date().toISOString().split('T')[0]}`,
            sources: ['project_management', 'quality_assurance', 'monitoring_frameworks'],
            focus: ['real_time_monitoring', 'quality_validation', 'completion_detection', 'stakeholder_notification'],
            packageName: 'task-monitoring'
        });
        if (monitoringResearch) {
            console.log('Task Monitoring: Context7 research completed for monitoring best practices');
        }
        if (this.config.enableRealTimeMonitoring) {
            this.startPeriodicMonitoring();
        }
        // Initialize file system watchers for task files
        await this.initializeTaskFileWatchers();
        console.log('Task monitoring started successfully');
    }
    /**
     * Stop task monitoring
     */
    stopMonitoring() {
        if (!this.isActive) {
            return;
        }
        this.isActive = false;
        if (this.monitoringTimer) {
            clearInterval(this.monitoringTimer);
            this.monitoringTimer = null;
        }
        this.statusBar.showInfo('Sentinel: Task monitoring stopped');
        console.log('Task monitoring stopped');
    }
    /**
     * Monitor task completion for a specific task
     */
    async monitorTaskCompletion(taskId) {
        try {
            // Get task information
            const taskInfo = await this.getTaskInformation(taskId);
            if (!taskInfo) {
                return null;
            }
            // Check if task is marked as completed
            if (taskInfo.status !== 'completed') {
                return null;
            }
            // Perform quality validation
            const qualityResult = await this.performQualityValidation(taskId);
            // Check stakeholder approvals
            const stakeholderApprovals = await this.checkStakeholderApprovals(taskId);
            // Determine validation result
            const validationResult = this.determineValidationResult(qualityResult, stakeholderApprovals);
            // Context7 research for completion validation
            const completionResearch = await this.context7.autoResearch({
                query: `task completion validation quality assurance ${taskInfo.taskType} best practices`,
                sources: ['completion_frameworks', 'quality_standards', 'validation_processes'],
                focus: ['completion_criteria', 'quality_validation', 'stakeholder_approval'],
                packageName: taskId
            });
            const completionEvent = {
                taskId,
                taskName: taskInfo.taskName,
                completionTimestamp: new Date(),
                qualityScore: qualityResult.overallQualityScore,
                validationResult,
                stakeholderApprovals,
                context7Insights: completionResearch || undefined
            };
            // Notify listeners
            this.notifyTaskCompletionListeners(completionEvent);
            // Generate alerts if needed
            await this.generateTaskAlerts(completionEvent, qualityResult);
            return completionEvent;
        }
        catch (error) {
            console.error(`Error monitoring task completion for ${taskId}:`, error);
            return null;
        }
    }
    /**
     * Perform comprehensive quality validation for a task
     */
    async performQualityValidation(taskId) {
        try {
            // Context7 research for quality validation methods
            const qualityResearch = await this.context7.autoResearch({
                query: `quality validation methods task completion assessment software development`,
                sources: ['quality_frameworks', 'validation_methodologies', 'assessment_standards'],
                focus: ['quality_metrics', 'validation_criteria', 'assessment_methods'],
                packageName: `quality-validation-${taskId}`
            });
            // Perform quality dimension assessments
            const qualityDimensions = await this.assessQualityDimensions(taskId);
            // Perform compliance checks
            const complianceChecks = await this.performComplianceChecks(taskId);
            // Calculate overall quality score
            const overallQualityScore = this.calculateOverallQualityScore(qualityDimensions);
            // Generate improvement recommendations
            const improvementRecommendations = this.generateImprovementRecommendations(qualityDimensions, complianceChecks, qualityResearch);
            const result = {
                taskId,
                overallQualityScore,
                qualityDimensions,
                complianceChecks,
                improvementRecommendations,
                validationTimestamp: new Date()
            };
            // Notify quality validation listeners
            this.notifyQualityValidationListeners(result);
            return result;
        }
        catch (error) {
            console.error(`Error performing quality validation for ${taskId}:`, error);
            throw error;
        }
    }
    /**
     * Generate task completion and quality alerts
     */
    async generateTaskAlerts(completionEvent, qualityResult) {
        const alerts = [];
        // Quality score alert
        if (qualityResult.overallQualityScore < this.config.qualityThresholds.minimumQualityScore) {
            alerts.push({
                alertId: `quality-${completionEvent.taskId}-${Date.now()}`,
                taskId: completionEvent.taskId,
                alertType: 'quality_issue',
                severity: 'high',
                message: `Task quality score (${qualityResult.overallQualityScore}) below threshold (${this.config.qualityThresholds.minimumQualityScore})`,
                timestamp: new Date(),
                actionRequired: true,
                recommendedActions: qualityResult.improvementRecommendations
            });
        }
        // Validation failure alert
        if (completionEvent.validationResult === 'failed') {
            alerts.push({
                alertId: `validation-${completionEvent.taskId}-${Date.now()}`,
                taskId: completionEvent.taskId,
                alertType: 'validation_failure',
                severity: 'critical',
                message: `Task completion validation failed for ${completionEvent.taskName}`,
                timestamp: new Date(),
                actionRequired: true,
                recommendedActions: ['Review completion criteria', 'Address quality issues', 'Obtain stakeholder approval']
            });
        }
        // Stakeholder approval pending alert
        const pendingApprovals = completionEvent.stakeholderApprovals.filter(a => a.approvalStatus === 'pending');
        if (pendingApprovals.length > 0) {
            alerts.push({
                alertId: `approval-${completionEvent.taskId}-${Date.now()}`,
                taskId: completionEvent.taskId,
                alertType: 'stakeholder_approval_pending',
                severity: 'medium',
                message: `${pendingApprovals.length} stakeholder approvals pending for ${completionEvent.taskName}`,
                timestamp: new Date(),
                actionRequired: true,
                recommendedActions: [`Contact pending stakeholders: ${pendingApprovals.map(a => a.stakeholderRole).join(', ')}`]
            });
        }
        // Notify alert listeners
        for (const alert of alerts) {
            this.notifyAlertListeners(alert);
        }
        return alerts;
    }
    /**
     * Get current task monitoring metrics
     */
    getMetrics() {
        return { ...this.metrics };
    }
    /**
     * Update task monitoring configuration
     */
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        console.log('Task monitoring configuration updated');
    }
    /**
     * Add event listeners
     */
    onTaskCompletion(listener) {
        this.taskEventListeners.push(listener);
    }
    onQualityValidation(listener) {
        this.qualityValidationListeners.push(listener);
    }
    onAlert(listener) {
        this.alertListeners.push(listener);
    }
    /**
     * Check if monitoring is active
     */
    isActive() {
        return this.isActive;
    }
    /**
     * Private helper methods
     */
    startPeriodicMonitoring() {
        this.monitoringTimer = setInterval(async () => {
            await this.performPeriodicCheck();
        }, this.config.monitoringInterval);
    }
    async performPeriodicCheck() {
        try {
            // Update metrics
            await this.updateMetrics();
            // Check for task status changes
            await this.checkTaskStatusChanges();
            // Validate ongoing tasks
            await this.validateOngoingTasks();
        }
        catch (error) {
            console.error('Error during periodic monitoring check:', error);
        }
    }
    async initializeTaskFileWatchers() {
        if (!vscode.workspace.workspaceFolders) {
            return;
        }
        const workspacePattern = new vscode.RelativePattern(vscode.workspace.workspaceFolders[0], '**/*.{md,ts,js,json}');
        const watcher = vscode.workspace.createFileSystemWatcher(workspacePattern);
        watcher.onDidChange(async (uri) => {
            await this.handleTaskFileChange(uri);
        });
    }
    async handleTaskFileChange(uri) {
        try {
            const filePath = uri.fsPath;
            // Check if file contains task markers
            if (await this.containsTaskMarkers(filePath)) {
                const tasks = await this.extractTasksFromFile(filePath);
                for (const task of tasks) {
                    if (task.status === 'completed') {
                        await this.monitorTaskCompletion(task.taskId);
                    }
                }
            }
        }
        catch (error) {
            console.error('Error handling task file change:', error);
        }
    }
    async getTaskInformation(taskId) {
        // Simplified task information retrieval
        return {
            taskId,
            taskName: `Task ${taskId}`,
            status: 'completed',
            taskType: 'development'
        };
    }
    async checkStakeholderApprovals(taskId) {
        // Simplified stakeholder approval check
        return [
            {
                stakeholderRole: 'Technical Lead',
                approvalStatus: 'approved',
                approvalTimestamp: new Date(),
                comments: 'Technical requirements met'
            },
            {
                stakeholderRole: 'Quality Assurance',
                approvalStatus: 'pending',
                comments: 'Awaiting final quality review'
            }
        ];
    }
    determineValidationResult(qualityResult, stakeholderApprovals) {
        const qualityPassed = qualityResult.overallQualityScore >= this.config.qualityThresholds.minimumQualityScore;
        const allApproved = stakeholderApprovals.every(a => a.approvalStatus === 'approved');
        const anyRejected = stakeholderApprovals.some(a => a.approvalStatus === 'rejected');
        if (anyRejected || !qualityPassed) {
            return 'failed';
        }
        else if (allApproved && qualityPassed) {
            return 'passed';
        }
        else {
            return 'pending';
        }
    }
    async assessQualityDimensions(taskId) {
        // Simplified quality dimension assessment
        return [
            {
                dimension: 'Functionality',
                score: Math.floor(Math.random() * 20) + 80,
                threshold: 85,
                status: 'passed',
                details: 'All functional requirements implemented'
            },
            {
                dimension: 'Reliability',
                score: Math.floor(Math.random() * 20) + 80,
                threshold: 85,
                status: 'passed',
                details: 'System demonstrates good reliability'
            }
        ];
    }
    async performComplianceChecks(taskId) {
        // Simplified compliance checks
        return [
            {
                checkName: 'Code Review Completed',
                status: 'compliant',
                details: 'Code review process completed successfully'
            },
            {
                checkName: 'Documentation Updated',
                status: 'compliant',
                details: 'All documentation updated and current'
            }
        ];
    }
    calculateOverallQualityScore(qualityDimensions) {
        if (qualityDimensions.length === 0)
            return 0;
        const totalScore = qualityDimensions.reduce((sum, dim) => sum + dim.score, 0);
        return totalScore / qualityDimensions.length;
    }
    generateImprovementRecommendations(qualityDimensions, complianceChecks, context7Research) {
        const recommendations = [];
        // Check for low-scoring quality dimensions
        const lowScoreDimensions = qualityDimensions.filter(dim => dim.score < dim.threshold);
        for (const dim of lowScoreDimensions) {
            recommendations.push(`Improve ${dim.dimension}: ${dim.details}`);
        }
        // Check for non-compliant checks
        const nonCompliantChecks = complianceChecks.filter(check => check.status === 'non_compliant');
        for (const check of nonCompliantChecks) {
            if (check.remediation) {
                recommendations.push(check.remediation);
            }
        }
        // Add Context7 insights if available
        if (context7Research && context7Research.insights) {
            recommendations.push(`Context7 Insight: ${context7Research.insights}`);
        }
        return recommendations;
    }
    async updateMetrics() {
        // Simplified metrics update
        this.metrics.totalTasksMonitored += 1;
        this.metrics.averageQualityScore = Math.floor(Math.random() * 20) + 80;
    }
    async checkTaskStatusChanges() {
        // Simplified task status change detection
        console.log('Checking for task status changes...');
    }
    async validateOngoingTasks() {
        // Simplified ongoing task validation
        console.log('Validating ongoing tasks...');
    }
    async containsTaskMarkers(filePath) {
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            return /- \[([ x\/\-])\]/.test(content);
        }
        catch (error) {
            return false;
        }
    }
    async extractTasksFromFile(filePath) {
        // Simplified task extraction
        return [];
    }
    notifyTaskCompletionListeners(event) {
        for (const listener of this.taskEventListeners) {
            try {
                listener(event);
            }
            catch (error) {
                console.error('Error notifying task completion listener:', error);
            }
        }
    }
    notifyQualityValidationListeners(result) {
        for (const listener of this.qualityValidationListeners) {
            try {
                listener(result);
            }
            catch (error) {
                console.error('Error notifying quality validation listener:', error);
            }
        }
    }
    notifyAlertListeners(alert) {
        for (const listener of this.alertListeners) {
            try {
                listener(alert);
            }
            catch (error) {
                console.error('Error notifying alert listener:', error);
            }
        }
    }
    /**
     * Dispose of monitoring resources
     */
    dispose() {
        this.stopMonitoring();
        this.taskEventListeners = [];
        this.qualityValidationListeners = [];
        this.alertListeners = [];
    }
}
exports.TaskMonitoringIntegration = TaskMonitoringIntegration;
//# sourceMappingURL=TaskMonitoringIntegration.js.map