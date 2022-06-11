from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

from src.controllers.actor_controller import getOriginStats


def auto_pct_func(pct, data):
    absolute = int(pct / 100. * np.sum(data))
    return absolute


class OriginPieChart(QVBoxLayout):
    def __init__(self):
        super(OriginPieChart, self).__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.addWidget(self.canvas)
        self.draw_pie_chart()

    def draw_pie_chart(self):
        origins_count = getOriginStats()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        labels = list(origins_count.keys())
        data = list(origins_count.values())
        explode = (0.1, 0, 0, 0)
        colors = ['#C4B454', '#DEB522', '#FFD700', '#F8DE7E']
        ax.pie(data, labels=labels, startangle=90,
               autopct=lambda pct: auto_pct_func(pct, data),
               colors=colors, explode=explode)
        self.canvas.draw()
