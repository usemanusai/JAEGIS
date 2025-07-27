#!/usr/bin/env python3
"""
A.C.I.D. Cognitive Persistence System
Autonomous Cognitive Intelligence Directorate - Memory & Learning

This module implements the Cognitive Persistence System for A.C.I.D., providing
long-term memory management, learning retention, and knowledge optimization
for the JAEGIS A.E.G.I.S. Protocol Suite.

Cognitive Persistence Features:
- Long-term memory management
- Learning retention and optimization
- Knowledge graph construction
- Experience-based adaptation
- Cross-session continuity
"""

import asyncio
import json
import logging
import time
import pickle
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of memory storage"""
    EPISODIC = "episodic"  # Specific events and experiences
    SEMANTIC = "semantic"  # General knowledge and facts
    PROCEDURAL = "procedural"  # Skills and procedures
    WORKING = "working"  # Temporary working memory
    ASSOCIATIVE = "associative"  # Connections and relationships

class LearningMode(Enum):
    """Learning adaptation modes"""
    PASSIVE = "passive"  # Observe and record
    ACTIVE = "active"  # Actively seek patterns
    REINFORCEMENT = "reinforcement"  # Learn from feedback
    TRANSFER = "transfer"  # Apply knowledge to new domains
    META = "meta"  # Learn how to learn

class KnowledgeConfidence(Enum):
    """Confidence levels for knowledge"""
    UNCERTAIN = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    CERTAIN = 5

@dataclass
class MemoryEntry:
    """Individual memory entry"""
    id: str
    memory_type: MemoryType
    content: Dict[str, Any]
    context: Dict[str, Any]
    confidence: KnowledgeConfidence
    importance: float  # 0.0 to 1.0
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    tags: Set[str] = field(default_factory=set)
    associations: Set[str] = field(default_factory=set)  # IDs of related memories
    decay_factor: float = 1.0  # Memory strength decay
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LearningPattern:
    """Identified learning pattern"""
    id: str
    pattern_type: str
    description: str
    conditions: Dict[str, Any]
    outcomes: Dict[str, Any]
    confidence: float
    frequency: int = 1
    last_observed: datetime = field(default_factory=datetime.now)
    effectiveness: float = 0.5  # How effective this pattern is
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class KnowledgeNode:
    """Node in knowledge graph"""
    id: str
    concept: str
    properties: Dict[str, Any]
    connections: Dict[str, float]  # node_id -> strength
    confidence: KnowledgeConfidence
    evidence_count: int = 1
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LearningSession:
    """Learning session tracking"""
    id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    agent_id: str = ""
    task_context: Dict[str, Any] = field(default_factory=dict)
    memories_created: List[str] = field(default_factory=list)
    patterns_discovered: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class CognitivePersistence:
    """
    A.C.I.D. Cognitive Persistence System
    
    Manages long-term memory, learning retention, and knowledge optimization
    for continuous improvement and adaptation of the A.E.G.I.S. ecosystem.
    """
    
    def __init__(self, storage_path: str = "cognitive_persistence.db"):
        self.storage_path = Path(storage_path)
        self.memories: Dict[str, MemoryEntry] = {}
        self.knowledge_graph: Dict[str, KnowledgeNode] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.active_sessions: Dict[str, LearningSession] = {}
        self.session_history: List[LearningSession] = []
        
        # Configuration parameters
        self.config = {
            "memory_decay_rate": 0.01,  # Daily decay rate
            "importance_threshold": 0.3,  # Minimum importance to retain
            "max_working_memory": 100,  # Maximum working memory entries
            "association_threshold": 0.5,  # Minimum strength for associations
            "pattern_confidence_threshold": 0.7,  # Minimum confidence for patterns
            "knowledge_consolidation_interval": 3600,  # Seconds between consolidation
            "auto_cleanup_interval": 86400  # Daily cleanup interval
        }
        
        # Initialize storage
        self._initialize_storage()
        
        # Start background processes
        asyncio.create_task(self._background_maintenance())
        
        logger.info("A.C.I.D. Cognitive Persistence System initialized")
    
    def _initialize_storage(self):
        """Initialize persistent storage database"""
        try:
            self.conn = sqlite3.connect(str(self.storage_path), check_same_thread=False)
            self.conn.execute("PRAGMA foreign_keys = ON")
            
            # Create tables
            self._create_tables()
            
            # Load existing data
            self._load_from_storage()
            
        except Exception as e:
            logger.error(f"Failed to initialize storage: {e}")
            # Fallback to in-memory storage
            self.conn = sqlite3.connect(":memory:")
            self._create_tables()
    
    def _create_tables(self):
        """Create database tables for persistent storage"""
        cursor = self.conn.cursor()
        
        # Memories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                context TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                importance REAL NOT NULL,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT NOT NULL,
                created_at TEXT NOT NULL,
                tags TEXT NOT NULL,
                associations TEXT NOT NULL,
                decay_factor REAL DEFAULT 1.0,
                metadata TEXT NOT NULL
            )
        """)
        
        # Knowledge graph table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_nodes (
                id TEXT PRIMARY KEY,
                concept TEXT NOT NULL,
                properties TEXT NOT NULL,
                connections TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                evidence_count INTEGER DEFAULT 1,
                last_updated TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
        """)
        
        # Learning patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                description TEXT NOT NULL,
                conditions TEXT NOT NULL,
                outcomes TEXT NOT NULL,
                confidence REAL NOT NULL,
                frequency INTEGER DEFAULT 1,
                last_observed TEXT NOT NULL,
                effectiveness REAL DEFAULT 0.5,
                metadata TEXT NOT NULL
            )
        """)
        
        # Learning sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_sessions (
                id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT,
                agent_id TEXT NOT NULL,
                task_context TEXT NOT NULL,
                memories_created TEXT NOT NULL,
                patterns_discovered TEXT NOT NULL,
                performance_metrics TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
    
    def _load_from_storage(self):
        """Load existing data from storage"""
        cursor = self.conn.cursor()
        
        # Load memories
        cursor.execute("SELECT * FROM memories")
        for row in cursor.fetchall():
            memory = self._row_to_memory(row)
            self.memories[memory.id] = memory
        
        # Load knowledge nodes
        cursor.execute("SELECT * FROM knowledge_nodes")
        for row in cursor.fetchall():
            node = self._row_to_knowledge_node(row)
            self.knowledge_graph[node.id] = node
        
        # Load learning patterns
        cursor.execute("SELECT * FROM learning_patterns")
        for row in cursor.fetchall():
            pattern = self._row_to_learning_pattern(row)
            self.learning_patterns[pattern.id] = pattern
        
        logger.info(f"Loaded {len(self.memories)} memories, {len(self.knowledge_graph)} knowledge nodes, {len(self.learning_patterns)} patterns")
    
    def _row_to_memory(self, row) -> MemoryEntry:
        """Convert database row to MemoryEntry"""
        return MemoryEntry(
            id=row[0],
            memory_type=MemoryType(row[1]),
            content=json.loads(row[2]),
            context=json.loads(row[3]),
            confidence=KnowledgeConfidence(row[4]),
            importance=row[5],
            access_count=row[6],
            last_accessed=datetime.fromisoformat(row[7]),
            created_at=datetime.fromisoformat(row[8]),
            tags=set(json.loads(row[9])),
            associations=set(json.loads(row[10])),
            decay_factor=row[11],
            metadata=json.loads(row[12])
        )
    
    def _row_to_knowledge_node(self, row) -> KnowledgeNode:
        """Convert database row to KnowledgeNode"""
        return KnowledgeNode(
            id=row[0],
            concept=row[1],
            properties=json.loads(row[2]),
            connections=json.loads(row[3]),
            confidence=KnowledgeConfidence(row[4]),
            evidence_count=row[5],
            last_updated=datetime.fromisoformat(row[6]),
            metadata=json.loads(row[7])
        )
    
    def _row_to_learning_pattern(self, row) -> LearningPattern:
        """Convert database row to LearningPattern"""
        return LearningPattern(
            id=row[0],
            pattern_type=row[1],
            description=row[2],
            conditions=json.loads(row[3]),
            outcomes=json.loads(row[4]),
            confidence=row[5],
            frequency=row[6],
            last_observed=datetime.fromisoformat(row[7]),
            effectiveness=row[8],
            metadata=json.loads(row[9])
        )
    
    async def store_memory(
        self,
        memory_type: MemoryType,
        content: Dict[str, Any],
        context: Dict[str, Any],
        confidence: KnowledgeConfidence = KnowledgeConfidence.MODERATE,
        importance: float = 0.5,
        tags: Optional[Set[str]] = None
    ) -> str:
        """
        Store a new memory entry
        
        Args:
            memory_type: Type of memory
            content: Memory content
            context: Contextual information
            confidence: Confidence in memory accuracy
            importance: Importance score (0.0 to 1.0)
            tags: Optional tags for categorization
            
        Returns:
            Memory ID
        """
        memory_id = str(uuid.uuid4())
        
        memory = MemoryEntry(
            id=memory_id,
            memory_type=memory_type,
            content=content,
            context=context,
            confidence=confidence,
            importance=importance,
            tags=tags or set()
        )
        
        self.memories[memory_id] = memory
        
        # Store in database
        await self._persist_memory(memory)
        
        # Update knowledge graph
        await self._update_knowledge_graph(memory)
        
        # Detect patterns
        await self._detect_learning_patterns(memory)
        
        logger.info(f"Stored {memory_type.value} memory: {memory_id}")
        return memory_id
    
    async def _persist_memory(self, memory: MemoryEntry):
        """Persist memory to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO memories 
            (id, memory_type, content, context, confidence, importance, 
             access_count, last_accessed, created_at, tags, associations, 
             decay_factor, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory.id,
            memory.memory_type.value,
            json.dumps(memory.content),
            json.dumps(memory.context),
            memory.confidence.value,
            memory.importance,
            memory.access_count,
            memory.last_accessed.isoformat(),
            memory.created_at.isoformat(),
            json.dumps(list(memory.tags)),
            json.dumps(list(memory.associations)),
            memory.decay_factor,
            json.dumps(memory.metadata)
        ))
        self.conn.commit()
    
    async def retrieve_memory(
        self,
        memory_id: str,
        update_access: bool = True
    ) -> Optional[MemoryEntry]:
        """
        Retrieve a specific memory by ID
        
        Args:
            memory_id: Memory ID
            update_access: Whether to update access statistics
            
        Returns:
            Memory entry or None
        """
        memory = self.memories.get(memory_id)
        
        if memory and update_access:
            memory.access_count += 1
            memory.last_accessed = datetime.now()
            await self._persist_memory(memory)
        
        return memory
    
    async def search_memories(
        self,
        query: Dict[str, Any],
        memory_types: Optional[List[MemoryType]] = None,
        tags: Optional[Set[str]] = None,
        min_confidence: Optional[KnowledgeConfidence] = None,
        min_importance: float = 0.0,
        limit: int = 10
    ) -> List[MemoryEntry]:
        """
        Search memories based on criteria
        
        Args:
            query: Search query parameters
            memory_types: Filter by memory types
            tags: Filter by tags
            min_confidence: Minimum confidence level
            min_importance: Minimum importance score
            limit: Maximum results to return
            
        Returns:
            List of matching memories
        """
        results = []
        
        for memory in self.memories.values():
            # Filter by memory type
            if memory_types and memory.memory_type not in memory_types:
                continue
            
            # Filter by confidence
            if min_confidence and memory.confidence.value < min_confidence.value:
                continue
            
            # Filter by importance
            if memory.importance < min_importance:
                continue
            
            # Filter by tags
            if tags and not tags.intersection(memory.tags):
                continue
            
            # Content matching
            if self._matches_query(memory, query):
                results.append(memory)
        
        # Sort by relevance and importance
        results.sort(key=lambda m: (m.importance, m.access_count), reverse=True)
        
        return results[:limit]
    
    def _matches_query(self, memory: MemoryEntry, query: Dict[str, Any]) -> bool:
        """Check if memory matches search query"""
        for key, value in query.items():
            # Check content
            if key in memory.content:
                if isinstance(value, str) and isinstance(memory.content[key], str):
                    if value.lower() not in memory.content[key].lower():
                        return False
                elif memory.content[key] != value:
                    return False
            
            # Check context
            elif key in memory.context:
                if isinstance(value, str) and isinstance(memory.context[key], str):
                    if value.lower() not in memory.context[key].lower():
                        return False
                elif memory.context[key] != value:
                    return False
            
            # Check metadata
            elif key in memory.metadata:
                if memory.metadata[key] != value:
                    return False
            
            else:
                return False
        
        return True
    
    async def _update_knowledge_graph(self, memory: MemoryEntry):
        """Update knowledge graph based on new memory"""
        # Extract concepts from memory content
        concepts = self._extract_concepts(memory)
        
        for concept in concepts:
            node_id = self._get_concept_node_id(concept)
            
            if node_id in self.knowledge_graph:
                # Update existing node
                node = self.knowledge_graph[node_id]
                node.evidence_count += 1
                node.last_updated = datetime.now()
                
                # Update confidence based on evidence
                if node.evidence_count > 5:
                    node.confidence = KnowledgeConfidence.HIGH
                elif node.evidence_count > 2:
                    node.confidence = KnowledgeConfidence.MODERATE
            else:
                # Create new node
                node = KnowledgeNode(
                    id=node_id,
                    concept=concept,
                    properties=self._extract_concept_properties(memory, concept),
                    connections={},
                    confidence=KnowledgeConfidence.LOW
                )
                self.knowledge_graph[node_id] = node
            
            # Update connections
            await self._update_concept_connections(node, memory)
            
            # Persist to database
            await self._persist_knowledge_node(node)
    
    def _extract_concepts(self, memory: MemoryEntry) -> List[str]:
        """Extract key concepts from memory"""
        concepts = []
        
        # Extract from content
        content_str = json.dumps(memory.content).lower()
        
        # Simple keyword extraction (could be enhanced with NLP)
        keywords = [
            "task", "agent", "squad", "formation", "swarm", "consensus",
            "validation", "optimization", "performance", "security",
            "deployment", "integration", "api", "database", "ui", "design"
        ]
        
        for keyword in keywords:
            if keyword in content_str:
                concepts.append(keyword)
        
        # Extract from tags
        concepts.extend(list(memory.tags))
        
        return list(set(concepts))
    
    def _get_concept_node_id(self, concept: str) -> str:
        """Generate consistent node ID for concept"""
        return hashlib.md5(concept.lower().encode()).hexdigest()
    
    def _extract_concept_properties(self, memory: MemoryEntry, concept: str) -> Dict[str, Any]:
        """Extract properties for a concept from memory"""
        properties = {
            "first_seen": memory.created_at.isoformat(),
            "memory_types": [memory.memory_type.value],
            "contexts": [memory.context.get("task_type", "unknown")]
        }
        
        # Extract specific properties based on concept
        if concept == "task":
            properties.update({
                "complexity": memory.context.get("complexity", "unknown"),
                "duration": memory.context.get("duration", 0),
                "success_rate": memory.content.get("success_rate", 0.5)
            })
        elif concept == "agent":
            properties.update({
                "capabilities": memory.content.get("capabilities", []),
                "performance": memory.content.get("performance", 0.5),
                "specialization": memory.content.get("specialization", "general")
            })
        
        return properties
    
    async def _update_concept_connections(self, node: KnowledgeNode, memory: MemoryEntry):
        """Update connections between concepts"""
        memory_concepts = self._extract_concepts(memory)
        
        for concept in memory_concepts:
            if concept != node.concept:
                other_node_id = self._get_concept_node_id(concept)
                
                # Strengthen connection
                current_strength = node.connections.get(other_node_id, 0.0)
                node.connections[other_node_id] = min(1.0, current_strength + 0.1)
    
    async def _persist_knowledge_node(self, node: KnowledgeNode):
        """Persist knowledge node to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO knowledge_nodes 
            (id, concept, properties, connections, confidence, evidence_count, last_updated, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            node.id,
            node.concept,
            json.dumps(node.properties),
            json.dumps(node.connections),
            node.confidence.value,
            node.evidence_count,
            node.last_updated.isoformat(),
            json.dumps(node.metadata)
        ))
        self.conn.commit()
    
    async def _detect_learning_patterns(self, memory: MemoryEntry):
        """Detect learning patterns from new memory"""
        # Pattern detection based on memory content and context
        patterns = []
        
        # Task completion patterns
        if memory.memory_type == MemoryType.EPISODIC and "task_completed" in memory.content:
            pattern = await self._analyze_task_completion_pattern(memory)
            if pattern:
                patterns.append(pattern)
        
        # Performance improvement patterns
        if "performance" in memory.content:
            pattern = await self._analyze_performance_pattern(memory)
            if pattern:
                patterns.append(pattern)
        
        # Error recovery patterns
        if "error" in memory.content or "failure" in memory.content:
            pattern = await self._analyze_error_recovery_pattern(memory)
            if pattern:
                patterns.append(pattern)
        
        # Store discovered patterns
        for pattern in patterns:
            await self._store_learning_pattern(pattern)
    
    async def _analyze_task_completion_pattern(self, memory: MemoryEntry) -> Optional[LearningPattern]:
        """Analyze task completion patterns"""
        task_type = memory.context.get("task_type")
        success = memory.content.get("success", False)
        
        if not task_type:
            return None
        
        # Look for similar task completions
        similar_memories = await self.search_memories(
            query={"task_type": task_type},
            memory_types=[MemoryType.EPISODIC],
            limit=10
        )
        
        if len(similar_memories) >= 3:
            success_rate = sum(1 for m in similar_memories if m.content.get("success", False)) / len(similar_memories)
            
            pattern = LearningPattern(
                id=str(uuid.uuid4()),
                pattern_type="task_completion",
                description=f"Task completion pattern for {task_type}",
                conditions={"task_type": task_type},
                outcomes={"success_rate": success_rate},
                confidence=min(1.0, len(similar_memories) / 10.0),
                effectiveness=success_rate
            )
            
            return pattern
        
        return None
    
    async def _analyze_performance_pattern(self, memory: MemoryEntry) -> Optional[LearningPattern]:
        """Analyze performance improvement patterns"""
        performance = memory.content.get("performance")
        context_key = memory.context.get("context_type", "general")
        
        if performance is None:
            return None
        
        # Look for performance trend
        similar_memories = await self.search_memories(
            query={"context_type": context_key},
            limit=20
        )
        
        performances = [m.content.get("performance") for m in similar_memories if m.content.get("performance") is not None]
        
        if len(performances) >= 5:
            # Calculate trend
            recent_avg = sum(performances[-3:]) / 3
            older_avg = sum(performances[:3]) / 3
            improvement = recent_avg - older_avg
            
            if abs(improvement) > 0.1:  # Significant change
                pattern = LearningPattern(
                    id=str(uuid.uuid4()),
                    pattern_type="performance_trend",
                    description=f"Performance trend in {context_key}",
                    conditions={"context_type": context_key},
                    outcomes={"improvement": improvement, "recent_performance": recent_avg},
                    confidence=0.8,
                    effectiveness=max(0.0, improvement)
                )
                
                return pattern
        
        return None
    
    async def _analyze_error_recovery_pattern(self, memory: MemoryEntry) -> Optional[LearningPattern]:
        """Analyze error recovery patterns"""
        error_type = memory.content.get("error_type")
        recovery_method = memory.content.get("recovery_method")
        
        if not error_type or not recovery_method:
            return None
        
        # Look for similar error recoveries
        similar_memories = await self.search_memories(
            query={"error_type": error_type},
            limit=10
        )
        
        recovery_methods = [m.content.get("recovery_method") for m in similar_memories if m.content.get("recovery_method")]
        
        if recovery_methods.count(recovery_method) >= 2:
            success_rate = sum(1 for m in similar_memories if m.content.get("recovery_success", False)) / len(similar_memories)
            
            pattern = LearningPattern(
                id=str(uuid.uuid4()),
                pattern_type="error_recovery",
                description=f"Error recovery pattern for {error_type}",
                conditions={"error_type": error_type},
                outcomes={"recovery_method": recovery_method, "success_rate": success_rate},
                confidence=min(1.0, len(similar_memories) / 5.0),
                effectiveness=success_rate
            )
            
            return pattern
        
        return None
    
    async def _store_learning_pattern(self, pattern: LearningPattern):
        """Store a learning pattern"""
        # Check if similar pattern exists
        existing_pattern = None
        for p in self.learning_patterns.values():
            if (p.pattern_type == pattern.pattern_type and 
                p.conditions == pattern.conditions):
                existing_pattern = p
                break
        
        if existing_pattern:
            # Update existing pattern
            existing_pattern.frequency += 1
            existing_pattern.last_observed = datetime.now()
            existing_pattern.confidence = min(1.0, existing_pattern.confidence + 0.1)
            existing_pattern.effectiveness = (existing_pattern.effectiveness + pattern.effectiveness) / 2
            pattern = existing_pattern
        else:
            # Store new pattern
            self.learning_patterns[pattern.id] = pattern
        
        # Persist to database
        await self._persist_learning_pattern(pattern)
        
        logger.info(f"Stored learning pattern: {pattern.pattern_type}")
    
    async def _persist_learning_pattern(self, pattern: LearningPattern):
        """Persist learning pattern to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO learning_patterns 
            (id, pattern_type, description, conditions, outcomes, confidence, 
             frequency, last_observed, effectiveness, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pattern.id,
            pattern.pattern_type,
            pattern.description,
            json.dumps(pattern.conditions),
            json.dumps(pattern.outcomes),
            pattern.confidence,
            pattern.frequency,
            pattern.last_observed.isoformat(),
            pattern.effectiveness,
            json.dumps(pattern.metadata)
        ))
        self.conn.commit()
    
    async def start_learning_session(
        self,
        agent_id: str,
        task_context: Dict[str, Any]
    ) -> str:
        """
        Start a new learning session
        
        Args:
            agent_id: ID of the learning agent
            task_context: Context of the task/session
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        
        session = LearningSession(
            id=session_id,
            start_time=datetime.now(),
            agent_id=agent_id,
            task_context=task_context
        )
        
        self.active_sessions[session_id] = session
        
        logger.info(f"Started learning session {session_id} for agent {agent_id}")
        return session_id
    
    async def end_learning_session(
        self,
        session_id: str,
        performance_metrics: Optional[Dict[str, float]] = None
    ) -> bool:
        """
        End a learning session
        
        Args:
            session_id: Session ID
            performance_metrics: Final performance metrics
            
        Returns:
            Success status
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        session.end_time = datetime.now()
        if performance_metrics:
            session.performance_metrics.update(performance_metrics)
        
        # Move to history
        self.session_history.append(session)
        del self.active_sessions[session_id]
        
        # Persist to database
        await self._persist_learning_session(session)
        
        # Analyze session for insights
        await self._analyze_learning_session(session)
        
        logger.info(f"Ended learning session {session_id}")
        return True
    
    async def _persist_learning_session(self, session: LearningSession):
        """Persist learning session to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO learning_sessions 
            (id, start_time, end_time, agent_id, task_context, memories_created, 
             patterns_discovered, performance_metrics, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session.id,
            session.start_time.isoformat(),
            session.end_time.isoformat() if session.end_time else None,
            session.agent_id,
            json.dumps(session.task_context),
            json.dumps(session.memories_created),
            json.dumps(session.patterns_discovered),
            json.dumps(session.performance_metrics),
            json.dumps(session.metadata)
        ))
        self.conn.commit()
    
    async def _analyze_learning_session(self, session: LearningSession):
        """Analyze completed learning session for insights"""
        # Store session as episodic memory
        await self.store_memory(
            memory_type=MemoryType.EPISODIC,
            content={
                "session_type": "learning_session",
                "duration": (session.end_time - session.start_time).total_seconds(),
                "memories_created": len(session.memories_created),
                "patterns_discovered": len(session.patterns_discovered),
                "performance_metrics": session.performance_metrics
            },
            context={
                "agent_id": session.agent_id,
                "task_context": session.task_context
            },
            importance=0.7,
            tags={"learning_session", "performance_analysis"}
        )
    
    async def get_learning_insights(
        self,
        agent_id: Optional[str] = None,
        time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """
        Get learning insights and recommendations
        
        Args:
            agent_id: Filter by specific agent
            time_window: Time window for analysis
            
        Returns:
            Learning insights and recommendations
        """
        cutoff_time = datetime.now() - (time_window or timedelta(days=7))
        
        # Filter sessions
        relevant_sessions = [
            s for s in self.session_history
            if (not agent_id or s.agent_id == agent_id) and
               s.start_time >= cutoff_time
        ]
        
        # Analyze patterns
        pattern_effectiveness = {}
        for pattern in self.learning_patterns.values():
            if pattern.last_observed >= cutoff_time:
                pattern_effectiveness[pattern.pattern_type] = pattern.effectiveness
        
        # Calculate learning metrics
        total_memories = len([m for m in self.memories.values() if m.created_at >= cutoff_time])
        avg_session_duration = 0
        if relevant_sessions:
            durations = [
                (s.end_time - s.start_time).total_seconds()
                for s in relevant_sessions if s.end_time
            ]
            avg_session_duration = sum(durations) / len(durations) if durations else 0
        
        insights = {
            "time_window": time_window.total_seconds() if time_window else 604800,  # 7 days default
            "total_sessions": len(relevant_sessions),
            "total_memories_created": total_memories,
            "average_session_duration": avg_session_duration,
            "most_effective_patterns": sorted(
                pattern_effectiveness.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "knowledge_graph_size": len(self.knowledge_graph),
            "learning_recommendations": await self._generate_learning_recommendations(relevant_sessions)
        }
        
        return insights
    
    async def _generate_learning_recommendations(
        self,
        sessions: List[LearningSession]
    ) -> List[str]:
        """Generate learning recommendations based on session analysis"""
        recommendations = []
        
        if not sessions:
            recommendations.append("Start more learning sessions to gather data for analysis")
            return recommendations
        
        # Analyze session performance
        performance_scores = []
        for session in sessions:
            if "overall_performance" in session.performance_metrics:
                performance_scores.append(session.performance_metrics["overall_performance"])
        
        if performance_scores:
            avg_performance = sum(performance_scores) / len(performance_scores)
            
            if avg_performance < 0.6:
                recommendations.append("Focus on improving task execution strategies")
            elif avg_performance > 0.8:
                recommendations.append("Consider taking on more complex challenges")
        
        # Analyze pattern effectiveness
        effective_patterns = [
            p for p in self.learning_patterns.values()
            if p.effectiveness > 0.7 and p.frequency >= 3
        ]
        
        if effective_patterns:
            recommendations.append(f"Continue using effective patterns: {', '.join([p.pattern_type for p in effective_patterns[:3]])}")
        
        # Memory analysis
        recent_memories = [
            m for m in self.memories.values()
            if m.created_at >= datetime.now() - timedelta(days=7)
        ]
        
        if len(recent_memories) < 10:
            recommendations.append("Increase memory recording for better learning retention")
        
        return recommendations
    
    async def _background_maintenance(self):
        """Background maintenance tasks"""
        while True:
            try:
                # Memory decay
                await self._apply_memory_decay()
                
                # Knowledge consolidation
                await self._consolidate_knowledge()
                
                # Cleanup old data
                await self._cleanup_old_data()
                
                # Sleep until next maintenance cycle
                await asyncio.sleep(self.config["knowledge_consolidation_interval"])
                
            except Exception as e:
                logger.error(f"Error in background maintenance: {e}")
                await asyncio.sleep(60)  # Retry after 1 minute
    
    async def _apply_memory_decay(self):
        """Apply decay to memory importance over time"""
        current_time = datetime.now()
        
        for memory in self.memories.values():
            # Calculate age in days
            age_days = (current_time - memory.last_accessed).days
            
            # Apply decay
            decay = self.config["memory_decay_rate"] * age_days
            memory.decay_factor = max(0.1, memory.decay_factor - decay)
            
            # Update effective importance
            effective_importance = memory.importance * memory.decay_factor
            
            # Mark for cleanup if too low
            if effective_importance < self.config["importance_threshold"]:
                memory.metadata["marked_for_cleanup"] = True
    
    async def _consolidate_knowledge(self):
        """Consolidate knowledge graph connections"""
        # Strengthen frequently accessed connections
        for node in self.knowledge_graph.values():
            for connected_id, strength in list(node.connections.items()):
                if strength > self.config["association_threshold"]:
                    # Strengthen strong connections
                    node.connections[connected_id] = min(1.0, strength * 1.01)
                else:
                    # Weaken weak connections
                    node.connections[connected_id] = max(0.0, strength * 0.99)
                    
                    # Remove very weak connections
                    if node.connections[connected_id] < 0.1:
                        del node.connections[connected_id]
    
    async def _cleanup_old_data(self):
        """Clean up old, low-importance data"""
        # Remove marked memories
        to_remove = [
            memory_id for memory_id, memory in self.memories.items()
            if memory.metadata.get("marked_for_cleanup", False)
        ]
        
        for memory_id in to_remove:
            del self.memories[memory_id]
            
            # Remove from database
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        
        if to_remove:
            self.conn.commit()
            logger.info(f"Cleaned up {len(to_remove)} old memories")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get cognitive persistence system status"""
        return {
            "total_memories": len(self.memories),
            "memory_types": {
                memory_type.value: len([m for m in self.memories.values() if m.memory_type == memory_type])
                for memory_type in MemoryType
            },
            "knowledge_graph_nodes": len(self.knowledge_graph),
            "learning_patterns": len(self.learning_patterns),
            "active_sessions": len(self.active_sessions),
            "total_sessions": len(self.session_history),
            "storage_path": str(self.storage_path),
            "config": self.config,
            "timestamp": datetime.now().isoformat()
        }

# Example usage and testing
async def main():
    """Example usage of the Cognitive Persistence System"""
    persistence = CognitivePersistence("test_cognitive.db")
    
    # Start a learning session
    session_id = await persistence.start_learning_session(
        agent_id="test_agent",
        task_context={"task_type": "data_analysis", "complexity": "medium"}
    )
    
    # Store some memories
    memory_ids = []
    
    # Episodic memory
    memory_id = await persistence.store_memory(
        memory_type=MemoryType.EPISODIC,
        content={
            "task_completed": True,
            "success": True,
            "performance": 0.85,
            "duration": 120
        },
        context={
            "task_type": "data_analysis",
            "agent_id": "test_agent",
            "session_id": session_id
        },
        importance=0.8,
        tags={"task_completion", "success"}
    )
    memory_ids.append(memory_id)
    
    # Semantic memory
    memory_id = await persistence.store_memory(
        memory_type=MemoryType.SEMANTIC,
        content={
            "concept": "data_analysis",
            "best_practices": ["clean_data", "validate_results", "document_process"],
            "tools": ["pandas", "numpy", "matplotlib"]
        },
        context={
            "domain": "data_science",
            "source": "experience"
        },
        importance=0.9,
        tags={"knowledge", "data_analysis"}
    )
    memory_ids.append(memory_id)
    
    # Procedural memory
    memory_id = await persistence.store_memory(
        memory_type=MemoryType.PROCEDURAL,
        content={
            "procedure": "data_cleaning",
            "steps": [
                "identify_missing_values",
                "handle_outliers",
                "normalize_data",
                "validate_consistency"
            ],
            "success_rate": 0.92
        },
        context={
            "domain": "data_preprocessing",
            "complexity": "medium"
        },
        importance=0.7,
        tags={"procedure", "data_cleaning"}
    )
    memory_ids.append(memory_id)
    
    # End learning session
    await persistence.end_learning_session(
        session_id,
        performance_metrics={"overall_performance": 0.85, "efficiency": 0.78}
    )
    
    # Search memories
    search_results = await persistence.search_memories(
        query={"task_type": "data_analysis"},
        tags={"success"},
        min_importance=0.5
    )
    
    print(f"Found {len(search_results)} memories matching search criteria")
    
    # Get learning insights
    insights = await persistence.get_learning_insights()
    print(f"Learning insights: {json.dumps(insights, indent=2)}")
    
    # Get system status
    status = persistence.get_system_status()
    print(f"System status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())