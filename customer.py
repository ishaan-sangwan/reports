import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px

# List of months for better readability
months = ['',
          "January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"
         ]

# Current month and year
current_month = dt.datetime.now().month
current_year = dt.datetime.now().year

# Function to filter data by month and year
def filter_by_month(df, month, year):
    """Filter data by month and year."""
    filter_condition = (
        (df['Grn Date'].dt.month == month) &
        (df['Grn Date'].dt.year == year)
    )
    return df[filter_condition]

# Function to generate the stock report
def stock():
    # Load the CSV file
    grn = pd.read_csv('GRN.CSV')
    grn['Grn Date'] = pd.to_datetime(grn['Grn Date'])
    
    # Prepare a dataframe to store total dispatch weight for each month
    source_locations = grn['Customer Name'].unique()

    # List to hold rows for concatenation later
    rows = []

    # Populate the dataframe with total dispatch weights for each source location
    for location in source_locations:
        report_row = {'Customer Name': location}
        for i in range(6):
            # Calculate the month in chronological order
            month = (current_month - 6 + i) % 12 + 1  # Adjust to get months from current to past 5 months
            year = current_year if (current_month - 5 + i) > 0 else current_year - 1  # Adjust year for negative months

            # Filter data for the current source location and month
            filtered_grn = grn[(grn['Customer Name'] == location) & (grn['Grn Date'].dt.month == month) & (grn['Grn Date'].dt.year == year)]
            total_weight = filtered_grn['Disp Weight'].sum()
            report_row[months[month]] = total_weight
        
        # Append the row to the list
        rows.append(report_row)
    
    # Create a DataFrame from the rows list
    report_df = pd.DataFrame(rows)

    # Display the dataframe with monthly total dispatch weights
    st.dataframe(report_df, use_container_width=True, height=800)  # Adjust the height value as needed

    # Location selection
    loc = st.selectbox('Select a Customer', options=['Select'] + list(grn['Customer Name'].unique()))

    if loc == 'Select':
        # If 'Select' is chosen, sum across all locations
        plot_data = report_df.set_index('Customer Name').sum(axis=0).reset_index()
        plot_data.columns = ['Month', 'Total Dispatch Weight']
    else: 
        # Filter the report_df for the selected location
        plot_data = report_df[report_df['Customer Name'] == loc].sum(numeric_only=True).reset_index()
        plot_data.columns = ['Month', 'Total Dispatch Weight']
    
    # Remove the "Source Location" from the plot_data for plotting
    plot_data = plot_data[plot_data['Month'] != 'Customer Name']

    # Reorder plot_data to match chronological order of months
    plot_data['Month'] = pd.Categorical(plot_data['Month'], categories=months[1:], ordered=True)
    plot_data = plot_data.sort_values('Month')

    # Plot the graph using Plotly
    # fig_line = px.line(plot_data, x='Month', y='Total Dispatch Weight', title='Total Dispatch Weight by Month',
                    #    labels={'Total Dispatch Weight': 'Total Dispatch Weight', 'Month': 'Month'})

    fig_bar = px.bar(plot_data, x='Month', y='Total Dispatch Weight', title='Total Dispatch Weight by Month',
                     labels={'Total Dispatch Weight': 'Total Dispatch Weight', 'Month': 'Month'})

    # Show the plots in Streamlit
    # st.plotly_chart(fig_line, use_container_width=True)
    st.plotly_chart(fig_bar, use_container_width=True)

# Run the Streamlit app
if __name__ == '__main__':
    st.set_page_config(layout='wide')
    stock()
