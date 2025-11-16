import pandas as pd
import pyqtgraph as pg


class PlotWidget(pg.PlotWidget):
    """Виджет графика биржевых котировок"""

    def __init__(self):
        super().__init__()

        self.setBackground('white')
        self.setLabel('left', 'Цена закрытия')
        self.setLabel('bottom', 'Время')
        self.setTitle('Интерактивный график биржевых котировок')
        self.showGrid(x=True, y=True, alpha=0.3)
        self.addLegend()

        self.date_axis = pg.DateAxisItem(orientation='bottom')
        self.setAxisItems({'bottom': self.date_axis})

        self.plot_item = None
        self.data_loaded = False

    def add_predictions(self):
        pass

    def update_plot(self, data: pd.DataFrame | None = None):
        """Обновить график"""
        if data is None or data.empty:
            return

        x = (data['DateTime'].astype("int64") / 1e9).to_numpy()
        y = data['Close'].to_numpy()

        self.plot(x, y, pen=pg.mkPen('b', width=2))

    def clear_plot(self):
        """Очистить график"""
        self.clear()