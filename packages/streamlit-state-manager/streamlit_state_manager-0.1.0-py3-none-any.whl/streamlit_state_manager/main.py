import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Import our StateManager
# In a real package, this would be: from streamlit_state_manager import StateManager
# But for this example, assume the above class definitions are in the same file


def main():
    st.title("State Manager Demo")

    # Sidebar for navigation
    page = st.sidebar.radio(
        "Select a page",
        ["Basic Demo", "Task Manager", "Data Analysis", "Multi-form Wizard"],
    )

    # Initialize basic state
    StateManager.init("page_visits", {})
    page_visits = StateManager.get("page_visits")

    # Track page visit
    if page not in page_visits:
        page_visits[page] = 0
    page_visits[page] += 1
    StateManager.set("page_visits", page_visits)

    # Show which page we're on
    st.sidebar.write(f"You've visited this page {page_visits[page]} times")

    # Handle different pages
    if page == "Basic Demo":
        basic_demo()
    elif page == "Task Manager":
        task_manager()
    elif page == "Data Analysis":
        data_analysis()
    elif page == "Multi-form Wizard":
        multi_form_wizard()


def basic_demo():
    st.header("Basic State Management")

    # Using global state (no namespace)
    st.subheader("Global Counter")

    # Initialize counter if not exists
    StateManager.init("counter", 0)
    count = StateManager.get("counter")

    st.write(f"Current count: {count}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Increment"):
            StateManager.set("counter", count + 1)
            st.experimental_rerun()

    with col2:
        if st.button("Reset Counter"):
            StateManager.set("counter", 0)
            st.experimental_rerun()

    # Using the StateManager's static methods with a namespace
    st.subheader("Namespaced Counter")

    # Initialize counter in the "demo" namespace
    StateManager.init("counter", 0, namespace="demo")
    demo_count = StateManager.get("counter", namespace="demo")

    st.write(f"Demo namespace count: {demo_count}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Increment Demo"):
            StateManager.set("counter", demo_count + 1, namespace="demo")
            st.experimental_rerun()

    with col2:
        if st.button("Reset Demo Counter"):
            StateManager.set("counter", 0, namespace="demo")
            st.experimental_rerun()

    # Display all current state keys
    st.subheader("Current State Keys")
    all_keys = StateManager.get_keys()
    st.write(f"All keys: {all_keys}")

    # Display namespaces
    st.subheader("Current Namespaces")
    namespaces = StateManager.get_namespaces()
    st.write(f"Namespaces: {namespaces}")

    # Clear all state button
    if st.button("Clear All State"):
        StateManager.clear_all()
        st.experimental_rerun()


def task_manager():
    st.header("Task Manager Example")

    # Create a namespaced manager for tasks
    tasks = StateManager.create_namespace("tasks")

    # Initialize task list
    tasks.init("items", [])
    tasks.init("filter", "all")

    # Add new task
    with st.form("new_task_form"):
        new_task = st.text_input("Add a new task")
        priority = st.select_slider("Priority", ["Low", "Medium", "High"], "Medium")
        submitted = st.form_submit_button("Add Task")

        if submitted and new_task:
            task_list = tasks.get("items")
            task_list.append(
                {
                    "id": len(task_list),
                    "text": new_task,
                    "done": False,
                    "priority": priority,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            tasks.set("items", task_list)

    # Filter tasks
    filter_options = ["all", "active", "completed"]
    current_filter = st.selectbox(
        "Filter", filter_options, index=filter_options.index(tasks.get("filter"))
    )
    tasks.set("filter", current_filter)

    # Show tasks
    task_list = tasks.get("items")
    if task_list:
        st.subheader("Your Tasks")

        for i, task in enumerate(task_list):
            if (
                current_filter == "all"
                or (current_filter == "active" and not task["done"])
                or (current_filter == "completed" and task["done"])
            ):

                col1, col2, col3, col4 = st.columns([0.1, 0.6, 0.2, 0.1])

                with col1:
                    done = st.checkbox("", task["done"], key=f"task_{task['id']}")
                    if done != task["done"]:
                        task_list[i]["done"] = done
                        tasks.set("items", task_list)

                with col2:
                    text = task["text"]
                    if task["done"]:
                        st.markdown(f"~~{text}~~")
                    else:
                        st.write(text)

                with col3:
                    priority_color = {"Low": "blue", "Medium": "orange", "High": "red"}
                    st.markdown(
                        f"<span style='color:{priority_color[task['priority']]}'>{task['priority']}</span>",
                        unsafe_allow_html=True,
                    )

                with col4:
                    if st.button("🗑️", key=f"delete_{task['id']}"):
                        task_list.pop(i)
                        tasks.set("items", task_list)
                        st.experimental_rerun()
    else:
        st.info("No tasks yet. Add some above!")

    # Statistics
    completed = sum(1 for task in task_list if task["done"])
    active = len(task_list) - completed

    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", len(task_list))
    col2.metric("Active", active)
    col3.metric("Completed", completed)

    # Clear completed button
    if st.button("Clear Completed Tasks"):
        task_list = [task for task in task_list if not task["done"]]
        tasks.set("items", task_list)
        st.experimental_rerun()

    # Clear all tasks button
    if st.button("Clear All Tasks"):
        tasks.clear()
        st.experimental_rerun()


def data_analysis():
    st.header("Data Analysis Example")

    # Create a namespaced manager for data analysis
    analysis = StateManager.create_namespace("analysis")

    # Initialize state
    analysis.init("data", None)
    analysis.init("chart_type", "line")
    analysis.init("columns", [])
    analysis.init("selected_columns", [])

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load the data if not already loaded or if file changed
        if analysis.get("data") is None:
            with st.spinner("Loading data..."):
                df = pd.read_csv(uploaded_file)
                analysis.set("data", df)
                analysis.set("columns", df.columns.tolist())
                # Default to numeric columns for visualization
                numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                analysis.set(
                    "selected_columns",
                    numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols,
                )

    # If data is loaded, show analysis options
    df = analysis.get("data")
    if df is not None:
        st.subheader("Data Preview")
        st.dataframe(df.head())

        # Column selection
        columns = analysis.get("columns")
        selected_columns = st.multiselect(
            "Select columns for visualization",
            columns,
            default=analysis.get("selected_columns"),
        )
        analysis.set("selected_columns", selected_columns)

        # Chart type selection
        chart_types = ["line", "bar", "area"]
        chart_type = st.selectbox(
            "Chart type",
            chart_types,
            index=chart_types.index(analysis.get("chart_type")),
        )
        analysis.set("chart_type", chart_type)

        # Show chart if columns selected
        if selected_columns:
            st.subheader("Visualization")
            chart_df = (
                df[selected_columns].set_index(selected_columns[0])
                if len(selected_columns) > 1
                else df[selected_columns]
            )

            if chart_type == "line":
                st.line_chart(chart_df)
            elif chart_type == "bar":
                st.bar_chart(chart_df)
            elif chart_type == "area":
                st.area_chart(chart_df)

        # Data statistics
        if st.checkbox("Show statistics"):
            st.subheader("Data Statistics")
            st.write(df.describe())

        # Clear data button
        if st.button("Clear Data"):
            analysis.clear()
            st.experimental_rerun()


def multi_form_wizard():
    st.header("Multi-step Form Wizard")

    # Create a namespaced manager for the wizard
    wizard = StateManager.create_namespace("wizard")

    # Initialize wizard state
    wizard.init("step", 1)
    wizard.init("data", {})

    # Get current step and data
    current_step = wizard.get("step")
    form_data = wizard.get("data")

    # Progress bar
    st.progress(current_step / 4)

    # Step 1: Personal Information
    if current_step == 1:
        st.subheader("Step 1: Personal Information")

        with st.form("personal_info"):
            name = st.text_input("Name", form_data.get("name", ""))
            email = st.text_input("Email", form_data.get("email", ""))
            age = st.number_input("Age", 18, 100, form_data.get("age", 25))

            submitted = st.form_submit_button("Next")

            if submitted:
                # Validate inputs
                if not name or not email:
                    st.error("Please fill out all fields")
                else:
                    # Update data and go to next step
                    form_data.update({"name": name, "email": email, "age": age})
                    wizard.set("data", form_data)
                    wizard.set("step", 2)
                    st.experimental_rerun()

    # Step 2: Preferences
    elif current_step == 2:
        st.subheader("Step 2: Preferences")

        with st.form("preferences"):
            color = st.color_picker("Favorite Color", form_data.get("color", "#ff4466"))
            hobby = st.selectbox(
                "Favorite Hobby",
                ["Reading", "Sports", "Music", "Art", "Travel", "Cooking", "Other"],
                index=[
                    "Reading",
                    "Sports",
                    "Music",
                    "Art",
                    "Travel",
                    "Cooking",
                    "Other",
                ].index(form_data.get("hobby", "Reading")),
            )
            pets = st.multiselect(
                "Pets",
                ["Dog", "Cat", "Bird", "Fish", "Other"],
                default=form_data.get("pets", []),
            )

            col1, col2 = st.columns(2)
            with col1:
                back = st.form_submit_button("Back")
            with col2:
                next_step = st.form_submit_button("Next")

            if back:
                wizard.set("step", 1)
                st.experimental_rerun()

            if next_step:
                # Update data and go to next step
                form_data.update({"color": color, "hobby": hobby, "pets": pets})
                wizard.set("data", form_data)
                wizard.set("step", 3)
                st.experimental_rerun()

    # Step 3: Feedback
    elif current_step == 3:
        st.subheader("Step 3: Feedback")

        with st.form("feedback"):
            rating = st.slider("Rate your experience", 1, 5, form_data.get("rating", 3))
            feedback = st.text_area(
                "Additional feedback", form_data.get("feedback", "")
            )

            col1, col2 = st.columns(2)
            with col1:
                back = st.form_submit_button("Back")
            with col2:
                next_step = st.form_submit_button("Submit")

            if back:
                wizard.set("step", 2)
                st.experimental_rerun()

            if next_step:
                # Update data and go to next step
                form_data.update({"rating": rating, "feedback": feedback})
                wizard.set("data", form_data)
                wizard.set("step", 4)

                # Simulate processing
                with st.spinner("Processing your submission..."):
                    time.sleep(1)
                st.experimental_rerun()

    # Step 4: Confirmation
    elif current_step == 4:
        st.subheader("Step 4: Confirmation")

        st.success("Form submitted successfully!")

        # Display submitted data
        st.json(form_data)

        # Start over button
        if st.button("Start Over"):
            wizard.clear()
            st.experimental_rerun()


if __name__ == "__main__":
    main()
