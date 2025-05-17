import logging
import os

from dotenv import load_dotenv
from vk_data_collector import create_collector

from src.crawler.crawler import Crawler


def main():
    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    log = logging.getLogger(__name__)

    # Initialize services
    load_dotenv()
    token = os.getenv("SERVICE_TOKEN")
    collector = create_collector(token)
    crawler = Crawler(collector)

    log.info("Crawler initialized")

    # groups = ["group_name"]
    # target_date = "2025-01-01"
    # crawler.collect_data(groups, target_date)


if __name__ == "__main__":
    main()
