/**
 * JAEGIS Decision Engine
 * Intelligent decision-making system for command routing and processing
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

class DecisionEngine {
  constructor({ config, cache }) {
    this.config = config
    this.cache = cache
    this.decisionHistory = []
    this.performanceMetrics = new Map()
    this.learningData = new Map()
    this.isInitialized = false
    
    // Decision factors and weights
    this.decisionFactors = {
      command_complexity: 0.25,
      data_requirements: 0.20,
      processing_time: 0.15,
      resource_availability: 0.15,
      user_context: 0.10,
      cache_availability: 0.10,
      historical_performance: 0.05
    }
    
    // Command patterns and their characteristics
    this.commandPatterns = new Map()
    this.initializeCommandPatterns()
  }

  async initialize() {
    logger.info('🧠 Initializing Decision Engine...')
    
    try {
      // Load historical decision data
      await this.loadHistoricalData()
      
      // Initialize performance tracking
      this.setupPerformanceTracking()
      
      this.isInitialized = true
      logger.info('✅ Decision Engine initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Decision Engine:', error)
      throw error
    }
  }

  initializeCommandPatterns() {
    // Define command patterns and their characteristics
    const patterns = [
      {
        pattern: /^(help|h)$/i,
        characteristics: {
          complexity: 'low',
          github_data_required: true,
          processing_time: 'fast',
          cache_strategy: 'aggressive',
          priority: 'high',
          squad_activation: false
        }
      },
      {
        pattern: /^(status|s)$/i,
        characteristics: {
          complexity: 'low',
          github_data_required: false,
          processing_time: 'fast',
          cache_strategy: 'none',
          priority: 'high',
          squad_activation: false
        }
      },
      {
        pattern: /^(config|c)$/i,
        characteristics: {
          complexity: 'medium',
          github_data_required: false,
          processing_time: 'medium',
          cache_strategy: 'minimal',
          priority: 'normal',
          squad_activation: false
        }
      },
      {
        pattern: /^(agents|a)$/i,
        characteristics: {
          complexity: 'medium',
          github_data_required: true,
          processing_time: 'medium',
          cache_strategy: 'moderate',
          priority: 'normal',
          squad_activation: true
        }
      },
      {
        pattern: /^(analytics|analyze)$/i,
        characteristics: {
          complexity: 'high',
          github_data_required: true,
          processing_time: 'slow',
          cache_strategy: 'aggressive',
          priority: 'low',
          squad_activation: true
        }
      },
      {
        pattern: /^(optimize|debug|troubleshoot)$/i,
        characteristics: {
          complexity: 'high',
          github_data_required: true,
          processing_time: 'slow',
          cache_strategy: 'moderate',
          priority: 'low',
          squad_activation: true
        }
      },
      {
        pattern: /^(mode-switch|mode)$/i,
        characteristics: {
          complexity: 'medium',
          github_data_required: false,
          processing_time: 'medium',
          cache_strategy: 'minimal',
          priority: 'normal',
          squad_activation: true
        }
      }
    ]
    
    patterns.forEach(({ pattern, characteristics }) => {
      this.commandPatterns.set(pattern, characteristics)
    })
    
    logger.info(`🧠 Initialized ${this.commandPatterns.size} command patterns`)
  }

  async makeDecision(command, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Decision Engine not initialized')
    }
    
    const startTime = Date.now()
    
    try {
      logger.info(`🧠 Making decision for command: ${command}`)
      
      // Analyze command characteristics
      const commandAnalysis = await this.analyzeCommand(command, options)
      
      // Evaluate decision factors
      const factorScores = await this.evaluateFactors(command, commandAnalysis, options)
      
      // Calculate decision score
      const decisionScore = this.calculateDecisionScore(factorScores)
      
      // Make routing decision
      const routingDecision = this.makeRoutingDecision(commandAnalysis, decisionScore, options)
      
      // Create decision object
      const decision = {
        command,
        timestamp: Date.now(),
        analysis: commandAnalysis,
        factors: factorScores,
        score: decisionScore,
        routing: routingDecision,
        processingTime: Date.now() - startTime,
        confidence: this.calculateConfidence(factorScores)
      }
      
      // Record decision for learning
      this.recordDecision(decision, options)
      
      logger.info(`🧠 Decision made for ${command}: ${JSON.stringify(routingDecision)}`)
      
      return decision
      
    } catch (error) {
      logger.error(`Decision making error for ${command}:`, error)
      
      // Return fallback decision
      return this.getFallbackDecision(command, options)
    }
  }

  async analyzeCommand(command, options) {
    const analysis = {
      command,
      normalized: command.toLowerCase().trim(),
      length: command.length,
      complexity: 'medium',
      pattern_match: null,
      characteristics: {}
    }
    
    // Find matching pattern
    for (const [pattern, characteristics] of this.commandPatterns) {
      if (pattern.test(analysis.normalized)) {
        analysis.pattern_match = pattern.source
        analysis.characteristics = { ...characteristics }
        analysis.complexity = characteristics.complexity
        break
      }
    }
    
    // If no pattern match, analyze heuristically
    if (!analysis.pattern_match) {
      analysis.characteristics = await this.heuristicAnalysis(command)
      analysis.complexity = this.determineComplexity(command)
    }
    
    return analysis
  }

  async heuristicAnalysis(command) {
    const characteristics = {
      complexity: 'medium',
      github_data_required: false,
      processing_time: 'medium',
      cache_strategy: 'moderate',
      priority: 'normal',
      squad_activation: false
    }
    
    const commandLower = command.toLowerCase()
    
    // Analyze for GitHub data requirement
    const githubIndicators = ['help', 'documentation', 'commands', 'list', 'show', 'fetch']
    characteristics.github_data_required = githubIndicators.some(indicator => 
      commandLower.includes(indicator)
    )
    
    // Analyze complexity
    const complexIndicators = ['analytics', 'optimize', 'debug', 'complex', 'advanced']
    const simpleIndicators = ['status', 'ping', 'version', 'info']
    
    if (complexIndicators.some(indicator => commandLower.includes(indicator))) {
      characteristics.complexity = 'high'
      characteristics.processing_time = 'slow'
      characteristics.squad_activation = true
    } else if (simpleIndicators.some(indicator => commandLower.includes(indicator))) {
      characteristics.complexity = 'low'
      characteristics.processing_time = 'fast'
    }
    
    // Analyze priority
    const highPriorityIndicators = ['emergency', 'urgent', 'critical', 'help', 'status']
    const lowPriorityIndicators = ['analytics', 'backup', 'cleanup', 'optimize']
    
    if (highPriorityIndicators.some(indicator => commandLower.includes(indicator))) {
      characteristics.priority = 'high'
    } else if (lowPriorityIndicators.some(indicator => commandLower.includes(indicator))) {
      characteristics.priority = 'low'
    }
    
    return characteristics
  }

  determineComplexity(command) {
    const commandLower = command.toLowerCase()
    
    // Count complexity indicators
    let complexityScore = 0
    
    // Length factor
    if (command.length > 20) complexityScore += 1
    if (command.length > 50) complexityScore += 1
    
    // Keyword analysis
    const complexKeywords = ['analytics', 'optimize', 'debug', 'integration', 'advanced']
    const simpleKeywords = ['status', 'help', 'info', 'ping']
    
    complexityScore += complexKeywords.filter(kw => commandLower.includes(kw)).length * 2
    complexityScore -= simpleKeywords.filter(kw => commandLower.includes(kw)).length
    
    if (complexityScore <= 0) return 'low'
    if (complexityScore <= 2) return 'medium'
    return 'high'
  }

  async evaluateFactors(command, analysis, options) {
    const factors = {}
    
    // Command complexity factor
    factors.command_complexity = this.evaluateComplexity(analysis.complexity)
    
    // Data requirements factor
    factors.data_requirements = this.evaluateDataRequirements(analysis.characteristics)
    
    // Processing time factor
    factors.processing_time = this.evaluateProcessingTime(analysis.characteristics)
    
    // Resource availability factor
    factors.resource_availability = await this.evaluateResourceAvailability()
    
    // User context factor
    factors.user_context = this.evaluateUserContext(options)
    
    // Cache availability factor
    factors.cache_availability = await this.evaluateCacheAvailability(command)
    
    // Historical performance factor
    factors.historical_performance = this.evaluateHistoricalPerformance(command)
    
    return factors
  }

  evaluateComplexity(complexity) {
    const scores = {
      'low': 0.2,
      'medium': 0.5,
      'high': 0.8
    }
    return scores[complexity] || 0.5
  }

  evaluateDataRequirements(characteristics) {
    if (characteristics.github_data_required) {
      return 0.8 // High data requirement
    }
    return 0.2 // Low data requirement
  }

  evaluateProcessingTime(characteristics) {
    const scores = {
      'fast': 0.2,
      'medium': 0.5,
      'slow': 0.8
    }
    return scores[characteristics.processing_time] || 0.5
  }

  async evaluateResourceAvailability() {
    try {
      // Check system resources
      const memoryUsage = process.memoryUsage()
      const memoryPercent = memoryUsage.heapUsed / memoryUsage.heapTotal
      
      // Check active processes (placeholder)
      const activeProcesses = 0 // Would get from actual process manager
      
      // Calculate resource availability score (lower is better)
      let score = 0
      score += memoryPercent * 0.5
      score += (activeProcesses / 10) * 0.3
      score += Math.random() * 0.2 // Network/IO simulation
      
      return Math.min(score, 1.0)
      
    } catch (error) {
      logger.error('Resource evaluation error:', error)
      return 0.5 // Default moderate load
    }
  }

  evaluateUserContext(options) {
    let score = 0.5 // Default
    
    // Check user context indicators
    if (options.context) {
      if (options.context.interactive) score -= 0.2 // Interactive sessions get priority
      if (options.context.cli) score += 0.1 // CLI might be less urgent
      if (options.context.websocket) score -= 0.1 // Real-time connections get priority
    }
    
    // Check request priority
    if (options.priority) {
      const priorityScores = {
        'emergency': 0.1,
        'high': 0.3,
        'normal': 0.5,
        'low': 0.8
      }
      score = priorityScores[options.priority] || score
    }
    
    return Math.max(0, Math.min(1, score))
  }

  async evaluateCacheAvailability(command) {
    try {
      // Check if command result is cached
      const cacheKey = `command_result:${command}`
      const cached = await this.cache.exists(cacheKey)
      
      if (cached) {
        return 0.1 // Very low score if cached (fast response)
      }
      
      // Check if related data is cached
      const relatedKeys = [`github_commands`, `command_data:${command.split(' ')[0]}`]
      let relatedCached = 0
      
      for (const key of relatedKeys) {
        if (await this.cache.exists(key)) {
          relatedCached++
        }
      }
      
      return 0.3 + (relatedCached / relatedKeys.length) * 0.4
      
    } catch (error) {
      logger.error('Cache evaluation error:', error)
      return 0.7 // Assume no cache available
    }
  }

  evaluateHistoricalPerformance(command) {
    const commandBase = command.split(' ')[0]
    const metrics = this.performanceMetrics.get(commandBase)
    
    if (!metrics) {
      return 0.5 // No historical data
    }
    
    // Calculate performance score based on historical data
    const avgResponseTime = metrics.totalTime / metrics.count
    const successRate = metrics.successes / metrics.count
    
    // Lower response time and higher success rate = lower score (better performance)
    let score = 0.5
    
    if (avgResponseTime < 1000) score -= 0.2 // Fast responses
    if (avgResponseTime > 5000) score += 0.2 // Slow responses
    
    if (successRate > 0.95) score -= 0.1 // High success rate
    if (successRate < 0.8) score += 0.2 // Low success rate
    
    return Math.max(0, Math.min(1, score))
  }

  calculateDecisionScore(factors) {
    let totalScore = 0
    
    for (const [factor, weight] of Object.entries(this.decisionFactors)) {
      const factorScore = factors[factor] || 0.5
      totalScore += factorScore * weight
    }
    
    return totalScore
  }

  makeRoutingDecision(analysis, decisionScore, options) {
    const decision = {
      needsGitHubData: analysis.characteristics.github_data_required || false,
      useCache: this.shouldUseCache(analysis, decisionScore),
      priority: this.determinePriority(analysis, decisionScore),
      processingStrategy: this.determineProcessingStrategy(analysis, decisionScore),
      squadActivation: analysis.characteristics.squad_activation || false,
      estimatedTime: this.estimateProcessingTime(analysis),
      confidence: this.calculateConfidence(decisionScore)
    }
    
    // Add specific routing recommendations
    if (decisionScore < 0.3) {
      decision.recommendation = 'fast_track'
      decision.reason = 'Low complexity, cached data available'
    } else if (decisionScore > 0.7) {
      decision.recommendation = 'careful_processing'
      decision.reason = 'High complexity or resource constraints'
    } else {
      decision.recommendation = 'standard_processing'
      decision.reason = 'Moderate complexity and resource usage'
    }
    
    return decision
  }

  shouldUseCache(analysis, decisionScore) {
    const cacheStrategy = analysis.characteristics.cache_strategy
    
    switch (cacheStrategy) {
      case 'aggressive':
        return true
      case 'none':
        return false
      case 'minimal':
        return decisionScore < 0.4
      case 'moderate':
      default:
        return decisionScore < 0.6
    }
  }

  determinePriority(analysis, decisionScore) {
    const basePriority = analysis.characteristics.priority || 'normal'
    
    // Adjust priority based on decision score
    if (decisionScore < 0.3 && basePriority !== 'low') {
      return 'high' // Fast processing available
    }
    
    if (decisionScore > 0.8 && basePriority !== 'high') {
      return 'low' // Resource constraints
    }
    
    return basePriority
  }

  determineProcessingStrategy(analysis, decisionScore) {
    if (analysis.characteristics.squad_activation) {
      return 'squad_coordination'
    }
    
    if (decisionScore < 0.3) {
      return 'fast_path'
    }
    
    if (decisionScore > 0.7) {
      return 'careful_processing'
    }
    
    return 'standard'
  }

  estimateProcessingTime(analysis) {
    const baseTime = {
      'low': 500,
      'medium': 2000,
      'high': 5000
    }
    
    let estimatedTime = baseTime[analysis.complexity] || 2000
    
    // Adjust based on characteristics
    if (analysis.characteristics.github_data_required) {
      estimatedTime += 1000
    }
    
    if (analysis.characteristics.squad_activation) {
      estimatedTime += 2000
    }
    
    return estimatedTime
  }

  calculateConfidence(factorScores) {
    // Calculate confidence based on factor consistency
    const scores = Object.values(factorScores)
    const mean = scores.reduce((a, b) => a + b, 0) / scores.length
    const variance = scores.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / scores.length
    
    // Lower variance = higher confidence
    const confidence = Math.max(0.1, 1 - variance)
    
    return Math.round(confidence * 100) / 100
  }

  getFallbackDecision(command, options) {
    return {
      command,
      timestamp: Date.now(),
      analysis: {
        command,
        complexity: 'medium',
        characteristics: {
          github_data_required: true,
          processing_time: 'medium',
          cache_strategy: 'moderate',
          priority: 'normal'
        }
      },
      routing: {
        needsGitHubData: true,
        useCache: true,
        priority: 'normal',
        processingStrategy: 'standard',
        squadActivation: false,
        estimatedTime: 2000,
        confidence: 0.5,
        recommendation: 'fallback_processing',
        reason: 'Decision engine error, using safe defaults'
      },
      confidence: 0.5,
      fallback: true
    }
  }

  recordDecision(decision, options) {
    // Record decision for learning
    this.decisionHistory.push({
      ...decision,
      options,
      timestamp: Date.now()
    })
    
    // Keep only recent decisions
    if (this.decisionHistory.length > 1000) {
      this.decisionHistory = this.decisionHistory.slice(-1000)
    }
    
    // Update learning data
    this.updateLearningData(decision, options)
  }

  updateLearningData(decision, options) {
    const commandBase = decision.command.split(' ')[0]
    
    if (!this.learningData.has(commandBase)) {
      this.learningData.set(commandBase, {
        count: 0,
        totalScore: 0,
        avgScore: 0,
        decisions: []
      })
    }
    
    const data = this.learningData.get(commandBase)
    data.count++
    data.totalScore += decision.score
    data.avgScore = data.totalScore / data.count
    data.decisions.push({
      score: decision.score,
      confidence: decision.confidence,
      timestamp: decision.timestamp
    })
    
    // Keep only recent decisions for learning
    if (data.decisions.length > 100) {
      data.decisions = data.decisions.slice(-100)
    }
  }

  recordPerformance(command, success, responseTime) {
    const commandBase = command.split(' ')[0]
    
    if (!this.performanceMetrics.has(commandBase)) {
      this.performanceMetrics.set(commandBase, {
        count: 0,
        successes: 0,
        totalTime: 0
      })
    }
    
    const metrics = this.performanceMetrics.get(commandBase)
    metrics.count++
    metrics.totalTime += responseTime
    
    if (success) {
      metrics.successes++
    }
  }

  async loadHistoricalData() {
    try {
      // Load historical decision data from cache
      const historicalData = await this.cache.get('decision_engine_history')
      
      if (historicalData) {
        this.decisionHistory = historicalData.decisions || []
        this.performanceMetrics = new Map(historicalData.performance || [])
        this.learningData = new Map(historicalData.learning || [])
        
        logger.info(`📊 Loaded ${this.decisionHistory.length} historical decisions`)
      }
      
    } catch (error) {
      logger.error('Failed to load historical data:', error)
    }
  }

  async saveHistoricalData() {
    try {
      const historicalData = {
        decisions: this.decisionHistory,
        performance: Array.from(this.performanceMetrics.entries()),
        learning: Array.from(this.learningData.entries()),
        timestamp: Date.now()
      }
      
      await this.cache.set('decision_engine_history', historicalData, 86400000) // 24 hours
      
      logger.info('💾 Historical decision data saved')
      
    } catch (error) {
      logger.error('Failed to save historical data:', error)
    }
  }

  setupPerformanceTracking() {
    // Save historical data periodically
    setInterval(() => {
      this.saveHistoricalData()
    }, 300000) // Every 5 minutes
  }

  getStats() {
    return {
      decisions_made: this.decisionHistory.length,
      commands_learned: this.learningData.size,
      performance_tracked: this.performanceMetrics.size,
      avg_confidence: this.decisionHistory.length > 0
        ? this.decisionHistory.reduce((sum, d) => sum + d.confidence, 0) / this.decisionHistory.length
        : 0,
      decision_factors: this.decisionFactors,
      patterns_registered: this.commandPatterns.size
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Decision Engine...')
    
    // Save final historical data
    await this.saveHistoricalData()
    
    // Clear data structures
    this.decisionHistory.length = 0
    this.performanceMetrics.clear()
    this.learningData.clear()
    this.commandPatterns.clear()
    
    this.isInitialized = false
    logger.info('✅ Decision Engine cleanup complete')
  }
}

module.exports = DecisionEngine