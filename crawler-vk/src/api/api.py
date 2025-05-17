import logging

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse

from src.client.client import Client
from src.crawler.crawler import Crawler
from src.db.dal import DAL
from src.service.service import Service

app = FastAPI()

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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception):
    log.exception("Unhandled error")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )


@app.post("/start")
def start_crawler(background_tasks: BackgroundTasks):
    if crawler.status_manager.get_status()["running"]:
        return {"status": "already running"}
    background_tasks.add_task(crawler.run)
    log.info("Crawler start command received")
    return {"status": "started"}


@app.post("/stop")
def stop_crawler():
    crawler.status_manager.stop()
    log.info("Crawler stop command received")
    return {"status": "stopping"}


@app.get("/status")
def get_status():
    status = crawler.status_manager.get_status()
    return status
