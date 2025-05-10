#include <Arduino.h>
// Use Serial1 for RX/TX (check your ESP32 board pinout)
#define RXD2 16
#define TXD2 17
#define LED_GRN 18
#define LED_YEL 19

void setup() {
  Serial.begin(115200);    // Debug Serial Monitor
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);  // Serial2 to Arduino
  pinMode(LED_GRN, OUTPUT);  // Set GPIO 18 as output
  pinMode(LED_YEL, OUTPUT);  // Set GPIO 19 as output
}

void loop() {
  if (Serial2.available()) {
    String distance = Serial2.readStringUntil('\n');  // Read until newline
    Serial.print("Received Distance: ");
    Serial.println(distance.toInt());
    if (distance.toInt() < 20) {
      digitalWrite(LED_GRN, LOW);  // Turn off green LED
      digitalWrite(LED_YEL, HIGH);  // Turn on yellow LED
    } else {
      digitalWrite(LED_GRN, HIGH);  // Turn on green LED
      digitalWrite(LED_YEL, LOW);  // Turn off yellow LED
    }
  }
}
