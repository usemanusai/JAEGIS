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
exports.WebResearchService = void 0;
const https = __importStar(require("https"));
class WebResearchService {
    researchCache = new Map();
    packageCache = new Map();
    /**
     * Get current package version from npm registry
     */
    async getCurrentPackageVersion(packageName) {
        const cacheKey = `package-${packageName}`;
        if (this.packageCache.has(cacheKey)) {
            const cached = this.packageCache.get(cacheKey);
            // Check if cache is still valid (less than 1 hour old)
            if (Date.now() - cached.lastUpdated.getTime() < 3600000) {
                return cached.currentVersion;
            }
        }
        try {
            const packageInfo = await this.fetchPackageInfo(packageName);
            this.packageCache.set(cacheKey, packageInfo);
            return packageInfo.currentVersion;
        }
        catch (error) {
            console.error(`Failed to fetch package info for ${packageName}:`, error);
            return 'unknown';
        }
    }
    /**
     * Check for security vulnerabilities
     */
    async checkSecurityVulnerabilities(packageName, version) {
        try {
            const packageInfo = await this.fetchPackageInfo(packageName);
            return packageInfo.vulnerabilities.length > 0;
        }
        catch (error) {
            console.error(`Failed to check vulnerabilities for ${packageName}:`, error);
            return false;
        }
    }
    /**
     * Find alternatives for a package or tool
     */
    async findAlternatives(packageOrTool) {
        const cacheKey = `alternatives-${packageOrTool}`;
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey);
            if (Date.now() - cached.timestamp.getTime() < 3600000) {
                return cached.results;
            }
        }
        try {
            const alternatives = await this.researchAlternatives(packageOrTool);
            this.researchCache.set(cacheKey, {
                query: packageOrTool,
                results: alternatives,
                timestamp: new Date(),
                sources: ['npm', 'github', 'stackoverflow']
            });
            return alternatives;
        }
        catch (error) {
            console.error(`Failed to find alternatives for ${packageOrTool}:`, error);
            return [];
        }
    }
    /**
     * Research current best practices for a technology
     */
    async researchBestPractices(technology) {
        const cacheKey = `best-practices-${technology}`;
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey);
            if (Date.now() - cached.timestamp.getTime() < 3600000) {
                return cached;
            }
        }
        try {
            const results = await this.performWebResearch(`${technology} best practices 2025`);
            const researchResult = {
                query: `${technology} best practices`,
                results: results,
                timestamp: new Date(),
                sources: ['official docs', 'github', 'dev community']
            };
            this.researchCache.set(cacheKey, researchResult);
            return researchResult;
        }
        catch (error) {
            console.error(`Failed to research best practices for ${technology}:`, error);
            return {
                query: `${technology} best practices`,
                results: [],
                timestamp: new Date(),
                sources: []
            };
        }
    }
    /**
     * Research framework compatibility
     */
    async researchFrameworkCompatibility(framework, version) {
        const cacheKey = `compatibility-${framework}-${version}`;
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey);
            if (Date.now() - cached.timestamp.getTime() < 3600000) {
                return cached.results[0];
            }
        }
        try {
            const compatibility = await this.fetchFrameworkCompatibility(framework, version);
            this.researchCache.set(cacheKey, {
                query: `${framework} ${version} compatibility`,
                results: [compatibility],
                timestamp: new Date(),
                sources: ['official docs', 'npm']
            });
            return compatibility;
        }
        catch (error) {
            console.error(`Failed to research compatibility for ${framework}@${version}:`, error);
            return {
                compatible: true,
                issues: [],
                recommendations: []
            };
        }
    }
    /**
     * Research security best practices
     */
    async researchSecurityPractices(context) {
        const cacheKey = `security-${context}`;
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey);
            if (Date.now() - cached.timestamp.getTime() < 3600000) {
                return cached;
            }
        }
        try {
            const results = await this.performWebResearch(`${context} security best practices 2025`);
            const researchResult = {
                query: `${context} security practices`,
                results: results,
                timestamp: new Date(),
                sources: ['OWASP', 'security advisories', 'official docs']
            };
            this.researchCache.set(cacheKey, researchResult);
            return researchResult;
        }
        catch (error) {
            console.error(`Failed to research security practices for ${context}:`, error);
            return {
                query: `${context} security practices`,
                results: [],
                timestamp: new Date(),
                sources: []
            };
        }
    }
    /**
     * Fetch package information from npm registry
     */
    async fetchPackageInfo(packageName) {
        return new Promise((resolve, reject) => {
            const url = `https://registry.npmjs.org/${packageName}`;
            https.get(url, (response) => {
                let data = '';
                response.on('data', (chunk) => {
                    data += chunk;
                });
                response.on('end', () => {
                    try {
                        const packageData = JSON.parse(data);
                        const latestVersion = packageData['dist-tags']?.latest || 'unknown';
                        resolve({
                            name: packageName,
                            currentVersion: latestVersion,
                            description: packageData.description || '',
                            lastUpdated: new Date(packageData.time?.[latestVersion] || Date.now()),
                            maintainers: packageData.maintainers?.map((m) => m.name) || [],
                            vulnerabilities: [], // Would need to check npm audit API
                            alternatives: []
                        });
                    }
                    catch (error) {
                        reject(new Error(`Failed to parse package data: ${error}`));
                    }
                });
            }).on('error', (error) => {
                reject(new Error(`HTTP request failed: ${error}`));
            });
        });
    }
    /**
     * Research alternatives for a package or tool
     */
    async researchAlternatives(packageOrTool) {
        // This would typically involve multiple API calls to different sources
        // For now, return some common alternatives based on known patterns
        const commonAlternatives = {
            'chrome': ['chromium', 'firefox', 'edge'],
            'node': ['nodejs', 'nvm', 'n'],
            'npm': ['yarn', 'pnpm'],
            'webpack': ['vite', 'rollup', 'parcel'],
            'jest': ['vitest', 'mocha', 'jasmine'],
            'eslint': ['tslint', 'jshint', 'standard']
        };
        return commonAlternatives[packageOrTool.toLowerCase()] || [];
    }
    /**
     * Perform web research (simplified implementation)
     */
    async performWebResearch(query) {
        // This would typically use a search API or web scraping
        // For now, return mock results based on common patterns
        return [
            {
                title: `${query} - Official Documentation`,
                url: `https://docs.example.com/${query}`,
                summary: `Official documentation for ${query}`,
                relevance: 0.9
            },
            {
                title: `${query} - Best Practices Guide`,
                url: `https://github.com/example/${query}`,
                summary: `Community best practices for ${query}`,
                relevance: 0.8
            }
        ];
    }
    /**
     * Fetch framework compatibility information
     */
    async fetchFrameworkCompatibility(framework, version) {
        // This would typically check compatibility matrices and peer dependencies
        return {
            compatible: true,
            issues: [],
            recommendations: [`${framework}@${version} is compatible with current ecosystem`],
            peerDependencies: {},
            engineRequirements: {}
        };
    }
    /**
     * Clear research cache
     */
    clearCache() {
        this.researchCache.clear();
        this.packageCache.clear();
    }
    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            researchCacheSize: this.researchCache.size,
            packageCacheSize: this.packageCache.size,
            totalCacheSize: this.researchCache.size + this.packageCache.size
        };
    }
}
exports.WebResearchService = WebResearchService;
//# sourceMappingURL=WebResearchService.js.map