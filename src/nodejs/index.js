#!/usr/bin/env node

/**
 * JAEGIS - AI Agent Intelligence System
 * Main Entry Point for Node.js Command Processing Engine
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const rateLimit = require('express-rate-limit')
const { createServer } = require('http')
const WebSocket = require('ws')
const cluster = require('cluster')
const os = require('os')

const CommandRouter = require('./core/CommandRouter')
const ConfigManager = require('./core/ConfigManager')
const CacheManager = require('./core/CacheManager')
const PythonBridge = require('./services/PythonBridge')
const MonitoringService = require('./services/MonitoringService')
const logger = require('./utils/logger')

class JAEGISServer {
  constructor() {
    this.app = express()
    this.server = null
    this.wss = null
    this.config = null
    this.commandRouter = null
    this.pythonBridge = null
    this.monitoring = null
    this.cache = null
  }

  async initialize() {
    try {
      logger.info('🚀 Initializing JAEGIS Command Processing Engine...')
      
      // Load configuration
      this.config = await ConfigManager.load()
      logger.info('⚙️ Configuration loaded successfully')
      
      // Initialize cache
      this.cache = new CacheManager(this.config.cache)
      await this.cache.initialize()
      logger.info('💾 Cache system initialized')
      
      // Initialize Python bridge
      this.pythonBridge = new PythonBridge(this.config.python_integration)
      await this.pythonBridge.initialize()
      logger.info('🐍 Python bridge established')
      
      // Initialize command router
      this.commandRouter = new CommandRouter({
        config: this.config,
        cache: this.cache,
        pythonBridge: this.pythonBridge
      })
      await this.commandRouter.initialize()
      logger.info('🎯 Command router initialized')
      
      // Initialize monitoring
      this.monitoring = new MonitoringService(this.config.monitoring)
      await this.monitoring.initialize()
      logger.info('📊 Monitoring service started')
      
      // Setup Express app
      this.setupMiddleware()
      this.setupRoutes()
      this.setupWebSocket()
      
      logger.info('✅ JAEGIS initialization complete!')
      
    } catch (error) {
      logger.error('❌ Failed to initialize JAEGIS:', error)
      process.exit(1)
    }
  }

  setupMiddleware() {
    // Security middleware
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", "'unsafe-inline'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          imgSrc: ["'self'", "data:", "https:"]
        }
      }
    }))

    // CORS configuration
    this.app.use(cors({
      origin: this.config.server.cors.origins,
      credentials: true,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
      allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
    }))

    // Rate limiting
    const limiter = rateLimit({
      windowMs: this.config.server.rate_limiting.window_ms,
      max: this.config.server.rate_limiting.max_requests,
      message: {
        error: 'Too many requests',
        message: 'Please try again later'
      },
      standardHeaders: true,
      legacyHeaders: false
    })
    this.app.use('/api/', limiter)

    // Body parsing
    this.app.use(express.json({ limit: '10mb' }))
    this.app.use(express.urlencoded({ extended: true, limit: '10mb' }))

    // Request logging
    this.app.use((req, res, next) => {
      const start = Date.now()
      res.on('finish', () => {
        const duration = Date.now() - start
        logger.info(`${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`)
        this.monitoring.recordRequest(req.method, req.path, res.statusCode, duration)
      })
      next()
    })
  }

  setupRoutes() {
    // Health check endpoint
    this.app.get('/health', async (req, res) => {
      try {
        const health = await this.getSystemHealth()
        const isHealthy = Object.values(health.services)
          .every(service => service.status === 'healthy')
        
        res.status(isHealthy ? 200 : 503).json(health)
      } catch (error) {
        logger.error('Health check failed:', error)
        res.status(503).json({
          status: 'unhealthy',
          error: error.message,
          timestamp: new Date().toISOString()
        })
      }
    })

    // Main command processing endpoint
    this.app.post('/api/command', async (req, res) => {
      try {
        const { command, parameters = {}, context = {} } = req.body
        
        if (!command) {
          return res.status(400).json({
            success: false,
            error: 'Command is required',
            code: 'MISSING_COMMAND'
          })
        }

        logger.info(`Processing command: ${command}`)
        const startTime = Date.now()
        
        const result = await this.commandRouter.processCommand(command, {
          parameters,
          context,
          requestId: req.headers['x-request-id'] || this.generateRequestId(),
          userAgent: req.headers['user-agent'],
          ip: req.ip
        })

        const processingTime = Date.now() - startTime
        this.monitoring.recordCommandProcessing(command, result.success, processingTime)

        res.json({
          ...result,
          metadata: {
            processingTime,
            requestId: result.requestId,
            timestamp: new Date().toISOString()
          }
        })

      } catch (error) {
        logger.error('Command processing error:', error)
        res.status(500).json({
          success: false,
          error: 'Internal server error',
          code: 'PROCESSING_ERROR',
          message: this.config.system.debug ? error.message : 'An error occurred'
        })
      }
    })

    // Command suggestions endpoint
    this.app.get('/api/commands/suggest', async (req, res) => {
      try {
        const { query, limit = 10 } = req.query
        const suggestions = await this.commandRouter.getSuggestions(query, parseInt(limit))
        
        res.json({
          success: true,
          data: suggestions,
          query,
          count: suggestions.length
        })
      } catch (error) {
        logger.error('Command suggestion error:', error)
        res.status(500).json({
          success: false,
          error: 'Failed to get suggestions'
        })
      }
    })

    // System status endpoint
    this.app.get('/api/status', async (req, res) => {
      try {
        const status = await this.getSystemStatus()
        res.json(status)
      } catch (error) {
        logger.error('Status endpoint error:', error)
        res.status(500).json({
          success: false,
          error: 'Failed to get system status'
        })
      }
    })

    // Configuration endpoint
    this.app.get('/api/config', async (req, res) => {
      try {
        const publicConfig = this.getPublicConfig()
        res.json({
          success: true,
          data: publicConfig
        })
      } catch (error) {
        logger.error('Config endpoint error:', error)
        res.status(500).json({
          success: false,
          error: 'Failed to get configuration'
        })
      }
    })

    // Metrics endpoint (for monitoring)
    this.app.get('/metrics', async (req, res) => {
      try {
        const metrics = await this.monitoring.getMetrics()
        res.set('Content-Type', 'text/plain')
        res.send(metrics)
      } catch (error) {
        logger.error('Metrics endpoint error:', error)
        res.status(500).send('# Error getting metrics')
      }
    })

    // 404 handler
    this.app.use('*', (req, res) => {
      res.status(404).json({
        success: false,
        error: 'Endpoint not found',
        code: 'NOT_FOUND',
        path: req.originalUrl
      })
    })

    // Error handler
    this.app.use((error, req, res, next) => {
      logger.error('Unhandled error:', error)
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        code: 'UNHANDLED_ERROR'
      })
    })
  }

  setupWebSocket() {
    this.server = createServer(this.app)
    this.wss = new WebSocket.Server({ 
      server: this.server,
      path: '/ws'
    })

    this.wss.on('connection', (ws, req) => {
      const clientId = this.generateRequestId()
      logger.info(`WebSocket client connected: ${clientId}`)

      ws.clientId = clientId
      ws.isAlive = true

      ws.on('pong', () => {
        ws.isAlive = true
      })

      ws.on('message', async (message) => {
        try {
          const data = JSON.parse(message)
          
          if (data.type === 'command') {
            const result = await this.commandRouter.processCommand(data.command, {
              parameters: data.parameters || {},
              context: { ...data.context, clientId, websocket: true },
              requestId: data.requestId || this.generateRequestId()
            })

            ws.send(JSON.stringify({
              type: 'command_result',
              requestId: data.requestId,
              ...result
            }))
          } else if (data.type === 'ping') {
            ws.send(JSON.stringify({ type: 'pong', timestamp: Date.now() }))
          }
        } catch (error) {
          logger.error('WebSocket message error:', error)
          ws.send(JSON.stringify({
            type: 'error',
            error: 'Invalid message format'
          }))
        }
      })

      ws.on('close', () => {
        logger.info(`WebSocket client disconnected: ${clientId}`)
      })

      ws.on('error', (error) => {
        logger.error(`WebSocket error for client ${clientId}:`, error)
      })

      // Send welcome message
      ws.send(JSON.stringify({
        type: 'welcome',
        clientId,
        message: 'Connected to JAEGIS Command Processing Engine',
        timestamp: Date.now()
      }))
    })

    // WebSocket heartbeat
    setInterval(() => {
      this.wss.clients.forEach((ws) => {
        if (!ws.isAlive) {
          logger.info(`Terminating inactive WebSocket client: ${ws.clientId}`)
          return ws.terminate()
        }
        
        ws.isAlive = false
        ws.ping()
      })
    }, 30000)
  }

  async getSystemHealth() {
    const pythonHealth = await this.pythonBridge.healthCheck()
    const cacheHealth = await this.cache.healthCheck()
    
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: this.config.system.version,
      services: {
        nodejs: {
          status: 'healthy',
          uptime: process.uptime(),
          memory: process.memoryUsage(),
          cpu: process.cpuUsage()
        },
        python: pythonHealth,
        cache: cacheHealth,
        monitoring: await this.monitoring.healthCheck()
      }
    }
  }

  async getSystemStatus() {
    const health = await this.getSystemHealth()
    const stats = await this.monitoring.getStats()
    
    return {
      success: true,
      data: {
        ...health,
        statistics: stats,
        configuration: {
          environment: this.config.system.environment,
          debug: this.config.system.debug,
          cache_enabled: this.config.cache.enabled,
          python_integration: this.config.python_integration.enabled
        }
      }
    }
  }

  getPublicConfig() {
    return {
      system: {
        name: this.config.system.name,
        version: this.config.system.version,
        environment: this.config.system.environment
      },
      commands: {
        prefix: this.config.commands.prefix,
        aliases: this.config.commands.aliases
      },
      features: {
        websocket: true,
        real_time: true,
        caching: this.config.cache.enabled,
        python_integration: this.config.python_integration.enabled
      }
    }
  }

  generateRequestId() {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  async start() {
    await this.initialize()
    
    const port = this.config.server.port
    const host = this.config.server.host
    
    this.server.listen(port, host, () => {
      logger.info(`🚀 JAEGIS Server running on http://${host}:${port}`)
      logger.info(`📡 WebSocket available at ws://${host}:${port}/ws`)
      logger.info(`📊 Health check: http://${host}:${port}/health`)
      logger.info(`📈 Metrics: http://${host}:${port}/metrics`)
      
      // Notify monitoring service
      this.monitoring.recordServerStart()
    })

    // Graceful shutdown
    process.on('SIGTERM', () => this.shutdown('SIGTERM'))
    process.on('SIGINT', () => this.shutdown('SIGINT'))
  }

  async shutdown(signal) {
    logger.info(`🛑 Received ${signal}, shutting down gracefully...`)
    
    // Close WebSocket connections
    this.wss.clients.forEach(ws => {
      ws.send(JSON.stringify({
        type: 'server_shutdown',
        message: 'Server is shutting down'
      }))
      ws.close()
    })
    
    // Close server
    this.server.close(() => {
      logger.info('✅ HTTP server closed')
    })
    
    // Cleanup services
    await this.pythonBridge.cleanup()
    await this.cache.cleanup()
    await this.monitoring.cleanup()
    
    logger.info('✅ JAEGIS shutdown complete')
    process.exit(0)
  }
}

// Cluster mode for production
if (cluster.isMaster && process.env.NODE_ENV === 'production') {
  const numCPUs = os.cpus().length
  logger.info(`🚀 Master ${process.pid} starting ${numCPUs} workers`)
  
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork()
  }
  
  cluster.on('exit', (worker, code, signal) => {
    logger.warn(`Worker ${worker.process.pid} died (${signal || code}). Restarting...`)
    cluster.fork()
  })
} else {
  // Single process mode or worker
  const server = new JAEGISServer()
  server.start().catch(error => {
    logger.error('Failed to start JAEGIS server:', error)
    process.exit(1)
  })
}

module.exports = JAEGISServer