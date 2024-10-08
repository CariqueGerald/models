import RPi.GPIO as GPIO
import time

# GPIO pin numbers for the two servos using PCM/hardware PWM-capable pins
servo1_pin = 18  # GPIO 18 for servo 1
servo2_pin = 19  # GPIO 19 for servo 2

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Set PWM frequency to 50Hz (standard for servos)
servo1 = GPIO.PWM(servo1_pin, 50)  # 50Hz PWM frequency for servo 1
servo2 = GPIO.PWM(servo2_pin, 50)  # 50Hz PWM frequency for servo 2

# Start PWM with a neutral duty cycle (7.5 is neutral for most servos)
servo1.start(7.5)
servo2.start(7.5)

# Function to set servo speed (0 to 100 for full forward)
def set_speed(servo, speed):
    # Neutral is around 7.5% duty cycle, adjust based on speed input
    neutral_duty_cycle = 7.5
    duty_cycle = neutral_duty_cycle + (speed / 100.0) * 2.5  # Adjust for speed range
    servo.ChangeDutyCycle(duty_cycle)

try:
    # Test moving forward
    print("Moving both servos forward")
    set_speed(servo1, -100)  # Full speed forward for servo 1
    set_speed(servo2, 100)  # Full speed forward for servo 2
    time.sleep(5)  # Move forward for 2 seconds
    
finally:
    # Stop and clean up
    print("motors stopped!")
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
