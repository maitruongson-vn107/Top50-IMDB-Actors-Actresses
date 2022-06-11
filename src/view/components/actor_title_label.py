from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class ActorTitleLabel(QLabel):
    def __init__(self, content):
        super(ActorTitleLabel, self).__init__()
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.setStyleSheet("QLabel { background-color : #deb522; color : #0c0b00; }")
        self.setMargin(10)
        self.setText(content)
        self.setWordWrap(True)
        self.setFont(font)