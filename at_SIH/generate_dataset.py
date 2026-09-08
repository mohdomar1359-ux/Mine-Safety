# generate_dataset.py
import csv
import random
import os

# Create dataset directory if it doesn't exist
os.makedirs('dataset', exist_ok=True)

# Generate 2000 lines of data
NUM_SAMPLES = 2000
filename = 'dataset/miner_health_data.csv'

def generate_data():
    data = []
    # Columns: Temp, Humidity, MQ135(PPM), HeartRate, SpO2, Risk_Level
    # Risk Levels: 0=Safe, 1=Warning, 2=Danger, 3=Critical
    for _ in range(NUM_SAMPLES):
        risk_level = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
        
        if risk_level == 0: # Safe
            temp = random.uniform(20, 30)
            hum = random.uniform(40, 60)
            mq135 = random.uniform(10, 50)
            hr = random.uniform(60, 90)
            spo2 = random.uniform(96, 100)
        elif risk_level == 1: # Warning (e.g., hard work or slight heat)
            temp = random.uniform(30, 35)
            hum = random.uniform(60, 75)
            mq135 = random.uniform(50, 150)
            hr = random.uniform(90, 110)
            spo2 = random.uniform(93, 95)
        elif risk_level == 2: # Danger (e.g., gas buildup, high heat)
            temp = random.uniform(35, 42)
            hum = random.uniform(75, 90)
            mq135 = random.uniform(150, 400)
            hr = random.uniform(110, 140)
            spo2 = random.uniform(88, 92)
        else: # Critical (e.g., toxic gas, heatstroke)
            temp = random.uniform(42, 55)
            hum = random.uniform(90, 100)
            mq135 = random.uniform(400, 1000)
            hr = random.uniform(140, 180)
            spo2 = random.uniform(70, 87)
            
        # Add a little noise
        temp += random.gauss(0, 1)
        hum += random.gauss(0, 2)
        
        # GPS Coordinates (Simulated around a fixed point)
        lat = 23.7957 + random.uniform(-0.001, 0.001)
        lon = 86.4304 + random.uniform(-0.001, 0.001)
        
        data.append([round(temp,1), round(hum,1), round(mq135,1), int(hr), int(spo2), round(lat,6), round(lon,6), risk_level])
        
    return data

# Save to CSV
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Temperature', 'Humidity', 'MQ135_PPM', 'Heart_Rate', 'SpO2', 'GPS_Lat', 'GPS_Lon', 'Risk_Level'])
    writer.writerows(generate_data())

print(f"Dataset generated successfully at {filename}")