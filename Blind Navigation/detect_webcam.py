import cv2
import pyttsx3
from ultralytics import YOLO

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Slow down speech for clarity

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Capture a single frame
ret, frame = cap.read()
cap.release()  # Release webcam after capturing one frame

if not ret:
    print("Error: Could not read frame.")
    exit()

# Run YOLO object detection
results = model(frame)

# Get frame dimensions
height, width, _ = frame.shape

# Object position mapping
def get_position(x_center, y_center, width, height):
    """Determine the object's position in a 3x3 grid."""
    x_section = ["left", "center", "right"]
    y_section = ["top", "middle", "bottom"]

    x_index = 0 if x_center < width * 0.33 else 1 if x_center < width * 0.66 else 2
    y_index = 0 if y_center < height * 0.33 else 1 if y_center < height * 0.66 else 2

    return f"{y_section[y_index]}-{x_section[x_index]}"

def estimate_depth(box_width, image_width):
    """Estimate depth based on the object's bounding box size."""
    ratio = box_width / image_width  # Compare object width to image width
    if ratio > 0.5:
        return "close"
    elif ratio > 0.2:
        return "medium distance"
    else:
        return "far"

# Process detection results
detections = results[0].boxes.data  # Get detected objects

object_descriptions = []

for det in detections:
    x_min, y_min, x_max, y_max, conf, class_id = det.tolist()
    x_center = (x_min + x_max) / 2  # Find object center (X)
    y_center = (y_min + y_max) / 2  # Find object center (Y)
    box_width = x_max - x_min  # Object width
    position = get_position(x_center, y_center, width, height)  # Determine position
    depth = estimate_depth(box_width, width)  # Estimate depth
    label = results[0].names[int(class_id)]  # Get object name
    object_descriptions.append(f"{label} {depth} {position}")

# Convert detected objects to speech
if object_descriptions:
    speech_text = ", ".join(object_descriptions)
    print("Detected:", speech_text)
    engine.say(speech_text)
    engine.runAndWait()
else:
    print("No objects detected.")

# Display the image with bounding boxes
annotated_frame = results[0].plot()
cv2.imshow("YOLO Detection", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
