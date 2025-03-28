import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time

# Function to fetch events from SQLite DB
def fetch_events():
    conn = sqlite3.connect('db/events.db')
    query = 'SELECT * FROM events ORDER BY timestamp DESC LIMIT 10'  # Fetch the last 100 events
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit App
st.title('Real-time Event Visualization')

# Create a placeholder for the plots and tables to update them in real-time
placeholder = st.empty()

# Counter for unique button keys
counter = 0

# If the session_state is not initialized, initialize it
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Loop for real-time data
while True:
    # Fetch the event data
    df = fetch_events()

    # Clear the previous content and create fresh content
    placeholder.empty()
    st.empty()

    # Show the raw data in a table
    st.subheader('Event Data')
    st.dataframe(df)

    # Visualize CPU and Memory usage over time
    st.subheader('CPU Usage Over Time')
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], df['cpu_usage'], label='CPU Usage (%)', color='blue')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('CPU Usage (%)')
    ax.set_xticklabels(df['timestamp'], rotation=45)
    ax.legend()
    st.pyplot(fig)

    st.subheader('Memory Usage Over Time')
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], df['memory_usage'], label='Memory Usage (%)', color='green')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Memory Usage (%)')
    ax.set_xticklabels(df['timestamp'], rotation=45)
    ax.legend()
    st.pyplot(fig)

    # Use the session_state to manage refresh and unique key for the button
    st.session_state.counter += 1
    if st.button(f'Refresh {st.session_state.counter}', key=f'refresh_button_{st.session_state.counter}'):
        # Trigger the re-run when the button is pressed
        st.experimental_rerun()

    # Sleep for 5 seconds before refreshing the data
    time.sleep(5)  # Refresh every 5 seconds
