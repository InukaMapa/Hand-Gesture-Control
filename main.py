import cv2

from modules.hand_tracker import HandTracker
from modules.virtual_keyboard import VirtualKeyboard
from modules.volume_control import VolumeControl
from modules.mouse_control import MouseControl
from modules.gesture_manager import GestureManager

cap = cv2.VideoCapture(0)

tracker = HandTracker()

keyboard = VirtualKeyboard()
volume = VolumeControl()
mouse = MouseControl()

gesture_manager = GestureManager()

while True:

    success, img = cap.read()

    if not success:
        continue

    img = cv2.flip(img, 1)

    # Hand detection
    img = tracker.find_hands(img)

    # Landmarks
    lmList = tracker.find_position(img)

    # Detect mode
    mode = gesture_manager.detect_mode(lmList)

    # Show current mode
    cv2.putText(
        img,
        f"MODE: {mode}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        3
    )

    # Keyboard Mode
    if mode == "KEYBOARD":

        img = keyboard.draw_keyboard(img)

        img = keyboard.detect_key_press(img, lmList)

    # Volume Mode
    elif mode == "VOLUME":

        img = volume.control_volume(img, lmList)

    # Mouse Mode
    elif mode == "MOUSE":

        img = mouse.control_mouse(img, lmList)

    cv2.imshow("AI Gesture System", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()