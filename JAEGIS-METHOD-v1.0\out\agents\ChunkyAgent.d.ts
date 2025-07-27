import { Context7Integration } from '../integration/Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Chunky - Task Decomposition & Execution Specialist
 *
 * Specialized agent for comprehensive task decomposition, execution orchestration,
 * and background optimization. Operates primarily in the background, silently managing
 * and orchestrating task execution while providing seamless integration with other
 * BMAD agents. Master of task orchestration ensuring no task is too large or complex
 * to be systematically decomposed, planned, and executed with precision.
 *
 * Key Capabilities:
 * - Comprehensive task decomposition and systematic chunking
 * - Advanced multi-agent coordination and execution orchestration
 * - Intelligent background optimization and performance enhancement
 * - Proactive resource management and allocation optimization
 * - Continuous monitoring and adaptive execution management
 *
 * Integration Features:
 * - Context7 automatic research for task management methodologies and optimization techniques
 * - Cross-agent collaboration for comprehensive task execution solutions
 * - Real-time performance monitoring and automated optimization
 * - Professional execution orchestration and quality assurance
 * - Strategic background operation with minimal user interruption
 */
export declare class ChunkyAgent {
    private context7;
    private statusBar;
    private logger;
    private orchestrationIntegration;
    private isActive;
    private activeDecompositions;
    private executionOrchestrations;
    private backgroundOptimizations;
    private orchestrationMetrics;
    private readonly DECOMPOSITION_TIMEOUT;
    private readonly ORCHESTRATION_TIMEOUT;
    private readonly OPTIMIZATION_CYCLE_INTERVAL;
    private readonly COMPLEXITY_THRESHOLD;
    private readonly AGENT_CAPACITY_THRESHOLD;
    private orchestrationPatterns;
    private optimizationFrameworks;
    private executionStrategies;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize Chunky with orchestration patterns and optimization frameworks
     */
    initialize(): Promise<void>;
    /**
     * Analyze and decompose complex tasks into manageable chunks
     */
    decomposeTask(taskRequirements: BMadTypes.TaskRequirements, decompositionOptions?: BMadTypes.DecompositionOptions): Promise<BMadTypes.TaskDecompositionResult>;
    /**
     * Orchestrate multi-agent execution based on decomposition results
     */
    orchestrateExecution(decompositionId: string, orchestrationOptions?: BMadTypes.OrchestrationOptions): Promise<BMadTypes.ExecutionOrchestrationResult>;
    /**
     * Perform continuous background optimization
     */
    performBackgroundOptimization(optimizationScope?: BMadTypes.OptimizationScope): Promise<BMadTypes.BackgroundOptimizationResult>;
    /**
     * Generate task decomposition plan
     */
    generateDecompositionPlan(taskRequirements: BMadTypes.TaskRequirements): Promise<string>;
    /**
     * Create execution orchestration framework
     */
    createOrchestrationFramework(decompositionId: string): Promise<string>;
    /**
     * Research task management best practices
     */
    researchTaskManagementBestPractices(domain: string, requirements: string[]): Promise<BMadTypes.TaskManagementResearchResult>;
    /**
     * Get current orchestration status
     */
    getOrchestrationStatus(): BMadTypes.OrchestrationStatus;
    private getCurrentDate;
    private generateDecompositionId;
    private generateOrchestrationId;
    private generateOptimizationId;
    private generateResearchId;
    private loadOrchestrationPatterns;
    private loadOptimizationFrameworks;
    private loadExecutionStrategies;
    private initializeOrchestrationMetrics;
    private startBackgroundMonitoring;
    private assessTaskComplexity;
    private createSingleAgentResult;
    private analyzeTaskStructure;
    private generateChunkingStrategy;
    private createAgentAssignmentStrategy;
    private developExecutionPlanning;
    private performDependencyAnalysis;
    private generateRiskAssessment;
    private calculateDecompositionMetrics;
    private calculateEfficiencyGain;
    private initializeExecutionEnvironment;
    private performMultiAgentCoordination;
    private executeContinuousMonitoring;
    private performQualityAssurance;
    private executeCompletionTransition;
    private calculateOrchestrationMetrics;
    private calculateExecutionEfficiency;
    private performSystemMonitoring;
    private executeOptimizationPlanning;
    private implementAutomatedOptimization;
    private performLearningAdaptation;
    private executeImpactAssessment;
    private getDefaultOptimizationScope;
    private calculateOptimizationMetrics;
    private calculatePerformanceImprovement;
    private loadTemplate;
    private analyzeTaskForPlanning;
    private populatePlanTemplate;
    private analyzeDecompositionForFramework;
    private populateFrameworkTemplate;
    private analyzeTaskManagementLandscape;
    private generateTaskManagementRecommendations;
    private assessTaskManagementImplementation;
    private generateTaskManagementGuidance;
    private generateTaskOptimizationFramework;
    /**
     * Shutdown Chunky
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=ChunkyAgent.d.ts.map