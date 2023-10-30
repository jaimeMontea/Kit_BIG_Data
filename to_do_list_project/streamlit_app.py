"""
streamlit_app.py.

This is the script launching the web UI of the Task Manager application.
It drives the UI of the Task Manager application using the
Streamlit framework.
"""

from datetime import date
import logging
import os
from typing import Type

import pandas as pd
import streamlit as st

from to_do_list_project.task import TaskData, TaskStatus, TaskPriority, Task
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
    - Modify Task: Modify tasks using their ID.
    """
    st.title("Task Manager")

    # Navigation
    menu = [
        "Home",
        "Create Task",
        "View Tasks",
        "Complete Task",
        "Delete Task",
        "Modify Task"
    ]
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
            "Status", [status for status in TaskStatus]
        )
        task_priority = st.selectbox(
            "Priority", [priority for priority in TaskPriority]
        )
        task_categories = st.text_input("Categories")

        if st.button("Submit"):
            new_task_data: TaskData = {
                "name": task_name,
                "description": task_description,
                "creation_date": date.today(),
                "due_date": task_due_date,
                "assignee": task_assignee,
                "status": TaskStatus(task_status),
                "priority": TaskPriority(task_priority),
                "categories": task_categories
            }

            logger.info(f"User Input to Create Task")
            logger.info(f"(Create) name: {task_name}")
            logger.info(f"(Create) description: {task_description}")
            logger.info(f"(Create) due_date: {task_due_date}")
            logger.info(f"(Create) assignee: {task_assignee}")
            logger.info(f"(Create) status: {task_status}")
            logger.info(f"(Create) priority: {task_priority}")
            logger.info(f"(Create) categories: {task_categories}")

            try:
                Task(1, task_name, task_description, task_due_date, task_assignee,
                     TaskStatus(task_status), TaskPriority(task_priority), task_categories) # Task instance created to capture any possible error.
                task_manager._db.insert_data("tasks", new_task_data)
                st.success("Task created successfully!")
                logger.info("Task created successfully.")
            except Exception as e:
                st.error(e)
                logger.error("Error when creating task: " + str(e))

    elif choice == "View Tasks":
        tasks = task_manager.get_all_tasks()
        if tasks:
            columns = (
                "Id",
                "Name",
                "Description",
                "Creation Date",
                "Due Date",
                "Assignee",
                "Status",
                "Priority",
                "Category",
            )
            table =  pd.DataFrame(tasks, columns=columns)
            table.replace({"Status": {i.value: i.name for i in TaskStatus}}, inplace=True)
            table.replace({"Priority": {i.value: i.name for i in TaskPriority}}, inplace=True)
            st.dataframe(table, hide_index=True)
        else:
            st.error("No tasks.")

    elif choice == "Complete Task":
        st.subheader("Mark a Task as Complete")
        tasks = task_manager.get_all_tasks()
        ids = [task[0] for task in tasks]
        task_id = st.selectbox("Task ID to Modify", ids)
        if st.button("Mark as Complete"):
            try:
                logger.info(f"User task id input (Complete Task): {task_id}")
                task_manager.complete_task(task_id)
                st.success(f"Task {task_id} marked as completed!")
                logger.info(f"Task {task_id} marked as completed")
            except Exception as e:
                st.write("Task ID not found.")
                logger.error("Error when marking task as completed: " + str(e))

    elif choice == "Delete Task":
        st.subheader("Delete a Task")
        tasks = task_manager.get_all_tasks()
        ids = [task[0] for task in tasks]
        task_id = st.selectbox("Task ID to Modify", ids)
        if st.button("Delete"):
            try:
                logger.info(f"User task id input (Delete Task): {task_id}")
                task_manager.remove_task(task_id)
                st.success(f"Task {task_id} deleted!")
                logger.info(f"Task {task_id} deleted")
            except Exception as e:
                st.error("Task ID not found.")
                logger.error("Error when deleting task: " + str(e))

    elif choice == "Modify Task":
        st.subheader("Modify a Task")
        tasks = task_manager.get_all_tasks()
        ids = [task[0] for task in tasks]
        task_id = st.selectbox("Task ID to Modify", ids)
        name = st.text_input("New Name to Modify [Leave Blank to not Modify]")
        description = st.text_input("New Description to Modify [Leave Blank to not Modify]")
        
        assignee = st.text_input("New Assignee to Modify [Leave Blank to not Modify]")
        status = st.selectbox("New Status to Modify [Leave Blank to not Modify]", [""] + [status for status in TaskStatus])
        priority = st.selectbox("New Priority to Modify [Leave Blank to not Modify]", [""] + [priority for priority in TaskPriority])

        to_change = st.checkbox('Modify Due Date')
        if to_change:
            due_date = st.date_input("New Due Date to Modify [Leave Blank to not Modify]")
        else:
            due_date = ''
        if st.button("Modify"):
            logger.info(f"User Input to Modify Task")
            logger.info(f"(Modify) id: {task_id}")
            logger.info(f"(Modify) name: {name}")
            logger.info(f"(Modify) description: {description}")
            logger.info(f"(Modify) assignee: {assignee}")
            logger.info(f"(Modify) status: {status}")
            logger.info(f"(Modify) priority: {priority}")
            if due_date:
                logger.info(f"(Modify) due_date: {due_date}")
            else:
                logger.info(f"(Modify) due_date: no input")
            try:
                task_manager.modify_task(task_id, name, description, due_date, assignee, status, priority)
                st.success(f"Task {task_id} modified!")
                logger.info(f"Task {task_id} modified!")
            except ValueError as e:
                st.error(e)
                logger.error("Error when modifying task: " + str(e))
            except Exception as e:
                st.error(e)
                logger.error("Error when modifying task: " + str(e))

def setup_logger(log_file: str) -> Type[logging.Logger]:
    """
    Set up a logger to write all user actions.

    Args:
        log_file (str): path where the log file is stored.

    Returns:
        Type[logging.Logger]: Logger object.
    """
    logger = logging.getLogger("streamlit_user_input")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    logger = setup_logger(os.path.join(parent_dir, "logs", "streamlit_user_input.log"))
    task_manager = TaskManager()
    main(task_manager)
