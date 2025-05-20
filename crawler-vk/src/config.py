import logging
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    # Base paths
    project_root: Path = Path.cwd().parent
    crawler_dir: Path = project_root / "crawler-vk"
    resources_dir: Path = crawler_dir / "resources"
    logs_dir: Path = project_root / "logs"
    models_dir: Path = project_root / "models"
    base_dir: Path = project_root / "data"

    # API settings
    service_token: str

    # Model settings
    fasttext_model_url: str = "https://vectors.nlpl.eu/repository/20/213.zip"
    fasttext_model_name: str = "geowac_lemmas_none_fasttextskipgram_300_5_2020"
    min_text_length: int = 50

    # Model paths
    vectorizer_model_path: Path = models_dir / "vectorizer"
    classifier_model_path: Path = models_dir / "classifier"

    # Features
    depression_dictionary_path: Path = (
        resources_dir / "depression_dictionary.json"
    )
    bow_vector_feature: str = "depression_bow_vector"
    bow_count_feature: str = "depression_words_count"

    model_config = SettingsConfigDict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.logs_dir.mkdir(exist_ok=True, parents=True)
        self.base_dir.mkdir(exist_ok=True, parents=True)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            handlers=[
                logging.FileHandler(self.logs_dir / "crawler.log"),
                logging.StreamHandler(),
            ],
        )


settings = Settings()
