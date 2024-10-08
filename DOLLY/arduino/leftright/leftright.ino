#include <Servo.h>

// Define servo pins
const int leftServoPin = 9;
const int rightServoPin = 10;

// Create servo objects
Servo leftServo;
Servo rightServo;

void setup() {
  // Set up serial communication
  Serial.begin(9600);
  
  // Attach servos to their pins
  leftServo.attach(leftServoPin);
  rightServo.attach(rightServoPin);
  
  // Stop servos initially
  stopMovement();
}

void loop() {
  // Check if there is data available from the Raspberry Pi
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming command

    if (command == 'F') { // If 'F' is received, move forward
      moveForward();
    } else if (command == 'S') { // If 'S' is received, stop
      stopMovement();
    } else if (command == 'L') { // If 'L' is received, perform smooth 180-degree scanning
      smooth180Scan();
    }
  }
}

// Move both servos forward
void moveForward() {
  leftServo.write(180);  // Adjust these values based on your servo characteristics
  rightServo.write(0);   // Move the right servo forward
  Serial.println("Moving forward");
}

// Stop both servos
void stopMovement() {
  leftServo.write(90);   // Neutral position (stops the servo)
  rightServo.write(90);  // Neutral position (stops the servo)
  Serial.println("Stopping");
}


