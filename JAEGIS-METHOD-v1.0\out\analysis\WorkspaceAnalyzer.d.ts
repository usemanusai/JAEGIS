import * as vscode from 'vscode';
import { ProjectAnalysis, WorkspaceAnalysisResult } from '../types/BMadTypes';
export declare class WorkspaceAnalyzer {
    constructor();
    /**
     * Perform comprehensive workspace analysis
     */
    analyzeWorkspace(workspaceFolder?: vscode.WorkspaceFolder): Promise<WorkspaceAnalysisResult>;
    /**
     * Analyze project characteristics and technology stack
     */
    analyzeProject(workspaceFolder: vscode.WorkspaceFolder): Promise<ProjectAnalysis>;
    /**
     * Check for existing BMAD setup in workspace
     */
    private checkExistingBmadSetup;
    /**
     * Generate intelligent recommendations based on project analysis
     */
    private generateRecommendations;
    /**
     * Generate agent recommendations with reasoning
     */
    private generateAgentRecommendations;
    /**
     * Generate action recommendations
     */
    private generateActionRecommendations;
    private readPackageJson;
    private readRequirementsTxt;
    private readCargoToml;
    private readPomXml;
    private detectDatabase;
    private detectAuthentication;
    private detectFrontend;
    private detectBackend;
    private detectDocker;
    private detectKubernetes;
    private detectTests;
    private detectCICD;
    private calculateComplexity;
    private extractDependencies;
    private extractDevDependencies;
    private recommendMode;
    private recommendAgents;
    private calculateConfidence;
    private determineProjectType;
    private detectFramework;
    private detectLanguage;
}
//# sourceMappingURL=WorkspaceAnalyzer.d.ts.map