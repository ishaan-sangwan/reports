import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px


# Load the CSV files
def site():
    grn = pd.read_csv("./GRN.CSV")
    vehicle_listing = pd.read_excel('VehicleListingReport-11 Oct 2024-1728626629578.xlsx')

    # Create a message column
    in_hub = vehicle_listing[vehicle_listing["In Hub"] != '-']
    in_hub['msg_in'] = in_hub["Vehicle Plate"] + "-" + in_hub["In Hub Since (HH:MM:SS)"].apply(lambda x : x[:5])

    # Group by 'In Hub' and aggregate messages
    first = in_hub[in_hub['In Hub Since (HH:MM:SS)'] != '-'].groupby("In Hub").agg(lambda x: '<br>'.join(map(str, x))).reset_index()

    # Function to render multi-line entries
    def render_multi_line_entries(value):
        if isinstance(value, str):
            return value.split("<br>")
        else:
            return value

    # Apply the multi-line rendering function to the 'message' column
    first['msg_in'] = first['msg_in'].apply(render_multi_line_entries)

    # Convert the message to a single string with line breaks for better display in the grid
    # first['msg_in'] = first['msg_in'].apply(lambda x: "\n".join(x))
    first['count'] = first['msg_in'].apply(lambda x: len(x))
    # Set up AgGrid options
    gb = GridOptionsBuilder.from_dataframe(first[['In Hub', 'msg_in', 'count']])
    gb.configure_column("msg_in", wrapText=True, autoHeight=True)
    gridOptions = gb.build()


    not_connected = vehicle_listing[vehicle_listing['Device Status'] != 'connected']

    first.to_excel('first.xlsx')
    # Layout: Place AgGrid and Plotly bar chart side by side
    col1, col2 = st.columns([2, 2])  # Adjust the width of columns

    # Display the dataframe in AgGrid with wrapping enabled
    with col1:
        col1_1 , col1_2 = st.columns([1,1])
        with col1_1:
            st.subheader("Cars in Hubs")
            AgGrid(first[['In Hub', 'msg_in','count' ]], gridOptions=gridOptions, fit_columns_on_grid_load=True)

        # Out-of-hub cars message creation
            out_hub = vehicle_listing[vehicle_listing['In Hub'] == '-']
            out_hub['msg_out'] = out_hub["Vehicle Plate"] + "-" +  vehicle_listing["State"].apply(lambda x: x[0])+'-'+ out_hub["Current State Since (HH:MM:SS)"].apply(lambda x : x[:5])
            st.write(f'the total number of cars in hub are : {sum(first['count'])}')
            st.subheader('vehicles outsite hub')
            out = out_hub['msg_out'].reset_index()
            st.dataframe(out['msg_out'])
            st.write(f'the total number of cars in hub are : {len(out)}')

        with col1_2:

            st.subheader('No External Power')
            nc = not_connected[['Vehicle Plate', 'Current State Since (HH:MM:SS)']].reset_index()
            st.dataframe(nc[['Vehicle Plate', 'Current State Since (HH:MM:SS)']])
            st.write(f'the total number of disconnected vehicles are {len(nc)}')
        # Hub car counts
    hub_counts = in_hub.groupby('In Hub').size().reset_index(name='Number of Cars')

    # Create the bar chart using Plotly
    fig = px.bar(
        hub_counts, 
        x='In Hub', 
        y='Number of Cars', 
        title="Number of Cars in Each Hub",
        labels={'In Hub': 'Hub', 'Number of Cars': 'Number of Cars'},
        template="plotly_white"
    )

    # Customize layout for better readability
    fig.update_layout(
        title={'x': 0.5},
        xaxis_title='Hub',
        yaxis_title='Number of Cars',
        margin=dict(l=40, r=40, t=40, b=40),
        height=500,
    )

    # Display the chart in the right column

    with col2:
        st.subheader("Fuel Less Than 100")
        # st.plotly_chart(fig)
        vehicle_listing['Fuel Level (Lts)'] = pd.to_numeric(vehicle_listing['Fuel Level (Lts)'], errors='coerce')
        st.dataframe(vehicle_listing.query("not `Fuel Level (Lts)`.isnull() and `Fuel Level (Lts)` <= 100")[['Vehicle Plate', "Address", 'Fuel Level (Lts)']])
        st.subheader("vehicle with AdBlue Less than 20")
        vehicle_listing['Adblue Level (Lts)'] = pd.to_numeric(vehicle_listing['Adblue Level (Lts)'], errors='coerce')
        st.dataframe(vehicle_listing.query("not `Adblue Level (Lts)`.isnull() and `Adblue Level (Lts)` <= 20")[['Vehicle Plate', "Address", 'Adblue Level (Lts)']])
        


