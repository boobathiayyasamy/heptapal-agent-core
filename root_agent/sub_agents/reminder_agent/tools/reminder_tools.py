from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from db.connection import DatabaseConnection
from db.repositories import ReminderRepository


class Reminder(BaseModel):
    id: int = Field(..., description="Unique identifier for the reminder.")
    title: str = Field(..., description="Short title for the reminder.")
    description: str = Field(..., description="Detailed description of what to be reminded about.")
    remind_time: str = Field(..., description="The specific time or expression when the reminder should trigger (e.g., '2024-12-15 15:30', 'tomorrow at 3 PM').")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp when the reminder was created.")
    is_active: bool = Field(True, description="Boolean indicating if the reminder is currently active.")


class ReminderTools:
    def __init__(self, config: Dict):
        """
        Initialize ReminderTools with database connection.
        
        Args:
            config: Application configuration containing database settings
        """
        self.config = config
        self.db_connection = DatabaseConnection(config.get('database', {}))
        self.db_connection.connect()
    
    def _parse_remind_time(self, remind_time: str) -> datetime:
        """
        Parse remind_time string into datetime object.
        
        Args:
            remind_time: Time string (e.g., "2024-12-15 15:30", "tomorrow at 3 PM")
        
        Returns:
            datetime: Parsed datetime object
        """
        remind_time_lower = remind_time.lower()
        now = datetime.now()
        
        if "tomorrow" in remind_time_lower:
            remind_date = now.date() + timedelta(days=1)
        else:
            remind_date = now.date()

        time_str = remind_time_lower.replace("tomorrow", "").strip()
        try:
            remind_time_obj = datetime.strptime(time_str, "%I %p").time()
        except ValueError:
            try:
                remind_time_obj = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                remind_time_obj = now.time()
        
        return datetime.combine(remind_date, remind_time_obj)

    def add_reminder(self, title: str, description: str, remind_time: str) -> Dict:
        """
        Add a new reminder to the system.
        Args:
            title: Short title for the reminder
            description: Detailed description of what to be reminded about
            remind_time: When to remind (e.g., "2024-12-15 15:30", "tomorrow at 3 PM")
        Returns:
            dict: Status and reminder details
        """
        try:
            parsed_time = self._parse_remind_time(remind_time)
            
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = ReminderRepository(session)
            result = repository.add_reminder(title, description, parsed_time)
            session.close()
            
            return result
        except Exception as e:
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
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = ReminderRepository(session)
            result = repository.list_reminders()
            session.close()
            
            return result
        except Exception as e:
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
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = ReminderRepository(session)
            result = repository.get_reminder(reminder_id)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get reminder: {str(e)}"
            }

    def update_reminder(self, reminder_id: int, title: Optional[str] = None, description: Optional[str] = None, remind_time: Optional[str] = None) -> Dict:
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
            parsed_time = None
            if remind_time:
                parsed_time = self._parse_remind_time(remind_time)
            
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = ReminderRepository(session)
            result = repository.update_reminder(reminder_id, title, description, parsed_time)
            session.close()
            
            return result
        except Exception as e:
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
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = ReminderRepository(session)
            result = repository.delete_reminder(reminder_id)
            session.close()
            
            return result
        except Exception as e:
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
            session = self.db_connection.get_session()
            if not session:
                return {
                    "status": "error",
                    "message": "Database connection failed"
                }
            
            repository = ReminderRepository(session)
            result = repository.search_reminders(query)
            session.close()
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to search reminders: {str(e)}"
            }
