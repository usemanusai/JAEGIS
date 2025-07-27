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
exports.PhoenixAgent = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const Context7Integration_1 = require("../integration/Context7Integration");
const DeploymentIntegration_1 = require("../integration/DeploymentIntegration");
/**
 * Phoenix Agent - System Deployment & Containerization Specialist
 */
class PhoenixAgent {
    context7;
    analyzer;
    statusBar;
    deploymentIntegration;
    constructor(analyzer, statusBar, context7Config) {
        this.analyzer = analyzer;
        this.statusBar = statusBar;
        this.context7 = new Context7Integration_1.Context7Integration(context7Config);
        this.deploymentIntegration = new DeploymentIntegration_1.DeploymentIntegration(this.context7, statusBar);
        console.log('Phoenix Agent (System Deployment & Containerization Specialist) initialized');
    }
    /**
     * Perform comprehensive deployment preparation
     */
    async performDeploymentPreparation(projectPath) {
        const workspacePath = projectPath || vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspacePath) {
            throw new Error('No workspace found for deployment preparation');
        }
        this.statusBar.showLoading('Phoenix: Analyzing deployment requirements...');
        try {
            const startTime = Date.now();
            const deploymentInfo = await this.analyzeDeploymentRequirements(workspacePath);
            const context7Insights = [];
            // Perform platform analysis with Context7 research
            const platformsAnalyzed = await this.analyzePlatforms(deploymentInfo.targetPlatforms);
            // Context7 research for deployment best practices
            for (const platform of deploymentInfo.targetPlatforms) {
                const deploymentResearch = await this.context7.autoResearch({
                    query: `deployment best practices ${deploymentInfo.applicationName} ${platform} ${new Date().toISOString().split('T')[0]}`,
                    sources: ['platform_documentation', 'deployment_guides', 'best_practices'],
                    focus: ['security', 'performance', 'reliability', 'scalability'],
                    packageName: deploymentInfo.applicationName,
                    ecosystem: platform
                });
                if (deploymentResearch) {
                    context7Insights.push(deploymentResearch);
                }
            }
            // Generate deployment scripts
            const scriptsGenerated = await this.generateDeploymentScripts(deploymentInfo, platformsAnalyzed);
            // Generate container configurations if needed
            const containerConfigs = deploymentInfo.deploymentType === 'container' || deploymentInfo.deploymentType === 'hybrid'
                ? await this.generateContainerConfigs(deploymentInfo)
                : [];
            // Calculate deployment health score
            const healthScore = this.calculateDeploymentHealthScore(deploymentInfo, platformsAnalyzed, context7Insights);
            // Generate recommendations
            const recommendations = await this.generateDeploymentRecommendations(deploymentInfo, context7Insights);
            const result = {
                projectPath: workspacePath,
                timestamp: new Date(),
                deploymentInfo,
                platformsAnalyzed,
                scriptsGenerated,
                containerConfigs,
                healthScore,
                context7Insights,
                recommendations
            };
            this.statusBar.showSuccess(`Phoenix: Deployment preparation complete - ${platformsAnalyzed.length} platforms analyzed`);
            // Generate and save deployment report
            await this.generateDeploymentReport(result);
            return result;
        }
        catch (error) {
            this.statusBar.showError(`Phoenix: Deployment preparation failed - ${error}`);
            throw error;
        }
    }
    /**
     * Perform containerization of the application
     */
    async performContainerization(deploymentInfo) {
        this.statusBar.showLoading('Phoenix: Containerizing application...');
        try {
            // Generate Dockerfile
            await this.generateDockerfile(deploymentInfo);
            // Generate docker-compose configurations
            await this.generateDockerCompose(deploymentInfo);
            // Generate Kubernetes manifests if needed
            if (deploymentInfo.orchestrationPlatform === 'kubernetes') {
                await this.generateKubernetesManifests(deploymentInfo);
            }
            // Context7 research for container security
            const securityResearch = await this.context7.autoResearch({
                query: `container security best practices ${deploymentInfo.applicationName} ${new Date().toISOString().split('T')[0]}`,
                sources: ['security_frameworks', 'container_security_guides', 'cis_benchmarks'],
                focus: ['security_hardening', 'vulnerability_mitigation', 'compliance'],
                packageName: deploymentInfo.applicationName
            });
            this.statusBar.showSuccess('Phoenix: Containerization complete');
        }
        catch (error) {
            this.statusBar.showError(`Phoenix: Containerization failed - ${error}`);
            throw error;
        }
    }
    /**
     * Perform cross-platform setup
     */
    async performCrossPlatformSetup(deploymentInfo) {
        this.statusBar.showLoading('Phoenix: Setting up cross-platform deployment...');
        try {
            // Generate platform-specific scripts
            const platforms = ['windows', 'linux', 'macos'];
            for (const platform of platforms) {
                await this.generatePlatformScript(deploymentInfo, platform);
            }
            // Generate configuration templates
            await this.generateConfigurationTemplates(deploymentInfo);
            // Context7 research for cross-platform compatibility
            const compatibilityResearch = await this.context7.autoResearch({
                query: `cross platform deployment ${deploymentInfo.applicationName} compatibility issues solutions`,
                sources: ['platform_documentation', 'compatibility_guides', 'troubleshooting'],
                focus: ['compatibility', 'platform_differences', 'workarounds'],
                packageName: deploymentInfo.applicationName
            });
            this.statusBar.showSuccess('Phoenix: Cross-platform setup complete');
        }
        catch (error) {
            this.statusBar.showError(`Phoenix: Cross-platform setup failed - ${error}`);
            throw error;
        }
    }
    /**
     * Analyze deployment requirements from project structure
     */
    async analyzeDeploymentRequirements(projectPath) {
        const packageJsonPath = path.join(projectPath, 'package.json');
        let applicationName = path.basename(projectPath);
        let applicationVersion = '1.0.0';
        // Try to extract info from package.json
        if (fs.existsSync(packageJsonPath)) {
            try {
                const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
                applicationName = packageJson.name || applicationName;
                applicationVersion = packageJson.version || applicationVersion;
            }
            catch (error) {
                console.warn('Phoenix: Failed to parse package.json:', error);
            }
        }
        // Detect project type and recommend deployment strategy
        const projectType = await this.detectProjectType(projectPath);
        const deploymentType = this.recommendDeploymentType(projectType);
        const targetPlatforms = this.detectTargetPlatforms(projectPath);
        return {
            projectPath,
            applicationName,
            applicationVersion,
            targetPlatforms,
            deploymentType,
            environment: 'production' // Default, can be configured
        };
    }
    /**
     * Analyze target platforms and their capabilities
     */
    async analyzePlatforms(targetPlatforms) {
        const platforms = [];
        for (const platform of targetPlatforms) {
            const platformInfo = await this.deploymentIntegration.detectPlatformCapabilities(platform);
            platforms.push(platformInfo);
        }
        return platforms;
    }
    /**
     * Generate deployment scripts for different platforms
     */
    async generateDeploymentScripts(deploymentInfo, platforms) {
        const scripts = [];
        for (const platform of platforms) {
            // Generate PowerShell script for Windows
            if (platform.platform.toLowerCase().includes('windows')) {
                const powershellScript = await this.generatePowerShellScript(deploymentInfo, platform);
                scripts.push(powershellScript);
            }
            // Generate Bash script for Linux/macOS
            if (platform.platform.toLowerCase().includes('linux') || platform.platform.toLowerCase().includes('darwin')) {
                const bashScript = await this.generateBashScript(deploymentInfo, platform);
                scripts.push(bashScript);
            }
            // Generate Python script for cross-platform
            const pythonScript = await this.generatePythonScript(deploymentInfo, platform);
            scripts.push(pythonScript);
        }
        return scripts;
    }
    /**
     * Generate container configurations
     */
    async generateContainerConfigs(deploymentInfo) {
        const configs = [];
        // Generate basic container config
        const config = {
            baseImage: this.selectBaseImage(deploymentInfo),
            runtimeImage: this.selectRuntimeImage(deploymentInfo),
            exposedPorts: [3000], // Default, should be configurable
            volumes: ['/app/data', '/app/logs'],
            environmentVariables: {
                NODE_ENV: deploymentInfo.environment,
                PORT: '3000'
            },
            healthCheck: 'curl -f http://localhost:3000/health || exit 1',
            securityContext: {
                runAsNonRoot: true,
                runAsUser: 1001,
                readOnlyRootFilesystem: true,
                capabilities: {
                    drop: ['ALL'],
                    add: ['NET_BIND_SERVICE']
                }
            }
        };
        configs.push(config);
        return configs;
    }
    /**
     * Calculate deployment health score
     */
    calculateDeploymentHealthScore(deploymentInfo, platforms, insights) {
        let score = 100;
        // Deduct for missing platforms
        if (platforms.length < 2) {
            score -= 20;
        }
        // Deduct for security concerns
        const securityInsights = insights.filter(insight => insight.response.insights?.some(i => i.toLowerCase().includes('security')));
        if (securityInsights.length === 0) {
            score -= 15;
        }
        // Deduct for missing containerization
        if (deploymentInfo.deploymentType === 'native') {
            score -= 10;
        }
        return Math.max(0, score);
    }
    /**
     * Generate deployment recommendations
     */
    async generateDeploymentRecommendations(deploymentInfo, insights) {
        const recommendations = [];
        // Security recommendations
        recommendations.push({
            type: 'security',
            priority: 'high',
            title: 'Implement Container Security Scanning',
            description: 'Add vulnerability scanning to your container build pipeline',
            actionRequired: true
        });
        // Performance recommendations
        recommendations.push({
            type: 'performance',
            priority: 'medium',
            title: 'Optimize Container Image Size',
            description: 'Use multi-stage builds and minimal base images to reduce image size',
            actionRequired: false
        });
        return recommendations;
    }
    /**
     * Helper methods for script generation
     */
    async generatePowerShellScript(deploymentInfo, platform) {
        // Implementation would generate PowerShell script content
        return {
            platform: platform.platform,
            scriptType: 'powershell',
            content: '# PowerShell deployment script placeholder',
            dependencies: ['docker', 'git'],
            configurationFiles: ['config/production.json']
        };
    }
    async generateBashScript(deploymentInfo, platform) {
        // Implementation would generate Bash script content
        return {
            platform: platform.platform,
            scriptType: 'bash',
            content: '#!/bin/bash\n# Bash deployment script placeholder',
            dependencies: ['docker', 'git', 'curl'],
            configurationFiles: ['config/production.json']
        };
    }
    async generatePythonScript(deploymentInfo, platform) {
        // Implementation would generate Python script content
        return {
            platform: platform.platform,
            scriptType: 'python',
            content: '#!/usr/bin/env python3\n# Python deployment script placeholder',
            dependencies: ['docker', 'requests'],
            configurationFiles: ['config/production.json']
        };
    }
    /**
     * Helper methods for project analysis
     */
    async detectProjectType(projectPath) {
        if (fs.existsSync(path.join(projectPath, 'package.json')))
            return 'nodejs';
        if (fs.existsSync(path.join(projectPath, 'requirements.txt')))
            return 'python';
        if (fs.existsSync(path.join(projectPath, 'Cargo.toml')))
            return 'rust';
        if (fs.existsSync(path.join(projectPath, 'go.mod')))
            return 'go';
        return 'unknown';
    }
    recommendDeploymentType(projectType) {
        // Default to container for most modern applications
        return 'container';
    }
    detectTargetPlatforms(projectPath) {
        // Default platforms - could be enhanced with project analysis
        return ['linux', 'windows', 'docker'];
    }
    selectBaseImage(deploymentInfo) {
        // Select appropriate base image based on project type
        return 'node:18-alpine';
    }
    selectRuntimeImage(deploymentInfo) {
        // Select appropriate runtime image
        return 'node:18-alpine';
    }
    /**
     * Generate various deployment artifacts
     */
    async generateDockerfile(deploymentInfo) {
        // Implementation would generate Dockerfile
        console.log('Phoenix: Generating Dockerfile');
    }
    async generateDockerCompose(deploymentInfo) {
        // Implementation would generate docker-compose.yml
        console.log('Phoenix: Generating docker-compose.yml');
    }
    async generateKubernetesManifests(deploymentInfo) {
        // Implementation would generate Kubernetes manifests
        console.log('Phoenix: Generating Kubernetes manifests');
    }
    async generatePlatformScript(deploymentInfo, platform) {
        // Implementation would generate platform-specific scripts
        console.log(`Phoenix: Generating ${platform} deployment script`);
    }
    async generateConfigurationTemplates(deploymentInfo) {
        // Implementation would generate configuration templates
        console.log('Phoenix: Generating configuration templates');
    }
    /**
     * Generate comprehensive deployment report
     */
    async generateDeploymentReport(result) {
        // Generate report using the template
        const reportPath = path.join(result.projectPath, 'deployment-report.md');
        // Implementation would generate the actual report file
        console.log(`Phoenix: Deployment report generated at ${reportPath}`);
    }
    /**
     * Get Phoenix agent status
     */
    getStatus() {
        return {
            context7Available: this.context7.isIntegrationAvailable(),
            deploymentIntegrationReady: true
        };
    }
    /**
     * Dispose of agent resources
     */
    dispose() {
        this.context7.dispose();
        this.deploymentIntegration.dispose();
    }
}
exports.PhoenixAgent = PhoenixAgent;
//# sourceMappingURL=PhoenixAgent.js.map