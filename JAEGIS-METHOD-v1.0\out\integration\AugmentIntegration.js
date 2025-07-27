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
 * Provides BMAD functionality as menu options within Augment's interface
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
                console.log('Augment AI Code extension not found. BMAD will use standard VS Code integration.');
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
     * Integrate BMAD workflows with Augment extension
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
                await this.registerBmadWorkflowProvider(augmentAPI);
                this.isIntegrated = true;
                console.log('Successfully integrated BMAD with Augment AI Code extension');
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
     * Register BMAD as a workflow provider with Augment
     */
    async registerBmadWorkflowProvider(augmentAPI) {
        const workflowProvider = {
            id: 'bmad-orchestrator',
            name: '🟣 BMAD AI Agent Orchestrator',
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
                },
                {
                    id: 'task-completion-monitoring',
                    name: '🛡️ Sentinel: Task Completion Monitoring',
                    description: 'Comprehensive task completion tracking and validation',
                    icon: '$(checklist)',
                    category: 'Task Management',
                    handler: this.handleTaskCompletionMonitoring.bind(this)
                },
                {
                    id: 'checklist-validation',
                    name: '📋 Sentinel: Checklist Validation',
                    description: 'Intelligent checklist completion validation',
                    icon: '$(list-ordered)',
                    category: 'Quality Assurance',
                    handler: this.handleChecklistValidation.bind(this)
                },
                {
                    id: 'quality-assurance-review',
                    name: '🏆 Sentinel: Quality Assurance Review',
                    description: 'Comprehensive quality assessment and improvement',
                    icon: '$(verified)',
                    category: 'Quality Assurance',
                    handler: this.handleQualityAssuranceReview.bind(this)
                },
                {
                    id: 'squad-architecture-monitoring',
                    name: '🏗️ Meta-Orchestrator: Squad Architecture Monitoring',
                    description: 'Real-time squad performance and collaboration analysis',
                    icon: '$(organization)',
                    category: 'Squad Management',
                    handler: this.handleSquadArchitectureMonitoring.bind(this)
                },
                {
                    id: 'agent-research-intelligence',
                    name: '🔬 Meta-Orchestrator: Agent Research Intelligence',
                    description: 'Automated research and intelligence gathering for agent methodologies',
                    icon: '$(search)',
                    category: 'Squad Management',
                    handler: this.handleAgentResearchIntelligence.bind(this)
                },
                {
                    id: 'squad-generation-design',
                    name: '🎯 Meta-Orchestrator: Squad Generation Design',
                    description: 'Intelligent design and generation of new agent squads',
                    icon: '$(add)',
                    category: 'Squad Management',
                    handler: this.handleSquadGenerationDesign.bind(this)
                }
            ]
        };
        // Agent Creator workflows (Blue theme #3B82F6)
        workflows['agent-creator'] = {
            title: 'Agent Creator - AI Agent Creation & Generation',
            description: 'Automated agent conceptualization, generation, and deployment workflows',
            color: '#3B82F6',
            workflows: [
                {
                    id: 'agent-conceptualization',
                    name: '🧠 Agent Creator: Agent Conceptualization',
                    description: 'Comprehensive conceptualization and design of new AI agents',
                    icon: '$(lightbulb)',
                    category: 'Agent Creation',
                    handler: this.handleAgentConceptualization.bind(this)
                },
                {
                    id: 'agent-generation',
                    name: '⚡ Agent Creator: Agent Generation',
                    description: 'Automated generation and implementation of new AI agents',
                    icon: '$(gear)',
                    category: 'Agent Generation',
                    handler: this.handleAgentGeneration.bind(this)
                },
                {
                    id: 'agent-deployment-pipeline',
                    name: '🚀 Agent Creator: Deployment Pipeline',
                    description: 'Streamlined deployment pipeline for newly generated agents',
                    icon: '$(rocket)',
                    category: 'Deployment Planning',
                    handler: this.handleAgentDeploymentPipeline.bind(this)
                }
            ]
        };
        // Web Agent Creator workflows (Green theme #10B981)
        workflows['web-agent-creator'] = {
            title: 'Web Agent Creator - Web Agent Creation & UI Generation',
            description: 'Comprehensive web agent design, generation, and deployment workflows',
            color: '#10B981',
            workflows: [
                {
                    id: 'web-agent-ui-design',
                    name: '🎨 Web Agent Creator: UI/UX Design',
                    description: 'Comprehensive UI/UX design and prototyping for web-based AI agents',
                    icon: '$(paintcan)',
                    category: 'Web Design',
                    handler: this.handleWebAgentUIDesign.bind(this)
                },
                {
                    id: 'web-agent-generation',
                    name: '⚡ Web Agent Creator: Web Agent Generation',
                    description: 'Automated generation and implementation of web-based AI agents',
                    icon: '$(code)',
                    category: 'Web Generation',
                    handler: this.handleWebAgentGeneration.bind(this)
                },
                {
                    id: 'web-agent-deployment',
                    name: '🚀 Web Agent Creator: Web Deployment',
                    description: 'Streamlined deployment and hosting for web-based AI agents',
                    icon: '$(cloud-upload)',
                    category: 'Web Deployment',
                    handler: this.handleWebAgentDeployment.bind(this)
                }
            ]
        };
        // DocQA workflows (Orange theme #F97316)
        workflows['docqa'] = {
            title: 'DocQA - Documentation Quality Assurance Specialist',
            description: 'Comprehensive documentation quality assurance and repository management workflows',
            color: '#F97316',
            workflows: [
                {
                    id: 'documentation-analysis',
                    name: '📋 DocQA: Documentation Analysis',
                    description: 'Comprehensive documentation analysis and quality assessment',
                    icon: '$(search)',
                    category: 'Documentation Analysis',
                    handler: this.handleDocumentationAnalysis.bind(this)
                },
                {
                    id: 'quality-validation',
                    name: '✅ DocQA: Quality Validation',
                    description: 'Documentation quality validation and compliance checking',
                    icon: '$(verified)',
                    category: 'Quality Validation',
                    handler: this.handleQualityValidation.bind(this)
                },
                {
                    id: 'documentation-improvement',
                    name: '🔧 DocQA: Documentation Improvement',
                    description: 'Documentation enhancement and optimization workflows',
                    icon: '$(tools)',
                    category: 'Documentation Improvement',
                    handler: this.handleDocumentationImprovement.bind(this)
                }
            ]
        };
        // Chunky workflows (Purple theme #8B5CF6)
        workflows['chunky'] = {
            title: 'Chunky - Task Decomposition & Execution Specialist',
            description: 'Comprehensive task decomposition and execution orchestration workflows',
            color: '#8B5CF6',
            workflows: [
                {
                    id: 'task-decomposition',
                    name: '🧩 Chunky: Task Decomposition',
                    description: 'Systematic task decomposition and chunking strategy development',
                    icon: '$(symbol-structure)',
                    category: 'Task Decomposition',
                    handler: this.handleTaskDecomposition.bind(this)
                },
                {
                    id: 'execution-orchestration',
                    name: '🚀 Chunky: Execution Orchestration',
                    description: 'Multi-agent execution orchestration and coordination management',
                    icon: '$(organization)',
                    category: 'Execution Orchestration',
                    handler: this.handleExecutionOrchestration.bind(this)
                },
                {
                    id: 'background-optimization',
                    name: '⚡ Chunky: Background Optimization',
                    description: 'Continuous background optimization and performance enhancement',
                    icon: '$(pulse)',
                    category: 'Background Optimization',
                    handler: this.handleBackgroundOptimization.bind(this)
                }
            ]
        };
        // Synergy workflows (Teal theme #14B8A6)
        workflows['synergy'] = {
            title: 'Synergy - Integrated Development & AI Enhancement Specialist',
            description: 'Comprehensive integrated development and AI enhancement workflows',
            color: '#14B8A6',
            workflows: [
                {
                    id: 'dependency-validation-future-proofing',
                    name: '🔍 Synergy: Dependency Validation & Future-Proofing',
                    description: 'Comprehensive dependency validation and future-proofing analysis',
                    icon: '$(shield)',
                    category: 'Dependency Management',
                    handler: this.handleDependencyValidationFutureProofing.bind(this)
                },
                {
                    id: 'code-polish-refinement',
                    name: '🔧 Synergy: Code Polish & Refinement',
                    description: 'Advanced code polish and refinement with automated quality enhancement',
                    icon: '$(tools)',
                    category: 'Code Quality',
                    handler: this.handleCodePolishRefinement.bind(this)
                },
                {
                    id: 'ai-integration-enhancement',
                    name: '🤖 Synergy: AI Integration & Enhancement',
                    description: 'Cutting-edge AI integration and intelligent automation enhancement',
                    icon: '$(robot)',
                    category: 'AI Integration',
                    handler: this.handleAIIntegrationEnhancement.bind(this)
                }
            ]
        };
        await augmentAPI.registerWorkflowProvider(workflowProvider);
    }
    /**
     * Setup fallback integration using standard VS Code APIs
     */
    async setupFallbackIntegration() {
        // Register BMAD menu items in VS Code's standard locations
        await this.registerVSCodeMenus();
        console.log('BMAD fallback integration initialized');
    }
    /**
     * Register BMAD commands in VS Code menus
     */
    async registerVSCodeMenus() {
        // Commands are already registered by CommandManager
        // This method can be extended to add additional menu contributions
        // Show notification about BMAD availability
        const action = await vscode.window.showInformationMessage('BMAD AI Agent Orchestrator is ready! Access workflows via Command Palette (Ctrl+Shift+P) or status bar.', 'Show Commands', 'Quick Start');
        if (action === 'Show Commands') {
            await vscode.commands.executeCommand('workbench.action.showCommands');
        }
        else if (action === 'Quick Start') {
            await vscode.commands.executeCommand('bmad.quickModeSelect');
        }
    }
    // Workflow Handlers - Bridge Augment UI to BMAD Orchestrator
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
            await vscode.commands.executeCommand('bmad.dependencyAudit');
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
            await vscode.commands.executeCommand('bmad.dependencyModernization');
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
            await vscode.commands.executeCommand('bmad.checkSecurityVulnerabilities');
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
            await vscode.commands.executeCommand('bmad.deploymentPreparation');
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
            await vscode.commands.executeCommand('bmad.containerizeProject');
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
            await vscode.commands.executeCommand('bmad.crossPlatformSetup');
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
            await vscode.commands.executeCommand('bmad.versionTracking');
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
            await vscode.commands.executeCommand('bmad.tokenMonitoring');
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
            await vscode.commands.executeCommand('bmad.modelUpdatesResearch');
            this.statusBar.showSuccess('Chronos: Model research completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform model research: ${error}`);
            throw error;
        }
    }
    /**
     * Handle task completion monitoring workflow
     */
    async handleTaskCompletionMonitoring(context) {
        try {
            this.statusBar.showLoading('Initializing Sentinel Task Completion Monitoring');
            // Execute task completion monitoring command
            await vscode.commands.executeCommand('bmad.taskCompletionMonitoring');
            this.statusBar.showSuccess('Sentinel: Task completion monitoring activated');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform task completion monitoring: ${error}`);
            throw error;
        }
    }
    /**
     * Handle checklist validation workflow
     */
    async handleChecklistValidation(context) {
        try {
            this.statusBar.showLoading('Initializing Sentinel Checklist Validation');
            // Execute checklist validation command
            await vscode.commands.executeCommand('bmad.checklistValidation');
            this.statusBar.showSuccess('Sentinel: Checklist validation completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform checklist validation: ${error}`);
            throw error;
        }
    }
    /**
     * Handle quality assurance review workflow
     */
    async handleQualityAssuranceReview(context) {
        try {
            this.statusBar.showLoading('Initializing Sentinel Quality Assurance Review');
            // Execute quality assurance review command
            await vscode.commands.executeCommand('bmad.qualityAssuranceReview');
            this.statusBar.showSuccess('Sentinel: Quality assurance review completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform quality assurance review: ${error}`);
            throw error;
        }
    }
    /**
     * Handle squad architecture monitoring workflow
     */
    async handleSquadArchitectureMonitoring(context) {
        try {
            this.statusBar.showLoading('Initializing Meta-Orchestrator Squad Architecture Monitoring');
            // Execute squad architecture monitoring command
            await vscode.commands.executeCommand('bmad.squadArchitectureMonitoring');
            this.statusBar.showSuccess('Meta-Orchestrator: Squad architecture monitoring completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform squad architecture monitoring: ${error}`);
            throw error;
        }
    }
    /**
     * Handle agent research intelligence workflow
     */
    async handleAgentResearchIntelligence(context) {
        try {
            this.statusBar.showLoading('Initializing Meta-Orchestrator Agent Research Intelligence');
            // Execute agent research intelligence command
            await vscode.commands.executeCommand('bmad.agentResearchIntelligence');
            this.statusBar.showSuccess('Meta-Orchestrator: Agent research intelligence completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform agent research intelligence: ${error}`);
            throw error;
        }
    }
    /**
     * Handle squad generation design workflow
     */
    async handleSquadGenerationDesign(context) {
        try {
            this.statusBar.showLoading('Initializing Meta-Orchestrator Squad Generation Design');
            // Execute squad generation design command
            await vscode.commands.executeCommand('bmad.squadGenerationDesign');
            this.statusBar.showSuccess('Meta-Orchestrator: Squad generation design completed');
        }
        catch (error) {
            this.statusBar.showError(`Failed to perform squad generation design: ${error}`);
            throw error;
        }
    }
    // Agent Creator Workflow Handlers
    /**
     * Handle agent conceptualization workflow
     */
    async handleAgentConceptualization(context) {
        try {
            this.statusBar.showLoading('Initializing Agent Creator Conceptualization');
            // Execute agent conceptualization command
            await vscode.commands.executeCommand('bmad.conceptualizeAgent');
            this.statusBar.showSuccess('Agent Creator: Conceptualization workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Agent Creator: Conceptualization workflow failed - ${error}`);
            this.logger.error('Agent conceptualization workflow failed', error);
        }
    }
    /**
     * Handle agent generation workflow
     */
    async handleAgentGeneration(context) {
        try {
            this.statusBar.showLoading('Initializing Agent Creator Generation');
            // Execute agent generation command
            await vscode.commands.executeCommand('bmad.generateAgent');
            this.statusBar.showSuccess('Agent Creator: Generation workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Agent Creator: Generation workflow failed - ${error}`);
            this.logger.error('Agent generation workflow failed', error);
        }
    }
    /**
     * Handle agent deployment pipeline workflow
     */
    async handleAgentDeploymentPipeline(context) {
        try {
            this.statusBar.showLoading('Initializing Agent Creator Deployment Pipeline');
            // Execute agent deployment command
            await vscode.commands.executeCommand('bmad.deployAgent');
            this.statusBar.showSuccess('Agent Creator: Deployment pipeline workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Agent Creator: Deployment pipeline workflow failed - ${error}`);
            this.logger.error('Agent deployment pipeline workflow failed', error);
        }
    }
    // Web Agent Creator Workflow Handlers
    /**
     * Handle web agent UI design workflow
     */
    async handleWebAgentUIDesign(context) {
        try {
            this.statusBar.showLoading('Initializing Web Agent Creator UI Design');
            // Execute web agent UI design command
            await vscode.commands.executeCommand('bmad.designWebAgentUI');
            this.statusBar.showSuccess('Web Agent Creator: UI design workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Web Agent Creator: UI design workflow failed - ${error}`);
            this.logger.error('Web agent UI design workflow failed', error);
        }
    }
    /**
     * Handle web agent generation workflow
     */
    async handleWebAgentGeneration(context) {
        try {
            this.statusBar.showLoading('Initializing Web Agent Creator Generation');
            // Execute web agent generation command
            await vscode.commands.executeCommand('bmad.generateWebAgent');
            this.statusBar.showSuccess('Web Agent Creator: Generation workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Web Agent Creator: Generation workflow failed - ${error}`);
            this.logger.error('Web agent generation workflow failed', error);
        }
    }
    /**
     * Handle web agent deployment workflow
     */
    async handleWebAgentDeployment(context) {
        try {
            this.statusBar.showLoading('Initializing Web Agent Creator Deployment');
            // Execute web agent deployment command
            await vscode.commands.executeCommand('bmad.deployWebAgent');
            this.statusBar.showSuccess('Web Agent Creator: Deployment workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Web Agent Creator: Deployment workflow failed - ${error}`);
            this.logger.error('Web agent deployment workflow failed', error);
        }
    }
    // DocQA Workflow Handlers
    /**
     * Handle documentation analysis workflow
     */
    async handleDocumentationAnalysis(context) {
        try {
            this.statusBar.showLoading('Initializing DocQA Documentation Analysis');
            // Execute documentation analysis command
            await vscode.commands.executeCommand('bmad.analyzeDocumentation');
            this.statusBar.showSuccess('DocQA: Documentation analysis workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`DocQA: Documentation analysis workflow failed - ${error}`);
            this.logger.error('Documentation analysis workflow failed', error);
        }
    }
    /**
     * Handle quality validation workflow
     */
    async handleQualityValidation(context) {
        try {
            this.statusBar.showLoading('Initializing DocQA Quality Validation');
            // Execute quality validation command
            await vscode.commands.executeCommand('bmad.validateDocumentationStandards');
            this.statusBar.showSuccess('DocQA: Quality validation workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`DocQA: Quality validation workflow failed - ${error}`);
            this.logger.error('Quality validation workflow failed', error);
        }
    }
    /**
     * Handle documentation improvement workflow
     */
    async handleDocumentationImprovement(context) {
        try {
            this.statusBar.showLoading('Initializing DocQA Documentation Improvement');
            // Execute documentation improvement command
            await vscode.commands.executeCommand('bmad.improveDocumentation');
            this.statusBar.showSuccess('DocQA: Documentation improvement workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`DocQA: Documentation improvement workflow failed - ${error}`);
            this.logger.error('Documentation improvement workflow failed', error);
        }
    }
    // Chunky Workflow Handlers
    /**
     * Handle task decomposition workflow
     */
    async handleTaskDecomposition(context) {
        try {
            this.statusBar.showLoading('Initializing Chunky Task Decomposition');
            // Execute task decomposition command
            await vscode.commands.executeCommand('bmad.decomposeTask');
            this.statusBar.showSuccess('Chunky: Task decomposition workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Chunky: Task decomposition workflow failed - ${error}`);
            this.logger.error('Task decomposition workflow failed', error);
        }
    }
    /**
     * Handle execution orchestration workflow
     */
    async handleExecutionOrchestration(context) {
        try {
            this.statusBar.showLoading('Initializing Chunky Execution Orchestration');
            // Execute execution orchestration command
            await vscode.commands.executeCommand('bmad.orchestrateExecution');
            this.statusBar.showSuccess('Chunky: Execution orchestration workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Chunky: Execution orchestration workflow failed - ${error}`);
            this.logger.error('Execution orchestration workflow failed', error);
        }
    }
    /**
     * Handle background optimization workflow
     */
    async handleBackgroundOptimization(context) {
        try {
            this.statusBar.showLoading('Initializing Chunky Background Optimization');
            // Execute background optimization command
            await vscode.commands.executeCommand('bmad.performBackgroundOptimization');
            this.statusBar.showSuccess('Chunky: Background optimization workflow completed');
        }
        catch (error) {
            this.statusBar.showError(`Chunky: Background optimization workflow failed - ${error}`);
            this.logger.error('Background optimization workflow failed', error);
        }
    }
    // Synergy workflow handlers
    async handleDependencyValidationFutureProofing() {
        await vscode.commands.executeCommand('bmad.validateDependenciesFutureProofing');
    }
    async handleCodePolishRefinement() {
        await vscode.commands.executeCommand('bmad.performCodePolishRefinement');
    }
    async handleAIIntegrationEnhancement() {
        await vscode.commands.executeCommand('bmad.performAIIntegrationEnhancement');
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