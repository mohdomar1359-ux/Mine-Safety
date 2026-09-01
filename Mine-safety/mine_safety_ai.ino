/*
  MINE WORKER SAFETY AI - ESP32
  --------------------------------
  Sensors used by the model:
    1. MPU6050 acceleration: ax, ay, az
    2. MPU6050 gyroscope:    gx, gy, gz
    3. Humidity sensor:      humidity
    4. MQ135 gas sensor:     mq135

  The AI outputs:
    SAFE    < 50%
    WARNING 50% - 80%
    DANGER  >= 80%

  IMPORTANT:
  - Put ai_model.h in the same Arduino sketch folder.
  - Replace readHumidity() with your actual humidity sensor code.
  - Replace BUZZER_PIN / transmitter code with your actual wiring/protocol.
  - Train the model using your REAL sensor readings before relying on it.
*/

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "ai_model.h"

Adafruit_MPU6050 mpu;

// ===== CHANGE THESE TO MATCH YOUR HARDWARE =====
const int MQ135_PIN  = 34;
const int BUZZER_PIN = 25;
// const int TX_PIN = ...; // add your transmitter pin if required
// ===============================================

float readHumidity() {
  // Replace this with your humidity sensor library/code.
  // Example for DHT11/DHT22:
  // return dht.readHumidity();
  return 0.0f;
}

float sigmoid(float z) {
  if (z > 50.0f) return 1.0f;
  if (z < -50.0f) return 0.0f;
  return 1.0f / (1.0f + expf(-z));
}

float runAI(float ax, float ay, float az,
            float gx, float gy, float gz,
            float humidity, float mq135) {
  float x[AI_FEATURES] = {
    ax, ay, az, gx, gy, gz, humidity, mq135
  };

  float score = AI_BIAS;
  for (int i = 0; i < AI_FEATURES; i++) {
    float normalized = (x[i] - AI_MEAN[i]) / AI_STD[i];
    score += AI_W[i] * normalized;
  }
  return sigmoid(score);
}

void setAlert(bool danger) {
  digitalWrite(BUZZER_PIN, danger ? HIGH : LOW);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(MQ135_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  setAlert(false);

  if (!mpu.begin()) {
    Serial.println("ERROR: MPU6050 not found.");
    while (true) delay(100);
  }

  // Typical MPU6050 setup; adjust to your project if needed.
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("Mine Worker Safety AI started.");
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float humidity = readHumidity();
  float mq135 = (float)analogRead(MQ135_PIN);

  float dangerProbability = runAI(
    a.acceleration.x,
    a.acceleration.y,
    a.acceleration.z,
    g.gyro.x,
    g.gyro.y,
    g.gyro.z,
    humidity,
    mq135
  );

  float dangerPercent = dangerProbability * 100.0f;

  Serial.print("AI danger probability: ");
  Serial.print(dangerPercent, 1);
  Serial.println(" %");

  if (dangerProbability >= 0.80f) {
    Serial.println("STATUS: DANGER");
    setAlert(true);
    // Send your emergency message through the transmitter here.
  } else if (dangerProbability >= 0.50f) {
    Serial.println("STATUS: WARNING");
    setAlert(false);
  } else {
    Serial.println("STATUS: SAFE");
    setAlert(false);
  }

  Serial.println("-------------------------");
  delay(200);
}
