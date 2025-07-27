import * as vscode from 'vscode';
import { BMadOrchestrator } from './orchestrator/BMadOrchestrator';
import { WorkspaceAnalyzer } from './analysis/WorkspaceAnalyzer';
import { CommandManager } from './commands/CommandManager';
import { StatusBarManager } from './ui/StatusBarManager';
import { WorkspaceMonitor } from './monitoring/WorkspaceMonitor';
import { ConfigurationManager } from './config/ConfigurationManager';
import { BMadInitializer } from './orchestrator/BMadInitializer';
declare let orchestrator: BMadOrchestrator;
declare let analyzer: WorkspaceAnalyzer;
declare let commandManager: CommandManager;
declare let statusBar: StatusBarManager;
declare let monitor: WorkspaceMonitor;
declare let configManager: ConfigurationManager;
declare let initializer: BMadInitializer;
export declare function activate(context: vscode.ExtensionContext): Promise<void>;
export declare function deactivate(): void;
export { orchestrator, analyzer, commandManager, statusBar, monitor, configManager, initializer };
//# sourceMappingURL=extension.d.ts.map