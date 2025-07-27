"""
JAEGIS Configuration Management System - Enhanced Command System
Command system with configuration-specific commands and enhanced functionality
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re

from ..core.config_engine import ConfigurationEngine
from ..core.security import SecurityManager, Permission
from ..agents.frequency_controller import FrequencyControllerAgent
from ..agents.protocol_manager import ProtocolManagerAgent
from ..agents.qa_rules_manager import QualityAssuranceRulesManager
from ..agents.suggestions_engine import IntelligentSuggestionsEngine, ProjectContext, ProjectType, UserExpertiseLevel, ProjectPhase
from ..ui.statistics_dashboard import RealTimeStatisticsDashboard

logger = logging.getLogger(__name__)

class CommandCategory(Enum):
    """Categories of commands"""
    CONFIGURATION = "configuration"
    FREQUENCY = "frequency"
    PROTOCOL = "protocol"
    AGENT = "agent"
    SYSTEM = "system"
    HELP = "help"

@dataclass
class Command:
    """Command definition"""
    name: str
    description: str
    category: CommandCategory
    handler: Callable
    permissions: List[Permission] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    parameters: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    hidden: bool = False

@dataclass
class CommandResult:
    """Result of command execution"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)

class EnhancedCommandSystem:
    """Enhanced command system for JAEGIS configuration management"""
    
    def __init__(self, config_engine: ConfigurationEngine,
                 security_manager: SecurityManager,
                 frequency_controller: FrequencyControllerAgent,
                 protocol_manager: ProtocolManagerAgent,
                 qa_rules_manager: QualityAssuranceRulesManager,
                 suggestions_engine: IntelligentSuggestionsEngine,
                 dashboard: RealTimeStatisticsDashboard):
        
        self.config_engine = config_engine
        self.security_manager = security_manager
        self.frequency_controller = frequency_controller
        self.protocol_manager = protocol_manager
        self.qa_rules_manager = qa_rules_manager
        self.suggestions_engine = suggestions_engine
        self.dashboard = dashboard
        
        # Command registry
        self.commands: Dict[str, Command] = {}
        self.aliases: Dict[str, str] = {}
        
        # Command history
        self.command_history: List[Dict[str, Any]] = []
        
        # Initialize commands
        self._register_commands()
        
        logger.info("Enhanced Command System initialized")
    
    def _register_commands(self):
        """Register all available commands"""
        
        # Help commands
        self._register_command(Command(
            name="help",
            description="Show available commands and usage information",
            category=CommandCategory.HELP,
            handler=self._cmd_help,
            aliases=["h", "?"],
            examples=["/help", "/help config-frequency"]
        ))
        
        # Configuration commands
        self._register_command(Command(
            name="config-frequency",
            description="Open frequency control menu for parameter adjustment",
            category=CommandCategory.FREQUENCY,
            handler=self._cmd_config_frequency,
            permissions=[Permission.READ_CONFIG],
            examples=["/config-frequency", "/config-frequency --interactive"]
        ))
        
        self._register_command(Command(
            name="config-protocols",
            description="Open protocol management menu",
            category=CommandCategory.PROTOCOL,
            handler=self._cmd_config_protocols,
            permissions=[Permission.READ_CONFIG],
            examples=["/config-protocols", "/config-protocols --list"]
        ))
        
        self._register_command(Command(
            name="config-agents",
            description="Open agent configuration menu",
            category=CommandCategory.AGENT,
            handler=self._cmd_config_agents,
            permissions=[Permission.READ_CONFIG],
            examples=["/config-agents", "/config-agents --status"]
        ))
        
        # Frequency control commands
        self._register_command(Command(
            name="set-frequency",
            description="Set frequency parameter value",
            category=CommandCategory.FREQUENCY,
            handler=self._cmd_set_frequency,
            permissions=[Permission.WRITE_CONFIG],
            parameters=["parameter", "value"],
            examples=["/set-frequency research_intensity 80", "/set-frequency validation_thoroughness 90"]
        ))
        
        self._register_command(Command(
            name="apply-preset",
            description="Apply preset configuration mode",
            category=CommandCategory.FREQUENCY,
            handler=self._cmd_apply_preset,
            permissions=[Permission.WRITE_CONFIG],
            parameters=["mode"],
            examples=["/apply-preset speed_mode", "/apply-preset quality_mode", "/apply-preset balanced_mode"]
        ))
        
        self._register_command(Command(
            name="get-suggestions",
            description="Get AI-powered configuration suggestions",
            category=CommandCategory.CONFIGURATION,
            handler=self._cmd_get_suggestions,
            permissions=[Permission.READ_CONFIG],
            parameters=["project_type", "expertise_level"],
            examples=["/get-suggestions web_application intermediate", "/get-suggestions api_service expert"]
        ))
        
        # Protocol management commands
        self._register_command(Command(
            name="create-protocol",
            description="Create a new workflow protocol",
            category=CommandCategory.PROTOCOL,
            handler=self._cmd_create_protocol,
            permissions=[Permission.MANAGE_PROTOCOLS],
            parameters=["name", "description"],
            examples=["/create-protocol \"My Protocol\" \"Custom workflow protocol\""]
        ))
        
        self._register_command(Command(
            name="list-protocols",
            description="List all available protocols",
            category=CommandCategory.PROTOCOL,
            handler=self._cmd_list_protocols,
            permissions=[Permission.READ_CONFIG],
            examples=["/list-protocols", "/list-protocols --filter web_application"]
        ))
        
        # System commands
        self._register_command(Command(
            name="status",
            description="Show system status and statistics",
            category=CommandCategory.SYSTEM,
            handler=self._cmd_status,
            permissions=[Permission.READ_CONFIG],
            examples=["/status", "/status --detailed"]
        ))
        
        self._register_command(Command(
            name="dashboard",
            description="Show configuration dashboard",
            category=CommandCategory.SYSTEM,
            handler=self._cmd_dashboard,
            permissions=[Permission.READ_CONFIG],
            examples=["/dashboard", "/dashboard --widget frequency_parameters"]
        ))
        
        self._register_command(Command(
            name="export-config",
            description="Export current configuration",
            category=CommandCategory.CONFIGURATION,
            handler=self._cmd_export_config,
            permissions=[Permission.EXPORT_CONFIG],
            parameters=["filename"],
            examples=["/export-config my_config.json"]
        ))
        
        self._register_command(Command(
            name="import-config",
            description="Import configuration from file",
            category=CommandCategory.CONFIGURATION,
            handler=self._cmd_import_config,
            permissions=[Permission.IMPORT_CONFIG],
            parameters=["filename"],
            examples=["/import-config my_config.json"]
        ))
        
        # Agent management commands
        self._register_command(Command(
            name="agent-status",
            description="Show agent status and utilization",
            category=CommandCategory.AGENT,
            handler=self._cmd_agent_status,
            permissions=[Permission.READ_CONFIG],
            examples=["/agent-status", "/agent-status --tier tier_2_primary"]
        ))
        
        self._register_command(Command(
            name="set-agent-utilization",
            description="Set agent utilization for a tier",
            category=CommandCategory.AGENT,
            handler=self._cmd_set_agent_utilization,
            permissions=[Permission.WRITE_CONFIG],
            parameters=["tier", "utilization"],
            examples=["/set-agent-utilization tier_2_primary 85"]
        ))
    
    def _register_command(self, command: Command):
        """Register a command"""
        self.commands[command.name] = command
        
        # Register aliases
        for alias in command.aliases:
            self.aliases[alias] = command.name
    
    async def execute_command(self, session_id: str, command_text: str) -> CommandResult:
        """Execute a command"""
        try:
            # Parse command
            parts = self._parse_command(command_text)
            if not parts:
                return CommandResult(
                    success=False,
                    error="Invalid command format",
                    suggestions=["Use /help to see available commands"]
                )
            
            command_name = parts[0].lower()
            args = parts[1:]
            
            # Resolve aliases
            if command_name in self.aliases:
                command_name = self.aliases[command_name]
            
            # Find command
            if command_name not in self.commands:
                return CommandResult(
                    success=False,
                    error=f"Unknown command: {command_name}",
                    suggestions=self._get_command_suggestions(command_name)
                )
            
            command = self.commands[command_name]
            
            # Check permissions
            for permission in command.permissions:
                if not self.security_manager.check_permission(session_id, permission):
                    return CommandResult(
                        success=False,
                        error="Insufficient permissions to execute this command"
                    )
            
            # Record command execution
            self._record_command_execution(session_id, command_name, args)
            
            # Execute command
            result = await command.handler(session_id, args)
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return CommandResult(
                success=False,
                error=f"Command execution failed: {str(e)}"
            )
    
    def _parse_command(self, command_text: str) -> List[str]:
        """Parse command text into parts"""
        # Remove leading slash if present
        if command_text.startswith('/'):
            command_text = command_text[1:]
        
        # Split by spaces, but respect quoted strings
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        for char in command_text:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part)
        
        return parts
    
    def _get_command_suggestions(self, command_name: str) -> List[str]:
        """Get command suggestions for unknown commands"""
        suggestions = []
        
        # Find similar command names
        for cmd_name in self.commands.keys():
            if self._similarity_score(command_name, cmd_name) > 0.6:
                suggestions.append(f"/help {cmd_name}")
        
        # Add general suggestions
        if not suggestions:
            suggestions = [
                "/help - Show all available commands",
                "/config-frequency - Manage frequency parameters",
                "/config-protocols - Manage workflow protocols"
            ]
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity score between two strings"""
        # Simple Levenshtein distance-based similarity
        if len(str1) == 0 or len(str2) == 0:
            return 0.0
        
        # Create matrix
        matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
        
        # Initialize first row and column
        for i in range(len(str1) + 1):
            matrix[i][0] = i
        for j in range(len(str2) + 1):
            matrix[0][j] = j
        
        # Fill matrix
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i-1] == str2[j-1]:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
                    matrix[i][j] = min(
                        matrix[i-1][j] + 1,      # deletion
                        matrix[i][j-1] + 1,      # insertion
                        matrix[i-1][j-1] + 1     # substitution
                    )
        
        # Calculate similarity
        max_len = max(len(str1), len(str2))
        distance = matrix[len(str1)][len(str2)]
        return 1.0 - (distance / max_len)
    
    def _record_command_execution(self, session_id: str, command_name: str, args: List[str]):
        """Record command execution in history"""
        user = self.security_manager.validate_session(session_id)
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "command": command_name,
            "args": args,
            "user_id": user.user_id if user else "unknown",
            "session_id": session_id
        }
        
        self.command_history.append(record)
        
        # Keep only last 1000 commands
        if len(self.command_history) > 1000:
            self.command_history = self.command_history[-1000:]
    
    # Command handlers
    async def _cmd_help(self, session_id: str, args: List[str]) -> CommandResult:
        """Help command handler"""
        if args:
            # Show help for specific command
            command_name = args[0].lower()
            if command_name in self.aliases:
                command_name = self.aliases[command_name]
            
            if command_name in self.commands:
                command = self.commands[command_name]
                help_text = f"**{command.name}**\n"
                help_text += f"Description: {command.description}\n"
                help_text += f"Category: {command.category.value}\n"
                
                if command.parameters:
                    help_text += f"Parameters: {', '.join(command.parameters)}\n"
                
                if command.examples:
                    help_text += "Examples:\n"
                    for example in command.examples:
                        help_text += f"  {example}\n"
                
                return CommandResult(success=True, message=help_text)
            else:
                return CommandResult(
                    success=False,
                    error=f"Unknown command: {command_name}",
                    suggestions=self._get_command_suggestions(command_name)
                )
        else:
            # Show all commands grouped by category
            help_text = "**JAEGIS Configuration Management Commands**\n\n"
            
            categories = {}
            for command in self.commands.values():
                if command.hidden:
                    continue
                
                category = command.category.value
                if category not in categories:
                    categories[category] = []
                categories[category].append(command)
            
            for category, commands in categories.items():
                help_text += f"**{category.upper()}**\n"
                for command in sorted(commands, key=lambda c: c.name):
                    help_text += f"  /{command.name} - {command.description}\n"
                help_text += "\n"
            
            help_text += "Use `/help <command>` for detailed information about a specific command.\n"
            help_text += "Use `/config-frequency`, `/config-protocols`, or `/config-agents` to access configuration menus."
            
            return CommandResult(success=True, message=help_text)
    
    async def _cmd_config_frequency(self, session_id: str, args: List[str]) -> CommandResult:
        """Frequency configuration menu handler"""
        current_state = self.frequency_controller.get_current_frequency_state()
        
        menu_text = "**🎛️ Frequency Control Menu**\n\n"
        menu_text += "**Current Parameters:**\n"
        
        freq_params = current_state["frequency_parameters"]
        for param_name, value in freq_params.items():
            if param_name != "agent_utilization":
                menu_text += f"  • {param_name.replace('_', ' ').title()}: {value}%\n"
        
        menu_text += "\n**Agent Utilization:**\n"
        for tier, utilization in freq_params["agent_utilization"].items():
            menu_text += f"  • {tier.replace('_', ' ').title()}: {utilization}%\n"
        
        menu_text += f"\n**Configuration Mode:** {current_state['configuration_mode']}\n"
        menu_text += f"**Last Modified:** {current_state['last_modified']}\n\n"
        
        menu_text += "**Available Commands:**\n"
        menu_text += "  • `/set-frequency <parameter> <value>` - Set parameter value\n"
        menu_text += "  • `/apply-preset <mode>` - Apply preset mode (speed_mode, quality_mode, balanced_mode)\n"
        menu_text += "  • `/get-suggestions <project_type> <expertise>` - Get AI suggestions\n"
        menu_text += "  • `/dashboard` - View real-time statistics\n"
        
        return CommandResult(
            success=True,
            message=menu_text,
            data=current_state
        )
    
    async def _cmd_config_protocols(self, session_id: str, args: List[str]) -> CommandResult:
        """Protocol configuration menu handler"""
        protocols_result = self.protocol_manager.get_protocols(session_id)
        
        if not protocols_result["success"]:
            return CommandResult(success=False, error=protocols_result["error"])
        
        protocols = protocols_result["protocols"]
        
        menu_text = "**📋 Protocol Management Menu**\n\n"
        menu_text += f"**Total Protocols:** {len(protocols)}\n\n"
        
        if protocols:
            menu_text += "**Active Protocols:**\n"
            for protocol in protocols[:5]:  # Show first 5
                menu_text += f"  • {protocol['name']} ({protocol['rule_count']} rules)\n"
                menu_text += f"    Project Types: {', '.join(protocol['project_types'])}\n"
            
            if len(protocols) > 5:
                menu_text += f"  ... and {len(protocols) - 5} more\n"
        else:
            menu_text += "No protocols configured.\n"
        
        menu_text += "\n**Available Commands:**\n"
        menu_text += "  • `/list-protocols` - List all protocols\n"
        menu_text += "  • `/create-protocol <name> <description>` - Create new protocol\n"
        menu_text += "  • `/help protocol` - Protocol management help\n"
        
        return CommandResult(
            success=True,
            message=menu_text,
            data={"protocols": protocols}
        )
    
    async def _cmd_config_agents(self, session_id: str, args: List[str]) -> CommandResult:
        """Agent configuration menu handler"""
        current_config = self.config_engine.get_current_config()
        freq_params = current_config.frequency_parameters
        
        menu_text = "**🤖 Agent Configuration Menu**\n\n"
        menu_text += "**Agent Utilization by Tier:**\n"
        
        for tier, utilization in freq_params.agent_utilization.items():
            status = "🟢 Active" if utilization >= 70 else "🟡 Limited" if utilization >= 30 else "🔴 Minimal"
            menu_text += f"  • {tier.value.replace('_', ' ').title()}: {utilization}% {status}\n"
        
        menu_text += f"\n**Total Configured Agents:** {len(current_config.agent_configurations)}\n"
        
        menu_text += "\n**Available Commands:**\n"
        menu_text += "  • `/agent-status` - Show detailed agent status\n"
        menu_text += "  • `/set-agent-utilization <tier> <value>` - Set tier utilization\n"
        menu_text += "  • `/help agent` - Agent management help\n"
        
        return CommandResult(
            success=True,
            message=menu_text,
            data={"agent_utilization": dict(freq_params.agent_utilization)}
        )
    
    async def _cmd_set_frequency(self, session_id: str, args: List[str]) -> CommandResult:
        """Set frequency parameter handler"""
        if len(args) < 2:
            return CommandResult(
                success=False,
                error="Usage: /set-frequency <parameter> <value>",
                suggestions=["Example: /set-frequency research_intensity 80"]
            )
        
        parameter_name = args[0]
        try:
            value = int(args[1])
        except ValueError:
            return CommandResult(
                success=False,
                error="Value must be a number between 0 and 100"
            )
        
        result = await self.frequency_controller.update_frequency_parameter(session_id, parameter_name, value)
        
        if result["success"]:
            return CommandResult(
                success=True,
                message=f"✅ Updated {parameter_name} from {result['old_value']}% to {result['new_value']}%",
                data=result
            )
        else:
            return CommandResult(
                success=False,
                error=result["error"]
            )
    
    async def _cmd_apply_preset(self, session_id: str, args: List[str]) -> CommandResult:
        """Apply preset mode handler"""
        if len(args) < 1:
            return CommandResult(
                success=False,
                error="Usage: /apply-preset <mode>",
                suggestions=["Available modes: speed_mode, quality_mode, balanced_mode"]
            )
        
        mode = args[0]
        result = await self.frequency_controller.apply_frequency_profile(session_id, mode)
        
        if result["success"]:
            return CommandResult(
                success=True,
                message=f"✅ Applied {result['profile']} with {result['total_changes']} parameter changes",
                data=result
            )
        else:
            return CommandResult(
                success=False,
                error=result["error"]
            )
    
    async def _cmd_get_suggestions(self, session_id: str, args: List[str]) -> CommandResult:
        """Get AI suggestions handler"""
        if len(args) < 2:
            return CommandResult(
                success=False,
                error="Usage: /get-suggestions <project_type> <expertise_level>",
                suggestions=[
                    "Example: /get-suggestions web_application intermediate",
                    "Project types: web_application, api_service, mobile_app, etc.",
                    "Expertise levels: beginner, intermediate, advanced, expert"
                ]
            )
        
        try:
            project_type = ProjectType(args[0])
            expertise_level = UserExpertiseLevel(args[1])
        except ValueError as e:
            return CommandResult(
                success=False,
                error=f"Invalid parameter: {e}",
                suggestions=[
                    "Valid project types: " + ", ".join([pt.value for pt in ProjectType]),
                    "Valid expertise levels: " + ", ".join([el.value for el in UserExpertiseLevel])
                ]
            )
        
        # Create project context
        context = ProjectContext(
            project_type=project_type,
            user_expertise=expertise_level,
            project_phase=ProjectPhase.DEVELOPMENT  # Default
        )
        
        suggestions = self.suggestions_engine.generate_suggestions(context)
        
        if suggestions:
            message = f"**🤖 AI Suggestions for {project_type.value} ({expertise_level.value})**\n\n"
            
            for i, suggestion in enumerate(suggestions[:3], 1):  # Show top 3
                message += f"**{i}. {suggestion.title}** (Confidence: {suggestion.confidence_score:.0%})\n"
                message += f"   {suggestion.description}\n"
                message += f"   Priority: {suggestion.priority.title()}\n\n"
            
            return CommandResult(
                success=True,
                message=message,
                data={"suggestions": [s.to_dict() for s in suggestions]}
            )
        else:
            return CommandResult(
                success=True,
                message="No specific suggestions available for your configuration.",
                suggestions=["Your current configuration appears to be well-optimized"]
            )
    
    async def _cmd_status(self, session_id: str, args: List[str]) -> CommandResult:
        """System status handler"""
        dashboard_summary = self.dashboard.get_dashboard_summary()
        config_stats = self.config_engine.get_configuration_statistics()
        
        status_text = "**📊 JAEGIS System Status**\n\n"
        status_text += f"**Configuration Mode:** {dashboard_summary['configuration_mode']}\n"
        status_text += f"**Average Frequency:** {dashboard_summary['average_frequency']}%\n"
        status_text += f"**Average Utilization:** {dashboard_summary['average_utilization']}%\n"
        status_text += f"**Active Metrics:** {dashboard_summary['active_metrics']}\n"
        status_text += f"**Total Protocols:** {config_stats['protocol_count']}\n"
        status_text += f"**Agent Configurations:** {config_stats['agent_configuration_count']}\n"
        status_text += f"**Last Updated:** {config_stats['modified_at']}\n"
        
        if config_stats['validation_errors'] > 0:
            status_text += f"\n⚠️ **Validation Errors:** {config_stats['validation_errors']}\n"
        else:
            status_text += "\n✅ **Configuration Valid**\n"
        
        return CommandResult(
            success=True,
            message=status_text,
            data={
                "dashboard_summary": dashboard_summary,
                "config_stats": config_stats
            }
        )
    
    async def _cmd_dashboard(self, session_id: str, args: List[str]) -> CommandResult:
        """Dashboard handler"""
        if args and args[0] == "--widget":
            if len(args) < 2:
                return CommandResult(
                    success=False,
                    error="Usage: /dashboard --widget <widget_id>"
                )
            
            widget_id = args[1]
            widget_data = self.dashboard.get_widget_data(widget_id)
            
            return CommandResult(
                success=True,
                message=f"Widget data for {widget_id}",
                data=widget_data
            )
        else:
            # Show dashboard summary
            summary = self.dashboard.get_dashboard_summary()
            
            dashboard_text = "**📈 Configuration Dashboard**\n\n"
            dashboard_text += f"**Mode:** {summary['configuration_mode']}\n"
            dashboard_text += f"**Avg Frequency:** {summary['average_frequency']}%\n"
            dashboard_text += f"**Avg Utilization:** {summary['average_utilization']}%\n"
            dashboard_text += f"**Widgets:** {summary['total_widgets']}\n"
            dashboard_text += f"**Metrics:** {summary['active_metrics']}\n"
            dashboard_text += f"**Updated:** {summary['last_updated']}\n"
            
            return CommandResult(
                success=True,
                message=dashboard_text,
                data=summary
            )
    
    async def _cmd_export_config(self, session_id: str, args: List[str]) -> CommandResult:
        """Export configuration handler"""
        if len(args) < 1:
            return CommandResult(
                success=False,
                error="Usage: /export-config <filename>"
            )
        
        filename = args[0]
        success = self.config_engine.export_configuration(filename)
        
        if success:
            return CommandResult(
                success=True,
                message=f"✅ Configuration exported to {filename}"
            )
        else:
            return CommandResult(
                success=False,
                error="Failed to export configuration"
            )
    
    async def _cmd_import_config(self, session_id: str, args: List[str]) -> CommandResult:
        """Import configuration handler"""
        if len(args) < 1:
            return CommandResult(
                success=False,
                error="Usage: /import-config <filename>"
            )
        
        filename = args[0]
        success = self.config_engine.import_configuration(filename)
        
        if success:
            return CommandResult(
                success=True,
                message=f"✅ Configuration imported from {filename}"
            )
        else:
            return CommandResult(
                success=False,
                error="Failed to import configuration"
            )
    
    async def _cmd_create_protocol(self, session_id: str, args: List[str]) -> CommandResult:
        """Create protocol handler"""
        if len(args) < 2:
            return CommandResult(
                success=False,
                error="Usage: /create-protocol <name> <description>"
            )
        
        protocol_data = {
            "name": args[0],
            "description": args[1]
        }
        
        result = await self.protocol_manager.create_protocol(session_id, protocol_data)
        
        if result["success"]:
            return CommandResult(
                success=True,
                message=result["message"],
                data={"protocol_id": result["protocol_id"]}
            )
        else:
            return CommandResult(
                success=False,
                error=result["error"]
            )
    
    async def _cmd_list_protocols(self, session_id: str, args: List[str]) -> CommandResult:
        """List protocols handler"""
        filters = {}
        if args and args[0] == "--filter" and len(args) > 1:
            filters["project_type"] = args[1]
        
        result = self.protocol_manager.get_protocols(session_id, filters)
        
        if result["success"]:
            protocols = result["protocols"]
            
            if protocols:
                message = f"**📋 Protocols ({len(protocols)} total)**\n\n"
                for protocol in protocols:
                    message += f"• **{protocol['name']}** ({protocol['rule_count']} rules)\n"
                    message += f"  {protocol['description']}\n"
                    if protocol['project_types']:
                        message += f"  Types: {', '.join(protocol['project_types'])}\n"
                    message += "\n"
            else:
                message = "No protocols found."
            
            return CommandResult(
                success=True,
                message=message,
                data=result
            )
        else:
            return CommandResult(
                success=False,
                error=result["error"]
            )
    
    async def _cmd_agent_status(self, session_id: str, args: List[str]) -> CommandResult:
        """Agent status handler"""
        current_config = self.config_engine.get_current_config()
        freq_params = current_config.frequency_parameters
        
        status_text = "**🤖 Agent Status Report**\n\n"
        
        for tier, utilization in freq_params.agent_utilization.items():
            tier_name = tier.value.replace('_', ' ').title()
            
            if utilization >= 80:
                status_icon = "🟢"
                status_text_desc = "Fully Active"
            elif utilization >= 50:
                status_icon = "🟡"
                status_text_desc = "Moderately Active"
            elif utilization >= 20:
                status_icon = "🟠"
                status_text_desc = "Limited Activity"
            else:
                status_icon = "🔴"
                status_text_desc = "Minimal Activity"
            
            status_text += f"{status_icon} **{tier_name}**: {utilization}% ({status_text_desc})\n"
        
        return CommandResult(
            success=True,
            message=status_text,
            data={"agent_utilization": dict(freq_params.agent_utilization)}
        )
    
    async def _cmd_set_agent_utilization(self, session_id: str, args: List[str]) -> CommandResult:
        """Set agent utilization handler"""
        if len(args) < 2:
            return CommandResult(
                success=False,
                error="Usage: /set-agent-utilization <tier> <value>",
                suggestions=["Example: /set-agent-utilization tier_2_primary 85"]
            )
        
        tier = args[0]
        try:
            value = int(args[1])
        except ValueError:
            return CommandResult(
                success=False,
                error="Value must be a number between 0 and 100"
            )
        
        result = await self.frequency_controller.update_agent_utilization(session_id, tier, value)
        
        if result["success"]:
            return CommandResult(
                success=True,
                message=f"✅ Updated {tier} utilization from {result['old_value']}% to {result['new_value']}%",
                data=result
            )
        else:
            return CommandResult(
                success=False,
                error=result["error"]
            )
    
    def get_command_history(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get command history for a session"""
        user = self.security_manager.validate_session(session_id)
        if not user:
            return []
        
        # Filter by user and return recent commands
        user_commands = [
            cmd for cmd in self.command_history
            if cmd["user_id"] == user.user_id
        ]
        
        return user_commands[-limit:]
    
    def get_command_statistics(self) -> Dict[str, Any]:
        """Get command usage statistics"""
        total_commands = len(self.command_history)
        
        # Count by command
        command_counts = {}
        for record in self.command_history:
            cmd = record["command"]
            command_counts[cmd] = command_counts.get(cmd, 0) + 1
        
        # Most used commands
        most_used = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_commands_executed": total_commands,
            "unique_commands": len(command_counts),
            "most_used_commands": most_used,
            "registered_commands": len(self.commands),
            "registered_aliases": len(self.aliases)
        }
