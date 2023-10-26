"""
main.py.

This is the main driver script for the Task Manager application.
It provides a command-line interface where users can add, remove,
modify, and view tasks.
"""

from datetime import datetime
import logging
import os
from typing import Callable, Tuple, Union

from .task import TaskPriority
from .task_manager import TaskManager
from .task_manager import TaskNotFoundError


logger = logging.getLogger("Task Manager")


def setup_logging() -> None:
    """Set up logging configurations."""
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    log_file = os.path.join(parent_dir, "logs", "user_input.log")

    os.makedirs(os.path.join(parent_dir, "logs"), exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def validate_date(date_str: str) -> Tuple[bool, str]:
    """Validate a date string and return a datetime object if valid."""
    try:
        due_date = datetime.strptime(date_str, "%d-%m-%Y")
        if due_date.date() < datetime.now().date():
            return False, "Due date must be in the future."
        return True, due_date
    except ValueError:
        return False, "Invalid date format."


def validate_priority(
    priority_str: str,
) -> Tuple[bool, Union[str, TaskPriority]]:
    """Validate a priority."""
    try:
        return True, TaskPriority[priority_str.upper()]
    except KeyError:
        return False, "Invalid priority value. Use LOW, MEDIUM, or HIGH."


def get_input(
    prompt: str, validator_func: Callable[[str], Tuple[bool, Union[int, str]]]
) -> Union[int, str]:
    """
    Repeatedly prompt the user for input until it passes a validation function.

    Parameters:
    - prompt (str): The prompt displayed to the user.
    - validator_func (function): A function that validates the user's input.
      It should return a tuple (bool, value), where bool indicates if the
      validation succeeded and value is the validated value or an error message.

    Returns:
    - value: The user's input after it has been validated.
    """
    while True:
        user_input = input(prompt)
        is_valid, value = validator_func(user_input)
        if is_valid:
            return value
        print(value)


def add_task(task_manager: TaskManager) -> None:
    """Add a task."""
    name = get_input(
        "Enter task name: ",
        lambda x: (bool(x), x if x else "Task name cannot be empty."),
    )
    description = get_input(
        "Enter task description: ",
        lambda x: (bool(x), x if x else "Task description cannot be empty."),
    )
    due_date = get_input("Enter due date (DD-MM-YYYY): ", validate_date)
    assignees = get_input(
        "Enter assignees (comma separated): ",
        lambda x: (
            bool(x.split(",")),
            x.split(",") if x else "Assignees list cannot be empty.",
        ),
    )
    priority = get_input(
        "Enter task priority (LOW, MEDIUM, HIGH): ", validate_priority
    )
    categories = get_input(
        "Enter task categories (comma separated): ",
        lambda x: (
            bool(x.split(",")),
            x.split(",") if x else "Categories list cannot be empty.",
        ),
    )

    result = task_manager.add_task(
        name,
        description,
        due_date,
        assignees,
        priority=priority,
        categories=categories,
    )
    if result is None:
        print(f"Task '{name}' added successfully.")
    else:
        print(result)


def remove_task(task_manager: TaskManager) -> None:
    """Remove a task by its ID."""
    try:
        task_id = int(input("Enter the task ID to remove: "))
    except ValueError:
        print("Please enter a valid integer for task ID.")
        logger.error("Input ID is not a valid integer.")
        return
    try:
        task_manager.remove_task(task_id)
        print("Task removed successfully.")
    except TaskNotFoundError:
        print("Task with given ID not found.")
        logger.error("Task with given ID not found.")


def complete_task(task_manager: TaskManager) -> None:
    """Mark a task as completed by its ID."""
    try:
        task_id = int(input("Enter the task ID to mark as completed: "))
        task_manager.complete_task(task_id)
        print(f"Task with ID {task_id} marked as complete.")
    except TaskNotFoundError:
        print("Task with given ID not found.")
    except ValueError:
        print("Please enter a valid integer for task ID.")
    except Exception as e:
        print(f"An error occurred: {e}")


def modify_task(task_manager) -> None:
    """Modify a task by its ID."""
    try:
        task_id = int(input("Enter the task ID to modify: "))
    except ValueError:
        print("Please enter a valid integer for task ID.")
        logger.error("Input ID is not a valid integer")
        return

    tasks_list = task_manager.get_all_tasks()
    list_id = [task[0] for task in tasks_list]

    if task_id not in list_id:
        print("ID not found")

    name = input("Enter new name[Press enter to not change]: ")
    description = input("Enter new description[Press enter to not change]: ")
    due_date = input("Enter new due_date[Press enter to not change]: ")
    assignee = input("Enter new assignee[Press enter to not change]: ")
    task_manager.modify_task(task_id, name, description, due_date, assignee)


def choice_validator(user_input: str) -> Tuple[bool, Union[str, int]]:
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
        return False, "Please enter a number between 1 and 6."
    except ValueError:
        return False, "Please enter a valid integer."


def display_all_tasks(task_manager):
    """Display all tasks."""
    all_tasks_with_ids = task_manager.get_all_tasks()
    print(all_tasks_with_ids)


def main():
    """Run the Task Manager app."""
    setup_logging()
    task_manager = TaskManager("tasks.db")

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
