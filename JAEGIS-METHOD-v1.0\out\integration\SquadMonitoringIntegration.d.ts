import { Context7Integration } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Squad Monitoring Integration Module
 *
 * Provides real-time agent performance tracking, squad evolution analysis,
 * and ecosystem optimization for the BMAD AI Agent system. Monitors all
 * agents continuously and provides strategic insights for squad management.
 *
 * Key Features:
 * - Real-time agent performance monitoring and analytics
 * - Squad collaboration effectiveness tracking
 * - Evolution pattern recognition and analysis
 * - Performance optimization recommendations
 * - Strategic alignment assessment and reporting
 *
 * Integration Capabilities:
 * - Context7 automatic research for squad optimization strategies
 * - Cross-agent performance correlation analysis
 * - Predictive analytics for squad evolution planning
 * - Automated reporting and dashboard generation
 * - Strategic decision support and recommendation engine
 */
export declare class SquadMonitoringIntegration {
    private context7;
    private statusBar;
    private logger;
    private isMonitoring;
    private monitoringInterval;
    private agentMetrics;
    private collaborationData;
    private evolutionTrends;
    private performanceHistory;
    private readonly MONITORING_INTERVAL;
    private readonly HISTORY_RETENTION_DAYS;
    private readonly PERFORMANCE_THRESHOLD;
    private readonly COLLABORATION_THRESHOLD;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize squad monitoring integration
     */
    initialize(): Promise<void>;
    /**
     * Start continuous squad monitoring
     */
    startMonitoring(): Promise<void>;
    /**
     * Stop squad monitoring
     */
    stopMonitoring(): Promise<void>;
    /**
     * Perform a complete monitoring cycle
     */
    private performMonitoringCycle;
    /**
     * Collect performance metrics from all BMAD agents
     */
    private collectAgentMetrics;
    /**
     * Analyze collaboration effectiveness between agents
     */
    private analyzeCollaboration;
    /**
     * Track evolution patterns and trends
     */
    private trackEvolutionPatterns;
    /**
     * Generate insights and recommendations based on monitoring data
     */
    private generateInsights;
    /**
     * Update performance history for trend analysis
     */
    private updatePerformanceHistory;
    /**
     * Get current squad monitoring status
     */
    getMonitoringStatus(): BMadTypes.SquadMonitoringStatus;
    /**
     * Generate comprehensive squad monitoring report
     */
    generateMonitoringReport(): Promise<BMadTypes.SquadMonitoringReport>;
    private getCurrentDate;
    private calculateOverallPerformance;
    private calculateOverallCollaboration;
    private calculateAverageResponseTime;
    private calculateAverageSuccessRate;
    private initializePerformanceTracking;
    private initializeCollaborationMonitoring;
    private initializeEvolutionAnalysis;
    private getAgentPerformanceMetrics;
    private calculateCollaborationEffectiveness;
    private analyzeEvolutionTrend;
    private identifyPerformanceIssues;
    private generateOptimizationRecommendations;
    private generateCurrentInsights;
    private generateCurrentRecommendations;
    /**
     * Shutdown squad monitoring integration
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=SquadMonitoringIntegration.d.ts.map