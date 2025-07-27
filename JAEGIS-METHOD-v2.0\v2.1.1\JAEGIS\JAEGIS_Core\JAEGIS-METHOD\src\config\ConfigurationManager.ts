import * as vscode from 'vscode';
import { JAEGISConfiguration, JAEGISMode } from '../types/JAEGISTypes';

export class ConfigurationManager {
    private readonly CONFIG_SECTION = 'jaegis';
    private configurationChangeListener?: vscode.Disposable;

    constructor() {
        this.setupConfigurationWatcher();
    }

    /**
     * Get current JAEGIS configuration from VS Code settings
     */
    getConfiguration(): JAEGISConfiguration {
        const config = vscode.workspace.getConfiguration(this.CONFIG_SECTION);
        
        return {
            autoInitialize: config.get('autoInitialize', true),
            defaultMode: config.get('defaultMode', 'documentation') as JAEGISMode,
            enableRealTimeMonitoring: config.get('enableRealTimeMonitoring', true),
            autoActivateRecommendedAgents: config.get('autoActivateRecommendedAgents', true),
            debugModeThreshold: config.get('debugModeThreshold', 5),
            progressNotifications: config.get('progressNotifications', true),
            intelligentRecommendations: config.get('intelligentRecommendations', true),
            statusBarIntegration: config.get('statusBarIntegration', true)
        };
    }

    /**
     * Update JAEGIS configuration in VS Code settings
     */
    async updateConfiguration(updates: Partial<JAEGISConfiguration>, target: vscode.ConfigurationTarget = vscode.ConfigurationTarget.Workspace): Promise<void> {
        const config = vscode.workspace.getConfiguration(this.CONFIG_SECTION);
        
        for (const [key, value] of Object.entries(updates)) {
            await config.update(key, value, target);
        }
    }

    /**
     * Get configuration for a specific key with type safety
     */
    getConfigValue<T>(key: keyof JAEGISConfiguration, defaultValue: T): T {
        const config = vscode.workspace.getConfiguration(this.CONFIG_SECTION);
        return config.get(key, defaultValue);
    }

    /**
     * Set up configuration change watcher
     */
    private setupConfigurationWatcher(): void {
        this.configurationChangeListener = vscode.workspace.onDidChangeConfiguration((event) => {
            if (event.affectsConfiguration(this.CONFIG_SECTION)) {
                this.onConfigurationChanged();
            }
        });
    }

    /**
     * Handle configuration changes
     */
    private onConfigurationChanged(): void {
        const newConfig = this.getConfiguration();
        
        // Emit configuration change event
        vscode.commands.executeCommand('jaegis.internal.configurationChanged', newConfig);
        
        console.log('JAEGIS configuration updated:', newConfig);
    }

    /**
     * Validate configuration values
     */
    validateConfiguration(config: JAEGISConfiguration): { isValid: boolean; errors: string[] } {
        const errors: string[] = [];

        // Validate debug mode threshold
        if (config.debugModeThreshold < 1 || config.debugModeThreshold > 20) {
            errors.push('Debug mode threshold must be between 1 and 20');
        }

        // Validate default mode
        const validModes: JAEGISMode[] = [
            'documentation', 'fullDevelopment', 'continueProject', 'taskOverview',
            'debugMode', 'continuousExecution', 'featureGapAnalysis', 'githubIntegration'
        ];
        
        if (!validModes.includes(config.defaultMode)) {
            errors.push(`Invalid default mode: ${config.defaultMode}`);
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Reset configuration to defaults
     */
    async resetToDefaults(): Promise<void> {
        const defaultConfig: JAEGISConfiguration = {
            autoInitialize: true,
            defaultMode: 'documentation',
            enableRealTimeMonitoring: true,
            autoActivateRecommendedAgents: true,
            debugModeThreshold: 5,
            progressNotifications: true,
            intelligentRecommendations: true,
            statusBarIntegration: true
        };

        await this.updateConfiguration(defaultConfig);
    }

    /**
     * Export configuration for backup or sharing
     */
    exportConfiguration(): string {
        const config = this.getConfiguration();
        return JSON.stringify(config, null, 2);
    }

    /**
     * Import configuration from JSON string
     */
    async importConfiguration(configJson: string): Promise<void> {
        try {
            const config = JSON.parse(configJson) as JAEGISConfiguration;
            const validation = this.validateConfiguration(config);
            
            if (!validation.isValid) {
                throw new Error(`Invalid configuration: ${validation.errors.join(', ')}`);
            }

            await this.updateConfiguration(config);
        } catch (error) {
            throw new Error(`Failed to import configuration: ${error}`);
        }
    }

    /**
     * Get workspace-specific configuration file path
     */
    getWorkspaceConfigPath(): string | undefined {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            return undefined;
        }

        return vscode.Uri.joinPath(workspaceFolder.uri, '.vscode', 'jaegis.json').fsPath;
    }

    /**
     * Save configuration to workspace file
     */
    async saveWorkspaceConfiguration(): Promise<void> {
        const configPath = this.getWorkspaceConfigPath();
        if (!configPath) {
            throw new Error('No workspace folder available');
        }

        const config = this.getConfiguration();
        const configJson = JSON.stringify(config, null, 2);
        const content = new TextEncoder().encode(configJson);

        await vscode.workspace.fs.writeFile(
            vscode.Uri.file(configPath),
            content
        );
    }

    /**
     * Load configuration from workspace file
     */
    async loadWorkspaceConfiguration(): Promise<void> {
        const configPath = this.getWorkspaceConfigPath();
        if (!configPath) {
            return;
        }

        try {
            const configUri = vscode.Uri.file(configPath);
            const configData = await vscode.workspace.fs.readFile(configUri);
            const configJson = new TextDecoder().decode(configData);

            await this.importConfiguration(configJson);
        } catch (error) {
            // Workspace config file doesn't exist or is invalid - use defaults
            console.log('No workspace configuration found, using defaults');
        }
    }

    /**
     * Dispose of resources
     */
    dispose(): void {
        if (this.configurationChangeListener) {
            this.configurationChangeListener.dispose();
        }
    }
}
