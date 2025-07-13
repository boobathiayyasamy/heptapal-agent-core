from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from .tools.todo_tools import TodoTools
from ...utils import get_logger
import yaml

logger = get_logger(__name__)

with open("application.yaml", "r") as f:
    config = yaml.safe_load(f)

todo_tools = TodoTools(config)

add_todo_tool = FunctionTool(func=todo_tools.add_todo)
list_todos_tool = FunctionTool(func=todo_tools.list_todos)
get_todo_tool = FunctionTool(func=todo_tools.get_todo)
update_todo_tool = FunctionTool(func=todo_tools.update_todo)
delete_todo_tool = FunctionTool(func=todo_tools.delete_todo)
search_todos_tool = FunctionTool(func=todo_tools.search_todos)
get_todo_statistics_tool = FunctionTool(func=todo_tools.get_todo_statistics)

todo_agent = Agent(
    name="todo_agent",
    model=config.get("model", "gemini-2.0-flash"),
    description="Keeps track of tasks you want to complete",
    instruction="""
    You are a Todo Agent. Your job is to manage user todo lists and tasks.
    You can perform the following operations on todo items:
    - Add a new todo item using `add_todo_tool`.
    - List todo items with optional filtering using `list_todos_tool`.
    - Get a specific todo item by ID using `get_todo_tool`.
    - Update an existing todo item using `update_todo_tool`.
    - Delete a todo item permanently using `delete_todo_tool`.
    - Search todo items by title or description using `search_todos_tool`.
    - Get statistics about todo items using `get_todo_statistics_tool`.
    Todos are optional, may or may not have a deadline, and require action (e.g., mark as complete).
    They can be recurring, but not always.
    Example: "Buy groceries this weekend"

    When adding a todo, if the title is not explicitly provided, generate it from the first few words of the description.
    If the priority is not specified, use the default priority configured in application.yaml.
    If the description is missing, you must ask the user for a detailed description before proceeding.
    If the due date is ambiguous or missing for a time-sensitive task, ask for clarification.

    If the user asks about reminders or alerts, escalate to the root agent by responding with: "ESCALATE_TO_ROOT: This is a reminder/alert request..."
    If the request is outside of your domain, escalate to the root agent by responding with: "ESCALATE_TO_ROOT: This request is outside my todo domain..."
    """,
    tools=[
        add_todo_tool,
        list_todos_tool,
        get_todo_tool,
        update_todo_tool,
        delete_todo_tool,
        search_todos_tool,
        get_todo_statistics_tool
    ]
)
