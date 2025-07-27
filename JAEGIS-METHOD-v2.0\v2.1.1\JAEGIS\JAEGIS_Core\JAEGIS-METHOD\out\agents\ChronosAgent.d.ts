import { Context7ResearchResult } from '../integration/Context7Integration';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Chronos - Version Control & Token Management Specialist Agent
 * Handles comprehensive version tracking, token monitoring, and temporal intelligence
 * with seamless Context7 integration for model research and optimization strategies
 */
export interface VersionInfo {
    fileName: string;
    currentVersion: string;
    lastModified: Date;
    versionFormat: 'semantic' | 'date-based' | 'custom';
    changeImpact: 'major' | 'minor' | 'patch' | 'maintenance';
    dependencies: string[];
}
export interface TokenUsageInfo {
    modelName: string;
    tokensConsumed: number;
    tokenLimit: number;
    usagePercentage: number;
    costEstimate: number;
    optimizationOpportunities: string[];
}
export interface ModelSpecification {
    modelId: string;
    provider: string;
    contextWindow: number;
    maxOutputTokens: number;
    tokenCounting: string;
    pricing: {
        inputPerToken: number;
        outputPerToken: number;
    };
    rateLimits: {
        requestsPerMinute: number;
        tokensPerMinute: number;
    };
}
export interface VersionTrackingResult {
    projectPath: string;
    timestamp: Date;
    totalFilesTracked: number;
    versionsUpdated: VersionInfo[];
    consistencyScore: number;
    temporalAccuracy: number;
    context7Insights: Context7ResearchResult[];
    recommendations: VersionRecommendation[];
}
export interface TokenMonitoringResult {
    projectPath: string;
    timestamp: Date;
    currentUsage: TokenUsageInfo;
    optimizationsPerformed: number;
    tokensSaved: number;
    efficiencyScore: number;
    context7Research: Context7ResearchResult[];
    alerts: TokenAlert[];
}
export interface VersionRecommendation {
    type: 'consistency' | 'optimization' | 'temporal' | 'dependency';
    priority: 'critical' | 'high' | 'medium' | 'low';
    title: string;
    description: string;
    actionRequired: boolean;
    context7Research?: Context7ResearchResult;
}
export interface TokenAlert {
    level: 'warning' | 'alert' | 'critical' | 'emergency';
    threshold: number;
    currentUsage: number;
    message: string;
    recommendedActions: string[];
    timestamp: Date;
}
/**
 * Chronos Agent - Version Control & Token Management Specialist
 */
export declare class ChronosAgent {
    private context7;
    private analyzer;
    private statusBar;
    private tokenMonitoring;
    private fileWatcher;
    private versionCache;
    private tokenCache;
    constructor(analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager, context7Config?: any);
    /**
     * Perform comprehensive version tracking across JAEGIS ecosystem
     */
    performVersionTracking(projectPath?: string): Promise<VersionTrackingResult>;
    /**
     * Perform real-time token monitoring and optimization
     */
    performTokenMonitoring(): Promise<TokenMonitoringResult>;
    /**
     * Research and update model specifications
     */
    performModelUpdatesResearch(): Promise<void>;
    /**
     * Initialize file system watcher for real-time version tracking
     */
    private initializeFileWatcher;
    /**
     * Handle file changes for real-time version tracking
     */
    private handleFileChange;
    /**
     * Handle file creation for version tracking
     */
    private handleFileCreate;
    /**
     * Handle file deletion for version tracking
     */
    private handleFileDelete;
    /**
     * Discover all JAEGIS ecosystem files for version tracking
     */
    private discoverJAEGISFiles;
    /**
     * Analyze version information for a specific file
     */
    private analyzeFileVersion;
    /**
     * Helper methods for version analysis
     */
    private determineVersionFormat;
    private assessChangeImpact;
    private extractDependencies;
    private calculateVersionConsistency;
    private calculateTemporalAccuracy;
    private generateVersionRecommendations;
    private generateTokenAlerts;
    private calculateTokenEfficiency;
    /**
     * Helper methods for version updates
     */
    private generateNextVersion;
    private updateFileVersion;
    private addVersionToNewFile;
    private updateVersionsWithCurrentDate;
    private generateVersionChangelog;
    private updateModelSpecifications;
    /**
     * Get Chronos agent status
     */
    getStatus(): {
        context7Available: boolean;
        tokenMonitoringActive: boolean;
        fileWatcherActive: boolean;
        versionsCached: number;
        lastUpdate?: Date;
    };
    /**
     * Dispose of agent resources
     */
    dispose(): void;
}
//# sourceMappingURL=ChronosAgent.d.ts.map