import cv2
import mediapipe as mp
import numpy as np
import os
import time

SIGN = "x" # we can change this to collect different signs.
DATA_PATH = f"data/{SIGN}"
os.makedirs(DATA_PATH, exist_ok=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,                 #  VERY IMPORTANT
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
count = 0
TARGET = 500

while cap.isOpened() and count < TARGET:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]   # only ONE hand
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        landmarks = []
        for lm in hand.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])

        if len(landmarks) == 63:
            np.save(f"{DATA_PATH}/{count}.npy", landmarks)
            count += 1
            time.sleep(0.03)   # prevents duplicates

    cv2.putText(frame, f"Samples: {count}/{TARGET}", (10,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Collect Data", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
