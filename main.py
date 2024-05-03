import logging

import requests
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QListWidgetItem
from qfluentwidgets import FluentWindow, FluentIcon, ImageLabel, SubtitleLabel, setFont, CaptionLabel, TextEdit, \
    LineEdit, PushButton, ToolButton, ListWidget

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


class subWindow1(QFrame):
    addItemSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        layout = QHBoxLayout(self)
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout(self)

        cover = 'resource/Archive1.png'
        self.image = ImageLabel(cover, self)
        self.image.scaledToHeight(290)
        self.image.setBorderRadius(8, 8, 8, 8)
        leftLayout.addWidget(self.image)

        subtitleLabel = '靶机扫描'
        self.subtitle = SubtitleLabel(subtitleLabel, self)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        setFont(self.subtitle, 24)
        self.subtitle.setFixedHeight(50)
        leftLayout.addWidget(self.subtitle, 1, Qt.AlignmentFlag.AlignLeft)

        scanContainer = QWidget()
        targetLayout = QHBoxLayout(scanContainer)
        self.targetLabel = CaptionLabel("扫描目标", self)
        setFont(self.targetLabel, 18)
        self.icon = ToolButton(self)
        self.icon.setIcon(FluentIcon.CONNECT)
        self.target = LineEdit()
        self.target.setPlaceholderText("https://192-168-1-{X}.pvp3994.bugku.cn")
        buttonText = "开始扫描"
        self.scan = PushButton(buttonText, self)
        targetLayout.addWidget(self.targetLabel)
        targetLayout.addWidget(self.icon)
        targetLayout.addWidget(self.target)
        targetLayout.addWidget(self.scan)
        leftLayout.addWidget(scanContainer)

        paramContainer = QWidget()
        paramLayout = QHBoxLayout(paramContainer)
        self.startLabel = CaptionLabel("起始值", self)
        setFont(self.startLabel, 18)
        self.start = LineEdit()
        self.start.setFixedWidth(100)
        self.start.setPlaceholderText("起始值")
        paramLayout.addWidget(self.startLabel)
        paramLayout.addWidget(self.start)
        # startLayout.addStretch(1)
        self.endLabel = CaptionLabel("最大值", self)
        setFont(self.endLabel, 18)
        self.end = LineEdit()
        self.end.setFixedWidth(100)
        self.end.setPlaceholderText("最大值")
        paramLayout.addWidget(self.endLabel)
        paramLayout.addWidget(self.end)
        # startLayout.addStretch(1)
        self.stepLabel = CaptionLabel("步进", self)
        setFont(self.stepLabel, 18)
        self.step = LineEdit()
        self.step.setFixedWidth(100)
        self.step.setPlaceholderText("步进")
        paramLayout.addWidget(self.stepLabel)
        paramLayout.addWidget(self.step)
        self.ignoreLabel = CaptionLabel("忽略值", self)
        setFont(self.ignoreLabel, 18)
        self.ignore = LineEdit()
        self.ignore.setFixedWidth(120)
        self.ignore.setPlaceholderText("忽略值[1, 39...]")
        paramLayout.addWidget(self.ignoreLabel)
        paramLayout.addWidget(self.ignore)
        paramLayout.addStretch(1)
        leftLayout.addWidget(paramContainer)

        self.listLabel = CaptionLabel("[+]靶机列表", self)
        setFont(self.listLabel, 18)
        leftLayout.addWidget(self.listLabel)
        self.list = ListWidget(self)
        font = QFont()
        font.setPointSize(18)
        item = QListWidgetItem("url")
        item.setFont(font)
        self.list.addItem(item)
        leftLayout.addWidget(self.list)
        leftLayout.setStretchFactor(self.list, 1)
        leftLayout.addStretch(1)

        self.logLabel = CaptionLabel("[*]扫描日志", self)
        setFont(self.logLabel, 18)
        rightLayout.addWidget(self.logLabel)
        self.log = TextEdit()
        self.log.setReadOnly(True)
        rightLayout.addWidget(self.log)

        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        self.scan.clicked.connect(self.HostScan)
        self.addItemSignal.connect(self.addItemSlot)

    def addItemSlot(self, item):
        self.list.addItem(item)

    def HostScan(self):
        target = self.target.text()
        start = self.start.text()
        end = self.end.text()
        step = self.step.text()
        ignore = self.step.text()
        start = int(start) if start.isdigit() else 0
        end = int(end) if end.isdigit() else 0
        step = int(step) if step.isdigit() else 1
        ignore = int(ignore) if ignore.isdigit() else 0

        for X in range(start, end + 1, step):
            if X != ignore:
                url = target.format(X=X)
                try:
                    requests.head(url, timeout=1)
                    self.addItemSignal.emit(url)
                    self.log.append(f"{url} 存活")
                    QApplication.processEvents()
                except Exception as e:
                    self.log.append(f"{url} 不存在")
                    logging.error(e)
                    QApplication.processEvents()
                    pass


class App(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lutalica")
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.showMaximized()

        self.home = HomeWindow()
        self.home.setObjectName("Home")
        self.addSubInterface(self.home, FluentIcon.HOME, "主页")

        self.window1 = subWindow1()
        self.window1.setObjectName("Window1")
        self.addSubInterface(self.window1, FluentIcon.HISTORY, "作业检查")


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
