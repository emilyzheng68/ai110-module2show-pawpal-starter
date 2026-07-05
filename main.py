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
        time="09:00"  # intentionally same time as Biscuit's feeding, to test conflict detection
    ))
    whiskers.add_task(Task(
        description="Playtime",
        duration=20,
        priority="low",
        frequency="daily",
        time="18:00"
    ))

    # Generate a schedule
    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()

    plan = scheduler.generate_plan(available_minutes=60)
    conflicts = scheduler.detect_conflicts(all_tasks)

    print(scheduler.explain_plan(plan))

    if conflicts:
        print("\nWarnings:")
        for warning in conflicts:
            print(warning)


if __name__ == "__main__":
    main()