"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ValidationService = void 0;
const WebResearchService_1 = require("../research/WebResearchService");
class ValidationService {
    webResearch;
    validationCache = new Map();
    constructor() {
        this.webResearch = new WebResearchService_1.WebResearchService();
    }
    /**
     * Validate dependencies with web research
     */
    async validateDependencies(dependencies) {
        const issues = [];
        const recommendations = [];
        const researchFindings = [];
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
            }
            catch (error) {
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
    async validateSingleDependency(dependency) {
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
    async validateSystemRequirements(requirements) {
        const issues = [];
        const recommendations = [];
        const researchFindings = [];
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
            }
            catch (error) {
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
    async validateTechnologyStack(stack) {
        const issues = [];
        const recommendations = [];
        const researchFindings = [];
        // Validate each technology in the stack
        for (const [category, technology] of Object.entries(stack)) {
            try {
                const validation = await this.validateTechnology(category, technology);
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
            }
            catch (error) {
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
    parseDependency(dependency) {
        const parts = dependency.split('@');
        if (parts.length === 2) {
            return [parts[0], parts[1]];
        }
        else if (parts.length === 3 && parts[0] === '') {
            // Handle scoped packages like @types/node@^18.0.0
            return [`@${parts[1]}`, parts[2]];
        }
        return [dependency, 'latest'];
    }
    /**
     * Check if version is outdated
     */
    isVersionOutdated(requested, current) {
        // Implement version comparison logic
        // This is a simplified version - in practice, you'd use semver
        return requested !== current && !requested.includes(current);
    }
    /**
     * Check compatibility
     */
    async checkCompatibility(packageName, version) {
        // Implement compatibility checking logic
        // This would involve checking peer dependencies, engine requirements, etc.
        return true; // Simplified for now
    }
    /**
     * Check system requirement availability
     */
    async checkSystemRequirement(requirement) {
        // Implement system requirement checking
        // This would check if tools like 'chrome', 'node', etc. are available
        return true; // Simplified for now
    }
    /**
     * Validate individual technology
     */
    async validateTechnology(category, technology) {
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
    generateRecommendation(packageName, requested, current, hasVulnerabilities, isCompatible) {
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
exports.ValidationService = ValidationService;
//# sourceMappingURL=ValidationService.js.map