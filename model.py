import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import json


with open('all_weather_data.json', 'r') as json_file: # Open and load weather data from the JSON file in read
    all_weather_data = json.load(json_file) # Parse the JSON file and load it into 'all_weather_data'

dates = [] # list to store dates
temperatures_fahrenheit = []  # List to store temperatures in Fahrenheit
for entry in all_weather_data: # loop through entries in all_weather_data
    date = entry['location']['localtime'] # Get the local date and time from the data
    daily_data = entry['forecast']['forecastday'][0]['hour'] # Get hourly data for the forecast day
    
    for hour_data in daily_data: # loop through hourly data
        dates.append(hour_data['time']) # Append the time of the hour to the dates list
        
        # Convert Celsius to Fahrenheit (Chat GPT)
        temp_celsius = hour_data['temp_c']  # Get the temperature in Celsius
        temp_fahrenheit = (temp_celsius * 9/5) + 32  # Convert to Fahrenheit
        temperatures_fahrenheit.append(temp_fahrenheit) # Append the Fahrenheit temperature to the list

# Create a pandas DataFrame
df = pd.DataFrame({
    'date': pd.to_datetime(dates),  # Convert dates to pandas datetime format
    'temperature': temperatures_fahrenheit  # Store temperatures in Fahrenheit
})

# Extract date-based features hour, day, month, day of the week
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.weekday

# Create a target column to predict the next hour's temperature
df['target'] = df['temperature'].shift(-1) # Shift the 'temperature' column by one, to get the next hour's temperature as the target

# Drop rows where there is no 'target'
df = df.dropna()

# Define the feature matrix (X) and the target vector (y)
X = df[['hour', 'day', 'month', 'weekday', 'temperature']]  # Features: hour, day, month, weekday, and current temperature
y = df['target']  # Target: The next hour's temperature

# Split the data into training and testing sets (80% training, 20% testing)s
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features (scale them to have mean=0 and variance=1)
scaler = StandardScaler() # Initialize the StandardScaler
X_train = scaler.fit_transform(X_train) # Fit the scaler to the training data and transform it
X_test = scaler.transform(X_test) # Transform the test data using the already fitted scaler

knn = KNeighborsRegressor(n_neighbors=5) # Initialize and train the K-Nearest Neighbors model with 5 neighbors
knn.fit(X_train, y_train)  # Train the model on the training data

y_pred = knn.predict(X_test) # Make predictions on the test set

# Evaluate the model's performance by calculating Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred) # Calculate the MSE between the predicted and actual values
print(f'Mean Squared Error: {mse}') # Print the MSE value

# Optionally, you can make a prediction for the next day (just an example)
next_day_features = pd.DataFrame({
    'hour': [12],  # Example: Predicting at noon (12 PM)
    'day': [16],   # Example: Day 16 of the month
    'month': [1],  # Example: January
    'weekday': [2], # Example: It's a Tuesday
    'temperature': [59]  # Example: Today's temperature is 59°F (converted from 15°C)
})

# Standardize the features before predicting
next_day_features_scaled = scaler.transform(next_day_features)

# Use the trained model to make a prediction for the next day
predicted_temperature = knn.predict(next_day_features_scaled) # Predict the temperature for the next day
print(f'Predicted temperature for the next day: {predicted_temperature[0]} °F') # Print the predicted temperature

df = pd.read_csv('Weather.csv') # Load an external CSV file ('Weather.csv') to perform some data cleaning

df = df.fillna('') # Fill missing values (NaN) in the DataFrame with empty strings (blank spaces)

df.to_csv('Weather.csv', index=False) # Write the DataFrame back to the CSV file without including the index

print(df)