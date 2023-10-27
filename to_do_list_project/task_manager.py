"""
task_manager.py.

This module provides functionalities to manage tasks
using an SQLite database. It primarily contains the
`TaskManager` class that enables operations like
loading tasks from the database, adding new tasks,
removing tasks, marking tasks as complete, listing
all tasks, and modifying tasks.

Classes:
    - DatabaseConnectionError: Raised when there's a
      failure connecting to the database.
    - TaskNotFoundError: Raised when a specified
      task is not found in the manager.
    - TaskManager: The main class to manage
      tasks with methods to handle CRUD operations
      and other utility functionalities related to tasks.
"""

from datetime import datetime
from typing import List

from .db import SQLiteDB
from .task import Task, TaskData, TaskStatus, TaskPriority


class DatabaseConnectionError(Exception):
    """Exception raised when the database connection fails."""


class TaskNotFoundError(Exception):
    """Exception raised when a task is not found in the manager."""


class TaskManager:
    """
    A management system for tasks using an SQLite database.

    This class provides methods to handle the CRUD
    operations and other utility functionalities
    related to tasks.
    """

    def __init__(self, db_name: str) -> None:
        """
        Initialize the TaskManager object.

        Args:
            db_name (str): Name of the database.

        Raises:
            DatabaseConnectionError: If the database connection fails.
        """
        try:
            self._db = SQLiteDB(db_name)
        except Exception as e:
            raise DatabaseConnectionError(
                "Failed to connect to the database."
            ) from e

        self._tasks = []
        self.load_tasks_from_db()

    def load_tasks_from_db(self) -> None:
        """Load all tasks from database."""
        try:
            all_tasks = self._db.get_all_tasks()
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
                    task = Task(
                        task_id,
                        name,
                        description,
                        datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S"),
                        assignee.split(","),
                        TaskStatus[status],
                        TaskPriority[priority],
                        categories.split(","),
                    )
                    self._tasks.append(task)
        except Exception as e:
            print(f"Exception occurred: {e}")

    def add_task(
        self,
        name: str,
        description: str,
        due_date: datetime,
        assignee: List[str],
        status: TaskStatus = TaskStatus.IN_PROGRESS,
        priority: TaskPriority = TaskPriority.MEDIUM,
        categories: List[str] = None,
    ) -> int:
        """Add task to database."""
        task_data: TaskData = {
            "name": name,
            "description": description,
            "creation_date": datetime.now(),
            "due_date": due_date,
            "assignee": assignee,
            "status": status,
            "priority": priority,
            "categories": categories if categories is not None else []
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
            categories
        )
        self._tasks.append(task)
        print(len(self._tasks))
        print("Tasks after adding a new task:", self._tasks)
        return task_id

    def remove_task(self, task_id: int) -> None:
        """Remove task from database."""
        print(f"Tasks before attempting removal: {self._tasks}")

        self._db.remove_task(task_id)

        for index, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[index]

        print(f"Tasks after removal: {self._tasks}")

    def complete_task(self, task_id: int) -> None:
        """
        Mark a task as complete.

        Raises:
            TaskNotFoundError: If the task is not found.
        """
        self._db.fetch_data(task_id, to_do="COMPLETE")

    def list_all_tasks(self) -> List[Task]:
        """List all the tasks of database."""
        return self._tasks

    def get_task_by_id(self, task_id: int) -> Task:
        """List all the tasks of database."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError("Task not found.")

    def get_all_tasks(self) -> List[tuple]:
        """Get all the tasks of database."""
        return self._db.get_all_tasks()

    def modify_task(
        self,
        task_id: int,
        new_name: str,
        new_description: str,
        new_due_date: datetime,
        new_assignee: List[str],
    ) -> None:
        """
        Modify an existing task's attributes.

        Args:
            task_id (int): The ID of the task to modify.
            new_name (str, optional): New name for the task.
            new_description (str, optional): New description for the task.
            new_due_date (datetime, optional): New due date for the task.
            new_assignee (List[str], optional): New assignees for the task.
            new_status (TaskStatus, optional): New status for the task.
            new_priority (TaskPriority, optional): New priority for the task.
            new_categories (List[str], optional): New categories for the task.

        Raises:
            TaskNotFoundError: If the task is not found.
        """
        tasks_list = self._db.get_all_tasks()

        for index, task in enumerate(tasks_list):
            if task_id == task[0]:
                name = tasks_list[index][1]
                description = tasks_list[index][2]
                due_date = tasks_list[index][3]
                assignee = tasks_list[index][4]

        if new_name:
            name = new_name
        if new_description:
            description = new_description
        if new_due_date:
            due_date = new_due_date
        if new_assignee:
            assignee = new_assignee

        data = name, description, due_date, assignee

        self._db.fetch_data(task_id, to_do="MODIFY", task=data)
