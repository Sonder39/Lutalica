from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ImageLabel, CaptionLabel, setFont


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
