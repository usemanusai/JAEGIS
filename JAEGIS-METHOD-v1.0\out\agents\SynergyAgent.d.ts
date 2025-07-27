import { Context7Integration } from '../integration/Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Synergy - Integrated Development & AI Enhancement Specialist
 *
 * Comprehensive specialist for holistic project evolution, dependency management,
 * code refinement, and AI integration. Master of project synergy, combining multiple
 * specialized capabilities into a unified, powerful approach that delivers robust,
 * polished, and AI-powered projects with seamless integration and optimization.
 *
 * Key Capabilities:
 * - Comprehensive dependency validation and future-proofing
 * - Advanced code polish and refinement with automated quality enhancement
 * - Cutting-edge AI integration and intelligent automation
 * - Holistic project enhancement with synergistic optimization
 * - Continuous evolution monitoring with predictive enhancement
 *
 * Integration Features:
 * - Context7 automatic research for technology trends and enhancement methodologies
 * - Cross-agent collaboration for comprehensive project enhancement solutions
 * - Real-time enhancement monitoring and automated optimization
 * - Professional integration orchestration and quality assurance
 * - Strategic future-proofing with AI-powered predictive analysis
 */
export declare class SynergyAgent {
    private context7;
    private statusBar;
    private logger;
    private enhancementIntegration;
    private isActive;
    private activeDependencyValidations;
    private activeCodeEnhancements;
    private activeAIIntegrations;
    private enhancementMetrics;
    private readonly DEPENDENCY_VALIDATION_TIMEOUT;
    private readonly CODE_ENHANCEMENT_TIMEOUT;
    private readonly AI_INTEGRATION_TIMEOUT;
    private readonly ENHANCEMENT_CYCLE_INTERVAL;
    private readonly QUALITY_THRESHOLD;
    private readonly PERFORMANCE_IMPROVEMENT_TARGET;
    private integrationPatterns;
    private aiEnhancementTechnologies;
    private enhancementStrategies;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize Synergy with integration patterns and enhancement frameworks
     */
    initialize(): Promise<void>;
    /**
     * Perform comprehensive dependency validation and future-proofing
     */
    validateDependenciesFutureProofing(projectPath: string, validationOptions?: BMadTypes.DependencyValidationOptions): Promise<BMadTypes.DependencyValidationResult>;
    /**
     * Perform comprehensive code polish and refinement
     */
    performCodePolishRefinement(projectPath: string, refinementOptions?: BMadTypes.CodeRefinementOptions): Promise<BMadTypes.CodeRefinementResult>;
    /**
     * Perform comprehensive AI integration and enhancement
     */
    performAIIntegrationEnhancement(projectPath: string, aiIntegrationOptions?: BMadTypes.AIIntegrationOptions): Promise<BMadTypes.AIIntegrationResult>;
    /**
     * Generate integrated enhancement plan
     */
    generateIntegratedEnhancementPlan(projectPath: string, enhancementScope: BMadTypes.EnhancementScope): Promise<string>;
    /**
     * Create AI integration framework
     */
    createAIIntegrationFramework(projectPath: string, aiRequirements: BMadTypes.AIRequirements): Promise<string>;
    /**
     * Research integrated development best practices
     */
    researchIntegratedDevelopmentBestPractices(domain: string, enhancementAreas: string[]): Promise<BMadTypes.IntegratedDevelopmentResearchResult>;
    /**
     * Get current enhancement status
     */
    getEnhancementStatus(): BMadTypes.EnhancementStatus;
    private getCurrentDate;
    private generateValidationId;
    private generateRefinementId;
    private generateIntegrationId;
    private generateResearchId;
    private loadIntegrationPatterns;
    private loadAIEnhancementTechnologies;
    private loadEnhancementStrategies;
    private initializeEnhancementMetrics;
    private startContinuousEnhancementMonitoring;
    private performDependencyDiscovery;
    private executeCompatibilityAnalysis;
    private performSecurityAssessment;
    private executeFutureProofingAnalysis;
    private performValidationPlanning;
    private calculateDependencyValidationMetrics;
    private calculateSecurityScore;
    private calculateFutureReadinessScore;
    private performCodeQualityAssessment;
    private executeCodeQualityEnhancement;
    private performRefactoringImprovement;
    private executeTestSuiteEnhancement;
    private performDocumentationEnhancement;
    private calculateCodeRefinementMetrics;
    private calculateQualityImprovement;
    private performAIOpportunityDiscovery;
    private executeAIArchitectureDesign;
    private performAIModelDevelopment;
    private executeAIIntegrationDeployment;
    private performAIEnhancementLearning;
    private calculateAIIntegrationMetrics;
    private calculateIntelligenceEnhancement;
    private loadTemplate;
    private analyzeProjectForEnhancementPlanning;
    private populateEnhancementPlanTemplate;
    private analyzeProjectForAIFramework;
    private populateAIFrameworkTemplate;
    private analyzeIntegratedDevelopmentLandscape;
    private generateIntegratedEnhancementRecommendations;
    private assessIntegratedImplementation;
    private generateIntegratedImplementationGuidance;
    private generateIntegratedEnhancementFramework;
    /**
     * Shutdown Synergy
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=SynergyAgent.d.ts.map