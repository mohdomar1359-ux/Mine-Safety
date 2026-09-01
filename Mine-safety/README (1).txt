MINE WORKER SAFETY AI - ESP32 PACKAGE

FILES
1. mine_safety_ai.ino
   ESP32 inference sketch. Reads MPU6050 + humidity + MQ135 and produces SAFE/WARNING/DANGER.

2. train_mine_safety_ai.py
   Python trainer. It converts a CSV of real sensor readings into ai_model.h.

3. ai_model.h
   Generated model constants. Run the trainer first to replace this template with a model trained on your data.

4. sample_sensor_data.csv
   Small example dataset only. DO NOT use it as a real safety model.

SETUP
A) Train on your own data:
   pip install numpy pandas
   python train_mine_safety_ai.py your_sensor_data.csv

B) Put the generated ai_model.h beside mine_safety_ai.ino.

C) Open mine_safety_ai.ino in Arduino IDE, select your ESP32 board, and upload.

DATA FORMAT
ax,ay,az are accelerometer readings.
gx,gy,gz are gyroscope readings.
humidity is relative humidity in percent.
mq135 is the raw ADC reading in this version.
label is 0 for SAFE and 1 for DANGER.

IMPORTANT
This is a student prototype. A model is only as good as the labelled sensor data used to train it. For a real mine-safety deployment, validate it against calibrated sensors, carefully labelled incident/non-incident data, false-alarm rates, environmental variation, and independent test data.
