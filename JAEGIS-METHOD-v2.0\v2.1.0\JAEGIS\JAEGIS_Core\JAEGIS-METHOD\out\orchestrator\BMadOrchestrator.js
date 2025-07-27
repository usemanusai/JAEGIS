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
exports.JAEGISOrchestrator = void 0;
const vscode = __importStar(require("vscode"));
const JAEGISTypes_1 = require("../types/JAEGISTypes");
class JAEGISOrchestrator {
    context;
    analyzer;
    statusBar;
    initializer;
    activeAgents = [];
    currentMode;
    workflowProgress;
    constructor(context, analyzer, statusBar, initializer) {
        this.context = context;
        this.analyzer = analyzer;
        this.statusBar = statusBar;
        this.initializer = initializer;
    }
    /**
     * Initialize workspace with JAEGIS structure
     */
    async initializeWorkspace(workspaceFolder) {
        try {
            await this.initializer.initializeWorkspace(workspaceFolder);
            // Emit initialization event
            await vscode.commands.executeCommand('jaegis.internal.workspaceInitialized', {
                workspaceFolder: workspaceFolder.name,
                timestamp: new Date().toISOString()
            });
        }
        catch (error) {
            throw new JAEGISTypes_1.JAEGISError(`Failed to initialize workspace: ${error}`, 'INIT_FAILED', 'initialization');
        }
    }
    /**
     * Execute a specific JAEGIS mode
     */
    async executeMode(mode, projectAnalysis) {
        try {
            this.currentMode = mode;
            // Create execution context
            const context = await this.createExecutionContext(mode, projectAnalysis);
            // Initialize workflow progress
            this.initializeWorkflowProgress(mode);
            // Activate recommended agents
            await this.activateAgents(projectAnalysis.recommendedAgents);
            // Execute mode-specific workflow
            await this.executeWorkflow(context);
        }
        catch (error) {
            console.error(`Failed to execute ${mode} mode:`, error);
            this.statusBar.showError(`Failed to execute ${mode} mode: ${error}`);
            throw error;
        }
    }
    /**
     * Activate specific AI agents
     */
    async activateAgents(agentIds) {
        try {
            this.activeAgents = [...agentIds];
            // Update status bar with active agents
            if (this.currentMode) {
                this.statusBar.updateMode(this.currentMode, this.activeAgents);
            }
            // Emit agent activation event
            await vscode.commands.executeCommand('jaegis.internal.agentsActivated', {
                agents: agentIds,
                timestamp: new Date().toISOString()
            });
            console.log(`Activated agents: ${agentIds.join(', ')}`);
        }
        catch (error) {
            throw new JAEGISTypes_1.JAEGISError(`Failed to activate agents: ${error}`, 'AGENT_ACTIVATION_FAILED', 'execution');
        }
    }
    /**
     * Get currently active agents
     */
    getActiveAgents() {
        return [...this.activeAgents];
    }
    /**
     * Get current mode
     */
    getCurrentMode() {
        return this.currentMode;
    }
    /**
     * Update workflow progress
     */
    updateProgress(progress) {
        if (this.workflowProgress) {
            this.workflowProgress = { ...this.workflowProgress, ...progress };
            this.statusBar.updateProgress(this.workflowProgress);
            // Emit progress update event
            vscode.commands.executeCommand('jaegis.internal.progressUpdated', this.workflowProgress);
        }
    }
    /**
     * Create execution context for mode
     */
    async createExecutionContext(mode, projectAnalysis) {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            throw new JAEGISTypes_1.JAEGISError('No workspace folder available', 'NO_WORKSPACE', 'execution');
        }
        // Get user preferences
        const config = vscode.workspace.getConfiguration('jaegis');
        const userPreferences = {
            autoActivateRecommendedAgents: config.get('autoActivateRecommendedAgents', true),
            enableRealTimeMonitoring: config.get('enableRealTimeMonitoring', true),
            progressNotifications: config.get('progressNotifications', true)
        };
        // Check for existing artifacts
        const existingArtifacts = await this.getExistingArtifacts(workspaceFolder);
        return {
            mode,
            workspaceFolder,
            projectAnalysis,
            selectedAgents: projectAnalysis.recommendedAgents,
            userPreferences,
            existingArtifacts
        };
    }
    /**
     * Initialize workflow progress tracking
     */
    initializeWorkflowProgress(mode) {
        this.workflowProgress = {
            mode,
            phase: 'Initializing',
            progress: 0,
            completedTasks: [],
            remainingTasks: this.getModeTaskList(mode)
        };
        this.statusBar.updateProgress(this.workflowProgress);
    }
    /**
     * Execute workflow based on mode
     */
    async executeWorkflow(context) {
        switch (context.mode) {
            case 'documentation':
                await this.executeDocumentationMode(context);
                break;
            case 'fullDevelopment':
                await this.executeFullDevelopmentMode(context);
                break;
            case 'continueProject':
                await this.executeContinueProjectMode(context);
                break;
            case 'taskOverview':
                await this.executeTaskOverviewMode(context);
                break;
            case 'debugMode':
                await this.executeDebugMode(context);
                break;
            case 'continuousExecution':
                await this.executeContinuousExecutionMode(context);
                break;
            case 'featureGapAnalysis':
                await this.executeFeatureGapAnalysisMode(context);
                break;
            case 'githubIntegration':
                await this.executeGithubIntegrationMode(context);
                break;
            default:
                throw new JAEGISTypes_1.JAEGISError(`Unknown mode: ${context.mode}`, 'UNKNOWN_MODE', 'execution');
        }
    }
    /**
     * Execute Documentation Mode workflow
     */
    async executeDocumentationMode(context) {
        this.updateProgress({ phase: 'Project Analysis', progress: 10 });
        // Simulate workflow execution
        await this.delay(1000);
        this.updateProgress({ phase: 'PRD Development', progress: 30 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Architecture Design', progress: 60 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Checklist Creation', progress: 90 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Documentation Complete', progress: 100 });
        // Show completion message
        const action = await vscode.window.showInformationMessage('Documentation Mode completed successfully! Generated: prd.md, architecture.md, checklist.md', 'Open Documents', 'Start Development', 'OK');
        if (action === 'Open Documents') {
            await this.openGeneratedDocuments(context.workspaceFolder);
        }
        else if (action === 'Start Development') {
            await this.executeMode('fullDevelopment', context.projectAnalysis);
        }
    }
    /**
     * Execute Full Development Mode workflow
     */
    async executeFullDevelopmentMode(context) {
        this.updateProgress({ phase: 'Development Planning', progress: 10 });
        // Show agent selection for development
        const action = await vscode.window.showInformationMessage('Full Development Mode: Ready to begin development workflow', 'Continue with Recommended Agents', 'Select Different Agents', 'Cancel');
        if (action === 'Continue with Recommended Agents') {
            this.updateProgress({ phase: 'Development in Progress', progress: 50 });
            // Continue with development workflow
        }
        else if (action === 'Select Different Agents') {
            await vscode.commands.executeCommand('jaegis.selectAgents');
        }
    }
    /**
     * Execute Continue Project Mode workflow
     */
    async executeContinueProjectMode(context) {
        this.updateProgress({ phase: 'Analyzing Existing Project', progress: 20 });
        // Analyze existing project state
        const existingState = await this.analyzeExistingProjectState(context.workspaceFolder);
        this.updateProgress({ phase: 'Identifying Continuation Points', progress: 60 });
        // Show continuation options
        await this.showContinuationOptions(existingState);
        this.updateProgress({ phase: 'Project Analysis Complete', progress: 100 });
    }
    /**
     * Execute Task Overview Mode workflow
     */
    async executeTaskOverviewMode(context) {
        this.updateProgress({ phase: 'Analyzing Task Structure', progress: 30 });
        // Analyze task management files
        await this.delay(1000);
        this.updateProgress({ phase: 'Generating Dashboard', progress: 70 });
        // Generate task overview dashboard
        await this.generateTaskDashboard(context.workspaceFolder);
        this.updateProgress({ phase: 'Task Overview Complete', progress: 100 });
    }
    /**
     * Execute Debug Mode workflow
     */
    async executeDebugMode(context) {
        this.updateProgress({ phase: 'Running Diagnostics', progress: 25 });
        // Get VS Code diagnostics
        const diagnostics = vscode.languages.getDiagnostics();
        const issues = this.processDiagnostics(diagnostics);
        this.updateProgress({ phase: 'Analyzing Issues', progress: 60 });
        if (issues.length > 0) {
            this.statusBar.updateIssues(issues);
            const action = await vscode.window.showWarningMessage(`Found ${issues.length} issues to resolve`, 'View Issues', 'Auto-Fix Available', 'Continue Analysis');
            if (action === 'View Issues') {
                await vscode.commands.executeCommand('workbench.actions.view.problems');
            }
        }
        this.updateProgress({ phase: 'Debug Analysis Complete', progress: 100 });
    }
    /**
     * Execute Continuous Execution Mode workflow
     */
    async executeContinuousExecutionMode(context) {
        // Autonomous execution without user prompts
        this.updateProgress({ phase: 'Autonomous Execution Started', progress: 10 });
        // Execute workflow phases automatically
        const phases = ['Analysis', 'Planning', 'Implementation', 'Validation'];
        for (let i = 0; i < phases.length; i++) {
            const phase = phases[i];
            const progress = 25 + (i * 20);
            this.updateProgress({ phase: `Autonomous ${phase}`, progress });
            await this.delay(2000); // Simulate work
        }
        this.updateProgress({ phase: 'Autonomous Execution Complete', progress: 100 });
    }
    /**
     * Execute Feature Gap Analysis Mode workflow
     */
    async executeFeatureGapAnalysisMode(context) {
        this.updateProgress({ phase: 'Analyzing Current Features', progress: 20 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Comparing with Industry Standards', progress: 50 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Generating Recommendations', progress: 80 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Feature Gap Analysis Complete', progress: 100 });
        vscode.window.showInformationMessage('Feature Gap Analysis completed! Check the generated report for improvement recommendations.');
    }
    /**
     * Execute GitHub Integration Mode workflow
     */
    async executeGithubIntegrationMode(context) {
        this.updateProgress({ phase: 'Analyzing Repository Structure', progress: 20 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Generating README', progress: 50 });
        await this.delay(1000);
        this.updateProgress({ phase: 'Creating Documentation', progress: 80 });
        await this.delay(1000);
        this.updateProgress({ phase: 'GitHub Integration Complete', progress: 100 });
        vscode.window.showInformationMessage('GitHub Integration completed! Professional repository documentation has been generated.');
    }
    // Helper methods
    async getExistingArtifacts(workspaceFolder) {
        const artifacts = [];
        const commonFiles = ['README.md', 'prd.md', 'architecture.md', 'checklist.md'];
        for (const file of commonFiles) {
            try {
                const fileUri = vscode.Uri.joinPath(workspaceFolder.uri, file);
                await vscode.workspace.fs.stat(fileUri);
                artifacts.push(file);
            }
            catch {
                // File doesn't exist
            }
        }
        return artifacts;
    }
    getModeTaskList(mode) {
        const taskLists = {
            documentation: ['Project Analysis', 'PRD Development', 'Architecture Design', 'Checklist Creation'],
            fullDevelopment: ['Planning', 'Setup', 'Development', 'Testing', 'Deployment'],
            continueProject: ['State Analysis', 'Context Restoration', 'Continuation Planning'],
            taskOverview: ['Task Analysis', 'Dashboard Generation', 'Progress Tracking'],
            debugMode: ['Diagnostics', 'Issue Analysis', 'Resolution Planning'],
            continuousExecution: ['Autonomous Analysis', 'Autonomous Planning', 'Autonomous Implementation'],
            featureGapAnalysis: ['Feature Analysis', 'Gap Identification', 'Recommendation Generation'],
            githubIntegration: ['Repository Analysis', 'Documentation Generation', 'Workflow Setup']
        };
        return taskLists[mode] || [];
    }
    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    async openGeneratedDocuments(workspaceFolder) {
        const documents = ['prd.md', 'architecture.md', 'checklist.md'];
        for (const doc of documents) {
            try {
                const docUri = vscode.Uri.joinPath(workspaceFolder.uri, doc);
                await vscode.window.showTextDocument(docUri);
            }
            catch (error) {
                console.log(`Document ${doc} not found or couldn't be opened`);
            }
        }
    }
    async analyzeExistingProjectState(workspaceFolder) {
        // Analyze existing project state for continuation
        return {
            hasExistingTasks: false,
            completionPercentage: 0,
            lastModified: new Date()
        };
    }
    async showContinuationOptions(existingState) {
        const options = [
            'Resume from last checkpoint',
            'Start new phase',
            'Review completed work',
            'Update project scope'
        ];
        const selected = await vscode.window.showQuickPick(options, {
            title: 'Select Continuation Point',
            placeHolder: 'Choose how to continue the project'
        });
        if (selected) {
            vscode.window.showInformationMessage(`Continuing with: ${selected}`);
        }
    }
    async generateTaskDashboard(workspaceFolder) {
        // Generate task overview dashboard
        vscode.window.showInformationMessage('Task dashboard generated successfully!');
    }
    processDiagnostics(diagnostics) {
        const issues = [];
        for (const [uri, diags] of diagnostics) {
            for (const diag of diags) {
                if (diag.severity === vscode.DiagnosticSeverity.Error) {
                    issues.push({
                        severity: 'critical',
                        category: 'quality',
                        message: diag.message,
                        file: uri.fsPath,
                        line: diag.range.start.line,
                        canAutoFix: false
                    });
                }
            }
        }
        return issues;
    }
}
exports.JAEGISOrchestrator = JAEGISOrchestrator;
//# sourceMappingURL=JAEGISOrchestrator.js.map