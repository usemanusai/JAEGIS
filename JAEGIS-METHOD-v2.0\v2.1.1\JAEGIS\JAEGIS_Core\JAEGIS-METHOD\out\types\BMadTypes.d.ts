import * as vscode from 'vscode';
export type JAEGISMode = 'documentation' | 'fullDevelopment' | 'continueProject' | 'taskOverview' | 'debugMode' | 'continuousExecution' | 'featureGapAnalysis' | 'githubIntegration';
export type ProjectType = 'react-frontend' | 'vue-frontend' | 'angular-frontend' | 'nodejs-api' | 'python-api' | 'rust-api' | 'fullstack-web' | 'mobile-app' | 'desktop-app' | 'library' | 'unknown';
export type ComplexityLevel = 'simple' | 'moderate' | 'complex' | 'enterprise';
export type AgentId = 'john' | 'fred' | 'jane' | 'sage' | 'alex' | 'tyler' | 'taylor' | 'sarah' | 'bob' | 'dakota' | 'phoenix' | 'chronos';
export interface ProjectAnalysis {
    type: ProjectType;
    framework: string;
    language: string;
    complexity: ComplexityLevel;
    hasDatabase: boolean;
    hasAuthentication: boolean;
    hasFrontend: boolean;
    hasBackend: boolean;
    hasDocker: boolean;
    hasKubernetes: boolean;
    hasTests: boolean;
    hasCICD: boolean;
    dependencies: string[];
    devDependencies: string[];
    recommendedMode: JAEGISMode;
    recommendedAgents: AgentId[];
    confidence: number;
}
export interface AgentConfig {
    id: AgentId;
    name: string;
    title: string;
    description: string;
    persona: string;
    tasks: string[];
    templates?: string[];
    checklists?: string[];
    specializations: string[];
}
export interface AgentRecommendation {
    agent: AgentConfig;
    reason: string;
    confidence: number;
    required: boolean;
}
export interface AgentSelection {
    required: AgentId[];
    recommended: AgentId[];
    rationale: string;
}
export interface JAEGISConfiguration {
    autoInitialize: boolean;
    defaultMode: JAEGISMode;
    enableRealTimeMonitoring: boolean;
    autoActivateRecommendedAgents: boolean;
    debugModeThreshold: number;
    progressNotifications: boolean;
    intelligentRecommendations: boolean;
    statusBarIntegration: boolean;
}
export interface WorkspaceAnalysisResult {
    projectAnalysis: ProjectAnalysis;
    existingJaegisSetup: boolean;
    jaegisConfigPath?: string;
    needsInitialization: boolean;
    recommendations: {
        mode: JAEGISMode;
        agents: AgentRecommendation[];
        actions: string[];
    };
}
export interface WorkflowProgress {
    mode: JAEGISMode;
    phase: string;
    progress: number;
    currentAgent?: AgentId;
    estimatedTimeRemaining?: number;
    completedTasks: string[];
    remainingTasks: string[];
}
export interface ProjectIssue {
    severity: 'critical' | 'high' | 'medium' | 'low';
    category: 'security' | 'performance' | 'quality' | 'dependency' | 'configuration';
    message: string;
    file?: string;
    line?: number;
    suggestedAction?: string;
    canAutoFix: boolean;
}
export interface ModeExecutionContext {
    mode: JAEGISMode;
    workspaceFolder: vscode.WorkspaceFolder;
    projectAnalysis: ProjectAnalysis;
    selectedAgents: AgentId[];
    userPreferences: Partial<JAEGISConfiguration>;
    existingArtifacts: string[];
}
export interface JAEGISFileStructure {
    jaegisAgentPath: string;
    personasPath: string;
    tasksPath: string;
    templatesPath: string;
    checklistsPath: string;
    dataPath: string;
    configPath: string;
}
export interface TechnologyStack {
    frontend: {
        framework?: string;
        version?: string;
        buildTool?: string;
        packageManager?: string;
    };
    backend: {
        language?: string;
        framework?: string;
        version?: string;
        runtime?: string;
    };
    database: {
        type?: string;
        version?: string;
        orm?: string;
    };
    infrastructure: {
        containerization?: string;
        orchestration?: string;
        cloudProvider?: string;
        cicd?: string;
    };
    testing: {
        unitTesting?: string;
        e2eTesting?: string;
        coverage?: string;
    };
}
export interface CommandResult {
    success: boolean;
    message: string;
    data?: any;
    errors?: string[];
    warnings?: string[];
}
export interface WorkspaceEvent {
    type: 'fileChange' | 'diagnosticChange' | 'configChange' | 'dependencyChange';
    timestamp: Date;
    details: any;
    triggeredActions: string[];
}
export interface AgentHandoffContext {
    fromAgent: AgentId;
    toAgent: AgentId;
    currentTask: string;
    completedWork: string[];
    pendingWork: string[];
    contextData: any;
    handoffReason: string;
}
export interface JAEGISQuickPickItem extends vscode.QuickPickItem {
    id: string;
    data?: any;
}
export interface StatusBarInfo {
    mode?: JAEGISMode;
    activeAgents: AgentId[];
    progress?: WorkflowProgress;
    issues?: ProjectIssue[];
    lastUpdate: Date;
}
export declare class JAEGISError extends Error {
    code: string;
    category: 'initialization' | 'analysis' | 'execution' | 'configuration';
    constructor(message: string, code: string, category?: 'initialization' | 'analysis' | 'execution' | 'configuration');
}
export interface JAEGISEvents {
    'modeActivated': {
        mode: JAEGISMode;
        agents: AgentId[];
    };
    'agentActivated': {
        agent: AgentId;
        context: any;
    };
    'progressUpdated': WorkflowProgress;
    'issueDetected': ProjectIssue[];
    'workspaceAnalyzed': WorkspaceAnalysisResult;
    'configurationChanged': JAEGISConfiguration;
}
//# sourceMappingURL=JAEGISTypes.d.ts.map