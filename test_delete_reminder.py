#!/usr/bin/env python3
"""
Test script to debug delete reminder issue
"""

import yaml
from db.connection import DatabaseConnection
from db.repositories import ReminderRepository
from datetime import datetime, timedelta

def load_config():
    with open("application.yaml", "r") as f:
        return yaml.safe_load(f)

def test_delete_reminder():
    """Test delete reminder functionality"""
    print("🔍 Testing delete reminder functionality...")
    
    config = load_config()
    db_connection = DatabaseConnection(config.get('database', {}))
    
    if not db_connection.connect():
        print("❌ Failed to connect to database")
        return
    
    session = db_connection.get_session()
    if not session:
        print("❌ Failed to get database session")
        return
    
    repository = ReminderRepository(session)
    
    try:
        # First, add a test reminder
        print("  Adding test reminder...")
        result = repository.add_reminder(
            title="Test Delete Reminder",
            description="This is a test reminder for deletion",
            remind_time=datetime.now() + timedelta(hours=1)
        )
        
        if result["status"] != "success":
            print(f"  ❌ Failed to add reminder: {result['message']}")
            return
        
        reminder_id = result["reminder"]["id"]
        print(f"  ✅ Added reminder with ID: {reminder_id}")
        
        # List reminders to confirm it exists
        print("  Listing reminders before deletion...")
        list_result = repository.list_reminders()
        print(f"  Found {len(list_result['reminders'])} reminders")
        
        # Try to delete the reminder
        print(f"  Deleting reminder {reminder_id}...")
        delete_result = repository.delete_reminder(reminder_id)
        print(f"  Delete result: {delete_result}")
        
        # List reminders again to see if it was deleted
        print("  Listing reminders after deletion...")
        list_result_after = repository.list_reminders()
        print(f"  Found {len(list_result_after['reminders'])} reminders after deletion")
        
        # Check if the reminder still exists but is inactive
        print("  Checking if reminder exists but is inactive...")
        get_result = repository.get_reminder(reminder_id)
        print(f"  Get result: {get_result}")
        
        if delete_result["status"] == "success":
            print("  ✅ Delete operation reported success")
        else:
            print(f"  ❌ Delete operation failed: {delete_result['message']}")
            
    except Exception as e:
        print(f"  ❌ Exception during test: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()
        db_connection.close()

if __name__ == "__main__":
    test_delete_reminder() 