from task_manager import TaskManager
from task import Task, TaskStatus, TaskPriority
from datetime import datetime

# Function to display menu options
def display_menu():
    print("\n--- Task Manager ---")
    print("Choose an option:")
    print("1: Add Task")
    print("2: Remove Task")
    print("3: Display All Tasks")
    print("4: Complete Task")
    print("5: Modify Task")
    print("6: Reset Task List")
    print("7: Send Notification (Email)")
    print("8: Exit")

# Function to add a task
def add_task(task_manager):
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    due_date_str = input("Enter due date (YYYY-MM-DD HH:MM:SS): ")

    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S')
        if due_date <= datetime.now():
            print("Due date must be in the future.")
            return
    except ValueError:
        print("Invalid date format.")
        return

    assignees = input("Enter assignees (comma separated): ").split(",")
    task_manager.add_task(name, description, due_date, assignees)
    print(f"Task '{name}' added successfully.")

# Function to remove a task
def remove_task(task_manager):
    try:
        task_id = int(input("Enter the task ID to remove: "))
        result = task_manager.delete_task(task_id)
        if result is None:
            print(f"Task with ID {task_id} removed.")
        else:
            print(result)
    except ValueError:
        print("Please enter a valid integer for task ID.")

# Function to display all tasks
def display_all_tasks(task_manager):
    tasks = task_manager.get_all_tasks()
    print("\n-- List of Tasks --")
    for task_id, task in tasks.items():
        print(f"ID: {task_id}, Name: {task.get_name()}, Status: {task.get_status().value}")

# Function to mark a task as complete
def complete_task(task_manager):
    try:
        task_id = int(input("Enter the task ID to mark as completed: "))
        result = task_manager.complete_task(task_id)
        if result is None:
            print(f"Task with ID {task_id} marked as complete.")
        else:
            print(result)
    except ValueError:
        print("Please enter a valid integer for task ID.")

# Main function
def main():
    task_manager = TaskManager()  # Initialize an instance of TaskManager

    while True:  # Main loop for the program
        print("\n--- Task Manager ---")
        print("Choose an option:")
        print("1: Add Task")
        print("2: Remove Task")
        print("3: Display All Tasks")
        print("4: Complete Task")
        print("5: Modify Task")
        print("6: Reset Task List")
        print("7: Send Notification (Email)")
        print("8: Exit")


        choice = input("Your choice: ")

        if choice == '1':  
            add_task(task_manager)  # Here you call your new add_task function
        elif choice == '2':
            remove_task(task_manager)
        elif choice == '3':
            display_all_tasks(task_manager)
        elif choice == '4':
            complete_task(task_manager)
        elif choice == '5':
            print("Feature to modify task is under development.")
        elif choice == '6':
            task_manager.reset_tasks()
            print("All tasks have been reset.")
        elif choice == '7':
            print("Feature to send email is under development.")
        elif choice == '8':
            print("Exiting the Task Manager.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
