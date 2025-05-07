import json
import time
import psycopg2
import requests
from kafka import KafkaConsumer

# Connect to Postgres
conn = psycopg2.connect(
    dbname='temperatures',
    user='postgres',
    password='postgres',
    host='postgres',
    port='5432',
)
cur = conn.cursor()

# Create Kafka consumer
consumer = KafkaConsumer(
    'temperature_data',
    bootstrap_servers='kafka.kafka.svc.cluster.local:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='temp-consumer-group',
)

print("Consumer started...")

# Pinata IPFS setup
PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI4ZGE3MDgzNC1mYzZmLTRjNDQtYTZkZS05ZGExNjFiNWZjNjEiLCJlbWFpbCI6ImFtZWR1Y2FsZWJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjNiOWQ5MDhiMmFiOGFmNzQ1Y2VmIiwic2NvcGVkS2V5U2VjcmV0IjoiMzk3MmJjN2M1MDk5YjkxYjI3NmExNDFhMDc1ZWY4ZDkwZWY4OTJhZDEzNGEwZWUwNzY3M2I1NDU2NTczNDBlZSIsImV4cCI6MTc3ODAxODgxM30.QklK8i_xa3VD38asQ2Vqu1jEB_bLJGA7GPO1RsQRdG0"  
PINATA_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
PINATA_HEADERS = {
    "Authorization": PINATA_JWT,
    "Content-Type": "application/json"
}

def upload_to_ipfs(data):
    payload = {
        "pinataMetadata": {
            "name": f"{data['city']}_temp_{data['timestamp']}"
        },
        "pinataContent": data
    }
    try:
        response = requests.post(PINATA_URL, headers=PINATA_HEADERS, json=payload)
        result = response.json()
        ipfs_url = f"https://gateway.pinata.cloud/ipfs/{result['IpfsHash']}"
        return ipfs_url
    except Exception as e:
        print(f"[IPFS Upload Error] {e}")
        return None

# Consume messages
for message in consumer:
    try:
        data = json.loads(message.value)

        # Insert readings into Postgres
        cur.execute(
            "INSERT INTO temperature_readings (city, temp_c, timestamp) VALUES (%s, %s, to_timestamp(%s))",
            (data['city'], data['temp_c'], data['timestamp'])
        )
        conn.commit()
        print(f"Stored in DB: {data}")

        # Upload data to IPFS
        ipfs_url = upload_to_ipfs(data)
        if ipfs_url:
            print(f"Stored in IPFS: {ipfs_url}")

    except Exception as e:
        print(f"[Error] {e}")
        conn.rollback()
