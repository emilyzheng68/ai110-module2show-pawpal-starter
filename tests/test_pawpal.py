from pawpal_system import Task, Pet, Owner, Scheduler


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


def test_sort_by_priority_orders_correctly():
    """Tasks should be sorted with high priority first, then medium, then low."""
    owner = Owner(name="Emily")
    scheduler = Scheduler(owner)

    tasks = [
        Task(description="Low task", duration=10, priority="low", frequency="once"),
        Task(description="High task", duration=10, priority="high", frequency="once"),
        Task(description="Medium task", duration=10, priority="medium", frequency="once"),
    ]

    sorted_tasks = scheduler.sort_by_priority(tasks)

    assert [t.priority for t in sorted_tasks] == ["high", "medium", "low"]


def test_recurring_task_creates_next_occurrence():
    """Completing a daily task should automatically create a new occurrence."""
    owner = Owner(name="Emily")
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    task = Task(
        description="Morning walk",
        duration=30,
        priority="high",
        frequency="daily"
    )
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.description == "Morning walk"
    assert len(pet.get_tasks()) == 2


def test_once_frequency_does_not_recur():
    """A one-time task should not generate a next occurrence when completed."""
    owner = Owner(name="Emily")
    pet = Pet(name="Whiskers", species="Cat")
    owner.add_pet(pet)

    task = Task(
        description="Vet visit",
        duration=60,
        priority="high",
        frequency="once"
    )
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_detect_conflicts_flags_duplicate_times():
    """The scheduler should flag two tasks scheduled at the same time."""
    owner = Owner(name="Emily")
    pet_a = Pet(name="Biscuit", species="Dog")
    pet_b = Pet(name="Whiskers", species="Cat")
    owner.add_pet(pet_a)
    owner.add_pet(pet_b)

    pet_a.add_task(Task(
        description="Feeding",
        duration=10,
        priority="high",
        frequency="daily",
        time="09:00"
    ))
    pet_b.add_task(Task(
        description="Litter box cleaning",
        duration=10,
        priority="medium",
        frequency="daily",
        time="09:00"
    ))

    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()
    conflicts = scheduler.detect_conflicts(all_tasks)

    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]


def test_detect_conflicts_no_conflict_when_times_differ():
    """No conflict should be flagged when tasks have different times."""
    owner = Owner(name="Emily")
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    pet.add_task(Task(
        description="Morning walk",
        duration=30,
        priority="high",
        frequency="daily",
        time="08:00"
    ))
    pet.add_task(Task(
        description="Feeding",
        duration=10,
        priority="high",
        frequency="daily",
        time="09:00"
    ))

    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()
    conflicts = scheduler.detect_conflicts(all_tasks)

    assert len(conflicts) == 0
