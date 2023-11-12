import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta
import io


# Function to create a sample data frame
# Function to add project data
def add_project_data(projects):
    with st.form("Project Data Form"):
        task = st.text_input("Task Name")
        resource = st.text_input("Resource")
        start = st.date_input("Start Date", datetime.today())
        duration = st.slider("Duration (weeks)", 1, 52, 4)
        salary = st.number_input("Salary", value=1000)
        submit = st.form_submit_button("Add Task")

        if submit:
            end = start + timedelta(weeks=duration)
            projects.append({
                "Task": task,
                "Resource": resource,
                "Start": start,
                "End": end,
                "Salary": salary
            })

# Function to create a Gantt chart
def create_gantt_chart(projects):
    df = pd.DataFrame(projects)
    chart = alt.Chart(df).mark_bar().encode(
        x='Start:T',
        x2='End:T',
        y=alt.Y('Task:N', sort=None),
        color='Resource:N',
        tooltip=['Task', 'Resource', 'Start', 'End', 'Salary']
    ).properties(title="Project Gantt Chart")
    return chart

# Mock data for budget
def create_mock_data():
    categories = ['Education', 'Healthcare', 'Infrastructure', 'Public Safety', 'Recreation']
    budget = np.random.randint(100000, 1000000, size=len(categories))
    spent = budget * np.random.rand(len(categories))
    return pd.DataFrame({'Category': categories, 'Budget': budget, 'Spent': spent})

# Function to display budget tracking using Altair
def budget_tracking():
    st.header("Budget Tracking and Analysis")
    df = create_mock_data()

    st.write("### Budget Overview")
    st.dataframe(df)

    st.write("### Budget Utilization Chart")

    chart = alt.Chart(df).mark_bar().encode(
        x='Category:N',
        y='Budget:Q',
        color=alt.value('skyblue'),
        tooltip=['Category', 'Budget', 'Spent']
    ) + alt.Chart(df).mark_bar().encode(
        x='Category:N',
        y='Spent:Q',
        color=alt.value('salmon'),
        tooltip=['Category', 'Budget', 'Spent']
    )

    st.altair_chart(chart, use_container_width=True)

# Main application
def main():
    st.title("Municipality Budget and Project Management SaaS")

    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose the module", ["Home", "Budget Tracking", "Project Management", "Gantt Chart"])

    if app_mode == "Home":
        st.write("Welcome to the Municipality Budget and Project Management System!")
    elif app_mode == "Budget Tracking":
        budget_tracking()
    elif app_mode == "Project Management":
        st.write("Project management features will be developed here.")
    elif app_mode == "Gantt Chart":
        st.write("### Enter Project Details")
        projects = []  # Store project data
        add_project_data(projects)

        if projects:
            st.write("### Gantt Chart")
            gantt_chart = create_gantt_chart(projects)
            st.altair_chart(gantt_chart, use_container_width=True)

if __name__ == "__main__":
    main()
