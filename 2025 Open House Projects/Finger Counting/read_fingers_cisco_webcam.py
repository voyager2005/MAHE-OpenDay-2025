import cv2
import mediapipe as mp
import numpy as np

# MediaPipe hands setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Webcam setup
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Finger tip landmarks
finger_tips = [4, 8, 12, 16, 20]

def fingers_up(hand_landmarks, hand_label):
    fingers = [False] * 5

    # Thumb
    if hand_label == 'Right':
        fingers[0] = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x
    else:
        fingers[0] = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x

    # Other fingers
    fingers[1] = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    fingers[2] = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    fingers[3] = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
    fingers[4] = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

    return fingers

def draw_finger_status(img, live_fingers):
    h, w, _ = img.shape
    y_offset = h - 80
    spacing = 40
    start_x_left = int(w * 0.1)
    start_x_right = int(w * 0.55)

    for hand, x_start in zip(['Left', 'Right'], [start_x_left, start_x_right]):
        fingers = live_fingers[hand]
        draw_order = fingers[::-1] if hand == 'Left' else fingers

        label = f'{hand} Hand'
        cv2.putText(img, label, (x_start, y_offset - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        for i, is_up in enumerate(draw_order):
            color = (0, 255, 0) if is_up else (50, 50, 50)
            center = (x_start + i * spacing, y_offset)
            cv2.circle(img, center, 18, color, -1)

# Create a fullscreen window
cv2.namedWindow("Live Finger Detection", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Live Finger Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    live_fingers = {'Left': [False]*5, 'Right': [False]*5}

    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = handedness.classification[0].label  # 'Left' or 'Right'
            fingers = fingers_up(hand_landmarks, label)
            live_fingers[label] = fingers
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    draw_finger_status(frame, live_fingers)

    cv2.putText(frame, "Press 'Q' to Quit", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2)

    cv2.imshow("Live Finger Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
