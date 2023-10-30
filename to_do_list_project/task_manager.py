"""
task_manager.py.

This module provides functionalities to manage tasks
using an SQLite database. It primarily contains the
`TaskManager` class that enables operations like
loading tasks from the database, adding new tasks,
removing tasks, marking tasks as complete, listing
all tasks, and modifying tasks.

Classes:
    - TaskNotFoundError: Raised when a specified
      task is not found in the manager.
    - TaskManager: The main class to manage
      tasks with methods to handle CRUD operations
      and other utility functionalities related to tasks.
"""

from datetime import datetime
from typing import List, Optional

from .db import SQLiteDB
from .task import Task, TaskData, TaskStatus, TaskPriority


class TaskNotFoundError(Exception):
    """Exception raised when a task is not found in the manager."""


class TaskManager:
    """
    A management system for tasks using an SQLite database.

    This class provides methods to handle the CRUD
    operations and other utility functionalities
    related to tasks.
    """

    def __init__(self, db: Optional[SQLiteDB] = None) -> None:
        """
        Initialize the TaskManager object.

        Args:
            db_name (str): Name of the database.

        Raises:
            DatabaseConnectionError: If the database connection fails.
        """
        self._db = db or SQLiteDB()
        self._tasks = self.load_tasks_from_db()

    def load_tasks_from_db(self) -> List[Task]:
        """
        Load all tasks from database.

        Returns:
            List of Task instances.
        
        """
        all_tasks = self._db.get_all_tasks()
        tasks = []
        if all_tasks:
            for task_tuple in all_tasks:
                (
                    task_id,
                    name,
                    description,
                    creation_date,
                    due_date,
                    assignee,
                    status,
                    priority,
                    categories,
                ) = task_tuple

                status = [
                    c_status
                    for c_status in TaskStatus
                    if c_status.value == status
                ][0]
                priority = [
                    c_priority
                    for c_priority in TaskPriority
                    if c_priority.value == priority
                ][0]
                task = Task(
                    task_id,
                    name,
                    description,
                    datetime.strptime(due_date, "%Y/%m/%d"),
                    assignee,
                    status,
                    priority,
                    categories,
                )
                tasks.append(task)
        return tasks

    def add_task(
        self,
        name: str,
        description: str,
        due_date: datetime,
        assignee: str,
        status: TaskStatus = TaskStatus.IN_PROGRESS,
        priority: TaskPriority = TaskPriority.MEDIUM,
        categories: str = None,
    ) -> int:
        """
        Add task to database.

        Args:
            name (str): Name of the task.
            description (str): Description of the data base.
            due_date (datetime.date): Due Date of the task.
            assignee (str): Assignee of the task.
            status (TaskStatus): Status of the task.
            priority (TaskPriority): Priority of the task.
            categories (str): Category of the task.

        Returns:
            task_id (int): Id of the task in data base.
        """
        task_data: TaskData = {
            "name": name,
            "description": description,
            "creation_date": datetime.now(),
            "due_date": due_date,
            "assignee": assignee,
            "status": status,
            "priority": priority,
            "categories": categories,
        }

        task_id = self._db.insert_data("tasks", task_data)
        task = Task(
            task_id,
            name,
            description,
            due_date,
            assignee,
            status,
            priority,
            categories,
        )
        self._tasks.append(task)
        return task_id

    def remove_task(self, task_id: int) -> None:
        """
        Remove task from database.
        
        Args:
            task_id (int): Task id of the task.
        Raises:
            TaskNotFoundError: If the task is not found.
        """
        self.get_task_by_id(task_id)
        self._db.remove_task(task_id)
        for index, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[index]

    def complete_task(self, task_id: int) -> None:
        """
        Mark a task as complete.

        Args:
            task_id (int): Task id of the task.

        Raises:
            TaskNotFoundError: If the task is not found.
        """
        self.get_task_by_id(task_id).status = TaskStatus.COMPLETE
        self._db.fetch_data(task_id, to_do="COMPLETE")

    def get_all_tasks(self) -> List[tuple]:
        """
        Get all the tasks of database.
        
        Returns:
            List of tuples. Each tuple represents the data of the task.
        """
        return self._db.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Task:
        """
        List all the tasks of database.
        
        Args:
            task_id (int): Task id of the task.
        Returns:
            Task instance.
        Raises:
            TaskNotFoundError if task_id is not found.
        """
        self._tasks = self.load_tasks_from_db()
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError("Task not found.")

    def modify_task(
        self,
        task_id: int,
        new_name: str,
        new_description: str,
        new_due_date: datetime,
        new_assignee: str,
        new_status: str,
        new_priority: str
    ) -> None:
        """
        Modify an existing task's attributes.

        Args:
            task_id (int): The ID of the task to modify.
            new_name (str, optional): New name for the task.
            new_description (str, optional): New description for the task.
            new_due_date (datetime, optional): New due date for the task.
            new_assignee (str, optional): New assignees for the task.
            new_status (TaskStatus, optional): New status for the task.
            new_priority (TaskPriority, optional): New priority for the task.
            new_categories (List[str], optional): New categories for the task.
            new_status (str, optional): New status for the task.
            new_priority (str, optional): New priority for the task.

        """
        task = self.get_task_by_id(task_id)

        if new_name:
            task.name = new_name
        if new_description:
            task.description = new_description
        if new_due_date:
            task.due_date = new_due_date
        if new_assignee:
            task.assignee = new_assignee
        if new_status:
            task.status = new_status
        if new_priority:
            task.priority = new_priority

        self._db.fetch_data(task_id, to_do="MODIFY", task=task)
