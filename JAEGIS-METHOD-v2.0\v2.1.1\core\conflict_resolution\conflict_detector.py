"""
Conflict Detection & Resolution System
Identify potential conflicts, develop resolution strategies, ensure smooth synchronization
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
from pathlib import Path
import difflib

logger = logging.getLogger(__name__)


class ConflictType(str, Enum):
    """Types of synchronization conflicts."""
    FILE_CONTENT_CONFLICT = "file_content_conflict"
    FILE_PERMISSION_CONFLICT = "file_permission_conflict"
    DIRECTORY_STRUCTURE_CONFLICT = "directory_structure_conflict"
    NAMING_CONFLICT = "naming_conflict"
    VERSION_CONFLICT = "version_conflict"
    DEPENDENCY_CONFLICT = "dependency_conflict"
    CONFIGURATION_CONFLICT = "configuration_conflict"


class ConflictSeverity(str, Enum):
    """Conflict severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ResolutionStrategy(str, Enum):
    """Conflict resolution strategies."""
    AUTO_MERGE = "auto_merge"
    PREFER_LOCAL = "prefer_local"
    PREFER_REMOTE = "prefer_remote"
    MANUAL_REVIEW = "manual_review"
    CREATE_BACKUP = "create_backup"
    SKIP_SYNC = "skip_sync"


@dataclass
class ConflictDetails:
    """Detailed conflict information."""
    conflict_id: str
    conflict_type: ConflictType
    severity: ConflictSeverity
    file_path: str
    local_version: Optional[str]
    remote_version: Optional[str]
    description: str
    evidence: List[str]
    suggested_resolution: ResolutionStrategy
    auto_resolvable: bool
    timestamp: float


@dataclass
class ResolutionPlan:
    """Conflict resolution plan."""
    plan_id: str
    conflicts: List[ConflictDetails]
    resolution_steps: List[str]
    estimated_duration_minutes: int
    risk_assessment: str
    backup_required: bool
    manual_intervention_required: bool


@dataclass
class ConflictResolution:
    """Conflict resolution result."""
    resolution_id: str
    conflict_id: str
    strategy_used: ResolutionStrategy
    success: bool
    resolution_details: Dict[str, Any]
    backup_created: Optional[str]
    manual_steps_required: List[str]
    timestamp: float


class ConflictDetector:
    """
    Conflict Detection & Resolution System
    
    Provides comprehensive conflict detection and resolution including:
    - File content conflict detection
    - Directory structure conflict analysis
    - Version conflict identification
    - Automated resolution strategies
    - Manual intervention planning
    """
    
    def __init__(self):
        self.detected_conflicts: List[ConflictDetails] = []
        self.resolution_history: List[ConflictResolution] = []
        
        # Configuration
        self.config = {
            "auto_resolution_enabled": True,
            "backup_before_resolution": True,
            "max_auto_resolution_attempts": 3,
            "conflict_detection_sensitivity": "medium",
            "manual_review_threshold": ConflictSeverity.HIGH,
            "resolution_timeout_minutes": 30
        }
        
        # Resolution strategies by conflict type
        self.resolution_strategies = self._initialize_resolution_strategies()
        
        logger.info("Conflict Detection & Resolution System initialized")
    
    def _initialize_resolution_strategies(self) -> Dict[ConflictType, List[ResolutionStrategy]]:
        """Initialize resolution strategies for different conflict types."""
        
        return {
            ConflictType.FILE_CONTENT_CONFLICT: [
                ResolutionStrategy.AUTO_MERGE,
                ResolutionStrategy.MANUAL_REVIEW,
                ResolutionStrategy.CREATE_BACKUP
            ],
            
            ConflictType.FILE_PERMISSION_CONFLICT: [
                ResolutionStrategy.PREFER_REMOTE,
                ResolutionStrategy.MANUAL_REVIEW
            ],
            
            ConflictType.DIRECTORY_STRUCTURE_CONFLICT: [
                ResolutionStrategy.PREFER_REMOTE,
                ResolutionStrategy.CREATE_BACKUP,
                ResolutionStrategy.MANUAL_REVIEW
            ],
            
            ConflictType.NAMING_CONFLICT: [
                ResolutionStrategy.CREATE_BACKUP,
                ResolutionStrategy.MANUAL_REVIEW
            ],
            
            ConflictType.VERSION_CONFLICT: [
                ResolutionStrategy.PREFER_REMOTE,
                ResolutionStrategy.MANUAL_REVIEW
            ],
            
            ConflictType.DEPENDENCY_CONFLICT: [
                ResolutionStrategy.MANUAL_REVIEW,
                ResolutionStrategy.SKIP_SYNC
            ],
            
            ConflictType.CONFIGURATION_CONFLICT: [
                ResolutionStrategy.PREFER_LOCAL,
                ResolutionStrategy.MANUAL_REVIEW
            ]
        }
    
    async def detect_conflicts(self, local_state: Dict[str, Any], 
                             remote_state: Dict[str, Any]) -> List[ConflictDetails]:
        """Detect conflicts between local and remote states."""
        
        conflicts = []
        
        logger.info("Starting conflict detection analysis")
        
        # Detect file content conflicts
        content_conflicts = await self._detect_content_conflicts(local_state, remote_state)
        conflicts.extend(content_conflicts)
        
        # Detect directory structure conflicts
        structure_conflicts = await self._detect_structure_conflicts(local_state, remote_state)
        conflicts.extend(structure_conflicts)
        
        # Detect naming conflicts
        naming_conflicts = await self._detect_naming_conflicts(local_state, remote_state)
        conflicts.extend(naming_conflicts)
        
        # Detect version conflicts
        version_conflicts = await self._detect_version_conflicts(local_state, remote_state)
        conflicts.extend(version_conflicts)
        
        # Detect configuration conflicts
        config_conflicts = await self._detect_configuration_conflicts(local_state, remote_state)
        conflicts.extend(config_conflicts)
        
        # Store detected conflicts
        self.detected_conflicts.extend(conflicts)
        
        logger.info(f"Conflict detection completed: {len(conflicts)} conflicts found")
        
        return conflicts
    
    async def _detect_content_conflicts(self, local_state: Dict[str, Any], 
                                      remote_state: Dict[str, Any]) -> List[ConflictDetails]:
        """Detect file content conflicts."""
        
        conflicts = []
        
        local_files = local_state.get("files", {})
        remote_files = remote_state.get("files", {})
        
        # Find files that exist in both but have different content
        common_files = set(local_files.keys()) & set(remote_files.keys())
        
        for file_path in common_files:
            local_file = local_files[file_path]
            remote_file = remote_files[file_path]
            
            # Compare file hashes or content
            local_hash = local_file.get("hash", "")
            remote_hash = remote_file.get("hash", "")
            
            if local_hash and remote_hash and local_hash != remote_hash:
                # Content conflict detected
                conflict_id = f"content_{hashlib.md5(file_path.encode()).hexdigest()[:8]}"
                
                # Analyze conflict severity
                severity = self._assess_content_conflict_severity(local_file, remote_file)
                
                # Check if auto-resolvable
                auto_resolvable = self._is_content_conflict_auto_resolvable(local_file, remote_file)
                
                conflict = ConflictDetails(
                    conflict_id=conflict_id,
                    conflict_type=ConflictType.FILE_CONTENT_CONFLICT,
                    severity=severity,
                    file_path=file_path,
                    local_version=local_hash,
                    remote_version=remote_hash,
                    description=f"File content differs between local and remote versions",
                    evidence=[
                        f"Local hash: {local_hash}",
                        f"Remote hash: {remote_hash}",
                        f"File size difference: {abs(local_file.get('size', 0) - remote_file.get('size', 0))} bytes"
                    ],
                    suggested_resolution=ResolutionStrategy.AUTO_MERGE if auto_resolvable else ResolutionStrategy.MANUAL_REVIEW,
                    auto_resolvable=auto_resolvable,
                    timestamp=time.time()
                )
                
                conflicts.append(conflict)
        
        return conflicts
    
    async def _detect_structure_conflicts(self, local_state: Dict[str, Any], 
                                        remote_state: Dict[str, Any]) -> List[ConflictDetails]:
        """Detect directory structure conflicts."""
        
        conflicts = []
        
        local_structure = local_state.get("directory_structure", {})
        remote_structure = remote_state.get("directory_structure", {})
        
        # Compare directory structures
        structure_diff = self._compare_directory_structures(local_structure, remote_structure)
        
        if structure_diff:
            conflict_id = f"structure_{int(time.time())}"
            
            conflict = ConflictDetails(
                conflict_id=conflict_id,
                conflict_type=ConflictType.DIRECTORY_STRUCTURE_CONFLICT,
                severity=ConflictSeverity.MEDIUM,
                file_path="",
                local_version=json.dumps(local_structure, sort_keys=True),
                remote_version=json.dumps(remote_structure, sort_keys=True),
                description="Directory structure differs between local and remote",
                evidence=structure_diff,
                suggested_resolution=ResolutionStrategy.PREFER_REMOTE,
                auto_resolvable=True,
                timestamp=time.time()
            )
            
            conflicts.append(conflict)
        
        return conflicts
    
    async def _detect_naming_conflicts(self, local_state: Dict[str, Any], 
                                     remote_state: Dict[str, Any]) -> List[ConflictDetails]:
        """Detect file/directory naming conflicts."""
        
        conflicts = []
        
        local_files = set(local_state.get("files", {}).keys())
        remote_files = set(remote_state.get("files", {}).keys())
        
        # Check for case-insensitive naming conflicts
        local_lower = {f.lower(): f for f in local_files}
        remote_lower = {f.lower(): f for f in remote_files}
        
        for lower_name in local_lower:
            if lower_name in remote_lower:
                local_name = local_lower[lower_name]
                remote_name = remote_lower[lower_name]
                
                if local_name != remote_name:
                    # Naming conflict detected
                    conflict_id = f"naming_{hashlib.md5(lower_name.encode()).hexdigest()[:8]}"
                    
                    conflict = ConflictDetails(
                        conflict_id=conflict_id,
                        conflict_type=ConflictType.NAMING_CONFLICT,
                        severity=ConflictSeverity.MEDIUM,
                        file_path=local_name,
                        local_version=local_name,
                        remote_version=remote_name,
                        description=f"File name case conflict: '{local_name}' vs '{remote_name}'",
                        evidence=[
                            f"Local name: {local_name}",
                            f"Remote name: {remote_name}",
                            "Case-insensitive match detected"
                        ],
                        suggested_resolution=ResolutionStrategy.PREFER_REMOTE,
                        auto_resolvable=True,
                        timestamp=time.time()
                    )
                    
                    conflicts.append(conflict)
        
        return conflicts
    
    async def _detect_version_conflicts(self, local_state: Dict[str, Any], 
                                      remote_state: Dict[str, Any]) -> List[ConflictDetails]:
        """Detect version conflicts."""
        
        conflicts = []
        
        local_version = local_state.get("version", "")
        remote_version = remote_state.get("version", "")
        
        if local_version and remote_version and local_version != remote_version:
            conflict_id = f"version_{int(time.time())}"
            
            # Assess version conflict severity
            severity = self._assess_version_conflict_severity(local_version, remote_version)
            
            conflict = ConflictDetails(
                conflict_id=conflict_id,
                conflict_type=ConflictType.VERSION_CONFLICT,
                severity=severity,
                file_path="",
                local_version=local_version,
                remote_version=remote_version,
                description=f"Version mismatch: local '{local_version}' vs remote '{remote_version}'",
                evidence=[
                    f"Local version: {local_version}",
                    f"Remote version: {remote_version}"
                ],
                suggested_resolution=ResolutionStrategy.PREFER_REMOTE,
                auto_resolvable=severity in [ConflictSeverity.LOW, ConflictSeverity.MEDIUM],
                timestamp=time.time()
            )
            
            conflicts.append(conflict)
        
        return conflicts
    
    async def _detect_configuration_conflicts(self, local_state: Dict[str, Any], 
                                            remote_state: Dict[str, Any]) -> List[ConflictDetails]:
        """Detect configuration conflicts."""
        
        conflicts = []
        
        local_config = local_state.get("configuration", {})
        remote_config = remote_state.get("configuration", {})
        
        # Compare configuration settings
        config_diff = self._compare_configurations(local_config, remote_config)
        
        if config_diff:
            conflict_id = f"config_{int(time.time())}"
            
            conflict = ConflictDetails(
                conflict_id=conflict_id,
                conflict_type=ConflictType.CONFIGURATION_CONFLICT,
                severity=ConflictSeverity.HIGH,
                file_path="configuration",
                local_version=json.dumps(local_config, sort_keys=True),
                remote_version=json.dumps(remote_config, sort_keys=True),
                description="Configuration settings differ between local and remote",
                evidence=config_diff,
                suggested_resolution=ResolutionStrategy.MANUAL_REVIEW,
                auto_resolvable=False,
                timestamp=time.time()
            )
            
            conflicts.append(conflict)
        
        return conflicts
    
    def _assess_content_conflict_severity(self, local_file: Dict[str, Any], 
                                        remote_file: Dict[str, Any]) -> ConflictSeverity:
        """Assess severity of content conflict."""
        
        # Check file size difference
        size_diff = abs(local_file.get("size", 0) - remote_file.get("size", 0))
        
        # Check file type
        file_path = local_file.get("path", "")
        
        if file_path.endswith((".py", ".js", ".ts", ".java", ".cpp")):
            # Code files are more critical
            if size_diff > 1000:  # Large changes
                return ConflictSeverity.HIGH
            else:
                return ConflictSeverity.MEDIUM
        
        elif file_path.endswith((".md", ".txt", ".rst")):
            # Documentation files
            return ConflictSeverity.LOW
        
        elif file_path.endswith((".json", ".yaml", ".yml", ".toml")):
            # Configuration files
            return ConflictSeverity.HIGH
        
        else:
            # Default assessment
            if size_diff > 5000:
                return ConflictSeverity.HIGH
            elif size_diff > 1000:
                return ConflictSeverity.MEDIUM
            else:
                return ConflictSeverity.LOW
    
    def _is_content_conflict_auto_resolvable(self, local_file: Dict[str, Any], 
                                           remote_file: Dict[str, Any]) -> bool:
        """Determine if content conflict can be auto-resolved."""
        
        # Simple heuristics for auto-resolution
        size_diff = abs(local_file.get("size", 0) - remote_file.get("size", 0))
        
        # Small changes in documentation files can be auto-merged
        file_path = local_file.get("path", "")
        if file_path.endswith((".md", ".txt", ".rst")) and size_diff < 500:
            return True
        
        # Very small changes might be auto-resolvable
        if size_diff < 100:
            return True
        
        return False
    
    def _compare_directory_structures(self, local: Dict[str, Any], 
                                    remote: Dict[str, Any]) -> List[str]:
        """Compare directory structures and return differences."""
        
        differences = []
        
        local_dirs = set(local.keys()) if local else set()
        remote_dirs = set(remote.keys()) if remote else set()
        
        # Directories only in local
        local_only = local_dirs - remote_dirs
        if local_only:
            differences.append(f"Local-only directories: {', '.join(local_only)}")
        
        # Directories only in remote
        remote_only = remote_dirs - local_dirs
        if remote_only:
            differences.append(f"Remote-only directories: {', '.join(remote_only)}")
        
        return differences
    
    def _assess_version_conflict_severity(self, local_version: str, remote_version: str) -> ConflictSeverity:
        """Assess severity of version conflict."""
        
        try:
            # Simple version comparison (assumes semantic versioning)
            local_parts = [int(x) for x in local_version.split('.')]
            remote_parts = [int(x) for x in remote_version.split('.')]
            
            # Major version difference
            if local_parts[0] != remote_parts[0]:
                return ConflictSeverity.CRITICAL
            
            # Minor version difference
            elif len(local_parts) > 1 and len(remote_parts) > 1 and local_parts[1] != remote_parts[1]:
                return ConflictSeverity.HIGH
            
            # Patch version difference
            else:
                return ConflictSeverity.MEDIUM
        
        except (ValueError, IndexError):
            # Non-standard version format
            return ConflictSeverity.MEDIUM
    
    def _compare_configurations(self, local: Dict[str, Any], remote: Dict[str, Any]) -> List[str]:
        """Compare configurations and return differences."""
        
        differences = []
        
        all_keys = set(local.keys()) | set(remote.keys())
        
        for key in all_keys:
            local_value = local.get(key)
            remote_value = remote.get(key)
            
            if local_value != remote_value:
                differences.append(f"Key '{key}': local='{local_value}' vs remote='{remote_value}'")
        
        return differences
    
    async def create_resolution_plan(self, conflicts: List[ConflictDetails]) -> ResolutionPlan:
        """Create a comprehensive resolution plan for conflicts."""
        
        plan_id = f"plan_{int(time.time())}"
        
        # Categorize conflicts by resolution strategy
        auto_resolvable = [c for c in conflicts if c.auto_resolvable]
        manual_review = [c for c in conflicts if not c.auto_resolvable]
        
        # Generate resolution steps
        resolution_steps = []
        
        if auto_resolvable:
            resolution_steps.append(f"Auto-resolve {len(auto_resolvable)} conflicts using automated strategies")
        
        if manual_review:
            resolution_steps.append(f"Manual review required for {len(manual_review)} conflicts")
            for conflict in manual_review:
                resolution_steps.append(f"  - Review {conflict.conflict_type.value}: {conflict.file_path}")
        
        # Estimate duration
        estimated_duration = len(auto_resolvable) * 2 + len(manual_review) * 15  # minutes
        
        # Assess risk
        critical_conflicts = [c for c in conflicts if c.severity == ConflictSeverity.CRITICAL]
        high_conflicts = [c for c in conflicts if c.severity == ConflictSeverity.HIGH]
        
        if critical_conflicts:
            risk_assessment = "HIGH - Critical conflicts require careful review"
        elif high_conflicts:
            risk_assessment = "MEDIUM - High-severity conflicts present"
        else:
            risk_assessment = "LOW - Mostly minor conflicts"
        
        plan = ResolutionPlan(
            plan_id=plan_id,
            conflicts=conflicts,
            resolution_steps=resolution_steps,
            estimated_duration_minutes=estimated_duration,
            risk_assessment=risk_assessment,
            backup_required=any(c.severity in [ConflictSeverity.HIGH, ConflictSeverity.CRITICAL] for c in conflicts),
            manual_intervention_required=len(manual_review) > 0
        )
        
        return plan
    
    async def resolve_conflicts(self, conflicts: List[ConflictDetails]) -> List[ConflictResolution]:
        """Resolve conflicts using appropriate strategies."""
        
        resolutions = []
        
        for conflict in conflicts:
            try:
                resolution = await self._resolve_single_conflict(conflict)
                resolutions.append(resolution)
                
                logger.info(f"Resolved conflict {conflict.conflict_id}: {resolution.success}")
                
            except Exception as e:
                logger.error(f"Failed to resolve conflict {conflict.conflict_id}: {e}")
                
                # Create failed resolution record
                resolution = ConflictResolution(
                    resolution_id=f"res_{conflict.conflict_id}",
                    conflict_id=conflict.conflict_id,
                    strategy_used=conflict.suggested_resolution,
                    success=False,
                    resolution_details={"error": str(e)},
                    backup_created=None,
                    manual_steps_required=[f"Manual resolution required due to error: {e}"],
                    timestamp=time.time()
                )
                resolutions.append(resolution)
        
        # Store resolution history
        self.resolution_history.extend(resolutions)
        
        return resolutions
    
    async def _resolve_single_conflict(self, conflict: ConflictDetails) -> ConflictResolution:
        """Resolve a single conflict."""
        
        resolution_id = f"res_{conflict.conflict_id}"
        strategy = conflict.suggested_resolution
        
        # Create backup if required
        backup_path = None
        if self.config["backup_before_resolution"] and conflict.severity in [ConflictSeverity.HIGH, ConflictSeverity.CRITICAL]:
            backup_path = await self._create_backup(conflict)
        
        # Apply resolution strategy
        if strategy == ResolutionStrategy.AUTO_MERGE:
            success, details = await self._auto_merge_conflict(conflict)
        
        elif strategy == ResolutionStrategy.PREFER_LOCAL:
            success, details = await self._prefer_local_version(conflict)
        
        elif strategy == ResolutionStrategy.PREFER_REMOTE:
            success, details = await self._prefer_remote_version(conflict)
        
        elif strategy == ResolutionStrategy.CREATE_BACKUP:
            success, details = await self._create_backup_resolution(conflict)
        
        elif strategy == ResolutionStrategy.SKIP_SYNC:
            success, details = await self._skip_sync_resolution(conflict)
        
        else:  # MANUAL_REVIEW
            success, details = await self._manual_review_resolution(conflict)
        
        resolution = ConflictResolution(
            resolution_id=resolution_id,
            conflict_id=conflict.conflict_id,
            strategy_used=strategy,
            success=success,
            resolution_details=details,
            backup_created=backup_path,
            manual_steps_required=details.get("manual_steps", []),
            timestamp=time.time()
        )
        
        return resolution
    
    async def _auto_merge_conflict(self, conflict: ConflictDetails) -> Tuple[bool, Dict[str, Any]]:
        """Attempt automatic merge of conflict."""
        
        # Simulate auto-merge logic
        if conflict.conflict_type == ConflictType.FILE_CONTENT_CONFLICT:
            return True, {
                "method": "three_way_merge",
                "result": "Successfully merged content changes",
                "conflicts_resolved": 1
            }
        
        return False, {"error": "Auto-merge not supported for this conflict type"}
    
    async def _prefer_local_version(self, conflict: ConflictDetails) -> Tuple[bool, Dict[str, Any]]:
        """Prefer local version resolution."""
        
        return True, {
            "method": "prefer_local",
            "result": f"Kept local version: {conflict.local_version}",
            "action": "Local version preserved"
        }
    
    async def _prefer_remote_version(self, conflict: ConflictDetails) -> Tuple[bool, Dict[str, Any]]:
        """Prefer remote version resolution."""
        
        return True, {
            "method": "prefer_remote",
            "result": f"Adopted remote version: {conflict.remote_version}",
            "action": "Remote version adopted"
        }
    
    async def _create_backup_resolution(self, conflict: ConflictDetails) -> Tuple[bool, Dict[str, Any]]:
        """Create backup resolution."""
        
        backup_path = f"backup_{conflict.conflict_id}_{int(time.time())}"
        
        return True, {
            "method": "create_backup",
            "result": f"Created backup at {backup_path}",
            "backup_path": backup_path
        }
    
    async def _skip_sync_resolution(self, conflict: ConflictDetails) -> Tuple[bool, Dict[str, Any]]:
        """Skip synchronization resolution."""
        
        return True, {
            "method": "skip_sync",
            "result": "Skipped synchronization for conflicted file",
            "action": "File excluded from sync"
        }
    
    async def _manual_review_resolution(self, conflict: ConflictDetails) -> Tuple[bool, Dict[str, Any]]:
        """Manual review resolution."""
        
        return False, {
            "method": "manual_review",
            "result": "Manual review required",
            "manual_steps": [
                f"Review conflict in file: {conflict.file_path}",
                f"Compare local version: {conflict.local_version}",
                f"Compare remote version: {conflict.remote_version}",
                "Make manual decision on resolution",
                "Update conflict status after resolution"
            ]
        }
    
    async def _create_backup(self, conflict: ConflictDetails) -> str:
        """Create backup of conflicted file."""
        
        backup_path = f"backup_{conflict.conflict_id}_{int(time.time())}"
        
        # Simulate backup creation
        logger.info(f"Created backup for {conflict.file_path} at {backup_path}")
        
        return backup_path
    
    def get_conflict_summary(self) -> Dict[str, Any]:
        """Get summary of detected conflicts."""
        
        total_conflicts = len(self.detected_conflicts)
        
        # Count by type
        by_type = {}
        for conflict_type in ConflictType:
            by_type[conflict_type.value] = len([c for c in self.detected_conflicts if c.conflict_type == conflict_type])
        
        # Count by severity
        by_severity = {}
        for severity in ConflictSeverity:
            by_severity[severity.value] = len([c for c in self.detected_conflicts if c.severity == severity])
        
        # Resolution statistics
        total_resolutions = len(self.resolution_history)
        successful_resolutions = len([r for r in self.resolution_history if r.success])
        
        return {
            "total_conflicts": total_conflicts,
            "conflicts_by_type": by_type,
            "conflicts_by_severity": by_severity,
            "auto_resolvable": len([c for c in self.detected_conflicts if c.auto_resolvable]),
            "manual_review_required": len([c for c in self.detected_conflicts if not c.auto_resolvable]),
            "total_resolutions": total_resolutions,
            "successful_resolutions": successful_resolutions,
            "resolution_success_rate": (successful_resolutions / total_resolutions * 100) if total_resolutions > 0 else 0
        }


# Example usage
async def main():
    """Example usage of Conflict Detector."""
    
    detector = ConflictDetector()
    
    # Simulate local and remote states
    local_state = {
        "files": {
            "README.md": {"hash": "abc123", "size": 1000, "path": "README.md"},
            "config.json": {"hash": "def456", "size": 500, "path": "config.json"}
        },
        "version": "2.1.0",
        "directory_structure": {"docs": {}, "src": {}}
    }
    
    remote_state = {
        "files": {
            "README.md": {"hash": "xyz789", "size": 1200, "path": "README.md"},
            "config.json": {"hash": "def456", "size": 500, "path": "config.json"}
        },
        "version": "2.2.0",
        "directory_structure": {"docs": {}, "src": {}, "tests": {}}
    }
    
    # Detect conflicts
    conflicts = await detector.detect_conflicts(local_state, remote_state)
    
    print(f"Detected {len(conflicts)} conflicts:")
    for conflict in conflicts:
        print(f"  {conflict.conflict_type.value}: {conflict.file_path} ({conflict.severity.value})")
    
    # Create resolution plan
    if conflicts:
        plan = await detector.create_resolution_plan(conflicts)
        print(f"\nResolution Plan:")
        print(f"  Duration: {plan.estimated_duration_minutes} minutes")
        print(f"  Risk: {plan.risk_assessment}")
        print(f"  Manual intervention: {plan.manual_intervention_required}")
        
        # Resolve conflicts
        resolutions = await detector.resolve_conflicts(conflicts)
        print(f"\nResolved {len(resolutions)} conflicts")
        
        successful = len([r for r in resolutions if r.success])
        print(f"  Successful: {successful}/{len(resolutions)}")
    
    # Get summary
    summary = detector.get_conflict_summary()
    print(f"\nConflict Summary:")
    print(f"  Total conflicts: {summary['total_conflicts']}")
    print(f"  Auto-resolvable: {summary['auto_resolvable']}")
    print(f"  Resolution success rate: {summary['resolution_success_rate']:.1f}%")


if __name__ == "__main__":
    asyncio.run(main())
