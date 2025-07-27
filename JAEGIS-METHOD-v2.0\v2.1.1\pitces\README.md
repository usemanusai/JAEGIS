# P.I.T.C.E.S. Framework

**Parallel Integrated Task Contexting Engine System**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JAEGIS Integration](https://img.shields.io/badge/JAEGIS-v2.2-green.svg)](https://github.com/usemanusai/JAEGIS)

A sophisticated project management framework that intelligently adapts its workflow based on quantifiable project characteristics, seamlessly integrating with the JAEGIS Enhanced Agent System v2.2.

## 🚀 Overview

P.I.T.C.E.S. is a hybrid operational framework that automatically selects between **Sequential Waterfall** and **Continuous Integration & Adaptive Refinement (CI/AR)** workflows based on project complexity metrics. It features advanced task management, intelligent triage systems, and comprehensive gap analysis capabilities.

### Key Features

- **🧠 Intelligent Workflow Selection**: Automatic mode selection based on project characteristics
- **⚡ Dual Workflow Modes**: Sequential Waterfall for simple projects, CI/AR for complex ones
- **🎯 Advanced Triage System**: Priority-based task queuing with SLA management
- **🔄 Task Preemption**: Safe context switching with state persistence
- **🔍 Gap Analysis Squad**: Automated auditing across 7 analysis domains
- **📊 Performance Monitoring**: Real-time metrics and resource utilization tracking
- **🔗 JAEGIS Integration**: Seamless integration with N.L.D.S. Tier 0 component

## 📋 Requirements

- **Python**: 3.11 or higher
- **Memory**: Maximum 512MB for typical projects (100 tasks)
- **Startup Time**: <3 seconds for framework initialization
- **Platform**: Cross-platform (Windows, macOS, Linux)

## 🛠️ Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/usemanusai/JAEGIS.git
cd JAEGIS/pitces

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run demonstration
python main.py
```

### Development Installation

```bash
# Install with development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/ --cov=pitces --cov-report=html

# Format code
black pitces/
isort pitces/

# Type checking
mypy pitces/
```

## 🎯 Workflow Selection Logic

P.I.T.C.E.S. analyzes four key project characteristics to determine the optimal workflow:

| Characteristic | Sequential Threshold | CI/AR Threshold |
|----------------|---------------------|-----------------|
| **Task Count** | < 50 tasks | ≥ 50 tasks |
| **Requirements Clarity** | > 95% clear | ≤ 95% clear |
| **Architectural Complexity** | ≤ 5 (scale 1-10) | > 5 (scale 1-10) |
| **Risk Level** | LOW | MEDIUM/HIGH |

### Decision Algorithm

```python
def select_workflow(project_specs):
    sequential_votes = 0
    ci_ar_votes = 0
    
    # Analyze each characteristic
    if project_specs.task_count < 50:
        sequential_votes += 1
    else:
        ci_ar_votes += 1
    
    # ... (similar logic for other characteristics)
    
    return 'SEQUENTIAL' if sequential_votes > ci_ar_votes else 'CI_AR'
```

## 🔄 Workflow Modes

### Sequential Waterfall Mode

**Best for**: Simple, well-defined projects with clear requirements

- **Phases**: Requirements → Design → Implementation → Testing → Deployment
- **Execution**: Strict linear progression with phase gates
- **Validation**: 100% completion required before proceeding
- **Overhead**: <10% computational overhead

### CI/AR Mode (Continuous Integration & Adaptive Refinement)

**Best for**: Complex, dynamic projects with evolving requirements

- **Triage Protocol**: 4-level priority system (CRITICAL, HIGH, MEDIUM, LOW)
- **Task Preemption**: Safe context switching with state persistence
- **SLA Management**: Automatic escalation for overdue tasks
- **Dependency Management**: DAG validation to prevent circular dependencies

## 🎯 Triage System

### Priority Levels & SLA Targets

| Priority | SLA Target | Use Cases |
|----------|------------|-----------|
| **CRITICAL** | 5 minutes | System-breaking bugs, security vulnerabilities |
| **HIGH** | 1 hour | Core functional failures |
| **MEDIUM** | 24 hours | Minor functional errors |
| **LOW** | 1 week | Cosmetic issues, documentation updates |

### Automatic Classification

The triage system automatically classifies tasks based on:

- **Security Keywords**: 'security', 'vulnerability', 'breach', etc.
- **System Critical Keywords**: 'system down', 'outage', 'crash', etc.
- **Deadline Urgency**: Time remaining until SLA deadline
- **Dependency Impact**: Number of dependent tasks
- **Business Impact**: Revenue, customer, production-related keywords

## 🔍 Gap Analysis Squad

Automated comprehensive auditing across seven analysis domains:

### Analysis Domains

1. **Functional Completeness** (20% weight)
   - Feature coverage analysis against requirements
   - Target: ≥80% completion

2. **Security & Integrity** (25% weight)
   - Vulnerability scanning and access control validation
   - Target: ≥90% security score

3. **Performance & Scalability** (15% weight)
   - Load testing and resource utilization analysis
   - Target: ≥85% performance score

4. **Integration & Interoperability** (15% weight)
   - API compatibility and data flow validation
   - Target: ≥85% compatibility score

5. **Compliance & Governance** (10% weight)
   - Regulatory requirement adherence checking
   - Target: ≥95% compliance

6. **Logical & Strategic Alignment** (10% weight)
   - Business objective mapping and ROI analysis
   - Target: ≥80% alignment score

7. **Documentation & Maintainability** (5% weight)
   - Code quality metrics and documentation coverage
   - Target: ≥75% quality score

## 📊 Usage Examples

### Basic Usage

```python
from pitces.core.controller import PITCESController

# Initialize controller
controller = PITCESController()

# Define project specifications
project_specs = {
    'task_count': 30,
    'requirements_clarity': 98.0,
    'complexity_score': 3,
    'risk_level': 'LOW'
}

# Select workflow
workflow_mode = controller.select_workflow(project_specs)
print(f"Selected workflow: {workflow_mode}")  # Output: SEQUENTIAL

# Execute workflow
tasks = [
    {'name': 'Design homepage', 'priority': 'HIGH', 'estimated_hours': 4},
    {'name': 'Implement navigation', 'priority': 'MEDIUM', 'estimated_hours': 3}
]

results = controller.execute_workflow(tasks)
print(f"Success rate: {results['success_rate']:.1f}%")
```

### Advanced Usage with Gap Analysis

```python
from pitces.core.gap_analysis_squad import GapAnalysisSquad
from pitces.core.models import ProjectSpecs, RiskLevel

# Initialize gap analysis
gap_squad = GapAnalysisSquad()

# Create project specifications
project_specs = ProjectSpecs(
    task_count=75,
    requirements_clarity=80.0,
    complexity_score=8,
    risk_level=RiskLevel.HIGH
)

# Run comprehensive audit
analysis_results = gap_squad.run_audit(project_specs, tasks)

# Generate report
report = gap_squad.generate_report(analysis_results)
print(f"Overall score: {report['overall_metrics']['overall_score']:.1f}%")
```

### Task Preemption Example

```python
from pitces.core.preemption_manager import PreemptionManager
from pitces.core.context_engine import ContextEngine

# Initialize preemption manager
context_engine = ContextEngine()
preemption_manager = PreemptionManager(context_engine)

# Pause a task
task_id = some_task.id
context_data = {'current_step': 'processing', 'progress': 0.6}

success = preemption_manager.pause_task(task_id, context_data)
if success:
    print("Task paused successfully")

# Resume the task later
restored_context = preemption_manager.resume_task(task_id)
if restored_context:
    print(f"Task resumed from step: {restored_context['current_step']}")
```

## 🔧 Configuration

### Environment Variables

```bash
# Optional GitHub integration
export GITHUB_TOKEN="your_github_token_here"

# Performance tuning
export PITCES_MAX_MEMORY_MB=512
export PITCES_STARTUP_TIMEOUT=3
export PITCES_STORAGE_PATH="./pitces_context"
```

### Configuration File (config.yaml)

```yaml
pitces:
  workflow_selection:
    task_count_threshold: 50
    clarity_threshold: 95.0
    complexity_threshold: 5
    sequential_risk_levels: ["LOW"]
  
  performance:
    max_memory_mb: 512
    startup_timeout_seconds: 3
    monitoring_enabled: true
  
  triage:
    max_queue_size: 1000
    sla_targets:
      CRITICAL: 300  # 5 minutes
      HIGH: 3600     # 1 hour
      MEDIUM: 86400  # 24 hours
      LOW: 604800    # 1 week
  
  gap_analysis:
    enable_detailed_analysis: true
    compliance_frameworks: ["SOC2", "GDPR"]
    performance_targets:
      response_time_ms: 500
      throughput_rps: 1000
      availability_percent: 99.9
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pitces --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/performance/   # Performance tests
```

### Test Coverage Requirements

- **Minimum Coverage**: 90%
- **Critical Paths**: 100% coverage required
- **Performance Tests**: Load testing up to 1000 tasks
- **Integration Tests**: End-to-end workflow validation

## 📈 Performance Benchmarks

### Framework Overhead

| Project Size | Sequential Mode | CI/AR Mode | Memory Usage |
|--------------|----------------|------------|--------------|
| 10 tasks | 2.1% overhead | 4.3% overhead | 45 MB |
| 50 tasks | 5.2% overhead | 7.8% overhead | 128 MB |
| 100 tasks | 8.1% overhead | 9.4% overhead | 256 MB |
| 500 tasks | 9.2% overhead | 9.8% overhead | 485 MB |

### Scalability Metrics

- **Maximum Tasks**: 1000+ tasks per workflow
- **Concurrent Workflows**: 10+ simultaneous workflows
- **Memory Efficiency**: <512MB for typical projects
- **Startup Time**: <3 seconds average

## 🔗 JAEGIS Integration

P.I.T.C.E.S. seamlessly integrates with the JAEGIS Enhanced Agent System v2.2:

### N.L.D.S. Tier 0 Component

- **Natural Language Processing**: Enhanced command interpretation
- **A.M.A.S.I.A.P. Protocol**: Automatic input enhancement
- **Multi-dimensional Analysis**: Logical, emotional, creative processing
- **Confidence Thresholds**: ≥85% accuracy validation

### GitHub Synchronization

- **Dynamic Resource Fetching**: Real-time configuration updates
- **Repository Integration**: `usemanusai/JAEGIS` repository sync
- **Command Templates**: GitHub-hosted command library
- **Configuration Management**: Centralized settings distribution

### 128-Agent Coordination

- **Tier 1**: JAEGIS Orchestrator (1 agent)
- **Tier 2**: Strategic agents - John, Fred, Tyler (3 agents)
- **Tier 3**: Specialized agents (16 agents)
- **Tier 4**: Conditional agents (4 agents)
- **Tier 5**: IUAS maintenance squad (20 agents)
- **Tier 6**: GARAS analysis squad (40 agents)

## 🚨 Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'pitces'`
```bash
# Solution: Install in development mode
pip install -e .
```

**Issue**: Memory usage exceeds 512MB
```bash
# Solution: Reduce task batch size or enable memory optimization
export PITCES_MEMORY_OPTIMIZATION=true
```

**Issue**: Workflow selection seems incorrect
```bash
# Solution: Check project specifications and thresholds
python -c "from pitces.core.workflow_selector import WorkflowSelector; ws = WorkflowSelector(); print(ws.get_current_thresholds())"
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
controller = PITCESController({'debug_mode': True})
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Maintain >90% test coverage
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **JAEGIS Enhanced Agent System v2.2** for foundational architecture
- **N.L.D.S. Tier 0 Component** for natural language processing
- **OpenRouter.ai** for AI model integration
- **GitHub** for dynamic resource management

---

**P.I.T.C.E.S. Framework v1.0.0**  
*Revolutionizing project management through intelligent workflow adaptation*

For more information, visit the [JAEGIS repository](https://github.com/usemanusai/JAEGIS) or contact the development team.
