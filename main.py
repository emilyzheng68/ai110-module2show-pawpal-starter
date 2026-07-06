from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create an owner
    owner = Owner(name="Emily", preferences={"max_hours_per_day": 4})

    # Create pets
    biscuit = Pet(name="Biscuit", species="Golden Retriever")
    whiskers = Pet(name="Whiskers", species="Cat")

    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    # Add tasks with different times/priorities
    biscuit.add_task(Task(
        description="Morning walk",
        duration=30,
        priority="high",
        frequency="daily",
        time="08:00"
    ))
    biscuit.add_task(Task(
        description="Feeding",
        duration=10,
        priority="high",
        frequency="daily",
        time="09:00"
    ))
    whiskers.add_task(Task(
        description="Litter box cleaning",
        duration=10,
        priority="medium",
        frequency="daily",
        time="09:00"  # same time as Biscuit's feeding, to test conflict detection
    ))
    whiskers.add_task(Task(
        description="Playtime",
        duration=20,
        priority="low",
        frequency="weekly",
        time="18:00"
    ))

    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()

    # --- Original plan + conflicts ---
    plan = scheduler.generate_plan(available_minutes=60)
    conflicts = scheduler.detect_conflicts(all_tasks)

    print(scheduler.explain_plan(plan))

    if conflicts:
        print("\nWarnings:")
        for warning in conflicts:
            print(warning)

    # --- Test filtering ---
    print("\n--- Filtering demo ---")
    biscuit_tasks = scheduler.filter_tasks(all_tasks, pet_name="Biscuit")
    print(f"Biscuit's tasks: {[t.description for t in biscuit_tasks]}")

    incomplete_tasks = scheduler.filter_tasks(all_tasks, completed=False)
    print(f"Incomplete tasks: {[t.description for t in incomplete_tasks]}")

    # --- Test recurring task completion ---
    print("\n--- Recurrence demo ---")
    morning_walk = biscuit.get_tasks()[0]
    print(f"Before completing: {morning_walk.description}, completed={morning_walk.completed}")

    next_task = scheduler.complete_task(morning_walk)

    print(f"After completing: {morning_walk.description}, completed={morning_walk.completed}")
    if next_task:
        print(f"New recurring task created: {next_task.description}, frequency={next_task.frequency}, completed={next_task.completed}")

    print(f"\nBiscuit now has {len(biscuit.get_tasks())} tasks (was 2, should now be 3).")


if __name__ == "__main__":
    main()