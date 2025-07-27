# JAEGIS ChatGPT Custom GPTs Integration

Complete integration of the JAEGIS Method with ChatGPT Custom GPTs for specialized AI assistants within OpenAI's ecosystem.

## Overview

This integration provides specialized ChatGPT Custom GPTs that implement the full JAEGIS methodology:

- **🎯 JAEGIS Orchestrator**: Master coordinator for the entire JAEGIS workflow
- **🧠 JAEGIS Brainstorming Specialist**: Psychology-backed creative ideation expert
- **📋 JAEGIS Product Manager**: Interactive PRD creation specialist
- **🏗️ JAEGIS Technical Architect**: System design and architecture expert

## Quick Start

### Prerequisites

- ChatGPT Plus or Pro subscription
- Access to Custom GPT creation
- JAEGIS API server (for advanced features)

### Option 1: Use Pre-built GPTs (Recommended)

1. **Access ChatGPT**: Go to [chat.openai.com](https://chat.openai.com)
2. **Find JAEGIS GPTs**: Search for "JAEGIS" in the GPT Store
3. **Start Using**: Click on any JAEGIS GPT to begin

### Option 2: Create Your Own GPTs

1. **Copy Configuration**: Use the JSON configurations from this directory
2. **Create New GPT**: In ChatGPT, go to "My GPTs" → "Create a GPT"
3. **Configure**: Import the JSON configuration or manually set up
4. **Test**: Verify the GPT works as expected

## Available GPTs

### 🎯 JAEGIS Orchestrator
**File**: `jaegis-orchestrator-gpt.json`

**Purpose**: Master coordinator for the entire JAEGIS methodology

**Key Features**:
- Project initialization and structure setup
- Phase coordination and progress tracking
- Quality assurance and validation
- Workflow orchestration across all JAEGIS phases

**Best for**:
- Starting new projects
- Managing complex multi-phase workflows
- Coordinating between different JAEGIS phases
- Getting project status and next steps

**Example Usage**:
```
User: I want to build a SaaS platform for small businesses
GPT: 🚀 Excellent! Let's start a new JAEGIS project for your SaaS platform. 
     I'll guide you through our structured methodology.
     
     [Initializes project with jaegis_init_project action]
     
     ✅ Project "SmallBiz SaaS" initialized! 
     
     Now, shall we start with brainstorming core features and user needs, 
     or do you have specific requirements already in mind?
```

### 🧠 JAEGIS Brainstorming Specialist
**File**: `jaegis-brainstorming-gpt.json`

**Purpose**: Expert in psychology-backed creative ideation

**Key Features**:
- 30+ advanced elicitation techniques
- Psychology-backed brainstorming methods
- Creative block breakthrough assistance
- Idea quality assessment and development

**Advanced Techniques**:
- **Analogical Thinking**: Drawing insights from distant domains
- **Perspective Taking**: Multiple stakeholder viewpoints
- **SCAMPER Method**: Systematic creative modification
- **Six Thinking Hats**: Structured parallel thinking
- **What-If Analysis**: Exploring alternative scenarios

**Example Usage**:
```
User: I need innovative features for a productivity app
GPT: 🧠 Let's explore this using analogical thinking!
     
     What other domains naturally boost productivity?
     🏭 **Manufacturing**: Assembly lines, just-in-time, automation
     🧠 **Neuroscience**: Focus states, cognitive load, habit formation
     🎵 **Music**: Rhythm, flow states, harmonious collaboration
     
     Which analogy sparks interesting ideas for your app?
```

### 📋 JAEGIS Product Manager
**File**: `jaegis-product-manager-gpt.json`

**Purpose**: Interactive PRD creation and requirements gathering

**Key Features**:
- Multiple PRD templates (Standard, Agile, Startup, Comprehensive)
- Interactive section-by-section guidance
- User story development with acceptance criteria
- Stakeholder analysis and feature prioritization

**Template Types**:
- **Standard**: Comprehensive product requirements
- **Agile**: Lightweight, iterative requirements
- **Startup**: MVP-focused requirements
- **Comprehensive**: Detailed enterprise requirements

**Example Usage**:
```
User: Help me create a PRD for my mobile game
GPT: 📋 Perfect! Let's create a comprehensive PRD for your mobile game.
     
     I'll use our interactive template that adapts to gaming projects.
     
     **Section 1: Game Concept & Vision**
     ❓ What genre is your game? (puzzle, action, RPG, etc.)
     ❓ What's the core gameplay loop?
     ❓ Who's your target audience?
     
     Let's build this section by section!
```

### 🏗️ JAEGIS Technical Architect
**File**: `jaegis-technical-architect-gpt.json`

**Purpose**: System design and technical architecture guidance

**Key Features**:
- Multiple architecture patterns (Monolithic, Microservices, Serverless)
- Technology selection and evaluation
- Scalability and performance planning
- Architecture documentation and diagrams

**Architecture Patterns**:
- **Monolithic**: Single deployable unit for simpler applications
- **Microservices**: Distributed services for complex systems
- **Serverless**: Function-based architecture for event-driven apps
- **Hybrid**: Combining patterns for optimal solutions

**Example Usage**:
```
User: Design architecture for a real-time chat application
GPT: 🏗️ Great! For a real-time chat app, let's consider the requirements:
     
     **Key Components Needed**:
     - Real-time messaging (WebSockets)
     - User authentication & presence
     - Message persistence & history
     - File/media sharing
     - Push notifications
     
     **Architecture Options**:
     1. **Microservices**: Best for scale (recommended)
     2. **Serverless**: Cost-effective for variable load
     3. **Hybrid**: Microservices + serverless functions
     
     What's your expected user scale and team size?
```

## Setup Instructions

### Step 1: Set Up JAEGIS API Server (Optional but Recommended)

The GPTs can work standalone, but for full functionality, set up the API server:

```bash
# Clone the repository
git clone https://github.com/jaegis-method/chatgpt-integration.git
cd chatgpt-integration

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start the API server
python jaegis-api-server.py
```

### Step 2: Create Custom GPTs

#### Method A: Import JSON Configuration

1. Go to ChatGPT → "My GPTs" → "Create a GPT"
2. Click "Configure" tab
3. Import the JSON configuration file
4. Adjust any settings as needed
5. Test the GPT

#### Method B: Manual Setup

1. **Create New GPT**: Go to "My GPTs" → "Create a GPT"
2. **Basic Info**:
   - Name: Copy from JSON file
   - Description: Copy from JSON file
   - Instructions: Copy the full instructions text
3. **Conversation Starters**: Add the provided starters
4. **Actions**: Set up each action with the provided schemas
5. **Knowledge**: Upload any relevant files
6. **Test**: Verify functionality

### Step 3: Configure Actions (For Full Functionality)

Each GPT uses actions to connect to the JAEGIS API:

1. **Get API Key**: Register at [api.jaegis-method.com](https://api.jaegis-method.com)
2. **Configure Actions**: 
   - Import action schemas from JSON files
   - Set authentication with your API key
   - Test each action endpoint
3. **Privacy Settings**: Configure according to your needs

## API Server Setup

### Requirements

```bash
# requirements.txt
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
python-multipart>=0.0.5
python-jose>=3.3.0
passlib>=1.7.4
python-dotenv>=0.19.0
```

### Basic API Server

```python
# jaegis-api-server.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="JAEGIS API Server", version="1.0.0")

class ProjectInit(BaseModel):
    project_name: str
    project_type: str
    description: Optional[str] = ""
    user_expertise: Optional[str] = "intermediate"

class BrainstormRequest(BaseModel):
    session_id: str
    topic: str
    techniques: Optional[List[str]] = []
    duration: Optional[int] = 30

@app.post("/v1/projects/init")
async def init_project(request: ProjectInit):
    session_id = str(uuid.uuid4())
    
    return {
        "session_id": session_id,
        "project_name": request.project_name,
        "project_structure": {
            "directories": ["docs", "brainstorming", "architecture", "development"],
            "files": ["README.md", "project-config.yaml"]
        },
        "next_steps": [
            "Start brainstorming session",
            "Create PRD",
            "Design architecture"
        ],
        "status": "initialized"
    }

@app.post("/v1/brainstorm/start")
async def start_brainstorm(request: BrainstormRequest):
    brainstorm_id = str(uuid.uuid4())
    
    # Mock brainstorming logic
    initial_ideas = [
        f"Innovative approach to {request.topic}",
        f"User-centric solution for {request.topic}",
        f"Scalable platform addressing {request.topic}"
    ]
    
    return {
        "brainstorm_id": brainstorm_id,
        "initial_ideas": initial_ideas,
        "suggested_techniques": ["analogical_thinking", "perspective_taking"],
        "interaction_prompt": f"Let's explore {request.topic} from multiple angles!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Running the Server

```bash
# Development
python jaegis-api-server.py

# Production
uvicorn jaegis-api-server:app --host 0.0.0.0 --port 8000
```

## Usage Examples

### Complete Project Workflow

```
1. 🎯 Start with Orchestrator
   User: "I want to build a food delivery app"
   → Initializes project structure
   → Recommends starting with brainstorming

2. 🧠 Use Brainstorming Specialist
   User: "What unique features could differentiate my app?"
   → Generates 20+ ideas using multiple techniques
   → Identifies key opportunities and pain points

3. 📋 Work with Product Manager
   User: "Let's create a comprehensive PRD"
   → Guides through all PRD sections
   → Develops detailed user stories and requirements

4. 🏗️ Consult Technical Architect
   User: "Design the system architecture"
   → Recommends microservices architecture
   → Selects appropriate technologies
   → Creates system diagrams

5. 🎯 Return to Orchestrator
   User: "What's next?"
   → Summarizes all previous work
   → Provides development roadmap
```

### Specialized Workflows

**Startup MVP Development**:
- Brainstorming Specialist: Market opportunity exploration
- Product Manager: Lean PRD with "startup" template
- Technical Architect: Cost-effective serverless architecture

**Enterprise Application**:
- Orchestrator: Stakeholder coordination
- Product Manager: Comprehensive PRD template
- Technical Architect: Scalable microservices design

## Best Practices

### For Users

1. **Start with Clear Goals**: Know what you want to build
2. **Engage Actively**: Provide detailed responses to GPT questions
3. **Follow the Flow**: Trust the JAEGIS methodology sequence
4. **Iterate and Refine**: Use GPTs to improve your ideas

### For GPT Creators

1. **Maintain Consistency**: Keep interaction patterns consistent
2. **Quality Focus**: Prioritize output quality over speed
3. **User Engagement**: Keep users intellectually engaged
4. **Test Thoroughly**: Verify all actions and workflows

## Troubleshooting

### Common Issues

**GPT Not Using Actions**:
- Verify API server is running
- Check action configurations
- Test with simple requests first

**Authentication Errors**:
- Verify API key is correct
- Check authentication headers
- Ensure proper permissions

**Inconsistent Responses**:
- Review system instructions
- Check for conflicting guidance
- Test with various inputs

### Getting Help

- **Documentation**: [jaegis-method.com/docs/chatgpt](https://jaegis-method.com/docs/chatgpt)
- **Discord**: Join #chatgpt-integration channel
- **GitHub**: Report issues at [jaegis-method/chatgpt-integration](https://github.com/jaegis-method/chatgpt-integration)
- **Email**: chatgpt-support@jaegis-method.com

## Contributing

1. **Test and Provide Feedback**: Use the GPTs and report issues
2. **Suggest Improvements**: Propose new features or enhancements
3. **Share Use Cases**: Document successful project workflows
4. **Create Specialized GPTs**: Develop domain-specific variants

## License

MIT License - see LICENSE file for details.

---

**Ready to get started?** Visit [ChatGPT](https://chat.openai.com) and search for "JAEGIS" in the GPT Store, or use the configurations in this repository to create your own!
