# JAEGIS Method Agent Commands Reference
## Comprehensive Command Documentation

**Last Updated:** 19 AUGUST, 2025  
**Version:** 2.3.0  
**Agent System:** JAEGIS Method v2.3  
**Total Agents:** 128+ across 6 Tiers  
**Architecture:** Multi-squad coordination system  
**Memory System:** Advanced cognitive memory with HNSW vector search

---

## 🎯 Core Commands

### `/help`
**Description:** Display comprehensive help system and command reference  
**Usage:** `/help [command]`  
**Examples:**
- `/help` - Show all available commands
- `/help config` - Get detailed help for config command
- `/help agent-workflow` - Get help for agent workflow configuration
- `/help squad` - Get help for squad management commands

**Response:** Complete command list with descriptions and usage examples

---

### `/config`
**Description:** Access system configuration and parameter control  
**Usage:** `/config [option]`  
**Options:**
- `/config` - Open main configuration menu
- `/config presets` - Access quick configuration presets
- `/config advanced` - Access advanced configuration options
- `/config export` - Export current configuration
- `/config import` - Import configuration from file
- `/config reset` - Reset all parameters to defaults
- `/config squad` - Configure squad-specific settings
- `/config tier` - Configure tier-specific settings

**Configuration Parameters:**
- **Deep Web Research Frequency** (0-100%) - Research thoroughness
- **Task Decomposition Depth** (0-100%) - Task breakdown detail
- **Agent Activation Frequency** (0-100%) - Agent utilization level
- **Quality Validation Intensity** (0-100%) - QA process thoroughness
- **Real-Time Monitoring Freq.** (0-100%) - System health monitoring
- **Cross-Validation Frequency** (0-100%) - Agent cross-referencing
- **Squad Coordination Intensity** (0-100%) - Inter-squad coordination
- **Tier Integration Level** (0-100%) - Cross-tier integration

**Presets:**
- **Performance Mode** - Optimized for speed and responsiveness
- **Quality Mode** - Optimized for maximum accuracy and thoroughness
- **Efficiency Mode** - Optimized for resource conservation
- **Balanced Mode** - Optimal balance across all metrics (Recommended)
- **Maintenance Mode** - Optimized for system maintenance and updates

---

### `/status`
**Description:** Show current system status and configuration  
**Usage:** `/status [detail]`  
**Options:**
- `/status` - Basic system status overview
- `/status detailed` - Detailed system status with all metrics
- `/status squads` - Squad-specific status information
- `/status tiers` - Tier-specific status information
- `/status agents` - Individual agent status

**Response:** System health, active agents, performance metrics, current settings, squad coordination status

---

## 🎮 Mode & Navigation Commands

### `/mode-switch`
**Description:** Switch between Documentation and Full Development modes  
**Usage:** `/mode-switch [mode]`  
**Options:**
- `/mode-switch documentation` - Switch to Documentation Mode
- `/mode-switch development` - Switch to Full Development Mode
- `/mode-switch maintenance` - Switch to Maintenance Mode
- `/mode-switch` - Interactive mode selection

---

### `/reset`
**Description:** Reset system to default configuration  
**Usage:** `/reset [scope]`  
**Options:**
- `/reset` - Reset all settings to defaults
- `/reset config` - Reset only configuration parameters
- `/reset agents` - Reset agent configurations
- `/reset squads` - Reset squad configurations
- `/reset cache` - Clear system cache
- `/reset tiers` - Reset tier configurations

---

## 🤖 Agent Management Commands

### `/agents`
**Description:** List all available agents and their capabilities  
**Usage:** `/agents [filter]`  
**Options:**
- `/agents` - List all agents (128+ total)
- `/agents active` - Show only active agents
- `/agents available` - Show available agents
- `/agents specialized` - Show specialized agents by category
- `/agents squad [squad-name]` - Show agents in specific squad
- `/agents tier [tier-number]` - Show agents in specific tier

**Agent Categories:**
- **Analysis Agents** - Data analysis, research, and investigation
- **Development Agents** - Code generation, testing, and optimization
- **Design Agents** - UI/UX design, architecture, and planning
- **Management Agents** - Project management, coordination, and monitoring
- **Quality Agents** - Testing, validation, and quality assurance
- **Documentation Agents** - Technical writing and documentation
- **Maintenance Agents** - System maintenance and updates
- **Monitoring Agents** - System health and performance monitoring

**Agent Tiers:**
- **Tier 1:** Core Foundation Agents
- **Tier 2:** Specialized Function Agents
- **Tier 3:** Advanced Integration Agents
- **Tier 4:** Conditional Activation Agents
- **Tier 5:** Expert System Agents
- **Tier 6:** Maintenance & Enhancement Agents

---

### `/activate`
**Description:** Manually activate specific agent or agent squad  
**Usage:** `/activate [agent/squad]`  
**Examples:**
- `/activate research-agent` - Activate research specialist
- `/activate development-squad` - Activate development team
- `/activate iuas` - Activate Internal Updates Agent Squad
- `/activate garas` - Activate Gaps Analysis and Resolution Agent Squad
- `/activate all` - Activate all available agents

---

### `/squad-status`
**Description:** Show current squad activation and coordination status  
**Usage:** `/squad-status [squad-name]`  
**Options:**
- `/squad-status` - Show all squad statuses
- `/squad-status iuas` - Show Internal Updates Agent Squad status
- `/squad-status garas` - Show Gaps Analysis and Resolution Agent Squad status
- `/squad-status active` - Show only active squads

**Response:** Active squads, coordination status, performance metrics, agent allocation

---

### `/squad-manage`
**Description:** Manage specific agent squads and their configurations  
**Usage:** `/squad-manage [squad-name] [action]`  
**Examples:**
- `/squad-manage iuas activate` - Activate IUAS squad
- `/squad-manage garas config` - Configure GARAS squad
- `/squad-manage iuas status` - Check IUAS squad status
- `/squad-manage all deactivate` - Deactivate all squads

---

## ⚙️ Workflow Configuration Commands

### `/agent-workflow`
**Description:** Configure agent selection and routing preferences  
**Usage:** `/agent-workflow [action]`  
**Options:**
- `/agent-workflow` - Open workflow configuration menu
- `/agent-workflow rules` - Set up custom routing rules
- `/agent-workflow priorities` - Configure agent priority settings
- `/agent-workflow automation` - Set up automated agent selection
- `/agent-workflow squad` - Configure squad-based workflows
- `/agent-workflow tier` - Configure tier-based workflows

---

### `/tool-workflow`
**Description:** Optimize tool usage patterns and preferences  
**Usage:** `/tool-workflow [category]`  
**Categories:**
- `/tool-workflow development` - Configure development tools
- `/tool-workflow analysis` - Configure analysis tools
- `/tool-workflow communication` - Configure communication tools
- `/tool-workflow monitoring` - Configure monitoring tools
- `/tool-workflow maintenance` - Configure maintenance tools

---

### `/protocols`
**Description:** Manage system protocols and behavioral rules  
**Usage:** `/protocols [action]`  
**Actions:**
- `/protocols` - View current protocols
- `/protocols add` - Add new protocol rule
- `/protocols edit` - Edit existing protocol
- `/protocols remove` - Remove protocol rule
- `/protocols export` - Export protocol configuration
- `/protocols squad` - Configure squad-specific protocols
- `/protocols coordination` - Configure coordination protocols

**Protocol Types:**
- **Cross-Unit Communication** - Inter-squad communication protocols
- **Unit Activation Triggers** - Squad activation mechanisms
- **Inter-Unit Dependencies** - Squad dependency management
- **Quality Validation** - Validation protocols
- **Performance Monitoring** - Performance tracking protocols

---

## 📊 System Monitoring Commands

### `/system-health`
**Description:** Display comprehensive system health dashboard  
**Usage:** `/system-health [detail]`  
**Options:**
- `/system-health` - Basic health overview
- `/system-health detailed` - Detailed health metrics
- `/system-health agents` - Agent-specific health data
- `/system-health performance` - Performance metrics
- `/system-health squads` - Squad-specific health data
- `/system-health predictive` - Predictive health analysis

**Health Metrics:**
- **System Reliability** - Overall system reliability percentage
- **Agent Performance** - Individual agent performance metrics
- **Squad Coordination** - Inter-squad coordination effectiveness
- **Resource Utilization** - System resource usage statistics
- **Predictive Analysis** - Future health predictions and recommendations

---

### `/performance`
**Description:** Show system performance metrics and optimization suggestions  
**Usage:** `/performance [metric]`  
**Metrics:**
- `/performance` - Overall performance overview
- `/performance response-time` - Response time analysis
- `/performance throughput` - System throughput metrics
- `/performance resource-usage` - Resource utilization data
- `/performance squads` - Squad-specific performance metrics
- `/performance agents` - Individual agent performance

---

### `/logs`
**Description:** Access system logs and activity history  
**Usage:** `/logs [filter]`  
**Filters:**
- `/logs` - Recent system logs
- `/logs errors` - Error logs only
- `/logs agents` - Agent activity logs
- `/logs performance` - Performance logs
- `/logs squads` - Squad activity logs
- `/logs [date]` - Logs from specific date

---

## 🔧 Advanced Commands

### `/debug`
**Description:** Enable debug mode for detailed system information  
**Usage:** `/debug [component]`  
**Components:**
- `/debug` - Enable general debug mode
- `/debug agents` - Debug agent interactions
- `/debug commands` - Debug command processing
- `/debug github` - Debug GitHub integration
- `/debug squads` - Debug squad coordination
- `/debug tiers` - Debug tier interactions

---

### `/optimize`
**Description:** Run system optimization and performance tuning  
**Usage:** `/optimize [target]`  
**Targets:**
- `/optimize` - General system optimization
- `/optimize performance` - Performance optimization
- `/optimize memory` - Memory usage optimization
- `/optimize cache` - Cache optimization
- `/optimize squads` - Squad coordination optimization
- `/optimize agents` - Agent performance optimization

---

### `/backup`
**Description:** Create system backup and configuration snapshot  
**Usage:** `/backup [scope]`  
**Scopes:**
- `/backup` - Full system backup
- `/backup config` - Configuration backup only
- `/backup data` - Data backup only
- `/backup squads` - Squad configuration backup
- `/backup agents` - Agent configuration backup

---

### `/restore`
**Description:** Restore system from backup  
**Usage:** `/restore [backup-id]`  
**Options:**
- `/restore` - Interactive restore selection
- `/restore latest` - Restore from latest backup
- `/restore [id]` - Restore from specific backup

---

## 📖 Documentation Commands

### `/tutorial`
**Description:** Access interactive JAEGIS tutorial  
**Usage:** `/tutorial [section]`  
**Sections:**
- `/tutorial` - Start from beginning
- `/tutorial basics` - Basic usage tutorial
- `/tutorial advanced` - Advanced features tutorial
- `/tutorial configuration` - Configuration tutorial
- `/tutorial squads` - Squad management tutorial
- `/tutorial agents` - Agent management tutorial

---

### `/best-practices`
**Description:** View system optimization best practices  
**Usage:** `/best-practices [category]`  
**Categories:**
- `/best-practices` - General best practices
- `/best-practices performance` - Performance optimization
- `/best-practices configuration` - Configuration best practices
- `/best-practices agents` - Agent management best practices
- `/best-practices squads` - Squad coordination best practices

---

### `/examples`
**Description:** See example configurations and use cases  
**Usage:** `/examples [type]`  
**Types:**
- `/examples` - All examples
- `/examples config` - Configuration examples
- `/examples workflows` - Workflow examples
- `/examples integrations` - Integration examples
- `/examples squads` - Squad configuration examples
- `/examples agents` - Agent usage examples

---

## 🔄 Data Management Commands

### `/export-config`
**Description:** Export current configuration for backup  
**Usage:** `/export-config [format]`  
**Formats:**
- `/export-config` - Default JSON format
- `/export-config json` - JSON format
- `/export-config yaml` - YAML format

---

### `/import-config`
**Description:** Import previously saved configuration  
**Usage:** `/import-config [source]`  
**Sources:**
- `/import-config` - Interactive file selection
- `/import-config file` - Import from file
- `/import-config url` - Import from URL

---

## 🚀 Quick Actions

### `/quick-start`
**Description:** Quick start wizard for new users  
**Usage:** `/quick-start`  
**Features:** Guided setup, configuration, and first project creation

---

### `/emergency-reset`
**Description:** Emergency system reset for critical issues  
**Usage:** `/emergency-reset`  
**Warning:** This will reset all configurations to factory defaults

---

## 📈 Analytics Commands

### `/analytics`
**Description:** View detailed system analytics and insights  
**Usage:** `/analytics [period]`  
**Periods:**
- `/analytics` - Current session analytics
- `/analytics daily` - Daily analytics
- `/analytics weekly` - Weekly analytics
- `/analytics monthly` - Monthly analytics
- `/analytics squads` - Squad-specific analytics
- `/analytics agents` - Agent-specific analytics

---

### `/agent-stats`
**Description:** Display agent performance and utilization statistics  
**Usage:** `/agent-stats [agent]`  
**Options:**
- `/agent-stats` - All agent statistics
- `/agent-stats [agent-name]` - Specific agent statistics
- `/agent-stats top` - Top performing agents
- `/agent-stats squad [squad-name]` - Squad-specific agent statistics

---

## 🔗 Integration Commands

### `/github`
**Description:** GitHub integration management  
**Usage:** `/github [action]`  
**Actions:**
- `/github status` - GitHub connection status
- `/github sync` - Sync with GitHub repository
- `/github update` - Update commands from GitHub
- `/github config` - Configure GitHub settings
- `/github fetch` - Fetch resources from GitHub

---

### `/api`
**Description:** API integration and management  
**Usage:** `/api [service]`  
**Services:**
- `/api status` - API connection status
- `/api test` - Test API connections
- `/api config` - Configure API settings

---

## 🎯 Context Commands

### `/context`
**Description:** Manage conversation context and memory  
**Usage:** `/context [action]`  
**Actions:**
- `/context` - View current context
- `/context save` - Save current context
- `/context load` - Load saved context
- `/context clear` - Clear current context

---

### `/memory`
**Description:** Advanced memory module configuration and management  
**Usage:** `/memory [action]`  
**Actions:**
- `/memory` - View memory system overview and status
- `/memory config` - Configure memory system parameters
- `/memory search` - Search and retrieve memories
- `/memory store` - Store new memories with metadata
- `/memory decay` - Configure memory decay and lifecycle
- `/memory optimize` - Optimize memory performance
- `/memory monitor` - Monitor memory system health
- `/memory analytics` - View memory analytics and insights
- `/memory patterns` - Analyze usage patterns
- `/memory preferences` - Manage user preferences
- `/memory history` - View command and interaction history
- `/memory cognitive` - Configure cognitive memory features
- `/memory temporal` - Configure temporal intelligence features
- `/memory self-improving` - Configure self-improving memory systems

---

## 🧠 Advanced Memory Module Commands

### `/memory-config`
**Description:** Configure advanced memory system parameters and settings  
**Usage:** `/memory-config [component]`  
**Components:**
- `/memory-config` - Open memory configuration menu
- `/memory-config backend` - Configure memory backend (RedisStack, Basic Redis)
- `/memory-config vector` - Configure vector search settings
- `/memory-config indexing` - Configure HNSW indexing parameters
- `/memory-config decay` - Configure memory decay settings
- `/memory-config namespaces` - Configure memory namespaces
- `/memory-config metadata` - Configure metadata handling

**Configuration Options:**
- **Backend Type** - RedisStack (HNSW) or Basic Redis
- **Vector Search** - Enable/disable semantic search capabilities
- **Indexing Method** - HNSW indexing for 100x faster search
- **Similarity Threshold** - Relevance threshold for memory retrieval
- **Context Search** - Enable conversation context awareness
- **Temporal Ranking** - Enable temporal-based memory ranking

---

### `/memory-search`
**Description:** Advanced memory search and retrieval with multiple search modes  
**Usage:** `/memory-search [mode] [query]`  
**Modes:**
- `/memory-search semantic [query]` - Semantic search using vector embeddings
- `/memory-search contextual [query]` - Context-aware search with conversation history
- `/memory-search temporal [query]` - Temporal search with time-based ranking
- `/memory-search hybrid [query]` - Hybrid search combining multiple methods
- `/memory-search namespace [namespace] [query]` - Search within specific namespace
- `/memory-search metadata [key=value] [query]` - Search by metadata filters

**Search Parameters:**
- **Limit** - Maximum number of results (default: 10)
- **Similarity Threshold** - Minimum relevance score (default: 0.8)
- **Context Weight** - Weight for context awareness (default: 0.4)
- **Temporal Weight** - Weight for temporal ranking (default: 0.3)
- **Enable Context Search** - Include conversation context (default: true)
- **Enable Temporal Ranking** - Boost recent memories (default: true)

**Examples:**
- `/memory-search semantic "machine learning algorithms"` - Semantic search
- `/memory-search contextual "project status" 5 0.9` - Contextual search with custom params
- `/memory-search namespace "user_conversations" "previous discussions"` - Namespace search

---

### `/memory-store`
**Description:** Store memories with intelligent classification and metadata  
**Usage:** `/memory-store [type] [content]`  
**Types:**
- `/memory-store auto [content]` - Auto-classify memory type
- `/memory-store short-term [content]` - Store as short-term memory
- `/memory-store long-term [content]` - Store as long-term memory
- `/memory-store episodic [content]` - Store episodic memory
- `/memory-store semantic [content]` - Store semantic memory
- `/memory-store working [content]` - Store working memory

**Storage Options:**
- **Vector Encoding** - Enable vector embeddings for search
- **Metadata** - Attach custom metadata to memories
- **Timestamp** - Automatic timestamp generation
- **Namespace** - Specify memory namespace
- **Confidence** - Set confidence level for stored information
- **Source** - Track memory source (user_input, system_generated, etc.)

**Examples:**
- `/memory-store auto "User prefers Python for data science projects"` - Auto-classified
- `/memory-store long-term "Important project deadline: March 15th" --vector --metadata priority:high` - Long-term with metadata

---

### `/memory-decay`
**Description:** Configure memory decay and lifecycle management  
**Usage:** `/memory-decay [action]`  
**Actions:**
- `/memory-decay` - View current decay configuration
- `/memory-decay enable` - Enable memory decay system
- `/memory-decay disable` - Disable memory decay system
- `/memory-decay configure` - Configure decay parameters
- `/memory-decay cleanup` - Manually trigger memory cleanup
- `/memory-decay stats` - View decay statistics

**Decay Configuration:**
- **Short Term Hours** - Duration for short-term memories (default: 2 hours)
- **Long Term Hours** - Duration for long-term memories (default: 168 hours)
- **Check Interval Minutes** - Cleanup frequency (default: 30 minutes)
- **Decay Curve** - Type of decay curve (linear, exponential, logarithmic)
- **Importance Boost** - Boost important memories decay time

**Examples:**
- `/memory-decay configure short_term_hours:4 long_term_hours:336 check_interval_minutes:60` - Custom decay settings
- `/memory-decay cleanup` - Manual cleanup of expired memories

---

### `/memory-optimize`
**Description:** Optimize memory system performance and efficiency  
**Usage:** `/memory-optimize [target]`  
**Targets:**
- `/memory-optimize` - General memory optimization
- `/memory-optimize performance` - Optimize for performance
- `/memory-optimize storage` - Optimize storage efficiency
- `/memory-optimize retrieval` - Optimize retrieval speed
- `/memory-optimize indexing` - Optimize indexing performance
- `/memory-optimize resources` - Optimize resource usage

**Optimization Strategies:**
- **Parameter Tuning** - Adjust memory system parameters
- **Structural Adjustment** - Modify memory structure
- **Resource Allocation** - Optimize resource allocation
- **Cache Management** - Optimize caching strategies
- **Index Optimization** - Optimize search indexes

---

### `/memory-monitor`
**Description:** Monitor memory system health and performance in real-time  
**Usage:** `/memory-monitor [aspect]`  
**Aspects:**
- `/memory-monitor` - Real-time memory dashboard
- `/memory-monitor health` - Memory system health status
- `/memory-monitor performance` - Performance metrics
- `/memory-monitor resources` - Resource utilization
- `/memory-monitor errors` - Error monitoring
- `/memory-monitor alerts` - Alert management

**Dashboard Metrics:**
- **Total Memories** - Number of stored memories
- **Active Memories** - Currently accessible memories
- **HNSW Performance** - Vector search performance
- **Memory Types** - Distribution by memory type
- **Search Latency** - Average search response time
- **Storage Usage** - Memory storage utilization

**Examples:**
- `/memory-monitor` - Launch real-time dashboard
- `/memory-monitor performance` - View performance metrics

---

### `/memory-analytics`
**Description:** Advanced memory analytics and insights  
**Usage:** `/memory-analytics [type]`  
**Types:**
- `/memory-analytics usage` - Usage pattern analysis
- `/memory-analytics performance` - Performance analytics
- `/memory-analytics retention` - Memory retention analysis
- `/memory-analytics quality` - Memory quality assessment
- `/memory-analytics trends` - Trend analysis and forecasting

**Analytics Features:**
- **Pattern Recognition** - Identify usage patterns
- **Performance Metrics** - Detailed performance analysis
- **Retention Rates** - Memory retention statistics
- **Quality Scores** - Memory quality assessment
- **Predictive Analysis** - Future usage predictions

---

### `/memory-cognitive`
**Description:** Configure cognitive memory features and intelligence  
**Usage:** `/memory-cognitive [feature]`  
**Features:**
- `/memory-cognitive` - View cognitive features status
- `/memory-cognitive enable` - Enable cognitive memory
- `/memory-cognitive disable` - Disable cognitive memory
- `/memory-cognitive configure` - Configure cognitive parameters
- `/memory-cognitive patterns` - Configure pattern recognition
- `/memory-cognitive learning` - Configure learning mechanisms

**Cognitive Features:**
- **Pattern Recognition** - Identify and learn patterns
- **Adaptive Learning** - Adapt to user behavior
- **Predictive Memory** - Predict future information needs
- **Contextual Understanding** - Deep context comprehension
- **Self-Improvement** - Automatic system optimization

---

### `/memory-temporal`
**Description:** Configure temporal intelligence and time-based memory features  
**Usage:** `/memory-temporal [feature]`  
**Features:**
- `/memory-temporal` - View temporal features status
- `/memory-temporal enable` - Enable temporal intelligence
- `/memory-temporal disable` - Disable temporal intelligence
- `/memory-temporal configure` - Configure temporal parameters
- `/memory-temporal historical` - Configure historical analysis
- `/memory-temporal predictive` - Configure predictive features

**Temporal Features:**
- **Historical Analysis** - Analyze past experiences
- **Present Context** - Understand current situations
- **Future Simulation** - Simulate future scenarios
- **Cross-Temporal Integration** - Integrate time perspectives
- **Temporal Binding** - Connect related time periods

---

### `/memory-self-improving`
**Description:** Configure self-improving memory systems  
**Usage:** `/memory-self-improving [aspect]`  
**Aspects:**
- `/memory-self-improving` - View self-improving status
- `/memory-self-improving enable` - Enable self-improvement
- `/memory-self-improving disable` - Disable self-improvement
- `/memory-self-improving configure` - Configure improvement parameters
- `/memory-self-improving learning` - Configure learning mechanisms
- `/memory-self-improving optimization` - Configure optimization targets

**Self-Improvement Features:**
- **Reinforcement Learning** - Learn from interactions
- **Supervised Learning** - Learn from feedback
- **Unsupervised Learning** - Discover patterns independently
- **Metacognitive Monitoring** - Monitor own performance
- **Adaptive Optimization** - Continuously improve performance

---

### `/memory-workflow`
**Description:** Create and manage memory-centric workflows  
**Usage:** `/memory-workflow [action]`  
**Actions:**
- `/memory-workflow` - View memory workflows
- `/memory-workflow create` - Create new memory workflow
- `/memory-workflow configure` - Configure workflow parameters
- `/memory-workflow execute` - Execute memory workflow
- `/memory-workflow monitor` - Monitor workflow execution

**Workflow Types:**
- **Conversational AI** - Memory-enhanced conversation systems
- **Knowledge Base** - Intelligent knowledge management
- **Content Analysis** - Content processing and analysis
- **Iterative Improvement** - Self-improving workflows
- **Cognitive Society** - Multi-agent deliberation systems

---

## 🛡️ Security Commands

### `/security`
**Description:** Security status and configuration  
**Usage:** `/security [check]`  
**Checks:**
- `/security` - General security status
- `/security scan` - Security vulnerability scan
- `/security config` - Security configuration
- `/security logs` - Security event logs

---

## 📱 Mobile & Accessibility Commands

### `/accessibility`
**Description:** Accessibility features and configuration  
**Usage:** `/accessibility [feature]`  
**Features:**
- `/accessibility` - Accessibility status
- `/accessibility voice` - Voice command configuration
- `/accessibility display` - Display accessibility options

---

## 🌐 Internationalization Commands

### `/language`
**Description:** Language and localization settings  
**Usage:** `/language [locale]`  
**Locales:**
- `/language` - Current language settings
- `/language en` - English
- `/language es` - Spanish
- `/language fr` - French
- `/language de` - German

---

## 🔍 Search Commands

### `/search`
**Description:** Search through commands, documentation, and history  
**Usage:** `/search [query]`  
**Examples:**
- `/search config` - Search for configuration-related commands
- `/search agent` - Search for agent-related commands
- `/search squad` - Search for squad-related commands
- `/search help` - Search for help-related content

---

## 💡 Tips & Shortcuts

### Quick Command Access
- Type `/` to see command suggestions
- Use Tab completion for command names
- Use arrow keys to navigate command history

### Command Chaining
- Chain commands with `&&`: `/config && /status`
- Use pipes for data flow: `/agents | /activate`

### Aliases
- `/h` = `/help`
- `/c` = `/config`
- `/s` = `/status`
- `/a` = `/agents`
- `/sq` = `/squad-status`

---

## 🆘 Emergency Commands

### `/emergency`
**Description:** Emergency system commands for critical situations  
**Usage:** `/emergency [action]`  
**Actions:**
- `/emergency stop` - Emergency stop all processes
- `/emergency reset` - Emergency system reset
- `/emergency backup` - Emergency backup creation
- `/emergency contact` - Emergency support contact

---

## 🏆 Squad-Specific Commands

### `/iuas`
**Description:** Internal Updates Agent Squad management  
**Usage:** `/iuas [action]`  
**Actions:**
- `/iuas status` - IUAS squad status
- `/iuas activate` - Activate IUAS squad
- `/iuas config` - Configure IUAS squad
- `/iuas monitors` - System monitors status
- `/iuas coordinators` - Update coordinators status

---

### `/garas`
**Description:** Gaps Analysis and Resolution Agent Squad management  
**Usage:** `/garas [action]`  
**Actions:**
- `/garas status` - GARAS squad status
- `/garas activate` - Activate GARAS squad
- `/garas config` - Configure GARAS squad
- `/garas detection` - Gap detection status
- `/garas resolution` - Gap resolution status

---

## 📋 Agent Coordination Commands

### `/coordination`
**Description:** Manage agent coordination and communication  
**Usage:** `/coordination [aspect]`  
**Aspects:**
- `/coordination status` - Coordination status overview
- `/coordination protocols` - View coordination protocols
- `/coordination optimize` - Optimize coordination processes
- `/coordination conflicts` - Resolve coordination conflicts

---

### `/handoff`
**Description:** Manage agent handoff processes  
**Usage:** `/handoff [action]`  
**Actions:**
- `/handoff status` - Handoff process status
- `/handoff configure` - Configure handoff protocols
- `/handoff monitor` - Monitor handoff operations
- `/handoff optimize` - Optimize handoff processes

---

**For additional help or support, use `/help [command]` for detailed information about any specific command.**

**System Status:** ✅ All commands operational  
**Last Verified:** 19 AUGUST, 2025  
**Command Count:** 100+ commands available  
**Agent Support:** 128+ agents across 6 tiers  
**Squad Support:** Multiple specialized squads with coordination protocols  
**Memory System:** Advanced cognitive memory with HNSW vector search, temporal intelligence, and self-improving capabilities
