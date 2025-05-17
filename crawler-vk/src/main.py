import logging

from client.client import Client
from crawler.crawler import Crawler
from db.dal import DAL
from service.service import Service

if __name__ == "__main__":
    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    log = logging.getLogger(__name__)

    # Initialize services
    client = Client()
    dal = DAL()
    service = Service(client, dal)
    crawler = Crawler(service, dal)

    # Start crawler
    log.info("Crawler started")
    for _ in range(10):
        crawler.get_random_posts(3)
    log.info("Crawler stopped")
