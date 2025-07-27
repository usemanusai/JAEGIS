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
            id: 'jaegis-menu-provider',
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
                id: 'jaegis.contextMenu.autoSetup',
                label: 'JAEGIS: Auto Setup Project',
                icon: '$(robot)',
                command: 'jaegis.autoSetup',
                when: 'explorerResourceIsFolder',
                group: 'jaegis@1'
            },
            {
                id: 'jaegis.contextMenu.analyzeProject',
                label: 'JAEGIS: Analyze Project',
                icon: '$(search)',
                command: 'jaegis.analyzeProject',
                when: 'explorerResourceIsFolder',
                group: 'jaegis@2'
            }
        ]);

        // Add to editor context menu
        await this.augmentAPI.addContextMenuItems('editor/context', [
            {
                id: 'jaegis.contextMenu.debugFile',
                label: 'JAEGIS: Debug This File',
                icon: '$(debug)',
                command: 'jaegis.debugCurrentFile',
                when: 'editorHasSelection',
                group: 'jaegis@1'
            },
            {
                id: 'jaegis.contextMenu.documentFile',
                label: 'JAEGIS: Document This File',
                icon: '$(book)',
                command: 'jaegis.documentCurrentFile',
                when: 'editorTextFocus',
                group: 'jaegis@2'
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
                id: 'jaegis.mainMenu.workflows',
                label: 'JAEGIS Workflows',
                icon: '$(robot)',
                submenu: [
                    {
                        id: 'jaegis.mainMenu.documentationMode',
                        label: 'Documentation Mode',
                        icon: '$(book)',
                        command: 'jaegis.activateDocumentationMode'
                    },
                    {
                        id: 'jaegis.mainMenu.fullDevelopmentMode',
                        label: 'Full Development Mode',
                        icon: '$(rocket)',
                        command: 'jaegis.activateFullDevelopmentMode'
                    },
                    {
                        id: 'jaegis.mainMenu.debugMode',
                        label: 'Debug & Troubleshoot',
                        icon: '$(debug)',
                        command: 'jaegis.debugMode'
                    },
                    {
                        id: 'jaegis.mainMenu.separator1',
                        label: '---',
                        command: ''
                    },
                    {
                        id: 'jaegis.mainMenu.continueProject',
                        label: 'Continue Project',
                        icon: '$(debug-continue)',
                        command: 'jaegis.continueProject'
                    },
                    {
                        id: 'jaegis.mainMenu.taskOverview',
                        label: 'Task Overview',
                        icon: '$(list-tree)',
                        command: 'jaegis.taskOverview'
                    },
                    {
                        id: 'jaegis.mainMenu.separator2',
                        label: '---',
                        command: ''
                    },
                    {
                        id: 'jaegis.mainMenu.continuousExecution',
                        label: 'Continuous Execution',
                        icon: '$(sync)',
                        command: 'jaegis.continuousExecution'
                    },
                    {
                        id: 'jaegis.mainMenu.featureGapAnalysis',
                        label: 'Feature Gap Analysis',
                        icon: '$(search)',
                        command: 'jaegis.featureGapAnalysis'
                    },
                    {
                        id: 'jaegis.mainMenu.githubIntegration',
                        label: 'GitHub Integration',
                        icon: '$(github)',
                        command: 'jaegis.githubIntegration'
                    }
                ]
            },
            {
                id: 'jaegis.mainMenu.quickActions',
                label: 'JAEGIS Quick Actions',
                icon: '$(zap)',
                submenu: [
                    {
                        id: 'jaegis.mainMenu.quickModeSelect',
                        label: 'Quick Mode Selection',
                        icon: '$(list-selection)',
                        command: 'jaegis.quickModeSelect'
                    },
                    {
                        id: 'jaegis.mainMenu.autoSetup',
                        label: 'Auto Setup Workspace',
                        icon: '$(gear)',
                        command: 'jaegis.autoSetup'
                    },
                    {
                        id: 'jaegis.mainMenu.showStatus',
                        label: 'Show Status',
                        icon: '$(info)',
                        command: 'jaegis.showStatus'
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
                id: 'jaegis.editor.debugSelection',
                label: 'Debug Selection with JAEGIS',
                icon: '$(debug)',
                command: 'jaegis.debugSelection',
                when: 'editorHasSelection'
            },
            {
                id: 'jaegis.editor.explainCode',
                label: 'Explain Code with JAEGIS',
                icon: '$(question)',
                command: 'jaegis.explainCode',
                when: 'editorTextFocus'
            },
            {
                id: 'jaegis.editor.generateTests',
                label: 'Generate Tests with JAEGIS',
                icon: '$(beaker)',
                command: 'jaegis.generateTests',
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
                id: 'jaegis.explorer.setupProject',
                label: 'Setup with JAEGIS',
                icon: '$(robot)',
                command: 'jaegis.autoSetup',
                when: 'explorerResourceIsFolder'
            },
            {
                id: 'jaegis.explorer.analyzeFolder',
                label: 'Analyze with JAEGIS',
                icon: '$(search)',
                command: 'jaegis.analyzeFolder',
                when: 'explorerResourceIsFolder'
            },
            {
                id: 'jaegis.explorer.generateDocs',
                label: 'Generate Documentation',
                icon: '$(book)',
                command: 'jaegis.generateDocsForFolder',
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
                id: 'jaegis.viewTitle.refresh',
                label: 'Refresh JAEGIS Analysis',
                icon: '$(refresh)',
                command: 'jaegis.refreshAnalysis'
            },
            {
                id: 'jaegis.viewTitle.settings',
                label: 'JAEGIS Settings',
                icon: '$(settings-gear)',
                command: 'jaegis.openSettings'
            }
        ];
    }

    /**
     * Get command palette items
     */
    private getCommandPaletteItems(): AugmentMenuItem[] {
        return [
            {
                id: 'jaegis.palette.quickStart',
                label: 'JAEGIS: Quick Start',
                icon: '$(rocket)',
                command: 'jaegis.quickModeSelect'
            },
            {
                id: 'jaegis.palette.showHelp',
                label: 'JAEGIS: Show Help',
                icon: '$(question)',
                command: 'jaegis.showHelp'
            }
        ];
    }

    /**
     * Create a custom JAEGIS panel within Augment
     */
    async showJaegisPanel(): Promise<void> {
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
                    command: 'jaegis.activateDocumentationMode'
                },
                {
                    id: 'full-development-mode',
                    label: 'Full Development',
                    icon: 'rocket',
                    command: 'jaegis.activateFullDevelopmentMode'
                },
                {
                    id: 'debug-mode',
                    label: 'Debug & Troubleshoot',
                    icon: 'debug',
                    command: 'jaegis.debugMode'
                }
            ]
        };

        await this.augmentAPI.showPanel('jaegis-orchestrator', panelContent);
    }

    /**
     * Generate HTML content for JAEGIS panel
     */
    private generatePanelHTML(): string {
        return `
            <div class="jaegis-panel">
                <h2>🤖 JAEGIS AI Agent Orchestrator</h2>
                <p>Choose a workflow to get started:</p>
                
                <div class="workflow-grid">
                    <button class="workflow-btn" onclick="executeCommand('jaegis.activateDocumentationMode')">
                        <span class="icon">📚</span>
                        <span class="title">Documentation Mode</span>
                        <span class="desc">Generate PRD, Architecture, and Checklist</span>
                    </button>
                    
                    <button class="workflow-btn" onclick="executeCommand('jaegis.activateFullDevelopmentMode')">
                        <span class="icon">🚀</span>
                        <span class="title">Full Development</span>
                        <span class="desc">Complete application development</span>
                    </button>
                    
                    <button class="workflow-btn" onclick="executeCommand('jaegis.debugMode')">
                        <span class="icon">🐛</span>
                        <span class="title">Debug & Troubleshoot</span>
                        <span class="desc">Systematic issue resolution</span>
                    </button>
                    
                    <button class="workflow-btn" onclick="executeCommand('jaegis.continueProject')">
                        <span class="icon">▶️</span>
                        <span class="title">Continue Project</span>
                        <span class="desc">Resume existing work</span>
                    </button>
                </div>
                
                <div class="quick-actions">
                    <button onclick="executeCommand('jaegis.quickModeSelect')">Quick Mode Selection</button>
                    <button onclick="executeCommand('jaegis.autoSetup')">Auto Setup</button>
                    <button onclick="executeCommand('jaegis.showStatus')">Show Status</button>
                </div>
            </div>
            
            <style>
                .jaegis-panel { padding: 20px; font-family: var(--vscode-font-family); }
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
