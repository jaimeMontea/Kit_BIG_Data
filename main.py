# main.py
from task_manager import TaskManager

if __name__ == "__main__":
    task_manager = TaskManager()

    while True:
        print("\n1: Add Task")
        print("2: Mark Task Done")
        print("3: Delete Task")
        print("4: Display Tasks")
        print("5: Quit")

        choice = input("Select an option: ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                category = input("Enter task category (optional, 'General' by default): ")
                task_manager.add_task(name, description, category)

            elif choice == '2':
                task_id = input("Enter task ID to mark as done: ")
                if not task_manager.mark_task_done_by_id(task_id):
                    print("Task ID not found.")

            elif choice == '3':
                task_id = input("Enter task ID to delete: ")
                task_manager.delete_task_by_id(task_id)

            elif choice == '4':
                print("Task List:")
                task_manager.display_tasks()

            elif choice == '5':
                break
            else:
                print("Invalid option, please try again.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
