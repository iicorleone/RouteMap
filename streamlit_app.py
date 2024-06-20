
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the Excel file
file_path = 'RideReport-2024-06-20.xlsx'
df = pd.read_excel(file_path, sheet_name='Tablib Dataset')

# Convert start_time and end_time to datetime
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Extract date from start_time for daily grouping
df['date'] = df['start_time'].dt.date

# Streamlit app
st.title('Vehicle Daily Routes Visualization')

# Date range filter
start_date = st.date_input('Start date', df['date'].min())
end_date = st.date_input('End date', df['date'].max())

# Filter data based on selected date range
filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Function to plot routes
def plot_routes(data, vehicle_id, color):
    vehicle_data = data[data['vehicle'] == vehicle_id]
    fig = px.line_mapbox(
        vehicle_data,
        lat=vehicle_data['start_location'].apply(lambda x: float(x.split(',')[0])),
        lon=vehicle_data['start_location'].apply(lambda x: float(x.split(',')[1])),
        color_discrete_sequence=[color],
        hover_name='start_address',
        zoom=10,
        height=600
    )
    return fig

# Plot routes for 'UAN202N' and 'UAW109Z'
fig1 = plot_routes(filtered_df, 'UAN202N', 'blue')
fig2 = plot_routes(filtered_df, 'UAW109Z', 'red')

# Combine the plots
fig = fig1
for trace in fig2.data:
    fig.add_trace(trace)

# Update layout
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Display the map
st.plotly_chart(fig)
