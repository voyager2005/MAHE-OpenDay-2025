import cv2
import pyttsx3
from ultralytics import YOLO
import os

# Set the image folder path
image_folder = r"C:\Users\Akshat - Personal\Visual Studio Code\Blind Navigation\images"

# Set the image name (CHANGE THIS BEFORE RUNNING)
image_name = "cooking.png"  # Example: Change this to your image file

# Construct full image path
image_path = os.path.join(image_folder, image_name)

# Check if the file exists
if not os.path.exists(image_path):
    print(f"Error: Image '{image_path}' not found.")
    exit()

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Slow down speech for clarity

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load the image
frame = cv2.imread(image_path)

if frame is None:
    print("Error: Could not load image.")
    exit()

# Run YOLO object detection
results = model(frame)

# Get image dimensions
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

objects = []

for det in detections:
    x_min, y_min, x_max, y_max, conf, class_id = det.tolist()
    x_center = (x_min + x_max) / 2  # Find object center (X)
    y_center = (y_min + y_max) / 2  # Find object center (Y)
    box_width = x_max - x_min  # Object width
    position = get_position(x_center, y_center, width, height)  # Determine position
    depth = estimate_depth(box_width, width)  # Estimate depth
    label = results[0].names[int(class_id)]  # Get object name
    objects.append((label, depth, position))

# Generate a descriptive sentence
if objects:
    sentence_parts = []
    for obj in objects:
        sentence_parts.append(f"a {obj[0]} that is {obj[1]} in the {obj[2]}")
    
    description = "In the image, I see " + ", ".join(sentence_parts) + "."
    print("Generated Description:", description)
    engine.say(description)
    engine.runAndWait()
else:
    description = "No objects detected in the image."
    print(description)
    engine.say(description)
    engine.runAndWait()

# Display the image with bounding boxes
annotated_frame = results[0].plot()
cv2.imshow("YOLO Detection", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
