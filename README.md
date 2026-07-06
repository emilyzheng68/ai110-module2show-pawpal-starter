# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Daily Plan:
- Morning walk (Pet: Biscuit, Duration: 30 mins, Priority: high)
- Feeding (Pet: Biscuit, Duration: 10 mins, Priority: high)
- Litter box cleaning (Pet: Whiskers, Duration: 10 mins, Priority: medium)
Tasks were included based on priority and available time.
Warnings:
Conflict: Task 'Litter box cleaning' (Pet: Whiskers) conflicts with Task 'Feeding' (Pet: Biscuit) at 09:00.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest
```

My test suite covers:
- Task completion status changes (`mark_complete()`)
- Adding tasks increases a pet's task count
- Sorting tasks correctly by priority (high → medium → low)
- Recurring tasks (daily/weekly) automatically generate their next occurrence when completed
- One-time tasks do NOT generate a next occurrence
- Conflict detection correctly flags tasks scheduled at the same time
- Conflict detection correctly reports no conflicts when times differ

Sample test output:

```
======================================================== test session starts =========================================================
platform darwin -- Python 3.13.1, pytest-9.1.0, pluggy-1.6.0
rootdir: /Users/emilyzheng/ai110-module2show-pawpal-starter
plugins: dash-3.2.0, anyio-4.13.0
collected 7 items

tests/test_pawpal.py .......                                                                                                   [100%]

========================================================= 7 passed in 0.01s ==========================================================
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — Core behaviors are verified and passing, but edge cases like empty task lists or malformed time strings haven't been tested yet.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()` | Sorts high > medium > low |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the exact same time slot |
| Recurring tasks | `Scheduler.create_next_occurrence()`, `Scheduler.complete_task()` | Automatically creates the next daily/weekly occurrence when a task is completed |

## 📸 Demo Walkthrough

1. Enter the owner's name, pet's name, and species at the top of the app.
2. Add care tasks using the task form — specify a title, duration, priority, optional time, and frequency (once, daily, or weekly). Click "Add task" to save it.
3. View all tasks in the "Current Tasks" section. Use the "Filter by pet" and "Filter by status" dropdowns to narrow down the list (for example, showing only incomplete tasks for a specific pet).
4. Click "Complete" next to any task to mark it done. If the task is recurring (daily/weekly), a new occurrence is automatically created and added to the list.
5. Set "Available minutes today" and click "Generate schedule" to produce a prioritized daily plan. High-priority tasks are scheduled first, and tasks are added until the time budget runs out.
6. If two tasks are scheduled at the same time, a conflict warning appears below the plan.
7. Expand "Why this plan?" to see a plain-language explanation of which tasks were included and why.

### Example workflow

Add a pet named "Biscuit," then add two tasks: "Morning walk" (30 min, high priority, daily, 08:00) and "Feeding" (10 min, high priority, daily, 09:00). Set available minutes to 60 and click "Generate schedule" — both tasks appear in the plan since they fit within the time budget and are both high priority.

```
Daily Plan:
- Morning walk (Pet: Biscuit, Duration: 30 mins, Priority: high)
- Feeding (Pet: Biscuit, Duration: 10 mins, Priority: high)
Tasks were included based on priority and available time.
```