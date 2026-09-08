# train_ai.py
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# 1. Load the Data
print("Loading dataset...")
df = pd.read_csv('dataset/miner_health_data.csv')

# We don't train on GPS coordinates, as location doesn't determine health risk
X = df[['Temperature', 'Humidity', 'MQ135_PPM', 'Heart_Rate', 'SpO2']].values
y = df['Risk_Level'].values

# 2. Preprocess Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data (very important for Neural Networks)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler values (You will put these in your C++ code later)
print("\n--- COPY THESE VALUES TO YOUR ESP32 CODE ---")
print(f"float means[5] = {{{', '.join(map(str, scaler.mean_))}}};")
print(f"float scales[5] = {{{', '.join(map(str, scaler.scale_))}}};")
print("--------------------------------------------\n")

# 3. Build the Neural Network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax') # 4 outputs for 4 risk levels
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 4. Train the AI
print("Training AI Model...")
model.fit(X_train_scaled, y_train, epochs=50, validation_data=(X_test_scaled, y_test))

# 5. Convert to TensorFlow Lite for ESP32
print("Converting to TensorFlow Lite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

os.makedirs('model', exist_ok=True)
with open('model/miner_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model saved to model/miner_model.tflite")
print("Next: Convert the .tflite file to a C array using xxd or a web converter like: https://xxd.nn-builders.com/")