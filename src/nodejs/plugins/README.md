# JAEGIS Plugin Architecture

## Overview

JAEGIS features a powerful plugin architecture that allows you to extend the command processing system with custom functionality. Plugins are dynamically loaded and can be developed in JavaScript with full access to the JAEGIS ecosystem.

## Plugin Structure

### Basic Plugin Template

```javascript
/**
 * Example JAEGIS Plugin
 * @version 1.0.0
 */

class ExamplePlugin {
  constructor() {
    this.name = 'example'
    this.description = 'Example plugin demonstrating JAEGIS plugin architecture'
    this.version = '1.0.0'
    this.category = 'utility'
    
    // Plugin metadata
    this.parameters = [
      {
        name: 'action',
        type: 'string',
        required: false,
        description: 'Action to perform'
      }
    ]
    
    this.examples = [
      {
        command: '/example',
        description: 'Basic example usage'
      },
      {
        command: '/example action=test',
        description: 'Example with parameters'
      }
    ]
    
    this.usage = '/example [action=<action>]'
  }

  /**
   * Main plugin execution method
   * @param {Object} context - Execution context
   * @returns {Object} - Plugin result
   */
  async execute(context) {
    const { parameters, logger, cache, pythonBridge, config } = context
    
    logger.info(`Executing example plugin with parameters:`, parameters)
    
    // Your plugin logic here
    const result = {
      message: 'Example plugin executed successfully',
      parameters,
      timestamp: Date.now()
    }
    
    return result
  }

  /**
   * Plugin lifecycle hooks (optional)
   */
  get hooks() {
    return {
      beforeExecution: async (context) => {
        context.logger.info('Example plugin: Before execution hook')
      },
      
      afterExecution: async (context) => {
        context.logger.info('Example plugin: After execution hook')
      },
      
      onError: async (context) => {
        context.logger.error('Example plugin: Error hook', context.error)
      },
      
      onSuccess: async (context) => {
        context.logger.info('Example plugin: Success hook')
      }
    }
  }
}

module.exports = new ExamplePlugin()
```

## Execution Context

When your plugin's `execute` method is called, it receives a rich execution context:

```javascript
const context = {
  // Command information
  command: 'example',
  originalCommand: '/example',
  parameters: { action: 'test' },
  
  // Execution metadata
  executionId: 'exec_1234567890_abc123',
  pluginName: 'example',
  startTime: 1234567890123,
  timestamp: 1234567890123,
  user: 'anonymous',
  
  // JAEGIS services
  cache: cacheManager,        // Access to caching system
  pythonBridge: pythonBridge, // Access to Python services
  config: config,             // System configuration
  logger: logger,             // Contextual logger
  
  // Additional context
  context: {
    cli: true,
    interactive: false,
    websocket: false
  }
}
```

## Plugin Capabilities

### 1. Caching

```javascript
async execute(context) {
  const { cache } = context
  
  // Get cached data
  const cached = await cache.get('my-plugin-data')
  if (cached) {
    return cached
  }
  
  // Process data
  const result = await this.processData()
  
  // Cache result for 1 hour
  await cache.set('my-plugin-data', result, 3600000)
  
  return result
}
```

### 2. Python Integration

```javascript
async execute(context) {
  const { pythonBridge } = context
  
  // Call Python service
  const response = await pythonBridge.fetchGitHubCommands(url)
  
  // Parse content with Python
  const parsed = await pythonBridge.parseMarkdownCommands(content)
  
  return parsed.data
}
```

### 3. Configuration Access

```javascript
async execute(context) {
  const { config } = context
  
  // Access system configuration
  const githubUrl = config.github.commands_url
  const cacheEnabled = config.cache.enabled
  
  return {
    github_url: githubUrl,
    cache_enabled: cacheEnabled
  }
}
```

### 4. Logging

```javascript
async execute(context) {
  const { logger } = context
  
  logger.info('Plugin started')
  logger.debug('Debug information', { data: 'value' })
  logger.warn('Warning message')
  logger.error('Error occurred', error)
  
  return { status: 'completed' }
}
```

## Plugin Types

### 1. Command Plugins

Standard plugins that respond to specific commands:

```javascript
class StatusPlugin {
  constructor() {
    this.name = 'status'
    this.description = 'Show system status'
  }
  
  async execute(context) {
    return {
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      timestamp: Date.now()
    }
  }
}
```

### 2. Middleware Plugins

Plugins that process all commands (registered as middleware):

```javascript
class AuthPlugin {
  constructor() {
    this.name = 'auth'
    this.type = 'middleware'
  }
  
  async execute(context) {
    // Authenticate user
    if (!context.user || context.user === 'anonymous') {
      throw new Error('Authentication required')
    }
    
    // Add user permissions to context
    context.permissions = await this.getUserPermissions(context.user)
    
    return context
  }
}
```

### 3. Background Plugins

Plugins that run continuously in the background:

```javascript
class MonitorPlugin {
  constructor() {
    this.name = 'monitor'
    this.type = 'background'
    this.interval = 30000 // 30 seconds
  }
  
  async start(context) {
    this.timer = setInterval(async () => {
      await this.checkSystemHealth(context)
    }, this.interval)
  }
  
  async stop() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  }
  
  async checkSystemHealth(context) {
    // Monitor system health
    const health = await this.getSystemHealth()
    
    if (health.status === 'unhealthy') {
      context.logger.warn('System health issue detected', health)
    }
  }
}
```

## Advanced Features

### 1. Plugin Dependencies

```javascript
class AdvancedPlugin {
  constructor() {
    this.name = 'advanced'
    this.dependencies = ['cache', 'github'] // Required plugins
  }
  
  async execute(context) {
    // This plugin requires cache and github plugins to be loaded
    return { message: 'Advanced functionality' }
  }
}
```

### 2. Plugin Configuration

```javascript
class ConfigurablePlugin {
  constructor() {
    this.name = 'configurable'
    this.defaultConfig = {
      timeout: 5000,
      retries: 3,
      enabled: true
    }
  }
  
  async execute(context) {
    const pluginConfig = {
      ...this.defaultConfig,
      ...context.config.plugins?.configurable
    }
    
    if (!pluginConfig.enabled) {
      return { message: 'Plugin disabled' }
    }
    
    // Use configuration
    return { config: pluginConfig }
  }
}
```

### 3. Plugin Events

```javascript
class EventPlugin {
  constructor() {
    this.name = 'events'
    this.events = ['command_executed', 'system_started']
  }
  
  async onCommandExecuted(event) {
    // Handle command execution event
    console.log('Command executed:', event.command)
  }
  
  async onSystemStarted(event) {
    // Handle system start event
    console.log('System started')
  }
}
```

## Plugin Development Guidelines

### 1. Error Handling

```javascript
async execute(context) {
  try {
    // Plugin logic
    const result = await this.processData()
    return result
  } catch (error) {
    context.logger.error('Plugin error:', error)
    
    // Return user-friendly error
    throw new Error(`Plugin failed: ${error.message}`)
  }
}
```

### 2. Performance Considerations

```javascript
async execute(context) {
  const startTime = Date.now()
  
  try {
    // Use caching for expensive operations
    const cacheKey = `plugin-${this.name}-${JSON.stringify(context.parameters)}`
    const cached = await context.cache.get(cacheKey)
    
    if (cached) {
      return cached
    }
    
    // Expensive operation
    const result = await this.expensiveOperation()
    
    // Cache result
    await context.cache.set(cacheKey, result, 300000) // 5 minutes
    
    return result
  } finally {
    const duration = Date.now() - startTime
    context.logger.performance('Plugin execution', duration, { plugin: this.name })
  }
}
```

### 3. Input Validation

```javascript
async execute(context) {
  const { parameters } = context
  
  // Validate required parameters
  if (!parameters.action) {
    throw new Error('Parameter "action" is required')
  }
  
  // Validate parameter values
  const validActions = ['start', 'stop', 'status']
  if (!validActions.includes(parameters.action)) {
    throw new Error(`Invalid action. Valid actions: ${validActions.join(', ')}`)
  }
  
  // Process with validated parameters
  return await this.processAction(parameters.action)
}
```

## Plugin Installation

### 1. File-based Plugins

Place your plugin file in the `src/nodejs/plugins/` directory:

```
src/nodejs/plugins/
├── my-plugin.js
├── another-plugin.js
└── README.md
```

### 2. NPM Package Plugins

Install as NPM packages and register them:

```bash
npm install jaegis-plugin-example
```

```javascript
// In your configuration
{
  "plugins": {
    "external": [
      "jaegis-plugin-example"
    ]
  }
}
```

## Plugin Testing

### 1. Unit Testing

```javascript
const ExamplePlugin = require('./example-plugin')

describe('ExamplePlugin', () => {
  let plugin
  let mockContext
  
  beforeEach(() => {
    plugin = new ExamplePlugin()
    mockContext = {
      parameters: {},
      logger: {
        info: jest.fn(),
        error: jest.fn()
      },
      cache: {
        get: jest.fn(),
        set: jest.fn()
      }
    }
  })
  
  test('should execute successfully', async () => {
    const result = await plugin.execute(mockContext)
    
    expect(result).toBeDefined()
    expect(result.message).toBe('Example plugin executed successfully')
  })
  
  test('should handle parameters', async () => {
    mockContext.parameters = { action: 'test' }
    
    const result = await plugin.execute(mockContext)
    
    expect(result.parameters.action).toBe('test')
  })
})
```

### 2. Integration Testing

```javascript
const { CommandExecutor } = require('../core/CommandExecutor')

describe('Plugin Integration', () => {
  let executor
  
  beforeEach(async () => {
    executor = new CommandExecutor(mockConfig)
    await executor.initialize()
  })
  
  test('should load and execute plugin', async () => {
    const result = await executor.executeCommand('example', { action: 'test' })
    
    expect(result.success).toBe(true)
    expect(result.data.message).toBe('Example plugin executed successfully')
  })
})
```

## Best Practices

1. **Keep plugins focused** - Each plugin should have a single, well-defined purpose
2. **Use descriptive names** - Plugin names should clearly indicate their functionality
3. **Provide good documentation** - Include clear descriptions, parameters, and examples
4. **Handle errors gracefully** - Always provide meaningful error messages
5. **Use caching wisely** - Cache expensive operations but be mindful of memory usage
6. **Log appropriately** - Use appropriate log levels and include relevant context
7. **Validate inputs** - Always validate and sanitize user inputs
8. **Test thoroughly** - Write comprehensive tests for your plugins
9. **Follow conventions** - Use consistent naming and structure patterns
10. **Consider performance** - Optimize for the expected usage patterns

## Plugin Registry

The JAEGIS plugin registry maintains information about all loaded plugins:

```javascript
// Get plugin information
const pluginInfo = executor.getPluginInfo('example')

// List all plugins
const allPlugins = executor.listPlugins()

// Check plugin status
const status = executor.getPluginStatus('example')
```

## Troubleshooting

### Common Issues

1. **Plugin not loading**
   - Check file syntax and exports
   - Verify plugin is in correct directory
   - Check console for error messages

2. **Plugin execution errors**
   - Review plugin logs
   - Check parameter validation
   - Verify dependencies are available

3. **Performance issues**
   - Profile plugin execution time
   - Check for memory leaks
   - Optimize expensive operations

### Debug Mode

Enable debug mode for detailed plugin information:

```javascript
{
  "system": {
    "debug": true,
    "log_level": "debug"
  }
}
```

## Contributing Plugins

To contribute plugins to the JAEGIS ecosystem:

1. Follow the plugin development guidelines
2. Include comprehensive tests
3. Provide clear documentation
4. Submit a pull request to the main repository
5. Include examples and use cases

For more information, see the [Contributing Guide](../../CONTRIBUTING.md).