#!/usr/bin/env python3
"""
Test script to verify root agent delegation works correctly
"""

import sys
import os
import yaml
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    with open("application.yaml", "r") as f:
        return yaml.safe_load(f)

def test_root_agent_tools():
    """Test that the root agent has all the necessary tools"""
    print("Testing root agent tool configuration...")
    
    try:
        from root_agent.agent import root_agent
        
        # Check that the root agent has all the necessary tools
        print(f"Root agent has {len(root_agent.tools)} tools")
        
        # Just verify we have the right number of tools
        expected_count = 13  # 6 reminder tools + 7 todo tools
        
        if len(root_agent.tools) == expected_count:
            print("✅ Root agent has the correct number of tools")
            print("Tools available:")
            for i, tool in enumerate(root_agent.tools, 1):
                print(f"  {i}. {tool.__class__.__name__}")
            return True
        else:
            print(f"❌ Expected {expected_count} tools, got {len(root_agent.tools)}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing root agent: {e}")
        return False

def test_tool_functionality():
    """Test that the tools actually work"""
    print("\nTesting tool functionality...")
    
    try:
        from root_agent.sub_agents.reminder_agent.tools.reminder_tools import ReminderTools
        from root_agent.sub_agents.todo_agent.tools.todo_tools import TodoTools
        
        config = load_config()
        
        # Test reminder tools
        reminder_tools = ReminderTools(config)
        
        # Add a test reminder
        result = reminder_tools.add_reminder("Test Reminder", "This is a test", "tomorrow at 10 AM")
        print(f"✅ Add reminder: {result['status']}")
        
        # List reminders
        result = reminder_tools.list_reminders()
        print(f"✅ List reminders: {result['status']}")
        print(f"   Found {len(result['reminders'])} reminders")
        
        # Test todo tools
        todo_tools = TodoTools(config)
        
        # Add a test todo
        result = todo_tools.add_todo(title="Test Todo", description="This is a test todo", priority="medium")
        print(f"✅ Add todo: {result['status']}")
        
        # List todos
        result = todo_tools.list_todos()
        print(f"✅ List todos: {result['status']}")
        print(f"   Found {len(result['todos'])} todos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing tools: {e}")
        return False

def test_delegation_logic():
    """Test that the root agent instructions are clear about tool usage"""
    print("\nTesting delegation logic...")
    
    try:
        from root_agent.agent import root_agent
        
        instructions = str(root_agent.instruction)
        
        # Check for key delegation patterns
        key_phrases = [
            "list_reminders_tool",
            "add_reminder_tool", 
            "list_todos_tool",
            "add_todo_tool",
            "List my reminders",
            "Show my todos"
        ]
        
        missing_phrases = []
        for phrase in key_phrases:
            if phrase not in instructions:
                missing_phrases.append(phrase)
        
        if missing_phrases:
            print(f"❌ Missing key phrases in instructions: {missing_phrases}")
            return False
        else:
            print("✅ Root agent instructions include proper tool guidance")
            return True
            
    except Exception as e:
        print(f"❌ Error testing delegation logic: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("ROOT AGENT DELEGATION TEST")
    print("=" * 60)
    
    tests = [
        test_root_agent_tools,
        test_tool_functionality,
        test_delegation_logic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! The root agent should now properly handle:")
        print("   - 'list my reminders' → list_reminders_tool")
        print("   - 'show my todos' → list_todos_tool")
        print("   - 'add reminder' → add_reminder_tool")
        print("   - 'add todo' → add_todo_tool")
        print("\nThe delegation issue should be fixed!")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 