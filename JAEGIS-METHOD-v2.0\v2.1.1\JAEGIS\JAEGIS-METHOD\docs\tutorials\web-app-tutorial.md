# Tutorial: Building a Web Application with JAEGIS Method

This comprehensive tutorial walks you through building a complete web application using the JAEGIS methodology. We'll create a **Task Management SaaS Platform** from initial brainstorming to deployment.

## 🎯 Tutorial Overview

**What We're Building**: A collaborative task management platform for small teams
**Duration**: 2-3 hours
**Difficulty**: Intermediate
**Prerequisites**: Basic understanding of web development concepts

**Final Result**: 
- Complete PRD with user stories and acceptance criteria
- Technical architecture with technology recommendations
- Code scaffolding and implementation guidance
- Deployment strategy and next steps

## 🚀 Phase 1: Brainstorming (30 minutes)

### Step 1: Initialize the Project

**Platform**: We'll use ChatGPT Custom GPT for this tutorial

```
Prompt: I want to build a web application that helps small teams manage their tasks and projects more effectively. The current solutions are either too complex for small teams or lack the collaboration features they need.
```

**AI Response**:
```
🚀 Excellent! Let's start a new JAEGIS project for your task management platform. 

[Initializes project with jaegis_init_project action]

✅ Project "TeamTask Pro" initialized! 

Now, let's begin with Phase 1: Brainstorming. What specific pain points do small teams face with current task management tools?
```

### Step 2: Problem Exploration

**Your Response**:
```
Small teams struggle with:
1. Tools that are too complex and require extensive setup
2. Lack of real-time collaboration features
3. Poor visibility into team workload and progress
4. Difficulty prioritizing tasks across multiple projects
5. No integration with their existing workflow tools
```

**AI Response**:
```
🧠 Perfect insights! Let's explore these pain points using analogical thinking:

🎮 **Gaming Perspective**: How do multiplayer games handle team coordination?
- Real-time status updates (who's online, what they're doing)
- Clear role definitions and responsibilities
- Progress visualization (levels, achievements, leaderboards)
- Quick communication systems (chat, pings, emotes)

📱 **Social Media Perspective**: What makes platforms engaging for teams?
- Activity feeds showing team progress
- @mentions and notifications for collaboration
- Easy sharing and commenting on work
- Visual progress indicators (stories, timelines)

🏭 **Manufacturing Perspective**: How do efficient factories manage workflow?
- Kanban boards for visual workflow management
- Just-in-time task assignment
- Bottleneck identification and resolution
- Quality checkpoints and approvals

Which analogies spark interesting feature ideas for your platform?
```

### Step 3: Feature Ideation

**Your Response**:
```
The gaming analogy is really interesting! I like the idea of:
- Real-time team presence (who's working on what)
- Progress visualization like game achievements
- Quick team communication without leaving the task view

From manufacturing, the bottleneck identification could be huge for small teams.
```

**AI Response**:
```
🎯 Excellent connections! Let's develop these ideas further:

**Real-Time Team Presence**:
- Live cursors showing who's viewing/editing tasks
- Status indicators: "In Progress", "Blocked", "Reviewing"
- Team activity feed with real-time updates
- "Focus mode" indicator when someone needs uninterrupted time

**Gamified Progress Visualization**:
- Team velocity tracking (tasks completed per sprint)
- Individual and team achievement badges
- Progress bars for projects with milestone celebrations
- "Streak" counters for consistent daily progress

**Integrated Communication**:
- Task-specific comment threads
- Quick emoji reactions for feedback
- @mention system with smart notifications
- Voice notes for complex explanations

**Bottleneck Detection**:
- Automatic identification of overloaded team members
- Task dependency mapping with critical path highlighting
- Workload balancing suggestions
- "Blocked task" alerts with suggested solutions

Let's also explore the "simplicity" angle - what would make this tool feel effortless for small teams?
```

### Step 4: Simplicity Focus

**Your Response**:
```
For simplicity:
- One-click project setup with smart templates
- Drag-and-drop task organization
- Automatic time tracking without manual input
- Smart task prioritization based on deadlines and dependencies
- Integration with tools they already use (Slack, Google Workspace, GitHub)
```

**AI Response**:
```
💡 Brilliant! You're thinking like a product designer. Let's synthesize our brainstorming:

**Core Value Proposition**: 
"The only task management tool small teams need - combines the simplicity of a sticky note with the power of enterprise project management"

**Key Differentiators**:
1. **Effortless Setup**: Smart templates + one-click project creation
2. **Real-Time Collaboration**: Live presence + integrated communication
3. **Intelligent Automation**: Auto-prioritization + bottleneck detection
4. **Seamless Integration**: Works with existing tools, not against them
5. **Gamified Progress**: Makes productivity visible and rewarding

**Target User Insight**: 
Small teams (3-15 people) who need enterprise-level coordination without enterprise-level complexity.

Ready to move to Phase 2: Modeling? We'll create a comprehensive PRD based on these insights!
```

## 📋 Phase 2: Modeling - PRD Creation (45 minutes)

### Step 5: Start PRD Creation

```
Prompt: Let's create a comprehensive PRD for TeamTask Pro based on our brainstorming insights.
```

**AI Response**:
```
📋 Perfect! I'll create a comprehensive PRD using our interactive template.

[Calls jaegis_create_prd action with template_type: "comprehensive"]

✅ PRD creation started! Let's begin with the Executive Summary.

**Section 1: Executive Summary**

Based on our brainstorming, here's what I understand:

**Problem Statement**: Small teams (3-15 people) struggle with task management tools that are either too simple (lacking collaboration features) or too complex (requiring extensive setup and training).

**Solution Overview**: TeamTask Pro combines effortless simplicity with powerful collaboration features, providing real-time team coordination, intelligent automation, and seamless integration with existing workflows.

**Target Market**: Small to medium businesses, startups, creative agencies, and remote teams who need enterprise-level coordination without enterprise-level complexity.

Let's refine this executive summary. What's the most important problem we're solving?
```

### Step 6: Refine Executive Summary

**Your Response**:
```
The most important problem is that small teams waste time on task management overhead instead of actual work. They either use tools that don't scale with their growth or enterprise tools that slow them down with unnecessary complexity.
```

**AI Response**:
```
🎯 Perfect! That's a much sharper problem statement. Let me update the executive summary:

**Executive Summary - Refined**

**Problem**: Small teams waste 20-30% of their productive time on task management overhead - either struggling with tools that don't scale or being slowed down by enterprise solutions designed for large organizations.

**Solution**: TeamTask Pro eliminates task management overhead through intelligent automation, real-time collaboration, and effortless simplicity. Teams can focus on work, not workflow management.

**Market Opportunity**: 50M+ small teams globally spend $2B+ annually on productivity tools that don't fit their needs.

**Success Metrics**: 
- Reduce time spent on task management by 50%
- Increase team productivity visibility by 80%
- Achieve 90%+ user satisfaction within first month

**Section 2: User Personas**

Let's define our primary users. Based on our discussion, I see three key personas:

👤 **"Startup Founder Sarah"** - Needs visibility into team progress without micromanaging
👤 **"Team Lead Tom"** - Manages 5-8 people across multiple projects
👤 **"Remote Worker Rachel"** - Needs clear communication and task clarity

Which persona should we develop first?
```

### Step 7: Develop User Personas

**Your Response**:
```
Let's start with Team Lead Tom since he's probably our primary user - the person who would evaluate and purchase the tool.
```

**AI Response**:
```
👤 **Primary Persona: "Team Lead Tom"**

**Demographics**:
- Age: 28-40
- Role: Team Lead, Project Manager, or Department Head
- Team Size: 5-12 people
- Industry: Tech, Marketing, Design, Consulting
- Experience: 3-8 years in leadership roles

**Goals**:
- Keep projects on track without constant check-ins
- Identify and resolve bottlenecks quickly
- Maintain team morale and productivity
- Provide clear progress updates to stakeholders
- Balance multiple projects simultaneously

**Pain Points**:
- Spends 2+ hours daily on status updates and coordination
- Struggles to see real-time team workload distribution
- Difficult to identify blocked or struggling team members
- Tools either too simple (spreadsheets) or too complex (enterprise PM)
- Context switching between multiple tools and platforms

**Motivations**:
- Team success and recognition
- Efficient, streamlined processes
- Clear communication and transparency
- Professional growth and leadership development

**Technology Comfort**: High - comfortable with SaaS tools, integrations, and new platforms

**Quote**: "I want to spend my time helping my team succeed, not managing tools and generating reports."

**Section 3: User Stories and Acceptance Criteria**

Let's create user stories for Team Lead Tom. What's his most critical workflow?
```

### Step 8: Define User Stories

**Your Response**:
```
Tom's most critical workflow is probably the daily/weekly team check-in where he needs to:
1. See what everyone is working on
2. Identify any blockers or issues
3. Redistribute work if someone is overloaded
4. Update stakeholders on progress
```

**AI Response**:
```
📝 **Epic: Daily Team Coordination**

**User Story 1: Real-Time Team Overview**
*As Team Lead Tom, I want to see real-time team activity and task status so that I can quickly assess team progress without interrupting individual work.*

**Acceptance Criteria**:
- [ ] Dashboard shows all team members and their current tasks
- [ ] Live status indicators (working, blocked, reviewing, available)
- [ ] Visual workload distribution across team members
- [ ] One-click drill-down into individual task details
- [ ] Updates in real-time without page refresh
- [ ] Mobile-responsive for on-the-go checking

**User Story 2: Bottleneck Detection**
*As Team Lead Tom, I want to automatically identify workflow bottlenecks so that I can proactively resolve issues before they impact deadlines.*

**Acceptance Criteria**:
- [ ] Automatic detection of overloaded team members
- [ ] Identification of tasks blocked for >24 hours
- [ ] Critical path analysis for project dependencies
- [ ] Suggested actions for resolving bottlenecks
- [ ] Notification system for urgent issues
- [ ] Historical bottleneck patterns and trends

**User Story 3: Effortless Progress Reporting**
*As Team Lead Tom, I want to generate stakeholder updates automatically so that I can focus on team leadership instead of report creation.*

**Acceptance Criteria**:
- [ ] One-click progress report generation
- [ ] Customizable report templates for different stakeholders
- [ ] Automatic inclusion of key metrics and milestones
- [ ] Visual progress charts and timeline updates
- [ ] Export options (PDF, email, Slack integration)
- [ ] Scheduled automatic report delivery

Should we continue with more user stories or move to functional requirements?
```

### Step 9: Complete Functional Requirements

**Your Response**:
```
Let's move to functional requirements. I think we have a good foundation with these user stories.
```

**AI Response**:
```
⚙️ **Section 4: Functional Requirements**

**Core Task Management**:
- [ ] Create, edit, delete, and organize tasks
- [ ] Drag-and-drop task prioritization and status changes
- [ ] Task dependencies and relationship mapping
- [ ] Subtask creation and hierarchical organization
- [ ] Due dates, time estimates, and automatic scheduling
- [ ] Task templates for recurring workflows
- [ ] Bulk task operations (assign, update, delete)

**Real-Time Collaboration**:
- [ ] Live presence indicators for team members
- [ ] Real-time task updates and notifications
- [ ] Task-specific comment threads and discussions
- [ ] @mention system with smart notifications
- [ ] File attachments and document sharing
- [ ] Activity feed with team progress updates
- [ ] Quick emoji reactions and feedback

**Intelligent Automation**:
- [ ] Automatic task prioritization based on deadlines and dependencies
- [ ] Smart workload balancing suggestions
- [ ] Bottleneck detection and resolution recommendations
- [ ] Automated progress tracking and reporting
- [ ] Smart notification filtering to reduce noise
- [ ] Predictive deadline alerts and risk assessment

**Integration & Workflow**:
- [ ] Single sign-on (SSO) with Google Workspace, Microsoft 365
- [ ] Slack, Microsoft Teams, and Discord integrations
- [ ] GitHub, GitLab, and Bitbucket project linking
- [ ] Calendar integration (Google Calendar, Outlook)
- [ ] Time tracking integration (Toggl, Harvest)
- [ ] API for custom integrations and automation

**Reporting & Analytics**:
- [ ] Team velocity and productivity metrics
- [ ] Project progress and milestone tracking
- [ ] Individual and team performance insights
- [ ] Customizable dashboards and reports
- [ ] Export capabilities (CSV, PDF, API)
- [ ] Historical data analysis and trends

Ready for Section 5: Technical Requirements?
```

## 🏗️ Phase 3: Architecture Design (45 minutes)

### Step 10: Technical Requirements

**Your Response**:
```
Yes, let's move to technical requirements. What do we need to consider for a real-time collaborative platform?
```

**AI Response**:
```
🏗️ Let's design the technical architecture for TeamTask Pro.

[Calls jaegis_design_architecture action]

**Section 5: Technical Requirements**

**Performance Requirements**:
- [ ] Page load time: <2 seconds for dashboard
- [ ] Real-time updates: <100ms latency for live features
- [ ] Support for 100+ concurrent users per team
- [ ] 99.9% uptime SLA (8.76 hours downtime/year max)
- [ ] Mobile responsiveness across all devices
- [ ] Offline capability for core task viewing/editing

**Scalability Requirements**:
- [ ] Support teams from 3 to 50 members
- [ ] Handle 10,000+ tasks per team
- [ ] Scale to 100,000+ registered users
- [ ] Auto-scaling infrastructure for traffic spikes
- [ ] Database performance optimization for large datasets

**Security Requirements**:
- [ ] SOC 2 Type II compliance
- [ ] End-to-end encryption for sensitive data
- [ ] Role-based access control (RBAC)
- [ ] Multi-factor authentication (MFA)
- [ ] Regular security audits and penetration testing
- [ ] GDPR and CCPA compliance for data privacy

**Integration Requirements**:
- [ ] RESTful API with rate limiting
- [ ] Webhook support for real-time integrations
- [ ] OAuth 2.0 for third-party authentication
- [ ] GraphQL endpoint for efficient data fetching
- [ ] WebSocket connections for real-time features

**Recommended Architecture: Microservices with Event-Driven Design**

🏗️ **System Components**:

**Frontend Layer**:
- **Technology**: React with TypeScript
- **State Management**: Redux Toolkit + RTK Query
- **Real-time**: Socket.io client
- **UI Framework**: Tailwind CSS + Headless UI
- **Mobile**: Progressive Web App (PWA)

**API Gateway**:
- **Technology**: Kong or AWS API Gateway
- **Features**: Rate limiting, authentication, routing
- **Load Balancing**: Round-robin with health checks

**Core Services**:
1. **User Service**: Authentication, profiles, team management
2. **Task Service**: Task CRUD, dependencies, scheduling
3. **Collaboration Service**: Comments, mentions, real-time updates
4. **Notification Service**: Email, push, in-app notifications
5. **Analytics Service**: Metrics, reporting, insights
6. **Integration Service**: Third-party API connections

**Data Layer**:
- **Primary Database**: PostgreSQL for relational data
- **Cache**: Redis for session management and real-time data
- **Search**: Elasticsearch for task search and analytics
- **File Storage**: AWS S3 for attachments and documents

**Infrastructure**:
- **Container Orchestration**: Kubernetes on AWS EKS
- **Message Queue**: Apache Kafka for event streaming
- **Monitoring**: Prometheus + Grafana + ELK stack
- **CI/CD**: GitHub Actions with automated testing

What's your team's experience with these technologies?
```

### Step 11: Technology Selection

**Your Response**:
```
Our team has strong experience with React and Node.js, moderate experience with PostgreSQL and Redis, but limited experience with Kubernetes and Kafka. Can we simplify the architecture for our initial MVP?
```

**AI Response**:
```
🎯 Absolutely! Let's design an MVP-friendly architecture that can scale:

**Simplified MVP Architecture**

**Frontend**:
- **React + TypeScript**: Leverage your team's strengths
- **Vite**: Fast development and building
- **TanStack Query**: Simpler than Redux for data fetching
- **Socket.io**: Real-time features without complexity
- **Tailwind CSS**: Rapid UI development

**Backend**:
- **Node.js + Express**: Familiar technology stack
- **TypeScript**: Type safety across the stack
- **Socket.io**: Real-time WebSocket handling
- **JWT**: Simple authentication to start

**Database**:
- **PostgreSQL**: Single database for simplicity
- **Redis**: Session storage and real-time data cache
- **Prisma ORM**: Type-safe database access

**Infrastructure (MVP)**:
- **Vercel**: Frontend deployment (zero config)
- **Railway/Render**: Backend deployment (simple scaling)
- **Supabase**: Managed PostgreSQL + Redis
- **GitHub Actions**: Simple CI/CD pipeline

**Growth Path**:
```
MVP → Scale → Enterprise
├── Monolith → Microservices → Distributed
├── Single DB → Read Replicas → Sharding
├── Simple Hosting → Container → Kubernetes
└── Basic Monitoring → APM → Full Observability
```

**MVP Development Timeline**:
- **Week 1-2**: Core task management (CRUD operations)
- **Week 3-4**: Real-time collaboration features
- **Week 5-6**: User authentication and team management
- **Week 7-8**: Basic integrations and notifications
- **Week 9-10**: Polish, testing, and deployment

Ready for Phase 4: Development planning?
```

## 💻 Phase 4: Development Planning (30 minutes)

### Step 12: Development Roadmap

**Your Response**:
```
Perfect! Let's create the development plan. What should we build first?
```

**AI Response**:
```
💻 **Development Roadmap: TeamTask Pro MVP**

**Sprint 1 (Weeks 1-2): Foundation & Core Tasks**

**Goals**: Basic task management functionality
**User Story**: "As a user, I can create, edit, and organize tasks"

**Backend Tasks**:
- [ ] Set up Node.js + Express + TypeScript project
- [ ] Configure PostgreSQL database with Prisma
- [ ] Implement User model and authentication (JWT)
- [ ] Create Task model with CRUD operations
- [ ] Set up basic API routes (/auth, /tasks)
- [ ] Add input validation and error handling

**Frontend Tasks**:
- [ ] Set up React + TypeScript + Vite project
- [ ] Configure Tailwind CSS and basic layout
- [ ] Create authentication pages (login, signup)
- [ ] Build task list component with CRUD operations
- [ ] Implement drag-and-drop task reordering
- [ ] Add basic routing and navigation

**Database Schema**:
```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'todo',
  priority INTEGER DEFAULT 0,
  due_date TIMESTAMP,
  assigned_to UUID REFERENCES users(id),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Sprint 2 (Weeks 3-4): Real-Time Collaboration**

**Goals**: Live updates and team collaboration
**User Story**: "As a team member, I can see real-time updates and collaborate on tasks"

**Backend Tasks**:
- [ ] Integrate Socket.io for real-time communication
- [ ] Implement team management (create, join, invite)
- [ ] Add task comments and mentions system
- [ ] Create activity feed and notifications
- [ ] Set up Redis for session management
- [ ] Add real-time presence indicators

**Frontend Tasks**:
- [ ] Integrate Socket.io client for real-time updates
- [ ] Build team dashboard with live task updates
- [ ] Create comment system with @mentions
- [ ] Add presence indicators (who's online/working)
- [ ] Implement activity feed component
- [ ] Add notification system (in-app alerts)

Want me to continue with Sprints 3-5, or should we dive deeper into Sprint 1 implementation?
```

### Step 13: Sprint 1 Implementation Details

**Your Response**:
```
Let's dive deeper into Sprint 1. Can you provide the actual code structure and key files we need to create?
```

**AI Response**:
```
🛠️ **Sprint 1: Detailed Implementation Guide**

**Project Structure**:
```
teamtask-pro/
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   │   ├── authController.ts
│   │   │   └── taskController.ts
│   │   ├── middleware/
│   │   │   ├── auth.ts
│   │   │   └── validation.ts
│   │   ├── models/
│   │   │   └── index.ts
│   │   ├── routes/
│   │   │   ├── auth.ts
│   │   │   └── tasks.ts
│   │   ├── utils/
│   │   │   └── jwt.ts
│   │   └── app.ts
│   ├── prisma/
│   │   └── schema.prisma
│   ├── package.json
│   └── tsconfig.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   ├── tasks/
│   │   │   └── layout/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

**Key Backend Files**:

**1. prisma/schema.prisma**:
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  avatarUrl String?  @map("avatar_url")
  createdAt DateTime @default(now()) @map("created_at")
  
  createdTasks Task[] @relation("TaskCreator")
  assignedTasks Task[] @relation("TaskAssignee")
  
  @@map("users")
}

model Task {
  id          String    @id @default(cuid())
  title       String
  description String?
  status      String    @default("todo")
  priority    Int       @default(0)
  dueDate     DateTime? @map("due_date")
  createdAt   DateTime  @default(now()) @map("created_at")
  updatedAt   DateTime  @updatedAt @map("updated_at")
  
  createdBy   String    @map("created_by")
  creator     User      @relation("TaskCreator", fields: [createdBy], references: [id])
  
  assignedTo  String?   @map("assigned_to")
  assignee    User?     @relation("TaskAssignee", fields: [assignedTo], references: [id])
  
  @@map("tasks")
}
```

**2. src/controllers/taskController.ts**:
```typescript
import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const getTasks = async (req: Request, res: Response) => {
  try {
    const tasks = await prisma.task.findMany({
      include: {
        creator: { select: { id: true, name: true, email: true } },
        assignee: { select: { id: true, name: true, email: true } }
      },
      orderBy: [
        { priority: 'desc' },
        { createdAt: 'desc' }
      ]
    });
    
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch tasks' });
  }
};

export const createTask = async (req: Request, res: Response) => {
  try {
    const { title, description, priority, dueDate, assignedTo } = req.body;
    const createdBy = req.user.id; // From auth middleware
    
    const task = await prisma.task.create({
      data: {
        title,
        description,
        priority: priority || 0,
        dueDate: dueDate ? new Date(dueDate) : null,
        createdBy,
        assignedTo: assignedTo || null
      },
      include: {
        creator: { select: { id: true, name: true, email: true } },
        assignee: { select: { id: true, name: true, email: true } }
      }
    });
    
    res.status(201).json(task);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create task' });
  }
};

export const updateTask = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    
    const task = await prisma.task.update({
      where: { id },
      data: {
        ...updates,
        updatedAt: new Date()
      },
      include: {
        creator: { select: { id: true, name: true, email: true } },
        assignee: { select: { id: true, name: true, email: true } }
      }
    });
    
    res.json(task);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update task' });
  }
};
```

**Key Frontend Files**:

**1. src/components/tasks/TaskList.tsx**:
```typescript
import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { Task } from '../../types';
import TaskCard from './TaskCard';
import { useTasks } from '../../hooks/useTasks';

const TaskList: React.FC = () => {
  const { tasks, updateTask, loading, error } = useTasks();
  
  const handleDragEnd = (result: any) => {
    if (!result.destination) return;
    
    const { source, destination, draggableId } = result;
    
    // Update task status based on column
    const newStatus = destination.droppableId;
    updateTask(draggableId, { status: newStatus });
  };
  
  const columns = {
    todo: tasks.filter(task => task.status === 'todo'),
    inProgress: tasks.filter(task => task.status === 'in_progress'),
    done: tasks.filter(task => task.status === 'done')
  };
  
  if (loading) return <div>Loading tasks...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="grid grid-cols-3 gap-6">
        {Object.entries(columns).map(([columnId, columnTasks]) => (
          <div key={columnId} className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-semibold mb-4 capitalize">
              {columnId.replace(/([A-Z])/g, ' $1')}
            </h3>
            
            <Droppable droppableId={columnId}>
              {(provided) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className="space-y-3"
                >
                  {columnTasks.map((task, index) => (
                    <Draggable
                      key={task.id}
                      draggableId={task.id}
                      index={index}
                    >
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                        >
                          <TaskCard task={task} />
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </div>
        ))}
      </div>
    </DragDropContext>
  );
};

export default TaskList;
```

**Next Steps for Sprint 1**:
1. Set up the project structure
2. Configure database and authentication
3. Implement basic CRUD operations
4. Build the drag-and-drop interface
5. Add form validation and error handling
6. Write unit tests for core functionality

Ready to move to Sprint 2 planning, or would you like more implementation details for any specific component?
```

## 🎯 Tutorial Summary

### What We Accomplished

In this tutorial, we used the JAEGIS method to:

1. **🧠 Brainstormed** a comprehensive task management solution using psychology-backed techniques
2. **📋 Created** a detailed PRD with user personas, stories, and requirements
3. **🏗️ Designed** a scalable technical architecture adapted to team capabilities
4. **💻 Planned** a practical development roadmap with detailed implementation guidance

### Key Takeaways

1. **Collaborative Process**: JAEGIS keeps you engaged throughout, ensuring the final product reflects your vision
2. **Research-Backed Methods**: The brainstorming techniques revealed insights we might have missed
3. **Adaptive Architecture**: The AI helped us balance ideal architecture with practical constraints
4. **Actionable Output**: We ended with concrete code examples and implementation steps

### Next Steps

1. **Implement Sprint 1**: Follow the detailed code examples provided
2. **Iterate and Refine**: Use JAEGIS to plan subsequent sprints
3. **Scale the Architecture**: Revisit the technical design as your team grows
4. **Expand Features**: Use the brainstorming techniques to explore new capabilities

### Resources

- **Complete Code Repository**: [github.com/jaegis-method/teamtask-pro-tutorial](https://github.com/jaegis-method/teamtask-pro-tutorial)
- **Live Demo**: [teamtask-pro-demo.jaegis-method.com](https://teamtask-pro-demo.jaegis-method.com)
- **Community Discussion**: [Discord #web-app-tutorial](https://discord.gg/jaegis-method)

---

**Congratulations!** You've completed your first JAEGIS web application project. The methodology guided you from initial idea to implementation-ready code, ensuring nothing important was overlooked.

**Ready for more?** Try the [Mobile App Tutorial](./mobile-app-tutorial.md) or [Game Development Tutorial](./game-dev-tutorial.md) to see how JAEGIS adapts to different project types!
