import psycopg2
from datetime import datetime

# Database connection details
dbname = 'temperatures'
user = 'postgres'
host = 'postgres'
port = '5432'
password = 'postgres'  

# Connect to PostgreSQL
conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port, password=password)
cursor = conn.cursor()

# Data to insert
data = [
    {"city": "Zurich", "temp_c": 12.0, "timestamp": 1746460838},
    {"city": "London", "temp_c": 10.0, "timestamp": 1746460838},
    {"city": "Miami", "temp_c": 27.0, "timestamp": 1746460838},
    {"city": "Tokyo", "temp_c": 19.0, "timestamp": 1746460838},
    {"city": "Singapore", "temp_c": 27.0, "timestamp": 1746460838},
    {"city": "Zurich", "temp_c": 12.0, "timestamp": 1746464431},
    {"city": "London", "temp_c": 10.0, "timestamp": 1746464431},
    {"city": "Miami", "temp_c": 30.0, "timestamp": 1746464431},
    {"city": "Tokyo", "temp_c": 19.0, "timestamp": 1746464431},
    {"city": "Singapore", "temp_c": 27.0, "timestamp": 1746464431},
    {"city": "Zurich", "temp_c": 12.0, "timestamp": 1746468031},
    {"city": "London", "temp_c": 14.0, "timestamp": 1746468031},
    {"city": "Miami", "temp_c": 30.0, "timestamp": 1746468031},
    {"city": "Tokyo", "temp_c": 19.0, "timestamp": 1746468031},
    {"city": "Singapore", "temp_c": 27.0, "timestamp": 1746468031},
    
]

# Insert each record into the table
for entry in data:
    cursor.execute("INSERT INTO temperatures (city, temperature, timestamp) VALUES (%s, %s, to_timestamp(%s))",
                   (entry["city"], entry["temp_c"], entry["timestamp"]))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully")
