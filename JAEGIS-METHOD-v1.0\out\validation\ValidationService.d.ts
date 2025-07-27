export interface ValidationResult {
    isValid: boolean;
    issues: ValidationIssue[];
    recommendations: string[];
    researchFindings: any[];
}
export interface ValidationIssue {
    type: 'error' | 'warning' | 'info';
    category: 'dependency' | 'security' | 'compatibility' | 'performance';
    message: string;
    details: string;
    resolution?: string;
}
export interface DependencyValidation {
    packageName: string;
    requestedVersion: string;
    currentVersion: string;
    isOutdated: boolean;
    hasVulnerabilities: boolean;
    isCompatible: boolean;
    recommendation: string;
}
export declare class ValidationService {
    private webResearch;
    private validationCache;
    constructor();
    /**
     * Validate dependencies with web research
     */
    validateDependencies(dependencies: string[]): Promise<ValidationResult>;
    /**
     * Validate a single dependency
     */
    private validateSingleDependency;
    /**
     * Validate system requirements
     */
    validateSystemRequirements(requirements: string[]): Promise<ValidationResult>;
    /**
     * Validate technology stack
     */
    validateTechnologyStack(stack: any): Promise<ValidationResult>;
    /**
     * Parse dependency string
     */
    private parseDependency;
    /**
     * Check if version is outdated
     */
    private isVersionOutdated;
    /**
     * Check compatibility
     */
    private checkCompatibility;
    /**
     * Check system requirement availability
     */
    private checkSystemRequirement;
    /**
     * Validate individual technology
     */
    private validateTechnology;
    /**
     * Generate recommendation
     */
    private generateRecommendation;
}
//# sourceMappingURL=ValidationService.d.ts.map