import logging
from typing import List

import pandas as pd

log = logging.getLogger(__name__)


def preprocess_groups(
    groups_files: List[str],
) -> pd.DataFrame:
    """Preprocess groups data.

    Args:
        groups_files: List of paths to groups JSON files

    Returns:
        DataFrame with preprocessed data
    """
    # Load and merge data
    groups = pd.concat([pd.read_json(path) for path in groups_files])

    return groups[["id", "name", "screen_name", "is_closed", "type"]]
