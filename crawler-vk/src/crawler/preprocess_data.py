import logging
from typing import List

import numpy as np
import pandas as pd
from gensim.models.fasttext import FastTextKeyedVectors

from src.crawler.model_loader.model_loader import ModelLoader
from src.crawler.preprocessing.feature_extractor import (
    DepressionFeatureExtractor,
)
from src.crawler.preprocessing.text_processor import TextProcessor
from src.crawler.utils.config import (
    DEPRESSION_DICTIONARY_PATH,
    FASTTEXT_MODEL_NAME,
    FASTTEXT_MODEL_URL,
    MIN_TEXT_LENGTH,
    VECTORIZER_MODEL_PATH,
)

log = logging.getLogger(__name__)


def preprocess_data(
    posts_files: List[str], comments_files: List[str]
) -> pd.DataFrame:
    """Preprocess posts and comments data.

    Args:
        posts_files: List of paths to posts JSON files
        comments_files: List of paths to comments JSON files

    Returns:
        DataFrame with preprocessed data
    """
    # Load and merge data
    posts = pd.concat([pd.read_json(path) for path in posts_files])
    comments = pd.concat([pd.read_json(path) for path in comments_files])

    publications = pd.concat(
        [
            posts[["owner_id", "id", "text"]],
            comments[["owner_id", "post_id", "id", "text"]],
        ],
        ignore_index=True,
        join="outer",
    )
    posts = None
    comments = None

    # Cast types
    publications["post_id"] = publications["post_id"].fillna(0.0)
    publications["post_id"] = publications["post_id"].astype(np.int64)
    publications["owner_id"] = publications["owner_id"].astype(np.int64)
    publications["id"] = publications["id"].astype(np.int64)

    # Filter by text length
    publications["text"] = publications["text"].fillna("")
    publications = publications[
        publications["text"].apply(lambda x: len(x) > MIN_TEXT_LENGTH)
    ]

    # Initialize processors
    text_processor = TextProcessor()
    feature_extractor = DepressionFeatureExtractor(
        str(DEPRESSION_DICTIONARY_PATH)
    )
    model_loader = ModelLoader(models_dir=VECTORIZER_MODEL_PATH)

    # Process text
    publications["text"] = publications["text"].apply(text_processor.clean_text)
    publications["tokens"] = publications["text"].apply(
        text_processor.tokenize_text
    )

    # Filter empty tokens
    publications = publications[publications["tokens"].apply(len) > 0]

    # Extract features
    publications[
        [
            feature_extractor.bow_vector_feature,
            feature_extractor.bow_count_feature,
        ]
    ] = (
        publications["tokens"]
        .apply(feature_extractor.extract_depression_features)
        .apply(pd.Series)
    )

    # Prepare BOW features
    publications = feature_extractor.prepare_bow_features(publications)
    publications = publications.drop(
        columns=[feature_extractor.bow_vector_feature], index=False
    )

    # Load FastText model
    model_path = model_loader.fetch_model(
        FASTTEXT_MODEL_URL, FASTTEXT_MODEL_NAME
    )
    model = model_loader.load_fasttext_model(model_path)

    def get_embeddings(
        model: FastTextKeyedVectors, lemmas: list[str]
    ) -> list[np.ndarray]:
        embeddings = []
        for lemma in lemmas:
            try:
                embeddings.append(model[lemma])
            except KeyError:
                # Skip words that are not in the model's vocabulary
                continue
        return embeddings

    # Extract word embeddings for each token
    publications["embeddings"] = publications["tokens"].apply(
        lambda x: get_embeddings(model, x)
    )

    # Calculate mean embeddings
    publications["embeddings"] = publications["embeddings"].apply(
        lambda x: np.mean(x, axis=0)
    )

    # Filter rows with empty embeddings
    publications = publications[publications["embeddings"].apply(len) > 0]

    return publications
