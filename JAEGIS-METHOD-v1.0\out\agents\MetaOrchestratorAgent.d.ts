import { Context7Integration } from '../integration/Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Meta-Orchestrator Agent - Agent Squad Management & Evolution Specialist
 *
 * Provides comprehensive squad management, evolution planning, and ecosystem optimization
 * for the BMAD AI Agent system. Monitors agent performance, coordinates evolution activities,
 * and ensures optimal squad composition and collaboration effectiveness.
 *
 * Key Capabilities:
 * - Real-time squad architecture monitoring and analysis
 * - Automated research and intelligence gathering for agent methodologies
 * - Intelligent squad generation and evolution planning
 * - Performance optimization and collaboration enhancement
 * - Strategic alignment and ecosystem quality assurance
 *
 * Integration Features:
 * - Context7 automatic research activation for squad methodologies
 * - Real-time agent performance tracking and analytics
 * - Squad evolution pattern recognition and optimization
 * - Cross-agent collaboration monitoring and enhancement
 * - Strategic planning and roadmap development
 */
export declare class MetaOrchestratorAgent {
    private context7;
    private statusBar;
    private logger;
    private isActive;
    private squadMonitoringActive;
    private researchCycleActive;
    private evolutionPlanningActive;
    private agentPerformanceMetrics;
    private collaborationEffectiveness;
    private capabilityGaps;
    private evolutionOpportunities;
    private researchFindings;
    private technologyTrends;
    private competitiveIntelligence;
    private methodologyUpdates;
    private squadSpecifications;
    private generationQueue;
    private validationResults;
    private implementationPlans;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize Meta-Orchestrator with squad monitoring and research systems
     */
    private initializeMetaOrchestrator;
    /**
     * Initialize squad monitoring and performance tracking systems
     */
    private initializeSquadMonitoring;
    /**
     * Initialize research intelligence and automated research systems
     */
    private initializeResearchIntelligence;
    /**
     * Initialize squad generation and evolution planning systems
     */
    private initializeSquadGeneration;
    /**
     * Squad Architecture Monitoring - Real-time monitoring and analysis
     */
    executeSquadArchitectureMonitoring(): Promise<BMadTypes.SquadArchitectureReport>;
    /**
     * Agent Research Intelligence - Automated research and intelligence gathering
     */
    executeAgentResearchIntelligence(): Promise<BMadTypes.ResearchIntelligenceReport>;
    /**
     * Squad Generation Design - Intelligent design and generation of new agents
     */
    executeSquadGenerationDesign(requirements: BMadTypes.SquadRequirements): Promise<BMadTypes.SquadGenerationReport>;
    /**
     * Generate comprehensive squad specification document
     */
    generateSquadSpecification(requirements: BMadTypes.SquadRequirements): Promise<string>;
    /**
     * Generate evolution report for squad transformation analysis
     */
    generateEvolutionReport(evolutionData: BMadTypes.EvolutionData): Promise<string>;
    /**
     * Monitor agent performance across the BMAD ecosystem
     */
    monitorAgentPerformance(): Promise<BMadTypes.AgentPerformanceReport>;
    /**
     * Analyze squad evolution patterns and trends
     */
    analyzeSquadEvolution(): Promise<BMadTypes.SquadEvolutionAnalysis>;
    /**
     * Validate squad proposal against quality and safety standards
     */
    validateSquadProposal(proposal: BMadTypes.SquadProposal): Promise<BMadTypes.ValidationResult>;
    private getCurrentDate;
    private generateReportId;
    private getWorkspaceRoot;
    private loadTemplate;
    private ensureDirectoryExists;
    private initializeAgentPerformanceTracking;
    private initializeCollaborationMonitoring;
    private initializeCapabilityGapDetection;
    private initializeEvolutionOpportunityIdentification;
    private initializeAutomatedResearch;
    private initializeTechnologyTrendMonitoring;
    private initializeCompetitiveIntelligence;
    private initializeMethodologyUpdateTracking;
    private initializeSquadSpecificationGeneration;
    private initializeValidationFrameworks;
    private initializeImplementationPlanning;
    private initializeEvolutionStrategyDevelopment;
    private startContinuousMonitoring;
    private performAgentEcosystemDiscovery;
    private collectPerformanceMetrics;
    private analyzeCollaborationEffectiveness;
    private evaluateArchitectureHealth;
    private generateOptimizationRecommendations;
    private identifyNextActions;
    private calculateOverallQualityScore;
    private analyzeAgentMethodologies;
    private analyzeTechnologyTrends;
    private analyzeCompetitiveIntelligence;
    private analyzeStrategicImplications;
    private generateActionableRecommendations;
    private assessResearchQuality;
    private calculateImplementationPriority;
    private analyzeCapabilityGaps;
    private generateAgentSpecifications;
    private designTechnicalImplementation;
    private createImplementationPlan;
    private calculateStrategicValue;
    private assessImplementationReadiness;
    private populateSquadSpecificationTemplate;
    private populateEvolutionReportTemplate;
    private collectAgentMetrics;
    private calculateCollaborationScore;
    private calculateQualityScore;
    private calculateOverallPerformanceScore;
    private generatePerformanceRecommendations;
    private identifyEvolutionPatterns;
    private analyzeTransformationTrends;
    private analyzePerformanceEvolution;
    private assessStrategicAlignment;
    private generateFutureRecommendations;
    private performSafetyValidation;
    private performIntegrationValidation;
    private performStrategicValidation;
    private calculateValidationScore;
    private determineApprovalStatus;
    /**
     * Get agent status for external monitoring
     */
    getStatus(): BMadTypes.AgentStatus;
    /**
     * Shutdown Meta-Orchestrator agent gracefully
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=MetaOrchestratorAgent.d.ts.map