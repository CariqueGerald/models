from ultralytics import YOLO
import RPi.GPIO as GPIO
import time

# Initialize the motor control pins for the Raspberry Pi
GPIO.setmode(GPIO .BCM)

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

# Start PWM with 100% duty cycle (full speed)
left_motor_pwm.start(100)
right_motor_pwm.start(100)

def move_forward():
    print("Moving forward")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def stop_motors():
    print("Stopping motors")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def detect_thumbs_up():
    # Load your custom YOLO model
    model = YOLO("/home/syntax/Downloads/dolly/dolly_model_mAP71.pt")

    # Capture video stream and run prediction
    result = model.predict(source="0", imgsz=640, conf=0.4, show=True, stream=True)

    # Check the results for 'thumbs up' detection (assuming 'thumbs up' is class 0)
    detected = False
    for r in result:
        for box in r.boxes:
            if box.cls == 1:  # Assuming class '0' is 'thumbs up'
                detected = True
                break

    # Debugging output
    print(f"Detection status: {detected}")

    return detected

try:
    while True:
        # Detect thumbs up
        detected = detect_thumbs_up()

        # Move forward if thumbs up is detected
        if detected:
            move_forward()
        else:
            stop_motors()

        time.sleep(0.1)  # Small delay to avoid overloading the CPU

except Exception as e:
    print(f"Error: {e}")
    GPIO.cleanup()
finally:
    # Cleanup the GPIO pins when exiting
    left_motor_pwm.stop()
    right_motor_pwm.stop()
    GPIO.cleanup()