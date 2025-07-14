"""
Database initialization script for Heptapal Agent Core.
Creates tables and tests database connection.
"""

import yaml
import logging
from pathlib import Path

from .connection import DatabaseConnection
from .models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config() -> dict:
    """
    Load application configuration from application.yaml.
    
    Returns:
        dict: Application configuration
    """
    config_path = Path(__file__).parent.parent / "application.yaml"
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise


def init_database():
    """
    Initialize database by creating tables and testing connection.
    """
    try:
        # Load configuration
        config = load_config()
        db_config = config.get('database', {})
        
        if not db_config:
            logger.error("Database configuration not found in application.yaml")
            return False
        
        # Create database connection
        db_connection = DatabaseConnection(db_config)
        
        # Test connection
        if not db_connection.connect():
            logger.error("Failed to connect to database")
            return False
        
        logger.info("Database connection successful")
        
        # Create tables
        db_connection.create_tables(Base)
        
        # Test connection again
        if not db_connection.test_connection():
            logger.error("Database connection test failed after table creation")
            return False
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = init_database()
    if success:
        print("✅ Database initialization completed successfully")
    else:
        print("❌ Database initialization failed")
        exit(1) 