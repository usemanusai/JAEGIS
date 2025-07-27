import { JAEGISOrchestrator } from '../orchestrator/JAEGISOrchestrator';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Integration interface for Augment AI Code extension
 * Provides JAEGIS functionality as menu options within Augment's interface
 */
export declare class AugmentIntegration {
    private orchestrator;
    private analyzer;
    private statusBar;
    private augmentExtension;
    private isIntegrated;
    constructor(orchestrator: JAEGISOrchestrator, analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager);
    /**
     * Initialize integration with Augment AI Code extension
     */
    initialize(): Promise<void>;
    /**
     * Integrate JAEGIS workflows with Augment extension
     */
    private integrateWithAugment;
    /**
     * Register JAEGIS as a workflow provider with Augment
     */
    private registerJaegisWorkflowProvider;
    /**
     * Setup fallback integration using standard VS Code APIs
     */
    private setupFallbackIntegration;
    /**
     * Register JAEGIS commands in VS Code menus
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
     * Dispose of integration resources
     */
    dispose(): void;
}
//# sourceMappingURL=AugmentIntegration.d.ts.map