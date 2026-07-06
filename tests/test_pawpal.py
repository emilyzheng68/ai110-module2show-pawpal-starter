from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    """Marking a task complete should set completed to True."""
    task = Task(
        description="Feed the cat",
        duration=10,
        priority="high",
        frequency="daily"
    )
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_task_count():
    """Adding a task to a Pet should increase its task count."""
    pet = Pet(name="Biscuit", species="Golden Retriever")
    assert len(pet.get_tasks()) == 0

    task = Task(
        description="Morning walk",
        duration=30,
        priority="high",
        frequency="daily"
    )
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1