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

# Emotion order and detection setup
emotion_sequence = ["angry", "happy", "sad"]
detected_faces = {emotion: None for emotion in emotion_sequence}
current_index = 0
last_detection_time = 0
frame_interval = 0.5  # seconds

# Start camera
cap = cv2.VideoCapture(1)  # Change to 0 for built-in webcam, or 1/2/etc for external
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Fullscreen setup
cv2.namedWindow("Emotion Minigame", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Emotion Minigame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

game_running = False
start_time = None
end_time = None
countdown_started = False
countdown_start_time = None
countdown_duration = 3  # Countdown duration in seconds

print("Press 'P' to start the challenge. Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_display = frame.copy()
    current_time = time.time()

    if countdown_started:
        seconds_left = countdown_duration - int(current_time - countdown_start_time)
        if seconds_left > 0:
            text = str(seconds_left)
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 4.0, 6)
            center_x = frame_display.shape[1] // 2 - text_width // 2
            center_y = frame_display.shape[0] // 2 + text_height // 2
            cv2.putText(frame_display, text, (center_x, center_y),
                        cv2.FONT_HERSHEY_DUPLEX, 4.0, (0, 255, 255), 6)
        else:
            countdown_started = False
            game_running = True
            start_time = time.time()
            last_detection_time = 0
            print("\u25B6\uFE0F Challenge started!")

    elif game_running:
        elapsed = current_time - start_time
        cv2.putText(frame_display, f"Time: {elapsed:.1f}s", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        current_emotion = emotion_sequence[current_index]
        cv2.putText(frame_display, f"Make the emotion: {current_emotion.upper()}",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if current_time - last_detection_time >= frame_interval:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion']
                print(f"Detected: {dominant_emotion}")

                if dominant_emotion == current_emotion:
                    print(f"\u2714 Captured {current_emotion}!")
                    face_img = cv2.resize(frame.copy(), (100, 100))
                    detected_faces[current_emotion] = face_img

                    current_index += 1
                    if current_index >= len(emotion_sequence):
                        end_time = current_time
                        game_running = False
                        print(f"\n\U0001F389 Challenge completed in {end_time - start_time:.2f} seconds!")

                last_detection_time = current_time
            except Exception as e:
                print("Emotion detection failed:", e)

        for i, emotion in enumerate(emotion_sequence):
            face = detected_faces[emotion] if detected_faces[emotion] is not None else np.ones((100, 100, 3), dtype=np.uint8) * 50
            emoji = emoji_images[emotion]
            combo = np.hstack((face, emoji))
            y_offset = 80 + i * 110
            if y_offset + 100 <= frame_display.shape[0]:
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
    elif key == ord('p') and not game_running and not countdown_started:
        print("\n\U0001F514 Get Ready! Countdown starting...")
        countdown_started = True
        countdown_start_time = time.time()
        current_index = 0
        end_time = None
        detected_faces = {emotion: None for emotion in emotion_sequence}
    elif key == ord('f') and game_running:
        current_emotion = emotion_sequence[current_index]
        print(f"\u26A1 Manual grant: {current_emotion}")
        face_img = cv2.resize(frame.copy(), (100, 100))
        detected_faces[current_emotion] = face_img

        current_index += 1
        if current_index >= len(emotion_sequence):
            end_time = time.time()
            game_running = False
            print(f"\n\U0001F389 Challenge completed in {end_time - start_time:.2f} seconds!")
        last_detection_time = current_time

cap.release()
cv2.destroyAllWindows()
