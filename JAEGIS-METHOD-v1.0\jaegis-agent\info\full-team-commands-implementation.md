# JAEGIS Full Team Commands Implementation

## Command System Overview

The Full Team Commands provide comprehensive control over the full team participation feature, allowing users to enable, disable, and monitor collaborative agent participation throughout workflow execution.

## Core Command Architecture

### 1. Command Registration and Processing

#### Enhanced Command Processor
```python
class FullTeamCommandProcessor:
    """Enhanced command processor with full team participation support"""
    
    def __init__(self):
        self.command_registry = CommandRegistry()
        self.participation_manager = ParticipationManager()
        self.session_manager = SessionManager()
        self.response_formatter = ResponseFormatter()
        
        # Register full team commands
        self.register_full_team_commands()
    
    def register_full_team_commands(self):
        """Register all full team participation commands"""
        
        commands = [
            FullTeamOnCommand(self.participation_manager, self.session_manager),
            FullTeamOffCommand(self.participation_manager, self.session_manager),
            FullTeamStatusCommand(self.participation_manager, self.session_manager)
        ]
        
        for command in commands:
            self.command_registry.register_command(command)
        
        return CommandRegistrationResult(
            registered_commands=[cmd.name for cmd in commands],
            registration_success=True
        )
    
    def process_command(self, command_input, session_context):
        """Process command with enhanced error handling and validation"""
        
        try:
            # Parse command
            parsed_command = self.parse_command(command_input)
            
            # Get command instance
            command_instance = self.command_registry.get_command(parsed_command.command_name)
            
            if not command_instance:
                return self.create_error_response(f"Unknown command: {parsed_command.command_name}")
            
            # Validate command context
            validation_result = command_instance.validate_context(session_context)
            if not validation_result.valid:
                return self.create_error_response(validation_result.error_message)
            
            # Execute command
            execution_result = command_instance.execute(parsed_command.parameters, session_context)
            
            # Format response
            formatted_response = self.response_formatter.format_command_response(
                execution_result,
                parsed_command.command_name
            )
            
            return CommandExecutionResult(
                success=execution_result.success,
                response=formatted_response,
                session_updates=execution_result.session_updates
            )
            
        except Exception as e:
            return self.create_error_response(f"Command execution error: {str(e)}")
```

### 2. /full_team_on Command Implementation

#### Complete Full Team On Command
```python
class FullTeamOnCommand:
    """Command to enable full team participation mode"""
    
    def __init__(self, participation_manager, session_manager):
        self.name = "full_team_on"
        self.aliases = ["full_team_enable", "enable_full_team"]
        self.category = "participation_management"
        self.description = "Enable full team participation mode for comprehensive project coverage"
        self.usage = "/full_team_on"
        self.examples = ["/full_team_on"]
        self.participation_manager = participation_manager
        self.session_manager = session_manager
    
    def validate_context(self, session_context):
        """Validate that command can be executed in current context"""
        
        if not session_context.session_active:
            return ValidationResult(
                valid=False,
                error_message="No active session. Please start a workflow session first."
            )
        
        if session_context.full_team_participation_enabled:
            return ValidationResult(
                valid=False,
                error_message="Full team participation is already enabled."
            )
        
        return ValidationResult(valid=True)
    
    def execute(self, parameters, session_context):
        """Execute full team on command"""
        
        try:
            # Enable full team participation
            enable_result = self.participation_manager.enable_full_team_participation(
                session_context.session_id
            )
            
            # Get all available agents
            all_agents = self.session_manager.get_all_available_agents()
            
            # Determine integration points for current workflow
            integration_points = self.participation_manager.get_integration_points(
                session_context.workflow_type,
                all_agents
            )
            
            # Update session configuration
            session_updates = {
                "full_team_participation": True,
                "participating_agents": [agent.name for agent in all_agents],
                "integration_points": len(integration_points),
                "expected_benefits": self.calculate_expected_benefits(all_agents, integration_points)
            }
            
            # Generate comprehensive response
            response = self.generate_activation_response(
                all_agents,
                integration_points,
                enable_result,
                session_context
            )
            
            return CommandResult(
                success=True,
                response=response,
                session_updates=session_updates
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                error=f"Failed to enable full team participation: {str(e)}"
            )
    
    def generate_activation_response(self, all_agents, integration_points, enable_result, session_context):
        """Generate comprehensive activation response"""
        
        response_sections = []
        
        # Header with activation confirmation
        response_sections.append("🤝 **Full Team Participation: ACTIVATED**")
        response_sections.append("=" * 50)
        response_sections.append("")
        
        # Activation summary
        response_sections.append("✅ **Activation Summary:**")
        response_sections.append(f"   • Status: Full team participation is now **ACTIVE**")
        response_sections.append(f"   • Team Size: **{len(all_agents)} agents** will collaborate")
        response_sections.append(f"   • Workflow Type: **{session_context.workflow_type.replace('_', ' ').title()}**")
        response_sections.append(f"   • Integration Points: **{len(integration_points)} opportunities** identified")
        response_sections.append("")
        
        # Agent team breakdown with 4-tier system
        response_sections.append("👥 **24-Agent Team Breakdown:**")
        response_sections.append("")

        # Tier 1: Orchestrator (always active)
        orchestrator_agents = [agent for agent in all_agents if agent.classification == "ORCHESTRATOR"]
        response_sections.append("**🎯 Tier 1: Orchestrator (System Controller):**")
        for agent in orchestrator_agents:
            response_sections.append(f"   • **{agent.name}** ({agent.title})")
            response_sections.append(f"     *Role*: System coordination and workflow management")
        response_sections.append("")

        # Tier 2: Primary agents (always active)
        primary_agents = [agent for agent in all_agents if agent.classification == "PRIMARY"]
        response_sections.append("**🎯 Tier 2: Primary Agents (Core Leadership - Always Active):**")
        for agent in primary_agents:
            response_sections.append(f"   • **{agent.name}** ({agent.title})")
            response_sections.append(f"     *Expertise*: {agent.primary_expertise}")
            response_sections.append(f"     *Role*: {self.get_agent_role_description(agent, session_context.workflow_type)}")
        response_sections.append("")

        # Tier 3: Secondary agents (full team participation)
        secondary_agents = [agent for agent in all_agents if agent.classification == "SECONDARY"]
        response_sections.append("**🚀 Tier 3: Secondary Agents (Domain Specialists - Full Team Mode):**")

        # Group secondary agents by domain for better organization
        domain_groups = self.group_agents_by_domain(secondary_agents)
        for domain_name, domain_agents in domain_groups.items():
            response_sections.append(f"  **{domain_name}:**")
            for agent in domain_agents:
                response_sections.append(f"   • **{agent.name}** ({agent.title})")
                response_sections.append(f"     *Expertise*: {agent.primary_expertise}")
                response_sections.append(f"     *Contribution*: {self.get_expected_contribution(agent, session_context.workflow_type)}")
        response_sections.append("")

        # Tier 4: Specialized agents (conditional activation)
        specialized_agents = [agent for agent in all_agents if agent.classification == "SPECIALIZED"]
        response_sections.append("**⚡ Tier 4: Specialized Agents (Conditional Activation):**")
        for agent in specialized_agents:
            activation_status = "🟢 Will activate" if self.should_activate_specialized_agent(agent, session_context) else "🟡 Conditional"
            response_sections.append(f"   • **{agent.name}** ({agent.title}) - {activation_status}")
            response_sections.append(f"     *Expertise*: {agent.primary_expertise}")
            response_sections.append(f"     *Activation Criteria*: {', '.join(agent.activation_criteria)}")
        response_sections.append("")
        
        # Integration timeline
        response_sections.append("📋 **Integration Timeline:**")
        integration_phases = self.group_integration_points_by_phase(integration_points)
        for phase_name, phase_points in integration_phases.items():
            response_sections.append(f"**{phase_name.replace('_', ' ').title()} Phase:**")
            for point in phase_points[:3]:  # Show top 3 per phase
                response_sections.append(f"   • {point.agent_name}: {point.contribution_description}")
            if len(phase_points) > 3:
                response_sections.append(f"   • ... and {len(phase_points) - 3} more integration opportunities")
            response_sections.append("")
        
        # Expected benefits
        response_sections.append("🎯 **Expected Benefits:**")
        benefits = [
            "**Comprehensive Coverage**: All project aspects reviewed by domain experts",
            "**Enhanced Quality**: Multi-perspective validation and quality assurance",
            "**Risk Mitigation**: Collaborative decision-making reduces project risks",
            "**Professional Standards**: Industry best practices applied across all domains",
            "**Knowledge Integration**: Cross-functional insights improve solution quality",
            "**Stakeholder Alignment**: Business, technical, and user perspectives integrated"
        ]
        for benefit in benefits:
            response_sections.append(f"   ✅ {benefit}")
        response_sections.append("")
        
        # Performance expectations
        response_sections.append("⚡ **Performance Expectations:**")
        response_sections.append(f"   • **Estimated Time Impact**: +15-20% for comprehensive collaboration")
        response_sections.append(f"   • **Quality Improvement**: +25-30% through expert validation")
        response_sections.append(f"   • **Coverage Enhancement**: 100% domain expertise utilization")
        response_sections.append("")
        
        # Next steps
        response_sections.append("🚀 **Ready to Proceed:**")
        response_sections.append("   • All agents are now prepared for collaborative participation")
        response_sections.append("   • Integration points have been optimized for your workflow")
        response_sections.append("   • Use `/full_team_status` to monitor participation progress")
        response_sections.append("   • Use `/full_team_off` to disable if needed")
        response_sections.append("")
        response_sections.append("**🎉 Full team collaboration activated! Let's create something amazing together!**")
        
        return "\n".join(response_sections)
    
    def get_agent_role_description(self, agent, workflow_type):
        """Get agent role description for specific workflow type"""
        
        role_descriptions = {
            "documentation_mode": {
                "John": "Business requirements analysis and stakeholder perspective",
                "Fred": "Technical architecture design and system validation",
                "Tyler": "Task breakdown and implementation planning"
            },
            "full_development_mode": {
                "John": "Product management and business coordination",
                "Fred": "System architecture and technical leadership",
                "Tyler": "Development planning and task coordination"
            }
        }
        
        return role_descriptions.get(workflow_type, {}).get(agent.name, "Core team coordination")
    
    def get_expected_contribution(self, agent, workflow_type):
        """Get expected contribution description for agent"""
        
        contribution_descriptions = {
            "Jane": "UX/UI design validation and user experience optimization",
            "Alex": "Infrastructure planning and security assessment",
            "James": "Implementation feasibility and code quality standards",
            "Sage": "Dependency validation and security compliance",
            "Dakota": "Data architecture and privacy compliance",
            "Sentinel": "Quality assurance and testing strategy",
            "DocQA": "Documentation standards and user guide creation"
        }
        
        return contribution_descriptions.get(agent.name, "Domain-specific expertise and validation")
    
    def calculate_expected_benefits(self, all_agents, integration_points):
        """Calculate expected benefits from full team participation"""
        
        return {
            "quality_improvement_percentage": 25,
            "coverage_enhancement_percentage": 100,
            "risk_reduction_percentage": 40,
            "expertise_utilization_percentage": 100,
            "collaboration_effectiveness_score": 9.2
        }
```

### 3. /full_team_off Command Implementation

#### Complete Full Team Off Command
```python
class FullTeamOffCommand:
    """Command to disable full team participation mode"""
    
    def __init__(self, participation_manager, session_manager):
        self.name = "full_team_off"
        self.aliases = ["full_team_disable", "disable_full_team"]
        self.category = "participation_management"
        self.description = "Disable full team participation and revert to selective agent activation"
        self.usage = "/full_team_off"
        self.examples = ["/full_team_off"]
        self.participation_manager = participation_manager
        self.session_manager = session_manager
    
    def validate_context(self, session_context):
        """Validate that command can be executed"""
        
        if not session_context.session_active:
            return ValidationResult(
                valid=False,
                error_message="No active session found."
            )
        
        if not session_context.full_team_participation_enabled:
            return ValidationResult(
                valid=False,
                error_message="Full team participation is not currently enabled."
            )
        
        return ValidationResult(valid=True)
    
    def execute(self, parameters, session_context):
        """Execute full team off command"""
        
        try:
            # Get current participation status before disabling
            current_status = self.participation_manager.get_current_participation_status(
                session_context.session_id
            )
            
            # Disable full team participation
            disable_result = self.participation_manager.disable_full_team_participation(
                session_context.session_id
            )
            
            # Determine selective agents for current workflow
            selective_agents = self.session_manager.select_workflow_agents(
                session_context.workflow_type,
                session_context.project_requirements
            )
            
            # Update session configuration
            session_updates = {
                "full_team_participation": False,
                "participating_agents": [agent.name for agent in selective_agents],
                "participation_mode": "selective",
                "deactivated_agents": self.get_deactivated_agents(current_status.all_agents, selective_agents)
            }
            
            # Generate comprehensive response
            response = self.generate_deactivation_response(
                current_status,
                selective_agents,
                disable_result,
                session_context
            )
            
            return CommandResult(
                success=True,
                response=response,
                session_updates=session_updates
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                error=f"Failed to disable full team participation: {str(e)}"
            )
    
    def generate_deactivation_response(self, current_status, selective_agents, disable_result, session_context):
        """Generate comprehensive deactivation response"""
        
        response_sections = []
        
        # Header
        response_sections.append("🔄 **Full Team Participation: DISABLED**")
        response_sections.append("=" * 50)
        response_sections.append("")
        
        # Deactivation summary
        response_sections.append("✅ **Deactivation Summary:**")
        response_sections.append(f"   • Status: Reverted to **selective agent activation**")
        response_sections.append(f"   • Team Size: Reduced from **{current_status.total_agents}** to **{len(selective_agents)}** agents")
        response_sections.append(f"   • Mode: **Selective** based on workflow requirements")
        response_sections.append("")
        
        # Current session impact
        if current_status.participated_agents:
            response_sections.append("📊 **Current Session Impact:**")
            response_sections.append(f"   • **{len(current_status.participated_agents)} agents** have already contributed")
            response_sections.append(f"   • **{current_status.total_contributions} contributions** will be preserved")
            response_sections.append(f"   • **Average quality score**: {current_status.average_quality:.1f}/10")
            response_sections.append("")
        
        # Active agents (selective mode)
        response_sections.append("🎯 **Active Agents (Selective Mode):**")
        for agent in selective_agents:
            contribution_status = "✅ Contributed" if agent.name in [a.name for a in current_status.participated_agents] else "⏳ Pending"
            response_sections.append(f"   • **{agent.name}** ({agent.title}) - {contribution_status}")
            response_sections.append(f"     *Primary Role*: {agent.primary_expertise}")
        response_sections.append("")
        
        # Deactivated agents
        deactivated_agents = self.get_deactivated_agents(current_status.all_agents, selective_agents)
        if deactivated_agents:
            response_sections.append("⏸️ **Deactivated Agents:**")
            for agent in deactivated_agents:
                contribution_status = "✅ Already contributed" if agent.name in [a.name for a in current_status.participated_agents] else "❌ No contribution"
                response_sections.append(f"   • **{agent.name}** ({agent.title}) - {contribution_status}")
            response_sections.append("")
        
        # Impact analysis
        response_sections.append("📈 **Impact Analysis:**")
        impact_benefits = [
            "**Faster Execution**: Streamlined workflow with focused agent team",
            "**Reduced Complexity**: Essential agents only for core requirements",
            "**Maintained Quality**: Core expertise coverage preserved",
            "**Efficient Resource Use**: Optimal agent utilization for workflow type"
        ]
        for benefit in impact_benefits:
            response_sections.append(f"   ✅ {benefit}")
        response_sections.append("")
        
        # Performance expectations
        response_sections.append("⚡ **Performance Expectations:**")
        response_sections.append(f"   • **Time Reduction**: 15-20% faster execution with selective team")
        response_sections.append(f"   • **Focus Enhancement**: Concentrated expertise on core requirements")
        response_sections.append(f"   • **Quality Maintenance**: Essential validation preserved")
        response_sections.append("")
        
        # Next steps
        response_sections.append("🚀 **Continuing with Selective Mode:**")
        response_sections.append("   • Workflow will continue with optimized agent team")
        response_sections.append("   • Use `/full_team_on` to re-enable full team participation")
        response_sections.append("   • Use `/full_team_status` to monitor current participation")
        response_sections.append("")
        response_sections.append("**🎯 Selective agent activation mode is now active!**")
        
        return "\n".join(response_sections)
    
    def get_deactivated_agents(self, all_agents, selective_agents):
        """Get list of agents that were deactivated"""
        
        selective_agent_names = [agent.name for agent in selective_agents]
        return [agent for agent in all_agents if agent.name not in selective_agent_names]
```

### 4. /full_team_status Command Implementation

#### Complete Full Team Status Command
```python
class FullTeamStatusCommand:
    """Command to display comprehensive full team participation status"""
    
    def __init__(self, participation_manager, session_manager):
        self.name = "full_team_status"
        self.aliases = ["team_status", "participation_status"]
        self.category = "information_display"
        self.description = "Display detailed full team participation status and progress"
        self.usage = "/full_team_status"
        self.examples = ["/full_team_status"]
        self.participation_manager = participation_manager
        self.session_manager = session_manager
    
    def validate_context(self, session_context):
        """Validate command context"""
        
        if not session_context.session_active:
            return ValidationResult(
                valid=False,
                error_message="No active session found."
            )
        
        return ValidationResult(valid=True)
    
    def execute(self, parameters, session_context):
        """Execute full team status command"""
        
        try:
            # Get comprehensive participation status
            participation_status = self.participation_manager.get_detailed_participation_status(
                session_context.session_id
            )
            
            # Get session progress metrics
            session_progress = self.participation_manager.calculate_session_progress(
                session_context.session_id
            )
            
            # Get upcoming opportunities
            upcoming_opportunities = self.participation_manager.get_upcoming_opportunities(
                session_context.session_id
            )
            
            # Get quality insights
            quality_insights = self.participation_manager.get_quality_insights(
                session_context.session_id
            )
            
            # Generate comprehensive status response
            response = self.generate_comprehensive_status_response(
                participation_status,
                session_progress,
                upcoming_opportunities,
                quality_insights,
                session_context
            )
            
            return CommandResult(
                success=True,
                response=response,
                metadata={
                    "participation_status": participation_status,
                    "session_progress": session_progress,
                    "quality_insights": quality_insights
                }
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                error=f"Failed to retrieve participation status: {str(e)}"
            )
    
    def generate_comprehensive_status_response(self, participation_status, session_progress, upcoming_opportunities, quality_insights, session_context):
        """Generate comprehensive status response"""
        
        response_sections = []
        
        # Header with current mode
        if participation_status.full_team_enabled:
            response_sections.append("🤝 **Full Team Participation Status: ACTIVE**")
        else:
            response_sections.append("🎯 **Selective Agent Participation Status: ACTIVE**")
        response_sections.append("=" * 60)
        response_sections.append("")
        
        # Executive dashboard
        response_sections.append("📊 **Executive Dashboard:**")
        response_sections.append(f"   • **Participation Rate**: {session_progress.participation_rate:.1f}% ({session_progress.participated_count}/{session_progress.total_agents} agents)")
        response_sections.append(f"   • **Average Quality Score**: {session_progress.average_quality_score:.1f}/10")
        response_sections.append(f"   • **Session Duration**: {self.format_duration(session_progress.session_duration)}")
        response_sections.append(f"   • **Current Phase**: {session_progress.current_phase.replace('_', ' ').title()}")
        response_sections.append(f"   • **Workflow Type**: {session_context.workflow_type.replace('_', ' ').title()}")
        response_sections.append("")
        
        # 24-Agent participation table with tier grouping
        response_sections.append("👥 **24-Agent Participation Status:**")
        response_sections.append("")

        # Group agents by tier for better organization
        agent_tiers = self.group_agents_by_tier(participation_status.agent_statuses)

        for tier_name, tier_agents in agent_tiers.items():
            response_sections.append(f"**{tier_name}:**")
            response_sections.append("| Agent | Title | Status | Contributions | Quality | Last Activity |")
            response_sections.append("|-------|-------|--------|---------------|---------|---------------|")

            for agent_name, agent_status in tier_agents.items():
                status_display = self.get_status_display(agent_status.participation_status)
                contribution_count = len(agent_status.contributions)
                quality_display = f"{agent_status.average_quality:.1f}" if agent_status.average_quality else "N/A"
                last_activity = self.format_last_activity(agent_status.last_contribution_time)

                response_sections.append(f"| {agent_name} | {agent_status.title} | {status_display} | {contribution_count} | {quality_display} | {last_activity} |")

            response_sections.append("")
        
        # Participation breakdown
        response_sections.append("📈 **Participation Breakdown:**")
        status_counts = self.calculate_status_counts(participation_status.agent_statuses)
        for status, count in status_counts.items():
            status_display = self.get_status_display(status)
            percentage = (count / session_progress.total_agents) * 100
            response_sections.append(f"   • {status_display}: **{count} agents** ({percentage:.1f}%)")
        response_sections.append("")
        
        # Quality insights
        response_sections.append("🎯 **Quality Insights:**")
        for insight in quality_insights[:5]:  # Top 5 insights
            response_sections.append(f"   • {insight}")
        response_sections.append("")
        
        # Upcoming integration opportunities
        if upcoming_opportunities:
            response_sections.append("🔮 **Upcoming Integration Opportunities:**")
            for opportunity in upcoming_opportunities[:5]:  # Next 5 opportunities
                response_sections.append(f"   • **{opportunity.agent_name}**: {opportunity.opportunity_description}")
                response_sections.append(f"     *Expected in*: {opportunity.phase_name.replace('_', ' ').title()} phase")
            
            if len(upcoming_opportunities) > 5:
                response_sections.append(f"   • ... and **{len(upcoming_opportunities) - 5} more opportunities**")
            response_sections.append("")
        
        # Performance metrics
        response_sections.append("⚡ **Performance Metrics:**")
        response_sections.append(f"   • **Meaningful Contribution Rate**: {session_progress.meaningful_contribution_rate:.1f}%")
        response_sections.append(f"   • **Average Response Time**: {session_progress.average_response_time:.1f} seconds")
        response_sections.append(f"   • **Collaboration Effectiveness**: {session_progress.collaboration_effectiveness:.1f}/10")
        response_sections.append("")
        
        # Recommendations
        recommendations = self.generate_participation_recommendations(participation_status, session_progress)
        if recommendations:
            response_sections.append("💡 **Recommendations:**")
            for recommendation in recommendations:
                response_sections.append(f"   • {recommendation}")
            response_sections.append("")
        
        # Command shortcuts
        response_sections.append("🛠️ **Available Commands:**")
        if participation_status.full_team_enabled:
            response_sections.append("   • `/full_team_off` - Switch to selective agent mode")
        else:
            response_sections.append("   • `/full_team_on` - Enable full team participation")
        response_sections.append("   • `/agent-list` - View all available agents")
        response_sections.append("   • `/pre_select_agents` - Customize agent selection")
        
        return "\n".join(response_sections)
    
    def get_status_display(self, participation_status):
        """Get formatted status display with emoji"""
        
        status_displays = {
            "PENDING": "⏳ Pending",
            "ACTIVE": "🔄 Contributing",
            "CONTRIBUTED": "✅ Contributed",
            "COMPLETED": "✅ Complete",
            "INSUFFICIENT": "❌ Needs Improvement",
            "SKIPPED": "⏭️ Skipped"
        }
        
        return status_displays.get(participation_status, "❓ Unknown")
    
    def format_duration(self, duration_seconds):
        """Format duration in human-readable format"""
        
        if duration_seconds < 60:
            return f"{int(duration_seconds)}s"
        elif duration_seconds < 3600:
            minutes = int(duration_seconds / 60)
            seconds = int(duration_seconds % 60)
            return f"{minutes}m {seconds}s"
        else:
            hours = int(duration_seconds / 3600)
            minutes = int((duration_seconds % 3600) / 60)
            return f"{hours}h {minutes}m"
    
    def format_last_activity(self, last_activity_timestamp):
        """Format last activity timestamp"""
        
        if not last_activity_timestamp:
            return "Never"
        
        time_diff = time.time() - last_activity_timestamp
        
        if time_diff < 60:
            return "Just now"
        elif time_diff < 3600:
            minutes = int(time_diff / 60)
            return f"{minutes}m ago"
        elif time_diff < 86400:
            hours = int(time_diff / 3600)
            return f"{hours}h ago"
        else:
            days = int(time_diff / 86400)
            return f"{days}d ago"

    def group_agents_by_domain(self, secondary_agents):
        """Group secondary agents by domain for better organization"""

        domain_groups = {
            "Development & Architecture": [],
            "Quality & Validation": [],
            "Business & Strategy": [],
            "Process & Coordination": [],
            "Content & Documentation": [],
            "System & Integration": []
        }

        domain_mapping = {
            "Jane": "Development & Architecture",
            "Alex": "Development & Architecture",
            "James": "Development & Architecture",
            "Dakota": "Development & Architecture",
            "Sage": "Quality & Validation",
            "Sentinel": "Quality & Validation",
            "Creator": "System & Integration",
            "Phoenix": "System & Integration",
            "Synergy": "System & Integration",
            "Analyst": "Business & Strategy",
            "PO": "Business & Strategy",
            "Meta": "Business & Strategy",
            "SM": "Process & Coordination",
            "Chronos": "Process & Coordination",
            "DocQA": "Content & Documentation",
            "Chunky": "Content & Documentation"
        }

        for agent in secondary_agents:
            domain = domain_mapping.get(agent.name, "System & Integration")
            domain_groups[domain].append(agent)

        # Remove empty domains
        return {k: v for k, v in domain_groups.items() if v}

    def should_activate_specialized_agent(self, agent, session_context):
        """Determine if specialized agent should be activated based on project context"""

        project_requirements = session_context.project_requirements.lower()

        activation_rules = {
            "WebCreator": ["web", "browser", "frontend", "javascript", "react", "vue"],
            "IDEDev": ["ide", "vscode", "development environment", "tooling"],
            "DevOpsIDE": ["devops", "ci/cd", "deployment", "automation", "pipeline"],
            "AdvancedIDE": ["complex ide", "advanced tooling", "ide architecture"]
        }

        agent_keywords = activation_rules.get(agent.name, [])
        return any(keyword in project_requirements for keyword in agent_keywords)

    def group_agents_by_tier(self, agent_statuses):
        """Group agents by tier for status display"""

        tier_groups = {
            "Tier 1: Orchestrator": {},
            "Tier 2: Primary Agents": {},
            "Tier 3: Secondary Agents": {},
            "Tier 4: Specialized Agents": {}
        }

        tier_mapping = {
            "JAEGIS": "Tier 1: Orchestrator",
            "John": "Tier 2: Primary Agents",
            "Fred": "Tier 2: Primary Agents",
            "Tyler": "Tier 2: Primary Agents",
            "Jane": "Tier 3: Secondary Agents",
            "Alex": "Tier 3: Secondary Agents",
            "James": "Tier 3: Secondary Agents",
            "Sage": "Tier 3: Secondary Agents",
            "Dakota": "Tier 3: Secondary Agents",
            "Sentinel": "Tier 3: Secondary Agents",
            "DocQA": "Tier 3: Secondary Agents",
            "Creator": "Tier 3: Secondary Agents",
            "Analyst": "Tier 3: Secondary Agents",
            "Chronos": "Tier 3: Secondary Agents",
            "Chunky": "Tier 3: Secondary Agents",
            "Meta": "Tier 3: Secondary Agents",
            "Phoenix": "Tier 3: Secondary Agents",
            "PO": "Tier 3: Secondary Agents",
            "SM": "Tier 3: Secondary Agents",
            "Synergy": "Tier 3: Secondary Agents",
            "WebCreator": "Tier 4: Specialized Agents",
            "IDEDev": "Tier 4: Specialized Agents",
            "DevOpsIDE": "Tier 4: Specialized Agents",
            "AdvancedIDE": "Tier 4: Specialized Agents"
        }

        for agent_name, agent_status in agent_statuses.items():
            tier = tier_mapping.get(agent_name, "Tier 3: Secondary Agents")
            tier_groups[tier][agent_name] = agent_status

        # Remove empty tiers
        return {k: v for k, v in tier_groups.items() if v}
```

### 5. Command Integration and Compatibility

#### Enhanced Command System Integration
```python
class CommandSystemIntegration:
    """Integrate full team commands with existing command system"""
    
    def __init__(self):
        self.existing_commands = ExistingCommandRegistry()
        self.compatibility_manager = CompatibilityManager()
    
    def integrate_full_team_commands(self):
        """Integrate full team commands with existing system"""
        
        integration_results = {}
        
        # Enhance existing commands for full team compatibility
        integration_results["agent_list"] = self.enhance_agent_list_command()
        integration_results["pre_select_agents"] = self.enhance_pre_select_agents_command()
        integration_results["yolo_commands"] = self.enhance_yolo_commands()
        
        # Ensure command precedence and conflict resolution
        integration_results["precedence"] = self.establish_command_precedence()
        
        return CommandIntegrationResult(
            integration_results=integration_results,
            integration_success=all(result.success for result in integration_results.values())
        )
    
    def enhance_agent_list_command(self):
        """Enhance /agent-list command to show participation status"""
        
        # Add participation status indicators to agent list
        enhanced_features = [
            "participation_status_indicators",
            "full_team_mode_display",
            "contribution_counts",
            "quality_scores"
        ]
        
        return CommandEnhancementResult(
            command_name="agent_list",
            enhanced_features=enhanced_features,
            success=True
        )
```

### 6. Success Metrics and Validation

#### Command System Success Criteria
- **Command Functionality**: 100% successful execution of all three commands
- **Response Quality**: Clear, comprehensive, and actionable command responses
- **Integration Compatibility**: Seamless operation with existing command system
- **Performance**: < 2 seconds response time for all commands
- **Error Handling**: Comprehensive error handling with helpful guidance
- **User Experience**: Intuitive command usage with clear feedback

## Implementation Status

✅ **Command Architecture**: Complete command processing framework
✅ **Full Team On Command**: Comprehensive activation with detailed response
✅ **Full Team Off Command**: Complete deactivation with impact analysis
✅ **Full Team Status Command**: Detailed status display with insights
✅ **Integration Framework**: Command system integration and compatibility

**Next Steps**: Integrate commands with workflow systems, implement user interface enhancements, and validate complete command functionality.
