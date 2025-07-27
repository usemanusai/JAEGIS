#!/usr/bin/env python3
"""
e.J.A.E.G.I.S. Command Line Interface
Provides the `eJaegis` command for initializing and managing e.J.A.E.G.I.S. agents
"""

import asyncio
import click
import json
import sys
from pathlib import Path
from typing import Optional
import logging

# Import e.J.A.E.G.I.S. core components
sys.path.append(str(Path(__file__).parent.parent))
from core.eJaegis_agent import E-JAEGISAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('E-JAEGIS-CLI')

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    e.J.A.E.G.I.S. (Enhanced Multi-agent Architecture & Dependency Specialist)
    
    A perpetual, active background monitor for project codebases that identifies,
    analyzes, and reports on dependencies affected by code modifications.
    """
    pass

@cli.command()
@click.option('--project-root', '-p', default='.', help='Project root directory (default: current directory)')
@click.option('--neo4j-uri', default='bolt://localhost:7687', help='Neo4j database URI')
@click.option('--force', '-f', is_flag=True, help='Force re-initialization even if already initialized')
def init(project_root: str, neo4j_uri: str, force: bool):
    """
    Initialize e.J.A.E.G.I.S. in the current project.
    
    This command:
    1. Creates .eJaegis/ directory for local storage
    2. Builds the initial codebase knowledge graph
    3. Creates a template OWNERSHIP_LEDGER.json file
    4. Starts the local file system monitor
    """
    project_path = Path(project_root).resolve()
    
    if not project_path.exists():
        click.echo(f"❌ Error: Project directory {project_path} does not exist", err=True)
        sys.exit(1)
    
    eJaegis_dir = project_path / ".eJaegis"
    
    # Check if already initialized
    if eJaegis_dir.exists() and not force:
        click.echo(f"⚠️  e.J.A.E.G.I.S. already initialized in {project_path}")
        click.echo("Use --force to re-initialize")
        return
    
    click.echo(f"🚀 Initializing e.J.A.E.G.I.S. in {project_path}")
    
    async def init_agent():
        try:
            # Create e.J.A.E.G.I.S. agent
            agent = E-JAEGISAgent(project_path)
            
            # Initialize the agent
            await agent.initialize()
            
            # Create configuration file
            config = {
                "version": "1.0.0",
                "project_root": str(project_path),
                "neo4j_uri": neo4j_uri,
                "initialized_at": agent.knowledge_graph.components[list(agent.knowledge_graph.components.keys())[0]].last_modified.isoformat() if agent.knowledge_graph.components else None,
                "monitoring_enabled": True
            }
            
            config_file = eJaegis_dir / "config.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            click.echo(f"✅ e.J.A.E.G.I.S. initialized successfully!")
            click.echo(f"📁 Configuration stored in {eJaegis_dir}")
            click.echo(f"📊 Knowledge graph built with {len(agent.knowledge_graph.components)} components")
            click.echo(f"📋 Ownership ledger created at {project_path / 'OWNERSHIP_LEDGER.json'}")
            click.echo(f"👁️  File monitoring started")
            
            # Keep the agent running for a moment to demonstrate
            click.echo("🔄 e.J.A.E.G.I.S. is now monitoring your codebase...")
            click.echo("Press Ctrl+C to stop monitoring")
            
            try:
                # Keep running until interrupted
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                click.echo("\n🛑 Stopping e.J.A.E.G.I.S. monitoring...")
                await agent.shutdown()
                click.echo("✅ e.J.A.E.G.I.S. stopped successfully")
            
        except Exception as e:
            click.echo(f"❌ Error initializing e.J.A.E.G.I.S.: {e}", err=True)
            logger.error(f"Initialization error: {e}", exc_info=True)
            sys.exit(1)
    
    # Run the async initialization
    asyncio.run(init_agent())

@cli.command()
@click.option('--project-root', '-p', default='.', help='Project root directory')
def status(project_root: str):
    """
    Show e.J.A.E.G.I.S. status and statistics.
    """
    project_path = Path(project_root).resolve()
    eJaegis_dir = project_path / ".eJaegis"
    
    if not eJaegis_dir.exists():
        click.echo(f"❌ e.J.A.E.G.I.S. not initialized in {project_path}")
        click.echo("Run 'eJaegis init' to initialize")
        return
    
    # Load configuration
    config_file = eJaegis_dir / "config.json"
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        click.echo(f"📊 e.J.A.E.G.I.S. Status for {project_path}")
        click.echo(f"Version: {config.get('version', 'Unknown')}")
        click.echo(f"Initialized: {config.get('initialized_at', 'Unknown')}")
        click.echo(f"Monitoring: {'✅ Enabled' if config.get('monitoring_enabled') else '❌ Disabled'}")
    
    # Check for recent notifications
    notifications_file = eJaegis_dir / "ide_notifications.json"
    if notifications_file.exists():
        with open(notifications_file, 'r') as f:
            notifications = json.load(f)
        
        click.echo(f"\n📬 Recent Notifications: {len(notifications)}")
        for notification in notifications[-3:]:  # Show last 3
            click.echo(f"  • {notification.get('timestamp', '')}: {notification.get('message', '')}")
    
    # Check ownership ledger
    ledger_file = project_path / "OWNERSHIP_LEDGER.json"
    if ledger_file.exists():
        with open(ledger_file, 'r') as f:
            ledger = json.load(f)
        
        entries = ledger.get('ownership_entries', [])
        click.echo(f"\n👥 Ownership Entries: {len(entries)}")
        for entry in entries[:3]:  # Show first 3
            click.echo(f"  • {entry.get('pattern', '')}: {entry.get('owner_id', '')} ({entry.get('owner_type', '')})")

@cli.command()
@click.option('--project-root', '-p', default='.', help='Project root directory')
@click.option('--daemon', '-d', is_flag=True, help='Run as daemon process')
def monitor(project_root: str, daemon: bool):
    """
    Start e.J.A.E.G.I.S. monitoring service.
    """
    project_path = Path(project_root).resolve()
    eJaegis_dir = project_path / ".eJaegis"
    
    if not eJaegis_dir.exists():
        click.echo(f"❌ e.J.A.E.G.I.S. not initialized in {project_path}")
        click.echo("Run 'eJaegis init' to initialize")
        return
    
    click.echo(f"🔄 Starting e.J.A.E.G.I.S. monitoring for {project_path}")
    
    async def start_monitoring():
        try:
            agent = E-JAEGISAgent(project_path)
            await agent.initialize()
            
            click.echo("✅ e.J.A.E.G.I.S. monitoring started")
            click.echo("Press Ctrl+C to stop")
            
            if daemon:
                click.echo("🔧 Daemon mode not yet implemented - running in foreground")
            
            # Keep running until interrupted
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            click.echo("\n🛑 Stopping e.J.A.E.G.I.S. monitoring...")
            await agent.shutdown()
            click.echo("✅ e.J.A.E.G.I.S. stopped successfully")
        except Exception as e:
            click.echo(f"❌ Error running e.J.A.E.G.I.S.: {e}", err=True)
            logger.error(f"Monitoring error: {e}", exc_info=True)
    
    asyncio.run(start_monitoring())

@cli.command()
@click.option('--project-root', '-p', default='.', help='Project root directory')
@click.option('--file-path', '-f', help='Specific file to analyze')
def analyze(project_root: str, file_path: Optional[str]):
    """
    Analyze dependencies for a specific file or entire project.
    """
    project_path = Path(project_root).resolve()
    
    async def run_analysis():
        try:
            agent = E-JAEGISAgent(project_path)
            await agent.initialize()
            
            if file_path:
                # Analyze specific file
                file_to_analyze = Path(file_path).resolve()
                if not file_to_analyze.exists():
                    click.echo(f"❌ File not found: {file_to_analyze}")
                    return
                
                click.echo(f"🔍 Analyzing dependencies for {file_to_analyze}")
                
                # Simulate a change to analyze impact
                impact_tasks = await agent.impact_engine.analyze_impact(str(file_to_analyze))
                
                if impact_tasks:
                    click.echo(f"📊 Found {len(impact_tasks)} potential impacts:")
                    for task in impact_tasks:
                        click.echo(f"  • {task.affected_component} ({task.impact_level} impact)")
                        click.echo(f"    Owner: {task.owner.owner_id}")
                        for action in task.suggested_actions[:2]:  # Show first 2 actions
                            click.echo(f"    - {action}")
                else:
                    click.echo("✅ No dependencies found or no impact detected")
            else:
                # Analyze entire project
                click.echo(f"🔍 Analyzing project dependencies for {project_path}")
                
                components = len(agent.knowledge_graph.components)
                click.echo(f"📊 Total components analyzed: {components}")
                
                # Show some statistics
                file_types = {}
                for comp in agent.knowledge_graph.components.values():
                    ext = Path(comp.file_path).suffix
                    file_types[ext] = file_types.get(ext, 0) + 1
                
                click.echo("📁 File types:")
                for ext, count in sorted(file_types.items()):
                    click.echo(f"  {ext}: {count} components")
            
            await agent.shutdown()
            
        except Exception as e:
            click.echo(f"❌ Error during analysis: {e}", err=True)
            logger.error(f"Analysis error: {e}", exc_info=True)
    
    asyncio.run(run_analysis())

@cli.command()
@click.option('--project-root', '-p', default='.', help='Project root directory')
def configure(project_root: str):
    """
    Configure e.J.A.E.G.I.S. settings and ownership ledger.
    """
    project_path = Path(project_root).resolve()
    ledger_file = project_path / "OWNERSHIP_LEDGER.json"
    
    if not ledger_file.exists():
        click.echo(f"❌ Ownership ledger not found at {ledger_file}")
        click.echo("Run 'eJaegis init' to initialize")
        return
    
    click.echo(f"⚙️  e.J.A.E.G.I.S. Configuration for {project_path}")
    click.echo(f"📋 Ownership ledger: {ledger_file}")
    click.echo("\nTo configure e.J.A.E.G.I.S.:")
    click.echo("1. Edit the OWNERSHIP_LEDGER.json file to define code ownership")
    click.echo("2. Modify patterns to match your project structure")
    click.echo("3. Set appropriate owners and notification methods")
    click.echo("4. Restart monitoring with 'eJaegis monitor'")
    
    # Show current configuration
    with open(ledger_file, 'r') as f:
        ledger = json.load(f)
    
    entries = ledger.get('ownership_entries', [])
    click.echo(f"\n👥 Current Ownership Entries ({len(entries)}):")
    for i, entry in enumerate(entries, 1):
        click.echo(f"{i}. Pattern: {entry.get('pattern', '')}")
        click.echo(f"   Owner: {entry.get('owner_id', '')} ({entry.get('owner_type', '')})")
        click.echo(f"   Contact: {entry.get('contact_method', '')}")
        click.echo(f"   Priority: {entry.get('priority', '')}")
        click.echo()

if __name__ == '__main__':
    cli()
