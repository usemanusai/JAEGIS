import { Context7ResearchResult } from '../integration/Context7Integration';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
import { StatusBarManager } from '../ui/StatusBarManager';
/**
 * Phoenix - System Deployment & Containerization Specialist Agent
 * Handles automated deployment preparation, containerization, and cross-platform setup
 * with seamless Context7 integration for deployment best practices research
 */
export interface DeploymentInfo {
    projectPath: string;
    applicationName: string;
    applicationVersion: string;
    targetPlatforms: string[];
    deploymentType: 'container' | 'native' | 'cloud' | 'hybrid';
    environment: 'development' | 'staging' | 'production';
    containerRegistry?: string;
    orchestrationPlatform?: string;
}
export interface PlatformInfo {
    platform: string;
    architecture: string;
    distribution?: string;
    packageManager: string;
    containerRuntime?: string;
    capabilities: string[];
}
export interface ContainerConfig {
    baseImage: string;
    runtimeImage: string;
    exposedPorts: number[];
    volumes: string[];
    environmentVariables: Record<string, string>;
    healthCheck: string;
    securityContext: SecurityContext;
}
export interface SecurityContext {
    runAsNonRoot: boolean;
    runAsUser?: number;
    readOnlyRootFilesystem: boolean;
    capabilities: {
        drop: string[];
        add: string[];
    };
}
export interface DeploymentScript {
    platform: string;
    scriptType: 'powershell' | 'bash' | 'python';
    content: string;
    dependencies: string[];
    configurationFiles: string[];
}
export interface DeploymentResult {
    projectPath: string;
    timestamp: Date;
    deploymentInfo: DeploymentInfo;
    platformsAnalyzed: PlatformInfo[];
    scriptsGenerated: DeploymentScript[];
    containerConfigs: ContainerConfig[];
    healthScore: number;
    context7Insights: Context7ResearchResult[];
    recommendations: DeploymentRecommendation[];
}
export interface DeploymentRecommendation {
    type: 'security' | 'performance' | 'compatibility' | 'optimization';
    priority: 'critical' | 'high' | 'medium' | 'low';
    title: string;
    description: string;
    actionRequired: boolean;
    context7Research?: Context7ResearchResult;
}
/**
 * Phoenix Agent - System Deployment & Containerization Specialist
 */
export declare class PhoenixAgent {
    private context7;
    private analyzer;
    private statusBar;
    private deploymentIntegration;
    constructor(analyzer: WorkspaceAnalyzer, statusBar: StatusBarManager, context7Config?: any);
    /**
     * Perform comprehensive deployment preparation
     */
    performDeploymentPreparation(projectPath?: string): Promise<DeploymentResult>;
    /**
     * Perform containerization of the application
     */
    performContainerization(deploymentInfo: DeploymentInfo): Promise<void>;
    /**
     * Perform cross-platform setup
     */
    performCrossPlatformSetup(deploymentInfo: DeploymentInfo): Promise<void>;
    /**
     * Analyze deployment requirements from project structure
     */
    private analyzeDeploymentRequirements;
    /**
     * Analyze target platforms and their capabilities
     */
    private analyzePlatforms;
    /**
     * Generate deployment scripts for different platforms
     */
    private generateDeploymentScripts;
    /**
     * Generate container configurations
     */
    private generateContainerConfigs;
    /**
     * Calculate deployment health score
     */
    private calculateDeploymentHealthScore;
    /**
     * Generate deployment recommendations
     */
    private generateDeploymentRecommendations;
    /**
     * Helper methods for script generation
     */
    private generatePowerShellScript;
    private generateBashScript;
    private generatePythonScript;
    /**
     * Helper methods for project analysis
     */
    private detectProjectType;
    private recommendDeploymentType;
    private detectTargetPlatforms;
    private selectBaseImage;
    private selectRuntimeImage;
    /**
     * Generate various deployment artifacts
     */
    private generateDockerfile;
    private generateDockerCompose;
    private generateKubernetesManifests;
    private generatePlatformScript;
    private generateConfigurationTemplates;
    /**
     * Generate comprehensive deployment report
     */
    private generateDeploymentReport;
    /**
     * Get Phoenix agent status
     */
    getStatus(): {
        context7Available: boolean;
        deploymentIntegrationReady: boolean;
        lastDeployment?: Date;
    };
    /**
     * Dispose of agent resources
     */
    dispose(): void;
}
//# sourceMappingURL=PhoenixAgent.d.ts.map