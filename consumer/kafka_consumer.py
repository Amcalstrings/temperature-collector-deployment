import json 
import time
import psycopg2
from kafka import KafkaConsumer

# connect to postgres
conn = psycopg2.connect(
    dbname='temperatures',
    user='postgres',
    password='password',
    host='postgres',
    port='5432',
)

cur = conn.cursor()

#create kafka consumer
consumer = KafkaConsumer(
    'temperature_data',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='temp-consumer-group',
)

print("Consumer started...")

for message in consumer:
    try:
        data = json.loads(message.value)
        cur.execute(
            "INSERT INTO temperature readings (city, temp_c, timestamp) VALUES (%s, %s, to_timestamps(%s))",
            (data['city'], data['temp_c'], data['timestamp'])
        )
        conn.commit()
        print(f"Stored: {data}")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    
    