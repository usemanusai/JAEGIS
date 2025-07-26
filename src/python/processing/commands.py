"""
JAEGIS Command Extractor
Advanced command extraction and processing from markdown content

@version 2.0.0
@author JAEGIS Development Team
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class Command:
    """Represents a parsed command with metadata."""
    name: str
    description: str
    usage: str
    examples: List[str]
    category: str
    aliases: List[str]
    parameters: List[Dict[str, Any]]
    response_type: str
    priority: str = "normal"
    requires_github_data: bool = False

@dataclass
class CommandCategory:
    """Represents a command category."""
    name: str
    description: str
    commands: List[str]
    icon: str = ""

class CommandExtractor:
    """Advanced command extraction from markdown content."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.command_patterns = self._compile_patterns()
        self.categories = {}
        self.commands = {}
        
    async def initialize(self):
        """Initialize the command extractor."""
        logger.info("🎯 Initializing Command Extractor...")
        logger.info("✅ Command Extractor initialized successfully")
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for command extraction."""
        return {
            'command_header': re.compile(r'^### `(/[^`]+)`', re.MULTILINE),
            'description': re.compile(r'\*\*Description:\*\* (.+)', re.MULTILINE),
            'usage': re.compile(r'\*\*Usage:\*\* `([^`]+)`', re.MULTILINE),
            'examples': re.compile(r'- `([^`]+)` - (.+)', re.MULTILINE),
            'category_header': re.compile(r'^## 🎯 (.+)', re.MULTILINE),
            'options': re.compile(r'\*\*Options:\*\*\n((?:- .+\n?)+)', re.MULTILINE),
            'parameters': re.compile(r'- `([^`]+)` - (.+)', re.MULTILINE),
            'response': re.compile(r'\*\*Response:\*\* (.+)', re.MULTILINE),
            'aliases': re.compile(r'\*\*Aliases:\*\* (.+)', re.MULTILINE)
        }
    
    async def extract_commands(self, content: str, format: str = "markdown", extract_metadata: bool = True) -> Dict[str, Any]:
        """
        Extract commands from content.
        
        Args:
            content: The content to parse
            format: Content format (markdown, json, etc.)
            extract_metadata: Whether to extract detailed metadata
            
        Returns:
            Dictionary containing extracted commands and metadata
        """
        logger.info("📝 Extracting commands from content...")
        
        try:
            if format.lower() == "markdown":
                result = await self._extract_from_markdown(content, extract_metadata)
            elif format.lower() == "json":
                result = await self._extract_from_json(content, extract_metadata)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"✅ Extracted {len(result.get('commands', []))} commands")
            return result
            
        except Exception as e:
            logger.error(f"Command extraction failed: {e}")
            raise
    
    async def _extract_from_markdown(self, content: str, extract_metadata: bool) -> Dict[str, Any]:
        """Extract commands from markdown content."""
        commands = []
        categories = {}
        current_category = "General"
        
        # Split content into sections
        sections = self._split_into_sections(content)
        
        for section in sections:
            # Check if this is a category header
            category_match = self.command_patterns['category_header'].search(section)
            if category_match:
                current_category = self._clean_category_name(category_match.group(1))
                categories[current_category] = {
                    'name': current_category,
                    'description': self._extract_category_description(section),
                    'commands': [],
                    'icon': self._extract_category_icon(section)
                }
                continue
            
            # Extract commands from this section
            section_commands = await self._extract_commands_from_section(section, current_category, extract_metadata)
            commands.extend(section_commands)
            
            # Add commands to category
            if current_category in categories:
                categories[current_category]['commands'].extend([cmd['name'] for cmd in section_commands])
        
        # Build command index
        command_index = {cmd['name']: cmd for cmd in commands}
        alias_index = {}
        
        for cmd in commands:
            for alias in cmd.get('aliases', []):
                alias_index[alias] = cmd['name']
        
        return {
            'commands': commands,
            'categories': categories,
            'command_index': command_index,
            'alias_index': alias_index,
            'metadata': {
                'total_commands': len(commands),
                'total_categories': len(categories),
                'extraction_method': 'markdown_parsing',
                'content_length': len(content)
            }
        }
    
    def _split_into_sections(self, content: str) -> List[str]:
        """Split content into logical sections."""
        # Split by major headers (## or ###)
        sections = re.split(r'\n(?=##)', content)
        return [section.strip() for section in sections if section.strip()]
    
    def _clean_category_name(self, name: str) -> str:
        """Clean category name by removing emojis and extra whitespace."""
        # Remove emojis and clean up
        cleaned = re.sub(r'[^\w\s-]', '', name).strip()
        return cleaned if cleaned else "General"
    
    def _extract_category_description(self, section: str) -> str:
        """Extract category description from section."""
        lines = section.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#') and not line.startswith('**'):
                return line.strip()
        return ""
    
    def _extract_category_icon(self, section: str) -> str:
        """Extract emoji icon from category header."""
        match = re.search(r'## ([🎯🤖⚙️🎮📊🔧📖🔄📱🌐🔍💡🆘🛡️📈🔗]+)', section)
        return match.group(1) if match else ""
    
    async def _extract_commands_from_section(self, section: str, category: str, extract_metadata: bool) -> List[Dict[str, Any]]:
        """Extract commands from a section."""
        commands = []
        
        # Find all command headers in this section
        command_matches = self.command_patterns['command_header'].findall(section)
        
        for command_name in command_matches:
            try:
                command_data = await self._parse_single_command(section, command_name, category, extract_metadata)
                if command_data:
                    commands.append(command_data)
            except Exception as e:
                logger.warning(f"Failed to parse command {command_name}: {e}")
                continue
        
        return commands
    
    async def _parse_single_command(self, section: str, command_name: str, category: str, extract_metadata: bool) -> Optional[Dict[str, Any]]:
        """Parse a single command from section content."""
        # Find the command block
        command_pattern = rf'### `{re.escape(command_name)}`(.*?)(?=### |$)'
        command_match = re.search(command_pattern, section, re.DOTALL)
        
        if not command_match:
            return None
        
        command_block = command_match.group(1)
        
        # Extract basic information
        description = self._extract_field(command_block, 'description')
        usage = self._extract_field(command_block, 'usage')
        response = self._extract_field(command_block, 'response')
        
        # Extract examples
        examples = self._extract_examples(command_block)
        
        # Extract aliases
        aliases = self._extract_aliases(command_block)
        
        # Extract parameters/options
        parameters = self._extract_parameters(command_block)
        
        # Determine command properties
        requires_github_data = self._requires_github_data(command_name, command_block)
        priority = self._determine_priority(command_name, category)
        
        command_data = {
            'name': command_name.lstrip('/'),
            'full_name': command_name,
            'description': description,
            'usage': usage,
            'examples': examples,
            'category': category,
            'aliases': aliases,
            'parameters': parameters,
            'response_type': self._determine_response_type(response),
            'priority': priority,
            'requires_github_data': requires_github_data
        }
        
        if extract_metadata:
            command_data['metadata'] = {
                'complexity': self._calculate_complexity(command_block),
                'estimated_response_time': self._estimate_response_time(command_name),
                'cache_strategy': self._determine_cache_strategy(command_name),
                'squad_activation': self._requires_squad_activation(command_name)
            }
        
        return command_data
    
    def _extract_field(self, text: str, field: str) -> str:
        """Extract a specific field from command text."""
        pattern_map = {
            'description': self.command_patterns['description'],
            'usage': self.command_patterns['usage'],
            'response': self.command_patterns['response']
        }
        
        pattern = pattern_map.get(field)
        if pattern:
            match = pattern.search(text)
            return match.group(1).strip() if match else ""
        return ""
    
    def _extract_examples(self, text: str) -> List[Dict[str, str]]:
        """Extract examples from command text."""
        examples = []
        
        # Look for examples section
        examples_section = re.search(r'\*\*Examples:\*\*\n((?:- .+\n?)+)', text, re.MULTILINE)
        if examples_section:
            example_lines = examples_section.group(1).strip().split('\n')
            for line in example_lines:
                if line.strip().startswith('- '):
                    # Parse example line
                    example_match = re.match(r'- `([^`]+)` - (.+)', line.strip())
                    if example_match:
                        examples.append({
                            'command': example_match.group(1),
                            'description': example_match.group(2)
                        })
                    else:
                        # Simple example without description
                        simple_match = re.match(r'- `([^`]+)`', line.strip())
                        if simple_match:
                            examples.append({
                                'command': simple_match.group(1),
                                'description': ""
                            })
        
        return examples
    
    def _extract_aliases(self, text: str) -> List[str]:
        """Extract command aliases."""
        aliases = []
        
        # Look for aliases in various formats
        alias_patterns = [
            r'\*\*Aliases:\*\* (.+)',
            r'\*\*Alias:\*\* (.+)',
            r'Aliases: (.+)',
            r'Also: (.+)'
        ]
        
        for pattern in alias_patterns:
            match = re.search(pattern, text)
            if match:
                alias_text = match.group(1)
                # Parse comma-separated aliases
                aliases = [alias.strip().strip('`') for alias in alias_text.split(',')]
                break
        
        return aliases
    
    def _extract_parameters(self, text: str) -> List[Dict[str, Any]]:
        """Extract command parameters and options."""
        parameters = []
        
        # Look for options section
        options_match = self.command_patterns['options'].search(text)
        if options_match:
            options_text = options_match.group(1)
            param_matches = self.command_patterns['parameters'].findall(options_text)
            
            for param_name, param_desc in param_matches:
                parameters.append({
                    'name': param_name,
                    'description': param_desc,
                    'required': 'required' in param_desc.lower(),
                    'type': self._infer_parameter_type(param_desc)
                })
        
        return parameters
    
    def _infer_parameter_type(self, description: str) -> str:
        """Infer parameter type from description."""
        desc_lower = description.lower()
        
        if 'number' in desc_lower or 'count' in desc_lower:
            return 'number'
        elif 'boolean' in desc_lower or 'true/false' in desc_lower:
            return 'boolean'
        elif 'array' in desc_lower or 'list' in desc_lower:
            return 'array'
        elif 'object' in desc_lower or 'json' in desc_lower:
            return 'object'
        else:
            return 'string'
    
    def _requires_github_data(self, command_name: str, command_block: str) -> bool:
        """Determine if command requires GitHub data."""
        github_indicators = [
            'github', 'commands', 'help', 'documentation',
            'fetch', 'update', 'sync', 'latest'
        ]
        
        text_to_check = (command_name + ' ' + command_block).lower()
        return any(indicator in text_to_check for indicator in github_indicators)
    
    def _determine_priority(self, command_name: str, category: str) -> str:
        """Determine command priority."""
        high_priority = ['help', 'status', 'emergency', 'error']
        low_priority = ['analytics', 'debug', 'optimize', 'backup']
        
        command_lower = command_name.lower()
        
        if any(hp in command_lower for hp in high_priority):
            return 'high'
        elif any(lp in command_lower for lp in low_priority):
            return 'low'
        else:
            return 'normal'
    
    def _determine_response_type(self, response_text: str) -> str:
        """Determine expected response type."""
        if not response_text:
            return 'text'
        
        response_lower = response_text.lower()
        
        if 'json' in response_lower or 'object' in response_lower:
            return 'json'
        elif 'list' in response_lower or 'array' in response_lower:
            return 'list'
        elif 'table' in response_lower or 'grid' in response_lower:
            return 'table'
        elif 'markdown' in response_lower:
            return 'markdown'
        else:
            return 'text'
    
    def _calculate_complexity(self, command_block: str) -> str:
        """Calculate command complexity based on content."""
        complexity_score = 0
        
        # Count parameters
        param_count = len(self.command_patterns['parameters'].findall(command_block))
        complexity_score += param_count * 2
        
        # Count examples
        example_count = len(self.command_patterns['examples'].findall(command_block))
        complexity_score += example_count
        
        # Check for advanced features
        advanced_keywords = ['configuration', 'advanced', 'complex', 'integration']
        for keyword in advanced_keywords:
            if keyword in command_block.lower():
                complexity_score += 3
        
        if complexity_score <= 3:
            return 'simple'
        elif complexity_score <= 8:
            return 'moderate'
        else:
            return 'complex'
    
    def _estimate_response_time(self, command_name: str) -> int:
        """Estimate response time in milliseconds."""
        fast_commands = ['status', 'help', 'config']
        slow_commands = ['analytics', 'optimize', 'backup', 'search']
        
        command_lower = command_name.lower()
        
        if any(fc in command_lower for fc in fast_commands):
            return 500  # 500ms
        elif any(sc in command_lower for sc in slow_commands):
            return 5000  # 5s
        else:
            return 2000  # 2s
    
    def _determine_cache_strategy(self, command_name: str) -> str:
        """Determine optimal cache strategy."""
        no_cache = ['status', 'real-time', 'live']
        aggressive_cache = ['help', 'documentation', 'reference']
        
        command_lower = command_name.lower()
        
        if any(nc in command_lower for nc in no_cache):
            return 'none'
        elif any(ac in command_lower for ac in aggressive_cache):
            return 'aggressive'
        else:
            return 'moderate'
    
    def _requires_squad_activation(self, command_name: str) -> bool:
        """Determine if command requires squad activation."""
        squad_commands = [
            'analytics', 'optimize', 'complex', 'advanced',
            'integration', 'workflow', 'automation'
        ]
        
        command_lower = command_name.lower()
        return any(sc in command_lower for sc in squad_commands)
    
    async def _extract_from_json(self, content: str, extract_metadata: bool) -> Dict[str, Any]:
        """Extract commands from JSON content."""
        try:
            data = json.loads(content)
            
            # Assume JSON structure with commands array
            commands = data.get('commands', [])
            categories = data.get('categories', {})
            
            # Build indices
            command_index = {cmd['name']: cmd for cmd in commands}
            alias_index = {}
            
            for cmd in commands:
                for alias in cmd.get('aliases', []):
                    alias_index[alias] = cmd['name']
            
            return {
                'commands': commands,
                'categories': categories,
                'command_index': command_index,
                'alias_index': alias_index,
                'metadata': {
                    'total_commands': len(commands),
                    'total_categories': len(categories),
                    'extraction_method': 'json_parsing',
                    'content_length': len(content)
                }
            }
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON content: {e}")
    
    async def validate_command(self, command: str, commands_data: Optional[Dict] = None, strict: bool = True) -> Dict[str, Any]:
        """Validate a command against available commands."""
        logger.info(f"✅ Validating command: {command}")
        
        if not commands_data:
            return {
                'valid': True,
                'message': 'No commands data available for validation'
            }
        
        command_clean = command.strip().lstrip('/')
        
        # Check direct command match
        if command_clean in commands_data.get('command_index', {}):
            return {
                'valid': True,
                'command': command_clean,
                'type': 'direct_match'
            }
        
        # Check alias match
        if command_clean in commands_data.get('alias_index', {}):
            actual_command = commands_data['alias_index'][command_clean]
            return {
                'valid': True,
                'command': actual_command,
                'type': 'alias_match',
                'alias': command_clean
            }
        
        # If strict mode, command is invalid
        if strict:
            suggestions = await self.generate_suggestions(command, {'commands_data': commands_data})
            return {
                'valid': False,
                'command': command_clean,
                'message': f'Unknown command: {command_clean}',
                'suggestions': suggestions.get('data', [])
            }
        
        # Non-strict mode, allow unknown commands
        return {
            'valid': True,
            'command': command_clean,
            'type': 'unknown',
            'message': 'Command not found but allowed in non-strict mode'
        }
    
    async def generate_suggestions(self, query: str, context: Dict[str, Any] = {}, max_suggestions: int = 10) -> Dict[str, Any]:
        """Generate command suggestions based on query."""
        logger.info(f"💡 Generating suggestions for: {query}")
        
        commands_data = context.get('commands_data', {})
        if not commands_data:
            return {'data': []}
        
        query_clean = query.strip().lstrip('/').lower()
        suggestions = []
        
        # Get all available commands
        all_commands = commands_data.get('commands', [])
        
        # Calculate similarity scores
        for cmd in all_commands:
            score = self._calculate_similarity(query_clean, cmd['name'])
            
            if score > 0.3:  # Minimum similarity threshold
                suggestions.append({
                    'command': cmd['name'],
                    'description': cmd.get('description', ''),
                    'category': cmd.get('category', ''),
                    'score': score,
                    'type': 'similarity_match'
                })
        
        # Sort by score and limit
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        suggestions = suggestions[:max_suggestions]
        
        return {
            'data': suggestions,
            'query': query,
            'total_suggestions': len(suggestions)
        }
    
    def _calculate_similarity(self, query: str, command: str) -> float:
        """Calculate similarity between query and command."""
        # Simple similarity based on common characters and substrings
        query_lower = query.lower()
        command_lower = command.lower()
        
        # Exact match
        if query_lower == command_lower:
            return 1.0
        
        # Substring match
        if query_lower in command_lower or command_lower in query_lower:
            return 0.8
        
        # Character overlap
        query_chars = set(query_lower)
        command_chars = set(command_lower)
        
        if not query_chars or not command_chars:
            return 0.0
        
        overlap = len(query_chars.intersection(command_chars))
        total = len(query_chars.union(command_chars))
        
        return overlap / total if total > 0 else 0.0
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("🧹 Cleaning up Command Extractor...")
        self.commands.clear()
        self.categories.clear()
        logger.info("✅ Command Extractor cleanup complete")