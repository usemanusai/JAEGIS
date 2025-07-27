"""
JAEGIS Brain Protocol Suite v1.0 - Workspace Integrity Protocol
Directive 1.6: Pre-execution scanning and absolute path validation

This module implements the mandatory workspace integrity protocol that ensures
the AGI maintains a clean, organized file system by performing pre-execution
scans and requiring user confirmation for all file operations.
"""

import asyncio
import json
import time
import logging
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class FileOperationType(str, Enum):
    """Types of file operations."""
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    MOVE = "move"
    COPY = "copy"


class IntegrityStatus(str, Enum):
    """Workspace integrity status levels."""
    CLEAN = "clean"
    MINOR_ISSUES = "minor_issues"
    MAJOR_ISSUES = "major_issues"
    CRITICAL_ISSUES = "critical_issues"


class ValidationResult(str, Enum):
    """File operation validation results."""
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    BLOCKED = "blocked"


@dataclass
class FileOperation:
    """File operation definition."""
    operation_id: str
    operation_type: FileOperationType
    source_path: str
    target_path: Optional[str]
    absolute_source_path: str
    absolute_target_path: Optional[str]
    file_size_bytes: int
    operation_reason: str
    timestamp: float


@dataclass
class IntegrityIssue:
    """Workspace integrity issue."""
    issue_id: str
    issue_type: str
    severity: str
    file_path: str
    description: str
    recommendation: str
    detected_at: float


@dataclass
class WorkspaceScan:
    """Workspace scan result."""
    scan_id: str
    scan_timestamp: float
    current_directory: str
    total_files: int
    total_directories: int
    duplicate_files: List[Tuple[str, str]]
    integrity_issues: List[IntegrityIssue]
    integrity_status: IntegrityStatus
    scan_duration_ms: float


@dataclass
class OperationValidation:
    """File operation validation result."""
    operation_id: str
    validation_result: ValidationResult
    validation_reasons: List[str]
    user_confirmation_required: bool
    absolute_paths_verified: bool
    conflicts_detected: List[str]
    recommendations: List[str]
    timestamp: float


class WorkspaceIntegrityManager:
    """
    JAEGIS Brain Protocol Suite Workspace Integrity Manager
    
    Implements Directive 1.6: Workspace Integrity Protocol
    
    Mandatory execution sequence:
    1. Pre-Execution Scan - Verify directory, scan for duplicates, state exact paths
    2. Wait for User Confirmation - Must wait for confirmation before proceeding
    3. Absolute Paths - All operations must use absolute paths
    """
    
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self.scan_history: List[WorkspaceScan] = []
        self.operation_history: List[FileOperation] = []
        self.validation_history: List[OperationValidation] = []
        
        # Integrity rules
        self.integrity_rules = {
            "max_file_size_mb": 100,
            "forbidden_extensions": [".tmp", ".cache", ".log", ".bak"],
            "forbidden_directories": ["__pycache__", ".git", "node_modules", ".env"],
            "duplicate_tolerance": 0,  # No duplicates allowed
            "max_depth": 10,
            "required_files": ["README.md"],
            "naming_conventions": {
                "no_spaces": True,
                "lowercase_preferred": True,
                "max_length": 255
            }
        }
        
        logger.info(f"Workspace Integrity Manager initialized for: {self.workspace_root}")
    
    async def mandatory_pre_execution_scan(self, operation: FileOperation) -> OperationValidation:
        """
        MANDATORY: Pre-execution scan before any file operation
        
        This method MUST be called before generating or modifying any file.
        It verifies current directory, scans for duplicates, and states exact paths.
        """
        
        logger.info(f"🔍 MANDATORY PRE-EXECUTION SCAN - Operation ID: {operation.operation_id}")
        logger.info(f"📁 Operation: {operation.operation_type.value} - {operation.source_path}")
        
        # Step 1: Verify current directory
        current_dir = await self._verify_current_directory()
        logger.info(f"📂 Current Directory: {current_dir}")
        
        # Step 2: Perform workspace scan
        workspace_scan = await self._perform_workspace_scan()
        
        # Step 3: Validate absolute paths
        absolute_paths_valid = await self._validate_absolute_paths(operation)
        
        # Step 4: Check for conflicts and duplicates
        conflicts = await self._detect_operation_conflicts(operation, workspace_scan)
        
        # Step 5: Apply integrity rules
        validation_reasons = await self._apply_integrity_rules(operation, workspace_scan)
        
        # Step 6: Determine validation result
        validation_result = await self._determine_validation_result(
            operation, workspace_scan, conflicts, validation_reasons, absolute_paths_valid
        )
        
        # Step 7: Generate recommendations
        recommendations = await self._generate_operation_recommendations(
            operation, workspace_scan, conflicts
        )
        
        # Step 8: Create validation result
        validation = OperationValidation(
            operation_id=operation.operation_id,
            validation_result=validation_result,
            validation_reasons=validation_reasons,
            user_confirmation_required=validation_result == ValidationResult.REQUIRES_CONFIRMATION,
            absolute_paths_verified=absolute_paths_valid,
            conflicts_detected=conflicts,
            recommendations=recommendations,
            timestamp=time.time()
        )
        
        # Store validation
        self.validation_history.append(validation)
        
        logger.info(f"✅ Pre-execution scan complete:")
        logger.info(f"  Validation Result: {validation_result.value}")
        logger.info(f"  Absolute Paths Valid: {absolute_paths_valid}")
        logger.info(f"  Conflicts Detected: {len(conflicts)}")
        logger.info(f"  User Confirmation Required: {validation.user_confirmation_required}")
        
        return validation
    
    async def wait_for_user_confirmation(self, validation: OperationValidation) -> bool:
        """
        MANDATORY: Wait for user confirmation before proceeding
        
        This method MUST wait for user confirmation before proceeding with
        any file system modification that requires confirmation.
        """
        
        if not validation.user_confirmation_required:
            logger.info("✅ No user confirmation required - proceeding")
            return True
        
        logger.warning("⏳ USER CONFIRMATION REQUIRED")
        logger.warning(f"Operation ID: {validation.operation_id}")
        logger.warning(f"Validation Result: {validation.validation_result.value}")
        
        if validation.validation_reasons:
            logger.warning("Validation Reasons:")
            for reason in validation.validation_reasons:
                logger.warning(f"  - {reason}")
        
        if validation.conflicts_detected:
            logger.warning("Conflicts Detected:")
            for conflict in validation.conflicts_detected:
                logger.warning(f"  - {conflict}")
        
        if validation.recommendations:
            logger.warning("Recommendations:")
            for rec in validation.recommendations:
                logger.warning(f"  - {rec}")
        
        # In a real implementation, this would wait for actual user input
        # For now, we'll simulate user approval for non-critical operations
        logger.warning("⚠️ SIMULATED USER CONFIRMATION - In production, wait for actual user input")
        
        # Simulate approval for non-blocked operations
        if validation.validation_result != ValidationResult.BLOCKED:
            logger.info("✅ User confirmation simulated as APPROVED")
            return True
        else:
            logger.error("❌ Operation BLOCKED - cannot proceed")
            return False
    
    async def _verify_current_directory(self) -> str:
        """Verify and return current working directory."""
        
        current_dir = Path.cwd().resolve()
        
        # Ensure we're in the expected workspace
        if not str(current_dir).startswith(str(self.workspace_root)):
            logger.warning(f"⚠️ Current directory outside workspace: {current_dir}")
        
        return str(current_dir)
    
    async def _perform_workspace_scan(self) -> WorkspaceScan:
        """Perform comprehensive workspace scan."""
        
        scan_start = time.time()
        scan_id = f"scan_{int(time.time())}"
        
        logger.info("🔍 Performing workspace scan...")
        
        # Count files and directories
        total_files = 0
        total_directories = 0
        file_hashes = {}
        duplicate_files = []
        integrity_issues = []
        
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                root_path = Path(root)
                
                # Skip forbidden directories
                dirs[:] = [d for d in dirs if d not in self.integrity_rules["forbidden_directories"]]
                
                total_directories += len(dirs)
                
                for file in files:
                    file_path = root_path / file
                    
                    # Skip forbidden extensions
                    if file_path.suffix in self.integrity_rules["forbidden_extensions"]:
                        continue
                    
                    total_files += 1
                    
                    # Check file size
                    try:
                        file_size = file_path.stat().st_size
                        if file_size > self.integrity_rules["max_file_size_mb"] * 1024 * 1024:
                            integrity_issues.append(IntegrityIssue(
                                issue_id=f"size_{len(integrity_issues)}",
                                issue_type="file_size",
                                severity="warning",
                                file_path=str(file_path),
                                description=f"File exceeds size limit: {file_size / (1024*1024):.1f}MB",
                                recommendation="Consider compressing or moving large files",
                                detected_at=time.time()
                            ))
                        
                        # Calculate hash for duplicate detection
                        if file_size < 10 * 1024 * 1024:  # Only hash files < 10MB
                            try:
                                with open(file_path, 'rb') as f:
                                    file_hash = hashlib.md5(f.read()).hexdigest()
                                
                                if file_hash in file_hashes:
                                    duplicate_files.append((str(file_path), file_hashes[file_hash]))
                                else:
                                    file_hashes[file_hash] = str(file_path)
                            except Exception:
                                pass  # Skip files that can't be read
                    
                    except Exception as e:
                        integrity_issues.append(IntegrityIssue(
                            issue_id=f"access_{len(integrity_issues)}",
                            issue_type="file_access",
                            severity="error",
                            file_path=str(file_path),
                            description=f"Cannot access file: {e}",
                            recommendation="Check file permissions",
                            detected_at=time.time()
                        ))
        
        except Exception as e:
            logger.error(f"Workspace scan error: {e}")
        
        # Check for required files
        for required_file in self.integrity_rules["required_files"]:
            required_path = self.workspace_root / required_file
            if not required_path.exists():
                integrity_issues.append(IntegrityIssue(
                    issue_id=f"missing_{len(integrity_issues)}",
                    issue_type="missing_file",
                    severity="warning",
                    file_path=str(required_path),
                    description=f"Required file missing: {required_file}",
                    recommendation=f"Create {required_file}",
                    detected_at=time.time()
                ))
        
        # Determine integrity status
        critical_issues = [i for i in integrity_issues if i.severity == "critical"]
        major_issues = [i for i in integrity_issues if i.severity == "error"]
        minor_issues = [i for i in integrity_issues if i.severity == "warning"]
        
        if critical_issues:
            integrity_status = IntegrityStatus.CRITICAL_ISSUES
        elif major_issues:
            integrity_status = IntegrityStatus.MAJOR_ISSUES
        elif minor_issues or duplicate_files:
            integrity_status = IntegrityStatus.MINOR_ISSUES
        else:
            integrity_status = IntegrityStatus.CLEAN
        
        scan_duration = (time.time() - scan_start) * 1000
        
        workspace_scan = WorkspaceScan(
            scan_id=scan_id,
            scan_timestamp=time.time(),
            current_directory=str(Path.cwd().resolve()),
            total_files=total_files,
            total_directories=total_directories,
            duplicate_files=duplicate_files,
            integrity_issues=integrity_issues,
            integrity_status=integrity_status,
            scan_duration_ms=scan_duration
        )
        
        self.scan_history.append(workspace_scan)
        
        logger.info(f"🔍 Workspace scan complete:")
        logger.info(f"  Files: {total_files}, Directories: {total_directories}")
        logger.info(f"  Duplicates: {len(duplicate_files)}")
        logger.info(f"  Issues: {len(integrity_issues)}")
        logger.info(f"  Status: {integrity_status.value}")
        logger.info(f"  Duration: {scan_duration:.1f}ms")
        
        return workspace_scan
    
    async def _validate_absolute_paths(self, operation: FileOperation) -> bool:
        """Validate that operation uses absolute paths."""
        
        try:
            # Verify source path is absolute
            source_path = Path(operation.source_path).resolve()
            operation.absolute_source_path = str(source_path)
            
            # Verify target path is absolute (if applicable)
            if operation.target_path:
                target_path = Path(operation.target_path).resolve()
                operation.absolute_target_path = str(target_path)
            
            # Ensure paths are within workspace
            source_in_workspace = str(source_path).startswith(str(self.workspace_root))
            target_in_workspace = True
            
            if operation.target_path:
                target_in_workspace = str(target_path).startswith(str(self.workspace_root))
            
            return source_in_workspace and target_in_workspace
        
        except Exception as e:
            logger.error(f"Path validation error: {e}")
            return False
    
    async def _detect_operation_conflicts(self, operation: FileOperation, 
                                        workspace_scan: WorkspaceScan) -> List[str]:
        """Detect conflicts with the proposed operation."""
        
        conflicts = []
        
        source_path = Path(operation.absolute_source_path)
        
        # Check for existing file conflicts
        if operation.operation_type == FileOperationType.CREATE:
            if source_path.exists():
                conflicts.append(f"File already exists: {source_path}")
        
        # Check for duplicate creation
        if operation.operation_type == FileOperationType.CREATE:
            for dup_pair in workspace_scan.duplicate_files:
                if source_path.name in [Path(p).name for p in dup_pair]:
                    conflicts.append(f"Potential duplicate file: {source_path.name}")
        
        # Check for directory conflicts
        if operation.operation_type in [FileOperationType.CREATE, FileOperationType.MOVE]:
            parent_dir = source_path.parent
            if not parent_dir.exists():
                conflicts.append(f"Parent directory does not exist: {parent_dir}")
        
        # Check for permission conflicts
        try:
            if operation.operation_type in [FileOperationType.CREATE, FileOperationType.MODIFY]:
                parent_dir = source_path.parent
                if not os.access(parent_dir, os.W_OK):
                    conflicts.append(f"No write permission: {parent_dir}")
        except Exception:
            conflicts.append("Cannot verify permissions")
        
        return conflicts
    
    async def _apply_integrity_rules(self, operation: FileOperation, 
                                   workspace_scan: WorkspaceScan) -> List[str]:
        """Apply integrity rules to the operation."""
        
        validation_reasons = []
        
        source_path = Path(operation.absolute_source_path)
        
        # Check file extension
        if source_path.suffix in self.integrity_rules["forbidden_extensions"]:
            validation_reasons.append(f"Forbidden file extension: {source_path.suffix}")
        
        # Check file size
        if operation.file_size_bytes > self.integrity_rules["max_file_size_mb"] * 1024 * 1024:
            validation_reasons.append(f"File size exceeds limit: {operation.file_size_bytes / (1024*1024):.1f}MB")
        
        # Check naming conventions
        if self.integrity_rules["naming_conventions"]["no_spaces"] and " " in source_path.name:
            validation_reasons.append("File name contains spaces")
        
        if len(source_path.name) > self.integrity_rules["naming_conventions"]["max_length"]:
            validation_reasons.append("File name too long")
        
        # Check directory depth
        try:
            relative_path = source_path.relative_to(self.workspace_root)
            if len(relative_path.parts) > self.integrity_rules["max_depth"]:
                validation_reasons.append("Directory depth exceeds limit")
        except ValueError:
            validation_reasons.append("Path outside workspace")
        
        return validation_reasons
    
    async def _determine_validation_result(self, operation: FileOperation, 
                                         workspace_scan: WorkspaceScan,
                                         conflicts: List[str], 
                                         validation_reasons: List[str],
                                         absolute_paths_valid: bool) -> ValidationResult:
        """Determine the final validation result."""
        
        # Block if absolute paths are invalid
        if not absolute_paths_valid:
            return ValidationResult.BLOCKED
        
        # Block if critical integrity issues exist
        critical_issues = [i for i in workspace_scan.integrity_issues if i.severity == "critical"]
        if critical_issues:
            return ValidationResult.BLOCKED
        
        # Block if forbidden extensions or severe violations
        forbidden_violations = [r for r in validation_reasons if "forbidden" in r.lower()]
        if forbidden_violations:
            return ValidationResult.BLOCKED
        
        # Require confirmation if conflicts or validation issues exist
        if conflicts or validation_reasons:
            return ValidationResult.REQUIRES_CONFIRMATION
        
        # Require confirmation for workspace integrity issues
        if workspace_scan.integrity_status in [IntegrityStatus.MAJOR_ISSUES, IntegrityStatus.CRITICAL_ISSUES]:
            return ValidationResult.REQUIRES_CONFIRMATION
        
        # Approve clean operations
        return ValidationResult.APPROVED
    
    async def _generate_operation_recommendations(self, operation: FileOperation,
                                                workspace_scan: WorkspaceScan,
                                                conflicts: List[str]) -> List[str]:
        """Generate recommendations for the operation."""
        
        recommendations = []
        
        # Recommendations for conflicts
        if conflicts:
            recommendations.append("Resolve conflicts before proceeding")
            
            for conflict in conflicts:
                if "already exists" in conflict:
                    recommendations.append("Consider using a different filename or backing up existing file")
                elif "duplicate" in conflict:
                    recommendations.append("Check if file is truly needed or consolidate duplicates")
                elif "permission" in conflict:
                    recommendations.append("Check file permissions and ownership")
        
        # Recommendations for integrity issues
        if workspace_scan.integrity_status != IntegrityStatus.CLEAN:
            recommendations.append("Clean up workspace integrity issues")
            
            if workspace_scan.duplicate_files:
                recommendations.append("Remove or consolidate duplicate files")
        
        # General recommendations
        recommendations.extend([
            "Use descriptive file names",
            "Maintain consistent directory structure",
            "Keep files organized by purpose"
        ])
        
        return recommendations
    
    def get_workspace_status(self) -> Dict[str, Any]:
        """Get comprehensive workspace status."""
        
        latest_scan = self.scan_history[-1] if self.scan_history else None
        recent_operations = len([op for op in self.operation_history if time.time() - op.timestamp < 3600])
        recent_validations = len([v for v in self.validation_history if time.time() - v.timestamp < 3600])
        
        return {
            "workspace_root": str(self.workspace_root),
            "latest_scan": {
                "scan_id": latest_scan.scan_id if latest_scan else None,
                "integrity_status": latest_scan.integrity_status.value if latest_scan else "unknown",
                "total_files": latest_scan.total_files if latest_scan else 0,
                "total_directories": latest_scan.total_directories if latest_scan else 0,
                "duplicate_files": len(latest_scan.duplicate_files) if latest_scan else 0,
                "integrity_issues": len(latest_scan.integrity_issues) if latest_scan else 0
            },
            "operation_history": {
                "total_operations": len(self.operation_history),
                "recent_operations_1h": recent_operations
            },
            "validation_history": {
                "total_validations": len(self.validation_history),
                "recent_validations_1h": recent_validations,
                "approval_rate": len([v for v in self.validation_history if v.validation_result == ValidationResult.APPROVED]) / len(self.validation_history) if self.validation_history else 0
            }
        }


# Global workspace integrity manager
WORKSPACE_INTEGRITY_MANAGER = WorkspaceIntegrityManager()


async def mandatory_workspace_validation(operation: FileOperation) -> OperationValidation:
    """
    MANDATORY: Validate workspace integrity before file operations
    
    This function MUST be called before any file system modification
    according to JAEGIS Brain Protocol Suite Directive 1.6.
    """
    
    return await WORKSPACE_INTEGRITY_MANAGER.mandatory_pre_execution_scan(operation)


async def mandatory_user_confirmation(validation: OperationValidation) -> bool:
    """
    MANDATORY: Wait for user confirmation if required
    
    This function MUST be called and must wait for user confirmation
    before proceeding with file operations that require approval.
    """
    
    return await WORKSPACE_INTEGRITY_MANAGER.wait_for_user_confirmation(validation)


# Example usage
async def main():
    """Example usage of Workspace Integrity Manager."""
    
    print("🔍 JAEGIS BRAIN PROTOCOL SUITE - WORKSPACE INTEGRITY TEST")
    
    # Test file operation
    test_operation = FileOperation(
        operation_id="test_op_001",
        operation_type=FileOperationType.CREATE,
        source_path="test_file.py",
        target_path=None,
        absolute_source_path="",
        absolute_target_path=None,
        file_size_bytes=1024,
        operation_reason="Testing workspace integrity",
        timestamp=time.time()
    )
    
    # Perform validation
    validation = await WORKSPACE_INTEGRITY_MANAGER.mandatory_pre_execution_scan(test_operation)
    
    print(f"\n✅ Validation Result:")
    print(f"  Operation ID: {validation.operation_id}")
    print(f"  Result: {validation.validation_result.value}")
    print(f"  User Confirmation Required: {validation.user_confirmation_required}")
    print(f"  Absolute Paths Valid: {validation.absolute_paths_verified}")
    print(f"  Conflicts: {len(validation.conflicts_detected)}")
    
    # Test user confirmation
    if validation.user_confirmation_required:
        confirmed = await WORKSPACE_INTEGRITY_MANAGER.wait_for_user_confirmation(validation)
        print(f"  User Confirmation: {'APPROVED' if confirmed else 'DENIED'}")
    
    # Get workspace status
    status = WORKSPACE_INTEGRITY_MANAGER.get_workspace_status()
    print(f"\n📊 Workspace Status:")
    print(f"  Workspace Root: {status['workspace_root']}")
    print(f"  Integrity Status: {status['latest_scan']['integrity_status']}")
    print(f"  Total Files: {status['latest_scan']['total_files']}")
    print(f"  Duplicate Files: {status['latest_scan']['duplicate_files']}")
    print(f"  Integrity Issues: {status['latest_scan']['integrity_issues']}")


if __name__ == "__main__":
    asyncio.run(main())
