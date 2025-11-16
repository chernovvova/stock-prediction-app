from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog
)

from app.widgets.plot_widget import PlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Прогнозирование биржевых котировок")
        self.resize(900, 650)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.plot_widget = PlotWidget()
        layout.addWidget(self.plot_widget, stretch=1)

        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self.select_file_button = QPushButton("Выбрать файл")
        self.select_file_button.clicked.connect(self.select_file)
        bottom_layout.addWidget(self.select_file_button)

        self.predict_button = QPushButton("Прогноз")
        self.predict_button.clicked.connect(self.make_prediction)
        bottom_layout.addWidget(self.predict_button)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите данные",
            "",
            "Data files (*.csv *.txt *.xlsx *.xls)"
        )
        if file_path:
            self.plot_widget.load_from_file(file_path)

    def make_prediction(self):
        self.plot_widget.add_prediction()
