from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from .tools.reminder_tools import ReminderTools
from ...utils import get_logger
import yaml

logger = get_logger(__name__)

with open("application.yaml", "r") as f:
    config = yaml.safe_load(f)

reminder_tools = ReminderTools()

add_reminder_tool = FunctionTool(func=reminder_tools.add_reminder)
list_reminders_tool = FunctionTool(func=reminder_tools.list_reminders)
get_reminder_tool = FunctionTool(func=reminder_tools.get_reminder)
update_reminder_tool = FunctionTool(func=reminder_tools.update_reminder)
delete_reminder_tool = FunctionTool(func=reminder_tools.delete_reminder)
search_reminders_tool = FunctionTool(func=reminder_tools.search_reminders)

reminder_agent = Agent(
    name="reminder_agent",
    model=config.get("model", "gemini-2.0-flash"),
    description="Notifies you at a specific time",
    instruction="""
    You are a Reminder Agent. Your job is to manage user reminders, which are always time-based.
    You can perform the following operations on reminders:
    - Add a new reminder using `add_reminder_tool`.
    - List all active reminders using `list_reminders_tool`.
    - Get a specific reminder by ID using `get_reminder_tool`.
    - Update an existing reminder using `update_reminder_tool`.
    - Delete (deactivate) a reminder using `delete_reminder_tool`.
    - Search reminders by title or description using `search_reminders_tool`.
    Reminders are nudges or alerts for specific times.
    They can be recurring.
    Example: "Take medicine at 8 PM"
    If the user asks about todos or tasks, escalate to the root agent by responding with: "ESCALATE_TO_ROOT: This is a todo/task request..."
    If the request is outside of your domain, escalate to the root agent by responding with: "ESCALATE_TO_ROOT: This request is outside my reminder domain..."
    """,
    tools=[
        add_reminder_tool,
        list_reminders_tool,
        get_reminder_tool,
        update_reminder_tool,
        delete_reminder_tool,
        search_reminders_tool
    ]
)
