from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from app.utils.utils import load_data_from_csv
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
        """Выбор файла данных"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите данные",
            "",
            "Data files (*.csv *.txt *.xlsx *.xls)"
        )

        file_extension = file_path.split('.')[-1]

        stock_data = None
        if file_extension == 'csv':
            try:
                stock_data = load_data_from_csv(file_path)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "CSV файл должен содержать столбцы 'DateTime' и 'Close'")
        else:
            raise NotImplementedError(f'Файлы с расширением {file_extension} не поддерживаются.')

        self.plot_widget.update_plot(data=stock_data)

    def make_prediction(self):
        self.plot_widget.add_prediction()
