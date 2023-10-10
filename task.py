#task.py

from datetime import datetime
from uuid import uuid4

class Task:
    def __init__(self, name: str, description: str, category: str = "General"):
        self.id = str(uuid4())  # Utilisation de l'UUID pour l'ID
        self.name = name
        self.description = description
        self.category = category
        self.created_at = datetime.now()
        self.is_done = False
#gg
    def mark_done(self):
        self.is_done = True

    def __str__(self):
        status = "Done" if self.is_done else "Not Done"
        return f"ID: {self.id}, Name: {self.name}, Description: {self.description}, Category: {self.category}, Status: {status}, Created At: {self.created_at}"
