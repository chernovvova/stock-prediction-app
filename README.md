# stock-prediction-app


#### Build

Linux/MacOs
```shell
poetry run pyinstaller --onefile --noconsole --windowed --add-data 'resources:resources' main.py
```

Windows
```shell
poetry run pyinstaller --onefile --noconsole --add-data 'resources;resources' main.py
```

