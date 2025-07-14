from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from db.connection import DatabaseConnection
from db.repositories import TodoRepository


class TodoItem(BaseModel):
    id: int = Field(..., description="Unique identifier for the todo item.")
    title: str = Field(..., description="Short title for the todo item.")
    description: Optional[str] = Field(None, description="Detailed description of the task.")
    priority: str = Field("medium", description="Priority level of the todo item (low, medium, high).")
    status: str = Field("pending", description="Current status of the todo item (pending, in_progress, completed).")
    due_date: Optional[str] = Field(None, description="Optional due date for the task in YYYY-MM-DD format.")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp when the todo item was created.")
    completed_at: Optional[str] = Field(None, description="Timestamp when the todo item was marked as completed.")


class TodoTools:
    def __init__(self, config: Dict):
        """
        Initialize TodoTools with database connection.
        
        Args:
            config: Application configuration containing database settings
        """
        self.config = config
        self.db_connection = DatabaseConnection(config.get('database', {}))
        self.db_connection.connect()

    def _parse_due_date(self, due_date: str) -> Optional[datetime]:
        """
        Parse due_date string into datetime object.
        
        Args:
            due_date: Date string in YYYY-MM-DD format
        
        Returns:
            datetime: Parsed datetime object or None if invalid
        """
        if not due_date:
            return None
        
        try:
            return datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return None

    def add_todo(self, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, due_date: Optional[str] = None) -> Dict:
        """
        Add a new todo item to the list.
        Args:
            title: Short title for the todo item (optional). If not provided, a title will be generated from the description.
            description: Detailed description of the task (optional).
            priority: Priority level (low, medium, high). If not provided, uses the default from application.yaml.
            due_date: Due date for the task (optional).
        Returns:
            dict: Status and todo item details
        """
        try:
            if not description:
                return {
                    "status": "error",
                    "message": "Description is required to add a todo item."
                }

            if not title:
                title = ' '.join(description.split()[:5])
                if len(description.split()) > 5:
                    title += '...'

            if priority is None:
                priority = self.config.get("default_todo_priority", "medium")
            elif priority not in ["low", "medium", "high"]:
                return {
                    "status": "error",
                    "message": "Invalid priority. Please choose from 'low', 'medium', or 'high'."
                }
            
            parsed_due_date = self._parse_due_date(due_date) if due_date else None
            
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = TodoRepository(session)
            result = repository.add_todo(title, description, priority, parsed_due_date)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add todo item: {str(e)}"
            }

    def list_todos(self, filter_status: Optional[str] = None, filter_priority: Optional[str] = None) -> Dict:
        """
        List todo items with optional filtering.
        Args:
            filter_status: Filter by status (pending, in_progress, completed)
            filter_priority: Filter by priority (low, medium, high)
        Returns:
            dict: List of todo items
        """
        try:
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = TodoRepository(session)
            result = repository.list_todos(filter_status, filter_priority)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to list todos: {str(e)}"
            }

    def get_todo(self, todo_id: int) -> Dict:
        """
        Get a specific todo item by ID.
        Args:
            todo_id: ID of the todo item to retrieve
        Returns:
            dict: Todo item details or error message
        """
        try:
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = TodoRepository(session)
            result = repository.get_todo(todo_id)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get todo item: {str(e)}"
            }

    def update_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None, 
                    priority: Optional[str] = None, status: Optional[str] = None, 
                    due_date: Optional[str] = None) -> Dict:
        """
        Update an existing todo item.
        Args:
            todo_id: ID of the todo item to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            status: New status (optional)
            due_date: New due date (optional)
        Returns:
            dict: Updated todo item details or error message
        """
        try:
            parsed_due_date = self._parse_due_date(due_date) if due_date else None
            
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = TodoRepository(session)
            result = repository.update_todo(todo_id, title, description, priority, status, parsed_due_date)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update todo item: {str(e)}"
            }

    def delete_todo(self, todo_id: int) -> Dict:
        """
        Delete a todo item permanently.
        Args:
            todo_id: ID of the todo item to delete
        Returns:
            dict: Deletion status
        """
        try:
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = TodoRepository(session)
            result = repository.delete_todo(todo_id)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete todo item: {str(e)}"
            }

    def search_todos(self, query: str) -> Dict:
        """
        Search todo items by title or description.
        Args:
            query: Search query
        Returns:
            dict: List of matching todo items
        """
        try:
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = TodoRepository(session)
            result = repository.search_todos(query)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to search todos: {str(e)}"
            }

    def get_todo_statistics(self) -> Dict:
        """
        Get statistics about todo items.
        Returns:
            dict: Various statistics about todo items
        """
        try:
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = TodoRepository(session)
            result = repository.get_todo_statistics()
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get todo statistics: {str(e)}"
            }
