/**
 * JAEGIS Configuration Manager
 * Centralized configuration management with validation and hot-reloading
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const fs = require('fs').promises
const path = require('path')
const Joi = require('joi')
const logger = require('../utils/logger')

class ConfigManager {
  constructor() {
    this.config = null
    this.configPath = null
    this.watchers = []
    this.schema = this.createValidationSchema()
  }

  static async load(configPath = null) {
    const manager = new ConfigManager()
    await manager.loadConfig(configPath)
    return manager.config
  }

  async loadConfig(configPath = null) {
    try {
      // Determine config file path
      this.configPath = configPath || this.findConfigFile()
      
      logger.info(`⚙️ Loading configuration from: ${this.configPath}`)
      
      // Read and parse config file
      const configData = await fs.readFile(this.configPath, 'utf8')
      const rawConfig = JSON.parse(configData)
      
      // Validate configuration
      const { error, value } = this.schema.validate(rawConfig, {
        allowUnknown: true,
        stripUnknown: false
      })
      
      if (error) {
        throw new Error(`Configuration validation failed: ${error.message}`)
      }
      
      this.config = this.processConfig(value)
      
      // Apply environment variable overrides
      this.applyEnvironmentOverrides()
      
      logger.info('✅ Configuration loaded and validated successfully')
      
      return this.config
      
    } catch (error) {
      logger.error('❌ Failed to load configuration:', error)
      
      // Fall back to default configuration
      logger.warn('🔄 Falling back to default configuration')
      this.config = this.getDefaultConfig()
      
      return this.config
    }
  }

  findConfigFile() {
    const possiblePaths = [
      process.env.JAEGIS_CONFIG,
      path.join(process.cwd(), 'config/config.json'),
      path.join(process.cwd(), 'config.json'),
      path.join(__dirname, '../../../config/config.json'),
      path.join(__dirname, '../../../config/config.example.json')
    ].filter(Boolean)
    
    for (const configPath of possiblePaths) {
      try {
        require('fs').accessSync(configPath, require('fs').constants.F_OK)
        return configPath
      } catch (error) {
        // File doesn't exist, try next
      }
    }
    
    throw new Error('No configuration file found')
  }

  createValidationSchema() {
    return Joi.object({
      system: Joi.object({
        name: Joi.string().default('JAEGIS'),
        version: Joi.string().default('2.0.0'),
        environment: Joi.string().valid('development', 'production', 'test').default('development'),
        debug: Joi.boolean().default(false),
        log_level: Joi.string().valid('error', 'warn', 'info', 'debug').default('info')
      }).default(),
      
      github: Joi.object({
        commands_url: Joi.string().uri().required(),
        api_base_url: Joi.string().uri().default('https://api.github.com'),
        repository: Joi.object({
          owner: Joi.string().required(),
          name: Joi.string().required()
        }).required(),
        token: Joi.string().optional(),
        timeout: Joi.number().positive().default(30000),
        max_retries: Joi.number().positive().default(3),
        retry_delay: Joi.number().positive().default(1000),
        update_interval: Joi.number().positive().default(1800000)
      }).required(),
      
      cache: Joi.object({
        enabled: Joi.boolean().default(true),
        type: Joi.string().valid('memory', 'redis').default('memory'),
        duration: Joi.number().positive().default(3600000),
        max_size: Joi.number().positive().default(100),
        cleanup_interval: Joi.number().positive().default(300000),
        redis: Joi.object({
          host: Joi.string().default('localhost'),
          port: Joi.number().port().default(6379),
          db: Joi.number().min(0).default(0),
          password: Joi.string().optional().allow(null)
        }).default()
      }).default(),
      
      server: Joi.object({
        port: Joi.number().port().default(3000),
        host: Joi.string().default('localhost'),
        cors: Joi.object({
          enabled: Joi.boolean().default(true),
          origins: Joi.array().items(Joi.string()).default(['http://localhost:3000'])
        }).default(),
        rate_limiting: Joi.object({
          enabled: Joi.boolean().default(true),
          window_ms: Joi.number().positive().default(900000),
          max_requests: Joi.number().positive().default(100)
        }).default()
      }).default(),
      
      python_integration: Joi.object({
        enabled: Joi.boolean().default(true),
        python_path: Joi.string().default('python3'),
        script_timeout: Joi.number().positive().default(60000),
        max_memory: Joi.string().default('512MB'),
        communication: Joi.object({
          type: Joi.string().valid('http', 'socket').default('http'),
          port: Joi.number().port().default(5000),
          host: Joi.string().default('localhost')
        }).default(),
        timeout: Joi.number().positive().default(30000),
        max_retries: Joi.number().positive().default(3),
        log_level: Joi.string().valid('error', 'warn', 'info', 'debug').default('info')
      }).default(),
      
      commands: Joi.object({
        prefix: Joi.string().default('/'),
        case_sensitive: Joi.boolean().default(false),
        auto_complete: Joi.boolean().default(true),
        history_size: Joi.number().positive().default(100),
        aliases: Joi.object().pattern(Joi.string(), Joi.string()).default({
          h: 'help',
          c: 'config',
          s: 'status',
          a: 'agents'
        })
      }).default(),
      
      processing: Joi.object({
        max_concurrent_commands: Joi.number().positive().default(5),
        command_timeout: Joi.number().positive().default(30000),
        queue_size: Joi.number().positive().default(50),
        priority_levels: Joi.array().items(Joi.string()).default(['emergency', 'high', 'normal', 'low']),
        default_priority: Joi.string().default('normal'),
        max_command_length: Joi.number().positive().default(1000)
      }).default(),
      
      monitoring: Joi.object({
        enabled: Joi.boolean().default(true),
        metrics: Joi.object({
          performance: Joi.boolean().default(true),
          usage: Joi.boolean().default(true),
          errors: Joi.boolean().default(true),
          health: Joi.boolean().default(true)
        }).default(),
        alerts: Joi.object({
          enabled: Joi.boolean().default(true),
          thresholds: Joi.object({
            response_time: Joi.number().positive().default(5000),
            error_rate: Joi.number().min(0).max(1).default(0.05),
            memory_usage: Joi.number().min(0).max(1).default(0.8),
            cpu_usage: Joi.number().min(0).max(1).default(0.8)
          }).default()
        }).default()
      }).default(),
      
      security: Joi.object({
        encryption: Joi.object({
          enabled: Joi.boolean().default(true),
          algorithm: Joi.string().default('aes-256-gcm')
        }).default(),
        authentication: Joi.object({
          required: Joi.boolean().default(false),
          type: Joi.string().valid('token', 'jwt').default('token'),
          token_expiry: Joi.number().positive().default(86400000)
        }).default(),
        input_validation: Joi.object({
          enabled: Joi.boolean().default(true),
          max_input_length: Joi.number().positive().default(10000),
          sanitize_html: Joi.boolean().default(true)
        }).default()
      }).default()
    })
  }

  processConfig(config) {
    // Process and normalize configuration values
    const processed = { ...config }
    
    // Ensure URLs don't have trailing slashes
    if (processed.github.api_base_url.endsWith('/')) {
      processed.github.api_base_url = processed.github.api_base_url.slice(0, -1)
    }
    
    // Set derived values
    processed.python_integration.communication.url = 
      `http://${processed.python_integration.communication.host}:${processed.python_integration.communication.port}`
    
    // Process environment-specific settings
    if (processed.system.environment === 'production') {
      processed.system.debug = false
      processed.system.log_level = 'warn'
    }
    
    return processed
  }

  applyEnvironmentOverrides() {
    const envMappings = {
      'JAEGIS_PORT': 'server.port',
      'JAEGIS_HOST': 'server.host',
      'JAEGIS_LOG_LEVEL': 'system.log_level',
      'JAEGIS_DEBUG': 'system.debug',
      'JAEGIS_GITHUB_TOKEN': 'github.token',
      'JAEGIS_GITHUB_COMMANDS_URL': 'github.commands_url',
      'JAEGIS_CACHE_ENABLED': 'cache.enabled',
      'JAEGIS_CACHE_TYPE': 'cache.type',
      'JAEGIS_REDIS_HOST': 'cache.redis.host',
      'JAEGIS_REDIS_PORT': 'cache.redis.port',
      'JAEGIS_PYTHON_ENABLED': 'python_integration.enabled',
      'JAEGIS_PYTHON_PORT': 'python_integration.communication.port',
      'JAEGIS_PYTHON_HOST': 'python_integration.communication.host'
    }
    
    for (const [envVar, configPath] of Object.entries(envMappings)) {
      const envValue = process.env[envVar]
      if (envValue !== undefined) {
        this.setNestedValue(this.config, configPath, this.parseEnvValue(envValue))
        logger.debug(`Applied environment override: ${envVar} -> ${configPath}`)
      }
    }
  }

  parseEnvValue(value) {
    // Parse environment variable values to appropriate types
    if (value === 'true') return true
    if (value === 'false') return false
    if (/^\d+$/.test(value)) return parseInt(value, 10)
    if (/^\d+\.\d+$/.test(value)) return parseFloat(value)
    return value
  }

  setNestedValue(obj, path, value) {
    const keys = path.split('.')
    let current = obj
    
    for (let i = 0; i < keys.length - 1; i++) {
      const key = keys[i]
      if (!(key in current) || typeof current[key] !== 'object') {
        current[key] = {}
      }
      current = current[key]
    }
    
    current[keys[keys.length - 1]] = value
  }

  getDefaultConfig() {
    return {
      system: {
        name: 'JAEGIS',
        version: '2.0.0',
        environment: 'development',
        debug: true,
        log_level: 'info'
      },
      github: {
        commands_url: 'https://raw.githubusercontent.com/usemanusai/JAEGIS/main/commands/commands.md',
        api_base_url: 'https://api.github.com',
        repository: {
          owner: 'usemanusai',
          name: 'JAEGIS'
        },
        timeout: 30000,
        max_retries: 3,
        retry_delay: 1000,
        update_interval: 1800000
      },
      cache: {
        enabled: true,
        type: 'memory',
        duration: 3600000,
        max_size: 100,
        cleanup_interval: 300000,
        redis: {
          host: 'localhost',
          port: 6379,
          db: 0,
          password: null
        }
      },
      server: {
        port: 3000,
        host: 'localhost',
        cors: {
          enabled: true,
          origins: ['http://localhost:3000']
        },
        rate_limiting: {
          enabled: true,
          window_ms: 900000,
          max_requests: 100
        }
      },
      python_integration: {
        enabled: true,
        python_path: 'python3',
        script_timeout: 60000,
        max_memory: '512MB',
        communication: {
          type: 'http',
          port: 5000,
          host: 'localhost',
          url: 'http://localhost:5000'
        },
        timeout: 30000,
        max_retries: 3,
        log_level: 'info'
      },
      commands: {
        prefix: '/',
        case_sensitive: false,
        auto_complete: true,
        history_size: 100,
        aliases: {
          h: 'help',
          c: 'config',
          s: 'status',
          a: 'agents'
        }
      },
      processing: {
        max_concurrent_commands: 5,
        command_timeout: 30000,
        queue_size: 50,
        priority_levels: ['emergency', 'high', 'normal', 'low'],
        default_priority: 'normal',
        max_command_length: 1000
      },
      monitoring: {
        enabled: true,
        metrics: {
          performance: true,
          usage: true,
          errors: true,
          health: true
        },
        alerts: {
          enabled: true,
          thresholds: {
            response_time: 5000,
            error_rate: 0.05,
            memory_usage: 0.8,
            cpu_usage: 0.8
          }
        }
      },
      security: {
        encryption: {
          enabled: true,
          algorithm: 'aes-256-gcm'
        },
        authentication: {
          required: false,
          type: 'token',
          token_expiry: 86400000
        },
        input_validation: {
          enabled: true,
          max_input_length: 10000,
          sanitize_html: true
        }
      }
    }
  }

  async saveConfig(configPath = null) {
    try {
      const savePath = configPath || this.configPath
      const configData = JSON.stringify(this.config, null, 2)
      
      await fs.writeFile(savePath, configData, 'utf8')
      logger.info(`✅ Configuration saved to: ${savePath}`)
      
    } catch (error) {
      logger.error('❌ Failed to save configuration:', error)
      throw error
    }
  }

  get(path, defaultValue = undefined) {
    const keys = path.split('.')
    let current = this.config
    
    for (const key of keys) {
      if (current && typeof current === 'object' && key in current) {
        current = current[key]
      } else {
        return defaultValue
      }
    }
    
    return current
  }

  set(path, value) {
    this.setNestedValue(this.config, path, value)
  }

  validate() {
    const { error } = this.schema.validate(this.config)
    if (error) {
      throw new Error(`Configuration validation failed: ${error.message}`)
    }
    return true
  }

  reload() {
    return this.loadConfig(this.configPath)
  }

  getPublicConfig() {
    // Return configuration safe for public consumption (no secrets)
    return {
      system: {
        name: this.config.system.name,
        version: this.config.system.version,
        environment: this.config.system.environment
      },
      commands: this.config.commands,
      features: {
        cache_enabled: this.config.cache.enabled,
        python_integration: this.config.python_integration.enabled,
        monitoring: this.config.monitoring.enabled
      }
    }
  }
}

module.exports = ConfigManager