/**
 * e.J.A.E.G.I.S. VS Code Extension
 * Provides IDE integration for Enhanced Multi-agent Architecture & Dependency Specialist
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn, ChildProcess } from 'child_process';
import WebSocket from 'ws';

interface E-JAEGISNotification {
    timestamp: string;
    task_id: string;
    message: string;
    impact_level: 'low' | 'medium' | 'high' | 'critical';
    suggested_actions: string[];
    affected_component?: string;
    owner?: {
        owner_id: string;
        owner_type: string;
    };
}

interface E-JAEGISStatus {
    isActive: boolean;
    isMonitoring: boolean;
    componentsCount: number;
    lastUpdate: string;
}

class E-JAEGISExtension {
    private context: vscode.ExtensionContext;
    private statusBarItem: vscode.StatusBarItem;
    private eJaegisProcess: ChildProcess | null = null;
    private notificationProvider: E-JAEGISNotificationProvider;
    private dependencyProvider: E-JAEGISDependencyProvider;
    private outputChannel: vscode.OutputChannel;
    private isActive: boolean = false;
    private workspaceRoot: string | undefined;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.outputChannel = vscode.window.createOutputChannel('e.J.A.E.G.I.S. Agent');
        this.workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        
        // Initialize providers
        this.notificationProvider = new E-JAEGISNotificationProvider(this.workspaceRoot);
        this.dependencyProvider = new E-JAEGISDependencyProvider(this.workspaceRoot);
        
        // Create status bar item
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Left,
            100
        );
        this.statusBarItem.command = 'eJaegis.showStatus';
        
        this.initialize();
    }

    private async initialize() {
        // Register commands
        this.registerCommands();
        
        // Register tree data providers
        vscode.window.registerTreeDataProvider('eJaegisNotifications', this.notificationProvider);
        vscode.window.registerTreeDataProvider('eJaegisDependencies', this.dependencyProvider);
        
        // Check if e.J.A.E.G.I.S. is already initialized in workspace
        if (this.workspaceRoot) {
            const eJaegisDir = path.join(this.workspaceRoot, '.eJaegis');
            if (fs.existsSync(eJaegisDir)) {
                this.isActive = true;
                await this.updateStatus();
                
                // Auto-start monitoring if enabled
                const config = vscode.workspace.getConfiguration('eJaegis');
                if (config.get('autoStart', true)) {
                    await this.startMonitoring();
                }
            }
        }
        
        // Set up file watcher for notifications
        this.setupNotificationWatcher();
        
        // Show status bar
        this.statusBarItem.show();
        this.context.subscriptions.push(this.statusBarItem);
    }

    private registerCommands() {
        const commands = [
            vscode.commands.registerCommand('eJaegis.initialize', () => this.initializeE-JAEGIS()),
            vscode.commands.registerCommand('eJaegis.startMonitoring', () => this.startMonitoring()),
            vscode.commands.registerCommand('eJaegis.stopMonitoring', () => this.stopMonitoring()),
            vscode.commands.registerCommand('eJaegis.showStatus', () => this.showStatus()),
            vscode.commands.registerCommand('eJaegis.analyzeFile', () => this.analyzeCurrentFile()),
            vscode.commands.registerCommand('eJaegis.showDependencies', () => this.showDependencies()),
            vscode.commands.registerCommand('eJaegis.configureOwnership', () => this.configureOwnership()),
        ];

        commands.forEach(command => this.context.subscriptions.push(command));
    }

    private async initializeE-JAEGIS() {
        if (!this.workspaceRoot) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        const config = vscode.workspace.getConfiguration('eJaegis');
        const pythonPath = config.get('pythonPath', 'python');
        const neo4jUri = config.get('neo4jUri', 'bolt://localhost:7687');

        try {
            this.outputChannel.appendLine('Initializing e.J.A.E.G.I.S. agent...');
            this.outputChannel.show();

            const result = await this.runE-JAEGISCommand([
                'init',
                '--project-root', this.workspaceRoot,
                '--neo4j-uri', neo4jUri
            ]);

            if (result.success) {
                this.isActive = true;
                await this.updateStatus();
                vscode.window.showInformationMessage('e.J.A.E.G.I.S. initialized successfully!');
                
                // Refresh tree views
                this.notificationProvider.refresh();
                this.dependencyProvider.refresh();
            } else {
                vscode.window.showErrorMessage(`e.J.A.E.G.I.S. initialization failed: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error initializing e.J.A.E.G.I.S.: ${error}`);
        }
    }

    private async startMonitoring() {
        if (!this.isActive) {
            vscode.window.showWarningMessage('e.J.A.E.G.I.S. not initialized. Run "Initialize e.J.A.E.G.I.S." first.');
            return;
        }

        try {
            this.outputChannel.appendLine('Starting e.J.A.E.G.I.S. monitoring...');
            
            const result = await this.runE-JAEGISCommand(['monitor', '--project-root', this.workspaceRoot!]);
            
            if (result.success) {
                await this.updateStatus();
                vscode.window.showInformationMessage('e.J.A.E.G.I.S. monitoring started');
            } else {
                vscode.window.showErrorMessage(`Failed to start monitoring: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error starting monitoring: ${error}`);
        }
    }

    private async stopMonitoring() {
        if (this.eJaegisProcess) {
            this.eJaegisProcess.kill();
            this.eJaegisProcess = null;
        }
        
        await this.updateStatus();
        vscode.window.showInformationMessage('e.J.A.E.G.I.S. monitoring stopped');
    }

    private async showStatus() {
        if (!this.isActive) {
            vscode.window.showInformationMessage('e.J.A.E.G.I.S. not initialized in this workspace');
            return;
        }

        try {
            const result = await this.runE-JAEGISCommand(['status', '--project-root', this.workspaceRoot!]);
            
            if (result.success) {
                // Parse status output and show in a webview or quick pick
                const statusInfo = this.parseStatusOutput(result.output);
                this.showStatusWebview(statusInfo);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error getting status: ${error}`);
        }
    }

    private async analyzeCurrentFile() {
        const activeEditor = vscode.window.activeTextEditor;
        if (!activeEditor) {
            vscode.window.showWarningMessage('No active file to analyze');
            return;
        }

        const filePath = activeEditor.document.uri.fsPath;
        const relativePath = path.relative(this.workspaceRoot!, filePath);

        try {
            this.outputChannel.appendLine(`Analyzing file: ${relativePath}`);
            
            const result = await this.runE-JAEGISCommand([
                'analyze',
                '--project-root', this.workspaceRoot!,
                '--file-path', filePath
            ]);

            if (result.success) {
                this.showAnalysisResults(relativePath, result.output);
            } else {
                vscode.window.showErrorMessage(`Analysis failed: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error analyzing file: ${error}`);
        }
    }

    private async showDependencies() {
        // Refresh and show dependency tree view
        this.dependencyProvider.refresh();
        vscode.commands.executeCommand('workbench.view.explorer');
    }

    private async configureOwnership() {
        if (!this.workspaceRoot) {
            return;
        }

        const ledgerPath = path.join(this.workspaceRoot, 'OWNERSHIP_LEDGER.json');
        
        if (fs.existsSync(ledgerPath)) {
            const document = await vscode.workspace.openTextDocument(ledgerPath);
            await vscode.window.showTextDocument(document);
        } else {
            vscode.window.showErrorMessage('OWNERSHIP_LEDGER.json not found. Initialize e.J.A.E.G.I.S. first.');
        }
    }

    private async runE-JAEGISCommand(args: string[]): Promise<{success: boolean, output: string, error?: string}> {
        return new Promise((resolve) => {
            const config = vscode.workspace.getConfiguration('eJaegis');
            const pythonPath = config.get('pythonPath', 'python');
            
            // Construct command to run e.J.A.E.G.I.S. CLI
            const eJaegisScript = path.join(__dirname, '..', '..', '..', 'cli', 'eJaegis_cli.py');
            const fullArgs = [eJaegisScript, ...args];
            
            const process = spawn(pythonPath, fullArgs, {
                cwd: this.workspaceRoot,
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let output = '';
            let error = '';

            process.stdout?.on('data', (data) => {
                output += data.toString();
                this.outputChannel.append(data.toString());
            });

            process.stderr?.on('data', (data) => {
                error += data.toString();
                this.outputChannel.append(data.toString());
            });

            process.on('close', (code) => {
                resolve({
                    success: code === 0,
                    output,
                    error: code !== 0 ? error : undefined
                });
            });

            process.on('error', (err) => {
                resolve({
                    success: false,
                    output: '',
                    error: err.message
                });
            });
        });
    }

    private setupNotificationWatcher() {
        if (!this.workspaceRoot) {
            return;
        }

        const notificationFile = path.join(this.workspaceRoot, '.eJaegis', 'ide_notifications.json');
        
        if (fs.existsSync(notificationFile)) {
            const watcher = fs.watchFile(notificationFile, () => {
                this.handleNewNotifications();
            });
            
            this.context.subscriptions.push({
                dispose: () => fs.unwatchFile(notificationFile)
            });
        }
    }

    private async handleNewNotifications() {
        if (!this.workspaceRoot) {
            return;
        }

        const notificationFile = path.join(this.workspaceRoot, '.eJaegis', 'ide_notifications.json');
        
        try {
            if (fs.existsSync(notificationFile)) {
                const content = fs.readFileSync(notificationFile, 'utf8');
                const notifications: E-JAEGISNotification[] = JSON.parse(content);
                
                // Show the most recent notification
                if (notifications.length > 0) {
                    const latest = notifications[notifications.length - 1];
                    await this.showNotification(latest);
                }
                
                // Refresh notification tree view
                this.notificationProvider.refresh();
            }
        } catch (error) {
            this.outputChannel.appendLine(`Error reading notifications: ${error}`);
        }
    }

    private async showNotification(notification: E-JAEGISNotification) {
        const config = vscode.workspace.getConfiguration('eJaegis');
        const enableNotifications = config.get('enableNotifications', true);
        const notificationLevel = config.get('notificationLevel', 'medium');
        
        if (!enableNotifications) {
            return;
        }
        
        // Check if notification meets threshold
        const levels = ['low', 'medium', 'high', 'critical'];
        const notificationLevelIndex = levels.indexOf(notification.impact_level);
        const thresholdIndex = levels.indexOf(notificationLevel);
        
        if (notificationLevelIndex < thresholdIndex) {
            return;
        }
        
        // Show notification based on impact level
        const message = `e.J.A.E.G.I.S.: ${notification.message}`;
        const actions = ['View Details', 'Dismiss'];
        
        let showMethod;
        switch (notification.impact_level) {
            case 'critical':
                showMethod = vscode.window.showErrorMessage;
                break;
            case 'high':
                showMethod = vscode.window.showWarningMessage;
                break;
            default:
                showMethod = vscode.window.showInformationMessage;
        }
        
        const result = await showMethod(message, ...actions);
        
        if (result === 'View Details') {
            this.showNotificationDetails(notification);
        }
    }

    private showNotificationDetails(notification: E-JAEGISNotification) {
        const panel = vscode.window.createWebviewPanel(
            'eJaegisNotification',
            'e.J.A.E.G.I.S. Notification Details',
            vscode.ViewColumn.Two,
            { enableScripts: true }
        );

        panel.webview.html = this.getNotificationWebviewContent(notification);
    }

    private getNotificationWebviewContent(notification: E-JAEGISNotification): string {
        return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>e.J.A.E.G.I.S. Notification</title>
            <style>
                body { font-family: var(--vscode-font-family); padding: 20px; }
                .header { border-bottom: 1px solid var(--vscode-panel-border); padding-bottom: 10px; }
                .impact-${notification.impact_level} { 
                    color: ${this.getImpactColor(notification.impact_level)}; 
                    font-weight: bold; 
                }
                .actions { margin-top: 20px; }
                .action-item { 
                    background: var(--vscode-button-background); 
                    color: var(--vscode-button-foreground);
                    padding: 5px 10px; 
                    margin: 5px 0; 
                    border-radius: 3px; 
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>e.J.A.E.G.I.S. Dependency Alert</h2>
                <p><strong>Impact Level:</strong> <span class="impact-${notification.impact_level}">${notification.impact_level.toUpperCase()}</span></p>
                <p><strong>Time:</strong> ${new Date(notification.timestamp).toLocaleString()}</p>
            </div>
            
            <div class="content">
                <h3>Description</h3>
                <p>${notification.message}</p>
                
                ${notification.affected_component ? `
                <h3>Affected Component</h3>
                <p><code>${notification.affected_component}</code></p>
                ` : ''}
                
                ${notification.owner ? `
                <h3>Responsible Owner</h3>
                <p>${notification.owner.owner_id} (${notification.owner.owner_type})</p>
                ` : ''}
                
                <h3>Suggested Actions</h3>
                <div class="actions">
                    ${notification.suggested_actions.map(action => 
                        `<div class="action-item">• ${action}</div>`
                    ).join('')}
                </div>
            </div>
        </body>
        </html>
        `;
    }

    private getImpactColor(level: string): string {
        switch (level) {
            case 'critical': return '#ff4444';
            case 'high': return '#ff8800';
            case 'medium': return '#ffaa00';
            case 'low': return '#00aa00';
            default: return '#888888';
        }
    }

    private parseStatusOutput(output: string): any {
        // Parse e.J.A.E.G.I.S. status output
        // This would parse the actual CLI output format
        return {
            isActive: this.isActive,
            isMonitoring: this.eJaegisProcess !== null,
            output: output
        };
    }

    private showStatusWebview(status: any) {
        const panel = vscode.window.createWebviewPanel(
            'eJaegisStatus',
            'e.J.A.E.G.I.S. Status',
            vscode.ViewColumn.Two,
            { enableScripts: true }
        );

        panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>e.J.A.E.G.I.S. Status</title>
            <style>
                body { font-family: var(--vscode-font-family); padding: 20px; }
                .status-item { margin: 10px 0; }
                .active { color: #00aa00; }
                .inactive { color: #aa0000; }
            </style>
        </head>
        <body>
            <h2>e.J.A.E.G.I.S. Agent Status</h2>
            <div class="status-item">
                <strong>Active:</strong> 
                <span class="${status.isActive ? 'active' : 'inactive'}">
                    ${status.isActive ? 'Yes' : 'No'}
                </span>
            </div>
            <div class="status-item">
                <strong>Monitoring:</strong> 
                <span class="${status.isMonitoring ? 'active' : 'inactive'}">
                    ${status.isMonitoring ? 'Yes' : 'No'}
                </span>
            </div>
            <pre>${status.output}</pre>
        </body>
        </html>
        `;
    }

    private showAnalysisResults(filePath: string, output: string) {
        const panel = vscode.window.createWebviewPanel(
            'eJaegisAnalysis',
            `e.J.A.E.G.I.S. Analysis: ${path.basename(filePath)}`,
            vscode.ViewColumn.Two,
            { enableScripts: true }
        );

        panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>e.J.A.E.G.I.S. Analysis</title>
            <style>
                body { font-family: var(--vscode-font-family); padding: 20px; }
                pre { background: var(--vscode-editor-background); padding: 10px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h2>Dependency Analysis: ${filePath}</h2>
            <pre>${output}</pre>
        </body>
        </html>
        `;
    }

    private async updateStatus() {
        if (this.isActive) {
            this.statusBarItem.text = "$(graph) e.J.A.E.G.I.S. Active";
            this.statusBarItem.tooltip = "e.J.A.E.G.I.S. Agent is monitoring dependencies";
            this.statusBarItem.backgroundColor = undefined;
            
            // Set context for views
            vscode.commands.executeCommand('setContext', 'eJaegis.isActive', true);
        } else {
            this.statusBarItem.text = "$(graph) e.J.A.E.G.I.S. Inactive";
            this.statusBarItem.tooltip = "e.J.A.E.G.I.S. Agent not initialized";
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
            
            vscode.commands.executeCommand('setContext', 'eJaegis.isActive', false);
        }
    }

    dispose() {
        this.statusBarItem.dispose();
        this.outputChannel.dispose();
        if (this.eJaegisProcess) {
            this.eJaegisProcess.kill();
        }
    }
}

class E-JAEGISNotificationProvider implements vscode.TreeDataProvider<E-JAEGISNotification> {
    private _onDidChangeTreeData: vscode.EventEmitter<E-JAEGISNotification | undefined | null | void> = new vscode.EventEmitter<E-JAEGISNotification | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<E-JAEGISNotification | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private workspaceRoot: string | undefined) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: E-JAEGISNotification): vscode.TreeItem {
        const item = new vscode.TreeItem(
            element.message,
            vscode.TreeItemCollapsibleState.None
        );
        
        item.tooltip = `Impact: ${element.impact_level}\nTime: ${element.timestamp}`;
        item.description = element.impact_level;
        
        // Set icon based on impact level
        switch (element.impact_level) {
            case 'critical':
                item.iconPath = new vscode.ThemeIcon('error');
                break;
            case 'high':
                item.iconPath = new vscode.ThemeIcon('warning');
                break;
            case 'medium':
                item.iconPath = new vscode.ThemeIcon('info');
                break;
            case 'low':
                item.iconPath = new vscode.ThemeIcon('check');
                break;
        }
        
        return item;
    }

    getChildren(element?: E-JAEGISNotification): Thenable<E-JAEGISNotification[]> {
        if (!this.workspaceRoot) {
            return Promise.resolve([]);
        }

        const notificationFile = path.join(this.workspaceRoot, '.eJaegis', 'ide_notifications.json');
        
        if (fs.existsSync(notificationFile)) {
            try {
                const content = fs.readFileSync(notificationFile, 'utf8');
                const notifications: E-JAEGISNotification[] = JSON.parse(content);
                return Promise.resolve(notifications.reverse()); // Show newest first
            } catch (error) {
                return Promise.resolve([]);
            }
        }
        
        return Promise.resolve([]);
    }
}

class E-JAEGISDependencyProvider implements vscode.TreeDataProvider<any> {
    private _onDidChangeTreeData: vscode.EventEmitter<any | undefined | null | void> = new vscode.EventEmitter<any | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<any | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private workspaceRoot: string | undefined) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: any): vscode.TreeItem {
        return new vscode.TreeItem(
            element.name,
            element.children ? vscode.TreeItemCollapsibleState.Collapsed : vscode.TreeItemCollapsibleState.None
        );
    }

    getChildren(element?: any): Thenable<any[]> {
        // This would load dependency information from e.J.A.E.G.I.S.
        // For now, return placeholder data
        if (!element) {
            return Promise.resolve([
                { name: 'Loading dependencies...', children: null }
            ]);
        }
        return Promise.resolve([]);
    }
}

export function activate(context: vscode.ExtensionContext) {
    const eJaegisExtension = new E-JAEGISExtension(context);
    context.subscriptions.push(eJaegisExtension);
}

export function deactivate() {
    // Cleanup handled by dispose methods
}
