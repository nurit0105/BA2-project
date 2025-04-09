import numpy as np
import cv2 as cv
import mediapipe as mp
from scipy.stats import false_discovery_control

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

finger_tips_ids = [8,12,16]
showingThree = False
showingTwo = False
showingOne = False

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print("Camera stream started. Press 'q' to quit.")
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Umwandlung in RGB für MediaPipe
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame_flipped = cv.flip(frame_rgb, 1)

    results = hands.process(frame_flipped)

    if results.multi_hand_landmarks:
        #print("Hand erkannt")
        for landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger = False
            middle_finger = False
            ring_finger = False

            landmarks = landmarks.landmark

            if landmarks[8].y < landmarks[6].y:
                index_finger = True
            elif landmarks[12].y > landmarks[10].y:
                middle_finger = True
            elif landmarks[16].y > landmarks[14].y:
                ring_finger = True

            if index_finger and middle_finger and ring_finger:
                showingThree = True
            elif index_finger and middle_finger and not ring_finger:
                showingTwo = True
            elif index_finger and not middle_finger and not ring_finger:
                showingOne = True

    else:
        print("No hands found")

    frame_bgr = cv.cvtColor(frame_flipped, cv.COLOR_RGB2BGR)

    # Display the resulting frame
    cv.imshow('mirrored', frame_bgr)
    if cv.waitKey(1) == ord('q'):
        break


    if showingThree:
        print("Showing three fingers")
    elif showingTwo:
        print("Showing two fingers")
    elif showingOne:
        print("Showing one finger")
    elif showingThree:
        print("Showing no fingers")


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()