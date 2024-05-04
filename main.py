import json
import logging

import requests
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem
from qfluentwidgets import FluentWindow, FluentIcon, ImageLabel, SubtitleLabel, CaptionLabel, TextEdit, LineEdit, \
    setFont, PushButton, ToolButton, ListWidget

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(asctime)s: %(message)s",
                    datefmt="%Y-%m-%d %A %H:%M:%S")


class HomeWindow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        leftLayout = QVBoxLayout(self)
        rightLayout = QVBoxLayout(self)

        cover = 'resource/logo.png'
        self.image = ImageLabel(cover, self)
        self.image.scaledToHeight(450)
        self.image.setBorderRadius(8, 8, 8, 8)
        leftLayout.addWidget(self.image)

        self.label = CaptionLabel("Lutalica", self)
        setFont(self.label, 64)
        rightLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)


class subWindow1(QFrame):
    addItemSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.aliveHosts = set()

        layout = QHBoxLayout(self)
        leftLayout = QVBoxLayout(self)
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
        self.scanButton = PushButton("开始扫描", self)
        self.stopButton = PushButton("停止扫描", self)
        self.scanState = "stopped"
        targetLayout.addWidget(self.targetLabel)
        targetLayout.addWidget(self.icon)
        targetLayout.addWidget(self.target)
        targetLayout.addWidget(self.scanButton)
        targetLayout.addWidget(self.stopButton)
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
        self.endLabel = CaptionLabel("最大值", self)
        setFont(self.endLabel, 18)
        self.end = LineEdit()
        self.end.setFixedWidth(100)
        self.end.setPlaceholderText("最大值")
        paramLayout.addWidget(self.endLabel)
        paramLayout.addWidget(self.end)
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

        listContainer = QWidget()
        listLayout = QHBoxLayout(listContainer)
        self.listLabel = CaptionLabel("[+]靶机列表", self)
        setFont(self.listLabel, 18)
        self.clearButton = PushButton("清空", self)
        self.clearButton.setFixedWidth(100)
        listLayout.addWidget(self.listLabel)
        listLayout.addWidget(self.clearButton)
        leftLayout.addWidget(listContainer)

        self.list = ListWidget(self)
        self.list.setFixedHeight(320)
        self.addItemSlot("存活靶机")
        leftLayout.addWidget(self.list)
        leftLayout.setStretchFactor(self.list, 1)
        leftLayout.addStretch(1)

        self.logLabel = CaptionLabel("[*]扫描日志", self)
        self.logLabel.setFixedHeight(50)
        setFont(self.logLabel, 20)
        rightLayout.addWidget(self.logLabel)
        self.log = TextEdit()
        textFont = QFont()
        textFont.setPointSize(14)
        self.log.setFont(textFont)
        self.log.setMinimumWidth(350)
        self.log.setReadOnly(True)
        rightLayout.addWidget(self.log)

        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        self.loadHosts()
        self.scanButton.clicked.connect(self.startScan)
        self.stopButton.clicked.connect(self.stopScan)
        self.clearButton.clicked.connect(self.clearHosts)
        self.addItemSignal.connect(self.addItemSlot)

    def addItemSlot(self, item):
        try:
            item = QListWidgetItem(item)
            itemFont = QFont()
            itemFont.setPointSize(14)
            item.setFont(itemFont)
            self.list.addItem(item)
        except Exception as e:
            logging.error(e)
            pass

    def loadHosts(self):
        try:
            with open('./data/ip.json', 'r') as f:
                hosts = json.load(f)
                for host in hosts:
                    ip = host["ip"]
                    self.aliveHosts.add(ip)
                    self.addItemSlot(ip)
        except Exception as e:
            logging.error(e)
            pass

    def saveHosts(self):
        try:
            with open('./data/ip.json', 'w') as f:
                hosts = [{"ip": host} for host in self.aliveHosts]
                json.dump(hosts, f)
        except Exception as e:
            logging.error(e)
            pass

    def startScan(self):
        self.scanState = "running"
        self.HostScan()

    def stopScan(self):
        self.scanState = "stopped"

    def HostScan(self):
        target = self.target.text()
        start = self.start.text()
        end = self.end.text()
        step = self.step.text()
        ignore = self.ignore.text()
        start = int(start) if start.isdigit() else 0
        end = int(end) if end.isdigit() else 0
        step = int(step) if step.isdigit() else 1
        ignore = int(ignore) if ignore.isdigit() else 0

        self.log.append(f"[*] 开始扫描")
        for X in range(start, end + 1, step):
            if self.scanState == "stopped":
                self.log.append("[-] 扫描已停止")
                logging.info("[-] 扫描已停止")
                break
            if X != ignore:
                url = target.format(X=X)
                try:
                    requests.head(url, timeout=0.3)
                    if url not in self.aliveHosts:
                        self.aliveHosts.add(url)
                        self.addItemSignal.emit(url)
                        self.log.append(f"{url} 存活")
                        QApplication.processEvents()
                        logging.info(f"{url} 存活")
                    else:
                        self.log.append(f"{url} 已存在")
                        QApplication.processEvents()
                        logging.warning(f"{url} 已存在")
                except Exception as e:
                    self.log.append(f"{url} 无法访问")
                    logging.error(e)
                    QApplication.processEvents()
                    logging.warning(f"{url} 无法访问")
                    pass
        self.log.append("[-] 扫描结束\n")
        logging.info("[-] 扫描结束\n")
        self.saveHosts()

    def clearHosts(self):
        self.list.clear()
        self.addItemSlot("存活靶机")
        with open('./data/ip.json', 'w') as f:
            json.dump([], f)


class App(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lutalica")
        self.setWindowIcon(QIcon('resource/logo.png'))

        self.home = HomeWindow()
        self.home.setObjectName("Home")
        self.addSubInterface(self.home, FluentIcon.HOME, "主页")

        self.window1 = subWindow1()
        self.window1.setObjectName("Window1")
        self.addSubInterface(self.window1, FluentIcon.HISTORY, "靶机扫描")
        self.showMaximized()


def run():
    try:
        app = QApplication([])
        # app.setFont(QFont("HarmonyOS Sans SC"))
        window = App()
        window.show()
        app.exec()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    run()
