/**
 * JAEGIS Cache Manager
 * Intelligent hybrid caching system with multiple storage backends
 * 
 * @version 2.0.0
 * @author JAEGIS Development Team
 */

const NodeCache = require('node-cache')
const redis = require('redis')
const crypto = require('crypto')
const logger = require('../utils/logger')

class CacheManager {
  constructor(config) {
    this.config = config
    this.memoryCache = null
    this.redisClient = null
    this.isInitialized = false
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      errors: 0
    }
    this.cleanupInterval = null
  }

  async initialize() {
    logger.info('💾 Initializing Cache Manager...')
    
    try {
      // Always initialize memory cache
      this.memoryCache = new NodeCache({
        stdTTL: this.config.duration / 1000, // Convert to seconds
        checkperiod: this.config.cleanup_interval / 1000,
        useClones: false,
        deleteOnExpire: true,
        maxKeys: this.config.max_size || 1000
      })

      // Setup memory cache event listeners
      this.memoryCache.on('set', (key, value) => {
        this.stats.sets++
        logger.cache('set', key, null, { backend: 'memory', size: this._getValueSize(value) })
      })

      this.memoryCache.on('del', (key, value) => {
        this.stats.deletes++
        logger.cache('delete', key, null, { backend: 'memory' })
      })

      this.memoryCache.on('expired', (key, value) => {
        logger.cache('expired', key, null, { backend: 'memory' })
      })

      // Initialize Redis if configured
      if (this.config.type === 'redis' && this.config.redis) {
        await this.initializeRedis()
      }

      // Setup periodic cleanup
      this.setupCleanup()

      this.isInitialized = true
      logger.info(`✅ Cache Manager initialized (${this.config.type} backend)`)

    } catch (error) {
      logger.error('❌ Failed to initialize Cache Manager:', error)
      throw error
    }
  }

  async initializeRedis() {
    try {
      const redisConfig = {
        host: this.config.redis.host,
        port: this.config.redis.port,
        db: this.config.redis.db || 0,
        retryDelayOnFailover: 100,
        enableReadyCheck: true,
        maxRetriesPerRequest: 3
      }

      if (this.config.redis.password) {
        redisConfig.password = this.config.redis.password
      }

      this.redisClient = redis.createClient(redisConfig)

      // Setup Redis event listeners
      this.redisClient.on('connect', () => {
        logger.info('🔗 Redis connected')
      })

      this.redisClient.on('ready', () => {
        logger.info('✅ Redis ready')
      })

      this.redisClient.on('error', (error) => {
        logger.error('❌ Redis error:', error)
        this.stats.errors++
      })

      this.redisClient.on('end', () => {
        logger.warn('🔌 Redis connection ended')
      })

      // Connect to Redis
      await this.redisClient.connect()

      // Test Redis connection
      await this.redisClient.ping()
      logger.info('🏓 Redis ping successful')

    } catch (error) {
      logger.error('❌ Redis initialization failed:', error)
      logger.warn('🔄 Falling back to memory cache only')
      this.config.type = 'memory'
    }
  }

  async get(key, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Cache Manager not initialized')
    }

    const cacheKey = this.generateKey(key, options.namespace)
    
    try {
      let value = null
      let backend = 'memory'

      // Try memory cache first (L1 cache)
      value = this.memoryCache.get(cacheKey)
      
      if (value !== undefined) {
        this.stats.hits++
        logger.cache('hit', cacheKey, true, { backend: 'memory' })
        return this.deserializeValue(value)
      }

      // Try Redis if available (L2 cache)
      if (this.redisClient && this.redisClient.isReady) {
        try {
          const redisValue = await this.redisClient.get(cacheKey)
          if (redisValue !== null) {
            value = JSON.parse(redisValue)
            backend = 'redis'
            
            // Populate memory cache for faster future access
            this.memoryCache.set(cacheKey, value, this.config.duration / 1000)
            
            this.stats.hits++
            logger.cache('hit', cacheKey, true, { backend: 'redis' })
            return this.deserializeValue(value)
          }
        } catch (redisError) {
          logger.error('Redis get error:', redisError)
          this.stats.errors++
        }
      }

      // Cache miss
      this.stats.misses++
      logger.cache('miss', cacheKey, false)
      return null

    } catch (error) {
      logger.error('Cache get error:', error)
      this.stats.errors++
      return null
    }
  }

  async set(key, value, ttl = null, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Cache Manager not initialized')
    }

    const cacheKey = this.generateKey(key, options.namespace)
    const serializedValue = this.serializeValue(value)
    const cacheTTL = ttl || this.config.duration

    try {
      // Set in memory cache (L1)
      this.memoryCache.set(cacheKey, serializedValue, cacheTTL / 1000)

      // Set in Redis if available (L2)
      if (this.redisClient && this.redisClient.isReady) {
        try {
          await this.redisClient.setEx(cacheKey, Math.floor(cacheTTL / 1000), JSON.stringify(serializedValue))
          logger.cache('set', cacheKey, null, { backend: 'redis', ttl: cacheTTL })
        } catch (redisError) {
          logger.error('Redis set error:', redisError)
          this.stats.errors++
        }
      }

      this.stats.sets++
      return true

    } catch (error) {
      logger.error('Cache set error:', error)
      this.stats.errors++
      return false
    }
  }

  async delete(key, options = {}) {
    if (!this.isInitialized) {
      throw new Error('Cache Manager not initialized')
    }

    const cacheKey = this.generateKey(key, options.namespace)

    try {
      // Delete from memory cache
      const memoryDeleted = this.memoryCache.del(cacheKey)

      // Delete from Redis if available
      let redisDeleted = 0
      if (this.redisClient && this.redisClient.isReady) {
        try {
          redisDeleted = await this.redisClient.del(cacheKey)
        } catch (redisError) {
          logger.error('Redis delete error:', redisError)
          this.stats.errors++
        }
      }

      const deleted = memoryDeleted > 0 || redisDeleted > 0
      if (deleted) {
        this.stats.deletes++
        logger.cache('delete', cacheKey, null, { memory: memoryDeleted, redis: redisDeleted })
      }

      return deleted

    } catch (error) {
      logger.error('Cache delete error:', error)
      this.stats.errors++
      return false
    }
  }

  async clear(pattern = null) {
    if (!this.isInitialized) {
      throw new Error('Cache Manager not initialized')
    }

    try {
      let cleared = 0

      if (pattern) {
        // Clear specific pattern
        cleared = await this.clearPattern(pattern)
      } else {
        // Clear all cache
        this.memoryCache.flushAll()
        cleared += this.memoryCache.getStats().keys

        if (this.redisClient && this.redisClient.isReady) {
          try {
            await this.redisClient.flushDb()
            logger.info('🧹 Redis cache cleared')
          } catch (redisError) {
            logger.error('Redis clear error:', redisError)
            this.stats.errors++
          }
        }
      }

      logger.info(`🧹 Cache cleared: ${cleared} entries`)
      return cleared

    } catch (error) {
      logger.error('Cache clear error:', error)
      this.stats.errors++
      return 0
    }
  }

  async clearPattern(pattern) {
    let cleared = 0

    try {
      // Clear from memory cache
      const memoryKeys = this.memoryCache.keys()
      for (const key of memoryKeys) {
        if (key.includes(pattern)) {
          this.memoryCache.del(key)
          cleared++
        }
      }

      // Clear from Redis
      if (this.redisClient && this.redisClient.isReady) {
        try {
          const redisKeys = await this.redisClient.keys(`*${pattern}*`)
          if (redisKeys.length > 0) {
            await this.redisClient.del(redisKeys)
            cleared += redisKeys.length
          }
        } catch (redisError) {
          logger.error('Redis pattern clear error:', redisError)
          this.stats.errors++
        }
      }

      return cleared

    } catch (error) {
      logger.error('Cache pattern clear error:', error)
      this.stats.errors++
      return 0
    }
  }

  async exists(key, options = {}) {
    if (!this.isInitialized) {
      return false
    }

    const cacheKey = this.generateKey(key, options.namespace)

    try {
      // Check memory cache first
      if (this.memoryCache.has(cacheKey)) {
        return true
      }

      // Check Redis if available
      if (this.redisClient && this.redisClient.isReady) {
        try {
          const exists = await this.redisClient.exists(cacheKey)
          return exists === 1
        } catch (redisError) {
          logger.error('Redis exists error:', redisError)
          this.stats.errors++
        }
      }

      return false

    } catch (error) {
      logger.error('Cache exists error:', error)
      this.stats.errors++
      return false
    }
  }

  async getTTL(key, options = {}) {
    if (!this.isInitialized) {
      return -1
    }

    const cacheKey = this.generateKey(key, options.namespace)

    try {
      // Check memory cache TTL
      const memoryTTL = this.memoryCache.getTtl(cacheKey)
      if (memoryTTL > 0) {
        return Math.floor((memoryTTL - Date.now()) / 1000)
      }

      // Check Redis TTL if available
      if (this.redisClient && this.redisClient.isReady) {
        try {
          const redisTTL = await this.redisClient.ttl(cacheKey)
          return redisTTL
        } catch (redisError) {
          logger.error('Redis TTL error:', redisError)
          this.stats.errors++
        }
      }

      return -1

    } catch (error) {
      logger.error('Cache TTL error:', error)
      this.stats.errors++
      return -1
    }
  }

  generateKey(key, namespace = null) {
    const prefix = this.config.key_prefix || 'jaegis'
    const parts = [prefix]
    
    if (namespace) {
      parts.push(namespace)
    }
    
    parts.push(key)
    
    return parts.join(':')
  }

  serializeValue(value) {
    return {
      data: value,
      timestamp: Date.now(),
      type: typeof value
    }
  }

  deserializeValue(serialized) {
    if (serialized && typeof serialized === 'object' && 'data' in serialized) {
      return serialized.data
    }
    return serialized
  }

  _getValueSize(value) {
    try {
      return JSON.stringify(value).length
    } catch {
      return 0
    }
  }

  getStats() {
    const memoryStats = this.memoryCache ? this.memoryCache.getStats() : {}
    
    return {
      ...this.stats,
      memory: {
        keys: memoryStats.keys || 0,
        hits: memoryStats.hits || 0,
        misses: memoryStats.misses || 0,
        ksize: memoryStats.ksize || 0,
        vsize: memoryStats.vsize || 0
      },
      redis: {
        connected: this.redisClient ? this.redisClient.isReady : false,
        enabled: this.config.type === 'redis'
      },
      hitRate: this.stats.hits + this.stats.misses > 0 
        ? (this.stats.hits / (this.stats.hits + this.stats.misses) * 100).toFixed(2) + '%'
        : '0%'
    }
  }

  async healthCheck() {
    const health = {
      status: 'healthy',
      backends: {
        memory: {
          status: 'healthy',
          keys: this.memoryCache ? this.memoryCache.keys().length : 0
        }
      },
      stats: this.getStats()
    }

    // Check Redis health
    if (this.config.type === 'redis') {
      try {
        if (this.redisClient && this.redisClient.isReady) {
          await this.redisClient.ping()
          health.backends.redis = {
            status: 'healthy',
            connected: true
          }
        } else {
          health.backends.redis = {
            status: 'unhealthy',
            connected: false,
            error: 'Not connected'
          }
          health.status = 'degraded'
        }
      } catch (error) {
        health.backends.redis = {
          status: 'unhealthy',
          connected: false,
          error: error.message
        }
        health.status = 'degraded'
      }
    }

    return health
  }

  setupCleanup() {
    if (this.config.cleanup_interval && this.config.cleanup_interval > 0) {
      this.cleanupInterval = setInterval(() => {
        this.performCleanup()
      }, this.config.cleanup_interval)
      
      logger.info(`🧹 Cache cleanup scheduled every ${this.config.cleanup_interval / 1000}s`)
    }
  }

  async performCleanup() {
    try {
      // Memory cache cleanup is automatic via node-cache
      
      // Redis cleanup (remove expired keys)
      if (this.redisClient && this.redisClient.isReady) {
        // Redis handles expiration automatically, but we can check connection
        await this.redisClient.ping()
      }
      
      logger.debug('🧹 Cache cleanup completed')
      
    } catch (error) {
      logger.error('Cache cleanup error:', error)
      this.stats.errors++
    }
  }

  async warmup(data) {
    logger.info('🔥 Warming up cache...')
    
    let warmed = 0
    
    for (const [key, value] of Object.entries(data)) {
      try {
        await this.set(key, value)
        warmed++
      } catch (error) {
        logger.error(`Cache warmup error for key ${key}:`, error)
      }
    }
    
    logger.info(`🔥 Cache warmed up with ${warmed} entries`)
    return warmed
  }

  async backup() {
    logger.info('💾 Creating cache backup...')
    
    const backup = {
      timestamp: Date.now(),
      config: this.config,
      data: {}
    }
    
    try {
      // Backup memory cache
      const memoryKeys = this.memoryCache.keys()
      for (const key of memoryKeys) {
        const value = this.memoryCache.get(key)
        const ttl = this.memoryCache.getTtl(key)
        
        backup.data[key] = {
          value,
          ttl: ttl > 0 ? Math.floor((ttl - Date.now()) / 1000) : -1
        }
      }
      
      logger.info(`💾 Cache backup created with ${Object.keys(backup.data).length} entries`)
      return backup
      
    } catch (error) {
      logger.error('Cache backup error:', error)
      throw error
    }
  }

  async restore(backup) {
    logger.info('🔄 Restoring cache from backup...')
    
    let restored = 0
    
    try {
      for (const [key, item] of Object.entries(backup.data)) {
        const ttl = item.ttl > 0 ? item.ttl * 1000 : this.config.duration
        await this.set(key, item.value, ttl)
        restored++
      }
      
      logger.info(`🔄 Cache restored with ${restored} entries`)
      return restored
      
    } catch (error) {
      logger.error('Cache restore error:', error)
      throw error
    }
  }

  async cleanup() {
    logger.info('🧹 Cleaning up Cache Manager...')
    
    // Clear cleanup interval
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval)
      this.cleanupInterval = null
    }
    
    // Close Redis connection
    if (this.redisClient) {
      try {
        await this.redisClient.quit()
        logger.info('🔌 Redis connection closed')
      } catch (error) {
        logger.error('Redis cleanup error:', error)
      }
      this.redisClient = null
    }
    
    // Clear memory cache
    if (this.memoryCache) {
      this.memoryCache.flushAll()
      this.memoryCache.close()
      this.memoryCache = null
    }
    
    this.isInitialized = false
    logger.info('✅ Cache Manager cleanup complete')
  }
}

module.exports = CacheManager