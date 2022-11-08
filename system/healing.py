# import asyncio

import numpy as np
import cv2
import pyautogui
import pygetwindow as gw


class Barras:
    def __init__(self):
        self.KAKELE = gw.getWindowsWithTitle('Kakele')[0]

    def take(self, nome):
        distance = 65 if nome == 'mana' else 35
        x0 = self.KAKELE.box.left + (self.KAKELE.width - (self.KAKELE.width - 95))
        x1 = self.KAKELE.width - (self.KAKELE.width - 194)
        y0 = self.KAKELE.box.top + (self.KAKELE.height - (self.KAKELE.height - distance))
        y1 = self.KAKELE.height - (self.KAKELE.height - 26)

        return x0, y0, x1, y1

    @classmethod
    async def screenshot(cls, barra):
        img = pyautogui.screenshot(region=barra)
        white_black = img.convert('L')
        white_black = np.array(white_black)

        (h, w) = white_black.shape[:2]
        white_black = cv2.resize(white_black, (w * 2, h * 2))

        black_white = cv2.threshold(np.array(white_black), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # cv2.imwrite('target.png', black_white)

        return black_white

    def target(self):
        x0 = self.KAKELE.box.left + 92
        y0 = self.KAKELE.box.top + 145

        return x0, y0


# b = Barras()
# asyncio.run(b.screenshot(b.teste()))


