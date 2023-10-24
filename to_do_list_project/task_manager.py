from datetime import datetime
from typing import List, Union
from db import SQLiteDB
from task import Task, TaskStatus, TaskPriority


class TaskManager:
    """A manager for tasks that provides functionalities to interact with a persistent SQLite database."""

    def __init__(self, db_name: str):
        """
        Create a TaskManager instance connected to an SQLite database.

        Args:
            db_name: Name of the SQLite database file.
        """
        self._db = SQLiteDB(db_name)
        self._tasks = {}  # Stores tasks in-memory, indexed by task IDs for quick retrieval

    def add_task(self, name: str, description: str, due_date: datetime, assignees: List[str], 
                 status: TaskStatus = TaskStatus.IN_PROGRESS, priority: TaskPriority = TaskPriority.MEDIUM, 
                 categories: List[str] = None) -> Union[None, str]:
        """
        Add a new task to the manager.

        Args:
            name: Name of the task.
            description: Detailed description of the task.
            due_date: The date by which the task should be completed.
            assignees: Names of people responsible for the task.
            status: The current status of the task. Defaults to IN_PROGRESS.
            priority: The importance level of the task. Defaults to MEDIUM.
            categories: Categories/tags associated with the task. Defaults to None.

        Returns:
            None if the task is successfully added, or an error message otherwise.
        """
        task = Task(name, description, due_date, assignees, status, priority, categories)
        task_id = self._db.insert_data('tasks', task)
        if task_id:
            self._tasks[task_id] = task
        else:
            return "Failed to add the task to the database."

    def get_task(self, task_id: int) -> Union[Task, None]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def complete_task(self, task_id: int) -> Union[None, str]:
        """Mark a task as complete."""
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETE
            if not self._db.update_task_status(task_id, TaskStatus.COMPLETE):
                return "Failed to update the task status in the database."
        else:
            return "Task not found."

    def remove_task(self, task_id: int) -> Union[None, str]:
        """Remove a task by its ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._db.remove_task(task_id)
        else:
            return "Task not found."

    def list_all_tasks(self) -> List[Task]:
        """List all managed tasks."""
        return list(self._tasks.values())

    def list_incomplete_tasks(self) -> List[Task]:
        """List tasks that are not marked as complete."""
        return [task for task in self._tasks.values() if task.status != TaskStatus.COMPLETE]
