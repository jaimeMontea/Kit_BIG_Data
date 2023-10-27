"""
test_db.py

This script is dedicated to test all the functionalities from db.py file.
"""

from datetime import datetime
from unittest.mock import Mock, patch
import pytest

from to_do_list_project.db import SQLiteDB
from to_do_list_project.task import Task

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

task_2 = Mock(
    return_value={
        "id": 2,
        "name": "Cook",
        "description": "Cook lunch",
        "creation_date": "2023/11/13 10:00:00",
        "due_date": "2023/12/13 10:00:00",
        "assignee": "James",
        "status": "In Progress",
        "priority": "Medium",
        "category": "House",
    }
)

task_3 = Mock(
    return_value={
        "id": 3,
        "name": "Buy",
        "description": "Buy lunch",
        "creation_date": "2023/11/13 10:00:00",
        "due_date": "2023/12/13 10:00:00",
        "assignee": "John",
        "status": "In Progress",
        "priority": "Medium",
        "category": "House",
    }
)

task_4 = Mock(
    return_value={
        "id": 3,
        "name": "Buy",
        "description": "Buy lunch",
        "creation_date": "2023/11/13 10:00:00",
        "due_date": datetime.strptime("2023-12-13 10:00:00", "%Y-%m-%d %H:%M:%S"),
        "assignee": "John",
        "status": "In Progress",
        "priority": "Medium",
        "category": "House",
    }
)

# @pytest.fixture
# def in_memory_db():
#     db = SQLiteDB(":memory:")
#     db.connect()
#     yield db
#     db.close_connection()

# # in_memory_db = SQLiteDB(":memory:")


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
def task() -> Task:
    """
    Pytest fixture that provides a predefined task instance.
    """
    return task_4


# def test_create_table(mock_db):
#     sqlite_db = SQLiteDB()
#     sqlite_db.create_table("tasks")
#     mock_db.assert_called_once()

# def test_insert_data(mock_db, task):
#     sqlite_db = SQLiteDB()
#     sqlite_db.insert_data("tasks", task)
#     cursor = mock_db.conn.cursor()
#     mock_db.query_all_data.call_count

#     cursor.execute("SELECT name FROM test_table WHERE name = ?", task)
#     result = cursor.fetchone()
#     print("Hereeeee3", mock_db.query_all_data.call_count)
#     assert result == task_1

#     mock_db.assert_called_once()

#     due_date = datetime.now() + timedelta(days=1)
#     assignee = ["Edouard"]
#     task = Task("Dish", "Wash the dishes after dinner", due_date, assignee)

#     in_memory_db = SQLiteDB(":memory:")
#     in_memory_db.insert_data("tasks", task)

#     cursor = in_memory_db.conn.cursor()
#      cursor.execute("SELECT name FROM task
#                     WHERE name='Dish' AND assignee='Edouard';")
#     result = cursor.fetchone()
#     assert result is not None


if __name__ == "__main__":
    pytest.main()
