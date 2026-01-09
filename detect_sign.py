import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import os
from collections import deque
import time
import win32com.client   # Windows TTS

# Load model
model = load_model("asl_model.h5")
labels = os.listdir("data")

# Windows Text-to-Speech (NON-BLOCKING)
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = -1
speaker.Volume = 100

# Confidence & stability
CONFIDENCE_THRESHOLD = 0.85
STABLE_FRAMES = 10
prediction_queue = deque(maxlen=STABLE_FRAMES)

# Word variables
current_word = ""
last_letter = ""
last_added_time = time.time()
LETTER_DELAY = 1.5

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    display_text = ""

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        landmarks = []
        for lm in hand.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])

        prediction = model.predict(np.array([landmarks]), verbose=0)[0]
        confidence = np.max(prediction)
        predicted_label = labels[np.argmax(prediction)].upper()

        if confidence > CONFIDENCE_THRESHOLD:
            prediction_queue.append(predicted_label)

            if prediction_queue.count(predicted_label) == STABLE_FRAMES:
                display_text = predicted_label

                if time.time() - last_added_time > LETTER_DELAY:
                    current_word += predicted_label
                    last_letter = predicted_label
                    last_added_time = time.time()
        else:
            prediction_queue.clear()

    # Display
    cv2.putText(frame, f"Letter: {display_text}", (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.putText(frame, f"Word: {current_word}", (30, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

    cv2.putText(frame,
                "SPC = Speak | BCS = Delete | ESC = Exit",
                (30, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 255), 2)

    cv2.imshow("ASL Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    # 🔊 SPACE → Speak (ASYNC) + Clear
    if key == 32 and current_word != "":
        speaker.Speak("", 3)
        time.sleep(0.1)
        speaker.Speak(current_word, 1)

        current_word = ""
        last_letter = ""
        prediction_queue.clear()
        last_added_time = time.time()

    # ⌫ BACKSPACE → Delete last letter
    if key == 8 and len(current_word) > 0:
        current_word = current_word[:-1]
        last_letter = ""          # allow same letter again
        last_added_time = time.time()

    # ESC → exit
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
