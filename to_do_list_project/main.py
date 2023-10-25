"""
main.py

This is the main driver script for the Task Manager application.
It provides a command-line interface where users can add, remove,
modify, and view tasks.
"""

from datetime import datetime
import logging
import os
from task import TaskPriority, TaskStatus  # Import the enumerations
from task_manager import TaskManager
from task_manager import TaskNotFoundError

# Initialize logging
logging.basicConfig(filename='task_manager.log', level=logging.INFO)
logger = logging.getLogger('Task Manager')

def setup_logging():
    """Set up logging configurations."""
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    log_file = os.path.join(parent_dir, 'logs', "user_input.log")
    
    # Create logs folder if it does not exist
    os.makedirs(os.path.join(parent_dir, 'logs'), exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def validate_date(date_str):
    """Validate a date string and return a datetime object if valid."""
    try:
        due_date = datetime.strptime(date_str, '%d-%m-%Y')
        if due_date.date() < datetime.now().date():
            return False, "Due date must be in the future."
        return True, due_date
    except ValueError:
        return False, "Invalid date format."

def validate_priority(priority_str):
    try:
        return True, TaskPriority[priority_str.upper()]
    except KeyError:
        return False, "Invalid priority value. Use LOW, MEDIUM, or HIGH."

def get_input(prompt, validator_func):
    """
    Repeatedly prompt the user for input until it passes a validation function.

    Parameters:
    - prompt (str): The prompt displayed to the user.
    - validator_func (function): A function that validates the user's input. It should return a tuple (bool, value),
      where bool indicates if the validation succeeded and value is the validated value or an error message.

    Returns:
    - value: The user's input after it has been validated.
    """
    while True:
        user_input = input(prompt)
        is_valid, value = validator_func(user_input)
        if is_valid:
            return value
        else:
            print(value)  # Display an error message
            # Logging error for validation failure can also be added here if needed


def add_task(task_manager):
    name = get_input("Enter task name: ", lambda x: (bool(x), x if x else "Task name cannot be empty."))
    description = get_input("Enter task description: ", lambda x: (bool(x), x if x else "Task description cannot be empty."))
    due_date = get_input("Enter due date (DD-MM-YYYY): ", validate_date)
    assignees = get_input("Enter assignees (comma separated): ", lambda x: (bool(x.split(',')), x.split(',') if x else "Assignees list cannot be empty."))
    priority = get_input("Enter task priority (LOW, MEDIUM, HIGH): ", validate_priority)
    categories = get_input("Enter task categories (comma separated): ", lambda x: (bool(x.split(',')), x.split(',') if x else "Categories list cannot be empty."))

    result = task_manager.add_task(name, description, due_date, assignees, priority=priority, categories=categories)
    if result is None:
        print(f"Task '{name}' added successfully.")
    else:
        print(result)

def remove_task(task_manager):
    task_id = int(input("Enter the task ID to remove: "))
    try:
        result = task_manager.remove_task(task_id)
        print("Task removed successfully.")
    except TaskNotFoundError:
        print("Task with given ID not found.")

def complete_task(task_manager):
    """Mark a task as completed by its ID."""
    while True:
        try:
            task_id = int(input("Enter the task ID to mark as completed: "))
            logger.info(f"task_id input to be completed: {task_id}")
            result = task_manager.complete_task(task_id)
            if result is None:
                print(f"Task with ID {task_id} marked as complete.")
                break
            else:
                print(result)
        except ValueError:
            print("Please enter a valid integer for task ID.")
            logger.error(f"Input ID is not a valid integer")

def modify_task(task_manager):
    task_id = input("Enter the task ID to modify: ")
    try:
        task = task_manager.get_task_by_id(int(task_id))
    except TaskNotFoundError:
        print("Task not found.")
        return  # Exit the function if no task is found

    name = get_input(f"Current Name: {task.name}. Enter new task name (leave blank to keep unchanged): ", lambda x: (True, x))
    description = get_input(f"Current Description: {task.description}. Enter new task description (leave blank to keep unchanged): ", lambda x: (True, x))
    due_date = get_input(f"Current Due Date: {task.due_date.strftime('%d-%m-%Y')}. Enter new due date (DD-MM-YYYY, leave blank to keep unchanged): ", validate_date)
    assignees_input = get_input(f"Current Assignees: {','.join(task.assignee)}. Enter new assignees (comma separated, leave blank to keep unchanged): ", lambda x: (True, [] if x.strip() == '' else x.split(",")))

    assignees = assignees_input if assignees_input != [] else task.assignee

    task_manager.modify_task(int(task_id), name or task.name, description or task.description, due_date or task.due_date, assignees)
    print(f"Task with ID {task_id} modified successfully.")


def choice_validator(user_input):
    """
    Validate the user's choice.

    Parameters:
    - user_input (str): The user's input.

    Returns:
    - tuple: (is_valid (bool), value (str or int))
    """
    try:
        choice = int(user_input)
        if choice >= 1 and choice <= 6:
            return True, choice
        else:
            return False, "Please enter a number between 1 and 6."
    except ValueError:
        return False, "Please enter a valid integer."

def display_all_tasks(task_manager):
    all_tasks_with_ids = task_manager._tasks
    if not all_tasks_with_ids:
        print("No tasks to display.")
        return

    print("\n--- All Tasks ---")
    for task_id, task in all_tasks_with_ids.items():
        print(f"Task ID: {task_id}")  # Display task ID
        print(f"Task Name: {task.name}")
        print(f"Task Description: {task.description}")
        print(f"Due Date: {task.due_date.strftime('%d-%m-%Y')}")
        print(f"Assignee: {', '.join(task.assignee)}")
        print(f"Status: {task.status}")  # Since you've defined __str__ for the enum, it should print nicely
        print(f"Priority: {task.priority}")  # Same as above
        print(f"Categories: {', '.join(task.categories)}")
        print("=" * 40)  # separator

def main():
    """Main function that runs the Task Manager app."""
    setup_logging()  # Initialize logging settings
    task_manager = TaskManager('tasks.db')
    
    
    while True:
        print("\n--- Task Manager ---")
        print("Choose an option:")
        print("1: Add Task")
        print("2: Remove Task")
        print("3: Display All Tasks")
        print("4: Complete Task")
        print("5: Modify Task")
        print("6: Exit")

        choice = get_input("Your choice: ", choice_validator)
        
        if choice == 1:
            add_task(task_manager)
        elif choice == 2:
            remove_task(task_manager)
        elif choice == 3:
            display_all_tasks(task_manager)
        elif choice == 4:
            complete_task(task_manager)
        elif choice == 5:
            modify_task(task_manager)
        elif choice == 6:
            print("Exiting the Task Manager.")
            break

if __name__ == "__main__":
    main()
