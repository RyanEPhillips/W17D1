import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import json

# Load weather data from the JSON file
with open('all_weather_data.json', 'r') as json_file:
    all_weather_data = json.load(json_file)

# Extract relevant data from the JSON
dates = []
temperatures_fahrenheit = []  # List to store temperatures in Fahrenheit
for entry in all_weather_data:
    date = entry['location']['localtime']
    daily_data = entry['forecast']['forecastday'][0]['hour']
    
    for hour_data in daily_data:
        dates.append(hour_data['time'])
        
        # Convert Celsius to Fahrenheit
        temp_celsius = hour_data['temp_c']
        temp_fahrenheit = (temp_celsius * 9/5) + 32  # Convert to Fahrenheit
        temperatures_fahrenheit.append(temp_fahrenheit)

# Create a DataFrame
df = pd.DataFrame({
    'date': pd.to_datetime(dates),
    'temperature': temperatures_fahrenheit  # Store temperatures in Fahrenheit
})

# Feature engineering: Extract date-based features such as the hour of the day
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.weekday

# Use the previous hour's temperature to predict the next hour's temperature
df['target'] = df['temperature'].shift(-1)

# Drop the last row since it has no target
df = df.dropna()

# Define the feature matrix (X) and the target vector (y)
X = df[['hour', 'day', 'month', 'weekday', 'temperature']]  # Features (current time and temp)
y = df['target']  # Target is the next hour's temperature

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the K-NN model
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, y_train)

# Make predictions on the test set
y_pred = knn.predict(X_test)

# Evaluate the model's performance using Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

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

# Make a prediction for the next day
predicted_temperature = knn.predict(next_day_features_scaled)
print(f'Predicted temperature for the next day: {predicted_temperature[0]} °F')

df = pd.read_csv('Weather.csv')
print(df)