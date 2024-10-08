from gpiozero import LED
import time
from picamera2 import Picamera2
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (trained for thumbs up and thumbs down)
model = YOLO('/home/syntax/Downloads/dolly/1st_try_version.pt')  # Replace with the path to your trained model

# Initialize the Raspberry Pi Camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1920, 1080)})
picam2.configure(config)
picam2.start()

# Set up GPIO for LED control using gpiozero
LED_PIN = 17
led = LED(LED_PIN)

try:
    print("Starting camera preview...")
    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()

        # Perform detection
        results = model.predict(frame)

        # Initialize a flag for detecting thumbs up
        thumbs_up_detected = False

        # Extract and display results on the frame
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            labels = result.boxes.cls.cpu().numpy()

            print(f"Detected labels: {labels}")
            print(f"Detected boxes: {boxes}")
            print(f"Detected confidences: {confs}")

            for box, conf, cls in zip(boxes, confs, labels):
                x1, y1, x2, y2 = map(int, box)
                label = model.names[int(cls)]
                conf = round(conf, 2)

                print(f"Detected label: {label}, Confidence: {conf}")

                if label == "thumbs_up" and conf > 0.5:
                    thumbs_up_detected = True
                    print("Thumbs up detected!")

                # Draw bounding box and label on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {conf}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        # Light the LED if a thumbs up is detected
        if thumbs_up_detected:
            led.on()
            print("LED is ON")
        else:
            led.off()
            print("LED is OFF")

        # Resize the frame to a smaller fixed size
        frame_resized = cv2.resize(frame, (320, 240))

        # Display the resulting frame
        cv2.imshow("Camera Preview", frame_resized)

        # Add a short delay to control the frame rate
        time.sleep(0.1)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    print("Stopping camera preview...")
    picam2.stop()
    cv2.destroyAllWindows()
    led.close()
