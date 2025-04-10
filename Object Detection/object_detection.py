import cv2
from ultralytics import YOLO

# Load a pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Open the webcam
cap = cv2.VideoCapture(0)

print("Press 'P' to detect objects in the current frame.")
print("Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show live webcam feed
    cv2.imshow("Live Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("p"):
        # Run detection on the current frame
        results = model(frame)
        annotated_frame = results[0].plot()

        # Show the detection result
        cv2.imshow("Detected Objects", annotated_frame)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
