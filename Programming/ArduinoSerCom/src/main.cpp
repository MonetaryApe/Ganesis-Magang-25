#include <Arduino.h>

const int IR_PIN = A0;

float analogToDistance(int analogValue) {
  return 12343.85 * pow(analogValue, -1.15);
}

void setup() {
  Serial.begin(9600);
}
void loop() {
  int analogValue = analogRead(IR_PIN);       // Read analog value from sensor
  float distance = analogToDistance(analogValue);
  Serial.println(distance); 
  delay(1000);
}