import streamlit as st

# Function to display the budget management section
def budget_management():
    st.header("Budget Management")
    st.write("Budget management features will go here.")

# Function to display the project management section
def project_management():
    st.header("Project Management")
    st.write("Project management features will go here.")

# Main application
def main():
    st.title("Municipality Budget and Project Management SaaS")

    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose the module",
                                ["Home", "Budget Management", "Project Management"])

    if app_mode == "Home":
        st.write("Welcome to the Municipality Budget and Project Management System!")
    elif app_mode == "Budget Management":
        budget_management()
    elif app_mode == "Project Management":
        project_management()

if __name__ == "__main__":
    main()
