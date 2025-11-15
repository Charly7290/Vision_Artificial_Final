#include <Servo.h>

Servo s1, s2, s3, s4;
int pos = 0;
String inputString = "";
boolean stringComplete = false;

void setup() {
  // put your setup code here, to run once:
  s1.attach(36); //Pin 36
  s2.attach(37); //Pin 37
  s3.attach(38); //Pin 38
  s4.attach(39); //Pin 39
  Serial.begin(9600); //To read messages from Python
  inputString.reserve(50);
  s1.write(10);
  s2.write(10);
  s3.write(360);
  s4.write(10);
}

void sweepservo(Servo &myservo, int back, int go, int time){
  delay(time); //Wait for the piece to come
  myservo.write(go);
  delay(500); 
  myservo.write(back);
  
  
}

void loop() {
  //sweepservo(s1, 20, 360, 3000);
  //sweepservo(s2, 20, 360, 2000);
  if (stringComplete) {
    if (inputString.startsWith("SERVO:")) {
      int servoNum = inputString.substring(6).toInt(); //Read number after SERVO: 
      switch(servoNum){
        case 0: sweepservo(s1, 10, 360, 950); break; //Change wait time according to each piece's arrival 
        case 1: sweepservo(s2, 10, 360, 1500); break;
        case 2: sweepservo(s3, 360, 10, 1750); break;
        case 3: sweepservo(s4, 10, 360, 2200); break;
      } 
    }
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      stringComplete = true;
    } else if (c != '\r') {
      inputString += c; //Add character to the message to form a word, since it's received per character. 
    }
  }
}
