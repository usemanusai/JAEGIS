import { Context7Integration } from '../integration/Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Agent Creator - AI Agent Creation & Generation Specialist
 *
 * Specialized agent for conceptualizing, designing, and generating new AI agents
 * within the BMAD ecosystem. Provides comprehensive agent development capabilities
 * including automated code generation, deployment pipeline management, and
 * quality assurance validation.
 *
 * Key Capabilities:
 * - Automated agent conceptualization and design
 * - Intelligent agent generation and implementation
 * - Streamlined deployment pipeline management
 * - Comprehensive quality and ethical assurance
 * - Agent lifecycle management and evolution
 *
 * Integration Features:
 * - Context7 automatic research for agent design patterns
 * - Cross-agent collaboration for ecosystem enhancement
 * - Real-time generation monitoring and optimization
 * - Automated quality validation and compliance verification
 * - Strategic agent portfolio management
 */
export declare class AgentCreatorAgent {
    private context7;
    private statusBar;
    private logger;
    private generationIntegration;
    private isActive;
    private activeConceptualizations;
    private generationQueue;
    private deploymentPipeline;
    private qualityMetrics;
    private readonly CONCEPTUALIZATION_TIMEOUT;
    private readonly GENERATION_BATCH_SIZE;
    private readonly QUALITY_THRESHOLD;
    private readonly DEPLOYMENT_RETRY_LIMIT;
    private agentBlueprints;
    private modelRepository;
    private deploymentTemplates;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize Agent Creator with blueprints and templates
     */
    initialize(): Promise<void>;
    /**
     * Conceptualize new AI agent based on requirements
     */
    conceptualizeAgent(requirements: BMadTypes.AgentRequirements): Promise<BMadTypes.AgentConceptualization>;
    /**
     * Generate new AI agent from approved conceptualization
     */
    generateAgent(conceptId: string, generationOptions?: BMadTypes.AgentGenerationOptions): Promise<BMadTypes.AgentGenerationResult>;
    /**
     * Deploy generated agent to target environment
     */
    deployAgent(generationId: string, deploymentConfig: BMadTypes.DeploymentConfiguration): Promise<BMadTypes.DeploymentResult>;
    /**
     * Generate comprehensive agent brief
     */
    generateAgentBrief(requirements: BMadTypes.AgentRequirements): Promise<string>;
    /**
     * Validate agent concept against feasibility criteria
     */
    validateAgentConcept(conceptId: string): Promise<BMadTypes.ConceptValidationResult>;
    /**
     * Analyze agent performance and optimization opportunities
     */
    analyzeAgentPerformance(agentId: string): Promise<BMadTypes.AgentPerformanceAnalysis>;
    /**
     * Research agent models and technologies
     */
    researchAgentModels(domain: string, requirements: string[]): Promise<BMadTypes.ModelResearchResult>;
    /**
     * Generate deployment plan for agent
     */
    generateDeploymentPlan(generationId: string, environment: string): Promise<string>;
    /**
     * Get current agent creation status
     */
    getCreationStatus(): BMadTypes.AgentCreationStatus;
    private getCurrentDate;
    private generateConceptId;
    private generateRequestId;
    private generateAnalysisId;
    private generateResearchId;
    private loadAgentBlueprints;
    private loadModelRepository;
    private loadDeploymentTemplates;
    private initializeQualityMetrics;
    private analyzeRequirements;
    private generateAgentPersona;
    private designAgentArchitecture;
    private performEthicalAnalysis;
    private calculateFeasibilityScore;
    private calculateStrategicValue;
    private generateImplementationPlan;
    private generateQualityFramework;
    private getDefaultGenerationOptions;
    private calculateGenerationPriority;
    private estimateGenerationDuration;
    private validateGeneratedAgent;
    private calculateQualityScore;
    private createDeploymentPipeline;
    private performPreDeploymentValidation;
    private executeDeployment;
    private performPostDeploymentValidation;
    private loadTemplate;
    private populateBriefTemplate;
    private loadChecklist;
    private performConceptValidation;
    private collectPerformanceMetrics;
    private identifyOptimizationOpportunities;
    private generateImprovementRecommendations;
    private calculateOverallPerformanceScore;
    private identifyPriorityActions;
    private analyzeModelRepository;
    private generateModelRecommendations;
    private assessIntegrationComplexity;
    private generateImplementationGuidance;
    private generateCostAnalysis;
    private populateDeploymentTemplate;
    private gatherDeploymentRequirements;
    /**
     * Shutdown Agent Creator
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=AgentCreatorAgent.d.ts.map