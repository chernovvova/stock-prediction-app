from dataclasses import dataclass

REQUIRED_DATASET_COLUMNS = ('Date', 'Time', 'Open', 'High', 'Low', 'OpenInterest')

@dataclass
class ModelConfig:
    """Оптимальные параметры на основе экспериментов"""
    # Параметры данных
    TIME_STEPS = 12  # Оптимум между 10-15
    TEST_SIZE = 0.2  # 20% на тест (вместо фиксированного числа)

    # Параметры обучения
    EPOCHS = 50
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001

    # Регуляризация
    DROPOUT = 0.35
    L2_REG = 0.01

    # Callbacks
    EARLY_STOP_PATIENCE = 15
    REDUCE_LR_PATIENCE = 7
    REDUCE_LR_FACTOR = 0.5