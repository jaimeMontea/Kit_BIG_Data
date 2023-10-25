#task_manager.py: This file would contain the TaskManager class, which manages a collection of tasks. 
#This class could have methods to add a task, delete a task, mark it as complete, etc.

from typing import List, Union
from task import Task, TaskStatus, TaskPriority
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import db

class TaskManager:

    # _next_id = 1 

    def __init__(self):
        # self.id = Task._next_id  
        # Task._next_id += 1  

        self.tasks = {}  # Initializing an empty dictionary to store Task objects
        self.data_base = db.SQLiteDB()

    # Add a new task by creating a Task object
    def add_task(self, name: str, description: str, due_date: datetime, assignee: List[str], 
                 status: TaskStatus = TaskStatus.IN_PROGRESS, 
                 priority: TaskPriority = TaskPriority.MEDIUM, 
                 category: List[str] = None) -> Union[None, str]:
        
        # Add the due_date validation here
        if due_date <= datetime.now():
            return "Due date must be in the future."
        
        new_task = Task(name, description, due_date, assignee, status, priority, category)
        # self.tasks[new_task.get_id()] = new_task -> TODO: modify with the rest of methods

        self.data_base.insert_data('tasks', new_task)

        return None

    # Add an existing task to the tasks dictionary
    def add_existing_task(self, task: Task) -> Union[None, str]:
        if not isinstance(task, Task):
            return "Only Task objects can be added"
        if task.get_id() in self.tasks:
            return "Task with the same ID already exists"
        self.tasks[task.get_id()] = task
        return None

    # Delete a task based on its ID
    def delete_task(self, task_id: int) -> Union[None, str]:
        if task_id not in self.tasks:
            return "Task ID not found"
        del self.tasks[task_id]

        self.data_base.remove_task(task_id)
        return None

    # Display all tasks
    def display_tasks(self) -> None:
        for task_id, task_obj in self.tasks.items():
            print(f"ID: {task_id}, Name: {task_obj.get_name()}, Status: {task_obj.get_status().value}")

    # Mark a task as complete
    def complete_task(self, task_id: int) -> Union[None, str]:
        if task_id not in self.tasks:
            return "Task ID not found"
        self.tasks[task_id].set_status(TaskStatus.COMPLETE)
        self.data_base.fetch_data(task_id)
        return None

    # Modify task attributes
    def modify_task(self, task_id: int, name=None, description=None, due_date=None) -> Union[None, str]:
        if task_id not in self.tasks:
            return "Task ID not found"
        task = self.tasks[task_id]
        if name:
            task.set_name(name)
        if description:
            task.set_description(description)
        if due_date:
            task.set_due_date(due_date)
        return None

    # Clear all tasks
    def reset_tasks(self) -> None:
        self.tasks.clear()

    # Send notification email for a task
    def send_notification(self, task_id: int, email_address: str) -> Union[None, str]:
        if task_id not in self.tasks:
            return "Task ID not found"
        task = self.tasks[task_id]
        subject = f"Notification for Task: {task.get_name()}"
        body = f"Task {task.get_name()} is due on {task.get_due_date()}"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "your_email@example.com"
        msg["To"] = email_address

        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.login("your_email@example.com", "your_password")
            server.send_message(msg)
        return None

    # Get all tasks
    def get_all_tasks(self) -> dict:
        return self.tasks

