from to_do_list_project.task import *

# task = Task(name="Wash dishes", description="Wash the dishes after dinner", due_date="2023-10-31",
#             assignee="John", status=TaskStatus.IN_PROGRESS, priority=TaskPriority.MEDIUM, category="Cleaning")
task = Task(name="Wash dishes", description="Wash the dishes after dinner",
            due_date=datetime(year=2023, month=10, day=31), assignee="John")


def test_task_creation():
    assert task.description == "Wash the dishes after dinner"
    # assert task.is_completed is False


# def test_task_completion():
#     task.complete()
#     assert task.is_completed is True


# def test_task_description_update():
#     task.update_description("Updated task description")
#     assert task.description == "Updated task description"
