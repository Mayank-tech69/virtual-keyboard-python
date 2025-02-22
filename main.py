#importing libraries
import cv2
import mediapipe as mp
from pynput.keyboard import Controller

# initializing web cam
cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(static_image_mode=False, max_num_hands=1,
                      min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_hands = mp.solutions.drawing_utils



keyboard = Controller()

#defining the layout of the buttons

numberKeys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "DEL"]

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "CL"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "SP"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "APR"]]

keys1 = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "CL"],
         ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "SP"],
         ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "APR"]]


def drawAll(img, buttonList, numberList):
    # Draw number row + DEL ALL
    for button in numberList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)  # Red

        # Adjust font size and positioning for DEL ALL
        if button.text == "DEL":
            cv2.putText(img, button.text, (x + 15, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        else:
            cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # Draw letter keys
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)  # Red
        cv2.putText(img, button.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    return img




while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (1000, 580))
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(img)
    landmarks = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([id, cx, cy])

            # ------------------------ Drawing  landmarks and connections ------------------------
            mp_hands.draw_landmarks(frame, hand_landmarks, mphands.HAND_CONNECTIONS)

    cv2.imshow("Web Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
