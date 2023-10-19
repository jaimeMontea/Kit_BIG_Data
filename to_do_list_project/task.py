#task.py: This file would contain the Task class that represents an individual task. 
#This class would have all the attributes you've listed (ID, name, description, etc.) 
#and possibly methods to manipulate these attributes.

from datetime import datetime
from enum import Enum

def parse_date(date_string: str) -> datetime:
    """Convert a string in the format 'DD-MM-YYYY' to a datetime object."""
    return datetime.strptime(date_string, "%d-%m-%Y")

def format_date(date_obj: datetime) -> str:
    """Convert a datetime object to a string in the format 'DD-MM-YYYY'."""
    return date_obj.strftime("%d-%m-%Y")

class TaskStatus(Enum):
    START = 1
    IN_PROGRESS = 2
    COMPLETE = 3

    def __str__(self):
        return self.name.replace("_", " ").title()

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __str__(self):
        return self.name.title()

class Task:
    """
    Represents a Task object with attributes such as ID, name, description, etc.
    """
    def __init__(self, name: str, description: str, due_date: datetime, assignee: list[str], 
                status: TaskStatus = TaskStatus.IN_PROGRESS, 
                priority: TaskPriority = TaskPriority.MEDIUM, 
                categories: list[str] = None) -> None:
        if categories is None:
            categories = []
            
        self.name = name
        self.description = description
        self.creation_date = datetime.now()
        self._set_initial_due_date(due_date) 
        self.assignee = assignee
        self.status = status
        self.priority = priority
        self._categories = categories

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if not new_name:
            raise ValueError("Name must be a non-empty string")
        self._name = new_name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        if not new_description:
            raise ValueError("Description must be a non-empty string")
        self._description = new_description

    def _set_initial_due_date(self, date: datetime):
        """Set the initial due date for the task after verification."""
        if date <= datetime.now():
            raise ValueError("Due date must be a future date")
        self._due_date = date

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @due_date.setter
    def due_date(self, new_due_date: datetime) -> None:
        if new_due_date <= datetime.now():
            raise ValueError("Due date must be a future date")
        self._due_date = new_due_date

    @property
    def assignee(self) -> list[str]:
        return self._assignee

    @assignee.setter
    def assignee(self, new_assignee: list[str]) -> None:
        if not new_assignee or not all(isinstance(assignee, str) for assignee in new_assignee):
            raise ValueError("Assignee list must be a non-empty list of strings")
        self._assignee = new_assignee

    @property
    def status(self) -> TaskStatus:
        return self._status

    @status.setter
    def status(self, new_status: TaskStatus) -> None:
        if not isinstance(new_status, TaskStatus):
            raise ValueError("Invalid status type")
        self._status = new_status

    @property
    def priority(self) -> TaskPriority:
        return self._priority

    @priority.setter
    def priority(self, new_priority: TaskPriority) -> None:
        if not isinstance(new_priority, TaskPriority):
            raise ValueError("Invalid priority type")
        self._priority = new_priority

    @property
    def categories(self) -> list[str]:
        return self._categories

    @categories.setter
    def categories(self, new_categories: list[str]) -> None:
        # Allow empty lists but still check for valid string entries
        if not all(isinstance(category, str) for category in new_categories):
            raise ValueError("Categories must be a list of strings")
        self._categories = new_categories