"""
JAEGIS Expansion Pack Framework
Implements modular system for domain-specific expansion packs with standardized API
"""

import json
import yaml
import uuid
import importlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Type, Protocol
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import semver

class PackStatus(Enum):
    DISCOVERED = "discovered"
    VALIDATED = "validated"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"

class ComponentType(Enum):
    AGENT = "agent"
    TEMPLATE = "template"
    WORKFLOW = "workflow"
    INTEGRATION = "integration"
    DATA_SOURCE = "data_source"

@dataclass
class PackMetadata:
    """Metadata for expansion pack"""
    pack_id: str
    pack_name: str
    version: str
    description: str
    author: str
    license: str
    homepage: Optional[str] = None
    repository: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    created_date: Optional[str] = None
    updated_date: Optional[str] = None

@dataclass
class PackDependencies:
    """Dependencies for expansion pack"""
    core_version: str  # Minimum JAEGIS version required
    required_packs: List[str] = field(default_factory=list)
    optional_packs: List[str] = field(default_factory=list)
    python_packages: List[str] = field(default_factory=list)
    system_requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PackCapabilities:
    """Capabilities provided by expansion pack"""
    provided_agents: List[str] = field(default_factory=list)
    provided_templates: List[str] = field(default_factory=list)
    provided_workflows: List[str] = field(default_factory=list)
    provided_integrations: List[str] = field(default_factory=list)
    provided_data_sources: List[str] = field(default_factory=list)
    extension_points: List[str] = field(default_factory=list)

@dataclass
class PackConfiguration:
    """Configuration schema and defaults for expansion pack"""
    settings_schema: Dict[str, Any] = field(default_factory=dict)
    default_settings: Dict[str, Any] = field(default_factory=dict)
    validation_rules: List[str] = field(default_factory=list)
    environment_variables: List[str] = field(default_factory=list)

@dataclass
class ExpansionPack:
    """Complete expansion pack definition"""
    metadata: PackMetadata
    dependencies: PackDependencies
    capabilities: PackCapabilities
    configuration: PackConfiguration
    manifest_path: Path
    pack_path: Path
    status: PackStatus = PackStatus.DISCOVERED
    load_time: Optional[datetime] = None
    error_message: Optional[str] = None
    loaded_components: Dict[str, Any] = field(default_factory=dict)

# Protocol definitions for expansion pack components
class JAEGISAgent(Protocol):
    """Protocol for JAEGIS agents"""
    def initialize(self, config: Dict[str, Any]) -> bool: ...
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]: ...
    def cleanup(self) -> None: ...

class JAEGISTemplate(Protocol):
    """Protocol for JAEGIS templates"""
    def render(self, context: Dict[str, Any]) -> str: ...
    def validate(self, content: str) -> Dict[str, Any]: ...
    def get_schema(self) -> Dict[str, Any]: ...

class JAEGISWorkflow(Protocol):
    """Protocol for JAEGIS workflows"""
    def define_steps(self) -> List[Dict[str, Any]]: ...
    def execute_step(self, step_id: str, context: Dict[str, Any]) -> Dict[str, Any]: ...
    def handle_transition(self, from_step: str, to_step: str, context: Dict[str, Any]) -> bool: ...

class ExpansionPackRegistry:
    """Registry for managing expansion packs"""
    
    def __init__(self, core_version: str = "1.0.0"):
        self.core_version = core_version
        self.registered_packs: Dict[str, ExpansionPack] = {}
        self.active_packs: Dict[str, ExpansionPack] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        self.component_registry: Dict[ComponentType, Dict[str, Any]] = {
            ComponentType.AGENT: {},
            ComponentType.TEMPLATE: {},
            ComponentType.WORKFLOW: {},
            ComponentType.INTEGRATION: {},
            ComponentType.DATA_SOURCE: {}
        }
        
    def discover_packs(self, search_paths: List[Path]) -> List[ExpansionPack]:
        """Discover expansion packs in specified directories"""
        
        discovered_packs = []
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
                
            # Look for pack manifests
            for manifest_path in search_path.rglob("jaegis-pack.yaml"):
                try:
                    pack = self._load_pack_manifest(manifest_path)
                    discovered_packs.append(pack)
                    self.registered_packs[pack.metadata.pack_id] = pack
                except Exception as e:
                    print(f"Error loading pack manifest {manifest_path}: {e}")
        
        return discovered_packs
    
    def _load_pack_manifest(self, manifest_path: Path) -> ExpansionPack:
        """Load expansion pack from manifest file"""
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = yaml.safe_load(f)
        
        # Parse metadata
        metadata = PackMetadata(
            pack_id=manifest_data['metadata']['pack_id'],
            pack_name=manifest_data['metadata']['pack_name'],
            version=manifest_data['metadata']['version'],
            description=manifest_data['metadata']['description'],
            author=manifest_data['metadata']['author'],
            license=manifest_data['metadata']['license'],
            homepage=manifest_data['metadata'].get('homepage'),
            repository=manifest_data['metadata'].get('repository'),
            keywords=manifest_data['metadata'].get('keywords', []),
            created_date=manifest_data['metadata'].get('created_date'),
            updated_date=manifest_data['metadata'].get('updated_date')
        )
        
        # Parse dependencies
        deps_data = manifest_data.get('dependencies', {})
        dependencies = PackDependencies(
            core_version=deps_data.get('core_version', '1.0.0'),
            required_packs=deps_data.get('required_packs', []),
            optional_packs=deps_data.get('optional_packs', []),
            python_packages=deps_data.get('python_packages', []),
            system_requirements=deps_data.get('system_requirements', {})
        )
        
        # Parse capabilities
        caps_data = manifest_data.get('capabilities', {})
        capabilities = PackCapabilities(
            provided_agents=caps_data.get('provided_agents', []),
            provided_templates=caps_data.get('provided_templates', []),
            provided_workflows=caps_data.get('provided_workflows', []),
            provided_integrations=caps_data.get('provided_integrations', []),
            provided_data_sources=caps_data.get('provided_data_sources', []),
            extension_points=caps_data.get('extension_points', [])
        )
        
        # Parse configuration
        config_data = manifest_data.get('configuration', {})
        configuration = PackConfiguration(
            settings_schema=config_data.get('settings_schema', {}),
            default_settings=config_data.get('default_settings', {}),
            validation_rules=config_data.get('validation_rules', []),
            environment_variables=config_data.get('environment_variables', [])
        )
        
        pack = ExpansionPack(
            metadata=metadata,
            dependencies=dependencies,
            capabilities=capabilities,
            configuration=configuration,
            manifest_path=manifest_path,
            pack_path=manifest_path.parent
        )
        
        return pack
    
    def validate_pack(self, pack: ExpansionPack) -> bool:
        """Validate expansion pack for compatibility and correctness"""
        
        try:
            # Check core version compatibility
            if not self._check_version_compatibility(pack.dependencies.core_version, self.core_version):
                pack.status = PackStatus.ERROR
                pack.error_message = f"Incompatible core version. Required: {pack.dependencies.core_version}, Available: {self.core_version}"
                return False
            
            # Check required dependencies
            for required_pack in pack.dependencies.required_packs:
                if required_pack not in self.registered_packs:
                    pack.status = PackStatus.ERROR
                    pack.error_message = f"Required dependency not found: {required_pack}"
                    return False
            
            # Validate pack structure
            if not self._validate_pack_structure(pack):
                pack.status = PackStatus.ERROR
                pack.error_message = "Invalid pack structure"
                return False
            
            # Validate component definitions
            if not self._validate_component_definitions(pack):
                pack.status = PackStatus.ERROR
                pack.error_message = "Invalid component definitions"
                return False
            
            pack.status = PackStatus.VALIDATED
            return True
            
        except Exception as e:
            pack.status = PackStatus.ERROR
            pack.error_message = f"Validation error: {str(e)}"
            return False
    
    def load_pack(self, pack_id: str) -> bool:
        """Load expansion pack components"""
        
        pack = self.registered_packs.get(pack_id)
        if not pack:
            return False
        
        if pack.status != PackStatus.VALIDATED:
            if not self.validate_pack(pack):
                return False
        
        try:
            # Load dependencies first
            for dep_pack_id in pack.dependencies.required_packs:
                if dep_pack_id not in self.active_packs:
                    if not self.load_pack(dep_pack_id):
                        pack.status = PackStatus.ERROR
                        pack.error_message = f"Failed to load dependency: {dep_pack_id}"
                        return False
            
            # Load pack components
            loaded_components = {}
            
            # Load agents
            for agent_id in pack.capabilities.provided_agents:
                agent_class = self._load_component(pack, ComponentType.AGENT, agent_id)
                if agent_class:
                    loaded_components[f"agent_{agent_id}"] = agent_class
                    self.component_registry[ComponentType.AGENT][agent_id] = agent_class
            
            # Load templates
            for template_id in pack.capabilities.provided_templates:
                template_class = self._load_component(pack, ComponentType.TEMPLATE, template_id)
                if template_class:
                    loaded_components[f"template_{template_id}"] = template_class
                    self.component_registry[ComponentType.TEMPLATE][template_id] = template_class
            
            # Load workflows
            for workflow_id in pack.capabilities.provided_workflows:
                workflow_class = self._load_component(pack, ComponentType.WORKFLOW, workflow_id)
                if workflow_class:
                    loaded_components[f"workflow_{workflow_id}"] = workflow_class
                    self.component_registry[ComponentType.WORKFLOW][workflow_id] = workflow_class
            
            pack.loaded_components = loaded_components
            pack.status = PackStatus.LOADED
            pack.load_time = datetime.now()
            
            return True
            
        except Exception as e:
            pack.status = PackStatus.ERROR
            pack.error_message = f"Load error: {str(e)}"
            return False
    
    def activate_pack(self, pack_id: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """Activate expansion pack"""
        
        pack = self.registered_packs.get(pack_id)
        if not pack:
            return False
        
        if pack.status != PackStatus.LOADED:
            if not self.load_pack(pack_id):
                return False
        
        try:
            # Apply configuration
            if config:
                pack_config = {**pack.configuration.default_settings, **config}
            else:
                pack_config = pack.configuration.default_settings
            
            # Initialize components
            for component_name, component_class in pack.loaded_components.items():
                if hasattr(component_class, 'initialize'):
                    component_class.initialize(pack_config)
            
            pack.status = PackStatus.ACTIVE
            self.active_packs[pack_id] = pack
            
            return True
            
        except Exception as e:
            pack.status = PackStatus.ERROR
            pack.error_message = f"Activation error: {str(e)}"
            return False
    
    def deactivate_pack(self, pack_id: str) -> bool:
        """Deactivate expansion pack"""
        
        pack = self.active_packs.get(pack_id)
        if not pack:
            return False
        
        try:
            # Cleanup components
            for component_name, component_class in pack.loaded_components.items():
                if hasattr(component_class, 'cleanup'):
                    component_class.cleanup()
            
            # Remove from active packs
            del self.active_packs[pack_id]
            pack.status = PackStatus.LOADED
            
            return True
            
        except Exception as e:
            pack.error_message = f"Deactivation error: {str(e)}"
            return False
    
    def get_component(self, component_type: ComponentType, component_id: str) -> Optional[Any]:
        """Get component by type and ID"""
        return self.component_registry[component_type].get(component_id)
    
    def list_components(self, component_type: ComponentType) -> List[str]:
        """List available components of specified type"""
        return list(self.component_registry[component_type].keys())
    
    def _check_version_compatibility(self, required_version: str, available_version: str) -> bool:
        """Check if versions are compatible"""
        try:
            return semver.compare(available_version, required_version) >= 0
        except:
            # Fallback to simple string comparison if semver fails
            return available_version >= required_version
    
    def _validate_pack_structure(self, pack: ExpansionPack) -> bool:
        """Validate pack directory structure"""
        
        required_dirs = ['agents', 'templates', 'workflows']
        
        for dir_name in required_dirs:
            dir_path = pack.pack_path / dir_name
            if not dir_path.exists():
                # Create directory if it doesn't exist but is needed
                if (dir_name == 'agents' and pack.capabilities.provided_agents) or \
                   (dir_name == 'templates' and pack.capabilities.provided_templates) or \
                   (dir_name == 'workflows' and pack.capabilities.provided_workflows):
                    return False
        
        return True
    
    def _validate_component_definitions(self, pack: ExpansionPack) -> bool:
        """Validate component definitions"""
        
        # Check that all declared components have corresponding files
        for agent_id in pack.capabilities.provided_agents:
            agent_file = pack.pack_path / 'agents' / f'{agent_id}.py'
            if not agent_file.exists():
                return False
        
        for template_id in pack.capabilities.provided_templates:
            template_file = pack.pack_path / 'templates' / f'{template_id}.yaml'
            if not template_file.exists():
                return False
        
        for workflow_id in pack.capabilities.provided_workflows:
            workflow_file = pack.pack_path / 'workflows' / f'{workflow_id}.py'
            if not workflow_file.exists():
                return False
        
        return True
    
    def _load_component(self, pack: ExpansionPack, component_type: ComponentType, component_id: str) -> Optional[Any]:
        """Load individual component from pack"""
        
        try:
            if component_type == ComponentType.AGENT:
                module_path = f"{pack.pack_path.name}.agents.{component_id}"
                module = importlib.import_module(module_path)
                return getattr(module, f"{component_id.title()}Agent")
            
            elif component_type == ComponentType.TEMPLATE:
                template_file = pack.pack_path / 'templates' / f'{component_id}.yaml'
                with open(template_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            
            elif component_type == ComponentType.WORKFLOW:
                module_path = f"{pack.pack_path.name}.workflows.{component_id}"
                module = importlib.import_module(module_path)
                return getattr(module, f"{component_id.title()}Workflow")
            
            return None
            
        except Exception as e:
            print(f"Error loading component {component_id}: {e}")
            return None

class ExpansionPackManager:
    """High-level manager for expansion pack operations"""
    
    def __init__(self, core_version: str = "1.0.0"):
        self.registry = ExpansionPackRegistry(core_version)
        self.pack_directories = []
        
    def add_pack_directory(self, directory: Path) -> None:
        """Add directory to search for expansion packs"""
        self.pack_directories.append(directory)
    
    def refresh_packs(self) -> List[ExpansionPack]:
        """Refresh pack registry by discovering packs in all directories"""
        return self.registry.discover_packs(self.pack_directories)
    
    def install_pack(self, pack_path: Path, activate: bool = True) -> bool:
        """Install expansion pack from path"""
        
        try:
            # Copy pack to managed directory if needed
            # Validate and register pack
            pack = self.registry._load_pack_manifest(pack_path / "jaegis-pack.yaml")
            
            if self.registry.validate_pack(pack):
                self.registry.registered_packs[pack.metadata.pack_id] = pack
                
                if activate:
                    return self.registry.activate_pack(pack.metadata.pack_id)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error installing pack: {e}")
            return False
    
    def uninstall_pack(self, pack_id: str) -> bool:
        """Uninstall expansion pack"""
        
        try:
            # Deactivate if active
            if pack_id in self.registry.active_packs:
                self.registry.deactivate_pack(pack_id)
            
            # Remove from registry
            if pack_id in self.registry.registered_packs:
                del self.registry.registered_packs[pack_id]
            
            return True
            
        except Exception as e:
            print(f"Error uninstalling pack: {e}")
            return False
    
    def get_pack_info(self, pack_id: str) -> Optional[Dict[str, Any]]:
        """Get information about expansion pack"""
        
        pack = self.registry.registered_packs.get(pack_id)
        if not pack:
            return None
        
        return {
            'metadata': pack.metadata.__dict__,
            'dependencies': pack.dependencies.__dict__,
            'capabilities': pack.capabilities.__dict__,
            'status': pack.status.value,
            'load_time': pack.load_time.isoformat() if pack.load_time else None,
            'error_message': pack.error_message
        }
    
    def list_packs(self, status_filter: Optional[PackStatus] = None) -> List[Dict[str, Any]]:
        """List all registered packs"""
        
        packs = []
        for pack_id, pack in self.registry.registered_packs.items():
            if status_filter is None or pack.status == status_filter:
                packs.append({
                    'pack_id': pack_id,
                    'pack_name': pack.metadata.pack_name,
                    'version': pack.metadata.version,
                    'status': pack.status.value,
                    'description': pack.metadata.description
                })
        
        return packs
    
    def get_available_components(self) -> Dict[str, List[str]]:
        """Get all available components from active packs"""
        
        return {
            'agents': self.registry.list_components(ComponentType.AGENT),
            'templates': self.registry.list_components(ComponentType.TEMPLATE),
            'workflows': self.registry.list_components(ComponentType.WORKFLOW),
            'integrations': self.registry.list_components(ComponentType.INTEGRATION),
            'data_sources': self.registry.list_components(ComponentType.DATA_SOURCE)
        }

# Example usage
if __name__ == "__main__":
    # Initialize expansion pack manager
    manager = ExpansionPackManager("1.0.0")
    
    # Add pack directories
    manager.add_pack_directory(Path("./expansion-packs"))
    
    # Discover packs
    discovered_packs = manager.refresh_packs()
    print(f"Discovered {len(discovered_packs)} expansion packs")
    
    # List all packs
    all_packs = manager.list_packs()
    for pack in all_packs:
        print(f"Pack: {pack['pack_name']} v{pack['version']} - {pack['status']}")
    
    # Get available components
    components = manager.get_available_components()
    print(f"Available components: {components}")
