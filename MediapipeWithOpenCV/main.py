import cv2
import cv2 as cv
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk

# GUI Window
window = tk.Tk()
window.geometry("640x560")
window.resizable(False, False)
window.title("Hand Recognition")

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Camera detection
def list_cameras(max_cameras=5):
    available = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        ret, _ = cap.read()
        if ret:
            available.append(i)
        cap.release()
    return available


camera_indices = list_cameras()
selected_camera = tk.IntVar(value=camera_indices[0] if camera_indices else 0)
cap = None

# UI: video display label
video_label = tk.Label(window)
video_label.pack(pady=(10, 5))

# UI: camera selector below video
dropdown_frame = tk.Frame(window)
dropdown_frame.pack(pady=(5, 10))
if camera_indices:
    tk.Label(dropdown_frame, text="Select Camera:").pack(side=tk.LEFT, padx=5)
    camera_dropdown = tk.OptionMenu(dropdown_frame, selected_camera, *camera_indices)
    camera_dropdown.pack(side=tk.LEFT)

def open_camera(index):
    global cap
    if cap:
        cap.release()
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Unable to open camera {index}")

def change_camera(*args):
    open_camera(selected_camera.get())

selected_camera.trace_add("write", change_camera)

# Your original frame update logic, untouched
def update_frame():
    global cap
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        return

    frame = cv.flip(frame, 1)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    thumb = False
    index_finger = False
    middle_finger = False
    ring_finger = False
    pinky_finger = False

    showing_one = False
    showing_two = False
    showing_three = False
    showing_four = False
    showing_five = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            if lm[4].y < lm[2].y:
                thumb = True
            if lm[8].y < lm[6].y:
                index_finger = True
            if lm[12].y < lm[10].y:
                middle_finger = True
            if lm[16].y < lm[14].y:
                ring_finger = True
            if lm[20].y < lm[17].y:
                pinky_finger = True

        if thumb and index_finger and middle_finger and ring_finger and pinky_finger:
            showing_five = True
        elif index_finger and middle_finger and ring_finger and pinky_finger:
            showing_four = True
        elif index_finger and middle_finger and ring_finger:
            showing_three = True
        elif index_finger and middle_finger:
            showing_two = True
        elif index_finger:
            showing_one = True
        else:
            print("Finger Count out of Scope")

    #if showing_five:
        #print("Showing Five Fingers")
    if showing_four:
        print("Showing Four Fingers")
    if showing_three:
        print("Showing Three Fingers")
    if showing_two:
        print("Showing Two Fingers")
    if showing_one:
        print("Showing One Finger")

    # Show image in GUI
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    window.after(10, update_frame)

# Start camera and main loop
if camera_indices:
    open_camera(selected_camera.get())
    update_frame()
else:
    tk.Label(window, text="No cameras found.").pack()

window.mainloop()

if cap:
    cap.release()
cv2.destroyAllWindows()
