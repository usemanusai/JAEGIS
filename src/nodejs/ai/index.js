/**
 * JAEGIS AI System Integration
 * Main orchestration module for all AI components
 * Provides unified interface and seamless integration with existing JAEGIS system
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

// Import AI components
const { OpenRouterManager } = require('./OpenRouterManager')
const { RedisAIManager } = require('./RedisAIManager')
const { AutonomousLearningEngine } = require('./AutonomousLearningEngine')
const { BackgroundProcessManager } = require('./BackgroundProcessManager')
const { AIIntegrationBridge } = require('./AIIntegrationBridge')
const { AIMonitoringDashboard } = require('./AIMonitoringDashboard')

// System states
const SYSTEM_STATES = {
  INITIALIZING: 'initializing',
  READY: 'ready',
  RUNNING: 'running',
  DEGRADED: 'degraded',
  ERROR: 'error',
  SHUTDOWN: 'shutdown'
}

// Integration modes
const INTEGRATION_MODES = {
  STANDALONE: 'standalone',
  INTEGRATED: 'integrated',
  ENHANCED: 'enhanced',
  AUTONOMOUS: 'autonomous'
}

class JAEGISAISystem {
  constructor(config = {}) {
    this.config = config
    
    // System state
    this.state = SYSTEM_STATES.INITIALIZING
    this.integrationMode = config.ai?.integration_mode || INTEGRATION_MODES.ENHANCED
    this.startTime = Date.now()
    
    // AI Components
    this.components = {
      openRouterManager: null,
      redisAIManager: null,
      autonomousLearningEngine: null,
      backgroundProcessManager: null,
      aiIntegrationBridge: null,
      aiMonitoringDashboard: null
    }
    
    // Existing JAEGIS components (will be injected)
    this.jaegisComponents = {
      commandRouter: null,
      commandExecutor: null,
      cacheManager: null,
      decisionEngine: null,
      errorHandler: null,
      performanceMonitor: null,
      contextManager: null,
      responseFormatter: null,
      securityValidator: null
    }
    
    // System configuration
    this.systemConfig = {
      enabled: config.ai?.enabled !== false,
      autoStart: config.ai?.auto_start !== false,
      gracefulShutdown: config.ai?.graceful_shutdown !== false,
      healthCheckInterval: config.ai?.health_check_interval || 60000, // 1 minute
      maxInitializationTime: config.ai?.max_initialization_time || 120000, // 2 minutes
      enableMetrics: config.ai?.enable_metrics !== false,
      enableDashboard: config.ai?.enable_dashboard !== false,
      enableLearning: config.ai?.enable_learning !== false,
      enableBackgroundProcessing: config.ai?.enable_background_processing !== false
    }
    
    // System metrics
    this.metrics = {
      initializationTime: 0,
      uptime: 0,
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      componentsInitialized: 0,
      lastHealthCheck: 0,
      performanceScore: 0
    }
    
    // Event handlers
    this.eventHandlers = new Map()
    
    // Health monitoring
    this.healthMonitor = null
    
    this.isInitialized = false
  }

  async initialize(jaegisComponents = {}) {
    const initStartTime = Date.now()
    
    try {
      logger.info('🚀 Initializing JAEGIS AI System...')
      
      // Validate system requirements
      await this.validateSystemRequirements()
      
      // Inject JAEGIS components
      this.injectJAEGISComponents(jaegisComponents)
      
      // Initialize AI components in order
      await this.initializeAIComponents()
      
      // Setup integration bridge
      await this.setupIntegrationBridge()
      
      // Initialize monitoring dashboard
      if (this.systemConfig.enableDashboard) {
        await this.initializeMonitoringDashboard()
      }
      
      // Start health monitoring
      this.startHealthMonitoring()
      
      // Setup event handlers
      this.setupEventHandlers()
      
      // Finalize initialization
      this.metrics.initializationTime = Date.now() - initStartTime
      this.metrics.componentsInitialized = Object.values(this.components).filter(c => c && c.isInitialized).length
      this.state = SYSTEM_STATES.READY
      this.isInitialized = true
      
      logger.info(`✅ JAEGIS AI System initialized successfully in ${this.metrics.initializationTime}ms`)
      logger.info(`🎯 Integration mode: ${this.integrationMode}`)
      logger.info(`📊 Components initialized: ${this.metrics.componentsInitialized}/6`)
      
      // Auto-start if configured
      if (this.systemConfig.autoStart) {
        await this.start()
      }
      
      return true
      
    } catch (error) {
      this.state = SYSTEM_STATES.ERROR
      logger.error('❌ Failed to initialize JAEGIS AI System:', error)
      throw error
    }
  }

  async validateSystemRequirements() {
    const requirements = []
    
    // Check Node.js version
    const nodeVersion = process.version
    const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0])
    if (majorVersion < 16) {
      requirements.push(`Node.js 16+ required (current: ${nodeVersion})`)
    }
    
    // Check configuration
    if (!this.config.ai) {
      requirements.push('AI configuration section missing')
    }
    
    if (!this.config.ai?.openrouter?.keys || this.config.ai.openrouter.keys.length === 0) {
      requirements.push('OpenRouter API keys not configured')
    }
    
    // Check Redis configuration
    if (!this.config.ai?.redis) {
      logger.warn('Redis configuration missing - some features may be limited')
    }
    
    if (requirements.length > 0) {
      throw new Error(`System requirements not met:\n${requirements.map(r => `- ${r}`).join('\n')}`)
    }
    
    logger.info('✅ System requirements validated')
  }

  injectJAEGISComponents(jaegisComponents) {
    // Inject existing JAEGIS components for integration
    this.jaegisComponents = {
      ...this.jaegisComponents,
      ...jaegisComponents
    }
    
    const injectedCount = Object.values(this.jaegisComponents).filter(c => c !== null).length
    logger.info(`🔗 Injected ${injectedCount} JAEGIS components for integration`)
  }

  async initializeAIComponents() {
    logger.info('🧠 Initializing AI components...')
    
    try {
      // 1. Initialize OpenRouter Manager (Core AI API)
      if (this.config.ai?.openrouter) {
        logger.info('🤖 Initializing OpenRouter Manager...')
        this.components.openRouterManager = new OpenRouterManager({
          config: this.config,
          cache: this.jaegisComponents.cacheManager,
          errorHandler: this.jaegisComponents.errorHandler,
          performanceMonitor: this.jaegisComponents.performanceMonitor
        })
        await this.components.openRouterManager.initialize()
        logger.info('✅ OpenRouter Manager initialized')
      }
      
      // 2. Initialize Redis AI Manager (Data & Agent Management)
      if (this.config.ai?.redis) {
        logger.info('🗄️ Initializing Redis AI Manager...')
        this.components.redisAIManager = new RedisAIManager({
          config: this.config,
          errorHandler: this.jaegisComponents.errorHandler,
          performanceMonitor: this.jaegisComponents.performanceMonitor
        })
        await this.components.redisAIManager.initialize()
        logger.info('✅ Redis AI Manager initialized')
      }
      
      // 3. Initialize Autonomous Learning Engine (Self-Learning)
      if (this.systemConfig.enableLearning && this.components.openRouterManager && this.components.redisAIManager) {
        logger.info('🧠 Initializing Autonomous Learning Engine...')
        this.components.autonomousLearningEngine = new AutonomousLearningEngine({
          config: this.config,
          openRouterManager: this.components.openRouterManager,
          redisAIManager: this.components.redisAIManager,
          errorHandler: this.jaegisComponents.errorHandler,
          performanceMonitor: this.jaegisComponents.performanceMonitor
        })
        await this.components.autonomousLearningEngine.initialize()
        logger.info('✅ Autonomous Learning Engine initialized')
      }
      
      // 4. Initialize Background Process Manager (Automation)
      if (this.systemConfig.enableBackgroundProcessing && this.components.openRouterManager) {
        logger.info('⚙️ Initializing Background Process Manager...')
        this.components.backgroundProcessManager = new BackgroundProcessManager({
          config: this.config,
          openRouterManager: this.components.openRouterManager,
          redisAIManager: this.components.redisAIManager,
          autonomousLearningEngine: this.components.autonomousLearningEngine,
          errorHandler: this.jaegisComponents.errorHandler,
          performanceMonitor: this.jaegisComponents.performanceMonitor
        })
        await this.components.backgroundProcessManager.initialize()
        logger.info('✅ Background Process Manager initialized')
      }
      
      logger.info('🎯 Core AI components initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize AI components:', error)
      throw error
    }
  }

  async setupIntegrationBridge() {
    if (this.integrationMode === INTEGRATION_MODES.STANDALONE) {
      logger.info('📋 Standalone mode - skipping integration bridge')
      return
    }
    
    try {
      logger.info('🌉 Setting up AI Integration Bridge...')
      
      this.components.aiIntegrationBridge = new AIIntegrationBridge({
        config: this.config,
        // Existing JAEGIS components
        commandRouter: this.jaegisComponents.commandRouter,
        commandExecutor: this.jaegisComponents.commandExecutor,
        cacheManager: this.jaegisComponents.cacheManager,
        decisionEngine: this.jaegisComponents.decisionEngine,
        errorHandler: this.jaegisComponents.errorHandler,
        performanceMonitor: this.jaegisComponents.performanceMonitor,
        contextManager: this.jaegisComponents.contextManager,
        responseFormatter: this.jaegisComponents.responseFormatter,
        // AI components
        openRouterManager: this.components.openRouterManager,
        redisAIManager: this.components.redisAIManager,
        autonomousLearningEngine: this.components.autonomousLearningEngine,
        backgroundProcessManager: this.components.backgroundProcessManager
      })
      
      await this.components.aiIntegrationBridge.initialize()
      logger.info('✅ AI Integration Bridge setup complete')
      
    } catch (error) {
      logger.error('❌ Failed to setup integration bridge:', error)
      throw error
    }
  }

  async initializeMonitoringDashboard() {
    try {
      logger.info('📊 Initializing AI Monitoring Dashboard...')
      
      this.components.aiMonitoringDashboard = new AIMonitoringDashboard({
        config: this.config,
        openRouterManager: this.components.openRouterManager,
        redisAIManager: this.components.redisAIManager,
        autonomousLearningEngine: this.components.autonomousLearningEngine,
        backgroundProcessManager: this.components.backgroundProcessManager,
        aiIntegrationBridge: this.components.aiIntegrationBridge,
        performanceMonitor: this.jaegisComponents.performanceMonitor,
        errorHandler: this.jaegisComponents.errorHandler
      })
      
      await this.components.aiMonitoringDashboard.initialize()
      logger.info('✅ AI Monitoring Dashboard initialized')
      
    } catch (error) {
      logger.error('❌ Failed to initialize monitoring dashboard:', error)
      throw error
    }
  }

  startHealthMonitoring() {
    if (this.healthMonitor) {
      clearInterval(this.healthMonitor)
    }
    
    this.healthMonitor = setInterval(async () => {
      await this.performHealthCheck()
    }, this.systemConfig.healthCheckInterval)
    
    logger.info('🔍 Health monitoring started')
  }

  setupEventHandlers() {
    // Setup graceful shutdown
    if (this.systemConfig.gracefulShutdown) {
      process.on('SIGINT', () => this.gracefulShutdown('SIGINT'))
      process.on('SIGTERM', () => this.gracefulShutdown('SIGTERM'))
      process.on('uncaughtException', (error) => this.handleUncaughtException(error))
      process.on('unhandledRejection', (reason) => this.handleUnhandledRejection(reason))
    }
    
    logger.info('📡 Event handlers setup complete')
  }

  async start() {
    if (this.state !== SYSTEM_STATES.READY) {
      throw new Error(`Cannot start system in state: ${this.state}`)
    }
    
    try {
      logger.info('🚀 Starting JAEGIS AI System...')
      
      this.state = SYSTEM_STATES.RUNNING
      this.startTime = Date.now()
      
      // Start background processes
      if (this.components.backgroundProcessManager) {
        // Background processes are already started during initialization
        logger.info('⚙️ Background processes running')
      }
      
      // Start learning processes
      if (this.components.autonomousLearningEngine) {
        // Learning processes are already started during initialization
        logger.info('🧠 Learning processes running')
      }
      
      // Start monitoring
      if (this.components.aiMonitoringDashboard) {
        // Monitoring is already started during initialization
        logger.info('📊 Monitoring dashboard active')
      }
      
      logger.info('✅ JAEGIS AI System is now running')
      
      // Emit start event
      this.emit('system:started', {
        timestamp: Date.now(),
        integrationMode: this.integrationMode,
        componentsActive: this.getActiveComponentCount()
      })
      
      return true
      
    } catch (error) {
      this.state = SYSTEM_STATES.ERROR
      logger.error('❌ Failed to start JAEGIS AI System:', error)
      throw error
    }
  }

  async stop() {
    if (this.state === SYSTEM_STATES.SHUTDOWN) {
      return true
    }
    
    try {
      logger.info('🛑 Stopping JAEGIS AI System...')
      
      this.state = SYSTEM_STATES.SHUTDOWN
      
      // Stop health monitoring
      if (this.healthMonitor) {
        clearInterval(this.healthMonitor)
        this.healthMonitor = null
      }
      
      // Cleanup components in reverse order
      const cleanupOrder = [
        'aiMonitoringDashboard',
        'aiIntegrationBridge',
        'backgroundProcessManager',
        'autonomousLearningEngine',
        'redisAIManager',
        'openRouterManager'
      ]
      
      for (const componentName of cleanupOrder) {
        const component = this.components[componentName]
        if (component && typeof component.cleanup === 'function') {
          try {
            await component.cleanup()
            logger.info(`✅ ${componentName} cleaned up`)
          } catch (error) {
            logger.warn(`⚠️ Failed to cleanup ${componentName}:`, error.message)
          }
        }
      }
      
      // Clear components
      Object.keys(this.components).forEach(key => {
        this.components[key] = null
      })
      
      this.isInitialized = false
      
      logger.info('✅ JAEGIS AI System stopped')
      
      // Emit stop event
      this.emit('system:stopped', {
        timestamp: Date.now(),
        uptime: Date.now() - this.startTime
      })
      
      return true
      
    } catch (error) {
      logger.error('❌ Failed to stop JAEGIS AI System:', error)
      throw error
    }
  }

  async restart() {
    logger.info('🔄 Restarting JAEGIS AI System...')
    
    await this.stop()
    await new Promise(resolve => setTimeout(resolve, 1000)) // Wait 1 second
    await this.initialize(this.jaegisComponents)
    
    logger.info('✅ JAEGIS AI System restarted')
  }

  async performHealthCheck() {
    const healthCheck = {
      timestamp: Date.now(),
      systemState: this.state,
      uptime: Date.now() - this.startTime,
      components: {},
      overall: 'healthy'
    }
    
    try {
      // Check each component
      for (const [name, component] of Object.entries(this.components)) {
        if (component) {
          healthCheck.components[name] = {
            initialized: component.isInitialized || false,
            status: component.isInitialized ? 'healthy' : 'unhealthy'
          }
          
          // Get component-specific health data
          if (typeof component.getUsageReport === 'function') {
            try {
              const report = component.getUsageReport()
              healthCheck.components[name].metrics = report
            } catch (error) {
              healthCheck.components[name].status = 'degraded'
              healthCheck.components[name].error = error.message
            }
          }
        } else {
          healthCheck.components[name] = {
            initialized: false,
            status: 'unavailable'
          }
        }
      }
      
      // Determine overall health
      const componentStatuses = Object.values(healthCheck.components).map(c => c.status)
      const unhealthyCount = componentStatuses.filter(s => s === 'unhealthy' || s === 'degraded').length
      
      if (unhealthyCount > 2) {
        healthCheck.overall = 'critical'
        this.state = SYSTEM_STATES.DEGRADED
      } else if (unhealthyCount > 0) {
        healthCheck.overall = 'degraded'
        this.state = SYSTEM_STATES.DEGRADED
      } else {
        healthCheck.overall = 'healthy'
        if (this.state === SYSTEM_STATES.DEGRADED) {
          this.state = SYSTEM_STATES.RUNNING
        }
      }
      
      this.metrics.lastHealthCheck = Date.now()
      this.metrics.uptime = healthCheck.uptime
      
      // Emit health check event
      this.emit('system:health_check', healthCheck)
      
      return healthCheck
      
    } catch (error) {
      logger.error('Health check failed:', error)
      healthCheck.overall = 'error'
      healthCheck.error = error.message
      return healthCheck
    }
  }

  // Public API methods
  async processAIRequest(request) {
    if (!this.isInitialized || this.state !== SYSTEM_STATES.RUNNING) {
      throw new Error(`AI System not ready (state: ${this.state})`)
    }
    
    const startTime = Date.now()
    this.metrics.totalRequests++
    
    try {
      let result = null
      
      // Route request based on type
      switch (request.type) {
        case 'completion':
          if (!this.components.openRouterManager) {
            throw new Error('OpenRouter Manager not available')
          }
          result = await this.components.openRouterManager.generateCompletion(
            request.prompt, 
            request.options
          )
          break
          
        case 'agent_discussion':
          if (!this.components.autonomousLearningEngine) {
            throw new Error('Autonomous Learning Engine not available')
          }
          result = await this.components.autonomousLearningEngine.initiateAgentDiscussion(request.data)
          break
          
        case 'background_task':
          if (!this.components.backgroundProcessManager) {
            throw new Error('Background Process Manager not available')
          }
          result = await this.components.backgroundProcessManager.scheduleTask(request.data)
          break
          
        case 'agent_create':
          if (!this.components.redisAIManager) {
            throw new Error('Redis AI Manager not available')
          }
          result = await this.components.redisAIManager.createAgent(request.data)
          break
          
        default:
          throw new Error(`Unknown request type: ${request.type}`)
      }
      
      this.metrics.successfulRequests++
      
      return {
        success: true,
        result,
        processingTime: Date.now() - startTime,
        timestamp: Date.now()
      }
      
    } catch (error) {
      this.metrics.failedRequests++
      
      logger.error(`AI request failed (${request.type}):`, error)
      
      return {
        success: false,
        error: error.message,
        processingTime: Date.now() - startTime,
        timestamp: Date.now()
      }
    }
  }

  getSystemStatus() {
    return {
      state: this.state,
      integrationMode: this.integrationMode,
      uptime: Date.now() - this.startTime,
      initialized: this.isInitialized,
      components: Object.fromEntries(
        Object.entries(this.components).map(([name, component]) => [
          name,
          {
            available: !!component,
            initialized: component?.isInitialized || false
          }
        ])
      ),
      metrics: { ...this.metrics },
      configuration: this.systemConfig
    }
  }

  getDashboardData(section = null) {
    if (!this.components.aiMonitoringDashboard) {
      throw new Error('Monitoring dashboard not available')
    }
    
    return this.components.aiMonitoringDashboard.getDashboardData(section)
  }

  getAlerts(filter = {}) {
    if (!this.components.aiMonitoringDashboard) {
      throw new Error('Monitoring dashboard not available')
    }
    
    return this.components.aiMonitoringDashboard.getAlerts(filter)
  }

  subscribeToUpdates(callback) {
    if (!this.components.aiMonitoringDashboard) {
      throw new Error('Monitoring dashboard not available')
    }
    
    return this.components.aiMonitoringDashboard.subscribeToUpdates(callback)
  }

  subscribeToAlerts(callback) {
    if (!this.components.aiMonitoringDashboard) {
      throw new Error('Monitoring dashboard not available')
    }
    
    return this.components.aiMonitoringDashboard.subscribeToAlerts(callback)
  }

  // Component access methods
  getOpenRouterManager() {
    return this.components.openRouterManager
  }

  getRedisAIManager() {
    return this.components.redisAIManager
  }

  getAutonomousLearningEngine() {
    return this.components.autonomousLearningEngine
  }

  getBackgroundProcessManager() {
    return this.components.backgroundProcessManager
  }

  getAIIntegrationBridge() {
    return this.components.aiIntegrationBridge
  }

  getAIMonitoringDashboard() {
    return this.components.aiMonitoringDashboard
  }

  // Utility methods
  getActiveComponentCount() {
    return Object.values(this.components).filter(c => c && c.isInitialized).length
  }

  async gracefulShutdown(signal) {
    logger.info(`🛑 Received ${signal}, initiating graceful shutdown...`)
    
    try {
      await this.stop()
      process.exit(0)
    } catch (error) {
      logger.error('Graceful shutdown failed:', error)
      process.exit(1)
    }
  }

  handleUncaughtException(error) {
    logger.error('Uncaught exception:', error)
    
    // Emit error event
    this.emit('system:error', {
      type: 'uncaught_exception',
      error: error.message,
      stack: error.stack,
      timestamp: Date.now()
    })
    
    // Attempt graceful shutdown
    this.gracefulShutdown('uncaughtException')
  }

  handleUnhandledRejection(reason) {
    logger.error('Unhandled rejection:', reason)
    
    // Emit error event
    this.emit('system:error', {
      type: 'unhandled_rejection',
      reason: reason,
      timestamp: Date.now()
    })
  }

  // Event system
  on(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, new Set())
    }
    this.eventHandlers.get(event).add(handler)
    
    return () => this.eventHandlers.get(event)?.delete(handler)
  }

  emit(event, data) {
    const handlers = this.eventHandlers.get(event)
    if (handlers) {
      for (const handler of handlers) {
        try {
          handler(data)
        } catch (error) {
          logger.warn(`Event handler failed for ${event}:`, error.message)
        }
      }
    }
  }

  // Static factory method
  static async create(config = {}, jaegisComponents = {}) {
    const aiSystem = new JAEGISAISystem(config)
    await aiSystem.initialize(jaegisComponents)
    return aiSystem
  }
}

// Export system and components
module.exports = {
  JAEGISAISystem,
  SYSTEM_STATES,
  INTEGRATION_MODES,
  
  // Export individual components for direct use
  OpenRouterManager,
  RedisAIManager,
  AutonomousLearningEngine,
  BackgroundProcessManager,
  AIIntegrationBridge,
  AIMonitoringDashboard
}