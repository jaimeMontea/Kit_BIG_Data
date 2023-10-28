"""
test_task.py

This script is dedicated to test all the functionalities from task.py file.
"""

from datetime import datetime, timedelta
import pytest

from to_do_list_project.task import (
    Task,
    TaskStatus,
    TaskPriority,
    parse_date,
    format_date,
)


def test_parse_date() -> None:
    """
    Check that the parse_date function returns a datetime object corresponding
    to the date string indicated
    """
    date_string = "31-10-2023"
    expected_date = datetime(2023, 10, 31)
    assert parse_date(date_string) == expected_date


def test_format_date() -> None:
    """
    Check that the format_date function returns a string corresponding to the
    date object indicated
    """
    date_obj = datetime(2023, 10, 31)
    expected_string = "31-10-2023"
    assert format_date(date_obj) == expected_string


def test_task_initialization() -> None:
    """
    Check that the Task object is initialized with the correct attributes
    """
    due_date = datetime.now() + timedelta(days=1)
    assignee = ["Edouard"]
    task = Task(1, "Dish", "Wash the dishes after dinner", due_date, assignee)
    assert task.name == "Dish"
    assert task.description == "Wash the dishes after dinner"
    time_difference = datetime.now() - task.creation_date
    assert abs(time_difference.total_seconds()) < 1
    assert task.assignee == assignee
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.priority == TaskPriority.MEDIUM
    assert not task.categories


def test_task_modification() -> None:
    """
    Check that the Task object attributes can be modified
    """
    due_date = datetime.now() + timedelta(days=1)
    assignee = ["Edouard"]
    task = Task(1, "Dish", "Wash the dishes after dinner", due_date, assignee)
    task.name = "laundry"
    assert task.name == "laundry"
    task.description = "Do the laundry"
    assert task.description == "Do the laundry"
    task.due_date = datetime.now() + timedelta(days=2)
    time_difference = datetime.now() + timedelta(days=2) - task.due_date
    assert abs(time_difference.total_seconds()) < 1
    task.assignee = ["Maxime"]
    assert task.assignee == ["Maxime"]
    task.status = TaskStatus.COMPLETE
    assert task.status == TaskStatus.COMPLETE
    task.priority = TaskPriority.HIGH
    assert task.priority == TaskPriority.HIGH
    task.categories = ["Cleaning"]
    assert task.categories == ["Cleaning"]


def test_invalid_task_name() -> None:
    """
    Check that the Task object raises an error when initialized or modified
    with an empty name
    """
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(1, "", "Wash the dishes after dinner", due_date, assignee)
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            2, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
        task.name = ""


def test_invalid_task_desciption() -> None:
    """
    Check that the Task object raises an error when initialized or modified
    with an empty description
    """
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(1, "Dish", "", due_date, assignee)
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            2, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
        task.description = ""


def test_invalid_task_due_date() -> None:
    """
    Check that the Task object raises an error when initialized or modified
    with a past due date
    """
    with pytest.raises(ValueError):
        due_date = datetime.now() - timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            1, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            2, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
        task.due_date = datetime.now() - timedelta(days=1)


def test_invalid_task_assignee() -> None:
    """
    Check that the Task object raises an error when initialized or modified
    with an invalid assignee list
    """
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard", 1]
        task = Task(
            1, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            2, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
        task.assignee = ["Edouard", 1]


def test_invalid_task_status() -> None:
    """
    Check that the Task object raises an error when initialized or modified
    with an invalid status
    """
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            1,
            "Dish",
            "Wash the dishes after dinner",
            due_date,
            assignee,
            status="In Progress",
        )
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            2, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
        task.status = "In Progress"


def test_invalid_task_priority() -> None:
    """
    Check that the Task object raises an error when initialized or modified
    with an invalid priority
    """
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            1,
            "Dish",
            "Wash the dishes after dinner",
            due_date,
            assignee,
            priority="Medium",
        )
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            1, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
        task.priority = "Medium"


def test_invalid_task_categories() -> None:
    """
    Check that the Task object raises an error when initialized or modified
    with an invalid categories list
    """
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            1,
            "Dish",
            "Wash the dishes after dinner",
            due_date,
            assignee,
            categories=["Cleaning", 1],
        )
    with pytest.raises(ValueError):
        due_date = datetime.now() + timedelta(days=1)
        assignee = ["Edouard"]
        task = Task(
            1, "Dish", "Wash the dishes after dinner", due_date, assignee
        )
        task.categories = ["Cleaning", 1]
