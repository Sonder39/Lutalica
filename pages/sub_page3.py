import json
import logging

import requests
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem
from qfluentwidgets import FluentIcon, ImageLabel, SubtitleLabel, CaptionLabel, TextEdit, LineEdit, \
    setFont, PushButton, ToolButton, ListWidget


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
