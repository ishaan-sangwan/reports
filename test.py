import streamlit as st

import index

# Function for Dashboard 1
def dashboard_1():
    # Add more widgets specific to Dashboard 1
    index.grn()

# Function for Dashboard 2
def dashboard_2():
    st.title("Dashboard 2")
    st.write("This is the content of Dashboard 2.")
    # Add more widgets specific to Dashboard 2

# Function for Dashboard 3
def dashboard_3():
    st.title("Dashboard 3")
    st.write("This is the content of Dashboard 3.")
    # Add more widgets specific to Dashboard 3

# Function for Dashboard 4
def dashboard_4():
    st.title("Dashboard 4")
    st.write("This is the content of Dashboard 4.")
    # Add more widgets specific to Dashboard 4

# Main app
def main():
    st.sidebar.title("Dashboard Selector")
    
    # Four buttons for different dashboards
    dashboard_choice = st.sidebar.radio("Choose a dashboard", ("Dashboard 1", "Dashboard 2", "Dashboard 3", "Dashboard 4"))
    
    # Show dashboard based on button clicked
    if dashboard_choice == "Dashboard 1":
        dashboard_1()
    elif dashboard_choice == "Dashboard 2":
        dashboard_2()
    elif dashboard_choice == "Dashboard 3":
        dashboard_3()
    elif dashboard_choice == "Dashboard 4":
        dashboard_4()

# Run the app
if __name__ == "__main__":
    main()

