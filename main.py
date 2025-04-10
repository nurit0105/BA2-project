import cv2
import cv2 as cv
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk

# GUI Window
window = tk.Tk()
window.geometry("400x400")
window.resizable(False, False)
window.title("Hand Recognition")

# Media Pipe (noch nach genaueren Erklärungen suchen)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# OpenCV Camera
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Unable to open camera.")
    exit(0)

div = tk.Label(window, text="Hand Recognition") # Label = img in html tag
div.pack() # pack = wie grid Befehle in css

# Finger Recognition
def update_frame(): # def = function
    global cap # global = greift auf die existierende variable zu
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        return

    frame = cv.flip(frame, 1)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    index_finger = False
    middle_finger = False
    ring_finger = False

    showing_one = False
    showing_two = False
    showing_three = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            if lm[8].y < lm[6].y:
                index_finger = True
            if lm[12].y < lm[10].y:
                middle_finger = True
            if lm[16].y < lm[14].y:
                ring_finger = True

        if index_finger and middle_finger and ring_finger:
            showing_three = True
        elif index_finger and middle_finger:
            showing_two = True
        elif index_finger:
            showing_one = True
        else:
            print("Finger Count out of Scope")

    #Output
    if showing_three:
        print("Showing Three Fingers")
    if showing_two:
        print("Showing Two Fingers")
    if showing_one:
        print("Showing One Finger")


    # Showing it in the GUI
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image = img)
    div.image = imgtk
    div.configure(image=imgtk)

    # frame cycle 10ms
    window.after(10, update_frame)

update_frame()
window.mainloop()

cap.release()
cv2.destroyAllWindows()
