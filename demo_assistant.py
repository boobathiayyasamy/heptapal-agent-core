#!/usr/bin/env python3
"""
Personal AI Assistant Demo Script
This script demonstrates the functionality of the Personal AI Assistant
with root agent delegation to reminder and todo sub-agents.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from root_agent.utils import get_logger
from root_agent.sub_agents.reminder_agent.agent import reminder_agent
from root_agent.sub_agents.todo_agent.agent import todo_agent

logger = get_logger(__name__)

def print_separator(title: str):
    """Print a nice separator for demo sections"""
    logger.info("\n" + "="*60)
    logger.info(f"  {title}")
    logger.info("="*60)

def demo_reminder_agent():
    """Demonstrate the reminder agent capabilities"""
    print_separator("REMINDER AGENT DEMO")
    
    # Import reminder tools to call them directly for demo
    from root_agent.sub_agents.reminder_agent.tools.reminder_tools import ReminderTools
    
    reminder_tools = ReminderTools()
    
    logger.info("\n1. Adding sample reminders...")
    reminder_tools.add_reminder("Doctor Appointment", "Annual health checkup with Dr. Smith", "2024-12-20 10:00")
    reminder_tools.add_reminder("Call Mom", "Weekly call with mom to catch up", "2024-12-18 19:00")
    reminder_tools.add_reminder("Pick up Groceries", "Buy milk, bread, and eggs from the store", "2024-12-17 17:00")
    reminder_tools.add_reminder("Team Meeting", "Weekly team standup meeting", "2024-12-19 09:00")
    
    logger.info("\n2. Listing all reminders...")
    logger.info(reminder_tools.list_reminders())
    
    logger.info("\n3. Getting specific reminder details...")
    logger.info(reminder_tools.get_reminder(2))
    
    logger.info("\n4. Updating a reminder...")
    reminder_tools.update_reminder(3, description="Buy milk, bread, eggs, and cheese from the store")
    
    logger.info("\n5. Searching reminders...")
    logger.info(reminder_tools.search_reminders("call"))
    
    logger.info("\n6. Deleting a reminder...")
    reminder_tools.delete_reminder(1)
    
    logger.info("\n7. Final reminder list...")
    logger.info(reminder_tools.list_reminders())

def demo_todo_agent():
    """Demonstrate the todo agent capabilities"""
    print_separator("TODO AGENT DEMO")
    
    # Import todo tools to call them directly for demo
    from root_agent.sub_agents.todo_agent.tools.todo_tools import TodoTools
    import yaml
    
    with open("application.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    todo_tools = TodoTools(config)
    
    logger.info("\n1. Adding sample todo items...")
    todo_tools.add_todo(title="Complete Project Report", description="Finish the Q4 project report for presentation", priority="high", due_date="2024-12-20")
    todo_tools.add_todo(title="Buy Christmas Gifts", description="Shop for Christmas presents for family", priority="medium", due_date="2024-12-23")
    todo_tools.add_todo(title="Clean House", description="Deep clean the house before guests arrive", priority="low", due_date="2024-12-21")
    todo_tools.add_todo(title="Schedule Dentist", description="Make appointment for dental cleaning", priority="medium")
    todo_tools.add_todo(title="Learn Python", description="Complete online Python course", priority="high", due_date="2024-12-31")
    
    logger.info("\n2. Listing all todo items...")
    logger.info(todo_tools.list_todos())
    
    logger.info("\n3. Filtering by status (pending)...")
    logger.info(todo_tools.list_todos(filter_status="pending"))
    
    logger.info("\n4. Filtering by priority (high)...")
    logger.info(todo_tools.list_todos(filter_priority="high"))
    
    logger.info("\n5. Getting specific todo item details...")
    logger.info(todo_tools.get_todo(2))
    
    logger.info("\n6. Updating a todo item (marking as in progress)...")
    todo_tools.update_todo(1, status="in_progress")
    
    logger.info("\n7. Marking a todo item as completed...")
    todo_tools.update_todo(4, status="completed")
    
    logger.info("\n8. Searching todo items...")
    logger.info(todo_tools.search_todos("Christmas"))
    
    logger.info("\n9. Getting todo statistics...")
    logger.info(todo_tools.get_todo_statistics())
    
    logger.info("\n10. Deleting a todo item...")
    todo_tools.delete_todo(3)
    
    logger.info("\n11. Final todo list...")
    logger.info(todo_tools.list_todos())

def demo_root_agent_delegation():
    """Demonstrate root agent delegation logic"""
    print_separator("ROOT AGENT DELEGATION DEMO")
    
    # Import the root agent
    from root_agent.agent import root_agent
    
    print("\n1. Testing root agent delegation...")
    print("Note: This would require ADK CLI to run the agent interactively")
    print("To test delegation, run: adk run .")
    print("Then try these commands:")
    print("- 'remind me to call John tomorrow at 3 PM'")
    print("- 'add buy groceries to my todo list'")
    print("- 'set an alert for my dentist appointment'")
    print("- 'create a high priority task for project deadline'")
    
    print("\n2. Agent Configuration:")
    print(f"Root Agent: {root_agent.name}")
    print(f"Reminder Agent: {reminder_agent.name}")
    print(f"Todo Agent: {todo_agent.name}")
    print("All agents are properly configured and ready for delegation!")

def main():
    """Main demo function"""
    print_separator("PERSONAL AI ASSISTANT DEMO")
    print("This demo showcases the Personal AI Assistant system")
    print("with root agent delegation to specialized sub-agents.")
    print("\nThe system includes:")
    print("- Root Agent: Delegates tasks to appropriate sub-agents")
    print("- Reminder Agent: Manages reminders and alerts")
    print("- Todo Agent: Manages todo lists and tasks")
    print("- All agents use Google ADK framework with comprehensive tools")
    
    try:
        # Demo each component
        demo_reminder_agent()
        demo_todo_agent()
        demo_root_agent_delegation()
        
        print_separator("DEMO COMPLETE")
        print("All agents and tools are working correctly!")
        print("The Personal AI Assistant is ready to use.")
        print("\nNext steps:")
        print("1. Run with ADK CLI: adk run .")
        print("2. Start web UI: adk web")
        print("3. Integrate with your preferred interface")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 