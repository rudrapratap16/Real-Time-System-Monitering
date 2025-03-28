import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('events.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create table to store event data
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT,
    event_type TEXT,
    system_name TEXT,
    cpu_usage REAL,
    memory_usage REAL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
