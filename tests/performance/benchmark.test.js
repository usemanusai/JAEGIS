/**
 * JAEGIS Performance Benchmark Tests
 * Comprehensive performance testing and benchmarking suite
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const { describe, it, beforeEach, afterEach, before, after } = require('mocha')
const { expect } = require('chai')
const { performance } = require('perf_hooks')

const { setupTests, teardownTests, TestUtils } = require('../setup')

// Import components for benchmarking
const CommandRouter = require('../../src/nodejs/core/CommandRouter')
const CommandExecutor = require('../../src/nodejs/core/CommandExecutor')
const CacheManager = require('../../src/nodejs/core/CacheManager')
const DecisionEngine = require('../../src/nodejs/core/DecisionEngine')
const PerformanceMonitor = require('../../src/nodejs/core/PerformanceMonitor')

// Performance thresholds (in milliseconds)
const PERFORMANCE_THRESHOLDS = {
  command_execution: {
    simple: 100,    // Simple commands like /help, /status
    medium: 500,    // Medium complexity commands
    complex: 2000   // Complex commands with external calls
  },
  cache_operations: {
    get: 10,
    set: 20,
    delete: 15
  },
  decision_making: 50,
  system_startup: 5000,
  concurrent_load: {
    '10_users': 1000,
    '50_users': 3000,
    '100_users': 5000
  }
}

describe('JAEGIS Performance Benchmarks', () => {
  let system
  let mockServices
  let testConfig

  before(async () => {
    await setupTests()
    mockServices = global.mockServices
    testConfig = global.testConfig
  })

  after(async () => {
    await teardownTests()
  })

  beforeEach(async () => {
    system = await initializeSystemForBenchmarks()
  })

  afterEach(async () => {
    if (system) {
      await cleanupSystem(system)
    }
  })

  async function initializeSystemForBenchmarks() {
    const cache = new CacheManager(testConfig)
    await cache.initialize()

    const decisionEngine = new DecisionEngine({ config: testConfig, cache })
    await decisionEngine.initialize()

    const performanceMonitor = new PerformanceMonitor({ config: testConfig, cache })
    await performanceMonitor.initialize()

    const commandExecutor = new CommandExecutor({
      config: testConfig,
      cache,
      pythonBridge: mockServices.pythonBridge,
      decisionEngine
    })
    await commandExecutor.initialize()

    const commandRouter = new CommandRouter({
      config: testConfig,
      cache,
      pythonBridge: mockServices.pythonBridge,
      decisionEngine,
      commandExecutor,
      performanceMonitor
    })
    await commandRouter.initialize()

    return {
      cache,
      decisionEngine,
      performanceMonitor,
      commandExecutor,
      commandRouter
    }
  }

  async function cleanupSystem(system) {
    const components = ['commandRouter', 'commandExecutor', 'performanceMonitor', 'decisionEngine', 'cache']
    
    for (const component of components) {
      if (system[component] && typeof system[component].cleanup === 'function') {
        await system[component].cleanup()
      }
    }
  }

  describe('System Startup Performance', () => {
    it('should initialize complete system within threshold', async () => {
      const startTime = performance.now()
      
      const testSystem = await initializeSystemForBenchmarks()
      
      const initTime = performance.now() - startTime
      
      console.log(`System initialization time: ${initTime.toFixed(2)}ms`)
      expect(initTime).to.be.lessThan(PERFORMANCE_THRESHOLDS.system_startup)
      
      await cleanupSystem(testSystem)
    })

    it('should initialize components in parallel efficiently', async () => {
      const componentTimes = {}
      
      // Measure individual component initialization
      const cache = new CacheManager(testConfig)
      const cacheStart = performance.now()
      await cache.initialize()
      componentTimes.cache = performance.now() - cacheStart

      const decisionEngine = new DecisionEngine({ config: testConfig, cache })
      const decisionStart = performance.now()
      await decisionEngine.initialize()
      componentTimes.decisionEngine = performance.now() - decisionStart

      const performanceMonitor = new PerformanceMonitor({ config: testConfig, cache })
      const monitorStart = performance.now()
      await performanceMonitor.initialize()
      componentTimes.performanceMonitor = performance.now() - monitorStart

      console.log('Component initialization times:', componentTimes)
      
      // Each component should initialize quickly
      Object.values(componentTimes).forEach(time => {
        expect(time).to.be.lessThan(1000) // 1 second max per component
      })

      await cache.cleanup()
      await decisionEngine.cleanup()
      await performanceMonitor.cleanup()
    })
  })

  describe('Command Execution Performance', () => {
    it('should execute simple commands within threshold', async () => {
      const commands = ['/help', '/status', '/config show']
      
      for (const command of commands) {
        const result = await TestUtils.measurePerformance(async () => {
          await system.commandRouter.processCommand(command)
        }, 10)
        
        console.log(`${command} average execution time: ${result.average.toFixed(2)}ms`)
        expect(result.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.command_execution.simple)
      }
    })

    it('should execute medium complexity commands within threshold', async () => {
      const commands = ['/agents', '/analytics', '/cache stats']
      
      for (const command of commands) {
        const result = await TestUtils.measurePerformance(async () => {
          await system.commandRouter.processCommand(command)
        }, 5)
        
        console.log(`${command} average execution time: ${result.average.toFixed(2)}ms`)
        expect(result.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.command_execution.medium)
      }
    })

    it('should maintain consistent performance across iterations', async () => {
      const iterations = 20
      const command = '/help'
      
      const result = await TestUtils.measurePerformance(async () => {
        await system.commandRouter.processCommand(command)
      }, iterations)
      
      const variance = Math.sqrt(
        result.times.reduce((sum, time) => sum + Math.pow(time - result.average, 2), 0) / iterations
      )
      
      console.log(`Performance variance: ${variance.toFixed(2)}ms`)
      console.log(`Min: ${result.min.toFixed(2)}ms, Max: ${result.max.toFixed(2)}ms`)
      
      // Variance should be reasonable (less than 50% of average)
      expect(variance).to.be.lessThan(result.average * 0.5)
    })

    it('should show performance improvement with caching', async () => {
      const command = '/help'
      
      // First execution (no cache)
      const firstResult = await TestUtils.measurePerformance(async () => {
        await system.commandRouter.processCommand(command)
      }, 1)
      
      // Subsequent executions (with cache)
      const cachedResult = await TestUtils.measurePerformance(async () => {
        await system.commandRouter.processCommand(command)
      }, 5)
      
      console.log(`First execution: ${firstResult.average.toFixed(2)}ms`)
      console.log(`Cached executions: ${cachedResult.average.toFixed(2)}ms`)
      
      // Cached executions should be faster or similar
      expect(cachedResult.average).to.be.lessThanOrEqual(firstResult.average * 1.1)
    })
  })

  describe('Cache Performance', () => {
    it('should perform cache operations within thresholds', async () => {
      const cache = system.cache
      const testData = { test: 'value', number: 42, array: [1, 2, 3] }
      
      // Test SET performance
      const setResult = await TestUtils.measurePerformance(async () => {
        await cache.set(`test-key-${Math.random()}`, testData)
      }, 100)
      
      console.log(`Cache SET average: ${setResult.average.toFixed(2)}ms`)
      expect(setResult.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.cache_operations.set)
      
      // Test GET performance
      await cache.set('get-test-key', testData)
      const getResult = await TestUtils.measurePerformance(async () => {
        await cache.get('get-test-key')
      }, 100)
      
      console.log(`Cache GET average: ${getResult.average.toFixed(2)}ms`)
      expect(getResult.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.cache_operations.get)
      
      // Test DELETE performance
      const deleteResult = await TestUtils.measurePerformance(async () => {
        const key = `delete-test-${Math.random()}`
        await cache.set(key, testData)
        await cache.delete(key)
      }, 50)
      
      console.log(`Cache DELETE average: ${deleteResult.average.toFixed(2)}ms`)
      expect(deleteResult.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.cache_operations.delete)
    })

    it('should handle large data efficiently', async () => {
      const cache = system.cache
      const largeData = {
        array: new Array(1000).fill(0).map((_, i) => ({ id: i, data: `item-${i}` })),
        text: 'x'.repeat(10000),
        nested: {
          level1: { level2: { level3: { data: 'deep' } } }
        }
      }
      
      const result = await TestUtils.measurePerformance(async () => {
        await cache.set('large-data', largeData)
        await cache.get('large-data')
      }, 10)
      
      console.log(`Large data cache operations average: ${result.average.toFixed(2)}ms`)
      expect(result.average).to.be.lessThan(100) // Should handle large data within 100ms
    })

    it('should maintain performance under concurrent access', async () => {
      const cache = system.cache
      const concurrency = 20
      
      const result = await TestUtils.measurePerformance(async () => {
        const promises = []
        
        for (let i = 0; i < concurrency; i++) {
          promises.push(cache.set(`concurrent-${i}`, { data: i }))
          promises.push(cache.get(`concurrent-${i}`))
        }
        
        await Promise.all(promises)
      }, 5)
      
      console.log(`Concurrent cache operations average: ${result.average.toFixed(2)}ms`)
      expect(result.average).to.be.lessThan(200) // Should handle concurrency efficiently
    })
  })

  describe('Decision Engine Performance', () => {
    it('should make decisions within threshold', async () => {
      const decisionEngine = system.decisionEngine
      const commands = ['/help', '/status', '/analytics', '/agents']
      
      for (const command of commands) {
        const result = await TestUtils.measurePerformance(async () => {
          await decisionEngine.makeDecision(command, {})
        }, 20)
        
        console.log(`Decision for ${command}: ${result.average.toFixed(2)}ms`)
        expect(result.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.decision_making)
      }
    })

    it('should improve decision speed with learning', async () => {
      const decisionEngine = system.decisionEngine
      const command = '/help'
      
      // Initial decisions
      const initialResult = await TestUtils.measurePerformance(async () => {
        await decisionEngine.makeDecision(command, {})
      }, 10)
      
      // Record some performance data
      for (let i = 0; i < 20; i++) {
        decisionEngine.recordPerformance(command, true, 100 + Math.random() * 50)
      }
      
      // Decisions after learning
      const learnedResult = await TestUtils.measurePerformance(async () => {
        await decisionEngine.makeDecision(command, {})
      }, 10)
      
      console.log(`Initial decisions: ${initialResult.average.toFixed(2)}ms`)
      console.log(`Learned decisions: ${learnedResult.average.toFixed(2)}ms`)
      
      // Should maintain or improve performance
      expect(learnedResult.average).to.be.lessThanOrEqual(initialResult.average * 1.1)
    })
  })

  describe('Concurrent Load Performance', () => {
    it('should handle 10 concurrent users efficiently', async () => {
      const userCount = 10
      const commandsPerUser = 5
      
      const result = await TestUtils.measurePerformance(async () => {
        const userPromises = []
        
        for (let user = 0; user < userCount; user++) {
          const userCommands = []
          
          for (let cmd = 0; cmd < commandsPerUser; cmd++) {
            userCommands.push(
              system.commandRouter.processCommand('/help', {
                context: { user: `user-${user}` }
              })
            )
          }
          
          userPromises.push(Promise.all(userCommands))
        }
        
        await Promise.all(userPromises)
      }, 3)
      
      console.log(`10 concurrent users: ${result.average.toFixed(2)}ms`)
      expect(result.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.concurrent_load['10_users'])
    })

    it('should handle 50 concurrent users efficiently', async () => {
      const userCount = 50
      const commandsPerUser = 3
      
      const result = await TestUtils.measurePerformance(async () => {
        const userPromises = []
        
        for (let user = 0; user < userCount; user++) {
          const userCommands = []
          
          for (let cmd = 0; cmd < commandsPerUser; cmd++) {
            userCommands.push(
              system.commandRouter.processCommand('/status', {
                context: { user: `user-${user}` }
              })
            )
          }
          
          userPromises.push(Promise.all(userCommands))
        }
        
        await Promise.all(userPromises)
      }, 2)
      
      console.log(`50 concurrent users: ${result.average.toFixed(2)}ms`)
      expect(result.average).to.be.lessThan(PERFORMANCE_THRESHOLDS.concurrent_load['50_users'])
    })

    it('should maintain response times under sustained load', async () => {
      const duration = 10000 // 10 seconds
      const interval = 100   // New request every 100ms
      const startTime = Date.now()
      const responseTimes = []
      
      while (Date.now() - startTime < duration) {
        const requestStart = performance.now()
        
        await system.commandRouter.processCommand('/help')
        
        const responseTime = performance.now() - requestStart
        responseTimes.push(responseTime)
        
        await TestUtils.delay(interval)
      }
      
      const averageResponseTime = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length
      const maxResponseTime = Math.max(...responseTimes)
      
      console.log(`Sustained load - Average: ${averageResponseTime.toFixed(2)}ms, Max: ${maxResponseTime.toFixed(2)}ms`)
      
      expect(averageResponseTime).to.be.lessThan(200)
      expect(maxResponseTime).to.be.lessThan(1000)
    })
  })

  describe('Memory Performance', () => {
    it('should maintain stable memory usage', async () => {
      const initialMemory = process.memoryUsage()
      
      // Execute many commands to test memory stability
      for (let i = 0; i < 100; i++) {
        await system.commandRouter.processCommand('/help')
        await system.commandRouter.processCommand('/status')
        
        if (i % 20 === 0) {
          // Force garbage collection if available
          if (global.gc) {
            global.gc()
          }
        }
      }
      
      const finalMemory = process.memoryUsage()
      const memoryIncrease = finalMemory.heapUsed - initialMemory.heapUsed
      
      console.log(`Memory increase: ${(memoryIncrease / 1024 / 1024).toFixed(2)}MB`)
      
      // Memory increase should be reasonable (less than 50MB)
      expect(memoryIncrease).to.be.lessThan(50 * 1024 * 1024)
    })

    it('should handle cache memory efficiently', async () => {
      const cache = system.cache
      const initialMemory = process.memoryUsage()
      
      // Fill cache with data
      for (let i = 0; i < 1000; i++) {
        await cache.set(`memory-test-${i}`, {
          id: i,
          data: `test-data-${i}`,
          timestamp: Date.now()
        })
      }
      
      const afterCacheMemory = process.memoryUsage()
      
      // Clear cache
      await cache.clear()
      
      // Force garbage collection if available
      if (global.gc) {
        global.gc()
      }
      
      await TestUtils.delay(100) // Allow GC to run
      
      const afterClearMemory = process.memoryUsage()
      
      const cacheMemoryUsage = afterCacheMemory.heapUsed - initialMemory.heapUsed
      const memoryRecovered = afterCacheMemory.heapUsed - afterClearMemory.heapUsed
      
      console.log(`Cache memory usage: ${(cacheMemoryUsage / 1024 / 1024).toFixed(2)}MB`)
      console.log(`Memory recovered: ${(memoryRecovered / 1024 / 1024).toFixed(2)}MB`)
      
      // Should recover most of the memory
      expect(memoryRecovered).to.be.greaterThan(cacheMemoryUsage * 0.5)
    })
  })

  describe('Performance Monitoring Overhead', () => {
    it('should have minimal monitoring overhead', async () => {
      // Test without monitoring
      const monitoringDisabled = { ...testConfig }
      monitoringDisabled.monitoring.enabled = false
      
      const systemWithoutMonitoring = await initializeSystemForBenchmarks()
      systemWithoutMonitoring.performanceMonitor.monitoringConfig.enabled = false
      
      const withoutMonitoringResult = await TestUtils.measurePerformance(async () => {
        await systemWithoutMonitoring.commandRouter.processCommand('/help')
      }, 20)
      
      // Test with monitoring
      const withMonitoringResult = await TestUtils.measurePerformance(async () => {
        await system.commandRouter.processCommand('/help')
      }, 20)
      
      const overhead = withMonitoringResult.average - withoutMonitoringResult.average
      const overheadPercentage = (overhead / withoutMonitoringResult.average) * 100
      
      console.log(`Monitoring overhead: ${overhead.toFixed(2)}ms (${overheadPercentage.toFixed(1)}%)`)
      
      // Monitoring overhead should be less than 20%
      expect(overheadPercentage).to.be.lessThan(20)
      
      await cleanupSystem(systemWithoutMonitoring)
    })
  })

  describe('Scalability Tests', () => {
    it('should scale linearly with simple operations', async () => {
      const testSizes = [10, 50, 100]
      const results = {}
      
      for (const size of testSizes) {
        const result = await TestUtils.measurePerformance(async () => {
          const promises = []
          
          for (let i = 0; i < size; i++) {
            promises.push(system.commandRouter.processCommand('/help'))
          }
          
          await Promise.all(promises)
        }, 3)
        
        results[size] = result.average
        console.log(`${size} operations: ${result.average.toFixed(2)}ms`)
      }
      
      // Check if scaling is roughly linear
      const ratio50to10 = results[50] / results[10]
      const ratio100to50 = results[100] / results[50]
      
      console.log(`Scaling ratios - 50/10: ${ratio50to10.toFixed(2)}, 100/50: ${ratio100to50.toFixed(2)}`)
      
      // Ratios should be reasonable (not exponential growth)
      expect(ratio50to10).to.be.lessThan(8) // Should be close to 5, allow some overhead
      expect(ratio100to50).to.be.lessThan(4) // Should be close to 2, allow some overhead
    })
  })

  describe('Performance Regression Detection', () => {
    it('should detect performance regressions', async () => {
      // Baseline performance
      const baselineResult = await TestUtils.measurePerformance(async () => {
        await system.commandRouter.processCommand('/help')
      }, 20)
      
      // Simulate performance regression by adding artificial delay
      const originalExecute = system.commandExecutor.executeCommand
      system.commandExecutor.executeCommand = async function(...args) {
        await TestUtils.delay(50) // Add 50ms delay
        return originalExecute.apply(this, args)
      }
      
      const regressionResult = await TestUtils.measurePerformance(async () => {
        await system.commandRouter.processCommand('/help')
      }, 20)
      
      const performanceDegradation = regressionResult.average - baselineResult.average
      
      console.log(`Baseline: ${baselineResult.average.toFixed(2)}ms`)
      console.log(`With regression: ${regressionResult.average.toFixed(2)}ms`)
      console.log(`Degradation: ${performanceDegradation.toFixed(2)}ms`)
      
      // Should detect the artificial regression
      expect(performanceDegradation).to.be.greaterThan(40) // Should detect the 50ms delay
      
      // Restore original function
      system.commandExecutor.executeCommand = originalExecute
    })
  })

  describe('Performance Summary', () => {
    it('should generate comprehensive performance report', async () => {
      // Execute various commands to generate data
      await system.commandRouter.processCommand('/help')
      await system.commandRouter.processCommand('/status')
      await system.commandRouter.processCommand('/analytics')
      
      const performanceReport = system.performanceMonitor.getPerformanceReport()
      
      expect(performanceReport).to.have.property('timestamp')
      expect(performanceReport).to.have.property('system')
      expect(performanceReport).to.have.property('commands')
      
      console.log('Performance Report Summary:')
      console.log(`- System uptime: ${performanceReport.system.current.uptime}s`)
      console.log(`- Total commands: ${performanceReport.system.totals.commands}`)
      console.log(`- Success rate: ${performanceReport.system.rates.successRate}`)
      console.log(`- Cache hit rate: ${performanceReport.cache.hitRate}`)
      
      // Verify performance meets expectations
      expect(parseFloat(performanceReport.system.rates.successRate)).to.be.greaterThan(95)
    })
  })
})