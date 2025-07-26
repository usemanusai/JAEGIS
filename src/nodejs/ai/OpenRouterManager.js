/**
 * JAEGIS OpenRouter.ai Manager
 * Advanced API management system for OpenRouter.ai integration
 * Handles intelligent key rotation, rate limiting, and model selection
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const axios = require('axios')
const logger = require('../utils/logger')

// OpenRouter API Configuration
const OPENROUTER_CONFIG = {
  baseURL: 'https://openrouter.ai/api/v1',
  endpoints: {
    chat: '/chat/completions',
    models: '/models',
    usage: '/auth/key',
    credits: '/auth/credits'
  },
  limits: {
    freeDaily: 50,        // 50 messages per free key per day
    paidDaily: 2000,      // 2000 messages per paid key per day
    requestsPerMinute: 20, // Rate limit per key
    maxRetries: 3,
    timeoutMs: 30000
  }
}

// Model Categories and Configurations
const MODEL_CATEGORIES = {
  reasoning: {
    primary: 'deepseek/deepseek-r1-0528:free',
    fallback: 'deepseek/deepseek-chat-v3-0324:free',
    description: 'Advanced reasoning and problem-solving tasks'
  },
  chat: {
    primary: 'deepseek/deepseek-chat-v3-0324:free',
    fallback: 'qwen/qwen3-coder:free',
    description: 'General conversation and assistance'
  },
  coding: {
    primary: 'qwen/qwen3-coder:free',
    fallback: 'deepseek/deepseek-chat-v3-0324:free',
    description: 'Code generation and programming tasks'
  },
  analysis: {
    primary: 'deepseek/deepseek-chat-v3-0324:free',
    fallback: 'deepseek/deepseek-r1-0528:free',
    description: 'Data analysis and interpretation'
  }
}

// Key Status Types
const KEY_STATUS = {
  ACTIVE: 'active',
  EXHAUSTED: 'exhausted',
  ERROR: 'error',
  COOLING_DOWN: 'cooling_down',
  DISABLED: 'disabled'
}

class OpenRouterManager {
  constructor({ config, cache, errorHandler, performanceMonitor }) {
    this.config = config
    this.cache = cache
    this.errorHandler = errorHandler
    this.performanceMonitor = performanceMonitor
    
    // API Key Management
    this.apiKeys = new Map()
    this.keyRotationIndex = 0
    this.keyUsageStats = new Map()
    this.dailyResetTime = null
    
    // Request Management
    this.requestQueue = []
    this.activeRequests = new Map()
    this.rateLimiters = new Map()
    
    // Model Management
    this.availableModels = new Map()
    this.modelPerformance = new Map()
    this.modelUsageStats = new Map()
    
    // Configuration
    this.aiConfig = {
      enabled: config?.ai?.enabled !== false,
      maxConcurrentRequests: config?.ai?.max_concurrent_requests || 10,
      defaultTimeout: config?.ai?.default_timeout || 30000,
      retryDelay: config?.ai?.retry_delay || 1000,
      quotaWarningThreshold: config?.ai?.quota_warning_threshold || 0.8,
      autoKeyRotation: config?.ai?.auto_key_rotation !== false,
      enableModelDiscovery: config?.ai?.enable_model_discovery !== false,
      cacheResponses: config?.ai?.cache_responses !== false,
      cacheTTL: config?.ai?.cache_ttl || 3600000 // 1 hour
    }
    
    // Monitoring
    this.metrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      totalTokensUsed: 0,
      averageResponseTime: 0,
      keyRotations: 0,
      quotaExhausted: 0
    }
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('🤖 Initializing OpenRouter.ai Manager...')
    
    try {
      // Load API keys
      await this.loadAPIKeys()
      
      // Initialize rate limiters
      this.initializeRateLimiters()
      
      // Discover available models
      if (this.aiConfig.enableModelDiscovery) {
        await this.discoverModels()
      }
      
      // Setup daily reset tracking
      this.setupDailyReset()
      
      // Start background processes
      this.startBackgroundProcesses()
      
      this.isInitialized = true
      logger.info(`✅ OpenRouter.ai Manager initialized with ${this.apiKeys.size} API keys`)
      
    } catch (error) {
      logger.error('❌ Failed to initialize OpenRouter.ai Manager:', error)
      throw error
    }
  }

  async loadAPIKeys() {
    const keys = this.config.ai?.openrouter?.keys || []
    
    if (keys.length === 0) {
      throw new Error('No OpenRouter.ai API keys configured')
    }
    
    for (const keyConfig of keys) {
      const keyData = {
        key: keyConfig.key,
        tier: keyConfig.tier || 'free', // 'free' or 'paid'
        dailyLimit: keyConfig.tier === 'paid' ? OPENROUTER_CONFIG.limits.paidDaily : OPENROUTER_CONFIG.limits.freeDaily,
        usedToday: 0,
        status: KEY_STATUS.ACTIVE,
        lastUsed: null,
        errorCount: 0,
        successCount: 0,
        averageResponseTime: 0,
        createdAt: Date.now()
      }
      
      this.apiKeys.set(keyConfig.key, keyData)
      this.keyUsageStats.set(keyConfig.key, {
        daily: [],
        hourly: [],
        errors: [],
        performance: []
      })
    }
    
    logger.info(`📋 Loaded ${this.apiKeys.size} API keys (${this.getKeysByTier('free').length} free, ${this.getKeysByTier('paid').length} paid)`)
  }

  initializeRateLimiters() {
    for (const [keyId] of this.apiKeys) {
      this.rateLimiters.set(keyId, {
        requests: [],
        lastRequest: 0
      })
    }
  }

  async discoverModels() {
    logger.info('🔍 Discovering available OpenRouter models...')
    
    try {
      const activeKey = this.getNextAvailableKey()
      if (!activeKey) {
        logger.warn('No available keys for model discovery')
        return
      }
      
      const response = await this.makeRequest({
        method: 'GET',
        url: `${OPENROUTER_CONFIG.baseURL}${OPENROUTER_CONFIG.endpoints.models}`,
        headers: {
          'Authorization': `Bearer ${activeKey.key}`,
          'HTTP-Referer': 'https://jaegis.ai',
          'X-Title': 'JAEGIS AI System'
        }
      })
      
      if (response.data && response.data.data) {
        for (const model of response.data.data) {
          this.availableModels.set(model.id, {
            id: model.id,
            name: model.name || model.id,
            description: model.description || '',
            context_length: model.context_length || 4096,
            pricing: model.pricing || {},
            top_provider: model.top_provider || {},
            discovered_at: Date.now()
          })
        }
        
        logger.info(`🎯 Discovered ${this.availableModels.size} available models`)
      }
      
    } catch (error) {
      logger.warn('Failed to discover models:', error.message)
    }
  }

  setupDailyReset() {
    // Calculate next midnight UTC
    const now = new Date()
    const tomorrow = new Date(now)
    tomorrow.setUTCDate(tomorrow.getUTCDate() + 1)
    tomorrow.setUTCHours(0, 0, 0, 0)
    
    this.dailyResetTime = tomorrow.getTime()
    
    // Schedule daily reset
    const timeUntilReset = this.dailyResetTime - Date.now()
    setTimeout(() => {
      this.performDailyReset()
      // Schedule recurring daily resets
      setInterval(() => this.performDailyReset(), 24 * 60 * 60 * 1000)
    }, timeUntilReset)
    
    logger.info(`⏰ Daily quota reset scheduled for ${tomorrow.toISOString()}`)
  }

  performDailyReset() {
    logger.info('🔄 Performing daily quota reset...')
    
    let resetCount = 0
    for (const [keyId, keyData] of this.apiKeys) {
      if (keyData.status === KEY_STATUS.EXHAUSTED) {
        keyData.status = KEY_STATUS.ACTIVE
        resetCount++
      }
      keyData.usedToday = 0
      keyData.errorCount = 0
    }
    
    // Update daily reset time
    const tomorrow = new Date()
    tomorrow.setUTCDate(tomorrow.getUTCDate() + 1)
    tomorrow.setUTCHours(0, 0, 0, 0)
    this.dailyResetTime = tomorrow.getTime()
    
    logger.info(`✅ Daily reset complete: ${resetCount} keys reactivated`)
  }

  startBackgroundProcesses() {
    // Key health monitoring
    setInterval(() => {
      this.monitorKeyHealth()
    }, 60000) // Every minute
    
    // Usage statistics cleanup
    setInterval(() => {
      this.cleanupUsageStats()
    }, 3600000) // Every hour
    
    // Performance optimization
    setInterval(() => {
      this.optimizePerformance()
    }, 300000) // Every 5 minutes
  }

  async generateCompletion(prompt, options = {}) {
    if (!this.isInitialized) {
      throw new Error('OpenRouter Manager not initialized')
    }
    
    const startTime = Date.now()
    const requestId = this.generateRequestId()
    
    try {
      // Validate input
      await this.validateInput(prompt, options)
      
      // Select appropriate model
      const model = this.selectModel(options.category || 'chat', options.model)
      
      // Get available API key
      const apiKey = this.getNextAvailableKey(options.priority)
      if (!apiKey) {
        throw new Error('No available API keys with remaining quota')
      }
      
      // Check cache if enabled
      if (this.aiConfig.cacheResponses) {
        const cacheKey = this.generateCacheKey(prompt, model, options)
        const cached = await this.cache.get(cacheKey)
        if (cached) {
          logger.debug(`📋 Cache hit for request ${requestId}`)
          return {
            ...cached,
            cached: true,
            requestId
          }
        }
      }
      
      // Prepare request
      const requestData = this.prepareRequest(prompt, model, options)
      
      // Make API request
      const response = await this.makeOpenRouterRequest(apiKey, requestData, requestId)
      
      // Process response
      const result = this.processResponse(response, requestId, startTime)
      
      // Update statistics
      this.updateUsageStats(apiKey.key, result, Date.now() - startTime)
      
      // Cache response if enabled
      if (this.aiConfig.cacheResponses && result.success) {
        const cacheKey = this.generateCacheKey(prompt, model, options)
        await this.cache.set(cacheKey, result, this.aiConfig.cacheTTL)
      }
      
      return result
      
    } catch (error) {
      const duration = Date.now() - startTime
      await this.handleRequestError(error, requestId, duration)
      throw error
    }
  }

  selectModel(category, specificModel = null) {
    if (specificModel) {
      // Use specific model if provided and available
      if (this.availableModels.has(specificModel)) {
        return specificModel
      }
      logger.warn(`Requested model ${specificModel} not available, falling back to category default`)
    }
    
    const categoryConfig = MODEL_CATEGORIES[category]
    if (!categoryConfig) {
      logger.warn(`Unknown category ${category}, using chat default`)
      return MODEL_CATEGORIES.chat.primary
    }
    
    // Check if primary model is available
    if (this.availableModels.has(categoryConfig.primary)) {
      return categoryConfig.primary
    }
    
    // Fall back to secondary model
    if (this.availableModels.has(categoryConfig.fallback)) {
      logger.warn(`Primary model ${categoryConfig.primary} unavailable, using fallback`)
      return categoryConfig.fallback
    }
    
    // Use any available model as last resort
    const availableModel = Array.from(this.availableModels.keys())[0]
    if (availableModel) {
      logger.warn(`Category models unavailable, using ${availableModel}`)
      return availableModel
    }
    
    throw new Error('No available models found')
  }

  getNextAvailableKey(priority = 'normal') {
    const availableKeys = Array.from(this.apiKeys.values())
      .filter(key => key.status === KEY_STATUS.ACTIVE && key.usedToday < key.dailyLimit)
      .sort((a, b) => {
        // Prioritize by tier (paid first), then by usage
        if (a.tier !== b.tier) {
          return a.tier === 'paid' ? -1 : 1
        }
        return a.usedToday - b.usedToday
      })
    
    if (availableKeys.length === 0) {
      return null
    }
    
    // For high priority requests, use the best available key
    if (priority === 'high') {
      return availableKeys[0]
    }
    
    // For normal priority, use round-robin among available keys
    const keyIndex = this.keyRotationIndex % availableKeys.length
    this.keyRotationIndex++
    
    return availableKeys[keyIndex]
  }

  async makeOpenRouterRequest(apiKey, requestData, requestId) {
    // Check rate limiting
    await this.checkRateLimit(apiKey.key)
    
    // Mark request as active
    this.activeRequests.set(requestId, {
      keyId: apiKey.key,
      startTime: Date.now(),
      model: requestData.model
    })
    
    try {
      const response = await axios({
        method: 'POST',
        url: `${OPENROUTER_CONFIG.baseURL}${OPENROUTER_CONFIG.endpoints.chat}`,
        headers: {
          'Authorization': `Bearer ${apiKey.key}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://jaegis.ai',
          'X-Title': 'JAEGIS AI System'
        },
        data: requestData,
        timeout: this.aiConfig.defaultTimeout
      })
      
      // Update key usage
      apiKey.usedToday++
      apiKey.lastUsed = Date.now()
      apiKey.successCount++
      
      // Check if key is exhausted
      if (apiKey.usedToday >= apiKey.dailyLimit) {
        apiKey.status = KEY_STATUS.EXHAUSTED
        logger.warn(`🔑 API key exhausted: ${apiKey.key.substring(0, 8)}...`)
      }
      
      return response
      
    } finally {
      this.activeRequests.delete(requestId)
    }
  }

  async checkRateLimit(keyId) {
    const rateLimiter = this.rateLimiters.get(keyId)
    if (!rateLimiter) return
    
    const now = Date.now()
    const oneMinute = 60 * 1000
    
    // Remove old requests
    rateLimiter.requests = rateLimiter.requests.filter(time => now - time < oneMinute)
    
    // Check if rate limit exceeded
    if (rateLimiter.requests.length >= OPENROUTER_CONFIG.limits.requestsPerMinute) {
      const oldestRequest = Math.min(...rateLimiter.requests)
      const waitTime = oneMinute - (now - oldestRequest)
      
      logger.debug(`⏳ Rate limit reached for key, waiting ${waitTime}ms`)
      await this.sleep(waitTime)
    }
    
    // Add current request
    rateLimiter.requests.push(now)
    rateLimiter.lastRequest = now
  }

  prepareRequest(prompt, model, options) {
    const requestData = {
      model,
      messages: [],
      max_tokens: options.maxTokens || 1000,
      temperature: options.temperature || 0.7,
      top_p: options.topP || 0.9,
      frequency_penalty: options.frequencyPenalty || 0,
      presence_penalty: options.presencePenalty || 0,
      stream: false
    }
    
    // Handle different prompt formats
    if (typeof prompt === 'string') {
      requestData.messages = [{ role: 'user', content: prompt }]
    } else if (Array.isArray(prompt)) {
      requestData.messages = prompt
    } else if (prompt.messages) {
      requestData.messages = prompt.messages
    }
    
    // Add system message if provided
    if (options.systemMessage) {
      requestData.messages.unshift({ role: 'system', content: options.systemMessage })
    }
    
    return requestData
  }

  processResponse(response, requestId, startTime) {
    const duration = Date.now() - startTime
    
    if (!response.data || !response.data.choices || response.data.choices.length === 0) {
      throw new Error('Invalid response format from OpenRouter')
    }
    
    const choice = response.data.choices[0]
    const usage = response.data.usage || {}
    
    // Update metrics
    this.metrics.totalRequests++
    this.metrics.successfulRequests++
    this.metrics.totalTokensUsed += usage.total_tokens || 0
    this.metrics.averageResponseTime = (this.metrics.averageResponseTime + duration) / 2
    
    return {
      success: true,
      requestId,
      content: choice.message?.content || choice.text || '',
      model: response.data.model,
      usage: {
        promptTokens: usage.prompt_tokens || 0,
        completionTokens: usage.completion_tokens || 0,
        totalTokens: usage.total_tokens || 0
      },
      finishReason: choice.finish_reason,
      duration,
      timestamp: Date.now(),
      cached: false
    }
  }

  async validateInput(prompt, options) {
    // Basic validation
    if (!prompt || (typeof prompt === 'string' && prompt.trim().length === 0)) {
      throw new Error('Prompt cannot be empty')
    }
    
    // Security validation if available
    if (this.errorHandler && this.errorHandler.securityValidator) {
      const validation = await this.errorHandler.securityValidator.validateInput(prompt, {
        operation: 'ai_request',
        source: 'openrouter'
      })
      
      if (!validation.valid) {
        throw new Error(`Security validation failed: ${validation.threats.map(t => t.message).join(', ')}`)
      }
    }
    
    // Size validation
    const promptText = typeof prompt === 'string' ? prompt : JSON.stringify(prompt)
    if (promptText.length > 100000) { // 100KB limit
      throw new Error('Prompt too large')
    }
  }

  generateCacheKey(prompt, model, options) {
    const promptText = typeof prompt === 'string' ? prompt : JSON.stringify(prompt)
    const optionsText = JSON.stringify({
      model,
      maxTokens: options.maxTokens,
      temperature: options.temperature,
      systemMessage: options.systemMessage
    })
    
    const crypto = require('crypto')
    return `ai_cache:${crypto.createHash('sha256').update(promptText + optionsText).digest('hex')}`
  }

  generateRequestId() {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  updateUsageStats(keyId, result, duration) {
    const stats = this.keyUsageStats.get(keyId)
    if (!stats) return
    
    const now = Date.now()
    const hour = Math.floor(now / 3600000) // Hour bucket
    
    // Update hourly stats
    const hourlyEntry = stats.hourly.find(h => h.hour === hour)
    if (hourlyEntry) {
      hourlyEntry.requests++
      hourlyEntry.tokens += result.usage?.totalTokens || 0
      hourlyEntry.totalDuration += duration
    } else {
      stats.hourly.push({
        hour,
        requests: 1,
        tokens: result.usage?.totalTokens || 0,
        totalDuration: duration,
        timestamp: now
      })
    }
    
    // Update daily stats
    const today = new Date().toISOString().split('T')[0]
    const dailyEntry = stats.daily.find(d => d.date === today)
    if (dailyEntry) {
      dailyEntry.requests++
      dailyEntry.tokens += result.usage?.totalTokens || 0
      dailyEntry.totalDuration += duration
    } else {
      stats.daily.push({
        date: today,
        requests: 1,
        tokens: result.usage?.totalTokens || 0,
        totalDuration: duration
      })
    }
    
    // Update performance stats
    stats.performance.push({
      timestamp: now,
      duration,
      tokens: result.usage?.totalTokens || 0,
      model: result.model,
      success: result.success
    })
    
    // Trim old data
    this.trimUsageStats(stats)
  }

  trimUsageStats(stats) {
    const oneWeek = 7 * 24 * 60 * 60 * 1000
    const cutoff = Date.now() - oneWeek
    
    stats.hourly = stats.hourly.filter(h => h.timestamp > cutoff)
    stats.performance = stats.performance.filter(p => p.timestamp > cutoff)
    
    // Keep only last 30 days of daily stats
    stats.daily = stats.daily.slice(-30)
  }

  async handleRequestError(error, requestId, duration) {
    this.metrics.totalRequests++
    this.metrics.failedRequests++
    
    logger.error(`❌ OpenRouter request ${requestId} failed:`, error.message)
    
    // Handle specific error types
    if (error.response) {
      const status = error.response.status
      const data = error.response.data
      
      if (status === 429) {
        // Rate limit exceeded
        logger.warn('🚫 Rate limit exceeded, implementing backoff')
        await this.handleRateLimit(error)
      } else if (status === 401) {
        // Invalid API key
        logger.error('🔑 Invalid API key detected')
        await this.handleInvalidKey(error)
      } else if (status === 402) {
        // Insufficient credits
        logger.warn('💳 Insufficient credits')
        await this.handleInsufficientCredits(error)
      }
    }
    
    // Use error handler if available
    if (this.errorHandler) {
      await this.errorHandler.handleError(error, {
        operation: 'openrouter_request',
        requestId,
        duration,
        service: 'openrouter'
      })
    }
  }

  async handleRateLimit(error) {
    // Implement exponential backoff
    const retryAfter = error.response?.headers['retry-after']
    const waitTime = retryAfter ? parseInt(retryAfter) * 1000 : 60000 // Default 1 minute
    
    logger.info(`⏳ Waiting ${waitTime}ms before retry due to rate limit`)
    await this.sleep(waitTime)
  }

  async handleInvalidKey(error) {
    // Mark key as disabled and rotate to next
    const requestData = this.activeRequests.get(error.config?.requestId)
    if (requestData) {
      const keyData = this.apiKeys.get(requestData.keyId)
      if (keyData) {
        keyData.status = KEY_STATUS.DISABLED
        keyData.errorCount++
        logger.warn(`🔑 Disabled invalid API key: ${requestData.keyId.substring(0, 8)}...`)
      }
    }
  }

  async handleInsufficientCredits(error) {
    // Mark key as exhausted
    const requestData = this.activeRequests.get(error.config?.requestId)
    if (requestData) {
      const keyData = this.apiKeys.get(requestData.keyId)
      if (keyData) {
        keyData.status = KEY_STATUS.EXHAUSTED
        logger.warn(`💳 API key exhausted: ${requestData.keyId.substring(0, 8)}...`)
      }
    }
  }

  monitorKeyHealth() {
    let healthyKeys = 0
    let exhaustedKeys = 0
    let errorKeys = 0
    
    for (const [keyId, keyData] of this.apiKeys) {
      switch (keyData.status) {
        case KEY_STATUS.ACTIVE:
          healthyKeys++
          break
        case KEY_STATUS.EXHAUSTED:
          exhaustedKeys++
          break
        case KEY_STATUS.ERROR:
        case KEY_STATUS.DISABLED:
          errorKeys++
          break
      }
      
      // Check for keys with high error rates
      if (keyData.errorCount > 10 && keyData.status === KEY_STATUS.ACTIVE) {
        keyData.status = KEY_STATUS.COOLING_DOWN
        setTimeout(() => {
          if (keyData.status === KEY_STATUS.COOLING_DOWN) {
            keyData.status = KEY_STATUS.ACTIVE
            keyData.errorCount = 0
          }
        }, 300000) // 5 minute cooldown
      }
    }
    
    // Log health summary
    if (healthyKeys === 0) {
      logger.error('🚨 No healthy API keys available!')
    } else if (healthyKeys < 3) {
      logger.warn(`⚠️ Low API key availability: ${healthyKeys} healthy, ${exhaustedKeys} exhausted, ${errorKeys} error`)
    }
  }

  cleanupUsageStats() {
    for (const [keyId, stats] of this.keyUsageStats) {
      this.trimUsageStats(stats)
    }
  }

  optimizePerformance() {
    // Analyze model performance and adjust preferences
    const modelStats = new Map()
    
    for (const [keyId, stats] of this.keyUsageStats) {
      for (const perf of stats.performance) {
        if (!modelStats.has(perf.model)) {
          modelStats.set(perf.model, {
            requests: 0,
            totalDuration: 0,
            successRate: 0,
            avgTokens: 0
          })
        }
        
        const modelStat = modelStats.get(perf.model)
        modelStat.requests++
        modelStat.totalDuration += perf.duration
        modelStat.successRate += perf.success ? 1 : 0
        modelStat.avgTokens += perf.tokens
      }
    }
    
    // Calculate averages and update model performance
    for (const [model, stats] of modelStats) {
      if (stats.requests > 0) {
        this.modelPerformance.set(model, {
          avgDuration: stats.totalDuration / stats.requests,
          successRate: (stats.successRate / stats.requests) * 100,
          avgTokens: stats.avgTokens / stats.requests,
          totalRequests: stats.requests,
          lastUpdated: Date.now()
        })
      }
    }
  }

  // Utility methods
  getKeysByTier(tier) {
    return Array.from(this.apiKeys.values()).filter(key => key.tier === tier)
  }

  getTotalDailyCapacity() {
    let total = 0
    for (const keyData of this.apiKeys.values()) {
      total += keyData.dailyLimit
    }
    return total
  }

  getRemainingDailyCapacity() {
    let remaining = 0
    for (const keyData of this.apiKeys.values()) {
      if (keyData.status === KEY_STATUS.ACTIVE) {
        remaining += Math.max(0, keyData.dailyLimit - keyData.usedToday)
      }
    }
    return remaining
  }

  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  // Statistics and reporting
  getUsageReport() {
    const totalCapacity = this.getTotalDailyCapacity()
    const remainingCapacity = this.getRemainingDailyCapacity()
    const usedCapacity = totalCapacity - remainingCapacity
    
    return {
      timestamp: Date.now(),
      capacity: {
        total: totalCapacity,
        used: usedCapacity,
        remaining: remainingCapacity,
        utilizationRate: totalCapacity > 0 ? (usedCapacity / totalCapacity * 100).toFixed(2) + '%' : '0%'
      },
      keys: {
        total: this.apiKeys.size,
        active: Array.from(this.apiKeys.values()).filter(k => k.status === KEY_STATUS.ACTIVE).length,
        exhausted: Array.from(this.apiKeys.values()).filter(k => k.status === KEY_STATUS.EXHAUSTED).length,
        error: Array.from(this.apiKeys.values()).filter(k => k.status === KEY_STATUS.ERROR).length
      },
      metrics: { ...this.metrics },
      models: {
        available: this.availableModels.size,
        performance: Object.fromEntries(this.modelPerformance)
      },
      nextReset: this.dailyResetTime ? new Date(this.dailyResetTime).toISOString() : null
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up OpenRouter.ai Manager...')
    
    // Cancel active requests
    for (const [requestId] of this.activeRequests) {
      this.activeRequests.delete(requestId)
    }
    
    // Clear data structures
    this.apiKeys.clear()
    this.keyUsageStats.clear()
    this.rateLimiters.clear()
    this.availableModels.clear()
    this.modelPerformance.clear()
    this.requestQueue.length = 0
    
    this.isInitialized = false
    logger.info('✅ OpenRouter.ai Manager cleanup complete')
  }
}

module.exports = {
  OpenRouterManager,
  MODEL_CATEGORIES,
  KEY_STATUS,
  OPENROUTER_CONFIG
}