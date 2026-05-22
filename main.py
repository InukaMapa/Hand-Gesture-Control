import cv2

from modules.hand_tracker import HandTracker

cap = cv2.VideoCapture(0)

tracker = HandTracker()

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)

    img = tracker.find_hands(img)

    lmList = tracker.find_position(img)

    # Test index finger
    if len(lmList) != 0:

        x, y = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Gesture System", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break