from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from src.controllers.actor_controller import getAgeStats


def add_labels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha='center')


class AgeBarChart(QVBoxLayout):
    def __init__(self):
        super(AgeBarChart, self).__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.addWidget(self.canvas)
        self.draw_bar_chart()

    def draw_bar_chart(self):
        ages_count = getAgeStats()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        data = list(ages_count.values())
        labels = list(ages_count.keys())
        ax.bar(labels, data, color='#DEB522')
        add_labels(labels, data)
        ax.set_xlabel("Age Range")
        ax.set_ylabel("Number of actors/actresses")
        self.canvas.draw()
