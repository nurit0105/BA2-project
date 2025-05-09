import cv2
import cv2 as cv
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk

# GUI Window
window = tk.Tk()
window.geometry("1500x700")  # Wider to accommodate three sections
window.resizable(False, False)
window.title("Hand Recognition")

# Grid layout setup
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = None

# LEFT: Video Display (1/3 width)
left_frame = tk.Frame(window)
left_frame.grid(row=0, column=0, sticky="nsew")

video_label = tk.Label(left_frame)
video_label.pack(pady=(10, 5))

status_label = tk.Label(left_frame, text="Waiting for gesture...", font=("Arial", 12))
status_label.pack(pady=(5, 10))

# CENTER: Circle placeholders
center_frame = tk.Frame(window)
center_frame.grid(row=0, column=1, sticky="nsew")
perf_label = tk.Label(center_frame, text="Simulation LEDs Smart Home", font=("Arial", 14))
perf_label.pack(pady=(10, 5))

circles = []
selected_index = None
circle_states = ["blue", "blue"]

for i in range(2):
    canvas = tk.Canvas(center_frame, width=80, height=80)
    circle_id = canvas.create_oval(10, 10, 70, 70, fill="blue", outline="black", width=3)
    canvas.pack(pady=20)
    circles.append((canvas, circle_id))


# RIGHT: Performance test placeholder
right_frame = tk.Frame(window)
right_frame.grid(row=0, column=2, sticky="nsew")

perf_label = tk.Label(right_frame, text="Performance Test", font=("Arial", 14))
perf_label.pack(pady=20)

def open_camera(index):
    global cap
    if cap:
        cap.release()
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Unable to open camera {index}")


current_state = "none"

def update_frame():
    global cap
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        return

    frame = cv.flip(frame, 1)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    index_finger = middle_finger = ring_finger = pinky_finger = False
    showing_one = showing_two = showing_three = showing_four = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            if lm[8].y < lm[6].y: index_finger = True
            if lm[12].y < lm[10].y: middle_finger = True
            if lm[16].y < lm[14].y: ring_finger = True
            if lm[20].y < lm[17].y: pinky_finger = True

        if index_finger and middle_finger and ring_finger and pinky_finger:
            showing_four = True
        elif index_finger and middle_finger and ring_finger:
            showing_three = True
        elif index_finger and middle_finger:
            showing_two = True
        elif index_finger:
            showing_one = True

    global selected_index, current_state

    for canvas, circle_id in circles:
        canvas.itemconfig(circle_id, fill="blue")

    if showing_four:
        print("Showing Four Fingers")
    if showing_three:
        print("Showing Three Fingers")
    if showing_two:
        print("Showing Two Fingers")
        selected_index = 1
        status_label.config(text="Selected LED 2")
    if showing_one:
        print("Showing One Finger")
        selected_index = 0
        status_label.config(text="Selected LED 1")

    # Apply color changes to selected circle
    if selected_index is not None:
        # Change state based on gesture
        if showing_three:
            circle_states[selected_index] = "green"
            status_label.config(text=f"LED {selected_index + 1} turned ON")
        elif showing_four:
            circle_states[selected_index] = "red"
            status_label.config(text=f"LED {selected_index + 1} turned OFF")

    for i, (canvas, circle_id) in enumerate(circles):
        canvas.itemconfig(circle_id, fill=circle_states[i])  # Set color based on state
        if i == selected_index:
            canvas.itemconfig(circle_id, outline="yellow")  # Highlight selected
        else:
            canvas.itemconfig(circle_id, outline="black")  # Normal border

    # Resize for 1/3 width display
    display_width = 500
    aspect_ratio = frame.shape[1] / frame.shape[0]
    resized_frame = cv2.resize(frame, (display_width, int(display_width / aspect_ratio)))

    img = Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    window.after(10, update_frame)


open_camera(0)
update_frame()
window.mainloop()

if cap:
    cap.release()
cv2.destroyAllWindows()
