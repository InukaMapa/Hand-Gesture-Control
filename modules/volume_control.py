import math
import numpy as np
import cv2

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl:

    def __init__(self):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        volRange = self.volume.GetVolumeRange()

        self.minVol = volRange[0]
        self.maxVol = volRange[1]

    def control_volume(self, img, lmList):

        if len(lmList) == 0:
            return img

        # Thumb tip
        x1, y1 = lmList[4][1], lmList[4][2]

        # Index tip
        x2, y2 = lmList[8][1], lmList[8][2]

        # Draw points
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

        # Draw line
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Distance
        length = math.hypot(x2 - x1, y2 - y1)

        # Convert to volume
        vol = np.interp(
            length,
            [20, 200],
            [self.minVol, self.maxVol]
        )

        self.volume.SetMasterVolumeLevel(vol, None)

        # Volume percentage
        volPer = int(np.interp(length, [20, 200], [0, 100]))

        # Volume bar
        volBar = np.interp(length, [20, 200], [400, 150])

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)

        cv2.rectangle(
            img,
            (50, int(volBar)),
            (85, 400),
            (0, 255, 0),
            cv2.FILLED
        )

        cv2.putText(
            img,
            f'{volPer}%',
            (40, 450),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        return img