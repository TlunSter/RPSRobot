#include <Arduino.h>

// put function declarations here:


void setup() {
  Serial.begin(115200);
}

void loop() {


  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n');
    Serial.print("You said: ");
    Serial.println(incomingData);
  }

  
}
