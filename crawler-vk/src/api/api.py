import logging
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from vk_data_collector import create_collector

from src.crawler.crawler import Crawler

# Load environment variables before importing settings
load_dotenv()

from src.config import settings  # noqa: E402

app = FastAPI()
log = logging.getLogger(__name__)

# Initialize services
collector = create_collector(settings.service_token)
crawler = Crawler(collector)


class CollectDataRequest(BaseModel):
    groups: List[str] = Field(
        ..., min_items=1, description="List of group names to collect data from"
    )
    target_date: str = Field(..., description="Date in YYYY-MM-DD format")

    @field_validator("target_date")
    @classmethod
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


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
    # Check if crawler is already working
    current_status = crawler.status_manager.get_status()
    if current_status["state"] != "idle":
        return {
            "error": f"Crawler is already working: {current_status['state']}",
            "current_status": current_status,
        }

    background_tasks.add_task(
        crawler.run_pipeline,
        request.groups,
        request.target_date,
    )

    return {"status": "ok"}


@app.post("/reset")
async def reset_status():
    """Reset crawler status."""
    crawler.status_manager.reset()
    return {"status": "ok"}
