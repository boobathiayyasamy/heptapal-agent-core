"""
Database connection management for Heptapal Agent Core.
Single responsibility: Handle database connections and session management.
"""

import logging
from typing import Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Database connection manager with single responsibility for connection handling.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize database connection with configuration.
        
        Args:
            config: Database configuration dictionary
        """
        self.config = config
        self.engine = None
        self.SessionLocal = None
        self._connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        """
        Build MySQL connection string from configuration.
        
        Returns:
            str: MySQL connection string
        """
        return (
            f"mysql+mysqlconnector://{self.config['user']}:{self.config['password']}"
            f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            f"?charset={self.config.get('charset', 'utf8mb4')}"
        )
    
    def connect(self) -> bool:
        """
        Establish database connection and create engine.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.engine = create_engine(
                self._connection_string,
                pool_size=self.config.get('pool_size', 10),
                max_overflow=self.config.get('max_overflow', 20),
                pool_pre_ping=True,
                echo=False
            )
            
            # Test connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            
            self.SessionLocal = sessionmaker(
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"Successfully connected to database: {self.config['database']}")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            return False
    
    def get_session(self) -> Optional[Session]:
        """
        Get a new database session.
        
        Returns:
            Session: Database session or None if connection failed
        """
        if not self.SessionLocal:
            if not self.connect():
                return None
        
        return self.SessionLocal()
    
    def close(self):
        """
        Close database connection and dispose engine.
        """
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
    
    def create_tables(self, base):
        """
        Create all tables defined in the base.
        
        Args:
            base: SQLAlchemy declarative base
        """
        try:
            base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create tables: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: True if connection is working, False otherwise
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except SQLAlchemyError as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False 