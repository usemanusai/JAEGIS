/**
 * JAEGIS AI System Integration Example
 * Comprehensive example showing how to integrate the AI system with existing JAEGIS
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const { JAEGISAISystem } = require('../src/nodejs/ai')
const logger = require('../src/nodejs/utils/logger')

// Example: Complete AI System Integration
async function demonstrateAIIntegration() {
  console.log('🚀 JAEGIS AI System Integration Example')
  console.log('=====================================\n')

  try {
    // 1. Configuration Setup
    console.log('📋 Step 1: Configuration Setup')
    const config = {
      ai: {
        enabled: true,
        auto_start: true,
        integration_mode: 'enhanced',
        
        openrouter: {
          keys: [
            {
              key: process.env.OPENROUTER_KEY_1 || 'sk-or-v1-demo-key-1',
              tier: 'free',
              description: 'Demo key #1'
            },
            {
              key: process.env.OPENROUTER_KEY_2 || 'sk-or-v1-demo-key-2',
              tier: 'free',
              description: 'Demo key #2'
            }
          ],
          auto_key_rotation: true,
          cache_responses: true
        },
        
        redis: {
          environment: 'development',
          max_agents: 100, // Reduced for demo
          enable_vector_search: true,
          enable_streams: true
        },
        
        learning: {
          enabled: true,
          max_concurrent_discussions: 2,
          learning_interval: 300000 // 5 minutes for demo
        },
        
        background: {
          enabled: true,
          max_concurrent_tasks: 2,
          research_interval: 600000 // 10 minutes for demo
        },
        
        dashboard: {
          enabled: true,
          refresh_interval: 15000 // 15 seconds for demo
        }
      }
    }
    console.log('✅ Configuration prepared\n')

    // 2. Mock Existing JAEGIS Components
    console.log('🔗 Step 2: Setting up existing JAEGIS components')
    const mockJAEGISComponents = createMockJAEGISComponents()
    console.log('✅ Mock JAEGIS components created\n')

    // 3. Initialize AI System
    console.log('🤖 Step 3: Initializing AI System')
    const aiSystem = await JAEGISAISystem.create(config, mockJAEGISComponents)
    console.log('✅ AI System initialized successfully\n')

    // 4. Demonstrate Core Features
    await demonstrateCoreFeatures(aiSystem)

    // 5. Demonstrate Agent Management
    await demonstrateAgentManagement(aiSystem)

    // 6. Demonstrate Learning Capabilities
    await demonstrateLearningCapabilities(aiSystem)

    // 7. Demonstrate Background Processing
    await demonstrateBackgroundProcessing(aiSystem)

    // 8. Demonstrate Monitoring & Alerts
    await demonstrateMonitoring(aiSystem)

    // 9. Demonstrate Integration Benefits
    await demonstrateIntegrationBenefits(aiSystem, mockJAEGISComponents)

    // 10. Performance Metrics
    await showPerformanceMetrics(aiSystem)

    // 11. Cleanup
    console.log('🧹 Step 11: Cleanup')
    await aiSystem.stop()
    console.log('✅ AI System stopped gracefully\n')

    console.log('🎉 AI Integration Example Completed Successfully!')
    console.log('================================================\n')

  } catch (error) {
    console.error('❌ Example failed:', error.message)
    process.exit(1)
  }
}

// Create mock JAEGIS components for demonstration
function createMockJAEGISComponents() {
  return {
    commandRouter: {
      processCommand: async (command, parameters, context) => {
        console.log(`  📨 Processing command: ${command}`)
        return {
          success: true,
          result: `Processed: ${command}`,
          timestamp: Date.now()
        }
      }
    },
    
    cacheManager: {
      get: async (key) => {
        console.log(`  📋 Cache GET: ${key}`)
        return null // Simulate cache miss
      },
      set: async (key, value, ttl) => {
        console.log(`  📋 Cache SET: ${key} (TTL: ${ttl}ms)`)
        return true
      },
      getStats: () => ({
        memory: {
          hits: 150,
          misses: 50,
          keys: 25,
          hitRate: '75%'
        }
      })
    },
    
    decisionEngine: {
      makeDecision: async (command, options) => {
        console.log(`  🧠 Making decision for: ${command}`)
        return {
          action: 'execute',
          confidence: 0.8,
          routing: { strategy: 'direct' }
        }
      }
    },
    
    errorHandler: {
      handleError: async (error, context) => {
        console.log(`  ⚠️ Handling error: ${error.message}`)
        return {
          handled: true,
          recovery: { strategy: 'retry' }
        }
      }
    },
    
    performanceMonitor: {
      recordMetric: (name, value, tags) => {
        console.log(`  📊 Metric: ${name} = ${value}`)
      },
      getSystemStats: () => ({
        current: {
          cpu: 0.25,
          memory: 0.45,
          uptime: 3600000
        }
      })
    },
    
    contextManager: {
      getContext: async (contextId) => {
        return {
          user: 'demo_user',
          session: 'demo_session',
          timestamp: Date.now()
        }
      },
      updateContext: async (contextId, updates) => {
        console.log(`  🔄 Context updated: ${contextId}`)
        return true
      }
    },
    
    responseFormatter: {
      formatResponse: (data, format) => {
        console.log(`  📝 Formatting response as: ${format}`)
        return {
          formatted: true,
          data,
          format
        }
      }
    }
  }
}

// Demonstrate core AI features
async function demonstrateCoreFeatures(aiSystem) {
  console.log('🎯 Step 4: Demonstrating Core AI Features')
  
  // AI Completion
  console.log('  🤖 Testing AI Completion...')
  const completionResult = await aiSystem.processAIRequest({
    type: 'completion',
    prompt: 'Explain the benefits of AI-powered command processing',
    options: {
      category: 'reasoning',
      maxTokens: 200,
      temperature: 0.7
    }
  })
  
  if (completionResult.success) {
    console.log('  ✅ AI Completion successful')
    console.log(`  📝 Response: ${completionResult.result.content.substring(0, 100)}...`)
  } else {
    console.log('  ⚠️ AI Completion failed (expected in demo mode)')
  }
  
  // System Status
  console.log('  📊 Checking System Status...')
  const status = aiSystem.getSystemStatus()
  console.log(`  📈 System State: ${status.state}`)
  console.log(`  🔧 Integration Mode: ${status.integrationMode}`)
  console.log(`  ⏱️ Uptime: ${Math.round(status.uptime / 1000)}s`)
  console.log(`  🧩 Components: ${Object.keys(status.components).length}`)
  console.log('✅ Core features demonstrated\n')
}

// Demonstrate agent management
async function demonstrateAgentManagement(aiSystem) {
  console.log('🤖 Step 5: Demonstrating Agent Management')
  
  // Create research agent
  console.log('  👤 Creating Research Agent...')
  const researchAgentResult = await aiSystem.processAIRequest({
    type: 'agent_create',
    data: {
      name: 'Demo Research Agent',
      type: 'research',
      capabilities: ['web_research', 'data_analysis', 'trend_identification'],
      metadata: {
        specialization: 'technology_research',
        demo: true
      }
    }
  })
  
  if (researchAgentResult.success) {
    console.log(`  ✅ Research Agent created: ${researchAgentResult.result}`)
  }
  
  // Create analysis agent
  console.log('  👤 Creating Analysis Agent...')
  const analysisAgentResult = await aiSystem.processAIRequest({
    type: 'agent_create',
    data: {
      name: 'Demo Analysis Agent',
      type: 'analysis',
      capabilities: ['data_analysis', 'pattern_recognition', 'insight_generation'],
      metadata: {
        specialization: 'performance_analysis',
        demo: true
      }
    }
  })
  
  if (analysisAgentResult.success) {
    console.log(`  ✅ Analysis Agent created: ${analysisAgentResult.result}`)
  }
  
  console.log('✅ Agent management demonstrated\n')
}

// Demonstrate learning capabilities
async function demonstrateLearningCapabilities(aiSystem) {
  console.log('🧠 Step 6: Demonstrating Learning Capabilities')
  
  // Start agent discussion
  console.log('  💬 Initiating Agent Discussion...')
  const discussionResult = await aiSystem.processAIRequest({
    type: 'agent_discussion',
    data: {
      topic: 'AI system optimization strategies',
      participants: ['demo_agent_1', 'demo_agent_2'],
      discussionType: 'knowledge_sharing'
    }
  })
  
  if (discussionResult.success) {
    console.log('  ✅ Agent discussion initiated')
  } else {
    console.log('  ⚠️ Agent discussion failed (expected in demo mode)')
  }
  
  // Check learning progress
  const learningEngine = aiSystem.getAutonomousLearningEngine()
  if (learningEngine) {
    console.log('  📚 Checking Learning Progress...')
    const learningReport = learningEngine.getLearningReport()
    console.log(`  📖 Knowledge Entries: ${learningReport.knowledgeBase.totalEntries}`)
    console.log(`  💬 Active Discussions: ${learningReport.activeDiscussions.count}`)
    console.log(`  📈 Learning Efficiency: ${(learningReport.metrics.learningEfficiency * 100).toFixed(1)}%`)
  }
  
  console.log('✅ Learning capabilities demonstrated\n')
}

// Demonstrate background processing
async function demonstrateBackgroundProcessing(aiSystem) {
  console.log('⚙️ Step 7: Demonstrating Background Processing')
  
  // Schedule web research task
  console.log('  🔍 Scheduling Web Research Task...')
  const researchTaskResult = await aiSystem.processAIRequest({
    type: 'background_task',
    data: {
      type: 'WEB_RESEARCH',
      priority: 2,
      data: {
        topic: 'Node.js performance optimization 2025',
        category: 'PROGRAMMING'
      }
    }
  })
  
  if (researchTaskResult.success) {
    console.log(`  ✅ Research task scheduled: ${researchTaskResult.result}`)
  }
  
  // Schedule performance analysis
  console.log('  📊 Scheduling Performance Analysis...')
  const analysisTaskResult = await aiSystem.processAIRequest({
    type: 'background_task',
    data: {
      type: 'PERFORMANCE_ANALYSIS',
      priority: 1,
      data: {
        timeframe: '1h'
      }
    }
  })
  
  if (analysisTaskResult.success) {
    console.log(`  ✅ Analysis task scheduled: ${analysisTaskResult.result}`)
  }
  
  // Check background processing status
  const backgroundManager = aiSystem.getBackgroundProcessManager()
  if (backgroundManager) {
    console.log('  ⚙️ Checking Background Processing Status...')
    const processingReport = backgroundManager.getProcessingReport()
    console.log(`  📋 Queue Length: ${processingReport.queue.length}`)
    console.log(`  🏃 Running Tasks: ${processingReport.queue.running}`)
    console.log(`  ✅ Completed Tasks: ${processingReport.metrics.completedTasks}`)
    console.log(`  👷 Active Workers: ${processingReport.workers.busy}/${processingReport.workers.total}`)
  }
  
  console.log('✅ Background processing demonstrated\n')
}

// Demonstrate monitoring and alerts
async function demonstrateMonitoring(aiSystem) {
  console.log('📊 Step 8: Demonstrating Monitoring & Alerts')
  
  // Get dashboard data
  console.log('  📈 Retrieving Dashboard Data...')
  try {
    const dashboardData = aiSystem.getDashboardData()
    console.log('  📊 Dashboard Sections Available:')
    Object.keys(dashboardData).forEach(section => {
      console.log(`    - ${section}`)
    })
    
    // Show overview data
    if (dashboardData.overview) {
      console.log('  🎯 System Overview:')
      console.log(`    Status: ${dashboardData.overview.systemStatus}`)
      console.log(`    Agents: ${dashboardData.overview.totalAgents}`)
      console.log(`    Discussions: ${dashboardData.overview.activeDiscussions}`)
      console.log(`    Background Tasks: ${dashboardData.overview.backgroundTasks}`)
    }
  } catch (error) {
    console.log('  ⚠️ Dashboard not available (expected in demo mode)')
  }
  
  // Check alerts
  console.log('  🚨 Checking System Alerts...')
  try {
    const alerts = aiSystem.getAlerts({ unresolved: true })
    console.log(`  📢 Active Alerts: ${alerts.length}`)
    
    if (alerts.length > 0) {
      alerts.slice(0, 3).forEach((alert, index) => {
        console.log(`    ${index + 1}. [${alert.type.toUpperCase()}] ${alert.message}`)
      })
    }
  } catch (error) {
    console.log('  ⚠️ Alerts not available (expected in demo mode)')
  }
  
  // Subscribe to real-time updates (demo)
  console.log('  📡 Setting up Real-time Monitoring...')
  try {
    const unsubscribe = aiSystem.subscribeToUpdates((update) => {
      console.log(`    📊 Real-time update: ${update.section}`)
    })
    
    // Simulate some time passing
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Unsubscribe
    unsubscribe()
    console.log('  ✅ Real-time monitoring demonstrated')
  } catch (error) {
    console.log('  ⚠️ Real-time monitoring not available (expected in demo mode)')
  }
  
  console.log('✅ Monitoring & alerts demonstrated\n')
}

// Demonstrate integration benefits
async function demonstrateIntegrationBenefits(aiSystem, mockComponents) {
  console.log('🌉 Step 9: Demonstrating Integration Benefits')
  
  console.log('  🔧 Testing Enhanced Command Processing...')
  
  // Simulate enhanced command processing
  const enhancedCommand = '/status --ai-enhanced'
  console.log(`  📨 Processing enhanced command: ${enhancedCommand}`)
  
  // The AI Integration Bridge would enhance this command
  const integrationBridge = aiSystem.getAIIntegrationBridge()
  if (integrationBridge) {
    console.log('  🌉 AI Integration Bridge active')
    const integrationReport = integrationBridge.getIntegrationReport()
    console.log(`  📈 Enhancement Success Rate: ${integrationReport.metrics.successRate}`)
    console.log(`  ⚡ AI Response Time: ${integrationReport.metrics.aiResponseTime}ms`)
    console.log(`  🔄 Total Enhancements: ${integrationReport.metrics.totalEnhancements}`)
  }
  
  console.log('  🎯 Integration Benefits:')
  console.log('    ✅ Intelligent command routing')
  console.log('    ✅ Context-aware responses')
  console.log('    ✅ Predictive caching')
  console.log('    ✅ Error intelligence')
  console.log('    ✅ Performance optimization')
  console.log('    ✅ Learning integration')
  
  console.log('✅ Integration benefits demonstrated\n')
}

// Show performance metrics
async function showPerformanceMetrics(aiSystem) {
  console.log('📈 Step 10: Performance Metrics Summary')
  
  const status = aiSystem.getSystemStatus()
  
  console.log('  🎯 System Performance:')
  console.log(`    Uptime: ${Math.round(status.uptime / 1000)}s`)
  console.log(`    Total Requests: ${status.metrics.totalRequests}`)
  console.log(`    Successful Requests: ${status.metrics.successfulRequests}`)
  console.log(`    Failed Requests: ${status.metrics.failedRequests}`)
  console.log(`    Success Rate: ${status.metrics.totalRequests > 0 ? 
    ((status.metrics.successfulRequests / status.metrics.totalRequests) * 100).toFixed(1) : 0}%`)
  
  console.log('  🧩 Component Status:')
  Object.entries(status.components).forEach(([name, component]) => {
    const statusIcon = component.initialized ? '✅' : '❌'
    console.log(`    ${statusIcon} ${name}: ${component.available ? 'Available' : 'Unavailable'}`)
  })
  
  // OpenRouter Manager metrics
  const openRouterManager = aiSystem.getOpenRouterManager()
  if (openRouterManager) {
    console.log('  🤖 OpenRouter Metrics:')
    const report = openRouterManager.getUsageReport()
    console.log(`    Total Capacity: ${report.capacity.total}`)
    console.log(`    Used Capacity: ${report.capacity.used}`)
    console.log(`    Utilization: ${report.capacity.utilizationRate}`)
    console.log(`    Active Keys: ${report.keys.active}/${report.keys.total}`)
  }
  
  // Redis AI Manager metrics
  const redisAIManager = aiSystem.getRedisAIManager()
  if (redisAIManager) {
    console.log('  🗄️ Redis AI Metrics:')
    const report = redisAIManager.getUsageReport()
    console.log(`    Agent Count: ${report.metrics.agentCount}`)
    console.log(`    Conversation Count: ${report.metrics.conversationCount}`)
    console.log(`    Data Size: ${Math.round(report.metrics.dataSize / 1024)}KB`)
  }
  
  console.log('✅ Performance metrics displayed\n')
}

// Advanced integration example
async function advancedIntegrationExample() {
  console.log('🚀 Advanced AI Integration Example')
  console.log('==================================\n')

  // Custom configuration for advanced features
  const advancedConfig = {
    ai: {
      enabled: true,
      integration_mode: 'autonomous',
      
      openrouter: {
        keys: [
          { key: 'sk-or-v1-advanced-key-1', tier: 'paid' },
          { key: 'sk-or-v1-advanced-key-2', tier: 'paid' }
        ],
        enable_model_discovery: true,
        cache_responses: true
      },
      
      learning: {
        enabled: true,
        max_concurrent_discussions: 5,
        synthesis_threshold: 0.8,
        consensus_threshold: 0.9
      },
      
      integration: {
        enhancement_level: 'autonomous',
        enable_predictive_caching: true,
        ai_response_threshold: 0.8
      }
    }
  }

  try {
    // Initialize with advanced configuration
    const aiSystem = await JAEGISAISystem.create(advancedConfig)
    
    // Demonstrate advanced agent creation
    console.log('🤖 Creating Specialized Agents...')
    
    const securityAgent = await aiSystem.processAIRequest({
      type: 'agent_create',
      data: {
        name: 'Security Specialist',
        type: 'security',
        capabilities: [
          'threat_detection',
          'vulnerability_analysis',
          'security_recommendations',
          'incident_response'
        ],
        metadata: {
          specialization: 'cybersecurity',
          clearance_level: 'high',
          priority: 'critical'
        }
      }
    })
    
    const optimizationAgent = await aiSystem.processAIRequest({
      type: 'agent_create',
      data: {
        name: 'Performance Optimizer',
        type: 'optimization',
        capabilities: [
          'performance_analysis',
          'resource_optimization',
          'bottleneck_identification',
          'scaling_recommendations'
        ],
        metadata: {
          specialization: 'system_performance',
          priority: 'high'
        }
      }
    })
    
    // Advanced learning session
    console.log('🧠 Initiating Advanced Learning Session...')
    await aiSystem.processAIRequest({
      type: 'agent_discussion',
      data: {
        topic: 'AI system security and performance optimization',
        participants: [securityAgent.result, optimizationAgent.result],
        discussionType: 'problem_solving',
        constraints: {
          maxRounds: 8,
          consensusThreshold: 0.9,
          timeLimit: 900000 // 15 minutes
        }
      }
    })
    
    // Advanced background processing
    console.log('⚙️ Scheduling Advanced Background Tasks...')
    
    // Security audit task
    await aiSystem.processAIRequest({
      type: 'background_task',
      data: {
        type: 'SECURITY_AUDIT',
        priority: 1,
        data: {
          scope: 'comprehensive',
          include_dependencies: true,
          generate_report: true
        }
      }
    })
    
    // Performance optimization task
    await aiSystem.processAIRequest({
      type: 'background_task',
      data: {
        type: 'PERFORMANCE_OPTIMIZATION',
        priority: 1,
        data: {
          target_metrics: ['response_time', 'throughput', 'resource_usage'],
          optimization_level: 'aggressive'
        }
      }
    })
    
    console.log('✅ Advanced integration example completed')
    
    await aiSystem.stop()
    
  } catch (error) {
    console.error('❌ Advanced example failed:', error.message)
  }
}

// Production deployment example
async function productionDeploymentExample() {
  console.log('🏭 Production Deployment Example')
  console.log('================================\n')

  const productionConfig = {
    ai: {
      enabled: true,
      integration_mode: 'enhanced',
      
      redis: {
        environment: 'production',
        url: process.env.REDIS_CLOUD_URL,
        max_agents: 50,
        compression_enabled: true
      },
      
      openrouter: {
        keys: process.env.OPENROUTER_KEYS?.split(',').map((key, index) => ({
          key: key.trim(),
          tier: index < 5 ? 'free' : 'paid',
          description: `Production key ${index + 1}`
        })) || []
      },
      
      dashboard: {
        enabled: true,
        retention_period: 43200000, // 12 hours
        enable_alert_notifications: true
      },
      
      security: {
        enable_input_validation: true,
        enable_output_filtering: true,
        enable_threat_detection: true
      },
      
      monitoring: {
        enable_metrics_collection: true,
        enable_performance_tracking: true,
        metrics_retention_hours: 168 // 7 days
      }
    }
  }

  console.log('🔧 Production configuration prepared')
  console.log('📊 Monitoring and security enabled')
  console.log('🔒 Threat detection active')
  console.log('📈 Performance tracking enabled')
  console.log('✅ Ready for production deployment\n')
}

// Main execution
async function main() {
  console.log('🎯 JAEGIS AI System - Integration Examples')
  console.log('==========================================\n')

  // Run basic integration example
  await demonstrateAIIntegration()
  
  console.log('\n' + '='.repeat(50) + '\n')
  
  // Run advanced integration example (commented out for demo)
  // await advancedIntegrationExample()
  
  console.log('\n' + '='.repeat(50) + '\n')
  
  // Show production deployment example
  await productionDeploymentExample()
  
  console.log('🎉 All examples completed successfully!')
}

// Error handling
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason)
  process.exit(1)
})

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error)
  process.exit(1)
})

// Run examples if this file is executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('❌ Example execution failed:', error)
    process.exit(1)
  })
}

module.exports = {
  demonstrateAIIntegration,
  advancedIntegrationExample,
  productionDeploymentExample,
  createMockJAEGISComponents
}