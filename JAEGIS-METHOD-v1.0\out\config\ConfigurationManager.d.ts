import * as vscode from 'vscode';
import { BMadConfiguration } from '../types/BMadTypes';
export declare class ConfigurationManager {
    private readonly CONFIG_SECTION;
    private configurationChangeListener?;
    constructor();
    /**
     * Get current BMAD configuration from VS Code settings
     */
    getConfiguration(): BMadConfiguration;
    /**
     * Update BMAD configuration in VS Code settings
     */
    updateConfiguration(updates: Partial<BMadConfiguration>, target?: vscode.ConfigurationTarget): Promise<void>;
    /**
     * Get configuration for a specific key with type safety
     */
    getConfigValue<T>(key: keyof BMadConfiguration, defaultValue: T): T;
    /**
     * Set up configuration change watcher
     */
    private setupConfigurationWatcher;
    /**
     * Handle configuration changes
     */
    private onConfigurationChanged;
    /**
     * Validate configuration values
     */
    validateConfiguration(config: BMadConfiguration): {
        isValid: boolean;
        errors: string[];
    };
    /**
     * Reset configuration to defaults
     */
    resetToDefaults(): Promise<void>;
    /**
     * Export configuration for backup or sharing
     */
    exportConfiguration(): string;
    /**
     * Import configuration from JSON string
     */
    importConfiguration(configJson: string): Promise<void>;
    /**
     * Get workspace-specific configuration file path
     */
    getWorkspaceConfigPath(): string | undefined;
    /**
     * Save configuration to workspace file
     */
    saveWorkspaceConfiguration(): Promise<void>;
    /**
     * Load configuration from workspace file
     */
    loadWorkspaceConfiguration(): Promise<void>;
    /**
     * Dispose of resources
     */
    dispose(): void;
}
//# sourceMappingURL=ConfigurationManager.d.ts.map