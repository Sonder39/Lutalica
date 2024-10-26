import logging

from PyQt6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme

from pages.app import App

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %A %H:%M:%S"
)

try:
    app = QApplication([])
    setTheme(Theme.AUTO)
    window = App()
    window.show()
    app.exec()
except Exception as e:
    logging.error(e)
    pass
