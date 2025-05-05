# temperature scraper
import requests, json, time
from kafka import KafkaProducer

cities = ['Zurich', 'London', 'Miami', 'Tokyo', 'Singapore']

def get_temperature(city):
    url = f"https://wttr.in/{city}?format=%t"
    try:
        response = requests.get(url)
        temp = response.text.replace("°C", "").strip("+")
        response.raise_for_status()
        return float(temp)
    except requests.RequestException as e:
        print(f"Error getting temperature for {city}: {e}")
        return None
    
# create a Kafka producer
producer = KafkaProducer(bootstrap_servers='kafka.kafka.svc.cluster.local:9092')


temperature_data = {city: get_temperature(city) for city in cities}
for city, temp in temperature_data.items():
    if temp is not None:
        data = json.dumps({"city": city, "temp_c": temp, "timestamp": int(time.time())})
        producer.send("temperature_data", data.encode("utf-8"))
        print(f"Sent data for {city} to kafka: {data}")
        
