import cv2
import cv2 as cv
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import os

# GUI Window
window = tk.Tk()
window.geometry("1500x700")
window.resizable(False, False)
window.title("Hand Recognition")

# Grid layout setup
window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=6)

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = None

# GUI LEFT: Video Display
left_frame = tk.Frame(window)
left_frame.grid(row=0, column=0, sticky="nsew")

video_label = tk.Label(left_frame)
video_label.pack(pady=(10, 5))

status_label = tk.Label(left_frame, text="Waiting for gesture...", font=("Arial", 12))
status_label.pack(pady=(5, 10))

# GUI CENTER: LED Simulation
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

# GUI RIGHT: Performance Test
right_frame = tk.Frame(window)
right_frame.grid(row=0, column=2, sticky="nsew")

perf_label = tk.Label(right_frame, text="Performance Test", font=("Arial", 12))
perf_label.pack(pady=20)

result_frame = tk.Frame(right_frame)
result_frame.pack(padx=10, pady=10)

metrics_label = tk.Label(right_frame, text="", font=("Arial", 12), justify="left")
metrics_label.pack(pady=10)

# Confusion Matrix Setup
confusion_matrix = np.zeros((5, 5), dtype=int)

# Metrics Logic
def calculate_metrics(confusion_matrix):
    num_classes = confusion_matrix.shape[0]
    total = np.sum(confusion_matrix)

    macro_precision = 0
    macro_recall = 0
    macro_f1 = 0
    macro_accuracy = 0

    for i in range(num_classes):
        TP = confusion_matrix[i, i]
        FP = np.sum(confusion_matrix[:, i]) - TP
        FN = np.sum(confusion_matrix[i, :]) - TP
        TN = total - TP - FP - FN

        precision = TP / (TP + FP) if (TP + FP) != 0 else 0
        recall = TP / (TP + FN) if (TP + FN) != 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        accuracy = (TP + TN) / total if total != 0 else 0

        macro_precision += precision
        macro_recall += recall
        macro_f1 += f1
        macro_accuracy += accuracy

    macro_precision /= num_classes
    macro_recall /= num_classes
    macro_f1 /= num_classes
    macro_accuracy /= num_classes

    return {
        "macroPrecision": round(macro_precision, 3),
        "macroRecall": round(macro_recall, 3),
        "macroF1": round(macro_f1, 3),
        "macroAccuracy": round(macro_accuracy, 3)
    }


def clear_results():
    global confusion_matrix
    confusion_matrix = np.zeros((5, 5), dtype=int)
    for widget in result_frame.winfo_children():
        widget.destroy()
    metrics_label.config(text="")

# Function for Testing Performance
def test_performance():
    # Test Data Set
    test_gestures = [
        # not 1 to 4 fingers (a fist)
        {"src": "../Test_images/own-fist.jpg", "label": 0},
        {"src": "../Test_images/0-person-01.jpg", "label": 0},
        {"src": "../Test_images/0-person-02.jpg", "label": 0},
        {"src": "../Test_images/0-person-03.jpg", "label": 0},
        {"src": "../Test_images/0-person-04.jpg", "label": 0},
        {"src": "../Test_images/0-person-05.jpg", "label": 0},
        {"src": "../Test_images/0-person-06.jpg", "label": 0},
        {"src": "../Test_images/0-person-07.jpg", "label": 0},
        {"src": "../Test_images/0-person-08.jpg", "label": 0},

        # showing one finger
        {"src": "../Test_images/own-one-finger.jpg", "label": 1},
        {"src": "../Test_images/1-person-01.jpg", "label": 1},
        {"src": "../Test_images/1-person-02.jpg", "label": 1},
        {"src": "../Test_images/1-person-03.jpg", "label": 1},
        {"src": "../Test_images/1-person-04.jpg", "label": 1},
        {"src": "../Test_images/1-person-05.jpg", "label": 1},
        {"src": "../Test_images/1-person-06.jpg", "label": 1},
        {"src": "../Test_images/1-person-07.jpg", "label": 1},
        {"src": "../Test_images/1-person-08.jpg", "label": 1},

        # showing two fingers
        {"src": "../Test_images/own-two-fingers.jpg", "label": 2},
        {"src": "../Test_images/2-person-01.jpg", "label": 2},
        {"src": "../Test_images/2-person-02.jpg", "label": 2},
        {"src": "../Test_images/2-person-03.jpg", "label": 2},
        {"src": "../Test_images/2-person-04.jpg", "label": 2},
        {"src": "../Test_images/2-person-05.jpg", "label": 2},
        {"src": "../Test_images/2-person-06.jpg", "label": 2},
        {"src": "../Test_images/2-person-07.jpg", "label": 2},
        {"src": "../Test_images/2-person-08.jpg", "label": 2},

        # showing three fingers
        {"src": "../Test_images/own-three-fingers.jpg", "label": 3},
        {"src": "../Test_images/3-person-01.jpg", "label": 3},
        {"src": "../Test_images/3-person-02.jpg", "label": 3},
        {"src": "../Test_images/3-person-03.jpg", "label": 3},
        {"src": "../Test_images/3-person-04.jpg", "label": 3},
        {"src": "../Test_images/3-person-05.jpg", "label": 3},
        {"src": "../Test_images/3-person-06.jpg", "label": 3},
        {"src": "../Test_images/3-person-07.jpg", "label": 3},
        {"src": "../Test_images/3-person-08.jpg", "label": 3},

        # showing four fingers
        {"src": "../Test_images/own-four-fingers.jpg", "label": 4},
        {"src": "../Test_images/4-person-01.jpg", "label": 4},
        {"src": "../Test_images/4-person-02.jpg", "label": 4},
        {"src": "../Test_images/4-person-03.jpg", "label": 4},
        {"src": "../Test_images/4-person-04.jpg", "label": 4},
        {"src": "../Test_images/4-person-05.jpg", "label": 4},
        {"src": "../Test_images/4-person-06.jpg", "label": 4},
        {"src": "../Test_images/4-person-07.jpg", "label": 4},
        {"src": "../Test_images/4-person-08.jpg", "label": 4},
    ]

    global confusion_matrix
    confusion_matrix = np.zeros((5, 5), dtype=int)

    for widget in result_frame.winfo_children():
        widget.destroy()

   # Scrollbar in Python GUI
    canvas_frame = tk.Frame(right_frame)
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
    canvas = tk.Canvas(canvas_frame)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    perf_label.pack(pady=20)
    result_frame.pack(padx=10, pady=10)
    metrics_label.pack(pady=10)

    # Images and their Prediction
    for idx, test in enumerate(test_gestures):
        img = cv2.imread(test["src"])
        if img is None:
            continue

        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        predicted = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm = hand_landmarks.landmark

                # landmark logic finger pointing up
                index_finger = lm[8].y < lm[6].y
                middle_finger = lm[12].y < lm[10].y
                ring_finger = lm[16].y < lm[14].y
                pinky_finger = lm[20].y < lm[17].y

                # which finger combination is what gesture
                if index_finger and middle_finger and ring_finger and pinky_finger:
                    predicted = 4
                elif index_finger and middle_finger and ring_finger:
                    predicted = 3
                elif index_finger and middle_finger:
                    predicted = 2
                elif index_finger:
                    predicted = 1

        actual = test["label"]
        confusion_matrix[actual][predicted] += 1

        status = "Correct" if predicted == actual else "Wrong"
        color = "green" if predicted == actual else "red"


        row = tk.Frame(scrollable_frame)
        row.pack(fill="x", pady=2)

        image_pil = Image.open(test["src"])
        image_pil.thumbnail((100, 100))

        img_display = ImageTk.PhotoImage(image=image_pil)


        img_label = tk.Label(row, image=img_display)
        img_label.image = img_display
        img_label.pack(side="left", padx=5)

        tk.Label(row, text=f"#{idx + 1}", width=5).pack(side="left")
        tk.Label(row, text=os.path.basename(test["src"]), width=15).pack(side="left")
        tk.Label(row, text=f"Expected: {actual}", width=15).pack(side="left")
        tk.Label(row, text=f"Predicted: {predicted}", width=15).pack(side="left")
        tk.Label(row, text=status, fg=color, font=("Arial", 12, "bold"), width=5).pack(side="left")

    # Display of Performance Results
    metrics = calculate_metrics(confusion_matrix)
    display_text = (
        f"Precision: {metrics['macroPrecision']:3f}\n"
        f"Recall: {metrics['macroRecall']:3f}\n"
        f"F1 Score: {metrics['macroF1']:3f}\n"
        f"Accuracy: {metrics['macroAccuracy']:3f}"
    )
    metrics_label.config(text=display_text)


# Add Performance Test Button
test_button = tk.Button(right_frame, text="Run Performance Test", command=test_performance)
test_button.pack(pady=5)

clear_button = tk.Button(right_frame, text="Clear Results", command=clear_results)
clear_button.pack(pady=5)

current_state = "none"

# Function for Video Stream and Life Recognition
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

            # Logic which finger is pointing up
            if lm[8].y < lm[6].y: index_finger = True
            if lm[12].y < lm[10].y: middle_finger = True
            if lm[16].y < lm[14].y: ring_finger = True
            if lm[20].y < lm[17].y: pinky_finger = True

        # What gesture is the combination of fingers pointing up
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

    # Logic for controlling the Simulated LEDs
    if selected_index is not None:
        if showing_three:
            circle_states[selected_index] = "green"
            status_label.config(text=f"LED {selected_index + 1} turned ON")
        elif showing_four:
            circle_states[selected_index] = "red"
            status_label.config(text=f"LED {selected_index + 1} turned OFF")

    for i, (canvas, circle_id) in enumerate(circles):
        canvas.itemconfig(circle_id, fill=circle_states[i])
        if i == selected_index:
            canvas.itemconfig(circle_id, outline="yellow")
        else:
            canvas.itemconfig(circle_id, outline="black")

    display_width = 400
    aspect_ratio = frame.shape[1] / frame.shape[0]
    resized_frame = cv2.resize(frame, (display_width, int(display_width / aspect_ratio)))

    img = Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    window.after(10, update_frame)


def open_camera(index):
    global cap
    if cap:
        cap.release()
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Unable to open camera {index}")


open_camera(0)
update_frame()
window.mainloop()

if cap:
    cap.release()
cv2.destroyAllWindows()
