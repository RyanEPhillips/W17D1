import requests
API_key = 'ca24d2447a0a671019bc9ef9e76981bd'
base_url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'

def get_weather_data(lat, lon, dt):
    params = {
        'lat': lat,
        'lon': lon,
        'dt': dt,
        'appid': API_key,
        'units': 'metric'
    }
print(get_weather_data(32.9810, 80.0326, 1633046400))

import requests
import datetime
import json

# Your API key
api_key = <Put you api key here as a string>

# Location
location = <Put your location here as a string>

# Function to get weather data for a specific date
def get_weather_data(date):
    url = f'https://api.weatherapi.com/v1/history.json?key={api_key}&q={location}&dt={date}'
    response = requests.get(url)
    return response.json()

# Start and end dates
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=180)

# List to store all weather data
all_weather_data = []

# Iterate through each day in the date range
current_date = start_date
while current_date <= end_date:
    weather_data = get_weather_data(current_date.strftime('%Y-%m-%d'))
    all_weather_data.append(weather_data)
    print(f'Fetched data for {current_date}')
    current_date += datetime.timedelta(days=1)

# Save all weather data to a single JSON file
with open('all_weather_data.json', 'w') as json_file:
    json.dump(all_weather_data, json_file, indent=4)

print('All weather data saved to all_weather_data.json')    