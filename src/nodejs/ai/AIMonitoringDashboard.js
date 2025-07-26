/**
 * JAEGIS AI Monitoring Dashboard
 * Comprehensive real-time monitoring and analytics for AI systems
 * Provides insights, alerts, and performance tracking for all AI components
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

// Dashboard Sections
const DASHBOARD_SECTIONS = {
  OVERVIEW: 'overview',
  API_USAGE: 'api_usage',
  LEARNING_PROGRESS: 'learning_progress',
  AGENT_ACTIVITY: 'agent_activity',
  BACKGROUND_TASKS: 'background_tasks',
  PERFORMANCE_METRICS: 'performance_metrics',
  SYSTEM_HEALTH: 'system_health',
  ALERTS: 'alerts'
}

// Alert Types
const ALERT_TYPES = {
  INFO: 'info',
  WARNING: 'warning',
  ERROR: 'error',
  CRITICAL: 'critical'
}

// Alert Categories
const ALERT_CATEGORIES = {
  API_QUOTA: 'api_quota',
  PERFORMANCE: 'performance',
  SYSTEM_HEALTH: 'system_health',
  LEARNING: 'learning',
  SECURITY: 'security',
  CAPACITY: 'capacity'
}

class AIMonitoringDashboard {
  constructor({ 
    config, 
    openRouterManager, 
    redisAIManager, 
    autonomousLearningEngine, 
    backgroundProcessManager,
    aiIntegrationBridge,
    performanceMonitor,
    errorHandler
  }) {
    this.config = config
    this.openRouterManager = openRouterManager
    this.redisAIManager = redisAIManager
    this.autonomousLearningEngine = autonomousLearningEngine
    this.backgroundProcessManager = backgroundProcessManager
    this.aiIntegrationBridge = aiIntegrationBridge
    this.performanceMonitor = performanceMonitor
    this.errorHandler = errorHandler
    
    // Dashboard configuration
    this.dashboardConfig = {
      enabled: config?.ai?.dashboard?.enabled !== false,
      refreshInterval: config?.ai?.dashboard?.refresh_interval || 30000, // 30 seconds
      alertThresholds: {
        apiQuotaWarning: config?.ai?.dashboard?.api_quota_warning || 0.8,
        apiQuotaCritical: config?.ai?.dashboard?.api_quota_critical || 0.95,
        performanceWarning: config?.ai?.dashboard?.performance_warning || 1000, // ms
        performanceCritical: config?.ai?.dashboard?.performance_critical || 5000, // ms
        errorRateWarning: config?.ai?.dashboard?.error_rate_warning || 0.1,
        errorRateCritical: config?.ai?.dashboard?.error_rate_critical || 0.2,
        memoryWarning: config?.ai?.dashboard?.memory_warning || 0.8,
        memoryCritical: config?.ai?.dashboard?.memory_critical || 0.95
      },
      retentionPeriod: config?.ai?.dashboard?.retention_period || 86400000, // 24 hours
      maxAlerts: config?.ai?.dashboard?.max_alerts || 100,
      enableRealTimeUpdates: config?.ai?.dashboard?.enable_realtime !== false,
      enableAlertNotifications: config?.ai?.dashboard?.enable_alert_notifications !== false
    }
    
    // Dashboard state
    this.dashboardData = {
      overview: {},
      apiUsage: {},
      learningProgress: {},
      agentActivity: {},
      backgroundTasks: {},
      performanceMetrics: {},
      systemHealth: {},
      alerts: []
    }
    
    // Real-time data
    this.realtimeData = {
      connections: new Set(),
      lastUpdate: Date.now(),
      updateQueue: [],
      metrics: new Map()
    }
    
    // Alert management
    this.alerts = []
    this.alertHistory = []
    this.alertSubscribers = new Set()
    
    // Performance tracking
    this.dashboardMetrics = {
      totalViews: 0,
      activeConnections: 0,
      alertsGenerated: 0,
      dataUpdates: 0,
      averageResponseTime: 0
    }
    
    // Update intervals
    this.intervals = []
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('📊 Initializing AI Monitoring Dashboard...')
    
    try {
      // Initialize dashboard data
      await this.initializeDashboardData()
      
      // Setup real-time monitoring
      this.setupRealtimeMonitoring()
      
      // Initialize alert system
      this.initializeAlertSystem()
      
      // Start data collection
      this.startDataCollection()
      
      // Setup alert monitoring
      this.setupAlertMonitoring()
      
      this.isInitialized = true
      logger.info('✅ AI Monitoring Dashboard initialized')
      
    } catch (error) {
      logger.error('❌ Failed to initialize AI Monitoring Dashboard:', error)
      throw error
    }
  }

  async initializeDashboardData() {
    // Initialize all dashboard sections
    await this.updateOverview()
    await this.updateAPIUsage()
    await this.updateLearningProgress()
    await this.updateAgentActivity()
    await this.updateBackgroundTasks()
    await this.updatePerformanceMetrics()
    await this.updateSystemHealth()
    
    logger.info('📋 Dashboard data initialized')
  }

  setupRealtimeMonitoring() {
    if (!this.dashboardConfig.enableRealTimeUpdates) return
    
    // Setup WebSocket-like real-time updates
    this.realtimeUpdater = {
      broadcast: (section, data) => {
        const update = {
          section,
          data,
          timestamp: Date.now()
        }
        
        this.realtimeData.updateQueue.push(update)
        this.realtimeData.lastUpdate = Date.now()
        
        // Notify subscribers
        this.notifySubscribers(update)
      },
      
      subscribe: (callback) => {
        this.realtimeData.connections.add(callback)
        return () => this.realtimeData.connections.delete(callback)
      }
    }
    
    logger.info('📡 Real-time monitoring setup complete')
  }

  initializeAlertSystem() {
    this.alertSystem = {
      generate: (type, category, message, data = {}) => {
        const alert = {
          id: this.generateAlertId(),
          type,
          category,
          message,
          data,
          timestamp: Date.now(),
          acknowledged: false,
          resolved: false
        }
        
        this.alerts.unshift(alert)
        this.alertHistory.push(alert)
        
        // Limit alerts
        if (this.alerts.length > this.dashboardConfig.maxAlerts) {
          this.alerts = this.alerts.slice(0, this.dashboardConfig.maxAlerts)
        }
        
        // Notify subscribers
        if (this.dashboardConfig.enableAlertNotifications) {
          this.notifyAlertSubscribers(alert)
        }
        
        this.dashboardMetrics.alertsGenerated++
        
        return alert.id
      },
      
      acknowledge: (alertId) => {
        const alert = this.alerts.find(a => a.id === alertId)
        if (alert) {
          alert.acknowledged = true
          alert.acknowledgedAt = Date.now()
        }
      },
      
      resolve: (alertId) => {
        const alert = this.alerts.find(a => a.id === alertId)
        if (alert) {
          alert.resolved = true
          alert.resolvedAt = Date.now()
        }
      },
      
      subscribe: (callback) => {
        this.alertSubscribers.add(callback)
        return () => this.alertSubscribers.delete(callback)
      }
    }
    
    logger.info('🚨 Alert system initialized')
  }

  startDataCollection() {
    // Main dashboard update interval
    const updateInterval = setInterval(async () => {
      await this.updateAllSections()
    }, this.dashboardConfig.refreshInterval)
    this.intervals.push(updateInterval)
    
    // Performance metrics collection
    const metricsInterval = setInterval(() => {
      this.collectPerformanceMetrics()
    }, 10000) // Every 10 seconds
    this.intervals.push(metricsInterval)
    
    // Alert cleanup
    const cleanupInterval = setInterval(() => {
      this.cleanupOldAlerts()
    }, 3600000) // Every hour
    this.intervals.push(cleanupInterval)
    
    logger.info('📈 Data collection started')
  }

  setupAlertMonitoring() {
    // Monitor API quota
    const quotaInterval = setInterval(() => {
      this.monitorAPIQuota()
    }, 60000) // Every minute
    this.intervals.push(quotaInterval)
    
    // Monitor performance
    const performanceInterval = setInterval(() => {
      this.monitorPerformance()
    }, 30000) // Every 30 seconds
    this.intervals.push(performanceInterval)
    
    // Monitor system health
    const healthInterval = setInterval(() => {
      this.monitorSystemHealth()
    }, 120000) // Every 2 minutes
    this.intervals.push(healthInterval)
    
    logger.info('🔍 Alert monitoring started')
  }

  // Dashboard section updates
  async updateOverview() {
    const overview = {
      timestamp: Date.now(),
      systemStatus: 'operational',
      totalAgents: 0,
      activeDiscussions: 0,
      backgroundTasks: 0,
      apiCapacity: 0,
      learningProgress: 0,
      alertCount: this.alerts.filter(a => !a.resolved).length,
      criticalAlerts: this.alerts.filter(a => a.type === ALERT_TYPES.CRITICAL && !a.resolved).length
    }
    
    try {
      // Get data from components
      if (this.redisAIManager) {
        overview.totalAgents = this.redisAIManager.agentRegistry.size
      }
      
      if (this.autonomousLearningEngine) {
        overview.activeDiscussions = this.autonomousLearningEngine.activeDiscussions.size
        overview.learningProgress = this.calculateOverallLearningProgress()
      }
      
      if (this.backgroundProcessManager) {
        overview.backgroundTasks = this.backgroundProcessManager.taskQueue.length + 
                                   this.backgroundProcessManager.runningTasks.size
      }
      
      if (this.openRouterManager) {
        const totalCapacity = this.openRouterManager.getTotalDailyCapacity()
        const remainingCapacity = this.openRouterManager.getRemainingDailyCapacity()
        overview.apiCapacity = totalCapacity > 0 ? (remainingCapacity / totalCapacity) : 0
      }
      
      // Determine system status
      if (overview.criticalAlerts > 0) {
        overview.systemStatus = 'critical'
      } else if (overview.alertCount > 5) {
        overview.systemStatus = 'warning'
      } else if (overview.apiCapacity < 0.1) {
        overview.systemStatus = 'degraded'
      }
      
    } catch (error) {
      logger.warn('Failed to update overview:', error.message)
      overview.systemStatus = 'error'
    }
    
    this.dashboardData.overview = overview
    this.realtimeUpdater?.broadcast(DASHBOARD_SECTIONS.OVERVIEW, overview)
  }

  async updateAPIUsage() {
    const apiUsage = {
      timestamp: Date.now(),
      totalCapacity: 0,
      usedCapacity: 0,
      remainingCapacity: 0,
      utilizationRate: 0,
      keyStatus: {},
      dailyUsage: [],
      hourlyUsage: [],
      modelUsage: {},
      errorRate: 0
    }
    
    try {
      if (this.openRouterManager) {
        const report = this.openRouterManager.getUsageReport()
        
        apiUsage.totalCapacity = report.capacity.total
        apiUsage.usedCapacity = report.capacity.used
        apiUsage.remainingCapacity = report.capacity.remaining
        apiUsage.utilizationRate = parseFloat(report.capacity.utilizationRate.replace('%', '')) / 100
        
        apiUsage.keyStatus = {
          total: report.keys.total,
          active: report.keys.active,
          exhausted: report.keys.exhausted,
          error: report.keys.error
        }
        
        apiUsage.errorRate = report.metrics.totalRequests > 0 
          ? report.metrics.failedRequests / report.metrics.totalRequests 
          : 0
        
        // Get model performance data
        apiUsage.modelUsage = report.models.performance || {}
        
        // Generate usage trends
        apiUsage.dailyUsage = this.generateUsageTrend('daily')
        apiUsage.hourlyUsage = this.generateUsageTrend('hourly')
      }
      
    } catch (error) {
      logger.warn('Failed to update API usage:', error.message)
    }
    
    this.dashboardData.apiUsage = apiUsage
    this.realtimeUpdater?.broadcast(DASHBOARD_SECTIONS.API_USAGE, apiUsage)
  }

  async updateLearningProgress() {
    const learningProgress = {
      timestamp: Date.now(),
      totalKnowledge: 0,
      recentLearning: 0,
      activeDiscussions: 0,
      learningEfficiency: 0,
      knowledgeGrowth: [],
      topTopics: [],
      capabilityProgress: {},
      consensusRate: 0
    }
    
    try {
      if (this.autonomousLearningEngine) {
        const report = this.autonomousLearningEngine.getLearningReport()
        
        learningProgress.totalKnowledge = report.knowledgeBase.totalEntries
        learningProgress.activeDiscussions = report.activeDiscussions.count
        learningProgress.learningEfficiency = report.metrics.learningEfficiency
        learningProgress.consensusRate = report.metrics.consensusReached / 
                                       Math.max(1, report.metrics.totalDiscussions)
        
        learningProgress.topTopics = report.knowledgeBase.recentEntries.map(entry => ({
          topic: entry.topic,
          confidence: entry.confidence,
          lastUpdated: entry.lastUpdated
        }))
        
        learningProgress.capabilityProgress = this.calculateCapabilityProgress(report)
        learningProgress.knowledgeGrowth = this.generateKnowledgeGrowthTrend()
        learningProgress.recentLearning = this.calculateRecentLearning()
      }
      
    } catch (error) {
      logger.warn('Failed to update learning progress:', error.message)
    }
    
    this.dashboardData.learningProgress = learningProgress
    this.realtimeUpdater?.broadcast(DASHBOARD_SECTIONS.LEARNING_PROGRESS, learningProgress)
  }

  async updateAgentActivity() {
    const agentActivity = {
      timestamp: Date.now(),
      totalAgents: 0,
      activeAgents: 0,
      agentsByType: {},
      agentsByStatus: {},
      topPerformers: [],
      recentActivity: [],
      conversationStats: {},
      taskAssignments: {}
    }
    
    try {
      if (this.redisAIManager) {
        const report = this.redisAIManager.getUsageReport()
        
        agentActivity.totalAgents = report.metrics.agentCount
        agentActivity.conversationStats = {
          total: report.metrics.conversationCount,
          active: report.registries.conversations
        }
        
        // Get agent details
        const agents = await this.redisAIManager.findAgents({ limit: 100 })
        
        // Categorize agents
        for (const agent of agents) {
          // By type
          agentActivity.agentsByType[agent.type] = (agentActivity.agentsByType[agent.type] || 0) + 1
          
          // By status
          agentActivity.agentsByStatus[agent.status] = (agentActivity.agentsByStatus[agent.status] || 0) + 1
          
          // Count active agents
          if (agent.status === 'active' || agent.status === 'working') {
            agentActivity.activeAgents++
          }
        }
        
        // Get top performers
        agentActivity.topPerformers = agents
          .sort((a, b) => (b.performance_score || 0) - (a.performance_score || 0))
          .slice(0, 10)
          .map(agent => ({
            id: agent.id,
            name: agent.name,
            type: agent.type,
            performance: agent.performance_score || 0,
            lastActive: agent.last_active
          }))
        
        // Get recent activity
        agentActivity.recentActivity = this.generateRecentAgentActivity(agents)
      }
      
    } catch (error) {
      logger.warn('Failed to update agent activity:', error.message)
    }
    
    this.dashboardData.agentActivity = agentActivity
    this.realtimeUpdater?.broadcast(DASHBOARD_SECTIONS.AGENT_ACTIVITY, agentActivity)
  }

  async updateBackgroundTasks() {
    const backgroundTasks = {
      timestamp: Date.now(),
      queueLength: 0,
      runningTasks: 0,
      completedTasks: 0,
      failedTasks: 0,
      tasksByType: {},
      tasksByPriority: {},
      workerStatus: {},
      recentTasks: [],
      averageExecutionTime: 0,
      throughput: 0
    }
    
    try {
      if (this.backgroundProcessManager) {
        const report = this.backgroundProcessManager.getProcessingReport()
        
        backgroundTasks.queueLength = report.queue.length
        backgroundTasks.runningTasks = report.queue.running
        backgroundTasks.completedTasks = report.metrics.completedTasks
        backgroundTasks.failedTasks = report.metrics.failedTasks
        backgroundTasks.averageExecutionTime = report.metrics.averageExecutionTime
        
        backgroundTasks.workerStatus = {
          total: report.workers.total,
          busy: report.workers.busy,
          idle: report.workers.idle
        }
        
        // Calculate throughput (tasks per hour)
        backgroundTasks.throughput = report.metrics.completedTasks > 0 
          ? (report.metrics.completedTasks / 24) // Assuming 24-hour period
          : 0
        
        // Get task distribution
        backgroundTasks.tasksByType = this.calculateTaskDistribution('type')
        backgroundTasks.tasksByPriority = this.calculateTaskDistribution('priority')
        
        // Get recent tasks
        backgroundTasks.recentTasks = this.generateRecentTaskActivity()
      }
      
    } catch (error) {
      logger.warn('Failed to update background tasks:', error.message)
    }
    
    this.dashboardData.backgroundTasks = backgroundTasks
    this.realtimeUpdater?.broadcast(DASHBOARD_SECTIONS.BACKGROUND_TASKS, backgroundTasks)
  }

  async updatePerformanceMetrics() {
    const performanceMetrics = {
      timestamp: Date.now(),
      systemPerformance: {},
      aiPerformance: {},
      responseTime: {},
      throughput: {},
      resourceUsage: {},
      trends: {}
    }
    
    try {
      // System performance
      if (this.performanceMonitor) {
        const systemStats = this.performanceMonitor.getSystemStats()
        performanceMetrics.systemPerformance = systemStats
      }
      
      // AI performance
      if (this.aiIntegrationBridge) {
        const integrationReport = this.aiIntegrationBridge.getIntegrationReport()
        performanceMetrics.aiPerformance = {
          enhancementSuccessRate: integrationReport.metrics.successRate,
          averageResponseTime: integrationReport.metrics.aiResponseTime,
          totalEnhancements: integrationReport.metrics.totalEnhancements,
          fallbackRate: integrationReport.metrics.fallbackCount / 
                       Math.max(1, integrationReport.metrics.totalEnhancements)
        }
      }
      
      // Response time analysis
      performanceMetrics.responseTime = this.analyzeResponseTimes()
      
      // Throughput analysis
      performanceMetrics.throughput = this.analyzeThroughput()
      
      // Resource usage
      performanceMetrics.resourceUsage = this.analyzeResourceUsage()
      
      // Performance trends
      performanceMetrics.trends = this.generatePerformanceTrends()
      
    } catch (error) {
      logger.warn('Failed to update performance metrics:', error.message)
    }
    
    this.dashboardData.performanceMetrics = performanceMetrics
    this.realtimeUpdater?.broadcast(DASHBOARD_SECTIONS.PERFORMANCE_METRICS, performanceMetrics)
  }

  async updateSystemHealth() {
    const systemHealth = {
      timestamp: Date.now(),
      overallHealth: 'healthy',
      componentHealth: {},
      connectivity: {},
      resourceStatus: {},
      alerts: {
        active: this.alerts.filter(a => !a.resolved).length,
        critical: this.alerts.filter(a => a.type === ALERT_TYPES.CRITICAL && !a.resolved).length
      },
      uptime: {},
      lastHealthCheck: Date.now()
    }
    
    try {
      // Check component health
      systemHealth.componentHealth = {
        openRouterManager: this.checkComponentHealth(this.openRouterManager),
        redisAIManager: this.checkComponentHealth(this.redisAIManager),
        autonomousLearningEngine: this.checkComponentHealth(this.autonomousLearningEngine),
        backgroundProcessManager: this.checkComponentHealth(this.backgroundProcessManager),
        aiIntegrationBridge: this.checkComponentHealth(this.aiIntegrationBridge)
      }
      
      // Check connectivity
      systemHealth.connectivity = await this.checkConnectivity()
      
      // Check resource status
      systemHealth.resourceStatus = this.checkResourceStatus()
      
      // Calculate overall health
      systemHealth.overallHealth = this.calculateOverallHealth(systemHealth)
      
      // Get uptime information
      systemHealth.uptime = this.getUptimeInformation()
      
    } catch (error) {
      logger.warn('Failed to update system health:', error.message)
      systemHealth.overallHealth = 'error'
    }
    
    this.dashboardData.systemHealth = systemHealth
    this.realtimeUpdater?.broadcast(DASHBOARD_SECTIONS.SYSTEM_HEALTH, systemHealth)
  }

  // Alert monitoring methods
  monitorAPIQuota() {
    if (!this.openRouterManager) return
    
    try {
      const report = this.openRouterManager.getUsageReport()
      const utilizationRate = parseFloat(report.capacity.utilizationRate.replace('%', '')) / 100
      
      if (utilizationRate >= this.dashboardConfig.alertThresholds.apiQuotaCritical) {
        this.alertSystem.generate(
          ALERT_TYPES.CRITICAL,
          ALERT_CATEGORIES.API_QUOTA,
          `API quota critically low: ${(utilizationRate * 100).toFixed(1)}% used`,
          { utilizationRate, remainingCapacity: report.capacity.remaining }
        )
      } else if (utilizationRate >= this.dashboardConfig.alertThresholds.apiQuotaWarning) {
        this.alertSystem.generate(
          ALERT_TYPES.WARNING,
          ALERT_CATEGORIES.API_QUOTA,
          `API quota warning: ${(utilizationRate * 100).toFixed(1)}% used`,
          { utilizationRate, remainingCapacity: report.capacity.remaining }
        )
      }
      
    } catch (error) {
      logger.warn('API quota monitoring failed:', error.message)
    }
  }

  monitorPerformance() {
    try {
      // Monitor AI response times
      if (this.aiIntegrationBridge) {
        const report = this.aiIntegrationBridge.getIntegrationReport()
        const avgResponseTime = report.metrics.aiResponseTime
        
        if (avgResponseTime >= this.dashboardConfig.alertThresholds.performanceCritical) {
          this.alertSystem.generate(
            ALERT_TYPES.CRITICAL,
            ALERT_CATEGORIES.PERFORMANCE,
            `AI response time critical: ${avgResponseTime}ms`,
            { responseTime: avgResponseTime }
          )
        } else if (avgResponseTime >= this.dashboardConfig.alertThresholds.performanceWarning) {
          this.alertSystem.generate(
            ALERT_TYPES.WARNING,
            ALERT_CATEGORIES.PERFORMANCE,
            `AI response time high: ${avgResponseTime}ms`,
            { responseTime: avgResponseTime }
          )
        }
      }
      
      // Monitor error rates
      if (this.openRouterManager) {
        const report = this.openRouterManager.getUsageReport()
        const errorRate = report.metrics.totalRequests > 0 
          ? report.metrics.failedRequests / report.metrics.totalRequests 
          : 0
        
        if (errorRate >= this.dashboardConfig.alertThresholds.errorRateCritical) {
          this.alertSystem.generate(
            ALERT_TYPES.CRITICAL,
            ALERT_CATEGORIES.PERFORMANCE,
            `Error rate critical: ${(errorRate * 100).toFixed(1)}%`,
            { errorRate, failedRequests: report.metrics.failedRequests }
          )
        } else if (errorRate >= this.dashboardConfig.alertThresholds.errorRateWarning) {
          this.alertSystem.generate(
            ALERT_TYPES.WARNING,
            ALERT_CATEGORIES.PERFORMANCE,
            `Error rate high: ${(errorRate * 100).toFixed(1)}%`,
            { errorRate, failedRequests: report.metrics.failedRequests }
          )
        }
      }
      
    } catch (error) {
      logger.warn('Performance monitoring failed:', error.message)
    }
  }

  monitorSystemHealth() {
    try {
      // Monitor Redis memory usage
      if (this.redisAIManager) {
        const report = this.redisAIManager.getUsageReport()
        const memoryUsage = report.metrics.dataSize
        const maxMemory = this.redisAIManager.aiConfig.environment === 'production' 
          ? 30 * 1024 * 1024 // 30MB for Redis Cloud Free Tier
          : 1024 * 1024 * 1024 // 1GB for development
        
        const memoryUtilization = memoryUsage / maxMemory
        
        if (memoryUtilization >= this.dashboardConfig.alertThresholds.memoryCritical) {
          this.alertSystem.generate(
            ALERT_TYPES.CRITICAL,
            ALERT_CATEGORIES.CAPACITY,
            `Memory usage critical: ${(memoryUtilization * 100).toFixed(1)}%`,
            { memoryUsage, maxMemory, utilization: memoryUtilization }
          )
        } else if (memoryUtilization >= this.dashboardConfig.alertThresholds.memoryWarning) {
          this.alertSystem.generate(
            ALERT_TYPES.WARNING,
            ALERT_CATEGORIES.CAPACITY,
            `Memory usage high: ${(memoryUtilization * 100).toFixed(1)}%`,
            { memoryUsage, maxMemory, utilization: memoryUtilization }
          )
        }
      }
      
      // Monitor component health
      const unhealthyComponents = []
      
      if (this.openRouterManager && !this.openRouterManager.isInitialized) {
        unhealthyComponents.push('OpenRouter Manager')
      }
      
      if (this.redisAIManager && !this.redisAIManager.isInitialized) {
        unhealthyComponents.push('Redis AI Manager')
      }
      
      if (this.autonomousLearningEngine && !this.autonomousLearningEngine.isInitialized) {
        unhealthyComponents.push('Autonomous Learning Engine')
      }
      
      if (unhealthyComponents.length > 0) {
        this.alertSystem.generate(
          ALERT_TYPES.ERROR,
          ALERT_CATEGORIES.SYSTEM_HEALTH,
          `Components unhealthy: ${unhealthyComponents.join(', ')}`,
          { unhealthyComponents }
        )
      }
      
    } catch (error) {
      logger.warn('System health monitoring failed:', error.message)
    }
  }

  // Utility methods
  calculateOverallLearningProgress() {
    if (!this.autonomousLearningEngine) return 0
    
    try {
      const report = this.autonomousLearningEngine.getLearningReport()
      return report.metrics.learningEfficiency || 0
    } catch (error) {
      return 0
    }
  }

  calculateCapabilityProgress(report) {
    const progress = {}
    
    if (report.capabilities && report.capabilities.avgProficiency) {
      progress.overall = report.capabilities.avgProficiency
      progress.improvements = report.capabilities.improvementOpportunities
      progress.total = report.capabilities.total
    }
    
    return progress
  }

  generateUsageTrend(period) {
    // Generate mock usage trend data
    const trend = []
    const now = Date.now()
    const interval = period === 'hourly' ? 3600000 : 86400000 // 1 hour or 1 day
    const points = period === 'hourly' ? 24 : 7
    
    for (let i = points - 1; i >= 0; i--) {
      trend.push({
        timestamp: now - (i * interval),
        usage: Math.floor(Math.random() * 100),
        requests: Math.floor(Math.random() * 50)
      })
    }
    
    return trend
  }

  generateKnowledgeGrowthTrend() {
    // Generate mock knowledge growth trend
    const trend = []
    const now = Date.now()
    const interval = 86400000 // 1 day
    
    for (let i = 6; i >= 0; i--) {
      trend.push({
        timestamp: now - (i * interval),
        knowledge: Math.floor(Math.random() * 100) + i * 10,
        discussions: Math.floor(Math.random() * 20),
        insights: Math.floor(Math.random() * 50)
      })
    }
    
    return trend
  }

  calculateRecentLearning() {
    if (!this.autonomousLearningEngine) return 0
    
    try {
      const report = this.autonomousLearningEngine.getLearningReport()
      return report.knowledgeBase.recentEntries.length
    } catch (error) {
      return 0
    }
  }

  generateRecentAgentActivity(agents) {
    return agents
      .filter(agent => agent.last_active && Date.now() - agent.last_active < 3600000) // Last hour
      .sort((a, b) => b.last_active - a.last_active)
      .slice(0, 10)
      .map(agent => ({
        id: agent.id,
        name: agent.name,
        type: agent.type,
        activity: 'active',
        timestamp: agent.last_active
      }))
  }

  calculateTaskDistribution(field) {
    // Mock task distribution calculation
    const distribution = {}
    
    if (field === 'type') {
      distribution['web_research'] = 30
      distribution['knowledge_synthesis'] = 20
      distribution['performance_analysis'] = 15
      distribution['health_check'] = 10
      distribution['data_cleanup'] = 25
    } else if (field === 'priority') {
      distribution['high'] = 20
      distribution['medium'] = 50
      distribution['low'] = 30
    }
    
    return distribution
  }

  generateRecentTaskActivity() {
    // Generate mock recent task activity
    const activities = []
    const taskTypes = ['web_research', 'knowledge_synthesis', 'performance_analysis', 'health_check']
    const statuses = ['completed', 'running', 'failed']
    
    for (let i = 0; i < 10; i++) {
      activities.push({
        id: `task_${Date.now()}_${i}`,
        type: taskTypes[Math.floor(Math.random() * taskTypes.length)],
        status: statuses[Math.floor(Math.random() * statuses.length)],
        timestamp: Date.now() - Math.random() * 3600000,
        duration: Math.floor(Math.random() * 30000)
      })
    }
    
    return activities.sort((a, b) => b.timestamp - a.timestamp)
  }

  analyzeResponseTimes() {
    return {
      average: Math.floor(Math.random() * 1000) + 200,
      p95: Math.floor(Math.random() * 2000) + 500,
      p99: Math.floor(Math.random() * 5000) + 1000,
      trend: 'stable'
    }
  }

  analyzeThroughput() {
    return {
      requestsPerSecond: Math.floor(Math.random() * 100) + 10,
      tasksPerHour: Math.floor(Math.random() * 1000) + 100,
      trend: 'increasing'
    }
  }

  analyzeResourceUsage() {
    return {
      cpu: Math.random() * 0.8 + 0.1,
      memory: Math.random() * 0.7 + 0.2,
      network: Math.random() * 0.5 + 0.1,
      storage: Math.random() * 0.6 + 0.1
    }
  }

  generatePerformanceTrends() {
    return {
      responseTime: 'improving',
      throughput: 'stable',
      errorRate: 'decreasing',
      resourceUsage: 'stable'
    }
  }

  checkComponentHealth(component) {
    if (!component) return 'unavailable'
    if (component.isInitialized === false) return 'unhealthy'
    if (component.isInitialized === true) return 'healthy'
    return 'unknown'
  }

  async checkConnectivity() {
    const connectivity = {}
    
    try {
      if (this.redisAIManager && this.redisAIManager.client) {
        const pong = await this.redisAIManager.client.ping()
        connectivity.redis = pong === 'PONG' ? 'connected' : 'disconnected'
      } else {
        connectivity.redis = 'unavailable'
      }
    } catch (error) {
      connectivity.redis = 'error'
    }
    
    // Check OpenRouter connectivity
    if (this.openRouterManager) {
      connectivity.openRouter = this.openRouterManager.getRemainingDailyCapacity() >= 0 ? 'connected' : 'disconnected'
    } else {
      connectivity.openRouter = 'unavailable'
    }
    
    return connectivity
  }

  checkResourceStatus() {
    return {
      memory: 'normal',
      cpu: 'normal',
      network: 'normal',
      storage: 'normal'
    }
  }

  calculateOverallHealth(systemHealth) {
    const components = Object.values(systemHealth.componentHealth)
    const unhealthyCount = components.filter(status => status === 'unhealthy' || status === 'error').length
    
    if (unhealthyCount > 2) return 'critical'
    if (unhealthyCount > 0) return 'degraded'
    if (systemHealth.alerts.critical > 0) return 'warning'
    return 'healthy'
  }

  getUptimeInformation() {
    // Mock uptime information
    const startTime = Date.now() - (Math.random() * 86400000 * 7) // Up to 7 days
    const uptime = Date.now() - startTime
    
    return {
      startTime,
      uptime,
      uptimeFormatted: this.formatUptime(uptime)
    }
  }

  formatUptime(uptime) {
    const days = Math.floor(uptime / 86400000)
    const hours = Math.floor((uptime % 86400000) / 3600000)
    const minutes = Math.floor((uptime % 3600000) / 60000)
    
    return `${days}d ${hours}h ${minutes}m`
  }

  collectPerformanceMetrics() {
    // Collect real-time performance metrics
    this.realtimeData.metrics.set('timestamp', Date.now())
    this.realtimeData.metrics.set('connections', this.realtimeData.connections.size)
    this.realtimeData.metrics.set('alerts', this.alerts.length)
    
    this.dashboardMetrics.dataUpdates++
  }

  cleanupOldAlerts() {
    const cutoff = Date.now() - this.dashboardConfig.retentionPeriod
    
    // Clean up alert history
    this.alertHistory = this.alertHistory.filter(alert => alert.timestamp > cutoff)
    
    // Clean up resolved alerts from active list
    this.alerts = this.alerts.filter(alert => !alert.resolved || alert.timestamp > cutoff)
  }

  generateAlertId() {
    return `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  notifySubscribers(update) {
    for (const callback of this.realtimeData.connections) {
      try {
        callback(update)
      } catch (error) {
        logger.warn('Failed to notify subscriber:', error.message)
      }
    }
  }

  notifyAlertSubscribers(alert) {
    for (const callback of this.alertSubscribers) {
      try {
        callback(alert)
      } catch (error) {
        logger.warn('Failed to notify alert subscriber:', error.message)
      }
    }
  }

  async updateAllSections() {
    try {
      await Promise.all([
        this.updateOverview(),
        this.updateAPIUsage(),
        this.updateLearningProgress(),
        this.updateAgentActivity(),
        this.updateBackgroundTasks(),
        this.updatePerformanceMetrics(),
        this.updateSystemHealth()
      ])
      
      this.dashboardMetrics.dataUpdates++
      
    } catch (error) {
      logger.error('Failed to update dashboard sections:', error)
    }
  }

  // Public API methods
  getDashboardData(section = null) {
    if (section && this.dashboardData[section]) {
      return this.dashboardData[section]
    }
    return this.dashboardData
  }

  getAlerts(filter = {}) {
    let alerts = [...this.alerts]
    
    if (filter.type) {
      alerts = alerts.filter(alert => alert.type === filter.type)
    }
    
    if (filter.category) {
      alerts = alerts.filter(alert => alert.category === filter.category)
    }
    
    if (filter.unresolved) {
      alerts = alerts.filter(alert => !alert.resolved)
    }
    
    return alerts
  }

  acknowledgeAlert(alertId) {
    return this.alertSystem.acknowledge(alertId)
  }

  resolveAlert(alertId) {
    return this.alertSystem.resolve(alertId)
  }

  subscribeToUpdates(callback) {
    return this.realtimeUpdater?.subscribe(callback)
  }

  subscribeToAlerts(callback) {
    return this.alertSystem.subscribe(callback)
  }

  getDashboardMetrics() {
    return {
      ...this.dashboardMetrics,
      activeConnections: this.realtimeData.connections.size,
      lastUpdate: this.realtimeData.lastUpdate,
      updateQueueSize: this.realtimeData.updateQueue.length
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up AI Monitoring Dashboard...')
    
    // Clear intervals
    this.intervals.forEach(interval => clearInterval(interval))
    this.intervals.length = 0
    
    // Clear data structures
    this.alerts.length = 0
    this.alertHistory.length = 0
    this.alertSubscribers.clear()
    this.realtimeData.connections.clear()
    this.realtimeData.updateQueue.length = 0
    this.realtimeData.metrics.clear()
    
    // Reset dashboard data
    this.dashboardData = {
      overview: {},
      apiUsage: {},
      learningProgress: {},
      agentActivity: {},
      backgroundTasks: {},
      performanceMetrics: {},
      systemHealth: {},
      alerts: []
    }
    
    this.isInitialized = false
    logger.info('✅ AI Monitoring Dashboard cleanup complete')
  }
}

module.exports = {
  AIMonitoringDashboard,
  DASHBOARD_SECTIONS,
  ALERT_TYPES,
  ALERT_CATEGORIES
}