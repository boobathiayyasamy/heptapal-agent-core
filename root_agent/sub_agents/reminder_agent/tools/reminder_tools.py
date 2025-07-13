from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

reminders_storage = []

class Reminder(BaseModel):
    id: int = Field(..., description="Unique identifier for the reminder.")
    title: str = Field(..., description="Short title for the reminder.")
    description: str = Field(..., description="Detailed description of what to be reminded about.")
    remind_time: str = Field(..., description="The specific time or expression when the reminder should trigger (e.g., '2024-12-15 15:30', 'tomorrow at 3 PM').")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp when the reminder was created.")
    is_active: bool = Field(True, description="Boolean indicating if the reminder is currently active.")


class ReminderTools:
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
            # Basic NLP for remind_time
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
            
            remind_datetime = datetime.combine(remind_date, remind_time_obj)
            remind_time_str = remind_datetime.strftime("%Y-%m-%d %H:%M:%S")

            reminder_id = len(reminders_storage) + 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            reminder = Reminder(
                id=reminder_id,
                title=title,
                description=description,
                remind_time=remind_time_str,
                is_active=True
            )
            
            reminders_storage.append(reminder)
            
            return {
                "status": "success",
                "message": f"Reminder '{title}' added successfully",
                "reminder": reminder.model_dump()
            }
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
            active_reminders = [r for r in reminders_storage if r.is_active]
            
            return {
                "status": "success",
                "message": f"Found {len(active_reminders)} active reminders",
                "reminders": [r.model_dump() for r in active_reminders]
            }
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
            reminder = next((r for r in reminders_storage if r.id == reminder_id), None)
            
            if not reminder:
                return {
                    "status": "error",
                    "message": f"Reminder with ID {reminder_id} not found"
                }
            
            return {
                "status": "success",
                "message": f"Reminder {reminder_id} retrieved successfully",
                "reminder": reminder.model_dump()
            }
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
            reminder = next((r for r in reminders_storage if r.id == reminder_id), None)
            
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
            
            return {
                "status": "success",
                "message": f"Reminder {reminder_id} updated successfully",
                "reminder": reminder.model_dump()
            }
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
            reminder = next((r for r in reminders_storage if r.id == reminder_id), None)
            
            if not reminder:
                return {
                    "status": "error",
                    "message": f"Reminder with ID {reminder_id} not found"
                }
            
            reminder.is_active = False
            
            return {
                "status": "success",
                "message": f"Reminder '{reminder.title}' deleted successfully"
            }
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
            query_lower = query.lower()
            matching_reminders = [
                r for r in reminders_storage 
                if r.is_active and (query_lower in r.title.lower() or query_lower in r.description.lower())
            ]
            
            return {
                "status": "success",
                "message": f"Found {len(matching_reminders)} matching reminders",
                "reminders": [r.model_dump() for r in matching_reminders]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to search reminders: {str(e)}"
            }
