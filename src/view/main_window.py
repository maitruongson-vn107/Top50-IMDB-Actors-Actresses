import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QScrollArea
from actor_main_table import ActorMainTable
from general_info_tab import GeneralInfoTab


class MainWindowBanner(QLabel):
    def __init__(self, text):
        super(MainWindowBanner, self).__init__()
        self.setGeometry(0, 0, 100, 100)
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.setSpacing(5)

        # ACTOR MAIN TABLE: List of Top 50 Actors/Actresses
        actor_main_table = ActorMainTable()
        hbox.addWidget(actor_main_table)

        # GENERAL INFO TAB: Basic statistics of 50 actors/actresses
        general_info_tab = GeneralInfoTab()
        general_info_widget = QWidget()
        general_info_widget.setLayout(general_info_tab)
        general_info_widget.setFixedWidth(390)
        general_info_scroll = QScrollArea()
        general_info_scroll.setFixedWidth(400)
        general_info_scroll.setWidget(general_info_widget)

        hbox.addWidget(general_info_scroll)

        self.setLayout(hbox)

        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('IMDB TOP 50')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()