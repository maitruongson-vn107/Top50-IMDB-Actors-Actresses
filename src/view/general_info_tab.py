from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QDialog, QDialogButtonBox
from src.controllers.actor_controller import getOriginStats
from src.controllers.film_controller import getTotalFilmsCount
from src.controllers.award_controller import getTotalAwardsCount

from src.view.components.actor_info_label import ActorInfoLabel
from src.view.components.actor_title_label import ActorTitleLabel

from src.data.crawler import crawlMainPage
from src.view.components.age_bar_chart import AgeBarChart
from src.view.components.origins_pie_chart import OriginPieChart


def open_confirm_dialog():
    """
    Confirmation Dialog when user click "Update Data" button
    """
    confirm_dialog = QDialog()
    confirm_dialog.setWindowTitle("Data Update Confirmation")
    QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    confirm_dialog.buttonBox = QDialogButtonBox(QBtn)
    confirm_dialog.buttonBox.accepted.connect(accept_update_data)
    confirm_dialog.buttonBox.rejected.connect(confirm_dialog.reject)

    layout = QVBoxLayout()
    message = QLabel("Data update will take about 2 hours.\nAre you sure to continue?")
    layout.addWidget(message)
    layout.addWidget(confirm_dialog.buttonBox)
    confirm_dialog.setLayout(layout)
    confirm_dialog.exec()


def accept_update_data():
    crawlMainPage()


class GeneralInfoTab(QVBoxLayout):
    def __init__(self):
        super(GeneralInfoTab, self).__init__()
        self.load_data()

    def load_data(self):
        # LOGO & UPDATE BUTTON
        update_btn = QPushButton("Update Data")
        update_btn.setStyleSheet(("QPushButton { background-color: #128bb5; border-radius: 4px; "
                                  "height: 40px; width: 200px; font-size: 15px; color: #fcf7f7}"
                                  "QPushButton:pressed { background-color: #4682B4 }"))

        update_btn.clicked.connect(open_confirm_dialog)

        imdb_image = QPixmap("../assets/IMDB_Logo_2016.png")
        imdb_logo_label = QLabel()
        imdb_logo_label.setPixmap(imdb_image.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio))
        self.addWidget(imdb_logo_label)
        self.addWidget(update_btn)

        # TITLE CONTAINER
        title_label = ActorTitleLabel("GENERAL STATISTICS")
        big_bold = QFont()
        big_bold.setBold(True)
        big_bold.setPointSize(20)
        title_label.setFont(big_bold)
        self.addWidget(title_label)

        # GENERAL STATISTICS CONTAINER
        total_films_count = getTotalFilmsCount()
        total_award_count = getTotalAwardsCount()

        actor_about_label = ActorInfoLabel(
            f"Actors: 50\n"
            f"Total Films: {total_films_count}\n"
            f"Total Awards: {total_award_count}"
        )
        small_bold = QFont()
        small_bold.setBold(True)
        small_bold.setPointSize(15)
        actor_about_label.setFont(small_bold)

        self.addWidget(actor_about_label)

        # ORIGINS COUNT
        origins_title = ActorTitleLabel("Where are they from?")
        self.addWidget(origins_title)
        origins_pie_chart = OriginPieChart()
        self.addLayout(origins_pie_chart)

        # AGE COUNT
        age_title = ActorTitleLabel("How old are they?")
        self.addWidget(age_title)
        age_bar_chart = AgeBarChart()
        self.addLayout(age_bar_chart)
