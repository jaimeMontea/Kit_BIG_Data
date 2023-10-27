"""
test_db.py

This script is dedicated to test all the functionalities from db.py file.
"""

import sqlite3
from unittest.mock import Mock, patch
import pytest

from to_do_list_project.db import SQLiteDB

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
