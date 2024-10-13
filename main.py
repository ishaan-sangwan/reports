import streamlit as st 
import index
import pending_receiving
import stock
import customer  

st.set_page_config(layout="wide")
st.title('Shree AshTech Ltd')

# Create a sidebar with radio buttons
option = st.sidebar.radio(
    "Choose a page:",
    ("index", "pending recieving" ,'stock', 'customer')
)

# Display different content based on the selected option
if option == "index":
    index.site()
elif option == "pending recieving":
    pending_receiving.pending_receiving()
elif option == 'stock':
    stock.stock()
elif option == 'customer':
    customer.stock()

# Optionally, add a footer or additional sections to the dashboard
