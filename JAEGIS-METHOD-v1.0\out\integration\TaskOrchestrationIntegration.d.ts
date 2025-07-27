import { Context7Integration } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Task Orchestration Integration Module
 *
 * Provides comprehensive task orchestration capabilities including automated
 * decomposition, multi-agent coordination, and background optimization for the
 * BMAD Chunky system. Handles the complete task orchestration pipeline from
 * complexity assessment to execution completion with professional coordination
 * and optimization standards.
 *
 * Key Features:
 * - Automated task complexity assessment and decomposition triggering
 * - Comprehensive multi-agent coordination and execution orchestration
 * - Intelligent background optimization and performance enhancement
 * - Real-time monitoring and adaptive execution management
 * - Professional resource allocation and workload balancing
 *
 * Integration Capabilities:
 * - Context7 automatic research for task management methodologies and optimization techniques
 * - Cross-platform task orchestration and execution coordination
 * - Real-time performance monitoring and optimization tracking
 * - Automated quality assurance and validation throughout execution
 * - Professional background operation with minimal user interruption
 */
export declare class TaskOrchestrationIntegration {
    private context7;
    private statusBar;
    private logger;
    private isOrchestrating;
    private activeOrchestrations;
    private orchestrationFrameworks;
    private optimizationStrategies;
    private orchestrationMetrics;
    private readonly ORCHESTRATION_TIMEOUT;
    private readonly MAX_CONCURRENT_ORCHESTRATIONS;
    private readonly COMPLEXITY_THRESHOLD;
    private readonly EFFICIENCY_THRESHOLD;
    private readonly ORCHESTRATION_FRAMEWORKS;
    private readonly OPTIMIZATION_PATTERNS;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize task orchestration integration
     */
    initialize(): Promise<void>;
    /**
     * Orchestrate task decomposition and execution comprehensively
     */
    orchestrateTaskExecution(request: BMadTypes.OrchestrationRequest): Promise<BMadTypes.OrchestrationResult>;
    /**
     * Execute comprehensive task complexity assessment
     */
    executeComplexityAssessment(request: BMadTypes.OrchestrationRequest, session: BMadTypes.OrchestrationSession): Promise<BMadTypes.ComplexityAssessmentResult>;
    /**
     * Perform systematic task decomposition
     */
    performTaskDecomposition(request: BMadTypes.OrchestrationRequest, session: BMadTypes.OrchestrationSession): Promise<BMadTypes.TaskDecompositionResult>;
    /**
     * Execute multi-agent coordination planning
     */
    executeCoordinationPlanning(request: BMadTypes.OrchestrationRequest, session: BMadTypes.OrchestrationSession): Promise<BMadTypes.CoordinationPlanningResult>;
    /**
     * Perform execution orchestration and monitoring
     */
    performExecutionOrchestration(request: BMadTypes.OrchestrationRequest, session: BMadTypes.OrchestrationSession): Promise<BMadTypes.ExecutionOrchestrationResult>;
    private getCurrentDate;
    private generateOrchestrationId;
    private generateAssessmentId;
    private generateDecompositionId;
    private generatePlanningId;
    private generateExecutionId;
    private calculateOverallEfficiency;
    private calculatePerformanceImprovement;
    private calculateOverallComplexityScore;
    private generateDecompositionRecommendation;
    private calculateDecompositionEfficiency;
    private identifyParallelizationOpportunities;
    private calculateCoordinationEfficiency;
    private optimizeCollaboration;
    private calculateExecutionEfficiency;
    private loadOrchestrationFrameworks;
    private initializeOptimizationStrategies;
    private initializeOrchestrationMetrics;
    private createOrchestrationSession;
    private analyzeTaskStructure;
    private assessResourceRequirements;
    private evaluateTimelineComplexity;
    private assessStakeholderComplexity;
    private evaluateIntegrationComplexity;
    private calculateComplexityMetrics;
    private executeHierarchicalBreakdown;
    private performChunkSizeOptimization;
    private executeDependencyAnalysis;
    private performAgentCapabilityMatching;
    private executeTimelineOptimization;
    private calculateDecompositionMetrics;
    private developAgentAssignmentStrategy;
    private createCommunicationProtocols;
    private designResourceAllocation;
    private establishQualityGates;
    private createMonitoringSystems;
    private calculateCoordinationMetrics;
    private launchCoordinatedExecution;
    private executeRealTimeMonitoring;
    private performAdaptiveExecutionManagement;
    private executeQualityAssuranceExecution;
    private performCompletionVerification;
    private calculateExecutionMetrics;
    private executeQualityAssurance;
    private performBackgroundOptimization;
    private calculateOrchestrationMetrics;
    private generateOptimizationRecommendations;
    /**
     * Shutdown task orchestration integration
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=TaskOrchestrationIntegration.d.ts.map