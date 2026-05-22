import cv2
import pyautogui


class MouseControl:

    def control_mouse(self, img, lmList):

        if len(lmList) == 0:
            return img

        x, y = lmList[8][1], lmList[8][2]

        screen_w, screen_h = pyautogui.size()

        cam_x = int((x / 640) * screen_w)
        cam_y = int((y / 480) * screen_h)

        pyautogui.moveTo(cam_x, cam_y)

        cv2.putText(
            img,
            "MOUSE MODE",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        return img