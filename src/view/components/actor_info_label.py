from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel
from src.controllers.actor_controller import getOneActorInfoById


class ActorInfoLabel(QLabel):
    def __init__(self, content):
        super(ActorInfoLabel, self).__init__()
        font = QFont()
        font.setPointSize(15)
        self.setStyleSheet("QLabel { background-color : white; color : black; }")
        self.setMargin(10)
        self.setText(content)
        self.setWordWrap(True)
        self.setFont(font)