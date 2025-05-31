#include <Arduino.h>
#define RXD2 16
#define TXD2 17
#define LED_GRN 18
#define LED_YEL 19

void setup() {
  Serial.begin(115200);    
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);  
  pinMode(LED_GRN, OUTPUT);  
  pinMode(LED_YEL, OUTPUT);  
}

void loop() {
  if (Serial2.available()) {
    String distance = Serial2.readStringUntil('\n');  
    Serial.print("Received Distance: ");
    Serial.println(distance.toInt());
    if (distance.toInt() < 20) {
      digitalWrite(LED_GRN, LOW);  
      digitalWrite(LED_YEL, HIGH);  
    } else {
      digitalWrite(LED_GRN, HIGH); 
      digitalWrite(LED_YEL, LOW); 
    }
  }
}
