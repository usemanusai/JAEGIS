export interface SharedContext {
    projectInfo: any;
    currentPhase: string;
    activeAgents: string[];
    handoffQueue: string[];
    validationResults: any;
    dependencyStatus: any;
    researchCache: any;
    decisions: any[];
    knowledgeBase: any;
}
export interface AgentConfig {
    title: string;
    name: string;
    description: string;
    persona: string;
    tasks: string[];
    coordination: string;
    handoffFrom?: string[];
    handoffTo?: string[];
    validation?: string[];
    priority: number;
}
export declare class AgentCoordinator {
    private sharedContext;
    private agentConfigs;
    private activeAgent;
    private handoffQueue;
    constructor();
    /**
     * Initialize the agent coordination system
     */
    initialize(workspaceRoot: string): Promise<void>;
    /**
     * Load agent configuration from standardized config file
     */
    private loadAgentConfiguration;
    /**
     * Parse the standardized agent configuration format
     */
    private parseAgentConfiguration;
    /**
     * Parse individual agent section
     */
    private parseAgentSection;
    /**
     * Activate an agent with proper coordination
     */
    activateAgent(agentId: string, taskId?: string): Promise<void>;
    /**
     * Perform agent handoff with context preservation
     */
    performHandoff(fromAgent: string, toAgent: string): Promise<void>;
    /**
     * Update shared context
     */
    updateSharedContext(key: string, value: any): void;
    /**
     * Get shared context
     */
    getSharedContext(): SharedContext;
    /**
     * Get available agents
     */
    getAvailableAgents(): AgentConfig[];
    /**
     * Get current active agent
     */
    getActiveAgent(): string | null;
    /**
     * Perform pre-activation validation
     */
    private performPreActivationValidation;
    /**
     * Perform pre-handoff validation
     */
    private performPreHandoffValidation;
    /**
     * Transfer context between agents
     */
    private transferContext;
    /**
     * Perform post-handoff validation
     */
    private performPostHandoffValidation;
    /**
     * Notify context update
     */
    private notifyContextUpdate;
}
//# sourceMappingURL=AgentCoordinator.d.ts.map