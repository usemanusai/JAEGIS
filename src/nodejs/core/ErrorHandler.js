/**
 * JAEGIS Error Handler
 * Comprehensive error handling and recovery framework
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

// Error types and codes
const ERROR_TYPES = {
  VALIDATION: 'VALIDATION_ERROR',
  AUTHENTICATION: 'AUTHENTICATION_ERROR',
  AUTHORIZATION: 'AUTHORIZATION_ERROR',
  NOT_FOUND: 'NOT_FOUND_ERROR',
  TIMEOUT: 'TIMEOUT_ERROR',
  RATE_LIMIT: 'RATE_LIMIT_ERROR',
  EXTERNAL_SERVICE: 'EXTERNAL_SERVICE_ERROR',
  PROCESSING: 'PROCESSING_ERROR',
  CONFIGURATION: 'CONFIGURATION_ERROR',
  PLUGIN: 'PLUGIN_ERROR',
  SYSTEM: 'SYSTEM_ERROR',
  NETWORK: 'NETWORK_ERROR',
  DATABASE: 'DATABASE_ERROR',
  CACHE: 'CACHE_ERROR',
  UNKNOWN: 'UNKNOWN_ERROR'
}

const ERROR_SEVERITY = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical'
}

const RECOVERY_STRATEGIES = {
  RETRY: 'retry',
  FALLBACK: 'fallback',
  CIRCUIT_BREAKER: 'circuit_breaker',
  GRACEFUL_DEGRADATION: 'graceful_degradation',
  FAIL_FAST: 'fail_fast',
  IGNORE: 'ignore'
}

class JAEGISError extends Error {
  constructor(message, type = ERROR_TYPES.UNKNOWN, code = null, details = {}) {
    super(message)
    this.name = 'JAEGISError'
    this.type = type
    this.code = code
    this.details = details
    this.timestamp = Date.now()
    this.severity = this.determineSeverity(type)
    this.recoverable = this.isRecoverable(type)
    this.userFriendly = this.generateUserFriendlyMessage(message, type)
    
    // Capture stack trace
    Error.captureStackTrace(this, JAEGISError)
  }

  determineSeverity(type) {
    const severityMap = {
      [ERROR_TYPES.VALIDATION]: ERROR_SEVERITY.LOW,
      [ERROR_TYPES.AUTHENTICATION]: ERROR_SEVERITY.MEDIUM,
      [ERROR_TYPES.AUTHORIZATION]: ERROR_SEVERITY.MEDIUM,
      [ERROR_TYPES.NOT_FOUND]: ERROR_SEVERITY.LOW,
      [ERROR_TYPES.TIMEOUT]: ERROR_SEVERITY.MEDIUM,
      [ERROR_TYPES.RATE_LIMIT]: ERROR_SEVERITY.MEDIUM,
      [ERROR_TYPES.EXTERNAL_SERVICE]: ERROR_SEVERITY.HIGH,
      [ERROR_TYPES.PROCESSING]: ERROR_SEVERITY.MEDIUM,
      [ERROR_TYPES.CONFIGURATION]: ERROR_SEVERITY.HIGH,
      [ERROR_TYPES.PLUGIN]: ERROR_SEVERITY.MEDIUM,
      [ERROR_TYPES.SYSTEM]: ERROR_SEVERITY.CRITICAL,
      [ERROR_TYPES.NETWORK]: ERROR_SEVERITY.HIGH,
      [ERROR_TYPES.DATABASE]: ERROR_SEVERITY.HIGH,
      [ERROR_TYPES.CACHE]: ERROR_SEVERITY.LOW,
      [ERROR_TYPES.UNKNOWN]: ERROR_SEVERITY.MEDIUM
    }
    
    return severityMap[type] || ERROR_SEVERITY.MEDIUM
  }

  isRecoverable(type) {
    const recoverableTypes = [
      ERROR_TYPES.TIMEOUT,
      ERROR_TYPES.RATE_LIMIT,
      ERROR_TYPES.EXTERNAL_SERVICE,
      ERROR_TYPES.NETWORK,
      ERROR_TYPES.CACHE
    ]
    
    return recoverableTypes.includes(type)
  }

  generateUserFriendlyMessage(message, type) {
    const friendlyMessages = {
      [ERROR_TYPES.VALIDATION]: 'Please check your input and try again.',
      [ERROR_TYPES.AUTHENTICATION]: 'Authentication required. Please log in.',
      [ERROR_TYPES.AUTHORIZATION]: 'You do not have permission to perform this action.',
      [ERROR_TYPES.NOT_FOUND]: 'The requested resource was not found.',
      [ERROR_TYPES.TIMEOUT]: 'The operation timed out. Please try again.',
      [ERROR_TYPES.RATE_LIMIT]: 'Too many requests. Please wait and try again.',
      [ERROR_TYPES.EXTERNAL_SERVICE]: 'External service is temporarily unavailable.',
      [ERROR_TYPES.PROCESSING]: 'An error occurred while processing your request.',
      [ERROR_TYPES.CONFIGURATION]: 'System configuration error. Please contact support.',
      [ERROR_TYPES.PLUGIN]: 'Plugin error occurred. Please try again.',
      [ERROR_TYPES.SYSTEM]: 'System error occurred. Please contact support.',
      [ERROR_TYPES.NETWORK]: 'Network error. Please check your connection.',
      [ERROR_TYPES.DATABASE]: 'Database error. Please try again later.',
      [ERROR_TYPES.CACHE]: 'Cache error. The operation may be slower than usual.',
      [ERROR_TYPES.UNKNOWN]: 'An unexpected error occurred. Please try again.'
    }
    
    return friendlyMessages[type] || 'An error occurred. Please try again.'
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      type: this.type,
      code: this.code,
      details: this.details,
      timestamp: this.timestamp,
      severity: this.severity,
      recoverable: this.recoverable,
      userFriendly: this.userFriendly,
      stack: this.stack
    }
  }
}

class ErrorHandler {
  constructor({ config, cache, pythonBridge }) {
    this.config = config
    this.cache = cache
    this.pythonBridge = pythonBridge
    
    // Error tracking
    this.errorHistory = []
    this.errorCounts = new Map()
    this.circuitBreakers = new Map()
    this.retryAttempts = new Map()
    
    // Recovery strategies
    this.recoveryStrategies = new Map()
    this.fallbackHandlers = new Map()
    
    // Configuration
    this.maxErrorHistory = config?.error_handling?.max_history || 1000
    this.retryConfig = {
      maxAttempts: config?.error_handling?.retry?.max_attempts || 3,
      baseDelay: config?.error_handling?.retry?.base_delay || 1000,
      maxDelay: config?.error_handling?.retry?.max_delay || 30000,
      backoffMultiplier: config?.error_handling?.retry?.backoff_multiplier || 2
    }
    
    this.circuitBreakerConfig = {
      failureThreshold: config?.error_handling?.circuit_breaker?.failure_threshold || 5,
      resetTimeout: config?.error_handling?.circuit_breaker?.reset_timeout || 60000,
      monitoringPeriod: config?.error_handling?.circuit_breaker?.monitoring_period || 300000
    }
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('🛡️ Initializing Error Handler...')
    
    try {
      // Setup default recovery strategies
      this.setupDefaultRecoveryStrategies()
      
      // Setup default fallback handlers
      this.setupDefaultFallbackHandlers()
      
      // Load error history from cache
      await this.loadErrorHistory()
      
      // Setup periodic cleanup
      this.setupPeriodicCleanup()
      
      this.isInitialized = true
      logger.info('✅ Error Handler initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Error Handler:', error)
      throw error
    }
  }

  async handleError(error, context = {}) {
    if (!this.isInitialized) {
      logger.error('Error Handler not initialized, using basic handling')
      return this.basicErrorHandling(error, context)
    }
    
    try {
      // Normalize error to JAEGISError
      const normalizedError = this.normalizeError(error, context)
      
      // Record error
      this.recordError(normalizedError, context)
      
      // Log error with appropriate level
      this.logError(normalizedError, context)
      
      // Determine recovery strategy
      const strategy = this.determineRecoveryStrategy(normalizedError, context)
      
      // Attempt recovery
      const recoveryResult = await this.attemptRecovery(normalizedError, strategy, context)
      
      // Return error response
      return this.createErrorResponse(normalizedError, recoveryResult, context)
      
    } catch (handlingError) {
      logger.error('Error in error handling:', handlingError)
      return this.basicErrorHandling(error, context)
    }
  }

  normalizeError(error, context) {
    if (error instanceof JAEGISError) {
      return error
    }
    
    // Determine error type based on error properties
    let type = ERROR_TYPES.UNKNOWN
    let code = null
    let details = {}
    
    if (error.name === 'ValidationError' || error.message.includes('validation')) {
      type = ERROR_TYPES.VALIDATION
    } else if (error.name === 'TimeoutError' || error.code === 'ETIMEDOUT') {
      type = ERROR_TYPES.TIMEOUT
    } else if (error.code === 'ENOTFOUND' || error.code === 'ECONNREFUSED') {
      type = ERROR_TYPES.NETWORK
    } else if (error.message.includes('rate limit')) {
      type = ERROR_TYPES.RATE_LIMIT
    } else if (error.message.includes('authentication')) {
      type = ERROR_TYPES.AUTHENTICATION
    } else if (error.message.includes('authorization') || error.message.includes('permission')) {
      type = ERROR_TYPES.AUTHORIZATION
    } else if (error.message.includes('not found')) {
      type = ERROR_TYPES.NOT_FOUND
    } else if (error.message.includes('plugin')) {
      type = ERROR_TYPES.PLUGIN
    } else if (error.message.includes('configuration') || error.message.includes('config')) {
      type = ERROR_TYPES.CONFIGURATION
    }
    
    // Extract additional details
    if (error.code) {
      code = error.code
    }
    
    if (error.details) {
      details = error.details
    }
    
    // Add context information
    details.originalError = {
      name: error.name,
      message: error.message,
      stack: error.stack
    }
    
    details.context = context
    
    return new JAEGISError(error.message, type, code, details)
  }

  recordError(error, context) {
    // Add to error history
    const errorRecord = {
      error: error.toJSON(),
      context,
      timestamp: Date.now(),
      id: this.generateErrorId()
    }
    
    this.errorHistory.push(errorRecord)
    
    // Maintain history size
    if (this.errorHistory.length > this.maxErrorHistory) {
      this.errorHistory = this.errorHistory.slice(-this.maxErrorHistory)
    }
    
    // Update error counts
    const errorKey = `${error.type}:${error.code || 'unknown'}`
    this.errorCounts.set(errorKey, (this.errorCounts.get(errorKey) || 0) + 1)
    
    // Update circuit breaker state
    this.updateCircuitBreaker(error, context)
  }

  logError(error, context) {
    const logData = {
      type: error.type,
      code: error.code,
      severity: error.severity,
      recoverable: error.recoverable,
      context: context.command || context.plugin || 'unknown',
      executionId: context.executionId,
      userId: context.user
    }
    
    switch (error.severity) {
      case ERROR_SEVERITY.CRITICAL:
        logger.error('CRITICAL ERROR:', error.message, logData)
        break
      case ERROR_SEVERITY.HIGH:
        logger.error('HIGH SEVERITY ERROR:', error.message, logData)
        break
      case ERROR_SEVERITY.MEDIUM:
        logger.warn('MEDIUM SEVERITY ERROR:', error.message, logData)
        break
      case ERROR_SEVERITY.LOW:
        logger.info('LOW SEVERITY ERROR:', error.message, logData)
        break
      default:
        logger.error('ERROR:', error.message, logData)
    }
  }

  determineRecoveryStrategy(error, context) {
    // Check for custom recovery strategy
    const customStrategy = this.recoveryStrategies.get(error.type)
    if (customStrategy) {
      return customStrategy
    }
    
    // Default strategy based on error type and recoverability
    if (!error.recoverable) {
      return RECOVERY_STRATEGIES.FAIL_FAST
    }
    
    // Check circuit breaker state
    const circuitBreaker = this.getCircuitBreaker(error.type)
    if (circuitBreaker.state === 'OPEN') {
      return RECOVERY_STRATEGIES.CIRCUIT_BREAKER
    }
    
    // Determine strategy based on error type
    switch (error.type) {
      case ERROR_TYPES.TIMEOUT:
      case ERROR_TYPES.NETWORK:
      case ERROR_TYPES.EXTERNAL_SERVICE:
        return RECOVERY_STRATEGIES.RETRY
      case ERROR_TYPES.RATE_LIMIT:
        return RECOVERY_STRATEGIES.GRACEFUL_DEGRADATION
      case ERROR_TYPES.CACHE:
        return RECOVERY_STRATEGIES.FALLBACK
      case ERROR_TYPES.VALIDATION:
      case ERROR_TYPES.NOT_FOUND:
        return RECOVERY_STRATEGIES.FAIL_FAST
      default:
        return RECOVERY_STRATEGIES.RETRY
    }
  }

  async attemptRecovery(error, strategy, context) {
    const recoveryContext = {
      error,
      strategy,
      context,
      attempt: 1,
      startTime: Date.now()
    }
    
    try {
      switch (strategy) {
        case RECOVERY_STRATEGIES.RETRY:
          return await this.retryRecovery(recoveryContext)
        case RECOVERY_STRATEGIES.FALLBACK:
          return await this.fallbackRecovery(recoveryContext)
        case RECOVERY_STRATEGIES.CIRCUIT_BREAKER:
          return await this.circuitBreakerRecovery(recoveryContext)
        case RECOVERY_STRATEGIES.GRACEFUL_DEGRADATION:
          return await this.gracefulDegradationRecovery(recoveryContext)
        case RECOVERY_STRATEGIES.FAIL_FAST:
          return await this.failFastRecovery(recoveryContext)
        case RECOVERY_STRATEGIES.IGNORE:
          return await this.ignoreRecovery(recoveryContext)
        default:
          return await this.failFastRecovery(recoveryContext)
      }
    } catch (recoveryError) {
      logger.error('Recovery attempt failed:', recoveryError)
      return {
        success: false,
        strategy,
        error: recoveryError.message,
        duration: Date.now() - recoveryContext.startTime
      }
    }
  }

  async retryRecovery(recoveryContext) {
    const { error, context } = recoveryContext
    const retryKey = `${error.type}:${context.command || context.plugin || 'unknown'}`
    
    // Get current retry count
    const currentAttempts = this.retryAttempts.get(retryKey) || 0
    
    if (currentAttempts >= this.retryConfig.maxAttempts) {
      // Max retries exceeded
      this.retryAttempts.delete(retryKey)
      return {
        success: false,
        strategy: RECOVERY_STRATEGIES.RETRY,
        reason: 'Max retry attempts exceeded',
        attempts: currentAttempts
      }
    }
    
    // Calculate delay with exponential backoff
    const delay = Math.min(
      this.retryConfig.baseDelay * Math.pow(this.retryConfig.backoffMultiplier, currentAttempts),
      this.retryConfig.maxDelay
    )
    
    // Update retry count
    this.retryAttempts.set(retryKey, currentAttempts + 1)
    
    // Wait before retry
    await this.sleep(delay)
    
    return {
      success: true,
      strategy: RECOVERY_STRATEGIES.RETRY,
      action: 'retry_scheduled',
      delay,
      attempt: currentAttempts + 1,
      maxAttempts: this.retryConfig.maxAttempts
    }
  }

  async fallbackRecovery(recoveryContext) {
    const { error, context } = recoveryContext
    
    // Look for fallback handler
    const fallbackHandler = this.fallbackHandlers.get(error.type)
    
    if (fallbackHandler) {
      try {
        const fallbackResult = await fallbackHandler(error, context)
        return {
          success: true,
          strategy: RECOVERY_STRATEGIES.FALLBACK,
          action: 'fallback_executed',
          result: fallbackResult
        }
      } catch (fallbackError) {
        return {
          success: false,
          strategy: RECOVERY_STRATEGIES.FALLBACK,
          reason: 'Fallback handler failed',
          error: fallbackError.message
        }
      }
    }
    
    return {
      success: false,
      strategy: RECOVERY_STRATEGIES.FALLBACK,
      reason: 'No fallback handler available'
    }
  }

  async circuitBreakerRecovery(recoveryContext) {
    const { error } = recoveryContext
    const circuitBreaker = this.getCircuitBreaker(error.type)
    
    return {
      success: false,
      strategy: RECOVERY_STRATEGIES.CIRCUIT_BREAKER,
      action: 'circuit_breaker_open',
      state: circuitBreaker.state,
      resetTime: circuitBreaker.resetTime,
      reason: 'Circuit breaker is open, requests blocked'
    }
  }

  async gracefulDegradationRecovery(recoveryContext) {
    const { error, context } = recoveryContext
    
    // Provide degraded functionality
    let degradedResponse = null
    
    switch (error.type) {
      case ERROR_TYPES.RATE_LIMIT:
        degradedResponse = {
          message: 'Service temporarily limited. Basic functionality available.',
          limited: true,
          retryAfter: 60000 // 1 minute
        }
        break
      case ERROR_TYPES.EXTERNAL_SERVICE:
        degradedResponse = {
          message: 'External service unavailable. Using cached data.',
          cached: true,
          stale: true
        }
        break
      default:
        degradedResponse = {
          message: 'Service degraded. Limited functionality available.',
          degraded: true
        }
    }
    
    return {
      success: true,
      strategy: RECOVERY_STRATEGIES.GRACEFUL_DEGRADATION,
      action: 'degraded_service',
      response: degradedResponse
    }
  }

  async failFastRecovery(recoveryContext) {
    return {
      success: false,
      strategy: RECOVERY_STRATEGIES.FAIL_FAST,
      action: 'fail_fast',
      reason: 'Error is not recoverable'
    }
  }

  async ignoreRecovery(recoveryContext) {
    return {
      success: true,
      strategy: RECOVERY_STRATEGIES.IGNORE,
      action: 'ignored',
      reason: 'Error ignored as configured'
    }
  }

  createErrorResponse(error, recoveryResult, context) {
    const response = {
      success: false,
      error: {
        message: error.userFriendly,
        type: error.type,
        code: error.code,
        severity: error.severity,
        timestamp: error.timestamp,
        recoverable: error.recoverable
      },
      recovery: recoveryResult,
      suggestions: this.generateSuggestions(error, context),
      support: this.generateSupportInfo(error, context)
    }
    
    // Add debug information if enabled
    if (this.config?.system?.debug) {
      response.debug = {
        originalMessage: error.message,
        stack: error.stack,
        details: error.details,
        context
      }
    }
    
    return response
  }

  generateSuggestions(error, context) {
    const suggestions = []
    
    switch (error.type) {
      case ERROR_TYPES.VALIDATION:
        suggestions.push('Check your input parameters and try again')
        suggestions.push('Use /help <command> for parameter information')
        break
      case ERROR_TYPES.NOT_FOUND:
        suggestions.push('Check the command spelling')
        suggestions.push('Use /help to see available commands')
        break
      case ERROR_TYPES.TIMEOUT:
        suggestions.push('Try again in a few moments')
        suggestions.push('Check your network connection')
        break
      case ERROR_TYPES.RATE_LIMIT:
        suggestions.push('Wait a moment before trying again')
        suggestions.push('Reduce the frequency of requests')
        break
      case ERROR_TYPES.EXTERNAL_SERVICE:
        suggestions.push('Try again later')
        suggestions.push('Check service status')
        break
      default:
        suggestions.push('Try again')
        suggestions.push('Contact support if the problem persists')
    }
    
    return suggestions
  }

  generateSupportInfo(error, context) {
    return {
      errorId: this.generateErrorId(),
      timestamp: error.timestamp,
      severity: error.severity,
      contactInfo: 'For support, please provide the error ID and timestamp',
      documentation: '/help troubleshooting'
    }
  }

  // Circuit breaker implementation
  getCircuitBreaker(errorType) {
    if (!this.circuitBreakers.has(errorType)) {
      this.circuitBreakers.set(errorType, {
        state: 'CLOSED', // CLOSED, OPEN, HALF_OPEN
        failureCount: 0,
        lastFailureTime: null,
        resetTime: null
      })
    }
    
    return this.circuitBreakers.get(errorType)
  }

  updateCircuitBreaker(error, context) {
    const circuitBreaker = this.getCircuitBreaker(error.type)
    
    if (error.severity === ERROR_SEVERITY.HIGH || error.severity === ERROR_SEVERITY.CRITICAL) {
      circuitBreaker.failureCount++
      circuitBreaker.lastFailureTime = Date.now()
      
      if (circuitBreaker.failureCount >= this.circuitBreakerConfig.failureThreshold) {
        circuitBreaker.state = 'OPEN'
        circuitBreaker.resetTime = Date.now() + this.circuitBreakerConfig.resetTimeout
        
        logger.warn(`Circuit breaker opened for ${error.type}`, {
          failureCount: circuitBreaker.failureCount,
          resetTime: circuitBreaker.resetTime
        })
      }
    }
    
    // Check if circuit breaker should reset
    if (circuitBreaker.state === 'OPEN' && Date.now() > circuitBreaker.resetTime) {
      circuitBreaker.state = 'HALF_OPEN'
      circuitBreaker.failureCount = 0
      
      logger.info(`Circuit breaker reset to HALF_OPEN for ${error.type}`)
    }
  }

  // Setup methods
  setupDefaultRecoveryStrategies() {
    // Set default recovery strategies for error types
    this.recoveryStrategies.set(ERROR_TYPES.TIMEOUT, RECOVERY_STRATEGIES.RETRY)
    this.recoveryStrategies.set(ERROR_TYPES.NETWORK, RECOVERY_STRATEGIES.RETRY)
    this.recoveryStrategies.set(ERROR_TYPES.EXTERNAL_SERVICE, RECOVERY_STRATEGIES.RETRY)
    this.recoveryStrategies.set(ERROR_TYPES.RATE_LIMIT, RECOVERY_STRATEGIES.GRACEFUL_DEGRADATION)
    this.recoveryStrategies.set(ERROR_TYPES.CACHE, RECOVERY_STRATEGIES.FALLBACK)
    this.recoveryStrategies.set(ERROR_TYPES.VALIDATION, RECOVERY_STRATEGIES.FAIL_FAST)
    this.recoveryStrategies.set(ERROR_TYPES.NOT_FOUND, RECOVERY_STRATEGIES.FAIL_FAST)
  }

  setupDefaultFallbackHandlers() {
    // Cache fallback handler
    this.fallbackHandlers.set(ERROR_TYPES.CACHE, async (error, context) => {
      logger.info('Using cache fallback handler')
      return {
        message: 'Cache unavailable, using direct processing',
        fallback: true
      }
    })
    
    // External service fallback handler
    this.fallbackHandlers.set(ERROR_TYPES.EXTERNAL_SERVICE, async (error, context) => {
      logger.info('Using external service fallback handler')
      
      // Try to get cached data
      if (this.cache) {
        try {
          const cached = await this.cache.get(`fallback:${context.command}`)
          if (cached) {
            return {
              message: 'Using cached data due to service unavailability',
              data: cached,
              fallback: true,
              stale: true
            }
          }
        } catch (cacheError) {
          logger.warn('Cache fallback also failed:', cacheError)
        }
      }
      
      return {
        message: 'External service unavailable and no cached data available',
        fallback: true,
        unavailable: true
      }
    })
  }

  async loadErrorHistory() {
    try {
      const cached = await this.cache.get('error_handler_history')
      if (cached) {
        this.errorHistory = cached.errorHistory || []
        this.errorCounts = new Map(cached.errorCounts || [])
        logger.info(`📊 Loaded ${this.errorHistory.length} error records from cache`)
      }
    } catch (error) {
      logger.warn('Failed to load error history from cache:', error.message)
    }
  }

  async saveErrorHistory() {
    try {
      const data = {
        errorHistory: this.errorHistory,
        errorCounts: Array.from(this.errorCounts.entries()),
        timestamp: Date.now()
      }
      
      await this.cache.set('error_handler_history', data, 86400000) // 24 hours
      logger.debug('💾 Error history saved to cache')
    } catch (error) {
      logger.warn('Failed to save error history to cache:', error.message)
    }
  }

  setupPeriodicCleanup() {
    // Save error history periodically
    setInterval(() => {
      this.saveErrorHistory()
    }, 300000) // Every 5 minutes
    
    // Clean up old retry attempts
    setInterval(() => {
      this.cleanupRetryAttempts()
    }, 60000) // Every minute
    
    // Reset circuit breakers if needed
    setInterval(() => {
      this.checkCircuitBreakers()
    }, 30000) // Every 30 seconds
  }

  cleanupRetryAttempts() {
    // Remove old retry attempts (older than 1 hour)
    const cutoff = Date.now() - 3600000
    
    for (const [key, attempts] of this.retryAttempts.entries()) {
      if (attempts.lastAttempt && attempts.lastAttempt < cutoff) {
        this.retryAttempts.delete(key)
      }
    }
  }

  checkCircuitBreakers() {
    for (const [errorType, circuitBreaker] of this.circuitBreakers.entries()) {
      if (circuitBreaker.state === 'OPEN' && Date.now() > circuitBreaker.resetTime) {
        circuitBreaker.state = 'HALF_OPEN'
        circuitBreaker.failureCount = 0
        logger.info(`Circuit breaker reset to HALF_OPEN for ${errorType}`)
      }
    }
  }

  // Utility methods
  basicErrorHandling(error, context) {
    logger.error('Basic error handling:', error.message, { context })
    
    return {
      success: false,
      error: {
        message: 'An error occurred. Please try again.',
        type: 'UNKNOWN_ERROR',
        timestamp: Date.now()
      },
      suggestions: [
        'Try again',
        'Check your input',
        'Contact support if the problem persists'
      ]
    }
  }

  generateErrorId() {
    return `err_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  // Statistics and monitoring
  getErrorStats() {
    const stats = {
      totalErrors: this.errorHistory.length,
      errorsByType: {},
      errorsBySeverity: {},
      recentErrors: this.errorHistory.slice(-10),
      circuitBreakerStates: {},
      retryAttempts: this.retryAttempts.size
    }
    
    // Count errors by type
    for (const [errorKey, count] of this.errorCounts.entries()) {
      const [type] = errorKey.split(':')
      stats.errorsByType[type] = (stats.errorsByType[type] || 0) + count
    }
    
    // Count errors by severity
    this.errorHistory.forEach(record => {
      const severity = record.error.severity
      stats.errorsBySeverity[severity] = (stats.errorsBySeverity[severity] || 0) + 1
    })
    
    // Circuit breaker states
    for (const [errorType, circuitBreaker] of this.circuitBreakers.entries()) {
      stats.circuitBreakerStates[errorType] = circuitBreaker.state
    }
    
    return stats
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Error Handler...')
    
    // Save final error history
    await this.saveErrorHistory()
    
    // Clear data structures
    this.errorHistory.length = 0
    this.errorCounts.clear()
    this.circuitBreakers.clear()
    this.retryAttempts.clear()
    this.recoveryStrategies.clear()
    this.fallbackHandlers.clear()
    
    this.isInitialized = false
    logger.info('✅ Error Handler cleanup complete')
  }
}

// Export error classes and handler
module.exports = {
  ErrorHandler,
  JAEGISError,
  ERROR_TYPES,
  ERROR_SEVERITY,
  RECOVERY_STRATEGIES
}