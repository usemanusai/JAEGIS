/**
 * JAEGIS Autonomous Learning Engine
 * Advanced self-learning system with agent discussions and knowledge synthesis
 * Implements continuous learning loops and capability expansion
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const logger = require('../utils/logger')

// Learning Types
const LEARNING_TYPES = {
  DISCUSSION: 'discussion',
  OBSERVATION: 'observation',
  EXPERIMENTATION: 'experimentation',
  FEEDBACK: 'feedback',
  SYNTHESIS: 'synthesis',
  REFLECTION: 'reflection'
}

// Learning Phases
const LEARNING_PHASES = {
  EXPLORATION: 'exploration',
  ANALYSIS: 'analysis',
  SYNTHESIS: 'synthesis',
  VALIDATION: 'validation',
  INTEGRATION: 'integration',
  OPTIMIZATION: 'optimization'
}

// Discussion Types
const DISCUSSION_TYPES = {
  KNOWLEDGE_SHARING: 'knowledge_sharing',
  PROBLEM_SOLVING: 'problem_solving',
  CAPABILITY_ASSESSMENT: 'capability_assessment',
  METHOD_IMPROVEMENT: 'method_improvement',
  CONSENSUS_BUILDING: 'consensus_building',
  CONFLICT_RESOLUTION: 'conflict_resolution'
}

class AutonomousLearningEngine {
  constructor({ config, openRouterManager, redisAIManager, errorHandler, performanceMonitor }) {
    this.config = config
    this.openRouterManager = openRouterManager
    this.redisAIManager = redisAIManager
    this.errorHandler = errorHandler
    this.performanceMonitor = performanceMonitor
    
    // Learning configuration
    this.learningConfig = {
      enabled: config?.ai?.learning?.enabled !== false,
      maxConcurrentDiscussions: config?.ai?.learning?.max_concurrent_discussions || 5,
      discussionTimeout: config?.ai?.learning?.discussion_timeout || 300000, // 5 minutes
      minParticipants: config?.ai?.learning?.min_participants || 2,
      maxParticipants: config?.ai?.learning?.max_participants || 5,
      learningInterval: config?.ai?.learning?.learning_interval || 3600000, // 1 hour
      synthesisThreshold: config?.ai?.learning?.synthesis_threshold || 0.7,
      consensusThreshold: config?.ai?.learning?.consensus_threshold || 0.8,
      improvementThreshold: config?.ai?.learning?.improvement_threshold || 0.1,
      maxLearningHistory: config?.ai?.learning?.max_learning_history || 1000
    }
    
    // Learning state
    this.activeDiscussions = new Map()
    this.learningHistory = []
    this.knowledgeBase = new Map()
    this.capabilityRegistry = new Map()
    this.improvementQueue = []
    
    // Learning metrics
    this.metrics = {
      totalDiscussions: 0,
      successfulLearning: 0,
      knowledgeGained: 0,
      capabilitiesImproved: 0,
      consensusReached: 0,
      conflictsResolved: 0,
      averageDiscussionTime: 0,
      learningEfficiency: 0
    }
    
    // Background processes
    this.learningIntervals = []
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('🧠 Initializing Autonomous Learning Engine...')
    
    try {
      // Load existing knowledge base
      await this.loadKnowledgeBase()
      
      // Initialize capability registry
      await this.initializeCapabilityRegistry()
      
      // Start learning processes
      this.startLearningProcesses()
      
      // Setup learning triggers
      this.setupLearningTriggers()
      
      this.isInitialized = true
      logger.info('✅ Autonomous Learning Engine initialized')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Autonomous Learning Engine:', error)
      throw error
    }
  }

  async loadKnowledgeBase() {
    try {
      // Load knowledge from Redis
      const knowledgeKeys = await this.redisAIManager.client.keys('knowledge:*')
      
      for (const key of knowledgeKeys) {
        const knowledge = await this.redisAIManager.client.hGetAll(key)
        if (knowledge.topic) {
          this.knowledgeBase.set(knowledge.topic, {
            topic: knowledge.topic,
            content: JSON.parse(knowledge.content || '{}'),
            confidence: parseFloat(knowledge.confidence || '0.5'),
            sources: JSON.parse(knowledge.sources || '[]'),
            lastUpdated: parseInt(knowledge.lastUpdated || '0'),
            validationCount: parseInt(knowledge.validationCount || '0')
          })
        }
      }
      
      logger.info(`📚 Loaded ${this.knowledgeBase.size} knowledge entries`)
      
    } catch (error) {
      logger.warn('Failed to load knowledge base:', error.message)
    }
  }

  async initializeCapabilityRegistry() {
    try {
      // Load capabilities from agents
      const agents = await this.redisAIManager.findAgents({ status: 'active' })
      
      for (const agent of agents) {
        for (const capability of agent.capabilities || []) {
          if (!this.capabilityRegistry.has(capability)) {
            this.capabilityRegistry.set(capability, {
              name: capability,
              agents: [],
              proficiency: new Map(),
              improvements: [],
              lastAssessed: 0
            })
          }
          
          const capabilityData = this.capabilityRegistry.get(capability)
          capabilityData.agents.push(agent.id)
          capabilityData.proficiency.set(agent.id, agent.performance_score || 0.5)
        }
      }
      
      logger.info(`🎯 Initialized ${this.capabilityRegistry.size} capabilities`)
      
    } catch (error) {
      logger.warn('Failed to initialize capability registry:', error.message)
    }
  }

  startLearningProcesses() {
    // Continuous learning process
    const learningInterval = setInterval(async () => {
      await this.performContinuousLearning()
    }, this.learningConfig.learningInterval)
    this.learningIntervals.push(learningInterval)
    
    // Knowledge synthesis process
    const synthesisInterval = setInterval(async () => {
      await this.performKnowledgeSynthesis()
    }, this.learningConfig.learningInterval * 2)
    this.learningIntervals.push(synthesisInterval)
    
    // Capability assessment process
    const assessmentInterval = setInterval(async () => {
      await this.performCapabilityAssessment()
    }, this.learningConfig.learningInterval * 3)
    this.learningIntervals.push(assessmentInterval)
    
    logger.info('🔄 Learning processes started')
  }

  setupLearningTriggers() {
    // Subscribe to learning events
    if (this.redisAIManager.subscriber) {
      this.redisAIManager.subscriber.subscribe('learning_notifications', (message) => {
        this.handleLearningTrigger(JSON.parse(message))
      })
    }
  }

  async performContinuousLearning() {
    if (!this.learningConfig.enabled) return
    
    try {
      logger.info('🧠 Starting continuous learning cycle...')
      
      // Identify learning opportunities
      const opportunities = await this.identifyLearningOpportunities()
      
      // Process each opportunity
      for (const opportunity of opportunities) {
        await this.processLearningOpportunity(opportunity)
      }
      
      // Update learning metrics
      this.updateLearningMetrics()
      
      logger.info(`✅ Continuous learning cycle complete: ${opportunities.length} opportunities processed`)
      
    } catch (error) {
      logger.error('Continuous learning failed:', error)
    }
  }

  async identifyLearningOpportunities() {
    const opportunities = []
    
    try {
      // Check for knowledge gaps
      const knowledgeGaps = await this.identifyKnowledgeGaps()
      opportunities.push(...knowledgeGaps.map(gap => ({
        type: LEARNING_TYPES.DISCUSSION,
        topic: gap.topic,
        priority: gap.priority,
        participants: gap.suggestedParticipants
      })))
      
      // Check for performance issues
      const performanceIssues = await this.identifyPerformanceIssues()
      opportunities.push(...performanceIssues.map(issue => ({
        type: LEARNING_TYPES.EXPERIMENTATION,
        topic: issue.area,
        priority: issue.severity,
        focus: issue.improvement
      })))
      
      // Check for conflicting knowledge
      const conflicts = await this.identifyKnowledgeConflicts()
      opportunities.push(...conflicts.map(conflict => ({
        type: LEARNING_TYPES.SYNTHESIS,
        topic: conflict.topic,
        priority: 'high',
        conflictingSources: conflict.sources
      })))
      
      // Sort by priority
      opportunities.sort((a, b) => {
        const priorityOrder = { high: 3, medium: 2, low: 1 }
        return (priorityOrder[b.priority] || 1) - (priorityOrder[a.priority] || 1)
      })
      
      return opportunities.slice(0, this.learningConfig.maxConcurrentDiscussions)
      
    } catch (error) {
      logger.error('Failed to identify learning opportunities:', error)
      return []
    }
  }

  async identifyKnowledgeGaps() {
    const gaps = []
    
    try {
      // Analyze recent conversations for unknown topics
      const recentConversations = await this.getRecentConversations()
      const mentionedTopics = new Set()
      
      for (const conversation of recentConversations) {
        const topics = await this.extractTopics(conversation.messages)
        topics.forEach(topic => mentionedTopics.add(topic))
      }
      
      // Find topics not in knowledge base
      for (const topic of mentionedTopics) {
        if (!this.knowledgeBase.has(topic)) {
          const agents = await this.findAgentsForTopic(topic)
          if (agents.length >= this.learningConfig.minParticipants) {
            gaps.push({
              topic,
              priority: 'medium',
              suggestedParticipants: agents.slice(0, this.learningConfig.maxParticipants)
            })
          }
        }
      }
      
      return gaps
      
    } catch (error) {
      logger.error('Failed to identify knowledge gaps:', error)
      return []
    }
  }

  async identifyPerformanceIssues() {
    const issues = []
    
    try {
      // Analyze agent performance trends
      const agents = await this.redisAIManager.findAgents({ status: 'active' })
      
      for (const agent of agents) {
        const performanceHistory = await this.getAgentPerformanceHistory(agent.id)
        const trend = this.calculatePerformanceTrend(performanceHistory)
        
        if (trend.direction === 'declining' && trend.magnitude > 0.1) {
          issues.push({
            area: `agent_performance_${agent.type}`,
            severity: trend.magnitude > 0.2 ? 'high' : 'medium',
            improvement: `Improve ${agent.type} agent performance`,
            agentId: agent.id
          })
        }
      }
      
      return issues
      
    } catch (error) {
      logger.error('Failed to identify performance issues:', error)
      return []
    }
  }

  async identifyKnowledgeConflicts() {
    const conflicts = []
    
    try {
      // Check for conflicting information in knowledge base
      for (const [topic, knowledge] of this.knowledgeBase) {
        if (knowledge.sources.length > 1) {
          const sourceAgreement = await this.calculateSourceAgreement(knowledge.sources)
          if (sourceAgreement < this.learningConfig.consensusThreshold) {
            conflicts.push({
              topic,
              sources: knowledge.sources,
              agreement: sourceAgreement
            })
          }
        }
      }
      
      return conflicts
      
    } catch (error) {
      logger.error('Failed to identify knowledge conflicts:', error)
      return []
    }
  }

  async processLearningOpportunity(opportunity) {
    try {
      switch (opportunity.type) {
        case LEARNING_TYPES.DISCUSSION:
          await this.initiateAgentDiscussion(opportunity)
          break
        case LEARNING_TYPES.EXPERIMENTATION:
          await this.conductExperiment(opportunity)
          break
        case LEARNING_TYPES.SYNTHESIS:
          await this.synthesizeKnowledge(opportunity)
          break
        default:
          logger.warn(`Unknown learning opportunity type: ${opportunity.type}`)
      }
      
    } catch (error) {
      logger.error(`Failed to process learning opportunity:`, error)
    }
  }

  async initiateAgentDiscussion(opportunity) {
    const discussionId = `discussion_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    try {
      logger.info(`💬 Initiating agent discussion: ${opportunity.topic}`)
      
      // Create conversation
      const conversationId = await this.redisAIManager.createConversation({
        id: discussionId,
        participants: opportunity.participants || [],
        topic: opportunity.topic
      })
      
      // Generate discussion prompt
      const prompt = await this.generateDiscussionPrompt(opportunity)
      
      // Start discussion
      const discussion = {
        id: discussionId,
        conversationId,
        topic: opportunity.topic,
        type: DISCUSSION_TYPES.KNOWLEDGE_SHARING,
        participants: opportunity.participants || [],
        phase: LEARNING_PHASES.EXPLORATION,
        startTime: Date.now(),
        messages: [],
        insights: [],
        consensus: null,
        status: 'active'
      }
      
      this.activeDiscussions.set(discussionId, discussion)
      
      // Add initial prompt
      await this.redisAIManager.addMessage(conversationId, {
        sender: 'learning_engine',
        content: prompt,
        metadata: { type: 'discussion_prompt' }
      })
      
      // Facilitate discussion
      await this.facilitateDiscussion(discussionId)
      
      this.metrics.totalDiscussions++
      
    } catch (error) {
      logger.error(`Failed to initiate discussion for ${opportunity.topic}:`, error)
    }
  }

  async generateDiscussionPrompt(opportunity) {
    const prompts = {
      knowledge_sharing: `Let's discuss the topic: "${opportunity.topic}". 
        Each participant should share their knowledge and insights about this topic. 
        Focus on practical applications, key concepts, and any relevant experiences.
        Goal: Build comprehensive understanding and identify knowledge gaps.`,
      
      problem_solving: `We need to solve a problem related to: "${opportunity.topic}".
        Let's analyze the issue, brainstorm solutions, and evaluate approaches.
        Each participant should contribute their expertise and perspective.
        Goal: Develop effective solutions and learn from the problem-solving process.`,
      
      capability_assessment: `Let's assess our capabilities in: "${opportunity.topic}".
        Discuss current strengths, weaknesses, and improvement opportunities.
        Share experiences and identify best practices.
        Goal: Understand our collective capabilities and plan improvements.`,
      
      method_improvement: `How can we improve our methods for: "${opportunity.topic}"?
        Analyze current approaches, identify inefficiencies, and propose enhancements.
        Consider new techniques, tools, or processes.
        Goal: Optimize our methods and increase effectiveness.`
    }
    
    const discussionType = opportunity.discussionType || 'knowledge_sharing'
    return prompts[discussionType] || prompts.knowledge_sharing
  }

  async facilitateDiscussion(discussionId) {
    const discussion = this.activeDiscussions.get(discussionId)
    if (!discussion) return
    
    try {
      const maxRounds = 5
      let round = 0
      
      while (round < maxRounds && discussion.status === 'active') {
        // Get responses from participants
        for (const participantId of discussion.participants) {
          await this.getParticipantResponse(discussionId, participantId, round)
        }
        
        // Analyze discussion progress
        const progress = await this.analyzeDiscussionProgress(discussionId)
        
        // Check for consensus or completion
        if (progress.consensus >= this.learningConfig.consensusThreshold) {
          await this.concludeDiscussion(discussionId, 'consensus_reached')
          break
        }
        
        // Move to next phase if needed
        if (progress.phaseComplete) {
          await this.advanceDiscussionPhase(discussionId)
        }
        
        round++
      }
      
      // Conclude discussion if not already concluded
      if (discussion.status === 'active') {
        await this.concludeDiscussion(discussionId, 'max_rounds_reached')
      }
      
    } catch (error) {
      logger.error(`Failed to facilitate discussion ${discussionId}:`, error)
      await this.concludeDiscussion(discussionId, 'error')
    }
  }

  async getParticipantResponse(discussionId, participantId, round) {
    const discussion = this.activeDiscussions.get(discussionId)
    if (!discussion) return
    
    try {
      // Get agent information
      const agent = await this.redisAIManager.getAgent(participantId)
      if (!agent) return
      
      // Get conversation history
      const conversation = await this.redisAIManager.getConversation(discussion.conversationId)
      if (!conversation) return
      
      // Generate context-aware prompt
      const prompt = await this.generateParticipantPrompt(discussion, agent, conversation, round)
      
      // Get AI response
      const response = await this.openRouterManager.generateCompletion(prompt, {
        category: 'reasoning',
        maxTokens: 500,
        temperature: 0.7,
        systemMessage: `You are ${agent.name}, an AI agent with capabilities in ${agent.capabilities.join(', ')}. 
          Participate in this discussion by sharing your knowledge and insights. 
          Be concise but informative. Build on previous messages and contribute new perspectives.`
      })
      
      if (response.success) {
        // Add response to conversation
        await this.redisAIManager.addMessage(discussion.conversationId, {
          sender: participantId,
          content: response.content,
          metadata: { 
            round,
            agent_type: agent.type,
            capabilities: agent.capabilities
          }
        })
        
        discussion.messages.push({
          sender: participantId,
          content: response.content,
          round,
          timestamp: Date.now()
        })
        
        // Extract insights
        const insights = await this.extractInsights(response.content, discussion.topic)
        discussion.insights.push(...insights)
      }
      
    } catch (error) {
      logger.error(`Failed to get response from participant ${participantId}:`, error)
    }
  }

  async generateParticipantPrompt(discussion, agent, conversation, round) {
    const recentMessages = conversation.messages.slice(-5) // Last 5 messages
    const messageHistory = recentMessages.map(msg => 
      `${msg.sender}: ${msg.content}`
    ).join('\n\n')
    
    const roundPrompts = {
      0: `Topic: ${discussion.topic}\n\nPrevious discussion:\n${messageHistory}\n\nShare your initial thoughts and knowledge about this topic.`,
      1: `Topic: ${discussion.topic}\n\nPrevious discussion:\n${messageHistory}\n\nBuild on the previous responses. Add new insights or perspectives.`,
      2: `Topic: ${discussion.topic}\n\nPrevious discussion:\n${messageHistory}\n\nAnalyze what has been shared so far. Identify key points and areas for deeper exploration.`,
      3: `Topic: ${discussion.topic}\n\nPrevious discussion:\n${messageHistory}\n\nSynthesize the discussion. What are the main conclusions and remaining questions?`,
      4: `Topic: ${discussion.topic}\n\nPrevious discussion:\n${messageHistory}\n\nProvide final thoughts and actionable insights from this discussion.`
    }
    
    return roundPrompts[round] || roundPrompts[4]
  }

  async analyzeDiscussionProgress(discussionId) {
    const discussion = this.activeDiscussions.get(discussionId)
    if (!discussion) return { consensus: 0, phaseComplete: false }
    
    try {
      // Analyze message content for consensus indicators
      const messages = discussion.messages
      if (messages.length === 0) return { consensus: 0, phaseComplete: false }
      
      // Simple consensus calculation based on agreement keywords
      const agreementKeywords = ['agree', 'correct', 'yes', 'exactly', 'right', 'true']
      const disagreementKeywords = ['disagree', 'wrong', 'no', 'incorrect', 'false', 'however']
      
      let agreementScore = 0
      let totalStatements = 0
      
      for (const message of messages) {
        const content = message.content.toLowerCase()
        const agreements = agreementKeywords.filter(keyword => content.includes(keyword)).length
        const disagreements = disagreementKeywords.filter(keyword => content.includes(keyword)).length
        
        if (agreements > 0 || disagreements > 0) {
          agreementScore += agreements - disagreements
          totalStatements += agreements + disagreements
        }
      }
      
      const consensus = totalStatements > 0 ? Math.max(0, agreementScore / totalStatements) : 0
      
      // Check if phase is complete (enough messages from all participants)
      const participantMessages = new Map()
      for (const message of messages) {
        participantMessages.set(message.sender, (participantMessages.get(message.sender) || 0) + 1)
      }
      
      const minMessagesPerParticipant = Math.max(1, Math.floor(messages.length / discussion.participants.length))
      const phaseComplete = discussion.participants.every(p => 
        (participantMessages.get(p) || 0) >= minMessagesPerParticipant
      )
      
      return { consensus, phaseComplete }
      
    } catch (error) {
      logger.error(`Failed to analyze discussion progress:`, error)
      return { consensus: 0, phaseComplete: false }
    }
  }

  async advanceDiscussionPhase(discussionId) {
    const discussion = this.activeDiscussions.get(discussionId)
    if (!discussion) return
    
    const phaseOrder = [
      LEARNING_PHASES.EXPLORATION,
      LEARNING_PHASES.ANALYSIS,
      LEARNING_PHASES.SYNTHESIS,
      LEARNING_PHASES.VALIDATION,
      LEARNING_PHASES.INTEGRATION
    ]
    
    const currentIndex = phaseOrder.indexOf(discussion.phase)
    if (currentIndex < phaseOrder.length - 1) {
      discussion.phase = phaseOrder[currentIndex + 1]
      logger.debug(`📈 Advanced discussion ${discussionId} to phase: ${discussion.phase}`)
    }
  }

  async concludeDiscussion(discussionId, reason) {
    const discussion = this.activeDiscussions.get(discussionId)
    if (!discussion) return
    
    try {
      discussion.status = 'completed'
      discussion.endTime = Date.now()
      discussion.duration = discussion.endTime - discussion.startTime
      discussion.conclusionReason = reason
      
      // Generate discussion summary
      const summary = await this.generateDiscussionSummary(discussion)
      
      // Extract and store knowledge
      const knowledge = await this.extractKnowledgeFromDiscussion(discussion)
      if (knowledge) {
        await this.storeKnowledge(knowledge)
      }
      
      // Update agent learning progress
      await this.updateParticipantLearning(discussion)
      
      // Record learning session
      await this.redisAIManager.recordLearningSession({
        agent_id: 'learning_engine',
        topic: discussion.topic,
        content: {
          discussion_id: discussionId,
          participants: discussion.participants,
          insights: discussion.insights,
          summary
        },
        insights: discussion.insights,
        performance_delta: knowledge ? 0.1 : 0,
        source: 'agent_discussion'
      })
      
      // Remove from active discussions
      this.activeDiscussions.delete(discussionId)
      
      // Update metrics
      if (reason === 'consensus_reached') {
        this.metrics.consensusReached++
      }
      this.metrics.successfulLearning++
      this.metrics.averageDiscussionTime = (this.metrics.averageDiscussionTime + discussion.duration) / 2
      
      logger.info(`✅ Concluded discussion ${discussionId}: ${reason}`)
      
    } catch (error) {
      logger.error(`Failed to conclude discussion ${discussionId}:`, error)
    }
  }

  async generateDiscussionSummary(discussion) {
    try {
      const messagesText = discussion.messages.map(msg => 
        `${msg.sender}: ${msg.content}`
      ).join('\n\n')
      
      const prompt = `Summarize this agent discussion about "${discussion.topic}":

${messagesText}

Provide a concise summary that captures:
1. Key insights and conclusions
2. Areas of agreement and disagreement
3. Actionable outcomes
4. Remaining questions or areas for further exploration

Summary:`
      
      const response = await this.openRouterManager.generateCompletion(prompt, {
        category: 'reasoning',
        maxTokens: 300,
        temperature: 0.3
      })
      
      return response.success ? response.content : 'Summary generation failed'
      
    } catch (error) {
      logger.error('Failed to generate discussion summary:', error)
      return 'Summary generation failed'
    }
  }

  async extractKnowledgeFromDiscussion(discussion) {
    try {
      // Combine all insights
      const allInsights = discussion.insights.join(' ')
      
      if (allInsights.length < 50) {
        return null // Not enough content
      }
      
      return {
        topic: discussion.topic,
        content: {
          summary: await this.generateDiscussionSummary(discussion),
          insights: discussion.insights,
          participants: discussion.participants,
          discussion_id: discussion.id
        },
        confidence: discussion.consensus || 0.5,
        sources: [`discussion_${discussion.id}`],
        lastUpdated: Date.now(),
        validationCount: 1
      }
      
    } catch (error) {
      logger.error('Failed to extract knowledge from discussion:', error)
      return null
    }
  }

  async storeKnowledge(knowledge) {
    try {
      // Store in knowledge base
      this.knowledgeBase.set(knowledge.topic, knowledge)
      
      // Store in Redis
      await this.redisAIManager.client.hSet(`knowledge:${knowledge.topic}`, {
        topic: knowledge.topic,
        content: JSON.stringify(knowledge.content),
        confidence: knowledge.confidence,
        sources: JSON.stringify(knowledge.sources),
        lastUpdated: knowledge.lastUpdated,
        validationCount: knowledge.validationCount
      })
      
      this.metrics.knowledgeGained++
      logger.info(`📚 Stored knowledge: ${knowledge.topic}`)
      
    } catch (error) {
      logger.error(`Failed to store knowledge for ${knowledge.topic}:`, error)
    }
  }

  async updateParticipantLearning(discussion) {
    try {
      for (const participantId of discussion.participants) {
        const agent = await this.redisAIManager.getAgent(participantId)
        if (!agent) continue
        
        // Calculate learning delta based on participation
        const participantMessages = discussion.messages.filter(msg => msg.sender === participantId)
        const participationScore = participantMessages.length / discussion.messages.length
        const learningDelta = participationScore * 0.05 // Small improvement
        
        // Update agent learning progress
        const learningProgress = agent.learning_progress || {}
        learningProgress[discussion.topic] = (learningProgress[discussion.topic] || 0) + learningDelta
        
        await this.redisAIManager.updateAgent(participantId, {
          learning_progress: learningProgress,
          performance_score: Math.min(1, agent.performance_score + learningDelta)
        })
      }
      
    } catch (error) {
      logger.error('Failed to update participant learning:', error)
    }
  }

  // Knowledge synthesis methods
  async performKnowledgeSynthesis() {
    try {
      logger.info('🔬 Performing knowledge synthesis...')
      
      // Find related knowledge entries
      const relatedGroups = await this.findRelatedKnowledge()
      
      // Synthesize each group
      for (const group of relatedGroups) {
        await this.synthesizeKnowledgeGroup(group)
      }
      
      logger.info(`✅ Knowledge synthesis complete: ${relatedGroups.length} groups processed`)
      
    } catch (error) {
      logger.error('Knowledge synthesis failed:', error)
    }
  }

  async findRelatedKnowledge() {
    const groups = []
    const processed = new Set()
    
    for (const [topic, knowledge] of this.knowledgeBase) {
      if (processed.has(topic)) continue
      
      const relatedTopics = await this.findRelatedTopics(topic)
      if (relatedTopics.length > 0) {
        const group = [topic, ...relatedTopics]
        groups.push(group)
        group.forEach(t => processed.add(t))
      }
    }
    
    return groups
  }

  async findRelatedTopics(topic) {
    const related = []
    const topicWords = topic.toLowerCase().split(/\s+/)
    
    for (const [otherTopic] of this.knowledgeBase) {
      if (otherTopic === topic) continue
      
      const otherWords = otherTopic.toLowerCase().split(/\s+/)
      const commonWords = topicWords.filter(word => otherWords.includes(word))
      
      if (commonWords.length > 0) {
        related.push(otherTopic)
      }
    }
    
    return related
  }

  async synthesizeKnowledgeGroup(topics) {
    try {
      if (topics.length < 2) return
      
      const knowledgeEntries = topics.map(topic => this.knowledgeBase.get(topic)).filter(Boolean)
      if (knowledgeEntries.length < 2) return
      
      // Create synthesis prompt
      const prompt = this.createSynthesisPrompt(knowledgeEntries)
      
      // Generate synthesis
      const response = await this.openRouterManager.generateCompletion(prompt, {
        category: 'reasoning',
        maxTokens: 800,
        temperature: 0.5
      })
      
      if (response.success) {
        // Store synthesized knowledge
        const synthesizedTopic = `synthesis_${topics.join('_')}`
        const synthesizedKnowledge = {
          topic: synthesizedTopic,
          content: {
            synthesis: response.content,
            sourceTopics: topics,
            originalEntries: knowledgeEntries.map(e => e.content)
          },
          confidence: Math.min(...knowledgeEntries.map(e => e.confidence)),
          sources: knowledgeEntries.flatMap(e => e.sources),
          lastUpdated: Date.now(),
          validationCount: 1
        }
        
        await this.storeKnowledge(synthesizedKnowledge)
        logger.info(`🔬 Synthesized knowledge: ${synthesizedTopic}`)
      }
      
    } catch (error) {
      logger.error('Failed to synthesize knowledge group:', error)
    }
  }

  createSynthesisPrompt(knowledgeEntries) {
    const entriesText = knowledgeEntries.map((entry, index) => 
      `Entry ${index + 1} (${entry.topic}):\n${JSON.stringify(entry.content, null, 2)}`
    ).join('\n\n')
    
    return `Synthesize the following related knowledge entries into a comprehensive understanding:

${entriesText}

Create a synthesis that:
1. Identifies common themes and patterns
2. Resolves any contradictions or conflicts
3. Combines insights into a unified understanding
4. Highlights key relationships and dependencies
5. Suggests practical applications

Synthesis:`
  }

  // Capability assessment methods
  async performCapabilityAssessment() {
    try {
      logger.info('🎯 Performing capability assessment...')
      
      // Assess each capability
      for (const [capability, data] of this.capabilityRegistry) {
        await this.assessCapability(capability, data)
      }
      
      // Identify improvement opportunities
      const improvements = await this.identifyCapabilityImprovements()
      this.improvementQueue.push(...improvements)
      
      logger.info(`✅ Capability assessment complete: ${this.capabilityRegistry.size} capabilities assessed`)
      
    } catch (error) {
      logger.error('Capability assessment failed:', error)
    }
  }

  async assessCapability(capability, data) {
    try {
      // Calculate average proficiency
      const proficiencies = Array.from(data.proficiency.values())
      const avgProficiency = proficiencies.reduce((sum, p) => sum + p, 0) / proficiencies.length
      
      // Assess improvement trend
      const recentImprovements = data.improvements.filter(
        imp => Date.now() - imp.timestamp < 30 * 24 * 60 * 60 * 1000 // Last 30 days
      )
      
      const improvementTrend = recentImprovements.length > 0 
        ? recentImprovements.reduce((sum, imp) => sum + imp.delta, 0) / recentImprovements.length
        : 0
      
      // Update capability data
      data.avgProficiency = avgProficiency
      data.improvementTrend = improvementTrend
      data.lastAssessed = Date.now()
      
      // Store assessment
      await this.redisAIManager.client.hSet(`capability:${capability}`, {
        name: capability,
        agents: JSON.stringify(data.agents),
        avgProficiency,
        improvementTrend,
        lastAssessed: data.lastAssessed,
        assessmentCount: (data.assessmentCount || 0) + 1
      })
      
    } catch (error) {
      logger.error(`Failed to assess capability ${capability}:`, error)
    }
  }

  async identifyCapabilityImprovements() {
    const improvements = []
    
    for (const [capability, data] of this.capabilityRegistry) {
      // Check for low proficiency
      if (data.avgProficiency < 0.6) {
        improvements.push({
          type: 'proficiency_improvement',
          capability,
          priority: 'high',
          currentLevel: data.avgProficiency,
          targetLevel: 0.8,
          agents: data.agents
        })
      }
      
      // Check for negative trend
      if (data.improvementTrend < -0.05) {
        improvements.push({
          type: 'trend_reversal',
          capability,
          priority: 'medium',
          trend: data.improvementTrend,
          agents: data.agents
        })
      }
    }
    
    return improvements
  }

  // Utility methods
  async getRecentConversations() {
    try {
      // Get recent conversations from Redis
      const conversationKeys = await this.redisAIManager.client.keys('conv:*')
      const conversations = []
      
      for (const key of conversationKeys.slice(-10)) { // Last 10 conversations
        const conversation = await this.redisAIManager.getConversation(key.split(':')[1])
        if (conversation) {
          conversations.push(conversation)
        }
      }
      
      return conversations
      
    } catch (error) {
      logger.error('Failed to get recent conversations:', error)
      return []
    }
  }

  async extractTopics(messages) {
    const topics = new Set()
    
    for (const message of messages) {
      const content = message.content.toLowerCase()
      
      // Simple topic extraction (in production, use NLP)
      const words = content.split(/\s+/)
      const importantWords = words.filter(word => 
        word.length > 4 && 
        !['this', 'that', 'with', 'from', 'they', 'have', 'been', 'will', 'would', 'could', 'should'].includes(word)
      )
      
      importantWords.forEach(word => topics.add(word))
    }
    
    return Array.from(topics)
  }

  async findAgentsForTopic(topic) {
    try {
      // Find agents with relevant capabilities
      const relevantAgents = []
      
      for (const [agentId, agent] of this.redisAIManager.agentRegistry) {
        const capabilities = agent.capabilities || []
        const hasRelevantCapability = capabilities.some(cap => 
          cap.toLowerCase().includes(topic.toLowerCase()) ||
          topic.toLowerCase().includes(cap.toLowerCase())
        )
        
        if (hasRelevantCapability) {
          relevantAgents.push(agentId)
        }
      }
      
      return relevantAgents
      
    } catch (error) {
      logger.error(`Failed to find agents for topic ${topic}:`, error)
      return []
    }
  }

  async getAgentPerformanceHistory(agentId) {
    try {
      // Get performance history from learning sessions
      const sessions = await this.redisAIManager.client.keys(`learn:*`)
      const history = []
      
      for (const sessionKey of sessions) {
        const session = await this.redisAIManager.client.hGetAll(sessionKey)
        if (session.agent_id === agentId) {
          history.push({
            timestamp: parseInt(session.timestamp),
            delta: parseFloat(session.performance_delta || '0')
          })
        }
      }
      
      return history.sort((a, b) => a.timestamp - b.timestamp)
      
    } catch (error) {
      logger.error(`Failed to get performance history for agent ${agentId}:`, error)
      return []
    }
  }

  calculatePerformanceTrend(history) {
    if (history.length < 2) {
      return { direction: 'stable', magnitude: 0 }
    }
    
    const recent = history.slice(-5) // Last 5 entries
    const totalDelta = recent.reduce((sum, entry) => sum + entry.delta, 0)
    const avgDelta = totalDelta / recent.length
    
    return {
      direction: avgDelta > 0.01 ? 'improving' : avgDelta < -0.01 ? 'declining' : 'stable',
      magnitude: Math.abs(avgDelta)
    }
  }

  async calculateSourceAgreement(sources) {
    // Simple agreement calculation
    // In production, this would analyze actual content similarity
    return Math.random() * 0.4 + 0.6 // Random between 0.6 and 1.0
  }

  async extractInsights(content, topic) {
    const insights = []
    
    // Simple insight extraction
    const sentences = content.split(/[.!?]+/)
    for (const sentence of sentences) {
      if (sentence.trim().length > 20 && sentence.toLowerCase().includes(topic.toLowerCase())) {
        insights.push({
          content: sentence.trim(),
          topic,
          confidence: 0.7,
          timestamp: Date.now()
        })
      }
    }
    
    return insights
  }

  handleLearningTrigger(data) {
    try {
      switch (data.type) {
        case 'performance_decline':
          this.improvementQueue.push({
            type: 'performance_improvement',
            agentId: data.agent_id,
            priority: 'high'
          })
          break
        case 'knowledge_gap':
          this.improvementQueue.push({
            type: 'knowledge_acquisition',
            topic: data.topic,
            priority: 'medium'
          })
          break
        case 'conflict_detected':
          this.improvementQueue.push({
            type: 'conflict_resolution',
            topic: data.topic,
            priority: 'high'
          })
          break
      }
      
    } catch (error) {
      logger.error('Failed to handle learning trigger:', error)
    }
  }

  updateLearningMetrics() {
    // Calculate learning efficiency
    const totalLearning = this.metrics.successfulLearning + this.metrics.knowledgeGained
    const totalAttempts = this.metrics.totalDiscussions
    this.metrics.learningEfficiency = totalAttempts > 0 ? totalLearning / totalAttempts : 0
  }

  // Statistics and reporting
  getLearningReport() {
    return {
      timestamp: Date.now(),
      metrics: { ...this.metrics },
      knowledgeBase: {
        totalEntries: this.knowledgeBase.size,
        avgConfidence: this.calculateAverageConfidence(),
        recentEntries: this.getRecentKnowledgeEntries()
      },
      capabilities: {
        total: this.capabilityRegistry.size,
        avgProficiency: this.calculateAverageProficiency(),
        improvementOpportunities: this.improvementQueue.length
      },
      activeDiscussions: {
        count: this.activeDiscussions.size,
        topics: Array.from(this.activeDiscussions.values()).map(d => d.topic)
      },
      configuration: this.learningConfig
    }
  }

  calculateAverageConfidence() {
    if (this.knowledgeBase.size === 0) return 0
    
    const confidences = Array.from(this.knowledgeBase.values()).map(k => k.confidence)
    return confidences.reduce((sum, c) => sum + c, 0) / confidences.length
  }

  calculateAverageProficiency() {
    if (this.capabilityRegistry.size === 0) return 0
    
    const proficiencies = Array.from(this.capabilityRegistry.values())
      .filter(c => c.avgProficiency !== undefined)
      .map(c => c.avgProficiency)
    
    return proficiencies.length > 0 
      ? proficiencies.reduce((sum, p) => sum + p, 0) / proficiencies.length 
      : 0
  }

  getRecentKnowledgeEntries() {
    const recent = Array.from(this.knowledgeBase.values())
      .sort((a, b) => b.lastUpdated - a.lastUpdated)
      .slice(0, 5)
    
    return recent.map(k => ({
      topic: k.topic,
      confidence: k.confidence,
      lastUpdated: k.lastUpdated
    }))
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Autonomous Learning Engine...')
    
    // Clear intervals
    this.learningIntervals.forEach(interval => clearInterval(interval))
    this.learningIntervals.length = 0
    
    // Clear data structures
    this.activeDiscussions.clear()
    this.knowledgeBase.clear()
    this.capabilityRegistry.clear()
    this.improvementQueue.length = 0
    this.learningHistory.length = 0
    
    this.isInitialized = false
    logger.info('✅ Autonomous Learning Engine cleanup complete')
  }
}

module.exports = {
  AutonomousLearningEngine,
  LEARNING_TYPES,
  LEARNING_PHASES,
  DISCUSSION_TYPES
}