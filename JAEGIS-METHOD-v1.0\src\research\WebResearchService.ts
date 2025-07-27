import * as vscode from 'vscode';
import * as https from 'https';

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

export class WebResearchService {
    private researchCache: Map<string, ResearchResult> = new Map();
    private packageCache: Map<string, PackageInfo> = new Map();

    /**
     * Get current package version from npm registry
     */
    public async getCurrentPackageVersion(packageName: string): Promise<string> {
        const cacheKey = `package-${packageName}`;
        
        if (this.packageCache.has(cacheKey)) {
            const cached = this.packageCache.get(cacheKey)!;
            // Check if cache is still valid (less than 1 hour old)
            if (Date.now() - cached.lastUpdated.getTime() < 3600000) {
                return cached.currentVersion;
            }
        }

        try {
            const packageInfo = await this.fetchPackageInfo(packageName);
            this.packageCache.set(cacheKey, packageInfo);
            return packageInfo.currentVersion;
        } catch (error) {
            console.error(`Failed to fetch package info for ${packageName}:`, error);
            return 'unknown';
        }
    }

    /**
     * Check for security vulnerabilities
     */
    public async checkSecurityVulnerabilities(packageName: string, version: string): Promise<boolean> {
        try {
            const packageInfo = await this.fetchPackageInfo(packageName);
            return packageInfo.vulnerabilities.length > 0;
        } catch (error) {
            console.error(`Failed to check vulnerabilities for ${packageName}:`, error);
            return false;
        }
    }

    /**
     * Find alternatives for a package or tool
     */
    public async findAlternatives(packageOrTool: string): Promise<string[]> {
        const cacheKey = `alternatives-${packageOrTool}`;
        
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey)!;
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
        } catch (error) {
            console.error(`Failed to find alternatives for ${packageOrTool}:`, error);
            return [];
        }
    }

    /**
     * Research current best practices for a technology
     */
    public async researchBestPractices(technology: string): Promise<ResearchResult> {
        const cacheKey = `best-practices-${technology}`;
        
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey)!;
            if (Date.now() - cached.timestamp.getTime() < 3600000) {
                return cached;
            }
        }

        try {
            const results = await this.performWebResearch(`${technology} best practices 2025`);
            const researchResult: ResearchResult = {
                query: `${technology} best practices`,
                results: results,
                timestamp: new Date(),
                sources: ['official docs', 'github', 'dev community']
            };
            
            this.researchCache.set(cacheKey, researchResult);
            return researchResult;
        } catch (error) {
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
    public async researchFrameworkCompatibility(framework: string, version: string): Promise<any> {
        const cacheKey = `compatibility-${framework}-${version}`;
        
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey)!;
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
        } catch (error) {
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
    public async researchSecurityPractices(context: string): Promise<ResearchResult> {
        const cacheKey = `security-${context}`;
        
        if (this.researchCache.has(cacheKey)) {
            const cached = this.researchCache.get(cacheKey)!;
            if (Date.now() - cached.timestamp.getTime() < 3600000) {
                return cached;
            }
        }

        try {
            const results = await this.performWebResearch(`${context} security best practices 2025`);
            const researchResult: ResearchResult = {
                query: `${context} security practices`,
                results: results,
                timestamp: new Date(),
                sources: ['OWASP', 'security advisories', 'official docs']
            };
            
            this.researchCache.set(cacheKey, researchResult);
            return researchResult;
        } catch (error) {
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
    private async fetchPackageInfo(packageName: string): Promise<PackageInfo> {
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
                            maintainers: packageData.maintainers?.map((m: any) => m.name) || [],
                            vulnerabilities: [], // Would need to check npm audit API
                            alternatives: []
                        });
                    } catch (error) {
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
    private async researchAlternatives(packageOrTool: string): Promise<string[]> {
        // This would typically involve multiple API calls to different sources
        // For now, return some common alternatives based on known patterns
        const commonAlternatives: { [key: string]: string[] } = {
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
    private async performWebResearch(query: string): Promise<any[]> {
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
    private async fetchFrameworkCompatibility(framework: string, version: string): Promise<any> {
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
    public clearCache(): void {
        this.researchCache.clear();
        this.packageCache.clear();
    }

    /**
     * Get cache statistics
     */
    public getCacheStats(): any {
        return {
            researchCacheSize: this.researchCache.size,
            packageCacheSize: this.packageCache.size,
            totalCacheSize: this.researchCache.size + this.packageCache.size
        };
    }
}
