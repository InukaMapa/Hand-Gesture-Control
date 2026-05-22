import cv2
import mediapipe as mp
import math
import numpy as np
import time

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Camera
cap = cv2.VideoCapture(0)

# MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpDraw = mp.solutions.drawing_utils

# Volume setup
devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

pTime =  0
smoothness = 5
currentVol = 0

while True:

    success, img = cap.read()

    if not success:
        break

    # Convert image to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process image
    results = hands.process(imgRGB)

    # Detect hands
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            # Draw hand landmarks
            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS
            )

            # Default coordinates
            thumb_x, thumb_y = 0, 0
            index_x, index_y = 0, 0

            # Get landmark positions
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Thumb tip
                if id == 4:
                    thumb_x, thumb_y = cx, cy

                    cv2.circle(
                        img,
                        (cx, cy),
                        15,
                        (255, 0, 255),
                        cv2.FILLED
                    )

                # Index finger tip
                if id == 8:
                    index_x, index_y = cx, cy

                    cv2.circle(
                        img,
                        (cx, cy),
                        15,
                        (255, 0, 255),
                        cv2.FILLED
                    )

            # Draw line between fingers
            cv2.line(
                img,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (0, 255, 0),
                3
            )

            # Midpoint circle
            center_x = (thumb_x + index_x) // 2
            center_y = (thumb_y + index_y) // 2

            cv2.circle(
                img,
                (center_x, center_y),
                10,
                (0, 255, 0),
                cv2.FILLED
            )

            # Distance calculation
            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )

            # Convert distance to volume
            vol = np.interp(
                distance,
                [20, 200],
                [minVol, maxVol]
            )

            currentVol = currentVol + (vol - currentVol) / smoothness
            volume.SetMasterVolumeLevel(currentVol, None)

            # Volume percentage
            volPercent = np.interp(
                distance,
                [20, 200],
                [0, 100]
            )
            volBar = np.interp(
                 distance,
                [20, 200],
                [400, 150]
        )

            # Show volume text
            cv2.putText(
                img,
                f'Volume: {int(volPercent)}%',
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3
            )
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(
                img,
                f'FPS: {int(fps)}',
                (40, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                3
           )
            # Volume bar outline
            cv2.rectangle(
              img,
             (50, 150),
             (85, 400),
            (0, 255, 0),
             3
            )

            # Filled volume bar
            cv2.rectangle(
                img,
                (50, int(volBar)),
                (85, 400),
                (0, 255, 0),
                cv2.FILLED
            )
            cv2.imshow("Hand Gesture Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()