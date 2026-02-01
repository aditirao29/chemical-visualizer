from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class BarChartCanvas(FigureCanvas):
    def __init__(self, distribution, parent=None):
        fig = Figure(figsize=(5, 3))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)

        self.plot(distribution)

    def plot(self, distribution):
        self.ax.clear()

        labels = list(distribution.keys())
        values = list(distribution.values())

        self.ax.bar(labels, values)
        self.ax.set_title("Equipment Type Distribution")
        self.ax.set_ylabel("Count")
        self.ax.set_xlabel("Equipment Type")

        self.draw()