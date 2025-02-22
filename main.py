import cv2
import mediapipe as mp
import numpy as np
import math
from pynput.keyboard import Controller

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpdraw = mp.solutions.drawing_utils

# Initialize virtual keyboard controller
keyboard = Controller()

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(2, 150)

text = ""

class Button():
    def __init__(self, pos, text, size=[70, 70]):
        self.pos = pos
        self.size = size
        self.text = text

# Lowercase letters with special keys (SP for Space, CL for Clear)
keys = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "CL"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "SP"],
        ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]]

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img

# Generate buttons
buttonList = []
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        buttonList.append(Button([80 * j + 10, 80 * (i + 1) + 10], key))

delay = 0

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Calibration curve for distance
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (900, 580))
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    landmark = []

    # Draw keys
    frame = drawAll(frame, buttonList)

    # Get hand landmarks
    if results.multi_hand_landmarks:
        for hn in results.multi_hand_landmarks:
            for id, lm in enumerate(hn.landmark):
                hl, wl, cl = frame.shape
                cx, cy = int(lm.x * wl), int(lm.y * hl)
                landmark.append([id, cx, cy])

    # Detect key presses
    if landmark:
        try:
            x5, y5 = landmark[5][1], landmark[5][2]
            x17, y17 = landmark[17][1], landmark[17][2]
            dis = calculate_distance(x5, y5, x17, y17)
            A, B, C = coff
            distanceCM = A * dis ** 2 + B * dis + C

            if 20 < distanceCM < 50:
                x, y = landmark[8][1], landmark[8][2]
                x3, y3 = landmark[12][1], landmark[12][2]
                cv2.circle(frame, (x, y), 20, (255, 0, 255), cv2.FILLED)

                # Check key press
                for button in buttonList:
                    xb, yb = button.pos
                    wb, hb = button.size
                    if xb < x < xb + wb and yb < y < yb + hb:
                        cv2.rectangle(frame, (xb - 5, yb - 5), (xb + wb + 5, yb + hb + 5), (160, 160, 160), cv2.FILLED)
                        cv2.putText(frame, button.text, (xb + 20, yb + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        if calculate_distance(x, y, x3, y3) < 50 and delay == 0:
                            k = button.text
                            if k == "SP":
                                text += ' '
                                keyboard.press(' ')
                            elif k == "CL":
                                text = text[:-1]
                                keyboard.press('\b')
                            else:
                                text += k
                                keyboard.press(k)

                            delay = 1
        except:
            pass

    if delay != 0:
        delay += 1
        if delay > 10:
            delay = 0

    # Display typed text
    cv2.rectangle(frame, (20, 450), (850, 550), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, text, (30, 500), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    cv2.imshow('Virtual Keyboard', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
