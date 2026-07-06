import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — a pet care planning assistant that builds a daily
schedule for your pet's tasks based on priority and available time.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# --- Persist Owner and Pet across reruns using session_state ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)

if "pet" not in st.session_state:
    pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(pet)
    st.session_state.pet = pet

owner = st.session_state.owner
pet = st.session_state.pet

# Keep name/species in sync if the user edits the text fields
owner.name = owner_name
pet.name = pet_name
pet.species = species

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed directly into the Scheduler below.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.text_input("Time (HH:MM, optional)", value="")

if st.button("Add task"):
    new_task = Task(
        description=task_title,
        duration=int(duration),
        priority=priority,
        frequency="daily",
        time=task_time if task_time else None,
    )
    pet.add_task(new_task)
    st.success(f"Added task: {task_title}")

current_tasks = pet.get_tasks()
if current_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Task": t.description,
                "Duration (min)": t.duration,
                "Priority": t.priority,
                "Time": t.time or "—",
            }
            for t in current_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input(
    "Available minutes today", min_value=10, max_value=600, value=60
)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()

    if not all_tasks:
        st.warning("No tasks to schedule yet. Add some tasks first.")
    else:
        plan = scheduler.generate_plan(available_minutes=int(available_minutes))
        conflicts = scheduler.detect_conflicts(all_tasks)

        st.markdown("#### Today's Plan")
        if plan:
            for task in plan:
                st.success(
                    f"**{task.description}** — {task.pet_name} "
                    f"({task.duration} min, priority: {task.priority}"
                    f"{', time: ' + task.time if task.time else ''})"
                )
        else:
            st.info("No tasks fit within the available time.")

        if conflicts:
            st.markdown("#### ⚠️ Conflicts")
            for warning in conflicts:
                st.warning(warning)

        with st.expander("Why this plan?"):
            st.text(scheduler.explain_plan(plan))