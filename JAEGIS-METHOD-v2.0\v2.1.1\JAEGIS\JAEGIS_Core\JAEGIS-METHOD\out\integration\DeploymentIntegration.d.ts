import { Context7Integration } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Deployment Integration Module for Phoenix Agent
 * Provides platform detection, deployment automation, and cross-platform compatibility
 * Automatically activates for deployment-related tasks with intelligent platform adaptation
 */
export interface PlatformInfo {
    platform: string;
    architecture: string;
    distribution?: string;
    packageManager: string;
    containerRuntime?: string;
    capabilities: string[];
    detectionDate: Date;
}
export interface DeploymentCapabilities {
    containerSupport: boolean;
    orchestrationSupport: string[];
    packageManagers: string[];
    scriptingSupport: string[];
    cloudProviders: string[];
    monitoringTools: string[];
}
export interface DeploymentConfig {
    targetPlatforms: string[];
    deploymentStrategy: 'blue-green' | 'rolling' | 'canary' | 'recreate';
    containerRegistry?: string;
    orchestrationPlatform?: string;
    monitoringEnabled: boolean;
    securityScanning: boolean;
    autoRollback: boolean;
}
export interface PlatformScript {
    platform: string;
    scriptType: 'powershell' | 'bash' | 'python' | 'dockerfile';
    filename: string;
    content: string;
    dependencies: string[];
    executionInstructions: string[];
}
/**
 * Deployment Integration Service
 * Handles platform detection, script generation, and deployment automation
 */
export declare class DeploymentIntegration {
    private context7;
    private statusBar;
    private platformCache;
    private lastDetection;
    private detectionCacheTimeout;
    constructor(context7: Context7Integration, statusBar: StatusBarManager);
    /**
     * Detect current platform capabilities
     */
    detectPlatformCapabilities(targetPlatform?: string): Promise<PlatformInfo>;
    /**
     * Generate cross-platform deployment scripts
     */
    generateDeploymentScripts(applicationName: string, deploymentConfig: DeploymentConfig): Promise<PlatformScript[]>;
    /**
     * Validate deployment configuration
     */
    validateDeploymentConfig(config: DeploymentConfig): Promise<{
        isValid: boolean;
        errors: string[];
        warnings: string[];
        recommendations: string[];
    }>;
    /**
     * Perform health check on deployment environment
     */
    performDeploymentHealthCheck(platform: string): Promise<{
        healthy: boolean;
        checks: Array<{
            name: string;
            status: 'pass' | 'fail' | 'warning';
            message: string;
        }>;
    }>;
    /**
     * Private helper methods
     */
    private getCurrentPlatform;
    private isCacheValid;
    private performPlatformDetection;
    private detectPackageManager;
    private detectContainerRuntime;
    private detectCapabilities;
    private detectLinuxDistribution;
    private generatePowerShellScript;
    private generateBashScript;
    private generatePythonScript;
    private generateDockerfile;
    private isValidRegistryUrl;
    /**
     * Dispose of integration resources
     */
    dispose(): void;
}
//# sourceMappingURL=DeploymentIntegration.d.ts.map