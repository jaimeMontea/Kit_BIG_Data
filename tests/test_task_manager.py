import pytest
from task_manager import TaskManager, Task, TaskStatus, TaskPriority
from datetime import datetime, timedelta


@pytest.fixture
def task_manager():
    return TaskManager()


def test_add_task(task_manager):
    due_date = datetime.now() + timedelta(days=1)
    result = task_manager.add_task(
        "Test Task", "Description", due_date, ["Edouard"])
    assert result is None
    assert len(task_manager.tasks) == 1


def test_add_task_past_due_date(task_manager):
    due_date = datetime.now() - timedelta(days=1)
    result = task_manager.add_task(
        "Expired Task", "Description", due_date, ["Edouard"])
    assert result == "Due date must be in the future."
    assert len(task_manager.tasks) == 0


def test_delete_task(task_manager):
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description", due_date, ["Edouard"])
    task_id = list(task_manager.tasks.keys())[0]
    task_manager.delete_task(task_id)
    assert len(task_manager.tasks) == 0


def test_complete_task(task_manager):
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description",
                          due_date, ["user@example.com"])
    task_id = list(task_manager.tasks.keys())[0]
    task_manager.complete_task(task_id)
    assert task_manager.tasks[task_id].status == TaskStatus.COMPLETE


def test_modify_task(task_manager):
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description",
                          due_date, ["user@example.com"])
    task_id = list(task_manager.tasks.keys())[0]
    task_manager.modify_task(task_id, name="Modified Task")
    assert task_manager.tasks[task_id].name == "Modified Task"


def test_send_notification(task_manager):
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description",
                          due_date, ["user@example.com"])
    task_id = list(task_manager.tasks.keys())[0]
    result = task_manager.send_notification(task_id, "recipient@example.com")
    assert result is None


def test_send_notification_invalid_task_id(task_manager):
    result = task_manager.send_notification(12345, "recipient@example.com")
    assert result == "Task ID not found"


def test_send_notification_invalid_email(task_manager):
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description",
                          due_date, ["user@example.com"])
    task_id = list(task_manager.tasks.keys())[0]
    result = task_manager.send_notification(task_id, "invalid_email")
    # Gérer le cas de l'e-mail invalide et retourner un message approprié
    assert result == None


def test_get_all_tasks(task_manager):
    due_date = datetime.now() + timedelta(days=1)
    task_manager.add_task("Test Task", "Description",
                          due_date, ["user@example.com"])
    assert len(task_manager.get_all_tasks()) == 1
