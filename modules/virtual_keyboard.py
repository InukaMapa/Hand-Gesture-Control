import cv2
import pyautogui


class VirtualKeyboard:

    def __init__(self):

        self.keys = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        self.finalText = ""

    def draw_keyboard(self, img):

        for i in range(len(self.keys)):

            for j, key in enumerate(self.keys[i]):

                x = 50 + j * 70
                y = 50 + i * 70

                cv2.rectangle(
                    img,
                    (x, y),
                    (x + 60, y + 60),
                    (255, 0, 255),
                    cv2.FILLED
                )

                cv2.putText(
                    img,
                    key,
                    (x + 18, y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )

        return img

    def detect_key_press(self, img, lmList):

        if len(lmList) == 0:
            return img

        # Index finger tip
        x, y = lmList[8][1], lmList[8][2]

        # Draw cursor
        cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)

        for i in range(len(self.keys)):

            for j, key in enumerate(self.keys[i]):

                keyX = 50 + j * 70
                keyY = 50 + i * 70

                # Hover detection
                if keyX < x < keyX + 60 and keyY < y < keyY + 60:

                    cv2.rectangle(
                        img,
                        (keyX, keyY),
                        (keyX + 60, keyY + 60),
                        (0, 255, 0),
                        cv2.FILLED
                    )

                    cv2.putText(
                        img,
                        key,
                        (keyX + 18, keyY + 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2
                    )

                    # TEMP TEST PRESS
                    self.finalText += key

                    pyautogui.press(key.lower())

        # Text display
        cv2.rectangle(
            img,
            (50, 300),
            (1000, 400),
            (175, 0, 175),
            cv2.FILLED
        )

        cv2.putText(
            img,
            self.finalText,
            (60, 370),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            3
        )

        return img