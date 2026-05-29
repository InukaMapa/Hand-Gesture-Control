import cv2
import pyautogui
import math
import time


class MouseControl:

    def __init__(self):

        # Screen size
        self.screen_w, self.screen_h = pyautogui.size()

        # Smooth movement
        self.prev_x = 0
        self.prev_y = 0

        self.smoothening = 5

        # Click state
        self.left_clicking = False
        self.right_clicking = False

        # Click delay
        self.last_click_time = 0
        self.click_delay = 0.4

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

        # Use the actual frame size from the current image
        frame_h, frame_w, _ = img.shape

        screen_x = int((x1 / frame_w) * self.screen_w)
        screen_y = int((y1 / frame_h) * self.screen_h)

        # Keep coordinates inside the screen bounds
        screen_x = max(0, min(self.screen_w - 1, screen_x))
        screen_y = max(0, min(self.screen_h - 1, screen_y))

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

        # Estimate hand size to adapt thresholds for different distances from the camera
        wrist_x, wrist_y = lmList[0][1], lmList[0][2]
        middle_mcp_x, middle_mcp_y = lmList[9][1], lmList[9][2]
        hand_size = max(20, math.hypot(wrist_x - middle_mcp_x, wrist_y - middle_mcp_y))

        left_click_threshold = max(20, min(70, int(hand_size * 0.35)))
        right_click_threshold = max(20, min(70, int(hand_size * 0.30)))

        left_pinch = left_distance < left_click_threshold

        if left_pinch and not self.left_clicking and not self.right_clicking:
            current_time = time.time()

            if current_time - self.last_click_time > self.click_delay:
                pyautogui.click()
                self.left_clicking = True
                self.right_clicking = False
                self.last_click_time = current_time

        if not left_pinch:
            self.left_clicking = False

        if self.left_clicking:
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
        right_pinch = (
            right_distance < right_click_threshold
            and left_distance > left_click_threshold * 0.6
        )

        if right_pinch and not self.right_clicking and not self.left_clicking:
            current_time = time.time()

            if current_time - self.last_click_time > self.click_delay:
                pyautogui.rightClick()
                self.right_clicking = True
                self.left_clicking = False
                self.last_click_time = current_time

        if not right_pinch:
            self.right_clicking = False

        if self.right_clicking:
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