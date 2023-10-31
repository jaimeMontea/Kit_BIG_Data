"""
streamlit_app.py.

This is the script launching the web UI of the Task Manager application.
It drives the UI of the Task Manager application using the
Streamlit framework.
"""

from datetime import datetime
from PIL import Image
import streamlit as st

from to_do_list_project.task import TaskData, TaskStatus, TaskPriority
from to_do_list_project.task_manager import TaskManager


def main(task_manager: TaskManager) -> None:
    """
    Drives the user interface for the Task Manager application using Streamlit.

    Features:
    - Home: Welcome page.
    - Create Task: Input form to add tasks to the database.
    - View Tasks: Display existing tasks.
    - Complete Task: Mark tasks as complete.
    - Delete Task: Remove tasks using their ID.
    """
    st.image(Image.open('assets/img/logo.png'))

    # Navigation
    menu = [
        "Home",
        "Create Task",
        "View Tasks",
        "Complete Task",
        "Delete Task",
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome")
        st.write("Navigate using the sidebar to manage tasks.")

    elif choice == "Create Task":
        st.subheader("Create a New Task")

        task_name = st.text_input("Task Name")
        task_description = st.text_area("Description")
        task_due_date = st.date_input("Due Date").strftime("%d-%m-%Y")
        task_assignee = st.text_input("Assignee")
        task_status = st.selectbox(
            "Status", [status.value for status in TaskStatus]
        )
        task_priority = st.selectbox(
            "Priority", [priority.value for priority in TaskPriority]
        )
        task_categories = st.text_input("Categories (comma-separated)")

        if st.button("Submit"):
            new_task: TaskData = {
                "name": task_name,
                "description": task_description,
                "creation_date": datetime.now(),
                "due_date": task_due_date,
                "assignee": [task_assignee],
                "status": TaskStatus(task_status),
                "priority": TaskPriority(task_priority),
                "categories": task_categories.split(",")
            }
            task_manager._db.insert_data("tasks", new_task)
            st.success("Task created successfully!")

    elif choice == "View Tasks":
        st.subheader("Existing Tasks")

    elif choice == "Complete Task":
        st.subheader("Mark a Task as Complete")
        task_id = st.number_input("Task ID", min_value=0)
        if st.button("Mark as Complete"):
            task_manager._db.fetch_data(task_id, to_do="COMPLETE")
            st.success(f"Task {task_id} marked as complete!")

    elif choice == "Delete Task":
        st.subheader("Delete a Task")
        task_id = st.number_input("Task ID to Delete", min_value=0)
        if st.button("Delete"):
            task_manager._db.remove_task(task_id)
            st.success(f"Task {task_id} deleted!")


if __name__ == "__main__":
    task_manager = TaskManager()
    main(task_manager)
