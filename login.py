import os
import sys
import pyautogui

from datetime import datetime
from pymongo import MongoClient

from PyQt6.QtWidgets import QMainWindow, QApplication
from forms.login_window_ui import Ui_MainWindow
from main import KakeleBot

mongodb = MongoClient(os.environ['HOST'])
db = mongodb.KAKELEBOT


class Login(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__(parent=None)
        self.setupUi(self)
        self.bot = KakeleBot()

        self.lineEdit_login.setFocus()
        self.pushButton_conectar.clicked.connect(self.on_click_login)

    def on_click_login(self):
        login = self.lineEdit_login.text()
        senha = self.lineEdit_senha.text()

        user = db.usuarios.find_one({'login': login})
        if user:
            if datetime.now().timestamp() > user['expiracao']:
                pyautogui.alert(text='Sua conta expirou', title='Autenticação', button='OK')
            elif user['senha'] == senha:
                self.bot.show()
                self.close()
            else:
                pyautogui.alert(text='Senha incorreta',
                                title='Autenticação',
                                button='OK')
        else:
            pyautogui.alert(text='Login não encontrado',
                            title='Autenticação',
                            button='OK')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    try:
        win = Login()
        win.show()
    except IndexError:
        pyautogui.alert(text='Inicie o Kakele antes de abrir o Bot',
                        title='Autenticação',
                        button='OK')
        sys.exit()
    sys.exit(app.exec())
