import cv2
import pyautogui
import math
import time


class MouseControl:

    def __init__(self):

        # Screen size
        self.screen_w, self.screen_h = pyautogui.size()

        # Camera size
        self.cam_w = 640
        self.cam_h = 480

        # Smooth movement
        self.prev_x = 0
        self.prev_y = 0

        self.smoothening = 5

        # Click delay
        self.last_click_time = 0
        self.click_delay = 0.5

    def control_mouse(self, img, lmList):

        if len(lmList) == 0:
            return img

        # Index finger tip
        x1, y1 = lmList[8][1], lmList[8][2]

        # Middle finger tip
        x2, y2 = lmList[12][1], lmList[12][2]

        # Thumb tip
        x_thumb, y_thumb = lmList[4][1], lmList[4][2]

        # -------------------------
        # MOUSE MOVEMENT
        # -------------------------

        screen_x = int((x1 / self.cam_w) * self.screen_w)
        screen_y = int((y1 / self.cam_h) * self.screen_h)

        # Smooth movement
        curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x = curr_x
        self.prev_y = curr_y

        # Draw cursor
        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)

        # -------------------------
        # LEFT CLICK
        # Thumb + Index pinch
        # -------------------------

        left_distance = math.hypot(x_thumb - x1, y_thumb - y1)

        if left_distance < 35:

            current_time = time.time()

            if current_time - self.last_click_time > self.click_delay:

                pyautogui.click()

                self.last_click_time = current_time

                cv2.putText(
                    img,
                    "LEFT CLICK",
                    (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

        # -------------------------
        # RIGHT CLICK
        # Index + Middle pinch
        # -------------------------

        right_distance = math.hypot(x1 - x2, y1 - y2)

        if right_distance < 30:

            current_time = time.time()

            if current_time - self.last_click_time > self.click_delay:

                pyautogui.rightClick()

                self.last_click_time = current_time

                cv2.putText(
                    img,
                    "RIGHT CLICK",
                    (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

        # Mode label
        cv2.putText(
            img,
            "MOUSE MODE",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            3
        )

        return img