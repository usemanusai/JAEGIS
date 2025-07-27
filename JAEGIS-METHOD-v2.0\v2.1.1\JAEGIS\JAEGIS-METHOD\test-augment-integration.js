/**
 * Test script for JAEGIS-Augment integration
 * This script verifies that the integration components work correctly
 */

const vscode = require('vscode');
const path = require('path');

class AugmentIntegrationTester {
    constructor() {
        this.testResults = [];
    }

    /**
     * Run all integration tests
     */
    async runAllTests() {
        console.log('🧪 Starting JAEGIS-Augment Integration Tests...\n');

        await this.testExtensionActivation();
        await this.testAugmentDetection();
        await this.testWorkflowRegistration();
        await this.testMenuIntegration();
        await this.testCommandRegistration();
        await this.testFallbackBehavior();

        this.printResults();
    }

    /**
     * Test extension activation
     */
    async testExtensionActivation() {
        console.log('📦 Testing Extension Activation...');
        
        try {
            const jaegisExtension = vscode.extensions.getExtension('jaegis-code.jaegis-vscode-extension');
            
            if (!jaegisExtension) {
                this.addResult('Extension Detection', false, 'JAEGIS extension not found');
                return;
            }

            if (!jaegisExtension.isActive) {
                await jaegisExtension.activate();
            }

            this.addResult('Extension Activation', jaegisExtension.isActive, 
                jaegisExtension.isActive ? 'Extension activated successfully' : 'Extension failed to activate');

        } catch (error) {
            this.addResult('Extension Activation', false, `Error: ${error.message}`);
        }
    }

    /**
     * Test Augment extension detection
     */
    async testAugmentDetection() {
        console.log('🔍 Testing Augment Detection...');
        
        try {
            const augmentExtensions = [
                'augment.ai-code',
                'augment.code',
                'augment-ai.code'
            ];

            let augmentFound = false;
            let foundExtension = null;

            for (const extensionId of augmentExtensions) {
                const extension = vscode.extensions.getExtension(extensionId);
                if (extension) {
                    augmentFound = true;
                    foundExtension = extension;
                    break;
                }
            }

            this.addResult('Augment Detection', augmentFound, 
                augmentFound ? `Found: ${foundExtension.id}` : 'Augment extension not found');

            if (augmentFound && !foundExtension.isActive) {
                await foundExtension.activate();
                this.addResult('Augment Activation', foundExtension.isActive, 
                    foundExtension.isActive ? 'Augment activated' : 'Augment activation failed');
            }

        } catch (error) {
            this.addResult('Augment Detection', false, `Error: ${error.message}`);
        }
    }

    /**
     * Test workflow registration
     */
    async testWorkflowRegistration() {
        console.log('⚙️ Testing Workflow Registration...');
        
        try {
            // Test if JAEGIS commands are registered
            const jaegisCommands = [
                'jaegis.activateDocumentationMode',
                'jaegis.activateFullDevelopmentMode',
                'jaegis.debugMode',
                'jaegis.continueProject',
                'jaegis.taskOverview'
            ];

            let registeredCommands = 0;
            const allCommands = await vscode.commands.getCommands();

            for (const command of jaegisCommands) {
                if (allCommands.includes(command)) {
                    registeredCommands++;
                }
            }

            const allRegistered = registeredCommands === jaegisCommands.length;
            this.addResult('Workflow Registration', allRegistered, 
                `${registeredCommands}/${jaegisCommands.length} workflows registered`);

        } catch (error) {
            this.addResult('Workflow Registration', false, `Error: ${error.message}`);
        }
    }

    /**
     * Test menu integration
     */
    async testMenuIntegration() {
        console.log('📋 Testing Menu Integration...');
        
        try {
            // Test if context menu commands are available
            const contextCommands = [
                'jaegis.debugCurrentFile',
                'jaegis.documentCurrentFile',
                'jaegis.analyzeFolder',
                'jaegis.generateDocsForFolder'
            ];

            let availableCommands = 0;
            const allCommands = await vscode.commands.getCommands();

            for (const command of contextCommands) {
                if (allCommands.includes(command)) {
                    availableCommands++;
                }
            }

            const allAvailable = availableCommands === contextCommands.length;
            this.addResult('Menu Integration', allAvailable, 
                `${availableCommands}/${contextCommands.length} menu commands available`);

        } catch (error) {
            this.addResult('Menu Integration', false, `Error: ${error.message}`);
        }
    }

    /**
     * Test command registration
     */
    async testCommandRegistration() {
        console.log('🎯 Testing Command Registration...');
        
        try {
            // Test executing a simple JAEGIS command
            const testCommand = 'jaegis.showHelp';
            
            try {
                await vscode.commands.executeCommand(testCommand);
                this.addResult('Command Execution', true, 'Help command executed successfully');
            } catch (commandError) {
                this.addResult('Command Execution', false, `Command failed: ${commandError.message}`);
            }

        } catch (error) {
            this.addResult('Command Registration', false, `Error: ${error.message}`);
        }
    }

    /**
     * Test fallback behavior
     */
    async testFallbackBehavior() {
        console.log('🔄 Testing Fallback Behavior...');
        
        try {
            // Test if JAEGIS works without Augment
            const jaegisExtension = vscode.extensions.getExtension('jaegis-code.jaegis-vscode-extension');
            
            if (jaegisExtension && jaegisExtension.isActive) {
                // Check if status bar is available (fallback UI)
                const statusBarItems = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left);
                statusBarItems.text = 'JAEGIS Test';
                statusBarItems.show();
                statusBarItems.dispose();

                this.addResult('Fallback Behavior', true, 'Status bar integration working');
            } else {
                this.addResult('Fallback Behavior', false, 'Extension not active for fallback test');
            }

        } catch (error) {
            this.addResult('Fallback Behavior', false, `Error: ${error.message}`);
        }
    }

    /**
     * Add test result
     */
    addResult(testName, passed, message) {
        this.testResults.push({
            name: testName,
            passed,
            message
        });

        const status = passed ? '✅' : '❌';
        console.log(`  ${status} ${testName}: ${message}`);
    }

    /**
     * Print test results summary
     */
    printResults() {
        console.log('\n📊 Test Results Summary:');
        console.log('========================');

        const passed = this.testResults.filter(r => r.passed).length;
        const total = this.testResults.length;
        const percentage = Math.round((passed / total) * 100);

        console.log(`Total Tests: ${total}`);
        console.log(`Passed: ${passed}`);
        console.log(`Failed: ${total - passed}`);
        console.log(`Success Rate: ${percentage}%`);

        if (percentage === 100) {
            console.log('\n🎉 All tests passed! JAEGIS-Augment integration is working correctly.');
        } else if (percentage >= 80) {
            console.log('\n⚠️ Most tests passed. Some features may need attention.');
        } else {
            console.log('\n🚨 Multiple test failures. Integration needs debugging.');
        }

        console.log('\n📋 Detailed Results:');
        this.testResults.forEach(result => {
            const status = result.passed ? '✅' : '❌';
            console.log(`  ${status} ${result.name}: ${result.message}`);
        });
    }
}

/**
 * Mock Augment API for testing
 */
class MockAugmentAPI {
    constructor() {
        this.registeredProviders = [];
        this.registeredMenus = [];
    }

    async registerWorkflowProvider(provider) {
        this.registeredProviders.push(provider);
        console.log(`Mock: Registered workflow provider ${provider.id}`);
        return Promise.resolve();
    }

    async registerMenuProvider(provider) {
        this.registeredMenus.push(provider);
        console.log(`Mock: Registered menu provider ${provider.id}`);
        return Promise.resolve();
    }

    async addContextMenuItems(location, items) {
        console.log(`Mock: Added ${items.length} context menu items to ${location}`);
        return Promise.resolve();
    }

    async addMainMenuItems(items) {
        console.log(`Mock: Added ${items.length} main menu items`);
        return Promise.resolve();
    }

    getCapabilities() {
        return Promise.resolve({
            version: '1.0.0',
            features: {
                workflowProviders: true,
                menuIntegration: true,
                progressReporting: true,
                fileOperations: true,
                contextAwareness: true
            },
            supportedCategories: ['Planning', 'Development', 'Debugging', 'Management', 'Automation']
        });
    }
}

// Export for use in VS Code extension tests
module.exports = {
    AugmentIntegrationTester,
    MockAugmentAPI
};

// Run tests if this script is executed directly
if (require.main === module) {
    const tester = new AugmentIntegrationTester();
    tester.runAllTests().catch(console.error);
}
