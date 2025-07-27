import { BMadOrchestrator } from '../orchestrator/BMadOrchestrator';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Integration interface for Augment AI Code extension
 * Provides BMAD functionality as menu options within Augment's interface
 */
export declare class AugmentIntegration {
    private orchestrator;
    private analyzer;
    private statusBar;
    private augmentExtension;
    private isIntegrated;
    constructor(orchestrator: BMadOrchestrator, analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager);
    /**
     * Initialize integration with Augment AI Code extension
     */
    initialize(): Promise<void>;
    /**
     * Integrate BMAD workflows with Augment extension
     */
    private integrateWithAugment;
    /**
     * Register BMAD as a workflow provider with Augment
     */
    private registerBmadWorkflowProvider;
    /**
     * Setup fallback integration using standard VS Code APIs
     */
    private setupFallbackIntegration;
    /**
     * Register BMAD commands in VS Code menus
     */
    private registerVSCodeMenus;
    /**
     * Handle Documentation Mode workflow
     */
    private handleDocumentationMode;
    /**
     * Handle Full Development Mode workflow
     */
    private handleFullDevelopmentMode;
    /**
     * Handle Debug Mode workflow
     */
    private handleDebugMode;
    /**
     * Handle Continue Project workflow
     */
    private handleContinueProject;
    /**
     * Handle Task Overview workflow
     */
    private handleTaskOverview;
    /**
     * Handle Continuous Execution workflow
     */
    private handleContinuousExecution;
    /**
     * Handle Feature Gap Analysis workflow
     */
    private handleFeatureGapAnalysis;
    /**
     * Handle GitHub Integration workflow
     */
    private handleGithubIntegration;
    /**
     * Check if integration with Augment is active
     */
    isAugmentIntegrated(): boolean;
    /**
     * Get Augment extension information
     */
    getAugmentInfo(): {
        available: boolean;
        version?: string;
        id?: string;
    };
    /**
     * Handle dependency audit workflow
     */
    private handleDependencyAudit;
    /**
     * Handle dependency modernization workflow
     */
    private handleDependencyModernization;
    /**
     * Handle security vulnerability scan workflow
     */
    private handleSecurityScan;
    /**
     * Handle deployment preparation workflow
     */
    private handleDeploymentPreparation;
    /**
     * Handle containerization workflow
     */
    private handleContainerization;
    /**
     * Handle cross-platform deployment workflow
     */
    private handleCrossPlatformDeployment;
    /**
     * Handle version tracking workflow
     */
    private handleVersionTracking;
    /**
     * Handle token monitoring workflow
     */
    private handleTokenMonitoring;
    /**
     * Handle model research workflow
     */
    private handleModelResearch;
    /**
     * Handle task completion monitoring workflow
     */
    private handleTaskCompletionMonitoring;
    /**
     * Handle checklist validation workflow
     */
    private handleChecklistValidation;
    /**
     * Handle quality assurance review workflow
     */
    private handleQualityAssuranceReview;
    /**
     * Handle squad architecture monitoring workflow
     */
    private handleSquadArchitectureMonitoring;
    /**
     * Handle agent research intelligence workflow
     */
    private handleAgentResearchIntelligence;
    /**
     * Handle squad generation design workflow
     */
    private handleSquadGenerationDesign;
    /**
     * Handle agent conceptualization workflow
     */
    private handleAgentConceptualization;
    /**
     * Handle agent generation workflow
     */
    private handleAgentGeneration;
    /**
     * Handle agent deployment pipeline workflow
     */
    private handleAgentDeploymentPipeline;
    /**
     * Handle web agent UI design workflow
     */
    private handleWebAgentUIDesign;
    /**
     * Handle web agent generation workflow
     */
    private handleWebAgentGeneration;
    /**
     * Handle web agent deployment workflow
     */
    private handleWebAgentDeployment;
    /**
     * Handle documentation analysis workflow
     */
    private handleDocumentationAnalysis;
    /**
     * Handle quality validation workflow
     */
    private handleQualityValidation;
    /**
     * Handle documentation improvement workflow
     */
    private handleDocumentationImprovement;
    /**
     * Handle task decomposition workflow
     */
    private handleTaskDecomposition;
    /**
     * Handle execution orchestration workflow
     */
    private handleExecutionOrchestration;
    /**
     * Handle background optimization workflow
     */
    private handleBackgroundOptimization;
    private handleDependencyValidationFutureProofing;
    private handleCodePolishRefinement;
    private handleAIIntegrationEnhancement;
    /**
     * Dispose of integration resources
     */
    dispose(): void;
}
//# sourceMappingURL=AugmentIntegration.d.ts.map