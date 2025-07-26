/**
 * JAEGIS Performance Monitor
 * Advanced performance monitoring and analytics system
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const os = require('os')
const process = require('process')
const logger = require('../utils/logger')

class PerformanceMonitor {
  constructor({ config, cache }) {
    this.config = config
    this.cache = cache
    
    // Monitoring configuration
    this.monitoringConfig = {
      enabled: config?.monitoring?.enabled || true,
      interval: config?.monitoring?.interval || 30000, // 30 seconds
      retention: config?.monitoring?.retention || 86400000, // 24 hours
      alertThresholds: {
        cpu: config?.monitoring?.thresholds?.cpu || 80,
        memory: config?.monitoring?.thresholds?.memory || 80,
        responseTime: config?.monitoring?.thresholds?.response_time || 5000,
        errorRate: config?.monitoring?.thresholds?.error_rate || 5
      }
    }
    
    // Performance data storage
    this.metrics = {
      system: [],
      commands: new Map(),
      plugins: new Map(),
      errors: [],
      requests: [],
      cache: [],
      python: []
    }
    
    // Real-time tracking
    this.currentMetrics = {
      activeRequests: 0,
      totalRequests: 0,
      totalErrors: 0,
      startTime: Date.now(),
      lastUpdate: Date.now()
    }
    
    // Performance counters
    this.counters = {
      commandExecutions: new Map(),
      pluginExecutions: new Map(),
      errorCounts: new Map(),
      responseTimeHistogram: new Map()
    }
    
    // Monitoring intervals
    this.intervals = {
      system: null,
      cleanup: null,
      alerts: null
    }
    
    // Alert system
    this.alerts = {
      active: new Map(),
      history: [],
      cooldown: new Map()
    }
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('📊 Initializing Performance Monitor...')
    
    try {
      // Load historical data
      await this.loadHistoricalData()
      
      // Start monitoring if enabled
      if (this.monitoringConfig.enabled) {
        this.startMonitoring()
      }
      
      // Setup cleanup
      this.setupCleanup()
      
      // Setup alert system
      this.setupAlertSystem()
      
      this.isInitialized = true
      logger.info('✅ Performance Monitor initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Performance Monitor:', error)
      throw error
    }
  }

  startMonitoring() {
    // System metrics monitoring
    this.intervals.system = setInterval(() => {
      this.collectSystemMetrics()
    }, this.monitoringConfig.interval)
    
    // Alert checking
    this.intervals.alerts = setInterval(() => {
      this.checkAlerts()
    }, 60000) // Check alerts every minute
    
    logger.info(`📊 Performance monitoring started (interval: ${this.monitoringConfig.interval}ms)`)
  }

  async collectSystemMetrics() {
    try {
      const timestamp = Date.now()
      
      // CPU metrics
      const cpuUsage = process.cpuUsage()
      const cpuPercent = this.calculateCPUPercent(cpuUsage)
      
      // Memory metrics
      const memoryUsage = process.memoryUsage()
      const systemMemory = {
        total: os.totalmem(),
        free: os.freemem(),
        used: os.totalmem() - os.freemem()
      }
      
      // System load
      const loadAverage = os.loadavg()
      
      // Network and I/O (basic)
      const networkStats = this.getNetworkStats()
      
      // Event loop lag
      const eventLoopLag = this.measureEventLoopLag()
      
      const systemMetric = {
        timestamp,
        cpu: {
          usage: cpuUsage,
          percent: cpuPercent,
          cores: os.cpus().length
        },
        memory: {
          process: memoryUsage,
          system: systemMemory,
          percentUsed: (memoryUsage.heapUsed / memoryUsage.heapTotal) * 100
        },
        load: {
          average: loadAverage,
          current: loadAverage[0]
        },
        network: networkStats,
        eventLoop: {
          lag: await eventLoopLag
        },
        uptime: process.uptime(),
        platform: os.platform(),
        nodeVersion: process.version
      }
      
      // Store metric
      this.metrics.system.push(systemMetric)
      this.trimMetrics('system')
      
      // Update current metrics
      this.currentMetrics.lastUpdate = timestamp
      
      logger.debug('📊 System metrics collected', {
        cpu: cpuPercent,
        memory: systemMetric.memory.percentUsed,
        load: loadAverage[0]
      })
      
    } catch (error) {
      logger.error('Failed to collect system metrics:', error)
    }
  }

  calculateCPUPercent(cpuUsage) {
    // Simple CPU percentage calculation
    // This is a basic implementation - in production you'd want more sophisticated tracking
    const totalUsage = cpuUsage.user + cpuUsage.system
    const totalTime = process.uptime() * 1000000 // Convert to microseconds
    
    return Math.min((totalUsage / totalTime) * 100, 100)
  }

  getNetworkStats() {
    // Basic network stats - in production you'd use more detailed monitoring
    return {
      connections: this.currentMetrics.activeRequests,
      totalRequests: this.currentMetrics.totalRequests,
      requestsPerSecond: this.calculateRequestsPerSecond()
    }
  }

  calculateRequestsPerSecond() {
    const now = Date.now()
    const oneSecondAgo = now - 1000
    
    const recentRequests = this.metrics.requests.filter(
      req => req.timestamp > oneSecondAgo
    )
    
    return recentRequests.length
  }

  async measureEventLoopLag() {
    return new Promise((resolve) => {
      const start = process.hrtime.bigint()
      setImmediate(() => {
        const lag = Number(process.hrtime.bigint() - start) / 1000000 // Convert to milliseconds
        resolve(lag)
      })
    })
  }

  // Request tracking
  trackRequest(requestInfo) {
    const timestamp = Date.now()
    
    this.currentMetrics.activeRequests++
    this.currentMetrics.totalRequests++
    
    const requestMetric = {
      id: requestInfo.id || this.generateId(),
      timestamp,
      method: requestInfo.method,
      path: requestInfo.path,
      userAgent: requestInfo.userAgent,
      ip: requestInfo.ip,
      startTime: timestamp
    }
    
    this.metrics.requests.push(requestMetric)
    this.trimMetrics('requests')
    
    return requestMetric.id
  }

  trackRequestEnd(requestId, responseInfo) {
    const endTime = Date.now()
    
    this.currentMetrics.activeRequests = Math.max(0, this.currentMetrics.activeRequests - 1)
    
    // Find and update request metric
    const requestMetric = this.metrics.requests.find(req => req.id === requestId)
    if (requestMetric) {
      requestMetric.endTime = endTime
      requestMetric.duration = endTime - requestMetric.startTime
      requestMetric.statusCode = responseInfo.statusCode
      requestMetric.responseSize = responseInfo.responseSize
      
      // Update response time histogram
      this.updateResponseTimeHistogram(requestMetric.duration)
      
      // Track errors
      if (responseInfo.statusCode >= 400) {
        this.trackError({
          type: 'http_error',
          statusCode: responseInfo.statusCode,
          path: requestMetric.path,
          duration: requestMetric.duration,
          timestamp: endTime
        })
      }
    }
  }

  // Command performance tracking
  trackCommandExecution(command, executionInfo) {
    const timestamp = Date.now()
    
    // Update command counter
    const commandCount = this.counters.commandExecutions.get(command) || 0
    this.counters.commandExecutions.set(command, commandCount + 1)
    
    // Store command metric
    if (!this.metrics.commands.has(command)) {
      this.metrics.commands.set(command, [])
    }
    
    const commandMetric = {
      timestamp,
      command,
      executionId: executionInfo.executionId,
      duration: executionInfo.duration,
      success: executionInfo.success,
      plugin: executionInfo.plugin,
      parameters: Object.keys(executionInfo.parameters || {}).length,
      cacheHit: executionInfo.cacheHit || false
    }
    
    this.metrics.commands.get(command).push(commandMetric)
    this.trimCommandMetrics(command)
    
    logger.performance('Command execution', executionInfo.duration, {
      command,
      success: executionInfo.success,
      plugin: executionInfo.plugin
    })
  }

  // Plugin performance tracking
  trackPluginExecution(plugin, executionInfo) {
    const timestamp = Date.now()
    
    // Update plugin counter
    const pluginCount = this.counters.pluginExecutions.get(plugin) || 0
    this.counters.pluginExecutions.set(plugin, pluginCount + 1)
    
    // Store plugin metric
    if (!this.metrics.plugins.has(plugin)) {
      this.metrics.plugins.set(plugin, [])
    }
    
    const pluginMetric = {
      timestamp,
      plugin,
      executionId: executionInfo.executionId,
      duration: executionInfo.duration,
      success: executionInfo.success,
      command: executionInfo.command,
      memoryUsage: process.memoryUsage().heapUsed
    }
    
    this.metrics.plugins.get(plugin).push(pluginMetric)
    this.trimPluginMetrics(plugin)
  }

  // Error tracking
  trackError(errorInfo) {
    const timestamp = Date.now()
    
    this.currentMetrics.totalErrors++
    
    // Update error counter
    const errorKey = `${errorInfo.type}:${errorInfo.statusCode || 'unknown'}`
    const errorCount = this.counters.errorCounts.get(errorKey) || 0
    this.counters.errorCounts.set(errorKey, errorCount + 1)
    
    const errorMetric = {
      timestamp,
      type: errorInfo.type,
      message: errorInfo.message,
      statusCode: errorInfo.statusCode,
      path: errorInfo.path,
      duration: errorInfo.duration,
      severity: errorInfo.severity || 'medium'
    }
    
    this.metrics.errors.push(errorMetric)
    this.trimMetrics('errors')
  }

  // Cache performance tracking
  trackCacheOperation(operation, info) {
    const timestamp = Date.now()
    
    const cacheMetric = {
      timestamp,
      operation, // get, set, delete, clear
      key: info.key,
      hit: info.hit,
      duration: info.duration,
      size: info.size,
      backend: info.backend // memory, redis
    }
    
    this.metrics.cache.push(cacheMetric)
    this.trimMetrics('cache')
  }

  // Python bridge performance tracking
  trackPythonOperation(operation, info) {
    const timestamp = Date.now()
    
    const pythonMetric = {
      timestamp,
      operation,
      duration: info.duration,
      success: info.success,
      endpoint: info.endpoint,
      responseSize: info.responseSize
    }
    
    this.metrics.python.push(pythonMetric)
    this.trimMetrics('python')
  }

  // Response time histogram
  updateResponseTimeHistogram(duration) {
    // Create buckets for response times
    const buckets = [50, 100, 200, 500, 1000, 2000, 5000, 10000]
    
    for (const bucket of buckets) {
      if (duration <= bucket) {
        const count = this.counters.responseTimeHistogram.get(bucket) || 0
        this.counters.responseTimeHistogram.set(bucket, count + 1)
        break
      }
    }
    
    // Handle very slow responses
    if (duration > 10000) {
      const count = this.counters.responseTimeHistogram.get('slow') || 0
      this.counters.responseTimeHistogram.set('slow', count + 1)
    }
  }

  // Analytics and reporting
  getSystemStats() {
    const latestSystem = this.metrics.system[this.metrics.system.length - 1]
    
    if (!latestSystem) {
      return {
        status: 'no_data',
        message: 'No system metrics available'
      }
    }
    
    return {
      current: {
        cpu: latestSystem.cpu.percent,
        memory: latestSystem.memory.percentUsed,
        load: latestSystem.load.current,
        uptime: latestSystem.uptime,
        activeRequests: this.currentMetrics.activeRequests
      },
      totals: {
        requests: this.currentMetrics.totalRequests,
        errors: this.currentMetrics.totalErrors,
        commands: Array.from(this.counters.commandExecutions.values()).reduce((a, b) => a + b, 0),
        plugins: Array.from(this.counters.pluginExecutions.values()).reduce((a, b) => a + b, 0)
      },
      rates: {
        requestsPerSecond: this.calculateRequestsPerSecond(),
        errorRate: this.calculateErrorRate(),
        successRate: this.calculateSuccessRate()
      }
    }
  }

  getCommandStats() {
    const stats = {}
    
    for (const [command, metrics] of this.metrics.commands) {
      const successful = metrics.filter(m => m.success).length
      const total = metrics.length
      const durations = metrics.map(m => m.duration)
      
      stats[command] = {
        totalExecutions: total,
        successfulExecutions: successful,
        successRate: total > 0 ? (successful / total * 100).toFixed(2) + '%' : '0%',
        averageDuration: durations.length > 0 ? Math.round(durations.reduce((a, b) => a + b, 0) / durations.length) : 0,
        minDuration: durations.length > 0 ? Math.min(...durations) : 0,
        maxDuration: durations.length > 0 ? Math.max(...durations) : 0,
        recentExecutions: metrics.slice(-10)
      }
    }
    
    return stats
  }

  getPluginStats() {
    const stats = {}
    
    for (const [plugin, metrics] of this.metrics.plugins) {
      const successful = metrics.filter(m => m.success).length
      const total = metrics.length
      const durations = metrics.map(m => m.duration)
      
      stats[plugin] = {
        totalExecutions: total,
        successfulExecutions: successful,
        successRate: total > 0 ? (successful / total * 100).toFixed(2) + '%' : '0%',
        averageDuration: durations.length > 0 ? Math.round(durations.reduce((a, b) => a + b, 0) / durations.length) : 0,
        minDuration: durations.length > 0 ? Math.min(...durations) : 0,
        maxDuration: durations.length > 0 ? Math.max(...durations) : 0,
        memoryImpact: this.calculateMemoryImpact(metrics)
      }
    }
    
    return stats
  }

  getErrorStats() {
    const now = Date.now()
    const oneHour = 60 * 60 * 1000
    const recentErrors = this.metrics.errors.filter(e => now - e.timestamp < oneHour)
    
    const errorsByType = {}
    const errorsBySeverity = {}
    
    recentErrors.forEach(error => {
      errorsByType[error.type] = (errorsByType[error.type] || 0) + 1
      errorsBySeverity[error.severity] = (errorsBySeverity[error.severity] || 0) + 1
    })
    
    return {
      total: this.metrics.errors.length,
      recent: recentErrors.length,
      errorRate: this.calculateErrorRate(),
      byType: errorsByType,
      bySeverity: errorsBySeverity,
      recentErrors: recentErrors.slice(-10)
    }
  }

  getCacheStats() {
    const cacheOps = this.metrics.cache
    const hits = cacheOps.filter(op => op.hit).length
    const total = cacheOps.filter(op => op.operation === 'get').length
    
    return {
      totalOperations: cacheOps.length,
      hitRate: total > 0 ? (hits / total * 100).toFixed(2) + '%' : '0%',
      averageResponseTime: this.calculateAverageResponseTime(cacheOps),
      operationsByType: this.groupBy(cacheOps, 'operation'),
      operationsByBackend: this.groupBy(cacheOps, 'backend')
    }
  }

  getPerformanceReport() {
    return {
      timestamp: Date.now(),
      system: this.getSystemStats(),
      commands: this.getCommandStats(),
      plugins: this.getPluginStats(),
      errors: this.getErrorStats(),
      cache: this.getCacheStats(),
      responseTimeHistogram: Object.fromEntries(this.counters.responseTimeHistogram),
      alerts: {
        active: Array.from(this.alerts.active.values()),
        recent: this.alerts.history.slice(-10)
      }
    }
  }

  // Alert system
  setupAlertSystem() {
    // Define alert rules
    this.alertRules = [
      {
        name: 'high_cpu_usage',
        condition: (metrics) => metrics.cpu?.percent > this.monitoringConfig.alertThresholds.cpu,
        message: (metrics) => `High CPU usage: ${metrics.cpu.percent.toFixed(2)}%`,
        severity: 'high',
        cooldown: 300000 // 5 minutes
      },
      {
        name: 'high_memory_usage',
        condition: (metrics) => metrics.memory?.percentUsed > this.monitoringConfig.alertThresholds.memory,
        message: (metrics) => `High memory usage: ${metrics.memory.percentUsed.toFixed(2)}%`,
        severity: 'high',
        cooldown: 300000
      },
      {
        name: 'slow_response_time',
        condition: () => this.getAverageResponseTime() > this.monitoringConfig.alertThresholds.responseTime,
        message: () => `Slow response time: ${this.getAverageResponseTime()}ms`,
        severity: 'medium',
        cooldown: 600000 // 10 minutes
      },
      {
        name: 'high_error_rate',
        condition: () => this.calculateErrorRate() > this.monitoringConfig.alertThresholds.errorRate,
        message: () => `High error rate: ${this.calculateErrorRate().toFixed(2)}%`,
        severity: 'high',
        cooldown: 300000
      }
    ]
  }

  checkAlerts() {
    const latestMetrics = this.metrics.system[this.metrics.system.length - 1]
    if (!latestMetrics) return
    
    for (const rule of this.alertRules) {
      try {
        if (rule.condition(latestMetrics)) {
          this.triggerAlert(rule, latestMetrics)
        } else {
          this.resolveAlert(rule.name)
        }
      } catch (error) {
        logger.error(`Alert rule ${rule.name} failed:`, error)
      }
    }
  }

  triggerAlert(rule, metrics) {
    const now = Date.now()
    const alertKey = rule.name
    
    // Check cooldown
    const lastAlert = this.alerts.cooldown.get(alertKey)
    if (lastAlert && (now - lastAlert) < rule.cooldown) {
      return
    }
    
    // Check if alert is already active
    if (this.alerts.active.has(alertKey)) {
      return
    }
    
    const alert = {
      name: rule.name,
      message: rule.message(metrics),
      severity: rule.severity,
      timestamp: now,
      metrics: metrics
    }
    
    this.alerts.active.set(alertKey, alert)
    this.alerts.history.push(alert)
    this.alerts.cooldown.set(alertKey, now)
    
    // Trim alert history
    if (this.alerts.history.length > 100) {
      this.alerts.history = this.alerts.history.slice(-100)
    }
    
    logger.warn(`🚨 ALERT: ${alert.message}`, {
      severity: alert.severity,
      rule: rule.name
    })
  }

  resolveAlert(alertName) {
    if (this.alerts.active.has(alertName)) {
      const alert = this.alerts.active.get(alertName)
      alert.resolvedAt = Date.now()
      alert.duration = alert.resolvedAt - alert.timestamp
      
      this.alerts.active.delete(alertName)
      
      logger.info(`✅ ALERT RESOLVED: ${alert.message}`, {
        duration: alert.duration,
        rule: alertName
      })
    }
  }

  // Utility methods
  calculateErrorRate() {
    const now = Date.now()
    const oneHour = 60 * 60 * 1000
    const recentRequests = this.metrics.requests.filter(r => now - r.timestamp < oneHour)
    const recentErrors = recentRequests.filter(r => r.statusCode >= 400)
    
    return recentRequests.length > 0 ? (recentErrors.length / recentRequests.length) * 100 : 0
  }

  calculateSuccessRate() {
    return 100 - this.calculateErrorRate()
  }

  getAverageResponseTime() {
    const now = Date.now()
    const oneHour = 60 * 60 * 1000
    const recentRequests = this.metrics.requests.filter(r => 
      now - r.timestamp < oneHour && r.duration !== undefined
    )
    
    if (recentRequests.length === 0) return 0
    
    const totalDuration = recentRequests.reduce((sum, req) => sum + req.duration, 0)
    return Math.round(totalDuration / recentRequests.length)
  }

  calculateAverageResponseTime(operations) {
    const durations = operations.filter(op => op.duration !== undefined).map(op => op.duration)
    return durations.length > 0 ? Math.round(durations.reduce((a, b) => a + b, 0) / durations.length) : 0
  }

  calculateMemoryImpact(metrics) {
    if (metrics.length < 2) return 0
    
    const memoryUsages = metrics.map(m => m.memoryUsage).filter(m => m !== undefined)
    if (memoryUsages.length < 2) return 0
    
    const avgBefore = memoryUsages.slice(0, Math.floor(memoryUsages.length / 2)).reduce((a, b) => a + b, 0) / Math.floor(memoryUsages.length / 2)
    const avgAfter = memoryUsages.slice(Math.floor(memoryUsages.length / 2)).reduce((a, b) => a + b, 0) / Math.ceil(memoryUsages.length / 2)
    
    return avgAfter - avgBefore
  }

  groupBy(array, key) {
    return array.reduce((groups, item) => {
      const group = item[key]
      groups[group] = (groups[group] || 0) + 1
      return groups
    }, {})
  }

  trimMetrics(type) {
    const maxSize = 1000 // Keep last 1000 entries
    
    if (Array.isArray(this.metrics[type]) && this.metrics[type].length > maxSize) {
      this.metrics[type] = this.metrics[type].slice(-maxSize)
    }
  }

  trimCommandMetrics(command) {
    const maxSize = 100 // Keep last 100 entries per command
    const metrics = this.metrics.commands.get(command)
    
    if (metrics && metrics.length > maxSize) {
      this.metrics.commands.set(command, metrics.slice(-maxSize))
    }
  }

  trimPluginMetrics(plugin) {
    const maxSize = 100 // Keep last 100 entries per plugin
    const metrics = this.metrics.plugins.get(plugin)
    
    if (metrics && metrics.length > maxSize) {
      this.metrics.plugins.set(plugin, metrics.slice(-maxSize))
    }
  }

  setupCleanup() {
    // Cleanup old data periodically
    this.intervals.cleanup = setInterval(() => {
      this.cleanupOldData()
    }, 3600000) // Every hour
    
    // Save metrics periodically
    setInterval(() => {
      this.saveMetrics()
    }, 300000) // Every 5 minutes
  }

  cleanupOldData() {
    const now = Date.now()
    const retention = this.monitoringConfig.retention
    
    // Clean up old metrics
    Object.keys(this.metrics).forEach(type => {
      if (Array.isArray(this.metrics[type])) {
        this.metrics[type] = this.metrics[type].filter(
          metric => now - metric.timestamp < retention
        )
      }
    })
    
    // Clean up old command metrics
    for (const [command, metrics] of this.metrics.commands) {
      const filtered = metrics.filter(metric => now - metric.timestamp < retention)
      if (filtered.length === 0) {
        this.metrics.commands.delete(command)
      } else {
        this.metrics.commands.set(command, filtered)
      }
    }
    
    // Clean up old plugin metrics
    for (const [plugin, metrics] of this.metrics.plugins) {
      const filtered = metrics.filter(metric => now - metric.timestamp < retention)
      if (filtered.length === 0) {
        this.metrics.plugins.delete(plugin)
      } else {
        this.metrics.plugins.set(plugin, filtered)
      }
    }
    
    logger.debug('📊 Performance data cleanup completed')
  }

  async loadHistoricalData() {
    try {
      const cached = await this.cache.get('performance_metrics')
      if (cached) {
        // Restore metrics data
        this.metrics.system = cached.system || []
        this.metrics.errors = cached.errors || []
        this.metrics.requests = cached.requests || []
        this.metrics.cache = cached.cache || []
        this.metrics.python = cached.python || []
        
        // Restore maps
        this.metrics.commands = new Map(cached.commands || [])
        this.metrics.plugins = new Map(cached.plugins || [])
        
        // Restore counters
        this.counters.commandExecutions = new Map(cached.counters?.commandExecutions || [])
        this.counters.pluginExecutions = new Map(cached.counters?.pluginExecutions || [])
        this.counters.errorCounts = new Map(cached.counters?.errorCounts || [])
        this.counters.responseTimeHistogram = new Map(cached.counters?.responseTimeHistogram || [])
        
        logger.info('📊 Loaded historical performance data from cache')
      }
    } catch (error) {
      logger.warn('Failed to load historical performance data:', error.message)
    }
  }

  async saveMetrics() {
    try {
      const data = {
        system: this.metrics.system,
        errors: this.metrics.errors,
        requests: this.metrics.requests,
        cache: this.metrics.cache,
        python: this.metrics.python,
        commands: Array.from(this.metrics.commands.entries()),
        plugins: Array.from(this.metrics.plugins.entries()),
        counters: {
          commandExecutions: Array.from(this.counters.commandExecutions.entries()),
          pluginExecutions: Array.from(this.counters.pluginExecutions.entries()),
          errorCounts: Array.from(this.counters.errorCounts.entries()),
          responseTimeHistogram: Array.from(this.counters.responseTimeHistogram.entries())
        },
        timestamp: Date.now()
      }
      
      await this.cache.set('performance_metrics', data, this.monitoringConfig.retention)
      logger.debug('💾 Performance metrics saved to cache')
    } catch (error) {
      logger.warn('Failed to save performance metrics:', error.message)
    }
  }

  generateId() {
    return `perf_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Performance Monitor...')
    
    // Clear intervals
    Object.values(this.intervals).forEach(interval => {
      if (interval) clearInterval(interval)
    })
    
    // Save final metrics
    await this.saveMetrics()
    
    // Clear data
    Object.keys(this.metrics).forEach(key => {
      if (Array.isArray(this.metrics[key])) {
        this.metrics[key].length = 0
      } else if (this.metrics[key] instanceof Map) {
        this.metrics[key].clear()
      }
    })
    
    Object.values(this.counters).forEach(counter => {
      if (counter instanceof Map) {
        counter.clear()
      }
    })
    
    this.alerts.active.clear()
    this.alerts.history.length = 0
    this.alerts.cooldown.clear()
    
    this.isInitialized = false
    logger.info('✅ Performance Monitor cleanup complete')
  }
}

module.exports = PerformanceMonitor