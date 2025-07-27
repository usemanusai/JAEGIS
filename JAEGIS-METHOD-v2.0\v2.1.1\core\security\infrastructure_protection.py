"""
JAEGIS Infrastructure Protection Commands
Lock/unlock infrastructure commands with protection protocols and audit logging
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import uuid
from pathlib import Path
import aiofiles

logger = logging.getLogger(__name__)


class ProtectionLevel(str, Enum):
    """Infrastructure protection levels."""
    NONE = "none"
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    MAXIMUM = "maximum"


class LockStatus(str, Enum):
    """Lock status for infrastructure components."""
    UNLOCKED = "unlocked"
    LOCKED = "locked"
    EMERGENCY_LOCKED = "emergency_locked"
    MAINTENANCE_LOCKED = "maintenance_locked"


class ComponentType(str, Enum):
    """Types of infrastructure components."""
    AGENT_SQUAD = "agent_squad"
    CORE_SYSTEM = "core_system"
    DATABASE = "database"
    API_ENDPOINT = "api_endpoint"
    CONFIGURATION = "configuration"
    SECURITY_MODULE = "security_module"


class OperationType(str, Enum):
    """Types of protection operations."""
    LOCK = "lock"
    UNLOCK = "unlock"
    EMERGENCY_LOCK = "emergency_lock"
    STATUS_CHECK = "status_check"
    AUDIT_LOG = "audit_log"


@dataclass
class ProtectedComponent:
    """Protected infrastructure component."""
    component_id: str
    component_type: ComponentType
    name: str
    description: str
    protection_level: ProtectionLevel
    lock_status: LockStatus
    locked_by: Optional[str]
    locked_at: Optional[float]
    unlock_key: Optional[str]
    dependencies: List[str]
    critical: bool


@dataclass
class ProtectionOperation:
    """Protection operation record."""
    operation_id: str
    operation_type: OperationType
    component_id: str
    user_id: str
    timestamp: float
    success: bool
    reason: str
    previous_status: Optional[LockStatus]
    new_status: Optional[LockStatus]
    authorization_level: str
    ip_address: Optional[str]
    session_id: Optional[str]


@dataclass
class AuditEntry:
    """Audit log entry."""
    entry_id: str
    timestamp: float
    user_id: str
    operation: str
    component_id: str
    details: Dict[str, Any]
    risk_level: str
    authorized: bool


class InfrastructureProtection:
    """
    JAEGIS Infrastructure Protection System
    
    Provides comprehensive protection for critical infrastructure components
    with lock/unlock commands, audit logging, and security protocols.
    """
    
    def __init__(self):
        self.components: Dict[str, ProtectedComponent] = {}
        self.operations: List[ProtectionOperation] = []
        self.audit_log: List[AuditEntry] = []
        
        # Configuration
        self.config = {
            "max_lock_duration": 86400,  # 24 hours
            "emergency_contacts": [],
            "audit_retention_days": 90,
            "require_2fa": True,
            "auto_unlock_timeout": 3600,  # 1 hour
            "critical_component_protection": True,
            "audit_log_file": "logs/infrastructure_audit.log"
        }
        
        # Initialize protected components
        self._initialize_protected_components()
        
        # Start background tasks
        asyncio.create_task(self._audit_log_manager())
        asyncio.create_task(self._auto_unlock_monitor())
        
        logger.info("Infrastructure Protection System initialized")
    
    def _initialize_protected_components(self):
        """Initialize protected infrastructure components."""
        
        # Core system components
        core_components = [
            {
                "component_id": "jaegis_master_orchestrator",
                "component_type": ComponentType.CORE_SYSTEM,
                "name": "JAEGIS Master Orchestrator",
                "description": "Main orchestration system for all JAEGIS agents",
                "protection_level": ProtectionLevel.MAXIMUM,
                "critical": True,
                "dependencies": []
            },
            {
                "component_id": "nlds_interface",
                "component_type": ComponentType.CORE_SYSTEM,
                "name": "N.L.D.S. Interface",
                "description": "Natural Language Detection System - Tier 0 interface",
                "protection_level": ProtectionLevel.HIGH,
                "critical": True,
                "dependencies": ["jaegis_master_orchestrator"]
            },
            {
                "component_id": "amasiap_protocol",
                "component_type": ComponentType.CORE_SYSTEM,
                "name": "A.M.A.S.I.A.P. Protocol",
                "description": "Always Modify And Send Input Automatically Protocol",
                "protection_level": ProtectionLevel.HIGH,
                "critical": False,
                "dependencies": ["nlds_interface"]
            }
        ]
        
        # Agent squad components
        squad_components = [
            {
                "component_id": "iuas_squad",
                "component_type": ComponentType.AGENT_SQUAD,
                "name": "Internal Updates Agent Squad",
                "description": "20-agent maintenance squad for system updates",
                "protection_level": ProtectionLevel.STANDARD,
                "critical": False,
                "dependencies": ["jaegis_master_orchestrator"]
            },
            {
                "component_id": "garas_squad",
                "component_type": ComponentType.AGENT_SQUAD,
                "name": "Gaps Analysis and Resolution Agent Squad",
                "description": "40-agent squad for gap analysis and resolution",
                "protection_level": ProtectionLevel.STANDARD,
                "critical": False,
                "dependencies": ["jaegis_master_orchestrator"]
            }
        ]
        
        # Security components
        security_components = [
            {
                "component_id": "auth_system",
                "component_type": ComponentType.SECURITY_MODULE,
                "name": "Authentication System",
                "description": "JWT-based authentication and authorization",
                "protection_level": ProtectionLevel.MAXIMUM,
                "critical": True,
                "dependencies": []
            },
            {
                "component_id": "api_gateway",
                "component_type": ComponentType.API_ENDPOINT,
                "name": "API Gateway",
                "description": "Main API gateway for external access",
                "protection_level": ProtectionLevel.HIGH,
                "critical": True,
                "dependencies": ["auth_system"]
            }
        ]
        
        # Database components
        database_components = [
            {
                "component_id": "user_profiles_db",
                "component_type": ComponentType.DATABASE,
                "name": "User Profiles Database",
                "description": "Encrypted user profile storage",
                "protection_level": ProtectionLevel.MAXIMUM,
                "critical": True,
                "dependencies": ["auth_system"]
            },
            {
                "component_id": "conversation_context_db",
                "component_type": ComponentType.DATABASE,
                "name": "Conversation Context Database",
                "description": "24-hour session persistence storage",
                "protection_level": ProtectionLevel.HIGH,
                "critical": False,
                "dependencies": ["user_profiles_db"]
            }
        ]
        
        # Create protected components
        all_components = core_components + squad_components + security_components + database_components
        
        for comp_config in all_components:
            component = ProtectedComponent(
                component_id=comp_config["component_id"],
                component_type=comp_config["component_type"],
                name=comp_config["name"],
                description=comp_config["description"],
                protection_level=comp_config["protection_level"],
                lock_status=LockStatus.UNLOCKED,
                locked_by=None,
                locked_at=None,
                unlock_key=None,
                dependencies=comp_config["dependencies"],
                critical=comp_config["critical"]
            )
            
            self.components[component.component_id] = component
        
        logger.info(f"Initialized {len(self.components)} protected components")
    
    async def lock_component(self, 
                           component_id: str,
                           user_id: str,
                           reason: str,
                           lock_type: LockStatus = LockStatus.LOCKED,
                           session_id: Optional[str] = None,
                           ip_address: Optional[str] = None) -> Dict[str, Any]:
        """Lock an infrastructure component."""
        
        operation_id = str(uuid.uuid4())
        timestamp = time.time()
        
        try:
            # Validate component exists
            if component_id not in self.components:
                return {
                    "success": False,
                    "error": f"Component {component_id} not found",
                    "operation_id": operation_id
                }
            
            component = self.components[component_id]
            
            # Check if already locked
            if component.lock_status != LockStatus.UNLOCKED:
                return {
                    "success": False,
                    "error": f"Component {component_id} is already locked",
                    "current_status": component.lock_status.value,
                    "locked_by": component.locked_by,
                    "operation_id": operation_id
                }
            
            # Check authorization for critical components
            if component.critical and not await self._authorize_critical_operation(user_id, component_id, "lock"):
                return {
                    "success": False,
                    "error": "Insufficient authorization for critical component",
                    "operation_id": operation_id
                }
            
            # Check dependencies
            dependency_issues = await self._check_dependencies(component_id, "lock")
            if dependency_issues:
                return {
                    "success": False,
                    "error": "Dependency constraints prevent locking",
                    "dependency_issues": dependency_issues,
                    "operation_id": operation_id
                }
            
            # Generate unlock key
            unlock_key = hashlib.sha256(f"{component_id}{user_id}{timestamp}".encode()).hexdigest()
            
            # Update component status
            previous_status = component.lock_status
            component.lock_status = lock_type
            component.locked_by = user_id
            component.locked_at = timestamp
            component.unlock_key = unlock_key
            
            # Record operation
            operation = ProtectionOperation(
                operation_id=operation_id,
                operation_type=OperationType.LOCK,
                component_id=component_id,
                user_id=user_id,
                timestamp=timestamp,
                success=True,
                reason=reason,
                previous_status=previous_status,
                new_status=lock_type,
                authorization_level="authorized",
                ip_address=ip_address,
                session_id=session_id
            )
            
            self.operations.append(operation)
            
            # Create audit entry
            await self._create_audit_entry(
                user_id=user_id,
                operation="LOCK_COMPONENT",
                component_id=component_id,
                details={
                    "reason": reason,
                    "lock_type": lock_type.value,
                    "unlock_key": unlock_key[:8] + "...",  # Partial key for audit
                    "ip_address": ip_address,
                    "session_id": session_id
                },
                risk_level="HIGH" if component.critical else "MEDIUM"
            )
            
            logger.info(f"Component {component_id} locked by {user_id}: {reason}")
            
            return {
                "success": True,
                "component_id": component_id,
                "lock_status": lock_type.value,
                "unlock_key": unlock_key,
                "locked_at": timestamp,
                "operation_id": operation_id,
                "message": f"Component {component.name} successfully locked"
            }
            
        except Exception as e:
            error_message = f"Failed to lock component {component_id}: {str(e)}"
            logger.error(error_message)
            
            # Record failed operation
            operation = ProtectionOperation(
                operation_id=operation_id,
                operation_type=OperationType.LOCK,
                component_id=component_id,
                user_id=user_id,
                timestamp=timestamp,
                success=False,
                reason=reason,
                previous_status=None,
                new_status=None,
                authorization_level="error",
                ip_address=ip_address,
                session_id=session_id
            )
            
            self.operations.append(operation)
            
            return {
                "success": False,
                "error": error_message,
                "operation_id": operation_id
            }
    
    async def unlock_component(self, 
                             component_id: str,
                             user_id: str,
                             unlock_key: str,
                             reason: str,
                             session_id: Optional[str] = None,
                             ip_address: Optional[str] = None) -> Dict[str, Any]:
        """Unlock an infrastructure component."""
        
        operation_id = str(uuid.uuid4())
        timestamp = time.time()
        
        try:
            # Validate component exists
            if component_id not in self.components:
                return {
                    "success": False,
                    "error": f"Component {component_id} not found",
                    "operation_id": operation_id
                }
            
            component = self.components[component_id]
            
            # Check if component is locked
            if component.lock_status == LockStatus.UNLOCKED:
                return {
                    "success": False,
                    "error": f"Component {component_id} is not locked",
                    "operation_id": operation_id
                }
            
            # Validate unlock key
            if component.unlock_key != unlock_key:
                await self._create_audit_entry(
                    user_id=user_id,
                    operation="UNLOCK_ATTEMPT_FAILED",
                    component_id=component_id,
                    details={
                        "reason": "Invalid unlock key",
                        "ip_address": ip_address,
                        "session_id": session_id
                    },
                    risk_level="HIGH"
                )
                
                return {
                    "success": False,
                    "error": "Invalid unlock key",
                    "operation_id": operation_id
                }
            
            # Check authorization for critical components
            if component.critical and not await self._authorize_critical_operation(user_id, component_id, "unlock"):
                return {
                    "success": False,
                    "error": "Insufficient authorization for critical component",
                    "operation_id": operation_id
                }
            
            # Update component status
            previous_status = component.lock_status
            component.lock_status = LockStatus.UNLOCKED
            component.locked_by = None
            component.locked_at = None
            component.unlock_key = None
            
            # Record operation
            operation = ProtectionOperation(
                operation_id=operation_id,
                operation_type=OperationType.UNLOCK,
                component_id=component_id,
                user_id=user_id,
                timestamp=timestamp,
                success=True,
                reason=reason,
                previous_status=previous_status,
                new_status=LockStatus.UNLOCKED,
                authorization_level="authorized",
                ip_address=ip_address,
                session_id=session_id
            )
            
            self.operations.append(operation)
            
            # Create audit entry
            await self._create_audit_entry(
                user_id=user_id,
                operation="UNLOCK_COMPONENT",
                component_id=component_id,
                details={
                    "reason": reason,
                    "previous_status": previous_status.value,
                    "ip_address": ip_address,
                    "session_id": session_id
                },
                risk_level="HIGH" if component.critical else "MEDIUM"
            )
            
            logger.info(f"Component {component_id} unlocked by {user_id}: {reason}")
            
            return {
                "success": True,
                "component_id": component_id,
                "lock_status": LockStatus.UNLOCKED.value,
                "unlocked_at": timestamp,
                "operation_id": operation_id,
                "message": f"Component {component.name} successfully unlocked"
            }
            
        except Exception as e:
            error_message = f"Failed to unlock component {component_id}: {str(e)}"
            logger.error(error_message)
            
            return {
                "success": False,
                "error": error_message,
                "operation_id": operation_id
            }
    
    async def emergency_lock_all(self, 
                               user_id: str,
                               reason: str,
                               session_id: Optional[str] = None,
                               ip_address: Optional[str] = None) -> Dict[str, Any]:
        """Emergency lock all critical components."""
        
        operation_id = str(uuid.uuid4())
        timestamp = time.time()
        
        try:
            # Check emergency authorization
            if not await self._authorize_emergency_operation(user_id):
                return {
                    "success": False,
                    "error": "Insufficient authorization for emergency lock",
                    "operation_id": operation_id
                }
            
            locked_components = []
            failed_components = []
            
            # Lock all critical components
            for component_id, component in self.components.items():
                if component.critical and component.lock_status == LockStatus.UNLOCKED:
                    try:
                        result = await self.lock_component(
                            component_id=component_id,
                            user_id=user_id,
                            reason=f"EMERGENCY: {reason}",
                            lock_type=LockStatus.EMERGENCY_LOCKED,
                            session_id=session_id,
                            ip_address=ip_address
                        )
                        
                        if result["success"]:
                            locked_components.append(component_id)
                        else:
                            failed_components.append({
                                "component_id": component_id,
                                "error": result["error"]
                            })
                    
                    except Exception as e:
                        failed_components.append({
                            "component_id": component_id,
                            "error": str(e)
                        })
            
            # Create emergency audit entry
            await self._create_audit_entry(
                user_id=user_id,
                operation="EMERGENCY_LOCK_ALL",
                component_id="ALL_CRITICAL",
                details={
                    "reason": reason,
                    "locked_components": locked_components,
                    "failed_components": failed_components,
                    "ip_address": ip_address,
                    "session_id": session_id
                },
                risk_level="CRITICAL"
            )
            
            logger.critical(f"Emergency lock executed by {user_id}: {reason}")
            
            return {
                "success": len(failed_components) == 0,
                "locked_components": locked_components,
                "failed_components": failed_components,
                "operation_id": operation_id,
                "message": f"Emergency lock completed: {len(locked_components)} components locked"
            }
            
        except Exception as e:
            error_message = f"Emergency lock failed: {str(e)}"
            logger.error(error_message)
            
            return {
                "success": False,
                "error": error_message,
                "operation_id": operation_id
            }
    
    async def get_component_status(self, component_id: str) -> Dict[str, Any]:
        """Get status of a protected component."""
        
        if component_id not in self.components:
            return {
                "success": False,
                "error": f"Component {component_id} not found"
            }
        
        component = self.components[component_id]
        
        return {
            "success": True,
            "component_id": component_id,
            "name": component.name,
            "description": component.description,
            "component_type": component.component_type.value,
            "protection_level": component.protection_level.value,
            "lock_status": component.lock_status.value,
            "locked_by": component.locked_by,
            "locked_at": component.locked_at,
            "critical": component.critical,
            "dependencies": component.dependencies
        }
    
    async def get_all_components_status(self) -> Dict[str, Any]:
        """Get status of all protected components."""
        
        components_status = {}
        
        for component_id, component in self.components.items():
            components_status[component_id] = {
                "name": component.name,
                "component_type": component.component_type.value,
                "protection_level": component.protection_level.value,
                "lock_status": component.lock_status.value,
                "locked_by": component.locked_by,
                "locked_at": component.locked_at,
                "critical": component.critical
            }
        
        # Calculate summary statistics
        total_components = len(self.components)
        locked_components = len([c for c in self.components.values() if c.lock_status != LockStatus.UNLOCKED])
        critical_components = len([c for c in self.components.values() if c.critical])
        critical_locked = len([c for c in self.components.values() if c.critical and c.lock_status != LockStatus.UNLOCKED])
        
        return {
            "success": True,
            "components": components_status,
            "summary": {
                "total_components": total_components,
                "locked_components": locked_components,
                "critical_components": critical_components,
                "critical_locked": critical_locked,
                "lock_percentage": (locked_components / total_components * 100) if total_components > 0 else 0
            }
        }
    
    async def _authorize_critical_operation(self, user_id: str, component_id: str, operation: str) -> bool:
        """Authorize operations on critical components."""
        
        # In a real implementation, this would check:
        # - User permissions and roles
        # - Multi-factor authentication
        # - Time-based restrictions
        # - Approval workflows
        
        # For now, simulate authorization check
        return True  # Placeholder - implement actual authorization logic
    
    async def _authorize_emergency_operation(self, user_id: str) -> bool:
        """Authorize emergency operations."""
        
        # Emergency operations require highest level authorization
        # In real implementation, would check emergency contact list
        return True  # Placeholder - implement actual emergency authorization
    
    async def _check_dependencies(self, component_id: str, operation: str) -> List[str]:
        """Check component dependencies for operation."""
        
        issues = []
        component = self.components[component_id]
        
        if operation == "lock":
            # Check if any dependent components would be affected
            for other_id, other_component in self.components.items():
                if component_id in other_component.dependencies and other_component.lock_status == LockStatus.UNLOCKED:
                    issues.append(f"Component {other_id} depends on {component_id}")
        
        return issues
    
    async def _create_audit_entry(self, user_id: str, operation: str, component_id: str, 
                                details: Dict[str, Any], risk_level: str):
        """Create audit log entry."""
        
        entry = AuditEntry(
            entry_id=str(uuid.uuid4()),
            timestamp=time.time(),
            user_id=user_id,
            operation=operation,
            component_id=component_id,
            details=details,
            risk_level=risk_level,
            authorized=True  # Set based on actual authorization check
        )
        
        self.audit_log.append(entry)
        
        # Write to audit log file
        await self._write_audit_log(entry)
    
    async def _write_audit_log(self, entry: AuditEntry):
        """Write audit entry to log file."""
        
        try:
            log_file = Path(self.config["audit_log_file"])
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            log_entry = {
                "timestamp": entry.timestamp,
                "entry_id": entry.entry_id,
                "user_id": entry.user_id,
                "operation": entry.operation,
                "component_id": entry.component_id,
                "details": entry.details,
                "risk_level": entry.risk_level,
                "authorized": entry.authorized
            }
            
            async with aiofiles.open(log_file, "a") as f:
                await f.write(json.dumps(log_entry) + "\n")
        
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
    
    async def _audit_log_manager(self):
        """Manage audit log retention and cleanup."""
        
        while True:
            try:
                current_time = time.time()
                retention_cutoff = current_time - (self.config["audit_retention_days"] * 86400)
                
                # Remove old audit entries
                self.audit_log = [
                    entry for entry in self.audit_log
                    if entry.timestamp > retention_cutoff
                ]
                
                await asyncio.sleep(86400)  # Check daily
                
            except Exception as e:
                logger.error(f"Audit log manager error: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour on error
    
    async def _auto_unlock_monitor(self):
        """Monitor for automatic unlock conditions."""
        
        while True:
            try:
                current_time = time.time()
                
                for component in self.components.values():
                    if (component.lock_status != LockStatus.UNLOCKED and 
                        component.locked_at and
                        current_time - component.locked_at > self.config["auto_unlock_timeout"]):
                        
                        # Auto-unlock non-emergency locks after timeout
                        if component.lock_status != LockStatus.EMERGENCY_LOCKED:
                            logger.info(f"Auto-unlocking component {component.component_id} after timeout")
                            
                            component.lock_status = LockStatus.UNLOCKED
                            component.locked_by = None
                            component.locked_at = None
                            component.unlock_key = None
                            
                            await self._create_audit_entry(
                                user_id="SYSTEM",
                                operation="AUTO_UNLOCK",
                                component_id=component.component_id,
                                details={"reason": "Timeout exceeded"},
                                risk_level="MEDIUM"
                            )
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Auto-unlock monitor error: {e}")
                await asyncio.sleep(600)  # Wait 10 minutes on error


# Example usage
async def main():
    """Example usage of Infrastructure Protection System."""
    
    protection = InfrastructureProtection()
    
    # Lock a component
    result = await protection.lock_component(
        component_id="nlds_interface",
        user_id="admin_user",
        reason="Maintenance update",
        session_id="session_123",
        ip_address="192.168.1.100"
    )
    
    print(f"Lock result: {result}")
    
    if result["success"]:
        unlock_key = result["unlock_key"]
        
        # Check status
        status = await protection.get_component_status("nlds_interface")
        print(f"Component status: {status}")
        
        # Unlock component
        unlock_result = await protection.unlock_component(
            component_id="nlds_interface",
            user_id="admin_user",
            unlock_key=unlock_key,
            reason="Maintenance completed",
            session_id="session_123",
            ip_address="192.168.1.100"
        )
        
        print(f"Unlock result: {unlock_result}")
    
    # Get all components status
    all_status = await protection.get_all_components_status()
    print(f"All components: {all_status['summary']}")


if __name__ == "__main__":
    asyncio.run(main())
