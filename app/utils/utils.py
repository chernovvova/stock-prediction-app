import os
import sys

import keras
import pandas as pd

from datetime import timedelta


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def load_data_from_csv(file_path : str) -> pd.DataFrame | None:
    """Получить данные для отрисовки графика биржевых котировок из csv файла"""
    data = pd.read_csv(file_path)
    return data[['DateTime', 'Close']]