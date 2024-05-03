import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QFrame)
from qfluentwidgets import FluentWindow, FluentIcon, setFont, CaptionLabel

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class HomeWindow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout(self)
        self.label = CaptionLabel("Lutalica", self)
        setFont(self.label, 64)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)


class App(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lutalica")
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.home = HomeWindow()
        self.home.setObjectName("Home")
        self.addSubInterface(self.home, FluentIcon.HOME, "主页")


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
