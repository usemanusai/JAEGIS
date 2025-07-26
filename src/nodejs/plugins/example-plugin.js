/**
 * Example JAEGIS Plugin
 * Demonstrates the JAEGIS plugin architecture and capabilities
 * 
 * @version 1.0.0
 * @author JAEGIS Development Team
 */

class ExamplePlugin {
  constructor() {
    this.name = 'example'
    this.description = 'Example plugin demonstrating JAEGIS plugin architecture and capabilities'
    this.version = '1.0.0'
    this.category = 'utility'
    this.author = 'JAEGIS Development Team'
    
    // Plugin metadata
    this.parameters = [
      {
        name: 'action',
        type: 'string',
        required: false,
        description: 'Action to perform (demo, cache, python, config)',
        default: 'demo'
      },
      {
        name: 'message',
        type: 'string',
        required: false,
        description: 'Custom message to display'
      },
      {
        name: 'count',
        type: 'number',
        required: false,
        description: 'Number for demonstration purposes',
        default: 1
      }
    ]
    
    this.examples = [
      {
        command: '/example',
        description: 'Basic example usage with default demo action'
      },
      {
        command: '/example action=cache message="test cache"',
        description: 'Demonstrate caching functionality'
      },
      {
        command: '/example action=python',
        description: 'Demonstrate Python bridge integration'
      },
      {
        command: '/example action=config',
        description: 'Show configuration access'
      }
    ]
    
    this.usage = '/example [action=<action>] [message=<message>] [count=<number>]'
    
    // Plugin state
    this.executionCount = 0
    this.lastExecution = null
  }

  /**
   * Main plugin execution method
   * @param {Object} context - Execution context
   * @returns {Object} - Plugin result
   */
  async execute(context) {
    const { parameters, logger, cache, pythonBridge, config } = context
    
    // Increment execution counter
    this.executionCount++
    this.lastExecution = Date.now()
    
    logger.info(`Executing example plugin (execution #${this.executionCount})`, {
      parameters,
      executionId: context.executionId
    })
    
    // Get action parameter with default
    const action = parameters.action || 'demo'
    
    try {
      switch (action) {
        case 'demo':
          return await this.demoAction(context)
        case 'cache':
          return await this.cacheAction(context)
        case 'python':
          return await this.pythonAction(context)
        case 'config':
          return await this.configAction(context)
        case 'error':
          return await this.errorAction(context)
        default:
          throw new Error(`Unknown action: ${action}`)
      }
    } catch (error) {
      logger.error('Example plugin execution error:', error)
      throw error
    }
  }

  /**
   * Demonstrate basic plugin functionality
   */
  async demoAction(context) {
    const { parameters, logger } = context
    const message = parameters.message || 'Hello from JAEGIS Example Plugin!'
    const count = parseInt(parameters.count) || 1
    
    logger.info('Executing demo action', { message, count })
    
    // Simulate some processing time
    await this.sleep(100)
    
    return {
      action: 'demo',
      message,
      count,
      repeated_message: Array(count).fill(message),
      plugin_info: {
        name: this.name,
        version: this.version,
        execution_count: this.executionCount,
        last_execution: this.lastExecution
      },
      system_info: {
        node_version: process.version,
        platform: process.platform,
        uptime: process.uptime(),
        memory_usage: process.memoryUsage()
      },
      timestamp: Date.now()
    }
  }

  /**
   * Demonstrate caching functionality
   */
  async cacheAction(context) {
    const { parameters, logger, cache } = context
    const message = parameters.message || 'Cache test message'
    const cacheKey = `example-plugin:cache-demo:${message}`
    
    logger.info('Executing cache action', { message, cacheKey })
    
    // Try to get from cache first
    const cached = await cache.get(cacheKey)
    if (cached) {
      logger.info('Retrieved data from cache')
      return {
        action: 'cache',
        message: 'Data retrieved from cache',
        cached_data: cached,
        cache_hit: true,
        timestamp: Date.now()
      }
    }
    
    // Simulate expensive operation
    logger.info('Performing expensive operation (not cached)')
    await this.sleep(1000) // Simulate 1 second processing
    
    const expensiveResult = {
      processed_message: message.toUpperCase(),
      processing_time: 1000,
      random_data: Math.random(),
      created_at: Date.now()
    }
    
    // Cache the result for 5 minutes
    await cache.set(cacheKey, expensiveResult, 300000)
    logger.info('Cached expensive operation result')
    
    return {
      action: 'cache',
      message: 'Expensive operation completed and cached',
      result: expensiveResult,
      cache_hit: false,
      cache_key: cacheKey,
      cache_ttl: 300000,
      timestamp: Date.now()
    }
  }

  /**
   * Demonstrate Python bridge integration
   */
  async pythonAction(context) {
    const { logger, pythonBridge } = context
    
    logger.info('Executing Python bridge action')
    
    try {
      // Test Python bridge health
      const health = await pythonBridge.healthCheck()
      logger.info('Python bridge health check completed', health)
      
      // Test Python service connection
      const testConnection = await pythonBridge.testConnection()
      logger.info('Python service connection test completed', testConnection)
      
      // Get Python service metrics (if available)
      let metrics = null
      try {
        metrics = await pythonBridge.getMetrics()
      } catch (error) {
        logger.warn('Could not retrieve Python metrics:', error.message)
      }
      
      return {
        action: 'python',
        message: 'Python bridge integration test completed',
        python_health: health,
        connection_test: testConnection,
        metrics: metrics,
        bridge_status: pythonBridge.getStatus(),
        timestamp: Date.now()
      }
      
    } catch (error) {
      logger.error('Python bridge action failed:', error)
      
      return {
        action: 'python',
        message: 'Python bridge integration test failed',
        error: error.message,
        bridge_status: pythonBridge.getStatus(),
        timestamp: Date.now()
      }
    }
  }

  /**
   * Demonstrate configuration access
   */
  async configAction(context) {
    const { logger, config } = context
    
    logger.info('Executing config action')
    
    // Access various configuration sections
    const configInfo = {
      system: {
        name: config.system?.name,
        version: config.system?.version,
        environment: config.system?.environment,
        debug: config.system?.debug
      },
      cache: {
        enabled: config.cache?.enabled,
        type: config.cache?.type,
        duration: config.cache?.duration
      },
      python_integration: {
        enabled: config.python_integration?.enabled,
        host: config.python_integration?.communication?.host,
        port: config.python_integration?.communication?.port
      },
      github: {
        commands_url: config.github?.commands_url,
        repository: config.github?.repository
      }
    }
    
    return {
      action: 'config',
      message: 'Configuration access demonstration',
      config_info: configInfo,
      plugin_config: config.plugins?.example || null,
      timestamp: Date.now()
    }
  }

  /**
   * Demonstrate error handling
   */
  async errorAction(context) {
    const { logger } = context
    
    logger.info('Executing error action (will throw error)')
    
    // Simulate different types of errors
    const errorTypes = [
      'validation_error',
      'processing_error',
      'timeout_error',
      'external_service_error'
    ]
    
    const errorType = errorTypes[Math.floor(Math.random() * errorTypes.length)]
    
    switch (errorType) {
      case 'validation_error':
        throw new Error('Validation failed: Invalid input parameters')
      case 'processing_error':
        throw new Error('Processing failed: Unable to complete operation')
      case 'timeout_error':
        throw new Error('Timeout error: Operation took too long')
      case 'external_service_error':
        throw new Error('External service error: Dependency unavailable')
      default:
        throw new Error('Unknown error occurred')
    }
  }

  /**
   * Plugin lifecycle hooks
   */
  get hooks() {
    return {
      beforeExecution: async (context) => {
        context.logger.info('Example plugin: Before execution hook', {
          plugin: this.name,
          executionId: context.executionId
        })
        
        // Add custom context data
        context.pluginStartTime = Date.now()
      },
      
      afterExecution: async (context) => {
        const duration = Date.now() - context.pluginStartTime
        
        context.logger.info('Example plugin: After execution hook', {
          plugin: this.name,
          executionId: context.executionId,
          duration
        })
        
        // Log performance metrics
        if (duration > 1000) {
          context.logger.warn('Example plugin: Slow execution detected', {
            duration,
            threshold: 1000
          })
        }
      },
      
      onError: async (context) => {
        context.logger.error('Example plugin: Error hook', {
          plugin: this.name,
          executionId: context.executionId,
          error: context.error?.message
        })
        
        // Could send error notifications, update metrics, etc.
      },
      
      onSuccess: async (context) => {
        context.logger.info('Example plugin: Success hook', {
          plugin: this.name,
          executionId: context.executionId,
          resultType: typeof context.result
        })
        
        // Could update success metrics, send notifications, etc.
      }
    }
  }

  /**
   * Plugin validation method (optional)
   */
  validateParameters(parameters) {
    const errors = []
    
    // Validate action parameter
    if (parameters.action) {
      const validActions = ['demo', 'cache', 'python', 'config', 'error']
      if (!validActions.includes(parameters.action)) {
        errors.push(`Invalid action '${parameters.action}'. Valid actions: ${validActions.join(', ')}`)
      }
    }
    
    // Validate count parameter
    if (parameters.count !== undefined) {
      const count = parseInt(parameters.count)
      if (isNaN(count) || count < 1 || count > 100) {
        errors.push('Count must be a number between 1 and 100')
      }
    }
    
    // Validate message length
    if (parameters.message && parameters.message.length > 1000) {
      errors.push('Message must be less than 1000 characters')
    }
    
    return {
      valid: errors.length === 0,
      errors
    }
  }

  /**
   * Plugin information method
   */
  getInfo() {
    return {
      name: this.name,
      description: this.description,
      version: this.version,
      category: this.category,
      author: this.author,
      parameters: this.parameters,
      examples: this.examples,
      usage: this.usage,
      execution_count: this.executionCount,
      last_execution: this.lastExecution
    }
  }

  /**
   * Plugin statistics
   */
  getStats() {
    return {
      execution_count: this.executionCount,
      last_execution: this.lastExecution,
      uptime: this.lastExecution ? Date.now() - this.lastExecution : 0
    }
  }

  /**
   * Utility method for simulating async operations
   */
  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  /**
   * Plugin cleanup method (optional)
   */
  async cleanup() {
    // Cleanup any resources, timers, etc.
    this.executionCount = 0
    this.lastExecution = null
  }
}

// Export plugin instance
module.exports = new ExamplePlugin()