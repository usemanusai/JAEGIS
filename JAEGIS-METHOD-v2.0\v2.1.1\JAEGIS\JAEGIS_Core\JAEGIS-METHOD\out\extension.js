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
exports.initializer = exports.configManager = exports.monitor = exports.statusBar = exports.commandManager = exports.analyzer = exports.orchestrator = void 0;
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const JAEGISOrchestrator_1 = require("./orchestrator/JAEGISOrchestrator");
const WorkspaceAnalyzer_1 = require("./analysis/WorkspaceAnalyzer");
const CommandManager_1 = require("./commands/CommandManager");
const StatusBarManager_1 = require("./ui/StatusBarManager");
const WorkspaceMonitor_1 = require("./monitoring/WorkspaceMonitor");
const ConfigurationManager_1 = require("./config/ConfigurationManager");
const JAEGISInitializer_1 = require("./orchestrator/JAEGISInitializer");
const AugmentIntegration_1 = require("./integration/AugmentIntegration");
const AugmentMenuIntegration_1 = require("./integration/AugmentMenuIntegration");
let orchestrator;
let analyzer;
let commandManager;
let statusBar;
let monitor;
let configManager;
let initializer;
let augmentIntegration;
let augmentMenuIntegration;
async function activate(context) {
    console.log('JAEGIS AI Agent Orchestrator is now active!');
    try {
        // Initialize core components
        exports.configManager = configManager = new ConfigurationManager_1.ConfigurationManager();
        exports.analyzer = analyzer = new WorkspaceAnalyzer_1.WorkspaceAnalyzer();
        exports.statusBar = statusBar = new StatusBarManager_1.StatusBarManager();
        exports.initializer = initializer = new JAEGISInitializer_1.JAEGISInitializer(analyzer);
        exports.orchestrator = orchestrator = new JAEGISOrchestrator_1.JAEGISOrchestrator(context, analyzer, statusBar, initializer);
        exports.commandManager = commandManager = new CommandManager_1.CommandManager(orchestrator, analyzer, statusBar);
        exports.monitor = monitor = new WorkspaceMonitor_1.WorkspaceMonitor(analyzer, orchestrator, statusBar);
        // Initialize Augment integration
        augmentIntegration = new AugmentIntegration_1.AugmentIntegration(orchestrator, analyzer, statusBar);
        augmentMenuIntegration = new AugmentMenuIntegration_1.AugmentMenuIntegration(orchestrator, analyzer);
        // Register all commands
        await commandManager.registerCommands(context);
        // Initialize status bar
        statusBar.initialize();
        // Set context for when clauses using modern API
        await vscode.commands.executeCommand('setContext', 'jaegisEnabled', true);
        // Auto-initialize workspace if enabled and workspace folders exist
        const config = configManager.getConfiguration();
        if (config.autoInitialize && vscode.workspace.workspaceFolders) {
            await autoInitializeWorkspaces();
        }
        // Start workspace monitoring if enabled
        if (config.enableRealTimeMonitoring) {
            await monitor.startMonitoring();
        }
        // Initialize Augment integration
        await augmentIntegration.initialize();
        // Show welcome message for first-time users
        await showWelcomeMessage(context);
        console.log('JAEGIS AI Agent Orchestrator activated successfully');
    }
    catch (error) {
        console.error('Failed to activate JAEGIS extension:', error);
        const errorMessage = error instanceof Error ? error.message : String(error);
        await vscode.window.showErrorMessage(`Failed to activate JAEGIS extension: ${errorMessage}`);
    }
}
function deactivate() {
    console.log('JAEGIS AI Agent Orchestrator is now deactivated');
    // Clean up resources in proper order
    try {
        if (monitor) {
            monitor.dispose();
        }
        if (statusBar) {
            statusBar.dispose();
        }
        if (configManager) {
            configManager.dispose();
        }
        if (augmentIntegration) {
            augmentIntegration.dispose();
        }
        if (augmentMenuIntegration) {
            augmentMenuIntegration.dispose();
        }
    }
    catch (error) {
        console.error('Error during deactivation:', error);
    }
}
async function autoInitializeWorkspaces() {
    if (!vscode.workspace.workspaceFolders) {
        return;
    }
    for (const folder of vscode.workspace.workspaceFolders) {
        try {
            const needsInitialization = await initializer.checkIfInitializationNeeded(folder);
            if (needsInitialization) {
                await initializer.initializeWorkspace(folder);
            }
        }
        catch (error) {
            console.error(`Failed to auto-initialize workspace ${folder.name}:`, error);
        }
    }
}
async function showWelcomeMessage(context) {
    const hasShownWelcome = context.globalState.get('jaegis.hasShownWelcome', false);
    if (!hasShownWelcome) {
        const action = await vscode.window.showInformationMessage('Welcome to JAEGIS AI Agent Orchestrator! Would you like to see the quick start guide?', { modal: false }, 'Show Guide', 'Quick Setup', 'Later');
        if (action === 'Show Guide') {
            await vscode.env.openExternal(vscode.Uri.parse('https://github.com/jaegiscode/JAEGIS-METHOD#readme'));
        }
        else if (action === 'Quick Setup') {
            await vscode.commands.executeCommand('jaegis.autoSetup');
        }
        await context.globalState.update('jaegis.hasShownWelcome', true);
    }
}
//# sourceMappingURL=extension.js.map