import pandas as pd
import numpy as np
from meteostat import Point, Daily
from datetime import datetime


location = Point(24.4672, 39.6024)  # Latitude and Longitude of Madinah

# time period
start = datetime(2020, 1, 1)
end = datetime(2021, 12, 31)

# Getting the daily temperature data
weather_data = Daily(location, start, end)
weather_data = weather_data.fetch()

temperature_data = weather_data[['tavg']].reset_index()
temperature_data.rename(columns={'time': 'date', 'tavg': 'temperature'}, inplace=True)

temperature_data['temperature'].fillna(method='ffill', inplace=True)

# Soil Moisture Simulator
temperature_data['moisture'] = np.clip(
    np.random.normal(loc=700, scale=150, size=len(temperature_data)), 0, 1023
).astype(int)



growth_stages = [1, 2, 3]  # 1: Vegetative, 2: Intermediate, 3: Fruiting
temperature_data['growth_stage'] = np.random.choice(growth_stages, size=len(temperature_data))

# Determine Pump Action Based on Conditions
def get_moisture_threshold(growth_stage):
    if growth_stage == 1:  
        return 500  
    elif growth_stage == 2: 
        return 600  
    elif growth_stage == 3:
        return 700  

# Pump simulation
def determine_pump_action(row):
    moisture_threshold = get_moisture_threshold(row['growth_stage'])

    if row['moisture'] > 850:
        return 1
    else:
        if row['moisture'] > moisture_threshold and row['temperature'] > np.average(temperature_data['temperature'])-5.5:
            return 1  # Pump
        else:
            return 0  # Don't pump

temperature_data['pump'] = temperature_data.apply(determine_pump_action, axis=1)

# Final dataset
final_dataset = temperature_data[['date', 'temperature', 'moisture', 'growth_stage', 'pump']]


final_dataset.to_csv('./smart_irrigation_data/test_data.csv', index=False)
