import logging
import os
import sqlite3
from typing import Type, bool

import task


class SQLiteDB():

    def __init__(self, db_name: str, log_file: str) -> None:
        path = os.path.dirname(os.path.abspath(__file__))

        self.db_name = os.path.join(path, db_name)
        self.conn = None 
        self.logger = self.setup_logger(os.path.join(path, 'logs', log_file))

    def setup_logger(self, log_file: str) -> Type[logging.Logger]: 
        logger = logging.getLogger("task_manager_database")
        if not len(logger.handlers):
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger


    def connect(self) -> None:
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.logger.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to database: {e}")

    def table_exists(self, table_name: str) -> bool:
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            response = cursor.fetchone()
        except sqlite3.Error as e:
            self.logger.error(f"Error checking if table is already in data base: {e}")
        finally: 
            self.close_connection()
        
        if response is None:
            return False
        else: 
            return True

    def create_table(self, table_name: str) -> None:
        try:
            self.connect()
            cursor = self.conn.cursor()
            create_table_sql = self.generate_sql_creation_statement(table_name)
            cursor.execute(create_table_sql)
            self.conn.commit()
            self.logger.info(f"Table {table_name} created successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error creating table: {e}")
        finally: 
            self.close_connection()

    def insert_data(self, table_name:str, data: Type[task.Task]) -> None:
        table_in_data_base = self.table_exists(table_name)
        if not table_in_data_base:
            self.create_table(table_name)

        try:
            self.connect()
            cursor = self.conn.cursor()
            insert_sql = self.generate_sql_insert_statement(table_name)
            id = str(data.id) 
            name = data.name
            description = data.description
            creation_date = data.creation_date.strftime("%Y/%m/%d %H:%M:%S")
            due_date = data.due_date.strftime("%Y/%m/%d %H:%M:%S")
            assignee = ', '.join(data.assignee)
            status = data.status.value
            priority = data.priority.value
            category = '' if not data.category else ''.join(data.category)

            cursor.execute(insert_sql, (id, name, description, creation_date, due_date, assignee, status, priority, category))
            self.conn.commit()
            self.logger.info("Data inserted successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error inserting data: {e}")
        finally: 
            self.close_connection()

    def fetch_data(self, task_id: int, to_do: str='COMPLETE') -> None:
        try:
            self.connect()
            cursor = self.conn.cursor()
            if to_do == 'COMPLETE':
                query = self.generate_sql_complete_statement()
            cursor.execute(query, (task.TaskStatus.COMPLETE.value, task_id))
            self.conn.commit()
            self.logger.info("Task completed successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching data: {e}")
            return None
        finally: 
            self.close_connection()

    def remove_task(self, task_id: int) -> int:
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

    def close_connection(self) -> None:
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

    def generate_sql_creation_statement(self, table_name: str) -> str:
        if table_name == 'tasks':
            create_table_sql = '''
                                    CREATE TABLE tasks (
                                        id INTEGER,
                                        name TEXT,
                                        description TEXT,
                                        creation_date DATETIME,
                                        due_date DATETIME,
                                        assignee TEXT,
                                        status TEXT,
                                        priority TEXT,
                                        category TEXT
                                        )
                                                            '''
        else: 
            create_table_sql = '''
                                    CREATE TABLE task_managers (
                                        id INTEGER PRIMARY KEY,
                                        task INTEGER
                                        )
                                                            '''
        return create_table_sql

    def generate_sql_insert_statement(self, table_name: str) -> str:
        if table_name == 'tasks':
            insert_sql = '''
                        INSERT INTO tasks
                        (id, name, description, creation_date, due_date, assignee, status, priority, category)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
        return insert_sql

    def generate_sql_remove_statement(self) -> str:
        remove_sql = '''DELETE FROM tasks WHERE id = ?'''
        return remove_sql

    def generate_sql_complete_statement(self) -> str:
        complete_sql = '''UPDATE tasks SET status = ? WHERE id = ?'''
        return complete_sql
 