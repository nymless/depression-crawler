import logging
import random
from datetime import UTC, datetime
from typing import cast

from db.dal import DAL
from service.service import Service
from vk_types.response.newsfeed_search import NewsfeedSearch
from vk_types.vk_api_objects.post import Post

log = logging.getLogger(__name__)


class Crawler:
    """Crawler for collecting posts from VK."""

    # Flag to indicate whether the crawler is running
    running: bool = False

    def __init__(self, service: Service, dal: DAL) -> None:
        """Initialize the crawler with the given service and data access
        layer."""
        self.service = service
        self.dal = dal

    def _get_random_letters(self, n: int) -> str:
        """Generate a string of N random letters from the Russian alphabet."""
        letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        return "".join(random.choices(letters, k=n))

    def _save_post(self, request_id: int, post: Post) -> None:
        """Save a collected post to the database."""
        timestamp = datetime.fromtimestamp(post["date"], UTC).isoformat()
        owner_type = "group" if post["owner_id"] < 0 else "user"
        self.dal.save_post(
            request_id=request_id,
            owner_type=owner_type,
            owner_id=post["owner_id"],
            post_id=post["id"],
            text=post["text"],
            likes=post["likes"]["count"],
            reposts=post["reposts"]["count"],
            comments=post["comments"]["count"],
            timestamp=timestamp,
        )
        log.info(f"Post {post['owner_id']}_{post['id']} saved")

    def get_random_posts(self, count: int = 10) -> None:
        """Retrieve random posts using a generated query."""
        letters = self._get_random_letters(3)
        log.info(f"Searching for posts with query: {letters}")
        response = self.service.search_posts_by_query(
            query=letters, count=count
        )
        if response.is_success:
            response.data = cast(NewsfeedSearch, response.data)
            posts = response.data["response"]["items"]
            for post in posts:
                self._save_post(response.request_id, post)
                log.info(f"Post {post['owner_id']}_{post['id']} processed")
