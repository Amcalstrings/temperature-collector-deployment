# temperature scraper
import requests, json, time
from kafka import KafkaProducer

cities = ['Zurich', 'London', 'Miami', 'Tokyo', 'Singapore']

def get_temperature(city):
    url = f"https://wttr.in/{city}?format=%t"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        return f"Error: {e}"
    

temperature_data = {city: get_temperature(city) for city in cities}
for city, temp in temperature_data.items():
    print(f"{city}: {temp}")
        
