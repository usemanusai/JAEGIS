# Getting Started with JAEGIS Method

Welcome to the JAEGIS Method! This guide will help you get started with structured human-AI collaborative project development.

## 🎯 What You'll Learn

By the end of this guide, you'll understand:
- How to set up JAEGIS for your preferred platform
- The four phases of the JAEGIS methodology
- How to start your first JAEGIS project
- Best practices for effective collaboration

## 🚀 Quick Start (5 Minutes)

### Step 1: Choose Your Platform

Pick the AI platform you prefer to work with:

#### 🔵 **Claude Code** (Recommended for Developers)
- **Best for**: Terminal-based development, file system integration
- **Setup time**: 5 minutes
- **Requirements**: Python 3.8+, terminal access

```bash
# Install JAEGIS MCP Server
git clone https://github.com/jaegis-method/claude-code-integration.git
cd claude-code-integration
pip install -r requirements.txt
python jaegis-mcp-server.py server
```

#### 🟢 **Gemini Gems** (Recommended for Google Users)
- **Best for**: Google ecosystem integration, conversation-based workflows
- **Setup time**: 2 minutes
- **Requirements**: Google account with Gemini access

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Search for "JAEGIS" in the Gems gallery
3. Start with "JAEGIS Orchestrator" gem

#### 🟠 **ChatGPT Custom GPTs** (Recommended for OpenAI Users)
- **Best for**: OpenAI ecosystem, action-based workflows
- **Setup time**: 3 minutes
- **Requirements**: ChatGPT Plus/Pro subscription

1. Go to [ChatGPT](https://chat.openai.com)
2. Search for "JAEGIS" in the GPT Store
3. Start with "JAEGIS Method Orchestrator"

### Step 2: Start Your First Project

Once you've chosen your platform, start with this simple command:

```
I want to build a [your project type] that [brief description]
```

**Examples**:
- "I want to build a mobile app that helps people track their fitness goals"
- "I want to build a web application that manages small business inventory"
- "I want to build a Unity 2D game that teaches kids about recycling"

### Step 3: Follow the JAEGIS Flow

The AI will guide you through the four phases:

1. **🧠 Brainstorming**: Generate and explore ideas
2. **📋 Modeling**: Create detailed requirements (PRD)
3. **🏗️ Architecture**: Design technical system
4. **💻 Development**: Build and implement

## 📚 Understanding JAEGIS Phases

### Phase 1: 🧠 Brainstorming (15-30 minutes)

**Goal**: Generate creative, well-researched ideas for your project

**What Happens**:
- Psychology-backed ideation using proven techniques
- Exploration of user needs and pain points
- Creative problem-solving and opportunity identification
- Documentation of all ideas for later evaluation

**Example Interaction**:
```
AI: Let's start brainstorming! What specific problems does your fitness app solve?

You: People struggle to stay motivated with their fitness routines.

AI: Great insight! Let's explore this from multiple angles:
🎮 Gaming: How do games keep players engaged? (achievements, progression, social competition)
📱 Social Media: What makes apps addictive? (streaks, sharing, community)
🏆 Sports: What motivates athletes? (personal bests, team dynamics, seasons)

Which of these resonates with your vision?
```

**Key Techniques Used**:
- Analogical thinking
- Stakeholder perspective-taking
- What-if analysis
- Creative constraint application

### Phase 2: 📋 Modeling (30-60 minutes)

**Goal**: Create a comprehensive Product Requirements Document (PRD)

**What Happens**:
- Interactive template guides you through each section
- AI asks clarifying questions to ensure completeness
- User stories and acceptance criteria development
- Stakeholder analysis and feature prioritization

**Example Sections**:
- **Executive Summary**: Problem statement and solution overview
- **User Personas**: Detailed target user profiles
- **Functional Requirements**: What the product must do
- **Technical Requirements**: Performance, security, scalability needs
- **Success Metrics**: How you'll measure success

**Example Interaction**:
```
AI: Let's define your primary user persona. Based on our brainstorming, I see fitness motivation as key.

You: My main user is busy professionals who want to stay fit but struggle with time and motivation.

AI: Perfect! Let's develop this persona:
👤 Name: "Busy Professional Beth"
📊 Demographics: 28-45, works 50+ hours/week, household income $60k+
🎯 Goals: Stay healthy, feel energetic, look good
😰 Pain Points: No time, boring workouts, lack of progress visibility
💡 Motivations: Efficiency, social validation, measurable progress

Does this capture your target user?
```

### Phase 3: 🏗️ Architecture (30-45 minutes)

**Goal**: Design the technical system architecture

**What Happens**:
- Analysis of technical requirements from PRD
- Architecture pattern selection (monolithic, microservices, serverless)
- Technology stack recommendations
- System component design and interaction mapping

**Example Interaction**:
```
AI: Based on your PRD, your fitness app needs:
- Real-time activity tracking
- Social features and leaderboards
- Push notifications
- Data analytics and insights

For this, I recommend a microservices architecture:

🏗️ **Core Components**:
- User Service (authentication, profiles)
- Activity Service (tracking, data processing)
- Social Service (friends, leaderboards, sharing)
- Notification Service (push notifications, reminders)
- Analytics Service (insights, reporting)

📱 **Frontend**: React Native for cross-platform mobile
🔧 **Backend**: Node.js with Express
💾 **Database**: PostgreSQL for user data, Redis for real-time features
☁️ **Infrastructure**: AWS with containerized deployment

What's your team's experience with these technologies?
```

### Phase 4: 💻 Development (Ongoing)

**Goal**: Build the application with AI assistance

**What Happens**:
- Code generation and scaffolding
- Development workflow coordination
- Quality assurance and testing guidance
- Deployment and maintenance planning

**Example Interaction**:
```
AI: Let's start with the User Service. I'll generate the basic structure:

📁 **Generated Files**:
- user-service/
  ├── src/
  │   ├── models/User.js
  │   ├── routes/auth.js
  │   ├── controllers/userController.js
  │   └── middleware/auth.js
  ├── tests/
  └── package.json

🔧 **Next Steps**:
1. Review the generated code structure
2. Customize the User model for your needs
3. Set up the database connection
4. Implement authentication logic

Which component should we work on first?
```

## 🎯 Best Practices for Success

### 1. **Be Specific and Detailed**
- Provide context about your project goals
- Share your technical background and constraints
- Describe your target users clearly

**Good**: "I want to build a mobile app for busy professionals who struggle to maintain fitness routines due to time constraints and lack of motivation."

**Better**: "I want to build a mobile app for busy professionals (ages 28-45, working 50+ hours/week) who struggle to maintain fitness routines. The app should gamify fitness with social features, provide quick 15-minute workouts, and integrate with wearable devices."

### 2. **Engage Actively in Each Phase**
- Don't just accept AI suggestions - build on them
- Ask questions when something isn't clear
- Provide feedback on generated ideas and designs

### 3. **Use the Iterative Nature**
- JAEGIS is designed for iteration and refinement
- Go back to previous phases when you learn new information
- Use insights from later phases to improve earlier work

### 4. **Document Everything**
- Save all brainstorming ideas, even "wild" ones
- Keep detailed notes on architectural decisions
- Maintain a project journal of lessons learned

## 🛠️ Platform-Specific Tips

### Claude Code Tips
- Use the terminal commands for quick project setup
- Leverage file system integration for automatic documentation
- Take advantage of real-time code generation and editing

### Gemini Gems Tips
- Use different gems for different phases (Orchestrator → Brainstorming → Product Manager → Architect)
- Leverage Google's knowledge integration for research
- Use conversation history to maintain context

### ChatGPT Custom GPT Tips
- Use actions for advanced functionality
- Upload relevant files for context
- Leverage the knowledge base for best practices

## 🚨 Common Pitfalls to Avoid

### 1. **Rushing Through Brainstorming**
- **Problem**: Jumping to solutions too quickly
- **Solution**: Spend adequate time exploring the problem space

### 2. **Vague Requirements**
- **Problem**: Creating PRDs that are too high-level
- **Solution**: Use the AI to drill down into specifics

### 3. **Over-Engineering Architecture**
- **Problem**: Designing for scale you don't need yet
- **Solution**: Start simple, plan for growth

### 4. **Passive Participation**
- **Problem**: Letting the AI do all the work
- **Solution**: Stay engaged and provide input throughout

## 📈 Measuring Success

Track your JAEGIS project success with these metrics:

### Process Metrics
- **Time to PRD**: How quickly you complete requirements
- **Architecture Clarity**: How well-defined your technical design is
- **Development Velocity**: How quickly you can implement features

### Quality Metrics
- **Requirement Completeness**: Are all user needs addressed?
- **Technical Soundness**: Is the architecture scalable and maintainable?
- **User Satisfaction**: Do users find value in your solution?

## 🎓 Next Steps

Once you've completed your first JAEGIS project:

1. **Explore Advanced Features**:
   - Try different elicitation techniques in brainstorming
   - Use expansion packs for domain-specific guidance
   - Experiment with different PRD templates

2. **Join the Community**:
   - Share your project in the JAEGIS Discord
   - Contribute to open-source expansion packs
   - Help improve documentation and tutorials

3. **Scale Your Usage**:
   - Use JAEGIS for team projects
   - Create custom expansion packs for your domain
   - Integrate JAEGIS into your organization's workflow

## 🔗 Quick Reference Links

- **[Core Concepts](./core-concepts.md)**: Deep dive into JAEGIS principles
- **[Workflow Guide](./workflow-guide.md)**: Detailed phase-by-phase instructions
- **[Platform Integrations](../integrations/)**: Setup guides for each platform
- **[Tutorials](../tutorials/)**: Step-by-step project examples
- **[Best Practices](../best-practices/)**: Advanced tips and techniques

---

**Ready to start?** Choose your platform above and begin your first JAEGIS project! Remember: the key to success is active engagement and iteration. The AI is your collaborative partner, not a replacement for your creativity and decision-making.

**Questions?** Join our [Discord community](https://discord.gg/jaegis-method) for real-time support and discussion!
