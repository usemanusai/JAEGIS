"""
N.L.D.S. Database Models
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

SQLAlchemy models for the N.L.D.S. database schema.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from uuid import uuid4
import enum

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Text, DECIMAL, 
    ForeignKey, ARRAY, Enum as SQLEnum, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


# ============================================================================
# ENUMS
# ============================================================================

class InputType(enum.Enum):
    """Input type enumeration."""
    TEXT = "text"
    VOICE = "voice"
    COMMAND = "command"
    CONVERSATION = "conversation"


class ConfidenceLevel(enum.Enum):
    """Confidence level enumeration."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProcessingStatus(enum.Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class UserRole(enum.Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"


# ============================================================================
# USER MANAGEMENT MODELS
# ============================================================================

class UserProfile(Base):
    """User profile model."""
    
    __tablename__ = "user_profiles"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, index=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    
    # User data
    preferences = Column(JSONB, default=dict)
    cognitive_patterns = Column(JSONB, default=dict)
    behavior_patterns = Column(JSONB, default=dict)
    learning_data = Column(JSONB, default=dict)
    interaction_history = Column(JSONB, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True))
    
    # Relationships
    authentication = relationship("UserAuthentication", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("ConversationSession", back_populates="user", cascade="all, delete-orphan")
    processing_requests = relationship("ProcessingRequest", back_populates="user", cascade="all, delete-orphan")
    analytics = relationship("UserAnalytics", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("UserFeedback", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_profiles_preferences_gin', 'preferences', postgresql_using='gin'),
        CheckConstraint("jsonb_typeof(preferences) = 'object'", name='valid_preferences'),
        CheckConstraint("jsonb_typeof(cognitive_patterns) = 'object'", name='valid_cognitive_patterns'),
        CheckConstraint("jsonb_typeof(behavior_patterns) = 'object'", name='valid_behavior_patterns'),
    )


class UserAuthentication(Base):
    """User authentication model."""
    
    __tablename__ = "user_authentication"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(255), ForeignKey("user_profiles.user_id", ondelete="CASCADE"), nullable=False)
    
    # Authentication data
    password_hash = Column(String(255))
    salt = Column(String(255))
    oauth_provider = Column(String(50))
    oauth_id = Column(String(255))
    oauth_data = Column(JSONB, default=dict)
    
    # API keys
    api_key_hash = Column(String(255))
    api_key_expires_at = Column(DateTime(timezone=True))
    
    # Security
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserProfile", back_populates="authentication")


# ============================================================================
# SESSION MANAGEMENT MODELS
# ============================================================================

class ConversationSession(Base):
    """Conversation session model."""
    
    __tablename__ = "conversation_sessions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(String(255), ForeignKey("user_profiles.user_id", ondelete="CASCADE"), nullable=False)
    
    # Session data
    context_data = Column(JSONB, default=dict)
    conversation_history = Column(JSONB, default=list)
    user_state = Column(JSONB, default=dict)
    
    # Session metadata
    ip_address = Column(INET)
    user_agent = Column(Text)
    device_info = Column(JSONB, default=dict)
    
    # Timing
    started_at = Column(DateTime(timezone=True), default=func.now())
    last_activity_at = Column(DateTime(timezone=True), default=func.now())
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.utcnow() + timedelta(hours=24))
    ended_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    user = relationship("UserProfile", back_populates="sessions")
    processing_requests = relationship("ProcessingRequest", back_populates="session", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_conversation_sessions_context_gin', 'context_data', postgresql_using='gin'),
        Index('idx_conversation_sessions_expires_at', 'expires_at'),
        CheckConstraint("jsonb_typeof(context_data) = 'object'", name='valid_context_data'),
        CheckConstraint("jsonb_typeof(conversation_history) = 'array'", name='valid_conversation_history'),
        CheckConstraint("expires_at > started_at", name='valid_expires_at'),
    )


# ============================================================================
# PROCESSING MODELS
# ============================================================================

class ProcessingRequest(Base):
    """Processing request model."""
    
    __tablename__ = "processing_requests"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(String(255), ForeignKey("conversation_sessions.session_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(255), ForeignKey("user_profiles.user_id", ondelete="CASCADE"), nullable=False)
    
    # Input data
    input_text = Column(Text, nullable=False)
    input_type = Column(SQLEnum(InputType), nullable=False)
    input_metadata = Column(JSONB, default=dict)
    
    # Processing results
    nlp_analysis = Column(JSONB, default=dict)
    dimensional_analysis = Column(JSONB, default=dict)
    human_processing = Column(JSONB, default=dict)
    translation_result = Column(JSONB, default=dict)
    
    # Confidence and quality
    confidence_score = Column(DECIMAL(5, 2))
    confidence_level = Column(SQLEnum(ConfidenceLevel))
    quality_metrics = Column(JSONB, default=dict)
    
    # Processing status
    status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING, index=True)
    processing_started_at = Column(DateTime(timezone=True))
    processing_completed_at = Column(DateTime(timezone=True))
    processing_time_ms = Column(Integer)
    
    # JAEGIS integration
    selected_mode = Column(Integer)
    selected_squads = Column(ARRAY(String))
    jaegis_commands = Column(JSONB, default=list)
    execution_result = Column(JSONB, default=dict)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    
    # Relationships
    session = relationship("ConversationSession", back_populates="processing_requests")
    user = relationship("UserProfile", back_populates="processing_requests")
    feedback = relationship("UserFeedback", back_populates="processing_request", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_processing_requests_text_search', func.to_tsvector('english', 'input_text'), postgresql_using='gin'),
        Index('idx_processing_requests_confidence', 'confidence_score'),
        CheckConstraint("confidence_score >= 0 AND confidence_score <= 100", name='valid_confidence_score'),
        CheckConstraint("processing_time_ms >= 0", name='valid_processing_time'),
        CheckConstraint("selected_mode >= 1 AND selected_mode <= 5", name='valid_mode'),
    )


# ============================================================================
# ANALYTICS MODELS
# ============================================================================

class PerformanceMetrics(Base):
    """Performance metrics model."""
    
    __tablename__ = "performance_metrics"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Metric identification
    metric_name = Column(String(100), nullable=False, index=True)
    metric_category = Column(String(50), nullable=False, index=True)
    
    # Metric values
    metric_value = Column(DECIMAL(15, 6), nullable=False)
    metric_unit = Column(String(20))
    metric_tags = Column(JSONB, default=dict)
    
    # Context
    session_id = Column(String(255))
    user_id = Column(String(255))
    component_name = Column(String(100))
    
    # Timing
    recorded_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_performance_metrics_tags_gin', 'metric_tags', postgresql_using='gin'),
        CheckConstraint("jsonb_typeof(metric_tags) = 'object'", name='valid_metric_tags'),
    )


class UserAnalytics(Base):
    """User analytics model."""
    
    __tablename__ = "user_analytics"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(255), ForeignKey("user_profiles.user_id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(255), ForeignKey("conversation_sessions.session_id", ondelete="CASCADE"))
    
    # Interaction data
    interaction_type = Column(String(50), nullable=False, index=True)
    interaction_data = Column(JSONB, default=dict)
    
    # Success metrics
    success_rate = Column(DECIMAL(5, 2))
    satisfaction_score = Column(DECIMAL(3, 1))
    completion_time_ms = Column(Integer)
    
    # Learning metrics
    learning_progress = Column(JSONB, default=dict)
    adaptation_metrics = Column(JSONB, default=dict)
    
    # Timing
    recorded_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    
    # Relationships
    user = relationship("UserProfile", back_populates="analytics")
    session = relationship("ConversationSession")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("success_rate >= 0 AND success_rate <= 100", name='valid_success_rate'),
        CheckConstraint("satisfaction_score >= 0 AND satisfaction_score <= 10", name='valid_satisfaction_score'),
    )


# ============================================================================
# LEARNING MODELS
# ============================================================================

class UserFeedback(Base):
    """User feedback model."""
    
    __tablename__ = "user_feedback"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(255), ForeignKey("user_profiles.user_id", ondelete="CASCADE"), nullable=False)
    processing_request_id = Column(UUID(as_uuid=True), ForeignKey("processing_requests.id", ondelete="CASCADE"))
    
    # Feedback data
    feedback_type = Column(String(50), nullable=False)
    feedback_score = Column(Integer)
    feedback_text = Column(Text)
    feedback_data = Column(JSONB, default=dict)
    
    # Context
    context_data = Column(JSONB, default=dict)
    
    # Processing
    is_processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    user = relationship("UserProfile", back_populates="feedback")
    processing_request = relationship("ProcessingRequest", back_populates="feedback")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("feedback_score >= 1 AND feedback_score <= 5", name='valid_feedback_score'),
    )


class TrainingData(Base):
    """Training data model."""
    
    __tablename__ = "training_data"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Data identification
    data_type = Column(String(50), nullable=False)
    data_source = Column(String(100), nullable=False)
    
    # Training data
    input_data = Column(JSONB, nullable=False)
    expected_output = Column(JSONB, nullable=False)
    actual_output = Column(JSONB)
    
    # Quality metrics
    quality_score = Column(DECIMAL(5, 2))
    validation_status = Column(String(20), default='pending')
    
    # Model information
    model_name = Column(String(100))
    model_version = Column(String(20))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), default=func.now())
    validated_at = Column(DateTime(timezone=True))
    
    # Constraints
    __table_args__ = (
        CheckConstraint("quality_score >= 0 AND quality_score <= 100", name='valid_quality_score'),
    )


# ============================================================================
# SYSTEM MODELS
# ============================================================================

class SystemConfiguration(Base):
    """System configuration model."""
    
    __tablename__ = "system_configuration"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Configuration identification
    config_key = Column(String(255), unique=True, nullable=False)
    config_category = Column(String(100), nullable=False)
    
    # Configuration data
    config_value = Column(JSONB, nullable=False)
    config_description = Column(Text)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_by = Column(String(255))


class APIUsage(Base):
    """API usage tracking model."""
    
    __tablename__ = "api_usage"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Request identification
    request_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(String(255), ForeignKey("user_profiles.user_id", ondelete="SET NULL"))
    api_key_hash = Column(String(255))
    
    # Request data
    endpoint = Column(String(255), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    request_size_bytes = Column(Integer)
    response_size_bytes = Column(Integer)
    
    # Response data
    status_code = Column(Integer, nullable=False, index=True)
    response_time_ms = Column(Integer, nullable=False)
    
    # Rate limiting
    rate_limit_remaining = Column(Integer)
    rate_limit_reset_at = Column(DateTime(timezone=True))
    
    # Metadata
    ip_address = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    
    # Relationships
    user = relationship("UserProfile")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status_code >= 100 AND status_code < 600", name='valid_status_code'),
        CheckConstraint("response_time_ms >= 0", name='valid_response_time'),
    )
