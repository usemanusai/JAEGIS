import { Context7Integration } from '../integration/Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * DocQA - Documentation Quality Assurance Specialist
 *
 * Specialized agent for comprehensive documentation quality assurance, repository
 * documentation management, and professional documentation standards enforcement.
 * Provides systematic documentation analysis, quality validation, and improvement
 * recommendations with focus on zero 404 errors and complete coverage.
 *
 * Key Capabilities:
 * - Comprehensive documentation analysis and quality assessment
 * - Advanced quality assurance validation and compliance checking
 * - Systematic documentation improvement and optimization
 * - Professional repository structure and workflow management
 * - Zero-tolerance link validation and reference verification
 *
 * Integration Features:
 * - Context7 automatic research for documentation standards and best practices
 * - Cross-agent collaboration for comprehensive documentation solutions
 * - Real-time quality monitoring and automated validation
 * - Professional Git workflow implementation and branch management
 * - Strategic documentation portfolio management and optimization
 */
export declare class DocQAAgent {
    private context7;
    private statusBar;
    private logger;
    private qaIntegration;
    private isActive;
    private activeAnalyses;
    private validationQueue;
    private improvementPipeline;
    private qualityMetrics;
    private readonly ANALYSIS_TIMEOUT;
    private readonly VALIDATION_BATCH_SIZE;
    private readonly QUALITY_THRESHOLD;
    private readonly LINK_VALIDATION_INTERVAL;
    private documentationPatterns;
    private qualityStandards;
    private validationFrameworks;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize DocQA with documentation patterns and quality frameworks
     */
    initialize(): Promise<void>;
    /**
     * Analyze documentation quality and structure
     */
    analyzeDocumentation(repositoryPath: string, analysisOptions?: BMadTypes.DocumentationAnalysisOptions): Promise<BMadTypes.DocumentationAnalysisResult>;
    /**
     * Validate documentation standards and compliance
     */
    validateDocumentationStandards(analysisId: string, validationOptions?: BMadTypes.ValidationOptions): Promise<BMadTypes.ValidationResult>;
    /**
     * Generate comprehensive documentation quality report
     */
    generateDocumentationReport(analysisId: string, reportOptions?: BMadTypes.ReportOptions): Promise<BMadTypes.DocumentationReport>;
    /**
     * Improve documentation based on analysis and validation results
     */
    improveDocumentation(analysisId: string, improvementOptions?: BMadTypes.ImprovementOptions): Promise<BMadTypes.DocumentationImprovementResult>;
    /**
     * Audit content quality and accuracy
     */
    auditContentQuality(repositoryPath: string, auditOptions?: BMadTypes.ContentAuditOptions): Promise<BMadTypes.ContentQualityAuditResult>;
    /**
     * Generate documentation specification
     */
    generateDocumentationSpec(projectRequirements: BMadTypes.DocumentationProjectRequirements): Promise<string>;
    /**
     * Create documentation style guide
     */
    createStyleGuide(projectRequirements: BMadTypes.StyleGuideRequirements): Promise<string>;
    /**
     * Research documentation best practices
     */
    researchDocumentationBestPractices(domain: string, requirements: string[]): Promise<BMadTypes.DocumentationResearchResult>;
    /**
     * Get current documentation QA status
     */
    getQAStatus(): BMadTypes.DocumentationQAStatus;
    private getCurrentDate;
    private generateAnalysisId;
    private generateRequestId;
    private generateReportId;
    private generateImprovementId;
    private generateAuditId;
    private generateResearchId;
    private loadDocumentationPatterns;
    private loadQualityStandards;
    private loadValidationFrameworks;
    private initializeQualityMetrics;
    private analyzeRepositoryStructure;
    private conductDocumentationInventory;
    private performLinkValidation;
    private assessContentQuality;
    private evaluateAccessibilityCompliance;
    private calculateQualityScores;
    private generateImprovementRecommendations;
    private calculateOverallQualityScore;
    private identifyCriticalIssues;
    private calculateAnalysisMetrics;
    private assessComplianceStatus;
    private getDefaultValidationOptions;
    private calculateValidationPriority;
    private estimateValidationDuration;
    private performComplianceVerification;
    private calculateComplianceScore;
    private calculateValidationScore;
    private generateExecutiveSummary;
    private generateDetailedFindings;
    private generateQualityMetricsDashboard;
    private generateImprovementActionPlan;
    private generateComplianceAssessment;
    private calculateReportMetrics;
    private prioritizeRecommendations;
    private generateNextSteps;
    private createImprovementPipeline;
    private resolveCriticalIssues;
    private enhanceContentQuality;
    private optimizeDocumentationStructure;
    private implementAccessibilityImprovements;
    private validateImprovements;
    private calculateQualityImprovementScore;
    private calculateImprovementMetrics;
    private verifyTechnicalAccuracy;
    private assessContentCompleteness;
    private evaluateContentClarity;
    private validateStyleConsistency;
    private assessUserExperience;
    private calculateOverallContentScore;
    private calculateContentQualityMetrics;
    private generateContentImprovementRecommendations;
    private loadTemplate;
    private analyzeProjectRequirements;
    private populateSpecTemplate;
    private analyzeStyleRequirements;
    private populateStyleGuideTemplate;
    private analyzeDocumentationLandscape;
    private generateBestPracticeRecommendations;
    private assessImplementationComplexity;
    private generateImplementationGuidance;
    private generateQualityFramework;
    /**
     * Shutdown DocQA
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=DocQAAgent.d.ts.map