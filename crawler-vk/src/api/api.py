import logging
import os

from fastapi import BackgroundTasks, FastAPI

from src.client.client import Client
from src.crawler.crawler import Crawler
from src.db.dal import DAL
from src.service.service import Service

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    filename="logs/crawler.log",
    filemode="a",
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
log = logging.getLogger(__name__)

# Initialize services
client = Client()
dal = DAL()
service = Service(client, dal)
crawler = Crawler(service, dal)

app = FastAPI()


def run_crawler():
    """Starts the crawler loop."""
    crawler.running = True
    log.info("Crawler started")
    while crawler.running:
        crawler.get_random_posts(3)
    log.info("Crawler stopped")


@app.post("/start")
def start_crawler(background_tasks: BackgroundTasks):
    """Starts the crawler in a background task."""
    if crawler.running:
        return {"status": "already running"}
    background_tasks.add_task(run_crawler)
    log.info("Crawler start command received")
    return {"status": "started"}


@app.post("/stop")
def stop_crawler():
    """Stops the crawler and closes the database connection."""
    crawler.running = False
    log.info("Crawler stop command received, database connection closed")
    return {"status": "stopping"}


@app.get("/status")
def get_status():
    """Returns the current status of the crawler."""
    return {"running": crawler.running}
