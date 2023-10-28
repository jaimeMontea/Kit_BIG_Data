"""
test_main.py

This script is dedicated to test all the functionalities from main.py file.
"""

from datetime import datetime, timedelta
import logging
import sqlite3
from typing import Any, Tuple, Union
from unittest.mock import call, MagicMock, Mock, patch, ANY
import pytest

from to_do_list_project.db import SQLiteDB
from to_do_list_project.main import (
    add_task,
    choice_validator,
    complete_task,
    display_all_tasks,
    get_input,
    main,
    modify_task,
    remove_task,
    validate_date,
    validate_priority,
)
from to_do_list_project.task_manager import (
    TaskManager,
    TaskPriority,
    TaskStatus,
)


@pytest.fixture
def task_manager() -> TaskManager:
    """Fixture to create and return a new TaskManager instance."""
    task_manager = TaskManager(SQLiteDB("file::memory:?cache=shared"))
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    yield task_manager
    conn.close()


@pytest.fixture
def task_manager_with_tasks() -> [TaskManager, Any]:
    """Fixture to create a new TaskManager instance with tasks."""
    task_manager = TaskManager(SQLiteDB("file::memory:?cache=shared"))
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)

    curent_date = datetime.now() + timedelta(days=1)

    task_manager.add_task(
        "Test Task",
        "Description",
        curent_date,
        ["user@example.com"],
        TaskStatus.IN_PROGRESS,
        TaskPriority.MEDIUM,
        ["Category1"],
    )

    yield task_manager, [
        (
            1,
            "Test Task",
            "Description",
            curent_date,
            ["user@example.com"],
            TaskStatus.IN_PROGRESS,
            TaskPriority.MEDIUM,
            ["Category1"],
        )
    ]
    conn.close()


@pytest.mark.parametrize(
    "input_val, expected_result",
    [
        ("1", (True, 1)),
        ("3", (True, 3)),
        ("7", (False, "Please enter a number between 1 and 6.")),
        ("0", (False, "Please enter a number between 1 and 6.")),
        ("a", (False, "Please enter a valid integer.")),
    ],
)
def test_choice_validator(input_val, expected_result) -> None:
    """Test if validator is logging error."""
    assert choice_validator(input_val) == expected_result


def test_log_message_for_invalid_range() -> None:
    """Test if validator is preventing choices outside 1 to 6."""
    with patch.object(logging.getLogger("user_input"), "error") as mock_log:
        choice_validator("7")
        mock_log.assert_called_with("Choice not between 1 and 6.")


def test_log_message_for_invalid_integer() -> None:
    """Test if validator is preventing choices having wrong type."""
    with patch.object(logging.getLogger("user_input"), "error") as mock_log:
        choice_validator("a")
        mock_log.assert_called_with("Input not a valid integer")


def test_add_task(task_manager: TaskManager) -> None:
    """Test if inputs are taken into account when adding task."""
    mock_get_input_values = [
        ("TaskName", "TaskName"),
        ("TaskDesc", "TaskDesc"),
        (
            datetime.now() + timedelta(days=1),
            datetime.now() + timedelta(days=1),
        ),
        ("John,Smith", ["John", "Smith"]),
        (TaskPriority.HIGH, TaskPriority.HIGH),
        ("Work,Project", ["Work", "Project"]),
    ]

    mock_get_input = Mock(
        side_effect=[val[1] for val in mock_get_input_values]
    )

    with patch("builtins.print") as mock_print, patch(
        "to_do_list_project.main.get_input", mock_get_input
    ):
        add_task(task_manager)

    mock_get_input.assert_has_calls(
        [
            call("Enter task name: ", ANY),
            call("Enter task description: ", ANY),
            call("Enter due date (YYYY/MM/DD): ", ANY),
            call("Enter assignees (comma separated): ", ANY),
            call("Enter task priority (LOW, MEDIUM, HIGH): ", ANY),
            call("Enter task categories (comma separated): ", ANY),
        ]
    )

    assert mock_print.call_count == 2
    mock_print.assert_any_call("Task 'TaskName' added successfully.")


def test_remove_task_successful(
    task_manager_with_tasks: [TaskManager, Any]
) -> None:
    """Test if remove task display successful."""
    with patch("to_do_list_project.main.input", return_value="1"), patch(
        "to_do_list_project.main.print"
    ) as mock_print, patch(
        "to_do_list_project.main.logger.info"
    ) as mock_logger_info:
        remove_task(task_manager_with_tasks[0])

        mock_print.assert_called_once_with("Task removed successfully.")
        mock_logger_info.assert_called_once_with(
            "Task with ID {task_id} was removed."
        )


def test_display_all_tasks_with_no_tasks(task_manager: TaskManager) -> None:
    """Test if display no tasks for user."""
    with patch("builtins.print") as print_mock:
        display_all_tasks(task_manager)

    print_mock.assert_called_once_with("No tasks.")


def test_display_all_tasks_with_tasks(
    task_manager_with_tasks: [TaskManager, Any]
) -> None:
    """Test if display all tasks for user."""
    formatted_tasks = []
    for task in task_manager_with_tasks[1]:
        formatted_task = (
            task[0],
            task[1],
            task[2],
            (datetime.now()).strftime("%Y/%m/%d %H:%M:%S"),
            task[3].strftime("%Y/%m/%d %H:%M:%S"),
            task[4][0],
            task[5].value,
            task[6].value,
            task[7][0],
        )
        formatted_tasks.append(formatted_task)

    columns = (
        "id",
        "name",
        "description",
        "creation_date",
        "due_date",
        "assignee",
        "status",
        "priority",
        "category",
    )

    with patch("builtins.print") as print_mock, patch(
        "to_do_list_project.main.tabulate"
    ) as tabulate_mock:
        display_all_tasks(task_manager_with_tasks[0])

    print("Actual call args to tabulate:", tabulate_mock.call_args)
    print("Actual call args to tabulate:", [columns] + formatted_tasks)

    tabulate_mock.assert_any_call(
        [columns] + formatted_tasks,
        headers="firstrow",
        tablefmt="fancy_grid",
    )
    print_mock.assert_called_once_with(tabulate_mock.return_value)


def test_complete_task_successful(
    task_manager_with_tasks: [TaskManager, Any]
) -> None:
    """Test if complete task is displayed successfully."""
    with patch("to_do_list_project.main.input", return_value="1"), patch(
        "to_do_list_project.main.print"
    ) as mock_print:
        complete_task(task_manager_with_tasks[0])

        mock_print.assert_called_once_with(
            "Task with ID 1 marked as complete."
        )


def test_modify_task_calls_modify_task() -> None:
    """Test if task_manager.modify_task is called correctly."""
    mock_task_manager = MagicMock()
    mock_task_manager.get_all_tasks.return_value = [
        (
            1,
            "Existing task",
            "Existing description",
            "Existing date",
            "Existing assignee",
        )
    ]

    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "New Name",
            "New Description",
            "New Date",
            "New Assignee",
        ],
    ):
        modify_task(mock_task_manager)

    mock_task_manager.modify_task.assert_called_once_with(
        1, "New Name", "New Description", "New Date", "New Assignee"
    )


def test_validate_date_valid_future_date() -> None:
    """Test that a valid future date string is correctly identified."""
    future_date = (datetime.now() + timedelta(days=5)).strftime("%Y/%m/%d")
    valid, response = validate_date(future_date)
    assert valid
    assert response.date() == (datetime.now() + timedelta(days=5)).date()


def test_validate_priority_valid_values() -> None:
    """Test that valid priority values are correctly identified."""
    for valid_priority in ["LOW", "MEDIUM", "HIGH", "low", "medium", "high"]:
        valid, response = validate_priority(valid_priority)
        assert valid
        assert response == TaskPriority[valid_priority.upper()]


class NoMoreInputs(Exception):
    """Raised when there are no more mock inputs."""


def mock_get_input(*args, **kwargs):
    """Mock inputs."""
    if not mock_get_input.values:
        raise NoMoreInputs
    return mock_get_input.values.pop(0)


@pytest.mark.parametrize(
    "mock_input_values",
    [(["1", "Some Task Details", "6"])],
)
def test_main(monkeypatch, capsys, mock_input_values):
    """
    Test the main Task Manager app loop based on mocked user input.
    """
    monkeypatch.setattr(
        "to_do_list_project.task_manager.TaskManager", lambda: None
    )
    monkeypatch.setattr("to_do_list_project.main.get_input", mock_get_input)
    mock_get_input.values = mock_input_values

    try:
        main()
    except NoMoreInputs:
        pass

    captured = capsys.readouterr()
    captured_output = captured.out
    assert "Choose an option" in captured_output
    assert "Add Task" in captured_output
    assert "Remove Task" in captured_output
    assert "Display All Tasks" in captured_output
    assert "Complete Task" in captured_output
    assert "Modify Task" in captured_output
    assert "Exit" in captured_output


def simple_validator(input_str: str) -> Tuple[bool, Union[int, str]]:
    """Simple validation function that checks if input is 'valid'."""
    if input_str == "valid":
        return True, "valid"
    return False, "Invalid input. Try again."


@pytest.mark.parametrize(
    "mock_inputs, expected_output, expected_return",
    [
        (["valid"], "", "valid"),
        (["invalid", "valid"], "Invalid input. Try again.\n", "valid"),
    ],
)
def test_get_input(
    monkeypatch, capsys, mock_inputs, expected_output, expected_return
):
    """
    Test the get_input function by simulating various user input scenarios.
    """
    monkeypatch.setattr("builtins.input", mock_get_input)
    mock_get_input.values = mock_inputs

    result = get_input("Enter a value: ", simple_validator)

    captured = capsys.readouterr()
    assert captured.out == expected_output
    assert result == expected_return
