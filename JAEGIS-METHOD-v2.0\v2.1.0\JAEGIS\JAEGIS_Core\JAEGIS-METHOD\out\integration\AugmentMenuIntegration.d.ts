import { JAEGISOrchestrator } from '../orchestrator/JAEGISOrchestrator';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';
/**
 * Enhanced menu integration for Augment AI Code extension
 * Provides JAEGIS functionality as menu buttons and context menu items
 */
export declare class AugmentMenuIntegration {
    private orchestrator;
    private analyzer;
    private augmentAPI;
    constructor(orchestrator: JAEGISOrchestrator, analyzer: WorkspaceAnalyzer);
    /**
     * Initialize menu integration with Augment
     */
    initialize(augmentAPI: any): Promise<boolean>;
    /**
     * Register JAEGIS as a menu provider with Augment
     */
    private registerMenuProvider;
    /**
     * Add JAEGIS items to Augment's context menus
     */
    private addContextMenuItems;
    /**
     * Add JAEGIS items to Augment's main menu
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
     * Create a custom JAEGIS panel within Augment
     */
    showJaegisPanel(): Promise<void>;
    /**
     * Generate HTML content for JAEGIS panel
     */
    private generatePanelHTML;
    /**
     * Dispose of menu integration resources
     */
    dispose(): void;
}
//# sourceMappingURL=AugmentMenuIntegration.d.ts.map