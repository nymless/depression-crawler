import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


class Client:
    """Basic client for making requests to the VK API."""

    base_url = "https://api.vk.com"

    _user_token = ""

    def __init__(self) -> None:
        """Class constructor.

        Raises:
            ValueError: SERVICE_TOKEN is missing in the .env file.
        """

        self.service_token = os.getenv("SERVICE_TOKEN")

        if not self.service_token:
            raise ValueError("SERVICE_TOKEN is missing in the .env file")

    def make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        user_token: str | None = None,
        v: str = "5.199",
    ):
        """Send a request to the VK API."""

        url = self.base_url + endpoint
        params["access_token"] = self.service_token
        params["v"] = v

        if user_token:
            params["access_token"] = user_token

        response = requests.get(url, params=params)
        return response
