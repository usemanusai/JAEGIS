/**
 * Context7 Integration Module for Dakota Agent
 * Provides seamless integration with Upstash Context7 system for dependency research
 * Automatically activates for dependency-related tasks without manual user prompts
 */
export interface Context7Config {
    apiKey?: string;
    baseUrl: string;
    autoActivate: boolean;
    maxRetries: number;
    timeoutMs: number;
    cacheEnabled: boolean;
    cacheTtlMs: number;
}
export interface Context7Query {
    query: string;
    sources?: string[];
    dateContext?: string;
    focus?: string[];
    packageName?: string;
    version?: string;
    ecosystem?: string;
}
export interface Context7Response {
    success: boolean;
    data?: any;
    insights?: string[];
    recommendations?: string[];
    sources?: string[];
    confidence?: number;
    error?: string;
    cached?: boolean;
}
export interface Context7ResearchResult {
    query: Context7Query;
    response: Context7Response;
    timestamp: Date;
    duration: number;
    quality: number;
}
/**
 * Context7 Integration Service
 * Handles automatic research activation and intelligent caching
 */
export declare class Context7Integration {
    private config;
    private cache;
    private isAvailable;
    private lastHealthCheck;
    private healthCheckInterval;
    constructor(config?: Partial<Context7Config>);
    /**
     * Initialize Context7 integration and check availability
     */
    private initializeIntegration;
    /**
     * Load configuration from VS Code settings
     */
    private loadConfiguration;
    /**
     * Check Context7 service health and availability
     */
    private healthCheck;
    /**
     * Automatic research activation for dependency tasks
     */
    autoResearch(query: Context7Query): Promise<Context7ResearchResult | null>;
    /**
     * Perform dependency security research
     */
    securityResearch(packageName: string, version?: string, ecosystem?: string): Promise<Context7ResearchResult | null>;
    /**
     * Perform dependency update research
     */
    updateResearch(packageName: string, currentVersion: string, targetVersion: string, ecosystem?: string): Promise<Context7ResearchResult | null>;
    /**
     * Perform alternative package research
     */
    alternativeResearch(packageName: string, reason: string, ecosystem?: string): Promise<Context7ResearchResult | null>;
    /**
     * Perform actual research request to Context7
     */
    private performResearch;
    /**
     * Make HTTP request to Context7 API
     */
    private makeRequest;
    /**
     * Generate cache key for query
     */
    private generateCacheKey;
    /**
     * Get cached result if available and not expired
     */
    private getCachedResult;
    /**
     * Cache research result
     */
    private setCachedResult;
    /**
     * Clean up expired cache entries
     */
    private cleanupCache;
    /**
     * Assess the quality of a Context7 response
     */
    private assessResponseQuality;
    /**
     * Check if Context7 integration is available
     */
    isIntegrationAvailable(): boolean;
    /**
     * Get integration status and statistics
     */
    getIntegrationStatus(): {
        available: boolean;
        cacheSize: number;
        lastHealthCheck: Date | null;
        config: Context7Config;
    };
    /**
     * Clear cache and reset integration
     */
    reset(): void;
    /**
     * Dispose of integration resources
     */
    dispose(): void;
}
//# sourceMappingURL=Context7Integration.d.ts.map