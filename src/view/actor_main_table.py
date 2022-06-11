from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
from src.controllers.actor_controller import getAllActors
from src.utils import text_utils
from actor_personal_window import ActorPersonalWindow


def getActorImage(actor_image_link):
    """
    From image link to QLabel widget
    :param actor_image_link: actor avatar link
    :return: QLabel containing actor's avatar
    """
    actor_image = QPixmap(actor_image_link)
    logo_label = QLabel()
    logo_label.setPixmap(actor_image.scaled(200, 200, aspectRatioMode=Qt.KeepAspectRatio))
    return logo_label


class ActorMainTable(QTableWidget):
    def __init__(self):
        super(ActorMainTable, self).__init__()
        self.actor_personal_window = None

        self.set_col_row()
        self.load_data()
        self.set_style()
        self.setHorizontalHeaderLabels(("", ""))

        self.itemDoubleClicked.connect(self.clickingHandler)

    def set_col_row(self):
        self.setColumnCount(2)
        self.setRowCount(100)

    def set_style(self):
        self.setColumnWidth(0, 200)
        self.resizeColumnToContents(0)
        self.horizontalHeader().setStretchLastSection(True)
        self.setWordWrap(True)

    def load_data(self):
        actor_list = getAllActors()
        for row in range(len(actor_list)):
            actor_record = actor_list[row]

            # ACTOR NAME
            actor_name = QTableWidgetItem(str(row + 1) + ".  " + actor_record[1])
            bold = QFont()
            bold.setBold(True)
            actor_name.setFont(bold)
            actor_name.setFlags(actor_name.flags() ^ Qt.ItemIsEditable)
            actor_name.setBackground(QColor(222, 181, 34))

            # ACTOR BIO
            actor_bio = QTableWidgetItem(text_utils.bioProcess(actor_record[8]))
            actor_bio.setFlags(actor_bio.flags() ^ Qt.ItemIsEditable)

            # ACTOR IMAGE
            actor_image_link = "../assets/actor_images/" + actor_record[1].lower().replace(" ", "").replace(".", "") + ".jpg"
            actor_image_widget = getActorImage(actor_image_link)

            self.setCellWidget(row * 2, 0, actor_image_widget)
            self.setItem(row * 2, 1, actor_name)
            self.setRowHeight(row * 2, 20)
            self.setItem(row * 2 + 1, 1, actor_bio)
            self.setRowHeight(row * 2 + 1, 180)
            self.setSpan(row * 2, 0, 2, 1)

    def clickingHandler(self, item: QTableWidgetItem):
        """
        Handler when a table item is clicked
        :param item: clicked table item
        """
        actor_id = int(item.row() / 2) + 1
        self.actor_personal_window = ActorPersonalWindow(actor_id)
        self.actor_personal_window.show()