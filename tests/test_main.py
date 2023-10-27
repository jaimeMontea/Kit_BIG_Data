"""
test_main.py

This script is dedicated to test all the functionalities from main.py file.
"""

from datetime import datetime, timedelta
import logging
import sqlite3
from unittest.mock import call, Mock, patch, ANY
import pytest

from to_do_list_project.db import SQLiteDB
from to_do_list_project.main import add_task, choice_validator
from to_do_list_project.task_manager import TaskManager, TaskPriority, TaskStatus


@pytest.fixture
def task_manager() -> TaskManager:
    """Fixture to create and return a new TaskManager instance."""
    task_manager = TaskManager(SQLiteDB("file::memory:?cache=shared"))
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    yield task_manager
    conn.close()


@pytest.mark.parametrize("input_val, expected_result", [
    ("1", (True, 1)),
    ("3", (True, 3)),
    ("7", (False, "Please enter a number between 1 and 6.")),
    ("0", (False, "Please enter a number between 1 and 6.")),
    ("a", (False, "Please enter a valid integer.")),
])
def test_choice_validator(input_val, expected_result) -> None:
    """Test if validator is logging error."""
    assert choice_validator(input_val) == expected_result


def test_log_message_for_invalid_range() -> None:
    """Test if validator is preventing choices outside 1 to 6."""
    with patch.object(logging.getLogger("user_input"), 'error') as mock_log:
        choice_validator("7")
        mock_log.assert_called_with("Choice not between 1 and 6.")


def test_log_message_for_invalid_integer() -> None:
    """Test if validator is preventing choices having wrong type."""
    with patch.object(logging.getLogger("user_input"), 'error') as mock_log:
        choice_validator("a")
        mock_log.assert_called_with("Input not a valid integer")


def test_add_task(task_manager: TaskManager) -> None:
    """Test if inputs are taken into account when adding task."""
    mock_get_input_values = [
        ("TaskName", "TaskName"),
        ("TaskDesc", "TaskDesc"),
        (
            datetime.now() + timedelta(days=1),
            datetime.now() + timedelta(days=1)
        ),
        ("John,Smith", ["John", "Smith"]),
        (TaskPriority.HIGH, TaskPriority.HIGH),
        ("Work,Project", ["Work", "Project"])
    ]

    mock_get_input = Mock(side_effect=[val[1]
                          for val in mock_get_input_values])

    with patch('builtins.print') as mock_print, \
            patch('to_do_list_project.main.get_input', mock_get_input):
        add_task(task_manager)

    mock_get_input.assert_has_calls([
        call("Enter task name: ", ANY),
        call("Enter task description: ", ANY),
        call("Enter due date (YYYY/MM/DD): ", ANY),
        call("Enter assignees (comma separated): ", ANY),
        call("Enter task priority (LOW, MEDIUM, HIGH): ", ANY),
        call("Enter task categories (comma separated): ", ANY),
    ])

    assert mock_print.call_count == 2
    mock_print.assert_any_call("Task 'TaskName' added successfully.")
