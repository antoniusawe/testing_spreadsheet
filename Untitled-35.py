#!/usr/bin/env python
# coding: utf-8

# In[2]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from JSON key file
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\078220\Downloads\my-project-streamlit-436805-e610ec20ce30.json", scope) 

# Authorize and initialize gspread
client = gspread.authorize(creds)

# Open the Google Sheet by URL
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1HRMUoIAq0PpzKXYUc0TEerG4pnQ1-IFh5L_FMkTv5jw/edit?usp=sharing')

# Select the first worksheet
worksheet = sheet.get_worksheet(0)  # or use sheet.sheet1 to get the first sheet

# Get all values from the sheet as a list of lists
data = worksheet.get_all_values()

# Convert `data` to DataFrame, using the first row as header
data = pd.DataFrame(data[1:], columns=data[0])

# Strip spaces from string columns only
data.columns = [col.strip() if isinstance(col, str) else col for col in data.columns]

# Check if 'Total Pembelian' exists
if 'Pembelian' not in data.columns:
    st.error("Column 'Pembelian' not found in the data.")
else:
    # Convert 'Total Pembelian' column to numeric type for calculations
    data['Pembelian'] = pd.to_numeric(data['Pembelian'], errors='coerce')

    # Tampilkan data di Streamlit
    st.title("Data Dummy Pelanggan")
    st.dataframe(data)

    # Tampilkan statistik sederhana
    st.subheader("Statistik Sederhana")
    st.write(data.describe())

    # Membuat bar chart dengan matplotlib
    st.subheader("Pembelian per Pelanggan")
    fig, ax = plt.subplots()

    # Ensure column names 'Nama' and 'Total Pembelian' are present
    if 'Nama' in data.columns and 'Pembelian' in data.columns:
        ax.bar(data['Nama'], data['Pembelian'])
        ax.set_xlabel('Nama Pelanggan')
        ax.set_ylabel('Pembelian')
        ax.set_title('Grafik Total Pembelian per Pelanggan')

        # Tampilkan chart di Streamlit
        st.pyplot(fig)
    else:
        st.error("Columns 'Nama' and 'Total Pembelian' not found in the data.")


# In[ ]:




