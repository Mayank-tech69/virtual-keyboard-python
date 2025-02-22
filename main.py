#importing libaries
import cv2
import mediapipe 
import math
from time import sleep
from pynput.keyboard import Controller

# initializing web cam

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    cv2.imshow("web camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()