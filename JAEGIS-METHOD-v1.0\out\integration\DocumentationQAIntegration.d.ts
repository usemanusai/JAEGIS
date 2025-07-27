import { Context7Integration } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Documentation Quality Assurance Integration Module
 *
 * Provides comprehensive documentation quality assurance capabilities including
 * automated analysis, validation, and improvement for the BMAD DocQA system.
 * Handles the complete documentation QA pipeline from analysis to improvement
 * implementation with professional standards enforcement.
 *
 * Key Features:
 * - Automated documentation analysis and quality assessment
 * - Comprehensive link validation and reference verification
 * - Content quality evaluation and accuracy validation
 * - Accessibility compliance and standards verification
 * - Professional repository structure optimization
 *
 * Integration Capabilities:
 * - Context7 automatic research for documentation standards and methodologies
 * - Cross-platform documentation analysis and validation
 * - Real-time quality monitoring and improvement tracking
 * - Automated compliance verification and regulatory adherence
 * - Professional Git workflow implementation and branch management
 */
export declare class DocumentationQAIntegration {
    private context7;
    private statusBar;
    private logger;
    private isValidating;
    private activeValidations;
    private validationFrameworks;
    private qualityStandards;
    private qaMetrics;
    private readonly VALIDATION_TIMEOUT;
    private readonly MAX_CONCURRENT_VALIDATIONS;
    private readonly QUALITY_THRESHOLD;
    private readonly COMPLIANCE_THRESHOLD;
    private readonly QA_FRAMEWORKS;
    private readonly VALIDATION_PATTERNS;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize documentation QA integration
     */
    initialize(): Promise<void>;
    /**
     * Validate documentation quality comprehensively
     */
    validateDocumentationQuality(request: BMadTypes.QualityValidationRequest): Promise<BMadTypes.ValidationResult>;
    /**
     * Execute comprehensive link validation
     */
    executeLinkValidation(request: BMadTypes.QualityValidationRequest, session: BMadTypes.QualityValidationSession): Promise<BMadTypes.LinkValidationResult>;
    /**
     * Perform content quality analysis
     */
    performContentQualityAnalysis(request: BMadTypes.QualityValidationRequest, session: BMadTypes.QualityValidationSession): Promise<BMadTypes.ContentQualityResult>;
    /**
     * Execute accessibility compliance testing
     */
    executeAccessibilityTesting(request: BMadTypes.QualityValidationRequest, session: BMadTypes.QualityValidationSession): Promise<BMadTypes.AccessibilityTestingResult>;
    /**
     * Validate repository structure and workflow
     */
    validateRepositoryStructure(request: BMadTypes.QualityValidationRequest, session: BMadTypes.QualityValidationSession): Promise<BMadTypes.RepositoryStructureResult>;
    private getCurrentDate;
    private generateValidationId;
    private generateAnalysisId;
    private generateTestingId;
    private calculateOverallScore;
    private calculateComplianceScore;
    private calculateLinkIntegrityScore;
    private calculateContentQualityScore;
    private calculateAccessibilityScore;
    private calculateStructureScore;
    private calculateWorkflowScore;
    private loadValidationFrameworks;
    private initializeQualityStandards;
    private initializeQAMetrics;
    private createValidationSession;
    private extractAllLinks;
    private validateInternalLinks;
    private validateExternalLinks;
    private validateCrossReferences;
    private detectBrokenLinks;
    private identifyCriticalLinkIssues;
    private calculateLinkValidationMetrics;
    private analyzeTechnicalAccuracy;
    private assessContentCompleteness;
    private evaluateContentClarity;
    private validateInformationCurrency;
    private assessContentUsability;
    private calculateContentQualityMetrics;
    private identifyContentImprovementOpportunities;
    private performWCAGComplianceTesting;
    private testScreenReaderCompatibility;
    private validateKeyboardNavigation;
    private testColorAccessibility;
    private validateMediaAccessibility;
    private determineComplianceLevel;
    private calculateAccessibilityMetrics;
    private identifyAccessibilityIssues;
    private analyzeBranchStructure;
    private validateDocumentationOrganization;
    private validateFileStructure;
    private validateVersionControl;
    private assessWorkflowCompliance;
    private calculateStructureMetrics;
    private identifyStructureImprovements;
    private performComplianceVerification;
    private validateTechnicalAccuracy;
    private validateStyleConsistency;
    private calculateQualityScoring;
    private identifyCriticalIssues;
    private calculateValidationMetrics;
    private generateImprovementRecommendations;
    /**
     * Shutdown documentation QA integration
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=DocumentationQAIntegration.d.ts.map