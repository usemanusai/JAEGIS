import * as vscode from 'vscode';
import { JAEGISOrchestrator } from './orchestrator/JAEGISOrchestrator';
import { WorkspaceAnalyzer } from './analysis/WorkspaceAnalyzer';
import { CommandManager } from './commands/CommandManager';
import { StatusBarManager } from './ui/StatusBarManager';
import { WorkspaceMonitor } from './monitoring/WorkspaceMonitor';
import { ConfigurationManager } from './config/ConfigurationManager';
import { JAEGISInitializer } from './orchestrator/JAEGISInitializer';
declare let orchestrator: JAEGISOrchestrator;
declare let analyzer: WorkspaceAnalyzer;
declare let commandManager: CommandManager;
declare let statusBar: StatusBarManager;
declare let monitor: WorkspaceMonitor;
declare let configManager: ConfigurationManager;
declare let initializer: JAEGISInitializer;
export declare function activate(context: vscode.ExtensionContext): Promise<void>;
export declare function deactivate(): void;
export { orchestrator, analyzer, commandManager, statusBar, monitor, configManager, initializer };
//# sourceMappingURL=extension.d.ts.map