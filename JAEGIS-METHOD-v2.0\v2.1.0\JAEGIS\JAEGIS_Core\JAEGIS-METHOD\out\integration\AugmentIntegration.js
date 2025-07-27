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
exports.AugmentIntegration = void 0;
const vscode = __importStar(require("vscode"));
/**
 * Integration interface for Augment AI Code extension
 * Provides JAEGIS functionality as menu options within Augment's interface
 */
class AugmentIntegration {
    orchestrator;
    analyzer;
    statusBar;
    augmentExtension;
    isIntegrated = false;
    constructor(orchestrator, analyzer, statusBar) {
        this.orchestrator = orchestrator;
        this.analyzer = analyzer;
        this.statusBar = statusBar;
    }
    /**
     * Initialize integration with Augment AI Code extension
     */
    async initialize() {
        try {
            // Check if Augment AI Code extension is available
            this.augmentExtension = vscode.extensions.getExtension('augment.ai-code') ||
                vscode.extensions.getExtension('augment.code') ||
                vscode.extensions.getExtension('augment-ai.code');
            if (!this.augmentExtension) {
                console.log('Augment AI Code extension not found. JAEGIS will use standard VS Code integration.');
                await this.setupFallbackIntegration();
                return;
            }
            // Attempt to integrate with Augment
            await this.integrateWithAugment();
        }
        catch (error) {
            console.error('Failed to initialize Augment integration:', error);
            await this.setupFallbackIntegration();
        }
    }
    /**
     * Integrate JAEGIS workflows with Augment extension
     */
    async integrateWithAugment() {
        if (!this.augmentExtension) {
            throw new Error('Augment extension not available');
        }
        try {
            // Activate Augment extension to get its API
            const augmentAPI = await this.augmentExtension.activate();
            // Check if Augment supports workflow provider registration
            if (augmentAPI && typeof augmentAPI.registerWorkflowProvider === 'function') {
                await this.registerJaegisWorkflowProvider(augmentAPI);
                this.isIntegrated = true;
                console.log('Successfully integrated JAEGIS with Augment AI Code extension');
            }
            else {
                console.log('Augment extension does not support workflow provider API. Using fallback integration.');
                await this.setupFallbackIntegration();
            }
        }
        catch (error) {
            console.error('Failed to integrate with Augment:', error);
            await this.setupFallbackIntegration();
        }
    }
    /**
     * Register JAEGIS as a workflow provider with Augment
     */
    async registerJaegisWorkflowProvider(augmentAPI) {
        const workflowProvider = {
            id: 'jaegis-orchestrator',
            name: '🟣 JAEGIS AI Agent Orchestrator',
            description: 'Collaborative AI agent workflows for comprehensive development',
            icon: '$(robot)',
            color: '#8B5CF6', // Purple color
            workflows: [
                {
                    id: 'documentation-mode',
                    name: '📚 Documentation Mode',
                    description: 'Generate comprehensive project documentation (PRD, Architecture, Checklist)',
                    icon: '$(book)',
                    category: 'Planning',
                    color: '#8B5CF6',
                    handler: this.handleDocumentationMode.bind(this)
                },
                {
                    id: 'full-development-mode',
                    name: '🚀 Full Development Mode',
                    description: 'Complete application development with AI agents',
                    icon: '$(rocket)',
                    category: 'Development',
                    color: '#8B5CF6',
                    handler: this.handleFullDevelopmentMode.bind(this)
                },
                {
                    id: 'debug-mode',
                    name: 'Debug & Troubleshoot',
                    description: 'Systematic issue diagnosis and resolution',
                    icon: '$(debug)',
                    category: 'Debugging',
                    handler: this.handleDebugMode.bind(this)
                },
                {
                    id: 'continue-project',
                    name: 'Continue Project',
                    description: 'Resume work on existing project with context awareness',
                    icon: '$(debug-continue)',
                    category: 'Development',
                    handler: this.handleContinueProject.bind(this)
                },
                {
                    id: 'task-overview',
                    name: 'Task Overview',
                    description: 'View and manage project tasks and progress',
                    icon: '$(list-tree)',
                    category: 'Management',
                    handler: this.handleTaskOverview.bind(this)
                },
                {
                    id: 'continuous-execution',
                    name: 'Continuous Execution',
                    description: 'Autonomous workflow execution without user prompts',
                    icon: '$(sync)',
                    category: 'Automation',
                    handler: this.handleContinuousExecution.bind(this)
                },
                {
                    id: 'feature-gap-analysis',
                    name: 'Feature Gap Analysis',
                    description: 'Analyze missing features and implementation gaps',
                    icon: '$(search)',
                    category: 'Analysis',
                    handler: this.handleFeatureGapAnalysis.bind(this)
                },
                {
                    id: 'github-integration',
                    name: 'GitHub Integration',
                    description: 'Automated GitHub workflow and issue management',
                    icon: '$(github)',
                    category: 'Integration',
                    handler: this.handleGithubIntegration.bind(this)
                },
                {
                    id: 'dependency-audit',
                    name: '🔍 Dakota: Dependency Audit',
                    description: 'Comprehensive dependency analysis with Context7 research',
                    icon: '$(search)',
                    category: 'Maintenance',
                    handler: this.handleDependencyAudit.bind(this)
                },
                {
                    id: 'dependency-modernization',
                    name: '⬆️ Dakota: Dependency Modernization',
                    description: 'Automated dependency updates and modernization',
                    icon: '$(arrow-up)',
                    category: 'Maintenance',
                    handler: this.handleDependencyModernization.bind(this)
                },
                {
                    id: 'security-scan',
                    name: '🛡️ Dakota: Security Scan',
                    description: 'Real-time security vulnerability detection and remediation',
                    icon: '$(shield)',
                    category: 'Security',
                    handler: this.handleSecurityScan.bind(this)
                },
                {
                    id: 'deployment-preparation',
                    name: '🚀 Phoenix: Deployment Preparation',
                    description: 'Comprehensive deployment analysis and preparation',
                    icon: '$(rocket)',
                    category: 'Deployment',
                    handler: this.handleDeploymentPreparation.bind(this)
                },
                {
                    id: 'containerization',
                    name: '🐳 Phoenix: Containerization',
                    description: 'Automated Docker and Kubernetes configuration',
                    icon: '$(package)',
                    category: 'Infrastructure',
                    handler: this.handleContainerization.bind(this)
                },
                {
                    id: 'cross-platform-deployment',
                    name: '🌐 Phoenix: Cross-Platform Deployment',
                    description: 'Multi-platform deployment script generation',
                    icon: '$(globe)',
                    category: 'DevOps',
                    handler: this.handleCrossPlatformDeployment.bind(this)
                },
                {
                    id: 'version-tracking',
                    name: '⏰ Chronos: Version Tracking',
                    description: 'Comprehensive version control and temporal tracking',
                    icon: '$(versions)',
                    category: 'Version Control',
                    handler: this.handleVersionTracking.bind(this)
                },
                {
                    id: 'token-monitoring',
                    name: '📊 Chronos: Token Monitoring',
                    description: 'Real-time token usage optimization and monitoring',
                    icon: '$(dashboard)',
                    category: 'Token Management',
                    handler: this.handleTokenMonitoring.bind(this)
                },
                {
                    id: 'model-research',
                    name: '🔬 Chronos: Model Research',
                    description: 'AI model specifications and updates research',
                    icon: '$(search)',
                    category: 'Model Research',
                    handler: this.handleModelResearch.bind(this)
                }
            ]
        };
        await augmentAPI.registerWorkflowProvider(workflowProvider);
    }
    /**
     * Setup fallback integration using standard VS Code APIs
     */
    async setupFallbackIntegration() {
        // Register JAEGIS menu items in VS Code's standard locations
        await this.registerVSCodeMenus();
        console.log('JAEGIS fallback integration initialized');
    }
    /**
     * Register JAEGIS commands in VS Code menus
     */
    async registerVSCodeMenus() {
        // Commands are already registered by CommandManager
        // This method can be extended to add additional menu contributions
        // Show notification about JAEGIS availability
        const action = await vscode.window.showInformationMessage('JAEGIS AI Agent Orchestrator is ready! Access workflows via Command Palette (Ctrl+Shift+P) or status bar.', 'Show Commands', 'Quick Start');
        if (action === 'Show Commands') {
            await vscode.commands.executeCommand('workbench.action.showCommands');
        }
        else if (action === 'Quick Start') {
            await vscode.commands.executeCommand('jaegis.quickModeSelect');
        }
    }
    // Workflow Handlers - Bridge Augment UI to JAEGIS Orchestrator
    /**
     * Handle Documentation Mode workflow
     */
    async handleDocumentationMode(context) {
        try {
            this.statusBar.showLoading('Initializing Documentation Mode');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('documentation', analysisResult.projectAnalysis);
            this.statusBar.updateMode('documentation', analysisResult.projectAnalysis.recommendedAgents);
            // Notify Augment of completion if context provided
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'Documentation Mode completed successfully',
                    outputs: ['prd.md', 'architecture.md', 'checklist.md']
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`Documentation Mode failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Handle Full Development Mode workflow
     */
    async handleFullDevelopmentMode(context) {
        try {
            this.statusBar.showLoading('Initializing Full Development Mode');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('fullDevelopment', analysisResult.projectAnalysis);
            this.statusBar.updateMode('fullDevelopment', analysisResult.projectAnalysis.recommendedAgents);
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'Full Development Mode initiated successfully'
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`Full Development Mode failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Handle Debug Mode workflow
     */
    async handleDebugMode(context) {
        try {
            this.statusBar.showLoading('Initializing Debug Mode');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('debugMode', analysisResult.projectAnalysis);
            this.statusBar.updateMode('debugMode', analysisResult.projectAnalysis.recommendedAgents);
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'Debug Mode completed successfully'
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`Debug Mode failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Handle Continue Project workflow
     */
    async handleContinueProject(context) {
        try {
            this.statusBar.showLoading('Continuing Project');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('continueProject', analysisResult.projectAnalysis);
            this.statusBar.updateMode('continueProject', analysisResult.projectAnalysis.recommendedAgents);
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'Project continuation initiated successfully'
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`Continue Project failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Handle Task Overview workflow
     */
    async handleTaskOverview(context) {
        try {
            this.statusBar.showLoading('Loading Task Overview');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('taskOverview', analysisResult.projectAnalysis);
            this.statusBar.updateMode('taskOverview', analysisResult.projectAnalysis.recommendedAgents);
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'Task Overview loaded successfully'
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`Task Overview failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Handle Continuous Execution workflow
     */
    async handleContinuousExecution(context) {
        try {
            this.statusBar.showLoading('Starting Continuous Execution');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('continuousExecution', analysisResult.projectAnalysis);
            this.statusBar.updateMode('continuousExecution', analysisResult.projectAnalysis.recommendedAgents);
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'Continuous Execution started successfully'
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`Continuous Execution failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Handle Feature Gap Analysis workflow
     */
    async handleFeatureGapAnalysis(context) {
        try {
            this.statusBar.showLoading('Analyzing Feature Gaps');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('featureGapAnalysis', analysisResult.projectAnalysis);
            this.statusBar.updateMode('featureGapAnalysis', analysisResult.projectAnalysis.recommendedAgents);
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'Feature Gap Analysis completed successfully'
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`Feature Gap Analysis failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Handle GitHub Integration workflow
     */
    async handleGithubIntegration(context) {
        try {
            this.statusBar.showLoading('Initializing GitHub Integration');
            const analysisResult = await this.analyzer.analyzeWorkspace();
            await this.orchestrator.executeMode('githubIntegration', analysisResult.projectAnalysis);
            this.statusBar.updateMode('githubIntegration', analysisResult.projectAnalysis.recommendedAgents);
            if (context && typeof context.onComplete === 'function') {
                context.onComplete({
                    success: true,
                    message: 'GitHub Integration completed successfully'
                });
            }
        }
        catch (error) {
            this.statusBar.showError(`GitHub Integration failed: ${error}`);
            if (context && typeof context.onError === 'function') {
                context.onError(error);
            }
        }
    }
    /**
     * Check if integration with Augment is active
     */
    isAugmentIntegrated() {
        return this.isIntegrated;
    }
    /**
     * Get Augment extension information
     */
    getAugmentInfo() {
        if (!this.augmentExtension) {
            return { available: false };
        }
        return {
            available: true,
            version: this.augmentExtension.packageJSON?.version,
            id: this.augmentExtension.id
        };
    }
    /**
     * Handle dependency audit workflow
     */
    async handleDependencyAudit(context) {
        try {
            this.statusBar.showLoading('Initializing Dakota Dependency Audit');
            // Execute dependency audit command
            await vscode.commands.executeCommand('jaegis.dependencyAudit');
            this.statusBar.showSuccess('Dakota: Dependency audit completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform dependency audit: ${error}`);
            throw error;
        }
    }
    /**
     * Handle dependency modernization workflow
     */
    async handleDependencyModernization(context) {
        try {
            this.statusBar.showLoading('Initializing Dakota Dependency Modernization');
            // Execute dependency modernization command
            await vscode.commands.executeCommand('jaegis.dependencyModernization');
            this.statusBar.showSuccess('Dakota: Dependency modernization completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform dependency modernization: ${error}`);
            throw error;
        }
    }
    /**
     * Handle security vulnerability scan workflow
     */
    async handleSecurityScan(context) {
        try {
            this.statusBar.showLoading('Initializing Dakota Security Scan');
            // Execute security vulnerability scan command
            await vscode.commands.executeCommand('jaegis.checkSecurityVulnerabilities');
            this.statusBar.showSuccess('Dakota: Security scan completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform security scan: ${error}`);
            throw error;
        }
    }
    /**
     * Handle deployment preparation workflow
     */
    async handleDeploymentPreparation(context) {
        try {
            this.statusBar.showLoading('Initializing Phoenix Deployment Preparation');
            // Execute deployment preparation command
            await vscode.commands.executeCommand('jaegis.deploymentPreparation');
            this.statusBar.showSuccess('Phoenix: Deployment preparation completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform deployment preparation: ${error}`);
            throw error;
        }
    }
    /**
     * Handle containerization workflow
     */
    async handleContainerization(context) {
        try {
            this.statusBar.showLoading('Initializing Phoenix Containerization');
            // Execute containerization command
            await vscode.commands.executeCommand('jaegis.containerizeProject');
            this.statusBar.showSuccess('Phoenix: Containerization completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform containerization: ${error}`);
            throw error;
        }
    }
    /**
     * Handle cross-platform deployment workflow
     */
    async handleCrossPlatformDeployment(context) {
        try {
            this.statusBar.showLoading('Initializing Phoenix Cross-Platform Deployment');
            // Execute cross-platform setup command
            await vscode.commands.executeCommand('jaegis.crossPlatformSetup');
            this.statusBar.showSuccess('Phoenix: Cross-platform deployment setup completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform cross-platform deployment setup: ${error}`);
            throw error;
        }
    }
    /**
     * Handle version tracking workflow
     */
    async handleVersionTracking(context) {
        try {
            this.statusBar.showLoading('Initializing Chronos Version Tracking');
            // Execute version tracking command
            await vscode.commands.executeCommand('jaegis.versionTracking');
            this.statusBar.showSuccess('Chronos: Version tracking completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform version tracking: ${error}`);
            throw error;
        }
    }
    /**
     * Handle token monitoring workflow
     */
    async handleTokenMonitoring(context) {
        try {
            this.statusBar.showLoading('Initializing Chronos Token Monitoring');
            // Execute token monitoring command
            await vscode.commands.executeCommand('jaegis.tokenMonitoring');
            this.statusBar.showSuccess('Chronos: Token monitoring activated');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform token monitoring: ${error}`);
            throw error;
        }
    }
    /**
     * Handle model research workflow
     */
    async handleModelResearch(context) {
        try {
            this.statusBar.showLoading('Initializing Chronos Model Research');
            // Execute model updates research command
            await vscode.commands.executeCommand('jaegis.modelUpdatesResearch');
            this.statusBar.showSuccess('Chronos: Model research completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform model research: ${error}`);
            throw error;
        }
    }
    /**
     * Dispose of integration resources
     */
    dispose() {
        // Clean up any resources if needed
        this.isIntegrated = false;
    }
}
exports.AugmentIntegration = AugmentIntegration;
//# sourceMappingURL=AugmentIntegration.js.map