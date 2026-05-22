import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:

            for handLms in self.results.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

        return img

    def find_position(self, img):

        lmList = []

        if self.results.multi_hand_landmarks:

            hand = self.results.multi_hand_landmarks[0]

            for id, lm in enumerate(hand.landmark):

                h, w, c = img.shape

                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])

        return lmList