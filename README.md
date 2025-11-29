# stock-prediction-app

#### Development

1. Установить poetry.
2. Установка зависимостей
  ```
  poetry install
  ```
3. Запуск приложения
```
poetry run python stock_prediction_app.py
```


#### Build

Linux/MacOs
```shell
poetry run pyinstaller --onefile --noconsole --windowed --add-data 'resources:resources' stock_prediction_app.py
```

Windows
```shell
poetry run pyinstaller --onefile --noconsole --add-data 'resources;resources' stock_prediction_app.py
```

