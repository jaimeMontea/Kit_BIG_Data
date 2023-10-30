"""
main.py.

This is the main driver script for the Task Manager application.
It provides a command-line interface where users can add, remove,
modify, and view tasks.
"""

from datetime import datetime
import logging
import os
from typing import Callable, Tuple, Type, Union

from tabulate import tabulate

from .task import TaskPriority, TaskStatus, Task
from .task_manager import TaskManager
from .task_manager import TaskNotFoundError


def setup_logger(log_file: str) -> Type[logging.Logger]:
    """
    Set up a logger to write all user actions.

    Args:
        log_file (str): path where the log file is stored.

    Returns:
        Type[logging.Logger]: Logger object.
    """
    logger = logging.getLogger("user_input")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
logger = setup_logger(os.path.join(parent_dir, "logs", "user_input.log"))


def validate_date(date_str: str) -> Tuple[bool, str]:
    """
    Validate a date string and return a datetime object if valid.
    
    Args:
        date_str (str): Date to be validated.
    Returns:
        Tuple[bool, str]: Tuple where the first value is a boolean representing if the test passed and
                          the second value representing the date validated.
    """
    try:
        due_date = datetime.strptime(date_str, "%Y/%m/%d")
        if due_date.date() < datetime.now().date():
            logger.error(
                "Wrong date format. Due date must be after present time."
            )
            return False, "Due date must be in the future."
        return True, due_date
    except ValueError:
        logger.error(
            "Wrong date format. Input data  need this format YYYY/MM/DD."
        )
        return False, "Invalid date format."


def validate_priority(
    priority_str: str,
) -> Tuple[bool, Union[str, TaskPriority]]:
    """
    Validate a priority.
    
    Args:
        priority_str (str): The priority of the task.

    Returns:
        Tuple[bool, str]: Tuple where the first value is a boolean representing if the test passed and
                          the second value representing the priority validated.
    """
    try:
        if not priority_str:
            return True, ""
        return True, TaskPriority[priority_str.upper().strip()]
    except KeyError:
        logger.error("Invalid priority value. Should be: LOW, MEDIUM or HIGH.")
        return False, "Invalid priority value. Use LOW, MEDIUM, or HIGH."

def validate_status(
    status_str: str,
) -> Tuple[bool, Union[str, TaskStatus]]:
    """
    Validate a Status.
    
    Args:
        status_str (str): The status of the task.

    Returns:
        Tuple[bool, str]: Tuple where the first value is a boolean representing if the test passed and
                          the second value representing the status validated.
    """
    try:
        if not status_str:
            return True, ""
        return True, TaskStatus[status_str.upper().replace(" ", "").strip()]
    except KeyError:
        logger.error("Invalid status value. Should be: START, IN_PROGRESS or COMPLETE.")
        return False, "Invalid status value. Use START, IN_PROGRESS, or COMPLETE."

def get_input(
    prompt: str, validator_func: Callable[[str], Tuple[bool, Union[int, str]]]
) -> Union[int, str]:
    """
    Repeatedly prompt the user for input until it passes a validation function.

    Args:
        prompt (str): The prompt displayed to the user.
        validator_func (function): A function that validates the user's input.
            It should return a tuple (bool, value), where bool indicates if the
            validation succeeded and value is the validated value or an error.
    Returns:
        value: The user's input after it has been validated.
    """
    while True:
        user_input = input(prompt)
        logger.info(f"Prompt: {prompt}, User input: {user_input}")
        is_valid, value = validator_func(user_input)
        if is_valid:
            return value
        print(value)

def add_task(task_manager: TaskManager) -> None:
    """
    Add a task.
    
    Args:
        task_manager (TaskManager): A TaskManager instance which control all task actions.
    """
    name = get_input(
        "Enter task name: ",
        lambda x: (bool(x), x if x else "Task name cannot be empty."),
    )
    description = get_input(
        "Enter task description: ",
        lambda x: (bool(x), x if x else "Task description cannot be empty."),
    )
    due_date = get_input("Enter due date (YYYY/MM/DD): ", validate_date)
    assignees = get_input(
        "Enter assignee: ",
        lambda x: (
            bool(x), x if x else "No Assignee"),
    )
    priority = get_input(
        "Enter task priority (LOW, MEDIUM, HIGH): ", validate_priority
    )
    categories = get_input(
        "Enter task category: ",
        lambda x: (
            bool(x), x if x else "No category",
        ),
    )

    try:
        Task(1, name, description, due_date, assignees, priority=priority, categories=categories) # Task instance created to capture any possible error.

        task_manager.add_task(
            name,
            description,
            due_date,
            assignees,
            priority=priority,
            categories=categories,
        )

        print(f"Task '{name}' added successfully.")

    except Exception as e:
        print(e)
        logger.error("Error when creating task: " + str(e))


def remove_task(task_manager: TaskManager) -> None:
    """
    Remove a task by its ID.
    
    Args:
        task_manager (TaskManager): A TaskManager instance which control all task actions.
    """
    try:
        task_id = int(input("Enter the task ID to remove: "))
    except ValueError:
        print("Please enter a valid integer for task ID.")
        logger.error("Input ID is not a valid integer.")
        return
    try:
        task_manager.remove_task(task_id)
        print("Task removed successfully.")
        logger.info("Task with ID {task_id} was removed.")
    except TaskNotFoundError:
        print("Task with given ID not found.")
        logger.error("Task with given ID not found.")


def complete_task(task_manager: TaskManager) -> None:
    """
    Mark a task as completed by its ID.
    
    Args:
        task_manager (TaskManager): A TaskManager instance which control all task actions.
    """
    try:
        task_id = int(input("Enter the task ID to mark as completed: "))
        task_manager.complete_task(task_id)
        print(f"Task with ID {task_id} marked as complete.")
        logger.info("Task with ID {task_id} marked as complete.")
    except TaskNotFoundError:
        print("Task with given ID not found.")
        logger.error("Task with ID {task_id} not found.")
    except ValueError:
        print("Please enter a valid integer for task ID.")
        logger.error("Task with ID {task_id} not a valid ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error("An error occurred: {e}")


def modify_task(task_manager) -> None:
    """
    Modify a task by its ID.
    
    Args:
        task_manager (TaskManager): A TaskManager instance which control all task actions.
    """
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
        logger.error(f"Task with ID {task_id} not found.")
        return

    name = input("Enter new name[Press enter to not change]: ")
    description = input("Enter new description[Press enter to not change]: ")
    due_date = input(
        "Enter new due_date (YYYY/MM/DD)[Press enter to not change]: "
    )

    due_date = datetime.strptime(due_date, "%Y/%m/%d") if due_date else due_date
    assignee = input("Enter new assignee[Press enter to not change]: ")
    status = get_input("Enter task status (Start, In Progress, Complete) [Press enter to not change]: ", validate_status)
    priority = get_input("Enter task priority (Low, Medium, High) [Press enter to not change]: ", validate_priority)

    try:
        task_manager.modify_task(task_id, name, description, due_date, assignee, status, priority)
        print("Task modified successfully.")
    except Exception as e:
        print(e)
        logger.error("Error when creating task: " + str(e))



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
        logger.error("Choice not between 1 and 6.")
        return False, "Please enter a number between 1 and 6."
    except ValueError:
        logger.error("Input not a valid integer")
        return False, "Please enter a valid integer."


def display_all_tasks(task_manager: TaskManager) -> None:
    """
    Display all tasks.
    
    Args:
        task_manager (TaskManager): A TaskManager instance which control all task actions.
    """
    tasks = task_manager.get_all_tasks()
    if tasks:
        columns = (
            "id",
            "name",
            "description",
            "creation_date",
            "due_date",
            "assignee",
            "status",
            "priority",
            "category",
        )
        print(
            tabulate(
                [columns] + tasks, headers="firstrow", tablefmt="fancy_grid"
            )
        )
    else:
        print("No tasks.")


def main(task_manager: TaskManager) -> None:
    """
    Run the Task Manager app.
    
    Args:
        task_manager (TaskManager): A TaskManager instance which control all task actions.
    """
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
    task_manager = TaskManager()
    main(task_manager)
