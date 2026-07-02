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

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        pass

    def get_tasks(self) -> List[Task]:
        """Retrieve all tasks for the pet."""
        pass


class Owner:
    def __init__(self, name: str, preferences: Optional[Dict[str, Any]] = None):
        self.name = name
        self.pets: List[Pet] = []
        self.preferences = preferences if preferences else {}

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self, available_minutes: int) -> List[Task]:
        """Generate a prioritized daily plan based on available minutes."""
        pass

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority."""
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect conflicts in the task schedule."""
        pass

    def explain_plan(self, plan: List[Task]) -> str:
        """Explain the generated plan."""
        pass