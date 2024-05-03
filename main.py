import logging

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (QApplication)
from qfluentwidgets import FluentWindow

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class App(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lutalica")
        self.setWindowIcon(QIcon('resource/logo.png'))


def run():
    try:
        app = QApplication([])
        app.setFont(QFont("HarmonyOS Sans SC"))
        window = App()
        window.show()
        app.exec()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    run()
