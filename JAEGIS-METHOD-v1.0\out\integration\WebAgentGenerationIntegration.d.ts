import { Context7Integration } from './Context7Integration';
import { StatusBarManager } from '../ui/StatusBarManager';
import { BMadTypes } from '../types/BMadTypes';
import { Logger } from '../utils/Logger';
/**
 * Web Agent Generation Integration Module
 *
 * Provides automated web agent generation capabilities including UI/UX implementation,
 * responsive design generation, and performance optimization for the BMAD Web Agent
 * Creator system. Handles the complete web development pipeline from design to
 * deployment-ready implementation.
 *
 * Key Features:
 * - Automated web application generation from design specifications
 * - Framework-agnostic code generation (React, Vue, Svelte, Angular)
 * - Responsive design implementation and cross-browser optimization
 * - Accessibility compliance and WCAG validation
 * - Performance optimization and Core Web Vitals compliance
 *
 * Integration Capabilities:
 * - Context7 automatic research for web development best practices
 * - Cross-framework pattern analysis and optimization
 * - Real-time generation monitoring and performance analytics
 * - Automated testing and accessibility validation integration
 * - Deployment pipeline preparation and hosting optimization
 */
export declare class WebAgentGenerationIntegration {
    private context7;
    private statusBar;
    private logger;
    private isGenerating;
    private activeGenerations;
    private generationTemplates;
    private frameworkAdapters;
    private generationMetrics;
    private readonly GENERATION_TIMEOUT;
    private readonly MAX_CONCURRENT_GENERATIONS;
    private readonly QUALITY_THRESHOLD;
    private readonly PERFORMANCE_THRESHOLD;
    private readonly WEB_FRAMEWORKS;
    private readonly COMPONENT_PATTERNS;
    constructor(context7: Context7Integration, statusBar: StatusBarManager, logger: Logger);
    /**
     * Initialize web agent generation integration
     */
    initialize(): Promise<void>;
    /**
     * Generate complete web agent implementation from design specification
     */
    generateWebAgent(request: BMadTypes.WebAgentGenerationRequest): Promise<BMadTypes.WebAgentGenerationResult>;
    /**
     * Generate project structure and configuration files
     */
    generateProjectStructure(request: BMadTypes.WebAgentGenerationRequest, session: BMadTypes.WebGenerationSession): Promise<BMadTypes.GeneratedArtifact>;
    /**
     * Generate UI components and layouts
     */
    generateUIComponents(request: BMadTypes.WebAgentGenerationRequest, session: BMadTypes.WebGenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    /**
     * Generate responsive styles and theme system
     */
    generateResponsiveStyles(request: BMadTypes.WebAgentGenerationRequest, session: BMadTypes.WebGenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    /**
     * Generate accessibility features and WCAG compliance
     */
    generateAccessibilityFeatures(request: BMadTypes.WebAgentGenerationRequest, session: BMadTypes.WebGenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    /**
     * Generate API integration and state management
     */
    generateAPIIntegration(request: BMadTypes.WebAgentGenerationRequest, session: BMadTypes.WebGenerationSession): Promise<BMadTypes.GeneratedArtifact[]>;
    private getCurrentDate;
    private generateGenerationId;
    private generateArtifactId;
    private calculateQualityScore;
    private calculatePerformanceScore;
    private calculateAccessibilityScore;
    private loadGenerationTemplates;
    private initializeFrameworkAdapters;
    private initializeGenerationMetrics;
    private createWebGenerationSession;
    private prepareProjectStructureVariables;
    private processProjectTemplate;
    private validateProjectStructure;
    private prepareComponentVariables;
    private processComponentTemplate;
    private validateComponent;
    private prepareStyleVariables;
    private processStyleTemplate;
    private validateStyles;
    private prepareAccessibilityVariables;
    private processAccessibilityTemplate;
    private validateAccessibility;
    private prepareAPIIntegrationVariables;
    private processAPITemplate;
    private validateAPIIntegration;
    private performWebQualityValidation;
    private calculateGenerationMetrics;
    private assessDeploymentReadiness;
    private generateTestingSuite;
    private generateBuildConfiguration;
    private generatePerformanceOptimization;
    /**
     * Shutdown web agent generation integration
     */
    shutdown(): Promise<void>;
}
//# sourceMappingURL=WebAgentGenerationIntegration.d.ts.map