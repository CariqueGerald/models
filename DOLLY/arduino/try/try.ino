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
    } 
    else if (command == 'S') { // If 'S' is received, stop
      stopMovement();
    } 
    else if (command == 'L') { // If 'L' is received, perform smooth 180-degree scanning
      smooth180Scan();
    }
  }
}

// Move both servos forward
void moveForward() {
  leftServo.write(130);  // Adjust these values based on your servo characteristics
  rightServo.write(50);   // Move the right servo forward
  Serial.println("Moving forward");
}

// Stop both servos
void stopMovement() {
  leftServo.write(90);   // Neutral position (stops the servo)
  rightServo.write(90);  // Neutral position (stops the servo)
  Serial.println("Stopping");
}

// Perform smooth 180-degree scanning left to right and back
void smooth180Scan() {
  Serial.println("Performing smooth 180-degree scan");

  // Step 1: Small turn left (move left servo backward, right servo forward)
  leftServo.write(82);  // Turn left wheel backward
  rightServo.write(82); // Turn right wheel forward
  delay(3000);          // Short left turn (adjust timing as needed)

  // Step 2: Smooth continuous right turn (left servo moves forward, right servo backward)
  leftServo.write(98); // Turn left wheel forward
  rightServo.write(98); // Turn right wheel backward
  delay(10000);          // Long right turn (adjust timing for a full 180 degrees)

  // Step 3: Smoothly turn back left (continue turning in opposite directions)
  leftServo.write(82);  // Turn left wheel backward
  rightServo.write(82); // Turn right wheel forward
  delay(3000);         // Long left turn to complete 180 degrees

  // Stop servos after completing the scan
  stopMovement();
  Serial.println("Finished smooth 180-degree scan");
}
