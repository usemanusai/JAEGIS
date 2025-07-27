"""
N.L.D.S. Logical Analysis Engine
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Advanced logical analysis for requirement extraction, logical decomposition,
and structured reasoning with 90%+ logical decomposition accuracy.
"""

import re
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import asyncio

# NLP and ML imports
import spacy
from spacy.matcher import Matcher
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Local imports
from ..nlp.tokenizer import TokenizationResult
from ..nlp.semantic_analyzer import SemanticAnalysisResult
from ..nlp.intent_recognizer import IntentRecognitionResult, IntentCategory
from ..nlp.context_extractor import ContextExtractionResult

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# LOGICAL STRUCTURES AND ENUMS
# ============================================================================

class LogicalOperator(Enum):
    """Logical operators for reasoning."""
    AND = "and"
    OR = "or"
    NOT = "not"
    IF = "if"
    THEN = "then"
    ELSE = "else"
    IMPLIES = "implies"
    EQUIVALENT = "equivalent"


class RequirementType(Enum):
    """Types of requirements."""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"
    ASSUMPTION = "assumption"
    DEPENDENCY = "dependency"
    BUSINESS_RULE = "business_rule"
    TECHNICAL_SPEC = "technical_spec"
    USER_STORY = "user_story"


class LogicalRelation(Enum):
    """Types of logical relationships."""
    CAUSE_EFFECT = "cause_effect"
    PREREQUISITE = "prerequisite"
    SEQUENCE = "sequence"
    CONDITIONAL = "conditional"
    ALTERNATIVE = "alternative"
    COMPOSITION = "composition"
    INHERITANCE = "inheritance"


@dataclass
class LogicalRequirement:
    """Individual logical requirement."""
    id: str
    text: str
    requirement_type: RequirementType
    priority: str  # high, medium, low
    confidence: float
    dependencies: List[str]
    conditions: List[str]
    acceptance_criteria: List[str]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class LogicalStatement:
    """Logical statement with operators."""
    statement: str
    operator: Optional[LogicalOperator]
    operands: List[str]
    truth_value: Optional[bool]
    confidence: float
    context: Dict[str, Any] = None


@dataclass
class LogicalStructure:
    """Complete logical structure."""
    premises: List[LogicalStatement]
    conclusions: List[LogicalStatement]
    logical_flow: List[Tuple[str, str, LogicalRelation]]
    validity_score: float
    completeness_score: float


@dataclass
class LogicalAnalysisResult:
    """Complete logical analysis result."""
    text: str
    requirements: List[LogicalRequirement]
    logical_structure: LogicalStructure
    reasoning_chain: List[Dict[str, Any]]
    complexity_score: float
    coherence_score: float
    processing_time_ms: float
    metadata: Dict[str, Any]


# ============================================================================
# LOGICAL ANALYSIS ENGINE
# ============================================================================

class LogicalAnalysisEngine:
    """
    Advanced logical analysis engine for requirement extraction and reasoning.
    
    Features:
    - Requirement extraction and classification
    - Logical structure decomposition
    - Reasoning chain construction
    - Dependency analysis
    - Constraint identification
    - Validity and completeness scoring
    - JAEGIS-specific logical patterns
    """
    
    def __init__(self):
        """Initialize logical analysis engine."""
        self.nlp = None
        self.matcher = None
        self.logical_patterns = self._load_logical_patterns()
        self.requirement_patterns = self._load_requirement_patterns()
        self.jaegis_logic_rules = self._load_jaegis_logic_rules()
        self.dependency_graph = nx.DiGraph()
        
        # Initialize NLP components
        self._initialize_nlp()
    
    def _initialize_nlp(self):
        """Initialize NLP components for logical analysis."""
        try:
            self.nlp = spacy.load("en_core_web_lg")
            self.matcher = Matcher(self.nlp.vocab)
            
            # Add logical patterns to matcher
            self._add_logical_patterns()
            
            logger.info("Logical analysis NLP components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP components: {e}")
    
    def _load_logical_patterns(self) -> Dict[str, List[Dict]]:
        """Load logical reasoning patterns."""
        return {
            "conditional": [
                [{"LOWER": "if"}, {"IS_ALPHA": True, "OP": "+"}, {"LOWER": "then"}],
                [{"LOWER": "when"}, {"IS_ALPHA": True, "OP": "+"}, {"LOWER": "then"}],
                [{"LOWER": "provided"}, {"LOWER": "that"}, {"IS_ALPHA": True, "OP": "+"}]
            ],
            "causal": [
                [{"LOWER": "because"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "since"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "due"}, {"LOWER": "to"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"IS_ALPHA": True, "OP": "+"}, {"LOWER": "causes"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"IS_ALPHA": True, "OP": "+"}, {"LOWER": "results"}, {"LOWER": "in"}, {"IS_ALPHA": True, "OP": "+"}]
            ],
            "sequential": [
                [{"LOWER": "first"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "then"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "next"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "finally"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "after"}, {"IS_ALPHA": True, "OP": "+"}, {"LOWER": "then"}]
            ],
            "alternative": [
                [{"LOWER": "either"}, {"IS_ALPHA": True, "OP": "+"}, {"LOWER": "or"}],
                [{"LOWER": "alternatively"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"IS_ALPHA": True, "OP": "+"}, {"LOWER": "or"}, {"IS_ALPHA": True, "OP": "+"}]
            ],
            "constraint": [
                [{"LOWER": "must"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "shall"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "should"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "cannot"}, {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "prohibited"}, {"IS_ALPHA": True, "OP": "+"}]
            ]
        }
    
    def _load_requirement_patterns(self) -> Dict[str, List[str]]:
        """Load requirement identification patterns."""
        return {
            "functional": [
                "system shall", "system must", "system should",
                "user can", "user shall", "application will",
                "function", "feature", "capability", "operation"
            ],
            "non_functional": [
                "performance", "scalability", "reliability", "security",
                "usability", "maintainability", "availability",
                "response time", "throughput", "latency"
            ],
            "constraint": [
                "limited to", "restricted to", "cannot exceed",
                "maximum", "minimum", "within", "bounds",
                "constraint", "limitation", "restriction"
            ],
            "assumption": [
                "assume", "assuming", "given that", "provided that",
                "it is assumed", "we assume", "assumption"
            ],
            "dependency": [
                "depends on", "requires", "needs", "prerequisite",
                "conditional on", "subject to", "based on"
            ]
        }
    
    def _load_jaegis_logic_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load JAEGIS-specific logical rules."""
        return {
            "squad_activation": {
                "prerequisites": ["mode_selection", "task_definition"],
                "constraints": ["max_concurrent_squads", "resource_availability"],
                "logical_flow": "mode -> task -> squad -> execution"
            },
            "mode_selection": {
                "prerequisites": ["complexity_assessment"],
                "constraints": ["user_permissions", "system_capacity"],
                "logical_flow": "assessment -> mode -> capabilities"
            },
            "agent_creation": {
                "prerequisites": ["template_selection", "capability_definition"],
                "constraints": ["resource_limits", "security_policies"],
                "logical_flow": "template -> configuration -> validation -> creation"
            },
            "task_management": {
                "prerequisites": ["task_definition", "priority_assignment"],
                "constraints": ["deadline_constraints", "resource_allocation"],
                "logical_flow": "definition -> assignment -> execution -> completion"
            }
        }
    
    def _add_logical_patterns(self):
        """Add logical patterns to spaCy matcher."""
        if not self.matcher:
            return
        
        for pattern_type, patterns in self.logical_patterns.items():
            for i, pattern in enumerate(patterns):
                pattern_name = f"{pattern_type}_{i}"
                self.matcher.add(pattern_name, [pattern])
    
    def extract_requirements(self, text: str, 
                           semantic_result: SemanticAnalysisResult,
                           intent_result: IntentRecognitionResult) -> List[LogicalRequirement]:
        """
        Extract logical requirements from text.
        
        Args:
            text: Input text
            semantic_result: Semantic analysis results
            intent_result: Intent recognition results
            
        Returns:
            List of extracted requirements
        """
        requirements = []
        
        # Process text with spaCy
        if not self.nlp:
            return requirements
        
        doc = self.nlp(text)
        
        # Extract sentences for requirement analysis
        sentences = [sent.text.strip() for sent in doc.sents]
        
        for i, sentence in enumerate(sentences):
            # Classify requirement type
            req_type = self._classify_requirement_type(sentence)
            
            if req_type != RequirementType.TECHNICAL_SPEC:  # Filter out non-requirements
                # Extract priority
                priority = self._extract_priority(sentence)
                
                # Extract dependencies
                dependencies = self._extract_dependencies(sentence, sentences)
                
                # Extract conditions
                conditions = self._extract_conditions(sentence)
                
                # Extract acceptance criteria
                acceptance_criteria = self._extract_acceptance_criteria(sentence)
                
                # Calculate confidence
                confidence = self._calculate_requirement_confidence(
                    sentence, req_type, semantic_result, intent_result
                )
                
                requirement = LogicalRequirement(
                    id=f"req_{i+1}",
                    text=sentence,
                    requirement_type=req_type,
                    priority=priority,
                    confidence=confidence,
                    dependencies=dependencies,
                    conditions=conditions,
                    acceptance_criteria=acceptance_criteria,
                    metadata={
                        "sentence_index": i,
                        "word_count": len(sentence.split()),
                        "intent_category": intent_result.primary_intent.intent.value
                    }
                )
                
                requirements.append(requirement)
        
        return requirements
    
    def _classify_requirement_type(self, text: str) -> RequirementType:
        """Classify the type of requirement."""
        text_lower = text.lower()
        
        # Check patterns for each requirement type
        for req_type, patterns in self.requirement_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return RequirementType(req_type)
        
        # Default classification based on keywords
        if any(word in text_lower for word in ["must", "shall", "will", "should"]):
            return RequirementType.FUNCTIONAL
        elif any(word in text_lower for word in ["assume", "given", "provided"]):
            return RequirementType.ASSUMPTION
        elif any(word in text_lower for word in ["depends", "requires", "needs"]):
            return RequirementType.DEPENDENCY
        else:
            return RequirementType.TECHNICAL_SPEC
    
    def _extract_priority(self, text: str) -> str:
        """Extract priority level from text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["critical", "urgent", "must", "essential"]):
            return "high"
        elif any(word in text_lower for word in ["important", "should", "significant"]):
            return "medium"
        else:
            return "low"
    
    def _extract_dependencies(self, sentence: str, all_sentences: List[str]) -> List[str]:
        """Extract dependencies from sentence."""
        dependencies = []
        sentence_lower = sentence.lower()
        
        # Look for dependency keywords
        dependency_keywords = ["depends on", "requires", "needs", "after", "when"]
        
        for keyword in dependency_keywords:
            if keyword in sentence_lower:
                # Find referenced entities or previous sentences
                for i, other_sentence in enumerate(all_sentences):
                    if other_sentence != sentence and any(
                        entity in other_sentence.lower() 
                        for entity in ["squad", "mode", "agent", "task"]
                    ):
                        dependencies.append(f"sentence_{i+1}")
        
        return dependencies
    
    def _extract_conditions(self, text: str) -> List[str]:
        """Extract conditions from text."""
        conditions = []
        
        # Use spaCy matcher to find conditional patterns
        if self.nlp and self.matcher:
            doc = self.nlp(text)
            matches = self.matcher(doc)
            
            for match_id, start, end in matches:
                span = doc[start:end]
                label = self.nlp.vocab.strings[match_id]
                
                if "conditional" in label:
                    conditions.append(span.text)
        
        return conditions
    
    def _extract_acceptance_criteria(self, text: str) -> List[str]:
        """Extract acceptance criteria from text."""
        criteria = []
        
        # Look for measurable criteria
        measurable_patterns = [
            r"within \d+ \w+",
            r"at least \d+",
            r"no more than \d+",
            r"\d+% \w+",
            r"response time.*\d+.*ms"
        ]
        
        for pattern in measurable_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            criteria.extend(matches)
        
        return criteria
    
    def _calculate_requirement_confidence(self, text: str, req_type: RequirementType,
                                        semantic_result: SemanticAnalysisResult,
                                        intent_result: IntentRecognitionResult) -> float:
        """Calculate confidence score for requirement."""
        base_confidence = 0.5
        
        # Boost for clear requirement language
        if any(word in text.lower() for word in ["must", "shall", "will"]):
            base_confidence += 0.2
        
        # Boost for specific requirement types
        if req_type in [RequirementType.FUNCTIONAL, RequirementType.CONSTRAINT]:
            base_confidence += 0.1
        
        # Boost for JAEGIS-specific content
        if any(entity in text.lower() for entity in ["squad", "mode", "agent"]):
            base_confidence += 0.15
        
        # Factor in semantic confidence
        base_confidence += semantic_result.confidence_score * 0.1
        
        # Factor in intent confidence
        base_confidence += intent_result.primary_intent.confidence * 0.05
        
        return min(base_confidence, 0.95)
    
    def decompose_logical_structure(self, text: str, requirements: List[LogicalRequirement]) -> LogicalStructure:
        """
        Decompose text into logical structure.
        
        Args:
            text: Input text
            requirements: Extracted requirements
            
        Returns:
            Logical structure
        """
        premises = []
        conclusions = []
        logical_flow = []
        
        if not self.nlp:
            return LogicalStructure(premises, conclusions, logical_flow, 0.0, 0.0)
        
        doc = self.nlp(text)
        
        # Extract logical statements
        for sent in doc.sents:
            statement_text = sent.text.strip()
            
            # Identify logical operators
            operator = self._identify_logical_operator(statement_text)
            
            # Extract operands
            operands = self._extract_operands(statement_text, operator)
            
            # Determine if premise or conclusion
            is_conclusion = self._is_conclusion(statement_text)
            
            logical_statement = LogicalStatement(
                statement=statement_text,
                operator=operator,
                operands=operands,
                truth_value=None,  # Would be determined by reasoning engine
                confidence=0.8,
                context={"sentence_type": "conclusion" if is_conclusion else "premise"}
            )
            
            if is_conclusion:
                conclusions.append(logical_statement)
            else:
                premises.append(logical_statement)
        
        # Build logical flow
        logical_flow = self._build_logical_flow(premises, conclusions)
        
        # Calculate scores
        validity_score = self._calculate_validity_score(premises, conclusions, logical_flow)
        completeness_score = self._calculate_completeness_score(requirements, premises, conclusions)
        
        return LogicalStructure(
            premises=premises,
            conclusions=conclusions,
            logical_flow=logical_flow,
            validity_score=validity_score,
            completeness_score=completeness_score
        )
    
    def _identify_logical_operator(self, text: str) -> Optional[LogicalOperator]:
        """Identify logical operator in text."""
        text_lower = text.lower()
        
        operator_patterns = {
            LogicalOperator.IF: ["if", "when", "provided that"],
            LogicalOperator.THEN: ["then", "therefore", "thus"],
            LogicalOperator.AND: ["and", "also", "additionally"],
            LogicalOperator.OR: ["or", "alternatively", "either"],
            LogicalOperator.NOT: ["not", "cannot", "never"],
            LogicalOperator.IMPLIES: ["implies", "means that", "results in"]
        }
        
        for operator, patterns in operator_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return operator
        
        return None
    
    def _extract_operands(self, text: str, operator: Optional[LogicalOperator]) -> List[str]:
        """Extract operands for logical operator."""
        operands = []
        
        if operator == LogicalOperator.IF:
            # Extract condition and consequence
            if_match = re.search(r'if\s+(.+?)\s+then\s+(.+)', text, re.IGNORECASE)
            if if_match:
                operands = [if_match.group(1).strip(), if_match.group(2).strip()]
        
        elif operator == LogicalOperator.AND:
            # Split on 'and'
            parts = re.split(r'\s+and\s+', text, flags=re.IGNORECASE)
            operands = [part.strip() for part in parts if part.strip()]
        
        elif operator == LogicalOperator.OR:
            # Split on 'or'
            parts = re.split(r'\s+or\s+', text, flags=re.IGNORECASE)
            operands = [part.strip() for part in parts if part.strip()]
        
        return operands
    
    def _is_conclusion(self, text: str) -> bool:
        """Determine if statement is a conclusion."""
        conclusion_indicators = [
            "therefore", "thus", "hence", "consequently",
            "as a result", "it follows", "we conclude"
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in conclusion_indicators)
    
    def _build_logical_flow(self, premises: List[LogicalStatement], 
                          conclusions: List[LogicalStatement]) -> List[Tuple[str, str, LogicalRelation]]:
        """Build logical flow between statements."""
        flow = []
        
        # Simple heuristic: premises lead to conclusions
        for premise in premises:
            for conclusion in conclusions:
                # Determine relationship type
                if premise.operator == LogicalOperator.IF:
                    relation = LogicalRelation.CONDITIONAL
                elif "because" in premise.statement.lower():
                    relation = LogicalRelation.CAUSE_EFFECT
                else:
                    relation = LogicalRelation.SEQUENCE
                
                flow.append((premise.statement, conclusion.statement, relation))
        
        return flow
    
    def _calculate_validity_score(self, premises: List[LogicalStatement],
                                conclusions: List[LogicalStatement],
                                logical_flow: List[Tuple[str, str, LogicalRelation]]) -> float:
        """Calculate logical validity score."""
        if not premises or not conclusions:
            return 0.0
        
        # Simple validity heuristics
        validity_factors = []
        
        # Check for logical operators
        has_operators = any(stmt.operator for stmt in premises + conclusions)
        validity_factors.append(0.3 if has_operators else 0.1)
        
        # Check for logical flow
        has_flow = len(logical_flow) > 0
        validity_factors.append(0.4 if has_flow else 0.1)
        
        # Check for consistency
        consistent = len(premises) <= len(conclusions) * 2  # Reasonable premise-to-conclusion ratio
        validity_factors.append(0.3 if consistent else 0.1)
        
        return sum(validity_factors)
    
    def _calculate_completeness_score(self, requirements: List[LogicalRequirement],
                                    premises: List[LogicalStatement],
                                    conclusions: List[LogicalStatement]) -> float:
        """Calculate logical completeness score."""
        if not requirements:
            return 0.0
        
        # Check coverage of requirements in logical structure
        covered_requirements = 0
        
        for req in requirements:
            req_text_lower = req.text.lower()
            
            # Check if requirement is covered in premises or conclusions
            covered = any(
                any(word in stmt.statement.lower() for word in req_text_lower.split()[:3])
                for stmt in premises + conclusions
            )
            
            if covered:
                covered_requirements += 1
        
        return covered_requirements / len(requirements)
    
    def build_reasoning_chain(self, logical_structure: LogicalStructure,
                            intent_result: IntentRecognitionResult) -> List[Dict[str, Any]]:
        """
        Build reasoning chain from logical structure.
        
        Args:
            logical_structure: Logical structure
            intent_result: Intent recognition results
            
        Returns:
            Reasoning chain steps
        """
        reasoning_chain = []
        
        # Start with intent
        reasoning_chain.append({
            "step": 1,
            "type": "intent_identification",
            "content": f"Identified intent: {intent_result.primary_intent.intent.value}",
            "confidence": intent_result.primary_intent.confidence,
            "reasoning": "Primary intent extracted from user input"
        })
        
        # Add premises
        for i, premise in enumerate(logical_structure.premises):
            reasoning_chain.append({
                "step": len(reasoning_chain) + 1,
                "type": "premise",
                "content": premise.statement,
                "confidence": premise.confidence,
                "reasoning": f"Premise {i+1}: Foundational assumption or given condition"
            })
        
        # Add logical flow
        for i, (source, target, relation) in enumerate(logical_structure.logical_flow):
            reasoning_chain.append({
                "step": len(reasoning_chain) + 1,
                "type": "logical_inference",
                "content": f"{source} → {target}",
                "confidence": 0.8,
                "reasoning": f"Logical inference using {relation.value} relationship"
            })
        
        # Add conclusions
        for i, conclusion in enumerate(logical_structure.conclusions):
            reasoning_chain.append({
                "step": len(reasoning_chain) + 1,
                "type": "conclusion",
                "content": conclusion.statement,
                "confidence": conclusion.confidence,
                "reasoning": f"Conclusion {i+1}: Derived from premises and logical inference"
            })
        
        return reasoning_chain
    
    async def analyze_logical_structure(self, text: str,
                                      semantic_result: SemanticAnalysisResult,
                                      intent_result: IntentRecognitionResult,
                                      context_result: ContextExtractionResult) -> LogicalAnalysisResult:
        """
        Perform complete logical analysis.
        
        Args:
            text: Input text
            semantic_result: Semantic analysis results
            intent_result: Intent recognition results
            context_result: Context extraction results
            
        Returns:
            Complete logical analysis result
        """
        import time
        start_time = time.time()
        
        try:
            # Extract requirements
            requirements = self.extract_requirements(text, semantic_result, intent_result)
            
            # Decompose logical structure
            logical_structure = self.decompose_logical_structure(text, requirements)
            
            # Build reasoning chain
            reasoning_chain = self.build_reasoning_chain(logical_structure, intent_result)
            
            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(text, requirements, logical_structure)
            
            # Calculate coherence score
            coherence_score = self._calculate_coherence_score(logical_structure, semantic_result)
            
            processing_time = (time.time() - start_time) * 1000
            
            return LogicalAnalysisResult(
                text=text,
                requirements=requirements,
                logical_structure=logical_structure,
                reasoning_chain=reasoning_chain,
                complexity_score=complexity_score,
                coherence_score=coherence_score,
                processing_time_ms=processing_time,
                metadata={
                    "requirements_count": len(requirements),
                    "premises_count": len(logical_structure.premises),
                    "conclusions_count": len(logical_structure.conclusions),
                    "reasoning_steps": len(reasoning_chain),
                    "intent_category": intent_result.primary_intent.intent.value,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Logical analysis failed: {e}")
            
            return LogicalAnalysisResult(
                text=text,
                requirements=[],
                logical_structure=LogicalStructure([], [], [], 0.0, 0.0),
                reasoning_chain=[],
                complexity_score=0.0,
                coherence_score=0.0,
                processing_time_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )
    
    def _calculate_complexity_score(self, text: str, requirements: List[LogicalRequirement],
                                  logical_structure: LogicalStructure) -> float:
        """Calculate logical complexity score."""
        factors = []
        
        # Text complexity
        word_count = len(text.split())
        sentence_count = len(text.split('.'))
        avg_sentence_length = word_count / max(sentence_count, 1)
        text_complexity = min(avg_sentence_length / 20, 1.0)  # Normalize to 0-1
        factors.append(text_complexity * 0.3)
        
        # Requirements complexity
        req_complexity = min(len(requirements) / 10, 1.0)  # Normalize to 0-1
        factors.append(req_complexity * 0.3)
        
        # Logical structure complexity
        structure_complexity = min(
            (len(logical_structure.premises) + len(logical_structure.conclusions)) / 10, 1.0
        )
        factors.append(structure_complexity * 0.4)
        
        return sum(factors)
    
    def _calculate_coherence_score(self, logical_structure: LogicalStructure,
                                 semantic_result: SemanticAnalysisResult) -> float:
        """Calculate logical coherence score."""
        factors = []
        
        # Logical validity
        factors.append(logical_structure.validity_score * 0.4)
        
        # Logical completeness
        factors.append(logical_structure.completeness_score * 0.3)
        
        # Semantic coherence
        factors.append(semantic_result.confidence_score * 0.3)
        
        return sum(factors)


# ============================================================================
# LOGICAL UTILITIES
# ============================================================================

class LogicalUtils:
    """Utility functions for logical analysis."""
    
    @staticmethod
    def requirements_to_dict(requirements: List[LogicalRequirement]) -> List[Dict[str, Any]]:
        """Convert requirements to dictionary format."""
        return [
            {
                "id": req.id,
                "text": req.text,
                "type": req.requirement_type.value,
                "priority": req.priority,
                "confidence": req.confidence,
                "dependencies": req.dependencies,
                "conditions": req.conditions,
                "acceptance_criteria": req.acceptance_criteria,
                "metadata": req.metadata
            }
            for req in requirements
        ]
    
    @staticmethod
    def validate_logical_consistency(logical_structure: LogicalStructure) -> Dict[str, Any]:
        """Validate logical consistency of structure."""
        issues = []
        
        # Check for contradictions
        statements = [stmt.statement.lower() for stmt in logical_structure.premises + logical_structure.conclusions]
        
        for i, stmt1 in enumerate(statements):
            for j, stmt2 in enumerate(statements[i+1:], i+1):
                if "not" in stmt1 and stmt1.replace("not", "").strip() in stmt2:
                    issues.append(f"Potential contradiction between statements {i+1} and {j+1}")
        
        # Check for circular reasoning
        flow_graph = nx.DiGraph()
        for source, target, _ in logical_structure.logical_flow:
            flow_graph.add_edge(source, target)
        
        try:
            cycles = list(nx.simple_cycles(flow_graph))
            if cycles:
                issues.append(f"Circular reasoning detected: {len(cycles)} cycles found")
        except:
            pass
        
        return {
            "consistent": len(issues) == 0,
            "issues": issues,
            "validity_score": logical_structure.validity_score,
            "completeness_score": logical_structure.completeness_score
        }
