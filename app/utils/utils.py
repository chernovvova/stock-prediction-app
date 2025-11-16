import os
import sys

import keras
import numpy as np
import pandas as pd

from datetime import timedelta

from app.utils.constants import REQUIRED_DATASET_COLUMNS, ModelConfig


def resource_path(relative_path: str) -> str:
    """Возвращает путь к ресурсу, совместимый с PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


def load_data_from_csv(file_path : str) -> pd.DataFrame | None:
    """Получить данные для отрисовки графика биржевых котировок из csv файла"""
    data = pd.read_csv(file_path)

    if any(column not in data.columns for column in REQUIRED_DATASET_COLUMNS):
        raise ValueError

    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data[['DateTime'] + data.columns.drop('DateTime').tolist()]
    data["DateTime"] = pd.to_datetime(data["DateTime"])

    data['CCI'] = calculate_cci(data['High'], data['Low'], data['Close'])
    data = data.drop(columns=['Date', 'Time', 'Open', 'High', 'Low', 'OpenInterest'])

    return data


def predict_values(stock_data: pd.DataFrame):
    """Предсказание значений"""
    model = keras.models.load_model(resource_path('resources/model.keras'))

    df = stock_data.copy()

    df = df.iloc[38:].reset_index(drop=True)

    df['Close'], mass_c = chunk_normalize_simple(df['Close'], 48)
    df['Volume'], mass_v = chunk_normalize_simple(df['Volume'], 48)

    df['CCI_Flag'] = 0
    df.loc[df['CCI'] < -100, 'CCI_Flag'] = -1
    df.loc[df['CCI'] > 100, 'CCI_Flag'] = 1

    df['CCI'] = np.clip(df['CCI'], -200, 200)
    df['CCI'] = (df['CCI'] + 200) / 400.0

    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.set_index('DateTime', inplace=True)

    features = df.copy()

    X, y = create_sequences(features, ModelConfig.TIME_STEPS)

    test_size = int(len(X) * ModelConfig.TEST_SIZE)
    train_size = len(X) - test_size

    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    data = X_test[-10:]
    y_predictions = model.predict(data)
    y_real = df[-10:]

    before_predictions = stock_data[
        stock_data['DateTime'] >= (stock_data['DateTime'][len(stock_data) - 1] - timedelta(days=7))
    ][:-10]

    last_before_predictions = before_predictions.iloc[[len(before_predictions) - 1]]

    predictions_denormalized = pd.DataFrame({
        'DateTime': pd.to_datetime(y_real.index.values),
        'Close': denormalize(y_predictions, mass_c),
    })
    predictions_denormalized = pd.concat([last_before_predictions, predictions_denormalized], ignore_index=True)
    after_predictions = pd.DataFrame({
        'DateTime': pd.to_datetime(y_real.index.values),
        'Close': stock_data['Close'].values[-10:],
    })
    after_predictions = pd.concat([last_before_predictions, after_predictions], ignore_index=True)
    return before_predictions, predictions_denormalized, after_predictions


def calculate_cci(high, low, close, window=20):
    """Вычисление индекса CCI"""
    typical_price = (high + low + close) / 3

    sma_tp = typical_price.rolling(window=window).mean()

    mean_deviation = abs(typical_price - sma_tp).rolling(window=window).mean()

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


def create_sequences(data, time_steps):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data.iloc[i:(i + time_steps)].values)
        y.append(data.iloc[i + time_steps]['Close'])
    return np.array(X), np.array(y)


def denormalize(pred, mass_c):
    tmp = []
    for i in range(len(pred)):
        tmp.append((pred[i] * mass_c[1] + mass_c[0])[0])

    return tmp
