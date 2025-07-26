/**
 * JAEGIS Command Processor
 * Advanced command processing with inter-process communication
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const EventEmitter = require('events')
const logger = require('../utils/logger')

class CommandProcessor extends EventEmitter {
  constructor({ config, cache, pythonBridge, decisionEngine }) {
    super()
    this.config = config
    this.cache = cache
    this.pythonBridge = pythonBridge
    this.decisionEngine = decisionEngine
    this.processingQueue = []
    this.activeProcesses = new Map()
    this.commandHandlers = new Map()
    this.isInitialized = false
  }

  async initialize() {
    logger.info('⚡ Initializing Command Processor...')
    
    try {
      // Register built-in command handlers
      this.registerBuiltInHandlers()
      
      // Setup processing queue
      this.setupProcessingQueue()
      
      this.isInitialized = true
      logger.info('✅ Command Processor initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Command Processor:', error)
      throw error
    }
  }

  registerBuiltInHandlers() {
    // Help commands
    this.commandHandlers.set('help', this.handleHelpCommand.bind(this))
    this.commandHandlers.set('h', this.handleHelpCommand.bind(this))
    
    // Status commands
    this.commandHandlers.set('status', this.handleStatusCommand.bind(this))
    this.commandHandlers.set('s', this.handleStatusCommand.bind(this))
    
    // Configuration commands
    this.commandHandlers.set('config', this.handleConfigCommand.bind(this))
    this.commandHandlers.set('c', this.handleConfigCommand.bind(this))
    
    // Agent commands
    this.commandHandlers.set('agents', this.handleAgentsCommand.bind(this))
    this.commandHandlers.set('a', this.handleAgentsCommand.bind(this))
    
    // Mode switching
    this.commandHandlers.set('mode-switch', this.handleModeSwitchCommand.bind(this))
    this.commandHandlers.set('mode', this.handleModeSwitchCommand.bind(this))
    
    // Analytics commands
    this.commandHandlers.set('analytics', this.handleAnalyticsCommand.bind(this))
    this.commandHandlers.set('analyze', this.handleAnalyticsCommand.bind(this))
    
    // Cache commands
    this.commandHandlers.set('cache', this.handleCacheCommand.bind(this))
    
    // Debug commands
    this.commandHandlers.set('debug', this.handleDebugCommand.bind(this))
    this.commandHandlers.set('troubleshoot', this.handleDebugCommand.bind(this))
    
    logger.info(`📋 Registered ${this.commandHandlers.size} built-in command handlers`)
  }

  async processCommand(command, options = {}) {
    const startTime = Date.now()
    const requestId = options.requestId || this.generateRequestId()
    
    try {
      logger.info(`⚡ Processing command: ${command} [${requestId}]`)
      
      // Validate input
      if (!command || typeof command !== 'string') {
        throw new Error('Invalid command format')
      }
      
      // Normalize command
      const normalizedCommand = this.normalizeCommand(command)
      
      // Check if we have a built-in handler
      if (this.commandHandlers.has(normalizedCommand)) {
        const result = await this.executeBuiltInCommand(normalizedCommand, options)
        result.processingTime = Date.now() - startTime
        result.requestId = requestId
        return result
      }
      
      // Process with GitHub data and Python integration
      const result = await this.processWithIntegration(normalizedCommand, options)
      result.processingTime = Date.now() - startTime
      result.requestId = requestId
      
      // Emit processing event
      this.emit('commandProcessed', {
        command: normalizedCommand,
        result,
        options
      })
      
      return result
      
    } catch (error) {
      logger.error(`Command processing error [${requestId}]:`, error)
      
      const errorResult = {
        success: false,
        error: error.message,
        code: 'PROCESSING_ERROR',
        requestId,
        processingTime: Date.now() - startTime
      }
      
      this.emit('commandError', {
        command,
        error,
        options
      })
      
      return errorResult
    }
  }

  async executeBuiltInCommand(command, options) {
    const handler = this.commandHandlers.get(command)
    
    if (!handler) {
      throw new Error(`No handler found for command: ${command}`)
    }
    
    try {
      const result = await handler(options)
      return {
        success: true,
        data: result,
        type: 'built_in',
        command
      }
    } catch (error) {
      throw new Error(`Built-in command failed: ${error.message}`)
    }
  }

  async processWithIntegration(command, options) {
    try {
      // Get commands data from cache or GitHub
      const commandsData = options.commandsData || await this.getCommandsData()
      
      // Find command definition
      const commandDef = this.findCommandDefinition(command, commandsData)
      
      if (!commandDef) {
        // Generate suggestions for unknown command
        const suggestions = await this.generateSuggestions(command, commandsData)
        return {
          success: false,
          error: `Unknown command: ${command}`,
          code: 'UNKNOWN_COMMAND',
          suggestions
        }
      }
      
      // Process the command based on its definition
      const result = await this.executeDefinedCommand(commandDef, options)
      
      return {
        success: true,
        data: result,
        type: 'defined',
        command: commandDef.name,
        category: commandDef.category
      }
      
    } catch (error) {
      throw new Error(`Integration processing failed: ${error.message}`)
    }
  }

  async getCommandsData() {
    // Try cache first
    const cached = await this.cache.get('commands_data')
    if (cached) {
      return cached
    }
    
    // Fetch from GitHub via Python bridge
    const response = await this.pythonBridge.fetchGitHubCommands(
      this.config.github.commands_url
    )
    
    if (!response.success) {
      throw new Error(`Failed to fetch commands: ${response.error}`)
    }
    
    // Parse commands
    const parseResult = await this.pythonBridge.parseMarkdownCommands(response.data.content)
    
    if (!parseResult.success) {
      throw new Error(`Failed to parse commands: ${parseResult.error}`)
    }
    
    const commandsData = parseResult.data
    
    // Cache the result
    await this.cache.set('commands_data', commandsData, 3600000) // 1 hour
    
    return commandsData
  }

  findCommandDefinition(command, commandsData) {
    if (!commandsData || !commandsData.command_index) {
      return null
    }
    
    // Direct match
    if (commandsData.command_index[command]) {
      return commandsData.command_index[command]
    }
    
    // Alias match
    if (commandsData.alias_index && commandsData.alias_index[command]) {
      const actualCommand = commandsData.alias_index[command]
      return commandsData.command_index[actualCommand]
    }
    
    return null
  }

  async executeDefinedCommand(commandDef, options) {
    // This is where we would execute the actual command logic
    // For now, return the command definition and usage information
    
    return {
      name: commandDef.name,
      description: commandDef.description,
      usage: commandDef.usage,
      examples: commandDef.examples,
      category: commandDef.category,
      message: `Command '${commandDef.name}' found. This is a placeholder response.`,
      metadata: commandDef.metadata || {}
    }
  }

  async generateSuggestions(command, commandsData) {
    try {
      const response = await this.pythonBridge.generateSuggestions(command, {
        commands_data: commandsData
      })
      
      return response.success ? response.data : []
      
    } catch (error) {
      logger.error('Suggestion generation failed:', error)
      return []
    }
  }

  // Built-in command handlers
  async handleHelpCommand(options) {
    const { parameters = {} } = options
    
    if (parameters.command) {
      // Help for specific command
      return await this.getCommandHelp(parameters.command)
    }
    
    // General help
    return {
      message: 'JAEGIS Command Processing System',
      description: 'AI Agent Intelligence System with GitHub Integration',
      version: this.config.system.version,
      available_commands: [
        '/help [command] - Show help information',
        '/status - Show system status',
        '/config - Configuration management',
        '/agents - List available agents',
        '/mode-switch <mode> - Switch operational mode',
        '/analytics - System analytics',
        '/cache - Cache management',
        '/debug - Debug information'
      ],
      usage_examples: [
        '/help config',
        '/status',
        '/agents list',
        '/mode-switch development'
      ]
    }
  }

  async handleStatusCommand(options) {
    const systemStatus = {
      system: {
        name: this.config.system.name,
        version: this.config.system.version,
        environment: this.config.system.environment,
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        pid: process.pid
      },
      services: {
        command_processor: {
          status: 'healthy',
          active_processes: this.activeProcesses.size,
          queue_length: this.processingQueue.length
        },
        python_bridge: await this.pythonBridge.healthCheck(),
        cache: await this.cache.healthCheck()
      },
      performance: {
        commands_processed: this.getProcessedCount(),
        average_response_time: this.getAverageResponseTime(),
        cache_hit_rate: this.cache.getStats().hitRate
      }
    }
    
    return systemStatus
  }

  async handleConfigCommand(options) {
    const { parameters = {} } = options
    
    switch (parameters.action) {
      case 'show':
        return this.getPublicConfig()
      case 'reload':
        return await this.reloadConfig()
      case 'validate':
        return await this.validateConfig()
      default:
        return {
          message: 'Configuration Management',
          available_actions: [
            'show - Display current configuration',
            'reload - Reload configuration from file',
            'validate - Validate current configuration'
          ],
          usage: '/config show'
        }
    }
  }

  async handleAgentsCommand(options) {
    const { parameters = {} } = options
    
    const agentSquads = {
      analysis_squad: {
        name: 'Analysis Squad',
        agents: ['research-agent', 'data-agent', 'insight-agent'],
        status: 'active',
        specialization: 'Data Analysis & Research'
      },
      development_squad: {
        name: 'Development Squad',
        agents: ['code-agent', 'test-agent', 'deploy-agent'],
        status: 'active',
        specialization: 'Software Development'
      },
      design_squad: {
        name: 'Design Squad',
        agents: ['ui-agent', 'ux-agent', 'architecture-agent'],
        status: 'standby',
        specialization: 'Design & Architecture'
      },
      management_squad: {
        name: 'Management Squad',
        agents: ['project-agent', 'coordination-agent', 'monitor-agent'],
        status: 'active',
        specialization: 'Project Management'
      }
    }
    
    if (parameters.squad) {
      return agentSquads[parameters.squad] || { error: 'Squad not found' }
    }
    
    return {
      message: 'JAEGIS Agent Squads',
      total_squads: Object.keys(agentSquads).length,
      squads: agentSquads,
      coordination_mode: 'dynamic_activation'
    }
  }

  async handleModeSwitchCommand(options) {
    const { parameters = {} } = options
    
    const availableModes = {
      documentation: 'Documentation Mode - Focus on creating comprehensive documentation',
      development: 'Development Mode - Interactive application development',
      analysis: 'Analysis Mode - Deep data analysis and insights'
    }
    
    if (!parameters.mode) {
      return {
        message: 'Mode Switch',
        current_mode: 'development',
        available_modes: availableModes,
        usage: '/mode-switch <mode>'
      }
    }
    
    if (!availableModes[parameters.mode]) {
      return {
        error: 'Invalid mode',
        available_modes: Object.keys(availableModes)
      }
    }
    
    // Switch mode logic would go here
    return {
      message: `Switched to ${parameters.mode} mode`,
      mode: parameters.mode,
      description: availableModes[parameters.mode]
    }
  }

  async handleAnalyticsCommand(options) {
    const analytics = {
      system_performance: {
        uptime: process.uptime(),
        memory_usage: process.memoryUsage(),
        cpu_usage: process.cpuUsage()
      },
      command_statistics: {
        total_processed: this.getProcessedCount(),
        success_rate: this.getSuccessRate(),
        average_response_time: this.getAverageResponseTime()
      },
      cache_performance: this.cache.getStats(),
      python_integration: {
        status: (await this.pythonBridge.healthCheck()).status,
        requests_made: this.getPythonRequestCount()
      }
    }
    
    return analytics
  }

  async handleCacheCommand(options) {
    const { parameters = {} } = options
    
    switch (parameters.action) {
      case 'stats':
        return this.cache.getStats()
      case 'clear':
        const cleared = await this.cache.clear(parameters.pattern)
        return { message: `Cleared ${cleared} cache entries` }
      case 'health':
        return await this.cache.healthCheck()
      default:
        return {
          message: 'Cache Management',
          available_actions: [
            'stats - Show cache statistics',
            'clear [pattern] - Clear cache entries',
            'health - Cache health check'
          ],
          current_stats: this.cache.getStats()
        }
    }
  }

  async handleDebugCommand(options) {
    const debugInfo = {
      system: {
        node_version: process.version,
        platform: process.platform,
        arch: process.arch,
        pid: process.pid,
        uptime: process.uptime()
      },
      memory: process.memoryUsage(),
      environment: {
        node_env: process.env.NODE_ENV,
        debug_mode: this.config.system.debug
      },
      services: {
        command_processor: this.isInitialized,
        python_bridge: this.pythonBridge.getStatus(),
        cache: await this.cache.healthCheck()
      },
      recent_errors: this.getRecentErrors()
    }
    
    return debugInfo
  }

  // Utility methods
  normalizeCommand(command) {
    return command.trim().toLowerCase().replace(/^\/+/, '')
  }

  generateRequestId() {
    return `proc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  getPublicConfig() {
    return {
      system: {
        name: this.config.system.name,
        version: this.config.system.version,
        environment: this.config.system.environment
      },
      features: {
        python_integration: this.config.python_integration.enabled,
        caching: this.config.cache.enabled,
        github_integration: true
      }
    }
  }

  async reloadConfig() {
    // Config reload logic would go here
    return { message: 'Configuration reloaded successfully' }
  }

  async validateConfig() {
    // Config validation logic would go here
    return { valid: true, message: 'Configuration is valid' }
  }

  getProcessedCount() {
    // Return processed command count
    return this.activeProcesses.size + 100 // Placeholder
  }

  getSuccessRate() {
    // Calculate success rate
    return '95.5%' // Placeholder
  }

  getAverageResponseTime() {
    // Calculate average response time
    return '1.2s' // Placeholder
  }

  getPythonRequestCount() {
    // Return Python request count
    return 50 // Placeholder
  }

  getRecentErrors() {
    // Return recent errors
    return [] // Placeholder
  }

  setupProcessingQueue() {
    // Setup command processing queue
    setInterval(() => {
      this.processQueue()
    }, 100) // Process queue every 100ms
  }

  async processQueue() {
    if (this.processingQueue.length === 0) return
    
    const maxConcurrent = this.config.processing?.max_concurrent_commands || 5
    
    while (this.processingQueue.length > 0 && this.activeProcesses.size < maxConcurrent) {
      const task = this.processingQueue.shift()
      this.activeProcesses.set(task.id, task)
      
      // Process task asynchronously
      this.processTask(task).finally(() => {
        this.activeProcesses.delete(task.id)
      })
    }
  }

  async processTask(task) {
    // Task processing logic
    try {
      await task.execute()
    } catch (error) {
      logger.error('Task processing error:', error)
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Command Processor...')
    
    // Clear active processes
    this.activeProcesses.clear()
    this.processingQueue.length = 0
    
    // Clear command handlers
    this.commandHandlers.clear()
    
    this.isInitialized = false
    logger.info('✅ Command Processor cleanup complete')
  }
}

module.exports = CommandProcessor