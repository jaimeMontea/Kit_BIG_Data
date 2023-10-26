from datetime import datetime
from typing import List
from db import SQLiteDB  # Make sure to import specific exceptions if available
from task import Task, TaskStatus, TaskPriority

class DatabaseConnectionError(Exception):
    """Exception raised when the database connection fails."""
    pass

class TaskNotFoundError(Exception):
    """Exception raised when a task is not found in the manager."""
    pass

class TaskManager:

    def __init__(self, db_name: str):
        """
        Initialize the TaskManager object.
        Args:
            db_name (str): Name of the database.
        
        Raises:
            DatabaseConnectionError: If the database connection fails.
        """
        try:
            self._db = SQLiteDB(db_name)
        except Exception as e:
            raise DatabaseConnectionError("Failed to connect to the database.") from e
        self._tasks = {}
        self.load_tasks_from_db()

    def load_tasks_from_db(self):
        """
        Load tasks from the database into the _tasks dictionary.
        """
        try:
            print("Trying to connect to DB...")  # Debug line
            self._db.connect()
            print("Connected to DB.")  # Debug line

            cursor = self._db.conn.cursor()
            print("Cursor created.")  # Debug line

            cursor.execute("SELECT * FROM tasks")
            print("SQL query executed.")  # Debug line

            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")  # Debug line

            self._db.close_connection()
            print("DB connection closed.")  # Debug line

            for row in rows:
                task_id, name, description, creation_date, due_date, assignee, status, priority, categories = row
                print(f"task_id: {task_id}, name: {name}, description: {description}, creation_date: {creation_date}, due_date: {due_date}, assignee: {assignee}, status: {status}, priority: {priority}, categories: {categories}")

                # Create Task object
                task = Task(name, description, datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S'), 
                            assignee.split(','), TaskStatus[status], TaskPriority[priority], categories.split(','))

                self._tasks[task_id] = task
                print(f"Task added to _tasks: {task_id}")  # Debug line

            print(f"Tasks after loading from DB: {self._tasks}")  # Debug line

        except Exception as e:
            print(f"Exception occurred: {e}")  # Debug line



    def add_task(self, name: str, description: str, due_date: datetime, assignee: List[str], 
                 status: TaskStatus = TaskStatus.IN_PROGRESS, 
                 priority: TaskPriority = TaskPriority.MEDIUM, 
                 categories: List[str] = None) -> int:
        """
        Add a new task to the manager.
        Returns:
            int: The ID of the newly created task.
        """
        task = Task(name, description, due_date, assignee, status, priority, categories)
        task_id = self._db.insert_data('tasks', task)
        self._tasks[task_id] = task
        
        print("Tasks after adding a new task:", self._tasks) # Debug line
        return task_id

    def remove_task(self, task_id: int):
        print(f"Tasks before attempting removal: {self._tasks}")

        # Remove the task from the database
        self._db.remove_task(task_id)

        # Remove the task from the _tasks dictionary if it exists
        if task_id in self._tasks:
            del self._tasks[task_id]

        print(f"Tasks after removal: {self._tasks}")
        return None

    def list_all_tasks(self) -> List[Task]:
        """
        List all tasks managed by the TaskManager.
        Returns:
            List[Task]: List of all tasks.
        """
        return list(self._tasks.values())

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get a task by its ID.
        Returns:
            Task: The task object.
        Raises:
            TaskNotFoundError: If the task is not found.
        """
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError("Task not found.")
        return task

    def modify_task(self, task_id: int, 
                    new_name: str = None, 
                    new_description: str = None, 
                    new_due_date: datetime = None,
                    new_assignee: List[str] = None,
                    new_status: TaskStatus = None,
                    new_priority: TaskPriority = None,
                    new_categories: List[str] = None):
        """
        Modify an existing task's attributes.
        Args:
            task_id (int): The ID of the task to modify.
            new_name (str, optional): New name for the task.
            new_description (str, optional): New description for the task.
            new_due_date (datetime, optional): New due date for the task.
            new_assignee (List[str], optional): New assignees for the task.
            new_status (TaskStatus, optional): New status for the task.
            new_priority (TaskPriority, optional): New priority for the task.
            new_categories (List[str], optional): New categories for the task.
        Raises:
            TaskNotFoundError: If the task is not found.
        """
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError("Task not found.")
        
        if new_name:
            task.name = new_name
        if new_description:
            task.description = new_description
        if new_due_date:
            task.due_date = new_due_date
        if new_assignee:
            task.assignee = new_assignee
        if new_status:
            task.status = new_status
        if new_priority:
            task.priority = new_priority
        if new_categories:
            task.categories = new_categories

        self._db.fetch_data(task_id, to_do="MODIFY", task=task) # This line was modified by Jaime

