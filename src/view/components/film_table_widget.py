from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class FilmTableWidget(QTableWidget):
    def __init__(self, films_list):
        super(FilmTableWidget, self).__init__()
        self.films_list = films_list
        self.set_col_row()
        self.load_data()
        self.set_style()

    def set_col_row(self):
        self.setColumnCount(4)
        self.setRowCount(len(self.films_list))
        self.setHorizontalHeaderLabels(("Name", "Year", "Rating", "Genres"))

    def load_data(self):
        for i in range(len(self.films_list)):
            film = self.films_list[i]
            film_name = QTableWidgetItem(film[2])
            bold = QFont()
            bold.setBold(True)
            film_name.setFont(bold)
            film_year = film[3]
            film_rating = film[4]
            film_genres = film[5].replace(",", ", ")

            self.setItem(i, 0, film_name)
            self.setItem(i, 1, QTableWidgetItem(str(film_year)))
            self.setItem(i, 2, QTableWidgetItem(str(film_rating)))
            self.setItem(i, 3, QTableWidgetItem(film_genres))

    def set_style(self):
        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 60)
        self.horizontalHeader().setStretchLastSection(True)
        self.setWordWrap(True)


