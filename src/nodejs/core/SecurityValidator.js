/**
 * JAEGIS Security Validator
 * Comprehensive security validation and protection system
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const crypto = require('crypto')
const logger = require('../utils/logger')

// Security threat types
const THREAT_TYPES = {
  XSS: 'xss',
  SQL_INJECTION: 'sql_injection',
  COMMAND_INJECTION: 'command_injection',
  PATH_TRAVERSAL: 'path_traversal',
  LDAP_INJECTION: 'ldap_injection',
  TEMPLATE_INJECTION: 'template_injection',
  DESERIALIZATION: 'deserialization',
  BUFFER_OVERFLOW: 'buffer_overflow',
  RATE_LIMIT_ABUSE: 'rate_limit_abuse',
  BRUTE_FORCE: 'brute_force'
}

// Security levels
const SECURITY_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical'
}

// Validation patterns
const SECURITY_PATTERNS = {
  xss: [
    /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
    /javascript:/gi,
    /on\w+\s*=/gi,
    /<iframe/gi,
    /<object/gi,
    /<embed/gi,
    /vbscript:/gi
  ],
  sqlInjection: [
    /(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)/gi,
    /(\b(OR|AND)\s+\d+\s*=\s*\d+)/gi,
    /('|(\\')|(;)|(--)|(\|)|(\*)|(%27)|(%3D)|(%3B)|(%2D%2D))/gi,
    /(\b(WAITFOR|DELAY)\b)/gi
  ],
  commandInjection: [
    /[;&|`$(){}[\]]/g,
    /\b(cat|ls|pwd|whoami|id|uname|ps|netstat|ifconfig|ping|wget|curl|nc|telnet|ssh|ftp|chmod|chown|rm|mv|cp|mkdir|rmdir)\b/gi,
    /(\||&&|;|`|\$\(|\$\{)/g
  ],
  pathTraversal: [
    /\.\.[\/\\]/g,
    /%2e%2e[\/\\]/gi,
    /\.\.[%2f%5c]/gi,
    /%252e%252e/gi,
    /\.\.%c0%af/gi,
    /\.\.%c1%9c/gi
  ],
  ldapInjection: [
    /(\*|\(|\)|\||&|!|=|<|>|~|;)/g,
    /(\${.*})/g,
    /(\%[0-9a-f]{2})/gi
  ],
  templateInjection: [
    /\{\{.*\}\}/g,
    /\$\{.*\}/g,
    /<\%.*\%>/g,
    /\[\[.*\]\]/g,
    /#\{.*\}/g
  ],
  deserialization: [
    /\b(pickle|marshal|yaml|json|xml|serialize|unserialize)\b/gi,
    /(__reduce__|__setstate__|__getstate__)/gi,
    /\b(eval|exec|compile)\b/gi
  ]
}

class SecurityValidator {
  constructor({ config }) {
    this.config = config
    
    // Security configuration
    this.securityConfig = {
      enabled: config?.security?.enabled !== false,
      strictMode: config?.security?.strict_mode || false,
      logThreats: config?.security?.log_threats !== false,
      blockThreats: config?.security?.block_threats !== false,
      alertOnThreats: config?.security?.alert_on_threats || false,
      maxInputSize: config?.security?.max_input_size || 10000,
      maxDepth: config?.security?.max_depth || 10,
      rateLimitWindow: config?.security?.rate_limit_window || 60000,
      rateLimitMax: config?.security?.rate_limit_max || 100
    }
    
    // Threat tracking
    this.threatLog = []
    this.blockedRequests = new Map()
    this.rateLimitTracking = new Map()
    this.suspiciousPatterns = new Map()
    
    // Security metrics
    this.securityMetrics = {
      totalValidations: 0,
      threatsDetected: 0,
      threatsBlocked: 0,
      falsePositives: 0,
      byThreatType: new Map(),
      bySecurityLevel: new Map()
    }
    
    // Whitelist and blacklist
    this.whitelist = new Set(config?.security?.whitelist || [])
    this.blacklist = new Set(config?.security?.blacklist || [])
    
    this.isInitialized = false
  }

  async initialize() {
    logger.info('🔒 Initializing Security Validator...')
    
    try {
      // Load security rules
      this.loadSecurityRules()
      
      // Setup threat detection
      this.setupThreatDetection()
      
      // Initialize rate limiting
      this.initializeRateLimiting()
      
      // Setup cleanup
      this.setupCleanup()
      
      this.isInitialized = true
      logger.info('✅ Security Validator initialized successfully')
      
    } catch (error) {
      logger.error('❌ Failed to initialize Security Validator:', error)
      throw error
    }
  }

  loadSecurityRules() {
    // Load additional security rules from configuration
    if (this.config.security?.customRules) {
      this.config.security.customRules.forEach(rule => {
        if (rule.pattern && rule.type) {
          if (!SECURITY_PATTERNS[rule.type]) {
            SECURITY_PATTERNS[rule.type] = []
          }
          SECURITY_PATTERNS[rule.type].push(new RegExp(rule.pattern, rule.flags || 'gi'))
        }
      })
    }
  }

  setupThreatDetection() {
    // Setup advanced threat detection algorithms
    this.threatDetectors = {
      anomalyDetection: this.createAnomalyDetector(),
      patternMatching: this.createPatternMatcher(),
      behaviorAnalysis: this.createBehaviorAnalyzer(),
      entropyAnalysis: this.createEntropyAnalyzer()
    }
  }

  initializeRateLimiting() {
    // Setup rate limiting cleanup
    setInterval(() => {
      this.cleanupRateLimiting()
    }, this.securityConfig.rateLimitWindow)
  }

  setupCleanup() {
    // Cleanup old threat logs and metrics
    setInterval(() => {
      this.cleanupThreatLogs()
    }, 3600000) // Every hour
  }

  async validateInput(input, context = {}) {
    if (!this.securityConfig.enabled) {
      return { valid: true, threats: [] }
    }
    
    this.securityMetrics.totalValidations++
    
    try {
      const validationResult = {
        valid: true,
        threats: [],
        sanitized: input,
        blocked: false,
        securityLevel: SECURITY_LEVELS.LOW
      }
      
      // Basic validation
      const basicValidation = this.performBasicValidation(input, context)
      if (!basicValidation.valid) {
        validationResult.valid = false
        validationResult.threats.push(...basicValidation.threats)
      }
      
      // Threat detection
      const threatDetection = await this.detectThreats(input, context)
      if (threatDetection.threats.length > 0) {
        validationResult.threats.push(...threatDetection.threats)
        validationResult.securityLevel = this.calculateSecurityLevel(threatDetection.threats)
      }
      
      // Rate limiting check
      const rateLimitCheck = this.checkRateLimit(context)
      if (!rateLimitCheck.allowed) {
        validationResult.valid = false
        validationResult.blocked = true
        validationResult.threats.push({
          type: THREAT_TYPES.RATE_LIMIT_ABUSE,
          severity: SECURITY_LEVELS.MEDIUM,
          message: 'Rate limit exceeded'
        })
      }
      
      // Input sanitization
      if (validationResult.threats.length > 0) {
        validationResult.sanitized = this.sanitizeInput(input, validationResult.threats)
      }
      
      // Determine if request should be blocked
      if (this.shouldBlockRequest(validationResult.threats, context)) {
        validationResult.valid = false
        validationResult.blocked = true
        this.securityMetrics.threatsBlocked++
      }
      
      // Log threats
      if (validationResult.threats.length > 0) {
        this.logThreat(input, validationResult.threats, context)
        this.securityMetrics.threatsDetected++
        
        // Update threat type metrics
        validationResult.threats.forEach(threat => {
          const count = this.securityMetrics.byThreatType.get(threat.type) || 0
          this.securityMetrics.byThreatType.set(threat.type, count + 1)
        })
      }
      
      return validationResult
      
    } catch (error) {
      logger.error('Security validation error:', error)
      return {
        valid: false,
        threats: [{
          type: 'validation_error',
          severity: SECURITY_LEVELS.HIGH,
          message: 'Security validation failed'
        }],
        sanitized: '',
        blocked: true
      }
    }
  }

  performBasicValidation(input, context) {
    const threats = []
    
    // Check input size
    if (typeof input === 'string' && input.length > this.securityConfig.maxInputSize) {
      threats.push({
        type: THREAT_TYPES.BUFFER_OVERFLOW,
        severity: SECURITY_LEVELS.MEDIUM,
        message: `Input size exceeds maximum allowed (${this.securityConfig.maxInputSize})`
      })
    }
    
    // Check for null bytes
    if (typeof input === 'string' && input.includes('\0')) {
      threats.push({
        type: THREAT_TYPES.COMMAND_INJECTION,
        severity: SECURITY_LEVELS.HIGH,
        message: 'Null byte detected in input'
      })
    }
    
    // Check object depth (for JSON inputs)
    if (typeof input === 'object') {
      const depth = this.calculateObjectDepth(input)
      if (depth > this.securityConfig.maxDepth) {
        threats.push({
          type: THREAT_TYPES.DESERIALIZATION,
          severity: SECURITY_LEVELS.MEDIUM,
          message: `Object depth exceeds maximum allowed (${this.securityConfig.maxDepth})`
        })
      }
    }
    
    // Check blacklist
    if (this.isBlacklisted(input, context)) {
      threats.push({
        type: 'blacklisted_input',
        severity: SECURITY_LEVELS.HIGH,
        message: 'Input matches blacklisted pattern'
      })
    }
    
    return {
      valid: threats.length === 0,
      threats
    }
  }

  async detectThreats(input, context) {
    const threats = []
    const inputString = typeof input === 'string' ? input : JSON.stringify(input)
    
    // Pattern-based detection
    for (const [threatType, patterns] of Object.entries(SECURITY_PATTERNS)) {
      for (const pattern of patterns) {
        if (pattern.test(inputString)) {
          threats.push({
            type: threatType,
            severity: this.getThreatSeverity(threatType),
            message: `Potential ${threatType} detected`,
            pattern: pattern.source,
            match: inputString.match(pattern)?.[0]
          })
        }
      }
    }
    
    // Advanced threat detection
    const anomalyThreats = await this.threatDetectors.anomalyDetection(inputString, context)
    const behaviorThreats = await this.threatDetectors.behaviorAnalysis(inputString, context)
    const entropyThreats = await this.threatDetectors.entropyAnalysis(inputString, context)
    
    threats.push(...anomalyThreats, ...behaviorThreats, ...entropyThreats)
    
    return { threats }
  }

  createAnomalyDetector() {
    return async (input, context) => {
      const threats = []
      
      // Check for unusual character distributions
      const charDistribution = this.analyzeCharacterDistribution(input)
      if (charDistribution.anomalyScore > 0.8) {
        threats.push({
          type: 'anomalous_input',
          severity: SECURITY_LEVELS.MEDIUM,
          message: 'Unusual character distribution detected',
          score: charDistribution.anomalyScore
        })
      }
      
      // Check for encoded payloads
      if (this.detectEncodedPayload(input)) {
        threats.push({
          type: 'encoded_payload',
          severity: SECURITY_LEVELS.HIGH,
          message: 'Potentially encoded malicious payload detected'
        })
      }
      
      return threats
    }
  }

  createPatternMatcher() {
    return async (input, context) => {
      const threats = []
      
      // Advanced pattern matching using machine learning-like approaches
      const suspiciousPatterns = this.detectSuspiciousPatterns(input)
      threats.push(...suspiciousPatterns)
      
      return threats
    }
  }

  createBehaviorAnalyzer() {
    return async (input, context) => {
      const threats = []
      
      // Analyze request behavior patterns
      if (context.user) {
        const userBehavior = this.analyzeUserBehavior(context.user, input)
        if (userBehavior.suspicious) {
          threats.push({
            type: 'suspicious_behavior',
            severity: SECURITY_LEVELS.MEDIUM,
            message: 'Unusual user behavior pattern detected',
            details: userBehavior.details
          })
        }
      }
      
      return threats
    }
  }

  createEntropyAnalyzer() {
    return async (input, context) => {
      const threats = []
      
      // Calculate input entropy
      const entropy = this.calculateEntropy(input)
      
      // High entropy might indicate encrypted/encoded payloads
      if (entropy > 7.5) {
        threats.push({
          type: 'high_entropy_input',
          severity: SECURITY_LEVELS.MEDIUM,
          message: 'High entropy input detected (possible encoded payload)',
          entropy
        })
      }
      
      // Very low entropy might indicate padding attacks
      if (entropy < 1.0 && input.length > 100) {
        threats.push({
          type: 'low_entropy_input',
          severity: SECURITY_LEVELS.LOW,
          message: 'Unusually low entropy input detected',
          entropy
        })
      }
      
      return threats
    }
  }

  analyzeCharacterDistribution(input) {
    const charCounts = {}
    const totalChars = input.length
    
    for (const char of input) {
      charCounts[char] = (charCounts[char] || 0) + 1
    }
    
    // Calculate distribution anomaly score
    const expectedFrequency = 1 / Object.keys(charCounts).length
    let anomalyScore = 0
    
    for (const count of Object.values(charCounts)) {
      const frequency = count / totalChars
      anomalyScore += Math.abs(frequency - expectedFrequency)
    }
    
    return { anomalyScore: anomalyScore / Object.keys(charCounts).length }
  }

  detectEncodedPayload(input) {
    // Check for common encoding patterns
    const encodingPatterns = [
      /^[A-Za-z0-9+/]+=*$/, // Base64
      /%[0-9A-Fa-f]{2}/, // URL encoding
      /\\x[0-9A-Fa-f]{2}/, // Hex encoding
      /\\u[0-9A-Fa-f]{4}/, // Unicode encoding
      /&[a-zA-Z]+;/ // HTML entities
    ]
    
    return encodingPatterns.some(pattern => pattern.test(input))
  }

  detectSuspiciousPatterns(input) {
    const threats = []
    
    // Check for obfuscation techniques
    if (this.detectObfuscation(input)) {
      threats.push({
        type: 'obfuscated_input',
        severity: SECURITY_LEVELS.HIGH,
        message: 'Obfuscated input detected'
      })
    }
    
    // Check for polyglot attacks
    if (this.detectPolyglot(input)) {
      threats.push({
        type: 'polyglot_attack',
        severity: SECURITY_LEVELS.HIGH,
        message: 'Potential polyglot attack detected'
      })
    }
    
    return threats
  }

  detectObfuscation(input) {
    // Look for common obfuscation patterns
    const obfuscationPatterns = [
      /[a-zA-Z]\s*\+\s*[a-zA-Z]/, // String concatenation
      /String\.fromCharCode/, // Character code conversion
      /eval\s*\(/, // Dynamic evaluation
      /Function\s*\(/, // Function constructor
      /setTimeout\s*\(/, // Delayed execution
      /\[.*\]\[.*\]/ // Bracket notation access
    ]
    
    return obfuscationPatterns.some(pattern => pattern.test(input))
  }

  detectPolyglot(input) {
    // Check if input contains multiple language constructs
    const languagePatterns = {
      javascript: /(<script|javascript:|on\w+\s*=)/i,
      sql: /(SELECT|INSERT|UPDATE|DELETE|UNION)/i,
      html: /(<[a-zA-Z][^>]*>)/i,
      xml: /(<\?xml|<!DOCTYPE)/i,
      php: /(<\?php|\$_)/i
    }
    
    const matchedLanguages = Object.keys(languagePatterns).filter(
      lang => languagePatterns[lang].test(input)
    )
    
    return matchedLanguages.length > 1
  }

  analyzeUserBehavior(userId, input) {
    // Simple behavior analysis (in production, this would be more sophisticated)
    const userHistory = this.getUserHistory(userId)
    
    const suspicious = {
      rapidRequests: userHistory.recentRequests > 50,
      unusualPatterns: this.detectUnusualPatterns(userHistory, input),
      escalatingComplexity: this.detectEscalatingComplexity(userHistory, input)
    }
    
    return {
      suspicious: Object.values(suspicious).some(Boolean),
      details: suspicious
    }
  }

  getUserHistory(userId) {
    // Mock user history - in production, this would come from a database
    return {
      recentRequests: Math.floor(Math.random() * 100),
      averageInputLength: 50,
      commonPatterns: ['help', 'status'],
      lastSeen: Date.now() - 3600000
    }
  }

  detectUnusualPatterns(userHistory, input) {
    // Check if input deviates significantly from user's normal patterns
    return input.length > userHistory.averageInputLength * 3
  }

  detectEscalatingComplexity(userHistory, input) {
    // Check for escalating attack complexity
    const complexityScore = this.calculateComplexityScore(input)
    return complexityScore > 0.8
  }

  calculateComplexityScore(input) {
    let score = 0
    
    // Special characters
    score += (input.match(/[^a-zA-Z0-9\s]/g) || []).length / input.length
    
    // Nested structures
    score += (input.match(/[({[]/g) || []).length / input.length
    
    // Keywords
    const keywords = ['script', 'eval', 'function', 'select', 'union', 'drop']
    score += keywords.filter(keyword => input.toLowerCase().includes(keyword)).length / keywords.length
    
    return Math.min(score, 1)
  }

  calculateEntropy(input) {
    const charCounts = {}
    
    for (const char of input) {
      charCounts[char] = (charCounts[char] || 0) + 1
    }
    
    let entropy = 0
    const length = input.length
    
    for (const count of Object.values(charCounts)) {
      const probability = count / length
      entropy -= probability * Math.log2(probability)
    }
    
    return entropy
  }

  calculateObjectDepth(obj, depth = 0) {
    if (depth > this.securityConfig.maxDepth) return depth
    if (typeof obj !== 'object' || obj === null) return depth
    
    let maxDepth = depth
    for (const value of Object.values(obj)) {
      if (typeof value === 'object' && value !== null) {
        maxDepth = Math.max(maxDepth, this.calculateObjectDepth(value, depth + 1))
      }
    }
    
    return maxDepth
  }

  getThreatSeverity(threatType) {
    const severityMap = {
      [THREAT_TYPES.XSS]: SECURITY_LEVELS.HIGH,
      [THREAT_TYPES.SQL_INJECTION]: SECURITY_LEVELS.CRITICAL,
      [THREAT_TYPES.COMMAND_INJECTION]: SECURITY_LEVELS.CRITICAL,
      [THREAT_TYPES.PATH_TRAVERSAL]: SECURITY_LEVELS.HIGH,
      [THREAT_TYPES.LDAP_INJECTION]: SECURITY_LEVELS.HIGH,
      [THREAT_TYPES.TEMPLATE_INJECTION]: SECURITY_LEVELS.HIGH,
      [THREAT_TYPES.DESERIALIZATION]: SECURITY_LEVELS.CRITICAL,
      [THREAT_TYPES.BUFFER_OVERFLOW]: SECURITY_LEVELS.MEDIUM,
      [THREAT_TYPES.RATE_LIMIT_ABUSE]: SECURITY_LEVELS.MEDIUM,
      [THREAT_TYPES.BRUTE_FORCE]: SECURITY_LEVELS.HIGH
    }
    
    return severityMap[threatType] || SECURITY_LEVELS.MEDIUM
  }

  calculateSecurityLevel(threats) {
    if (threats.some(t => t.severity === SECURITY_LEVELS.CRITICAL)) {
      return SECURITY_LEVELS.CRITICAL
    }
    if (threats.some(t => t.severity === SECURITY_LEVELS.HIGH)) {
      return SECURITY_LEVELS.HIGH
    }
    if (threats.some(t => t.severity === SECURITY_LEVELS.MEDIUM)) {
      return SECURITY_LEVELS.MEDIUM
    }
    return SECURITY_LEVELS.LOW
  }

  shouldBlockRequest(threats, context) {
    if (!this.securityConfig.blockThreats) return false
    
    // Block critical threats
    if (threats.some(t => t.severity === SECURITY_LEVELS.CRITICAL)) {
      return true
    }
    
    // Block in strict mode
    if (this.securityConfig.strictMode && threats.length > 0) {
      return true
    }
    
    // Block repeated offenders
    if (context.user && this.isRepeatedOffender(context.user)) {
      return true
    }
    
    return false
  }

  isRepeatedOffender(userId) {
    const userThreats = this.threatLog.filter(
      log => log.context.user === userId && 
      Date.now() - log.timestamp < 3600000 // Last hour
    )
    
    return userThreats.length > 5
  }

  sanitizeInput(input, threats) {
    let sanitized = input
    
    if (typeof sanitized !== 'string') {
      sanitized = JSON.stringify(sanitized)
    }
    
    // Remove detected threats
    threats.forEach(threat => {
      if (threat.match) {
        sanitized = sanitized.replace(new RegExp(threat.match, 'gi'), '[SANITIZED]')
      }
    })
    
    // Apply general sanitization
    sanitized = this.applyGeneralSanitization(sanitized)
    
    return sanitized
  }

  applyGeneralSanitization(input) {
    return input
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;')
      .replace(/\\/g, '&#x5C;')
      .replace(/`/g, '&#x60;')
      .replace(/=/g, '&#x3D;')
  }

  checkRateLimit(context) {
    const identifier = context.ip || context.user || 'anonymous'
    const now = Date.now()
    const windowStart = now - this.securityConfig.rateLimitWindow
    
    // Get or create rate limit entry
    if (!this.rateLimitTracking.has(identifier)) {
      this.rateLimitTracking.set(identifier, [])
    }
    
    const requests = this.rateLimitTracking.get(identifier)
    
    // Remove old requests
    const recentRequests = requests.filter(timestamp => timestamp > windowStart)
    this.rateLimitTracking.set(identifier, recentRequests)
    
    // Check if limit exceeded
    if (recentRequests.length >= this.securityConfig.rateLimitMax) {
      return {
        allowed: false,
        remaining: 0,
        resetTime: windowStart + this.securityConfig.rateLimitWindow
      }
    }
    
    // Add current request
    recentRequests.push(now)
    
    return {
      allowed: true,
      remaining: this.securityConfig.rateLimitMax - recentRequests.length,
      resetTime: windowStart + this.securityConfig.rateLimitWindow
    }
  }

  isBlacklisted(input, context) {
    const inputString = typeof input === 'string' ? input : JSON.stringify(input)
    
    // Check exact matches
    if (this.blacklist.has(inputString)) return true
    
    // Check pattern matches
    for (const pattern of this.blacklist) {
      if (pattern.startsWith('/') && pattern.endsWith('/')) {
        // Regex pattern
        const regex = new RegExp(pattern.slice(1, -1), 'i')
        if (regex.test(inputString)) return true
      } else if (inputString.toLowerCase().includes(pattern.toLowerCase())) {
        return true
      }
    }
    
    // Check context-based blacklisting
    if (context.ip && this.blacklist.has(context.ip)) return true
    if (context.user && this.blacklist.has(context.user)) return true
    
    return false
  }

  logThreat(input, threats, context) {
    if (!this.securityConfig.logThreats) return
    
    const threatLog = {
      timestamp: Date.now(),
      input: typeof input === 'string' ? input.substring(0, 1000) : '[OBJECT]',
      threats,
      context: {
        user: context.user,
        ip: context.ip,
        userAgent: context.userAgent,
        operation: context.operation
      },
      blocked: this.shouldBlockRequest(threats, context)
    }
    
    this.threatLog.push(threatLog)
    
    // Log to system logger
    logger.warn('🚨 Security threat detected', {
      threatCount: threats.length,
      severity: this.calculateSecurityLevel(threats),
      user: context.user,
      ip: context.ip,
      blocked: threatLog.blocked
    })
    
    // Send alert if configured
    if (this.securityConfig.alertOnThreats) {
      this.sendSecurityAlert(threatLog)
    }
  }

  sendSecurityAlert(threatLog) {
    // In production, this would send alerts via email, Slack, etc.
    logger.error('🚨 SECURITY ALERT', {
      timestamp: new Date(threatLog.timestamp).toISOString(),
      threats: threatLog.threats.map(t => t.type),
      severity: this.calculateSecurityLevel(threatLog.threats),
      context: threatLog.context,
      blocked: threatLog.blocked
    })
  }

  cleanupRateLimiting() {
    const now = Date.now()
    const windowStart = now - this.securityConfig.rateLimitWindow
    
    for (const [identifier, requests] of this.rateLimitTracking.entries()) {
      const recentRequests = requests.filter(timestamp => timestamp > windowStart)
      
      if (recentRequests.length === 0) {
        this.rateLimitTracking.delete(identifier)
      } else {
        this.rateLimitTracking.set(identifier, recentRequests)
      }
    }
  }

  cleanupThreatLogs() {
    const cutoff = Date.now() - 86400000 // 24 hours
    this.threatLog = this.threatLog.filter(log => log.timestamp > cutoff)
  }

  // Security reporting and analytics
  getSecurityReport() {
    const now = Date.now()
    const oneHour = 60 * 60 * 1000
    const oneDay = 24 * oneHour
    
    const recentThreats = this.threatLog.filter(log => now - log.timestamp < oneHour)
    const dailyThreats = this.threatLog.filter(log => now - log.timestamp < oneDay)
    
    return {
      timestamp: now,
      summary: {
        totalValidations: this.securityMetrics.totalValidations,
        threatsDetected: this.securityMetrics.threatsDetected,
        threatsBlocked: this.securityMetrics.threatsBlocked,
        blockRate: this.securityMetrics.threatsDetected > 0 
          ? (this.securityMetrics.threatsBlocked / this.securityMetrics.threatsDetected * 100).toFixed(2) + '%'
          : '0%'
      },
      recent: {
        lastHour: recentThreats.length,
        lastDay: dailyThreats.length
      },
      byThreatType: Object.fromEntries(this.securityMetrics.byThreatType),
      topThreats: this.getTopThreats(dailyThreats),
      riskAssessment: this.assessSecurityRisk(dailyThreats),
      recommendations: this.generateSecurityRecommendations(dailyThreats)
    }
  }

  getTopThreats(threats) {
    const threatCounts = {}
    
    threats.forEach(log => {
      log.threats.forEach(threat => {
        threatCounts[threat.type] = (threatCounts[threat.type] || 0) + 1
      })
    })
    
    return Object.entries(threatCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([type, count]) => ({ type, count }))
  }

  assessSecurityRisk(threats) {
    if (threats.length === 0) return 'LOW'
    
    const criticalThreats = threats.filter(log => 
      log.threats.some(t => t.severity === SECURITY_LEVELS.CRITICAL)
    ).length
    
    const highThreats = threats.filter(log => 
      log.threats.some(t => t.severity === SECURITY_LEVELS.HIGH)
    ).length
    
    if (criticalThreats > 5) return 'CRITICAL'
    if (criticalThreats > 0 || highThreats > 10) return 'HIGH'
    if (highThreats > 0 || threats.length > 50) return 'MEDIUM'
    
    return 'LOW'
  }

  generateSecurityRecommendations(threats) {
    const recommendations = []
    
    const threatTypes = new Set()
    threats.forEach(log => {
      log.threats.forEach(threat => {
        threatTypes.add(threat.type)
      })
    })
    
    if (threatTypes.has(THREAT_TYPES.XSS)) {
      recommendations.push('Implement Content Security Policy (CSP) headers')
    }
    
    if (threatTypes.has(THREAT_TYPES.SQL_INJECTION)) {
      recommendations.push('Review database query parameterization')
    }
    
    if (threatTypes.has(THREAT_TYPES.RATE_LIMIT_ABUSE)) {
      recommendations.push('Consider implementing more aggressive rate limiting')
    }
    
    if (threats.length > 100) {
      recommendations.push('Consider implementing IP-based blocking for repeat offenders')
    }
    
    return recommendations
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Security Validator...')
    
    // Clear threat logs
    this.threatLog.length = 0
    
    // Clear tracking data
    this.rateLimitTracking.clear()
    this.blockedRequests.clear()
    this.suspiciousPatterns.clear()
    
    // Reset metrics
    this.securityMetrics = {
      totalValidations: 0,
      threatsDetected: 0,
      threatsBlocked: 0,
      falsePositives: 0,
      byThreatType: new Map(),
      bySecurityLevel: new Map()
    }
    
    this.isInitialized = false
    logger.info('✅ Security Validator cleanup complete')
  }
}

module.exports = {
  SecurityValidator,
  THREAT_TYPES,
  SECURITY_LEVELS,
  SECURITY_PATTERNS
}