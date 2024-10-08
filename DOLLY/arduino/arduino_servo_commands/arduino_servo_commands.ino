#include <Servo.h>

// Define servo pins
const int leftServoPin = 9;
const int rightServoPin = 10;

// Create servo objects
Servo leftServo;
Servo rightServo;

void setup() {
  Serial.begin(9600); // Start serial communication
  leftServo.attach(leftServoPin);
  rightServo.attach(rightServoPin);
  
  // Start with servos stopped
  stopMovement();
}

void loop() {
  // Check for incoming serial data from Raspberry Pi
  if (Serial.available() > 0) {
    char command = Serial.read();

    switch (command) {
      case 'F': // Move forward
        moveForward();
        break;
      case 'S': // Stop
        stopMovement();
        break;
      case 'L': // Move left (slow scan)
        slowScanLeft();
        break;
      case 'R': // Move right (slow scan)
        slowScanRight();
        break;
      default:
        stopMovement(); // Stop for any unknown command
        break;
    }
  }
}

// Move forward at full speed
void moveForward() {
  leftServo.write(180);  // Adjust based on your servo (180 for full speed)
  rightServo.write(0);    // Adjust based on your servo (0 for full speed)
  Serial.println("Moving forward");
}

// Stop movement
void stopMovement() {
  leftServo.write(90);  // Stop position for servo
  rightServo.write(90); // Stop position for servo
  Serial.println("Stopped");
}

// Slow scan left
void slowScanLeft() {
  Serial.println("Scanning left...");
  for (int angle = 90; angle <= 180; angle += 1) {
    leftServo.write(angle);
    rightServo.write(90);  // Keep the right servo stationary
    delay(15); // Adjust delay for slower scanning
  }
  for (int angle = 180; angle >= 90; angle -= 1) {
    leftServo.write(angle);
    rightServo.write(90);  // Keep the right servo stationary
    delay(15); // Adjust delay for slower scanning
  }
}

// Slow scan right
void slowScanRight() {
  Serial.println("Scanning right...");
  for (int angle = 90; angle >= 0; angle -= 1) {
    leftServo.write(90);  // Keep the left servo stationary
    rightServo.write(angle);
    delay(15); // Adjust delay for slower scanning
  }
  for (int angle = 0; angle <= 90; angle += 1) {
    leftServo.write(90);  // Keep the left servo stationary
    rightServo.write(angle);
    delay(15); // Adjust delay for slower scanning
  }
}
