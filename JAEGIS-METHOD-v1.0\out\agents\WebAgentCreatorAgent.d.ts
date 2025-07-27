import { Context7Integration } from '../integration/Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Web Agent Creator - Web Agent Creation & UI Generation Specialist
 *
 * Specialized agent for designing, generating, and deploying web-based AI agent
 * interfaces within the BMAD ecosystem. Provides comprehensive web development
 * capabilities including UI/UX design, automated code generation, and deployment
 * pipeline management with focus on accessibility and performance.
 *
 * Key Capabilities:
 * - Intuitive web agent UI/UX design and prototyping
 * - Advanced web agent generation and implementation
 * - Seamless web deployment and integration
 * - Rigorous quality and security assurance
 * - Responsive design and cross-platform optimization
 *
 * Integration Features:
 * - Context7 automatic research for web design patterns and technologies
 * - Cross-agent collaboration for comprehensive web solutions
 * - Real-time performance monitoring and optimization
 * - Automated accessibility validation and compliance verification
 * - Strategic web agent portfolio management
 */
export declare class WebAgentCreatorAgent {
    private context7;
    private statusBar;
    private logger;
    private generationIntegration;
    private isActive;
    private activeDesigns;
    private generationQueue;
    private deploymentPipeline;
    private performanceMetrics;
    private readonly DESIGN_TIMEOUT;
    private readonly GENERATION_BATCH_SIZE;
    private readonly PERFORMANCE_THRESHOLD;
    private readonly DEPLOYMENT_RETRY_LIMIT;
    private uiComponentLibrary;
    private webAgentTemplates;
    private styleGuideTemplates;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize Web Agent Creator with UI components and templates
     */
    initialize(): Promise<void>;
    /**
     * Design web agent UI/UX based on requirements
     */
    designWebAgentUI(requirements: BMadTypes.WebAgentRequirements): Promise<BMadTypes.WebAgentDesign>;
    /**
     * Generate web agent implementation from approved design
     */
    generateWebAgent(designId: string, generationOptions?: BMadTypes.WebAgentGenerationOptions): Promise<BMadTypes.WebAgentGenerationResult>;
    /**
     * Deploy generated web agent to target environment
     */
    deployWebAgent(generationId: string, deploymentConfig: BMadTypes.WebDeploymentConfiguration): Promise<BMadTypes.WebDeploymentResult>;
    /**
     * Generate comprehensive web agent specification
     */
    generateWebAgentSpec(requirements: BMadTypes.WebAgentRequirements): Promise<string>;
    /**
     * Validate web agent design against UX criteria
     */
    validateWebAgentDesign(designId: string): Promise<BMadTypes.DesignValidationResult>;
    /**
     * Analyze web agent performance and optimization opportunities
     */
    analyzeWebAgentPerformance(deploymentId: string): Promise<BMadTypes.WebPerformanceAnalysis>;
    /**
     * Research web technologies and frameworks
     */
    researchWebTechnologies(domain: string, requirements: string[]): Promise<BMadTypes.WebTechnologyResearchResult>;
    /**
     * Generate style guide for web agent
     */
    generateStyleGuide(designId: string): Promise<string>;
    /**
     * Get current web agent creation status
     */
    getCreationStatus(): BMadTypes.WebAgentCreationStatus;
    private getCurrentDate;
    private generateDesignId;
    private generateRequestId;
    private generateAnalysisId;
    private generateResearchId;
    private loadUIComponentLibrary;
    private loadWebAgentTemplates;
    private loadStyleGuideTemplates;
    private initializePerformanceMetrics;
    private conductUserResearch;
    private designInformationArchitecture;
    private createVisualDesign;
    private performAccessibilityAnalysis;
    private createResponsiveDesign;
    private generatePrototypes;
    private calculateDesignScore;
    private calculateUsabilityScore;
    private generateImplementationPlan;
    private generateQualityFramework;
    private getDefaultGenerationOptions;
    private calculateGenerationPriority;
    private estimateGenerationDuration;
    private validateGeneratedWebAgent;
    private calculateQualityScore;
    private calculatePerformanceScore;
    private createWebDeploymentPipeline;
    private performPreDeploymentValidation;
    private executeWebDeployment;
    private performPostDeploymentValidation;
    private collectPerformanceMetrics;
    private loadTemplate;
    private populateSpecTemplate;
    private loadChecklist;
    private performDesignValidation;
    private collectWebPerformanceMetrics;
    private analyzeCoreWebVitals;
    private identifyPerformanceOptimizations;
    private generatePerformanceRecommendations;
    private calculateOverallPerformanceScore;
    private identifyPriorityActions;
    private analyzeTechnologyLandscape;
    private generateTechnologyRecommendations;
    private assessImplementationComplexity;
    private generateImplementationGuidance;
    private generatePerformanceComparison;
    private populateStyleGuideTemplate;
    private gatherDesignSpecifications;
    /**
     * Shutdown Web Agent Creator
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=WebAgentCreatorAgent.d.ts.map