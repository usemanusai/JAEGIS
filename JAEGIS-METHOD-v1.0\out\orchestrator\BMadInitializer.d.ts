import * as vscode from 'vscode';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
export declare class BMadInitializer {
    private readonly BMAD_FOLDER;
    private analyzer;
    constructor(analyzer: WorkspaceAnalyzer);
    /**
     * Check if workspace needs BMAD initialization
     */
    checkIfInitializationNeeded(workspaceFolder: vscode.WorkspaceFolder): Promise<boolean>;
    /**
     * Initialize BMAD structure in workspace
     */
    initializeWorkspace(workspaceFolder: vscode.WorkspaceFolder): Promise<void>;
    /**
     * Create BMAD folder structure
     */
    private createBmadStructure;
    /**
     * Copy base templates and files
     */
    private copyBaseTemplates;
    /**
     * Create basic persona files
     */
    private createPersonaFiles;
    /**
     * Create basic task files
     */
    private createTaskFiles;
    /**
     * Create template files based on project type
     */
    private createTemplateFiles;
    /**
     * Create checklist files
     */
    private createChecklistFiles;
    /**
     * Create data files
     */
    private createDataFiles;
    /**
     * Generate project-specific configuration
     */
    private generateConfiguration;
    /**
     * Create IDE orchestrator configuration
     */
    private createIdeOrchestratorConfig;
    /**
     * Configure workspace settings
     */
    private configureWorkspaceSettings;
    /**
     * Validate existing BMAD setup
     */
    private validateExistingSetup;
    /**
     * Show initialization success message
     */
    private showInitializationSuccess;
    private getBmadPersonaContent;
    private getPmPersonaContent;
    private getArchitectPersonaContent;
    private getDesignArchitectPersonaContent;
    private getSecurityEngineerPersonaContent;
    private getPlatformEngineerPersonaContent;
    private getTaskBreakdownSpecialistPersonaContent;
    private getTechnicalWriterPersonaContent;
    private getDocumentationModeTaskContent;
    private getContinueProjectTaskContent;
    private getTaskOverviewTaskContent;
    private getDebugTaskContent;
    private getPrdTemplateContent;
    private getArchitectureTemplateContent;
    private getChecklistTemplateContent;
    private getPmChecklistContent;
    private getArchitectChecklistContent;
    private getSecurityChecklistContent;
    private getBmadKnowledgeBaseContent;
    private getIdeOrchestratorConfigContent;
}
//# sourceMappingURL=BMadInitializer.d.ts.map