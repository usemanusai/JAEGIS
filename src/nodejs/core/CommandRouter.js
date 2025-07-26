/**
 * JAEGIS Command Router
 * Intelligent command processing and routing system
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')
const CommandProcessor = require('./CommandProcessor')
const DecisionEngine = require('./DecisionEngine')

class CommandRouter {
  constructor({ config, cache, pythonBridge }) {
    this.config = config
    this.cache = cache
    this.pythonBridge = pythonBridge
    this.processor = null
    this.decisionEngine = null
    this.commandsData = null
    this.lastCommandsUpdate = null
    this.commandAliases = new Map()
    this.commandHistory = []
    this.activeCommands = new Map()
  }

  async initialize() {
    logger.info('🎯 Initializing Command Router...')
    
    // Initialize decision engine
    this.decisionEngine = new DecisionEngine({
      config: this.config,
      cache: this.cache
    })
    await this.decisionEngine.initialize()
    
    // Initialize command processor
    this.processor = new CommandProcessor({
      config: this.config,
      cache: this.cache,
      pythonBridge: this.pythonBridge,
      decisionEngine: this.decisionEngine
    })
    await this.processor.initialize()
    
    // Load command aliases
    this.loadCommandAliases()
    
    // Initial commands fetch
    await this.updateCommandsFromGitHub()
    
    // Setup periodic updates
    this.setupPeriodicUpdates()
    
    logger.info('✅ Command Router initialized successfully')
  }

  async processCommand(command, options = {}) {
    const startTime = Date.now()
    const requestId = options.requestId || this.generateRequestId()
    
    try {
      logger.info(`🎯 Processing command: ${command} [${requestId}]`)
      
      // Normalize command
      const normalizedCommand = this.normalizeCommand(command)
      
      // Check if command is active (prevent duplicate processing)
      if (this.activeCommands.has(normalizedCommand)) {
        return {
          success: false,
          error: 'Command is already being processed',
          code: 'COMMAND_IN_PROGRESS',
          requestId
        }
      }
      
      // Mark command as active
      this.activeCommands.set(normalizedCommand, {
        requestId,
        startTime,
        options
      })
      
      try {
        // Validate command
        const validation = await this.validateCommand(normalizedCommand, options)
        if (!validation.valid) {
          return {
            success: false,
            error: validation.error,
            code: 'VALIDATION_ERROR',
            suggestions: validation.suggestions,
            requestId
          }
        }
        
        // Make routing decision
        const decision = await this.decisionEngine.makeDecision(normalizedCommand, options)
        logger.debug(`Decision for ${normalizedCommand}:`, decision)
        
        let result
        
        if (decision.needsGitHubData) {
          // Fetch fresh commands from GitHub
          await this.updateCommandsFromGitHub()
          result = await this.processWithGitHubData(normalizedCommand, options, decision)
        } else {
          // Process with cached/local data
          result = await this.processWithLocalData(normalizedCommand, options, decision)
        }
        
        // Add metadata
        result.requestId = requestId
        result.processingTime = Date.now() - startTime
        result.decision = decision
        
        // Record in history
        this.recordCommandHistory(normalizedCommand, result, options)
        
        return result
        
      } finally {
        // Remove from active commands
        this.activeCommands.delete(normalizedCommand)
      }
      
    } catch (error) {
      logger.error(`Command processing error [${requestId}]:`, error)
      
      return {
        success: false,
        error: 'Command processing failed',
        code: 'PROCESSING_ERROR',
        details: this.config.system.debug ? error.message : undefined,
        requestId,
        processingTime: Date.now() - startTime
      }
    }
  }

  async processWithGitHubData(command, options, decision) {
    logger.info(`📥 Processing ${command} with GitHub data`)
    
    try {
      // Ensure we have fresh commands data
      if (!this.commandsData || this.isCommandsDataStale()) {
        await this.updateCommandsFromGitHub()
      }
      
      // Process command with fresh data
      return await this.processor.processCommand(command, {
        ...options,
        commandsData: this.commandsData,
        decision,
        dataSource: 'github'
      })
      
    } catch (error) {
      logger.error('GitHub data processing error:', error)
      
      // Fallback to cached data if available
      if (this.commandsData) {
        logger.warn('Falling back to cached commands data')
        return await this.processWithLocalData(command, options, decision)
      }
      
      throw error
    }
  }

  async processWithLocalData(command, options, decision) {
    logger.info(`💾 Processing ${command} with local/cached data`)
    
    return await this.processor.processCommand(command, {
      ...options,
      commandsData: this.commandsData,
      decision,
      dataSource: 'cache'
    })
  }

  async updateCommandsFromGitHub() {
    const cacheKey = 'github_commands_data'
    
    try {
      logger.info('🌐 Fetching commands from GitHub...')
      
      // Check cache first
      const cached = await this.cache.get(cacheKey)
      if (cached && !this.isCommandsDataStale(cached.timestamp)) {
        this.commandsData = cached.data
        this.lastCommandsUpdate = cached.timestamp
        logger.info('📋 Using cached commands data')
        return
      }
      
      // Fetch from GitHub via Python bridge
      const response = await this.pythonBridge.fetchGitHubCommands(
        this.config.github.commands_url
      )
      
      if (!response.success) {
        throw new Error(`GitHub fetch failed: ${response.error}`)
      }
      
      // Process and cache the data
      const processedData = await this.processCommandsData(response.data)
      
      await this.cache.set(cacheKey, {
        data: processedData,
        timestamp: Date.now(),
        url: this.config.github.commands_url
      }, this.config.cache.duration)
      
      this.commandsData = processedData
      this.lastCommandsUpdate = Date.now()
      
      logger.info(`✅ Commands updated from GitHub (${processedData.commands.length} commands)`)
      
    } catch (error) {
      logger.error('Failed to update commands from GitHub:', error)
      
      // If we have cached data, use it
      if (!this.commandsData) {
        const cached = await this.cache.get(cacheKey)
        if (cached) {
          this.commandsData = cached.data
          this.lastCommandsUpdate = cached.timestamp
          logger.warn('Using stale cached commands data due to GitHub fetch failure')
        } else {
          throw new Error('No commands data available and GitHub fetch failed')
        }
      }
    }
  }

  async processCommandsData(rawData) {
    logger.info('📝 Processing commands data...')
    
    try {
      // Parse commands from markdown content
      const parseResult = await this.pythonBridge.parseMarkdownCommands(rawData.content)
      
      if (!parseResult.success) {
        throw new Error(`Command parsing failed: ${parseResult.error}`)
      }
      
      const commands = parseResult.data.commands || []
      const categories = parseResult.data.categories || {}
      
      // Build command index for fast lookup
      const commandIndex = new Map()
      const aliasIndex = new Map()
      
      commands.forEach(cmd => {
        commandIndex.set(cmd.name, cmd)
        
        // Index aliases
        if (cmd.aliases) {
          cmd.aliases.forEach(alias => {
            aliasIndex.set(alias, cmd.name)
          })
        }
      })
      
      return {
        commands,
        categories,
        commandIndex,
        aliasIndex,
        metadata: {
          totalCommands: commands.length,
          totalCategories: Object.keys(categories).length,
          lastUpdated: Date.now(),
          source: 'github'
        }
      }
      
    } catch (error) {
      logger.error('Commands data processing error:', error)
      throw error
    }
  }

  async validateCommand(command, options) {
    // Basic validation
    if (!command || typeof command !== 'string') {
      return {
        valid: false,
        error: 'Command must be a non-empty string'
      }
    }
    
    // Length validation
    if (command.length > this.config.processing.max_command_length || 1000) {
      return {
        valid: false,
        error: 'Command is too long'
      }
    }
    
    // Check if command exists (if we have commands data)
    if (this.commandsData) {
      const exists = this.commandExists(command)
      if (!exists) {
        const suggestions = await this.getSuggestions(command, 5)
        return {
          valid: false,
          error: `Unknown command: ${command}`,
          suggestions
        }
      }
    }
    
    return { valid: true }
  }

  commandExists(command) {
    if (!this.commandsData) return true // Assume valid if no data loaded yet
    
    const normalized = this.normalizeCommand(command)
    
    // Check direct command
    if (this.commandsData.commandIndex.has(normalized)) {
      return true
    }
    
    // Check aliases
    if (this.commandsData.aliasIndex.has(normalized)) {
      return true
    }
    
    // Check configured aliases
    if (this.commandAliases.has(normalized)) {
      return true
    }
    
    return false
  }

  async getSuggestions(query, limit = 10) {
    if (!this.commandsData) {
      return []
    }
    
    const normalizedQuery = this.normalizeCommand(query)
    const suggestions = []
    
    // Exact matches first
    for (const [cmdName, cmd] of this.commandsData.commandIndex) {
      if (cmdName.includes(normalizedQuery)) {
        suggestions.push({
          command: cmdName,
          description: cmd.description,
          score: this.calculateSimilarity(normalizedQuery, cmdName),
          type: 'exact'
        })
      }
    }
    
    // Fuzzy matches
    for (const [cmdName, cmd] of this.commandsData.commandIndex) {
      if (!cmdName.includes(normalizedQuery)) {
        const score = this.calculateSimilarity(normalizedQuery, cmdName)
        if (score > 0.3) {
          suggestions.push({
            command: cmdName,
            description: cmd.description,
            score,
            type: 'fuzzy'
          })
        }
      }
    }
    
    // Sort by score and limit
    return suggestions
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
  }

  calculateSimilarity(str1, str2) {
    // Simple Levenshtein distance-based similarity
    const longer = str1.length > str2.length ? str1 : str2
    const shorter = str1.length > str2.length ? str2 : str1
    
    if (longer.length === 0) return 1.0
    
    const distance = this.levenshteinDistance(longer, shorter)
    return (longer.length - distance) / longer.length
  }

  levenshteinDistance(str1, str2) {
    const matrix = []
    
    for (let i = 0; i <= str2.length; i++) {
      matrix[i] = [i]
    }
    
    for (let j = 0; j <= str1.length; j++) {
      matrix[0][j] = j
    }
    
    for (let i = 1; i <= str2.length; i++) {
      for (let j = 1; j <= str1.length; j++) {
        if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1]
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          )
        }
      }
    }
    
    return matrix[str2.length][str1.length]
  }

  normalizeCommand(command) {
    let normalized = command.trim().toLowerCase()
    
    // Remove command prefix if present
    const prefix = this.config.commands.prefix || '/'
    if (normalized.startsWith(prefix)) {
      normalized = normalized.substring(prefix.length)
    }
    
    // Resolve aliases
    if (this.commandAliases.has(normalized)) {
      normalized = this.commandAliases.get(normalized)
    }
    
    return normalized
  }

  loadCommandAliases() {
    const aliases = this.config.commands.aliases || {}
    this.commandAliases.clear()
    
    for (const [alias, command] of Object.entries(aliases)) {
      this.commandAliases.set(alias, command)
    }
    
    logger.info(`📋 Loaded ${this.commandAliases.size} command aliases`)
  }

  isCommandsDataStale(timestamp = null) {
    const checkTime = timestamp || this.lastCommandsUpdate
    if (!checkTime) return true
    
    const maxAge = this.config.cache.duration || 3600000 // 1 hour default
    return (Date.now() - checkTime) > maxAge
  }

  setupPeriodicUpdates() {
    const updateInterval = this.config.github.update_interval || 1800000 // 30 minutes
    
    setInterval(async () => {
      try {
        logger.info('🔄 Periodic commands update...')
        await this.updateCommandsFromGitHub()
      } catch (error) {
        logger.error('Periodic update failed:', error)
      }
    }, updateInterval)
    
    logger.info(`⏰ Periodic updates scheduled every ${updateInterval / 1000}s`)
  }

  recordCommandHistory(command, result, options) {
    const record = {
      command,
      success: result.success,
      timestamp: Date.now(),
      processingTime: result.processingTime,
      requestId: result.requestId,
      userAgent: options.userAgent,
      ip: options.ip
    }
    
    this.commandHistory.push(record)
    
    // Keep only last 1000 records
    if (this.commandHistory.length > 1000) {
      this.commandHistory = this.commandHistory.slice(-1000)
    }
  }

  generateRequestId() {
    return `cmd_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  getStats() {
    return {
      totalCommands: this.commandsData?.commands?.length || 0,
      totalCategories: Object.keys(this.commandsData?.categories || {}).length,
      lastUpdate: this.lastCommandsUpdate,
      commandHistory: this.commandHistory.length,
      activeCommands: this.activeCommands.size,
      aliases: this.commandAliases.size
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Command Router...')
    
    if (this.processor) {
      await this.processor.cleanup()
    }
    
    if (this.decisionEngine) {
      await this.decisionEngine.cleanup()
    }
    
    this.activeCommands.clear()
    this.commandHistory.length = 0
    
    logger.info('✅ Command Router cleanup complete')
  }
}

module.exports = CommandRouter