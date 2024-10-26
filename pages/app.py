from PyQt6.QtGui import QIcon
from qfluentwidgets import FluentWindow, FluentIcon

from pages.home_page import HomeWindow
from pages.sub_page1 import subWindow1
from pages.sub_page2 import subWindow2
from pages.sub_page3 import subWindow3
from utils.event import Event


class App(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lutalica")
        self.setWindowIcon(QIcon('resource/logo.png'))

        self.home = HomeWindow()
        self.home.setObjectName("Home")
        self.addSubInterface(self.home, FluentIcon.HOME, "主页")

        updateEvent1 = Event()
        updateEvent2 = Event()
        self.window1 = subWindow1(updateEvent1)
        self.window1.setObjectName("Window1")
        self.addSubInterface(self.window1, FluentIcon.HISTORY, "靶机扫描")
        self.window2 = subWindow2(updateEvent1, updateEvent2)
        self.window2.setObjectName("Window2")
        self.addSubInterface(self.window2, FluentIcon.COMMAND_PROMPT, "后门利用")
        self.window3 = subWindow3(updateEvent2)
        self.window3.setObjectName("Window3")
        self.addSubInterface(self.window3, FluentIcon.SAVE, "批量提交")
        self.showMaximized()
