import logging
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    # Base paths
    crawler_root: Path = Path.cwd()
    resources_dir: Path = crawler_root / "./resources"
    data_dir: Path = crawler_root / "./data"
    logs_dir: Path = crawler_root / "./logs"
    models_dir: Path = crawler_root / "./models"

    # API settings
    service_token: str

    # Model urls
    vectorizer_model_url: str = "https://vectors.nlpl.eu/repository/20/213.zip"
    classifier_model_gdrive_id: str = "https://drive.google.com/uc?id=1tfEAATh00xiUxORls9bwm79bAMRG9EoU"
    
    # Skip texts less than min_text_length
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
        self.data_dir.mkdir(exist_ok=True, parents=True)
        self.vectorizer_model_path.mkdir(exist_ok=True, parents=True)
        self.classifier_model_path.mkdir(exist_ok=True, parents=True)

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
