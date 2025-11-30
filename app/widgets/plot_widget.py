from datetime import datetime

import numpy as np
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

        self.plot_item = None
        self.data_loaded = False
        self.addLegend()
        self.last_index = None
        self.ticks: set[str] = set()

    def update_plot(
        self,
        pen,
        symbol,
        symbol_brush,
        symbol_size=7,
        name: str = None,
        data: pd.DataFrame | None = None,
    ):
        """Обновить график"""
        if data is None or data.empty:
            return

        if self.last_index is None:
            x = np.arange(len(data['DateTime']))
            self.last_index = x[-1]
        else:
            x = np.arange(self.last_index, self.last_index + len(data['DateTime']))
            self.last_index = x[-1]
        y = data['Close'].to_numpy()

        self.plot(
            x,
            y,
            pen=pen,
            name=name,
            symbol=symbol,
            symbolBrush=symbol_brush,
            symbolSize=symbol_size,
        )

        for i, dt in enumerate(data['DateTime']):
            label = dt.strftime('%Y-%m-%d\n%H:%M')
            self.ticks.add(label)
        time_labels = sorted(
           list(self.ticks), key=lambda x: datetime.strptime(x, '%Y-%m-%d\n%H:%M').timestamp()
        )
        self.getAxis('bottom').setTicks([[(i, dt) for i, dt in enumerate(time_labels)]])

    def clear_plot(self):
        """Очистить график"""
        self.clear()
