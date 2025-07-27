"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConfigurationManager = void 0;
const vscode = __importStar(require("vscode"));
class ConfigurationManager {
    CONFIG_SECTION = 'bmad';
    configurationChangeListener;
    constructor() {
        this.setupConfigurationWatcher();
    }
    /**
     * Get current BMAD configuration from VS Code settings
     */
    getConfiguration() {
        const config = vscode.workspace.getConfiguration(this.CONFIG_SECTION);
        return {
            autoInitialize: config.get('autoInitialize', true),
            defaultMode: config.get('defaultMode', 'documentation'),
            enableRealTimeMonitoring: config.get('enableRealTimeMonitoring', true),
            autoActivateRecommendedAgents: config.get('autoActivateRecommendedAgents', true),
            debugModeThreshold: config.get('debugModeThreshold', 5),
            progressNotifications: config.get('progressNotifications', true),
            intelligentRecommendations: config.get('intelligentRecommendations', true),
            statusBarIntegration: config.get('statusBarIntegration', true)
        };
    }
    /**
     * Update BMAD configuration in VS Code settings
     */
    async updateConfiguration(updates, target = vscode.ConfigurationTarget.Workspace) {
        const config = vscode.workspace.getConfiguration(this.CONFIG_SECTION);
        for (const [key, value] of Object.entries(updates)) {
            await config.update(key, value, target);
        }
    }
    /**
     * Get configuration for a specific key with type safety
     */
    getConfigValue(key, defaultValue) {
        const config = vscode.workspace.getConfiguration(this.CONFIG_SECTION);
        return config.get(key, defaultValue);
    }
    /**
     * Set up configuration change watcher
     */
    setupConfigurationWatcher() {
        this.configurationChangeListener = vscode.workspace.onDidChangeConfiguration((event) => {
            if (event.affectsConfiguration(this.CONFIG_SECTION)) {
                this.onConfigurationChanged();
            }
        });
    }
    /**
     * Handle configuration changes
     */
    onConfigurationChanged() {
        const newConfig = this.getConfiguration();
        // Emit configuration change event
        vscode.commands.executeCommand('bmad.internal.configurationChanged', newConfig);
        console.log('BMAD configuration updated:', newConfig);
    }
    /**
     * Validate configuration values
     */
    validateConfiguration(config) {
        const errors = [];
        // Validate debug mode threshold
        if (config.debugModeThreshold < 1 || config.debugModeThreshold > 20) {
            errors.push('Debug mode threshold must be between 1 and 20');
        }
        // Validate default mode
        const validModes = [
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
    async resetToDefaults() {
        const defaultConfig = {
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
    exportConfiguration() {
        const config = this.getConfiguration();
        return JSON.stringify(config, null, 2);
    }
    /**
     * Import configuration from JSON string
     */
    async importConfiguration(configJson) {
        try {
            const config = JSON.parse(configJson);
            const validation = this.validateConfiguration(config);
            if (!validation.isValid) {
                throw new Error(`Invalid configuration: ${validation.errors.join(', ')}`);
            }
            await this.updateConfiguration(config);
        }
        catch (error) {
            throw new Error(`Failed to import configuration: ${error}`);
        }
    }
    /**
     * Get workspace-specific configuration file path
     */
    getWorkspaceConfigPath() {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            return undefined;
        }
        return vscode.Uri.joinPath(workspaceFolder.uri, '.vscode', 'bmad.json').fsPath;
    }
    /**
     * Save configuration to workspace file
     */
    async saveWorkspaceConfiguration() {
        const configPath = this.getWorkspaceConfigPath();
        if (!configPath) {
            throw new Error('No workspace folder available');
        }
        const config = this.getConfiguration();
        const configJson = JSON.stringify(config, null, 2);
        const content = new TextEncoder().encode(configJson);
        await vscode.workspace.fs.writeFile(vscode.Uri.file(configPath), content);
    }
    /**
     * Load configuration from workspace file
     */
    async loadWorkspaceConfiguration() {
        const configPath = this.getWorkspaceConfigPath();
        if (!configPath) {
            return;
        }
        try {
            const configUri = vscode.Uri.file(configPath);
            const configData = await vscode.workspace.fs.readFile(configUri);
            const configJson = new TextDecoder().decode(configData);
            await this.importConfiguration(configJson);
        }
        catch (error) {
            // Workspace config file doesn't exist or is invalid - use defaults
            console.log('No workspace configuration found, using defaults');
        }
    }
    /**
     * Dispose of resources
     */
    dispose() {
        if (this.configurationChangeListener) {
            this.configurationChangeListener.dispose();
        }
    }
}
exports.ConfigurationManager = ConfigurationManager;
//# sourceMappingURL=ConfigurationManager.js.map