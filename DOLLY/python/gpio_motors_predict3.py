import RPi.GPIO as GPIO
import time

# Initialize the motor control pins for the Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for Motor 1 (Left Motor)
IN1 = 24  # Input 1 for Motor 1
IN2 = 23  # Input 2 for Motor 1
EN1 = 25  # Enable pin for Motor 1

# Define GPIO pins for Motor 2 (Right Motor)
IN3 = 27  # Input 3 for Motor 2
IN4 = 22  # Input 4 for Motor 2
EN2 = 17  # Enable pin for Motor 2

# Set up all motor control pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN1, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(EN2, GPIO.OUT)

# Set PWM for speed control
left_motor_pwm = GPIO.PWM(EN1, 1000)  # Frequency at 1kHz
right_motor_pwm = GPIO.PWM(EN2, 1000) # Frequency at 1kHz

left_motor_pwm.start(100)
right_motor_pwm.start(100)

def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Test motors by moving forward for 5 seconds
try:
    move_forward()
    time.sleep(5)
finally:
    stop_motors()
    left_motor_pwm.stop()
    right_motor_pwm.stop()
    GPIO.cleanup()