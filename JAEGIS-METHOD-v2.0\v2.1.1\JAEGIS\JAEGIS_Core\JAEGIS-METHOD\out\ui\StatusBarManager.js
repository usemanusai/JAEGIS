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
exports.StatusBarManager = void 0;
const vscode = __importStar(require("vscode"));
class StatusBarManager {
    statusBarItem;
    progressItem;
    issueItem;
    currentInfo;
    constructor() {
        // Create status bar items
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.progressItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 99);
        this.issueItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 98);
        // Initialize current info
        this.currentInfo = {
            activeAgents: [],
            lastUpdate: new Date()
        };
    }
    /**
     * Initialize status bar with default state
     */
    initialize() {
        this.statusBarItem.text = '$(robot) JAEGIS: Ready';
        this.statusBarItem.tooltip = 'JAEGIS AI Agent Orchestrator - Click to select mode';
        this.statusBarItem.command = 'jaegis.quickModeSelect';
        this.statusBarItem.show();
        console.log('JAEGIS Status Bar initialized');
    }
    /**
     * Update status bar with current mode and agents
     */
    updateMode(mode, agents = []) {
        this.currentInfo.mode = mode;
        this.currentInfo.activeAgents = agents;
        this.currentInfo.lastUpdate = new Date();
        const modeDisplayName = this.getModeDisplayName(mode);
        const agentNames = agents.map(id => this.getAgentDisplayName(id)).join(', ');
        this.statusBarItem.text = `$(robot) JAEGIS: ${modeDisplayName}`;
        this.statusBarItem.tooltip = this.buildModeTooltip(mode, agents);
        this.statusBarItem.command = 'jaegis.showModeDetails';
        this.statusBarItem.backgroundColor = undefined; // Clear any error background
        this.statusBarItem.show();
        // Show notification if enabled
        const config = vscode.workspace.getConfiguration('jaegis');
        if (config.get('progressNotifications', true)) {
            vscode.window.showInformationMessage(`JAEGIS ${modeDisplayName} mode activated${agents.length > 0 ? ` with agents: ${agentNames}` : ''}`);
        }
    }
    /**
     * Update progress information
     */
    updateProgress(progress) {
        this.currentInfo.progress = progress;
        this.currentInfo.lastUpdate = new Date();
        if (progress.progress > 0 && progress.progress < 100) {
            this.progressItem.text = `$(sync~spin) ${progress.phase} (${progress.progress}%)`;
            this.progressItem.tooltip = this.buildProgressTooltip(progress);
            this.progressItem.command = 'jaegis.showProgress';
            this.progressItem.show();
        }
        else if (progress.progress >= 100) {
            this.progressItem.text = `$(check) ${progress.phase} Complete`;
            this.progressItem.tooltip = 'Workflow completed successfully';
            this.progressItem.command = 'jaegis.showProgress';
            // Hide progress item after 5 seconds
            setTimeout(() => {
                this.progressItem.hide();
            }, 5000);
        }
        else {
            this.progressItem.hide();
        }
    }
    /**
     * Update issue information
     */
    updateIssues(issues) {
        this.currentInfo.issues = issues;
        this.currentInfo.lastUpdate = new Date();
        if (issues.length === 0) {
            this.issueItem.hide();
            return;
        }
        const criticalIssues = issues.filter(issue => issue.severity === 'critical');
        const highIssues = issues.filter(issue => issue.severity === 'high');
        if (criticalIssues.length > 0) {
            this.issueItem.text = `$(error) ${criticalIssues.length} Critical`;
            this.issueItem.tooltip = this.buildIssueTooltip(issues);
            this.issueItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
        }
        else if (highIssues.length > 0) {
            this.issueItem.text = `$(warning) ${highIssues.length} High`;
            this.issueItem.tooltip = this.buildIssueTooltip(issues);
            this.issueItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        }
        else {
            this.issueItem.text = `$(info) ${issues.length} Issues`;
            this.issueItem.tooltip = this.buildIssueTooltip(issues);
            this.issueItem.backgroundColor = undefined;
        }
        this.issueItem.command = 'jaegis.debugMode';
        this.issueItem.show();
    }
    /**
     * Show error state
     */
    showError(message, command) {
        this.statusBarItem.text = '$(error) JAEGIS: Error';
        this.statusBarItem.tooltip = `Error: ${message}\nClick for details`;
        this.statusBarItem.command = command || 'jaegis.showErrorDetails';
        this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
        this.statusBarItem.show();
        // Show error notification
        vscode.window.showErrorMessage(`JAEGIS Error: ${message}`, 'Show Details').then(action => {
            if (action === 'Show Details' && command) {
                vscode.commands.executeCommand(command);
            }
        });
    }
    /**
     * Show loading state
     */
    showLoading(message) {
        this.statusBarItem.text = `$(sync~spin) JAEGIS: ${message}`;
        this.statusBarItem.tooltip = `JAEGIS is ${message.toLowerCase()}...`;
        this.statusBarItem.command = undefined;
        this.statusBarItem.backgroundColor = undefined;
        this.statusBarItem.show();
    }
    /**
     * Show success state
     */
    showSuccess(message, command) {
        this.statusBarItem.text = '$(check) JAEGIS: Success';
        this.statusBarItem.tooltip = `Success: ${message}\nClick for details`;
        this.statusBarItem.command = command || 'jaegis.quickModeSelect';
        this.statusBarItem.backgroundColor = undefined;
        this.statusBarItem.show();
        // Show success notification
        vscode.window.showInformationMessage(`JAEGIS: ${message}`);
        // Auto-clear success state after 5 seconds
        setTimeout(() => {
            this.statusBarItem.text = '$(robot) JAEGIS: Ready';
            this.statusBarItem.tooltip = 'JAEGIS AI Agent Orchestrator - Click to select mode';
            this.statusBarItem.command = 'jaegis.quickModeSelect';
        }, 5000);
    }
    /**
     * Show info state
     */
    showInfo(message, command) {
        this.statusBarItem.text = '$(info) JAEGIS: Info';
        this.statusBarItem.tooltip = `Info: ${message}\nClick for details`;
        this.statusBarItem.command = command || 'jaegis.quickModeSelect';
        this.statusBarItem.backgroundColor = undefined;
        this.statusBarItem.show();
        // Show info notification
        vscode.window.showInformationMessage(`JAEGIS: ${message}`);
        // Auto-clear info state after 3 seconds
        setTimeout(() => {
            this.statusBarItem.text = '$(robot) JAEGIS: Ready';
            this.statusBarItem.tooltip = 'JAEGIS AI Agent Orchestrator - Click to select mode';
            this.statusBarItem.command = 'jaegis.quickModeSelect';
        }, 3000);
    }
    /**
     * Clear all status items
     */
    clear() {
        this.statusBarItem.hide();
        this.progressItem.hide();
        this.issueItem.hide();
    }
    /**
     * Get current status information
     */
    getCurrentInfo() {
        return { ...this.currentInfo };
    }
    /**
     * Dispose of status bar items
     */
    dispose() {
        this.statusBarItem.dispose();
        this.progressItem.dispose();
        this.issueItem.dispose();
    }
    // Helper methods
    getModeDisplayName(mode) {
        const modeNames = {
            documentation: 'Documentation',
            fullDevelopment: 'Full Development',
            continueProject: 'Continue Project',
            taskOverview: 'Task Overview',
            debugMode: 'Debug & Troubleshoot',
            continuousExecution: 'Continuous Execution',
            featureGapAnalysis: 'Feature Gap Analysis',
            githubIntegration: 'GitHub Integration'
        };
        return modeNames[mode] || mode;
    }
    getAgentDisplayName(agentId) {
        const agentNames = {
            john: 'John (PM)',
            fred: 'Fred (Architect)',
            jane: 'Jane (Design)',
            sage: 'Sage (Security)',
            alex: 'Alex (Platform)',
            tyler: 'Tyler (Tasks)',
            taylor: 'Taylor (Writer)',
            sarah: 'Sarah (PO)',
            bob: 'Bob (SM)',
            dakota: 'Dakota (Dependencies)',
            phoenix: 'Phoenix (Deployment)',
            chronos: 'Chronos (Versioning)'
        };
        return agentNames[agentId] || agentId;
    }
    buildModeTooltip(mode, agents) {
        const modeDescription = this.getModeDescription(mode);
        const agentList = agents.length > 0
            ? `\n\nActive Agents:\n${agents.map(id => `• ${this.getAgentDisplayName(id)}`).join('\n')}`
            : '';
        return `JAEGIS AI Agent Orchestrator\n\nMode: ${this.getModeDisplayName(mode)}\n${modeDescription}${agentList}\n\nClick to view mode details`;
    }
    buildProgressTooltip(progress) {
        const timeRemaining = progress.estimatedTimeRemaining
            ? `\nEstimated time remaining: ${Math.round(progress.estimatedTimeRemaining / 60)} minutes`
            : '';
        const currentAgent = progress.currentAgent
            ? `\nCurrent agent: ${this.getAgentDisplayName(progress.currentAgent)}`
            : '';
        const completedTasks = progress.completedTasks.length > 0
            ? `\n\nCompleted tasks:\n${progress.completedTasks.map(task => `• ${task}`).join('\n')}`
            : '';
        return `JAEGIS Workflow Progress\n\nPhase: ${progress.phase}\nProgress: ${progress.progress}%${timeRemaining}${currentAgent}${completedTasks}\n\nClick for detailed progress view`;
    }
    buildIssueTooltip(issues) {
        const issueSummary = issues.reduce((acc, issue) => {
            acc[issue.severity] = (acc[issue.severity] || 0) + 1;
            return acc;
        }, {});
        const summaryText = Object.entries(issueSummary)
            .map(([severity, count]) => `${count} ${severity}`)
            .join(', ');
        const recentIssues = issues.slice(0, 3).map(issue => `• ${issue.severity.toUpperCase()}: ${issue.message}`).join('\n');
        return `Project Issues Detected\n\nSummary: ${summaryText}\n\nRecent issues:\n${recentIssues}\n\nClick to activate Debug & Troubleshoot mode`;
    }
    getModeDescription(mode) {
        const descriptions = {
            documentation: 'Generate comprehensive project documentation',
            fullDevelopment: 'Complete application development workflow',
            continueProject: 'Resume interrupted project work',
            taskOverview: 'Project status dashboard and task management',
            debugMode: 'Systematic issue diagnosis and resolution',
            continuousExecution: 'Autonomous workflow execution',
            featureGapAnalysis: 'Analyze missing features and improvements',
            githubIntegration: 'GitHub repository documentation and workflow'
        };
        return descriptions[mode] || 'JAEGIS workflow mode';
    }
}
exports.StatusBarManager = StatusBarManager;
//# sourceMappingURL=StatusBarManager.js.map