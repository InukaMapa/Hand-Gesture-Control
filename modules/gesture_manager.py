class GestureManager:

    def __init__(self):

        self.current_mode = "NONE"

    def detect_mode(self, lmList):

        if len(lmList) == 0:
            return self.current_mode

        # Finger tips
        index_tip = lmList[8][2]
        middle_tip = lmList[12][2]
        ring_tip = lmList[16][2]
        pinky_tip = lmList[20][2]

        # Finger joints
        index_joint = lmList[6][2]
        middle_joint = lmList[10][2]
        ring_joint = lmList[14][2]
        pinky_joint = lmList[18][2]

        # Finger states
        index_up = index_tip < index_joint
        middle_up = middle_tip < middle_joint
        ring_up = ring_tip < ring_joint
        pinky_up = pinky_tip < pinky_joint

        # ☝️ Keyboard Mode
        if index_up and not middle_up:
            self.current_mode = "KEYBOARD"

        # ✌️ Mouse Mode
        elif index_up and middle_up:
            self.current_mode = "MOUSE"

        # 🤏 Volume Mode
        elif not index_up and not middle_up:
            self.current_mode = "VOLUME"

        return self.current_mode