import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta
import io

# Function to create a sample data frame
def create_sample_data():
    sample_data = {
        'Task': ['Task A', 'Task B', 'Task C'],
        'Resource': ['Team 1', 'Team 2', 'Team 3'],
        'Start': pd.to_datetime(['2023-01-01', '2023-01-15', '2023-02-01']),
        'End': pd.to_datetime(['2023-01-10', '2023-01-25', '2023-02-15']),
        'Emergency Time': [2, 3, 4],  # days
        'Price Spent': [1000, 1500, 1200]
    }
    return pd.DataFrame(sample_data)

# Function to create and download an Excel template
def download_excel_template():
    data = create_sample_data()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Template')
    st.download_button(label="Download Excel Template",
                       data=output.getvalue(),
                       file_name="gantt_chart_template.xlsx",
                       mime="application/vnd.ms-excel")


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
    app_mode = st.sidebar.radio("Choose the module", ["Home", "Budget Tracking", "Project Management", "Gantt Chart"])

    if app_mode == "Home":
        st.write("Welcome to the Municipality Budget and Project Management System!")
    elif app_mode == "Budget Tracking":
        budget_tracking()
    elif app_mode == "Project Management":
        st.write("Project management features will be developed here.")
    elif app_mode == "Gantt Chart":
        st.write("### Gantt Chart Generator")
        
        # Display Download Template Button
        st.write("Download the Excel template to format your project data.")
        download_excel_template()

        st.write("### Upload Your Project Schedule")
        uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])

        if uploaded_file is not None:
            data = process_file(uploaded_file)
            gantt_chart = create_gantt_chart(data)
            st.altair_chart(gantt_chart, use_container_width=True)
        
        # Display Gantt Chart with Sample Data
        st.write("### Example Gantt Chart")
        sample_data = create_sample_data()
        sample_gantt_chart = create_gantt_chart(sample_data)
        st.altair_chart(sample_gantt_chart, use_container_width=True)

if __name__ == "__main__":
    main()
