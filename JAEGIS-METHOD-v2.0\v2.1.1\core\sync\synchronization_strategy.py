"""
Synchronization Strategy Planning System
Develop optimal sync strategy, branch targeting, file prioritization, and dependency management
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import networkx as nx

logger = logging.getLogger(__name__)


class SyncStrategy(str, Enum):
    """Synchronization strategies."""
    INCREMENTAL = "incremental"
    FULL_SYNC = "full_sync"
    SELECTIVE = "selective"
    PRIORITY_BASED = "priority_based"
    DEPENDENCY_AWARE = "dependency_aware"


class BranchStrategy(str, Enum):
    """Branch targeting strategies."""
    MAIN_ONLY = "main_only"
    DEVELOPMENT_FIRST = "development_first"
    FEATURE_BRANCHES = "feature_branches"
    ALL_BRANCHES = "all_branches"


class FilePriority(str, Enum):
    """File synchronization priorities."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DEFERRED = "deferred"


@dataclass
class FileMetadata:
    """File metadata for synchronization."""
    file_path: str
    priority: FilePriority
    dependencies: List[str]
    size_bytes: int
    last_modified: float
    file_type: str
    sync_frequency: str
    critical_for_build: bool


@dataclass
class SyncPlan:
    """Comprehensive synchronization plan."""
    plan_id: str
    strategy: SyncStrategy
    branch_strategy: BranchStrategy
    target_branches: List[str]
    file_batches: List[List[str]]
    dependency_order: List[str]
    estimated_duration_minutes: int
    bandwidth_requirements_mb: float
    risk_assessment: str
    rollback_plan: List[str]


@dataclass
class SyncExecution:
    """Synchronization execution tracking."""
    execution_id: str
    plan_id: str
    start_time: float
    end_time: Optional[float]
    status: str
    files_synced: int
    files_failed: int
    bytes_transferred: int
    errors: List[str]


class SynchronizationPlanner:
    """
    Synchronization Strategy Planning System
    
    Provides intelligent synchronization planning including:
    - Optimal sync strategy selection
    - Branch targeting optimization
    - File prioritization and batching
    - Dependency-aware ordering
    - Bandwidth and time optimization
    """
    
    def __init__(self):
        self.file_metadata: Dict[str, FileMetadata] = {}
        self.dependency_graph = nx.DiGraph()
        self.sync_history: List[SyncExecution] = []
        
        # Configuration
        self.config = {
            "max_batch_size_mb": 100,
            "max_concurrent_files": 10,
            "bandwidth_limit_mbps": 50,
            "sync_timeout_minutes": 60,
            "retry_attempts": 3,
            "priority_weights": {
                FilePriority.CRITICAL: 1.0,
                FilePriority.HIGH: 0.8,
                FilePriority.MEDIUM: 0.6,
                FilePriority.LOW: 0.4,
                FilePriority.DEFERRED: 0.2
            }
        }
        
        # File type priorities
        self.file_type_priorities = self._initialize_file_type_priorities()
        
        logger.info("Synchronization Strategy Planner initialized")
    
    def _initialize_file_type_priorities(self) -> Dict[str, FilePriority]:
        """Initialize default file type priorities."""
        
        return {
            # Critical system files
            ".py": FilePriority.CRITICAL,
            ".js": FilePriority.CRITICAL,
            ".ts": FilePriority.CRITICAL,
            ".json": FilePriority.HIGH,
            ".yaml": FilePriority.HIGH,
            ".yml": FilePriority.HIGH,
            ".toml": FilePriority.HIGH,
            
            # Documentation
            ".md": FilePriority.MEDIUM,
            ".rst": FilePriority.MEDIUM,
            ".txt": FilePriority.MEDIUM,
            
            # Configuration
            ".cfg": FilePriority.HIGH,
            ".ini": FilePriority.HIGH,
            ".conf": FilePriority.HIGH,
            
            # Build files
            "Dockerfile": FilePriority.HIGH,
            "requirements.txt": FilePriority.HIGH,
            "package.json": FilePriority.HIGH,
            "Cargo.toml": FilePriority.HIGH,
            
            # Assets
            ".png": FilePriority.LOW,
            ".jpg": FilePriority.LOW,
            ".jpeg": FilePriority.LOW,
            ".gif": FilePriority.LOW,
            ".svg": FilePriority.MEDIUM,
            
            # Archives
            ".zip": FilePriority.DEFERRED,
            ".tar": FilePriority.DEFERRED,
            ".gz": FilePriority.DEFERRED,
            
            # Temporary files
            ".tmp": FilePriority.DEFERRED,
            ".log": FilePriority.LOW,
            ".cache": FilePriority.DEFERRED
        }
    
    async def analyze_workspace(self, workspace_path: str) -> Dict[str, Any]:
        """Analyze workspace to build file metadata and dependencies."""
        
        logger.info(f"Analyzing workspace: {workspace_path}")
        
        workspace = Path(workspace_path)
        analysis_result = {
            "total_files": 0,
            "total_size_mb": 0,
            "file_types": {},
            "priority_distribution": {},
            "dependency_count": 0
        }
        
        # Scan all files
        for file_path in workspace.rglob("*"):
            if file_path.is_file():
                await self._analyze_file(file_path, workspace)
                analysis_result["total_files"] += 1
        
        # Build dependency graph
        await self._build_dependency_graph()
        
        # Calculate statistics
        total_size = sum(metadata.size_bytes for metadata in self.file_metadata.values())
        analysis_result["total_size_mb"] = total_size / (1024 * 1024)
        
        # Count by file type
        for metadata in self.file_metadata.values():
            file_type = metadata.file_type
            analysis_result["file_types"][file_type] = analysis_result["file_types"].get(file_type, 0) + 1
        
        # Count by priority
        for metadata in self.file_metadata.values():
            priority = metadata.priority.value
            analysis_result["priority_distribution"][priority] = analysis_result["priority_distribution"].get(priority, 0) + 1
        
        analysis_result["dependency_count"] = self.dependency_graph.number_of_edges()
        
        logger.info(f"Workspace analysis complete: {analysis_result['total_files']} files, {analysis_result['total_size_mb']:.1f} MB")
        
        return analysis_result
    
    async def _analyze_file(self, file_path: Path, workspace_root: Path):
        """Analyze individual file for metadata."""
        
        try:
            relative_path = str(file_path.relative_to(workspace_root))
            file_stats = file_path.stat()
            
            # Determine file type and priority
            file_extension = file_path.suffix.lower()
            file_name = file_path.name
            
            # Get priority based on file type or name
            priority = self.file_type_priorities.get(file_extension, FilePriority.MEDIUM)
            
            # Special handling for specific files
            if file_name in ["README.md", "LICENSE", "CHANGELOG.md"]:
                priority = FilePriority.HIGH
            elif file_name.startswith("."):
                priority = FilePriority.LOW
            
            # Detect dependencies
            dependencies = await self._detect_file_dependencies(file_path)
            
            # Determine sync frequency
            sync_frequency = self._determine_sync_frequency(file_path, priority)
            
            # Check if critical for build
            critical_for_build = self._is_critical_for_build(file_path)
            
            metadata = FileMetadata(
                file_path=relative_path,
                priority=priority,
                dependencies=dependencies,
                size_bytes=file_stats.st_size,
                last_modified=file_stats.st_mtime,
                file_type=file_extension or "unknown",
                sync_frequency=sync_frequency,
                critical_for_build=critical_for_build
            )
            
            self.file_metadata[relative_path] = metadata
            
        except Exception as e:
            logger.error(f"Failed to analyze file {file_path}: {e}")
    
    async def _detect_file_dependencies(self, file_path: Path) -> List[str]:
        """Detect file dependencies through static analysis."""
        
        dependencies = []
        
        try:
            if file_path.suffix.lower() == ".py":
                # Python import analysis
                dependencies.extend(await self._analyze_python_imports(file_path))
            
            elif file_path.suffix.lower() in [".js", ".ts"]:
                # JavaScript/TypeScript import analysis
                dependencies.extend(await self._analyze_js_imports(file_path))
            
            elif file_path.suffix.lower() == ".json":
                # JSON reference analysis
                dependencies.extend(await self._analyze_json_references(file_path))
            
            elif file_path.name in ["Dockerfile"]:
                # Dockerfile dependency analysis
                dependencies.extend(await self._analyze_dockerfile_dependencies(file_path))
        
        except Exception as e:
            logger.debug(f"Dependency analysis failed for {file_path}: {e}")
        
        return dependencies
    
    async def _analyze_python_imports(self, file_path: Path) -> List[str]:
        """Analyze Python imports to detect dependencies."""
        
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Handle 'from ... import ...' statements
                if line.startswith('from ') and ' import ' in line:
                    module = line.split('from ')[1].split(' import ')[0].strip()
                    if module.startswith('.'):  # Relative import
                        # Convert to file path
                        module_path = module.replace('.', '/') + '.py'
                        dependencies.append(module_path)
                
                # Handle 'import ...' statements
                elif line.startswith('import '):
                    modules = line.split('import ')[1].split(',')
                    for module in modules:
                        module = module.strip().split(' as ')[0]
                        if '.' in module:
                            module_path = module.replace('.', '/') + '.py'
                            dependencies.append(module_path)
        
        except Exception as e:
            logger.debug(f"Python import analysis failed for {file_path}: {e}")
        
        return dependencies
    
    async def _analyze_js_imports(self, file_path: Path) -> List[str]:
        """Analyze JavaScript/TypeScript imports."""
        
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Handle ES6 imports
                if 'import ' in line and ' from ' in line:
                    import_path = line.split(' from ')[1].strip().strip('\'"')
                    if import_path.startswith('./') or import_path.startswith('../'):
                        dependencies.append(import_path)
                
                # Handle require statements
                elif 'require(' in line:
                    start = line.find('require(') + 8
                    end = line.find(')', start)
                    if end > start:
                        import_path = line[start:end].strip('\'"')
                        if import_path.startswith('./') or import_path.startswith('../'):
                            dependencies.append(import_path)
        
        except Exception as e:
            logger.debug(f"JS import analysis failed for {file_path}: {e}")
        
        return dependencies
    
    async def _analyze_json_references(self, file_path: Path) -> List[str]:
        """Analyze JSON file references."""
        
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            data = json.loads(content)
            
            # Look for file references in common JSON structures
            if isinstance(data, dict):
                # Check for file paths in values
                for key, value in data.items():
                    if isinstance(value, str) and ('/' in value or '\\' in value):
                        if value.endswith(('.py', '.js', '.ts', '.json', '.yaml', '.yml')):
                            dependencies.append(value)
        
        except Exception as e:
            logger.debug(f"JSON analysis failed for {file_path}: {e}")
        
        return dependencies
    
    async def _analyze_dockerfile_dependencies(self, file_path: Path) -> List[str]:
        """Analyze Dockerfile dependencies."""
        
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # COPY and ADD commands
                if line.startswith('COPY ') or line.startswith('ADD '):
                    parts = line.split()
                    if len(parts) >= 3:
                        source = parts[1]
                        if not source.startswith('http'):  # Local file
                            dependencies.append(source)
        
        except Exception as e:
            logger.debug(f"Dockerfile analysis failed for {file_path}: {e}")
        
        return dependencies
    
    def _determine_sync_frequency(self, file_path: Path, priority: FilePriority) -> str:
        """Determine synchronization frequency for file."""
        
        if priority == FilePriority.CRITICAL:
            return "immediate"
        elif priority == FilePriority.HIGH:
            return "hourly"
        elif priority == FilePriority.MEDIUM:
            return "daily"
        else:
            return "weekly"
    
    def _is_critical_for_build(self, file_path: Path) -> bool:
        """Determine if file is critical for build process."""
        
        critical_files = {
            "Dockerfile", "docker-compose.yml", "requirements.txt",
            "package.json", "Cargo.toml", "setup.py", "pyproject.toml"
        }
        
        critical_extensions = {".py", ".js", ".ts", ".json", ".yaml", ".yml"}
        
        return (file_path.name in critical_files or 
                file_path.suffix.lower() in critical_extensions)
    
    async def _build_dependency_graph(self):
        """Build dependency graph from file metadata."""
        
        self.dependency_graph.clear()
        
        # Add all files as nodes
        for file_path in self.file_metadata.keys():
            self.dependency_graph.add_node(file_path)
        
        # Add dependency edges
        for file_path, metadata in self.file_metadata.items():
            for dependency in metadata.dependencies:
                if dependency in self.file_metadata:
                    self.dependency_graph.add_edge(dependency, file_path)
    
    async def create_sync_plan(self, strategy: SyncStrategy = SyncStrategy.PRIORITY_BASED,
                             branch_strategy: BranchStrategy = BranchStrategy.DEVELOPMENT_FIRST) -> SyncPlan:
        """Create comprehensive synchronization plan."""
        
        plan_id = f"sync_plan_{int(time.time())}"
        
        logger.info(f"Creating sync plan: {strategy.value} strategy")
        
        # Determine target branches
        target_branches = self._determine_target_branches(branch_strategy)
        
        # Create file batches based on strategy
        file_batches = await self._create_file_batches(strategy)
        
        # Determine dependency order
        dependency_order = self._calculate_dependency_order()
        
        # Estimate duration and bandwidth
        estimated_duration, bandwidth_requirements = self._estimate_sync_requirements(file_batches)
        
        # Assess risks
        risk_assessment = self._assess_sync_risks(file_batches, strategy)
        
        # Create rollback plan
        rollback_plan = self._create_rollback_plan(file_batches)
        
        plan = SyncPlan(
            plan_id=plan_id,
            strategy=strategy,
            branch_strategy=branch_strategy,
            target_branches=target_branches,
            file_batches=file_batches,
            dependency_order=dependency_order,
            estimated_duration_minutes=estimated_duration,
            bandwidth_requirements_mb=bandwidth_requirements,
            risk_assessment=risk_assessment,
            rollback_plan=rollback_plan
        )
        
        logger.info(f"Sync plan created: {len(file_batches)} batches, {estimated_duration} min duration")
        
        return plan
    
    def _determine_target_branches(self, strategy: BranchStrategy) -> List[str]:
        """Determine target branches based on strategy."""
        
        if strategy == BranchStrategy.MAIN_ONLY:
            return ["main"]
        elif strategy == BranchStrategy.DEVELOPMENT_FIRST:
            return ["development", "main"]
        elif strategy == BranchStrategy.FEATURE_BRANCHES:
            return ["development", "feature/*", "main"]
        else:  # ALL_BRANCHES
            return ["*"]
    
    async def _create_file_batches(self, strategy: SyncStrategy) -> List[List[str]]:
        """Create file batches based on synchronization strategy."""
        
        if strategy == SyncStrategy.PRIORITY_BASED:
            return self._create_priority_batches()
        
        elif strategy == SyncStrategy.DEPENDENCY_AWARE:
            return self._create_dependency_batches()
        
        elif strategy == SyncStrategy.SELECTIVE:
            return self._create_selective_batches()
        
        elif strategy == SyncStrategy.INCREMENTAL:
            return self._create_incremental_batches()
        
        else:  # FULL_SYNC
            return self._create_full_sync_batches()
    
    def _create_priority_batches(self) -> List[List[str]]:
        """Create batches based on file priorities."""
        
        batches = []
        
        # Group files by priority
        priority_groups = {}
        for file_path, metadata in self.file_metadata.items():
            priority = metadata.priority
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(file_path)
        
        # Create batches in priority order
        priority_order = [FilePriority.CRITICAL, FilePriority.HIGH, FilePriority.MEDIUM, FilePriority.LOW, FilePriority.DEFERRED]
        
        for priority in priority_order:
            if priority in priority_groups:
                files = priority_groups[priority]
                
                # Split into size-based batches
                current_batch = []
                current_size = 0
                max_size = self.config["max_batch_size_mb"] * 1024 * 1024
                
                for file_path in files:
                    file_size = self.file_metadata[file_path].size_bytes
                    
                    if current_size + file_size > max_size and current_batch:
                        batches.append(current_batch)
                        current_batch = [file_path]
                        current_size = file_size
                    else:
                        current_batch.append(file_path)
                        current_size += file_size
                
                if current_batch:
                    batches.append(current_batch)
        
        return batches
    
    def _create_dependency_batches(self) -> List[List[str]]:
        """Create batches respecting dependency order."""
        
        batches = []
        
        try:
            # Get topological order
            topo_order = list(nx.topological_sort(self.dependency_graph))
            
            # Create batches respecting dependencies
            current_batch = []
            current_size = 0
            max_size = self.config["max_batch_size_mb"] * 1024 * 1024
            
            for file_path in topo_order:
                if file_path in self.file_metadata:
                    file_size = self.file_metadata[file_path].size_bytes
                    
                    if current_size + file_size > max_size and current_batch:
                        batches.append(current_batch)
                        current_batch = [file_path]
                        current_size = file_size
                    else:
                        current_batch.append(file_path)
                        current_size += file_size
            
            if current_batch:
                batches.append(current_batch)
        
        except nx.NetworkXError:
            # Fallback to priority-based if dependency graph has cycles
            logger.warning("Dependency graph has cycles, falling back to priority-based batching")
            return self._create_priority_batches()
        
        return batches
    
    def _create_selective_batches(self) -> List[List[str]]:
        """Create selective batches for critical files only."""
        
        critical_files = [
            file_path for file_path, metadata in self.file_metadata.items()
            if metadata.priority in [FilePriority.CRITICAL, FilePriority.HIGH] or metadata.critical_for_build
        ]
        
        return [critical_files] if critical_files else []
    
    def _create_incremental_batches(self) -> List[List[str]]:
        """Create incremental batches based on modification time."""
        
        # Sort by modification time (most recent first)
        sorted_files = sorted(
            self.file_metadata.items(),
            key=lambda x: x[1].last_modified,
            reverse=True
        )
        
        batches = []
        current_batch = []
        current_size = 0
        max_size = self.config["max_batch_size_mb"] * 1024 * 1024
        
        for file_path, metadata in sorted_files:
            if current_size + metadata.size_bytes > max_size and current_batch:
                batches.append(current_batch)
                current_batch = [file_path]
                current_size = metadata.size_bytes
            else:
                current_batch.append(file_path)
                current_size += metadata.size_bytes
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _create_full_sync_batches(self) -> List[List[str]]:
        """Create batches for full synchronization."""
        
        all_files = list(self.file_metadata.keys())
        
        batches = []
        current_batch = []
        current_size = 0
        max_size = self.config["max_batch_size_mb"] * 1024 * 1024
        
        for file_path in all_files:
            file_size = self.file_metadata[file_path].size_bytes
            
            if current_size + file_size > max_size and current_batch:
                batches.append(current_batch)
                current_batch = [file_path]
                current_size = file_size
            else:
                current_batch.append(file_path)
                current_size += file_size
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _calculate_dependency_order(self) -> List[str]:
        """Calculate optimal dependency order for synchronization."""
        
        try:
            return list(nx.topological_sort(self.dependency_graph))
        except nx.NetworkXError:
            # If there are cycles, return files sorted by priority
            return sorted(
                self.file_metadata.keys(),
                key=lambda x: self.config["priority_weights"][self.file_metadata[x].priority],
                reverse=True
            )
    
    def _estimate_sync_requirements(self, file_batches: List[List[str]]) -> Tuple[int, float]:
        """Estimate synchronization duration and bandwidth requirements."""
        
        total_size_bytes = 0
        total_files = 0
        
        for batch in file_batches:
            for file_path in batch:
                if file_path in self.file_metadata:
                    total_size_bytes += self.file_metadata[file_path].size_bytes
                    total_files += 1
        
        # Estimate duration based on file count and size
        file_processing_time = total_files * 2  # 2 seconds per file overhead
        transfer_time = (total_size_bytes / (1024 * 1024)) / self.config["bandwidth_limit_mbps"] * 60  # minutes
        
        estimated_duration = int(file_processing_time / 60 + transfer_time)
        bandwidth_requirements = total_size_bytes / (1024 * 1024)  # MB
        
        return estimated_duration, bandwidth_requirements
    
    def _assess_sync_risks(self, file_batches: List[List[str]], strategy: SyncStrategy) -> str:
        """Assess synchronization risks."""
        
        total_files = sum(len(batch) for batch in file_batches)
        critical_files = sum(
            1 for batch in file_batches for file_path in batch
            if file_path in self.file_metadata and self.file_metadata[file_path].priority == FilePriority.CRITICAL
        )
        
        if critical_files > total_files * 0.5:
            return "HIGH - Many critical files in sync"
        elif strategy == SyncStrategy.FULL_SYNC:
            return "MEDIUM - Full synchronization carries inherent risks"
        elif total_files > 1000:
            return "MEDIUM - Large number of files to sync"
        else:
            return "LOW - Standard synchronization risk"
    
    def _create_rollback_plan(self, file_batches: List[List[str]]) -> List[str]:
        """Create rollback plan for synchronization."""
        
        return [
            "Stop current synchronization process",
            "Restore files from backup if available",
            "Verify system integrity",
            "Rollback to previous known good state",
            "Notify stakeholders of rollback",
            "Investigate sync failure causes",
            "Plan corrective actions"
        ]
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get synchronization statistics and metrics."""
        
        total_files = len(self.file_metadata)
        total_size = sum(metadata.size_bytes for metadata in self.file_metadata.values())
        
        # Priority distribution
        priority_counts = {}
        for priority in FilePriority:
            priority_counts[priority.value] = len([
                m for m in self.file_metadata.values() if m.priority == priority
            ])
        
        # File type distribution
        type_counts = {}
        for metadata in self.file_metadata.values():
            file_type = metadata.file_type
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
        
        return {
            "total_files": total_files,
            "total_size_mb": total_size / (1024 * 1024),
            "priority_distribution": priority_counts,
            "file_type_distribution": type_counts,
            "dependency_edges": self.dependency_graph.number_of_edges(),
            "critical_files": priority_counts.get("critical", 0),
            "sync_executions": len(self.sync_history)
        }


# Example usage
async def main():
    """Example usage of Synchronization Planner."""
    
    planner = SynchronizationPlanner()
    
    # Simulate workspace analysis
    print("Analyzing workspace...")
    # analysis = await planner.analyze_workspace(".")
    
    # Create sync plan
    plan = await planner.create_sync_plan(
        strategy=SyncStrategy.PRIORITY_BASED,
        branch_strategy=BranchStrategy.DEVELOPMENT_FIRST
    )
    
    print(f"Sync Plan Created:")
    print(f"  Strategy: {plan.strategy.value}")
    print(f"  Branches: {plan.target_branches}")
    print(f"  Batches: {len(plan.file_batches)}")
    print(f"  Duration: {plan.estimated_duration_minutes} minutes")
    print(f"  Bandwidth: {plan.bandwidth_requirements_mb:.1f} MB")
    print(f"  Risk: {plan.risk_assessment}")
    
    # Get statistics
    stats = planner.get_sync_statistics()
    print(f"\nStatistics:")
    print(f"  Total files: {stats['total_files']}")
    print(f"  Total size: {stats['total_size_mb']:.1f} MB")
    print(f"  Critical files: {stats['critical_files']}")


if __name__ == "__main__":
    asyncio.run(main())
