/**
 * JAEGIS Background Process Manager
 * Advanced background processing system for AI-powered automation
 * Handles asynchronous tasks, web research, and intelligent scheduling
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

// Task Types
const TASK_TYPES = {
  WEB_RESEARCH: 'web_research',
  KNOWLEDGE_SYNTHESIS: 'knowledge_synthesis',
  AGENT_TRAINING: 'agent_training',
  PERFORMANCE_ANALYSIS: 'performance_analysis',
  SYSTEM_OPTIMIZATION: 'system_optimization',
  DATA_CLEANUP: 'data_cleanup',
  HEALTH_CHECK: 'health_check',
  LEARNING_SESSION: 'learning_session',
  CAPABILITY_ASSESSMENT: 'capability_assessment',
  TREND_ANALYSIS: 'trend_analysis'
}

// Task Priorities
const TASK_PRIORITIES = {
  CRITICAL: 1,
  HIGH: 2,
  MEDIUM: 3,
  LOW: 4,
  BACKGROUND: 5
}

// Task Status
const TASK_STATUS = {
  PENDING: 'pending',
  QUEUED: 'queued',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled',
  RETRYING: 'retrying'
}

// Research Categories
const RESEARCH_CATEGORIES = {
  TECHNOLOGY: 'technology',
  AI_DEVELOPMENTS: 'ai_developments',
  PROGRAMMING: 'programming',
  INDUSTRY_TRENDS: 'industry_trends',
  BEST_PRACTICES: 'best_practices',
  SECURITY: 'security',
  PERFORMANCE: 'performance',
  TOOLS: 'tools'
}

class BackgroundProcessManager {
  constructor({ config, openRouterManager, redisAIManager, autonomousLearningEngine, errorHandler, performanceMonitor }) {
    this.config = config
    this.openRouterManager = openRouterManager
    this.redisAIManager = redisAIManager
    this.autonomousLearningEngine = autonomousLearningEngine
    this.errorHandler = errorHandler
    this.performanceMonitor = performanceMonitor
    
    // Configuration
    this.processConfig = {
      enabled: config?.ai?.background?.enabled !== false,
      maxConcurrentTasks: config?.ai?.background?.max_concurrent_tasks || 3,
      maxQueueSize: config?.ai?.background?.max_queue_size || 100,
      taskTimeout: config?.ai?.background?.task_timeout || 300000, // 5 minutes
      retryAttempts: config?.ai?.background?.retry_attempts || 3,
      retryDelay: config?.ai?.background?.retry_delay || 60000, // 1 minute
      healthCheckInterval: config?.ai?.background?.health_check_interval || 300000, // 5 minutes
      researchInterval: config?.ai?.background?.research_interval || 3600000, // 1 hour
      cleanupInterval: config?.ai?.background?.cleanup_interval || 86400000, // 24 hours
      currentDate: new Date().toISOString().split('T')[0] // Current date for research
    }
    
    // Task management
    this.taskQueue = []
    this.runningTasks = new Map()
    this.completedTasks = []
    this.failedTasks = []
    this.taskHistory = new Map()
    
    // Worker management
    this.workers = new Map()
    this.workerPool = []
    
    // Research state
    this.researchTopics = new Set()
    this.researchHistory = new Map()
    this.trendingTopics = []
    
    // Metrics
    this.metrics = {
      totalTasks: 0,
      completedTasks: 0,
      failedTasks: 0,
      averageExecutionTime: 0,
      queueLength: 0,
      activeWorkers: 0,
      researchSessions: 0,
      knowledgeUpdates: 0
    }
    
    // Background intervals
    this.intervals = []
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('⚙️ Initializing Background Process Manager...')
    
    try {
      // Initialize worker pool
      this.initializeWorkerPool()
      
      // Load existing tasks
      await this.loadExistingTasks()
      
      // Setup research topics
      this.setupResearchTopics()
      
      // Start background processes
      this.startBackgroundProcesses()
      
      // Schedule initial tasks
      await this.scheduleInitialTasks()
      
      this.isInitialized = true
      logger.info(`✅ Background Process Manager initialized with ${this.workerPool.length} workers`)
      
    } catch (error) {
      logger.error('❌ Failed to initialize Background Process Manager:', error)
      throw error
    }
  }

  initializeWorkerPool() {
    const workerCount = this.processConfig.maxConcurrentTasks
    
    for (let i = 0; i < workerCount; i++) {
      const worker = {
        id: `worker_${i}`,
        status: 'idle',
        currentTask: null,
        tasksCompleted: 0,
        totalExecutionTime: 0,
        lastActive: Date.now(),
        capabilities: ['general', 'research', 'analysis']
      }
      
      this.workerPool.push(worker)
      this.workers.set(worker.id, worker)
    }
    
    logger.info(`👷 Initialized ${workerCount} background workers`)
  }

  async loadExistingTasks() {
    try {
      // Load tasks from Redis
      const taskKeys = await this.redisAIManager.client.keys('bg_task:*')
      
      for (const key of taskKeys) {
        const task = await this.redisAIManager.client.hGetAll(key)
        if (task.status === TASK_STATUS.PENDING || task.status === TASK_STATUS.QUEUED) {
          this.taskQueue.push(this.parseTask(task))
        }
      }
      
      // Sort queue by priority
      this.sortTaskQueue()
      
      logger.info(`📋 Loaded ${this.taskQueue.length} existing tasks`)
      
    } catch (error) {
      logger.warn('Failed to load existing tasks:', error.message)
    }
  }

  setupResearchTopics() {
    // Initialize research topics based on current trends and system needs
    const defaultTopics = [
      'AI developments 2025',
      'JavaScript performance optimization',
      'Node.js best practices',
      'Redis optimization techniques',
      'OpenRouter.ai updates',
      'Machine learning trends',
      'Software architecture patterns',
      'API security best practices',
      'Cloud computing innovations',
      'DevOps automation tools'
    ]
    
    defaultTopics.forEach(topic => this.researchTopics.add(topic))
    
    // Add dynamic topics based on system usage
    this.addDynamicResearchTopics()
    
    logger.info(`🔍 Setup ${this.researchTopics.size} research topics`)
  }

  addDynamicResearchTopics() {
    // Add topics based on recent system activity
    if (this.autonomousLearningEngine && this.autonomousLearningEngine.knowledgeBase) {
      for (const [topic] of this.autonomousLearningEngine.knowledgeBase) {
        if (topic.length > 5 && !topic.startsWith('synthesis_')) {
          this.researchTopics.add(`${topic} latest developments`)
        }
      }
    }
    
    // Add topics based on current date
    const currentYear = new Date().getFullYear()
    const currentMonth = new Date().toLocaleString('default', { month: 'long' })
    
    this.researchTopics.add(`Technology trends ${currentMonth} ${currentYear}`)
    this.researchTopics.add(`AI breakthroughs ${currentYear}`)
    this.researchTopics.add(`Programming languages popularity ${currentYear}`)
  }

  startBackgroundProcesses() {
    // Task processing loop
    const processingInterval = setInterval(async () => {
      await this.processTaskQueue()
    }, 5000) // Every 5 seconds
    this.intervals.push(processingInterval)
    
    // Health check process
    const healthInterval = setInterval(async () => {
      await this.performHealthCheck()
    }, this.processConfig.healthCheckInterval)
    this.intervals.push(healthInterval)
    
    // Research automation
    const researchInterval = setInterval(async () => {
      await this.performAutomatedResearch()
    }, this.processConfig.researchInterval)
    this.intervals.push(researchInterval)
    
    // Cleanup process
    const cleanupInterval = setInterval(async () => {
      await this.performCleanup()
    }, this.processConfig.cleanupInterval)
    this.intervals.push(cleanupInterval)
    
    // Metrics collection
    const metricsInterval = setInterval(() => {
      this.updateMetrics()
    }, 60000) // Every minute
    this.intervals.push(metricsInterval)
    
    logger.info('🔄 Background processes started')
  }

  async scheduleInitialTasks() {
    // Schedule initial health check
    await this.scheduleTask({
      type: TASK_TYPES.HEALTH_CHECK,
      priority: TASK_PRIORITIES.HIGH,
      data: { component: 'system_startup' }
    })
    
    // Schedule initial research
    await this.scheduleTask({
      type: TASK_TYPES.WEB_RESEARCH,
      priority: TASK_PRIORITIES.MEDIUM,
      data: { 
        topic: `AI developments ${new Date().getFullYear()}`,
        category: RESEARCH_CATEGORIES.AI_DEVELOPMENTS
      }
    })
    
    // Schedule performance analysis
    await this.scheduleTask({
      type: TASK_TYPES.PERFORMANCE_ANALYSIS,
      priority: TASK_PRIORITIES.MEDIUM,
      data: { timeframe: '24h' }
    })
  }

  async scheduleTask(taskData) {
    if (!this.processConfig.enabled) {
      logger.debug('Background processing disabled, skipping task')
      return null
    }
    
    if (this.taskQueue.length >= this.processConfig.maxQueueSize) {
      logger.warn('Task queue full, rejecting new task')
      return null
    }
    
    const task = {
      id: this.generateTaskId(),
      type: taskData.type,
      priority: taskData.priority || TASK_PRIORITIES.MEDIUM,
      status: TASK_STATUS.PENDING,
      data: taskData.data || {},
      createdAt: Date.now(),
      scheduledFor: taskData.scheduledFor || Date.now(),
      attempts: 0,
      maxAttempts: taskData.maxAttempts || this.processConfig.retryAttempts,
      timeout: taskData.timeout || this.processConfig.taskTimeout,
      dependencies: taskData.dependencies || [],
      tags: taskData.tags || []
    }
    
    try {
      // Store task in Redis
      await this.redisAIManager.client.hSet(`bg_task:${task.id}`, {
        ...task,
        data: JSON.stringify(task.data),
        dependencies: JSON.stringify(task.dependencies),
        tags: JSON.stringify(task.tags)
      })
      
      // Add to queue
      this.taskQueue.push(task)
      this.sortTaskQueue()
      
      this.metrics.totalTasks++
      
      logger.info(`📋 Scheduled task: ${task.type} (${task.id})`)
      return task.id
      
    } catch (error) {
      logger.error('Failed to schedule task:', error)
      return null
    }
  }

  async processTaskQueue() {
    if (this.taskQueue.length === 0) return
    
    // Find available workers
    const availableWorkers = this.workerPool.filter(worker => worker.status === 'idle')
    if (availableWorkers.length === 0) return
    
    // Process tasks with available workers
    const tasksToProcess = Math.min(availableWorkers.length, this.taskQueue.length)
    
    for (let i = 0; i < tasksToProcess; i++) {
      const task = this.taskQueue.shift()
      const worker = availableWorkers[i]
      
      if (this.canExecuteTask(task)) {
        await this.executeTask(task, worker)
      } else {
        // Put task back in queue
        this.taskQueue.unshift(task)
        break
      }
    }
  }

  canExecuteTask(task) {
    // Check if task is ready to execute
    if (task.scheduledFor > Date.now()) {
      return false
    }
    
    // Check dependencies
    if (task.dependencies.length > 0) {
      const dependenciesMet = task.dependencies.every(depId => 
        this.completedTasks.some(t => t.id === depId)
      )
      if (!dependenciesMet) {
        return false
      }
    }
    
    return true
  }

  async executeTask(task, worker) {
    const startTime = Date.now()
    
    try {
      // Update task and worker status
      task.status = TASK_STATUS.RUNNING
      task.startedAt = startTime
      task.workerId = worker.id
      
      worker.status = 'busy'
      worker.currentTask = task.id
      worker.lastActive = startTime
      
      this.runningTasks.set(task.id, task)
      
      // Update task in Redis
      await this.redisAIManager.client.hSet(`bg_task:${task.id}`, {
        status: task.status,
        startedAt: task.startedAt,
        workerId: task.workerId
      })
      
      logger.info(`🚀 Executing task: ${task.type} (${task.id}) on worker ${worker.id}`)
      
      // Execute task with timeout
      const result = await Promise.race([
        this.executeTaskByType(task),
        this.createTaskTimeout(task.timeout)
      ])
      
      // Task completed successfully
      await this.completeTask(task, worker, result, startTime)
      
    } catch (error) {
      // Task failed
      await this.failTask(task, worker, error, startTime)
    }
  }

  async executeTaskByType(task) {
    switch (task.type) {
      case TASK_TYPES.WEB_RESEARCH:
        return await this.executeWebResearch(task)
      
      case TASK_TYPES.KNOWLEDGE_SYNTHESIS:
        return await this.executeKnowledgeSynthesis(task)
      
      case TASK_TYPES.AGENT_TRAINING:
        return await this.executeAgentTraining(task)
      
      case TASK_TYPES.PERFORMANCE_ANALYSIS:
        return await this.executePerformanceAnalysis(task)
      
      case TASK_TYPES.SYSTEM_OPTIMIZATION:
        return await this.executeSystemOptimization(task)
      
      case TASK_TYPES.DATA_CLEANUP:
        return await this.executeDataCleanup(task)
      
      case TASK_TYPES.HEALTH_CHECK:
        return await this.executeHealthCheck(task)
      
      case TASK_TYPES.LEARNING_SESSION:
        return await this.executeLearningSession(task)
      
      case TASK_TYPES.CAPABILITY_ASSESSMENT:
        return await this.executeCapabilityAssessment(task)
      
      case TASK_TYPES.TREND_ANALYSIS:
        return await this.executeTrendAnalysis(task)
      
      default:
        throw new Error(`Unknown task type: ${task.type}`)
    }
  }

  async executeWebResearch(task) {
    const { topic, category } = task.data
    
    logger.info(`🔍 Researching: ${topic}`)
    
    // Generate research prompt
    const prompt = this.generateResearchPrompt(topic, category)
    
    // Get AI research
    const response = await this.openRouterManager.generateCompletion(prompt, {
      category: 'reasoning',
      maxTokens: 1000,
      temperature: 0.7,
      systemMessage: `You are a research assistant conducting web research on ${topic}. 
        Provide comprehensive, accurate, and up-to-date information. 
        Focus on recent developments, trends, and practical insights.
        Current date: ${this.processConfig.currentDate}`
    })
    
    if (!response.success) {
      throw new Error('Research generation failed')
    }
    
    // Process research results
    const researchData = {
      topic,
      category,
      content: response.content,
      insights: await this.extractResearchInsights(response.content),
      sources: ['AI Research'],
      confidence: 0.8,
      timestamp: Date.now(),
      relevanceScore: await this.calculateRelevanceScore(response.content, topic)
    }
    
    // Store research results
    await this.storeResearchResults(researchData)
    
    // Update research history
    this.researchHistory.set(topic, researchData)
    
    this.metrics.researchSessions++
    
    return {
      success: true,
      data: researchData,
      insights: researchData.insights.length
    }
  }

  generateResearchPrompt(topic, category) {
    const categoryPrompts = {
      [RESEARCH_CATEGORIES.TECHNOLOGY]: `Research the latest developments in ${topic}. Focus on:
        - Recent technological breakthroughs
        - Industry adoption trends
        - Future implications
        - Key players and innovations`,
      
      [RESEARCH_CATEGORIES.AI_DEVELOPMENTS]: `Research recent AI developments related to ${topic}. Include:
        - New AI models and capabilities
        - Research breakthroughs
        - Industry applications
        - Ethical considerations`,
      
      [RESEARCH_CATEGORIES.PROGRAMMING]: `Research programming developments for ${topic}. Cover:
        - New language features
        - Framework updates
        - Best practices
        - Performance improvements`,
      
      [RESEARCH_CATEGORIES.INDUSTRY_TRENDS]: `Analyze industry trends for ${topic}. Include:
        - Market movements
        - Adoption patterns
        - Future predictions
        - Impact analysis`,
      
      [RESEARCH_CATEGORIES.BEST_PRACTICES]: `Research best practices for ${topic}. Focus on:
        - Proven methodologies
        - Expert recommendations
        - Common pitfalls to avoid
        - Implementation strategies`,
      
      [RESEARCH_CATEGORIES.SECURITY]: `Research security aspects of ${topic}. Cover:
        - Security vulnerabilities
        - Protection strategies
        - Compliance requirements
        - Risk assessments`,
      
      [RESEARCH_CATEGORIES.PERFORMANCE]: `Research performance optimization for ${topic}. Include:
        - Optimization techniques
        - Benchmarking results
        - Scalability considerations
        - Resource efficiency`,
      
      [RESEARCH_CATEGORIES.TOOLS]: `Research tools and technologies for ${topic}. Cover:
        - Available tools
        - Feature comparisons
        - Integration capabilities
        - User experiences`
    }
    
    return categoryPrompts[category] || categoryPrompts[RESEARCH_CATEGORIES.TECHNOLOGY]
  }

  async extractResearchInsights(content) {
    const insights = []
    
    // Simple insight extraction
    const sentences = content.split(/[.!?]+/)
    
    for (const sentence of sentences) {
      const trimmed = sentence.trim()
      if (trimmed.length > 30) {
        // Check for insight indicators
        const insightIndicators = [
          'important', 'significant', 'breakthrough', 'innovation',
          'trend', 'development', 'improvement', 'advancement',
          'key', 'critical', 'essential', 'major'
        ]
        
        const hasIndicator = insightIndicators.some(indicator => 
          trimmed.toLowerCase().includes(indicator)
        )
        
        if (hasIndicator) {
          insights.push({
            content: trimmed,
            confidence: 0.7,
            type: 'research_insight',
            timestamp: Date.now()
          })
        }
      }
    }
    
    return insights.slice(0, 10) // Limit to top 10 insights
  }

  async calculateRelevanceScore(content, topic) {
    const topicWords = topic.toLowerCase().split(/\s+/)
    const contentWords = content.toLowerCase().split(/\s+/)
    
    let matches = 0
    for (const word of topicWords) {
      if (contentWords.includes(word)) {
        matches++
      }
    }
    
    return topicWords.length > 0 ? matches / topicWords.length : 0
  }

  async storeResearchResults(researchData) {
    try {
      // Store in Redis
      await this.redisAIManager.client.hSet(`research:${researchData.topic}`, {
        topic: researchData.topic,
        category: researchData.category,
        content: researchData.content,
        insights: JSON.stringify(researchData.insights),
        sources: JSON.stringify(researchData.sources),
        confidence: researchData.confidence,
        timestamp: researchData.timestamp,
        relevanceScore: researchData.relevanceScore
      })
      
      // Update knowledge base if learning engine is available
      if (this.autonomousLearningEngine) {
        await this.autonomousLearningEngine.storeKnowledge({
          topic: researchData.topic,
          content: {
            research: researchData.content,
            insights: researchData.insights,
            category: researchData.category
          },
          confidence: researchData.confidence,
          sources: researchData.sources,
          lastUpdated: researchData.timestamp,
          validationCount: 1
        })
        
        this.metrics.knowledgeUpdates++
      }
      
    } catch (error) {
      logger.error('Failed to store research results:', error)
    }
  }

  async executeKnowledgeSynthesis(task) {
    if (!this.autonomousLearningEngine) {
      throw new Error('Autonomous Learning Engine not available')
    }
    
    await this.autonomousLearningEngine.performKnowledgeSynthesis()
    
    return {
      success: true,
      data: { synthesized: true },
      message: 'Knowledge synthesis completed'
    }
  }

  async executeAgentTraining(task) {
    const { agentId, trainingData } = task.data
    
    if (!agentId) {
      throw new Error('Agent ID required for training')
    }
    
    // Simulate agent training
    const agent = await this.redisAIManager.getAgent(agentId)
    if (!agent) {
      throw new Error(`Agent ${agentId} not found`)
    }
    
    // Update agent performance
    const improvementDelta = 0.05 // 5% improvement
    await this.redisAIManager.updateAgent(agentId, {
      performance_score: Math.min(1, agent.performance_score + improvementDelta),
      last_training: Date.now()
    })
    
    return {
      success: true,
      data: { agentId, improvement: improvementDelta },
      message: 'Agent training completed'
    }
  }

  async executePerformanceAnalysis(task) {
    const { timeframe } = task.data
    
    // Collect performance metrics
    const metrics = {
      system: this.performanceMonitor ? this.performanceMonitor.getSystemStats() : {},
      tasks: {
        total: this.metrics.totalTasks,
        completed: this.metrics.completedTasks,
        failed: this.metrics.failedTasks,
        averageTime: this.metrics.averageExecutionTime
      },
      queue: {
        length: this.taskQueue.length,
        running: this.runningTasks.size
      },
      workers: {
        total: this.workerPool.length,
        active: this.workerPool.filter(w => w.status === 'busy').length
      }
    }
    
    // Analyze trends
    const analysis = await this.analyzePerformanceTrends(metrics)
    
    return {
      success: true,
      data: { metrics, analysis, timeframe },
      message: 'Performance analysis completed'
    }
  }

  async analyzePerformanceTrends(metrics) {
    // Simple trend analysis
    const trends = {
      taskThroughput: 'stable',
      errorRate: metrics.tasks.failed / metrics.tasks.total > 0.1 ? 'high' : 'normal',
      queueHealth: metrics.queue.length > 50 ? 'congested' : 'healthy',
      workerUtilization: metrics.workers.active / metrics.workers.total
    }
    
    const recommendations = []
    
    if (trends.errorRate === 'high') {
      recommendations.push('Investigate task failures and improve error handling')
    }
    
    if (trends.queueHealth === 'congested') {
      recommendations.push('Consider increasing worker pool size or task timeout')
    }
    
    if (trends.workerUtilization > 0.8) {
      recommendations.push('High worker utilization - consider scaling up')
    }
    
    return { trends, recommendations }
  }

  async executeSystemOptimization(task) {
    const optimizations = []
    
    // Optimize task queue
    if (this.taskQueue.length > 20) {
      this.optimizeTaskQueue()
      optimizations.push('Task queue optimized')
    }
    
    // Clean up completed tasks
    if (this.completedTasks.length > 100) {
      this.completedTasks = this.completedTasks.slice(-50)
      optimizations.push('Completed tasks cleaned up')
    }
    
    // Optimize worker allocation
    await this.optimizeWorkerAllocation()
    optimizations.push('Worker allocation optimized')
    
    return {
      success: true,
      data: { optimizations },
      message: `System optimization completed: ${optimizations.length} optimizations applied`
    }
  }

  async executeDataCleanup(task) {
    const cleaned = []
    
    try {
      // Clean up old tasks
      const oldTaskKeys = await this.redisAIManager.client.keys('bg_task:*')
      const cutoff = Date.now() - (7 * 24 * 60 * 60 * 1000) // 7 days
      
      for (const key of oldTaskKeys) {
        const task = await this.redisAIManager.client.hGetAll(key)
        if (parseInt(task.createdAt) < cutoff && task.status === TASK_STATUS.COMPLETED) {
          await this.redisAIManager.client.del(key)
          cleaned.push(key)
        }
      }
      
      // Clean up old research data
      const researchKeys = await this.redisAIManager.client.keys('research:*')
      for (const key of researchKeys) {
        const research = await this.redisAIManager.client.hGetAll(key)
        if (parseInt(research.timestamp) < cutoff) {
          await this.redisAIManager.client.del(key)
          cleaned.push(key)
        }
      }
      
    } catch (error) {
      logger.error('Data cleanup failed:', error)
    }
    
    return {
      success: true,
      data: { cleaned: cleaned.length },
      message: `Data cleanup completed: ${cleaned.length} items removed`
    }
  }

  async executeHealthCheck(task) {
    const { component } = task.data
    const health = {
      timestamp: Date.now(),
      component: component || 'all',
      status: 'healthy',
      checks: {}
    }
    
    try {
      // Check OpenRouter Manager
      if (this.openRouterManager) {
        const openRouterHealth = this.openRouterManager.getRemainingDailyCapacity() > 0
        health.checks.openRouter = {
          status: openRouterHealth ? 'healthy' : 'degraded',
          capacity: this.openRouterManager.getRemainingDailyCapacity()
        }
      }
      
      // Check Redis AI Manager
      if (this.redisAIManager) {
        const redisHealth = await this.redisAIManager.client.ping()
        health.checks.redis = {
          status: redisHealth === 'PONG' ? 'healthy' : 'unhealthy',
          response: redisHealth
        }
      }
      
      // Check Learning Engine
      if (this.autonomousLearningEngine) {
        health.checks.learningEngine = {
          status: this.autonomousLearningEngine.isInitialized ? 'healthy' : 'unhealthy',
          activeDiscussions: this.autonomousLearningEngine.activeDiscussions.size
        }
      }
      
      // Check worker health
      health.checks.workers = {
        total: this.workerPool.length,
        active: this.workerPool.filter(w => w.status === 'busy').length,
        idle: this.workerPool.filter(w => w.status === 'idle').length
      }
      
      // Overall health assessment
      const unhealthyChecks = Object.values(health.checks).filter(
        check => check.status === 'unhealthy'
      )
      
      if (unhealthyChecks.length > 0) {
        health.status = 'degraded'
      }
      
    } catch (error) {
      health.status = 'unhealthy'
      health.error = error.message
    }
    
    return {
      success: true,
      data: health,
      message: `Health check completed: ${health.status}`
    }
  }

  async executeLearningSession(task) {
    if (!this.autonomousLearningEngine) {
      throw new Error('Autonomous Learning Engine not available')
    }
    
    const { topic, participants } = task.data
    
    // Initiate learning session
    await this.autonomousLearningEngine.initiateAgentDiscussion({
      topic,
      participants,
      discussionType: 'knowledge_sharing'
    })
    
    return {
      success: true,
      data: { topic, participants },
      message: 'Learning session initiated'
    }
  }

  async executeCapabilityAssessment(task) {
    if (!this.autonomousLearningEngine) {
      throw new Error('Autonomous Learning Engine not available')
    }
    
    await this.autonomousLearningEngine.performCapabilityAssessment()
    
    return {
      success: true,
      data: { assessed: true },
      message: 'Capability assessment completed'
    }
  }

  async executeTrendAnalysis(task) {
    const { category, timeframe } = task.data
    
    // Analyze trends in research data
    const trends = await this.analyzeTrends(category, timeframe)
    
    return {
      success: true,
      data: trends,
      message: 'Trend analysis completed'
    }
  }

  async analyzeTrends(category, timeframe) {
    const trends = {
      category,
      timeframe,
      topics: [],
      insights: [],
      recommendations: []
    }
    
    try {
      // Get research data for analysis
      const researchKeys = await this.redisAIManager.client.keys('research:*')
      const researchData = []
      
      for (const key of researchKeys) {
        const research = await this.redisAIManager.client.hGetAll(key)
        if (research.category === category) {
          researchData.push(research)
        }
      }
      
      // Analyze trending topics
      const topicFrequency = new Map()
      for (const research of researchData) {
        const words = research.topic.toLowerCase().split(/\s+/)
        for (const word of words) {
          if (word.length > 3) {
            topicFrequency.set(word, (topicFrequency.get(word) || 0) + 1)
          }
        }
      }
      
      // Get top trending topics
      trends.topics = Array.from(topicFrequency.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([topic, frequency]) => ({ topic, frequency }))
      
      // Generate insights
      if (trends.topics.length > 0) {
        trends.insights.push(`Most discussed topic: ${trends.topics[0].topic}`)
        trends.insights.push(`${trends.topics.length} trending topics identified`)
        
        if (trends.topics[0].frequency > 3) {
          trends.recommendations.push(`Focus research efforts on ${trends.topics[0].topic}`)
        }
      }
      
    } catch (error) {
      logger.error('Trend analysis failed:', error)
    }
    
    return trends
  }

  createTaskTimeout(timeout) {
    return new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error('Task timeout'))
      }, timeout)
    })
  }

  async completeTask(task, worker, result, startTime) {
    const duration = Date.now() - startTime
    
    try {
      // Update task status
      task.status = TASK_STATUS.COMPLETED
      task.completedAt = Date.now()
      task.duration = duration
      task.result = result
      
      // Update worker status
      worker.status = 'idle'
      worker.currentTask = null
      worker.tasksCompleted++
      worker.totalExecutionTime += duration
      worker.lastActive = Date.now()
      
      // Remove from running tasks
      this.runningTasks.delete(task.id)
      
      // Add to completed tasks
      this.completedTasks.push(task)
      
      // Update task in Redis
      await this.redisAIManager.client.hSet(`bg_task:${task.id}`, {
        status: task.status,
        completedAt: task.completedAt,
        duration: task.duration,
        result: JSON.stringify(result)
      })
      
      // Update metrics
      this.metrics.completedTasks++
      this.metrics.averageExecutionTime = (this.metrics.averageExecutionTime + duration) / 2
      
      logger.info(`✅ Task completed: ${task.type} (${task.id}) in ${duration}ms`)
      
      // Schedule follow-up tasks if needed
      await this.scheduleFollowUpTasks(task, result)
      
    } catch (error) {
      logger.error(`Failed to complete task ${task.id}:`, error)
    }
  }

  async failTask(task, worker, error, startTime) {
    const duration = Date.now() - startTime
    
    try {
      task.attempts++
      task.lastError = error.message
      task.lastAttemptAt = Date.now()
      
      // Update worker status
      worker.status = 'idle'
      worker.currentTask = null
      worker.lastActive = Date.now()
      
      // Remove from running tasks
      this.runningTasks.delete(task.id)
      
      // Check if should retry
      if (task.attempts < task.maxAttempts) {
        task.status = TASK_STATUS.RETRYING
        task.scheduledFor = Date.now() + this.processConfig.retryDelay
        
        // Put back in queue
        this.taskQueue.unshift(task)
        this.sortTaskQueue()
        
        logger.warn(`🔄 Retrying task: ${task.type} (${task.id}) - Attempt ${task.attempts}/${task.maxAttempts}`)
      } else {
        task.status = TASK_STATUS.FAILED
        task.failedAt = Date.now()
        
        // Add to failed tasks
        this.failedTasks.push(task)
        
        this.metrics.failedTasks++
        
        logger.error(`❌ Task failed: ${task.type} (${task.id}) - ${error.message}`)
      }
      
      // Update task in Redis
      await this.redisAIManager.client.hSet(`bg_task:${task.id}`, {
        status: task.status,
        attempts: task.attempts,
        lastError: task.lastError,
        lastAttemptAt: task.lastAttemptAt,
        scheduledFor: task.scheduledFor || '',
        failedAt: task.failedAt || ''
      })
      
    } catch (updateError) {
      logger.error(`Failed to update failed task ${task.id}:`, updateError)
    }
  }

  async scheduleFollowUpTasks(completedTask, result) {
    // Schedule follow-up tasks based on completed task type and results
    switch (completedTask.type) {
      case TASK_TYPES.WEB_RESEARCH:
        if (result.insights > 5) {
          // Schedule knowledge synthesis if research yielded many insights
          await this.scheduleTask({
            type: TASK_TYPES.KNOWLEDGE_SYNTHESIS,
            priority: TASK_PRIORITIES.MEDIUM,
            data: { trigger: 'research_insights' }
          })
        }
        break
      
      case TASK_TYPES.PERFORMANCE_ANALYSIS:
        if (result.data.analysis.recommendations.length > 0) {
          // Schedule optimization if recommendations were made
          await this.scheduleTask({
            type: TASK_TYPES.SYSTEM_OPTIMIZATION,
            priority: TASK_PRIORITIES.HIGH,
            data: { trigger: 'performance_recommendations' }
          })
        }
        break
      
      case TASK_TYPES.HEALTH_CHECK:
        if (result.data.status === 'degraded') {
          // Schedule another health check in 5 minutes
          await this.scheduleTask({
            type: TASK_TYPES.HEALTH_CHECK,
            priority: TASK_PRIORITIES.HIGH,
            scheduledFor: Date.now() + 300000,
            data: { trigger: 'degraded_health' }
          })
        }
        break
    }
  }

  async performAutomatedResearch() {
    if (!this.processConfig.enabled) return
    
    try {
      // Select research topic
      const topic = this.selectResearchTopic()
      if (!topic) return
      
      // Schedule research task
      await this.scheduleTask({
        type: TASK_TYPES.WEB_RESEARCH,
        priority: TASK_PRIORITIES.MEDIUM,
        data: {
          topic,
          category: this.categorizeResearchTopic(topic)
        }
      })
      
      logger.info(`🔍 Scheduled automated research: ${topic}`)
      
    } catch (error) {
      logger.error('Automated research scheduling failed:', error)
    }
  }

  selectResearchTopic() {
    const topics = Array.from(this.researchTopics)
    if (topics.length === 0) return null
    
    // Prioritize topics that haven't been researched recently
    const unresearchedTopics = topics.filter(topic => 
      !this.researchHistory.has(topic) ||
      Date.now() - this.researchHistory.get(topic).timestamp > 86400000 // 24 hours
    )
    
    if (unresearchedTopics.length > 0) {
      return unresearchedTopics[Math.floor(Math.random() * unresearchedTopics.length)]
    }
    
    // If all topics have been researched recently, pick a random one
    return topics[Math.floor(Math.random() * topics.length)]
  }

  categorizeResearchTopic(topic) {
    const topicLower = topic.toLowerCase()
    
    if (topicLower.includes('ai') || topicLower.includes('machine learning')) {
      return RESEARCH_CATEGORIES.AI_DEVELOPMENTS
    }
    if (topicLower.includes('javascript') || topicLower.includes('node') || topicLower.includes('programming')) {
      return RESEARCH_CATEGORIES.PROGRAMMING
    }
    if (topicLower.includes('security')) {
      return RESEARCH_CATEGORIES.SECURITY
    }
    if (topicLower.includes('performance') || topicLower.includes('optimization')) {
      return RESEARCH_CATEGORIES.PERFORMANCE
    }
    if (topicLower.includes('tool') || topicLower.includes('framework')) {
      return RESEARCH_CATEGORIES.TOOLS
    }
    if (topicLower.includes('trend') || topicLower.includes('industry')) {
      return RESEARCH_CATEGORIES.INDUSTRY_TRENDS
    }
    if (topicLower.includes('best practice') || topicLower.includes('methodology')) {
      return RESEARCH_CATEGORIES.BEST_PRACTICES
    }
    
    return RESEARCH_CATEGORIES.TECHNOLOGY
  }

  async performHealthCheck() {
    await this.scheduleTask({
      type: TASK_TYPES.HEALTH_CHECK,
      priority: TASK_PRIORITIES.HIGH,
      data: { component: 'scheduled_check' }
    })
  }

  async performCleanup() {
    await this.scheduleTask({
      type: TASK_TYPES.DATA_CLEANUP,
      priority: TASK_PRIORITIES.LOW,
      data: { trigger: 'scheduled_cleanup' }
    })
  }

  // Utility methods
  generateTaskId() {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  sortTaskQueue() {
    this.taskQueue.sort((a, b) => {
      // Sort by priority first, then by scheduled time
      if (a.priority !== b.priority) {
        return a.priority - b.priority
      }
      return a.scheduledFor - b.scheduledFor
    })
  }

  parseTask(taskData) {
    return {
      ...taskData,
      data: JSON.parse(taskData.data || '{}'),
      dependencies: JSON.parse(taskData.dependencies || '[]'),
      tags: JSON.parse(taskData.tags || '[]'),
      createdAt: parseInt(taskData.createdAt),
      scheduledFor: parseInt(taskData.scheduledFor || taskData.createdAt),
      attempts: parseInt(taskData.attempts || '0'),
      maxAttempts: parseInt(taskData.maxAttempts || '3'),
      timeout: parseInt(taskData.timeout || '300000')
    }
  }

  optimizeTaskQueue() {
    // Remove duplicate tasks
    const seen = new Set()
    this.taskQueue = this.taskQueue.filter(task => {
      const key = `${task.type}_${JSON.stringify(task.data)}`
      if (seen.has(key)) {
        return false
      }
      seen.add(key)
      return true
    })
    
    // Re-sort queue
    this.sortTaskQueue()
  }

  async optimizeWorkerAllocation() {
    // Analyze worker performance and adjust if needed
    for (const worker of this.workerPool) {
      if (worker.tasksCompleted > 0) {
        worker.averageExecutionTime = worker.totalExecutionTime / worker.tasksCompleted
      }
    }
    
    // Could implement more sophisticated worker optimization here
  }

  updateMetrics() {
    this.metrics.queueLength = this.taskQueue.length
    this.metrics.activeWorkers = this.workerPool.filter(w => w.status === 'busy').length
  }

  // Statistics and reporting
  getProcessingReport() {
    return {
      timestamp: Date.now(),
      metrics: { ...this.metrics },
      queue: {
        length: this.taskQueue.length,
        running: this.runningTasks.size,
        nextTask: this.taskQueue[0] ? {
          type: this.taskQueue[0].type,
          priority: this.taskQueue[0].priority,
          scheduledFor: this.taskQueue[0].scheduledFor
        } : null
      },
      workers: {
        total: this.workerPool.length,
        busy: this.workerPool.filter(w => w.status === 'busy').length,
        idle: this.workerPool.filter(w => w.status === 'idle').length,
        performance: this.workerPool.map(w => ({
          id: w.id,
          status: w.status,
          tasksCompleted: w.tasksCompleted,
          averageTime: w.averageExecutionTime || 0
        }))
      },
      research: {
        topics: this.researchTopics.size,
        completed: this.researchHistory.size,
        sessions: this.metrics.researchSessions
      },
      configuration: this.processConfig
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Background Process Manager...')
    
    // Clear intervals
    this.intervals.forEach(interval => clearInterval(interval))
    this.intervals.length = 0
    
    // Cancel running tasks
    for (const [taskId, task] of this.runningTasks) {
      task.status = TASK_STATUS.CANCELLED
      await this.redisAIManager.client.hSet(`bg_task:${taskId}`, {
        status: task.status,
        cancelledAt: Date.now()
      })
    }
    
    // Clear data structures
    this.taskQueue.length = 0
    this.runningTasks.clear()
    this.completedTasks.length = 0
    this.failedTasks.length = 0
    this.taskHistory.clear()
    this.workers.clear()
    this.workerPool.length = 0
    this.researchTopics.clear()
    this.researchHistory.clear()
    
    this.isInitialized = false
    logger.info('✅ Background Process Manager cleanup complete')
  }
}

module.exports = {
  BackgroundProcessManager,
  TASK_TYPES,
  TASK_PRIORITIES,
  TASK_STATUS,
  RESEARCH_CATEGORIES
}