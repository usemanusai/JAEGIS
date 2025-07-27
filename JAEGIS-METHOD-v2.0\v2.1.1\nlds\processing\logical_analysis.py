"""
N.L.D.S. Logical Analysis Engine
Structured reasoning engine for requirement extraction and logical decomposition
"""

import re
import spacy
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from collections import defaultdict, deque
import time

logger = logging.getLogger(__name__)


class LogicalRelationType(str, Enum):
    """Types of logical relationships."""
    CAUSE_EFFECT = "cause_effect"
    PREREQUISITE = "prerequisite"
    DEPENDENCY = "dependency"
    SEQUENCE = "sequence"
    CONDITIONAL = "conditional"
    ALTERNATIVE = "alternative"
    COMPOSITION = "composition"
    CLASSIFICATION = "classification"


class RequirementType(str, Enum):
    """Types of requirements."""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    TECHNICAL = "technical"
    BUSINESS = "business"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USABILITY = "usability"
    CONSTRAINT = "constraint"


class LogicalOperator(str, Enum):
    """Logical operators for reasoning."""
    AND = "and"
    OR = "or"
    NOT = "not"
    IF_THEN = "if_then"
    IF_AND_ONLY_IF = "if_and_only_if"
    IMPLIES = "implies"


@dataclass
class LogicalStatement:
    """Logical statement representation."""
    statement_id: str
    text: str
    subject: str
    predicate: str
    object: Optional[str]
    modifiers: List[str]
    confidence: float
    statement_type: str
    logical_form: str


@dataclass
class Requirement:
    """Extracted requirement."""
    requirement_id: str
    text: str
    requirement_type: RequirementType
    priority: str
    stakeholder: Optional[str]
    acceptance_criteria: List[str]
    dependencies: List[str]
    constraints: List[str]
    confidence: float
    source_statements: List[str]


@dataclass
class LogicalRelation:
    """Logical relationship between entities."""
    relation_id: str
    relation_type: LogicalRelationType
    source: str
    target: str
    strength: float
    evidence: List[str]
    logical_operator: Optional[LogicalOperator]


@dataclass
class LogicalAnalysisResult:
    """Logical analysis result."""
    statements: List[LogicalStatement]
    requirements: List[Requirement]
    relations: List[LogicalRelation]
    reasoning_chain: List[Dict[str, Any]]
    logical_consistency: float
    completeness_score: float
    processing_time_ms: float
    analysis_confidence: float


class LogicalAnalysisEngine:
    """
    Structured reasoning engine for requirement extraction and logical decomposition.
    
    Provides systematic analysis of natural language input to extract logical
    structures, requirements, and reasoning chains for JAEGIS command generation.
    """
    
    def __init__(self):
        # Initialize spaCy for linguistic analysis
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            try:
                self.nlp = spacy.load("en_core_web_md")
            except OSError:
                self.nlp = spacy.load("en_core_web_sm")
        
        # Logical patterns and indicators
        self.logical_patterns = self._initialize_logical_patterns()
        
        # Requirement extraction patterns
        self.requirement_patterns = self._initialize_requirement_patterns()
        
        # Logical operators and connectives
        self.logical_connectives = self._initialize_logical_connectives()
        
        # Reasoning templates
        self.reasoning_templates = self._initialize_reasoning_templates()
        
        # Priority indicators
        self.priority_indicators = self._initialize_priority_indicators()
        
        logger.info("Logical Analysis Engine initialized")
    
    def _initialize_logical_patterns(self) -> Dict[str, List[str]]:
        """Initialize logical reasoning patterns."""
        
        return {
            "cause_effect": [
                r"because\s+(.+?),\s*(.+)",
                r"(.+?)\s+causes?\s+(.+)",
                r"(.+?)\s+results?\s+in\s+(.+)",
                r"due\s+to\s+(.+?),\s*(.+)",
                r"as\s+a\s+result\s+of\s+(.+?),\s*(.+)"
            ],
            
            "conditional": [
                r"if\s+(.+?),?\s+then\s+(.+)",
                r"when\s+(.+?),\s*(.+)",
                r"provided\s+that\s+(.+?),\s*(.+)",
                r"assuming\s+(.+?),\s*(.+)",
                r"given\s+(.+?),\s*(.+)"
            ],
            
            "prerequisite": [
                r"before\s+(.+?),\s*(.+)",
                r"(.+?)\s+requires?\s+(.+)",
                r"(.+?)\s+needs?\s+(.+)",
                r"(.+?)\s+depends?\s+on\s+(.+)",
                r"first\s+(.+?),?\s+then\s+(.+)"
            ],
            
            "sequence": [
                r"first\s+(.+?),?\s+then\s+(.+)",
                r"after\s+(.+?),\s*(.+)",
                r"once\s+(.+?),\s*(.+)",
                r"step\s+\d+:\s*(.+)",
                r"next,?\s+(.+)"
            ],
            
            "alternative": [
                r"either\s+(.+?)\s+or\s+(.+)",
                r"(.+?)\s+or\s+alternatively\s+(.+)",
                r"(.+?)\s+instead\s+of\s+(.+)",
                r"(.+?)\s+rather\s+than\s+(.+)"
            ]
        }
    
    def _initialize_requirement_patterns(self) -> Dict[RequirementType, List[str]]:
        """Initialize requirement extraction patterns."""
        
        return {
            RequirementType.FUNCTIONAL: [
                r"(?:system|application|service)\s+(?:must|should|shall)\s+(.+)",
                r"(?:user|actor)\s+(?:can|should be able to)\s+(.+)",
                r"(?:feature|functionality)\s+(?:to|for)\s+(.+)",
                r"(?:implement|create|build)\s+(.+?)\s+(?:feature|function|capability)"
            ],
            
            RequirementType.NON_FUNCTIONAL: [
                r"(?:performance|speed|response time)\s+(?:must|should)\s+(.+)",
                r"(?:system|application)\s+(?:must|should)\s+(?:handle|support)\s+(.+)",
                r"(?:availability|uptime)\s+(?:of|must be)\s+(.+)",
                r"(?:scalability|capacity)\s+(?:to|for)\s+(.+)"
            ],
            
            RequirementType.SECURITY: [
                r"(?:secure|security|protect|authentication|authorization)\s+(.+)",
                r"(?:encrypt|encryption)\s+(.+)",
                r"(?:access control|permissions)\s+(?:for|to)\s+(.+)",
                r"(?:audit|logging)\s+(?:of|for)\s+(.+)"
            ],
            
            RequirementType.TECHNICAL: [
                r"(?:using|with|based on)\s+(.+?)\s+(?:technology|framework|platform)",
                r"(?:integrate|integration)\s+(?:with|to)\s+(.+)",
                r"(?:api|interface)\s+(?:for|to)\s+(.+)",
                r"(?:database|storage)\s+(?:for|to)\s+(.+)"
            ],
            
            RequirementType.CONSTRAINT: [
                r"(?:cannot|must not|should not)\s+(.+)",
                r"(?:limited|restricted)\s+(?:to|by)\s+(.+)",
                r"(?:within|under)\s+(.+?)\s+(?:budget|time|constraint)",
                r"(?:compliance|compliant)\s+(?:with|to)\s+(.+)"
            ]
        }
    
    def _initialize_logical_connectives(self) -> Dict[str, LogicalOperator]:
        """Initialize logical connectives mapping."""
        
        return {
            "and": LogicalOperator.AND,
            "also": LogicalOperator.AND,
            "additionally": LogicalOperator.AND,
            "furthermore": LogicalOperator.AND,
            "moreover": LogicalOperator.AND,
            
            "or": LogicalOperator.OR,
            "alternatively": LogicalOperator.OR,
            "either": LogicalOperator.OR,
            "otherwise": LogicalOperator.OR,
            
            "not": LogicalOperator.NOT,
            "cannot": LogicalOperator.NOT,
            "without": LogicalOperator.NOT,
            "except": LogicalOperator.NOT,
            
            "if": LogicalOperator.IF_THEN,
            "when": LogicalOperator.IF_THEN,
            "provided": LogicalOperator.IF_THEN,
            "assuming": LogicalOperator.IF_THEN,
            
            "implies": LogicalOperator.IMPLIES,
            "means": LogicalOperator.IMPLIES,
            "suggests": LogicalOperator.IMPLIES,
            "indicates": LogicalOperator.IMPLIES
        }
    
    def _initialize_reasoning_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize reasoning templates."""
        
        return {
            "requirement_decomposition": {
                "pattern": "break down {requirement} into components",
                "steps": ["identify main components", "analyze dependencies", "define interfaces"]
            },
            
            "cause_analysis": {
                "pattern": "analyze causes of {problem}",
                "steps": ["identify symptoms", "trace root causes", "validate causal relationships"]
            },
            
            "solution_design": {
                "pattern": "design solution for {problem}",
                "steps": ["understand requirements", "evaluate alternatives", "select optimal approach"]
            },
            
            "dependency_analysis": {
                "pattern": "analyze dependencies for {component}",
                "steps": ["identify direct dependencies", "trace transitive dependencies", "detect circular dependencies"]
            }
        }
    
    def _initialize_priority_indicators(self) -> Dict[str, int]:
        """Initialize priority indicators."""
        
        return {
            "critical": 5,
            "urgent": 5,
            "high": 4,
            "important": 4,
            "medium": 3,
            "normal": 3,
            "low": 2,
            "nice to have": 1,
            "optional": 1
        }
    
    def analyze_logical_structure(self, text: str, context: Optional[Dict[str, Any]] = None) -> LogicalAnalysisResult:
        """Analyze logical structure of input text."""
        
        start_time = time.time()
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Extract logical statements
        statements = self._extract_logical_statements(doc, text)
        
        # Extract requirements
        requirements = self._extract_requirements(doc, text, statements)
        
        # Identify logical relations
        relations = self._identify_logical_relations(statements, doc)
        
        # Build reasoning chain
        reasoning_chain = self._build_reasoning_chain(statements, relations, requirements)
        
        # Assess logical consistency
        logical_consistency = self._assess_logical_consistency(statements, relations)
        
        # Calculate completeness score
        completeness_score = self._calculate_completeness_score(requirements, relations)
        
        # Calculate overall confidence
        analysis_confidence = self._calculate_analysis_confidence(
            statements, requirements, relations, logical_consistency
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return LogicalAnalysisResult(
            statements=statements,
            requirements=requirements,
            relations=relations,
            reasoning_chain=reasoning_chain,
            logical_consistency=logical_consistency,
            completeness_score=completeness_score,
            processing_time_ms=processing_time,
            analysis_confidence=analysis_confidence
        )
    
    def _extract_logical_statements(self, doc, text: str) -> List[LogicalStatement]:
        """Extract logical statements from text."""
        
        statements = []
        
        # Process sentences
        for sent_idx, sent in enumerate(doc.sents):
            # Extract subject, predicate, object
            subject, predicate, obj = self._extract_spo_triple(sent)
            
            if subject and predicate:
                # Extract modifiers
                modifiers = self._extract_modifiers(sent)
                
                # Determine statement type
                statement_type = self._classify_statement_type(sent.text)
                
                # Generate logical form
                logical_form = self._generate_logical_form(subject, predicate, obj, modifiers)
                
                # Calculate confidence
                confidence = self._calculate_statement_confidence(sent, subject, predicate, obj)
                
                statement = LogicalStatement(
                    statement_id=f"stmt_{sent_idx}",
                    text=sent.text.strip(),
                    subject=subject,
                    predicate=predicate,
                    object=obj,
                    modifiers=modifiers,
                    confidence=confidence,
                    statement_type=statement_type,
                    logical_form=logical_form
                )
                
                statements.append(statement)
        
        return statements
    
    def _extract_spo_triple(self, sent) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract Subject-Predicate-Object triple from sentence."""
        
        subject = None
        predicate = None
        obj = None
        
        # Find root verb (predicate)
        for token in sent:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                predicate = token.lemma_
                break
        
        # Find subject
        for token in sent:
            if token.dep_ in ["nsubj", "nsubjpass"]:
                subject = self._extract_noun_phrase(token)
                break
        
        # Find object
        for token in sent:
            if token.dep_ in ["dobj", "pobj", "attr"]:
                obj = self._extract_noun_phrase(token)
                break
        
        return subject, predicate, obj
    
    def _extract_noun_phrase(self, token) -> str:
        """Extract full noun phrase from token."""
        
        # Get the noun phrase that includes this token
        for chunk in token.doc.noun_chunks:
            if token in chunk:
                return chunk.text
        
        # Fallback to token text
        return token.text
    
    def _extract_modifiers(self, sent) -> List[str]:
        """Extract modifiers from sentence."""
        
        modifiers = []
        
        for token in sent:
            if token.dep_ in ["advmod", "amod", "prep"]:
                modifiers.append(token.text)
        
        return modifiers
    
    def _classify_statement_type(self, text: str) -> str:
        """Classify the type of logical statement."""
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["if", "when", "provided", "assuming"]):
            return "conditional"
        elif any(word in text_lower for word in ["because", "since", "due to", "causes"]):
            return "causal"
        elif any(word in text_lower for word in ["must", "should", "shall", "required"]):
            return "requirement"
        elif any(word in text_lower for word in ["before", "after", "then", "next"]):
            return "sequential"
        elif "?" in text:
            return "question"
        else:
            return "declarative"
    
    def _generate_logical_form(self, subject: str, predicate: str, 
                             obj: Optional[str], modifiers: List[str]) -> str:
        """Generate logical form representation."""
        
        if obj:
            logical_form = f"{predicate}({subject}, {obj})"
        else:
            logical_form = f"{predicate}({subject})"
        
        if modifiers:
            modifier_str = " ∧ ".join(f"modifier({mod})" for mod in modifiers)
            logical_form = f"{logical_form} ∧ {modifier_str}"
        
        return logical_form
    
    def _calculate_statement_confidence(self, sent, subject: str, 
                                      predicate: str, obj: Optional[str]) -> float:
        """Calculate confidence in statement extraction."""
        
        confidence = 0.5  # Base confidence
        
        # Boost for complete SPO triple
        if subject and predicate and obj:
            confidence += 0.3
        elif subject and predicate:
            confidence += 0.2
        
        # Boost for clear sentence structure
        if len(sent) > 3:  # Reasonable sentence length
            confidence += 0.1
        
        # Boost for named entities
        if any(ent.label_ in ["PERSON", "ORG", "PRODUCT"] for ent in sent.ents):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _extract_requirements(self, doc, text: str, statements: List[LogicalStatement]) -> List[Requirement]:
        """Extract requirements from text and statements."""
        
        requirements = []
        
        # Extract using patterns
        for req_type, patterns in self.requirement_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    requirement_text = match.group(0)
                    extracted_content = match.group(1) if match.groups() else requirement_text
                    
                    # Determine priority
                    priority = self._extract_priority(requirement_text)
                    
                    # Extract acceptance criteria
                    acceptance_criteria = self._extract_acceptance_criteria(requirement_text)
                    
                    # Find dependencies
                    dependencies = self._find_requirement_dependencies(requirement_text, statements)
                    
                    # Extract constraints
                    constraints = self._extract_constraints(requirement_text)
                    
                    # Calculate confidence
                    confidence = self._calculate_requirement_confidence(requirement_text, req_type)
                    
                    requirement = Requirement(
                        requirement_id=f"req_{len(requirements)}",
                        text=requirement_text,
                        requirement_type=req_type,
                        priority=priority,
                        stakeholder=None,  # Could be extracted with more sophisticated analysis
                        acceptance_criteria=acceptance_criteria,
                        dependencies=dependencies,
                        constraints=constraints,
                        confidence=confidence,
                        source_statements=[stmt.statement_id for stmt in statements 
                                         if requirement_text.lower() in stmt.text.lower()]
                    )
                    
                    requirements.append(requirement)
        
        return requirements
    
    def _extract_priority(self, text: str) -> str:
        """Extract priority from requirement text."""
        
        text_lower = text.lower()
        
        for priority_word, priority_value in self.priority_indicators.items():
            if priority_word in text_lower:
                if priority_value >= 5:
                    return "critical"
                elif priority_value >= 4:
                    return "high"
                elif priority_value >= 3:
                    return "medium"
                elif priority_value >= 2:
                    return "low"
                else:
                    return "optional"
        
        return "medium"  # Default priority
    
    def _extract_acceptance_criteria(self, text: str) -> List[str]:
        """Extract acceptance criteria from requirement text."""
        
        criteria = []
        
        # Look for measurable criteria
        measurable_patterns = [
            r"(\d+(?:\.\d+)?)\s*(?:seconds?|ms|minutes?)",  # Time
            r"(\d+(?:\.\d+)?)\s*(?:%|percent)",  # Percentage
            r"(\d+(?:,\d{3})*)\s*(?:users?|requests?|transactions?)",  # Volume
            r"(\d+(?:\.\d+)?)\s*(?:MB|GB|TB)"  # Size
        ]
        
        for pattern in measurable_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                criteria.append(f"Measurable: {match}")
        
        # Look for behavioral criteria
        if "must" in text.lower():
            criteria.append("Mandatory requirement")
        if "should" in text.lower():
            criteria.append("Recommended requirement")
        
        return criteria
    
    def _find_requirement_dependencies(self, req_text: str, statements: List[LogicalStatement]) -> List[str]:
        """Find dependencies for a requirement."""
        
        dependencies = []
        req_lower = req_text.lower()
        
        # Look for explicit dependency keywords
        dependency_keywords = ["requires", "needs", "depends on", "after", "before"]
        
        for keyword in dependency_keywords:
            if keyword in req_lower:
                # Find related statements
                for stmt in statements:
                    if any(word in stmt.text.lower() for word in req_lower.split()):
                        dependencies.append(stmt.statement_id)
        
        return dependencies
    
    def _extract_constraints(self, text: str) -> List[str]:
        """Extract constraints from requirement text."""
        
        constraints = []
        text_lower = text.lower()
        
        # Time constraints
        time_patterns = [
            r"within\s+(\d+\s+(?:days?|weeks?|months?))",
            r"by\s+(\w+\s+\d+)",
            r"deadline\s+(?:of\s+)?(\w+\s+\d+)"
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                constraints.append(f"Time constraint: {match}")
        
        # Budget constraints
        if "budget" in text_lower or "cost" in text_lower:
            constraints.append("Budget constraint")
        
        # Technology constraints
        tech_constraints = ["using", "with", "based on", "compatible with"]
        for constraint in tech_constraints:
            if constraint in text_lower:
                constraints.append(f"Technology constraint: {constraint}")
        
        return constraints
    
    def _calculate_requirement_confidence(self, text: str, req_type: RequirementType) -> float:
        """Calculate confidence in requirement extraction."""
        
        confidence = 0.6  # Base confidence
        
        # Boost for clear requirement indicators
        requirement_indicators = ["must", "shall", "should", "required", "need"]
        if any(indicator in text.lower() for indicator in requirement_indicators):
            confidence += 0.2
        
        # Boost for specific requirement type indicators
        if req_type == RequirementType.FUNCTIONAL and any(word in text.lower() 
                                                         for word in ["function", "feature", "capability"]):
            confidence += 0.1
        elif req_type == RequirementType.SECURITY and any(word in text.lower() 
                                                         for word in ["secure", "protect", "encrypt"]):
            confidence += 0.1
        
        # Boost for measurable criteria
        if re.search(r'\d+', text):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _identify_logical_relations(self, statements: List[LogicalStatement], doc) -> List[LogicalRelation]:
        """Identify logical relations between statements."""
        
        relations = []
        
        # Check each pair of statements for relationships
        for i, stmt1 in enumerate(statements):
            for j, stmt2 in enumerate(statements):
                if i != j:
                    relation = self._analyze_statement_relationship(stmt1, stmt2, doc)
                    if relation:
                        relations.append(relation)
        
        # Extract relations from logical patterns
        text = doc.text
        for relation_type, patterns in self.logical_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    if len(match.groups()) >= 2:
                        source_text = match.group(1).strip()
                        target_text = match.group(2).strip()
                        
                        relation = LogicalRelation(
                            relation_id=f"rel_{len(relations)}",
                            relation_type=LogicalRelationType(relation_type),
                            source=source_text,
                            target=target_text,
                            strength=0.8,
                            evidence=[match.group(0)],
                            logical_operator=self._infer_logical_operator(match.group(0))
                        )
                        
                        relations.append(relation)
        
        return relations
    
    def _analyze_statement_relationship(self, stmt1: LogicalStatement, 
                                      stmt2: LogicalStatement, doc) -> Optional[LogicalRelation]:
        """Analyze relationship between two statements."""
        
        # Check for shared entities
        shared_entities = set(stmt1.text.lower().split()) & set(stmt2.text.lower().split())
        
        if len(shared_entities) < 2:  # Need some overlap
            return None
        
        # Determine relationship type based on content
        relation_type = self._infer_relation_type(stmt1, stmt2)
        
        if relation_type:
            return LogicalRelation(
                relation_id=f"rel_{stmt1.statement_id}_{stmt2.statement_id}",
                relation_type=relation_type,
                source=stmt1.statement_id,
                target=stmt2.statement_id,
                strength=len(shared_entities) / max(len(stmt1.text.split()), len(stmt2.text.split())),
                evidence=[stmt1.text, stmt2.text],
                logical_operator=None
            )
        
        return None
    
    def _infer_relation_type(self, stmt1: LogicalStatement, stmt2: LogicalStatement) -> Optional[LogicalRelationType]:
        """Infer the type of relationship between statements."""
        
        text1_lower = stmt1.text.lower()
        text2_lower = stmt2.text.lower()
        
        # Check for causal relationships
        if any(word in text1_lower for word in ["because", "causes", "results in"]):
            return LogicalRelationType.CAUSE_EFFECT
        
        # Check for conditional relationships
        if any(word in text1_lower for word in ["if", "when", "provided"]):
            return LogicalRelationType.CONDITIONAL
        
        # Check for sequential relationships
        if any(word in text1_lower for word in ["before", "after", "then", "next"]):
            return LogicalRelationType.SEQUENCE
        
        # Check for dependency relationships
        if any(word in text1_lower for word in ["requires", "depends", "needs"]):
            return LogicalRelationType.DEPENDENCY
        
        return None
    
    def _infer_logical_operator(self, text: str) -> Optional[LogicalOperator]:
        """Infer logical operator from text."""
        
        text_lower = text.lower()
        
        for connective, operator in self.logical_connectives.items():
            if connective in text_lower:
                return operator
        
        return None
    
    def _build_reasoning_chain(self, statements: List[LogicalStatement], 
                             relations: List[LogicalRelation], 
                             requirements: List[Requirement]) -> List[Dict[str, Any]]:
        """Build reasoning chain from statements and relations."""
        
        reasoning_chain = []
        
        # Create reasoning steps based on relations
        for relation in relations:
            if relation.relation_type == LogicalRelationType.CAUSE_EFFECT:
                reasoning_chain.append({
                    "step_type": "causal_inference",
                    "premise": relation.source,
                    "conclusion": relation.target,
                    "reasoning": f"Because {relation.source}, therefore {relation.target}",
                    "confidence": relation.strength
                })
            
            elif relation.relation_type == LogicalRelationType.CONDITIONAL:
                reasoning_chain.append({
                    "step_type": "conditional_reasoning",
                    "condition": relation.source,
                    "consequence": relation.target,
                    "reasoning": f"If {relation.source}, then {relation.target}",
                    "confidence": relation.strength
                })
            
            elif relation.relation_type == LogicalRelationType.DEPENDENCY:
                reasoning_chain.append({
                    "step_type": "dependency_analysis",
                    "dependent": relation.target,
                    "dependency": relation.source,
                    "reasoning": f"{relation.target} depends on {relation.source}",
                    "confidence": relation.strength
                })
        
        # Add requirement-based reasoning
        for requirement in requirements:
            if requirement.dependencies:
                reasoning_chain.append({
                    "step_type": "requirement_decomposition",
                    "requirement": requirement.text,
                    "dependencies": requirement.dependencies,
                    "reasoning": f"To satisfy {requirement.text}, need to address dependencies",
                    "confidence": requirement.confidence
                })
        
        return reasoning_chain
    
    def _assess_logical_consistency(self, statements: List[LogicalStatement], 
                                  relations: List[LogicalRelation]) -> float:
        """Assess logical consistency of the analysis."""
        
        consistency_score = 1.0
        
        # Check for contradictions
        contradictions = self._find_contradictions(statements)
        consistency_score -= len(contradictions) * 0.2
        
        # Check for circular dependencies
        circular_deps = self._find_circular_dependencies(relations)
        consistency_score -= len(circular_deps) * 0.1
        
        # Check for logical gaps
        gaps = self._find_logical_gaps(statements, relations)
        consistency_score -= len(gaps) * 0.05
        
        return max(0.0, consistency_score)
    
    def _find_contradictions(self, statements: List[LogicalStatement]) -> List[Tuple[str, str]]:
        """Find contradictory statements."""
        
        contradictions = []
        
        for i, stmt1 in enumerate(statements):
            for j, stmt2 in enumerate(statements):
                if i < j:  # Avoid duplicate checks
                    if self._are_contradictory(stmt1, stmt2):
                        contradictions.append((stmt1.statement_id, stmt2.statement_id))
        
        return contradictions
    
    def _are_contradictory(self, stmt1: LogicalStatement, stmt2: LogicalStatement) -> bool:
        """Check if two statements are contradictory."""
        
        # Simple contradiction detection based on negation
        text1_lower = stmt1.text.lower()
        text2_lower = stmt2.text.lower()
        
        # Check for explicit negation
        if ("not" in text1_lower and "not" not in text2_lower) or \
           ("not" in text2_lower and "not" not in text1_lower):
            # Check if they refer to the same subject
            if stmt1.subject and stmt2.subject and stmt1.subject.lower() == stmt2.subject.lower():
                return True
        
        return False
    
    def _find_circular_dependencies(self, relations: List[LogicalRelation]) -> List[List[str]]:
        """Find circular dependencies in relations."""
        
        # Build dependency graph
        graph = nx.DiGraph()
        
        for relation in relations:
            if relation.relation_type == LogicalRelationType.DEPENDENCY:
                graph.add_edge(relation.source, relation.target)
        
        # Find cycles
        try:
            cycles = list(nx.simple_cycles(graph))
            return cycles
        except:
            return []
    
    def _find_logical_gaps(self, statements: List[LogicalStatement], 
                          relations: List[LogicalRelation]) -> List[str]:
        """Find logical gaps in reasoning."""
        
        gaps = []
        
        # Check for missing premises in conditional statements
        for stmt in statements:
            if stmt.statement_type == "conditional":
                # Check if the condition has supporting evidence
                condition_supported = any(
                    relation.target == stmt.statement_id 
                    for relation in relations
                )
                
                if not condition_supported:
                    gaps.append(f"Missing support for condition in {stmt.statement_id}")
        
        return gaps
    
    def _calculate_completeness_score(self, requirements: List[Requirement], 
                                    relations: List[LogicalRelation]) -> float:
        """Calculate completeness score of the analysis."""
        
        if not requirements:
            return 0.0
        
        # Check requirement coverage
        covered_requirements = 0
        
        for requirement in requirements:
            # Check if requirement has dependencies identified
            if requirement.dependencies:
                covered_requirements += 0.5
            
            # Check if requirement has acceptance criteria
            if requirement.acceptance_criteria:
                covered_requirements += 0.3
            
            # Check if requirement has constraints
            if requirement.constraints:
                covered_requirements += 0.2
        
        return min(1.0, covered_requirements / len(requirements))
    
    def _calculate_analysis_confidence(self, statements: List[LogicalStatement],
                                     requirements: List[Requirement],
                                     relations: List[LogicalRelation],
                                     logical_consistency: float) -> float:
        """Calculate overall analysis confidence."""
        
        if not statements:
            return 0.0
        
        # Average statement confidence
        avg_statement_confidence = sum(stmt.confidence for stmt in statements) / len(statements)
        
        # Average requirement confidence
        avg_requirement_confidence = (
            sum(req.confidence for req in requirements) / len(requirements)
            if requirements else 0.0
        )
        
        # Relation strength
        avg_relation_strength = (
            sum(rel.strength for rel in relations) / len(relations)
            if relations else 0.0
        )
        
        # Weighted combination
        overall_confidence = (
            avg_statement_confidence * 0.4 +
            avg_requirement_confidence * 0.3 +
            avg_relation_strength * 0.2 +
            logical_consistency * 0.1
        )
        
        return overall_confidence


# Example usage
if __name__ == "__main__":
    # Initialize logical analysis engine
    engine = LogicalAnalysisEngine()
    
    # Test text with logical structure
    test_text = """
    The system must authenticate users before allowing access to sensitive data.
    If authentication fails, then the system should log the attempt and deny access.
    The authentication service requires a secure database connection.
    Performance should be under 500ms for login requests.
    Because security is critical, we need to implement multi-factor authentication.
    """
    
    # Perform logical analysis
    result = engine.analyze_logical_structure(test_text)
    
    print(f"Logical Analysis Results:")
    print(f"Statements: {len(result.statements)}")
    print(f"Requirements: {len(result.requirements)}")
    print(f"Relations: {len(result.relations)}")
    print(f"Reasoning steps: {len(result.reasoning_chain)}")
    print(f"Logical consistency: {result.logical_consistency:.3f}")
    print(f"Completeness: {result.completeness_score:.3f}")
    print(f"Overall confidence: {result.analysis_confidence:.3f}")
    print(f"Processing time: {result.processing_time_ms:.2f}ms")
    
    print(f"\nExtracted Requirements:")
    for req in result.requirements:
        print(f"  - {req.requirement_type.value}: {req.text}")
        print(f"    Priority: {req.priority}, Confidence: {req.confidence:.2f}")
    
    print(f"\nLogical Relations:")
    for rel in result.relations:
        print(f"  - {rel.relation_type.value}: {rel.source} -> {rel.target}")
        print(f"    Strength: {rel.strength:.2f}")
