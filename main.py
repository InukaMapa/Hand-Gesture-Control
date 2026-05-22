import cv2
import pyautogui

pyautogui.FAILSAFE = False

from modules.hand_tracker import HandTracker
from modules.volume_control import VolumeControl
from modules.mouse_control import MouseControl
from modules.gesture_manager import GestureManager

# =====================================
# CAMERA SETUP
# =====================================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# HD Resolution
cap.set(3, 1280)
cap.set(4, 720)

# =====================================
# MODULES
# =====================================

tracker = HandTracker()

volume = VolumeControl()

mouse = MouseControl()

gesture_manager = GestureManager()

# =====================================
# MAIN LOOP
# =====================================
import time

exit_start_time = None

while True:

    success, img = cap.read()

    if not success:
        continue

    # Mirror effect
    img = cv2.flip(img, 1)

    # =====================================
    # HAND DETECTION
    # =====================================

    img = tracker.find_hands(img)

    lmList = tracker.find_position(img)

    # Finger detection
    fingers = (
        gesture_manager.get_fingers(lmList)
        if len(lmList) != 0
        else []
    )

    # =====================================
    # MODE DETECTION
    # =====================================

    mode = gesture_manager.detect_mode(lmList)

    # =====================================
    # TOP UI PANEL
    # =====================================

    cv2.rectangle(
        img,
        (0, 0),
        (1280, 90),
        (30, 30, 30),
        cv2.FILLED
    )

    # Title
    cv2.putText(
        img,
        "AI Gesture Control System",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        3
    )

    # Active mode
    cv2.putText(
        img,
        f"MODE : {mode if mode else 'NONE'}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Finger debug
    cv2.putText(
        img,
        f"FINGERS : {fingers}",
        (500, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # =====================================
    # MODE SYSTEM
    # =====================================

    # MOUSE MODE
    if mode == "MOUSE":

        img = mouse.control_mouse(img, lmList)

    # VOLUME MODE
    elif mode == "VOLUME":

        img = volume.control_volume(img, lmList)

    # IDLE MODE
    else:

        cv2.putText(
            img,
            "SYSTEM IDLE",
            (450, 350),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            4
        )

    # =====================================
    # BOTTOM GUIDE PANEL
    # =====================================


    # =====================================
    # SHOW WINDOW
    # =====================================

    cv2.imshow("AI Gesture Control System", img)

    # Quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =====================================
# RELEASE
# =====================================

cap.release()

cv2.destroyAllWindows()