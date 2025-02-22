import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Keyboard Layout
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "APR"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "SP"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "CL"]
]

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Draw keys function
def draw_keyboard(frame):
    key_width, key_height = 60, 60
    start_x, start_y = 20, 20

    for row_idx, row in enumerate(keys):
        for col_idx, key in enumerate(row):
            x, y = start_x + col_idx * key_width, start_y + row_idx * key_height
            cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), (0, 0, 255), -1)
            cv2.putText(frame, key, (x + 15, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Detect finger over key
def get_key_pressed(index_x, index_y):
    key_width, key_height = 60, 60
    start_x, start_y = 20, 20

    for row_idx, row in enumerate(keys):
        for col_idx, key in enumerate(row):
            x, y = start_x + col_idx * key_width, start_y + row_idx * key_height
            if x <= index_x <= x + key_width and y <= index_y <= y + key_height:
                return key
    return None

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    draw_keyboard(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            cv2.circle(frame, (index_x, index_y), 15, (0, 255, 0), -1)
            key_pressed = get_key_pressed(index_x, index_y)

            if key_pressed:
                cv2.rectangle(frame, (index_x - 30, index_y - 30), (index_x + 30, index_y + 30), (255, 0, 0), -1)
                cv2.putText(frame, key_pressed, (index_x - 10, index_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Simulate typing when index finger touches the key
                if key_pressed == "SP":
                    pyautogui.press("space")
                elif key_pressed == "APR":
                    pyautogui.press("enter")
                elif key_pressed == "CL":
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.press("backspace")
                else:
                    pyautogui.write(key_pressed)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Virtual Keyboard", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
