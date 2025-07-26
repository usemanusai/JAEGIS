/**
 * JAEGIS Logger Utility
 * Centralized logging system with multiple transports
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const winston = require('winston')
const path = require('path')
const fs = require('fs')

// Ensure logs directory exists
const logsDir = path.join(process.cwd(), 'logs')
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true })
}

// Custom format for console output
const consoleFormat = winston.format.combine(
  winston.format.timestamp({ format: 'HH:mm:ss' }),
  winston.format.colorize(),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    let log = `${timestamp} [${level}] ${message}`
    
    // Add metadata if present
    if (Object.keys(meta).length > 0) {
      log += ` ${JSON.stringify(meta)}`
    }
    
    return log
  })
)

// Custom format for file output
const fileFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
)

// Create logger instance
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: fileFormat,
  defaultMeta: {
    service: 'jaegis',
    version: '2.0.0',
    pid: process.pid
  },
  transports: [
    // Console transport
    new winston.transports.Console({
      format: consoleFormat,
      level: process.env.NODE_ENV === 'production' ? 'warn' : 'debug'
    }),
    
    // File transport for all logs
    new winston.transports.File({
      filename: path.join(logsDir, 'jaegis.log'),
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5,
      tailable: true
    }),
    
    // File transport for errors only
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5,
      tailable: true
    })
  ],
  
  // Handle uncaught exceptions
  exceptionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'exceptions.log')
    })
  ],
  
  // Handle unhandled rejections
  rejectionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'rejections.log')
    })
  ]
})

// Add request logging middleware
logger.requestLogger = (req, res, next) => {
  const start = Date.now()
  
  res.on('finish', () => {
    const duration = Date.now() - start
    const logData = {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
      userAgent: req.get('User-Agent'),
      ip: req.ip || req.connection.remoteAddress
    }
    
    if (res.statusCode >= 400) {
      logger.warn('HTTP Request', logData)
    } else {
      logger.info('HTTP Request', logData)
    }
  })
  
  next()
}

// Add performance logging
logger.performance = (operation, duration, metadata = {}) => {
  logger.info('Performance', {
    operation,
    duration: `${duration}ms`,
    ...metadata
  })
}

// Add structured logging methods
logger.command = (command, result, metadata = {}) => {
  logger.info('Command Execution', {
    command,
    success: result.success,
    processingTime: result.processingTime,
    ...metadata
  })
}

logger.github = (action, url, result, metadata = {}) => {
  logger.info('GitHub Operation', {
    action,
    url,
    success: result.success,
    ...metadata
  })
}

logger.cache = (action, key, hit = null, metadata = {}) => {
  logger.debug('Cache Operation', {
    action,
    key,
    hit,
    ...metadata
  })
}

logger.python = (action, result, metadata = {}) => {
  logger.info('Python Bridge', {
    action,
    success: result.success,
    ...metadata
  })
}

// Add development helpers
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    level: 'debug',
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }))
}

module.exports = logger