import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

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

if __name__ == "__main__":
    main()
