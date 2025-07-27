# JAEGIS Gemini Gems Integration

Complete integration of the JAEGIS Method with Google's Gemini Gems for specialized AI assistants within Google's ecosystem.

## Overview

This integration provides four specialized Gemini Gems that implement the full JAEGIS methodology:

- **🎯 JAEGIS Orchestrator**: Master coordinator for the entire JAEGIS workflow
- **🧠 JAEGIS Brainstorming Specialist**: Psychology-backed creative ideation expert
- **📋 JAEGIS Product Manager**: Interactive PRD creation specialist
- **🏗️ JAEGIS Technical Architect**: System design and architecture expert

## Quick Start

### Option 1: Use Pre-configured Gems (Recommended)

1. **Access Google AI Studio**: Go to [aistudio.google.com](https://aistudio.google.com)
2. **Find JAEGIS Gems**: Search for "JAEGIS" in the Gems gallery
3. **Start Using**: Click on any JAEGIS Gem to begin

### Option 2: Create Your Own Gems

1. **Copy Configuration**: Use the configurations from `gem-configurations.yaml`
2. **Create New Gem**: In Google AI Studio, click "Create new Gem"
3. **Configure**: Paste the system instructions and conversation starters
4. **Test**: Verify the gem works as expected

## Available Gems

### 🎯 JAEGIS Orchestrator
**Purpose**: Master coordinator for the entire JAEGIS methodology

**Best for**:
- Starting new projects
- Managing multi-phase workflows
- Coordinating between different JAEGIS phases
- Getting project status and next steps

**Example conversation**:
```
User: I want to build a mobile app for fitness tracking
Gem: 🚀 Great! Let's start a new JAEGIS project for your fitness tracking app. 
     I'll initialize the project and guide you through each phase.
     
     First, let me set up the project structure...
     [Calls jaegis_init_project function]
     
     ✅ Project initialized! Now, shall we start with brainstorming 
     features and user needs, or do you have specific requirements 
     already in mind?
```

### 🧠 JAEGIS Brainstorming Specialist
**Purpose**: Expert in psychology-backed creative ideation

**Best for**:
- Generating innovative ideas
- Breaking through creative blocks
- Exploring problems from multiple perspectives
- Using advanced brainstorming techniques

**Example conversation**:
```
User: I need ideas for making fitness tracking more engaging
Gem: 🧠 Perfect! Let's explore this using multiple brainstorming techniques.
     
     First, let's try analogical thinking - what other activities make 
     people naturally want to engage repeatedly?
     
     🎮 Games use progression systems...
     📱 Social media uses community features...
     🏆 Sports use competition and achievements...
     
     Which of these resonates with your vision? Let's dive deeper!
```

### 📋 JAEGIS Product Manager
**Purpose**: Interactive PRD creation and requirements gathering

**Best for**:
- Creating comprehensive product requirements
- Defining user stories and acceptance criteria
- Stakeholder analysis
- Feature prioritization

**Example conversation**:
```
User: Help me create a PRD for my fitness app
Gem: 📋 I'd love to help you create a comprehensive PRD! 
     
     Let's start with the executive summary. Based on our brainstorming,
     your fitness app focuses on engagement through gamification.
     
     ❓ What specific problem does your app solve that existing 
     fitness apps don't address well?
     
     ❓ Who is your primary target user? (age, fitness level, tech comfort)
     
     Let's build this section by section to ensure we capture everything!
```

### 🏗️ JAEGIS Technical Architect
**Purpose**: System design and technical architecture guidance

**Best for**:
- Designing system architecture
- Technology selection
- Scalability planning
- Technical documentation

**Example conversation**:
```
User: I need to design the architecture for my fitness tracking app
Gem: 🏗️ Excellent! Let's design a robust architecture for your fitness app.
     
     Based on your PRD, I see you need:
     - Real-time activity tracking
     - Social features and leaderboards  
     - Data analytics and insights
     - Push notifications
     
     🤔 For this type of app, I'd recommend considering:
     
     **Option 1**: Microservices architecture for scalability
     **Option 2**: Serverless for cost-effectiveness
     **Option 3**: Hybrid approach
     
     What's your expected user scale and team size?
```

## Features

### 🔄 Seamless Workflow Integration
- **Phase Transitions**: Smooth handoffs between brainstorming, PRD, and architecture
- **Context Preservation**: Each gem maintains awareness of previous work
- **Progress Tracking**: Clear visibility into project completion status

### 🧠 Psychology-Backed Methods
- **30+ Elicitation Techniques**: Advanced brainstorming methods based on cognitive science
- **Dual-Process Thinking**: Leverages both System 1 (intuitive) and System 2 (analytical) thinking
- **Collaborative Intelligence**: Maintains user engagement while providing AI assistance

### 📋 Interactive Templates
- **Agentic Templates**: Templates that actively guide users through completion
- **Multiple Formats**: Standard, Agile, Startup, and Comprehensive PRD templates
- **Dynamic Adaptation**: Templates adjust based on project type and user expertise

### 🏗️ Architecture Intelligence
- **Pattern Recognition**: Recommends appropriate architecture patterns
- **Technology Matching**: Suggests technologies based on requirements
- **Trade-off Analysis**: Explains pros and cons of different approaches

## Advanced Usage

### Function Calling Integration

For advanced functionality, you can set up function calling with a JAEGIS API server:

```python
# Example function call from Gemini Gem
{
  "function_name": "jaegis_init_project",
  "parameters": {
    "project_name": "FitTracker Pro",
    "project_type": "mobile-app",
    "description": "Gamified fitness tracking application"
  }
}
```

### Multi-Gem Workflows

Use multiple gems in sequence for comprehensive project development:

1. **Start with Orchestrator**: Initialize project and get overview
2. **Use Brainstorming Specialist**: Generate and refine ideas
3. **Work with Product Manager**: Create detailed PRD
4. **Consult Technical Architect**: Design system architecture
5. **Return to Orchestrator**: Coordinate development phase

### Session Continuity

Maintain context across gem interactions:

```
Session ID: jaegis_session_abc123
Project: FitTracker Pro
Current Phase: Architecture Design
Previous Work: Brainstorming (15 ideas), PRD (5 sections complete)
```

## Configuration

### Custom Gem Setup

To create your own JAEGIS gems:

1. **Copy Base Configuration**:
   ```yaml
   # From gem-configurations.yaml
   system_instructions: |
     You are the JAEGIS [Specialist Type]...
   ```

2. **Customize for Your Needs**:
   - Adjust expertise areas
   - Modify conversation starters
   - Add domain-specific knowledge

3. **Test Thoroughly**:
   - Verify all conversation flows
   - Test error handling
   - Validate output quality

### API Integration (Optional)

For advanced features, set up the JAEGIS API server:

```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
python jaegis-api-server.py

# Configure gems to use API endpoints
```

## Best Practices

### For Users

1. **Start with Clear Goals**: Know what you want to build before beginning
2. **Engage Actively**: Provide detailed responses to gem questions
3. **Iterate and Refine**: Use gems to improve and polish your ideas
4. **Follow the Flow**: Trust the JAEGIS methodology sequence

### For Gem Creators

1. **Maintain Consistency**: Keep interaction patterns consistent across gems
2. **Preserve Context**: Ensure gems can reference previous work
3. **Quality Focus**: Prioritize output quality over speed
4. **User Engagement**: Keep users intellectually engaged in the process

## Troubleshooting

### Common Issues

**Gem Not Responding Appropriately**:
- Check system instructions are properly configured
- Verify conversation starters are engaging
- Test with simpler queries first

**Context Loss Between Gems**:
- Use session IDs to maintain continuity
- Reference previous work explicitly
- Consider using the Orchestrator gem as coordinator

**Function Calls Not Working**:
- Verify API server is running
- Check function definitions match implementation
- Test with simple function calls first

### Getting Help

- **Documentation**: [jaegis-method.com/docs/gemini-gems](https://jaegis-method.com/docs/gemini-gems)
- **Discord**: Join #gemini-gems channel
- **GitHub**: Report issues at [jaegis-method/gemini-gems](https://github.com/jaegis-method/gemini-gems)
- **Email**: gems-support@jaegis-method.com

## Examples

### Complete Project Workflow

```
1. 🎯 Orchestrator: "Let's build a task management app"
   → Initializes project structure
   → Recommends starting with brainstorming

2. 🧠 Brainstorming: "What makes task management frustrating?"
   → Generates 20+ ideas using multiple techniques
   → Identifies key pain points and opportunities

3. 📋 Product Manager: "Let's create a comprehensive PRD"
   → Guides through all PRD sections
   → Develops user stories and acceptance criteria

4. 🏗️ Architect: "Design the technical architecture"
   → Recommends microservices architecture
   → Selects appropriate technologies
   → Creates system diagrams

5. 🎯 Orchestrator: "Ready to begin development!"
   → Summarizes all previous work
   → Provides development roadmap
```

### Specialized Use Cases

**Startup MVP Development**:
- Use Brainstorming Specialist for market opportunity exploration
- Use Product Manager with "startup" template for lean PRD
- Use Architect for cost-effective serverless architecture

**Enterprise Application**:
- Use Orchestrator for stakeholder coordination
- Use Product Manager with "comprehensive" template
- Use Architect for scalable microservices design

**Creative Projects**:
- Focus heavily on Brainstorming Specialist
- Use Product Manager for creative brief development
- Use Architect for content management systems

## Contributing

We welcome contributions to improve the JAEGIS Gemini Gems:

1. **Test and Provide Feedback**: Use the gems and report issues
2. **Suggest Improvements**: Propose new features or enhancements
3. **Share Use Cases**: Document successful project workflows
4. **Create Specialized Gems**: Develop domain-specific variants

## License

MIT License - see LICENSE file for details.

---

**Ready to get started?** Visit [Google AI Studio](https://aistudio.google.com) and search for "JAEGIS" to find our pre-configured gems, or use the configurations in this repository to create your own!
