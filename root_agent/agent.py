from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from .sub_agents.reminder_agent.tools.reminder_tools import ReminderTools
from .sub_agents.todo_agent.tools.todo_tools import TodoTools
from .utils import get_logger
import yaml

logger = get_logger(__name__)

with open("application.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialize tools
reminder_tools = ReminderTools(config)
todo_tools = TodoTools(config)

# Create FunctionTools for all operations
# Reminder tools
add_reminder_tool = FunctionTool(func=reminder_tools.add_reminder)
list_reminders_tool = FunctionTool(func=reminder_tools.list_reminders)
get_reminder_tool = FunctionTool(func=reminder_tools.get_reminder)
update_reminder_tool = FunctionTool(func=reminder_tools.update_reminder)
delete_reminder_tool = FunctionTool(func=reminder_tools.delete_reminder)
search_reminders_tool = FunctionTool(func=reminder_tools.search_reminders)

# Todo tools
add_todo_tool = FunctionTool(func=todo_tools.add_todo)
list_todos_tool = FunctionTool(func=todo_tools.list_todos)
get_todo_tool = FunctionTool(func=todo_tools.get_todo)
update_todo_tool = FunctionTool(func=todo_tools.update_todo)
delete_todo_tool = FunctionTool(func=todo_tools.delete_todo)
search_todos_tool = FunctionTool(func=todo_tools.search_todos)
get_todo_statistics_tool = FunctionTool(func=todo_tools.get_todo_statistics)

root_agent = Agent(
    name="root_agent",
    model=config.get("model", "gemini-2.0-flash"),
    description="Intelligent delegation agent that routes user requests to specialized sub-agents",
    instruction="""
    You are a root delegation agent that intelligently routes user requests to the appropriate specialized tools.
    Your main task is to analyze the user's request and use the correct tools.
    
    **Tool Selection Rules:**
    - For reminder-related tasks (alerts, notifications, time-based reminders), use reminder tools:
      * add_reminder_tool: Create new reminders
      * list_reminders_tool: Show all active reminders
      * get_reminder_tool: Get specific reminder details
      * update_reminder_tool: Modify existing reminders
      * delete_reminder_tool: Remove reminders
      * search_reminders_tool: Find reminders by content
    
    - For todo-related tasks (tasks to complete, action items, project work), use todo tools:
      * add_todo_tool: Create new todo items
      * list_todos_tool: Show todos with optional filtering
      * get_todo_tool: Get specific todo details
      * update_todo_tool: Modify existing todos
      * delete_todo_tool: Remove todos
      * search_todos_tool: Find todos by content
      * get_todo_statistics_tool: View todo analytics
    
    **Examples:**
    - "Remind me to call John tomorrow at 3 PM" → add_reminder_tool
    - "List my reminders" → list_reminders_tool
    - "Add buy groceries to my todo list" → add_todo_tool
    - "Show my todos" → list_todos_tool
    - "Set an alert for my dentist appointment" → add_reminder_tool
    - "Create a high priority task for project deadline" → add_todo_tool
    
    **Handling:**
    - Always use the most appropriate tool for the request
    - If a request is ambiguous, ask for clarification
    - Provide clear responses about what action was taken
    """,
    tools=[
        # Reminder tools
        add_reminder_tool,
        list_reminders_tool,
        get_reminder_tool,
        update_reminder_tool,
        delete_reminder_tool,
        search_reminders_tool,
        # Todo tools
        add_todo_tool,
        list_todos_tool,
        get_todo_tool,
        update_todo_tool,
        delete_todo_tool,
        search_todos_tool,
        get_todo_statistics_tool
    ]
)
