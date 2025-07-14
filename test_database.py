#!/usr/bin/env python3
"""
Test script to verify database functionality for Heptapal Agent Core.
"""

import yaml
import logging
from datetime import datetime, timedelta

from db.connection import DatabaseConnection
from db.repositories import ReminderRepository, TodoRepository

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    """Load application configuration."""
    with open("application.yaml", "r") as f:
        return yaml.safe_load(f)


def test_database_connection():
    """Test database connection."""
    print("🔌 Testing database connection...")
    
    config = load_config()
    db_config = config.get('database', {})
    
    db_connection = DatabaseConnection(db_config)
    
    if db_connection.connect():
        print("✅ Database connection successful")
        return db_connection
    else:
        print("❌ Database connection failed")
        return None


def test_reminder_operations(db_connection):
    """Test reminder operations."""
    print("\n📅 Testing reminder operations...")
    
    session = db_connection.get_session()
    if not session:
        print("❌ Failed to get database session")
        return
    
    repository = ReminderRepository(session)
    
    try:
        # Test adding a reminder
        print("  Adding reminder...")
        result = repository.add_reminder(
            title="Test Meeting",
            description="This is a test reminder for database functionality",
            remind_time=datetime.now() + timedelta(hours=1)
        )
        
        if result["status"] == "success":
            print("  ✅ Reminder added successfully")
            reminder_id = result["reminder"]["id"]
            
            # Test getting the reminder
            print("  Getting reminder...")
            get_result = repository.get_reminder(reminder_id)
            if get_result["status"] == "success":
                print("  ✅ Reminder retrieved successfully")
            
            # Test listing reminders
            print("  Listing reminders...")
            list_result = repository.list_reminders()
            if list_result["status"] == "success":
                print(f"  ✅ Found {len(list_result['reminders'])} reminders")
            
            # Test searching reminders
            print("  Searching reminders...")
            search_result = repository.search_reminders("test")
            if search_result["status"] == "success":
                print(f"  ✅ Found {len(search_result['reminders'])} matching reminders")
            
            # Test updating reminder
            print("  Updating reminder...")
            update_result = repository.update_reminder(
                reminder_id, 
                title="Updated Test Meeting"
            )
            if update_result["status"] == "success":
                print("  ✅ Reminder updated successfully")
            
            # Test deleting reminder
            print("  Deleting reminder...")
            delete_result = repository.delete_reminder(reminder_id)
            if delete_result["status"] == "success":
                print("  ✅ Reminder deleted successfully")
        
        else:
            print(f"  ❌ Failed to add reminder: {result['message']}")
    
    except Exception as e:
        print(f"  ❌ Error during reminder operations: {str(e)}")
    
    finally:
        session.close()


def test_todo_operations(db_connection):
    """Test todo operations."""
    print("\n📝 Testing todo operations...")
    
    session = db_connection.get_session()
    if not session:
        print("❌ Failed to get database session")
        return
    
    repository = TodoRepository(session)
    
    try:
        # Test adding a todo
        print("  Adding todo...")
        result = repository.add_todo(
            title="Test Task",
            description="This is a test todo for database functionality",
            priority="high",
            due_date=datetime.now() + timedelta(days=1)
        )
        
        if result["status"] == "success":
            print("  ✅ Todo added successfully")
            todo_id = result["todo"]["id"]
            
            # Test getting the todo
            print("  Getting todo...")
            get_result = repository.get_todo(todo_id)
            if get_result["status"] == "success":
                print("  ✅ Todo retrieved successfully")
            
            # Test listing todos
            print("  Listing todos...")
            list_result = repository.list_todos()
            if list_result["status"] == "success":
                print(f"  ✅ Found {len(list_result['todos'])} todos")
            
            # Test filtering todos
            print("  Filtering todos by priority...")
            filter_result = repository.list_todos(filter_priority="high")
            if filter_result["status"] == "success":
                print(f"  ✅ Found {len(filter_result['todos'])} high priority todos")
            
            # Test searching todos
            print("  Searching todos...")
            search_result = repository.search_todos("test")
            if search_result["status"] == "success":
                print(f"  ✅ Found {len(search_result['todos'])} matching todos")
            
            # Test updating todo
            print("  Updating todo...")
            update_result = repository.update_todo(
                todo_id, 
                title="Updated Test Task",
                status="in_progress"
            )
            if update_result["status"] == "success":
                print("  ✅ Todo updated successfully")
            
            # Test getting statistics
            print("  Getting todo statistics...")
            stats_result = repository.get_todo_statistics()
            if stats_result["status"] == "success":
                print("  ✅ Todo statistics retrieved successfully")
                print(f"     Total: {stats_result['statistics']['total']}")
                print(f"     Pending: {stats_result['statistics']['pending']}")
                print(f"     In Progress: {stats_result['statistics']['in_progress']}")
                print(f"     Completed: {stats_result['statistics']['completed']}")
            
            # Test deleting todo
            print("  Deleting todo...")
            delete_result = repository.delete_todo(todo_id)
            if delete_result["status"] == "success":
                print("  ✅ Todo deleted successfully")
        
        else:
            print(f"  ❌ Failed to add todo: {result['message']}")
    
    except Exception as e:
        print(f"  ❌ Error during todo operations: {str(e)}")
    
    finally:
        session.close()


def main():
    """Main test function."""
    print("🚀 Starting database functionality test...")
    
    # Test database connection
    db_connection = test_database_connection()
    if not db_connection:
        return
    
    # Test reminder operations
    test_reminder_operations(db_connection)
    
    # Test todo operations
    test_todo_operations(db_connection)
    
    # Close database connection
    db_connection.close()
    
    print("\n🎉 Database functionality test completed!")


if __name__ == "__main__":
    main() 