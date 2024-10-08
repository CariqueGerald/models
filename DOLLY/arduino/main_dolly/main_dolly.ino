#include <Servo.h>

// Servo pins
const int leftServoPin = 9;   // Replace with your left servo pin
const int rightServoPin = 10; // Replace with your right servo pin

// Create Servo objects
Servo leftServo;
Servo rightServo;

void setup() {
    Serial.begin(9600);  // Ensure baud rate matches Raspberry Pi serial communication
    leftServo.attach(leftServoPin);
    rightServo.attach(rightServoPin);
    Serial.println("Arduino Ready!");
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        Serial.print("Received command: ");
        Serial.println(command);

        if (command == "F_SLOW") {
            moveForward();
        } else if (command == "STOP") {
            stopMovement();
        }
    }
}

// Function to move both servos forward
void moveForward() {
    leftServo.write(180);  // Full speed forward for left servo
    rightServo.write(0);   // Full speed forward in opposite direction for right servo
    Serial.println("Moving Forward...");
}

// Function to stop both servos
void stopMovement() {
    leftServo.write(90);  // Stop (neutral position)
    rightServo.write(90); // Stop (neutral position)
    Serial.println("Stopping...");
}
