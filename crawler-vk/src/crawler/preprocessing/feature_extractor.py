import json
from collections import Counter
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class DepressionFeatureExtractor:
    def __init__(self, dictionary_path: str):
        with open(dictionary_path, "r") as f:
            self.depression_dictionary = json.load(f)
        self.bow_vector_feature = "depression_bow_vector"
        self.bow_count_feature = "depression_words_count"

    def extract_depression_features(
        self, tokenized_text: List[str]
    ) -> Tuple[np.ndarray, int]:
        word_counts = Counter(tokenized_text)
        bow_vector = np.array(
            [word_counts[word] for word in self.depression_dictionary]
        )
        total_count = int(np.sum(bow_vector))
        return bow_vector, total_count

    def prepare_bow_features(self, data: pd.DataFrame) -> pd.DataFrame:
        bow_df = (
            data[self.bow_vector_feature]
            .apply(pd.Series)
            .fillna(0)
            .astype(float)
        )
        bow_df.columns = [f"bow_{col}" for col in bow_df.columns]

        data = pd.concat([data, bow_df], axis=1)
        data[self.bow_count_feature] = bow_df.sum(axis=1)

        row_sums = bow_df.sum(axis=1).replace(0, 1)
        data[bow_df.columns] = bow_df.div(row_sums, axis=0)

        scaler = MinMaxScaler()
        data[[self.bow_count_feature]] = scaler.fit_transform(
            data[[self.bow_count_feature]]
        )

        return data
