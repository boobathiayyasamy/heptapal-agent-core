from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

todos_storage = []

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
        self.config = config

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
            
            todo_id = len(todos_storage) + 1
            
            todo = TodoItem(
                id=todo_id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )
            
            todos_storage.append(todo)
            
            return {
                "status": "success",
                "message": f"Todo item '{title}' added successfully",
                "todo": todo.model_dump()
            }
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
            filtered_todos = todos_storage.copy()
            
            if filter_status:
                filtered_todos = [t for t in filtered_todos if t.status == filter_status]
            
            if filter_priority:
                filtered_todos = [t for t in filtered_todos if t.priority == filter_priority]
            
            return {
                "status": "success",
                "message": f"Found {len(filtered_todos)} todo items",
                "todos": [t.model_dump() for t in filtered_todos]
            }
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
            todo = next((t for t in todos_storage if t.id == todo_id), None)
            
            if not todo:
                return {
                    "status": "error",
                    "message": f"Todo item with ID {todo_id} not found"
                }
            
            return {
                "status": "success",
                "message": f"Todo item {todo_id} retrieved successfully",
                "todo": todo.model_dump()
            }
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
            todo = next((t for t in todos_storage if t.id == todo_id), None)
            
            if not todo:
                return {
                    "status": "error",
                    "message": f"Todo item with ID {todo_id} not found"
                }
            
            if title:
                todo.title = title
            if description:
                todo.description = description
            if priority and priority in ["low", "medium", "high"]:
                todo.priority = priority
            if status and status in ["pending", "in_progress", "completed"]:
                todo.status = status
                if status == "completed" and not todo.completed_at:
                    todo.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                elif status != "completed":
                    todo.completed_at = None
            if due_date:
                todo.due_date = due_date
            
            return {
                "status": "success",
                "message": f"Todo item {todo_id} updated successfully",
                "todo": todo.model_dump()
            }
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
            todo = next((t for t in todos_storage if t.id == todo_id), None)
            
            if not todo:
                return {
                    "status": "error",
                    "message": f"Todo item with ID {todo_id} not found"
                }
            
            todos_storage.remove(todo)
            
            return {
                "status": "success",
                "message": f"Todo item '{todo.title}' deleted successfully"
            }
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
            query_lower = query.lower()
            matching_todos = [
                t for t in todos_storage 
                if query_lower in t.title.lower() or query_lower in t.description.lower()
            ]
            
            return {
                "status": "success",
                "message": f"Found {len(matching_todos)} matching todo items",
                "todos": [t.model_dump() for t in matching_todos]
            }
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
            total_todos = len(todos_storage)
            pending_todos = len([t for t in todos_storage if t.status == "pending"])
            in_progress_todos = len([t for t in todos_storage if t.status == "in_progress"])
            completed_todos = len([t for t in todos_storage if t.status == "completed"])
            
            high_priority = len([t for t in todos_storage if t.priority == "high"])
            medium_priority = len([t for t in todos_storage if t.priority == "medium"])
            low_priority = len([t for t in todos_storage if t.priority == "low"])
            
            overdue_todos = len([t for t in todos_storage if t.due_date and t.due_date < datetime.now().strftime("%Y-%m-%d") and t.status != "completed"])
            
            return {
                "status": "success",
                "message": "Todo statistics retrieved successfully",
                "statistics": {
                    "total": total_todos,
                    "pending": pending_todos,
                    "in_progress": in_progress_todos,
                    "completed": completed_todos,
                    "high_priority": high_priority,
                    "medium_priority": medium_priority,
                    "low_priority": low_priority,
                    "overdue": overdue_todos
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get todo statistics: {str(e)}"
            }
