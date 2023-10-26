"""
test_task_manager.py

This script is dedicated to test all the functionalities from db.py file.
"""

from datetime import datetime, timedelta
import pytest

from to_do_list_project.task_manager import TaskManager, TaskStatus


@pytest.fixture
def task_manager():
    """Fixture to create and return a new TaskManager instance."""
    return TaskManager("tasks")


def test_add_task(task_manager: TaskManager) -> None:
    """
    Test if a task can be successfully added to the task manager.
    """
    due_date = datetime.now() + timedelta(days=1)
    result = task_manager.add_task(
        "Test Task", "Description", due_date, ["Edouard"]
    )
    assert result is None
    assert len(task_manager.tasks) == 1


def test_add_task_past_due_date(task_manager: TaskManager) -> None:
    """
    Test if a task with a past due date returns the appropriate error message.
    """
    due_date = datetime.now() - timedelta(days=1)
    result = task_manager.add_task(
        "Expired Task", "Description", due_date, ["Edouard"]
    )
    assert result == "Due date must be in the future."
    assert len(task_manager.tasks) == 0


def test_delete_task(task_manager: TaskManager) -> None:
    """
    Test if a task can be successfully deleted from the task manager.
    """
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description", due_date, ["Edouard"])
    task_id = list(task_manager.tasks.keys())[0]
    task_manager.delete_task(task_id)
    assert len(task_manager.tasks) == 0


def test_complete_task(task_manager: TaskManager) -> None:
    """
    Test if a task can be marked as complete in the task manager.
    """
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task(
        "Test Task", "Description", due_date, ["user@example.com"]
    )
    task_id = list(task_manager.tasks.keys())[0]
    task_manager.complete_task(task_id)
    assert task_manager.tasks[task_id].status == TaskStatus.COMPLETE


def test_modify_task(task_manager: TaskManager) -> None:
    """
    Test if the name of a task can be successfully modified in
    the task manager.
    """
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task(
        "Test Task", "Description", due_date, ["user@example.com"]
    )
    task_id = list(task_manager.tasks.keys())[0]
    task_manager.modify_task(task_id, name="Modified Task")
    assert task_manager.tasks[task_id].name == "Modified Task"


def test_send_notification(task_manager: TaskManager) -> None:
    """
    Test if a notification can be successfully sent for a task
    in the task manager.
    """
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task(
        "Test Task", "Description", due_date, ["user@example.com"]
    )
    task_id = list(task_manager.tasks.keys())[0]
    result = task_manager.send_notification(task_id, "recipient@example.com")
    assert result is None


def test_send_notification_invalid_task_id(task_manager: TaskManager) -> None:
    """
    Test the case when trying to send a notification for a non-existent
    task ID.
    """
    result = task_manager.send_notification(12345, "recipient@example.com")
    assert result == "Task ID not found"


def test_send_notification_invalid_email(task_manager: TaskManager) -> None:
    """
    Test the case when trying to send a notification to an invalid email
    address.
    """
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task(
        "Test Task", "Description", due_date, ["user@example.com"]
    )
    task_id = list(task_manager.tasks.keys())[0]
    result = task_manager.send_notification(task_id, "invalid_email")
    # Gérer le cas de l'e-mail invalide et retourner un message approprié
    assert result is None


def test_get_all_tasks(task_manager: TaskManager) -> None:
    """
    Test if all tasks can be successfully retrieved from the task manager.
    """
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task(
        "Test Task", "Description", due_date, ["user@example.com"]
    )
    assert len(task_manager.get_all_tasks()) == 1
