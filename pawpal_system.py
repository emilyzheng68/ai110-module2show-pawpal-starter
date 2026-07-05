from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Task:
    description: str
    duration: int  # in minutes
    priority: str  # "high", "medium", "low"
    frequency: str  # "daily", "weekly", "once"
    time: Optional[str] = None  # preferred time (optional)
    completed: bool = False
    pet_name: Optional[str] = None  # Name of the pet this task belongs to

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        task.pet_name = self.name  # Set the pet_name in the task
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Retrieve all tasks for the pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, preferences: Optional[Dict[str, Any]] = None):
        self.name = name
        self.pets: List[Pet] = []
        self.preferences = preferences if preferences else {}

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority."""
        priority_order = {"high": 1, "medium": 2, "low": 3}
        return sorted(tasks, key=lambda task: priority_order[task.priority])

    def generate_plan(self, available_minutes: int) -> List[Task]:
        """Generate a prioritized daily plan based on available minutes."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = self.sort_by_priority(all_tasks)
        plan = []
        total_time = 0

        for task in sorted_tasks:
            if total_time + task.duration <= available_minutes:
                plan.append(task)
                total_time += task.duration
            else:
                break

        return plan

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect conflicts in the task schedule."""
        conflicts = []
        time_map = {}

        for task in tasks:
            if task.time:
                if task.time in time_map:
                    conflicts.append(
                        f"Conflict: Task '{task.description}' (Pet: {task.pet_name}) "
                        f"conflicts with Task '{time_map[task.time].description}' "
                        f"(Pet: {time_map[task.time].pet_name}) at {task.time}."
                    )
                else:
                    time_map[task.time] = task

        return conflicts

    def explain_plan(self, plan: List[Task]) -> str:
        """Explain the generated plan."""
        explanation = ["Daily Plan:"]
        for task in plan:
            explanation.append(
                f"- {task.description} (Pet: {task.pet_name}, Duration: {task.duration} mins, Priority: {task.priority})"
            )
        explanation.append("Tasks were included based on priority and available time.")
        return "\n".join(explanation)