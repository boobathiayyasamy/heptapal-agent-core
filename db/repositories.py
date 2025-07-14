"""
Database repositories for Heptapal Agent Core.
Single responsibility: Handle database operations for reminders and todos.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import SQLAlchemyError

from .models import Reminder, TodoItem, PriorityEnum, StatusEnum

logger = logging.getLogger(__name__)


class ReminderRepository:
    """
    Repository for reminder database operations.
    Single responsibility: Handle all reminder-related database operations.
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def add_reminder(self, title: str, description: str, remind_time: datetime) -> Dict:
        """
        Add a new reminder to the database.
        
        Args:
            title: Short title for the reminder
            description: Detailed description of what to be reminded about
            remind_time: When to remind (datetime object)
        
        Returns:
            dict: Status and reminder details
        """
        try:
            reminder = Reminder(
                title=title,
                description=description,
                remind_time=remind_time,
                is_active=True
            )
            
            self.session.add(reminder)
            self.session.commit()
            
            return {
                "status": "success",
                "message": f"Reminder '{title}' added successfully",
                "reminder": reminder.to_dict()
            }
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Failed to add reminder: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to add reminder: {str(e)}"
            }
    
    def list_reminders(self) -> Dict:
        """
        List all active reminders.
        
        Returns:
            dict: List of all active reminders
        """
        try:
            reminders = self.session.query(Reminder).filter(Reminder.is_active == True).all()
            
            return {
                "status": "success",
                "message": f"Found {len(reminders)} active reminders",
                "reminders": [r.to_dict() for r in reminders]
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to list reminders: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to list reminders: {str(e)}"
            }
    
    def get_reminder(self, reminder_id: int) -> Dict:
        """
        Get a specific reminder by ID.
        
        Args:
            reminder_id: ID of the reminder to retrieve
        
        Returns:
            dict: Reminder details or error message
        """
        try:
            reminder = self.session.query(Reminder).filter(Reminder.id == reminder_id).first()
            
            if not reminder:
                return {
                    "status": "error",
                    "message": f"Reminder with ID {reminder_id} not found"
                }
            
            return {
                "status": "success",
                "message": f"Reminder {reminder_id} retrieved successfully",
                "reminder": reminder.to_dict()
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to get reminder: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get reminder: {str(e)}"
            }
    
    def update_reminder(self, reminder_id: int, title: Optional[str] = None, 
                       description: Optional[str] = None, remind_time: Optional[datetime] = None) -> Dict:
        """
        Update an existing reminder.
        
        Args:
            reminder_id: ID of the reminder to update
            title: New title (optional)
            description: New description (optional)
            remind_time: New remind time (optional)
        
        Returns:
            dict: Updated reminder details or error message
        """
        try:
            reminder = self.session.query(Reminder).filter(Reminder.id == reminder_id).first()
            
            if not reminder:
                return {
                    "status": "error",
                    "message": f"Reminder with ID {reminder_id} not found"
                }
            
            if title:
                reminder.title = title
            if description:
                reminder.description = description
            if remind_time:
                reminder.remind_time = remind_time
            
            self.session.commit()
            
            return {
                "status": "success",
                "message": f"Reminder {reminder_id} updated successfully",
                "reminder": reminder.to_dict()
            }
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Failed to update reminder: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to update reminder: {str(e)}"
            }
    
    def delete_reminder(self, reminder_id: int) -> Dict:
        """
        Delete (deactivate) a reminder.
        
        Args:
            reminder_id: ID of the reminder to delete
        
        Returns:
            dict: Deletion status
        """
        try:
            reminder = self.session.query(Reminder).filter(Reminder.id == reminder_id).first()
            
            if not reminder:
                return {
                    "status": "error",
                    "message": f"Reminder with ID {reminder_id} not found"
                }
            
            reminder.is_active = False
            self.session.commit()
            
            return {
                "status": "success",
                "message": f"Reminder '{reminder.title}' deleted successfully"
            }
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Failed to delete reminder: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to delete reminder: {str(e)}"
            }
    
    def search_reminders(self, query: str) -> Dict:
        """
        Search reminders by title or description.
        
        Args:
            query: Search query
        
        Returns:
            dict: List of matching reminders
        """
        try:
            query_lower = f"%{query.lower()}%"
            reminders = self.session.query(Reminder).filter(
                and_(
                    Reminder.is_active == True,
                    or_(
                        func.lower(Reminder.title).like(query_lower),
                        func.lower(Reminder.description).like(query_lower)
                    )
                )
            ).all()
            
            return {
                "status": "success",
                "message": f"Found {len(reminders)} matching reminders",
                "reminders": [r.to_dict() for r in reminders]
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to search reminders: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to search reminders: {str(e)}"
            }


class TodoRepository:
    """
    Repository for todo database operations.
    Single responsibility: Handle all todo-related database operations.
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def add_todo(self, title: str, description: Optional[str] = None, 
                 priority: str = "medium", due_date: Optional[datetime] = None) -> Dict:
        """
        Add a new todo item to the database.
        
        Args:
            title: Short title for the todo item
            description: Detailed description of the task (optional)
            priority: Priority level (low, medium, high)
            due_date: Due date for the task (optional)
        
        Returns:
            dict: Status and todo item details
        """
        try:
            priority_enum = PriorityEnum(priority.lower())
            
            todo = TodoItem(
                title=title,
                description=description,
                priority=priority_enum,
                due_date=due_date
            )
            
            self.session.add(todo)
            self.session.commit()
            
            return {
                "status": "success",
                "message": f"Todo item '{title}' added successfully",
                "todo": todo.to_dict()
            }
        except ValueError:
            return {
                "status": "error",
                "message": "Invalid priority. Please choose from 'low', 'medium', or 'high'."
            }
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Failed to add todo: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to add todo: {str(e)}"
            }
    
    def list_todos(self, filter_status: Optional[str] = None, 
                   filter_priority: Optional[str] = None) -> Dict:
        """
        List todo items with optional filtering.
        
        Args:
            filter_status: Filter by status (pending, in_progress, completed)
            filter_priority: Filter by priority (low, medium, high)
        
        Returns:
            dict: List of todo items
        """
        try:
            query = self.session.query(TodoItem)
            
            if filter_status:
                status_enum = StatusEnum(filter_status.lower())
                query = query.filter(TodoItem.status == status_enum)
            
            if filter_priority:
                priority_enum = PriorityEnum(filter_priority.lower())
                query = query.filter(TodoItem.priority == priority_enum)
            
            todos = query.all()
            
            return {
                "status": "success",
                "message": f"Found {len(todos)} todo items",
                "todos": [t.to_dict() for t in todos]
            }
        except ValueError:
            return {
                "status": "error",
                "message": "Invalid filter value. Please check status and priority values."
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to list todos: {str(e)}")
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
            todo = self.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
            
            if not todo:
                return {
                    "status": "error",
                    "message": f"Todo item with ID {todo_id} not found"
                }
            
            return {
                "status": "success",
                "message": f"Todo item {todo_id} retrieved successfully",
                "todo": todo.to_dict()
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to get todo: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get todo: {str(e)}"
            }
    
    def update_todo(self, todo_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None, priority: Optional[str] = None,
                   status: Optional[str] = None, due_date: Optional[datetime] = None) -> Dict:
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
            todo = self.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
            
            if not todo:
                return {
                    "status": "error",
                    "message": f"Todo item with ID {todo_id} not found"
                }
            
            if title:
                todo.title = title
            if description:
                todo.description = description
            if priority:
                todo.priority = PriorityEnum(priority.lower())
            if status:
                todo.status = StatusEnum(status.lower())
                if status.lower() == "completed" and not todo.completed_at:
                    todo.completed_at = datetime.now()
                elif status.lower() != "completed":
                    todo.completed_at = None
            if due_date:
                todo.due_date = due_date
            
            self.session.commit()
            
            return {
                "status": "success",
                "message": f"Todo item {todo_id} updated successfully",
                "todo": todo.to_dict()
            }
        except ValueError as e:
            self.session.rollback()
            return {
                "status": "error",
                "message": f"Invalid value: {str(e)}"
            }
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Failed to update todo: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to update todo: {str(e)}"
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
            todo = self.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
            
            if not todo:
                return {
                    "status": "error",
                    "message": f"Todo item with ID {todo_id} not found"
                }
            
            self.session.delete(todo)
            self.session.commit()
            
            return {
                "status": "success",
                "message": f"Todo item '{todo.title}' deleted successfully"
            }
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Failed to delete todo: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to delete todo: {str(e)}"
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
            query_lower = f"%{query.lower()}%"
            todos = self.session.query(TodoItem).filter(
                or_(
                    func.lower(TodoItem.title).like(query_lower),
                    func.lower(TodoItem.description).like(query_lower)
                )
            ).all()
            
            return {
                "status": "success",
                "message": f"Found {len(todos)} matching todo items",
                "todos": [t.to_dict() for t in todos]
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to search todos: {str(e)}")
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
            total_todos = self.session.query(TodoItem).count()
            pending_todos = self.session.query(TodoItem).filter(TodoItem.status == StatusEnum.PENDING).count()
            in_progress_todos = self.session.query(TodoItem).filter(TodoItem.status == StatusEnum.IN_PROGRESS).count()
            completed_todos = self.session.query(TodoItem).filter(TodoItem.status == StatusEnum.COMPLETED).count()
            
            high_priority = self.session.query(TodoItem).filter(TodoItem.priority == PriorityEnum.HIGH).count()
            medium_priority = self.session.query(TodoItem).filter(TodoItem.priority == PriorityEnum.MEDIUM).count()
            low_priority = self.session.query(TodoItem).filter(TodoItem.priority == PriorityEnum.LOW).count()
            
            return {
                "status": "success",
                "statistics": {
                    "total": total_todos,
                    "pending": pending_todos,
                    "in_progress": in_progress_todos,
                    "completed": completed_todos,
                    "high_priority": high_priority,
                    "medium_priority": medium_priority,
                    "low_priority": low_priority
                }
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to get todo statistics: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get todo statistics: {str(e)}"
            } 