import cv2
import time
import numpy as np
from deepface import DeepFace

# Load emoji images
emoji_images = {
    "angry": cv2.imread("images/angry.png"),
    "happy": cv2.imread("images/happy.png"),
    "sad": cv2.imread("images/sad.png")
}

# Resize emoji images
for key in emoji_images:
    emoji_images[key] = cv2.resize(emoji_images[key], (100, 100))

# Setup
emotion_sequence = ["angry", "happy", "sad"]
detected_faces = {emotion: None for emotion in emotion_sequence}
current_index = 0
last_detection_time = 0
frame_interval = 1  # seconds

cap = cv2.VideoCapture(0)
game_running = False
start_time = None
end_time = None

print("Press 'P' to start the challenge. Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_display = frame.copy()
    current_time = time.time()

    if game_running:
        elapsed = current_time - start_time
        cv2.putText(frame_display, f"Time: {elapsed:.1f}s", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display current target
        current_emotion = emotion_sequence[current_index]
        cv2.putText(frame_display, f"Make the emotion: {current_emotion.upper()}",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # One detection per second
        if current_time - last_detection_time >= frame_interval:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion']
                print(f"Detected: {dominant_emotion}")

                if dominant_emotion == current_emotion:
                    print(f"✔ Captured {current_emotion}!")
                    face_img = frame.copy()
                    face_img = cv2.resize(face_img, (100, 100))
                    detected_faces[current_emotion] = face_img

                    current_index += 1
                    if current_index >= len(emotion_sequence):
                        end_time = current_time
                        game_running = False
                        print(f"\n🎉 Challenge completed in {end_time - start_time:.2f} seconds!")

                last_detection_time = current_time
            except Exception as e:
                print("Emotion detection failed:", e)

        # Draw detection grid on right side of webcam feed
        for i, emotion in enumerate(emotion_sequence):
            face = detected_faces[emotion] if detected_faces[emotion] is not None else np.ones((100, 100, 3), dtype=np.uint8) * 50
            emoji = emoji_images[emotion]
            combo = np.hstack((face, emoji))
            y_offset = 80 + i * 110
            frame_display[y_offset:y_offset + 100, -200:] = combo

    else:
        cv2.putText(frame_display, "Press 'P' to Start", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

        if end_time:
            total_time = end_time - start_time
            cv2.putText(frame_display, f"Last time: {total_time:.2f}s", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Emotion Minigame", frame_display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p') and not game_running:
        print("\n▶️ Starting new challenge...")
        game_running = True
        start_time = time.time()
        end_time = None
        current_index = 0
        detected_faces = {emotion: None for emotion in emotion_sequence}
        last_detection_time = 0

cap.release()
cv2.destroyAllWindows()
