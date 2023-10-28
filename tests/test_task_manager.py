"""
test_task_manager.py

This script is dedicated to test all the functionalities from db.py file.
"""

from datetime import datetime, timedelta
import sqlite3
import pytest

from to_do_list_project.db import SQLiteDB
from to_do_list_project.task_manager import TaskManager, TaskStatus


@pytest.fixture
def task_manager() -> TaskManager:
    """Fixture to create and return a new TaskManager instance."""
    task_manager = TaskManager(SQLiteDB("file::memory:?cache=shared"))
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    yield task_manager
    conn.close()


def test_add_task(task_manager: TaskManager) -> None:
    """Test if a task can be added to the task manager."""
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description", due_date, ["Edouard"])
    assert len(task_manager._tasks) == 1


def test_add_task_past_due_date(task_manager: TaskManager) -> None:
    """Test if a task with a past due date raises the godd error."""
    due_date = datetime.now() - timedelta(days=1)

    with pytest.raises(ValueError, match="Due date must be a future date"):
        task_manager.add_task(
            "Expired Task", "Description", due_date, ["Edouard"]
        )

    assert len(task_manager._tasks) == 0


def test_delete_task(task_manager: TaskManager) -> None:
    """Test if a task can be deleted from the task manager."""
    due_date = datetime.now() + timedelta(days=1)
    task_id = task_manager.add_task(
        "Test Task", "Description", due_date, ["Edouard"]
    )
    assert len(task_manager._tasks) == 1
    task_manager.remove_task(task_id)
    assert len(task_manager._tasks) == 0


def test_complete_task(task_manager: TaskManager) -> None:
    """Test if a task can be marked as complete."""
    due_date = datetime.now() + timedelta(days=1)
    task_id = task_manager.add_task(
        "Test Task",
        "Description",
        due_date,
        ["user@example.com"],
        TaskStatus.IN_PROGRESS,
    )
    task_manager.complete_task(task_id)
    assert task_manager.get_task_by_id(task_id).status == TaskStatus.COMPLETE


def test_modify_task(task_manager: TaskManager) -> None:
    """
    Test if the name of a task can be successfully modified in
    the task manager.
    """
    due_date = datetime.now() + timedelta(days=1)
    task_id = task_manager.add_task(
        "Test Task", "Description", due_date, ["user@example.com"]
    )
    task_manager.modify_task(
        task_id, "Modified Task", "Description", due_date, ["user@example.com"]
    )
    assert task_manager.get_task_by_id(task_id).name == "Modified Task"


def test_get_all_tasks(task_manager: TaskManager) -> None:
    """Test if all tasks can be retrieved from the task manager."""
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task(
        "Test Task", "Description", due_date, ["user@example.com"]
    )
    print(task_manager.get_all_tasks())
    assert len(task_manager.get_all_tasks()) == 1
