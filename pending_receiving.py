import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as ex

def pending_receiving():
# Load the data
    grn = pd.read_csv('GRN.CSV')
    grn['Grn Date'] = pd.to_datetime(grn['Grn Date'])

    # Current date details
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Adjust month values for handling wrap around (e.g., January to December of the previous year)
    last_month = current_month - 1 if current_month > 1 else 12
    month_before = current_month - 2 if current_month > 2 else 12 + (current_month - 2)
    if last_month == 12:
        last_month_year = current_year - 1
    else:
        last_month_year = current_year

    if month_before == 12 or month_before == 11:
        month_before_year = current_year - 1
    else:
        month_before_year = current_year

    # Configure page layout

    # List of months
    months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]

    # Multiselect for customers
    customer = st.multiselect(
        "customer",
        options=['Select'] + list(grn['Customer Name'].unique()),
        default='Select'
    )

    c1, c2, c3 = st.columns([2, 2, 2])

    # Function to handle customer filtering (either inclusive or exclusive based on selection)
    def filter_by_customer(df, month, year, customer_list, exclude=False):
        """Filter by customer and date range."""
        filter_condition = (
            (df['Grn Date'].dt.month == month) &
            (df['Grn Date'].dt.year == year) &
            ((df['Dest Weight'] == '0') | df['Dest Weight'].isnull())
        )
        
        if customer_list == ['Select']:  # No specific customer selected, return all customers
            return df[filter_condition].groupby(['Vehicle No'])['Dest Weight'].agg(lambda x: len(list(map(str, x))))
        
        # If exclude is True, exclude the selected customers; otherwise include only selected customers
        if exclude:
            return df[filter_condition & (~df['Customer Name'].isin(customer_list))].groupby(['Vehicle No'])['Dest Weight'].agg(lambda x: len(list(map(str, x))))
        else:
            return df[filter_condition & (df['Customer Name'].isin(customer_list))].groupby(['Vehicle No'])['Dest Weight'].agg(lambda x: len(list(map(str, x))))


    # Current month receiving pending
    with c1:
        st.subheader(f'Receiving pending for {months[current_month - 1]}')
        
        output = filter_by_customer(grn, current_month, current_year, customer, exclude=True)
        output = output.rename("count").reset_index()
        st.dataframe(output)
        st.write(f'the total count for this month is :{sum(output['count'])}')
    # Last month receiving pending
    with c2:
        st.subheader(f'Receiving pending for {months[last_month - 1]}')
        
        output = filter_by_customer(grn, last_month, last_month_year, customer, exclude=True)
        output = output.rename("count").reset_index()
        st.dataframe(output)
        st.write(f'the total count for this month is :{sum(output['count'])}')


    # Month before last receiving pending
    with c3:
        st.subheader(f'Receiving pending for {months[month_before - 1]}')
        
        output = filter_by_customer(grn, month_before, month_before_year, customer, exclude=True)
        output = output.rename("count").reset_index()
        st.dataframe(output)
        st.write(f'the total count for this month is :{sum(output['count'])}')



    # Month name for grouping in graph
    grn['month'] = grn['Grn Date'].dt.month_name()

    # Define correct order of months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']

    # Convert 'month' column to categorical type with defined order
    grn['month'] = pd.Categorical(grn['month'], categories=month_order, ordered=True)

    # Filter for current year and group by month
    graph_grn = grn[grn['Grn Date'].dt.year == current_year].groupby('month').size().reset_index(name='count')

    # Plot the bar chart using Plotly
    fig = ex.bar(graph_grn, x='month', y='count', color='month', barmode='group')

    # Display the chart in Streamlit
    st.plotly_chart(fig)
