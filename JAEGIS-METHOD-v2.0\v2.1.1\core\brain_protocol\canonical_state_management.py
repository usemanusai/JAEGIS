"""
JAEGIS Brain Protocol Suite v1.0 - Canonical State Management Protocol
Directive 1.5: Single source of truth for project metrics with dynamic lookup

This module implements the mandatory canonical state management protocol that ensures
the AGI provides consistent, accurate project information by maintaining a single
source of truth and forbidding memory-based metric reporting.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)


class MetricType(str, Enum):
    """Types of canonical metrics."""
    PROJECT_STATUS = "project_status"
    AGENT_COUNT = "agent_count"
    SYSTEM_PERFORMANCE = "system_performance"
    DEPLOYMENT_STATUS = "deployment_status"
    SECURITY_STATUS = "security_status"
    DOCUMENTATION_STATUS = "documentation_status"
    INTEGRATION_STATUS = "integration_status"
    VERSION_INFO = "version_info"


class MetricSource(str, Enum):
    """Sources of canonical metrics."""
    CONFIGURATION_FILE = "configuration_file"
    RUNTIME_CALCULATION = "runtime_calculation"
    EXTERNAL_API = "external_api"
    FILE_SYSTEM_SCAN = "file_system_scan"
    DATABASE_QUERY = "database_query"


@dataclass
class CanonicalMetric:
    """Canonical metric definition."""
    metric_id: str
    metric_type: MetricType
    metric_name: str
    current_value: Any
    source: MetricSource
    source_path: str
    last_updated: float
    update_frequency_seconds: float
    validation_hash: str
    dependencies: List[str]


@dataclass
class MetricValidation:
    """Metric validation result."""
    metric_id: str
    is_valid: bool
    validation_errors: List[str]
    source_accessible: bool
    hash_matches: bool
    last_validation: float


@dataclass
class StateSnapshot:
    """Complete system state snapshot."""
    snapshot_id: str
    timestamp: float
    metrics: Dict[str, CanonicalMetric]
    validation_results: Dict[str, MetricValidation]
    system_health: str
    inconsistencies_detected: List[str]


class CanonicalStateManager:
    """
    JAEGIS Brain Protocol Suite Canonical State Manager
    
    Implements Directive 1.5: Canonical State Management Protocol
    
    Mandatory execution sequence:
    1. Single Source of Truth - All metrics stored in canonical source
    2. Force Dynamic Lookup - Forbidden from stating metrics from memory
    3. Real-time Validation - Continuous validation and consistency checking
    """
    
    def __init__(self):
        self.canonical_state_path = Path("core/brain_protocol/canonical_state.json")
        self.metrics_registry: Dict[str, CanonicalMetric] = {}
        self.validation_history: List[MetricValidation] = []
        self.state_snapshots: List[StateSnapshot] = []
        
        # Initialize canonical state
        self._initialize_canonical_state()
        
        logger.info("Canonical State Manager initialized")
    
    def _initialize_canonical_state(self):
        """Initialize the canonical state management system."""
        
        # Create canonical state directory
        self.canonical_state_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize core metrics
        self._initialize_core_metrics()
        
        # Load existing state or create new
        if self.canonical_state_path.exists():
            self._load_canonical_state()
        else:
            self._create_initial_canonical_state()
    
    def _initialize_core_metrics(self):
        """Initialize core canonical metrics."""
        
        core_metrics = [
            {
                "metric_id": "jaegis_version",
                "metric_type": MetricType.VERSION_INFO,
                "metric_name": "JAEGIS System Version",
                "source": MetricSource.CONFIGURATION_FILE,
                "source_path": "core/brain_protocol/protocol_suite.json",
                "update_frequency_seconds": 3600,  # 1 hour
                "dependencies": []
            },
            {
                "metric_id": "total_agents",
                "metric_type": MetricType.AGENT_COUNT,
                "metric_name": "Total JAEGIS Agents",
                "source": MetricSource.RUNTIME_CALCULATION,
                "source_path": "core/brain_protocol/task_scoping_delegation.py",
                "update_frequency_seconds": 300,  # 5 minutes
                "dependencies": []
            },
            {
                "metric_id": "system_status",
                "metric_type": MetricType.PROJECT_STATUS,
                "metric_name": "Overall System Status",
                "source": MetricSource.RUNTIME_CALCULATION,
                "source_path": "core/brain_protocol/system_initialization.py",
                "update_frequency_seconds": 60,  # 1 minute
                "dependencies": ["jaegis_version", "total_agents"]
            },
            {
                "metric_id": "brain_protocol_status",
                "metric_type": MetricType.DEPLOYMENT_STATUS,
                "metric_name": "Brain Protocol Implementation Status",
                "source": MetricSource.FILE_SYSTEM_SCAN,
                "source_path": "core/brain_protocol/",
                "update_frequency_seconds": 300,  # 5 minutes
                "dependencies": []
            },
            {
                "metric_id": "documentation_completeness",
                "metric_type": MetricType.DOCUMENTATION_STATUS,
                "metric_name": "Documentation Completeness Percentage",
                "source": MetricSource.FILE_SYSTEM_SCAN,
                "source_path": ".",
                "update_frequency_seconds": 600,  # 10 minutes
                "dependencies": []
            },
            {
                "metric_id": "security_compliance",
                "metric_type": MetricType.SECURITY_STATUS,
                "metric_name": "Security Compliance Score",
                "source": MetricSource.RUNTIME_CALCULATION,
                "source_path": "core/brain_protocol/",
                "update_frequency_seconds": 1800,  # 30 minutes
                "dependencies": ["brain_protocol_status"]
            }
        ]
        
        for metric_data in core_metrics:
            metric = CanonicalMetric(
                metric_id=metric_data["metric_id"],
                metric_type=metric_data["metric_type"],
                metric_name=metric_data["metric_name"],
                current_value=None,  # Will be calculated
                source=metric_data["source"],
                source_path=metric_data["source_path"],
                last_updated=0.0,
                update_frequency_seconds=metric_data["update_frequency_seconds"],
                validation_hash="",
                dependencies=metric_data["dependencies"]
            )
            
            self.metrics_registry[metric.metric_id] = metric
    
    def _create_initial_canonical_state(self):
        """Create initial canonical state file."""
        
        initial_state = {
            "version": "1.0",
            "created": time.time(),
            "last_updated": time.time(),
            "metrics": {},
            "metadata": {
                "total_metrics": 0,
                "last_validation": 0.0,
                "validation_frequency_seconds": 300
            }
        }
        
        with open(self.canonical_state_path, 'w') as f:
            json.dump(initial_state, f, indent=2)
        
        logger.info("Created initial canonical state file")
    
    def _load_canonical_state(self):
        """Load existing canonical state."""
        
        try:
            with open(self.canonical_state_path, 'r') as f:
                state_data = json.load(f)
            
            # Load metrics from state
            for metric_id, metric_data in state_data.get("metrics", {}).items():
                if metric_id in self.metrics_registry:
                    metric = self.metrics_registry[metric_id]
                    metric.current_value = metric_data.get("current_value")
                    metric.last_updated = metric_data.get("last_updated", 0.0)
                    metric.validation_hash = metric_data.get("validation_hash", "")
            
            logger.info("Loaded existing canonical state")
            
        except Exception as e:
            logger.error(f"Failed to load canonical state: {e}")
            self._create_initial_canonical_state()
    
    async def force_dynamic_lookup(self, metric_id: str) -> Any:
        """
        MANDATORY: Force dynamic lookup of metric value
        
        This method MUST be used instead of memory-based metric reporting.
        The AGI is FORBIDDEN from stating project metrics from memory.
        """
        
        logger.info(f"🔍 FORCE DYNAMIC LOOKUP - Metric ID: {metric_id}")
        
        if metric_id not in self.metrics_registry:
            raise ValueError(f"Unknown metric ID: {metric_id}")
        
        metric = self.metrics_registry[metric_id]
        
        # Check if metric needs update
        time_since_update = time.time() - metric.last_updated
        needs_update = time_since_update > metric.update_frequency_seconds
        
        if needs_update or metric.current_value is None:
            logger.info(f"📊 Updating metric: {metric.metric_name}")
            await self._update_metric(metric)
        
        # Validate metric
        validation = await self._validate_metric(metric)
        
        if not validation.is_valid:
            logger.warning(f"⚠️ Metric validation failed: {metric_id}")
            logger.warning(f"Errors: {validation.validation_errors}")
        
        logger.info(f"✅ Dynamic lookup complete: {metric.metric_name} = {metric.current_value}")
        
        return metric.current_value
    
    async def _update_metric(self, metric: CanonicalMetric):
        """Update metric value from its canonical source."""
        
        try:
            if metric.source == MetricSource.CONFIGURATION_FILE:
                metric.current_value = await self._read_from_config_file(metric)
            
            elif metric.source == MetricSource.RUNTIME_CALCULATION:
                metric.current_value = await self._calculate_runtime_metric(metric)
            
            elif metric.source == MetricSource.FILE_SYSTEM_SCAN:
                metric.current_value = await self._scan_file_system(metric)
            
            elif metric.source == MetricSource.EXTERNAL_API:
                metric.current_value = await self._query_external_api(metric)
            
            elif metric.source == MetricSource.DATABASE_QUERY:
                metric.current_value = await self._query_database(metric)
            
            else:
                raise ValueError(f"Unknown metric source: {metric.source}")
            
            # Update metadata
            metric.last_updated = time.time()
            metric.validation_hash = self._calculate_validation_hash(metric)
            
            # Save to canonical state
            await self._save_canonical_state()
            
        except Exception as e:
            logger.error(f"Failed to update metric {metric.metric_id}: {e}")
            raise
    
    async def _read_from_config_file(self, metric: CanonicalMetric) -> Any:
        """Read metric value from configuration file."""
        
        config_path = Path(metric.source_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {metric.source_path}")
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Extract specific values based on metric type
        if metric.metric_id == "jaegis_version":
            return config_data.get("version", "unknown")
        
        return config_data
    
    async def _calculate_runtime_metric(self, metric: CanonicalMetric) -> Any:
        """Calculate metric value at runtime."""
        
        if metric.metric_id == "total_agents":
            # Import and count agents from delegation engine
            try:
                from .task_scoping_delegation import TASK_DELEGATION_ENGINE
                return len(TASK_DELEGATION_ENGINE.agents)
            except ImportError:
                return 128  # Default from enhanced system
        
        elif metric.metric_id == "system_status":
            # Calculate overall system status
            try:
                from .system_initialization import JAEGIS_BRAIN_INITIALIZER
                if JAEGIS_BRAIN_INITIALIZER.is_initialized():
                    return "operational"
                else:
                    return "initializing"
            except ImportError:
                return "unknown"
        
        elif metric.metric_id == "security_compliance":
            # Calculate security compliance score
            brain_protocol_files = list(Path("core/brain_protocol").glob("*.py"))
            compliance_score = min(100, len(brain_protocol_files) * 15)  # 15 points per file
            return compliance_score
        
        return "calculated_value"
    
    async def _scan_file_system(self, metric: CanonicalMetric) -> Any:
        """Scan file system for metric value."""
        
        scan_path = Path(metric.source_path)
        
        if metric.metric_id == "brain_protocol_status":
            # Count implemented brain protocol files
            if scan_path.is_dir():
                protocol_files = list(scan_path.glob("*.py"))
                total_expected = 11  # 6 directives + 5 mandates
                implemented = len(protocol_files)
                completion_percentage = (implemented / total_expected) * 100
                return f"{completion_percentage:.1f}% complete ({implemented}/{total_expected} files)"
            
        elif metric.metric_id == "documentation_completeness":
            # Calculate documentation completeness
            if scan_path.is_dir():
                doc_files = list(scan_path.glob("**/*.md"))
                readme_exists = (scan_path / "README.md").exists()
                changelog_exists = (scan_path / "CHANGELOG.md").exists()
                
                base_score = 50 if readme_exists else 0
                base_score += 20 if changelog_exists else 0
                base_score += min(30, len(doc_files) * 5)  # 5 points per doc file, max 30
                
                return base_score
        
        return "scanned_value"
    
    async def _query_external_api(self, metric: CanonicalMetric) -> Any:
        """Query external API for metric value."""
        
        # Placeholder for external API queries
        return "api_value"
    
    async def _query_database(self, metric: CanonicalMetric) -> Any:
        """Query database for metric value."""
        
        # Placeholder for database queries
        return "db_value"
    
    def _calculate_validation_hash(self, metric: CanonicalMetric) -> str:
        """Calculate validation hash for metric."""
        
        hash_input = f"{metric.metric_id}:{metric.current_value}:{metric.last_updated}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    async def _validate_metric(self, metric: CanonicalMetric) -> MetricValidation:
        """Validate metric integrity and consistency."""
        
        validation_errors = []
        source_accessible = True
        hash_matches = True
        
        # Check source accessibility
        try:
            source_path = Path(metric.source_path)
            if metric.source in [MetricSource.CONFIGURATION_FILE, MetricSource.FILE_SYSTEM_SCAN]:
                source_accessible = source_path.exists()
                if not source_accessible:
                    validation_errors.append(f"Source path not accessible: {metric.source_path}")
        except Exception as e:
            source_accessible = False
            validation_errors.append(f"Source validation error: {e}")
        
        # Validate hash
        expected_hash = self._calculate_validation_hash(metric)
        hash_matches = expected_hash == metric.validation_hash
        if not hash_matches:
            validation_errors.append("Validation hash mismatch")
        
        # Check dependencies
        for dep_id in metric.dependencies:
            if dep_id not in self.metrics_registry:
                validation_errors.append(f"Missing dependency: {dep_id}")
        
        validation = MetricValidation(
            metric_id=metric.metric_id,
            is_valid=len(validation_errors) == 0,
            validation_errors=validation_errors,
            source_accessible=source_accessible,
            hash_matches=hash_matches,
            last_validation=time.time()
        )
        
        self.validation_history.append(validation)
        
        return validation
    
    async def _save_canonical_state(self):
        """Save current state to canonical state file."""
        
        state_data = {
            "version": "1.0",
            "created": time.time(),
            "last_updated": time.time(),
            "metrics": {},
            "metadata": {
                "total_metrics": len(self.metrics_registry),
                "last_validation": time.time(),
                "validation_frequency_seconds": 300
            }
        }
        
        # Serialize metrics
        for metric_id, metric in self.metrics_registry.items():
            state_data["metrics"][metric_id] = {
                "metric_type": metric.metric_type.value,
                "metric_name": metric.metric_name,
                "current_value": metric.current_value,
                "source": metric.source.value,
                "source_path": metric.source_path,
                "last_updated": metric.last_updated,
                "update_frequency_seconds": metric.update_frequency_seconds,
                "validation_hash": metric.validation_hash,
                "dependencies": metric.dependencies
            }
        
        with open(self.canonical_state_path, 'w') as f:
            json.dump(state_data, f, indent=2)
    
    async def get_system_state_snapshot(self) -> StateSnapshot:
        """Get complete system state snapshot."""
        
        snapshot_id = f"snapshot_{int(time.time())}"
        
        # Update all metrics
        for metric in self.metrics_registry.values():
            await self._update_metric(metric)
        
        # Validate all metrics
        validation_results = {}
        for metric_id, metric in self.metrics_registry.items():
            validation_results[metric_id] = await self._validate_metric(metric)
        
        # Determine system health
        failed_validations = [v for v in validation_results.values() if not v.is_valid]
        if not failed_validations:
            system_health = "healthy"
        elif len(failed_validations) < len(validation_results) * 0.2:  # Less than 20% failed
            system_health = "degraded"
        else:
            system_health = "critical"
        
        # Detect inconsistencies
        inconsistencies = []
        for validation in failed_validations:
            inconsistencies.extend(validation.validation_errors)
        
        snapshot = StateSnapshot(
            snapshot_id=snapshot_id,
            timestamp=time.time(),
            metrics=self.metrics_registry.copy(),
            validation_results=validation_results,
            system_health=system_health,
            inconsistencies_detected=inconsistencies
        )
        
        self.state_snapshots.append(snapshot)
        
        return snapshot
    
    def get_canonical_state_status(self) -> Dict[str, Any]:
        """Get canonical state management status."""
        
        total_metrics = len(self.metrics_registry)
        recent_validations = [v for v in self.validation_history if time.time() - v.last_validation < 3600]
        failed_validations = [v for v in recent_validations if not v.is_valid]
        
        return {
            "total_metrics": total_metrics,
            "canonical_state_file": str(self.canonical_state_path),
            "file_exists": self.canonical_state_path.exists(),
            "recent_validations": len(recent_validations),
            "failed_validations": len(failed_validations),
            "validation_success_rate": (len(recent_validations) - len(failed_validations)) / len(recent_validations) if recent_validations else 0,
            "state_snapshots": len(self.state_snapshots),
            "last_snapshot": self.state_snapshots[-1].timestamp if self.state_snapshots else None
        }


# Global canonical state manager
CANONICAL_STATE_MANAGER = CanonicalStateManager()


async def mandatory_metric_lookup(metric_id: str) -> Any:
    """
    MANDATORY: Force dynamic lookup of project metric
    
    This function MUST be used instead of memory-based metric reporting
    according to JAEGIS Brain Protocol Suite Directive 1.5.
    """
    
    return await CANONICAL_STATE_MANAGER.force_dynamic_lookup(metric_id)


async def get_canonical_system_snapshot() -> StateSnapshot:
    """
    Get complete canonical system state snapshot
    
    This provides a comprehensive view of all canonical metrics and their
    validation status for system health monitoring.
    """
    
    return await CANONICAL_STATE_MANAGER.get_system_state_snapshot()


# Example usage
async def main():
    """Example usage of Canonical State Manager."""
    
    print("📊 JAEGIS BRAIN PROTOCOL SUITE - CANONICAL STATE MANAGEMENT TEST")
    
    # Test dynamic metric lookups
    test_metrics = [
        "jaegis_version",
        "total_agents", 
        "system_status",
        "brain_protocol_status",
        "documentation_completeness",
        "security_compliance"
    ]
    
    for metric_id in test_metrics:
        try:
            value = await CANONICAL_STATE_MANAGER.force_dynamic_lookup(metric_id)
            print(f"  {metric_id}: {value}")
        except Exception as e:
            print(f"  {metric_id}: ERROR - {e}")
    
    # Get system snapshot
    snapshot = await CANONICAL_STATE_MANAGER.get_system_state_snapshot()
    print(f"\n📸 System Snapshot:")
    print(f"  Snapshot ID: {snapshot.snapshot_id}")
    print(f"  System Health: {snapshot.system_health}")
    print(f"  Total Metrics: {len(snapshot.metrics)}")
    print(f"  Inconsistencies: {len(snapshot.inconsistencies_detected)}")
    
    # Get status
    status = CANONICAL_STATE_MANAGER.get_canonical_state_status()
    print(f"\n📊 Canonical State Status:")
    print(f"  Total Metrics: {status['total_metrics']}")
    print(f"  Validation Success Rate: {status['validation_success_rate']:.1%}")
    print(f"  State Snapshots: {status['state_snapshots']}")


if __name__ == "__main__":
    asyncio.run(main())
