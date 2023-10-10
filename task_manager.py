#task_manager.py

from typing import List
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, name: str, description: str, category: str = "General"):
        new_task = Task(name, description, category)
        self.tasks.append(new_task)

    def mark_task_done_by_id(self, task_id: str):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_done()
                return True
        return False

    def delete_task_by_id(self, task_id: str):
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def display_tasks(self):
        for task in self.tasks:
            print(task)
