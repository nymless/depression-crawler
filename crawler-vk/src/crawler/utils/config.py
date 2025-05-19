import os
from pathlib import Path

# Get project root directory (one level up from current directory)
PROJECT_ROOT = Path.cwd().parent

# Пути к файлам и директориям
BASE_DIR = Path(os.getenv("CRAWLER_DATA_DIR", str(PROJECT_ROOT / "data")))
CRAWLER_DIR = PROJECT_ROOT / "crawler-vk"
RESOURCES_DIR = CRAWLER_DIR / "resources"

# Параметры модели FastText
FASTTEXT_MODEL_URL = "https://vectors.nlpl.eu/repository/20/213.zip"
FASTTEXT_MODEL_NAME = "geowac_lemmas_none_fasttextskipgram_300_5_2020"

# Пути к словарям
DEPRESSION_DICTIONARY_PATH = RESOURCES_DIR / "depression_dictionary.json"

# Параметры обработки текста
MIN_TEXT_LENGTH = 50

# Пути к моделям
MODELS_DIR = PROJECT_ROOT / "models"
VECTORIZER_MODEL_PATH = MODELS_DIR / "vectorizer"
CLASSIFIER_MODEL_PATH = MODELS_DIR / "classifier"
