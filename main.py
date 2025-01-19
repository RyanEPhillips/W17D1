import requests
import pandas as pd
import json
import time
import datetime

API_key = '5ad526685e5640a19b1225856251501'


location = 'Goose Creek, SC'

def get_weather_data(date):
    base_url = f'https://api.weatherapi.com/v1/history.json?key={API_key}&q={location}&dt={date}' # define base URL with query perameters
    response = requests.get(base_url) # set get response to api with formated url
    return response.json() # return Json response containing data

end_date = datetime.date.today() # store todays date as end variable
start_date = end_date - datetime.timedelta(days=180) # set start date by subtracting 180 days from todays date (end_date variable)

all_weather_data = [] # List to store all weather data
    

current_date = start_date # set current date to start date
while current_date <= end_date: # while current date is less than or equal to end date
    weather_data = get_weather_data(current_date.strftime('%Y-%m-%d')) # get weather data for current date
    time.sleep(1) # sleep for 1 second to avoid hitting API rate limit (Amazon Q add in)
    all_weather_data.append(weather_data) # append weather data to all_weather_data list
    print(f'Fetched data for {current_date}') 
    current_date += datetime.timedelta(days=1) # move to the next day adding 1 day to current

with open('all_weather_data.json', 'w') as json_file: # Open the file 'all_weather_data.json' in write mode ('w') to store the weather data
    json.dump(all_weather_data, json_file, indent=4) # Write with dump the list of all weather data to the JSON file with indents for readability

print('All weather data saved to all_weather_data.json')   