# 🔧 **JAEGIS API Reference**

## **Overview**
Comprehensive API documentation for the JAEGIS Enhanced Agent System v2.2, including all classes, methods, command interfaces, and integration endpoints.

## **📋 Table of Contents**

- [Core Classes](#core-classes)
- [Agent Management](#agent-management)
- [Squad Operations](#squad-operations)
- [Command Interface](#command-interface)
- [Configuration Management](#configuration-management)
- [Security & Protection](#security--protection)
- [GitHub Integration](#github-integration)
- [OpenRouter.ai Integration](#openrouterai-integration)
- [Monitoring & Analytics](#monitoring--analytics)
- [Error Handling](#error-handling)

---

## **🎯 Core Classes**

### **JAEGISOrchestrator**
Main orchestrator class for the JAEGIS system.

```python
class JAEGISOrchestrator:
    """
    Main orchestrator for JAEGIS Enhanced Agent System v2.2
    
    Manages 128-agent ecosystem across 6-tier architecture with
    advanced squad coordination and cross-system integration.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize JAEGIS orchestrator.
        
        Args:
            config: Optional configuration dictionary
        """
        
    def activate_mode(self, mode: int) -> bool:
        """
        Activate operational mode.
        
        Args:
            mode: Mode number (1-5)
                1: Documentation Mode (3 agents)
                2: Standard Development (24 agents)
                3: Enhanced Development (68 agents)
                4: AI System Mode (variable agents)
                5: Agent Creator Mode (128 agents)
                
        Returns:
            bool: True if activation successful
            
        Raises:
            ModeActivationError: If mode activation fails
        """
        
    def get_system_status(self) -> SystemStatus:
        """
        Get comprehensive system status.
        
        Returns:
            SystemStatus: Current system state and metrics
        """
        
    def execute_task(self, task_config: TaskConfig) -> TaskResult:
        """
        Execute complex task with multi-agent coordination.
        
        Args:
            task_config: Task configuration and parameters
            
        Returns:
            TaskResult: Execution results and metrics
        """
```

### **Agent**
Base agent class for all JAEGIS agents.

```python
class Agent:
    """
    Base class for all JAEGIS agents.
    
    Provides core functionality for agent communication,
    task execution, and performance monitoring.
    """
    
    def __init__(self, name: str, priority: int, capabilities: List[str]):
        """
        Initialize agent.
        
        Args:
            name: Agent name and identifier
            priority: Agent priority (1-10, 10 highest)
            capabilities: List of agent capabilities
        """
        
    def execute(self, task: Task) -> TaskResult:
        """
        Execute assigned task.
        
        Args:
            task: Task to execute
            
        Returns:
            TaskResult: Execution results
        """
        
    def communicate(self, target_agent: str, message: Message) -> Response:
        """
        Communicate with another agent.
        
        Args:
            target_agent: Target agent identifier
            message: Message to send
            
        Returns:
            Response: Agent response
        """
```

---

## **👥 Agent Management**

### **AgentManager**
Manages agent lifecycle and coordination.

```python
class AgentManager:
    """Agent lifecycle and coordination management."""
    
    def activate_agent(self, agent_name: str) -> bool:
        """
        Activate specific agent.
        
        Args:
            agent_name: Name of agent to activate
            
        Returns:
            bool: True if activation successful
        """
        
    def deactivate_agent(self, agent_name: str) -> bool:
        """
        Deactivate specific agent.
        
        Args:
            agent_name: Name of agent to deactivate
            
        Returns:
            bool: True if deactivation successful
        """
        
    def get_agent_status(self, agent_name: str) -> AgentStatus:
        """
        Get agent status and metrics.
        
        Args:
            agent_name: Name of agent
            
        Returns:
            AgentStatus: Current agent status
        """
        
    def list_agents(self, tier: int = None) -> List[AgentInfo]:
        """
        List all agents or agents in specific tier.
        
        Args:
            tier: Optional tier filter (1-6)
            
        Returns:
            List[AgentInfo]: Agent information list
        """
```

---

## **🏗️ Squad Operations**

### **SquadManager**
Manages squad operations and coordination.

```python
class SquadManager:
    """Squad operations and coordination management."""
    
    def activate_squad(self, squad_name: str) -> bool:
        """
        Activate specific squad.
        
        Args:
            squad_name: Name of squad to activate
                - development-squad
                - quality-squad
                - business-squad
                - process-squad
                - content-squad
                - system-squad
                - task-management-squad
                - agent-builder-squad
                - system-coherence-squad
                - temporal-intelligence-squad
                - iuas-squad
                - garas-squad
                
        Returns:
            bool: True if activation successful
        """
        
    def coordinate_squads(self, squad_list: List[str]) -> CoordinationResult:
        """
        Coordinate multiple squads for complex operations.
        
        Args:
            squad_list: List of squad names to coordinate
            
        Returns:
            CoordinationResult: Coordination results and metrics
        """
        
    def get_squad_performance(self, squad_name: str) -> SquadMetrics:
        """
        Get squad performance metrics.
        
        Args:
            squad_name: Name of squad
            
        Returns:
            SquadMetrics: Performance data and analytics
        """
```

---

## **⚡ Command Interface**

### **CommandProcessor**
Processes and executes JAEGIS commands.

```python
class CommandProcessor:
    """Command processing and execution."""
    
    def execute_command(self, command: str, params: Dict = None) -> CommandResult:
        """
        Execute JAEGIS command.
        
        Args:
            command: Command string (e.g., '/jaegis-status')
            params: Optional command parameters
            
        Returns:
            CommandResult: Command execution results
        """
        
    def validate_command(self, command: str) -> bool:
        """
        Validate command syntax and permissions.
        
        Args:
            command: Command to validate
            
        Returns:
            bool: True if command is valid
        """
        
    def get_command_help(self, command: str = None) -> str:
        """
        Get command help information.
        
        Args:
            command: Optional specific command
            
        Returns:
            str: Help information
        """
```

### **Core Commands**

#### **Mode Selection Commands**
```python
# Mode activation
jaegis.execute_command('/mode-agent-creator')  # Activate Mode 5
jaegis.execute_command('/mode-enhanced')        # Activate Mode 3
jaegis.execute_command('/mode-standard')        # Activate Mode 2

# Mode information
jaegis.execute_command('/mode-select')          # Show mode menu
```

#### **Squad Management Commands**
```python
# Squad operations
jaegis.execute_command('/squad-activate', {'name': 'development-squad'})
jaegis.execute_command('/squad-status', {'name': 'garas-squad'})
jaegis.execute_command('/squad-list')

# Multi-squad coordination
jaegis.execute_command('/multi-squad-activate', {
    'squads': ['development-squad', 'quality-squad', 'garas-squad']
})
```

#### **Infrastructure Protection Commands**
```python
# Protection control
jaegis.execute_command('/jaegis-lock-infrastructure')
jaegis.execute_command('/jaegis-unlock-infrastructure')
jaegis.execute_command('/jaegis-infrastructure-status')

# Security operations
jaegis.execute_command('/jaegis-security-scan')
jaegis.execute_command('/jaegis-protection-audit')
```

---

## **⚙️ Configuration Management**

### **ConfigManager**
Manages system configuration and settings.

```python
class ConfigManager:
    """Configuration management and dynamic loading."""
    
    def load_config(self, config_path: str) -> bool:
        """
        Load configuration from file or URL.
        
        Args:
            config_path: Path to configuration file or GitHub URL
            
        Returns:
            bool: True if loading successful
        """
        
    def update_setting(self, key: str, value: Any) -> bool:
        """
        Update specific configuration setting.
        
        Args:
            key: Configuration key
            value: New value
            
        Returns:
            bool: True if update successful
        """
        
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get configuration setting value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
```

---

## **🛡️ Security & Protection**

### **SecurityManager**
Manages security protocols and protection mechanisms.

```python
class SecurityManager:
    """Security and protection management."""
    
    def lock_infrastructure(self) -> bool:
        """
        Activate infrastructure protection.
        
        Returns:
            bool: True if lock successful
        """
        
    def unlock_infrastructure(self) -> bool:
        """
        Deactivate infrastructure protection.
        
        Returns:
            bool: True if unlock successful
        """
        
    def scan_security(self) -> SecurityReport:
        """
        Execute comprehensive security scan.
        
        Returns:
            SecurityReport: Security analysis results
        """
        
    def generate_audit(self) -> AuditReport:
        """
        Generate comprehensive audit report.
        
        Returns:
            AuditReport: Audit trail and analysis
        """
```

---

## **🔗 GitHub Integration**

### **GitHubManager**
Manages GitHub integration and synchronization.

```python
class GitHubManager:
    """GitHub integration and synchronization."""
    
    def start_sync(self) -> bool:
        """
        Start automated GitHub synchronization.
        
        Returns:
            bool: True if sync started successfully
        """
        
    def stop_sync(self) -> bool:
        """
        Stop automated GitHub synchronization.
        
        Returns:
            bool: True if sync stopped successfully
        """
        
    def get_sync_status(self) -> SyncStatus:
        """
        Get synchronization status and metrics.
        
        Returns:
            SyncStatus: Current sync state and statistics
        """
        
    def fetch_resource(self, resource_path: str) -> str:
        """
        Fetch resource from GitHub repository.
        
        Args:
            resource_path: Path to resource in repository
            
        Returns:
            str: Resource content
        """
```

---

## **🤖 OpenRouter.ai Integration**

### **OpenRouterManager**
Manages OpenRouter.ai integration and load balancing.

```python
class OpenRouterManager:
    """OpenRouter.ai integration and management."""
    
    def get_key_pool_status(self) -> KeyPoolStatus:
        """
        Get API key pool status and metrics.
        
        Returns:
            KeyPoolStatus: Key pool statistics
        """
        
    def optimize_load_balancing(self) -> bool:
        """
        Optimize API key load balancing.
        
        Returns:
            bool: True if optimization successful
        """
        
    def test_failover(self) -> FailoverResult:
        """
        Test failover mechanisms.
        
        Returns:
            FailoverResult: Failover test results
        """
```

---

## **📊 Monitoring & Analytics**

### **MonitoringManager**
Manages system monitoring and analytics.

```python
class MonitoringManager:
    """System monitoring and analytics."""
    
    def get_system_metrics(self) -> SystemMetrics:
        """
        Get comprehensive system metrics.
        
        Returns:
            SystemMetrics: Current system performance data
        """
        
    def get_agent_analytics(self, agent_name: str = None) -> AgentAnalytics:
        """
        Get agent performance analytics.
        
        Args:
            agent_name: Optional specific agent name
            
        Returns:
            AgentAnalytics: Agent performance data
        """
        
    def generate_report(self, report_type: str) -> Report:
        """
        Generate system report.
        
        Args:
            report_type: Type of report ('performance', 'security', 'usage')
            
        Returns:
            Report: Generated report
        """
```

---

## **🚨 Error Handling**

### **Exception Classes**

```python
class JAEGISException(Exception):
    """Base exception for JAEGIS system."""
    pass

class ModeActivationError(JAEGISException):
    """Raised when mode activation fails."""
    pass

class SquadActivationError(JAEGISException):
    """Raised when squad activation fails."""
    pass

class SecurityViolationError(JAEGISException):
    """Raised when security violation detected."""
    pass

class ConfigurationError(JAEGISException):
    """Raised when configuration error occurs."""
    pass

class GitHubSyncError(JAEGISException):
    """Raised when GitHub sync fails."""
    pass
```

---

## **📚 Usage Examples**

### **Basic System Initialization**
```python
from jaegis import JAEGISOrchestrator

# Initialize JAEGIS system
jaegis = JAEGISOrchestrator()

# Activate Agent Creator Mode (128 agents)
jaegis.activate_mode(5)

# Check system status
status = jaegis.get_system_status()
print(f"System Status: {status.state}")
print(f"Active Agents: {status.active_agents}")
```

### **Squad Coordination**
```python
# Activate multiple squads
jaegis.activate_squad('development-squad')
jaegis.activate_squad('quality-squad')
jaegis.activate_squad('garas-squad')

# Execute coordinated task
task_config = {
    'type': 'documentation-enhancement',
    'squads': ['content-squad', 'garas-squad'],
    'target': 'github-repository'
}

result = jaegis.execute_task(task_config)
print(f"Task Result: {result.status}")
```

### **Security Operations**
```python
# Lock infrastructure for protection
jaegis.execute_command('/jaegis-lock-infrastructure')

# Execute security scan
scan_result = jaegis.execute_command('/jaegis-security-scan')

# Generate audit report
audit = jaegis.execute_command('/jaegis-protection-audit')
```

---

## **📞 Support**

For API support and questions:
- 📧 **Email**: api-support@jaegis.ai
- 💬 **Discussions**: [GitHub Discussions](https://github.com/usemanusai/JAEGIS/discussions)
- 📖 **Documentation**: [docs.jaegis.ai](https://docs.jaegis.ai)

---

*Last Updated: July 26, 2025*  
*JAEGIS Enhanced Agent System v2.2*
