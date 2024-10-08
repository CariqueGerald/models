import RPi.GPIO as GPIO
from time import sleep
from ultralytics import YOLO
import cv2

# Setup for GPIO and motor control
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for Motor 1 and Motor 2
motor1_in1 = 24
motor1_in2 = 23
motor2_in1 = 27
motor2_in2 = 22
motor_enable1 = 25
motor_enable2 = 17

# Setup GPIO pins as outputs
GPIO.setup(motor1_in1, GPIO.OUT)
GPIO.setup(motor1_in2, GPIO.OUT)
GPIO.setup(motor_enable1, GPIO.OUT)
GPIO.setup(motor2_in1, GPIO.OUT)
GPIO.setup(motor2_in2, GPIO.OUT)
GPIO.setup(motor_enable2, GPIO.OUT)

# Initialize motors (ensure they're off initially)
GPIO.output(motor1_in1, GPIO.LOW)
GPIO.output(motor1_in2, GPIO.LOW)
GPIO.output(motor_enable1, GPIO.LOW)
GPIO.output(motor2_in1, GPIO.LOW)
GPIO.output(motor2_in2, GPIO.LOW)
GPIO.output(motor_enable2, GPIO.LOW)

# Function to move motors forward
def move_forward():
    # Motor 1
    GPIO.output(motor1_in1, GPIO.HIGH)
    GPIO.output(motor1_in2, GPIO.LOW)
    GPIO.output(motor_enable1, GPIO.HIGH)
    
    # Motor 2
    GPIO.output(motor2_in1, GPIO.HIGH)
    GPIO.output(motor2_in2, GPIO.LOW)
    GPIO.output(motor_enable2, GPIO.HIGH)

# Function to stop motors
def stop_motors():
    GPIO.output(motor1_in1, GPIO.LOW)
    GPIO.output(motor1_in2, GPIO.LOW)
    GPIO.output(motor_enable1, GPIO.LOW)
    
    GPIO.output(motor2_in1, GPIO.LOW)
    GPIO.output(motor2_in2, GPIO.LOW)
    GPIO.output(motor_enable2, GPIO.LOW)

# Load the YOLO model
model = YOLO("/home/syntax/Downloads/dolly/dolly_model_mAP71.pt")

# Start video capture (0 = default webcam)
cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        ret, frame = cap.read()  # Capture frame-by-frame
        if not ret:
            print("Failed to grab frame")
            break
        
        # Run prediction on the captured frame
        results = model.predict(source=frame, imgsz=640, conf=0.5)
        
        # Display the frame with detections
        annotated_frame = results[0].plot()  # Plot the detections on the frame
        cv2.imshow("YOLO Detection", annotated_frame)

        thumbs_up_detected = False  # Reset thumbs up detection flag
        
        # Loop over the detections
        for result in results:
            for box in result.boxes:
                cls = int(box.cls)  # class index
                if cls == 1:  # Assuming class 1 is thumbs-up
                    thumbs_up_detected = True
                    print("Thumbs up detected! Moving forward.")
                    move_forward()
                    break
        
        if not thumbs_up_detected:
            stop_motors()  # Stop motors if no thumbs up is detected
        
        # Check if the "q" key is pressed to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting the program...")
            break

finally:
    # Stop motors when the program is exited
    stop_motors()
    
    # Cleanup GPIO and release the camera
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
