import logging
from datetime import date

import psycopg2

from src.db.db import add_group, create_crawler_run, save_predictions

log = logging.getLogger(__name__)


class DepressionDataHandler:
    """Handles saving depression predictions data to the database."""

    def __init__(
        self,
        conn: psycopg2.extensions.connection,
        groups: list[str],
        target_date: date,
    ) -> None:
        """
        Initialize the handler.

        Args:
            conn: Database connection
            groups: List of VK group names to analyze
            target_date: Target date for the analysis
        """
        self.conn = conn
        self.groups = groups
        self.target_date = target_date

    def start_run(self) -> int:
        """
        Create a new crawler run record and link it with groups.

        Returns:
            ID of the created run
        """
        return create_crawler_run(
            conn=self.conn,
            target_date=self.target_date,
            group_ids=[int(group) for group in self.groups],
        )

    def add_group(self, group_id: int, name: str) -> None:
        """
        Add a new group or update existing one.

        Args:
            group_id: VK group ID
            name: Group name
        """
        add_group(conn=self.conn, group_id=group_id, name=name)

    def save_prediction(
        self,
        run_id: int,
        owner_id: int,
        post_id: int,
        vk_id: int,
        depression_prediction: bool,
    ) -> None:
        """
        Save a single prediction to the database.
        If a post with the same owner_id, post_id and vk_id already exists,
        the prediction will be skipped.

        Args:
            run_id: ID of the crawler run
            owner_id: VK group ID
            post_id: Post ID (0 for posts, actual post_id for comments)
            vk_id: Post ID for posts, comment ID for comments
            depression_prediction: Prediction result (True/False)
        """
        save_predictions(
            conn=self.conn,
            run_id=run_id,
            owner_id=owner_id,
            post_id=post_id,
            vk_id=vk_id,
            depression_prediction=depression_prediction,
        )
