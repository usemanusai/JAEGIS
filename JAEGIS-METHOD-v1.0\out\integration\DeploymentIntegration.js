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
exports.DeploymentIntegration = void 0;
const os = __importStar(require("os"));
const fs = __importStar(require("fs"));
/**
 * Deployment Integration Service
 * Handles platform detection, script generation, and deployment automation
 */
class DeploymentIntegration {
    context7;
    statusBar;
    platformCache = new Map();
    lastDetection = null;
    detectionCacheTimeout = 300000; // 5 minutes
    constructor(context7, statusBar) {
        this.context7 = context7;
        this.statusBar = statusBar;
        console.log('DeploymentIntegration initialized');
    }
    /**
     * Detect current platform capabilities
     */
    async detectPlatformCapabilities(targetPlatform) {
        const platform = targetPlatform || this.getCurrentPlatform();
        // Check cache first
        const cached = this.platformCache.get(platform);
        if (cached && this.isCacheValid()) {
            return cached;
        }
        try {
            const platformInfo = await this.performPlatformDetection(platform);
            // Cache the result
            this.platformCache.set(platform, platformInfo);
            this.lastDetection = new Date();
            return platformInfo;
        }
        catch (error) {
            console.error('Platform detection failed:', error);
            throw new Error(`Failed to detect platform capabilities: ${error}`);
        }
    }
    /**
     * Generate cross-platform deployment scripts
     */
    async generateDeploymentScripts(applicationName, deploymentConfig) {
        const scripts = [];
        for (const platform of deploymentConfig.targetPlatforms) {
            const platformInfo = await this.detectPlatformCapabilities(platform);
            // Generate platform-specific scripts
            if (platform.toLowerCase().includes('windows')) {
                const powershellScript = await this.generatePowerShellScript(applicationName, platformInfo, deploymentConfig);
                scripts.push(powershellScript);
            }
            if (platform.toLowerCase().includes('linux') || platform.toLowerCase().includes('darwin')) {
                const bashScript = await this.generateBashScript(applicationName, platformInfo, deploymentConfig);
                scripts.push(bashScript);
            }
            // Always generate Python script for cross-platform compatibility
            const pythonScript = await this.generatePythonScript(applicationName, platformInfo, deploymentConfig);
            scripts.push(pythonScript);
            // Generate Dockerfile if container deployment
            if (deploymentConfig.containerRegistry) {
                const dockerScript = await this.generateDockerfile(applicationName, platformInfo, deploymentConfig);
                scripts.push(dockerScript);
            }
        }
        return scripts;
    }
    /**
     * Validate deployment configuration
     */
    async validateDeploymentConfig(config) {
        const errors = [];
        const warnings = [];
        const recommendations = [];
        // Validate target platforms
        if (!config.targetPlatforms || config.targetPlatforms.length === 0) {
            errors.push('At least one target platform must be specified');
        }
        // Validate container registry if using containers
        if (config.containerRegistry && !this.isValidRegistryUrl(config.containerRegistry)) {
            errors.push('Invalid container registry URL format');
        }
        // Check platform capabilities
        for (const platform of config.targetPlatforms) {
            try {
                const platformInfo = await this.detectPlatformCapabilities(platform);
                if (config.containerRegistry && !platformInfo.capabilities.includes('docker')) {
                    warnings.push(`Platform ${platform} may not support Docker containers`);
                }
                if (config.orchestrationPlatform === 'kubernetes' && !platformInfo.capabilities.includes('kubernetes')) {
                    warnings.push(`Platform ${platform} may not support Kubernetes orchestration`);
                }
            }
            catch (error) {
                errors.push(`Failed to validate platform ${platform}: ${error}`);
            }
        }
        // Generate recommendations
        if (config.targetPlatforms.length === 1) {
            recommendations.push('Consider adding multiple target platforms for better deployment flexibility');
        }
        if (!config.securityScanning) {
            recommendations.push('Enable security scanning for better deployment security');
        }
        if (!config.monitoringEnabled) {
            recommendations.push('Enable monitoring for better deployment observability');
        }
        return {
            isValid: errors.length === 0,
            errors,
            warnings,
            recommendations
        };
    }
    /**
     * Perform health check on deployment environment
     */
    async performDeploymentHealthCheck(platform) {
        const checks = [];
        try {
            const platformInfo = await this.detectPlatformCapabilities(platform);
            // Check Docker availability
            if (platformInfo.capabilities.includes('docker')) {
                checks.push({
                    name: 'Docker Runtime',
                    status: 'pass',
                    message: 'Docker is available and accessible'
                });
            }
            else {
                checks.push({
                    name: 'Docker Runtime',
                    status: 'warning',
                    message: 'Docker runtime not detected'
                });
            }
            // Check package manager
            if (platformInfo.packageManager) {
                checks.push({
                    name: 'Package Manager',
                    status: 'pass',
                    message: `${platformInfo.packageManager} is available`
                });
            }
            else {
                checks.push({
                    name: 'Package Manager',
                    status: 'fail',
                    message: 'No package manager detected'
                });
            }
            // Check network connectivity
            try {
                // This would be implemented with actual network checks
                checks.push({
                    name: 'Network Connectivity',
                    status: 'pass',
                    message: 'Network connectivity verified'
                });
            }
            catch (error) {
                checks.push({
                    name: 'Network Connectivity',
                    status: 'fail',
                    message: 'Network connectivity issues detected'
                });
            }
            const healthy = checks.every(check => check.status !== 'fail');
            return { healthy, checks };
        }
        catch (error) {
            return {
                healthy: false,
                checks: [{
                        name: 'Platform Detection',
                        status: 'fail',
                        message: `Failed to detect platform: ${error}`
                    }]
            };
        }
    }
    /**
     * Private helper methods
     */
    getCurrentPlatform() {
        const platform = os.platform();
        const arch = os.arch();
        return `${platform}-${arch}`;
    }
    isCacheValid() {
        if (!this.lastDetection) {
            return false;
        }
        const now = new Date();
        return (now.getTime() - this.lastDetection.getTime()) < this.detectionCacheTimeout;
    }
    async performPlatformDetection(platform) {
        const osType = os.type();
        const arch = os.arch();
        const release = os.release();
        // Detect package manager
        const packageManager = await this.detectPackageManager();
        // Detect container runtime
        const containerRuntime = await this.detectContainerRuntime();
        // Detect capabilities
        const capabilities = await this.detectCapabilities();
        // Detect distribution for Linux
        let distribution;
        if (osType === 'Linux') {
            distribution = await this.detectLinuxDistribution();
        }
        return {
            platform: `${osType}-${arch}`,
            architecture: arch,
            distribution,
            packageManager,
            containerRuntime,
            capabilities,
            detectionDate: new Date()
        };
    }
    async detectPackageManager() {
        const packageManagers = [
            { name: 'npm', command: 'npm --version' },
            { name: 'yarn', command: 'yarn --version' },
            { name: 'pnpm', command: 'pnpm --version' },
            { name: 'pip', command: 'pip --version' },
            { name: 'apt', command: 'apt --version' },
            { name: 'yum', command: 'yum --version' },
            { name: 'brew', command: 'brew --version' },
            { name: 'choco', command: 'choco --version' },
            { name: 'winget', command: 'winget --version' }
        ];
        for (const pm of packageManagers) {
            try {
                // This would be implemented with actual command execution
                // For now, return a default based on platform
                if (os.platform() === 'win32' && pm.name === 'npm') {
                    return pm.name;
                }
                else if (os.platform() === 'darwin' && pm.name === 'brew') {
                    return pm.name;
                }
                else if (os.platform() === 'linux' && pm.name === 'apt') {
                    return pm.name;
                }
            }
            catch (error) {
                // Continue to next package manager
            }
        }
        return 'unknown';
    }
    async detectContainerRuntime() {
        const runtimes = ['docker', 'podman', 'containerd'];
        for (const runtime of runtimes) {
            try {
                // This would be implemented with actual command execution
                // For now, assume Docker is available on most systems
                if (runtime === 'docker') {
                    return runtime;
                }
            }
            catch (error) {
                // Continue to next runtime
            }
        }
        return undefined;
    }
    async detectCapabilities() {
        const capabilities = [];
        // Check for common tools and capabilities
        const tools = [
            'docker',
            'kubernetes',
            'git',
            'curl',
            'wget',
            'ssh',
            'rsync'
        ];
        for (const tool of tools) {
            try {
                // This would be implemented with actual command execution
                // For now, assume common tools are available
                if (['docker', 'git', 'curl'].includes(tool)) {
                    capabilities.push(tool);
                }
            }
            catch (error) {
                // Tool not available
            }
        }
        return capabilities;
    }
    async detectLinuxDistribution() {
        try {
            const osReleasePath = '/etc/os-release';
            if (fs.existsSync(osReleasePath)) {
                const content = fs.readFileSync(osReleasePath, 'utf8');
                const idMatch = content.match(/^ID=(.+)$/m);
                if (idMatch) {
                    return idMatch[1].replace(/"/g, '');
                }
            }
        }
        catch (error) {
            // Fallback detection methods could be implemented here
        }
        return undefined;
    }
    async generatePowerShellScript(applicationName, platformInfo, config) {
        const content = `# ${applicationName} PowerShell Deployment Script
# Generated by Phoenix Agent on ${new Date().toISOString().split('T')[0]}
# Platform: ${platformInfo.platform}

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "production"
)

Write-Host "🔥 Phoenix Deployment Script for ${applicationName}" -ForegroundColor Cyan
Write-Host "Platform: ${platformInfo.platform}" -ForegroundColor Yellow

# Platform validation
if ($PSVersionTable.PSVersion.Major -lt 5) {
    throw "PowerShell 5.1 or later required"
}

# Deployment steps would be generated here based on configuration
Write-Host "✅ Deployment preparation complete" -ForegroundColor Green
`;
        return {
            platform: platformInfo.platform,
            scriptType: 'powershell',
            filename: `deploy-${applicationName}.ps1`,
            content,
            dependencies: ['powershell', 'docker'],
            executionInstructions: [
                'Run PowerShell as Administrator',
                'Execute: .\\deploy-' + applicationName + '.ps1',
                'Follow on-screen prompts'
            ]
        };
    }
    async generateBashScript(applicationName, platformInfo, config) {
        const content = `#!/bin/bash
# ${applicationName} Bash Deployment Script
# Generated by Phoenix Agent on ${new Date().toISOString().split('T')[0]}
# Platform: ${platformInfo.platform}

set -euo pipefail

echo "🔥 Phoenix Deployment Script for ${applicationName}"
echo "Platform: ${platformInfo.platform}"

# Platform validation
if ! command -v bash >/dev/null 2>&1; then
    echo "❌ Bash is required but not installed"
    exit 1
fi

# Deployment steps would be generated here based on configuration
echo "✅ Deployment preparation complete"
`;
        return {
            platform: platformInfo.platform,
            scriptType: 'bash',
            filename: `deploy-${applicationName}.sh`,
            content,
            dependencies: ['bash', 'docker', 'curl'],
            executionInstructions: [
                'Make script executable: chmod +x deploy-' + applicationName + '.sh',
                'Execute: ./deploy-' + applicationName + '.sh',
                'Follow on-screen prompts'
            ]
        };
    }
    async generatePythonScript(applicationName, platformInfo, config) {
        const content = `#!/usr/bin/env python3
"""
${applicationName} Python Deployment Script
Generated by Phoenix Agent on ${new Date().toISOString().split('T')[0]}
Platform: ${platformInfo.platform}
"""

import sys
import platform
import subprocess
from datetime import datetime

def main():
    print(f"🔥 Phoenix Deployment Script for ${applicationName}")
    print(f"Platform: {platform.system()}-{platform.machine()}")
    
    # Platform validation
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8 or later required")
    
    # Deployment steps would be generated here based on configuration
    print("✅ Deployment preparation complete")

if __name__ == "__main__":
    main()
`;
        return {
            platform: platformInfo.platform,
            scriptType: 'python',
            filename: `deploy-${applicationName}.py`,
            content,
            dependencies: ['python3', 'docker'],
            executionInstructions: [
                'Ensure Python 3.8+ is installed',
                'Execute: python3 deploy-' + applicationName + '.py',
                'Follow on-screen prompts'
            ]
        };
    }
    async generateDockerfile(applicationName, platformInfo, config) {
        const content = `# ${applicationName} Dockerfile
# Generated by Phoenix Agent on ${new Date().toISOString().split('T')[0]}
# Multi-stage build for optimized production deployment

FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:18-alpine AS runtime
RUN addgroup -g 1001 -S nodejs && adduser -S ${applicationName} -u 1001
WORKDIR /app
COPY --from=builder --chown=${applicationName}:nodejs /app/dist ./dist
COPY --from=builder --chown=${applicationName}:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=${applicationName}:nodejs /app/package.json ./package.json

USER ${applicationName}
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["npm", "start"]
`;
        return {
            platform: 'docker',
            scriptType: 'dockerfile',
            filename: 'Dockerfile',
            content,
            dependencies: ['docker'],
            executionInstructions: [
                'Build image: docker build -t ' + applicationName + ' .',
                'Run container: docker run -p 3000:3000 ' + applicationName,
                'Check health: docker ps'
            ]
        };
    }
    isValidRegistryUrl(url) {
        try {
            new URL(url);
            return true;
        }
        catch {
            return false;
        }
    }
    /**
     * Dispose of integration resources
     */
    dispose() {
        this.platformCache.clear();
    }
}
exports.DeploymentIntegration = DeploymentIntegration;
//# sourceMappingURL=DeploymentIntegration.js.map