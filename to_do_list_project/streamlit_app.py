import streamlit as st
from task import Task, TaskStatus, TaskPriority
from db import SQLiteDB
from datetime import datetime

# Set up the SQLite database
database = SQLiteDB("tasks.db")


def main():
    st.title("Task Manager")

    # Navigation
    menu = ["Home", "Create Task", "View Tasks",
            "Complete Task", "Delete Task"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to Task Manager")
        st.write("Navigate using the sidebar to manage tasks.")

    elif choice == "Create Task":
        st.subheader("Create a New Task")

        task_name = st.text_input("Task Name")
        task_description = st.text_area("Description")
        task_due_date = st.date_input("Due Date")
        task_assignee = st.text_input("Assignee")
        task_status = st.selectbox(
            "Status", [status.value for status in TaskStatus])
        task_priority = st.selectbox(
            "Priority", [priority.value for priority in TaskPriority])
        task_categories = st.text_input("Categories (comma-separated)")

        if st.button("Submit"):
            new_task = Task(
                name=task_name,
                description=task_description,
                due_date=task_due_date,
                assignee=[task_assignee],
                status=TaskStatus(task_status),
                priority=TaskPriority(task_priority),
                categories=task_categories.split(',')
            )
            database.insert_data('tasks', new_task)
            st.success("Task created successfully!")

    elif choice == "View Tasks":
        st.subheader("Existing Tasks")
        # Logic to retrieve and display tasks from the database

    elif choice == "Complete Task":
        st.subheader("Mark a Task as Complete")
        task_id = st.number_input("Task ID", min_value=0)
        if st.button("Mark as Complete"):
            # Logic to mark the task as complete
            database.fetch_data(task_id, to_do="COMPLETE")
            st.success(f"Task {task_id} marked as complete!")

    elif choice == "Delete Task":
        st.subheader("Delete a Task")
        task_id = st.number_input("Task ID to Delete", min_value=0)
        if st.button("Delete"):
            # Logic to delete the task from the database
            database.remove_task(task_id)
            st.success(f"Task {task_id} deleted!")


if __name__ == "__main__":
    main()
