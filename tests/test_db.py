# In progress
import pytest
from unittest.mock import Mock, MagicMock
from to_do_list_project.db import SQLiteDB

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
    def __init__(self, db_name: str, log_file: str) -> None:
        self.conn = mock_connection

@pytest.fixture
def mock_db():
    return MockSQliteDB("example.db", "example.log")

def test_create_table(mock_db):
    mock_db.create_table("table")


if __name__ == "__main__":
    pytest.main()