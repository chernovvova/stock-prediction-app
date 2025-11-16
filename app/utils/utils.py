import os
import sys

import keras
import pandas as pd

from datetime import timedelta

from app.utils.constants import REQUIRED_DATASET_COLUMNS


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def load_data_from_csv(file_path : str) -> pd.DataFrame | None:
    """Получить данные для отрисовки графика биржевых котировок из csv файла"""
    data = pd.read_csv(file_path)

    if any(column not in data.columns for column in REQUIRED_DATASET_COLUMNS):
        raise ValueError

    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data[['DateTime'] + data.columns.drop('DateTime').tolist()]
    data["DateTime"] = pd.to_datetime(data["DateTime"])

    last_week_data = data[data["DateTime"] >= (data["DateTime"][len(data) - 1] - timedelta(days=7))]

    last_week_data['CCI'] = calculate_cci(data['High'], data['Low'], data['Close'])
    last_week_data = last_week_data.drop(columns=['Date', 'Time', 'Open', 'High', 'Low', 'OpenInterest'])

    return last_week_data


def predict_values(count_predictions: int) -> pd.DataFrame:
    """Предсказание значений"""
    model = keras.models.load_model(resource_path('app/models/model.keras'))
    model.summary()


def calculate_cci(high, low, close, window=20):
    """Вычисление индекса CCI"""
    typical_price = (high + low + close) / 3

    sma_tp = typical_price.rolling(window=window).mean()

    mean_deviation = abs(typical_price - sma_tp).rolling(window=window).mean()

    # CCI
    cci = (typical_price - sma_tp) / (0.015 * mean_deviation)

    return cci


def chunk_normalize_simple(series, chunk_size=48):
    """Нормализация данных"""
    normalized = pd.Series(index=series.index, dtype=float)
    n_chunks = (len(series) + chunk_size - 1) // chunk_size

    for i in range(n_chunks):
        ms = []
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(series))

        chunk_data = series.iloc[start_idx:end_idx]

        if len(chunk_data) > 0:
            chunk_mean = chunk_data.mean()
            chunk_max = chunk_data.max()
            chunk_min = chunk_data.min()
            chunk_range = chunk_max - chunk_min

            if chunk_range > 0:
                normalized.iloc[start_idx:end_idx] = (chunk_data - chunk_mean) / chunk_range
            else:
                normalized.iloc[start_idx:end_idx] = 0

            if end_idx == len(series):
                ms = [chunk_mean, chunk_range]

    return normalized, ms