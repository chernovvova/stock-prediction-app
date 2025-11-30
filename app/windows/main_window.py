from datetime import timedelta
import pyqtgraph as pg

import pandas as pd
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from app.utils.utils import load_data_from_csv, predict_next_value
from app.widgets.plot_widget import PlotWidget


class MainWindow(QMainWindow):
    _stock_data: pd.DataFrame | None = None

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

        self._stock_data = stock_data

        self.plot_widget.clear_plot()
        last_week_data = stock_data[
            stock_data["DateTime"] >= (stock_data["DateTime"][len(stock_data) - 1] - timedelta(days=7))
        ][:-1]
        self.plot_widget.update_plot(
            data=last_week_data,
            pen=pg.mkPen('b', width=3),
            symbol='o',
            symbol_brush='b',
            name='Данные до предсказания'
        )

    def make_prediction(self):
        before_predictions, predictions_denormalized, after_predictions = predict_next_value(self._stock_data)
        self.plot_widget.last_index -= 1
        self.plot_widget.update_plot(
            data=predictions_denormalized,
            pen=pg.mkPen('r', width=3),
            symbol='o',
            symbol_brush='r',
            name='Предсказанные значения',
        )
        self.plot_widget.last_index -= len(predictions_denormalized)
        self.plot_widget.update_plot(
            data=after_predictions,
            pen=pg.mkPen('y', width=3),
            symbol='o',
            symbol_brush='y',
            name='Настоящие значения',
        )
