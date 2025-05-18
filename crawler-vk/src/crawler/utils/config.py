import os
from pathlib import Path

# Пути к файлам и директориям
BASE_DIR = Path(os.getenv("CRAWLER_DATA_DIR", "data"))
MODELS_DIR = Path("models")
RESOURCES_DIR = Path("resources")

# Параметры модели FastText
FASTTEXT_MODEL_URL = "https://vectors.nlpl.eu/repository/20/213.zip"
FASTTEXT_MODEL_NAME = "geowac_lemmas_none_fasttextskipgram_300_5_2020"

# Пути к словарям
DEPRESSION_DICTIONARY_PATH = RESOURCES_DIR / "depression_dictionary.json"

# Параметры обработки текста
MIN_TEXT_LENGTH = 50

# Пути к моделям
VECTORIZER_MODEL_PATH = MODELS_DIR / "vectorizer"
CLASSIFIER_MODEL_PATH = MODELS_DIR / "classifier"
