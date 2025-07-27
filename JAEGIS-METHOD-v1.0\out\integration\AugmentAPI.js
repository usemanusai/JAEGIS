"use strict";
/**
 * Type definitions for Augment AI Code extension API
 * These interfaces define the expected API structure for integration
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_AUGMENT_CONFIG = void 0;
exports.isAugmentAPI = isAugmentAPI;
exports.isAugmentExtendedAPI = isAugmentExtendedAPI;
/**
 * Type guard to check if an object implements AugmentAPI
 */
function isAugmentAPI(obj) {
    return obj &&
        typeof obj.registerWorkflowProvider === 'function' &&
        typeof obj.unregisterWorkflowProvider === 'function' &&
        typeof obj.getWorkflowProviders === 'function';
}
/**
 * Type guard to check if an object implements AugmentExtendedAPI
 */
function isAugmentExtendedAPI(obj) {
    return isAugmentAPI(obj) &&
        typeof obj.addMainMenuItems === 'function' &&
        typeof obj.showPanel === 'function';
}
/**
 * Default configuration for Augment integration
 */
exports.DEFAULT_AUGMENT_CONFIG = {
    enableWorkflowProvider: true,
    enableMenuIntegration: true,
    enableProgressReporting: true,
    defaultCategory: 'AI Workflows',
    fallbackToVSCode: true,
    showNotifications: true
};
//# sourceMappingURL=AugmentAPI.js.map