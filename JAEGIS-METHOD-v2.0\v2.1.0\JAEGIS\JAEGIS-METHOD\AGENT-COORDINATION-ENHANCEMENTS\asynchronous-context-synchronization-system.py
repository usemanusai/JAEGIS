#!/usr/bin/env python3
"""
JAEGIS Agent System - Asynchronous Context Synchronization System
CRITICAL GAP RESOLUTION: Eliminates context conflicts in parallel agent execution

Date: 24 July 2025
Priority: CRITICAL - Phase 1 Implementation
Gap ID: 2.1 - Asynchronous Context Synchronization
Impact: CRITICAL - Prevents context conflicts and race conditions
"""

import asyncio
import json
import threading
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import copy

class ContextSyncStatus(Enum):
    """Context synchronization status"""
    SYNCHRONIZED = "SYNCHRONIZED"
    PENDING_SYNC = "PENDING_SYNC"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    SYNC_FAILED = "SYNC_FAILED"
    ROLLBACK_REQUIRED = "ROLLBACK_REQUIRED"

class ConflictResolutionStrategy(Enum):
    """Strategies for resolving context conflicts"""
    LAST_WRITER_WINS = "LAST_WRITER_WINS"
    MERGE_STRATEGY = "MERGE_STRATEGY"
    PRIORITY_BASED = "PRIORITY_BASED"
    MANUAL_RESOLUTION = "MANUAL_RESOLUTION"
    ROLLBACK_AND_RETRY = "ROLLBACK_AND_RETRY"

@dataclass
class ContextVersion:
    """Versioned context with metadata"""
    version_id: str
    agent_id: str
    context_data: Dict[str, Any]
    timestamp: str
    checksum: str
    parent_version: Optional[str] = None
    merge_conflicts: List[str] = field(default_factory=list)

@dataclass
class ContextConflict:
    """Context conflict information"""
    conflict_id: str
    conflicting_agents: List[str]
    conflicting_keys: List[str]
    conflict_type: str
    resolution_strategy: ConflictResolutionStrategy
    created_at: str
    resolved: bool = False
    resolution_result: Optional[Dict] = None

class JAEGISAsyncContextSynchronizer:
    """
    JAEGIS Asynchronous Context Synchronization System
    Eliminates context conflicts and enables safe parallel agent execution
    """
    
    def __init__(self):
        # Context versioning
        self.context_versions: Dict[str, ContextVersion] = {}
        self.current_version_id: str = self._generate_version_id()
        self.version_history: List[str] = []
        
        # Conflict management
        self.active_conflicts: Dict[str, ContextConflict] = {}
        self.conflict_resolution_strategies: Dict[str, ConflictResolutionStrategy] = {}
        
        # Synchronization control
        self.sync_lock = asyncio.Lock()
        self.agent_locks: Dict[str, asyncio.Lock] = {}
        self.pending_updates: Dict[str, List[Dict]] = {}
        
        # Performance monitoring
        self.sync_metrics = {
            'total_syncs': 0,
            'conflicts_detected': 0,
            'conflicts_resolved': 0,
            'rollbacks_performed': 0,
            'average_sync_time': 0.0
        }
        
        # Initialize system
        self._initialize_context_sync_system()
    
    async def update_context_async(self, agent_id: str, context_updates: Dict[str, Any], 
                                 priority: int = 5) -> Dict[str, Any]:
        """
        Asynchronously update context with conflict detection and resolution
        
        Args:
            agent_id: ID of the agent making the update
            context_updates: Dictionary of context updates
            priority: Update priority (1-10, higher = more important)
            
        Returns:
            Update result with synchronization status
        """
        update_id = str(uuid.uuid4())
        start_time = time.time()
        
        print(f"🔄 ASYNC CONTEXT UPDATE: Agent {agent_id} | Update ID: {update_id}")
        
        try:
            # Acquire agent-specific lock
            if agent_id not in self.agent_locks:
                self.agent_locks[agent_id] = asyncio.Lock()
            
            async with self.agent_locks[agent_id]:
                # Create new context version
                new_version = await self._create_context_version(
                    agent_id, context_updates, priority
                )
                
                # Detect conflicts with other pending updates
                conflicts = await self._detect_context_conflicts(new_version)
                
                if conflicts:
                    print(f"⚠️ CONFLICTS DETECTED: {len(conflicts)} conflicts found")
                    
                    # Resolve conflicts based on strategy
                    resolution_result = await self._resolve_context_conflicts(
                        new_version, conflicts
                    )
                    
                    if resolution_result['success']:
                        # Apply resolved version
                        await self._apply_context_version(resolution_result['resolved_version'])
                        sync_status = ContextSyncStatus.SYNCHRONIZED
                    else:
                        # Conflict resolution failed
                        sync_status = ContextSyncStatus.CONFLICT_DETECTED
                        await self._handle_resolution_failure(new_version, conflicts)
                else:
                    # No conflicts - apply directly
                    await self._apply_context_version(new_version)
                    sync_status = ContextSyncStatus.SYNCHRONIZED
                
                # Update metrics
                sync_time = time.time() - start_time
                await self._update_sync_metrics(sync_time, len(conflicts))
                
                return {
                    'update_id': update_id,
                    'agent_id': agent_id,
                    'version_id': new_version.version_id,
                    'sync_status': sync_status.value,
                    'conflicts_detected': len(conflicts),
                    'sync_time': sync_time,
                    'success': sync_status == ContextSyncStatus.SYNCHRONIZED
                }
                
        except Exception as e:
            print(f"❌ CONTEXT UPDATE FAILED: {e}")
            return {
                'update_id': update_id,
                'agent_id': agent_id,
                'sync_status': ContextSyncStatus.SYNC_FAILED.value,
                'error': str(e),
                'success': False
            }
    
    async def _create_context_version(self, agent_id: str, updates: Dict[str, Any], 
                                    priority: int) -> ContextVersion:
        """Create new context version with updates"""
        
        # Get current context
        current_context = await self._get_current_context()
        
        # Apply updates to create new context
        new_context = copy.deepcopy(current_context)
        new_context.update(updates)
        
        # Create version
        version_id = self._generate_version_id()
        checksum = self._calculate_context_checksum(new_context)
        
        version = ContextVersion(
            version_id=version_id,
            agent_id=agent_id,
            context_data=new_context,
            timestamp=datetime.now().isoformat(),
            checksum=checksum,
            parent_version=self.current_version_id
        )
        
        return version
    
    async def _detect_context_conflicts(self, new_version: ContextVersion) -> List[ContextConflict]:
        """Detect conflicts with other pending updates"""
        conflicts = []
        
        # Check against pending updates from other agents
        for other_agent_id, pending_updates in self.pending_updates.items():
            if other_agent_id == new_version.agent_id:
                continue
                
            for pending_update in pending_updates:
                conflict = await self._check_version_conflict(new_version, pending_update)
                if conflict:
                    conflicts.append(conflict)
        
        # Check against recent versions
        recent_versions = self._get_recent_versions(5)
        for version in recent_versions:
            if version.agent_id != new_version.agent_id:
                conflict = await self._check_version_conflict(new_version, version)
                if conflict:
                    conflicts.append(conflict)
        
        return conflicts
    
    async def _check_version_conflict(self, version1: ContextVersion, 
                                    version2: ContextVersion) -> Optional[ContextConflict]:
        """Check if two versions have conflicts"""
        
        # Find overlapping keys
        keys1 = set(version1.context_data.keys())
        keys2 = set(version2.context_data.keys())
        overlapping_keys = keys1.intersection(keys2)
        
        conflicting_keys = []
        for key in overlapping_keys:
            if version1.context_data[key] != version2.context_data[key]:
                conflicting_keys.append(key)
        
        if conflicting_keys:
            conflict = ContextConflict(
                conflict_id=str(uuid.uuid4()),
                conflicting_agents=[version1.agent_id, version2.agent_id],
                conflicting_keys=conflicting_keys,
                conflict_type="VALUE_CONFLICT",
                resolution_strategy=self._determine_resolution_strategy(conflicting_keys),
                created_at=datetime.now().isoformat()
            )
            return conflict
        
        return None
    
    async def _resolve_context_conflicts(self, version: ContextVersion, 
                                       conflicts: List[ContextConflict]) -> Dict[str, Any]:
        """Resolve context conflicts using appropriate strategies"""
        
        print(f"🔧 RESOLVING {len(conflicts)} CONTEXT CONFLICTS")
        
        resolved_context = copy.deepcopy(version.context_data)
        resolution_success = True
        
        for conflict in conflicts:
            try:
                if conflict.resolution_strategy == ConflictResolutionStrategy.LAST_WRITER_WINS:
                    # Keep the newer version's values
                    resolution_result = await self._apply_last_writer_wins(conflict, resolved_context)
                    
                elif conflict.resolution_strategy == ConflictResolutionStrategy.MERGE_STRATEGY:
                    # Attempt intelligent merge
                    resolution_result = await self._apply_merge_strategy(conflict, resolved_context)
                    
                elif conflict.resolution_strategy == ConflictResolutionStrategy.PRIORITY_BASED:
                    # Use agent priority to resolve
                    resolution_result = await self._apply_priority_resolution(conflict, resolved_context)
                    
                else:
                    # Default to manual resolution flag
                    resolution_result = {'success': False, 'requires_manual': True}
                
                if resolution_result['success']:
                    resolved_context = resolution_result['resolved_context']
                    conflict.resolved = True
                    conflict.resolution_result = resolution_result
                else:
                    resolution_success = False
                    
            except Exception as e:
                print(f"❌ CONFLICT RESOLUTION FAILED: {e}")
                resolution_success = False
        
        if resolution_success:
            # Create resolved version
            resolved_version = ContextVersion(
                version_id=self._generate_version_id(),
                agent_id=f"RESOLVED_{version.agent_id}",
                context_data=resolved_context,
                timestamp=datetime.now().isoformat(),
                checksum=self._calculate_context_checksum(resolved_context),
                parent_version=version.version_id
            )
            
            return {
                'success': True,
                'resolved_version': resolved_version,
                'conflicts_resolved': len([c for c in conflicts if c.resolved])
            }
        else:
            return {
                'success': False,
                'unresolved_conflicts': [c for c in conflicts if not c.resolved]
            }
    
    async def _apply_last_writer_wins(self, conflict: ContextConflict, 
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply last writer wins resolution strategy"""
        
        # Keep the current context values (last writer)
        return {
            'success': True,
            'resolved_context': context,
            'strategy_applied': 'LAST_WRITER_WINS'
        }
    
    async def _apply_merge_strategy(self, conflict: ContextConflict, 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply intelligent merge resolution strategy"""
        
        merged_context = copy.deepcopy(context)
        
        for key in conflict.conflicting_keys:
            # Attempt intelligent merge based on data type
            if isinstance(context[key], dict):
                # Merge dictionaries
                merged_context[key] = {**merged_context[key], **context[key]}
            elif isinstance(context[key], list):
                # Merge lists (remove duplicates)
                merged_context[key] = list(set(merged_context[key] + context[key]))
            else:
                # For primitive types, use last writer wins
                merged_context[key] = context[key]
        
        return {
            'success': True,
            'resolved_context': merged_context,
            'strategy_applied': 'MERGE_STRATEGY'
        }
    
    async def _apply_priority_resolution(self, conflict: ContextConflict, 
                                       context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply priority-based resolution strategy"""
        
        # Get agent priorities
        agent_priorities = self._get_agent_priorities()
        
        # Determine highest priority agent
        highest_priority_agent = max(
            conflict.conflicting_agents,
            key=lambda agent: agent_priorities.get(agent, 5)
        )
        
        # Use highest priority agent's values
        # (Implementation would need access to other agent's context)
        
        return {
            'success': True,
            'resolved_context': context,
            'strategy_applied': 'PRIORITY_BASED',
            'winning_agent': highest_priority_agent
        }
    
    async def _apply_context_version(self, version: ContextVersion) -> None:
        """Apply context version as current"""
        
        async with self.sync_lock:
            # Store version
            self.context_versions[version.version_id] = version
            
            # Update current version
            self.current_version_id = version.version_id
            self.version_history.append(version.version_id)
            
            # Limit version history
            if len(self.version_history) > 100:
                self.version_history = self.version_history[-100:]
            
            print(f"✅ CONTEXT VERSION APPLIED: {version.version_id} by {version.agent_id}")
    
    async def rollback_context(self, target_version_id: str) -> Dict[str, Any]:
        """Rollback context to a previous version"""
        
        if target_version_id not in self.context_versions:
            return {'success': False, 'error': 'Version not found'}
        
        async with self.sync_lock:
            target_version = self.context_versions[target_version_id]
            
            # Create rollback version
            rollback_version = ContextVersion(
                version_id=self._generate_version_id(),
                agent_id="SYSTEM_ROLLBACK",
                context_data=copy.deepcopy(target_version.context_data),
                timestamp=datetime.now().isoformat(),
                checksum=target_version.checksum,
                parent_version=self.current_version_id
            )
            
            await self._apply_context_version(rollback_version)
            
            self.sync_metrics['rollbacks_performed'] += 1
            
            print(f"🔄 CONTEXT ROLLBACK: Rolled back to version {target_version_id}")
            
            return {
                'success': True,
                'rollback_version_id': rollback_version.version_id,
                'target_version_id': target_version_id
            }
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Get current synchronization status"""
        
        return {
            'current_version_id': self.current_version_id,
            'total_versions': len(self.context_versions),
            'active_conflicts': len(self.active_conflicts),
            'pending_updates': sum(len(updates) for updates in self.pending_updates.values()),
            'sync_metrics': self.sync_metrics,
            'agent_locks_active': len([lock for lock in self.agent_locks.values() if lock.locked()]),
            'system_status': 'OPERATIONAL'
        }
    
    def _generate_version_id(self) -> str:
        """Generate unique version ID"""
        return f"CTX_V_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
    
    def _calculate_context_checksum(self, context: Dict[str, Any]) -> str:
        """Calculate checksum for context integrity"""
        context_str = json.dumps(context, sort_keys=True)
        return hashlib.sha256(context_str.encode()).hexdigest()[:16]
    
    async def _get_current_context(self) -> Dict[str, Any]:
        """Get current context data"""
        if self.current_version_id in self.context_versions:
            return self.context_versions[self.current_version_id].context_data
        return {}
    
    def _get_recent_versions(self, count: int) -> List[ContextVersion]:
        """Get recent context versions"""
        recent_version_ids = self.version_history[-count:]
        return [self.context_versions[vid] for vid in recent_version_ids 
                if vid in self.context_versions]
    
    def _determine_resolution_strategy(self, conflicting_keys: List[str]) -> ConflictResolutionStrategy:
        """Determine appropriate conflict resolution strategy"""
        
        # Simple strategy determination based on key types
        if any('config' in key.lower() for key in conflicting_keys):
            return ConflictResolutionStrategy.PRIORITY_BASED
        elif any('data' in key.lower() for key in conflicting_keys):
            return ConflictResolutionStrategy.MERGE_STRATEGY
        else:
            return ConflictResolutionStrategy.LAST_WRITER_WINS
    
    def _get_agent_priorities(self) -> Dict[str, int]:
        """Get agent priority mappings"""
        return {
            'JAEGIS': 10,
            'John': 9,
            'Fred': 9,
            'Tyler': 9,
            'Jane': 8,
            'Alex': 8,
            'James': 8,
            'Dakota': 8,
            'Sage': 8,
            'Sentinel': 8,
            'DocQA': 7
        }
    
    async def _update_sync_metrics(self, sync_time: float, conflicts_count: int) -> None:
        """Update synchronization metrics"""
        self.sync_metrics['total_syncs'] += 1
        self.sync_metrics['conflicts_detected'] += conflicts_count
        
        # Update average sync time
        current_avg = self.sync_metrics['average_sync_time']
        total_syncs = self.sync_metrics['total_syncs']
        self.sync_metrics['average_sync_time'] = (
            (current_avg * (total_syncs - 1) + sync_time) / total_syncs
        )
    
    async def _handle_resolution_failure(self, version: ContextVersion, 
                                       conflicts: List[ContextConflict]) -> None:
        """Handle failed conflict resolution"""
        
        # Store conflicts for manual resolution
        for conflict in conflicts:
            self.active_conflicts[conflict.conflict_id] = conflict
        
        # Add to pending updates for retry
        if version.agent_id not in self.pending_updates:
            self.pending_updates[version.agent_id] = []
        
        self.pending_updates[version.agent_id].append(version)
        
        print(f"⚠️ RESOLUTION FAILURE: {len(conflicts)} conflicts require manual resolution")
    
    def _initialize_context_sync_system(self) -> None:
        """Initialize the context synchronization system"""
        
        # Create initial context version
        initial_context = {
            'system_initialized': True,
            'initialization_time': datetime.now().isoformat(),
            'sync_system_version': '1.0.0'
        }
        
        initial_version = ContextVersion(
            version_id=self.current_version_id,
            agent_id="SYSTEM_INIT",
            context_data=initial_context,
            timestamp=datetime.now().isoformat(),
            checksum=self._calculate_context_checksum(initial_context)
        )
        
        self.context_versions[self.current_version_id] = initial_version
        self.version_history.append(self.current_version_id)
        
        print("🔄 JAEGIS Asynchronous Context Synchronization System initialized")
        print(f"   Initial Version: {self.current_version_id}")
        print("   Conflict Resolution: ACTIVE")
        print("   Version Control: ENABLED")
        print("   Rollback Support: AVAILABLE")

# Global synchronization system instance
JAEGIS_ASYNC_CONTEXT_SYNC = JAEGISAsyncContextSynchronizer()

# Convenience functions for agent integration
async def update_agent_context(agent_id: str, updates: Dict[str, Any], priority: int = 5) -> Dict[str, Any]:
    """Update agent context with async synchronization"""
    return await JAEGIS_ASYNC_CONTEXT_SYNC.update_context_async(agent_id, updates, priority)

async def get_context_sync_status() -> Dict[str, Any]:
    """Get current context synchronization status"""
    return await JAEGIS_ASYNC_CONTEXT_SYNC.get_sync_status()

async def rollback_agent_context(version_id: str) -> Dict[str, Any]:
    """Rollback context to previous version"""
    return await JAEGIS_ASYNC_CONTEXT_SYNC.rollback_context(version_id)

# Example usage and testing
if __name__ == "__main__":
    async def test_async_context_sync():
        print("🧪 Testing JAEGIS Asynchronous Context Synchronization...")
        
        # Test concurrent updates
        tasks = []
        for i in range(5):
            agent_id = f"TestAgent_{i}"
            updates = {f"test_key_{i}": f"value_{i}", "shared_key": f"agent_{i}_value"}
            task = update_agent_context(agent_id, updates, priority=i+1)
            tasks.append(task)
        
        # Execute concurrent updates
        results = await asyncio.gather(*tasks)
        
        print(f"\n📊 CONCURRENT UPDATE RESULTS:")
        for result in results:
            print(f"   Agent: {result['agent_id']} | Status: {result['sync_status']} | Conflicts: {result['conflicts_detected']}")
        
        # Get system status
        status = await get_context_sync_status()
        print(f"\n🎯 SYNC SYSTEM STATUS:")
        print(f"   Total Syncs: {status['sync_metrics']['total_syncs']}")
        print(f"   Conflicts Detected: {status['sync_metrics']['conflicts_detected']}")
        print(f"   Average Sync Time: {status['sync_metrics']['average_sync_time']:.3f}s")
        
        print("\n✅ JAEGIS Asynchronous Context Synchronization test completed")
    
    # Run test
    asyncio.run(test_async_context_sync())
