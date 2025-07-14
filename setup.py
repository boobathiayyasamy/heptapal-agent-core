#!/usr/bin/env python3
"""
Setup script for Heptapal Agent Core.
Installs dependencies and initializes the database.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 12):
        print("❌ Python 3.12 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def install_dependencies():
    """Install Python dependencies using uv."""
    # Check if uv is available
    if not run_command("uv --version", "Checking for uv"):
        print("❌ uv is not installed. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    
    # Install dependencies using uv add
    return run_command("uv add mysql-connector-python sqlalchemy", "Installing dependencies with uv")


def setup_database():
    """Set up the database."""
    print("\n🗄️  Database Setup")
    print("=" * 50)
    
    # Check if MySQL client is available
    if not run_command("mysql --version", "Checking MySQL client"):
        print("⚠️  MySQL client not found. Please install MySQL client tools.")
        print("   You can still run the application, but database setup will need to be done manually.")
        return True
    
    # Ask user if they want to set up the database
    response = input("\nDo you want to set up the database now? (y/n): ").lower().strip()
    if response != 'y':
        print("⏭️  Skipping database setup. You can run it manually later with:")
        print("   mysql -h 192.168.0.111 -u admin -p < database_schema.sql")
        return True
    
    # Run database schema
    if run_command("mysql -h 192.168.0.111 -u admin -p heptapal-db < database_schema.sql", "Creating database tables"):
        print("✅ Database setup completed")
        return True
    else:
        print("❌ Database setup failed. Please check your MySQL connection and run manually:")
        print("   mysql -h 192.168.0.111 -u admin -p heptapal-db < database_schema.sql")
        return False


def test_setup():
    """Test the setup by running the database test."""
    print("\n🧪 Testing Setup")
    print("=" * 50)
    
    if run_command("python test_database.py", "Running database tests"):
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return False


def main():
    """Main setup function."""
    print("🚀 Heptapal Agent Core Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Failed to setup database")
        sys.exit(1)
    
    # Test setup
    if not test_setup():
        print("❌ Setup verification failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the demo: python demo_assistant.py")
    print("2. Use with ADK: adk run .")
    print("3. Check the documentation: README.md and DATABASE_SETUP.md")


if __name__ == "__main__":
    main() 