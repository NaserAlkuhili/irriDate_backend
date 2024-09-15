import pandas as pd
import numpy as np
from meteostat import Point, Daily
from datetime import datetime

# Retrieve Historical Temperature Data

location = Point(24.4672, 39.6024)  # Latitude and Longitude of Madinah

# time period
start = datetime(2022, 1, 1)
end = datetime(2023, 12, 31)

# Get daily temperature data
weather_data = Daily(location, start, end)
weather_data = weather_data.fetch()

temperature_data = weather_data[['tavg']].reset_index()
temperature_data.rename(columns={'time': 'date', 'tavg': 'temperature'}, inplace=True)

# Handle missing temperature data
temperature_data['temperature'].fillna(method='ffill', inplace=True)

# Soil Moisture Simulator

temperature_data['moisture'] = np.clip(
    np.random.normal(loc=600, scale=150, size=len(temperature_data)), 0, 1023
).astype(int)

# Simulate Growth Stages

growth_stages = [1, 2, 3]  # 1: Vegetative, 2: Reproductive, 3: Maturation
temperature_data['growth_stage'] = np.random.choice(growth_stages, size=len(temperature_data))



#Determine Pump Action Based on Conditions
# Define moisture thresholds for each growth stage
def get_moisture_threshold(growth_stage):
    if growth_stage == 1:  
        return 700  
    elif growth_stage == 2:  
        return 700  
    elif growth_stage == 3: 
        return 600  


# Pump simulation
def determine_pump_action(row):
    moisture_threshold = get_moisture_threshold(row['growth_stage'])

    if row['moisture'] < moisture_threshold and row['temperature'] > 20:
        return 1  # Pump
    else:
        return 0  # Don't pump

temperature_data['pump'] = temperature_data.apply(determine_pump_action, axis=1)

final_dataset = temperature_data[['date', 'temperature', 'moisture', 'growth_stage', 'pump']]

final_dataset.to_csv('data.csv', index=False)

