/**
 * JAEGIS Response Formatter
 * Flexible response formatting system for multiple output types and contexts
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

// Response formats
const RESPONSE_FORMATS = {
  JSON: 'json',
  TEXT: 'text',
  MARKDOWN: 'markdown',
  HTML: 'html',
  TABLE: 'table',
  LIST: 'list',
  CARD: 'card',
  INTERACTIVE: 'interactive'
}

// Output contexts
const OUTPUT_CONTEXTS = {
  CLI: 'cli',
  WEB: 'web',
  API: 'api',
  WEBSOCKET: 'websocket',
  MOBILE: 'mobile',
  TERMINAL: 'terminal'
}

// Response types
const RESPONSE_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
  HELP: 'help',
  STATUS: 'status',
  DATA: 'data'
}

class ResponseFormatter {
  constructor({ config }) {
    this.config = config
    
    // Formatting templates
    this.templates = new Map()
    this.formatters = new Map()
    this.contextAdapters = new Map()
    
    // Configuration
    this.defaultFormat = config?.response?.default_format || RESPONSE_FORMATS.JSON
    this.enableColors = config?.response?.enable_colors !== false
    this.maxLength = config?.response?.max_length || 10000
    this.truncateThreshold = config?.response?.truncate_threshold || 8000
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('🎨 Initializing Response Formatter...')
    
    try {
      // Setup default templates
      this.setupDefaultTemplates()
      
      // Setup formatters
      this.setupFormatters()
      
      // Setup context adapters
      this.setupContextAdapters()
      
      this.isInitialized = true
      logger.info('✅ Response Formatter initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Response Formatter:', error)
      throw error
    }
  }

  async formatResponse(data, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Response Formatter not initialized')
    }
    
    try {
      // Normalize options
      const formatOptions = this.normalizeOptions(options)
      
      // Determine response type
      const responseType = this.determineResponseType(data, formatOptions)
      
      // Apply pre-processing
      const processedData = await this.preprocessData(data, formatOptions)
      
      // Format response
      const formattedResponse = await this.applyFormatting(processedData, formatOptions, responseType)
      
      // Apply context adaptation
      const adaptedResponse = await this.adaptForContext(formattedResponse, formatOptions)
      
      // Apply post-processing
      const finalResponse = await this.postprocessResponse(adaptedResponse, formatOptions)
      
      return finalResponse
      
    } catch (error) {
      logger.error('Response formatting error:', error)
      return this.createErrorResponse(error, options)
    }
  }

  normalizeOptions(options) {
    return {
      format: options.format || this.defaultFormat,
      context: options.context || OUTPUT_CONTEXTS.API,
      colors: options.colors !== undefined ? options.colors : this.enableColors,
      compact: options.compact || false,
      includeMetadata: options.includeMetadata !== false,
      maxLength: options.maxLength || this.maxLength,
      template: options.template || null,
      locale: options.locale || 'en',
      timezone: options.timezone || 'UTC',
      user: options.user || null,
      requestId: options.requestId || null
    }
  }

  determineResponseType(data, options) {
    if (data.success === false || data.error) {
      return RESPONSE_TYPES.ERROR
    }
    
    if (data.warning) {
      return RESPONSE_TYPES.WARNING
    }
    
    if (data.type) {
      return data.type
    }
    
    if (data.help || data.usage || data.examples) {
      return RESPONSE_TYPES.HELP
    }
    
    if (data.status || data.health) {
      return RESPONSE_TYPES.STATUS
    }
    
    return RESPONSE_TYPES.SUCCESS
  }

  async preprocessData(data, options) {
    // Clone data to avoid mutations
    let processedData = JSON.parse(JSON.stringify(data))
    
    // Add metadata if requested
    if (options.includeMetadata) {
      processedData.metadata = {
        ...processedData.metadata,
        formatted_at: new Date().toISOString(),
        format: options.format,
        context: options.context,
        request_id: options.requestId
      }
    }
    
    // Truncate large content
    processedData = this.truncateContent(processedData, options.maxLength)
    
    // Localize content
    processedData = await this.localizeContent(processedData, options.locale)
    
    return processedData
  }

  async applyFormatting(data, options, responseType) {
    const formatter = this.formatters.get(options.format)
    
    if (!formatter) {
      throw new Error(`Unknown format: ${options.format}`)
    }
    
    return await formatter(data, options, responseType)
  }

  async adaptForContext(response, options) {
    const adapter = this.contextAdapters.get(options.context)
    
    if (adapter) {
      return await adapter(response, options)
    }
    
    return response
  }

  async postprocessResponse(response, options) {
    // Apply final transformations
    let finalResponse = response
    
    // Compact mode
    if (options.compact) {
      finalResponse = this.compactResponse(finalResponse)
    }
    
    // Validate response size
    finalResponse = this.validateResponseSize(finalResponse, options.maxLength)
    
    return finalResponse
  }

  setupDefaultTemplates() {
    // Success template
    this.templates.set('success', {
      structure: {
        success: true,
        data: '{{data}}',
        message: '{{message}}',
        timestamp: '{{timestamp}}'
      },
      required: ['data'],
      optional: ['message', 'metadata']
    })
    
    // Error template
    this.templates.set('error', {
      structure: {
        success: false,
        error: {
          message: '{{error.message}}',
          type: '{{error.type}}',
          code: '{{error.code}}'
        },
        suggestions: '{{suggestions}}',
        timestamp: '{{timestamp}}'
      },
      required: ['error'],
      optional: ['suggestions', 'recovery', 'support']
    })
    
    // Help template
    this.templates.set('help', {
      structure: {
        title: '{{title}}',
        description: '{{description}}',
        usage: '{{usage}}',
        examples: '{{examples}}',
        related: '{{related}}'
      },
      required: ['title'],
      optional: ['description', 'usage', 'examples', 'related']
    })
    
    // Status template
    this.templates.set('status', {
      structure: {
        status: '{{status}}',
        system: '{{system}}',
        services: '{{services}}',
        metrics: '{{metrics}}',
        timestamp: '{{timestamp}}'
      },
      required: ['status'],
      optional: ['system', 'services', 'metrics']
    })
  }

  setupFormatters() {
    // JSON formatter
    this.formatters.set(RESPONSE_FORMATS.JSON, async (data, options, type) => {
      return {
        format: 'json',
        content: data,
        contentType: 'application/json'
      }
    })
    
    // Text formatter
    this.formatters.set(RESPONSE_FORMATS.TEXT, async (data, options, type) => {
      let text = ''
      
      switch (type) {
        case RESPONSE_TYPES.SUCCESS:
          text = this.formatSuccessText(data, options)
          break
        case RESPONSE_TYPES.ERROR:
          text = this.formatErrorText(data, options)
          break
        case RESPONSE_TYPES.HELP:
          text = this.formatHelpText(data, options)
          break
        case RESPONSE_TYPES.STATUS:
          text = this.formatStatusText(data, options)
          break
        default:
          text = this.formatGenericText(data, options)
      }
      
      return {
        format: 'text',
        content: text,
        contentType: 'text/plain'
      }
    })
    
    // Markdown formatter
    this.formatters.set(RESPONSE_FORMATS.MARKDOWN, async (data, options, type) => {
      let markdown = ''
      
      switch (type) {
        case RESPONSE_TYPES.SUCCESS:
          markdown = this.formatSuccessMarkdown(data, options)
          break
        case RESPONSE_TYPES.ERROR:
          markdown = this.formatErrorMarkdown(data, options)
          break
        case RESPONSE_TYPES.HELP:
          markdown = this.formatHelpMarkdown(data, options)
          break
        case RESPONSE_TYPES.STATUS:
          markdown = this.formatStatusMarkdown(data, options)
          break
        default:
          markdown = this.formatGenericMarkdown(data, options)
      }
      
      return {
        format: 'markdown',
        content: markdown,
        contentType: 'text/markdown'
      }
    })
    
    // HTML formatter
    this.formatters.set(RESPONSE_FORMATS.HTML, async (data, options, type) => {
      const html = this.formatHTML(data, options, type)
      
      return {
        format: 'html',
        content: html,
        contentType: 'text/html'
      }
    })
    
    // Table formatter
    this.formatters.set(RESPONSE_FORMATS.TABLE, async (data, options, type) => {
      const table = this.formatTable(data, options, type)
      
      return {
        format: 'table',
        content: table,
        contentType: 'text/plain'
      }
    })
    
    // List formatter
    this.formatters.set(RESPONSE_FORMATS.LIST, async (data, options, type) => {
      const list = this.formatList(data, options, type)
      
      return {
        format: 'list',
        content: list,
        contentType: 'text/plain'
      }
    })
    
    // Card formatter
    this.formatters.set(RESPONSE_FORMATS.CARD, async (data, options, type) => {
      const card = this.formatCard(data, options, type)
      
      return {
        format: 'card',
        content: card,
        contentType: 'application/json'
      }
    })
    
    // Interactive formatter
    this.formatters.set(RESPONSE_FORMATS.INTERACTIVE, async (data, options, type) => {
      const interactive = this.formatInteractive(data, options, type)
      
      return {
        format: 'interactive',
        content: interactive,
        contentType: 'application/json'
      }
    })
  }

  setupContextAdapters() {
    // CLI adapter
    this.contextAdapters.set(OUTPUT_CONTEXTS.CLI, async (response, options) => {
      if (response.format === 'text' || response.format === 'markdown') {
        // Add CLI-specific formatting
        if (options.colors) {
          response.content = this.addCliColors(response.content, response.format)
        }
      }
      
      return response
    })
    
    // Web adapter
    this.contextAdapters.set(OUTPUT_CONTEXTS.WEB, async (response, options) => {
      // Add web-specific metadata
      response.webMetadata = {
        responsive: true,
        theme: 'default',
        interactive: response.format === 'interactive'
      }
      
      return response
    })
    
    // API adapter
    this.contextAdapters.set(OUTPUT_CONTEXTS.API, async (response, options) => {
      // Ensure consistent API response structure
      return {
        ...response,
        apiVersion: '2.0.0',
        timestamp: new Date().toISOString(),
        requestId: options.requestId
      }
    })
    
    // WebSocket adapter
    this.contextAdapters.set(OUTPUT_CONTEXTS.WEBSOCKET, async (response, options) => {
      // Add WebSocket-specific envelope
      return {
        type: 'response',
        id: options.requestId,
        payload: response,
        timestamp: Date.now()
      }
    })
    
    // Mobile adapter
    this.contextAdapters.set(OUTPUT_CONTEXTS.MOBILE, async (response, options) => {
      // Optimize for mobile display
      if (response.content && typeof response.content === 'string') {
        response.content = this.optimizeForMobile(response.content)
      }
      
      response.mobileOptimized = true
      
      return response
    })
  }

  // Text formatting methods
  formatSuccessText(data, options) {
    let text = ''
    
    if (data.message) {
      text += `✅ ${data.message}\n`
    }
    
    if (data.data) {
      if (typeof data.data === 'string') {
        text += data.data
      } else if (typeof data.data === 'object') {
        text += this.objectToText(data.data, 0)
      }
    }
    
    return text.trim()
  }

  formatErrorText(data, options) {
    let text = `❌ Error: ${data.error?.message || data.message || 'Unknown error'}\n`
    
    if (data.error?.type) {
      text += `Type: ${data.error.type}\n`
    }
    
    if (data.error?.code) {
      text += `Code: ${data.error.code}\n`
    }
    
    if (data.suggestions && data.suggestions.length > 0) {
      text += '\n💡 Suggestions:\n'
      data.suggestions.forEach(suggestion => {
        text += `  • ${suggestion}\n`
      })
    }
    
    return text.trim()
  }

  formatHelpText(data, options) {
    let text = ''
    
    if (data.title) {
      text += `📚 ${data.title}\n`
      text += '='.repeat(data.title.length + 4) + '\n\n'
    }
    
    if (data.description) {
      text += `${data.description}\n\n`
    }
    
    if (data.usage) {
      text += `Usage: ${data.usage}\n\n`
    }
    
    if (data.examples && data.examples.length > 0) {
      text += 'Examples:\n'
      data.examples.forEach(example => {
        if (typeof example === 'string') {
          text += `  ${example}\n`
        } else {
          text += `  ${example.command} - ${example.description}\n`
        }
      })
    }
    
    return text.trim()
  }

  formatStatusText(data, options) {
    let text = `📊 System Status: ${data.status || 'Unknown'}\n\n`
    
    if (data.system) {
      text += 'System Information:\n'
      text += this.objectToText(data.system, 1)
      text += '\n'
    }
    
    if (data.services) {
      text += 'Services:\n'
      text += this.objectToText(data.services, 1)
      text += '\n'
    }
    
    if (data.metrics) {
      text += 'Metrics:\n'
      text += this.objectToText(data.metrics, 1)
    }
    
    return text.trim()
  }

  formatGenericText(data, options) {
    if (typeof data === 'string') {
      return data
    }
    
    if (data.message) {
      return data.message
    }
    
    return this.objectToText(data, 0)
  }

  // Markdown formatting methods
  formatSuccessMarkdown(data, options) {
    let markdown = ''
    
    if (data.message) {
      markdown += `## ✅ ${data.message}\n\n`
    }
    
    if (data.data) {
      if (typeof data.data === 'string') {
        markdown += data.data
      } else {
        markdown += this.objectToMarkdown(data.data)
      }
    }
    
    return markdown.trim()
  }

  formatErrorMarkdown(data, options) {
    let markdown = `## ❌ Error\n\n**${data.error?.message || data.message || 'Unknown error'}**\n\n`
    
    if (data.error?.type || data.error?.code) {
      markdown += '### Details\n\n'
      if (data.error.type) markdown += `- **Type:** ${data.error.type}\n`
      if (data.error.code) markdown += `- **Code:** ${data.error.code}\n`
      markdown += '\n'
    }
    
    if (data.suggestions && data.suggestions.length > 0) {
      markdown += '### 💡 Suggestions\n\n'
      data.suggestions.forEach(suggestion => {
        markdown += `- ${suggestion}\n`
      })
    }
    
    return markdown.trim()
  }

  formatHelpMarkdown(data, options) {
    let markdown = ''
    
    if (data.title) {
      markdown += `# 📚 ${data.title}\n\n`
    }
    
    if (data.description) {
      markdown += `${data.description}\n\n`
    }
    
    if (data.usage) {
      markdown += `## Usage\n\n\`\`\`\n${data.usage}\n\`\`\`\n\n`
    }
    
    if (data.examples && data.examples.length > 0) {
      markdown += '## Examples\n\n'
      data.examples.forEach(example => {
        if (typeof example === 'string') {
          markdown += `- \`${example}\`\n`
        } else {
          markdown += `- \`${example.command}\` - ${example.description}\n`
        }
      })
    }
    
    return markdown.trim()
  }

  formatStatusMarkdown(data, options) {
    let markdown = `# 📊 System Status: ${data.status || 'Unknown'}\n\n`
    
    if (data.system) {
      markdown += '## System Information\n\n'
      markdown += this.objectToMarkdown(data.system)
      markdown += '\n'
    }
    
    if (data.services) {
      markdown += '## Services\n\n'
      markdown += this.objectToMarkdown(data.services)
      markdown += '\n'
    }
    
    if (data.metrics) {
      markdown += '## Metrics\n\n'
      markdown += this.objectToMarkdown(data.metrics)
    }
    
    return markdown.trim()
  }

  formatGenericMarkdown(data, options) {
    if (typeof data === 'string') {
      return data
    }
    
    if (data.message) {
      return `## ${data.message}\n\n${this.objectToMarkdown(data)}`
    }
    
    return this.objectToMarkdown(data)
  }

  // HTML formatting
  formatHTML(data, options, type) {
    const className = `jaegis-response jaegis-${type}`
    
    let html = `<div class="${className}">`
    
    switch (type) {
      case RESPONSE_TYPES.SUCCESS:
        html += this.formatSuccessHTML(data, options)
        break
      case RESPONSE_TYPES.ERROR:
        html += this.formatErrorHTML(data, options)
        break
      case RESPONSE_TYPES.HELP:
        html += this.formatHelpHTML(data, options)
        break
      default:
        html += this.formatGenericHTML(data, options)
    }
    
    html += '</div>'
    
    return html
  }

  formatSuccessHTML(data, options) {
    let html = ''
    
    if (data.message) {
      html += `<div class="success-message">✅ ${this.escapeHtml(data.message)}</div>`
    }
    
    if (data.data) {
      html += `<div class="success-data">${this.objectToHTML(data.data)}</div>`
    }
    
    return html
  }

  formatErrorHTML(data, options) {
    let html = `<div class="error-message">❌ ${this.escapeHtml(data.error?.message || data.message || 'Unknown error')}</div>`
    
    if (data.suggestions && data.suggestions.length > 0) {
      html += '<div class="suggestions"><h4>💡 Suggestions:</h4><ul>'
      data.suggestions.forEach(suggestion => {
        html += `<li>${this.escapeHtml(suggestion)}</li>`
      })
      html += '</ul></div>'
    }
    
    return html
  }

  formatHelpHTML(data, options) {
    let html = ''
    
    if (data.title) {
      html += `<h2>📚 ${this.escapeHtml(data.title)}</h2>`
    }
    
    if (data.description) {
      html += `<p>${this.escapeHtml(data.description)}</p>`
    }
    
    if (data.usage) {
      html += `<div class="usage"><strong>Usage:</strong> <code>${this.escapeHtml(data.usage)}</code></div>`
    }
    
    if (data.examples && data.examples.length > 0) {
      html += '<div class="examples"><h4>Examples:</h4><ul>'
      data.examples.forEach(example => {
        if (typeof example === 'string') {
          html += `<li><code>${this.escapeHtml(example)}</code></li>`
        } else {
          html += `<li><code>${this.escapeHtml(example.command)}</code> - ${this.escapeHtml(example.description)}</li>`
        }
      })
      html += '</ul></div>'
    }
    
    return html
  }

  formatGenericHTML(data, options) {
    return this.objectToHTML(data)
  }

  // Table formatting
  formatTable(data, options, type) {
    if (Array.isArray(data.data)) {
      return this.arrayToTable(data.data)
    }
    
    if (typeof data.data === 'object') {
      return this.objectToTable(data.data)
    }
    
    return this.formatGenericText(data, options)
  }

  // List formatting
  formatList(data, options, type) {
    if (Array.isArray(data.data)) {
      return this.arrayToList(data.data)
    }
    
    if (typeof data.data === 'object') {
      return this.objectToList(data.data)
    }
    
    return this.formatGenericText(data, options)
  }

  // Card formatting
  formatCard(data, options, type) {
    return {
      type: 'card',
      title: data.title || data.message || 'JAEGIS Response',
      content: data.data || data,
      actions: data.actions || [],
      metadata: data.metadata || {}
    }
  }

  // Interactive formatting
  formatInteractive(data, options, type) {
    return {
      type: 'interactive',
      components: this.generateInteractiveComponents(data, type),
      actions: data.actions || [],
      state: data.state || {}
    }
  }

  generateInteractiveComponents(data, type) {
    const components = []
    
    switch (type) {
      case RESPONSE_TYPES.HELP:
        components.push({
          type: 'search',
          placeholder: 'Search commands...',
          action: 'search_commands'
        })
        break
      case RESPONSE_TYPES.STATUS:
        components.push({
          type: 'refresh',
          label: 'Refresh Status',
          action: 'refresh_status'
        })
        break
    }
    
    return components
  }

  // Utility methods
  objectToText(obj, indent = 0) {
    const spaces = '  '.repeat(indent)
    let text = ''
    
    for (const [key, value] of Object.entries(obj)) {
      if (typeof value === 'object' && value !== null) {
        text += `${spaces}${key}:\n${this.objectToText(value, indent + 1)}`
      } else {
        text += `${spaces}${key}: ${value}\n`
      }
    }
    
    return text
  }

  objectToMarkdown(obj) {
    let markdown = ''
    
    for (const [key, value] of Object.entries(obj)) {
      if (typeof value === 'object' && value !== null) {
        markdown += `### ${key}\n\n${this.objectToMarkdown(value)}\n`
      } else {
        markdown += `- **${key}:** ${value}\n`
      }
    }
    
    return markdown
  }

  objectToHTML(obj) {
    if (typeof obj !== 'object' || obj === null) {
      return this.escapeHtml(String(obj))
    }
    
    let html = '<dl>'
    
    for (const [key, value] of Object.entries(obj)) {
      html += `<dt>${this.escapeHtml(key)}</dt>`
      
      if (typeof value === 'object' && value !== null) {
        html += `<dd>${this.objectToHTML(value)}</dd>`
      } else {
        html += `<dd>${this.escapeHtml(String(value))}</dd>`
      }
    }
    
    html += '</dl>'
    
    return html
  }

  arrayToTable(array) {
    if (array.length === 0) return 'No data'
    
    // Simple table formatting
    const headers = Object.keys(array[0])
    let table = headers.join('\t') + '\n'
    table += headers.map(() => '---').join('\t') + '\n'
    
    array.forEach(row => {
      table += headers.map(header => row[header] || '').join('\t') + '\n'
    })
    
    return table
  }

  objectToTable(obj) {
    let table = 'Key\tValue\n---\t---\n'
    
    for (const [key, value] of Object.entries(obj)) {
      table += `${key}\t${typeof value === 'object' ? JSON.stringify(value) : value}\n`
    }
    
    return table
  }

  arrayToList(array) {
    return array.map((item, index) => `${index + 1}. ${typeof item === 'object' ? JSON.stringify(item) : item}`).join('\n')
  }

  objectToList(obj) {
    return Object.entries(obj).map(([key, value]) => `• ${key}: ${typeof value === 'object' ? JSON.stringify(value) : value}`).join('\n')
  }

  escapeHtml(text) {
    const div = { innerHTML: '' }
    div.textContent = text
    return div.innerHTML
  }

  addCliColors(text, format) {
    // Add ANSI color codes for CLI
    return text
      .replace(/✅/g, '\x1b[32m✅\x1b[0m')
      .replace(/❌/g, '\x1b[31m❌\x1b[0m')
      .replace(/💡/g, '\x1b[33m💡\x1b[0m')
      .replace(/📚/g, '\x1b[34m📚\x1b[0m')
      .replace(/📊/g, '\x1b[36m📊\x1b[0m')
  }

  optimizeForMobile(content) {
    // Optimize content for mobile display
    return content
      .replace(/\t/g, '  ') // Replace tabs with spaces
      .replace(/(.{50})/g, '$1\n') // Break long lines
  }

  truncateContent(data, maxLength) {
    const jsonString = JSON.stringify(data)
    
    if (jsonString.length <= maxLength) {
      return data
    }
    
    // Truncate and add indicator
    const truncated = JSON.parse(jsonString.substring(0, this.truncateThreshold))
    truncated._truncated = true
    truncated._originalLength = jsonString.length
    
    return truncated
  }

  async localizeContent(data, locale) {
    // Basic localization - in production you'd use a proper i18n library
    if (locale === 'en' || !locale) {
      return data
    }
    
    // Placeholder for localization
    return data
  }

  compactResponse(response) {
    // Remove unnecessary whitespace and metadata for compact mode
    if (typeof response.content === 'string') {
      response.content = response.content.replace(/\n\s*\n/g, '\n').trim()
    }
    
    return response
  }

  validateResponseSize(response, maxLength) {
    const responseString = JSON.stringify(response)
    
    if (responseString.length > maxLength) {
      return {
        ...response,
        content: 'Response too large to display',
        truncated: true,
        originalSize: responseString.length,
        maxSize: maxLength
      }
    }
    
    return response
  }

  createErrorResponse(error, options) {
    return {
      format: options.format || this.defaultFormat,
      content: {
        success: false,
        error: {
          message: 'Response formatting failed',
          details: error.message
        }
      },
      contentType: 'application/json'
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Response Formatter...')
    
    this.templates.clear()
    this.formatters.clear()
    this.contextAdapters.clear()
    
    this.isInitialized = false
    logger.info('✅ Response Formatter cleanup complete')
  }
}

module.exports = {
  ResponseFormatter,
  RESPONSE_FORMATS,
  OUTPUT_CONTEXTS,
  RESPONSE_TYPES
}