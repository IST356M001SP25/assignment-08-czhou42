'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")

st.title("Parking Tickets by Location")

tickets_df = pd.read_csv('./cache/tickets_in_top_locations.csv')

locations = tickets_df['location'].unique()
selected_location = st.selectbox("Select a Location", locations)

filtered_df = tickets_df[tickets_df['location'] == selected_location]

st.metric(label="Total Tickets", value=len(filtered_df))
st.metric(label="Total Fine Amount", value=f"${filtered_df['violation_amount'].sum():,.2f}")

dayofweek_counts = filtered_df['dayofweek'].value_counts().sort_index()
st.bar_chart(dayofweek_counts)

hourofday_counts = filtered_df['hourofday'].value_counts().sort_index()
st.line_chart(hourofday_counts)

lat = filtered_df['lat'].iloc[0]
lon = filtered_df['lon'].iloc[0]

st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
