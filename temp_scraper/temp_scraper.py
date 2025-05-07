# temperature scraper
import requests, json, time
from kafka import KafkaProducer

cities = ['Zurich', 'London', 'Miami', 'Tokyo', 'Singapore']

def get_temperature(city):
    url = f"https://wttr.in/{city}?format=%t&m"
    try:
        response = requests.get(url)
        temp = response.text.replace("°C", "").replace("+", "").replace("−", "-").strip()
        response.raise_for_status()
        return float(temp)
    except requests.RequestException as e:
        print(f"Error getting temperature for {city}: {e}")
        return None

# create a Kafka producer with JSON serializer
producer = KafkaProducer(
    bootstrap_servers='kafka.kafka.svc.cluster.local:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

try:
    for city in cities:
        temp = get_temperature(city)
        if temp is not None:
            data = {
                "city": city,
                "temp_c": temp,
                "timestamp": int(time.time())
            }
            producer.send("temperature_data", value=data)
            print(f"Sent data for {city} to kafka: {data}")
finally:
    # producer shuts down cleanly
    producer.flush()
    producer.close()
