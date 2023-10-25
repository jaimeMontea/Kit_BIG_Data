# In progress
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock
from to_do_list_project.db import SQLiteDB
import logging
import os
from to_do_list_project.task import Task, TaskStatus, TaskPriority, parse_date, format_date

task_1 = Mock(return_value={"id": 1, "name": "Clean", 
                            "description": "Clean room", "creation_date": "2023/11/12 10:00:00", 
                            "due_date": "2023/12/12 10:00:00", "assignee": "James", 
                            "status": "In Progress", "priority": "Medium", 
                            "category": "House"})

task_2 = Mock(return_value={"id": 2, "name": "Cook", 
                            "description": "Cook lunch", "creation_date": "2023/11/13 10:00:00", 
                            "due_date": "2023/12/13 10:00:00", "assignee": "James", 
                            "status": "In Progress", "priority": "Medium", 
                            "category": "House"})

task_3 = Mock(return_value={"id": 3, "name": "Buy", 
                            "description": "Buy lunch", "creation_date": "2023/11/13 10:00:00", 
                            "due_date": "2023/12/13 10:00:00", "assignee": "John", 
                            "status": "In Progress", "priority": "Medium", 
                            "category": "House"})

mock_connection = MagicMock()

class MockSQliteDB(SQLiteDB):
    def __init__(self) -> None:
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        self.db_name = os.path.join(parent_dir, ":memory:")
        self.conn = None
        self.logger = self.setup_logger(os.path.join(parent_dir, 'logs', 'test_data_base.log'))

    def setup_logger(self, log_file: str): 
        logger = logging.getLogger("task_manager_database")
        if not len(logger.handlers):
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

@pytest.fixture
def in_memory_db():
    return MockSQliteDB()

def test_create_table(mock_db):
    mock_db.create_table("tasks")


# def test_create_table_with_mock(mock):
#     db = SQLiteDB("test.db")
#     db.connect()

#     create_table_sql = """
#     CREATE TABLE IF NOT EXISTS test_table (
#         id INTEGER PRIMARY KEY,
#         name TEXT
#     );
#     """

#     mock_cursor = db.conn.cursor = Mock()
#     db.create_table("tasks")

#     # Verify that execute and commit were called
#     mock_cursor.execute.assert_called_with("tasks")
#     db.conn.commit.assert_called_once()

# def test_insert_data(mock_db, task_1):
#     mock_db.insert_data("tasks", task_1)


@pytest.fixture
def in_memory_db():
    db = SQLiteDB(":memory:")
    db.connect()
    yield db
    db.close_connection()
    
in_memory_db = SQLiteDB(":memory:")
def test_create_table():
    
    in_memory_db.create_table("tasks")

    # Check if the table was created
    cursor = in_memory_db.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';")
    result = cursor.fetchone()
    in_memory_db.close_connection()
    assert result is not None

def test_insert_data():
    due_date = datetime.now() + timedelta(days=1)
    assignee = ["Edouard"]
    task = Task("Dish", "Wash the dishes after dinner", due_date, assignee)

    in_memory_db = SQLiteDB(":memory:")
    in_memory_db.insert_data("tasks", task)

    cursor = in_memory_db.conn.cursor()
    cursor.execute("SELECT name FROM task WHERE name='Dish' AND assignee='Edouard';")
    result = cursor.fetchone()
    assert result is not None

if __name__ == "__main__":
    pytest.main()