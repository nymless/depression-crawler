import logging
import random
from datetime import UTC, datetime
from typing import cast

from src.crawler.status_manager import CrawlerStatusManager
from src.db.dal import DAL
from src.service.service import Service
from src.vk_types.response.newsfeed_search import NewsfeedSearch
from src.vk_types.vk_api_objects.post import Post

log = logging.getLogger(__name__)


class Crawler:
    """
    Crawler for collecting posts from VK.
    """

    POSTS_PER_REQUEST = 10

    def __init__(self, service: Service, dal: DAL) -> None:
        self.service = service
        self.dal = dal
        self.status_manager = CrawlerStatusManager()

    def _get_random_letters(self, n: int) -> str:
        """
        Generates a string of n random letters from the Russian alphabet.
        """
        letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        return "".join(random.choices(letters, k=n))

    def _save_post(self, request_id: int, post: Post) -> None:
        """
        Saves a post to the database and updates the saved posts counter.
        """
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
        self.status_manager.increment_saved_posts()

    def process_posts(self, count: int = 10) -> None:
        """
        Generates a query, performs a post search, and saves the posts.
        """
        query = self._get_random_letters(3)
        log.info(f"Searching for posts with query: {query}")
        response = self.service.search_posts_by_query(query=query, count=count)
        self.status_manager.increment_requests()
        if response.is_success:
            response.data = cast(NewsfeedSearch, response.data)
            posts = response.data["response"]["items"]
            texts = []
            for post in posts:
                """
                A 3-letters search may return reposts of the same post
                from diffent groups or users without any markers.
                Therefore, we check the first 20 characters of the text within
                one request to ensure uniqueness, and skip saving duplicates
                to the database.
                """
                if post["text"][:20] in texts:
                    continue
                texts.append(post["text"][:20])
                self._save_post(response.request_id, post)
                log.info(f"Post {post['owner_id']}_{post['id']} processed")

    def run(self) -> None:
        """
        Main crawler loop: starts, processes posts, and resets counters after
        stopping.
        """
        self.status_manager.start()
        log.info("Crawler started")
        try:
            while self.status_manager.get_status()["running"]:
                self.process_posts(Crawler.POSTS_PER_REQUEST)
        finally:
            self.status_manager.reset()
            log.info("Crawler stopped")
