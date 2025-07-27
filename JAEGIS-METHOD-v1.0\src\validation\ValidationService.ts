import * as vscode from 'vscode';
import { WebResearchService } from '../research/WebResearchService';

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

export class ValidationService {
    private webResearch: WebResearchService;
    private validationCache: Map<string, ValidationResult> = new Map();

    constructor() {
        this.webResearch = new WebResearchService();
    }

    /**
     * Validate dependencies with web research
     */
    public async validateDependencies(dependencies: string[]): Promise<ValidationResult> {
        const issues: ValidationIssue[] = [];
        const recommendations: string[] = [];
        const researchFindings: any[] = [];

        for (const dependency of dependencies) {
            try {
                const validation = await this.validateSingleDependency(dependency);
                
                if (validation.isOutdated) {
                    issues.push({
                        type: 'warning',
                        category: 'dependency',
                        message: `Outdated dependency: ${dependency}`,
                        details: `Current version ${validation.currentVersion} available, using ${validation.requestedVersion}`,
                        resolution: `Update to version ${validation.currentVersion}`
                    });
                }

                if (validation.hasVulnerabilities) {
                    issues.push({
                        type: 'error',
                        category: 'security',
                        message: `Security vulnerability in ${dependency}`,
                        details: `Known vulnerabilities found in ${validation.requestedVersion}`,
                        resolution: `Update to secure version ${validation.currentVersion}`
                    });
                }

                if (!validation.isCompatible) {
                    issues.push({
                        type: 'error',
                        category: 'compatibility',
                        message: `Compatibility issue with ${dependency}`,
                        details: `Version ${validation.requestedVersion} may not be compatible`,
                        resolution: validation.recommendation
                    });
                }

                recommendations.push(validation.recommendation);
                researchFindings.push({
                    package: dependency,
                    validation: validation,
                    researchDate: new Date().toISOString()
                });

            } catch (error) {
                issues.push({
                    type: 'error',
                    category: 'dependency',
                    message: `Failed to validate ${dependency}`,
                    details: `Validation error: ${error}`,
                    resolution: 'Manual verification required'
                });
            }
        }

        return {
            isValid: issues.filter(i => i.type === 'error').length === 0,
            issues,
            recommendations,
            researchFindings
        };
    }

    /**
     * Validate a single dependency
     */
    private async validateSingleDependency(dependency: string): Promise<DependencyValidation> {
        // Parse package name and version
        const [packageName, requestedVersion] = this.parseDependency(dependency);
        
        // Research current version
        const currentVersion = await this.webResearch.getCurrentPackageVersion(packageName);
        
        // Check for vulnerabilities
        const hasVulnerabilities = await this.webResearch.checkSecurityVulnerabilities(packageName, requestedVersion);
        
        // Check compatibility
        const isCompatible = await this.checkCompatibility(packageName, requestedVersion);
        
        // Determine if outdated
        const isOutdated = this.isVersionOutdated(requestedVersion, currentVersion);
        
        // Generate recommendation
        const recommendation = this.generateRecommendation(packageName, requestedVersion, currentVersion, hasVulnerabilities, isCompatible);

        return {
            packageName,
            requestedVersion,
            currentVersion,
            isOutdated,
            hasVulnerabilities,
            isCompatible,
            recommendation
        };
    }

    /**
     * Validate system requirements
     */
    public async validateSystemRequirements(requirements: string[]): Promise<ValidationResult> {
        const issues: ValidationIssue[] = [];
        const recommendations: string[] = [];
        const researchFindings: any[] = [];

        for (const requirement of requirements) {
            try {
                const isAvailable = await this.checkSystemRequirement(requirement);
                
                if (!isAvailable) {
                    const alternatives = await this.webResearch.findAlternatives(requirement);
                    
                    issues.push({
                        type: 'error',
                        category: 'dependency',
                        message: `System requirement not found: ${requirement}`,
                        details: `Required tool '${requirement}' is not available in system PATH`,
                        resolution: `Install ${requirement} or use alternative: ${alternatives.join(', ')}`
                    });

                    recommendations.push(`Install ${requirement} or consider alternatives: ${alternatives.join(', ')}`);
                    researchFindings.push({
                        requirement,
                        alternatives,
                        researchDate: new Date().toISOString()
                    });
                }
            } catch (error) {
                issues.push({
                    type: 'warning',
                    category: 'dependency',
                    message: `Could not validate system requirement: ${requirement}`,
                    details: `Validation error: ${error}`,
                    resolution: 'Manual verification recommended'
                });
            }
        }

        return {
            isValid: issues.filter(i => i.type === 'error').length === 0,
            issues,
            recommendations,
            researchFindings
        };
    }

    /**
     * Validate technology stack
     */
    public async validateTechnologyStack(stack: any): Promise<ValidationResult> {
        const issues: ValidationIssue[] = [];
        const recommendations: string[] = [];
        const researchFindings: any[] = [];

        // Validate each technology in the stack
        for (const [category, technology] of Object.entries(stack)) {
            try {
                const validation = await this.validateTechnology(category, technology as string);
                
                if (!validation.isCurrentVersion) {
                    issues.push({
                        type: 'warning',
                        category: 'dependency',
                        message: `Outdated ${category}: ${technology}`,
                        details: `Current version ${validation.currentVersion} available`,
                        resolution: `Consider updating to ${validation.currentVersion}`
                    });
                }

                if (validation.hasSecurityIssues) {
                    issues.push({
                        type: 'error',
                        category: 'security',
                        message: `Security issues in ${category}: ${technology}`,
                        details: validation.securityDetails,
                        resolution: validation.securityResolution
                    });
                }

                recommendations.push(validation.recommendation);
                researchFindings.push(validation.researchData);

            } catch (error) {
                issues.push({
                    type: 'warning',
                    category: 'dependency',
                    message: `Could not validate ${category}: ${technology}`,
                    details: `Validation error: ${error}`,
                    resolution: 'Manual verification recommended'
                });
            }
        }

        return {
            isValid: issues.filter(i => i.type === 'error').length === 0,
            issues,
            recommendations,
            researchFindings
        };
    }

    /**
     * Parse dependency string
     */
    private parseDependency(dependency: string): [string, string] {
        const parts = dependency.split('@');
        if (parts.length === 2) {
            return [parts[0], parts[1]];
        } else if (parts.length === 3 && parts[0] === '') {
            // Handle scoped packages like @types/node@^18.0.0
            return [`@${parts[1]}`, parts[2]];
        }
        return [dependency, 'latest'];
    }

    /**
     * Check if version is outdated
     */
    private isVersionOutdated(requested: string, current: string): boolean {
        // Implement version comparison logic
        // This is a simplified version - in practice, you'd use semver
        return requested !== current && !requested.includes(current);
    }

    /**
     * Check compatibility
     */
    private async checkCompatibility(packageName: string, version: string): Promise<boolean> {
        // Implement compatibility checking logic
        // This would involve checking peer dependencies, engine requirements, etc.
        return true; // Simplified for now
    }

    /**
     * Check system requirement availability
     */
    private async checkSystemRequirement(requirement: string): Promise<boolean> {
        // Implement system requirement checking
        // This would check if tools like 'chrome', 'node', etc. are available
        return true; // Simplified for now
    }

    /**
     * Validate individual technology
     */
    private async validateTechnology(category: string, technology: string): Promise<any> {
        // Implement technology validation logic
        return {
            isCurrentVersion: true,
            currentVersion: 'latest',
            hasSecurityIssues: false,
            securityDetails: '',
            securityResolution: '',
            recommendation: `${technology} is up to date`,
            researchData: {}
        };
    }

    /**
     * Generate recommendation
     */
    private generateRecommendation(packageName: string, requested: string, current: string, hasVulnerabilities: boolean, isCompatible: boolean): string {
        if (hasVulnerabilities) {
            return `CRITICAL: Update ${packageName} from ${requested} to ${current} to fix security vulnerabilities`;
        }
        if (!isCompatible) {
            return `Update ${packageName} to compatible version ${current}`;
        }
        if (requested !== current) {
            return `Consider updating ${packageName} from ${requested} to ${current} for latest features and fixes`;
        }
        return `${packageName}@${requested} is current and secure`;
    }
}
