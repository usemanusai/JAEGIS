/**
 * JAEGIS Context Manager
 * Agent context management and state persistence system
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

// Context types
const CONTEXT_TYPES = {
  USER: 'user',
  SESSION: 'session',
  COMMAND: 'command',
  AGENT: 'agent',
  SYSTEM: 'system',
  WORKFLOW: 'workflow'
}

// Context scopes
const CONTEXT_SCOPES = {
  GLOBAL: 'global',
  USER: 'user',
  SESSION: 'session',
  REQUEST: 'request',
  TEMPORARY: 'temporary'
}

// State persistence levels
const PERSISTENCE_LEVELS = {
  NONE: 'none',
  MEMORY: 'memory',
  CACHE: 'cache',
  PERSISTENT: 'persistent'
}

class ContextManager {
  constructor({ config, cache }) {
    this.config = config
    this.cache = cache
    
    // Context storage
    this.contexts = new Map()
    this.sessions = new Map()
    this.workflows = new Map()
    this.agentStates = new Map()
    
    // Context configuration
    this.contextConfig = {
      maxContextSize: config?.context?.max_size || 10000,
      maxSessions: config?.context?.max_sessions || 1000,
      sessionTimeout: config?.context?.session_timeout || 3600000, // 1 hour
      persistenceLevel: config?.context?.persistence_level || PERSISTENCE_LEVELS.CACHE,
      autoCleanup: config?.context?.auto_cleanup !== false,
      cleanupInterval: config?.context?.cleanup_interval || 300000 // 5 minutes
    }
    
    // Context templates
    this.contextTemplates = new Map()
    this.contextValidators = new Map()
    this.contextTransformers = new Map()
    
    // Event tracking
    this.contextEvents = []
    this.maxEvents = 1000
    
    // Cleanup interval
    this.cleanupInterval = null
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('🧠 Initializing Context Manager...')
    
    try {
      // Setup context templates
      this.setupContextTemplates()
      
      // Setup validators
      this.setupContextValidators()
      
      // Setup transformers
      this.setupContextTransformers()
      
      // Load persistent contexts
      await this.loadPersistentContexts()
      
      // Setup cleanup
      if (this.contextConfig.autoCleanup) {
        this.setupCleanup()
      }
      
      this.isInitialized = true
      logger.info('✅ Context Manager initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Context Manager:', error)
      throw error
    }
  }

  // Context creation and management
  async createContext(type, scope, data = {}, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Context Manager not initialized')
    }
    
    const contextId = this.generateContextId(type, scope)
    
    const context = {
      id: contextId,
      type,
      scope,
      data: { ...data },
      metadata: {
        createdAt: Date.now(),
        updatedAt: Date.now(),
        accessCount: 0,
        lastAccess: Date.now(),
        version: 1,
        ...options.metadata
      },
      options: {
        ttl: options.ttl || this.getDefaultTTL(scope),
        persistence: options.persistence || this.getDefaultPersistence(scope),
        maxSize: options.maxSize || this.contextConfig.maxContextSize,
        ...options
      }
    }
    
    // Validate context
    await this.validateContext(context)
    
    // Apply transformations
    await this.transformContext(context)
    
    // Store context
    this.contexts.set(contextId, context)
    
    // Persist if required
    if (context.options.persistence !== PERSISTENCE_LEVELS.NONE) {
      await this.persistContext(context)
    }
    
    // Record event
    this.recordContextEvent('created', contextId, { type, scope })
    
    logger.debug(`🧠 Context created: ${contextId}`, { type, scope })
    
    return contextId
  }

  async getContext(contextId, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Context Manager not initialized')
    }
    
    // Try memory first
    let context = this.contexts.get(contextId)
    
    if (!context && options.loadFromPersistence !== false) {
      // Try to load from persistence
      context = await this.loadContext(contextId)
      
      if (context) {
        this.contexts.set(contextId, context)
      }
    }
    
    if (!context) {
      return null
    }
    
    // Update access metadata
    context.metadata.accessCount++
    context.metadata.lastAccess = Date.now()
    
    // Check TTL
    if (this.isContextExpired(context)) {
      await this.deleteContext(contextId)
      return null
    }
    
    // Record event
    this.recordContextEvent('accessed', contextId)
    
    return context
  }

  async updateContext(contextId, updates, options = {}) {
    const context = await this.getContext(contextId)
    
    if (!context) {
      throw new Error(`Context not found: ${contextId}`)
    }
    
    // Merge updates
    if (updates.data) {
      if (options.merge !== false) {
        context.data = { ...context.data, ...updates.data }
      } else {
        context.data = updates.data
      }
    }
    
    if (updates.metadata) {
      context.metadata = { ...context.metadata, ...updates.metadata }
    }
    
    if (updates.options) {
      context.options = { ...context.options, ...updates.options }
    }
    
    // Update metadata
    context.metadata.updatedAt = Date.now()
    context.metadata.version++
    
    // Validate updated context
    await this.validateContext(context)
    
    // Apply transformations
    await this.transformContext(context)
    
    // Persist if required
    if (context.options.persistence !== PERSISTENCE_LEVELS.NONE) {
      await this.persistContext(context)
    }
    
    // Record event
    this.recordContextEvent('updated', contextId, { updates })
    
    logger.debug(`🧠 Context updated: ${contextId}`)
    
    return context
  }

  async deleteContext(contextId) {
    const context = this.contexts.get(contextId)
    
    if (context) {
      // Remove from memory
      this.contexts.delete(contextId)
      
      // Remove from persistence
      if (context.options.persistence !== PERSISTENCE_LEVELS.NONE) {
        await this.removePersistentContext(contextId)
      }
      
      // Record event
      this.recordContextEvent('deleted', contextId)
      
      logger.debug(`🧠 Context deleted: ${contextId}`)
      
      return true
    }
    
    return false
  }

  // Session management
  async createSession(userId, data = {}, options = {}) {
    const sessionId = this.generateSessionId(userId)
    
    const session = {
      id: sessionId,
      userId,
      data: { ...data },
      contexts: new Set(),
      metadata: {
        createdAt: Date.now(),
        updatedAt: Date.now(),
        lastActivity: Date.now(),
        commandCount: 0,
        ...options.metadata
      },
      options: {
        timeout: options.timeout || this.contextConfig.sessionTimeout,
        maxContexts: options.maxContexts || 100,
        ...options
      }
    }
    
    this.sessions.set(sessionId, session)
    
    // Create session context
    await this.createContext(CONTEXT_TYPES.SESSION, CONTEXT_SCOPES.SESSION, {
      sessionId,
      userId,
      ...data
    }, {
      persistence: PERSISTENCE_LEVELS.CACHE,
      ttl: session.options.timeout
    })
    
    logger.debug(`🧠 Session created: ${sessionId} for user: ${userId}`)
    
    return sessionId
  }

  async getSession(sessionId) {
    const session = this.sessions.get(sessionId)
    
    if (!session) {
      return null
    }
    
    // Check timeout
    if (this.isSessionExpired(session)) {
      await this.deleteSession(sessionId)
      return null
    }
    
    // Update activity
    session.metadata.lastActivity = Date.now()
    
    return session
  }

  async updateSession(sessionId, updates) {
    const session = await this.getSession(sessionId)
    
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`)
    }
    
    // Merge updates
    if (updates.data) {
      session.data = { ...session.data, ...updates.data }
    }
    
    if (updates.metadata) {
      session.metadata = { ...session.metadata, ...updates.metadata }
    }
    
    session.metadata.updatedAt = Date.now()
    session.metadata.lastActivity = Date.now()
    
    logger.debug(`🧠 Session updated: ${sessionId}`)
    
    return session
  }

  async deleteSession(sessionId) {
    const session = this.sessions.get(sessionId)
    
    if (session) {
      // Delete associated contexts
      for (const contextId of session.contexts) {
        await this.deleteContext(contextId)
      }
      
      // Remove session
      this.sessions.delete(sessionId)
      
      logger.debug(`🧠 Session deleted: ${sessionId}`)
      
      return true
    }
    
    return false
  }

  // Workflow context management
  async createWorkflow(name, steps, data = {}, options = {}) {
    const workflowId = this.generateWorkflowId(name)
    
    const workflow = {
      id: workflowId,
      name,
      steps,
      currentStep: 0,
      data: { ...data },
      state: 'initialized',
      metadata: {
        createdAt: Date.now(),
        updatedAt: Date.now(),
        startedAt: null,
        completedAt: null,
        ...options.metadata
      },
      options: {
        timeout: options.timeout || 3600000, // 1 hour
        maxRetries: options.maxRetries || 3,
        ...options
      }
    }
    
    this.workflows.set(workflowId, workflow)
    
    // Create workflow context
    await this.createContext(CONTEXT_TYPES.WORKFLOW, CONTEXT_SCOPES.USER, {
      workflowId,
      name,
      steps,
      ...data
    }, {
      persistence: PERSISTENCE_LEVELS.PERSISTENT,
      ttl: workflow.options.timeout
    })
    
    logger.debug(`🧠 Workflow created: ${workflowId}`)
    
    return workflowId
  }

  async getWorkflow(workflowId) {
    return this.workflows.get(workflowId)
  }

  async updateWorkflow(workflowId, updates) {
    const workflow = this.workflows.get(workflowId)
    
    if (!workflow) {
      throw new Error(`Workflow not found: ${workflowId}`)
    }
    
    // Merge updates
    Object.assign(workflow, updates)
    workflow.metadata.updatedAt = Date.now()
    
    // Update workflow context
    const contextId = this.generateContextId(CONTEXT_TYPES.WORKFLOW, CONTEXT_SCOPES.USER)
    await this.updateContext(contextId, { data: workflow })
    
    logger.debug(`🧠 Workflow updated: ${workflowId}`)
    
    return workflow
  }

  // Agent state management
  async setAgentState(agentId, state, options = {}) {
    const stateId = `agent:${agentId}`
    
    const agentState = {
      agentId,
      state,
      metadata: {
        updatedAt: Date.now(),
        version: (this.agentStates.get(stateId)?.metadata?.version || 0) + 1
      },
      options
    }
    
    this.agentStates.set(stateId, agentState)
    
    // Create/update agent context
    await this.createContext(CONTEXT_TYPES.AGENT, CONTEXT_SCOPES.GLOBAL, {
      agentId,
      state,
      ...options.data
    }, {
      persistence: PERSISTENCE_LEVELS.CACHE,
      ttl: options.ttl || 3600000
    })
    
    logger.debug(`🧠 Agent state set: ${agentId}`)
    
    return agentState
  }

  async getAgentState(agentId) {
    const stateId = `agent:${agentId}`
    return this.agentStates.get(stateId)
  }

  // Context templates
  setupContextTemplates() {
    // User context template
    this.contextTemplates.set(CONTEXT_TYPES.USER, {
      required: ['userId'],
      optional: ['preferences', 'history', 'permissions'],
      defaults: {
        preferences: {},
        history: [],
        permissions: []
      }
    })
    
    // Session context template
    this.contextTemplates.set(CONTEXT_TYPES.SESSION, {
      required: ['sessionId', 'userId'],
      optional: ['startTime', 'lastActivity', 'commands'],
      defaults: {
        startTime: Date.now(),
        lastActivity: Date.now(),
        commands: []
      }
    })
    
    // Command context template
    this.contextTemplates.set(CONTEXT_TYPES.COMMAND, {
      required: ['command', 'executionId'],
      optional: ['parameters', 'user', 'session'],
      defaults: {
        parameters: {},
        timestamp: Date.now()
      }
    })
    
    // Agent context template
    this.contextTemplates.set(CONTEXT_TYPES.AGENT, {
      required: ['agentId'],
      optional: ['state', 'configuration', 'metrics'],
      defaults: {
        state: 'idle',
        configuration: {},
        metrics: {}
      }
    })
    
    // Workflow context template
    this.contextTemplates.set(CONTEXT_TYPES.WORKFLOW, {
      required: ['workflowId', 'name'],
      optional: ['steps', 'currentStep', 'data'],
      defaults: {
        steps: [],
        currentStep: 0,
        data: {}
      }
    })
  }

  setupContextValidators() {
    // User context validator
    this.contextValidators.set(CONTEXT_TYPES.USER, async (context) => {
      if (!context.data.userId) {
        throw new Error('User context requires userId')
      }
      
      if (context.data.permissions && !Array.isArray(context.data.permissions)) {
        throw new Error('User permissions must be an array')
      }
    })
    
    // Session context validator
    this.contextValidators.set(CONTEXT_TYPES.SESSION, async (context) => {
      if (!context.data.sessionId || !context.data.userId) {
        throw new Error('Session context requires sessionId and userId')
      }
    })
    
    // Command context validator
    this.contextValidators.set(CONTEXT_TYPES.COMMAND, async (context) => {
      if (!context.data.command || !context.data.executionId) {
        throw new Error('Command context requires command and executionId')
      }
    })
    
    // Agent context validator
    this.contextValidators.set(CONTEXT_TYPES.AGENT, async (context) => {
      if (!context.data.agentId) {
        throw new Error('Agent context requires agentId')
      }
    })
    
    // Workflow context validator
    this.contextValidators.set(CONTEXT_TYPES.WORKFLOW, async (context) => {
      if (!context.data.workflowId || !context.data.name) {
        throw new Error('Workflow context requires workflowId and name')
      }
    })
  }

  setupContextTransformers() {
    // User context transformer
    this.contextTransformers.set(CONTEXT_TYPES.USER, async (context) => {
      // Sanitize sensitive data
      if (context.data.password) {
        delete context.data.password
      }
      
      // Ensure history is limited
      if (context.data.history && context.data.history.length > 100) {
        context.data.history = context.data.history.slice(-100)
      }
    })
    
    // Session context transformer
    this.contextTransformers.set(CONTEXT_TYPES.SESSION, async (context) => {
      // Ensure commands array is limited
      if (context.data.commands && context.data.commands.length > 50) {
        context.data.commands = context.data.commands.slice(-50)
      }
    })
    
    // Command context transformer
    this.contextTransformers.set(CONTEXT_TYPES.COMMAND, async (context) => {
      // Add timestamp if not present
      if (!context.data.timestamp) {
        context.data.timestamp = Date.now()
      }
      
      // Sanitize parameters
      if (context.data.parameters) {
        context.data.parameters = this.sanitizeParameters(context.data.parameters)
      }
    })
  }

  // Context validation and transformation
  async validateContext(context) {
    const validator = this.contextValidators.get(context.type)
    
    if (validator) {
      await validator(context)
    }
    
    // Check size limits
    const contextSize = JSON.stringify(context).length
    if (contextSize > context.options.maxSize) {
      throw new Error(`Context size (${contextSize}) exceeds maximum (${context.options.maxSize})`)
    }
  }

  async transformContext(context) {
    const transformer = this.contextTransformers.get(context.type)
    
    if (transformer) {
      await transformer(context)
    }
  }

  // Persistence
  async persistContext(context) {
    const persistenceLevel = context.options.persistence
    
    switch (persistenceLevel) {
      case PERSISTENCE_LEVELS.CACHE:
        await this.cache.set(`context:${context.id}`, context, context.options.ttl)
        break
      case PERSISTENCE_LEVELS.PERSISTENT:
        // In a real implementation, this would save to a database
        await this.cache.set(`persistent:context:${context.id}`, context, 0) // No TTL
        break
    }
  }

  async loadContext(contextId) {
    try {
      // Try cache first
      let context = await this.cache.get(`context:${contextId}`)
      
      if (!context) {
        // Try persistent storage
        context = await this.cache.get(`persistent:context:${contextId}`)
      }
      
      return context
    } catch (error) {
      logger.error(`Failed to load context ${contextId}:`, error)
      return null
    }
  }

  async loadPersistentContexts() {
    try {
      // Load all persistent contexts
      // In a real implementation, this would query a database
      logger.debug('🧠 Loading persistent contexts...')
    } catch (error) {
      logger.error('Failed to load persistent contexts:', error)
    }
  }

  async removePersistentContext(contextId) {
    try {
      await this.cache.delete(`context:${contextId}`)
      await this.cache.delete(`persistent:context:${contextId}`)
    } catch (error) {
      logger.error(`Failed to remove persistent context ${contextId}:`, error)
    }
  }

  // Utility methods
  generateContextId(type, scope) {
    return `ctx_${type}_${scope}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  generateSessionId(userId) {
    return `sess_${userId}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  generateWorkflowId(name) {
    return `wf_${name}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  getDefaultTTL(scope) {
    const ttlMap = {
      [CONTEXT_SCOPES.GLOBAL]: 86400000, // 24 hours
      [CONTEXT_SCOPES.USER]: 3600000,    // 1 hour
      [CONTEXT_SCOPES.SESSION]: 1800000, // 30 minutes
      [CONTEXT_SCOPES.REQUEST]: 300000,  // 5 minutes
      [CONTEXT_SCOPES.TEMPORARY]: 60000  // 1 minute
    }
    
    return ttlMap[scope] || 3600000
  }

  getDefaultPersistence(scope) {
    const persistenceMap = {
      [CONTEXT_SCOPES.GLOBAL]: PERSISTENCE_LEVELS.PERSISTENT,
      [CONTEXT_SCOPES.USER]: PERSISTENCE_LEVELS.CACHE,
      [CONTEXT_SCOPES.SESSION]: PERSISTENCE_LEVELS.CACHE,
      [CONTEXT_SCOPES.REQUEST]: PERSISTENCE_LEVELS.MEMORY,
      [CONTEXT_SCOPES.TEMPORARY]: PERSISTENCE_LEVELS.NONE
    }
    
    return persistenceMap[scope] || PERSISTENCE_LEVELS.MEMORY
  }

  isContextExpired(context) {
    if (!context.options.ttl) return false
    
    const age = Date.now() - context.metadata.createdAt
    return age > context.options.ttl
  }

  isSessionExpired(session) {
    const age = Date.now() - session.metadata.lastActivity
    return age > session.options.timeout
  }

  sanitizeParameters(parameters) {
    const sanitized = {}
    
    for (const [key, value] of Object.entries(parameters)) {
      if (typeof value === 'string') {
        // Remove potentially dangerous content
        sanitized[key] = value.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      } else {
        sanitized[key] = value
      }
    }
    
    return sanitized
  }

  recordContextEvent(event, contextId, data = {}) {
    const eventRecord = {
      event,
      contextId,
      data,
      timestamp: Date.now()
    }
    
    this.contextEvents.push(eventRecord)
    
    // Trim events
    if (this.contextEvents.length > this.maxEvents) {
      this.contextEvents = this.contextEvents.slice(-this.maxEvents)
    }
  }

  // Cleanup
  setupCleanup() {
    this.cleanupInterval = setInterval(() => {
      this.performCleanup()
    }, this.contextConfig.cleanupInterval)
    
    logger.debug('🧠 Context cleanup scheduled')
  }

  async performCleanup() {
    try {
      let cleaned = 0
      
      // Clean expired contexts
      for (const [contextId, context] of this.contexts.entries()) {
        if (this.isContextExpired(context)) {
          await this.deleteContext(contextId)
          cleaned++
        }
      }
      
      // Clean expired sessions
      for (const [sessionId, session] of this.sessions.entries()) {
        if (this.isSessionExpired(session)) {
          await this.deleteSession(sessionId)
          cleaned++
        }
      }
      
      // Clean old events
      const cutoff = Date.now() - 86400000 // 24 hours
      this.contextEvents = this.contextEvents.filter(event => event.timestamp > cutoff)
      
      if (cleaned > 0) {
        logger.debug(`🧠 Context cleanup: removed ${cleaned} expired items`)
      }
      
    } catch (error) {
      logger.error('Context cleanup error:', error)
    }
  }

  // Statistics and monitoring
  getContextStats() {
    const stats = {
      contexts: {
        total: this.contexts.size,
        byType: {},
        byScope: {}
      },
      sessions: {
        total: this.sessions.size,
        active: 0
      },
      workflows: {
        total: this.workflows.size,
        byState: {}
      },
      agentStates: {
        total: this.agentStates.size
      },
      events: {
        total: this.contextEvents.length,
        recent: this.contextEvents.slice(-10)
      }
    }
    
    // Count contexts by type and scope
    for (const context of this.contexts.values()) {
      stats.contexts.byType[context.type] = (stats.contexts.byType[context.type] || 0) + 1
      stats.contexts.byScope[context.scope] = (stats.contexts.byScope[context.scope] || 0) + 1
    }
    
    // Count active sessions
    const now = Date.now()
    for (const session of this.sessions.values()) {
      if (!this.isSessionExpired(session)) {
        stats.sessions.active++
      }
    }
    
    // Count workflows by state
    for (const workflow of this.workflows.values()) {
      stats.workflows.byState[workflow.state] = (stats.workflows.byState[workflow.state] || 0) + 1
    }
    
    return stats
  }

  // Context queries
  async findContexts(criteria) {
    const results = []
    
    for (const context of this.contexts.values()) {
      let matches = true
      
      if (criteria.type && context.type !== criteria.type) {
        matches = false
      }
      
      if (criteria.scope && context.scope !== criteria.scope) {
        matches = false
      }
      
      if (criteria.userId && context.data.userId !== criteria.userId) {
        matches = false
      }
      
      if (criteria.sessionId && context.data.sessionId !== criteria.sessionId) {
        matches = false
      }
      
      if (matches) {
        results.push(context)
      }
    }
    
    return results
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Context Manager...')
    
    // Clear cleanup interval
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval)
      this.cleanupInterval = null
    }
    
    // Save persistent contexts
    for (const context of this.contexts.values()) {
      if (context.options.persistence === PERSISTENCE_LEVELS.PERSISTENT) {
        await this.persistContext(context)
      }
    }
    
    // Clear data structures
    this.contexts.clear()
    this.sessions.clear()
    this.workflows.clear()
    this.agentStates.clear()
    this.contextTemplates.clear()
    this.contextValidators.clear()
    this.contextTransformers.clear()
    this.contextEvents.length = 0
    
    this.isInitialized = false
    logger.info('✅ Context Manager cleanup complete')
  }
}

module.exports = {
  ContextManager,
  CONTEXT_TYPES,
  CONTEXT_SCOPES,
  PERSISTENCE_LEVELS
}