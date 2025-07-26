/**
 * JAEGIS Redis AI Manager
 * Advanced Redis database management for AI agents and learning systems
 * Supports hybrid architecture: self-hosted for development, Redis Cloud for production
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const Redis = require('redis')
const logger = require('../utils/logger')

// Redis Configuration
const REDIS_CONFIG = {
  development: {
    host: 'localhost',
    port: 6379,
    db: 0,
    maxRetries: 3,
    retryDelayOnFailover: 100
  },
  production: {
    // Redis Cloud configuration will be loaded from environment
    url: process.env.REDIS_CLOUD_URL,
    maxRetries: 5,
    retryDelayOnFailover: 200
  }
}

// Data Structure Schemas
const SCHEMAS = {
  agent: {
    prefix: 'agent:',
    fields: {
      id: 'string',
      name: 'string',
      type: 'string',
      capabilities: 'array',
      status: 'string',
      created_at: 'timestamp',
      last_active: 'timestamp',
      performance_score: 'float',
      learning_progress: 'json',
      conversation_history: 'json',
      metadata: 'json'
    }
  },
  conversation: {
    prefix: 'conv:',
    fields: {
      id: 'string',
      participants: 'array',
      topic: 'string',
      messages: 'json',
      started_at: 'timestamp',
      ended_at: 'timestamp',
      summary: 'text',
      insights: 'json',
      status: 'string'
    }
  },
  learning_session: {
    prefix: 'learn:',
    fields: {
      id: 'string',
      agent_id: 'string',
      topic: 'string',
      content: 'json',
      insights: 'json',
      performance_delta: 'float',
      timestamp: 'timestamp',
      source: 'string'
    }
  },
  task: {
    prefix: 'task:',
    fields: {
      id: 'string',
      type: 'string',
      priority: 'integer',
      status: 'string',
      assigned_to: 'string',
      created_at: 'timestamp',
      due_at: 'timestamp',
      completed_at: 'timestamp',
      data: 'json',
      results: 'json'
    }
  }
}

// Agent Status Types
const AGENT_STATUS = {
  ACTIVE: 'active',
  IDLE: 'idle',
  LEARNING: 'learning',
  DISCUSSING: 'discussing',
  WORKING: 'working',
  OFFLINE: 'offline',
  ERROR: 'error'
}

// Task Status Types
const TASK_STATUS = {
  PENDING: 'pending',
  ASSIGNED: 'assigned',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled'
}

class RedisAIManager {
  constructor({ config, errorHandler, performanceMonitor }) {
    this.config = config
    this.errorHandler = errorHandler
    this.performanceMonitor = performanceMonitor
    
    // Redis clients
    this.client = null
    this.subscriber = null
    this.publisher = null
    
    // Configuration
    this.aiConfig = {
      environment: config?.ai?.redis?.environment || 'development',
      maxAgents: config?.ai?.redis?.max_agents || 12000,
      maxConversations: config?.ai?.redis?.max_conversations || 1000,
      maxLearningHistory: config?.ai?.redis?.max_learning_history || 10000,
      enableVectorSearch: config?.ai?.redis?.enable_vector_search !== false,
      enableStreams: config?.ai?.redis?.enable_streams !== false,
      enablePubSub: config?.ai?.redis?.enable_pubsub !== false,
      compressionEnabled: config?.ai?.redis?.compression_enabled !== false,
      ttlDefault: config?.ai?.redis?.ttl_default || 86400000, // 24 hours
      cleanupInterval: config?.ai?.redis?.cleanup_interval || 3600000 // 1 hour
    }
    
    // Scaling configuration based on environment
    if (this.aiConfig.environment === 'production') {
      // Scale down for Redis Cloud Free Tier (30MB limit)
      this.aiConfig.maxAgents = Math.min(this.aiConfig.maxAgents, 50)
      this.aiConfig.maxConversations = Math.min(this.aiConfig.maxConversations, 100)
      this.aiConfig.maxLearningHistory = Math.min(this.aiConfig.maxLearningHistory, 500)
      this.aiConfig.compressionEnabled = true
    }
    
    // Data management
    this.agentRegistry = new Map()
    this.conversationRegistry = new Map()
    this.taskQueue = new Map()
    
    // Performance tracking
    this.metrics = {
      totalOperations: 0,
      successfulOperations: 0,
      failedOperations: 0,
      averageResponseTime: 0,
      cacheHitRate: 0,
      dataSize: 0,
      agentCount: 0,
      conversationCount: 0
    }
    
    // Cleanup intervals
    this.cleanupIntervals = []
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('🗄️ Initializing Redis AI Manager...')
    
    try {
      // Connect to Redis
      await this.connectToRedis()
      
      // Setup data structures
      await this.setupDataStructures()
      
      // Initialize vector search if enabled
      if (this.aiConfig.enableVectorSearch) {
        await this.initializeVectorSearch()
      }
      
      // Setup streams if enabled
      if (this.aiConfig.enableStreams) {
        await this.initializeStreams()
      }
      
      // Setup pub/sub if enabled
      if (this.aiConfig.enablePubSub) {
        await this.initializePubSub()
      }
      
      // Start background processes
      this.startBackgroundProcesses()
      
      this.isInitialized = true
      logger.info(`✅ Redis AI Manager initialized (${this.aiConfig.environment} mode)`)
      
    } catch (error) {
      logger.error('❌ Failed to initialize Redis AI Manager:', error)
      throw error
    }
  }

  async connectToRedis() {
    const redisConfig = this.aiConfig.environment === 'production' 
      ? REDIS_CONFIG.production 
      : REDIS_CONFIG.development
    
    try {
      // Main client
      this.client = Redis.createClient(redisConfig)
      this.client.on('error', (err) => logger.error('Redis Client Error:', err))
      this.client.on('connect', () => logger.info('📡 Redis client connected'))
      await this.client.connect()
      
      // Subscriber client
      this.subscriber = Redis.createClient(redisConfig)
      this.subscriber.on('error', (err) => logger.error('Redis Subscriber Error:', err))
      await this.subscriber.connect()
      
      // Publisher client
      this.publisher = Redis.createClient(redisConfig)
      this.publisher.on('error', (err) => logger.error('Redis Publisher Error:', err))
      await this.publisher.connect()
      
      // Test connection
      const pong = await this.client.ping()
      if (pong !== 'PONG') {
        throw new Error('Redis connection test failed')
      }
      
      logger.info(`✅ Connected to Redis (${this.aiConfig.environment})`)
      
    } catch (error) {
      logger.error('❌ Failed to connect to Redis:', error)
      throw error
    }
  }

  async setupDataStructures() {
    logger.info('🏗️ Setting up Redis data structures...')
    
    try {
      // Create indexes for efficient querying
      await this.createIndexes()
      
      // Initialize counters
      await this.initializeCounters()
      
      // Setup TTL policies
      await this.setupTTLPolicies()
      
      logger.info('✅ Redis data structures setup complete')
      
    } catch (error) {
      logger.warn('⚠️ Some data structures may not be available:', error.message)
    }
  }

  async createIndexes() {
    // Create search indexes for efficient querying
    const indexes = [
      {
        name: 'idx:agents',
        prefix: 'agent:',
        schema: [
          'name', 'TEXT',
          'type', 'TAG',
          'status', 'TAG',
          'capabilities', 'TAG',
          'performance_score', 'NUMERIC',
          'created_at', 'NUMERIC',
          'last_active', 'NUMERIC'
        ]
      },
      {
        name: 'idx:conversations',
        prefix: 'conv:',
        schema: [
          'topic', 'TEXT',
          'participants', 'TAG',
          'status', 'TAG',
          'started_at', 'NUMERIC',
          'ended_at', 'NUMERIC'
        ]
      },
      {
        name: 'idx:tasks',
        prefix: 'task:',
        schema: [
          'type', 'TAG',
          'status', 'TAG',
          'priority', 'NUMERIC',
          'assigned_to', 'TAG',
          'created_at', 'NUMERIC',
          'due_at', 'NUMERIC'
        ]
      }
    ]
    
    for (const index of indexes) {
      try {
        await this.client.ft.create(index.name, index.schema, {
          ON: 'HASH',
          PREFIX: index.prefix
        })
        logger.debug(`📋 Created index: ${index.name}`)
      } catch (error) {
        if (!error.message.includes('Index already exists')) {
          logger.warn(`Failed to create index ${index.name}:`, error.message)
        }
      }
    }
  }

  async initializeCounters() {
    const counters = [
      'agents:count',
      'conversations:count',
      'tasks:count',
      'learning_sessions:count'
    ]
    
    for (const counter of counters) {
      const exists = await this.client.exists(counter)
      if (!exists) {
        await this.client.set(counter, 0)
      }
    }
  }

  async setupTTLPolicies() {
    // Set default TTL for different data types
    const ttlPolicies = {
      'temp:*': 3600,      // 1 hour for temporary data
      'cache:*': 7200,     // 2 hours for cache data
      'session:*': 86400,  // 24 hours for session data
      'log:*': 604800      // 7 days for log data
    }
    
    // Note: TTL policies would be implemented with Redis modules in production
    logger.debug('📋 TTL policies configured')
  }

  async initializeVectorSearch() {
    logger.info('🔍 Initializing vector search capabilities...')
    
    try {
      // Create vector index for agent similarity search
      await this.client.ft.create('idx:agent_vectors', [
        'capabilities_vector', 'VECTOR', 'FLAT', '6', 'TYPE', 'FLOAT32', 'DIM', '384', 'DISTANCE_METRIC', 'COSINE'
      ], {
        ON: 'HASH',
        PREFIX: 'agent_vector:'
      })
      
      logger.info('✅ Vector search initialized')
      
    } catch (error) {
      if (!error.message.includes('Index already exists')) {
        logger.warn('Vector search not available:', error.message)
      }
    }
  }

  async initializeStreams() {
    logger.info('🌊 Initializing Redis Streams...')
    
    const streams = [
      'agent_communications',
      'learning_events',
      'task_updates',
      'system_events'
    ]
    
    for (const stream of streams) {
      try {
        // Create stream if it doesn't exist
        await this.client.xAdd(stream, '*', { init: 'stream_created', timestamp: Date.now() })
        logger.debug(`🌊 Stream created: ${stream}`)
      } catch (error) {
        logger.warn(`Failed to create stream ${stream}:`, error.message)
      }
    }
    
    logger.info('✅ Redis Streams initialized')
  }

  async initializePubSub() {
    logger.info('📢 Initializing Redis Pub/Sub...')
    
    // Subscribe to system channels
    const channels = [
      'agent_status_updates',
      'conversation_events',
      'learning_notifications',
      'task_notifications',
      'system_alerts'
    ]
    
    for (const channel of channels) {
      await this.subscriber.subscribe(channel, (message, channel) => {
        this.handlePubSubMessage(channel, message)
      })
    }
    
    logger.info('✅ Redis Pub/Sub initialized')
  }

  startBackgroundProcesses() {
    // Data cleanup process
    const cleanupInterval = setInterval(async () => {
      await this.performDataCleanup()
    }, this.aiConfig.cleanupInterval)
    this.cleanupIntervals.push(cleanupInterval)
    
    // Metrics collection
    const metricsInterval = setInterval(async () => {
      await this.collectMetrics()
    }, 60000) // Every minute
    this.cleanupIntervals.push(metricsInterval)
    
    // Health monitoring
    const healthInterval = setInterval(async () => {
      await this.monitorHealth()
    }, 30000) // Every 30 seconds
    this.cleanupIntervals.push(healthInterval)
    
    logger.info('🔄 Background processes started')
  }

  // Agent Management
  async createAgent(agentData) {
    const agentId = agentData.id || this.generateId('agent')
    const agent = {
      id: agentId,
      name: agentData.name,
      type: agentData.type || 'general',
      capabilities: agentData.capabilities || [],
      status: AGENT_STATUS.ACTIVE,
      created_at: Date.now(),
      last_active: Date.now(),
      performance_score: agentData.performance_score || 0.5,
      learning_progress: agentData.learning_progress || {},
      conversation_history: [],
      metadata: agentData.metadata || {}
    }
    
    try {
      // Store agent data
      await this.client.hSet(`agent:${agentId}`, agent)
      
      // Update registry
      this.agentRegistry.set(agentId, agent)
      
      // Increment counter
      await this.client.incr('agents:count')
      
      // Create vector representation if vector search is enabled
      if (this.aiConfig.enableVectorSearch && agent.capabilities.length > 0) {
        await this.createAgentVector(agentId, agent.capabilities)
      }
      
      // Publish creation event
      await this.publishEvent('agent_status_updates', {
        type: 'agent_created',
        agent_id: agentId,
        timestamp: Date.now()
      })
      
      logger.info(`🤖 Created agent: ${agentId} (${agent.name})`)
      return agentId
      
    } catch (error) {
      logger.error(`Failed to create agent ${agentId}:`, error)
      throw error
    }
  }

  async getAgent(agentId) {
    try {
      const agent = await this.client.hGetAll(`agent:${agentId}`)
      
      if (Object.keys(agent).length === 0) {
        return null
      }
      
      // Parse JSON fields
      agent.capabilities = JSON.parse(agent.capabilities || '[]')
      agent.learning_progress = JSON.parse(agent.learning_progress || '{}')
      agent.conversation_history = JSON.parse(agent.conversation_history || '[]')
      agent.metadata = JSON.parse(agent.metadata || '{}')
      
      return agent
      
    } catch (error) {
      logger.error(`Failed to get agent ${agentId}:`, error)
      return null
    }
  }

  async updateAgent(agentId, updates) {
    try {
      const agent = await this.getAgent(agentId)
      if (!agent) {
        throw new Error(`Agent ${agentId} not found`)
      }
      
      // Merge updates
      const updatedAgent = { ...agent, ...updates, last_active: Date.now() }
      
      // Store updated data
      await this.client.hSet(`agent:${agentId}`, updatedAgent)
      
      // Update registry
      this.agentRegistry.set(agentId, updatedAgent)
      
      // Update vector if capabilities changed
      if (updates.capabilities && this.aiConfig.enableVectorSearch) {
        await this.createAgentVector(agentId, updates.capabilities)
      }
      
      // Publish update event
      await this.publishEvent('agent_status_updates', {
        type: 'agent_updated',
        agent_id: agentId,
        updates: Object.keys(updates),
        timestamp: Date.now()
      })
      
      return updatedAgent
      
    } catch (error) {
      logger.error(`Failed to update agent ${agentId}:`, error)
      throw error
    }
  }

  async findAgents(criteria) {
    try {
      let query = '*'
      const filters = []
      
      if (criteria.type) {
        filters.push(`@type:{${criteria.type}}`)
      }
      
      if (criteria.status) {
        filters.push(`@status:{${criteria.status}}`)
      }
      
      if (criteria.capabilities) {
        const capFilters = criteria.capabilities.map(cap => `@capabilities:{${cap}}`)
        filters.push(`(${capFilters.join('|')})`)
      }
      
      if (criteria.performance_min) {
        filters.push(`@performance_score:[${criteria.performance_min} +inf]`)
      }
      
      if (filters.length > 0) {
        query = filters.join(' ')
      }
      
      const results = await this.client.ft.search('idx:agents', query, {
        LIMIT: { from: 0, size: criteria.limit || 100 }
      })
      
      const agents = []
      for (let i = 1; i < results.documents.length; i += 2) {
        const agentData = results.documents[i]
        agents.push(await this.parseAgentData(agentData))
      }
      
      return agents
      
    } catch (error) {
      logger.error('Failed to find agents:', error)
      return []
    }
  }

  async createAgentVector(agentId, capabilities) {
    // Create a simple vector representation of capabilities
    // In production, this would use proper embeddings
    const vector = new Array(384).fill(0)
    
    // Simple hash-based vector generation
    for (const capability of capabilities) {
      const hash = this.simpleHash(capability)
      for (let i = 0; i < 10; i++) {
        const index = (hash + i) % 384
        vector[index] += 0.1
      }
    }
    
    // Normalize vector
    const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0))
    if (magnitude > 0) {
      for (let i = 0; i < vector.length; i++) {
        vector[i] /= magnitude
      }
    }
    
    await this.client.hSet(`agent_vector:${agentId}`, {
      agent_id: agentId,
      capabilities_vector: Buffer.from(new Float32Array(vector).buffer)
    })
  }

  // Conversation Management
  async createConversation(conversationData) {
    const convId = conversationData.id || this.generateId('conv')
    const conversation = {
      id: convId,
      participants: conversationData.participants || [],
      topic: conversationData.topic || 'General Discussion',
      messages: [],
      started_at: Date.now(),
      ended_at: null,
      summary: '',
      insights: {},
      status: 'active'
    }
    
    try {
      await this.client.hSet(`conv:${convId}`, conversation)
      this.conversationRegistry.set(convId, conversation)
      await this.client.incr('conversations:count')
      
      // Create stream for conversation messages
      await this.client.xAdd(`conv_stream:${convId}`, '*', {
        type: 'conversation_started',
        participants: JSON.stringify(conversation.participants),
        topic: conversation.topic,
        timestamp: Date.now()
      })
      
      logger.info(`💬 Created conversation: ${convId}`)
      return convId
      
    } catch (error) {
      logger.error(`Failed to create conversation ${convId}:`, error)
      throw error
    }
  }

  async addMessage(conversationId, message) {
    try {
      const conversation = await this.getConversation(conversationId)
      if (!conversation) {
        throw new Error(`Conversation ${conversationId} not found`)
      }
      
      const messageData = {
        id: this.generateId('msg'),
        sender: message.sender,
        content: message.content,
        timestamp: Date.now(),
        metadata: message.metadata || {}
      }
      
      conversation.messages.push(messageData)
      
      // Update conversation
      await this.client.hSet(`conv:${conversationId}`, {
        messages: JSON.stringify(conversation.messages)
      })
      
      // Add to stream
      await this.client.xAdd(`conv_stream:${conversationId}`, '*', {
        type: 'message_added',
        sender: message.sender,
        content: message.content,
        timestamp: Date.now()
      })
      
      // Add to agent communications stream
      await this.client.xAdd('agent_communications', '*', {
        conversation_id: conversationId,
        sender: message.sender,
        content: message.content,
        timestamp: Date.now()
      })
      
      return messageData.id
      
    } catch (error) {
      logger.error(`Failed to add message to conversation ${conversationId}:`, error)
      throw error
    }
  }

  async getConversation(conversationId) {
    try {
      const conversation = await this.client.hGetAll(`conv:${conversationId}`)
      
      if (Object.keys(conversation).length === 0) {
        return null
      }
      
      // Parse JSON fields
      conversation.participants = JSON.parse(conversation.participants || '[]')
      conversation.messages = JSON.parse(conversation.messages || '[]')
      conversation.insights = JSON.parse(conversation.insights || '{}')
      
      return conversation
      
    } catch (error) {
      logger.error(`Failed to get conversation ${conversationId}:`, error)
      return null
    }
  }

  // Task Management
  async createTask(taskData) {
    const taskId = taskData.id || this.generateId('task')
    const task = {
      id: taskId,
      type: taskData.type || 'general',
      priority: taskData.priority || 5,
      status: TASK_STATUS.PENDING,
      assigned_to: taskData.assigned_to || null,
      created_at: Date.now(),
      due_at: taskData.due_at || null,
      completed_at: null,
      data: taskData.data || {},
      results: {}
    }
    
    try {
      await this.client.hSet(`task:${taskId}`, task)
      this.taskQueue.set(taskId, task)
      await this.client.incr('tasks:count')
      
      // Add to task stream
      await this.client.xAdd('task_updates', '*', {
        type: 'task_created',
        task_id: taskId,
        task_type: task.type,
        priority: task.priority,
        timestamp: Date.now()
      })
      
      logger.info(`📋 Created task: ${taskId} (${task.type})`)
      return taskId
      
    } catch (error) {
      logger.error(`Failed to create task ${taskId}:`, error)
      throw error
    }
  }

  async assignTask(taskId, agentId) {
    try {
      const task = await this.getTask(taskId)
      if (!task) {
        throw new Error(`Task ${taskId} not found`)
      }
      
      const agent = await this.getAgent(agentId)
      if (!agent) {
        throw new Error(`Agent ${agentId} not found`)
      }
      
      // Update task
      await this.client.hSet(`task:${taskId}`, {
        assigned_to: agentId,
        status: TASK_STATUS.ASSIGNED
      })
      
      // Update agent status
      await this.updateAgent(agentId, { status: AGENT_STATUS.WORKING })
      
      // Publish assignment event
      await this.publishEvent('task_notifications', {
        type: 'task_assigned',
        task_id: taskId,
        agent_id: agentId,
        timestamp: Date.now()
      })
      
      logger.info(`📋 Assigned task ${taskId} to agent ${agentId}`)
      
    } catch (error) {
      logger.error(`Failed to assign task ${taskId}:`, error)
      throw error
    }
  }

  async getTask(taskId) {
    try {
      const task = await this.client.hGetAll(`task:${taskId}`)
      
      if (Object.keys(task).length === 0) {
        return null
      }
      
      // Parse JSON fields
      task.data = JSON.parse(task.data || '{}')
      task.results = JSON.parse(task.results || '{}')
      
      return task
      
    } catch (error) {
      logger.error(`Failed to get task ${taskId}:`, error)
      return null
    }
  }

  // Learning Session Management
  async recordLearningSession(sessionData) {
    const sessionId = this.generateId('learn')
    const session = {
      id: sessionId,
      agent_id: sessionData.agent_id,
      topic: sessionData.topic,
      content: sessionData.content || {},
      insights: sessionData.insights || {},
      performance_delta: sessionData.performance_delta || 0,
      timestamp: Date.now(),
      source: sessionData.source || 'unknown'
    }
    
    try {
      await this.client.hSet(`learn:${sessionId}`, session)
      await this.client.incr('learning_sessions:count')
      
      // Add to learning events stream
      await this.client.xAdd('learning_events', '*', {
        type: 'learning_session',
        agent_id: session.agent_id,
        topic: session.topic,
        performance_delta: session.performance_delta,
        timestamp: Date.now()
      })
      
      // Update agent learning progress
      if (session.agent_id) {
        const agent = await this.getAgent(session.agent_id)
        if (agent) {
          const learningProgress = agent.learning_progress || {}
          learningProgress[session.topic] = (learningProgress[session.topic] || 0) + session.performance_delta
          
          await this.updateAgent(session.agent_id, {
            learning_progress: learningProgress,
            performance_score: Math.max(0, Math.min(1, agent.performance_score + session.performance_delta))
          })
        }
      }
      
      logger.info(`📚 Recorded learning session: ${sessionId}`)
      return sessionId
      
    } catch (error) {
      logger.error(`Failed to record learning session:`, error)
      throw error
    }
  }

  // Utility Methods
  generateId(prefix) {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  simpleHash(str) {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash // Convert to 32-bit integer
    }
    return Math.abs(hash)
  }

  async parseAgentData(data) {
    // Parse agent data from Redis response
    const agent = {}
    for (let i = 0; i < data.length; i += 2) {
      const key = data[i]
      const value = data[i + 1]
      
      if (['capabilities', 'learning_progress', 'conversation_history', 'metadata'].includes(key)) {
        agent[key] = JSON.parse(value || '{}')
      } else {
        agent[key] = value
      }
    }
    return agent
  }

  // Event Handling
  async publishEvent(channel, data) {
    try {
      await this.publisher.publish(channel, JSON.stringify(data))
    } catch (error) {
      logger.error(`Failed to publish event to ${channel}:`, error)
    }
  }

  handlePubSubMessage(channel, message) {
    try {
      const data = JSON.parse(message)
      logger.debug(`📢 Received message on ${channel}:`, data.type)
      
      // Handle different message types
      switch (channel) {
        case 'agent_status_updates':
          this.handleAgentStatusUpdate(data)
          break
        case 'conversation_events':
          this.handleConversationEvent(data)
          break
        case 'learning_notifications':
          this.handleLearningNotification(data)
          break
        case 'task_notifications':
          this.handleTaskNotification(data)
          break
        case 'system_alerts':
          this.handleSystemAlert(data)
          break
      }
      
    } catch (error) {
      logger.error(`Failed to handle pub/sub message:`, error)
    }
  }

  handleAgentStatusUpdate(data) {
    // Handle agent status updates
    logger.debug(`🤖 Agent ${data.agent_id}: ${data.type}`)
  }

  handleConversationEvent(data) {
    // Handle conversation events
    logger.debug(`💬 Conversation ${data.conversation_id}: ${data.type}`)
  }

  handleLearningNotification(data) {
    // Handle learning notifications
    logger.debug(`📚 Learning event: ${data.type}`)
  }

  handleTaskNotification(data) {
    // Handle task notifications
    logger.debug(`📋 Task ${data.task_id}: ${data.type}`)
  }

  handleSystemAlert(data) {
    // Handle system alerts
    logger.warn(`🚨 System alert: ${data.type} - ${data.message}`)
  }

  // Background Processes
  async performDataCleanup() {
    try {
      const now = Date.now()
      const cutoff = now - (7 * 24 * 60 * 60 * 1000) // 7 days
      
      // Clean up old temporary data
      const tempKeys = await this.client.keys('temp:*')
      for (const key of tempKeys) {
        const ttl = await this.client.ttl(key)
        if (ttl === -1) { // No TTL set
          await this.client.expire(key, 3600) // Set 1 hour TTL
        }
      }
      
      // Clean up old log entries
      const logKeys = await this.client.keys('log:*')
      for (const key of logKeys) {
        const createdAt = await this.client.hGet(key, 'created_at')
        if (createdAt && parseInt(createdAt) < cutoff) {
          await this.client.del(key)
        }
      }
      
      // Trim streams to prevent unlimited growth
      const streams = ['agent_communications', 'learning_events', 'task_updates', 'system_events']
      for (const stream of streams) {
        try {
          await this.client.xTrim(stream, 'MAXLEN', '~', 10000)
        } catch (error) {
          // Stream might not exist
        }
      }
      
      logger.debug('🧹 Data cleanup completed')
      
    } catch (error) {
      logger.error('Data cleanup failed:', error)
    }
  }

  async collectMetrics() {
    try {
      // Collect basic metrics
      const info = await this.client.info('memory')
      const memoryUsage = this.parseRedisInfo(info)
      
      this.metrics.dataSize = memoryUsage.used_memory || 0
      this.metrics.agentCount = parseInt(await this.client.get('agents:count') || '0')
      this.metrics.conversationCount = parseInt(await this.client.get('conversations:count') || '0')
      
      // Update performance monitor if available
      if (this.performanceMonitor) {
        this.performanceMonitor.recordMetric('redis_memory_usage', this.metrics.dataSize)
        this.performanceMonitor.recordMetric('redis_agent_count', this.metrics.agentCount)
        this.performanceMonitor.recordMetric('redis_conversation_count', this.metrics.conversationCount)
      }
      
    } catch (error) {
      logger.error('Metrics collection failed:', error)
    }
  }

  async monitorHealth() {
    try {
      const start = Date.now()
      await this.client.ping()
      const latency = Date.now() - start
      
      if (latency > 1000) {
        logger.warn(`⚠️ High Redis latency: ${latency}ms`)
      }
      
      // Check memory usage for production environment
      if (this.aiConfig.environment === 'production') {
        const info = await this.client.info('memory')
        const memoryInfo = this.parseRedisInfo(info)
        const usedMemory = memoryInfo.used_memory || 0
        const maxMemory = 30 * 1024 * 1024 // 30MB for free tier
        
        if (usedMemory > maxMemory * 0.8) {
          logger.warn(`⚠️ Redis memory usage high: ${(usedMemory / 1024 / 1024).toFixed(2)}MB`)
          await this.performDataCleanup()
        }
      }
      
    } catch (error) {
      logger.error('Health monitoring failed:', error)
    }
  }

  parseRedisInfo(info) {
    const lines = info.split('\r\n')
    const result = {}
    
    for (const line of lines) {
      if (line.includes(':')) {
        const [key, value] = line.split(':')
        result[key] = isNaN(value) ? value : parseInt(value)
      }
    }
    
    return result
  }

  // Statistics and Reporting
  getUsageReport() {
    return {
      timestamp: Date.now(),
      environment: this.aiConfig.environment,
      metrics: { ...this.metrics },
      configuration: {
        maxAgents: this.aiConfig.maxAgents,
        maxConversations: this.aiConfig.maxConversations,
        maxLearningHistory: this.aiConfig.maxLearningHistory,
        vectorSearchEnabled: this.aiConfig.enableVectorSearch,
        streamsEnabled: this.aiConfig.enableStreams,
        pubSubEnabled: this.aiConfig.enablePubSub
      },
      registries: {
        agents: this.agentRegistry.size,
        conversations: this.conversationRegistry.size,
        tasks: this.taskQueue.size
      }
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Redis AI Manager...')
    
    try {
      // Clear intervals
      this.cleanupIntervals.forEach(interval => clearInterval(interval))
      this.cleanupIntervals.length = 0
      
      // Close Redis connections
      if (this.client) {
        await this.client.quit()
      }
      if (this.subscriber) {
        await this.subscriber.quit()
      }
      if (this.publisher) {
        await this.publisher.quit()
      }
      
      // Clear registries
      this.agentRegistry.clear()
      this.conversationRegistry.clear()
      this.taskQueue.clear()
      
      this.isInitialized = false
      logger.info('✅ Redis AI Manager cleanup complete')
      
    } catch (error) {
      logger.error('Cleanup failed:', error)
    }
  }
}

module.exports = {
  RedisAIManager,
  AGENT_STATUS,
  TASK_STATUS,
  SCHEMAS
}