import { Context7ResearchResult } from '../integration/Context7Integration';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Dakota - Dependency Modernization Specialist Agent
 * Handles automated dependency analysis, modernization, and maintenance
 * with seamless Context7 integration for intelligent research
 */
export interface DependencyInfo {
    name: string;
    currentVersion: string;
    latestVersion?: string;
    type: 'production' | 'development' | 'peer' | 'optional';
    ecosystem: string;
    vulnerabilities?: VulnerabilityInfo[];
    maintenanceStatus?: 'well-maintained' | 'moderate' | 'poor' | 'abandoned';
    licenseInfo?: LicenseInfo;
    updateRecommendation?: UpdateRecommendation;
}
export interface VulnerabilityInfo {
    id: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    title: string;
    description: string;
    patchedVersions?: string[];
    cveId?: string;
}
export interface LicenseInfo {
    license: string;
    compatible: boolean;
    concerns?: string[];
}
export interface UpdateRecommendation {
    action: 'auto-update' | 'manual-review' | 'hold' | 'replace';
    targetVersion?: string;
    reasoning: string;
    riskLevel: 'low' | 'medium' | 'high' | 'critical';
    migrationComplexity?: 'simple' | 'moderate' | 'complex';
    context7Research?: Context7ResearchResult;
}
export interface DependencyAuditResult {
    projectPath: string;
    timestamp: Date;
    totalDependencies: number;
    vulnerabilities: VulnerabilityInfo[];
    outdatedPackages: DependencyInfo[];
    recommendations: UpdateRecommendation[];
    healthScore: number;
    context7Insights: Context7ResearchResult[];
}
/**
 * Dakota Agent - Dependency Modernization Specialist
 */
export declare class DakotaAgent {
    private context7;
    private analyzer;
    private statusBar;
    private dependencyMonitor;
    private isMonitoring;
    constructor(analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager, context7Config?: any);
    /**
     * Perform comprehensive dependency audit
     */
    performDependencyAudit(projectPath?: string): Promise<DependencyAuditResult>;
    /**
     * Perform dependency modernization based on audit results
     */
    performDependencyModernization(auditResult: DependencyAuditResult): Promise<void>;
    /**
     * Start background dependency monitoring
     */
    startDependencyMonitoring(): Promise<void>;
    /**
     * Stop background dependency monitoring
     */
    stopDependencyMonitoring(): void;
    /**
     * Discover dependencies in the project
     */
    private discoverDependencies;
    /**
     * Parse dependency file based on ecosystem
     */
    private parseDependencyFile;
    /**
     * Generate update recommendation for a dependency
     */
    private generateUpdateRecommendation;
    /**
     * Get latest version for a dependency
     */
    private getLatestVersion;
    /**
     * Analyze version difference between current and target
     */
    private analyzeVersionDifference;
    /**
     * Generate reasoning text for recommendation
     */
    private generateRecommendationReasoning;
    /**
     * Extract vulnerabilities from Context7 research
     */
    private extractVulnerabilitiesFromResearch;
    /**
     * Calculate overall health score for dependencies
     */
    private calculateHealthScore;
    /**
     * Prioritize recommendations by risk and impact
     */
    private prioritizeRecommendations;
    /**
     * Execute automatic update
     */
    private executeAutomaticUpdate;
    /**
     * Present manual reviews to user
     */
    private presentManualReviews;
    /**
     * Generate comprehensive audit report
     */
    private generateAuditReport;
    /**
     * Get Dakota agent status
     */
    getStatus(): {
        isMonitoring: boolean;
        context7Available: boolean;
        monitoringStats: any;
        lastAudit?: Date;
    };
    /**
     * Dispose of agent resources
     */
    dispose(): void;
}
//# sourceMappingURL=DakotaAgent.d.ts.map