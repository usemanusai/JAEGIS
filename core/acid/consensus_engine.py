#!/usr/bin/env python3
"""
A.C.I.D. Consensus Engine
Autonomous Cognitive Intelligence Directorate - Consensus Validation

This module implements the Consensus Engine for A.C.I.D., providing
cross-agent validation, voting systems, and quality assurance protocols
for the JAEGIS A.E.G.I.S. Protocol Suite.

Consensus Features:
- Cross-agent validation mechanisms
- Multi-tier voting systems
- Quality assurance protocols
- Confidence scoring algorithms
- Dispute resolution frameworks
"""

import asyncio
import json
import logging
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsensusType(Enum):
    """Types of consensus mechanisms"""
    SIMPLE_MAJORITY = "simple_majority"
    QUALIFIED_MAJORITY = "qualified_majority"
    UNANIMOUS = "unanimous"
    WEIGHTED_VOTING = "weighted_voting"
    BYZANTINE_FAULT_TOLERANT = "byzantine_fault_tolerant"

class ValidationLevel(Enum):
    """Validation strictness levels"""
    BASIC = 1
    STANDARD = 2
    STRICT = 3
    CRITICAL = 4
    MAXIMUM = 5

class VoteType(Enum):
    """Types of votes"""
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"
    CONDITIONAL = "conditional"

class DisputeStatus(Enum):
    """Dispute resolution status"""
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

@dataclass
class Vote:
    """Individual vote in consensus process"""
    voter_id: str
    vote_type: VoteType
    confidence: float  # 0.0 to 1.0
    reasoning: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConsensusProposal:
    """Proposal for consensus validation"""
    id: str
    title: str
    description: str
    proposer_id: str
    proposal_data: Dict[str, Any]
    consensus_type: ConsensusType
    validation_level: ValidationLevel
    required_votes: int
    votes: List[Vote] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Validator:
    """Agent validator in consensus system"""
    id: str
    name: str
    expertise_areas: List[str]
    trust_score: float = 1.0
    validation_history: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    is_active: bool = True
    last_active: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Dispute:
    """Dispute in consensus process"""
    id: str
    proposal_id: str
    disputer_id: str
    dispute_reason: str
    evidence: Dict[str, Any]
    status: DisputeStatus = DisputeStatus.PENDING
    resolution: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConsensusResult:
    """Result of consensus process"""
    proposal_id: str
    decision: str  # "approved", "rejected", "no_consensus"
    confidence_score: float
    vote_summary: Dict[str, int]
    participating_validators: List[str]
    consensus_strength: float
    quality_score: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class ConsensusEngine:
    """
    A.C.I.D. Consensus Engine
    
    Manages cross-agent validation, voting systems, and quality assurance
    protocols for ensuring high-quality decision making in the A.E.G.I.S. ecosystem.
    """
    
    def __init__(self):
        self.validators: Dict[str, Validator] = {}
        self.proposals: Dict[str, ConsensusProposal] = {}
        self.disputes: Dict[str, Dispute] = {}
        self.consensus_history: List[ConsensusResult] = []
        self.quality_thresholds = {
            ValidationLevel.BASIC: 0.6,
            ValidationLevel.STANDARD: 0.7,
            ValidationLevel.STRICT: 0.8,
            ValidationLevel.CRITICAL: 0.9,
            ValidationLevel.MAXIMUM: 0.95
        }
        self.consensus_algorithms = {
            ConsensusType.SIMPLE_MAJORITY: self._simple_majority_consensus,
            ConsensusType.QUALIFIED_MAJORITY: self._qualified_majority_consensus,
            ConsensusType.UNANIMOUS: self._unanimous_consensus,
            ConsensusType.WEIGHTED_VOTING: self._weighted_voting_consensus,
            ConsensusType.BYZANTINE_FAULT_TOLERANT: self._byzantine_fault_tolerant_consensus
        }
        
        logger.info("A.C.I.D. Consensus Engine initialized")
    
    async def register_validator(
        self,
        name: str,
        expertise_areas: List[str],
        trust_score: float = 1.0
    ) -> str:
        """
        Register a new validator
        
        Args:
            name: Validator name
            expertise_areas: Areas of expertise
            trust_score: Initial trust score
            
        Returns:
            Validator ID
        """
        validator_id = str(uuid.uuid4())
        
        validator = Validator(
            id=validator_id,
            name=name,
            expertise_areas=expertise_areas,
            trust_score=trust_score,
            performance_metrics={
                "accuracy": 1.0,
                "consistency": 1.0,
                "timeliness": 1.0,
                "participation_rate": 1.0
            }
        )
        
        self.validators[validator_id] = validator
        
        logger.info(f"Registered validator '{name}' with expertise in {expertise_areas}")
        return validator_id
    
    async def submit_proposal(
        self,
        title: str,
        description: str,
        proposer_id: str,
        proposal_data: Dict[str, Any],
        consensus_type: ConsensusType = ConsensusType.SIMPLE_MAJORITY,
        validation_level: ValidationLevel = ValidationLevel.STANDARD,
        deadline: Optional[datetime] = None
    ) -> str:
        """
        Submit a proposal for consensus validation
        
        Args:
            title: Proposal title
            description: Proposal description
            proposer_id: ID of proposing agent
            proposal_data: Proposal data to validate
            consensus_type: Type of consensus mechanism
            validation_level: Validation strictness level
            deadline: Voting deadline
            
        Returns:
            Proposal ID
        """
        proposal_id = str(uuid.uuid4())
        
        # Calculate required votes based on consensus type and validation level
        required_votes = self._calculate_required_votes(consensus_type, validation_level)
        
        proposal = ConsensusProposal(
            id=proposal_id,
            title=title,
            description=description,
            proposer_id=proposer_id,
            proposal_data=proposal_data,
            consensus_type=consensus_type,
            validation_level=validation_level,
            required_votes=required_votes,
            deadline=deadline
        )
        
        self.proposals[proposal_id] = proposal
        
        # Automatically select suitable validators
        await self._select_validators_for_proposal(proposal_id)
        
        logger.info(f"Submitted proposal '{title}' for consensus validation")
        return proposal_id
    
    def _calculate_required_votes(
        self,
        consensus_type: ConsensusType,
        validation_level: ValidationLevel
    ) -> int:
        """Calculate required number of votes"""
        base_votes = max(3, len(self.validators) // 3)  # Minimum 3 validators
        
        # Adjust based on consensus type
        if consensus_type == ConsensusType.UNANIMOUS:
            return len(self.validators)
        elif consensus_type == ConsensusType.QUALIFIED_MAJORITY:
            return max(base_votes, int(len(self.validators) * 0.67))
        elif consensus_type == ConsensusType.BYZANTINE_FAULT_TOLERANT:
            return max(base_votes, int(len(self.validators) * 0.67) + 1)
        else:
            return base_votes
    
    async def _select_validators_for_proposal(self, proposal_id: str):
        """Select suitable validators for a proposal"""
        proposal = self.proposals[proposal_id]
        
        # Find validators with relevant expertise
        suitable_validators = []
        
        for validator in self.validators.values():
            if not validator.is_active:
                continue
            
            # Check expertise match
            expertise_match = self._calculate_expertise_match(
                validator.expertise_areas,
                proposal.proposal_data
            )
            
            if expertise_match > 0.3:  # Minimum expertise threshold
                suitability_score = (
                    validator.trust_score * 0.4 +
                    expertise_match * 0.4 +
                    validator.performance_metrics.get("accuracy", 0.5) * 0.2
                )
                suitable_validators.append((validator, suitability_score))
        
        # Sort by suitability and select top validators
        suitable_validators.sort(key=lambda x: x[1], reverse=True)
        
        # Select validators up to required votes
        selected_count = min(proposal.required_votes, len(suitable_validators))
        
        for i in range(selected_count):
            validator = suitable_validators[i][0]
            await self._invite_validator_to_proposal(validator.id, proposal_id)
    
    def _calculate_expertise_match(
        self,
        validator_expertise: List[str],
        proposal_data: Dict[str, Any]
    ) -> float:
        """Calculate how well validator expertise matches proposal"""
        # Extract keywords from proposal data
        proposal_text = json.dumps(proposal_data).lower()
        
        matches = 0
        for expertise in validator_expertise:
            if expertise.lower() in proposal_text:
                matches += 1
        
        return matches / len(validator_expertise) if validator_expertise else 0.0
    
    async def _invite_validator_to_proposal(self, validator_id: str, proposal_id: str):
        """Invite a validator to participate in proposal validation"""
        validator = self.validators.get(validator_id)
        proposal = self.proposals.get(proposal_id)
        
        if validator and proposal:
            # Add to validator's validation history
            validator.validation_history.append(proposal_id)
            
            logger.info(f"Invited validator '{validator.name}' to validate proposal '{proposal.title}'")
    
    async def submit_vote(
        self,
        proposal_id: str,
        voter_id: str,
        vote_type: VoteType,
        confidence: float,
        reasoning: str,
        evidence: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Submit a vote for a proposal
        
        Args:
            proposal_id: Proposal ID
            voter_id: Validator ID
            vote_type: Type of vote
            confidence: Confidence in vote (0.0 to 1.0)
            reasoning: Reasoning for vote
            evidence: Supporting evidence
            
        Returns:
            Success status
        """
        proposal = self.proposals.get(proposal_id)
        validator = self.validators.get(voter_id)
        
        if not proposal or not validator:
            return False
        
        if proposal.status != "pending":
            logger.warning(f"Cannot vote on proposal {proposal_id} with status {proposal.status}")
            return False
        
        # Check if validator already voted
        existing_vote = next((v for v in proposal.votes if v.voter_id == voter_id), None)
        if existing_vote:
            logger.warning(f"Validator {voter_id} already voted on proposal {proposal_id}")
            return False
        
        # Calculate vote weight based on validator trust and expertise
        vote_weight = self._calculate_vote_weight(validator, proposal)
        
        vote = Vote(
            voter_id=voter_id,
            vote_type=vote_type,
            confidence=confidence,
            reasoning=reasoning,
            evidence=evidence or {},
            weight=vote_weight
        )
        
        proposal.votes.append(vote)
        
        # Update validator metrics
        await self._update_validator_metrics(validator, vote)
        
        # Check if consensus is reached
        await self._check_consensus(proposal_id)
        
        logger.info(f"Vote submitted by '{validator.name}' for proposal '{proposal.title}'")
        return True
    
    def _calculate_vote_weight(self, validator: Validator, proposal: ConsensusProposal) -> float:
        """Calculate weight of a validator's vote"""
        base_weight = validator.trust_score
        
        # Expertise bonus
        expertise_match = self._calculate_expertise_match(
            validator.expertise_areas,
            proposal.proposal_data
        )
        expertise_bonus = expertise_match * 0.5
        
        # Performance bonus
        performance_bonus = validator.performance_metrics.get("accuracy", 0.5) * 0.3
        
        total_weight = base_weight + expertise_bonus + performance_bonus
        
        # Normalize to reasonable range
        return min(2.0, max(0.1, total_weight))
    
    async def _update_validator_metrics(self, validator: Validator, vote: Vote):
        """Update validator performance metrics"""
        # Update participation rate
        total_invitations = len(validator.validation_history)
        if total_invitations > 0:
            validator.performance_metrics["participation_rate"] = min(1.0, 
                validator.performance_metrics.get("participation_rate", 1.0) * 1.01)
        
        # Update timeliness (simplified - based on vote confidence)
        validator.performance_metrics["timeliness"] = (
            validator.performance_metrics.get("timeliness", 1.0) * 0.9 +
            vote.confidence * 0.1
        )
        
        validator.last_active = datetime.now()
    
    async def _check_consensus(self, proposal_id: str):
        """Check if consensus has been reached for a proposal"""
        proposal = self.proposals[proposal_id]
        
        if len(proposal.votes) < proposal.required_votes:
            return  # Not enough votes yet
        
        # Apply consensus algorithm
        consensus_algorithm = self.consensus_algorithms[proposal.consensus_type]
        result = await consensus_algorithm(proposal)
        
        if result:
            proposal.result = result
            proposal.status = "completed"
            
            # Add to consensus history
            consensus_result = ConsensusResult(
                proposal_id=proposal_id,
                decision=result["decision"],
                confidence_score=result["confidence_score"],
                vote_summary=result["vote_summary"],
                participating_validators=result["participating_validators"],
                consensus_strength=result["consensus_strength"],
                quality_score=result["quality_score"]
            )
            
            self.consensus_history.append(consensus_result)
            
            logger.info(f"Consensus reached for proposal '{proposal.title}': {result['decision']}")
    
    async def _simple_majority_consensus(self, proposal: ConsensusProposal) -> Optional[Dict[str, Any]]:
        """Simple majority consensus algorithm"""
        approve_votes = [v for v in proposal.votes if v.vote_type == VoteType.APPROVE]
        reject_votes = [v for v in proposal.votes if v.vote_type == VoteType.REJECT]
        
        # Weight votes
        approve_weight = sum(v.weight * v.confidence for v in approve_votes)
        reject_weight = sum(v.weight * v.confidence for v in reject_votes)
        
        total_weight = approve_weight + reject_weight
        
        if total_weight == 0:
            return None
        
        approve_ratio = approve_weight / total_weight
        
        decision = "approved" if approve_ratio > 0.5 else "rejected"
        confidence_score = max(approve_ratio, 1 - approve_ratio)
        
        # Check quality threshold
        quality_threshold = self.quality_thresholds[proposal.validation_level]
        if confidence_score < quality_threshold:
            decision = "no_consensus"
        
        return {
            "decision": decision,
            "confidence_score": confidence_score,
            "vote_summary": {
                "approve": len(approve_votes),
                "reject": len(reject_votes),
                "abstain": len([v for v in proposal.votes if v.vote_type == VoteType.ABSTAIN])
            },
            "participating_validators": [v.voter_id for v in proposal.votes],
            "consensus_strength": confidence_score,
            "quality_score": confidence_score
        }
    
    async def _qualified_majority_consensus(self, proposal: ConsensusProposal) -> Optional[Dict[str, Any]]:
        """Qualified majority consensus algorithm (requires 2/3 majority)"""
        approve_votes = [v for v in proposal.votes if v.vote_type == VoteType.APPROVE]
        total_votes = len(proposal.votes)
        
        if total_votes == 0:
            return None
        
        # Weight votes
        approve_weight = sum(v.weight * v.confidence for v in approve_votes)
        total_weight = sum(v.weight * v.confidence for v in proposal.votes)
        
        approve_ratio = approve_weight / total_weight if total_weight > 0 else 0
        
        # Require 2/3 majority
        decision = "approved" if approve_ratio >= 0.67 else "rejected"
        confidence_score = approve_ratio if decision == "approved" else (1 - approve_ratio)
        
        # Check quality threshold
        quality_threshold = self.quality_thresholds[proposal.validation_level]
        if confidence_score < quality_threshold:
            decision = "no_consensus"
        
        return {
            "decision": decision,
            "confidence_score": confidence_score,
            "vote_summary": {
                "approve": len(approve_votes),
                "reject": len([v for v in proposal.votes if v.vote_type == VoteType.REJECT]),
                "abstain": len([v for v in proposal.votes if v.vote_type == VoteType.ABSTAIN])
            },
            "participating_validators": [v.voter_id for v in proposal.votes],
            "consensus_strength": approve_ratio,
            "quality_score": confidence_score
        }
    
    async def _unanimous_consensus(self, proposal: ConsensusProposal) -> Optional[Dict[str, Any]]:
        """Unanimous consensus algorithm"""
        non_abstain_votes = [v for v in proposal.votes if v.vote_type != VoteType.ABSTAIN]
        
        if not non_abstain_votes:
            return None
        
        # Check if all non-abstain votes are the same
        first_vote_type = non_abstain_votes[0].vote_type
        unanimous = all(v.vote_type == first_vote_type for v in non_abstain_votes)
        
        if unanimous:
            decision = "approved" if first_vote_type == VoteType.APPROVE else "rejected"
            
            # Calculate confidence as average of all votes
            avg_confidence = statistics.mean(v.confidence for v in non_abstain_votes)
            
            return {
                "decision": decision,
                "confidence_score": avg_confidence,
                "vote_summary": {
                    "approve": len([v for v in proposal.votes if v.vote_type == VoteType.APPROVE]),
                    "reject": len([v for v in proposal.votes if v.vote_type == VoteType.REJECT]),
                    "abstain": len([v for v in proposal.votes if v.vote_type == VoteType.ABSTAIN])
                },
                "participating_validators": [v.voter_id for v in proposal.votes],
                "consensus_strength": 1.0,  # Perfect consensus
                "quality_score": avg_confidence
            }
        else:
            return {
                "decision": "no_consensus",
                "confidence_score": 0.0,
                "vote_summary": {
                    "approve": len([v for v in proposal.votes if v.vote_type == VoteType.APPROVE]),
                    "reject": len([v for v in proposal.votes if v.vote_type == VoteType.REJECT]),
                    "abstain": len([v for v in proposal.votes if v.vote_type == VoteType.ABSTAIN])
                },
                "participating_validators": [v.voter_id for v in proposal.votes],
                "consensus_strength": 0.0,
                "quality_score": 0.0
            }
    
    async def _weighted_voting_consensus(self, proposal: ConsensusProposal) -> Optional[Dict[str, Any]]:
        """Weighted voting consensus algorithm"""
        approve_weight = sum(
            v.weight * v.confidence 
            for v in proposal.votes 
            if v.vote_type == VoteType.APPROVE
        )
        
        reject_weight = sum(
            v.weight * v.confidence 
            for v in proposal.votes 
            if v.vote_type == VoteType.REJECT
        )
        
        total_weight = approve_weight + reject_weight
        
        if total_weight == 0:
            return None
        
        approve_ratio = approve_weight / total_weight
        
        # Use weighted threshold
        threshold = 0.6  # Higher threshold for weighted voting
        decision = "approved" if approve_ratio > threshold else "rejected"
        confidence_score = max(approve_ratio, 1 - approve_ratio)
        
        # Check quality threshold
        quality_threshold = self.quality_thresholds[proposal.validation_level]
        if confidence_score < quality_threshold:
            decision = "no_consensus"
        
        return {
            "decision": decision,
            "confidence_score": confidence_score,
            "vote_summary": {
                "approve": len([v for v in proposal.votes if v.vote_type == VoteType.APPROVE]),
                "reject": len([v for v in proposal.votes if v.vote_type == VoteType.REJECT]),
                "abstain": len([v for v in proposal.votes if v.vote_type == VoteType.ABSTAIN])
            },
            "participating_validators": [v.voter_id for v in proposal.votes],
            "consensus_strength": approve_ratio,
            "quality_score": confidence_score
        }
    
    async def _byzantine_fault_tolerant_consensus(self, proposal: ConsensusProposal) -> Optional[Dict[str, Any]]:
        """Byzantine fault tolerant consensus algorithm"""
        # Simplified BFT - requires 2/3 + 1 honest validators
        total_validators = len(proposal.votes)
        required_honest = (total_validators * 2) // 3 + 1
        
        # Identify potentially malicious votes (very low confidence or inconsistent)
        honest_votes = []
        for vote in proposal.votes:
            if vote.confidence >= 0.5:  # Minimum confidence threshold
                honest_votes.append(vote)
        
        if len(honest_votes) < required_honest:
            return {
                "decision": "no_consensus",
                "confidence_score": 0.0,
                "vote_summary": {
                    "approve": len([v for v in proposal.votes if v.vote_type == VoteType.APPROVE]),
                    "reject": len([v for v in proposal.votes if v.vote_type == VoteType.REJECT]),
                    "abstain": len([v for v in proposal.votes if v.vote_type == VoteType.ABSTAIN])
                },
                "participating_validators": [v.voter_id for v in proposal.votes],
                "consensus_strength": 0.0,
                "quality_score": 0.0
            }
        
        # Apply majority consensus on honest votes
        approve_votes = [v for v in honest_votes if v.vote_type == VoteType.APPROVE]
        approve_ratio = len(approve_votes) / len(honest_votes)
        
        decision = "approved" if approve_ratio > 0.5 else "rejected"
        confidence_score = max(approve_ratio, 1 - approve_ratio)
        
        return {
            "decision": decision,
            "confidence_score": confidence_score,
            "vote_summary": {
                "approve": len([v for v in proposal.votes if v.vote_type == VoteType.APPROVE]),
                "reject": len([v for v in proposal.votes if v.vote_type == VoteType.REJECT]),
                "abstain": len([v for v in proposal.votes if v.vote_type == VoteType.ABSTAIN])
            },
            "participating_validators": [v.voter_id for v in proposal.votes],
            "consensus_strength": approve_ratio,
            "quality_score": confidence_score
        }
    
    async def submit_dispute(
        self,
        proposal_id: str,
        disputer_id: str,
        dispute_reason: str,
        evidence: Dict[str, Any]
    ) -> str:
        """
        Submit a dispute for a consensus decision
        
        Args:
            proposal_id: Proposal ID
            disputer_id: ID of disputing agent
            dispute_reason: Reason for dispute
            evidence: Supporting evidence
            
        Returns:
            Dispute ID
        """
        dispute_id = str(uuid.uuid4())
        
        dispute = Dispute(
            id=dispute_id,
            proposal_id=proposal_id,
            disputer_id=disputer_id,
            dispute_reason=dispute_reason,
            evidence=evidence
        )
        
        self.disputes[dispute_id] = dispute
        
        # Mark proposal for review
        proposal = self.proposals.get(proposal_id)
        if proposal:
            proposal.status = "disputed"
        
        logger.info(f"Dispute submitted for proposal {proposal_id}")
        return dispute_id
    
    async def resolve_dispute(
        self,
        dispute_id: str,
        resolution: str,
        resolver_id: str
    ) -> bool:
        """
        Resolve a dispute
        
        Args:
            dispute_id: Dispute ID
            resolution: Resolution decision
            resolver_id: ID of resolving authority
            
        Returns:
            Success status
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            return False
        
        dispute.status = DisputeStatus.RESOLVED
        dispute.resolution = resolution
        dispute.resolved_at = datetime.now()
        
        # Update proposal status
        proposal = self.proposals.get(dispute.proposal_id)
        if proposal:
            if "upheld" in resolution.lower():
                proposal.status = "completed"
            else:
                proposal.status = "pending"  # Reopen for voting
        
        logger.info(f"Dispute {dispute_id} resolved: {resolution}")
        return True
    
    def get_consensus_metrics(self) -> Dict[str, Any]:
        """Get consensus system metrics"""
        total_proposals = len(self.proposals)
        completed_proposals = len([p for p in self.proposals.values() if p.status == "completed"])
        disputed_proposals = len([p for p in self.proposals.values() if p.status == "disputed"])
        
        # Calculate average confidence
        completed_results = [r for r in self.consensus_history if r.decision != "no_consensus"]
        avg_confidence = statistics.mean([r.confidence_score for r in completed_results]) if completed_results else 0.0
        
        # Calculate validator performance
        active_validators = len([v for v in self.validators.values() if v.is_active])
        avg_trust_score = statistics.mean([v.trust_score for v in self.validators.values()]) if self.validators else 0.0
        
        return {
            "total_proposals": total_proposals,
            "completed_proposals": completed_proposals,
            "disputed_proposals": disputed_proposals,
            "pending_proposals": total_proposals - completed_proposals - disputed_proposals,
            "completion_rate": completed_proposals / total_proposals if total_proposals > 0 else 0.0,
            "dispute_rate": disputed_proposals / total_proposals if total_proposals > 0 else 0.0,
            "average_confidence": avg_confidence,
            "total_validators": len(self.validators),
            "active_validators": active_validators,
            "average_trust_score": avg_trust_score,
            "total_disputes": len(self.disputes),
            "resolved_disputes": len([d for d in self.disputes.values() if d.status == DisputeStatus.RESOLVED]),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_proposal_status(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return None
        
        return {
            "id": proposal.id,
            "title": proposal.title,
            "status": proposal.status,
            "consensus_type": proposal.consensus_type.value,
            "validation_level": proposal.validation_level.value,
            "required_votes": proposal.required_votes,
            "current_votes": len(proposal.votes),
            "votes": [
                {
                    "voter_id": vote.voter_id,
                    "vote_type": vote.vote_type.value,
                    "confidence": vote.confidence,
                    "weight": vote.weight,
                    "timestamp": vote.timestamp.isoformat()
                }
                for vote in proposal.votes
            ],
            "result": proposal.result,
            "created_at": proposal.created_at.isoformat(),
            "deadline": proposal.deadline.isoformat() if proposal.deadline else None
        }
    
    async def update_validator_trust(self, validator_id: str, trust_adjustment: float):
        """Update validator trust score"""
        validator = self.validators.get(validator_id)
        if validator:
            validator.trust_score = max(0.0, min(2.0, validator.trust_score + trust_adjustment))
            logger.info(f"Updated trust score for validator {validator_id}: {validator.trust_score}")

# Example usage and testing
async def main():
    """Example usage of the Consensus Engine"""
    engine = ConsensusEngine()
    
    # Register validators
    validators = [
        ("Alice", ["security", "cryptography"], 1.0),
        ("Bob", ["performance", "optimization"], 0.9),
        ("Charlie", ["ui_design", "user_experience"], 1.1),
        ("Diana", ["data_analysis", "machine_learning"], 1.2),
        ("Eve", ["testing", "quality_assurance"], 0.8)
    ]
    
    validator_ids = []
    for name, expertise, trust in validators:
        validator_id = await engine.register_validator(name, expertise, trust)
        validator_ids.append(validator_id)
    
    # Submit a proposal
    proposal_data = {
        "feature": "new_authentication_system",
        "security_level": "high",
        "implementation": "oauth2_with_mfa",
        "estimated_effort": "2_weeks"
    }
    
    proposal_id = await engine.submit_proposal(
        title="Implement New Authentication System",
        description="Proposal to implement OAuth2 with MFA for enhanced security",
        proposer_id="system",
        proposal_data=proposal_data,
        consensus_type=ConsensusType.QUALIFIED_MAJORITY,
        validation_level=ValidationLevel.STRICT
    )
    
    # Submit votes
    votes = [
        (validator_ids[0], VoteType.APPROVE, 0.9, "Strong security implementation"),
        (validator_ids[1], VoteType.APPROVE, 0.7, "Good performance characteristics"),
        (validator_ids[2], VoteType.REJECT, 0.8, "UX concerns with MFA"),
        (validator_ids[3], VoteType.APPROVE, 0.85, "Data protection benefits"),
        (validator_ids[4], VoteType.APPROVE, 0.75, "Testable implementation")
    ]
    
    for validator_id, vote_type, confidence, reasoning in votes:
        await engine.submit_vote(
            proposal_id=proposal_id,
            voter_id=validator_id,
            vote_type=vote_type,
            confidence=confidence,
            reasoning=reasoning
        )
    
    # Get proposal status
    status = engine.get_proposal_status(proposal_id)
    print(f"Proposal Status: {json.dumps(status, indent=2)}")
    
    # Get consensus metrics
    metrics = engine.get_consensus_metrics()
    print(f"Consensus Metrics: {json.dumps(metrics, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())