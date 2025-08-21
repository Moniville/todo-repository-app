import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ===============================
# File for persistent storage
# ===============================
DATA_FILE = "tasks.json"

# Load tasks
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ===============================
# App UI
# ===============================
st.set_page_config(page_title="To-Do List App", page_icon="✅", layout="wide")
st.title("📝 To-Do List App")
st.write("Manage your tasks efficiently with categories, deadlines, and progress tracking.")

# Sidebar: Add new task
st.sidebar.header("➕ Add New Task")
task_name = st.sidebar.text_input("Task Name")
category = st.sidebar.selectbox("Category", ["Work", "Personal", "Urgent", "Other"])
due_date = st.sidebar.date_input("Due Date")
priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"])

if st.sidebar.button("Add Task"):
    if task_name:
        new_task = {
            "name": task_name,
            "category": category,
            "due_date": str(due_date),
            "priority": priority,
            "completed": False
        }
        st.session_state.tasks.append(new_task)
        save_tasks(st.session_state.tasks)
        st.sidebar.success("Task added!")
    else:
        st.sidebar.error("Task name cannot be empty")

# ===============================
# Main Content: Task List
# ===============================
st.subheader("📌 Your Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add some from the sidebar!")
else:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4, col5 = st.columns([0.05, 0.4, 0.2, 0.2, 0.15])
        
        with col1:
            done = st.checkbox("", value=task["completed"], key=f"done_{i}")
            st.session_state.tasks[i]["completed"] = done
        
        with col2:
            st.markdown(f"**{task['name']}**")
            st.caption(f"{task['category']} | Priority: {task['priority']}")
        
        with col3:
            st.write("📅", task["due_date"])
            days_left = (datetime.strptime(task["due_date"], "%Y-%m-%d") - datetime.now()).days
            st.caption(f"{days_left} days left")
        
        with col4:
            if st.button("✏️ Edit", key=f"edit_{i}"):
                st.session_state.edit_task = i
            
        with col5:
            if st.button("🗑️ Delete", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                save_tasks(st.session_state.tasks)
                st.experimental_rerun()

# ===============================
# Progress Bar
# ===============================
total = len(st.session_state.tasks)
completed = sum(1 for t in st.session_state.tasks if t["completed"])
if total > 0:
    progress = completed / total
    st.progress(progress)
    st.success(f"Completed {completed}/{total} tasks ({int(progress*100)}%)")

# Save tasks automatically
save_tasks(st.session_state.tasks)
