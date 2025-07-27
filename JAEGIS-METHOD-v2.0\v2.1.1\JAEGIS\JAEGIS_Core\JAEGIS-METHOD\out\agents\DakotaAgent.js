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
exports.DakotaAgent = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const Context7Integration_1 = require("../integration/Context7Integration");
const DependencyMonitor_1 = require("../monitoring/DependencyMonitor");
/**
 * Dakota Agent - Dependency Modernization Specialist
 */
class DakotaAgent {
    context7;
    analyzer;
    statusBar;
    dependencyMonitor;
    isMonitoring = false;
    constructor(analyzer, statusBar, context7Config) {
        this.analyzer = analyzer;
        this.statusBar = statusBar;
        this.context7 = new Context7Integration_1.Context7Integration(context7Config);
        this.dependencyMonitor = new DependencyMonitor_1.DependencyMonitor(this.context7, statusBar);
        console.log('Dakota Agent (Dependency Modernization Specialist) initialized');
    }
    /**
     * Perform comprehensive dependency audit
     */
    async performDependencyAudit(projectPath) {
        const workspacePath = projectPath || vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspacePath) {
            throw new Error('No workspace found for dependency audit');
        }
        this.statusBar.showLoading('Dakota: Analyzing dependencies...');
        try {
            const startTime = Date.now();
            const dependencies = await this.discoverDependencies(workspacePath);
            const context7Insights = [];
            // Perform security analysis with Context7 research
            const vulnerabilities = [];
            for (const dep of dependencies) {
                // Context7 security research
                const securityResearch = await this.context7.securityResearch(dep.name, dep.currentVersion, dep.ecosystem);
                if (securityResearch) {
                    context7Insights.push(securityResearch);
                    // Extract vulnerabilities from research
                    const vulns = this.extractVulnerabilitiesFromResearch(securityResearch);
                    vulnerabilities.push(...vulns);
                }
                // Check for updates and generate recommendations
                const updateRecommendation = await this.generateUpdateRecommendation(dep);
                dep.updateRecommendation = updateRecommendation;
            }
            // Calculate health score
            const healthScore = this.calculateHealthScore(dependencies, vulnerabilities);
            // Generate recommendations
            const recommendations = dependencies
                .filter(dep => dep.updateRecommendation)
                .map(dep => dep.updateRecommendation)
                .sort((a, b) => this.prioritizeRecommendations(a, b));
            const result = {
                projectPath: workspacePath,
                timestamp: new Date(),
                totalDependencies: dependencies.length,
                vulnerabilities,
                outdatedPackages: dependencies.filter(dep => dep.latestVersion && dep.currentVersion !== dep.latestVersion),
                recommendations,
                healthScore,
                context7Insights
            };
            this.statusBar.showSuccess(`Dakota: Audit complete - ${dependencies.length} dependencies analyzed`);
            // Generate and save audit report
            await this.generateAuditReport(result);
            return result;
        }
        catch (error) {
            this.statusBar.showError(`Dakota: Audit failed - ${error}`);
            throw error;
        }
    }
    /**
     * Perform dependency modernization based on audit results
     */
    async performDependencyModernization(auditResult) {
        this.statusBar.showLoading('Dakota: Modernizing dependencies...');
        try {
            const autoUpdates = auditResult.recommendations.filter(rec => rec.action === 'auto-update');
            const manualReviews = auditResult.recommendations.filter(rec => rec.action === 'manual-review');
            // Process automatic updates
            for (const update of autoUpdates) {
                await this.executeAutomaticUpdate(update);
            }
            // Present manual reviews to user
            if (manualReviews.length > 0) {
                await this.presentManualReviews(manualReviews);
            }
            this.statusBar.showSuccess(`Dakota: Modernization complete - ${autoUpdates.length} auto-updates, ${manualReviews.length} manual reviews`);
        }
        catch (error) {
            this.statusBar.showError(`Dakota: Modernization failed - ${error}`);
            throw error;
        }
    }
    /**
     * Start background dependency monitoring
     */
    async startDependencyMonitoring() {
        if (this.isMonitoring) {
            return;
        }
        this.isMonitoring = true;
        await this.dependencyMonitor.startMonitoring();
        this.statusBar.showInfo('Dakota: Background monitoring started');
    }
    /**
     * Stop background dependency monitoring
     */
    stopDependencyMonitoring() {
        this.dependencyMonitor.stopMonitoring();
        this.isMonitoring = false;
        this.statusBar.showInfo('Dakota: Background monitoring stopped');
    }
    /**
     * Discover dependencies in the project
     */
    async discoverDependencies(projectPath) {
        const dependencies = [];
        // Check for different package managers and ecosystems
        const packageManagers = [
            { file: 'package.json', ecosystem: 'npm' },
            { file: 'requirements.txt', ecosystem: 'pip' },
            { file: 'pyproject.toml', ecosystem: 'poetry' },
            { file: 'Cargo.toml', ecosystem: 'cargo' },
            { file: 'go.mod', ecosystem: 'go' },
            { file: 'pom.xml', ecosystem: 'maven' },
            { file: 'build.gradle', ecosystem: 'gradle' },
            { file: 'composer.json', ecosystem: 'composer' },
            { file: 'Gemfile', ecosystem: 'bundler' }
        ];
        for (const pm of packageManagers) {
            const filePath = path.join(projectPath, pm.file);
            if (fs.existsSync(filePath)) {
                const deps = await this.parseDependencyFile(filePath, pm.ecosystem);
                dependencies.push(...deps);
            }
        }
        return dependencies;
    }
    /**
     * Parse dependency file based on ecosystem
     */
    async parseDependencyFile(filePath, ecosystem) {
        const dependencies = [];
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            switch (ecosystem) {
                case 'npm':
                    const packageJson = JSON.parse(content);
                    // Production dependencies
                    if (packageJson.dependencies) {
                        for (const [name, version] of Object.entries(packageJson.dependencies)) {
                            dependencies.push({
                                name,
                                currentVersion: version,
                                type: 'production',
                                ecosystem
                            });
                        }
                    }
                    // Development dependencies
                    if (packageJson.devDependencies) {
                        for (const [name, version] of Object.entries(packageJson.devDependencies)) {
                            dependencies.push({
                                name,
                                currentVersion: version,
                                type: 'development',
                                ecosystem
                            });
                        }
                    }
                    // Peer dependencies
                    if (packageJson.peerDependencies) {
                        for (const [name, version] of Object.entries(packageJson.peerDependencies)) {
                            dependencies.push({
                                name,
                                currentVersion: version,
                                type: 'peer',
                                ecosystem
                            });
                        }
                    }
                    break;
                // Add other ecosystem parsers as needed
                default:
                    console.warn(`Dakota: Unsupported ecosystem ${ecosystem} for file ${filePath}`);
            }
        }
        catch (error) {
            console.error(`Dakota: Failed to parse ${filePath}:`, error);
        }
        return dependencies;
    }
    /**
     * Generate update recommendation for a dependency
     */
    async generateUpdateRecommendation(dependency) {
        // Get latest version information
        const latestVersion = await this.getLatestVersion(dependency);
        dependency.latestVersion = latestVersion;
        // If already up to date
        if (dependency.currentVersion === latestVersion) {
            return {
                action: 'hold',
                reasoning: 'Already at latest version',
                riskLevel: 'low'
            };
        }
        // Context7 research for update strategy
        const updateResearch = await this.context7.updateResearch(dependency.name, dependency.currentVersion, latestVersion || 'latest', dependency.ecosystem);
        // Analyze version difference
        const versionDiff = this.analyzeVersionDifference(dependency.currentVersion, latestVersion || '');
        let action = 'manual-review';
        let riskLevel = 'medium';
        // Determine action based on version difference and research
        if (versionDiff.type === 'patch' && !versionDiff.hasBreakingChanges) {
            action = 'auto-update';
            riskLevel = 'low';
        }
        else if (versionDiff.type === 'minor' && !versionDiff.hasBreakingChanges) {
            action = 'auto-update';
            riskLevel = 'low';
        }
        else if (versionDiff.type === 'major') {
            action = 'manual-review';
            riskLevel = 'high';
        }
        // Override for security vulnerabilities
        if (dependency.vulnerabilities && dependency.vulnerabilities.length > 0) {
            const criticalVulns = dependency.vulnerabilities.filter(v => v.severity === 'critical');
            if (criticalVulns.length > 0) {
                action = 'auto-update';
                riskLevel = 'critical';
            }
        }
        return {
            action,
            targetVersion: latestVersion,
            reasoning: this.generateRecommendationReasoning(dependency, versionDiff, updateResearch),
            riskLevel,
            migrationComplexity: versionDiff.type === 'major' ? 'complex' : 'simple',
            context7Research: updateResearch || undefined
        };
    }
    /**
     * Get latest version for a dependency
     */
    async getLatestVersion(dependency) {
        // This would integrate with package registries
        // For now, return a placeholder
        return undefined;
    }
    /**
     * Analyze version difference between current and target
     */
    analyzeVersionDifference(current, target) {
        // Simplified semantic version analysis
        // In a real implementation, this would use semver library
        return {
            type: 'minor',
            hasBreakingChanges: false
        };
    }
    /**
     * Generate reasoning text for recommendation
     */
    generateRecommendationReasoning(dependency, versionDiff, research) {
        let reasoning = `Update ${dependency.name} from ${dependency.currentVersion} to ${dependency.latestVersion}. `;
        if (research && research.response.success) {
            reasoning += `Context7 research indicates: ${research.response.insights?.join(', ') || 'No specific concerns found'}.`;
        }
        return reasoning;
    }
    /**
     * Extract vulnerabilities from Context7 research
     */
    extractVulnerabilitiesFromResearch(research) {
        // Extract vulnerability information from Context7 response
        // This would parse the research data for vulnerability details
        return [];
    }
    /**
     * Calculate overall health score for dependencies
     */
    calculateHealthScore(dependencies, vulnerabilities) {
        let score = 100;
        // Deduct for vulnerabilities
        const criticalVulns = vulnerabilities.filter(v => v.severity === 'critical').length;
        const highVulns = vulnerabilities.filter(v => v.severity === 'high').length;
        const mediumVulns = vulnerabilities.filter(v => v.severity === 'medium').length;
        score -= (criticalVulns * 20) + (highVulns * 10) + (mediumVulns * 5);
        // Deduct for outdated packages
        const outdated = dependencies.filter(d => d.latestVersion && d.currentVersion !== d.latestVersion).length;
        score -= Math.min(30, outdated * 2);
        return Math.max(0, score);
    }
    /**
     * Prioritize recommendations by risk and impact
     */
    prioritizeRecommendations(a, b) {
        const riskOrder = { 'critical': 0, 'high': 1, 'medium': 2, 'low': 3 };
        return riskOrder[a.riskLevel] - riskOrder[b.riskLevel];
    }
    /**
     * Execute automatic update
     */
    async executeAutomaticUpdate(recommendation) {
        // Implementation would execute the actual update
        console.log(`Dakota: Auto-updating to ${recommendation.targetVersion}`);
    }
    /**
     * Present manual reviews to user
     */
    async presentManualReviews(recommendations) {
        // Implementation would show user interface for manual review
        console.log(`Dakota: ${recommendations.length} updates require manual review`);
    }
    /**
     * Generate comprehensive audit report
     */
    async generateAuditReport(result) {
        // Generate report using the template
        const reportPath = path.join(result.projectPath, 'dependency-audit-report.md');
        // Implementation would generate the actual report file
        console.log(`Dakota: Audit report generated at ${reportPath}`);
    }
    /**
     * Get Dakota agent status
     */
    getStatus() {
        const monitoringStatus = this.dependencyMonitor.getMonitoringStatus();
        return {
            isMonitoring: this.isMonitoring,
            context7Available: this.context7.isIntegrationAvailable(),
            monitoringStats: monitoringStatus.stats
        };
    }
    /**
     * Dispose of agent resources
     */
    dispose() {
        this.stopDependencyMonitoring();
        this.dependencyMonitor.dispose();
        this.context7.dispose();
    }
}
exports.DakotaAgent = DakotaAgent;
//# sourceMappingURL=DakotaAgent.js.map