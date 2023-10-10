#task_manager.py: This file would contain the TaskManager class, which manages a collection of tasks. 
#This class could have methods to add a task, delete a task, mark it as complete, etc.

import smtplib  # Import the smtplib library for sending emails
from email.mime.text import MIMEText  # Import MIMEText to format the email

# Define the TaskManager class
class TaskManager:

    # The constructor initializes an empty list to hold Task objects
    def __init__(self):
        self.tasks = []

    # Method to add a new task to the tasks list
    def add_task(self, task):
        self.tasks.append(task)  # Append the new Task object to the tasks list

    # Method to delete a task based on its ID
    def delete_task(self, task_id):
        for task in self.tasks:  # Loop through each Task object in the tasks list
            if task.get_id() == task_id:  # If the Task's ID matches the given ID
                self.tasks.remove(task)  # Remove the Task object from the tasks list
                return  # Exit the method
        print("Task with given ID not found.")  # Print a message if no matching Task is found

    # Method to display all tasks
    def display_tasks(self):
        for task in self.tasks:  # Loop through each Task object in the tasks list
            # Print some basic information about each Task
            print(f"ID: {task.get_id()}, Name: {task.get_name()}, Status: {task.get_status().value}")

    # Method to mark a task as complete based on its ID
    def complete_task(self, task_id):
        for task in self.tasks:  # Loop through each Task object in the tasks list
            if task.get_id() == task_id:  # If the Task's ID matches the given ID
                task.set_status(TaskStatus.COMPLETE)  # Set the Task's status to COMPLETE
                return  # Exit the method
        print("Task with given ID not found.")  # Print a message if no matching Task is found

    # Method to modify a task's attributes based on its ID
    def modify_task(self, task_id, name=None, description=None, due_date=None):
        for task in self.tasks:  # Loop through each Task object in the tasks list
            if task.get_id() == task_id:  # If the Task's ID matches the given ID
                if name:  # If a new name is provided
                    task.set_name(name)  # Set the Task's name to the new name
                if description:  # If a new description is provided
                    task.set_description(description)  # Set the Task's description to the new description
                if due_date:  # If a new due_date is provided
                    task.set_due_date(due_date)  # Set the Task's due_date to the new due_date
                return  # Exit the method
        print("Task with given ID not found.")  # Print a message if no matching Task is found

    # Method to reset (clear) all tasks
    def reset_tasks(self):
        self.tasks.clear()  # Clear all Task objects from the tasks list

    # Method to send an email notification for a task based on its ID
    def send_notification(self, task_id, email_address):
        for task in self.tasks:  # Loop through each Task object in the tasks list
            if task.get_id() == task_id:  # If the Task's ID matches the given ID
                # Create the email subject and body
                subject = f"Notification for Task: {task.get_name()}"
                body = f"Task {task.get_name()} is due on {task.get_due_date()}"

                # Create a MIMEText object to hold the email content
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = "your_email@example.com"
                msg["To"] = email_address

                # Send the email using smtplib
                with smtplib.SMTP("smtp.example.com", 587) as server:
                    server.login("your_email@example.com", "your_password")
                    server.send_message(msg)
                return  # Exit the method
        print("Task with given ID not found.")  # Print a message if no matching Task is found

