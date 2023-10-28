"""
db.py.

This is the script allowing for management and interaction
with a SQLite database.The module provides the SQLiteDB class
which facilitates tasks such as establishing connections,
logging database activities, and performing various database
operations.

The primary class, SQLiteDB, is designed to handle tasks specific
to a task manager application.This includes methods for adding,
removing, and updating tasks, among others.
"""

import logging
import os
import sqlite3
from typing import List, Type, Union

from .task import TaskData, TaskStatus


class SQLiteDB:
    """A class for managing tasks in a SQLite database."""

    def __init__(self, db_name: str = "task_manager.db") -> None:
        """Initialize the SQLiteDB object.

        Sets up the database connection and the logger for db operations.

        Args:
            db_name (str): Name of the db file. Default is "task_manager.db".
        """
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        if db_name == "file::memory:?cache=shared":
            self.db_name = db_name
        else:
            self.db_name = os.path.join(parent_dir, db_name)

        self.conn = None
        self.logger = self.setup_logger(
            os.path.join(parent_dir, "logs", "data_base.log")
        )

    def setup_logger(self, log_file: str) -> Type[logging.Logger]:
        """
        Set up a logger to write all actions in data base.

        Args:
            log_file (str): path where the log file is stored.

        Returns:
            Type[logging.Logger]: Logger object.
        """
        logger = logging.getLogger("task_manager_database")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def connect(self) -> None:
        """Connect to the data base."""
        try:
            self.conn = sqlite3.connect(self.db_name, uri=True)
            self.logger.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to database: {e}")

    def table_exists(self, table_name: str) -> bool:
        """
        Verify if the table already exists in data base.

        Args:
            table_name (str): Table name to check.

        Returns:
            bool: boolean that verify existance of table.
        """
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"  # noqa: E501
            )
            response = cursor.fetchone()
        except sqlite3.Error as e:
            self.logger.error(
                f"Error checking if table is already in data base: {e}"
            )
        finally:
            self.close_connection()

        if response is None:
            return False
        return True

    def create_table_tasks(self) -> None:
        """
        Create a table to initialize data base.

        Args:
            table_name (str): Table to be created.
        """
        try:
            self.connect()
            cursor = self.conn.cursor()
            create_table_sql = self.generate_sql_creation_statement()
            cursor.execute(create_table_sql)
            self.conn.commit()
            self.logger.info("Table tasks created successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error creating table: {e}")
        finally:
            self.close_connection()

    def insert_data(self, table_name: str, data: TaskData) -> Union[int, None]:
        """
        Insert new data in table.

        Args:
            table_name (str): Table where data is going to be inserted.
            data (Type[Task]): Task to be inserted in table.

        Returns:
            Type[Task]: Task id of new task inserted.
        """
        table_in_data_base = self.table_exists(table_name)
        if not table_in_data_base:
            self.create_table_tasks()
        task_id = None
        try:
            self.connect()
            cursor = self.conn.cursor()
            insert_sql = self.generate_sql_insert_statement(table_name)
            name = data["name"]
            description = data["description"]
            creation_date = data["creation_date"].strftime("%Y/%m/%d %H:%M:%S")
            due_date = data["due_date"].strftime("%Y/%m/%d %H:%M:%S")
            assignee = ", ".join(data["assignee"])
            status = data["status"].value
            priority = data["priority"].value
            category = (
                "" if not data["categories"] else " ".join(data["categories"])
            )

            cursor.execute(
                insert_sql,
                (
                    name,
                    description,
                    creation_date,
                    due_date,
                    assignee,
                    status,
                    priority,
                    category,
                ),
            )
            self.conn.commit()
            task_id = cursor.lastrowid
            self.logger.info("Data inserted successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error inserting data: {e}")
        finally:
            self.close_connection()
        return task_id

    def fetch_data(
        self, task_id: int, to_do: str = "COMPLETE", task=None
    ) -> None:
        """
        Modify task.

        It changes the status to COMPLETE by default.

        Args:
            task_id (int): Task id of task to be modified.
            to_do (str, optional): Action to be performed
            on the task. Defaults to "COMPLETE".
            task (_type_, optional): Task to be modified. Defaults to None.
        """
        try:
            self.connect()
            cursor = self.conn.cursor()
            if to_do == "COMPLETE":
                query = self.generate_sql_complete_statement()
                cursor.execute(query, (TaskStatus.COMPLETE.value, task_id))
                self.logger.info("Task completed successfully")
            elif to_do == "MODIFY":
                query = self.generate_sql_modify_statement()
                cursor.execute(
                    query, (task[0], task[1], task[2], task[3], task_id)
                )
                self.logger.info("Task modified successfully")
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching data: {e}")
        finally:
            self.close_connection()

    def remove_task(self, task_id: int) -> None:
        """
        Remove a task from the data base by its id.

        Args:
            task_id (int): Task id of the task to be removed.
        """
        try:
            self.connect()
            cursor = self.conn.cursor()
            remove_sql = self.generate_sql_remove_statement()
            cursor.execute(remove_sql, str(task_id))
            self.conn.commit()
            self.logger.info("Data removed successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error removing data: {e}")
        finally:
            self.close_connection()

    def get_all_tasks(self) -> List[tuple]:
        """
        Return all tasks stored in data base.

        Returns:
            List[tuple]: List of tuples. This list has all tasks in db.
                         Each tuple represents the data of a task.
        """
        data = None
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            data = cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Error getting all tasks: {e}")
        finally:
            self.close_connection()
        return data

    def close_connection(self) -> None:
        """Close connection of data base."""
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

    @staticmethod
    def generate_sql_creation_statement() -> str:
        """
        Generate the sql statement to create a table.

        Args:
            table_name: Table to be created.

        Returns:
            str: SQL statement.
        """
        create_table_sql = """
                                    CREATE TABLE tasks (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT,
                                        description TEXT,
                                        creation_date DATETIME,
                                        due_date DATETIME,
                                        assignee TEXT,
                                        status INTEGER,
                                        priority INTEGER,
                                        category TEXT
                                        )
                                                            """

        return create_table_sql

    @staticmethod
    def generate_sql_insert_statement(table_name: str) -> str:
        """
        Return SQL statement to insert a new data.

        Args:
            table_name: Table where the new data is going to be inserted.

        Returns:
            str: SQL statement.
        """
        if table_name == "tasks":
            insert_sql = """
            INSERT INTO tasks
            (name, description, creation_date, due_date,
            assignee, status, priority, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
        return insert_sql

    @staticmethod
    def generate_sql_remove_statement() -> str:
        """
        Return SQL statement to delete a task.

        Returns:
            str: SQL statement.
        """
        return """DELETE FROM tasks WHERE id = ?"""

    @staticmethod
    def generate_sql_complete_statement() -> str:
        """
        Return SQL statement to change the status of a task.

        Returns:
            str: SQL statement.
        """
        return """UPDATE tasks SET status = ? WHERE id = ?"""

    @staticmethod
    def generate_sql_modify_statement() -> str:
        """
        Return SQL statement to modifi a task.

        Args:
            str: SQL statement.
        """
        return """UPDATE tasks
                  SET  name = ?,
                       description = ?,
                       due_date = ?,
                       assignee = ?
                  WHERE id = ?"""
