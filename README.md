# Personal AI Assistant with Google ADK

A comprehensive Personal AI Assistant built with Google Agent Development Kit (ADK) that uses a multi-agent architecture to handle reminders and todo lists efficiently with MySQL database persistence.

## 🏗️ Architecture

The system implements a **multi-agent architecture** with specialized agents and **MySQL database persistence**:

### Root Agent
- **Purpose**: Delegates tasks to appropriate sub-agents based on user requests
- **Model**: `gemini-2.0-flash`
- **Capabilities**: 
  - Understands user intent (reminder vs todo)
  - Routes requests to specialized sub-agents
  - Provides unified interface for the assistant

### Reminder Agent
- **Purpose**: Manages reminders and alerts
- **Model**: `gemini-2.0-flash`
- **Tools**:
  - `add_reminder`: Create new reminders with title, description, and time
  - `list_reminders`: View all active reminders
  - `get_reminder`: Get specific reminder details
  - `update_reminder`: Modify existing reminders
  - `delete_reminder`: Remove reminders
  - `search_reminders`: Find reminders by content

### Todo Agent
- **Purpose**: Manages todo lists and tasks
- **Model**: `gemini-2.0-flash`
- **Tools**:
  - `add_todo`: Create new todo items with priority and due dates
  - `list_todos`: View todos with filtering options
  - `get_todo`: Get specific todo details
  - `update_todo`: Modify existing todos
  - `delete_todo`: Remove todos
  - `search_todos`: Find todos by content
  - `get_todo_statistics`: View todo analytics

### Database Layer
- **Purpose**: Persistent storage for reminders and todos
- **Technology**: MySQL with SQLAlchemy ORM
- **Features**:
  - Connection pooling and management
  - Repository pattern for data access
  - Single Responsibility Principle design
  - Comprehensive error handling

## 🚀 Features

### Reminder Management
- ✅ Add reminders with titles, descriptions, and remind times
- ✅ List all active reminders with formatted output
- ✅ Search reminders by content
- ✅ Update and delete reminders
- ✅ Rich console output with emojis and formatting
- ✅ **Persistent storage in MySQL database**

### Todo Management
- ✅ Add todo items with priorities (low, medium, high)
- ✅ Set due dates for tasks
- ✅ Track task status (pending, in_progress, completed)
- ✅ Filter todos by status and priority
- ✅ Complete task analytics and statistics
- ✅ Rich console output with priority indicators
- ✅ **Persistent storage in MySQL database**

### Agent Delegation
- ✅ Intelligent request routing based on user intent
- ✅ Seamless integration between agents
- ✅ Error handling and graceful fallbacks

### Database Features
- ✅ **MySQL database persistence**
- ✅ **Connection pooling** for performance
- ✅ **Repository pattern** for clean data access
- ✅ **Automatic table creation** and schema management
- ✅ **Comprehensive error handling** and logging
- ✅ **Search and filtering** capabilities

## 📦 Installation

1. **Install Google ADK**:
   ```bash
   uv add google-adk
   ```

2. **Clone/Download the project**:
   ```bash
   # If you have the project in a directory
   cd heptapal-agent-core
   ```

3. **Install dependencies**:
   ```bash
   uv add mysql-connector-python sqlalchemy
   ```

4. **Database Setup**:
   ```bash
   # Create database and tables
   mysql -h 192.168.0.111 -u admin -p < database_schema.sql
   
   # Initialize database (optional - tables will be created automatically)
   python -m db.init_db
   ```

## 🎯 Usage

### Running the Demo

To see the system in action, run the comprehensive demo:

```bash
python demo_assistant.py
```

This will demonstrate:
- Adding sample reminders and todos
- All available operations
- Agent delegation functionality
- Rich console output with formatting
- **Database persistence**

### Testing Database Functionality

Run the database test script to verify everything is working:

```bash
python test_database.py
```

This will test:
- Database connection
- Reminder operations (CRUD)
- Todo operations (CRUD)
- Search and filtering
- Statistics functionality

### Using with ADK CLI

1. **Interactive mode**:
   ```bash
   adk run .
   ```

2. **Web interface**:
   ```bash
   adk web
   ```

### Example Interactions

#### Reminder Examples
```
User: "Remind me to call John tomorrow at 3 PM"
Assistant: Uses delegate_to_reminder_agent → Creates reminder in database

User: "Show me all my reminders"
Assistant: Uses reminder agent → Lists all active reminders from database

User: "Find reminders about doctor"
Assistant: Uses search_reminders → Shows matching reminders from database
```

#### Todo Examples
```
User: "Add buy groceries to my todo list with high priority"
Assistant: Uses delegate_to_todo_agent → Creates high priority todo in database

User: "Show me all my pending tasks"
Assistant: Uses list_todos with status filter → Shows pending items from database

User: "Mark task 3 as completed"
Assistant: Uses update_todo → Marks task as completed in database
```

## 📊 Data Structures

### Reminder Structure
```python
{
    "id": 1,
    "title": "Doctor Appointment",
    "description": "Annual health checkup with Dr. Smith",
    "remind_time": "2024-12-20 10:00",
    "created_at": "2024-12-15 14:30:00",
    "is_active": true
}
```

### Todo Structure
```python
{
    "id": 1,
    "title": "Complete Project Report",
    "description": "Finish the Q4 project report for presentation",
    "priority": "high",           # low, medium, high
    "status": "pending",          # pending, in_progress, completed
    "due_date": "2024-12-20",
    "created_at": "2024-12-15 14:30:00",
    "completed_at": null
}
```

## 🛠️ Technical Implementation

### Framework
- **Google ADK**: Agent Development Kit for multi-agent systems
- **Python 3.12+**: Modern Python with type hints
- **MySQL Database**: Persistent storage with SQLAlchemy ORM
- **SQLAlchemy**: Database ORM with connection pooling

### Key Components

1. **Agent Classes**: Each agent extends ADK's `Agent` class
2. **Function Tools**: Custom Python functions wrapped as ADK tools
3. **Database Layer**: 
   - `DatabaseConnection`: Connection management and pooling
   - `ReminderRepository` & `TodoRepository`: Data access layer
   - SQLAlchemy models with proper indexing
4. **Type Safety**: Full type annotations for reliable operations
5. **Error Handling**: Comprehensive error handling with user-friendly messages
6. **Rich Output**: Formatted console output with emojis and visual indicators

### File Structure
```
heptapal-agent-core/
├── db/                          # Database package
│   ├── __init__.py             # Package initialization
│   ├── connection.py           # Database connection management
│   ├── models.py               # SQLAlchemy models
│   ├── repositories.py         # Data access repositories
│   └── init_db.py              # Database initialization
├── root_agent/
│   ├── agent.py                # Root agent with delegation logic
│   ├── __init__.py             # Package initialization
│   └── sub_agents/
│       ├── __init__.py         # Sub-agents package
│       ├── reminder_agent/
│       │   ├── agent.py        # Reminder agent + tools
│       │   ├── __init__.py     # Package initialization
│       │   └── tools/
│       │       ├── __init__.py # Tools package
│       │       └── reminder_tools.py # Reminder tools with DB
│       └── todo_agent/
│           ├── agent.py        # Todo agent + tools
│           ├── __init__.py     # Package initialization
│           └── tools/
│               ├── __init__.py # Tools package
│               └── todo_tools.py # Todo tools with DB
├── application.yaml            # Configuration including DB settings
├── database_schema.sql         # Database schema script
├── test_database.py            # Database functionality test
├── demo_assistant.py           # Comprehensive demo script
├── pyproject.toml             # Project configuration
├── DATABASE_SETUP.md          # Database setup guide
└── README.md                  # This documentation
```

## 🎨 Console Output Examples

### Reminder Output
```
[REMINDER AGENT] ✅ Reminder Added Successfully!
  ID: 1
  Title: Doctor Appointment
  Description: Annual health checkup with Dr. Smith
  Remind Time: 2024-12-20 10:00
  Created At: 2024-12-15 14:30:00
--------------------------------------------------
```

### Todo Output
```
[TODO AGENT] ✅ Todo Item Added Successfully!
  ID: 1
  Title: Complete Project Report
  Description: Finish the Q4 project report for presentation
  Priority: HIGH
  Status: PENDING
  Due Date: 2024-12-20
  Created At: 2024-12-15 14:30:00
--------------------------------------------------
```

### Todo List Display
```
[TODO AGENT] 📋 Todo List (3 items):
============================================================
  [1] 🔄 🔴 Complete Project Report
      Description: Finish the Q4 project report for presentation
      Priority: HIGH
      Status: IN_PROGRESS
      Due Date: 2024-12-20
      Created: 2024-12-15 14:30:00
  [2] ⏳ 🟡 Buy Christmas Gifts
      Description: Shop for Christmas presents for family
      Priority: MEDIUM
      Status: PENDING
      Due Date: 2024-12-23
      Created: 2024-12-15 14:31:00
```

## 🔧 Extending the System

### Adding New Agents
1. Create a new agent directory under `root_agent/sub_agents/`
2. Implement the agent class with ADK's `Agent`
3. Add custom tools using `FunctionTool`
4. Update root agent delegation logic

### Adding New Tools
```