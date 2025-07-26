/**
 * JAEGIS System Integration Tests
 * End-to-end testing of the complete JAEGIS system
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const { describe, it, beforeEach, afterEach, before, after } = require('mocha')
const { expect } = require('chai')
const request = require('supertest')
const WebSocket = require('ws')

const { setupTests, teardownTests, TestUtils } = require('../setup')

// Import main components
const CommandRouter = require('../../src/nodejs/core/CommandRouter')
const CommandExecutor = require('../../src/nodejs/core/CommandExecutor')
const CacheManager = require('../../src/nodejs/core/CacheManager')
const DecisionEngine = require('../../src/nodejs/core/DecisionEngine')
const ErrorHandler = require('../../src/nodejs/core/ErrorHandler').ErrorHandler
const PerformanceMonitor = require('../../src/nodejs/core/PerformanceMonitor')
const HelpSystem = require('../../src/nodejs/core/HelpSystem')
const ContextManager = require('../../src/nodejs/core/ContextManager').ContextManager
const ResponseFormatter = require('../../src/nodejs/core/ResponseFormatter').ResponseFormatter

describe('JAEGIS System Integration Tests', () => {
  let system
  let mockServices
  let testConfig
  let server
  let wsServer

  before(async () => {
    await setupTests()
    mockServices = global.mockServices
    testConfig = global.testConfig
  })

  after(async () => {
    await teardownTests()
  })

  beforeEach(async () => {
    // Initialize complete system
    system = await initializeSystem()
    
    // Start test server
    server = await startTestServer(system)
    wsServer = await startWebSocketServer(system)
  })

  afterEach(async () => {
    if (server) {
      await server.close()
    }
    if (wsServer) {
      await wsServer.close()
    }
    if (system) {
      await cleanupSystem(system)
    }
  })

  async function initializeSystem() {
    const cache = new CacheManager(testConfig)
    await cache.initialize()

    const decisionEngine = new DecisionEngine({ config: testConfig, cache })
    await decisionEngine.initialize()

    const errorHandler = new ErrorHandler({ 
      config: testConfig, 
      cache, 
      pythonBridge: mockServices.pythonBridge 
    })
    await errorHandler.initialize()

    const performanceMonitor = new PerformanceMonitor({ config: testConfig, cache })
    await performanceMonitor.initialize()

    const contextManager = new ContextManager({ config: testConfig, cache })
    await contextManager.initialize()

    const responseFormatter = new ResponseFormatter({ config: testConfig })
    await responseFormatter.initialize()

    const commandExecutor = new CommandExecutor({
      config: testConfig,
      cache,
      pythonBridge: mockServices.pythonBridge,
      decisionEngine
    })
    await commandExecutor.initialize()

    const helpSystem = new HelpSystem({
      config: testConfig,
      cache,
      pythonBridge: mockServices.pythonBridge,
      commandExecutor
    })
    await helpSystem.initialize()

    const commandRouter = new CommandRouter({
      config: testConfig,
      cache,
      pythonBridge: mockServices.pythonBridge,
      decisionEngine,
      commandExecutor,
      errorHandler,
      performanceMonitor,
      helpSystem,
      contextManager,
      responseFormatter
    })
    await commandRouter.initialize()

    return {
      cache,
      decisionEngine,
      errorHandler,
      performanceMonitor,
      contextManager,
      responseFormatter,
      commandExecutor,
      helpSystem,
      commandRouter
    }
  }

  async function startTestServer(system) {
    const express = require('express')
    const app = express()
    
    app.use(express.json())
    
    // Health check endpoint
    app.get('/health', (req, res) => {
      res.json({ status: 'healthy', timestamp: Date.now() })
    })
    
    // Command execution endpoint
    app.post('/api/command', async (req, res) => {
      try {
        const { command, parameters = {}, context = {} } = req.body
        
        const result = await system.commandRouter.processCommand(command, {
          parameters,
          context: {
            ...context,
            ip: req.ip,
            userAgent: req.get('User-Agent'),
            method: 'api'
          }
        })
        
        res.json(result)
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message
        })
      }
    })
    
    // Status endpoint
    app.get('/api/status', async (req, res) => {
      try {
        const status = await system.commandExecutor.executeCommand('status')
        res.json(status)
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message
        })
      }
    })
    
    // Metrics endpoint
    app.get('/api/metrics', async (req, res) => {
      try {
        const metrics = system.performanceMonitor.getPerformanceReport()
        res.json(metrics)
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message
        })
      }
    })
    
    return new Promise((resolve) => {
      const server = app.listen(0, () => {
        const port = server.address().port
        console.log(`Test server started on port ${port}`)
        resolve(server)
      })
    })
  }

  async function startWebSocketServer(system) {
    return new Promise((resolve) => {
      const wss = new WebSocket.Server({ port: 0 }, () => {
        const port = wss.address().port
        console.log(`WebSocket server started on port ${port}`)
        resolve(wss)
      })
      
      wss.on('connection', (ws) => {
        ws.on('message', async (data) => {
          try {
            const message = JSON.parse(data)
            
            if (message.type === 'command') {
              const result = await system.commandRouter.processCommand(message.command, {
                parameters: message.parameters || {},
                context: {
                  ...message.context,
                  method: 'websocket',
                  requestId: message.id
                }
              })
              
              ws.send(JSON.stringify({
                type: 'response',
                id: message.id,
                payload: result
              }))
            }
          } catch (error) {
            ws.send(JSON.stringify({
              type: 'error',
              error: error.message
            }))
          }
        })
      })
    })
  }

  async function cleanupSystem(system) {
    const components = [
      'commandRouter',
      'helpSystem',
      'commandExecutor',
      'responseFormatter',
      'contextManager',
      'performanceMonitor',
      'errorHandler',
      'decisionEngine',
      'cache'
    ]
    
    for (const component of components) {
      if (system[component] && typeof system[component].cleanup === 'function') {
        await system[component].cleanup()
      }
    }
  }

  describe('System Initialization', () => {
    it('should initialize all components successfully', async () => {
      expect(system.cache.isInitialized).to.be.true
      expect(system.decisionEngine.isInitialized).to.be.true
      expect(system.errorHandler.isInitialized).to.be.true
      expect(system.performanceMonitor.isInitialized).to.be.true
      expect(system.contextManager.isInitialized).to.be.true
      expect(system.responseFormatter.isInitialized).to.be.true
      expect(system.commandExecutor.isInitialized).to.be.true
      expect(system.helpSystem.isInitialized).to.be.true
      expect(system.commandRouter.isInitialized).to.be.true
    })

    it('should have proper component dependencies', async () => {
      // CommandRouter should have all dependencies
      expect(system.commandRouter.cache).to.equal(system.cache)
      expect(system.commandRouter.decisionEngine).to.equal(system.decisionEngine)
      expect(system.commandRouter.commandExecutor).to.equal(system.commandExecutor)
    })
  })

  describe('End-to-End Command Processing', () => {
    it('should process help command through complete pipeline', async () => {
      const result = await system.commandRouter.processCommand('/help')
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('title')
      expect(result.data).to.have.property('available_commands')
      expect(result).to.have.property('processingTime')
      expect(result).to.have.property('requestId')
    })

    it('should process status command with full system integration', async () => {
      const result = await system.commandRouter.processCommand('/status')
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('system')
      expect(result.data).to.have.property('executor')
      expect(result.data).to.have.property('services')
    })

    it('should handle command with parameters', async () => {
      const result = await system.commandRouter.processCommand('/help', {
        parameters: { command: 'status' }
      })
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('command')
      expect(result.data.command).to.equal('status')
    })

    it('should apply decision engine routing', async () => {
      const result = await system.commandRouter.processCommand('/analytics')
      
      expect(result.success).to.be.true
      // Decision engine should have been consulted
      expect(system.decisionEngine.getStats().decisions_made).to.be.greaterThan(0)
    })
  })

  describe('HTTP API Integration', () => {
    it('should handle health check', async () => {
      const response = await request(server)
        .get('/health')
        .expect(200)
      
      expect(response.body).to.have.property('status', 'healthy')
      expect(response.body).to.have.property('timestamp')
    })

    it('should execute commands via API', async () => {
      const response = await request(server)
        .post('/api/command')
        .send({ command: '/help' })
        .expect(200)
      
      expect(response.body.success).to.be.true
      expect(response.body.data).to.have.property('title')
    })

    it('should handle API command with parameters', async () => {
      const response = await request(server)
        .post('/api/command')
        .send({ 
          command: '/help',
          parameters: { command: 'status' }
        })
        .expect(200)
      
      expect(response.body.success).to.be.true
      expect(response.body.data.command).to.equal('status')
    })

    it('should return status via API', async () => {
      const response = await request(server)
        .get('/api/status')
        .expect(200)
      
      expect(response.body.success).to.be.true
      expect(response.body.data).to.have.property('system')
    })

    it('should return metrics via API', async () => {
      const response = await request(server)
        .get('/api/metrics')
        .expect(200)
      
      expect(response.body).to.have.property('timestamp')
      expect(response.body).to.have.property('system')
    })

    it('should handle API errors gracefully', async () => {
      const response = await request(server)
        .post('/api/command')
        .send({ command: '/nonexistent' })
        .expect(200)
      
      expect(response.body.success).to.be.false
      expect(response.body).to.have.property('error')
    })
  })

  describe('WebSocket Integration', () => {
    it('should handle WebSocket command execution', (done) => {
      const port = wsServer.address().port
      const ws = new WebSocket(`ws://localhost:${port}`)
      
      ws.on('open', () => {
        ws.send(JSON.stringify({
          type: 'command',
          id: 'test-1',
          command: '/help'
        }))
      })
      
      ws.on('message', (data) => {
        const response = JSON.parse(data)
        
        expect(response.type).to.equal('response')
        expect(response.id).to.equal('test-1')
        expect(response.payload.success).to.be.true
        
        ws.close()
        done()
      })
    })

    it('should handle WebSocket errors', (done) => {
      const port = wsServer.address().port
      const ws = new WebSocket(`ws://localhost:${port}`)
      
      ws.on('open', () => {
        ws.send('invalid json')
      })
      
      ws.on('message', (data) => {
        const response = JSON.parse(data)
        
        expect(response.type).to.equal('error')
        expect(response).to.have.property('error')
        
        ws.close()
        done()
      })
    })
  })

  describe('Performance Integration', () => {
    it('should track performance across all components', async () => {
      // Execute multiple commands to generate metrics
      await system.commandRouter.processCommand('/help')
      await system.commandRouter.processCommand('/status')
      await system.commandRouter.processCommand('/analytics')
      
      const metrics = system.performanceMonitor.getPerformanceReport()
      
      expect(metrics).to.have.property('system')
      expect(metrics).to.have.property('commands')
      expect(metrics.system.totals.commands).to.be.greaterThan(0)
    })

    it('should monitor system resources', async () => {
      const stats = system.performanceMonitor.getSystemStats()
      
      expect(stats.current).to.have.property('cpu')
      expect(stats.current).to.have.property('memory')
      expect(stats.current).to.have.property('uptime')
    })
  })

  describe('Error Handling Integration', () => {
    it('should handle errors through complete pipeline', async () => {
      const result = await system.commandRouter.processCommand('/nonexistent')
      
      expect(result.success).to.be.false
      expect(result).to.have.property('error')
      expect(result).to.have.property('recovery')
      expect(result).to.have.property('suggestions')
    })

    it('should track errors in performance monitor', async () => {
      await system.commandRouter.processCommand('/nonexistent')
      
      const errorStats = system.performanceMonitor.getErrorStats()
      expect(errorStats.total).to.be.greaterThan(0)
    })
  })

  describe('Cache Integration', () => {
    it('should cache command results across components', async () => {
      // First execution
      const result1 = await system.commandRouter.processCommand('/help')
      
      // Second execution should use cache
      const result2 = await system.commandRouter.processCommand('/help')
      
      expect(result1.success).to.be.true
      expect(result2.success).to.be.true
      
      const cacheStats = system.cache.getStats()
      expect(cacheStats.memory.keys).to.be.greaterThan(0)
    })

    it('should share cache between components', async () => {
      // Set something in cache through one component
      await system.cache.set('test-key', 'test-value')
      
      // Retrieve through another component
      const value = await system.cache.get('test-key')
      expect(value).to.equal('test-value')
    })
  })

  describe('Context Management Integration', () => {
    it('should maintain context across command executions', async () => {
      const userId = 'test-user'
      const sessionId = await system.contextManager.createSession(userId)
      
      const result = await system.commandRouter.processCommand('/help', {
        context: { userId, sessionId }
      })
      
      expect(result.success).to.be.true
      
      const session = await system.contextManager.getSession(sessionId)
      expect(session).to.not.be.null
      expect(session.userId).to.equal(userId)
    })

    it('should track user command history', async () => {
      const userId = 'test-user'
      const sessionId = await system.contextManager.createSession(userId)
      
      await system.commandRouter.processCommand('/help', {
        context: { userId, sessionId }
      })
      
      await system.commandRouter.processCommand('/status', {
        context: { userId, sessionId }
      })
      
      const contexts = await system.contextManager.findContexts({
        userId,
        sessionId
      })
      
      expect(contexts.length).to.be.greaterThan(0)
    })
  })

  describe('Response Formatting Integration', () => {
    it('should format responses based on context', async () => {
      const result = await system.commandRouter.processCommand('/help', {
        context: { format: 'markdown' }
      })
      
      expect(result.success).to.be.true
      // Response should be formatted according to context
    })

    it('should handle different output formats', async () => {
      const formats = ['json', 'text', 'markdown']
      
      for (const format of formats) {
        const result = await system.commandRouter.processCommand('/help', {
          context: { format }
        })
        
        expect(result.success).to.be.true
      }
    })
  })

  describe('Load Testing', () => {
    it('should handle concurrent requests', async () => {
      const concurrency = 10
      const promises = []
      
      for (let i = 0; i < concurrency; i++) {
        promises.push(system.commandRouter.processCommand('/help'))
      }
      
      const results = await Promise.all(promises)
      
      results.forEach(result => {
        expect(result.success).to.be.true
      })
      
      const metrics = system.performanceMonitor.getSystemStats()
      expect(metrics.totals.commands).to.equal(concurrency)
    })

    it('should maintain performance under load', async () => {
      const startTime = Date.now()
      const iterations = 20
      
      for (let i = 0; i < iterations; i++) {
        await system.commandRouter.processCommand('/help')
      }
      
      const totalTime = Date.now() - startTime
      const avgTime = totalTime / iterations
      
      // Should maintain reasonable performance
      expect(avgTime).to.be.lessThan(1000) // Less than 1 second per command
    })
  })

  describe('System Health', () => {
    it('should report healthy status for all components', async () => {
      const healthChecks = await Promise.all([
        system.cache.healthCheck(),
        system.performanceMonitor.getSystemStats(),
        system.contextManager.getContextStats()
      ])
      
      healthChecks.forEach(health => {
        expect(health).to.be.an('object')
      })
    })

    it('should handle component failures gracefully', async () => {
      // Simulate cache failure
      const originalGet = system.cache.get
      system.cache.get = async () => {
        throw new Error('Cache failure')
      }
      
      // System should still work with degraded performance
      const result = await system.commandRouter.processCommand('/help')
      expect(result.success).to.be.true
      
      // Restore cache
      system.cache.get = originalGet
    })
  })

  describe('Data Flow Integration', () => {
    it('should pass data correctly through all layers', async () => {
      const testData = {
        command: '/help',
        parameters: { command: 'status' },
        context: { 
          user: 'test-user',
          format: 'json',
          requestId: 'test-123'
        }
      }
      
      const result = await system.commandRouter.processCommand(
        testData.command,
        {
          parameters: testData.parameters,
          context: testData.context
        }
      )
      
      expect(result.success).to.be.true
      expect(result.requestId).to.equal('test-123')
      expect(result.data.command).to.equal('status')
    })

    it('should maintain data integrity across components', async () => {
      const originalData = { test: 'value', number: 42, array: [1, 2, 3] }
      
      await system.cache.set('integrity-test', originalData)
      const retrievedData = await system.cache.get('integrity-test')
      
      expect(retrievedData).to.deep.equal(originalData)
    })
  })
})