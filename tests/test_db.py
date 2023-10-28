"""
test_db.py

This script is dedicated to test all the functionalities from db.py file.
"""

from datetime import datetime, timedelta
import sqlite3
from unittest.mock import Mock, patch
import pytest

from to_do_list_project.db import SQLiteDB
from to_do_list_project.task import TaskPriority, TaskStatus

task_1 = Mock(
    return_value={
        "name": "Clean",
        "description": "Clean room",
        "creation_date": "2023/11/12 10:00:00",
        "due_date": "2023/12/12 10:00:00",
        "assignee": "James",
        "status": "In Progress",
        "priority": "Medium",
        "category": "House",
    }
)


@pytest.fixture
def mock_db() -> None:
    """
    Pytest fixture that mocks the 'connect' method of the SQLiteDB class.
    """
    with patch.object(
        SQLiteDB, "connect", return_value=Mock()
    ) as mock_connect:
        yield mock_connect


@pytest.fixture
def db_manager() -> SQLiteDB:
    """Fixture to create and return a new SQlite instance."""
    db = SQLiteDB("file::memory:?cache=shared")
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    yield db
    conn.close()


def test_table_creation_and_existence(db_manager: SQLiteDB) -> None:
    """Test if a table can be added to the db."""
    table_name = "tasks"

    assert not db_manager.table_exists(table_name)
    db_manager.create_table_tasks()
    assert db_manager.table_exists(table_name)


def test_insert_data(db_manager: SQLiteDB):
    """Test if data can be inserted into the db."""
    table_name = "tasks"
    sample_task = {
        "name": "Test task",
        "description": "This is a test task.",
        "creation_date": datetime.now(),
        "due_date": datetime.now() + timedelta(days=1),
        "assignee": ["John Doe"],
        "status": TaskStatus.IN_PROGRESS,
        "priority": TaskPriority.MEDIUM,
        "categories": ["Work", "Important"],
    }

    task_id = db_manager.insert_data(table_name, sample_task)
    assert task_id is not None

    db_manager.connect()
    cursor = db_manager.conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE id=?", (task_id,))
    row = cursor.fetchone()
    db_manager.close_connection()

    assert row is not None
    assert row[1] == sample_task["name"]


def test_remove_task(db_manager: SQLiteDB):
    """Test if data can be inserted into the db."""
    table_name = "tasks"
    sample_task = {
        "name": "Test task",
        "description": "This is a test task.",
        "creation_date": datetime.now(),
        "due_date": datetime.now() + timedelta(days=1),
        "assignee": ["John Doe"],
        "status": TaskStatus.IN_PROGRESS,
        "priority": TaskPriority.MEDIUM,
        "categories": ["Work", "Important"],
    }

    task_id = db_manager.insert_data(table_name, sample_task)
    assert task_id is not None

    db_manager.remove_task(task_id)
    db_manager.connect()
    cursor = db_manager.conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE id=?", (task_id,))
    row = cursor.fetchone()
    db_manager.close_connection()

    assert row is None
