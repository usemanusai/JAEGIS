/**
 * JAEGIS Help System
 * Intelligent contextual help and documentation system
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

class HelpSystem {
  constructor({ config, cache, pythonBridge, commandExecutor }) {
    this.config = config
    this.cache = cache
    this.pythonBridge = pythonBridge
    this.commandExecutor = commandExecutor
    
    // Help content storage
    this.helpContent = new Map()
    this.tutorials = new Map()
    this.examples = new Map()
    this.faq = new Map()
    
    // Context tracking
    this.userContexts = new Map()
    this.helpHistory = []
    this.searchIndex = new Map()
    
    // Help categories
    this.categories = {
      'getting-started': 'Getting Started',
      'commands': 'Command Reference',
      'configuration': 'Configuration',
      'troubleshooting': 'Troubleshooting',
      'advanced': 'Advanced Features',
      'api': 'API Reference',
      'examples': 'Examples & Tutorials'
    }
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('📚 Initializing Help System...')
    
    try {
      // Load help content
      await this.loadHelpContent()
      
      // Build search index
      await this.buildSearchIndex()
      
      // Load tutorials and examples
      await this.loadTutorials()
      await this.loadExamples()
      
      // Load FAQ
      await this.loadFAQ()
      
      this.isInitialized = true
      logger.info(`✅ Help System initialized with ${this.helpContent.size} help topics`)
      
    } catch (error) {
      logger.error('❌ Failed to initialize Help System:', error)
      throw error
    }
  }

  async loadHelpContent() {
    // Core help topics
    const coreTopics = [
      {
        id: 'overview',
        title: 'JAEGIS Overview',
        category: 'getting-started',
        content: this.createOverviewHelp(),
        keywords: ['overview', 'introduction', 'what is', 'about']
      },
      {
        id: 'quick-start',
        title: 'Quick Start Guide',
        category: 'getting-started',
        content: this.createQuickStartHelp(),
        keywords: ['quick start', 'getting started', 'begin', 'start']
      },
      {
        id: 'commands',
        title: 'Command Reference',
        category: 'commands',
        content: await this.createCommandReferenceHelp(),
        keywords: ['commands', 'reference', 'list', 'available']
      },
      {
        id: 'configuration',
        title: 'Configuration Guide',
        category: 'configuration',
        content: this.createConfigurationHelp(),
        keywords: ['config', 'configuration', 'settings', 'setup']
      },
      {
        id: 'agents',
        title: 'Agent System Guide',
        category: 'advanced',
        content: this.createAgentSystemHelp(),
        keywords: ['agents', 'squads', 'coordination', 'ai']
      },
      {
        id: 'troubleshooting',
        title: 'Troubleshooting Guide',
        category: 'troubleshooting',
        content: this.createTroubleshootingHelp(),
        keywords: ['troubleshooting', 'problems', 'issues', 'errors', 'debug']
      },
      {
        id: 'api',
        title: 'API Reference',
        category: 'api',
        content: this.createAPIReferenceHelp(),
        keywords: ['api', 'endpoints', 'rest', 'websocket']
      }
    ]
    
    // Store help topics
    coreTopics.forEach(topic => {
      this.helpContent.set(topic.id, topic)
    })
    
    // Try to load additional help from GitHub
    try {
      await this.loadHelpFromGitHub()
    } catch (error) {
      logger.warn('Failed to load help from GitHub:', error.message)
    }
  }

  async loadHelpFromGitHub() {
    try {
      // Fetch help content from GitHub repository
      const helpUrl = `${this.config.github.commands_url.replace('commands.md', 'docs/help.md')}`
      const response = await this.pythonBridge.fetchGitHubCommands(helpUrl)
      
      if (response.success) {
        const parsedHelp = await this.parseHelpMarkdown(response.data.content)
        
        parsedHelp.forEach(topic => {
          this.helpContent.set(topic.id, topic)
        })
        
        logger.info(`📥 Loaded ${parsedHelp.length} help topics from GitHub`)
      }
    } catch (error) {
      // Silently fail - GitHub help is optional
      logger.debug('GitHub help loading failed:', error.message)
    }
  }

  async parseHelpMarkdown(content) {
    try {
      const response = await this.pythonBridge.parseMarkdownCommands(content)
      
      if (response.success) {
        // Convert parsed content to help topics
        return response.data.commands.map(cmd => ({
          id: cmd.name,
          title: cmd.description,
          category: cmd.category || 'commands',
          content: {
            description: cmd.description,
            usage: cmd.usage,
            examples: cmd.examples,
            parameters: cmd.parameters
          },
          keywords: [cmd.name, ...cmd.aliases]
        }))
      }
    } catch (error) {
      logger.error('Failed to parse help markdown:', error)
    }
    
    return []
  }

  async buildSearchIndex() {
    this.searchIndex.clear()
    
    for (const [id, topic] of this.helpContent) {
      // Index title
      this.indexText(topic.title, id, 'title', 10)
      
      // Index keywords
      topic.keywords.forEach(keyword => {
        this.indexText(keyword, id, 'keyword', 8)
      })
      
      // Index content
      if (typeof topic.content === 'string') {
        this.indexText(topic.content, id, 'content', 5)
      } else if (typeof topic.content === 'object') {
        Object.values(topic.content).forEach(value => {
          if (typeof value === 'string') {
            this.indexText(value, id, 'content', 3)
          }
        })
      }
    }
    
    logger.info(`🔍 Built search index with ${this.searchIndex.size} terms`)
  }

  indexText(text, topicId, type, weight) {
    const words = text.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2)
    
    words.forEach(word => {
      if (!this.searchIndex.has(word)) {
        this.searchIndex.set(word, [])
      }
      
      this.searchIndex.get(word).push({
        topicId,
        type,
        weight
      })
    })
  }

  async getHelp(query, context = {}) {
    if (!this.isInitialized) {
      throw new Error('Help System not initialized')
    }
    
    try {
      logger.info(`📚 Getting help for: ${query}`)
      
      // Track user context
      this.updateUserContext(context.user || 'anonymous', query)
      
      // Determine help type
      const helpType = this.determineHelpType(query, context)
      
      let result
      
      switch (helpType) {
        case 'command':
          result = await this.getCommandHelp(query, context)
          break
        case 'topic':
          result = await this.getTopicHelp(query, context)
          break
        case 'search':
          result = await this.searchHelp(query, context)
          break
        case 'contextual':
          result = await this.getContextualHelp(query, context)
          break
        default:
          result = await this.getGeneralHelp(context)
      }
      
      // Add contextual suggestions
      result.suggestions = await this.generateSuggestions(query, context)
      
      // Record help request
      this.recordHelpRequest(query, helpType, result, context)
      
      return result
      
    } catch (error) {
      logger.error('Help system error:', error)
      return this.getErrorHelp(error, query)
    }
  }

  determineHelpType(query, context) {
    const queryLower = query.toLowerCase().trim()
    
    // Check if it's a command help request
    if (queryLower.startsWith('/') || this.commandExecutor.plugins.has(queryLower)) {
      return 'command'
    }
    
    // Check if it's a specific topic
    if (this.helpContent.has(queryLower)) {
      return 'topic'
    }
    
    // Check for contextual help indicators
    const contextualIndicators = ['how to', 'how do i', 'what is', 'explain', 'show me']
    if (contextualIndicators.some(indicator => queryLower.includes(indicator))) {
      return 'contextual'
    }
    
    // Default to search
    return 'search'
  }

  async getCommandHelp(query, context) {
    const command = query.replace(/^\/+/, '').toLowerCase()
    const plugin = this.commandExecutor.plugins.get(command)
    
    if (!plugin) {
      return {
        type: 'command_not_found',
        query,
        message: `Command '${command}' not found`,
        available_commands: Array.from(this.commandExecutor.plugins.keys()).slice(0, 10)
      }
    }
    
    return {
      type: 'command_help',
      command,
      title: `Help for /${command}`,
      description: plugin.description || 'No description available',
      usage: plugin.usage || `/${command}`,
      parameters: plugin.parameters || [],
      examples: plugin.examples || [],
      category: plugin.category || 'general',
      related_commands: this.getRelatedCommands(command)
    }
  }

  async getTopicHelp(query, context) {
    const topic = this.helpContent.get(query.toLowerCase())
    
    if (!topic) {
      return await this.searchHelp(query, context)
    }
    
    return {
      type: 'topic_help',
      topic: topic.id,
      title: topic.title,
      category: topic.category,
      content: topic.content,
      related_topics: this.getRelatedTopics(topic.id)
    }
  }

  async searchHelp(query, context) {
    const results = this.performSearch(query)
    
    return {
      type: 'search_results',
      query,
      results: results.slice(0, 10),
      total_results: results.length,
      categories: this.getSearchCategories(results)
    }
  }

  performSearch(query) {
    const queryWords = query.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2)
    
    const scores = new Map()
    
    queryWords.forEach(word => {
      const matches = this.searchIndex.get(word) || []
      
      matches.forEach(match => {
        const currentScore = scores.get(match.topicId) || 0
        scores.set(match.topicId, currentScore + match.weight)
      })
    })
    
    // Convert to results array and sort by score
    const results = Array.from(scores.entries())
      .map(([topicId, score]) => {
        const topic = this.helpContent.get(topicId)
        return {
          id: topicId,
          title: topic.title,
          category: topic.category,
          score,
          snippet: this.generateSnippet(topic, query)
        }
      })
      .sort((a, b) => b.score - a.score)
    
    return results
  }

  generateSnippet(topic, query) {
    const content = typeof topic.content === 'string' 
      ? topic.content 
      : JSON.stringify(topic.content)
    
    const queryWords = query.toLowerCase().split(/\s+/)
    const sentences = content.split(/[.!?]+/)
    
    // Find sentence with most query words
    let bestSentence = sentences[0] || ''
    let maxMatches = 0
    
    sentences.forEach(sentence => {
      const matches = queryWords.filter(word => 
        sentence.toLowerCase().includes(word)
      ).length
      
      if (matches > maxMatches) {
        maxMatches = matches
        bestSentence = sentence
      }
    })
    
    return bestSentence.trim().substring(0, 200) + '...'
  }

  async getContextualHelp(query, context) {
    // Analyze query for intent
    const intent = this.analyzeIntent(query)
    
    switch (intent) {
      case 'how_to':
        return await this.getHowToHelp(query, context)
      case 'what_is':
        return await this.getDefinitionHelp(query, context)
      case 'troubleshoot':
        return await this.getTroubleshootingHelp(query, context)
      default:
        return await this.searchHelp(query, context)
    }
  }

  analyzeIntent(query) {
    const queryLower = query.toLowerCase()
    
    if (queryLower.includes('how to') || queryLower.includes('how do i')) {
      return 'how_to'
    }
    
    if (queryLower.includes('what is') || queryLower.includes('what are')) {
      return 'what_is'
    }
    
    if (queryLower.includes('error') || queryLower.includes('problem') || queryLower.includes('issue')) {
      return 'troubleshoot'
    }
    
    return 'general'
  }

  async getHowToHelp(query, context) {
    // Extract the action from "how to" query
    const action = query.toLowerCase()
      .replace(/how\s+to\s+/, '')
      .replace(/how\s+do\s+i\s+/, '')
    
    // Search for relevant tutorials
    const tutorials = this.searchTutorials(action)
    
    return {
      type: 'how_to_help',
      query,
      action,
      tutorials,
      quick_steps: this.generateQuickSteps(action),
      related_commands: this.findCommandsForAction(action)
    }
  }

  async getDefinitionHelp(query, context) {
    // Extract the term from "what is" query
    const term = query.toLowerCase()
      .replace(/what\s+is\s+/, '')
      .replace(/what\s+are\s+/, '')
    
    // Look for definitions
    const definition = this.findDefinition(term)
    
    return {
      type: 'definition_help',
      query,
      term,
      definition,
      related_topics: this.getRelatedTopics(term)
    }
  }

  async getTroubleshootingHelp(query, context) {
    // Analyze error or problem
    const issue = this.analyzeIssue(query)
    
    return {
      type: 'troubleshooting_help',
      query,
      issue,
      solutions: this.findSolutions(issue),
      diagnostic_steps: this.getDiagnosticSteps(issue),
      related_faq: this.getRelatedFAQ(issue)
    }
  }

  async getGeneralHelp(context) {
    return {
      type: 'general_help',
      title: 'JAEGIS Help System',
      description: 'AI Agent Intelligence System - Interactive Help',
      categories: this.categories,
      popular_topics: this.getPopularTopics(),
      recent_updates: this.getRecentUpdates(),
      quick_links: {
        'Getting Started': 'quick-start',
        'Command Reference': 'commands',
        'Troubleshooting': 'troubleshooting',
        'Examples': 'examples'
      }
    }
  }

  // Content creation methods
  createOverviewHelp() {
    return {
      description: 'JAEGIS is an AI Agent Intelligence System that provides intelligent command processing with GitHub integration.',
      key_features: [
        'Dynamic command processing from GitHub repository',
        'Intelligent agent squad coordination',
        'Hybrid Node.js + Python architecture',
        'Real-time caching and performance optimization',
        'Interactive CLI and WebSocket support'
      ],
      architecture: 'Hybrid system combining Node.js for performance and Python for AI capabilities',
      use_cases: [
        'Command automation and processing',
        'Documentation generation',
        'System monitoring and analytics',
        'Agent coordination and management'
      ]
    }
  }

  createQuickStartHelp() {
    return {
      description: 'Get started with JAEGIS in minutes',
      steps: [
        {
          step: 1,
          title: 'Installation',
          command: 'git clone https://github.com/usemanusai/JAEGIS.git',
          description: 'Clone the repository'
        },
        {
          step: 2,
          title: 'Setup Dependencies',
          command: 'npm install && pip install -r requirements.txt',
          description: 'Install Node.js and Python dependencies'
        },
        {
          step: 3,
          title: 'Configuration',
          command: 'cp config/config.example.json config/config.json',
          description: 'Copy and customize configuration'
        },
        {
          step: 4,
          title: 'Start Services',
          command: 'npm start',
          description: 'Start the JAEGIS server'
        },
        {
          step: 5,
          title: 'Use CLI',
          command: 'node src/nodejs/cli.js interactive',
          description: 'Start interactive mode'
        }
      ],
      first_commands: [
        '/help - Show available commands',
        '/status - Check system status',
        '/agents - View agent squads'
      ]
    }
  }

  async createCommandReferenceHelp() {
    const commands = Array.from(this.commandExecutor.plugins.entries()).map(([name, plugin]) => ({
      name,
      description: plugin.description || 'No description available',
      usage: plugin.usage || `/${name}`,
      category: plugin.category || 'general',
      parameters: plugin.parameters || []
    }))
    
    // Group by category
    const groupedCommands = {}
    commands.forEach(cmd => {
      if (!groupedCommands[cmd.category]) {
        groupedCommands[cmd.category] = []
      }
      groupedCommands[cmd.category].push(cmd)
    })
    
    return {
      description: 'Complete reference of all available JAEGIS commands',
      total_commands: commands.length,
      categories: groupedCommands,
      usage_notes: [
        'Commands can be prefixed with / or used without',
        'Use /help <command> for detailed help on specific commands',
        'Parameters in [brackets] are optional, <brackets> are required'
      ]
    }
  }

  createConfigurationHelp() {
    return {
      description: 'Guide to configuring JAEGIS system',
      config_file: 'config/config.json',
      main_sections: {
        system: 'Basic system settings (name, version, environment)',
        github: 'GitHub integration settings (repository, token, URLs)',
        cache: 'Caching configuration (type, duration, Redis settings)',
        server: 'Server settings (port, host, CORS, rate limiting)',
        python_integration: 'Python service configuration',
        commands: 'Command processing settings',
        monitoring: 'System monitoring and metrics'
      },
      environment_variables: [
        'JAEGIS_PORT - Override server port',
        'JAEGIS_HOST - Override server host',
        'JAEGIS_LOG_LEVEL - Set logging level',
        'JAEGIS_GITHUB_TOKEN - GitHub API token'
      ],
      examples: {
        basic_config: 'See config/config.example.json for basic setup',
        production_config: 'Use environment variables for production secrets'
      }
    }
  }

  createAgentSystemHelp() {
    return {
      description: 'Guide to the JAEGIS Agent Squad System',
      overview: 'JAEGIS uses coordinated agent squads for complex task processing',
      squads: {
        analysis_squad: {
          purpose: 'Data analysis and research tasks',
          agents: ['research-agent', 'data-agent', 'insight-agent'],
          activation: 'Triggered by analytics and research commands'
        },
        development_squad: {
          purpose: 'Software development and coding tasks',
          agents: ['code-agent', 'test-agent', 'deploy-agent'],
          activation: 'Triggered by development-related commands'
        },
        design_squad: {
          purpose: 'UI/UX and architecture design',
          agents: ['ui-agent', 'ux-agent', 'architecture-agent'],
          activation: 'Triggered by design and architecture commands'
        },
        management_squad: {
          purpose: 'Project management and coordination',
          agents: ['project-agent', 'coordination-agent', 'monitor-agent'],
          activation: 'Always active for coordination tasks'
        }
      },
      coordination_modes: [
        'collaborative - Agents work together on shared tasks',
        'sequential - Agents work in predefined order',
        'parallel - Agents work simultaneously on different aspects',
        'hierarchical - Lead agent coordinates others'
      ]
    }
  }

  createTroubleshootingHelp() {
    return {
      description: 'Common issues and solutions for JAEGIS',
      common_issues: {
        'Command not found': {
          symptoms: 'Error message: Unknown command',
          causes: ['Typo in command name', 'Command not loaded', 'GitHub sync issue'],
          solutions: [
            'Check command spelling with /help',
            'Update commands with /cache clear',
            'Verify GitHub connectivity'
          ]
        },
        'Python service not responding': {
          symptoms: 'Python bridge errors, slow responses',
          causes: ['Python service not started', 'Port conflicts', 'Dependencies missing'],
          solutions: [
            'Start Python service: python src/python/api/main.py',
            'Check port 5000 availability',
            'Install Python dependencies: pip install -r requirements.txt'
          ]
        },
        'Cache issues': {
          symptoms: 'Stale data, performance issues',
          causes: ['Cache corruption', 'Redis connection issues', 'Memory limits'],
          solutions: [
            'Clear cache: /cache clear',
            'Check Redis connection',
            'Restart services'
          ]
        }
      },
      diagnostic_commands: [
        '/status - Check overall system health',
        '/debug - Get detailed diagnostic information',
        '/cache health - Check cache system',
        '/agents status - Check agent system'
      ]
    }
  }

  createAPIReferenceHelp() {
    return {
      description: 'JAEGIS API endpoints and WebSocket interface',
      rest_api: {
        base_url: 'http://localhost:3000/api',
        endpoints: {
          'POST /command': 'Execute a command',
          'GET /status': 'Get system status',
          'GET /health': 'Health check',
          'GET /config': 'Get public configuration',
          'GET /metrics': 'Get system metrics'
        }
      },
      websocket: {
        url: 'ws://localhost:3000/ws',
        events: {
          'command': 'Execute command via WebSocket',
          'ping': 'Ping server',
          'command_result': 'Command execution result',
          'error': 'Error message'
        }
      },
      examples: {
        curl_command: 'curl -X POST http://localhost:3000/api/command -H "Content-Type: application/json" -d \'{"command": "/help"}\'',
        websocket_message: '{"type": "command", "command": "/status", "requestId": "123"}'
      }
    }
  }

  // Utility methods
  updateUserContext(userId, query) {
    if (!this.userContexts.has(userId)) {
      this.userContexts.set(userId, {
        queries: [],
        preferences: {},
        lastAccess: Date.now()
      })
    }
    
    const context = this.userContexts.get(userId)
    context.queries.push({
      query,
      timestamp: Date.now()
    })
    
    // Keep only recent queries
    if (context.queries.length > 50) {
      context.queries = context.queries.slice(-50)
    }
    
    context.lastAccess = Date.now()
  }

  async generateSuggestions(query, context) {
    const suggestions = []
    
    // Related commands
    const relatedCommands = this.getRelatedCommands(query)
    suggestions.push(...relatedCommands.map(cmd => ({
      type: 'command',
      text: `/${cmd}`,
      description: `Try the ${cmd} command`
    })))
    
    // Related topics
    const relatedTopics = this.getRelatedTopics(query)
    suggestions.push(...relatedTopics.map(topic => ({
      type: 'topic',
      text: topic,
      description: `Learn about ${topic}`
    })))
    
    // Popular searches
    if (suggestions.length < 5) {
      const popular = this.getPopularTopics()
      suggestions.push(...popular.slice(0, 5 - suggestions.length).map(topic => ({
        type: 'popular',
        text: topic,
        description: `Popular topic: ${topic}`
      })))
    }
    
    return suggestions.slice(0, 5)
  }

  getRelatedCommands(query) {
    const queryLower = query.toLowerCase()
    const related = []
    
    for (const [name, plugin] of this.commandExecutor.plugins) {
      if (name !== queryLower && (
        name.includes(queryLower) ||
        (plugin.description && plugin.description.toLowerCase().includes(queryLower))
      )) {
        related.push(name)
      }
    }
    
    return related.slice(0, 3)
  }

  getRelatedTopics(topicId) {
    const topic = this.helpContent.get(topicId)
    if (!topic) return []
    
    const related = []
    
    for (const [id, otherTopic] of this.helpContent) {
      if (id !== topicId && otherTopic.category === topic.category) {
        related.push(id)
      }
    }
    
    return related.slice(0, 3)
  }

  getPopularTopics() {
    // Based on help request frequency
    const topicCounts = {}
    
    this.helpHistory.forEach(request => {
      const topic = request.result?.topic || request.query
      topicCounts[topic] = (topicCounts[topic] || 0) + 1
    })
    
    return Object.entries(topicCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([topic]) => topic)
  }

  getRecentUpdates() {
    return [
      'Added new agent coordination features',
      'Improved command execution performance',
      'Enhanced help system with contextual assistance',
      'Updated GitHub integration with better caching'
    ]
  }

  getSearchCategories(results) {
    const categories = {}
    
    results.forEach(result => {
      const category = result.category
      categories[category] = (categories[category] || 0) + 1
    })
    
    return categories
  }

  recordHelpRequest(query, type, result, context) {
    const request = {
      query,
      type,
      result,
      context,
      timestamp: Date.now(),
      userId: context.user || 'anonymous'
    }
    
    this.helpHistory.push(request)
    
    // Keep only recent requests
    if (this.helpHistory.length > 1000) {
      this.helpHistory = this.helpHistory.slice(-1000)
    }
  }

  getErrorHelp(error, query) {
    return {
      type: 'error_help',
      query,
      error: error.message,
      suggestions: [
        'Try rephrasing your question',
        'Check the command reference with /help commands',
        'Use /status to check system health',
        'Contact support if the issue persists'
      ],
      fallback_topics: ['troubleshooting', 'quick-start', 'commands']
    }
  }

  // Placeholder methods for future implementation
  async loadTutorials() {
    // Load interactive tutorials
    this.tutorials.set('getting-started', {
      title: 'Getting Started Tutorial',
      steps: [],
      interactive: true
    })
  }

  async loadExamples() {
    // Load code examples and use cases
    this.examples.set('basic-usage', {
      title: 'Basic Usage Examples',
      examples: []
    })
  }

  async loadFAQ() {
    // Load frequently asked questions
    this.faq.set('general', {
      category: 'General',
      questions: []
    })
  }

  searchTutorials(action) {
    // Search for relevant tutorials
    return []
  }

  generateQuickSteps(action) {
    // Generate quick steps for common actions
    return []
  }

  findCommandsForAction(action) {
    // Find commands related to an action
    return []
  }

  findDefinition(term) {
    // Find definition for a term
    return `Definition for ${term} not found`
  }

  analyzeIssue(query) {
    // Analyze issue from query
    return {
      type: 'unknown',
      severity: 'medium',
      keywords: []
    }
  }

  findSolutions(issue) {
    // Find solutions for an issue
    return []
  }

  getDiagnosticSteps(issue) {
    // Get diagnostic steps for an issue
    return []
  }

  getRelatedFAQ(issue) {
    // Get related FAQ entries
    return []
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Help System...')
    
    this.helpContent.clear()
    this.tutorials.clear()
    this.examples.clear()
    this.faq.clear()
    this.userContexts.clear()
    this.helpHistory.length = 0
    this.searchIndex.clear()
    
    this.isInitialized = false
    logger.info('✅ Help System cleanup complete')
  }
}

module.exports = HelpSystem