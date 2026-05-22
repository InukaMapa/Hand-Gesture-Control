import time


class GestureManager:

    def __init__(self):

        self.current_mode = None

        self.last_switch_time = 0

        self.switch_cooldown = 2

    # -----------------------------------
    # FINGER DETECTION
    # -----------------------------------

    def get_fingers(self, lmList):

        fingers = []

        # Thumb
        fingers.append(
            1 if abs(lmList[4][1] - lmList[3][1]) > 30 else 0
        )

        # Index
        fingers.append(
            1 if lmList[8][2] < lmList[6][2] else 0
        )

        # Middle
        fingers.append(
            1 if lmList[12][2] < lmList[10][2] else 0
        )

        # Ring
        fingers.append(
            1 if lmList[16][2] < lmList[14][2] else 0
        )

        # Pinky
        fingers.append(
            1 if lmList[20][2] < lmList[18][2] else 0
        )

        return fingers

    # -----------------------------------
    # MODE DETECTION
    # -----------------------------------

    def detect_mode(self, lmList):

        if len(lmList) == 0:
            return self.current_mode

        fingers = self.get_fingers(lmList)

        current_time = time.time()

        # Prevent fast switching
        if current_time - self.last_switch_time < self.switch_cooldown:
            return self.current_mode

        # -----------------------------------
        # MOUSE MODE
        # ✌️ Two fingers
        # -----------------------------------

        if fingers == [0, 1, 1, 0, 0]:

            self.current_mode = "MOUSE"

            self.last_switch_time = current_time

        # -----------------------------------
        # VOLUME MODE
        # ☝️ One finger
        # -----------------------------------

        elif fingers == [0, 1, 0, 0, 0]:

            self.current_mode = "VOLUME"

            self.last_switch_time = current_time

        # -----------------------------------
        # EXIT MODE
        # ✋ Open hand
        # -----------------------------------

        elif fingers == [1, 1, 1, 1, 1]:

            self.current_mode = None

            self.last_switch_time = current_time

        return self.current_mode