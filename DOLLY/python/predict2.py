import time
from picamera2 import Picamera2
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (trained for thumbs up and thumbs down)
model_path = '/home/syntax/Downloads/dolly/dolly_model_mAP71.pt'
try:
    model = YOLO(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Initialize the Raspberry Pi Camera
try:
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1920, 1080)})  # Smaller size for speed
    picam2.configure(config)
    picam2.start()
except Exception as e:
    print(f"Error initializing camera: {e}")
    exit()

frame_rate = 30  # Desired frame rate
frame_time = 1 / frame_rate

try:
    print("Starting camera preview...")
    last_time = time.time()
    while True:
        current_time = time.time()
        if current_time - last_time >= frame_time:
            last_time = current_time

            # Capture frame-by-frame
            frame = picam2.capture_array()

            # Perform detection
            results = model.predict(frame)

            # Extract and display results on the frame
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes
                confs = result.boxes.conf.cpu().numpy()  # Confidence scores
                labels = result.boxes.cls.cpu().numpy()  # Class labels

                for box, conf, cls in zip(boxes, confs, labels):
                    x1, y1, x2, y2 = map(int, box)
                    label = model.names[int(cls)]
                    conf = round(conf, 2)

                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {conf}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            # Resize the frame to a smaller fixed size for display
            frame_resized = cv2.resize(frame, (640, 480))  # Resize to fit display window

            # Display the resulting frame
            cv2.imshow("Camera Preview", frame_resized)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    print("Stopping camera preview...")
    picam2.stop()
    cv2.destroyAllWindows()
