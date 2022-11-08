import asyncio
import sys
import threading

import pyautogui
import pytesseract
import keyboard

from system.downloads import download_tesseract
from system.features import Features
from system.healing import Barras
from system.hunt import CaveBot

from PyQt6.QtWidgets import QMainWindow, QApplication
from forms.bot_window_ui import Ui_MainWindow

download_tesseract()
pytesseract.pytesseract.tesseract_cmd = './comp_out/tesseract/tesseract'


class KakeleBot(QMainWindow,
                Ui_MainWindow,
                Features,
                Barras,
                CaveBot):

    def __init__(self, parent=None):
        super(KakeleBot, self).__init__(parent=parent)
        self.setupUi(self)
        self.keyboard = keyboard

        # O segundo self, é a instância KakeleBot
        Features.__init__(self, pytesseract, self)
        Barras.__init__(self)
        CaveBot.__init__(self, self)

        self.slider_vida.valueChanged.connect(self.on_change_pontos_vida)
        self.checkBox_ligar_vida.clicked.connect(self.on_click_ligar_vida)
        self.pushButton_hotkey_vida.clicked.connect(self.on_click_hk_vida)

        self.slider_mana.valueChanged.connect(self.on_change_pontos_mana)
        self.checkBox_ligar_mana.clicked.connect(self.on_click_ligar_mana)
        self.pushButton_hotkey_mana.clicked.connect(self.on_click_hk_mana)

        self.checkBox_ligar_hur.clicked.connect(self.on_click_ligar_hur)
        self.pushButton_hotkey_hur.clicked.connect(self.on_click_hk_hur)

        self.checkBox_auto_atk.clicked.connect(self.on_click_ligar_auto_atk)
        self.pushButton_ligar_registro.clicked.connect(self.on_click_ligar_registro)
        self.checkBox_load_way.clicked.connect(self.on_click_ligar_load_way)

    def on_click_ligar_vida(self):
        if not self.thread_vida:
            self.thread_vida = threading.Thread(target=asyncio.run, args=[self.vida_on()])
            self.thread_vida.start()
        else:
            self.thread_vida = None

    def on_click_ligar_mana(self):
        if not self.thread_mana:
            self.thread_mana = threading.Thread(target=asyncio.run, args=[self.mana_on()])
            self.thread_mana.start()
        else:
            self.thread_mana = None

    def on_click_ligar_hur(self):
        if not self.thread_hur:
            self.thread_hur = threading.Thread(target=asyncio.run, args=[self.hur_on()])
            self.thread_hur.start()
        else:
            self.thread_hur = None

    def on_click_ligar_auto_atk(self):
        if not self.thread_auto:
            self.thread_auto = threading.Thread(target=asyncio.run, args=[self.auto_attack()])
            self.thread_auto.start()
        else:
            self.thread_auto = None

    def on_click_ligar_registro(self):
        if not self.thread_waypoint and not self.thread_loadway:
            self.thread_waypoint = threading.Thread(target=self.start_way)
            self.thread_waypoint.start()
            self.config['map_1']['way'].clear()
            self.pushButton_ligar_registro.setText('Parar registro')
        else:
            self.thread_waypoint = None
            self.py_direct_input.press('esc')
            self.save_way()
            self.pushButton_ligar_registro.setText('Iniciar novos waypoints')

    def on_click_ligar_load_way(self):
        if not self.thread_loadway and not self.thread_waypoint:
            self.thread_loadway = threading.Thread(target=asyncio.run, args=[self.auto_walk()])
            self.thread_loadway.start()
        else:
            self.thread_loadway = None

    def on_click_hk_vida(self):
        threading.Thread(target=self.get_hk,
                         args=[self.pushButton_hotkey_vida]).start()
        self.pushButton_hotkey_vida.setStyleSheet("background-color: orange")

    def on_click_hk_mana(self):
        threading.Thread(target=self.get_hk,
                         args=[self.pushButton_hotkey_mana]).start()
        self.pushButton_hotkey_mana.setStyleSheet("background-color: orange")

    def on_click_hk_hur(self):
        threading.Thread(target=self.get_hk,
                         args=[self.pushButton_hotkey_hur]).start()
        self.pushButton_hotkey_hur.setStyleSheet("background-color: orange")

    def on_change_pontos_vida(self):
        self.label_pontoMax_vida.setText(str(self.slider_vida.value()))

    def on_change_pontos_mana(self):
        self.label_pontoMax_mana.setText(str(self.slider_mana.value()))

    def get_hk(self, push_hk):
        hk = self.keyboard.read_key().upper()
        label_hk = push_hk.text().split('-')[0].strip()

        push_hk.setStyleSheet("background-color: (160, 0, 212)")
        push_hk.setText(f'{label_hk} - {hk}')

2
""" INICIAR O BOT DIRETAMENTE SEM LOGIN"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    try:
        win = KakeleBot()
        win.show()
    except IndexError:
        pyautogui.alert(text='Inicie o Kakele antes de abrir o Bot',
                        title='Autenticação',
                        button='OK')
        sys.exit()
    sys.exit(app.exec())
""" INICIAR O BOT DIRETAMENTE SEM LOGIN"""
