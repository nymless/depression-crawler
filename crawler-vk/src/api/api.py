import logging
import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from vk_data_collector import create_collector

from src.crawler.crawler import Crawler

app = FastAPI()

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


class CollectDataRequest(BaseModel):
    groups: List[str]
    target_date: str


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception):
    log.exception("Unhandled error")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )


@app.get("/status")
def get_status():
    """Get the current status of the crawler."""
    status = crawler.status_manager.get_status()
    return status


@app.post("/stop")
def stop_crawler():
    """Request the crawler to stop its current work."""
    crawler.status_manager.request_stop()
    log.info("Crawler stop requested")
    return {"status": "stop_requested"}


@app.post("/collect")
def collect_data(
    request: CollectDataRequest, background_tasks: BackgroundTasks
):
    """
    Start data collection for specified groups up to target date.
    """
    try:
        # Validate date format
        datetime.strptime(request.target_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}

    if not request.groups:
        return {"error": "No groups specified"}

    # Check if crawler is already working
    current_status = crawler.status_manager.get_status()
    if current_status["state"] != "idle":
        return {
            "error": f"Crawler is already working: {current_status['state']}",
            "current_status": current_status,
        }

    background_tasks.add_task(
        crawler.collect_data,
        request.groups,
        request.target_date,
    )

    return {"status": "ok"}
