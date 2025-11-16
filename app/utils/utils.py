import pandas as pd


def load_data_from_csv(file_path : str) -> pd.DataFrame:
    """Получить данные для отрисовки графика биржевых котировок из csv файла"""
    data = pd.read_csv(file_path)
    return data[['DateTime', 'Close']]