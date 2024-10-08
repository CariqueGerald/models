import pvporcupine
import pyaudio
import struct
import serial
import cv2
import time
from ultralytics import YOLO

# Set up the wake word path and model
ACCESS_KEY = "Ax90xE5Rua3eSzXkxjLbxCNOVlBMUHgSlhrxbz9/QEgvI1FYd+5dOQ=="
WAKE_WORD_PATH = "/home/sintax/dolly/wake_word/Hey-Dolly_en_raspberry-pi_v3_0_0.ppn"
YOLO_MODEL_PATH = "/home/sintax/dolly/models/dolly_model_mAP71.pt"

# Serial communication setup with Arduino
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Setup for wake word detection using Porcupine
def listen_for_wake_word():
    porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[WAKE_WORD_PATH])
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
    print("Listening for wake word...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected! Activating Dolly...")
                return True
    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        porcupine.delete()
    return False

# Function to perform object detection using YOLO and control Dolly's movement
def run_object_detection():
    # Load the YOLO model
    model = YOLO(YOLO_MODEL_PATH)
    cap = cv2.VideoCapture(0)  # Open USB webcam

    # Setup serial communication with Arduino
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Run object detection on the frame
            results = model.predict(source=frame, imgsz=416, conf=0.5, show=True)

            # Check for 'thumbs_up' in the detected results
            detected = False
            for box in results[0].boxes:
                cls = results[0].names[int(box.cls[0])]
                if cls == "thumbs_up":
                    detected = True
                    print("Thumbs Up Detected! Moving forward...")
                    ser.write(b"F_SLOW\n")  # Send the command to move forward
                    break

            # If no 'thumbs_up' detected, stop the movement
            if not detected:
                print("No thumbs up detected, stopping...")
                ser.write(b"STOP\n")  # Send stop command to Arduino

    except KeyboardInterrupt:
        print("Object detection terminated by user.")
    finally:
        cap.release()
        ser.close()

if __name__ == "__main__":
    if listen_for_wake_word():
        run_object_detection()