from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class AwardTableWidget(QTableWidget):
    def __init__(self, awards_dict):
        super(AwardTableWidget, self).__init__()
        self.awards_dict = awards_dict
        self.set_col_row()
        self.load_data()
        self.set_style()

    def set_col_row(self):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(("Year", "Outcome", "Title"))

    def insertAward(self, award_info):
        self.insertRow(self.rowCount())

        award_outcome = QTableWidgetItem(award_info[0])
        award_outcome.setTextAlignment(Qt.AlignCenter)
        self.setItem(self.rowCount() - 1, 1, award_outcome)

        award_title = QTableWidgetItem(award_info[1])
        award_title.setTextAlignment(Qt.AlignCenter)
        self.setItem(self.rowCount() - 1, 2, award_title)

        award_year = QTableWidgetItem(str(award_info[2]))
        award_year.setTextAlignment(Qt.AlignCenter)
        self.setItem(self.rowCount() - 1, 0, award_year)

    def load_data(self):
        for category in self.awards_dict.keys():
            # INSERT CATEGORY ROW
            self.insertRow(self.rowCount())
            self.setSpan(self.rowCount() - 1, 0, 1, 3)
            category_item = QTableWidgetItem(category)
            category_item.setTextAlignment(Qt.AlignCenter)
            category_item.setForeground(QColor(18, 139, 181))

            bold = QFont()
            bold.setBold(True)

            category_item.setFont(bold)
            self.setItem(self.rowCount() - 1, 0, category_item)

            cate_awards_list = self.awards_dict[category]
            for award_info in cate_awards_list:
                self.insertAward(award_info)

    def set_style(self):
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 200)
        self.horizontalHeader().setStretchLastSection(True)
