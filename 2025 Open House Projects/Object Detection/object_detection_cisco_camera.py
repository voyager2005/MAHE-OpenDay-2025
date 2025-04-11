import cv2
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Use external webcam (Device index 1, DirectShow backend)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

print("Press 'P' to detect objects in the current frame.")
print("Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        break

    # Show live webcam feed
    cv2.imshow("Live Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("p"):
        # Run detection on the current frame
        results = model(frame)
        annotated = results[0].plot()
        cv2.imshow("Detected Objects", annotated)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
