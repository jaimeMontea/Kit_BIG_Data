"""
test_streamlit.py

This script is dedicated to test all the functionalities
from test_streamlit.py file, our graphical interface.
"""

from datetime import datetime, timedelta
import sqlite3
from unittest.mock import patch

import pytest

from to_do_list_project.db import SQLiteDB
from to_do_list_project.streamlit_app import main
from to_do_list_project.task import TaskPriority, TaskStatus
from to_do_list_project.task_manager import TaskManager


@pytest.fixture
def task_manager() -> TaskManager:
    """Fixture to create and return a new TaskManager instance."""
    task_manager = TaskManager(SQLiteDB("file::memory:?cache=shared"))
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    yield task_manager
    conn.close()


def test_display_home(task_manager: TaskManager) -> None:
    """Test the main interface of the Task Manager for 'Home' option."""
    with patch(
        "to_do_list_project.streamlit_app.st.sidebar.selectbox",
        return_value="Home",
    ):
        with patch(
            "to_do_list_project.streamlit_app.st.subheader"
        ) as mock_subheader:
            with patch(
                "to_do_list_project.streamlit_app.st.write"
            ) as mock_write:
                main(task_manager)

                mock_subheader.assert_called_once_with(
                    "Welcome"
                )
                mock_write.assert_called_once_with(
                    "Navigate using the sidebar to manage tasks."
                )


def test_display_create_task(task_manager: TaskManager) -> None:
    """Test the main interface of the Task Manager for 'Create Task' option."""
    with patch(
        "to_do_list_project.streamlit_app.st.sidebar.selectbox",
        return_value="Create Task",
    ):
        with patch(
            "to_do_list_project.streamlit_app.st.subheader"
        ) as mock_subheader:
            with patch("to_do_list_project.streamlit_app.st.text_input"):
                with patch("to_do_list_project.streamlit_app.st.text_area"):
                    with patch(
                        "to_do_list_project.streamlit_app.st.date_input"
                    ):
                        with patch(
                            "to_do_list_project.streamlit_app.st.selectbox"
                        ):
                            main(task_manager)

                            mock_subheader.assert_called_once_with(
                                "Create a New Task"
                            )


def test_display_task_created_successfully(task_manager: TaskManager) -> None:
    """
    This test simulates the user selecting the 'Create Task'
    option from the sidebar,filling out the task details,
    clicking the 'Submit' button, and checks if the
    "Task created successfully" message is displayed.
    """
    with patch(
        "to_do_list_project.streamlit_app.st.sidebar.selectbox",
        return_value="Create Task",
    ):
        with patch(
            "to_do_list_project.streamlit_app.st.text_input",
            return_value="Sample Task",
        ):
            with patch(
                "to_do_list_project.streamlit_app.st.text_area",
                return_value="Sample Description",
            ):
                with patch(
                    "to_do_list_project.streamlit_app.st.date_input",
                    return_value=(datetime.now() + timedelta(days=1)).date(),
                ):
                    with patch(
                        "to_do_list_project.streamlit_app.st.selectbox",
                        side_effect=[
                            TaskStatus.COMPLETE.value,
                            TaskPriority.HIGH.value,
                        ],
                    ):
                        with patch(
                            "to_do_list_project.streamlit_app.st.button",
                            return_value=True,
                        ):
                            with patch.object(task_manager._db, "insert_data"):  # noqa: E501
                                with patch(
                                    "to_do_list_project.streamlit_app.st.success"  # noqa: E501
                                ) as mock_success:
                                    main(task_manager)
                                    mock_success.assert_called_once_with(
                                        "Task created successfully!"
                                    )


def test_display_complete_task(task_manager: TaskManager) -> None:
    """
    Test the main interface of the Task Manager for the 'Complete Task' option.
    """
    with patch(
        "to_do_list_project.streamlit_app.st.sidebar.selectbox",
        return_value="Complete Task",
    ):
        with patch(
            "to_do_list_project.streamlit_app.st.subheader"
        ) as mock_subheader:
            with patch("to_do_list_project.streamlit_app.st.number_input"):
                with patch("to_do_list_project.streamlit_app.st.button"):
                    main(task_manager)
                    mock_subheader.assert_called_once_with(
                        "Mark a Task as Complete"
                    )


def test_display_delete_task(task_manager: TaskManager) -> None:
    """
    Test the main interface of the Task Manager for the 'Delete Task' option.
    """
    with patch(
        "to_do_list_project.streamlit_app.st.sidebar.selectbox",
        return_value="Delete Task",
    ):
        with patch(
            "to_do_list_project.streamlit_app.st.subheader"
        ) as mock_subheader:
            with patch("to_do_list_project.streamlit_app.st.number_input"):
                with patch("to_do_list_project.streamlit_app.st.button"):
                    main(task_manager)
                    mock_subheader.assert_called_once_with("Delete a Task")


def test_display_view_tasks(task_manager: TaskManager) -> None:
    """
    Test the main interface of the Task Manager for the 'View Tasks' option.
    """
    with patch(
        "to_do_list_project.streamlit_app.st.sidebar.selectbox",
        return_value="View Tasks",
    ):
        with patch(
            "to_do_list_project.streamlit_app.st.subheader"
        ) as mock_subheader:
            main(task_manager)
            mock_subheader.assert_called_once_with("Existing Tasks")
