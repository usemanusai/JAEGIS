import { Context7Integration } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Agent Generation Integration Module
 *
 * Provides automated agent generation capabilities including code generation,
 * template processing, and quality validation for the BMAD AI Agent system.
 * Handles the complete agent generation pipeline from conceptualization to
 * deployment-ready implementation.
 *
 * Key Features:
 * - Automated code generation from agent blueprints
 * - Template-based agent implementation creation
 * - Quality validation and compliance verification
 * - Integration with BMAD ecosystem patterns
 * - Performance optimization and efficiency analysis
 *
 * Integration Capabilities:
 * - Context7 automatic research for generation best practices
 * - Cross-agent pattern analysis and optimization
 * - Real-time generation monitoring and analytics
 * - Automated testing and validation integration
 * - Deployment pipeline preparation and optimization
 */
export declare class AgentGenerationIntegration {
    private context7;
    private statusBar;
    private logger;
    private isGenerating;
    private activeGenerations;
    private generationTemplates;
    private qualityValidators;
    private generationMetrics;
    private readonly GENERATION_TIMEOUT;
    private readonly MAX_CONCURRENT_GENERATIONS;
    private readonly QUALITY_THRESHOLD;
    private readonly VALIDATION_RETRY_LIMIT;
    private readonly BMAD_PATTERNS;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize agent generation integration
     */
    initialize(): Promise<void>;
    /**
     * Generate complete agent implementation from conceptualization
     */
    generateAgent(request: BMadTypes.AgentGenerationRequest): Promise<BMadTypes.AgentGenerationResult>;
    /**
     * Generate agent core implementation class
     */
    generateAgentCore(request: BMadTypes.AgentGenerationRequest, session: BMadTypes.GenerationSession): Promise<BMadTypes.GeneratedArtifact>;
    /**
     * Generate task workflow implementations
     */
    generateTaskWorkflows(request: BMadTypes.AgentGenerationRequest, session: BMadTypes.GenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    /**
     * Generate safety and quality checklists
     */
    generateSafetyChecklists(request: BMadTypes.AgentGenerationRequest, session: BMadTypes.GenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    /**
     * Generate data sources and knowledge bases
     */
    generateDataSources(request: BMadTypes.AgentGenerationRequest, session: BMadTypes.GenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    /**
     * Generate professional templates
     */
    generateTemplates(request: BMadTypes.AgentGenerationRequest, session: BMadTypes.GenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    /**
     * Generate integration modules
     */
    generateIntegrationModules(request: BMadTypes.AgentGenerationRequest, session: BMadTypes.GenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    private getCurrentDate;
    private generateGenerationId;
    private generateArtifactId;
    private calculateQualityScore;
    private loadGenerationTemplates;
    private initializeQualityValidators;
    private initializeGenerationMetrics;
    private createGenerationSession;
    private processTemplate;
    private validateGeneratedCode;
    private prepareAgentCoreVariables;
    private prepareWorkflowVariables;
    private prepareChecklistVariables;
    private prepareDataSourceVariables;
    private prepareTemplateVariables;
    private prepareIntegrationVariables;
    private validateWorkflow;
    private validateChecklist;
    private validateDataSource;
    private validateTemplate;
    private validateIntegration;
    private countChecklistItems;
    private performQualityValidation;
    private calculateGenerationMetrics;
    private assessDeploymentReadiness;
    private generateVSCodeIntegration;
    private generateAugmentIntegration;
    /**
     * Shutdown agent generation integration
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=AgentGenerationIntegration.d.ts.map