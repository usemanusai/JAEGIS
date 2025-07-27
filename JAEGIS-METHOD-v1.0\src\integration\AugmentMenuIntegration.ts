import * as vscode from 'vscode';
import { AugmentExtendedAPI, AugmentMenuItem, AugmentMenuProvider, isAugmentExtendedAPI } from './AugmentAPI';
import { JAEGISOrchestrator } from '../orchestrator/JAEGISOrchestrator';
import { WorkspaceAnalyzer } from '../analysis/WorkspaceAnalyzer';

/**
 * Enhanced menu integration for Augment AI Code extension
 * Provides JAEGIS functionality as menu buttons and context menu items
 */
export class AugmentMenuIntegration {
    private orchestrator: JAEGISOrchestrator;
    private analyzer: WorkspaceAnalyzer;
    private augmentAPI: AugmentExtendedAPI | null = null;

    constructor(orchestrator: JAEGISOrchestrator, analyzer: WorkspaceAnalyzer) {
        this.orchestrator = orchestrator;
        this.analyzer = analyzer;
    }

    /**
     * Initialize menu integration with Augment
     */
    async initialize(augmentAPI: any): Promise<boolean> {
        if (!isAugmentExtendedAPI(augmentAPI)) {
            console.log('Augment API does not support extended menu integration');
            return false;
        }

        this.augmentAPI = augmentAPI;
        await this.registerMenuProvider();
        await this.addContextMenuItems();
        await this.addMainMenuItems();
        
        console.log('JAEGIS menu integration with Augment initialized successfully');
        return true;
    }

    /**
     * Register JAEGIS as a menu provider with Augment
     */
    private async registerMenuProvider(): Promise<void> {
        if (!this.augmentAPI) return;

        const menuProvider: AugmentMenuProvider = {
            id: 'JAEGIS-menu-provider',
            name: 'JAEGIS AI Agent Orchestrator',
            menus: {
                'editor/context': this.getEditorContextMenuItems(),
                'explorer/context': this.getExplorerContextMenuItems(),
                'view/title': this.getViewTitleMenuItems(),
                'commandPalette': this.getCommandPaletteItems()
            }
        };

        await this.augmentAPI.registerMenuProvider(menuProvider);
    }

    /**
     * Add JAEGIS items to Augment's context menus
     */
    private async addContextMenuItems(): Promise<void> {
        if (!this.augmentAPI) return;

        // Add to file explorer context menu
        await this.augmentAPI.addContextMenuItems('explorer/context', [
            {
                id: 'JAEGIS.contextMenu.autoSetup',
                label: 'JAEGIS: Auto Setup Project',
                icon: '$(robot)',
                command: 'JAEGIS.autoSetup',
                when: 'explorerResourceIsFolder',
                group: 'JAEGIS@1'
            },
            {
                id: 'JAEGIS.contextMenu.analyzeProject',
                label: 'JAEGIS: Analyze Project',
                icon: '$(search)',
                command: 'JAEGIS.analyzeProject',
                when: 'explorerResourceIsFolder',
                group: 'JAEGIS@2'
            }
        ]);

        // Add to editor context menu
        await this.augmentAPI.addContextMenuItems('editor/context', [
            {
                id: 'JAEGIS.contextMenu.debugFile',
                label: 'JAEGIS: Debug This File',
                icon: '$(debug)',
                command: 'JAEGIS.debugCurrentFile',
                when: 'editorHasSelection',
                group: 'JAEGIS@1'
            },
            {
                id: 'JAEGIS.contextMenu.documentFile',
                label: 'JAEGIS: Document This File',
                icon: '$(book)',
                command: 'JAEGIS.documentCurrentFile',
                when: 'editorTextFocus',
                group: 'JAEGIS@2'
            }
        ]);
    }

    /**
     * Add JAEGIS items to Augment's main menu
     */
    private async addMainMenuItems(): Promise<void> {
        if (!this.augmentAPI) return;

        const mainMenuItems: AugmentMenuItem[] = [
            {
                id: 'JAEGIS.mainMenu.workflows',
                label: 'JAEGIS Workflows',
                icon: '$(robot)',
                submenu: [
                    {
                        id: 'JAEGIS.mainMenu.documentationMode',
                        label: 'Documentation Mode',
                        icon: '$(book)',
                        command: 'JAEGIS.activateDocumentationMode'
                    },
                    {
                        id: 'JAEGIS.mainMenu.fullDevelopmentMode',
                        label: 'Full Development Mode',
                        icon: '$(rocket)',
                        command: 'JAEGIS.activateFullDevelopmentMode'
                    },
                    {
                        id: 'JAEGIS.mainMenu.debugMode',
                        label: 'Debug & Troubleshoot',
                        icon: '$(debug)',
                        command: 'JAEGIS.debugMode'
                    },
                    {
                        id: 'JAEGIS.mainMenu.separator1',
                        label: '---',
                        command: ''
                    },
                    {
                        id: 'JAEGIS.mainMenu.continueProject',
                        label: 'Continue Project',
                        icon: '$(debug-continue)',
                        command: 'JAEGIS.continueProject'
                    },
                    {
                        id: 'JAEGIS.mainMenu.taskOverview',
                        label: 'Task Overview',
                        icon: '$(list-tree)',
                        command: 'JAEGIS.taskOverview'
                    },
                    {
                        id: 'JAEGIS.mainMenu.separator2',
                        label: '---',
                        command: ''
                    },
                    {
                        id: 'JAEGIS.mainMenu.continuousExecution',
                        label: 'Continuous Execution',
                        icon: '$(sync)',
                        command: 'JAEGIS.continuousExecution'
                    },
                    {
                        id: 'JAEGIS.mainMenu.featureGapAnalysis',
                        label: 'Feature Gap Analysis',
                        icon: '$(search)',
                        command: 'JAEGIS.featureGapAnalysis'
                    },
                    {
                        id: 'JAEGIS.mainMenu.githubIntegration',
                        label: 'GitHub Integration',
                        icon: '$(github)',
                        command: 'JAEGIS.githubIntegration'
                    }
                ]
            },
            {
                id: 'JAEGIS.mainMenu.quickActions',
                label: 'JAEGIS Quick Actions',
                icon: '$(zap)',
                submenu: [
                    {
                        id: 'JAEGIS.mainMenu.quickModeSelect',
                        label: 'Quick Mode Selection',
                        icon: '$(list-selection)',
                        command: 'JAEGIS.quickModeSelect'
                    },
                    {
                        id: 'JAEGIS.mainMenu.autoSetup',
                        label: 'Auto Setup Workspace',
                        icon: '$(gear)',
                        command: 'JAEGIS.autoSetup'
                    },
                    {
                        id: 'JAEGIS.mainMenu.showStatus',
                        label: 'Show Status',
                        icon: '$(info)',
                        command: 'JAEGIS.showStatus'
                    }
                ]
            }
        ];

        await this.augmentAPI.addMainMenuItems(mainMenuItems);
    }

    /**
     * Get editor context menu items
     */
    private getEditorContextMenuItems(): AugmentMenuItem[] {
        return [
            {
                id: 'JAEGIS.editor.debugSelection',
                label: 'Debug Selection with JAEGIS',
                icon: '$(debug)',
                command: 'JAEGIS.debugSelection',
                when: 'editorHasSelection'
            },
            {
                id: 'JAEGIS.editor.explainCode',
                label: 'Explain Code with JAEGIS',
                icon: '$(question)',
                command: 'JAEGIS.explainCode',
                when: 'editorTextFocus'
            },
            {
                id: 'JAEGIS.editor.generateTests',
                label: 'Generate Tests with JAEGIS',
                icon: '$(beaker)',
                command: 'JAEGIS.generateTests',
                when: 'editorTextFocus'
            }
        ];
    }

    /**
     * Get explorer context menu items
     */
    private getExplorerContextMenuItems(): AugmentMenuItem[] {
        return [
            {
                id: 'JAEGIS.explorer.setupProject',
                label: 'Setup with JAEGIS',
                icon: '$(robot)',
                command: 'JAEGIS.autoSetup',
                when: 'explorerResourceIsFolder'
            },
            {
                id: 'JAEGIS.explorer.analyzeFolder',
                label: 'Analyze with JAEGIS',
                icon: '$(search)',
                command: 'JAEGIS.analyzeFolder',
                when: 'explorerResourceIsFolder'
            },
            {
                id: 'JAEGIS.explorer.generateDocs',
                label: 'Generate Documentation',
                icon: '$(book)',
                command: 'JAEGIS.generateDocsForFolder',
                when: 'explorerResourceIsFolder'
            }
        ];
    }

    /**
     * Get view title menu items
     */
    private getViewTitleMenuItems(): AugmentMenuItem[] {
        return [
            {
                id: 'JAEGIS.viewTitle.refresh',
                label: 'Refresh JAEGIS Analysis',
                icon: '$(refresh)',
                command: 'JAEGIS.refreshAnalysis'
            },
            {
                id: 'JAEGIS.viewTitle.settings',
                label: 'JAEGIS Settings',
                icon: '$(settings-gear)',
                command: 'JAEGIS.openSettings'
            }
        ];
    }

    /**
     * Get command palette items
     */
    private getCommandPaletteItems(): AugmentMenuItem[] {
        return [
            {
                id: 'JAEGIS.palette.quickStart',
                label: 'JAEGIS: Quick Start',
                icon: '$(rocket)',
                command: 'JAEGIS.quickModeSelect'
            },
            {
                id: 'JAEGIS.palette.showHelp',
                label: 'JAEGIS: Show Help',
                icon: '$(question)',
                command: 'JAEGIS.showHelp'
            }
        ];
    }

    /**
     * Create a custom JAEGIS panel within Augment
     */
    async showJAEGISPanel(): Promise<void> {
        if (!this.augmentAPI) return;

        const panelContent = {
            title: 'JAEGIS AI Agent Orchestrator',
            type: 'webview',
            content: this.generatePanelHTML(),
            actions: [
                {
                    id: 'documentation-mode',
                    label: 'Documentation Mode',
                    icon: 'book',
                    command: 'JAEGIS.activateDocumentationMode'
                },
                {
                    id: 'full-development-mode',
                    label: 'Full Development',
                    icon: 'rocket',
                    command: 'JAEGIS.activateFullDevelopmentMode'
                },
                {
                    id: 'debug-mode',
                    label: 'Debug & Troubleshoot',
                    icon: 'debug',
                    command: 'JAEGIS.debugMode'
                }
            ]
        };

        await this.augmentAPI.showPanel('JAEGIS-orchestrator', panelContent);
    }

    /**
     * Generate HTML content for JAEGIS panel
     */
    private generatePanelHTML(): string {
        return `
            <div class="JAEGIS-panel">
                <h2>🤖 JAEGIS AI Agent Orchestrator</h2>
                <p>Choose a workflow to get started:</p>
                
                <div class="workflow-grid">
                    <button class="workflow-btn" onclick="executeCommand('JAEGIS.activateDocumentationMode')">
                        <span class="icon">📚</span>
                        <span class="title">Documentation Mode</span>
                        <span class="desc">Generate PRD, Architecture, and Checklist</span>
                    </button>
                    
                    <button class="workflow-btn" onclick="executeCommand('JAEGIS.activateFullDevelopmentMode')">
                        <span class="icon">🚀</span>
                        <span class="title">Full Development</span>
                        <span class="desc">Complete application development</span>
                    </button>
                    
                    <button class="workflow-btn" onclick="executeCommand('JAEGIS.debugMode')">
                        <span class="icon">🐛</span>
                        <span class="title">Debug & Troubleshoot</span>
                        <span class="desc">Systematic issue resolution</span>
                    </button>
                    
                    <button class="workflow-btn" onclick="executeCommand('JAEGIS.continueProject')">
                        <span class="icon">▶️</span>
                        <span class="title">Continue Project</span>
                        <span class="desc">Resume existing work</span>
                    </button>
                </div>
                
                <div class="quick-actions">
                    <button onclick="executeCommand('JAEGIS.quickModeSelect')">Quick Mode Selection</button>
                    <button onclick="executeCommand('JAEGIS.autoSetup')">Auto Setup</button>
                    <button onclick="executeCommand('JAEGIS.showStatus')">Show Status</button>
                </div>
            </div>
            
            <style>
                .JAEGIS-panel { padding: 20px; font-family: var(--vscode-font-family); }
                .workflow-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
                .workflow-btn {
                    padding: 15px; border: 2px solid #8B5CF6;
                    background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%);
                    color: white;
                    border-radius: 8px; cursor: pointer; text-align: left; display: flex; flex-direction: column;
                    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
                    transition: all 0.3s ease;
                }
                .workflow-btn:hover {
                    background: linear-gradient(135deg, #7C3AED 0%, #9333EA 100%);
                    transform: translateY(-2px);
                    box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
                }
                .workflow-btn .icon { font-size: 24px; margin-bottom: 8px; color: #E5E7EB; }
                .workflow-btn .title { font-weight: bold; margin-bottom: 4px; color: white; }
                .workflow-btn .desc { font-size: 12px; opacity: 0.9; color: #E5E7EB; }
                .quick-actions { display: flex; gap: 10px; margin-top: 20px; }
                .quick-actions button {
                    padding: 8px 16px; border: 2px solid #8B5CF6;
                    background: rgba(139, 92, 246, 0.1); color: #8B5CF6;
                    border-radius: 6px; cursor: pointer;
                    transition: all 0.2s ease;
                }
                .quick-actions button:hover {
                    background: #8B5CF6; color: white;
                    transform: translateY(-1px);
                }
            </style>
            
            <script>
                function executeCommand(command) {
                    vscode.postMessage({ command: command });
                }
            </script>
        `;
    }

    /**
     * Dispose of menu integration resources
     */
    dispose(): void {
        this.augmentAPI = null;
    }
}
