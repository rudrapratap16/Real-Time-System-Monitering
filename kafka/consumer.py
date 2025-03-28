import sqlite3
import json
from kafka import KafkaConsumer

# SQLite Database connection
def insert_event(event):
    conn = sqlite3.connect('db/events.db')
    cursor = conn.cursor()

    # Insert event data into the database
    cursor.execute('''
    INSERT OR REPLACE INTO events (event_id, timestamp, event_type, system_name, cpu_usage, memory_usage)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (event['event_id'], event['timestamp'], event['event_type'], event['system_name'], event['cpu_usage'], event['memory_usage']))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Kafka consumer setup
consumer = KafkaConsumer(
    'system_events',  # Kafka topic
    bootstrap_servers='localhost:29092',  # Kafka broker
    group_id='system_events_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages and insert them into the database
for msg in consumer:
    event = msg.value
    insert_event(event)  # Save the event to the SQLite database

    # Print the event (optional for debugging)
    print(f"Inserted event into DB: {event}")
