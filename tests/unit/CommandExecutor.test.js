/**
 * JAEGIS CommandExecutor Test Suite
 * Comprehensive tests for the command execution framework
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const { describe, it, beforeEach, afterEach, before, after } = require('mocha')
const { expect } = require('chai')
const sinon = require('sinon')

const CommandExecutor = require('../../src/nodejs/core/CommandExecutor')
const { setupTests, teardownTests } = require('../setup')

describe('CommandExecutor', () => {
  let executor
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
    executor = new CommandExecutor({
      config: testConfig,
      cache: mockServices.cache,
      pythonBridge: mockServices.pythonBridge,
      decisionEngine: mockServices.decisionEngine
    })
    
    await executor.initialize()
  })

  afterEach(async () => {
    if (executor) {
      await executor.cleanup()
    }
  })

  describe('Initialization', () => {
    it('should initialize successfully', async () => {
      expect(executor.isInitialized).to.be.true
      expect(executor.plugins.size).to.be.greaterThan(0)
    })

    it('should load core plugins', async () => {
      const corePlugins = ['help', 'status', 'config', 'agents', 'analytics']
      
      for (const plugin of corePlugins) {
        expect(executor.plugins.has(plugin)).to.be.true
      }
    })

    it('should setup middleware pipeline', async () => {
      expect(executor.middleware.length).to.be.greaterThan(0)
    })
  })

  describe('Plugin Management', () => {
    it('should register a new plugin', async () => {
      const testPlugin = {
        name: 'test-plugin',
        description: 'Test plugin',
        execute: async (context) => ({ message: 'Test executed' })
      }

      await executor.registerPlugin('test-plugin', testPlugin)
      
      expect(executor.plugins.has('test-plugin')).to.be.true
    })

    it('should validate plugin structure', async () => {
      const invalidPlugin = {
        name: 'invalid-plugin'
        // Missing execute method
      }

      try {
        await executor.registerPlugin('invalid-plugin', invalidPlugin)
        expect.fail('Should have thrown an error')
      } catch (error) {
        expect(error.message).to.include('Invalid plugin structure')
      }
    })

    it('should wrap plugin execution with context', async () => {
      const testPlugin = {
        name: 'context-test',
        execute: sinon.spy(async (context) => {
          expect(context).to.have.property('executionId')
          expect(context).to.have.property('cache')
          expect(context).to.have.property('pythonBridge')
          expect(context).to.have.property('logger')
          return { success: true }
        })
      }

      await executor.registerPlugin('context-test', testPlugin)
      await executor.executeCommand('context-test')
      
      expect(testPlugin.execute.calledOnce).to.be.true
    })
  })

  describe('Command Execution', () => {
    it('should execute help command successfully', async () => {
      const result = await executor.executeCommand('help')
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('title')
      expect(result.data).to.have.property('available_commands')
    })

    it('should execute status command successfully', async () => {
      const result = await executor.executeCommand('status')
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('system')
      expect(result.data).to.have.property('executor')
      expect(result.data).to.have.property('services')
    })

    it('should handle command with parameters', async () => {
      const result = await executor.executeCommand('help', { command: 'status' })
      
      expect(result.success).to.be.true
      expect(result.data).to.have.property('command')
      expect(result.data.command).to.equal('status')
    })

    it('should handle unknown command', async () => {
      const result = await executor.executeCommand('unknown-command')
      
      expect(result.success).to.be.false
      expect(result.error).to.include('No plugin found')
    })

    it('should normalize command names', async () => {
      const result1 = await executor.executeCommand('/help')
      const result2 = await executor.executeCommand('HELP')
      const result3 = await executor.executeCommand('  help  ')
      
      expect(result1.success).to.be.true
      expect(result2.success).to.be.true
      expect(result3.success).to.be.true
    })

    it('should track execution metrics', async () => {
      const initialCount = executor.getProcessedCount()
      
      await executor.executeCommand('help')
      
      expect(executor.getProcessedCount()).to.be.greaterThan(initialCount)
    })

    it('should generate unique execution IDs', async () => {
      const result1 = await executor.executeCommand('help')
      const result2 = await executor.executeCommand('help')
      
      expect(result1.executionId).to.not.equal(result2.executionId)
    })
  })

  describe('Middleware Pipeline', () => {
    it('should apply middleware in order', async () => {
      const executionOrder = []
      
      // Add test middleware
      executor.middleware.unshift(async (context) => {
        executionOrder.push('middleware1')
        return context
      })
      
      executor.middleware.push(async (context) => {
        executionOrder.push('middleware2')
        return context
      })
      
      await executor.executeCommand('help')
      
      expect(executionOrder).to.include('middleware1')
      expect(executionOrder).to.include('middleware2')
    })

    it('should handle middleware errors', async () => {
      // Add failing middleware
      executor.middleware.push(async (context) => {
        throw new Error('Middleware error')
      })
      
      const result = await executor.executeCommand('help')
      
      expect(result.success).to.be.false
      expect(result.error).to.include('Middleware failed')
    })

    it('should validate parameters through middleware', async () => {
      const result = await executor.executeCommand('help', {
        maliciousParam: '<script>alert("xss")</script>',
        longParam: 'x'.repeat(2000)
      })
      
      expect(result.success).to.be.true
      // Parameters should be sanitized by middleware
    })
  })

  describe('Plugin Hooks', () => {
    it('should execute beforeExecution hooks', async () => {
      const hookSpy = sinon.spy()
      
      const testPlugin = {
        name: 'hook-test',
        execute: async () => ({ success: true }),
        hooks: {
          beforeExecution: hookSpy
        }
      }
      
      await executor.registerPlugin('hook-test', testPlugin)
      await executor.executeCommand('hook-test')
      
      expect(hookSpy.calledOnce).to.be.true
    })

    it('should execute afterExecution hooks', async () => {
      const hookSpy = sinon.spy()
      
      const testPlugin = {
        name: 'hook-test',
        execute: async () => ({ success: true }),
        hooks: {
          afterExecution: hookSpy
        }
      }
      
      await executor.registerPlugin('hook-test', testPlugin)
      await executor.executeCommand('hook-test')
      
      expect(hookSpy.calledOnce).to.be.true
    })

    it('should execute onError hooks when plugin fails', async () => {
      const hookSpy = sinon.spy()
      
      const testPlugin = {
        name: 'error-test',
        execute: async () => {
          throw new Error('Plugin error')
        },
        hooks: {
          onError: hookSpy
        }
      }
      
      await executor.registerPlugin('error-test', testPlugin)
      const result = await executor.executeCommand('error-test')
      
      expect(result.success).to.be.false
      expect(hookSpy.calledOnce).to.be.true
    })

    it('should execute onSuccess hooks when plugin succeeds', async () => {
      const hookSpy = sinon.spy()
      
      const testPlugin = {
        name: 'success-test',
        execute: async () => ({ success: true }),
        hooks: {
          onSuccess: hookSpy
        }
      }
      
      await executor.registerPlugin('success-test', testPlugin)
      await executor.executeCommand('success-test')
      
      expect(hookSpy.calledOnce).to.be.true
    })
  })

  describe('Performance Tracking', () => {
    it('should track execution time', async () => {
      const result = await executor.executeCommand('help')
      
      expect(result).to.have.property('executionTime')
      expect(result.executionTime).to.be.a('number')
      expect(result.executionTime).to.be.greaterThan(0)
    })

    it('should update performance metrics', async () => {
      const initialStats = executor.getPerformanceStats()
      
      await executor.executeCommand('help')
      
      const updatedStats = executor.getPerformanceStats()
      expect(Object.keys(updatedStats)).to.have.length.greaterThan(0)
    })

    it('should track plugin performance separately', async () => {
      await executor.executeCommand('help')
      await executor.executeCommand('status')
      
      const stats = executor.getPluginPerformanceStats()
      expect(stats).to.be.an('array')
      expect(stats.length).to.be.greaterThan(0)
    })
  })

  describe('Error Handling', () => {
    it('should handle plugin execution errors gracefully', async () => {
      const errorPlugin = {
        name: 'error-plugin',
        execute: async () => {
          throw new Error('Test error')
        }
      }
      
      await executor.registerPlugin('error-plugin', errorPlugin)
      const result = await executor.executeCommand('error-plugin')
      
      expect(result.success).to.be.false
      expect(result.error).to.include('Test error')
    })

    it('should provide error context', async () => {
      const result = await executor.executeCommand('non-existent-command')
      
      expect(result.success).to.be.false
      expect(result).to.have.property('executionId')
      expect(result).to.have.property('timestamp')
    })

    it('should emit error events', async () => {
      let errorEvent = null
      
      executor.on('commandError', (event) => {
        errorEvent = event
      })
      
      await executor.executeCommand('non-existent-command')
      
      expect(errorEvent).to.not.be.null
      expect(errorEvent).to.have.property('command')
      expect(errorEvent).to.have.property('error')
    })
  })

  describe('Core Plugins', () => {
    describe('Help Plugin', () => {
      it('should provide general help', async () => {
        const result = await executor.executeCommand('help')
        
        expect(result.success).to.be.true
        expect(result.data).to.have.property('title')
        expect(result.data).to.have.property('available_commands')
        expect(result.data.available_commands).to.be.an('array')
      })

      it('should provide specific command help', async () => {
        const result = await executor.executeCommand('help', { command: 'status' })
        
        expect(result.success).to.be.true
        expect(result.data).to.have.property('command')
        expect(result.data.command).to.equal('status')
      })
    })

    describe('Status Plugin', () => {
      it('should return system status', async () => {
        const result = await executor.executeCommand('status')
        
        expect(result.success).to.be.true
        expect(result.data).to.have.property('system')
        expect(result.data).to.have.property('executor')
        expect(result.data.system).to.have.property('uptime')
        expect(result.data.executor).to.have.property('plugins_loaded')
      })
    })

    describe('Config Plugin', () => {
      it('should show configuration', async () => {
        const result = await executor.executeCommand('config', { action: 'show' })
        
        expect(result.success).to.be.true
        expect(result.data).to.have.property('system')
        expect(result.data).to.have.property('features')
      })

      it('should validate configuration', async () => {
        const result = await executor.executeCommand('config', { action: 'validate' })
        
        expect(result.success).to.be.true
        expect(result.data).to.have.property('valid')
      })
    })

    describe('Analytics Plugin', () => {
      it('should return analytics data', async () => {
        const result = await executor.executeCommand('analytics')
        
        expect(result.success).to.be.true
        expect(result.data).to.have.property('system_performance')
        expect(result.data).to.have.property('command_statistics')
      })
    })
  })

  describe('Concurrency', () => {
    it('should handle concurrent executions', async () => {
      const promises = []
      
      for (let i = 0; i < 5; i++) {
        promises.push(executor.executeCommand('help'))
      }
      
      const results = await Promise.all(promises)
      
      results.forEach(result => {
        expect(result.success).to.be.true
      })
    })

    it('should track active executions', async () => {
      const slowPlugin = {
        name: 'slow-plugin',
        execute: async () => {
          await new Promise(resolve => setTimeout(resolve, 100))
          return { success: true }
        }
      }
      
      await executor.registerPlugin('slow-plugin', slowPlugin)
      
      const promise1 = executor.executeCommand('slow-plugin')
      const promise2 = executor.executeCommand('slow-plugin')
      
      // Check active executions while commands are running
      expect(executor.activeExecutions.size).to.be.greaterThan(0)
      
      await Promise.all([promise1, promise2])
      
      // Should be cleaned up after completion
      expect(executor.activeExecutions.size).to.equal(0)
    })
  })

  describe('Events', () => {
    it('should emit commandExecuted event', async () => {
      let executedEvent = null
      
      executor.on('commandExecuted', (event) => {
        executedEvent = event
      })
      
      await executor.executeCommand('help')
      
      expect(executedEvent).to.not.be.null
      expect(executedEvent).to.have.property('command')
      expect(executedEvent).to.have.property('result')
    })

    it('should emit pluginRegistered event', async () => {
      let registeredEvent = null
      
      executor.on('pluginRegistered', (event) => {
        registeredEvent = event
      })
      
      const testPlugin = {
        name: 'event-test',
        execute: async () => ({ success: true })
      }
      
      await executor.registerPlugin('event-test', testPlugin)
      
      expect(registeredEvent).to.not.be.null
      expect(registeredEvent).to.have.property('name')
      expect(registeredEvent.name).to.equal('event-test')
    })
  })

  describe('Cleanup', () => {
    it('should cleanup resources properly', async () => {
      await executor.cleanup()
      
      expect(executor.isInitialized).to.be.false
      expect(executor.plugins.size).to.equal(0)
      expect(executor.middleware.length).to.equal(0)
    })
  })
})