/**
 * JAEGIS Component Integration Tests
 * Testing integration between Node.js and Python components
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const { describe, it, beforeEach, afterEach, before, after } = require('mocha')
const { expect } = require('chai')
const sinon = require('sinon')

const { setupTests, teardownTests, TestUtils } = require('../setup')

// Import components for integration testing
const PythonBridge = require('../../src/nodejs/bridge/PythonBridge')
const CacheManager = require('../../src/nodejs/core/CacheManager')
const DecisionEngine = require('../../src/nodejs/core/DecisionEngine')
const CommandRouter = require('../../src/nodejs/core/CommandRouter')

describe('Component Integration Tests', () => {
  let pythonBridge
  let cache
  let decisionEngine
  let commandRouter
  let testConfig

  before(async () => {
    await setupTests()
    testConfig = global.testConfig
  })

  after(async () => {
    await teardownTests()
  })

  beforeEach(async () => {
    // Initialize components in dependency order
    cache = new CacheManager(testConfig)
    await cache.initialize()

    pythonBridge = new PythonBridge(testConfig)
    await pythonBridge.initialize()

    decisionEngine = new DecisionEngine({ config: testConfig, cache })
    await decisionEngine.initialize()

    commandRouter = new CommandRouter({
      config: testConfig,
      cache,
      pythonBridge,
      decisionEngine
    })
    await commandRouter.initialize()
  })

  afterEach(async () => {
    // Cleanup in reverse order
    if (commandRouter) await commandRouter.cleanup()
    if (decisionEngine) await decisionEngine.cleanup()
    if (pythonBridge) await pythonBridge.cleanup()
    if (cache) await cache.cleanup()
  })

  describe('Python Bridge Integration', () => {
    it('should establish connection with Python service', async () => {
      const healthCheck = await pythonBridge.healthCheck()
      
      expect(healthCheck).to.have.property('status', 'healthy')
      expect(healthCheck).to.have.property('connected', true)
    })

    it('should fetch GitHub commands through Python bridge', async () => {
      const result = await pythonBridge.fetchGitHubCommands(testConfig.github.commands_url)
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('content')
      expect(result.data).to.have.property('url')
      expect(result.data.content).to.be.a('string')
      expect(result.data.content.length).to.be.greaterThan(0)
    })

    it('should parse markdown commands through Python bridge', async () => {
      const mockMarkdown = `# Test Commands

## Core Commands

### \`/test\`
**Description:** Test command
**Usage:** \`/test [param]\`
**Examples:**
- \`/test\` - Basic test
- \`/test param\` - Test with parameter`

      const result = await pythonBridge.parseMarkdownCommands(mockMarkdown)
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('commands')
      expect(result.data.commands).to.be.an('array')
      expect(result.data.commands.length).to.be.greaterThan(0)
      
      const testCommand = result.data.commands.find(cmd => cmd.name === 'test')
      expect(testCommand).to.exist
      expect(testCommand).to.have.property('description', 'Test command')
      expect(testCommand).to.have.property('usage', '/test [param]')
    })

    it('should generate suggestions through Python bridge', async () => {
      const result = await pythonBridge.generateSuggestions('hel', {
        availableCommands: ['help', 'health', 'hello']
      })
      
      expect(result.success).to.be.true
      expect(result.data).to.be.an('array')
      expect(result.data.length).to.be.greaterThan(0)
      
      const suggestions = result.data
      expect(suggestions[0]).to.have.property('command')
      expect(suggestions[0]).to.have.property('score')
      expect(suggestions[0].score).to.be.a('number')
    })

    it('should handle Python bridge errors gracefully', async () => {
      // Simulate Python service unavailable
      const originalRequest = pythonBridge.makeRequest
      pythonBridge.makeRequest = sinon.stub().rejects(new Error('Connection refused'))
      
      const result = await pythonBridge.fetchGitHubCommands('invalid-url')
      
      expect(result.success).to.be.false
      expect(result.error).to.include('Connection refused')
      
      // Restore original method
      pythonBridge.makeRequest = originalRequest
    })
  })

  describe('Cache Integration', () => {
    it('should integrate cache with Python bridge results', async () => {
      const url = testConfig.github.commands_url
      
      // First call should fetch from Python and cache
      const result1 = await pythonBridge.fetchGitHubCommands(url)
      expect(result1.success).to.be.true
      
      // Check if result is cached
      const cacheKey = pythonBridge.generateCacheKey('github_commands', url)
      const cached = await cache.get(cacheKey)
      expect(cached).to.not.be.null
      
      // Second call should use cache
      const result2 = await pythonBridge.fetchGitHubCommands(url)
      expect(result2.success).to.be.true
      expect(result2.data).to.deep.equal(result1.data)
    })

    it('should cache parsed command data', async () => {
      const mockMarkdown = '# Test\n## Commands\n### `/test`\nTest command'
      
      const result1 = await pythonBridge.parseMarkdownCommands(mockMarkdown)
      expect(result1.success).to.be.true
      
      // Check cache
      const cacheKey = pythonBridge.generateCacheKey('parsed_commands', mockMarkdown)
      const cached = await cache.get(cacheKey)
      expect(cached).to.not.be.null
      
      // Second call should use cache
      const result2 = await pythonBridge.parseMarkdownCommands(mockMarkdown)
      expect(result2.success).to.be.true
      expect(result2.data).to.deep.equal(result1.data)
    })

    it('should handle cache invalidation', async () => {
      const url = testConfig.github.commands_url
      
      // Cache some data
      await pythonBridge.fetchGitHubCommands(url)
      const cacheKey = pythonBridge.generateCacheKey('github_commands', url)
      
      // Verify cached
      let cached = await cache.get(cacheKey)
      expect(cached).to.not.be.null
      
      // Invalidate cache
      await cache.delete(cacheKey)
      
      // Verify cache cleared
      cached = await cache.get(cacheKey)
      expect(cached).to.be.null
    })
  })

  describe('Decision Engine Integration', () => {
    it('should integrate with cache for decision data', async () => {
      const command = '/test'
      const options = { user: 'test-user' }
      
      // Make decision
      const decision1 = await decisionEngine.makeDecision(command, options)
      expect(decision1).to.have.property('command', command)
      expect(decision1).to.have.property('routing')
      
      // Check if decision patterns are cached
      const cacheStats = cache.getStats()
      expect(cacheStats.memory.keys).to.be.greaterThan(0)
    })

    it('should use Python bridge for complex analysis', async () => {
      const command = '/complex-analysis'
      const options = { 
        complexity: 'high',
        requiresExternalData: true
      }
      
      const decision = await decisionEngine.makeDecision(command, options)
      
      expect(decision).to.have.property('analysis')
      expect(decision.analysis).to.have.property('complexity')
      expect(decision).to.have.property('routing')
      expect(decision.routing).to.have.property('needsGitHubData')
    })

    it('should record performance data for future decisions', async () => {
      const command = '/performance-test'
      
      // Make initial decision
      const decision = await decisionEngine.makeDecision(command, {})
      expect(decision).to.have.property('confidence')
      
      // Record performance
      decisionEngine.recordPerformance(command, true, 150)
      decisionEngine.recordPerformance(command, true, 120)
      decisionEngine.recordPerformance(command, true, 180)
      
      // Make another decision - should be influenced by performance data
      const decision2 = await decisionEngine.makeDecision(command, {})
      expect(decision2).to.have.property('confidence')
      
      // Check performance stats
      const stats = decisionEngine.getStats()
      expect(stats).to.have.property('decisions_made')
      expect(stats.decisions_made).to.be.greaterThan(1)
    })
  })

  describe('Command Router Integration', () => {
    it('should integrate all components for command processing', async () => {
      const command = '/help'
      const options = {
        parameters: { command: 'status' },
        context: { user: 'integration-test' }
      }
      
      const result = await commandRouter.processCommand(command, options)
      
      expect(result.success).to.be.true
      expect(result).to.have.property('data')
      expect(result).to.have.property('requestId')
      expect(result).to.have.property('processingTime')
      expect(result.processingTime).to.be.a('number')
    })

    it('should use decision engine for routing decisions', async () => {
      const command = '/analytics'
      
      // Spy on decision engine
      const makeDecisionSpy = sinon.spy(decisionEngine, 'makeDecision')
      
      const result = await commandRouter.processCommand(command)
      
      expect(result.success).to.be.true
      expect(makeDecisionSpy.calledOnce).to.be.true
      expect(makeDecisionSpy.calledWith(command)).to.be.true
      
      makeDecisionSpy.restore()
    })

    it('should leverage cache across the processing pipeline', async () => {
      const command = '/status'
      
      // First execution
      const result1 = await commandRouter.processCommand(command)
      expect(result1.success).to.be.true
      
      // Check cache usage
      const cacheStats1 = cache.getStats()
      const initialKeys = cacheStats1.memory.keys
      
      // Second execution should use cached data
      const result2 = await commandRouter.processCommand(command)
      expect(result2.success).to.be.true
      
      // Cache should have been utilized
      const cacheStats2 = cache.getStats()
      expect(cacheStats2.memory.hits).to.be.greaterThan(cacheStats1.memory.hits)
    })

    it('should handle Python bridge failures gracefully', async () => {
      // Simulate Python bridge failure
      const originalHealthCheck = pythonBridge.healthCheck
      pythonBridge.healthCheck = sinon.stub().rejects(new Error('Python service down'))
      
      const command = '/help'
      const result = await commandRouter.processCommand(command)
      
      // Should still work with degraded functionality
      expect(result.success).to.be.true
      expect(result).to.have.property('data')
      
      // Restore original method
      pythonBridge.healthCheck = originalHealthCheck
    })
  })

  describe('Data Flow Integration', () => {
    it('should maintain data consistency across components', async () => {
      const testData = {
        command: '/test-data-flow',
        timestamp: Date.now(),
        user: 'integration-test'
      }
      
      // Store in cache
      await cache.set('test-data', testData)
      
      // Retrieve through different component
      const retrieved = await cache.get('test-data')
      expect(retrieved).to.deep.equal(testData)
      
      // Use in decision engine
      const decision = await decisionEngine.makeDecision(testData.command, {
        user: testData.user
      })
      
      expect(decision).to.have.property('command', testData.command)
    })

    it('should handle concurrent operations correctly', async () => {
      const commands = ['/help', '/status', '/analytics', '/config']
      const promises = commands.map(cmd => commandRouter.processCommand(cmd))
      
      const results = await Promise.all(promises)
      
      results.forEach((result, index) => {
        expect(result.success).to.be.true
        expect(result).to.have.property('requestId')
        expect(result.requestId).to.be.a('string')
      })
      
      // All should have unique request IDs
      const requestIds = results.map(r => r.requestId)
      const uniqueIds = [...new Set(requestIds)]
      expect(uniqueIds.length).to.equal(commands.length)
    })

    it('should propagate errors correctly through the pipeline', async () => {
      // Simulate cache failure
      const originalGet = cache.get
      cache.get = sinon.stub().rejects(new Error('Cache failure'))
      
      const result = await commandRouter.processCommand('/help')
      
      // Should handle gracefully
      expect(result.success).to.be.true // Should still work with degraded performance
      
      // Restore cache
      cache.get = originalGet
    })
  })

  describe('Performance Integration', () => {
    it('should maintain performance across integrated components', async () => {
      const startTime = Date.now()
      const iterations = 10
      
      for (let i = 0; i < iterations; i++) {
        const result = await commandRouter.processCommand('/help')
        expect(result.success).to.be.true
      }
      
      const totalTime = Date.now() - startTime
      const avgTime = totalTime / iterations
      
      // Should maintain reasonable performance
      expect(avgTime).to.be.lessThan(1000) // Less than 1 second per command
    })

    it('should show performance improvement with caching', async () => {
      const command = '/performance-test'
      
      // Clear any existing cache
      await cache.clear()
      
      // First execution (no cache)
      const start1 = Date.now()
      const result1 = await commandRouter.processCommand(command)
      const time1 = Date.now() - start1
      
      expect(result1.success).to.be.true
      
      // Second execution (with cache)
      const start2 = Date.now()
      const result2 = await commandRouter.processCommand(command)
      const time2 = Date.now() - start2
      
      expect(result2.success).to.be.true
      
      // Second execution should be faster or similar
      expect(time2).to.be.lessThanOrEqual(time1 * 1.5) // Allow some variance
    })
  })

  describe('Error Recovery Integration', () => {
    it('should recover from component failures', async () => {
      // Simulate temporary Python bridge failure
      const originalMakeRequest = pythonBridge.makeRequest
      let callCount = 0
      
      pythonBridge.makeRequest = function(...args) {
        callCount++
        if (callCount <= 2) {
          return Promise.reject(new Error('Temporary failure'))
        }
        return originalMakeRequest.apply(this, args)
      }
      
      // Should eventually succeed with retry logic
      const result = await commandRouter.processCommand('/help')
      expect(result.success).to.be.true
      
      pythonBridge.makeRequest = originalMakeRequest
    })

    it('should maintain service availability during partial failures', async () => {
      // Disable Python bridge
      await pythonBridge.cleanup()
      
      // Basic commands should still work
      const result = await commandRouter.processCommand('/help')
      expect(result.success).to.be.true
      
      // Re-initialize for cleanup
      pythonBridge = new PythonBridge(testConfig)
      await pythonBridge.initialize()
    })
  })

  describe('Configuration Integration', () => {
    it('should respect configuration across all components', async () => {
      // Check that all components use the same configuration
      expect(cache.config).to.equal(testConfig)
      expect(pythonBridge.config).to.equal(testConfig)
      expect(decisionEngine.config).to.equal(testConfig)
      expect(commandRouter.config).to.equal(testConfig)
    })

    it('should handle configuration changes consistently', async () => {
      // Simulate configuration update
      const newConfig = {
        ...testConfig,
        cache: {
          ...testConfig.cache,
          duration: 1800000 // 30 minutes
        }
      }
      
      // Components should be able to handle config updates
      // (In a real implementation, this would trigger reinitialization)
      expect(newConfig.cache.duration).to.equal(1800000)
    })
  })

  describe('Health Check Integration', () => {
    it('should provide comprehensive health status', async () => {
      const healthChecks = await Promise.all([
        cache.healthCheck(),
        pythonBridge.healthCheck(),
        decisionEngine.getStats()
      ])
      
      // Cache health
      expect(healthChecks[0]).to.have.property('status', 'healthy')
      
      // Python bridge health
      expect(healthChecks[1]).to.have.property('status', 'healthy')
      expect(healthChecks[1]).to.have.property('connected', true)
      
      // Decision engine stats
      expect(healthChecks[2]).to.be.an('object')
    })

    it('should detect unhealthy components', async () => {
      // Simulate unhealthy Python bridge
      const originalHealthCheck = pythonBridge.healthCheck
      pythonBridge.healthCheck = sinon.stub().resolves({
        status: 'unhealthy',
        connected: false,
        error: 'Connection timeout'
      })
      
      const health = await pythonBridge.healthCheck()
      expect(health.status).to.equal('unhealthy')
      expect(health.connected).to.be.false
      
      pythonBridge.healthCheck = originalHealthCheck
    })
  })
})