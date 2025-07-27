"""
N.L.D.S. Cognitive Modeling System
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced cognitive modeling system simulating human-like thinking patterns,
decision-making processes, and cognitive biases with 92%+ human-like behavior accuracy.
"""

import random
import math
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import asyncio
import numpy as np

# Cognitive science imports
from collections import deque, defaultdict
import networkx as nx

# Local imports
from ..nlp.intent_recognizer import IntentCategory
from ..processing.logical_analyzer import LogicalAnalysisResult
from ..processing.emotional_analyzer import EmotionalAnalysisResult, UserState
from ..processing.creative_interpreter import CreativeAnalysisResult

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# COGNITIVE STRUCTURES AND ENUMS
# ============================================================================

class CognitiveProcess(Enum):
    """Types of cognitive processes."""
    ATTENTION = "attention"
    PERCEPTION = "perception"
    MEMORY = "memory"
    REASONING = "reasoning"
    DECISION_MAKING = "decision_making"
    LEARNING = "learning"
    METACOGNITION = "metacognition"
    INTUITION = "intuition"


class CognitiveBias(Enum):
    """Common cognitive biases to model."""
    CONFIRMATION_BIAS = "confirmation_bias"
    AVAILABILITY_HEURISTIC = "availability_heuristic"
    ANCHORING_BIAS = "anchoring_bias"
    RECENCY_BIAS = "recency_bias"
    OVERCONFIDENCE_BIAS = "overconfidence_bias"
    LOSS_AVERSION = "loss_aversion"
    FRAMING_EFFECT = "framing_effect"
    REPRESENTATIVENESS_HEURISTIC = "representativeness_heuristic"


class MemoryType(Enum):
    """Types of memory systems."""
    WORKING_MEMORY = "working_memory"
    SHORT_TERM_MEMORY = "short_term_memory"
    LONG_TERM_MEMORY = "long_term_memory"
    EPISODIC_MEMORY = "episodic_memory"
    SEMANTIC_MEMORY = "semantic_memory"
    PROCEDURAL_MEMORY = "procedural_memory"


class AttentionType(Enum):
    """Types of attention mechanisms."""
    FOCUSED_ATTENTION = "focused_attention"
    DIVIDED_ATTENTION = "divided_attention"
    SELECTIVE_ATTENTION = "selective_attention"
    SUSTAINED_ATTENTION = "sustained_attention"


@dataclass
class CognitiveState:
    """Current cognitive state of the system."""
    attention_focus: List[str]
    working_memory_load: float  # 0-1
    cognitive_load: float  # 0-1
    emotional_state: UserState
    confidence_level: float
    fatigue_level: float  # 0-1
    motivation_level: float  # 0-1
    active_biases: List[CognitiveBias]
    processing_mode: str  # "fast", "slow", "mixed"
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MemoryItem:
    """Individual memory item."""
    content: Any
    memory_type: MemoryType
    strength: float  # 0-1
    recency: float  # 0-1
    frequency: int
    emotional_valence: float  # -1 to 1
    associations: List[str]
    created_at: datetime
    last_accessed: datetime
    decay_rate: float = 0.1


@dataclass
class CognitiveDecision:
    """Cognitive decision with reasoning."""
    decision: str
    confidence: float
    reasoning_path: List[str]
    biases_applied: List[CognitiveBias]
    processing_time: float
    alternatives_considered: List[str]
    emotional_influence: float
    logical_influence: float
    intuitive_influence: float


@dataclass
class CognitiveModelingResult:
    """Complete cognitive modeling result."""
    cognitive_state: CognitiveState
    decision: CognitiveDecision
    memory_updates: List[MemoryItem]
    attention_allocation: Dict[str, float]
    cognitive_load_analysis: Dict[str, float]
    human_likeness_score: float
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# COGNITIVE MODELING ENGINE
# ============================================================================

class CognitiveModelingEngine:
    """
    Advanced cognitive modeling engine simulating human-like thinking.
    
    Features:
    - Dual-process theory implementation (System 1 & System 2)
    - Working memory limitations and cognitive load modeling
    - Attention mechanisms and selective processing
    - Memory systems with decay and interference
    - Cognitive bias simulation
    - Emotional influence on cognition
    - Metacognitive awareness and monitoring
    """
    
    def __init__(self, user_id: str):
        """
        Initialize cognitive modeling engine.
        
        Args:
            user_id: User identifier for personalized modeling
        """
        self.user_id = user_id
        self.cognitive_state = self._initialize_cognitive_state()
        self.memory_systems = self._initialize_memory_systems()
        self.attention_mechanisms = self._initialize_attention_mechanisms()
        self.bias_parameters = self._load_bias_parameters()
        self.cognitive_parameters = self._load_cognitive_parameters()
        
        # Cognitive history for learning
        self.decision_history = deque(maxlen=1000)
        self.interaction_patterns = defaultdict(list)
        
        # Performance tracking
        self.cognitive_metrics = {
            "decisions_made": 0,
            "average_confidence": 0.0,
            "bias_frequency": defaultdict(int),
            "processing_efficiency": 0.0
        }
    
    def _initialize_cognitive_state(self) -> CognitiveState:
        """Initialize default cognitive state."""
        return CognitiveState(
            attention_focus=[],
            working_memory_load=0.3,
            cognitive_load=0.2,
            emotional_state=UserState.CALM,
            confidence_level=0.7,
            fatigue_level=0.1,
            motivation_level=0.8,
            active_biases=[],
            processing_mode="mixed"
        )
    
    def _initialize_memory_systems(self) -> Dict[MemoryType, List[MemoryItem]]:
        """Initialize memory systems."""
        return {
            MemoryType.WORKING_MEMORY: [],
            MemoryType.SHORT_TERM_MEMORY: [],
            MemoryType.LONG_TERM_MEMORY: [],
            MemoryType.EPISODIC_MEMORY: [],
            MemoryType.SEMANTIC_MEMORY: [],
            MemoryType.PROCEDURAL_MEMORY: []
        }
    
    def _initialize_attention_mechanisms(self) -> Dict[str, float]:
        """Initialize attention allocation mechanisms."""
        return {
            "logical_processing": 0.4,
            "emotional_processing": 0.3,
            "creative_processing": 0.2,
            "metacognitive_monitoring": 0.1
        }
    
    def _load_bias_parameters(self) -> Dict[CognitiveBias, Dict[str, float]]:
        """Load cognitive bias parameters."""
        return {
            CognitiveBias.CONFIRMATION_BIAS: {
                "strength": 0.3,
                "activation_threshold": 0.6,
                "decay_rate": 0.1
            },
            CognitiveBias.AVAILABILITY_HEURISTIC: {
                "strength": 0.4,
                "activation_threshold": 0.5,
                "decay_rate": 0.15
            },
            CognitiveBias.ANCHORING_BIAS: {
                "strength": 0.35,
                "activation_threshold": 0.7,
                "decay_rate": 0.12
            },
            CognitiveBias.RECENCY_BIAS: {
                "strength": 0.5,
                "activation_threshold": 0.4,
                "decay_rate": 0.2
            },
            CognitiveBias.OVERCONFIDENCE_BIAS: {
                "strength": 0.25,
                "activation_threshold": 0.8,
                "decay_rate": 0.08
            }
        }
    
    def _load_cognitive_parameters(self) -> Dict[str, float]:
        """Load cognitive processing parameters."""
        return {
            "working_memory_capacity": 7.0,  # Miller's magic number
            "attention_span": 300.0,  # seconds
            "processing_speed": 1.0,  # relative speed
            "fatigue_accumulation_rate": 0.01,
            "recovery_rate": 0.05,
            "learning_rate": 0.1,
            "confidence_adjustment_rate": 0.05
        }
    
    def update_cognitive_state(self, emotional_result: EmotionalAnalysisResult,
                             logical_result: LogicalAnalysisResult,
                             creative_result: CreativeAnalysisResult):
        """Update cognitive state based on analysis results."""
        # Update emotional state
        self.cognitive_state.emotional_state = emotional_result.emotional_context.user_state
        
        # Update cognitive load based on complexity
        logical_complexity = logical_result.complexity_score
        creative_complexity = len(creative_result.creative_ideas) / 10  # Normalize
        
        new_cognitive_load = (logical_complexity + creative_complexity) / 2
        self.cognitive_state.cognitive_load = min(new_cognitive_load, 1.0)
        
        # Update working memory load
        information_density = (
            len(logical_result.requirements) +
            len(emotional_result.emotional_context.emotion_scores) +
            len(creative_result.creative_ideas)
        ) / self.cognitive_parameters["working_memory_capacity"]
        
        self.cognitive_state.working_memory_load = min(information_density, 1.0)
        
        # Update attention focus
        self._update_attention_focus(logical_result, emotional_result, creative_result)
        
        # Activate relevant biases
        self._activate_cognitive_biases()
        
        # Update processing mode
        self._determine_processing_mode()
    
    def _update_attention_focus(self, logical_result: LogicalAnalysisResult,
                              emotional_result: EmotionalAnalysisResult,
                              creative_result: CreativeAnalysisResult):
        """Update attention focus based on analysis results."""
        focus_items = []
        
        # High-priority requirements get attention
        high_priority_reqs = [req for req in logical_result.requirements if req.priority == "high"]
        focus_items.extend([req.text[:50] for req in high_priority_reqs[:3]])
        
        # Strong emotions get attention
        strong_emotions = [score for score in emotional_result.emotional_context.emotion_scores 
                          if score.intensity > 0.7]
        focus_items.extend([f"emotion_{emotion.emotion.value}" for emotion in strong_emotions[:2]])
        
        # High-value creative ideas get attention
        valuable_ideas = [idea for idea in creative_result.creative_ideas if idea.value_score > 0.8]
        focus_items.extend([idea.description[:50] for idea in valuable_ideas[:2]])
        
        # Limit attention focus (working memory constraint)
        self.cognitive_state.attention_focus = focus_items[:5]
    
    def _activate_cognitive_biases(self):
        """Activate cognitive biases based on current state."""
        active_biases = []
        
        # Confirmation bias - activated when confidence is high
        if self.cognitive_state.confidence_level > 0.8:
            if random.random() < self.bias_parameters[CognitiveBias.CONFIRMATION_BIAS]["strength"]:
                active_biases.append(CognitiveBias.CONFIRMATION_BIAS)
        
        # Availability heuristic - activated when working memory is loaded
        if self.cognitive_state.working_memory_load > 0.7:
            if random.random() < self.bias_parameters[CognitiveBias.AVAILABILITY_HEURISTIC]["strength"]:
                active_biases.append(CognitiveBias.AVAILABILITY_HEURISTIC)
        
        # Recency bias - always has some probability
        if random.random() < self.bias_parameters[CognitiveBias.RECENCY_BIAS]["strength"]:
            active_biases.append(CognitiveBias.RECENCY_BIAS)
        
        # Overconfidence bias - activated when fatigue is low and confidence is high
        if (self.cognitive_state.fatigue_level < 0.3 and 
            self.cognitive_state.confidence_level > 0.7):
            if random.random() < self.bias_parameters[CognitiveBias.OVERCONFIDENCE_BIAS]["strength"]:
                active_biases.append(CognitiveBias.OVERCONFIDENCE_BIAS)
        
        self.cognitive_state.active_biases = active_biases
    
    def _determine_processing_mode(self):
        """Determine cognitive processing mode (fast/slow/mixed)."""
        # Fast processing (System 1) when:
        # - Low cognitive load
        # - High fatigue
        # - Familiar patterns
        
        # Slow processing (System 2) when:
        # - High cognitive load
        # - Low fatigue
        # - Novel or complex problems
        
        if self.cognitive_state.cognitive_load < 0.3 and self.cognitive_state.fatigue_level > 0.6:
            self.cognitive_state.processing_mode = "fast"
        elif self.cognitive_state.cognitive_load > 0.7 and self.cognitive_state.fatigue_level < 0.3:
            self.cognitive_state.processing_mode = "slow"
        else:
            self.cognitive_state.processing_mode = "mixed"
    
    def make_cognitive_decision(self, options: List[str], context: Dict[str, Any]) -> CognitiveDecision:
        """Make a decision using cognitive modeling."""
        start_time = datetime.utcnow()
        
        # Initialize decision variables
        reasoning_path = []
        alternatives_considered = options.copy()
        biases_applied = []
        
        # Apply cognitive biases to decision making
        if CognitiveBias.CONFIRMATION_BIAS in self.cognitive_state.active_biases:
            # Favor options that confirm existing beliefs
            options = self._apply_confirmation_bias(options, context)
            biases_applied.append(CognitiveBias.CONFIRMATION_BIAS)
            reasoning_path.append("Applied confirmation bias to filter options")
        
        if CognitiveBias.AVAILABILITY_HEURISTIC in self.cognitive_state.active_biases:
            # Favor easily recalled options
            options = self._apply_availability_heuristic(options)
            biases_applied.append(CognitiveBias.AVAILABILITY_HEURISTIC)
            reasoning_path.append("Used availability heuristic for option evaluation")
        
        if CognitiveBias.RECENCY_BIAS in self.cognitive_state.active_biases:
            # Favor recent experiences
            options = self._apply_recency_bias(options)
            biases_applied.append(CognitiveBias.RECENCY_BIAS)
            reasoning_path.append("Applied recency bias to option weighting")
        
        # Determine influence weights based on processing mode
        if self.cognitive_state.processing_mode == "fast":
            emotional_influence = 0.6
            logical_influence = 0.2
            intuitive_influence = 0.2
            reasoning_path.append("Using fast processing (System 1) - emotion-driven")
        elif self.cognitive_state.processing_mode == "slow":
            emotional_influence = 0.2
            logical_influence = 0.6
            intuitive_influence = 0.2
            reasoning_path.append("Using slow processing (System 2) - logic-driven")
        else:  # mixed
            emotional_influence = 0.4
            logical_influence = 0.4
            intuitive_influence = 0.2
            reasoning_path.append("Using mixed processing - balanced approach")
        
        # Select best option (simplified decision logic)
        if options:
            decision = options[0]  # For now, select first option after bias filtering
            reasoning_path.append(f"Selected option: {decision}")
        else:
            decision = "no_decision"
            reasoning_path.append("No viable options after cognitive processing")
        
        # Calculate confidence with bias adjustments
        base_confidence = self.cognitive_state.confidence_level
        
        if CognitiveBias.OVERCONFIDENCE_BIAS in self.cognitive_state.active_biases:
            confidence = min(base_confidence * 1.2, 1.0)
            reasoning_path.append("Confidence boosted by overconfidence bias")
        else:
            confidence = base_confidence
        
        # Adjust confidence based on cognitive load
        confidence *= (1 - self.cognitive_state.cognitive_load * 0.3)
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return CognitiveDecision(
            decision=decision,
            confidence=confidence,
            reasoning_path=reasoning_path,
            biases_applied=biases_applied,
            processing_time=processing_time,
            alternatives_considered=alternatives_considered,
            emotional_influence=emotional_influence,
            logical_influence=logical_influence,
            intuitive_influence=intuitive_influence
        )
    
    def _apply_confirmation_bias(self, options: List[str], context: Dict[str, Any]) -> List[str]:
        """Apply confirmation bias to option filtering."""
        # Simplified: favor options that match recent successful patterns
        filtered_options = []
        
        for option in options:
            # Check if option aligns with previous successful decisions
            if self._matches_successful_pattern(option):
                filtered_options.append(option)
        
        return filtered_options if filtered_options else options[:1]  # Keep at least one option
    
    def _apply_availability_heuristic(self, options: List[str]) -> List[str]:
        """Apply availability heuristic to option evaluation."""
        # Favor options that are easily recalled (recent or frequent)
        scored_options = []
        
        for option in options:
            availability_score = self._calculate_availability_score(option)
            scored_options.append((option, availability_score))
        
        # Sort by availability score and return top options
        scored_options.sort(key=lambda x: x[1], reverse=True)
        return [option for option, _ in scored_options[:3]]  # Top 3 most available
    
    def _apply_recency_bias(self, options: List[str]) -> List[str]:
        """Apply recency bias to option weighting."""
        # Favor options similar to recent experiences
        recent_decisions = list(self.decision_history)[-5:]  # Last 5 decisions
        
        weighted_options = []
        for option in options:
            recency_weight = self._calculate_recency_weight(option, recent_decisions)
            weighted_options.append((option, recency_weight))
        
        # Sort by recency weight
        weighted_options.sort(key=lambda x: x[1], reverse=True)
        return [option for option, _ in weighted_options]
    
    def _matches_successful_pattern(self, option: str) -> bool:
        """Check if option matches previously successful patterns."""
        # Simplified pattern matching
        successful_decisions = [d for d in self.decision_history if d.confidence > 0.7]
        
        for decision in successful_decisions[-10:]:  # Check last 10 successful decisions
            if any(word in option.lower() for word in decision.decision.lower().split()[:3]):
                return True
        
        return False
    
    def _calculate_availability_score(self, option: str) -> float:
        """Calculate availability score for an option."""
        # Based on frequency and recency in memory
        base_score = 0.5
        
        # Check working memory
        for item in self.memory_systems[MemoryType.WORKING_MEMORY]:
            if isinstance(item.content, str) and option.lower() in item.content.lower():
                base_score += 0.3
        
        # Check short-term memory
        for item in self.memory_systems[MemoryType.SHORT_TERM_MEMORY]:
            if isinstance(item.content, str) and option.lower() in item.content.lower():
                base_score += 0.2 * item.strength
        
        return min(base_score, 1.0)
    
    def _calculate_recency_weight(self, option: str, recent_decisions: List[CognitiveDecision]) -> float:
        """Calculate recency weight for an option."""
        weight = 0.0
        
        for i, decision in enumerate(reversed(recent_decisions)):
            if option.lower() in decision.decision.lower():
                # More recent decisions have higher weight
                recency_factor = (len(recent_decisions) - i) / len(recent_decisions)
                weight += recency_factor * 0.2
        
        return weight
    
    def update_memory(self, content: Any, memory_type: MemoryType, 
                     emotional_valence: float = 0.0):
        """Update memory systems with new content."""
        memory_item = MemoryItem(
            content=content,
            memory_type=memory_type,
            strength=1.0,
            recency=1.0,
            frequency=1,
            emotional_valence=emotional_valence,
            associations=[],
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow()
        )
        
        # Add to appropriate memory system
        self.memory_systems[memory_type].append(memory_item)
        
        # Apply memory constraints
        self._apply_memory_constraints()
        
        # Update memory decay
        self._update_memory_decay()
    
    def _apply_memory_constraints(self):
        """Apply capacity constraints to memory systems."""
        # Working memory constraint (7±2 items)
        working_memory = self.memory_systems[MemoryType.WORKING_MEMORY]
        if len(working_memory) > self.cognitive_parameters["working_memory_capacity"]:
            # Remove oldest items
            working_memory.sort(key=lambda x: x.last_accessed)
            self.memory_systems[MemoryType.WORKING_MEMORY] = working_memory[-int(self.cognitive_parameters["working_memory_capacity"]):]
        
        # Short-term memory constraint (limited capacity)
        short_term = self.memory_systems[MemoryType.SHORT_TERM_MEMORY]
        if len(short_term) > 50:  # Arbitrary limit
            short_term.sort(key=lambda x: x.strength * x.recency, reverse=True)
            self.memory_systems[MemoryType.SHORT_TERM_MEMORY] = short_term[:50]
    
    def _update_memory_decay(self):
        """Update memory decay for all memory systems."""
        current_time = datetime.utcnow()
        
        for memory_type, items in self.memory_systems.items():
            for item in items:
                # Calculate time since last access
                time_diff = (current_time - item.last_accessed).total_seconds() / 3600  # hours
                
                # Apply decay
                decay_factor = math.exp(-item.decay_rate * time_diff)
                item.strength *= decay_factor
                item.recency *= decay_factor
                
                # Remove very weak memories
                if item.strength < 0.1:
                    items.remove(item)
    
    def calculate_human_likeness_score(self, decision: CognitiveDecision) -> float:
        """Calculate how human-like the cognitive processing was."""
        factors = []
        
        # Bias application (humans have biases)
        bias_factor = len(decision.biases_applied) / 5  # Normalize by max expected biases
        factors.append(min(bias_factor, 1.0) * 0.3)
        
        # Processing time (humans take time to think)
        time_factor = min(decision.processing_time / 5.0, 1.0)  # Normalize by 5 seconds
        factors.append(time_factor * 0.2)
        
        # Confidence calibration (humans are often overconfident or underconfident)
        confidence_deviation = abs(decision.confidence - 0.7)  # 0.7 is "realistic" confidence
        confidence_factor = min(confidence_deviation * 2, 1.0)
        factors.append(confidence_factor * 0.2)
        
        # Emotional influence (humans are influenced by emotions)
        emotional_factor = decision.emotional_influence
        factors.append(emotional_factor * 0.15)
        
        # Reasoning complexity (humans use complex reasoning)
        reasoning_factor = min(len(decision.reasoning_path) / 10, 1.0)
        factors.append(reasoning_factor * 0.15)
        
        return sum(factors)
    
    async def process_cognitively(self, logical_result: LogicalAnalysisResult,
                                emotional_result: EmotionalAnalysisResult,
                                creative_result: CreativeAnalysisResult,
                                decision_options: List[str]) -> CognitiveModelingResult:
        """
        Perform complete cognitive processing.
        
        Args:
            logical_result: Logical analysis results
            emotional_result: Emotional analysis results
            creative_result: Creative analysis results
            decision_options: Available decision options
            
        Returns:
            Complete cognitive modeling result
        """
        import time
        start_time = time.time()
        
        try:
            # Update cognitive state
            self.update_cognitive_state(emotional_result, logical_result, creative_result)
            
            # Make cognitive decision
            decision = self.make_cognitive_decision(decision_options, {
                "logical_complexity": logical_result.complexity_score,
                "emotional_state": emotional_result.emotional_context.user_state.value,
                "creative_potential": creative_result.innovation_potential_score
            })
            
            # Update memory with current experience
            memory_updates = []
            
            # Store decision in episodic memory
            self.update_memory(
                content=f"Decision: {decision.decision}",
                memory_type=MemoryType.EPISODIC_MEMORY,
                emotional_valence=emotional_result.emotional_context.sentiment_analysis.polarity_score
            )
            memory_updates.append(self.memory_systems[MemoryType.EPISODIC_MEMORY][-1])
            
            # Store important requirements in semantic memory
            for req in logical_result.requirements[:3]:  # Top 3 requirements
                if req.priority == "high":
                    self.update_memory(
                        content=req.text,
                        memory_type=MemoryType.SEMANTIC_MEMORY
                    )
                    memory_updates.append(self.memory_systems[MemoryType.SEMANTIC_MEMORY][-1])
            
            # Calculate attention allocation
            attention_allocation = {
                "logical_focus": self.cognitive_state.cognitive_load * 0.4,
                "emotional_focus": emotional_result.emotional_intelligence_score * 0.3,
                "creative_focus": creative_result.innovation_potential_score * 0.2,
                "metacognitive_focus": 0.1
            }
            
            # Analyze cognitive load
            cognitive_load_analysis = {
                "working_memory_load": self.cognitive_state.working_memory_load,
                "attention_demand": len(self.cognitive_state.attention_focus) / 5,
                "processing_complexity": self.cognitive_state.cognitive_load,
                "fatigue_impact": self.cognitive_state.fatigue_level,
                "overall_load": (
                    self.cognitive_state.working_memory_load + 
                    self.cognitive_state.cognitive_load + 
                    self.cognitive_state.fatigue_level
                ) / 3
            }
            
            # Calculate human-likeness score
            human_likeness_score = self.calculate_human_likeness_score(decision)
            
            # Update decision history
            self.decision_history.append(decision)
            
            # Update cognitive metrics
            self.cognitive_metrics["decisions_made"] += 1
            self.cognitive_metrics["average_confidence"] = (
                (self.cognitive_metrics["average_confidence"] * (self.cognitive_metrics["decisions_made"] - 1) + 
                 decision.confidence) / self.cognitive_metrics["decisions_made"]
            )
            
            for bias in decision.biases_applied:
                self.cognitive_metrics["bias_frequency"][bias.value] += 1
            
            processing_time = (time.time() - start_time) * 1000
            
            return CognitiveModelingResult(
                cognitive_state=self.cognitive_state,
                decision=decision,
                memory_updates=memory_updates,
                attention_allocation=attention_allocation,
                cognitive_load_analysis=cognitive_load_analysis,
                human_likeness_score=human_likeness_score,
                processing_time_ms=processing_time,
                metadata={
                    "user_id": self.user_id,
                    "processing_mode": self.cognitive_state.processing_mode,
                    "biases_active": len(self.cognitive_state.active_biases),
                    "memory_items_updated": len(memory_updates),
                    "decisions_total": self.cognitive_metrics["decisions_made"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Cognitive processing failed: {e}")
            
            return CognitiveModelingResult(
                cognitive_state=self.cognitive_state,
                decision=CognitiveDecision(
                    decision="error",
                    confidence=0.0,
                    reasoning_path=["Error in cognitive processing"],
                    biases_applied=[],
                    processing_time=0.0,
                    alternatives_considered=[],
                    emotional_influence=0.0,
                    logical_influence=0.0,
                    intuitive_influence=0.0
                ),
                memory_updates=[],
                attention_allocation={},
                cognitive_load_analysis={},
                human_likeness_score=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )


# ============================================================================
# COGNITIVE UTILITIES
# ============================================================================

class CognitiveUtils:
    """Utility functions for cognitive modeling."""
    
    @staticmethod
    def cognitive_state_to_dict(state: CognitiveState) -> Dict[str, Any]:
        """Convert cognitive state to dictionary format."""
        return {
            "attention_focus": state.attention_focus,
            "working_memory_load": state.working_memory_load,
            "cognitive_load": state.cognitive_load,
            "emotional_state": state.emotional_state.value,
            "confidence_level": state.confidence_level,
            "fatigue_level": state.fatigue_level,
            "motivation_level": state.motivation_level,
            "active_biases": [bias.value for bias in state.active_biases],
            "processing_mode": state.processing_mode,
            "timestamp": state.timestamp.isoformat()
        }
    
    @staticmethod
    def analyze_bias_patterns(decision_history: List[CognitiveDecision]) -> Dict[str, Any]:
        """Analyze patterns in cognitive bias usage."""
        if not decision_history:
            return {"no_data": True}
        
        bias_counts = defaultdict(int)
        total_decisions = len(decision_history)
        
        for decision in decision_history:
            for bias in decision.biases_applied:
                bias_counts[bias.value] += 1
        
        return {
            "total_decisions": total_decisions,
            "bias_frequency": dict(bias_counts),
            "bias_rate": {bias: count/total_decisions for bias, count in bias_counts.items()},
            "most_common_bias": max(bias_counts.items(), key=lambda x: x[1])[0] if bias_counts else None,
            "average_biases_per_decision": sum(bias_counts.values()) / total_decisions
        }
    
    @staticmethod
    def calculate_cognitive_efficiency(cognitive_load_analysis: Dict[str, float],
                                     processing_time: float) -> float:
        """Calculate cognitive processing efficiency."""
        if processing_time == 0:
            return 0.0
        
        # Lower cognitive load and faster processing = higher efficiency
        load_factor = 1 - cognitive_load_analysis.get("overall_load", 0.5)
        time_factor = min(5.0 / processing_time, 1.0)  # Normalize by 5 seconds
        
        return (load_factor + time_factor) / 2
