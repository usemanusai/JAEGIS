import { Context7Integration, Context7ResearchResult } from '../integration/Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Background Dependency Monitoring System for Dakota Agent
 * Provides continuous monitoring of dependencies with configurable policies
 * and minimal performance impact on VS Code
 */
export interface MonitoringPolicy {
    securityCheckInterval: number;
    updateCheckInterval: number;
    autoUpdateEnabled: boolean;
    autoUpdateRiskLevel: 'low' | 'medium' | 'high';
    notificationThreshold: 'critical' | 'high' | 'medium' | 'low';
    backgroundProcessingEnabled: boolean;
    maxConcurrentChecks: number;
}
export interface MonitoringAlert {
    id: string;
    type: 'security' | 'update' | 'maintenance' | 'license';
    severity: 'critical' | 'high' | 'medium' | 'low';
    packageName: string;
    currentVersion: string;
    message: string;
    actionRequired: boolean;
    timestamp: Date;
    context7Research?: Context7ResearchResult;
}
export interface MonitoringStats {
    totalPackagesMonitored: number;
    lastSecurityCheck: Date | null;
    lastUpdateCheck: Date | null;
    alertsGenerated: number;
    autoUpdatesPerformed: number;
    context7QueriesExecuted: number;
    averageResponseTime: number;
}
/**
 * Background Dependency Monitor
 * Runs continuous monitoring with minimal performance impact
 */
export declare class DependencyMonitor {
    private context7;
    private statusBar;
    private isMonitoring;
    private monitoringPolicy;
    private activeAlerts;
    private monitoringStats;
    private securityCheckTimer;
    private updateCheckTimer;
    private workspaceWatcher;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, policy?: Partial<MonitoringPolicy>);
    /**
     * Start background monitoring
     */
    startMonitoring(): Promise<void>;
    /**
     * Stop background monitoring
     */
    stopMonitoring(): void;
    /**
     * Update monitoring policy
     */
    updatePolicy(newPolicy: Partial<MonitoringPolicy>): void;
    /**
     * Get current monitoring status
     */
    getMonitoringStatus(): {
        isActive: boolean;
        policy: MonitoringPolicy;
        stats: MonitoringStats;
        activeAlerts: MonitoringAlert[];
    };
    /**
     * Load configuration from VS Code settings
     */
    private loadConfiguration;
    /**
     * Set up file system watchers for dependency files
     */
    private setupFileWatchers;
    /**
     * Schedule periodic security checks
     */
    private scheduleSecurityChecks;
    /**
     * Schedule periodic update checks
     */
    private scheduleUpdateChecks;
    /**
     * Perform initial scan when monitoring starts
     */
    private performInitialScan;
    /**
     * Perform security vulnerability check
     */
    private performSecurityCheck;
    /**
     * Perform update availability check
     */
    private performUpdateCheck;
    /**
     * Handle dependency file changes
     */
    private handleDependencyFileChange;
    /**
     * Discover dependencies in workspace (simplified)
     */
    private discoverDependencies;
    /**
     * Process security research results
     */
    private processSecurityResearch;
    /**
     * Determine severity from research insights
     */
    private determineSeverity;
    /**
     * Add alert to active alerts
     */
    private addAlert;
    /**
     * Check if alert should trigger notification
     */
    private shouldShowNotification;
    /**
     * Show alert notification
     */
    private showAlert;
    /**
     * Dispose of monitoring resources
     */
    dispose(): void;
}
//# sourceMappingURL=DependencyMonitor.d.ts.map