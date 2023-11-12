import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta


# Function to process Excel file and create Gantt chart data
def process_file(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    df['Duration'] = df['End'] - df['Start']
    df['End with Emergency'] = df['End'] + df['Emergency Time'].apply(lambda x: timedelta(days=x))
    return df

# Function to create a Gantt chart using Altair
def create_gantt_chart(df):
    chart = alt.Chart(df).mark_bar().encode(
        x='Start:T',
        x2='End with Emergency:T',
        y=alt.Y('Task:N', sort=None),
        color='Resource:N',
        tooltip=['Task', 'Resource', 'Start', 'End', 'Duration', 'Emergency Time', 'Price Spent']
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
    app_mode = st.sidebar.radio("Choose the module", ["Home", "Budget Tracking", "Project Management"])

    if app_mode == "Home":
        st.write("Welcome to the Municipality Budget and Project Management System!")
    elif app_mode == "Budget Tracking":
        budget_tracking()
    elif app_mode == "Project Management":
        st.write("Project management features will be developed here.")
    elif app_mode == "Gantt Chart":
        st.write("### Gantt Chart Generator")
        st.write("Upload your project schedule Excel file.")
        uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])

        if uploaded_file is not None:
            data = process_file(uploaded_file)
            gantt_chart = create_gantt_chart(data)
            st.altair_chart(gantt_chart, use_container_width=True)

if __name__ == "__main__":
    main()
