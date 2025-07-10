import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sample data
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"Task": "Check motor alignment", "Assigned To": "Ravi", "Due Time": "11:00 AM", "Status": "To Do"},
        {"Task": "Clean Tank Filters", "Assigned To": "Mani", "Due Time": "1:00 PM", "Status": "In Progress"},
        {"Task": "Replace Valve #3", "Assigned To": "Arun", "Due Time": "3:00 PM", "Status": "Done"}
    ]

st.title("🛠️ Shop Floor Task Display")

# Show bottlenecks and team roles
with st.expander("🔍 Operational Insights"):
    st.markdown("""
    - **Possible Bottlenecks:**
        - Tasks missed due to verbal communication only
        - Workers unclear on priority or deadline
        - No visual confirmation on completed tasks

    - **Practical Support Needed:**
        - 🧑 Supervisor: Task assignment
        - 👷 Workers: Tap or click when task is done
        - 💻 IT/Admin: Setup display on smart TV or tablet
    """)

# Display tasks
st.subheader("📋 Today's Tasks")
for i, task in enumerate(st.session_state.tasks):
    cols = st.columns([4, 2, 2, 2])
    cols[0].markdown(f"**{task['Task']}**")
    cols[1].markdown(f"👤 {task['Assigned To']}")
    cols[2].markdown(f"⏰ {task['Due Time']}")
    new_status = cols[3].selectbox("Status", ["To Do", "In Progress", "Done"], index=["To Do", "In Progress", "Done"].index(task['Status']), key=f"status_{i}")
    st.session_state.tasks[i]['Status'] = new_status

# Add new task section
with st.expander("➕ Add New Task"):
    new_task = st.text_input("Task Description")
    assigned_to = st.text_input("Assign To")
    due_time = st.time_input("Due Time", value=datetime.now().time())
    if st.button("Add Task"):
        if new_task and assigned_to:
            st.session_state.tasks.append({
                "Task": new_task,
                "Assigned To": assigned_to,
                "Due Time": due_time.strftime('%I:%M %p'),
                "Status": "To Do"
            })
            st.success("✅ Task Added!")
        else:
            st.warning("Please enter both task and assignee.")

st.markdown("---")
st.markdown("🔄 This demo resets on refresh. Data can be connected to a real backend (Google Sheets, Firebase, etc.)")
