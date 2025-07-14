#!/usr/bin/env python3
"""
Test script to check delete_reminder tool functionality
"""

import yaml
from root_agent.sub_agents.reminder_agent.tools.reminder_tools import ReminderTools
from datetime import datetime, timedelta

def load_config():
    with open("application.yaml", "r") as f:
        return yaml.safe_load(f)

def test_delete_tool():
    """Test delete_reminder tool functionality"""
    print("🔍 Testing delete_reminder tool...")
    
    config = load_config()
    reminder_tools = ReminderTools(config)
    
    try:
        # First, add a test reminder
        print("  Adding test reminder...")
        add_result = reminder_tools.add_reminder(
            title="Test Delete Tool",
            description="This is a test reminder for tool deletion",
            remind_time="tomorrow at 10 AM"
        )
        
        if add_result["status"] != "success":
            print(f"  ❌ Failed to add reminder: {add_result['message']}")
            return
        
        reminder_id = add_result["reminder"]["id"]
        print(f"  ✅ Added reminder with ID: {reminder_id}")
        
        # List reminders to confirm it exists
        print("  Listing reminders before deletion...")
        list_result = reminder_tools.list_reminders()
        print(f"  Found {len(list_result['reminders'])} reminders")
        
        # Try to delete the reminder using the tool
        print(f"  Deleting reminder {reminder_id} using tool...")
        delete_result = reminder_tools.delete_reminder(reminder_id)
        print(f"  Delete tool result: {delete_result}")
        
        # List reminders again to see if it was deleted
        print("  Listing reminders after deletion...")
        list_result_after = reminder_tools.list_reminders()
        print(f"  Found {len(list_result_after['reminders'])} reminders after deletion")
        
        # Check if the reminder still exists but is inactive
        print("  Checking if reminder exists but is inactive...")
        get_result = reminder_tools.get_reminder(reminder_id)
        print(f"  Get result: {get_result}")
        
        if delete_result["status"] == "success":
            print("  ✅ Delete tool operation reported success")
        else:
            print(f"  ❌ Delete tool operation failed: {delete_result['message']}")
            
    except Exception as e:
        print(f"  ❌ Exception during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_delete_tool() 