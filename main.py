import requests
import pandas as pd
import json
import time
import datetime

API_key = '5ad526685e5640a19b1225856251501'


location = 'Goose Creek, SC'

def get_weather_data(date):
    base_url = f'https://api.weatherapi.com/v1/history.json?key={API_key}&q={location}&dt={date}'
    response = requests.get(base_url)
    return response.json()

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