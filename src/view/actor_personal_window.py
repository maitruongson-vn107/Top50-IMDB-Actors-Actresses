from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QFontMetrics
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, \
    QComboBox, QHBoxLayout, QLabel

from src.controllers.actor_controller import getOneActorInfoById
from src.controllers.award_controller import getAwardsCountByActorID, getAwardsListByActorID
from src.controllers.film_controller import getFilmsCountByActorId, getAverageRatingByActorID
from src.controllers.genre_controller import getGenresByActorID
from src.utils import text_utils
from src.view.components.actor_info_label import ActorInfoLabel
from src.view.components.actor_subtitle_label import ActorSubTitleLabel
from src.view.components.actor_title_label import ActorTitleLabel
from src.view.components.award_table_widget import AwardTableWidget
from src.view.components.film_table_widget import FilmTableWidget


class ActorPersonalWindow(QScrollArea):
    def __init__(self, actor_id):
        super(ActorPersonalWindow, self).__init__()
        self.film_rating_stats = {}
        self.rating_layout = QHBoxLayout
        self.film_rating_label = QLabel()
        self.film_rating_box = QComboBox()
        self.vbox = QVBoxLayout()
        self.overall_year = "Overall"
        self.load_personal_data(actor_id=actor_id)
        self.load_film_data(actor_id=actor_id)
        self.load_award_data(actor_id=actor_id)
        self.setUI()

    def setUI(self):
        actor_personal_widget = QWidget()
        actor_personal_widget.setFixedWidth(800)
        actor_personal_widget.setLayout(self.vbox)
        self.setWidget(actor_personal_widget)
        self.setGeometry(500, 500, 800, 800)

    def load_personal_data(self, actor_id):
        self.vbox = QVBoxLayout()
        actor_info = getOneActorInfoById(actor_id=actor_id)

        # NAME CONTAINER
        actor_name = actor_info[1]
        self.setWindowTitle(actor_name.upper())
        actor_birth_name = actor_info[2]
        actor_full_name = f"{actor_name}\n({actor_birth_name})"

        actor_name_label = ActorInfoLabel(actor_full_name)
        bold = QFont()
        bold.setBold(True)
        bold.setPointSize(20)
        actor_name_label.setFont(bold)
        actor_name_label.setStyleSheet("QLabel { background-color : #deb522; color : #0c0b00; }")
        self.vbox.addWidget(actor_name_label)

        # ABOUT CONTAINER
        actor_nick_name = actor_info[3]
        actor_dob = text_utils.birthdayConvert(actor_info[4])
        actor_origin = (actor_info[5])
        actor_height = actor_info[6].strip()

        actor_about_label = ActorInfoLabel(
            f"Nickname: {actor_nick_name}\n"
            f"D.O.B: {actor_dob}\n"
            f"Origin: {actor_origin}\n"
            f"Height: {actor_height}"
        ) if actor_nick_name != "" else ActorInfoLabel(
            f"D.O.B: {actor_dob}\n"
            f"Origin: {actor_origin}\n"
            f"Height: {actor_height}"
        )

        self.vbox.addWidget(actor_about_label)

        # GENERAL INFO CONTAINER
        actor_films_count = getFilmsCountByActorId(actor_id)
        actor_awards_count = getAwardsCountByActorID(actor_id)
        actor_genre_list = ',  '.join(getGenresByActorID(actor_id))
        actor_career_info = ActorInfoLabel(
            f"Total Films: {actor_films_count}\n"
            f"Total Awards: {actor_awards_count}\n"
            f"Top 5 Genres: {actor_genre_list}"
        )
        self.vbox.addWidget(actor_career_info)

        actor_bio = actor_info[8].replace(",", ", ").replace(".", ". ")
        actor_bio_label = ActorInfoLabel(actor_bio)
        painter = QPainter()
        metrics = QFontMetrics(actor_bio_label.font())
        elided = metrics.elidedText(actor_bio_label.text(), Qt.ElideRight, actor_bio_label.width())
        painter.drawText(actor_bio_label.rect(), actor_bio_label.alignment(), elided)
        actor_bio_label.setWindowFlags(Qt.Dialog)

        self.vbox.addWidget(actor_bio_label)

    def load_film_data(self, actor_id):
        # FILMOGRAPHY AREA
        films_title = ActorTitleLabel("Filmography")
        self.vbox.addWidget(films_title)

        films_table_widget = FilmTableWidget(actor_id)
        self.vbox.addWidget(films_table_widget)

        # RATING AREA
        self.film_rating_stats = getAverageRatingByActorID(actor_id)

        film_rating_title = ActorTitleLabel("Average Rating")
        self.vbox.addWidget(film_rating_title)

        self.rating_layout = QHBoxLayout()
        self.film_rating_box = QComboBox()
        self.film_rating_box.addItems(self.film_rating_stats.keys())
        self.film_rating_box.currentIndexChanged.connect(self.selection_change)

        self.film_rating_label = ActorSubTitleLabel(str(self.film_rating_stats["All Time"]))
        self.rating_layout.addWidget(self.film_rating_box)
        self.rating_layout.addWidget(self.film_rating_label)

        self.vbox.addLayout(self.rating_layout)

    def selection_change(self):
        self.overall_year = self.film_rating_box.currentText()
        self.film_rating_label.setText(str(self.film_rating_stats[self.overall_year]))

    def load_award_data(self, actor_id):
        # AWARD AREA
        award_title = ActorTitleLabel("Awards")
        self.vbox.addWidget(award_title)

        awards_dict = getAwardsListByActorID(actor_id)
        awards_table_widget = AwardTableWidget(awards_dict)
        self.vbox.addWidget(awards_table_widget)