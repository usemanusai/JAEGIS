-- N.L.D.S. Database Schema Design
-- JAEGIS Enhanced Agent System v2.2 - Tier 0 Component
-- PostgreSQL 15+ with JSONB support

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create custom types
CREATE TYPE input_type AS ENUM ('text', 'voice', 'command', 'conversation');
CREATE TYPE confidence_level AS ENUM ('high', 'medium', 'low');
CREATE TYPE processing_status AS ENUM ('pending', 'processing', 'completed', 'failed');
CREATE TYPE user_role AS ENUM ('user', 'admin', 'developer', 'analyst');

-- ============================================================================
-- USER MANAGEMENT TABLES
-- ============================================================================

-- User profiles table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    role user_role DEFAULT 'user',
    
    -- User preferences and settings
    preferences JSONB DEFAULT '{}',
    cognitive_patterns JSONB DEFAULT '{}',
    behavior_patterns JSONB DEFAULT '{}',
    
    -- Learning and adaptation data
    learning_data JSONB DEFAULT '{}',
    interaction_history JSONB DEFAULT '{}',
    
    -- Metadata
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_preferences CHECK (jsonb_typeof(preferences) = 'object'),
    CONSTRAINT valid_cognitive_patterns CHECK (jsonb_typeof(cognitive_patterns) = 'object'),
    CONSTRAINT valid_behavior_patterns CHECK (jsonb_typeof(behavior_patterns) = 'object')
);

-- User authentication table
CREATE TABLE user_authentication (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    
    -- Authentication methods
    password_hash VARCHAR(255),
    salt VARCHAR(255),
    
    -- OAuth tokens
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    oauth_data JSONB DEFAULT '{}',
    
    -- API keys
    api_key_hash VARCHAR(255),
    api_key_expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Security
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- SESSION MANAGEMENT TABLES
-- ============================================================================

-- Conversation sessions table
CREATE TABLE conversation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    
    -- Session data
    context_data JSONB DEFAULT '{}',
    conversation_history JSONB DEFAULT '[]',
    user_state JSONB DEFAULT '{}',
    
    -- Session metadata
    ip_address INET,
    user_agent TEXT,
    device_info JSONB DEFAULT '{}',
    
    -- Timing
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP + INTERVAL '24 hours'),
    ended_at TIMESTAMP WITH TIME ZONE,
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Constraints
    CONSTRAINT valid_context_data CHECK (jsonb_typeof(context_data) = 'object'),
    CONSTRAINT valid_conversation_history CHECK (jsonb_typeof(conversation_history) = 'array'),
    CONSTRAINT valid_expires_at CHECK (expires_at > started_at)
);

-- ============================================================================
-- PROCESSING TABLES
-- ============================================================================

-- Input processing requests table
CREATE TABLE processing_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) NOT NULL REFERENCES conversation_sessions(session_id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    
    -- Input data
    input_text TEXT NOT NULL,
    input_type input_type NOT NULL,
    input_metadata JSONB DEFAULT '{}',
    
    -- Processing results
    nlp_analysis JSONB DEFAULT '{}',
    dimensional_analysis JSONB DEFAULT '{}',
    human_processing JSONB DEFAULT '{}',
    translation_result JSONB DEFAULT '{}',
    
    -- Confidence and quality metrics
    confidence_score DECIMAL(5,2),
    confidence_level confidence_level,
    quality_metrics JSONB DEFAULT '{}',
    
    -- Processing status and timing
    status processing_status DEFAULT 'pending',
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processing_completed_at TIMESTAMP WITH TIME ZONE,
    processing_time_ms INTEGER,
    
    -- JAEGIS integration
    selected_mode INTEGER,
    selected_squads TEXT[],
    jaegis_commands JSONB DEFAULT '[]',
    execution_result JSONB DEFAULT '{}',
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_confidence_score CHECK (confidence_score >= 0 AND confidence_score <= 100),
    CONSTRAINT valid_processing_time CHECK (processing_time_ms >= 0),
    CONSTRAINT valid_mode CHECK (selected_mode >= 1 AND selected_mode <= 5)
);

-- ============================================================================
-- ANALYTICS AND METRICS TABLES
-- ============================================================================

-- System performance metrics table
CREATE TABLE performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Metric identification
    metric_name VARCHAR(100) NOT NULL,
    metric_category VARCHAR(50) NOT NULL,
    
    -- Metric values
    metric_value DECIMAL(15,6) NOT NULL,
    metric_unit VARCHAR(20),
    metric_tags JSONB DEFAULT '{}',
    
    -- Context
    session_id VARCHAR(255),
    user_id VARCHAR(255),
    component_name VARCHAR(100),
    
    -- Timing
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_metric_tags CHECK (jsonb_typeof(metric_tags) = 'object')
);

-- User interaction analytics table
CREATE TABLE user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    session_id VARCHAR(255) REFERENCES conversation_sessions(session_id) ON DELETE CASCADE,
    
    -- Interaction data
    interaction_type VARCHAR(50) NOT NULL,
    interaction_data JSONB DEFAULT '{}',
    
    -- Success metrics
    success_rate DECIMAL(5,2),
    satisfaction_score DECIMAL(3,1),
    completion_time_ms INTEGER,
    
    -- Learning metrics
    learning_progress JSONB DEFAULT '{}',
    adaptation_metrics JSONB DEFAULT '{}',
    
    -- Timing
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_success_rate CHECK (success_rate >= 0 AND success_rate <= 100),
    CONSTRAINT valid_satisfaction_score CHECK (satisfaction_score >= 0 AND satisfaction_score <= 10)
);

-- ============================================================================
-- LEARNING AND ADAPTATION TABLES
-- ============================================================================

-- User feedback table
CREATE TABLE user_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    processing_request_id UUID REFERENCES processing_requests(id) ON DELETE CASCADE,
    
    -- Feedback data
    feedback_type VARCHAR(50) NOT NULL,
    feedback_score INTEGER,
    feedback_text TEXT,
    feedback_data JSONB DEFAULT '{}',
    
    -- Context
    context_data JSONB DEFAULT '{}',
    
    -- Processing
    is_processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_feedback_score CHECK (feedback_score >= 1 AND feedback_score <= 5)
);

-- Model training data table
CREATE TABLE training_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Data identification
    data_type VARCHAR(50) NOT NULL,
    data_source VARCHAR(100) NOT NULL,
    
    -- Training data
    input_data JSONB NOT NULL,
    expected_output JSONB NOT NULL,
    actual_output JSONB,
    
    -- Quality metrics
    quality_score DECIMAL(5,2),
    validation_status VARCHAR(20) DEFAULT 'pending',
    
    -- Model information
    model_name VARCHAR(100),
    model_version VARCHAR(20),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    validated_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_quality_score CHECK (quality_score >= 0 AND quality_score <= 100)
);

-- ============================================================================
-- SYSTEM CONFIGURATION TABLES
-- ============================================================================

-- System configuration table
CREATE TABLE system_configuration (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Configuration identification
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_category VARCHAR(100) NOT NULL,
    
    -- Configuration data
    config_value JSONB NOT NULL,
    config_description TEXT,
    
    -- Metadata
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(255),
    
    -- Constraints
    CONSTRAINT valid_config_value CHECK (jsonb_typeof(config_value) IN ('object', 'array', 'string', 'number', 'boolean'))
);

-- API usage tracking table
CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Request identification
    request_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) REFERENCES user_profiles(user_id) ON DELETE SET NULL,
    api_key_hash VARCHAR(255),
    
    -- Request data
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    request_size_bytes INTEGER,
    response_size_bytes INTEGER,
    
    -- Response data
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER NOT NULL,
    
    -- Rate limiting
    rate_limit_remaining INTEGER,
    rate_limit_reset_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_status_code CHECK (status_code >= 100 AND status_code < 600),
    CONSTRAINT valid_response_time CHECK (response_time_ms >= 0)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- User profiles indexes
CREATE INDEX CONCURRENTLY idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX CONCURRENTLY idx_user_profiles_email ON user_profiles(email);
CREATE INDEX CONCURRENTLY idx_user_profiles_active ON user_profiles(is_active);
CREATE INDEX CONCURRENTLY idx_user_profiles_preferences_gin ON user_profiles USING GIN (preferences);

-- Session indexes
CREATE INDEX CONCURRENTLY idx_conversation_sessions_session_id ON conversation_sessions(session_id);
CREATE INDEX CONCURRENTLY idx_conversation_sessions_user_id ON conversation_sessions(user_id);
CREATE INDEX CONCURRENTLY idx_conversation_sessions_active ON conversation_sessions(is_active);
CREATE INDEX CONCURRENTLY idx_conversation_sessions_expires_at ON conversation_sessions(expires_at);
CREATE INDEX CONCURRENTLY idx_conversation_sessions_context_gin ON conversation_sessions USING GIN (context_data);

-- Processing requests indexes
CREATE INDEX CONCURRENTLY idx_processing_requests_session_id ON processing_requests(session_id);
CREATE INDEX CONCURRENTLY idx_processing_requests_user_id ON processing_requests(user_id);
CREATE INDEX CONCURRENTLY idx_processing_requests_status ON processing_requests(status);
CREATE INDEX CONCURRENTLY idx_processing_requests_confidence ON processing_requests(confidence_score);
CREATE INDEX CONCURRENTLY idx_processing_requests_created_at ON processing_requests(created_at);
CREATE INDEX CONCURRENTLY idx_processing_requests_text_search ON processing_requests USING GIN (to_tsvector('english', input_text));

-- Performance metrics indexes
CREATE INDEX CONCURRENTLY idx_performance_metrics_name ON performance_metrics(metric_name);
CREATE INDEX CONCURRENTLY idx_performance_metrics_category ON performance_metrics(metric_category);
CREATE INDEX CONCURRENTLY idx_performance_metrics_recorded_at ON performance_metrics(recorded_at);
CREATE INDEX CONCURRENTLY idx_performance_metrics_tags_gin ON performance_metrics USING GIN (metric_tags);

-- Analytics indexes
CREATE INDEX CONCURRENTLY idx_user_analytics_user_id ON user_analytics(user_id);
CREATE INDEX CONCURRENTLY idx_user_analytics_type ON user_analytics(interaction_type);
CREATE INDEX CONCURRENTLY idx_user_analytics_recorded_at ON user_analytics(recorded_at);

-- API usage indexes
CREATE INDEX CONCURRENTLY idx_api_usage_user_id ON api_usage(user_id);
CREATE INDEX CONCURRENTLY idx_api_usage_endpoint ON api_usage(endpoint);
CREATE INDEX CONCURRENTLY idx_api_usage_created_at ON api_usage(created_at);
CREATE INDEX CONCURRENTLY idx_api_usage_status_code ON api_usage(status_code);

-- ============================================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_authentication_updated_at BEFORE UPDATE ON user_authentication FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_system_configuration_updated_at BEFORE UPDATE ON system_configuration FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update last_activity_at for sessions
CREATE OR REPLACE FUNCTION update_session_activity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversation_sessions 
    SET last_activity_at = CURRENT_TIMESTAMP 
    WHERE session_id = NEW.session_id;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to update session activity on new processing requests
CREATE TRIGGER update_session_activity_trigger 
    AFTER INSERT ON processing_requests 
    FOR EACH ROW EXECUTE FUNCTION update_session_activity();

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Active user sessions view
CREATE VIEW active_user_sessions AS
SELECT 
    cs.session_id,
    cs.user_id,
    up.email,
    cs.started_at,
    cs.last_activity_at,
    cs.expires_at,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - cs.last_activity_at)) / 60 AS minutes_since_activity
FROM conversation_sessions cs
JOIN user_profiles up ON cs.user_id = up.user_id
WHERE cs.is_active = true 
  AND cs.expires_at > CURRENT_TIMESTAMP;

-- User performance summary view
CREATE VIEW user_performance_summary AS
SELECT 
    pr.user_id,
    COUNT(*) AS total_requests,
    AVG(pr.confidence_score) AS avg_confidence,
    AVG(pr.processing_time_ms) AS avg_processing_time,
    COUNT(CASE WHEN pr.status = 'completed' THEN 1 END) AS successful_requests,
    COUNT(CASE WHEN pr.status = 'failed' THEN 1 END) AS failed_requests
FROM processing_requests pr
WHERE pr.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY pr.user_id;

-- System health metrics view
CREATE VIEW system_health_metrics AS
SELECT
    metric_category,
    metric_name,
    AVG(metric_value) AS avg_value,
    MIN(metric_value) AS min_value,
    MAX(metric_value) AS max_value,
    COUNT(*) AS sample_count
FROM performance_metrics
WHERE recorded_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
GROUP BY metric_category, metric_name
ORDER BY metric_category, metric_name;

-- ============================================================================
-- INITIAL DATA SETUP
-- ============================================================================

-- Insert default system configuration
INSERT INTO system_configuration (config_key, config_category, config_value, config_description) VALUES
('confidence_threshold', 'processing', '85.0', 'Minimum confidence threshold for processing'),
('max_session_duration', 'session', '86400', 'Maximum session duration in seconds (24 hours)'),
('rate_limit_requests_per_minute', 'api', '1000', 'API rate limit per minute'),
('nlp_model_version', 'models', '"v2.2.0"', 'Current NLP model version'),
('enable_learning', 'features', 'true', 'Enable user learning and adaptation'),
('log_level', 'system', '"INFO"', 'System logging level'),
('jaegis_integration_enabled', 'integration', 'true', 'Enable JAEGIS integration'),
('amasiap_integration_enabled', 'integration', 'true', 'Enable A.M.A.S.I.A.P. integration');

-- Create default admin user
INSERT INTO user_profiles (user_id, email, role, preferences) VALUES
('admin', 'admin@jaegis.ai', 'admin', '{"theme": "dark", "language": "en", "notifications": true}');

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO nlds_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO nlds_user;
