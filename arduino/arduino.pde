#include <Servo.h>

/*TORSO 1
HEAD 2
LEFT_SHOULDER 3
RIGHT_SHOULDER 4
LEFT_ARM 5
RIGHT_ARM 6
LEFT_TREAD 7
RIGHT_TREAD 8*/

// Servo variables
int val;
int diff;
int startbyte;
int serialServoId;
int serialServoValue;
int servoStartPin = 2;
Servo servos[8];

// Flags
int serialServoFlag = 255;

// Initial setup
void setup() {
  Serial.begin(9600);
  int servoPin = servoStartPin;
  for (int servoId = 0; servoId < 8; servoId++) {
    servos[servoId].attach(servoPin);
    move(servoId, 90);
    servoPin++;
  }
}

// Main loop
void loop() {
  if (Serial.available() > 2) {
    startbyte = Serial.read();
    if (startbyte == serialServoFlag) {
      move(Serial.read()-1, Serial.read());
    }
  }
}

// Writes a PWM signal to a servo
void move(int servoId, int position) {
  servos[servoId].write(position);
}


