"""
task.py.

This script provides utilities and classes to create,
modify, and manage tasks.Tasks can have various attributes
such as id, name, description, due date, assignees, status,
priority, and categories.
"""

from datetime import datetime, date
from enum import Enum, unique
from typing import TypedDict, Union


def parse_date(date_string: str) -> datetime:
    """Convert a string in the format 'DD-MM-YYYY' to a datetime object."""
    return datetime.strptime(date_string, "%Y/%m/%d")


def format_date(date_obj: datetime) -> str:
    """Convert a datetime object to a string in the format 'DD-MM-YYYY'."""
    return date_obj.strftime("%d-%m-%Y")


@unique
class TaskStatus(Enum):
    """
    Enum class representing various stages of a task's lifecycle.

    Attributes:
    START (int): Indicates the task has just begun.
    IN_PROGRESS (int): Indicates the task is currently being worked on.
    COMPLETE (int): Indicates the task has been finished.
    """

    START = 1
    IN_PROGRESS = 2
    COMPLETE = 3

    def __str__(self) -> str:
        """Return task status as a formatted string."""
        return self.name.replace("_", " ").title()


@unique
class TaskPriority(Enum):
    """
    Enum class representing the priority levels of a task.

    Attributes:
    LOW (int): Task with the least urgency.
    MEDIUM (int): Task with moderate urgency.
    HIGH (int): Task with the highest urgency.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __str__(self) -> str:
        """Return priority level as a formatted string."""
        return self.name.title()


class TaskData(TypedDict):
    """A dictionary representing the data structure of a Task."""

    name: str
    description: str
    due_date: datetime
    creation_date: datetime
    assignee: str
    status: TaskStatus
    priority: TaskPriority
    categories: str


class Task:
    """
    Represents a Task object.

    It has attributes such as ID, name, description, etc.
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        due_date: Union[datetime, str],
        assignee: str,
        status: TaskStatus = TaskStatus.IN_PROGRESS,
        priority: TaskPriority = TaskPriority.MEDIUM,
        categories: str = ""
    ) -> None:
        """
        Initialize a Task object.

        Parameters:
        name (str): The name of the task.
        description (str): The description of the task.
        due_date (Union[datetime, str]): The due date of the task.
        Can be either a datetime object or a string in
        'DD-MM-YYYY' format.
        assignee (str): List of assignees for the task.
        status (TaskStatus, optional): The status of the task.
        Default is IN_PROGRESS.
        priority (TaskPriority, optional): Priority of the task.
        Default is MEDIUM.
        categories (str, optional): Categories the task belongs to.
        Default is None.
        """
        self.id = id
        self.name = name
        self.description = description
        self.creation_date = date.today()

        # Ensure that due_date is always in 'DD-MM-YYYY' format
        if isinstance(due_date, str):
            self._set_initial_due_date(parse_date(due_date))
        elif isinstance(due_date, date):
            # Format the datetime object as 'DD-MM-YYYY' string
            self._set_initial_due_date(due_date)
        else:
            raise ValueError("Invalid type for due_date")

        self.assignee = assignee
        self.status = status
        self.priority = priority
        self.categories = categories

    @property
    def id(self) -> int:
        """Getter for the task's id."""
        return self._id

    @id.setter
    def id(self, new_id: int) -> None:
        if not new_id:
            raise ValueError("Id must be a non-empty integer")
        self._id = new_id

    @property
    def name(self) -> str:
        """Getter for the task's name."""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if not new_name or not isinstance(new_name, str) or new_name.isnumeric():
            raise ValueError("Name must be a non-empty string")
        self._name = new_name

    @property
    def description(self) -> str:
        """Getter for the task's description."""
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        if not new_description or not isinstance(new_description, str) or new_description.isnumeric():
            raise ValueError("Description must be a non-empty string")
        self._description = new_description

    def _set_initial_due_date(self, date: datetime) -> None:
        if date <= date.today():
            raise ValueError("Due date must be a future date")
        self._due_date = date

    @property
    def due_date(self) -> datetime:
        """Getter for the task's due date."""
        return self._due_date

    @due_date.setter
    def due_date(self, new_due_date: datetime) -> None:
        if new_due_date <= date.today():
            raise ValueError("Due date must be a future date")
        self._due_date = new_due_date

    @property
    def assignee(self) -> str:
        """Getter for the list of assignees for the task."""
        return self._assignee

    @assignee.setter
    def assignee(self, new_assignee: str) -> None:
        if not new_assignee or not isinstance(new_assignee, str) or new_assignee.isnumeric():
            raise ValueError(
                "Assignee list must be a non-empty string"
            )
        self._assignee = new_assignee

    @property
    def status(self) -> TaskStatus:
        """Getter for the task's status."""
        return self._status

    @status.setter
    def status(self, new_status: TaskStatus) -> None:
        if not isinstance(new_status, TaskStatus):
            raise ValueError("Invalid status type")
        self._status = new_status

    @property
    def priority(self) -> TaskPriority:
        """Getter for the task's priority level."""
        return self._priority

    @priority.setter
    def priority(self, new_priority: TaskPriority) -> None:
        if not isinstance(new_priority, TaskPriority):
            raise ValueError("Invalid priority type")
        self._priority = new_priority

    @property
    def categories(self) -> str:
        """Getter for the task's categories."""
        return self.categories

    @categories.setter
    def categories(self, new_categories: str) -> None:
        if not new_categories or not isinstance(new_categories, str) or new_categories.isnumeric():
            raise ValueError("Categories must be a non-empt string")
        self._categories = new_categories
