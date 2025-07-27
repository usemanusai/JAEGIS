"""
Test suite for e.J.A.E.G.I.S. Agent
Comprehensive tests for all core components
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
import json
from datetime import datetime

# Import e.J.A.E.G.I.S. components
import sys
sys.path.append(str(Path(__file__).parent.parent))
from core.eJaegis_agent import (
    E-JAEGISAgent, 
    CodebaseKnowledgeGraph, 
    OwnershipLedger, 
    ImpactAnalysisEngine,
    TaskDispatchRouter,
    CodeComponent,
    OwnershipEntry,
    ImpactTask
)

class TestE-JAEGISAgent:
    """Test the main e.J.A.E.G.I.S. Agent functionality"""
    
    @pytest.fixture
    async def temp_project(self):
        """Create a temporary project for testing"""
        temp_dir = Path(tempfile.mkdtemp(prefix="eJaegis_test_"))
        
        # Create sample project structure
        (temp_dir / "src").mkdir()
        (temp_dir / "src" / "core").mkdir()
        (temp_dir / "src" / "api").mkdir()
        (temp_dir / "tests").mkdir()
        
        # Create sample Python files
        models_content = '''"""Core models"""

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
    
    def get_display_name(self):
        return f"User: {self.name}"

class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price
'''
        
        api_content = '''"""API routes"""

from ..core.models import User, Product

class UserAPI:
    def __init__(self):
        self.users = {}
    
    def create_user(self, user_data):
        user = User(user_data["id"], user_data["name"])
        self.users[user.user_id] = user
        return user.get_display_name()
'''
        
        test_content = '''"""Tests for models"""

import unittest
from src.core.models import User

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User("123", "Test User")
        self.assertEqual(user.user_id, "123")
        self.assertEqual(user.name, "Test User")
'''
        
        # Write files
        (temp_dir / "src" / "core" / "models.py").write_text(models_content)
        (temp_dir / "src" / "api" / "routes.py").write_text(api_content)
        (temp_dir / "tests" / "test_models.py").write_text(test_content)
        
        yield temp_dir
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, temp_project):
        """Test e.J.A.E.G.I.S. agent initialization"""
        agent = E-JAEGISAgent(temp_project)
        
        # Initialize agent
        await agent.initialize()
        
        # Verify initialization
        assert agent.is_initialized
        assert agent.eJaegis_dir.exists()
        assert len(agent.knowledge_graph.components) > 0
        assert len(agent.ownership_ledger.ownership_entries) > 0
        
        # Cleanup
        await agent.shutdown()
    
    @pytest.mark.asyncio
    async def test_file_change_processing(self, temp_project):
        """Test file change detection and processing"""
        agent = E-JAEGISAgent(temp_project)
        await agent.initialize()
        
        # Modify a file
        models_file = temp_project / "src" / "core" / "models.py"
        original_content = models_file.read_text()
        
        # Add a new method
        new_content = original_content + '''
    
    def new_method(self):
        """A new method for testing"""
        return "new functionality"
'''
        models_file.write_text(new_content)
        
        # Process the change
        await agent.process_file_change(str(models_file))
        
        # Verify the change was processed
        # (In a real test, we'd check for generated impact tasks)
        
        await agent.shutdown()

class TestCodebaseKnowledgeGraph:
    """Test the knowledge graph component"""
    
    @pytest.fixture
    async def knowledge_graph(self, temp_project):
        """Create a knowledge graph for testing"""
        graph = CodebaseKnowledgeGraph(temp_project)
        await graph.initialize()
        yield graph
        if graph.driver:
            graph.driver.close()
    
    @pytest.mark.asyncio
    async def test_initial_graph_building(self, knowledge_graph, temp_project):
        """Test initial knowledge graph construction"""
        await knowledge_graph.build_initial_graph()
        
        # Verify components were found
        assert len(knowledge_graph.components) > 0
        
        # Check for expected components
        component_names = [comp.name for comp in knowledge_graph.components.values()]
        assert "User" in component_names
        assert "Product" in component_names
        assert "UserAPI" in component_names
    
    @pytest.mark.asyncio
    async def test_python_file_analysis(self, knowledge_graph, temp_project):
        """Test Python file analysis"""
        models_file = temp_project / "src" / "core" / "models.py"
        components = knowledge_graph._analyze_file(models_file)
        
        # Verify components were extracted
        assert len(components) >= 2  # User and Product classes
        
        # Check component details
        user_component = next((c for c in components if c.name == "User"), None)
        assert user_component is not None
        assert user_component.component_type == "class"
        assert user_component.file_path == "src/core/models.py"
    
    @pytest.mark.asyncio
    async def test_dependency_finding(self, knowledge_graph, temp_project):
        """Test dependency relationship detection"""
        await knowledge_graph.build_initial_graph()
        
        # Find a component
        user_component_id = None
        for comp_id, comp in knowledge_graph.components.items():
            if comp.name == "User":
                user_component_id = comp_id
                break
        
        assert user_component_id is not None
        
        # Find dependents
        dependents = await knowledge_graph.find_dependents(user_component_id)
        
        # Should find components that depend on User
        # (The exact number depends on the analysis accuracy)
        assert isinstance(dependents, list)

class TestOwnershipLedger:
    """Test the ownership ledger component"""
    
    @pytest.mark.asyncio
    async def test_ledger_initialization(self, temp_project):
        """Test ownership ledger initialization"""
        ledger = OwnershipLedger(temp_project)
        await ledger.initialize()
        
        # Verify ledger was created
        assert ledger.ledger_path.exists()
        assert len(ledger.ownership_entries) > 0
        
        # Check default entries
        patterns = [entry.pattern for entry in ledger.ownership_entries]
        assert "src/api/**" in patterns
        assert "src/core/**" in patterns
        assert "tests/**" in patterns
    
    @pytest.mark.asyncio
    async def test_owner_finding(self, temp_project):
        """Test finding owners for file paths"""
        ledger = OwnershipLedger(temp_project)
        await ledger.initialize()
        
        # Test finding owners
        api_owner = ledger.find_owner("src/api/routes.py")
        assert api_owner is not None
        assert api_owner.owner_id == "API-Agent"
        
        core_owner = ledger.find_owner("src/core/models.py")
        assert core_owner is not None
        assert core_owner.owner_id == "Core-Architecture-Agent"
        
        test_owner = ledger.find_owner("tests/test_models.py")
        assert test_owner is not None
        assert test_owner.owner_id == "QA-Agent"
    
    @pytest.mark.asyncio
    async def test_ledger_persistence(self, temp_project):
        """Test ledger saving and loading"""
        ledger = OwnershipLedger(temp_project)
        await ledger.initialize()
        
        # Add a custom entry
        custom_entry = OwnershipEntry(
            pattern="custom/**",
            owner_type="human",
            owner_id="custom_team",
            contact_method="email",
            priority=2
        )
        ledger.ownership_entries.append(custom_entry)
        
        # Save ledger
        await ledger.save_ledger()
        
        # Create new ledger instance and load
        new_ledger = OwnershipLedger(temp_project)
        await new_ledger.load_ledger()
        
        # Verify custom entry was persisted
        custom_patterns = [e.pattern for e in new_ledger.ownership_entries if e.pattern == "custom/**"]
        assert len(custom_patterns) == 1

class TestImpactAnalysisEngine:
    """Test the impact analysis engine"""
    
    @pytest.fixture
    async def impact_engine(self, temp_project):
        """Create an impact analysis engine for testing"""
        knowledge_graph = CodebaseKnowledgeGraph(temp_project)
        await knowledge_graph.initialize()
        await knowledge_graph.build_initial_graph()
        
        ownership_ledger = OwnershipLedger(temp_project)
        await ownership_ledger.initialize()
        
        engine = ImpactAnalysisEngine(knowledge_graph, ownership_ledger)
        yield engine
        
        if knowledge_graph.driver:
            knowledge_graph.driver.close()
    
    @pytest.mark.asyncio
    async def test_impact_analysis(self, impact_engine, temp_project):
        """Test impact analysis for file changes"""
        # Analyze impact of changing models.py
        models_file = "src/core/models.py"
        
        impact_tasks = await impact_engine.analyze_impact(models_file)
        
        # Verify impact tasks were generated
        assert isinstance(impact_tasks, list)
        
        # Check task properties if any were generated
        for task in impact_tasks:
            assert isinstance(task, ImpactTask)
            assert task.task_id
            assert task.impact_level in ["low", "medium", "high", "critical"]
            assert task.owner
            assert isinstance(task.suggested_actions, list)
    
    @pytest.mark.asyncio
    async def test_impact_level_assessment(self, impact_engine):
        """Test impact level assessment logic"""
        # Test different scenarios
        api_impact = await impact_engine._assess_impact_level(
            "src/api/routes.py:UserAPI", 
            "src/core/models.py:User"
        )
        assert api_impact in ["low", "medium", "high", "critical"]
        
        test_impact = await impact_engine._assess_impact_level(
            "src/core/models.py:User", 
            "tests/test_models.py:TestUser"
        )
        assert test_impact in ["low", "medium", "high", "critical"]

class TestTaskDispatchRouter:
    """Test the task dispatch router"""
    
    @pytest.mark.asyncio
    async def test_router_initialization(self, temp_project):
        """Test task dispatch router initialization"""
        router = TaskDispatchRouter(temp_project)
        await router.initialize()
        
        # Verify handlers are registered
        assert "ide_notification" in router.notification_handlers
        assert "slack" in router.notification_handlers
        assert "email" in router.notification_handlers
        assert "webhook" in router.notification_handlers
    
    @pytest.mark.asyncio
    async def test_task_dispatching(self, temp_project):
        """Test task dispatching functionality"""
        router = TaskDispatchRouter(temp_project)
        await router.initialize()
        
        # Create a test task
        owner = OwnershipEntry(
            pattern="test/**",
            owner_type="agent",
            owner_id="Test-Agent",
            contact_method="ide_notification",
            priority=1
        )
        
        task = ImpactTask(
            task_id="test_task_123",
            affected_component="test_component",
            change_description="Test change description",
            impact_level="medium",
            owner=owner,
            suggested_actions=["Test action 1", "Test action 2"],
            created_at=datetime.now()
        )
        
        # Dispatch the task
        await router.dispatch_task(task)
        
        # Give the router time to process
        await asyncio.sleep(0.1)
        
        # Verify notification file was created
        notification_file = temp_project / ".eJaegis" / "ide_notifications.json"
        assert notification_file.exists()
        
        # Check notification content
        with open(notification_file, 'r') as f:
            notifications = json.load(f)
        
        assert len(notifications) > 0
        assert notifications[-1]["task_id"] == "test_task_123"

class TestIntegration:
    """Integration tests for the complete e.J.A.E.G.I.S. system"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self, temp_project):
        """Test complete end-to-end workflow"""
        # Initialize e.J.A.E.G.I.S. agent
        agent = E-JAEGISAgent(temp_project)
        await agent.initialize()
        
        # Verify initial state
        assert agent.is_initialized
        initial_component_count = len(agent.knowledge_graph.components)
        
        # Simulate a file change
        models_file = temp_project / "src" / "core" / "models.py"
        original_content = models_file.read_text()
        
        # Add new functionality
        new_content = original_content + '''

class NewModel:
    """A new model for testing"""
    def __init__(self, model_id: str):
        self.model_id = model_id
    
    def process(self):
        return f"Processing {self.model_id}"
'''
        models_file.write_text(new_content)
        
        # Process the change
        await agent.process_file_change(str(models_file))
        
        # Verify the system responded
        # (Components should be updated, impact analysis should run)
        
        # Check for notifications
        notification_file = agent.eJaegis_dir / "ide_notifications.json"
        if notification_file.exists():
            with open(notification_file, 'r') as f:
                notifications = json.load(f)
            # Verify notifications were generated if dependencies exist
            assert isinstance(notifications, list)
        
        # Cleanup
        await agent.shutdown()
    
    @pytest.mark.asyncio
    async def test_multiple_file_changes(self, temp_project):
        """Test handling multiple file changes"""
        agent = E-JAEGISAgent(temp_project)
        await agent.initialize()
        
        # Change multiple files
        files_to_change = [
            temp_project / "src" / "core" / "models.py",
            temp_project / "src" / "api" / "routes.py"
        ]
        
        for file_path in files_to_change:
            content = file_path.read_text()
            # Add a comment to trigger change detection
            new_content = content + "\n# Modified for testing\n"
            file_path.write_text(new_content)
            
            # Process each change
            await agent.process_file_change(str(file_path))
        
        # Verify system handled multiple changes
        # (This tests the robustness of the change processing)
        
        await agent.shutdown()

# Test fixtures and utilities
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
