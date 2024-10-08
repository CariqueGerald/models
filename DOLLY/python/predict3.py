from ultralytics import YOLO
import cv2

model = YOLO("/home/syntax/Downloads/dolly/dolly_model_mAP71.pt")

result = model.predict(source="0", imgsz=640, conf=0.5, show=True)