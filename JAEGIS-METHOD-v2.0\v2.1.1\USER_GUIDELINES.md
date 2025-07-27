# JAEGIS GitHub Integration - User Guidelines (N.L.D.S. Enhanced)

## Natural Language Interface (Primary Method)

**Simply type your request in natural language - No commands needed!**

### Examples of Natural Language Input:
```text
"Fetch the JAEGIS guidelines from GitHub"
"I need the GOLD.md file from the repository"
"Load the master guidelines document"
"Get the latest JAEGIS documentation"
"Show me the system guidelines"
```

**N.L.D.S. automatically:**
- Analyzes your input through three-dimensional processing
- Selects optimal mode (confidence ≥85%)
- Fetches GitHub resources (GOLD.md + related links that come out of GOLD.md)
- Activates appropriate agents and squads
- Applies A.M.A.S.I.A.P. Protocol enhancement

## Single Line Command for GitHub Guideline Fetching (Advanced Users)

```python
await process_github_integration("Fetch JAEGIS guidelines", "https://github.com/usemanusai/JAEGIS/GOLD.md", enable_amasiap=True, enable_multi_fetch=True)
```

**Usage Example:**
```python
from github_integration.integration_orchestrator import process_github_integration

# Fetch JAEGIS GOLD.md guidelines with full integration
result = await process_github_integration(
    user_input="Fetch JAEGIS guidelines",
    github_url="https://github.com/usemanusai/JAEGIS/GOLD.md",
    enable_amasiap=True,
    enable_multi_fetch=True
)
```

## Complete System Integration Features

This triggers the complete JAEGIS GitHub Integration System including:
- **N.L.D.S. Processing**: Three-dimensional input analysis
- **Automatic Mode Selection**: Optimal mode selection (≥85% confidence)
- **Single GitHub Link Fetching**: GOLD.md primary document
- **Multi-Fetch Discovery**: Automatic discovery and fetching of related resources
- **Dynamic Resource Loading**: Commands.md, agent-config.txt, and other linked resources
- **A.M.A.S.I.A.P. Protocol**: Automatic input enhancement with 15-20 research queries
- **Agent Squad Coordination**: Specialized squads activated based on requirements
- **7-Tier Architecture**: Full 128+ agent system with N.L.D.S. as Tier 0

## N.L.D.S. Confidence Levels

- **High Confidence (≥85%)**: Automatic execution with selected mode
- **Low Confidence (<85%)**: Manual mode selection menu presented
- **Fallback Available**: Traditional command interface always accessible
