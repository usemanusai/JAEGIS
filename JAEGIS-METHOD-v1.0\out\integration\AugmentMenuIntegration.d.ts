import { BMadOrchestrator } from '../orchestrator/BMadOrchestrator';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
/**
 * Enhanced menu integration for Augment AI Code extension
 * Provides BMAD functionality as menu buttons and context menu items
 */
export declare class AugmentMenuIntegration {
    private orchestrator;
    private analyzer;
    private augmentAPI;
    constructor(orchestrator: BMadOrchestrator, analyzer: WorkspaceAnalyzer);
    /**
     * Initialize menu integration with Augment
     */
    initialize(augmentAPI: any): Promise<boolean>;
    /**
     * Register BMAD as a menu provider with Augment
     */
    private registerMenuProvider;
    /**
     * Add BMAD items to Augment's context menus
     */
    private addContextMenuItems;
    /**
     * Add BMAD items to Augment's main menu
     */
    private addMainMenuItems;
    /**
     * Get editor context menu items
     */
    private getEditorContextMenuItems;
    /**
     * Get explorer context menu items
     */
    private getExplorerContextMenuItems;
    /**
     * Get view title menu items
     */
    private getViewTitleMenuItems;
    /**
     * Get command palette items
     */
    private getCommandPaletteItems;
    /**
     * Create a custom BMAD panel within Augment
     */
    showBmadPanel(): Promise<void>;
    /**
     * Generate HTML content for BMAD panel
     */
    private generatePanelHTML;
    /**
     * Dispose of menu integration resources
     */
    dispose(): void;
}
//# sourceMappingURL=AugmentMenuIntegration.d.ts.map