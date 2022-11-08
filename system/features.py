import asyncio
import pyautogui
from python_imagesearch.imagesearch import imagesearch


class Features:
    def __init__(self, pytesseract, kakelebot):
        self.pytesseract = pytesseract
        self.KakeleBot = kakelebot

        self.thread_vida = None
        self.thread_mana = None
        self.thread_hur = None
        self.thread_auto = None

        self.flags = {'life': None,
                      'mana': None,
                      'haste': False}

        self.anti_exausted = 0.668
        self.time_haste = 29
        self.FPS = 0.02
        self.error = 99999

    @classmethod
    async def remove_suffix_n(cls, string):
        while '\n' in string[-1]:
            string = string.removesuffix('\n')
        return string

    async def img_to_string(self, img):
        string = self.pytesseract.image_to_string(img, config='--psm 6 digits')
        if len(string) <= 0:
            return '_'
        return await self.remove_suffix_n(string)

    @classmethod
    async def take_point_remove(cls, strg):
        return [letter.strip('.').strip(',') for letter in strg]

    @classmethod
    async def take_insert_bar(cls, pipe):
        pipe.insert(int(len(pipe) / 2), '/')
        return pipe

    @classmethod
    async def take_split_bar(cls, pipe):
        pipe = ''.join(pipe)
        return [int(XY) for XY in pipe.split('/') if XY.isdigit()]

    async def take_issuccess(self, pipe):
        if len(pipe) < 2:
            pipe = [self.error, self.error]
        return pipe

    async def take_numbers_bar(self, barra):
        img = await self.KakeleBot.screenshot(barra)
        strg = await self.img_to_string(img)
        pipe = await self.take_point_remove(strg)
        pipe = await self.take_insert_bar(pipe)
        pipe = await self.take_split_bar(pipe)
        pipe = await self.take_issuccess(pipe)

        return pipe

    async def vida_limit(self, life):
        if life[0] <= self.KakeleBot.slider_vida.value():
            hk = self.KakeleBot.pushButton_hotkey_vida.text().lower().split('-')[1].strip()

            if not self.tem_hk_alert(hk, 'Vida'):
                return None

            self.KakeleBot.keyboard.send(hk)
            await asyncio.sleep(self.anti_exausted)

    async def vida_update(self, life):
        if not self.flags['life'] and life[1] != self.error:
            self.KakeleBot.label_vida.setText(f'{life[0]}/{life[1]}')
            self.KakeleBot.slider_vida.setMaximum(life[1])
            self.flags['life'] = life[1]
        else:
            self.KakeleBot.label_vida.setText(f'{life[0]}/{self.flags["life"]}')

    async def vida_on(self):
        while self.thread_vida:
            await self.sleep_bot()

            life = await self.take_numbers_bar(self.KakeleBot.take('vida'))
            await self.vida_update(life)

            await self.release_haste()

            await self.vida_limit(life)
            await asyncio.sleep(self.FPS)

    async def mana_limit(self, mana):
        if mana[0] <= self.KakeleBot.slider_mana.value():
            hk = self.KakeleBot.pushButton_hotkey_mana.text().lower().split('-')[1].strip()

            if not self.tem_hk_alert(hk, 'Mana'):
                return None

            self.KakeleBot.keyboard.send(hk)
            await asyncio.sleep(self.anti_exausted)

    async def mana_update(self, mana):
        if not self.flags['mana'] and mana[1] != self.error:
            self.KakeleBot.label_mana.setText(f'{mana[0]}/{mana[1]}')
            self.KakeleBot.slider_mana.setMaximum(mana[1])
            self.flags['mana'] = mana[1]
        else:
            self.KakeleBot.label_mana.setText(f'{mana[0]}/{self.flags["mana"]}')

    async def mana_on(self):
        while self.thread_mana:
            await self.sleep_bot()

            mana = await self.take_numbers_bar(self.KakeleBot.take('mana'))

            await self.mana_update(mana)

            await self.release_haste()

            await self.mana_limit(mana)
            await asyncio.sleep(self.FPS)

    async def release_haste(self):
        while self.flags['haste']:
            await asyncio.sleep(self.anti_exausted)
            self.flags['haste'] = False
            break

    async def hur_on(self):
        while self.thread_hur:
            await self.sleep_bot()

            self.flags['haste'] = True

            await asyncio.sleep(self.anti_exausted)
            hk = self.KakeleBot.pushButton_hotkey_hur.text().lower().split('-')[1].strip()

            if not self.tem_hk_alert(hk, 'Aceleração'):
                continue

            self.KakeleBot.keyboard.send(hk)
            await asyncio.sleep(self.time_haste)

    async def auto_attack(self):
        await self.sleep_bot()

        while self.thread_auto:
            await self.sleep_bot()

            pos = self.KakeleBot.target()
            target = imagesearch('./comp_out/targets/enemy.png')

            if not (pos[0] == target[0] and pos[1] == target[1]):
                self.KakeleBot.keyboard.send('space')
            await asyncio.sleep(1)

    async def sleep_bot(self):
        while not self.KakeleBot.KAKELE.isActive:
            await asyncio.sleep(3)

    @staticmethod
    def tem_hk_alert(hk, titulo):
        if hk == 'vazio':
            pyautogui.alert(text='Escolha um atalho', title=titulo, button='OK')
            return False
        return True
