from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class ActorSubTitleLabel(QLabel):
    def __init__(self, content):
        super(ActorSubTitleLabel, self).__init__()
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.setStyleSheet("QLabel { background-color : #fcf7f7; color : #128bb5; }")
        self.setMargin(10)
        self.setText(content)
        self.setWordWrap(True)
        self.setFont(font)