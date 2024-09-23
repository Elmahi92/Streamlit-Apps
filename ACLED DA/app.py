import streamlit as st
import configparser
import pandas as pd
import matplotlib.pyplot as plt
from utils import fetch_acled_data
from datetime import datetime



# Fetch data from ACLED
st.header("Data from ACLED")
acled_data = fetch_acled_data()

if not acled_data.empty:
    # Display the first few rows of the fetched data
    st.write("Fetched Data:")
    st.dataframe(acled_data)
else:
    st.write("No data available for the specified parameters.")
