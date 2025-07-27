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
exports.AgentCoordinator = void 0;
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
class AgentCoordinator {
    sharedContext;
    agentConfigs = new Map();
    activeAgent = null;
    handoffQueue = [];
    constructor() {
        this.sharedContext = {
            projectInfo: {},
            currentPhase: 'initialization',
            activeAgents: [],
            handoffQueue: [],
            validationResults: {},
            dependencyStatus: {},
            researchCache: {},
            decisions: [],
            knowledgeBase: {}
        };
    }
    /**
     * Initialize the agent coordination system
     */
    async initialize(workspaceRoot) {
        try {
            await this.loadAgentConfiguration(workspaceRoot);
            this.updateSharedContext('currentPhase', 'initialized');
            console.log('Agent Coordinator initialized successfully');
        }
        catch (error) {
            console.error('Failed to initialize Agent Coordinator:', error);
            throw error;
        }
    }
    /**
     * Load agent configuration from standardized config file
     */
    async loadAgentConfiguration(workspaceRoot) {
        const configPath = path.join(workspaceRoot, 'bmad-agent', 'agent-config.txt');
        if (!fs.existsSync(configPath)) {
            throw new Error('Agent configuration file not found: ' + configPath);
        }
        const configContent = fs.readFileSync(configPath, 'utf8');
        this.parseAgentConfiguration(configContent);
    }
    /**
     * Parse the standardized agent configuration format
     */
    parseAgentConfiguration(content) {
        const sections = content.split('==================== START:');
        for (const section of sections) {
            if (section.trim() === '')
                continue;
            const lines = section.split('\n');
            const sectionName = lines[0].split('====================')[0].trim();
            if (sectionName === 'CONFIGURATION') {
                // Parse configuration section
                continue;
            }
            // Parse agent sections
            const agentConfig = this.parseAgentSection(lines);
            if (agentConfig) {
                this.agentConfigs.set(sectionName, agentConfig);
            }
        }
    }
    /**
     * Parse individual agent section
     */
    parseAgentSection(lines) {
        const config = {};
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed.startsWith('Title:')) {
                config.title = trimmed.substring(6).trim();
            }
            else if (trimmed.startsWith('Name:')) {
                config.name = trimmed.substring(5).trim();
            }
            else if (trimmed.startsWith('Description:')) {
                config.description = trimmed.substring(12).trim();
            }
            else if (trimmed.startsWith('Persona:')) {
                config.persona = trimmed.substring(8).trim();
            }
            else if (trimmed.startsWith('Coordination:')) {
                config.coordination = trimmed.substring(13).trim();
            }
            else if (trimmed.startsWith('Priority:')) {
                config.priority = parseInt(trimmed.substring(9).trim());
            }
            // Parse tasks, handoff-from, handoff-to, validation arrays
        }
        if (config.title && config.name) {
            return config;
        }
        return null;
    }
    /**
     * Activate an agent with proper coordination
     */
    async activateAgent(agentId, taskId) {
        const agentConfig = this.agentConfigs.get(agentId);
        if (!agentConfig) {
            throw new Error(`Agent not found: ${agentId}`);
        }
        // Validate handoff requirements
        if (agentConfig.handoffFrom && agentConfig.handoffFrom.length > 0) {
            const hasValidHandoff = agentConfig.handoffFrom.some(fromAgent => this.sharedContext.activeAgents.includes(fromAgent));
            if (!hasValidHandoff) {
                throw new Error(`Agent ${agentId} requires handoff from: ${agentConfig.handoffFrom.join(', ')}`);
            }
        }
        // Perform pre-activation validation
        await this.performPreActivationValidation(agentId);
        // Update shared context
        this.activeAgent = agentId;
        this.sharedContext.activeAgents.push(agentId);
        this.updateSharedContext('currentPhase', `active-${agentId}`);
        console.log(`Agent activated: ${agentConfig.title} (${agentConfig.name})`);
    }
    /**
     * Perform agent handoff with context preservation
     */
    async performHandoff(fromAgent, toAgent) {
        const fromConfig = this.agentConfigs.get(fromAgent);
        const toConfig = this.agentConfigs.get(toAgent);
        if (!fromConfig || !toConfig) {
            throw new Error('Invalid agent handoff configuration');
        }
        // Validate handoff is allowed
        if (fromConfig.handoffTo && !fromConfig.handoffTo.includes(toAgent)) {
            throw new Error(`Agent ${fromAgent} cannot handoff to ${toAgent}`);
        }
        // Perform pre-handoff validation
        await this.performPreHandoffValidation(fromAgent);
        // Transfer context
        await this.transferContext(fromAgent, toAgent);
        // Update active agent
        this.activeAgent = toAgent;
        this.sharedContext.activeAgents = this.sharedContext.activeAgents.filter(a => a !== fromAgent);
        this.sharedContext.activeAgents.push(toAgent);
        // Perform post-handoff validation
        await this.performPostHandoffValidation(toAgent);
        console.log(`Handoff completed: ${fromAgent} → ${toAgent}`);
    }
    /**
     * Update shared context
     */
    updateSharedContext(key, value) {
        this.sharedContext[key] = value;
        this.notifyContextUpdate(key, value);
    }
    /**
     * Get shared context
     */
    getSharedContext() {
        return { ...this.sharedContext };
    }
    /**
     * Get available agents
     */
    getAvailableAgents() {
        return Array.from(this.agentConfigs.values());
    }
    /**
     * Get current active agent
     */
    getActiveAgent() {
        return this.activeAgent;
    }
    /**
     * Perform pre-activation validation
     */
    async performPreActivationValidation(agentId) {
        // Implement validation logic
        console.log(`Pre-activation validation for ${agentId}`);
    }
    /**
     * Perform pre-handoff validation
     */
    async performPreHandoffValidation(agentId) {
        // Implement validation logic
        console.log(`Pre-handoff validation for ${agentId}`);
    }
    /**
     * Transfer context between agents
     */
    async transferContext(fromAgent, toAgent) {
        // Implement context transfer logic
        console.log(`Context transfer: ${fromAgent} → ${toAgent}`);
    }
    /**
     * Perform post-handoff validation
     */
    async performPostHandoffValidation(agentId) {
        // Implement validation logic
        console.log(`Post-handoff validation for ${agentId}`);
    }
    /**
     * Notify context update
     */
    notifyContextUpdate(key, value) {
        // Implement context update notification
        console.log(`Context updated: ${key} = ${JSON.stringify(value)}`);
    }
}
exports.AgentCoordinator = AgentCoordinator;
//# sourceMappingURL=AgentCoordinator.js.map