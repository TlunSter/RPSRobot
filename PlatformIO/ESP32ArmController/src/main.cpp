#include <Arduino.h>

int ledPin1 = 21;
int ledPin2 = 22;
int ledPin3 = 23;
void resetFingers(){
  analogWrite (ledPin1, 0);
  analogWrite (ledPin2, 0);
  analogWrite (ledPin3, 0);
}

void showRock(){
  analogWrite (ledPin1, 255);
  analogWrite (ledPin2, 0);
  analogWrite (ledPin3, 0);
}
void showPaper(){
  analogWrite (ledPin1, 0);
  analogWrite (ledPin2, 0);
  analogWrite (ledPin3, 255);
}
void showScissors(){
  analogWrite (ledPin1, 0);
  analogWrite (ledPin2, 255);
  analogWrite (ledPin3, 0);
}

void classifyAndMoveHand(String instruction){
  if(instruction == "Rock"){
    showRock();
  }
  else if (instruction == "Scissors")
  {
    showScissors();
  }else if (instruction == "Paper")
  {
    showPaper();
  }
}

void setup() {
  Serial.begin(115200);
}

void loop() {


  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n');
    Serial.print("Serial Recieved: ");
    Serial.println(incomingData);
    classifyAndMoveHand(incomingData);
  }
  
  
}
