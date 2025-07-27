/**
 * N.L.D.S. JavaScript SDK
 * JAEGIS Enhanced Agent System v2.2 - Tier 0 Component
 * 
 * Official JavaScript/Node.js client SDK for the N.L.D.S. API with comprehensive
 * features, error handling, and developer-friendly interface.
 */

const axios = require('axios');
const WebSocket = require('ws');
const EventEmitter = require('events');

// ============================================================================
// CONSTANTS AND ENUMS
// ============================================================================

const ProcessingMode = {
    STANDARD: 'standard',
    ENHANCED: 'enhanced',
    COMPREHENSIVE: 'comprehensive',
    FAST: 'fast'
};

const AnalysisType = {
    LOGICAL: 'logical',
    EMOTIONAL: 'emotional',
    CREATIVE: 'creative',
    COMPREHENSIVE: 'comprehensive'
};

// ============================================================================
// EXCEPTIONS
// ============================================================================

class NLDSError extends Error {
    constructor(message, errorCode = null, details = null) {
        super(message);
        this.name = 'NLDSError';
        this.errorCode = errorCode;
        this.details = details || {};
    }
}

class AuthenticationError extends NLDSError {
    constructor(message, ...args) {
        super(message, ...args);
        this.name = 'AuthenticationError';
    }
}

class RateLimitError extends NLDSError {
    constructor(message, retryAfter = null, ...args) {
        super(message, ...args);
        this.name = 'RateLimitError';
        this.retryAfter = retryAfter;
    }
}

class ValidationError extends NLDSError {
    constructor(message, ...args) {
        super(message, ...args);
        this.name = 'ValidationError';
    }
}

class ProcessingError extends NLDSError {
    constructor(message, ...args) {
        super(message, ...args);
        this.name = 'ProcessingError';
    }
}

class NetworkError extends NLDSError {
    constructor(message, ...args) {
        super(message, ...args);
        this.name = 'NetworkError';
    }
}

// ============================================================================
// CONFIGURATION
// ============================================================================

class NLDSConfig {
    constructor(options = {}) {
        this.apiKey = options.apiKey || '';
        this.baseUrl = options.baseUrl || 'https://api.nlds.jaegis.ai';
        this.timeout = options.timeout || 30000;
        this.maxRetries = options.maxRetries || 3;
        this.retryDelay = options.retryDelay || 1000;
        this.userAgent = options.userAgent || 'NLDS-JS-SDK/2.2.0';
        this.validateSSL = options.validateSSL !== false;
    }
}

// ============================================================================
// MAIN CLIENT CLASS
// ============================================================================

class NLDSClient extends EventEmitter {
    /**
     * N.L.D.S. API client for JavaScript/Node.js
     * 
     * Features:
     * - Complete API coverage
     * - Automatic retries with exponential backoff
     * - Rate limit handling
     * - WebSocket real-time communication
     * - Comprehensive error handling
     * - Event-driven architecture
     */
    
    constructor(config) {
        super();
        
        if (typeof config === 'string') {
            // If config is just an API key string
            this.config = new NLDSConfig({ apiKey: config });
        } else {
            this.config = new NLDSConfig(config || {});
        }
        
        // Validate API key
        if (!this.config.apiKey) {
            throw new AuthenticationError('API key is required');
        }
        
        // Setup axios instance
        this.http = axios.create({
            baseURL: this.config.baseUrl,
            timeout: this.config.timeout,
            headers: {
                'Authorization': `Bearer ${this.config.apiKey}`,
                'Content-Type': 'application/json',
                'User-Agent': this.config.userAgent,
                'Accept': 'application/json'
            },
            validateStatus: () => true // Handle all status codes manually
        });
        
        // WebSocket connection
        this.websocket = null;
        this.isConnected = false;
        
        // Request interceptor for logging
        this.http.interceptors.request.use(
            (config) => {
                this.emit('request', {
                    method: config.method,
                    url: config.url,
                    timestamp: new Date().toISOString()
                });
                return config;
            },
            (error) => {
                this.emit('error', error);
                return Promise.reject(error);
            }
        );
        
        // Response interceptor for logging
        this.http.interceptors.response.use(
            (response) => {
                this.emit('response', {
                    status: response.status,
                    url: response.config.url,
                    responseTime: response.headers['x-response-time'],
                    timestamp: new Date().toISOString()
                });
                return response;
            },
            (error) => {
                this.emit('error', error);
                return Promise.reject(error);
            }
        );
    }
    
    /**
     * Process natural language input
     * 
     * @param {Object} request - Processing request
     * @param {string} request.inputText - Input text to process
     * @param {string} [request.mode] - Processing mode
     * @param {Object} [request.context] - Additional context
     * @param {Object} [request.userPreferences] - User preferences
     * @param {boolean} [request.enableAmasiap] - Enable A.M.A.S.I.A.P. protocol
     * @returns {Promise<Object>} Processing result
     */
    async process(request) {
        try {
            const requestData = {
                input_text: request.inputText,
                mode: request.mode || ProcessingMode.STANDARD,
                context: request.context || null,
                user_preferences: request.userPreferences || null,
                enable_amasiap: request.enableAmasiap !== false
            };
            
            const response = await this._makeRequest('POST', '/process', requestData);
            
            this.emit('processing_complete', {
                requestId: response.request_id,
                success: response.success,
                processingTime: response.processing_time_ms
            });
            
            return response;
            
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new ProcessingError(`Processing failed: ${error.message}`);
        }
    }
    
    /**
     * Perform detailed analysis
     * 
     * @param {Object} request - Analysis request
     * @param {string} request.inputText - Text to analyze
     * @param {Array<string>} [request.analysisTypes] - Types of analysis
     * @param {number} [request.depthLevel] - Analysis depth (1-5)
     * @param {boolean} [request.includeMetadata] - Include metadata
     * @returns {Promise<Object>} Analysis result
     */
    async analyze(request) {
        try {
            const requestData = {
                input_text: request.inputText,
                analysis_types: request.analysisTypes || [AnalysisType.COMPREHENSIVE],
                depth_level: request.depthLevel || 3,
                include_metadata: request.includeMetadata !== false
            };
            
            const response = await this._makeRequest('POST', '/analyze', requestData);
            
            // Parse timestamp
            response.timestamp = new Date(response.timestamp);
            
            this.emit('analysis_complete', {
                requestId: response.request_id,
                processingTime: response.processing_time_ms
            });
            
            return response;
            
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new ProcessingError(`Analysis failed: ${error.message}`);
        }
    }
    
    /**
     * Translate to JAEGIS commands
     * 
     * @param {string} inputText - Input text to translate
     * @param {Object} [options] - Translation options
     * @param {number} [options.targetMode] - Preferred JAEGIS mode
     * @param {string} [options.preferredSquad] - Preferred squad
     * @param {string} [options.priority] - Command priority
     * @returns {Promise<Object>} Translation result
     */
    async translate(inputText, options = {}) {
        try {
            const requestData = {
                input_text: inputText,
                target_mode: options.targetMode || null,
                preferred_squad: options.preferredSquad || null,
                priority: options.priority || 'normal'
            };
            
            const response = await this._makeRequest('POST', '/translate', requestData);
            
            this.emit('translation_complete', {
                requestId: response.request_id,
                processingTime: response.processing_time_ms
            });
            
            return response;
            
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new ProcessingError(`Translation failed: ${error.message}`);
        }
    }
    
    /**
     * Submit command to JAEGIS
     * 
     * @param {Object} command - JAEGIS command
     * @param {Object} [options] - Submission options
     * @param {string} [options.priority] - Command priority
     * @param {number} [options.timeoutSeconds] - Command timeout
     * @returns {Promise<Object>} Submission result
     */
    async submitCommand(command, options = {}) {
        try {
            const requestData = {
                command: command,
                priority: options.priority || 'normal',
                timeout_seconds: options.timeoutSeconds || 300
            };
            
            const response = await this._makeRequest('POST', '/jaegis/submit', requestData);
            
            this.emit('command_submitted', {
                commandId: response.command_id,
                status: response.status
            });
            
            return response;
            
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new ProcessingError(`Command submission failed: ${error.message}`);
        }
    }
    
    /**
     * Get command status
     * 
     * @param {string} commandId - Command ID
     * @returns {Promise<Object>} Command status
     */
    async getCommandStatus(commandId) {
        try {
            const response = await this._makeRequest('GET', `/jaegis/status/${commandId}`);
            
            this.emit('status_checked', {
                commandId: commandId,
                status: response.status,
                progress: response.progress_percentage
            });
            
            return response;
            
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new ProcessingError(`Status check failed: ${error.message}`);
        }
    }
    
    /**
     * Get system health
     * 
     * @returns {Promise<Object>} Health status
     */
    async getHealth() {
        try {
            return await this._makeRequest('GET', '/health');
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new NetworkError(`Health check failed: ${error.message}`);
        }
    }
    
    /**
     * Get system status
     * 
     * @returns {Promise<Object>} System status
     */
    async getStatus() {
        try {
            return await this._makeRequest('GET', '/status');
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new NetworkError(`Status check failed: ${error.message}`);
        }
    }
    
    /**
     * Get system metrics
     * 
     * @returns {Promise<Object>} System metrics
     */
    async getMetrics() {
        try {
            return await this._makeRequest('GET', '/metrics');
        } catch (error) {
            if (error instanceof NLDSError) {
                throw error;
            }
            throw new NetworkError(`Metrics retrieval failed: ${error.message}`);
        }
    }
    
    /**
     * Connect to WebSocket for real-time updates
     * 
     * @returns {Promise<void>}
     */
    async connectWebSocket() {
        return new Promise((resolve, reject) => {
            try {
                const wsUrl = this.config.baseUrl.replace(/^http/, 'ws') + '/ws';
                
                this.websocket = new WebSocket(wsUrl, {
                    headers: {
                        'Authorization': `Bearer ${this.config.apiKey}`
                    }
                });
                
                this.websocket.on('open', () => {
                    this.isConnected = true;
                    this.emit('websocket_connected');
                    resolve();
                });
                
                this.websocket.on('message', (data) => {
                    try {
                        const message = JSON.parse(data);
                        this.emit('websocket_message', message);
                        
                        // Emit specific events based on message type
                        if (message.message_type) {
                            this.emit(`websocket_${message.message_type}`, message);
                        }
                    } catch (error) {
                        this.emit('websocket_error', new Error(`Invalid JSON received: ${data}`));
                    }
                });
                
                this.websocket.on('close', () => {
                    this.isConnected = false;
                    this.emit('websocket_disconnected');
                });
                
                this.websocket.on('error', (error) => {
                    this.emit('websocket_error', error);
                    reject(new NetworkError(`WebSocket connection failed: ${error.message}`));
                });
                
            } catch (error) {
                reject(new NetworkError(`WebSocket setup failed: ${error.message}`));
            }
        });
    }
    
    /**
     * Send message via WebSocket
     * 
     * @param {Object} message - Message to send
     * @returns {Promise<void>}
     */
    async sendWebSocketMessage(message) {
        if (!this.isConnected || !this.websocket) {
            throw new NetworkError('WebSocket not connected');
        }
        
        try {
            this.websocket.send(JSON.stringify(message));
        } catch (error) {
            throw new NetworkError(`Failed to send WebSocket message: ${error.message}`);
        }
    }
    
    /**
     * Disconnect WebSocket
     */
    disconnectWebSocket() {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
            this.isConnected = false;
        }
    }
    
    /**
     * Make HTTP request with retries and error handling
     * 
     * @private
     * @param {string} method - HTTP method
     * @param {string} endpoint - API endpoint
     * @param {Object} [data] - Request data
     * @param {Object} [params] - Query parameters
     * @returns {Promise<Object>} Response data
     */
    async _makeRequest(method, endpoint, data = null, params = null) {
        let lastError;
        
        for (let attempt = 0; attempt <= this.config.maxRetries; attempt++) {
            try {
                const config = {
                    method: method.toLowerCase(),
                    url: endpoint,
                    params: params
                };
                
                if (data && ['post', 'put', 'patch'].includes(method.toLowerCase())) {
                    config.data = data;
                }
                
                const response = await this.http.request(config);
                
                // Handle response status
                if (response.status === 200) {
                    return response.data;
                } else if (response.status === 401) {
                    throw new AuthenticationError('Invalid API key or authentication failed');
                } else if (response.status === 403) {
                    throw new AuthenticationError('Insufficient permissions');
                } else if (response.status === 429) {
                    const retryAfter = parseInt(response.headers['retry-after'] || '60');
                    throw new RateLimitError('Rate limit exceeded', retryAfter);
                } else if (response.status === 400) {
                    const errorData = response.data || {};
                    throw new ValidationError(
                        errorData.error?.message || 'Validation failed',
                        400,
                        errorData
                    );
                } else if (response.status >= 500) {
                    if (attempt < this.config.maxRetries) {
                        // Retry on server errors
                        await this._sleep(this.config.retryDelay * Math.pow(2, attempt));
                        continue;
                    } else {
                        const errorData = response.data || {};
                        throw new NetworkError(
                            `Server error: ${response.status}`,
                            response.status,
                            errorData
                        );
                    }
                } else {
                    const errorData = response.data || {};
                    throw new NLDSError(
                        `Request failed: ${response.status}`,
                        response.status,
                        errorData
                    );
                }
                
            } catch (error) {
                lastError = error;
                
                if (error instanceof NLDSError) {
                    throw error;
                }
                
                if (attempt < this.config.maxRetries) {
                    await this._sleep(this.config.retryDelay * Math.pow(2, attempt));
                    continue;
                } else {
                    throw new NetworkError(`Network error: ${error.message}`);
                }
            }
        }
        
        throw new NetworkError('Max retries exceeded');
    }
    
    /**
     * Sleep for specified milliseconds
     * 
     * @private
     * @param {number} ms - Milliseconds to sleep
     * @returns {Promise<void>}
     */
    _sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * Close client and cleanup resources
     */
    close() {
        this.disconnectWebSocket();
        this.removeAllListeners();
    }
}

// ============================================================================
// CONVENIENCE FUNCTIONS
// ============================================================================

/**
 * Create N.L.D.S. client with default configuration
 * 
 * @param {string|Object} config - API key string or configuration object
 * @returns {NLDSClient} N.L.D.S. client
 */
function createClient(config) {
    return new NLDSClient(config);
}

/**
 * Quick processing function
 * 
 * @param {string} apiKey - API key
 * @param {string} inputText - Input text to process
 * @param {Object} [options] - Processing options
 * @returns {Promise<Object>} Processing result
 */
async function quickProcess(apiKey, inputText, options = {}) {
    const client = createClient(apiKey);
    try {
        return await client.process({
            inputText: inputText,
            ...options
        });
    } finally {
        client.close();
    }
}

/**
 * Quick analysis function
 * 
 * @param {string} apiKey - API key
 * @param {string} inputText - Text to analyze
 * @param {Object} [options] - Analysis options
 * @returns {Promise<Object>} Analysis result
 */
async function quickAnalyze(apiKey, inputText, options = {}) {
    const client = createClient(apiKey);
    try {
        return await client.analyze({
            inputText: inputText,
            ...options
        });
    } finally {
        client.close();
    }
}

// ============================================================================
// EXPORTS
// ============================================================================

module.exports = {
    NLDSClient,
    NLDSConfig,
    NLDSError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ProcessingError,
    NetworkError,
    ProcessingMode,
    AnalysisType,
    createClient,
    quickProcess,
    quickAnalyze
};

// ============================================================================
// EXAMPLE USAGE
// ============================================================================

if (require.main === module) {
    // Example usage
    const apiKey = process.env.NLDS_API_KEY || 'your_api_key_here';
    
    async function example() {
        const client = createClient(apiKey);
        
        try {
            // Set up event listeners
            client.on('processing_complete', (data) => {
                console.log('Processing completed:', data);
            });
            
            client.on('error', (error) => {
                console.error('Client error:', error);
            });
            
            // Process input
            const result = await client.process({
                inputText: 'Analyze the current market trends for renewable energy',
                mode: ProcessingMode.ENHANCED,
                enableAmasiap: true
            });
            
            console.log('Processing successful:', result.success);
            console.log('Enhanced input:', result.enhanced_input);
            console.log('Confidence:', result.confidence_score);
            
            // Connect to WebSocket for real-time updates
            await client.connectWebSocket();
            
            client.on('websocket_message', (message) => {
                console.log('WebSocket message:', message);
            });
            
            // Send a test message
            await client.sendWebSocketMessage({
                message_type: 'heartbeat',
                timestamp: new Date().toISOString()
            });
            
        } catch (error) {
            console.error('Example error:', error);
        } finally {
            client.close();
        }
    }
    
    // Run example (uncomment to test)
    // example().catch(console.error);
}
