export interface ResearchResult {
    query: string;
    results: any[];
    timestamp: Date;
    sources: string[];
}
export interface PackageInfo {
    name: string;
    currentVersion: string;
    description: string;
    lastUpdated: Date;
    maintainers: string[];
    vulnerabilities: any[];
    alternatives: string[];
}
export declare class WebResearchService {
    private researchCache;
    private packageCache;
    /**
     * Get current package version from npm registry
     */
    getCurrentPackageVersion(packageName: string): Promise<string>;
    /**
     * Check for security vulnerabilities
     */
    checkSecurityVulnerabilities(packageName: string, version: string): Promise<boolean>;
    /**
     * Find alternatives for a package or tool
     */
    findAlternatives(packageOrTool: string): Promise<string[]>;
    /**
     * Research current best practices for a technology
     */
    researchBestPractices(technology: string): Promise<ResearchResult>;
    /**
     * Research framework compatibility
     */
    researchFrameworkCompatibility(framework: string, version: string): Promise<any>;
    /**
     * Research security best practices
     */
    researchSecurityPractices(context: string): Promise<ResearchResult>;
    /**
     * Fetch package information from npm registry
     */
    private fetchPackageInfo;
    /**
     * Research alternatives for a package or tool
     */
    private researchAlternatives;
    /**
     * Perform web research (simplified implementation)
     */
    private performWebResearch;
    /**
     * Fetch framework compatibility information
     */
    private fetchFrameworkCompatibility;
    /**
     * Clear research cache
     */
    clearCache(): void;
    /**
     * Get cache statistics
     */
    getCacheStats(): any;
}
//# sourceMappingURL=WebResearchService.d.ts.map