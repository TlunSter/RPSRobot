import cv2
import mediapipe as mp
import urllib.request
import os
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision
from serial_connector import SerialConnector

#Model download. Same directory as file.
MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"



#If model doesnt exist, download it. One Time
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


base_options = mp_tasks.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)
landmarker = vision.HandLandmarker.create_from_options(options)


#Joints of specific fingers. Ranges.
FINGER_TIPS = {
    "thumb": (4, 2),
    "index": (8, 6),
    "middle": (12, 10),
    "ring": (16, 14),
    "pinky": (20, 18),
}


#Between what joints to join the lines.
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]

# what beats what
COUNTER_MOVE = {
    "Rock": "Paper",
    "Paper": "Scissors",
    "Scissors": "Rock",
}

def is_finger_extended(landmarks, tip_idx, pip_idx, wrist_idx=0):
    wrist = landmarks[wrist_idx]
    tip = landmarks[tip_idx]
    pip = landmarks[pip_idx]
    dist_tip = (tip.x - wrist.x) ** 2 + (tip.y - wrist.y) ** 2
    dist_pip = (pip.x - wrist.x) ** 2 + (pip.y - wrist.y) ** 2
    return dist_tip > dist_pip


#Classify Rock Paper And Scissors. No thumb. not leeded. 
def classify_gesture(landmarks):
    extended = {name: is_finger_extended(landmarks, t, p) for name, (t, p) in FINGER_TIPS.items()}
    non_thumb_count = sum(extended[f] for f in ("index", "middle", "ring", "pinky"))

    if non_thumb_count == 0:
        return "Rock"
    elif non_thumb_count == 4:
        return "Paper"
    elif extended["index"] and extended["middle"] and not extended["ring"] and not extended["pinky"]:
        return "Scissors"
    else:
        return "Unknown"


def draw_skeleton(frame, landmarks, w, h):
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for start_idx, end_idx in HAND_CONNECTIONS:
        cv2.line(frame, points[start_idx], points[end_idx], (0, 0, 0), 2)
    for x, y in points:
        cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)


#Serial Communication
serial_connector = SerialConnector("COM9", 115200)


#Enough resolution is 640x480, will work well with less. down to 240x180
cap = cv2.VideoCapture(0)
cv2.namedWindow("RPS Robot", cv2.WINDOW_NORMAL)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_timestamp_ms = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    frame_timestamp_ms += 33
    result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

    gesture_text = "No hand detected"
    counter_text = ""

    if result.hand_landmarks:
        landmarks = result.hand_landmarks[0]
        gesture_text = classify_gesture(landmarks)
        draw_skeleton(frame, landmarks, w, h)

        if gesture_text in COUNTER_MOVE:
            counter_text = f"Robot plays: {COUNTER_MOVE[gesture_text]}"

    # Player's gesture, bottom-left, green
    cv2.putText(frame, gesture_text, (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 255, 0), 2)

    # What the robot needs to win, upper-right, red
    if counter_text:
        text_size, _ = cv2.getTextSize(counter_text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
        text_x = w - text_size[0] - 20
        cv2.putText(frame, counter_text, (text_x, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 0, 255), 2)

    cv2.imshow("RPS Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
landmarker.close()