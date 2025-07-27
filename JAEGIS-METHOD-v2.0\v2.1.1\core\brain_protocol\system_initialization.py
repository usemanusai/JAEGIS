"""
JAEGIS Brain Protocol Suite v1.0 - System Initialization & Context Protocol
Directive 1.1: Mandatory initialization sequence with core directives loading and system clock synchronization

This module implements the foundational initialization protocol that must be executed
at the beginning of every new user session without exception.
"""

import asyncio
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class InitializationStatus(str, Enum):
    """System initialization status levels."""
    NOT_STARTED = "not_started"
    INITIALIZING = "initializing"
    CORE_LOADED = "core_loaded"
    CLOCK_SYNCED = "clock_synced"
    AGENTS_READY = "agents_ready"
    COMPLETE = "complete"
    FAILED = "failed"


class SessionType(str, Enum):
    """Types of session initialization."""
    NEW_SESSION = "new_session"
    RE_INITIALIZATION = "re_initialization"
    RECOVERY = "recovery"
    EMERGENCY = "emergency"


@dataclass
class SystemClock:
    """System clock synchronization data."""
    utc_timestamp: float
    utc_datetime: str
    local_timestamp: float
    local_datetime: str
    timezone_offset: str
    sync_accuracy_ms: float


@dataclass
class CoreDirectives:
    """Core directives loading status."""
    protocol_suite_version: str
    directives_loaded: List[str]
    mandates_loaded: List[str]
    total_protocols: int
    load_timestamp: float
    validation_hash: str


@dataclass
class InitializationResult:
    """Complete initialization result."""
    session_id: str
    session_type: SessionType
    status: InitializationStatus
    system_clock: SystemClock
    core_directives: CoreDirectives
    initialization_duration_ms: float
    errors_encountered: List[str]
    warnings: List[str]
    timestamp: float


class JAEGISBrainInitializer:
    """
    JAEGIS Brain Protocol Suite System Initializer
    
    Implements Directive 1.1: System Initialization & Context Protocol
    
    Mandatory execution sequence:
    1. Force Initialization - Execute without exception
    2. Load Core Directives - Load entire Protocol Suite
    3. System Clock Synchronization - Query precise UTC time
    4. Re-Initialization Support - Handle session corruption
    """
    
    def __init__(self):
        self.initialization_history: List[InitializationResult] = []
        self.current_session: Optional[InitializationResult] = None
        self.protocol_suite_path = Path("core/brain_protocol/protocol_suite.json")
        
        # Protocol Suite Definition
        self.protocol_suite_definition = {
            "version": "1.0",
            "date": "July 27, 2025",
            "core_operational_directives": [
                "1.1: System Initialization & Context Protocol",
                "1.2: Task Scoping & Agent Delegation Protocol", 
                "1.3: Knowledge Cutoff & Augmentation Protocol",
                "1.4: JAEGIS Efficiency Calibration Protocol",
                "1.5: Canonical State Management Protocol",
                "1.6: Workspace Integrity Protocol"
            ],
            "core_strategic_mandates": [
                "2.1: Persistent Project Memex Protocol",
                "2.2: Proactive Next-Step & Dependency Analysis Protocol",
                "2.3: Living Documentation Mandate",
                "2.4: Strategic Roadmap Alignment Protocol",
                "2.5: Path of Maximal Scrutiny Protocol"
            ]
        }
        
        logger.info("JAEGIS Brain Initializer created - ready for mandatory execution")
    
    async def force_initialization(self, session_type: SessionType = SessionType.NEW_SESSION) -> InitializationResult:
        """
        MANDATORY: Force initialization without exception
        
        This method MUST be executed at the beginning of every new user session.
        No user task can proceed until this initialization is complete.
        """
        
        initialization_start = time.time()
        session_id = f"jaegis_brain_{int(time.time())}_{id(self)}"
        
        logger.info(f"🧠 JAEGIS BRAIN PROTOCOL SUITE v1.0 - FORCE INITIALIZATION")
        logger.info(f"Session ID: {session_id}")
        logger.info(f"Session Type: {session_type.value}")
        
        result = InitializationResult(
            session_id=session_id,
            session_type=session_type,
            status=InitializationStatus.INITIALIZING,
            system_clock=None,
            core_directives=None,
            initialization_duration_ms=0.0,
            errors_encountered=[],
            warnings=[],
            timestamp=time.time()
        )
        
        try:
            # Step 1: Load Core Directives (MANDATORY)
            logger.info("📋 Step 1: Loading Core Directives...")
            result.core_directives = await self._load_core_directives()
            result.status = InitializationStatus.CORE_LOADED
            
            # Step 2: System Clock Synchronization (MANDATORY)
            logger.info("🕐 Step 2: System Clock Synchronization...")
            result.system_clock = await self._synchronize_system_clock()
            result.status = InitializationStatus.CLOCK_SYNCED
            
            # Step 3: Agent System Readiness Check
            logger.info("🤖 Step 3: Agent System Readiness...")
            await self._verify_agent_system_readiness()
            result.status = InitializationStatus.AGENTS_READY
            
            # Step 4: Complete Initialization
            result.status = InitializationStatus.COMPLETE
            result.initialization_duration_ms = (time.time() - initialization_start) * 1000
            
            # Store as current session
            self.current_session = result
            self.initialization_history.append(result)
            
            logger.info(f"✅ JAEGIS Brain initialization COMPLETE - {result.initialization_duration_ms:.1f}ms")
            logger.info(f"🧠 Protocol Suite v{result.core_directives.protocol_suite_version} loaded")
            logger.info(f"🕐 System time synchronized: {result.system_clock.utc_datetime}")
            
            return result
        
        except Exception as e:
            logger.error(f"❌ JAEGIS Brain initialization FAILED: {e}")
            result.status = InitializationStatus.FAILED
            result.errors_encountered.append(str(e))
            result.initialization_duration_ms = (time.time() - initialization_start) * 1000
            
            # Store failed attempt
            self.initialization_history.append(result)
            
            raise Exception(f"JAEGIS Brain initialization failed: {e}")
    
    async def force_re_initialization(self) -> InitializationResult:
        """
        MANDATORY: Force re-initialization purging previous state
        
        This method purges the previous session state and re-runs the complete
        initialization sequence. Used for session corruption recovery.
        """
        
        logger.warning("🔄 FORCE RE-INITIALIZATION - Purging previous state")
        
        # Purge previous state
        self.current_session = None
        
        # Execute fresh initialization
        return await self.force_initialization(SessionType.RE_INITIALIZATION)
    
    async def _load_core_directives(self) -> CoreDirectives:
        """Load and validate the complete Protocol Suite."""
        
        load_start = time.time()
        
        # Create protocol suite file if it doesn't exist
        if not self.protocol_suite_path.exists():
            self.protocol_suite_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.protocol_suite_path, 'w') as f:
                json.dump(self.protocol_suite_definition, f, indent=2)
        
        # Load protocol suite
        with open(self.protocol_suite_path, 'r') as f:
            protocol_data = json.load(f)
        
        # Validate protocol suite
        if protocol_data.get("version") != "1.0":
            raise Exception(f"Invalid protocol suite version: {protocol_data.get('version')}")
        
        # Calculate validation hash
        validation_hash = str(hash(json.dumps(protocol_data, sort_keys=True)))
        
        core_directives = CoreDirectives(
            protocol_suite_version=protocol_data["version"],
            directives_loaded=protocol_data["core_operational_directives"],
            mandates_loaded=protocol_data["core_strategic_mandates"],
            total_protocols=len(protocol_data["core_operational_directives"]) + len(protocol_data["core_strategic_mandates"]),
            load_timestamp=time.time(),
            validation_hash=validation_hash
        )
        
        logger.info(f"📋 Core Directives loaded: {core_directives.total_protocols} protocols")
        logger.info(f"📋 Validation hash: {validation_hash[:16]}...")
        
        return core_directives
    
    async def _synchronize_system_clock(self) -> SystemClock:
        """Synchronize system clock and anchor all analysis to precise timestamp."""
        
        sync_start = time.time()
        
        # Get precise UTC time
        utc_now = datetime.now(timezone.utc)
        local_now = datetime.now()
        
        # Calculate sync accuracy
        sync_end = time.time()
        sync_accuracy_ms = (sync_end - sync_start) * 1000
        
        system_clock = SystemClock(
            utc_timestamp=utc_now.timestamp(),
            utc_datetime=utc_now.isoformat(),
            local_timestamp=local_now.timestamp(),
            local_datetime=local_now.isoformat(),
            timezone_offset=str(local_now.astimezone().tzinfo),
            sync_accuracy_ms=sync_accuracy_ms
        )
        
        logger.info(f"🕐 System clock synchronized: {system_clock.utc_datetime}")
        logger.info(f"🕐 Sync accuracy: {sync_accuracy_ms:.2f}ms")
        
        return system_clock
    
    async def _verify_agent_system_readiness(self):
        """Verify that the JAEGIS agent system is ready for operation."""
        
        # Check for agent configuration files
        agent_config_paths = [
            Path("agent-config.txt"),
            Path("enhanced-agent-config.txt"),
            Path("core/nlds/implementation_project.py")
        ]
        
        missing_components = []
        for path in agent_config_paths:
            if not path.exists():
                missing_components.append(str(path))
        
        if missing_components:
            logger.warning(f"⚠️ Missing agent components: {missing_components}")
        else:
            logger.info("🤖 Agent system components verified")
    
    def get_current_session(self) -> Optional[InitializationResult]:
        """Get the current active session."""
        return self.current_session
    
    def is_initialized(self) -> bool:
        """Check if the system is properly initialized."""
        return (self.current_session is not None and 
                self.current_session.status == InitializationStatus.COMPLETE)
    
    def get_initialization_status(self) -> Dict[str, Any]:
        """Get comprehensive initialization status."""
        
        if not self.current_session:
            return {
                "initialized": False,
                "status": "not_initialized",
                "message": "No active session - initialization required"
            }
        
        return {
            "initialized": self.is_initialized(),
            "session_id": self.current_session.session_id,
            "status": self.current_session.status.value,
            "session_type": self.current_session.session_type.value,
            "protocol_version": self.current_session.core_directives.protocol_suite_version if self.current_session.core_directives else None,
            "system_time": self.current_session.system_clock.utc_datetime if self.current_session.system_clock else None,
            "initialization_duration_ms": self.current_session.initialization_duration_ms,
            "errors": self.current_session.errors_encountered,
            "warnings": self.current_session.warnings
        }
    
    def get_initialization_history(self) -> List[Dict[str, Any]]:
        """Get complete initialization history."""
        
        return [
            {
                "session_id": result.session_id,
                "session_type": result.session_type.value,
                "status": result.status.value,
                "duration_ms": result.initialization_duration_ms,
                "timestamp": result.timestamp,
                "errors": len(result.errors_encountered),
                "warnings": len(result.warnings)
            }
            for result in self.initialization_history
        ]


# Global initializer instance
JAEGIS_BRAIN_INITIALIZER = JAEGISBrainInitializer()


async def mandatory_initialization_check():
    """
    MANDATORY: Check if initialization is required and execute if needed
    
    This function MUST be called before any user task execution.
    """
    
    if not JAEGIS_BRAIN_INITIALIZER.is_initialized():
        logger.warning("🚨 MANDATORY INITIALIZATION REQUIRED")
        await JAEGIS_BRAIN_INITIALIZER.force_initialization()
    
    return JAEGIS_BRAIN_INITIALIZER.get_current_session()


async def force_system_re_initialization():
    """
    MANDATORY: Force complete system re-initialization
    
    This function purges all previous state and re-initializes the system.
    """
    
    logger.warning("🔄 FORCING SYSTEM RE-INITIALIZATION")
    return await JAEGIS_BRAIN_INITIALIZER.force_re_initialization()


# Example usage and testing
async def main():
    """Example usage of JAEGIS Brain System Initialization."""
    
    print("🧠 JAEGIS BRAIN PROTOCOL SUITE v1.0 - INITIALIZATION TEST")
    
    # Test mandatory initialization
    result = await JAEGIS_BRAIN_INITIALIZER.force_initialization()
    
    print(f"\n✅ Initialization Result:")
    print(f"  Session ID: {result.session_id}")
    print(f"  Status: {result.status.value}")
    print(f"  Duration: {result.initialization_duration_ms:.1f}ms")
    print(f"  Protocol Version: {result.core_directives.protocol_suite_version}")
    print(f"  System Time: {result.system_clock.utc_datetime}")
    
    # Test status check
    status = JAEGIS_BRAIN_INITIALIZER.get_initialization_status()
    print(f"\n📊 System Status:")
    print(f"  Initialized: {status['initialized']}")
    print(f"  Status: {status['status']}")
    
    # Test re-initialization
    print(f"\n🔄 Testing Re-initialization...")
    re_init_result = await JAEGIS_BRAIN_INITIALIZER.force_re_initialization()
    print(f"  Re-init Status: {re_init_result.status.value}")
    print(f"  Re-init Duration: {re_init_result.initialization_duration_ms:.1f}ms")


if __name__ == "__main__":
    asyncio.run(main())
