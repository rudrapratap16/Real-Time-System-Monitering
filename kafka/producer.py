import json
import time
import random
from kafka import KafkaProducer
from faker import Faker

# Initialize the Faker library to generate fake data
fake = Faker()

# Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:29092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# List of event types (could be extended with more)
event_types = ['error', 'warning', 'info']

# Function to generate fake system event data
def generate_fake_data():
    return {
        'event_id': fake.uuid4(),
        'timestamp': str(fake.date_this_year()),  # Random timestamp for the event
        'event_type': random.choice(event_types),  # Randomly choose an event type
        'system_name': fake.hostname(),
        'cpu_usage': round(random.uniform(0.0, 100.0), 2),  # Random CPU usage percentage
        'memory_usage': round(random.uniform(0.0, 100.0), 2)  # Random memory usage percentage
    }

# Function to send fake data to Kafka topic
def produce_fake_data():
    while True:
        fake_event = generate_fake_data()
        producer.send('system_events', fake_event)  # Send data to 'system_events' Kafka topic
        print(f"Produced Data...")  # Print the event for debugging or logging
        time.sleep(1)  # Wait for 1 second before sending the next event

if __name__ == '__main__':
    produce_fake_data()
