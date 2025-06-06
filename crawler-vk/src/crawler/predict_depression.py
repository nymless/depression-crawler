import json
import logging

import numpy as np
import pandas as pd

from src.config import settings
from src.crawler.model_loader.model_loader import ModelLoader

log = logging.getLogger(__name__)


def predict_depression(data: pd.DataFrame) -> None:
    """Predict depression for posts and comments.
    Modifies input DataFrame by adding depression predictions.

    Args:
        data: DataFrame with embeddings and features to predict on
    """
    try:
        # Initialize model
        model_loader = ModelLoader(
            vectorizer_model_path=settings.vectorizer_model_path,
            classifier_model_path=settings.classifier_model_path,
        )
        model_path = model_loader.fetch_classifier_model(
            settings.classifier_model_gdrive_id
        )
        model = model_loader.load_classifier_model(model_path)

        # Prepare features list
        with open(
            settings.classifier_model_path.joinpath("selected_features.json"),
            "r",
        ) as f:
            selected_features = json.load(f)

        # Prepare embeddings and features
        embeddings = np.array(data["embeddings"].to_list())
        features = data[selected_features].to_numpy()

        # Combine embeddings and features
        combined = np.hstack((embeddings, features))

        # Use model
        predictions = model.predict(combined)

        # Add predictions to original data
        data["depression_prediction"] = predictions
    except Exception as e:
        log.exception(
            "Error predicting depression",
            exc_info=e,
        )
        raise
