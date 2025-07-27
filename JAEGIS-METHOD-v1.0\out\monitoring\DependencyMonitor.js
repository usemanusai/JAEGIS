"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.DependencyMonitor = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
/**
 * Background Dependency Monitor
 * Runs continuous monitoring with minimal performance impact
 */
class DependencyMonitor {
    context7;
    statusBar;
    isMonitoring = false;
    monitoringPolicy;
    activeAlerts = new Map();
    monitoringStats;
    securityCheckTimer = null;
    updateCheckTimer = null;
    workspaceWatcher = null;
    constructor(context7, statusBar, policy) {
        this.context7 = context7;
        this.statusBar = statusBar;
        // Default monitoring policy
        this.monitoringPolicy = {
            securityCheckInterval: 4 * 60 * 60 * 1000, // 4 hours
            updateCheckInterval: 24 * 60 * 60 * 1000, // 24 hours
            autoUpdateEnabled: true,
            autoUpdateRiskLevel: 'low',
            notificationThreshold: 'medium',
            backgroundProcessingEnabled: true,
            maxConcurrentChecks: 3,
            ...policy
        };
        this.monitoringStats = {
            totalPackagesMonitored: 0,
            lastSecurityCheck: null,
            lastUpdateCheck: null,
            alertsGenerated: 0,
            autoUpdatesPerformed: 0,
            context7QueriesExecuted: 0,
            averageResponseTime: 0
        };
        this.loadConfiguration();
    }
    /**
     * Start background monitoring
     */
    async startMonitoring() {
        if (this.isMonitoring) {
            return;
        }
        this.isMonitoring = true;
        console.log('Dakota: Starting background dependency monitoring');
        // Set up file system watchers for dependency files
        this.setupFileWatchers();
        // Schedule periodic checks
        this.scheduleSecurityChecks();
        this.scheduleUpdateChecks();
        // Perform initial scan
        await this.performInitialScan();
        this.statusBar.showInfo('Dakota: Background monitoring active');
    }
    /**
     * Stop background monitoring
     */
    stopMonitoring() {
        if (!this.isMonitoring) {
            return;
        }
        this.isMonitoring = false;
        console.log('Dakota: Stopping background dependency monitoring');
        // Clear timers
        if (this.securityCheckTimer) {
            clearInterval(this.securityCheckTimer);
            this.securityCheckTimer = null;
        }
        if (this.updateCheckTimer) {
            clearInterval(this.updateCheckTimer);
            this.updateCheckTimer = null;
        }
        // Dispose file watchers
        if (this.workspaceWatcher) {
            this.workspaceWatcher.dispose();
            this.workspaceWatcher = null;
        }
        this.statusBar.showInfo('Dakota: Background monitoring stopped');
    }
    /**
     * Update monitoring policy
     */
    updatePolicy(newPolicy) {
        this.monitoringPolicy = { ...this.monitoringPolicy, ...newPolicy };
        // Restart monitoring with new policy if currently active
        if (this.isMonitoring) {
            this.stopMonitoring();
            this.startMonitoring();
        }
    }
    /**
     * Get current monitoring status
     */
    getMonitoringStatus() {
        return {
            isActive: this.isMonitoring,
            policy: this.monitoringPolicy,
            stats: this.monitoringStats,
            activeAlerts: Array.from(this.activeAlerts.values())
        };
    }
    /**
     * Load configuration from VS Code settings
     */
    loadConfiguration() {
        const config = vscode.workspace.getConfiguration('bmad.dakota.monitoring');
        this.monitoringPolicy.securityCheckInterval = config.get('securityCheckInterval', 4 * 60 * 60 * 1000);
        this.monitoringPolicy.updateCheckInterval = config.get('updateCheckInterval', 24 * 60 * 60 * 1000);
        this.monitoringPolicy.autoUpdateEnabled = config.get('autoUpdateEnabled', true);
        this.monitoringPolicy.autoUpdateRiskLevel = config.get('autoUpdateRiskLevel', 'low');
        this.monitoringPolicy.notificationThreshold = config.get('notificationThreshold', 'medium');
        this.monitoringPolicy.backgroundProcessingEnabled = config.get('backgroundProcessingEnabled', true);
        this.monitoringPolicy.maxConcurrentChecks = config.get('maxConcurrentChecks', 3);
    }
    /**
     * Set up file system watchers for dependency files
     */
    setupFileWatchers() {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            return;
        }
        // Watch for changes to dependency files
        const dependencyFiles = [
            'package.json',
            'package-lock.json',
            'yarn.lock',
            'requirements.txt',
            'pyproject.toml',
            'Cargo.toml',
            'Cargo.lock',
            'go.mod',
            'go.sum',
            'pom.xml',
            'build.gradle',
            'composer.json',
            'composer.lock',
            'Gemfile',
            'Gemfile.lock'
        ];
        const pattern = `**/{${dependencyFiles.join(',')}}`;
        this.workspaceWatcher = vscode.workspace.createFileSystemWatcher(pattern);
        this.workspaceWatcher.onDidChange(async (uri) => {
            console.log(`Dakota: Dependency file changed: ${uri.fsPath}`);
            await this.handleDependencyFileChange(uri);
        });
        this.workspaceWatcher.onDidCreate(async (uri) => {
            console.log(`Dakota: Dependency file created: ${uri.fsPath}`);
            await this.handleDependencyFileChange(uri);
        });
    }
    /**
     * Schedule periodic security checks
     */
    scheduleSecurityChecks() {
        this.securityCheckTimer = setInterval(async () => {
            if (this.monitoringPolicy.backgroundProcessingEnabled) {
                await this.performSecurityCheck();
            }
        }, this.monitoringPolicy.securityCheckInterval);
    }
    /**
     * Schedule periodic update checks
     */
    scheduleUpdateChecks() {
        this.updateCheckTimer = setInterval(async () => {
            if (this.monitoringPolicy.backgroundProcessingEnabled) {
                await this.performUpdateCheck();
            }
        }, this.monitoringPolicy.updateCheckInterval);
    }
    /**
     * Perform initial scan when monitoring starts
     */
    async performInitialScan() {
        try {
            console.log('Dakota: Performing initial dependency scan');
            // Lightweight initial scan
            await this.performSecurityCheck();
            // Schedule update check for later to avoid blocking startup
            setTimeout(async () => {
                await this.performUpdateCheck();
            }, 30000); // 30 seconds delay
        }
        catch (error) {
            console.error('Dakota: Initial scan failed:', error);
        }
    }
    /**
     * Perform security vulnerability check
     */
    async performSecurityCheck() {
        if (!this.isMonitoring) {
            return;
        }
        try {
            const startTime = Date.now();
            console.log('Dakota: Performing background security check');
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (!workspaceFolder) {
                return;
            }
            // Discover dependencies
            const dependencies = await this.discoverDependencies(workspaceFolder.uri.fsPath);
            this.monitoringStats.totalPackagesMonitored = dependencies.length;
            // Check critical dependencies first
            const criticalDependencies = dependencies.slice(0, this.monitoringPolicy.maxConcurrentChecks);
            for (const dep of criticalDependencies) {
                const research = await this.context7.securityResearch(dep.name, dep.version, dep.ecosystem);
                if (research) {
                    this.monitoringStats.context7QueriesExecuted++;
                    await this.processSecurityResearch(dep, research);
                }
            }
            this.monitoringStats.lastSecurityCheck = new Date();
            this.monitoringStats.averageResponseTime = Date.now() - startTime;
        }
        catch (error) {
            console.error('Dakota: Security check failed:', error);
        }
    }
    /**
     * Perform update availability check
     */
    async performUpdateCheck() {
        if (!this.isMonitoring) {
            return;
        }
        try {
            console.log('Dakota: Performing background update check');
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (!workspaceFolder) {
                return;
            }
            // Check for updates (simplified implementation)
            // In a real implementation, this would check package registries
            this.monitoringStats.lastUpdateCheck = new Date();
        }
        catch (error) {
            console.error('Dakota: Update check failed:', error);
        }
    }
    /**
     * Handle dependency file changes
     */
    async handleDependencyFileChange(uri) {
        if (!this.isMonitoring) {
            return;
        }
        try {
            // Debounce rapid changes
            await new Promise(resolve => setTimeout(resolve, 1000));
            console.log(`Dakota: Processing dependency file change: ${path.basename(uri.fsPath)}`);
            // Trigger security check for changed dependencies
            await this.performSecurityCheck();
        }
        catch (error) {
            console.error('Dakota: Failed to handle dependency file change:', error);
        }
    }
    /**
     * Discover dependencies in workspace (simplified)
     */
    async discoverDependencies(workspacePath) {
        const dependencies = [];
        // Check package.json
        const packageJsonPath = path.join(workspacePath, 'package.json');
        if (fs.existsSync(packageJsonPath)) {
            try {
                const content = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
                // Add production dependencies
                if (content.dependencies) {
                    for (const [name, version] of Object.entries(content.dependencies)) {
                        dependencies.push({ name, version: version, ecosystem: 'npm' });
                    }
                }
            }
            catch (error) {
                console.error('Dakota: Failed to parse package.json:', error);
            }
        }
        return dependencies;
    }
    /**
     * Process security research results
     */
    async processSecurityResearch(dependency, research) {
        if (!research.response.success) {
            return;
        }
        // Extract security information from research
        const insights = research.response.insights || [];
        const hasSecurityIssues = insights.some(insight => insight.toLowerCase().includes('vulnerability') ||
            insight.toLowerCase().includes('security') ||
            insight.toLowerCase().includes('cve'));
        if (hasSecurityIssues) {
            const alert = {
                id: `security-${dependency.name}-${Date.now()}`,
                type: 'security',
                severity: this.determineSeverity(insights),
                packageName: dependency.name,
                currentVersion: dependency.version,
                message: `Security vulnerability detected in ${dependency.name}`,
                actionRequired: true,
                timestamp: new Date(),
                context7Research: research
            };
            this.addAlert(alert);
        }
    }
    /**
     * Determine severity from research insights
     */
    determineSeverity(insights) {
        const text = insights.join(' ').toLowerCase();
        if (text.includes('critical') || text.includes('remote code execution')) {
            return 'critical';
        }
        else if (text.includes('high') || text.includes('privilege escalation')) {
            return 'high';
        }
        else if (text.includes('medium') || text.includes('cross-site scripting')) {
            return 'medium';
        }
        else {
            return 'low';
        }
    }
    /**
     * Add alert to active alerts
     */
    addAlert(alert) {
        this.activeAlerts.set(alert.id, alert);
        this.monitoringStats.alertsGenerated++;
        // Show notification if severity meets threshold
        if (this.shouldShowNotification(alert.severity)) {
            this.showAlert(alert);
        }
    }
    /**
     * Check if alert should trigger notification
     */
    shouldShowNotification(severity) {
        const thresholds = { 'critical': 0, 'high': 1, 'medium': 2, 'low': 3 };
        const alertLevel = thresholds[severity];
        const thresholdLevel = thresholds[this.monitoringPolicy.notificationThreshold];
        return alertLevel <= thresholdLevel;
    }
    /**
     * Show alert notification
     */
    async showAlert(alert) {
        const icon = alert.severity === 'critical' ? '🚨' :
            alert.severity === 'high' ? '⚠️' :
                alert.severity === 'medium' ? '📋' : 'ℹ️';
        const message = `${icon} Dakota: ${alert.message}`;
        if (alert.severity === 'critical') {
            await vscode.window.showErrorMessage(message, 'View Details', 'Dismiss');
        }
        else if (alert.severity === 'high') {
            await vscode.window.showWarningMessage(message, 'View Details', 'Dismiss');
        }
        else {
            await vscode.window.showInformationMessage(message, 'View Details', 'Dismiss');
        }
    }
    /**
     * Dispose of monitoring resources
     */
    dispose() {
        this.stopMonitoring();
        this.activeAlerts.clear();
    }
}
exports.DependencyMonitor = DependencyMonitor;
//# sourceMappingURL=DependencyMonitor.js.map