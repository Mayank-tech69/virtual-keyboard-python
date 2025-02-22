import cv2 
import mediapipe as mp 
import numpy as np 
from time import sleep
import math 
from pynput.keyboard import Controller

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpdraw = mp.solutions.drawing_utils

keyboard = Controller()

cap = cv2.VideoCapture(0)
cap.set(2, 150)

text = ""
tx = ""

class Button():
    def __init__(self, pos, text, size=[70, 70]):
        self.pos = pos
        self.size = size
        self.text = text

# Number row with DEL
numberKeys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "DEL"]

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "CL"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "SP"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "APR"]]

keys1 = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "CL"],
         ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "SP"],
         ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "APR"]]


def drawAll(img, buttonList, numberList):
    # Draw number row + DEL
    for button in numberList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)  # Red
        cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # Draw letter keys
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)  # Red
        cv2.putText(img, button.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    return img


# Generate buttons
buttonList = []
buttonList1 = []
numberList = []

# Number row with DEL
for j, key in enumerate(numberKeys):
    numberList.append(Button([80 * j + 10, 10], key))  # Top row

# Uppercase letters
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([80 * j + 10, 80 * (i + 1) + 10], key))

# Lowercase letters
for i in range(len(keys1)):
    for j, key in enumerate(keys1[i]):
        buttonList1.append(Button([80 * j + 10, 80 * (i + 1) + 10], key))

app = 0
delay = 0


def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (1000, 580))
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    landmark = []

    # Draw keys
    if app == 0:
        frame = drawAll(frame, buttonList, numberList)
        currentList = buttonList
        r = "up"
    if app == 1:
        frame = drawAll(frame, buttonList1, numberList)
        currentList = buttonList1
        r = "down"

    # Get hand landmarks
    if results.multi_hand_landmarks:
        for hn in results.multi_hand_landmarks:
            for id, lm in enumerate(hn.landmark):
                hl, wl, cl = frame.shape
                cx, cy = int(lm.x * wl), int(lm.y * hl)
                landmark.append([id, cx, cy])

    # Detect key presses
    if landmark != 0:
        try:
            x5, y5 = landmark[5][1], landmark[5][2]
            x17, y17 = landmark[17][1], landmark[17][2]
            dis = calculate_distance(x5, y5, x17, y17)
            A, B, C = coff
            distanceCM = A * dis ** 2 + B * dis + C
            if 20 < distanceCM < 50:
                x, y = landmark[8][1], landmark[8][2]
                x2, y2 = landmark[6][1], landmark[6][2]
                x3, y3 = landmark[12][1], landmark[12][2]
                cv2.circle(frame, (x, y), 20, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x3, y3), 20, (255, 0, 255), cv2.FILLED)

                if y2 > y:
                    # Number row + DEL
                    for button in numberList:
                        xb, yb = button.pos
                        wb, hb = button.size
                        if (xb < x < xb + wb) and (yb < y < yb + hb):
                            cv2.rectangle(frame, (xb - 5, yb - 5), (xb + wb + 5, yb + hb + 5), (160, 160, 160), cv2.FILLED)
                            cv2.putText(frame, button.text, (xb + 20, yb + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            dis = calculate_distance(x, y, x3, y3)
                            if dis < 50 and delay == 0:
                                k = button.text
                                cv2.rectangle(frame, (xb - 5, yb - 5), (xb + wb + 5, yb + hb + 5), (255, 255, 255), cv2.FILLED)
                                cv2.putText(frame, k, (xb + 20, yb + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                                
                                if k == "DEL":  # Erase all text
                                    text = ""  # Clear entire text
                                else:
                                    text += k
                                    keyboard.press(k)

                                delay = 1


                    # Letters
                    for button in currentList:
                        xb, yb = button.pos
                        wb, hb = button.size

                        if (xb < x < xb + wb) and (yb < y < yb + hb):
                            cv2.rectangle(frame, (xb - 5, yb - 5), (xb + wb + 5, yb + hb + 5), (160, 160, 160), cv2.FILLED)
                            cv2.putText(frame, button.text, (xb + 20, yb + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            dis = calculate_distance(x, y, x3, y3)
                            if dis < 50 and delay == 0:
                                k = button.text
                                cv2.rectangle(frame, (xb - 5, yb - 5), (xb + wb + 5, yb + hb + 5), (255, 255, 255), cv2.FILLED)
                                cv2.putText(frame, k, (xb + 20, yb + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

                                if k == "SP":
                                    tx = ' '
                                    text += tx
                                    keyboard.press(tx)

                                elif k == "CL":
                                    tx = text[: -1]
                                    text = ""
                                    text += tx
                                    keyboard.press('\b')

                                elif k == "APR" and r == "up":
                                    app = 1

                                elif k == "APR" and r == "down":
                                    app = 0

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