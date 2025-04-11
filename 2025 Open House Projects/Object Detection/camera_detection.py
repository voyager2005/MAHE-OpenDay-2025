import cv2
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if cap.isOpened():
    print("External cam is working!")
else:
    print("Still can't access external cam.")
