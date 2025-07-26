/**
 * JAEGIS Python Bridge
 * Communication bridge between Node.js and Python services
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const axios = require('axios')
const { spawn } = require('child_process')
const path = require('path')
const fs = require('fs').promises
const logger = require('../utils/logger')

class PythonBridge {
  constructor(config) {
    this.config = config
    this.pythonProcess = null
    this.httpClient = null
    this.isInitialized = false
    this.healthCheckInterval = null
    this.retryCount = 0
    this.maxRetries = config.max_retries || 3
    this.baseUrl = `http://${config.communication.host}:${config.communication.port}`
  }

  async initialize() {
    logger.info('🐍 Initializing Python Bridge...')
    
    try {
      // Start Python service if not running
      if (this.config.enabled) {
        await this.startPythonService()
        await this.setupHttpClient()
        await this.waitForPythonService()
        this.setupHealthCheck()
      }
      
      this.isInitialized = true
      logger.info('✅ Python Bridge initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Python Bridge:', error)
      throw error
    }
  }

  async startPythonService() {
    if (this.pythonProcess) {
      logger.info('Python service already running')
      return
    }
    
    logger.info('🚀 Starting Python service...')
    
    const pythonPath = this.config.python_path || 'python3'
    const scriptPath = path.join(__dirname, '../../python/api/main.py')
    
    // Check if Python script exists
    try {
      await fs.access(scriptPath)
    } catch (error) {
      throw new Error(`Python script not found: ${scriptPath}`)
    }
    
    // Spawn Python process
    this.pythonProcess = spawn(pythonPath, [scriptPath], {
      env: {
        ...process.env,
        JAEGIS_PORT: this.config.communication.port.toString(),
        JAEGIS_HOST: this.config.communication.host,
        JAEGIS_LOG_LEVEL: this.config.log_level || 'info',
        PYTHONPATH: path.join(__dirname, '../../python')
      },
      stdio: ['pipe', 'pipe', 'pipe']
    })
    
    // Handle Python process events
    this.pythonProcess.stdout.on('data', (data) => {
      const output = data.toString().trim()
      if (output) {
        logger.debug(`Python stdout: ${output}`)
      }
    })
    
    this.pythonProcess.stderr.on('data', (data) => {
      const error = data.toString().trim()
      if (error && !error.includes('INFO') && !error.includes('DEBUG')) {
        logger.warn(`Python stderr: ${error}`)
      }
    })
    
    this.pythonProcess.on('close', (code) => {
      logger.warn(`Python process exited with code ${code}`)
      this.pythonProcess = null
      
      // Auto-restart if unexpected exit
      if (this.isInitialized && code !== 0) {
        logger.info('Attempting to restart Python service...')
        setTimeout(() => this.startPythonService(), 5000)
      }
    })
    
    this.pythonProcess.on('error', (error) => {
      logger.error('Python process error:', error)
      this.pythonProcess = null
    })
    
    logger.info(`Python service started with PID: ${this.pythonProcess.pid}`)
  }

  setupHttpClient() {
    this.httpClient = axios.create({
      baseURL: this.baseUrl,
      timeout: this.config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'JAEGIS-NodeJS-Bridge/2.0.0',
        'X-Source': 'nodejs-bridge'
      }
    })
    
    // Request interceptor
    this.httpClient.interceptors.request.use(
      (config) => {
        logger.debug(`Python API request: ${config.method.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        logger.error('Python API request error:', error)
        return Promise.reject(error)
      }
    )
    
    // Response interceptor
    this.httpClient.interceptors.response.use(
      (response) => {
        logger.debug(`Python API response: ${response.status} ${response.config.url}`)
        return response
      },
      (error) => {
        logger.error('Python API response error:', error.message)
        return Promise.reject(error)
      }
    )
  }

  async waitForPythonService(maxWaitTime = 30000) {
    const startTime = Date.now()
    const checkInterval = 1000
    
    logger.info('⏳ Waiting for Python service to be ready...')
    
    while (Date.now() - startTime < maxWaitTime) {
      try {
        const response = await this.httpClient.get('/health')
        if (response.status === 200) {
          logger.info('✅ Python service is ready')
          return
        }
      } catch (error) {
        // Service not ready yet, continue waiting
      }
      
      await new Promise(resolve => setTimeout(resolve, checkInterval))
    }
    
    throw new Error('Python service failed to start within timeout period')
  }

  setupHealthCheck() {
    this.healthCheckInterval = setInterval(async () => {
      try {
        await this.healthCheck()
      } catch (error) {
        logger.warn('Python service health check failed:', error.message)
      }
    }, 30000) // Check every 30 seconds
  }

  async healthCheck() {
    if (!this.config.enabled) {
      return {
        status: 'disabled',
        message: 'Python integration is disabled'
      }
    }
    
    try {
      const response = await this.httpClient.get('/health')
      return {
        status: 'healthy',
        data: response.data,
        responseTime: response.headers['x-response-time']
      }
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        code: error.code
      }
    }
  }

  async fetchGitHubCommands(url) {
    logger.info(`📥 Fetching GitHub commands from: ${url}`)
    
    try {
      const response = await this.httpClient.post('/github/fetch', {
        url: url,
        cache: true,
        parse: false
      })
      
      if (response.data.success) {
        logger.info('✅ GitHub commands fetched successfully')
        return response.data
      } else {
        throw new Error(response.data.error || 'Unknown error')
      }
      
    } catch (error) {
      logger.error('GitHub fetch error:', error)
      
      // Retry logic
      if (this.retryCount < this.maxRetries) {
        this.retryCount++
        logger.info(`Retrying GitHub fetch (${this.retryCount}/${this.maxRetries})...`)
        await new Promise(resolve => setTimeout(resolve, 1000 * this.retryCount))
        return this.fetchGitHubCommands(url)
      }
      
      this.retryCount = 0
      throw new Error(`Failed to fetch GitHub commands: ${error.message}`)
    }
  }

  async parseMarkdownCommands(content) {
    logger.info('📝 Parsing markdown commands...')
    
    try {
      const response = await this.httpClient.post('/processing/parse-commands', {
        content: content,
        format: 'markdown',
        extract_metadata: true
      })
      
      if (response.data.success) {
        logger.info(`✅ Parsed ${response.data.data.commands?.length || 0} commands`)
        return response.data
      } else {
        throw new Error(response.data.error || 'Parsing failed')
      }
      
    } catch (error) {
      logger.error('Markdown parsing error:', error)
      throw new Error(`Failed to parse markdown commands: ${error.message}`)
    }
  }

  async analyzeContent(content, options = {}) {
    logger.info('🔍 Analyzing content...')
    
    try {
      const response = await this.httpClient.post('/processing/analyze', {
        content: content,
        options: {
          extract_commands: true,
          analyze_structure: true,
          generate_summary: true,
          ...options
        }
      })
      
      return response.data
      
    } catch (error) {
      logger.error('Content analysis error:', error)
      throw new Error(`Failed to analyze content: ${error.message}`)
    }
  }

  async generateSuggestions(query, context = {}) {
    logger.info(`💡 Generating suggestions for: ${query}`)
    
    try {
      const response = await this.httpClient.post('/ai/suggestions', {
        query: query,
        context: context,
        max_suggestions: 10
      })
      
      return response.data
      
    } catch (error) {
      logger.error('Suggestion generation error:', error)
      throw new Error(`Failed to generate suggestions: ${error.message}`)
    }
  }

  async validateCommand(command, commandsData) {
    logger.info(`✅ Validating command: ${command}`)
    
    try {
      const response = await this.httpClient.post('/processing/validate', {
        command: command,
        commands_data: commandsData,
        strict: true
      })
      
      return response.data
      
    } catch (error) {
      logger.error('Command validation error:', error)
      throw new Error(`Failed to validate command: ${error.message}`)
    }
  }

  async processAIRequest(request) {
    logger.info('🤖 Processing AI request...')
    
    try {
      const response = await this.httpClient.post('/ai/process', request)
      return response.data
      
    } catch (error) {
      logger.error('AI processing error:', error)
      throw new Error(`Failed to process AI request: ${error.message}`)
    }
  }

  async getCacheStats() {
    try {
      const response = await this.httpClient.get('/cache/stats')
      return response.data
    } catch (error) {
      logger.error('Cache stats error:', error)
      return { error: error.message }
    }
  }

  async clearCache(pattern = null) {
    try {
      const response = await this.httpClient.post('/cache/clear', {
        pattern: pattern
      })
      return response.data
    } catch (error) {
      logger.error('Cache clear error:', error)
      throw new Error(`Failed to clear cache: ${error.message}`)
    }
  }

  async getMetrics() {
    try {
      const response = await this.httpClient.get('/metrics')
      return response.data
    } catch (error) {
      logger.error('Metrics error:', error)
      return { error: error.message }
    }
  }

  async executeScript(script, parameters = {}) {
    logger.info('📜 Executing Python script...')
    
    try {
      const response = await this.httpClient.post('/execute/script', {
        script: script,
        parameters: parameters,
        timeout: this.config.script_timeout || 60000
      })
      
      return response.data
      
    } catch (error) {
      logger.error('Script execution error:', error)
      throw new Error(`Failed to execute script: ${error.message}`)
    }
  }

  async testConnection() {
    try {
      const response = await this.httpClient.get('/test')
      return {
        success: true,
        data: response.data,
        responseTime: response.headers['x-response-time']
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      }
    }
  }

  getStatus() {
    return {
      enabled: this.config.enabled,
      initialized: this.isInitialized,
      processRunning: !!this.pythonProcess,
      processPid: this.pythonProcess?.pid,
      baseUrl: this.baseUrl,
      retryCount: this.retryCount,
      maxRetries: this.maxRetries
    }
  }

  async restart() {
    logger.info('🔄 Restarting Python service...')
    
    try {
      await this.cleanup()
      await new Promise(resolve => setTimeout(resolve, 2000))
      await this.initialize()
      logger.info('✅ Python service restarted successfully')
    } catch (error) {
      logger.error('Failed to restart Python service:', error)
      throw error
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Python Bridge...')
    
    // Clear health check interval
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval)
      this.healthCheckInterval = null
    }
    
    // Terminate Python process
    if (this.pythonProcess) {
      logger.info('Terminating Python process...')
      
      // Try graceful shutdown first
      try {
        await this.httpClient.post('/shutdown')
        await new Promise(resolve => setTimeout(resolve, 2000))
      } catch (error) {
        // Ignore errors during graceful shutdown
      }
      
      // Force kill if still running
      if (this.pythonProcess && !this.pythonProcess.killed) {
        this.pythonProcess.kill('SIGTERM')
        
        // Force kill after timeout
        setTimeout(() => {
          if (this.pythonProcess && !this.pythonProcess.killed) {
            this.pythonProcess.kill('SIGKILL')
          }
        }, 5000)
      }
      
      this.pythonProcess = null
    }
    
    this.isInitialized = false
    this.retryCount = 0
    
    logger.info('✅ Python Bridge cleanup complete')
  }
}

module.exports = PythonBridge