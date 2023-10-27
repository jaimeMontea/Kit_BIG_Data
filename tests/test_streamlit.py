"""
test_streamlit.py

This script is dedicated to test all the functionalities
from test_streamlit.py file, our graphical interface.
"""

from unittest.mock import patch

from to_do_list_project.streamlit_app import main


def test_display_home() -> None:
    """Basic test for streamlit app's main function."""
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
                main()

                mock_subheader.assert_called_once_with(
                    "Welcome to Task Manager"
                )
                mock_write.assert_called_once_with(
                    "Navigate using the sidebar to manage tasks."
                )
