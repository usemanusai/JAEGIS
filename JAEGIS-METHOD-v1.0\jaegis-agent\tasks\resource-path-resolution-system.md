# Enhanced Resource Path Resolution System with Intelligence

## Purpose

- Comprehensive resource path resolution system with real-time validation and research integration
- Conduct path resolution with validated methodologies and collaborative intelligence
- Ensure resolution excellence with current file system standards and path practices
- Integrate web research for current path frameworks and resolution patterns
- Provide validated path strategies with cross-team coordination and continuous optimization

## Enhanced Capabilities

### Path Intelligence
- **Path Validation**: Real-time resource path validation against current file system standards
- **Research Integration**: Current path resolution best practices and file system frameworks
- **Resolution Assessment**: Comprehensive path resolution analysis and optimization
- **System Validation**: File system path analysis and resolution validation with continuous improvement

### Collaborative Intelligence
- **Shared Context Integration**: Access to all path contexts and resolution requirements
- **Cross-Team Coordination**: Seamless collaboration with system teams and path stakeholders
- **Quality Assurance**: Professional-grade path resolution with validation reports
- **Research Integration**: Current file systems, path methodologies, and resolution best practices

[[LLM: VALIDATION CHECKPOINT - All resource path resolution must be validated for accuracy, reliability, and current file system standards. Include research-backed path methodologies and resolution principles.]]

## Complete Resource Path Resolution Algorithm

### 1. JAEGIS Directory Structure Specification

```
JAEGIS/
├── JAEGIS-METHOD/
│   └── JAEGIS-agent/
│       ├── personas/
│       │   ├── personas.txt (sectioned file)
│       │   └── *.md (individual persona files)
│       ├── tasks/
│       │   ├── tasks.txt (sectioned file)
│       │   └── *.md (individual task files)
│       ├── checklists/
│       │   ├── checklists.txt (sectioned file)
│       │   └── *.md (individual checklist files)
│       ├── templates/
│       │   ├── templates.txt (sectioned file)
│       │   └── *.md (individual template files)
│       ├── data/
│       │   ├── data.txt (sectioned file)
│       │   └── *.md (individual data files)
│       └── agent-config.txt (main configuration file)
```

### 2. Path Resolution Variables

#### Core Variables
- `(project-root)`: Absolute path to the JAEGIS project root directory
- `(agent-root)`: Absolute path to JAEGIS-agent directory: `(project-root)/JAEGIS-METHOD/JAEGIS-agent/`
- `(personas-dir)`: `(agent-root)/personas/`
- `(tasks-dir)`: `(agent-root)/tasks/`
- `(checklists-dir)`: `(agent-root)/checklists/`
- `(templates-dir)`: `(agent-root)/templates/`
- `(data-dir)`: `(agent-root)/data/`

#### Variable Resolution Process
1. **Project Root Detection**:
   - Search for `JAEGIS-METHOD` directory in current working directory
   - If not found, search parent directories up to 5 levels
   - If still not found, prompt user for project root path
   - Validate by checking for `JAEGIS-agent/agent-config.txt`

2. **Agent Root Validation**:
   - Construct: `(project-root)/JAEGIS-METHOD/JAEGIS-agent/`
   - Verify directory exists and is accessible
   - Check for required subdirectories: personas, tasks, checklists, templates, data
   - Validate agent-config.txt exists and is readable

### 3. File Reference Resolution Algorithm

#### Reference Format Types
1. **Sectioned File Reference**: `FILE_PREFIX#SECTION_NAME`
   - Example: `personas#pm`, `tasks#documentation-mode-workflow`
2. **Direct File Reference**: `FILENAME.md`
   - Example: `analyst.md`, `frontend-checklist.md`
3. **Absolute Path Reference**: `/full/path/to/file.md`
4. **Relative Path Reference**: `./relative/path/file.md`

#### Resolution Process
```python
def resolve_resource_path(reference, context_type):
    """
    Resolve resource path with comprehensive validation
    
    Args:
        reference: String reference (e.g., "personas#pm", "analyst.md")
        context_type: Type of resource ("personas", "tasks", "checklists", "templates", "data")
    
    Returns:
        ResolvedPath object with content and metadata
    """
    
    # Step 1: Parse reference format
    if '#' in reference:
        file_prefix, section_name = reference.split('#', 1)
        resolution_type = "sectioned"
    elif reference.endswith('.md'):
        file_prefix = reference
        section_name = None
        resolution_type = "direct"
    elif reference.startswith('/'):
        resolution_type = "absolute"
    elif reference.startswith('./'):
        resolution_type = "relative"
    else:
        resolution_type = "unknown"
    
    # Step 2: Construct base path
    base_dir = get_context_directory(context_type)
    
    # Step 3: Resolve file path
    if resolution_type == "sectioned":
        file_path = f"{base_dir}/{file_prefix}.txt"
        fallback_path = f"{base_dir}/{file_prefix}.md"
    elif resolution_type == "direct":
        file_path = f"{base_dir}/{reference}"
        fallback_path = None
    elif resolution_type == "absolute":
        file_path = reference
        fallback_path = None
    elif resolution_type == "relative":
        file_path = resolve_relative_path(reference, base_dir)
        fallback_path = None
    else:
        raise PathResolutionError(f"Unknown reference format: {reference}")
    
    # Step 4: Validate and load content
    return load_with_fallback(file_path, fallback_path, section_name)
```

### 4. Fallback Mechanisms

#### Primary Fallback Sequence
1. **Sectioned File Fallback**:
   - Primary: `{context_dir}/{file_prefix}.txt` with section extraction
   - Fallback 1: `{context_dir}/{file_prefix}.md` (treat as direct file)
   - Fallback 2: `{context_dir}/{section_name}.md` (direct section file)
   - Fallback 3: Search all `.md` files for matching content

2. **Direct File Fallback**:
   - Primary: `{context_dir}/{filename}.md`
   - Fallback 1: `{context_dir}/{filename}.txt`
   - Fallback 2: Case-insensitive search in context directory
   - Fallback 3: Fuzzy matching with similar filenames

3. **Missing Directory Fallback**:
   - Create missing directories with default structure
   - Generate placeholder files with standard templates
   - Log missing resource warnings
   - Continue with degraded functionality

#### Error Handling Behaviors
```python
class PathResolutionError(Exception):
    """Custom exception for path resolution failures"""
    pass

def load_with_fallback(primary_path, fallback_path, section_name):
    """Load content with comprehensive fallback handling"""

    try:
        # Attempt primary path
        if os.path.exists(primary_path):
            content = load_file_content(primary_path, section_name)
            return ResolvedPath(content, primary_path, "primary")
    except Exception as e:
        log_warning(f"Primary path failed: {primary_path}, error: {e}")

    try:
        # Attempt fallback path
        if fallback_path and os.path.exists(fallback_path):
            content = load_file_content(fallback_path, section_name)
            return ResolvedPath(content, fallback_path, "fallback")
    except Exception as e:
        log_warning(f"Fallback path failed: {fallback_path}, error: {e}")

    # Generate default content
    default_content = generate_default_content(primary_path, section_name)
    log_error(f"All paths failed, using default content for: {primary_path}")
    return ResolvedPath(default_content, None, "default")
```

### 5. Path Validation Procedures

#### Pre-Resolution Validation
1. **Directory Structure Validation**:
   ```python
   def validate_JAEGIS_structure():
       required_dirs = [
           "(agent-root)/personas",
           "(agent-root)/tasks",
           "(agent-root)/checklists",
           "(agent-root)/templates",
           "(agent-root)/data"
       ]

       for dir_path in required_dirs:
           if not os.path.exists(resolve_path(dir_path)):
               create_directory_with_defaults(dir_path)
               log_warning(f"Created missing directory: {dir_path}")
   ```

2. **File Accessibility Validation**:
   ```python
   def validate_file_access(file_path):
       if not os.path.exists(file_path):
           return ValidationResult(False, "FILE_NOT_FOUND")
       if not os.access(file_path, os.R_OK):
           return ValidationResult(False, "FILE_NOT_READABLE")
       if os.path.getsize(file_path) == 0:
           return ValidationResult(False, "FILE_EMPTY")
       return ValidationResult(True, "FILE_VALID")
   ```

#### Post-Resolution Validation
1. **Content Validation**:
   - Verify file encoding (UTF-8 expected)
   - Check for required section markers in sectioned files
   - Validate markdown syntax for .md files
   - Ensure minimum content length requirements

2. **Dependency Validation**:
   - Check all referenced files exist
   - Validate circular reference detection
   - Ensure required sections are present
   - Verify template variable completeness

### 6. Section Extraction Algorithm

#### Sectioned File Format
```
==================== START: SECTION_NAME ====================
Section content here...
Multiple lines supported...
==================== END: SECTION_NAME ====================
```

#### Extraction Process
```python
def extract_section(file_content, section_name):
    """Extract specific section from sectioned file"""

    start_marker = f"==================== START: {section_name} ===================="
    end_marker = f"==================== END: {section_name} ===================="

    lines = file_content.split('\n')
    section_lines = []
    in_section = False

    for line in lines:
        if line.strip() == start_marker:
            in_section = True
            continue
        elif line.strip() == end_marker:
            break
        elif in_section:
            section_lines.append(line)

    if not section_lines:
        raise SectionNotFoundError(f"Section '{section_name}' not found")

    return '\n'.join(section_lines).strip()
```
### 7. Relative vs Absolute Path Handling

#### Absolute Path Processing
- **Format**: Paths starting with `/` (Unix) or `C:\` (Windows)
- **Validation**: Verify path exists and is accessible
- **Security**: Restrict access to paths outside project boundaries
- **Cross-Platform**: Handle Windows/Unix path differences

#### Relative Path Processing
- **Format**: Paths starting with `./` or `../`
- **Base Resolution**: Resolve relative to current context directory
- **Normalization**: Convert to absolute paths for internal processing
- **Validation**: Ensure resolved path stays within project boundaries

### 8. Performance Optimization

#### Caching Strategy
```python
class PathCache:
    """Intelligent caching for resolved paths"""

    def __init__(self):
        self.cache = {}
        self.cache_stats = {"hits": 0, "misses": 0}

    def get_cached_path(self, reference, context_type):
        cache_key = f"{context_type}:{reference}"
        if cache_key in self.cache:
            self.cache_stats["hits"] += 1
            return self.cache[cache_key]

        self.cache_stats["misses"] += 1
        return None

    def cache_path(self, reference, context_type, resolved_path):
        cache_key = f"{context_type}:{reference}"
        self.cache[cache_key] = resolved_path
```

#### File System Monitoring
- Monitor file system changes for cache invalidation
- Automatic cache refresh when files are modified
- Lazy loading for improved startup performance
- Memory management for large file collections

### 9. Error Recovery Procedures

#### Graceful Degradation Levels
1. **Level 1 - Full Functionality**: All resources available
2. **Level 2 - Reduced Functionality**: Some resources missing, fallbacks used
3. **Level 3 - Basic Functionality**: Core resources only, minimal features
4. **Level 4 - Emergency Mode**: Default content only, system warnings

#### Recovery Actions
```python
def handle_resource_failure(resource_type, reference, error):
    """Comprehensive error recovery handling"""

    recovery_actions = {
        "FILE_NOT_FOUND": create_default_file,
        "FILE_NOT_READABLE": fix_permissions,
        "SECTION_NOT_FOUND": create_default_section,
        "INVALID_FORMAT": repair_file_format,
        "CIRCULAR_REFERENCE": break_circular_dependency
    }

    action = recovery_actions.get(error.type, log_and_continue)
    return action(resource_type, reference, error)
```

### 10. Diagnostic and Troubleshooting

#### System Health Check
```python
def run_system_health_check():
    """Comprehensive system validation"""

    health_report = {
        "directory_structure": validate_directory_structure(),
        "file_accessibility": validate_file_accessibility(),
        "content_integrity": validate_content_integrity(),
        "dependency_resolution": validate_dependencies(),
        "performance_metrics": collect_performance_metrics()
    }

    return HealthReport(health_report)
```

#### Common Issues and Solutions
1. **Issue**: "File not found" errors
   - **Diagnosis**: Check file paths and permissions
   - **Solution**: Verify directory structure, create missing files

2. **Issue**: "Section not found" in sectioned files
   - **Diagnosis**: Check section marker format
   - **Solution**: Verify section names match exactly

3. **Issue**: Slow path resolution
   - **Diagnosis**: Check cache performance and file system speed
   - **Solution**: Optimize caching strategy, consider SSD storage

4. **Issue**: Permission denied errors
   - **Diagnosis**: Check file and directory permissions
   - **Solution**: Adjust permissions or run with appropriate privileges
