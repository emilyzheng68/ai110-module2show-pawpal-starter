# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Core actions a user should be able to perform:
1. Add a pet and its owner's basic info
2. Add/edit care tasks with duration and priority
3. Generate and view a daily schedule based on priority and time constraints

Owner

Attributes: name, pets (list of Pet objects), preferences (e.g. preferred start time, max hours per day)
Methods: add_pet(), get_all_tasks()

Pet

Attributes: name, species, tasks (list of Task objects)
Methods: add_task(), get_tasks()

Task

Attributes: description, duration (minutes), priority (high/medium/low), time (optional preferred time), frequency (daily/weekly/once), completed (bool)
Methods: mark_complete()

Scheduler

Attributes: owner (reference to the Owner whose tasks it schedules)
Methods: generate_plan(available_minutes), sort_by_priority(), detect_conflicts(), explain_plan()

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I asked Copilot to review pawpal_system.py for missing relationships or bottlenecks. It flagged that Task had no reference back to the Pet it belongs to, which would make it hard to trace tasks once they're pulled together across multiple pets for scheduling (e.g., in generate_plan or explain_plan). I added a `pet_name` field to Task to fix this.

Copilot also raised points about priority tie-breaking, conflict definitions, and recurring task logic — I'm deferring those to Phase 2 and Phase 4 since they depend on logic I haven't written yet, rather than being skeleton-level design flaws. I decided not to add a two-way Owner↔Scheduler reference or a structured preferences class, since those would add complexity without a clear benefit for this project's scope.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers two main constraints: task priority (high/medium/low) and available time (in minutes). generate_plan() sorts tasks by priority first, then greedily fills the available time budget, so higher-priority tasks are always favored when time is limited. I decided priority and time mattered most because they're the two things a busy pet owner cares about most directly — what's most important to get done, and how much time they actually have. Owner preferences (like max hours per day) exist as a data structure but aren't yet used directly in scheduling logic — that's a possible improvement for later.



**b. Tradeoffs**

My conflict detection only checks for exact matching time strings (e.g., "09:00" vs "09:00"), rather than detecting overlapping durations (e.g., a 30-minute task starting at 08:45 overlapping a 09:00 task). This is a simpler and more predictable approach for a small personal pet-scheduling app, where tasks are usually assigned to fixed time slots rather than flexible windows. A more robust version would parse times and compare intervals, but that adds complexity that isn't necessary at this scale.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project: brainstorming the four core classes and their responsibilities, generating a Mermaid.js UML diagram from my design, scaffolding the initial class skeletons, reviewing my skeleton for missing relationships (which led me to add pet_name to Task), and suggesting algorithm simplifications for filtering and recurrence logic. The most helpful prompts were specific ones that referenced my actual files (e.g., "based on my skeleton in pawpal_system.py...") rather than generic questions, since they produced code that matched my existing design instead of a generic alternative.

**b. Judgment and verification**

I asked Copilot how to simplify filter_tasks and create_next_occurrence. Its filter_tasks suggestion (combining conditions into one list comprehension) was a genuine improvement, so I adopted it. However, its "simplified" create_next_occurrence actually changed the function's behavior — instead of returning a new Task object ready to attach to a Pet, it returned a datetime representing the next due date. That would have broken complete_task(), which expects a Task back so it can call pet.add_task(). I verified this by tracing through how complete_task() uses the return value, and decided to keep my original version since it matched the rest of my system's design.

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding tasks to a pet, sorting by priority, recurring task generation (daily and one-time), and conflict detection (both when conflicts exist and when they don't). These were important because they cover the core "smart" behaviors of the scheduler — if sorting or recurrence broke, the whole app's usefulness would break with it.

**b. Confidence**

I'm fairly confident (4/5) the scheduler works correctly for the cases I tested. If I had more time, I'd test edge cases like: an empty task list, a pet with no tasks at all, three or more tasks all conflicting at the same time, and tasks with missing/invalid time strings.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
