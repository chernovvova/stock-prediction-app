import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        self.ax = self.figure.subplots()

        self.data = None
        self.prediction = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_from_file(file_path)

    def load_from_file(self, path: str):
        print("Loaded file:", path)
        self.data = 
        self.prediction = None
        self._update_plot()

    def add_prediction(self):
        if self.data is None:
            return

        last_value = self.data[-1]
        forecast = last_value + np.cumsum(np.random.randn(10))

        self.prediction = forecast
        self._update_plot()

    def _update_plot(self):
        self.ax.clear()

        if self.data is not None:
            self.ax.plot(self.data, color="black")

        if self.prediction is not None:
            start = len(self.data)
            x = list(range(start, start + len(self.prediction)))
            self.ax.plot(x, self.prediction, color="red")

        self.ax.set_ylabel("Цена")
        self.canvas.draw()
