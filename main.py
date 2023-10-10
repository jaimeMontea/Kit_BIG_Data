from task_manager import TaskManager  # Assuming task_manager.py contains a TaskManager class
from task import Task  # Assuming task.py contains a Task class

def main():
    task_manager = TaskManager()  # Initialize the TaskManager
    
    while True:
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
            # Add a new task
            task_name = input("Enter task name: ")
            task_desc = input("Enter task description: ")
            description = input("Enter additional details for the task: ")
            due_date = input("Enter due date (leave blank for none): ")
            assignee = input("Enter assignee (leave blank for none): ")
            
            new_task = Task(task_name, task_desc, description, due_date, assignee)  # Create new Task object
            task_manager.add_task(new_task)  # Add task to TaskManager
            print(f"Task '{task_name}' added successfully.")

        elif choice == '2':
            # Remove a task
            task_id = int(input("Enter the task ID to remove: "))
            task_manager.remove_task(task_id)
            print(f"Task with ID {task_id} removed.")

        elif choice == '3':
            # Display all tasks
            tasks = task_manager.get_all_tasks()
            print("\n-- List of Tasks --")
            for task in tasks:
                print(task)

        elif choice == '4':
            # Mark a task as completed
            task_id = int(input("Enter the task ID to mark as completed: "))
            task_manager.complete_task(task_id)
            print(f"Task with ID {task_id} marked as complete.")

        elif choice == '5':
            # Modify a task (this is a placeholder, replace with your own logic)
            print("Feature to modify task is under development.")

        elif choice == '6':
            # Reset all tasks
            task_manager.reset_tasks()
            print("All tasks have been reset.")

        elif choice == '7':
            # Send an email notification (this is a placeholder, replace with your own logic)
            print("Feature to send email is under development.")

        elif choice == '8':
            # Exit the application
            print("Exiting the Task Manager.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
