import { Context7Integration } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Token Monitoring Integration Module for Chronos Agent
 * Provides real-time token tracking, optimization, and model specification management
 * Automatically activates for token-related tasks with intelligent monitoring and alerts
 */
export interface ModelSpecification {
    modelId: string;
    provider: string;
    contextWindow: number;
    maxOutputTokens: number;
    effectiveInputLimit: number;
    tokenCounting: string;
    pricing: {
        inputPerToken: number;
        outputPerToken: number;
    };
    rateLimits: {
        requestsPerMinute: number;
        tokensPerMinute: number;
        requestsPerDay: number;
    };
    lastUpdated: Date;
}
export interface TokenUsageInfo {
    modelName: string;
    tokensConsumed: number;
    tokenLimit: number;
    usagePercentage: number;
    costEstimate: number;
    optimizationOpportunities: string[];
    conversationLength: number;
    averageTokensPerExchange: number;
}
export interface OptimizationResult {
    optimizationsCount: number;
    tokensSaved: number;
    originalLength: number;
    optimizedLength: number;
    qualityScore: number;
    techniques: string[];
    preservedContext: string[];
}
export interface TokenThresholds {
    warning: number;
    alert: number;
    critical: number;
    emergency: number;
}
/**
 * Token Monitoring Integration Service
 * Handles real-time token tracking, optimization, and model management
 */
export declare class TokenMonitoringIntegration {
    private context7;
    private statusBar;
    private modelDatabase;
    private currentModel;
    private tokenUsageHistory;
    private optimizationHistory;
    private monitoringActive;
    private thresholds;
    constructor(context7: Context7Integration, statusBar: StatusBarManager);
    /**
     * Detect current AI model being used
     */
    detectCurrentModel(): Promise<ModelSpecification>;
    /**
     * Get current token usage information
     */
    getCurrentTokenUsage(): Promise<TokenUsageInfo>;
    /**
     * Perform token optimization based on current usage
     */
    performOptimization(usage: TokenUsageInfo): Promise<OptimizationResult>;
    /**
     * Update model database with latest specifications
     */
    updateModelDatabase(): Promise<void>;
    /**
     * Check if monitoring is active
     */
    isActive(): boolean;
    /**
     * Start real-time token monitoring
     */
    startMonitoring(): void;
    /**
     * Stop real-time token monitoring
     */
    stopMonitoring(): void;
    /**
     * Get token usage history
     */
    getUsageHistory(): TokenUsageInfo[];
    /**
     * Get optimization history
     */
    getOptimizationHistory(): OptimizationResult[];
    /**
     * Private helper methods
     */
    private initializeModelDatabase;
    private simulateModelDetection;
    private getDefaultModel;
    private simulateTokenUsage;
    private identifyOptimizationOpportunities;
    private performEmergencyOptimization;
    private performCriticalOptimization;
    private performAlertOptimization;
    private performWarningOptimization;
    private getModelsForProvider;
    private updateModelSpecification;
    /**
     * Dispose of integration resources
     */
    dispose(): void;
}
//# sourceMappingURL=TokenMonitoringIntegration.d.ts.map